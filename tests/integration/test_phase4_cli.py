"""P4-D06: independent CLI cases, failure retention and input-only boundaries."""
from __future__ import annotations

import json
from pathlib import Path

import pytest


def phase4_step7_inputs(directory, *, representation=True, provenance=False):
    records = directory / "records.jsonl"
    rows = [{"dataset_version": "v1", "record_id": str(i), "content": "PRIVATE_CONTENT_" + str(i),
             "topic": topic, "weight": weight} for i, (topic, weight) in enumerate(
                (("A", 10.0), ("A", 1.0), ("B", 1.0), ("C", 1.0)))]
    records.write_text("\n".join(json.dumps(row) for row in rows), encoding="utf-8")
    config = directory / "config.json"
    config.write_text(json.dumps({"representation": {"name": "topic", "source": "topic_field", "field": "topic",
        "version": "1", "missing_value_policy": "exclude"}} if representation else {}), encoding="utf-8")
    args = ["--records", str(records), "--config", str(config)]
    if provenance:
        manifest = directory / "provenance.jsonl"
        manifest.write_text("\n".join(json.dumps({"dataset_version": "v1", "record_id": str(i),
            "source_type": source, "provenance_confidence": "confirmed", "external_grounding": grounding})
            for i, (source, grounding) in enumerate((("human", "yes"), ("synthetic", "no"), ("mixed", "unknown")))), encoding="utf-8")
        args += ["--provenance", str(manifest)]
    return args, records, config


def phase4_step7_invoke(args, directory, capsys, command="audit"):
    from recursive_integrity_toolkit.cli import main
    code = main([command, *args, "--out", str(directory)])
    streams = capsys.readouterr()
    report = json.loads((directory / "report.json").read_bytes()) if (directory / "report.json").exists() else None
    if report is not None:
        from recursive_integrity_toolkit.result import validate_report, SECTION_ORDER
        validate_report(report)
        assert set(report) == set(SECTION_ORDER)
        assert (directory / "report.md").read_text(encoding="utf-8").startswith("# Recursive Integrity Audit Report\n")
    return code, report, streams


def test_phase4_step7_explicit_single_version_metrics_match_hand_counts(tmp_path, capsys):
    args, records, config = phase4_step7_inputs(tmp_path, provenance=True)
    before = {path: path.read_bytes() for path in tmp_path.iterdir()}
    code, report, streams = phase4_step7_invoke(args, tmp_path / "out", capsys)
    assert code == 0 and report["run"]["run_status"] == "complete"
    assert report["derived_metrics"]["support"]["by_version"]["v1"]["support_size"]["value"] == 3
    assert report["derived_metrics"]["diversity"]["by_version"]["v1"]["gini_simpson_diversity"]["value"] == 0.625
    direct = report["derived_metrics"]["closure_exposure"]["direct"]
    assert [direct[key]["value"] for key in ("lower_bound", "upper_bound", "interval_width")] == [0.25, 0.75, 0.5]
    assert report["run"]["resolved_options"]["weighted"] is False
    assert "weighted_support_size" not in report["derived_metrics"]["support"]["by_version"]["v1"]
    assert report["simulations"] == {} and "tail" not in report["derived_metrics"]
    assert report["capabilities"]["lineage"]["execution_status"] == "deferred"
    assert report["capabilities"] == report["observability"]["capabilities"]
    assert all(path.read_bytes() == data for path, data in before.items())
    assert {artifact["role"] for artifact in report["inputs"]["artifacts"]} == {"config", "records_primary", "provenance_manifest"}
    assert json.loads(streams.out)["reports"] == [str(tmp_path / "out" / name) for name in ("report.json", "report.md")]
    assert "PRIVATE_CONTENT_" not in json.dumps(report) + streams.out + streams.err + (tmp_path / "out/report.md").read_text()


def test_phase4_step7_missing_representation_is_limited_success_without_fallback(tmp_path, capsys):
    args, records, config = phase4_step7_inputs(tmp_path, representation=False)
    code, report, streams = phase4_step7_invoke(args, tmp_path / "out", capsys)
    assert code == 0 and report["run"]["run_status"] == "complete"
    assert report["inputs"]["representation"] is None
    assert "support" not in report["derived_metrics"] and "diversity" not in report["derived_metrics"]
    assert "content" not in report["observed_facts"]
    # The accepted direct-bounds API requires a supplied manifest. No manifest
    # preserves unavailable endpoints instead of inventing a [0, 1] result.
    for endpoint in ("lower_bound", "upper_bound", "interval_width"):
        item = report["derived_metrics"]["closure_exposure"]["direct"][endpoint]
        assert item["value"] is None and item["status"] == "unavailable"
        assert item["reason_codes"] and item["required_evidence"]
    assert report["capabilities"]["content_diagnostics"]["execution_status"] == "not_requested"
    assert report["unavailable_conclusions"] and report["warnings"] and not report["errors"]


@pytest.mark.parametrize("rule,threshold,expected", [
    ("singleton_count", None, 2), ("count_at_or_below", "0", 0),
    ("count_at_or_below", "1", 2), ("frequency_at_or_below", "0.25", 2),
    ("frequency_at_or_below", "1", 3),
])
def test_phase4_step7_tail_only_uses_explicit_rule(tmp_path, capsys, rule, threshold, expected):
    args, records, config = phase4_step7_inputs(tmp_path)
    args += ["--tail-rule", rule]
    if threshold is not None:
        args += ["--tail-threshold", threshold]
    code, report, streams = phase4_step7_invoke(args, tmp_path / "out", capsys)
    assert code == 0 and report["derived_metrics"]["tail"]["tail_support_size"]["value"] == expected
    assert report["derived_metrics"]["tail"]["selection"]["rule"] == rule
    assert report["simulations"] == {}


@pytest.mark.parametrize("args", [
    ["--tail-threshold", "1"], ["--tail-rule", "singleton_count", "--tail-threshold", "1"],
    ["--tail-rule", "count_at_or_below"], ["--tail-rule", "count_at_or_below", "--tail-threshold", "1.0"],
    ["--tail-rule", "count_at_or_below", "--tail-threshold", "-1"],
    ["--tail-rule", "frequency_at_or_below", "--tail-threshold", "nan"],
    ["--tail-rule", "frequency_at_or_below", "--tail-threshold", "inf"],
    ["--tail-rule", "frequency_at_or_below", "--tail-threshold", "1.1"],
    ["--tail-rule", "state_list"], ["--missing-state-id", "PRIVATE_SENTINEL"],
    ["--record-ids", "omit"], ["--id-salt-file", "PRIVATE_SECRET"],
    ["--compare", "PRIVATE_COMPARE"], ["--state-semantics", "PRIVATE_MEANING"],
    ["--simulation"], ["--debug"], ["--force"], ["--rec", "PRIVATE_PATH"],
])
def test_phase4_step7_unsupported_or_invalid_options_fail_safely(tmp_path, capsys, args):
    base, records, config = phase4_step7_inputs(tmp_path)
    code, report, streams = phase4_step7_invoke(base + args, tmp_path / "out", capsys)
    assert code == 2
    assert "PRIVATE_" not in streams.out + streams.err + json.dumps(report)
    if report is not None:
        assert report["run"]["run_status"] == "failed" and report["errors"]
        assert report["derived_metrics"] == {} and report["observed_facts"] == {}


@pytest.mark.parametrize("flag,value", [
    ("--records", "a"), ("--config", "a"), ("--provenance", "a"), ("--compare", "a"),
    ("--out", "a"), ("--schema-mapping", "a"), ("--version-order", "a"),
    ("--tail-rule", "singleton_count"), ("--tail-threshold", "1"),
    ("--redacted", None), ("--strict", None),
])
def test_phase4_step7_repeated_singletons_do_not_silently_override(tmp_path, capsys, flag, value):
    from recursive_integrity_toolkit.cli import main
    option = [flag] if value is None else [flag, value]
    assert main(["audit", "--records", "a", *option, *option]) == 2
    streams = capsys.readouterr()
    assert streams.out == "" and "E_CONFIG_INVALID" in streams.err
    assert not list(tmp_path.iterdir())


@pytest.mark.parametrize("configuration,extra", [
    ({"privacy_mode": "standard"}, ["--redacted"]),
    ({"strict_mode": False}, ["--strict"]),
    ({"output": {"directory": "other"}}, []),
    ({"inputs": {"records_primary": "other.jsonl"}}, []),
    ({"output": {"unknown": "PRIVATE_VALUE"}}, []),
    ({"output": {"record_id_mode": False}}, []),
    ({"privacy_mode": "debug"}, []),
    ({"simulation": {"enabled": True, "seed": 1}}, []),
    ({"state_mapping": {"A": "B"}}, []),
    ({"inputs": {"records_compare": "compare.jsonl"}}, []),
    ({"unknown": "PRIVATE_VALUE"}, []),
])
def test_phase4_step7_configuration_conflicts_and_closed_options(tmp_path, capsys, configuration, extra):
    args, records, config = phase4_step7_inputs(tmp_path)
    config.write_text(json.dumps(configuration))
    code, report, streams = phase4_step7_invoke(args + extra, tmp_path / "out", capsys)
    assert code == 2 and "PRIVATE_VALUE" not in streams.err + json.dumps(report)


@pytest.mark.parametrize("policy,sentinel,expected,exit_code", [
    ("exclude", None, 2, 0), ("explicit_missing_state", "MISSING", 3, 0),
    ("explicit_missing_state", None, None, 2), ("explicit_missing_state", "A", None, 2),
    ("error", None, None, 1),
])
def test_phase4_step7_missing_state_policy_preserves_provenance_scope(tmp_path, capsys, policy, sentinel, expected, exit_code):
    args, records, config = phase4_step7_inputs(tmp_path)
    rows = [json.loads(line) for line in records.read_text().splitlines()]
    rows[-1]["topic"] = None
    records.write_text("\n".join(json.dumps(row) for row in rows))
    raw = json.loads(config.read_text()); raw["representation"]["missing_value_policy"] = policy
    config.write_text(json.dumps(raw))
    if sentinel is not None:
        args += ["--missing-state-id", sentinel]
    code, report, streams = phase4_step7_invoke(args, tmp_path / "out", capsys)
    assert code == exit_code
    if expected is not None:
        support = report["derived_metrics"]["support"]["by_version"]["v1"]["support_size"]
        assert support["value"] == expected
        assert support["scope"]["record_count"] == (3 if policy == "exclude" else 4)
        assert report["derived_metrics"]["closure_exposure"]["direct"]["lower_bound"]["scope"]["record_count"] == 4
    elif sentinel == "A" or policy == "error":
        assert report["run"]["run_status"] == "partial"
        assert "closure_exposure" in report["derived_metrics"] and "support" not in report["derived_metrics"]


@pytest.mark.parametrize("profile,expected", [("exact_utf8_v1", 0), ("unsupported", 2)])
def test_phase4_step7_explicit_content_hash_and_duplicates(tmp_path, capsys, profile, expected):
    args, records, config = phase4_step7_inputs(tmp_path)
    rows = [json.loads(line) for line in records.read_text().splitlines()]
    rows[-1]["content"] = rows[0]["content"]
    records.write_text("\n".join(json.dumps(row) for row in rows))
    config.write_text(json.dumps({"representation": {"name": "exact", "source": "content_hash", "field": "content",
        "version": "1", "missing_value_policy": "error", "normalization_profile": profile}}))
    code, report, streams = phase4_step7_invoke(args, tmp_path / "out", capsys)
    assert code == expected
    if expected == 0:
        assert report["observed_facts"]["content"]["duplicate_record_count"]["value"] == 1
        assert report["observed_facts"]["content"]["duplicate_group_count"]["value"] == 1
        assert report["derived_metrics"]["support"]["by_version"]["v1"]["support_size"]["value"] == 3


def test_phase4_step7_validate_blocks_every_calculation_and_content_reader(tmp_path, capsys, monkeypatch):
    import importlib
    import inspect
    from recursive_integrity_toolkit import cli
    from recursive_integrity_toolkit.reports import assembly
    from recursive_integrity_toolkit.io import loaders
    args, records, config = phase4_step7_inputs(tmp_path, provenance=True)
    touched = []
    def denied(*args, **kwargs):
        touched.append(True)
        raise AssertionError("calculation or content-reference reader executed")
    for name in ("metrics.diversity", "metrics.provenance", "metrics.bounds", "metrics.duplicates", "metrics.tail",
                 "metrics.resampling", "representations.base", "representations.field", "representations.content_hash",
                 "representations.compatibility"):
        module = importlib.import_module("recursive_integrity_toolkit." + name)
        for key, value in vars(module).copy().items():
            if inspect.isfunction(value) and value.__module__ == module.__name__:
                monkeypatch.setattr(module, key, denied)
    monkeypatch.setattr(cli, "_calculations", denied)
    monkeypatch.setattr(loaders, "load_content_reference", denied)
    code, report, streams = phase4_step7_invoke(args, tmp_path / "out", capsys, command="validate")
    assert code == 0 and touched == [] and report["run"]["run_status"] == "complete"
    assert report["derived_metrics"] == report["proxy_signals"] == report["simulations"] == {}
    assert report["observed_facts"]["record_counts"]["v1"]["value"] == 4
    assert report["capabilities"]["provenance"]["execution_status"] == "not_requested"


@pytest.mark.parametrize("command,expected", [("audit", 1), ("validate", 0)])
def test_phase4_step7_multiple_versions_are_never_implicitly_pooled(tmp_path, capsys, command, expected):
    args, records, config = phase4_step7_inputs(tmp_path)
    rows = [json.loads(line) for line in records.read_text().splitlines()]
    rows[-1]["dataset_version"] = "v2"
    records.write_text("\n".join(json.dumps(row) for row in rows))
    code, report, streams = phase4_step7_invoke(args, tmp_path / "out", capsys, command=command)
    assert code == expected
    assert report["inputs"]["scope"]["dataset_versions"] == ["v1", "v2"]
    assert set(report["observed_facts"]["record_counts"]) == {"v1", "v2"}
    assert "support" not in report["derived_metrics"] and "provenance" not in report["derived_metrics"]
    assert report["run"]["run_status"] == ("partial" if command == "audit" else "complete")
    assert report["inputs"]["artifacts"]


@pytest.mark.parametrize("contents,code", [(b"", "E_EMPTY_DATASET"), (b"{PRIVATE_CONTENT", "E_FILE_PARSE"),
                                         (b"\xff", "E_FILE_ENCODING")])
def test_phase4_step7_empty_or_malformed_inputs_emit_error_only_pair(tmp_path, capsys, contents, code):
    args, records, config = phase4_step7_inputs(tmp_path)
    records.write_bytes(contents)
    status, report, streams = phase4_step7_invoke(args, tmp_path / "out", capsys)
    assert status == 1 and report["run"]["run_status"] == "failed"
    assert report["errors"][0]["code"] == code
    assert report["observed_facts"] == report["derived_metrics"] == report["inputs"] == {}
    assert "PRIVATE_CONTENT" not in streams.err + json.dumps(report)


@pytest.mark.parametrize("strict,codes,expected", [(False, [], 0), (True, [], 0), (True, ["W_PROVENANCE_MISSING_ROW"], 1)])
def test_phase4_step7_strict_promotion_uses_configured_codes(tmp_path, capsys, strict, codes, expected):
    args, records, config = phase4_step7_inputs(tmp_path)
    data = json.loads(config.read_text());data["strict_warning_codes"] = codes
    config.write_text(json.dumps(data))
    if strict:
        args += ["--strict"]
    code, report, streams = phase4_step7_invoke(args, tmp_path / "out", capsys)
    assert code == expected
    assert report["run"]["run_status"] == ("partial" if expected else "complete")
    assert report["derived_metrics"]["support"]["by_version"]["v1"]["support_size"]["value"] == 3


@pytest.mark.parametrize("module,name,extra", [
    ("metrics.provenance", "summarize_provenance", []), ("metrics.bounds", "direct_closure_exposure", []),
    ("representations.field", "assign_field_states", []), ("metrics.diversity", "calculate_state_distribution", []),
    ("metrics.tail", "select_tail", ["--tail-rule", "singleton_count"]),
])
def test_phase4_step7_family_failure_retains_independent_evidence(tmp_path, capsys, monkeypatch, module, name, extra):
    import importlib
    args, records, config = phase4_step7_inputs(tmp_path)
    def denied(*args, **kwargs):
        raise RuntimeError("PRIVATE_EXCEPTION_BODY")
    monkeypatch.setattr(importlib.import_module("recursive_integrity_toolkit." + module), name, denied)
    code, report, streams = phase4_step7_invoke(args + extra, tmp_path / "out", capsys)
    assert code == 4 and report["run"]["run_status"] == "partial"
    assert report["errors"] and report["observed_facts"]["record_counts"]["v1"]["value"] == 4
    assert ("support" in report["derived_metrics"]) if module in ("metrics.provenance", "metrics.bounds", "metrics.tail") else ("provenance" in report["derived_metrics"])
    assert "PRIVATE_EXCEPTION_BODY" not in json.dumps(report) + streams.err + streams.out


@pytest.mark.parametrize("mode", ["preserve", "hash", "omit"])
def test_phase4_step7_redacted_all_sinks_and_secret_reservations(tmp_path, capsys, mode):
    args, records, config = phase4_step7_inputs(tmp_path)
    text = records.read_text().replace('"v1"', '"PRIVATE_VERSION"').replace('"A"', '"PRIVATE_STATE"')
    records.write_text(text)
    salt = tmp_path / "PRIVATE_SALT_PATH";salt.write_bytes(b"PRIVATE_SECRET_MATERIAL_123456789012")
    code, report, streams = phase4_step7_invoke(args + ["--redacted", "--record-ids", mode, "--id-salt-file", str(salt)], tmp_path / "PRIVATE_OUT", capsys)
    assert code == 0 and report["run"]["identifier_protection"]["stability_scope"] == "cross_run"
    emitted = json.dumps(report) + streams.err + streams.out + (tmp_path / "PRIVATE_OUT/report.md").read_text()
    assert "PRIVATE_" not in emitted and str(tmp_path) not in emitted
    assert json.loads(streams.out)["reports"] == ["report.json", "report.md"]
    assert report["run"]["resolved_options"]["record_id_mode"] == mode
    assert report["run"]["network_call_count"] == 0


def test_phase4_step7_publication_failure_does_not_overwrite_and_input_collision_fails(tmp_path, capsys):
    from recursive_integrity_toolkit.cli import main
    args, records, config = phase4_step7_inputs(tmp_path)
    output = tmp_path / "out";output.mkdir();target = output / "report.json";target.write_bytes(b"KEEP")
    code = main(["audit", *args, "--out", str(output)])
    streams = capsys.readouterr()
    assert code == 1 and streams.out == "" and "E_OUTPUT_EXISTS" in streams.err
    assert target.read_bytes() == b"KEEP" and not (output / "report.md").exists()


@pytest.mark.parametrize("codes,expected", [([], 0), ([0, 1], 1), ([1, 3], 3), ([3, 2], 2), ([1, 2, 3, 4], 4), ([4, 3, 2, 1], 4)])
def test_phase4_step7_exit_precedence_is_order_independent(codes, expected):
    from recursive_integrity_toolkit.cli import _exit_code
    assert _exit_code(codes) == expected
    assert _exit_code(tuple(reversed(codes))) == expected


def test_phase4_step7_config_paths_are_relative_to_config_and_default_output_to_cwd(tmp_path, capsys, monkeypatch):
    from recursive_integrity_toolkit.cli import main
    controls = tmp_path / "controls";controls.mkdir()
    args, records, config = phase4_step7_inputs(controls, provenance=True)
    data = json.loads(config.read_text());data["inputs"] = {"provenance_manifest": "provenance.jsonl"}
    data["output"] = {"directory": "reports"}
    config.write_text(json.dumps(data))
    monkeypatch.chdir(tmp_path)
    assert main(["audit", "--records", str(records), "--config", str(config)]) == 0
    capsys.readouterr()
    report = json.loads((controls / "reports/report.json").read_bytes())
    assert report["derived_metrics"]["closure_exposure"]["direct"]["lower_bound"]["value"] == 0.25
    assert main(["validate", "--records", str(records)]) == 0
    capsys.readouterr()
    assert (tmp_path / "rit-report/report.json").is_file()


def test_phase4_step7_config_and_input_resource_limits_are_enforced(tmp_path, capsys):
    args, records, config = phase4_step7_inputs(tmp_path)
    config.write_text(json.dumps({"resource_limits": {"max_rows": 2}}))
    code, report, streams = phase4_step7_invoke(args, tmp_path / "out", capsys)
    assert code == 1 and report["errors"][0]["code"] == "E_FILE_PARSE"


def test_phase4_step7_help_and_version_execute_without_analytical_imports(subprocess_env, tmp_path):
    import subprocess
    import sys
    program = '''import importlib.abc,sys
class Block(importlib.abc.MetaPathFinder):
 def find_spec(self,fullname,path=None,target=None):
  if fullname.split('.')[0] in ('numpy','pandas','pyarrow') or fullname.startswith(('recursive_integrity_toolkit.io','recursive_integrity_toolkit.metrics','recursive_integrity_toolkit.reports','recursive_integrity_toolkit.config')):
   raise AssertionError('startup crossed lazy boundary')
sys.meta_path.insert(0,Block())
from recursive_integrity_toolkit.cli import main
for args in ([],['--help'],['--version'],['version'],['audit','--help'],['validate','--help']):
 try: assert main(args)==0
 except SystemExit as error: assert error.code==0
'''
    result = subprocess.run([sys.executable, "-c", program], cwd=tmp_path, env=subprocess_env, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert "0.1.0.dev3" in result.stdout and "--records" in result.stdout
    assert not list(tmp_path.iterdir())


def test_phase4_step7_ordinary_audit_with_network_operations_blocked(tmp_path, capsys, monkeypatch):
    import socket
    from recursive_integrity_toolkit.io import loaders
    args, records, config = phase4_step7_inputs(tmp_path)
    def denied(*args, **kwargs):
        raise AssertionError("network or content-reference operation forbidden")
    monkeypatch.setattr(socket, "socket", denied)
    monkeypatch.setattr(socket, "getaddrinfo", denied)
    monkeypatch.setattr(loaders, "load_content_reference", denied)
    code, report, streams = phase4_step7_invoke(args, tmp_path / "out", capsys)
    assert code == 0 and report["run"]["network_call_count"] == 0

@pytest.mark.parametrize("contents", [b'{"strict_mode":true,"strict_mode":false}', b'{"x":NaN}', b'{PRIVATE_CONFIG', b'\xff'])
def test_phase4_step7_malformed_configuration_is_exit_two(tmp_path, capsys, contents):
    args, records, config = phase4_step7_inputs(tmp_path)
    config.write_bytes(contents)
    code, report, streams = phase4_step7_invoke(args, tmp_path / "out", capsys)
    assert code == 2 and report["errors"][0]["code"] == "E_CONFIG_INVALID"
    assert "PRIVATE_CONFIG" not in streams.err + json.dumps(report)


@pytest.mark.parametrize("unsupported,expected", [(False, 3), (True, 2)])
def test_phase4_step7_existing_lineage_error_retains_metrics_and_precedence(tmp_path, capsys, unsupported, expected):
    args, records, config = phase4_step7_inputs(tmp_path, provenance=True)
    manifest = tmp_path / "provenance.jsonl"
    rows = [json.loads(line) for line in manifest.read_text().splitlines()]
    rows[0]["parent_ids"] = ["v1::too::many"]
    manifest.write_text("\n".join(json.dumps(row) for row in rows))
    if unsupported:
        data = json.loads(config.read_text());data["representation"]["source"] = "unsupported"
        config.write_text(json.dumps(data))
    code, report, streams = phase4_step7_invoke(args, tmp_path / "out", capsys)
    assert code == expected and report["run"]["run_status"] == "partial"
    assert "E_PARENT_FORMAT" in {item["code"] for item in report["errors"]}
    assert report["observed_facts"]["record_counts"]["v1"]["value"] == 4
    assert "closure_exposure" in report["derived_metrics"]
    assert report["capabilities"]["lineage"]["execution_status"] == "deferred"
    if not unsupported:
        assert report["derived_metrics"]["support"]["by_version"]["v1"]["support_size"]["value"] == 3


def test_phase4_step7_salt_file_is_a_protected_input_target(tmp_path, capsys):
    from recursive_integrity_toolkit.cli import main
    args, records, config = phase4_step7_inputs(tmp_path)
    output = tmp_path / "out";output.mkdir();salt = output / "report.json"
    secret = b"PRIVATE_SECRET_INPUT_123456789012345"
    salt.write_bytes(secret)
    code = main(["audit", *args, "--redacted", "--id-salt-file", str(salt), "--out", str(output)])
    streams = capsys.readouterr()
    assert code == 1 and "E_OUTPUT_INPUT_COLLISION" in streams.err
    assert streams.out == "" and "PRIVATE_SECRET_INPUT" not in streams.err
    assert salt.read_bytes() == secret and not (output / "report.md").exists()


def test_phase4_step7_outer_internal_failure_never_exposes_traceback(tmp_path, capsys, monkeypatch):
    from recursive_integrity_toolkit import cli
    def broken(*args, **kwargs):
        raise RuntimeError("PRIVATE_INTERNAL_TRACEBACK")
    monkeypatch.setattr(cli, "_execute", broken)
    assert cli.main(["audit", "--records", str(tmp_path / "file")]) == 4
    streams = capsys.readouterr()
    assert streams.out == "" and "PRIVATE_INTERNAL_TRACEBACK" not in streams.err and "Traceback" not in streams.err


def test_phase4_step7_module_invocation_executes_current_audit(tmp_path, subprocess_env):
    import subprocess
    import sys
    args, records, config = phase4_step7_inputs(tmp_path)
    output = tmp_path / "out"
    result = subprocess.run([sys.executable, "-m", "recursive_integrity_toolkit", "audit", *args, "--out", str(output)],
                            cwd=tmp_path, env=subprocess_env, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    report = json.loads((output / "report.json").read_bytes())
    assert report["derived_metrics"]["diversity"]["by_version"]["v1"]["gini_simpson_diversity"]["value"] == 0.625


def test_phase4_step7_toml_configuration_preserves_explicit_selection(tmp_path, capsys):
    args, records, config = phase4_step7_inputs(tmp_path)
    toml = tmp_path / "config.toml"
    toml.write_text('[representation]\nname = "topic"\nsource = "topic_field"\nfield = "topic"\nversion = "1"\nmissing_value_policy = "exclude"\n')
    code, report, streams = phase4_step7_invoke(["--records", str(records), "--config", str(toml)], tmp_path / "out", capsys)
    assert code == 0 and report["derived_metrics"]["support"]["by_version"]["v1"]["support_size"]["value"] == 3


def test_phase4_step7_published_view_is_the_only_report_diagnostic_source(tmp_path, capsys, monkeypatch):
    from recursive_integrity_toolkit.reports import assembly
    from recursive_integrity_toolkit import cli
    args, records, config = phase4_step7_inputs(tmp_path)
    def broken(*args, **kwargs):
        raise RuntimeError("PRIVATE_ASSEMBLY_EXCEPTION")
    monkeypatch.setattr(assembly, "assemble_report", broken)
    code, report, streams = phase4_step7_invoke(args + ["--redacted"], tmp_path / "out", capsys)
    assert code == 4 and report["run"]["run_status"] == "failed"
    assert report["observed_facts"] == report["derived_metrics"] == {} and report["errors"]
    assert "PRIVATE_ASSEMBLY_EXCEPTION" not in streams.err + json.dumps(report)



def phase4_step8_pair_inputs(directory):
    """Independent counts: A,B,C,D -> A,A,B,E; delta -1, retention 1/2."""
    args, later, config = phase4_step7_inputs(directory)
    rows = [{"dataset_version": "later", "record_id": "l" + str(i), "content": "PRIVATE_CONTENT", "topic": t}
            for i, t in enumerate(("A", "A", "B", "E"))]
    later.write_text("\n".join(json.dumps(row) for row in rows), encoding="utf-8")
    earlier = directory / "earlier.jsonl"
    earlier.write_text("\n".join(json.dumps({"dataset_version": "earlier", "record_id": "e" + str(i),
        "content": "PRIVATE_CONTENT", "topic": t}) for i, t in enumerate(("A", "B", "C", "D"))), encoding="utf-8")
    order = directory / "order.json"
    order.write_text(json.dumps({"version_order": ["earlier", "later"]}), encoding="utf-8")
    return args + ["--compare", str(earlier), "--version-order", str(order), "--state-semantics", "literal categories"], later, earlier, config, order


def test_phase4_step8_explicit_pair_uses_hand_counts_and_keeps_scopes(tmp_path, capsys):
    args, later, earlier, config, order = phase4_step8_pair_inputs(tmp_path)
    before = {p: p.read_bytes() for p in tmp_path.iterdir()}
    code, report, streams = phase4_step7_invoke(args, tmp_path / "out", capsys)
    assert code == 0 and report["run"]["run_status"] == "complete"
    support = report["derived_metrics"]["support"]
    assert support["by_version"]["earlier"]["support_size"]["value"] == 4
    assert support["by_version"]["later"]["support_size"]["value"] == 3
    assert support["support_delta"]["value"] == -1
    assert support["support_retention_ratio"]["value"] == 0.5
    assert support["extinct_states"]["value"] == ["C", "D"]
    assert support["added_states"]["value"] == ["E"]
    assert support["support_loss_count"]["value"] == 2
    assert support["support_added_count"]["value"] == 1
    assert report["derived_metrics"]["diversity"]["gini_simpson_diversity_delta"]["value"] == -0.125
    assert support["comparison_details"]["value"]["compatibility_method"] == "identical_declared_basis"
    assert support["support_delta"]["scope"]["dataset_versions"] == ["earlier", "later"]
    assert report["derived_metrics"]["closure_exposure"]["direct"]["lower_bound"]["scope"]["dataset_versions"] == ["later"]
    assert report["capabilities"]["dataset_longitudinal"]["execution_status"] == "partial"
    assert report["capabilities"]["dataset_longitudinal"]["execution_scope"] == ["supplied_explicit_pair_support_and_diversity"]
    assert report["simulations"] == {} and "tail" not in report["derived_metrics"]
    assert all(p.read_bytes() == raw for p, raw in before.items())


@pytest.mark.parametrize("case", ["missing_order", "reverse", "omitted_version", "conflicting_sources", "same_version", "earlier_multiversion", "later_multiversion", "missing_representation", "earlier_missing_state"])
def test_phase4_step8_pair_failure_retains_independent_evidence(tmp_path, capsys, case):
    args, later, earlier, config, order = phase4_step8_pair_inputs(tmp_path)
    if case == "missing_order":
        i = args.index("--version-order"); del args[i:i+2]
    elif case == "reverse":
        order.write_text(json.dumps({"version_order": ["later", "earlier"]}))
    elif case == "omitted_version":
        order.write_text(json.dumps({"version_order": ["earlier"]}))
    elif case == "conflicting_sources":
        order.write_text(json.dumps({"version_order": ["earlier", "later"], "version_rank": {"earlier": 1, "later": 0}}))
    elif case == "same_version":
        earlier.write_text(earlier.read_text().replace('"earlier"', '"later"'))
    elif case in ("earlier_multiversion", "later_multiversion"):
        path = earlier if case.startswith("earlier") else later
        rows = [json.loads(line) for line in path.read_text().splitlines()]
        rows[-1]["dataset_version"] = "third"
        path.write_text("\n".join(json.dumps(row) for row in rows))
        order.write_text(json.dumps({"version_order": ["earlier", "later", "third"]}))
    elif case == "missing_representation":
        config.write_text("{}")
    else:
        raw = json.loads(config.read_text()); raw["representation"]["missing_value_policy"] = "error"
        config.write_text(json.dumps(raw))
        rows = [json.loads(line) for line in earlier.read_text().splitlines()]; rows[0]["topic"] = None
        earlier.write_text("\n".join(json.dumps(row) for row in rows))
    code, report, streams = phase4_step7_invoke(args, tmp_path / "out", capsys)
    assert code == 1 and report["run"]["run_status"] == "partial"
    assert report["observed_facts"]["record_counts"] and report["errors"]
    assert "support_delta" not in report["derived_metrics"].get("support", {})
    assert report["capabilities"]["dataset_longitudinal"]["execution_status"] == "failed"
    if case not in ("later_multiversion", "missing_representation"):
        assert report["derived_metrics"]["support"]["by_version"]["later"]["support_size"]["value"] == 3
    if case == "later_multiversion":
        assert set(report["derived_metrics"]["support"]["by_version"]) == {"earlier"}
    assert "PRIVATE_CONTENT" not in json.dumps(report) + streams.out + streams.err


@pytest.mark.parametrize("case", ["absent_meaning", "blank_meaning", "duplicate_meaning", "mapping", "compatibility", "validate_meaning"])
def test_phase4_step8_semantic_declarations_cannot_be_inferred_or_overridden(tmp_path, capsys, case):
    args, later, earlier, config, order = phase4_step8_pair_inputs(tmp_path)
    if case == "absent_meaning":
        i = args.index("--state-semantics"); del args[i:i+2]
    elif case == "blank_meaning":
        args[-1] = "   "
    elif case == "duplicate_meaning":
        args += ["--state-semantics", "different meaning"]
    elif case in ("mapping", "compatibility"):
        raw = json.loads(config.read_text())
        raw["state_mapping" if case == "mapping" else "representation_compatibility"] = {"earlier": "meaning one", "later": "meaning two"}
        config.write_text(json.dumps(raw))
    code, report, streams = phase4_step7_invoke(args, tmp_path / "out", capsys,
        command="validate" if case == "validate_meaning" else "audit")
    assert code == 2
    if report is not None:
        assert report["run"]["run_status"] == "failed"
        assert report["derived_metrics"] == {} and report["errors"]


def test_phase4_step8_validate_two_inputs_never_dispatches_pair(tmp_path, capsys, monkeypatch):
    from recursive_integrity_toolkit import cli
    from recursive_integrity_toolkit.metrics import diversity
    args, later, earlier, config, order = phase4_step8_pair_inputs(tmp_path)
    i = args.index("--state-semantics"); del args[i:i+2]
    called = []
    def denied(*args, **kwargs):
        called.append(True)
        raise AssertionError("unexpected calculation")
    monkeypatch.setattr(cli, "_calculations", denied)
    monkeypatch.setattr(cli, "_pair_calculations", denied)
    monkeypatch.setattr(diversity, "compare_support", denied)
    code, report, streams = phase4_step7_invoke(args, tmp_path / "out", capsys, command="validate")
    assert code == 0 and called == []
    assert report["derived_metrics"] == report["proxy_signals"] == report["simulations"] == {}
    assert set(report["observed_facts"]["record_counts"]) == {"earlier", "later"}


def test_phase4_step8_comparison_internal_failure_preserves_both_distributions(tmp_path, capsys, monkeypatch):
    from recursive_integrity_toolkit.metrics import diversity
    args, later, earlier, config, order = phase4_step8_pair_inputs(tmp_path)
    def broken(*args, **kwargs):
        raise RuntimeError("PRIVATE_EXCEPTION")
    monkeypatch.setattr(diversity, "compare_support", broken)
    code, report, streams = phase4_step7_invoke(args, tmp_path / "out", capsys)
    assert code == 4 and report["run"]["run_status"] == "partial"
    assert set(report["derived_metrics"]["support"]["by_version"]) == {"earlier", "later"}
    assert "PRIVATE_EXCEPTION" not in json.dumps(report) + streams.err


@pytest.mark.parametrize("mode", ["hash", "omit", "preserve"])
def test_phase4_step8_pair_redaction_preserves_numbers_and_hides_semantics(tmp_path, capsys, mode):
    args, later, earlier, config, order = phase4_step8_pair_inputs(tmp_path)
    args[-1] = "PRIVATE_MEANING"
    for p in (earlier, later, order):
        p.write_text(p.read_text().replace('"earlier"', '"PRIVATE_EARLIER"').replace('"later"', '"PRIVATE_LATER"').replace('"C"', '"PRIVATE_STATE"'))
    code, report, streams = phase4_step7_invoke(args + ["--redacted", "--record-ids", mode], tmp_path / "out", capsys)
    assert code == 0
    support = report["derived_metrics"]["support"]
    assert support["support_delta"]["value"] == -1 and support["support_retention_ratio"]["value"] == 0.5
    emitted = json.dumps(report) + streams.out + streams.err + (tmp_path / "out/report.md").read_text()
    assert "PRIVATE_" not in emitted and str(tmp_path) not in emitted


def test_phase4_step8_pair_does_not_activate_other_calculation_families(tmp_path, capsys, monkeypatch):
    import importlib
    import inspect
    import socket
    import urllib.request
    from recursive_integrity_toolkit.io import loaders
    args, later, earlier, config, order = phase4_step8_pair_inputs(tmp_path)
    calls = []
    def denied(*args, **kwargs):
        calls.append(True)
        raise AssertionError("unopened operation")
    for name in ("metrics.resampling", "lineage.graph", "lineage.ancestry", "lineage.cycles"):
        module = importlib.import_module("recursive_integrity_toolkit." + name)
        for key, value in vars(module).copy().items():
            if inspect.isfunction(value): monkeypatch.setattr(module, key, denied)
    for owner, name in ((socket, "socket"), (socket, "getaddrinfo"), (urllib.request, "urlopen"), (loaders, "load_content_reference")):
        monkeypatch.setattr(owner, name, denied)
    code, report, streams = phase4_step7_invoke(args, tmp_path / "out", capsys)
    assert code == 0 and not calls and report["simulations"] == {}


def test_phase4_step8_tail_stays_in_later_scope(tmp_path, capsys):
    args, later, earlier, config, order = phase4_step8_pair_inputs(tmp_path)
    code, report, streams = phase4_step7_invoke(args + ["--tail-rule", "singleton_count"], tmp_path / "out", capsys)
    assert code == 0
    tail = report["derived_metrics"]["tail"]["tail_support_size"]
    assert tail["value"] == 2 and tail["scope"]["dataset_versions"] == ["later"]


def test_phase4_step8_config_declared_compare_uses_config_parent(tmp_path, capsys):
    from recursive_integrity_toolkit.cli import main
    args, later, earlier, config, order = phase4_step8_pair_inputs(tmp_path)
    data = json.loads(config.read_text()); data["inputs"] = {"records_compare": earlier.name}
    data["version_order"] = ["earlier", "later"]
    config.write_text(json.dumps(data))
    assert main(["audit", "--records", str(later), "--config", str(config), "--state-semantics", "literal categories", "--out", str(tmp_path / "out")]) == 0
    capsys.readouterr()
    report = json.loads((tmp_path / "out/report.json").read_bytes())
    assert report["derived_metrics"]["support"]["support_delta"]["value"] == -1


def test_phase4_step8_same_version_pair_retains_only_primary_metrics(tmp_path, capsys):
    args, later, earlier, config, order = phase4_step8_pair_inputs(tmp_path)
    earlier.write_text(earlier.read_text().replace('"earlier"', '"later"'))
    order.write_text(json.dumps({"version_order": ["later"]}))
    provenance = tmp_path / "provenance.jsonl"
    provenance.write_text("\n".join(json.dumps({"dataset_version": "later", "record_id": prefix + str(i),
        "source_type": source, "external_grounding": grounding, "provenance_confidence": "confirmed"})
        for prefix, source, grounding in (("e", "synthetic", "no"), ("l", "human", "yes")) for i in range(4)))
    code, report, streams = phase4_step7_invoke(args + ["--provenance", str(provenance)], tmp_path / "out", capsys)
    assert code == 1 and report["run"]["run_status"] == "partial"
    support = report["derived_metrics"]["support"]
    assert set(support["by_version"]) == {"later"} and "support_delta" not in support
    assert support["by_version"]["later"]["support_size"]["value"] == 3
    assert support["by_version"]["later"]["support_size"]["scope"]["record_count"] == 4
    assert report["derived_metrics"]["diversity"]["by_version"]["later"]["gini_simpson_diversity"]["value"] == 0.625
    # The accepted provenance contract covers complete versions. Its observed
    # bundle coverage stays truthful; no pooled composition is mislabeled as
    # primary-only evidence when both roles assert the same version identity.
    coverage = report["observed_facts"]["provenance"]["provenance_row_coverage"]
    assert coverage["value"] == 1 and coverage["scope"]["record_count"] == 8
    assert "provenance" not in report["derived_metrics"]
    assert "closure_exposure" not in report["derived_metrics"]
    assert report["capabilities"]["dataset_longitudinal"]["execution_status"] == "failed"
    assert "E_VERSION_ORDER_CONFLICT" in {error["code"] for error in report["errors"]}
    assert any(error["code"] == "E_SCHEMA_TYPE" and error["effect_on_capabilities"] == ["provenance"]
               for error in report["errors"])
    assert "E_INTERNAL" not in {error["code"] for error in report["errors"]}


@pytest.mark.parametrize("redacted", [False, True])
def test_phase4_step8_rejected_order_retains_exact_input_hash(tmp_path, capsys, redacted):
    import hashlib
    args, later, earlier, config, order = phase4_step8_pair_inputs(tmp_path)
    original = b'{"version_order": ["earlier"]}\n'
    order.write_bytes(original)
    code, report, streams = phase4_step7_invoke(args + (["--redacted"] if redacted else []), tmp_path / "out", capsys)
    assert code == 1 and report["run"]["run_status"] == "partial"
    artifacts = report["inputs"]["artifacts"]
    indexed = [(i, entry) for i, entry in enumerate(artifacts) if entry["role"] == "version_order"]
    assert len(indexed) == 1
    index, artifact = indexed[0]
    expected_hash = hashlib.sha256(original).hexdigest()
    assert artifact["file_hash"] == expected_hash and artifact["size_bytes"] == len(original)
    assert {"artifact_index": index, "algorithm": "sha256", "value": expected_hash} in report["inputs"]["file_hashes"]
    assert "support_delta" not in report["derived_metrics"]["support"]
    assert order.read_bytes() == original
    if redacted:
        assert str(tmp_path) not in json.dumps(report) + streams.out + streams.err


def test_phase4_step8_changed_rejected_order_never_claims_a_stale_hash(tmp_path, capsys, monkeypatch):
    from recursive_integrity_toolkit.errors import ErrorCode, ToolkitError
    from recursive_integrity_toolkit.io import validation
    args, later, earlier, config, order = phase4_step8_pair_inputs(tmp_path)
    order.write_text(json.dumps({"version_order": ["earlier"]}))
    original = validation.validate_bundle
    calls = []
    def replaced_during_validation(*args, **kwargs):
        calls.append(True)
        try:
            return original(*args, **kwargs)
        except ToolkitError as error:
            assert error.code is ErrorCode.VERSION_ORDER_CONFLICT
            order.write_text(json.dumps({"version_order": ["earlier", "later"], "PRIVATE_CHANGED_INPUT": True}))
            raise
    monkeypatch.setattr(validation, "validate_bundle", replaced_during_validation)
    code, report, streams = phase4_step7_invoke(args, tmp_path / "out", capsys)
    assert code == 1 and calls == [True]
    assert report["run"]["run_status"] == "failed"
    assert report["inputs"] == report["derived_metrics"] == {}
    assert report["errors"][0]["code"] == "E_FILE_PARSE"
    assert "PRIVATE_CHANGED_INPUT" not in json.dumps(report) + streams.out + streams.err


def phase4_step9_block_network(monkeypatch):
    import socket
    import urllib.request

    attempts = []
    def blocked(*args, **kwargs):
        attempts.append(True)
        raise AssertionError("Step 9 intercepted an outbound operation")
    for owner, name in ((socket, "socket"), (socket, "create_connection"),
                        (socket, "getaddrinfo"), (socket, "gethostbyname"),
                        (urllib.request, "urlopen"), (urllib.request.OpenerDirector, "open")):
        monkeypatch.setattr(owner, name, blocked)
    return attempts


@pytest.mark.parametrize("redacted", [False, True])
@pytest.mark.parametrize("case,expected_exit", [
    ("complete", 0), ("malformed_input", 1), ("malformed_config", 2),
    ("duplicate_identity", 1), ("family_internal", 4), ("publication_io", 1),
])
def test_phase4_step9_offline_privacy_covers_every_cli_sink_on_failure(
        tmp_path, capsys, caplog, monkeypatch, redacted, case, expected_exit):
    from recursive_integrity_toolkit.metrics import bounds
    from recursive_integrity_toolkit.utils import paths

    args, records, config = phase4_step7_inputs(tmp_path, provenance=True)
    rows = [json.loads(line) for line in records.read_text().splitlines()]
    for row in rows:
        row["content"] = "CONTENT_NEVER_PUBLISH_583"
        row["notes"] = "NOTES_NEVER_PUBLISH_583"
    records.write_text("\n".join(json.dumps(row) for row in rows), encoding="utf-8")
    manifest = tmp_path / "provenance.jsonl"
    rows = [json.loads(line) for line in manifest.read_text().splitlines()]
    for row in rows:
        row["source_uri"] = "https://invalid.example/REMOTE_METADATA_NEVER_PUBLISH_583"
        row["notes"] = "NOTES_NEVER_PUBLISH_583"
    manifest.write_text("\n".join(json.dumps(row) for row in rows), encoding="utf-8")
    salt = tmp_path / "SALT_PATH_NEVER_PUBLISH_583"
    salt.write_bytes(b"SECRET_NEVER_PUBLISH_583_0123456789")
    if redacted:
        args += ["--redacted", "--id-salt-file", str(salt)]
    if case == "malformed_input":
        records.write_bytes(b'{"CONTENT_NEVER_PUBLISH_583":')
    elif case == "malformed_config":
        config.write_bytes(b'{"NOTES_NEVER_PUBLISH_583":')
    elif case == "duplicate_identity":
        records.write_bytes(records.read_bytes() + b"\n" + records.read_bytes().splitlines()[0])
    elif case == "family_internal":
        def broken(*args, **kwargs):
            raise RuntimeError({"nested": ["EXCEPTION_NEVER_PUBLISH_583"]})
        monkeypatch.setattr(bounds, "direct_closure_exposure", broken)
    before = {path: path.read_bytes() for path in (records, config, manifest, salt)}
    staged = []
    original_write = paths._output_write
    def inspect_write(path, payload, owned):
        staged.append((path.name, payload.decode("utf-8")))
        original_write(path, payload, owned)
        if case == "publication_io" and path.name == "report.md":
            raise OSError("EXCEPTION_NEVER_PUBLISH_583")
    monkeypatch.setattr(paths, "_output_write", inspect_write)
    attempts = phase4_step9_block_network(monkeypatch)
    output = tmp_path / "PRIVATE_OUTPUT_583"
    code, report, streams = phase4_step7_invoke(args, output, capsys)
    assert code == expected_exit and attempts == []
    assert all(path.read_bytes() == raw for path, raw in before.items())
    retained = [path for path in tmp_path.rglob("*") if path.is_file() and path not in before]
    sinks = streams.out + streams.err + caplog.text
    sinks += "".join(text for _, text in staged)
    sinks += "".join(path.read_text(encoding="utf-8") for path in retained)
    for secret in ("CONTENT_NEVER_PUBLISH_583", "NOTES_NEVER_PUBLISH_583",
                   "REMOTE_METADATA_NEVER_PUBLISH_583", "SECRET_NEVER_PUBLISH_583",
                   "EXCEPTION_NEVER_PUBLISH_583", "SALT_PATH_NEVER_PUBLISH_583"):
        assert secret not in sinks
    assert "Traceback" not in sinks
    assert not any(path.name.startswith(".rit-stage-") for path in tmp_path.rglob("*"))
    if redacted:
        assert str(tmp_path) not in sinks and "PRIVATE_OUTPUT_583" not in sinks
    if case == "publication_io":
        assert report is None and retained == [] and streams.out == ""
        assert [name for name, _ in staged] == ["report.json", "report.md"]
        assert "E_OUTPUT_IO" in streams.err
    else:
        assert {path.name for path in retained} == {"report.json", "report.md"}
        assert report["run"]["network_call_count"] == 0
        if case == "complete":
            assert report["run"]["run_status"] == "complete" and report["errors"] == []
        elif case == "family_internal":
            assert report["run"]["run_status"] == "partial"
            values = report["derived_metrics"]["support"]["by_version"].values()
            assert [item["support_size"]["value"] for item in values] == [3]
            # P4-D04 protects unregistered diagnostic identifiers in both modes.
            assert len(report["errors"]) == 1
            assert report["errors"][0]["code"].startswith("hmac-sha256:")
            assert report["errors"][0]["severity"] == "error"
            assert report["errors"][0]["effect_on_capabilities"] == ["provenance"]
        else:
            expected = {"malformed_input": "E_FILE_PARSE", "malformed_config": "E_CONFIG_INVALID",
                        "duplicate_identity": "E_RECORD_DUPLICATE_ID"}[case]
            assert expected in {item["code"] for item in report["errors"]}
            assert report["run"]["run_status"] == "failed"
        diagnostics = [json.loads(line) for line in streams.err.splitlines()]
        assert diagnostics == report["warnings"] + report["errors"]


@pytest.mark.parametrize("redacted", [False, True])
@pytest.mark.parametrize("label", [
    "<script>FORGED_583</script>|`[x](javascript:alert(1))",
    "state\n## FORGED_583\n| field | invented |\x1b[31m",
    "café 状态\u202eFORGED_583\u2066x\u2069\u2028end",
])
def test_phase4_step9_hostile_state_labels_stay_inert_through_cli(
        tmp_path, capsys, monkeypatch, redacted, label):
    import re
    import unicodedata

    args, records, config = phase4_step7_inputs(tmp_path)
    rows = [json.loads(line) for line in records.read_text().splitlines()]
    for row in rows[:2]:
        row["topic"] = label
    records.write_text("\n".join(json.dumps(row) for row in rows), encoding="utf-8")
    before = records.read_bytes()
    attempts = phase4_step9_block_network(monkeypatch)
    output = tmp_path / "out"
    code, report, streams = phase4_step7_invoke(args + (["--redacted"] if redacted else []), output, capsys)
    assert code == 0 and attempts == [] and records.read_bytes() == before
    version = next(iter(report["derived_metrics"]["support"]["by_version"]))
    assert report["derived_metrics"]["support"]["by_version"][version]["support_size"]["value"] == 3
    assert report["derived_metrics"]["diversity"]["by_version"][version]["gini_simpson_diversity"]["value"] == 0.625
    markdown = (output / "report.md").read_text(encoding="utf-8")
    assert len([line for line in markdown.splitlines() if line.startswith("## ")]) == 12
    assert "<script>" not in markdown and not re.search(r"^#{1,6} FORGED_583", markdown, re.MULTILINE)
    outside_code = re.sub(r"`[^`\n]*`", "", markdown)
    assert "javascript:" not in outside_code
    assert all(character == "\n" or unicodedata.category(character) not in
               {"Cc", "Cf", "Cs", "Zl", "Zp"} for character in markdown)
    if redacted:
        assert "FORGED_583" not in json.dumps(report) + markdown + streams.out + streams.err
    else:
        def strings(node):
            if isinstance(node, str):
                yield node
            elif isinstance(node, dict):
                for key, value in node.items():
                    yield key
                    yield from strings(value)
            elif isinstance(node, list):
                for value in node:
                    yield from strings(value)
        assert label in set(strings(report))
        literals = []
        for span in re.findall(r"`([^`\n]*)`", markdown):
            try:
                literals.extend(strings(json.loads(span)))
            except json.JSONDecodeError:
                pass
        assert label in literals


@pytest.mark.parametrize("mode", ["standard", "hash", "omit"])
def test_phase4_step10_warning_scope_summary_preserves_diagnostics_and_privacy(tmp_path, capsys, mode):
    """Missing-row warnings retain each location and each distinct capability effect."""
    args, records, config = phase4_step7_inputs(tmp_path, provenance=True)
    version = "PRIVATE_VERSION_STEP10"
    rows = [json.loads(line) for line in records.read_text().splitlines()]
    for index, row in enumerate(rows):
        row.update(dataset_version=version, record_id=f"PRIVATE_RECORD_STEP10_{index}")
    records.write_text("\n".join(json.dumps(row) for row in rows), encoding="utf-8")
    provenance = tmp_path / "provenance.jsonl"
    entries = [json.loads(line) for line in provenance.read_text().splitlines()][:2]
    for index, row in enumerate(entries):
        row.update(dataset_version=version, record_id=f"PRIVATE_RECORD_STEP10_{index}")
    entries[1]["external_grounding"] = "unknown"
    provenance.write_text("\n".join(json.dumps(row) for row in entries), encoding="utf-8")
    extra = [] if mode == "standard" else ["--redacted", "--record-ids", mode]
    output = tmp_path / "out"
    code, report, streams = phase4_step7_invoke(args + extra, output, capsys)
    assert code == 0 and report["run"]["run_status"] == "complete" and report["errors"] == []
    expected = [
        ("W_PROVENANCE_MISSING_ROW", None, ["ingestion"]),
        ("W_PROVENANCE_MISSING_ROW", None, ["ingestion"]),
        ("W_GROUNDING_UNKNOWN", 2, ["provenance"]),
        ("W_PROVENANCE_MISSING_ROW", 3, ["ingestion"]),
        ("W_PROVENANCE_MISSING_ROW", 4, ["ingestion"]),
        ("W_PROVENANCE_MISSING_ROW", 3, ["provenance"]),
        ("W_PROVENANCE_MISSING_ROW", 4, ["provenance"]),
    ]
    assert [(item["code"], item["representative_locations"][0]["row_number"],
             item["effect_on_capabilities"]) for item in report["warnings"]] == expected
    scope = report["inputs"]["scope"]
    summary = {key: scope[key] for key in ("dataset_versions", "record_count", "excluded_record_count",
                                          "denominator_basis", "scope_id")}
    for item in report["warnings"]:
        assert item["count"] == 1 and item["severity"] == "warning"
        assert item["affected_scope"] == summary
        assert len(item["representative_locations"]) == 1
    facts = report["observed_facts"]["provenance"]
    assert facts["source_type_counts"]["value"] == dict(human=1, synthetic=1, mixed=0, sensor=0, unknown=0)
    assert facts["missing_provenance_count"]["value"] == 2
    assert [facts[name]["value"] for name in ("known_open_count", "known_closed_count", "unresolved_grounding_count")] == [1, 0, 3]
    direct = report["derived_metrics"]["closure_exposure"]["direct"]
    assert [direct[name]["value"] for name in ("lower_bound", "upper_bound", "interval_width")] == [0, .75, .75]
    assert all(direct[name]["denominator"] == 4 for name in ("lower_bound", "upper_bound", "interval_width"))
    assert [json.loads(line) for line in streams.err.splitlines()] == report["warnings"]
    markdown = (output / "report.md").read_text(encoding="utf-8")
    for warning_code in ("W_PROVENANCE_MISSING_ROW", "W_GROUNDING_UNKNOWN"):
        assert warning_code in markdown
    locations = [item["representative_locations"][0] for item in report["warnings"]]
    assert [location["file_role"] for location in locations] == [None, None, "provenance_manifest",
                                                               "records_primary", "records_primary", "records_primary", "records_primary"]
    assert [location["field"] for location in locations] == [None, None, "external_grounding", None, None, None, None]
    assert all(location["line_number"] is None for location in locations)
    if mode == "omit":
        assert "included_record_keys" not in scope
        assert all(location["record_key"] is None for location in locations)
    else:
        keys = scope["included_record_keys"]
        assert len(keys) == 4 and len({(key["dataset_version"], key["record_id"]) for key in keys}) == 4
        assert [location["record_key"] for location in locations] == [keys[index] for index in (2, 3, 1, 2, 3, 2, 3)]
        if mode == "standard":
            assert keys == [{"dataset_version": version, "record_id": row["record_id"]} for row in rows]
        else:
            assert all(key["record_id"].startswith("hmac-sha256:") for key in keys)
    emitted = json.dumps(report) + streams.out + streams.err + markdown
    assert "PRIVATE_CONTENT_" not in emitted
    if mode != "standard":
        assert "PRIVATE_VERSION_STEP10" not in emitted and "PRIVATE_RECORD_STEP10_" not in emitted
        assert str(tmp_path) not in emitted


def test_phase4_step10_diagnostic_deduplication_keeps_equality_order_and_context():
    """Repeated adapter passes coalesce exact duplicates without merging contexts."""
    from copy import deepcopy
    from dataclasses import replace
    from recursive_integrity_toolkit.models import FileRole, RecordKey, ValidationMessage, ValidationSeverity
    from recursive_integrity_toolkit.reports.assembly import _diagnostics, _diagnostic_equality_key

    scope = dict(dataset_versions=["v"], record_count=2, excluded_record_count=0,
                 denominator_basis="all_validated_bundle_records", scope_id="validated_bundle",
                 included_record_keys=[dict(dataset_version="v", record_id=key) for key in ("a", "b")],
                 excluded_record_keys=[])
    payload = {"inputs": {"scope": scope, "limitations": []}, "warnings": [], "errors": []}
    first = ValidationMessage("W_PROVENANCE_MISSING_ROW", ValidationSeverity.WARNING,
        "record has no matching provenance row", file_role=FileRole.RECORDS_PRIMARY,
        record_key=RecordKey("v", "a"), row_number=1, line_number=1)
    second = replace(first, record_key=RecordKey("v", "b"), row_number=2, line_number=2)
    error = replace(first, code="E_SCHEMA_REQUIRED_FIELD", severity=ValidationSeverity.ERROR)
    _diagnostics(payload, (first, second, first, error, error))
    original = deepcopy(payload)
    payload["warnings"][0] = dict(reversed(tuple(payload["warnings"][0].items())))
    _diagnostics(payload, (second, first, error))
    assert payload == original and payload["inputs"]["scope"] == scope
    _diagnostics(payload, (first, first, error, error), family="provenance")
    assert [warning["representative_locations"][0]["record_key"]["record_id"] for warning in payload["warnings"]] == ["a", "b", "a"]
    assert [warning["effect_on_capabilities"] for warning in payload["warnings"]] == [["ingestion"], ["ingestion"], ["provenance"]]
    assert [item["effect_on_capabilities"] for item in payload["errors"]] == [["ingestion"], ["provenance"]]
    assert all(item["count"] == 1 for item in payload["warnings"])
    # Preserve prior Python equality while canonical validation owns field types.
    for left, right in (({"x": [1, None, True], "y": 2}, {"y": 2.0, "x": [1.0, None, 1]}),
                        ({"x": [1, 2]}, {"x": [2, 1]}), ({"x": None}, {"x": False}),
                        ({"x": []}, {"x": {}}), ({"x": "1"}, {"x": 1})):
        assert (_diagnostic_equality_key(left) == _diagnostic_equality_key(right)) == (left == right)
