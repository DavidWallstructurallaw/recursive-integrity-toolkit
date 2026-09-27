"""Select explicit snapshot populations and declaration-compatible pairs.

Owner IDs:
    PR-007, PR-011, T1; P6A-D01 through P6A-D03 and P6A-D08.

Inputs:
    Retained BundleValidationResult, explicit snapshot declarations, pair-local
    mappings, baseline policy and a selected-version admission limit.

Outputs:
    Immutable complete population scopes, validated chronology, deterministic
    pair schedule, declaration-only compatibility and a private input binding.

Assumptions:
    Primary/comparison roles select records; context and chronology-only entries
    cannot silently acquire snapshot membership. Meanings remain declarations.

Limits:
    No I/O, assignment, distributions, deltas, tail, graph, simulation, report or
    CLI dispatch. Map totality on actual states belongs to consuming kernels.

Current phase status:
    Phase 6A Step 2 selection and compatibility only. Import-safe.
"""
from __future__ import annotations

from dataclasses import dataclass, field, fields, replace
from types import MappingProxyType

from ..config import RepresentationConfig
from ..errors import CanonicalValidationError, ErrorCode
from ..io.validation import join_provenance, resolve_version_order
from ..models import (
    BundleValidationResult, CalculationReason, CalculationScope, CalculationStatus,
    CanonicalRow, FileRole, RecordKey, RepresentationDescriptor, VersionOrderResult,
)
from ..representations.base import _literal_text, _selected_records
from ..representations.compatibility import (
    RepresentationBasisCompatibility, StateMappingDeclaration, validate_representation_basis,
)
from ..representations.content_hash import select_content_representation
from ..representations.field import select_field_representation
from ..utils.hashing import sha256_canonical


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


def _binding(rows, joined, order, declarations, pairs, baseline, max_versions):
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
            _plain(declarations), pair_declarations, baseline, max_versions))
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
        _binding(rows, joined, checked, declarations, pairs, baseline, max_versions), baseline)


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
