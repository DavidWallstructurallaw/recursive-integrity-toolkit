"""Step 4 independent provenance, direct-bound and longitudinal delta contracts."""
from dataclasses import FrozenInstanceError, replace

import pytest

from recursive_integrity_toolkit.config import RepresentationConfig
from recursive_integrity_toolkit.errors import CanonicalValidationError, ErrorCode, WarningCode
from recursive_integrity_toolkit.io.validation import join_provenance, validate_bundle
from recursive_integrity_toolkit.metrics import longitudinal as series
from recursive_integrity_toolkit.metrics.bounds import direct_closure_exposure
from recursive_integrity_toolkit.metrics.provenance import summarize_provenance
from recursive_integrity_toolkit.models import (
    AuditBundle, CalculationEvidenceClass, CalculationReason, CalculationStatus,
    FileRole, InputSource, ValidationSeverity,
)
from recursive_integrity_toolkit.result import ExecutionStatus
from test_longitudinal_analysis import _delta, _family, _select
from test_longitudinal_fixture_inputs import (
    HERO, _check_provenance, _fraction, _hero_validation, _load_case,
)
from test_longitudinal_selection import _case, _declarations, _mapping


CATEGORIES = ("human", "synthetic", "mixed", "sensor", "unknown")
COVERAGE = (
    ("row", "provenance_row_coverage_delta"),
    ("required", "provenance_required_field_coverage_delta"),
    ("grounding", "grounding_field_coverage_delta"),
)
BOUNDS = (
    "direct_closure_lower_bound_delta", "direct_closure_upper_bound_delta",
    "direct_closure_interval_width_delta",
)
STEP4_DELTAS = tuple(name for _, name in COVERAGE) + ("missing_provenance_share_delta",) + BOUNDS


def _analyze(case, tmp_path, **selection_options):
    validation = _load_case(case, tmp_path)
    selection = _select(case, validation, **selection_options)
    return validation, series.analyze_longitudinal(validation, selection=selection)


def _bounds(result):
    return tuple(getattr(result, field).value for field in ("lower_bound", "upper_bound", "interval_width"))


def _step4_values(pair):
    return tuple(_delta(pair, name) for name in STEP4_DELTAS) + tuple(pair.source_type_share_deltas.values())


def _check_pair(pair, expected):
    for key, name in COVERAGE:
        _fraction(_delta(pair, name).value, expected["coverage_delta"][key])
    for category in CATEGORIES:
        _fraction(pair.source_type_share_deltas[category].value, expected["source_share_delta"][category])
    _fraction(_delta(pair, "missing_provenance_share_delta").value,
              expected["missing_provenance_share_delta"])
    for name, value in zip(BOUNDS, expected["direct_bounds_delta"], strict=True):
        _fraction(_delta(pair, name).value, value)


def test_observed_series_matches_frozen_provenance_and_interval_oracles(tmp_path):
    case = _case()
    _, result = _analyze(case, tmp_path)
    for snapshot in result.snapshots:
        expected = case["expected_provenance"][snapshot.scope.dataset_version]
        _check_provenance(snapshot.provenance, expected)
        for actual, value in zip(_bounds(snapshot.direct_closure), expected["direct_bounds"], strict=True):
            _fraction(actual, value)
        assert snapshot.provenance.scope.included_record_keys == snapshot.scope.population_scope.included_record_keys
        assert snapshot.provenance.scope.excluded_record_keys == ()
        assert snapshot.direct_closure.scope == snapshot.provenance.scope
        assert _family(snapshot, "provenance").execution_status is ExecutionStatus.COMPLETED
        assert _family(snapshot, "direct_closure").execution_status is ExecutionStatus.COMPLETED
    pairs = {(p.pair.earlier_version, p.pair.later_version): p for p in result.comparisons}
    for oracle in case["expected_pairs"]:
        _check_pair(pairs[oracle["earlier"], oracle["later"]], oracle["provenance"])
    assert result.execution_status is ExecutionStatus.COMPLETED
    assert result.reason_codes == ()
    assert all(_family(s, "lineage").execution_status is ExecutionStatus.NOT_REQUESTED
               for s in (*result.snapshots, *result.comparisons))


def test_each_new_delta_preserves_owner_formula_and_separate_endpoint_denominators(tmp_path):
    _, result = _analyze(_case(), tmp_path)
    snapshots = {s.scope.dataset_version: s for s in result.snapshots}
    for pair in result.comparisons:
        earlier, later = (snapshots[v].provenance for v in (pair.pair.earlier_version, pair.pair.later_version))
        assert tuple(d.metric_name for d in pair.deltas) == (
            "record_count_delta", "support_delta", "gini_simpson_diversity_delta", *STEP4_DELTAS)
        assert set(pair.source_type_share_deltas) == set(CATEGORIES)
        for delta in _step4_values(pair):
            owner = ("T3" if delta.metric_name in BOUNDS else
                     "PR-005" if delta.metric_name == "source_type_share_deltas" else "PR-004")
            assert (delta.owner_id, delta.formula_id, delta.unit) == (owner, "F-018", "ratio")
            assert delta.evidence_class is CalculationEvidenceClass.DERIVED_METRIC
            assert delta.method == "later minus earlier" and delta.representation is None
            assert delta.denominator is None and delta.denominator_reason == "not_applicable_to_difference"
            assert delta.earlier_denominator == earlier.analyzed_record_count.value
            assert delta.later_denominator == later.analyzed_record_count.value
            assert delta.earlier_scope == earlier.scope and delta.later_scope == later.scope
            assert delta.earlier_scope.dataset_versions == (pair.pair.earlier_version,)
            assert delta.later_scope.dataset_versions == (pair.pair.later_version,)
            assert delta.value == pytest.approx(delta.later_value - delta.earlier_value)
            assert delta.status is CalculationStatus.AVAILABLE and delta.reason_codes == ()


def test_hero_keeps_frozen_values_and_exact_single_target_results():
    validation = _hero_validation("v2")
    config = RepresentationConfig("topic", "topic_field", "topic", "hero-topic-v1", "exclude")
    declarations = tuple(series.SnapshotDeclaration(v, config, "hero topic meanings") for v in ("v1", "v2"))
    result = series.analyze_longitudinal(validation, selection=series.select_longitudinal_versions(
        validation, declarations=declarations))
    for snapshot in result.snapshots:
        version = snapshot.scope.dataset_version
        _check_provenance(snapshot.provenance, HERO["expected_provenance"][version])
        explicit = summarize_provenance(join_provenance(validation.records, validation.provenance,
            dataset_versions=(version,)), scope=snapshot.provenance.scope)
        assert snapshot.provenance == explicit
        assert snapshot.direct_closure == direct_closure_exposure(explicit)
        assert snapshot.provenance.analyzed_record_count.metadata.evidence_class is CalculationEvidenceClass.OBSERVED_FACT
        assert snapshot.direct_closure.lower_bound.metadata.formula_id == "F-009"
        assert snapshot.direct_closure.upper_bound.metadata.formula_id == "F-010"
    _check_pair(result.comparisons[0], HERO["expected_pairs"][0]["provenance"])
    assert result.execution_status is ExecutionStatus.COMPLETED


def test_all_five_source_categories_keep_missing_as_sixth_component(tmp_path):
    case = _case("all_excluded_later")
    record_template, provenance_template = case["records"][0], case["provenance"][0]
    case["records"], case["provenance"] = [], []
    for version in ("v1", "v2"):
        for index in range(6):
            record_id = f"r{index}"
            case["records"].append({**record_template, "dataset_version": version,
                                    "record_id": record_id, "topic": "A", "weight": 0})
            if index < 5:
                category = "human" if version == "v2" and index == 4 else CATEGORIES[index]
                case["provenance"].append({**provenance_template, "dataset_version": version,
                                          "record_id": record_id, "source_type": category})
    _, result = _analyze(case, tmp_path)
    a, b = (s.provenance for s in result.snapshots)
    assert dict(a.source.counts) == dict.fromkeys(CATEGORIES, 1)
    assert dict(a.source.shares) == dict.fromkeys(CATEGORIES, 1 / 6)
    assert a.missing_provenance_count.value == 1 and a.missing_provenance_share.value == 1 / 6
    assert dict(b.source.counts) == dict(human=2, synthetic=1, mixed=1, sensor=1, unknown=0)
    for composition in (a, b):
        assert sum(dict(composition.source.shares).values()) + composition.missing_provenance_share.value == pytest.approx(1)
        assert composition.weighted_source is None
    pair = result.comparisons[0]
    expected = dict(human=1 / 6, synthetic=0, mixed=0, sensor=0, unknown=-1 / 6)
    assert {k: d.value for k, d in pair.source_type_share_deltas.items()} == pytest.approx(expected)
    assert sum(d.value for d in pair.source_type_share_deltas.values()) + _delta(pair, "missing_provenance_share_delta").value == pytest.approx(0)
    with pytest.raises(TypeError):
        pair.source_type_share_deltas["human"] = pair.source_type_share_deltas["unknown"]
    with pytest.raises(FrozenInstanceError):
        pair.source_type_share_deltas["human"].value = 0


@pytest.mark.parametrize("mode", ["absent_manifest", "empty_manifest", "declared_unknown"])
def test_manifest_absence_and_missing_rows_remain_distinct_from_declared_unknown(tmp_path, mode):
    case = _case("all_excluded_later")
    for row in case["records"]:
        row["topic"] = "A"
    if mode == "declared_unknown":
        for row in case["provenance"]:
            row.update(source_type="unknown", provenance_confidence="unknown", external_grounding="unknown")
    validation = _load_case(case, tmp_path)
    if mode != "declared_unknown":
        sources = tuple(InputSource(entry.role, entry.path) for entry in validation.inventory
                        if entry.role is not FileRole.PROVENANCE_MANIFEST)
        if mode == "empty_manifest":
            # An empty CSV retains the required declared columns, unlike a
            # headerless empty JSONL file, which the input contract rejects.
            path = tmp_path / "empty_provenance.csv"
            path.write_text("dataset_version,record_id,source_type,provenance_confidence,external_grounding\n")
            sources += (InputSource(FileRole.PROVENANCE_MANIFEST, path),)
        validation = validate_bundle(AuditBundle(sources))
    result = series.analyze_longitudinal(validation, selection=_select(case, validation))
    for snapshot in result.snapshots:
        composition = snapshot.provenance
        assert composition.provenance_supplied is (mode != "absent_manifest")
        assert composition.grounding_field_coverage.ratio == 0
        assert composition.source.status is CalculationStatus.AVAILABLE
        if mode == "declared_unknown":
            assert composition.provenance_row_coverage.ratio == composition.provenance_required_field_coverage.ratio == 1
            assert dict(composition.source.shares)["unknown"] == 1
            assert composition.missing_provenance_share.value == 0
            assert _bounds(snapshot.direct_closure) == (0, 1, 1)
            assert _family(snapshot, "direct_closure").execution_status is ExecutionStatus.COMPLETED
        else:
            assert composition.provenance_row_coverage.ratio == composition.provenance_required_field_coverage.ratio == 0
            assert sum(dict(composition.source.shares).values()) == 0
            assert composition.missing_provenance_share.value == 1
            assert _bounds(snapshot.direct_closure) == (None, None, None)
            assert _family(snapshot, "direct_closure").execution_status is ExecutionStatus.FAILED
    pair = result.comparisons[0]
    assert all(_delta(pair, name).value == 0 for _, name in COVERAGE)
    assert all(d.value == 0 for d in pair.source_type_share_deltas.values())
    assert result.execution_status is (ExecutionStatus.COMPLETED if mode == "declared_unknown" else ExecutionStatus.PARTIAL)


@pytest.mark.parametrize("field", ["source_type", "provenance_confidence", "external_grounding"])
@pytest.mark.parametrize("form", ["absent", "null"])
def test_incomplete_required_fields_preserve_known_coverages_and_other_family_results(tmp_path, field, form):
    case = _case()
    row = next(row for row in case["provenance"] if row["dataset_version"] == "v1")
    if form == "absent":
        del row[field]
    else:
        row[field] = None
    _, result = _analyze(case, tmp_path)
    snapshot = result.snapshots[0]
    provenance = snapshot.provenance
    assert provenance.input_has_errors
    assert provenance.provenance_row_coverage.ratio == 1
    assert provenance.provenance_required_field_coverage.ratio == 3 / 4
    assert provenance.grounding_field_coverage.ratio == (3 / 4 if field == "external_grounding" else 1)
    assert provenance.missing_provenance_share.value == 0
    assert _bounds(snapshot.direct_closure) == (0, 1 / 4, 1 / 4)
    assert _family(snapshot, "direct_closure").execution_status is ExecutionStatus.PARTIAL
    errors = [m for m in snapshot.messages if m.field == field and m.severity is ValidationSeverity.ERROR]
    assert errors and all(m in result.messages for m in errors)
    pair = result.comparisons[0]
    assert _delta(pair, "provenance_row_coverage_delta").value == -1 / 4
    assert _delta(pair, "provenance_required_field_coverage_delta").value == 0
    assert all(_delta(pair, name).status is CalculationStatus.AVAILABLE for name in BOUNDS)
    if field == "source_type":
        assert provenance.source.shares is None and provenance.source.counts is None
        assert all(d.value is None for d in pair.source_type_share_deltas.values())
        assert all(CalculationReason.PROVENANCE_FIELD_UNAVAILABLE in d.earlier_reason_codes
                   for d in pair.source_type_share_deltas.values())
    else:
        assert all(d.status is CalculationStatus.AVAILABLE for d in pair.source_type_share_deltas.values())
    assert _family(snapshot, "provenance").execution_status is ExecutionStatus.PARTIAL
    assert result.execution_status is ExecutionStatus.PARTIAL
    assert ErrorCode.SCHEMA_REQUIRED_FIELD.value in result.reason_codes
    assert all(_family(pair, family).execution_status is ExecutionStatus.PARTIAL
               for family in ("provenance", "direct_closure"))
    assert result.snapshots[-1].provenance.source.status is CalculationStatus.AVAILABLE
    assert all(_family(result.comparisons[-1], family).execution_status is ExecutionStatus.COMPLETED
               for family in ("provenance", "direct_closure"))


@pytest.mark.parametrize("field,value", [("source_type", "invented"), ("external_grounding", True),
                                          ("provenance_confidence", "certain")])
def test_malformed_present_provenance_is_rejected_before_series_analysis(tmp_path, field, value, monkeypatch):
    case = _case()
    case["provenance"][0][field] = value
    monkeypatch.setattr(series, "analyze_longitudinal", lambda *a, **k: pytest.fail("invalid input reached analysis"))
    with pytest.raises(CanonicalValidationError):
        _load_case(case, tmp_path)


def test_empty_snapshot_preserves_unavailable_endpoints_without_inventing_provenance(tmp_path):
    _, result = _analyze(_case("identified_empty_later"), tmp_path)
    empty = result.snapshots[1]
    assert empty.provenance is None and empty.direct_closure is None
    for family in ("provenance", "direct_closure"):
        status = _family(empty, family)
        assert status.execution_status is ExecutionStatus.FAILED
        assert CalculationReason.EMPTY_SCOPE in status.reason_codes
    pair = result.comparisons[0]
    assert _delta(pair, "record_count_delta").value == -2
    for delta in _step4_values(pair):
        assert delta.status is CalculationStatus.UNAVAILABLE and delta.value is None
        assert delta.later_value is None and delta.later_denominator == 0
        assert CalculationReason.EMPTY_SCOPE in delta.later_reason_codes
    assert result.execution_status is ExecutionStatus.PARTIAL


@pytest.mark.parametrize("mode", ["all_excluded", "missing_column"])
def test_representation_failure_preserves_complete_provenance_denominators_and_values(tmp_path, mode):
    case = _case("all_excluded_later")
    if mode == "missing_column":
        for row in case["records"]:
            if row["dataset_version"] == "v2":
                del row["topic"]
    _, result = _analyze(case, tmp_path)
    snapshot = result.snapshots[1]
    assert snapshot.provenance.analyzed_record_count.value == snapshot.direct_closure.denominator == 2
    assert snapshot.provenance.scope.excluded_record_keys == ()
    assert snapshot.provenance.provenance_row_coverage.ratio == 1
    assert _bounds(snapshot.direct_closure) == (1, 1, 0)
    pair = result.comparisons[0]
    assert pair.support_comparison is None
    assert all(delta.value == 0 for delta in _step4_values(pair))
    assert _family(pair, "provenance").execution_status is ExecutionStatus.COMPLETED
    assert _family(pair, "direct_closure").execution_status is ExecutionStatus.COMPLETED
    assert result.execution_status is ExecutionStatus.PARTIAL


@pytest.mark.parametrize("mode", ["incompatible", "incomplete_mapping"])
def test_incompatible_pair_blocks_provenance_and_bounds_without_discarding_snapshots(tmp_path, mode):
    case = _case("incompatible_middle" if mode == "incompatible" else "directed_many_to_one")
    validation = _load_case(case, tmp_path)
    declarations = _declarations(case)
    mappings = () if mode == "incompatible" else (_mapping(declarations, states={"red": "apple", "pear": "pear"}),)
    selection = _select(case, validation, baseline="none", declarations=declarations, mappings=mappings)
    result = series.analyze_longitudinal(validation, selection=selection)
    assert all(s.provenance.source.status is CalculationStatus.AVAILABLE for s in result.snapshots)
    assert all(s.direct_closure.status is CalculationStatus.AVAILABLE for s in result.snapshots)
    for pair in result.comparisons:
        assert all(d.status is CalculationStatus.UNAVAILABLE and d.value is None for d in _step4_values(pair))
        assert all(_family(pair, family).execution_status is ExecutionStatus.FAILED
                   for family in ("provenance", "direct_closure"))
    assert result.execution_status is ExecutionStatus.FAILED


@pytest.mark.parametrize("warning", [WarningCode.PROVENANCE_ESTIMATED, WarningCode.GROUNDING_UNKNOWN,
                                     WarningCode.PROVENANCE_MISSING_ROW])
def test_strict_warning_promotion_survives_per_version_rejoins(tmp_path, warning):
    case = _case()
    ordinary = _load_case(case, tmp_path)
    sources = tuple(InputSource(entry.role, entry.path) for entry in ordinary.inventory)
    strict = validate_bundle(AuditBundle(sources), configuration={"strict_mode": True,
        "strict_warning_codes": [warning.value]})
    result = series.analyze_longitudinal(strict, selection=_select(case, strict))
    promoted = [m for m in result.messages if m.code == warning.value]
    assert promoted and all(m.severity is ValidationSeverity.ERROR for m in promoted)
    assert result.execution_status is ExecutionStatus.PARTIAL
    assert warning.value in result.reason_codes
    affected = {
        WarningCode.PROVENANCE_ESTIMATED: {"v2", "v3"},
        WarningCode.GROUNDING_UNKNOWN: {"v3"},
        WarningCode.PROVENANCE_MISSING_ROW: {"v2"},
    }[warning]
    for snapshot in result.snapshots:
        composition = snapshot.provenance
        assert warning.value in composition.promoted_warning_codes
        expected = (ExecutionStatus.PARTIAL if snapshot.scope.dataset_version in affected
                    else ExecutionStatus.COMPLETED)
        for family in ("provenance", "direct_closure"):
            assert _family(snapshot, family).execution_status is expected
        messages = [m for m in composition.validation_messages if m.code == warning.value]
        if messages:
            assert composition.input_has_errors and snapshot.direct_closure.input_has_errors
            assert all(m.severity is ValidationSeverity.ERROR for m in messages)
            assert all(m in snapshot.messages and m in result.messages for m in messages)
    for actual, oracle in zip(result.comparisons, (case["expected_pairs"][0], case["expected_pairs"][2],
                                                  case["expected_pairs"][1]), strict=True):
        _check_pair(actual, oracle["provenance"])
        assert all(delta.status is CalculationStatus.AVAILABLE for delta in _step4_values(actual))
        endpoints = {actual.pair.earlier_version, actual.pair.later_version}
        expected = ExecutionStatus.PARTIAL if endpoints & affected else ExecutionStatus.COMPLETED
        assert all(_family(actual, family).execution_status is expected
                   for family in ("provenance", "direct_closure"))


@pytest.mark.parametrize("strict_first", [False, True])
def test_selection_binding_rejects_changed_strict_warning_policy_before_calculation(tmp_path, monkeypatch, strict_first):
    case = _case()
    ordinary = _load_case(case, tmp_path)
    sources = tuple(InputSource(entry.role, entry.path) for entry in ordinary.inventory)
    strict = validate_bundle(AuditBundle(sources), configuration={"strict_mode": True,
        "strict_warning_codes": [WarningCode.GROUNDING_UNKNOWN.value]})
    original, changed = (strict, ordinary) if strict_first else (ordinary, strict)
    selection = _select(case, original)
    assert selection.input_signature != _select(case, changed).input_signature
    def forbidden(*args, **kwargs):
        pytest.fail("stale strict policy binding reached calculation")
    monkeypatch.setattr(series, "assign_field_states", forbidden)
    monkeypatch.setattr(series, "summarize_provenance", forbidden)
    with pytest.raises(CanonicalValidationError):
        series.analyze_longitudinal(changed, selection=selection)


def test_context_required_field_error_preserves_selected_values_and_local_family_statuses(tmp_path):
    case = _case("lexical_order_context_unloaded")
    _, ordinary = _analyze(case, tmp_path)
    next(row for row in case["provenance"] if row["dataset_version"] == "v0")["source_type"] = None
    _, result = _analyze(case, tmp_path)
    assert ordinary.execution_status is ExecutionStatus.COMPLETED
    assert result.execution_status is ExecutionStatus.PARTIAL
    assert result.reason_codes == (ErrorCode.SCHEMA_REQUIRED_FIELD.value,)
    errors = [message for message in result.messages if message.severity is ValidationSeverity.ERROR]
    assert errors and all(message.record_key.dataset_version == "v0" for message in errors)
    for snapshot, baseline in zip(result.snapshots, ordinary.snapshots, strict=True):
        assert snapshot.provenance.input_has_errors and snapshot.direct_closure.input_has_errors
        assert snapshot.distribution == baseline.distribution
        assert snapshot.provenance.source.counts == baseline.provenance.source.counts
        assert snapshot.provenance.source.shares == baseline.provenance.source.shares
        assert snapshot.provenance.missing_provenance_share == baseline.provenance.missing_provenance_share
        for field in ("provenance_row_coverage", "provenance_required_field_coverage", "grounding_field_coverage"):
            assert getattr(snapshot.provenance, field) == getattr(baseline.provenance, field)
        assert _bounds(snapshot.direct_closure) == _bounds(baseline.direct_closure)
    for pair, baseline in zip(result.comparisons, ordinary.comparisons, strict=True):
        assert pair.deltas == baseline.deltas
        assert pair.source_type_share_deltas == baseline.source_type_share_deltas
    for item in (*result.snapshots, *result.comparisons):
        assert all(_family(item, family).execution_status is ExecutionStatus.COMPLETED
                   for family in ("distribution", "provenance", "direct_closure"))


@pytest.mark.parametrize("case_name,expected_counts", [("observed_three_version", (4, 4, 3)),
                                                       ("identified_empty_later", (2,))])
def test_provenance_and_bounds_run_once_per_nonempty_snapshot_without_graph_or_scenarios(tmp_path, monkeypatch, case_name, expected_counts):
    import recursive_integrity_toolkit.lineage.ancestry as ancestry
    import recursive_integrity_toolkit.lineage.graph as graph
    import recursive_integrity_toolkit.metrics.resampling as resampling

    case = _case(case_name)
    validation = _load_case(case, tmp_path)
    calls, bounds_calls = [], []
    summarize, bound = series.summarize_provenance, series.direct_closure_exposure
    def composition(joined, **kwargs):
        calls.append(joined.provenance_row_coverage.denominator)
        assert len(kwargs["scope"].dataset_versions) == 1
        assert kwargs["scope"].excluded_record_keys == ()
        return summarize(joined, **kwargs)
    def closure(value, *args, **kwargs):
        bounds_calls.append(value.analyzed_record_count.value)
        return bound(value, *args, **kwargs)
    def forbidden(*args, **kwargs):
        pytest.fail("Step 4 executed graph or scenario analysis")
    monkeypatch.setattr(series, "summarize_provenance", composition)
    monkeypatch.setattr(series, "direct_closure_exposure", closure)
    monkeypatch.setattr(ancestry, "analyze_lineage", forbidden)
    monkeypatch.setattr(graph, "build_lineage_graph", forbidden)
    monkeypatch.setattr(resampling, "expected_diversity_after_steps", forbidden)
    monkeypatch.setattr(resampling, "simulate_closed_resampling", forbidden)
    result = series.analyze_longitudinal(validation, selection=_select(case, validation))
    assert tuple(calls) == tuple(bounds_calls) == expected_counts
    assert result.shared_lineage is None


def test_context_records_and_unused_order_entries_do_not_enter_provenance_denominators(tmp_path):
    case = _case("lexical_order_context_unloaded")
    _, result = _analyze(case, tmp_path)
    selected = set(case["selected_versions"])
    assert set(result.selection.context_versions).isdisjoint(selected)
    for snapshot in result.snapshots:
        version = snapshot.scope.dataset_version
        count = sum(row["dataset_version"] == version for row in case["records"])
        assert snapshot.provenance.analyzed_record_count.value == count
        assert snapshot.direct_closure.denominator == count
        assert all(key.dataset_version == version for key in snapshot.provenance.scope.included_record_keys)


@pytest.mark.parametrize("mutation", ["missing_category", "extra_category", "foreign_scope",
                                      "changed_denominator", "changed_endpoint_value"])
def test_source_share_result_integrity_rejects_category_scope_and_value_forgery(tmp_path, mutation):
    _, result = _analyze(_case(), tmp_path)
    pair = result.comparisons[0]
    shares = dict(pair.source_type_share_deltas)
    original = shares["human"]
    with pytest.raises(CanonicalValidationError):
        if mutation == "missing_category":
            del shares["human"]
        elif mutation == "extra_category":
            shares["missing"] = original
        elif mutation == "foreign_scope":
            shares["human"] = replace(original, earlier_scope=result.snapshots[-1].provenance.scope)
        elif mutation == "changed_denominator":
            shares["human"] = replace(original, earlier_denominator=original.earlier_denominator + 1)
        else:
            # Keep later-minus-earlier internally consistent while changing the
            # observed endpoint: a valid scalar is still bound to its snapshot.
            shares["human"] = replace(original, earlier_value=original.earlier_value - 1 / 4,
                                      value=original.value + 1 / 4)
        changed = replace(pair, source_type_share_deltas=shares)
        replace(result, comparisons=(changed, *result.comparisons[1:]))


@pytest.mark.parametrize("mutation", ["lower_bound", "upper_bound", "interval_width",
                                      "available_to_unavailable", "unavailable_to_available"])
def test_snapshot_rejects_forged_direct_interval_values_and_availability(tmp_path, mutation):
    case = _case()
    if mutation == "unavailable_to_available":
        for row in case["provenance"]:
            if row["dataset_version"] == "v1":
                row["source_type"] = None
    _, result = _analyze(case, tmp_path)
    snapshot = result.snapshots[0 if mutation == "unavailable_to_available" else 1]
    bounds = snapshot.direct_closure
    if mutation in ("lower_bound", "upper_bound", "interval_width"):
        scalar = getattr(bounds, mutation)
        changed = replace(bounds, **{mutation: replace(scalar, value=scalar.value + 1 / 8)})
    else:
        available = mutation == "unavailable_to_available"
        # The fabricated available values still form the correct conservative
        # envelope; absent required provenance cannot make them available.
        values = (0, 1, 1) if available else (None, None, None)
        changed = replace(bounds, **{
            name: replace(getattr(bounds, name), value=value,
                          status=CalculationStatus.AVAILABLE if available else CalculationStatus.UNAVAILABLE,
                          reason_codes=() if available else (CalculationReason.PROVENANCE_FIELD_UNAVAILABLE,))
            for name, value in zip(("lower_bound", "upper_bound", "interval_width"), values, strict=True)
        })
    with pytest.raises(CanonicalValidationError):
        replace(snapshot, direct_closure=changed)
