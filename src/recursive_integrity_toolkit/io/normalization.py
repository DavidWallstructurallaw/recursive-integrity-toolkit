"""Normalize serialization-level values into row-valid canonical fields.

Owner IDs:
    PR-001 identity, PR-004 provenance row fields, PR-008 parent list types,
    PR-009 declared generation type, PR-016 deterministic row order.

Inputs:
    Plain typed dictionaries, loader RawRow objects, or explicit MappedRow results.
    CSV inputs retain their original RawRow spelling; policies are explicit.

Outputs:
    Detached CanonicalRow objects with field-state and source-location metadata.

Assumptions:
    Physical parsing and any field mapping have already been performed.
    CSV and native input types have separate, declared conversion rules.

Limits:
    No file access, source mutation, automatic field mapping, provenance join,
    coverage, parent resolution, generation derivation, chronology, representation
    assignment, content-reference opening, metric, simulation, or report export.

Current phase status:
    Phase 2 Step 4 canonical row normalization. No analytical behavior.
"""

from __future__ import annotations

import json
import math
import re
from datetime import datetime, timezone
from types import MappingProxyType
from zoneinfo import ZoneInfo

from ..config import ResourceLimits
from ..errors import CanonicalValidationError, ErrorCode
from ..models import (
    CanonicalRow, ContentMode, FileFormat, FileRole, LoadedTable,
    NormalizationOptions, RawRow, RowLocation,
)
from ..utils.ordering import stable_record_order
from .schema_mapping import MappedRow
from .loaders import _check_depth, _unique_object, _reject_constant, _finite_float
from .validation import (
    ENUMS, OPTIONAL_IDENTIFIERS, RECORD_REQUIRED, PROVENANCE_REQUIRED,
    canonical_fields, validate_canonical_values, validate_unique_keys, _fail,
)


_INTEGER = re.compile(r"[+-]?[0-9]+\Z")
_FLOAT = re.compile(r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?\Z")


def _policy(options: NormalizationOptions | None, limits: ResourceLimits | None
            ) -> tuple[NormalizationOptions, ResourceLimits]:
    chosen = NormalizationOptions() if options is None else options
    bounded = ResourceLimits() if limits is None else limits
    if type(chosen) is not NormalizationOptions or type(bounded) is not ResourceLimits:
        raise CanonicalValidationError(ErrorCode.CONFIG_INVALID, "use explicit normalization options and resource limits")
    if type(chosen.content_mode) is not ContentMode:
        raise CanonicalValidationError(ErrorCode.CONFIG_INVALID, "content_mode must use the approved enum")
    if any(type(flag) is not bool for flag in (
        chosen.csv_boolean_compatibility, chosen.blank_as_null, chosen.preserve_extras,
    )):
        raise CanonicalValidationError(ErrorCode.CONFIG_INVALID, "normalization flags must be booleans")
    if type(chosen.null_tokens) is not tuple or any(type(token) is not str or not token for token in chosen.null_tokens):
        raise CanonicalValidationError(ErrorCode.CONFIG_INVALID, "null tokens must be an explicit tuple of nonempty strings")
    if len(set(chosen.null_tokens)) != len(chosen.null_tokens) or "unknown" in chosen.null_tokens:
        raise CanonicalValidationError(ErrorCode.CONFIG_INVALID, "null tokens cannot duplicate or replace explicit unknown")
    for value in (bounded.max_content_bytes, bounded.max_parent_list_length, bounded.max_json_depth):
        if value is not None and (type(value) is not int or value <= 0):
            raise CanonicalValidationError(ErrorCode.CONFIG_INVALID, "normalization limits must be positive integers")
    return chosen, bounded


def _location(value: RowLocation | None, row_number: int | None,
              line_number: int | None) -> RowLocation:
    result = RowLocation() if value is None else value
    if type(result) is not RowLocation:
        raise CanonicalValidationError(ErrorCode.CONFIG_INVALID, "location must use RowLocation")
    if result.file_role is not None and type(result.file_role) is not FileRole:
        raise CanonicalValidationError(ErrorCode.CONFIG_INVALID, "location role must use FileRole")
    if result.file_path is not None and type(result.file_path) is not str:
        raise CanonicalValidationError(ErrorCode.CONFIG_INVALID, "location path must be text")
    return RowLocation(result.file_role, result.file_path,
                       result.row_number if result.row_number is not None else row_number,
                       result.line_number if result.line_number is not None else line_number)


def _csv_quotes(row: RawRow, location: RowLocation) -> dict[str, bool]:
    """Retain quoting flags from an already parsed record, without reading a file."""
    if type(row) is not RawRow or type(row.serialized_text) is not str or type(row.values) is not dict:
        raise _fail(ErrorCode.SCHEMA_TYPE, "CSV normalization requires the original parsed row spelling", None, location)
    flags = [False]
    state = "start"
    for char in row.serialized_text:
        if state == "quoted":
            if char == '"':
                state = "closed"
        elif state == "closed":
            if char == '"':
                state = "quoted"
            elif char == ",":
                flags.append(False)
                state = "start"
            elif char not in "\r\n":
                raise _fail(ErrorCode.FILE_PARSE, "CSV spelling is inconsistent with a parsed row", None, location)
        elif char == ",":
            flags.append(False)
            state = "start"
        elif char == '"':
            if state != "start":
                raise _fail(ErrorCode.FILE_PARSE, "CSV spelling is inconsistent with a parsed row", None, location)
            flags[-1] = True
            state = "quoted"
        elif char not in "\r\n":
            state = "bare"
    if state == "quoted" or len(flags) != len(row.values):
        raise _fail(ErrorCode.FILE_PARSE, "CSV spelling is inconsistent with a parsed row", None, location)
    return dict(zip(row.values, flags))


def _input(row: dict[str, object] | RawRow | MappedRow, file_format: FileFormat | None,
           source_row: RawRow | None, location: RowLocation
           ) -> tuple[dict[str, object], dict[str, object], dict[str, bool]]:
    if file_format is not None and type(file_format) is not FileFormat:
        raise _fail(ErrorCode.CONFIG_INVALID, "row serialization must use FileFormat", None, location)
    if file_format is not None and file_format not in (FileFormat.CSV, FileFormat.JSONL, FileFormat.PARQUET):
        raise _fail(ErrorCode.CONFIG_INVALID, "declare a supported row serialization", None, location)
    values = row.values if type(row) in (RawRow, MappedRow) else row
    if type(values) is not dict or any(type(name) is not str for name in values):
        raise _fail(ErrorCode.SCHEMA_TYPE, "row must contain a plain string-keyed dictionary", None, location)
    extras = row.extras if type(row) is MappedRow else {}
    quoted: dict[str, bool] = {}
    if file_format is FileFormat.CSV:
        original = row if type(row) is RawRow else source_row
        if type(original) is not RawRow:
            raise _fail(ErrorCode.SCHEMA_TYPE, "CSV requires its original RawRow; quoting cannot be inferred", None, location)
        flags = _csv_quotes(original, location)
        if type(row) is RawRow:
            quoted = flags
        elif type(row) is MappedRow:
            if row.row_number != original.row_number or row.line_number != original.line_number:
                raise _fail(ErrorCode.SCHEMA_TYPE, "mapped CSV row and source location disagree", None, location)
            # Only unchanged selectors inherit lexical null semantics. Explicit
            # transforms/constants produce literal values; no lexeme is invented.
            for trace in row.field_traces:
                if (trace.selector == "source" and len(trace.source_fields) == 1
                        and all(op == "rename" for op in trace.operations)):
                    source = trace.source_fields[0]
                    if source in flags:
                        quoted[trace.target] = flags[source]
        else:
            raise _fail(ErrorCode.SCHEMA_TYPE, "CSV normalization needs RawRow or MappedRow with original spelling", None, location)
    return values, extras, quoted


def _state(value: object, *, csv_mode: bool, quoted: bool,
           tokens: tuple[str, ...]) -> str:
    if value is None:
        return "null"
    if type(value) is str:
        if csv_mode and not quoted and value == "":
            return "csv_unquoted_blank"
        if csv_mode and not quoted and value in tokens:
            return "csv_null_token"
        if value == "":
            return "csv_quoted_empty" if csv_mode and quoted else "empty_string"
        if not value.strip():
            return "blank_string"
    return "value"


def _timestamp(value: object, name: str, location: RowLocation) -> datetime:
    try:
        parsed = datetime.fromisoformat(value) if type(value) is str else value
        # Do not call arbitrary tzinfo hooks supplied as Python objects.
        if type(parsed) is not datetime or type(parsed.tzinfo) not in (timezone, ZoneInfo):
            raise ValueError
        return parsed.astimezone(timezone.utc)
    except (ValueError, TypeError, OverflowError):
        raise _fail(ErrorCode.SCHEMA_TYPE, "timestamp requires an explicit ISO 8601 timezone", name, location) from None


def _parent_list(value: object, *, csv_mode: bool, limits: ResourceLimits,
                 location: RowLocation) -> tuple[str, ...]:
    try:
        if type(value) is str and csv_mode:
            if value == "":
                return ()
            _check_depth(value, limits.max_json_depth)
            value = json.loads(value, object_pairs_hook=_unique_object,
                               parse_constant=_reject_constant, parse_float=_finite_float)
        if type(value) not in (list, tuple) or any(type(item) is not str for item in value):
            raise ValueError
        if limits.max_parent_list_length is not None and len(value) > limits.max_parent_list_length:
            raise ValueError
        # Keep duplicates and spelling. Resolution/deduplication belong to Step 6.
        return tuple(sorted(value))
    except (ValueError, TypeError, RecursionError):
        raise _fail(ErrorCode.PARENT_FORMAT, "parent_ids needs a bounded array of strings", "parent_ids", location) from None


def _field_value(name: str, value: object, state: str, *, csv_mode: bool,
                 options: NormalizationOptions, limits: ResourceLimits,
                 location: RowLocation) -> object:
    if value is None or state == "csv_null_token":
        return None
    if name == "parent_ids" and csv_mode and type(value) is str and value == "":
        return ()
    if state == "csv_unquoted_blank":
        return "" if name == "content" else None
    if type(value) is str and value == "":
        if name in OPTIONAL_IDENTIFIERS or name in ENUMS or name in ("weight", "generation", "human_reviewed", "timestamp"):
            return None
        if options.blank_as_null and name not in ("dataset_version", "record_id", "content"):
            return None
    if name == "timestamp":
        return _timestamp(value, name, location)
    if name == "parent_ids":
        return _parent_list(value, csv_mode=csv_mode, limits=limits, location=location)
    if name in ("weight", "generation") and csv_mode and type(value) is str:
        pattern = _FLOAT if name == "weight" else _INTEGER
        if not pattern.fullmatch(value):
            code = ErrorCode.WEIGHT_INVALID if name == "weight" else ErrorCode.SCHEMA_TYPE
            raise _fail(code, "numeric field is not in canonical notation", name, location)
        try:
            value = float(value) if name == "weight" else int(value)
        except (ValueError, OverflowError):
            raise _fail(ErrorCode.SCHEMA_TYPE, "numeric field cannot be represented", name, location) from None
    if name == "weight" and type(value) in (int, float):
        try:
            value = float(value)
            if not math.isfinite(value):
                raise ValueError
        except (ValueError, OverflowError):
            raise _fail(ErrorCode.WEIGHT_INVALID, "weight must be finite", name, location) from None
    if name == "human_reviewed" and csv_mode and type(value) is str:
        tokens = {"true": True, "false": False}
        if options.csv_boolean_compatibility:
            tokens.update({"1": True, "0": False, "yes": True, "no": False})
        if value.lower() not in tokens:
            raise _fail(ErrorCode.SCHEMA_TYPE, "review flag needs an approved boolean token", name, location)
        return tokens[value.lower()]
    return value


def _freeze(value: object) -> object:
    """Copy only plain data. No deepcopy, object hooks or implicit conversions."""
    if value is None or type(value) in (str, bool, int):
        return value
    if type(value) is float and math.isfinite(value):
        return value
    if type(value) is datetime and type(value.tzinfo) in (timezone, ZoneInfo):
        return value.astimezone(timezone.utc)
    if type(value) in (tuple, list):
        return tuple(_freeze(item) for item in value)
    if type(value) is dict and all(type(name) is str for name in value):
        return MappingProxyType({name: _freeze(item) for name, item in value.items()})
    raise CanonicalValidationError(ErrorCode.SCHEMA_TYPE, "preserved fields must be plain finite data")


def normalize_row(row: dict[str, object] | RawRow | MappedRow, *, kind: str,
                  file_format: FileFormat | None = None, source_row: RawRow | None = None,
                  options: NormalizationOptions | None = None,
                  limits: ResourceLimits | None = None,
                  location: RowLocation | None = None) -> CanonicalRow:
    """Normalize one supplied row, without loading data or certifying later capabilities.

    None file_format means already typed values (for example explicit mapping
    output); literal native strings are never interpreted as CSV null tokens.
    Mapped CSV requires source_row for unchanged-selector quoting evidence.
    Absent optional fields are not filled, except the documented content_type
    default and the minimum nullable parent_ids column. Field states retain the
    original absence, null, empty, and token distinctions.
    """
    fields = canonical_fields(kind)
    options, limits = _policy(options, limits)
    numbered = type(row) in (RawRow, MappedRow)
    loc = _location(location, row.row_number if numbered else None,
                    row.line_number if numbered else None)
    values, extra_source, quoted = _input(row, file_format, source_row, loc)
    result: dict[str, object] = {}
    states: dict[str, str] = {}
    for name in fields:
        if name not in values:
            states[name] = "absent"
            continue
        state = _state(values[name], csv_mode=file_format is FileFormat.CSV and name in quoted,
                       quoted=quoted.get(name, False), tokens=options.null_tokens)
        states[name] = state
        result[name] = _field_value(name, values[name], state, csv_mode=file_format is FileFormat.CSV,
                                    options=options, limits=limits, location=loc)
    if "record_key" in values:
        result["record_key"] = values["record_key"]
    defaults: list[str] = []
    if kind == "records" and "content_type" not in result:
        result["content_type"] = "text/plain"
        defaults.append("content_type")
    if kind == "provenance" and "parent_ids" not in result:
        result["parent_ids"] = None
        # None preserves absence without asserting that no parents exist.
    key = validate_canonical_values(result, kind=kind, location=loc,
                                    content_mode=options.content_mode,
                                    max_content_bytes=limits.max_content_bytes)
    result["record_key"] = str(key)
    ignored = tuple(sorted(name for name in values if name not in fields and name != "record_key"))
    extras: dict[str, object] = {}
    if options.preserve_extras:
        if type(extra_source) is not dict or any(type(name) is not str for name in extra_source):
            raise _fail(ErrorCode.SCHEMA_TYPE, "mapped extras must use a plain dictionary", None, loc, key)
        if set(extra_source) & set(ignored):
            raise _fail(ErrorCode.SCHEMA_TYPE, "extras sources collide; resolve their namespace explicitly", None, loc, key)
        extras = dict(extra_source)
        extras.update({name: values[name] for name in ignored})
    try:
        frozen_values = _freeze(result)
        frozen_extras = _freeze(extras)
    except (CanonicalValidationError, RecursionError):
        raise _fail(ErrorCode.SCHEMA_TYPE, "canonical or preserved fields contain unsupported data", None, loc, key) from None
    return CanonicalRow(kind, key, frozen_values, MappingProxyType(states), frozen_extras,
                        ignored, tuple(defaults), loc)


def normalize_table(table: LoadedTable, *, options: NormalizationOptions | None = None,
                    limits: ResourceLimits | None = None) -> tuple[CanonicalRow, ...]:
    """Normalize an already loaded same-kind table. No load, join or mapping runs."""
    if type(table) is not LoadedTable:
        raise CanonicalValidationError(ErrorCode.SCHEMA_TYPE, "normalize_table requires a LoadedTable")
    role = table.inventory.role
    if role in (FileRole.RECORDS_PRIMARY, FileRole.RECORDS_COMPARE):
        kind = "records"
    elif role is FileRole.PROVENANCE_MANIFEST:
        kind = "provenance"
    else:
        raise CanonicalValidationError(ErrorCode.CONFIG_INVALID, "table role must be records or provenance")
    options, limits = _policy(options, limits)
    required = RECORD_REQUIRED if kind == "records" else PROVENANCE_REQUIRED
    for name in required:
        if name not in table.inventory.fields:
            raise _fail(ErrorCode.SCHEMA_REQUIRED_FIELD, "required canonical column is missing", name,
                        RowLocation(role, str(table.inventory.path)))
    rows = tuple(normalize_row(
        row, kind=kind, file_format=table.inventory.file_format, options=options, limits=limits,
        location=RowLocation(role, str(table.inventory.path), row.row_number, row.line_number),
    ) for row in table.rows)
    validate_unique_keys(rows, kind=kind)
    return stable_record_order(rows)
