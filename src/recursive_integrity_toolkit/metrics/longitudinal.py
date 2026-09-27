"""Select ordered snapshots and coordinate observed distribution changes.

Owner IDs:
    PR-002, PR-007, PR-011, T1, T2; P6A-D01 through P6A-D04 and P6A-D08.

Inputs:
    Retained BundleValidationResult, explicit snapshot declarations, pair-local
    mappings, baseline policy and a selected-version admission limit.

Outputs:
    Immutable complete population scopes, validated chronology, deterministic
    pair schedule, original distributions, pair-local changes and input binding.

Assumptions:
    Primary/comparison roles select records; context and chronology-only entries
    cannot silently acquire snapshot membership. Meanings remain declarations.

Limits:
    Selection performs no calculation. Analysis delegates existing distribution,
    comparison and tail owners. No I/O, graph, simulation, report or CLI dispatch.
    Provenance/direct-closure integration remains explicitly deferred to Step 4.

Current phase status:
    Phase 6A Step 3 snapshot distributions and observed changes. Import-safe.
"""
from __future__ import annotations

from dataclasses import dataclass, field, fields, replace
from math import isfinite
from types import MappingProxyType

from ..config import RepresentationConfig
from ..errors import CanonicalValidationError, ErrorCode
from ..io.validation import join_provenance, resolve_version_order
from ..models import (
    BundleValidationResult, CalculationEvidenceClass, CalculationMetadata,
    CalculationReason, CalculationScope, CalculationStatus, CanonicalRow,
    ContentMode, ExplicitPairContext, FileRole, RecordKey, RepresentationDescriptor,
    ScalarCalculation, TailSelectionOptions, ValidationCoverage, ValidationMessage,
    ValidationSeverity, VersionOrderResult,
)
from ..representations.base import _literal_text, _selected_records
from ..representations.compatibility import (
    RepresentationBasisCompatibility, StateMappingDeclaration, validate_representation_basis,
)
from ..representations.content_hash import assign_content_states, select_content_representation
from ..representations.field import assign_field_states, select_field_representation
from ..result import ExecutionStatus
from ..utils.hashing import sha256_canonical
from .diversity import (
    StateDistributionResult, SupportComparison, _harmonize_distribution,
    calculate_state_distribution, compare_support,
)
from .tail import TailSelectionResult, _options as _tail_options, select_tail


def _invalid(message: str, *, code: ErrorCode = ErrorCode.CONFIG_INVALID,
             field_name: str = "longitudinal") -> CanonicalValidationError:
    return CanonicalValidationError(code, message, field=field_name)


def _version(value: object) -> str:
    if not _literal_text(value):
        raise _invalid("snapshot identity must be canonical literal text")
    try:
        RecordKey(value, "selection-check")
    except (TypeError, ValueError):
        raise _invalid("snapshot identity violates the canonical contract") from None
    return value


def _limit(value: object) -> int:
    if type(value) is not int or value <= 0:
        raise _invalid("selected-version limit must be a positive integer", field_name="max_versions")
    return value


def _baseline(value: object) -> str:
    if type(value) is not str or value not in ("none", "first"):
        raise _invalid("baseline must be none or first", field_name="baseline")
    return value


@dataclass(frozen=True, slots=True)
class SnapshotDeclaration:
    dataset_version: str
    representation: RepresentationConfig
    state_semantics: str = field(repr=False)
    missing_state_id: str | None = field(default=None, repr=False)
    empty_scope: bool = False

    def __post_init__(self) -> None:
        _version(self.dataset_version)
        if not _literal_text(self.state_semantics) or type(self.empty_scope) is not bool:
            raise _invalid("snapshot requires literal meaning and an explicit empty-scope flag")
        if self.missing_state_id is not None and not _literal_text(self.missing_state_id):
            raise _invalid("missing-state marker must be literal nonempty text")
        if type(self.representation) is not RepresentationConfig:
            raise _invalid("snapshot requires an explicit RepresentationConfig")
        # Primitive immutable leaves only; never retain an arbitrary config hook.
        for item in fields(self.representation):
            value = getattr(self.representation, item.name)
            if value is not None and not _literal_text(value):
                raise _invalid("representation metadata requires literal nonempty text")
        object.__setattr__(self, "representation", replace(self.representation))
        _descriptor_for(self)


def _descriptor_for(declaration: SnapshotDeclaration) -> RepresentationDescriptor:
    config = declaration.representation
    if config.source == "content_hash":
        if (config.field not in (None, "content") or config.missing_value_policy not in (None, "error")
                or declaration.missing_state_id is not None):
            raise _invalid("exact-content declarations require content and the error policy")
        return select_content_representation(representation_name=config.name,
            representation_version=config.version,
            normalization_profile=config.normalization_profile).descriptor
    # Metadata selection on no rows performs no assignment or inclusion decision.
    return select_field_representation((), dataset_versions=(declaration.dataset_version,),
        config=config, missing_state_id=declaration.missing_state_id).descriptor


@dataclass(frozen=True, slots=True)
class LongitudinalMapping:
    """One scheduled pair's directed mapping; never composed across pairs."""

    earlier_version: str
    later_version: str
    declaration: StateMappingDeclaration = field(repr=False)

    def __post_init__(self) -> None:
        if _version(self.earlier_version) == _version(self.later_version):
            raise _invalid("mapping endpoints must be distinct")
        value = self.declaration
        if type(value) is not StateMappingDeclaration:
            raise _invalid("pair mapping requires a full StateMappingDeclaration")
        earlier, later = value.source_representation, value.target_representation
        first, second = value.source_state_semantics, value.target_state_semantics
        if value.direction == "later_to_earlier":
            earlier, later, first, second = later, earlier, second, first
        checked = validate_representation_basis(earlier, later,
            earlier_state_semantics=first, later_state_semantics=second, state_mapping=value)
        object.__setattr__(self, "declaration", checked.mapping)


@dataclass(frozen=True, slots=True)
class SnapshotScope:
    dataset_version: str
    population_scope: CalculationScope
    representation_scope: CalculationScope | None
    declaration: SnapshotDeclaration

    def __post_init__(self) -> None:
        _version(self.dataset_version)
        if (type(self.declaration) is not SnapshotDeclaration
                or self.declaration.dataset_version != self.dataset_version
                or type(self.population_scope) is not CalculationScope
                or self.population_scope.dataset_versions != (self.dataset_version,)
                or self.population_scope.excluded_record_keys
                or self.population_scope.denominator_basis != "selected_valid_records"):
            raise _invalid("snapshot requires a complete declared version population")
        object.__setattr__(self, "declaration", replace(self.declaration))
        object.__setattr__(self, "population_scope", replace(self.population_scope))
        if self.declaration.empty_scope != (not self.population_scope.included_record_keys):
            raise _invalid("snapshot emptiness must agree with its population")
        scope = self.representation_scope
        if scope is not None:
            if (type(scope) is not CalculationScope or scope.dataset_versions != (self.dataset_version,)
                    or scope.denominator_basis != "included_representation_records"
                    or set((*scope.included_record_keys, *scope.excluded_record_keys))
                    != set(self.population_scope.included_record_keys)):
                raise _invalid("representation scope must partition its snapshot population")
            object.__setattr__(self, "representation_scope", replace(scope))


@dataclass(frozen=True, slots=True)
class LongitudinalPair:
    earlier_version: str
    later_version: str
    kinds: tuple[str, ...]
    mapping: StateMappingDeclaration | None = field(repr=False)
    compatibility: RepresentationBasisCompatibility | None = field(repr=False)
    reason_codes: tuple[CalculationReason, ...] = ()

    def __post_init__(self) -> None:
        if _version(self.earlier_version) == _version(self.later_version):
            raise _invalid("pair endpoints must be distinct")
        if type(self.kinds) is not tuple or self.kinds not in (
                ("adjacent",), ("baseline",), ("adjacent", "baseline")):
            raise _invalid("pair kinds must be a canonical nonempty tuple")
        if self.compatibility is None:
            if (self.mapping is not None or type(self.reason_codes) is not tuple
                    or self.reason_codes != (CalculationReason.REPRESENTATION_INCOMPATIBLE,)):
                raise _invalid("an incompatible pair must retain its explicit gap reason")
        else:
            if type(self.compatibility) is not RepresentationBasisCompatibility or self.reason_codes != ():
                raise _invalid("pair basis evidence has invalid status")
            value = self.compatibility
            checked = validate_representation_basis(value.earlier_representation, value.later_representation,
                earlier_state_semantics=value.earlier_state_semantics,
                later_state_semantics=value.later_state_semantics, state_mapping=self.mapping)
            if checked != value:
                raise _invalid("pair basis evidence disagrees with its declarations")
            object.__setattr__(self, "compatibility", checked)
            object.__setattr__(self, "mapping", checked.mapping)

    @property
    def status(self) -> CalculationStatus:
        """Declaration compatibility only; does not certify numerical availability."""
        return CalculationStatus.AVAILABLE if self.compatibility is not None else CalculationStatus.UNAVAILABLE


@dataclass(frozen=True, slots=True)
class LongitudinalSelection:
    primary_version: str
    selected_versions: tuple[str, ...]
    context_versions: tuple[str, ...]
    version_order: VersionOrderResult
    selected_order: tuple[str, ...]
    snapshots: tuple[SnapshotScope, ...]
    pairs: tuple[LongitudinalPair, ...]
    max_versions: int
    input_signature: str = field(repr=False)
    baseline: str = "none"

    def __post_init__(self) -> None:
        _version(self.primary_version)
        _limit(self.max_versions)
        _baseline(self.baseline)
        for versions in (self.selected_versions, self.context_versions, self.selected_order):
            if type(versions) is not tuple:
                raise _invalid("selection identities require immutable tuples")
            for version in versions:
                _version(version)
            if len(set(versions)) != len(versions):
                raise _invalid("selection identities must be unique")
        if (not 2 <= len(self.selected_versions) <= self.max_versions
                or self.primary_version not in self.selected_versions
                or set(self.selected_versions) != set(self.selected_order)
                or set(self.selected_versions) & set(self.context_versions)
                or type(self.snapshots) is not tuple or type(self.pairs) is not tuple
                or any(type(item) is not SnapshotScope for item in self.snapshots)
                or any(type(item) is not LongitudinalPair for item in self.pairs)):
            raise _invalid("selection populations and selected chronology disagree")
        if (type(self.input_signature) is not str or len(self.input_signature) != 64
                or any(char not in "0123456789abcdef" for char in self.input_signature)):
            raise _invalid("selection requires a canonical private input binding")
        order = self.version_order
        if type(order) is not VersionOrderResult or type(order.declarations) not in (dict, MappingProxyType):
            raise _invalid("selection requires retained chronology")
        checked = resolve_version_order(order.loaded_versions, document=order.declarations or None)
        if order.invocation_order is not None or checked != order:
            raise _invalid("selection chronology must retain explicit source evidence")
        selected = set(self.selected_versions)
        if (self.selected_versions != tuple(sorted(self.selected_versions))
                or self.context_versions != tuple(sorted(self.context_versions))
                or self.selected_order != tuple(v for v in checked.order if v in selected)
                or tuple(item.dataset_version for item in self.snapshots) != self.selected_order
                or any(item.representation_scope is not None for item in self.snapshots)
                or tuple((item.earlier_version, item.later_version, item.kinds) for item in self.pairs)
                != tuple((a, b, kinds) for (a, b), kinds in _pair_schedule(self.selected_order, self.baseline).items())):
            raise _invalid("selection snapshots and pairs must follow the complete canonical schedule")
        object.__setattr__(self, "version_order", checked)
        object.__setattr__(self, "snapshots", tuple(replace(item) for item in self.snapshots))
        object.__setattr__(self, "pairs", tuple(replace(item) for item in self.pairs))


def _populations(validation: BundleValidationResult):
    if (type(validation) is not BundleValidationResult or type(validation.records) is not tuple
            or not validation.records or any(type(row) is not CanonicalRow for row in validation.records)):
        raise _invalid("selection requires a nonempty validated record bundle")
    if type(validation.content_mode) is not ContentMode:
        raise _invalid("selection requires a retained explicit content mode")
    order = validation.version_order
    if type(order) is not VersionOrderResult:
        raise _invalid("selection requires retained version-order evidence")
    # Validate every record once, including context, before using its identity.
    if any(type(row.record_key) is not RecordKey for row in validation.records):
        raise _invalid("selection requires canonical record identities")
    actual_versions = tuple(sorted({_version(row.record_key.dataset_version) for row in validation.records}))
    rows = _selected_records(validation.records, actual_versions)
    by_version, roles, files, file_versions = {}, {}, {}, {}
    selected_roles = (FileRole.RECORDS_PRIMARY, FileRole.RECORDS_COMPARE)
    original = {row.record_key: row for row in validation.records}
    for key, values, location in rows:
        role = location.file_role
        if role not in (*selected_roles, FileRole.LINEAGE_CONTEXT):
            raise _invalid("every loaded record requires an explicit input role")
        version = key.dataset_version
        by_version.setdefault(version, []).append(key)
        roles.setdefault(version, set()).add(role)
        path = original[key].location.file_path
        if role in selected_roles:
            files.setdefault(version, set()).add((role, path))
            if path is not None:
                file_versions.setdefault((role, path), set()).add(version)
    if type(order.loaded_versions) is not tuple or order.loaded_versions != actual_versions:
        raise _invalid("retained loaded versions disagree with canonical records")
    if (any(len(value) != 1 for value in roles.values())
            or any(len(value) != 1 for value in files.values())
            or any(len(value) != 1 for value in file_versions.values())):
        raise _invalid("snapshot roles and files must be disjoint complete version populations")
    primary = tuple(version for version in roles if FileRole.RECORDS_PRIMARY in roles[version])
    if len(primary) != 1:
        raise _invalid("selection requires exactly one nonempty primary version")
    context = tuple(sorted(version for version in roles if FileRole.LINEAGE_CONTEXT in roles[version]))
    selected = set(by_version) - set(context)
    # Join validation rejects duplicate/unmatched or malformed supplied provenance.
    joined = join_provenance(validation.records, validation.provenance)
    return rows, by_version, selected, context, primary[0], joined


def _plain(value):
    """Canonical literal conversion, only for validated internal declarations."""
    if type(value) is MappingProxyType:
        return {name: _plain(item) for name, item in value.items()}
    if type(value) is dict:
        return {name: _plain(item) for name, item in value.items()}
    if type(value) in (tuple, list):
        return tuple(_plain(item) for item in value)
    if type(value) in (RepresentationConfig, RepresentationDescriptor, StateMappingDeclaration,
                       SnapshotDeclaration):
        return {item.name: _plain(getattr(value, item.name)) for item in fields(value)}
    return value


def _binding(rows, joined, order, declarations, pairs, baseline, max_versions, content_mode):
    # Canonical values include state/parent evidence. Private hashes and digests
    # never authorize public disclosure. Paths, row positions and extras are absent.
    records = tuple(((key.dataset_version, key.record_id), location.file_role.value, values)
                    for key, values, location in rows)
    provenance = tuple(((match.record_key.dataset_version, match.record_key.record_id),
                        None if match.provenance is None else dict(match.provenance.values))
                       for match in joined.matches)
    pair_declarations = tuple((pair.earlier_version, pair.later_version, pair.kinds,
                               _plain(pair.mapping)) for pair in pairs)
    try:
        return sha256_canonical((records, joined.provenance_supplied, provenance, _plain(order.declarations),
            _plain(declarations), pair_declarations, baseline, max_versions, content_mode.value))
    except (TypeError, ValueError):
        raise _invalid("selection input binding requires canonical literal data") from None


def _pair_schedule(selected_order, baseline):
    schedule = {}
    first = selected_order[0]
    for index, later in enumerate(selected_order[1:], 1):
        earlier = selected_order[index - 1]
        if baseline == "first":
            schedule[first, later] = ("adjacent", "baseline") if index == 1 else ("baseline",)
        if (earlier, later) not in schedule:
            schedule[earlier, later] = ("adjacent",)
    return schedule


def select_longitudinal_versions(
    validation: BundleValidationResult, *, declarations: tuple[SnapshotDeclaration, ...],
    baseline: str = "none", max_versions: int = 100,
    mappings: tuple[LongitudinalMapping, ...] = (),
) -> LongitudinalSelection:
    """Validate explicit populations, chronology and each scheduled pair's basis.

    Unmapped differing bases retain an unavailable pair. Malformed explicit maps
    and missing/conflicting chronology raise structured input errors. No states
    are assigned and no metrics or graph are evaluated. Typed empty snapshots
    may precede or follow the latest loaded primary; CLI empty files stay invalid.
    """
    _limit(max_versions)
    _baseline(baseline)
    if type(declarations) is not tuple or type(mappings) is not tuple:
        raise _invalid("snapshot and mapping declarations require explicit tuples")
    if len(declarations) > max_versions:
        raise _invalid("selected-version admission limit exceeded",
                       code=ErrorCode.LONGITUDINAL_RESOURCE_LIMIT_EXCEEDED, field_name="max_versions")
    if len(declarations) < 2 or any(type(item) is not SnapshotDeclaration for item in declarations):
        raise _invalid("series requires at least two explicit snapshot declarations")
    declarations = tuple(replace(item) for item in declarations)
    declared = {item.dataset_version: item for item in declarations}
    if len(declared) != len(declarations):
        raise _invalid("snapshot declarations must be unique")
    rows, populations, loaded_selected, context, primary, joined = _populations(validation)
    if len(loaded_selected | set(declared)) > max_versions:
        raise _invalid("selected-version admission limit exceeded",
                       code=ErrorCode.LONGITUDINAL_RESOURCE_LIMIT_EXCEEDED, field_name="max_versions")
    if set(declared) & set(context) or loaded_selected - set(declared):
        raise _invalid("declarations must cover every selected version and exclude context")
    for version, declaration in declared.items():
        if declaration.empty_scope != (version not in populations):
            raise _invalid("only explicitly identified unloaded snapshots may have empty scope")
    retained = validation.version_order
    # Invocation order remains valid for legacy pairs, never for a new series.
    if retained.invocation_order is not None:
        raise _invalid("series chronology cannot use invocation order",
                       code=ErrorCode.VERSION_ORDER_CONFLICT, field_name="version_order")
    checked = resolve_version_order(retained.loaded_versions, document=retained.declarations or None)
    if not checked.declarations or not checked.order or set(declared) - set(checked.order):
        raise _invalid("series requires explicit chronology covering every selected snapshot",
                       code=ErrorCode.VERSION_ORDER_CONFLICT, field_name="version_order")
    selected_order = tuple(version for version in checked.order if version in declared)
    if tuple(version for version in selected_order if version in loaded_selected)[-1] != primary:
        raise _invalid("primary must be latest among loaded selected versions",
                       code=ErrorCode.VERSION_ORDER_CONFLICT, field_name="primary_version")
    snapshots = tuple(SnapshotScope(version,
        CalculationScope((version,), tuple(populations.get(version, ())), (),
                         "selected_valid_records", f"longitudinal-population-{index:04d}"),
        None, declared[version]) for index, version in enumerate(selected_order, 1))
    schedule = _pair_schedule(selected_order, baseline)
    supplied = {}
    for item in mappings:
        if type(item) is not LongitudinalMapping:
            raise _invalid("pair maps require explicit typed endpoint declarations")
        item = replace(item)
        key = item.earlier_version, item.later_version
        if key not in schedule or key in supplied:
            raise _invalid("pair maps must be unique and belong to the requested schedule")
        supplied[key] = item.declaration
    descriptors = {version: _descriptor_for(declared[version]) for version in selected_order}
    pairs = []
    for (earlier, later), kinds in schedule.items():
        mapping = supplied.get((earlier, later))
        try:
            compatibility = validate_representation_basis(descriptors[earlier], descriptors[later],
                earlier_state_semantics=declared[earlier].state_semantics,
                later_state_semantics=declared[later].state_semantics, state_mapping=mapping)
        except CanonicalValidationError as error:
            if mapping is not None or error.code is not ErrorCode.REPRESENTATION_INCOMPATIBLE:
                raise
            compatibility = None
        pairs.append(LongitudinalPair(earlier, later, kinds,
            None if compatibility is None else compatibility.mapping, compatibility,
            (CalculationReason.REPRESENTATION_INCOMPATIBLE,) if compatibility is None else ()))
    declarations = tuple(declared[version] for version in selected_order)
    pairs = tuple(pairs)
    return LongitudinalSelection(primary, tuple(sorted(declared)), context, checked, selected_order,
        snapshots, pairs, max_versions,
        _binding(rows, joined, checked, declarations, pairs, baseline, max_versions, validation.content_mode), baseline)


def validate_longitudinal_selection(
    validation: BundleValidationResult, selection: LongitudinalSelection,
) -> LongitudinalSelection:
    """Revalidate full populations, schedule and binding at a consuming boundary."""
    if type(selection) is not LongitudinalSelection:
        raise _invalid("consumer requires a LongitudinalSelection")
    selection = replace(selection)
    checked = select_longitudinal_versions(validation,
        declarations=tuple(item.declaration for item in selection.snapshots),
        baseline=selection.baseline, max_versions=selection.max_versions,
        mappings=tuple(LongitudinalMapping(item.earlier_version, item.later_version, item.mapping)
                       for item in selection.pairs if item.mapping is not None))
    if checked != selection:
        raise _invalid("selection is stale or disagrees with complete current input")
    return checked


@dataclass(frozen=True, slots=True)
class LongitudinalFamilyStatus:
    family: str
    execution_status: ExecutionStatus
    reason_codes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if (type(self.family) is not str or self.family not in
                ("distribution", "provenance", "direct_closure", "tail", "lineage")
                or type(self.execution_status) is not ExecutionStatus
                or type(self.reason_codes) is not tuple
                or any(type(code) is not str or not code for code in self.reason_codes)
                or (self.execution_status is ExecutionStatus.COMPLETED) != (not self.reason_codes)):
            raise _invalid("family status must retain its explicit execution reasons")


@dataclass(frozen=True, slots=True)
class LongitudinalDelta:
    """A difference with two endpoint scopes; no pooled population or denominator."""

    metric_name: str
    owner_id: str
    formula_id: str
    unit: str
    earlier_scope: CalculationScope
    later_scope: CalculationScope
    representation: RepresentationDescriptor | None
    earlier_value: int | float | None
    later_value: int | float | None
    value: int | float | None
    status: CalculationStatus
    reason_codes: tuple[CalculationReason, ...]
    earlier_denominator: int | float | None = None
    later_denominator: int | float | None = None
    earlier_coverage: ValidationCoverage | None = None
    later_coverage: ValidationCoverage | None = None
    earlier_reason_codes: tuple[CalculationReason, ...] = ()
    later_reason_codes: tuple[CalculationReason, ...] = ()
    evidence_class: CalculationEvidenceClass = CalculationEvidenceClass.DERIVED_METRIC
    method: str = "later minus earlier"
    denominator: None = None
    denominator_reason: str = "not_applicable_to_difference"

    def __post_init__(self) -> None:
        for value in (self.metric_name, self.owner_id, self.formula_id, self.unit):
            if not _literal_text(value):
                raise _invalid("delta metadata requires literal declarations")
        expected = {"record_count_delta": ("T1", "F-018", "records"),
                    "support_delta": ("T1", "F-005", "states"),
                    "gini_simpson_diversity_delta": ("T1", "F-018", "dimensionless")}
        if expected.get(self.metric_name) != (self.owner_id, self.formula_id, self.unit):
            raise _invalid("delta ownership, formula and unit must match the approved field")
        if (type(self.earlier_scope) is not CalculationScope or type(self.later_scope) is not CalculationScope
                or len(self.earlier_scope.dataset_versions) != 1 or len(self.later_scope.dataset_versions) != 1
                or self.earlier_scope.dataset_versions == self.later_scope.dataset_versions
                or self.representation is not None and type(self.representation) is not RepresentationDescriptor
                or type(self.status) is not CalculationStatus
                or self.evidence_class is not CalculationEvidenceClass.DERIVED_METRIC
                or self.formula_id not in ("F-005", "F-018") or self.method != "later minus earlier"
                or self.denominator is not None or self.denominator_reason != "not_applicable_to_difference"):
            raise _invalid("delta requires separate scopes and its approved method")
        for reasons in (self.reason_codes, self.earlier_reason_codes, self.later_reason_codes):
            if type(reasons) is not tuple or any(type(code) is not CalculationReason for code in reasons):
                raise _invalid("delta reasons require the existing calculation registry")
        for value in (self.earlier_value, self.later_value, self.value,
                      self.earlier_denominator, self.later_denominator):
            if value is not None:
                try:
                    valid = type(value) in (int, float) and isfinite(value)
                except OverflowError:
                    valid = False
                if not valid:
                    raise _invalid("delta endpoints and values must be finite numbers or null")
        for coverage in (self.earlier_coverage, self.later_coverage):
            if coverage is not None and type(coverage) is not ValidationCoverage:
                raise _invalid("delta coverage requires a named coverage object")
        if self.status is CalculationStatus.AVAILABLE:
            if (self.earlier_value is None or self.later_value is None or self.reason_codes
                    or self.earlier_reason_codes or self.later_reason_codes
                    or self.value != self.later_value - self.earlier_value):
                raise _invalid("available delta must equal its declared endpoint difference")
        elif self.value is not None or not self.reason_codes:
            raise _invalid("unavailable delta must be null with explicit reasons")


@dataclass(frozen=True, slots=True)
class TailDisappearanceResult:
    """Earlier-tail membership and its observed later absence on this pair's basis."""

    options: TailSelectionOptions
    earlier_scope: CalculationScope
    later_scope: CalculationScope
    representation: RepresentationDescriptor | None
    earlier_tail: TailSelectionResult | None = field(repr=False)
    earlier_sample_size: int | None
    status: CalculationStatus
    reason_codes: tuple[CalculationReason, ...]
    tail_extinction_count: int | None
    tail_extinct_states: tuple[str, ...] | None = field(repr=False)
    owner_id: str = "T2"
    evidence_class: CalculationEvidenceClass = CalculationEvidenceClass.DERIVED_METRIC
    method: str = "earlier tail intersect missing states"
    interpretation: str = "extinct from the observed later version under the declared representation"

    def __post_init__(self) -> None:
        object.__setattr__(self, "options", _tail_options(self.options))
        if (type(self.earlier_scope) is not CalculationScope or type(self.later_scope) is not CalculationScope
                or type(self.status) is not CalculationStatus or type(self.reason_codes) is not tuple
                or any(type(code) is not CalculationReason for code in self.reason_codes)
                or self.owner_id != "T2" or self.evidence_class is not CalculationEvidenceClass.DERIVED_METRIC
                or self.method != "earlier tail intersect missing states"):
            raise _invalid("observed tail disappearance requires its scoped method and reasons")
        if self.status is CalculationStatus.AVAILABLE:
            if (type(self.tail_extinct_states) is not tuple or type(self.tail_extinction_count) is not int
                    or self.tail_extinction_count != len(self.tail_extinct_states) or self.reason_codes
                    or type(self.earlier_tail) is not TailSelectionResult
                    or self.earlier_tail.status is not CalculationStatus.AVAILABLE
                    or self.earlier_sample_size != self.earlier_tail.denominator
                    or self.earlier_scope != self.earlier_tail.scope
                    or self.representation != self.earlier_tail.representation
                    or not set(self.tail_extinct_states) <= set(self.earlier_tail.tail_membership)):
                raise _invalid("available tail disappearance must retain its earlier selection")
        elif self.tail_extinct_states is not None or self.tail_extinction_count is not None or not self.reason_codes:
            raise _invalid("unavailable tail disappearance requires null sets and count")


@dataclass(frozen=True, slots=True)
class SnapshotSummary:
    scope: SnapshotScope
    distribution: StateDistributionResult | None = field(repr=False)
    record_count: ScalarCalculation
    representation_eligible_record_count: ScalarCalculation
    representation_excluded_record_count: ScalarCalculation
    family_statuses: tuple[LongitudinalFamilyStatus, ...]
    messages: tuple[ValidationMessage, ...] = ()
    provenance: None = None
    direct_closure: None = None
    lineage: None = None

    def __post_init__(self) -> None:
        _result_rows(self.family_statuses, self.messages)
        if type(self.scope) is not SnapshotScope:
            raise _invalid("snapshot summary requires a typed population")
        for count in (self.record_count, self.representation_eligible_record_count,
                      self.representation_excluded_record_count):
            if (type(count) is not ScalarCalculation or count.metadata.scope != self.scope.population_scope
                    or count.metadata.evidence_class is not CalculationEvidenceClass.OBSERVED_FACT):
                raise _invalid("snapshot counts must retain their complete population and evidence class")
        if self.record_count.value != len(self.scope.population_scope.included_record_keys):
            raise _invalid("snapshot record count disagrees with the selected population")
        scope = self.scope.representation_scope
        counts = self.representation_eligible_record_count.value, self.representation_excluded_record_count.value
        expected = (None, None) if scope is None else (len(scope.included_record_keys), len(scope.excluded_record_keys))
        if counts != expected:
            raise _invalid("representation counts disagree with their assigned scope")
        if self.distribution is not None:
            if (type(self.distribution) is not StateDistributionResult
                    or self.distribution.unweighted.scope != scope or self.distribution.weighted is not None
                    or self.distribution.coverage.numerator != counts[0]
                    or self.distribution.coverage.denominator != self.record_count.value):
                raise _invalid("snapshot distribution must retain its independent unweighted denominator")
        if self.provenance is not None or self.direct_closure is not None or self.lineage is not None:
            raise _invalid("later analytical families remain deferred in this step")


@dataclass(frozen=True, slots=True)
class LongitudinalPairResult:
    pair: LongitudinalPair
    compatibility: RepresentationBasisCompatibility | None = field(repr=False)
    support_comparison: SupportComparison | None = field(repr=False)
    deltas: tuple[LongitudinalDelta, ...]
    tail_disappearance: TailDisappearanceResult | None
    family_statuses: tuple[LongitudinalFamilyStatus, ...]
    messages: tuple[ValidationMessage, ...] = ()

    def __post_init__(self) -> None:
        _result_rows(self.family_statuses, self.messages)
        if (type(self.pair) is not LongitudinalPair or type(self.deltas) is not tuple
                or any(type(delta) is not LongitudinalDelta for delta in self.deltas)
                or tuple(delta.metric_name for delta in self.deltas) !=
                ("record_count_delta", "support_delta", "gini_simpson_diversity_delta")):
            raise _invalid("pair result requires all three scoped distribution deltas")
        for delta in self.deltas:
            if (delta.earlier_scope.dataset_versions != (self.pair.earlier_version,)
                    or delta.later_scope.dataset_versions != (self.pair.later_version,)):
                raise _invalid("pair delta endpoints disagree with the scheduled pair")
        if self.compatibility is None:
            if self.support_comparison is not None or any(d.value is not None for d in self.deltas):
                raise _invalid("blocked pair cannot carry available comparison values")
        elif self.compatibility != self.pair.compatibility:
            raise _invalid("pair result must retain its declared compatible basis")
        comparison = self.support_comparison
        if comparison is not None:
            if (type(comparison) is not SupportComparison or comparison.status is not CalculationStatus.AVAILABLE
                    or comparison.original_earlier.scope.dataset_versions != (self.pair.earlier_version,)
                    or comparison.original_later.scope.dataset_versions != (self.pair.later_version,)
                    or self.deltas[1].value != comparison.support_delta.value
                    or self.deltas[2].value != comparison.gini_simpson_diversity_delta.value):
                raise _invalid("pair summary differs from its existing comparison kernel")
        tail = self.tail_disappearance
        if tail is not None:
            if type(tail) is not TailDisappearanceResult:
                raise _invalid("tail disappearance requires its typed comparison result")
            if tail.status is CalculationStatus.AVAILABLE and (comparison is None or
                    tail.tail_extinct_states != tuple(sorted(set(tail.earlier_tail.tail_membership)
                                                            & set(comparison.extinct_states)))):
                raise _invalid("observed tail loss must intersect the harmonized earlier tail")


@dataclass(frozen=True, slots=True)
class LongitudinalResult:
    selection: LongitudinalSelection
    snapshots: tuple[SnapshotSummary, ...]
    comparisons: tuple[LongitudinalPairResult, ...]
    execution_status: ExecutionStatus
    reason_codes: tuple[str, ...]
    messages: tuple[ValidationMessage, ...]
    input_signature: str = field(repr=False)
    tail_options: TailSelectionOptions | None = None
    shared_lineage: None = None

    def __post_init__(self) -> None:
        if (type(self.selection) is not LongitudinalSelection or type(self.snapshots) is not tuple
                or any(type(item) is not SnapshotSummary for item in self.snapshots)
                or type(self.comparisons) is not tuple
                or any(type(item) is not LongitudinalPairResult for item in self.comparisons)
                or tuple(s.scope.dataset_version for s in self.snapshots) != self.selection.selected_order
                or tuple(p.pair for p in self.comparisons) != self.selection.pairs
                or self.shared_lineage is not None):
            raise _invalid("series results must retain every selected snapshot and scheduled pair")
        for selected, snapshot in zip(self.selection.snapshots, self.snapshots):
            if (selected.population_scope != snapshot.scope.population_scope
                    or selected.declaration != snapshot.scope.declaration):
                raise _invalid("analyzed snapshot no longer matches its selected declaration")
        snapshots = {s.scope.dataset_version: s for s in self.snapshots}
        for pair in self.comparisons:
            count = pair.deltas[0]
            if (count.earlier_value != snapshots[pair.pair.earlier_version].record_count.value
                    or count.later_value != snapshots[pair.pair.later_version].record_count.value):
                raise _invalid("record-count delta must use the complete endpoint populations")
        options = None if self.tail_options is None else _tail_options(self.tail_options)
        if self.input_signature != _analysis_signature(self.selection, options):
            raise _invalid("series input binding differs from its selection or tail request")
        if any((pair.tail_disappearance is None) != (options is None) for pair in self.comparisons):
            raise _invalid("series tail results must match explicit enablement")
        if (type(self.execution_status) is not ExecutionStatus or type(self.reason_codes) is not tuple
                or any(type(code) is not str or not code for code in self.reason_codes)
                or type(self.messages) is not tuple or any(type(m) is not ValidationMessage for m in self.messages)):
            raise _invalid("series execution status and diagnostics require immutable typed values")
        useful = any(delta.status is CalculationStatus.AVAILABLE for pair in self.comparisons for delta in pair.deltas)
        if (self.execution_status is not (ExecutionStatus.PARTIAL if useful else ExecutionStatus.FAILED)
                or "R_LONGITUDINAL_FAMILIES_DEFERRED" not in self.reason_codes):
            raise _invalid("Step 3 result must disclose its deferred required families")


def _result_rows(families, messages):
    if (type(families) is not tuple or any(type(f) is not LongitudinalFamilyStatus for f in families)
            or tuple(f.family for f in families) != ("distribution", "provenance", "direct_closure", "tail", "lineage")
            or type(messages) is not tuple or any(type(m) is not ValidationMessage for m in messages)):
        raise _invalid("analytical summaries require immutable complete family rows and diagnostics")


def _analysis_signature(selection, options):
    return sha256_canonical((selection.input_signature, None if options is None else
        (options.rule, options.count_threshold, options.frequency_threshold, options.state_ids)))


def _family(family, status, reasons=()):
    return LongitudinalFamilyStatus(family, status, tuple(dict.fromkeys(str(code) for code in reasons)))


def _families(distribution, tail=None):
    return (distribution,
        _family("provenance", ExecutionStatus.DEFERRED, ("R_LONGITUDINAL_FAMILIES_DEFERRED",)),
        _family("direct_closure", ExecutionStatus.DEFERRED, ("R_LONGITUDINAL_FAMILIES_DEFERRED",)),
        tail or _family("tail", ExecutionStatus.NOT_REQUESTED, ("R_LONGITUDINAL_FAMILY_NOT_REQUESTED",)),
        _family("lineage", ExecutionStatus.NOT_REQUESTED, ("R_LONGITUDINAL_FAMILY_NOT_REQUESTED",)))


def _message(error, field_name):
    return ValidationMessage(error.code.value, ValidationSeverity.ERROR, error.safe_message, field=field_name)


def _count(name, count, snapshot, *, representation=None, reasons=()):
    metadata = CalculationMetadata(name, "PR-002" if name == "record_count" else "PR-011", None,
        CalculationEvidenceClass.OBSERVED_FACT, "records",
        "PR-002.record_count" if name == "record_count" else "cardinality of explicit representation scope",
        snapshot.population_scope, representation)
    return ScalarCalculation(metadata, CalculationStatus.UNAVAILABLE if reasons else CalculationStatus.AVAILABLE,
                             None if reasons else count, reasons)


def _snapshot_distribution(snapshot, records, ordinal, content_mode):
    declaration = snapshot.declaration
    config = declaration.representation
    distribution, messages, reasons = None, (), ()
    try:
        if config.source == "content_hash":
            if content_mode is ContentMode.LOCAL_REF and records:
                raise _invalid("local-reference content payloads are unavailable to series analysis",
                               code=ErrorCode.CONTENT_REF_MISSING)
            represented = assign_content_states(records, dataset_versions=(snapshot.dataset_version,),
                scope_id=f"longitudinal-representation-{ordinal:04d}", representation_name=config.name,
                representation_version=config.version, normalization_profile=config.normalization_profile,
                content_mode=ContentMode.INLINE).representation
        else:
            represented = assign_field_states(records, dataset_versions=(snapshot.dataset_version,),
                scope_id=f"longitudinal-representation-{ordinal:04d}", config=config,
                missing_state_id=declaration.missing_state_id)
        snapshot = replace(snapshot, representation_scope=represented.scope)
        distribution = calculate_state_distribution(represented)
    except CanonicalValidationError as error:
        reasons = ((CalculationReason.CONTENT_UNAVAILABLE,) if error.code is ErrorCode.CONTENT_REF_MISSING
                   else (CalculationReason.REPRESENTATION_MISSING,))
        messages = (_message(error, "longitudinal_snapshot"),)
    scope = snapshot.representation_scope
    descriptor = _descriptor_for(declaration)
    counts_reasons = reasons if scope is None else ()
    record_count = _count("record_count", len(snapshot.population_scope.included_record_keys), snapshot)
    included = _count("representation_eligible_record_count", None if scope is None else len(scope.included_record_keys),
                      snapshot, representation=descriptor, reasons=counts_reasons)
    excluded = _count("representation_excluded_record_count", None if scope is None else len(scope.excluded_record_keys),
                      snapshot, representation=descriptor, reasons=counts_reasons)
    if distribution is not None:
        reasons = distribution.unweighted.reason_codes
    status = ExecutionStatus.PARTIAL if reasons else ExecutionStatus.COMPLETED
    return SnapshotSummary(snapshot, distribution, record_count, included, excluded,
        _families(_family("distribution", status, reasons)), messages)


def _distribution_reasons(snapshot):
    if snapshot.distribution is not None:
        return snapshot.distribution.unweighted.reason_codes
    return tuple(CalculationReason(code) for code in snapshot.family_statuses[0].reason_codes)


def _pair_distributions(pair, earlier, later, order):
    """Use the pair kernel only with available, actually loaded endpoints."""
    basis = pair.compatibility
    a = None if earlier.distribution is None else earlier.distribution.unweighted
    b = None if later.distribution is None else later.distribution.unweighted
    if basis is None:
        return None, None, a, b, (CalculationReason.REPRESENTATION_INCOMPATIBLE,), (
            ValidationMessage(ErrorCode.REPRESENTATION_INCOMPATIBLE.value, ValidationSeverity.ERROR,
                "pair declarations have no compatible comparison basis", field="longitudinal_pair"),)
    try:
        if a is not None and b is not None and a.status is b.status is CalculationStatus.AVAILABLE:
            comparison = compare_support(a, b,
                context=ExplicitPairContext(a.scope, b.scope, a.representation, b.representation, order),
                earlier_state_semantics=basis.earlier_state_semantics,
                later_state_semantics=basis.later_state_semantics, state_mapping=pair.mapping)
            return basis, comparison, comparison.harmonized_earlier, comparison.harmonized_later, (), ()
        # An unavailable/empty side never enters the legacy loaded-pair kernel.
        # Reuse its owner for literal coverage and aggregation on any source that
        # exists, so a missing map entry still blocks independent record deltas.
        if pair.mapping is not None:
            forward = pair.mapping.direction == "earlier_to_later"
            source = a if forward else b
            if source is None:
                raise _invalid("mapping coverage requires its source representation", code=ErrorCode.REPRESENTATION_INCOMPATIBLE)
            source = _harmonize_distribution(source, pair.mapping)
            a, b = (source, b) if forward else (a, source)
        reasons = tuple(dict.fromkeys(_distribution_reasons(earlier) + _distribution_reasons(later)))
        return basis, None, a, b, reasons, ()
    except CanonicalValidationError as error:
        return None, None, None, None, (CalculationReason.REPRESENTATION_INCOMPATIBLE,), (
            _message(error, "longitudinal_pair"),)


def _delta(name, earlier, later, basis, a, b, reasons, *, comparison=None):
    record = name == "record_count_delta"
    formula, unit = ("F-018", "records") if record else (
        ("F-005", "states") if name == "support_delta" else ("F-018", "dimensionless"))
    if record:
        left, right = earlier.record_count.value, later.record_count.value
        left_scope, right_scope = earlier.scope.population_scope, later.scope.population_scope
        left_reasons = right_reasons = ()
        reasons = () if basis is not None else reasons
    else:
        metric = "support_size" if name == "support_delta" else "gini_simpson_diversity"
        left, right = (None if a is None else getattr(a, metric).value), (None if b is None else getattr(b, metric).value)
        left_scope = earlier.scope.representation_scope or earlier.scope.population_scope
        right_scope = later.scope.representation_scope or later.scope.population_scope
        left_reasons, right_reasons = _distribution_reasons(earlier), _distribution_reasons(later)
    available = not reasons
    # Existing pair scalars own F-005/F-018 distribution arithmetic.
    value = (right - left if record else getattr(comparison, name).value) if available else None
    return LongitudinalDelta(name, "T1", formula, unit, left_scope, right_scope,
        None if record or basis is None else basis.harmonized_representation,
        left, right, value, CalculationStatus.AVAILABLE if available else CalculationStatus.UNAVAILABLE, reasons,
        None if record or a is None else a.frequency_denominator,
        None if record or b is None else b.frequency_denominator,
        None if record or earlier.distribution is None else earlier.distribution.coverage,
        None if record or later.distribution is None else later.distribution.coverage,
        left_reasons, right_reasons)


def _tail_disappearance(options, basis, comparison, earlier, later, a, reasons):
    tail, messages = None, ()
    if not reasons:
        try:
            tail = select_tail(a, options=options)
        except CanonicalValidationError as error:
            reasons = (CalculationReason.UNSUPPORTED_OPTION,)
            messages = (_message(error, "longitudinal_tail"),)
    lost = None if reasons else tuple(sorted(set(tail.tail_membership) & set(comparison.extinct_states)))
    return TailDisappearanceResult(options,
        earlier.scope.representation_scope or earlier.scope.population_scope,
        later.scope.representation_scope or later.scope.population_scope,
        None if basis is None else basis.harmonized_representation, tail,
        None if a is None else a.frequency_denominator,
        CalculationStatus.UNAVAILABLE if reasons else CalculationStatus.AVAILABLE,
        reasons, None if lost is None else len(lost), lost), messages


def _pair_result(pair, earlier, later, order, options):
    basis, comparison, a, b, reasons, messages = _pair_distributions(pair, earlier, later, order)
    deltas = tuple(_delta(name, earlier, later, basis, a, b, reasons, comparison=comparison)
        for name in ("record_count_delta", "support_delta", "gini_simpson_diversity_delta"))
    distribution_status = (ExecutionStatus.COMPLETED if comparison is not None else
                           ExecutionStatus.PARTIAL if basis is not None else ExecutionStatus.FAILED)
    tail, tail_status = None, None
    if options is not None:
        tail, tail_messages = _tail_disappearance(options, basis, comparison, earlier, later, a, reasons)
        messages += tail_messages
        tail_status = _family("tail", ExecutionStatus.COMPLETED if tail.status is CalculationStatus.AVAILABLE
                              else ExecutionStatus.FAILED, tail.reason_codes)
    return LongitudinalPairResult(pair, basis, comparison, deltas, tail,
        _families(_family("distribution", distribution_status, reasons), tail_status), messages)


def analyze_longitudinal(
    validation: BundleValidationResult, *, selection: LongitudinalSelection,
    lineage: bool = False, tail_options: TailSelectionOptions | None = None, lineage_limits=None,
) -> LongitudinalResult:
    """Compute unweighted original snapshots and observed pair-local changes.

    Records are grouped once and each selected distribution runs once. Context
    supplies no snapshot denominator. Unavailable endpoints preserve record
    deltas only under a valid comparison basis; state sets remain null. Tail is
    opt-in and uses the harmonized earlier distribution. Required provenance and
    direct closure remain explicitly deferred until Step 4, so this staged
    result cannot claim a completed full series. Lineage options await Step 5.
    """
    if type(lineage) is not bool or lineage or lineage_limits is not None:
        raise _invalid("selected lineage execution is deferred to Phase 6A Step 5")
    options = None if tail_options is None else _tail_options(tail_options)
    selection = validate_longitudinal_selection(validation, selection)
    grouped = {version: [] for version in selection.selected_versions}
    for row in validation.records:
        if row.record_key.dataset_version in grouped:
            grouped[row.record_key.dataset_version].append(row)
    snapshots = tuple(_snapshot_distribution(scope, tuple(grouped[scope.dataset_version]), index, validation.content_mode)
                      for index, scope in enumerate(selection.snapshots, 1))
    index = {snapshot.scope.dataset_version: snapshot for snapshot in snapshots}
    comparisons = tuple(_pair_result(pair, index[pair.earlier_version], index[pair.later_version],
                                    selection.version_order, options) for pair in selection.pairs)
    useful = any(delta.status is CalculationStatus.AVAILABLE for pair in comparisons for delta in pair.deltas)
    reasons = ["R_LONGITUDINAL_FAMILIES_DEFERRED"]
    if any(pair.compatibility is None for pair in comparisons):
        reasons.append("R_LONGITUDINAL_PAIR_BLOCKED")
    if any(f.execution_status in (ExecutionStatus.PARTIAL, ExecutionStatus.FAILED)
           for pair in comparisons for f in pair.family_statuses if f.family in ("distribution", "tail")):
        reasons.append("R_LONGITUDINAL_ENDPOINT_UNAVAILABLE")
    messages = tuple(message for item in (*snapshots, *comparisons) for message in item.messages)
    signature = _analysis_signature(selection, options)
    return LongitudinalResult(selection, snapshots, comparisons,
        ExecutionStatus.PARTIAL if useful else ExecutionStatus.FAILED,
        tuple(reasons), messages, signature, options)
