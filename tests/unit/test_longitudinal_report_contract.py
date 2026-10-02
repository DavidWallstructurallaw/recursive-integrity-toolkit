"""Canonical series mutation tests at the public, computation-free boundary."""
from copy import deepcopy

import pytest

from recursive_integrity_toolkit.metrics.longitudinal import analyze_longitudinal
from recursive_integrity_toolkit.reports.assembly import assemble_report, privacy_view
from recursive_integrity_toolkit.result import ReportValidationError, validate_report
from recursive_integrity_toolkit.utils.hashing import IdentifierProtection
from test_longitudinal_analysis import _select
from test_longitudinal_fixture_inputs import _load_case
from test_longitudinal_selection import _case
from test_PR012_evidence_classes import phase4_step2_evidence_report_fixture


@pytest.fixture(scope="module")
def supplied_report(tmp_path_factory):
    case = _case("lineage_complete")
    bundle = _load_case(case, tmp_path_factory.mktemp("series_contract"))
    result = analyze_longitudinal(bundle, selection=_select(case, bundle), lineage=True)
    return assemble_report(bundle, run=phase4_step2_evidence_report_fixture()["run"],
                           longitudinal=result)


def _snapshot(payload, index=0):
    return payload["derived_metrics"]["longitudinal"]["snapshots"][index]


def _comparison(payload, index=0):
    return payload["derived_metrics"]["longitudinal"]["comparisons"][index]


def _inputs(payload):
    return payload["inputs"]["longitudinal"]


def _execution(payload):
    return payload["capabilities"]["dataset_longitudinal"]["longitudinal_execution"]


def _mutate(payload, case):
    if case == "foreign_snapshot_scope":
        _snapshot(payload)["support_size"]["scope_id"] = "s0002.representation"
    elif case == "foreign_pair_scope":
        _comparison(payload)["record_count_delta"]["earlier_scope_id"] = "s0003.population"
    elif case == "invented_scope":
        _comparison(payload)["support_delta"]["later_scope_id"] = "missing.scope"
    elif case == "foreign_basis":
        _snapshot(payload)["support_size"]["basis_id"] = "b9999"
    elif case == "duplicate_snapshot":
        _inputs(payload)["snapshots"].append(deepcopy(_inputs(payload)["snapshots"][0]))
    elif case == "duplicate_pair":
        _inputs(payload)["comparisons"].append(deepcopy(_inputs(payload)["comparisons"][0]))
    elif case == "wrong_pair_order":
        _inputs(payload)["comparisons"][1:3] = list(reversed(_inputs(payload)["comparisons"][1:3]))
    elif case == "wrong_version_order":
        a, b = _inputs(payload)["snapshots"][:2]
        a["dataset_version"], b["dataset_version"] = b["dataset_version"], a["dataset_version"]
    elif case == "wrong_population":
        _inputs(payload)["scopes"][0]["record_count"] += 1
    elif case == "wrong_delta":
        _comparison(payload)["ancestry_concentration_hhi_delta"]["value"] += 0.1
    elif case == "forged_endpoints":
        envelope = _comparison(payload)["record_count_delta"]
        envelope["earlier_value"] += 1
        envelope["later_value"] += 1
    elif case == "wrong_endpoint_denominator":
        _comparison(payload)["ancestry_concentration_hhi_delta"]["earlier_denominator"] += 1
    elif case == "wrong_endpoint_coverage":
        coverage = _comparison(payload)["ancestry_concentration_hhi_delta"]["earlier_coverage"]
        coverage["numerator"] = 0
        coverage["ratio"] = 0
    elif case == "missing_endpoint_coverage":
        _comparison(payload)["ancestry_concentration_hhi_delta"]["earlier_coverage"] = None
    elif case == "wrong_endpoint_coverage_population":
        coverage = _comparison(payload)["ancestry_concentration_hhi_delta"]["earlier_coverage"]
        coverage["numerator"] *= 2
        coverage["denominator"] *= 2
    elif case == "wrong_endpoint_reason":
        _comparison(payload)["ancestry_concentration_hhi_delta"]["earlier_reason_codes"] = ["NO_RESOLVED_EXTERNAL_ROOTS"]
    elif case == "wrong_owner":
        _comparison(payload)["record_count_delta"]["owner_ids"] = ["PR-002"]
    elif case == "wrong_method":
        _snapshot(payload)["ancestry_concentration_hhi"]["method_id"] = "F-013"
    elif case == "false_count":
        _snapshot(payload)["grounded_record_count"]["value"] = True
    elif case == "wrong_partition":
        _snapshot(payload)["grounded_record_count"]["value"] -= 1
    elif case == "false_root_zero":
        _snapshot(payload)["distinct_external_root_count"]["value"] = 0
    elif case == "wrong_interval":
        _snapshot(payload)["lineage_closure_interval_width"]["value"] = 0.1
    elif case == "common_delta_denominator":
        _comparison(payload)["record_count_delta"]["denominator"] = 4
    elif case == "weighted_series":
        _comparison(payload)["record_count_delta"]["weighting"] = {"weighting_mode": "weighted", "weight_field": "weight"}
    elif case == "invented_input_basis":
        _comparison(payload)["record_count_delta"]["input_basis"] = "unknown"
    elif case == "missing_version_redaction":
        _inputs(payload)["snapshots"][0]["dataset_version"] = None
    elif case == "false_detail_count":
        _comparison(payload)["extinct_states"]["value"]["total_count"] += 1
    elif case == "capability_execution_mismatch":
        payload["capabilities"]["dataset_longitudinal"]["execution_status"] = "partial"
        payload["capabilities"]["dataset_longitudinal"]["execution_reason_codes"] = ["R_LONGITUDINAL_ENDPOINT_UNAVAILABLE"]
    elif case == "failed_with_useful_comparisons":
        _execution(payload)["status"] = "failed"
        _execution(payload)["reason_codes"] = ["R_LONGITUDINAL_ENDPOINT_UNAVAILABLE"]
        payload["capabilities"]["dataset_longitudinal"]["execution_status"] = "failed"
        payload["capabilities"]["dataset_longitudinal"]["execution_reason_codes"] = ["R_LONGITUDINAL_ENDPOINT_UNAVAILABLE"]
    elif case == "extra_unreferenced_scope":
        extra = deepcopy(_inputs(payload)["scopes"][0])
        extra["scope_id"] = "extra.population"
        _inputs(payload)["scopes"].append(extra)
    elif case == "wrong_shared_node_count":
        payload["observed_facts"]["longitudinal"]["shared_lineage"]["loaded_record_count"] = 0
    elif case == "wrong_shared_edge_count":
        payload["observed_facts"]["longitudinal"]["shared_lineage"]["unique_edge_count"] += 1
    else:
        raise AssertionError(case)
    payload["observability"]["capabilities"] = deepcopy(payload["capabilities"])


@pytest.mark.parametrize("case", (
    "foreign_snapshot_scope", "foreign_pair_scope", "invented_scope", "foreign_basis",
    "duplicate_snapshot", "duplicate_pair", "wrong_pair_order", "wrong_version_order",
    "wrong_population", "wrong_delta", "forged_endpoints", "wrong_endpoint_denominator",
    "wrong_endpoint_coverage", "missing_endpoint_coverage", "wrong_endpoint_coverage_population",
    "wrong_endpoint_reason", "wrong_owner", "wrong_method", "false_count", "wrong_partition",
    "false_root_zero", "wrong_interval", "common_delta_denominator", "weighted_series",
    "invented_input_basis", "missing_version_redaction", "false_detail_count",
    "capability_execution_mismatch", "failed_with_useful_comparisons", "extra_unreferenced_scope",
    "wrong_shared_node_count", "wrong_shared_edge_count",
))
def test_canonical_report_rejects_inconsistent_series_handoffs(supplied_report, case):
    payload = supplied_report.to_dict()
    _mutate(payload, case)
    with pytest.raises(ReportValidationError):
        validate_report(payload)


def test_identity_omission_keeps_valid_rows_and_rejects_unmarked_nulls(supplied_report):
    view = privacy_view(supplied_report, mode="redacted", record_id_mode="omit",
                        protection=IdentifierProtection(secret=b"series-contract-only-secret-key!"))
    payload = view.to_dict()
    validate_report(payload)
    assert _inputs(payload)["snapshots"][0]["dataset_version"] is None
    _inputs(payload)["snapshots"][0]["redaction"] = None
    with pytest.raises(ReportValidationError):
        validate_report(payload)


@pytest.mark.parametrize("field", ("later_reason_codes", "earlier_coverage", "later_coverage"))
def test_zero_grounded_endpoint_cannot_drop_reasons_or_coverage(tmp_path, field):
    case = _case("lineage_zero_grounded")
    bundle = _load_case(case, tmp_path)
    result = analyze_longitudinal(bundle, selection=_select(case, bundle), lineage=True)
    payload = assemble_report(bundle, run=phase4_step2_evidence_report_fixture()["run"],
                              longitudinal=result).to_dict()
    envelope = _comparison(payload, -1)["ancestry_concentration_hhi_delta"]
    assert envelope["later_reason_codes"] == ["NO_RESOLVED_EXTERNAL_ROOTS"]
    envelope[field] = [] if field == "later_reason_codes" else None
    with pytest.raises(ReportValidationError):
        validate_report(payload)


@pytest.mark.parametrize("record_id_mode", ("hash", "omit"))
def test_safe_duplicate_diagnostics_preserve_distinct_source_events(tmp_path, record_id_mode):
    case = _case("lineage_partial")
    case["provenance"][-3]["parent_ids"] = ["anchors::missing"]
    bundle = _load_case(case, tmp_path)
    result = analyze_longitudinal(bundle, selection=_select(case, bundle), lineage=True)
    report = assemble_report(bundle, run=phase4_step2_evidence_report_fixture()["run"],
                             longitudinal=result)
    detail = report.to_dict()["observed_facts"]["longitudinal"]["shared_lineage"]["graph_diagnostics"]
    assert detail["total_count"] == len(result.shared_lineage.messages)
    assert detail["total_count"] >= 2
    assert len({tuple(row.items()) for row in detail["items"]}) < len(detail["items"])
    protected = privacy_view(report, mode="redacted", record_id_mode=record_id_mode,
        protection=IdentifierProtection(secret=b"series-diagnostic-test-secret-key!")).to_dict()
    validate_report(protected)
    safe_detail = protected["observed_facts"]["longitudinal"]["shared_lineage"]["graph_diagnostics"]
    assert safe_detail["total_count"] == detail["total_count"]
    assert safe_detail["returned_count"] + safe_detail["omitted_count"] == detail["total_count"]
