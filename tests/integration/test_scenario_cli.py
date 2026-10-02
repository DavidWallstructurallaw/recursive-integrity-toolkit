"""Explicit scenario commands retain independent evidence and input-only validation."""
from __future__ import annotations

import json
import subprocess
import sys

import pytest


CLOSED = "closed_resampling"
REOPENED = "reopened_resampling"
PRIVATE_STATE = "PRIVATE_SCENARIO_STATE"
PRIVATE_OTHER = "PRIVATE_SCENARIO_OTHER"
PRIVATE_SCOPE = "PRIVATE_SCENARIO_SCOPE"
PRIVATE_VERSION = "PRIVATE_SCENARIO_VERSION"
PRIVATE_MEANING = "PRIVATE_SCENARIO_MEANING"


def declaration(*, models=(CLOSED, REOPENED), enabled=True):
    result = {
        "seed": 29, "models": list(models),
        "state_distribution": {PRIVATE_STATE: .75, PRIVATE_OTHER: .25},
        "resample_size": 7, "simulation_horizon": 3, "simulation_replicates": 2,
        "representation": {
            "representation_name": "explicit_scenario_categories",
            "representation_source": "topic_field", "representation_version": "scenario-v1",
            "binning_or_mapping_rule": "literal_field_value", "field_name": "topic",
            "missing_value_policy": "exclude", "missing_state_id": None,
            "normalization_profile": None,
        },
        "state_semantics": PRIVATE_MEANING, "scope_id": PRIVATE_SCOPE,
        "dataset_version": PRIVATE_VERSION,
    }
    if enabled is not None:
        result["enabled"] = enabled
    if REOPENED in models:
        result["external_input_distribution"] = {PRIVATE_STATE: .25, PRIVATE_OTHER: .75}
        result["reopening_weight"] = .5
    return result


def inputs(directory, simulation):
    records = directory / "records.jsonl"
    rows = [{"dataset_version": "audit-v1", "record_id": f"r{index}",
             "content": f"PRIVATE_CONTENT_{index}", "topic": state}
            for index, state in enumerate(("A", "A", "B", "C"))]
    records.write_text("\n".join(map(json.dumps, rows)), encoding="utf-8")
    provenance = directory / "provenance.jsonl"
    provenance.write_text("\n".join(json.dumps({"dataset_version": "audit-v1", "record_id": f"r{index}",
        "source_type": "human", "provenance_confidence": "confirmed", "external_grounding": "yes"})
        for index in range(4)), encoding="utf-8")
    config = directory / "config.json"
    config.write_text(json.dumps({
        "representation": {"name": "topic", "source": "topic_field", "field": "topic",
                           "version": "1", "missing_value_policy": "exclude"},
        "simulation": simulation,
    }), encoding="utf-8")
    return ["--records", str(records), "--provenance", str(provenance), "--config", str(config)], config


def invoke(args, output, capsys, *, command="audit"):
    from recursive_integrity_toolkit.cli import main
    from recursive_integrity_toolkit.result import validate_report
    code = main([command, *args, "--out", str(output)])
    streams = capsys.readouterr()
    path = output / "report.json"
    report = json.loads(path.read_bytes()) if path.exists() else None
    if report is not None:
        validate_report(report)
        assert (output / "report.md").is_file()
    return code, report, streams


def independent_evidence(report):
    assert report["observed_facts"]["record_counts"]["audit-v1"]["value"] == 4
    assert report["derived_metrics"]["support"]["by_version"]["audit-v1"]["support_size"]["value"] == 3
    assert report["derived_metrics"]["diversity"]["by_version"]["audit-v1"]["gini_simpson_diversity"]["value"] == .625
    assert report["derived_metrics"]["closure_exposure"]["direct"]["lower_bound"]["value"] == 0
    assert report["capabilities"]["content_diagnostics"]["execution_status"] == "completed"


@pytest.mark.parametrize("models,enabled,flags", [
    ((CLOSED,), None, ["--simulate"]),
    ((REOPENED,), True, []),
    ((CLOSED, REOPENED), True, []),
    ((REOPENED, CLOSED), True, ["--simulate"]),
])
def test_explicit_scenario_activation_uses_only_declared_scope_and_models(tmp_path, capsys, models, enabled, flags):
    args, config = inputs(tmp_path, declaration(models=models, enabled=enabled))
    original = config.read_bytes()
    code, report, streams = invoke(args + flags, tmp_path / "out", capsys)
    assert code == 0 and report["run"]["run_status"] == "complete"
    assert report["run"]["random_seed"] == 29
    assert "PRIVATE_" not in json.dumps(report["run"]["resolved_options"])
    independent_evidence(report)
    expected = {CLOSED if model == CLOSED else "external_reopening" for model in models}
    assert set(report["simulations"]) == expected
    for node in report["simulations"].values():
        assert node["status"] == "experimental" and node["evidence_class"] == "simulation"
        assert node["state_semantics"] == PRIVATE_MEANING
        assert node["parameters"]["random_seed"] == report["run"]["random_seed"]
        assert node["parameters"]["resample_size"] == 7
        assert {row["state_id"]: row["probability"] for row in node["initial_distribution"]} == {
            PRIVATE_STATE: .75, PRIVATE_OTHER: .25}
        assert node["representation"]["representation_name"] == "explicit_scenario_categories"
        scope = node["scope"]
        assert scope["scope_id"] == PRIVATE_SCOPE and scope["dataset_versions"] == [PRIVATE_VERSION]
        assert scope["denominator_basis"] == "explicit_scenario_probability_vector"
        assert scope["included_record_keys"] == scope["excluded_record_keys"] == []
        assert scope["record_count"] == scope["excluded_record_count"] == 0
    assert report["capabilities"]["intervention_simulation"]["execution_status"] == "completed"
    unavailable = [row for row in report["unavailable_conclusions"]
                   if row["conclusion"] == "empirical_intervention_effect"]
    assert len(unavailable) == 1 and unavailable[0]["status"] == "unavailable"
    assert "PRIVATE_CONTENT_" not in json.dumps(report) + streams.out + streams.err
    assert config.read_bytes() == original


def test_model_selection_order_does_not_change_cli_sampled_paths(tmp_path, capsys):
    args, config = inputs(tmp_path, declaration(models=(CLOSED, REOPENED)))
    first_code, first, _ = invoke(args, tmp_path / "first", capsys)
    raw = json.loads(config.read_bytes())
    raw["simulation"]["models"].reverse()
    config.write_text(json.dumps(raw), encoding="utf-8")
    second_code, second, _ = invoke(args, tmp_path / "second", capsys)
    assert first_code == second_code == 0
    for name in (CLOSED, "external_reopening"):
        assert first["simulations"][name]["sampled_paths"] == second["simulations"][name]["sampled_paths"]


@pytest.mark.parametrize("simulation", [declaration(enabled=False), declaration(enabled=None),
                                       {"enabled": False, "seed": 29}])
def test_disabled_scenarios_are_inert_during_audit(tmp_path, capsys, monkeypatch, simulation):
    from recursive_integrity_toolkit.metrics import resampling
    def denied(*_args, **_kwargs):
        pytest.fail("An inactive declaration executed a scenario")
    monkeypatch.setattr(resampling, "run_scenario_experiment", denied)
    args, _ = inputs(tmp_path, simulation)
    code, report, _ = invoke(args, tmp_path / "out", capsys)
    assert code == 0 and report["simulations"] == {}
    independent_evidence(report)
    assert report["capabilities"]["intervention_simulation"]["execution_status"] == "not_requested"


@pytest.mark.parametrize("enabled", [True, False])
def test_validate_scenario_declarations_never_import_sampler_or_numpy(tmp_path, subprocess_env, enabled):
    args, _ = inputs(tmp_path, declaration(enabled=enabled))
    output = tmp_path / "out"
    program = '''import importlib.abc,sys
attempts=[]
class Block(importlib.abc.MetaPathFinder):
 def find_spec(self,fullname,path=None,target=None):
  if fullname == 'numpy' or fullname.startswith(('numpy.','recursive_integrity_toolkit.metrics.resampling')):
   attempts.append(fullname)
   raise AssertionError('input-only validation imported a sampler dependency')
sys.meta_path.insert(0,Block())
from recursive_integrity_toolkit.cli import main
code=main(sys.argv[1:])
assert code == 0, code
assert attempts == [], attempts
assert 'recursive_integrity_toolkit.metrics.resampling' not in sys.modules
assert 'numpy' not in sys.modules
'''
    process = subprocess.run([sys.executable, "-c", program, "validate", *args, "--out", str(output)],
        cwd=tmp_path, env=subprocess_env, capture_output=True, text=True)
    assert process.returncode == 0, process.stderr
    from recursive_integrity_toolkit.result import validate_report
    report = json.loads((output / "report.json").read_bytes())
    validate_report(report)
    assert report["run"]["run_status"] == "complete"
    assert report["simulations"] == report["proxy_signals"] == {}
    assert report["derived_metrics"] == {"longitudinal": {"snapshots": [], "comparisons": []}}
    assert report["capabilities"]["intervention_simulation"]["execution_status"] != "completed"
    assert report["capabilities"]["intervention_simulation"]["status"] == ("experimental" if enabled else "unavailable")
    assert report["observed_facts"]["record_counts"]["audit-v1"]["value"] == 4


def test_numpy_unavailable_retains_independent_audit_evidence(tmp_path, subprocess_env):
    args, _ = inputs(tmp_path, declaration())
    output = tmp_path / "out"
    program = '''import importlib.abc,sys
attempts=[]
class Block(importlib.abc.MetaPathFinder):
 def find_spec(self,fullname,path=None,target=None):
  if fullname == 'numpy' or fullname.startswith('numpy.'):
   attempts.append(fullname)
   raise ModuleNotFoundError('PRIVATE_DEPENDENCY_EXCEPTION')
sys.meta_path.insert(0,Block())
from recursive_integrity_toolkit.cli import main
assert main(sys.argv[1:]) == 2
assert attempts
'''
    process = subprocess.run([sys.executable, "-c", program, "audit", *args, "--out", str(output)],
        cwd=tmp_path, env=subprocess_env, capture_output=True, text=True)
    assert process.returncode == 0, process.stderr
    from recursive_integrity_toolkit.result import validate_report
    report = json.loads((output / "report.json").read_bytes())
    validate_report(report)
    independent_evidence(report)
    assert report["simulations"] == {} and report["run"]["run_status"] == "partial"
    assert report["capabilities"]["intervention_simulation"]["execution_status"] == "failed"
    assert any(row["code"] == "E_CONFIG_INVALID" for row in report["errors"])
    assert "PRIVATE_DEPENDENCY_EXCEPTION" not in process.stdout + process.stderr + json.dumps(report)


def test_underflow_failure_keeps_independent_evidence_and_occurs_before_rng(tmp_path, capsys, monkeypatch):
    import numpy as np
    scenario = declaration(models=(REOPENED,))
    scenario["state_distribution"] = {"main": 1., "tiny": 5e-324}
    scenario["external_input_distribution"] = {"main": 1., "tiny": 0.}
    def denied(*_args, **_kwargs):
        pytest.fail("Numerically inadmissible scenario initialized an RNG")
    monkeypatch.setattr(np.random, "PCG64", denied)
    args, _ = inputs(tmp_path, scenario)
    code, report, _ = invoke(args, tmp_path / "out", capsys)
    assert code == 1 and report["run"]["run_status"] == "partial"
    independent_evidence(report)
    assert report["simulations"] == {}
    assert report["capabilities"]["intervention_simulation"]["execution_status"] == "failed"
    assert any(row["code"] == "E_SCHEMA_TYPE" for row in report["errors"])


@pytest.mark.parametrize("record_mode", ["hash", "omit"])
def test_redacted_scenario_cli_protects_configuration_text_and_all_output_sinks(tmp_path, capsys, record_mode):
    args, _ = inputs(tmp_path, declaration())
    output = tmp_path / "out"
    code, report, streams = invoke(args + ["--redacted", "--record-ids", record_mode], output, capsys)
    assert code == 0 and report["simulations"]
    emitted = json.dumps(report) + streams.out + streams.err + (output / "report.md").read_text(encoding="utf-8")
    for private in (PRIVATE_STATE, PRIVATE_OTHER, PRIVATE_SCOPE, PRIVATE_VERSION, PRIVATE_MEANING,
                    "PRIVATE_CONTENT_", str(tmp_path)):
        assert private not in emitted
    closed = report["simulations"][CLOSED]
    reopened = report["simulations"]["external_reopening"]
    assert closed["parameters"]["state_order"] == reopened["parameters"]["state_order"]
    assert closed["scope"]["scope_id"] == reopened["scope"]["scope_id"]
    assert closed["state_semantics"] == reopened["state_semantics"]


@pytest.mark.parametrize("mutation,flags", [
    ({"enabled": False}, ["--simulate"]),
    ({"seed": None}, ["--simulate"]),
    ({"state_distribution": None}, []),
    ({"scope_id": None}, []),
    ({"PRIVATE_UNKNOWN_PARAMETER": "PRIVATE_VALUE"}, []),
])
def test_conflicting_or_incomplete_activation_fails_safely(tmp_path, capsys, mutation, flags):
    scenario = declaration()
    scenario.update(mutation)
    args, _ = inputs(tmp_path, scenario)
    code, report, streams = invoke(args + flags, tmp_path / "out", capsys)
    assert code == 2
    emitted = streams.out + streams.err + json.dumps(report)
    assert "PRIVATE_" not in emitted
    if report is not None:
        assert report["simulations"] == {} and report["run"]["run_status"] == "failed"


def test_simulate_is_a_singleton_and_is_unavailable_on_validate(tmp_path, capsys):
    from recursive_integrity_toolkit.cli import main
    for arguments in (("audit", "--simulate", "--simulate"), ("validate", "--simulate")):
        assert main([*arguments, "--records", "PRIVATE_MISSING_RECORDS", "--out", str(tmp_path / "out")]) == 2
        streams = capsys.readouterr()
        assert streams.out == "" and "E_CONFIG_INVALID" in streams.err and "PRIVATE_" not in streams.err
    assert not (tmp_path / "out").exists()


def test_default_hero_example_keeps_simulation_unrequested(tmp_path, capsys):
    from recursive_integrity_toolkit.cli import main
    output = tmp_path / "hero"
    assert main(["example", "--out", str(output)]) == 0
    capsys.readouterr()
    report = json.loads((output / "reports/report.json").read_bytes())
    assert report["simulations"] == {}
    assert report["capabilities"]["intervention_simulation"]["execution_status"] == "not_requested"
    assert report["run"]["random_seed"] is None


@pytest.mark.parametrize("enabled,flags", [(None, ["--simulate"]), (True, [])])
def test_example_explicit_scenario_overlay_is_retained_with_packaged_audit_inputs(tmp_path, capsys, enabled, flags):
    from recursive_integrity_toolkit.cli import main
    scenario = declaration(enabled=enabled)
    overlay = tmp_path / "scenario.json"
    overlay.write_text(json.dumps({"simulation": scenario}), encoding="utf-8")
    original = overlay.read_bytes()
    output = tmp_path / "example"
    assert main(["example", "--out", str(output), "--config", str(overlay), *flags]) == 0
    capsys.readouterr()
    report = json.loads((output / "reports/report.json").read_bytes())
    assert set(report["simulations"]) == {CLOSED, "external_reopening"}
    assert report["derived_metrics"]["support"]["by_version"]
    assert overlay.read_bytes() == original
    extracted = json.loads((output / "inputs/config.json").read_bytes())
    assert extracted["simulation"] == scenario
    assert extracted["representation"]


@pytest.mark.parametrize("contents,flags", [
    ({"simulation": declaration(enabled=False)}, ["--simulate"]),
    ({"simulation": declaration(), "representation": {"name": "PRIVATE_EXTRA"}}, []),
    (None, ["--simulate"]),
])
def test_invalid_example_overlay_is_rejected_before_extraction(tmp_path, capsys, contents, flags):
    from recursive_integrity_toolkit.cli import main
    output = tmp_path / "example"
    arguments = ["example", "--out", str(output), *flags]
    if contents is not None:
        overlay = tmp_path / "scenario.json"
        overlay.write_text(json.dumps(contents), encoding="utf-8")
        arguments += ["--config", str(overlay)]
    assert main(arguments) == 2
    streams = capsys.readouterr()
    assert "PRIVATE_" not in streams.out + streams.err
    assert not output.exists()
