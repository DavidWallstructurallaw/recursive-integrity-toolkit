"""Define Phase 2 core contracts for validated input metadata.

Owner IDs:
    PR-001, PR-002, PR-004, PR-007, PR-008, PR-009, PR-010, PR-011, PR-016, PR-017

Inputs:
    Explicit identifiers, file metadata, validation metadata, and capability declarations.

Outputs:
    Immutable project-owned contracts shared by Phase 2 ingestion and validation layers.

Assumptions:
    Canonical identity is the ordered pair ``(dataset_version, record_id)``.
    Unknown values remain explicit and are never promoted to stronger evidence.

Limits:
    No file ingestion, mapping, metric, lineage traversal, report assembly, or simulation is
    implemented here. These types carry validated metadata only.

Current phase status:
    Phase 2 Step 4 core and canonical-row contracts. Import-safe. No analytical behavior.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Mapping


RESERVED_RECORD_KEY_SEPARATOR = "::"
MAX_DATASET_VERSION_CODEPOINTS = 256
MAX_RECORD_ID_CODEPOINTS = 512


class FileRole(StrEnum):
    """Approved audit-bundle file roles."""

    RECORDS_PRIMARY = "records_primary"
    RECORDS_COMPARE = "records_compare"
    PROVENANCE_MANIFEST = "provenance_manifest"
    SCHEMA_MAPPING = "schema_mapping"
    CONFIG = "config"
    VERSION_ORDER = "version_order"
    EMBEDDING_DATA = "embedding_data"
    EXTERNAL_REFERENCE = "external_reference"


class FileFormat(StrEnum):
    """File formats that Phase 2 may recognize structurally."""

    CSV = "csv"
    JSONL = "jsonl"
    PARQUET = "parquet"
    JSON = "json"
    TOML = "toml"
    NPY = "npy"


class ValidationSeverity(StrEnum):
    """Canonical validation severity registry."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    FATAL = "fatal"


class CapabilityStatus(StrEnum):
    """Canonical capability status registry."""

    AVAILABLE = "available"
    PARTIAL = "partial"
    UNAVAILABLE = "unavailable"
    EXPERIMENTAL = "experimental"


class CapabilityKey(StrEnum):
    """Required initial capability keys."""

    INGESTION = "ingestion"
    CONTENT_DIAGNOSTICS = "content_diagnostics"
    PROVENANCE = "provenance"
    LINEAGE = "lineage"
    DATASET_LONGITUDINAL = "dataset_longitudinal"
    MODEL_LONGITUDINAL = "model_longitudinal"
    INTERVENTION_SIMULATION = "intervention_simulation"


class PrivacyMode(StrEnum):
    """Approved local output privacy modes."""

    STANDARD = "standard"
    REDACTED = "redacted"
    DEBUG = "debug"


class ParentResolutionStatus(StrEnum):
    """Input-validation status for an individual declared parent reference."""

    RESOLVED = "resolved"
    UNRESOLVED = "unresolved"
    AMBIGUOUS = "ambiguous"
    INVALID = "invalid"


@dataclass(frozen=True, slots=True, order=True)
class RecordKey:
    """Canonical record identity with stable transport serialization."""

    dataset_version: str
    record_id: str

    def __post_init__(self) -> None:
        _validate_identifier(
            "dataset_version",
            self.dataset_version,
            MAX_DATASET_VERSION_CODEPOINTS,
        )
        _validate_identifier("record_id", self.record_id, MAX_RECORD_ID_CODEPOINTS)

    def __str__(self) -> str:
        return f"{self.dataset_version}{RESERVED_RECORD_KEY_SEPARATOR}{self.record_id}"

    @classmethod
    def parse(cls, value: str) -> "RecordKey":
        """Parse the approved ``dataset_version::record_id`` transport form."""
        if not isinstance(value, str):
            raise TypeError("record_key serialization must be a string")
        if value.count(RESERVED_RECORD_KEY_SEPARATOR) != 1:
            raise ValueError("record_key must contain exactly one reserved separator")
        dataset_version, record_id = value.split(RESERVED_RECORD_KEY_SEPARATOR, 1)
        return cls(dataset_version=dataset_version, record_id=record_id)


def _validate_identifier(name: str, value: str, maximum_codepoints: int) -> None:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    if not value:
        raise ValueError(f"{name} must be nonempty")
    if value != value.strip():
        raise ValueError(f"{name} must not have leading or trailing whitespace")
    if len(value) > maximum_codepoints:
        raise ValueError(f"{name} exceeds the approved length limit")
    if RESERVED_RECORD_KEY_SEPARATOR in value:
        raise ValueError(f"{name} contains the reserved record-key separator")
    if "\x00" in value:
        raise ValueError(f"{name} must not contain NUL")


@dataclass(frozen=True, slots=True)
class InputSource:
    """One declared local input source before ingestion."""

    role: FileRole
    path: Path
    declared_format: FileFormat | None = None


@dataclass(frozen=True, slots=True)
class AuditBundle:
    """Collection of input declarations supplied to one toolkit run."""

    sources: tuple[InputSource, ...] = ()


@dataclass(frozen=True, slots=True)
class FileInventoryEntry:
    """Structural metadata produced by a future Phase 2 loader."""

    role: FileRole
    path: Path
    file_format: FileFormat
    size_bytes: int
    sha256: str
    row_count: int | None = None
    fields: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class ValidationMessage:
    """Content-safe structured validation message."""

    code: str
    severity: ValidationSeverity
    message: str
    file_role: FileRole | None = None
    file_path: str | None = None
    field: str | None = None
    record_key: RecordKey | None = None
    row_number: int | None = None


@dataclass(frozen=True, slots=True)
class ValidationCoverage:
    """Named validation coverage counts without analytical interpretation."""

    numerator: int
    denominator: int
    denominator_name: str

    def __post_init__(self) -> None:
        if self.numerator < 0 or self.denominator < 0:
            raise ValueError("coverage counts must be nonnegative")
        if self.numerator > self.denominator:
            raise ValueError("coverage numerator cannot exceed denominator")
        if not self.denominator_name:
            raise ValueError("coverage denominator must be named")


@dataclass(frozen=True, slots=True)
class Capability:
    """One independently evaluated analysis-family status."""

    status: CapabilityStatus
    coverage: ValidationCoverage | None = None
    requirements_met: tuple[str, ...] = ()
    requirements_missing: tuple[str, ...] = ()
    reason_codes: tuple[str, ...] = ()
    notes: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class ObservabilityAssessment:
    """Contract for a future maximum level and complete capability matrix."""

    maximum_level: int
    capabilities: Mapping[CapabilityKey, Capability] = field(default_factory=dict)
    basis: tuple[str, ...] = ()
    limitations: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if isinstance(self.maximum_level, bool) or not isinstance(self.maximum_level, int):
            raise TypeError("maximum observability level must be an integer")
        if not 0 <= self.maximum_level <= 5:
            raise ValueError("maximum observability level must be between 0 and 5")
        supplied = set(self.capabilities)
        expected = set(CapabilityKey)
        if supplied != expected:
            missing = sorted(key.value for key in expected - supplied)
            extra = sorted(str(key) for key in supplied - expected)
            raise ValueError(f"capability matrix keys mismatch; missing={missing}, extra={extra}")


@dataclass(frozen=True, slots=True)
class RawRow:
    """Unmapped row with physical location; payload is excluded from repr.

    CSV strings and their original serialized spelling are retained so later
    normalization can distinguish a quoted empty string from an empty field.
    JSONL keeps native values, absent keys, and explicit nulls distinct.
    Parquet rows have an ordinal but no text line or serialized spelling.
    """

    values: Mapping[str, object] = field(repr=False)
    row_number: int
    line_number: int | None = None
    serialized_text: str | None = field(default=None, repr=False)


@dataclass(frozen=True, slots=True)
class LoadedTable:
    """Parsed physical table and inventory; canonical validation is deferred."""

    inventory: FileInventoryEntry
    rows: tuple[RawRow, ...] = field(repr=False)


class SourceType(StrEnum):
    """Declared source categories from DATA_AND_PROVENANCE_SPEC section 9.3."""

    HUMAN = "human"
    SYNTHETIC = "synthetic"
    MIXED = "mixed"
    SENSOR = "sensor"
    UNKNOWN = "unknown"


class ProvenanceConfidence(StrEnum):
    """Declared confidence categories, without conversion to probabilities."""

    CONFIRMED = "confirmed"
    LOG_DERIVED = "log_derived"
    ESTIMATED = "estimated"
    UNKNOWN = "unknown"


class ExternalGrounding(StrEnum):
    """Declared grounding values, independent of source type and human review."""

    YES = "yes"
    NO = "no"
    UNKNOWN = "unknown"


class Transformation(StrEnum):
    """Approved transformation names; no operation is executed by this enum."""

    GENERATE = "generate"
    REWRITE = "rewrite"
    SUMMARIZE = "summarize"
    TRANSLATE = "translate"
    FILTER = "filter"
    LABEL = "label"
    CARRYOVER = "carryover"
    OTHER = "other"


class ContentMode(StrEnum):
    """Source-wide content interpretation; local_ref resolution remains Step 7."""

    INLINE = "inline"
    LOCAL_REF = "local_ref"


@dataclass(frozen=True, slots=True)
class NormalizationOptions:
    """Explicit serialization policies; no new run-config fields are introduced."""

    content_mode: ContentMode = ContentMode.INLINE
    null_tokens: tuple[str, ...] = ("null", "NULL")
    csv_boolean_compatibility: bool = False
    blank_as_null: bool = False
    preserve_extras: bool = False


@dataclass(frozen=True, slots=True)
class RowLocation:
    """Physical input location. Private paths do not appear in default repr."""

    file_role: FileRole | None = None
    file_path: str | None = field(default=None, repr=False)
    row_number: int | None = None
    line_number: int | None = None


@dataclass(frozen=True, slots=True)
class CanonicalRow:
    """Step 4 row-valid fields only; no join, parent, or capability certification.

    values, field_states and extras are detached read-only mappings returned by
    normalization. Parent arrays use immutable tuples internally. Field states
    preserve absence, explicit null, and CSV blank/token distinctions separately.
    """

    kind: str
    record_key: RecordKey
    values: Mapping[str, object] = field(repr=False)
    field_states: Mapping[str, str] = field(repr=False)
    extras: Mapping[str, object] = field(repr=False)
    ignored_fields: tuple[str, ...] = ()
    defaulted_fields: tuple[str, ...] = ()
    location: RowLocation = RowLocation()
