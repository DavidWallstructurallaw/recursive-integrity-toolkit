"""Validate canonical rows, provenance attachment and declared dependency inputs.

Owner IDs:
    PR-001, PR-004 row validity, exact joins and validation coverage; PR-007 chronology;
    PR-008 immediate-reference validation; PR-009 generation consistency.

Inputs:
    Serialization-normalized fields, locations and explicit content mode; loaded
    identities, declared version order, immediate parents and generation values.

Outputs:
    Row-valid identities, provenance joins, VersionOrderResult, immediate parent
    validation and GenerationValidationResult, with content-safe diagnostics.

Assumptions:
    Input normalization and explicit mapping precede canonical field checks.
    Source categories, grounding and review flags are independent declarations.

Limits:
    No source shares, closure bounds, lineage depth, general graph analysis, roots,
    ancestors, metric, capability classification or report.
    A valid local_ref string does not certify a safe or existing referenced file.

Current phase status:
    Phase 2 Step 6 chronology, parent references and generation validation. No analytical behavior.
"""

from __future__ import annotations

import json
import math
from datetime import datetime, timezone
from types import MappingProxyType

from ..errors import CanonicalValidationError, ErrorCode, WarningCode
from ..models import (
    CanonicalRow, ContentMode, ExternalGrounding, ProvenanceConfidence,
    RecordKey, RowLocation, SourceType, Transformation, FileRole,
    ProvenanceAssessment, ProvenanceMatch, ProvenanceJoinResult,
    ValidationCoverage, ValidationMessage, ValidationSeverity, ParentResolutionStatus,
    VersionOrderResult, ParentReference, ParentValidationResult,
    GenerationAssessment, GenerationValidationResult,
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


# Phase 2 Step 6: input chronology, immediate references and generation checks.
def _version_failure(message: str, field: str = "version_order") -> CanonicalValidationError:
    return CanonicalValidationError(ErrorCode.VERSION_ORDER_CONFLICT, message,
                                    file_role=FileRole.VERSION_ORDER.value, field=field)


def _version_labels(value: object, *, field: str, allow_empty: bool = False) -> tuple[str, ...]:
    if type(value) not in (list, tuple) or (not value and not allow_empty):
        raise _version_failure("version order requires an explicit nonempty sequence", field)
    for label in value:
        if (type(label) is not str or not label or label != label.strip()
                or len(label) > 256 or "::" in label or "\x00" in label):
            raise _version_failure("version identifier violates the canonical contract", field)
    if len(set(value)) != len(value):
        raise _version_failure("a version appears more than once", field)
    return tuple(value)


def _version_map(value: object, field: str) -> dict[str, object]:
    if type(value) not in (dict, MappingProxyType) or not value:
        raise _version_failure("ordering map must be a nonempty explicit dictionary", field)
    _version_labels(tuple(value), field=field)
    return dict(value)


def _version_timestamp(value: object) -> datetime:
    if type(value) is not str:
        raise _version_failure("version timestamp must be explicit ISO 8601 text", "version_timestamps")
    try:
        stamp = datetime.fromisoformat(value)
        if stamp.tzinfo is None:
            raise ValueError
        return stamp.astimezone(timezone.utc)
    except (ValueError, OverflowError):
        raise _version_failure("version timestamp needs a valid explicit timezone", "version_timestamps") from None


def resolve_version_order(
    loaded_versions: tuple[str, ...], *, document: dict[str, object] | None = None,
    invocation_order: tuple[str, ...] | None = None,
) -> VersionOrderResult:
    """Validate declared ordering sources and retain their exact provenance.

    document uses version_order, version_rank, version_timestamps and optional
    timestamp_tiebreak. Already parsed input is required; no file is opened.
    Every supplied source must cover the loaded scope. Extra explicitly named
    versions are retained. All shared version pairs must agree across sources.
    Integer ranks may have gaps. No chronology is inferred from spelling.
    """
    loaded = _version_labels(loaded_versions, field="loaded_versions")
    if type(loaded_versions) is not tuple:
        raise _version_failure("loaded versions must be an explicit tuple", "loaded_versions")
    if document is not None:
        if type(document) not in (dict, MappingProxyType):
            raise _version_failure("ordering document must be a plain dictionary")
        if not document:
            raise _version_failure("an explicitly supplied ordering document cannot be empty")
    else:
        document = {}
    allowed = {"version_order", "version_rank", "version_timestamps", "timestamp_tiebreak"}
    if any(type(name) is not str for name in document) or set(document) - allowed:
        raise _version_failure("ordering document contains an unsupported field")
    frozen: dict[str, object] = {}
    sources: dict[str, tuple[str, ...]] = {}
    if "version_order" in document:
        order = _version_labels(document["version_order"], field="version_order")
        frozen["version_order"] = order
        sources["explicit_version_order"] = order
    if "version_rank" in document:
        ranks = _version_map(document["version_rank"], "version_rank")
        if any(type(rank) is not int for rank in ranks.values()) or len(set(ranks.values())) != len(ranks):
            raise _version_failure("version ranks must be unique integers", "version_rank")
        frozen["version_rank"] = MappingProxyType(ranks)
        sources["integer_rank"] = tuple(name for rank, name in sorted((rank, name) for name, rank in ranks.items()))
    invoked = None if invocation_order is None else _version_labels(invocation_order, field="invocation_order")
    if invocation_order is not None and type(invocation_order) is not tuple:
        raise _version_failure("invocation order must be an explicit tuple", "invocation_order")
    tiebreak = None
    if "timestamp_tiebreak" in document:
        if "version_timestamps" not in document:
            raise _version_failure("timestamp tie-break requires timestamps", "timestamp_tiebreak")
        tiebreak = _version_labels(document["timestamp_tiebreak"], field="timestamp_tiebreak")
        frozen["timestamp_tiebreak"] = tiebreak
    if "version_timestamps" in document:
        timestamp_text = _version_map(document["version_timestamps"], "version_timestamps")
        times = {name: _version_timestamp(text) for name, text in timestamp_text.items()}
        frozen["version_timestamps"] = MappingProxyType(timestamp_text)
        # A separately supplied explicit order is an explicit tie-break as well.
        if tiebreak is None:
            tiebreak = next(iter(sources.values()), invoked)
        tie_positions = {} if tiebreak is None else {name: i for i, name in enumerate(tiebreak)}
        grouped: dict[datetime, list[str]] = {}
        for name, stamp in times.items():
            grouped.setdefault(stamp, []).append(name)
        timed_order: list[str] = []
        for stamp in sorted(grouped):
            group = grouped[stamp]
            if len(group) == 1:
                timed_order.extend(group)
            else:
                if any(name not in tie_positions for name in group):
                    raise _version_failure("equal timestamps require an explicit covering tie-break", "version_timestamps")
                timed_order.extend(name for _, name in sorted((tie_positions[name], name) for name in group))
        sources["version_timestamps"] = tuple(timed_order)
    if invoked is not None:
        sources["invocation_order"] = invoked
    for name, order in sources.items():
        if set(loaded) - set(order):
            raise _version_failure("ordering source omits a loaded version", name)
    all_orders = tuple(sources.values())
    for i, left in enumerate(all_orders):
        for right in all_orders[i + 1:]:
            shared = set(left) & set(right)
            if tuple(v for v in left if v in shared) != tuple(v for v in right if v in shared):
                raise _version_failure("explicit ordering sources disagree")
    messages: tuple[ValidationMessage, ...] = ()
    if sources:
        chosen_source = next(iter(sources))
        chosen_order = sources[chosen_source]
    elif len(loaded) == 1:
        chosen_source, chosen_order = "single_version", loaded
    else:
        chosen_source, chosen_order = "unavailable", ()
        messages = (ValidationMessage(WarningCode.VERSION_ORDER_MISSING.value,
                    ValidationSeverity.WARNING, "multiple versions lack ordering evidence",
                    FileRole.VERSION_ORDER, field="version_order"),)
    return VersionOrderResult(tuple(sorted(loaded)), chosen_order, chosen_source,
                              MappingProxyType(dict(sources)), MappingProxyType(frozen), invoked, messages)


def _checked_order(order: VersionOrderResult | None, loaded: tuple[str, ...]) -> VersionOrderResult:
    if order is None:
        return resolve_version_order(loaded)
    if type(order) is not VersionOrderResult:
        raise _version_failure("ordering evidence must use VersionOrderResult")
    declared_loaded = _version_labels(order.loaded_versions, field="loaded_versions")
    if type(order.loaded_versions) is not tuple or declared_loaded != tuple(sorted(loaded)):
        raise _version_failure("ordering evidence does not match the loaded version scope")
    if type(order.declarations) not in (dict, MappingProxyType):
        raise _version_failure("ordering declarations must be a plain dictionary")
    # Stored source labels and resolved flags never replace the declarations.
    return resolve_version_order(loaded, document=order.declarations or None,
                                 invocation_order=order.invocation_order)


def _parent_keys(keys: tuple[RecordKey, ...]) -> tuple[RecordKey, ...]:
    if type(keys) is not tuple or not keys:
        raise CanonicalValidationError(ErrorCode.EMPTY_DATASET, "parent lookup needs a nonempty explicit record-key tuple")
    seen: set[RecordKey] = set()
    for key in keys:
        if (type(key) is not RecordKey or type(key.dataset_version) is not str
                or type(key.record_id) is not str):
            raise CanonicalValidationError(ErrorCode.SCHEMA_TYPE, "parent lookup requires canonical record keys")
        try:
            valid = RecordKey(key.dataset_version, key.record_id)
        except (TypeError, ValueError):
            raise CanonicalValidationError(ErrorCode.SCHEMA_TYPE, "invalid record identity in parent lookup") from None
        if valid in seen:
            raise CanonicalValidationError(ErrorCode.RECORD_DUPLICATE_ID, "duplicate record identity in parent lookup")
        seen.add(valid)
    return tuple(sorted(seen))


def parse_parent_ids(value: object, *, csv_encoded: bool = False,
                     max_parent_list_length: int | None = None) -> tuple[str, ...] | None:
    """Parse the list container only. Null stays null; a blank CSV field is empty.

    Already decoded CSV values must have passed the Step 4 null-token policy.
    Native JSONL/Parquet strings are scalar errors, never implicitly reparsed.
    Reference spellings are validated separately. No parent lookup occurs here.
    """
    if type(csv_encoded) is not bool or (max_parent_list_length is not None and
            (type(max_parent_list_length) is not int or max_parent_list_length < 1)):
        raise CanonicalValidationError(ErrorCode.CONFIG_INVALID, "parent parsing options must be explicit")
    if value is None:
        return None
    if csv_encoded:
        if type(value) is not str:
            raise CanonicalValidationError(ErrorCode.PARENT_FORMAT, "CSV parents require a JSON-array string")
        if value == "":
            return ()
        try:
            value = json.loads(value)
        except (ValueError, RecursionError):
            raise CanonicalValidationError(ErrorCode.PARENT_FORMAT, "invalid parent-list JSON") from None
    if type(value) not in (tuple, list) or any(type(item) is not str for item in value):
        raise CanonicalValidationError(ErrorCode.PARENT_FORMAT, "parent declaration must be an array of strings")
    if max_parent_list_length is not None and len(value) > max_parent_list_length:
        raise CanonicalValidationError(ErrorCode.PARENT_FORMAT, "parent declaration exceeds its explicit length limit")
    return tuple(value)


def _reference_key(text: str, location: RowLocation, child: RecordKey) -> RecordKey | None:
    if not text or text != text.strip() or "\x00" in text:
        raise _fail(ErrorCode.PARENT_FORMAT, "invalid parent reference spelling", "parent_ids", location, child)
    if "::" in text:
        try:
            return RecordKey.parse(text)
        except (TypeError, ValueError):
            raise _fail(ErrorCode.PARENT_FORMAT, "invalid composite parent reference", "parent_ids", location, child) from None
    if len(text) > 512:
        raise _fail(ErrorCode.PARENT_FORMAT, "bare parent identifier exceeds its length limit", "parent_ids", location, child)
    return None


def _parent_notice(code: WarningCode, message: str, child: RecordKey,
                   location: RowLocation, promoted: tuple[str, ...]) -> ValidationMessage:
    severity = ValidationSeverity.ERROR if code.value in promoted else ValidationSeverity.WARNING
    return _join_message(code.value, severity, message, child, location, "parent_ids")


def _parent_lookup(keys: tuple[RecordKey, ...], order: VersionOrderResult
                   ) -> tuple[set[RecordKey], dict[str, list[RecordKey]], dict[str, int]]:
    """Flat identity indexes only; no adjacency map or graph traversal."""
    by_id: dict[str, list[RecordKey]] = {}
    for key in keys:
        by_id.setdefault(key.record_id, []).append(key)
    return set(keys), by_id, {version: i for i, version in enumerate(order.order)}


def _resolve_parent_list(child: RecordKey, values: tuple[str, ...] | None,
                         lookup: tuple[set[RecordKey], dict[str, list[RecordKey]], dict[str, int]],
                         location: RowLocation, promoted: tuple[str, ...]) -> ParentValidationResult:
    loaded, by_id, positions = lookup
    messages: list[ValidationMessage] = []
    grouped: dict[tuple[str, str], tuple[RecordKey | None, list[str], bool, str]] = {}
    graph_deferred = False
    for text in sorted(values or ()):
        parsed = _reference_key(text, location, child)
        bare = parsed is None
        if bare:
            candidates = by_id.get(text, [])
            if len(candidates) > 1:
                raise _fail(ErrorCode.PARENT_AMBIGUOUS, "bare parent matches multiple loaded records", "parent_ids", location, child)
            parsed = candidates[0] if candidates else None
        resolved = parsed in loaded if parsed is not None else False
        if parsed == child:
            raise _fail(ErrorCode.LINEAGE_CYCLE, "direct self-parent reference is invalid input", "parent_ids", location, child)
        temporal = "unavailable"
        if parsed is not None:
            if parsed.dataset_version == child.dataset_version:
                temporal = "same_version"
                graph_deferred = True
            elif parsed.dataset_version in positions and child.dataset_version in positions:
                if positions[parsed.dataset_version] > positions[child.dataset_version]:
                    raise _fail(ErrorCode.PARENT_FUTURE_VERSION, "parent refers to a later declared version", "parent_ids", location, child)
                temporal = "earlier_version"
        token = ("key", str(parsed)) if parsed is not None else ("bare", text)
        if token in grouped:
            grouped[token][1].append(text)
            messages.append(_parent_notice(WarningCode.PARENT_DUPLICATE_REFERENCE,
                            "duplicate parent target retained as one reference", child, location, promoted))
            continue
        grouped[token] = (parsed, [text], resolved, temporal)
        if bare and resolved:
            messages.append(_parent_notice(WarningCode.PARENT_BARE_COMPATIBILITY,
                            "bare parent uniquely resolved through compatibility mode", child, location, promoted))
        if not resolved:
            messages.append(_parent_notice(WarningCode.PARENT_UNRESOLVED,
                            "declared parent has no loaded match", child, location, promoted))
        if temporal == "unavailable" and parsed is not None:
            messages.append(_parent_notice(WarningCode.VERSION_ORDER_MISSING,
                            "cross-version parent chronology cannot be validated", child, location, promoted))
    references = tuple(ParentReference(tuple(texts), str(key) if key is not None else None,
                       key, ParentResolutionStatus.RESOLVED if resolved else ParentResolutionStatus.UNRESOLVED,
                       temporal) for token, (key, texts, resolved, temporal) in sorted(grouped.items()))
    state = "null" if values is None else ("empty" if not values else "declared")
    return ParentValidationResult(child, state, references, graph_deferred, tuple(messages))


def resolve_parent_references(
    child_key: RecordKey, parent_ids: object, loaded_keys: tuple[RecordKey, ...], *,
    version_order: VersionOrderResult | None = None, location: RowLocation = RowLocation(),
    csv_encoded: bool = False, max_parent_list_length: int | None = None,
    strict_mode: bool = False, strict_warning_codes: tuple[str, ...] = (),
) -> ParentValidationResult:
    """Resolve immediate input references only; same-version graph checks stay deferred."""
    keys = _parent_keys(loaded_keys)
    loc = _join_location(location)
    if type(child_key) is not RecordKey or child_key not in keys:
        raise _fail(ErrorCode.SCHEMA_TYPE, "child must have a loaded canonical identity", "record_id", loc)
    promoted = _join_options(None, strict_mode, strict_warning_codes)
    order = _checked_order(version_order, tuple(sorted({key.dataset_version for key in keys})))
    try:
        parents = parse_parent_ids(parent_ids, csv_encoded=csv_encoded,
                                    max_parent_list_length=max_parent_list_length)
    except CanonicalValidationError as exc:
        raise _fail(exc.code, exc.safe_message, "parent_ids", loc, child_key) from None
    return _resolve_parent_list(child_key, parents, _parent_lookup(keys, order), loc, promoted)


def validate_generation_declarations(
    loaded_keys: tuple[RecordKey, ...], provenance: tuple[CanonicalRow | ProvenanceAssessment, ...], *,
    version_order: VersionOrderResult | None = None, strict_mode: bool = False,
    strict_warning_codes: tuple[str, ...] = (),
) -> GenerationValidationResult:
    """Validate non-grounding counts using only safely established dependencies.

    This internal input check does not construct or traverse an ancestry graph.
    Monotone bounded scans propagate established expected counts; declarations
    never seed expected values. Stalled dependencies remain unavailable, without
    inferring a cycle. Grounding yes establishes zero directly, independently of
    lineage depth. Parent validity and incomplete-provenance errors stay visible.
    """
    keys = _parent_keys(loaded_keys)
    promoted = _join_options(None, strict_mode, strict_warning_codes)
    order = _checked_order(version_order, tuple(sorted({key.dataset_version for key in keys})))
    if type(provenance) is not tuple:
        raise CanonicalValidationError(ErrorCode.SCHEMA_TYPE, "generation checks require explicit provenance rows")
    rows: dict[RecordKey, ProvenanceAssessment] = {}
    parents: dict[RecordKey, ParentValidationResult] = {}
    messages = [ValidationMessage(message.code,
                ValidationSeverity.ERROR if message.code in promoted else message.severity,
                message.message, message.file_role, message.file_path, message.field,
                message.record_key, message.row_number) for message in order.messages]
    for row in provenance:
        if type(row) not in (CanonicalRow, ProvenanceAssessment):
            raise CanonicalValidationError(ErrorCode.SCHEMA_TYPE, "generation checks require canonical or assessed provenance")
        assessed = assess_provenance_row(row)
        key = assessed.record_key
        if key in rows:
            raise _fail(ErrorCode.PROVENANCE_DUPLICATE_ROW, "duplicate generation input identity", "record_id", assessed.location, key)
        if key not in keys:
            raise _fail(ErrorCode.PROVENANCE_UNMATCHED_ROW, "generation input has no matching loaded record", "record_id", assessed.location, key)
        rows[key] = assessed
    lookup = _parent_lookup(keys, order)
    for key in sorted(rows):
        row = rows[key]
        parsed = parse_parent_ids(row.values.get("parent_ids"))
        parent_result = _resolve_parent_list(key, parsed, lookup, row.location, promoted)
        if "parent_ids" not in row.values:
            parent_result = ParentValidationResult(key, "absent", parent_result.references,
                            parent_result.graph_validation_deferred, parent_result.messages)
        parents[key] = parent_result
        messages.extend(parent_result.messages)
        for field_name in row.missing_required_fields:
            messages.append(_join_message(ErrorCode.SCHEMA_REQUIRED_FIELD.value, ValidationSeverity.ERROR,
                            "generation input lacks a required provenance field", key, row.location, field_name))
    expected: dict[RecordKey, int] = {}
    reasons: dict[RecordKey, tuple[str, ...]] = {}
    for key in keys:
        row = rows.get(key)
        if row is None:
            reasons[key] = ("PROVENANCE_MISSING",)
            messages.append(_join_message(WarningCode.PROVENANCE_MISSING_ROW.value,
                            ValidationSeverity.ERROR if WarningCode.PROVENANCE_MISSING_ROW.value in promoted else ValidationSeverity.WARNING,
                            "record has no provenance for generation validation", key, RowLocation()))
        elif not row.required_fields_valid:
            reasons[key] = ("REQUIRED_PROVENANCE_FIELDS_INVALID",)
        elif row.values["external_grounding"] == "yes":
            expected[key] = 0
        elif row.values["external_grounding"] == "unknown":
            reasons[key] = ("GROUNDING_UNKNOWN",)
        elif parents[key].declaration_state in ("null", "absent"):
            reasons[key] = ("PARENT_DECLARATION_UNAVAILABLE",)
        elif not parents[key].references:
            reasons[key] = ("NO_GROUNDED_DEPENDENCY",)
        elif any(ref.resolution_status is not ParentResolutionStatus.RESOLVED for ref in parents[key].references):
            reasons[key] = ("PARENT_UNRESOLVED",)
        elif any(ref.temporal_status == "unavailable" for ref in parents[key].references):
            reasons[key] = ("PARENT_CHRONOLOGY_UNAVAILABLE",)
    # At most one new count per record. No queue of graph nodes or topological sort.
    pending = set(keys) - set(expected) - set(reasons)
    # An existing declared version order can schedule scans, without deriving a
    # topological order from parent edges. Same-version dependencies may need
    # repeated scans. No stalled dependency is ever relabelled as a cycle.
    positions = lookup[2]
    scan_order = tuple(item[3] for item in sorted(
        (positions.get(key.dataset_version, 0), key.dataset_version, key.record_id, key)
        for key in pending))
    for _ in range(len(pending)):
        newly_established: set[RecordKey] = set()
        for key in scan_order:
            if key not in pending:
                continue
            dependencies = parents[key].references
            if all(ref.parent_key in expected for ref in dependencies):
                expected[key] = 1 + max(expected[ref.parent_key] for ref in dependencies)
                newly_established.add(key)
        if not newly_established:
            break
        pending.difference_update(newly_established)
    for key in pending:
        reasons[key] = ("PARENT_GENERATION_UNAVAILABLE",)
    assessments: list[GenerationAssessment] = []
    for key in keys:
        row = rows.get(key)
        declared = None if row is None else row.values.get("generation")
        value = expected.get(key)
        mismatch = value is not None and declared is not None and declared != value
        if mismatch:
            code = WarningCode.GENERATION_MISMATCH.value
            messages.append(_join_message(code,
                            ValidationSeverity.ERROR if code in promoted else ValidationSeverity.WARNING,
                            "declared generation disagrees with the validated expected value", key,
                            row.location, "generation"))
        assessments.append(GenerationAssessment(key, declared, value, reasons.get(key, ()), mismatch))
    return GenerationValidationResult(tuple(assessments), tuple(parents[key] for key in sorted(parents)),
                                      tuple(messages), promoted)
