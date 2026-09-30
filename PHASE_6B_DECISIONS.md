# Phase 6B decisions

| Field | Value |
|---|---|
| Status | Steps 1 through 7 complete; Step 8 verification in progress |
| Authority | Theory Owner instructions `Phase 6B 继续吧`, `Phase 6B step 2 go`, `Phase 6B Step 3 开始`, `Phase 6B Step 4 继续`, `Phase 6B Step 5 go`, `Phase 6B Step 6继续`, `Phase 6B Step 7`, `Phase 6B Step 8`, 2026-09-30 |
| Governing decision | Approved UD-017; empirical ingestion remains deferred by UD-031 |
| Accepted baseline | `b6389c6c50f2fc61d39580274bd24ed39e09ca45` |
| Branch | `phase6b-simulation` |
| Current runtime | `0.1.0.dev6`, report schema `1.3` |
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

## Step 4 authorization and report boundary

The Theory Owner requested `Phase 6B Step 4 继续` on 2026-09-30. Work starts from
Step 3 commit `2e0805dba85754d78854750f692ac02ddaf44a8a`. P6B-D06 implements the
approved T5 evidence placement and existing PR-012 through PR-016 reporting,
privacy and reproducibility boundaries. Schema 1.3 is integrated once, in the
existing schema/field-registry owner, with its packaged copy kept identical.

The typed experiment is supplied explicitly to assembly. Request/result binding,
source arithmetic, complete events and comparison checks never execute a kernel
or RNG. Closed/T2 restrictions remain model-specific. A separately supplied
legacy closed result may coexist with a reopened-only experiment without
manufacturing a comparison. The analytic baseline retains its own closed
envelope and effective-start basis.

State pseudonyms preserve cross-model alignment and numerical array positions;
record-identity omission does not remove semantic states. Markdown limits
detail tables while JSON retains full admitted evidence. Input eligibility stays
separate from actually supplied execution evidence, and the empirical intervention
conclusion remains unavailable for simulation results.

The source gate advances to Step 3 and authorizes only `result.py`, report
assembly, Markdown and the canonical/packaged report schema pair. Numerical
kernels, CLI/configuration, dependencies, package version and frozen root
specifications remain protected. Existing current report fixtures move only
their schema-version literals unless a concrete strengthened contract requires
a matching fixture correction. Later CLI activation retains Step 5 scope.
Actual final source checks and the unrun installed-case boundary are recorded in
`PHASE_6B_STEP_4.md`.

## Step 5 authorization and execution boundary

The Theory Owner requested `Phase 6B Step 5 go` on 2026-09-30. Work starts from
Step 4 commit `f5d94d9aa250bbb63c7317884966946bc1d44533`. P6B-D07 connects the
complete declaration block to explicit audit/example execution. Partial legacy
declarations remain inert; an activated audit requires every scientific input.
An explicitly false enabled value conflicts with `--simulate`. Validation always
stays input-only, including complete enabled configurations.

The input layer shares literal-state, absolute-mass and admission predicates with
observability without importing numerical owners. Full context survives config
serialization and hashing. Scope uses supplied labels with no record membership;
audit data never implies a distribution. Existing family failures preserve
independent results, and run metadata binds the selected seed. Report assembly
defers scenario-owner imports until supplied simulation evidence needs adapting.

The example command accepts a scenario-only local config overlay, validated
before workspace creation and preserved in the extracted config. Ordinary
packaged examples and canonical resources remain unchanged. The standalone
installed synthetic example remains Step 6 work.

The existing source gate advances to Step 4 with five exact product owners:
config, CLI, observability, config schema and the assembly import adjustment.
The numerical kernels, report schema/renderers, dependencies and package version
remain frozen. Focused checks and corrected attempts are recorded in
`PHASE_6B_STEP_5.md`; no candidate or installed delivery pass is claimed.

## Step 6 authorization and installed example

The Theory Owner requested `Phase 6B Step 6继续` on 2026-09-30. Work starts from
Step 5 commit `33ae8af1aaeb99ac118368148a80d563804eeff9`. The increment adds a
small packaged `simulation` dataset, explicit CLI selection and a user walkthrough
under the existing P6B-D01 through D07 contracts.

The teaching case uses the independent rational Step 1 example: `p=(1,0)`,
`r=(0,1)`, lambda `1/4` and sample size 2. Six transitions and three replicates
with seed 17 make a bounded replayable report. Separate fictional audit records
use X/Y topics; they never establish A/B probabilities or scenario membership.
The packaged expectations enumerate first-step possibilities without pinning
cross-environment random paths or guaranteeing realized re-entry.

`example --dataset simulation --simulate` requires explicit activation and
rejects custom overlays, lineage and longitudinal example modes before workspace
creation. It copies all four resources unchanged. A user may edit a separate
config and rerun `audit --simulate`; the existing overlay interface on other
examples is unchanged. Documentation explains assumptions, closed-baseline scope,
source/sample distinction, possible/realized re-entry, privacy and input-only
validation.

The existing source gate advances to Step 5, authorizing only the CLI owner,
one package-data addition and eight canonical/packaged resource paths. Every
other parsed package-metadata value remains protected. The 41 runtime modules,
16 frozen specifications and report schema 1.3 are unchanged; packaged resources
increase from 14 to 18. The existing installed-example and workflow checks are
extended rather than adding a separate delivery registry.

Actual local wheel and sdist-derived wheel installations are recorded in
`PHASE_6B_STEP_6.md`. This is bounded example delivery evidence; the supported
candidate matrix, actual optional-dependency absence, performance preparation,
dev6 version change and any release action retain their later scope.

## Step 7 authorization and bounded verification

The Theory Owner requested `Phase 6B Step 7` on 2026-09-30. Work starts from
Step 6 commit `065cafa017881258c6dc139c22815b806b75bce6`. All 83 product files
are frozen at that commit; the existing source gate has an empty implementation
allowlist. No runtime, schema, package, example or numerical limit changes are
needed for this increment.

Scientific checks add an independent three-state joint multinomial enumeration
and a concentrated external-source counterexample to guaranteed diversity gain.
The ten concrete faults already named in the plan are tested separately in
disposable source copies against existing direct assertions. Their outcomes are
recorded in the step record, without adding a mutation framework or registry.

Real one-million-cell admission and immediate over-budget refusal are exercised
across configuration, eligibility and kernel preflight. Accepted boundary probes
stop at the first generation, so they establish admission without claiming
full-capacity report performance. Both model orders also exercise failure after
the first model completes: all scenario evidence is discarded and independent
audit results remain available.

The existing report measurement fixture now records Linux process peak RSS via
`/proc/self/status` `VmHWM`, avoiding the inherited parent peak in `ru_maxrss`.
Optional timing wraps the actual experiment coordinator; complete CLI publication
remains separately timed. Four fresh untraced observations cover 84 and 33,280
combined state/step/replicate cells, each with two loaded fictional audit records. Every
attempt is retained, including input hashes and JSON/Markdown sizes. No new
performance SLA or capacity guarantee follows from these bounded observations.

Actual checks and all measurement results are recorded in `PHASE_6B_STEP_7.md`.
The package remains dev5 and schema 1.3. The full supported matrix, actual PyArrow
absence/presence, 100k dataset workload, installation/security gates and dev6
candidate handoff remain Step 8 work.

## Step 8 authorization and candidate boundary

The Theory Owner requested `Phase 6B Step 8` on 2026-09-30. The accepted
starting commit is `9af8462bee86c367b6d0f5ae560e97f96cc58409`. This increment
advances only the two package version declarations from dev5 to dev6. The source
gate requires exact accepted bytes after that single replacement in each file;
all other product files remain frozen. Current tests and five report goldens
receive only the corresponding toolkit-version metadata change. Mathematical,
evidence-class, scope, privacy and schema assertions remain intact.

Existing candidate jobs perform the complete supported matrix, actual optional
dependency absence and presence, scientific/Hero, security, complete performance
and installed delivery checks. Dedicated security selection includes the new
simulation disclosure and execution boundaries. No new verification registry
or phase dispatcher is introduced. The current candidate's actual results and
all material failed attempts are recorded in `PHASE_6B_COMPLETION.md`; previous
candidate results retain their named source and cannot certify this candidate.

UD-017 supplies the simulation authority; UD-031 keeps empirical intervention
ingestion deferred. This is the development handoff authorized by the plan.
Main merge, release tagging and publication retain separate scope.
