"""Explicit finite closed resampling and its F-015 expectation.

Owner IDs:
    T1: finite multinomial transition and F-015, Definitions 12.1-12.5.
    PR-016: P3-D07 explicit PCG64 seed, canonical order and bounded numerics.
    T2: one-step extinction remains in tail.py; no duplicate implementation.
    T5: reserved; external-reference loss and reopening remain unimplemented.

Inputs:
    Explicit state/probability pairs, representation, scope, positive resample
    size and nonnegative horizon. Sampled paths also require seed and replicates.

Outputs:
    Immutable analytic expectations OR distinguishable sampled paths; simulation
    evidence throughout, with parameters, method, correction and limits retained.

Assumptions:
    Finite fixed state space; each generation is a multinomial resample of its
    predecessor. No mutation, migration, independent data or external correction.

Limits:
    No I/O, global RNG, implicit parameters, reopening, external loss, graph,
    report or automatic dispatch. Expected contraction does not require every
    realized diversity path to decrease. Simulation time is not a training epoch.

Current phase status:
    Phase 3 Step 8 only. NumPy is lazy and used only for explicitly sampled paths.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from math import exp, fsum, isfinite, log1p
from types import MappingProxyType

from ..errors import CanonicalValidationError, ErrorCode
from ..models import (
    CalculationEvidenceClass, CalculationMetadata, CalculationScope,
    NumericalPolicy, RepresentationDescriptor, WeightingOptions,
)
from .diversity import _context

# Engineering work limits, not theoretical limits or scenario defaults.
MAX_STATES = 4096
MAX_STEPS = 10000
MAX_REPLICATES = 10000
MAX_PATH_CELLS = 1000000
MAX_RESAMPLE_SIZE = 2147483647
MAX_SEED_BITS = 4096
METHOD_VERSION = "closed_categorical_v1"
SAMPLER_ALGORITHM = "sequential_binomial_complement_v1"
ASSUMPTIONS = (
    "Fixed finite declared state space and constant positive integer resample size.",
    "X_t conditional on p_t is Multinomial(n,p_t); p_(t+1)=X_t/n.",
    "No mutation, migration, independent real data or external corrective input.",
)
LIMITATIONS = (
    "Experimental conditional simulation; no calibrated production-failure probability.",
    "Diversity contraction holds in expectation, not monotonically on every sampled path.",
    "Simulated steps are not record generations, training epochs or dataset releases.",
    "No external-reference loss, reopening, lineage, risk score or audit workflow is implemented.",
    "Floating-point and pseudorandom sampling are numerical realizations of the declared model.",
)


@dataclass(frozen=True, slots=True)
class ResamplingInput:
    """Supplied and effective probability vectors in canonical Unicode order."""

    scope: CalculationScope
    representation: RepresentationDescriptor
    supplied_distribution: tuple[tuple[str, float], ...] = field(repr=False)
    effective_distribution: tuple[tuple[str, float], ...] = field(repr=False)
    supplied_probability_total: float
    effective_probability_total: float
    probability_residual: float
    correction_applied: bool
    correction_method: str
    normalization_divisor: float
    probability_corrections: tuple[tuple[str, float], ...] = field(repr=False)
    numerical_policy: NumericalPolicy = NumericalPolicy()
    input_basis: str = "explicit_supplied_state_probability_vector"


@dataclass(frozen=True, slots=True)
class ExpectedDiversityResult:
    """F-015 t=0..steps, never a random realization or an observed delta."""

    inputs: ResamplingInput = field(repr=False)
    resample_size: int
    simulation_horizon: int
    initial_gini_simpson_diversity: float
    contraction_factor: float
    expected_diversity: tuple[float, ...]
    expected_diversity_metadata: CalculationMetadata
    numerical_underflow_steps: tuple[int, ...]
    method: str = "analytic_expectation"
    method_version: str = METHOD_VERSION
    model_name: str = "closed_resampling"
    experimental: bool = True
    evidence_class: CalculationEvidenceClass = CalculationEvidenceClass.SIMULATION
    random_seed: None = None
    rng_name: None = None
    simulation_replicates: None = None
    assumptions: tuple[str, ...] = ASSUMPTIONS
    limitations: tuple[str, ...] = LIMITATIONS + (
        "Analytic input residuals within the approved tolerance are disclosed and left unchanged.",
    )


@dataclass(frozen=True, slots=True)
class SampledGeneration:
    """Simulation state; initial counts are None rather than invented records."""

    step: int
    state_counts: tuple[int, ...] | None
    state_frequencies: tuple[float, ...]
    support: tuple[str, ...] = field(repr=False)
    support_size: int
    gini_simpson_diversity: float


@dataclass(frozen=True, slots=True)
class ResamplingReplicate:
    replicate_index: int
    generations: tuple[SampledGeneration, ...]


@dataclass(frozen=True, slots=True)
class ResamplingSimulation:
    """One named generator per call; paths use replicate-major step-major order."""

    inputs: ResamplingInput = field(repr=False)
    resample_size: int
    simulation_horizon: int
    simulation_replicates: int
    random_seed: int
    numpy_version: str
    state_order: tuple[str, ...] = field(repr=False)
    sampled_paths: tuple[ResamplingReplicate, ...]
    trajectory_metadata: tuple[CalculationMetadata, ...]
    method: str = "sampled_path"
    method_version: str = METHOD_VERSION
    sampler_algorithm: str = SAMPLER_ALGORITHM
    rng_name: str = "numpy.random.Generator(PCG64)"
    replicate_schedule: str = "replicate_major_step_major"
    state_schedule: str = "ascending_unicode_state_id_skip_zero"
    model_name: str = "closed_resampling"
    experimental: bool = True
    evidence_class: CalculationEvidenceClass = CalculationEvidenceClass.SIMULATION
    assumptions: tuple[str, ...] = ASSUMPTIONS
    limitations: tuple[str, ...] = LIMITATIONS + (
        "Replay requires the same method, NumPy build/environment, seed and parameters.",
        "Bit-identical paths across dependency versions or platforms are not promised.",
        "Accepted input round-off is corrected only by division by its validated total.",
    )


def _invalid(message: str, *, resource: bool = False) -> CanonicalValidationError:
    return CanonicalValidationError(ErrorCode.CONFIG_INVALID if resource else ErrorCode.SCHEMA_TYPE,
                                    message, field="closed_resampling")


def _integer(value: object, *, positive: bool = False) -> int:
    if type(value) is not int or value < 0 or (positive and value == 0):
        raise _invalid("scenario parameters require explicit integers in their declared range")
    return value


def _resources(n: object, steps: object, states: int, replicates: object = 1) -> None:
    _integer(n, positive=True)
    _integer(steps)
    _integer(replicates, positive=True)
    if (n > MAX_RESAMPLE_SIZE or steps > MAX_STEPS or states > MAX_STATES
            or replicates > MAX_REPLICATES or states * (steps + 1) * replicates > MAX_PATH_CELLS):
        raise _invalid("closed scenario exceeds the documented bounded work or memory limits", resource=True)


def _state(value: object) -> str:
    if type(value) is not str or "\x00" in value:
        raise _invalid("scenario state IDs must be literal text")
    try:
        value.encode("utf-8")
    except UnicodeEncodeError:
        raise _invalid("scenario state IDs must be valid UTF-8") from None
    return value


def _inputs(value: object, scope: CalculationScope, representation: RepresentationDescriptor,
            *, sampled: bool) -> ResamplingInput:
    scope, representation = _context(scope, representation)
    if type(value) not in (dict, MappingProxyType, tuple) or not value:
        raise _invalid("scenario requires a nonempty explicit state/probability mapping or tuple")
    if len(value) > MAX_STATES:
        raise _invalid("scenario state count exceeds the documented limit", resource=True)
    pairs = tuple(value.items()) if type(value) in (dict, MappingProxyType) else value
    checked = {}
    for pair in pairs:
        if type(pair) is not tuple or len(pair) != 2:
            raise _invalid("scenario distribution entries must be state/probability pairs")
        state, probability = pair
        state = _state(state)
        if state in checked:
            raise _invalid("scenario state IDs must be unique")
        if type(probability) not in (int, float):
            raise _invalid("scenario probabilities must be finite built-in numbers")
        try:
            valid = isfinite(probability) and 0 <= probability <= 1
        except OverflowError:
            valid = False
        if not valid:
            raise _invalid("scenario probabilities must be finite and in the unit interval")
        checked[state] = float(probability)
    supplied = tuple(sorted(checked.items()))
    total = fsum(p for _, p in supplied)
    tolerance = NumericalPolicy().probability_mass_tolerance
    if total <= 0 or abs(total - 1.0) > tolerance:
        raise _invalid("scenario probability mass must equal one within the approved absolute tolerance")
    corrected = sampled and total != 1.0
    effective = tuple((s, p / total) for s, p in supplied) if corrected else supplied
    if any(p > 0 and effective[i][1] == 0 for i, (_, p) in enumerate(supplied)):
        raise _invalid("probability correction would remove positive support")
    changes = tuple((s, effective[i][1] - p) for i, (s, p) in enumerate(supplied))
    if any(abs(delta) > tolerance for _, delta in changes):
        raise _invalid("probability correction exceeds the approved bound")
    return ResamplingInput(scope, representation, supplied, effective, total,
                           fsum(p for _, p in effective), total - 1.0, corrected,
                           "divide_by_validated_total" if corrected else "none",
                           total if corrected else 1.0, changes)


def _metadata(name: str, formula: str | None, unit: str, inputs: ResamplingInput,
              method: str) -> CalculationMetadata:
    return CalculationMetadata(name, "T1", formula, CalculationEvidenceClass.SIMULATION,
        unit, method, inputs.scope, inputs.representation, WeightingOptions(), ASSUMPTIONS, LIMITATIONS)


def _diversity(probabilities: tuple[float, ...]) -> float:
    value = 1.0 - fsum(p * p for p in probabilities)
    if not 0.0 <= value < 1.0:
        raise _invalid("scenario diversity exceeds its numerical domain; no clipping is performed")
    return value


def expected_diversity_after_steps(
    initial_distribution: object, *, resample_size: int, steps: int,
    scope: CalculationScope, representation: RepresentationDescriptor,
) -> ExpectedDiversityResult:
    """F-015 and its fixed-n iteration, with the full supplied basis retained.

    This deterministic analytic function never imports NumPy or creates a seed.
    There is no probability repair in this branch. Positive expectations rounded
    to zero are disclosed as numerical underflow, not finite-time absorption.
    """
    _resources(resample_size, steps, 1)
    inputs = _inputs(initial_distribution, scope, representation, sampled=False)
    _resources(resample_size, steps, len(inputs.effective_distribution))
    initial = _diversity(tuple(p for _, p in inputs.effective_distribution))
    factor = 1.0 - 1.0 / resample_size
    values, underflow = [initial], []
    for step in range(1, steps + 1):
        value = 0.0 if resample_size == 1 or initial == 0 else initial * exp(step * log1p(-1.0 / resample_size))
        if initial > 0 and resample_size > 1 and value == 0:
            underflow.append(step)
        values.append(value)
    return ExpectedDiversityResult(inputs, resample_size, steps, initial, factor, tuple(values),
        _metadata("expected_gini_simpson_diversity", "F-015", "ratio", inputs,
                  "analytic_expectation; D0*(1-1/n)**t; t=0..steps; constant n"), tuple(underflow))


def _sample_counts(rng: object, masses: tuple[int | float, ...], n: int) -> tuple[int, ...]:
    """Multinomial factorization with canonical order and explicit zero absorption.

    Integer masses after the first generation retain exact suffix sums. For the
    supplied float vector suffixes use fsum. Sampling the smaller binomial side
    avoids subtracting a tiny tail probability from one. Only the last positive
    state receives the remaining count; an exact zero state is never that state.
    """
    suffix = [0] * (len(masses) + 1)
    integers = all(type(mass) is int for mass in masses)
    for i in range(len(masses) - 1, -1, -1):
        suffix[i] = masses[i] + suffix[i + 1] if integers else fsum((masses[i], suffix[i + 1]))
    remaining, counts = n, []
    for i, mass in enumerate(masses):
        if mass == 0 or remaining == 0:
            count = 0
        elif suffix[i + 1] == 0:
            count = remaining
        elif mass <= suffix[i + 1]:
            count = int(rng.binomial(remaining, mass / suffix[i]))
        else:
            count = remaining - int(rng.binomial(remaining, suffix[i + 1] / suffix[i]))
        counts.append(count)
        remaining -= count
    if remaining != 0 or any(c < 0 for c in counts):
        raise _invalid("sampled integer count invariant failed")
    return tuple(counts)


def _generation(step: int, counts: tuple[int, ...] | None, probabilities: tuple[float, ...],
                state_order: tuple[str, ...]) -> SampledGeneration:
    support = tuple(state_order[i] for i, p in enumerate(probabilities) if p > 0)
    return SampledGeneration(step, counts, probabilities, support, len(support), _diversity(probabilities))


def simulate_closed_resampling(
    initial_distribution: object, *, resample_size: int, steps: int, seed: int,
    replicates: int, scope: CalculationScope, representation: RepresentationDescriptor,
) -> ResamplingSimulation:
    """Explicit seeded finite multinomial paths; no external inputs are accepted.

    Work limits and probability/domain checks precede the lazy NumPy import,
    generator creation and path allocation. One generator services all replicates
    in their recorded order. No global random stream is read or changed.
    """
    _resources(resample_size, steps, 1, replicates)
    _integer(seed)
    if seed.bit_length() > MAX_SEED_BITS:
        raise _invalid("seed exceeds the documented input-resource limit", resource=True)
    inputs = _inputs(initial_distribution, scope, representation, sampled=True)
    _resources(resample_size, steps, len(inputs.effective_distribution), replicates)
    state_order = tuple(s for s, _ in inputs.effective_distribution)
    probabilities = tuple(p for _, p in inputs.effective_distribution)
    initial = _generation(0, None, probabilities, state_order)
    try:
        import numpy as np
    except ModuleNotFoundError:
        raise _invalid("sampled closed resampling requires installed NumPy; no automatic installation", resource=True) from None
    rng = np.random.Generator(np.random.PCG64(seed))
    paths = []
    for replicate in range(replicates):
        masses, generations = probabilities, [initial]
        for step in range(1, steps + 1):
            counts = _sample_counts(rng, masses, resample_size)
            frequencies = tuple(count / resample_size for count in counts)
            generations.append(_generation(step, counts, frequencies, state_order))
            masses = counts
        paths.append(ResamplingReplicate(replicate, tuple(generations)))
    metadata = tuple(_metadata(name, formula, unit, inputs, "sampled_path; " + SAMPLER_ALGORITHM)
                     for name, formula, unit in (
                         ("state_count", None, "sampled_records"),
                         ("state_frequency", "F-001", "ratio"),
                         ("support_size", "F-002", "states"),
                         ("gini_simpson_diversity", "F-003", "ratio")))
    return ResamplingSimulation(inputs, resample_size, steps, replicates, seed, np.__version__,
                                state_order, tuple(paths), metadata)
