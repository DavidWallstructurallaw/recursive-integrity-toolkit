"""Validate one explicitly ordered pair and its declared common state basis.

Owner IDs:
    T1, PR-007, PR-011; P3-D03 and Definitions 6.9.

Inputs:
    ExplicitPairContext, two explicit state-meaning declarations and an optional
    directed literal StateMappingDeclaration with full source/target descriptors.

Outputs:
    Detached immutable compatibility evidence and a harmonized descriptor. This
    module validates declarations; it does not assign records or calculate metrics.

Assumptions:
    State meanings are caller declarations, not independently certified semantics.
    Accepted Phase 2 ordering declarations supply chronology, never filenames.

Limits:
    No discovery, inference, one-to-many allocation, callable mappings, I/O,
    metrics, lineage, trajectory, model comparison or report generation.
    A many-to-one mapping changes the comparison basis; it does not establish
    equivalence of the original representations or restore lost distinctions.

Current phase status:
    Phase 3 Step 9 explicit representation compatibility only. Import-safe.
"""
from __future__ import annotations

from dataclasses import dataclass, field, replace
from types import MappingProxyType

from ..errors import CanonicalValidationError, ErrorCode
from ..io.validation import resolve_version_order
from ..models import CalculationScope, ExplicitPairContext, RecordKey, RepresentationDescriptor, VersionOrderResult


@dataclass(frozen=True, slots=True)
class StateMappingDeclaration:
    """A total-on-used-states, directed literal map; no implicit identity fallback."""

    direction: str
    source_representation: RepresentationDescriptor
    target_representation: RepresentationDescriptor
    source_state_semantics: str
    target_state_semantics: str
    state_mapping: object = field(repr=False)


@dataclass(frozen=True, slots=True)
class RepresentationCompatibility:
    """One explicit pair and its declared basis; no universal semantic certificate."""

    context: ExplicitPairContext
    earlier_state_semantics: str
    later_state_semantics: str
    harmonized_representation: RepresentationDescriptor
    harmonized_state_semantics: str
    method: str
    mapping: StateMappingDeclaration | None
    collision_groups: tuple[tuple[str, tuple[str, ...]], ...] = field(repr=False)
    limitations: tuple[str, ...] = (
        "State meaning is declared, not independently inferred or verified.",
        "Many-to-one mapping can hide original distinctions; original bases remain separately visible.",
        "Chronology alone does not establish lineage, causality or functional failure.",
    )


def _invalid(message: str, *, order: bool = False) -> CanonicalValidationError:
    return CanonicalValidationError(
        ErrorCode.VERSION_ORDER_CONFLICT if order else ErrorCode.REPRESENTATION_INCOMPATIBLE,
        message, field="pair_order" if order else "representation_compatibility",
    )


def _text(value: object, *, empty: bool = False) -> str:
    if type(value) is not str or (not value and not empty) or "\x00" in value:
        raise _invalid("pair declarations require literal text with explicit meaning")
    try:
        value.encode("utf-8")
    except UnicodeEncodeError:
        raise _invalid("pair declaration is not valid UTF-8") from None
    return value


def _scope(value: object) -> CalculationScope:
    if type(value) is not CalculationScope or type(value.dataset_versions) is not tuple or len(value.dataset_versions) != 1:
        raise _invalid("each comparison side requires one explicit dataset-version scope")
    _text(value.dataset_versions[0]); _text(value.scope_id); _text(value.denominator_basis)
    try:
        RecordKey(value.dataset_versions[0], "scope-check")
    except (TypeError, ValueError):
        raise _invalid("invalid comparison version identity") from None
    for keys in (value.included_record_keys, value.excluded_record_keys):
        if type(keys) is not tuple:
            raise _invalid("comparison scope identities must be immutable tuples")
        for key in keys:
            if type(key) is not RecordKey:
                raise _invalid("comparison scope requires canonical record identities")
            try:
                RecordKey(_text(key.dataset_version), _text(key.record_id))
            except (TypeError, ValueError):
                raise _invalid("invalid comparison record identity") from None
    try:
        return replace(value, included_record_keys=tuple(sorted(value.included_record_keys)),
                       excluded_record_keys=tuple(sorted(value.excluded_record_keys)))
    except (TypeError, ValueError):
        raise _invalid("comparison scope identities fail canonical validation") from None


def _descriptor(value: object) -> RepresentationDescriptor:
    if type(value) is not RepresentationDescriptor:
        raise _invalid("comparison requires explicit representation descriptors")
    for text in (value.representation_name, value.representation_source, value.representation_version,
                 value.binning_or_mapping_rule, value.missing_value_policy):
        _text(text)
    for text in (value.field_name, value.missing_state_id, value.normalization_profile):
        if text is not None:
            _text(text)
    try:
        return replace(value)
    except (TypeError, ValueError):
        raise _invalid("comparison representation fails its approved declaration contract") from None


def _context(value: object) -> ExplicitPairContext:
    if type(value) is not ExplicitPairContext:
        raise _invalid("comparison requires an ExplicitPairContext")
    earlier, later = _scope(value.earlier_scope), _scope(value.later_scope)
    if earlier.dataset_versions == later.dataset_versions:
        raise _invalid("comparison versions must be distinct and ordered", order=True)
    order = value.version_order
    if type(order) is not VersionOrderResult or type(order.loaded_versions) is not tuple:
        raise _invalid("comparison requires retained version-order evidence", order=True)
    if type(order.declarations) not in (dict, MappingProxyType):
        raise _invalid("version-order declarations must be plain retained data", order=True)
    # Revalidate source declarations. Cached order/source labels are not authority.
    checked = resolve_version_order(order.loaded_versions, document=order.declarations or None,
                                    invocation_order=order.invocation_order)
    a, b = earlier.dataset_versions[0], later.dataset_versions[0]
    if a not in checked.loaded_versions or b not in checked.loaded_versions:
        raise _invalid("comparison versions must belong to the loaded chronology scope", order=True)
    if not checked.order or a not in checked.order or b not in checked.order or checked.order.index(a) >= checked.order.index(b):
        raise _invalid("declared chronology does not support the requested earlier/later pair", order=True)
    return ExplicitPairContext(earlier, later, _descriptor(value.earlier_representation),
                               _descriptor(value.later_representation), checked)


def _mapping(value: object, context: ExplicitPairContext, earlier_meaning: str,
             later_meaning: str) -> tuple[StateMappingDeclaration, tuple[tuple[str, tuple[str, ...]], ...]]:
    if type(value) is not StateMappingDeclaration:
        raise _invalid("a bare state_mapping cannot establish a directed comparison basis")
    if type(value.direction) is not str or value.direction not in ("earlier_to_later", "later_to_earlier"):
        raise _invalid("state mapping direction must be explicit")
    source, target = _descriptor(value.source_representation), _descriptor(value.target_representation)
    source_meaning, target_meaning = _text(value.source_state_semantics), _text(value.target_state_semantics)
    expected = ((context.earlier_representation, context.later_representation, earlier_meaning, later_meaning)
                if value.direction == "earlier_to_later" else
                (context.later_representation, context.earlier_representation, later_meaning, earlier_meaning))
    if (source, target, source_meaning, target_meaning) != expected:
        raise _invalid("mapping source, target or state meanings disagree with its declared direction")
    if type(value.state_mapping) not in (dict, MappingProxyType):
        raise _invalid("state mapping must be an exact literal dictionary")
    pairs = []
    for key, item in value.state_mapping.items():
        pairs.append((_text(key, empty=True), _text(item, empty=True)))
    if not pairs:
        raise _invalid("an explicit state mapping cannot be empty")
    pairs.sort()
    mapping = dict(pairs)
    if source.missing_value_policy != target.missing_value_policy:
        raise _invalid("a state map cannot change inclusion or missing-value policy")
    if source.missing_value_policy == "explicit_missing_state":
        if mapping.get(source.missing_state_id) != target.missing_state_id:
            raise _invalid("explicit missing state requires its matching target missing state")
        if any(k != source.missing_state_id and v == target.missing_state_id for k, v in pairs):
            raise _invalid("observed state cannot collide with the target missing-state marker")
    groups = {}
    for key, item in pairs:
        groups.setdefault(item, []).append(key)
    collisions = tuple((key, tuple(groups[key])) for key in sorted(groups) if len(groups[key]) > 1)
    return StateMappingDeclaration(value.direction, source, target, source_meaning, target_meaning,
                                    MappingProxyType(mapping)), collisions


def validate_representation_compatibility(
    context: ExplicitPairContext, *, earlier_state_semantics: str, later_state_semantics: str,
    state_mapping: StateMappingDeclaration | None = None,
) -> RepresentationCompatibility:
    """Require explicit chronology and identical declarations or a directed map.

    Version names alone never authorize comparison. A map can intentionally
    coarsen states, with its exact dictionary and collisions retained. It does
    not silently alter record inclusion or missing-state policy. Consuming
    kernels must still check map coverage against their actual state tables.
    """
    context = _context(context)
    earlier_meaning, later_meaning = _text(earlier_state_semantics), _text(later_state_semantics)
    if state_mapping is None:
        if context.earlier_representation != context.later_representation or earlier_meaning != later_meaning:
            raise _invalid("representation or state-meaning declarations differ without an explicit directed map")
        return RepresentationCompatibility(context, earlier_meaning, later_meaning,
            context.earlier_representation, earlier_meaning, "identical_declared_basis", None, ())
    mapping, collisions = _mapping(state_mapping, context, earlier_meaning, later_meaning)
    return RepresentationCompatibility(context, earlier_meaning, later_meaning,
        mapping.target_representation, mapping.target_state_semantics,
        "explicit_directed_state_mapping", mapping, collisions)
