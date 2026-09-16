"""Validate canonical row fields and same-kind record identity.

Owner IDs:
    PR-001, PR-004 row validity, exact joins and validation coverage, PR-008 list types only,
    PR-009 declared generation types only; PR-007 remains deferred.

Inputs:
    Serialization-normalized field dictionaries, row locations and explicit content mode.

Outputs:
    Valid RecordKey values or content-safe CanonicalValidationError diagnostics.

Assumptions:
    Input normalization and explicit mapping precede canonical field checks.
    Source categories, grounding and review flags are independent declarations.

Limits:
    No source shares, closure bounds, chronology, parent resolution, generation
    derivation, lineage depth, graph, metric, capability classification or report.
    A valid local_ref string does not certify a safe or existing referenced file.

Current phase status:
    Phase 2 Step 5 provenance join and validation coverage. No analytical behavior.
"""

from __future__ import annotations

import math
from datetime import datetime, timezone
from types import MappingProxyType

from ..errors import CanonicalValidationError, ErrorCode, WarningCode
from ..models import (
    CanonicalRow, ContentMode, ExternalGrounding, ProvenanceConfidence,
    RecordKey, RowLocation, SourceType, Transformation, FileRole,
    ProvenanceAssessment, ProvenanceMatch, ProvenanceJoinResult,
    ValidationCoverage, ValidationMessage, ValidationSeverity,
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
    _validate_present_fields(values, fields, location, key)
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


def _validate_present_fields(values: dict[str, object], fields: tuple[str, ...],
                             location: RowLocation, key: RecordKey) -> None:
    """Shared Step 4 field checks; absent required fields are checked by callers."""
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


def _join_location(location: RowLocation) -> RowLocation:
    """Validate location types before using them in content-safe diagnostics."""
    if type(location) is not RowLocation:
        raise CanonicalValidationError(ErrorCode.SCHEMA_TYPE, "location must use RowLocation")
    if location.file_role is not None and type(location.file_role) is not FileRole:
        raise CanonicalValidationError(ErrorCode.SCHEMA_TYPE, "location role must use FileRole")
    if location.file_path is not None and type(location.file_path) is not str:
        raise CanonicalValidationError(ErrorCode.SCHEMA_TYPE, "location path must be text")
    for number in (location.row_number, location.line_number):
        if number is not None and (type(number) is not int or number < 1):
            raise CanonicalValidationError(ErrorCode.SCHEMA_TYPE, "location numbers must be positive integers")
    return location


def _join_fields(values: object, location: RowLocation) -> dict[str, object]:
    """Copy typed canonical field containers; do not parse, coerce or infer."""
    if type(values) not in (dict, MappingProxyType):
        raise _fail(ErrorCode.SCHEMA_TYPE, "join fields must be a plain or read-only dictionary", None, location)
    if any(type(name) is not str for name in values):
        raise _fail(ErrorCode.SCHEMA_TYPE, "join field names must be literal strings", None, location)
    return dict(values)


def _join_identity(values: dict[str, object], location: RowLocation) -> RecordKey:
    """Require exact join fields without filling any provenance metadata."""
    for name in ("dataset_version", "record_id"):
        value = values.get(name)
        if value is None:
            raise _fail(ErrorCode.SCHEMA_REQUIRED_FIELD, "required join field is missing", name, location)
        maximum = 256 if name == "dataset_version" else 512
        if (type(value) is not str or not value or value != value.strip()
                or len(value) > maximum or "::" in value or "\x00" in value):
            raise _fail(ErrorCode.SCHEMA_TYPE, "join identifier violates canonical identity", name, location)
    key = RecordKey(values["dataset_version"], values["record_id"])
    if "record_key" in values and (type(values["record_key"]) is not str or values["record_key"] != str(key)):
        raise _fail(ErrorCode.SCHEMA_TYPE, "supplied record_key disagrees with join fields", "record_key", location, key)
    return key


def assess_provenance_row(
    row: CanonicalRow | ProvenanceAssessment | dict[str, object], *,
    location: RowLocation = RowLocation(),
) -> ProvenanceAssessment:
    """Assess already typed provenance fields, including incomplete required sets.

    RawRow and MappedRow must first undergo serialization normalization. This
    function never interprets CSV tokens or substitutes unknown for missing.
    Invalid present values fail. Absent/null non-identity required fields remain
    in an explicitly incomplete assessment for separate row/field coverage.
    """
    wrapped = type(row) in (CanonicalRow, ProvenanceAssessment)
    if type(row) is CanonicalRow and row.kind != "provenance":
        raise CanonicalValidationError(ErrorCode.SCHEMA_TYPE, "provenance input has the wrong row kind")
    loc = _join_location(row.location if wrapped else location)
    values = _join_fields(row.values if wrapped else row, loc)
    if set(values) - set(PROVENANCE_FIELDS) - {"record_key"}:
        raise _fail(ErrorCode.SCHEMA_TYPE, "unexpected provenance field; map before joining", None, loc)
    key = _join_identity(values, loc)
    if wrapped and (type(row.record_key) is not RecordKey or row.record_key != key):
        raise _fail(ErrorCode.SCHEMA_TYPE, "row identity disagrees with its fields", "record_key", loc, key)
    _validate_present_fields(values, PROVENANCE_FIELDS, loc, key)
    missing = tuple(name for name in PROVENANCE_REQUIRED if name not in values or values[name] is None)
    # Invalid required fields cannot be smuggled in as a row certified by Step 4.
    if type(row) is CanonicalRow and missing:
        raise _fail(ErrorCode.SCHEMA_REQUIRED_FIELD, "canonical provenance row is incomplete", missing[0], loc, key)
    if type(values.get("parent_ids")) is list:
        values["parent_ids"] = tuple(values["parent_ids"])
    return ProvenanceAssessment(key, MappingProxyType(values), loc, missing, not missing,
                                values.get("external_grounding") in ("yes", "no"))


def _join_message(code: str, severity: ValidationSeverity, message: str,
                  key: RecordKey, location: RowLocation,
                  field: str | None = None) -> ValidationMessage:
    return ValidationMessage(code, severity, message, location.file_role,
                             location.file_path, field, key,
                             location.row_number if location.row_number is not None else location.line_number)


def _join_options(dataset_versions: tuple[str, ...] | None, strict_mode: bool,
                  strict_warning_codes: tuple[str, ...]) -> tuple[str, ...]:
    """Validate explicit scope/promotion declarations without config inference."""
    if dataset_versions is not None:
        if (type(dataset_versions) is not tuple or not dataset_versions
                or any(type(v) is not str or not v for v in dataset_versions)
                or len(set(dataset_versions)) != len(dataset_versions)):
            raise CanonicalValidationError(ErrorCode.CONFIG_INVALID, "dataset scope must name unique versions")
    if type(strict_mode) is not bool or type(strict_warning_codes) is not tuple:
        raise CanonicalValidationError(ErrorCode.CONFIG_INVALID, "strict warning promotion must be explicit")
    known = {code.value for code in WarningCode}
    if (any(type(code) is not str or code not in known for code in strict_warning_codes)
            or len(set(strict_warning_codes)) != len(strict_warning_codes)):
        raise CanonicalValidationError(ErrorCode.CONFIG_INVALID, "strict warning codes must be unique approved codes")
    return tuple(sorted(strict_warning_codes)) if strict_mode else ()


def join_provenance(
    records: tuple[CanonicalRow, ...],
    provenance: tuple[CanonicalRow | ProvenanceAssessment, ...] | None = None, *,
    dataset_versions: tuple[str, ...] | None = None,
    strict_mode: bool = False,
    strict_warning_codes: tuple[str, ...] = (),
) -> ProvenanceJoinResult:
    """Validate one-to-one attachment and three unweighted coverage measures.

    records is the full loaded valid-record scope. dataset_versions optionally
    selects a subset for coverage. Every supplied provenance identity must match
    the full record scope, including rows outside the selected versions. Missing
    provenance is None in each match, never a synthesized unknown declaration.
    No field normalization, parent lookup, source-share calculation, report,
    content reference access, or observability classification occurs here.
    """
    promoted = _join_options(dataset_versions, strict_mode, strict_warning_codes)
    if type(records) is not tuple or (provenance is not None and type(provenance) is not tuple):
        raise CanonicalValidationError(ErrorCode.SCHEMA_TYPE, "join inputs must use explicit row tuples")
    validate_unique_keys(records, kind="records")
    record_index: dict[RecordKey, tuple[dict[str, object], RowLocation]] = {}
    for record in records:
        loc = _join_location(record.location)
        values = _join_fields(record.values, loc)
        key = validate_canonical_values(values, kind="records", location=loc)
        if key != record.record_key:
            raise _fail(ErrorCode.SCHEMA_TYPE, "record identity disagrees with its fields", "record_key", loc, key)
        record_index[key] = (values, loc)
    loaded_versions = {key.dataset_version for key in record_index}
    selected_versions = loaded_versions if dataset_versions is None else set(dataset_versions)
    if selected_versions - loaded_versions:
        raise CanonicalValidationError(ErrorCode.CONFIG_INVALID, "selected dataset version is not loaded")
    scope = tuple(key for key in sorted(record_index) if key.dataset_version in selected_versions)
    if not scope:
        raise CanonicalValidationError(ErrorCode.EMPTY_DATASET, "no valid records in selected join scope")
    provenance_index: dict[RecordKey, ProvenanceAssessment] = {}
    for row in provenance or ():
        if type(row) not in (CanonicalRow, ProvenanceAssessment):
            raise CanonicalValidationError(ErrorCode.SCHEMA_TYPE, "supply canonical or explicitly assessed provenance rows")
        assessed = assess_provenance_row(row)
        key = assessed.record_key
        if key in provenance_index:
            raise _fail(ErrorCode.PROVENANCE_DUPLICATE_ROW, "multiple provenance rows have one composite identity",
                        "record_id", assessed.location, key)
        if key not in record_index:
            raise _fail(ErrorCode.PROVENANCE_UNMATCHED_ROW, "provenance has no matching loaded record",
                        "record_id", assessed.location, key)
        provenance_index[key] = assessed
    matches: list[ProvenanceMatch] = []
    missing: list[RecordKey] = []
    messages: list[ValidationMessage] = []
    # Required-field errors in supplied provenance survive scope selection.
    # Coverage remains scoped; malformed input is never silently excused by it.
    for key in sorted(provenance_index):
        assessed = provenance_index[key]
        for name in assessed.missing_required_fields:
            messages.append(_join_message(ErrorCode.SCHEMA_REQUIRED_FIELD.value, ValidationSeverity.ERROR,
                                           "matched provenance row lacks a required field", key,
                                           assessed.location, name))
    matched_count = required_count = grounding_count = 0
    for key in scope:
        record_values, loc = record_index[key]
        assessed = provenance_index.get(key)
        metadata = MappingProxyType({name: record_values[name] for name in ("batch_id", "timestamp")
                                     if name in record_values})
        conflicts: tuple[str, ...] = ()
        if assessed is None:
            missing.append(key)
            code = WarningCode.PROVENANCE_MISSING_ROW.value
            severity = ValidationSeverity.ERROR if code in promoted else ValidationSeverity.WARNING
            messages.append(_join_message(code, severity, "record has no matching provenance row", key, loc))
        else:
            matched_count += 1
            required_count += int(assessed.required_fields_valid)
            grounding_count += int(assessed.grounding_known)
            for name, expected, code, message in (
                ("external_grounding", "unknown", WarningCode.GROUNDING_UNKNOWN.value,
                 "matched provenance declares unknown grounding"),
                ("provenance_confidence", "estimated", WarningCode.PROVENANCE_ESTIMATED.value,
                 "matched provenance confidence is estimated"),
            ):
                if assessed.values.get(name) == expected:
                    severity = ValidationSeverity.ERROR if code in promoted else ValidationSeverity.WARNING
                    messages.append(_join_message(code, severity, message, key, assessed.location, name))
            conflicts = tuple(name for name in ("batch_id", "timestamp")
                              if name in metadata and name in assessed.values
                              and metadata[name] is not None and assessed.values[name] is not None
                              and metadata[name] != assessed.values[name])
        matches.append(ProvenanceMatch(key, assessed, loc, metadata, conflicts))
    denominator = len(scope)
    denominator_name = "all_valid_records_in_selected_dataset_scope"
    return ProvenanceJoinResult(
        tuple(sorted(selected_versions)), scope, provenance is not None, tuple(matches), tuple(missing),
        ValidationCoverage(matched_count, denominator, denominator_name),
        ValidationCoverage(required_count, denominator, denominator_name),
        ValidationCoverage(grounding_count, denominator, denominator_name),
        tuple(messages), promoted,
    )
