# Theory Traceability

Status: Phase 1 scaffold.

The controlling maps are:

- `THEORY_SOURCE_MAP.md`
- `THEORY_TO_CODE_TRACEABILITY.md`

Every Python module identifies its Trace IDs or Product Rule IDs in the module docstring. Phase 1 does not implement the theory-derived formulas.


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
