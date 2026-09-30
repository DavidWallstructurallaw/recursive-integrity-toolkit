# Theory Traceability

## Current Phase 6B Step 7 verification

T5/F-017 gains a three-state joint count-law check using independently enumerated
rational multinomial probabilities. With mixed source `(1/2,3/8,1/8)` and `n=3`,
the ten count vectors sum to probability one, the initially absent third state
has re-entry probability `169/512`, and expected sampled diversity is `19/48`.
Broad per-outcome sampling bounds avoid cross-environment path promises.

A lambda-one source concentrated on one state, with initial `p=(1/2,1/2)` and
sample size 4, produces exact zero diversity after every transition while the
closed F-015 expectation stays positive at finite horizons. This preserves the
external-input quality limitation and prevents an assumed diversity benefit.
No reopened multi-step F-015 identity
is introduced.

The plan's ten scientific, execution and privacy faults are each detected by
existing direct tests in disposable source copies. PR-010/PR-011 aggregate
admission is exercised at its actual limit; PR-014/PR-015 failure handling retains
independent audit evidence while discarding an incomplete experiment. The
[Step 7 record](../PHASE_6B_STEP_7.md) identifies each detector and the complete
bounded performance observations. Product and theory definitions are unchanged.

## Accepted Phase 6B Step 6 implementation

The installed synthetic example exposes the accepted T1/T5 comparison with
explicit `p=(1,0)`, `r=(0,1)`, lambda `1/4` and sample size 2. Its packaged
mathematical expectations reuse the Step 1 rational case: first source
`(3/4,1/4)`, count-vector probabilities `9/16,6/16,1/16`, re-entry probability
`7/16` and one-step expected sampled diversity `3/16`. These arithmetic targets
are independent of generated sample paths. The closed path remains absorbed
at A, with its own zero-diversity F-015 baseline.

PR-011/PR-016 govern explicit activation and same-environment replay. PR-012
keeps all scenario paths under simulation evidence; PR-014 retains unavailable
empirical intervention conclusions. PR-015 protects reports while the copied
public input declarations remain intact. The separate X/Y audit population is
deliberately distinct from the scenario scope and cannot establish its inputs.
The example documentation states the constant-source assumptions and the
difference between a possible re-entry and an actual positive sampled count.

## Accepted Phase 6B Step 5 implementation

P6B-D07 connects explicit configuration and CLI requests to the accepted
T1/T5 experiment coordinator. PR-010 declaration eligibility uses input-only
checks aligned with the executable state, mass, parameter and aggregate limits.
PR-011 requires explicit distributions, models, scope, representation, meaning
and seed. Audit records never supply or imply a scenario probability vector.
PR-016 preserves every declaration through serialization and normalized hashing
and binds the run seed to sampled evidence. PR-014/PR-015 preserve independent
audit results and safe diagnostics when a scenario fails.

`validate` never executes a scenario, including when configuration requests one.
Eligibility remains deferred until separately supplied execution evidence exists.
Tests in `test_scenario_config.py` and `test_scenario_cli.py` exercise activation,
input isolation, literal-state boundaries, replay, explicit scope and privacy.
No formula or numerical owner changes in this step; F-016 and empirical
intervention effects remain excluded.

## Accepted Phase 6B Step 4 implementation

PR-012/PR-013 report integration exposes the existing T5 simulation owner in
schema 1.3 under `simulations.external_reopening`. T1/F-015 remains confined to
the distinct closed analytic baseline. Report assembly and canonical validation
bind supplied requests, parameters, probability corrections, sampled paths,
transition sources, events and comparisons. Composite event identities retain
recurrence; reachable states remain possibilities until a positive sample count
is supplied. No report layer executes a mathematical kernel or random generator.

PR-014 retains unavailable empirical intervention effects even when simulation
execution completes. PR-015 protects new state, scope and caller-text paths
without changing numerical evidence or alignment. JSON preserves complete
bounded evidence; Markdown summarizes trajectories and limits detail tables
with truthful omission counts. External-reference loss F-016 remains unregistered.

## Accepted Phase 6B Step 3 implementation

`run_scenario_experiment` implements P6B-D04/D05 under PR-011/PR-016: explicit
selection, shared declarations, aggregate admission and independently reset seeds.
It reuses the accepted T1/F-015 analytic API only for a selected closed model,
passing that model's sampled effective initial vector and labeling the baseline
basis. A reopened path never acquires a closed multi-step expectation. Comparison
rows contain both realized support/diversity values and reopened-minus-closed
differences; they make no pooled statistical or causal claim. Closed transition
losses reuse Definitions 12.10, while initial reachability is explicitly a
pre-first-draw possibility. `test_scenario_experiment.py` verifies this binding,
selection/replay, correction basis, exact events and refusal before sampling.

T5 / TM-M07 / F-017 is implemented in `metrics/resampling.py` by
`mix_external_input` and `simulate_reopened_resampling`, under approved UD-017
and P6B-D01/D02/D03/D05. The external vector and weight remain constant and
explicit; identical declared state spaces may have different positive supports.
Re-entry follows Definitions 13.6 exactly, while local extinction events follow
Definitions 12.10. Recurrent events retain replicate, step and state identity.

All new results and metadata retain experimental simulation evidence. Mixture
metadata identifies F-017; sampled frequencies/support/diversity reuse
F-001/F-002/F-003 under T5. The reopened result has no F-015 multi-step expectation.
PR-016 governs canonical state order, named PCG64, explicit schedules and same-
environment replay. Disclosed bounded normalization preserves supplied/effective
vectors; underflow cannot silently erase positive source reachability.

`test_T5_reopening.py` connects the independent rational fixtures to actual
mixtures, scripted possible transitions and real RNG path invariants. It also
protects integer-mass lambda-zero replay, per-step external refresh, event
recurrence, numerical/refusal boundaries and input isolation. The existing
T1 and schema/eligibility neighbors remain active. F-016 external-reference loss,
empirical intervention effects and T5 public report fields remain outside this
step. Frozen root specifications are unchanged.

## Accepted Phase 6A implementation

Development version `0.1.0.dev5` implements the approved
[longitudinal contract](longitudinal_contract.md) while preserving the existing
theory map, formula IDs and Phase 3-5 owner meanings. The frozen root
`THEORY_TO_CODE_TRACEABILITY.md` remains unchanged. The following additive index
connects series behavior to its existing mathematical or product basis. Detailed
public field inventories appear in longitudinal contract sections 4.3-4.4 and
[the schema registry](report_schema.md).

| Series family / report path | Existing definition, owner and implementation | Evidence, denominator and limit | Independent verification |
|---|---|---|---|
| `configuration.longitudinal`, input snapshot/pair/basis/scope descriptors | PR-007, PR-011 and approved P6A-D01/D02/D06; selection in `metrics/longitudinal.py`, declarations in `config.py` | Product metadata; explicit chronology and compatible representations; context excluded from selected membership | `test_longitudinal_selection.py`, `test_longitudinal_config.py`, `test_longitudinal_cli.py` |
| `observed_facts.longitudinal.snapshots`: population, representation and provenance counts/coverage | PR-002, PR-004, PR-005, PR-011; existing representation/provenance owners via the coordinator | Existing observed evidence; full selected population N, independent of representation exclusions; missing rows remain separate | `test_longitudinal_analysis.py`, `test_longitudinal_provenance.py`, `test_longitudinal_shared_inputs.py` |
| `derived_metrics.longitudinal.snapshots`: support, diversity and source shares | T1 F-002/F-003 and PR-005 F-007; existing diversity/provenance owners | Derived metrics; declared representation for distributions; five source shares plus separate missing-provenance share | `test_longitudinal_analysis.py`, `test_longitudinal_provenance.py` |
| Snapshot direct/lineage closure bounds and widths | T3 F-009/F-010 and approved Phase 5 G/C/U interval; `metrics/bounds.py` | Derived conservative intervals; retain each target's N and unknown evidence; no inferred midpoint or confidence discount | `test_longitudinal_provenance.py`, `test_longitudinal_lineage.py` |
| Snapshot target-supported roots, HHI and effective root count | T4 F-012/F-013; `lineage/ancestry.py` selected-target summaries | Derived supplied-graph evidence; union of target supporting roots, incidence over N and fractional concentration over G; G=0 concentration unavailable | `test_selected_primary_lineage.py`, `test_longitudinal_lineage.py`, `test_selected_lineage_handoff.py` |
| `observed_facts.longitudinal.shared_lineage` and declared/resolved/unresolved reference counts | PR-008, PR-009, T6; existing graph/cycle/ancestry owners | Supplied retrospective graph facts; declaration-entry coverage stays distinct from unique edges and ancestry coverage | `test_selected_lineage_handoff.py`, `test_longitudinal_adversarial.py`, `test_longitudinal_shared_structure.py` |
| Comparison signed deltas | T1 support F-005; other signed changes F-018 with inherited T1/T3/T4 or PR owner; `metrics/longitudinal.py` | Derived later-minus-earlier differences in endpoint units; two scopes, denominators, coverages and reason lists retained | `test_longitudinal_analysis.py`, `test_longitudinal_provenance.py`, `test_longitudinal_lineage.py` |
| Observed lost/added/retained sets and support retention | T1; Definitions 7.9-7.12, F-006; `metrics/diversity.py` | Exact pair sets and earlier-positive-support retention; observed later absence can be followed by reappearance | Frozen `cases.json` / `hero_expected.json`, `test_longitudinal_analysis.py` |
| Earlier-tail disappearance | T2 accepted tail rules and T1 pair sets; `metrics/tail.py` through the coordinator | Derived observed disappearance from the earlier harmonized tail; no F-014 simulation is executed | `test_longitudinal_analysis.py` including asymmetric earlier/later-tail cases |
| Schema 1.2, safe series views, status and failure handoffs | PR-012 through PR-016, PR-018; `result.py`, report/CLI owners | Preserve five evidence classes, null reasons, exact aggregate counts and scope/basis references through hash/omit; partial useful evidence survives | `test_longitudinal_report_contract.py`, `test_longitudinal_handoff.py`, `test_longitudinal_failure.py`, `test_longitudinal_reports.py`, `test_longitudinal_installed.py` |

The frozen three-version oracle has support 3, 2, 3 with intermediate
disappearance and later reappearance. Hero retains supports 8 and 5, diversity
7/8 and 3/4, direct closure change +1/2, supporting roots 8 and 5, HHI 1/8 and
1/4, and effective roots 8 and 4. Coverage and lineage variants preserve each
snapshot's own N and G. Expected rational values, state sets and classifications
were authored independently of the coordinator.

[Step 8](../PHASE_6A_STEP_8.md) records eight detected concrete mutations:
reversed deltas, lexical chronology, context in N, missing provenance folded
into unknown, later-tail selection, incompatible-pair acceptance,
unavailable-to-zero substitution and all-loaded roots replacing target roots.
Five stopped at typed semantic guards, one at a chronology guard and two at
direct assertions. This finite experiment does not establish exhaustive fault
coverage. Bounded resource/detail cases verify admission before calculation,
100-row display caps after exact aggregation and shared budgets without reset.

No new theory equation, formula identifier, universal score or empirical causal
inference is introduced. Model-performance decline, causal ancestor effect and
permanent extinction remain unsupported. New series orchestration executes no
simulation; Phase 6B uses its separately authorized pure APIs above. Actual candidate environments,
installed evidence and scale measurements are identified in
[Phase 6A completion](../PHASE_6A_COMPLETION.md).

## Historical Phase 5 implementation

Development version `0.1.0.dev4` implements the approved [lineage contract](lineage_contract.md)
and preserves the existing mathematical definitions and direct calculations.

| Owner | Current implementation | Independent behavioral coverage |
|---|---|---|
| PR-008 | Retained immediate-parent evidence and canonical graph adjacency with target/context isolation | Parent batch, graph and context-input suites; missing, ambiguous, future, duplicate and malformed references |
| T6 | Iterative cyclic-component detection and affected-path propagation | Self-cycle, multi-node SCC, disjoint components, bounded witnesses and unaffected branches |
| PR-009 | Structural depth in `lineage/cycles.py`; generation remains separate in input validation | Same-version chains, missing/unknown inputs, cycles, grounded resets and declaration mismatch |
| T4 | Strict external ancestry, G/C/U, root incidence, fractional mass, HHI and effective roots | Frozen Hero and hand-authored partial/carryover/diamond/all-closed/all-unresolved oracles |
| T3 | Explicit lineage closure bounds from the full target partition | Rational interval, unavailable and denominator cases alongside preserved direct bounds |
| PR-012, PR-013, PR-015, PR-016 | Schema 1.1, evidence metadata, privacy and deterministic lineage reporting | Typed/wire semantic negatives, forged/stale results, standard/redacted output and input permutation cases |
| PR-011 and package boundary | Explicit CLI dispatch, context formats, installed ordinary/lineage Hero | Context isolation, input-only validation, clean installs and real optional Parquet |

The Hero's eight v2 targets resolve to five external roots, HHI 1/4, effective
roots 4 and lineage bounds [0,0], while direct bounds remain [1/2,1/2]. The partial
oracle fixes N/G/C/U at 4/2/1/1, incidence 2 and 1, fractional masses 3/2 and 1/2,
HHI 5/8, effective roots 8/5 and lineage bounds [1/4,1/2]. These expectations were
specified independently of production calculations. Root incidence uses N;
fractional concentration normalizes over G. No confidence discount is introduced.

Seven bounded Step 9 mutations were detected by current tests, covering wrong
denominators, duplicate memberships, carryover roots, unknown-state propagation,
cycle propagation, interval order and HHI inversion. [Step 9](../PHASE_5_STEP_9.md)
records those experiments; [completion](../PHASE_5_COMPLETION.md) records the
candidate. No new theorem, formula identifier, calibrated risk score, Phase 6A
longitudinal orchestration or Phase 6B reopening is claimed.

The sections below retain historical implementation explanations. Current checks
protect owner/layer boundaries and current behavior; they no longer require
historical test-body or source-binding migrations to execute. Frozen specifications
and mathematical/Hero expectations remain unchanged.

Historical Phase 3 status: mathematical development milestone. Final acceptance is recorded in the three Phase 3 milestone reports.

The controlling maps are:

- `THEORY_SOURCE_MAP.md`
- `THEORY_TO_CODE_TRACEABILITY.md`

Every Python module identifies its Trace IDs or Product Rule IDs in its docstring. The step records retain their historical boundaries; the final field index describes the complete approved Phase 3 subset. Some frozen runtime docstrings retain earlier-step statements; current ownership and implementation are established by this index, exact source gates and executed tests.


## Phase 3 Step 3 implemented trace

| Owner | Implemented basis | Authoritative definition | Evidence |
|---|---|---|---|
| PR-006 | exact_utf8_v1 decoded text bytes and SHA-256 | P3-D05; DEFINITIONS_AND_UNITS 6.10 and 20.2 | record-form identity only |
| PR-006 | duplicate_record_count, sum of group size minus one | DEFINITIONS_AND_UNITS 8.3; THEORY_TO_CODE_TRACEABILITY 17 | observed_fact, records |
| PR-006 | duplicate_group_count, groups of size greater than one | DEFINITIONS_AND_UNITS 8.4; THEORY_TO_CODE_TRACEABILITY 17 | observed_fact, groups |
| T1 supporting basis | immutable exact-content state assignments | PHASE_3_PLAN Step 3 | no support/diversity calculation |
| PR-016 supporting basis | canonical members and sorted digest groups | PHASE_3_PLAN 5.3 | deterministic ordering |

The PR-006 placeholder test keeps its original node ID but now checks the exact
implemented boundary. Tests cover known hashes, transformations that must remain
absent, exact grouping, source preservation, explicit payload selection, collisions,
private repr, unavailable versus zero, and rejection of premature capabilities.
No new F-number, theorem, entropy measure or semantic-support claim is introduced.
Report redaction remains a separate unimplemented PR-015/Phase 4 responsibility.

## Phase 3 Step 4 traceability

| Output | Owner and source | Computation |
|---|---|---|
| state_count | T1; Definitions 7.1 | Integer count of included assignments, or explicitly supplied aggregate |
| state_frequency | T1; F-001; Definitions 7.3 | State count divided by the included-record denominator |
| support_size | T1; F-002; Definitions 7.4-7.6 | Number of strictly positive frequency components |
| gini_simpson_diversity | T1; F-003; Definitions 9.2 | One minus sum of squared frequencies |
| simpson_concentration | T1; F-004; Definitions 9.3 | Sum of squared frequencies, without ancestry interpretation |
| Explicit weighted companions | T1; UD-021; Definitions 9.5 and 19 | State weight mass divided by total included weight; unweighted output preserved |

The supplied-vector entry point does not apply F-001 or fabricate record counts.
The vector's empirical relationship to its named scope remains caller-declared.
Calculated scalar fields use derived_metric evidence; supplied vectors and
integer record counts are labelled observed facts under their declared method.
Probability acceptance uses P3-D07 with no clipping or normalization.

Tests consume unchanged F001/F002 hand cases and frozen F003-A through F003-D.
Additional rational, weighting, zero-state, invalid-input and metamorphic cases
verify implementation behavior without extending the theory. Record-form
support remains representation-specific. Distributional concentration alone
never establishes functional failure or semantic completeness.

## Phase 3 Step 5 traceability

| Output | Owner and basis | Evidence and unit | Validation |
|---|---|---|---|
| Source counts | PR-005; Definitions 11.1 | observed_fact, records | Rational partial fixture and missing/unknown separation |
| Source shares | PR-005; F-007 | derived_metric, ratio over full selected scope | Exact rational values and denominator reconciliation |
| Confidence counts | PR-004; Definitions 3.3 | observed_fact, records | Missing field cases and no confidence discount |
| Missing-row count/share | PR-004; Definitions 11.4 | observed count, derived ratio | Absence versus declared unknown |
| Row/required/grounding coverage | PR-004; F-008 and Definitions 3.10-3.12 | Retained validation facts, named ratios | Reconciliation and forged-evidence rejection |
| Source/confidence field coverage | PR-004; Definitions 3.13 | observed_fact, ratio | Incomplete matched fields |
| Direct open/closed/unresolved counts | T3; Definitions 3.7-3.9; P3-D08 | observed_fact, records; toolkit_operationalization | Source/grounding/review/confidence cross-products |
| Weighted source and missing masses/shares | PR-005; F-007 weighted variant; Definitions 19 | derived_metric, weight mass or ratio | Independent rational fixture, scaling and invalid-weight tests |

Every numeric scalar/table carries scope, denominator basis, unit, method, owner,
evidence class and defined formula identifier where applicable. Confidence does
not become a truth score, source counts do not certify independence, and review
never replaces grounding. Required-field-incomplete provenance stays unresolved
in the direct partition while original grounding-field coverage retains its own
meaning. No closure interval, ancestry concentration, effective roots or report
is introduced. The original frozen Phase 3 mathematical oracles remain unchanged.


## Phase 3 Step 6: direct closure-exposure interval

`metrics/bounds.py` now exposes explicit pure `closure_exposure_bounds(...)` and
`direct_closure_exposure(...)`. Both use the full unweighted single-version scope.
T3 F-009 = C/N, F-010 = (C+U)/N, width = U/N. Results are derived metrics labeled
`toolkit_operationalization`, not a lineage measure or a universal risk score.

The dataset adapter consumes Step 5 results, preserves input errors and independent
coverage/confidence disclosure, and rejects inconsistent partitions or altered
availability summaries. No usable required provenance means unavailable dataset
scalars; valid explicit unknown grounding can support [0,1]. No confidence weighting,
midpoint, graph, file access, or automatic input-pipeline invocation is introduced.
All later-stage boundaries and immutable earlier implementations remain.

## Phase 3 Step 7: T2 direct implementation mapping

| Output | Basis | Unit / evidence | Tests |
|---|---|---|---|
| tail_membership | Definitions 10.1-10.3; P3-D06 four explicit rules | state set / derived_metric | T2 rule, threshold, absent-state, positive-support cases |
| tail_support_size | Definitions 10.4; selected positive-state cardinality | states / derived_metric | T2 empty/nonempty tails and fixture |
| tail_record_share | Definitions 10.5; selected counts / included record total | ratio / derived_metric | T2 rational, replication, exclusion cases |
| rarity_rank | Definitions 10.6; frequency/count/Unicode, 1-based ordinal | ordinal_rank / derived_metric | T2 tie and permutation cases |
| one_step_extinction_probability | F-014; Definitions 10.7; Validation 15 | probability / simulation | T2 exact rationals, endpoints, monotonicity, tiny-p and underflow cases |

Every output retains representation, scope, rule or model assumptions and limits.
Scenario n is explicit; horizon is one; analytic evaluation draws no random sample.
The selected-state marginal is disclosed without claiming a complete empirical
probability vector. Count/frequency metadata in ranking entries remains the Step 4
basis. Numeric underflow is disclosed separately from the exact zero endpoint.
No calibrated failure forecast, tail severity narrative, reopening or temporal
workflow is supplied. Original input validation continues to call no metric.

## Phase 3 Step 8 traceability

T1 F-015: `expected_diversity_after_steps` evaluates D0*(1-1/n)**t under the
fixed finite closed multinomial model. T1's sampled counterpart is
`simulate_closed_resampling`, implemented by sequential conditional binomials.
All output evidence is simulation, including sampled counts and support, with
method/parameter/representation/scope records. P3-D07 permits only disclosed
within-tolerance sampler correction. PR-016 governs canonical state order,
explicit PCG64 seed, replicate schedule and same-environment repeatability.
T2 remains in tail.py; T5 is reserved and unimplemented. Source authority is
unchanged. Tests in test_T1_resampling.py use frozen rational expectations,
finite enumeration and distributional checks independent of implementation.

## Phase 3 Step 9 traceability

T1 now includes the explicitly selected ordered pair kernel in
`metrics/diversity.py::compare_support`: F-005 support delta, F-006 support
retention and F-018 Gini-Simpson diversity delta, plus Definitions 7.9-7.12
loss/addition counts and state sets. PR-007 ordering evidence is revalidated by the
existing input validator; PR-011 compatibility checks live in
`representations/compatibility.py::validate_representation_compatibility`.
P3-D03 restricts these computations to one explicitly supplied pair. Phase 6A
automatic longitudinal orchestration remains deferred.

The comparison basis includes representation identity, rule, missing policy and
explicit state semantics. A many-to-one map changes that basis; original results,
exact directed mapping and collapsed groups remain visible. The derived results
make no lineage, causal, model-performance or permanent process-extinction claim.
Tests use the frozen HERO-PAIR oracle and independent rational fixtures. Existing
F-001 through F-004 source definitions and their numerical tests remain unchanged.

## Phase 3 Step 10 integration and mathematical evidence

The frozen `phase3_math_cases.json` and its source notes retain their original
bytes. `test_phase3_math.py` explicitly executes all twenty source-indexed cases,
including Hero single-version, F-005/F-006/F-018 pair values and the separately
invoked F-014/F-015 scenarios. Inherited mathematical unit tests remain intact.
The test-only pipeline preserves observed facts, derived metrics, simulation
labels, confidence/missingness, denominators and original validation errors.

The 100000-record performance oracle is independently determined by its documented
synthetic construction (100 equal topic states, 1000 repeated forms, two equal
source classes). Timing and traced allocations are engineering observations only.
No new entropy, quality, integrity, lineage or universal failure score is added.

## Phase 3 final field index

This index complements the historical step records above. `Definitions` refers to the unchanged `DEFINITIONS_AND_UNITS.md`; formula IDs refer to `THEORY_TO_CODE_TRACEABILITY.md`. Every scalar's `CalculationMetadata` carries its owner, formula or product-only method, units, scope/denominator, evidence, representation where applicable, assumptions and limits. Table/path values retain the corresponding table or trajectory metadata. All objects remain internal Python results; Phase 4 report fields and serialization remain deferred.

### Representation, counts and distribution

| Field(s) | Definition / owner / module | Unit and evidence | Tests and limit |
|---|---|---|---|
| `selected_count`, `included_count`, `excluded_count`; coverage numerator/denominator/ratio | P3-D06; Definitions 6; T1 supporting / representations/base, field | records and observed coverage ratio over selected valid records | `test_T1_representation.py`; declared literal states, no semantic certification |
| Exact-content assignments, duplicate group membership and group `record_count` | P3-D05; Definitions 6.10, 20.2; PR-006 / representations/content_hash | deterministic record-form identity and exact group cardinality / observed_fact | `test_PR006_duplicates.py`, `test_T1_representation.py`; hashes are linkable, paths are not content |
| `duplicate_record_count` | Definitions 8.3; PR-006 / metrics/duplicates; sum(group size - 1) | records / observed_fact | `test_PR006_duplicates.py`; no deduplication or semantic equivalence |
| `duplicate_group_count` | Definitions 8.4; PR-006 / metrics/duplicates | groups / observed_fact | Same tests; exact groups of at least two |
| `analyzed_record_count`, `state_count` | Definitions 7.1; T1 / metrics/diversity | records / observed_fact | `test_T1_support.py`, `test_T1_diversity.py`; probability-only inputs do not invent state counts |
| `state_mass`, weighted `frequency_denominator` | Definitions 19, UD-021; T1 / metrics/diversity | explicit weight mass / derived_metric | Same tests; supplied nonnegative weights, preserved unweighted values |
| `state_frequency`, unweighted `frequency_denominator` | F-001; Definitions 7.3; T1 / metrics/diversity | ratio over included count or explicit weight mass / derived_metric | Same tests and F001-A; explicit vector mode retains supplied observations without pretending F-001 counted records |
| `support`, `support_size` | F-002; Definitions 7.4-7.6; T1 / metrics/diversity | positive-mass states and cardinality / derived_metric | `test_T1_support.py`, frozen F002 cases; representation-specific |
| `gini_simpson_diversity` | F-003; Definitions 9.2; T1 / metrics/diversity | dimensionless, 1 - sum(p²) / derived_metric | `test_T1_diversity.py`, F003-A through D; no functional-failure claim |
| `simpson_concentration` | F-004; Definitions 9.3; T1 / metrics/diversity | dimensionless, sum(p²) / derived_metric | Same unit tests; distributional concentration only |
| `supplied_probability_total`, `probability_residual` | P3-D07; T1/PR-016 / metrics/diversity | mass and total-minus-one / numerical input diagnostics | Probability/roundoff tests in `test_T1_support.py`; no clipping or repair |

### Provenance and direct exposure

| Field(s) | Definition / owner / module | Unit and evidence | Tests and limit |
|---|---|---|---|
| `analyzed_record_count`, `records_with_matching_rows`, `missing_provenance_count` | Definitions 11.4; PR-004 / metrics/provenance | records / observed_fact | `test_PR004_coverage.py`; full selected scope, missing distinct from unknown |
| `missing_provenance_share` | Definitions 11.4; PR-004 / metrics/provenance | missing rows / full selected records / derived_metric | Same tests; no invented source bucket |
| `source.counts`, `source.shares` | Definitions 11.1, F-007; PR-005 / metrics/provenance | records / observed_fact; ratios / derived_metric | `test_PR005_source_shares.py`; five exact declared source categories |
| `confidence.counts` | Definitions 3.3; PR-004 / metrics/provenance | records / observed_fact | `test_T3_provenance.py`; no confidence-share metric, trust score or discount |
| Row, required-field and grounding coverage numerator/denominator/ratio | F-008; Definitions 3.10-3.12; PR-004 / preserved validation and metrics/provenance | records and observed coverage ratios | `test_PR004_coverage.py`, `test_T3_provenance.py`; three distinct evidence bases |
| Source/confidence field coverage numerator/denominator/ratio | Definitions 3.13; PR-004 / metrics/provenance | records and observed coverage ratios | Same tests; incomplete matched fields remain unavailable |
| `known_open_count`, `known_closed_count`, `unresolved_grounding_count` | Definitions 3.7-3.9; P3-D08; T3 / metrics/provenance | records / observed_fact under toolkit_operationalization | `test_T3_provenance.py`; declarations do not prove external truth/independence |
| `weighted_source_type_masses`, `total_weight`, `missing_provenance_weight` | Definitions 19, UD-021; PR-005 / metrics/provenance | weight mass / derived_metric | `test_PR005_source_shares.py`; declared weights, no confidence weighting |
| `weighted_source_type_shares`, `weighted_missing_provenance_share` | Weighted F-007 variant; PR-005 / metrics/provenance | ratio over all selected weight / derived_metric | Same tests; full weight denominator, distinct missingness |
| Bounds `denominator` and retained partition counts | Definitions 3.7-3.9, 11.4; T3 / metrics/bounds | records / retained observed basis | `test_T3_bounds.py`; one unweighted full selected scope |
| `lower_bound`, `upper_bound`, `interval_width` | F-009 C/N; F-010 (C+U)/N; width U/N; T3 / metrics/bounds | ratios / derived_metric, toolkit_operationalization | `test_T3_bounds.py`, DIRECT-A, Hero; direct evidence only, no lineage or universal risk |
| Bounds coverage/confidence counts and errors | Same PR-004 basis above, retained by T3 adapter | unchanged observed evidence | `test_T3_bounds.py`; missingness/errors cannot be erased by the interval |

### Tail and closed model

| Field(s) | Definition / owner / module | Unit and evidence | Tests and limit |
|---|---|---|---|
| Tail denominator and ranking `state_count`, `state_frequency` | F-001 and Definitions 10; T2 / metrics/tail, retained T1 basis | records / observed_fact; ratios / derived_metric | `test_T2_tail.py`; unweighted count-backed input only |
| `tail_membership`, `tail_support_size` | Definitions 10.1-10.4, P3-D06; T2 / metrics/tail | state set/cardinality / derived_metric | Same tests; four explicit rules, positive states only |
| `tail_record_share` | Definitions 10.5; T2 / metrics/tail | selected counts / included record count / derived_metric | Same tests; no quantile/weighted-tail invention |
| `rarity_rank` | Definitions 10.6; T2 / metrics/tail | 1-based ordinal / derived_metric | Same tests; frequency, count, Unicode tie order |
| `one_step_extinction_probability` | F-014, Definitions 10.7; T2 / metrics/tail | probability / simulation, analytic_extinction | Same tests, frozen F014/Hero cases; closed multinomial assumption, explicit p and n |
| `initial_gini_simpson_diversity`, `contraction_factor`, `expected_diversity` | F-003 and F-015, Definitions 12.1-12.5; T1 / metrics/resampling | ratios / simulation, analytic_expectation | `test_T1_resampling.py`, frozen F015/Hero cases; fixed n and explicit horizon, no seed |
| Sampled `state_counts`, `state_frequencies` | Finite multinomial model and F-001; T1 / metrics/resampling | sampled records / simulation; ratios / simulation | Same tests; counts total n at t>0; initial counts absent |
| Sampled `support`, `support_size`, `gini_simpson_diversity` | F-002/F-003 applied to sampled path; T1 / metrics/resampling | states/cardinality/ratio / simulation | Same tests; scenario trajectories retain simulation classification |
| `step`, `replicate_index`, n, horizon, replicates and seed | Definitions 12; P3-D02/P3-D07; T1/PR-016 / metrics/resampling | explicit integer indices/parameters | Same tests and `test_PR016_determinism.py`; local PCG64, schedule/version retained |
| Supplied/effective vectors and totals, residual, divisor, corrections | P3-D07; T1/PR-016 / metrics/resampling | numerical execution diagnostics, not empirical metrics | Roundoff tests in `test_T1_resampling.py`; sampled-only correction within 1e-12, positive support preserved |
| `numerical_underflow`, `numerical_underflow_steps` | P3-D07; T2/T1 / tail, resampling | bool / step indices, numerical diagnostics | Underflow tests in the same modules; distinguishes numeric zero from model absorption |

The sampler's independent checks include exact finite multinomial enumeration, n=1 absorption, absorbing/extinct states, count conservation, seed determinism, input permutation and a predeclared Monte Carlo check: p=(1/2,1/2), n=4, t=1..3, 8000 replicates, seed 812, absolute mean-diversity tolerance 0.025. Expected values use rational (1/2)(3/4)^t, independent of the implementation. Fixed-seed outcomes are checked within each recorded environment; cross-version NumPy path identity is not required.

### Explicit pair and metadata

| Field(s) | Definition / owner / module | Unit and evidence | Tests and limit |
|---|---|---|---|
| `support_delta` | F-005; T1 / metrics/diversity | later support minus earlier support, states / derived_metric | `test_T1_support.py`, `test_T1_compatibility.py`, HERO-PAIR |
| `support_loss_count`, `support_added_count`; extinct/added/retained state sets | Definitions 7.9-7.12; T1 / metrics/diversity | cardinalities/state sets / derived_metric | Same tests; observed/supplied pair only, no permanent extinction inference |
| `support_retention_ratio`, `retention_denominator` | F-006; T1 / metrics/diversity | intersection / earlier positive support; states denominator / derived basis | Same tests; common harmonized representation |
| `gini_simpson_diversity_delta` | F-018; T1 / metrics/diversity | dimensionless, later D minus earlier D / derived_metric | `test_T1_diversity.py`, HERO-PAIR; compatible weighting and scope families |
| Original/harmonized distribution fields | F-001 through F-004 as indexed above; T1 | retained original or explicitly aggregated derived basis | `test_T1_compatibility.py`; complete directed maps only |
| `mapping_effect` support sizes, `collision_groups`, map direction and state semantics | P3-D03, Definitions 6/7; PR-011 / representations/compatibility; T1 / diversity | disclosed transformation diagnostics | Same tests; cannot recover distinctions collapsed by a map |
| Units, methods, evidence, status, reasons, assumptions, representation, scope and weighting | Definitions 6/19; approved Step 1 contracts; PR-016 supporting / models and result owners | metadata, no additional numerical claim | `test_phase3_contracts.py`, each family above; unavailable scalars carry None, not invented zero |

F-001 through F-010, F-014/F-015 and F-018 cover this approved subset. F-011 through F-013 ancestry-related work and F-016 external-reference loss and F-017 reopening work remain unimplemented. T4/T6, lineage bounds, T5, public report/CLI fields and complete temporal workflows retain their separate phase gates. Twenty frozen cases run without changing their JSON/source-note bytes. The final integration runner also checks evidence labels, scope separation and fail-on-call input-only behavior. No universal integrity, entropy, collapse or causal-failure score is introduced.

## Phase 4 Step 1: preserved mathematical and ownership baseline

The Phase 4 governance baseline is accepted Phase 3 commit
`e3ffb8c0a88bfe31f669f9662d9b5213da628b3a`. Step 1 preserves the complete
Phase 3 field index above, owner IDs, evidence classifications, formula
transcriptions, units, unavailable-value rules and approved numerical tolerances.
All forty package modules, twenty mathematical oracle cases, canonical Hero
inputs and sixteen Phase 0 authority documents remain protected by their pinned
identities. The approved plan adds product and verification decisions without
adding mathematical fields, formulas or interpretations of the theory papers.

| Step 1 control | Traceability effect | Evidence boundary |
|---|---|---|
| Approved plan and P4-D01 through P4-D11 | Record authorized future report/CLI design | Approval does not establish implementation or empirical theory validation |
| Frozen Phase 3 source and test identities | Preserve accepted analytical definitions and inherited test nodes | Historical assertions run against their explicitly named snapshot |
| Explicit Phase 4 checker dispatch | Validate current governance before unchanged mathematical AST checks | Step 1 cannot authorize new report behavior or relax old formula guards |
| Exact migration and path permissions | Bound maintenance to listed source-binding changes and approved files | Protected source/oracle changes and forged scope expansion are rejected |

The public report path registry and canonical result envelopes are scheduled for
Step 2. No public report field, serializer, redaction claim, new primary owner or
scientific measurement is established by this Step 1 checkpoint. Subsequent
steps must map every analytical field to its existing calculation basis and
preserve assumptions and limitations under the approved plan.


## Phase 4 Step 2: field and evidence contract

`result.py` activates PR-012, PR-013 and PR-014 for canonical report contracts
only. PR-015/PR-016 metadata fields record the declared reporting contract without
implementing privacy transforms or later orchestration. `docs/report_schema.md`
is the detailed typed public-field registry, preserving the approved paths from
`THEORY_TO_CODE_TRACEABILITY.md` sections 30 through 37 and registering explicitly
bounded companions of already accepted Phase 3 results.

Every analytical field has one evidence class, a status, unit/type, method or
product rule, owner and trace identifiers, scope, representation when applicable,
coverage/denominator, assumptions and limitations. Metadata retains product
ownership without becoming a scientific measurement. The provenance coverage
fields keep their approved `observed_facts.provenance.*` registry locations.

Input capability assessment and actual execution status remain distinct.
Level 4 input eligibility does not imply that deferred lineage computation ran.
Zero is a measured value; unavailable values retain explicit nulls and reasons.
Proxy triggers and scenario model declarations retain their own evidence classes.
The schema can describe future registered fields without authorizing the current
phase to calculate them. Unregistered public results are rejected.

No new formula, interpretation of the supplied theory papers, causal claim,
universal score or functional-failure diagnosis is introduced. Original numerical
expectations, authority records and all calculation bodies remain fixed.


## Phase 4 Step 3 assembly ownership

PR-012 owns evidence placement; PR-014 owns bounded unavailable conclusions
and actionable metadata recommendations; PR-018 owns the distinction between
measurements, declared assumptions, proxies and prohibited stronger conclusions.
The assembly adapters preserve the existing T, PR and F owners of their supplied
results. A proxy does not acquire the authority of its numerical basis.

The frozen Step 2 registry controls every public analytical path. Missing
provenance rows remain distinct from explicit unknown declarations, and
representation exclusions never shrink provenance denominators. Weighted
companions retain their weight basis. Supplied analytic or sampled scenarios
retain their model, method, parameters and original numerical values under
simulations. No adapter creates a new formula or infers model performance,
source independence, causal ancestry, production failure or universal integrity.

Phase 5 lineage conclusions stay deferred even when the accepted Phase 2 input
assessment reaches Level 4. Validation and assembly do not certify empirical
truth or prove that arbitrary caller-supplied objects came from a trusted run.
The actual Step 3 authorization, preservation rules and verification evidence
are recorded in the Phase 4 control files and the external step receipt.

## Phase 4 Step 4 privacy and diagnostic ownership

| Existing owner | Step 4 responsibility | Preserved boundary |
|---|---|---|
| PR-015 | Standard/redacted views, HMAC pseudonyms, record-ID modes and safe diagnostics | No raw content, notes, embeddings or secret material in selected output |
| PR-016 | Explicit safe run/configuration metadata and deterministic fixed-context transformations | Fresh default secrets intentionally separate runs; no metric recomputation |
| PR-012/PR-013/PR-014 | Safe immutable report views preserve evidence placement, availability and null meaning | Frozen field registry, root schema, evidence classes and aggregate values |
| Existing T1-T6/PR/F field owners | Values and denominator/scope semantics already supplied to the report | Privacy transformation creates no mathematical, causal or empirical conclusion |

The report privacy stage changes disclosure after accepted calculation and
assembly. A protected identifier denotes the same report entity within its
explicit context. Omitted identity-bearing details are disclosed as redaction,
not as missing source evidence. Error severity, evidence classes, aggregate
numeric values and availability remain unchanged. No calculation owner or
input parser executes during the installed privacy-transformation check.

Safe option summaries and sanitized diagnostics are operational product rules.
They do not add a theory equation, empirical authenticity guarantee, general
anonymity claim, network monitor or statistical privacy bound. The declared
network count concerns toolkit-managed operations; blocked network execution
checks provide separate evidence. User approval for Step 4 is the contextual
instruction `继续` following accepted Step 3; the approved Phase 4 plan remains
byte-frozen.

## Phase 4 Step 5 renderer ownership

| Existing owner | Renderer responsibility | Preserved evidence boundary |
|---|---|---|
| PR-013 | Validated JSON and twelve-section Markdown output | Frozen schema and field registry; no new analytical path |
| PR-016 | Stable section and mapping order, retained arrays and finite numeric representation | Supplied numerical values and upstream sequence semantics remain unchanged |
| PR-018 | Visible statuses, null reasons, evidence legend and literal-safe caller labels | No stronger conclusion, executable markup or caller-authored toolkit assertion |
| PR-015 | Render only an explicitly selected `SafeReportView` | Rendering does not replace privacy selection or provide statistical anonymity |
| PR-012/PR-014 and existing T/PR/F field owners | Retain classifications, scopes, denominators, limitations and unavailable conclusions | Serialization supplies no formula, inferred evidence or independent empirical verification |

The renderers consume the accepted report after its privacy transformation.
Observability remains an input assessment; a Level 4 report may retain deferred
lineage execution. Partial capabilities retain their coverage and reasons.
Supplied scenarios remain experimental simulation evidence, and unavailable
conclusions remain distinct from conclusions established to be false. The
capability compatibility mirror produces one human-readable matrix without
creating a second assessment.

JSON and Markdown retain provided values without thresholding, percentage
conversion, interval midpoint substitution, rounding tiny values to zero or
deriving an additional metric. Markdown quotes dynamic labels as data and
preserves ordinary Unicode while escaping markup and display controls. These
are presentation and product rules; they neither reinterpret the theory papers
nor establish source authenticity, causal ancestry, model performance, universal
integrity or a collapse prediction. The twenty frozen mathematical cases and
their numerical expectations remain the responsibility of their existing
owners.

## Phase 4 Step 6 output boundary

P4-D07 and the privacy/output requirements map to additive publication helpers
in `utils/paths.py` and fixed operational diagnostics in `utils/logging.py`.
PR-015 privacy and the existing PR-017 input/content-reference protections stay
in force. There is no new theory interpretation, formula, empirical inference,
metric recomputation or evidence-class promotion. Existing result, privacy,
JSON/Markdown and mathematical contracts remain unchanged. A publication failure
is an operational outcome and cannot alter the report's analytical conclusions.
The new output-safety test file, current runtime AST checks, preserved helper
checks and isolated installed-wheel smoke exercise this boundary directly.


## Phase 4 Step 7 CLI boundary

P4-D06 maps to `cli.py` call orchestration and additive `config.py` input settings.
PR-013/015/016/018 govern output, privacy, reproducibility and safe diagnostics.
T1 support/diversity, T2 explicit tail selection and T3 provenance/direct bounds
remain calls to their unchanged accepted owners. Explicit exact-content duplicate
analysis remains PR-006 and describes record form only. No new formula, empirical
claim, weighted interpretation or theoretical score is introduced.

Current CLI tests include independently hand-counted support/diversity and direct
bounds, absence of representation fallback, input-only execution with all metric
functions blocked, failed-family evidence retention, safe privacy across sinks,
configuration conflicts and exit precedence. Current AST and immutable historical
bindings prevent scope growth. The installed smoke operates outside the source
checkout with network operations blocked; it does not certify whole-product Hero
performance or Phase 4 completion.


### Phase 4 Step 8 explicit-pair and example wiring

P4-D03/P4-D09 authorize CLI composition only: T1's accepted F-005/F-006/F-018
comparison fields and existing lost/added state sets; PR-013/015/016/018 govern
safe local reports, privacy, determinism and limits. No new formula or report
field is introduced. Independent CLI cases use A,B,C,D versus A,A,B,E: support
delta -1, retention 1/2, diversity delta -1/8, lost C,D and added E. The separate
Hero cases assert the approved plan section 8 targets, not generated goldens.
Every comparison carries declared common representation, literal state meaning,
selected versions and revalidated chronology. Input eligibility stays separate
from performed analysis. Lineage, causal ancestor effects, model decline and
universal conclusions retain their accepted deferred/unavailable classifications.
