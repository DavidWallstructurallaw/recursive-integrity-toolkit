"""Lineage closure envelopes and descriptive shared-root evidence.

Frozen acceptance values, exact fractions and masking protect the partition
semantics. Direct grounding keeps its separate calculation and denominator.
"""

import builtins
from dataclasses import FrozenInstanceError, replace
from fractions import Fraction
import json
import math
from pathlib import Path
import socket

import pytest

from recursive_integrity_toolkit.errors import CanonicalValidationError
from recursive_integrity_toolkit.io.validation import join_provenance, validate_bundle
from recursive_integrity_toolkit.lineage import ancestry, cycles, graph
from recursive_integrity_toolkit.lineage.graph import LineageLimits
from recursive_integrity_toolkit.metrics import bounds
from recursive_integrity_toolkit.metrics.provenance import summarize_provenance
from recursive_integrity_toolkit.models import AuditBundle, CalculationScope, FileRole, InputSource
from recursive_integrity_toolkit.result import ExecutionStatus, ReportStatus

# Reuse canonical input construction only. Expected intervals and witnesses
# below come from the frozen fixtures or independently authored root sets.
from test_T4_ancestry import (
    _CASES, _FIXTURES, _MISSING, _ROOT, _fixture_validation, _key, _validation,
)


def _analyze(validation, target="v2", **limits):
    return ancestry.analyze_lineage(validation, target_dataset_version=target,
                                    limits=LineageLimits(**limits))


def _values(result):
    return result.lower_bound, result.upper_bound, result.interval_width


def _assert_interval(result, expected):
    if expected is None:
        assert _values(result) == (None, None, None)
        assert result.status is ReportStatus.UNAVAILABLE
        assert result.reason_codes
    else:
        for actual, value in zip(_values(result), expected, strict=True):
            assert type(actual) is float and math.isfinite(actual)
            assert actual == pytest.approx(float(Fraction(value)), rel=1e-13, abs=1e-15)
        assert result.status is ReportStatus.AVAILABLE
        assert result.reason_codes == ()


@pytest.mark.parametrize("case", _CASES, ids=lambda case: case["case_id"])
def test_frozen_partition_bounds_and_shared_root_evidence(case, tmp_path):
    validation, target = _fixture_validation(tmp_path, case)
    analysis = _analyze(validation, target)
    interval = bounds.lineage_closure_exposure(analysis)
    proxy = ancestry.shared_ancestry_dependence(analysis)
    expected = case["expected_lineage"]
    counts = expected["counts"]
    _assert_interval(interval, expected["lineage_bounds"])
    assert interval.denominator == counts["target"]
    assert (interval.grounded_record_count, interval.closed_record_count,
            interval.unresolved_record_count) == (
        counts["grounded"], counts["closed"], counts["unresolved"])
    assert interval.scope == proxy.scope == analysis.scope
    assert interval.input_execution_status is proxy.input_execution_status is analysis.execution_status
    assert interval.validation_messages == proxy.validation_messages == analysis.messages
    roots = [set(values) for values in expected["complete_root_sets"].values()]
    incidence = {root: sum(root in support for support in roots)
                 for support in roots for root in support}
    witnesses = sorted((root for root, count in incidence.items() if count >= 2),
                       key=lambda root: (-incidence[root], _key(root)))
    if witnesses:
        assert proxy.level == "present"
        assert proxy.status is (ReportStatus.PARTIAL if counts["unresolved"] else ReportStatus.AVAILABLE)
        assert str(proxy.witness.record_key) == witnesses[0]
        assert proxy.witness.incidence_count == incidence[witnesses[0]]
    elif counts["target"] and not counts["unresolved"]:
        assert proxy.level == "not_present"
        assert proxy.status is ReportStatus.AVAILABLE
        assert proxy.witness is None
    else:
        assert proxy.level == "indeterminate"
        assert proxy.status is ReportStatus.UNAVAILABLE
        assert proxy.witness is None
    if "shared_ancestry_proxy" in expected:
        assert proxy.level == expected["shared_ancestry_proxy"]
    reason = (("EMPTY_TARGET_SCOPE",) if not counts["target"] else
              ("UNRESOLVED_ANCESTRY",) if counts["unresolved"] else ())
    assert proxy.reason_codes == reason
    if not counts["target"]:
        assert interval.reason_codes == ("EMPTY_TARGET_SCOPE",)


def test_hero_lineage_zero_and_direct_half_remain_distinct():
    hero = _ROOT / "examples" / "hero"
    expected = json.loads((_FIXTURES / "lineage_complete" / "hero_expected.json").read_text())
    validation = validate_bundle(AuditBundle((
        InputSource(FileRole.RECORDS_PRIMARY, hero / "records_v2.csv"),
        InputSource(FileRole.RECORDS_COMPARE, hero / "records_v1.csv"),
        InputSource(FileRole.PROVENANCE_MANIFEST, hero / "provenance.csv"),
        InputSource(FileRole.VERSION_ORDER, hero / "version_order.json"),
    )))
    joined = join_provenance(validation.records, validation.provenance, dataset_versions=("v2",))
    scope = CalculationScope(("v2",), joined.scope_record_keys, (),
                             joined.provenance_row_coverage.denominator_name, "hero-direct")
    composition = summarize_provenance(joined, scope=scope)
    direct_before = bounds.direct_closure_exposure(composition)
    analysis = _analyze(validation)
    interval = bounds.lineage_closure_exposure(analysis)
    proxy = ancestry.shared_ancestry_dependence(analysis)
    direct_after = bounds.direct_closure_exposure(composition)
    _assert_interval(interval, expected["lineage_bounds"])
    assert tuple(getattr(direct_after, field).value for field in
                 ("lower_bound", "upper_bound", "interval_width")) == tuple(
        float(Fraction(value)) for value in expected["direct_bounds"])
    assert direct_after == direct_before
    assert interval.denominator == direct_after.denominator == 8
    assert interval.scope.loaded_record_count == 16
    assert interval.input_execution_status is ExecutionStatus.COMPLETED
    assert proxy.status is ReportStatus.AVAILABLE and proxy.level == "present"
    assert str(proxy.witness.record_key) == "v1::v1_01"
    assert proxy.witness.incidence_count == 3


@pytest.mark.parametrize("target_count", (1, 2))
def test_shared_root_boundary_counts_targets_and_deduplicates_aliases(target_count, tmp_path):
    declarations = {
        "v1::root": [], "v1::context_a": ["v1::root"],
        "v1::context_b": ["v1::root"],
        **{f"v2::t{index}": ["root", "v1::root", "root"] for index in range(target_count)},
    }
    analysis = _analyze(_validation(tmp_path, declarations, grounding={"v1::root": "yes"}))
    proxy = ancestry.shared_ancestry_dependence(analysis)
    assert analysis.root_contributions[0].incidence_count == target_count
    assert proxy.status is ReportStatus.AVAILABLE
    assert proxy.level == ("present" if target_count == 2 else "not_present")
    assert (proxy.witness.incidence_count if proxy.witness else None) == (2 if target_count == 2 else None)
    assert proxy.scope.target_record_count == target_count
    assert proxy.scope.context_record_count == 3
    _assert_interval(bounds.lineage_closure_exposure(analysis), (0, 0, 0))


@pytest.mark.parametrize("witness", (False, True))
def test_incomplete_ancestry_requires_positive_witness_for_partial_proxy(witness, tmp_path):
    declarations = {"v1::a": [], "v1::b": [], "v2::one": ["v1::a"],
                    "v2::two": ["v1::a" if witness else "v1::b"], "v2::u": []}
    analysis = _analyze(_validation(tmp_path, declarations, grounding={
        "v1::a": "yes", "v1::b": "yes", "v2::u": "unknown"}))
    interval = bounds.lineage_closure_exposure(analysis)
    proxy = ancestry.shared_ancestry_dependence(analysis)
    _assert_interval(interval, (0, "1/3", "1/3"))
    assert proxy.status is (ReportStatus.PARTIAL if witness else ReportStatus.UNAVAILABLE)
    assert proxy.level == ("present" if witness else "indeterminate")
    assert proxy.reason_codes == ("UNRESOLVED_ANCESTRY",)
    assert (proxy.witness is not None) is witness
    assert interval.resolved_lineage_coverage == proxy.resolved_lineage_coverage == 2 / 3
    assert interval.external_ancestry_coverage == proxy.external_ancestry_coverage == 2 / 3
    assert interval.unresolved_reason_codes == ("UNKNOWN_GROUNDING",)
    assert set(proxy.evidence_fields) == {
        "root_contributions.incidence_count", "resolved_lineage_coverage", "external_ancestry_coverage"}


@pytest.mark.parametrize("failure", (False, True))
def test_completed_all_unresolved_partition_has_conservative_numeric_bounds(failure, tmp_path):
    validation = (_validation(tmp_path, {"v2::u": ["v1::missing"]}, strict=True) if failure else
                  _validation(tmp_path, {"v2::u": []}, grounding={"v2::u": "unknown"}))
    analysis = _analyze(validation)
    interval = bounds.lineage_closure_exposure(analysis)
    proxy = ancestry.shared_ancestry_dependence(analysis)
    assert analysis.execution_status is (ExecutionStatus.FAILED if failure else ExecutionStatus.PARTIAL)
    _assert_interval(interval, (0, 1, 1))
    assert interval.unresolved_record_count == interval.denominator == 1
    assert interval.input_has_errors is failure
    assert interval.input_execution_reason_codes == analysis.execution_reason_codes
    assert interval.validation_messages == analysis.messages
    assert interval.unresolved_reason_codes
    assert proxy.status is ReportStatus.UNAVAILABLE and proxy.level == "indeterminate"
    assert proxy.input_has_errors is failure


def test_missing_and_unknown_branches_exclude_observed_roots_without_erasing_valid_witness(tmp_path):
    declarations = {"v1::root": [], "v1::unknown": [], "v1::missing_provenance": _MISSING,
                    "v2::g1": ["v1::root"], "v2::g2": ["v1::root"], "v2::closed": [],
                    "v2::u_unknown": ["v1::root", "v1::unknown"],
                    "v2::u_missing": ["v1::root", "v1::missing_provenance"]}
    analysis = _analyze(_validation(tmp_path, declarations, grounding={
        "v1::root": "yes", "v1::unknown": "unknown"}))
    interval = bounds.lineage_closure_exposure(analysis)
    proxy = ancestry.shared_ancestry_dependence(analysis)
    _assert_interval(interval, ("1/5", "3/5", "2/5"))
    assert (interval.grounded_record_count, interval.closed_record_count,
            interval.unresolved_record_count) == (2, 1, 2)
    assert proxy.status is ReportStatus.PARTIAL and proxy.level == "present"
    assert proxy.witness.incidence_count == 2
    assert proxy.resolved_lineage_coverage == 3 / 5
    assert proxy.external_ancestry_coverage == 2 / 5
    assert {"UNKNOWN_GROUNDING", "MISSING_PROVENANCE", "INCOMPLETE_PARENT_ANCESTRY"} <= set(
        interval.unresolved_reason_codes)


def test_declared_empty_target_and_resource_abort_have_distinct_unavailable_reasons(tmp_path):
    empty = _analyze(_validation(tmp_path / "empty", {"v1::a": []},
                                 grounding={"v1::a": "yes"}, target="v2"))
    aborted = _analyze(_validation(tmp_path / "resource", {"v1::a": [], "v2::t": ["v1::a"]},
                                   grounding={"v1::a": "yes"}), max_root_memberships=1)
    for source, reason, count in ((empty, "EMPTY_TARGET_SCOPE", 0),
                                  (aborted, "LINEAGE_RESOURCE_LIMIT_EXCEEDED", None)):
        interval = bounds.lineage_closure_exposure(source)
        proxy = ancestry.shared_ancestry_dependence(source)
        _assert_interval(interval, None)
        assert interval.reason_codes == proxy.reason_codes == (reason,)
        assert interval.scope.target_dataset_version == "v2"
        assert interval.grounded_record_count == interval.closed_record_count == interval.unresolved_record_count == count
        assert interval.resolved_lineage_coverage is interval.external_ancestry_coverage is None
        assert proxy.status is ReportStatus.UNAVAILABLE and proxy.level == "indeterminate"
        assert proxy.witness is None
        assert interval.input_execution_status is source.execution_status
    assert empty.execution_status is ExecutionStatus.COMPLETED
    assert aborted.execution_status is ExecutionStatus.FAILED


def test_masking_complete_grounded_or_closed_evidence_only_widens_the_interval(tmp_path):
    declarations = {"v2::grounded": [], "v2::closed": [], "v2::unknown": []}
    originals = {"v2::grounded": "yes", "v2::unknown": "unknown"}
    baseline = bounds.lineage_closure_exposure(_analyze(_validation(
        tmp_path / "base", declarations, grounding=originals)))
    _assert_interval(baseline, ("1/3", "2/3", "1/3"))
    for name, expected in (("grounded", ("1/3", 1, "2/3")), ("closed", (0, "2/3", "2/3"))):
        masked = bounds.lineage_closure_exposure(_analyze(_validation(
            tmp_path / name, declarations, grounding={**originals, f"v2::{name}": "unknown"})))
        _assert_interval(masked, expected)
        assert masked.lower_bound <= baseline.lower_bound <= baseline.upper_bound <= masked.upper_bound
        assert masked.interval_width >= baseline.interval_width
        assert masked.denominator == baseline.denominator


def _mixed_analysis(tmp_path):
    return _analyze(_validation(tmp_path, {"v1::a": [], "v2::g1": ["v1::a"],
        "v2::g2": ["v1::a"], "v2::closed": [], "v2::u": []},
        grounding={"v1::a": "yes", "v2::u": "unknown"}))


def test_bounds_and_proxy_are_frozen_source_snapshots_without_unsupported_scores(tmp_path):
    source = _mixed_analysis(tmp_path)
    interval = bounds.lineage_closure_exposure(source)
    proxy = ancestry.shared_ancestry_dependence(source)
    assert type(interval) is bounds.LineageClosureExposureBounds
    assert type(proxy) is ancestry.SharedAncestryDependence
    assert interval.denominator_basis == "all_valid_records_in_selected_dataset_scope"
    for value in (interval, proxy):
        assert value.source is not source and value.source == source
        with pytest.raises(FrozenInstanceError):
            value.source = source
        for name in ("midpoint", "risk_score", "risk_threshold", "severity", "universal_score",
                     "causal_contribution", "independent_information", "biological_relatedness"):
            assert not hasattr(value, name)
    with pytest.raises(TypeError):
        replace(interval, lower_bound=0.0)
    with pytest.raises(TypeError):
        replace(proxy, level="not_present")
    object.__setattr__(source, "closed_record_count", 999)
    object.__setattr__(source, "execution_status", ExecutionStatus.COMPLETED)
    _assert_interval(interval, ("1/4", "1/2", "1/4"))
    assert proxy.status is ReportStatus.PARTIAL and proxy.level == "present"
    assert interval.input_execution_status is proxy.input_execution_status is ExecutionStatus.PARTIAL


def test_new_entrypoints_reject_wrong_types_and_forged_complete_handoffs(tmp_path):
    source = _mixed_analysis(tmp_path)

    class Hostile:
        def __getattr__(self, name):
            raise AssertionError("foreign input must not be dispatched")

    for calculate in (bounds.lineage_closure_exposure, ancestry.shared_ancestry_dependence):
        for invalid in (None, {}, Hostile()):
            with pytest.raises(CanonicalValidationError):
                calculate(invalid)
        for field, value in (("closed_record_count", True), ("grounded_record_count", 4),
                             ("unresolved_record_count", 0), ("records", source.records[:-1]),
                             ("root_contributions", ()), ("resolved_lineage_coverage", 1.0),
                             ("execution_status", ExecutionStatus.COMPLETED)):
            forged = replace(source)
            object.__setattr__(forged, field, value)
            with pytest.raises(CanonicalValidationError):
                calculate(forged)


def test_pure_summaries_do_not_rerun_graph_or_access_files_network_or_raw_data(tmp_path, monkeypatch):
    source = _mixed_analysis(tmp_path)

    def blocked(*args, **kwargs):
        raise AssertionError("a typed summary must not perform I/O or repeat graph resolution")

    with monkeypatch.context() as patch:
        patch.setattr(builtins, "open", blocked)
        patch.setattr(Path, "open", blocked)
        patch.setattr(socket, "socket", blocked)
        patch.setattr(socket, "create_connection", blocked)
        patch.setattr(graph, "build_lineage_graph", blocked)
        patch.setattr(cycles, "analyze_cycles", blocked)
        patch.setattr(ancestry, "build_lineage_graph", blocked)
        patch.setattr(ancestry, "analyze_cycles", blocked)
        patch.setattr(ancestry, "analyze_lineage", blocked)
        patch.setattr(ancestry, "_resolve_roots", blocked)
        patch.setattr(ancestry, "join_provenance", blocked)
        interval = bounds.lineage_closure_exposure(source)
        proxy = ancestry.shared_ancestry_dependence(source)
    _assert_interval(interval, ("1/4", "1/2", "1/4"))
    assert proxy.level == "present"
    for value in (interval, proxy, interval.source, proxy.source):
        assert "Private ancestry fixture" not in repr(value)
        assert str(tmp_path) not in repr(value)
        for name in ("content", "content_ref", "uri", "local_path", "provenance"):
            assert not hasattr(value, name)
