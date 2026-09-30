"""Offline simulation delivery through an actual installed distribution.

Set RIT_INSTALLED_PYTHON to an absolute wheel-installed interpreter, or run these
tests in the installed CI environment. Missing installation is a setup failure.
The subprocesses use isolated mode outside the checkout and never invoke pip.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[2]
NAMES = ("config.json", "records.jsonl", "provenance.jsonl", "EXPECTED_OUTPUTS.md")


RUNNER = r'''
import importlib.abc, json, pathlib, socket, sys, urllib.request
def denied(*args, **kwargs):
    raise AssertionError("installed simulation attempted network access")
socket.socket.connect = denied
socket.socket.connect_ex = denied
socket.create_connection = denied
urllib.request.urlopen = denied
repo = pathlib.Path(sys.argv.pop(1)).resolve()
arguments = sys.argv[1:]
input_only = arguments[0] == "validate"
sampler_attempts = []
class Block(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname == "pyarrow" or fullname.startswith("pyarrow."):
            raise ModuleNotFoundError("optional PyArrow unavailable for installed check")
        if input_only and (fullname == "numpy" or fullname.startswith(
                ("numpy.", "recursive_integrity_toolkit.metrics.resampling"))):
            sampler_attempts.append(fullname)
            raise AssertionError("input-only validation imported a sampler dependency")
sys.meta_path.insert(0, Block())
import recursive_integrity_toolkit
package = pathlib.Path(recursive_integrity_toolkit.__file__).resolve()
assert not package.is_relative_to(repo), "installed check imported the source checkout"
assert "site-packages" in package.parts, "a real installed distribution is required"
assert not pathlib.Path.cwd().is_relative_to(repo), "installed check ran inside the checkout"
from recursive_integrity_toolkit.cli import main
code = main(arguments)
assert "pyarrow" not in sys.modules
if input_only:
    assert sampler_attempts == [], sampler_attempts
    assert "numpy" not in sys.modules
    assert "recursive_integrity_toolkit.metrics.resampling" not in sys.modules
if code == 0:
    from importlib.resources import files
    from recursive_integrity_toolkit.result import validate_report
    out = pathlib.Path(arguments[arguments.index("--out") + 1])
    report_path = out / ("reports/report.json" if arguments[0] == "example" else "report.json")
    payload = json.loads(report_path.read_bytes())
    validate_report(payload)
    assert payload["run"]["report_schema_version"] == "1.3"
    assert payload["run"]["toolkit_version"] == recursive_integrity_toolkit.__version__
    if arguments[0] == "example":
        resources = files("recursive_integrity_toolkit").joinpath("data", "simulation")
        for name in ("config.json", "records.jsonl", "provenance.jsonl", "EXPECTED_OUTPUTS.md"):
            assert (out / "inputs" / name).read_bytes() == resources.joinpath(name).read_bytes()
sys.exit(code)
'''


@pytest.fixture(scope="module")
def installed_python():
    path = Path(os.environ.get("RIT_INSTALLED_PYTHON", sys.executable))
    assert path.is_absolute() and path.is_file(), "Installed interpreter must be an existing absolute path"
    return path


def _invoke(python, directory, arguments):
    directory.mkdir(parents=True, exist_ok=True)
    assert not directory.resolve().is_relative_to(ROOT)
    env = os.environ.copy()
    env.pop("PYTHONPATH", None)
    env.pop("PYTHONHOME", None)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    process = subprocess.run([str(python), "-I", "-c", RUNNER, str(ROOT), *arguments],
        cwd=directory, env=env, text=True, capture_output=True, timeout=60, check=False)
    assert "Traceback" not in process.stderr, process.stderr
    return process


def _report(directory):
    payload = json.loads((directory / "report.json").read_bytes())
    assert payload["run"]["report_schema_version"] == "1.3"
    assert payload["run"]["network_call_count"] == 0
    assert payload["capabilities"] == payload["observability"]["capabilities"]
    assert (directory / "report.md").read_text().startswith("# Recursive Integrity Audit Report\n")
    return payload


def _probabilities(rows):
    return [row["probability"] for row in rows]


def _sample_signature(node):
    """Compare paths and events while allowing per-report privacy aliases."""
    states = node["parameters"]["state_order"]
    return {
        "paths": [[(row["step"], row["state_counts"], row["state_frequencies"],
                    [states.index(state) for state in row["support"]],
                    row["support_size"], row["gini_simpson_diversity"])
                   for row in path["generations"]] for path in node["sampled_paths"]],
        "events": {name: [(row["replicate_index"], row["step"], states.index(row["state_id"]))
                          for row in node.get(name, [])]
                   for name in ("extinction_events", "state_reentry_events")},
        "sources": [(row["replicate_index"], row["step"],
                     _probabilities(row["input_normalization"]["effective_distribution"]))
                    for row in node.get("mixed_sources", [])],
    }


def _check_science(report):
    assert set(report["simulations"]) == {"closed_resampling", "external_reopening"}
    assert report["run"]["random_seed"] == 17
    assert report["capabilities"]["intervention_simulation"]["execution_status"] == "completed"
    assert [row["value"] for row in report["observed_facts"]["record_counts"].values()] == [2]
    assert [row["support_size"]["value"] for row in
            report["derived_metrics"]["support"]["by_version"].values()] == [2]
    assert [row["gini_simpson_diversity"]["value"] for row in
            report["derived_metrics"]["diversity"]["by_version"].values()] == [.5]
    closed = report["simulations"]["closed_resampling"]
    reopened = report["simulations"]["external_reopening"]
    states = closed["parameters"]["state_order"]
    assert len(states) == 2 and reopened["parameters"]["state_order"] == states
    for node in (closed, reopened):
        assert node["status"] == "experimental" and node["evidence_class"] == "simulation"
        assert node["parameters"]["random_seed"] == 17
        assert node["parameters"]["resample_size"] == 2
        assert node["parameters"]["simulation_horizon"] == 6
        assert node["parameters"]["simulation_replicates"] == 3
        assert node["parameters"]["scenario_schedule"] == "reset_same_seed_per_model"
        assert _probabilities(node["initial_distribution"]) == [1., 0.]
        assert node["scope"]["denominator_basis"] == "explicit_scenario_probability_vector"
        assert node["scope"]["included_record_keys"] == node["scope"]["excluded_record_keys"] == []
        assert node["scope"]["record_count"] == 0
        assert node["assumption_table"] and node["limitations"]
        assert len(node["sampled_paths"]) == 3
        expected_extinctions, expected_reentries = [], []
        for replicate, path in enumerate(node["sampled_paths"]):
            assert path["replicate_index"] == replicate
            rows = path["generations"]
            assert [row["step"] for row in rows] == list(range(7))
            assert rows[0]["state_counts"] is None
            for row in rows:
                masses = row["state_frequencies"]
                assert row["support"] == [state for state, mass in zip(states, masses) if mass > 0]
                assert row["support_size"] == len(row["support"])
                assert row["gini_simpson_diversity"] == pytest.approx(1 - sum(p*p for p in masses))
                if row["step"]:
                    assert sum(row["state_counts"]) == 2
                    assert masses == [count / 2 for count in row["state_counts"]]
            for before, after in zip(rows, rows[1:]):
                for state, old, new in zip(states, before["state_frequencies"], after["state_frequencies"]):
                    event = {"replicate_index": replicate, "step": after["step"], "state_id": state}
                    if old > 0 and new == 0:
                        expected_extinctions.append(event)
                    if old == 0 and new > 0:
                        expected_reentries.append(event)
        assert node["extinction_events"] == expected_extinctions
        assert node.get("state_reentry_events", []) == expected_reentries
    assert all(row["state_frequencies"] == [1., 0.] for path in closed["sampled_paths"]
               for row in path["generations"])
    assert closed["analytic_baseline"]["expected_diversity"] == [0.] * 7
    assert "analytic_baseline" not in reopened and "expected_diversity" not in reopened
    assert reopened["parameters"]["reopening_weight"] == .25
    assert _probabilities(reopened["external_input_distribution"]) == [0., 1.]
    assert len(reopened["mixed_sources"]) == 18
    for source in reopened["mixed_sources"]:
        previous = reopened["sampled_paths"][source["replicate_index"]]["generations"][source["step"] - 1]
        p_a, p_b = previous["state_frequencies"]
        assert _probabilities(source["input_normalization"]["effective_distribution"]) == [
            .75 * p_a, .75 * p_b + .25]
        assert source["possible_reentry_states"] == ([states[1]] if p_b == 0 else [])
    comparison = reopened["scenario_comparison"]
    assert comparison["difference_direction"] == "reopened_minus_closed"
    assert len(comparison["rows"]) == 21
    assert comparison["initial_reachability"][0]["reachable_states"] == [states[0]]
    assert comparison["initial_reachability"][1]["reachable_states"] == states
    assert comparison["initial_reachability"][1]["possible_reentry_states"] == [states[1]]
    assert "External independence, reliability and relevance are supplied assumptions, not verified facts." in reopened["limitations"]
    assert any(row["conclusion"] == "empirical_intervention_effect" and row["status"] == "unavailable"
               for row in report["unavailable_conclusions"])


@pytest.mark.parametrize("redacted", [False, True])
def test_packaged_simulation_outside_checkout_with_network_blocked(installed_python, tmp_path, redacted):
    reports = []
    for name in ("first", "replay"):
        out = tmp_path / name
        arguments = ["example", "--dataset", "simulation", "--simulate", "--out", str(out)]
        if redacted:
            arguments.append("--redacted")
        process = _invoke(installed_python, tmp_path, arguments)
        assert process.returncode == 0, process.stderr
        report = _report(out / "reports")
        _check_science(report)
        assert report["run"]["privacy_mode"] == ("redacted" if redacted else "standard")
        for resource in NAMES:
            assert (out / "inputs" / resource).read_bytes() == (ROOT / "examples/simulation" / resource).read_bytes()
        markdown = (out / "reports/report.md").read_text()
        assert "Experimental simulation" in markdown and "Scenario assumptions" in markdown
        assert "Pre-draw source probabilities" in markdown and "Distinct closed analytic baseline" in markdown
        if redacted:
            emitted = json.dumps(report) + markdown + process.stdout + process.stderr
            config = json.loads((out / "inputs/config.json").read_bytes())["simulation"]
            assert str(tmp_path) not in emitted
            for text in (config["scope_id"], config["state_semantics"], config["dataset_version"]):
                assert text not in emitted
            assert report["simulations"]["closed_resampling"]["parameters"]["state_order"] != ["A", "B"]
        reports.append(report)
    for model in ("closed_resampling", "external_reopening"):
        assert _sample_signature(reports[0]["simulations"][model]) == _sample_signature(reports[1]["simulations"][model])


def test_installed_validate_never_imports_sampler_or_numpy(installed_python, tmp_path):
    out = tmp_path / "example"
    process = _invoke(installed_python, tmp_path,
        ["example", "--dataset", "simulation", "--simulate", "--out", str(out)])
    assert process.returncode == 0, process.stderr
    original = {name: (out / "inputs" / name).read_bytes() for name in NAMES}
    enabled = json.loads(original["config.json"])
    enabled["simulation"]["enabled"] = True
    enabled_path = tmp_path / "enabled-config.json"
    enabled_path.write_text(json.dumps(enabled), encoding="utf-8")
    for config_path in (out / "inputs/config.json", enabled_path):
        checked = tmp_path / ("validated-enabled" if config_path == enabled_path else "validated")
        process = _invoke(installed_python, tmp_path, ["validate",
            "--records", str(out / "inputs/records.jsonl"),
            "--provenance", str(out / "inputs/provenance.jsonl"),
            "--config", str(config_path), "--out", str(checked)])
        assert process.returncode == 0, process.stderr
        report = _report(checked)
        assert report["simulations"] == report["proxy_signals"] == {}
        assert report["derived_metrics"] == {"longitudinal": {"snapshots": [], "comparisons": []}}
        assert report["capabilities"]["intervention_simulation"]["execution_status"] != "completed"
        assert report["capabilities"]["intervention_simulation"]["status"] == (
            "experimental" if config_path == enabled_path else "unavailable")
    assert original == {name: (out / "inputs" / name).read_bytes() for name in NAMES}


@pytest.mark.parametrize("extra", [[], ["--simulate", "--lineage"],
    ["--simulate", "--longitudinal"], ["--simulate", "--config", "PRIVATE_MISSING_CONFIG"]])
def test_installed_simulation_requires_its_explicit_mode(installed_python, tmp_path, extra):
    out = tmp_path / "rejected"
    process = _invoke(installed_python, tmp_path,
        ["example", "--dataset", "simulation", *extra, "--out", str(out)])
    assert process.returncode == 2, process.stderr
    assert "E_CONFIG_INVALID" in process.stderr and "PRIVATE_" not in process.stdout + process.stderr
    assert not out.exists()
