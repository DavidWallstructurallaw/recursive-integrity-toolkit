# THEORY_TO_CODE_TRACEABILITY

## Document control

| Field | Value |
|---|---|
| Project | Recursive Integrity Toolkit |
| Target release | v0.1 |
| Phase | Phase 0 |
| Status | APPROVED PHASE 0 BASELINE |
| Primary owner | Theory Owner |
| Technical reviewers | Mathematical Reviewer, Technical Maintainer |
| Depends on | `SPEC_AUDIT.md`, `THEORY_SOURCE_MAP.md`, `UNRESOLVED_DECISIONS.md`, `PROJECT_INSTRUCTIONS.md`, `V0.1_PRODUCT_SPEC.md`, `DEFINITIONS_AND_UNITS.md`, `DATA_AND_PROVENANCE_SPEC.md`, `OBSERVABILITY_AND_REPORTING.md` |
| Purpose | Connect every public result to its source basis, mathematical object or product rule, planned code owner, tests, report field, evidence class, observability requirement, and limitation |
| Implementation code authorized | No |

This file is the canonical traceability contract for Recursive Integrity Toolkit v0.1.

It connects:

```text
theory or product basis
-> canonical definition
-> mathematical object or deterministic rule
-> implementation module
-> test
-> public report field
-> evidence class
-> observability requirement
-> limitation
```

No public result may enter v0.1 unless this chain is complete.

A source article can authorize a concept or mathematical object. Product specifications control the exact v0.1 implementation contract. Tests must demonstrate that code follows both.

This file preserves three distinctions:

1. exact theory-derived mathematics,
2. theory-guided toolkit operationalizations,
3. product-only engineering rules.

These categories must remain visible in code headers, tests, reports, and release review.

Definitions or paths marked `APPROVED DECISION` become implementation-authoritative only after the related `UD-*` decision is approved.

---

## 1. Traceability objectives

The traceability system exists to prevent:

- an implementation convention from being presented as a theorem,
- a structural analogy from becoming an identical cross-domain equation,
- a simulation from being reported as an observed production result,
- a proxy signal from becoming a causal claim,
- an unavailable conclusion from disappearing from the report,
- a code module from silently changing a theory term,
- a public report field from lacking test ownership,
- a deferred claim from entering v0.1 through implementation convenience.

The traceability system should allow a reviewer to answer:

- Which source passage supports this result?
- Which definition controls its meaning?
- Which formula or deterministic rule produces it?
- Which module owns the behavior?
- Which tests verify it?
- Which report field exposes it?
- What evidence class applies?
- What observability level is required?
- Which conclusion remains prohibited?

---

## 2. Source classes

Every trace record must use one source class.

### 2.1 `THEORY_EXACT`

The authoritative theory source supplies an exact mathematical object or process that v0.1 can implement under declared assumptions.

Examples:

- finite multinomial resampling,
- Gini-Simpson expected contraction,
- one-step rare-state extinction probability,
- external reopening mixture.

### 2.2 `THEORY_STRUCTURAL`

The theory source supplies a structural interpretation or boundary without a universal operational metric.

Examples:

- closed recursion,
- integrity as external fidelity,
- concentration becoming failure only relative to an unresolved obligation,
- entropy as a structural boundary.

### 2.3 `THEORY_GUIDED_OPERATIONALIZATION`

The theory motivates a toolkit metric, while the exact calculation is created by the product specification.

Examples:

- closure exposure lower and upper bounds,
- fractional external-root allocation,
- ancestry HHI,
- effective external-root count.

These results must carry a note such as:

```text
toolkit_operationalization
```

### 2.4 `PRODUCT_RULE`

The behavior exists because the product needs a safe, deterministic, auditable contract.

Examples:

- composite record keys,
- version-order requirements,
- cycle rejection in the ancestry DAG,
- JSON section order,
- schema-mapping restrictions,
- redaction behavior.

A product rule must not be presented as a theorem from the theory corpus.

### 2.5 `DEFERRED_THEORY`

The theory source contains a relevant concept that lacks an approved v0.1 operational definition.

Examples:

- universal integrity,
- universal presence,
- universal quality,
- universal stability,
- amplification threshold,
- causal ancestor contribution.

Deferred theory may appear in documentation or unavailable conclusions. It must not power public derived metrics.

---

## 3. Identifier namespaces

### 3.1 Theory Trace IDs

The migration package established these primary Trace IDs:

```text
T1
T2
T3
T4
T5
T6
```

Their meanings are frozen in this file.

No new `T*` identifier may be created until a corresponding entry is first approved in `THEORY_SOURCE_MAP.md`.

### 3.2 Theory Map IDs

Use `TM-*` identifiers from `THEORY_SOURCE_MAP.md`.

Examples:

```text
TM-M03
TM-C06
TM-P04
TM-E01
```

### 3.3 Product Rule IDs

This file defines `PR-*` identifiers for product-only behavior.

A `PR-*` identifier:

- does not claim theory authority,
- may own a public observed fact or engineering-derived metric,
- must still have definitions, code, tests, and report fields.

### 3.4 Formula IDs

Use `F-*` identifiers from `DEFINITIONS_AND_UNITS.md`.

### 3.5 Decision IDs

Use `UD-*` identifiers from `UNRESOLVED_DECISIONS.md`.

### 3.6 Error and warning codes

Use canonical error and warning codes from `DATA_AND_PROVENANCE_SPEC.md`.

---

## 4. Primary Trace ID summary

| Trace ID | Canonical claim | Source class | Primary Theory Map IDs | v0.1 status |
|---|---|---|---|---|
| `T1` | Finite closed recursive resampling contracts expected diversity and can remove support | `THEORY_EXACT` | `TM-M01`, `TM-M03`, `TM-M05`, `TM-C04` | Approved under explicit assumptions |
| `T2` | Low-frequency states face greater one-step extinction probability under finite closed resampling | `THEORY_EXACT` | `TM-C06`, `TM-M04` | Approved as simulation plus proxy interpretation |
| `T3` | Missing grounding and provenance evidence widen the closure exposure interval | `THEORY_GUIDED_OPERATIONALIZATION` | `TM-P01`, `TM-C01`, `TM-P02` | Approved pending decision |
| `T4` | Apparent record count can conceal concentrated external ancestry | `THEORY_GUIDED_OPERATIONALIZATION` | `TM-P04`, `TM-P03`, `TM-C07` | Approved as topology plus proxy interpretation |
| `T5` | Genuine external input can reopen state reachability in the finite resampling model | `THEORY_EXACT` | `TM-M07`, `TM-C02`, `TM-C05` | Approved as experimental simulation |
| `T6` | A cycle invalidates the selected generational ancestry graph interpretation | `PRODUCT_RULE` | `TM-P05` | Approved as graph-validity engineering rule |

---

## 5. Planned module ownership map

The module paths below follow the approved repository skeleton.

| Module | Primary ownership |
|---|---|
| `src/recursive_integrity_toolkit/io/loaders.py` | physical file loading |
| `src/recursive_integrity_toolkit/io/schema_mapping.py` | declarative mapping |
| `src/recursive_integrity_toolkit/io/validation.py` | schema, identity, enum, join, and lineage prerequisite validation |
| `src/recursive_integrity_toolkit/observability/levels.py` | maximum level and capability matrix |
| `src/recursive_integrity_toolkit/metrics/diversity.py` | support, frequencies, Gini-Simpson diversity, deltas |
| `src/recursive_integrity_toolkit/metrics/tail.py` | tail membership, rarity ranking, one-step extinction scenario |
| `src/recursive_integrity_toolkit/metrics/provenance.py` | coverage, source counts, source shares, grounding classes |
| `src/recursive_integrity_toolkit/metrics/bounds.py` | direct and lineage closure exposure intervals |
| `src/recursive_integrity_toolkit/metrics/resampling.py` | closed resampling, expected contraction, external reference loss, reopening scenarios |
| `src/recursive_integrity_toolkit/lineage/graph.py` | canonical graph construction and edge resolution |
| `src/recursive_integrity_toolkit/lineage/ancestry.py` | roots, external roots, incidence, HHI, effective roots |
| `src/recursive_integrity_toolkit/lineage/cycles.py` | cycle detection |
| `src/recursive_integrity_toolkit/reports/json_report.py` | JSON report contract |
| `src/recursive_integrity_toolkit/reports/markdown_report.py` | Markdown report |
| `src/recursive_integrity_toolkit/reports/html_report.py` | optional offline HTML |
| `src/recursive_integrity_toolkit/utils/hashing.py` | file, content, and redaction hashes |
| `src/recursive_integrity_toolkit/utils/logging.py` | content-safe logs |
| `src/recursive_integrity_toolkit/config.py` | resolved configuration |
| `src/recursive_integrity_toolkit/cli.py` | CLI orchestration |

A public behavior must have one primary module owner.

Supporting modules may validate or render the result, but only one module owns its calculation.

---

# PART I. PRIMARY THEORY TRACE RECORDS

## 6. T1: Closed resampling, diversity contraction, and support loss

### 6.1 Trace record

| Field | Value |
|---|---|
| Trace ID | `T1` |
| Canonical claim | Finite closed recursive resampling contracts expected Gini-Simpson diversity and can permanently remove states from the modeled support |
| Source class | `THEORY_EXACT` |
| Primary source | *The Universal Inbreeding Law v2* |
| Source location | Pages 6 through 9 |
| Theory Map IDs | `TM-M01`, `TM-M02`, `TM-M03`, `TM-M05`, `TM-C04` |
| Formula IDs | `F-002`, `F-003`, `F-005`, `F-015` |
| Decisions | `UD-011`, `UD-017`, `UD-033` |
| Primary module owners | `metrics/diversity.py`, `metrics/resampling.py` |
| Minimum observability | Level 1 for observed diversity; experimental Level 5 for recursive scenario paths |
| Release status | Approved under declared representation and resampling assumptions |

### 6.2 Exact mathematical objects

State distribution:

\[
p_t=(p_{t,1},\ldots,p_{t,K})
\]

Closed finite resampling:

\[
X_t\mid p_t
\sim
\operatorname{Multinomial}(n,p_t)
\]

\[
p_{t+1}
=
\frac{X_t}{n}
\]

Gini-Simpson diversity:

\[
D_t
=
1-\sum_i p_{t,i}^2
\]

Expected contraction:

\[
\mathbb{E}[D_{t+1}\mid p_t]
=
\left(1-\frac{1}{n}\right)D_t
\]

Fixed-\(n\) iteration:

\[
\mathbb{E}[D_t]
=
\left(1-\frac{1}{n}\right)^tD_0
\]

Absorbing state loss:

\[
p_{t,i}=0
\Rightarrow
p_{t+k,i}=0
\quad
\text{for all }k>0
\]

under the closed model.

### 6.3 T1 subclaims

#### T1.A Observed support and diversity

The toolkit may calculate support and Gini-Simpson diversity from an observed dataset under a declared representation.

Evidence class:

```text
derived_metric
```

This calculation does not require the real pipeline to follow the closed-resampling model.

#### T1.B Observed longitudinal support contraction

The toolkit may calculate:

```text
support_delta
support_loss_count
support_retention_ratio
extinct_states
gini_simpson_diversity_delta
```

from two ordered representation-compatible versions.

Evidence class:

```text
derived_metric
```

An observed negative delta does not prove that finite resampling caused the change.

#### T1.C Expected closed-resampling contraction

The toolkit may calculate expected diversity under the finite closed-resampling model.

Evidence class:

```text
simulation
```

or:

```text
derived scenario quantity
```

The report must preserve the scenario assumptions.

#### T1.D Sampled recursive paths

The toolkit may simulate finite recursive paths with a recorded random seed.

Evidence class:

```text
simulation
```

#### T1.E Absorbing support within the model

The toolkit may identify that a state with zero modeled probability has no internal route back under the closed operator.

This is a property of the model.

It must not be converted into a permanent production conclusion.

### 6.4 Input requirements

For observed support and diversity:

- valid analyzed records,
- declared representation,
- state assignments,
- nonempty included record scope.

For longitudinal metrics:

- at least two versions,
- explicit version order,
- compatible representation,
- stable state semantics.

For resampling:

- normalized probability vector,
- positive integer sample size,
- non-negative horizon,
- recorded seed for stochastic paths.

### 6.5 Planned public fields

Observed and derived:

```text
derived_metrics.support.by_version.<version>.support_size
derived_metrics.support.support_delta
derived_metrics.support.support_loss_count
derived_metrics.support.support_added_count
derived_metrics.support.support_retention_ratio
derived_metrics.support.extinct_states
derived_metrics.diversity.by_version.<version>.gini_simpson_diversity
derived_metrics.diversity.gini_simpson_diversity_delta
```

Simulation:

```text
simulations.closed_resampling.expected_diversity
simulations.closed_resampling.sampled_paths
simulations.closed_resampling.support_trajectories
simulations.closed_resampling.extinction_events
```

Proxy:

```text
proxy_signals.support_contraction
```

Unavailable conclusion:

```text
unavailable_conclusions.production_failure
unavailable_conclusions.universal_collapse_prediction
```

### 6.6 Planned APIs

Recommended calculation signatures:

```python
def state_frequencies(
    state_ids: Sequence[str],
    *,
    weights: Sequence[float] | None = None,
) -> Mapping[str, float]:
    ...
```

```python
def gini_simpson(
    frequencies: Mapping[str, float],
) -> float:
    ...
```

```python
def compare_support(
    earlier_states: Collection[str],
    later_states: Collection[str],
) -> SupportComparison:
    ...
```

```python
def expected_diversity_after_steps(
    initial_diversity: float,
    *,
    resample_size: int,
    steps: int,
) -> float:
    ...
```

```python
def simulate_closed_resampling(
    initial_distribution: Mapping[str, float],
    *,
    resample_size: int,
    steps: int,
    seed: int,
    replicates: int = 1,
) -> ResamplingSimulation:
    ...
```

These signatures are planning contracts. Final implementation details belong to Phase 3.

### 6.7 Required unit tests

Recommended files:

```text
tests/unit/test_T1_diversity.py
tests/unit/test_T1_support.py
tests/unit/test_T1_resampling.py
```

Required tests:

```text
test_T1_single_state_diversity_is_zero
test_T1_uniform_distribution_matches_hand_calculation
test_T1_support_size_counts_declared_states
test_T1_support_comparison_returns_added_and_extinct_states
test_T1_expected_one_step_contraction_matches_formula
test_T1_expected_multi_step_contraction_matches_formula
test_T1_closed_zero_state_remains_zero
test_T1_fixed_seed_path_is_deterministic
test_T1_weighted_and_unweighted_outputs_remain_separate
test_T1_incompatible_representations_block_comparison
```

### 6.8 Required integration tests

```text
test_T1_hero_topic_support_matches_golden
test_T1_hero_extinct_topics_match_golden
test_T1_report_names_topic_representation
test_T1_observed_delta_does_not_appear_under_simulations
test_T1_simulated_contraction_does_not_appear_under_observed_facts
```

### 6.9 Negative tests

The implementation must not output:

- a collapse score,
- a universal failure threshold,
- a claim that finite resampling caused an observed version delta,
- semantic support when only content hashes are available,
- permanent extinction from one later version.

### 6.10 Required limitations

Every T1 result must disclose relevant limits:

- representation dependence,
- version compatibility,
- closed-resampling assumptions,
- observed versus simulated distinction,
- concentration versus functional failure distinction.

---

## 7. T2: Rare-state extinction and tail fragility

### 7.1 Trace record

| Field | Value |
|---|---|
| Trace ID | `T2` |
| Canonical claim | Under finite closed multinomial resampling, lower-frequency states have greater one-step probability of being absent from the next sample |
| Source class | `THEORY_EXACT` |
| Primary source | *The Universal Inbreeding Law v2* |
| Source location | Page 7 |
| Theory Map IDs | `TM-C06`, `TM-M04`, `TM-M05` |
| Formula IDs | `F-014` |
| Decisions | `UD-012`, `UD-013` |
| Primary module owner | `metrics/tail.py` |
| Minimum observability | Level 1 |
| Scenario status | Simulation |
| Proxy status | Allowed with explicit limitation |

### 7.2 Exact mathematical object

For observed frequency \(p_i\) and finite sample size \(n\):

\[
P_{\text{extinct,next}}(i)
=
(1-p_i)^n
\]

### 7.3 T2 subclaims

#### T2.A Tail membership

Tail membership is a toolkit definition under a declared threshold rule.

Evidence class:

```text
derived_metric
```

The theory supports attention to low-frequency states. The exact threshold belongs to the product specification.

#### T2.B Rarity ranking

States may be ranked from lowest observed frequency to highest.

Evidence class:

```text
derived_metric
```

#### T2.C One-step extinction probability

The exact formula may be reported only under the finite closed-resampling scenario.

Evidence class:

```text
simulation
```

#### T2.D Tail fragility signal

A narrative or categorical warning may summarize the tail structure and scenario result.

Evidence class:

```text
proxy_signal
```

### 7.4 Input requirements

- valid representation,
- observed state counts,
- positive analyzed record count,
- declared tail rule,
- positive scenario sample size for extinction probability.

### 7.5 Planned public fields

Derived:

```text
derived_metrics.tail.tail_rule
derived_metrics.tail.tail_support_size
derived_metrics.tail.tail_record_share
derived_metrics.tail.tail_states
derived_metrics.tail.rarity_ranking
```

Simulation:

```text
simulations.tail_extinction.model
simulations.tail_extinction.resample_size
simulations.tail_extinction.by_state.<state>.one_step_extinction_probability
```

Proxy:

```text
proxy_signals.tail_fragility
```

### 7.6 Planned APIs

```python
def select_tail(
    state_counts: Mapping[str, int],
    *,
    rule: TailRule,
) -> TailSelection:
    ...
```

```python
def rank_by_rarity(
    state_counts: Mapping[str, int],
) -> Sequence[RarityRecord]:
    ...
```

```python
def one_step_extinction_probability(
    frequency: float,
    *,
    resample_size: int,
) -> float:
    ...
```

### 7.7 Required unit tests

Recommended file:

```text
tests/unit/test_T2_tail.py
```

Required tests:

```text
test_T2_singleton_tail_rule_selects_count_one_states
test_T2_rarity_ranking_uses_deterministic_tie_break
test_T2_probability_is_one_when_frequency_is_zero
test_T2_probability_is_zero_when_frequency_is_one
test_T2_probability_matches_hand_calculation
test_T2_lower_frequency_has_higher_probability_for_fixed_n
test_T2_invalid_resample_size_is_rejected
test_T2_missing_representation_blocks_tail_analysis
```

### 7.8 Required report tests

```text
test_T2_probability_appears_only_under_simulations
test_T2_tail_membership_appears_under_derived_metrics
test_T2_tail_warning_appears_under_proxy_signals
test_T2_report_discloses_one_step_horizon
test_T2_report_discloses_closed_multinomial_assumption
test_T2_report_avoids_calibrated_production_forecast_language
```

### 7.9 Negative tests

The implementation must not:

- place the probability under observed facts,
- call the probability a production failure probability,
- choose a universal tail threshold without configuration,
- infer semantic tail from exact hashes,
- claim that every rare state will disappear.

### 7.10 Required limitation

Every T2 scenario must state:

> The probability applies to the declared one-step closed multinomial resampling model. It is not a calibrated forecast of the production pipeline unless separate validation establishes that equivalence.

---

## 8. T3: Provenance uncertainty and closure exposure bounds

### 8.1 Trace record

| Field | Value |
|---|---|
| Trace ID | `T3` |
| Canonical claim | Missing or unknown grounding evidence widens the range of closure exposure compatible with the supplied metadata |
| Source class | `THEORY_GUIDED_OPERATIONALIZATION` |
| Primary theory basis | *The Universal Inbreeding Law v2*, pages 3, 8 through 10, 15 through 17 |
| Supporting theory basis | *Entropy as a Structural Boundary Condition, Not a Causal Force v2*, pages 5 through 10 |
| Theory Map IDs | `TM-P01`, `TM-C01`, `TM-P02` |
| Formula IDs | `F-008`, `F-009`, `F-010` |
| Decisions | `UD-008`, `UD-009`, `UD-010` |
| Primary module owners | `metrics/provenance.py`, `metrics/bounds.py` |
| Minimum observability | Level 2 for direct bounds, Level 3 for lineage bounds |
| Required label | `toolkit_operationalization` |

### 8.2 Source-boundary statement

The theory establishes that claims about openness and correction depend on genuine external input.

The exact lower and upper-bound formula is a toolkit operationalization.

Reports and documentation must not present the interval formula as a theorem quoted from the theory article.

### 8.3 Direct classification

Each analyzed record belongs to one direct class:

```text
known_open
known_closed
unresolved_grounding
```

Conditions are defined in `DEFINITIONS_AND_UNITS.md`.

### 8.4 Direct closure exposure bounds

Let:

- \(N_C\) be known-closed records,
- \(N_U\) be unresolved records,
- \(N\) be total analyzed records.

\[
C_{\min}^{\text{direct}}
=
\frac{N_C}{N}
\]

\[
C_{\max}^{\text{direct}}
=
\frac{N_C+N_U}{N}
\]

\[
W_C^{\text{direct}}
=
C_{\max}^{\text{direct}}
-
C_{\min}^{\text{direct}}
\]

### 8.5 Lineage classification

Each record may belong to:

```text
lineage_known_grounded
lineage_known_closed
lineage_unresolved
```

### 8.6 Lineage closure exposure bounds

Let:

- \(N_{LC}\) be lineage-known-closed records,
- \(N_{LU}\) be lineage-unresolved records.

\[
C_{\min}^{\text{lineage}}
=
\frac{N_{LC}}{N}
\]

\[
C_{\max}^{\text{lineage}}
=
\frac{N_{LC}+N_{LU}}{N}
\]

### 8.7 Input requirements

Direct bounds:

- valid analyzed records,
- matched provenance where present,
- canonical `external_grounding`,
- explicit missing-row classification.

Lineage bounds:

- canonical parent graph,
- external-root determination,
- resolved and unresolved lineage status,
- no unhandled ambiguity.

### 8.8 Planned public fields

Observed basis:

```text
observed_facts.provenance.records_with_matching_rows
observed_facts.provenance.records_missing_rows
observed_facts.provenance.known_open_count
observed_facts.provenance.known_closed_count
observed_facts.provenance.unresolved_grounding_count
```

Derived direct interval:

```text
derived_metrics.closure_exposure.direct.lower_bound
derived_metrics.closure_exposure.direct.upper_bound
derived_metrics.closure_exposure.direct.interval_width
```

Derived lineage interval:

```text
derived_metrics.closure_exposure.lineage.lower_bound
derived_metrics.closure_exposure.lineage.upper_bound
derived_metrics.closure_exposure.lineage.interval_width
```

Unavailable conclusion:

```text
unavailable_conclusions.complete_pipeline_closure
```

when supplied evidence remains incomplete.

### 8.9 Planned APIs

```python
def classify_direct_grounding(
    records: Sequence[Record],
    provenance: Mapping[RecordKey, ProvenanceRow],
) -> DirectGroundingClassification:
    ...
```

```python
def closure_exposure_bounds(
    *,
    known_closed: int,
    unresolved: int,
    total: int,
) -> Bounds:
    ...
```

```python
def classify_lineage_grounding(
    graph: LineageGraph,
    *,
    external_roots: Mapping[RecordKey, frozenset[RecordKey]],
) -> LineageGroundingClassification:
    ...
```

### 8.10 Required unit tests

Recommended files:

```text
tests/unit/test_T3_provenance.py
tests/unit/test_T3_bounds.py
```

Required tests:

```text
test_T3_complete_known_open_has_zero_width
test_T3_complete_known_closed_has_zero_width
test_T3_unknown_grounding_widens_interval
test_T3_missing_provenance_widens_interval
test_T3_explicit_unknown_and_missing_row_remain_distinct
test_T3_lower_bound_never_exceeds_upper_bound
test_T3_interval_width_equals_unresolved_share
test_T3_empty_dataset_is_rejected
test_T3_lineage_unresolved_parent_widens_lineage_interval
test_T3_direct_and_lineage_intervals_remain_separate
```

### 8.11 Required report tests

```text
test_T3_bounds_are_rendered_as_range
test_T3_midpoint_is_not_inserted
test_T3_report_uses_toolkit_operationalization_label
test_T3_report_discloses_grounding_field_coverage
test_T3_report_preserves_estimated_confidence
```

### 8.12 Negative tests

The implementation must not:

- convert `source_type=human` into known open,
- convert `human_reviewed=true` into known open,
- convert missing provenance into known closed,
- hide interval width,
- combine direct and lineage intervals,
- present a midpoint as the result.

### 8.13 Required limitations

- closure is relative to the audited loop,
- metadata may be incomplete or incorrect,
- the interval describes what is compatible with supplied classifications,
- hidden dependencies remain outside direct observation,
- confidence categories remain separate from classification.

---

## 9. T4: External ancestry concentration

### 9.1 Trace record

| Field | Value |
|---|---|
| Trace ID | `T4` |
| Canonical claim | A large set of records can remain dependent on a narrow set of external roots, so record count alone can overstate independent ancestry breadth |
| Source class | `THEORY_GUIDED_OPERATIONALIZATION` |
| Primary source | *Supplementary Case Registry for the Universal Inbreeding Law, Version 2.0* |
| Source location | Pages 6 through 9 |
| Supporting source | *The Universal Inbreeding Law v2*, pages 8 through 10 and 14 through 16 |
| Theory Map IDs | `TM-P03`, `TM-P04`, `TM-C07` |
| Formula IDs | `F-011`, `F-012`, `F-013` |
| Decisions | `UD-006`, `UD-014`, `UD-015`, `UD-034` |
| Primary module owner | `lineage/ancestry.py` |
| Minimum observability | Level 3 |
| Metric status | Derived topology |
| Proxy status | Shared-ancestry dependence signal |

### 9.2 Source-boundary statement

The theory and GA witness support ancestry concentration as a meaningful structural condition.

The exact fractional-root allocation, HHI, and inverse-HHI convention are toolkit operationalizations.

They must not be presented as direct causal contribution measures.

### 9.3 External-root set

For record \(r\):

\[
A_r
=
\{a : a \text{ is a validated reachable external root}\}
\]

### 9.4 Ancestor incidence

For external root \(a\):

\[
I_a
=
|\{r:a\in A_r\}|
\]

### 9.5 Fractional root mass

For record \(r\) with \(k_r=|A_r|\):

\[
m_{r,a}
=
\begin{cases}
1/k_r,&a\in A_r\\
0,&a\notin A_r
\end{cases}
\]

Aggregate:

\[
M_a
=
\sum_r m_{r,a}
\]

Normalize:

\[
w_a
=
\frac{M_a}{\sum_bM_b}
\]

### 9.6 Ancestry HHI

\[
HHI_{\text{ancestry}}
=
\sum_aw_a^2
\]

### 9.7 Effective external-root count

\[
N_{\text{effective roots}}
=
\frac{1}{HHI_{\text{ancestry}}}
\]

### 9.8 Input requirements

- valid acyclic ancestry graph,
- resolved parent references for included records,
- validated external-root determination,
- disclosed unresolved lineage,
- approved multi-root allocation convention.

### 9.9 Planned public fields

Observed basis:

```text
observed_facts.lineage.declared_parent_edge_count
observed_facts.lineage.resolved_parent_edge_count
observed_facts.lineage.unresolved_parent_edge_count
observed_facts.lineage.cycle_detected
```

Derived metrics:

```text
derived_metrics.lineage.resolved_parent_edge_coverage
derived_metrics.lineage.resolved_lineage_coverage
derived_metrics.lineage.external_ancestry_coverage
derived_metrics.lineage.distinct_external_root_count
derived_metrics.lineage.top_shared_ancestors
derived_metrics.lineage.ancestry_concentration_hhi
derived_metrics.lineage.effective_external_root_count
```

Proxy:

```text
proxy_signals.shared_ancestry_dependence
```

Unavailable conclusions:

```text
unavailable_conclusions.causal_ancestor_effect
unavailable_conclusions.correlated_semantic_error
```

### 9.10 Planned APIs

```python
def reachable_external_roots(
    graph: LineageGraph,
    *,
    external_root_flags: Mapping[RecordKey, bool],
) -> Mapping[RecordKey, frozenset[RecordKey]]:
    ...
```

```python
def ancestor_incidence(
    root_sets: Mapping[RecordKey, frozenset[RecordKey]],
) -> Mapping[RecordKey, int]:
    ...
```

```python
def fractional_root_shares(
    root_sets: Mapping[RecordKey, frozenset[RecordKey]],
) -> Mapping[RecordKey, float]:
    ...
```

```python
def ancestry_concentration(
    root_shares: Mapping[RecordKey, float],
) -> AncestryConcentration:
    ...
```

### 9.11 Required unit tests

Recommended file:

```text
tests/unit/test_T4_ancestry.py
```

Required tests:

```text
test_T4_single_root_hhi_is_one
test_T4_two_equal_roots_hhi_is_one_half
test_T4_effective_root_count_is_inverse_hhi
test_T4_multi_root_record_allocates_total_mass_one
test_T4_incidence_counts_each_reachable_root
test_T4_unresolved_record_excluded_from_fractional_mass
test_T4_root_shares_sum_to_one
test_T4_carryover_does_not_create_new_root
test_T4_deterministic_top_ancestor_tie_break
test_T4_empty_external_root_set_is_unavailable
```

### 9.12 Required fixture tests

```text
test_T4_hero_external_root_count_is_five
test_T4_hero_top_root_incidence_is_three
test_T4_multi_root_fixture_matches_hand_calculation
test_T4_unresolved_parent_reduces_coverage
```

### 9.13 Required report tests

```text
test_T4_report_calls_metric_topological
test_T4_report_discloses_fractional_allocation
test_T4_report_does_not_use_causal_contribution_language
test_T4_report_lists_resolved_lineage_coverage
test_T4_proxy_is_named_shared_ancestry_dependence
```

### 9.14 Negative tests

The implementation must not:

- divide contribution according to parent-list order,
- treat every grounded carryover as a new root,
- include unresolved records in HHI without disclosure,
- call HHI an integrity score,
- state that a root caused downstream errors,
- state that incidence share equals content contribution share.

### 9.15 Required limitations

- topology only,
- no causal weights,
- no semantic error evidence,
- external-root classification depends on supplied provenance,
- incomplete lineage reduces coverage,
- HHI convention is a toolkit operationalization.

---

## 10. T5: External reopening simulation

### 10.1 Trace record

| Field | Value |
|---|---|
| Trace ID | `T5` |
| Canonical claim | A genuine external input distribution can restore positive reachability for states absent from the internal distribution |
| Source class | `THEORY_EXACT` |
| Primary source | *The Universal Inbreeding Law v2* |
| Source location | Pages 8 and 9 |
| Supporting source | *Supplementary Case Registry for the Universal Inbreeding Law, Version 2.0*, pages 6 through 9 |
| Theory Map IDs | `TM-M07`, `TM-C02`, `TM-C05` |
| Formula IDs | `F-017` |
| Decision | `UD-017` |
| Primary module owner | `metrics/resampling.py` |
| Minimum observability | Experimental Level 5 |
| Public status | Experimental simulation |

### 10.2 Exact mathematical object

External mixture:

\[
s_t
=
(1-\lambda)p_t+\lambda r_t
\]

Reopened resampling:

\[
p_{t+1}
=
R_n(s_t)
\]

with:

\[
0\leq\lambda\leq1
\]

### 10.3 T5 subclaims

#### T5.A Reachability restoration

When:

\[
p_{t,i}=0
\]

and:

\[
r_{t,i}>0
\]

with:

\[
\lambda>0
\]

the mixed source probability for state \(i\) is positive before finite resampling.

This restores possible re-entry.

It does not guarantee realized re-entry in a finite sample.

#### T5.B Scenario comparison

The toolkit may compare:

- closed scenario,
- partially reopened scenario,
- fully external source scenario.

Evidence class:

```text
simulation
```

#### T5.C Integrity limitation

A larger reopening weight does not guarantee better fidelity when \(r_t\) is contaminated, irrelevant, or shares the same closed ancestry.

No universal integrity conclusion follows from \(\lambda\).

### 10.4 Input requirements

- internal probability distribution,
- external probability distribution,
- compatible support definition,
- reopening weight,
- sample size,
- horizon,
- seed,
- replicate count where requested.

### 10.5 Planned public fields

```text
simulations.external_reopening.model
simulations.external_reopening.parameters.reopening_weight
simulations.external_reopening.parameters.resample_size
simulations.external_reopening.parameters.horizon
simulations.external_reopening.parameters.random_seed
simulations.external_reopening.external_input_distribution
simulations.external_reopening.state_reentry_events
simulations.external_reopening.diversity_trajectory
simulations.external_reopening.support_trajectory
simulations.external_reopening.scenario_comparison
```

Unavailable conclusion:

```text
unavailable_conclusions.empirical_intervention_effect
```

### 10.6 Planned APIs

```python
def mix_external_input(
    internal: Mapping[str, float],
    external: Mapping[str, float],
    *,
    reopening_weight: float,
) -> Mapping[str, float]:
    ...
```

```python
def simulate_reopened_resampling(
    internal: Mapping[str, float],
    external: Mapping[str, float],
    *,
    reopening_weight: float,
    resample_size: int,
    steps: int,
    seed: int,
    replicates: int = 1,
) -> ReopeningSimulation:
    ...
```

### 10.7 Required unit tests

Recommended file:

```text
tests/unit/test_T5_reopening.py
```

Required tests:

```text
test_T5_lambda_zero_matches_closed_source
test_T5_lambda_one_matches_external_source_before_resampling
test_T5_mixture_sums_to_one
test_T5_missing_internal_state_gains_positive_mixed_probability
test_T5_reentry_is_possible_but_not_guaranteed
test_T5_invalid_lambda_is_rejected
test_T5_incompatible_support_is_rejected_or_explicitly_aligned
test_T5_fixed_seed_is_deterministic
```

### 10.8 Required report tests

```text
test_T5_output_is_marked_experimental
test_T5_output_appears_only_under_simulations
test_T5_report_discloses_external_distribution
test_T5_report_discloses_lambda
test_T5_report_does_not_claim_empirical_causal_effect
test_T5_report_does_not_call_lambda_presence_score
```

### 10.9 Negative tests

The implementation must not:

- assume the external distribution is reliable,
- infer \(r_t\) from missing data,
- select \(\lambda\) silently,
- claim that reopening guarantees retention,
- present simulation as an intervention result,
- convert \(\lambda\) into universal Presence.

---

## 11. T6: Cycle validity in the ancestry graph

### 11.1 Trace record

| Field | Value |
|---|---|
| Trace ID | `T6` |
| Canonical claim | A directed cycle invalidates the selected generational ancestry graph interpretation |
| Source class | `PRODUCT_RULE` |
| Theory Map ID | `TM-P05` |
| Decision | `UD-018` |
| Primary module owner | `lineage/cycles.py` |
| Supporting module | `lineage/graph.py` |
| Minimum observability | Level 3 requested |
| Public result | Cycle status and lineage-family error |
| Theory status | Engineering rule, not a theorem of the Universal Inbreeding Law |

### 11.2 Product rule

The record ancestry graph represents parent-to-child generational dependence.

For that representation:

- a record cannot be its own ancestor,
- a directed cycle prevents generation depth and root tracing,
- affected lineage metrics must stop.

Real process feedback loops may be represented through runs, versions, jobs, or process graphs without creating a cycle inside the record ancestry DAG.

### 11.3 Input requirements

- canonical record keys,
- resolved parent edges,
- directed graph construction.

### 11.4 Planned public fields

```text
observed_facts.lineage.cycle_status.detected
observed_facts.lineage.cycle_status.cycle_count
observed_facts.lineage.cycle_status.affected_record_keys
errors[].code = E_LINEAGE_CYCLE
```

Capability effect:

```text
capabilities.lineage.status
```

### 11.5 Planned APIs

```python
def detect_cycles(
    graph: LineageGraph,
) -> CycleResult:
    ...
```

```python
def assert_acyclic_for_ancestry(
    graph: LineageGraph,
) -> None:
    ...
```

### 11.6 Required unit tests

Recommended file:

```text
tests/unit/test_T6_cycles.py
```

Required tests:

```text
test_T6_empty_graph_is_acyclic
test_T6_single_node_without_parent_is_acyclic
test_T6_self_cycle_is_detected
test_T6_two_node_cycle_is_detected
test_T6_long_cycle_is_detected
test_T6_disconnected_cycle_is_detected
test_T6_acyclic_same_version_edges_are_allowed
```

### 11.7 Required integration tests

```text
test_T6_cycle_blocks_ancestry_metrics
test_T6_cycle_preserves_valid_non_lineage_sections_when_partial_report_allowed
test_T6_error_contains_affected_record_keys_without_raw_content
test_T6_report_calls_cycle_graph_validity_error
```

### 11.8 Negative tests

The implementation must not:

- silently remove a cycle,
- choose one edge to break,
- convert a cycle node into a root,
- claim that every real recursive feedback loop is invalid,
- present T6 as direct proof of integrity decay.

---

# PART II. PRODUCT RULE TRACE RECORDS

## 12. PR-001: Canonical record identity

| Field | Value |
|---|---|
| Product Rule ID | `PR-001` |
| Rule | Canonical record identity is `(dataset_version, record_id)` |
| Source class | `PRODUCT_RULE` |
| Definition source | `DEFINITIONS_AND_UNITS.md` Sections 2.2 and 2.3 |
| Data source | `DATA_AND_PROVENANCE_SPEC.md` Sections 8 and 10 |
| Decision | `UD-006` |
| Primary module owner | `io/validation.py` |
| Supporting module | `lineage/graph.py` |
| Evidence class | Observed fact or validation error |
| Public fields | input inventory, duplicate-key errors |

Required tests:

```text
test_PR001_record_id_unique_within_version
test_PR001_same_record_id_allowed_across_versions
test_PR001_duplicate_composite_key_is_error
test_PR001_reserved_separator_is_rejected
```

Prohibited behavior:

- global bare-ID identity,
- filename-based identity,
- numeric coercion of identifiers.

---

## 13. PR-002: Safe loading and format parsing

| Field | Value |
|---|---|
| Product Rule ID | `PR-002` |
| Rule | Input files are parsed locally under explicit supported formats and UTF-8 text rules |
| Source class | `PRODUCT_RULE` |
| Specification source | `DATA_AND_PROVENANCE_SPEC.md` Sections 3 through 7 |
| Primary module owner | `io/loaders.py` |
| Evidence class | Observed fact, warning, or error |
| Public fields | input inventory, parse status, errors |

Required tests:

```text
test_PR002_valid_csv_loads
test_PR002_valid_jsonl_loads
test_PR002_optional_parquet_loads_when_extra_installed
test_PR002_invalid_utf8_fails
test_PR002_unsupported_format_fails
test_PR002_nonfinite_json_number_fails
```

---

## 14. PR-003: Declarative schema mapping

| Field | Value |
|---|---|
| Product Rule ID | `PR-003` |
| Rule | Schema mapping uses an allowlisted declarative operation set and cannot execute arbitrary code |
| Source class | `PRODUCT_RULE` |
| Specification source | `DATA_AND_PROVENANCE_SPEC.md` Section 14 |
| Decision | `UD-016` |
| Primary module owner | `io/schema_mapping.py` |
| Evidence class | Observed transformation record or error |
| Public fields | input mapping inventory, warnings, errors |

Required tests:

```text
test_PR003_rename_succeeds
test_PR003_constant_succeeds
test_PR003_coalesce_succeeds
test_PR003_map_values_succeeds
test_PR003_operation_order_is_deterministic
test_PR003_eval_is_rejected
test_PR003_shell_operation_is_rejected
test_PR003_network_operation_is_rejected
test_PR003_target_collision_is_error
```

Required report field:

```text
inputs.schema_mapping.operations
```

---

## 15. PR-004: Provenance coverage

| Field | Value |
|---|---|
| Product Rule ID | `PR-004` |
| Rule | Row coverage, required-field coverage, and grounding-field coverage remain separate |
| Source class | `PRODUCT_RULE` with structural theory support |
| Theory Map IDs | `TM-P01`, `TM-P02` |
| Formula ID | `F-008` and coverage definitions |
| Decisions | `UD-008`, `UD-009` |
| Primary module owner | `metrics/provenance.py` |
| Minimum observability | Level 2 |
| Evidence class | Observed fact |

Public fields:

```text
observed_facts.provenance.provenance_row_coverage
observed_facts.provenance.provenance_required_field_coverage
observed_facts.provenance.grounding_field_coverage
observed_facts.provenance.missing_provenance_count
```

Required tests:

```text
test_PR004_full_row_coverage_is_one
test_PR004_missing_row_reduces_row_coverage
test_PR004_unknown_grounding_does_not_reduce_row_coverage
test_PR004_unknown_grounding_reduces_grounding_coverage
test_PR004_required_field_coverage_is_separate
```

---

## 16. PR-005: Source-type counts and shares

| Field | Value |
|---|---|
| Product Rule ID | `PR-005` |
| Rule | Source shares are calculated from declared canonical source categories without grounding inference |
| Source class | `PRODUCT_RULE` with structural theory support |
| Theory Map ID | `TM-P02` |
| Formula ID | `F-007` |
| Primary module owner | `metrics/provenance.py` |
| Minimum observability | Level 2 |
| Evidence class | Counts are observed facts; shares are derived metrics |

Public fields:

```text
observed_facts.provenance.source_type_counts
derived_metrics.provenance.source_type_shares
derived_metrics.provenance.missing_provenance_share
```

Required tests:

```text
test_PR005_source_counts_partition_declared_rows
test_PR005_mixed_remains_separate
test_PR005_unknown_and_missing_provenance_remain_separate
test_PR005_unweighted_is_default
test_PR005_weighted_outputs_use_distinct_names
```

Prohibited behavior:

- splitting `mixed` into assumed fractions,
- converting human share into grounding share,
- counting missing rows as declared unknown.

---

## 17. PR-006: Exact duplicate detection

| Field | Value |
|---|---|
| Product Rule ID | `PR-006` |
| Rule | Exact duplicates use a declared deterministic content-normalization profile and hash |
| Source class | `PRODUCT_RULE` |
| Primary module owners | `utils/hashing.py`, `metrics/diversity.py` or future `metrics/duplicates.py` |
| Minimum observability | Level 1 |
| Evidence class | Observed fact |

Public fields:

```text
observed_facts.content.duplicate_record_count
observed_facts.content.duplicate_group_count
observed_facts.content.exact_duplicate_groups
```

Required tests:

```text
test_PR006_identical_normalized_content_groups
test_PR006_duplicate_record_count_excludes_first_representative
test_PR006_profile_is_recorded
test_PR006_content_hash_does_not_claim_semantic_identity
test_PR006_redacted_report_hides_content
```

Near-duplicate behavior remains optional under `UD-020`.

---

## 18. PR-007: Version ordering

| Field | Value |
|---|---|
| Product Rule ID | `PR-007` |
| Rule | Longitudinal analysis requires explicit ordering evidence |
| Source class | `PRODUCT_RULE` |
| Decision | `UD-007` |
| Primary module owners | `io/validation.py`, `config.py` |
| Minimum observability | Required for Level 4 |
| Evidence class | Observed configuration fact or error |

Order priority:

1. explicit version order,
2. valid timestamps,
3. user-declared CLI order.

Public fields:

```text
inputs.version_order
inputs.version_order_source
warnings[].code = W_VERSION_ORDER_MISSING
errors[].code = E_VERSION_ORDER_CONFLICT
```

Required tests:

```text
test_PR007_explicit_list_order
test_PR007_rank_order
test_PR007_timestamp_order
test_PR007_cli_order
test_PR007_conflicting_sources_fail
test_PR007_filename_order_is_not_inferred
```

---

## 19. PR-008: Parent resolution

| Field | Value |
|---|---|
| Product Rule ID | `PR-008` |
| Rule | Parent references resolve against canonical record keys with explicit ambiguity handling |
| Source class | `PRODUCT_RULE` |
| Decisions | `UD-006`, `UD-015` |
| Primary module owners | `lineage/graph.py`, `io/validation.py` |
| Evidence class | Observed fact, warning, or error |

Public fields:

```text
observed_facts.lineage.declared_parent_edge_count
observed_facts.lineage.resolved_parent_edge_count
observed_facts.lineage.unresolved_parent_edge_count
warnings[].code = W_PARENT_UNRESOLVED
errors[].code = E_PARENT_AMBIGUOUS
errors[].code = E_PARENT_FUTURE_VERSION
```

Required tests:

```text
test_PR008_composite_parent_resolves
test_PR008_unique_bare_parent_compatibility_warns
test_PR008_unresolved_parent_warns
test_PR008_ambiguous_parent_fails
test_PR008_future_parent_fails
test_PR008_missing_parent_is_not_external_root
```

---

## 20. PR-009: Generation consistency

| Field | Value |
|---|---|
| Product Rule ID | `PR-009` |
| Rule | Declared generation is validated against approved grounding and lineage rules while remaining separate from lineage depth |
| Source class | `PRODUCT_RULE` guided by theory |
| Theory Map IDs | `TM-C01`, `TM-C02` |
| Decision | `UD-005` |
| Primary module owner | `io/validation.py` |
| Evidence class | Observed declaration plus warning or error |

Public fields:

```text
observed_facts.lineage.declared_generation
derived_metrics.lineage.lineage_depth
warnings[].code = W_GENERATION_MISMATCH
```

Required tests:

```text
test_PR009_grounded_carryover_can_remain_generation_zero
test_PR009_ungrounded_child_increments_generation
test_PR009_generation_and_lineage_depth_remain_separate
test_PR009_unknown_grounding_makes_expected_generation_unavailable
test_PR009_mismatch_warns
```

---

## 21. PR-010: Observability level

| Field | Value |
|---|---|
| Product Rule ID | `PR-010` |
| Rule | The maximum observability level reflects the strongest validated capability available in the run |
| Source class | `PRODUCT_RULE` |
| Decisions | `UD-003`, `UD-004`, `UD-017` |
| Primary module owner | `observability/levels.py` |
| Evidence class | Derived product classification |

Public field:

```text
observability.maximum_level
```

Required tests:

```text
test_PR010_minimal_file_is_level_zero
test_PR010_records_only_is_level_one
test_PR010_partial_provenance_reaches_level_two
test_PR010_valid_lineage_reaches_level_three
test_PR010_ordered_versions_reach_level_four
test_PR010_valid_scenario_reaches_level_five
test_PR010_hero_reaches_level_four
```

---

## 22. PR-011: Capability matrix

| Field | Value |
|---|---|
| Product Rule ID | `PR-011` |
| Rule | Each analysis family receives independent availability, partiality, unavailability, or experimental status |
| Source class | `PRODUCT_RULE` |
| Decision | `UD-004` |
| Primary module owner | `observability/levels.py` |
| Evidence class | Derived product classification |

Required capability keys:

```text
ingestion
content_diagnostics
provenance
lineage
dataset_longitudinal
model_longitudinal
intervention_simulation
```

Public fields:

```text
capabilities.<capability>.status
capabilities.<capability>.coverage
capabilities.<capability>.requirements_met
capabilities.<capability>.requirements_missing
capabilities.<capability>.reason_codes
```

Required tests:

```text
test_PR011_partial_provenance_reports_partial
test_PR011_partial_lineage_reports_partial
test_PR011_level_four_can_have_model_longitudinal_unavailable
test_PR011_simulation_capability_is_experimental
test_PR011_coverage_denominator_is_named
```

---

## 23. PR-012: Report evidence separation

| Field | Value |
|---|---|
| Product Rule ID | `PR-012` |
| Rule | Public results are separated into observed facts, derived metrics, proxy signals, simulations, and unavailable conclusions |
| Source class | `PRODUCT_RULE` with theory boundary support |
| Theory Map IDs | `TM-E01`, `TM-E02`, `TM-C08` |
| Primary module owners | all report modules |
| Evidence class | Report architecture |

Required top-level paths:

```text
observed_facts
derived_metrics
proxy_signals
simulations
unavailable_conclusions
```

Required tests:

```text
test_PR012_exact_count_under_observed_facts
test_PR012_diversity_under_derived_metrics
test_PR012_tail_probability_under_simulations
test_PR012_ancestry_warning_under_proxy_signals
test_PR012_universal_collapse_under_unavailable_conclusions
```

---

## 24. PR-013: Report structure and schema

| Field | Value |
|---|---|
| Product Rule ID | `PR-013` |
| Rule | JSON and Markdown reports use the approved section order and required top-level keys |
| Source class | `PRODUCT_RULE` |
| Decisions | `UD-019`, `UD-036` |
| Primary module owners | `reports/json_report.py`, `reports/markdown_report.py`, optional `reports/html_report.py` |
| Evidence class | Report contract |

Required top-level keys:

```text
run
inputs
observability
capabilities
observed_facts
derived_metrics
proxy_signals
simulations
unavailable_conclusions
recommended_next_metadata
warnings
errors
```

Required tests:

```text
test_PR013_all_top_level_keys_exist
test_PR013_empty_sections_are_preserved
test_PR013_markdown_section_order
test_PR013_json_contains_no_nan
test_PR013_report_schema_version_present
test_PR013_html_is_offline_when_enabled
```

---

## 25. PR-014: Unavailable conclusions

| Field | Value |
|---|---|
| Product Rule ID | `PR-014` |
| Rule | Relevant unsupported conclusions are explicitly listed with blocking evidence and required next metadata |
| Source class | `PRODUCT_RULE` with structural theory support |
| Theory Map IDs | `TM-C08`, `TM-E04`, `TM-E05`, `TM-S01`, `TM-S02` |
| Primary module owner | report assembly layer |
| Evidence class | Unavailable conclusion |

Required hero entries:

```text
model_performance_decline
causal_ancestor_effect
universal_integrity
universal_collapse_prediction
```

Required tests:

```text
test_PR014_hero_lists_model_performance_decline_unavailable
test_PR014_hero_lists_causal_ancestor_effect_unavailable
test_PR014_unavailable_does_not_render_as_zero
test_PR014_required_next_metadata_is_present
```

---

## 26. PR-015: Redaction and privacy-safe reporting

| Field | Value |
|---|---|
| Product Rule ID | `PR-015` |
| Rule | Redacted mode hides sensitive content after calculation without changing metric values |
| Source class | `PRODUCT_RULE` |
| Primary module owners | report modules, `utils/hashing.py`, `utils/logging.py` |
| Evidence class | Product behavior |

Redacted fields include:

- raw content,
- notes,
- full file paths,
- local content references,
- source URIs,
- grounding-evidence paths,
- full embeddings.

Required tests:

```text
test_PR015_redacted_json_hides_content
test_PR015_redacted_markdown_hides_notes
test_PR015_hashed_ids_are_deterministic_under_declared_salt
test_PR015_metrics_match_standard_mode
test_PR015_normal_logs_exclude_content
```

---

## 27. PR-016: Determinism and run metadata

| Field | Value |
|---|---|
| Product Rule ID | `PR-016` |
| Rule | Same inputs, resolved configuration, toolkit version, and seed produce stable public analytical outputs |
| Source class | `PRODUCT_RULE` |
| Primary module owners | `config.py`, `utils/hashing.py`, all metric modules |
| Evidence class | Run metadata and product guarantee |

Public fields:

```text
run.toolkit_version
run.report_schema_version
run.config_hash
run.random_seed
run.deterministic
run.network_call_count
inputs.file_hashes
```

Required tests:

```text
test_PR016_same_input_same_output_after_variable_metadata_normalization
test_PR016_fixed_seed_same_simulation
test_PR016_stable_sorting
test_PR016_file_hash_changes_when_input_changes
test_PR016_hero_network_call_count_is_zero
```

---

## 28. PR-017: Local content-reference safety

| Field | Value |
|---|---|
| Product Rule ID | `PR-017` |
| Rule | Local content references remain inside the approved base directory and do not authorize network access |
| Source class | `PRODUCT_RULE` |
| Primary module owner | `io/loaders.py` |
| Evidence class | Validation behavior |

Required tests:

```text
test_PR017_valid_relative_reference
test_PR017_missing_reference_fails_content_analysis
test_PR017_path_traversal_is_blocked
test_PR017_symlink_escape_is_blocked
test_PR017_network_scheme_is_blocked
test_PR017_metadata_only_analysis_can_continue_when_allowed
```

---

## 29. PR-018: Public terminology restrictions

| Field | Value |
|---|---|
| Product Rule ID | `PR-018` |
| Rule | Public language preserves causal and evidential boundaries |
| Source class | `PRODUCT_RULE` with theory-language authority |
| Theory Map IDs | `TM-E01`, `TM-E02`, `TM-E04`, `TM-E05`, `TM-C08` |
| Decision | `UD-035` |
| Primary module owners | report modules |
| Evidence class | Rendering rule |

Restricted direct-conclusion phrases include:

```text
collapse score
entropy caused
proved failure
ancestor caused the error
human data is safe
synthetic data caused collapse
```

Required tests:

```text
test_PR018_golden_report_contains_no_collapse_metric
test_PR018_report_names_mechanism_before_entropy
test_PR018_report_uses_declared_grounding_language
test_PR018_extinction_language_is_observed_version_bound
test_PR018_ancestry_language_is_noncausal
```

---

# PART III. PUBLIC FIELD REGISTRY

## 30. Run and input fields

| Report path | Owner | Source class | Evidence class | Minimum level |
|---|---|---|---|---:|
| `run.run_id` | `PR-016` | Product rule | Observed fact | 0 |
| `run.toolkit_version` | `PR-016` | Product rule | Observed fact | 0 |
| `run.report_schema_version` | `PR-013` | Product rule | Observed fact | 0 |
| `run.duration_seconds` | `PR-016` | Product rule | Observed fact | 0 |
| `run.config_hash` | `PR-016` | Product rule | Observed fact | 0 |
| `run.random_seed` | `PR-016` | Product rule | Observed fact | 0 |
| `run.deterministic` | `PR-016` | Product rule | Derived product status | 0 |
| `run.network_call_count` | `PR-016` | Product rule | Observed fact | 0 |
| `inputs.artifacts` | `PR-002` | Product rule | Observed fact | 0 |
| `inputs.file_hashes` | `PR-016` | Product rule | Observed fact | 0 |
| `inputs.version_order` | `PR-007` | Product rule | Observed configuration fact | 0 |
| `inputs.version_order_source` | `PR-007` | Product rule | Observed configuration fact | 0 |
| `inputs.representation` | `PR-011`, `T1`, `T2` | Mixed | Observed configuration fact | 1 |
| `inputs.schema_mapping` | `PR-003` | Product rule | Observed transformation record | 0 |

---

## 31. Observability and capability fields

| Report path | Owner | Evidence class | Minimum level |
|---|---|---|---:|
| `observability.maximum_level` | `PR-010` | Derived product classification | 0 |
| `observability.level_label` | `PR-010` | Derived product classification | 0 |
| `observability.basis` | `PR-010` | Product explanation | 0 |
| `observability.limitations` | `PR-010`, `PR-014` | Product explanation | 0 |
| `capabilities.ingestion` | `PR-011` | Derived product classification | 0 |
| `capabilities.content_diagnostics` | `PR-011` | Derived product classification | 0 |
| `capabilities.provenance` | `PR-011` | Derived product classification | 0 |
| `capabilities.lineage` | `PR-011` | Derived product classification | 0 |
| `capabilities.dataset_longitudinal` | `PR-011` | Derived product classification | 0 |
| `capabilities.model_longitudinal` | `PR-011` | Derived product classification | 0 |
| `capabilities.intervention_simulation` | `PR-011` | Derived product classification | 0 |

---

## 32. Observed-fact fields

| Report path | Owner | Minimum level | Required limit |
|---|---|---:|---|
| `observed_facts.record_counts` | `PR-002` | 0 | Scope by version |
| `observed_facts.content.duplicate_record_count` | `PR-006` | 1 | Exact normalization only |
| `observed_facts.content.duplicate_group_count` | `PR-006` | 1 | Exact normalization only |
| `observed_facts.provenance.provenance_row_coverage` | `PR-004` | 2 | Matching row coverage |
| `observed_facts.provenance.provenance_required_field_coverage` | `PR-004` | 2 | Required field validity |
| `observed_facts.provenance.grounding_field_coverage` | `PR-004` | 2 | `yes` or `no` only |
| `observed_facts.provenance.source_type_counts` | `PR-005` | 2 | Declared categories |
| `observed_facts.provenance.provenance_confidence_counts` | `PR-004` | 2 | No probability conversion |
| `observed_facts.lineage.declared_parent_edge_count` | `PR-008` | 3 | Declared references |
| `observed_facts.lineage.resolved_parent_edge_count` | `PR-008` | 3 | Unique resolved edges |
| `observed_facts.lineage.unresolved_parent_edge_count` | `PR-008` | 3 | Missing remains unresolved |
| `observed_facts.lineage.cycle_status` | `T6` | 3 | Graph-validity status |

---

## 33. Derived metric fields

| Report path | Owner | Formula or rule | Minimum level |
|---|---|---|---:|
| `derived_metrics.support.by_version.*.support_size` | `T1` | `F-002` | 1 |
| `derived_metrics.support.support_delta` | `T1` | `F-005` | 4 |
| `derived_metrics.support.support_retention_ratio` | `T1` | `F-006` | 4 |
| `derived_metrics.support.support_loss_count` | `T1` | set difference | 4 |
| `derived_metrics.support.support_added_count` | `T1` | set difference | 4 |
| `derived_metrics.support.extinct_states` | `T1` | earlier minus later support | 4 |
| `derived_metrics.diversity.by_version.*.gini_simpson_diversity` | `T1` | `F-003` | 1 |
| `derived_metrics.diversity.gini_simpson_diversity_delta` | `T1` | `F-018` | 4 |
| `derived_metrics.tail.tail_support_size` | `T2` | tail rule | 1 |
| `derived_metrics.tail.tail_record_share` | `T2` | declared tail mass | 1 |
| `derived_metrics.tail.rarity_ranking` | `T2` | frequency ordering | 1 |
| `derived_metrics.provenance.source_type_shares` | `PR-005` | `F-007` | 2 |
| `derived_metrics.provenance.missing_provenance_share` | `PR-004` | one minus row coverage | 2 |
| `derived_metrics.closure_exposure.direct.lower_bound` | `T3` | `F-009` | 2 |
| `derived_metrics.closure_exposure.direct.upper_bound` | `T3` | `F-010` | 2 |
| `derived_metrics.closure_exposure.direct.interval_width` | `T3` | upper minus lower | 2 |
| `derived_metrics.closure_exposure.lineage.lower_bound` | `T3` | lineage rule | 3 |
| `derived_metrics.closure_exposure.lineage.upper_bound` | `T3` | lineage rule | 3 |
| `derived_metrics.lineage.resolved_parent_edge_coverage` | `PR-008` | resolved edges divided by declared edges | 3 |
| `derived_metrics.lineage.resolved_lineage_coverage` | `T4` | resolved records divided by scope | 3 |
| `derived_metrics.lineage.external_ancestry_coverage` | `T4` | externally rooted records divided by scope | 3 |
| `derived_metrics.lineage.distinct_external_root_count` | `T4` | root-set union cardinality | 3 |
| `derived_metrics.lineage.top_shared_ancestors` | `T4` | incidence ranking | 3 |
| `derived_metrics.lineage.ancestry_concentration_hhi` | `T4` | `F-012` | 3 |
| `derived_metrics.lineage.effective_external_root_count` | `T4` | `F-013` | 3 |
| `derived_metrics.lineage.lineage_depth` | `PR-009` | maximum resolved parent depth | 3 |

---

## 34. Proxy signal fields

| Report path | Owner | Basis | Minimum level |
|---|---|---|---:|
| `proxy_signals.support_contraction` | `T1` | support delta and extinct states | 4 |
| `proxy_signals.tail_fragility` | `T2` | rarity and scenario results | 1 |
| `proxy_signals.shared_ancestry_dependence` | `T4` | incidence, HHI, effective roots | 3 |
| `proxy_signals.provenance_uncertainty` | `T3` | interval width and field coverage | 2 |

Every proxy must disclose:

- basis fields,
- coverage,
- trigger rule,
- limitation.

---

## 35. Simulation fields

| Report path | Owner | Minimum level | Status |
|---|---|---:|---|
| `simulations.closed_resampling` | `T1` | 5 | Experimental |
| `simulations.tail_extinction` | `T2` | 1 when explicitly requested | Simulation |
| `simulations.external_reopening` | `T5` | 5 | Experimental |
| `simulations.external_reference_loss` | `TM-M06`, future approved trace | 5 | Optional |

`external_reference_loss` must remain absent until its trace ownership is approved for public v0.1 exposure.

---

## 36. Unavailable-conclusion fields

| Conclusion key | Owner | Default trigger |
|---|---|---|
| `model_performance_decline` | `PR-014` | no model outcomes |
| `causal_ancestor_effect` | `T4`, `PR-014` | topology without causal evidence |
| `correlated_semantic_error` | `T4`, `PR-014` | ancestry without error labels |
| `production_failure` | `T1`, `PR-014` | structural metrics without outcome evidence |
| `universal_integrity` | `TM-C03`, `TM-S01`, `PR-014` | no operational definition |
| `universal_quality` | `TM-S01`, `PR-014` | no operational definition |
| `universal_stability` | `TM-S02`, `PR-014` | no operational definition |
| `universal_entropy_score` | `TM-E05`, `PR-014` | forbidden |
| `universal_collapse_prediction` | `PR-014`, `PR-018` | outside v0.1 |
| `empirical_intervention_effect` | `T5`, `PR-014` | simulation without controlled empirical design |
| `amplification_threshold` | `TM-A02`, `PR-014` | deferred branch |

---

# PART IV. FILE HEADER AND CODE DOCUMENTATION CONTRACT

## 37. Required theory-relevant module header

Every theory-relevant module should begin with a docstring containing:

```python
"""
Purpose:
    <single-purpose description>

Primary trace ownership:
    T1

Theory Map IDs:
    TM-M01, TM-M03

Formula IDs:
    F-003, F-015

Source class:
    THEORY_EXACT

Public fields:
    derived_metrics.diversity.*
    simulations.closed_resampling.*

Assumptions:
    - declared representation
    - finite categorical support
    - multinomial sampling for simulation paths

Limits:
    - observed diversity does not prove functional failure
    - closed-resampling formulas do not automatically describe a production pipeline
"""
```

Product-only modules should replace trace ownership with:

```text
Primary product rule ownership:
    PR-003
```

### 37.1 One primary owner

A source file may reference several IDs.

It must identify one primary ownership record for each public calculation.

### 37.2 No undocumented public behavior

A function that changes a public result must reference:

- Trace ID or Product Rule ID,
- formula or deterministic rule,
- expected evidence class.

---

## 38. Public function documentation

A public calculation function should document:

- inputs,
- units,
- missingness behavior,
- assumptions,
- return type,
- evidence class,
- trace owner,
- error conditions,
- deterministic behavior.

Example:

```python
def gini_simpson(frequencies: Mapping[str, float]) -> float:
    """
    Calculate Gini-Simpson diversity.

    Trace:
        T1, TM-C04, TM-M03, F-003

    Evidence class:
        derived_metric

    Preconditions:
        Frequencies are finite, non-negative, and sum to one.

    Limits:
        The value is representation-bound and does not establish functional failure.
    """
```

---

# PART V. TEST TRACEABILITY

## 39. Test naming convention

Required pattern:

```text
test_<OWNER_ID>_<behavior>
```

Examples:

```text
test_T1_expected_one_step_contraction_matches_formula
test_T4_single_root_hhi_is_one
test_PR003_eval_is_rejected
```

### 39.1 Test owner requirement

Every required test must name:

- one primary Trace ID or Product Rule ID,
- one expected behavior,
- one independent expected-value source.

### 39.2 Independent expected values

Expected values must come from:

- hand calculation,
- closed-form derivation,
- separately reviewed notebook,
- manually prepared fixture,
- external standard where applicable.

Expected values must not be created by running the implementation and copying its output.

---

## 40. Test directory map

Recommended structure:

```text
tests/
├── fixtures/
│   ├── hero/
│   ├── lineage_multi_root/
│   ├── lineage_ambiguous/
│   ├── lineage_cycles/
│   ├── representation_incompatible/
│   └── provenance_partial/
├── unit/
│   ├── test_T1_diversity.py
│   ├── test_T1_support.py
│   ├── test_T1_resampling.py
│   ├── test_T2_tail.py
│   ├── test_T3_provenance.py
│   ├── test_T3_bounds.py
│   ├── test_T4_ancestry.py
│   ├── test_T5_reopening.py
│   ├── test_T6_cycles.py
│   ├── test_PR001_identity.py
│   ├── test_PR002_loaders.py
│   ├── test_PR003_schema_mapping.py
│   ├── test_PR004_coverage.py
│   ├── test_PR005_source_shares.py
│   ├── test_PR006_duplicates.py
│   ├── test_PR007_version_order.py
│   ├── test_PR008_parent_resolution.py
│   ├── test_PR009_generation.py
│   ├── test_PR010_observability.py
│   ├── test_PR011_capabilities.py
│   ├── test_PR012_evidence_classes.py
│   ├── test_PR013_report_schema.py
│   ├── test_PR014_unavailable.py
│   ├── test_PR015_redaction.py
│   ├── test_PR016_determinism.py
│   ├── test_PR017_content_refs.py
│   └── test_PR018_language.py
├── integration/
│   ├── test_hero_end_to_end.py
│   ├── test_partial_provenance_report.py
│   ├── test_partial_lineage_report.py
│   ├── test_cli_validation.py
│   └── test_no_network.py
└── golden/
    ├── hero_report.json
    ├── hero_report.md
    ├── partial_provenance_report.json
    └── lineage_multi_root_report.json
```

---

## 41. Hero golden traceability

| Hero assertion | Owner | Expected value |
|---|---|---|
| v1 record count | `PR-002` | 8 |
| v2 record count | `PR-002` | 8 |
| maximum observability | `PR-010` | 4 |
| topic representation | `T1`, `PR-011` | `topic` |
| v1 support | `T1` | 8 |
| v2 support | `T1` | 5 |
| support delta | `T1` | -3 |
| support retention | `T1` | 0.625 |
| extinct states | `T1` | `lizard`, `turtle`, `battery` |
| v2 provenance row coverage | `PR-004` | 1.0 |
| v2 human share | `PR-005` | 0.5 |
| v2 synthetic share | `PR-005` | 0.5 |
| v2 unknown share | `PR-005` | 0.0 |
| cycle detected | `T6` | false |
| distinct external roots | `T4` | 5 |
| top shared root | `T4` | `v1::v1_01` |
| top shared-root incidence | `T4` | 3 |
| top shared-root incidence share | `T4` | 0.375 |
| model longitudinal | `PR-011` | unavailable |
| universal collapse | `PR-014` | unavailable |

---

## 42. Negative golden assertions

The hero report must not contain:

```text
collapse_score
integrity_score
entropy_score
model_performance_decline: true
causal_ancestor_effect: true
```

The Markdown report must not state:

```text
The model has collapsed.
The top ancestor caused the error.
Human data made the system safe.
Entropy caused the support loss.
```

Owners:

```text
PR-012
PR-014
PR-018
```

---

# PART VI. PHASE TRACEABILITY

## 43. Phase 0 traceability deliverables

Required files:

- `SPEC_AUDIT.md`
- `THEORY_SOURCE_MAP.md`
- `UNRESOLVED_DECISIONS.md`
- `PROJECT_INSTRUCTIONS.md`
- `V0.1_PRODUCT_SPEC.md`
- `DEFINITIONS_AND_UNITS.md`
- `DATA_AND_PROVENANCE_SPEC.md`
- `OBSERVABILITY_AND_REPORTING.md`
- `THEORY_TO_CODE_TRACEABILITY.md`

Phase 0 traceability gate:

- T1 through T6 fully mapped,
- product rules mapped,
- public field registry present,
- deferred claims listed,
- no code produced.

---

## 44. Phase 1 traceability requirements

Repository scaffold must include:

- planned module paths,
- planned test paths,
- file headers with ownership placeholders,
- no metric behavior,
- dependency justification.

Phase 1 review asks:

- Does every planned public field have an owner?
- Does every module have a bounded purpose?
- Do tests have planned owner IDs?
- Are deferred modules absent?

---

## 45. Phase 2 traceability requirements

Implemented owners:

```text
PR-001
PR-002
PR-003
PR-004 input basis
PR-007
PR-008 input basis
PR-009 validation
PR-010
PR-011
PR-017
```

Required evidence:

- loaders,
- mapping,
- validation,
- observability,
- capability matrix,
- exact warnings and errors.

No T1 through T5 calculation is required for Phase 2 completion.

---

## 46. Phase 3 traceability requirements

Implemented owners:

```text
T1
T2
T3 direct bounds
PR-005
PR-006
```

Optional experimental implementation:

```text
T5
```

Required review:

- formula transcription,
- hand-calculated tests,
- evidence-class placement,
- no black-box score.

---

## 47. Phase 4 traceability requirements

Implemented owners:

```text
PR-012
PR-013
PR-014
PR-015
PR-016
PR-018
```

Required review:

- JSON contract,
- Markdown order,
- redaction,
- unavailable conclusions,
- terminology restrictions,
- golden outputs.

---

## 48. Phase 5 traceability requirements

Implemented owners:

```text
T4
T6
PR-008 full lineage behavior
PR-009 lineage depth
T3 lineage bounds
```

Required review:

- multi-root fixture,
- unresolved-parent behavior,
- cycle behavior,
- external-root logic,
- HHI convention,
- topological limitation.

---

## 49. Phase 6A traceability requirements

Implemented owners:

```text
T1 observed longitudinal comparison
PR-007
PR-011 dataset_longitudinal
```

Required review:

- explicit order,
- representation compatibility,
- observed extinction wording,
- model longitudinal remains separate.

---

## 50. Phase 6B traceability requirements

Implemented owners:

```text
T1 closed resampling simulation
T2 extinction scenario
T5 reopening scenario
```

Required review:

- experimental labels,
- seeds,
- assumptions,
- no empirical causal claim,
- no automatic scenario execution.

---

# PART VII. DEFERRED AND FORBIDDEN TRACE RECORDS

## 51. Deferred theory registry

| Theory Map ID | Concept | v0.1 status | Reason |
|---|---|---|---|
| `TM-C03` | Universal integrity | Deferred | No universal unit or external-reference contract |
| `TM-C05` | Universal Presence | Deferred outside scenario \(\lambda\) | No independence and relevance measure |
| `TM-S01` | \(Q=I\times D\) numerical score | Deferred | \(I\) and \(Q\) lack operational definitions |
| `TM-S02` | \(S=P\times I\) numerical score | Deferred | \(P\), \(I\), and \(S\) lack operational definitions |
| `TM-E05` | Universal entropy score | Forbidden | Different entropy objects cannot be collapsed into one score |
| `TM-A01` | Amplification branch | Deferred | Outside contraction-focused v0.1 |
| `TM-A02` | Spectral-radius threshold | Deferred | No transfer-matrix input schema |
| `TM-A03` | Delayed visibility metric | Deferred | No calibrated observation model |
| `TM-GA01` through `TM-GA05` | GA-specific operators | Supporting only | Future validation fixture, not core product |

### 51.1 Public behavior

Deferred concepts may appear in:

- theory documentation,
- unavailable conclusions,
- future-work notes.

They must not appear in:

- `observed_facts`,
- `derived_metrics`,
- `proxy_signals`,
- `simulations`,

unless a later approved trace record authorizes them.

---

## 52. Forbidden public results

The following remain forbidden in v0.1:

```text
collapse_score
universal_integrity_score
universal_presence_score
universal_quality_score
universal_stability_score
universal_entropy_score
epoch_countdown_to_failure
automatic_human_source_inference
automatic_external_grounding_inference
causal_ancestor_contribution
```

A schema-validation test should reject or flag any accidental introduction of these field names.

Recommended test:

```text
test_traceability_forbidden_public_fields_absent
```

---

# PART VIII. TRACEABILITY REVIEW PROCEDURES

## 53. Pre-implementation review

Before implementing a public result, the maintainer must confirm:

- [ ] trace owner exists,
- [ ] source class is correct,
- [ ] definitions are approved,
- [ ] decisions are approved,
- [ ] module owner exists,
- [ ] tests are listed,
- [ ] report path exists,
- [ ] evidence class is fixed,
- [ ] observability prerequisites are fixed,
- [ ] limitations are fixed.

If any item fails, implementation stops.

---

## 54. Pull-request traceability checklist

Every theory-relevant pull request should include:

```text
Trace IDs:
Theory Map IDs:
Product Rule IDs:
Formula IDs:
Decisions used:
Public fields changed:
Tests added or changed:
Evidence classes affected:
Limitations changed:
Golden outputs changed:
```

A pull request that changes a public metric meaning must update:

- definitions,
- traceability,
- tests,
- report schema,
- release notes.

---

## 55. Release traceability audit

Before `official-v0.1`, verify:

1. every public field appears in the registry,
2. every public field has one primary owner,
3. every owner has at least one test,
4. every formula has an independent expected-value test,
5. every proxy names its basis fields,
6. every simulation lists assumptions,
7. every unavailable conclusion lists blocking evidence,
8. every deferred claim is absent from public metric sections,
9. every report field has stable type and unit,
10. every theory-relevant module header lists ownership IDs,
11. every golden output matches the approved hero values,
12. terminology tests pass,
13. redaction tests pass,
14. no hidden network call occurs.

---

## 56. Traceability coverage metrics

The repository may calculate internal release-review metrics.

These metrics are product quality checks, not user dataset diagnostics.

### 56.1 Public-field trace coverage

\[
P_{\text{field trace}}
=
\frac{\text{public fields with approved owner}}
{\text{total public fields}}
\]

Release requirement:

```text
1.0
```

### 56.2 Owner test coverage

\[
P_{\text{owner test}}
=
\frac{\text{owners with at least one required passing test}}
{\text{total active owners}}
\]

Release requirement:

```text
1.0
```

### 56.3 Limitation coverage

\[
P_{\text{limitation}}
=
\frac{\text{public proxy and simulation fields with explicit limitations}}
{\text{total public proxy and simulation fields}}
\]

Release requirement:

```text
1.0
```

These internal checks must not be called integrity scores.

---

## 57. Traceability failure conditions

Release must stop when:

- a public field has no owner,
- a metric has no unit,
- a formula has no independent test,
- a proxy has no limitation,
- a simulation lacks assumptions or seed behavior,
- an unavailable conclusion is omitted from the hero report,
- a deferred theory object powers a result,
- a product operationalization is presented as an exact theory theorem,
- a product rule is presented as theory,
- a source passage cannot be verified,
- a report renderer changes evidence class.

---

# PART IX. APPROVAL

## 58. Approval checklist

The Theory Owner and reviewers should confirm:

- [ ] T1 correctly separates observed longitudinal change from closed-resampling simulation.
- [ ] T2 keeps extinction probability under simulation.
- [ ] T3 is labeled as a toolkit operationalization.
- [ ] T4 is labeled as topology and not causal contribution.
- [ ] T5 remains experimental.
- [ ] T6 remains a graph-validity product rule.
- [ ] product-only fields use `PR-*` ownership.
- [ ] every planned public field has an owner.
- [ ] every owner has required tests.
- [ ] unavailable conclusions are traceable.
- [ ] deferred theory does not power public v0.1 results.
- [ ] module headers preserve ownership and limits.
- [ ] phase gates identify which owners may be implemented.
- [ ] hero golden assertions have complete ownership.

### Theory Owner decision

- [ ] Approve traceability baseline
- [ ] Approve with exceptions
- [ ] Return for revision

Exceptions:

```text

```

Theory Owner:

```text
Xiangyu Guo
```

Approval date:

```text

```

Approved status:

```text
PENDING
```

### Mathematical Reviewer acknowledgment

- [ ] Theory equations are transcribed correctly.
- [ ] Toolkit operationalizations are labeled correctly.
- [ ] Formula assumptions are explicit.
- [ ] Required hand-calculated tests are sufficient.
- [ ] Observed and simulated quantities remain separate.

Reviewer notes:

```text

```

Reviewer:

```text

```

Date:

```text

```

### Technical Maintainer acknowledgment

- [ ] Planned module ownership is implementable.
- [ ] Public field paths are stable enough for v0.1.
- [ ] Test ownership is complete.
- [ ] Report renderers can preserve evidence classes.
- [ ] Deferred claims can be blocked by schema and tests.

Technical notes:

```text

```

Maintainer:

```text

```

Date:

```text

```

---

## 59. Change-control rule

After approval:

1. a new public theory-relevant metric requires a Theory Map entry before a new `T*` Trace ID,
2. a new product-only behavior requires a new `PR-*` record,
3. a field cannot change owner silently,
4. a field cannot change evidence class silently,
5. a formula change requires definition, test, report, and release-note updates,
6. a limitation cannot be removed without stronger approved evidence,
7. a deferred concept cannot enter implementation without full traceability,
8. a golden-output change requires Theory Owner and Technical Maintainer review,
9. traceability records remain in version history when superseded,
10. code convenience cannot override source meaning or product boundaries.
