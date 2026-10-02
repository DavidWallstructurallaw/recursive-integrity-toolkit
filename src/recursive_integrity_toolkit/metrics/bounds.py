"""Compute the direct closure-exposure interval, without lineage inference.

Owner IDs:
    T3: F-009, F-010; Definitions 5.3-5.5; Phase 3 Step 6.

Inputs:
    Explicit integer counts and a single-version scope, or the accepted Step 5
    ProvenanceCompositionResult. No source files or parent references are read.

Outputs:
    Immutable lower, upper and width calculations, denominator, operationalization
    label, retained coverage, separate confidence disclosure and validation errors.

Assumptions:
    Known-open, known-closed and unresolved classes use the approved direct
    grounding operationalization relative to the audited loop. Supplied evidence
    has not been independently verified by this calculation.

Limits:
    No lineage bounds, midpoint, confidence discount, risk threshold, universal
    score, empirical truth checking, simulation, report or file/network access.
    A count envelope alone never certifies usable dataset provenance.

Current phase status:
    Phase 3 Step 6 direct bounds only. Pure explicit calls; import-safe.
"""
from __future__ import annotations

from dataclasses import dataclass, field, replace
from math import isclose

from ..errors import CanonicalValidationError, ErrorCode
from ..models import (
    CalculationEvidenceClass, CalculationMetadata, CalculationReason,
    CalculationScope, CalculationStatus, NumericalPolicy, ProvenanceConfidence,
    RecordKey, ScalarCalculation, ValidationCoverage, ValidationMessage,
    ValidationSeverity, WeightingOptions,
)
from .provenance import (
    DeclaredComposition, DirectGroundingAssignment, DirectGroundingBasis,
    ProvenanceCompositionResult,
)


@dataclass(frozen=True, slots=True)
class DirectClosureExposureBounds:
    """Direct interval and its evidence basis. This object is not a report."""

    scope: CalculationScope
    known_open_count: int
    known_closed_count: int
    unresolved_grounding_count: int
    denominator: int
    denominator_basis: str
    lower_bound: ScalarCalculation
    upper_bound: ScalarCalculation
    interval_width: ScalarCalculation
    classification_basis: str = "toolkit_operationalization"
    operationalization_label: str = "toolkit_operationalization"
    provenance_row_coverage: ValidationCoverage | None = None
    provenance_required_field_coverage: ValidationCoverage | None = None
    grounding_field_coverage: ValidationCoverage | None = None
    confidence_field_coverage: ValidationCoverage | None = None
    confidence_status: CalculationStatus | None = None
    confidence_counts: tuple[tuple[str, int], ...] | None = None
    confidence_disclosure: str = "provenance_confidence_is_separate_and_does_not_discount_grounding"
    input_has_errors: bool = False
    validation_messages: tuple[ValidationMessage, ...] = field(default=(), repr=False)
    limitations: tuple[str, ...] = (
        "Direct exposure is relative to the audited loop and supplied metadata.",
        "Toolkit operationalization; metadata can be incorrect and hidden dependencies unobserved.",
        "Confidence remains separate; no lineage, midpoint, threshold or causal claim.",
    )

    @property
    def status(self) -> CalculationStatus:
        return self.lower_bound.status


def _invalid(message: str, code: ErrorCode = ErrorCode.SCHEMA_TYPE) -> CanonicalValidationError:
    return CanonicalValidationError(code, message, field="direct_closure_exposure")


def _text(value: object) -> str:
    if type(value) is not str or not value or "\x00" in value:
        raise _invalid("direct closure metadata requires literal text")
    try:
        value.encode("utf-8")
    except UnicodeEncodeError:
        raise _invalid("direct closure metadata must be valid UTF-8") from None
    return value


def _key(value: object) -> RecordKey:
    if type(value) is not RecordKey:
        raise _invalid("direct closure requires canonical record identities")
    try:
        return RecordKey(_text(value.dataset_version), _text(value.record_id))
    except (TypeError, ValueError):
        raise _invalid("direct closure identity violates the canonical contract") from None


def _count(value: object) -> int:
    if type(value) is not int or value < 0:
        raise _invalid("direct closure counts must be nonnegative built-in integers")
    return value


def _scope(value: object, total: int) -> CalculationScope:
    if type(value) is not CalculationScope:
        raise _invalid("direct closure requires an explicit CalculationScope")
    if type(value.dataset_versions) is not tuple or len(value.dataset_versions) != 1:
        raise _invalid("direct closure requires one explicit dataset version")
    _text(value.dataset_versions[0])
    _text(value.scope_id)
    if (type(value.denominator_basis) is not str or
            value.denominator_basis != "all_valid_records_in_selected_dataset_scope"):
        raise _invalid("direct closure requires the complete valid-record denominator")
    if (type(value.included_record_keys) is not tuple or
            type(value.excluded_record_keys) is not tuple or value.excluded_record_keys):
        raise _invalid("direct closure scope cannot contain representation exclusions")
    keys = tuple(_key(key) for key in value.included_record_keys)
    if len(keys) != total or len(set(keys)) != total:
        raise _invalid("scope size and unique identities must match the denominator")
    try:
        return replace(value, included_record_keys=tuple(sorted(keys)))
    except (ValueError, TypeError):
        raise _invalid("direct closure scope violates its canonical contract") from None


def _metric(name: str, formula: str | None, value: float | None,
            scope: CalculationScope, method: str) -> ScalarCalculation:
    metadata = CalculationMetadata(
        name, "T3", formula, CalculationEvidenceClass.DERIVED_METRIC, "ratio", method,
        scope, None, WeightingOptions(),
        assumptions=("Approved direct grounding partition; uncertainty remains unresolved.",),
        limitations=("Toolkit operationalization relative to supplied metadata, without lineage or truth certification.",),
    )
    return ScalarCalculation(
        metadata, CalculationStatus.UNAVAILABLE if value is None else CalculationStatus.AVAILABLE,
        value, (CalculationReason.PROVENANCE_FIELD_UNAVAILABLE,) if value is None else (),
    )


def closure_exposure_bounds(*, known_closed: int, unresolved: int, total: int,
                            scope: CalculationScope) -> DirectClosureExposureBounds:
    """Pure F-009/F-010 envelope; no dataset evidence is certified by counts."""
    known_closed, unresolved, total = _count(known_closed), _count(unresolved), _count(total)
    if total == 0:
        raise _invalid("direct bounds require positive total", ErrorCode.EMPTY_DATASET)
    if known_closed + unresolved > total:
        raise _invalid("known closed plus unresolved exceeds total")
    scope = _scope(scope, total)
    lower = known_closed / total
    upper = (known_closed + unresolved) / total
    width = unresolved / total
    policy = NumericalPolicy()
    if not (0 <= lower <= upper <= 1) or not isclose(
            upper - lower, width, abs_tol=policy.absolute_tolerance, rel_tol=policy.relative_tolerance):
        raise _invalid("direct interval numerical invariant failed")
    return DirectClosureExposureBounds(
        scope, total - known_closed - unresolved, known_closed, unresolved, total, scope.denominator_basis,
        _metric("direct_closure_exposure_lower_bound", "F-009", lower, scope, "known_closed_count / total_record_count"),
        _metric("direct_closure_exposure_upper_bound", "F-010", upper, scope,
                "(known_closed_count + unresolved_grounding_count) / total_record_count"),
        _metric("direct_closure_exposure_interval_width", None, width, scope,
                "upper_bound - lower_bound = unresolved_grounding_count / total_record_count"),
    )


def _observed(value: object, name: str, owner: str, scope: CalculationScope) -> int:
    if type(value) is not ScalarCalculation or value.status is not CalculationStatus.AVAILABLE:
        raise _invalid("direct basis requires available observed counts")
    count = _count(value.value)
    meta = value.metadata
    if (type(meta) is not CalculationMetadata or type(meta.metric_name) is not str or meta.metric_name != name
            or type(meta.owner_id) is not str or meta.owner_id != owner
            or meta.evidence_class is not CalculationEvidenceClass.OBSERVED_FACT
            or type(meta.unit) is not str or meta.unit != "records"
            or _scope(meta.scope, len(scope.included_record_keys)) != scope
            or type(meta.weighting) is not WeightingOptions
            or type(meta.weighting.weighting_mode) is not str or meta.weighting.weighting_mode != "unweighted"
            or meta.weighting.weight_field is not None or type(value.reason_codes) is not tuple or value.reason_codes):
        raise _invalid("observed count metadata disagrees with the direct basis")
    return count


def _coverage(value: object, scope: CalculationScope) -> ValidationCoverage:
    if (type(value) is not ValidationCoverage or type(value.numerator) is not int
            or type(value.denominator) is not int or value.denominator != len(scope.included_record_keys)
            or not 0 <= value.numerator <= value.denominator
            or type(value.denominator_name) is not str or value.denominator_name != scope.denominator_basis):
        raise _invalid("coverage disagrees with direct closure scope")
    return replace(value)


def _basis(value: object, scope: CalculationScope) -> tuple[tuple[int, int, int], int, int]:
    """Reconcile Step 5 direct classes and reasons, without reading parent data."""
    total = len(scope.included_record_keys)
    if type(value) is not DirectGroundingBasis or _scope(value.scope, total) != scope:
        raise _invalid("direct grounding basis has the wrong scope")
    if type(value.classification_basis) is not str or value.classification_basis != "toolkit_operationalization":
        raise _invalid("direct grounding basis lost its operationalization label")
    if type(value.assignments) is not tuple or len(value.assignments) != total:
        raise _invalid("direct assignments must exhaust the scope")
    classes = {
        "missing_provenance_row": "unresolved_grounding",
        "incomplete_required_provenance": "unresolved_grounding",
        "valid_direct_grounding_yes": "known_open",
        "valid_direct_grounding_no": "known_closed",
        "declared_unknown_grounding": "unresolved_grounding",
    }
    keys, seen = set(scope.included_record_keys), set()
    counts = {"known_open": 0, "known_closed": 0, "unresolved_grounding": 0}
    missing = incomplete = 0
    for assignment in value.assignments:
        if type(assignment) is not DirectGroundingAssignment:
            raise _invalid("direct assignments must use their exact contract")
        key = _key(assignment.record_key)
        if key not in keys or key in seen:
            raise _invalid("direct assignment identity is duplicated or outside scope")
        seen.add(key)
        basis, classification = assignment.basis, assignment.classification
        if (type(basis) is not str or basis not in classes or type(classification) is not str
                or classification != classes[basis]):
            raise _invalid("direct class disagrees with its declared basis")
        fields = assignment.missing_required_fields
        if (type(fields) is not tuple or any(type(name) is not str or name not in
                ("source_type", "provenance_confidence", "external_grounding") for name in fields)
                or len(set(fields)) != len(fields)
                or bool(fields) != (basis == "incomplete_required_provenance")):
            raise _invalid("direct class has inconsistent required-field evidence")
        missing += int(basis == "missing_provenance_row")
        incomplete += int(basis == "incomplete_required_provenance")
        counts[classification] += 1
    observed = tuple(_observed(scalar, name, "T3", scope) for scalar, name in (
        (value.known_open_count, "known_open_count"), (value.known_closed_count, "known_closed_count"),
        (value.unresolved_grounding_count, "unresolved_grounding_count")))
    if observed != (counts["known_open"], counts["known_closed"], counts["unresolved_grounding"]):
        raise _invalid("direct count partition disagrees with the assignments")
    return observed, missing, incomplete


def _messages(result: ProvenanceCompositionResult) -> tuple[ValidationMessage, ...]:
    if type(result.validation_messages) is not tuple or type(result.direct_grounding.validation_messages) is not tuple:
        raise _invalid("direct bounds require immutable validation messages")
    messages = []
    for message in result.validation_messages:
        if type(message) is not ValidationMessage or type(message.severity) is not ValidationSeverity:
            raise _invalid("direct validation messages have invalid types")
        _text(message.code)
        _text(message.message)
        key = None if message.record_key is None else _key(message.record_key)
        messages.append(replace(message, record_key=key))
    messages = tuple(messages)
    if messages != result.direct_grounding.validation_messages:
        raise _invalid("direct bounds cannot drop original validation messages")
    error = any(m.severity in (ValidationSeverity.ERROR, ValidationSeverity.FATAL) for m in messages)
    if (type(result.input_has_errors) is not bool or type(result.direct_grounding.input_has_errors) is not bool
            or result.input_has_errors != error or result.direct_grounding.input_has_errors != error):
        raise _invalid("error flags disagree with retained validation messages")
    errors = {(m.record_key, m.field) for m in messages if m.code == ErrorCode.SCHEMA_REQUIRED_FIELD.value
              and m.severity in (ValidationSeverity.ERROR, ValidationSeverity.FATAL)}
    for assignment in result.direct_grounding.assignments:
        if any((assignment.record_key, name) not in errors for name in assignment.missing_required_fields):
            raise _invalid("incomplete provenance has lost its required-field errors")
    return messages


def _confidence(value: object, scope: CalculationScope, matched: int
                ) -> tuple[ValidationCoverage, CalculationStatus, tuple[tuple[str, int], ...] | None]:
    if type(value) is not DeclaredComposition or value.field_name != "provenance_confidence":
        raise _invalid("direct bounds require separate declared confidence composition")
    coverage = _coverage(value.field_coverage, scope)
    if type(value.unavailable_record_keys) is not tuple or type(value.reason_codes) is not tuple:
        raise _invalid("confidence disclosure requires immutable missingness")
    missing = tuple(_key(key) for key in value.unavailable_record_keys)
    if len(set(missing)) != len(missing) or not set(missing) <= set(scope.included_record_keys):
        raise _invalid("confidence missingness does not match the scope")
    if coverage.numerator + len(missing) != matched:
        raise _invalid("confidence coverage does not reconcile to matched rows")
    if value.shares is not None or value.shares_metadata is not None:
        raise _invalid("confidence must remain counts without discount weights")
    if missing:
        if (value.status is not CalculationStatus.UNAVAILABLE or value.counts is not None
                or value.reason_codes != (CalculationReason.PROVENANCE_FIELD_UNAVAILABLE,)):
            raise _invalid("incomplete confidence cannot be certified as available")
        return coverage, value.status, None
    if value.status is not CalculationStatus.AVAILABLE or value.reason_codes or type(value.counts) is not tuple:
        raise _invalid("complete confidence counts must remain available")
    counts = []
    for item in value.counts:
        if type(item) is not tuple or len(item) != 2 or type(item[0]) is not str:
            raise _invalid("confidence counts require explicit category pairs")
        counts.append((item[0], _count(item[1])))
    if (tuple(name for name, _ in counts) != tuple(item.value for item in ProvenanceConfidence)
            or sum(count for _, count in counts) != matched):
        raise _invalid("confidence categories or total are inconsistent")
    return coverage, value.status, tuple(counts)


def direct_closure_exposure(result: ProvenanceCompositionResult) -> DirectClosureExposureBounds:
    """Dataset-facing direct interval; original errors never turn into validation success.

    All-missing/incomplete provenance yields unavailable scalars. Valid explicit
    unknown grounding permits the full [0,1] interval. Revalidation checks internal
    consistency of the supplied Step 5 result, without claiming independent truth.
    """
    if type(result) is not ProvenanceCompositionResult or type(result.analyzed_record_count) is not ScalarCalculation:
        raise _invalid("direct bounds require the accepted Step 5 composition contract")
    total = _count(result.analyzed_record_count.value)
    if total == 0:
        raise _invalid("direct bounds require nonempty provenance scope", ErrorCode.EMPTY_DATASET)
    scope = _scope(result.scope, total)
    _observed(result.analyzed_record_count, "analyzed_record_count", "PR-004", scope)
    counts, missing, incomplete = _basis(result.direct_grounding, scope)
    matched = total - missing
    if (type(result.provenance_supplied) is not bool or (not result.provenance_supplied and matched)
            or _observed(result.records_with_matching_rows, "records_with_matching_rows", "PR-004", scope) != matched
            or _observed(result.missing_provenance_count, "missing_provenance_count", "PR-004", scope) != missing):
        raise _invalid("provenance availability disagrees with the direct partition")
    row_cov = _coverage(result.provenance_row_coverage, scope)
    required_cov = _coverage(result.provenance_required_field_coverage, scope)
    grounding_cov = _coverage(result.grounding_field_coverage, scope)
    if (row_cov.numerator != matched or required_cov.numerator != matched - incomplete
            or not counts[0] + counts[1] <= grounding_cov.numerator <= counts[0] + counts[1] + incomplete):
        raise _invalid("inherited coverage disagrees with direct assignment evidence")
    confidence_cov, confidence_status, confidence_counts = _confidence(result.confidence, scope, matched)
    messages = _messages(result)
    kernel = closure_exposure_bounds(known_closed=counts[1], unresolved=counts[2], total=total, scope=scope)
    lower, upper, width = kernel.lower_bound, kernel.upper_bound, kernel.interval_width
    if required_cov.numerator == 0:
        lower = _metric("direct_closure_exposure_lower_bound", "F-009", None, scope, "no usable required-provenance row")
        upper = _metric("direct_closure_exposure_upper_bound", "F-010", None, scope, "no usable required-provenance row")
        width = _metric("direct_closure_exposure_interval_width", None, None, scope, "no usable required-provenance row")
    return replace(kernel, lower_bound=lower, upper_bound=upper, interval_width=width,
        provenance_row_coverage=row_cov, provenance_required_field_coverage=required_cov,
        grounding_field_coverage=grounding_cov, confidence_field_coverage=confidence_cov,
        confidence_status=confidence_status, confidence_counts=confidence_counts,
        input_has_errors=result.input_has_errors, validation_messages=messages)
