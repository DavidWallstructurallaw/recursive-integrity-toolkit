# Phase 6B Step 3: explicit scenario experiments

Date: 2026-09-30. Status: **TASK COMPLETE, PHASE CONTINUES**.

## Completed

The Theory Owner requested `Phase 6B Step 3 开始`, authorizing this increment
from Step 2 commit `552df0b80e55780185bcd95a073f2c602f9d5366` on
`phase6b-simulation`.

Implemented `ScenarioExperimentRequest` and `run_scenario_experiment` in the
existing `metrics/resampling.py` owner. The inert request reuses existing
`ScenarioParameters` and retains a common scope, representation, explicit state
meaning and seed. Execution admits one or two unique selected models, validates
immutable declarations and shared supplied-vector/parameter agreement, then
checks combined work and predictable numerical failures before any sampled
trajectory or RNG is created. The experiment seed is limited to `0..2**53-1`;
standalone sampler limits remain unchanged.

Only selected models execute, in request order, each with a fresh PCG64 using
the same explicit seed. Adding or reordering the other model preserves each
model's result. A selected closed model receives a distinct analytic baseline
through the unchanged F-015 API, using exactly its sampled effective initial
vector and the basis `closed_sampled_effective_distribution`. The sampled
result retains the original correction; the analytic result retains its actual
input and has no invented seed or replicate count.

Two-model requests retain support and diversity values and their labeled
reopened-minus-closed differences for every replicate/step, including equal
step-zero values. Initial reachability and possible re-entry are explicitly
pre-first-draw possibilities. Horizon zero evaluates no transition mixture;
its possibility sets come from the declared positive coefficients. Closed
positive-to-zero events are derived from the actual paths. Reopened transition
and event evidence remains supplied by the existing kernel. No pooled Monte
Carlo summary, significance, external-quality ranking or empirical effect is
produced.

The immutable typed result retains the validated original request, ordered
sampled results, optional baseline, closed events and optional comparison for
Step 4 assembly. New parent representations hide caller text and state labels.
The existing input-only guard now includes the experiment API, and focused CI
includes its tests. The single source gate advances to Step 2 while authorizing
only the existing resampling owner. Architecture, contract and traceability
records describe the implemented handoff.

## Validation

One final focused run:

```text
tests/unit/test_scenario_experiment.py
tests/unit/test_T1_resampling.py
tests/unit/test_T5_reopening.py
tests/unit/test_reopening_fixture_inputs.py
tests/integration/test_phase3_metric_pipeline.py
tests/integration/test_current_verification.py
tests/integration/test_ci_workflows.py
373 passed in 5.72s
```

This includes 48 new experiment cases, 264 existing numerical/fixture cases and
61 integration/boundary cases, with no failures or skips. Tests cover explicit
selection, corrected baseline binding, independent replay, exact positive and
negative comparison differences, events, literal/canonical state identity,
zero horizon, common-input conflicts, collective refusal before execution,
inclusive work limits, future underflow, report-safe seeds, immutable inputs,
conversion-hook rejection, inert construction, repr privacy and global RNG
isolation. Existing T1/T5 endpoint and transition mathematics continue to pass.

Independent read-only review found no blocker. Its 27 supplemental experiment
probes varied lambda, horizon and seed and checked selection/order independence,
effective baseline input, complete closed events, comparison binding and repr
privacy. These probes are separate from the formal pytest count.

Verification used Python 3.12.14, pytest 9.1.1 and NumPy 2.3.5 with this checkout's
`src` first on `PYTHONPATH` and the preserved test dependencies. This is focused
source verification, not the later candidate compatibility or installed-wheel
matrix. Current specification, traceability and source/resource checks passed:
five schemas, 41 owned modules, 16 unchanged frozen specifications, 14 unchanged
canonical resource copies, 74 protected product files and one authorized runtime
owner. `git diff --check` passed.

## Continuation

Used approved UD-017 and P6B-D02/D03/D04/D05 under the existing T1/T5 and
PR-011/PR-016 contracts. No new theory decision or conflict was introduced.
UD-031 still defers empirical intervention ingestion; public F-016 remains
excluded.

Package `0.1.0.dev5`, report schema `1.2`, CLI and configuration behavior are
unchanged. Step 4 will add typed assembly, schema 1.3 serialization and privacy
validation of this supplied experiment evidence. No merge, tag or release
publication was performed.
