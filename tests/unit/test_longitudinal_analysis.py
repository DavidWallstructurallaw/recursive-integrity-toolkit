"""Independent Step 3 observations, unavailable gaps and owner-kernel reuse."""
from dataclasses import FrozenInstanceError, replace
from fractions import Fraction
import json

import pytest

from recursive_integrity_toolkit.config import RepresentationConfig
from recursive_integrity_toolkit.errors import CanonicalValidationError, ErrorCode
from recursive_integrity_toolkit.io.validation import validate_bundle
from recursive_integrity_toolkit.metrics import longitudinal as series
from recursive_integrity_toolkit.metrics.diversity import compare_support
from recursive_integrity_toolkit.models import (
    AuditBundle, CalculationEvidenceClass, CalculationReason, CalculationStatus,
    ContentMode, ExplicitPairContext, FileRole, InputSource, NormalizationOptions,
    TailSelectionOptions,
)
from recursive_integrity_toolkit.result import ExecutionStatus
from test_longitudinal_fixture_inputs import DISTRIBUTION_CASES, _fraction, _load_case
from test_longitudinal_selection import _case, _declarations, _mapping


def _select(case, validation, baseline="first", declarations=None, mappings=None):
    declarations = _declarations(case) if declarations is None else declarations
    if mappings is None:
        mappings = (_mapping(declarations),) if case["case_id"] == "directed_many_to_one" else ()
    return series.select_longitudinal_versions(validation, declarations=declarations,
                                               baseline=baseline, mappings=mappings)


def _delta(pair, name):
    return next(item for item in pair.deltas if item.metric_name == name)


def _family(item, name):
    return next(family for family in item.family_statuses if family.family == name)


def _analyze(case, tmp_path, *, tail=True, baseline="first"):
    validation = _load_case(case, tmp_path)
    selection = _select(case, validation, baseline)
    return validation, series.analyze_longitudinal(validation, selection=selection,
        tail_options=TailSelectionOptions("singleton_count") if tail else None)


@pytest.mark.parametrize("case", [case for case in DISTRIBUTION_CASES if case["case_id"] != "missing_order"],
                         ids=lambda case: case["case_id"])
@pytest.mark.parametrize("tail", [False, True])
def test_frozen_snapshot_and_pair_oracles(case, tmp_path, tail):
    validation, result = _analyze(case, tmp_path, tail=tail)
    assert tuple(item.scope.dataset_version for item in result.snapshots) == tuple(case["selected_versions"])
    assert all(snapshot.scope.representation_scope is not None for snapshot in result.snapshots)
    for snapshot in result.snapshots:
        expected = case["expected_snapshots"][snapshot.scope.dataset_version]
        actual = snapshot.distribution.unweighted
        assert snapshot.record_count.value == expected["record_count"]
        assert snapshot.representation_eligible_record_count.value == expected["eligible_count"]
        assert snapshot.representation_excluded_record_count.value == expected["excluded_count"]
        assert snapshot.distribution.coverage.denominator == expected["record_count"]
        assert actual.support_size.value == expected["support_size"]
        _fraction(actual.gini_simpson_diversity.value, expected["diversity"])
        assert {state.state_id: state.state_count for state in actual.states} == expected["state_counts"]
        assert actual.status.value == expected["status"]
        assert list(actual.reason_codes) == expected["reason_codes"]
        assert snapshot.record_count.metadata.evidence_class is CalculationEvidenceClass.OBSERVED_FACT
        assert snapshot.record_count.metadata.method == "PR-002.record_count"
    pairs = {(pair.pair.earlier_version, pair.pair.later_version): pair for pair in result.comparisons}
    for oracle in case["expected_pairs"]:
        pair = pairs[oracle["earlier"], oracle["later"]]
        if "expected_pair_error" in oracle:
            assert pair.compatibility is None and pair.support_comparison is None
            assert all(delta.value is None for delta in pair.deltas)
            assert oracle["expected_pair_error"] in {message.code for message in pair.messages}
            continue
        expected = oracle["distribution"]
        assert _delta(pair, "record_count_delta").value == expected["record_count_delta"]
        assert _delta(pair, "support_delta").value == expected["support_delta"]
        _fraction(_delta(pair, "gini_simpson_diversity_delta").value, expected["diversity_delta"])
        comparison = pair.support_comparison
        for name, key in (("extinct_states", "missing_states"), ("added_states", "added_states"),
                          ("retained_states", "retained_states")):
            actual = None if comparison is None else getattr(comparison, name)
            assert (None if actual is None else list(actual)) == expected[key]
        if comparison is not None:
            _fraction(comparison.support_retention_ratio.value, expected["support_retention"])
            assert comparison.support_loss_count.value == len(expected["missing_states"])
            assert comparison.support_added_count.value == len(expected["added_states"])
        assert _delta(pair, "support_delta").formula_id == "F-005"
        assert _delta(pair, "gini_simpson_diversity_delta").formula_id == "F-018"
        if tail:
            observed = pair.tail_disappearance
            actual = observed.tail_extinct_states
            assert (None if actual is None else list(actual)) == expected["tail_extinct_states"]
            assert observed.tail_extinction_count == (None if actual is None else len(actual))
        else:
            assert pair.tail_disappearance is None
            assert _family(pair, "tail").execution_status is ExecutionStatus.NOT_REQUESTED
    assert result.selection.version_order.loaded_versions == validation.version_order.loaded_versions
    incomplete = case["case_id"] in ("incompatible_middle", "all_excluded_later", "identified_empty_later")
    assert result.execution_status is (ExecutionStatus.PARTIAL if incomplete else ExecutionStatus.COMPLETED)
    assert "R_LONGITUDINAL_FAMILIES_DEFERRED" not in result.reason_codes
    for item in (*result.snapshots, *result.comparisons):
        assert _family(item, "provenance").execution_status is not ExecutionStatus.DEFERRED
        assert _family(item, "direct_closure").execution_status is not ExecutionStatus.DEFERRED
        assert _family(item, "lineage").execution_status is ExecutionStatus.NOT_REQUESTED


def test_reappearance_and_baseline_preserve_intermediate_observations(tmp_path):
    _, result = _analyze(_case(), tmp_path)
    first, baseline, last = result.comparisons
    assert first.support_comparison.extinct_states == ("B", "C")
    assert last.support_comparison.added_states == ("B",)
    assert baseline.support_comparison.extinct_states == ("C",)
    assert _delta(baseline, "support_delta").value == 0
    assert _delta(last, "record_count_delta").value == -1


@pytest.mark.parametrize("baseline,expected", [("none", 2), ("first", 3)])
def test_distribution_once_per_snapshot_and_pair_once_per_schedule(tmp_path, monkeypatch, baseline, expected):
    case = _case()
    validation = _load_case(case, tmp_path)
    selection = _select(case, validation, baseline)
    calls, sizes = [], []
    assign, calculate, compare = series.assign_field_states, series.calculate_state_distribution, series.compare_support
    def assignment(records, **kwargs):
        sizes.append(len(records))
        assert {row.record_key.dataset_version for row in records} == set(kwargs["dataset_versions"])
        return assign(records, **kwargs)
    def distribution(*args, **kwargs):
        calls.append("distribution")
        return calculate(*args, **kwargs)
    def pair(*args, **kwargs):
        calls.append("pair")
        return compare(*args, **kwargs)
    monkeypatch.setattr(series, "assign_field_states", assignment)
    monkeypatch.setattr(series, "calculate_state_distribution", distribution)
    monkeypatch.setattr(series, "compare_support", pair)
    result = series.analyze_longitudinal(validation, selection=selection)
    assert sizes == [4, 4, 3] and calls.count("distribution") == 3 and calls.count("pair") == expected
    assert len(result.comparisons) == expected


@pytest.mark.parametrize("case_name", ["identified_empty_later", "all_excluded_later"])
def test_unavailable_evidence_does_not_execute_numerical_pair_or_imply_extinction(tmp_path, monkeypatch, case_name):
    case = _case(case_name)
    validation = _load_case(case, tmp_path)
    selection = _select(case, validation)
    def forbidden(*args, **kwargs):
        pytest.fail("unavailable distribution reached numerical pair or tail selection")
    monkeypatch.setattr(series, "compare_support", forbidden)
    monkeypatch.setattr(series, "select_tail", forbidden)
    result = series.analyze_longitudinal(validation, selection=selection, tail_options=TailSelectionOptions("singleton_count"))
    pair = result.comparisons[0]
    assert _delta(pair, "record_count_delta").status is CalculationStatus.AVAILABLE
    assert _delta(pair, "support_delta").value is None
    assert _delta(pair, "support_delta").later_reason_codes
    assert pair.support_comparison is None and pair.tail_disappearance.tail_extinct_states is None
    assert _family(pair, "distribution").execution_status is ExecutionStatus.PARTIAL


def test_exclusion_changes_representation_denominator_only(tmp_path):
    case = _case()
    case["records"][0]["topic"] = None
    validation, result = _analyze(case, tmp_path)
    earlier = result.snapshots[0]
    assert earlier.record_count.value == 4
    assert earlier.distribution.coverage.numerator == 3
    assert earlier.distribution.coverage.denominator == 4
    first = result.comparisons[0]
    count, diversity = _delta(first, "record_count_delta"), _delta(first, "gini_simpson_diversity_delta")
    assert count.value == 0 and count.earlier_value == count.later_value == 4
    assert count.denominator is None and count.representation is None
    assert diversity.earlier_denominator == 3 and diversity.later_denominator == 4
    assert diversity.earlier_coverage.ratio == 3/4
    assert diversity.denominator is None and diversity.denominator_reason == "not_applicable_to_difference"
    assert first.tail_disappearance.earlier_sample_size == 3
    assert count.earlier_scope is earlier.scope.population_scope
    assert count.later_scope is result.snapshots[1].scope.population_scope


@pytest.mark.parametrize("mode", ["missing_column", "error_policy", "marker_collision"])
def test_failed_assignment_preserves_other_snapshots_and_record_deltas(tmp_path, mode):
    case = _case()
    declarations = _declarations(case)
    for row in case["records"]:
        if row["dataset_version"] == "v2":
            if mode == "missing_column":
                row.pop("topic")
            else:
                row["topic"] = None if mode == "error_policy" else "MISSING"
    if mode != "missing_column":
        declarations = tuple(replace(d, representation=replace(d.representation,
            missing_value_policy="error" if mode == "error_policy" else "explicit_missing_state"),
            missing_state_id=None if mode == "error_policy" else "MISSING") for d in declarations)
    validation = _load_case(case, tmp_path)
    selection = _select(case, validation, declarations=declarations)
    result = series.analyze_longitudinal(validation, selection=selection)
    assert result.snapshots[1].distribution is None
    assert result.snapshots[1].scope.representation_scope is None
    assert result.snapshots[1].representation_eligible_record_count.value is None
    assert result.snapshots[1].record_count.value == 4
    assert result.snapshots[0].distribution and result.snapshots[2].distribution
    assert result.comparisons[1].support_comparison.status is CalculationStatus.AVAILABLE
    assert _delta(result.comparisons[0], "record_count_delta").value == 0
    assert result.snapshots[1].messages


def test_incompatible_all_pairs_fails_without_losing_single_version_observations(tmp_path):
    validation, result = _analyze(_case("incompatible_middle"), tmp_path, baseline="none")
    assert result.execution_status is ExecutionStatus.FAILED
    assert all(s.distribution.unweighted.status is CalculationStatus.AVAILABLE for s in result.snapshots)
    assert all(_delta(p, "record_count_delta").value is None for p in result.comparisons)
    assert "R_LONGITUDINAL_PAIR_BLOCKED" in result.reason_codes


@pytest.mark.parametrize("direction", ["earlier_to_later", "later_to_earlier"])
def test_mapped_pairs_equal_legacy_kernel_and_preserve_original_distributions(tmp_path, direction):
    case = _case("directed_many_to_one")
    if direction == "later_to_earlier":
        for row in (*case["records"], *case["provenance"]):
            row["dataset_version"] = "v2" if row["dataset_version"] == "v1" else "v1"
        case["representations"]["v1"], case["representations"]["v2"] = case["representations"]["v2"], case["representations"]["v1"]
    validation = _load_case(case, tmp_path)
    declarations = _declarations(case)
    supplied = _mapping(declarations, direction=direction)
    selection = _select(case, validation, declarations=declarations, mappings=(supplied,))
    result = series.analyze_longitudinal(validation, selection=selection, tail_options=TailSelectionOptions("singleton_count"))
    a, b = (s.distribution.unweighted for s in result.snapshots)
    legacy = compare_support(a, b, context=ExplicitPairContext(a.scope, b.scope, a.representation,
        b.representation, selection.version_order), earlier_state_semantics=declarations[0].state_semantics,
        later_state_semantics=declarations[1].state_semantics, state_mapping=supplied.declaration)
    assert result.comparisons[0].support_comparison == legacy
    assert (a.support_size.value, b.support_size.value) == ((3, 2) if direction == "earlier_to_later" else (2, 3))
    assert _delta(result.comparisons[0], "gini_simpson_diversity_delta").value == 0
    assert legacy.compatibility.collision_groups == (("apple", ("green", "red")),)


def test_tail_uses_harmonized_earlier_counts_and_never_later_tail(tmp_path):
    case = _case("directed_many_to_one")
    for row in case["records"]:
        if row["dataset_version"] == "v2":
            row["topic"] = "new"
    _, result = _analyze(case, tmp_path)
    pair = result.comparisons[0]
    tail = pair.tail_disappearance
    assert pair.support_comparison.extinct_states == ("apple", "pear")
    assert tail.earlier_tail.tail_membership == ("pear",)
    assert tail.tail_extinct_states == ("pear",) and tail.tail_extinction_count == 1
    assert tail.earlier_sample_size == 4
    assert tail.representation == pair.compatibility.harmonized_representation
    assert result.snapshots[0].distribution.unweighted.support == ("green", "pear", "red")


@pytest.mark.parametrize("options,expected", [
    (TailSelectionOptions("count_at_or_below", count_threshold=0), ()),
    (TailSelectionOptions("count_at_or_below", count_threshold=1), ("B", "C")),
    (TailSelectionOptions("frequency_at_or_below", frequency_threshold=.25), ("B", "C")),
    (TailSelectionOptions("state_list", state_ids=("C", "B")), ("B", "C")),
])
def test_explicit_tail_rules_and_valid_empty_selection(tmp_path, options, expected):
    case = _case()
    validation = _load_case(case, tmp_path)
    result = series.analyze_longitudinal(validation, selection=_select(case, validation), tail_options=options)
    tail = result.comparisons[0].tail_disappearance
    assert tail.status is CalculationStatus.AVAILABLE
    assert tail.tail_extinct_states == expected and tail.tail_extinction_count == len(expected)
    if options.rule == "state_list":
        assert result.comparisons[-1].tail_disappearance.status is CalculationStatus.UNAVAILABLE
        assert result.comparisons[-1].support_comparison.status is CalculationStatus.AVAILABLE
        assert _delta(result.comparisons[-1], "record_count_delta").value == -1


@pytest.mark.parametrize("empty_target", [False, True])
def test_missing_map_coverage_blocks_all_pair_deltas_even_with_unavailable_target(tmp_path, empty_target):
    case = _case("directed_many_to_one")
    if empty_target:
        case["records"] = [row for row in case["records"] if row["dataset_version"] == "v1"]
        case["provenance"] = [row for row in case["provenance"] if row["dataset_version"] == "v1"]
    validation = _load_case(case, tmp_path)
    declarations = _declarations(case)
    mapping = _mapping(declarations, states={"red": "apple", "pear": "pear"})
    selection = _select(case, validation, declarations=declarations, mappings=(mapping,))
    assert selection.pairs[0].status is CalculationStatus.AVAILABLE  # Step 2 checks only declarations
    result = series.analyze_longitudinal(validation, selection=selection)
    assert result.comparisons[0].compatibility is None
    assert all(d.value is None for d in result.comparisons[0].deltas)
    assert result.comparisons[0].messages[0].code == ErrorCode.SCHEMA_TYPE.value
    assert result.execution_status is ExecutionStatus.FAILED
    assert result.snapshots[0].distribution.unweighted.support_size.value == 3


def test_pair_local_mappings_cannot_create_a_transitive_baseline(tmp_path):
    case = _case()
    for row in case["records"]:
        if row["dataset_version"] == "v2":
            row["topic"] = {"A": "x", "D": "y"}[row["topic"]]
        if row["dataset_version"] == "v3":
            row["topic"] = {"A": "q", "B": "r", "D": "s"}[row["topic"]]
    validation = _load_case(case, tmp_path)
    declarations = tuple(replace(d, representation=replace(d.representation, version=f"basis-{i}"),
                                 state_semantics=f"meaning-{i}") for i, d in enumerate(_declarations(case)))
    maps = (_mapping(declarations, states={"A": "x", "B": "x", "C": "y"}),
            _mapping(declarations[1:], states={"x": "q", "y": "q"}))
    result = series.analyze_longitudinal(validation, selection=_select(case, validation, declarations=declarations, mappings=maps))
    first, baseline, last = result.comparisons
    assert first.compatibility.harmonized_representation != last.compatibility.harmonized_representation
    assert first.support_comparison and last.support_comparison
    assert baseline.support_comparison is None and baseline.compatibility is None
    assert result.snapshots[1].distribution.unweighted.support == ("x", "y")


def test_added_mapping_entries_and_record_weights_create_no_artificial_states(tmp_path):
    case = _case("directed_many_to_one")
    for row in case["records"]:
        row["weight"] = 0
    validation = _load_case(case, tmp_path)
    declarations = _declarations(case)
    mapping = _mapping(declarations, states={"red": "apple", "green": "apple", "pear": "pear", "unused": "ghost"})
    result = series.analyze_longitudinal(validation, selection=_select(case, validation, declarations=declarations, mappings=(mapping,)))
    assert all(s.distribution.weighted is None for s in result.snapshots)
    assert "ghost" not in result.comparisons[0].support_comparison.harmonized_earlier.support
    assert result.snapshots[0].distribution.unweighted.analyzed_record_count == 4


def test_permutation_preserves_complete_result_and_tail_options_are_bound(tmp_path):
    case = _case()
    validation = _load_case(case, tmp_path)
    selection = _select(case, validation)
    plain = series.analyze_longitudinal(validation, selection=selection)
    tail = series.analyze_longitudinal(validation, selection=selection, tail_options=TailSelectionOptions("singleton_count"))
    shuffled = replace(validation, records=validation.records[::-1], provenance=validation.provenance[::-1])
    assert series.analyze_longitudinal(shuffled, selection=selection) == plain
    assert tail.input_signature != plain.input_signature
    assert plain.input_signature not in repr(plain)
    with pytest.raises(FrozenInstanceError):
        plain.execution_status = ExecutionStatus.COMPLETED


def test_version_renaming_preserves_ordered_numerical_observations(tmp_path):
    case = _case()
    rename = {"v1": "z", "v2": "v10", "v3": "v2"}
    for row in (*case["records"], *case["provenance"]):
        row["dataset_version"] = rename[row["dataset_version"]]
    case["selected_versions"] = [rename[v] for v in case["selected_versions"]]
    case["order_document"] = {"version_order": case["selected_versions"]}
    case["representations"] = {rename[v]: declaration for v, declaration in case["representations"].items()}
    _, result = _analyze(case, tmp_path)
    assert result.selection.selected_order == ("z", "v10", "v2")
    assert [s.distribution.unweighted.support_size.value for s in result.snapshots] == [3, 2, 3]
    assert [_delta(p, "support_delta").value for p in result.comparisons] == [-1, 0, 1]
    assert [p.tail_disappearance.tail_extinct_states for p in result.comparisons] == [("B", "C"), ("C",), ()]


@pytest.mark.parametrize("mutation", ["missing_snapshot", "reversed_pairs", "tail_binding", "completed", "denominator"])
def test_result_constructors_reject_scope_enablement_and_status_forgery(tmp_path, mutation):
    case = _case("all_excluded_later") if mutation == "completed" else _case()
    _, result = _analyze(case, tmp_path)
    with pytest.raises(CanonicalValidationError):
        if mutation == "missing_snapshot":
            replace(result, snapshots=result.snapshots[:-1])
        elif mutation == "reversed_pairs":
            replace(result, comparisons=result.comparisons[::-1])
        elif mutation == "tail_binding":
            replace(result, tail_options=None)
        elif mutation == "completed":
            replace(result, execution_status=ExecutionStatus.COMPLETED)
        else:
            pair = result.comparisons[0]
            count = pair.deltas[0]
            count = replace(count, earlier_value=count.earlier_value - 1, value=count.value + 1)
            pair = replace(pair, deltas=(count, *pair.deltas[1:]))
            replace(result, comparisons=(pair, *result.comparisons[1:]))


@pytest.mark.parametrize("changes", [{"formula_id": "F-005"}, {"unit": "ratio"}, {"value": True},
                                   {"value": float("nan")}, {"value": 10**400}])
def test_new_delta_values_and_trace_metadata_stay_typed(tmp_path, changes):
    _, result = _analyze(_case(), tmp_path)
    with pytest.raises(CanonicalValidationError):
        replace(_delta(result.comparisons[0], "record_count_delta"), **changes)


@pytest.mark.parametrize("change", ["state", "mode", "population"])
def test_stale_selection_is_rejected_before_calculation(tmp_path, monkeypatch, change):
    case = _case()
    validation = _load_case(case, tmp_path)
    selection = _select(case, validation)
    if change == "state":
        validation = replace(validation, records=(replace(validation.records[0],
            values={**validation.records[0].values, "topic": "changed"}), *validation.records[1:]))
    elif change == "mode":
        validation = replace(validation, content_mode=ContentMode.LOCAL_REF)
    else:
        scope = selection.snapshots[0]
        smaller = replace(scope, population_scope=replace(scope.population_scope,
            included_record_keys=scope.population_scope.included_record_keys[:-1]))
        selection = replace(selection, snapshots=(smaller, *selection.snapshots[1:]))
    monkeypatch.setattr(series, "calculate_state_distribution", lambda *a, **k: pytest.fail("invalid selection ran analysis"))
    with pytest.raises(CanonicalValidationError):
        series.analyze_longitudinal(validation, selection=selection)


@pytest.mark.parametrize("kwargs", [{"lineage": True, "lineage_limits": {}}, {"lineage": 1}, {"lineage_limits": {}}, {"tail_options": {}},
                                   {"tail_options": "singleton_count"}])
def test_unsupported_or_malformed_options_fail_before_execution(tmp_path, monkeypatch, kwargs):
    case = _case()
    validation = _load_case(case, tmp_path)
    selection = _select(case, validation)
    monkeypatch.setattr(series, "assign_field_states", lambda *a, **k: pytest.fail("invalid option ran assignment"))
    with pytest.raises(CanonicalValidationError):
        series.analyze_longitudinal(validation, selection=selection, **kwargs)


def test_hero_series_matches_frozen_pair_oracle(repo_root):
    hero = repo_root / "examples/hero"
    roles = (FileRole.RECORDS_COMPARE, FileRole.RECORDS_PRIMARY, FileRole.PROVENANCE_MANIFEST, FileRole.VERSION_ORDER)
    names = ("records_v1.csv", "records_v2.csv", "provenance.csv", "version_order.json")
    validation = validate_bundle(AuditBundle(tuple(InputSource(role, hero / name) for role, name in zip(roles, names))))
    config = RepresentationConfig("topic", "topic_field", "topic", "hero-topic-v1", "exclude")
    declarations = tuple(series.SnapshotDeclaration(v, config, "hero topic meanings") for v in ("v1", "v2"))
    result = series.analyze_longitudinal(validation, selection=series.select_longitudinal_versions(validation, declarations=declarations))
    oracle = next(c["expected"] for c in json.loads((repo_root / "tests/golden/phase3_math_cases.json").read_text())["cases"] if c["case_id"] == "HERO-PAIR")
    pair = result.comparisons[0]
    assert _delta(pair, "record_count_delta").value == 0
    assert _delta(pair, "support_delta").value == oracle["support_delta"] == -3
    assert _delta(pair, "gini_simpson_diversity_delta").value == float(Fraction(oracle["diversity_delta"]))
    assert list(pair.support_comparison.extinct_states) == oracle["lost_states"]


@pytest.mark.parametrize("resolved", [False, True])
def test_retained_local_reference_mode_never_hashes_path_text(tmp_path, resolved):
    case = _case("tied_timestamps_explicit_order")
    for i, row in enumerate(case["records"]):
        row["content"] = f"content-{i}.txt"
        (tmp_path / row["content"]).write_text("Actual local text, not the path")
    initial = _load_case(case, tmp_path)
    validation = validate_bundle(AuditBundle(tuple(InputSource(entry.role, entry.path) for entry in initial.inventory)),
        normalization_options=NormalizationOptions(content_mode=ContentMode.LOCAL_REF),
        resolve_local_content=resolved)
    assert validation.content_mode is ContentMode.LOCAL_REF
    declarations = tuple(replace(d, representation=RepresentationConfig("exact", "content_hash", "content",
        "r1", "error", "exact_utf8_v1"), state_semantics="exact record form") for d in _declarations(case))
    result = series.analyze_longitudinal(validation, selection=_select(case, validation, declarations=declarations))
    assert all(s.distribution is None for s in result.snapshots)
    assert all(CalculationReason.CONTENT_UNAVAILABLE in _family(s, "distribution").reason_codes for s in result.snapshots)
    assert all(s.scope.representation_scope is None for s in result.snapshots)
    assert _delta(result.comparisons[0], "record_count_delta").value == 1
    fields = series.analyze_longitudinal(validation, selection=_select(case, validation))
    assert all(s.distribution.unweighted.status is CalculationStatus.AVAILABLE for s in fields.snapshots)


def test_inline_content_uses_existing_exact_hash_assignment(tmp_path):
    case = _case("tied_timestamps_explicit_order")
    for row in case["records"]:
        row["content"] = "shared literal content"
    validation = _load_case(case, tmp_path)
    declarations = tuple(replace(d, representation=RepresentationConfig("exact", "content_hash", "content", "r1",
        "error", "exact_utf8_v1"), state_semantics="exact record form") for d in _declarations(case))
    result = series.analyze_longitudinal(validation, selection=_select(case, validation, declarations=declarations))
    assert [s.distribution.unweighted.support_size.value for s in result.snapshots] == [1, 1]
    assert _delta(result.comparisons[0], "gini_simpson_diversity_delta").value == 0
    assert result.comparisons[0].support_comparison.extinct_states == ()


def test_analysis_never_dispatches_graph_scenarios_or_io(tmp_path, monkeypatch):
    import builtins
    from recursive_integrity_toolkit.lineage import ancestry, graph
    from recursive_integrity_toolkit.metrics import resampling, tail

    validation = _load_case(_case(), tmp_path)
    selection = _select(_case(), validation)
    def forbidden(*args, **kwargs):
        pytest.fail("series dispatched a deferred, stochastic or I/O operation")
    for module, name in ((graph, "build_lineage_graph"), (ancestry, "analyze_lineage"),
            (tail, "one_step_extinction_probability"), (builtins, "open")):
        monkeypatch.setattr(module, name, forbidden)
    for name in ("expected_diversity_after_steps", "simulate_closed_resampling"):
        monkeypatch.setattr(resampling, name, forbidden)
    assert series.analyze_longitudinal(validation, selection=selection,
        tail_options=TailSelectionOptions("singleton_count")).shared_lineage is None
