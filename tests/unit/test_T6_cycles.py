"""T6 cycle and structural-depth behavior over the retained parent graph.

Frozen fixture expectations predate implementation. A small reachability oracle
checks SCC behavior independently; scale and release gates remain separate.
"""

from dataclasses import FrozenInstanceError, replace
from itertools import permutations
import json
from pathlib import Path
import socket
from types import MappingProxyType

import pytest

from recursive_integrity_toolkit.errors import CanonicalValidationError
from recursive_integrity_toolkit.io.normalization import normalize_row
from recursive_integrity_toolkit.io.validation import (
    assess_provenance_row, resolve_parent_batch, resolve_version_order, validate_bundle,
    validate_generation_declarations,
)
from recursive_integrity_toolkit.lineage import cycles
from recursive_integrity_toolkit.lineage.graph import (
    LineageGraph, LineageLimits, LineageResourceUsage, LineageScope,
)
from recursive_integrity_toolkit.models import (
    AuditBundle, FileRole, InputSource, ParentResolutionStatus, RecordKey,
    ValidationMessage, ValidationSeverity,
)


_ABSENT = object()
_NO_PROVENANCE = object()
_FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"


def _key(identity):
    return RecordKey.parse(identity)


def _graph_from_rows(keys, provenance, *, target="v2", chronology=True, order=None):
    """Use real normalization/reference semantics without generation traversal."""
    nodes = tuple(sorted(keys))
    versions = tuple(sorted({key.dataset_version for key in nodes}))
    ordering = None
    if chronology and nodes:
        ordering = resolve_version_order(versions, invocation_order=tuple(order or versions))
    batch = resolve_parent_batch(nodes, tuple(provenance), version_order=ordering)
    evidence = {entry.child_key: entry for entry in batch.assessments}
    parents, children = {}, {node: [] for node in nodes}
    for child in nodes:
        result = evidence[child].result
        parents[child] = tuple(sorted({
            ref.parent_key for ref in (() if result is None else result.references)
            if ref.resolution_status is ParentResolutionStatus.RESOLVED
            and ref.temporal_status in ("same_version", "earlier_version")
            and ref.parent_key != child
        }))
        for parent in parents[child]:
            children[parent].append(child)
    targets = tuple(key for key in nodes if key.dataset_version == target)
    return LineageGraph(
        LineageScope(target, targets, len(targets), len(nodes), len(nodes) - len(targets), versions),
        nodes, parents, {key: tuple(value) for key, value in children.items()}, evidence,
        tuple(key for key in nodes if evidence[key].invalid_self_reference_count),
        batch.messages,
        LineageResourceUsage(len(nodes), sum(map(len, parents.values())), 0, 0, LineageLimits()),
    )


def _graph(declarations, *, target="v2", chronology=True, grounding=None, reverse=False):
    rows = []
    items = list(declarations.items())
    if reverse:
        items.reverse()
    for identity, parents in items:
        if parents is _NO_PROVENANCE:
            continue
        key = _key(identity)
        row = {
            "dataset_version": key.dataset_version, "record_id": key.record_id,
            "source_type": "unknown", "provenance_confidence": "confirmed",
            "external_grounding": (grounding or {}).get(identity, "no"),
        }
        if parents is not _ABSENT:
            row["parent_ids"] = list(reversed(parents)) if reverse and isinstance(parents, list) else parents
        rows.append(normalize_row(row, kind="provenance"))
    return _graph_from_rows(tuple(_key(identity) for identity in declarations), rows,
                            target=target, chronology=chronology)


def _fixture_cases(folder):
    return json.loads((_FIXTURES / folder / "cases.json").read_text(encoding="utf-8"))["cases"]


def _fixture_graph(case):
    keys = tuple(RecordKey(row["dataset_version"], row["record_id"]) for row in case["records"])
    rows = tuple(normalize_row(row, kind="provenance") for row in case["provenance"])
    target_keys = case["target_record_keys"]
    target = _key(target_keys[0]).dataset_version if target_keys else None
    return _graph_from_rows(keys, rows, target=target, order=case["version_order"])


def _depth(result, identity):
    return result.depths_by_record[_key(identity)].lineage_depth


def _check_topology(result, graph):
    order = result.topological_order
    assert len(set(order)) == len(order)
    assert set(order) == set(graph.node_keys) - set(result.affected_record_keys)
    positions = {key: index for index, key in enumerate(order)}
    for parent in order:
        for child in graph.children_by_parent[parent]:
            if child in positions:
                assert positions[parent] < positions[child]


def _check_witnesses(result, graph):
    for detail in result.component_details:
        component = result.cyclic_components[detail.component_index - 1]
        assert detail.member_count == len(component)
        assert detail.target_member_count == len(set(component) & set(graph.scope.target_record_keys))
        witness = detail.witness_record_keys
        if witness is None:
            assert detail.witness_reason == "diagnostic_limit"
            assert detail.witness_edge_count is None
            continue
        assert witness[0] == witness[-1]
        assert detail.witness_edge_count == len(witness) - 1
        assert 1 <= detail.witness_edge_count <= 64
        assert detail.witness_reason is None
        assert set(witness) <= set(component)
        for parent, child in zip(witness, witness[1:]):
            assert child in graph.children_by_parent[parent] or (
                parent == child and parent in graph.self_parent_record_keys
            )


@pytest.mark.parametrize("case", _fixture_cases("lineage_cycles"), ids=lambda case: case["case_id"])
def test_frozen_cycle_oracles_and_unaffected_topology(case):
    graph = _fixture_graph(case)
    result = cycles.analyze_cycles(graph)
    expected = case["expected_lineage"]
    assert result.cyclic_components == tuple(tuple(map(_key, group)) for group in expected["cyclic_components"])
    assert result.cycle_member_record_keys == tuple(map(_key, expected["cycle_member_keys"]))
    assert result.affected_record_keys == tuple(map(_key, expected["affected_record_keys"]))
    assert result.detected is expected["cycle_detected"]
    assert result.cycle_count == expected["cycle_count"]
    assert result.counting_method == expected["cycle_count_method"]
    assert result.cycle_status == "cyclic"
    targets = set(graph.scope.target_record_keys)
    assert result.cycle_member_count == len(result.cycle_member_record_keys)
    assert result.target_cycle_member_count == len(targets & set(result.cycle_member_record_keys))
    assert result.affected_record_count == len(result.affected_record_keys)
    assert result.target_affected_record_count == len(targets & set(result.affected_record_keys))
    assert result.has_errors
    assert any(message.code == "E_LINEAGE_CYCLE" and message.severity is ValidationSeverity.ERROR
               for message in result.messages)
    for key in result.affected_record_keys:
        assert result.depths_by_record[key].lineage_depth is None
        assert "CYCLE_AFFECTED" in result.depths_by_record[key].reason_codes
    if "lineage_depth" in expected:
        assert result.lineage_depth == expected["lineage_depth"]
    _check_topology(result, graph)
    _check_witnesses(result, graph)


@pytest.mark.parametrize("case", _fixture_cases("lineage_complete"), ids=lambda case: case["case_id"])
def test_frozen_complete_depth_oracles(case):
    graph = _fixture_graph(case)
    result = cycles.analyze_cycles(graph)
    expected = case["expected_lineage"]
    assert result.cycle_count == 0
    assert result.cycle_status == "acyclic"
    for key, depth in expected.get("depth_by_record", {}).items():
        assert _depth(result, key) == depth
    if "lineage_depth" in expected:
        assert result.lineage_depth == expected["lineage_depth"]
    if "carryover_depth" in expected:
        assert _depth(result, "v2::carry") == expected["carryover_depth"]
        assert _depth(result, "v2::diamond") == expected["diamond_depth"]
        rows = tuple(normalize_row(row, kind="provenance") for row in case["provenance"])
        generation = validate_generation_declarations(graph.node_keys, rows,
            version_order=resolve_version_order(graph.scope.loaded_dataset_versions,
                                                invocation_order=tuple(case["version_order"])))
        carry = next(entry for entry in generation.assessments if entry.record_key == _key("v2::carry"))
        assert carry.expected_generation == expected["carryover_generation"] == 0
        assert _depth(result, "v2::carry") == 1
    _check_topology(result, graph)


def test_depth_uses_longest_required_branch_and_deduplicates_diamond_paths():
    graph = _graph({
        "v2::root": [], "v2::a": ["root"], "v2::b": ["a"],
        "v2::c": ["b"], "v2::short": ["root"],
        "v2::join": ["short", "c", "v2::c"], "v2::last": ["join", "root"],
    })
    result = cycles.analyze_cycles(graph)
    expected = {"v2::root": 0, "v2::a": 1, "v2::b": 2, "v2::c": 3,
                "v2::short": 1, "v2::join": 4, "v2::last": 5}
    assert {_key(key): depth for key, depth in expected.items()} == {
        key: value.lineage_depth for key, value in result.depths_by_record.items()}
    assert result.lineage_depth == result.maximum_resolved_target_depth == 5
    assert result.depth_resolved_record_count == 7


@pytest.mark.parametrize("parents,reason", [
    (_ABSENT, "PARENT_DECLARATION_UNAVAILABLE"),
    (None, "PARENT_DECLARATION_UNAVAILABLE"),
    (_NO_PROVENANCE, "MISSING_PROVENANCE"),
    (["v2::missing"], "UNRESOLVED_PARENT_REFERENCE"),
    ([" invalid "], "INVALID_PARENT_REFERENCE"),
    (["v3::future"], "INVALID_PARENT_REFERENCE"),
])
def test_incomplete_branch_prevents_whole_target_depth(parents, reason):
    graph = _graph({"v2::safe": [], "v2::bad": parents,
                    "v2::join": ["safe", "bad"], "v2::child": ["join"], "v3::future": []})
    result = cycles.analyze_cycles(graph)
    assert _depth(result, "v2::safe") == 0
    assert _depth(result, "v2::bad") is None
    assert reason in result.depths_by_record[_key("v2::bad")].reason_codes
    for key in ("v2::join", "v2::child"):
        assert _depth(result, key) is None
        assert "INCOMPLETE_PARENT_DEPTH" in result.depths_by_record[_key(key)].reason_codes
    assert result.lineage_depth is None
    assert result.maximum_resolved_target_depth == 0
    assert result.depth_resolved_record_count == 1
    assert not result.detected
    assert result.cycle_status == "acyclic"
    assert result.cycle_status_scope == "accepted_edges_and_explicit_self_references"
    assert reason in result.input_reason_codes
    assert result.depth_reason_codes == ("INCOMPLETE_TARGET_DEPTH",)


def test_ambiguous_parent_blocks_depth_without_creating_cycle():
    graph = _graph({"v1::p": [], "v2::p": [], "v2::child": ["p", "v1::p"]})
    result = cycles.analyze_cycles(graph)
    assert _depth(result, "v2::child") is None
    assert "INVALID_PARENT_REFERENCE" in result.depths_by_record[_key("v2::child")].reason_codes
    assert result.cycle_count == 0
    assert result.has_errors


def test_malformed_parent_container_has_no_invented_zero_depth():
    key = _key("v2::bad")
    row = normalize_row({"dataset_version": "v2", "record_id": "bad",
                         "source_type": "unknown", "provenance_confidence": "confirmed",
                         "external_grounding": "no", "parent_ids": []}, kind="provenance")
    row = replace(row, values=MappingProxyType({**row.values, "parent_ids": "private scalar"}))
    graph = _graph_from_rows((key,), (row,))
    result = cycles.analyze_cycles(graph)
    assert _depth(result, "v2::bad") is None
    assert "INVALID_PARENT_REFERENCE" in result.depths_by_record[key].reason_codes
    assert result.depth_resolved_record_count == 0
    assert result.maximum_resolved_target_depth is None
    assert result.lineage_depth is None


def test_unknown_grounding_preserves_structural_depth():
    graph = _graph({"v2::root": [], "v2::child": ["root"]},
                   grounding={"v2::root": "unknown", "v2::child": "unknown"})
    result = cycles.analyze_cycles(graph)
    assert _depth(result, "v2::root") == 0
    assert _depth(result, "v2::child") == result.lineage_depth == 1
    assert all(entry.reason_codes == () for entry in result.depths_by_record.values())


def test_missing_nonstructural_metadata_does_not_invalidate_explicit_empty_depth():
    row = assess_provenance_row({"dataset_version": "v2", "record_id": "root", "parent_ids": []})
    graph = _graph_from_rows((row.record_key,), (row,))
    assert row.missing_required_fields
    result = cycles.analyze_cycles(graph)
    assert result.lineage_depth == 0
    assert result.depths_by_record[row.record_key].reason_codes == ()
    assert result.has_errors


def test_fatal_input_evidence_preserves_error_status_in_acyclic_graph():
    graph = _graph({"v2::root": []})
    graph = replace(graph, messages=(ValidationMessage(
        "E_PARENT_FORMAT", ValidationSeverity.FATAL, "Private arbitrary diagnostic"),))
    result = cycles.analyze_cycles(graph)
    assert result.cycle_status == "acyclic"
    assert result.has_errors
    assert result.messages[0].severity is ValidationSeverity.FATAL
    assert "Private arbitrary diagnostic" not in repr(result)


def test_resolved_identity_without_chronology_cannot_establish_depth():
    graph = _graph({"v1::root": [], "v2::child": ["v1::root"]}, chronology=False)
    assert graph.parent_evidence_by_record[_key("v2::child")].resolved_reference_count == 1
    result = cycles.analyze_cycles(graph)
    assert _depth(result, "v1::root") == 0
    assert _depth(result, "v2::child") is None
    assert "VERSION_ORDER_UNAVAILABLE" in result.depths_by_record[_key("v2::child")].reason_codes
    assert result.maximum_resolved_target_depth is None
    assert result.depth_resolved_record_count == 0
    assert result.lineage_depth is None


@pytest.mark.parametrize("size", [64, 65])
def test_cycle_witness_exact_edge_limit_and_order(size):
    keys = [f"v2::n{index:03}" for index in range(size)]
    graph = _graph({key: [keys[(index - 1) % size]] for index, key in enumerate(keys)})
    result = cycles.analyze_cycles(graph)
    detail = result.component_details[0]
    assert result.cycle_count == 1
    assert result.cycle_member_count == result.affected_record_count == size
    if size == 64:
        assert detail.witness_record_keys == tuple(map(_key, keys + [keys[0]]))
        assert detail.witness_edge_count == 64
    else:
        assert detail.witness_record_keys is None
        assert detail.witness_reason == "diagnostic_limit"
    _check_witnesses(result, graph)


def test_self_cycle_witness_and_bounded_detail_do_not_truncate_analysis():
    declarations = {f"v2::self{index:03}": [f"v2::self{index:03}"] for index in range(101)}
    result = cycles.analyze_cycles(_graph(declarations))
    assert result.cycle_count == result.cycle_member_count == result.affected_record_count == 101
    assert result.depth_resolved_record_count == 0
    assert len(result.component_details) == 100
    for index, detail in enumerate(result.component_details):
        key = _key(f"v2::self{index:03}")
        assert detail.component_index == index + 1
        assert detail.witness_record_keys == (key, key)
        assert detail.witness_edge_count == 1
    assert result.topological_order == ()


def test_cycle_depth_and_witness_results_ignore_input_permutations():
    declarations = {"v2::a": ["c", "b"], "v2::b": ["a", "c"],
                    "v2::c": ["a"], "v2::tail": ["c"], "v2::root": [], "v2::safe": ["root"]}
    left = cycles.analyze_cycles(_graph(declarations))
    right = cycles.analyze_cycles(_graph(declarations, reverse=True))
    assert left == right


def test_iterative_chain_beyond_python_recursion_depth():
    count = 1500
    declarations = {f"v2::n{index:04}": [] if index == 0 else [f"v2::n{index - 1:04}"]
                    for index in range(count)}
    graph = _graph(declarations)
    result = cycles.analyze_cycles(graph)
    assert not result.detected
    assert result.lineage_depth == result.maximum_resolved_target_depth == count - 1
    assert result.depth_resolved_record_count == count
    assert result.topological_order == graph.node_keys
    assert tuple(item.lineage_depth for item in result.depths_by_record.values()) == tuple(range(count))


def test_context_depth_is_excluded_from_target_maximum():
    graph = _graph({"v1::a": [], "v1::b": ["a"], "v1::c": ["b"], "v2::target": []})
    result = cycles.analyze_cycles(graph)
    assert _depth(result, "v1::c") == 2
    assert result.lineage_depth == result.maximum_resolved_target_depth == 0
    assert result.depth_resolved_record_count == 1


@pytest.mark.parametrize("target", [None, "v2"])
def test_empty_target_never_borrows_context_depth(target):
    result = cycles.analyze_cycles(_graph({"v1::root": [], "v1::child": ["root"]}, target=target))
    assert result.scope.target_record_count == 0
    assert result.lineage_depth is result.maximum_resolved_target_depth is None
    assert result.depth_resolved_record_count == 0
    assert result.depth_reason_codes == ("EMPTY_TARGET_SCOPE",)
    assert _depth(result, "v1::child") == 1


def test_empty_graph_has_complete_empty_topology_and_unavailable_depth():
    result = cycles.analyze_cycles(_graph({}, target=None))
    assert result.cyclic_components == result.cycle_member_record_keys == result.affected_record_keys == ()
    assert result.topological_order == ()
    assert dict(result.depths_by_record) == {}
    assert result.lineage_depth is result.maximum_resolved_target_depth is None
    assert result.depth_resolved_record_count == 0
    assert result.cycle_status == "acyclic"


def test_result_is_a_defensive_immutable_snapshot():
    result = cycles.analyze_cycles(_graph({"v2::root": [], "v2::child": ["root"]}))
    external = dict(result.depths_by_record)
    copied = replace(result, depths_by_record=external)
    external.clear()
    assert copied == result
    with pytest.raises(TypeError):
        copied.depths_by_record[_key("v2::root")] = None
    with pytest.raises(FrozenInstanceError):
        copied.lineage_depth = 999
    with pytest.raises(FrozenInstanceError):
        copied.depths_by_record[_key("v2::root")].lineage_depth = 999


@pytest.mark.parametrize("mutation", ["type", "adjacency", "evidence", "scope",
                                      "resolved_without_key", "resolved_self",
                                      "false_earlier_version", "false_unavailable"])
def test_forged_graph_handoff_is_rejected(mutation):
    graph = _graph({"v2::root": [], "v2::child": ["root"]})
    if mutation == "type":
        graph = {"node_keys": graph.node_keys}
    elif mutation == "adjacency":
        object.__setattr__(graph, "children_by_parent", MappingProxyType({key: () for key in graph.node_keys}))
    elif mutation == "evidence":
        evidence = dict(graph.parent_evidence_by_record)
        child = _key("v2::child")
        evidence[child] = replace(evidence[child], resolved_reference_count=0)
        object.__setattr__(graph, "parent_evidence_by_record", evidence)
    elif mutation == "scope":
        object.__setattr__(graph.scope, "target_record_count", True)
    else:
        evidence = dict(graph.parent_evidence_by_record)
        child = _key("v2::child")
        entry = evidence[child]
        reference = entry.result.references[0]
        if mutation in ("false_earlier_version", "false_unavailable"):
            reference = replace(reference, temporal_status=(
                "earlier_version" if mutation == "false_earlier_version" else "unavailable"))
        else:
            parent = child if mutation == "resolved_self" else None
            reference = replace(reference, parent_key=parent,
                                canonical_reference=None if parent is None else str(parent))
        evidence[child] = replace(entry, result=replace(entry.result, references=(reference,)))
        if mutation == "false_earlier_version":
            graph = replace(graph, parent_evidence_by_record=evidence)
        else:
            # These forms have no accepted adjacency. Rebuild a consistent
            # outer graph to exercise semantic reference admission.
            graph = replace(graph, parents_by_child={key: () for key in graph.node_keys},
                            children_by_parent={key: () for key in graph.node_keys},
                            parent_evidence_by_record=evidence,
                            resource_usage=replace(graph.resource_usage, admitted_edge_count=0))
    with pytest.raises(CanonicalValidationError):
        cycles.analyze_cycles(graph)


def test_cycle_analysis_uses_no_file_or_network_io(monkeypatch):
    graph = _graph({"v2::a": ["b"], "v2::b": ["a"], "v2::missing": ["unknown"]})
    def forbidden(*args, **kwargs):
        raise AssertionError("Cycle analysis must consume only its immutable graph")
    monkeypatch.setattr("builtins.open", forbidden)
    monkeypatch.setattr(Path, "open", forbidden)
    monkeypatch.setattr(socket, "socket", forbidden)
    result = cycles.analyze_cycles(graph)
    assert result.cycle_count == 1
    assert all(message.file_path is message.row_number is message.line_number is None
               for message in result.messages)


def test_input_validation_never_dispatches_cycle_analysis(tmp_path, monkeypatch):
    records = tmp_path / "records.jsonl"
    provenance = tmp_path / "provenance.jsonl"
    records.write_text(json.dumps({"dataset_version": "v2", "record_id": "a", "content": "private"}) + "\n")
    provenance.write_text(json.dumps({"dataset_version": "v2", "record_id": "a", "source_type": "unknown",
        "provenance_confidence": "confirmed", "external_grounding": "no", "parent_ids": []}) + "\n")
    def forbidden(*args, **kwargs):
        raise AssertionError("Input validation cannot dispatch cycle analysis")
    monkeypatch.setattr(cycles, "analyze_cycles", forbidden)
    result = validate_bundle(AuditBundle((InputSource(FileRole.RECORDS_PRIMARY, records),
                                         InputSource(FileRole.PROVENANCE_MANIFEST, provenance))))
    assert result.parent_validation is not None
    assert not result.has_errors


def test_all_three_node_directed_graphs_match_independent_reachability_oracle():
    """64 small graphs detect SCC splitting, descendant direction and lost edges."""
    keys = tuple(_key(f"v2::{name}") for name in "abc")
    possible_edges = tuple(permutations(range(3), 2))
    for mask in range(1 << len(possible_edges)):
        edges = {edge for index, edge in enumerate(possible_edges) if mask & (1 << index)}
        reach = [[(start, end) in edges for end in range(3)] for start in range(3)]
        for via in range(3):
            for start in range(3):
                for end in range(3):
                    reach[start][end] |= reach[start][via] and reach[via][end]
        components, seen = [], set()
        for start in range(3):
            if start not in seen and reach[start][start]:
                members = tuple(index for index in range(3) if reach[start][index] and reach[index][start])
                components.append(tuple(keys[index] for index in members))
                seen.update(members)
        affected = {index for member in seen for index in range(3) if index == member or reach[member][index]}
        declarations = {str(key): [str(keys[parent]) for parent in range(3) if (parent, child) in edges]
                        for child, key in enumerate(keys)}
        graph = _graph(declarations)
        result = cycles.analyze_cycles(graph)
        assert result.cyclic_components == tuple(components), mask
        assert result.cycle_member_record_keys == tuple(keys[index] for index in sorted(seen)), mask
        assert result.affected_record_keys == tuple(keys[index] for index in sorted(affected)), mask
        _check_topology(result, graph)
        _check_witnesses(result, graph)
