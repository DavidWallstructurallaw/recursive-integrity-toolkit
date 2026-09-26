"""Direct work-budget behavior for complete external-root propagation.

Fixtures use canonical normalization, joining and batch reference validation.
They omit generation traversal so the long chain isolates iterative ancestry.
"""

from dataclasses import FrozenInstanceError

import pytest

from recursive_integrity_toolkit.errors import LineageResourceLimitError
from recursive_integrity_toolkit.io.normalization import normalize_row
from recursive_integrity_toolkit.io.validation import (
    join_provenance, resolve_parent_batch, resolve_version_order,
)
from recursive_integrity_toolkit.lineage.ancestry import analyze_lineage
from recursive_integrity_toolkit.lineage.graph import LineageLimits
from recursive_integrity_toolkit.models import BundleValidationResult, RecordKey, ValidationSeverity
from recursive_integrity_toolkit.observability.levels import classify_observability
from recursive_integrity_toolkit.result import ExecutionStatus


def _key(identity):
    return RecordKey.parse(identity)


def _validation(declarations, *, grounding=None, transformation=None, reverse=False):
    """Construct a validated handoff with generation omitted to isolate ancestry."""
    records, provenance = [], []
    items = list(declarations.items())
    if reverse:
        items.reverse()
    for identity, parents in items:
        key = _key(identity)
        fields = {"dataset_version": key.dataset_version, "record_id": key.record_id}
        records.append(normalize_row({**fields, "content": "private input"}, kind="records"))
        provenance.append(normalize_row({
            **fields, "source_type": "unknown", "provenance_confidence": "confirmed",
            "external_grounding": (grounding or {}).get(identity, "no"),
            "transformation": (transformation or {}).get(identity, "generate"),
            "parent_ids": list(reversed(parents)) if reverse else parents,
        }, kind="provenance"))
    records, provenance = tuple(records), tuple(provenance)
    keys = tuple(row.record_key for row in records)
    versions = tuple(sorted({key.dataset_version for key in keys}))
    order = resolve_version_order(versions, invocation_order=versions)
    joined = join_provenance(records, provenance)
    batch = resolve_parent_batch(keys, provenance, version_order=order)
    observability = classify_observability(records, provenance=provenance, version_order=order)
    return BundleValidationResult(
        (), records, provenance, joined, order, None, observability,
        (), (), tuple(joined.messages) + tuple(batch.messages), batch,
    )


def _analyze(declarations, *, grounding=None, transformation=None, reverse=False, **limits):
    return analyze_lineage(_validation(declarations, grounding=grounding,
                                       transformation=transformation, reverse=reverse),
                           target_dataset_version="v2", limits=LineageLimits(**limits))


def _shared_roots(*, aliases=False):
    """Two roots, one union, then a union with a duplicate candidate root."""
    return {
        "v1::a": [], "v1::b": [],
        "v2::m": ["a", "b", "v1::a", "a"] if aliases else ["a", "b"],
        "v2::z": ["m", "a", "v2::m", "a"] if aliases else ["m", "a"],
    }


def _assert_root_failure(result, *, name, memberships, visits, attempted):
    assert result.execution_status is ExecutionStatus.FAILED
    assert "LINEAGE_RESOURCE_LIMIT_EXCEEDED" in result.execution_reason_codes
    assert any(message.code == "E_LINEAGE_RESOURCE_LIMIT_EXCEEDED"
               and message.severity in (ValidationSeverity.ERROR, ValidationSeverity.FATAL)
               for message in result.messages)
    assert result.records is None
    assert result.grounded_record_count is None
    assert result.closed_record_count is None
    assert result.unresolved_record_count is None
    assert result.records_with_resolved_external_ancestry is None
    assert result.resolved_lineage_coverage is None
    assert result.external_ancestry_coverage is None
    usage = result.resource_usage
    assert usage.exhausted_limit == name
    assert usage.stored_root_membership_count == memberships
    assert usage.root_union_visit_count == visits
    assert usage.attempted_value == attempted
    # Graph and structural analysis finished before root propagation stopped.
    assert result.cycles is not None
    assert result.cycles.cycle_count == 0
    assert result.cycles.lineage_depth == 2
    assert result.resolved_parent_edge_coverage == 1.0


def test_anchor_storage_and_known_empty_sets_have_distinct_work_costs():
    result = _analyze({"v2::anchor": [], "v2::closed": []},
                      grounding={"v2::anchor": "yes"},
                      max_root_memberships=1, max_root_union_visits=1)
    usage = result.resource_usage
    assert result.execution_status is ExecutionStatus.COMPLETED
    assert usage.stored_root_membership_count == 1
    assert usage.root_union_visit_count == 0
    assert usage.exhausted_limit is None
    assert usage.attempted_value is None
    roots = {entry.record_key: entry.external_root_keys for entry in result.records}
    assert roots[_key("v2::anchor")] == frozenset({_key("v2::anchor")})
    assert roots[_key("v2::closed")] == frozenset()
    with pytest.raises(FrozenInstanceError):
        usage.root_union_visit_count = 1


def test_grounded_carryover_charges_logical_membership_even_if_set_is_shared():
    result = _analyze({"v2::anchor": [], "v2::carry": ["anchor"]},
                      grounding={"v2::anchor": "yes", "v2::carry": "yes"},
                      transformation={"v2::carry": "carryover"},
                      max_root_memberships=2, max_root_union_visits=1)
    assert result.execution_status is ExecutionStatus.COMPLETED
    assert result.resource_usage.stored_root_membership_count == 2
    assert result.resource_usage.root_union_visit_count == 1
    assert all(entry.external_root_keys == frozenset({_key("v2::anchor")})
               for entry in result.records)


@pytest.mark.parametrize("aliases", [False, True])
def test_root_union_counts_duplicate_candidates_but_deduplicates_alias_edges(aliases):
    result = _analyze(_shared_roots(aliases=aliases),
                      grounding={"v1::a": "yes", "v1::b": "yes"},
                      max_root_memberships=6, max_root_union_visits=5)
    assert result.execution_status is ExecutionStatus.COMPLETED
    usage = result.resource_usage
    assert (usage.admitted_node_count, usage.admitted_edge_count) == (4, 4)
    assert (usage.stored_root_membership_count, usage.root_union_visit_count) == (6, 5)
    assert usage.exhausted_limit is None
    assert usage.attempted_value is None
    by_key = {entry.record_key: entry for entry in result.records}
    expected = frozenset({_key("v1::a"), _key("v1::b")})
    assert result.scope.target_record_count == result.grounded_record_count == 2
    assert by_key[_key("v2::m")].external_root_keys == expected
    assert by_key[_key("v2::z")].external_root_keys == expected


@pytest.mark.parametrize("membership_limit,expected_visits", [(4, 3), (5, 5)])
def test_membership_limit_rejects_next_storage_without_returning_partial_partition(
        membership_limit, expected_visits):
    result = _analyze(_shared_roots(), grounding={"v1::a": "yes", "v1::b": "yes"},
                      max_root_memberships=membership_limit, max_root_union_visits=5)
    _assert_root_failure(result, name="max_root_memberships", memberships=membership_limit,
                         visits=expected_visits, attempted=membership_limit + 1)


def test_union_limit_rejects_next_candidate_before_visit_or_storage():
    result = _analyze(_shared_roots(), grounding={"v1::a": "yes", "v1::b": "yes"},
                      max_root_memberships=6, max_root_union_visits=4)
    _assert_root_failure(result, name="max_root_union_visits", memberships=5,
                         visits=4, attempted=5)


def test_unresolved_branches_never_consume_storage_for_observed_partial_roots():
    result = _analyze({
        "v2::anchor": [], "v2::unknown": [],
        "v2::mixed": ["anchor", "unknown"], "v2::descendant": ["mixed"],
        "v2::unsupported": ["anchor", "unknown"],
    }, grounding={"v2::anchor": "yes", "v2::unknown": "unknown", "v2::unsupported": "yes"},
        max_root_memberships=1, max_root_union_visits=1)
    assert result.execution_status is ExecutionStatus.PARTIAL
    assert result.resource_usage.stored_root_membership_count == 1
    assert result.resource_usage.root_union_visit_count == 0
    assert result.resource_usage.exhausted_limit is None
    by_key = {entry.record_key: entry for entry in result.records}
    for name in ("unknown", "mixed", "descendant", "unsupported"):
        assert by_key[_key("v2::" + name)].external_root_keys is None
    assert (result.grounded_record_count, result.closed_record_count,
            result.unresolved_record_count) == (1, 0, 4)


def test_budget_schedule_uses_canonical_ready_nodes_and_is_input_permutation_invariant():
    # z must run before a because a depends on z. Once z finishes, a is the
    # canonical next ready node, ahead of the independent zz anchor.
    declarations = {"v2::z": [], "v2::a": ["z"], "v2::b": ["a"], "v2::zz": []}
    grounding = {"v2::z": "yes", "v2::zz": "yes"}
    results = [_analyze(declarations, grounding=grounding, reverse=reverse,
                        max_root_memberships=2, max_root_union_visits=10)
               for reverse in (False, True)]
    for result in results:
        _assert_root_failure(result, name="max_root_memberships", memberships=2,
                             visits=2, attempted=3)
    assert results[0] == results[1]


def test_root_propagation_is_iterative_for_a_chain_beyond_python_recursion_depth():
    size = 1200
    declarations = {f"v2::n{index:04d}": [] if index == size - 1 else [f"n{index + 1:04d}"]
                    for index in range(size)}
    anchor = f"v2::n{size - 1:04d}"
    result = _analyze(declarations, grounding={anchor: "yes"},
                      max_root_memberships=size, max_root_union_visits=size - 1)
    assert result.execution_status is ExecutionStatus.COMPLETED
    assert result.grounded_record_count == size
    assert result.closed_record_count == result.unresolved_record_count == 0
    assert result.resource_usage.stored_root_membership_count == size
    assert result.resource_usage.root_union_visit_count == size - 1
    assert result.cycles.lineage_depth == size - 1
    assert all(entry.external_root_keys == frozenset({_key(anchor)}) for entry in result.records)


@pytest.mark.parametrize("visit_limit", [256, 257])
def test_layered_fan_in_counts_repeated_paths_and_rejects_the_next_visit(visit_limit):
    roots = [f"v1::r{index:02d}" for index in range(32)]
    middles = [f"v1::m{index}" for index in range(4)]
    declarations = {**{root: [] for root in roots}, **{middle: roots for middle in middles},
                    "v2::target": [*middles, roots[0]]}
    result = _analyze(declarations, grounding={root: "yes" for root in roots},
                      max_root_memberships=192, max_root_union_visits=visit_limit)
    usage = result.resource_usage
    assert (usage.admitted_node_count, usage.admitted_edge_count) == (37, 133)
    assert usage.stored_root_membership_count == 192
    assert usage.root_union_visit_count == visit_limit
    assert result.cycles.lineage_depth == 2
    if visit_limit == 256:
        assert result.execution_status is ExecutionStatus.FAILED
        assert result.records is result.grounded_record_count is result.root_contributions is None
        assert result.resolved_lineage_coverage is None
        assert usage.exhausted_limit == "max_root_union_visits" and usage.attempted_value == 257
    else:
        assert result.execution_status is ExecutionStatus.COMPLETED
        assert usage.exhausted_limit is usage.attempted_value is None
        assert result.records[0].external_root_keys == frozenset(_key(root) for root in roots)
        assert result.grounded_record_count == 1
        assert result.ancestry_concentration_hhi == 1 / 32
        assert result.effective_external_root_count == 32.0


@pytest.mark.parametrize("limits,limit_name,expected_nodes,expected_edges", [
    ({"max_nodes": 1}, "max_nodes", 1, 0),
    ({"max_edges": 1}, "max_edges", 3, 1),
])
def test_graph_admission_failure_keeps_existing_typed_error_before_root_work(
        limits, limit_name, expected_nodes, expected_edges):
    with pytest.raises(LineageResourceLimitError) as caught:
        _analyze({"v2::a": [], "v2::b": ["a"], "v2::c": ["b"]},
                 grounding={"v2::a": "yes"}, **limits)
    usage = caught.value.resource_usage
    assert caught.value.reason_code == "LINEAGE_RESOURCE_LIMIT_EXCEEDED"
    assert usage.exhausted_limit == limit_name
    assert (usage.admitted_node_count, usage.admitted_edge_count) == (expected_nodes, expected_edges)
    assert usage.stored_root_membership_count == usage.root_union_visit_count == 0
    assert usage.attempted_value == 2
