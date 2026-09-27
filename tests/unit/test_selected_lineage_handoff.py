"""Step 6 supplied lineage evidence is checked without dispatching analysis."""
from dataclasses import replace

import pytest

from recursive_integrity_toolkit.errors import CanonicalValidationError, LineageResourceLimitError
from recursive_integrity_toolkit.lineage import ancestry, cycles as cycle_module
from recursive_integrity_toolkit.lineage.cycles import CycleComponent, DepthAssessment
from recursive_integrity_toolkit.lineage.graph import LineageLimits, LineageResourceUsage
from recursive_integrity_toolkit.models import RecordKey
from test_longitudinal_analysis import _select
from test_longitudinal_fixture_inputs import _load_case
from test_longitudinal_selection import _case


def _inputs(tmp_path, name="lineage_complete", limits=None):
    case = _case(name)
    validation = _load_case(case, tmp_path)
    selection = _select(case, validation)
    result = ancestry.analyze_selected_lineage(validation, selection=selection, limits=limits)
    return validation, selection, result


def _verify(validation, selection, result):
    ancestry.validate_selected_lineage_result(validation, selection=selection, result=result)


def _forged_roots(result, roots):
    """Forge self-consistent target aggregates while retaining the input signature."""
    certificate = replace(result.certificate, roots=roots)
    targets = []
    for target in result.targets:
        records = tuple(replace(row, external_root_keys=roots[row.record_key]) for row in target.records)
        contributions, count, hhi, effective = ancestry._root_metrics(
            records, len(records), target.grounded_record_count)
        targets.append(replace(target, records=records, root_contributions=contributions,
                               distinct_external_root_count=count, ancestry_concentration_hhi=hhi,
                               effective_external_root_count=effective))
    return replace(result, certificate=certificate, targets=tuple(targets))


@pytest.mark.parametrize("name", ["lineage_complete", "lineage_partial", "lineage_zero_grounded"])
def test_handoff_verification_never_dispatches_analysis(tmp_path, monkeypatch, name):
    validation, selection, result = _inputs(tmp_path, name)
    def forbidden(*args, **kwargs):
        pytest.fail("handoff validation dispatched an analysis kernel")
    for name in ("build_lineage_graph", "analyze_cycles", "analyze_lineage",
                 "analyze_selected_lineage", "_resolve_roots", "_selected_certificate"):
        monkeypatch.setattr(ancestry, name, forbidden)
    monkeypatch.setattr(cycle_module, "analyze_cycles", forbidden)
    monkeypatch.setattr(cycle_module, "_cyclic_components", forbidden)
    _verify(validation, selection, result)


@pytest.mark.parametrize("all_records", [False, True])
def test_same_signature_consistent_wrong_root_derivation_is_rejected(tmp_path, all_records):
    validation, selection, result = _inputs(tmp_path)
    a, b = RecordKey("anchors", "a"), RecordKey("anchors", "b")
    roots = dict(result.certificate.roots)
    for key, values in roots.items():
        if all_records or key.dataset_version == "v2":
            roots[key] = frozenset(b if root == a else a if root == b else root for root in values)
    forged = _forged_roots(result, roots)
    assert forged.input_signature == result.input_signature
    assert forged.targets[1].ancestry_concentration_hhi == result.targets[1].ancestry_concentration_hhi
    with pytest.raises(CanonicalValidationError, match="root anchor|parent contribution"):
        _verify(validation, selection, forged)


def test_target_rows_cannot_disagree_with_verified_context_certificate(tmp_path):
    validation, selection, result = _inputs(tmp_path)
    roots = dict(result.certificate.roots)
    roots[RecordKey("v2", "r1")] = frozenset((RecordKey("anchors", "b"),))
    forged = _forged_roots(result, roots)
    forged = replace(forged, certificate=result.certificate)
    with pytest.raises(CanonicalValidationError, match="target roots"):
        _verify(validation, selection, forged)


def test_self_consistent_depth_offset_is_rejected(tmp_path):
    validation, selection, result = _inputs(tmp_path)
    cycles = result.shared_cycles
    depths = {key: replace(value, lineage_depth=value.lineage_depth + 1)
              for key, value in cycles.depths_by_record.items()}
    altered_cycles = replace(cycles, depths_by_record=depths,
                             lineage_depth=cycles.lineage_depth + 1,
                             maximum_resolved_target_depth=cycles.maximum_resolved_target_depth + 1)
    targets = tuple(replace(target,
        records=tuple(replace(row, lineage_depth=row.lineage_depth + 1) for row in target.records),
        lineage_depth=target.lineage_depth + 1,
        maximum_resolved_target_depth=target.maximum_resolved_target_depth + 1)
        for target in result.targets)
    forged = replace(result, shared_cycles=altered_cycles, targets=targets)
    with pytest.raises(CanonicalValidationError, match="depth contradicts"):
        _verify(validation, selection, forged)


def test_graph_dependency_order_is_verified_from_supplied_ranks(tmp_path):
    validation, selection, result = _inputs(tmp_path)
    ranks = dict(result.certificate.component_ranks)
    first, second = RecordKey("anchors", "a"), RecordKey("v1", "r1")
    ranks[first], ranks[second] = ranks[second], ranks[first]
    forged = replace(result, certificate=replace(result.certificate, component_ranks=ranks))
    with pytest.raises(CanonicalValidationError, match="rank contradicts"):
        _verify(validation, selection, forged)


@pytest.mark.parametrize("field", ["stored_root_membership_count", "root_union_visit_count"])
def test_completed_work_counts_are_checked_against_root_equations(tmp_path, field):
    validation, selection, result = _inputs(tmp_path)
    usage = replace(result.resource_usage, **{field: getattr(result.resource_usage, field) + 1})
    targets = tuple(replace(target, resource_usage=usage) for target in result.targets)
    forged = replace(result, resource_usage=usage, targets=targets)
    with pytest.raises(CanonicalValidationError, match="completed work counters"):
        _verify(validation, selection, forged)


def test_certificate_is_immutable_and_hides_from_representation(tmp_path):
    _, _, result = _inputs(tmp_path)
    with pytest.raises(TypeError):
        result.certificate.roots[RecordKey("anchors", "a")] = frozenset()
    assert "certificate=" not in repr(result)


@pytest.mark.parametrize("field", ["max_root_memberships", "max_root_union_visits"])
def test_root_exhaustion_verifies_without_retaining_partial_root_sets(tmp_path, field):
    validation, selection, result = _inputs(tmp_path, limits=replace(LineageLimits(), **{field: 1}))
    assert result.certificate.roots is result.certificate.reasons is None
    assert all(target.records is None for target in result.targets)
    _verify(validation, selection, result)


@pytest.mark.parametrize("field", ["max_nodes", "max_edges"])
def test_graph_stage_exhaustion_requires_a_real_rejected_admission(tmp_path, field):
    case = _case("lineage_complete")
    validation = _load_case(case, tmp_path)
    selection = _select(case, validation)
    with pytest.raises(LineageResourceLimitError) as caught:
        ancestry.analyze_selected_lineage(validation, selection=selection,
                                         limits=replace(LineageLimits(), **{field: 1}))
    ancestry.validate_lineage_graph_exhaustion(validation, usage=caught.value.resource_usage)
    limits = LineageLimits()
    usage = (LineageResourceUsage(limits.max_nodes, 0, 0, 0, limits, field, limits.max_nodes + 1)
             if field == "max_nodes" else LineageResourceUsage(len(validation.records),
             limits.max_edges, 0, 0, limits, field, limits.max_edges + 1))
    with pytest.raises(CanonicalValidationError):
        ancestry.validate_lineage_graph_exhaustion(validation, usage=usage)


def _cycle_inputs(tmp_path, *, isolated=False):
    case = _case("lineage_complete")
    if isolated:
        source_record = next(row for row in case["records"] if row["dataset_version"] == "anchors")
        source_provenance = next(row for row in case["provenance"] if row["dataset_version"] == "anchors")
        case["records"].append({**source_record, "record_id": "isolated"})
        case["provenance"].append({**source_provenance, "record_id": "isolated", "parent_ids": []})
    for row in case["provenance"]:
        if row["dataset_version"] == "anchors" and row["record_id"] != "isolated":
            row["parent_ids"] = ["anchors::b" if row["record_id"] == "a" else "anchors::a"]
            row["external_grounding"] = "no"
    validation = _load_case(case, tmp_path)
    selection = _select(case, validation)
    result = ancestry.analyze_selected_lineage(validation, selection=selection)
    return validation, selection, result


def test_real_context_cycle_certificate_and_partial_depth_are_accepted(tmp_path):
    validation, selection, result = _cycle_inputs(tmp_path)
    assert result.shared_cycles.cycle_count == 1
    assert result.shared_cycles.affected_record_count == len(validation.records)
    _verify(validation, selection, result)


def test_false_split_cycle_components_are_rejected(tmp_path):
    validation, selection, result = _cycle_inputs(tmp_path)
    first, second = result.shared_cycles.cyclic_components[0]
    altered = replace(result.shared_cycles, cyclic_components=((first,), (second,)),
        component_details=(CycleComponent(1, 1, 0, (first, first), 1, None),
                           CycleComponent(2, 1, 0, (second, second), 1, None)))
    forged = replace(result, shared_cycles=altered)
    with pytest.raises(CanonicalValidationError, match="singleton cycle"):
        _verify(validation, selection, forged)


def test_cycle_witness_requires_actual_parent_edges(tmp_path):
    validation, selection, result = _cycle_inputs(tmp_path)
    first = result.shared_cycles.cyclic_components[0][0]
    detail = replace(result.shared_cycles.component_details[0],
                     witness_record_keys=(first, first), witness_edge_count=1)
    forged = replace(result, shared_cycles=replace(result.shared_cycles, component_details=(detail,)))
    with pytest.raises(CanonicalValidationError, match="witness includes an unsupported edge"):
        _verify(validation, selection, forged)


def test_small_cycle_cannot_claim_a_witness_diagnostic_limit(tmp_path):
    validation, selection, result = _cycle_inputs(tmp_path)
    detail = replace(result.shared_cycles.component_details[0], witness_record_keys=None,
                     witness_edge_count=None, witness_reason="diagnostic_limit")
    forged = replace(result, shared_cycles=replace(result.shared_cycles, component_details=(detail,)))
    with pytest.raises(CanonicalValidationError, match="witness omission"):
        _verify(validation, selection, forged)


def test_cycle_affected_scope_cannot_include_disconnected_context(tmp_path):
    validation, selection, result = _cycle_inputs(tmp_path, isolated=True)
    isolated = RecordKey("anchors", "isolated")
    cycles = result.shared_cycles
    depths = dict(cycles.depths_by_record)
    depths[isolated] = DepthAssessment(None, ("CYCLE_AFFECTED",))
    forged_cycles = replace(cycles,
        affected_record_keys=tuple(sorted(cycles.affected_record_keys + (isolated,))),
        topological_order=tuple(key for key in cycles.topological_order if key != isolated),
        depths_by_record=depths)
    forged = replace(result, shared_cycles=forged_cycles)
    with pytest.raises(CanonicalValidationError, match="affected scope includes an unsupported"):
        _verify(validation, selection, forged)
