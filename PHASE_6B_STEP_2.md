# Phase 6B Step 2: external mixture and reopened sampler

Date: 2026-09-30. Status: **TASK COMPLETE, PHASE CONTINUES**.

## Completed

The Theory Owner requested `Phase 6B step 2 go`, authorizing this increment from
Step 1 commit `230e321f0de31953babe0372625a6e20164606f0` on `phase6b-simulation`.

Implemented `mix_external_input` and `simulate_reopened_resampling` in the
existing `metrics/resampling.py` owner. The pure mixture computes F-017 without
NumPy or RNG creation. The sampled kernel uses constant explicit external input
and weight, named PCG64 and the accepted sequential-binomial sampler. Both return
immutable, detached experimental simulation evidence with separate supplied and
effective vector records.

The sampler records each transition's mixed source and possible re-entry set,
sampled paths, realized re-entry events and local extinction events. It preserves
recurrence and distinguishes initial absent-state entry from step-zero events.
Lambda zero retains exact closed paths through the existing integer-mass route;
lambda one refreshes from the effective external vector on every draw.

Extracted the accepted bounded normalization calculation into one private shared
helper. Legacy closed calculations retain their numerical behavior. Endpoint
source records avoid a second correction; partial mixtures disclose their own
raw/effective correction. Initial and predictable future underflow that would
erase positive reachability are rejected before RNG creation. Existing work,
seed and numerical bounds are unchanged.

Replaced the obsolete T5 runtime prohibition test with direct behavior tests.
Existing input-only integration guards now cover both new functions and both
scenario model declarations. The existing focused CI command includes T1/T5
and the rational fixtures. The single source gate advances to Step 1 with only
`metrics/resampling.py` authorized. Updated current architecture, traceability
and the simulation contract with actual implemented interfaces and numerical
clarifications.

## Validation

Final numerical run:

```text
tests/unit/test_T1_resampling.py
tests/unit/test_T5_reopening.py
tests/unit/test_reopening_fixture_inputs.py
264 passed in 0.90s
```

The T5 suite contains 116 cases. It uses independently authored rational
mixtures, exact possible-count paths for event semantics, real fixed-seed path
invariants and a bounded one-step marginal sanity check. Coverage includes
lambda endpoints, integer draw masses, repeated events, actual current-source
mixing, count/frequency/support identities, distinct input/mixed corrections,
masked future underflow, no unexecuted horizon-zero transition, invalid literal
inputs, resource refusal before allocation, required parameters, conversion-hook
rejection, no global RNG effects, no I/O/raw diagnostic identifiers and pure
mixture operation with NumPy blocked.

Affected boundary run:

```text
tests/integration/test_phase3_metric_pipeline.py
tests/unit/test_PR013_report_schema.py
tests/unit/test_PR010_observability.py
tests/unit/test_PR016_determinism.py
tests/unit/test_phase3_contracts.py
tests/integration/test_no_algorithms.py
tests/integration/test_current_verification.py
tests/integration/test_ci_workflows.py
307 passed in 38.89s
```

These two runs cover **571 distinct passing tests**, with no failures or skips.
They used Python 3.12.14, pytest 9.1.1 and NumPy 2.3.5 with this checkout's
`src` first on `PYTHONPATH` and the preserved test dependencies. This is source
verification, not a candidate compatibility matrix or installed-wheel claim.

Independent read-only review found no numerical or metadata blocker. Its
additional 81-scenario probes checked exact lambda-zero replay, source
reconstruction, complete event sets and future-underflow handling. These probes
are supplementary and are not added to the 571 pytest count.

Current specification, traceability and source/resource checks passed: five
schemas, 41 owned modules, 16 unchanged frozen specifications, 14 unchanged
canonical resource copies, 74 protected unchanged product files and one
authorized runtime owner. `git diff --check` passed. No new dependency, schema,
resource or package-version change was made.

## Decisions and continuation

Used approved UD-017, T5/TM-M07/F-017, Definitions 12-13, accepted Phase 3
numerical/replay policy and P6B-D01/D02/D03/D05. UD-031 continues to defer
empirical intervention ingestion. Conflicts: none.

Runtime remains version `0.1.0.dev5`, report schema `1.2`. Step 3 will compose
explicit scenario requests, the closed analytic baseline and scenario
comparisons. T5 report serialization, new config/CLI execution, example delivery,
performance preparation and dev6 candidate verification remain in their planned
steps. External-reference loss F-016 stays excluded. No merge, tag or publication
was performed.
