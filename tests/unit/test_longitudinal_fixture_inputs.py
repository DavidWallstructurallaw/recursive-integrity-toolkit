"""Phase 6A acceptance fixtures checked against existing explicit kernels.

The authored rational oracles are independent of toolkit output. These tests
load canonical inputs and call accepted single-version/pair APIs explicitly.
They do not implement or certify future series selection, series deltas,
shared graph execution, report serialization or CLI longitudinal dispatch.
"""

from collections import Counter
from fractions import Fraction
import json
from pathlib import Path

import pytest

from recursive_integrity_toolkit.config import RepresentationConfig
from recursive_integrity_toolkit.errors import CanonicalValidationError
from recursive_integrity_toolkit.io.validation import (
    join_provenance,
    validate_bundle,
)
from recursive_integrity_toolkit.metrics.bounds import direct_closure_exposure
from recursive_integrity_toolkit.metrics.diversity import (
    calculate_state_distribution,
    compare_support,
)
from recursive_integrity_toolkit.metrics.provenance import summarize_provenance
from recursive_integrity_toolkit.metrics.tail import select_tail
from recursive_integrity_toolkit.models import (
    AuditBundle,
    CalculationScope,
    ExplicitPairContext,
    FileRole,
    InputSource,
    NumericalPolicy,
    TailSelectionOptions,
    ValidationSeverity,
)
from recursive_integrity_toolkit.representations.compatibility import StateMappingDeclaration
from recursive_integrity_toolkit.representations.field import assign_field_states


ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / "tests" / "fixtures" / "longitudinal"
DOCUMENT = json.loads((FIXTURES / "cases.json").read_text(encoding="utf-8"))
CASES = DOCUMENT["cases"]
HERO = json.loads((FIXTURES / "hero_expected.json").read_text(encoding="utf-8"))
DISTRIBUTION_CASES = [case for case in CASES if "expected_snapshots" in case]
LINEAGE_CASES = [case for case in CASES if "expected_lineage" in case]
NUMERICAL_POLICY = NumericalPolicy()


def _fraction(actual, exact):
    if exact is None:
        assert actual is None
    else:
        assert actual == pytest.approx(float(Fraction(exact)),
                                       rel=NUMERICAL_POLICY.relative_tolerance,
                                       abs=NUMERICAL_POLICY.absolute_tolerance)


def _write_rows(path, records):
    path.write_text("".join(json.dumps(row) + "\n" for row in records), encoding="utf-8")


def _load_case(case, tmp_path, *, primary=None):
    """Load a fresh ordinary invocation; never alter validated roles/objects."""
    loaded = {row["dataset_version"] for row in case["records"]}
    primary = primary or next(v for v in reversed(case["selected_versions"]) if v in loaded)
    sources = []
    for index, version in enumerate(sorted(loaded)):
        path = tmp_path / f"records_{index}.jsonl"
        _write_rows(path, [r for r in case["records"] if r["dataset_version"] == version])
        role = (FileRole.LINEAGE_CONTEXT if version in case["context_versions"] else
                FileRole.RECORDS_PRIMARY if version == primary else FileRole.RECORDS_COMPARE)
        sources.append(InputSource(role, path))
    path = tmp_path / "provenance.jsonl"
    _write_rows(path, case["provenance"])
    sources.append(InputSource(FileRole.PROVENANCE_MANIFEST, path))
    if case["order_document"] is not None:
        path = tmp_path / "order.json"
        path.write_text(json.dumps(case["order_document"]), encoding="utf-8")
        sources.append(InputSource(FileRole.VERSION_ORDER, path))
    return validate_bundle(AuditBundle(tuple(sources)))


def _distributions(case, validation):
    result = {}
    for version, declaration in case["representations"].items():
        config = RepresentationConfig(**{
            key: value for key, value in declaration.items() if key != "state_semantics"
        })
        represented = assign_field_states(
            tuple(row for row in validation.records if row.record_key.dataset_version == version),
            dataset_versions=(version,), scope_id="fixture-" + version,
            config=config,
        )
        result[version] = calculate_state_distribution(represented).unweighted
    return result


def _provenance(validation, version):
    joined = join_provenance(validation.records, validation.provenance,
                             dataset_versions=(version,))
    scope = CalculationScope((version,), joined.scope_record_keys, (),
                             joined.provenance_row_coverage.denominator_name,
                             "fixture-provenance-" + version)
    return summarize_provenance(joined, scope=scope)


def _check_provenance(result, expected):
    assert result.analyzed_record_count.value == expected["record_count"]
    assert dict(result.source.counts) == expected["source_counts"]
    assert dict(result.confidence.counts) == expected["confidence_counts"]
    assert result.missing_provenance_count.value == expected["missing_provenance_count"]
    for category, value in result.source.shares:
        _fraction(value, expected["source_shares"][category])
    _fraction(result.missing_provenance_share.value, expected["missing_provenance_share"])
    for name, actual in (("row", result.provenance_row_coverage),
                         ("required", result.provenance_required_field_coverage),
                         ("grounding", result.grounding_field_coverage)):
        assert actual.denominator == expected["record_count"]
        _fraction(actual.ratio, expected["coverage"][name])
    direct = result.direct_grounding
    assert (direct.known_open_count.value, direct.known_closed_count.value,
            direct.unresolved_grounding_count.value) == tuple(
                expected["grounding_counts"][k] for k in ("yes", "no", "unresolved"))
    bounds = direct_closure_exposure(result)
    for actual, value in zip((bounds.lower_bound.value, bounds.upper_bound.value,
                              bounds.interval_width.value), expected["direct_bounds"], strict=True):
        _fraction(actual, value)


def _check_lineage(result, expected):
    from recursive_integrity_toolkit.metrics.bounds import lineage_closure_exposure

    assert result.scope.target_record_count == expected["N"]
    assert (result.grounded_record_count, result.closed_record_count,
            result.unresolved_record_count) == tuple(expected[k] for k in ("G", "C", "U"))
    assert {str(row.record_key): None if row.external_root_keys is None else
            sorted(map(str, row.external_root_keys)) for row in result.records} == expected["complete_root_sets"]
    for actual, name in ((result.declared_parent_reference_count, "declared_parent_references"),
                         (result.resolved_parent_reference_count, "resolved_parent_references"),
                         (result.unresolved_parent_reference_count, "unresolved_parent_references"),
                         (result.distinct_external_root_count, "distinct_external_root_count")):
        assert actual == expected[name]
    for actual, name in ((result.resolved_parent_edge_coverage, "resolved_reference_coverage"),
                         (result.resolved_lineage_coverage, "resolved_lineage_coverage"),
                         (result.external_ancestry_coverage, "external_ancestry_coverage"),
                         (result.ancestry_concentration_hhi, "hhi"),
                         (result.effective_external_root_count, "effective_root_count")):
        _fraction(actual, expected[name])
    assert result.root_metrics_status.value == expected["root_metrics_status"]
    assert result.concentration_status.value == expected["concentration_status"]
    assert list(result.concentration_reason_codes) == expected["concentration_reason_codes"]
    bounds = lineage_closure_exposure(result)
    for actual, value in zip((bounds.lower_bound, bounds.upper_bound, bounds.interval_width),
                             expected["lineage_bounds"], strict=True):
        _fraction(actual, value)
    # Incidence N and weight G remain distinct in the partial oracle.
    for contribution in result.root_contributions:
        root = str(contribution.record_key)
        sets = [roots for roots in expected["complete_root_sets"].values() if roots]
        incidence = sum(root in roots for roots in sets)
        mass = sum((Fraction(1, len(roots)) for roots in sets if root in roots), Fraction())
        assert contribution.incidence_count == incidence
        assert contribution.incidence_denominator == expected["N"]
        assert contribution.weight_denominator == expected["G"]
        _fraction(contribution.incidence_share, Fraction(incidence, expected["N"]))
        _fraction(contribution.normalized_weight, mass / expected["G"])


@pytest.mark.parametrize("case", CASES, ids=lambda case: case["case_id"])
def test_longitudinal_fixture_inputs_load_without_analytical_dispatch(case, tmp_path, monkeypatch):
    import recursive_integrity_toolkit.lineage.ancestry as ancestry
    import recursive_integrity_toolkit.metrics.diversity as diversity

    def forbidden(*args, **kwargs):
        raise AssertionError("input validation executed an analytical kernel")

    monkeypatch.setattr(ancestry, "analyze_lineage", forbidden)
    monkeypatch.setattr(diversity, "compare_support", forbidden)
    result = _load_case(case, tmp_path)
    assert {(row.record_key.dataset_version, row.record_key.record_id) for row in result.records} == {
        (row["dataset_version"], row["record_id"]) for row in case["records"]
    }
    errors = {m.code for m in result.validation_messages
              if m.severity in (ValidationSeverity.ERROR, ValidationSeverity.FATAL)}
    warnings = {m.code for m in result.validation_messages if m.severity is ValidationSeverity.WARNING}
    assert errors == set(case["expected_input"]["error_codes"])
    assert set(case["expected_input"]["required_warning_codes"]) <= warnings
    if case["order_document"] is None:
        assert result.version_order.order == ()
    if "expected_selected_order" in case:
        # Independent contract expectation, not a claim of runtime selection.
        selected = [v for v in result.version_order.order if v in case["selected_versions"]]
        assert selected == case["expected_selected_order"]
        assert not set(selected) & set(case["context_versions"])


@pytest.mark.parametrize("case", DISTRIBUTION_CASES, ids=lambda case: case["case_id"])
def test_existing_distribution_kernels_match_literal_snapshot_oracles(case, tmp_path):
    validation = _load_case(case, tmp_path)
    for version, actual in _distributions(case, validation).items():
        expected = case["expected_snapshots"][version]
        assert actual.analyzed_record_count == expected["eligible_count"]
        assert len(actual.scope.excluded_record_keys) == expected["excluded_count"]
        assert actual.analyzed_record_count + len(actual.scope.excluded_record_keys) == expected["record_count"]
        assert {row.state_id: row.state_count for row in actual.states} == expected["state_counts"]
        assert actual.support_size.value == expected["support_size"]
        _fraction(actual.gini_simpson_diversity.value, expected["diversity"])
        assert actual.status.value == expected["status"]
        assert list(actual.reason_codes) == expected["reason_codes"]


@pytest.mark.parametrize("case", DISTRIBUTION_CASES, ids=lambda case: case["case_id"])
def test_existing_explicit_pairs_match_oracles_without_series_execution(case, tmp_path):
    validation = _load_case(case, tmp_path)
    distributions = _distributions(case, validation)
    order = validation.version_order
    for pair in case["expected_pairs"]:
        a, b = (distributions[pair[k]] for k in ("earlier", "later"))
        meanings = [case["representations"][pair[k]]["state_semantics"] for k in ("earlier", "later")]
        kwargs = dict(context=ExplicitPairContext(a.scope, b.scope, a.representation,
                                                  b.representation, order),
                      earlier_state_semantics=meanings[0], later_state_semantics=meanings[1])
        if case.get("current_pair_kernel_rejects_unloaded_endpoint"):
            # Keep actual loaded-version evidence. The future selected-scope
            # compatibility helper is required for this empty series endpoint.
            assert pair["later"] not in order.loaded_versions
            with pytest.raises(CanonicalValidationError) as error:
                compare_support(a, b, **kwargs)
            assert error.value.code.value == "E_VERSION_ORDER_CONFLICT"
            continue
        if "mapping" in pair:
            declaration = pair["mapping"]
            kwargs["state_mapping"] = StateMappingDeclaration(
                declaration["direction"], a.representation, b.representation,
                *meanings, declaration["state_mapping"],
            )
        if "expected_pair_error" in pair:
            with pytest.raises(CanonicalValidationError) as error:
                compare_support(a, b, **kwargs)
            assert error.value.code.value == pair["expected_pair_error"]
            continue
        actual = compare_support(a, b, **kwargs)
        expected = pair["distribution"]
        assert actual.status.value == expected["status"]
        assert list(actual.reason_codes) == expected["reason_codes"]
        assert actual.support_delta.value == expected["support_delta"]
        _fraction(actual.gini_simpson_diversity_delta.value, expected["diversity_delta"])
        _fraction(actual.support_retention_ratio.value, expected["support_retention"])
        for name, field in (("extinct_states", "missing_states"), ("added_states", "added_states"),
                            ("retained_states", "retained_states")):
            values = getattr(actual, name)
            assert (None if values is None else list(values)) == expected[field]
        if actual.extinct_states is not None:
            tail = select_tail(actual.harmonized_earlier, options=TailSelectionOptions("singleton_count"))
            assert sorted(set(tail.tail_membership) & set(actual.extinct_states)) == expected["tail_extinct_states"]
        if "expected_harmonized" in pair:
            mapped = pair["expected_harmonized"]
            for side in ("earlier", "later"):
                distribution = getattr(actual, "harmonized_" + side)
                assert {r.state_id: r.state_count for r in distribution.states} == mapped[side + "_counts"]
                _fraction(distribution.gini_simpson_diversity.value, mapped[side + "_diversity"])
            assert [[target, list(sources)] for target, sources in actual.compatibility.collision_groups] == mapped["collision_groups"]
            assert actual.original_earlier == a and actual.original_later == b


def test_observed_three_version_provenance_uses_complete_populations(tmp_path):
    case = next(case for case in CASES if case["case_id"] == "observed_three_version")
    validation = _load_case(case, tmp_path)
    for version, expected in case["expected_provenance"].items():
        _check_provenance(_provenance(validation, version), expected)


@pytest.mark.parametrize("case", LINEAGE_CASES, ids=lambda case: case["case_id"])
def test_lineage_oracles_match_separate_existing_primary_invocations(case, tmp_path):
    from recursive_integrity_toolkit.lineage.ancestry import analyze_lineage

    for version, expected in case["expected_lineage"].items():
        validation = _load_case(case, tmp_path, primary=version)
        actual = analyze_lineage(validation, target_dataset_version=version)
        _check_lineage(actual, expected)
        assert actual.scope.loaded_record_count == len(case["records"])
        assert actual.scope.context_record_count == len(case["records"]) - expected["N"]


def _hero_validation(primary):
    hero = ROOT / "examples" / "hero"
    other = "v2" if primary == "v1" else "v1"
    return validate_bundle(AuditBundle((
        InputSource(FileRole.RECORDS_PRIMARY, hero / f"records_{primary}.csv"),
        InputSource(FileRole.RECORDS_COMPARE, hero / f"records_{other}.csv"),
        InputSource(FileRole.PROVENANCE_MANIFEST, hero / "provenance.csv"),
        InputSource(FileRole.VERSION_ORDER, hero / "version_order.json"),
    )))


@pytest.mark.parametrize("version", ["v1", "v2"])
def test_hero_per_version_provenance_and_lineage_oracles(version):
    from recursive_integrity_toolkit.lineage.ancestry import analyze_lineage

    validation = _hero_validation(version)
    _check_provenance(_provenance(validation, version), HERO["expected_provenance"][version])
    _check_lineage(analyze_lineage(validation, target_dataset_version=version),
                   HERO["expected_lineage"][version])


@pytest.mark.parametrize("case", DISTRIBUTION_CASES, ids=lambda case: case["case_id"])
def test_authored_distribution_oracles_follow_exact_rows_and_pair_sets(case):
    """Independent Fraction/set arithmetic, not comparison of two product outputs."""
    for version, expected in case["expected_snapshots"].items():
        rows = [row for row in case["records"] if row["dataset_version"] == version]
        counts = Counter(row["topic"] for row in rows if row["topic"] is not None)
        assert len(rows) == expected["record_count"]
        assert counts == expected["state_counts"]
        if expected["diversity"] is not None:
            n = sum(counts.values())
            assert 1 - sum((Fraction(n_i, n) ** 2 for n_i in counts.values()), Fraction()) == Fraction(expected["diversity"])
    for pair in case["expected_pairs"]:
        if "distribution" not in pair:
            continue
        expected = pair["distribution"]
        a, b = (case["expected_snapshots"][pair[k]] for k in ("earlier", "later"))
        assert b["record_count"] - a["record_count"] == expected["record_count_delta"]
        if expected["status"] == "unavailable":
            assert all(expected[field] is None for field in ("support_delta", "diversity_delta", "missing_states", "added_states", "retained_states", "support_retention", "tail_extinct_states"))
            continue
        left, right = a["state_counts"], b["state_counts"]
        if "mapping" in pair:
            mapped = Counter()
            for state, count in left.items():
                mapped[pair["mapping"]["state_mapping"][state]] += count
            left = mapped
        sa, sb = set(left), set(right)
        assert len(sb) - len(sa) == expected["support_delta"]
        assert sorted(sa - sb) == expected["missing_states"]
        assert sorted(sb - sa) == expected["added_states"]
        assert sorted(sa & sb) == expected["retained_states"]
        assert Fraction(len(sa & sb), len(sa)) == Fraction(expected["support_retention"])
        da, db = [1 - sum((Fraction(n, sum(counts.values())) ** 2 for n in counts.values()), Fraction())
                  for counts in (left, right)]
        assert db - da == Fraction(expected["diversity_delta"])
        assert sorted({k for k, n in left.items() if n == 1} & (sa - sb)) == expected["tail_extinct_states"]


@pytest.mark.parametrize("case", [CASES[0], HERO], ids=["three_version", "hero"])
def test_authored_provenance_deltas_use_exact_separate_denominators(case):
    for pair in case["expected_pairs"]:
        expected = pair["provenance"]
        a, b = (case["expected_provenance"][pair[k]] for k in ("earlier", "later"))
        for family, field in (("coverage", "coverage_delta"), ("source_shares", "source_share_delta")):
            for name, delta in expected[field].items():
                assert Fraction(b[family][name]) - Fraction(a[family][name]) == Fraction(delta)
        assert Fraction(b["missing_provenance_share"]) - Fraction(a["missing_provenance_share"]) == Fraction(expected["missing_provenance_share_delta"])
        for left, right, delta in zip(a["direct_bounds"], b["direct_bounds"], expected["direct_bounds_delta"], strict=True):
            assert Fraction(right) - Fraction(left) == Fraction(delta)


@pytest.mark.parametrize("case", [*LINEAGE_CASES, HERO], ids=lambda case: case.get("case_id", "hero"))
def test_authored_lineage_oracles_and_deltas_use_exact_grounded_sets(case):
    for version, expected in case["expected_lineage"].items():
        sets = list(expected["complete_root_sets"].values())
        assert len(sets) == expected["N"]
        assert sum(roots is None for roots in sets) == expected["U"]
        assert sum(roots == [] for roots in sets) == expected["C"]
        grounded = [roots for roots in sets if roots]
        assert len(grounded) == expected["G"]
        roots = set().union(*map(set, grounded)) if grounded else set()
        assert len(roots) == expected["distinct_external_root_count"]
        if grounded:
            weights = [sum((Fraction(1, len(s)) for s in grounded if root in s), Fraction()) / len(grounded)
                       for root in roots]
            hhi = sum((weight ** 2 for weight in weights), Fraction())
            assert hhi == Fraction(expected["hhi"])
            assert 1 / hhi == Fraction(expected["effective_root_count"])
        else:
            assert expected["hhi"] is expected["effective_root_count"] is None
        assert Fraction(expected["C"], expected["N"]) == Fraction(expected["lineage_bounds"][0])
        assert Fraction(expected["C"] + expected["U"], expected["N"]) == Fraction(expected["lineage_bounds"][1])
    for pair in case["expected_pairs"]:
        a, b = (case["expected_lineage"][pair[k]] for k in ("earlier", "later"))
        expected = pair["lineage"]
        for name in ("distinct_external_root_count", "hhi", "effective_root_count", "unresolved_parent_references", "resolved_reference_coverage", "resolved_lineage_coverage", "external_ancestry_coverage"):
            delta = expected[name + "_delta"]
            if a[name] is None or b[name] is None:
                assert delta is None
                assert expected["concentration_delta_reason_codes"]
            else:
                assert Fraction(b[name]) - Fraction(a[name]) == Fraction(delta)
        for left, right, delta in zip(a["lineage_bounds"], b["lineage_bounds"], expected["lineage_bounds_delta"], strict=True):
            assert Fraction(right) - Fraction(left) == Fraction(delta)
