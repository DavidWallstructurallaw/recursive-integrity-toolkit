"""Phase 1 placeholder for PR-015.

Planned scope:
    Future redaction tests are deferred to Phase 4.

Current Phase 1 scope:
    Verify the approved owner ID and confirm that the target module remains a
    docstring-only, import-safe placeholder.

Limits:
    No mathematical metric, data loading, graph operation, or report result is tested.
"""


# Phase 4 Step 4: independently authored privacy cases.
def phase4_step4_private_report(tmp_path, *, scenario=False, duplicates=False, pair=False):
    import json
    import pytest
    from recursive_integrity_toolkit.config import RepresentationConfig
    from recursive_integrity_toolkit.io.validation import validate_bundle
    from recursive_integrity_toolkit.metrics.diversity import calculate_state_distribution
    from recursive_integrity_toolkit.models import AuditBundle, FileRole, InputSource
    from recursive_integrity_toolkit.reports.assembly import assemble_report
    from recursive_integrity_toolkit.representations.field import assign_field_states
    tmp_path.mkdir(parents=True, exist_ok=True)
    path = tmp_path / 'PATH_SENTINEL_records.jsonl'
    version = 'VERSION_SENTINEL'
    labels = ('STATE_SENTINEL_A', 'STATE_SENTINEL_A', 'STATE_SENTINEL_B', 'STATE_SENTINEL_C')
    records = [{'dataset_version': version, 'record_id': 'RECORD_SENTINEL_' + str(index), 'content': 'CONTENT_SENTINEL', 'topic': label, 'notes': 'NOTES_SENTINEL'} for index, label in enumerate(labels)]
    if pair:
        records += [{**record, 'dataset_version': 'LATER_VERSION_SENTINEL', 'topic': 'STATE_SENTINEL_A' if record['topic'] == 'STATE_SENTINEL_B' else record['topic']} for record in records]
    path.write_text(''.join((json.dumps(row) + '\n' for row in records)), encoding='utf-8')
    representation = {'name': 'topic', 'source': 'topic_field', 'field': 'topic', 'version': 'TAXONOMY_SENTINEL', 'missing_value_policy': 'exclude'}
    configuration = {'representation': representation}
    if pair:
        configuration['version_order'] = [version, 'LATER_VERSION_SENTINEL']
    bundle = validate_bundle(AuditBundle((InputSource(FileRole.RECORDS_PRIMARY, path),)), configuration=configuration)
    selected = assign_field_states(bundle.records, dataset_versions=(version,), scope_id='SCOPE_SENTINEL', config=RepresentationConfig(**representation))
    distribution = calculate_state_distribution(selected)
    distributions = (distribution,)
    nullable = ('started_at', 'completed_at', 'duration_seconds', 'python_version', 'platform', 'command', 'config_hash', 'random_seed')
    run = {'run_id': 'RUN_SENTINEL', 'toolkit_version': '0.1.0.dev2', 'report_schema_version': '1.1', **dict.fromkeys(nullable), 'strict_mode': False, 'redacted_mode': False, 'network_call_count': 0, 'deterministic': True, 'privacy_mode': 'standard', 'run_status': 'complete', 'null_reasons': {key: 'Test supplies no execution metadata.' for key in nullable}}
    kwargs = {}
    if pair:
        from recursive_integrity_toolkit.metrics.diversity import compare_support
        from recursive_integrity_toolkit.models import ExplicitPairContext
        later = calculate_state_distribution(assign_field_states(bundle.records, dataset_versions=('LATER_VERSION_SENTINEL',), scope_id='LATER_SCOPE_SENTINEL', config=RepresentationConfig(**representation)))
        distributions += (later,)
        a, b = (distribution.unweighted, later.unweighted)
        kwargs['comparison'] = compare_support(a, b, context=ExplicitPairContext(a.scope, b.scope, a.representation, b.representation, bundle.version_order), earlier_state_semantics='SEMANTICS_SENTINEL', later_state_semantics='SEMANTICS_SENTINEL')
    if scenario:
        from recursive_integrity_toolkit.metrics.resampling import simulate_closed_resampling
        kwargs['resampling'] = simulate_closed_resampling({labels[0]: 1 / 2, labels[2]: 1 / 4, labels[3]: 1 / 4}, resample_size=4, steps=2, seed=17, replicates=2, scope=distribution.unweighted.scope, representation=distribution.unweighted.representation)
    if duplicates:
        from recursive_integrity_toolkit.metrics.duplicates import detect_exact_duplicates
        from recursive_integrity_toolkit.models import ContentMode
        kwargs['duplicates'] = detect_exact_duplicates(bundle.records, dataset_versions=(version,), scope_id='DUPLICATE_SCOPE_SENTINEL', representation_version='HASH_VERSION_SENTINEL', representation_name='content_hash', normalization_profile='exact_utf8_v1', content_mode=ContentMode.INLINE)
    return assemble_report(bundle, run=run, distributions=distributions, **kwargs)


def phase4_step4_view(report, mode='redacted', record_id_mode=None, secret=b'fixed-test-only-secret-32-bytes!!'):
    import json
    import pytest
    from recursive_integrity_toolkit.reports.assembly import privacy_view
    from recursive_integrity_toolkit.utils.hashing import IdentifierProtection
    return privacy_view(report, mode=mode, record_id_mode=record_id_mode, protection=IdentifierProtection.create(secret=secret))


def phase4_step4_validate(view, repo_root):
    import json
    import pytest
    from jsonschema import Draft202012Validator
    from recursive_integrity_toolkit.result import CanonicalReport
    value = view.to_dict()
    schema = json.loads((repo_root / 'schemas/report.schema.json').read_text(encoding='utf-8'))
    Draft202012Validator(schema).validate(value)
    CanonicalReport.from_dict(value)
    return value


def phase4_step4_semantics(value):
    import json
    import pytest
    'Identity-independent existing quantitative values and evidence labels.'
    observed = []

    def walk(item):
        if type(item) is dict:
            for key, child in item.items():
                if key in {'value', 'record_count', 'excluded_record_count', 'numerator', 'denominator', 'ratio', 'coverage', 'count', 'row_number', 'probability', 'evidence_class', 'status', 'unit', 'severity', 'effect_on_run', 'execution_status', 'maximum_level', 'owner_ids', 'theory_map_ids', 'trace_ids', 'support_size', 'gini_simpson_diversity', 'state_counts', 'state_frequencies', 'step', 'replicate_index'}:
                    if type(child) in (int, float, bool, str, type(None)):
                        observed.append((key, child))
                    elif type(child) is list and key in {'owner_ids', 'theory_map_ids', 'trace_ids', 'state_counts', 'state_frequencies'}:
                        observed.append((key, child))
                walk(child)
        elif type(item) is list:
            for child in item:
                walk(child)
    for section in ('observed_facts', 'derived_metrics', 'simulations', 'proxy_signals', 'unavailable_conclusions', 'errors', 'warnings', 'capabilities'):
        walk(value[section])
    return observed


def test_phase4_step4_redacted_identity_modes_keep_numbers_and_schema(tmp_path, repo_root):
    import json
    import pytest
    for record_id_mode in ['hash', 'preserve', 'omit']:
        report = phase4_step4_private_report(tmp_path)
        original = report.to_dict()
        actual = phase4_step4_validate(phase4_step4_view(report, record_id_mode=record_id_mode), repo_root)
        text = json.dumps(actual)
        for sentinel in ('STATE_SENTINEL', 'VERSION_SENTINEL', 'SCOPE_SENTINEL', 'PATH_SENTINEL', 'TAXONOMY_SENTINEL', 'RUN_SENTINEL', 'CONTENT_SENTINEL', 'NOTES_SENTINEL'):
            assert sentinel not in text
        assert ('RECORD_SENTINEL' in text) == (record_id_mode == 'preserve')
        assert phase4_step4_semantics(actual) == phase4_step4_semantics(original)
        assert report.to_dict() == original
        assert actual['observability']['capabilities'] == actual['capabilities']
        assert actual['run']['identifier_protection']['record_id_mode'] == record_id_mode


def test_phase4_step4_standard_retains_structural_labels_but_excludes_raw_payload(tmp_path, repo_root):
    import json
    import pytest
    report = phase4_step4_private_report(tmp_path)
    actual = phase4_step4_validate(phase4_step4_view(report, mode='standard'), repo_root)
    text = json.dumps(actual)
    assert 'STATE_SENTINEL_A' in text and 'VERSION_SENTINEL' in text
    assert 'CONTENT_SENTINEL' not in text and 'NOTES_SENTINEL' not in text
    assert actual['run']['privacy_mode'] == 'standard'
    assert phase4_step4_semantics(actual) == phase4_step4_semantics(report.to_dict())


def test_phase4_step4_free_text_error_sentinels_do_not_escape(tmp_path, repo_root):
    import json
    import pytest
    for field in ['message', 'remediation', 'field', 'code']:
        for mode in ['standard', 'redacted']:
            from recursive_integrity_toolkit.result import CanonicalReport
            payload = phase4_step4_private_report(tmp_path).to_dict()
            payload['run']['run_status'] = 'partial'
            error = {'code': 'E_SCHEMA_TYPE', 'severity': 'error', 'message': 'Raw PRIVATE_ERROR_SENTINEL', 'file_role': 'records_primary', 'field': 'topic', 'record_key': None, 'row_number': 2, 'effect_on_run': 'partial', 'effect_on_capabilities': ['content_diagnostics'], 'remediation': ['Review declared input types.']}
            error[field] = ['PRIVATE_ERROR_SENTINEL'] if field == 'remediation' else 'PRIVATE_ERROR_SENTINEL'
            payload['errors'] = [error]
            actual = phase4_step4_validate(phase4_step4_view(CanonicalReport(payload), mode=mode), repo_root)
            assert 'PRIVATE_ERROR_SENTINEL' not in json.dumps(actual)
            assert actual['errors'][0]['severity'] == 'error'
            assert actual['errors'][0]['effect_on_run'] == 'partial'
            assert actual['errors'][0]['effect_on_capabilities'] == ['content_diagnostics']
            assert actual['errors'][0]['row_number'] == 2
            assert actual['run']['run_status'] == 'partial'


def test_phase4_step4_run_command_null_reasons_and_metadata_are_not_raw_sinks(tmp_path, repo_root):
    import json
    import pytest
    for mode in ['standard', 'redacted']:
        from recursive_integrity_toolkit.result import CanonicalReport
        payload = phase4_step4_private_report(tmp_path).to_dict()
        run = payload['run']
        run['command'] = 'rit audit --records /PRIVATE_COMMAND_SENTINEL --password SECRET_SENTINEL'
        run['platform'] = 'PRIVATE_PLATFORM_SENTINEL'
        for key in ('command', 'platform'):
            del run['null_reasons'][key]
        run['null_reasons']['started_at'] = 'PRIVATE_REASON_SENTINEL'
        actual = phase4_step4_validate(phase4_step4_view(CanonicalReport(payload), mode=mode), repo_root)
        serialized = json.dumps(actual)
        for sentinel in ('PRIVATE_COMMAND_SENTINEL', 'SECRET_SENTINEL', 'PRIVATE_PLATFORM_SENTINEL', 'PRIVATE_REASON_SENTINEL'):
            assert sentinel not in serialized


def test_phase4_step4_fixed_secret_reproduces_ids_and_fresh_secret_separates_runs(tmp_path):
    import json
    import pytest
    from recursive_integrity_toolkit.reports.assembly import privacy_view
    report = phase4_step4_private_report(tmp_path)
    assert phase4_step4_view(report).to_dict() == phase4_step4_view(report).to_dict()
    first = privacy_view(report, mode='redacted').to_dict()
    second = privacy_view(report, mode='redacted').to_dict()
    assert first['inputs']['scope']['dataset_versions'] != second['inputs']['scope']['dataset_versions']
    assert phase4_step4_semantics(first) == phase4_step4_semantics(second)
    assert first['run']['identifier_protection']['stability_scope'] == 'run'


def test_phase4_step4_duplicate_group_omission_is_not_missing_evidence(tmp_path, repo_root):
    import json
    import pytest
    for record_id_mode in ['hash', 'preserve', 'omit']:
        report = phase4_step4_private_report(tmp_path, duplicates=True)
        actual = phase4_step4_validate(phase4_step4_view(report, record_id_mode=record_id_mode), repo_root)
        envelope = actual['observed_facts']['content']['exact_duplicate_groups']
        assert envelope['status'] == 'available'
        assert len(envelope['value']) == 1
        group = envelope['value'][0]
        assert group['record_count'] == 4
        if record_id_mode == 'omit':
            assert group['record_keys'] is None
            assert group['redaction'] == {'omitted_fields': ['record_keys'], 'reason': 'redacted_identity_details'}
        else:
            assert len(group['record_keys']) == 4
            assert 'redaction' not in group
        assert phase4_step4_semantics(actual) == phase4_step4_semantics(report.to_dict())


def test_phase4_step4_simulation_state_identity_keeps_array_positions_and_values(tmp_path, repo_root):
    import json
    import pytest
    report = phase4_step4_private_report(tmp_path, scenario=True)
    actual = phase4_step4_validate(phase4_step4_view(report), repo_root)
    assert 'STATE_SENTINEL' not in json.dumps(actual)
    before = report.to_dict()['simulations']['closed_resampling']
    after = actual['simulations']['closed_resampling']
    assert len(before['parameters']['state_order']) == len(after['parameters']['state_order'])
    assert phase4_step4_semantics(report.to_dict()) == phase4_step4_semantics(actual)


def test_phase4_step4_transform_executes_no_io_input_or_calculation(tmp_path, monkeypatch):
    import json
    import pytest
    import builtins
    import socket
    from pathlib import Path
    from recursive_integrity_toolkit import config
    from recursive_integrity_toolkit.io import validation
    from recursive_integrity_toolkit.metrics import diversity, resampling
    report = phase4_step4_private_report(tmp_path, scenario=True)

    def forbidden(*args, **kwargs):
        raise AssertionError('Privacy transform crossed pure supplied-data boundary')
    with monkeypatch.context() as patch:
        for owner, name in ((builtins, 'open'), (Path, 'open'), (socket, 'socket'), (socket, 'getaddrinfo'), (config, 'load_config'), (validation, 'validate_bundle'), (diversity, 'calculate_state_distribution'), (resampling, 'simulate_closed_resampling')):
            patch.setattr(owner, name, forbidden)
        actual = phase4_step4_view(report).to_dict()
    assert actual['run']['network_call_count'] == 0


def test_phase4_step4_safe_view_is_immutable_and_detached(tmp_path):
    import json
    import pytest
    view = phase4_step4_view(phase4_step4_private_report(tmp_path))
    original = view.to_dict()
    edited = view.to_dict()
    edited['inputs']['version_order'].append('changed')
    assert view.to_dict() == original
    with pytest.raises(TypeError):
        view.sections['run']['run_id'] = 'changed'


def test_phase4_step4_unsupported_privacy_modes_fail_closed(tmp_path):
    import json
    import pytest
    for mode in ['debug', 'raw', '', None, True]:
        with pytest.raises((TypeError, ValueError)):
            phase4_step4_view(phase4_step4_private_report(tmp_path), mode=mode)


def test_phase4_step4_pair_scopes_map_keys_and_shared_semantics_stay_consistent(tmp_path, repo_root):
    import json
    import pytest
    report = phase4_step4_private_report(tmp_path, pair=True)
    actual = phase4_step4_validate(phase4_step4_view(report), repo_root)
    text = json.dumps(actual)
    assert 'SENTINEL' not in text
    assert phase4_step4_semantics(actual) == phase4_step4_semantics(report.to_dict())
    support = actual['derived_metrics']['support']
    assert support['support_delta']['value'] == -1
    assert support['support_retention_ratio']['value'] == 2 / 3
    assert len(support['extinct_states']['value']) == 1
    assert set(support['by_version']) == set(actual['inputs']['version_order'])


def test_phase4_step4_omitted_exclusion_identity_retains_scope_counts_and_reason(tmp_path, repo_root):
    import json
    import pytest
    from recursive_integrity_toolkit.result import CanonicalReport
    payload = phase4_step4_private_report(tmp_path).to_dict()
    scope = payload['inputs']['scope']
    excluded = {'dataset_version': 'VERSION_SENTINEL', 'record_id': 'EXCLUDED_RECORD_SENTINEL'}
    scope['excluded_record_count'] = 1
    scope['excluded_record_keys'] = [excluded]
    scope['exclusions'] = [{'record_key': excluded, 'reason_codes': ['R_CALC_EMPTY_SCOPE']}]
    report = CanonicalReport(payload)
    actual = phase4_step4_validate(phase4_step4_view(report, record_id_mode='omit'), repo_root)
    assert actual['inputs']['scope']['record_count'] == 4
    assert actual['inputs']['scope']['excluded_record_count'] == 1
    assert 'excluded_record_keys' not in actual['inputs']['scope']
    assert 'EXCLUDED_RECORD_SENTINEL' not in json.dumps(actual)
    assert any(('R_CALC_EMPTY_SCOPE' in line for line in actual['run']['identifier_protection']['limitations']))


def test_phase4_step4_metadata_builder_and_selected_privacy_form_one_valid_pipeline(tmp_path, repo_root):
    import json
    import pytest
    from recursive_integrity_toolkit.config import resolve_phase4_options
    from recursive_integrity_toolkit.reports.assembly import build_run_metadata
    from recursive_integrity_toolkit.result import CanonicalReport
    options = resolve_phase4_options(cli={'records': 'PRIVATE_INPUT_SENTINEL.jsonl', 'redacted': True, 'out': 'PRIVATE_OUTPUT_SENTINEL'})
    run = build_run_metadata(options=options, run_id='RUN_SENTINEL', operation='audit', started_at='2026-09-19T00:00:00Z', completed_at='2026-09-19T00:00:01Z', duration_seconds=1, python_version='3.12.14', platform='Linux')
    assert run['privacy_mode'] == 'standard' and run['redacted_mode'] is False
    payload = phase4_step4_private_report(tmp_path).to_dict()
    payload['run'] = run
    actual = phase4_step4_validate(phase4_step4_view(CanonicalReport(payload)), repo_root)
    assert actual['run']['command'] == 'rit audit --redacted'
    assert actual['run']['resolved_options']['privacy_mode'] == 'redacted'
    assert actual['run']['duration_seconds'] == 1
    assert actual['run']['config_hash'] == run['config_hash']
    assert actual['run']['network_count_scope'] == 'toolkit_managed_outbound_operations'
    assert actual['run']['config_hash_exclusions'] == ['id_salt_file', 'identifier_secret_material']
    assert 'PRIVATE_INPUT_SENTINEL' not in json.dumps(actual)
    assert 'PRIVATE_OUTPUT_SENTINEL' not in json.dumps(actual)


def test_phase4_step4_redacted_content_digest_states_are_not_raw_hashes(tmp_path, repo_root):
    import json
    import pytest
    from recursive_integrity_toolkit.result import CanonicalReport
    from recursive_integrity_toolkit.utils.hashing import sha256_bytes
    payload = phase4_step4_private_report(tmp_path).to_dict()
    digest = sha256_bytes(b'sensitive record content')

    def substitute(value):
        if type(value) is str:
            return digest if value == 'STATE_SENTINEL_A' else value
        if type(value) is list:
            return [substitute(item) for item in value]
        if type(value) is dict:
            return {key: substitute(item) for key, item in value.items()}
        return value
    payload = substitute(payload)
    actual = phase4_step4_validate(phase4_step4_view(CanonicalReport(payload)), repo_root)
    assert digest not in json.dumps(actual)
    assert actual['inputs']['file_hashes'] == payload['inputs']['file_hashes']


def test_phase4_step4_unknown_diagnostic_code_has_one_identity_across_sections(tmp_path, repo_root):
    import json
    import pytest
    from recursive_integrity_toolkit.result import CanonicalReport
    payload = phase4_step4_private_report(tmp_path).to_dict()
    payload['run']['run_status'] = 'partial'
    payload['errors'] = [{'code': 'PRIVATE_CODE_SENTINEL', 'severity': 'error', 'message': 'PRIVATE_TEXT_SENTINEL', 'file_role': 'records_primary', 'field': 'topic', 'record_key': None, 'row_number': 1, 'effect_on_run': 'partial', 'effect_on_capabilities': ['content_diagnostics'], 'remediation': []}]
    payload['inputs']['artifacts'][0]['reason_codes'] = ['PRIVATE_CODE_SENTINEL']
    actual = phase4_step4_validate(phase4_step4_view(CanonicalReport(payload)), repo_root)
    assert actual['errors'][0]['code'] == actual['inputs']['artifacts'][0]['reason_codes'][0]
    assert 'PRIVATE_CODE_SENTINEL' not in json.dumps(actual)


def test_phase4_step4_selected_view_cannot_rewrite_hashed_configuration_meaning(tmp_path):
    import pytest
    from recursive_integrity_toolkit.config import resolve_phase4_options
    from recursive_integrity_toolkit.reports.assembly import build_run_metadata, privacy_view
    from recursive_integrity_toolkit.result import CanonicalReport
    payload = phase4_step4_private_report(tmp_path).to_dict()
    payload["run"] = build_run_metadata(options=resolve_phase4_options(cli={"redacted": True}),
                                         run_id="configured-private-run")
    report = CanonicalReport(payload)
    for selected in ({"mode": "standard"}, {"mode": "redacted", "record_id_mode": "preserve"}):
        with pytest.raises((TypeError, ValueError)):
            privacy_view(report, **selected)
