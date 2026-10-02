"""Summarize declared provenance in one explicit, unfiltered record scope.

Owner IDs:
    PR-004: inherited coverage, confidence and missing-row facts; F-008.
    PR-005: source counts/shares; F-007 and Definitions 11/19.
    T3: direct grounding input basis; Definitions 3.7-3.9 and P3-D08.
    PR-016: deterministic ordering and separate explicit weighted companions.

Inputs:
    A Phase 2 ProvenanceJoinResult, its single-version CalculationScope, and
    optional complete canonical-key weights with explicit weighted opt-in.

Outputs:
    Immutable declared compositions, retained validation coverage/diagnostics,
    direct classification counts and separately named weighted source shares.

Assumptions:
    Phase 2 supplies attachment evidence. Consumed fields and coverage are
    revalidated without a new join. Declarations do not establish source truth.

Limits:
    No content inspection, source independence inference, confidence discount,
    parent traversal, closure interval, other metric, simulation, report,
    orchestration, file/network access, or change to source records.

Current phase status:
    Phase 3 Step 5 only. Explicit in-memory calculations; import-safe.
"""
from __future__ import annotations

from dataclasses import dataclass, field, replace
from math import fsum, isfinite
from types import MappingProxyType

from ..errors import CanonicalValidationError, ErrorCode, WarningCode
from ..io.validation import assess_provenance_row
from ..models import (
    CalculationEvidenceClass, CalculationMetadata, CalculationReason,
    CalculationScope, CalculationStatus, FileRole, ProvenanceAssessment,
    ProvenanceConfidence, ProvenanceJoinResult, ProvenanceMatch, RecordKey,
    ScalarCalculation, SourceType, ValidationCoverage, ValidationMessage,
    ValidationSeverity, WeightingOptions,
)


@dataclass(frozen=True, slots=True)
class DeclaredComposition:
    """A complete category table or unavailable values with exact missingness.

    Missing rows have a separate inventory outside the enum. Missing fields in
    matched rows make this complete table unavailable, never a repaired subset.
    Confidence exposes counts without numeric trust conversion.
    """
    field_name: str
    status: CalculationStatus
    reason_codes: tuple[CalculationReason, ...]
    counts: tuple[tuple[str, int], ...] | None
    shares: tuple[tuple[str, float], ...] | None
    counts_metadata: CalculationMetadata
    shares_metadata: CalculationMetadata | None
    field_coverage: ValidationCoverage
    field_coverage_metadata: CalculationMetadata
    unavailable_record_keys: tuple[RecordKey, ...] = field(repr=False)


@dataclass(frozen=True, slots=True)
class DirectGroundingAssignment:
    """One declaration-bound class, without an ancestry or independence claim."""
    record_key: RecordKey = field(repr=False)
    classification: str
    basis: str
    missing_required_fields: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class DirectGroundingBasis:
    """Unweighted T3 basis only; F-009/F-010 remain unimplemented."""
    scope: CalculationScope
    assignments: tuple[DirectGroundingAssignment, ...] = field(repr=False)
    known_open_count: ScalarCalculation
    known_closed_count: ScalarCalculation
    unresolved_grounding_count: ScalarCalculation
    input_has_errors: bool
    validation_messages: tuple[ValidationMessage, ...] = field(repr=False)
    classification_basis: str = "toolkit_operationalization"
    limitations: tuple[str, ...] = (
        "Direct classes are relative to supplied grounding about the audited loop.",
        "No independent truth, source independence, ancestry or complete closure is certified.",
        "Incomplete required provenance remains unresolved with original errors retained.",
    )


@dataclass(frozen=True, slots=True)
class WeightedSourceComposition:
    """Explicit weight mass and shares, separate from unweighted record counts."""
    status: CalculationStatus
    reason_codes: tuple[CalculationReason, ...]
    weighted_source_type_masses: tuple[tuple[str, float], ...] | None
    weighted_source_type_shares: tuple[tuple[str, float], ...] | None
    mass_metadata: CalculationMetadata
    shares_metadata: CalculationMetadata
    total_weight: ScalarCalculation
    missing_provenance_weight: ScalarCalculation
    weighted_missing_provenance_share: ScalarCalculation
    unavailable_record_keys: tuple[RecordKey, ...] = field(repr=False)
    denominator_basis: str = "all_selected_record_weight_mass"


@dataclass(frozen=True, slots=True)
class ProvenanceCompositionResult:
    """Calculation records with original input validity retained independently."""
    scope: CalculationScope
    source: DeclaredComposition
    confidence: DeclaredComposition
    direct_grounding: DirectGroundingBasis
    weighted_source: WeightedSourceComposition | None
    provenance_row_coverage: ValidationCoverage
    provenance_required_field_coverage: ValidationCoverage
    grounding_field_coverage: ValidationCoverage
    coverage_metadata: tuple[CalculationMetadata, ...]
    analyzed_record_count: ScalarCalculation
    records_with_matching_rows: ScalarCalculation
    missing_provenance_count: ScalarCalculation
    missing_provenance_share: ScalarCalculation
    provenance_supplied: bool
    input_has_errors: bool
    validation_messages: tuple[ValidationMessage, ...] = field(repr=False)
    promoted_warning_codes: tuple[str, ...]
    limitations: tuple[str, ...] = (
        "Declared composition does not certify input validity or increase observability.",
        "Source, confidence, human review and grounding are independent declarations.",
        "Representation exclusions cannot reduce the provenance denominator.",
    )


def _invalid(message: str, *, weight: bool = False) -> CanonicalValidationError:
    return CanonicalValidationError(
        ErrorCode.WEIGHT_INVALID if weight else ErrorCode.SCHEMA_TYPE,
        message, field="weight" if weight else "provenance_composition",
    )


def _text(value: object, *, empty: bool = False) -> str:
    if type(value) is not str or (not value and not empty) or "\x00" in value:
        raise _invalid("composition metadata requires literal text")
    try:
        value.encode("utf-8")
    except UnicodeEncodeError:
        raise _invalid("composition metadata must be valid UTF-8") from None
    return value


def _key(value: object) -> RecordKey:
    if type(value) is not RecordKey:
        raise _invalid("composition requires canonical record identities")
    try:
        return RecordKey(_text(value.dataset_version), _text(value.record_id))
    except (ValueError, TypeError):
        raise _invalid("composition identity violates the canonical contract") from None


def _keys(value: object) -> tuple[RecordKey, ...]:
    if type(value) is not tuple:
        raise _invalid("composition identities must be explicit tuples")
    keys = tuple(_key(key) for key in value)
    if len(set(keys)) != len(keys):
        raise _invalid("duplicate identity in composition scope")
    return tuple(sorted(keys))


def _messages(joined: ProvenanceJoinResult) -> tuple[ValidationMessage, ...]:
    if type(joined.messages) is not tuple or type(joined.promoted_warning_codes) is not tuple:
        raise _invalid("validation messages and promotion codes must be tuples")
    known = {code.value for code in WarningCode}
    for code in joined.promoted_warning_codes:
        if type(code) is not str or code not in known:
            raise _invalid("unrecognized strict warning promotion")
    if len(set(joined.promoted_warning_codes)) != len(joined.promoted_warning_codes):
        raise _invalid("duplicate strict warning promotion")
    messages = []
    for message in joined.messages:
        if type(message) is not ValidationMessage or type(message.severity) is not ValidationSeverity:
            raise _invalid("validation message requires typed severity")
        _text(message.code)
        _text(message.message, empty=True)
        for value in (message.file_path, message.field):
            if value is not None:
                _text(value, empty=True)
        if message.file_role is not None and type(message.file_role) is not FileRole:
            raise _invalid("validation message has an invalid file role")
        for value in (message.row_number, message.line_number):
            if value is not None and (type(value) is not int or value <= 0):
                raise _invalid("validation message has an invalid location")
        key = None if message.record_key is None else _key(message.record_key)
        messages.append(replace(message, record_key=key))
    return tuple(messages)


def _checked_join(joined: ProvenanceJoinResult, scope: CalculationScope
                  ) -> tuple[CalculationScope, tuple[tuple[RecordKey, ProvenanceAssessment | None], ...],
                             tuple[ValidationMessage, ...]]:
    """Reconcile supplied matches without rebuilding attachment from separate tables."""
    if type(joined) is not ProvenanceJoinResult or type(scope) is not CalculationScope:
        raise _invalid("composition needs a validated join and explicit calculation scope")
    if type(scope.dataset_versions) is not tuple or len(scope.dataset_versions) != 1:
        raise _invalid("composition requires exactly one explicit dataset version")
    _text(scope.dataset_versions[0])
    _text(scope.scope_id)
    _text(scope.denominator_basis)
    keys = _keys(scope.included_record_keys)
    if _keys(scope.excluded_record_keys):
        raise _invalid("provenance scope cannot contain representation exclusions")
    try:
        scope = replace(scope, included_record_keys=keys)
    except (ValueError, TypeError):
        raise _invalid("invalid composition scope") from None
    if not keys:
        raise CanonicalValidationError(ErrorCode.EMPTY_DATASET, "composition requires a nonempty valid record scope")
    if (type(joined.selected_dataset_versions) is not tuple
            or any(type(v) is not str for v in joined.selected_dataset_versions)
            or joined.selected_dataset_versions != scope.dataset_versions
            or _keys(joined.scope_record_keys) != keys
            or scope.denominator_basis != "all_valid_records_in_selected_dataset_scope"):
        raise _invalid("composition scope must exactly match the unfiltered Phase 2 join")
    if type(joined.provenance_supplied) is not bool or type(joined.matches) is not tuple:
        raise _invalid("join availability and matches have invalid types")
    messages = _messages(joined)
    errors = {(m.record_key, m.field) for m in messages
              if m.code == ErrorCode.SCHEMA_REQUIRED_FIELD.value
              and m.severity in (ValidationSeverity.ERROR, ValidationSeverity.FATAL)}
    notices = {(m.record_key, m.code, m.severity) for m in messages}
    entries = {}
    key_set = set(keys)
    matched = required = grounding = 0
    missing = []
    for match in joined.matches:
        if type(match) is not ProvenanceMatch:
            raise _invalid("join matches must use ProvenanceMatch")
        key = _key(match.record_key)
        if key in entries or key not in key_set:
            raise _invalid("join match is duplicated or outside the explicit scope")
        assessed = None
        if match.provenance is None:
            missing.append(key)
            warnings = (WarningCode.PROVENANCE_MISSING_ROW.value,)
        else:
            original = match.provenance
            if type(original) is not ProvenanceAssessment or not joined.provenance_supplied:
                raise _invalid("matched row requires explicitly supplied provenance evidence")
            _key(original.record_key)
            assessed = assess_provenance_row(original)
            if (assessed.record_key != key
                    or type(original.required_fields_valid) is not bool
                    or type(original.grounding_known) is not bool
                    or type(original.missing_required_fields) is not tuple
                    or any(type(name) is not str for name in original.missing_required_fields)
                    or original.required_fields_valid != assessed.required_fields_valid
                    or original.grounding_known != assessed.grounding_known
                    or original.missing_required_fields != assessed.missing_required_fields):
                raise _invalid("stored provenance flags disagree with revalidated field evidence")
            if any((key, name) not in errors for name in assessed.missing_required_fields):
                raise _invalid("incomplete provenance must retain its original required-field errors")
            matched += 1
            required += int(assessed.required_fields_valid)
            grounding += int(assessed.grounding_known)
            warnings = tuple(code for name, expected, code in (
                ("external_grounding", "unknown", WarningCode.GROUNDING_UNKNOWN.value),
                ("provenance_confidence", "estimated", WarningCode.PROVENANCE_ESTIMATED.value),
            ) if assessed.values.get(name) == expected)
        for code in warnings:
            severity = ValidationSeverity.ERROR if code in joined.promoted_warning_codes else ValidationSeverity.WARNING
            if (key, code, severity) not in notices:
                raise _invalid("join warning or strict promotion evidence is missing")
        entries[key] = assessed
    if tuple(sorted(entries)) != keys or _keys(joined.missing_record_keys) != tuple(sorted(missing)):
        raise _invalid("join matches or missing-row inventory disagree with scope")
    for coverage, numerator in (
        (joined.provenance_row_coverage, matched),
        (joined.provenance_required_field_coverage, required),
        (joined.grounding_field_coverage, grounding),
    ):
        if (type(coverage) is not ValidationCoverage or type(coverage.numerator) is not int
                or type(coverage.denominator) is not int or type(coverage.denominator_name) is not str
                or coverage.numerator != numerator or coverage.denominator != len(keys)
                or coverage.denominator_name != scope.denominator_basis):
            raise _invalid("inherited validation coverage disagrees with its scoped evidence")
    return scope, tuple((key, entries[key]) for key in keys), messages


def _metadata(name: str, owner: str, formula: str | None, unit: str,
              scope: CalculationScope, method: str, *, derived: bool = False,
              weighting: WeightingOptions = WeightingOptions()) -> CalculationMetadata:
    return CalculationMetadata(
        name, owner, formula,
        CalculationEvidenceClass.DERIVED_METRIC if derived else CalculationEvidenceClass.OBSERVED_FACT,
        unit, method, scope, None, weighting,
        assumptions=("Exact explicit single-version Phase 2 join scope; no representation exclusions.",),
        limitations=("Supplied declarations only; no truth or source-independence certification.",),
    )


def _scalar(name: str, owner: str, value: int | float, scope: CalculationScope,
            method: str, *, unit: str = "records", formula: str | None = None,
            derived: bool = False, weighting: WeightingOptions = WeightingOptions()) -> ScalarCalculation:
    return ScalarCalculation(_metadata(name, owner, formula, unit, scope, method,
                                       derived=derived, weighting=weighting),
                             CalculationStatus.AVAILABLE, value)


def _composition(entries: tuple[tuple[RecordKey, ProvenanceAssessment | None], ...],
                 scope: CalculationScope, field_name: str) -> DeclaredComposition:
    source = field_name == "source_type"
    categories = tuple(item.value for item in (SourceType if source else ProvenanceConfidence))
    counts = {category: 0 for category in categories}
    unavailable = []
    for key, row in entries:
        if row is None:
            continue
        value = row.values.get(field_name)
        if value is None:
            unavailable.append(key)
        else:
            counts[value] += 1
    available = not unavailable
    owner = "PR-005" if source else "PR-004"
    count_meta = _metadata(field_name + "_counts", owner, None, "records", scope,
                           "Definitions 3.3/11.1; count declared canonical categories")
    share_meta = _metadata("source_type_shares", "PR-005", "F-007", "ratio", scope,
                           "category count / all selected valid records", derived=True) if source else None
    return DeclaredComposition(
        field_name, CalculationStatus.AVAILABLE if available else CalculationStatus.UNAVAILABLE,
        () if available else (CalculationReason.PROVENANCE_FIELD_UNAVAILABLE,),
        tuple(counts.items()) if available else None,
        tuple((c, counts[c] / len(entries)) for c in categories) if source and available else None,
        count_meta, share_meta,
        ValidationCoverage(sum(counts.values()), len(entries), scope.denominator_basis),
        _metadata(field_name + "_field_coverage", "PR-004", None, "ratio", scope,
                  "Definitions 3.13; nonmissing valid field / all selected valid records"),
        tuple(unavailable),
    )


def _direct(entries: tuple[tuple[RecordKey, ProvenanceAssessment | None], ...],
            scope: CalculationScope, messages: tuple[ValidationMessage, ...]) -> DirectGroundingBasis:
    counts = {"known_open": 0, "known_closed": 0, "unresolved_grounding": 0}
    assignments = []
    for key, row in entries:
        missing = () if row is None else row.missing_required_fields
        classification = "unresolved_grounding"
        if row is None:
            basis = "missing_provenance_row"
        elif not row.required_fields_valid:
            basis = "incomplete_required_provenance"
        elif row.values["external_grounding"] == "yes":
            classification, basis = "known_open", "valid_direct_grounding_yes"
        elif row.values["external_grounding"] == "no":
            classification, basis = "known_closed", "valid_direct_grounding_no"
        else:
            basis = "declared_unknown_grounding"
        counts[classification] += 1
        assignments.append(DirectGroundingAssignment(key, classification, basis, missing))
    method = "toolkit_operationalization; Definitions 3.7-3.9; P3-D08"
    return DirectGroundingBasis(scope, tuple(assignments),
        _scalar("known_open_count", "T3", counts["known_open"], scope, method),
        _scalar("known_closed_count", "T3", counts["known_closed"], scope, method),
        _scalar("unresolved_grounding_count", "T3", counts["unresolved_grounding"], scope, method),
        any(m.severity in (ValidationSeverity.ERROR, ValidationSeverity.FATAL) for m in messages), messages)


def _weights(weights: object, scope: CalculationScope) -> dict[RecordKey, int | float]:
    if type(weights) not in (dict, MappingProxyType):
        raise _invalid("weighted source shares require an explicit canonical-key map", weight=True)
    checked = {}
    for key, value in weights.items():
        key = _key(key)
        if type(value) not in (int, float):
            raise _invalid("weights must be finite nonnegative built-in numbers", weight=True)
        try:
            valid = isfinite(value) and value >= 0
        except OverflowError:
            valid = False
        if not valid:
            raise _invalid("weights must be finite nonnegative built-in numbers", weight=True)
        checked[key] = value
    if set(checked) != set(scope.included_record_keys):
        raise _invalid("weights must cover all selected records, including missing provenance", weight=True)
    return checked


def _weighted(entries: tuple[tuple[RecordKey, ProvenanceAssessment | None], ...],
              scope: CalculationScope, composition: DeclaredComposition,
              weighting: WeightingOptions, weights: dict[RecordKey, int | float]) -> WeightedSourceComposition:
    groups = {item.value: [] for item in SourceType}
    missing = []
    for key, row in entries:
        if row is None:
            missing.append(weights[key])
        elif row.values.get("source_type") is not None:
            groups[row.values["source_type"]].append(weights[key])
    try:
        total = fsum(weights[key] for key, _ in entries)
        missing_mass = fsum(missing)
        masses = tuple((c, fsum(group)) for c, group in groups.items())
    except OverflowError:
        raise _invalid("source weight sum exceeds the finite numerical range", weight=True) from None
    if not isfinite(total) or total <= 0:
        raise _invalid("weighted source scope requires positive finite total mass", weight=True)
    shares = tuple((c, mass / total) for c, mass in masses)
    missing_share = missing_mass / total
    if ((missing_mass > 0 and missing_share == 0)
            or any(mass > 0 and share == 0 for (_, mass), (_, share) in zip(masses, shares))):
        raise _invalid("positive source weight mass underflows its share", weight=True)
    available = composition.status is CalculationStatus.AVAILABLE
    method = "F-007 weighted variant; category mass / all selected record weight mass"
    return WeightedSourceComposition(
        composition.status, composition.reason_codes, masses if available else None, shares if available else None,
        _metadata("weighted_source_type_masses", "PR-005", None, "user_declared_weight_mass", scope,
                  "Definitions 19; sum explicit weights by source", derived=True, weighting=weighting),
        _metadata("weighted_source_type_shares", "PR-005", "F-007", "ratio", scope,
                  method, derived=True, weighting=weighting),
        _scalar("total_weight", "PR-005", total, scope, "Definitions 19; all selected weights",
                unit="user_declared_weight_mass", derived=True, weighting=weighting),
        _scalar("missing_provenance_weight", "PR-005", missing_mass, scope, "Definitions 19; missing-row mass",
                unit="user_declared_weight_mass", derived=True, weighting=weighting),
        _scalar("weighted_missing_provenance_share", "PR-005", missing_share, scope,
                "Definitions 11.4/19; missing-row mass / all selected record weight mass",
                unit="ratio", derived=True, weighting=weighting),
        composition.unavailable_record_keys,
    )


def classify_direct_grounding(joined: ProvenanceJoinResult, *, scope: CalculationScope) -> DirectGroundingBasis:
    """Return the unweighted direct partition without a stronger lineage claim."""
    scope, entries, messages = _checked_join(joined, scope)
    return _direct(entries, scope, messages)


def summarize_provenance(
    joined: ProvenanceJoinResult, *, scope: CalculationScope,
    weighting: WeightingOptions = WeightingOptions(),
    weights: dict[RecordKey, int | float] | None = None,
) -> ProvenanceCompositionResult:
    """Compute declared composition without loading or attaching records.

    Five source categories plus missing-row share describe the complete scope.
    Confidence remains four counts. A missing field inside a matched row makes
    its table unavailable with reasons, without an invented category or repaired
    denominator. Weighting is opt-in; confidence weights and weighted direct
    classifications are excluded.
    """
    scope, entries, messages = _checked_join(joined, scope)
    if type(weighting) is not WeightingOptions:
        raise _invalid("weighting must use its explicit contract", weight=True)
    try:
        weighting = replace(weighting)
    except (ValueError, TypeError):
        raise _invalid("invalid explicit weighting declaration", weight=True) from None
    if weighting.weighting_mode == "unweighted" and weights is not None:
        raise _invalid("source weights require explicit weighted opt-in", weight=True)
    source = _composition(entries, scope, "source_type")
    confidence = _composition(entries, scope, "provenance_confidence")
    weighted = None if weighting.weighting_mode == "unweighted" else _weighted(
        entries, scope, source, weighting, _weights(weights, scope))
    total = len(entries)
    missing = len(joined.missing_record_keys)
    coverages = (joined.provenance_row_coverage, joined.provenance_required_field_coverage,
                 joined.grounding_field_coverage)
    names = ("provenance_row_coverage", "provenance_required_field_coverage", "grounding_field_coverage")
    return ProvenanceCompositionResult(
        scope, source, confidence, _direct(entries, scope, messages), weighted,
        *tuple(replace(c) for c in coverages),
        tuple(_metadata(name, "PR-004", "F-008" if name == "provenance_row_coverage" else None,
                        "ratio", scope, "Reuse Phase 2 coverage; Definitions 3.10-3.12") for name in names),
        _scalar("analyzed_record_count", "PR-004", total, scope, "All selected valid records"),
        _scalar("records_with_matching_rows", "PR-004", total - missing, scope, "Phase 2 matched-row inventory"),
        _scalar("missing_provenance_count", "PR-004", missing, scope, "Phase 2 missing-row inventory"),
        _scalar("missing_provenance_share", "PR-004", missing / total, scope,
                "Definitions 11.4; missing rows / all selected valid records", unit="ratio", derived=True),
        joined.provenance_supplied,
        any(m.severity in (ValidationSeverity.ERROR, ValidationSeverity.FATAL) for m in messages),
        messages, tuple(joined.promoted_warning_codes),
    )
