"""Phase 1 placeholder for PR-014.

Planned scope:
    Future unavailable-conclusion tests are deferred to Phase 4.

Current Phase 1 scope:
    Verify the approved owner ID and confirm that the target module remains a
    docstring-only, import-safe placeholder.

Limits:
    No mathematical metric, data loading, graph operation, or report result is tested.
"""


# Phase 4 Step 3: independently authored report assembly expectations.
def phase4_step3_run():
    return {
        "run_id": "step3-independent-case", "toolkit_version": "0.1.0.dev2",
        "report_schema_version": "1.1", "started_at": None, "completed_at": None,
        "duration_seconds": None, "python_version": None, "platform": None,
        "command": None, "config_hash": None, "random_seed": None,
        "strict_mode": False, "redacted_mode": False, "network_call_count": 0,
        "deterministic": True, "privacy_mode": "standard", "run_status": "complete",
        "null_reasons": {
            "started_at": "Pure assembly does not start a clock.",
            "completed_at": "Pure assembly does not start a clock.",
            "duration_seconds": "Pure assembly does not measure execution.",
            "python_version": "No execution environment is asserted.",
            "platform": "No execution environment is asserted.",
            "command": "Direct Python API, no command invoked.",
            "config_hash": "No resolved configuration hash was supplied.",
            "random_seed": "No run-wide random generator was requested.",
        },
    }


def phase4_step3_bundle(tmp_path, labels=("a", "a", "b", "c"), *,
                        provenance_rows=None, versions=None, representation=True):
    import json
    from recursive_integrity_toolkit.io.validation import validate_bundle
    from recursive_integrity_toolkit.models import AuditBundle, FileRole, InputSource

    if not labels:
        from recursive_integrity_toolkit.models import (
            BundleValidationResult, Capability, CapabilityKey, CapabilityStatus,
            ObservabilityAssessment, ProvenanceJoinResult, ValidationCoverage, VersionOrderResult,
        )
        coverage = ValidationCoverage(0, 0, "selected_valid_records")
        joined = ProvenanceJoinResult((), (), False, (), (), coverage, coverage, coverage, ())
        order = VersionOrderResult((), (), "unavailable", {}, {})
        assessment = ObservabilityAssessment(0, {
            key: Capability(CapabilityStatus.UNAVAILABLE, coverage,
                            requirements_missing=("valid records",), reason_codes=("R_EMPTY_SCOPE",))
            for key in CapabilityKey
        }, limitations=("No records were supplied.",))
        return BundleValidationResult((), (), None, joined, order, None, assessment, (), (), ())
    versions = ("v1",) * len(labels) if versions is None else versions
    records = [dict(dataset_version=version, record_id="r" + str(index),
                    content="synthetic public fixture", topic=label)
               for index, (version, label) in enumerate(zip(versions, labels))]
    tmp_path.mkdir(parents=True, exist_ok=True)
    path = tmp_path / "records.jsonl"
    path.write_text("".join(json.dumps(row) + "\n" for row in records), encoding="utf-8")
    sources = [InputSource(FileRole.RECORDS_PRIMARY, path)]
    if provenance_rows is not None:
        path = tmp_path / "provenance.jsonl"
        path.write_text("".join(json.dumps(row) + "\n" for row in provenance_rows), encoding="utf-8")
        sources.append(InputSource(FileRole.PROVENANCE_MANIFEST, path))
    config = {}
    if representation:
        config["representation"] = {
            "name": "topic", "source": "topic_field", "field": "topic",
            "version": "taxonomy-v1", "missing_value_policy": "exclude",
        }
    if len(set(versions)) > 1:
        config["version_order"] = list(dict.fromkeys(versions))
    return validate_bundle(AuditBundle(tuple(sources)), configuration=config)


def phase4_step3_distribution(bundle, version="v1", *, weights=None):
    from recursive_integrity_toolkit.config import RepresentationConfig
    from recursive_integrity_toolkit.metrics.diversity import calculate_state_distribution
    from recursive_integrity_toolkit.models import WeightingOptions
    from recursive_integrity_toolkit.representations.field import assign_field_states

    represented = assign_field_states(
        bundle.records, dataset_versions=(version,), scope_id="report-" + version,
        config=RepresentationConfig("topic", "topic_field", "topic", "taxonomy-v1", "exclude"),
    )
    if weights is None:
        return calculate_state_distribution(represented)
    return calculate_state_distribution(represented, weighting=WeightingOptions("weighted", "weight"),
                                        weights=weights)


def phase4_step3_schema(report, repo_root):
    import json
    from jsonschema import Draft202012Validator

    payload = report.to_dict()
    schema = json.loads((repo_root / "schemas/report.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator(schema).validate(payload)
    assert tuple(payload) == (
        "run", "inputs", "observability", "capabilities", "observed_facts",
        "derived_metrics", "proxy_signals", "simulations", "unavailable_conclusions",
        "recommended_next_metadata", "warnings", "errors",
    )
    assert payload["observability"]["capabilities"] == payload["capabilities"]
    return payload


def test_phase4_step3_default_report_discloses_unsupported_conclusions_without_zero(tmp_path, repo_root):
    from recursive_integrity_toolkit.reports.assembly import assemble_report

    bundle = phase4_step3_bundle(tmp_path)
    report = phase4_step3_schema(assemble_report(bundle, run=phase4_step3_run()), repo_root)
    conclusions = {item["conclusion"]: item for item in report["unavailable_conclusions"]}
    assert {"model_performance_decline", "causal_ancestor_effect", "universal_integrity",
            "universal_collapse_prediction", "lineage_analysis", "lineage_closure_exposure",
            "complete_pipeline_closure"} <= set(conclusions)
    for item in conclusions.values():
        assert item["evidence_class"] == "unavailable_conclusion"
        assert item["status"] == "unavailable"
        assert item["reason_codes"] and item["required_evidence"]
        assert "value" not in item
    assert report["run"]["run_status"] == "complete"
    assert report["simulations"] == {} and not report["errors"]


def test_phase4_step3_no_representation_keeps_inputs_and_explicit_analysis_limit(tmp_path, repo_root):
    from recursive_integrity_toolkit.reports.assembly import assemble_report

    bundle = phase4_step3_bundle(tmp_path, representation=False)
    report = phase4_step3_schema(assemble_report(bundle, run=phase4_step3_run()), repo_root)
    assert report["inputs"]["scope"]["record_count"] == 4
    assert not report["derived_metrics"].get("support", {}).get("by_version")
    assert not report["derived_metrics"].get("diversity", {}).get("by_version")
    text = " ".join(item["metadata"] + " " + item["reason"] for item in report["recommended_next_metadata"]).lower()
    assert "representation" in text
    assert report["capabilities"]["content_diagnostics"]["execution_status"] == "not_requested"


def test_phase4_step3_all_excluded_representation_remains_unavailable_with_original_scope(tmp_path, repo_root):
    from recursive_integrity_toolkit.reports.assembly import assemble_report

    bundle = phase4_step3_bundle(tmp_path, (None, None))
    result = phase4_step3_distribution(bundle)
    report = phase4_step3_schema(assemble_report(bundle, run=phase4_step3_run(), distributions=(result,)), repo_root)
    metric = report["derived_metrics"]["support"]["by_version"]["v1"]["support_size"]
    assert metric["value"] is None and metric["status"] == "unavailable"
    assert metric["reason_codes"] and metric["required_evidence"]
    assert metric["scope"]["record_count"] == 0
    assert metric["scope"]["excluded_record_count"] == 2
    assert metric["scope"]["exclusions"] == [
        {"record_key": {"dataset_version": "v1", "record_id": "r0"},
         "reason_codes": ["R_CALC_REPRESENTATION_MISSING"]},
        {"record_key": {"dataset_version": "v1", "record_id": "r1"},
         "reason_codes": ["R_CALC_REPRESENTATION_MISSING"]},
    ]
    assert metric["coverage"] == 0
    assert report["inputs"]["scope"]["record_count"] == 2


def test_phase4_step3_family_failure_keeps_usable_single_version_evidence(tmp_path, repo_root):
    from recursive_integrity_toolkit.models import CapabilityKey, ValidationMessage, ValidationSeverity
    from recursive_integrity_toolkit.reports.assembly import FamilyFailure, assemble_report

    bundle = phase4_step3_bundle(tmp_path)
    result = phase4_step3_distribution(bundle)
    failure = FamilyFailure(CapabilityKey.DATASET_LONGITUDINAL, (
        ValidationMessage("E_SCHEMA_TYPE", ValidationSeverity.ERROR,
                          "Selected representations are incompatible; provide an explicit compatible declaration."),))
    report = phase4_step3_schema(assemble_report(bundle, run=phase4_step3_run(),
        distributions=(result,), family_errors=(failure,)), repo_root)
    assert report["derived_metrics"]["diversity"]["by_version"]["v1"]["gini_simpson_diversity"]["value"] == 5 / 8
    assert report["capabilities"]["dataset_longitudinal"]["execution_status"] == "failed"
    assert report["run"]["run_status"] == "partial"
    assert report["errors"][0]["code"] == "E_SCHEMA_TYPE"
    assert "dataset_longitudinal" in report["errors"][0]["effect_on_capabilities"]
    assert "support_delta" not in report["derived_metrics"]["support"]


def test_phase4_step3_family_failure_contract_rejects_warning_only_and_forged_types(tmp_path):
    import pytest
    from recursive_integrity_toolkit.models import CapabilityKey, ValidationMessage, ValidationSeverity
    from recursive_integrity_toolkit.reports.assembly import FamilyFailure, assemble_report

    bundle = phase4_step3_bundle(tmp_path)
    for messages in ((), (ValidationMessage("W_PROVENANCE_MISSING_ROW", ValidationSeverity.WARNING,
                                             "Required metadata has not been supplied."),)):
        with pytest.raises((TypeError, ValueError)):
            failure = FamilyFailure(CapabilityKey.PROVENANCE, messages)
            assemble_report(bundle, run=phase4_step3_run(), family_errors=(failure,))
    with pytest.raises((TypeError, ValueError)):
        assemble_report(bundle, run=phase4_step3_run(), family_errors=({"capability": "lineage"},))


def test_phase4_step3_error_only_empty_input_keeps_null_missingness_and_diagnostics(tmp_path, repo_root):
    from recursive_integrity_toolkit.reports.assembly import assemble_report

    bundle = phase4_step3_bundle(tmp_path, ())
    report = phase4_step3_schema(assemble_report(bundle, run=phase4_step3_run()), repo_root)
    assert report["inputs"]["scope"]["record_count"] == 0
    assert report["inputs"]["scope"]["dataset_versions"] == []
    assert report["simulations"] == {}
    assert not report["derived_metrics"].get("support", {}).get("by_version")
    assert report["observability"]["maximum_level"] == bundle.observability.maximum_level
    assert not report["observed_facts"].get("state_counts", {}).get("by_version")


def test_phase4_step3_fatal_family_error_forces_failed_run_despite_surviving_evidence(tmp_path, repo_root):
    from recursive_integrity_toolkit.models import CapabilityKey, ValidationMessage, ValidationSeverity
    from recursive_integrity_toolkit.reports.assembly import FamilyFailure, assemble_report

    bundle = phase4_step3_bundle(tmp_path)
    distribution = phase4_step3_distribution(bundle)
    failure = FamilyFailure(CapabilityKey.CONTENT_DIAGNOSTICS, (
        ValidationMessage("E_INTERNAL", ValidationSeverity.FATAL, "A required invariant failed."),))
    report = phase4_step3_schema(assemble_report(bundle, run=phase4_step3_run(),
        distributions=(distribution,), family_errors=(failure,)), repo_root)
    assert report["run"]["run_status"] == "failed"
    assert report["derived_metrics"]["support"]["by_version"]["v1"]["support_size"]["value"] == 3
    assert any(item["severity"] == "fatal" for item in report["errors"])


def test_phase4_step3_failed_content_subfamily_keeps_completed_distribution_and_partial_status(tmp_path, repo_root):
    from recursive_integrity_toolkit.models import CapabilityKey, ValidationMessage, ValidationSeverity
    from recursive_integrity_toolkit.reports.assembly import FamilyFailure, assemble_report

    bundle = phase4_step3_bundle(tmp_path)
    distribution = phase4_step3_distribution(bundle)
    failure = FamilyFailure(CapabilityKey.CONTENT_DIAGNOSTICS, (
        ValidationMessage("E_FILE_PARSE", ValidationSeverity.ERROR, "Explicit content evidence could not be read."),))
    report = phase4_step3_schema(assemble_report(bundle, run=phase4_step3_run(),
        distributions=(distribution,), family_errors=(failure,)), repo_root)
    assert report["run"]["run_status"] == "partial"
    assert report["capabilities"]["content_diagnostics"]["execution_status"] == "partial"
    assert report["derived_metrics"]["diversity"]["by_version"]["v1"]["gini_simpson_diversity"]["value"] == 5 / 8
    assert any("content_diagnostics" in item["effect_on_capabilities"] for item in report["errors"])
