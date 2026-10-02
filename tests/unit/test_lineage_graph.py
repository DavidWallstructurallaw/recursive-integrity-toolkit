"""Direct Phase 5 graph behavior, reference boundaries and resource admission.

These tests execute graph construction only. They make no ancestry, cycle,
concentration or report-completion claim.
"""

from dataclasses import FrozenInstanceError, replace
import json
from pathlib import Path
import socket

import pytest

from recursive_integrity_toolkit.errors import CanonicalValidationError
from recursive_integrity_toolkit.io.validation import resolve_version_order, validate_bundle
from recursive_integrity_toolkit.lineage.graph import (
    LineageLimits,
    LineageResourceLimitError,
    build_lineage_graph,
)
from recursive_integrity_toolkit.models import (
    AuditBundle,
    FileRole,
    InputSource,
    RecordKey,
    ValidationSeverity,
)


ABSENT = object()
MISSING_PROVENANCE = object()


def _key(value):
    return RecordKey.parse(value)


def _write_rows(path, rows):
    path.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")


def _validation(tmp_path, declarations, *, target="v2", chronology=True,
                strict=False, reverse=False):
    """Use the real loader and validator so fixture evidence is never forged."""
    tmp_path.mkdir(parents=True, exist_ok=True)
    records = []
    provenance = []
    for identity, parents in declarations.items():
        key = _key(identity)
        identity_fields = {"dataset_version": key.dataset_version, "record_id": key.record_id}
        records.append({**identity_fields, "content": "Private fixture content"})
        if parents is MISSING_PROVENANCE:
            continue
        row = {
            **identity_fields,
            "source_type": "synthetic",
            "provenance_confidence": "confirmed",
            "external_grounding": "no",
            "transformation": "generate",
        }
        if parents is not ABSENT:
            row["parent_ids"] = list(reversed(parents)) if reverse and isinstance(parents, list) else parents
        provenance.append(row)
    if reverse:
        records.reverse()
        provenance.reverse()
    primary = [row for row in records if row["dataset_version"] == target]
    context = [row for row in records if row["dataset_version"] != target]
    sources = []
    for name, role, rows in (
        ("primary.jsonl", FileRole.RECORDS_PRIMARY, primary),
        ("context.jsonl", FileRole.RECORDS_COMPARE, context),
    ):
        if rows:
            path = tmp_path / name
            _write_rows(path, rows)
            sources.append(InputSource(role, path))
    if provenance:
        path = tmp_path / "provenance.jsonl"
        _write_rows(path, provenance)
        sources.append(InputSource(FileRole.PROVENANCE_MANIFEST, path))
    if chronology:
        path = tmp_path / "order.json"
        versions = sorted({row["dataset_version"] for row in records} | {target})
        path.write_text(json.dumps({"version_order": versions}), encoding="utf-8")
        sources.append(InputSource(FileRole.VERSION_ORDER, path))
    configuration = None
    if strict:
        configuration = {"strict_mode": True, "strict_warning_codes": ["W_PARENT_UNRESOLVED"]}
    return validate_bundle(AuditBundle(tuple(sources)), configuration=configuration)


def _edges(graph):
    return {(str(parent), str(child)) for child, parents in graph.parents_by_child.items()
            for parent in parents}


def _evidence(graph, identity):
    return graph.parent_evidence_by_record[_key(identity)]


def test_exact_graph_keeps_context_out_of_target_population(tmp_path):
    validation = _validation(tmp_path, {
        "v1::a": [], "v1::b": [],
        "v2::c": ["v1::a", "v1::b"], "v2::d": ["v2::c"],
    })
    graph = build_lineage_graph(validation, target_dataset_version="v2")
    assert tuple(map(str, graph.node_keys)) == ("v1::a", "v1::b", "v2::c", "v2::d")
    assert graph.scope.target_record_keys == (_key("v2::c"), _key("v2::d"))
    assert (graph.scope.target_record_count, graph.scope.loaded_record_count,
            graph.scope.context_record_count) == (2, 4, 2)
    assert graph.scope.loaded_dataset_versions == ("v1", "v2")
    assert _edges(graph) == {("v1::a", "v2::c"), ("v1::b", "v2::c"), ("v2::c", "v2::d")}
    assert set(graph.parents_by_child) == set(graph.node_keys) == set(graph.children_by_parent)
    assert {(str(parent), str(child)) for parent, children in graph.children_by_parent.items()
            for child in children} == _edges(graph)
    assert graph.parents_by_child[_key("v1::a")] == ()
    assert graph.children_by_parent[_key("v2::d")] == ()
    assert (graph.resource_usage.admitted_node_count, graph.resource_usage.admitted_edge_count) == (4, 3)
    assert graph.resource_usage.stored_root_membership_count == 0
    assert graph.resource_usage.root_union_visit_count == 0
    assert graph.resource_usage.exhausted_limit is None


def test_aliases_preserve_original_reference_count_and_one_edge(tmp_path):
    validation = _validation(tmp_path, {"v1::a": [], "v2::c": ["a", "v1::a", "a"]})
    graph = build_lineage_graph(validation, target_dataset_version="v2", limits=LineageLimits(max_edges=1))
    evidence = _evidence(graph, "v2::c")
    assert _edges(graph) == {("v1::a", "v2::c")}
    assert evidence.declared_reference_count == evidence.resolved_reference_count == 3
    assert evidence.result.references[0].source_references == ("a", "a", "v1::a")
    assert graph.resource_usage.admitted_edge_count == 1


@pytest.mark.parametrize("reference,error_code", [
    ("v1::missing", "W_PARENT_UNRESOLVED"),
    ("p", "E_PARENT_AMBIGUOUS"),
    ("v3::future", "E_PARENT_FUTURE_VERSION"),
    (" malformed ", "E_PARENT_FORMAT"),
    ("v2::c", "E_LINEAGE_CYCLE"),
])
def test_invalid_sibling_never_erases_valid_reference_or_becomes_edge(tmp_path, reference, error_code):
    validation = _validation(tmp_path, {
        "v1::p": [], "v1::q": [], "v2::p": [], "v3::future": [],
        "v2::c": [reference, "v1::q"],
    })
    graph = build_lineage_graph(validation, target_dataset_version="v2")
    evidence = _evidence(graph, "v2::c")
    assert _edges(graph) == {("v1::q", "v2::c")}
    assert evidence.declared_reference_count == 2
    assert evidence.resolved_reference_count == 1
    assert error_code in {message.code for message in graph.messages}
    expected_self = (_key("v2::c"),) if reference == "v2::c" else ()
    assert graph.self_parent_record_keys == expected_self
    assert evidence.invalid_self_reference_count == len(expected_self)
    assert _key("v1::missing") not in graph.node_keys


def test_unknown_cross_version_chronology_cannot_certify_edge(tmp_path):
    validation = _validation(tmp_path, {"v10::p": [], "v2::c": ["v10::p"]}, chronology=False)
    graph = build_lineage_graph(validation, target_dataset_version="v2")
    evidence = _evidence(graph, "v2::c")
    assert evidence.result.references[0].temporal_status == "unavailable"
    assert "W_VERSION_ORDER_MISSING" in {message.code for message in graph.messages}
    assert _edges(graph) == set()


def test_absent_null_empty_and_missing_provenance_remain_distinct(tmp_path):
    validation = _validation(tmp_path, {
        "v2::absent": ABSENT, "v2::null": None,
        "v2::empty": [], "v2::missing": MISSING_PROVENANCE,
    })
    graph = build_lineage_graph(validation, target_dataset_version="v2")
    for identity, state in (("v2::absent", "absent"), ("v2::null", "null"), ("v2::empty", "empty")):
        evidence = _evidence(graph, identity)
        assert evidence.provenance_available
        assert evidence.result.declaration_state == state
        assert evidence.declared_reference_count == 0
    missing = _evidence(graph, "v2::missing")
    assert not missing.provenance_available
    assert missing.result.declaration_state == "absent"
    assert len(graph.node_keys) == graph.scope.target_record_count == 4
    assert not _edges(graph)


def test_missing_reference_strict_promotion_survives_graph_handoff(tmp_path):
    declarations = {"v2::c": ["missing"]}
    ordinary = build_lineage_graph(_validation(tmp_path / "ordinary", declarations), target_dataset_version="v2")
    strict = build_lineage_graph(_validation(tmp_path / "strict", declarations, strict=True), target_dataset_version="v2")
    assert [m.severity for m in ordinary.messages if m.code == "W_PARENT_UNRESOLVED"] == [ValidationSeverity.WARNING]
    assert [m.severity for m in strict.messages if m.code == "W_PARENT_UNRESOLVED"] == [ValidationSeverity.ERROR]
    assert ordinary.node_keys == strict.node_keys
    assert _edges(ordinary) == _edges(strict) == set()


def test_cycle_fixture_preserves_graph_and_self_evidence_without_execution_claim(tmp_path):
    validation = _validation(tmp_path, {
        "v1::self": ["v1::self"], "v1::a": ["v1::b"], "v1::b": ["v1::a"],
        "v2::child": ["v1::a"], "v2::safe": [],
    })
    graph = build_lineage_graph(validation, target_dataset_version="v2")
    assert _edges(graph) == {("v1::a", "v1::b"), ("v1::b", "v1::a"), ("v1::a", "v2::child")}
    assert graph.self_parent_record_keys == (_key("v1::self"),)
    assert len(graph.node_keys) == 5


def test_graph_is_deterministic_under_rows_and_references_permutation(tmp_path):
    declarations = {"v1::b": [], "v1::a": [], "v2::z": ["v1::b", "a", "v1::a"]}
    left = build_lineage_graph(_validation(tmp_path / "left", declarations), target_dataset_version="v2")
    right = build_lineage_graph(_validation(tmp_path / "right", declarations, reverse=True), target_dataset_version="v2")
    assert left == right


def test_graph_mappings_are_defensive_immutable_snapshots(tmp_path):
    graph = build_lineage_graph(_validation(tmp_path, {"v1::a": [], "v2::c": ["v1::a"]}), target_dataset_version="v2")
    parents = dict(graph.parents_by_child)
    children = dict(graph.children_by_parent)
    evidence = dict(graph.parent_evidence_by_record)
    copied = replace(graph, parents_by_child=parents, children_by_parent=children,
                     parent_evidence_by_record=evidence)
    parents.clear()
    children.clear()
    evidence.clear()
    assert copied == graph
    for mapping in (graph.parents_by_child, graph.children_by_parent, graph.parent_evidence_by_record):
        with pytest.raises(TypeError):
            mapping[_key("v2::c")] = ()
    with pytest.raises(FrozenInstanceError):
        graph.scope.target_record_count = 999
    with pytest.raises(FrozenInstanceError):
        _evidence(graph, "v2::c").declared_reference_count = 0


def test_graph_construction_does_not_reopen_input_or_use_network(tmp_path, monkeypatch):
    validation = _validation(tmp_path, {"v1::a": [], "v2::c": ["v1::a", "missing"]})
    def forbidden(*args, **kwargs):
        raise AssertionError("Graph construction must consume its in-memory validated handoff")
    monkeypatch.setattr("builtins.open", forbidden)
    monkeypatch.setattr(Path, "open", forbidden)
    monkeypatch.setattr(socket, "socket", forbidden)
    graph = build_lineage_graph(validation, target_dataset_version="v2")
    assert _edges(graph) == {("v1::a", "v2::c")}
    assert graph.messages
    assert all(message.file_path is None and message.row_number is None
               and message.line_number is None for message in graph.messages)
    assert "Private fixture content" not in repr(graph)
    assert str(tmp_path) not in repr(graph)


@pytest.mark.parametrize("field,value", [
    ("target_record_count", True), ("loaded_record_count", 1),
    ("context_record_count", -1), ("target_record_keys", (_key("v1::a"),)),
])
def test_forged_scope_cannot_replace_graph_population(tmp_path, field, value):
    graph = build_lineage_graph(_validation(tmp_path, {"v1::a": [], "v2::c": ["v1::a"]}), target_dataset_version="v2")
    with pytest.raises((CanonicalValidationError, TypeError, ValueError)):
        replace(graph, scope=replace(graph.scope, **{field: value}))


@pytest.mark.parametrize("selection", [None, "missing", "v1"])
def test_target_selection_rejects_implicit_or_context_population(tmp_path, selection):
    validation = _validation(tmp_path, {"v1::a": [], "v2::c": ["v1::a"]})
    with pytest.raises(CanonicalValidationError):
        build_lineage_graph(validation, target_dataset_version=selection)


@pytest.mark.parametrize("selection", [None, "v2"])
def test_empty_selected_scope_preserves_context_and_explicit_version(tmp_path, selection):
    validation = _validation(tmp_path, {"v1::a": []}, target="v1")
    # The approved empty-selection fixture is an in-memory scope contract.
    # Current input CLI still requires a nonempty primary table. Retain the
    # validated canonical data, explicitly mark its sole version as context,
    # and provide the empty version declaration without inventing a record.
    order = resolve_version_order(("v1",), document={"version_order": ["v1", "v2"]})
    validation = replace(
        validation,
        records=tuple(replace(row, location=replace(row.location, file_role=FileRole.RECORDS_COMPARE))
                      for row in validation.records),
        version_order=order,
        parent_validation=replace(validation.parent_validation, version_order=order),
    )
    graph = build_lineage_graph(validation, target_dataset_version=selection)
    assert graph.scope.target_dataset_version == selection
    assert graph.scope.target_record_keys == ()
    assert graph.scope.target_record_count == 0
    assert graph.scope.loaded_record_count == graph.scope.context_record_count == 1
    assert graph.node_keys == (_key("v1::a"),)
    assert not _edges(graph)


@pytest.mark.parametrize("mutation", ["missing_batch", "duplicate_node", "removed_node", "counter", "reference"])
def test_invalid_typed_handoff_is_rejected(tmp_path, mutation):
    validation = _validation(tmp_path, {"v1::a": [], "v2::c": ["v1::a"]})
    if mutation == "missing_batch":
        validation = replace(validation, parent_validation=None)
    elif mutation == "duplicate_node":
        validation = replace(validation, records=validation.records + (validation.records[0],))
    elif mutation == "removed_node":
        validation = replace(validation, records=validation.records[1:])
    else:
        batch = validation.parent_validation
        evidence = next(item for item in batch.assessments if item.child_key == _key("v2::c"))
        if mutation == "counter":
            forged = replace(evidence, resolved_reference_count=0)
        else:
            reference = evidence.result.references[0]
            forged_reference = replace(reference, parent_key=_key("v2::c"), canonical_reference="v2::c")
            forged = replace(evidence, result=replace(evidence.result, references=(forged_reference,)))
        validation = replace(validation, parent_validation=replace(batch, assessments=tuple(
            forged if item.child_key == evidence.child_key else item for item in batch.assessments)))
    with pytest.raises(CanonicalValidationError):
        build_lineage_graph(validation, target_dataset_version="v2")


@pytest.mark.parametrize("field,value", [
    ("max_nodes", True), ("max_edges", False), ("max_nodes", 0), ("max_edges", -1),
    ("max_root_memberships", None), ("max_root_union_visits", 1.5),
    ("max_edges", float("inf")),
])
def test_resource_limit_values_require_positive_exact_integers(field, value):
    with pytest.raises((CanonicalValidationError, TypeError, ValueError)):
        LineageLimits(**{field: value})


@pytest.mark.parametrize("exhausted,limit,admitted,attempted", [
    ("max_nodes", 2, 2, 3), ("max_edges", 1, 1, 2),
])
def test_resource_exhaustion_stops_at_next_admission(tmp_path, exhausted, limit, admitted, attempted):
    validation = _validation(tmp_path, {"v1::a": [], "v1::b": [], "v2::c": ["v1::a", "v1::b"]})
    limits = LineageLimits(**{exhausted: limit})
    with pytest.raises(LineageResourceLimitError) as error:
        build_lineage_graph(validation, target_dataset_version="v2", limits=limits)
    usage = error.value.resource_usage
    assert usage.exhausted_limit == exhausted
    assert usage.attempted_value == attempted
    assert (usage.admitted_node_count if exhausted == "max_nodes" else usage.admitted_edge_count) == admitted
    assert usage.limits == limits
    assert error.value.reason_code == "LINEAGE_RESOURCE_LIMIT_EXCEEDED"
    assert error.value.code.value == "E_LINEAGE_RESOURCE_LIMIT_EXCEEDED"


def test_resource_limits_allow_exact_boundary_without_truncation(tmp_path):
    validation = _validation(tmp_path, {"v1::a": [], "v1::b": [], "v2::c": ["v1::a", "v1::b"]})
    graph = build_lineage_graph(validation, target_dataset_version="v2", limits=LineageLimits(max_nodes=3, max_edges=2))
    assert len(graph.node_keys) == 3 and len(_edges(graph)) == 2
    assert graph.resource_usage.exhausted_limit is None
    assert graph.resource_usage.attempted_value is None


def test_direct_graph_handoff_cannot_drop_selected_version_records(tmp_path):
    graph = build_lineage_graph(_validation(tmp_path, {
        "v1::a": [], "v2::c": ["v1::a"], "v2::d": [],
    }), target_dataset_version="v2")
    # Counts can be internally consistent while silently excluding a target.
    forged_scope = replace(graph.scope, target_record_keys=(_key("v2::c"),),
                           target_record_count=1, context_record_count=2)
    with pytest.raises(CanonicalValidationError):
        replace(graph, scope=forged_scope)


def test_direct_graph_handoff_rejects_counter_disagreement_with_reference_evidence(tmp_path):
    graph = build_lineage_graph(_validation(tmp_path, {
        "v1::a": [], "v2::c": ["v1::a"],
    }), target_dataset_version="v2")
    evidence = dict(graph.parent_evidence_by_record)
    evidence[_key("v2::c")] = replace(evidence[_key("v2::c")], resolved_reference_count=0)
    with pytest.raises(CanonicalValidationError):
        replace(graph, parent_evidence_by_record=evidence)
