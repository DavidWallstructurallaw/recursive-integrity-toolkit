"""Resolve Phase 2 local configuration into immutable project-owned contracts.

Owner IDs:
    PR-007, PR-010, PR-011, PR-016 supporting infrastructure, PR-017

Inputs:
    Explicit JSON or TOML configuration values and local input declarations.

Outputs:
    Immutable ``ResolvedConfig`` objects that preserve user declarations without inference.

Assumptions:
    Version order, representation choice, privacy mode, strict-mode promotion, and scenario
    declarations are explicit. Configuration never activates analysis at import time.

Limits:
    No file ingestion, version-order inference, metric, lineage, simulation, report assembly,
    configuration hash, or remote access is implemented here.

Current phase status:
    Phase 2 Step 1 configuration contracts and local parsing. No analytical behavior.
"""

from __future__ import annotations

import json
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from .errors import ConfigurationError, ErrorCode
from .models import FileFormat, FileRole, InputSource, PrivacyMode


_ALLOWED_TOP_LEVEL = {
    "config_version",
    "inputs",
    "representation",
    "representation_compatibility",
    "state_mapping",
    "version_order",
    "privacy_mode",
    "strict_mode",
    "strict_warning_codes",
    "resource_limits",
    "output",
    "simulation",
}

_MULTI_ROLES = {
    FileRole.RECORDS_COMPARE,
    FileRole.EMBEDDING_DATA,
    FileRole.EXTERNAL_REFERENCE,
}


@dataclass(frozen=True, slots=True)
class RepresentationConfig:
    name: str | None = None
    source: str | None = None
    field: str | None = None
    version: str | None = None
    missing_value_policy: str | None = None
    normalization_profile: str | None = None


@dataclass(frozen=True, slots=True)
class ResourceLimits:
    max_file_bytes: int | None = None
    max_rows: int | None = None
    max_content_bytes: int | None = None
    max_parent_list_length: int | None = None
    max_json_depth: int | None = None


@dataclass(frozen=True, slots=True)
class ScenarioConfig:
    enabled: bool = False
    seed: int | None = None


@dataclass(frozen=True, slots=True)
class ResolvedConfig:
    config_version: str | None = None
    inputs: tuple[InputSource, ...] = ()
    representation: RepresentationConfig | None = None
    representation_compatibility: tuple[tuple[str, str], ...] = ()
    state_mapping: tuple[tuple[str, str], ...] = ()
    version_order: tuple[str, ...] = ()
    privacy_mode: PrivacyMode = PrivacyMode.STANDARD
    strict_mode: bool = False
    strict_warning_codes: tuple[str, ...] = ()
    resource_limits: ResourceLimits = ResourceLimits()
    output: tuple[tuple[str, Any], ...] = ()
    simulation: ScenarioConfig = ScenarioConfig()


def load_config(path: str | Path) -> ResolvedConfig:
    """Load one explicit local JSON or TOML configuration file."""
    config_path = Path(path)
    suffix = config_path.suffix.lower()
    try:
        raw = config_path.read_bytes()
    except OSError as exc:
        raise ConfigurationError(ErrorCode.CONFIG_INVALID, "configuration file cannot be read") from exc

    try:
        if suffix == ".json":
            data = json.loads(raw.decode("utf-8"))
        elif suffix == ".toml":
            data = tomllib.loads(raw.decode("utf-8"))
        else:
            raise ConfigurationError(
                ErrorCode.CONFIG_INVALID,
                "configuration format must be JSON or TOML",
            )
    except UnicodeDecodeError as exc:
        raise ConfigurationError(ErrorCode.CONFIG_INVALID, "configuration must use UTF-8") from exc
    except (json.JSONDecodeError, tomllib.TOMLDecodeError) as exc:
        raise ConfigurationError(ErrorCode.CONFIG_INVALID, "configuration cannot be parsed") from exc

    if not isinstance(data, Mapping):
        raise ConfigurationError(ErrorCode.CONFIG_INVALID, "configuration root must be an object")
    return resolve_config(data)


def resolve_config(data: Mapping[str, Any]) -> ResolvedConfig:
    """Resolve approved Phase 2 configuration fields without inferring missing evidence."""
    unknown = sorted(set(data) - _ALLOWED_TOP_LEVEL)
    if unknown:
        raise ConfigurationError(
            ErrorCode.CONFIG_INVALID,
            f"unknown configuration fields: {', '.join(unknown)}",
        )

    config_version = _optional_string(data.get("config_version"), "config_version")
    inputs = _parse_inputs(data.get("inputs"))
    representation = _parse_representation(data.get("representation"))
    representation_compatibility = _string_mapping(
        data.get("representation_compatibility"),
        "representation_compatibility",
    )
    state_mapping = _string_mapping(data.get("state_mapping"), "state_mapping")
    version_order = _parse_version_order(data.get("version_order"))
    privacy_mode = _enum_value(
        PrivacyMode,
        data.get("privacy_mode", PrivacyMode.STANDARD.value),
        "privacy_mode",
    )
    strict_mode = _bool_value(data.get("strict_mode", False), "strict_mode")
    strict_warning_codes = _string_sequence(data.get("strict_warning_codes"), "strict_warning_codes")
    resource_limits = _parse_resource_limits(data.get("resource_limits"))
    output = _frozen_mapping(data.get("output"), "output")
    simulation = _parse_simulation(data.get("simulation"))

    return ResolvedConfig(
        config_version=config_version,
        inputs=inputs,
        representation=representation,
        representation_compatibility=representation_compatibility,
        state_mapping=state_mapping,
        version_order=version_order,
        privacy_mode=privacy_mode,
        strict_mode=strict_mode,
        strict_warning_codes=strict_warning_codes,
        resource_limits=resource_limits,
        output=output,
        simulation=simulation,
    )


def _parse_inputs(value: Any) -> tuple[InputSource, ...]:
    if value is None:
        return ()
    if not isinstance(value, Mapping):
        _invalid("inputs must be an object")
    sources: list[InputSource] = []
    for raw_role, raw_spec in value.items():
        role = _enum_value(FileRole, raw_role, "input role")
        entries = raw_spec if isinstance(raw_spec, list) else [raw_spec]
        if role not in _MULTI_ROLES and len(entries) > 1:
            _invalid(f"input role {role.value} accepts at most one declaration")
        for entry in entries:
            sources.append(_parse_input_source(role, entry))
    return tuple(sources)


def _parse_input_source(role: FileRole, value: Any) -> InputSource:
    if isinstance(value, str):
        path = value
        declared_format = None
    elif isinstance(value, Mapping):
        unknown = sorted(set(value) - {"path", "format"})
        if unknown:
            _invalid(f"input declaration has unknown fields: {', '.join(unknown)}")
        path = value.get("path")
        declared = value.get("format")
        declared_format = None if declared is None else _enum_value(FileFormat, declared, "input format")
    else:
        _invalid("input declaration must be a path string or object")
    if not isinstance(path, str) or not path:
        _invalid("input path must be a nonempty string")
    return InputSource(role=role, path=Path(path), declared_format=declared_format)


def _parse_representation(value: Any) -> RepresentationConfig | None:
    if value is None:
        return None
    if not isinstance(value, Mapping):
        _invalid("representation must be an object")
    allowed = {
        "name",
        "source",
        "field",
        "version",
        "missing_value_policy",
        "normalization_profile",
    }
    unknown = sorted(set(value) - allowed)
    if unknown:
        _invalid(f"representation has unknown fields: {', '.join(unknown)}")
    return RepresentationConfig(
        name=_optional_string(value.get("name"), "representation.name"),
        source=_optional_string(value.get("source"), "representation.source"),
        field=_optional_string(value.get("field"), "representation.field"),
        version=_optional_string(value.get("version"), "representation.version"),
        missing_value_policy=_optional_string(
            value.get("missing_value_policy"),
            "representation.missing_value_policy",
        ),
        normalization_profile=_optional_string(
            value.get("normalization_profile"),
            "representation.normalization_profile",
        ),
    )


def _parse_version_order(value: Any) -> tuple[str, ...]:
    if value is None:
        return ()
    values = _string_sequence(value, "version_order")
    if len(set(values)) != len(values):
        _invalid("version_order must not contain duplicates")
    return values


def _parse_resource_limits(value: Any) -> ResourceLimits:
    if value is None:
        return ResourceLimits()
    if not isinstance(value, Mapping):
        _invalid("resource_limits must be an object")
    allowed = {
        "max_file_bytes",
        "max_rows",
        "max_content_bytes",
        "max_parent_list_length",
        "max_json_depth",
    }
    unknown = sorted(set(value) - allowed)
    if unknown:
        _invalid(f"resource_limits has unknown fields: {', '.join(unknown)}")
    kwargs = {
        key: _optional_positive_int(value.get(key), f"resource_limits.{key}")
        for key in allowed
    }
    return ResourceLimits(**kwargs)


def _parse_simulation(value: Any) -> ScenarioConfig:
    if value is None:
        return ScenarioConfig()
    if not isinstance(value, Mapping):
        _invalid("simulation must be an object")
    unknown = sorted(set(value) - {"enabled", "seed"})
    if unknown:
        _invalid(f"simulation has unknown fields: {', '.join(unknown)}")
    enabled = _bool_value(value.get("enabled", False), "simulation.enabled")
    seed = value.get("seed")
    if seed is not None and (isinstance(seed, bool) or not isinstance(seed, int)):
        _invalid("simulation.seed must be an integer")
    return ScenarioConfig(enabled=enabled, seed=seed)


def _optional_string(value: Any, name: str) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str) or not value:
        _invalid(f"{name} must be a nonempty string")
    return value


def _string_sequence(value: Any, name: str) -> tuple[str, ...]:
    if value is None:
        return ()
    if not isinstance(value, list):
        _invalid(f"{name} must be an array")
    result: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item:
            _invalid(f"{name} items must be nonempty strings")
        result.append(item)
    return tuple(result)


def _string_mapping(value: Any, name: str) -> tuple[tuple[str, str], ...]:
    if value is None:
        return ()
    if not isinstance(value, Mapping):
        _invalid(f"{name} must be an object")
    result: list[tuple[str, str]] = []
    for key, item in value.items():
        if not isinstance(key, str) or not key or not isinstance(item, str):
            _invalid(f"{name} must map strings to strings")
        result.append((key, item))
    return tuple(sorted(result))


def _frozen_mapping(value: Any, name: str) -> tuple[tuple[str, Any], ...]:
    if value is None:
        return ()
    if not isinstance(value, Mapping):
        _invalid(f"{name} must be an object")
    return tuple(sorted(value.items(), key=lambda item: str(item[0])))


def _bool_value(value: Any, name: str) -> bool:
    if not isinstance(value, bool):
        _invalid(f"{name} must be a boolean")
    return value


def _optional_positive_int(value: Any, name: str) -> int | None:
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        _invalid(f"{name} must be a positive integer")
    return value


def _enum_value(enum_type, value: Any, name: str):
    if not isinstance(value, str):
        _invalid(f"{name} must be a string")
    try:
        return enum_type(value)
    except ValueError as exc:
        _invalid(f"{name} has an unsupported value")
        raise AssertionError from exc


def _invalid(message: str) -> None:
    raise ConfigurationError(ErrorCode.CONFIG_INVALID, message)
