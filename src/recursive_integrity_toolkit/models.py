"""Define input metadata and Phase 3 Step 2 supporting contracts.

Owner IDs:
    PR-001, PR-002, PR-004, PR-007, PR-008, PR-009, PR-010, PR-011, PR-016, PR-017
    T1, T2, T3 direct branch, PR-005, PR-006: supporting contracts only.

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
    Phase 3 Step 2 contracts; Phase 2 behavior preserved. Import-safe. No metrics.
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
    LINEAGE_CONTEXT = "lineage_context"
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
    line_number: int | None = None


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


    @property
    def ratio(self) -> float | None:
        """Validation coverage only; zero denominator has no defined ratio."""
        return self.numerator / self.denominator if self.denominator else None


@dataclass(frozen=True, slots=True)
class Capability:
    """One independently evaluated analysis-family status."""

    status: CapabilityStatus
    coverage: ValidationCoverage | None = None
    requirements_met: tuple[str, ...] = ()
    requirements_missing: tuple[str, ...] = ()
    reason_codes: tuple[str, ...] = ()
    notes: tuple[str, ...] = ()
    coverage_details: Mapping[str, ValidationCoverage] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class ObservabilityAssessment:
    """Contract for a future maximum level and complete capability matrix."""

    maximum_level: int
    capabilities: Mapping[CapabilityKey, Capability] = field(default_factory=dict)
    basis: tuple[str, ...] = ()
    limitations: tuple[str, ...] = ()
    validation_messages: tuple[ValidationMessage, ...] = ()

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


@dataclass(frozen=True, slots=True)
class ProvenanceAssessment:
    """Typed row evidence, which may have missing required provenance fields.

    This is not a CanonicalRow. Missing fields retain their absence or null and
    remain errors; they are never synthesized as an explicit unknown value.
    join_provenance revalidates the stored fields and does not trust these flags.
    """

    record_key: RecordKey
    values: Mapping[str, object] = field(repr=False)
    location: RowLocation = RowLocation()
    missing_required_fields: tuple[str, ...] = ()
    required_fields_valid: bool = False
    grounding_known: bool = False


@dataclass(frozen=True, slots=True)
class ProvenanceMatch:
    """One selected record and its optional unique provenance row.

    Shared metadata stays in separate namespaces. conflicting_fields identifies
    discrepancies without choosing or overwriting either declaration. Raw record
    content is deliberately not retained in the join result.
    """

    record_key: RecordKey
    provenance: ProvenanceAssessment | None = field(repr=False)
    record_location: RowLocation = RowLocation()
    record_metadata: Mapping[str, object] = field(default_factory=dict, repr=False)
    conflicting_fields: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class ProvenanceJoinResult:
    """Step 5 internal validation basis; no metric/report/capability output.

    All coverage denominators are the same explicit selected valid-record scope.
    Missing-field diagnostics remain errors even when coverage can be measured.
    The original records are not discarded and this object writes no report.
    """

    selected_dataset_versions: tuple[str, ...]
    scope_record_keys: tuple[RecordKey, ...]
    provenance_supplied: bool
    matches: tuple[ProvenanceMatch, ...] = field(repr=False)
    missing_record_keys: tuple[RecordKey, ...]
    provenance_row_coverage: ValidationCoverage
    provenance_required_field_coverage: ValidationCoverage
    grounding_field_coverage: ValidationCoverage
    messages: tuple[ValidationMessage, ...]
    promoted_warning_codes: tuple[str, ...] = ()

    @property
    def has_errors(self) -> bool:
        """Expose retained errors; partial coverage never suppresses a failure."""
        return any(m.severity in (ValidationSeverity.ERROR, ValidationSeverity.FATAL)
                   for m in self.messages)


@dataclass(frozen=True, slots=True)
class VersionOrderResult:
    """PR-007 chronology evidence only; no longitudinal result or filename inference.

    declarations and invocation_order retain the input basis for revalidation.
    order may include explicitly declared unloaded versions. loaded_versions is
    a lexical inventory, never an inferred chronological ordering.
    """

    loaded_versions: tuple[str, ...]
    order: tuple[str, ...]
    order_source: str
    source_orders: Mapping[str, tuple[str, ...]] = field(repr=False)
    declarations: Mapping[str, object] = field(repr=False)
    invocation_order: tuple[str, ...] | None = None
    messages: tuple[ValidationMessage, ...] = ()


@dataclass(frozen=True, slots=True)
class ParentReference:
    """PR-008 one unique reference target, with original spellings retained.

    An unresolved composite can have a parsed key without a loaded parent.
    An unresolved bare reference has no canonical key or canonical spelling.
    Neither supplies external-root evidence.
    """

    source_references: tuple[str, ...] = field(repr=False)
    canonical_reference: str | None
    parent_key: RecordKey | None
    resolution_status: ParentResolutionStatus
    temporal_status: str


@dataclass(frozen=True, slots=True)
class ParentValidationResult:
    """PR-008 immediate-reference validation, never an ancestry graph.

    graph_validation_deferred remains true for same-version references. A
    successful reference lookup never certifies whole-lineage completeness.
    """

    child_key: RecordKey
    declaration_state: str
    references: tuple[ParentReference, ...] = field(repr=False)
    graph_validation_deferred: bool
    messages: tuple[ValidationMessage, ...] = ()


@dataclass(frozen=True, slots=True)
class ParentRecordValidation:
    """Retained immediate evidence for one loaded record, including failures.

    Missing and null declarations have zero declared references, while an
    unparseable container has unknown cardinality. Identity resolution counts
    remain distinct from chronological eligibility for ancestry edges.
    """

    child_key: RecordKey
    provenance_available: bool
    result: ParentValidationResult | None = field(repr=False)
    declared_reference_count: int | None
    resolved_reference_count: int
    invalid_self_reference_count: int
    messages: tuple[ValidationMessage, ...] = ()

    def __post_init__(self) -> None:
        if type(self.child_key) is not RecordKey or type(self.provenance_available) is not bool:
            raise TypeError("parent evidence requires a canonical key and explicit provenance flag")
        if self.result is not None and (type(self.result) is not ParentValidationResult
                                       or self.result.child_key != self.child_key):
            raise ValueError("parent result must belong to its loaded record")
        if self.result is not None:
            if (self.result.declaration_state not in ("absent", "null", "empty", "declared")
                    or type(self.result.graph_validation_deferred) is not bool):
                raise ValueError("parent evidence requires an explicit declaration state")
            if type(self.result.references) is not tuple:
                raise TypeError("parent references require an immutable tuple")
            for reference in self.result.references:
                if (type(reference) is not ParentReference
                        or type(reference.source_references) is not tuple
                        or any(type(text) is not str for text in reference.source_references)):
                    raise TypeError("parent source references require immutable literal spellings")
            if type(self.result.messages) is not tuple or any(type(item) is not ValidationMessage
                                                            for item in self.result.messages):
                raise TypeError("parent result messages require an immutable tuple")
        counts = (self.resolved_reference_count, self.invalid_self_reference_count)
        if self.declared_reference_count is not None:
            counts += (self.declared_reference_count,)
        for value in counts:
            if type(value) is not int or value < 0:
                raise ValueError("parent reference counts require nonnegative integers")
        if self.declared_reference_count is not None and (
                self.resolved_reference_count + self.invalid_self_reference_count
                > self.declared_reference_count):
            raise ValueError("parent evidence counts exceed the declaration count")
        if type(self.messages) is not tuple or any(type(item) is not ValidationMessage for item in self.messages):
            raise TypeError("parent messages require an immutable tuple")


@dataclass(frozen=True, slots=True)
class ParentBatchValidationResult:
    """Input-only immediate evidence retained for every loaded canonical key."""

    record_keys: tuple[RecordKey, ...]
    assessments: tuple[ParentRecordValidation, ...] = field(repr=False)
    version_order: VersionOrderResult
    messages: tuple[ValidationMessage, ...]
    promoted_warning_codes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if type(self.record_keys) is not tuple or any(type(key) is not RecordKey for key in self.record_keys):
            raise TypeError("parent batch keys require an immutable canonical tuple")
        if tuple(sorted(set(self.record_keys))) != self.record_keys:
            raise ValueError("parent batch keys must be unique and sorted")
        if type(self.assessments) is not tuple or any(type(item) is not ParentRecordValidation
                                                   for item in self.assessments):
            raise TypeError("parent batch assessments require an immutable tuple")
        if tuple(item.child_key for item in self.assessments) != self.record_keys:
            raise ValueError("parent batch assessments must cover every loaded key exactly once")
        if type(self.version_order) is not VersionOrderResult:
            raise TypeError("parent batch chronology requires typed evidence")
        if type(self.messages) is not tuple or any(type(item) is not ValidationMessage for item in self.messages):
            raise TypeError("parent batch messages require an immutable tuple")
        if type(self.promoted_warning_codes) is not tuple or any(type(code) is not str
                                                               for code in self.promoted_warning_codes):
            raise TypeError("parent warning policy requires an immutable tuple")


@dataclass(frozen=True, slots=True)
class GenerationAssessment:
    """PR-009 declaration versus safely established non-grounding step count."""

    record_key: RecordKey
    declared_generation: int | None
    expected_generation: int | None
    reason_codes: tuple[str, ...]
    mismatch: bool


@dataclass(frozen=True, slots=True)
class GenerationValidationResult:
    """PR-009 validation basis. No depth, roots, ancestors, metrics or report.

    Dependency failure retains an unavailable reason; it never diagnoses a
    general cycle. Input warnings and errors remain visible in messages.
    """

    assessments: tuple[GenerationAssessment, ...]
    parents: tuple[ParentValidationResult, ...] = field(repr=False)
    messages: tuple[ValidationMessage, ...]
    promoted_warning_codes: tuple[str, ...] = ()

    @property
    def has_errors(self) -> bool:
        """Expose retained failures without changing the declarations."""
        return any(message.severity in (ValidationSeverity.ERROR, ValidationSeverity.FATAL)
                   for message in self.messages)


@dataclass(frozen=True, slots=True)
class ScenarioParameters:
    """PR-010/PR-011 explicit internal scenario inputs, never simulated results.

    Canonical parameter names come from DEFINITIONS_AND_UNITS sections 12-13.
    Distributions contain explicit (state, mass) pairs and are never estimated,
    mixed or renormalized. This does not extend the run-config JSON schema or
    enable a simulator. Activation and recorded seed still use ScenarioConfig.
    """

    model_name: str
    resample_size: int | None = None
    simulation_horizon: int | None = None
    simulation_replicates: int | None = None
    state_distribution: tuple[tuple[str, float], ...] | None = field(default=None, repr=False)
    external_input_distribution: tuple[tuple[str, float], ...] | None = field(default=None, repr=False)
    reopening_weight: float | None = None


@dataclass(frozen=True, slots=True)
class RowMappingEvidence:
    """Ordered row-transform metadata without source values or expression execution."""

    record_key: RecordKey
    location: RowLocation
    mapping_sha256: str
    source_fields: tuple[str, ...]
    unmapped_fields: tuple[str, ...]
    fields: tuple[tuple[str, str, tuple[str, ...], tuple[str, ...]], ...]


@dataclass(frozen=True, slots=True)
class BundleValidationResult:
    """Internal Phase 2 handoff, never a final report or a metric result.

    Input data is hidden from repr and retained only for the explicit caller.
    Family failures remain visible; generation can be unavailable after an
    invalid parent declaration while independent dataset eligibility survives.
    A nonzero maximum level does not clear has_errors.
    """

    inventory: tuple[FileInventoryEntry, ...] = field(repr=False)
    records: tuple[CanonicalRow, ...] = field(repr=False)
    provenance: tuple[CanonicalRow | ProvenanceAssessment, ...] | None = field(repr=False)
    provenance_join: ProvenanceJoinResult = field(repr=False)
    version_order: VersionOrderResult
    generation: GenerationValidationResult | None = field(repr=False)
    observability: ObservabilityAssessment
    mapping_traces: tuple[RowMappingEvidence, ...] = field(repr=False)
    content_read_keys: tuple[RecordKey, ...]
    validation_messages: tuple[ValidationMessage, ...]
    parent_validation: ParentBatchValidationResult | None = field(default=None, repr=False)

    @property
    def has_errors(self) -> bool:
        return any(message.severity in (ValidationSeverity.ERROR, ValidationSeverity.FATAL)
                   for message in self.validation_messages)


# Phase 3 Step 1: supporting contracts only. Constructors check declarations;
# they do not assign states, compute metrics, certify evidence, or run scenarios.
# Owners: T1, T2, T3 direct branch, PR-004/005/006/007/011/016 supporting basis.

class CalculationEvidenceClass(StrEnum):
    OBSERVED_FACT = "observed_fact"
    DERIVED_METRIC = "derived_metric"
    SIMULATION = "simulation"


class CalculationStatus(StrEnum):
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"


class CalculationReason(StrEnum):
    EMPTY_SCOPE = "R_CALC_EMPTY_SCOPE"
    ALL_EXCLUDED = "R_CALC_ALL_EXCLUDED"
    REPRESENTATION_MISSING = "R_CALC_REPRESENTATION_MISSING"
    REPRESENTATION_INCOMPATIBLE = "R_CALC_REPRESENTATION_INCOMPATIBLE"
    ORDER_MISSING = "R_CALC_ORDER_MISSING"
    PROVENANCE_FIELD_UNAVAILABLE = "R_CALC_PROVENANCE_FIELD_UNAVAILABLE"
    WEIGHT_BASIS_INVALID = "R_CALC_WEIGHT_BASIS_INVALID"
    NUMERICAL_INPUT_INVALID = "R_CALC_NUMERICAL_INPUT_INVALID"
    UNSUPPORTED_OPTION = "R_CALC_UNSUPPORTED_OPTION"
    CONTENT_UNAVAILABLE = "R_CALC_CONTENT_UNAVAILABLE"


def _calculation_text(value: object) -> None:
    if type(value) is not str or not value or "\x00" in value:
        raise ValueError("calculation metadata requires nonempty literal text")


def _calculation_strings(value: object) -> None:
    if type(value) is not tuple:
        raise TypeError("calculation declarations require immutable tuples")
    for item in value:
        _calculation_text(item)


def _calculation_integer(value: object, *, positive: bool = False) -> None:
    if type(value) is not int or value < 0 or (positive and value == 0):
        raise ValueError("calculation parameter requires an explicit integer in range")


def _calculation_number(value: object) -> None:
    # Range/type validation only. No metric arithmetic or probability repair.
    import math
    if type(value) not in (int, float):
        raise TypeError("calculation scalar must be a built-in number")
    try:
        valid = math.isfinite(value)
    except OverflowError:
        valid = False
    if not valid:
        raise ValueError("calculation scalar must be finite")


@dataclass(frozen=True, slots=True)
class NumericalPolicy:
    """Approved tolerances as declarations; no numerical function is executed."""

    absolute_tolerance: float = 1e-12
    relative_tolerance: float = 1e-12
    probability_mass_tolerance: float = 1e-12

    def __post_init__(self) -> None:
        for value in (self.absolute_tolerance, self.relative_tolerance, self.probability_mass_tolerance):
            if type(value) is not float or value != 1e-12:
                raise ValueError("Phase 3 uses its explicitly approved numerical policy")


@dataclass(frozen=True, slots=True)
class RepresentationDescriptor:
    """Declared identity and rules. This object does not validate empirical meaning."""

    representation_name: str
    representation_source: str
    representation_version: str
    binning_or_mapping_rule: str
    field_name: str | None = None
    missing_value_policy: str = "error"
    missing_state_id: str | None = field(default=None, repr=False)
    normalization_profile: str | None = None

    def __post_init__(self) -> None:
        for value in (self.representation_name, self.representation_source,
                      self.representation_version, self.binning_or_mapping_rule):
            _calculation_text(value)
        for value in (self.field_name, self.missing_state_id, self.normalization_profile):
            if value is not None:
                _calculation_text(value)
        if type(self.missing_value_policy) is not str or self.missing_value_policy not in (
                "error", "exclude", "explicit_missing_state"):
            raise ValueError("representation missing policy must be explicit and approved")
        if (self.missing_value_policy == "explicit_missing_state") != (self.missing_state_id is not None):
            raise ValueError("explicit missing policy requires its own literal state ID")
        if self.normalization_profile not in (None, "exact_utf8_v1"):
            raise ValueError("normalization profile has no approved Phase 3 definition")


@dataclass(frozen=True, slots=True)
class RecordStateAssignment:
    """One explicitly supplied assignment or exclusion; no assignment algorithm."""

    record_key: RecordKey
    state_id: str | None = field(repr=False)
    exclusion_reason: CalculationReason | None = None

    def __post_init__(self) -> None:
        if type(self.record_key) is not RecordKey:
            raise TypeError("state assignment needs a canonical record key")
        if self.state_id is None:
            if type(self.exclusion_reason) is not CalculationReason:
                raise ValueError("excluded assignment needs a recorded reason")
        else:
            # Canonical empty strings remain different from null. Metadata and
            # explicit missing-state IDs still require nonempty declarations.
            if type(self.state_id) is not str or "\x00" in self.state_id:
                raise ValueError("assigned state must be literal text without NUL")
            if self.exclusion_reason is not None:
                raise ValueError("assigned state cannot simultaneously be excluded")


@dataclass(frozen=True, slots=True)
class CalculationScope:
    """Caller-selected scope, with explicit included/excluded identities.

    Membership is checked, not inferred. An empty included set remains possible
    for an unavailable calculation. Provenance and representation scopes retain
    separate denominator_basis declarations.
    """

    dataset_versions: tuple[str, ...]
    included_record_keys: tuple[RecordKey, ...] = field(repr=False)
    excluded_record_keys: tuple[RecordKey, ...] = field(repr=False)
    denominator_basis: str
    scope_id: str

    def __post_init__(self) -> None:
        _calculation_strings(self.dataset_versions)
        if not self.dataset_versions or len(set(self.dataset_versions)) != len(self.dataset_versions):
            raise ValueError("calculation scope requires unique explicitly selected versions")
        _calculation_text(self.denominator_basis)
        _calculation_text(self.scope_id)
        for values in (self.included_record_keys, self.excluded_record_keys):
            if type(values) is not tuple or any(type(key) is not RecordKey for key in values):
                raise TypeError("scope identities must be an immutable canonical tuple")
            if len(set(values)) != len(values):
                raise ValueError("scope identities must be unique")
            if any(key.dataset_version not in self.dataset_versions for key in values):
                raise ValueError("scope identity belongs to an undeclared version")
        if set(self.included_record_keys) & set(self.excluded_record_keys):
            raise ValueError("included and excluded scope identities overlap")


@dataclass(frozen=True, slots=True)
class WeightingOptions:
    """Explicit opt-in only; record weights are validated by later kernels."""

    weighting_mode: str = "unweighted"
    weight_field: str | None = None

    def __post_init__(self) -> None:
        if type(self.weighting_mode) is not str or self.weighting_mode not in ("unweighted", "weighted"):
            raise ValueError("weighting mode must be approved")
        if self.weighting_mode == "unweighted" and self.weight_field is not None:
            raise ValueError("unweighted calculation cannot select a weight field")
        if self.weighting_mode == "weighted" and (type(self.weight_field) is not str or self.weight_field != "weight"):
            raise ValueError("weighted calculation requires the explicit canonical weight field")


@dataclass(frozen=True, slots=True)
class TailSelectionOptions:
    """P3-D06 declaration only; no rarity ranking or tail membership calculation."""

    rule: str
    count_threshold: int | None = None
    frequency_threshold: float | None = None
    state_ids: tuple[str, ...] = field(default=(), repr=False)

    def __post_init__(self) -> None:
        if type(self.rule) is not str or self.rule not in (
                "singleton_count", "count_at_or_below", "frequency_at_or_below", "state_list"):
            raise ValueError("tail rule has no approved Phase 3 implementation contract")
        _calculation_strings(self.state_ids)
        if len(set(self.state_ids)) != len(self.state_ids):
            raise ValueError("tail state list must be unique")
        if self.rule == "count_at_or_below":
            _calculation_integer(self.count_threshold)
        elif self.count_threshold is not None:
            raise ValueError("count threshold does not match the selected rule")
        if self.rule == "frequency_at_or_below":
            _calculation_number(self.frequency_threshold)
            if not 0 <= self.frequency_threshold <= 1:
                raise ValueError("frequency threshold must lie in the unit interval")
        elif self.frequency_threshold is not None:
            raise ValueError("frequency threshold does not match the selected rule")
        if self.rule == "state_list":
            if not self.state_ids:
                raise ValueError("explicit tail state list must be nonempty")
        elif self.state_ids:
            raise ValueError("state list does not match the selected rule")


@dataclass(frozen=True, slots=True)
class CalculationMetadata:
    """Numerical-field trace metadata; not a report schema or evidence certificate."""

    metric_name: str
    owner_id: str
    formula_id: str | None
    evidence_class: CalculationEvidenceClass
    unit: str
    method: str
    scope: CalculationScope
    representation: RepresentationDescriptor | None
    weighting: WeightingOptions = WeightingOptions()
    assumptions: tuple[str, ...] = ()
    limitations: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for value in (self.metric_name, self.owner_id, self.unit, self.method):
            _calculation_text(value)
        if self.formula_id is not None:
            _calculation_text(self.formula_id)
        if type(self.evidence_class) is not CalculationEvidenceClass or type(self.scope) is not CalculationScope:
            raise TypeError("calculation metadata requires explicit evidence and scope types")
        if self.representation is not None and type(self.representation) is not RepresentationDescriptor:
            raise TypeError("calculation representation must use its descriptor contract")
        if type(self.weighting) is not WeightingOptions:
            raise TypeError("calculation weighting must use WeightingOptions")
        _calculation_strings(self.assumptions)
        _calculation_strings(self.limitations)


@dataclass(frozen=True, slots=True)
class ScalarCalculation:
    """Already supplied scalar or unavailable marker. Never computes a result."""

    metadata: CalculationMetadata
    status: CalculationStatus
    value: int | float | None = field(repr=False)
    reason_codes: tuple[CalculationReason, ...] = ()

    def __post_init__(self) -> None:
        if type(self.metadata) is not CalculationMetadata or type(self.status) is not CalculationStatus:
            raise TypeError("scalar result requires explicit metadata and status contracts")
        if type(self.reason_codes) is not tuple or any(type(code) is not CalculationReason for code in self.reason_codes):
            raise TypeError("calculation reasons must use the frozen reason registry")
        if self.status is CalculationStatus.UNAVAILABLE:
            if self.value is not None or not self.reason_codes:
                raise ValueError("unavailable calculation requires no value and an explicit reason")
        else:
            _calculation_number(self.value)
            if self.reason_codes:
                raise ValueError("available calculation cannot carry an unavailable reason")


@dataclass(frozen=True, slots=True)
class ExplicitPairContext:
    """Pair declarations only. Later compatibility checks must validate all evidence."""

    earlier_scope: CalculationScope
    later_scope: CalculationScope
    earlier_representation: RepresentationDescriptor
    later_representation: RepresentationDescriptor
    version_order: VersionOrderResult = field(repr=False)

    def __post_init__(self) -> None:
        if type(self.earlier_scope) is not CalculationScope or type(self.later_scope) is not CalculationScope:
            raise TypeError("pair context needs explicit scope contracts")
        if type(self.earlier_representation) is not RepresentationDescriptor or type(self.later_representation) is not RepresentationDescriptor:
            raise TypeError("pair context needs explicit representation descriptors")
        if type(self.version_order) is not VersionOrderResult:
            raise TypeError("pair context needs retained version-order evidence")


@dataclass(frozen=True, slots=True)
class ClosedResamplingMetadata:
    """Closed-model method declarations only. No RNG or formula is called.

    Analytic methods carry no fabricated seed. Sampled paths require named PCG64
    and NumPy identity. State order and replicate scheduling remain explicit.
    No external distribution, reopening weight or experiment scheduler is accepted.
    """

    method: str
    resample_size: int
    simulation_horizon: int
    representation: RepresentationDescriptor
    state_order: tuple[str, ...] = field(repr=False)
    assumptions: tuple[str, ...]
    random_seed: int | None = None
    simulation_replicates: int | None = None
    rng_name: str | None = None
    numpy_version: str | None = None
    replicate_schedule: str | None = None
    model_name: str = "closed_resampling"
    evidence_class: CalculationEvidenceClass = CalculationEvidenceClass.SIMULATION
    experimental: bool = True

    def __post_init__(self) -> None:
        if type(self.model_name) is not str or self.model_name != "closed_resampling":
            raise ValueError("only the finite closed model is selected")
        if self.evidence_class is not CalculationEvidenceClass.SIMULATION or self.experimental is not True:
            raise ValueError("scenario declarations must remain experimental simulation evidence")
        _calculation_integer(self.resample_size, positive=True)
        _calculation_integer(self.simulation_horizon)
        if type(self.representation) is not RepresentationDescriptor:
            raise TypeError("scenario requires an explicit representation descriptor")
        _calculation_strings(self.state_order)
        if not self.state_order or len(set(self.state_order)) != len(self.state_order):
            raise ValueError("scenario state order must be explicit and unique")
        _calculation_strings(self.assumptions)
        if not self.assumptions:
            raise ValueError("scenario assumptions must be recorded")
        if type(self.method) is not str or self.method not in ("analytic_expectation", "analytic_extinction", "sampled_path"):
            raise ValueError("scenario method must be explicitly selected")
        if self.method == "sampled_path":
            _calculation_integer(self.random_seed)
            _calculation_integer(self.simulation_replicates, positive=True)
            if type(self.rng_name) is not str or self.rng_name != "numpy.random.Generator(PCG64)":
                raise ValueError("sampled paths require the approved named generator")
            _calculation_text(self.numpy_version)
            if type(self.replicate_schedule) is not str or self.replicate_schedule != "replicate_major_step_major":
                raise ValueError("sampled paths require explicit replicate-major scheduling")
        elif any(value is not None for value in (self.random_seed, self.simulation_replicates,
                                                self.rng_name, self.numpy_version, self.replicate_schedule)):
            raise ValueError("analytic method must not claim a random realization")
