"""Step 5 shared lineage, independent target oracles and truthful changes."""
from dataclasses import FrozenInstanceError, replace
from fractions import Fraction
from types import MappingProxyType

import pytest

from recursive_integrity_toolkit.config import RepresentationConfig
from recursive_integrity_toolkit.errors import CanonicalValidationError, LineageResourceLimitError
from recursive_integrity_toolkit.lineage import ancestry
from recursive_integrity_toolkit.lineage.graph import LineageLimits
from recursive_integrity_toolkit.metrics import longitudinal as series
from recursive_integrity_toolkit.models import CalculationEvidenceClass, CalculationStatus
from recursive_integrity_toolkit.result import ExecutionStatus, ReportStatus
from test_longitudinal_analysis import _family, _select
from test_longitudinal_fixture_inputs import HERO, LINEAGE_CASES, _fraction, _hero_validation, _load_case
from test_longitudinal_selection import _case, _declarations
from test_T4_ancestry import _replace_provenance


_DELTA_FIELDS = {
    "distinct_external_root_count_delta": "distinct_external_root_count_delta",
    "ancestry_concentration_hhi_delta": "hhi_delta",
    "effective_external_root_count_delta": "effective_root_count_delta",
    "unresolved_parent_reference_count_delta": "unresolved_parent_references_delta",
    "resolved_parent_edge_coverage_delta": "resolved_reference_coverage_delta",
    "resolved_lineage_coverage_delta": "resolved_lineage_coverage_delta",
    "external_ancestry_coverage_delta": "external_ancestry_coverage_delta",
}
_BOUND_NAMES = ("lineage_closure_lower_bound_delta", "lineage_closure_upper_bound_delta",
                "lineage_closure_interval_width_delta")


def _inputs(tmp_path, name="lineage_complete", *, baseline="none"):
    case = _case(name)
    validation = _load_case(case, tmp_path)
    return case, validation, _select(case, validation, baseline)


def _delta(pair, name):
    return next(item for item in pair.lineage_deltas if item.metric_name == name)


def _check_target(target, expected):
    assert target.scope.target_record_count == expected["N"]
    assert target.population_scope.excluded_record_keys == ()
    assert target.scope.target_record_keys == target.population_scope.included_record_keys
    assert (target.grounded_record_count, target.closed_record_count,
            target.unresolved_record_count) == tuple(expected[key] for key in ("G", "C", "U"))
    assert {str(row.record_key): None if row.external_root_keys is None else
            sorted(map(str, row.external_root_keys)) for row in target.records} == expected["complete_root_sets"]
    for actual, name in ((target.declared_parent_reference_count, "declared_parent_references"),
                         (target.resolved_parent_reference_count, "resolved_parent_references"),
                         (target.unresolved_parent_reference_count, "unresolved_parent_references"),
                         (target.distinct_external_root_count, "distinct_external_root_count")):
        assert actual == expected[name]
    for actual, name in ((target.resolved_parent_edge_coverage, "resolved_reference_coverage"),
                         (target.resolved_lineage_coverage, "resolved_lineage_coverage"),
                         (target.external_ancestry_coverage, "external_ancestry_coverage"),
                         (target.ancestry_concentration_hhi, "hhi"),
                         (target.effective_external_root_count, "effective_root_count")):
        _fraction(actual, expected[name])
    assert target.root_metrics_status.value == expected["root_metrics_status"]
    assert target.concentration_status.value == expected["concentration_status"]
    assert list(target.concentration_reason_codes) == expected["concentration_reason_codes"]
    for contribution in target.root_contributions:
        root = str(contribution.record_key)
        grounded_sets = [roots for roots in expected["complete_root_sets"].values() if roots]
        incidence = sum(root in roots for roots in grounded_sets)
        mass = sum((Fraction(1, len(roots)) for roots in grounded_sets if root in roots), Fraction())
        assert contribution.incidence_count == incidence
        assert contribution.incidence_denominator == expected["N"]
        assert contribution.weight_denominator == expected["G"]
        _fraction(contribution.incidence_share, Fraction(incidence, expected["N"]))
        _fraction(contribution.normalized_weight, mass / expected["G"])


def _check_pairs(result, oracles):
    pairs = {(pair.pair.earlier_version, pair.pair.later_version): pair for pair in result.comparisons}
    snapshots = {row.scope.dataset_version: row for row in result.snapshots}
    for oracle in oracles:
        pair = pairs[oracle["earlier"], oracle["later"]]
        expected = oracle["lineage"]
        assert {item.metric_name for item in pair.lineage_deltas} == set(_DELTA_FIELDS) | set(_BOUND_NAMES)
        for name, key in _DELTA_FIELDS.items():
            _fraction(_delta(pair, name).value, expected[key])
        for name, value in zip(_BOUND_NAMES, expected["lineage_bounds_delta"], strict=True):
            _fraction(_delta(pair, name).value, value)
        assert _delta(pair, "distinct_external_root_count_delta").status.value == expected["root_delta_status"]
        for name in ("ancestry_concentration_hhi_delta", "effective_external_root_count_delta"):
            delta = _delta(pair, name)
            assert delta.status.value == expected["concentration_delta_status"]
            assert set(expected["concentration_delta_reason_codes"]) <= set(delta.reason_codes)
        for delta in pair.lineage_deltas:
            assert delta.formula_id == "F-018"
            assert delta.evidence_class is CalculationEvidenceClass.DERIVED_METRIC
            assert delta.representation is None
            assert delta.earlier_scope == snapshots[oracle["earlier"]].scope.population_scope
            assert delta.later_scope == snapshots[oracle["later"]].scope.population_scope
            assert delta.denominator is None
            assert delta.denominator_reason == "not_applicable_to_difference"
            if delta.value is not None:
                assert delta.value == delta.later_value - delta.earlier_value


@pytest.mark.parametrize("case", LINEAGE_CASES, ids=lambda case: case["case_id"])
@pytest.mark.parametrize("baseline", ["none", "first"])
def test_frozen_lineage_target_and_delta_oracles(case, tmp_path, baseline):
    validation = _load_case(case, tmp_path)
    selection = _select(case, validation, baseline)
    result = series.analyze_longitudinal(validation, selection=selection, lineage=True)
    shared = result.shared_lineage
    assert shared.selected_versions == selection.selected_order
    assert tuple(target.scope.target_dataset_version for target in shared.targets) == selection.selected_order
    for snapshot, target in zip(result.snapshots, shared.targets, strict=True):
        assert snapshot.lineage is target
        assert target.population_scope == snapshot.scope.population_scope
        _check_target(target, case["expected_lineage"][snapshot.scope.dataset_version])
    _check_pairs(result, case["expected_pairs"])
    if baseline == "first":
        first = case["expected_lineage"][selection.selected_order[0]]
        last = case["expected_lineage"][selection.selected_order[-1]]
        pair = result.comparisons[1]
        assert pair.pair.kinds == ("baseline",)
        assert _delta(pair, "distinct_external_root_count_delta").value == (
            last["distinct_external_root_count"] - first["distinct_external_root_count"])
        expected_hhi = None if last["hhi"] is None else Fraction(last["hhi"]) - Fraction(first["hhi"])
        _fraction(_delta(pair, "ancestry_concentration_hhi_delta").value, expected_hhi)
        for name, a, b in zip(_BOUND_NAMES, first["lineage_bounds"], last["lineage_bounds"], strict=True):
            _fraction(_delta(pair, name).value, Fraction(b) - Fraction(a))
    assert shared.shared_graph.scope.target_dataset_version == selection.primary_version
    assert shared.resource_usage.admitted_node_count == len(case["records"])
    assert all(target.resource_usage is shared.resource_usage for target in shared.targets)
    assert result.execution_status is (ExecutionStatus.COMPLETED if case["case_id"] == "lineage_complete"
                                        else ExecutionStatus.PARTIAL)
    ancestry.validate_selected_lineage_result(validation, selection=selection, result=shared)


def test_hero_both_targets_and_all_lineage_changes_match_independent_oracle():
    validation = _hero_validation("v2")
    config = RepresentationConfig(name="topic", source="topic_field", field="topic",
                                  version="hero-topic-v1", missing_value_policy="exclude")
    declarations = tuple(series.SnapshotDeclaration(version, config, "Hero literal topics") for version in ("v1", "v2"))
    selection = series.select_longitudinal_versions(validation, declarations=declarations)
    result = series.analyze_longitudinal(validation, selection=selection, lineage=True)
    for snapshot in result.snapshots:
        _check_target(snapshot.lineage, HERO["expected_lineage"][snapshot.scope.dataset_version])
    _check_pairs(result, HERO["expected_pairs"])
    assert result.execution_status is ExecutionStatus.COMPLETED


@pytest.mark.parametrize("baseline", ["none", "first"])
def test_graph_cycles_and_root_propagation_execute_once_for_all_targets(tmp_path, monkeypatch, baseline):
    _, validation, selection = _inputs(tmp_path, baseline=baseline)
    calls = []
    for name in ("build_lineage_graph", "analyze_cycles", "_resolve_roots"):
        original = getattr(ancestry, name)
        def counted(*args, _name=name, _original=original, **kwargs):
            calls.append(_name)
            return _original(*args, **kwargs)
        monkeypatch.setattr(ancestry, name, counted)
    def forbidden(*args, **kwargs):
        pytest.fail("selected lineage dispatched a primary-only analysis per target")
    monkeypatch.setattr(ancestry, "analyze_lineage", forbidden)
    result = series.analyze_longitudinal(validation, selection=selection, lineage=True)
    assert calls == ["build_lineage_graph", "analyze_cycles", "_resolve_roots"]
    assert len(result.shared_lineage.targets) == 3


def test_lineage_requires_explicit_opt_in(tmp_path, monkeypatch):
    _, validation, selection = _inputs(tmp_path)
    def forbidden(*args, **kwargs):
        pytest.fail("ordinary longitudinal analysis executed lineage")
    monkeypatch.setattr(ancestry, "analyze_selected_lineage", forbidden)
    monkeypatch.setattr(ancestry, "build_lineage_graph", forbidden)
    result = series.analyze_longitudinal(validation, selection=selection)
    assert result.shared_lineage is None
    for snapshot in result.snapshots:
        assert snapshot.lineage is None
        assert _family(snapshot, "lineage").execution_status is ExecutionStatus.NOT_REQUESTED
    for pair in result.comparisons:
        assert pair.lineage_deltas == ()
        assert _family(pair, "lineage").execution_status is ExecutionStatus.NOT_REQUESTED


@pytest.mark.parametrize("version", ["v1", "anchors"])
def test_legacy_api_keeps_primary_only_target_guard(tmp_path, version):
    _, validation, selection = _inputs(tmp_path)
    with pytest.raises(CanonicalValidationError):
        ancestry.analyze_lineage(validation, target_dataset_version=version)
    assert ancestry.analyze_selected_lineage(validation, selection=selection).selected_versions == ("v1", "v2", "v3")


def test_representation_exclusion_never_removes_lineage_targets(tmp_path):
    case = _case("lineage_complete")
    for row in case["records"]:
        if row["dataset_version"] == "v2":
            row["topic"] = None
    validation = _load_case(case, tmp_path)
    result = series.analyze_longitudinal(validation, selection=_select(case, validation), lineage=True)
    snapshot = result.snapshots[1]
    assert snapshot.representation_eligible_record_count.value == 0
    assert snapshot.record_count.value == snapshot.lineage.grounded_record_count == 4
    assert snapshot.lineage.scope.target_record_count == 4
    assert snapshot.lineage.ancestry_concentration_hhi == 1
    assert _delta(result.comparisons[0], "ancestry_concentration_hhi_delta").value == 1/2


def test_representation_block_preserves_targets_but_blocks_every_lineage_delta(tmp_path):
    case = _case("lineage_complete")
    declarations = _declarations(case)
    declarations = (declarations[0], replace(declarations[1], state_semantics="different meanings"), declarations[2])
    validation = _load_case(case, tmp_path)
    selection = _select(case, validation, baseline="first", declarations=declarations)
    result = series.analyze_longitudinal(validation, selection=selection, lineage=True)
    assert all(snapshot.lineage.records for snapshot in result.snapshots)
    assert result.comparisons[1].pair.earlier_version == "v1"
    assert result.comparisons[1].pair.later_version == "v3"
    assert _delta(result.comparisons[1], "distinct_external_root_count_delta").value == 0
    for pair in (result.comparisons[0], result.comparisons[2]):
        assert all(delta.value is None and delta.status is ReportStatus.UNAVAILABLE for delta in pair.lineage_deltas)
        assert all("R_LONGITUDINAL_PAIR_BLOCKED" in delta.reason_codes for delta in pair.lineage_deltas)


def test_context_anchor_inventory_does_not_become_target_root_count(tmp_path):
    case = _case("lineage_complete")
    case["records"].append(dict(case["records"][0], record_id="unused"))
    case["provenance"].append(dict(case["provenance"][0], record_id="unused"))
    case["order_document"]["version_order"].insert(0, "unloaded")
    validation = _load_case(case, tmp_path)
    selected = ancestry.analyze_selected_lineage(validation, selection=_select(case, validation))
    assert selected.selected_versions == ("v1", "v2", "v3")
    assert selected.resource_usage.admitted_node_count == 13
    assert [target.scope.target_record_count for target in selected.targets] == [4, 4, 2]
    assert [target.distinct_external_root_count for target in selected.targets] == [2, 1, 2]
    assert all(root.record_key.record_id != "unused" for target in selected.targets for root in target.root_contributions)
    assert all(key.dataset_version != "unloaded" for key in selected.shared_graph.node_keys)


def test_identified_empty_snapshot_keeps_zero_population_and_null_concentration(tmp_path):
    case, validation, selection = _inputs(tmp_path, "identified_empty_later")
    result = series.analyze_longitudinal(validation, selection=selection, lineage=True)
    target = result.snapshots[-1].lineage
    assert target.scope.target_record_count == 0
    assert target.records == ()
    assert target.population_scope.included_record_keys == ()
    assert target.grounded_record_count == target.closed_record_count == target.unresolved_record_count == 0
    assert target.distinct_external_root_count == 0
    assert target.ancestry_concentration_hhi is target.effective_external_root_count is None
    assert target.resolved_lineage_coverage is target.external_ancestry_coverage is None
    assert "EMPTY_TARGET_SCOPE" in target.ancestry_coverage_reason_codes
    assert case["selected_versions"][-1] not in validation.version_order.loaded_versions
    for name in (*_BOUND_NAMES, "ancestry_concentration_hhi_delta", "resolved_lineage_coverage_delta"):
        assert _delta(result.comparisons[0], name).value is None


@pytest.mark.parametrize("limit", ["max_root_memberships", "max_root_union_visits"])
def test_shared_root_budget_abort_removes_all_target_root_values_but_keeps_references(tmp_path, limit):
    _, validation, selection = _inputs(tmp_path)
    limits = replace(LineageLimits(), **{limit: 1})
    result = series.analyze_longitudinal(validation, selection=selection, lineage=True, lineage_limits=limits)
    shared = result.shared_lineage
    assert shared.resource_usage.exhausted_limit == limit
    assert shared.resource_usage.attempted_value == 2
    assert shared.execution_status is ExecutionStatus.FAILED
    for target in shared.targets:
        assert target.resource_usage is shared.resource_usage
        assert target.records is target.root_contributions is None
        assert target.grounded_record_count is target.closed_record_count is target.unresolved_record_count is None
        assert target.distinct_external_root_count is target.ancestry_concentration_hhi is target.effective_external_root_count is None
        assert target.resolved_lineage_coverage is target.external_ancestry_coverage is None
        assert target.resolved_parent_reference_count == target.scope.target_record_count
        assert target.resolved_parent_edge_coverage == 1
    assert result.execution_status is ExecutionStatus.PARTIAL
    assert all(snapshot.distribution.unweighted.status is CalculationStatus.AVAILABLE for snapshot in result.snapshots)
    assert all(snapshot.provenance is not None and snapshot.direct_closure is not None for snapshot in result.snapshots)
    for pair in result.comparisons:
        assert _delta(pair, "distinct_external_root_count_delta").value is None
        assert _delta(pair, "unresolved_parent_reference_count_delta").value == 0
        assert _delta(pair, "resolved_parent_edge_coverage_delta").value == 0


@pytest.mark.parametrize("limit", ["max_nodes", "max_edges"])
def test_graph_admission_failure_is_typed_and_coordinator_preserves_other_families(tmp_path, limit):
    _, validation, selection = _inputs(tmp_path)
    limits = replace(LineageLimits(), **{limit: 1})
    with pytest.raises(LineageResourceLimitError):
        ancestry.analyze_selected_lineage(validation, selection=selection, limits=limits)
    result = series.analyze_longitudinal(validation, selection=selection, lineage=True, lineage_limits=limits)
    assert result.shared_lineage is None
    assert result.execution_status is ExecutionStatus.PARTIAL
    assert any(message.code == "E_LINEAGE_RESOURCE_LIMIT_EXCEEDED" for message in result.messages)
    for snapshot in result.snapshots:
        assert snapshot.lineage is None
        assert snapshot.distribution.unweighted.status is CalculationStatus.AVAILABLE
        assert snapshot.provenance.analyzed_record_count.value == snapshot.record_count.value
        assert _family(snapshot, "lineage").execution_status is ExecutionStatus.FAILED
    for pair in result.comparisons:
        assert all(delta.value is None for delta in pair.lineage_deltas)
        coverage = _delta(pair, "resolved_lineage_coverage_delta")
        assert coverage.earlier_denominator == len(coverage.earlier_scope.included_record_keys)
        assert coverage.later_denominator == len(coverage.later_scope.included_record_keys)
        assert _delta(pair, "ancestry_concentration_hhi_delta").earlier_denominator is None
        assert _delta(pair, "resolved_parent_edge_coverage_delta").earlier_denominator is None


def test_disconnected_context_cycle_retains_error_without_corrupting_exact_targets(tmp_path):
    case = _case("lineage_complete")
    case["context_versions"].append("cycle_context")
    case["order_document"]["version_order"].insert(1, "cycle_context")
    for record_id, parent in (("x", "y"), ("y", "x")):
        case["records"].append(dict(case["records"][0], dataset_version="cycle_context", record_id=record_id))
        case["provenance"].append(dict(case["provenance"][0], dataset_version="cycle_context",
                                       record_id=record_id, external_grounding="no", parent_ids=[parent]))
    validation = _load_case(case, tmp_path)
    result = series.analyze_longitudinal(validation, selection=_select(case, validation), lineage=True)
    shared = result.shared_lineage
    assert shared.execution_status is ExecutionStatus.PARTIAL
    assert any("CYCLE" in message.code for message in shared.messages)
    assert result.execution_status is ExecutionStatus.PARTIAL
    for target in shared.targets:
        _check_target(target, case["expected_lineage"][target.scope.target_dataset_version])
        assert target.execution_status is ExecutionStatus.PARTIAL


def test_missing_provenance_preserves_unresolved_roots_and_known_other_declarations(tmp_path):
    case = _case("lineage_complete")
    case["provenance"] = [row for row in case["provenance"]
                          if (row["dataset_version"], row["record_id"]) != ("v2", "r1")]
    validation = _load_case(case, tmp_path)
    result = series.analyze_longitudinal(validation, selection=_select(case, validation), lineage=True)
    target = result.snapshots[1].lineage
    assert target.declared_parent_reference_count == target.resolved_parent_reference_count == 3
    assert target.unresolved_parent_reference_count == 0
    assert target.resolved_parent_edge_coverage == 1
    assert not target.no_declared_parents
    assert target.reference_coverage_reason_codes == ()
    assert target.unresolved_record_count == 1
    assert target.grounded_record_count == 3
    assert target.ancestry_concentration_hhi == 1
    assert _delta(result.comparisons[0], "unresolved_parent_reference_count_delta").value == 0


def test_malformed_parent_declaration_fails_selection_before_graph_execution(tmp_path, monkeypatch):
    case, validation, _ = _inputs(tmp_path)
    rows = tuple(replace(row, values=MappingProxyType({**row.values, "parent_ids": "malformed-list"}))
                 if str(row.record_key) == "v2::r1" else row for row in validation.provenance)
    validation = _replace_provenance(validation, rows)
    def forbidden(*args, **kwargs):
        pytest.fail("malformed selected provenance reached graph construction")
    monkeypatch.setattr(ancestry, "build_lineage_graph", forbidden)
    with pytest.raises(CanonicalValidationError) as error:
        ancestry.analyze_selected_lineage(validation, selection=_select(case, validation))
    assert error.value.code.value == "E_PARENT_FORMAT"


def test_same_parent_aliases_count_as_declarations_without_duplicate_edges(tmp_path):
    case = _case("lineage_complete")
    row = next(row for row in case["provenance"] if (row["dataset_version"], row["record_id"]) == ("v1", "r1"))
    row["parent_ids"] = ["anchors::a", "anchors::a"]
    validation = _load_case(case, tmp_path)
    shared = ancestry.analyze_selected_lineage(validation, selection=_select(case, validation))
    target = shared.targets[0]
    assert target.declared_parent_reference_count == target.resolved_parent_reference_count == 5
    assert target.unresolved_parent_reference_count == 0
    assert target.ancestry_concentration_hhi == 1/2
    assert shared.resource_usage.admitted_edge_count == 10


@pytest.mark.parametrize("change", ["parent", "context", "selection"])
def test_stale_same_identity_or_selected_basis_cannot_reuse_shared_handoff(tmp_path, change):
    case, validation, selection = _inputs(tmp_path)
    shared = ancestry.analyze_selected_lineage(validation, selection=selection)
    if change == "parent":
        row = next(row for row in case["provenance"] if (row["dataset_version"], row["record_id"]) == ("v1", "r1"))
        row["parent_ids"] = ["anchors::b"]
    elif change == "context":
        case["provenance"][0]["external_grounding"] = "no"
    changed = _load_case(case, tmp_path)
    declarations = _declarations(case)
    if change == "selection":
        declarations = tuple(replace(item, state_semantics="new declared meaning") for item in declarations)
    changed_selection = _select(case, changed, declarations=declarations)
    with pytest.raises(CanonicalValidationError):
        ancestry.validate_selected_lineage_result(changed, selection=changed_selection, result=shared)


def test_shared_signature_binds_limits_even_when_both_runs_complete(tmp_path):
    _, validation, selection = _inputs(tmp_path)
    first = ancestry.analyze_selected_lineage(validation, selection=selection)
    second = ancestry.analyze_selected_lineage(validation, selection=selection,
        limits=replace(LineageLimits(), max_root_union_visits=20000000))
    assert first.input_signature != second.input_signature
    assert [target.records for target in first.targets] == [target.records for target in second.targets]


def test_public_handoff_is_immutable_and_rejects_shrunken_target_selection(tmp_path):
    _, validation, selection = _inputs(tmp_path)
    shared = ancestry.analyze_selected_lineage(validation, selection=selection)
    with pytest.raises(FrozenInstanceError):
        shared.selected_versions = ("v3",)
    with pytest.raises(FrozenInstanceError):
        shared.targets[0].grounded_record_count = 0
    with pytest.raises(CanonicalValidationError):
        replace(shared, targets=shared.targets[1:])


def test_row_order_changes_preserve_shared_evidence_and_signature(tmp_path):
    case, validation, selection = _inputs(tmp_path)
    first = ancestry.analyze_selected_lineage(validation, selection=selection)
    case["records"].reverse()
    case["provenance"].reverse()
    reordered = _load_case(case, tmp_path)
    second = ancestry.analyze_selected_lineage(reordered, selection=_select(case, reordered, baseline="none"))
    assert first.input_signature == second.input_signature
    assert first.targets == second.targets
    assert first.resource_usage == second.resource_usage


def test_partial_concentration_retains_grounded_and_population_denominators(tmp_path):
    _, validation, selection = _inputs(tmp_path, "lineage_partial")
    result = series.analyze_longitudinal(validation, selection=selection, lineage=True)
    pair = result.comparisons[-1]
    concentration = _delta(pair, "ancestry_concentration_hhi_delta")
    assert concentration.status is ReportStatus.PARTIAL
    assert (concentration.earlier_denominator, concentration.later_denominator) == (4, 2)
    assert "R_LONGITUDINAL_PARTIAL_COVERAGE" in concentration.reason_codes
    assert concentration.owner_id == "T4" and concentration.unit == "ratio"
    coverage = _delta(pair, "resolved_lineage_coverage_delta")
    assert (coverage.earlier_denominator, coverage.later_denominator) == (4, 3)
    reference = _delta(pair, "resolved_parent_edge_coverage_delta")
    assert (reference.earlier_denominator, reference.later_denominator) == (4, 3)
    assert reference.owner_id == "PR-008"
    bounds = _delta(pair, "lineage_closure_upper_bound_delta")
    assert (bounds.earlier_denominator, bounds.later_denominator) == (4, 3)
    assert bounds.owner_id == "T3" and bounds.unit == "ratio"


def test_multi_root_fractional_allocation_and_direct_bounds_stay_independent(tmp_path):
    case = _case("lineage_complete")
    row = next(row for row in case["provenance"] if (row["dataset_version"], row["record_id"]) == ("v3", "r1"))
    row["parent_ids"] = ["anchors::a", "anchors::b"]
    validation = _load_case(case, tmp_path)
    selection = _select(case, validation)
    ordinary = series.analyze_longitudinal(validation, selection=selection)
    result = series.analyze_longitudinal(validation, selection=selection, lineage=True)
    target = result.snapshots[-1].lineage
    roots = {str(item.record_key): item for item in target.root_contributions}
    assert roots["anchors::a"].normalized_weight == 1/4
    assert roots["anchors::b"].normalized_weight == 3/4
    assert roots["anchors::a"].incidence_share == 1/2
    assert roots["anchors::b"].incidence_share == 1
    assert target.ancestry_concentration_hhi == 5/8
    assert target.effective_external_root_count == 8/5
    for before, after in zip(ordinary.snapshots, result.snapshots, strict=True):
        assert before.provenance == after.provenance
        assert before.direct_closure == after.direct_closure
    assert result.snapshots[-1].direct_closure.lower_bound.value == 1
    assert _delta(result.comparisons[-1], "lineage_closure_lower_bound_delta").value == 0


@pytest.mark.parametrize("limit,maximum", [("max_nodes", 11), ("max_edges", 9),
                                          ("max_root_memberships", 11), ("max_root_union_visits", 9)])
def test_limits_apply_to_combined_graph_work_not_individual_targets(tmp_path, limit, maximum):
    _, validation, selection = _inputs(tmp_path)
    limits = replace(LineageLimits(), **{limit: maximum})
    if limit in ("max_nodes", "max_edges"):
        with pytest.raises(LineageResourceLimitError) as error:
            ancestry.analyze_selected_lineage(validation, selection=selection, limits=limits)
        usage = error.value.resource_usage
    else:
        result = ancestry.analyze_selected_lineage(validation, selection=selection, limits=limits)
        assert all(target.records is None for target in result.targets)
        usage = result.resource_usage
    assert usage.exhausted_limit == limit
    assert usage.attempted_value == maximum + 1


def test_later_selected_parent_stays_invalid_under_retained_chronology(tmp_path):
    case = _case("lineage_complete")
    row = next(row for row in case["provenance"] if (row["dataset_version"], row["record_id"]) == ("v1", "r1"))
    row["parent_ids"] = ["v2::r1"]
    validation = _load_case(case, tmp_path)
    shared = ancestry.analyze_selected_lineage(validation, selection=_select(case, validation))
    target = shared.targets[0]
    record = next(record for record in target.records if record.record_key.record_id == "r1")
    assert record.external_root_keys is None
    assert record.classification == "unresolved"
    assert target.unresolved_parent_reference_count == 1
    assert shared.execution_status is ExecutionStatus.PARTIAL
    assert any(message.code == "E_PARENT_FUTURE_VERSION" for message in shared.messages)


def test_handoff_validation_does_not_rerun_graph_algorithms(tmp_path, monkeypatch):
    _, validation, selection = _inputs(tmp_path)
    result = ancestry.analyze_selected_lineage(validation, selection=selection)
    def forbidden(*args, **kwargs):
        pytest.fail("handoff binding reran a graph algorithm")
    for name in ("build_lineage_graph", "analyze_cycles", "_resolve_roots"):
        monkeypatch.setattr(ancestry, name, forbidden)
    ancestry.validate_selected_lineage_result(validation, selection=selection, result=result)


def test_zero_declared_reference_coverage_retains_its_explicit_convention(tmp_path):
    _, validation, selection = _inputs(tmp_path, "lineage_zero_grounded")
    result = series.analyze_longitudinal(validation, selection=selection, lineage=True)
    target = result.snapshots[-1].lineage
    assert target.no_declared_parents and target.declared_parent_reference_count == 0
    assert target.resolved_parent_edge_coverage == 1
    delta = _delta(result.comparisons[-1], "resolved_parent_edge_coverage_delta")
    assert (delta.earlier_denominator, delta.later_denominator) == (4, 0)
    assert delta.earlier_no_declared_parents is False
    assert delta.later_no_declared_parents is True
    assert delta.value == 0 and delta.status is ReportStatus.AVAILABLE
    concentration = _delta(result.comparisons[-1], "ancestry_concentration_hhi_delta")
    assert concentration.later_denominator == 0
    assert concentration.later_value is concentration.value is None
    assert concentration.later_reason_codes == ("NO_RESOLVED_EXTERNAL_ROOTS",)
    assert "LATER_NO_RESOLVED_EXTERNAL_ROOTS" in concentration.reason_codes


@pytest.mark.parametrize("options", [{"lineage": 1}, {"lineage": "true"},
    {"lineage": True, "lineage_limits": True}, {"lineage": True, "lineage_limits": {}},
    {"lineage": False, "lineage_limits": LineageLimits()}])
def test_invalid_lineage_requests_fail_before_graph_or_distribution(tmp_path, monkeypatch, options):
    _, validation, selection = _inputs(tmp_path)
    def forbidden(*args, **kwargs):
        pytest.fail("invalid lineage options reached analytical execution")
    monkeypatch.setattr(ancestry, "build_lineage_graph", forbidden)
    monkeypatch.setattr(series, "calculate_state_distribution", forbidden)
    with pytest.raises(CanonicalValidationError):
        series.analyze_longitudinal(validation, selection=selection, **options)


@pytest.mark.parametrize("tamper", ["promote_partial", "grounded_denominator", "zero_concentration"])
def test_result_rejects_lineage_delta_semantics_changed_after_computation(tmp_path, tamper):
    name = "lineage_zero_grounded" if tamper == "zero_concentration" else "lineage_partial"
    _, validation, selection = _inputs(tmp_path, name)
    result = series.analyze_longitudinal(validation, selection=selection, lineage=True)
    pair = result.comparisons[-1]
    delta = _delta(pair, "ancestry_concentration_hhi_delta")
    if tamper == "promote_partial":
        changed = replace(delta, status=ReportStatus.AVAILABLE, reason_codes=(),
                          earlier_status=ReportStatus.AVAILABLE, earlier_reason_codes=(),
                          later_status=ReportStatus.AVAILABLE, later_reason_codes=())
    elif tamper == "grounded_denominator":
        changed = replace(delta, later_denominator=3)
    else:
        changed = replace(delta, later_value=0, value=-delta.earlier_value,
                          status=ReportStatus.AVAILABLE, reason_codes=(),
                          later_status=ReportStatus.AVAILABLE, later_reason_codes=())
    deltas = tuple(changed if item.metric_name == delta.metric_name else item for item in pair.lineage_deltas)
    forged_pair = replace(pair, lineage_deltas=deltas)
    with pytest.raises(CanonicalValidationError):
        replace(result, comparisons=(*result.comparisons[:-1], forged_pair))
