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


# Phase 4 Step 4: independent content-safe diagnostic sink expectations.
def phase4_step4_diagnostic_context():
    from recursive_integrity_toolkit.utils.hashing import IdentifierProtection

    return IdentifierProtection.create(secret=b"diagnostic-test-only-key-32-bytes!!")


def test_phase4_step4_standard_diagnostic_replaces_raw_parser_notes_embeddings_and_secrets():
    import json
    from recursive_integrity_toolkit.models import FileRole, RecordKey, ValidationMessage, ValidationSeverity
    from recursive_integrity_toolkit.utils.logging import format_diagnostic

    sentinels = ["RAW_CONTENT_SENTINEL", "PRIVATE_NOTE_SENTINEL", "SECRET_TOKEN_SENTINEL", "VECTOR_1.324_SENTINEL"]
    message = ValidationMessage("E_FILE_PARSE", ValidationSeverity.ERROR, " ".join(sentinels),
        file_role=FileRole.RECORDS_PRIMARY, file_path="/private/PATH_SENTINEL.jsonl",
        field="content", record_key=RecordKey("version-public", "record-public"), row_number=7, line_number=8)
    output = format_diagnostic(message, effect_on_capabilities=("ingestion",),
                               protection=phase4_step4_diagnostic_context())
    assert all(sentinel not in output for sentinel in sentinels + ["PATH_SENTINEL"])
    payload = json.loads(output)
    assert payload["code"] == "E_FILE_PARSE" and payload["severity"] == "error"
    assert payload["file_role"] == "records_primary" and payload["field"] == "content"
    assert payload["row_number"] == 7 and payload["line_number"] == 8
    assert payload["record_key"] == {"dataset_version": "version-public", "record_id": "record-public"}
    assert payload["effect_on_capabilities"] == ["ingestion"]
    assert payload["effect_on_run"] == "partial"
    assert payload["message"] == "A local input could not be parsed."
    assert payload["remediation"] == ["Correct the input syntax at the reported location."]


def test_phase4_step4_all_registered_diagnostic_codes_keep_identity_and_actionable_guidance():
    from recursive_integrity_toolkit.errors import ErrorCode, WarningCode
    from recursive_integrity_toolkit.models import ValidationMessage, ValidationSeverity
    from recursive_integrity_toolkit.utils.logging import safe_diagnostic

    context = phase4_step4_diagnostic_context()
    for code in (*ErrorCode, *WarningCode):
        severity = ValidationSeverity.WARNING if code.value.startswith("W_") else ValidationSeverity.ERROR
        payload = safe_diagnostic(ValidationMessage(code.value, severity, "NEVER_ECHO_SENTINEL"), protection=context)
        assert payload["code"] == code.value
        assert payload["severity"] == severity.value
        assert "Unregistered diagnostic" not in payload["message"]
        assert len(payload["remediation"]) == 1 and len(payload["remediation"][0]) > 20
        assert "NEVER_ECHO_SENTINEL" not in repr(payload)


def test_phase4_step4_unknown_diagnostic_codes_are_protected_without_reclassification():
    from recursive_integrity_toolkit.models import ValidationMessage, ValidationSeverity
    from recursive_integrity_toolkit.utils.logging import safe_diagnostic

    context = phase4_step4_diagnostic_context()
    message = ValidationMessage("CUSTOM_SECRET_CODE_SENTINEL", ValidationSeverity.WARNING,
        "FREE_TEXT_SENTINEL", field="MAPPING_SECRET_FIELD_SENTINEL")
    first = safe_diagnostic(message, mode="standard", protection=context,
                            effect_on_capabilities=("provenance",))
    second = safe_diagnostic(message, mode="redacted", protection=context,
                             effect_on_capabilities=("provenance",))
    assert first == second
    assert first["code"] == context.pseudonym("diagnostic_code", "CUSTOM_SECRET_CODE_SENTINEL")
    assert first["code"] != "E_INTERNAL" and first["severity"] == "warning"
    assert first["field"] is None and first["effect_on_run"] is None
    assert first["effect_on_capabilities"] == ["provenance"]
    assert first["message"] == "Unregistered diagnostic; supplied details withheld."
    assert "SENTINEL" not in repr(first)
    assert safe_diagnostic(message)["code"] != safe_diagnostic(message)["code"]


def test_phase4_step4_redacted_record_key_uses_shared_unambiguous_identity_domains():
    from recursive_integrity_toolkit.models import RecordKey, ValidationMessage, ValidationSeverity
    from recursive_integrity_toolkit.utils.logging import safe_diagnostic

    context = phase4_step4_diagnostic_context()
    message = ValidationMessage("E_SCHEMA_TYPE", ValidationSeverity.ERROR, "BODY_SENTINEL",
        record_key=RecordKey("VERSION_SENTINEL", "RECORD_SENTINEL"))
    payload = safe_diagnostic(message, mode="redacted", protection=context)
    assert payload["record_key"] == {
        "dataset_version": context.pseudonym("dataset_version", "VERSION_SENTINEL"),
        "record_id": context.pseudonym("record_id", ["VERSION_SENTINEL", "RECORD_SENTINEL"]),
    }
    assert "SENTINEL" not in repr(payload)
    other = ValidationMessage("E_SCHEMA_TYPE", ValidationSeverity.ERROR, "BODY_SENTINEL",
        record_key=RecordKey("OTHER_VERSION_SENTINEL", "RECORD_SENTINEL"))
    assert safe_diagnostic(other, mode="redacted", protection=context)["record_key"]["record_id"] != payload["record_key"]["record_id"]


def test_phase4_step4_preserve_applies_only_to_declared_record_id_and_omit_removes_key():
    from recursive_integrity_toolkit.models import RecordKey, ValidationMessage, ValidationSeverity
    from recursive_integrity_toolkit.utils.logging import safe_diagnostic

    message = ValidationMessage("E_SCHEMA_TYPE", ValidationSeverity.ERROR, "TEXT_SENTINEL",
        field="FIELD_SENTINEL", file_path="/private/PATH_SENTINEL",
        record_key=RecordKey("VERSION_SENTINEL", "EXPLICIT_RECORD_SENTINEL"))
    context = phase4_step4_diagnostic_context()
    preserved = safe_diagnostic(message, mode="redacted", record_id_mode="preserve", protection=context)
    assert preserved["record_key"]["record_id"] == "EXPLICIT_RECORD_SENTINEL"
    assert preserved["record_key"]["dataset_version"] != "VERSION_SENTINEL"
    for forbidden in ("TEXT_SENTINEL", "FIELD_SENTINEL", "PATH_SENTINEL", "VERSION_SENTINEL"):
        assert forbidden not in repr(preserved)
    omitted = safe_diagnostic(message, mode="redacted", record_id_mode="omit", protection=context)
    assert omitted["record_key"] is None
    assert "SENTINEL" not in repr(omitted)


def test_phase4_step4_strict_warning_promotion_and_fatal_effects_remain_visible():
    import pytest
    from recursive_integrity_toolkit.models import ValidationMessage, ValidationSeverity
    from recursive_integrity_toolkit.utils.logging import safe_diagnostic

    context = phase4_step4_diagnostic_context()
    promoted = safe_diagnostic(ValidationMessage("W_PROVENANCE_MISSING_ROW", ValidationSeverity.ERROR, "SECRET"),
        protection=context, effect_on_capabilities=("provenance",), effect_on_run="failed")
    assert promoted["code"] == "W_PROVENANCE_MISSING_ROW"
    assert promoted["severity"] == "error" and promoted["effect_on_run"] == "failed"
    fatal = ValidationMessage("E_FILE_PARSE", ValidationSeverity.FATAL, "SECRET")
    assert safe_diagnostic(fatal, protection=context)["effect_on_run"] == "failed"
    with pytest.raises(ValueError, match="fatal diagnostics"):
        safe_diagnostic(fatal, protection=context, effect_on_run="partial")
    with pytest.raises(ValueError, match="approved capability"):
        safe_diagnostic(fatal, protection=context, effect_on_capabilities=("SECRET_EFFECT",))


def test_phase4_step4_exception_boundary_never_evaluates_arbitrary_exception_text():
    from recursive_integrity_toolkit.utils.logging import safe_diagnostic

    class HostileException(Exception):
        @property
        def code(self):
            raise AssertionError("custom exception attributes must not be inspected")

        def __str__(self):
            raise AssertionError("exception strings must not be evaluated")

        def __repr__(self):
            raise AssertionError("exception repr must not be evaluated")

    payload = safe_diagnostic(HostileException("EXCEPTION_SECRET_SENTINEL"),
                               protection=phase4_step4_diagnostic_context())
    assert payload["severity"] == "fatal" and payload["effect_on_run"] == "failed"
    assert payload["message"] == "Unregistered diagnostic; supplied details withheld."
    assert "SENTINEL" not in repr(payload)


def test_phase4_step4_known_toolkit_exception_safe_message_label_does_not_bypass_sanitizer():
    from recursive_integrity_toolkit.errors import CanonicalValidationError, ErrorCode, IngestionError
    from recursive_integrity_toolkit.utils.logging import safe_diagnostic

    context = phase4_step4_diagnostic_context()
    exception = IngestionError(ErrorCode.FILE_PARSE, "PARSER_FRAGMENT_SENTINEL", file_role="records_primary",
                               file_path="/secret/LOCATION_SENTINEL", row_number=4, line_number=5)
    payload = safe_diagnostic(exception, protection=context)
    assert payload["code"] == "E_FILE_PARSE" and payload["row_number"] == 4 and payload["line_number"] == 5
    assert "SENTINEL" not in repr(payload)
    canonical = CanonicalValidationError(ErrorCode.SCHEMA_TYPE, "VALUE_SENTINEL", field="content",
        record_key="VERSION_SENTINEL::RECORD_SENTINEL", severity="fatal")
    protected = safe_diagnostic(canonical, mode="redacted", protection=context)
    assert protected["severity"] == "fatal" and protected["field"] == "content"
    assert "SENTINEL" not in repr(protected)


def test_phase4_step4_diagnostic_sinks_require_explicit_stream_and_reject_raw_dicts(capsys):
    import io
    import json
    import pytest
    from recursive_integrity_toolkit.models import ValidationMessage, ValidationSeverity
    from recursive_integrity_toolkit.utils.logging import emit_diagnostic

    stream = io.StringIO()
    message = ValidationMessage("E_FILE_PARSE", ValidationSeverity.ERROR, "RAW_SENTINEL\nFAKE_LOG")
    emit_diagnostic(message, stream=stream, protection=phase4_step4_diagnostic_context())
    text = stream.getvalue()
    assert text.count("\n") == 1 and "SENTINEL" not in text and "FAKE_LOG" not in text
    assert json.loads(text)["code"] == "E_FILE_PARSE"
    assert capsys.readouterr() == ("", "")
    with pytest.raises(TypeError):
        emit_diagnostic(message)
    with pytest.raises(TypeError, match="validation message or exception"):
        emit_diagnostic({"message": "RAW_SENTINEL"}, stream=stream)
    assert stream.getvalue() == text


def test_phase4_step4_diagnostic_control_characters_cannot_create_additional_lines():
    import json
    from recursive_integrity_toolkit.models import RecordKey, ValidationMessage, ValidationSeverity
    from recursive_integrity_toolkit.utils.logging import format_diagnostic

    message = ValidationMessage("E_SCHEMA_TYPE", ValidationSeverity.ERROR, "\x1b[31mSECRET",
        record_key=RecordKey("public", "record\nline\t\x1b[31m"))
    output = format_diagnostic(message)
    assert output.count("\n") == 1 and "\x1b" not in output and "\t" not in output
    assert json.loads(output)["record_key"]["record_id"] == "record\nline\t\x1b[31m"


def test_phase4_step4_invalid_diagnostic_modes_types_and_locations_fail_without_echo():
    import pytest
    from recursive_integrity_toolkit.models import ValidationMessage, ValidationSeverity
    from recursive_integrity_toolkit.utils.logging import safe_diagnostic

    message = ValidationMessage("E_FILE_PARSE", ValidationSeverity.ERROR, "SECRET_SENTINEL")
    for options in ({"mode": "debug"}, {"mode": "PRIVATE_MODE_SENTINEL"},
                    {"mode": "standard", "record_id_mode": "hash"},
                    {"mode": "redacted", "record_id_mode": "PRIVATE_MODE_SENTINEL"},
                    {"effect_on_run": "PRIVATE_EFFECT_SENTINEL"}, {"protection": object()}):
        with pytest.raises((TypeError, ValueError)) as error:
            safe_diagnostic(message, **options)
        assert "SENTINEL" not in str(error.value)
    for number in (True, 0, -1, 1.5, "POSITION_SENTINEL"):
        invalid = ValidationMessage("E_FILE_PARSE", ValidationSeverity.ERROR, "SECRET_SENTINEL", row_number=number)
        with pytest.raises(ValueError, match="positive integers"):
            safe_diagnostic(invalid)


def test_phase4_step4_sanitizer_failure_does_not_write_partial_diagnostic():
    import io
    import pytest
    from recursive_integrity_toolkit.models import ValidationMessage, ValidationSeverity
    from recursive_integrity_toolkit.utils.logging import emit_diagnostic

    stream = io.StringIO()
    invalid = ValidationMessage("E_FILE_PARSE", ValidationSeverity.ERROR, "PRIVATE_FRAGMENT", row_number=False)
    with pytest.raises(ValueError):
        emit_diagnostic(invalid, stream=stream)
    assert stream.getvalue() == ""


def test_phase4_step4_diagnostic_privacy_enums_interoperate_without_enabling_debug():
    import pytest
    from recursive_integrity_toolkit.models import PrivacyMode as InputPrivacyMode, ValidationMessage, ValidationSeverity
    from recursive_integrity_toolkit.result import PrivacyMode as OutputPrivacyMode, RecordIdMode
    from recursive_integrity_toolkit.utils.logging import safe_diagnostic

    message = ValidationMessage("E_FILE_PARSE", ValidationSeverity.ERROR, "PRIVATE_SENTINEL")
    context = phase4_step4_diagnostic_context()
    for value in ("standard", InputPrivacyMode.STANDARD, OutputPrivacyMode.STANDARD,
                  "redacted", InputPrivacyMode.REDACTED, OutputPrivacyMode.REDACTED):
        assert safe_diagnostic(message, mode=value, record_id_mode=RecordIdMode.PRESERVE,
                               protection=context)["code"] == "E_FILE_PARSE"
    with pytest.raises(ValueError, match="only standard or redacted"):
        safe_diagnostic(message, mode=InputPrivacyMode.DEBUG)


# Phase 4 Step 5: readable evidence and injection-safe Markdown.
def phase4_step5_markdown_data_strings(markdown):
    """Read quoted JSON literals inside inline code, never execute markup."""
    import json
    import re

    result = []
    for token in re.findall(r"`([^`\n]+)`", markdown):
        try:
            value = json.loads(token)
        except (ValueError, TypeError):
            continue
        if type(value) is str:
            result.append(value)
    return result


def phase4_step5_hostile_identity_payload(label):
    from test_PR012_evidence_classes import phase4_step2_metric_report_fixture

    payload = phase4_step2_metric_report_fixture()
    metric = payload["derived_metrics"]["diversity"]["by_version"].pop("v1")["gini_simpson_diversity"]
    metric["scope"]["dataset_versions"] = [label]
    metric["scope"]["scope_id"] = label
    metric["representation"]["representation_name"] = label
    payload["derived_metrics"]["diversity"]["by_version"][label] = {"gini_simpson_diversity": metric}
    return payload


def test_phase4_step5_markdown_title_twelve_headings_and_empty_sections_are_visible():
    from test_PR013_report_schema import phase4_step2_report_fixture, phase4_step5_renderers, phase4_step5_view

    _, render_markdown = phase4_step5_renderers()
    markdown = render_markdown(phase4_step5_view(phase4_step2_report_fixture()))
    assert markdown.startswith("# Recursive Integrity Audit Report\n")
    assert [line for line in markdown.splitlines() if line.startswith("## ")] == [
        "## Run metadata", "## Input inventory", "## Observability summary", "## Capability matrix",
        "## Observed facts", "## Derived metrics", "## Proxy signals", "## Simulations",
        "## Unavailable conclusions", "## Recommended next metadata", "## Warnings", "## Errors"]
    assert markdown.count("# Recursive Integrity Audit Report") == 1
    for empty in ("Input inventory", "Observability summary", "Capability matrix", "Observed facts",
                  "Derived metrics", "Proxy signals", "Simulations", "Unavailable conclusions",
                  "Recommended next metadata", "Warnings", "Errors"):
        body = markdown.split("## " + empty + "\n", 1)[1].split("\n## ", 1)[0]
        assert body.strip()


def test_phase4_step5_markdown_preserves_status_evidence_and_full_precision_with_units():
    from test_PR013_report_schema import phase4_step5_renderers, phase4_step5_rich_payload, phase4_step5_view

    _, render_markdown = phase4_step5_renderers()
    view = phase4_step5_view(phase4_step5_rich_payload())
    markdown = render_markdown(view)
    strings = phase4_step5_markdown_data_strings(markdown)
    for value in ("partial", "available", "unavailable", "deferred", "experimental",
                  "observed_fact", "derived_metric", "simulation", "unavailable_conclusion",
                  "dimensionless", "records", "ratio", "F-003", "F-009", "F-010", "T3"):
        assert value in strings or value in markdown, value
    assert "0.12345678901234566" in markdown
    assert "0.25" in markdown and "0.75" in markdown and "0.5" in markdown
    for field in ("lower_bound", "upper_bound", "interval_width", "denominator", "coverage",
                  "record_count", "excluded_record_count", "representation", "method_id",
                  "owner_ids", "trace_ids", "assumptions", "limitations", "reason_codes"):
        assert field in markdown, field
    assert "midpoint" not in markdown
    assert view.to_dict()["capabilities"]["lineage"]["coverage"] == 0.75


def test_phase4_step5_markdown_never_substitutes_unavailable_metric_with_zero():
    from test_PR012_evidence_classes import phase4_step2_metric_report_fixture
    from test_PR013_report_schema import phase4_step5_renderers, phase4_step5_view

    payload = phase4_step2_metric_report_fixture()
    metric = payload["derived_metrics"]["diversity"]["by_version"]["v1"]["gini_simpson_diversity"]
    metric.update({"value": None, "status": "unavailable", "representation": None,
        "coverage": None, "coverage_reason": "No selected-state distribution was supplied.",
        "denominator": None, "denominator_reason": "No eligible records were supplied.",
        "reason_codes": ["R_REPRESENTATION_NOT_DECLARED"],
        "required_evidence": ["An explicit state representation is required."]})
    view = phase4_step5_view(payload)
    markdown = phase4_step5_renderers()[1](view)
    body = markdown.split("## Derived metrics\n", 1)[1].split("\n## ", 1)[0]
    assert "Unavailable" in body
    value_rows = [line for line in body.splitlines()
                  if line.startswith('| `["value"]` |')]
    assert len(value_rows) == 1
    assert "Unavailable" in value_rows[0]
    assert "Value: Unavailable" in body
    assert "NaN" not in body
    assert "R_REPRESENTATION_NOT_DECLARED" in body
    strings = phase4_step5_markdown_data_strings(body)
    safe_metric = view.to_dict()["derived_metrics"]["diversity"]["by_version"]["v1"]["gini_simpson_diversity"]
    for reason in (safe_metric["coverage_reason"], safe_metric["denominator_reason"],
                   *safe_metric["required_evidence"]):
        assert reason in strings or reason in body
    assert safe_metric["value"] is None
    assert "value" in body and "denominator" in body and "coverage" in body


def test_phase4_step5_markdown_run_null_reasons_and_required_footer_are_preserved():
    from test_PR013_report_schema import phase4_step2_report_fixture, phase4_step5_renderers, phase4_step5_view

    view = phase4_step5_view(phase4_step2_report_fixture())
    markdown = phase4_step5_renderers()[1](view)
    strings = phase4_step5_markdown_data_strings(markdown)
    reason = view.to_dict()["run"]["null_reasons"]["random_seed"]
    assert reason in strings or reason in markdown
    assert "Unavailable" in markdown
    footer = markdown.split("## Errors\n", 1)[1]
    for value in ("0.1.0.dev2", "1.0", "observed_fact", "derived_metric", "proxy_signal",
                  "simulation", "unavailable_conclusion", "traceability"):
        assert value.lower() in footer.lower(), value
    assert "unavailable conclusions" in footer.lower()
    assert "false conclusions" in footer.lower()
    assert "round" in markdown.lower() or "precision" in markdown.lower()
    assert "JSON" in markdown


def test_phase4_step5_markdown_unicode_and_hostile_structural_ids_remain_inert_data():
    import json
    import re
    import unicodedata
    from test_PR013_report_schema import phase4_step5_renderers, phase4_step5_view

    render_json, render_markdown = phase4_step5_renderers()
    for label in ("中文状态 café 🚀", "left|right", "`` `escape` ```", "<script>alert(1)</script>",
                  "[claim](javascript:alert(1))", "![image](https://invalid.example/track)",
                  "\n## Forged report\n| field | claimed |", "\r\n# Forged title\t\x1b[31m",
                  "safe\u202eevil\u2066text\u2069\u2028line\u2029paragraph", "&lt;img src=x&gt;"):
        view = phase4_step5_view(phase4_step5_hostile_identity_payload(label))
        assert label in view.to_dict()["derived_metrics"]["diversity"]["by_version"]
        serialized = render_json(view)
        assert label in json.loads(serialized)["derived_metrics"]["diversity"]["by_version"]
        markdown = render_markdown(view)
        assert label in phase4_step5_markdown_data_strings(markdown), repr(label)
        assert "<script>" not in markdown and "<img" not in markdown
        outside_code = re.sub(r"`[^`\n]*`", "", markdown)
        assert "javascript:" not in outside_code
        assert "https://invalid.example/track" not in outside_code
        assert "[claim]" not in outside_code and "![image]" not in outside_code
        assert not re.search(r"^#{1,6} Forged", markdown, re.MULTILINE)
        assert not re.search(r"^```", markdown, re.MULTILINE)
        assert all(character == "\n" or unicodedata.category(character) not in (
            "Cc", "Cf", "Cs", "Zl", "Zp") for character in markdown)
        assert len([line for line in markdown.splitlines() if line.startswith("## ")]) == 12
        for line in markdown.splitlines():
            if line.startswith("|") and "left" in line and "right" in line:
                assert "left|right" not in line
        if label == "中文状态 café 🚀":
            assert label in markdown


def test_phase4_step5_redacted_reports_withhold_hostile_identity_but_keep_analysis():
    import json
    from test_PR013_report_schema import phase4_step5_renderers, phase4_step5_view

    label = "PRIVATE_RENDERER_ID|[claim](javascript:evil)中文"
    view = phase4_step5_view(phase4_step5_hostile_identity_payload(label), "redacted")
    render_json, render_markdown = phase4_step5_renderers()
    serialized, markdown = render_json(view), render_markdown(view)
    assert "PRIVATE_RENDERER_ID" not in serialized + markdown
    payload = json.loads(serialized)
    versions = payload["derived_metrics"]["diversity"]["by_version"]
    assert len(versions) == 1
    identity = next(iter(versions))
    assert identity.startswith("hmac-sha256:")
    assert identity in markdown
    assert versions[identity]["gini_simpson_diversity"]["value"] == 0
    assert "derived_metric" in markdown and "F-003" in markdown


def test_phase4_step5_all_supplied_analytical_string_values_are_visible_after_sanitization():
    from test_PR013_report_schema import phase4_step5_renderers, phase4_step5_rich_payload, phase4_step5_view

    def strings(value):
        if type(value) is str:
            yield value
        elif type(value) is dict:
            for child in value.values():
                yield from strings(child)
        elif type(value) is list:
            for child in value:
                yield from strings(child)

    for mode in ("standard", "redacted"):
        view = phase4_step5_view(phase4_step5_rich_payload(), mode)
        markdown = phase4_step5_renderers()[1](view)
        visible = phase4_step5_markdown_data_strings(markdown)
        for name in ("observed_facts", "derived_metrics", "simulations", "unavailable_conclusions"):
            for value in strings(view.to_dict()[name]):
                assert value in visible or value in markdown, (name, value)


def test_phase4_step5_error_and_warning_codes_remain_visible_without_raw_diagnostic_text():
    from test_PR013_report_schema import phase4_step2_error_report_fixture, phase4_step5_renderers, phase4_step5_view

    payload = phase4_step2_error_report_fixture()
    payload["errors"][0]["code"] = "E_FILE_PARSE"
    payload["errors"][0]["message"] = "PRIVATE_ERROR_BODY\n## Forged claim"
    payload["errors"][0]["remediation"] = ["PRIVATE_ERROR_REMEDIATION"]
    payload["warnings"] = [{"code": "W_PROVENANCE_MISSING_ROW",
        "message": "PRIVATE_ERROR_BODY", "count": 1,
        "affected_scope": {"dataset_versions": ["v1"], "record_count": 2,
            "excluded_record_count": 0, "denominator_basis": "included_records", "scope_id": "v1"},
        "representative_locations": [], "effect_on_capabilities": ["provenance"],
        "remediation": ["PRIVATE_ERROR_REMEDIATION"], "severity": "warning", "coverage": None}]
    view = phase4_step5_view(payload)
    for render in phase4_step5_renderers():
        output = render(view)
        assert "PRIVATE_ERROR_BODY" not in output
        assert "PRIVATE_ERROR_REMEDIATION" not in output
        assert "E_FILE_PARSE" in output
        assert "W_PROVENANCE_MISSING_ROW" in output
        assert "failed" in output


def test_phase4_step5_markdown_preserves_tiny_finite_values_and_signed_zero():
    from test_PR012_evidence_classes import phase4_step2_metric_report_fixture
    from test_PR013_report_schema import phase4_step5_renderers, phase4_step5_view

    for value, expected in ((5e-324, "5e-324"), (-0.0, "-0.0"), (0.0, "0.0")):
        payload = phase4_step2_metric_report_fixture()
        payload["derived_metrics"]["diversity"]["by_version"]["v1"][
            "gini_simpson_diversity"]["value"] = value
        markdown = phase4_step5_renderers()[1](phase4_step5_view(payload))
        assert expected in markdown


def test_phase4_step5_capability_known_coverage_keeps_explicit_null_reason_field():
    from test_PR013_report_schema import phase4_step5_renderers, phase4_step5_rich_payload, phase4_step5_view

    view = phase4_step5_view(phase4_step5_rich_payload())
    assert view.to_dict()["capabilities"]["ingestion"]["coverage"] == 1.0
    assert view.to_dict()["capabilities"]["ingestion"]["coverage_reason"] is None
    markdown = phase4_step5_renderers()[1](view)
    body = markdown.split("## Capability matrix\n", 1)[1].split("\n## ", 1)[0]
    assert body.count("coverage_reason") == 7
    assert "Unavailable" in body
    assert "null" in body


def test_phase4_step5_canonical_boundary_rejects_invalid_unicode_before_rendering():
    import pytest
    from test_PR013_report_schema import phase4_step5_view

    for label in ("has\x00nul", "unpaired\ud800surrogate"):
        with pytest.raises(ValueError):
            phase4_step5_view(phase4_step5_hostile_identity_payload(label))


def test_phase4_step5_proxy_signal_retains_bounded_claim_basis_and_metadata_requests(tmp_path):
    import json
    from recursive_integrity_toolkit.metrics.tail import select_tail
    from recursive_integrity_toolkit.models import TailSelectionOptions
    from recursive_integrity_toolkit.reports.assembly import assemble_report
    from test_PR013_report_schema import phase4_step5_renderers, phase4_step5_view

    bundle = phase4_step3_bundle(tmp_path)
    distribution = phase4_step3_distribution(bundle)
    tail = select_tail(distribution.unweighted, options=TailSelectionOptions("singleton_count"))
    report = assemble_report(bundle, run=phase4_step3_run(), distributions=(distribution,), tail=tail)
    render_json, render_markdown = phase4_step5_renderers()
    for mode in ("standard", "redacted"):
        view = phase4_step5_view(report.to_dict(), mode)
        actual = json.loads(render_json(view))
        signal = actual["proxy_signals"]["tail_fragility"]
        assert signal["evidence_class"] == "proxy_signal"
        assert signal["level"] == "present"
        assert actual["derived_metrics"]["tail"]["tail_support_size"]["value"] == 2
        assert "This signal is not a calibrated forecast of the production pipeline." in signal["limitations"]
        markdown = render_markdown(view)
        body = markdown.split("## Proxy signals\n", 1)[1].split("\n## ", 1)[0]
        assert "proxy_signal" in body and "present" in body
        assert "basis_fields" in body and "trigger_rule" in body
        assert "not a calibrated forecast" in body
        assert actual["recommended_next_metadata"]
        recommendations = markdown.split("## Recommended next metadata\n", 1)[1].split("\n## ", 1)[0]
        assert recommendations.lstrip().startswith("- ")
        assert "scope" in recommendations and "expected_unlock" in recommendations
