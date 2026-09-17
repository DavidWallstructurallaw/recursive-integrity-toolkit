"""Compute single-scope frequencies, positive support and named diversity.

Owner IDs:
    T1: F-001, F-002, F-003, F-004. PR-016 deterministic ordering.
    UD-021: explicitly requested weighted variants (Definitions sections 9.5, 19).

Inputs:
    Validated in-memory representation assignments; or explicit count/probability
    pairs with a single-version CalculationScope and RepresentationDescriptor.
    Weighted assignments require an exact canonical-key map of included weights.

Outputs:
    Immutable scoped counts, frequencies, support, Gini-Simpson diversity and
    Simpson concentration. Weighted outputs accompany the unchanged unweighted
    result. Supplied probability vectors are labelled as supplied, not empirical.

Assumptions:
    State identities preserve the declared representation. Counts are integers.
    Negative/nonfinite components fail before mass-tolerance checks. Accepted
    probability residuals are retained, never clipped, smoothed or normalized.

Limits:
    No I/O, inference, randomness, pair comparison, tail, source-share, closure,
    lineage, Shannon entropy, functional-failure verdict, report or orchestration.
    A structurally valid supplied assignment does not certify its empirical origin.

Current phase status:
    Phase 3 Step 4 single-scope F-001 through F-004 only.
"""
from __future__ import annotations

from dataclasses import dataclass, field, replace
from math import fsum, isfinite
from types import MappingProxyType

from ..errors import CanonicalValidationError, ErrorCode
from ..models import (
    CalculationEvidenceClass, CalculationMetadata, CalculationReason,
    CalculationScope, CalculationStatus, NumericalPolicy, RecordKey,
    RecordStateAssignment, RepresentationDescriptor, ScalarCalculation,
    ValidationCoverage, ValidationMessage, ValidationSeverity, WeightingOptions,
)
from ..representations.base import RepresentationResult, RepresentationSelection


@dataclass(frozen=True, slots=True)
class StateFrequency:
    """One state; count/mass table metadata lives on its enclosing result."""

    state_id: str = field(repr=False)
    state_count: int | None
    state_mass: int | float | None
    state_frequency: float


@dataclass(frozen=True, slots=True)
class DistributionMetrics:
    """F-001 through F-004, with every table bound to a declared basis."""

    scope: CalculationScope
    representation: RepresentationDescriptor
    weighting: WeightingOptions
    input_basis: str
    status: CalculationStatus
    reason_codes: tuple[CalculationReason, ...]
    analyzed_record_count: int
    frequency_denominator: int | float | None
    denominator_basis: str
    states: tuple[StateFrequency, ...] = field(repr=False)
    support: tuple[str, ...] = field(repr=False)
    support_size: ScalarCalculation
    gini_simpson_diversity: ScalarCalculation
    simpson_concentration: ScalarCalculation
    frequency_metadata: CalculationMetadata
    count_metadata: CalculationMetadata | None
    mass_metadata: CalculationMetadata | None
    supplied_probability_total: float | None
    probability_residual: float | None
    numerical_policy: NumericalPolicy = NumericalPolicy()
    limitations: tuple[str, ...] = (
        "Distributional concentration does not establish functional failure.",
        "Record-form support and declared field support do not certify semantic coverage.",
        "No source, grounding, independence, ancestry or model-performance claim follows.",
        "Accepted round-off residuals are disclosed and left unchanged.",
    )


@dataclass(frozen=True, slots=True)
class StateDistributionResult:
    """Empirical unweighted output plus a separately enabled weighted result."""

    unweighted: DistributionMetrics
    weighted: DistributionMetrics | None
    coverage: ValidationCoverage
    selection_basis: str
    selection_messages: tuple[ValidationMessage, ...]
    excluded_assignments: tuple[RecordStateAssignment, ...] = field(repr=False)


def _invalid(message: str, *, weight: bool = False) -> CanonicalValidationError:
    return CanonicalValidationError(
        ErrorCode.WEIGHT_INVALID if weight else ErrorCode.SCHEMA_TYPE, message,
        field="weight" if weight else "distribution",
    )


def _text(value: object, *, empty: bool = False) -> str:
    if type(value) is not str or (not value and not empty) or "\x00" in value:
        raise _invalid("distribution metadata and state identities must be literal text")
    try:
        value.encode("utf-8")
    except UnicodeEncodeError:
        raise _invalid("distribution text is not valid UTF-8") from None
    return value


def _key(value: object) -> RecordKey:
    if (type(value) is not RecordKey or type(value.dataset_version) is not str
            or type(value.record_id) is not str):
        raise _invalid("distribution scope requires canonical record identities")
    try:
        return RecordKey(_text(value.dataset_version), _text(value.record_id))
    except (ValueError, TypeError):
        raise _invalid("invalid canonical identity in distribution scope") from None


def _context(scope: CalculationScope, representation: RepresentationDescriptor
             ) -> tuple[CalculationScope, RepresentationDescriptor]:
    if type(scope) is not CalculationScope or type(representation) is not RepresentationDescriptor:
        raise _invalid("calculation requires explicit scope and representation contracts")
    if type(scope.dataset_versions) is not tuple or len(scope.dataset_versions) != 1:
        raise _invalid("single-scope metrics require exactly one selected dataset version")
    try:
        RecordKey(_text(scope.dataset_versions[0]), "scope-check")
    except (ValueError, TypeError):
        raise _invalid("selected version violates the canonical identity contract") from None
    _text(scope.scope_id)
    _text(scope.denominator_basis)
    for keys in (scope.included_record_keys, scope.excluded_record_keys):
        if type(keys) is not tuple:
            raise _invalid("calculation scope identities must use explicit tuples")
        for key in keys:
            _key(key)
    for text in (representation.representation_name, representation.representation_source,
                 representation.representation_version, representation.binning_or_mapping_rule,
                 representation.missing_value_policy):
        _text(text)
    for text in (representation.field_name, representation.missing_state_id, representation.normalization_profile):
        if text is not None:
            _text(text)
    try:
        checked_scope = replace(scope, included_record_keys=tuple(sorted(scope.included_record_keys)),
                                excluded_record_keys=tuple(sorted(scope.excluded_record_keys)))
        checked_representation = replace(representation)
    except (ValueError, TypeError):
        raise _invalid("invalid scope or representation declaration") from None
    return checked_scope, checked_representation


def _number(value: object, *, weight: bool = False) -> int | float:
    if type(value) not in (int, float):
        raise _invalid("mass must be a built-in finite nonnegative number", weight=weight)
    try:
        valid = isfinite(value) and value >= 0
    except OverflowError:
        valid = False
    if not valid:
        raise _invalid("mass must be a built-in finite nonnegative number", weight=weight)
    return value


def _pairs(values: object) -> tuple[tuple[str, object], ...]:
    if type(values) in (dict, MappingProxyType):
        entries = tuple(values.items())
    elif type(values) is tuple:
        entries = values
    else:
        raise _invalid("supply a plain state map or an immutable tuple of state-value pairs")
    seen = set()
    checked = []
    for pair in entries:
        if type(pair) is not tuple or len(pair) != 2:
            raise _invalid("state-value entry must contain exactly two items")
        state = _text(pair[0], empty=True)
        if state in seen:
            raise _invalid("duplicate state identity in supplied distribution")
        seen.add(state)
        checked.append((state, pair[1]))
    return tuple(sorted(checked))


def _probabilities(pairs: tuple[tuple[str, object], ...]) -> float:
    if not pairs:
        raise _invalid("an explicit probability distribution cannot be empty")
    for _, value in pairs:
        _number(value)
        if value > 1:
            raise _invalid("probability component is outside the unit interval")
    try:
        total = fsum(value for _, value in pairs)
    except OverflowError:
        raise _invalid("probability total is not representable") from None
    if total <= 0 or abs(total - 1.0) > NumericalPolicy().probability_mass_tolerance:
        raise _invalid("probability mass must equal one within the approved absolute tolerance")
    return total


def _metadata(name: str, formula: str | None, unit: str, scope: CalculationScope,
              representation: RepresentationDescriptor, weighting: WeightingOptions,
              method: str, *, supplied: bool = False) -> CalculationMetadata:
    return CalculationMetadata(
        name, "T1", formula,
        CalculationEvidenceClass.OBSERVED_FACT if supplied else CalculationEvidenceClass.DERIVED_METRIC,
        unit, method, scope, representation, weighting,
        assumptions=("One explicitly selected version and declared representation.",
                     "No implicit pooling, probability repair, confidence weighting or sampling."),
        limitations=("Representation-bound; does not establish functional failure or semantic completeness.",),
    )


def _metrics(pairs, counts, masses, *, scope, representation, weighting, basis,
             denominator, denominator_basis, reason=None) -> DistributionMetrics:
    """The only F-002/F-003/F-004 arithmetic site. No clipping or normalization."""
    status = CalculationStatus.AVAILABLE if reason is None else CalculationStatus.UNAVAILABLE
    reasons = () if reason is None else (reason,)
    total = _probabilities(pairs) if reason is None else None
    support = tuple(state for state, value in pairs if value > 0)
    concentration = fsum(value * value for _, value in pairs) if reason is None else None
    diversity = 1.0 - concentration if reason is None else None
    if reason is None and not (0 <= concentration <= 1 and 0 <= diversity < 1):
        raise _invalid("distribution moments are outside the supported floating-point range")
    scalar_results = []
    for name, formula, unit, value in (
        ("support_size", "F-002", "states", len(support) if reason is None else None),
        ("gini_simpson_diversity", "F-003", "dimensionless", diversity),
        ("simpson_concentration", "F-004", "dimensionless", concentration),
    ):
        metadata = _metadata(name, formula, unit, scope, representation, weighting, basis)
        scalar_results.append(ScalarCalculation(metadata, status, value, reasons))
    supplied = basis == "explicit_probability_vector"
    frequency_metadata = _metadata(
        "state_frequency", None if supplied else "F-001", "ratio", scope, representation,
        weighting, basis, supplied=supplied,
    )
    count_metadata = None if counts is None else _metadata(
        "state_count", None, "records", scope, representation, WeightingOptions(),
        "Definitions 7.1; " + basis, supplied=True,
    )
    mass_metadata = None if masses is None else _metadata(
        "state_mass", None, "user_declared_weight_mass", scope, representation, weighting,
        "Definitions 9.5; canonical record weights summed within each state",
    )
    states = tuple(StateFrequency(state, None if counts is None else counts[state],
                                  None if masses is None else masses[state], value)
                   for state, value in pairs)
    return DistributionMetrics(
        scope, representation, weighting, basis, status, reasons, len(scope.included_record_keys),
        denominator, denominator_basis, states, support, scalar_results[0], scalar_results[1],
        scalar_results[2], frequency_metadata, count_metadata, mass_metadata, total,
        None if total is None else total - 1.0,
    )


def distribution_from_counts(
    counts: dict[str, int] | tuple[tuple[str, int], ...], *,
    scope: CalculationScope, representation: RepresentationDescriptor,
) -> DistributionMetrics:
    """F-001 exact counts divided by N; count sum must match included identities.

    Explicit zero-count states are retained but excluded from positive support.
    This validates a declared aggregate, without claiming to have checked its
    record-level empirical correspondence. Empty/zero-total aggregates fail.
    """
    scope, representation = _context(scope, representation)
    pairs = _pairs(counts)
    for _, count in pairs:
        if type(count) is not int or count < 0:
            raise _invalid("state counts must be nonnegative integers, excluding booleans")
    total = sum(count for _, count in pairs)
    if total <= 0 or total != len(scope.included_record_keys):
        raise _invalid("positive count total must match the included-record denominator")
    frequencies = tuple((state, count / total) for state, count in pairs)
    return _metrics(frequencies, dict(pairs), None, scope=scope, representation=representation,
                    weighting=WeightingOptions(), basis="explicit_counts_divided_by_included_records",
                    denominator=total, denominator_basis=scope.denominator_basis)


def distribution_from_probabilities(
    probabilities: dict[str, float] | tuple[tuple[str, float], ...], *,
    scope: CalculationScope, representation: RepresentationDescriptor,
) -> DistributionMetrics:
    """F-002/F-003/F-004 on an explicit vector; no fabricated count table or F-001.

    Requires a nonempty named calculation scope. The probability values are
    supplied facts, not frequencies recomputed from that scope's record values.
    The original probability total and residual are disclosed, without repair.
    """
    scope, representation = _context(scope, representation)
    if not scope.included_record_keys:
        raise _invalid("explicit distribution requires a nonempty calculation scope")
    pairs = _pairs(probabilities)
    return _metrics(pairs, None, None, scope=scope, representation=representation,
                    weighting=WeightingOptions(), basis="explicit_probability_vector",
                    denominator=None, denominator_basis="explicit_probability_mass")


def _assignments(represented: RepresentationResult):
    if type(represented) is not RepresentationResult or type(represented.selection) is not RepresentationSelection:
        raise _invalid("record calculation requires a RepresentationResult")
    selection = represented.selection
    scope, representation = _context(represented.scope, selection.descriptor)
    _text(selection.selection_basis)
    if type(selection.considered_fields) is not tuple or type(selection.messages) is not tuple:
        raise _invalid("selection evidence must be explicit tuples")
    for name in selection.considered_fields:
        _text(name)
    for message in selection.messages:
        if type(message) is not ValidationMessage or type(message.severity) is not ValidationSeverity:
            raise _invalid("selection message has an invalid type")
        _text(message.code)
        _text(message.message)
    if type(represented.assignments) is not tuple or type(represented.field_states) is not tuple:
        raise _invalid("assignments and field states must be explicit tuples")
    included, excluded = set(scope.included_record_keys), set(scope.excluded_record_keys)
    states = {}
    for entry in represented.field_states:
        if type(entry) is not tuple or len(entry) != 2:
            raise _invalid("field state evidence is malformed")
        key = _key(entry[0])
        if type(entry[1]) is not str or entry[1] not in ("value", "absent", "null") or key in states:
            raise _invalid("field state evidence is invalid or duplicated")
        states[key] = entry[1]
    if set(states) != included | excluded:
        raise _invalid("field state evidence does not match the selected scope")
    assignments = {}
    for assignment in represented.assignments:
        if type(assignment) is not RecordStateAssignment:
            raise _invalid("assignment requires RecordStateAssignment")
        key = _key(assignment.record_key)
        if key in assignments or key not in states:
            raise _invalid("assignment identity is duplicated or outside its scope")
        value = assignment.state_id
        if key in included:
            _text(value, empty=True)
            if assignment.exclusion_reason is not None:
                raise _invalid("included state cannot carry an exclusion reason")
            if states[key] != "value":
                if representation.missing_value_policy != "explicit_missing_state" or value != representation.missing_state_id:
                    raise _invalid("missing field lacks an explicit missing-state assignment")
            elif representation.missing_state_id is not None and value == representation.missing_state_id:
                raise _invalid("explicit missing-state ID collides with an observed state")
        elif (value is not None or type(assignment.exclusion_reason) is not CalculationReason
              or states[key] == "value" or representation.missing_value_policy != "exclude"):
            raise _invalid("excluded assignment is inconsistent with the declared missing policy")
        assignments[key] = RecordStateAssignment(key, value, assignment.exclusion_reason)
    if set(assignments) != included | excluded:
        raise _invalid("assignments do not cover their declared scope")
    reason = CalculationReason.EMPTY_SCOPE if not assignments else CalculationReason.ALL_EXCLUDED if not included else None
    expected_status = CalculationStatus.UNAVAILABLE if reason is not None else CalculationStatus.AVAILABLE
    expected_reasons = (reason,) if reason is not None else ()
    coverage = represented.coverage
    if (type(coverage) is not ValidationCoverage or type(coverage.numerator) is not int
            or type(coverage.denominator) is not int or coverage.numerator != len(included)
            or coverage.denominator != len(assignments) or coverage.denominator_name != "selected_valid_records"
            or type(represented.status) is not CalculationStatus or represented.status is not expected_status
            or represented.reason_codes != expected_reasons or type(represented.reason_codes) is not tuple):
        raise _invalid("representation summary disagrees with its assignments and scope")
    return scope, representation, tuple(assignments[key] for key in sorted(assignments)), reason


def _weights(weights, scope) -> dict[RecordKey, int | float]:
    if type(weights) not in (dict, MappingProxyType):
        raise _invalid("weighted analysis requires an explicit plain weight map", weight=True)
    checked = {}
    for key, value in weights.items():
        key = _key(key)
        checked[key] = _number(value, weight=True)
    if set(checked) != set(scope.included_record_keys):
        raise _invalid("weights must exactly cover the included weighted scope", weight=True)
    return checked


def calculate_state_distribution(
    represented: RepresentationResult, *, weighting: WeightingOptions = WeightingOptions(),
    weights: dict[RecordKey, float] | None = None,
) -> StateDistributionResult:
    """Compute empirical single-version metrics without altering the input audit.

    Weighting is off unless explicitly selected. Providing weights while it is
    off is an error, rather than automatic activation. Weighted outputs preserve
    all unweighted counts. Excluded records never shrink a provenance denominator.
    """
    scope, representation, assignments, reason = _assignments(represented)
    if type(weighting) is not WeightingOptions:
        raise _invalid("weighting must use its explicit contract", weight=True)
    try:
        weighting = replace(weighting)
    except (ValueError, TypeError):
        raise _invalid("unsupported weighting declaration", weight=True) from None
    if weighting.weighting_mode == "unweighted" and weights is not None:
        raise _invalid("weight map requires explicit weighted opt-in", weight=True)
    checked_weights = _weights(weights, scope) if weighting.weighting_mode == "weighted" else None
    counts = {}
    groups = {}
    exclusions = []
    for assignment in assignments:
        if assignment.state_id is None:
            exclusions.append(assignment)
            continue
        state = assignment.state_id
        counts[state] = counts.get(state, 0) + 1
        if checked_weights is not None:
            bucket = groups.setdefault(state, [])
            bucket.append(checked_weights[assignment.record_key])
    if reason is None:
        unweighted = distribution_from_counts(counts, scope=scope, representation=representation)
        unweighted = replace(unweighted, input_basis="empirical_assignments",
            frequency_metadata=replace(unweighted.frequency_metadata, method="empirical_assignments; n_i/N"),
            count_metadata=replace(unweighted.count_metadata, method="count included record-state assignments"))
    else:
        unweighted = _metrics((), {}, None, scope=scope, representation=representation,
            weighting=WeightingOptions(), basis="empirical_assignments", denominator=None,
            denominator_basis=scope.denominator_basis, reason=reason)
    weighted = None
    if checked_weights is not None:
        if reason is not None:
            weighted = _metrics((), {}, {}, scope=scope, representation=representation, weighting=weighting,
                basis="weighted_record_mass", denominator=None, denominator_basis="included_record_weight_mass", reason=reason)
        else:
            try:
                masses = {state: fsum(groups[state]) for state in sorted(groups)}
                total = fsum(checked_weights[key] for key in sorted(checked_weights))
            except OverflowError:
                raise _invalid("weight sum exceeds the finite numerical range", weight=True) from None
            if not isfinite(total) or total <= 0:
                raise _invalid("selected weighted scope needs positive finite total mass", weight=True)
            frequencies = tuple((state, masses[state] / total) for state in sorted(masses))
            if any(masses[state] > 0 and value == 0 for state, value in frequencies):
                raise _invalid("positive state mass underflows its frequency; no state is silently removed", weight=True)
            weighted = _metrics(frequencies, counts, masses, scope=scope, representation=representation,
                weighting=weighting, basis="weighted_record_mass", denominator=total,
                denominator_basis="included_record_weight_mass")
    return StateDistributionResult(unweighted, weighted,
        ValidationCoverage(len(scope.included_record_keys), len(assignments), "selected_valid_records"),
        represented.selection.selection_basis, tuple(represented.selection.messages), tuple(exclusions))
