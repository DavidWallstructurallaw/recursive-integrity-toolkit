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
