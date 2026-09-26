"""Exact root allocation, target denominators and conditional concentration.

Frozen acceptance values and independent rational arithmetic protect the
topological allocation convention. No report caps, bounds or proxy are applied.
"""

from dataclasses import FrozenInstanceError, replace
from fractions import Fraction
import json
import math

import pytest

from recursive_integrity_toolkit.errors import CanonicalValidationError
from recursive_integrity_toolkit.io.validation import validate_bundle
from recursive_integrity_toolkit.lineage import ancestry
from recursive_integrity_toolkit.lineage.graph import LineageLimits
from recursive_integrity_toolkit.models import AuditBundle, FileRole, InputSource
from recursive_integrity_toolkit.result import ExecutionStatus, ReportStatus

# Reuse input construction only; all allocation oracles below are independent
# of the product implementation and the existing root-resolution assertions.
from test_T4_ancestry import _CASES, _FIXTURES, _ROOT, _fixture_validation, _key, _validation


def _analyze(validation, target="v2", **limits):
    return ancestry.analyze_lineage(validation, target_dataset_version=target,
                                    limits=LineageLimits(**limits))


def _assert_fraction(actual, expected):
    assert type(actual) is float
    assert math.isfinite(actual)
    assert actual == pytest.approx(float(Fraction(expected)), rel=1e-13, abs=1e-15)


def _assert_allocation(result, complete_sets, *, total, grounded, unresolved):
    """Count incidences directly from independently specified target root sets."""
    complete = [frozenset(roots) for roots in complete_sets.values() if roots]
    assert len(complete) == grounded
    roots = set().union(*complete) if complete else set()
    incidence = {root: sum(root in support for support in complete) for root in roots}
    mass = {root: sum((Fraction(1, len(support)) for support in complete if root in support),
                      Fraction()) for root in roots}
    expected_order = sorted(roots, key=lambda root: (-incidence[root], _key(root)))
    rows = result.root_contributions
    assert type(rows) is tuple
    assert [str(row.record_key) for row in rows] == expected_order
    assert result.distinct_external_root_count == len(roots)
    assert result.root_metrics_status is (ReportStatus.PARTIAL if unresolved else ReportStatus.AVAILABLE)
    for row in rows:
        root = str(row.record_key)
        assert type(row) is ancestry.RootContribution
        assert row.incidence_count == incidence[root]
        assert row.incidence_denominator == total
        assert row.weight_denominator == grounded
        _assert_fraction(row.incidence_share, Fraction(incidence[root], total))
        _assert_fraction(row.fractional_mass, mass[root])
        _assert_fraction(row.normalized_weight, mass[root] / grounded)
    if grounded:
        hhi = sum(((mass[root] / grounded) ** 2 for root in roots), Fraction())
        _assert_fraction(result.ancestry_concentration_hhi, hhi)
        _assert_fraction(result.effective_external_root_count, 1 / hhi)
        assert result.concentration_status is result.root_metrics_status
        assert result.concentration_reason_codes == ()
        assert math.fsum(row.fractional_mass for row in rows) == pytest.approx(grounded)
        assert math.fsum(row.normalized_weight for row in rows) == pytest.approx(1)
    else:
        assert rows == ()
        assert result.ancestry_concentration_hhi is None
        assert result.effective_external_root_count is None
        assert result.concentration_status is ReportStatus.UNAVAILABLE
        assert result.concentration_reason_codes == ("NO_RESOLVED_EXTERNAL_ROOTS",)


@pytest.mark.parametrize("case", _CASES, ids=lambda case: case["case_id"])
def test_frozen_root_sets_and_rational_oracles_determine_complete_allocation(case, tmp_path):
    validation, target = _fixture_validation(tmp_path, case)
    result = _analyze(validation, target)
    expected = case["expected_lineage"]
    counts = expected["counts"]
    _assert_allocation(result, expected["complete_root_sets"], total=counts["target"],
                       grounded=counts["grounded"], unresolved=counts["unresolved"])
    for source, field in (("ancestry_hhi", "ancestry_concentration_hhi"),
                          ("effective_external_root_count", "effective_external_root_count")):
        if source in expected:
            if expected[source] is None:
                assert getattr(result, field) is None
            else:
                _assert_fraction(getattr(result, field), expected[source])
    if "root_order" in expected:
        assert [str(row.record_key) for row in result.root_contributions] == expected["root_order"]
        assert [row.incidence_count for row in result.root_contributions] == expected["incidence"]
        for fixture_field, field in (("incidence_shares", "incidence_share"),
                                     ("fractional_masses", "fractional_mass"),
                                     ("normalized_weights", "normalized_weight")):
            for row, value in zip(result.root_contributions, expected[fixture_field], strict=True):
                _assert_fraction(getattr(row, field), value)


def test_hero_incidence_mass_and_concentration_match_preimplementation_oracle():
    hero = _ROOT / "examples" / "hero"
    expected = json.loads((_FIXTURES / "lineage_complete" / "hero_expected.json").read_text())
    validation = validate_bundle(AuditBundle((
        InputSource(FileRole.RECORDS_PRIMARY, hero / "records_v2.csv"),
        InputSource(FileRole.RECORDS_COMPARE, hero / "records_v1.csv"),
        InputSource(FileRole.PROVENANCE_MANIFEST, hero / "provenance.csv"),
        InputSource(FileRole.VERSION_ORDER, hero / "version_order.json"),
    )))
    result = _analyze(validation)
    rows = result.root_contributions
    assert result.scope.target_record_count == 8
    assert result.scope.loaded_record_count == 16
    assert result.distinct_external_root_count == expected["distinct_external_roots"]
    assert [str(row.record_key) for row in rows] == expected["root_order"]
    assert [row.incidence_count for row in rows] == expected["incidence"]
    for fixture_field, field in (("incidence_shares", "incidence_share"),
                                 ("fractional_masses", "fractional_mass"),
                                 ("normalized_weights", "normalized_weight")):
        for row, value in zip(rows, expected[fixture_field], strict=True):
            _assert_fraction(getattr(row, field), value)
    assert all(row.incidence_denominator == row.weight_denominator == 8 for row in rows)
    _assert_fraction(result.ancestry_concentration_hhi, expected["ancestry_hhi"])
    _assert_fraction(result.effective_external_root_count, expected["effective_external_root_count"])
    assert result.root_metrics_status is result.concentration_status is ReportStatus.AVAILABLE


def _unequal_supports():
    return {
        "v1::a": [], "v1::b": [], "v1::c": [], "v1::unrelated": [],
        "v2::t1": ["v1::a"], "v2::t2": ["v1::a", "v1::b"],
        "v2::t3": ["v1::a", "v1::b", "v1::c"], "v2::t4": ["v1::b", "v1::c"],
        "v2::closed": [], "v2::unknown": [],
    }


def _grounding():
    return {"v1::a": "yes", "v1::b": "yes", "v1::c": "yes",
            "v1::unrelated": "yes", "v2::unknown": "unknown"}


def test_unequal_supports_use_n_for_incidence_and_g_for_weights(tmp_path):
    result = _analyze(_validation(tmp_path, _unequal_supports(), grounding=_grounding()))
    assert result.scope.loaded_record_count == 10
    assert (result.grounded_record_count, result.closed_record_count, result.unresolved_record_count) == (4, 1, 1)
    rows = result.root_contributions
    assert [str(row.record_key) for row in rows] == ["v1::a", "v1::b", "v1::c"]
    assert [row.incidence_count for row in rows] == [3, 3, 2]
    for row, mass, weight, share in zip(rows, ("11/6", "4/3", "5/6"),
                                       ("11/24", "1/3", "5/24"), ("1/2", "1/2", "1/3"), strict=True):
        assert row.incidence_denominator == 6
        assert row.weight_denominator == 4
        _assert_fraction(row.fractional_mass, mass)
        _assert_fraction(row.normalized_weight, weight)
        _assert_fraction(row.incidence_share, share)
    _assert_fraction(result.ancestry_concentration_hhi, "35/96")
    _assert_fraction(result.effective_external_root_count, "96/35")
    assert result.root_metrics_status is result.concentration_status is ReportStatus.PARTIAL
    assert result.external_ancestry_coverage == 4 / 6


def test_permutation_and_redundant_paths_cannot_multiply_fractional_mass(tmp_path):
    declarations = _unequal_supports()
    baseline = _analyze(_validation(tmp_path / "base", declarations, grounding=_grounding()))
    reversed_input = _analyze(_validation(tmp_path / "reverse", declarations,
                                         grounding=_grounding(), reverse=True))
    expanded = {**declarations, "v1::path_a": ["v1::a"], "v1::path_ab": ["v1::a", "v1::b"]}
    expanded["v2::t2"] = ["a", "v1::a", "v1::b", "v1::path_a", "v1::path_ab", "a"]
    redundant = _analyze(_validation(tmp_path / "redundant", expanded, grounding=_grounding()))
    for result in (reversed_input, redundant):
        assert result.root_contributions == baseline.root_contributions
        assert result.distinct_external_root_count == baseline.distinct_external_root_count
        assert result.ancestry_concentration_hhi == baseline.ancestry_concentration_hhi
        assert result.effective_external_root_count == baseline.effective_external_root_count
    assert redundant.declared_parent_reference_count > baseline.declared_parent_reference_count


def test_bijective_identity_rename_preserves_values_and_reorders_only_canonical_ties(tmp_path):
    declarations, grounding = _unequal_supports(), _grounding()
    baseline = _analyze(_validation(tmp_path / "base", declarations, grounding=grounding))
    renamed = {key: key.split("::")[0] + "::" + str(100 - index)
               for index, key in enumerate(declarations)}
    changed = {renamed[key]: [renamed[parent] for parent in parents]
               for key, parents in declarations.items()}
    result = _analyze(_validation(tmp_path / "renamed", changed,
                                  grounding={renamed[key]: value for key, value in grounding.items()}))
    expected = {renamed[str(row.record_key)]: row for row in baseline.root_contributions}
    for row in result.root_contributions:
        original = expected[str(row.record_key)]
        assert row.incidence_count == original.incidence_count
        assert row.fractional_mass == original.fractional_mass
        assert row.normalized_weight == original.normalized_weight
        assert row.incidence_share == original.incidence_share
    assert tuple(result.root_contributions) == tuple(sorted(result.root_contributions,
        key=lambda row: (-row.incidence_count, row.record_key)))
    assert result.ancestry_concentration_hhi == pytest.approx(baseline.ancestry_concentration_hhi)
    assert result.effective_external_root_count == pytest.approx(baseline.effective_external_root_count)


def test_ranking_uses_incidence_before_mass_and_includes_singletons(tmp_path):
    result = _analyze(_validation(tmp_path, {
        "v1::a": [], "v1::b": [], "v1::c": [], "v1::d": [],
        "v2::one": ["v1::a"], "v2::two": ["v1::b", "v1::c", "v1::d"],
        "v2::three": ["v1::b", "v1::c", "v1::d"],
    }, grounding={f"v1::{name}": "yes" for name in "abcd"}))
    assert [str(row.record_key) for row in result.root_contributions] == ["v1::b", "v1::c", "v1::d", "v1::a"]
    assert [row.incidence_count for row in result.root_contributions] == [2, 2, 2, 1]
    assert result.root_contributions[-1].fractional_mass == 1.0
    assert result.root_contributions[0].fractional_mass < 1.0


def test_all_loaded_roots_are_computed_before_any_future_detail_limit(tmp_path):
    roots = [f"v1::r{index:03d}" for index in range(105)]
    declarations = {root: [] for root in roots}
    declarations.update({"v2::wide": roots, "v2::single": [roots[-1]]})
    result = _analyze(_validation(tmp_path, declarations, grounding={root: "yes" for root in roots}))
    _assert_allocation(result, {"v2::wide": roots, "v2::single": [roots[-1]]},
                       total=2, grounded=2, unresolved=0)
    assert len(result.root_contributions) == result.distinct_external_root_count == 105
    assert result.root_contributions[0].record_key == _key(roots[-1])
    _assert_fraction(result.ancestry_concentration_hhi, "9/35")
    _assert_fraction(result.effective_external_root_count, "35/9")


def test_completed_all_unresolved_partition_retains_exact_empty_root_distribution(tmp_path):
    result = _analyze(_validation(tmp_path, {"v2::self": ["self"]}))
    assert result.execution_status is ExecutionStatus.FAILED
    assert result.unresolved_record_count == 1
    _assert_allocation(result, {}, total=1, grounded=0, unresolved=1)


@pytest.mark.parametrize("limits", [{"max_root_memberships": 1}, {"max_root_union_visits": 1}])
def test_resource_abort_cannot_emit_partial_exact_root_distribution(tmp_path, limits):
    result = _analyze(_validation(tmp_path, {
        "v1::a": [], "v1::b": [], "v2::one": ["v1::a", "v1::b"],
    }, grounding={"v1::a": "yes", "v1::b": "yes"}), **limits)
    assert result.execution_status is ExecutionStatus.FAILED
    assert result.records is None
    assert result.root_contributions is None
    assert result.distinct_external_root_count is None
    assert result.ancestry_concentration_hhi is None
    assert result.effective_external_root_count is None
    assert result.root_metrics_status is result.concentration_status is ReportStatus.UNAVAILABLE
    assert result.concentration_reason_codes == ("LINEAGE_RESOURCE_LIMIT_EXCEEDED",)
    with pytest.raises(CanonicalValidationError):
        replace(result, root_contributions=(), distinct_external_root_count=0)


def _valid_contribution():
    return ancestry.RootContribution(
        record_key=_key("v1::a"), incidence_count=2, incidence_share=0.5,
        incidence_denominator=4, fractional_mass=1.5, normalized_weight=0.75,
        weight_denominator=2,
    )


def test_root_contribution_is_immutable_and_rejects_invalid_units_or_ratios():
    contribution = _valid_contribution()
    with pytest.raises(FrozenInstanceError):
        contribution.fractional_mass = 1.0
    invalid = (
        {"record_key": "v1::a"}, {"incidence_count": True}, {"incidence_count": 0},
        {"incidence_count": 3}, {"incidence_denominator": True}, {"incidence_denominator": 0},
        {"incidence_denominator": 1}, {"weight_denominator": False}, {"weight_denominator": 0},
        {"weight_denominator": 5}, {"incidence_share": True}, {"incidence_share": 0.6},
        {"incidence_share": float("inf")}, {"fractional_mass": float("nan")},
        {"fractional_mass": float("inf")}, {"fractional_mass": 0.0}, {"fractional_mass": -1.0},
        {"fractional_mass": 3.0}, {"normalized_weight": True}, {"normalized_weight": 1.1},
        {"normalized_weight": float("nan")}, {"normalized_weight": 0.5},
    )
    for changes in invalid:
        with pytest.raises(CanonicalValidationError):
            replace(contribution, **changes)


def test_result_rejects_truncation_wrong_denominators_and_forged_concentration(tmp_path):
    result = _analyze(_validation(tmp_path, _unequal_supports(), grounding=_grounding()))
    rows = result.root_contributions
    with pytest.raises(FrozenInstanceError):
        result.root_contributions = ()
    # Each replacement below can be internally valid as an individual root,
    # while contradicting the complete typed target population or root sets.
    wrong_n = replace(rows[0], incidence_denominator=7, incidence_share=3 / 7)
    wrong_g = replace(rows[0], weight_denominator=5, normalized_weight=rows[0].fractional_mass / 5)
    wrong_mass = replace(rows[0], fractional_mass=1.0, normalized_weight=1 / 4)
    absent_root = replace(rows[0], record_key=_key("v1::unrelated"))
    invalid = (
        {"root_contributions": list(rows)}, {"root_contributions": None},
        {"root_contributions": rows[:-1]}, {"root_contributions": tuple(reversed(rows))},
        {"root_contributions": (wrong_n,) + rows[1:]},
        {"root_contributions": (wrong_g,) + rows[1:]},
        {"root_contributions": (wrong_mass,) + rows[1:]},
        {"root_contributions": (absent_root,) + rows[1:]},
        {"distinct_external_root_count": 2}, {"distinct_external_root_count": True},
        {"ancestry_concentration_hhi": None}, {"ancestry_concentration_hhi": 0.0},
        {"ancestry_concentration_hhi": True}, {"ancestry_concentration_hhi": float("nan")},
        {"effective_external_root_count": None}, {"effective_external_root_count": 3.0},
        {"effective_external_root_count": float("inf")},
    )
    for changes in invalid:
        with pytest.raises(CanonicalValidationError):
            replace(result, **changes)


def test_no_grounded_targets_cannot_be_given_zero_or_infinite_concentration(tmp_path):
    result = _analyze(_validation(tmp_path, {"v2::closed": []}))
    for changes in (
        {"ancestry_concentration_hhi": 0.0}, {"effective_external_root_count": float("inf")},
        {"root_contributions": None}, {"distinct_external_root_count": None},
    ):
        with pytest.raises(CanonicalValidationError):
            replace(result, **changes)
