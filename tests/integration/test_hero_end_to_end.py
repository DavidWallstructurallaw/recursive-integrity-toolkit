"""Phase 2 Step 9 input pipeline. PR-001/002/003/004/007/009/010/011/017.

Synthetic fixtures and the unchanged approved Hero are validated without any
analytical expectation, report renderer, graph computation or simulation.
"""
import hashlib
import json
import socket
import pytest
from recursive_integrity_toolkit.config import ResourceLimits
from recursive_integrity_toolkit.errors import CanonicalValidationError, ErrorCode, ToolkitError, WarningCode
from recursive_integrity_toolkit.io.validation import validate_bundle
from recursive_integrity_toolkit.models import (
    AuditBundle, CapabilityKey, CapabilityStatus, ContentMode, FileRole, InputSource,
    NormalizationOptions, ProvenanceAssessment, RecordKey, ValidationSeverity,
)


def _records(*ids, version="v1", **fields):
    return [{"dataset_version": version, "record_id": i, "content": "synthetic text", **fields} for i in ids]


def _prov(identifier="a", **fields):
    return {"dataset_version": "v1", "record_id": identifier, "source_type": "human",
            "provenance_confidence": "confirmed", "external_grounding": "yes", "parent_ids": [], **fields}


def _table(root, name, rows, role=FileRole.RECORDS_PRIMARY):
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(''.join(json.dumps(row) + '\n' for row in rows), encoding='utf-8')
    return InputSource(role, path)


def _control(root, name, value, role):
    path = root / name
    path.write_text(json.dumps(value), encoding='utf-8')
    return InputSource(role, path)


def _topic():
    return {"representation": {"name": "topic", "source": "topic_field", "field": "topic",
                               "version": "test-v1", "missing_value_policy": "error"}}


def test_phase2_step9_hero_one_call(repo_root):
    hero = repo_root / 'examples/hero'
    names = ('records_v1.csv', 'records_v2.csv', 'provenance.csv', 'config.json', 'version_order.json', 'EXPECTED_OUTPUTS.md')
    before = {name: (hero / name).read_bytes() for name in names}
    roles = (FileRole.RECORDS_PRIMARY, FileRole.RECORDS_COMPARE, FileRole.PROVENANCE_MANIFEST, FileRole.CONFIG, FileRole.VERSION_ORDER)
    result = validate_bundle(AuditBundle(tuple(InputSource(role, name) for role, name in zip(roles, names))), base_directory=hero)
    assert result.observability.maximum_level == 4 and not result.has_errors
    assert result.observability.capabilities[CapabilityKey.MODEL_LONGITUDINAL].status is CapabilityStatus.UNAVAILABLE
    assert result.version_order.order == ('v1', 'v2') and len(result.inventory) == 5
    assert len({r.record_key for r in result.records}) == len(result.records)
    assert result.provenance_join.provenance_row_coverage.ratio == 1.0
    assert all(match.provenance is not None for match in result.provenance_join.matches)
    assert result.generation is not None and not result.generation.has_errors
    assert all(ref.canonical_reference and '::' in ref.canonical_reference
               for item in result.generation.parents for ref in item.references)
    assert {name: (hero / name).read_bytes() for name in names} == before
    for entry in result.inventory:
        assert entry.sha256 == hashlib.sha256(before[entry.path.name]).hexdigest()
    for name in ('derived_metrics', 'proxy_signals', 'simulations', 'report', 'support_size', 'ancestry_hhi'):
        assert not hasattr(result, name)


def test_phase2_step9_minimal_inline_and_metadata_only(tmp_path):
    source = _table(tmp_path, 'records.jsonl', _records('a', content='not-opened.txt'))
    inline = validate_bundle(AuditBundle((source,)))
    metadata = validate_bundle(AuditBundle((source,)), normalization_options=NormalizationOptions(content_mode=ContentMode.LOCAL_REF))
    assert inline.observability.maximum_level == 1 and metadata.observability.maximum_level == 0
    assert metadata.observability.capabilities[CapabilityKey.INGESTION].status is CapabilityStatus.AVAILABLE
    assert not metadata.content_read_keys


def test_phase2_step9_mapping_csv_keeps_quoted_empty_and_null(tmp_path):
    path = tmp_path / 'source.csv'
    path.write_text('id,text,category\n0001,synthetic,""\n0002,synthetic,null\n', encoding='utf-8')
    mapping = _control(tmp_path, 'mapping.json', {'schema_version': '1.0', 'records': {'fields': {
        'record_id': {'source': 'id'}, 'dataset_version': {'constant': 'v1'},
        'content': {'source': 'text'}, 'topic': {'source': 'category'}}}}, FileRole.SCHEMA_MAPPING)
    result = validate_bundle(AuditBundle((InputSource(FileRole.RECORDS_PRIMARY, path), mapping)))
    assert [r.record_key.record_id for r in result.records] == ['0001', '0002']
    assert result.records[0].values['topic'] == '' and result.records[1].values['topic'] is None
    assert len(result.mapping_traces) == 2
    assert result.mapping_traces[0].fields[0] == ('record_id', 'source', ('id',), ())
    assert result.records[0].location.row_number == 1 and result.records[0].location.line_number == 2


def test_phase2_step9_config_relative_paths(tmp_path):
    nested = tmp_path / 'nested'; nested.mkdir()
    _table(nested, 'records.jsonl', _records('a'))
    config = _control(nested, 'config.json', {'inputs': {'records_primary': 'records.jsonl'}}, FileRole.CONFIG)
    assert validate_bundle(AuditBundle((config,))).records[0].record_key == RecordKey('v1', 'a')


def test_phase2_step9_toml_and_output_do_not_write(tmp_path):
    _table(tmp_path, 'records.jsonl', _records('a'))
    path = tmp_path / 'config.toml'
    path.write_text('[inputs]\nrecords_primary = "records.jsonl"\n[output]\npath = "never-created"\n', encoding='utf-8')
    before = set(tmp_path.iterdir())
    result = validate_bundle(AuditBundle((InputSource(FileRole.CONFIG, path),)))
    assert len(result.records) == 1 and set(tmp_path.iterdir()) == before


@pytest.mark.parametrize('text', ['{"inputs":{},"inputs":{}}', '{"resource_limits":{"max_rows":NaN}}',
                                  '[]', '{broken', '{"output":{"x":1e999}}'])
def test_phase2_step9_bad_control_documents_fail(tmp_path, text):
    path = tmp_path / 'config.json'; path.write_text(text, encoding='utf-8')
    with pytest.raises(ToolkitError):
        validate_bundle(AuditBundle((InputSource(FileRole.CONFIG, path),)))


@pytest.mark.parametrize('roles', [(), (FileRole.RECORDS_PRIMARY, FileRole.RECORDS_PRIMARY),
                                   (FileRole.RECORDS_PRIMARY, FileRole.PROVENANCE_MANIFEST, FileRole.PROVENANCE_MANIFEST)])
def test_phase2_step9_role_cardinality_before_table_reads(tmp_path, roles):
    with pytest.raises(CanonicalValidationError) as caught:
        validate_bundle(AuditBundle(tuple(InputSource(role, tmp_path / f'{i}.jsonl') for i, role in enumerate(roles))))
    assert caught.value.code is ErrorCode.CONFIG_INVALID


def test_phase2_step9_competing_and_recursive_config_fail(tmp_path):
    source = _table(tmp_path, 'records.jsonl', _records('a'))
    config = _control(tmp_path, 'config.json', {}, FileRole.CONFIG)
    with pytest.raises(ToolkitError):
        validate_bundle(AuditBundle((source, config)), configuration={})
    with pytest.raises(ToolkitError):
        validate_bundle(AuditBundle((source,)), configuration={'inputs': {'config': 'other.json'}}, base_directory=tmp_path)
    with pytest.raises(ToolkitError):
        validate_bundle(AuditBundle((source,)), configuration={'inputs': {'records_primary': 'records.jsonl'}}, base_directory=tmp_path)


@pytest.mark.parametrize('uri', ['https://invalid.example/x.csv', 's3://bucket/x.csv', '//server/share/x.csv'])
def test_phase2_step9_remote_source_before_network(tmp_path, monkeypatch, uri):
    def no_network(*args, **kwargs):
        raise AssertionError('network was attempted')
    monkeypatch.setattr(socket, 'getaddrinfo', no_network); monkeypatch.setattr(socket, 'create_connection', no_network)
    with pytest.raises(ToolkitError):
        validate_bundle(AuditBundle((InputSource(FileRole.RECORDS_PRIMARY, uri),)), base_directory=tmp_path)


def test_phase2_step9_duplicate_identity_across_files(tmp_path):
    a = _table(tmp_path, 'one.jsonl', _records('a'))
    b = _table(tmp_path, 'two.jsonl', _records('a'), FileRole.RECORDS_COMPARE)
    with pytest.raises(CanonicalValidationError) as caught:
        validate_bundle(AuditBundle((a, b)))
    assert caught.value.code is ErrorCode.RECORD_DUPLICATE_ID


@pytest.mark.parametrize('rows,code', [([_prov('b')], ErrorCode.PROVENANCE_UNMATCHED_ROW),
                                      ([_prov(), _prov()], ErrorCode.PROVENANCE_DUPLICATE_ROW)])
def test_phase2_step9_invalid_provenance_join(tmp_path, rows, code):
    source = _table(tmp_path, 'records.jsonl', _records('a'))
    prov = _table(tmp_path, 'prov.jsonl', rows, FileRole.PROVENANCE_MANIFEST)
    with pytest.raises(CanonicalValidationError) as caught:
        validate_bundle(AuditBundle((source, prov)))
    assert caught.value.code is code


@pytest.mark.parametrize('format', ['csv', 'jsonl'])
def test_phase2_step9_incomplete_provenance_preserves_error_and_coverage(tmp_path, format):
    source = _table(tmp_path, 'records.jsonl', _records('a', 'b'))
    path = tmp_path / ('prov.' + format)
    if format == 'csv':
        path.write_text('dataset_version,record_id,source_type,external_grounding\nv1,a,human,yes\n', encoding='utf-8')
    else:
        row = _prov(); del row['provenance_confidence']; path.write_text(json.dumps(row)+'\n', encoding='utf-8')
    result = validate_bundle(AuditBundle((source, InputSource(FileRole.PROVENANCE_MANIFEST, path))))
    assert result.has_errors and type(result.provenance[0]) is ProvenanceAssessment
    assert result.provenance_join.provenance_row_coverage.ratio == 0.5
    assert result.provenance_join.provenance_required_field_coverage.ratio == 0.0
    assert result.provenance_join.grounding_field_coverage.ratio == 0.5
    assert 'provenance_confidence' not in result.provenance[0].values
    assert any(m.code == ErrorCode.SCHEMA_REQUIRED_FIELD.value for m in result.validation_messages)


def test_phase2_step9_unknown_grounding_and_missing_rows_are_distinct(tmp_path):
    source = _table(tmp_path, 'records.jsonl', _records('a', 'b'))
    prov = _table(tmp_path, 'prov.jsonl', [_prov(source_type='synthetic', external_grounding='unknown', human_reviewed=True)], FileRole.PROVENANCE_MANIFEST)
    result = validate_bundle(AuditBundle((source, prov)))
    assert result.observability.maximum_level == 2
    assert result.provenance_join.grounding_field_coverage.ratio == 0.0
    assert result.provenance[0].values['source_type'] == 'synthetic'
    assert result.provenance[0].values['external_grounding'] == 'unknown'
    assert result.provenance[0].values['human_reviewed'] is True
    assert result.provenance_join.matches[1].provenance is None


def test_phase2_step9_empty_vs_absent_manifest(tmp_path):
    source = _table(tmp_path, 'records.jsonl', _records('a')); path = tmp_path / 'prov.csv'
    path.write_text('dataset_version,record_id,source_type,provenance_confidence,external_grounding\n', encoding='utf-8')
    a = validate_bundle(AuditBundle((source,)))
    b = validate_bundle(AuditBundle((source, InputSource(FileRole.PROVENANCE_MANIFEST, path))))
    assert a.provenance is None and b.provenance == ()
    assert not a.provenance_join.provenance_supplied and b.provenance_join.provenance_supplied
    path.write_text('record_id\n', encoding='utf-8')
    with pytest.raises(CanonicalValidationError):
        validate_bundle(AuditBundle((source, InputSource(FileRole.PROVENANCE_MANIFEST, path))))


def test_phase2_step9_strict_generation_mismatch_retained(tmp_path):
    source = _table(tmp_path, 'records.jsonl', _records('a'))
    prov = _table(tmp_path, 'prov.jsonl', [_prov(generation=7)], FileRole.PROVENANCE_MANIFEST)
    result = validate_bundle(AuditBundle((source, prov)), configuration={'strict_mode': True, 'strict_warning_codes': [WarningCode.GENERATION_MISMATCH.value]})
    assert result.has_errors and result.generation.has_errors and result.provenance[0].values['generation'] == 7
    assert any(m.code == WarningCode.GENERATION_MISMATCH.value and m.severity is ValidationSeverity.ERROR for m in result.validation_messages)


def test_phase2_step9_missing_order_and_incompatible_representations(tmp_path):
    a = _table(tmp_path, 'z_early.jsonl', _records('a', topic='cat'))
    b = _table(tmp_path, 'a_late.jsonl', _records('b', version='v2', topic='dog'), FileRole.RECORDS_COMPARE)
    config = _topic()
    missing = validate_bundle(AuditBundle((a, b)), configuration=config)
    assert missing.observability.maximum_level == 1
    config['version_order'] = ['v1', 'v2']; config['representation_compatibility'] = {'v1': 'x', 'v2': 'y'}
    result = validate_bundle(AuditBundle((a, b)), configuration=config)
    assert result.observability.capabilities[CapabilityKey.DATASET_LONGITUDINAL].status is CapabilityStatus.UNAVAILABLE


def test_phase2_step9_independent_order_sources(tmp_path):
    source = _table(tmp_path, 'records.jsonl', _records('a') + _records('b', version='v2'))
    order = _control(tmp_path, 'order.json', {'version_rank': {'v1': 0, 'v2': 1}}, FileRole.VERSION_ORDER)
    result = validate_bundle(AuditBundle((source, order)), configuration={'version_order': ['v1', 'v2']})
    assert result.version_order.order == ('v1', 'v2')
    with pytest.raises(CanonicalValidationError) as caught:
        validate_bundle(AuditBundle((source, order)), configuration={'version_order': ['v2', 'v1']})
    assert caught.value.code is ErrorCode.VERSION_ORDER_CONFLICT


def test_phase2_step9_resource_limits_and_conflicts(tmp_path):
    source = _table(tmp_path, 'records.jsonl', _records('a', 'b'))
    with pytest.raises(ToolkitError):
        validate_bundle(AuditBundle((source,)), configuration={'resource_limits': {'max_rows': 1}})
    with pytest.raises(ToolkitError):
        validate_bundle(AuditBundle((source,)), configuration={'resource_limits': {'max_rows': 2}}, limits=ResourceLimits(max_rows=1))


def test_phase2_step9_deterministic_offline_no_later_imports(tmp_path, monkeypatch, capsys):
    import builtins
    original = builtins.__import__
    def guarded(name, globals=None, locals=None, fromlist=(), level=0):
        if any(part in name.split('.') for part in ('metrics', 'lineage', 'reports', 'representations')):
            raise AssertionError('later analytical layer imported')
        return original(name, globals, locals, fromlist, level)
    def no_network(*args, **kwargs):
        raise AssertionError('network was attempted')
    a = _table(tmp_path, 'a.jsonl', _records('a', topic='cat'))
    b = _table(tmp_path, 'b.jsonl', _records('b', version='v2', topic='dog'), FileRole.RECORDS_COMPARE)
    before = {p.name: p.read_bytes() for p in tmp_path.iterdir()}
    with monkeypatch.context() as patch:
        patch.setattr(builtins, '__import__', guarded); patch.setattr(socket, 'getaddrinfo', no_network); patch.setattr(socket, 'create_connection', no_network)
        left = validate_bundle(AuditBundle((a, b)), configuration=_topic(), invocation_order=('v1', 'v2'))
        right = validate_bundle(AuditBundle((b, a)), configuration=_topic(), invocation_order=('v1', 'v2'))
    assert left == right and left.observability.maximum_level == 4
    assert {p.name: p.read_bytes() for p in tmp_path.iterdir()} == before
    assert capsys.readouterr() == ('', '')


def test_phase2_step9_unsafe_mapping_cannot_execute(tmp_path):
    source = _table(tmp_path, 'records.jsonl', _records('a'))
    mapping = _control(tmp_path, 'mapping.json', {'schema_version': '1.0', 'records': {'fields': {
        'content': {'source': 'content', 'operations': [{'op': 'exec', 'value': 'UNSAFE_SENTINEL'}]}}}}, FileRole.SCHEMA_MAPPING)
    with pytest.raises(ToolkitError) as caught:
        validate_bundle(AuditBundle((source, mapping)))
    assert caught.value.code is ErrorCode.MAPPING_UNSAFE_TRANSFORM
    assert 'UNSAFE_SENTINEL' not in str(caught.value)



def phase4_step8_hero_values(report):
    """Independent section 8 targets; no output-derived golden regeneration."""
    support, diversity = report["derived_metrics"]["support"], report["derived_metrics"]["diversity"]
    assert sorted(v["support_size"]["value"] for v in support["by_version"].values()) == [5, 8]
    assert sorted(v["gini_simpson_diversity"]["value"] for v in diversity["by_version"].values()) == [0.75, 0.875]
    assert support["support_delta"]["value"] == -3 and support["support_retention_ratio"]["value"] == 0.625
    assert support["support_loss_count"]["value"] == 3 and support["support_added_count"]["value"] == 0
    assert diversity["gini_simpson_diversity_delta"]["value"] == -0.125
    assert report["derived_metrics"]["provenance"]["source_type_shares"]["value"] == {"human": 0.5, "synthetic": 0.5, "mixed": 0.0, "sensor": 0.0, "unknown": 0.0}
    assert report["derived_metrics"]["provenance"]["missing_provenance_share"]["value"] == 0
    for name in ("provenance_row_coverage", "provenance_required_field_coverage", "grounding_field_coverage"):
        assert report["observed_facts"]["provenance"][name]["value"] == 1.0
        assert report["observed_facts"]["provenance"][name]["scope"]["record_count"] == 8
    direct = report["derived_metrics"]["closure_exposure"]["direct"]
    assert [direct[n]["value"] for n in ("lower_bound", "upper_bound", "interval_width")] == [0.5, 0.5, 0]
    assert report["observability"]["maximum_level"] == 4 and report["capabilities"] == report["observability"]["capabilities"]
    assert report["capabilities"]["lineage"]["execution_status"] == "deferred"
    assert report["capabilities"]["dataset_longitudinal"]["execution_status"] == "partial"
    assert report["capabilities"]["model_longitudinal"]["status"] == "unavailable"
    assert report["capabilities"]["intervention_simulation"]["status"] == "unavailable"
    assert report["simulations"] == {} and report["errors"] == []
    assert "lineage" not in report["derived_metrics"]["closure_exposure"]
    assert "ancestry" not in report["derived_metrics"] and "shared_ancestry_dependence" not in report["proxy_signals"]
    assert "support_contraction" in report["proxy_signals"]
    assert {"model_performance_decline", "causal_ancestor_effect", "universal_integrity", "universal_collapse_prediction"} <= {item["conclusion"] for item in report["unavailable_conclusions"]}


@pytest.mark.parametrize("redacted", [False, True])
def test_phase4_step8_packaged_one_command_hero(repo_root, tmp_path, capsys, monkeypatch, redacted):
    from recursive_integrity_toolkit.cli import main
    from importlib.resources import files
    import jsonschema
    import urllib.request
    def denied(*args, **kwargs):
        raise AssertionError("network operation")
    monkeypatch.setattr(socket, "socket", denied)
    monkeypatch.setattr(socket, "getaddrinfo", denied)
    monkeypatch.setattr(urllib.request, "urlopen", denied)
    output = tmp_path / "PRIVATE_WORKSPACE"
    assert main(["example", "--out", str(output), *(["--redacted"] if redacted else [])]) == 0
    streams = capsys.readouterr()
    report = json.loads((output / "reports/report.json").read_bytes())
    phase4_step8_hero_values(report)
    assert report["run"]["command"] == "rit example" + (" --redacted" if redacted else "")
    assert "full-product reference" in streams.err and "lineage execution is deferred" in streams.err
    assert len(list((output / "inputs").iterdir())) == 6
    for path in (output / "inputs").iterdir():
        assert path.read_bytes() == (repo_root / "examples/hero" / path.name).read_bytes()
    schema = files("recursive_integrity_toolkit").joinpath("data", "report.schema.json").read_bytes()
    assert schema == (repo_root / "schemas/report.schema.json").read_bytes()
    jsonschema.Draft202012Validator(json.loads(schema)).validate(report)
    markdown = (output / "reports/report.md").read_text(encoding="utf-8")
    assert markdown.startswith("# Recursive Integrity Audit Report") and "deferred" in markdown
    if redacted:
        assert "PRIVATE_WORKSPACE" not in json.dumps(report) + markdown + streams.out + streams.err
        assert str(tmp_path) not in json.dumps(report) + markdown + streams.out + streams.err
    else:
        assert report["derived_metrics"]["support"]["extinct_states"]["value"] == ["battery", "lizard", "turtle"]
        assert [report["observed_facts"]["record_counts"][v]["value"] for v in ("v1", "v2")] == [8, 8]
        assert {a["role"]:a["row_count"] for a in report["inputs"]["artifacts"] if a["role"] in ("records_primary", "records_compare", "provenance_manifest")} == {"records_primary":8,"records_compare":8,"provenance_manifest":16}


@pytest.mark.parametrize("existing", ["empty", "file", "populated"])
def test_phase4_step8_example_never_reuses_a_workspace(tmp_path, capsys, existing):
    from recursive_integrity_toolkit.cli import main
    output = tmp_path / "out"
    if existing == "file": output.write_bytes(b"KEEP")
    else:
        output.mkdir()
        if existing == "populated": (output / "sentinel").write_bytes(b"KEEP")
    before = {p:p.read_bytes() for p in tmp_path.rglob("*") if p.is_file()}
    assert main(["example", "--out", str(output)]) == 1
    streams = capsys.readouterr()
    assert streams.out == "" and "E_OUTPUT_EXISTS" in streams.err
    assert {p:p.read_bytes() for p in tmp_path.rglob("*") if p.is_file()} == before


@pytest.mark.parametrize("path", ["https://invalid.example/x", "//server/share/x", "\\\\server\\share", "../outside", "out/../outside", "NUL", "bad\\path", "bad\x00name"])
def test_phase4_step8_example_rejects_unsafe_paths_before_resources(tmp_path, capsys, monkeypatch, path):
    from recursive_integrity_toolkit.cli import main
    import importlib.resources
    import os
    monkeypatch.chdir(tmp_path)
    accessed = []
    def denied(*args, **kwargs):
        accessed.append(True)
        raise AssertionError("resources read before path rejection")
    monkeypatch.setattr(importlib.resources, "files", denied)
    # Backslash is a native Windows separator. This case then fails because
    # its parent is absent; POSIX rejects the spelling before filesystem use.
    native_missing_parent = os.name == "nt" and path == "bad\\path"
    assert main(["example", "--out", path]) == (1 if native_missing_parent else 2)
    streams = capsys.readouterr()
    expected_code = "E_OUTPUT_IO" if native_missing_parent else "E_OUTPUT_PATH_INVALID"
    assert streams.out == "" and expected_code in streams.err
    assert not accessed and not list(tmp_path.iterdir())


def test_phase4_step8_example_extraction_failure_cleans_only_its_files(tmp_path, capsys, monkeypatch):
    from recursive_integrity_toolkit.cli import main
    from recursive_integrity_toolkit.utils import paths
    original = paths._output_write
    count = []
    def fail(path, payload, owned):
        original(path, payload, owned)
        count.append(True)
        if len(count) == 2: raise OSError("PRIVATE_DISK_ERROR")
    monkeypatch.setattr(paths, "_output_write", fail)
    assert main(["example", "--out", str(tmp_path / "out")]) == 1
    streams = capsys.readouterr()
    assert streams.out == "" and "PRIVATE_DISK_ERROR" not in streams.err
    assert not (tmp_path / "out").exists()


def test_phase4_step8_example_concurrent_reservation_does_not_overwrite(tmp_path, capsys, monkeypatch):
    from pathlib import Path
    from recursive_integrity_toolkit.cli import main
    original = Path.mkdir
    output = tmp_path / "out"
    def race(path, *args, **kwargs):
        if path == output:
            original(path)
            (path / "foreign").write_bytes(b"KEEP")
        return original(path, *args, **kwargs)
    monkeypatch.setattr(Path, "mkdir", race)
    assert main(["example", "--out", str(output)]) == 1
    streams = capsys.readouterr()
    assert streams.out == "" and (output / "foreign").read_bytes() == b"KEEP"
    assert list(output.iterdir()) == [output / "foreign"]


def test_phase4_step8_example_help_remains_lazy(tmp_path, subprocess_env):
    import subprocess
    import sys
    program = "import importlib.abc,sys\nclass Block(importlib.abc.MetaPathFinder):\n def find_spec(self,fullname,path=None,target=None):\n  if fullname.startswith(('numpy','pandas','pyarrow','recursive_integrity_toolkit.io','recursive_integrity_toolkit.config','recursive_integrity_toolkit.reports')):raise AssertionError('eager execution')\nsys.meta_path.insert(0,Block())\nfrom recursive_integrity_toolkit.cli import main\ntry:main(['example','--help'])\nexcept SystemExit as e:assert e.code==0\n"
    result = subprocess.run([sys.executable, "-c", program], cwd=tmp_path, env=subprocess_env, capture_output=True, text=True)
    assert result.returncode == 0 and "--out" in result.stdout and not list(tmp_path.iterdir())


@pytest.mark.parametrize("redacted", [False, True])
def test_phase4_step9_example_report_write_failure_preserves_inputs_and_no_network(
        repo_root, tmp_path, capsys, caplog, monkeypatch, redacted):
    import urllib.request
    from recursive_integrity_toolkit.cli import main
    from recursive_integrity_toolkit.utils import paths

    canonical = repo_root / "examples/hero"
    before = {path.name: path.read_bytes() for path in canonical.iterdir() if path.is_file()}
    calls = []
    def blocked(*args, **kwargs):
        calls.append(True)
        raise AssertionError("example attempted outbound operation")
    for owner, name in ((socket, "socket"), (socket, "create_connection"),
                        (socket, "getaddrinfo"), (socket, "gethostbyname"),
                        (urllib.request, "urlopen"), (urllib.request.OpenerDirector, "open")):
        monkeypatch.setattr(owner, name, blocked)
    staged_reports = []
    original = paths._output_write
    def fail_report(path, payload, owned):
        original(path, payload, owned)
        if path.name in {"report.json", "report.md"}:
            staged_reports.append(payload.decode("utf-8"))
        if path.name == "report.md":
            raise OSError("PRIVATE_EXAMPLE_DISK_DIAGNOSTIC_852")
    monkeypatch.setattr(paths, "_output_write", fail_report)
    output = tmp_path / "PRIVATE_EXAMPLE_DIRECTORY_852"
    args = ["example", "--out", str(output)] + (["--redacted"] if redacted else [])
    assert main(args) == 1
    streams = capsys.readouterr()
    assert calls == [] and streams.out == "" and "E_OUTPUT_IO" in streams.err
    assert len(staged_reports) == 2
    report = json.loads(staged_reports[0])
    phase4_step8_hero_values(report)
    assert report["run"]["network_call_count"] == 0
    assert "## Errors" in staged_reports[1] and "deferred" in staged_reports[1]
    extracted = {path.name: path.read_bytes() for path in (output / "inputs").iterdir()}
    assert len(extracted) == 6
    assert all(raw == before[name] for name, raw in extracted.items())
    assert {path.name: path.read_bytes() for path in canonical.iterdir() if path.is_file()} == before
    assert not any(path.is_file() for path in (output / "reports").rglob("*"))
    assert not any(path.name.startswith(".rit-stage-") for path in output.rglob("*"))
    sinks = "".join(staged_reports) + streams.err + caplog.text
    assert "PRIVATE_EXAMPLE_DISK_DIAGNOSTIC_852" not in sinks and "Traceback" not in sinks
    if redacted:
        assert str(tmp_path) not in sinks and "PRIVATE_EXAMPLE_DIRECTORY_852" not in sinks
