"""Define the pure record-to-state representation boundary.

Owner IDs:
    T1 input basis, PR-011; PR-001 and PR-016 supporting scope and ordering.

Inputs:
    Explicit canonical records, selected versions and field configuration.

Outputs:
    Immutable representation selection, assignments, exclusions and named coverage.

Assumptions:
    Canonical values have already undergone explicit mapping and normalization.
    Declared field labels do not certify semantics, truth or source independence.

Limits:
    No file access, hashing, frequency, support, diversity, tail, sampling, graph,
    report, callback dispatch or plugin registration. Protocol is typing only.
    Consumers must revalidate inputs; a caller-created result is not certification.

Current phase status:
    Phase 3 Step 2 representation protocol and scope validation only.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Protocol

from ..config import RepresentationConfig
from ..errors import CanonicalValidationError, ErrorCode
from ..io.validation import validate_canonical_values
from ..models import (
    CalculationReason, CalculationScope, CalculationStatus, CanonicalRow,
    FileRole, RecordKey, RecordStateAssignment, RepresentationDescriptor,
    RowLocation, ValidationCoverage, ValidationMessage,
)


@dataclass(frozen=True, slots=True)
class RepresentationSelection:
    """Selected declaration and its audit basis; no empirical semantic claim."""

    descriptor: RepresentationDescriptor
    selection_basis: str
    considered_fields: tuple[str, ...]
    messages: tuple[ValidationMessage, ...] = ()


@dataclass(frozen=True, slots=True)
class RepresentationResult:
    """In-memory assignments only; field absence and explicit null remain visible."""

    selection: RepresentationSelection
    scope: CalculationScope
    assignments: tuple[RecordStateAssignment, ...] = field(repr=False)
    field_states: tuple[tuple[RecordKey, str], ...] = field(repr=False)
    coverage: ValidationCoverage
    status: CalculationStatus
    reason_codes: tuple[CalculationReason, ...] = ()
    limitations: tuple[str, ...] = (
        "Literal declared field labels do not certify semantic validity.",
        "Coverage uses selected valid records; provenance scope is unchanged.",
        "No frequencies or analytical metrics have been calculated.",
    )

    @property
    def selected_count(self) -> int:
        return len(self.assignments)

    @property
    def included_count(self) -> int:
        return len(self.scope.included_record_keys)

    @property
    def excluded_count(self) -> int:
        return len(self.scope.excluded_record_keys)


class RepresentationProtocol(Protocol):
    """Static callable shape only. No runtime accepts or invokes a user callback."""

    def __call__(
        self, records: tuple[CanonicalRow, ...], *, dataset_versions: tuple[str, ...],
        scope_id: str, config: RepresentationConfig | None = None,
        allow_fallback: bool = False, fallback_version: str | None = None,
        fallback_missing_policy: str | None = None, missing_state_id: str | None = None,
    ) -> RepresentationResult:
        ...


def _representation_error(
    code: ErrorCode, message: str, *, field_name: str | None = None,
    key: RecordKey | None = None, location: RowLocation = RowLocation(),
) -> CanonicalValidationError:
    return CanonicalValidationError(
        code, message, field=field_name,
        file_role=location.file_role.value if location.file_role is not None else None,
        file_path="[redacted]" if location.file_path is not None else None,
        row_number=location.row_number, line_number=location.line_number,
        record_key=str(key) if key is not None else None,
    )


def _literal_text(value: object) -> bool:
    """Validate literal declarations without normalization or object hooks."""
    if type(value) is not str or not value or "\x00" in value:
        return False
    try:
        value.encode("utf-8")
    except UnicodeEncodeError:
        return False
    return True


def _selected_records(
    records: tuple[CanonicalRow, ...], dataset_versions: tuple[str, ...],
) -> tuple[tuple[RecordKey, dict[str, object], RowLocation], ...]:
    """Validate and snapshot canonical rows; selection never pools implicitly."""
    if type(records) is not tuple or type(dataset_versions) is not tuple or not dataset_versions:
        raise _representation_error(ErrorCode.CONFIG_INVALID, "records and selected versions require explicit tuples")
    for version in dataset_versions:
        if (not _literal_text(version) or version != version.strip()
                or len(version) > 256 or "::" in version):
            raise _representation_error(ErrorCode.CONFIG_INVALID, "invalid selected version identity")
    if len(set(dataset_versions)) != len(dataset_versions):
        raise _representation_error(ErrorCode.CONFIG_INVALID, "selected versions must be unique")
    seen: set[RecordKey] = set()
    loaded: set[str] = set()
    selected = []
    for row in records:
        if type(row) is not CanonicalRow or type(row.kind) is not str or row.kind != "records":
            raise _representation_error(ErrorCode.SCHEMA_TYPE, "representation requires canonical record rows")
        if type(row.record_key) is not RecordKey or type(row.location) is not RowLocation:
            raise _representation_error(ErrorCode.SCHEMA_TYPE, "canonical identity and location types are required")
        location = row.location
        if (location.file_role is not None and type(location.file_role) is not FileRole
                or location.file_path is not None and type(location.file_path) is not str):
            raise _representation_error(ErrorCode.SCHEMA_TYPE, "invalid row location")
        for number in (location.row_number, location.line_number):
            if number is not None and (type(number) is not int or number < 1):
                raise _representation_error(ErrorCode.SCHEMA_TYPE, "invalid row coordinates")
        if type(row.values) not in (dict, MappingProxyType) or any(type(name) is not str for name in row.values):
            raise _representation_error(ErrorCode.SCHEMA_TYPE, "canonical fields must be plain literal-key mappings")
        values = dict(row.values)
        safe_location = RowLocation(location.file_role, "[redacted]" if location.file_path is not None else None,
                                    location.row_number, location.line_number)
        key = validate_canonical_values(values, kind="records", location=safe_location)
        if (type(row.record_key.dataset_version) is not str or type(row.record_key.record_id) is not str
                or key != row.record_key):
            raise _representation_error(ErrorCode.SCHEMA_TYPE, "record identity disagrees with its fields")
        if key in seen:
            raise _representation_error(ErrorCode.RECORD_DUPLICATE_ID, "duplicate composite record identity",
                                        field_name="record_id", key=key, location=location)
        seen.add(key)
        loaded.add(key.dataset_version)
        if key.dataset_version in dataset_versions:
            selected.append((key, values, safe_location))
    if records and set(dataset_versions) - loaded:
        raise _representation_error(ErrorCode.CONFIG_INVALID, "selected version is not present in the loaded scope")
    return tuple(sorted(selected, key=_selected_key))


def _selected_key(row: tuple[RecordKey, dict[str, object], RowLocation]) -> RecordKey:
    return row[0]
