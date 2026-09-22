"""Compute single-scope frequencies, positive support and named diversity.

Owner IDs:
    T1: F-001, F-002, F-003, F-004, F-005, F-006, F-018. PR-016 deterministic ordering.
    PR-007, PR-011: explicit pair chronology and representation compatibility.
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
    No I/O, inference, randomness, automatic pair selection, tail, source-share, closure,
    lineage, Shannon entropy, functional-failure verdict, report or orchestration.
    A structurally valid supplied assignment does not certify its empirical origin.

Current phase status:
    Phase 3 Step 4 F-001 through F-004 preserved; Phase 3 Step 9 explicit F-005/F-006/F-018 pair kernels.
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


# Phase 3 Step 9: pure pairwise mathematics. All earlier single-scope definitions
# above are retained unchanged. No version discovery or longitudinal dispatcher.
from ..models import ExplicitPairContext
from ..representations.compatibility import (
    RepresentationCompatibility, StateMappingDeclaration, validate_representation_compatibility,
)


@dataclass(frozen=True, slots=True)
class SupportComparison:
    """F-005/F-006/F-018 over one explicit pair in a declared common basis.

    Original and harmonized distributions are separately visible. Mapping
    coarsening is never described as observed recovery of an original state.
    None in a state set means comparison unavailable, not a measured empty set.
    """

    compatibility: RepresentationCompatibility
    original_earlier: DistributionMetrics = field(repr=False)
    original_later: DistributionMetrics = field(repr=False)
    harmonized_earlier: DistributionMetrics = field(repr=False)
    harmonized_later: DistributionMetrics = field(repr=False)
    status: CalculationStatus
    reason_codes: tuple[CalculationReason, ...]
    support_delta: ScalarCalculation
    support_loss_count: ScalarCalculation
    support_added_count: ScalarCalculation
    support_retention_ratio: ScalarCalculation
    gini_simpson_diversity_delta: ScalarCalculation
    extinct_states: tuple[str, ...] | None = field(repr=False)
    added_states: tuple[str, ...] | None = field(repr=False)
    retained_states: tuple[str, ...] | None = field(repr=False)
    retention_denominator: int | None
    retention_denominator_basis: str
    set_metadata: tuple[CalculationMetadata, ...]
    mapping_effect: tuple[tuple[str, int | None, int | None], ...]
    limitations: tuple[str, ...] = (
        "One explicitly selected earlier/later pair only; no trajectory or automatic adjacent comparison.",
        "Extinct means absent from the supplied later support in the harmonized representation.",
        "No permanent process extinction, causality, model-performance or source-independence claim follows.",
        "Supplied probability vectors remain mathematical inputs, not empirical record-frequency observations.",
        "Many-to-one mapping can conceal original distinctions; original inputs remain separately visible.",
        "Weighted support is positive weight mass, not unweighted record presence.",
    )


def _pair_metadata_check(actual: object, expected: CalculationMetadata | None) -> CalculationMetadata | None:
    """Validate trace identities for consumed numerical fields without object hooks."""
    if expected is None:
        if actual is not None:
            raise _invalid("pair input contains incompatible count or mass trace metadata")
        return
    if type(actual) is not CalculationMetadata:
        raise _invalid("pair input lacks typed numerical trace metadata")
    scope, representation = _context(actual.scope, actual.representation)
    if type(actual.weighting) is not WeightingOptions:
        raise _invalid("pair input metadata has invalid weighting")
    try:
        weighting = replace(actual.weighting)
    except (ValueError, TypeError):
        raise _invalid("pair metadata weighting failed validation") from None
    for text in (actual.metric_name, actual.owner_id, actual.unit, actual.method):
        _text(text)
    if actual.formula_id is not None:
        _text(actual.formula_id)
    for values in (actual.assumptions, actual.limitations):
        if type(values) is not tuple:
            raise _invalid("pair trace assumptions and limits must be literal tuples")
        for text in values:
            _text(text)
    if (actual.metric_name != expected.metric_name or actual.owner_id != expected.owner_id
            or actual.formula_id != expected.formula_id or actual.unit != expected.unit
            or actual.evidence_class is not expected.evidence_class
            or scope != expected.scope or representation != expected.representation or weighting != expected.weighting):
        raise _invalid("pair input numerical trace disagrees with its distribution basis")
    return replace(actual, scope=scope, representation=representation, weighting=weighting)


def _pair_scalar_check(actual: object, expected: ScalarCalculation) -> ScalarCalculation:
    if type(actual) is not ScalarCalculation or actual.status is not expected.status:
        raise _invalid("pair input scalar status disagrees with its distribution")
    if type(actual.reason_codes) is not tuple or any(type(code) is not CalculationReason for code in actual.reason_codes):
        raise _invalid("pair scalar reasons must use the approved registry")
    if actual.reason_codes != expected.reason_codes:
        raise _invalid("pair scalar unavailable reasons disagree with the record scope")
    if type(actual.value) is not type(expected.value) or actual.value != expected.value:
        raise _invalid("pair input scalar differs from its recomputed count or mass basis")
    metadata = _pair_metadata_check(actual.metadata, expected.metadata)
    return replace(actual, metadata=metadata)


def _pair_distribution(value: object) -> DistributionMetrics:
    """Revalidate raw table evidence and every consumed summary; never trust a flag."""
    if type(value) is not DistributionMetrics:
        raise _invalid("pair comparison requires typed DistributionMetrics inputs")
    scope, representation = _context(value.scope, value.representation)
    if type(value.weighting) is not WeightingOptions:
        raise _invalid("pair weighting requires its explicit declaration contract")
    try:
        weighting = replace(value.weighting)
    except (ValueError, TypeError):
        raise _invalid("invalid pair weighting declaration") from None
    bases = ("empirical_assignments", "explicit_counts_divided_by_included_records",
             "explicit_probability_vector", "weighted_record_mass")
    if type(value.input_basis) is not str or value.input_basis not in bases:
        raise _invalid("pair distribution has no approved input basis")
    weighted = value.input_basis == "weighted_record_mass"
    supplied = value.input_basis == "explicit_probability_vector"
    if weighted != (weighting.weighting_mode == "weighted"):
        raise _invalid("pair input basis and weighting disagree")
    total = len(scope.included_record_keys)
    if (type(value.analyzed_record_count) is not int or value.analyzed_record_count != total
            or type(value.states) is not tuple or type(value.support) is not tuple
            or type(value.reason_codes) is not tuple or type(value.status) is not CalculationStatus
            or type(value.numerical_policy) is not NumericalPolicy):
        raise _invalid("pair input summary is structurally invalid")
    try:
        replace(value.numerical_policy)
    except (ValueError, TypeError):
        raise _invalid("pair input numerical policy differs from the approved policy") from None
    for reason in value.reason_codes:
        if type(reason) is not CalculationReason:
            raise _invalid("pair input uses an unregistered reason")
    support = tuple(_text(state, empty=True) for state in value.support)
    if len(set(support)) != len(support):
        raise _invalid("pair input support contains duplicates")
    counts, masses, frequencies = (None if supplied else {}), ({} if weighted else None), {}
    for row in value.states:
        if type(row) is not StateFrequency:
            raise _invalid("pair input state table requires typed rows")
        state = _text(row.state_id, empty=True)
        if state in frequencies:
            raise _invalid("pair input state table contains duplicates")
        p = _number(row.state_frequency)
        if p > 1:
            raise _invalid("pair input frequency exceeds one")
        frequencies[state] = p
        if supplied:
            if row.state_count is not None or row.state_mass is not None:
                raise _invalid("probability-only input cannot claim record counts or weight mass")
        else:
            if type(row.state_count) is not int or not 0 <= row.state_count <= total:
                raise _invalid("pair state count must be an integer within the selected scope")
            counts[state] = row.state_count
            if weighted:
                masses[state] = _number(row.state_mass, weight=True)
                if row.state_count == 0 and row.state_mass != 0:
                    raise _invalid("zero records cannot carry positive state weight mass")
            elif row.state_mass is not None:
                raise _invalid("unweighted pair input cannot contain state weight mass")
    reason = None
    if total == 0:
        if supplied or value.states:
            raise _invalid("empty record scope cannot certify a supplied distribution")
        reason = CalculationReason.ALL_EXCLUDED if scope.excluded_record_keys else CalculationReason.EMPTY_SCOPE
        denominator = None
    elif supplied:
        denominator = None
    elif weighted:
        denominator = _number(value.frequency_denominator, weight=True)
        if denominator <= 0:
            raise _invalid("weighted pair requires positive total weight", weight=True)
        try:
            mass_total = fsum(masses.values())
        except OverflowError:
            raise _invalid("pair weight mass exceeds the finite range", weight=True) from None
        if abs(mass_total - denominator) > NumericalPolicy().probability_mass_tolerance * max(1.0, denominator):
            raise _invalid("pair state masses do not reconcile to declared total weight", weight=True)
    else:
        denominator = total
    expected_basis = "included_record_weight_mass" if weighted else "explicit_probability_mass" if supplied else scope.denominator_basis
    if (type(value.denominator_basis) is not str or value.denominator_basis != expected_basis
            or type(value.frequency_denominator) is not type(denominator) or value.frequency_denominator != denominator):
        raise _invalid("pair denominator disagrees with its explicit input basis")
    if counts is not None and sum(counts.values()) != total:
        raise _invalid("pair state counts do not sum to the included record count")
    if reason is None and not supplied:
        for state, p in frequencies.items():
            numerator = masses[state] if weighted else counts[state]
            if p != numerator / denominator or (numerator > 0 and p == 0):
                raise _invalid("pair frequency disagrees with its count or weight denominator")
    rebuilt = _metrics(tuple(sorted(frequencies.items())), counts, masses,
        scope=scope, representation=representation, weighting=weighting, basis=value.input_basis,
        denominator=denominator, denominator_basis=expected_basis, reason=reason)
    if value.status is not rebuilt.status or value.reason_codes != rebuilt.reason_codes or tuple(sorted(support)) != rebuilt.support:
        raise _invalid("pair input availability or support disagrees with revalidated evidence")
    for actual, expected in ((value.supplied_probability_total, rebuilt.supplied_probability_total),
                             (value.probability_residual, rebuilt.probability_residual)):
        if type(actual) is not type(expected) or actual != expected:
            raise _invalid("pair probability total or residual disagrees with the state table")
    scalars = tuple(_pair_scalar_check(actual, expected) for actual, expected in (
        (value.support_size, rebuilt.support_size),
        (value.gini_simpson_diversity, rebuilt.gini_simpson_diversity),
        (value.simpson_concentration, rebuilt.simpson_concentration)))
    metadata = tuple(_pair_metadata_check(actual, expected) for actual, expected in (
        (value.frequency_metadata, rebuilt.frequency_metadata),
        (value.count_metadata, rebuilt.count_metadata), (value.mass_metadata, rebuilt.mass_metadata)))
    if type(value.limitations) is not tuple:
        raise _invalid("pair input limitations must be a literal tuple")
    for limitation in value.limitations:
        _text(limitation)
    return replace(rebuilt, support_size=scalars[0], gini_simpson_diversity=scalars[1],
                   simpson_concentration=scalars[2], frequency_metadata=metadata[0],
                   count_metadata=metadata[1], mass_metadata=metadata[2], limitations=value.limitations)


def _harmonize_distribution(value: DistributionMetrics, declaration: StateMappingDeclaration) -> DistributionMetrics:
    """Aggregate only explicitly mapped existing states; never add missing data."""
    mapping = declaration.state_mapping
    if any(row.state_id not in mapping for row in value.states):
        raise _invalid("directed state map does not cover every supplied source-state entry")
    count_backed = value.count_metadata is not None
    weighted = value.weighting.weighting_mode == "weighted"
    groups = {}
    for row in value.states:
        groups.setdefault(mapping[row.state_id], []).append(row)
    counts = {state: sum(row.state_count for row in rows) for state, rows in groups.items()} if count_backed else None
    masses = {state: fsum(row.state_mass for row in rows) for state, rows in groups.items()} if weighted else None
    if value.status is CalculationStatus.UNAVAILABLE:
        pairs = ()
    elif weighted:
        pairs = tuple((state, masses[state] / value.frequency_denominator) for state in sorted(groups))
    elif count_backed:
        pairs = tuple((state, counts[state] / value.frequency_denominator) for state in sorted(groups))
    else:
        pairs = tuple((state, fsum(row.state_frequency for row in groups[state])) for state in sorted(groups))
    harmonized = _metrics(pairs, counts, masses, scope=value.scope,
        representation=declaration.target_representation, weighting=value.weighting, basis=value.input_basis,
        denominator=value.frequency_denominator, denominator_basis=value.denominator_basis,
        reason=value.reason_codes[0] if value.status is CalculationStatus.UNAVAILABLE else None)
    return replace(harmonized, limitations=value.limitations + (
        "Explicit directed state aggregation changes this basis; inspect original distributions separately.",))


def _pair_metadata(name: str, formula: str | None, unit: str, compatibility: RepresentationCompatibility,
                   weighting: WeightingOptions, method: str) -> CalculationMetadata:
    a, b = compatibility.context.earlier_scope, compatibility.context.later_scope
    scope = CalculationScope(a.dataset_versions + b.dataset_versions,
        a.included_record_keys + b.included_record_keys, a.excluded_record_keys + b.excluded_record_keys,
        "separate_ordered_representation_scopes", a.scope_id + " -> " + b.scope_id)
    return CalculationMetadata(name, "T1", formula, CalculationEvidenceClass.DERIVED_METRIC,
        unit, method, scope, compatibility.harmonized_representation, weighting,
        assumptions=("Earlier and later scopes explicitly selected and independently validated.",
                     "State identity uses the declared common basis, including any disclosed map.",),
        limitations=("Observed/supplied support only; no permanent extinction or causal/model-performance verdict.",
                     "A coarsened comparison cannot recover distinctions lost through its mapping.",))


def compare_support(
    earlier: DistributionMetrics, later: DistributionMetrics, *, context: ExplicitPairContext,
    earlier_state_semantics: str, later_state_semantics: str,
    state_mapping: StateMappingDeclaration | None = None,
) -> SupportComparison:
    """Compare exactly two explicit inputs: F-005/F-006/F-018 and state sets.

    Both sides must use the same weighting and compatible denominator families.
    Count-backed inputs and supplied probability-only inputs are not mixed. All
    consumed summaries are revalidated. A failed side yields unavailable pair
    values, preserving the individually valid side. No automatic bundle dispatch.
    """
    compatibility = validate_representation_compatibility(context,
        earlier_state_semantics=earlier_state_semantics, later_state_semantics=later_state_semantics,
        state_mapping=state_mapping)
    a, b = _pair_distribution(earlier), _pair_distribution(later)
    context = compatibility.context
    if (a.scope != context.earlier_scope or b.scope != context.later_scope
            or a.representation != context.earlier_representation or b.representation != context.later_representation):
        raise _invalid("comparison distributions do not match their explicit pair context")
    if (a.weighting != b.weighting or a.denominator_basis != b.denominator_basis
            or (a.input_basis == "explicit_probability_vector") != (b.input_basis == "explicit_probability_vector")):
        raise _invalid("comparison requires compatible weighting and denominator families")
    original_a, original_b = a, b
    if compatibility.mapping is not None:
        if compatibility.mapping.direction == "earlier_to_later":
            a = _harmonize_distribution(a, compatibility.mapping)
        else:
            b = _harmonize_distribution(b, compatibility.mapping)
    reasons = tuple(sorted(set(a.reason_codes + b.reason_codes), key=str))
    available = a.status is CalculationStatus.AVAILABLE and b.status is CalculationStatus.AVAILABLE
    status = CalculationStatus.AVAILABLE if available else CalculationStatus.UNAVAILABLE
    left, right = set(a.support), set(b.support)
    lost = tuple(sorted(left - right)) if available else None
    added = tuple(sorted(right - left)) if available else None
    retained = tuple(sorted(left & right)) if available else None
    values = (
        len(right) - len(left), len(left - right), len(right - left),
        len(left & right) / len(left) if left else None,
        b.gini_simpson_diversity.value - a.gini_simpson_diversity.value if available else None,
    )
    descriptions = (
        ("support_delta", "F-005", "states", "later support_size minus earlier support_size"),
        ("support_loss_count", None, "states", "cardinality of earlier support minus later support"),
        ("support_added_count", None, "states", "cardinality of later support minus earlier support"),
        ("support_retention_ratio", "F-006", "ratio", "intersection support size / earlier positive-mass support size"),
        ("gini_simpson_diversity_delta", "F-018", "dimensionless", "later Gini-Simpson diversity minus earlier diversity"),
    )
    scalars = tuple(ScalarCalculation(_pair_metadata(name, formula, unit, compatibility, a.weighting, method),
                                     status, value if available else None, reasons)
                    for value, (name, formula, unit, method) in zip(values, descriptions))
    sets = tuple(_pair_metadata(name, None, "set_of_states", compatibility, a.weighting, method)
                 for name, method in (("extinct_states", "earlier support minus later support"),
                                      ("added_states", "later support minus earlier support"),
                                      ("retained_states", "earlier support intersect later support")))
    effects = (("earlier", original_a.support_size.value, a.support_size.value),
               ("later", original_b.support_size.value, b.support_size.value))
    return SupportComparison(compatibility, original_a, original_b, a, b, status, reasons,
        *scalars, lost, added, retained, len(left) if available else None,
        "earlier_positive_mass_support_in_harmonized_representation", sets, effects)
