"""Phase 1 placeholder for PR-013.

Planned scope:
    Future report-rendering tests are deferred to Phase 4.

Current Phase 1 scope:
    Verify the approved owner ID and confirm that the target module remains a
    docstring-only, import-safe placeholder.

Limits:
    No mathematical metric, data loading, graph operation, or report result is tested.
"""


def phase4_step2_report_fixture():
    """Hand-authored empty report from reporting sections 8, 10 and 31.

    No production factory or schema defaults supply expected values.
    """
    return {
        "run": {
            "run_id": "independent-empty-case",
            "toolkit_version": "0.1.0.dev2",
            "report_schema_version": "1.1",
            "started_at": "2026-09-19T00:00:00+00:00",
            "completed_at": "2026-09-19T00:00:00.500000+00:00",
            "duration_seconds": 0.5,
            "python_version": "3.12.14",
            "platform": "independent-test-platform",
            "command": "rit validate",
            "config_hash": "0123456789abcdef" * 4,
            "random_seed": None,
            "strict_mode": False,
            "redacted_mode": False,
            "network_call_count": 0,
            "deterministic": True,
            "privacy_mode": "standard",
            "run_status": "complete",
            "null_reasons": {"random_seed": "No stochastic scenario was requested."},
        },
        "inputs": {},
        "observability": {},
        "capabilities": {},
        "observed_facts": {},
        "derived_metrics": {},
        "proxy_signals": {},
        "simulations": {},
        "unavailable_conclusions": [],
        "recommended_next_metadata": [],
        "warnings": [],
        "errors": [],
    }


def phase4_step2_schema_validator(schema_root):
    """Resolve only local definitions; a network lookup is a test failure."""
    import json

    from jsonschema import Draft202012Validator
    from referencing import Registry

    def refuse_remote(uri):
        raise AssertionError(f"A local report schema attempted remote retrieval: {uri}")

    schema = json.loads((schema_root / "report.schema.json").read_text(encoding="utf-8"))
    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, registry=Registry(retrieve=refuse_remote))


def test_phase4_step2_empty_report_retains_all_twelve_sections(schema_root):
    from recursive_integrity_toolkit.result import CanonicalReport, validate_report

    payload = phase4_step2_report_fixture()
    phase4_step2_schema_validator(schema_root).validate(payload)
    validate_report(payload)
    exported = CanonicalReport.from_dict(payload).to_dict()
    assert exported == payload
    assert tuple(exported) == (
        "run", "inputs", "observability", "capabilities", "observed_facts",
        "derived_metrics", "proxy_signals", "simulations", "unavailable_conclusions",
        "recommended_next_metadata", "warnings", "errors",
    )
    assert all(exported[name] == {} for name in (
        "inputs", "observability", "capabilities", "observed_facts",
        "derived_metrics", "proxy_signals", "simulations",
    ))
    assert all(exported[name] == [] for name in (
        "unavailable_conclusions", "recommended_next_metadata", "warnings", "errors",
    ))


def test_phase4_step2_missing_top_level_sections_fail_both_contracts(schema_root):
    import pytest

    from recursive_integrity_toolkit.result import CanonicalReport

    validator = phase4_step2_schema_validator(schema_root)
    for name in phase4_step2_report_fixture():
        payload = phase4_step2_report_fixture()
        del payload[name]
        assert not validator.is_valid(payload), name
        with pytest.raises(ValueError):
            CanonicalReport.from_dict(payload)


def test_phase4_step2_section_types_are_not_interchangeable(schema_root):
    import pytest

    from recursive_integrity_toolkit.result import CanonicalReport

    validator = phase4_step2_schema_validator(schema_root)
    for name in phase4_step2_report_fixture():
        for wrong in (None, 0, "", [] if name not in (
            "unavailable_conclusions", "recommended_next_metadata", "warnings", "errors",
        ) else {}):
            payload = phase4_step2_report_fixture()
            payload[name] = wrong
            assert not validator.is_valid(payload), (name, wrong)
            with pytest.raises(ValueError):
                CanonicalReport.from_dict(payload)


def test_phase4_step2_required_run_metadata_cannot_disappear(schema_root):
    import pytest

    from recursive_integrity_toolkit.result import CanonicalReport

    validator = phase4_step2_schema_validator(schema_root)
    for name in phase4_step2_report_fixture()["run"]:
        payload = phase4_step2_report_fixture()
        del payload["run"][name]
        assert not validator.is_valid(payload), name
        with pytest.raises(ValueError):
            CanonicalReport.from_dict(payload)


def test_phase4_step2_unknown_public_keys_are_rejected(schema_root):
    import pytest

    from recursive_integrity_toolkit.result import CanonicalReport

    validator = phase4_step2_schema_validator(schema_root)
    for section in (None, "run", "inputs", "observability", "capabilities", "observed_facts",
                    "derived_metrics", "proxy_signals", "simulations"):
        payload = phase4_step2_report_fixture()
        target = payload if section is None else payload[section]
        target["unregistered_private_result"] = 0
        assert not validator.is_valid(payload), section
        with pytest.raises(ValueError):
            CanonicalReport.from_dict(payload)


def test_phase4_step2_numeric_run_fields_reject_boolean_values(schema_root):
    import pytest

    from recursive_integrity_toolkit.result import CanonicalReport

    validator = phase4_step2_schema_validator(schema_root)
    for field in ("duration_seconds", "network_call_count", "random_seed"):
        for value in (True, False):
            payload = phase4_step2_report_fixture()
            payload["run"][field] = value
            if field == "random_seed":
                payload["run"]["null_reasons"] = {}
            assert not validator.is_valid(payload), (field, value)
            with pytest.raises(ValueError):
                CanonicalReport.from_dict(payload)


def test_phase4_step2_boolean_run_fields_reject_numeric_values(schema_root):
    import pytest

    from recursive_integrity_toolkit.result import CanonicalReport

    validator = phase4_step2_schema_validator(schema_root)
    for field in ("strict_mode", "redacted_mode", "deterministic"):
        for value in (0, 1, "false", None):
            payload = phase4_step2_report_fixture()
            payload["run"][field] = value
            assert not validator.is_valid(payload), (field, value)
            with pytest.raises(ValueError):
                CanonicalReport.from_dict(payload)


def test_phase4_step2_nonfinite_run_numbers_are_rejected(schema_root):
    import json
    import pytest

    from recursive_integrity_toolkit.result import CanonicalReport

    validator = phase4_step2_schema_validator(schema_root)
    for field in ("duration_seconds", "network_call_count", "random_seed"):
        for value in (float("nan"), float("inf"), float("-inf")):
            payload = phase4_step2_report_fixture()
            payload["run"][field] = value
            if field == "random_seed":
                payload["run"]["null_reasons"] = {}
            assert not validator.is_valid(payload), (field, value)
            with pytest.raises(ValueError):
                json.dumps(payload, allow_nan=False)
            with pytest.raises(ValueError):
                CanonicalReport.from_dict(payload)


def test_phase4_step2_run_status_and_schema_version_are_exact(schema_root):
    import pytest

    from recursive_integrity_toolkit.result import CanonicalReport

    validator = phase4_step2_schema_validator(schema_root)
    for field, value in (
        ("report_schema_version", "1"), ("report_schema_version", 1.0),
        ("report_schema_version", "2.0"), ("run_status", "success"),
        ("run_status", "available"), ("privacy_mode", "anonymous"),
    ):
        payload = phase4_step2_report_fixture()
        payload["run"][field] = value
        assert not validator.is_valid(payload), (field, value)
        with pytest.raises(ValueError):
            CanonicalReport.from_dict(payload)


def test_phase4_step2_null_run_metadata_requires_honest_reasons():
    import pytest

    from recursive_integrity_toolkit.result import CanonicalReport

    for field in ("started_at", "completed_at", "duration_seconds", "python_version",
                  "platform", "command", "config_hash", "random_seed"):
        payload = phase4_step2_report_fixture()
        payload["run"][field] = None
        payload["run"]["null_reasons"][field] = "Unavailable before input initialization."
        assert CanonicalReport.from_dict(payload).to_dict()["run"][field] is None
        del payload["run"]["null_reasons"][field]
        with pytest.raises(ValueError):
            CanonicalReport.from_dict(payload)


def test_phase4_step2_mutable_inputs_and_exports_do_not_alias():
    from recursive_integrity_toolkit.result import CanonicalReport

    payload = phase4_step2_report_fixture()
    report = CanonicalReport.from_dict(payload)
    payload["run"]["null_reasons"]["random_seed"] = "source mutated"
    payload["unavailable_conclusions"].append({"injected": True})
    first = report.to_dict()
    assert first["run"]["null_reasons"]["random_seed"] == "No stochastic scenario was requested."
    assert first["unavailable_conclusions"] == []
    first["run"]["null_reasons"]["random_seed"] = "export mutated"
    first["unavailable_conclusions"].append({"injected": True})
    assert report.to_dict() == phase4_step2_report_fixture()


def test_phase4_step2_public_canonical_sections_are_deeply_read_only():
    import pytest

    from recursive_integrity_toolkit.result import CanonicalReport

    report = CanonicalReport.from_dict(phase4_step2_report_fixture())
    with pytest.raises(TypeError):
        report.sections["run"] = {}
    with pytest.raises(TypeError):
        report.sections["run"]["null_reasons"]["random_seed"] = "injected"
    with pytest.raises((AttributeError, TypeError)):
        report.sections["warnings"].append({"injected": True})
    with pytest.raises((AttributeError, TypeError)):
        report.sections = {}
    assert report.to_dict() == phase4_step2_report_fixture()


def phase4_step2_capability_report_fixture():
    """Input eligibility and executed work are intentionally different here."""
    import copy

    payload = phase4_step2_report_fixture()
    capabilities = {}
    for key in ("ingestion", "content_diagnostics", "provenance", "lineage",
                "dataset_longitudinal", "model_longitudinal", "intervention_simulation"):
        unavailable = key in ("model_longitudinal", "intervention_simulation")
        capabilities[key] = {
            "status": "unavailable" if unavailable else "available",
            "reason_codes": ["R_MODEL_EVIDENCE_MISSING" if key == "model_longitudinal"
                             else "R_SCENARIO_NOT_CONFIGURED"] if unavailable else [],
            "coverage": None if unavailable else 1.0,
            "coverage_reason": "No eligible evidence was supplied." if unavailable else None,
            "requirements_met": [] if unavailable else ["Declared input requirements are met."],
            "requirements_missing": ["Required evidence was not supplied."] if unavailable else [],
            "notes": ["Input eligibility does not assert that analysis was executed."],
            "execution_status": "completed" if key == "ingestion" else (
                "deferred" if key == "model_longitudinal" else "not_requested"
            ),
            "execution_scope": ["input_validation"] if key == "ingestion" else [],
            "execution_reason_codes": [] if key == "ingestion" else [
                "IMPLEMENTATION_DEFERRED" if key == "model_longitudinal" else "NOT_REQUESTED"
            ],
        }
    payload["capabilities"] = capabilities
    payload["observability"] = {
        "maximum_level": 4, "level_label": "longitudinal_dataset_observability",
        "basis": ["Explicit dataset chronology and representation eligibility were supplied."],
        "limitations": ["This is input eligibility; lineage analysis was not requested."],
        "partial_evidence": [], "capabilities": copy.deepcopy(capabilities),
    }
    return payload


def test_phase4_step2_capability_mirror_preserves_input_and_execution_status(schema_root):
    from recursive_integrity_toolkit.result import CanonicalReport

    payload = phase4_step2_capability_report_fixture()
    phase4_step2_schema_validator(schema_root).validate(payload)
    report = CanonicalReport.from_dict(payload)
    exported = report.to_dict()
    assert exported["capabilities"] == exported["observability"]["capabilities"]
    assert exported["observability"]["maximum_level"] == 4
    assert exported["capabilities"]["lineage"]["status"] == "available"
    assert exported["capabilities"]["lineage"]["execution_status"] == "not_requested"
    assert report.sections["capabilities"] is report.sections["observability"]["capabilities"]


def test_phase4_step2_disagreeing_capability_mirrors_fail_semantic_validation():
    import pytest

    from recursive_integrity_toolkit.result import CanonicalReport, validate_report

    for field, value in (("status", "partial"), ("coverage", 0.5),
                         ("execution_status", "failed"), ("notes", ["Changed mirror."])):
        payload = phase4_step2_capability_report_fixture()
        payload["observability"]["capabilities"]["lineage"][field] = value
        with pytest.raises(ValueError):
            validate_report(payload)
        with pytest.raises(ValueError):
            CanonicalReport.from_dict(payload)


def test_phase4_step2_nonempty_capability_matrix_has_exactly_seven_keys(schema_root):
    import copy
    import pytest

    from recursive_integrity_toolkit.result import CanonicalReport

    validator = phase4_step2_schema_validator(schema_root)
    for missing in phase4_step2_capability_report_fixture()["capabilities"]:
        payload = phase4_step2_capability_report_fixture()
        del payload["capabilities"][missing]
        payload["observability"]["capabilities"] = copy.deepcopy(payload["capabilities"])
        assert not validator.is_valid(payload), missing
        with pytest.raises(ValueError):
            CanonicalReport.from_dict(payload)
    payload = phase4_step2_capability_report_fixture()
    payload["capabilities"]["universal_integrity"] = copy.deepcopy(payload["capabilities"]["ingestion"])
    payload["observability"]["capabilities"] = copy.deepcopy(payload["capabilities"])
    assert not validator.is_valid(payload)
    with pytest.raises(ValueError):
        CanonicalReport.from_dict(payload)


def test_phase4_step2_capability_status_names_are_exact(schema_root):
    import copy
    import pytest

    from recursive_integrity_toolkit.result import CanonicalReport

    validator = phase4_step2_schema_validator(schema_root)
    for field, value in (("status", "completed"), ("status", "deferred"),
                         ("execution_status", "available"), ("execution_status", "unavailable"),
                         ("execution_status", "experimental"), ("coverage", True)):
        payload = phase4_step2_capability_report_fixture()
        payload["capabilities"]["lineage"][field] = value
        payload["observability"]["capabilities"] = copy.deepcopy(payload["capabilities"])
        assert not validator.is_valid(payload), (field, value)
        with pytest.raises(ValueError):
            CanonicalReport.from_dict(payload)


def test_phase4_step2_capability_execution_reasons_are_not_optional():
    import copy
    import pytest

    from recursive_integrity_toolkit.result import CanonicalReport

    for status in ("partial", "not_requested", "deferred", "failed"):
        payload = phase4_step2_capability_report_fixture()
        payload["capabilities"]["lineage"]["execution_status"] = status
        payload["capabilities"]["lineage"]["execution_reason_codes"] = []
        payload["observability"]["capabilities"] = copy.deepcopy(payload["capabilities"])
        with pytest.raises(ValueError):
            CanonicalReport.from_dict(payload)


def test_phase4_step2_observability_level_is_a_bounded_integer(schema_root):
    import pytest

    from recursive_integrity_toolkit.result import CanonicalReport

    validator = phase4_step2_schema_validator(schema_root)
    for value in (True, False, -1, 6, 1.5, "4"):
        payload = phase4_step2_capability_report_fixture()
        payload["observability"]["maximum_level"] = value
        assert not validator.is_valid(payload), value
        with pytest.raises(ValueError):
            CanonicalReport.from_dict(payload)


def test_phase4_step2_runtime_contract_uses_no_analytical_or_schema_dependency(subprocess_env):
    import json
    import subprocess
    import sys

    script = '''
import builtins
import json
import sys

original_import = builtins.__import__

def restricted_import(name, *args, **kwargs):
    if name.split('.')[0] in {'numpy', 'pandas', 'pyarrow', 'jsonschema'}:
        raise AssertionError('Runtime contract imported an optional analytical/test dependency: ' + name)
    if 'recursive_integrity_toolkit.metrics' in name or 'recursive_integrity_toolkit.io' in name:
        raise AssertionError('Runtime contract imported an input or calculation owner: ' + name)
    return original_import(name, *args, **kwargs)

builtins.__import__ = restricted_import
from recursive_integrity_toolkit.result import CanonicalReport, validate_report
payload = json.loads(sys.argv[1])
validate_report(payload)
assert CanonicalReport.from_dict(payload).to_dict() == payload
assert not any(name.startswith(('recursive_integrity_toolkit.metrics.',
                                'recursive_integrity_toolkit.io.')) for name in sys.modules)
'''
    result = subprocess.run(
        [sys.executable, "-c", script, json.dumps(phase4_step2_report_fixture(), allow_nan=False)],
        env=subprocess_env, capture_output=True, text=True, check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def phase4_step2_error_report_fixture():
    payload = phase4_step2_report_fixture()
    payload["run"]["run_status"] = "failed"
    payload["errors"] = [{
        "code": "INPUT_PARSE_FAILED", "severity": "fatal",
        "message": "The records artifact could not be parsed.",
        "file_role": "records", "field": None, "record_key": None, "row_number": None,
        "effect_on_run": "failed", "effect_on_capabilities": ["ingestion"],
        "remediation": ["Supply a records artifact in one of the supported local formats."],
    }]
    return payload


def test_phase4_step2_error_only_report_is_schema_conforming(schema_root):
    from recursive_integrity_toolkit.result import CanonicalReport

    payload = phase4_step2_error_report_fixture()
    phase4_step2_schema_validator(schema_root).validate(payload)
    exported = CanonicalReport.from_dict(payload).to_dict()
    assert exported == payload
    assert exported["run"]["run_status"] == "failed"
    assert exported["errors"][0]["code"] == "INPUT_PARSE_FAILED"
    for section in ("observed_facts", "derived_metrics", "proxy_signals", "simulations"):
        assert exported[section] == {}


def test_phase4_step2_error_details_are_typed_and_do_not_accept_unknown_keys(schema_root):
    import pytest

    from recursive_integrity_toolkit.result import CanonicalReport

    validator = phase4_step2_schema_validator(schema_root)
    for field, value in (("severity", "warning"), ("row_number", True), ("row_number", -1),
                         ("row_number", 1.5), ("effect_on_run", "success"),
                         ("record_key", "unscoped-id"), ("raw_content", "private input text")):
        payload = phase4_step2_error_report_fixture()
        payload["errors"][0][field] = value
        assert not validator.is_valid(payload), (field, value)
        with pytest.raises(ValueError):
            CanonicalReport.from_dict(payload)
    for field in phase4_step2_error_report_fixture()["errors"][0]:
        payload = phase4_step2_error_report_fixture()
        del payload["errors"][0][field]
        assert not validator.is_valid(payload), field
        with pytest.raises(ValueError):
            CanonicalReport.from_dict(payload)


def test_phase4_step2_null_reason_keys_cannot_explain_a_nonnull_or_unknown_field():
    import pytest

    from recursive_integrity_toolkit.result import CanonicalReport

    for field in ("duration_seconds", "unregistered_run_field"):
        payload = phase4_step2_report_fixture()
        payload["run"]["null_reasons"][field] = "This value was not available."
        with pytest.raises(ValueError):
            CanonicalReport.from_dict(payload)


def test_phase4_step2_canonical_section_order_is_independent_of_input_insertion_order():
    from recursive_integrity_toolkit.result import CanonicalReport

    expected = phase4_step2_report_fixture()
    reversed_input = dict(reversed(list(expected.items())))
    actual = CanonicalReport.from_dict(reversed_input).to_dict()
    assert tuple(actual) == tuple(expected)
    assert actual == expected


def test_phase4_step2_sha256_metadata_rejects_trailing_line_breaks(schema_root):
    import pytest

    from recursive_integrity_toolkit.result import CanonicalReport

    validator = phase4_step2_schema_validator(schema_root)
    for value in ("a" * 64 + "\n", "a" * 64 + "\r\n", " " + "a" * 64):
        payload = phase4_step2_report_fixture()
        payload["run"]["config_hash"] = value
        assert not validator.is_valid(payload), repr(value)
        with pytest.raises(ValueError):
            CanonicalReport.from_dict(payload)


# Phase 4 Step 5: authored renderer contracts, without expected-output goldens.
def phase4_step5_rich_payload():
    """Combine independent, already reviewed literal evidence contracts."""
    import copy
    from test_PR012_evidence_classes import (
        phase4_step2_additional_evidence_fixture, phase4_step2_interval_report_fixture,
        phase4_step2_metric_fixture, phase4_step2_sampled_path_report_fixture,
    )

    payload = phase4_step2_capability_report_fixture()
    payload["run"]["run_status"] = "partial"
    payload["capabilities"]["lineage"].update({"status": "partial", "coverage": 0.75,
        "reason_codes": ["R_LINEAGE_PARTIAL"]})
    payload["observability"]["capabilities"] = copy.deepcopy(payload["capabilities"])
    payload["observed_facts"] = {"content": {
        "duplicate_record_count": phase4_step2_metric_fixture(observed=True)}}
    metric = phase4_step2_metric_fixture()
    metric["value"] = 0.12345678901234566
    payload["derived_metrics"] = phase4_step2_interval_report_fixture()["derived_metrics"]
    payload["derived_metrics"]["diversity"] = {"by_version": {"v1": {
        "gini_simpson_diversity": metric}}}
    payload["simulations"] = phase4_step2_sampled_path_report_fixture()["simulations"]
    payload["unavailable_conclusions"] = [
        phase4_step2_additional_evidence_fixture("unavailable_conclusion")]
    return payload


def phase4_step5_view(payload, mode="standard", record_id_mode=None):
    from recursive_integrity_toolkit.reports.assembly import privacy_view
    from recursive_integrity_toolkit.result import CanonicalReport
    from recursive_integrity_toolkit.utils.hashing import IdentifierProtection

    return privacy_view(CanonicalReport.from_dict(payload), mode=mode,
        record_id_mode=record_id_mode,
        protection=IdentifierProtection.create(secret=b"renderer-contract-only-key-32byte"))


def phase4_step5_renderers():
    from recursive_integrity_toolkit.reports.json_report import render_json
    from recursive_integrity_toolkit.reports.markdown_report import render_markdown

    return render_json, render_markdown


def test_phase4_step5_json_round_trip_validates_local_schema_and_all_values(schema_root):
    import json
    from recursive_integrity_toolkit.result import validate_report

    validator = phase4_step2_schema_validator(schema_root)
    render_json, _ = phase4_step5_renderers()
    for payload in (phase4_step2_report_fixture(), phase4_step2_error_report_fixture(),
                    phase4_step5_rich_payload()):
        for mode in ("standard", "redacted"):
            view = phase4_step5_view(payload, mode)
            expected = view.to_dict()
            result = render_json(view)
            assert type(result) is str
            actual = json.loads(result)
            validator.validate(actual)
            validate_report(actual)
            assert actual == expected
            assert tuple(actual) == ("run", "inputs", "observability", "capabilities",
                "observed_facts", "derived_metrics", "proxy_signals", "simulations",
                "unavailable_conclusions", "recommended_next_metadata", "warnings", "errors")
            assert actual["observability"].get("capabilities", {}) == actual["capabilities"]
            assert view.to_dict() == expected


def test_phase4_step5_json_does_not_round_intervals_or_precise_scalar_values():
    import json

    render_json, _ = phase4_step5_renderers()
    actual = json.loads(render_json(phase4_step5_view(phase4_step5_rich_payload())))
    assert actual["derived_metrics"]["diversity"]["by_version"]["v1"][
        "gini_simpson_diversity"]["value"] == 0.12345678901234566
    interval = actual["derived_metrics"]["closure_exposure"]["direct"]
    assert interval["lower_bound"]["value"] == 0.25
    assert interval["upper_bound"]["value"] == 0.75
    assert interval["interval_width"]["value"] == 0.5
    assert "midpoint" not in interval
    assert actual["observed_facts"]["content"]["duplicate_record_count"]["value"] == 0
    assert actual["simulations"]["closed_resampling"]["status"] == "experimental"
    assert actual["capabilities"]["lineage"]["execution_status"] == "not_requested"


def test_phase4_step5_renderers_require_explicit_safe_view_without_adapting_inputs():
    import pytest
    from recursive_integrity_toolkit.result import CanonicalReport

    class CannotInspect:
        def to_dict(self):
            raise AssertionError("Raw input must not be introspected")

        def __str__(self):
            raise AssertionError("Raw input must not be formatted")

    payload = phase4_step5_rich_payload()
    for render in phase4_step5_renderers():
        for value in (None, False, payload, CanonicalReport.from_dict(payload),
                      "PRIVATE_INPUT_SENTINEL", CannotInspect()):
            with pytest.raises(TypeError) as error:
                render(value)
            assert "PRIVATE_INPUT_SENTINEL" not in str(error.value)


def test_phase4_step5_renderers_revalidate_and_reject_nonfinite_or_broken_contract():
    import copy
    import pytest
    from recursive_integrity_toolkit.result import CanonicalReport, SafeReportView

    original = phase4_step5_view(phase4_step5_rich_payload()).to_dict()
    for case in ("nan", "infinity", "missing_section", "wrong_mirror"):
        payload = copy.deepcopy(original)
        if case in ("nan", "infinity"):
            payload["run"]["duration_seconds"] = float("nan" if case == "nan" else "inf")
        elif case == "missing_section":
            del payload["warnings"]
        else:
            payload["observability"]["capabilities"]["lineage"]["coverage"] = 0.5
        broken = object.__new__(CanonicalReport)
        object.__setattr__(broken, "sections", payload)
        view = object.__new__(SafeReportView)
        object.__setattr__(view, "_report", broken)
        for render in phase4_step5_renderers():
            with pytest.raises(ValueError):
                render(view)


def test_phase4_step5_renderers_perform_no_file_network_input_or_metric_operations(monkeypatch):
    import builtins
    import os
    import socket
    from pathlib import Path
    from recursive_integrity_toolkit import config
    from recursive_integrity_toolkit.io import validation
    from recursive_integrity_toolkit.metrics import diversity, provenance, resampling

    view = phase4_step5_view(phase4_step5_rich_payload())
    before = view.to_dict()
    renderers = phase4_step5_renderers()

    def forbidden(*args, **kwargs):
        raise AssertionError("Renderer crossed its pure supplied-data boundary")

    with monkeypatch.context() as patch:
        for owner, name in ((builtins, "open"), (os, "open"), (Path, "open"),
                            (socket, "socket"), (socket, "getaddrinfo"),
                            (config, "load_config"), (validation, "validate_bundle"),
                            (diversity, "calculate_state_distribution"),
                            (provenance, "summarize_provenance"),
                            (resampling, "simulate_closed_resampling")):
            patch.setattr(owner, name, forbidden)
        for render in renderers:
            assert type(render(view)) is str
    assert view.to_dict() == before


def test_phase4_step5_renderer_imports_do_not_load_analytical_or_input_owners(subprocess_env):
    import subprocess
    import sys

    script = '''
import builtins
import sys
original_import = builtins.__import__
def restricted_import(name, *args, **kwargs):
    if name.split('.')[0] in {'numpy', 'pandas', 'pyarrow', 'jsonschema'}:
        raise AssertionError('Renderer imported an analytical/test dependency: ' + name)
    if 'recursive_integrity_toolkit.metrics' in name or 'recursive_integrity_toolkit.io' in name:
        raise AssertionError('Renderer imported an input or calculation owner: ' + name)
    return original_import(name, *args, **kwargs)
builtins.__import__ = restricted_import
from recursive_integrity_toolkit.reports.json_report import render_json
from recursive_integrity_toolkit.reports.markdown_report import render_markdown
assert callable(render_json) and callable(render_markdown)
assert not any(name.startswith(('recursive_integrity_toolkit.metrics.',
    'recursive_integrity_toolkit.io.')) for name in sys.modules)
'''
    result = subprocess.run([sys.executable, "-c", script], env=subprocess_env,
        capture_output=True, text=True, check=False)
    assert result.returncode == 0, result.stdout + result.stderr


def test_phase4_step5_json_preserves_smallest_float_large_finite_count_and_negative_zero():
    import json
    import math
    from test_PR012_evidence_classes import phase4_step2_metric_report_fixture

    render_json, _ = phase4_step5_renderers()
    for value in (5e-324, -0.0, 0.9999999999999999):
        payload = phase4_step2_metric_report_fixture()
        payload["derived_metrics"]["diversity"]["by_version"]["v1"][
            "gini_simpson_diversity"]["value"] = value
        actual = json.loads(render_json(phase4_step5_view(payload)))["derived_metrics"][
            "diversity"]["by_version"]["v1"]["gini_simpson_diversity"]["value"]
        assert actual == value
        assert math.copysign(1, actual) == math.copysign(1, value)
    payload = phase4_step2_metric_report_fixture(observed=True)
    payload["observed_facts"]["content"]["duplicate_record_count"]["value"] = 9007199254740993
    actual = json.loads(render_json(phase4_step5_view(payload)))
    assert actual["observed_facts"]["content"]["duplicate_record_count"]["value"] == 9007199254740993
