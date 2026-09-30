# Phase 6B simulation contract

Status: staged implementation contract, 2026-09-30. Step 1 does not activate these
APIs, configuration fields or report schema 1.3. The current running package is
dev5/schema 1.2. See `PHASE_6B_PLAN.md` for scope, owners and implementation order.

## 1. Mathematical and input boundary

T5/F-017 implements `s_t=(1-lambda)*p_t+lambda*r`, followed by the existing finite
multinomial operator `p_(t+1)=X_t/n`. The external distribution `r`, reopening
weight and positive integer `n` are constant within the scenario. The supplied
external source is a model assumption; no declaration proves genuine independent
ancestry, reliability or relevance.

Both probability vectors are explicit built-in dictionaries, immutable mapping
proxies or tuples of `(state_id, probability)` pairs accepted by the existing
resampling owner. They must have the same complete declared state set. Positive
support means strictly positive mass; no tolerance turns a positive mass into
zero. A state absent internally but present externally must occur in the
internal vector with an explicit zero. Reject mismatched sets, duplicate states,
empty vectors, booleans, nonfinite/out-of-range probabilities and unsupported
objects. Do not align, trim, normalize labels or estimate probabilities.

State IDs are literal valid UTF-8 strings without NUL, including the literal
empty string. Preserve canonical ascending Unicode order. Callers supply one
`RepresentationDescriptor` and explicit state meaning for the experiment.
Both vectors share that declared meaning. Scientific compatibility is asserted
by the caller, not inferred from matching label spelling.

The pure kernel also receives the existing `CalculationScope`. It preserves
the declared vector's scope separately from observed audit data. The experiment
interface does not claim that the vector was measured from loaded records.

## 2. Numerical policy and resource admission

Reuse `NumericalPolicy` with absolute probability-mass tolerance `1e-12`.
Validate each supplied vector independently before mixing. For sampled execution,
reuse the accepted divide-by-validated-total correction only when its total
differs from one within that tolerance. Retain supplied/effective vectors,
totals, residual, correction method, divisor and per-state corrections for both
internal and external inputs. Do not introduce clipping or a looser tolerance.

Compute each mixture using nonnegative contributions and accurate summation.
Retain the raw and effective mixed vector through the same disclosed bounded
correction policy. Reject a numerically zero mixed mass when its mathematical
source is positive (`lambda < 1 and p_i > 0`, or `lambda > 0 and r_i > 0`). This
includes underflow that would silently erase restored reachability. No positive
support may disappear during correction. Later transition normalization refers
to that transition's current source, not a silently reused initial mixture.

Lambda zero uses the existing closed transition route, retaining integer counts
as masses after the first draw. This protects exact equality to the accepted
closed sampler. Lambda one uses the effective external vector before every
draw. It is not equivalent to a multi-step closed process initialized with `r`.

| Bound | Contract |
|---|---|
| Declared states | 1 through 4096 |
| Resample size | Integer 1 through 2147483647 |
| Horizon | Integer 0 through 10000 |
| Replicates | Integer 1 through 10000 |
| Standalone sampler seed | Existing nonnegative integer, at most 4096 bits |
| New report-facing experiment seed | Integer 0 through `2**53-1`, exactly representable across JSON consumers |
| Requested models | One or two distinct supported names |
| Combined sampled-path cells | Sum of `states*(horizon+1)*replicates` over selected models, at most 1000000 |

All parameters are explicit, including replicate count. Booleans are not
integers. Validate every requested input and the combined budget before any RNG
creation or trajectory allocation. Bound mixed-source and event output by the
same admitted transitions/state cells; do not copy unbounded paths into summary
tables. A resource refusal yields an explicit failure, never a truncated
successful trajectory. Existing standalone API limits are not relaxed.

## 3. Staged Python interface and owner

`metrics/resampling.py` remains the mathematical owner. NumPy stays lazy and
confined to this module. No new analytical dependency is needed.

```python
mix_external_input(
    internal, external, *, reopening_weight,
    scope: CalculationScope, representation: RepresentationDescriptor,
) -> ExternalMixtureResult

simulate_reopened_resampling(
    internal, external, *, reopening_weight,
    resample_size, steps, seed, replicates,
    scope: CalculationScope, representation: RepresentationDescriptor,
) -> ReopeningSimulation

run_scenario_experiment(request: ScenarioExperimentRequest) -> ScenarioExperimentResult
```

`ExternalMixtureResult` retains separately validated internal/external inputs,
lambda, raw/effective mixture and numerical disclosure. It is deterministic and
does not import NumPy or invent a seed. `ReopeningSimulation` retains the same
context and replay metadata as `ResamplingSimulation`, plus constant external
inputs, lambda, transition sources and events. Its model is
`reopened_resampling`, method `sampled_path`, method version
`reopened_categorical_constant_v1`, primary owner T5, evidence `simulation`,
and experimental flag true. Field values must be detached immutable data.

Reuse `SampledGeneration` and `ResamplingReplicate` where their meaning is
unchanged. Step zero retains the supplied effective initial frequencies and
`state_counts=None`; do not invent a sampled initial population. All later
counts are nonnegative integers summing exactly to `n`, and frequencies equal
counts divided by `n`. Support and Gini-Simpson diversity are retained per step.

Each transition records `(replicate_index, step)` with `step >= 1`, the mixed
pre-resampling distribution and its correction evidence. Re-entry and loss
events retain `(replicate_index, step, state_id)`. Their definitions are:

| Event or possibility | Exact condition |
|---|---|
| Reachable next state | Effective mixed probability is positive |
| Possible re-entry at this transition | Current internal frequency is zero and mixed source probability is positive through the declared external input |
| Realized state re-entry | Possible re-entry and positive next sampled count |
| Simulated extinction event | Positive current internal frequency and zero next sampled count |

An initially absent state may re-enter on step one. Repeated loss/re-entry of
the same state is retained. Horizon zero has one initial generation per
replicate and no transitions or events. Simulated extinction here is a local
transition; only the closed model makes subsequent absence absorbing.

## 4. Request, execution and comparison

`ScenarioExperimentRequest` is an immutable declaration, using existing
`ScenarioParameters` for each selected model instead of a second parameter
vocabulary. It contains:

- ordered, unique selected model names (`closed_resampling`, `reopened_resampling`);
- a common internal `state_distribution`, scope, representation and state meaning;
- common `resample_size`, `simulation_horizon`, `simulation_replicates` and seed;
- `external_input_distribution` and `reopening_weight` exactly when reopening is selected.

It admits one instance of each model. Both branches of a comparison use exactly
the same initial distribution, representation/meaning, declared states, sample
size, horizon, replicates, seed and numerical/sampling methods. The external
distribution and lambda apply only to the reopened branch. Reject conflicting
declarations before execution. Do not add a baseline or a lambda endpoint just
because another scenario was requested.

Use `numpy.random.Generator(PCG64)` with
`sequential_binomial_complement_v1`, canonical states and
`replicate_major_step_major` scheduling. Create a fresh RNG with the same
explicit seed for each selected model (`reset_same_seed_per_model`). Adding or
reordering the other model must not change a model's sampled paths. Do not
read/change global RNG state. Retain NumPy version and sampler/model identities.
Replay is promised within the same method and numerical environment, not
bit-identically across platforms or dependency versions.

The experiment owner calls the closed analytic expectation explicitly when the
closed scenario is requested. It retains this as a distinct analytic baseline,
with no seed/replicate identity. This resolves the current report's one-slot
constraint without overwriting the sampled result or pretending the expectation
is a realization. Pass the sampled closed result's effective initial vector to
the unchanged analytic API and declare the baseline basis as
`closed_sampled_effective_distribution`. Retain the original supplied-to-effective
correction in the parent closed result and the analytic API's own input record
in the baseline. The legacy analytic API still performs no normalization; do
not compare an uncorrected caller-vector expectation against a corrected sampled
start and silently call them the same basis.
The closed F-015 multi-step baseline is never attached to a
reopened trajectory. Kernel numerical-underflow disclosures remain intact.

When both models are selected, retain comparison rows by `(replicate_index,
step)` for support size and diversity, with both values and the explicitly
labeled `reopened_minus_closed` differences. At step zero the two sides agree.
Include each model's initially reachable states and initially possible re-entry
states, labeled as pre-first-draw possibilities. Later possibilities are in the
transition sources. No pooled means, quantiles, confidence intervals, p-values,
causal effects or variance-reduction claims are produced. Matching replicate
indices identify reproducible paths; differing distributions may consume RNG
draws differently. Comparisons do not diagnose which external input is better.

`ScenarioExperimentResult` retains the original validated request, selected
typed results, optional closed analytic baseline and comparison evidence.
Assembly validates that supplied evidence is bound to that request and has
consistent counts/events/lengths. It never reruns a sampler to establish trust.

## 5. Staged configuration and CLI

Extend the existing `simulation` block, preserving `enabled` and `seed`.
Other fields are inert declarations. Unknown/competing fields are rejected.

| Config field | Meaning |
|---|---|
| `enabled` | Explicit execution request; default false |
| `seed` | Common experiment seed; canonical report name `random_seed` |
| `models` | One or two distinct names in explicit order |
| `state_distribution` | Explicit literal state-to-probability object |
| `external_input_distribution` | Required exactly when reopened model selected |
| `reopening_weight` | Required exactly when reopened model selected |
| `resample_size` | Positive integer n |
| `simulation_horizon` | Nonnegative integer transition count |
| `simulation_replicates` | Positive integer repeat count |
| `representation` | Full existing `RepresentationDescriptor` declaration |
| `state_semantics` | Explicit shared state meaning, protected as caller text |
| `scope_id` | Explicit scenario scope identity |
| `dataset_version` | Explicit single scope version label; does not prove empirical derivation |

For this config adapter, construct a scenario `CalculationScope` with the two
supplied scope labels, empty included/excluded record identities and
`denominator_basis=explicit_scenario_probability_vector`. Do not infer scope
membership from the audit bundle or assign `n` synthetic record IDs. Python
callers retain the accepted explicit scope interface.

`audit --simulate --config PATH` can explicitly enable this block; an explicitly
enabled complete block also requests execution without the flag. A false
enabled value competing with `--simulate` is an error. Without activation,
valid declarations may be validated but no scenario runs. Partial disabled
legacy `enabled`/`seed` configurations remain inert; activation requires all
scientific declarations. There are no defaults for lambda, distribution, seed,
n, horizon, replicates or selected models.

`validate` always performs input-only work, even with complete enabled scenario
declarations. It must never import/call the sampler, create an RNG, or promote
execution to completed. Declaration eligibility remains separate from actual
execution. Full declarations and scope must survive config round-trip and
normalized hashing. Safe summaries must not leak distribution keys or caller
text. The run seed and all stochastic result seeds must agree.

Align existing eligibility predicates with the literal-state, absolute mass,
range and executable-admission contracts above. Keep this validation in an
input-only/shared declaration layer; do not import `metrics/resampling.py` into
`observability/levels.py` merely to reuse private helpers. Its current
`math.isclose` predicate is not a different approved probability-repair policy.

The example command may select a new explicit synthetic simulation example;
ordinary Hero and longitudinal examples keep their existing behavior. No
standalone server, remote source retrieval or experiment-scheduling service is
introduced.

## 6. Staged canonical report

`result.py` remains the schema and field-registry owner. Generate schema 1.3 and
its packaged copy together in Step 4. Default `simulations` remains `{}`. Extend
`assemble_report` with an explicit optional `scenario_experiment` argument. It
conflicts with legacy `expected_diversity`/`resampling` arguments if they would
occupy the same closed slot; reject rather than overwrite. Legacy calls retain
their existing result shape. Tail extinction remains a separately supplied
T2 analytic result, without automatic tail selection.

| Public path | Meaning / owner |
|---|---|
| `simulations.closed_resampling` | Existing T1 sampled envelope when selected |
| `simulations.closed_resampling.state_semantics` | Experiment's shared state meaning, when supplied through the new experiment interface |
| `simulations.closed_resampling.analytic_baseline` | Distinct T1/F-015 analytic envelope with expected diversity, initial diversity, contraction factor, normalization and underflow disclosure; no RNG identity |
| `simulations.closed_resampling.extinction_events` | Supplied positive-to-zero transition events |
| `simulations.external_reopening` | T5 experimental simulation envelope |
| `...model`, `...model_version`, `...method` | Reopened constant-source model and sampled method identities |
| `...parameters` | Existing canonical parameter names, scalar lambda and replay metadata; `scenario_schedule=reset_same_seed_per_model` |
| `...initial_distribution` | Effective internal starting vector |
| `...input_normalization` | Supplied/effective internal vector and correction evidence |
| `...state_semantics` | Supplied shared state meaning; protected caller text |
| `...external_input_distribution` | Effective constant external vector, also bound to the parameter declaration |
| `...external_input_normalization` | Separately supplied/effective external vector and correction evidence |
| `...sampled_paths` | Typed per-replicate initial and sampled generations |
| `...mixed_sources` | Transition-indexed pre-draw source vectors and correction evidence |
| `...state_reentry_events` | Exact realized re-entry events, no step zero |
| `...extinction_events` | Exact local positive-to-zero transitions, including recurrent losses |
| `...support_trajectory`, `...diversity_trajectory` | Per-replicate arrays from step zero through horizon, bound to sampled paths |
| `...scenario_comparison` | Only when both models were requested: identities, initial reachability and per-replicate/step comparison rows |
| `...assumption_table` | Fixed rule rows describing declarations and their unverified external-quality limitation |

Here `...` means `simulations.external_reopening`. Required top-level envelope
metadata includes scope, representation, assumptions, limitations, trace T5,
evidence class `simulation` and status `experimental`. Do not create new report
root sections. T5's planned `horizon`/`seed` aliases map to the established
`parameters.simulation_horizon` / `parameters.random_seed`; its
`internal_distribution` maps to `initial_distribution` plus the retained
`input_normalization.supplied_distribution`. Avoid competing wire aliases.

Closed expectations remain distinguishable from sampled closed paths. The
analytic baseline retains its own approved assumptions and limitations and
does not acquire lambda/r parameters. Each model remains valid without the
other. Standalone reopened output omits `scenario_comparison`; it does not
silently execute a control scenario.

Use T5-specific structural/semantic validation while keeping the current closed
and T2 prohibitions on external inputs. Check count/frequency/support consistency,
transition source arithmetic, event conditions, complete event coverage,
replicate/step coverage and comparison binding. These are bounded checks of
supplied evidence, not new analysis or RNG dispatch. Event uniqueness is
`(replicate_index, step, state_id)` within its model; mixed-source/comparison
uniqueness is `(replicate_index, step)`. Generic uniqueness by state ID alone
must not reject recurrence. No T5 object may claim F-015 expected contraction
for its reopened path.

Capability `intervention_simulation` retains its legacy name. Inputs may qualify
as experimental while execution is not requested, deferred, failed or completed.
Completed requires actually supplied successful results. Preserve reasons for
noncompleted execution and valid independent audit families on scenario failure.
Always retain `unavailable_conclusions.empirical_intervention_effect`; its
explanation must acknowledge the simulated evidence while stating that no
empirical intervention effect was established. No lambda-to-integrity mapping.

## 7. Presentation, privacy and limits

Markdown uses a visible experimental/simulation label and a compact assumption
table: fixed state space, multinomial transition, constant n/lambda/r, input
basis, replay schedule, numerical corrections and unverified external quality.
Closed-only output also discloses its assumptions; lambda/r rows are omitted or
marked not applicable, without suggesting an external input was provided.
Display simulation step separately from dataset version/generation. Source
probability and realized sample count must remain distinguishable.

Reuse established detail-table limits (100 rows) with full bounded JSON evidence
and truthful omission counts. This includes state/source/event tables. Trajectory
rows summarize support and diversity; they must not embed a full 4096-state
vector in each visible row and defeat the detail bound.
Display both comparison values and labeled scenario
differences. Do not imply monotonically improving diversity, guaranteed re-entry
or causal benefit. Float presentation must not relabel a positive tiny value as
an exact theoretical zero.

Apply existing standard/redacted policies to every state identity:
internal/external distribution keys, correction entries, state order,
mixed sources, support arrays, event state IDs, initially reachable/possible
re-entry lists and comparison metadata. Scenario scope/version labels and caller
state meaning receive the same existing protections as other scope/text fields.
Raw values must not escape through errors, repr, normalized-config summaries or
assumption text. In redacted mode, semantic state identities remain consistently
pseudonymized across both models, regardless of the record-ID mode. The inherited
`preserve`/`hash`/`omit` option governs record identities and associated record
collections, not a new semantic-state omission policy. Keep numeric values,
state alignment and event relationships intact through the protected identities.

No network, content retrieval, executable config, hidden logging or new public
loss/score field is part of this contract. Step 1 fixtures test independent
mathematics only; later steps must separately validate actual execution,
serialization, privacy, installation and resource behavior.
