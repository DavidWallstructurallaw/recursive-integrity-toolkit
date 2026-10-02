"""Explicit scenario declarations remain private, replayable and input-only."""

from copy import deepcopy
from dataclasses import FrozenInstanceError, replace
import json
import subprocess
import sys
from types import MappingProxyType

import jsonschema
import pytest

from recursive_integrity_toolkit import config as config_module
from recursive_integrity_toolkit.config import (
    ScenarioConfig, load_config, phase4_config_hash, phase4_config_summary,
    phase4_validation_configuration, resolve_config, resolve_phase4_options,
)
from recursive_integrity_toolkit.errors import ConfigurationError
from recursive_integrity_toolkit.models import (
    CanonicalRow, CapabilityKey, CapabilityStatus, RecordKey, ScenarioParameters,
)
from recursive_integrity_toolkit.observability.levels import classify_observability


CLOSED = "closed_resampling"
REOPENED = "reopened_resampling"


def declaration(**changes):
    value = {
        "enabled": True,
        "seed": 37,
        "models": [REOPENED, CLOSED],
        "state_distribution": {"PRIVATE-state": .5, "": 0., "é": .25, "e\u0301": .25},
        "external_input_distribution": {"PRIVATE-state": .25, "": .25, "é": .25, "e\u0301": .25},
        "reopening_weight": .25,
        "resample_size": 8,
        "simulation_horizon": 3,
        "simulation_replicates": 2,
        "representation": {
            "representation_name": "PRIVATE-representation",
            "representation_source": "PRIVATE-source",
            "representation_version": "PRIVATE-taxonomy",
            "binning_or_mapping_rule": "PRIVATE-rule",
            "field_name": "PRIVATE-field",
            "missing_value_policy": "explicit_missing_state",
            "missing_state_id": "PRIVATE-missing",
            "normalization_profile": "exact_utf8_v1",
        },
        "state_semantics": "PRIVATE-category meaning",
        "scope_id": "PRIVATE-scope",
        "dataset_version": "PRIVATE-scenario-version",
    }
    value.update(changes)
    return {"simulation": value}


def capability(scenario, parameters=None):
    values = {"dataset_version": "audit-v1", "record_id": "observed", "content": "synthetic"}
    records = (CanonicalRow("records", RecordKey("audit-v1", "observed"),
        MappingProxyType(values), MappingProxyType({}), MappingProxyType({})),)
    return classify_observability(records, scenario=scenario, scenario_parameters=parameters).capabilities[
        CapabilityKey.INTERVENTION_SIMULATION]


def test_full_declaration_is_detached_and_preserves_literal_states_and_model_order():
    raw = declaration()
    config = resolve_config(raw)
    scenario = config.simulation
    expected = deepcopy(raw["simulation"])
    raw["simulation"]["models"].reverse()
    raw["simulation"]["state_distribution"].clear()
    raw["simulation"]["representation"]["representation_name"] = "changed"
    assert scenario.models == (REOPENED, CLOSED)
    assert dict(scenario.state_distribution) == expected["state_distribution"]
    assert "é" in dict(scenario.state_distribution) and "e\u0301" in dict(scenario.state_distribution)
    assert scenario.representation.representation_name == "PRIVATE-representation"
    with pytest.raises(FrozenInstanceError):
        scenario.seed = 38
    options = resolve_phase4_options(config)
    detached = phase4_validation_configuration(options)
    assert resolve_config(detached).simulation == scenario
    detached["simulation"]["state_distribution"]["PRIVATE-state"] = 0
    assert dict(scenario.state_distribution)["PRIVATE-state"] == .5
    assert "PRIVATE" not in repr(scenario)
    assert "PRIVATE" not in repr(options)
    assert "PRIVATE" not in json.dumps(phase4_config_summary(options))
    assert phase4_config_summary(options)["scenario_requested"] is True


def test_config_adapter_retains_declared_scope_without_fabricating_record_membership():
    scenario = resolve_config(declaration()).simulation
    scope = config_module.scenario_calculation_scope(scenario)
    assert scope.dataset_versions == ("PRIVATE-scenario-version",)
    assert scope.scope_id == "PRIVATE-scope"
    assert scope.denominator_basis == "explicit_scenario_probability_vector"
    assert scope.included_record_keys == scope.excluded_record_keys == ()
    parameters = config_module.config_scenario_parameters(scenario)
    assert tuple(item.model_name for item in parameters) == scenario.models
    for item in parameters:
        assert type(item) is ScenarioParameters
        assert item.state_distribution == scenario.state_distribution
        assert (item.resample_size, item.simulation_horizon, item.simulation_replicates) == (8, 3, 2)
    assert parameters[0].external_input_distribution == scenario.external_input_distribution
    assert parameters[0].reopening_weight == .25
    assert parameters[1].external_input_distribution is None
    assert parameters[1].reopening_weight is None


def test_json_and_toml_preserve_the_same_complete_declaration(tmp_path):
    raw = declaration()
    json_path = tmp_path / "scenario.json"
    json_path.write_text(json.dumps(raw, ensure_ascii=False), encoding="utf-8")
    values = raw["simulation"]
    tables = {"state_distribution", "external_input_distribution", "representation"}
    lines = ["[simulation]"]
    for name, value in values.items():
        if name not in tables:
            lines.append(f"{name} = {json.dumps(value, ensure_ascii=False)}")
    for name in ("state_distribution", "external_input_distribution", "representation"):
        lines.append(f"[simulation.{name}]")
        lines.extend(f"{json.dumps(key, ensure_ascii=False)} = {json.dumps(value, ensure_ascii=False)}"
            for key, value in values[name].items())
    toml_path = tmp_path / "scenario.toml"
    toml_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    assert load_config(json_path) == load_config(toml_path) == resolve_config(raw)
    assert phase4_config_hash(resolve_phase4_options(load_config(json_path))) == phase4_config_hash(
        resolve_phase4_options(load_config(toml_path)))


@pytest.mark.parametrize("document", [
    '{"simulation":{"enabled":true,"enabled":false}}',
    '{"simulation":{"models":["closed_resampling"],"models":["reopened_resampling"]}}',
    '{"simulation":{"state_distribution":{"PRIVATE-state":0.4,"PRIVATE-state":1.0}}}',
])
def test_json_duplicate_declarations_fail_without_silently_overwriting_inputs(tmp_path, document):
    path = tmp_path / "scenario.json"
    path.write_text(document, encoding="utf-8")
    with pytest.raises(ConfigurationError) as failure:
        load_config(path)
    assert "PRIVATE" not in str(failure.value)


def test_normalized_hash_binds_every_scientific_and_protected_declaration():
    raw = declaration()
    baseline = phase4_config_hash(resolve_phase4_options(raw))
    reordered = {"simulation": dict(reversed(tuple(raw["simulation"].items())))}
    for name in ("state_distribution", "external_input_distribution", "representation"):
        reordered["simulation"][name] = dict(reversed(tuple(raw["simulation"][name].items())))
    assert phase4_config_hash(resolve_phase4_options(reordered)) == baseline
    for name, value in {
        "enabled": False, "seed": 38, "models": [CLOSED, REOPENED],
        "resample_size": 9, "simulation_horizon": 4, "simulation_replicates": 3,
        "reopening_weight": .5, "state_semantics": "different meaning",
        "scope_id": "different-scope", "dataset_version": "different-version",
        "state_distribution": {"PRIVATE-state": .25, "": .25, "é": .25, "e\u0301": .25},
        "external_input_distribution": {"PRIVATE-state": .5, "": 0., "é": .25, "e\u0301": .25},
    }.items():
        assert phase4_config_hash(resolve_phase4_options(declaration(**{name: value}))) != baseline, name
    for name in ("representation_name", "representation_source", "representation_version",
                 "binning_or_mapping_rule", "field_name", "missing_state_id"):
        changed = deepcopy(raw)
        changed["simulation"]["representation"][name] += "-changed"
        assert phase4_config_hash(resolve_phase4_options(changed)) != baseline, name
    changed = deepcopy(raw)
    changed["simulation"]["representation"]["normalization_profile"] = None
    assert phase4_config_hash(resolve_phase4_options(changed)) != baseline
    changed = deepcopy(raw)
    changed["simulation"]["representation"].update(missing_value_policy="error", missing_state_id=None)
    assert phase4_config_hash(resolve_phase4_options(changed)) != baseline
    relabeled = deepcopy(raw)
    for name in ("state_distribution", "external_input_distribution"):
        relabeled["simulation"][name]["PRIVATE-renamed"] = relabeled["simulation"][name].pop("PRIVATE-state")
    assert phase4_config_hash(resolve_phase4_options(relabeled)) != baseline


def test_explicit_activation_and_disabled_legacy_behavior():
    ordinary = resolve_phase4_options()
    disabled = resolve_phase4_options({"simulation": {"enabled": False}})
    assert phase4_config_hash(disabled) == phase4_config_hash(ordinary)
    assert phase4_config_summary(disabled)["scenario_requested"] is False
    for raw in ({"simulation": {"enabled": False, "seed": 37}}, declaration(enabled=False)):
        options = resolve_phase4_options(raw)
        assert capability(options.configuration.simulation).status is CapabilityStatus.UNAVAILABLE
        assert phase4_config_summary(options)["scenario_requested"] is False
    implicit = declaration()
    implicit["simulation"].pop("enabled")
    assert not resolve_phase4_options(implicit).configuration.simulation.enabled
    flagged = resolve_phase4_options(implicit, cli={"simulate": True})
    assert flagged.configuration.simulation.enabled
    assert phase4_config_hash(flagged) == phase4_config_hash(resolve_phase4_options(declaration()))
    with pytest.raises(ConfigurationError):
        resolve_phase4_options(declaration(enabled=False), cli={"simulate": True})
    with pytest.raises(ConfigurationError):
        resolve_phase4_options(cli={"simulate": True})


def test_activation_requires_each_scientific_declaration_but_validate_is_inert():
    required = ("seed", "models", "state_distribution", "resample_size", "simulation_horizon",
        "simulation_replicates", "representation", "state_semantics", "scope_id", "dataset_version")
    for name in required:
        incomplete = declaration()
        incomplete["simulation"].pop(name)
        with pytest.raises(ConfigurationError):
            resolve_phase4_options(incomplete)
    legacy = {"simulation": {"enabled": True, "seed": 37}}
    validated = resolve_phase4_options(legacy, operation="validate")
    assert capability(validated.configuration.simulation).status is CapabilityStatus.UNAVAILABLE
    complete = resolve_phase4_options(declaration(), operation="validate")
    eligible = capability(complete.configuration.simulation)
    assert eligible.status is CapabilityStatus.EXPERIMENTAL
    assert "R_SCENARIO_EXECUTION_DEFERRED" in eligible.reason_codes
    with pytest.raises(ConfigurationError):
        resolve_phase4_options(declaration(), cli={"simulate": True}, operation="validate")


@pytest.mark.parametrize("field,value", [
    ("seed", True), ("seed", -1), ("seed", 2 ** 53),
    ("resample_size", 0), ("resample_size", 2 ** 31), ("resample_size", 2.),
    ("simulation_horizon", -1), ("simulation_horizon", 10001),
    ("simulation_replicates", False), ("simulation_replicates", 10001),
    ("models", []), ("models", [CLOSED, CLOSED]), ("models", ["unknown"]),
    ("reopening_weight", True), ("reopening_weight", float("inf")),
    ("reopening_weight", -.1), ("state_distribution", {"a": True}),
    ("state_distribution", {"a": float("nan")}),
    ("state_distribution", {"a": .5, "b": .5 + 1.5e-12}),
    ("state_distribution", {"a\x00b": 1.}), ("state_distribution", {"\ud800": 1.}),
    ("external_input_distribution", {"different": 1.}),
    ("state_semantics", " "), ("scope_id", ""), ("dataset_version", ""),
    ("dataset_version", " v1"), ("dataset_version", "v::1"), ("dataset_version", "v" * 257),
])
def test_invalid_explicit_declarations_fail_before_execution(field, value):
    with pytest.raises(ConfigurationError):
        resolve_phase4_options(declaration(**{field: value}))


def test_exact_admission_bounds_and_combined_budget_are_shared_by_eligibility():
    boundary = declaration(seed=2 ** 53 - 1, resample_size=2 ** 31 - 1,
        simulation_horizon=0, simulation_replicates=10000)
    assert capability(resolve_phase4_options(boundary).configuration.simulation).status is CapabilityStatus.EXPERIMENTAL
    closed = declaration(models=[CLOSED], simulation_horizon=9999, simulation_replicates=25)
    closed["simulation"].pop("external_input_distribution")
    closed["simulation"].pop("reopening_weight")
    assert capability(resolve_phase4_options(closed).configuration.simulation).status is CapabilityStatus.EXPERIMENTAL
    # Four states * 10,000 generations * 25 replicates fits one million cells;
    # adding the second selected model would exceed the common admission bound.
    with pytest.raises(ConfigurationError):
        resolve_phase4_options(declaration(simulation_horizon=9999, simulation_replicates=25))
    with pytest.raises(ConfigurationError):
        resolve_phase4_options(declaration(state_distribution={str(i): 1 / 8192 for i in range(8192)},
            external_input_distribution={str(i): 1 / 8192 for i in range(8192)}))
    maximal_states = {str(i): 1 / 4096 for i in range(4096)}
    accepted = resolve_phase4_options(declaration(state_distribution=maximal_states,
        external_input_distribution=maximal_states, simulation_horizon=0, simulation_replicates=1))
    assert capability(accepted.configuration.simulation).status is CapabilityStatus.EXPERIMENTAL


def test_tolerated_mass_residual_is_preserved_without_input_layer_normalization():
    supplied = {"": .5, "literal": .5 + 5e-13}
    scenario = resolve_phase4_options(declaration(seed=0, resample_size=1,
        simulation_horizon=0, simulation_replicates=1,
        state_distribution=supplied, external_input_distribution={"": 0., "literal": 1.})).configuration.simulation
    assert dict(scenario.state_distribution) == supplied
    assert sum(dict(scenario.state_distribution).values()) != 1.
    assert capability(scenario).status is CapabilityStatus.EXPERIMENTAL


def test_reopening_inputs_are_required_exactly_for_selected_reopened_model():
    for name in ("external_input_distribution", "reopening_weight"):
        missing = declaration()
        missing["simulation"].pop(name)
        with pytest.raises(ConfigurationError):
            resolve_phase4_options(missing)
    with pytest.raises(ConfigurationError):
        resolve_phase4_options(declaration(models=[CLOSED]))
    only_reopened = resolve_phase4_options(declaration(models=[REOPENED]))
    assert capability(only_reopened.configuration.simulation).status is CapabilityStatus.EXPERIMENTAL
    for name, value in (("random_seed", 37), ("steps", 3), ("probabilities", {"a": 1.})):
        with pytest.raises(ConfigurationError):
            resolve_config(declaration(**{name: value}))


def test_legacy_input_eligibility_uses_literal_states_absolute_mass_and_execution_bounds():
    parameters = ScenarioParameters(CLOSED, 8, 0, 1, (("", .5), ("e\u0301", .25), ("é", .25)))
    assert capability(ScenarioConfig(True, 37), parameters).status is CapabilityStatus.EXPERIMENTAL
    for seed in (-1, 2 ** 53):
        assert capability(ScenarioConfig(True, seed), parameters).status is CapabilityStatus.UNAVAILABLE
    for name, value in {
        "state_distribution": (("", .5), ("é", .5 + 1.5e-12)),
        "resample_size": 2 ** 31, "simulation_horizon": 10001,
        "simulation_replicates": 10001,
    }.items():
        assert capability(ScenarioConfig(True, 37), replace(parameters, **{name: value})).status is CapabilityStatus.UNAVAILABLE
    oversized = replace(parameters, simulation_horizon=9999, simulation_replicates=34)
    assert capability(ScenarioConfig(True, 37), oversized).status is CapabilityStatus.UNAVAILABLE


def test_forged_model_objects_are_rejected_without_calling_their_equality():
    class UnsafeModel:
        def __eq__(self, other):
            raise AssertionError("untrusted model equality was executed")

    scenario = replace(resolve_config(declaration()).simulation, models=(UnsafeModel(),))
    assert config_module.scenario_config_reasons(scenario) == ("R_SCENARIO_PARAMETERS_INVALID",)
    with pytest.raises(ConfigurationError):
        config_module.config_scenario_parameters(scenario)
    forged = replace(resolve_config(declaration()), simulation=scenario)
    with pytest.raises(ConfigurationError):
        resolve_phase4_options(forged)


def test_schema_exposes_full_declarations_without_accepting_competing_vocabulary(repo_root):
    schema = json.loads((repo_root / "schemas/config.schema.json").read_text())
    validator = jsonschema.Draft202012Validator(schema)
    for raw in (declaration(), declaration(enabled=False), {"simulation": {"enabled": False, "seed": 0}}):
        validator.validate(raw)
    for raw in (declaration(models=[CLOSED, CLOSED]), declaration(seed=True),
            declaration(seed=2 ** 53), declaration(steps=2)):
        assert list(validator.iter_errors(raw))


def test_input_configuration_and_eligibility_never_import_numerical_owner(subprocess_env):
    source = r'''
import builtins, json, sys
original = builtins.__import__
def guarded(name, *args, **kwargs):
    if any(part in name.split(".") for part in ("metrics", "numpy")):
        raise AssertionError("input declarations imported numerical execution")
    return original(name, *args, **kwargs)
builtins.__import__ = guarded
from recursive_integrity_toolkit.config import resolve_phase4_options, phase4_validation_configuration
from recursive_integrity_toolkit.observability.levels import classify_observability
from recursive_integrity_toolkit.models import CanonicalRow, CapabilityKey, CapabilityStatus, RecordKey
from types import MappingProxyType
options = resolve_phase4_options(json.load(sys.stdin), operation="validate")
assert phase4_validation_configuration(options)["simulation"]["enabled"] is True
values = {"dataset_version": "audit-v1", "record_id": "observed", "content": "synthetic"}
records = (CanonicalRow("records", RecordKey("audit-v1", "observed"),
    MappingProxyType(values), MappingProxyType({}), MappingProxyType({})),)
result = classify_observability(records, scenario=options.configuration.simulation)
capability = result.capabilities[CapabilityKey.INTERVENTION_SIMULATION]
assert capability.status is CapabilityStatus.EXPERIMENTAL
assert "R_SCENARIO_EXECUTION_DEFERRED" in capability.reason_codes
assert "recursive_integrity_toolkit.metrics.resampling" not in sys.modules
assert "numpy" not in sys.modules
'''
    completed = subprocess.run([sys.executable, "-c", source], input=json.dumps(declaration()),
        text=True, capture_output=True, env=subprocess_env, timeout=30)
    assert completed.returncode == 0, completed.stderr
