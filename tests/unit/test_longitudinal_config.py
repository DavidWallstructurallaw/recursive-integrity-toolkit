"""Inert series declarations, invocation conflicts and normalized identity."""

import builtins
from copy import deepcopy
from dataclasses import FrozenInstanceError, replace
import json
from pathlib import Path

import jsonschema
import pytest

from recursive_integrity_toolkit.config import (
    LongitudinalOptions, ResourceLimits, load_config, load_phase4_invocation,
    phase4_config_hash, phase4_config_summary, phase4_pair_requested,
    phase4_validation_configuration, resolve_config, resolve_phase4_options,
)
from recursive_integrity_toolkit.errors import ConfigurationError
from recursive_integrity_toolkit.models import FileRole


REPRESENTATION = {"name": "PRIVATE-topic", "source": "topic_field", "field": "topic",
                  "version": "taxonomy-1", "missing_value_policy": "error"}
DESCRIPTOR = {"representation_name": "PRIVATE-topic", "representation_source": "topic_field",
              "representation_version": "taxonomy-1", "binning_or_mapping_rule": "literal_field_value",
              "field_name": "topic", "missing_value_policy": "error", "missing_state_id": None,
              "normalization_profile": None}
MAPPING = {"earlier_version": "v1", "later_version": "v2", "declaration": {
    "direction": "earlier_to_later", "source_representation": DESCRIPTOR,
    "target_representation": DESCRIPTOR, "source_state_semantics": "PRIVATE-meaning",
    "target_state_semantics": "PRIVATE-meaning", "state_mapping": {"PRIVATE-state": "PRIVATE-target", "": ""}}}


def common(**changes):
    data = {"representation": deepcopy(REPRESENTATION),
            "longitudinal": {"enabled": True, "state_semantics": "PRIVATE-meaning"}}
    data["longitudinal"].update(changes)
    return data


def heterogeneous(**changes):
    data = {"longitudinal": {"enabled": True, "versions": [
        {"dataset_version": version, "representation": deepcopy(REPRESENTATION),
         "state_semantics": "PRIVATE-meaning"} for version in ("v1", "v2")],
        "mappings": [deepcopy(MAPPING)]}}
    data["longitudinal"].update(changes)
    return data


def validator():
    return jsonschema.Draft202012Validator(json.loads(
        (Path(__file__).parents[2] / "schemas/config.schema.json").read_text()))


def test_resolution_is_inert_without_analytical_import_or_file_read(monkeypatch):
    original_import = builtins.__import__

    def guarded(name, *args, **kwargs):
        if any(part in name.split(".") for part in ("metrics", "representations", "lineage", "reports", "simulations")):
            raise AssertionError("input configuration must not import analytical modules")
        return original_import(name, *args, **kwargs)

    def forbidden(*args, **kwargs):
        raise AssertionError("declarations must not open an input or secret")

    monkeypatch.setattr(builtins, "__import__", guarded)
    monkeypatch.setattr(Path, "open", forbidden)
    data = heterogeneous()
    config = resolve_config(data)
    options = resolve_phase4_options(config)
    assert config.longitudinal.enabled
    assert options.longitudinal == config.longitudinal
    assert config.resource_limits.max_longitudinal_versions == 100
    assert not phase4_pair_requested(options, operation="audit")


def test_mapping_and_version_declarations_are_detached_immutable_and_private():
    data = heterogeneous()
    config = resolve_config(data)
    mapping = config.longitudinal.mappings[0]
    data["longitudinal"]["mappings"][0]["declaration"]["state_mapping"]["PRIVATE-state"] = "changed"
    data["longitudinal"]["versions"][0]["representation"]["name"] = "changed"
    assert mapping.declaration.state_mapping["PRIVATE-state"] == "PRIVATE-target"
    assert config.longitudinal.versions[0].representation.name == "PRIVATE-topic"
    with pytest.raises(TypeError):
        mapping.declaration.state_mapping["x"] = "y"
    with pytest.raises(FrozenInstanceError):
        mapping.earlier_version = "new"
    options = resolve_phase4_options(config)
    assert "PRIVATE" not in repr(options)
    assert "PRIVATE" not in repr(config.longitudinal)
    assert "PRIVATE" not in json.dumps(phase4_config_summary(options))


@pytest.mark.parametrize("value", [None, False, True, 0, -1, 1.5, float("inf"), float("nan"), "3"])
def test_selected_version_limit_requires_exact_positive_integer(value):
    with pytest.raises(ConfigurationError):
        resolve_config({"resource_limits": {"max_longitudinal_versions": value}})


def test_resource_limit_round_trip_and_forged_resource_rejection():
    config = resolve_config({"resource_limits": {"max_longitudinal_versions": 7}})
    assert config.resource_limits.max_longitudinal_versions == 7
    options = resolve_phase4_options(config)
    assert resolve_config(phase4_validation_configuration(options)).resource_limits == config.resource_limits
    with pytest.raises(ConfigurationError):
        resolve_phase4_options(replace(config, resource_limits=ResourceLimits(max_longitudinal_versions=True)))


@pytest.mark.parametrize("value", [None, True, [], "https://example.invalid/config", {"unknown": 1},
    {"enabled": 1}, {"enabled": None}, {"baseline": "latest"}, {"baseline": None},
    {"state_semantics": None}, {"state_semantics": ""}, {"state_semantics": "  "},
    {"versions": {}}, {"versions": None}, {"mappings": {}}, {"mappings": "mapping.json"}])
def test_longitudinal_object_rejects_wrong_shapes(value):
    with pytest.raises(ConfigurationError):
        resolve_config({"longitudinal": value})


@pytest.mark.parametrize("changes", [{"baseline": "first"}, {"state_semantics": "literal"},
    {"versions": heterogeneous()["longitudinal"]["versions"]}, {"mappings": [MAPPING]}])
def test_disabled_declarations_remain_inert_but_audit_requires_enablement(changes):
    data = {"longitudinal": changes}
    assert resolve_config(data).longitudinal.enabled is False
    with pytest.raises(ConfigurationError, match="enablement"):
        resolve_phase4_options(data)
    options = resolve_phase4_options(data, operation="validate")
    assert not phase4_pair_requested(options, operation="validate")


def test_validate_config_enablement_is_inert_and_accepts_multiple_comparisons():
    data = common()
    options = resolve_phase4_options(data, operation="validate", cli={"compare": ["a.jsonl", "b.csv"]})
    assert options.longitudinal.enabled
    assert not phase4_pair_requested(options, operation="validate")
    assert len([source for source in options.inputs if source.role is FileRole.RECORDS_COMPARE]) == 2


@pytest.mark.parametrize("cli", [{"longitudinal": True}, {"longitudinal": False}, {"baseline": "none"},
                               {"state_semantics": "literal"}])
def test_validate_rejects_explicit_execution_options(cli):
    with pytest.raises(ConfigurationError, match="cannot request calculations"):
        resolve_phase4_options(operation="validate", cli=cli)


@pytest.mark.parametrize("declared,invoked", [({"enabled": True}, {"longitudinal": True}),
    ({"enabled": False}, {"longitudinal": True}), ({"baseline": "none"}, {"baseline": "none"}),
    ({"state_semantics": "same"}, {"state_semantics": "same"})])
def test_same_singleton_competes_even_when_equal(declared, invoked):
    with pytest.raises(ConfigurationError, match="compete"):
        resolve_phase4_options({"longitudinal": declared}, cli=invoked)


@pytest.mark.parametrize("cli", [{"baseline": "none"}, {"baseline": "first"}, {"longitudinal": 1}])
def test_baseline_requires_series_and_enablement_requires_boolean(cli):
    with pytest.raises(ConfigurationError):
        resolve_phase4_options(cli=cli)


def test_comparison_cardinality_preserves_ordinary_pair_and_source_conflicts():
    for cli in ({"compare": ["a.csv", "b.csv"]},):
        with pytest.raises(ConfigurationError):
            resolve_phase4_options(cli=cli)
        assert len(resolve_phase4_options(cli=cli, operation="validate").inputs) == 2
        assert len(resolve_phase4_options(common(), cli=cli).inputs) == 2
    data = common()
    data["inputs"] = {"records_compare": ["a.csv", "b.csv"]}
    assert len(resolve_phase4_options(data).inputs) == 2
    with pytest.raises(ConfigurationError, match="compete"):
        resolve_phase4_options(data, cli={"compare": ["c.csv"]})
    ordinary = resolve_phase4_options(cli={"compare": ["one.csv"], "state_semantics": "meaning"})
    assert phase4_pair_requested(ordinary, operation="audit")


@pytest.mark.parametrize("field,value", [("dataset_version", " v1"), ("dataset_version", "v::1"),
    ("dataset_version", ""), ("representation", None), ("state_semantics", ""),
    ("missing_state_id", "orphan"), ("missing_state_id", None), ("empty_scope", True)])
def test_per_version_rejects_invalid_identity_missing_policy_and_python_only_flags(field, value):
    data = heterogeneous()
    data["longitudinal"]["versions"][0][field] = value
    with pytest.raises(ConfigurationError):
        resolve_config(data)


def test_per_version_missing_marker_supported_sources_and_mixed_modes():
    data = heterogeneous()
    row = data["longitudinal"]["versions"][0]
    row["representation"]["missing_value_policy"] = "explicit_missing_state"
    with pytest.raises(ConfigurationError):
        resolve_config(data)
    row["missing_state_id"] = "PRIVATE-missing"
    assert resolve_config(data).longitudinal.versions[0].missing_state_id == "PRIVATE-missing"
    validator().validate(data)
    row["representation"]["source"] = "python.callback"
    with pytest.raises(ConfigurationError):
        resolve_config(data)
    for common_field in ("state_semantics", "missing_state_id"):
        with pytest.raises(ConfigurationError, match="compete"):
            resolve_phase4_options(heterogeneous(), cli={common_field: "literal"})
    data = heterogeneous()
    data["representation"] = REPRESENTATION
    with pytest.raises(ConfigurationError, match="compete"):
        resolve_config(data)
    with pytest.raises(ConfigurationError, match="compete"):
        resolve_config(heterogeneous(state_semantics="literal"))


def test_per_version_exact_content_keeps_existing_profile_contract():
    data = heterogeneous(mappings=[])
    row = data["longitudinal"]["versions"][0]
    row["representation"] = {"name": "content", "source": "content_hash", "version": "1",
                             "normalization_profile": "exact_utf8_v1"}
    assert resolve_config(data).longitudinal.versions[0].representation.source == "content_hash"
    row["representation"]["normalization_profile"] = "arbitrary"
    with pytest.raises(ConfigurationError):
        resolve_config(data)


def test_duplicate_versions_pairs_and_legacy_maps_are_rejected():
    for key in ("versions", "mappings"):
        data = heterogeneous()
        data["longitudinal"][key].append(deepcopy(data["longitudinal"][key][0]))
        with pytest.raises(ConfigurationError, match="unique"):
            resolve_config(data)
    for key in ("state_mapping", "representation_compatibility"):
        data = common()
        data[key] = {"x": "y"}
        with pytest.raises(ConfigurationError):
            resolve_config(data)


@pytest.mark.parametrize("key", list(DESCRIPTOR))
def test_mapping_descriptor_requires_all_eight_fields(key):
    data = heterogeneous()
    del data["longitudinal"]["mappings"][0]["declaration"]["source_representation"][key]
    with pytest.raises(ConfigurationError):
        resolve_config(data)
    assert list(validator().iter_errors(data))


@pytest.mark.parametrize("key,value", [("direction", "forward"), ("source_state_semantics", ""),
    ("state_mapping", "https://example.invalid/map.json"), ("state_mapping", "package.function"),
    ("state_mapping", {"a": ["b", "c"]}), ("state_mapping", {"a": None}),
    ("state_mapping", {"a": lambda value: value})])
def test_mapping_accepts_literal_dictionary_only(key, value):
    data = heterogeneous()
    data["longitudinal"]["mappings"][0]["declaration"][key] = value
    with pytest.raises(ConfigurationError):
        resolve_config(data)


def test_normalized_hash_preserves_ordinary_identity_and_binds_series_options():
    ordinary = phase4_config_hash(resolve_phase4_options())
    assert ordinary == "b1a13095d612c99d736316f0e618b2bf68281b814bb5ddaa3d71c3cd91beb49d"
    assert ordinary == phase4_config_hash(resolve_phase4_options({"longitudinal": {},
        "resource_limits": {"max_longitudinal_versions": 100}}))
    configured = resolve_phase4_options(common())
    invoked = resolve_phase4_options({"representation": REPRESENTATION},
                                    cli={"longitudinal": True, "state_semantics": "PRIVATE-meaning"})
    baseline = phase4_config_hash(configured)
    assert baseline == phase4_config_hash(invoked)
    assert baseline != ordinary
    assert baseline != phase4_config_hash(resolve_phase4_options(common(baseline="first")))
    assert baseline != phase4_config_hash(resolve_phase4_options(common(state_semantics="different")))
    limited = common()
    limited["resource_limits"] = {"max_longitudinal_versions": 7}
    assert baseline != phase4_config_hash(resolve_phase4_options(limited))
    mapped = heterogeneous()
    before = phase4_config_hash(resolve_phase4_options(mapped))
    mapped["longitudinal"]["mappings"][0]["declaration"]["state_mapping"]["PRIVATE-state"] = "different"
    assert before != phase4_config_hash(resolve_phase4_options(mapped))


def test_detached_validation_configuration_round_trips_full_declarations():
    options = resolve_phase4_options(heterogeneous(), cli={"baseline": "first"})
    detached = phase4_validation_configuration(options)
    assert resolve_config(detached).longitudinal == options.longitudinal
    assert detached["version_order"] == []
    assert len(detached["longitudinal"]["mappings"][0]["declaration"]["source_representation"]) == 8
    detached["longitudinal"]["mappings"][0]["declaration"]["state_mapping"]["PRIVATE-state"] = "tampered"
    assert options.longitudinal.mappings[0].declaration.state_mapping["PRIVATE-state"] == "PRIVATE-target"


def test_json_toml_and_relative_comparison_sources(tmp_path):
    folder = tmp_path / "settings"
    folder.mkdir()
    data = common()
    data["inputs"] = {"records_primary": "latest.jsonl", "records_compare": ["a.csv", "b.csv"]}
    path = folder / "config.json"
    path.write_text(json.dumps(data))
    assert load_config(path).longitudinal.enabled
    options, inventory = load_phase4_invocation(config_path=path, cli={}, base_directory=tmp_path)
    assert len(inventory) == 1
    assert {source.path for source in options.inputs} == {folder / item for item in ("latest.jsonl", "a.csv", "b.csv")}
    assert options.version_order == ()
    toml = folder / "config.toml"
    toml.write_text('[longitudinal]\nenabled = true\nbaseline = "first"\nstate_semantics = "literal"\n[resource_limits]\nmax_longitudinal_versions = 5\n')
    assert load_config(toml).longitudinal.baseline == "first"
    assert load_config(toml).resource_limits.max_longitudinal_versions == 5


def test_schema_accepts_structural_modes_and_rejects_unknown_properties():
    for data in (common(), heterogeneous(), {"longitudinal": {}}, {"resource_limits": {"max_longitudinal_versions": 1}}):
        validator().validate(data)
    for data in ({"longitudinal": {"mappings_url": "https://example.invalid"}},
                 {"longitudinal": {"enabled": 1}}, {"resource_limits": {"max_longitudinal_versions": True}},
                 heterogeneous(state_semantics="conflict")):
        assert list(validator().iter_errors(data))
