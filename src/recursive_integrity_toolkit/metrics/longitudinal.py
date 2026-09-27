"""Coordinate ordered distribution, provenance and requested lineage changes.

Owner IDs:
    PR-002, PR-004, PR-005, PR-007, PR-008, PR-011, T1, T2, T3, T4;
    P6A-D01 through P6A-D06 and P6A-D08.

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
    comparison, tail, provenance and bound owners. Explicit lineage delegates
    one shared graph/root analysis. No I/O, simulation, report or CLI dispatch.

Current phase status:
    Phase 6A Step 5 shared selected lineage and observed changes. Import-safe.
"""
from __future__ import annotations

from dataclasses import dataclass, field, fields, is_dataclass, replace
from math import isfinite
from types import MappingProxyType
from typing import TYPE_CHECKING

from ..config import RepresentationConfig
from ..errors import CanonicalValidationError, ErrorCode, LineageResourceLimitError
from ..io.validation import join_provenance, resolve_version_order
from ..models import (
    BundleValidationResult, CalculationEvidenceClass, CalculationMetadata,
    CalculationReason, CalculationScope, CalculationStatus, CanonicalRow,
    ContentMode, ExplicitPairContext, FileRole, ProvenanceJoinResult, RecordKey, RepresentationDescriptor,
    ScalarCalculation, TailSelectionOptions, ValidationCoverage, ValidationMessage,
    ValidationSeverity, VersionOrderResult,
)
from ..representations.base import _literal_text, _selected_records
from ..representations.compatibility import (
    RepresentationBasisCompatibility, StateMappingDeclaration, validate_representation_basis,
)
from ..representations.content_hash import assign_content_states, select_content_representation
from ..representations.field import assign_field_states, select_field_representation
from ..result import ExecutionStatus, ReportStatus
from ..utils.hashing import sha256_canonical
from .bounds import (
    DirectClosureExposureBounds, LineageClosureExposureBounds, direct_closure_exposure,
    lineage_closure_exposure,
)
from .diversity import (
    StateDistributionResult, SupportComparison, _harmonize_distribution,
    calculate_state_distribution, compare_support,
)
from .provenance import ProvenanceCompositionResult, summarize_provenance
from .tail import TailSelectionResult, _options as _tail_options, select_tail

if TYPE_CHECKING:
    from ..lineage.ancestry import SelectedLineageResult, TargetLineageSummary
    from ..lineage.graph import LineageLimits, LineageResourceUsage


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
    promoted = _promotions(validation)
    joined = join_provenance(validation.records, validation.provenance,
                             strict_mode=bool(promoted), strict_warning_codes=promoted)
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
        return sha256_canonical((records, joined.provenance_supplied, provenance, joined.promoted_warning_codes,
            _plain(order.declarations),
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


_DISTRIBUTION_DELTAS = ("record_count_delta", "support_delta", "gini_simpson_diversity_delta")
_COVERAGE_DELTAS = ("provenance_row_coverage_delta", "provenance_required_field_coverage_delta",
                    "grounding_field_coverage_delta")
_PROVENANCE_DELTAS = (*_COVERAGE_DELTAS, "missing_provenance_share_delta")
_DIRECT_DELTAS = ("direct_closure_lower_bound_delta", "direct_closure_upper_bound_delta",
                  "direct_closure_interval_width_delta")
_SOURCE_CATEGORIES = ("human", "synthetic", "mixed", "sensor", "unknown")
_DELTA_METADATA = {
    "record_count_delta": ("T1", "F-018", "records"),
    "support_delta": ("T1", "F-005", "states"),
    "gini_simpson_diversity_delta": ("T1", "F-018", "dimensionless"),
    **{name: ("PR-004", "F-018", "ratio") for name in _PROVENANCE_DELTAS},
    "source_type_share_deltas": ("PR-005", "F-018", "ratio"),
    **{name: ("T3", "F-018", "ratio") for name in _DIRECT_DELTAS},
}

_LINEAGE_DELTA_METADATA = {
    "distinct_external_root_count_delta": ("T4", "roots"),
    "ancestry_concentration_hhi_delta": ("T4", "ratio"),
    "effective_external_root_count_delta": ("T4", "roots"),
    "unresolved_parent_reference_count_delta": ("PR-008", "reference_entries"),
    "resolved_parent_edge_coverage_delta": ("PR-008", "ratio"),
    "resolved_lineage_coverage_delta": ("T4", "ratio"),
    "external_ancestry_coverage_delta": ("T4", "ratio"),
    "lineage_closure_lower_bound_delta": ("T3", "ratio"),
    "lineage_closure_upper_bound_delta": ("T3", "ratio"),
    "lineage_closure_interval_width_delta": ("T3", "ratio"),
}


@dataclass(frozen=True, slots=True)
class LongitudinalLineageDelta:
    """Series wrapper preserving finite partial ancestry values and both bases."""

    metric_name: str
    owner_id: str
    unit: str
    earlier_scope: CalculationScope
    later_scope: CalculationScope
    earlier_value: int | float | None
    later_value: int | float | None
    value: int | float | None
    status: ReportStatus
    reason_codes: tuple[str, ...]
    earlier_denominator: int | None
    later_denominator: int | None
    earlier_coverage: ValidationCoverage | None
    later_coverage: ValidationCoverage | None
    earlier_reason_codes: tuple[str, ...]
    later_reason_codes: tuple[str, ...]
    earlier_status: ReportStatus
    later_status: ReportStatus
    formula_id: str = "F-018"
    evidence_class: CalculationEvidenceClass = CalculationEvidenceClass.DERIVED_METRIC
    representation: None = None
    method: str = "later minus earlier"
    denominator: None = None
    denominator_reason: str = "not_applicable_to_difference"
    earlier_no_declared_parents: bool | None = None
    later_no_declared_parents: bool | None = None

    def __post_init__(self) -> None:
        if (_LINEAGE_DELTA_METADATA.get(self.metric_name) != (self.owner_id, self.unit)
                or self.formula_id != "F-018" or self.method != "later minus earlier"
                or self.evidence_class is not CalculationEvidenceClass.DERIVED_METRIC
                or self.representation is not None or self.denominator is not None
                or self.denominator_reason != "not_applicable_to_difference"):
            raise _invalid("lineage delta must preserve its approved ownership and method")
        if (type(self.earlier_scope) is not CalculationScope or type(self.later_scope) is not CalculationScope
                or len(self.earlier_scope.dataset_versions) != 1 or len(self.later_scope.dataset_versions) != 1
                or self.earlier_scope.dataset_versions == self.later_scope.dataset_versions
                or self.earlier_scope.excluded_record_keys or self.later_scope.excluded_record_keys):
            raise _invalid("lineage delta requires two complete target scopes")
        for value in (self.earlier_value, self.later_value, self.value):
            try:
                valid = value is None or type(value) in (int, float) and isfinite(value)
            except OverflowError:
                valid = False
            if not valid:
                raise _invalid("lineage delta values must be finite numbers or null")
        for denominator in (self.earlier_denominator, self.later_denominator):
            if denominator is not None and (type(denominator) is not int or denominator < 0):
                raise _invalid("lineage endpoint denominator must be an exact nonnegative count")
        for coverage in (self.earlier_coverage, self.later_coverage):
            if coverage is not None and type(coverage) is not ValidationCoverage:
                raise _invalid("lineage endpoint coverage must retain its named basis")
        for status, value, reasons in ((self.status, self.value, self.reason_codes),
                (self.earlier_status, self.earlier_value, self.earlier_reason_codes),
                (self.later_status, self.later_value, self.later_reason_codes)):
            if (type(status) is not ReportStatus or status is ReportStatus.EXPERIMENTAL or type(reasons) is not tuple
                    or any(type(code) is not str or not code for code in reasons)
                    or (status is ReportStatus.UNAVAILABLE) != (value is None)
                    or status is ReportStatus.AVAILABLE and reasons
                    or status is not ReportStatus.AVAILABLE and not reasons):
                raise _invalid("lineage delta status must preserve null, partial and available distinctions")
        for flag in (self.earlier_no_declared_parents, self.later_no_declared_parents):
            if flag is not None and type(flag) is not bool:
                raise _invalid("reference coverage convention requires literal boolean flags")
        if self.status is not ReportStatus.UNAVAILABLE:
            if (self.earlier_value is None or self.later_value is None
                    or self.value != self.later_value - self.earlier_value
                    or (self.status is ReportStatus.PARTIAL) !=
                       (ReportStatus.PARTIAL in (self.earlier_status, self.later_status))):
                raise _invalid("lineage difference must retain both finite endpoints and partial dependency")


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
        if _DELTA_METADATA.get(self.metric_name) != (self.owner_id, self.formula_id, self.unit):
            raise _invalid("delta ownership, formula and unit must match the approved field")
        if self.metric_name not in _DISTRIBUTION_DELTAS and self.representation is not None:
            raise _invalid("provenance and direct-bound deltas have no representation basis")
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
    provenance: ProvenanceCompositionResult | None = field(default=None, repr=False)
    direct_closure: DirectClosureExposureBounds | None = field(default=None, repr=False)
    lineage: TargetLineageSummary | None = field(default=None, repr=False)
    lineage_closure: LineageClosureExposureBounds | None = field(default=None, repr=False)

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
        if self.lineage is not None:
            from ..lineage.ancestry import TargetLineageSummary
            if (type(self.lineage) is not TargetLineageSummary
                    or self.lineage.population_scope != self.scope.population_scope
                    or type(self.lineage_closure) is not LineageClosureExposureBounds
                    or self.lineage_closure.source != self.lineage
                    or self.family_statuses[-1] != _lineage_snapshot_family(self)):
                raise _invalid("lineage snapshot must retain its selected complete population and bounds")
        elif self.lineage_closure is not None:
            raise _invalid("lineage bounds require the selected target evidence")
        provenance, bounds = self.provenance, self.direct_closure
        if not self.record_count.value:
            if provenance is not None or bounds is not None:
                raise _invalid("empty snapshots cannot supply fabricated provenance calculations")
        elif (type(provenance) is not ProvenanceCompositionResult
                or type(bounds) is not DirectClosureExposureBounds
                or provenance.scope != _provenance_scope(self.scope)
                or provenance.analyzed_record_count.value != self.record_count.value
                or provenance.weighted_source is not None or bounds.scope != provenance.scope
                or bounds.denominator != self.record_count.value
                or (bounds.known_open_count, bounds.known_closed_count, bounds.unresolved_grounding_count) !=
                   (provenance.direct_grounding.known_open_count.value,
                    provenance.direct_grounding.known_closed_count.value,
                    provenance.direct_grounding.unresolved_grounding_count.value)
                or bounds.provenance_row_coverage != provenance.provenance_row_coverage
                or bounds.provenance_required_field_coverage != provenance.provenance_required_field_coverage
                or bounds.grounding_field_coverage != provenance.grounding_field_coverage
                or bounds.validation_messages != provenance.validation_messages
                or bounds.input_has_errors != provenance.input_has_errors):
            raise _invalid("snapshot provenance and bounds must retain their complete population and evidence")
        if bounds is not None:
            _validate_snapshot_bounds(provenance, bounds)
        if self.family_statuses[1:3] != _snapshot_evidence_families(provenance, bounds):
            raise _invalid("snapshot evidence availability differs from its family status")


@dataclass(frozen=True, slots=True)
class LongitudinalPairResult:
    pair: LongitudinalPair
    compatibility: RepresentationBasisCompatibility | None = field(repr=False)
    support_comparison: SupportComparison | None = field(repr=False)
    deltas: tuple[LongitudinalDelta, ...]
    tail_disappearance: TailDisappearanceResult | None
    family_statuses: tuple[LongitudinalFamilyStatus, ...]
    source_type_share_deltas: MappingProxyType = field(repr=False)
    messages: tuple[ValidationMessage, ...] = ()
    lineage_deltas: tuple[LongitudinalLineageDelta, ...] = ()

    def __post_init__(self) -> None:
        _result_rows(self.family_statuses, self.messages)
        if (type(self.lineage_deltas) is not tuple
                or any(type(delta) is not LongitudinalLineageDelta for delta in self.lineage_deltas)
                or self.lineage_deltas and tuple(d.metric_name for d in self.lineage_deltas)
                    != tuple(_LINEAGE_DELTA_METADATA)):
            raise _invalid("requested lineage deltas require the complete immutable inventory")
        if (type(self.pair) is not LongitudinalPair or type(self.deltas) is not tuple
                or any(type(delta) is not LongitudinalDelta for delta in self.deltas)
                or tuple(delta.metric_name for delta in self.deltas) !=
                (*_DISTRIBUTION_DELTAS, *_PROVENANCE_DELTAS, *_DIRECT_DELTAS)):
            raise _invalid("pair result requires the complete scoped delta inventory")
        shares = self.source_type_share_deltas
        if (type(shares) not in (dict, MappingProxyType) or tuple(shares) != _SOURCE_CATEGORIES
                or any(type(d) is not LongitudinalDelta or d.metric_name != "source_type_share_deltas"
                       for d in shares.values())):
            raise _invalid("source-share deltas require all five declared categories")
        object.__setattr__(self, "source_type_share_deltas", MappingProxyType(dict(shares)))
        for delta in (*self.deltas, *shares.values(), *self.lineage_deltas):
            if (delta.earlier_scope.dataset_versions != (self.pair.earlier_version,)
                    or delta.later_scope.dataset_versions != (self.pair.later_version,)):
                raise _invalid("pair delta endpoints disagree with the scheduled pair")
        if self.compatibility is None:
            if self.support_comparison is not None or any(d.value is not None for d in
                    (*self.deltas, *shares.values(), *self.lineage_deltas)):
                raise _invalid("blocked pair cannot carry available comparison values")
        elif self.compatibility != self.pair.compatibility:
            raise _invalid("pair result must retain its declared compatible basis")
        if self.family_statuses[1:3] != _pair_evidence_families(self.deltas, shares, self.messages):
            raise _invalid("pair evidence availability differs from its family status")
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
    shared_lineage: SelectedLineageResult | None = field(default=None, repr=False)
    lineage_requested: bool = False
    lineage_limits: LineageLimits | None = None
    lineage_input_signature: str | None = field(default=None, repr=False)
    lineage_resource_usage: LineageResourceUsage | None = None

    def __post_init__(self) -> None:
        if (type(self.selection) is not LongitudinalSelection or type(self.snapshots) is not tuple
                or any(type(item) is not SnapshotSummary for item in self.snapshots)
                or type(self.comparisons) is not tuple
                or any(type(item) is not LongitudinalPairResult for item in self.comparisons)
                or tuple(s.scope.dataset_version for s in self.snapshots) != self.selection.selected_order
                or tuple(p.pair for p in self.comparisons) != self.selection.pairs):
            raise _invalid("series results must retain every selected snapshot and scheduled pair")
        for selected, snapshot in zip(self.selection.snapshots, self.snapshots):
            if (selected.population_scope != snapshot.scope.population_scope
                    or selected.declaration != snapshot.scope.declaration):
                raise _invalid("analyzed snapshot no longer matches its selected declaration")
        snapshots = {s.scope.dataset_version: s for s in self.snapshots}
        for pair in self.comparisons:
            earlier, later = snapshots[pair.pair.earlier_version], snapshots[pair.pair.later_version]
            count = pair.deltas[0]
            if (count.earlier_value != earlier.record_count.value or count.later_value != later.record_count.value):
                raise _invalid("record-count delta must use the complete endpoint populations")
            expected = tuple(_evidence_delta(name, earlier, later, pair.compatibility)
                             for name in (*_PROVENANCE_DELTAS, *_DIRECT_DELTAS))
            shares = {category: _evidence_delta("source_type_share_deltas", earlier, later,
                        pair.compatibility, category=category) for category in _SOURCE_CATEGORIES}
            if pair.deltas[3:] != expected or pair.source_type_share_deltas != shares:
                raise _invalid("provenance/direct deltas must retain their exact endpoint evidence")
            if any(message not in pair.messages for message in _pair_provenance_errors(earlier, later)):
                raise _invalid("pair execution cannot discard its endpoints' provenance errors")
            if self.lineage_requested:
                expected_lineage = tuple(_lineage_delta(name, earlier, later, pair.compatibility)
                                         for name in _LINEAGE_DELTA_METADATA)
                if (pair.lineage_deltas != expected_lineage
                        or pair.family_statuses[-1] != _lineage_pair_family(expected_lineage, earlier, later)):
                    raise _invalid("lineage changes must retain their target values, coverage and execution")
            elif pair.lineage_deltas:
                raise _invalid("unrequested lineage cannot supply comparison values")
        _validate_series_lineage(self)
        options = None if self.tail_options is None else _tail_options(self.tail_options)
        if self.input_signature != _analysis_signature(self.selection, options, self.lineage_requested,
                                                       self.lineage_limits, self.lineage_input_signature):
            raise _invalid("series input binding differs from its selection or requested calculations")
        if any((pair.tail_disappearance is None) != (options is None) for pair in self.comparisons):
            raise _invalid("series tail results must match explicit enablement")
        if (type(self.execution_status) is not ExecutionStatus or type(self.reason_codes) is not tuple
                or any(type(code) is not str or not code for code in self.reason_codes)
                or type(self.messages) is not tuple or any(type(m) is not ValidationMessage for m in self.messages)):
            raise _invalid("series execution status and diagnostics require immutable typed values")
        if (self.execution_status, self.reason_codes) != _series_execution(self.snapshots, self.comparisons):
            raise _invalid("series execution must reflect all requested snapshot and pair families")


def _result_rows(families, messages):
    if (type(families) is not tuple or any(type(f) is not LongitudinalFamilyStatus for f in families)
            or tuple(f.family for f in families) != ("distribution", "provenance", "direct_closure", "tail", "lineage")
            or type(messages) is not tuple or any(type(m) is not ValidationMessage for m in messages)):
        raise _invalid("analytical summaries require immutable complete family rows and diagnostics")


def _analysis_signature(selection, options, lineage=False, limits=None, lineage_signature=None):
    return sha256_canonical((selection.input_signature, None if options is None else
        (options.rule, options.count_threshold, options.frequency_threshold, options.state_ids),
        lineage, None if limits is None else (limits.max_nodes, limits.max_edges,
            limits.max_root_memberships, limits.max_root_union_visits), lineage_signature))


def _validate_series_lineage(result):
    if type(result.lineage_requested) is not bool:
        raise _invalid("lineage request must be a literal boolean")
    if not result.lineage_requested:
        if (any(value is not None for value in (result.shared_lineage, result.lineage_limits,
                result.lineage_input_signature, result.lineage_resource_usage))
                or any(s.lineage is not None for s in result.snapshots)
                or any(item.family_statuses[-1].execution_status is not ExecutionStatus.NOT_REQUESTED
                       for item in (*result.snapshots, *result.comparisons))):
            raise _invalid("unrequested lineage cannot contain executed evidence")
        return
    from ..lineage.ancestry import SelectedLineageResult
    from ..lineage.graph import LineageResourceUsage, _limits
    limits = _limits(result.lineage_limits)
    signature = result.lineage_input_signature
    usage = result.lineage_resource_usage
    if (type(signature) is not str or len(signature) != 64 or any(c not in "0123456789abcdef" for c in signature)
            or type(usage) is not LineageResourceUsage or usage.limits != limits):
        raise _invalid("requested lineage requires input binding and its exact work budget")
    shared = result.shared_lineage
    if shared is None:
        if (usage.exhausted_limit not in ("max_nodes", "max_edges")
                or any(s.lineage is not None or s.family_statuses[-1].execution_status is not ExecutionStatus.FAILED
                       for s in result.snapshots)):
            raise _invalid("missing shared graph must disclose its failed admission stage")
    elif (type(shared) is not SelectedLineageResult or shared.selected_versions != result.selection.selected_order
            or shared.selection_signature != result.selection.input_signature
            or shared.input_signature != signature or shared.resource_usage != usage
            or tuple(s.lineage for s in result.snapshots) != shared.targets):
        raise _invalid("series lineage must retain the complete selected shared analysis")


def _lineage_endpoint(snapshot, name, *, target=None, bounds=None):
    target = snapshot.lineage if target is None else target
    if target is None:
        unknown_denominator = name in (
            "ancestry_concentration_hhi_delta", "effective_external_root_count_delta",
            "unresolved_parent_reference_count_delta", "resolved_parent_edge_coverage_delta")
        denominator = None if unknown_denominator else len(snapshot.scope.population_scope.included_record_keys)
        return None, denominator, None, ReportStatus.UNAVAILABLE, ("LINEAGE_RESOURCE_LIMIT_EXCEEDED",), None
    total = target.scope.target_record_count
    metric = name.removesuffix("_delta")
    reference = metric in ("unresolved_parent_reference_count", "resolved_parent_edge_coverage")
    concentration = metric in ("ancestry_concentration_hhi", "effective_external_root_count")
    if reference:
        denominator = target.declared_parent_reference_count
        coverage = None if denominator is None else ValidationCoverage(
            target.resolved_parent_reference_count, denominator, "declared_parent_references")
        value = getattr(target, metric)
        status = ReportStatus.UNAVAILABLE if value is None else ReportStatus.AVAILABLE
        reasons = target.reference_coverage_reason_codes
        return value, denominator, coverage, status, reasons, target.no_declared_parents
    denominator = target.grounded_record_count if concentration else total
    resolved = target.records_with_resolved_external_ancestry
    if metric in ("distinct_external_root_count", "ancestry_concentration_hhi", "effective_external_root_count"):
        coverage = None if target.records is None else ValidationCoverage(
            target.grounded_record_count, total, "all_valid_records_in_selected_dataset_scope")
        value = getattr(target, metric)
        status = target.concentration_status if concentration else target.root_metrics_status
        reasons = (target.concentration_reason_codes if concentration and value is None else
                   ("LINEAGE_RESOURCE_LIMIT_EXCEEDED",) if target.records is None else
                   ("UNRESOLVED_ANCESTRY",) if status is ReportStatus.PARTIAL else ())
    else:
        coverage = None if resolved is None else ValidationCoverage(
            resolved, total, "all_valid_records_in_selected_dataset_scope")
        if metric.startswith("lineage_closure_"):
            bounds = snapshot.lineage_closure if bounds is None else bounds
            value = getattr(bounds, metric.removeprefix("lineage_closure_"))
            status, reasons = bounds.status, bounds.reason_codes
        else:
            value = getattr(target, metric)
            status = ReportStatus.UNAVAILABLE if value is None else ReportStatus.AVAILABLE
            reasons = target.ancestry_coverage_reason_codes
    return value, denominator, coverage, status, reasons, None


def _lineage_delta(name, earlier, later, basis):
    a, an, ac, ast, ar, af = _lineage_endpoint(earlier, name)
    b, bn, bc, bst, br, bf = _lineage_endpoint(later, name)
    unavailable = basis is None or a is None or b is None
    partial = ReportStatus.PARTIAL in (ast, bst)
    reasons = tuple(dict.fromkeys(
        (("R_LONGITUDINAL_PAIR_BLOCKED", CalculationReason.REPRESENTATION_INCOMPATIBLE.value) if basis is None else ())
        + (("R_LONGITUDINAL_ENDPOINT_UNAVAILABLE",) if a is None or b is None else ())
        + (("R_LONGITUDINAL_PARTIAL_COVERAGE",) if partial else ()) + ar + br
        + tuple("EARLIER_" + reason for reason in ar if ast is ReportStatus.UNAVAILABLE)
        + tuple("LATER_" + reason for reason in br if bst is ReportStatus.UNAVAILABLE)))
    owner, unit = _LINEAGE_DELTA_METADATA[name]
    return LongitudinalLineageDelta(name, owner, unit,
        earlier.scope.population_scope, later.scope.population_scope, a, b, None if unavailable else b - a,
        ReportStatus.UNAVAILABLE if unavailable else ReportStatus.PARTIAL if partial else ReportStatus.AVAILABLE,
        reasons, an, bn, ac, bc, ar, br, ast, bst,
        earlier_no_declared_parents=af, later_no_declared_parents=bf)


def _lineage_family(statuses, reasons):
    reasons = tuple(dict.fromkeys(reasons))
    useful = any(status is not ReportStatus.UNAVAILABLE for status in statuses)
    completed = all(status is ReportStatus.AVAILABLE for status in statuses) and not reasons
    return _family("lineage", ExecutionStatus.COMPLETED if completed else
                   ExecutionStatus.PARTIAL if useful else ExecutionStatus.FAILED, reasons)


def _lineage_snapshot_family(snapshot, *, target=None, bounds=None):
    target = snapshot.lineage if target is None else target
    endpoints = tuple(_lineage_endpoint(snapshot, name, target=target, bounds=bounds)
                      for name in _LINEAGE_DELTA_METADATA)
    reasons = tuple(reason for endpoint in endpoints for reason in endpoint[4])
    if target is not None:
        reasons += target.execution_reason_codes
    return _lineage_family(tuple(endpoint[3] for endpoint in endpoints), reasons)


def _lineage_pair_family(deltas, earlier, later):
    reasons = tuple(reason for delta in deltas for reason in delta.reason_codes)
    for snapshot in (earlier, later):
        if snapshot.lineage is not None:
            reasons += snapshot.lineage.execution_reason_codes
    return _lineage_family(tuple(delta.status for delta in deltas), reasons)


def _attach_lineage(validation, selection, snapshots, limits):
    from ..lineage.ancestry import analyze_selected_lineage, _selected_lineage_signature
    signature = _selected_lineage_signature(validation, selection, limits)
    try:
        shared = analyze_selected_lineage(validation, selection=selection, limits=limits)
    except LineageResourceLimitError as error:
        family = _family("lineage", ExecutionStatus.FAILED, (error.reason_code,))
        message = _message(error, "longitudinal_lineage")
        return tuple(replace(snapshot, family_statuses=(*snapshot.family_statuses[:-1], family),
                             messages=(*snapshot.messages, message)) for snapshot in snapshots), None, error.resource_usage, signature
    attached = []
    for snapshot, target in zip(snapshots, shared.targets, strict=True):
        bounds = lineage_closure_exposure(target)
        family = _lineage_snapshot_family(snapshot, target=target, bounds=bounds)
        attached.append(replace(snapshot, lineage=target, lineage_closure=bounds,
            family_statuses=(*snapshot.family_statuses[:-1], family),
            messages=tuple(dict.fromkeys((*snapshot.messages, *target.messages)))))
    return tuple(attached), shared, shared.resource_usage, signature


def _family(family, status, reasons=()):
    return LongitudinalFamilyStatus(family, status, tuple(dict.fromkeys(str(code) for code in reasons)))


def _families(distribution, provenance, direct, tail=None):
    return (distribution, provenance, direct,
        tail or _family("tail", ExecutionStatus.NOT_REQUESTED, ("R_LONGITUDINAL_FAMILY_NOT_REQUESTED",)),
        _family("lineage", ExecutionStatus.NOT_REQUESTED, ("R_LONGITUDINAL_FAMILY_NOT_REQUESTED",)))


def _promotions(validation):
    if type(validation.provenance_join) is not ProvenanceJoinResult:
        raise _invalid("series provenance requires the retained validation join")
    # join_provenance validates the literal registry and rebuilds warning severity.
    return validation.provenance_join.promoted_warning_codes


def _provenance_scope(snapshot):
    # Same complete population, using the existing provenance owner's convention.
    return replace(snapshot.population_scope,
        denominator_basis="all_valid_records_in_selected_dataset_scope",
        scope_id=snapshot.population_scope.scope_id + "-provenance")


def _snapshot_evidence_families(provenance, bounds):
    if provenance is None:
        return tuple(_family(name, ExecutionStatus.FAILED, (CalculationReason.EMPTY_SCOPE,))
                     for name in ("provenance", "direct_closure"))
    errors = _input_error_codes(_local_provenance_errors(provenance))
    reasons = tuple(dict.fromkeys((*provenance.source.reason_codes, *provenance.confidence.reason_codes, *errors)))
    return (_family("provenance", ExecutionStatus.PARTIAL if reasons else ExecutionStatus.COMPLETED, reasons),
            _family("direct_closure", (ExecutionStatus.PARTIAL if errors else ExecutionStatus.COMPLETED)
                    if bounds.status is CalculationStatus.AVAILABLE else ExecutionStatus.FAILED,
                    (*bounds.lower_bound.reason_codes, *errors)))


def _input_error_codes(messages):
    return tuple(dict.fromkeys(m.code for m in messages
        if m.severity in (ValidationSeverity.ERROR, ValidationSeverity.FATAL)))


def _local_provenance_errors(provenance):
    if provenance is None:
        return ()
    keys = set(provenance.scope.included_record_keys)
    return tuple(m for m in provenance.validation_messages if m.record_key in keys
                 and m.severity in (ValidationSeverity.ERROR, ValidationSeverity.FATAL))


def _pair_provenance_errors(earlier, later):
    return tuple(dict.fromkeys((*_local_provenance_errors(earlier.provenance),
                               *_local_provenance_errors(later.provenance))))


def _snapshot_provenance(snapshot, validation):
    if not snapshot.population_scope.included_record_keys:
        return None, None
    promoted = _promotions(validation)
    # Keep the owner join's full-input identity/error checks. Only coverage and
    # composition are scoped. Context and other snapshots never enter N.
    joined = join_provenance(validation.records, validation.provenance,
        dataset_versions=(snapshot.dataset_version,), strict_mode=bool(promoted), strict_warning_codes=promoted)
    provenance = summarize_provenance(joined, scope=_provenance_scope(snapshot))
    return provenance, direct_closure_exposure(provenance)


def _validate_snapshot_bounds(provenance, bounds):
    total = bounds.denominator
    counts = bounds.known_open_count, bounds.known_closed_count, bounds.unresolved_grounding_count
    if (any(type(count) is not int or count < 0 for count in counts) or sum(counts) != total
            or bounds.denominator_basis != bounds.scope.denominator_basis):
        raise _invalid("snapshot direct counts must partition the complete population")
    available = provenance.provenance_required_field_coverage.numerator > 0
    expected = (counts[1] / total, (counts[1] + counts[2]) / total, counts[2] / total)
    for scalar, field_name, formula, value in zip(
            (bounds.lower_bound, bounds.upper_bound, bounds.interval_width),
            ("lower_bound", "upper_bound", "interval_width"), ("F-009", "F-010", None), expected):
        if (type(scalar) is not ScalarCalculation or scalar.metadata.scope != bounds.scope
                or scalar.metadata.metric_name != "direct_closure_exposure_" + field_name
                or scalar.metadata.owner_id != "T3" or scalar.metadata.formula_id != formula
                or scalar.metadata.unit != "ratio" or scalar.metadata.representation is not None
                or scalar.metadata.evidence_class is not CalculationEvidenceClass.DERIVED_METRIC
                or scalar.status is not (CalculationStatus.AVAILABLE if available else CalculationStatus.UNAVAILABLE)
                or scalar.value != (value if available else None)
                or scalar.reason_codes != (() if available else (CalculationReason.PROVENANCE_FIELD_UNAVAILABLE,))):
            raise _invalid("snapshot direct interval must preserve its existing count envelope and availability")


def _evidence_endpoint(snapshot, name, category):
    provenance, bounds = snapshot.provenance, snapshot.direct_closure
    scope = provenance.scope if provenance is not None else _provenance_scope(snapshot.scope)
    total = len(scope.included_record_keys)
    if provenance is None:
        return scope, None, total, None, (CalculationReason.EMPTY_SCOPE,)
    if name in _COVERAGE_DELTAS:
        coverage = getattr(provenance, name.removesuffix("_delta"))
        return scope, coverage.ratio, total, coverage, ()
    if name == "source_type_share_deltas":
        source = provenance.source
        return (scope, None if source.shares is None else dict(source.shares)[category],
                total, source.field_coverage, source.reason_codes)
    if name == "missing_provenance_share_delta":
        scalar, coverage = provenance.missing_provenance_share, provenance.provenance_row_coverage
    else:
        scalar = getattr(bounds, name.removeprefix("direct_closure_").removesuffix("_delta"))
        coverage = bounds.grounding_field_coverage
    return scope, scalar.value, total, coverage, scalar.reason_codes


def _evidence_delta(name, earlier, later, basis, *, category=None):
    left_scope, left, left_n, left_coverage, left_reasons = _evidence_endpoint(earlier, name, category)
    right_scope, right, right_n, right_coverage, right_reasons = _evidence_endpoint(later, name, category)
    reasons = tuple(dict.fromkeys((() if basis is not None else
        (CalculationReason.REPRESENTATION_INCOMPATIBLE,)) + left_reasons + right_reasons))
    owner, formula, unit = _DELTA_METADATA[name]
    return LongitudinalDelta(name, owner, formula, unit, left_scope, right_scope, None,
        left, right, None if reasons else right - left,
        CalculationStatus.UNAVAILABLE if reasons else CalculationStatus.AVAILABLE, reasons,
        left_n, right_n, left_coverage, right_coverage, left_reasons, right_reasons)


def _delta_family(name, deltas, errors):
    reasons = tuple(dict.fromkeys((*errors, *(reason for delta in deltas for reason in delta.reason_codes))))
    available = sum(delta.status is CalculationStatus.AVAILABLE for delta in deltas)
    status = (ExecutionStatus.COMPLETED if available == len(deltas) and not errors else
              ExecutionStatus.PARTIAL if available else ExecutionStatus.FAILED)
    return _family(name, status, reasons)


def _pair_evidence_families(deltas, shares, messages):
    # Only provenance diagnostics in these rows carry record identities;
    # representation/tail execution errors have their separate family owners.
    errors = _input_error_codes(m for m in messages if m.record_key is not None)
    return (_delta_family("provenance", (*deltas[3:7], *shares.values()), errors),
            _delta_family("direct_closure", deltas[7:], errors))


def _series_execution(snapshots, comparisons):
    reasons = []
    if any(pair.compatibility is None for pair in comparisons):
        reasons.append("R_LONGITUDINAL_PAIR_BLOCKED")
    if any(f.execution_status not in (ExecutionStatus.COMPLETED, ExecutionStatus.NOT_REQUESTED)
           for item in (*snapshots, *comparisons) for f in item.family_statuses):
        reasons.append("R_LONGITUDINAL_ENDPOINT_UNAVAILABLE")
    reasons.extend(_input_error_codes(message for item in (*snapshots, *comparisons) for message in item.messages))
    useful = any(delta.status is CalculationStatus.AVAILABLE for pair in comparisons
                 for delta in (*pair.deltas, *pair.source_type_share_deltas.values()))
    useful = useful or any(delta.status is not ReportStatus.UNAVAILABLE for pair in comparisons
                           for delta in pair.lineage_deltas)
    status = (ExecutionStatus.COMPLETED if not reasons else
              ExecutionStatus.PARTIAL if useful else ExecutionStatus.FAILED)
    return status, tuple(reasons)


def _message(error, field_name):
    return ValidationMessage(error.code.value, ValidationSeverity.ERROR, error.safe_message, field=field_name)


def _count(name, count, snapshot, *, representation=None, reasons=()):
    metadata = CalculationMetadata(name, "PR-002" if name == "record_count" else "PR-011", None,
        CalculationEvidenceClass.OBSERVED_FACT, "records",
        "PR-002.record_count" if name == "record_count" else "cardinality of explicit representation scope",
        snapshot.population_scope, representation)
    return ScalarCalculation(metadata, CalculationStatus.UNAVAILABLE if reasons else CalculationStatus.AVAILABLE,
                             None if reasons else count, reasons)


def _snapshot_distribution(snapshot, records, ordinal, validation):
    declaration = snapshot.declaration
    config = declaration.representation
    distribution, messages, reasons = None, (), ()
    try:
        if config.source == "content_hash":
            if validation.content_mode is ContentMode.LOCAL_REF and records:
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
    provenance, bounds = _snapshot_provenance(snapshot, validation)
    provenance_family, direct_family = _snapshot_evidence_families(provenance, bounds)
    if provenance is not None:
        messages += provenance.validation_messages
    return SnapshotSummary(snapshot, distribution, record_count, included, excluded,
        _families(_family("distribution", status, reasons), provenance_family, direct_family),
        messages, provenance, bounds)


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


def _pair_result(pair, earlier, later, order, options, lineage=False):
    basis, comparison, a, b, reasons, messages = _pair_distributions(pair, earlier, later, order)
    deltas = tuple(_delta(name, earlier, later, basis, a, b, reasons, comparison=comparison)
        for name in _DISTRIBUTION_DELTAS)
    deltas += tuple(_evidence_delta(name, earlier, later, basis) for name in (*_PROVENANCE_DELTAS, *_DIRECT_DELTAS))
    shares = {category: _evidence_delta("source_type_share_deltas", earlier, later, basis, category=category)
              for category in _SOURCE_CATEGORIES}
    messages += _pair_provenance_errors(earlier, later)
    provenance_family, direct_family = _pair_evidence_families(deltas, shares, messages)
    distribution_status = (ExecutionStatus.COMPLETED if comparison is not None else
                           ExecutionStatus.PARTIAL if basis is not None else ExecutionStatus.FAILED)
    tail, tail_status = None, None
    if options is not None:
        tail, tail_messages = _tail_disappearance(options, basis, comparison, earlier, later, a, reasons)
        messages += tail_messages
        tail_status = _family("tail", ExecutionStatus.COMPLETED if tail.status is CalculationStatus.AVAILABLE
                              else ExecutionStatus.FAILED, tail.reason_codes)
    families = _families(_family("distribution", distribution_status, reasons), provenance_family, direct_family, tail_status)
    lineage_deltas = ()
    if lineage:
        lineage_deltas = tuple(_lineage_delta(name, earlier, later, basis) for name in _LINEAGE_DELTA_METADATA)
        families = (*families[:-1], _lineage_pair_family(lineage_deltas, earlier, later))
    return LongitudinalPairResult(pair, basis, comparison, deltas, tail, families, shares, messages, lineage_deltas)


def analyze_longitudinal(
    validation: BundleValidationResult, *, selection: LongitudinalSelection,
    lineage: bool = False, tail_options: TailSelectionOptions | None = None, lineage_limits=None,
) -> LongitudinalResult:
    """Compute unweighted original snapshots and observed pair-local changes.

    Records are grouped once and each selected distribution runs once. Context
    supplies no snapshot denominator. Unavailable endpoints preserve record
    deltas only under a valid comparison basis; state sets remain null. Tail is
    opt-in and uses the harmonized earlier distribution. Each nonempty snapshot
    retains its complete provenance and direct-bound results, independently of
    representation exclusions. All pair deltas require a compatible basis.
    Explicit lineage uses one shared graph/cycle/root pass and target-only
    summaries. Its complete or partial values never change distribution scopes.
    """
    if type(lineage) is not bool or not lineage and lineage_limits is not None:
        raise _invalid("lineage requires an explicit boolean request before limits are supplied")
    if lineage:
        from ..lineage.graph import LineageLimits, _limits
        lineage_limits = _limits(LineageLimits() if lineage_limits is None else lineage_limits)
    options = None if tail_options is None else _tail_options(tail_options)
    selection = validate_longitudinal_selection(validation, selection)
    grouped = {version: [] for version in selection.selected_versions}
    for row in validation.records:
        if row.record_key.dataset_version in grouped:
            grouped[row.record_key.dataset_version].append(row)
    snapshots = tuple(_snapshot_distribution(scope, tuple(grouped[scope.dataset_version]), index, validation)
                      for index, scope in enumerate(selection.snapshots, 1))
    shared, usage, lineage_signature = None, None, None
    if lineage:
        snapshots, shared, usage, lineage_signature = _attach_lineage(validation, selection, snapshots, lineage_limits)
    index = {snapshot.scope.dataset_version: snapshot for snapshot in snapshots}
    comparisons = tuple(_pair_result(pair, index[pair.earlier_version], index[pair.later_version],
                                    selection.version_order, options, lineage) for pair in selection.pairs)
    status, reasons = _series_execution(snapshots, comparisons)
    # A full-input required-field diagnostic may be inherited by multiple
    # snapshot joins. Retain it once in the series without dropping local copies.
    messages = tuple(dict.fromkeys(message for item in (*snapshots, *comparisons) for message in item.messages))
    signature = _analysis_signature(selection, options, lineage, lineage_limits, lineage_signature)
    return LongitudinalResult(selection, snapshots, comparisons, status, reasons, messages, signature, options,
                             shared, lineage, lineage_limits, lineage_signature, usage)


def _handoff_equal(actual, expected, label):
    """Require canonical literal types as well as values, including nested leaves."""
    if type(actual) is not type(expected):
        raise _invalid(label + " has an invalid handoff type")
    if is_dataclass(expected):
        for item in fields(expected):
            _handoff_equal(getattr(actual, item.name), getattr(expected, item.name), label)
    elif type(expected) in (dict, MappingProxyType):
        if tuple(actual) != tuple(expected):
            raise _invalid(label + " has different handoff keys")
        for key in expected:
            _handoff_equal(actual[key], expected[key], label)
    elif type(expected) is tuple:
        if len(actual) != len(expected):
            raise _invalid(label + " has different handoff membership")
        for left, right in zip(actual, expected):
            _handoff_equal(left, right, label)
    elif actual != expected:
        raise _invalid(label + " disagrees with its retained input evidence")


def _handoff_distribution(validation, snapshot, rows):
    """Check assignment evidence and supplied arithmetic without metric dispatch."""
    from ..models import RecordStateAssignment, WeightingOptions
    from ..representations.base import _representation_error
    from ..representations.content_hash import exact_content_bytes
    from ..utils.hashing import sha256_bytes
    from .diversity import _metrics

    declaration, scope = snapshot.scope.declaration, snapshot.scope.representation_scope
    config = declaration.representation
    reasons, messages = (), ()
    counts, included, exclusions = {}, [], []
    try:
        if config.source == "content_hash":
            if validation.content_mode is ContentMode.LOCAL_REF and rows:
                raise _invalid("local-reference content payloads are unavailable to series analysis",
                               code=ErrorCode.CONTENT_REF_MISSING)
            selection = select_content_representation(representation_name=config.name,
                representation_version=config.version, normalization_profile=config.normalization_profile)
        else:
            selection = select_field_representation(tuple(rows), dataset_versions=(snapshot.scope.dataset_version,),
                config=config, missing_state_id=declaration.missing_state_id)
        selected = _selected_records(tuple(rows), (snapshot.scope.dataset_version,))
        # Check collisions before missing-cell failures, as the assignment owner does.
        for key, values, location in selected:
            if (config.source != "content_hash" and declaration.missing_state_id is not None
                    and values.get(config.field) == declaration.missing_state_id):
                raise _representation_error(ErrorCode.CONFIG_INVALID,
                    "missing-state ID collides with an observed value", field_name=config.field,
                    key=key, location=location)
        raw_by_digest = {}
        for key, values, location in selected:
            if config.source == "content_hash":
                raw = exact_content_bytes(values["content"], normalization_profile=config.normalization_profile)
                state = sha256_bytes(raw)
                if state in raw_by_digest and raw_by_digest[state] != raw:
                    raise _representation_error(ErrorCode.SCHEMA_TYPE, "equal content digests have unequal bytes",
                                               field_name="content", key=key, location=location)
                raw_by_digest[state] = raw
            else:
                state = values.get(config.field)
                if state is None:
                    if config.missing_value_policy == "error":
                        raise _representation_error(ErrorCode.SCHEMA_REQUIRED_FIELD,
                            "missing state blocks this representation", field_name=config.field,
                            key=key, location=location)
                    if config.missing_value_policy == "exclude":
                        exclusions.append(RecordStateAssignment(key, None, CalculationReason.REPRESENTATION_MISSING))
                        continue
                    state = declaration.missing_state_id
            included.append(key)
            counts[state] = counts.get(state, 0) + 1
    except CanonicalValidationError as error:
        reasons = ((CalculationReason.CONTENT_UNAVAILABLE,) if error.code is ErrorCode.CONTENT_REF_MISSING
                   else (CalculationReason.REPRESENTATION_MISSING,))
        messages = (_message(error, "longitudinal_snapshot"),)
        if scope is not None or snapshot.distribution is not None:
            raise _invalid("failed snapshot assignment cannot supply a distribution")
    else:
        if scope is None or snapshot.distribution is None:
            raise _invalid("valid snapshot assignment cannot be silently omitted")
        expected_scope = CalculationScope((snapshot.scope.dataset_version,), tuple(included),
            tuple(item.record_key for item in exclusions), "included_representation_records", scope.scope_id)
        _handoff_equal(scope, expected_scope, "representation population")
        total = len(included)
        reason = CalculationReason.EMPTY_SCOPE if not rows else CalculationReason.ALL_EXCLUDED if not total else None
        reason_args = dict(reason=reason) if reason else {}
        metric = _metrics(tuple((state, counts[state] / total) for state in sorted(counts)), counts, None,
            scope=scope, representation=selection.descriptor, weighting=WeightingOptions(),
            basis="explicit_counts_divided_by_included_records" if reason is None else "empirical_assignments",
            denominator=total if total else None, denominator_basis=scope.denominator_basis, **reason_args)
        if reason is None:
            metric = replace(metric, input_basis="empirical_assignments",
                frequency_metadata=replace(metric.frequency_metadata, method="empirical_assignments; n_i/N"),
                count_metadata=replace(metric.count_metadata, method="count included record-state assignments"))
        expected = StateDistributionResult(metric, None,
            ValidationCoverage(total, len(rows), "selected_valid_records"), selection.selection_basis,
            selection.messages, tuple(exclusions))
        _handoff_equal(snapshot.distribution, expected, "snapshot distribution")
        reasons = metric.reason_codes
    descriptor = _descriptor_for(declaration)
    for actual, expected in (
        (snapshot.record_count, _count("record_count", len(rows), snapshot.scope)),
        (snapshot.representation_eligible_record_count, _count("representation_eligible_record_count",
            None if scope is None else len(scope.included_record_keys), snapshot.scope,
            representation=descriptor, reasons=reasons if scope is None else ())),
        (snapshot.representation_excluded_record_count, _count("representation_excluded_record_count",
            None if scope is None else len(scope.excluded_record_keys), snapshot.scope,
            representation=descriptor, reasons=reasons if scope is None else ())),
    ):
        _handoff_equal(actual, expected, "snapshot count")
    _handoff_equal(snapshot.family_statuses[0],
        _family("distribution", ExecutionStatus.PARTIAL if reasons else ExecutionStatus.COMPLETED, reasons),
        "snapshot distribution execution")
    return messages


def _handoff_provenance(validation, snapshot):
    """Validate source declarations, direct classes, coverage and owner metadata."""
    from .provenance import _checked_join, _composition, _direct, _metadata, _scalar
    from .bounds import _metric

    if not snapshot.record_count.value:
        return ()
    promoted = _promotions(validation)
    joined = join_provenance(validation.records, validation.provenance,
        dataset_versions=(snapshot.scope.dataset_version,), strict_mode=bool(promoted), strict_warning_codes=promoted)
    scope, entries, messages = _checked_join(joined, _provenance_scope(snapshot.scope))
    total, missing = len(entries), len(joined.missing_record_keys)
    coverages = (joined.provenance_row_coverage, joined.provenance_required_field_coverage,
                 joined.grounding_field_coverage)
    names = ("provenance_row_coverage", "provenance_required_field_coverage", "grounding_field_coverage")
    expected = ProvenanceCompositionResult(scope, _composition(entries, scope, "source_type"),
        _composition(entries, scope, "provenance_confidence"), _direct(entries, scope, messages), None,
        *coverages,
        tuple(_metadata(name, "PR-004", "F-008" if name == "provenance_row_coverage" else None,
                        "ratio", scope, "Reuse Phase 2 coverage; Definitions 3.10-3.12") for name in names),
        _scalar("analyzed_record_count", "PR-004", total, scope, "All selected valid records"),
        _scalar("records_with_matching_rows", "PR-004", total - missing, scope, "Phase 2 matched-row inventory"),
        _scalar("missing_provenance_count", "PR-004", missing, scope, "Phase 2 missing-row inventory"),
        _scalar("missing_provenance_share", "PR-004", missing / total, scope,
                "Definitions 11.4; missing rows / all selected valid records", unit="ratio", derived=True),
        joined.provenance_supplied,
        any(m.severity in (ValidationSeverity.ERROR, ValidationSeverity.FATAL) for m in messages),
        messages, tuple(joined.promoted_warning_codes))
    _handoff_equal(snapshot.provenance, expected, "snapshot provenance")
    grounding = expected.direct_grounding
    opened, closed, unresolved = (grounding.known_open_count.value, grounding.known_closed_count.value,
                                 grounding.unresolved_grounding_count.value)
    available = coverages[1].numerator > 0
    bounds = DirectClosureExposureBounds(scope, opened, closed, unresolved, total, scope.denominator_basis,
        *tuple(_metric("direct_closure_exposure_" + name, formula, value if available else None, scope,
                       method if available else "no usable required-provenance row")
            for name, formula, value, method in (
                ("lower_bound", "F-009", closed / total, "known_closed_count / total_record_count"),
                ("upper_bound", "F-010", (closed + unresolved) / total,
                 "(known_closed_count + unresolved_grounding_count) / total_record_count"),
                ("interval_width", None, unresolved / total,
                 "upper_bound - lower_bound = unresolved_grounding_count / total_record_count"))),
        provenance_row_coverage=coverages[0], provenance_required_field_coverage=coverages[1],
        grounding_field_coverage=coverages[2], confidence_field_coverage=expected.confidence.field_coverage,
        confidence_status=expected.confidence.status, confidence_counts=expected.confidence.counts,
        input_has_errors=expected.input_has_errors, validation_messages=messages)
    _handoff_equal(snapshot.direct_closure, bounds, "snapshot direct interval")
    return messages


def validate_longitudinal_snapshot(validation: BundleValidationResult, snapshot: SnapshotSummary) -> None:
    """Validate one complete input population, without requiring series chronology.

    This consumer checks literal assignments, supplied tables and scalar arithmetic.
    It invokes no representation assignment, metric coordinator or graph builder.
    Shared lineage derivation is validated once by the enclosing series consumer.
    """
    if type(validation) is not BundleValidationResult or type(snapshot) is not SnapshotSummary:
        raise _invalid("snapshot handoff requires typed validation and summary")
    replace(snapshot)
    replace(snapshot.scope)
    replace(snapshot.scope.declaration)
    rows = tuple(row for row in validation.records if row.record_key.dataset_version == snapshot.scope.dataset_version)
    keys = tuple(key for key, _, _ in _selected_records(rows, (snapshot.scope.dataset_version,)))
    scope = snapshot.scope.population_scope
    if (scope.included_record_keys != keys or scope.excluded_record_keys
            or scope.dataset_versions != (snapshot.scope.dataset_version,)
            or scope.denominator_basis != "selected_valid_records"
            or not rows and not snapshot.scope.declaration.empty_scope
            or rows and any(row.location.file_role not in (FileRole.RECORDS_PRIMARY, FileRole.RECORDS_COMPARE)
                            for row in rows)):
        raise _invalid("snapshot handoff must preserve its complete selected input population")
    messages = _handoff_distribution(validation, snapshot, rows) + _handoff_provenance(validation, snapshot)
    _handoff_equal(snapshot.family_statuses[3],
        _family("tail", ExecutionStatus.NOT_REQUESTED, ("R_LONGITUDINAL_FAMILY_NOT_REQUESTED",)),
        "snapshot tail execution")
    if snapshot.lineage is not None:
        replace(snapshot.lineage)
        replace(snapshot.lineage_closure)
        messages += snapshot.lineage.messages
    elif snapshot.family_statuses[-1].execution_status is ExecutionStatus.NOT_REQUESTED:
        _handoff_equal(snapshot.family_statuses[-1],
            _family("lineage", ExecutionStatus.NOT_REQUESTED, ("R_LONGITUDINAL_FAMILY_NOT_REQUESTED",)),
            "snapshot lineage execution")
    elif snapshot.family_statuses[-1].execution_status is not ExecutionStatus.NOT_REQUESTED:
        # Graph admission diagnostics are checked against actual loaded evidence
        # by the enclosing consumer. Independent snapshot validation preserves them.
        if any(message.code == ErrorCode.LINEAGE_RESOURCE_LIMIT_EXCEEDED.value for message in snapshot.messages):
            messages += (ValidationMessage(ErrorCode.LINEAGE_RESOURCE_LIMIT_EXCEEDED.value,
                ValidationSeverity.ERROR, "lineage computation exceeded an explicit resource limit",
                field="longitudinal_lineage"),)
    _handoff_equal(snapshot.messages, tuple(dict.fromkeys(messages)), "snapshot diagnostics")


def _handoff_comparison(pair, earlier, later, order):
    """Validate pair-local mapped tables, state sets and all five legacy scalars."""
    from ..representations.compatibility import validate_representation_compatibility
    from .diversity import _pair_metadata

    basis = pair.compatibility
    a = None if earlier.distribution is None else earlier.distribution.unweighted
    b = None if later.distribution is None else later.distribution.unweighted
    if basis is None:
        return None, None, a, b, (CalculationReason.REPRESENTATION_INCOMPATIBLE,), (
            ValidationMessage(ErrorCode.REPRESENTATION_INCOMPATIBLE.value, ValidationSeverity.ERROR,
                "pair declarations have no compatible comparison basis", field="longitudinal_pair"),)
    try:
        original_a, original_b = a, b
        available = a is not None and b is not None and a.status is b.status is CalculationStatus.AVAILABLE
        compatibility = None
        if available:
            compatibility = validate_representation_compatibility(
                ExplicitPairContext(a.scope, b.scope, a.representation, b.representation, order),
                earlier_state_semantics=basis.earlier_state_semantics,
                later_state_semantics=basis.later_state_semantics, state_mapping=pair.mapping)
        if pair.mapping is not None:
            forward = pair.mapping.direction == "earlier_to_later"
            source = a if forward else b
            if source is None:
                raise _invalid("mapping coverage requires its source representation", code=ErrorCode.REPRESENTATION_INCOMPATIBLE)
            source = _harmonize_distribution(source, pair.mapping)
            a, b = (source, b) if forward else (a, source)
        if not available:
            reasons = tuple(dict.fromkeys(_distribution_reasons(earlier) + _distribution_reasons(later)))
            return basis, None, a, b, reasons, ()
        left, right = set(a.support), set(b.support)
        specs = (
            ("support_delta", "F-005", "states", len(right) - len(left), "later support_size minus earlier support_size"),
            ("support_loss_count", None, "states", len(left - right), "cardinality of earlier support minus later support"),
            ("support_added_count", None, "states", len(right - left), "cardinality of later support minus earlier support"),
            ("support_retention_ratio", "F-006", "ratio", len(left & right) / len(left),
             "intersection support size / earlier positive-mass support size"),
            ("gini_simpson_diversity_delta", "F-018", "dimensionless",
             b.gini_simpson_diversity.value - a.gini_simpson_diversity.value,
             "later Gini-Simpson diversity minus earlier diversity"))
        scalars = tuple(ScalarCalculation(_pair_metadata(name, formula, unit, compatibility, a.weighting, method),
                                         CalculationStatus.AVAILABLE, value)
                        for name, formula, unit, value, method in specs)
        sets = tuple(_pair_metadata(name, None, "set_of_states", compatibility, a.weighting, method)
                     for name, method in (("extinct_states", "earlier support minus later support"),
                                          ("added_states", "later support minus earlier support"),
                                          ("retained_states", "earlier support intersect later support")))
        expected = SupportComparison(compatibility, original_a, original_b, a, b, CalculationStatus.AVAILABLE, (),
            *scalars, tuple(sorted(left - right)), tuple(sorted(right - left)), tuple(sorted(left & right)),
            len(left), "earlier_positive_mass_support_in_harmonized_representation", sets,
            (("earlier", original_a.support_size.value, a.support_size.value),
             ("later", original_b.support_size.value, b.support_size.value)))
        return basis, expected, a, b, (), ()
    except CanonicalValidationError as error:
        return None, None, None, None, (CalculationReason.REPRESENTATION_INCOMPATIBLE,), (
            _message(error, "longitudinal_pair"),)


def _handoff_tail(options, basis, comparison, earlier, later, a, reasons):
    from .tail import RarityEntry, _invalid as invalid_tail, _metadata

    tail, messages = None, ()
    if not reasons:
        ranked = sorted(a.states, key=lambda row: (row.state_frequency, row.state_count, row.state_id))
        if options.rule == "state_list" and set(options.state_ids) - set(a.support):
            reasons = (CalculationReason.UNSUPPORTED_OPTION,)
            messages = (_message(invalid_tail("tail state list contains an absent or zero-count state"),
                                 "longitudinal_tail"),)
        else:
            selected = {row.state_id for row in ranked
                if (options.rule == "singleton_count" and row.state_count == 1
                    or options.rule == "count_at_or_below" and row.state_count <= options.count_threshold
                    or options.rule == "frequency_at_or_below" and row.state_frequency <= options.frequency_threshold
                    or options.rule == "state_list" and row.state_id in options.state_ids)}
            scope, representation = a.scope, a.representation
            method = "Definitions 10.1-10.6; explicit " + options.rule
            total = len(scope.included_record_keys)
            tail = TailSelectionResult(scope, representation, options, a.input_basis, a.status, a.reason_codes,
                total, scope.denominator_basis, tuple(sorted(selected)),
                tuple(RarityEntry(row.state_id, row.state_count, row.state_frequency, index, row.state_id in selected)
                      for index, row in enumerate(ranked, 1)),
                ScalarCalculation(_metadata("tail_support_size", "states", scope, representation, method),
                                  CalculationStatus.AVAILABLE, len(selected)),
                ScalarCalculation(_metadata("tail_record_share", "ratio", scope, representation,
                    method + "; selected counts / included records"), CalculationStatus.AVAILABLE,
                    sum(row.state_count for row in ranked if row.state_id in selected) / total),
                _metadata("rarity_rank", "ordinal_rank", scope, representation,
                          "ascending frequency, then count, then Unicode state ID; 1-based ordinal"),
                _metadata("tail_membership", "set_of_states", scope, representation, method),
                a.count_metadata, a.frequency_metadata)
    lost = None if reasons else tuple(sorted(set(tail.tail_membership) & set(comparison.extinct_states)))
    return TailDisappearanceResult(options,
        earlier.scope.representation_scope or earlier.scope.population_scope,
        later.scope.representation_scope or later.scope.population_scope,
        None if basis is None else basis.harmonized_representation, tail,
        None if a is None else a.frequency_denominator,
        CalculationStatus.UNAVAILABLE if reasons else CalculationStatus.AVAILABLE,
        reasons, None if lost is None else len(lost), lost), messages


def _validate_longitudinal_pair(result, earlier, later, order, options, lineage):
    pair = result.pair
    basis, comparison, a, b, reasons, messages = _handoff_comparison(pair, earlier, later, order)
    _handoff_equal(result.support_comparison, comparison, "scheduled support comparison")
    deltas = tuple(_delta(name, earlier, later, basis, a, b, reasons, comparison=comparison)
                   for name in _DISTRIBUTION_DELTAS)
    deltas += tuple(_evidence_delta(name, earlier, later, basis) for name in (*_PROVENANCE_DELTAS, *_DIRECT_DELTAS))
    shares = {category: _evidence_delta("source_type_share_deltas", earlier, later, basis, category=category)
              for category in _SOURCE_CATEGORIES}
    messages += _pair_provenance_errors(earlier, later)
    provenance_family, direct_family = _pair_evidence_families(deltas, shares, messages)
    distribution_status = (ExecutionStatus.COMPLETED if comparison is not None else
                           ExecutionStatus.PARTIAL if basis is not None else ExecutionStatus.FAILED)
    tail, tail_family = None, None
    if options is not None:
        tail, tail_messages = _handoff_tail(options, basis, comparison, earlier, later, a, reasons)
        messages += tail_messages
        tail_family = _family("tail", ExecutionStatus.COMPLETED if tail.status is CalculationStatus.AVAILABLE
                              else ExecutionStatus.FAILED, tail.reason_codes)
    families = _families(_family("distribution", distribution_status, reasons), provenance_family, direct_family, tail_family)
    lineage_deltas = ()
    if lineage:
        lineage_deltas = tuple(_lineage_delta(name, earlier, later, basis) for name in _LINEAGE_DELTA_METADATA)
        families = (*families[:-1], _lineage_pair_family(lineage_deltas, earlier, later))
    expected = LongitudinalPairResult(pair, basis, comparison, deltas, tail, families, shares, messages, lineage_deltas)
    _handoff_equal(result, expected, "scheduled pair")


def validate_longitudinal_result(validation: BundleValidationResult, *, result: LongitudinalResult) -> None:
    """Validate a supplied series handoff against current input and arithmetic.

    Binding alone cannot certify caller-created aggregates. This checks complete
    membership, assignments, declared evidence, owner metadata, pair arithmetic
    and requested shared lineage evidence. No analysis entry point, representation
    assignment, tail selector, graph builder or cycle analyzer is invoked.
    """
    if type(result) is not LongitudinalResult:
        raise _invalid("longitudinal handoff requires its typed result")
    validate_longitudinal_selection(validation, result.selection)
    replace(result)
    snapshots = {}
    for ordinal, snapshot in enumerate(result.snapshots, 1):
        validate_longitudinal_snapshot(validation, snapshot)
        scope = snapshot.scope.representation_scope
        if scope is not None and scope.scope_id != f"longitudinal-representation-{ordinal:04d}":
            raise _invalid("representation scope reference disagrees with selected chronology")
        snapshots[snapshot.scope.dataset_version] = snapshot
    if result.lineage_requested:
        from ..lineage.ancestry import validate_selected_lineage_result, _selected_lineage_signature
        if result.lineage_input_signature != _selected_lineage_signature(validation, result.selection, result.lineage_limits):
            raise _invalid("requested lineage binding disagrees with its input")
        if result.shared_lineage is not None:
            validate_selected_lineage_result(validation, selection=result.selection, result=result.shared_lineage)
        else:
            from ..lineage.ancestry import validate_lineage_graph_exhaustion
            validate_lineage_graph_exhaustion(validation, usage=result.lineage_resource_usage)
            failure = _message(LineageResourceLimitError(result.lineage_resource_usage), "longitudinal_lineage")
            family = _family("lineage", ExecutionStatus.FAILED, ("LINEAGE_RESOURCE_LIMIT_EXCEEDED",))
            for snapshot in result.snapshots:
                if failure not in snapshot.messages or snapshot.family_statuses[-1] != family:
                    raise _invalid("graph admission failure must retain its exact status and diagnostic")
    for pair in result.comparisons:
        _validate_longitudinal_pair(pair, snapshots[pair.pair.earlier_version], snapshots[pair.pair.later_version],
                                  result.selection.version_order, result.tail_options, result.lineage_requested)
    messages = tuple(dict.fromkeys(message for item in (*result.snapshots, *result.comparisons)
                                  for message in item.messages))
    _handoff_equal(result.messages, messages, "series diagnostics")


@dataclass(frozen=True, slots=True)
class LongitudinalFailureResult:
    """Rejected selection with independent evidence and no inferred chronology."""

    declarations: tuple[SnapshotDeclaration, ...]
    mappings: tuple[LongitudinalMapping, ...]
    snapshots: tuple[SnapshotSummary, ...]
    context_versions: tuple[str, ...]
    selected_version_count: int
    baseline: str
    max_versions: int
    lineage_requested: bool
    tail_options: TailSelectionOptions | None
    messages: tuple[ValidationMessage, ...]
    reason_codes: tuple[str, ...]
    input_signature: str = field(repr=False)
    selection_errors: tuple[ValidationMessage, ...] = ()

    def __post_init__(self):
        _baseline(self.baseline)
        _limit(self.max_versions)
        if (type(self.declarations) is not tuple
                or any(type(d) is not SnapshotDeclaration for d in self.declarations)
                or type(self.mappings) is not tuple
                or any(type(m) is not LongitudinalMapping for m in self.mappings)
                or type(self.snapshots) is not tuple
                or any(type(s) is not SnapshotSummary for s in self.snapshots)
                or type(self.context_versions) is not tuple
                or any(type(v) is not str for v in self.context_versions)
                or type(self.selected_version_count) is not int
                or self.selected_version_count != len(self.declarations)
                or type(self.lineage_requested) is not bool
                or type(self.messages) is not tuple or not self.messages
                or any(type(m) is not ValidationMessage for m in self.messages)
                or type(self.reason_codes) is not tuple or not self.reason_codes
                or type(self.selection_errors) is not tuple
                or any(type(m) is not ValidationMessage for m in self.selection_errors)
                or type(self.input_signature) is not str or not self.input_signature):
            raise _invalid("failed series requires a complete immutable request and evidence")
        if self.tail_options is not None:
            _tail_options(self.tail_options)
        if any(s.lineage is not None or s.lineage_closure is not None for s in self.snapshots):
            raise _invalid("failed selection cannot claim selected lineage work")

    @property
    def execution_status(self):
        return ExecutionStatus.FAILED


def _retained_selection_errors(validation, errors):
    """Bind prior CLI rejection to retained validation and physical input evidence."""
    if type(errors) is not tuple or any(type(item) is not ValidationMessage for item in errors):
        raise _invalid("selection errors must be immutable validation evidence")
    if len(set(errors)) != len(errors):
        raise _invalid("selection errors cannot repeat")
    for item in errors:
        if (item.severity is not ValidationSeverity.ERROR or item not in validation.validation_messages
                or type(item.message) is not str or not item.message
                or item.record_key is not None or item.row_number is not None or item.line_number is not None):
            raise _invalid("selection rejection must already be retained by input validation")
        if item.code == ErrorCode.VERSION_ORDER_CONFLICT.value:
            if (item.file_role is not FileRole.VERSION_ORDER or item.field not in
                    ("version_order", "version_rank", "version_timestamps", "timestamp_tiebreak",
                     "invocation_order", "loaded_versions")):
                raise _invalid("retained chronology rejection has an invalid source")
        elif item.code == ErrorCode.SCHEMA_TYPE.value:
            entries = tuple(entry for entry in validation.inventory
                if entry.role is item.file_role and str(entry.path) == item.file_path)
            if (item.file_role not in (FileRole.RECORDS_PRIMARY, FileRole.RECORDS_COMPARE)
                    or item.field != "dataset_version" or len(entries) != 1):
                raise _invalid("file selection rejection must identify one loaded selected input")
            versions = {row.record_key.dataset_version for row in validation.records
                if row.location.file_role is item.file_role and row.location.file_path == item.file_path}
            if len(versions) == 1:
                raise _invalid("a valid selected file cannot claim a version-count rejection")
        else:
            raise _invalid("unsupported retained selection rejection")
    return errors


def _failed_request(validation, declarations, mappings, baseline, max_versions, lineage, tail_options,
                    selection_errors=()):
    _baseline(baseline)
    _limit(max_versions)
    if (type(lineage) is not bool or type(declarations) is not tuple
            or any(type(d) is not SnapshotDeclaration for d in declarations)
            or type(mappings) is not tuple or any(type(m) is not LongitudinalMapping for m in mappings)):
        raise _invalid("failed selection requires typed declarations and explicit request options")
    options = None if tail_options is None else _tail_options(tail_options)
    retained = _retained_selection_errors(validation, selection_errors)
    try:
        select_longitudinal_versions(validation, declarations=declarations, mappings=mappings,
                                     baseline=baseline, max_versions=max_versions)
    except CanonicalValidationError as error:
        failure = _message(error, "longitudinal_selection")
    else:
        if not retained:
            raise _invalid("valid selection cannot be supplied as a failed series")
        failure = None
    failures = tuple(dict.fromkeys((*retained, *((failure,) if failure is not None else ()))))
    rows, populations, selected, context, _, joined = _populations(validation)
    resource_failure = any(item.code == ErrorCode.LONGITUDINAL_RESOURCE_LIMIT_EXCEEDED.value
                           for item in failures)
    reasons = tuple(dict.fromkeys(("R_LONGITUDINAL_RESOURCE_LIMIT" if resource_failure else
        "R_LONGITUDINAL_SELECTION_INVALID", *(item.code for item in failures))))
    scopes = []
    if not resource_failure:
        seen = set()
        for declaration in declarations:
            version = declaration.dataset_version
            if version in seen:
                continue
            seen.add(version)
            if version in context or declaration.empty_scope != (version not in populations):
                continue
            if version not in selected and not declaration.empty_scope:
                continue
            scopes.append(SnapshotScope(version,
                CalculationScope((version,), tuple(populations.get(version, ())), (),
                    "selected_valid_records", f"longitudinal-population-{len(scopes) + 1:04d}"),
                None, declaration))
    binding = _binding(rows, joined, validation.version_order, declarations, (),
                       baseline, max_versions, validation.content_mode)
    signature = sha256_canonical((binding, tuple((m.earlier_version, m.later_version,
        _plain(m.declaration)) for m in mappings), lineage,
        None if options is None else {f.name: _plain(getattr(options, f.name)) for f in fields(options)},
        reasons, tuple((item.code, item.severity.value, item.message,
            item.file_role.value, item.file_path, item.field) for item in retained),
        tuple((entry.role.value, str(entry.path), entry.sha256, entry.size_bytes, entry.row_count)
              for entry in validation.inventory) if retained else ()))
    return tuple(scopes), context, failures, reasons, signature, options


def analyze_longitudinal_failure(
    validation: BundleValidationResult, *, declarations: tuple[SnapshotDeclaration, ...],
    baseline: str = "none", max_versions: int = 100,
    mappings: tuple[LongitudinalMapping, ...] = (), lineage: bool = False,
    tail_options: TailSelectionOptions | None = None,
    selection_errors: tuple[ValidationMessage, ...] = (),
) -> LongitudinalFailureResult:
    """Retain independent evidence after a confirmed selection rejection.

    This calculation entry point is separate from report assembly. Declaration
    order identifies rows only. Admission failures perform no snapshot work;
    no failure path invents chronology, compares endpoints, or runs lineage.
    """
    scopes, context, failures, reasons, signature, options = _failed_request(
        validation, declarations, mappings, baseline, max_versions, lineage, tail_options, selection_errors)
    grouped = {scope.dataset_version: [] for scope in scopes}
    for row in validation.records:
        if row.record_key.dataset_version in grouped:
            grouped[row.record_key.dataset_version].append(row)
    snapshots = tuple(_snapshot_distribution(scope, tuple(grouped[scope.dataset_version]), index, validation)
                      for index, scope in enumerate(scopes, 1))
    if lineage:
        snapshots = tuple(replace(snapshot, family_statuses=(*snapshot.family_statuses[:-1],
            _family("lineage", ExecutionStatus.FAILED, reasons))) for snapshot in snapshots)
    messages = tuple(dict.fromkeys((*failures, *(m for s in snapshots for m in s.messages))))
    return LongitudinalFailureResult(declarations, mappings, snapshots, context, len(declarations),
        baseline, max_versions, lineage, options, messages, reasons, signature, selection_errors)


def validate_longitudinal_failure(validation: BundleValidationResult, *, result: LongitudinalFailureResult):
    """Check a failed request and its independent handoffs without calculations."""
    if type(result) is not LongitudinalFailureResult:
        raise _invalid("consumer requires a typed failed series")
    replace(result)
    scopes, context, failures, reasons, signature, options = _failed_request(validation,
        result.declarations, result.mappings, result.baseline, result.max_versions,
        result.lineage_requested, result.tail_options, result.selection_errors)
    if (len(scopes) != len(result.snapshots) or result.context_versions != context
            or result.reason_codes != reasons or result.input_signature != signature
            or result.tail_options != options
            or result.messages != tuple(dict.fromkeys((*failures,
                *(m for s in result.snapshots for m in s.messages))))):
        raise _invalid("failed series evidence differs from the current request or input")
    for scope, snapshot in zip(scopes, result.snapshots):
        if (snapshot.scope.population_scope != scope.population_scope
                or snapshot.scope.declaration != scope.declaration):
            raise _invalid("failed series snapshot differs from its complete declaration")
        validate_longitudinal_snapshot(validation, snapshot)
        expected = (_family("lineage", ExecutionStatus.FAILED, reasons) if result.lineage_requested else
                    _family("lineage", ExecutionStatus.NOT_REQUESTED, ("R_LONGITUDINAL_FAMILY_NOT_REQUESTED",)))
        if snapshot.family_statuses[-1] != expected:
            raise _invalid("failed series lineage must retain its selection failure")
    return result
