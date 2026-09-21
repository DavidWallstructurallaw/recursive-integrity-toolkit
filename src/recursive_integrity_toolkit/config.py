"""Preserve Phase 2 configuration and add explicit inert Phase 4 report options.

Owner IDs:
    PR-007, PR-010, PR-011, PR-015, PR-016 supporting infrastructure, PR-017

Inputs:
    Explicit JSON or TOML configuration values and local input declarations.

Outputs:
    Immutable ``ResolvedConfig`` objects that preserve user declarations without
    inference; restricted Phase 4 options, safe summaries and normalized hashes.

Assumptions:
    Version order, representation choice, privacy mode, strict-mode promotion, and scenario
    declarations are explicit. Configuration never activates analysis at import time.

Limits:
    Phase 4 resolution performs no file ingestion, secret read, version-order
    inference, metric, lineage, simulation, report assembly or remote access.

Current phase status:
    Phase 4 Step 7 invocation adapter. Inherited parsers remain unchanged.
"""

from __future__ import annotations

import json
import math
import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping

from .errors import ConfigurationError, ErrorCode
from .models import FileFormat, FileRole, InputSource, PrivacyMode
from .utils.hashing import sha256_canonical
from .utils.paths import local_input_path


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


@dataclass(frozen=True, slots=True)
class Phase4Options:
    """Explicit inert report options; raw declarations are hidden from repr.

    Resolution does not read inputs, load a secret, perform calculations or
    activate a command. ``configuration`` retains the accepted Phase 2 contract.
    """

    configuration: ResolvedConfig = field(repr=False)
    inputs: tuple[InputSource, ...] = field(repr=False)
    directory: Path = field(repr=False)
    privacy_mode: str
    record_id_mode: str
    id_salt_file: Path | None = field(repr=False)
    strict_mode: bool
    version_order: tuple[str, ...] = field(repr=False)
    state_semantics: str | None = field(repr=False)
    missing_state_id: str | None = field(repr=False)
    tail_rule: str | None
    tail_threshold: int | float | None

    def __post_init__(self) -> None:
        if (type(self.configuration) is not ResolvedConfig or type(self.inputs) is not tuple
                or any(type(source) is not InputSource or type(source.role) is not FileRole
                       or not isinstance(source.path, Path) for source in self.inputs)
                or type(self.strict_mode) is not bool or type(self.privacy_mode) is not str
                or self.privacy_mode not in {"standard", "redacted"}
                or type(self.record_id_mode) is not str or self.record_id_mode not in {"preserve", "hash", "omit"}
                or not isinstance(self.directory, Path)
                or self.id_salt_file is not None and not isinstance(self.id_salt_file, Path)
                or type(self.version_order) is not tuple
                or any(type(value) is not str for value in self.version_order)
                or self.state_semantics is not None and type(self.state_semantics) is not str
                or self.missing_state_id is not None and type(self.missing_state_id) is not str):
            _invalid("Phase 4 options have invalid structural fields")
        if (self.tail_rule is not None and (type(self.tail_rule) is not str
                or self.tail_rule not in {"singleton_count", "count_at_or_below", "frequency_at_or_below"})
                or self.tail_rule in (None, "singleton_count") and self.tail_threshold is not None
                or self.tail_rule == "count_at_or_below" and (type(self.tail_threshold) is not int or self.tail_threshold < 0)
                or self.tail_rule == "frequency_at_or_below" and (type(self.tail_threshold) not in (int, float)
                    or not 0 <= self.tail_threshold <= 1)):
            _invalid("Phase 4 options have an invalid tail selection")


def _phase4_config_data(config: ResolvedConfig) -> dict[str, Any]:
    """Explicitly copy known declarations for validation and configuration hashing."""
    if type(config) is not ResolvedConfig or type(config.inputs) is not tuple:
        _invalid("Phase 4 configuration must use the accepted declaration contract")
    inputs: dict[str, Any] = {}
    for source in config.inputs:
        if (type(source) is not InputSource or type(source.role) is not FileRole
                or not isinstance(source.path, Path)
                or source.declared_format is not None and type(source.declared_format) is not FileFormat):
            _invalid("Phase 4 input declarations are invalid")
        entry = {"path": str(source.path)}
        if source.declared_format is not None:
            entry["format"] = source.declared_format.value
        if source.role.value in inputs:
            if source.role not in _MULTI_ROLES:
                _invalid("Phase 4 singleton input declarations compete")
            prior = inputs[source.role.value]
            inputs[source.role.value] = prior + [entry] if type(prior) is list else [prior, entry]
        else:
            inputs[source.role.value] = entry
    representation = config.representation
    if representation is not None and type(representation) is not RepresentationConfig:
        _invalid("Phase 4 representation declaration is invalid")
    if type(config.resource_limits) is not ResourceLimits or type(config.simulation) is not ScenarioConfig:
        _invalid("Phase 4 resource or scenario declaration is invalid")
    if type(config.privacy_mode) is not PrivacyMode:
        _invalid("Phase 4 privacy declaration is invalid")
    for pairs in (config.output, config.state_mapping, config.representation_compatibility):
        if (type(pairs) is not tuple or any(type(pair) is not tuple or len(pair) != 2
                or type(pair[0]) is not str for pair in pairs)
                or len({pair[0] for pair in pairs}) != len(pairs)):
            _invalid("Phase 4 mapping declaration is invalid")
    if type(config.version_order) is not tuple or type(config.strict_warning_codes) is not tuple:
        _invalid("Phase 4 sequence declaration is invalid")
    return {
        "config_version": config.config_version,
        "inputs": inputs,
        "representation": None if representation is None else {
            "name": representation.name, "source": representation.source,
            "field": representation.field, "version": representation.version,
            "missing_value_policy": representation.missing_value_policy,
            "normalization_profile": representation.normalization_profile,
        },
        "representation_compatibility": dict(config.representation_compatibility),
        "state_mapping": dict(config.state_mapping), "version_order": list(config.version_order),
        "privacy_mode": config.privacy_mode.value, "strict_mode": config.strict_mode,
        "strict_warning_codes": list(config.strict_warning_codes),
        "resource_limits": {
            "max_file_bytes": config.resource_limits.max_file_bytes,
            "max_rows": config.resource_limits.max_rows,
            "max_content_bytes": config.resource_limits.max_content_bytes,
            "max_parent_list_length": config.resource_limits.max_parent_list_length,
            "max_json_depth": config.resource_limits.max_json_depth,
        },
        "output": dict(config.output),
        "simulation": {"enabled": config.simulation.enabled, "seed": config.simulation.seed},
    }


def _phase4_option_path(value: object) -> Path:
    """Validate a local declaration lexically, without opening or resolving it."""
    if not isinstance(value, (str, Path)) or not str(value) or any(
            ord(character) < 32 or ord(character) == 127 for character in str(value)):
        _invalid("Phase 4 paths must be nonempty local declarations")
    try:
        local_input_path(value)
    except Exception:
        _invalid("Phase 4 paths must be nonempty local declarations")
    return Path(value)


def _phase4_literal(value: object) -> str:
    if type(value) is not str or not value or "\x00" in value:
        _invalid("Phase 4 text declarations must be nonempty literal strings")
    try:
        value.encode("utf-8")
    except UnicodeEncodeError:
        _invalid("Phase 4 text declarations must use valid Unicode")
    return value


def resolve_phase4_options(config: ResolvedConfig | Mapping[str, Any] | None = None, *,
                           cli: Mapping[str, Any] | None = None) -> Phase4Options:
    """Validate Phase 4 declarations without overriding competing singletons.

    CLI keys use underscore spellings of the approved option names. Omitted
    options are absent or ``None``. Raw config mappings retain explicit-field
    provenance. With a ``ResolvedConfig``, its privacy and strictness values are
    authoritative because Phase 2 does not retain omission provenance.
    """
    allowed_cli = {"records", "provenance", "compare", "schema_mapping", "version_order",
                   "state_semantics", "missing_state_id", "out", "redacted", "record_ids",
                   "id_salt_file", "strict", "tail_rule", "tail_threshold"}
    if cli is None:
        cli = {}
    if not isinstance(cli, Mapping) or any(type(key) is not str or key not in allowed_cli for key in cli):
        _invalid("unsupported Phase 4 option")
    options = {key: value for key, value in cli.items() if value is not None}
    if config is None:
        raw, declared = {}, set()
    elif type(config) is ResolvedConfig:
        raw = _phase4_config_data(config)
        declared = set(raw)
    elif isinstance(config, Mapping):
        if any(type(key) is not str for key in config):
            _invalid("Phase 4 configuration keys must be strings")
        raw, declared = dict(config), set(config)
    else:
        _invalid("Phase 4 configuration must be an accepted declaration or object")
    try:
        resolved = resolve_config(raw)
    except (ConfigurationError, TypeError, ValueError):
        raise ConfigurationError(ErrorCode.CONFIG_INVALID, "Phase 4 configuration is invalid") from None
    if resolved.privacy_mode not in (PrivacyMode.STANDARD, PrivacyMode.REDACTED):
        _invalid("Phase 4 supports only standard or redacted output")
    if resolved.simulation.enabled or resolved.state_mapping or resolved.representation_compatibility:
        _invalid("Phase 4 options do not activate simulations or arbitrary state mappings")
    output = dict(resolved.output)
    if any(type(key) is not str or key not in {"directory", "record_id_mode", "id_salt_file"} for key in output):
        _invalid("unsupported Phase 4 output field")
    for key, cli_key in (("directory", "out"), ("record_id_mode", "record_ids"), ("id_salt_file", "id_salt_file")):
        if key in output and cli_key in options:
            _invalid("Phase 4 output declarations compete")
        if key in output and (type(output[key]) is not str or not output[key]):
            _invalid("Phase 4 output values must be nonempty strings")
    privacy_mode = resolved.privacy_mode.value
    if "redacted" in options:
        if type(options["redacted"]) is not bool:
            _invalid("Phase 4 redacted selection must be boolean")
        selected = "redacted" if options["redacted"] else "standard"
        if "privacy_mode" in declared:
            _invalid("Phase 4 privacy declarations compete")
        privacy_mode = selected
    strict_mode = resolved.strict_mode
    if "strict" in options:
        if type(options["strict"]) is not bool:
            _invalid("Phase 4 strict selection must be boolean")
        if "strict_mode" in declared:
            _invalid("Phase 4 strict declarations compete")
        strict_mode = options["strict"]
    record_id_mode = options.get("record_ids", output.get("record_id_mode", "hash" if privacy_mode == "redacted" else "preserve"))
    if type(record_id_mode) is not str or record_id_mode not in {"preserve", "hash", "omit"}:
        _invalid("Phase 4 record ID mode must be preserve, hash or omit")
    salt_file = options.get("id_salt_file", output.get("id_salt_file"))
    if privacy_mode != "redacted" and ("record_ids" in options or "record_id_mode" in output or salt_file is not None):
        _invalid("Phase 4 identifier options require redacted output")
    directory = _phase4_option_path(options.get("out", output.get("directory", "./rit-report")))
    salt_file = None if salt_file is None else _phase4_option_path(salt_file)
    sources = list(resolved.inputs)
    if any(source.role is FileRole.CONFIG for source in sources):
        _invalid("Phase 4 recursive configuration inputs are unsupported")
    for source in sources:
        _phase4_option_path(source.path)
    for key, role in (("records", FileRole.RECORDS_PRIMARY), ("provenance", FileRole.PROVENANCE_MANIFEST),
                      ("compare", FileRole.RECORDS_COMPARE), ("schema_mapping", FileRole.SCHEMA_MAPPING)):
        existing = [source for source in sources if source.role is role]
        if len(existing) > 1 or existing and key in options:
            _invalid("Phase 4 singleton input declarations compete")
        if key in options:
            sources.append(InputSource(role, _phase4_option_path(options[key])))
    version_order = resolved.version_order
    if "version_order" in options:
        if version_order or any(source.role is FileRole.VERSION_ORDER for source in sources):
            _invalid("Phase 4 version order declarations compete")
        supplied_order = options["version_order"]
        if type(supplied_order) in (list, tuple):
            version_order = tuple(_phase4_literal(value) for value in supplied_order)
            if not version_order or len(set(version_order)) != len(version_order):
                _invalid("Phase 4 version order must be nonempty and unique")
        else:
            sources.append(InputSource(FileRole.VERSION_ORDER, _phase4_option_path(supplied_order)))
    if version_order and any(source.role is FileRole.VERSION_ORDER for source in sources):
        _invalid("Phase 4 version order declarations compete")
    state_semantics = None if "state_semantics" not in options else _phase4_literal(options["state_semantics"])
    missing_state_id = None if "missing_state_id" not in options else _phase4_literal(options["missing_state_id"])
    explicit_missing = resolved.representation is not None and resolved.representation.missing_value_policy == "explicit_missing_state"
    if explicit_missing != (missing_state_id is not None):
        _invalid("Phase 4 missing-state ID is required exactly for the explicit_missing_state policy")
    tail_rule, threshold = options.get("tail_rule"), options.get("tail_threshold")
    if tail_rule is None:
        if threshold is not None:
            _invalid("Phase 4 tail threshold requires an explicit tail rule")
    elif type(tail_rule) is not str or tail_rule not in {"singleton_count", "count_at_or_below", "frequency_at_or_below"}:
        _invalid("unsupported Phase 4 tail rule")
    elif resolved.representation is None:
        _invalid("Phase 4 tail selection requires an explicit representation")
    elif tail_rule == "singleton_count" and threshold is not None:
        _invalid("singleton_count rejects a tail threshold")
    elif tail_rule == "count_at_or_below" and (type(threshold) is not int or threshold < 0):
        _invalid("count_at_or_below requires a nonnegative integer threshold")
    elif tail_rule == "frequency_at_or_below" and (type(threshold) not in (int, float)
            or not 0 <= threshold <= 1 or not math.isfinite(threshold)):
        _invalid("frequency_at_or_below requires a finite threshold within zero and one")
    return Phase4Options(resolved, tuple(sorted(sources, key=lambda source: (source.role.value, str(source.path)))),
                         directory, privacy_mode, record_id_mode, salt_file, strict_mode, version_order,
                         state_semantics, missing_state_id, tail_rule, threshold)


def phase4_config_summary(options: Phase4Options) -> dict[str, Any]:
    """Return only schema-allowlisted safe scalars, never paths or free text.

    Identity-bearing declarations still affect ``phase4_config_hash``. They are
    omitted here rather than described as missing evidence or replaced by a
    fabricated representation. The canonical report discloses their meaning.
    """
    if type(options) is not Phase4Options:
        _invalid("safe configuration summary requires resolved Phase 4 options")
    options.__post_init__()
    tail = None if options.tail_rule is None else {
        "rule": options.tail_rule,
        "count_threshold": options.tail_threshold if options.tail_rule == "count_at_or_below" else None,
        "frequency_threshold": options.tail_threshold if options.tail_rule == "frequency_at_or_below" else None,
        "state_ids": [], "ranking_rule": "ascending_frequency_then_count_then_unicode_state_id",
    }
    return {"strict_mode": options.strict_mode, "privacy_mode": options.privacy_mode,
            "record_id_mode": options.record_id_mode, "tail_selection": tail, "weighted": False,
            "comparison_requested": any(source.role is FileRole.RECORDS_COMPARE for source in options.inputs),
            "scenario_requested": False}


def phase4_config_hash(options: Phase4Options) -> str:
    """Hash normalized resolved meaning; exclude secret material and secret path.

    Input/output paths and identity-bearing declarations affect this hash but
    are never returned as a configuration dump. Changing only the local secret
    path keeps the hash stable; changing its declared stability scope does not.
    A config hash is linkable metadata, not authentication or anonymity.
    """
    if type(options) is not Phase4Options:
        _invalid("configuration hashing requires resolved Phase 4 options")
    options.__post_init__()
    normalized = _phase4_config_data(options.configuration)
    normalized["inputs"] = [{"role": source.role.value, "path": str(source.path),
                              "format": None if source.declared_format is None else source.declared_format.value}
                             for source in options.inputs]
    normalized["privacy_mode"] = options.privacy_mode
    normalized["strict_mode"] = options.strict_mode
    normalized["strict_warning_codes"] = sorted(options.configuration.strict_warning_codes)
    normalized["version_order"] = list(options.version_order)
    normalized["output"] = {"directory": str(options.directory), "record_id_mode": options.record_id_mode,
                             "identifier_secret_source": "local_file" if options.id_salt_file is not None else "fresh"}
    normalized["state_semantics"] = options.state_semantics
    normalized["missing_state_id"] = options.missing_state_id
    normalized["tail_rule"] = options.tail_rule
    normalized["tail_threshold"] = options.tail_threshold
    return sha256_canonical({"encoding": "rit.phase4.config.v1", "options": normalized})


def load_phase4_invocation(*, cli: Mapping[str, Any], config_path: str | Path | None = None,
                           base_directory: Path) -> tuple[Phase4Options, tuple]:
    """Read one local control document, retaining its explicit-field provenance.

    Reuse the accepted finite, unique-key control reader and its resource limits.
    Config-declared paths are relative to the config file; invocation paths are
    relative to the explicit working directory. No records or secrets are read.
    The returned config inventory describes the exact bytes parsed here, so the
    CLI passes detached declarations to validation without reopening the config.
    """
    from dataclasses import replace
    from .errors import ToolkitError
    from .io.validation import _bundle_control, _bundle_document

    base = _phase4_option_path(base_directory)
    if not base.is_absolute():
        _invalid("Phase 4 invocation requires an absolute working directory")
    raw, inventory, config_base = {}, (), base
    if config_path is not None:
        path = _phase4_option_path(config_path)
        _phase4_literal(str(path))
        source = InputSource(FileRole.CONFIG, path if path.is_absolute() else base / path)
        try:
            entry, text = _bundle_control(source, ResourceLimits())
            raw = _bundle_document(text, source, ResourceLimits())
        except ToolkitError:
            raise ConfigurationError(ErrorCode.CONFIG_INVALID, "The local configuration cannot be parsed or read") from None
        inventory, config_base = (entry,), entry.path.parent
    options = resolve_phase4_options(raw, cli=cli)
    if inventory:
        limits = options.configuration.resource_limits
        if limits.max_file_bytes is not None and inventory[0].size_bytes > limits.max_file_bytes:
            _invalid("Phase 4 configuration exceeds its declared resource limit")
        try:
            _bundle_document(text, source, limits)
        except ToolkitError:
            raise ConfigurationError(ErrorCode.CONFIG_INVALID, "The local configuration violates its resource limits") from None
    for path in (options.directory, *(source.path for source in options.inputs)):
        _phase4_literal(str(path))
    if options.id_salt_file is not None:
        _phase4_literal(str(options.id_salt_file))
    configured_roles = {source.role for source in options.configuration.inputs}
    sources = tuple(InputSource(source.role, source.path if source.path.is_absolute() else
                    (config_base if source.role in configured_roles else base) / source.path,
                    source.declared_format) for source in options.inputs)
    output = dict(options.configuration.output)
    directory_base = config_base if "directory" in output else base
    directory = options.directory if options.directory.is_absolute() else directory_base / options.directory
    salt = options.id_salt_file
    if salt is not None and not salt.is_absolute():
        salt = (config_base if "id_salt_file" in output else base) / salt
    return replace(options, inputs=sources, directory=directory, id_salt_file=salt), inventory


def phase4_validation_configuration(options: Phase4Options) -> dict[str, Any]:
    """Detach effective input settings without duplicating resolved source roles."""
    if type(options) is not Phase4Options:
        _invalid("validation requires resolved Phase 4 options")
    data = _phase4_config_data(options.configuration)
    data["inputs"] = {}
    data["strict_mode"] = options.strict_mode
    data["privacy_mode"] = options.privacy_mode
    data["version_order"] = list(options.version_order)
    return data


def phase4_pair_requested(options: Phase4Options, *, operation: str) -> bool:
    """Check explicit pair intent without inferring chronology or state meaning.

    Input-only validation accepts two declared files without requesting a pair.
    State-meaning declarations belong to audit/example calculation requests.
    """
    if type(options) is not Phase4Options or operation not in ("audit", "validate", "example"):
        _invalid("invalid Phase 4 operation")
    requested = any(source.role is FileRole.RECORDS_COMPARE for source in options.inputs)
    if operation == "validate":
        if options.state_semantics is not None or options.tail_rule is not None:
            _invalid("input-only validation cannot request calculations")
        return False
    if requested != (options.state_semantics is not None):
        _invalid("comparison requires both an earlier input and one shared literal state meaning")
    if options.state_semantics is not None and not options.state_semantics.strip():
        _invalid("comparison state meaning must be nonblank")
    return requested
