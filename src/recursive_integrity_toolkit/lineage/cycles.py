"""Analyze structural cycles, unaffected topology and complete structural depth.

Owner IDs: T6, PR-009 structural depth; Phase 5 Step 3.

Iterative traversals consume an immutable, revalidated parent graph. Cyclic
strongly connected components include separately retained invalid self-parents.
Complete internal identity sets support later ancestry work; presentation rows
are capped independently. No roots, scientific metrics, rendering or I/O occur.

Current phase status:
    Phase 5 Step 3 cycle detection, descendant propagation, topology and depth.
    External-root analysis and report integration remain later steps.
"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass, replace
from types import MappingProxyType
from typing import Mapping

from ..errors import ErrorCode
from ..models import ParentResolutionStatus, RecordKey, ValidationMessage, ValidationSeverity
from .graph import LineageGraph, LineageScope, _integer, _invalid, _key, _keys, _messages


_DETAIL_LIMIT = 100
_WITNESS_EDGE_LIMIT = 64
_DEPTH_REASONS = frozenset({
    "MISSING_PROVENANCE", "PARENT_DECLARATION_UNAVAILABLE", "INVALID_PARENT_REFERENCE",
    "UNRESOLVED_PARENT_REFERENCE", "VERSION_ORDER_UNAVAILABLE", "CYCLE_AFFECTED",
    "INCOMPLETE_PARENT_DEPTH",
})


@dataclass(frozen=True, slots=True)
class DepthAssessment:
    """Complete structural depth, or explicit structural failure reasons."""
    lineage_depth: int | None
    reason_codes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if (type(self.reason_codes) is not tuple
                or any(type(code) is not str or code not in _DEPTH_REASONS for code in self.reason_codes)
                or self.reason_codes != tuple(sorted(set(self.reason_codes)))):
            raise _invalid("structural depth requires canonical known reason codes")
        if self.lineage_depth is None:
            if not self.reason_codes:
                raise _invalid("unavailable structural depth requires a reason")
        else:
            _integer(self.lineage_depth)
            if self.reason_codes:
                raise _invalid("complete structural depth cannot carry failure reasons")


@dataclass(frozen=True, slots=True)
class CycleComponent:
    """Bounded component detail, independent of its complete internal membership."""
    component_index: int
    member_count: int
    target_member_count: int
    witness_record_keys: tuple[RecordKey, ...] | None
    witness_edge_count: int | None
    witness_reason: str | None

    def __post_init__(self) -> None:
        _integer(self.component_index, positive=True)
        _integer(self.member_count, positive=True)
        _integer(self.target_member_count)
        if self.target_member_count > self.member_count:
            raise _invalid("target cycle members exceed their component")
        witness = self.witness_record_keys
        if witness is None:
            if self.witness_edge_count is not None or self.witness_reason != "diagnostic_limit":
                raise _invalid("an omitted cycle witness requires its diagnostic limit reason")
        else:
            if type(witness) is not tuple or not 2 <= len(witness) <= _WITNESS_EDGE_LIMIT + 1:
                raise _invalid("cycle witnesses require bounded immutable key sequences")
            for key in witness:
                _key(key)
            _integer(self.witness_edge_count, positive=True)
            if (witness[0] != witness[-1] or self.witness_edge_count != len(witness) - 1
                    or self.witness_reason is not None):
                raise _invalid("cycle witness must be closed with its exact edge count")


@dataclass(frozen=True, slots=True)
class CycleAnalysis:
    """Full internal observations with separately bounded component diagnostics.

    Complete components/member/affected keys support later ancestry. Step 7 will
    wrap identity-bearing report collections in the approved bounded/privacy
    detail shape. Witness work already covers only the first 100 components.
    """
    scope: LineageScope
    cyclic_components: tuple[tuple[RecordKey, ...], ...]
    cycle_member_record_keys: tuple[RecordKey, ...]
    affected_record_keys: tuple[RecordKey, ...]
    topological_order: tuple[RecordKey, ...]
    depths_by_record: Mapping[RecordKey, DepthAssessment]
    component_details: tuple[CycleComponent, ...]
    lineage_depth: int | None
    maximum_resolved_target_depth: int | None
    depth_resolved_record_count: int
    messages: tuple[ValidationMessage, ...]

    def __post_init__(self) -> None:
        if type(self.scope) is not LineageScope:
            raise _invalid("cycle analysis requires a typed scope")
        scope = replace(self.scope)
        if type(self.depths_by_record) not in (dict, MappingProxyType):
            raise _invalid("cycle depth assessments require a mapping snapshot")
        nodes = _keys(tuple(sorted(self.depths_by_record)))
        if (len(nodes) != scope.loaded_record_count
                or tuple(key for key in nodes if key.dataset_version == scope.target_dataset_version) != scope.target_record_keys
                or tuple(sorted({key.dataset_version for key in nodes})) != scope.loaded_dataset_versions):
            raise _invalid("cycle depth coverage disagrees with the loaded scope")
        depths = {}
        for key in nodes:
            assessment = self.depths_by_record[key]
            if type(assessment) is not DepthAssessment:
                raise _invalid("cycle depths require typed assessments")
            depths[key] = replace(assessment)
        if type(self.cyclic_components) is not tuple:
            raise _invalid("cyclic components require immutable tuples")
        components = tuple(_keys(component) for component in self.cyclic_components)
        if any(not component for component in components) or components != tuple(sorted(components)):
            raise _invalid("cyclic components require canonical nonempty membership")
        members = _keys(self.cycle_member_record_keys)
        flattened = tuple(sorted(key for component in components for key in component))
        if flattened != members:
            raise _invalid("cyclic components must have disjoint, complete member coverage")
        affected = _keys(self.affected_record_keys)
        affected_set = set(affected)
        if not set(members) <= affected_set <= set(nodes):
            raise _invalid("cycle affected records must include all members within loaded scope")
        if (type(self.topological_order) is not tuple
                or any(type(key) is not RecordKey for key in self.topological_order)
                or len(set(self.topological_order)) != len(self.topological_order)
                or set(self.topological_order) != set(nodes) - affected_set):
            raise _invalid("cycle topology must cover exactly the unaffected records")
        if any(depths[key].lineage_depth is not None or "CYCLE_AFFECTED" not in depths[key].reason_codes for key in affected):
            raise _invalid("cycle affected records cannot have complete structural depth")
        if any("CYCLE_AFFECTED" in depths[key].reason_codes for key in nodes if key not in affected_set):
            raise _invalid("cycle depth reasons disagree with the affected-record set")
        if (type(self.component_details) is not tuple
                or len(self.component_details) != min(len(components), _DETAIL_LIMIT)):
            raise _invalid("cycle component details must observe the diagnostic cap")
        target_set = set(scope.target_record_keys)
        details = []
        for index, detail in enumerate(self.component_details, 1):
            if type(detail) is not CycleComponent:
                raise _invalid("cycle component details require typed rows")
            detail = replace(detail)
            component = components[index - 1]
            if (detail.component_index != index or detail.member_count != len(component)
                    or detail.target_member_count != sum(key in target_set for key in component)
                    or (detail.witness_record_keys is not None and not set(detail.witness_record_keys) <= set(component))):
                raise _invalid("cycle component detail disagrees with its complete membership")
            details.append(detail)
        complete = [depths[key].lineage_depth for key in scope.target_record_keys
                    if depths[key].lineage_depth is not None]
        maximum = max(complete, default=None)
        whole = maximum if len(complete) == scope.target_record_count else None
        _integer(self.depth_resolved_record_count)
        for value in (self.lineage_depth, self.maximum_resolved_target_depth):
            if value is not None:
                _integer(value)
        if (self.depth_resolved_record_count != len(complete)
                or self.maximum_resolved_target_depth != maximum or self.lineage_depth != whole):
            raise _invalid("cycle depth summaries disagree with the complete target subset")
        messages = _messages(self.messages)
        if components and not any(message.code == ErrorCode.LINEAGE_CYCLE.value
                                  and message.severity is ValidationSeverity.ERROR for message in messages):
            raise _invalid("detected cycles require an explicit lineage error")
        object.__setattr__(self, "scope", scope)
        object.__setattr__(self, "depths_by_record", MappingProxyType(depths))
        object.__setattr__(self, "component_details", tuple(details))
        object.__setattr__(self, "messages", messages)

    @property
    def detected(self) -> bool:
        return bool(self.cyclic_components)

    @property
    def cycle_count(self) -> int:
        return len(self.cyclic_components)

    @property
    def counting_method(self) -> str:
        return "cyclic_strongly_connected_components"

    @property
    def cycle_status(self) -> str:
        return "cyclic" if self.detected else "acyclic"

    @property
    def cycle_status_scope(self) -> str:
        return "accepted_edges_and_explicit_self_references"

    @property
    def cycle_member_count(self) -> int:
        return len(self.cycle_member_record_keys)

    @property
    def target_cycle_member_count(self) -> int:
        targets = set(self.scope.target_record_keys)
        return sum(key in targets for key in self.cycle_member_record_keys)

    @property
    def affected_record_count(self) -> int:
        return len(self.affected_record_keys)

    @property
    def target_affected_record_count(self) -> int:
        targets = set(self.scope.target_record_keys)
        return sum(key in targets for key in self.affected_record_keys)

    @property
    def omitted_component_count(self) -> int:
        return self.cycle_count - len(self.component_details)

    @property
    def depth_reason_codes(self) -> tuple[str, ...]:
        if not self.scope.target_record_count:
            return ("EMPTY_TARGET_SCOPE",)
        return () if self.lineage_depth is not None else ("INCOMPLETE_TARGET_DEPTH",)

    @property
    def input_reason_codes(self) -> tuple[str, ...]:
        return tuple(sorted({code for assessment in self.depths_by_record.values()
                             for code in assessment.reason_codes
                             if code not in ("CYCLE_AFFECTED", "INCOMPLETE_PARENT_DEPTH")}))

    @property
    def has_errors(self) -> bool:
        return any(message.severity in (ValidationSeverity.ERROR, ValidationSeverity.FATAL)
                   for message in self.messages)


def _cyclic_components(graph: LineageGraph) -> tuple[tuple[RecordKey, ...], ...]:
    """Iterative Kosaraju traversal, retaining only cyclic components."""
    visited, finished = set(), []
    for start in graph.node_keys:
        if start in visited:
            continue
        visited.add(start)
        stack = [(start, iter(graph.children_by_parent[start]))]
        while stack:
            node, neighbors = stack[-1]
            neighbor = next(neighbors, None)
            if neighbor is None:
                finished.append(node)
                stack.pop()
            elif neighbor not in visited:
                visited.add(neighbor)
                stack.append((neighbor, iter(graph.children_by_parent[neighbor])))
    visited.clear()
    self_parents = set(graph.self_parent_record_keys)
    components = []
    for start in reversed(finished):
        if start in visited:
            continue
        component, pending = [], [start]
        visited.add(start)
        while pending:
            node = pending.pop()
            component.append(node)
            for parent in graph.parents_by_child[node]:
                if parent not in visited:
                    visited.add(parent)
                    pending.append(parent)
        if len(component) > 1 or start in self_parents:
            components.append(tuple(sorted(component)))
    return tuple(sorted(components))


def _witness(graph: LineageGraph, component: tuple[RecordKey, ...],
             self_parents: set[RecordKey]) -> tuple[RecordKey, ...] | None:
    """Canonical DFS with at most 64 active nodes; a missed witness stays omitted."""
    membership = set(component)

    def neighbors(node: RecordKey):
        needs_self = node in self_parents
        for child in graph.children_by_parent[node]:
            if needs_self and child > node:
                yield node
                needs_self = False
            if child in membership:
                yield child
        if needs_self:
            yield node

    start = component[0]
    path, positions, visited = [start], {start: 0}, {start}
    stack = [neighbors(start)]
    while stack:
        child = next(stack[-1], None)
        if child is None:
            stack.pop()
            positions.pop(path.pop())
        elif child in positions:
            return tuple(path[positions[child]:] + [child])
        elif child not in visited:
            if len(path) == _WITNESS_EDGE_LIMIT:
                return None
            visited.add(child)
            positions[child] = len(path)
            path.append(child)
            stack.append(neighbors(child))
    return None


def _local_depth_reasons(graph: LineageGraph, key: RecordKey) -> set[str]:
    """Inspect structural evidence only; grounding and unrelated fields are inert."""
    evidence = graph.parent_evidence_by_record[key]
    reasons = set()
    if not evidence.provenance_available:
        reasons.add("MISSING_PROVENANCE")
    result = evidence.result
    if result is None:
        reasons.add("INVALID_PARENT_REFERENCE")
        return reasons
    if result.declaration_state in ("absent", "null"):
        reasons.add("PARENT_DECLARATION_UNAVAILABLE")
    represented = sum(len(ref.source_references) for ref in result.references)
    if (evidence.invalid_self_reference_count
            or evidence.declared_reference_count != represented
            or (result.declaration_state == "declared" and not represented)):
        reasons.add("INVALID_PARENT_REFERENCE")
    for reference in result.references:
        if reference.resolution_status is ParentResolutionStatus.RESOLVED and reference.parent_key is None:
            raise _invalid("resolved lineage references require a canonical parent identity")
        parent = reference.parent_key
        if parent == key:
            raise _invalid("self-parent references require separately retained invalid evidence")
        if parent is not None:
            same_version = parent.dataset_version == key.dataset_version
            if (reference.temporal_status == "same_version") != same_version:
                raise _invalid("lineage reference chronology disagrees with its canonical identities")
        if reference.resolution_status is not ParentResolutionStatus.RESOLVED:
            reasons.add("UNRESOLVED_PARENT_REFERENCE")
        if reference.temporal_status == "unavailable":
            reasons.add("VERSION_ORDER_UNAVAILABLE")
    return reasons


def analyze_cycles(graph: LineageGraph) -> CycleAnalysis:
    """Compute exact loaded-graph SCCs and target depth without recursive calls.

    Traversals are O(V + E), apart from canonical sorting and constructor
    validation. Witness search is bounded and cannot weaken an SCC finding.
    ``cycle_status`` describes accepted edges plus explicit self-reference
    evidence; ``input_reason_codes`` discloses structural input incompleteness.
    """
    if type(graph) is not LineageGraph:
        raise _invalid("cycle analysis requires a typed lineage graph")
    graph = replace(graph)
    components = _cyclic_components(graph)
    members = tuple(sorted(key for component in components for key in component))
    affected, pending = set(members), deque(members)
    while pending:
        for child in graph.children_by_parent[pending.popleft()]:
            if child not in affected:
                affected.add(child)
                pending.append(child)
    unaffected = tuple(key for key in graph.node_keys if key not in affected)
    indegree = {key: len(graph.parents_by_child[key]) for key in unaffected}
    pending = deque(key for key in unaffected if not indegree[key])
    topology = []
    local_reasons = {key: _local_depth_reasons(graph, key) for key in graph.node_keys}
    depths = {key: DepthAssessment(None, tuple(sorted(local_reasons[key] | {"CYCLE_AFFECTED"})))
              for key in graph.node_keys if key in affected}
    while pending:
        key = pending.popleft()
        topology.append(key)
        reasons = local_reasons[key]
        parent_depths = [depths[parent].lineage_depth for parent in graph.parents_by_child[key]]
        if any(value is None for value in parent_depths):
            reasons.add("INCOMPLETE_PARENT_DEPTH")
        value = None if reasons else 1 + max(parent_depths, default=-1)
        depths[key] = DepthAssessment(value, tuple(sorted(reasons)))
        for child in graph.children_by_parent[key]:
            if child not in affected:
                indegree[child] -= 1
                if not indegree[child]:
                    pending.append(child)
    if len(topology) != len(unaffected):
        raise _invalid("cycle topology did not cover every unaffected record")
    targets, self_parents = set(graph.scope.target_record_keys), set(graph.self_parent_record_keys)
    details = []
    for index, component in enumerate(components[:_DETAIL_LIMIT], 1):
        witness = _witness(graph, component, self_parents)
        details.append(CycleComponent(index, len(component), sum(key in targets for key in component),
                                      witness, None if witness is None else len(witness) - 1,
                                      "diagnostic_limit" if witness is None else None))
    complete = [depths[key].lineage_depth for key in graph.scope.target_record_keys
                if depths[key].lineage_depth is not None]
    maximum = max(complete, default=None)
    whole = maximum if len(complete) == graph.scope.target_record_count else None
    messages = graph.messages
    if components:
        messages += (ValidationMessage(ErrorCode.LINEAGE_CYCLE.value, ValidationSeverity.ERROR,
                                       "A cyclic component was detected in the loaded lineage graph."),)
    return CycleAnalysis(graph.scope, components, members, tuple(sorted(affected)), tuple(topology),
                         depths, tuple(details), whole, maximum, len(complete), messages)
