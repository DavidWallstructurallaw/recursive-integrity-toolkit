"""Cross-layer admission and atomic failure at real experiment boundaries."""
from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
import json
from types import MappingProxyType

import numpy as np
import pytest

from recursive_integrity_toolkit.config import (
    config_scenario_parameters,
    resolve_phase4_options,
    scenario_calculation_scope,
)
from recursive_integrity_toolkit.errors import CanonicalValidationError, ConfigurationError, ErrorCode
from recursive_integrity_toolkit.metrics import resampling
from recursive_integrity_toolkit.models import CanonicalRow, CapabilityKey, CapabilityStatus, RecordKey
from recursive_integrity_toolkit.observability.levels import classify_observability


CLOSED = "closed_resampling"
REOPENED = "reopened_resampling"
SELECTIONS = ((CLOSED,), (REOPENED,), (CLOSED, REOPENED), (REOPENED, CLOSED))


@pytest.fixture
def example_config(repo_root):
    return json.loads((repo_root / "examples/simulation/config.json").read_bytes())


def _states(count):
    # Zero-mass states still occupy every retained generation's declared vector.
    return {f"PRIVATE_STATE_{index}": int(index == 0) for index in range(count)}


def _declaration(example_config, models, *, over=False):
    raw = deepcopy(example_config)
    # 100 * 10,000 == 1,000,000, or two models * 100 * 5,000.
    # Single-model rejection is exactly one cell over. For two common models,
    # 2 * 106 * 4,717 == 1,000,004; both individually remain below the bound.
    count, generations = ((101, 9901) if len(models) == 1 else (106, 4717)) if over else (
        100, 10000 // len(models))
    scenario = raw["simulation"]
    scenario.update(enabled=True, models=list(models), state_distribution=_states(count),
        simulation_horizon=generations - 1, simulation_replicates=1)
    if REOPENED in models:
        scenario["external_input_distribution"] = _states(count)
    else:
        scenario.pop("external_input_distribution")
        scenario.pop("reopening_weight")
    return raw


def _request(scenario):
    return resampling.ScenarioExperimentRequest(
        scenarios=config_scenario_parameters(scenario),
        scope=scenario_calculation_scope(scenario),
        representation=scenario.representation,
        state_semantics=scenario.state_semantics,
        seed=scenario.seed,
    )


def _capability(scenario):
    values = {"dataset_version": "audit-v1", "record_id": "record", "content": "synthetic"}
    row = CanonicalRow("records", RecordKey("audit-v1", "record"),
        MappingProxyType(values), MappingProxyType({}), MappingProxyType({}))
    return classify_observability((row,), scenario=scenario).capabilities[CapabilityKey.INTERVENTION_SIMULATION]


def _forbid_execution(monkeypatch):
    def forbidden(*_args, **_kwargs):
        pytest.fail("Rejected declaration reached RNG or trajectory allocation")
    monkeypatch.setattr(np.random, "PCG64", forbidden)
    for name in ("_generation", "_sample_counts", "simulate_closed_resampling", "simulate_reopened_resampling"):
        monkeypatch.setattr(resampling, name, forbidden)


@pytest.mark.parametrize("models", SELECTIONS)
def test_actual_million_cell_boundary_is_admitted_across_layers(example_config, models, monkeypatch):
    scenario = resolve_phase4_options(_declaration(example_config, models)).configuration.simulation
    request = _request(scenario)
    assert resampling.MAX_PATH_CELLS == 1_000_000
    assert sum(len(item.state_distribution) * (item.simulation_horizon + 1) * item.simulation_replicates
               for item in request.scenarios) == 1_000_000
    assert _capability(scenario).status is CapabilityStatus.EXPERIMENTAL

    class AdmittedToGeneration(Exception):
        pass

    def first_generation(step, counts, probabilities, state_order):
        assert step == 0 and counts is None
        assert len(probabilities) == len(state_order) == 100
        raise AdmittedToGeneration

    def forbidden(*_args, **_kwargs):
        pytest.fail("Admission probe executed random draws")

    monkeypatch.setattr(resampling, "_generation", first_generation)
    monkeypatch.setattr(np.random, "PCG64", forbidden)
    monkeypatch.setattr(resampling, "_sample_counts", forbidden)
    # No limit is patched, and no million-cell report is constructed. Reaching
    # this sentinel proves collective and per-model preflight both accepted.
    with pytest.raises(AdmittedToGeneration):
        resampling.run_scenario_experiment(request)


@pytest.mark.parametrize("models", SELECTIONS)
def test_just_over_real_budget_rejected_by_config_eligibility_and_kernel(example_config, models, monkeypatch):
    accepted = resolve_phase4_options(_declaration(example_config, models)).configuration.simulation
    request = _request(accepted)
    oversized = _declaration(example_config, models, over=True)
    supplied = oversized["simulation"]
    distribution = tuple(supplied["state_distribution"].items())
    horizon = supplied["simulation_horizon"]
    cells_each = len(distribution) * (horizon + 1)
    assert len(models) * cells_each == (1_000_001 if len(models) == 1 else 1_000_004)
    if len(models) == 2:
        assert cells_each < 1_000_000
    forged = replace(accepted, state_distribution=distribution, simulation_horizon=horizon,
        external_input_distribution=distribution if REOPENED in models else None)
    request = replace(request, scenarios=tuple(replace(item, state_distribution=distribution,
        simulation_horizon=horizon,
        external_input_distribution=distribution if item.model_name == REOPENED else None)
        for item in request.scenarios))
    _forbid_execution(monkeypatch)
    with pytest.raises(ConfigurationError) as config_error:
        resolve_phase4_options(oversized)
    assert config_error.value.code is ErrorCode.CONFIG_INVALID
    capability = _capability(forged)
    assert capability.status is CapabilityStatus.UNAVAILABLE
    assert "R_SCENARIO_PARAMETERS_INVALID" in capability.reason_codes
    with pytest.raises(CanonicalValidationError) as kernel_error:
        resampling.run_scenario_experiment(request)
    assert kernel_error.value.code is ErrorCode.CONFIG_INVALID
    assert "PRIVATE_" not in str(config_error.value) + str(kernel_error.value)


@pytest.mark.parametrize("command", ("audit", "validate"))
def test_cli_budget_refusal_precedes_sampling_and_emits_no_successful_paths(
        example_config, repo_root, tmp_path, capsys, monkeypatch, command):
    from recursive_integrity_toolkit.cli import main
    from recursive_integrity_toolkit.result import validate_report
    raw = _declaration(example_config, (CLOSED, REOPENED), over=True)
    config_path = tmp_path / "PRIVATE_CONFIGURATION.json"
    config_path.write_text(json.dumps(raw), encoding="utf-8")
    output = tmp_path / "out"
    _forbid_execution(monkeypatch)
    assert main([command, "--config", str(config_path), "--records",
        str(repo_root / "examples/simulation/records.jsonl"), "--out", str(output)]) == 2
    streams = capsys.readouterr()
    report = json.loads((output / "report.json").read_bytes())
    validate_report(report)
    assert report["run"]["run_status"] == "failed" and report["simulations"] == {}
    assert report["observed_facts"] == report["derived_metrics"] == report["capabilities"] == {}
    assert any(row["code"] == "E_CONFIG_INVALID" for row in report["errors"])
    emitted = json.dumps(report) + streams.out + streams.err + (output / "report.md").read_text(encoding="utf-8")
    assert "PRIVATE_" not in emitted


@pytest.mark.parametrize("models", ((CLOSED, REOPENED), (REOPENED, CLOSED)))
def test_second_model_rng_failure_discards_experiment_and_retains_independent_audit(
        example_config, repo_root, tmp_path, capsys, monkeypatch, models):
    from recursive_integrity_toolkit.cli import main
    from recursive_integrity_toolkit.result import validate_report
    raw = deepcopy(example_config)
    raw["simulation"].update(enabled=True, models=list(models))
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps(raw), encoding="utf-8")
    completed, generators = [], []
    for model, name in ((CLOSED, "simulate_closed_resampling"), (REOPENED, "simulate_reopened_resampling")):
        actual = getattr(resampling, name)

        def observed(*args, _actual=actual, _model=model, **kwargs):
            result = _actual(*args, **kwargs)
            completed.append(_model)
            return result

        monkeypatch.setattr(resampling, name, observed)
    actual_pcg64 = np.random.PCG64

    def fail_second(seed):
        generators.append(seed)
        if len(generators) == 2:
            raise RuntimeError("PRIVATE_RNG_FAILURE_DETAIL")
        return actual_pcg64(seed)

    monkeypatch.setattr(np.random, "PCG64", fail_second)
    example = repo_root / "examples/simulation"
    output = tmp_path / "out"
    code = main(["audit", "--config", str(config_path), "--records", str(example / "records.jsonl"),
        "--provenance", str(example / "provenance.jsonl"), "--out", str(output)])
    streams = capsys.readouterr()
    report = json.loads((output / "report.json").read_bytes())
    validate_report(report)
    assert completed == [models[0]] and generators == [17, 17]
    assert code == 4 and report["run"]["run_status"] == "partial"
    assert report["simulations"] == {}
    assert report["capabilities"]["intervention_simulation"]["execution_status"] == "failed"
    assert report["observed_facts"]["record_counts"]["audit-v1"]["value"] == 2
    assert report["derived_metrics"]["support"]["by_version"]["audit-v1"]["support_size"]["value"] == 2
    assert report["derived_metrics"]["diversity"]["by_version"]["audit-v1"]["gini_simpson_diversity"]["value"] == .5
    assert report["derived_metrics"]["closure_exposure"]["direct"]["lower_bound"]["value"] == 1
    assert report["capabilities"]["content_diagnostics"]["execution_status"] == "completed"
    assert any(row["severity"] == "error" and row["effect_on_capabilities"] == ["intervention_simulation"]
               and row["effect_on_run"] == "partial"
               for row in report["errors"])
    assert any(row["conclusion"] == "empirical_intervention_effect" and row["status"] == "unavailable"
               for row in report["unavailable_conclusions"])
    emitted = json.dumps(report) + streams.out + streams.err + (output / "report.md").read_text(encoding="utf-8")
    assert "PRIVATE_RNG_FAILURE_DETAIL" not in emitted
