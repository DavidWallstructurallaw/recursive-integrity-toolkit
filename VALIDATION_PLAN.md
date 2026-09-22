# VALIDATION_PLAN

## Document control

| Field | Value |
|---|---|
| Project | Recursive Integrity Toolkit |
| Target release | v0.1 |
| Phase | Phase 0 |
| Status | APPROVED PHASE 0 BASELINE |
| Primary owner | Theory Owner |
| Technical reviewers | Mathematical Reviewer, Technical Maintainer, Security Reviewer, Domain Validator |
| Depends on | `SPEC_AUDIT.md`, `THEORY_SOURCE_MAP.md`, `UNRESOLVED_DECISIONS.md`, `PROJECT_INSTRUCTIONS.md`, `V0.1_PRODUCT_SPEC.md`, `DEFINITIONS_AND_UNITS.md`, `DATA_AND_PROVENANCE_SPEC.md`, `OBSERVABILITY_AND_REPORTING.md`, `THEORY_TO_CODE_TRACEABILITY.md` |
| Purpose | Define independent validation methods, fixtures, expected values, failure behavior, phase gates, continuous-integration checks, and release evidence for v0.1 |
| Implementation code authorized | No |

This file defines how Recursive Integrity Toolkit v0.1 will be shown to conform to its theory, specifications, schemas, calculations, privacy posture, reporting contract, and release promises.

Validation is divided into independent layers so that one successful test family cannot conceal failure in another.

The plan distinguishes:

- correctness of formulas,
- correctness of implementation,
- correctness of data interpretation,
- correctness of report classification,
- usefulness under realistic workflows,
- performance within declared limits,
- privacy and security behavior,
- release completeness.

Expected values must come from hand calculation, closed-form derivation, separately reviewed notebooks, authoritative format rules, or manually prepared fixtures.

Expected values must not be created by running the implementation and copying its output.

Definitions marked `APPROVED DECISION` become release-authoritative only after the corresponding `UD-*` decision is approved.

---

## 1. Validation objectives

v0.1 validation must establish all of the following.

### 1.1 Mathematical fidelity

The implemented formulas reproduce the intended mathematical objects under their declared assumptions.

### 1.2 Specification fidelity

Canonical names, units, denominators, enum values, missingness rules, and evidence classes match the approved specifications.

### 1.3 Input fidelity

The toolkit reads valid inputs, rejects invalid inputs, preserves unknown values, and does not invent provenance or lineage.

### 1.4 Traceability fidelity

Every public field has:

- a definition,
- an owner,
- a formula or deterministic rule,
- tests,
- an evidence class,
- an observability requirement,
- a limitation.

### 1.5 Reporting fidelity

The report preserves the distinction among:

- observed facts,
- derived metrics,
- proxy signals,
- simulations,
- unavailable conclusions.

### 1.6 Reproducibility

The same inputs, resolved configuration, toolkit version, and random seed produce stable analytical outputs.

### 1.7 Privacy fidelity

Normal execution does not expose raw content, notes, full embeddings, or private paths in logs and redacted reports.

### 1.8 Security fidelity

Inputs cannot execute code, escape approved local content directories, trigger remote retrieval, or silently expand the attack surface.

### 1.9 Performance fidelity

The hero example and declared standard-audit scale meet their published targets on representative local hardware.

### 1.10 User-value fidelity

A new user can run the hero example, understand the result, identify limitations, and determine which metadata would unlock stronger analysis.

---

## 2. Validation principles

### 2.1 Independent expected values

A test oracle must be independent from the implementation under test.

Approved sources of expected values:

- hand arithmetic,
- algebraic derivation,
- separately reviewed notebook,
- manually enumerated graph,
- manually prepared golden report,
- format specification,
- fixed public standard,
- approved product rule.

Disallowed source:

```text
the implementation output itself
```

### 2.2 Small exact cases before large cases

Every metric must first pass a tiny case that can be checked by inspection.

Large synthetic or empirical examples supplement exact cases.

They do not replace them.

### 2.3 Positive and negative validation

Every public capability requires:

- at least one valid-input test,
- at least one boundary test,
- at least one invalid-input test,
- at least one unavailable-evidence test,
- at least one report-classification test.

### 2.4 No cross-layer substitution

Passing unit tests does not replace:

- integration tests,
- golden report tests,
- security tests,
- performance tests,
- empirical usefulness review.

### 2.5 Assumption visibility

A mathematical scenario passes only when its assumptions appear in:

- configuration,
- structured result,
- human-readable report,
- test fixture.

### 2.6 Exact unknown handling

Validation must explicitly test that:

- missing differs from unknown,
- unknown differs from zero,
- unknown source differs from missing provenance,
- lineage root differs from external root,
- source type differs from external grounding.

### 2.7 Failure locality

A failure in one capability should block only the affected capability when a valid partial report remains possible.

Fatal input failures must stop the full run.

### 2.8 No hidden remediation

The toolkit must not silently:

- repair malformed parent references,
- choose a version order,
- infer a source type,
- infer grounding,
- remove a graph cycle,
- select a semantic representation,
- impute a missing weight,
- replace an interval with a midpoint.

### 2.9 Deterministic test data

Fixtures must be version-controlled, human-readable where practical, and stable across releases.

### 2.10 Theory and product rules remain distinct

Tests for `THEORY_EXACT`, `THEORY_GUIDED_OPERATIONALIZATION`, and `PRODUCT_RULE` must identify their source class.

---

## 3. Validation layers

v0.1 uses ten validation layers.

| Layer | Name | Primary question |
|---:|---|---|
| 0 | Specification consistency | Do the approved documents agree? |
| 1 | Mathematical validation | Do formulas and exact rules produce intended values? |
| 2 | Data-contract validation | Are inputs parsed, mapped, normalized, and classified correctly? |
| 3 | Unit validation | Does each module behave correctly in isolation? |
| 4 | Integration validation | Do modules work together across a complete audit flow? |
| 5 | Report and golden validation | Does public output preserve values, classes, limits, and language? |
| 6 | Privacy and security validation | Does execution remain local, non-executable, and redaction-safe? |
| 7 | Determinism and compatibility validation | Are outputs stable across supported environments? |
| 8 | Performance validation | Does the toolkit meet declared runtime and scale targets? |
| 9 | Empirical usefulness validation | Do outputs remain useful on realistic workflows without overclaiming? |

A release candidate must pass every required layer.

---

## 4. Validation result statuses

### 4.1 Test statuses

Allowed test statuses:

```text
passed
failed
skipped
blocked
xfail
```

### 4.2 Release interpretation

| Test status | Release interpretation |
|---|---|
| `passed` | Requirement satisfied |
| `failed` | Release blocked |
| `skipped` | Acceptable only for optional dependency or unsupported environment with documented reason |
| `blocked` | Release blocked when the test is required |
| `xfail` | Acceptable only for an explicitly deferred behavior excluded from public v0.1 |

### 4.3 No silent expected failure

An `xfail` test must identify:

- deferred decision or issue,
- reason,
- target release,
- public fields that remain unavailable.

### 4.4 Flaky tests

A flaky required test is a failed release condition.

Retries may diagnose infrastructure instability.

Retries must not convert an unstable result into a pass without investigation.

---

## 5. Severity and gate classes

### 5.1 Gate classes

| Gate class | Meaning |
|---|---|
| `PHASE_BLOCKER` | Blocks completion of the current development phase |
| `RELEASE_BLOCKER` | Blocks public v0.1 release |
| `OPTIONAL_FEATURE_BLOCKER` | Blocks only an optional feature |
| `ADVISORY` | Does not block release but requires documentation |

### 5.2 Required release-blocking categories

The following failures block release:

- incorrect formula output,
- public field without trace owner,
- unknown provenance silently reclassified,
- parent ambiguity silently resolved,
- cycle silently removed,
- evidence class misplaced,
- simulation presented as observation,
- forbidden public score emitted,
- raw content leaked in normal logs,
- hidden network call,
- hero golden mismatch,
- nondeterministic fixed-seed output,
- required report section missing,
- unsafe schema operation accepted.

---

## 6. Test ownership and naming

### 6.1 Naming convention

Required pattern:

```text
test_<TRACE_OR_RULE_ID>_<behavior>
```

Examples:

```text
test_T1_expected_one_step_contraction_matches_formula
test_T4_single_root_hhi_is_one
test_PR003_eval_is_rejected
```

### 6.2 One primary owner

Every test must identify one primary:

- `T*` Trace ID,
- or `PR-*` Product Rule ID.

A test may cite additional supporting IDs.

### 6.3 Test metadata

Recommended docstring fields:

```text
Owner:
Source class:
Formula or rule:
Fixture:
Independent oracle:
Public fields protected:
```

### 6.4 Test-to-field coverage

Every public field must be covered by at least:

- one unit or rule test,
- one report-schema test,
- one integration or golden test when the field appears in the hero or required fixture.

---

## 7. Fixture governance

### 7.1 Fixture requirements

Every fixture must include:

- purpose,
- schema version,
- expected observability,
- expected capabilities,
- expected warnings,
- expected errors,
- expected metric values,
- excluded conclusions.

### 7.2 Fixture directory

Recommended structure:

```text
tests/fixtures/
├── hero/
├── minimal_valid/
├── invalid_schema/
├── provenance_partial/
├── provenance_unknown/
├── lineage_complete/
├── lineage_multi_root/
├── lineage_unresolved/
├── lineage_ambiguous/
├── lineage_cycles/
├── version_order/
├── representation_compatible/
├── representation_incompatible/
├── schema_mapping/
├── content_references/
├── weighted/
├── resampling/
├── reopening/
└── security/
```

### 7.3 Fixture immutability

Once a fixture supports a published golden output:

- changes require review,
- old values remain in version history,
- the reason for change must be documented,
- the report schema version must be considered.

### 7.4 No private data

Repository fixtures must use:

- synthetic examples,
- public-like examples with no private source material,
- manually constructed graphs,
- redacted IDs.

### 7.5 Fixture checksums

Release fixtures should have file hashes stored in the golden manifest.

---

# PART I. SPECIFICATION CONSISTENCY VALIDATION

## 8. Specification consistency audit

Before implementation, run a manual or scripted consistency audit across the approved Markdown files.

### 8.1 Required consistency checks

Verify that:

- all canonical fields use the same spelling,
- all enum registries match,
- formula IDs match formulas,
- Trace IDs match theory-map entries,
- report paths match the public field registry,
- error and warning codes match the data specification,
- decision statuses are approved before implementation,
- hero values match across files,
- observability levels match across files,
- deferred concepts remain deferred.

### 8.2 Required cross-file checks

| Concept | Files that must agree |
|---|---|
| `generation` | decisions, definitions, data spec, traceability |
| parent encoding | decisions, definitions, data spec, hero fixture |
| provenance coverage | definitions, data spec, reporting, traceability |
| closure bounds | decisions, definitions, reporting, traceability |
| tail probability class | decisions, definitions, reporting, traceability |
| ancestry HHI | decisions, definitions, reporting, traceability |
| hero Level 4 | decisions, product spec, reporting, traceability |
| collapse restriction | project instructions, product spec, reporting, traceability |

### 8.3 Specification-lint result

Recommended output:

```text
specification_consistency_report.json
```

Required fields:

- files inspected,
- unresolved references,
- duplicate field definitions,
- conflicting enum definitions,
- missing trace owners,
- decision dependencies,
- pass or fail.

### 8.4 Phase 0 gate

Phase 0 does not pass until:

- every blocking decision is approved or deferred,
- every approved choice is propagated,
- consistency audit has no blocking conflict.

---

# PART II. MATHEMATICAL VALIDATION

## 9. Mathematical validation policy

Mathematical validation tests formulas independently from ingestion, reporting, and CLI behavior.

Every mathematical case must include:

- exact input,
- exact expected value,
- derivation,
- tolerance,
- trace owner,
- formula ID,
- assumption list.

### 9.1 Numeric tolerance

Recommended default:

```text
absolute tolerance: 1e-12
relative tolerance: 1e-12
```

Use exact rational comparison when practical.

Monte Carlo tests use distributional tolerances rather than exact path equality, except fixed-seed path tests.

### 9.2 Probability-vector validation

Probability vectors must be:

- finite,
- non-negative,
- nonempty,
- sum to 1 within approved tolerance.

Invalid vectors must be rejected.

---

## 10. F-001 state-frequency validation

Formula:

\[
p_i=\frac{n_i}{N}
\]

### Case F001-A

Counts:

```text
a: 2
b: 1
c: 1
```

Total:

```text
4
```

Expected:

```text
a: 0.5
b: 0.25
c: 0.25
```

Required test:

```text
test_T1_state_frequencies_match_hand_calculation
```

### Case F001-B

One state:

```text
a: 5
```

Expected:

```text
a: 1.0
```

### Invalid cases

- empty count map,
- negative count,
- fractional unweighted count,
- total zero.

---

## 11. F-002 support validation

Support:

\[
\operatorname{supp}(p)=\{i:p_i>0\}
\]

### Case F002-A

Distribution:

```text
a: 0.5
b: 0.5
c: 0.0
```

Expected support:

```text
a
b
```

Expected support size:

```text
2
```

### Case F002-B

Observed state list:

```text
cat
cat
dog
bird
```

Expected support:

```text
bird
cat
dog
```

Expected support size:

```text
3
```

### Required tests

```text
test_T1_zero_probability_state_excluded_from_support
test_T1_observed_support_deduplicates_states
```

---

## 12. F-003 Gini-Simpson validation

Formula:

\[
D=1-\sum_i p_i^2
\]

### Case F003-A: one state

Distribution:

```text
1
```

Expected:

\[
D=0
\]

### Case F003-B: two equal states

Distribution:

```text
1/2
1/2
```

Expected:

\[
D=1-\left(\frac14+\frac14\right)=\frac12
\]

### Case F003-C: four equal states

Expected:

\[
D=1-4\left(\frac1{16}\right)=\frac34
\]

### Case F003-D: uneven distribution

Distribution:

```text
1/2
1/4
1/4
```

Expected:

\[
D
=
1-\left(\frac14+\frac1{16}+\frac1{16}\right)
=
\frac58
=
0.625
\]

### Required tests

```text
test_T1_single_state_diversity_is_zero
test_T1_two_equal_states_diversity_is_one_half
test_T1_four_equal_states_diversity_is_three_quarters
test_T1_uneven_distribution_matches_five_eighths
```

---

## 13. Hero diversity validation

### 13.1 v1 topic distribution

Eight topic states each occur once.

\[
p_i=\frac18
\]

Expected:

\[
D_{v1}
=
1-8\left(\frac1{8}\right)^2
=
1-\frac18
=
\frac78
=
0.875
\]

### 13.2 v2 topic distribution

Counts:

```text
cat: 3
dog: 2
bird: 1
fish: 1
refund: 1
```

Expected:

\[
D_{v2}
=
1-
\left[
\left(\frac38\right)^2
+
\left(\frac28\right)^2
+
3\left(\frac18\right)^2
\right]
\]

\[
D_{v2}
=
1-\frac{16}{64}
=
\frac34
=
0.75
\]

### 13.3 Diversity delta

\[
\Delta D
=
D_{v2}-D_{v1}
=
0.75-0.875
=
-0.125
\]

### Required tests

```text
test_T1_hero_v1_diversity_is_seven_eighths
test_T1_hero_v2_diversity_is_three_quarters
test_T1_hero_diversity_delta_is_negative_one_eighth
```

These values should enter the mathematical golden manifest even when the public hero summary emphasizes support rather than diversity.

---

## 14. F-005 and F-006 support comparison validation

Earlier support:

```text
cat
dog
bird
fish
lizard
turtle
refund
battery
```

Later support:

```text
cat
dog
bird
fish
refund
```

Expected:

\[
\Delta K=5-8=-3
\]

Expected extinct set:

```text
battery
lizard
turtle
```

Expected added set:

```text
empty
```

Expected retention:

\[
R_{\text{support}}
=
\frac58
=
0.625
\]

Required tests:

```text
test_T1_hero_support_delta_is_negative_three
test_T1_hero_support_retention_is_five_eighths
test_T1_hero_extinct_states_match_expected_set
test_T1_support_set_order_is_deterministic
```

---

## 15. F-014 one-step extinction validation

Formula:

\[
P_{\text{extinct,next}}=(1-p_i)^n
\]

### Case F014-A

\[
p_i=0
\]

Expected:

\[
P=1
\]

### Case F014-B

\[
p_i=1
\]

Expected:

\[
P=0
\]

### Case F014-C

\[
p_i=\frac12,\quad n=2
\]

Expected:

\[
P=\left(\frac12\right)^2=\frac14
\]

### Case F014-D

\[
p_i=\frac14,\quad n=4
\]

Expected:

\[
P=\left(\frac34\right)^4
=
\frac{81}{256}
=
0.31640625
\]

### Case F014-E: hero singleton state with \(n=8\)

\[
p_i=\frac18
\]

Expected:

\[
P
=
\left(\frac78\right)^8
=
\frac{5,764,801}{16,777,216}
\approx
0.3436089158
\]

### Case F014-F: hero dog state with \(n=8\)

\[
p_i=\frac14
\]

Expected:

\[
P
=
\left(\frac34\right)^8
=
\frac{6,561}{65,536}
\approx
0.1001129150
\]

### Case F014-G: hero cat state with \(n=8\)

\[
p_i=\frac38
\]

Expected:

\[
P
=
\left(\frac58\right)^8
=
\frac{390,625}{16,777,216}
\approx
0.0232830644
\]

### Ordering property

For fixed \(n>0\):

```text
lower p means higher one-step extinction probability
```

Required tests:

```text
test_T2_probability_boundary_zero
test_T2_probability_boundary_one
test_T2_probability_one_half_n_two
test_T2_probability_one_quarter_n_four
test_T2_hero_singleton_probability
test_T2_hero_dog_probability
test_T2_hero_cat_probability
test_T2_probability_monotone_in_frequency
```

---

## 16. F-015 expected diversity contraction validation

Formula:

\[
\mathbb{E}[D_{t+1}\mid p_t]
=
\left(1-\frac1n\right)D_t
\]

### Case F015-A

\[
D_t=\frac12,\quad n=2
\]

Expected:

\[
\mathbb{E}[D_{t+1}]
=
\frac12\cdot\frac12
=
\frac14
\]

### Case F015-B

\[
D_t=\frac34,\quad n=4
\]

Expected:

\[
\mathbb{E}[D_{t+1}]
=
\frac34\cdot\frac34
=
\frac9{16}
=
0.5625
\]

### Case F015-C: hero v2 distribution with \(n=8\)

\[
D_t=0.75
\]

Expected:

\[
\mathbb{E}[D_{t+1}]
=
\frac78\cdot\frac34
=
\frac{21}{32}
=
0.65625
\]

### Case F015-D: hero v1 distribution with \(n=8\)

\[
D_t=0.875=\frac78
\]

Expected:

\[
\mathbb{E}[D_{t+1}]
=
\frac78\cdot\frac78
=
\frac{49}{64}
=
0.765625
\]

### Multi-step case

\[
D_0=\frac34,\quad n=4,\quad t=2
\]

Expected:

\[
\mathbb{E}[D_2]
=
\left(\frac34\right)^2\frac34
=
\frac{27}{64}
=
0.421875
\]

Required tests:

```text
test_T1_expected_contraction_one_step_n_two
test_T1_expected_contraction_one_step_n_four
test_T1_hero_v2_expected_contraction_n_eight
test_T1_hero_v1_expected_contraction_n_eight
test_T1_expected_contraction_two_steps
```

---

## 17. Closed-resampling process validation

### 17.1 Conditional expectation property

For a fixed distribution \(p\), many Monte Carlo replicates should produce an empirical mean close to \(p\).

This is a statistical sanity test.

It does not replace the exact formula test.

Recommended test parameters:

```text
distribution: [0.5, 0.3, 0.2]
sample size: 100
replicates: 50,000
seed: fixed
```

Acceptance:

- each empirical mean within a predeclared tolerance,
- tolerance justified through standard error.

### 17.2 Absorbing zero property

A state with zero initial probability must remain zero in every closed-resampling path.

### 17.3 Fixed-seed determinism

The same implementation version, parameters, and seed must produce the same path.

### 17.4 Different-seed variability

Different seeds should not be required to produce different paths in every case.

The validation should confirm seed use rather than demand uniqueness.

### 17.5 Distribution normalization

Every simulated distribution must:

- contain finite values,
- contain no negative values,
- sum to 1 within tolerance,
- have frequencies in multiples of \(1/n\).

Required tests:

```text
test_T1_monte_carlo_mean_matches_current_distribution
test_T1_zero_state_never_reappears_under_closed_model
test_T1_fixed_seed_reproduces_path
test_T1_simulated_distribution_is_normalized
test_T1_simulated_frequencies_are_multiples_of_inverse_n
```

---

## 18. F-008 provenance coverage validation

### Case F008-A

Records:

```text
8
```

Matching provenance rows:

```text
8
```

Expected:

\[
P_{\text{row}}=1
\]

### Case F008-B

Records:

```text
8
```

Matching rows:

```text
6
```

Expected:

\[
P_{\text{row}}=\frac68=0.75
\]

### Required-field case

Eight matching rows, seven valid required-field sets.

Expected:

```text
row coverage: 1.0
required-field coverage: 0.875
```

### Grounding-field case

Eight matching rows:

- 4 yes,
- 2 no,
- 2 unknown.

Expected:

\[
P_{\text{grounding}}=\frac68=0.75
\]

Required tests:

```text
test_PR004_full_row_coverage
test_PR004_partial_row_coverage
test_PR004_required_field_coverage_separate
test_PR004_grounding_known_excludes_unknown
```

---

## 19. F-009 and F-010 closure-bound validation

### Case F009-A: complete classification

Total:

```text
8
```

Known closed:

```text
4
```

Unresolved:

```text
0
```

Expected:

\[
C_{\min}=C_{\max}=\frac48=0.5
\]

Interval width:

```text
0
```

### Case F009-B: partial classification

Total:

```text
8
```

Known closed:

```text
3
```

Unresolved:

```text
2
```

Expected:

\[
C_{\min}=\frac38=0.375
\]

\[
C_{\max}=\frac58=0.625
\]

Width:

\[
0.25
\]

### Case F009-C: all unresolved

Total:

```text
8
```

Known closed:

```text
0
```

Unresolved:

```text
8
```

Expected interval:

```text
0.0 to 1.0
```

### Required invariants

\[
0\leq C_{\min}\leq C_{\max}\leq1
\]

\[
C_{\max}-C_{\min}
=
\frac{N_U}{N}
\]

Required tests:

```text
test_T3_complete_classification_has_zero_width
test_T3_partial_classification_matches_three_eighths_to_five_eighths
test_T3_all_unresolved_spans_zero_to_one
test_T3_lower_never_exceeds_upper
test_T3_width_equals_unresolved_share
```

---

## 20. Hero direct and lineage closure validation

### 20.1 Direct classification

For v2:

- 4 records declare external grounding `yes`,
- 4 records declare external grounding `no`,
- 0 unresolved.

Expected direct interval:

\[
0.5\text{ to }0.5
\]

### 20.2 Lineage classification candidate

Every v2 record has a resolved path to at least one validated external root.

Under the recommended lineage classification:

- lineage-known-grounded: 8,
- lineage-known-closed: 0,
- lineage-unresolved: 0.

Expected lineage interval:

\[
0.0\text{ to }0.0
\]

This candidate golden value requires approval of `UD-010` and the external-root rules.

Required tests after approval:

```text
test_T3_hero_direct_closure_is_one_half
test_T3_hero_lineage_closure_is_zero
test_T3_hero_direct_and_lineage_bounds_remain_distinct
```

The report must explain why direct and lineage results answer different questions.

---

## 21. F-011 ancestor-incidence validation

### Case F011-A

Root sets:

```text
r1: {a}
r2: {a}
r3: {b}
r4: {a, b}
```

Expected incidence:

```text
a: 3
b: 2
```

All-record shares:

```text
a: 3/4
b: 1/2
```

Required tests:

```text
test_T4_incidence_counts_reachable_root_membership
test_T4_multi_root_record_contributes_to_each_incidence
```

---

## 22. F-012 ancestry HHI validation

### Case F012-A: one root

Shares:

```text
1.0
```

Expected:

\[
HHI=1
\]

Effective roots:

\[
1
\]

### Case F012-B: two equal roots

Shares:

```text
0.5
0.5
```

Expected:

\[
HHI=0.5
\]

Effective roots:

\[
2
\]

### Case F012-C: four equal roots

Expected:

\[
HHI=4\left(\frac14\right)^2=\frac14
\]

Effective roots:

\[
4
\]

### Case F012-D: uneven shares

Shares:

```text
0.75
0.25
```

Expected:

\[
HHI
=
0.75^2+0.25^2
=
0.625
\]

Effective roots:

\[
1.6
\]

### Required tests

```text
test_T4_single_root_hhi_is_one
test_T4_two_equal_roots_hhi_is_one_half
test_T4_four_equal_roots_hhi_is_one_quarter
test_T4_uneven_root_hhi_is_five_eighths
test_T4_effective_roots_is_inverse_hhi
```

---

## 23. Hero ancestry validation

v2 root incidences:

```text
v1::v1_01: 3
v1::v1_02: 2
v1::v1_03: 1
v1::v1_04: 1
v1::v1_07: 1
```

Every v2 record has one reachable external root.

Fractional shares:

```text
3/8
2/8
1/8
1/8
1/8
```

Expected HHI:

\[
HHI
=
\frac{9+4+1+1+1}{64}
=
\frac{16}{64}
=
0.25
\]

Expected effective external-root count:

\[
\frac1{0.25}=4
\]

Expected distinct root count:

```text
5
```

Required tests after `UD-014` approval:

```text
test_T4_hero_distinct_roots_is_five
test_T4_hero_hhi_is_one_quarter
test_T4_hero_effective_roots_is_four
test_T4_hero_top_root_incidence_is_three
test_T4_hero_top_root_share_is_three_eighths
```

---

## 24. Multi-root allocation validation

### Fixture

Resolved root sets:

```text
c1: {a}
c2: {a, b}
c3: {b}
```

Fractional contributions:

```text
c1 -> a: 1
c2 -> a: 1/2, b: 1/2
c3 -> b: 1
```

Aggregate mass:

```text
a: 1.5
b: 1.5
```

Normalized shares:

```text
a: 0.5
b: 0.5
```

Expected:

```text
HHI: 0.5
effective roots: 2
```

Required tests:

```text
test_T4_multi_root_mass_per_record_sums_to_one
test_T4_multi_root_fixture_root_shares_are_equal
test_T4_multi_root_fixture_hhi_is_one_half
```

---

## 25. F-017 reopening validation

Mixture:

\[
s=(1-\lambda)p+\lambda r
\]

### Case F017-A: closed boundary

\[
\lambda=0
\]

Expected:

\[
s=p
\]

### Case F017-B: fully external source

\[
\lambda=1
\]

Expected:

\[
s=r
\]

### Case F017-C: equal mixture

\[
p=(1,0)
\]

\[
r=(0,1)
\]

\[
\lambda=\frac12
\]

Expected:

\[
s=\left(\frac12,\frac12\right)
\]

### Case F017-D: state re-entry probability before sampling

Internal:

```text
a: 1
b: 0
```

External:

```text
a: 0.8
b: 0.2
```

\[
\lambda=0.25
\]

Expected mixed probability for `b`:

\[
0.25\cdot0.2=0.05
\]

The state has positive reachability before resampling.

### Required tests

```text
test_T5_lambda_zero_returns_internal_distribution
test_T5_lambda_one_returns_external_distribution
test_T5_equal_mixture_matches_half_half
test_T5_absent_internal_state_gains_positive_probability
test_T5_mixture_remains_normalized
test_T5_lambda_outside_zero_one_rejected
```

---

## 26. External-reference loss validation

This metric remains optional until its public trace ownership is approved.

Definition:

\[
L=\sum_i(p_i-q_i)^2
\]

### Case

\[
p=(1,0)
\]

\[
q=(0.5,0.5)
\]

Expected:

\[
L=(0.5)^2+(-0.5)^2=0.5
\]

Under sample size \(n=2\), \(D=0\) for \(p=(1,0)\), so expected next loss remains 0.5.

Required deferred tests:

```text
test_TM_M06_external_reference_loss_matches_half
test_TM_M06_zero_diversity_adds_zero_expected_variance
```

These tests may remain `xfail` only while the public metric remains deferred.

---

# PART III. DATA-CONTRACT VALIDATION

## 27. Records ingestion validation

### 27.1 Required valid cases

- minimal valid CSV,
- minimal valid JSONL,
- valid CSV with quoted commas,
- valid JSONL with Unicode content,
- optional valid Parquet,
- multiple versions in one source,
- separate comparison files.

### 27.2 Required invalid cases

- file missing,
- unsupported extension,
- invalid UTF-8,
- malformed CSV,
- malformed JSONL,
- duplicate headers,
- missing `record_id`,
- missing `dataset_version`,
- missing `content`,
- duplicate composite key,
- empty dataset,
- empty required content,
- invalid weight.

### 27.3 Required tests

```text
test_PR002_minimal_csv_loads
test_PR002_minimal_jsonl_loads
test_PR002_csv_quoted_comma_preserved
test_PR002_unicode_content_preserved
test_PR002_missing_file_fails
test_PR002_invalid_utf8_fails
test_PR002_malformed_csv_fails
test_PR002_malformed_jsonl_fails
test_PR001_duplicate_composite_key_fails
test_PR002_empty_dataset_fails
test_PR002_empty_content_fails
test_PR005_negative_weight_fails
```

---

## 28. CSV list serialization validation

Required cases for `parent_ids`:

- blank field,
- `[]`,
- one composite parent,
- multiple composite parents,
- malformed JSON,
- JSON scalar,
- non-string list item,
- duplicate parent.

Expected behavior:

| Case | Expected |
|---|---|
| blank | empty list |
| `[]` | empty list |
| valid array | parsed list |
| malformed JSON | `E_PARENT_FORMAT` |
| scalar | `E_PARENT_FORMAT` |
| non-string item | `E_PARENT_FORMAT` |
| duplicate reference | warning plus approved deterministic deduplication |

Required tests:

```text
test_PR008_blank_parent_field_is_empty_list
test_PR008_json_empty_array_is_empty_list
test_PR008_multiple_parent_array_parses
test_PR008_malformed_parent_json_fails
test_PR008_parent_scalar_fails
test_PR008_parent_non_string_item_fails
test_PR008_duplicate_parent_warns
```

---

## 29. Provenance join validation

### 29.1 Valid cases

- complete matching provenance,
- partial matching provenance,
- explicit unknown source type,
- explicit unknown grounding,
- mixed source type,
- estimated confidence.

### 29.2 Invalid cases

- duplicate provenance row,
- provenance row without record,
- invalid enum,
- invalid generation,
- invalid boolean,
- conflicting identity.

### 29.3 Required tests

```text
test_PR004_complete_provenance_join
test_PR004_missing_record_provenance_warns
test_PR004_explicit_unknown_preserved
test_PR005_mixed_preserved
test_PR004_estimated_confidence_preserved
test_PR004_duplicate_provenance_row_fails
test_PR004_unmatched_provenance_row_fails
test_PR004_invalid_source_enum_fails
test_PR004_invalid_grounding_enum_fails
test_PR009_negative_generation_fails
```

---

## 30. Source type and grounding separation

Construct a crossed fixture:

| Record | Source type | External grounding |
|---|---|---|
| r1 | human | yes |
| r2 | human | no |
| r3 | synthetic | yes |
| r4 | synthetic | no |
| r5 | mixed | unknown |
| r6 | sensor | no |
| r7 | unknown | yes |
| r8 | unknown | unknown |

Validation must preserve every pair.

Required tests:

```text
test_PR005_human_no_remains_known_closed_directly
test_PR005_synthetic_yes_remains_known_open_directly
test_PR005_mixed_unknown_remains_unresolved
test_PR005_sensor_no_remains_known_closed_directly
test_PR005_unknown_source_yes_remains_known_open_directly
test_PR005_source_type_never_overwrites_grounding
```

---

## 31. Schema-mapping validation

### 31.1 Valid operations

- rename,
- trim,
- cast string,
- cast integer,
- cast float,
- cast boolean,
- parse datetime,
- parse JSON list,
- constant,
- coalesce,
- map values,
- normalize whitespace,
- lowercase,
- uppercase.

### 31.2 Invalid operations

- `eval`,
- `exec`,
- shell,
- subprocess,
- network call,
- remote script,
- dynamic import,
- user-defined callback,
- executable template.

### 31.3 Determinism

The same source row and mapping must produce the same normalized row.

### 31.4 Required tests

```text
test_PR003_rename_succeeds
test_PR003_trim_is_explicit
test_PR003_integer_cast_rejects_fraction
test_PR003_float_cast_rejects_nan
test_PR003_boolean_mapping_is_explicit
test_PR003_datetime_parse_uses_declared_format
test_PR003_json_list_parse_succeeds
test_PR003_constant_assignment_succeeds
test_PR003_coalesce_uses_first_nonmissing
test_PR003_map_values_unmapped_error
test_PR003_operation_order_is_stable
test_PR003_eval_rejected
test_PR003_subprocess_rejected
test_PR003_network_rejected
test_PR003_dynamic_import_rejected
```

---

## 32. Version-order validation

Required valid cases:

- explicit ordered list,
- integer-rank map,
- timestamp order,
- CLI order.

Required invalid or unavailable cases:

- conflicting sources,
- missing version,
- duplicate rank,
- equal timestamps without tie-break,
- multiple versions without order,
- lexical filename temptation.

Required tests:

```text
test_PR007_explicit_order_list
test_PR007_rank_map_order
test_PR007_timezone_timestamp_order
test_PR007_cli_order_recorded
test_PR007_conflicting_order_fails
test_PR007_duplicate_rank_fails
test_PR007_equal_timestamp_without_tiebreak_fails
test_PR007_missing_order_blocks_longitudinal
test_PR007_lexical_filename_order_not_used
```

---

## 33. Representation validation

### 33.1 Valid cases

- explicit topic,
- explicit label,
- content-hash record form,
- embedding clusters with metadata,
- compatible mapping across versions.

### 33.2 Missing-value policies

Validate:

- exclude,
- error,
- explicit missing state.

### 33.3 Invalid cases

- configured field missing,
- semantic claim from content hash,
- incompatible taxonomy version,
- one-to-many mapping without allocation rule,
- embedding dimension mismatch,
- missing cluster metadata.

### 33.4 Required tests

```text
test_T1_topic_representation
test_T1_label_representation
test_PR006_content_hash_labeled_record_form
test_T1_missing_state_exclude_reduces_coverage
test_T1_missing_state_error_blocks_metric
test_T1_explicit_missing_state_is_counted
test_T1_compatible_versions_compare
test_T1_incompatible_versions_block_support_delta
test_T1_one_to_many_state_mapping_rejected
test_T1_embedding_dimension_mismatch_rejected
```

---

# PART IV. LINEAGE VALIDATION

## 34. Parent-resolution validation

Required cases:

- one composite parent,
- multiple composite parents,
- unique bare parent compatibility,
- unresolved bare parent,
- ambiguous bare parent,
- future-version parent,
- same-version acyclic parent,
- self-parent.

Required tests:

```text
test_PR008_composite_parent_resolves
test_PR008_multiple_composite_parents_resolve
test_PR008_unique_bare_parent_warns
test_PR008_unresolved_bare_parent_warns
test_PR008_ambiguous_bare_parent_fails
test_PR008_future_parent_fails
test_PR008_same_version_acyclic_parent_allowed
test_T6_self_parent_detected_as_cycle
```

---

## 35. Cycle validation

Fixtures:

1. empty graph,
2. one root,
3. simple chain,
4. branching DAG,
5. self-cycle,
6. two-node cycle,
7. longer cycle,
8. disconnected graph with one cyclic component.

Required tests:

```text
test_T6_empty_graph_acyclic
test_T6_single_root_acyclic
test_T6_chain_acyclic
test_T6_branching_graph_acyclic
test_T6_self_cycle_detected
test_T6_two_node_cycle_detected
test_T6_long_cycle_detected
test_T6_disconnected_cycle_detected
```

Required behavior:

- cycle nodes listed,
- lineage capability unavailable or partial according to scope,
- no edge silently removed,
- non-lineage capabilities preserved when possible.

---

## 36. External-root validation

Required cases:

- grounded parentless root,
- ungrounded parentless root,
- unknown-grounding parentless root,
- grounded carryover with one parent,
- new independent external input,
- multi-parent child,
- unresolved upstream parent.

Required tests:

```text
test_T4_grounded_parentless_record_is_external_root
test_T4_ungrounded_parentless_record_not_external_root
test_T4_unknown_parentless_root_remains_unresolved
test_T4_grounded_carryover_preserves_parent_root
test_T4_carryover_does_not_multiply_roots
test_T4_declared_new_external_input_can_add_root
test_T4_multi_parent_child_unions_root_sets
test_T4_unresolved_upstream_parent_reduces_lineage_coverage
```

---

## 37. Generation validation

Required cases:

- grounded root generation 0,
- grounded carryover generation 0 with lineage depth 1,
- ungrounded child generation 1,
- second ungrounded descendant generation 2,
- unknown grounding,
- unresolved parent,
- mismatch warning,
- strict-mode promotion.

Required tests:

```text
test_PR009_grounded_root_generation_zero
test_PR009_grounded_carryover_generation_zero_depth_one
test_PR009_ungrounded_child_generation_one
test_PR009_second_ungrounded_descendant_generation_two
test_PR009_unknown_grounding_expected_generation_unavailable
test_PR009_unresolved_parent_expected_generation_unavailable
test_PR009_mismatch_emits_warning
test_PR009_strict_mode_promotes_selected_mismatch
```

---

# PART V. OBSERVABILITY VALIDATION

## 38. Maximum-level tests

### Level 0 fixture

- readable records file,
- minimal schema,
- no analyzable content or representation beyond inventory.

Expected:

```text
maximum level: 0
```

### Level 1 fixture

- valid records,
- topic or content-hash representation,
- no provenance.

Expected:

```text
maximum level: 1
```

### Level 2 fixture

- at least one valid provenance row,
- no parent path.

Expected:

```text
maximum level: 2
```

### Level 3 fixture

- valid resolvable lineage path,
- one dataset version.

Expected:

```text
maximum level: 3
```

### Level 4 fixture

- two ordered compatible versions.

Expected:

```text
maximum level: 4
```

### Level 5 fixture

- valid approved scenario configuration.

Expected:

```text
maximum level: 5
intervention_simulation: experimental
```

Required tests:

```text
test_PR010_level_zero_fixture
test_PR010_level_one_fixture
test_PR010_level_two_fixture
test_PR010_level_three_fixture
test_PR010_level_four_fixture
test_PR010_level_five_fixture
test_PR010_hero_level_four
```

---

## 39. Capability-matrix tests

Required cases:

### Case A

Level 4 dataset versions, no model outcomes.

Expected:

```text
dataset_longitudinal: available
model_longitudinal: unavailable
```

### Case B

Partial provenance.

Expected:

```text
provenance: partial
```

with exact coverage.

### Case C

Partial lineage.

Expected:

```text
lineage: partial
```

with unresolved-parent count.

### Case D

Valid scenario.

Expected:

```text
intervention_simulation: experimental
```

### Case E

Content hashes only, user asks for semantic support.

Expected:

```text
content_diagnostics: partial
```

or requested semantic capability unavailable, with record-form support preserved.

Required tests:

```text
test_PR011_level_four_model_longitudinal_unavailable
test_PR011_partial_provenance_has_coverage
test_PR011_partial_lineage_has_coverage
test_PR011_scenario_is_experimental
test_PR011_record_form_does_not_claim_semantic_capability
```

---

# PART VI. REPORT AND GOLDEN VALIDATION

## 40. JSON schema validation

Every successful full report must contain:

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
test_PR013_required_top_level_keys
test_PR013_empty_sections_preserved
test_PR013_report_schema_version
test_PR013_json_has_no_nan
test_PR013_json_has_no_infinity
test_PR013_public_field_types_match_registry
```

### 40.1 Stable types

A field must not change among:

- number,
- string,
- object,
- array,
- null,

within the same report-schema version except where the schema explicitly allows null for unavailable.

---

## 41. Evidence-class placement validation

Required assertions:

| Result | Required section |
|---|---|
| record count | observed facts |
| provenance row coverage | observed facts |
| Gini-Simpson diversity | derived metrics |
| closure bounds | derived metrics |
| ancestry HHI | derived metrics |
| support-contraction warning | proxy signals |
| tail fragility warning | proxy signals |
| one-step extinction probability | simulations |
| external reopening | simulations |
| universal collapse | unavailable conclusions |

Required tests:

```text
test_PR012_record_count_observed
test_PR012_diversity_derived
test_PR012_closure_bounds_derived
test_PR012_ancestry_hhi_derived
test_PR012_support_warning_proxy
test_PR012_tail_warning_proxy
test_PR012_extinction_probability_simulation
test_PR012_reopening_simulation
test_PR012_universal_collapse_unavailable
```

---

## 42. Interval-reporting validation

Closure exposure must show:

- lower bound,
- upper bound,
- interval width,
- unresolved count,
- denominator.

Required tests:

```text
test_T3_json_preserves_both_bounds
test_T3_markdown_renders_range
test_T3_midpoint_absent
test_T3_interval_width_rendered
test_T3_unresolved_count_rendered
```

---

## 43. Simulation-reporting validation

Every simulation must include:

- model,
- parameters,
- assumptions,
- seed where stochastic,
- horizon,
- replicate count,
- limitations,
- `experimental` status where required.

Required tests:

```text
test_T1_resampling_report_has_assumptions
test_T2_extinction_report_has_one_step_horizon
test_T2_extinction_report_has_resample_size
test_T5_reopening_report_has_lambda
test_T5_reopening_report_has_external_distribution
test_T5_reopening_report_experimental
test_simulation_not_rendered_as_observed
```

---

## 44. Unavailable-conclusion validation

Required hero entries:

```text
model_performance_decline
causal_ancestor_effect
universal_integrity
universal_collapse_prediction
```

Every entry must include:

- reason code,
- blocking evidence,
- next metadata,
- related capability.

Required tests:

```text
test_PR014_hero_model_performance_unavailable
test_PR014_hero_causal_ancestor_unavailable
test_PR014_hero_universal_integrity_unavailable
test_PR014_hero_universal_collapse_unavailable
test_PR014_unavailable_not_false_language
test_PR014_unavailable_not_rendered_as_zero
```

---

## 45. Report-language validation

### 45.1 Forbidden direct-conclusion fragments

Golden reports must not contain these fragments as direct toolkit conclusions:

```text
collapse score
entropy caused
proved failure
ancestor caused the error
human data is safe
synthetic data caused collapse
will fail after
universal integrity score
universal entropy score
```

### 45.2 Required mechanism language

When support contracts, the report should mention:

- selected representation,
- earlier and later versions,
- observed missing states.

When ancestry concentrates, the report should mention:

- reachable ancestry,
- incidence,
- topology,
- noncausal limitation.

### 45.3 Required tests

```text
test_PR018_forbidden_fragments_absent
test_PR018_support_language_names_representation
test_PR018_extinction_language_is_version_bound
test_PR018_ancestry_language_is_noncausal
test_PR018_entropy_does_not_replace_mechanism
```

---

## 46. Markdown rendering validation

Required checks:

- heading present,
- section order correct,
- capability table present,
- unavailable conclusions visible,
- no raw content in standard summary unless explicitly requested,
- percentages and metric precision follow reporting rules,
- unavailable shown as `Unavailable`,
- tables remain readable.

Required tests:

```text
test_PR013_markdown_heading
test_PR013_markdown_section_order
test_PR013_capability_table_present
test_PR014_unavailable_visible_in_markdown
test_PR013_unavailable_not_dash_or_zero
test_PR013_markdown_numeric_format
```

---

## 47. Optional HTML validation

When HTML is implemented:

- self-contained,
- no remote scripts,
- no remote CSS,
- no external fonts,
- user strings escaped,
- redaction preserved,
- section order preserved.

Required optional tests:

```text
test_PR013_html_self_contained
test_PR013_html_no_remote_resources
test_PR013_html_escapes_user_metadata
test_PR015_html_redaction
```

HTML failure blocks only the optional feature unless HTML becomes required.

---

# PART VII. HERO GOLDEN VALIDATION

## 48. Hero fixture inputs

Required files:

```text
records_v1.csv
records_v2.csv
provenance.csv
version_order.json
representation.json
EXPECTED_OUTPUTS.md
```

### 48.1 File content

Hero records and provenance must match `DATA_AND_PROVENANCE_SPEC.md`.

### 48.2 Input hashes

Golden manifest stores approved SHA-256 hashes.

### 48.3 No manual edits

The hero command must run from repository checkout without modifying fixture files.

---

## 49. Hero required golden values

### 49.1 Input and observability

```text
v1 record count: 8
v2 record count: 8
maximum observability level: 4
representation: topic
```

### 49.2 Capability matrix

```text
ingestion: available
content_diagnostics: available
provenance: available
lineage: available
dataset_longitudinal: available
model_longitudinal: unavailable
intervention_simulation: unavailable
```

### 49.3 Support and diversity

```text
v1 support size: 8
v2 support size: 5
support delta: -3
support retention: 0.625
v1 Gini-Simpson diversity: 0.875
v2 Gini-Simpson diversity: 0.75
diversity delta: -0.125
```

### 49.4 Extinct observed states

```text
battery
lizard
turtle
```

Order must be deterministic.

### 49.5 Provenance

```text
v2 provenance row coverage: 1.0
v2 required-field coverage: 1.0
v2 grounding-field coverage: 1.0
v2 human share: 0.5
v2 synthetic share: 0.5
v2 mixed share: 0.0
v2 sensor share: 0.0
v2 unknown share: 0.0
v2 missing provenance share: 0.0
```

### 49.6 Closure bounds

Pending `UD-010` approval:

```text
direct closure lower bound: 0.5
direct closure upper bound: 0.5
direct interval width: 0.0
lineage closure lower bound: 0.0
lineage closure upper bound: 0.0
lineage interval width: 0.0
```

### 49.7 Lineage

```text
cycle detected: false
declared parent edges for v2: 8
resolved parent edges for v2: 8
unresolved parent edges for v2: 0
distinct external roots supporting v2: 5
top shared root: v1::v1_01
top shared-root incidence: 3
top shared-root incidence share: 0.375
ancestry HHI: 0.25
effective external-root count: 4.0
```

Ancestry HHI values require `UD-014` approval.

### 49.8 Proxy signals

Required:

```text
support_contraction: present
shared_ancestry_dependence: present
```

No universal risk level is required.

### 49.9 Simulations

Default hero audit:

```text
none
```

### 49.10 Unavailable conclusions

Required:

```text
model_performance_decline
causal_ancestor_effect
universal_integrity
universal_collapse_prediction
```

### 49.11 Privacy and execution

```text
network call count: 0
raw content in normal logs: none
deterministic: true
```

---

## 50. Hero command validation

Recommended command:

```bash
rit audit \
  --records examples/hero/records_v2.csv \
  --provenance examples/hero/provenance.csv \
  --compare examples/hero/records_v1.csv \
  --version-order examples/hero/version_order.json \
  --config examples/hero/config.json \
  --out out/hero
```

Required outcomes:

- exit code 0,
- JSON report created,
- Markdown report created,
- output paths printed,
- no network access,
- runtime target met,
- golden values match.

Required test:

```text
test_hero_end_to_end
```

---

## 51. Golden comparison rules

### 51.1 Normalize variable metadata

Golden comparison may normalize:

- run ID,
- start timestamp,
- end timestamp,
- duration,
- absolute file paths,
- platform string.

### 51.2 Do not normalize analytical values

Golden comparison must preserve:

- counts,
- ratios,
- field names,
- evidence classes,
- capability statuses,
- warning codes,
- error codes,
- limitations,
- unavailable conclusions.

### 51.3 Golden change approval

A golden change requires:

- reason,
- affected trace IDs,
- affected public fields,
- updated hand calculation when numerical,
- Theory Owner approval for theory-relevant meaning,
- Technical Maintainer approval.

---

# PART VIII. PRIVACY AND SECURITY VALIDATION

## 52. Normal-log privacy tests

Normal logs must not contain:

- raw content,
- notes,
- provenance notes,
- full embeddings,
- local content payloads,
- credentials.

Required tests:

```text
test_PR015_normal_log_excludes_raw_content
test_PR015_normal_log_excludes_notes
test_PR015_normal_log_excludes_embeddings
test_PR015_error_message_uses_record_key_not_content
```

Use sentinel secret strings inside fixtures to detect leakage.

---

## 53. Redacted-report tests

Required checks:

- content absent,
- notes absent,
- paths hidden,
- IDs hashed when configured,
- metrics unchanged,
- stable hash behavior documented.

Required tests:

```text
test_PR015_redacted_json_hides_sentinel_content
test_PR015_redacted_markdown_hides_sentinel_notes
test_PR015_redacted_paths_removed
test_PR015_redacted_ids_hashed
test_PR015_redaction_does_not_change_metrics
```

---

## 54. No-network validation

### 54.1 Required behavior

Hero and standard audits require no network.

### 54.2 Validation methods

Use one or more:

- network namespace isolation,
- socket monkeypatch that raises,
- firewall rule in CI,
- dependency audit,
- runtime network-call counter.

### 54.3 Required tests

```text
test_no_network_hero
test_PR017_http_content_reference_rejected
test_PR003_network_mapping_operation_rejected
test_optional_html_has_no_remote_resource
```

---

## 55. Content-reference security tests

Required attack cases:

- `../` traversal,
- absolute path outside base,
- symlink escape,
- network URI,
- missing file,
- oversized file,
- invalid UTF-8 content file.

Required tests:

```text
test_PR017_parent_traversal_blocked
test_PR017_absolute_path_blocked_by_default
test_PR017_symlink_escape_blocked
test_PR017_network_uri_blocked
test_PR017_missing_file_error
test_PR017_size_limit_enforced
test_PR017_invalid_text_encoding_error
```

---

## 56. Schema-execution security tests

Malicious mapping fixtures should attempt:

- Python expression,
- shell command,
- subprocess,
- environment-variable exfiltration,
- dynamic import,
- remote request,
- template evaluation.

Expected:

```text
E_MAPPING_UNSAFE_TRANSFORM
```

Required tests:

```text
test_PR003_python_expression_rejected
test_PR003_shell_command_rejected
test_PR003_subprocess_rejected
test_PR003_environment_access_rejected
test_PR003_dynamic_import_rejected
test_PR003_remote_request_rejected
test_PR003_template_execution_rejected
```

---

## 57. CSV export safety tests

When normalized CSV export exists:

- cells beginning with formula markers must be protected,
- JSONL export may preserve raw string values,
- protection behavior must be documented.

Required optional tests:

```text
test_csv_export_formula_prefix_escaped
test_jsonl_export_preserves_literal_string
```

---

# PART IX. DETERMINISM AND COMPATIBILITY

## 58. Determinism tests

Required stable behavior:

- sort order,
- hash algorithm,
- configuration resolution,
- fixed-seed simulation,
- report field order where specified,
- warning aggregation,
- ancestor ranking.

Required tests:

```text
test_PR016_stable_state_order
test_PR016_stable_ancestor_order
test_PR016_stable_warning_order
test_PR016_fixed_seed_path
test_PR016_same_config_same_hash
test_PR016_same_inputs_same_analytical_json
```

---

## 59. Cross-platform compatibility

Recommended CI matrix:

- Ubuntu,
- Windows,
- Python 3.11,
- Python 3.12.

Optional before official release:

- macOS,
- Python 3.13 after dependency verification.

### 59.1 Required compatibility checks

- path handling,
- CRLF and LF,
- UTF-8,
- floating-point tolerance,
- CLI quoting,
- file hashing,
- deterministic sorting.

### 59.2 Required tests

```text
test_cross_platform_newline_parsing
test_cross_platform_file_hash_bytes
test_cross_platform_path_redaction
test_cross_platform_cli_hero
```

---

## 60. Dependency compatibility

Every required dependency must be tested at:

- minimum supported version,
- current pinned development version,
- latest compatible version where practical.

Optional extras must fail gracefully when absent.

Required tests:

```text
test_parquet_without_extra_has_clear_error
test_parquet_with_extra_loads
test_optional_html_dependency_absence_does_not_break_core
```

---

# PART X. PERFORMANCE VALIDATION

## 61. Performance principles

Performance tests must not weaken correctness or privacy.

Benchmarks should record:

- hardware,
- operating system,
- Python version,
- dependency versions,
- input size,
- runtime,
- peak memory where available.

### 61.1 Hero target

Required:

```text
under 5 seconds on a common laptop CPU
```

Includes:

- load,
- validate,
- observability,
- required metrics,
- JSON,
- Markdown.

### 61.2 Standard audit target

Recommended scale:

```text
approximately 100,000 records
```

Targeted operations:

- metadata loading,
- joins,
- source shares,
- coverage,
- support and diversity,
- sparse lineage that fits memory.

### 61.3 Pairwise similarity

No general exact all-pairs performance promise.

The toolkit must block or warn before impractical quadratic work.

---

## 62. Performance benchmark fixtures

### 62.1 Hero benchmark

16 records total plus provenance.

### 62.2 Metadata benchmark

100,000 records with:

- five source classes,
- partial provenance,
- no content similarity,
- simple representation.

### 62.3 Sparse-lineage benchmark

100,000 records with average parent count near 1 and acyclic structure.

### 62.4 High-fan-in boundary fixture

Smaller graph with controlled multi-parent fan-in to test memory and traversal behavior.

### 62.5 Duplicate benchmark

100,000 short records with repeated content patterns.

---

## 63. Performance acceptance

### 63.1 Required release evidence

- hero runtime,
- metadata-audit runtime,
- peak memory estimate,
- benchmark configuration,
- no hidden network calls.

### 63.2 Regression policy

Recommended threshold:

- more than 20 percent slowdown on the same benchmark requires review,
- more than 50 percent memory growth requires review.

Performance regression alone may be advisory before a formal baseline is approved.

Failure to meet the published hero target is a release blocker.

---

# PART XI. PROPERTY AND METAMORPHIC VALIDATION

## 64. Purpose

Property tests validate general invariants beyond fixed examples.

A property test supplements exact hand-calculated cases.

It does not replace them.

---

## 65. Distribution properties

Required properties:

- frequencies sum to 1,
- Gini-Simpson diversity remains within valid range,
- one-state diversity equals zero,
- permutation of records does not change distribution metrics,
- duplicating every record equally preserves frequencies and diversity,
- state renaming preserves numerical metrics.

Required tests:

```text
test_T1_frequency_sum_property
test_T1_diversity_range_property
test_T1_record_permutation_invariance
test_T1_uniform_duplication_invariance
test_T1_state_rename_invariance
```

---

## 66. Support-comparison properties

Required properties:

- comparing a support set to itself gives zero delta and retention 1,
- extinct and added sets are disjoint,
- reversing comparison swaps added and extinct sets,
- support delta equals added count minus loss count.

Required tests:

```text
test_T1_identity_comparison
test_T1_added_extinct_disjoint
test_T1_reverse_comparison_swaps_sets
test_T1_delta_equals_added_minus_lost
```

---

## 67. Extinction-probability properties

For fixed \(n\):

- probability decreases as \(p\) increases.

For fixed \(0<p<1\):

- probability decreases as \(n\) increases.

Boundary:

- \(p=0\) gives 1,
- \(p=1\) gives 0.

Required tests:

```text
test_T2_probability_decreases_with_frequency
test_T2_probability_decreases_with_sample_size
test_T2_probability_within_zero_one
```

---

## 68. Closure-bound properties

Required properties:

- lower bound at most upper bound,
- interval width equals unresolved share,
- resolving an unknown as open cannot increase lower bound,
- resolving an unknown as closed cannot decrease lower bound,
- complete classification gives zero width.

Required tests:

```text
test_T3_bounds_order_property
test_T3_width_property
test_T3_resolve_unknown_open_narrows_upper
test_T3_resolve_unknown_closed_raises_lower
test_T3_complete_classification_zero_width_property
```

---

## 69. Ancestry properties

Required properties:

- each externally rooted record contributes total fractional mass 1,
- normalized root shares sum to 1,
- HHI lies in \([1/K,1]\) for \(K\) roots,
- effective root count lies in \([1,K]\),
- record-order permutation does not change ancestry metrics,
- root-ID renaming does not change numerical metrics.

Required tests:

```text
test_T4_fractional_mass_per_record_property
test_T4_root_share_sum_property
test_T4_hhi_range_property
test_T4_effective_root_range_property
test_T4_record_order_invariance
test_T4_root_rename_invariance
```

---

## 70. Reopening properties

Required properties:

- \(\lambda=0\) returns internal distribution,
- \(\lambda=1\) returns external distribution,
- mixture remains normalized,
- state absent internally and present externally gains positive pre-sampling probability when \(\lambda>0\),
- mixture is linear in \(\lambda\).

Required tests:

```text
test_T5_lambda_boundary_properties
test_T5_mixture_normalization_property
test_T5_reachability_property
test_T5_linearity_property
```

---

# PART XII. CLI AND PACKAGE VALIDATION

## 71. Installation validation

Required install modes:

- editable development install,
- built wheel install,
- source distribution install where supported.

Required checks:

- package imports,
- CLI entrypoint exists,
- version command works,
- no network required for core install after dependencies are available.

Required tests:

```text
test_package_import
test_cli_version
test_wheel_install_smoke
test_sdist_install_smoke
```

---

## 72. CLI command validation

Recommended commands:

```text
rit audit
rit validate
rit example
rit version
```

Required behavior:

- help text,
- required argument validation,
- exit codes,
- concise status,
- output paths,
- no raw content in console,
- structured error output where possible.

Required tests:

```text
test_cli_help
test_cli_audit_minimal
test_cli_validate_invalid_input
test_cli_example_runs_hero
test_cli_version
test_cli_missing_records_argument
test_cli_output_directory_created
test_cli_raw_content_not_printed
```

---

## 73. CLI exit-code validation

Recommended codes:

| Code | Meaning |
|---:|---|
| 0 | completed |
| 1 | input or validation error |
| 2 | configuration error |
| 3 | lineage graph error |
| 4 | internal software error |

Required tests:

```text
test_cli_exit_zero_success
test_cli_exit_one_invalid_input
test_cli_exit_two_invalid_config
test_cli_exit_three_lineage_cycle
test_cli_internal_error_is_sanitized
```

Exact codes remain subject to technical approval.

---

# PART XIII. EMPIRICAL USEFULNESS VALIDATION

## 74. Purpose

Empirical validation asks whether the toolkit produces useful, honest output on realistic workflows before large-scale calibration.

It does not attempt to prove a universal collapse threshold.

### 74.1 Required v0.1 empirical checks

1. hero example,
2. one partial-provenance workflow,
3. one realistic multi-version workflow,
4. one lineage workflow with shared ancestry,
5. one failure workflow with incomplete metadata.

### 74.2 Candidate public-like example

A small publicly redistributable or manually synthesized example should contain:

- multiple dataset versions,
- partial source metadata,
- at least one tail state,
- at least one shared ancestor,
- no private content.

### 74.3 Reviewer questions

The Domain Validator should answer:

- Can the report be understood without author explanation?
- Are observed and simulated results clearly separated?
- Does the report expose the most important metadata gap?
- Are recommendations actionable?
- Does the report avoid universal claims?
- Can every result be traced back to inputs and definitions?

### 74.4 Empirical acceptance

The example passes when:

- run completes,
- output is internally consistent,
- at least one useful conclusion is produced at low observability,
- unavailable conclusions remain explicit,
- the reviewer does not need hidden implementation knowledge.

---

## 75. Human review protocol

Recommended reviewers:

- one ML researcher,
- one research engineer,
- one data-governance reviewer,
- one independent technical reader when available.

Review form should capture:

- installation difficulty,
- command clarity,
- report clarity,
- misleading language,
- missing metadata recommendations,
- trust in traceability,
- unresolved ambiguity.

Human review supports usability.

It does not replace mathematical or software tests.

---

# PART XIV. PHASE VALIDATION MATRIX

## 76. Phase 0 gate

Required artifacts:

- all specification files,
- approved decisions,
- theory map,
- traceability map,
- validation plan.

Required checks:

- no implementation code,
- all conflicts listed,
- hero contradictions resolved,
- deferred claims blocked,
- cross-file consistency pass.

Phase result:

```text
PASS
```

only after approvals are recorded.

---

## 77. Phase 1 gate

Required deliverables:

- repository scaffold,
- package metadata,
- placeholder modules,
- test directories,
- fixture directories,
- CI skeleton,
- licenses,
- README shell.

Required validation:

- file tree matches approved architecture,
- every module has ownership placeholder,
- dependencies justified,
- no analysis algorithm present,
- package imports or placeholder import behavior is documented.

Forbidden:

- provisional metrics,
- hidden score,
- later-phase implementation.

---

## 78. Phase 2 gate

Required implemented owners:

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

Required passing tests:

- loaders,
- schema mapping,
- canonical validation,
- provenance joins,
- parent parsing,
- version order,
- observability,
- capability matrix,
- content-reference security.

Hero requirement:

- inputs load without manual changes,
- unknown remains unknown,
- Level 4 eligibility is recognized from inputs,
- no analytical metric needed for phase completion.

---

## 79. Phase 3 gate

Required implemented owners:

```text
T1
T2
T3 direct bounds
PR-005
PR-006
```

Required validation:

- exact formula tests,
- hand-calculated hero metrics,
- property tests,
- fixed-seed determinism,
- correct evidence classes,
- no black-box score.

Optional:

```text
T5 experimental scenario
```

If T5 is absent, related capability remains unavailable.

---

## 80. Phase 4 gate

Required implemented owners:

```text
PR-012
PR-013
PR-014
PR-015
PR-016
PR-018
```

Required outputs:

- JSON,
- Markdown,
- CLI.

Required validation:

- report schema,
- section order,
- evidence-class placement,
- unavailable conclusions,
- language golden tests,
- redacted mode,
- no-network hero,
- hero end-to-end golden.

---

## 81. Phase 5 gate

Required implemented owners:

```text
T4
T6
PR-008 full behavior
PR-009 lineage depth
T3 lineage bounds
```

Required validation:

- cycle fixtures,
- parent ambiguity,
- unresolved lineage,
- external-root rules,
- carryover behavior,
- multi-root fixture,
- ancestry HHI,
- effective roots,
- topological limitation language.

---

## 82. Phase 6A gate

Required validation:

- explicit version order,
- compatible representation,
- support delta,
- diversity delta,
- extinct observed states,
- provenance change,
- lineage change where available,
- observed-versus-simulated separation.

---

## 83. Phase 6B gate

Required validation:

- closed scenario,
- reopening scenario,
- exact parameters,
- seed,
- horizon,
- replicate behavior,
- experimental labeling,
- no causal claim,
- no hidden default execution.

---

# PART XV. CONTINUOUS INTEGRATION

## 84. Required CI jobs

Recommended jobs:

```text
spec-lint
unit
integration
golden
security
no-network
package-build
hero-smoke
```

Optional jobs:

```text
performance-smoke
html-report
parquet-extra
```

### 84.1 Spec-lint

Checks:

- Markdown files present,
- trace IDs resolve,
- formula IDs resolve,
- public field owners exist,
- forbidden fields absent from schema.

### 84.2 Unit

Runs all required unit tests.

### 84.3 Integration

Runs:

- hero,
- partial provenance,
- partial lineage,
- invalid input,
- CLI.

### 84.4 Golden

Compares normalized JSON and Markdown outputs.

### 84.5 Security

Runs malicious mapping and content-reference fixtures.

### 84.6 No-network

Runs hero in a network-blocked environment.

### 84.7 Package build

Builds wheel and source distribution and installs them in a clean environment.

### 84.8 Hero smoke

Runs the documented one-command example.

---

## 85. CI merge gate

A change may merge only when:

- all required jobs pass,
- traceability metadata is included,
- golden changes are approved,
- no blocking decision is open for the changed behavior.

Branch protection should require review for:

- theory-relevant metrics,
- schema changes,
- report-field changes,
- security-sensitive mapping behavior.

---

# PART XVI. GOLDEN OUTPUT GOVERNANCE

## 86. Golden output purpose

Golden files validate the public contract.

They should remain small enough for human review.

### 86.1 Required golden outputs

```text
hero_report.json
hero_report.md
partial_provenance_report.json
lineage_multi_root_report.json
cycle_error_report.json
```

### 86.2 Golden source manifest

Each golden set should identify:

- fixture hashes,
- configuration hash,
- toolkit version,
- report schema version,
- expected trace owners,
- normalized variable fields.

### 86.3 Golden review

Reviewers must inspect:

- numerical changes,
- evidence-class movement,
- limitation changes,
- warning changes,
- unavailable-conclusion changes.

A formatting-only change must still confirm that semantic content is unchanged.

---

# PART XVII. DEFECT, WAIVER, AND DEFERMENT POLICY

## 87. Defect classification

| Severity | Meaning |
|---|---|
| Critical | incorrect public conclusion, privacy leak, code execution, hidden network |
| High | incorrect metric, wrong evidence class, unknown inference, hero failure |
| Medium | partial capability misreported, unclear remediation, noncritical compatibility |
| Low | formatting, wording, optional convenience |

Critical and High defects block release.

### 87.1 Defect record

Each defect should include:

- issue ID,
- affected owner IDs,
- affected fields,
- fixture,
- expected behavior,
- actual behavior,
- severity,
- remediation,
- regression test.

---

## 88. Waivers

A release waiver cannot be used for:

- incorrect formula,
- privacy leak,
- unsafe code execution,
- hidden telemetry,
- unsupported public score,
- missing trace owner,
- hero golden failure.

A waiver may apply to:

- optional HTML,
- optional Parquet,
- noncritical platform support,
- advisory performance regression.

Every waiver requires:

- reason,
- scope,
- expiration,
- public documentation where user-visible.

---

## 89. Deferred tests

Tests for deferred features should remain outside required CI or use explicit `xfail`.

Examples:

- amplification threshold,
- empirical intervention effect,
- universal integrity,
- effective source diversity.

Deferred tests must not create public fields.

---

# PART XVIII. RELEASE VALIDATION PACKAGE

## 90. Required proof artifacts

An official v0.1 release must preserve:

- CI results,
- unit-test summary,
- integration-test summary,
- golden comparison summary,
- security-test summary,
- no-network result,
- performance benchmark,
- traceability coverage report,
- specification consistency report,
- release checklist,
- known limitations.

### 90.1 Release validation summary

Recommended file:

```text
VALIDATION_SUMMARY_v0.1.md
```

It should state:

- tests run,
- tests passed,
- tests skipped,
- optional features excluded,
- hardware used,
- open nonblocking issues,
- final approvals.

---

## 91. Quantitative release requirements

Required:

```text
public-field trace coverage: 1.0
active-owner test coverage: 1.0
proxy and simulation limitation coverage: 1.0
hero golden match: 1.0
required unit tests passing: 1.0
required integration tests passing: 1.0
network calls in hero: 0
```

No required test may remain `xfail`.

---

## 92. Final release gate

A release candidate passes only when:

1. all blocking decisions are approved or intentionally deferred,
2. specifications are consistent,
3. every required formula passes exact tests,
4. every required product rule passes tests,
5. every public field has trace ownership,
6. hero golden outputs match,
7. partial-provenance and partial-lineage reports behave correctly,
8. language restrictions pass,
9. redaction tests pass,
10. security tests pass,
11. no-network test passes,
12. deterministic tests pass,
13. package installation passes,
14. CLI smoke tests pass,
15. hero runtime target passes,
16. no forbidden public field appears,
17. unavailable conclusions remain explicit,
18. licenses and release metadata are coherent.

Release status:

```text
official-v0.1
```

may be used only after this gate passes.

---

# PART XIX. VALIDATION MATRIX BY OWNER

## 93. Primary theory owners

| Owner | Exact tests | Integration tests | Report tests | Release requirement |
|---|---:|---:|---:|---|
| `T1` | required | required | required | pass |
| `T2` | required | required when scenario enabled | required | pass |
| `T3` | required | required | required | pass |
| `T4` | required | required | required | pass |
| `T5` | required only if feature ships | required only if feature ships | required only if feature ships | optional experimental |
| `T6` | required | required | required | pass |

## 94. Product-rule owners

| Owner | Required status |
|---|---|
| `PR-001` | pass |
| `PR-002` | pass |
| `PR-003` | pass |
| `PR-004` | pass |
| `PR-005` | pass |
| `PR-006` | pass |
| `PR-007` | pass |
| `PR-008` | pass |
| `PR-009` | pass |
| `PR-010` | pass |
| `PR-011` | pass |
| `PR-012` | pass |
| `PR-013` | pass |
| `PR-014` | pass |
| `PR-015` | pass |
| `PR-016` | pass |
| `PR-017` | pass |
| `PR-018` | pass |

---

# PART XX. APPROVAL

## 95. Approval checklist

The Theory Owner and reviewers should confirm:

- [ ] validation layers are independent,
- [ ] mathematical expected values are hand-checkable,
- [ ] hero diversity values are included,
- [ ] closure bounds preserve uncertainty,
- [ ] tail extinction remains a simulation,
- [ ] ancestry HHI remains a toolkit operationalization,
- [ ] direct and lineage closure remain separate,
- [ ] source type and grounding are tested independently,
- [ ] unknown and missing remain distinct,
- [ ] partial reports preserve valid capabilities,
- [ ] forbidden language is covered by golden tests,
- [ ] redaction and no-network behavior are tested,
- [ ] security fixtures cannot execute code,
- [ ] performance targets are measurable,
- [ ] every phase has an exact validation gate,
- [ ] every public owner has required tests,
- [ ] deferred concepts remain outside required public outputs.

### Theory Owner decision

- [ ] Approve validation baseline
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

- [ ] Formula cases are correct.
- [ ] Exact rational values are correctly derived.
- [ ] Statistical sanity tests supplement exact tests.
- [ ] Tolerances are appropriate.
- [ ] Scenario assumptions remain visible.

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

- [ ] Test structure is implementable.
- [ ] CI jobs are feasible.
- [ ] Fixtures are sufficient.
- [ ] Golden normalization rules are clear.
- [ ] Phase gates can be automated.

Technical notes:

```text

```

Maintainer:

```text

```

Date:

```text

```

### Security Reviewer acknowledgment

- [ ] Mapping operations are safely testable.
- [ ] Local reference protections are covered.
- [ ] No-network behavior is covered.
- [ ] Redaction leakage tests are sufficient.
- [ ] Unsafe inputs fail without code execution.

Security notes:

```text

```

Reviewer:

```text

```

Date:

```text

```

### Domain Validator acknowledgment

- [ ] Hero output is understandable.
- [ ] Partial-provenance output remains useful.
- [ ] Recommendations identify actionable metadata.
- [ ] Unavailable conclusions prevent overinterpretation.
- [ ] A realistic workflow can be audited without author intervention.

Domain notes:

```text

```

Validator:

```text

```

Date:

```text

```

---

## 96. Change-control rule

After approval:

1. every new public field requires validation ownership,
2. every formula change requires new independent expected values,
3. every evidence-class change requires report and golden review,
4. every schema change requires input and migration tests,
5. every new mapping operation requires security tests,
6. every new optional dependency requires absence and presence tests,
7. every golden change requires a documented reason,
8. every performance promise requires a benchmark,
9. every deferred feature remains outside required CI until approved,
10. no test may be weakened merely to make an implementation pass,
11. a failing required test must lead to code correction, specification correction through governance, or a blocked release.
