# Phase 6B decisions

| Field | Value |
|---|---|
| Status | Steps 1 through 3 complete |
| Authority | Theory Owner instructions `Phase 6B 继续吧`, `Phase 6B step 2 go`, `Phase 6B Step 3 开始`, 2026-09-30 |
| Governing decision | Approved UD-017; empirical ingestion remains deferred by UD-031 |
| Accepted baseline | `b6389c6c50f2fc61d39580274bd24ed39e09ca45` |
| Branch | `phase6b-simulation` |
| Current runtime | `0.1.0.dev5`, report schema `1.2` |
| Staged target | `0.1.0.dev6`, report schema `1.3` |

The current instruction authorizes starting Phase 6B. It is not represented as
prior approval of this newly written plan's individual engineering choices.
P6B-D01 through P6B-D07 in `PHASE_6B_PLAN.md` implement the existing authorized
model, evidence classes and product boundaries. There is no identified missing
theory decision blocking this bounded start.

Step 1 completed the preparation in the established stepwise workflow. Existing
permission to synchronize project work continues on this branch. No merge, tag,
publication, empirical intervention feature or F-016 public field is authorized
by this record.

## Step 1 clarifications

1. Use constant `r_t=r` as an explicit model assumption. Both vectors declare
   identical state IDs; their positive supports may differ. States introduced
   by `r` must be explicitly present with zero internal mass.
2. Exact event meaning comes from `DEFINITIONS_AND_UNITS.md` sections 12.10 and
   13.6. Repeated state losses and re-entries are valid separate transitions.
3. Reset the supplied PCG64 seed independently for each requested model. This
   makes replay and the lambda-zero equality check well defined; it does not
   establish paired statistical precision or causal effect.
4. Limit each request to one closed and/or one reopened scenario. Shared
   parameters are declared once. No general parameter grid or automatic
   lambda-zero/one control is added.
5. Reuse existing limits with a combined one-million-path-cell admission bound.
   New report-facing experiment requests use exactly representable nonnegative
   JSON seeds up to `2**53-1`; the existing standalone kernel's seed domain is
   unchanged. This is a serialization boundary, not a change in theory.
6. Opening T5 requires a model-specific report variant. The existing closed
   family continues to reject external parameters. Event uniqueness must retain
   replicate, step and state; valid recurrence must not be deduplicated.
7. Eligibility remains input-only. Align literal state validation and absolute
   mass tolerance with the accepted kernel; separately check executable limits.
   Config resolution, validation, assembly and rendering never create an RNG.

## Step 1 verification boundary

The single current source reference advances to accepted Phase 6A completion
`b6389c6`. Step 1's product implementation allowlist is empty. All 75 protected
product files, all 16 frozen specifications and all 14 canonical packaged
resources retain their accepted bytes. The obsolete dev4-to-dev5 exception is
removed because dev5 is now part of the accepted baseline.

The new rational fixtures are independent acceptance targets, not generated
sampled outputs. They validate their stated arithmetic; they do not certify an
unimplemented reopened sampler, report, CLI, privacy transform or performance
profile. Actual Step 1 checks are recorded in `PHASE_6B_STEP_1.md`.

## Step 2 authorization and numerical clarification

The Theory Owner requested `Phase 6B step 2 go` on 2026-09-30. Work starts from
`230e321f0de31953babe0372625a6e20164606f0` and implements the two pure APIs in
`metrics/resampling.py`. P6B-D01/D02/D03/D05 govern this increment. Experiment
orchestration, report schema and CLI execution retain their later-step scope.

Endpoint source records preserve the already effective vector without applying
a second correction. Lambda zero's later actual sampler masses are integer
counts, with count/n retained as transition evidence. Lambda one refreshes from
the same effective external vector at every step. Partial mixtures use the
previous generation's actual count/n values and disclose any correction of the
computed mixed source. These details preserve the existing closed numerical
route and the declared F-017 transition.

Initial mixed-source underflow is rejected before RNG creation. For horizons
of at least two, a positive external weighted term rounded to zero is rejected
even if initial internal mass masks it: a later loss could expose false zero
reachability. Horizon zero validates its inputs and returns initial generations
with no transition-source or event records. No numerical tolerances or work
limits are relaxed.

The single current source gate advances to Step 1 commit `230e321`, authorizing
only `src/recursive_integrity_toolkit/metrics/resampling.py`. The other 74
protected product files, 16 frozen specifications and 14 canonical resource
copies remain unchanged. Existing focused CI includes the T1/T5 and rational
fixture tests. Actual checks are in `PHASE_6B_STEP_2.md`.

## Step 3 authorization and experiment handoff

The Theory Owner requested `Phase 6B Step 3 开始` on 2026-09-30. Work starts from
Step 2 commit `552df0b80e55780185bcd95a073f2c602f9d5366`. P6B-D04/D05 govern
the explicit coordinator and comparison; D02/D03 continue to govern its numerical
and replay behavior. Scope, representation, state meaning and seed occur once
in `ScenarioExperimentRequest`. Existing per-model `ScenarioParameters` retain
their vocabulary; their common supplied vector and numerical parameters must
agree. Immutable probability-pair tuples preserve the original validated request.
Constructor declaration is inert; execution validates everything collectively.

The closed baseline is computed only when closed is selected and uses exactly
that sampled result's effective initial vector. Its `baseline_basis` is
`closed_sampled_effective_distribution`; original correction evidence remains in
the sampled input. Selected results preserve request order and independently
reset the seed. Comparison rows and closed loss events derive from actual typed
paths, without additional sampling. At horizon zero, initial reachable/re-entry
sets describe declared next-draw possibilities, with no executed mixture/event.

The existing source gate advances to Step 2, still authorizing only
`metrics/resampling.py`. No report schema, input/config/CLI behavior, dependency
or package version is changed. Step 4 will validate and serialize this typed
handoff. Actual checks are recorded in `PHASE_6B_STEP_3.md`.
