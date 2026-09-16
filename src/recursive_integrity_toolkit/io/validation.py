"""Validate canonical row fields and same-kind record identity.

Owner IDs:
    PR-001, PR-004 row validity only, PR-008 list types only,
    PR-009 declared generation types only; PR-007 remains deferred.

Inputs:
    Serialization-normalized field dictionaries, row locations and explicit content mode.

Outputs:
    Valid RecordKey values or content-safe CanonicalValidationError diagnostics.

Assumptions:
    Input normalization and explicit mapping precede canonical field checks.
    Source categories, grounding and review flags are independent declarations.

Limits:
    No provenance joins, coverage, chronology, parent resolution, generation
    derivation, lineage depth, graph, metric, capability classification or report.
    A valid local_ref string does not certify a safe or existing referenced file.

Current phase status:
    Phase 2 Step 4 canonical row and identity validation. No analytical behavior.
"""

from __future__ import annotations

import math
from datetime import datetime, timezone

from ..errors import CanonicalValidationError, ErrorCode
from ..models import (
    CanonicalRow, ContentMode, ExternalGrounding, ProvenanceConfidence,
    RecordKey, RowLocation, SourceType, Transformation,
)


RECORD_REQUIRED = ("dataset_version", "record_id", "content")
PROVENANCE_REQUIRED = (
    "dataset_version", "record_id", "source_type", "provenance_confidence", "external_grounding",
)
RECORD_FIELDS = RECORD_REQUIRED + (
    "topic", "label", "timestamp", "weight", "embedding_ref", "batch_id",
    "notes", "content_type", "language",
)
PROVENANCE_FIELDS = PROVENANCE_REQUIRED + (
    "parent_ids", "generator_id", "generator_version", "transformation", "generation",
    "human_reviewed", "batch_id", "timestamp", "grounding_evidence_ref", "source_uri",
    "license_id", "notes",
)
ENUMS = {
    "source_type": tuple(item.value for item in SourceType),
    "provenance_confidence": tuple(item.value for item in ProvenanceConfidence),
    "external_grounding": tuple(item.value for item in ExternalGrounding),
    "transformation": tuple(item.value for item in Transformation),
}
OPTIONAL_IDENTIFIERS = (
    "embedding_ref", "batch_id", "generator_id", "generator_version",
    "grounding_evidence_ref", "source_uri", "license_id",
)


def _fail(code: ErrorCode, message: str, field: str | None, location: RowLocation,
          key: RecordKey | None = None) -> CanonicalValidationError:
    return CanonicalValidationError(
        code, message, field=field,
        file_role=location.file_role.value if location.file_role is not None else None,
        file_path=location.file_path, row_number=location.row_number,
        line_number=location.line_number, record_key=str(key) if key is not None else None,
    )


def canonical_fields(kind: str) -> tuple[str, ...]:
    """Return the closed row schema, never infer a kind from field content."""
    if type(kind) is str and kind == "records":
        return RECORD_FIELDS
    if type(kind) is str and kind == "provenance":
        return PROVENANCE_FIELDS
    raise CanonicalValidationError(ErrorCode.CONFIG_INVALID, "row kind must be records or provenance")


def validate_canonical_values(values: dict[str, object], *, kind: str,
                              location: RowLocation = RowLocation(),
                              content_mode: ContentMode = ContentMode.INLINE,
                              max_content_bytes: int | None = None) -> RecordKey:
    """Validate row-local fields only. No cross-table evidence is consulted."""
    fields = canonical_fields(kind)
    if type(values) is not dict or any(type(name) is not str for name in values):
        raise _fail(ErrorCode.SCHEMA_TYPE, "canonical values must be a plain field dictionary", None, location)
    if set(values) - set(fields) - {"record_key"}:
        raise _fail(ErrorCode.SCHEMA_TYPE, "unexpected canonical field; map it or preserve it as extras", None, location)
    required = RECORD_REQUIRED if kind == "records" else PROVENANCE_REQUIRED
    for name in required:
        if name not in values or values[name] is None:
            raise _fail(ErrorCode.SCHEMA_REQUIRED_FIELD, "required canonical field is missing", name, location)
    for name in ("dataset_version", "record_id"):
        if type(values[name]) is not str:
            raise _fail(ErrorCode.SCHEMA_TYPE, "identifier must be an explicit string", name, location)
        maximum = 256 if name == "dataset_version" else 512
        value = values[name]
        if not value or value != value.strip() or len(value) > maximum or "::" in value or "\x00" in value:
            raise _fail(ErrorCode.SCHEMA_TYPE, "identifier violates the canonical identity contract", name, location)
    key = RecordKey(values["dataset_version"], values["record_id"])
    if "record_key" in values and (type(values["record_key"]) is not str or values["record_key"] != str(key)):
        raise _fail(ErrorCode.SCHEMA_TYPE, "supplied record_key disagrees with canonical identity", "record_key", location, key)
    for name in fields:
        value = values.get(name)
        if value is None:
            continue
        if name in ENUMS:
            if type(value) is not str or value not in ENUMS[name]:
                raise _fail(ErrorCode.SCHEMA_ENUM, "enum value must match the approved spelling", name, location, key)
        elif name == "generation":
            if type(value) is not int or value < 0:
                raise _fail(ErrorCode.SCHEMA_TYPE, "generation must be a nonnegative integer", name, location, key)
        elif name == "human_reviewed":
            if type(value) is not bool:
                raise _fail(ErrorCode.SCHEMA_TYPE, "review flag must be a boolean", name, location, key)
        elif name == "weight":
            if type(value) not in (int, float):
                raise _fail(ErrorCode.WEIGHT_INVALID, "weight must be a finite nonnegative number", name, location, key)
            try:
                valid = math.isfinite(value) and value >= 0
            except OverflowError:
                valid = False
            if not valid:
                raise _fail(ErrorCode.WEIGHT_INVALID, "weight must be a finite nonnegative number", name, location, key)
        elif name == "parent_ids":
            if type(value) not in (tuple, list) or any(type(item) is not str for item in value):
                raise _fail(ErrorCode.PARENT_FORMAT, "parent_ids must be an array of strings or null", name, location, key)
        elif name == "timestamp":
            if type(value) is not datetime or value.tzinfo is not timezone.utc:
                raise _fail(ErrorCode.SCHEMA_TYPE, "timestamp must be a UTC-aware datetime", name, location, key)
        elif type(value) is not str:
            raise _fail(ErrorCode.SCHEMA_TYPE, "canonical string field has an invalid type", name, location, key)
    if kind == "records":
        if type(content_mode) is not ContentMode:
            raise _fail(ErrorCode.CONFIG_INVALID, "content mode must be explicit and approved", "content", location, key)
        content = values["content"]
        if not content.strip():
            raise _fail(ErrorCode.RECORD_EMPTY_CONTENT, "required content cannot be empty or whitespace-only", "content", location, key)
        try:
            size = len(content.encode("utf-8"))
        except UnicodeEncodeError:
            raise _fail(ErrorCode.SCHEMA_TYPE, "content must be valid Unicode text", "content", location, key) from None
        if max_content_bytes is not None:
            if type(max_content_bytes) is not int or max_content_bytes <= 0:
                raise _fail(ErrorCode.CONFIG_INVALID, "max_content_bytes must be a positive integer", "content", location, key)
            if content_mode is ContentMode.INLINE and size > max_content_bytes:
                raise _fail(ErrorCode.SCHEMA_TYPE, "inline content exceeds max_content_bytes", "content", location, key)
    return key


def validate_unique_keys(rows: tuple[CanonicalRow, ...], *, kind: str) -> None:
    """Reject duplicate keys within the supplied same-kind scope; never deduplicate."""
    canonical_fields(kind)
    if type(rows) is not tuple:
        raise CanonicalValidationError(ErrorCode.SCHEMA_TYPE, "row scope must be an explicit tuple")
    seen: set[RecordKey] = set()
    for row in rows:
        if type(row) is not CanonicalRow or row.kind != kind or type(row.record_key) is not RecordKey:
            raise CanonicalValidationError(ErrorCode.SCHEMA_TYPE, "identity scope contains an incompatible row")
        if row.record_key in seen:
            code = ErrorCode.RECORD_DUPLICATE_ID if kind == "records" else ErrorCode.PROVENANCE_DUPLICATE_ROW
            raise _fail(code, "duplicate composite identity in the supplied scope", "record_id", row.location, row.record_key)
        seen.add(row.record_key)
