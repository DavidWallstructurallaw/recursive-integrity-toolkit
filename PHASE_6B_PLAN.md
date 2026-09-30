# PHASE_6B_PLAN

## Document control

| Field | Value |
|---|---|
| Project | Recursive Integrity Toolkit |
| Phase | Phase 6B: optional experimental simulation |
| Version / date | 1.0 / 2026-09-30 |
| Status | Steps 1 through 7 complete; Step 8 candidate verification in progress |
| Authority | Theory Owner instructions: `Phase 6B 继续吧`, `Phase 6B step 2 go`, `Phase 6B Step 3 开始`, `Phase 6B Step 4 继续`, `Phase 6B Step 5 go`, `Phase 6B Step 6继续`, `Phase 6B Step 7`, `Phase 6B Step 8` |
| Accepted starting commit | `b6389c6c50f2fc61d39580274bd24ed39e09ca45` |
| Accepted source tree | `b1c10344854f6af6176899f72b2d05344d5f8243` |
| Baseline branch / package / schema | `phase6a-longitudinal` / `0.1.0.dev5` / `1.2` |
| Working branch | `phase6b-simulation` |
| Eventual development candidate | `0.1.0.dev6`; report schema `1.3` |
| Merge, tag or publication authorization | None |

The initial instruction separately authorizes Phase 6B under approved UD-017.
This plan is newly prepared under that instruction; it was not part of the
earlier Phase 6A approval. Step 1 is recorded in
[PHASE_6B_STEP_1.md](PHASE_6B_STEP_1.md). The subsequent explicit Step 2 request
on 2026-09-30 authorizes the pure T5 kernel implementation under this plan;
see [PHASE_6B_STEP_2.md](PHASE_6B_STEP_2.md). The explicit Step 3 request on the
same date authorizes the experiment coordinator, baseline and comparison;
see [PHASE_6B_STEP_3.md](PHASE_6B_STEP_3.md). The Step 4 request on the same
date authorizes typed report integration, schema 1.3 and protected presentation;
see [PHASE_6B_STEP_4.md](PHASE_6B_STEP_4.md). The Step 5 request on the same
date authorizes explicit configuration, CLI execution and input-only validation;
see [PHASE_6B_STEP_5.md](PHASE_6B_STEP_5.md). The Step 6 request on the same
date authorizes user documentation and the installed synthetic example;
see [PHASE_6B_STEP_6.md](PHASE_6B_STEP_6.md). The Step 7 request on the same
date authorizes bounded scientific/adversarial and performance preparation;
see [PHASE_6B_STEP_7.md](PHASE_6B_STEP_7.md). The Step 8 request on the same
date authorizes the dev6 candidate, supported verification and development
handoff; actual acceptance is recorded in
[PHASE_6B_COMPLETION.md](PHASE_6B_COMPLETION.md).
Existing project synchronization permission continues.

## 1. Starting point and authority

Phase 6A is complete. The accepted checkout contains 323 tracked files, 41
Python package modules and 14 canonical packaged resources. Its tested dev5
candidate was `157109717079c9db9f02ac65ec1493709f37d8a4`; the accepted starting
commit adds the completed handoff record. Its successful candidate matrix is
historical evidence, not a Phase 6B verification result. Earlier development
PRs need not be merged to start this branch.

Apply `PROJECT_INSTRUCTIONS.md` section 4.4 and the frozen Phase 0 authority
order, approved UD decisions, and accepted Phase 3 numerical/report contracts.
Primary owners are T5 / TM-M07 / F-017 and PR-010, PR-011, PR-012, PR-013,
PR-014, PR-015 and PR-016. Reuse T1/F-015 for closed expectations and sampled
paths; do not transfer the closed multi-step expectation to reopened paths.
UD-017 authorizes experimental simulations. UD-031 continues to defer empirical
intervention ingestion. No new theory formula or public integrity score is
introduced.

The supplied *Universal Inbreeding Law v2.2* PDF, page 8, was inspected as a
rendered page to verify the reopening equation. Page 9 explains the limitation
on external-input quality. These agree with `DEFINITIONS_AND_UNITS.md` sections
12-13 and T5. The attached PDF does not silently replace the frozen source map
or authorize other theories' product features.

## 2. Objective and bounded model

Execute explicitly requested finite categorical scenarios and report their
assumptions, sampled trajectories, state losses and re-entry. Compare a closed
scenario with a reopened scenario only when both are requested on the same
declared basis and numerical parameters.

The reopened model is

\[
s_t=(1-\lambda)p_t+\lambda r,\qquad p_{t+1}=R_n(s_t),\qquad0\leq\lambda\leq1.
\]

This implementation specializes the source's time-indexed external input to a
constant, explicitly supplied `r`; `n` and `lambda` also remain constant within
a run. Both distributions declare exactly the same state IDs, including zero
masses. Equal positive support is not required. No automatic state alignment,
probability estimation from records, source-quality inference or hidden scenario
is permitted.

Each request selects `closed_resampling`, `reopened_resampling`, or both, with
each model appearing at most once. This preserves the existing singleton report
slots and limits a comparison to two declared scenarios. Users may make separate
explicit requests for lambda zero, a partial mixture or lambda one. Parameter
sweeps, time-varying external schedules and general experiment grids are outside
this phase.

All outputs carry `experimental` status and `simulation` evidence. Positive
mixed mass restores possible entry; an actual state re-entry additionally
requires a positive sampled count. Lambda is an input weight, not Presence,
integrity, external reliability or an empirical intervention effect.

External-reference loss F-016 remains excluded: its mathematical definition
exists, but the accepted report registry has no public trace for it. The
external input `r` must not become an assumed truth distribution `q`. Also
excluded are causal ingestion, model-performance prediction, universal scores,
new analytical dependencies, network access, dashboards and release publication.

## 3. Implementation decisions within the authorized scope

The exact staged interfaces and wire names are in
[docs/simulation_contract.md](docs/simulation_contract.md). These are maintainer
choices implementing existing meaning; their IDs do not create a new approval
system. [PHASE_6B_DECISIONS.md](PHASE_6B_DECISIONS.md) records their scope.

| Decision | Contract |
|---|---|
| P6B-D01 | Constant explicit `r`, lambda and `n`; identical declared state space; preserve literal zero and empty-string state IDs. |
| P6B-D02 | Reuse absolute mass tolerance and disclosed correction; preserve zero support; reject numerically erased positive reachability. |
| P6B-D03 | Named PCG64, canonical state order and replicate schedule; lambda zero reproduces the existing closed path, lambda one refreshes from `r` at every step. |
| P6B-D04 | Explicit one- or two-model request; reset the same supplied seed independently per model; common comparison inputs and aggregate work admission. |
| P6B-D05 | Per-replicate sampled trajectories and exact transition events; no Monte Carlo summary or significance claim in this phase. |
| P6B-D06 | One additive schema 1.3 integration, T5 only under `simulations`, inert assembly, inherited privacy and truthful execution states. |
| P6B-D07 | Explicit inert configuration and CLI activation; validate never samples; no distribution inferred from observed records. |

## 4. Step sequence and acceptance

| Step | Deliverable | Acceptance boundary |
|---|---|---|
| 1 | Plan, staged contracts, independent rational examples and current source boundary | Formula/source agreement, exact small enumeration, no runtime/schema/package changes |
| 2 | Pure external mixture and reopened sampler in `metrics/resampling.py` | Lambda endpoints, mass/count/support invariants, recurring re-entry, disclosed corrections, underflow rejection, deterministic replay and pre-allocation limits |
| 3 | Explicit experiment request, closed baseline and comparison orchestration | Only selected models execute; common inputs and seed retained; combined admission checked before any draw; no observed-data conversion |
| 4 | Typed assembly, canonical schema 1.3, JSON/Markdown and privacy | T5 evidence placement, exact event identities, forged-result rejection, closed restrictions retained, all new identity paths redacted |
| 5 | Configuration, audit/example activation and input-only validation | Full parameter serialization/hash, explicit activation, correct capability/execution states, local-only behavior and validation isolation |
| 6 | User documentation and one small installed synthetic example | Reproducible explicit closed/reopened comparison, assumption table, expected source arithmetic and honest stochastic interpretation |
| 7 | Bounded scientific/adversarial and performance preparation | Distinct failure modes detected, aggregate limits exercised, time/memory/output measured for a representative admitted request; no limits raised to pass |
| 8 | dev6 candidate verification and handoff | Current full regression, supported compatibility matrix, optional Parquet, security, performance and delivery gates; actual artifacts/results recorded |

Step 2 changes the obsolete T5 prohibition test to current behavior tests while
retaining the F-016/public-scope exclusions. It does not open the CLI or report
early. Step 4 is the only schema-version integration. Step 5 aligns executable
declaration checks without importing analytical owners into input-only modules.
Step 8 updates the development package version, not a release tag.

## 5. Scientific acceptance inputs

The independently authored fixtures under `tests/fixtures/reopening/` use
rational probabilities. For `p=(1,0)`, `r=(0,1)`, lambda `1/4` and `n=2`, the
mixed source is `(3/4,1/4)`. The possible count vectors `(2,0)`, `(1,1)`, `(0,2)`
have probabilities `9/16`, `6/16`, `1/16`. Re-entry of the second state has
probability `7/16`, while absence still has probability `9/16`. The mixture's
diversity is `3/8`; expected one-step sampled diversity is `3/16`.

Endpoint and contrasting cases cover lambda zero, lambda one at every step,
overlapping/identical distributions, a state absent from both sources, one-state
inputs, `n=1`, horizon zero, and repeated loss/re-entry. A first appearance from
an initial zero state satisfies the approved re-entry definition; earlier
positive history is not required. No event is assigned to step zero.

Future direct tests also cover mismatched declared spaces, shuffled literal
input order, invalid/nonfinite/bool probabilities and parameters, duplicate
states, tiny positive masses, near-unit totals, mismatched comparison inputs,
resource refusal before RNG creation, repeatability and untouched global RNG.
Separate sampler distribution checks from tests of exact count/path invariants.
Do not require every reopened path to gain diversity or every closed realized
path to lose it monotonically.

Use a finite set of meaningful faults: wrong lambda coefficient, external input
applied only at initialization, nonabsorbing lambda-zero state, reachability
reported as realized re-entry, step-zero event, recurrent event deduplication,
closed F-015 applied to reopened trajectories, swapped comparison direction,
implicit scenario execution, or raw state identity leaked through a new field.
No test-count quota or mutation registry is required.

## 6. Verification and delivery policy

Continue the user's Verification Governance and Complexity Control policy and
P5-D11. Direct scientific checks remain strict. Use the existing specification,
traceability and source-scope checks. Advance their single current accepted Git
reference/implementation allowlist at the appropriate step; do not add phase
dispatchers, approval registries, source-body migrations or evidence chains.

For Step 1 run the authored mathematical-oracle checks, their affected existing
closed numerical neighbors, existing scope-rejection tests and current static
checks. No compatibility matrix, wheel rebuild or 100k dataset measurement is
needed for contracts and fixtures.

For implementation steps run direct unit/integration checks for the behavior
changed. At the stable candidate, retain the existing Ubuntu/Windows,
Python 3.11/3.12, minimum/current direct-dependency matrix, actual PyArrow absence
and presence cases, security, Hero and installed delivery checks. T5 fixed-seed
replay is tested within each environment; bit-identical paths across NumPy
versions or platforms are not promised.

Simulation performance uses admitted state/step/replicate cells, not fabricated
dataset-record counts. Existing 100k dataset reference gates remain candidate
checks. Measure simulation runtime, peak memory and report sizes; bounded
execution failures retain reasons and do not yield truncated successful paths.

## 7. Completion and handoff

Phase completion requires all approved model outputs, assumption disclosure,
public evidence and privacy boundaries, actual supported-environment checks and
delivery verification. Record any failed attempt and its correction honestly.
Do not label Step 1 fixtures as implemented simulation or claim a Phase 6B
candidate pass from earlier evidence.

After Step 8, stop with a development handoff. Merging, release tagging and
publication remain separate actions. Phase 6A's completed records remain
historical and need no rewrite when this phase starts.
