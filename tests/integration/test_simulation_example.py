"""The offline synthetic example binds declared sources to actual sampled evidence."""
from __future__ import annotations

from fractions import Fraction
from importlib.resources import files
from itertools import product
import json
from pathlib import Path
import socket
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[2]
EXAMPLE = ROOT / "examples/simulation"
NAMES = ("config.json", "records.jsonl", "provenance.jsonl", "EXPECTED_OUTPUTS.md")
CLOSED = "closed_resampling"
REOPENED = "external_reopening"


def resources():
    return files("recursive_integrity_toolkit").joinpath("data", "simulation")


def probabilities(rows):
    return {row["state_id"]: row["probability"] for row in rows}


def strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from strings(item)


@pytest.fixture(autouse=True)
def deny_network(monkeypatch):
    def denied(*_args, **_kwargs):
        pytest.fail("The packaged local example attempted network access")
    for name in ("connect", "connect_ex"):
        monkeypatch.setattr(socket.socket, name, denied)
    monkeypatch.setattr(socket, "create_connection", denied)
    monkeypatch.setattr(socket, "getaddrinfo", denied)


def invoke(workspace, capsys, *flags):
    from recursive_integrity_toolkit.cli import main
    from recursive_integrity_toolkit.result import validate_report
    code = main(["example", "--dataset", "simulation", "--simulate", "--out", str(workspace), *flags])
    streams = capsys.readouterr()
    report = json.loads((workspace / "reports/report.json").read_bytes()) if code == 0 else None
    if report is not None:
        validate_report(report)
    return code, report, streams


@pytest.mark.parametrize("name", NAMES)
def test_packaged_simulation_resources_match_public_inputs(name):
    assert resources().joinpath(name).read_bytes() == (EXAMPLE / name).read_bytes()


def test_declared_first_transition_has_independent_exact_oracle():
    scenario = json.loads(resources().joinpath("config.json").read_bytes())["simulation"]
    assert scenario["models"] == [CLOSED, "reopened_resampling"]
    assert scenario["state_distribution"] == {"A": 1, "B": 0}
    assert scenario["external_input_distribution"] == {"A": 0, "B": 1}
    assert (scenario["seed"], scenario["resample_size"], scenario["simulation_horizon"],
            scenario["simulation_replicates"]) == (17, 2, 6, 3)
    weight = Fraction(str(scenario["reopening_weight"]))
    source = {state: (1 - weight) * Fraction(scenario["state_distribution"][state])
              + weight * Fraction(scenario["external_input_distribution"][state])
              for state in ("A", "B")}
    assert source == {"A": Fraction(3, 4), "B": Fraction(1, 4)}
    # Enumerate the four ordered two-draw outcomes, independently of the sampler.
    count_probabilities = {0: Fraction(0), 1: Fraction(0), 2: Fraction(0)}
    for first, second in product(("A", "B"), repeat=2):
        count_probabilities[(first == "B") + (second == "B")] += source[first] * source[second]
    assert count_probabilities == {0: Fraction(9, 16), 1: Fraction(6, 16), 2: Fraction(1, 16)}
    expected_diversity = sum(probability * (1 - Fraction(count, 2) ** 2 - Fraction(2 - count, 2) ** 2)
                             for count, probability in count_probabilities.items())
    assert expected_diversity == Fraction(3, 16)
    assert count_probabilities[1] + count_probabilities[2] == Fraction(7, 16)


def test_example_retains_independent_audit_and_zero_membership_scenario(tmp_path, capsys):
    workspace = tmp_path / "example"
    code, report, streams = invoke(workspace, capsys)
    assert code == 0, streams.err
    assert report["run"]["random_seed"] == 17
    assert report["run"]["network_call_count"] == 0
    assert report["run"]["run_status"] == "complete"
    assert report["observed_facts"]["record_counts"]["audit-v1"]["value"] == 2
    assert report["observed_facts"]["state_counts"]["by_version"]["audit-v1"]["value"] == [
        {"state_id": "X", "state_count": 1}, {"state_id": "Y", "state_count": 1}]
    assert report["derived_metrics"]["support"]["by_version"]["audit-v1"]["support_size"]["value"] == 2
    assert report["derived_metrics"]["diversity"]["by_version"]["audit-v1"]["gini_simpson_diversity"]["value"] == .5
    assert report["derived_metrics"]["closure_exposure"]["direct"]["lower_bound"]["value"] == 1
    assert set(report["simulations"]) == {CLOSED, REOPENED}
    assert report["capabilities"]["intervention_simulation"]["execution_status"] == "completed"
    for model in report["simulations"].values():
        assert model["status"] == "experimental" and model["evidence_class"] == "simulation"
        assert probabilities(model["initial_distribution"]) == {"A": 1, "B": 0}
        assert model["parameters"]["random_seed"] == 17
        assert model["parameters"]["state_order"] == ["A", "B"]
        assert model["scope"]["scope_id"] == "simulation-example-scenario"
        assert model["scope"]["dataset_versions"] == ["scenario-v1"]
        assert model["scope"]["denominator_basis"] == "explicit_scenario_probability_vector"
        assert model["scope"]["included_record_keys"] == model["scope"]["excluded_record_keys"] == []
        assert model["scope"]["record_count"] == model["scope"]["excluded_record_count"] == 0
        assert model["denominator"] == 2
    assert any(row["conclusion"] == "empirical_intervention_effect" and row["status"] == "unavailable"
               for row in report["unavailable_conclusions"])
    for name in NAMES:
        assert (workspace / "inputs" / name).read_bytes() == resources().joinpath(name).read_bytes()


def test_sampled_counts_sources_and_event_identities_match_each_actual_path(tmp_path, capsys):
    code, report, streams = invoke(tmp_path / "example", capsys)
    assert code == 0, streams.err
    closed, reopened = report["simulations"][CLOSED], report["simulations"][REOPENED]
    sources = {(row["replicate_index"], row["step"]): row for row in reopened["mixed_sources"]}
    assert set(sources) == set(product(range(3), range(1, 7)))
    for node in (closed, reopened):
        reentries, extinctions = [], []
        assert [path["replicate_index"] for path in node["sampled_paths"]] == [0, 1, 2]
        for path in node["sampled_paths"]:
            replicate = path["replicate_index"]
            generations = path["generations"]
            assert [row["step"] for row in generations] == list(range(7))
            assert generations[0]["state_counts"] is None
            assert generations[0]["state_frequencies"] == [1, 0]
            previous = [Fraction(1), Fraction(0)]
            for row in generations:
                step = row["step"]
                if step:
                    assert all(type(count) is int and count >= 0 for count in row["state_counts"])
                    assert sum(row["state_counts"]) == 2
                    frequencies = [Fraction(count, 2) for count in row["state_counts"]]
                    assert row["state_frequencies"] == [float(value) for value in frequencies]
                    for index, state in enumerate(("A", "B")):
                        if previous[index] > 0 and frequencies[index] == 0:
                            extinctions.append((replicate, step, state))
                        if previous[index] == 0 and frequencies[index] > 0:
                            reentries.append((replicate, step, state))
                    if node is reopened:
                        expected_source = {"A": float(Fraction(3, 4) * previous[0]),
                                           "B": float(Fraction(3, 4) * previous[1] + Fraction(1, 4))}
                        source = sources[replicate, step]
                        assert probabilities(source["input_normalization"]["effective_distribution"]) == expected_source
                        assert source["possible_reentry_states"] == [state for index, state in enumerate(("A", "B"))
                            if previous[index] == 0 and expected_source[state] > 0]
                    previous = frequencies
                assert row["support"] == [state for state, value in zip(("A", "B"), previous) if value > 0]
                assert row["support_size"] == len(row["support"])
                assert row["gini_simpson_diversity"] == float(1 - sum(value * value for value in previous))
            if node is reopened:
                assert node["support_trajectory"][replicate]["support_sizes"] == [row["support_size"] for row in generations]
                assert node["diversity_trajectory"][replicate]["gini_simpson_diversities"] == [row["gini_simpson_diversity"] for row in generations]
        identity = lambda rows: [(row["replicate_index"], row["step"], row["state_id"]) for row in rows]
        assert identity(node["extinction_events"]) == extinctions
        if node is reopened:
            assert identity(node["state_reentry_events"]) == reentries
        else:
            assert reentries == extinctions == []
            assert all(row["support"] == ["A"] for path in node["sampled_paths"] for row in path["generations"])


def test_closed_baseline_and_reopened_assumptions_remain_distinct(tmp_path, capsys):
    workspace = tmp_path / "example"
    code, report, streams = invoke(workspace, capsys)
    assert code == 0, streams.err
    closed, reopened = report["simulations"][CLOSED], report["simulations"][REOPENED]
    baseline = closed["analytic_baseline"]
    assert baseline["method"] == "analytic_expectation"
    assert baseline["expected_diversity"] == [0] * 7
    assert baseline["parameters"]["random_seed"] is None
    assert "analytic_baseline" not in reopened and "expected_diversity" not in reopened
    assert {row["assumption"] for row in reopened["assumption_table"]} >= {"External quality", "Constant external input"}
    assumptions = json.dumps(reopened["assumption_table"])
    assert "supplied assumptions" in assumptions
    assert "without guaranteeing a sampled count" in assumptions
    comparison = reopened["scenario_comparison"]
    assert comparison["difference_direction"] == "reopened_minus_closed"
    assert len(comparison["rows"]) == 21
    assert comparison["initial_reachability"][0]["reachable_states"] == ["A"]
    assert comparison["initial_reachability"][1]["reachable_states"] == ["A", "B"]
    assert comparison["initial_reachability"][1]["possible_reentry_states"] == ["B"]
    markdown = (workspace / "reports/report.md").read_text(encoding="utf-8")
    assert "Scenario assumptions" in markdown and "Distinct closed analytic baseline" in markdown
    assert "**Pre-draw source probabilities**" in markdown and "**Realized sample detail**" in markdown


def test_same_environment_seed_replays_identical_simulations(tmp_path, capsys):
    first_code, first, _ = invoke(tmp_path / "first", capsys)
    second_code, second, _ = invoke(tmp_path / "second", capsys)
    assert first_code == second_code == 0
    assert first["simulations"] == second["simulations"]


def test_redacted_reports_protect_scenario_labels_while_extracted_inputs_remain_exact(tmp_path, capsys):
    workspace = tmp_path / "redacted"
    code, report, streams = invoke(workspace, capsys, "--redacted")
    assert code == 0, streams.err
    configuration = json.loads(resources().joinpath("config.json").read_bytes())["simulation"]
    serialized = json.dumps(report) + streams.out + streams.err + (workspace / "reports/report.md").read_text(encoding="utf-8")
    for private in (configuration["scope_id"], configuration["dataset_version"], configuration["state_semantics"], str(workspace)):
        assert private not in serialized
    assert not {"A", "B"}.intersection(strings(report["simulations"]))
    closed, reopened = report["simulations"][CLOSED], report["simulations"][REOPENED]
    assert closed["parameters"]["state_order"] == reopened["parameters"]["state_order"]
    assert closed["scope"]["scope_id"] == reopened["scope"]["scope_id"]
    for name in NAMES:
        assert (workspace / "inputs" / name).read_bytes() == resources().joinpath(name).read_bytes()


@pytest.mark.parametrize("flags", [[], ["--simulate", "--lineage"], ["--simulate", "--longitudinal"],
                                  ["--simulate", "--config", "PRIVATE_UNREAD_CONFIG.json"]])
def test_invalid_example_selection_fails_before_creating_workspace(tmp_path, capsys, flags):
    from recursive_integrity_toolkit.cli import main
    workspace = tmp_path / "invalid"
    assert main(["example", "--dataset", "simulation", "--out", str(workspace), *flags]) == 2
    streams = capsys.readouterr()
    assert "E_CONFIG_INVALID" in streams.err
    assert "PRIVATE_UNREAD_CONFIG" not in streams.out + streams.err
    assert not workspace.exists()


def test_example_refuses_existing_workspace_without_changing_its_files(tmp_path, capsys):
    workspace = tmp_path / "example"
    code, _, streams = invoke(workspace, capsys)
    assert code == 0, streams.err
    before = {str(path.relative_to(workspace)): path.read_bytes() for path in workspace.rglob("*") if path.is_file()}
    code, _, streams = invoke(workspace, capsys)
    assert code == 1 and "E_OUTPUT_EXISTS" in streams.err
    assert {str(path.relative_to(workspace)): path.read_bytes() for path in workspace.rglob("*") if path.is_file()} == before


def test_validate_extracted_declaration_never_imports_sampler(tmp_path, capsys, subprocess_env):
    workspace = tmp_path / "example"
    code, _, streams = invoke(workspace, capsys)
    assert code == 0, streams.err
    inputs = workspace / "inputs"
    # Activate the complete declaration in the validate input to exercise the strongest case.
    configuration = json.loads((inputs / "config.json").read_bytes())
    configuration["simulation"]["enabled"] = True
    active = tmp_path / "enabled.json"
    active.write_text(json.dumps(configuration), encoding="utf-8")
    program = '''import importlib.abc,socket,sys
attempts=[]
class Block(importlib.abc.MetaPathFinder):
 def find_spec(self,fullname,path=None,target=None):
  if fullname == 'numpy' or fullname.startswith(('numpy.','recursive_integrity_toolkit.metrics.resampling')):
   attempts.append(fullname)
   raise AssertionError('input-only validation imported a sampler dependency')
def denied(*args,**kwargs): raise AssertionError('offline validation attempted network access')
socket.socket.connect=denied
socket.socket.connect_ex=denied
socket.create_connection=denied
socket.getaddrinfo=denied
sys.meta_path.insert(0,Block())
from recursive_integrity_toolkit.cli import main
assert main(sys.argv[1:]) == 0
assert attempts == []
assert 'numpy' not in sys.modules
assert 'recursive_integrity_toolkit.metrics.resampling' not in sys.modules
'''
    output = tmp_path / "validation"
    process = subprocess.run([sys.executable, "-c", program, "validate", "--records", str(inputs / "records.jsonl"),
        "--provenance", str(inputs / "provenance.jsonl"), "--config", str(active), "--out", str(output)],
        cwd=tmp_path, env=subprocess_env, capture_output=True, text=True)
    assert process.returncode == 0, process.stderr
    report = json.loads((output / "report.json").read_bytes())
    from recursive_integrity_toolkit.result import validate_report
    validate_report(report)
    assert report["simulations"] == report["proxy_signals"] == {}
    assert report["derived_metrics"] == {"longitudinal": {"snapshots": [], "comparisons": []}}
    assert report["capabilities"]["intervention_simulation"]["execution_status"] != "completed"
    assert report["run"]["network_call_count"] == 0


@pytest.mark.parametrize("selection", [[], ["--dataset", "longitudinal", "--longitudinal"]])
def test_existing_examples_keep_simulation_inactive(tmp_path, capsys, monkeypatch, selection):
    from recursive_integrity_toolkit.cli import main
    from recursive_integrity_toolkit.metrics import resampling
    def forbidden(*_args, **_kwargs):
        pytest.fail("An ordinary example dispatched a scenario")
    monkeypatch.setattr(resampling, "run_scenario_experiment", forbidden)
    workspace = tmp_path / "ordinary"
    assert main(["example", "--out", str(workspace), *selection]) == 0
    capsys.readouterr()
    report = json.loads((workspace / "reports/report.json").read_bytes())
    assert report["simulations"] == {}
    assert report["capabilities"]["intervention_simulation"]["execution_status"] == "not_requested"
