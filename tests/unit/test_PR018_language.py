"""Phase 1 placeholder for PR-018.

Planned scope:
    Future report-language tests are deferred to Phase 4.

Current Phase 1 scope:
    Verify the approved owner ID and confirm that the target module remains a
    docstring-only, import-safe placeholder.

Limits:
    No mathematical metric, data loading, graph operation, or report result is tested.
"""


def test_PR018_language_owner_and_placeholder(owner_checker, placeholder_checker,phase3_final_owner_checker,phase3_final_placeholder_checker):
    owner_checker = phase3_final_owner_checker
    placeholder_checker = phase3_final_placeholder_checker
    owner_checker("reports/markdown_report.py", "PR-018")
    placeholder_checker("reports/markdown_report.py")


# Phase 4 Step 3: independently authored report assembly expectations.
def phase4_step3_run():
    return {
        "run_id": "step3-independent-case", "toolkit_version": "0.1.0.dev2",
        "report_schema_version": "1.0", "started_at": None, "completed_at": None,
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


def phase4_step3_provenance(bundle, *, weights=None):
    from recursive_integrity_toolkit.metrics.provenance import summarize_provenance
    from recursive_integrity_toolkit.models import CalculationScope, WeightingOptions

    joined = bundle.provenance_join
    scope = CalculationScope(("v1",), joined.scope_record_keys, (),
                             joined.provenance_row_coverage.denominator_name, "provenance-v1")
    if weights is None:
        return summarize_provenance(joined, scope=scope)
    return summarize_provenance(joined, scope=scope,
                                weighting=WeightingOptions("weighted", "weight"), weights=weights)


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


def test_phase4_step3_tail_proxy_names_basis_rule_and_forecast_limitation(tmp_path, repo_root):
    from recursive_integrity_toolkit.metrics.tail import select_tail
    from recursive_integrity_toolkit.models import TailSelectionOptions
    from recursive_integrity_toolkit.reports.assembly import assemble_report

    bundle = phase4_step3_bundle(tmp_path)
    distribution = phase4_step3_distribution(bundle)
    tail = select_tail(distribution.unweighted, options=TailSelectionOptions("singleton_count"))
    report = phase4_step3_schema(assemble_report(bundle, run=phase4_step3_run(), distributions=(distribution,), tail=tail), repo_root)
    signal = report["proxy_signals"]["tail_fragility"]
    assert signal["evidence_class"] == "proxy_signal" and signal["level"] == "present"
    assert signal["trigger_rule"] and signal["basis_fields"]
    assert any("tail" in path for path in signal["basis_fields"])
    assert "This signal is not a calibrated forecast of the production pipeline." in signal["limitations"]
    assert report["derived_metrics"]["tail"]["tail_states"]["value"] == ["b", "c"]
    assert report["derived_metrics"]["tail"]["tail_support_size"]["value"] == 2
    assert report["simulations"] == {}


def test_phase4_step3_proxy_basis_paths_resolve_and_never_claim_causal_error(tmp_path, repo_root):
    from recursive_integrity_toolkit.reports.assembly import assemble_report

    bundle = phase4_step3_bundle(tmp_path)
    report = phase4_step3_schema(assemble_report(bundle, run=phase4_step3_run(),
        provenance=phase4_step3_provenance(bundle)), repo_root)
    for name, signal in report["proxy_signals"].items():
        assert signal["evidence_class"] == "proxy_signal"
        assert signal["level"] in ("present", "not_present", "indeterminate")
        assert signal["limitations"] and signal["trigger_rule"]
        if signal["status"] != "unavailable":
            assert signal["basis_fields"]
            for path in signal["basis_fields"]:
                value = report
                for component in path.split("."):
                    value = value[component]
        assert name != "correlated_error"
    assert "ancestry_concentration" not in report["proxy_signals"]
    if "shared_ancestry_dependence" in report["proxy_signals"]:
        signal = report["proxy_signals"]["shared_ancestry_dependence"]
        assert signal["status"] == "unavailable" and signal["level"] == "indeterminate"


def test_phase4_step3_recommendations_are_actionable_metadata_requests_with_scope(tmp_path, repo_root):
    from recursive_integrity_toolkit.reports.assembly import assemble_report

    bundle = phase4_step3_bundle(tmp_path, representation=False)
    report = phase4_step3_schema(assemble_report(bundle, run=phase4_step3_run()), repo_root)
    recommendations = report["recommended_next_metadata"]
    assert recommendations
    for item in recommendations:
        assert type(item["priority"]) is int and item["priority"] > 0
        assert item["metadata"] and item["scope"] and item["expected_unlock"] and item["reason"]
    combined = " ".join(item["metadata"] + " " + item["reason"] for item in recommendations).lower()
    assert "representation" in combined and "provenance" in combined
    assert "model" in combined and "performance" in combined


def test_phase4_step3_proxy_trigger_and_recommendation_order_are_deterministic(tmp_path, repo_root):
    from recursive_integrity_toolkit.reports.assembly import assemble_report

    bundle = phase4_step3_bundle(tmp_path)
    provenance = phase4_step3_provenance(bundle)
    first = phase4_step3_schema(assemble_report(bundle, run=phase4_step3_run(), provenance=provenance), repo_root)
    second = phase4_step3_schema(assemble_report(bundle, run=phase4_step3_run(), provenance=provenance), repo_root)
    assert first["proxy_signals"] == second["proxy_signals"]
    assert first["unavailable_conclusions"] == second["unavailable_conclusions"]
    assert first["recommended_next_metadata"] == second["recommended_next_metadata"]
    signal = first["proxy_signals"]["provenance_uncertainty"]
    assert signal["level"] == "present"
    assert signal["basis_fields"] and signal["limitations"]


def test_phase4_step3_standard_assembly_rejects_unperformed_redaction_claim(tmp_path):
    import pytest
    from recursive_integrity_toolkit.reports.assembly import assemble_report

    bundle = phase4_step3_bundle(tmp_path)
    run = phase4_step3_run()
    run["privacy_mode"], run["redacted_mode"] = "redacted", True
    with pytest.raises((TypeError, ValueError)):
        assemble_report(bundle, run=run)


def test_phase4_step3_empty_tail_is_not_present_and_simulation_alone_is_not_tail_evidence(tmp_path, repo_root):
    from recursive_integrity_toolkit.metrics.tail import select_tail, one_step_extinction_probability
    from recursive_integrity_toolkit.models import TailSelectionOptions
    from recursive_integrity_toolkit.reports.assembly import assemble_report

    bundle = phase4_step3_bundle(tmp_path, ("a", "a", "b", "b"))
    distribution = phase4_step3_distribution(bundle)
    tail = select_tail(distribution.unweighted, options=TailSelectionOptions("singleton_count"))
    report = phase4_step3_schema(assemble_report(bundle, run=phase4_step3_run(), distributions=(distribution,), tail=tail), repo_root)
    assert report["derived_metrics"]["tail"]["tail_support_size"]["value"] == 0
    assert report["proxy_signals"]["tail_fragility"]["level"] == "not_present"
    scenario = one_step_extinction_probability(1 / 2, state_id="a", resample_size=4,
        scope=distribution.unweighted.scope, representation=distribution.unweighted.representation)
    alone = phase4_step3_schema(assemble_report(bundle, run=phase4_step3_run(), extinction=(scenario,)), repo_root)
    assert "tail_fragility" not in alone["proxy_signals"]
