"""Inert lineage declarations, exact resource domains and invocation provenance."""

from dataclasses import replace
import json
from pathlib import Path

import pytest

from recursive_integrity_toolkit.config import (
    ResourceLimits,
    load_phase4_invocation,
    phase4_config_hash,
    phase4_config_summary,
    phase4_pair_requested,
    phase4_validation_configuration,
    resolve_config,
    resolve_phase4_options,
)
from recursive_integrity_toolkit.errors import ConfigurationError
from recursive_integrity_toolkit.lineage.graph import LineageLimits
from recursive_integrity_toolkit.models import FileRole


LIMITS = {
    "max_lineage_nodes": ("max_nodes", 200000),
    "max_lineage_edges": ("max_edges", 1000000),
    "max_lineage_root_memberships": ("max_root_memberships", 1000000),
    "max_lineage_root_union_visits": ("max_root_union_visits", 10000000),
}


def test_lineage_resolution_is_inert_and_preserves_existing_multiple_roles(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("resolving declarations must not open inputs or run lineage")

    monkeypatch.setattr(Path, "open", forbidden)
    monkeypatch.setattr("recursive_integrity_toolkit.lineage.ancestry.analyze_lineage", forbidden)
    config = resolve_config({
        "lineage": True,
        "inputs": {
            role: ["PRIVATE-one.jsonl", "PRIVATE-two.jsonl"]
            for role in ("lineage_context", "records_compare", "external_reference", "embedding_data")
        },
    })
    assert config.lineage is True
    assert len(config.inputs) == 8
    options = resolve_phase4_options({"lineage": True, "inputs": {"lineage_context": ["PRIVATE-a.jsonl", "PRIVATE-b.csv"]}})
    assert options.lineage and not phase4_pair_requested(options, operation="audit")
    assert "PRIVATE" not in repr(options)
    assert "PRIVATE" not in json.dumps(phase4_config_summary(options))
    assert phase4_config_summary(options)["lineage_requested"] is True


def test_graph_defaults_match_kernel_and_remain_independent_of_input_limits():
    config = resolve_config({})
    assert config.lineage is False
    assert config.resource_limits.max_rows is None
    for name, (graph_name, expected) in LIMITS.items():
        assert getattr(config.resource_limits, name) == expected
        assert getattr(LineageLimits(), graph_name) == expected
    assert resolve_config({"resource_limits": {"max_rows": None}}).resource_limits.max_rows is None


@pytest.mark.parametrize("value", [None, True, False, 0, -1, 1.5, float("inf"), "10"])
def test_each_lineage_limit_requires_an_explicit_positive_integer(value):
    for name in LIMITS:
        with pytest.raises(ConfigurationError):
            resolve_config({"resource_limits": {name: value}})


def test_graph_limits_round_trip_and_forged_declarations_fail_validation():
    configured = resolve_config({"lineage": True, "resource_limits": {name: 7 for name in LIMITS}})
    options = resolve_phase4_options(configured)
    detached = phase4_validation_configuration(options)
    assert detached["lineage"] is True
    assert all(detached["resource_limits"][name] == 7 for name in LIMITS)
    assert resolve_config(detached).resource_limits == configured.resource_limits
    with pytest.raises(ConfigurationError):
        resolve_phase4_options(replace(configured, resource_limits=ResourceLimits(max_lineage_nodes=None)))


def test_effective_lineage_context_and_limit_changes_affect_hash():
    ordinary = resolve_phase4_options()
    disabled = resolve_phase4_options({"lineage": False, "resource_limits": {name: default for name, (_, default) in LIMITS.items()}})
    assert phase4_config_hash(ordinary) == phase4_config_hash(disabled)
    assert phase4_config_summary(ordinary) == phase4_config_summary(disabled)
    cli_enabled = resolve_phase4_options(cli={"lineage": True})
    config_enabled = resolve_phase4_options({"lineage": True})
    baseline = phase4_config_hash(config_enabled)
    assert baseline == phase4_config_hash(cli_enabled)
    assert baseline != phase4_config_hash(ordinary)
    for name in LIMITS:
        assert baseline != phase4_config_hash(resolve_phase4_options({"lineage": True, "resource_limits": {name: 7}}))
    assert baseline != phase4_config_hash(resolve_phase4_options(cli={"lineage": True, "lineage_records": ["ancestor.csv"]}))


@pytest.mark.parametrize("value", [None, 0, 1, "true", []])
def test_lineage_config_rejects_nonboolean_requests(value):
    with pytest.raises(ConfigurationError):
        resolve_config({"lineage": value})


def test_explicit_lineage_declarations_obey_existing_conflict_policy():
    for value in (True, False):
        with pytest.raises(ConfigurationError, match="compete"):
            resolve_phase4_options({"lineage": value}, cli={"lineage": True})
    with pytest.raises(ConfigurationError):
        resolve_phase4_options(cli={"lineage": 1})
    with pytest.raises(ConfigurationError):
        resolve_phase4_options(cli={"lineage_records": "ancestor.csv"})


def test_input_only_validation_accepts_context_and_rejects_lineage_execution():
    contexts = resolve_phase4_options(cli={"lineage_records": ["a.csv", "b.jsonl"]})
    assert not phase4_pair_requested(contexts, operation="validate")
    assert [source.role for source in contexts.inputs] == [FileRole.LINEAGE_CONTEXT] * 2
    for options in (resolve_phase4_options({"lineage": True}), resolve_phase4_options(cli={"lineage": True})):
        with pytest.raises(ConfigurationError, match="cannot request calculations"):
            phase4_pair_requested(options, operation="validate")


def test_mixed_context_paths_preserve_each_declarations_base(tmp_path):
    config_directory = tmp_path / "settings"
    config_directory.mkdir()
    config_path = config_directory / "audit.json"
    config_path.write_text(json.dumps({"lineage": True, "inputs": {"lineage_context": ["shared.jsonl", "configured.csv"]}}))
    options, inventory = load_phase4_invocation(
        config_path=config_path, base_directory=tmp_path,
        cli={"records": "target.csv", "lineage_records": ["shared.jsonl", "invoked.csv"]},
    )
    assert len(inventory) == 1
    contexts = {source.path for source in options.inputs if source.role is FileRole.LINEAGE_CONTEXT}
    assert contexts == {config_directory / "shared.jsonl", config_directory / "configured.csv", tmp_path / "shared.jsonl", tmp_path / "invoked.csv"}
    assert next(source.path for source in options.inputs if source.role is FileRole.RECORDS_PRIMARY) == tmp_path / "target.csv"


def test_config_schema_admits_contexts_and_matches_new_resource_domains():
    import jsonschema

    schema = json.loads((Path(__file__).parents[2] / "schemas/config.schema.json").read_text())
    validator = jsonschema.Draft202012Validator(schema)
    validator.validate({"lineage": True, "inputs": {"lineage_context": ["a.csv", "b.jsonl"]}, "resource_limits": {name: 7 for name in LIMITS}})
    for name in LIMITS:
        for invalid in (None, True, 0, -1, 1.5):
            assert list(validator.iter_errors({"resource_limits": {name: invalid}}))

