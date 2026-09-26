"""Build a bounded immutable parent graph from retained input validation.

Owner IDs: PR-008; Phase 5 Step 2. The shared input resolver owns reference
identity and chronology. This module selects an explicit target population and
admits accepted edges. No cycle/ancestry traversal, metrics, file or network I/O.
Raw record content, provenance URI fields and locations never enter graph results.
Reference spellings remain identity evidence, including duplicate aliases.

Current phase status:
    Phase 5 Step 2 parent graph construction. General cycle and ancestry
    analysis remain deferred to the following implementation steps.
"""
from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

from ..errors import CanonicalValidationError, ErrorCode, LineageResourceLimitError, WarningCode
from ..models import (
    BundleValidationResult, CanonicalRow, FileRole, ParentBatchValidationResult,
    ParentRecordValidation, ParentReference, ParentResolutionStatus,
    ParentValidationResult, RecordKey, RowLocation, ValidationMessage, ValidationSeverity,
)


def _invalid(message: str, code: ErrorCode = ErrorCode.SCHEMA_TYPE) -> CanonicalValidationError:
    return CanonicalValidationError(code, message)


def _integer(value: object, *, positive: bool = False) -> None:
    if type(value) is not int or value < (1 if positive else 0):
        raise _invalid("lineage counts and limits require exact integers in range")


def _key(value: object) -> RecordKey:
    if type(value) is not RecordKey:
        raise _invalid("lineage identities require canonical record keys")
    try:
        return RecordKey(value.dataset_version, value.record_id)
    except (TypeError, ValueError):
        raise _invalid("lineage identity violates the canonical contract") from None


def _keys(value: object) -> tuple[RecordKey, ...]:
    if type(value) is not tuple:
        raise _invalid("lineage identity collections require immutable tuples")
    checked = tuple(_key(item) for item in value)
    if checked != tuple(sorted(set(checked))):
        raise _invalid("lineage identities must be unique and canonically ordered")
    return checked


def _version(value: object) -> str:
    try:
        return RecordKey(value, "lineage-scope").dataset_version
    except (TypeError, ValueError):
        raise _invalid("lineage target requires a valid explicit version", ErrorCode.CONFIG_INVALID) from None


@dataclass(frozen=True, slots=True)
class LineageLimits:
    """Positive work limits, independent of loader limits and performance goals."""
    max_nodes: int = 200000
    max_edges: int = 1000000
    max_root_memberships: int = 1000000
    max_root_union_visits: int = 10000000

    def __post_init__(self) -> None:
        for value in (self.max_nodes, self.max_edges, self.max_root_memberships, self.max_root_union_visits):
            _integer(value, positive=True)


def _limits(value: object) -> LineageLimits:
    if type(value) is not LineageLimits:
        raise _invalid("lineage limits require LineageLimits", ErrorCode.CONFIG_INVALID)
    return LineageLimits(value.max_nodes, value.max_edges, value.max_root_memberships, value.max_root_union_visits)


@dataclass(frozen=True, slots=True)
class LineageResourceUsage:
    """Exact admitted work and the next rejected work unit, when exhausted."""
    admitted_node_count: int
    admitted_edge_count: int
    stored_root_membership_count: int
    root_union_visit_count: int
    limits: LineageLimits
    exhausted_limit: str | None = None
    attempted_value: int | None = None

    def __post_init__(self) -> None:
        bounded = _limits(self.limits)
        pairs = (
            ("max_nodes", self.admitted_node_count, bounded.max_nodes),
            ("max_edges", self.admitted_edge_count, bounded.max_edges),
            ("max_root_memberships", self.stored_root_membership_count, bounded.max_root_memberships),
            ("max_root_union_visits", self.root_union_visit_count, bounded.max_root_union_visits),
        )
        for _, count, maximum in pairs:
            _integer(count)
            if count > maximum:
                raise _invalid("lineage usage exceeds its admitted limit")
        if self.exhausted_limit is None:
            if self.attempted_value is not None:
                raise _invalid("completed lineage work cannot have a rejected attempt")
        else:
            limits_by_name = {name: (count, maximum) for name, count, maximum in pairs}
            if type(self.exhausted_limit) is not str or self.exhausted_limit not in limits_by_name:
                raise _invalid("lineage exhaustion names an unsupported limit")
            _integer(self.attempted_value, positive=True)
            count, maximum = limits_by_name[self.exhausted_limit]
            if count != maximum or self.attempted_value != maximum + 1:
                raise _invalid("lineage exhaustion must identify its next rejected admission")
        object.__setattr__(self, "limits", bounded)


@dataclass(frozen=True, slots=True)
class LineageScope:
    """Target records determine population size; all other nodes are context."""
    target_dataset_version: str | None
    target_record_keys: tuple[RecordKey, ...]
    target_record_count: int
    loaded_record_count: int
    context_record_count: int
    loaded_dataset_versions: tuple[str, ...]

    def __post_init__(self) -> None:
        keys = _keys(self.target_record_keys)
        for value in (self.target_record_count, self.loaded_record_count, self.context_record_count):
            _integer(value)
        if self.target_record_count != len(keys) or self.loaded_record_count != len(keys) + self.context_record_count:
            raise _invalid("lineage scope counts do not match their explicit population")
        if self.target_dataset_version is None:
            if keys:
                raise _invalid("a populated lineage target requires an explicit version", ErrorCode.CONFIG_INVALID)
        else:
            _version(self.target_dataset_version)
            if any(key.dataset_version != self.target_dataset_version for key in keys):
                raise _invalid("lineage target keys do not match their selected version")
        if type(self.loaded_dataset_versions) is not tuple:
            raise _invalid("lineage version inventory requires an immutable tuple")
        versions = tuple(_version(value) for value in self.loaded_dataset_versions)
        if versions != tuple(sorted(set(versions))):
            raise _invalid("lineage version inventory must be unique and lexical")
        if bool(versions) != bool(self.loaded_record_count) or set(key.dataset_version for key in keys) - set(versions):
            raise _invalid("lineage version inventory disagrees with its scope")


_DIAGNOSTIC_CODES = frozenset(code.value for code in ErrorCode) | frozenset(code.value for code in WarningCode)


def _safe_message(value: object) -> ValidationMessage:
    if (type(value) is not ValidationMessage or type(value.code) is not str
            or value.code not in _DIAGNOSTIC_CODES or type(value.severity) is not ValidationSeverity):
        raise _invalid("lineage diagnostics require known typed validation codes")
    key = None if value.record_key is None else _key(value.record_key)
    return ValidationMessage(value.code, value.severity,
                             "Validation evidence reported this diagnostic.", record_key=key)


def _messages(values: object) -> tuple[ValidationMessage, ...]:
    if type(values) is not tuple:
        raise _invalid("lineage diagnostics require an immutable tuple")
    messages = {_safe_message(value) for value in values}
    return tuple(sorted(messages, key=lambda item: (
        "" if item.record_key is None else item.record_key.dataset_version,
        "" if item.record_key is None else item.record_key.record_id, item.code, item.severity.value)))


def _safe_evidence(value: object, child: RecordKey) -> ParentRecordValidation:
    if type(value) is not ParentRecordValidation or _key(value.child_key) != child:
        raise _invalid("lineage parent evidence must match its record")
    if type(value.provenance_available) is not bool:
        raise _invalid("lineage provenance availability requires an explicit boolean")
    if value.declared_reference_count is not None:
        _integer(value.declared_reference_count)
    _integer(value.resolved_reference_count)
    _integer(value.invalid_self_reference_count)
    if (value.declared_reference_count is not None
            and value.resolved_reference_count + value.invalid_self_reference_count > value.declared_reference_count):
        raise _invalid("lineage reference counts exceed their declarations")
    result = value.result
    if result is not None:
        if (type(result) is not ParentValidationResult or _key(result.child_key) != child
                or result.declaration_state not in ("absent", "null", "empty", "declared")
                or type(result.references) is not tuple or type(result.graph_validation_deferred) is not bool):
            raise _invalid("lineage requires typed parent declaration evidence")
        refs = []
        for ref in result.references:
            if (type(ref) is not ParentReference or type(ref.source_references) is not tuple
                    or not ref.source_references or any(type(text) is not str for text in ref.source_references)
                    or type(ref.resolution_status) is not ParentResolutionStatus
                    or ref.temporal_status not in ("same_version", "earlier_version", "unavailable")):
                raise _invalid("lineage reference evidence is invalid")
            parent = None if ref.parent_key is None else _key(ref.parent_key)
            if ref.canonical_reference != (None if parent is None else str(parent)):
                raise _invalid("lineage reference identity disagrees with its canonical spelling")
            for text in ref.source_references:
                try:
                    RecordKey.parse(text) if "::" in text else RecordKey(child.dataset_version, text)
                except (TypeError, ValueError):
                    raise _invalid("lineage evidence contains an invalid reference spelling") from None
            refs.append(ParentReference(tuple(ref.source_references), ref.canonical_reference,
                                        parent, ref.resolution_status, ref.temporal_status))
        resolved = sum(len(ref.source_references) for ref in refs
                       if ref.resolution_status is ParentResolutionStatus.RESOLVED)
        represented = sum(len(ref.source_references) for ref in refs) + value.invalid_self_reference_count
        if (resolved != value.resolved_reference_count or value.declared_reference_count is None
                or represented > value.declared_reference_count
                or (result.declaration_state != "declared" and value.declared_reference_count != 0)):
            raise _invalid("lineage reference evidence disagrees with its declared counts")
        result = ParentValidationResult(child, result.declaration_state, tuple(refs),
                                        result.graph_validation_deferred, _messages(result.messages))
    elif value.declared_reference_count is not None or value.resolved_reference_count or value.invalid_self_reference_count:
        raise _invalid("missing parent result requires unknown declaration cardinality")
    return ParentRecordValidation(child, value.provenance_available, result,
                                  value.declared_reference_count, value.resolved_reference_count,
                                  value.invalid_self_reference_count, _messages(value.messages))


def _accepted_parents(evidence: ParentRecordValidation) -> tuple[RecordKey, ...]:
    if evidence.result is None:
        return ()
    return tuple(sorted({ref.parent_key for ref in evidence.result.references
                         if ref.resolution_status is ParentResolutionStatus.RESOLVED
                         and ref.temporal_status in ("same_version", "earlier_version")
                         and ref.parent_key is not None and ref.parent_key != evidence.child_key}))


@dataclass(frozen=True, slots=True)
class LineageGraph:
    """Accepted edges and rejected-reference evidence, without an acyclic claim.

    Both adjacency mappings include isolated nodes. All nested containers are
    detached immutable values; raw source locations are removed from diagnostics.
    """
    scope: LineageScope
    node_keys: tuple[RecordKey, ...]
    parents_by_child: Mapping[RecordKey, tuple[RecordKey, ...]]
    children_by_parent: Mapping[RecordKey, tuple[RecordKey, ...]]
    parent_evidence_by_record: Mapping[RecordKey, ParentRecordValidation]
    self_parent_record_keys: tuple[RecordKey, ...]
    messages: tuple[ValidationMessage, ...]
    resource_usage: LineageResourceUsage

    def __post_init__(self) -> None:
        nodes = _keys(self.node_keys)
        if type(self.scope) is not LineageScope:
            raise _invalid("lineage graph requires an explicit typed scope")
        scope = LineageScope(self.scope.target_dataset_version, self.scope.target_record_keys,
                             self.scope.target_record_count, self.scope.loaded_record_count,
                             self.scope.context_record_count, self.scope.loaded_dataset_versions)
        node_set = set(nodes)
        if (scope.loaded_record_count != len(nodes)
                or scope.target_record_keys != tuple(key for key in nodes if key.dataset_version == scope.target_dataset_version)
                or scope.loaded_dataset_versions != tuple(sorted({key.dataset_version for key in nodes}))):
            raise _invalid("lineage graph nodes disagree with its scope")
        mappings = (self.parents_by_child, self.children_by_parent, self.parent_evidence_by_record)
        if any(type(value) not in (dict, MappingProxyType) or set(value) != node_set for value in mappings):
            raise _invalid("lineage mappings must cover exactly the loaded nodes")
        evidence = {key: _safe_evidence(self.parent_evidence_by_record[key], key) for key in nodes}
        parents, children = {}, {key: [] for key in nodes}
        for child in nodes:
            adjacent = _keys(self.parents_by_child[child])
            if set(adjacent) - node_set or adjacent != _accepted_parents(evidence[child]):
                raise _invalid("lineage adjacency disagrees with accepted reference evidence")
            parents[child] = adjacent
            for parent in adjacent:
                children[parent].append(child)
        for parent in nodes:
            if _keys(self.children_by_parent[parent]) != tuple(children[parent]):
                raise _invalid("lineage forward and reverse adjacency disagree")
        self_keys = _keys(self.self_parent_record_keys)
        if self_keys != tuple(key for key in nodes if evidence[key].invalid_self_reference_count):
            raise _invalid("lineage self-reference diagnostics disagree with retained evidence")
        usage = self.resource_usage
        if type(usage) is not LineageResourceUsage:
            raise _invalid("lineage graph requires typed resource usage")
        usage = LineageResourceUsage(usage.admitted_node_count, usage.admitted_edge_count,
                    usage.stored_root_membership_count, usage.root_union_visit_count,
                    usage.limits, usage.exhausted_limit, usage.attempted_value)
        if (usage.admitted_node_count != len(nodes) or usage.admitted_edge_count != sum(map(len, parents.values()))
                or usage.stored_root_membership_count or usage.root_union_visit_count or usage.exhausted_limit is not None):
            raise _invalid("completed parent graph has inconsistent resource usage")
        object.__setattr__(self, "scope", scope)
        object.__setattr__(self, "node_keys", nodes)
        object.__setattr__(self, "parents_by_child", MappingProxyType(parents))
        object.__setattr__(self, "children_by_parent", MappingProxyType({key: tuple(values) for key, values in children.items()}))
        object.__setattr__(self, "parent_evidence_by_record", MappingProxyType(evidence))
        object.__setattr__(self, "messages", _messages(self.messages))
        object.__setattr__(self, "resource_usage", usage)


def build_lineage_graph(
    validation: BundleValidationResult, *, target_dataset_version: str | None,
    limits: LineageLimits = LineageLimits(),
) -> LineageGraph:
    """Revalidate the shared batch once, then admit bounded deduplicated edges.

    Older handoffs without retained ``parent_validation`` must be rebuilt through
    ``validate_bundle``. Rechecking uses one identity lookup for the entire batch,
    avoiding a per-record rebuild. Reference count evidence includes original
    aliases; accepted graph edges additionally require known chronology.
    """
    from ..io.validation import resolve_parent_batch

    bounded = _limits(limits)
    if type(validation) is not BundleValidationResult or type(validation.records) is not tuple:
        raise _invalid("lineage graph requires a typed bundle validation result")
    if len(validation.records) > bounded.max_nodes:
        raise LineageResourceLimitError(LineageResourceUsage(bounded.max_nodes, 0, 0, 0,
                                        bounded, "max_nodes", bounded.max_nodes + 1))
    keys, primary_versions, roles_by_version = [], set(), {}
    for row in validation.records:
        if type(row) is not CanonicalRow or row.kind != "records":
            raise _invalid("lineage graph requires canonical record rows")
        key = _key(row.record_key)
        if (type(row.values) not in (dict, MappingProxyType)
                or row.values.get("dataset_version") != key.dataset_version
                or row.values.get("record_id") != key.record_id):
            raise _invalid("lineage record identity disagrees with its retained values")
        if type(row.location) is not RowLocation or (row.location.file_role is not None and
                (type(row.location.file_role) is not FileRole or row.location.file_role not in
                 (FileRole.RECORDS_PRIMARY, FileRole.RECORDS_COMPARE, FileRole.LINEAGE_CONTEXT))):
            raise _invalid("lineage records have an unsupported input role")
        role = row.location.file_role
        roles_by_version.setdefault(key.dataset_version, set()).add(role)
        if role is FileRole.RECORDS_PRIMARY:
            primary_versions.add(key.dataset_version)
        keys.append(key)
    nodes = tuple(sorted(keys))
    if len(set(nodes)) != len(nodes):
        raise _invalid("duplicate canonical record identity in lineage input", ErrorCode.RECORD_DUPLICATE_ID)
    if len(primary_versions) > 1 or any(
            FileRole.RECORDS_PRIMARY in roles and FileRole.RECORDS_COMPARE in roles
            or FileRole.LINEAGE_CONTEXT in roles and bool(
                roles & {FileRole.RECORDS_PRIMARY, FileRole.RECORDS_COMPARE})
            for roles in roles_by_version.values()):
        raise _invalid("lineage primary and context version roles must be disjoint", ErrorCode.CONFIG_INVALID)
    if target_dataset_version is None:
        if primary_versions or (nodes and all(roles == {None} for roles in roles_by_version.values())):
            raise _invalid("loaded primary records require an explicit target version", ErrorCode.CONFIG_INVALID)
    else:
        _version(target_dataset_version)
        if primary_versions and target_dataset_version not in primary_versions:
            raise _invalid("lineage target must select the primary version", ErrorCode.CONFIG_INVALID)
        if not primary_versions and roles_by_version.get(target_dataset_version, set()) & {
                FileRole.RECORDS_COMPARE, FileRole.LINEAGE_CONTEXT}:
            raise _invalid("lineage context records cannot define the primary target", ErrorCode.CONFIG_INVALID)
    retained = validation.parent_validation
    if type(retained) is not ParentBatchValidationResult:
        raise _invalid("lineage needs retained parent validation; call validate_bundle again")
    promoted = retained.promoted_warning_codes
    if type(promoted) is not tuple:
        raise _invalid("lineage warning promotion evidence is invalid")
    rebuilt = resolve_parent_batch(nodes, validation.provenance, version_order=validation.version_order,
                                    strict_mode=bool(promoted), strict_warning_codes=promoted)
    if retained != rebuilt:
        raise _invalid("retained parent validation disagrees with its original declarations")
    versions = tuple(sorted({key.dataset_version for key in nodes}))
    if target_dataset_version is not None and target_dataset_version not in versions and target_dataset_version not in rebuilt.version_order.order:
        raise _invalid("lineage target version is outside the declared input scope", ErrorCode.CONFIG_INVALID)
    targets = tuple(key for key in nodes if key.dataset_version == target_dataset_version)
    scope = LineageScope(target_dataset_version, targets, len(targets), len(nodes), len(nodes) - len(targets), versions)
    evidence = {item.child_key: item for item in rebuilt.assessments}
    if tuple(evidence) != nodes:
        raise _invalid("retained parent validation does not cover the loaded scope")
    parents, children = {}, {key: [] for key in nodes}
    edges = 0
    for child in nodes:
        adjacent = _accepted_parents(evidence[child])
        accepted = []
        for parent in adjacent:
            if edges == bounded.max_edges:
                raise LineageResourceLimitError(LineageResourceUsage(len(nodes), edges, 0, 0,
                                                bounded, "max_edges", edges + 1))
            accepted.append(parent)
            children[parent].append(child)
            edges += 1
        parents[child] = tuple(accepted)
    usage = LineageResourceUsage(len(nodes), edges, 0, 0, bounded)
    if type(validation.validation_messages) is not tuple:
        raise _invalid("lineage validation diagnostics require an immutable tuple")
    return LineageGraph(scope, nodes, parents, {key: tuple(value) for key, value in children.items()},
                         evidence, tuple(key for key in nodes if evidence[key].invalid_self_reference_count),
                         validation.validation_messages + rebuilt.messages, usage)
