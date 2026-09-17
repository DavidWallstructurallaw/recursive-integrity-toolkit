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
