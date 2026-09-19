"""PR-008/009/017 Phase 2 Step 9 partial-family validation, never a report."""
import json
import pytest
from recursive_integrity_toolkit.errors import ErrorCode, WarningCode
from recursive_integrity_toolkit.io.validation import validate_bundle
from recursive_integrity_toolkit.models import (
    AuditBundle, CapabilityKey, CapabilityStatus, ContentMode, FileRole, InputSource,
    NormalizationOptions, RecordKey, ValidationSeverity,
)


def _put(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(''.join(json.dumps(row) + '\n' for row in rows), encoding='utf-8')
    return path


def _bundle(root, parents):
    records = [{'dataset_version': 'v1', 'record_id': 'p', 'content': 'text', 'topic': 'cat'},
               {'dataset_version': 'v2', 'record_id': 'c', 'content': 'text', 'topic': 'dog'}]
    provenance = [{'dataset_version': 'v1', 'record_id': 'p', 'source_type': 'human',
                   'provenance_confidence': 'confirmed', 'external_grounding': 'yes', 'parent_ids': []},
                  {'dataset_version': 'v2', 'record_id': 'c', 'source_type': 'synthetic',
                   'provenance_confidence': 'confirmed', 'external_grounding': 'no', 'parent_ids': parents}]
    return AuditBundle((InputSource(FileRole.RECORDS_PRIMARY, _put(root/'records.jsonl', records)),
                        InputSource(FileRole.PROVENANCE_MANIFEST, _put(root/'prov.jsonl', provenance))))


def _config():
    return {'version_order': ['v1', 'v2'], 'representation': {'name': 'topic', 'source': 'topic_field',
            'field': 'topic', 'version': 'test-v1', 'missing_value_policy': 'error'}}


def test_phase2_step9_unresolved_parent_preserves_level_four(tmp_path):
    result = validate_bundle(_bundle(tmp_path, ['v1::absent']), configuration=_config())
    assert result.observability.maximum_level == 4
    assert result.observability.capabilities[CapabilityKey.LINEAGE].status is CapabilityStatus.UNAVAILABLE
    assert any(m.code == WarningCode.PARENT_UNRESOLVED.value for m in result.validation_messages)
    assert result.generation is not None


@pytest.mark.parametrize('parents', [['v2::c'], ['bad::format::x']])
def test_phase2_step9_invalid_parent_preserves_independent_dataset_evidence(tmp_path, parents):
    result = validate_bundle(_bundle(tmp_path, parents), configuration=_config())
    assert result.has_errors and result.generation is None
    assert result.observability.maximum_level == 4
    assert result.observability.capabilities[CapabilityKey.LINEAGE].status is CapabilityStatus.UNAVAILABLE
    assert any(m.code in (ErrorCode.LINEAGE_CYCLE.value, ErrorCode.PARENT_FORMAT.value)
               and m.severity is ValidationSeverity.ERROR for m in result.validation_messages)


def test_phase2_step9_valid_generation_pipeline(tmp_path):
    result = validate_bundle(_bundle(tmp_path, ['v1::p']), configuration=_config())
    assert not result.has_errors
    assert [r.expected_generation for r in result.generation.assessments] == [0, 1]
    assert result.observability.maximum_level == 4


def test_phase2_step9_content_reads_use_each_records_directory(tmp_path):
    sources = []
    for folder, version, role in [('one', 'v1', FileRole.RECORDS_PRIMARY), ('two', 'v2', FileRole.RECORDS_COMPARE)]:
        path = _put(tmp_path/folder/'records.jsonl', [{'dataset_version': version, 'record_id': 'a', 'content': 'text.txt'}])
        (path.parent/'text.txt').write_text('different synthetic text '+folder, encoding='utf-8')
        sources.append(InputSource(role, path))
    result = validate_bundle(AuditBundle(tuple(sources)), resolve_local_content=True,
                             normalization_options=NormalizationOptions(content_mode=ContentMode.LOCAL_REF))
    assert result.content_read_keys == (RecordKey('v1', 'a'), RecordKey('v2', 'a'))
    assert result.observability.maximum_level == 1 and 'different synthetic text' not in repr(result)


@pytest.mark.parametrize('reference', ['missing.txt', '../escape.txt', 'https://invalid.example/a'])
def test_phase2_step9_content_failure_retains_metadata_and_error(tmp_path, reference):
    path = _put(tmp_path/'records.jsonl', [{'dataset_version':'v1','record_id':'a','content':reference}])
    result = validate_bundle(AuditBundle((InputSource(FileRole.RECORDS_PRIMARY, path),)), resolve_local_content=True,
        normalization_options=NormalizationOptions(content_mode=ContentMode.LOCAL_REF))
    assert result.has_errors and result.observability.maximum_level == 0
    assert result.observability.capabilities[CapabilityKey.INGESTION].status is CapabilityStatus.AVAILABLE
    assert result.records[0].values['content'] == reference and not result.content_read_keys
    assert any(m.code == WarningCode.CONTENT_ANALYSIS_UNAVAILABLE.value for m in result.validation_messages)
    assert all(m.file_path in (None, '[redacted]') for m in result.validation_messages)
    assert all(reference not in m.message for m in result.validation_messages)


def test_phase2_step9_content_limits_and_invalid_utf8(tmp_path):
    path = _put(tmp_path/'records.jsonl', [{'dataset_version':'v1','record_id':'a','content':'text.txt'}])
    target = tmp_path/'text.txt'
    for content, limits, expected in [(b'abcde', {'max_content_bytes': 4}, ErrorCode.FILE_PARSE), (b'\xff', {}, ErrorCode.FILE_ENCODING)]:
        target.write_bytes(content)
        result = validate_bundle(AuditBundle((InputSource(FileRole.RECORDS_PRIMARY,path),)), resolve_local_content=True,
            normalization_options=NormalizationOptions(content_mode=ContentMode.LOCAL_REF), configuration={'resource_limits':limits})
        assert result.has_errors
        assert any(m.code == expected.value and m.row_number == 1 for m in result.validation_messages)


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


def test_phase4_step3_level_four_keeps_lineage_input_available_and_execution_deferred(tmp_path, repo_root):
    from recursive_integrity_toolkit.reports.assembly import assemble_report

    bundle = validate_bundle(_bundle(tmp_path, ["v1::p"]), configuration=_config())
    report = phase4_step3_schema(assemble_report(bundle, run=phase4_step3_run()), repo_root)
    assert report["observability"]["maximum_level"] == 4
    lineage = report["capabilities"]["lineage"]
    assert lineage["status"] == "available" and lineage["execution_status"] == "deferred"
    assert lineage["execution_reason_codes"]
    assert report["capabilities"]["dataset_longitudinal"]["status"] == "available"
    assert report["capabilities"]["dataset_longitudinal"]["execution_status"] == "not_requested"
    assert report["run"]["run_status"] == "complete"
    assert report["simulations"] == {}


def test_phase4_step3_ordering_validation_never_becomes_graph_cycle_or_ancestry_result(tmp_path, repo_root):
    from recursive_integrity_toolkit.reports.assembly import assemble_report

    bundle = validate_bundle(_bundle(tmp_path, ["v1::p"]), configuration=_config())
    report = phase4_step3_schema(assemble_report(bundle, run=phase4_step3_run()), repo_root)
    facts = report["observed_facts"].get("lineage", {})
    if "cycle_status" in facts:
        assert facts["cycle_status"]["status"] == "unavailable"
        assert facts["cycle_status"]["value"] is None
    for field, value in report["derived_metrics"].get("lineage", {}).items():
        if field != "resolved_parent_edge_coverage":
            assert value["status"] == "unavailable" and value["value"] is None
    for value in report["derived_metrics"].get("closure_exposure", {}).get("lineage", {}).values():
        assert value["status"] == "unavailable" and value["value"] is None
    assert "cycle_detected" not in facts and "external_root_count" not in facts
    conclusions = {item["conclusion"] for item in report["unavailable_conclusions"]}
    assert {"lineage_analysis", "external_ancestry", "causal_ancestor_effect"} <= conclusions


def test_phase4_step3_unresolved_parent_warning_survives_without_observability_downgrade(tmp_path, repo_root):
    from recursive_integrity_toolkit.reports.assembly import assemble_report

    bundle = validate_bundle(_bundle(tmp_path, ["v1::absent"]), configuration=_config())
    report = phase4_step3_schema(assemble_report(bundle, run=phase4_step3_run()), repo_root)
    assert report["observability"]["maximum_level"] == 4
    assert report["capabilities"]["lineage"]["status"] == "unavailable"
    assert report["capabilities"]["lineage"]["execution_status"] == "deferred"
    assert any(item["code"] == WarningCode.PARENT_UNRESOLVED.value for item in report["warnings"])
    assert not report["errors"] and report["run"]["run_status"] == "complete"


def test_phase4_step3_existing_parent_errors_keep_level_four_and_partial_report(tmp_path, repo_root):
    from recursive_integrity_toolkit.reports.assembly import assemble_report

    for index, parents in enumerate((["v2::c"], ["bad::format::x"])):
        bundle = validate_bundle(_bundle(tmp_path / str(index), parents), configuration=_config())
        report = phase4_step3_schema(assemble_report(bundle, run=phase4_step3_run()), repo_root)
        assert report["observability"]["maximum_level"] == 4
        assert report["capabilities"]["lineage"]["status"] == "unavailable"
        assert report["run"]["run_status"] == "partial"
        assert report["errors"] and report["inputs"]["scope"]["record_count"] == 2
        codes = {item["code"] for item in report["errors"]}
        assert codes & {ErrorCode.LINEAGE_CYCLE.value, ErrorCode.PARENT_FORMAT.value}
        assert "lineage_closure_exposure" in {item["conclusion"] for item in report["unavailable_conclusions"]}


def test_phase4_step3_assembly_never_traverses_or_revalidates_lineage(tmp_path, repo_root, monkeypatch):
    from recursive_integrity_toolkit.io import validation
    from recursive_integrity_toolkit.reports import assembly

    bundle = validate_bundle(_bundle(tmp_path, ["v1::p"]), configuration=_config())
    def phase4_step3_forbid(*args, **kwargs):
        raise AssertionError("Assembly attempted lineage traversal or validation")
    for name in ("resolve_parent_references", "validate_generation_declarations"):
        monkeypatch.setattr(validation, name, phase4_step3_forbid)
        if hasattr(assembly, name):
            monkeypatch.setattr(assembly, name, phase4_step3_forbid)
    report = phase4_step3_schema(assembly.assemble_report(bundle, run=phase4_step3_run()), repo_root)
    assert report["observability"]["maximum_level"] == 4
    assert report["capabilities"]["lineage"]["execution_status"] == "deferred"
