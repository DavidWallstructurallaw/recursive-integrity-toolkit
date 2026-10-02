"""Apply the approved, non-executable field-mapping language to supplied rows.

Owner IDs:
    PR-003; PR-002 and PR-016 support explicit local mapping-file snapshots.

Inputs:
    A versioned JSON mapping document and an already parsed plain row or RawRow.

Outputs:
    MappingPlan, MappedRow, ordered field traces, and content-safe diagnostics.

Assumptions:
    Field names are literal dictionary keys. Every transformation is explicit.
    The original row supplies all selectors; target fields cannot feed each other.

Limits:
    No canonical normalization, source inference, identity validation, provenance
    join, metric, lineage, observability classification, report, network, plugin,
    user callback, or executable expression. Missing, null, and unknown stay distinct.

Current phase status:
    Phase 2 Step 3 mapping only. No analytical behavior.
"""

from __future__ import annotations

import json
import math
import re
from dataclasses import dataclass, field, replace
from datetime import datetime
from pathlib import Path

from ..config import ResourceLimits
from ..errors import ErrorCode, MappingError, WarningCode
from ..models import FileFormat, FileInventoryEntry, FileRole, InputSource, RawRow
from ..utils.hashing import sha256_bytes
from .loaders import _check_depth, _limits, _read_source, _text


# Closed dispatch table of syntax only. No user value selects a Python callable.
_OPERATION_KEYS = {
    "rename": {"op"}, "trim": {"op"}, "cast_string": {"op"},
    "cast_integer": {"op"}, "cast_float": {"op"},
    "cast_boolean": {"op", "mapping"}, "parse_datetime": {"op", "format"},
    "parse_json_list": {"op"}, "constant": {"op", "value"},
    "coalesce": {"op", "sources"}, "map_values": {"op", "mapping", "unmapped"},
    "normalize_whitespace": {"op", "format"}, "lowercase": {"op"}, "uppercase": {"op"},
}
_MISSING = object()
_INTEGER = re.compile(r"[+-]?[0-9]+\Z")
_FLOAT = re.compile(r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?\Z")


@dataclass(frozen=True, slots=True)
class MappingPlan:
    """Immutable JSON snapshot; declaration values are hidden from repr."""

    schema_version: str
    document_json: str = field(repr=False)
    sha256: str
    sections: tuple[str, ...]
    max_json_depth: int | None = None
    inventory: FileInventoryEntry | None = None


@dataclass(frozen=True, slots=True)
class FieldMappingTrace:
    """Selector and ordered operation names; never include source values."""

    target: str
    selector: str
    source_fields: tuple[str, ...]
    operations: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class MappingNotice:
    """An unmatched value was handled by an explicit keep or null policy."""

    code: str
    field: str
    operation_index: int
    policy: str


@dataclass(frozen=True, slots=True)
class MappedRow:
    """Internal mapping output, not a validated record or audit report."""

    values: dict[str, object] = field(repr=False)
    extras: dict[str, object] = field(repr=False)
    source_fields: tuple[str, ...]
    unmapped_fields: tuple[str, ...]
    field_traces: tuple[FieldMappingTrace, ...]
    notices: tuple[MappingNotice, ...]
    mapping_sha256: str
    row_number: int | None = None
    line_number: int | None = None


def _error(code: ErrorCode, message: str, **location) -> MappingError:
    return MappingError(code, message, **location)


def _copy_value(value: object, *, allow_datetime: bool = False) -> object:
    """Copy only plain data without invoking user conversion or copy hooks."""
    kind = type(value)
    if value is None or kind in (str, bool, int):
        return value
    if kind is float and math.isfinite(value):
        return value
    if allow_datetime and kind is datetime:
        return value
    if kind is list:
        return [_copy_value(item, allow_datetime=allow_datetime) for item in value]
    if kind is dict and all(type(key) is str for key in value):
        return {key: _copy_value(item, allow_datetime=allow_datetime) for key, item in value.items()}
    raise _error(ErrorCode.SCHEMA_TYPE, "mapping accepts plain finite data only")


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise _error(ErrorCode.MAPPING_TARGET_COLLISION, "duplicate mapping or JSON object key")
        result[key] = value
    return result


def _reject_constant(value: str) -> None:
    raise ValueError("nonfinite number")


def _finite_float(value: str) -> float:
    result = float(value)
    if not math.isfinite(result):
        raise ValueError("nonfinite number")
    return result


def _json_value(text: str, maximum: int | None) -> object:
    _check_depth(text, maximum)
    return json.loads(text, object_pairs_hook=_unique_object,
                      parse_constant=_reject_constant, parse_float=_finite_float)


def _name(value: object) -> bool:
    return type(value) is str and bool(value)


def _validate_operation(operation: object) -> None:
    if type(operation) is not dict or type(operation.get("op")) is not str:
        raise _error(ErrorCode.MAPPING_UNSAFE_TRANSFORM, "operation must name an approved transform")
    op = operation["op"]
    if op not in _OPERATION_KEYS or set(operation) != _OPERATION_KEYS[op]:
        raise _error(ErrorCode.MAPPING_UNSAFE_TRANSFORM, "unsupported operation or operation parameters")
    if op in {"cast_boolean", "map_values"}:
        tokens = operation["mapping"]
        if type(tokens) is not dict:
            raise _error(ErrorCode.SCHEMA_TYPE, "token mapping must be an object")
        if op == "cast_boolean" and (not tokens or any(type(v) is not bool for v in tokens.values())):
            raise _error(ErrorCode.SCHEMA_TYPE, "boolean tokens require explicit boolean destinations")
    if op == "map_values" and operation["unmapped"] not in ("keep", "null", "error"):
        raise _error(ErrorCode.SCHEMA_ENUM, "unmapped policy must be keep, null, or error")
    if op == "parse_datetime":
        fmt = operation["format"]
        if not _name(fmt):
            raise _error(ErrorCode.SCHEMA_TYPE, "datetime parsing requires an explicit format")
        if fmt != "iso8601":
            # Keep declared formats portable and independent of process locale.
            if re.sub(r"%(?:%|Y|y|m|d|H|M|S|f|z|j)", "", fmt).find("%") != -1:
                raise _error(ErrorCode.SCHEMA_TYPE, "datetime format uses an unsupported directive")
    if op == "normalize_whitespace" and operation["format"] != "collapse":
        raise _error(ErrorCode.SCHEMA_ENUM, "whitespace format must explicitly select collapse")
    if op == "coalesce":
        sources = operation["sources"]
        if type(sources) is not list or not sources or any(not _name(s) for s in sources):
            raise _error(ErrorCode.SCHEMA_TYPE, "coalesce requires named source fields")


def _validate_document(document: object) -> None:
    if type(document) is not dict:
        raise _error(ErrorCode.SCHEMA_TYPE, "mapping root must be an object")
    if set(document) - {"schema_version", "mapping_version", "records", "provenance"}:
        raise _error(ErrorCode.MAPPING_UNSAFE_TRANSFORM, "unsupported mapping document fields")
    versions = [document[k] for k in ("schema_version", "mapping_version") if k in document]
    if len(versions) != 1 or versions[0] != "1.0":
        raise _error(ErrorCode.SCHEMA_TYPE, "declare exactly one supported mapping version, 1.0")
    sections = set(document) & {"records", "provenance"}
    if not sections:
        raise _error(ErrorCode.SCHEMA_REQUIRED_FIELD, "mapping needs a records or provenance section")
    for section in sections:
        block = document[section]
        if type(block) is not dict or set(block) != {"fields"} or type(block["fields"]) is not dict:
            raise _error(ErrorCode.SCHEMA_TYPE, "mapping section requires a fields object", section=section)
        for target, spec in block["fields"].items():
            if not _name(target) or type(spec) is not dict:
                raise _error(ErrorCode.SCHEMA_TYPE, "field mapping must have a nonempty target", section=section)
            if set(spec) - {"source", "constant", "operations"}:
                raise _error(ErrorCode.MAPPING_UNSAFE_TRANSFORM, "unsupported field mapping parameters",
                             section=section, target=target)
            if "source" in spec and "constant" in spec:
                raise _error(ErrorCode.MAPPING_TARGET_COLLISION, "one selector must own a target field",
                             section=section, target=target)
            if "source" in spec and not _name(spec["source"]):
                raise _error(ErrorCode.SCHEMA_TYPE, "source field must be a nonempty literal name",
                             section=section, target=target)
            operations = spec.get("operations", [])
            if type(operations) is not list:
                raise _error(ErrorCode.SCHEMA_TYPE, "operations must be an ordered array", section=section, target=target)
            for index, operation in enumerate(operations):
                try:
                    _validate_operation(operation)
                except MappingError as exc:
                    raise _error(exc.code, exc.safe_message, section=section, target=target,
                                 operation_index=index) from None
            if "source" not in spec and "constant" not in spec:
                if not operations or operations[0]["op"] not in {"constant", "coalesce"}:
                    raise _error(ErrorCode.SCHEMA_REQUIRED_FIELD, "field needs an explicit selector",
                                 section=section, target=target)


def compile_mapping(document: dict[str, object], *, limits: ResourceLimits | None = None) -> MappingPlan:
    """Validate and freeze declarations. No rows, files, or transforms execute."""
    checked = _limits(limits)
    try:
        copied = _copy_value(document)
        _validate_document(copied)
        text = json.dumps(copied, ensure_ascii=False, allow_nan=False, separators=(",", ":"))
        _check_depth(text, checked.max_json_depth)
        encoded = text.encode("utf-8")
    except MappingError:
        raise
    except (ValueError, TypeError, OverflowError, RecursionError):
        raise _error(ErrorCode.SCHEMA_TYPE, "mapping must contain bounded valid UTF-8 JSON data") from None
    return MappingPlan("1.0", text, sha256_bytes(encoded),
                       tuple(s for s in ("records", "provenance") if s in copied), checked.max_json_depth)


def parse_mapping_json(text: str, *, limits: ResourceLimits | None = None) -> MappingPlan:
    """Parse strict JSON before validation so duplicate targets cannot disappear."""
    checked = _limits(limits)
    if type(text) is not str:
        raise _error(ErrorCode.SCHEMA_TYPE, "mapping JSON must be text")
    try:
        document = _json_value(text, checked.max_json_depth)
    except MappingError:
        raise
    except (ValueError, RecursionError):
        raise _error(ErrorCode.FILE_PARSE, "mapping JSON cannot be parsed safely") from None
    return compile_mapping(document, limits=checked)


def load_mapping(path: str | Path, *, limits: ResourceLimits | None = None) -> MappingPlan:
    """Read exactly one local JSON mapping file with the existing snapshot loader."""
    checked = _limits(limits)
    source = InputSource(FileRole.SCHEMA_MAPPING, path, FileFormat.JSON)
    local, raw = _read_source(source, checked)
    plan = parse_mapping_json(_text(source, raw), limits=checked)
    inventory = FileInventoryEntry(source.role, local, FileFormat.JSON, len(raw), sha256_bytes(raw))
    return replace(plan, inventory=inventory)


def _select(spec: dict[str, object], row: dict[str, object]) -> object:
    if "constant" in spec:
        return _copy_value(spec["constant"])
    if "source" not in spec:
        return _MISSING
    source = spec["source"]
    if source not in row:
        raise _error(ErrorCode.MAPPING_SOURCE_FIELD_MISSING, "required source field is absent")
    return row[source]


def _coalesce(sources: list[str], row: dict[str, object]) -> object:
    present = False
    for source in sources:
        if source in row:
            present = True
            if row[source] is not None:
                return row[source]
    return None if present else _MISSING


def _apply_operation(value: object, operation: dict[str, object], row: dict[str, object],
                     maximum: int | None) -> tuple[object, str | None]:
    """Fixed branch dispatch. Return optional unmatched policy for audit metadata."""
    op = operation["op"]
    if op == "constant":
        return _copy_value(operation["value"]), None
    if op == "coalesce":
        return _coalesce(operation["sources"], row), None
    if value is _MISSING or value is None:
        return value, None
    if op == "rename":
        return value, None
    if op == "map_values":
        tokens = operation["mapping"]
        if type(value) is str and value in tokens:
            return _copy_value(tokens[value]), None
        policy = operation["unmapped"]
        if policy == "error":
            raise _error(ErrorCode.SCHEMA_ENUM, "source value has no declared mapping")
        return (None if policy == "null" else value), policy
    if op == "cast_string":
        if type(value) is str:
            return value, None
        if type(value) in (int, bool, float):
            return json.dumps(value, allow_nan=False), None
    elif op == "cast_integer":
        if type(value) is int:
            return value, None
        if type(value) is str and _INTEGER.fullmatch(value):
            return int(value), None
    elif op == "cast_float":
        if type(value) in (int, float) or (type(value) is str and _FLOAT.fullmatch(value)):
            result = float(value)
            if math.isfinite(result):
                return result, None
    elif type(value) is str:
        if op == "trim":
            return value.strip(), None
        if op == "lowercase":
            return value.lower(), None
        if op == "uppercase":
            return value.upper(), None
        if op == "normalize_whitespace":
            return re.sub(r"\s+", " ", value), None
        if op == "cast_boolean" and value in operation["mapping"]:
            return operation["mapping"][value], None
        if op == "parse_datetime":
            fmt = operation["format"]
            return (datetime.fromisoformat(value) if fmt == "iso8601" else datetime.strptime(value, fmt)), None
        if op == "parse_json_list":
            parsed = _json_value(value, maximum)
            if type(parsed) is list:
                return parsed, None
    raise _error(ErrorCode.SCHEMA_TYPE, "value does not satisfy the declared transform")


def map_row(row: dict[str, object] | RawRow, plan: MappingPlan, *, section: str = "records",
            preserve_extras: bool = False) -> MappedRow:
    """Apply one declaration to one row without mutating it or following references.

    All named selectors read the original row, never an earlier target value.
    Coalesce treats only absent keys and None as missing. Null passes through
    ordinary transforms. Raw CSV null-token interpretation belongs to Step 4.
    """
    if type(plan) is not MappingPlan or type(section) is not str or section not in ("records", "provenance"):
        raise _error(ErrorCode.SCHEMA_TYPE, "use a MappingPlan and an approved section")
    if type(plan.sha256) is not str or type(plan.schema_version) is not str or type(plan.sections) is not tuple:
        raise _error(ErrorCode.SCHEMA_TYPE, "mapping plan metadata must use plain types")
    if any(type(name) is not str for name in plan.sections):
        raise _error(ErrorCode.SCHEMA_TYPE, "mapping plan sections must be strings")
    if type(preserve_extras) is not bool:
        raise _error(ErrorCode.SCHEMA_TYPE, "preserve_extras must be an explicit boolean")
    original = row.values if type(row) is RawRow else row
    row_number = row.row_number if type(row) is RawRow else None
    line_number = row.line_number if type(row) is RawRow else None
    try:
        # Recheck the frozen document rather than trusting a manually constructed plan.
        verified = parse_mapping_json(plan.document_json, limits=ResourceLimits(max_json_depth=plan.max_json_depth))
        if verified.sha256 != plan.sha256 or verified.sections != plan.sections or plan.schema_version != "1.0":
            raise _error(ErrorCode.SCHEMA_TYPE, "mapping plan metadata does not match its document")
        document = _json_value(verified.document_json, plan.max_json_depth)
        if section not in document:
            raise _error(ErrorCode.SCHEMA_REQUIRED_FIELD, "requested mapping section is absent", section=section)
        if type(original) is not dict:
            raise _error(ErrorCode.SCHEMA_TYPE, "row must contain a plain field dictionary")
        source = _copy_value(original, allow_datetime=True)
    except RecursionError:
        raise _error(ErrorCode.SCHEMA_TYPE, "row or mapping exceeds supported nesting") from None
    values: dict[str, object] = {}
    used: set[str] = set()
    traces: list[FieldMappingTrace] = []
    notices: list[MappingNotice] = []
    for target, spec in document[section]["fields"].items():
        operations = spec.get("operations", [])
        sources = [spec["source"]] if "source" in spec else []
        for operation in operations:
            if operation["op"] == "coalesce":
                sources.extend(operation["sources"])
        used.update(sources)
        index = None
        try:
            value = _select(spec, source)
            for index, operation in enumerate(operations):
                value, policy = _apply_operation(value, operation, source, plan.max_json_depth)
                if policy:
                    notices.append(MappingNotice(WarningCode.MAPPING_VALUE_UNMAPPED.value, target, index, policy))
            if value is not _MISSING:
                values[target] = _copy_value(value, allow_datetime=True)
        except MappingError as exc:
            raise _error(exc.code, exc.safe_message, section=section, target=target,
                         operation_index=index, row_number=row_number, line_number=line_number) from None
        except (ValueError, TypeError, OverflowError, RecursionError):
            raise _error(ErrorCode.SCHEMA_TYPE, "value cannot be converted by the declared transform",
                         section=section, target=target, operation_index=index,
                         row_number=row_number, line_number=line_number) from None
        selector = "source" if "source" in spec else "constant" if "constant" in spec else "operations"
        traces.append(FieldMappingTrace(target, selector, tuple(dict.fromkeys(sources)),
                                        tuple(op["op"] for op in operations)))
    unmapped = tuple(key for key in source if key not in used)
    extras = {key: _copy_value(source[key], allow_datetime=True) for key in unmapped} if preserve_extras else {}
    return MappedRow(values, extras, tuple(source), unmapped, tuple(traces), tuple(notices),
                     plan.sha256, row_number, line_number)
