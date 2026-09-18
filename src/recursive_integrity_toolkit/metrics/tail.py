"""Select an explicit observed tail and compute a separate one-step scenario.

Owner IDs:
    T2: Definitions 10.1-10.8, F-014; Phase 3 P3-D06/P3-D07.
    PR-016: deterministic frequency/count/Unicode ordering only.

Inputs:
    Unweighted count-backed Step 4 DistributionMetrics and TailSelectionOptions;
    or a supplied state frequency, positive resample size, scope and representation.

Outputs:
    Immutable tail membership, tail support size, tail record share and ordinal
    rarity ranking; separately requested analytic one-step extinction probability.

Assumptions:
    Tail selection is relative to declared representation and positive observed
    support. F-014 assumes a finite closed categorical multinomial resample.

Limits:
    No implicit rule, weighted tail, quantile, absent-state imputation, risk signal,
    random sampling, reopening, lineage, pair comparison, report or file/network I/O.
    A scenario probability is not a calibrated production-failure probability.

Current phase status:
    Phase 3 Step 7 only. Explicit in-memory calls; import-safe; no RNG.
"""
from __future__ import annotations

from dataclasses import dataclass, field, replace
from math import exp, isfinite, log1p

from ..errors import CanonicalValidationError, ErrorCode
from ..models import (
    CalculationEvidenceClass, CalculationMetadata, CalculationReason,
    CalculationScope, CalculationStatus, NumericalPolicy, RepresentationDescriptor,
    ScalarCalculation, TailSelectionOptions, WeightingOptions,
)
from .diversity import DistributionMetrics, StateFrequency, _context


@dataclass(frozen=True, slots=True)
class RarityEntry:
    """An ordinal, not a universal risk score; exact ties use Unicode state ID."""

    state_id: str = field(repr=False)
    state_count: int
    state_frequency: float
    rarity_rank: int
    in_tail: bool


@dataclass(frozen=True, slots=True)
class TailSelectionResult:
    """Derived tail diagnostics bound to one count-backed representation."""

    scope: CalculationScope
    representation: RepresentationDescriptor
    options: TailSelectionOptions
    input_basis: str
    status: CalculationStatus
    reason_codes: tuple[CalculationReason, ...]
    denominator: int | None
    denominator_basis: str
    tail_membership: tuple[str, ...] = field(repr=False)
    rarity_ranking: tuple[RarityEntry, ...] = field(repr=False)
    tail_support_size: ScalarCalculation
    tail_record_share: ScalarCalculation
    ranking_metadata: CalculationMetadata
    membership_metadata: CalculationMetadata
    count_metadata: CalculationMetadata
    frequency_metadata: CalculationMetadata
    ranking_rule: str = "ascending_frequency_then_count_then_unicode_state_id"
    limitations: tuple[str, ...] = (
        "Tail membership depends on the explicit rule and declared representation.",
        "Count-backed unweighted records only; probability-only vectors do not supply record shares.",
        "Declared zero-count states are outside observed support and are not ranked.",
        "Rarity does not establish importance, harm, production failure or permanent extinction.",
    )


@dataclass(frozen=True, slots=True)
class ExtinctionProbabilityResult:
    """Analytic F-014 conditional scenario, with no random realization."""

    state_id: str = field(repr=False)
    state_frequency: float
    resample_size: int
    one_step_extinction_probability: ScalarCalculation
    numerical_underflow: bool
    scope: CalculationScope
    representation: RepresentationDescriptor
    method: str = "analytic_extinction"
    model_name: str = "closed_resampling"
    simulation_horizon: int = 1
    experimental: bool = True
    evidence_class: CalculationEvidenceClass = CalculationEvidenceClass.SIMULATION
    random_seed: None = None
    input_basis: str = "supplied_selected_state_marginal"
    evaluation_method: str = "exp(resample_size * log1p(-state_frequency)); exact endpoints"
    numerical_policy: NumericalPolicy = NumericalPolicy()
    limitations: tuple[str, ...] = (
        "Conditional on the supplied current frequency and the closed multinomial model.",
        "The input is a selected-state marginal; no complete empirical distribution is inferred.",
        "A zero-frequency boundary case describes continued absence, not a newly observed loss.",
        "Underflow is disclosed; a rounded zero for an interior frequency is not impossibility.",
        "One step only; no training-epoch countdown or calibrated production-failure forecast.",
    )


def _invalid(message: str) -> CanonicalValidationError:
    return CanonicalValidationError(ErrorCode.SCHEMA_TYPE, message, field="tail")


def _state(value: object) -> str:
    if type(value) is not str or "\x00" in value:
        raise _invalid("state identity must be literal text")
    try:
        value.encode("utf-8")
    except UnicodeEncodeError:
        raise _invalid("state identity must be valid UTF-8") from None
    return value


def _options(options: object) -> TailSelectionOptions:
    if type(options) is not TailSelectionOptions or type(options.rule) is not str:
        raise _invalid("tail selection requires explicit TailSelectionOptions")
    if type(options.state_ids) is not tuple:
        raise _invalid("tail state list must be an immutable literal tuple")
    for state in options.state_ids:
        _state(state)
    try:
        return replace(options, state_ids=tuple(sorted(options.state_ids)))
    except (ValueError, TypeError):
        raise _invalid("unsupported or invalid explicit tail rule") from None


def _metadata(name: str, unit: str, scope: CalculationScope,
              representation: RepresentationDescriptor, method: str, *, scenario: bool = False
              ) -> CalculationMetadata:
    return CalculationMetadata(
        name, "T2", "F-014" if scenario else None,
        CalculationEvidenceClass.SIMULATION if scenario else CalculationEvidenceClass.DERIVED_METRIC,
        unit, method, scope, representation, WeightingOptions(),
        assumptions=(
            ("Categorical multinomial sampling; positive explicit n; one-step horizon; no external reopening."
             if scenario else "Explicit rule over positive observed unweighted count support."),
        ),
        limitations=("Representation-bound; no calibrated production-failure or universal risk conclusion.",),
    )


def _distribution(value: object) -> tuple[CalculationScope, RepresentationDescriptor, tuple[StateFrequency, ...]]:
    """Revalidate only the consumed count/frequency basis, without recomputing diversity."""
    if type(value) is not DistributionMetrics:
        raise _invalid("tail selection requires a count-backed DistributionMetrics result")
    scope, representation = _context(value.scope, value.representation)
    if (type(value.weighting) is not WeightingOptions
            or type(value.weighting.weighting_mode) is not str
            or value.weighting.weighting_mode != "unweighted" or value.weighting.weight_field is not None):
        raise _invalid("weighted tail selection is not implemented")
    if (type(value.input_basis) is not str or value.input_basis not in
            ("empirical_assignments", "explicit_counts_divided_by_included_records")):
        raise _invalid("record-based tails require counts; probability-only vectors are unsupported")
    total = len(scope.included_record_keys)
    if (type(value.analyzed_record_count) is not int or value.analyzed_record_count != total
            or type(value.denominator_basis) is not str or value.denominator_basis != scope.denominator_basis
            or type(value.status) is not CalculationStatus or type(value.reason_codes) is not tuple
            or type(value.states) is not tuple or type(value.support) is not tuple):
        raise _invalid("distribution status or denominator does not match its record scope")
    for state in value.support:
        _state(state)
    if type(value.numerical_policy) is not NumericalPolicy:
        raise _invalid("distribution requires its approved numerical policy")
    try:
        replace(value.numerical_policy)
    except (ValueError, TypeError):
        raise _invalid("distribution numerical policy differs from the approved policy") from None
    for metadata, name, formula, evidence, unit in (
        (value.count_metadata, "state_count", None, CalculationEvidenceClass.OBSERVED_FACT, "records"),
        (value.frequency_metadata, "state_frequency", "F-001", CalculationEvidenceClass.DERIVED_METRIC, "ratio"),
    ):
        if type(metadata) is not CalculationMetadata:
            raise _invalid("tail input lacks its count or frequency trace metadata")
        try:
            checked = replace(metadata)
        except (ValueError, TypeError):
            raise _invalid("tail input trace metadata is malformed") from None
        if (checked.scope != value.scope or checked.representation != value.representation
                or checked.weighting != WeightingOptions() or checked.owner_id != "T1"
                or checked.metric_name != name or checked.formula_id != formula
                or checked.evidence_class is not evidence or checked.unit != unit):
            raise _invalid("count or frequency trace metadata does not match its distribution")
    if total == 0:
        reason = CalculationReason.ALL_EXCLUDED if scope.excluded_record_keys else CalculationReason.EMPTY_SCOPE
        if (value.status is not CalculationStatus.UNAVAILABLE or value.reason_codes != (reason,)
                or value.states or value.support or value.frequency_denominator is not None):
            raise _invalid("empty or excluded scope requires an unavailable distribution")
        return scope, representation, ()
    if (value.status is not CalculationStatus.AVAILABLE or value.reason_codes
            or type(value.frequency_denominator) is not int or value.frequency_denominator != total):
        raise _invalid("nonempty tail input needs an available exact record denominator")
    seen = set()
    states = []
    for row in value.states:
        if type(row) is not StateFrequency:
            raise _invalid("frequency table requires typed state entries")
        state = _state(row.state_id)
        if state in seen or type(row.state_count) is not int or row.state_count < 0 or row.state_count > total:
            raise _invalid("state counts must be unique, nonnegative and within the record total")
        if (type(row.state_frequency) is not float or not isfinite(row.state_frequency)
                or row.state_frequency != row.state_count / total or row.state_mass is not None):
            raise _invalid("state frequency does not match its unweighted count denominator")
        seen.add(state)
        states.append(StateFrequency(state, row.state_count, None, row.state_frequency))
    if sum(row.state_count for row in states) != total:
        raise _invalid("state counts do not reconcile to the record scope")
    positive = tuple(sorted(row.state_id for row in states if row.state_count > 0))
    if tuple(sorted(value.support)) != positive:
        raise _invalid("declared support differs from positive-count support")
    return scope, representation, tuple(states)


def _rarity_key(row: StateFrequency) -> tuple[float, int, str]:
    return row.state_frequency, row.state_count, row.state_id


def select_tail(distribution: DistributionMetrics, *, options: TailSelectionOptions) -> TailSelectionResult:
    """Select and rank positive observed states; no implicit scenario calculation.

    singleton_count uses count == 1; count_at_or_below and frequency_at_or_below
    include their exact thresholds. state_list must name present positive states.
    Membership is in Unicode order; ranking is frequency/count/Unicode order.
    Empty support due to no usable records is unavailable. A valid empty tail is zero.
    """
    options = _options(options)
    scope, representation, states = _distribution(distribution)
    ranked = sorted((row for row in states if row.state_count > 0), key=_rarity_key)
    support = {row.state_id for row in ranked}
    if options.rule == "state_list" and set(options.state_ids) - support:
        raise _invalid("tail state list contains an absent or zero-count state")
    selected = set()
    for row in ranked:
        if ((options.rule == "singleton_count" and row.state_count == 1)
                or (options.rule == "count_at_or_below" and row.state_count <= options.count_threshold)
                or (options.rule == "frequency_at_or_below" and row.state_frequency <= options.frequency_threshold)
                or (options.rule == "state_list" and row.state_id in options.state_ids)):
            selected.add(row.state_id)
    total = len(scope.included_record_keys)
    status, reasons = distribution.status, distribution.reason_codes
    count = len(selected) if total else None
    share = sum(row.state_count for row in ranked if row.state_id in selected) / total if total else None
    method = "Definitions 10.1-10.6; explicit " + options.rule
    return TailSelectionResult(
        scope, representation, options, distribution.input_basis, status, reasons,
        total if total else None, scope.denominator_basis, tuple(sorted(selected)),
        tuple(RarityEntry(row.state_id, row.state_count, row.state_frequency, i,
                          row.state_id in selected) for i, row in enumerate(ranked, 1)),
        ScalarCalculation(_metadata("tail_support_size", "states", scope, representation, method), status, count, reasons),
        ScalarCalculation(_metadata("tail_record_share", "ratio", scope, representation,
                                     method + "; selected counts / included records"), status, share, reasons),
        _metadata("rarity_rank", "ordinal_rank", scope, representation,
                  "ascending frequency, then count, then Unicode state ID; 1-based ordinal"),
        _metadata("tail_membership", "set_of_states", scope, representation, method),
        replace(distribution.count_metadata, scope=scope, representation=representation),
        replace(distribution.frequency_metadata, scope=scope, representation=representation),
    )


def one_step_extinction_probability(
    state_frequency: float, *, resample_size: int, state_id: str,
    scope: CalculationScope, representation: RepresentationDescriptor,
) -> ExtinctionProbabilityResult:
    """Evaluate F-014 analytically; no random draw, inferred size or implicit seed.

    p=0 and p=1 are exact boundaries. log1p avoids cancellation for tiny positive p.
    Resample sizes outside finite numerical evaluation fail rather than truncate.
    Interior numerical underflow is disclosed, never interpreted as impossibility.
    """
    state = _state(state_id)
    scope, representation = _context(scope, representation)
    if not scope.included_record_keys:
        raise _invalid("analytic scenario requires a nonempty explicit scope")
    if type(state_frequency) not in (int, float):
        raise _invalid("scenario frequency must be a finite built-in number in the unit interval")
    if not 0 <= state_frequency <= 1 or not isfinite(state_frequency):
        raise _invalid("scenario frequency must lie in the unit interval")
    if type(resample_size) is not int or resample_size <= 0:
        raise _invalid("resample_size must be an explicit positive integer, not a weight or boolean")
    try:
        finite_size = isfinite(resample_size)
    except OverflowError:
        finite_size = False
    if not finite_size:
        raise _invalid("resample_size exceeds the finite numerical evaluation range")
    p = float(state_frequency)
    if p == 0:
        probability = 1.0
    elif p == 1:
        probability = 0.0
    else:
        probability = exp(resample_size * log1p(-p))
    scalar = ScalarCalculation(
        _metadata("one_step_extinction_probability", "probability", scope, representation,
                  "F-014; (1-p_i)^n; analytic one-step closed multinomial", scenario=True),
        CalculationStatus.AVAILABLE, probability,
    )
    return ExtinctionProbabilityResult(state, p, resample_size, scalar,
                                       0 < p < 1 and probability == 0.0, scope, representation)
