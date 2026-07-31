# SPEC_AUDIT

## Document control

| Field | Value |
|---|---|
| Project | Recursive Integrity Toolkit |
| Target release | v0.1 |
| Phase | Phase 0: specification audit |
| Status | PASS - SPECIFICATION BASELINE APPROVED |
| Implementation code produced | None |
| Audit purpose | Identify contradictions, undefined terms, scope conflicts, unsafe defaults, and missing acceptance conditions before repository scaffolding or algorithm implementation |

## Phase 0 approval record

| Field | Value |
|---|---|
| Approved by | Xiangyu Guo, Theory Owner |
| Approval date | 2026-07-29 |
| Decision basis | All recommended options in `UNRESOLVED_DECISIONS.md` approved without exceptions |
| Baseline effect | This file is frozen as part of the approved Phase 0 baseline |
| Change policy | Later changes require the recorded change-control process |

This document is the controlling Phase 0 audit record for the Recursive Integrity Toolkit. It audits the current migration package against the uploaded theory sources and converts unresolved ambiguity into explicit decisions.

Approval of this file freezes the recommended resolutions below unless a later specification change is recorded through governance and traceability.

---

## 1. Sources audited

### S1. Product and migration package

**Concise Migration Package for the Recursive Integrity Toolkit**

Primary material audited:

- executive product framing
- repository skeleton
- Phase 0-6 acceptance gates
- `PROJECT_INSTRUCTIONS.md`
- `V0.1_PRODUCT_SPEC.md`
- `DEFINITIONS_AND_UNITS.md`
- `DATA_AND_PROVENANCE_SPEC.md`
- `OBSERVABILITY_AND_REPORTING.md`
- `THEORY_TO_CODE_TRACEABILITY.md`
- `VALIDATION_PLAN.md`
- privacy, licensing, success, governance, README, hero fixture, and golden expectations

### S2. Primary theory source

**The Universal Inbreeding Law v2**

Primary material audited:

- closure, diversity loss, correlated error, and integrity decay
- finite closed-resampling model
- expected Gini-Simpson diversity contraction
- rare-state extinction probability
- absorbing support loss
- inherited deviation relative to an external distribution
- external reopening through an input mixture
- distinction between concentration and functional failure
- distinction between exact stochastic commonality and broader structural analogy

### S3. Entropy interpretation source

**Entropy as a Structural Boundary Condition, Not a Causal Force v2**

Primary material audited:

- entropy as a structural boundary and descriptive signature
- separation of causal mechanism from entropy accounting
- open-system requirements for maintained order
- limits on cross-domain interpretation
- prohibition on treating entropy as an independent causal agent

### S4. Supplementary case source

**Supplementary Case Registry for the Universal Inbreeding Law, Version 2.0**

Primary material audited:

- contraction-dominant genetic algorithm case
- selection pressure, finite resampling, absorbing homogeneity, mutation, immigration, and restart
- ancestry concentration and local-basin lock-in
- amplification-dominant prion witness
- separation of contraction and amplification branches
- case-admission template and versioning policy

---

## 2. Audit verdict

The package contains a coherent product direction and a usable theory-to-tool path. The mathematical core needed for v0.1 is sufficiently explicit in the Universal Inbreeding Law:

1. finite self-resampling,
2. expected diversity contraction,
3. disproportionate rare-state extinction,
4. absorbing loss under closure,
5. inherited deviation,
6. reopening through genuine external input.

The current package is not yet fully frozen because several terms, metrics, data encodings, and observability rules remain underdefined or internally inconsistent. The most important conflicts concern:

- the authority order between theory and product scope,
- the hero example's observability level,
- the meaning of `generation`,
- parent reference encoding,
- closure exposure bounds,
- support representation,
- tail fragility classification,
- ancestry concentration,
- Phase 6 intervention scope.

No implementation should begin until the blocking resolutions in Section 5 are approved.

---

## 3. Authority model

The migration package currently gives all uploaded theory PDFs priority over product and implementation specifications. That order is too broad because theory authority and release-scope authority perform different functions.

The following dual authority model is recommended.

### 3.1 Theory authority

The uploaded theory sources control:

- conceptual meaning,
- mathematical interpretation,
- causal boundaries,
- the distinction between exact results and structural extensions,
- prohibited overclaims,
- the meaning of closure, difference, external correction, and integrity decay.

When a product specification changes the meaning of a theory term, the theory source prevails.

### 3.2 Product authority

The approved v0.1 specifications control:

- which theoretically valid mechanisms enter v0.1,
- required and optional inputs,
- output schemas,
- implementation order,
- release gates,
- dependency limits,
- performance targets,
- privacy behavior.

A theory claim does not automatically enter v0.1 merely because it appears in an authoritative article.

### 3.3 Exact contract authority

After Phase 0 approval, the following files control exact field names and public behavior:

1. `SPEC_AUDIT.md`
2. `V0.1_PRODUCT_SPEC.md`
3. `DEFINITIONS_AND_UNITS.md`
4. `DATA_AND_PROVENANCE_SPEC.md`
5. `OBSERVABILITY_AND_REPORTING.md`
6. `THEORY_TO_CODE_TRACEABILITY.md`
7. `VALIDATION_PLAN.md`

Any later conflict must be recorded rather than silently resolved.

---

## 4. Stable foundations approved by the audit

The following foundations are already strong enough to freeze.

### 4.1 Product identity

Recursive Integrity Toolkit v0.1 is a local-first, auditable research toolkit for synthetic-data and recursive-data pipelines.

Its core public value is evidence-bounded diagnosis of:

- recursive closure exposure,
- support and diversity contraction,
- tail vulnerability,
- provenance incompleteness,
- source concentration,
- ancestry concentration,
- observability limits.

### 4.2 Primary domain

The v0.1 implementation is for machine-learning data pipelines. Biological, cognitive, institutional, and social cases remain theory sources and validation witnesses. Public reports must not generalize a dataset result into a biological or civilizational conclusion.

### 4.3 Mathematical core

The exact stochastic core is the finite closed-resampling model in *The Universal Inbreeding Law v2*, especially the equations on pages 6-9:

\[
X_t \mid p_t \sim \operatorname{Multinomial}(n,p_t),
\qquad
p_{t+1}=\frac{X_t}{n}.
\]

With Gini-Simpson diversity

\[
D_t=1-\sum_i p_{t,i}^2,
\]

the model gives

\[
\mathbb{E}[D_{t+1}\mid p_t]
=
\left(1-\frac{1}{n}\right)D_t.
\]

For state \(i\),

\[
\Pr(p_{t+1,i}=0\mid p_{t,i})
=
(1-p_{t,i})^n.
\]

These are eligible for direct deterministic calculation or explicitly labeled scenario simulation when their assumptions are satisfied.

### 4.4 Entropy boundary

The tool must not produce a generic entropy-caused-failure claim. Entropy language may describe uncertainty, distributional structure, or the boundary of sustained order under declared assumptions. Reports must identify the actual observed or modeled mechanism, such as finite resampling, source closure, lineage concentration, missing external roots, or support loss.

### 4.5 No universal integrity score

The structural relations

\[
Q=I\times D
\]

and

\[
S=P\times I
\]

remain theory-level dependencies. v0.1 lacks operational definitions for universal `Quality`, `Integrity`, `Presence`, and `Stability` scores. They must not power a black-box public metric.

### 4.6 Evidence classes

Every public output must belong to one of these classes:

- observed fact,
- derived metric,
- proxy signal,
- simulation,
- unavailable conclusion.

No value may appear in more than one class without an explicit cross-reference and explanation.

### 4.7 Unknown provenance

Unknown provenance remains unknown. Human review, fluent content, source reputation, or model confidence cannot silently convert an unknown origin into human, external, or grounded origin.

### 4.8 Reproducibility and privacy

v0.1 runs locally by default, performs no hidden network calls, uses deterministic paths when possible, and excludes raw content from normal logs.

---

## 5. Blocking findings and proposed resolutions

All items in this section require approval before Phase 1.

### B01. Authority order is too broad

**Finding**

The migration package gives theory PDFs absolute priority over all product specifications. This can force theoretically valid but out-of-scope mechanisms into v0.1.

**Risk**

Scope expansion, conflicting instructions, and uncontrolled implementation.

**Proposed resolution**

Adopt the dual authority model in Section 3:

- theory controls meaning,
- approved product specifications control v0.1 scope and exact public contracts.

**Required file changes**

- revise `PROJECT_INSTRUCTIONS.md`
- add a conflict-handling paragraph to `V0.1_PRODUCT_SPEC.md`

---

### B02. Hero observability level is internally inconsistent

**Finding**

The README quick-start expectation reports Level 3 while using:

- `records_v2.csv`,
- `provenance.csv`,
- `records_v1.csv` through `--compare`.

The hero golden expectations state that v1 plus v2 plus provenance provide Level 4 inputs.

**Risk**

The same command can produce two different expected observability levels.

**Proposed resolution**

The hero quick-start command must report:

- maximum observability level: **4**
- lineage capability: **Level 3 available**
- longitudinal dataset capability: **Level 4 available**
- model-performance trend: **unavailable**

A single maximum level must be accompanied by a capability matrix so the level does not imply that every metric at that level is available.

**Required file changes**

- update README expected output from Level 3 to Level 4
- update `EXPECTED_OUTPUTS.md`
- add `observability.capabilities` to the report schema

---

### B03. Level 4 input requirements are ambiguous

**Finding**

The observability table refers to multiple dataset/model versions. The hero note suggests that lack of model-performance data can limit longitudinal analysis.

**Risk**

The classifier may incorrectly block valid support and tail comparisons when model-performance data are absent.

**Proposed resolution**

Multiple compatible dataset versions are sufficient for Level 4 dataset analysis.

Level 4 may include separate capabilities:

- `dataset_longitudinal`: version deltas, support loss, tail extinction
- `model_longitudinal`: model-performance or behavior trends when model evidence is supplied

Missing model-performance data blocks only model-level conclusions.

**Required file changes**

- refine Level 4 in `OBSERVABILITY_AND_REPORTING.md`
- define capability-specific unavailable conclusions

---

### B04. `generation` conflates recursive generation and graph depth

**Finding**

The definitions describe `generation` as recursion depth from an external root. The hero provenance gives v2 human carryovers a parent in v1 while retaining `generation=0`.

**Risk**

A graph traversal can disagree with the declared value even when the provenance is conceptually valid.

**Proposed resolution**

Freeze `generation` as:

> The number of consecutive non-grounding generative steps since the most recent externally grounded state. A carryover of an externally grounded record may remain generation 0 even when it has a parent link.

Add a separate derived field:

- `lineage_depth`: number of parent edges on the selected path or path summary

Rules:

- `external_grounding=yes` permits `generation=0`
- `external_grounding=no` with a known parent normally requires `generation >= 1`
- `external_grounding=unknown` prevents strict generation verification
- declared generation and computed lineage evidence must be compared and mismatches reported

**Required file changes**

- revise `DEFINITIONS_AND_UNITS.md`
- revise provenance validation rules
- add generation-consistency warnings

---

### B05. Parent references are not safely encoded

**Finding**

`record_id` is unique only within `dataset_version`, while `parent_ids` contains bare record IDs. Multiple parent encoding in CSV is undefined.

**Risk**

Ambiguous joins, incorrect lineage edges, and accidental cross-version matches.

**Proposed resolution**

The canonical internal parent key is:

\[
(\text{dataset\_version},\text{record\_id})
\]

The canonical CSV value for multiple parents is a JSON array of composite strings:

```text
["v1::v1_01","v1::v1_02"]
```

Compatibility behavior:

- a bare parent ID may be accepted only when it resolves to exactly one loaded record
- ambiguous bare IDs are errors
- canonical normalized exports always use composite references
- no delimiter-splitting heuristic may be applied silently

**Required file changes**

- revise `DATA_AND_PROVENANCE_SPEC.md`
- update hero provenance or document its unambiguous compatibility status
- add valid and ambiguous-parent tests

---

### B06. Provenance coverage has no exact definition

**Finding**

The package uses `provenance coverage` without distinguishing row coverage from field completeness.

**Risk**

A dataset may show 100 percent provenance coverage while all decisive fields remain unknown.

**Proposed resolution**

Report at least three separate measures:

1. `provenance_row_coverage`  
   Share of records with a matching provenance row.

2. `provenance_required_field_coverage`  
   Share of records whose required provenance fields are present and valid.

3. `grounding_field_coverage`  
   Share of records whose `external_grounding` value is `yes` or `no`.

Optional field coverage must be reported by exact field name when used in a conclusion.

**Required file changes**

- revise `DEFINITIONS_AND_UNITS.md`
- revise JSON report schema
- revise hero golden assertions to specify row coverage

---

### B07. External grounding is underdefined

**Finding**

The schema contains `source_type`, `human_reviewed`, and `external_grounding`, but their authority relationship is not frozen.

**Risk**

Implementers may treat `human` as grounded, `synthetic` as closed, or `human_reviewed=true` as external correction.

**Proposed resolution**

`external_grounding` is the controlling field for direct grounding claims.

Rules:

- `source_type` describes declared origin class
- `external_grounding` describes whether the record introduces independent external signal relative to the audited recursive loop
- `human_reviewed` is a review flag only
- no source type automatically determines grounding
- `mixed` does not imply grounding
- a synthetic record may be externally grounded
- a human record may remain ungrounded or unknown relative to a closed internal process

An `external root` is a record that:

- has `external_grounding=yes`, and
- has no parent that must be traversed to establish the same grounding claim.

A grounded carryover may point to an earlier external root without becoming a new distinct root.

**Required file changes**

- expand `DEFINITIONS_AND_UNITS.md`
- add examples to `DATA_AND_PROVENANCE_SPEC.md`

---

### B08. Closure exposure bounds lack a formula

**Finding**

The product spec requires a closure exposure envelope but provides no exact calculation.

**Risk**

Different implementations may produce incompatible bounds.

**Proposed resolution**

At Level 2, compute **direct closure exposure bounds** over all analyzed records.

Classify each record:

- `known_open`: `external_grounding=yes`
- `known_closed`: `external_grounding=no`
- `unresolved`: grounding unknown, missing, invalid, or absent because the provenance row is missing

Then:

\[
\text{closure lower bound}
=
\frac{N_{\text{known closed}}}{N_{\text{total}}}
\]

\[
\text{closure upper bound}
=
\frac{N_{\text{known closed}}+N_{\text{unresolved}}}{N_{\text{total}}}
\]

At Level 3, a separate **lineage closure exposure envelope** may be computed:

- known grounded: at least one reachable confirmed external root and no blocking ancestry ambiguity
- known closed: complete known ancestry with no reachable external root
- unresolved: missing parent, unknown grounding, incomplete ancestry, or conflicting lineage evidence

The report must identify which envelope is being shown.

**Required file changes**

- add exact formulas to `DEFINITIONS_AND_UNITS.md`
- add T3 detail to `THEORY_TO_CODE_TRACEABILITY.md`
- add hand-checkable lower/upper-bound tests

---

### B09. Support representation is missing

**Finding**

Support, diversity, tail, and extinction depend on a selected representation. The package lists topic, label, embeddings, and content but does not freeze representation selection.

**Risk**

A tool may present exact text uniqueness as semantic diversity or silently infer topics with an LLM.

**Proposed resolution**

Every support-based result must include:

- `representation_name`
- `representation_source`
- `representation_version`
- `binning_or_mapping_rule`

Selection order:

1. explicit user configuration
2. `topic` when present
3. `label` when present
4. user-provided embedding clusters or bins
5. exact normalized content hash for record-form support only

Rules:

- no embedded LLM may infer topics in v0.1
- exact content hash may support duplicate and record-form calculations
- exact content hash must not be described as semantic support
- comparison across versions requires compatible representations

**Required file changes**

- revise `DEFINITIONS_AND_UNITS.md`
- add representation metadata to reports
- add comparison-compatibility validation

---

### B10. Tail definition and tail fragility classification are incomplete

**Finding**

The theory gives an exact one-step extinction probability under finite closed resampling. The product package calls tail fragility a metric but does not state whether it is an observed fact, proxy, or simulation.

**Risk**

A hypothetical scenario may be presented as a forecast.

**Proposed resolution**

Freeze the following:

- `tail` is a subset under a declared threshold rule
- default threshold for the hero example: singleton states, frequency count equal to 1
- all default choices must appear in run metadata
- the ranking may cover all states, while alerts may be limited to the declared tail

For a state with observed frequency \(p_i\) and scenario sample size \(n\):

\[
P_{\text{extinct,next}}(i)=(1-p_i)^n
\]

Classification:

- frequency and support counts: observed facts
- deterministic ranking by rarity: derived metric
- one-step extinction probability under closed resampling: simulation result
- public summary warning based on that scenario: proxy signal

The tool must state:

- closed multinomial assumption,
- selected representation,
- assumed sample size,
- one-step horizon,
- absence or presence of reopening.

**Required file changes**

- revise `OBSERVABILITY_AND_REPORTING.md`
- expand T2 in traceability
- add scenario-assumption fields to JSON output

---

### B11. Ancestry concentration lacks an exact metric

**Finding**

The package requires ancestry concentration and effective external ancestry without defining allocation or normalization.

**Risk**

Shared ancestors can be double-counted, and an apparently precise score may depend on an undocumented convention.

**Proposed resolution**

v0.1 should report a transparent metric family rather than one opaque value.

Required Level 3 outputs:

1. `distinct_external_root_count`
2. `records_with_resolved_external_ancestry`
3. `external_ancestry_coverage`
4. `ancestor_incidence_count`
5. `ancestor_incidence_share`
6. `top_shared_ancestors`

Optional derived concentration outputs:

For each record with \(k\) reachable external roots, allocate \(1/k\) mass to each root. Aggregate and normalize the root masses to shares \(w_a\).

\[
HHI_{\text{ancestry}}=\sum_a w_a^2
\]

\[
N_{\text{effective roots}}=\frac{1}{HHI_{\text{ancestry}}}
\]

These two values must be labeled as topological derived metrics. They do not estimate causal contribution unless parent weights are supplied.

The hero assertion that `v1_01` supports three v2 records uses incidence count, not fractional mass.

**Required file changes**

- freeze formulas in `DEFINITIONS_AND_UNITS.md`
- expand T4 in traceability
- add multiple-root golden fixtures

---

### B12. Missing-parent behavior is undefined

**Finding**

The spec defines unmatched provenance rows and cycles but does not define parent references that point outside the loaded data.

**Risk**

The tool may invent roots, fail unnecessarily, or report complete ancestry from an incomplete graph.

**Proposed resolution**

Default behavior:

- unresolved parent reference: warning
- ambiguous parent reference: error
- cycle: error for lineage analysis
- strict mode may elevate unresolved parents to errors
- unresolved parents reduce lineage coverage
- no missing parent may be silently converted into an external root

Level 3 may still be available for partial lineage, but every ancestry conclusion must disclose the resolved coverage denominator.

**Required file changes**

- add lineage completeness rules
- add warning and strict-mode tests

---

### B13. Schema mapping permits unsafe interpretation

**Finding**

The mapping spec allows an optional expression without defining a safe expression language.

**Risk**

Arbitrary code execution, inconsistent transformations, and hidden data mutation.

**Proposed resolution**

v0.1 schema mapping is declarative only.

Allowed operations:

- rename
- type cast
- datetime parse with declared format
- JSON-list parse
- constant assignment
- coalesce among named fields
- whitespace normalization

Forbidden operations:

- `eval`
- arbitrary Python
- shell execution
- network calls
- user-defined plugins
- implicit content classification

Every transformation must be recorded in normalized run metadata.

**Required file changes**

- revise schema mapping table
- add invalid-transform tests

---

### B14. Phase 6 intervention scope is not specified

**Finding**

The phase plan includes controlled interventions and Level 5 outputs, but no intervention input schema or causal comparison contract exists.

**Risk**

Phase 6 may drift into an unbounded experimental framework.

**Proposed resolution**

Split Phase 6:

- **Phase 6A, required for v0.1:** longitudinal dataset comparison
- **Phase 6B, optional experimental:** closed-resampling and reopening scenario comparison from explicit configuration

Empirical controlled-intervention ingestion remains deferred until a separate schema is approved.

Phase 6B outputs must be labeled `experimental` and `simulation`. They do not support causal claims about a real production system.

**Required file changes**

- revise Phase 6 acceptance gate
- revise Level 5 wording
- add a deferred intervention-data entry to traceability

---

## 6. Non-blocking findings and frozen clarifications

The following items can be resolved through specification edits without delaying Phase 1 after the blocking package is approved.

### N01. Source shares

`mixed` remains its own category. v0.1 must not split a mixed record into human and synthetic fractions unless explicit component weights are provided.

Unweighted shares are the default:

\[
\text{share}(c)=\frac{N_c}{N}
\]

Weighted shares are optional, must be explicitly enabled, and must appear under separate field names.

### N02. Exact duplicates and near-duplicates

Exact duplicate detection is required and may use normalized content hashes.

Near-duplicate detection is optional in v0.1 and requires one of:

- user-provided embeddings,
- an explicitly configured deterministic text similarity method.

No default semantic near-duplicate threshold is frozen by this audit.

### N03. Markdown and HTML output

Required human-readable output: Markdown.

Optional output: HTML.

Phase 4 acceptance must not require HTML for v0.1 completion.

### N04. `collapse` terminology

`collapse` is forbidden as a metric name and forbidden as a direct conclusion from toolkit diagnostics.

The term may appear in:

- theory references,
- a statement that universal collapse prediction is unavailable,
- documentation describing the research problem.

### N05. Shannon entropy

Shannon entropy may later be supported as a declared distribution statistic. v0.1 defaults to Gini-Simpson diversity because the primary mathematical derivation and hero fixture use that quantity.

A Shannon value must not be converted into a generic system-entropy or integrity-decay claim.

### N06. Amplification-dominant recursion

The prion case establishes a distinct amplification branch with retention, recursive return, threshold behavior, and delayed visibility.

v0.1 does not implement:

- transfer-matrix threshold estimation,
- spectral-radius amplification analysis,
- epidemic or contagion models,
- prion-specific logic.

These remain candidates for a later `recursive_amplification` module.

### N07. Genetic algorithm case

The genetic algorithm case is eligible as a later validation fixture because it directly instantiates:

- selection concentration,
- finite resampling,
- ancestry takeover,
- absorbing homogeneity,
- reopening through mutation, immigration, and restart.

It is not required for the initial hero example.

### N08. Content references

When `content` is a reference rather than inline text:

- v0.1 may resolve local file references only,
- network retrieval is disabled by default,
- unresolved references are validation errors for content-dependent analysis,
- metadata-only analysis may continue when the report states the limitation.

### N09. Version ordering

String version IDs do not establish chronology.

Comparison and parent validation require one of:

- explicit `version_order`,
- valid timestamps,
- command-line order declared by the user.

The tool must record the selected ordering rule.

### N10. Record weights

`weight` is ignored for default count-based metrics unless the user explicitly enables weighted analysis.

When enabled:

- negative weights are errors,
- all-zero weights are errors,
- weighted and unweighted outputs remain separate.

### N11. Error and warning codes

Phase 2 should freeze a minimal taxonomy before implementation:

- `E_SCHEMA_REQUIRED_FIELD`
- `E_SCHEMA_ENUM`
- `E_RECORD_DUPLICATE_ID`
- `E_PROVENANCE_UNMATCHED_ROW`
- `E_PARENT_AMBIGUOUS`
- `E_LINEAGE_CYCLE`
- `E_MAPPING_UNSAFE_TRANSFORM`
- `W_PROVENANCE_MISSING_ROW`
- `W_GROUNDING_UNKNOWN`
- `W_PARENT_UNRESOLVED`
- `W_GENERATION_MISMATCH`
- `W_REPRESENTATION_FALLBACK`
- `W_LONGITUDINAL_INCOMPATIBLE_REPRESENTATION`

Exact message text belongs in the validation specification and golden tests.

### N12. Capability matrix

A maximum observability level must be supplemented by per-capability status:

- available
- partial
- unavailable
- experimental

This prevents a high level from implying complete data across every metric family.

---

## 7. Theory-to-implementation eligibility audit

| Theory object or claim | v0.1 status | Evidence class | Implementation boundary |
|---|---|---|---|
| Record count | Approved | Observed fact | Exact metadata count |
| Exact duplicate count | Approved | Observed fact | Deterministic normalization and hashing |
| Gini-Simpson diversity | Approved | Derived metric | Requires declared representation |
| Expected diversity contraction factor \(1-1/n\) | Approved | Derived metric or simulation parameter | Valid under finite multinomial resampling |
| Rare-state one-step extinction probability | Approved | Simulation | Requires \(p_i\), \(n\), and closed-resampling assumption |
| Support loss across versions | Approved | Derived metric | Requires compatible representations |
| Tail extinction list | Approved | Derived metric | Requires ordered compatible versions |
| Direct provenance row coverage | Approved | Observed fact | Exact join coverage |
| Source-type shares | Approved | Derived metric | No inference from content |
| Direct closure exposure bounds | Approved after B08 | Derived metric | Based on grounding states and unknown envelope |
| Lineage cycle detection | Approved | Observed graph fact | Requires resolvable parent graph |
| External-root incidence | Approved | Derived metric | Requires lineage and grounding evidence |
| Ancestry concentration HHI | Approved after B11 | Derived topological metric | No causal contribution claim |
| Effective external ancestor number | Approved after B11 | Derived topological metric | Inverse HHI convention must be reported |
| External reopening scenario | Approved as experimental | Simulation | Requires explicit \(\lambda\), external distribution, seed, horizon |
| `Quality = Integrity x Diversity` | Deferred | Unavailable conclusion | No operational integrity definition |
| `Stability = Presence x Integrity` | Deferred | Unavailable conclusion | No operational presence or integrity score |
| Universal integrity score | Forbidden | None | Black-box score prohibited |
| Universal collapse prediction | Forbidden | Unavailable conclusion | Outside v0.1 |
| Epoch countdown to failure | Forbidden | None | Unsupported |
| Thermodynamic entropy of an ML pipeline | Deferred | Unavailable conclusion | No cross-domain physical identity claim |
| Amplification threshold \(\rho(K)\) | Deferred | Simulation or domain model | Outside contraction-focused v0.1 |
| Social or institutional diagnosis | Deferred | Unavailable conclusion | Outside primary product domain |

---

## 8. Observability model after audit

### Level 0: Ingest-only observability

Minimum evidence:

- readable file
- minimal record identity or recoverable row identity

Allowed outputs:

- ingest status
- row count
- schema inventory
- auditability gaps
- validation errors and warnings

### Level 1: Content or representation observability

Minimum evidence:

- records with analyzable content, labels, topics, bins, or embeddings

Capability-dependent outputs:

- exact duplicates
- support size
- Gini-Simpson diversity
- rarity ranking
- tail definition
- version support comparison when multiple compatible versions exist

Restrictions:

- semantic support requires a semantic representation
- content hashes provide record-form support only

### Level 2: Provenance observability

Minimum evidence:

- matching provenance for at least part of the records

Allowed outputs:

- row coverage
- field coverage
- source-type shares
- unknown share
- direct closure exposure bounds
- effective source diversity when its formula is separately frozen

### Level 3: Lineage observability

Minimum evidence:

- at least one resolvable parent-child path
- cycle-free analyzed subgraph

Allowed outputs:

- lineage coverage
- cycle status
- external-root incidence
- shared ancestors
- ancestry concentration
- lineage closure exposure bounds

Restrictions:

- incomplete ancestry widens uncertainty
- unresolved parents cannot become external roots by default

### Level 4: Longitudinal observability

Minimum evidence:

- at least two ordered, representation-compatible dataset versions

Allowed outputs:

- version deltas
- support loss
- tail extinction alerts
- provenance change
- ancestry change when lineage is available

Model-performance conclusions require separate model evidence.

### Level 5: Experimental intervention observability

v0.1 status:

- optional
- simulation only
- explicit assumptions required

Empirical causal intervention analysis remains deferred.

---

## 9. Hero fixture audit

### 9.1 Fixture strengths

The hero example is appropriate for v0.1 because it is small, exact, and hand-checkable.

It demonstrates:

- v1 support of eight topics,
- v2 support of five topics,
- extinction of `lizard`, `turtle`, and `battery`,
- v2 source shares of 0.50 human and 0.50 synthetic,
- complete v2 provenance row coverage,
- five distinct external roots supporting v2,
- concentration around `v1_01`,
- a valid comparison between direct record count and effective ancestry breadth.

### 9.2 Required corrections

1. The quick-start maximum observability level must be Level 4.
2. `provenance coverage: 100%` must be renamed `provenance row coverage: 100%`.
3. Parent encoding must be documented as compatibility input or converted to composite references.
4. The representation must be declared as `topic`.
5. Support contraction must be described as topic-support contraction.
6. The top shared ancestor result must state that it uses incidence count.
7. The report must not claim universal collapse.
8. The recommendation to reintroduce extinct topics must appear as a recommendation grounded in the selected topic representation.

### 9.3 Golden values retained

| Assertion | Expected value |
|---|---|
| v1 topic support | 8 |
| v2 topic support | 5 |
| extinct topics | `lizard`, `turtle`, `battery` |
| v2 provenance row coverage | 1.00 |
| v2 human share | 0.50 |
| v2 synthetic share | 0.50 |
| v2 unknown share | 0.00 |
| distinct external roots supporting v2 | 5 |
| most shared external root | `v1_01` |
| v2 records supported by `v1_01` | 3 |
| maximum observability level with v1, v2, and provenance | 4 |

### 9.4 Additional golden fixture required

A second lineage fixture must include:

- one record with two external roots,
- one unresolved parent,
- one unknown grounding value,
- one ambiguous bare parent ID,
- one cycle in a separate failure fixture.

This fixture is required to validate concentration, coverage, ambiguity, and failure behavior beyond the single-parent hero graph.

---

## 10. Source transcription and editorial controls

The source PDFs contain several formatting conditions that must not be copied blindly into specifications or code comments.

### 10.1 Formula source control

The rendered equations on pages 6-9 of *The Universal Inbreeding Law v2* are the controlling mathematical source.

The executive-summary text contains a duplicated rendering of the contraction factor. Implementations must use the displayed equation:

\[
1-\frac{1}{n}
\]

### 10.2 Editorial duplication

The introduction of *The Universal Inbreeding Law v2* contains a duplicated phrase around "general interpretive key." This does not change the theory meaning and must not be reproduced in tool documentation.

### 10.3 PDF line wrapping

The migration package's CSV examples contain line-wrapped headers and formatting artifacts. Canonical schemas must be reconstructed from the field tables rather than copied from PDF line breaks.

### 10.4 Mathematical symbols in the registry

The prion case relies on the distinction:

\[
\rho(K)<1
\]

for decay and

\[
\rho(K)>1
\]

for amplification. This branch is deferred from v0.1, but later transcription must be verified against the rendered pages.

---

## 11. Required specification changes before Phase 1

### `PROJECT_INSTRUCTIONS.md`

Add:

- dual authority model
- capability matrix requirement
- prohibition on arbitrary mapping expressions
- rule that maximum observability level does not imply complete metric availability

### `V0.1_PRODUCT_SPEC.md`

Clarify:

- ML pipeline as primary domain
- Markdown required, HTML optional
- Phase 6A required and Phase 6B optional experimental
- near-duplicate analysis optional unless representation is supplied
- support representation requirements

### `DEFINITIONS_AND_UNITS.md`

Freeze:

- revised `generation`
- `lineage_depth`
- provenance coverage measures
- external root
- direct and lineage closure exposure
- representation metadata
- ancestry incidence and concentration formulas
- unweighted default behavior

### `DATA_AND_PROVENANCE_SPEC.md`

Freeze:

- composite parent references
- JSON-array encoding
- version ordering
- missing-parent behavior
- declarative mapping operations
- local-only content references

### `OBSERVABILITY_AND_REPORTING.md`

Revise:

- hero Level 4 rule
- capability matrix
- Level 4 dataset/model distinction
- tail fragility classification
- experimental simulation placement
- field coverage disclosures

### `THEORY_TO_CODE_TRACEABILITY.md`

Expand:

- T2 with scenario assumptions
- T3 with exact direct and lineage bounds
- T4 with incidence and HHI conventions
- T5 with explicit experimental status
- deferred entries for compact structural formulas and amplification thresholds

### `VALIDATION_PLAN.md`

Add:

- ambiguous parent case
- unresolved parent case
- multiple-root ancestry case
- incompatible representation case
- generation mismatch case
- unsafe mapping rejection
- Level 3 versus Level 4 hero classification
- weighted-analysis opt-in test

---

## 12. Phase 0 acceptance gate

Phase 0 passes only when all of the following are true.

| Gate | Status |
|---|---|
| All contradictions are listed | Complete |
| Undefined public metrics are listed | Complete |
| Scope conflicts are listed | Complete |
| Unsafe defaults are listed | Complete |
| Theory-level and product-level authority are separated | Proposed |
| Blocking resolutions B01-B14 are approved | Pending |
| Required downstream specification edits are identified | Complete |
| Deferred claims are prevented from powering public results | Complete |
| No implementation code has been produced | Complete |
| Hero observability contradiction is resolved | Complete |
| Parent encoding is resolved | Complete |
| Closure exposure bounds are frozen | Complete |
| Ancestry concentration is frozen | Complete |
| Phase 6 scope is frozen | Complete |

**Current Phase 0 result: PASS - SPECIFICATION BASELINE APPROVED**

The Theory Owner approved all proposed resolutions without exceptions on 2026-07-29. The specification baseline is approved, and Phase 1 repository scaffolding may begin.

---

## 13. Approval block

### Theory Owner decision

- [x] Approve all proposed resolutions B01-B14
- [ ] Approve with listed exceptions
- [ ] Return for revision

Exceptions or modifications:

```text

```

Theory Owner:

```text
Xiangyu Guo
```

Approval date:

```text
2026-07-29
```

Approved baseline status:

```text
APPROVED
```
