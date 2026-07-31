# UNRESOLVED_DECISIONS

## Document control

| Field | Value |
|---|---|
| Project | Recursive Integrity Toolkit |
| Target release | v0.1 |
| Phase | Phase 0: decision closure |
| Status | APPROVED DECISION REGISTER |
| Depends on | `SPEC_AUDIT.md`, `THEORY_SOURCE_MAP.md` |
| Decision owner | Theory Owner, with technical review where indicated |
| Implementation code produced | None |
| Purpose | Record every decision that must be approved, deferred, or rejected before implementation proceeds |

## Phase 0 approval record

| Field | Value |
|---|---|
| Approved by | Xiangyu Guo, Theory Owner |
| Approval date | 2026-07-29 |
| Decision basis | All recommended options in `UNRESOLVED_DECISIONS.md` approved without exceptions |
| Baseline effect | This file is frozen as part of the approved Phase 0 baseline |
| Change policy | Later changes require the recorded change-control process |

This file is the formal decision register for the Recursive Integrity Toolkit.

## Blanket approval effect

The Theory Owner approved every recommended option in this register without exceptions on 2026-07-29.

All entries previously marked `RECOMMENDED` are approved for v0.1. Entries explicitly marked `DEFERRED` remain deferred. Prohibited v0.1 capabilities remain prohibited. This approval authorizes Phase 1 repository scaffolding.
 It converts ambiguities identified in `SPEC_AUDIT.md` and `THEORY_SOURCE_MAP.md` into explicit choices.

A decision remains open until one option is selected and its status is changed to `APPROVED`, `DEFERRED`, or `REJECTED`.

No implementation team, maintainer, Work session, or code-generation system may silently resolve an open decision.

---

## 1. Decision status legend

| Status | Meaning |
|---|---|
| `OPEN` | A decision is required |
| `RECOMMENDED` | Historical status used before Theory Owner approval |
| `APPROVED` | The decision is frozen for v0.1 |
| `DEFERRED` | The decision is intentionally postponed and must not power v0.1 public behavior |
| `REJECTED` | The proposed option has been explicitly rejected |
| `SUPERSEDED` | A later approved decision replaces this entry |

### Priority labels

| Priority | Meaning |
|---|---|
| `BLOCKING-PHASE-1` | Must be closed before repository scaffolding |
| `BLOCKING-PHASE-2` | Must be closed before ingestion and validation implementation |
| `BLOCKING-PHASE-3` | Must be closed before metric implementation |
| `BLOCKING-PHASE-4` | Must be closed before report and CLI implementation |
| `NONBLOCKING-V0.1` | May remain open temporarily, but must close before release |
| `DEFERRED-POST-V0.1` | Explicitly outside v0.1 |

---

## 2. Phase 0 exit rule

Phase 0 may pass only when:

1. every `BLOCKING-PHASE-1` decision is approved or deferred,
2. no deferred item is exposed as a public v0.1 result,
3. approved choices are copied into the controlling specification files,
4. the Theory Owner signs the final approval block,
5. all contradictions between the hero example, observability model, field definitions, and theory map are resolved.

Repository scaffolding may begin after Phase 0 passes.

Algorithm implementation must wait until the decisions assigned to its phase are closed.

---

## 3. Decision register summary

| ID | Decision | Priority | Approved status |
|---|---|---|---|
| UD-001 | Authority model | BLOCKING-PHASE-1 | APPROVE |
| UD-002 | Primary product domain | BLOCKING-PHASE-1 | APPROVE |
| UD-003 | Hero maximum observability level | BLOCKING-PHASE-1 | APPROVE |
| UD-004 | Capability matrix alongside observability level | BLOCKING-PHASE-1 | APPROVE |
| UD-005 | Meaning of `generation` | BLOCKING-PHASE-2 | APPROVE |
| UD-006 | Canonical parent reference encoding | BLOCKING-PHASE-2 | APPROVE |
| UD-007 | Dataset version ordering | BLOCKING-PHASE-2 | APPROVE |
| UD-008 | Provenance coverage definitions | BLOCKING-PHASE-2 | APPROVE |
| UD-009 | Authority of `external_grounding` | BLOCKING-PHASE-2 | APPROVE |
| UD-010 | Closure exposure bounds | BLOCKING-PHASE-3 | APPROVE |
| UD-011 | Support representation selection | BLOCKING-PHASE-3 | APPROVE |
| UD-012 | Tail definition and default threshold | BLOCKING-PHASE-3 | APPROVE |
| UD-013 | Tail extinction evidence classification | BLOCKING-PHASE-3 | APPROVE |
| UD-014 | Ancestry concentration convention | BLOCKING-PHASE-3 | APPROVE |
| UD-015 | Missing and ambiguous parent behavior | BLOCKING-PHASE-2 | APPROVE |
| UD-016 | Safe schema mapping operations | BLOCKING-PHASE-2 | APPROVE |
| UD-017 | Phase 6 split | BLOCKING-PHASE-1 | APPROVE |
| UD-018 | Cycle detection classification | BLOCKING-PHASE-2 | APPROVE |
| UD-019 | Human-readable report requirement | BLOCKING-PHASE-4 | APPROVE |
| UD-020 | Near-duplicate analysis scope | BLOCKING-PHASE-3 | APPROVE |
| UD-021 | Weighted analysis behavior | BLOCKING-PHASE-3 | APPROVE |
| UD-022 | OpenLineage and ML Metadata integration | NONBLOCKING-V0.1 | DEFER ADAPTERS |
| UD-023 | Code and documentation licenses | BLOCKING-PHASE-1 | APPROVE |
| UD-024 | Theory PDF inclusion in repository | BLOCKING-PHASE-1 | APPROVE REFERENCE-ONLY POLICY |
| UD-025 | Python version and dependency ceiling | BLOCKING-PHASE-1 | APPROVE |
| UD-026 | Package and CLI naming | BLOCKING-PHASE-1 | APPROVE |
| UD-027 | CI platform coverage | NONBLOCKING-V0.1 | APPROVE MINIMUM |
| UD-028 | Effective source diversity | DEFERRED-POST-V0.1 | DEFER |
| UD-029 | Universal integrity, quality, presence, and stability scores | DEFERRED-POST-V0.1 | FORBID IN v0.1 |
| UD-030 | Amplification-dominant analysis | DEFERRED-POST-V0.1 | DEFER |
| UD-031 | Controlled empirical intervention ingestion | DEFERRED-POST-V0.1 | DEFER |
| UD-032 | Release labels and approval authority | BLOCKING-PHASE-1 | APPROVE |
| UD-033 | Hero fixture corrections | BLOCKING-PHASE-1 | APPROVE |
| UD-034 | Additional lineage golden fixture | BLOCKING-PHASE-3 | APPROVE |
| UD-035 | Public use of the word `collapse` | BLOCKING-PHASE-4 | APPROVE RESTRICTION |
| UD-036 | HTML report support | NONBLOCKING-V0.1 | OPTIONAL |

---

# PART I. BLOCKING DECISIONS

## UD-001. Authority model

| Field | Value |
|---|---|
| Status | `APPROVED` |
| Priority | `BLOCKING-PHASE-1` |
| Owner | Theory Owner |
| Technical review | Technical Maintainer |
| Source | `SPEC_AUDIT.md` B01; `THEORY_SOURCE_MAP.md` Section 2 |

### Decision needed

How should conflicts between theory sources and product specifications be resolved?

### Options

**Option A: Single absolute theory authority**

All theory PDFs override all product and implementation specifications.

**Option B: Single product authority**

The product specification controls both conceptual meaning and implementation scope.

**Option C: Dual authority**

- theory sources control conceptual meaning, mathematical interpretation, causal limits, and prohibited overclaims,
- approved product specifications control v0.1 scope, field names, output contracts, implementation order, and release requirements.

### Approved decision

**Approve Option C.**

### Rationale

The theory corpus should protect the meaning of closure, difference, integrity, entropy, and functional failure. Product specifications must still control which valid theory branches enter v0.1.

### Consequences

- theory cannot be silently redefined by implementation,
- theory claims do not automatically create product features,
- conflicts must be recorded,
- Phase 0 files become the exact contract after approval.

### Approval

- [ ] Approve Option C
- [ ] Select another option
- [ ] Return for revision

Decision notes:

```text

```

---

## UD-002. Primary product domain

| Field | Value |
|---|---|
| Status | `APPROVED` |
| Priority | `BLOCKING-PHASE-1` |
| Owner | Theory Owner |
| Source | `THEORY_SOURCE_MAP.md` TM-E04 and theory coverage matrix |

### Decision needed

Should v0.1 be a general cross-domain recursive-integrity tool or an ML data-pipeline tool?

### Options

**Option A: Cross-domain v0.1**

Attempt to support biological, cognitive, institutional, social, and ML systems.

**Option B: ML pipeline v0.1**

Build the implementation for synthetic-data and recursive-data pipelines. Preserve other domains as theory sources and validation witnesses.

### Approved decision

**Approve Option B.**

### Rationale

The exact input schemas, provenance model, support metrics, and lineage graph currently fit data pipelines. Cross-domain software would require separate domain-native state definitions and validation.

### Consequences

Public reports may discuss:

- records,
- datasets,
- provenance,
- generations of recursive data,
- support,
- ancestry,
- simulations.

Public reports may not diagnose:

- biological fitness,
- childhood development,
- social institutions,
- civilization,
- thermodynamic state.

### Approval

- [ ] Approve ML pipeline v0.1
- [ ] Expand scope
- [ ] Return for revision

Decision notes:

```text

```

---

## UD-003. Hero maximum observability level

| Field | Value |
|---|---|
| Status | `APPROVED` |
| Priority | `BLOCKING-PHASE-1` |
| Owner | Theory Owner |
| Technical review | Technical Maintainer |
| Source | `SPEC_AUDIT.md` B02 and hero fixture audit |

### Conflict

The README quick-start expects Level 3 while the same command loads two dataset versions and lineage provenance, which satisfies the proposed Level 4 dataset requirements.

### Options

**Option A: Report Level 3**

Treat lineage as the maximum capability and ignore the version comparison when classifying observability.

**Option B: Report Level 4**

Treat compatible multiple versions as Level 4 and separately identify available Level 3 lineage capabilities.

**Option C: Remove maximum level**

Report only independent capabilities.

### Approved decision

**Approve Option B, with a capability matrix.**

### Frozen expected hero result

```text
maximum_observability_level: 4
dataset_longitudinal: available
lineage: available
model_longitudinal: unavailable
intervention: unavailable
```

### Approval

- [ ] Approve Level 4 plus capability matrix
- [ ] Select another option
- [ ] Return for revision

Decision notes:

```text

```

---

## UD-004. Capability matrix

| Field | Value |
|---|---|
| Status | `APPROVED` |
| Priority | `BLOCKING-PHASE-1` |
| Owner | Theory Owner |
| Technical review | Technical Maintainer |
| Source | `SPEC_AUDIT.md` B02-B03 |

### Decision needed

Should the report provide only one observability level, or a maximum level plus capability-specific status?

### Options

**Option A: One level only**

**Option B: Maximum level plus capability matrix**

Each capability receives:

- `available`
- `partial`
- `unavailable`
- `experimental`

### Approved decision

**Approve Option B.**

### Required initial capabilities

- ingestion
- content diagnostics
- provenance
- lineage
- dataset longitudinal comparison
- model longitudinal comparison
- intervention simulation

### Rationale

A dataset can provide Level 4 version comparison while still lacking model-performance evidence, complete lineage, embeddings, or intervention data.

### Approval

- [ ] Approve capability matrix
- [ ] Use one level only
- [ ] Return for revision

Decision notes:

```text

```

---

## UD-005. Meaning of `generation`

| Field | Value |
|---|---|
| Status | `APPROVED` |
| Priority | `BLOCKING-PHASE-2` |
| Owner | Theory Owner |
| Technical review | Mathematical Reviewer and Technical Maintainer |
| Source | `SPEC_AUDIT.md` B04 |

### Conflict

The current definition describes recursion depth from an external root. The hero fixture assigns `generation=0` to grounded carryovers that still have a parent edge.

### Options

**Option A: Graph depth**

Every parent edge increments generation.

**Option B: Consecutive non-grounding generation count**

`generation` counts consecutive non-grounding generative steps since the most recent external grounding.

**Option C: Remove the declared field**

Compute all depth values from the graph.

### Approved decision

**Approve Option B and add a separate derived `lineage_depth`.**

### Proposed definition

> `generation` is the number of consecutive non-grounding generative steps since the most recent externally grounded state. A grounded carryover may remain generation 0 while preserving a parent link.

### Required validation

- `generation >= 0`
- grounding `yes` may have generation 0
- grounding `no` with a known parent normally has generation at least 1
- declared generation and graph evidence are compared
- disagreement produces `W_GENERATION_MISMATCH`
- strict mode may elevate impossible combinations to errors

### Approval

- [ ] Approve consecutive non-grounding definition
- [ ] Use graph depth
- [ ] Remove declared generation
- [ ] Return for revision

Decision notes:

```text

```

---

## UD-006. Canonical parent reference encoding

| Field | Value |
|---|---|
| Status | `APPROVED` |
| Priority | `BLOCKING-PHASE-2` |
| Owner | Technical Maintainer |
| Theory review | Theory Owner |
| Source | `SPEC_AUDIT.md` B05 |

### Problem

`record_id` is unique only within a dataset version. Bare `parent_ids` can become ambiguous.

### Options

**Option A: Bare record IDs**

Resolve parent IDs globally.

**Option B: Separate parent version and parent ID columns**

Use repeated rows or additional columns.

**Option C: Composite references**

Use `dataset_version::record_id` inside a JSON array.

### Approved decision

**Approve Option C.**

### Canonical CSV form

```text
["v1::v1_01","v1::v1_02"]
```

### Compatibility rule

A bare ID may be accepted only when it resolves to exactly one loaded record.

- unique bare ID: warning or compatibility notice
- ambiguous bare ID: error
- canonical exports: always composite
- silent comma or delimiter guessing: forbidden

### Approval

- [ ] Approve composite references
- [ ] Select another encoding
- [ ] Return for revision

Decision notes:

```text

```

---

## UD-007. Dataset version ordering

| Field | Value |
|---|---|
| Status | `APPROVED` |
| Priority | `BLOCKING-PHASE-2` |
| Owner | Technical Maintainer |
| Theory review | Theory Owner |
| Source | `SPEC_AUDIT.md` N09 |

### Problem

String IDs such as `v2`, `v10`, `final`, and `archive` do not provide a reliable chronology.

### Options

**Option A: Lexical ordering**

**Option B: Natural numeric parsing**

**Option C: Explicit ordering contract**

Use one of:

- `version_order` in config,
- valid timestamps,
- user-declared CLI order.

### Approved decision

**Approve Option C.**

### Fallback behavior

When no ordering evidence exists:

- allow single-version analysis,
- block longitudinal conclusions,
- emit a specific warning or error,
- never infer chronology from filenames alone.

### Approval

- [ ] Approve explicit ordering contract
- [ ] Permit automatic filename ordering
- [ ] Return for revision

Decision notes:

```text

```

---

## UD-008. Provenance coverage definitions

| Field | Value |
|---|---|
| Status | `APPROVED` |
| Priority | `BLOCKING-PHASE-2` |
| Owner | Theory Owner |
| Technical review | Technical Maintainer |
| Source | `SPEC_AUDIT.md` B06 |

### Problem

One number called `provenance coverage` hides the difference between matching rows and meaningful field completeness.

### Approved decision

Approve three required measures:

1. `provenance_row_coverage`
2. `provenance_required_field_coverage`
3. `grounding_field_coverage`

### Definitions

\[
\text{provenance row coverage}
=
\frac{\text{records with a matching provenance row}}
{\text{total analyzed records}}
\]

\[
\text{required field coverage}
=
\frac{\text{records with valid required provenance fields}}
{\text{total analyzed records}}
\]

\[
\text{grounding field coverage}
=
\frac{\text{records with external grounding yes or no}}
{\text{total analyzed records}}
\]

### Hero correction

The hero fixture's 100 percent value should be named:

```text
v2_provenance_row_coverage: 1.00
```

### Approval

- [ ] Approve all three measures
- [ ] Modify the measure set
- [ ] Return for revision

Decision notes:

```text

```

---

## UD-009. Authority of `external_grounding`

| Field | Value |
|---|---|
| Status | `APPROVED` |
| Priority | `BLOCKING-PHASE-2` |
| Owner | Theory Owner |
| Source | `SPEC_AUDIT.md` B07; `THEORY_SOURCE_MAP.md` TM-P02 |

### Decision needed

Which field controls direct claims that a record introduces independent external signal?

### Options

**Option A: Derive grounding from `source_type`**

**Option B: Derive grounding from `human_reviewed`**

**Option C: Use `external_grounding` as the controlling declared field**

### Approved decision

**Approve Option C.**

### Required distinctions

- `source_type`: declared origin class
- `external_grounding`: relation to the audited recursive loop
- `human_reviewed`: review flag only
- `provenance_confidence`: confidence in the assignment

### Required rules

- human does not automatically mean grounded
- synthetic does not automatically mean closed
- mixed does not imply grounding
- human review does not create independent ancestry
- unknown remains unknown

### Approval

- [ ] Approve `external_grounding` authority
- [ ] Select another rule
- [ ] Return for revision

Decision notes:

```text

```

---

## UD-010. Closure exposure bounds

| Field | Value |
|---|---|
| Status | `APPROVED` |
| Priority | `BLOCKING-PHASE-3` |
| Owner | Theory Owner |
| Mathematical review | Required |
| Source | `SPEC_AUDIT.md` B08; `THEORY_SOURCE_MAP.md` TM-P01 |

### Decision needed

How should incomplete grounding metadata be converted into a transparent uncertainty interval?

### Recommended direct bounds

Classify every analyzed record:

- `known_open`: `external_grounding=yes`
- `known_closed`: `external_grounding=no`
- `unresolved`: missing, invalid, unknown, or lacking a matching provenance row

Then:

\[
C_{\min}
=
\frac{N_{\text{known closed}}}{N_{\text{total}}}
\]

\[
C_{\max}
=
\frac{N_{\text{known closed}}+N_{\text{unresolved}}}{N_{\text{total}}}
\]

### Lineage-aware bounds

At Level 3, compute a separate lineage envelope:

- known grounded: a resolved path reaches a confirmed external root
- known closed: complete known ancestry has no reachable external root
- unresolved: missing parent, incomplete ancestry, conflicting evidence, or unknown grounding

### Required disclosure

These bounds are a toolkit operationalization guided by theory. They are not a formula stated in the theory article.

### Approval

- [ ] Approve direct and lineage-aware bounds
- [ ] Approve direct bounds only
- [ ] Return for revision

Decision notes:

```text

```

---

## UD-011. Support representation selection

| Field | Value |
|---|---|
| Status | `APPROVED` |
| Priority | `BLOCKING-PHASE-3` |
| Owner | Theory Owner |
| Technical review | Technical Maintainer |
| Source | `SPEC_AUDIT.md` B09; `THEORY_SOURCE_MAP.md` TM-C04 |

### Problem

Support, diversity, tail, and extinction depend on how records are represented as states.

### Recommended selection order

1. explicit user configuration
2. `topic`
3. `label`
4. user-provided embedding clusters or bins
5. exact normalized content hash for record-form support only

### Required report metadata

- `representation_name`
- `representation_source`
- `representation_version`
- `binning_or_mapping_rule`

### Required restrictions

- no embedded LLM topic inference in v0.1
- exact hash support cannot be called semantic support
- version comparison requires compatible representations
- fallback use must generate `W_REPRESENTATION_FALLBACK`

### Approval

- [ ] Approve selection order
- [ ] Require explicit configuration only
- [ ] Modify fallback behavior
- [ ] Return for revision

Decision notes:

```text

```

---

## UD-012. Tail definition and default threshold

| Field | Value |
|---|---|
| Status | `APPROVED` |
| Priority | `BLOCKING-PHASE-3` |
| Owner | Theory Owner |
| Mathematical review | Required |
| Source | `SPEC_AUDIT.md` B10; `THEORY_SOURCE_MAP.md` TM-C06 |

### Decision needed

How should v0.1 define the low-frequency tail?

### Options

**Option A: Fixed frequency-share threshold**

Example: states below 1 percent.

**Option B: Quantile-based threshold**

Example: lowest 10 percent of states by frequency.

**Option C: Declared configurable rule with a simple hero default**

### Approved decision

**Approve Option C.**

### Proposed hero default

```text
tail_rule: singleton_count
tail_count_threshold: 1
```

A state belongs to the hero tail when its observed count equals 1.

### General behavior

- user-configured rules override the default,
- the full rarity ranking may include every state,
- alerts may be limited to the declared tail,
- threshold metadata must appear in reports.

### Approval

- [ ] Approve configurable rule and singleton hero default
- [ ] Select a global default
- [ ] Return for revision

Decision notes:

```text

```

---

## UD-013. Tail extinction evidence classification

| Field | Value |
|---|---|
| Status | `APPROVED` |
| Priority | `BLOCKING-PHASE-3` |
| Owner | Theory Owner |
| Mathematical review | Required |
| Source | `THEORY_SOURCE_MAP.md` TM-M04 |

### Decision needed

How should the one-step formula

\[
(1-p_i)^n
\]

appear in reports?

### Options

**Option A: Derived metric**

Present it as a direct risk estimate for the real pipeline.

**Option B: Simulation result**

Present it under an explicit finite closed-resampling scenario.

**Option C: Proxy only**

Do not expose the probability.

### Approved decision

**Approve Option B.**

### Evidence classes

- observed frequency: `observed_fact`
- rarity ranking: `derived_metric`
- one-step absence probability: `simulation`
- warning text based on the scenario: `proxy_signal`

### Required assumptions

- multinomial resampling
- sample size \(n\)
- one-step horizon
- declared representation
- no external reopening unless modeled

### Approval

- [ ] Approve simulation classification
- [ ] Hide the probability in v0.1
- [ ] Return for revision

Decision notes:

```text

```

---

## UD-014. Ancestry concentration convention

| Field | Value |
|---|---|
| Status | `APPROVED` |
| Priority | `BLOCKING-PHASE-3` |
| Owner | Theory Owner |
| Mathematical review | Required |
| Source | `SPEC_AUDIT.md` B11; `THEORY_SOURCE_MAP.md` TM-P04 |

### Problem

A record may have multiple reachable external roots. Simple counting can double-count ancestry.

### Recommended required outputs

- `distinct_external_root_count`
- `records_with_resolved_external_ancestry`
- `external_ancestry_coverage`
- `ancestor_incidence_count`
- `ancestor_incidence_share`
- `top_shared_ancestors`

### Recommended optional concentration convention

For each record with \(k\) reachable external roots, allocate \(1/k\) mass to each root.

Normalize aggregate root mass to shares \(w_a\).

\[
HHI_{\text{ancestry}}=\sum_a w_a^2
\]

\[
N_{\text{effective roots}}=\frac{1}{HHI_{\text{ancestry}}}
\]

### Required limits

- topology only
- no causal contribution claim
- no semantic-error claim
- parent weights, when later supported, require a separate method

### Hero interpretation

`v1_01` supports three v2 records by incidence count.

### Approval

- [ ] Approve incidence plus fractional HHI
- [ ] Approve incidence only
- [ ] Select another convention
- [ ] Return for revision

Decision notes:

```text

```

---

## UD-015. Missing and ambiguous parent behavior

| Field | Value |
|---|---|
| Status | `APPROVED` |
| Priority | `BLOCKING-PHASE-2` |
| Owner | Technical Maintainer |
| Theory review | Theory Owner |
| Source | `SPEC_AUDIT.md` B12 |

### Approved decision

Adopt the following behavior:

| Condition | Default behavior |
|---|---|
| Missing parent reference | Warning |
| Ambiguous parent reference | Error |
| Cycle | Lineage-analysis error |
| Parent in a future version under declared ordering | Error |
| Strict mode unresolved parent | Error |
| Missing parent treated as external root | Forbidden |

### Consequences

- partial lineage may still support Level 3 capability,
- every ancestry conclusion must state resolved coverage,
- unresolved edges widen lineage uncertainty,
- no external ancestry may be invented.

### Approval

- [ ] Approve behavior table
- [ ] Make all missing parents fatal
- [ ] Return for revision

Decision notes:

```text

```

---

## UD-016. Safe schema mapping operations

| Field | Value |
|---|---|
| Status | `APPROVED` |
| Priority | `BLOCKING-PHASE-2` |
| Owner | Technical Maintainer |
| Security review | Required |
| Source | `SPEC_AUDIT.md` B13 |

### Problem

The current schema allows an unspecified transformation expression.

### Recommended allowed operations

- rename
- declared type cast
- datetime parse with declared format
- JSON-list parse
- constant assignment
- coalesce among named fields
- whitespace normalization

### Forbidden operations

- `eval`
- arbitrary Python
- shell execution
- network calls
- remote plugin execution
- hidden content classification
- arbitrary user-defined code

### Required audit behavior

Every transformation must appear in normalized run metadata.

### Approval

- [ ] Approve declarative-only mapping
- [ ] Define a separate sandboxed expression language
- [ ] Return for revision

Decision notes:

```text

```

---

## UD-017. Phase 6 split

| Field | Value |
|---|---|
| Status | `APPROVED` |
| Priority | `BLOCKING-PHASE-1` |
| Owner | Theory Owner |
| Technical review | Technical Maintainer |
| Source | `SPEC_AUDIT.md` B14 |

### Conflict

The phase plan combines longitudinal analysis and controlled interventions without an intervention-data schema.

### Approved decision

Split Phase 6 into:

### Phase 6A: required v0.1 longitudinal comparison

- version deltas
- support loss
- tail extinction
- provenance change
- ancestry change where available

### Phase 6B: optional experimental simulation

- closed-resampling scenarios
- external reopening scenarios
- explicit assumptions
- fixed seeds
- experimental label

### Deferred

Empirical controlled-intervention ingestion and causal comparison.

### Approval

- [ ] Approve Phase 6A and 6B split
- [ ] Remove Phase 6B from v0.1
- [ ] Define empirical intervention schema now
- [ ] Return for revision

Decision notes:

```text

```

---

## UD-018. Cycle detection classification

| Field | Value |
|---|---|
| Status | `APPROVED` |
| Priority | `BLOCKING-PHASE-2` |
| Owner | Theory Owner |
| Technical review | Technical Maintainer |
| Source | `THEORY_SOURCE_MAP.md` TM-P05 |

### Decision needed

Should cycle rejection be presented as a direct theory claim or as an engineering rule of the chosen lineage representation?

### Approved decision

Classify cycle rejection as a **graph-validity engineering rule**.

### Rationale

The provenance graph models generational ancestry. A cycle invalidates that interpretation. Real-world feedback loops may still exist and can be represented through runs, versions, or process-level edges outside the record-ancestry DAG.

### Required consequence

Trace ID T6 must identify its source class as:

```text
implementation_integrity_rule
```

### Approval

- [ ] Approve engineering-rule classification
- [ ] Retain theory-claim classification
- [ ] Return for revision

Decision notes:

```text

```

---

## UD-019. Human-readable report requirement

| Field | Value |
|---|---|
| Status | `APPROVED` |
| Priority | `BLOCKING-PHASE-4` |
| Owner | Technical Maintainer |
| Product review | Theory Owner |
| Source | Migration package report requirements |

### Options

**Option A: Markdown required, HTML optional**

**Option B: HTML required, Markdown optional**

**Option C: Both required**

### Approved decision

**Approve Option A.**

### Required Phase 4 outputs

- JSON report
- Markdown report
- CLI entrypoint

### Optional output

- HTML report generated from structured results

### Approval

- [ ] Approve Markdown required, HTML optional
- [ ] Require both
- [ ] Return for revision

Decision notes:

```text

```

---

## UD-020. Near-duplicate analysis scope

| Field | Value |
|---|---|
| Status | `APPROVED` |
| Priority | `BLOCKING-PHASE-3` |
| Owner | Theory Owner |
| Technical review | Technical Maintainer |
| Source | Product scope and `SPEC_AUDIT.md` N02 |

### Problem

Near-duplicate analysis depends on representation, method, and threshold. The current product spec lists it without freezing those choices.

### Approved decision

- exact duplicate detection: required
- near-duplicate detection: optional
- embeddings: user-provided in v0.1
- deterministic text similarity: allowed only when explicitly configured
- default semantic model download: forbidden
- universal default similarity threshold: not provided

### Approval

- [ ] Approve optional near-duplicate scope
- [ ] Remove near-duplicates from v0.1
- [ ] Freeze a default method now
- [ ] Return for revision

Decision notes:

```text

```

---

## UD-021. Weighted analysis behavior

| Field | Value |
|---|---|
| Status | `APPROVED` |
| Priority | `BLOCKING-PHASE-3` |
| Owner | Theory Owner |
| Mathematical review | Required |
| Source | `SPEC_AUDIT.md` N10 |

### Approved decision

Unweighted analysis is the default.

Weighted analysis:

- requires explicit opt-in,
- uses separate output field names,
- rejects negative weights,
- rejects an all-zero weight vector,
- does not replace unweighted results,
- records the normalization rule.

### Approval

- [ ] Approve unweighted default plus opt-in weighted outputs
- [ ] Ignore weights in all v0.1 analysis
- [ ] Make weights automatic when present
- [ ] Return for revision

Decision notes:

```text

```

---

## UD-023. Code and documentation licenses

| Field | Value |
|---|---|
| Status | `APPROVED` |
| Priority | `BLOCKING-PHASE-1` |
| Owner | Theory Owner |
| Legal review | Optional before public release |
| Source | Migration package licensing notes |

### Approved decision

| Asset | License |
|---|---|
| Source code | Apache License 2.0 |
| Repository specifications and reusable documentation | CC BY 4.0 |
| Example datasets created for the repository | CC BY 4.0 |
| Theory PDFs | Preserve their existing license |
| Third-party fixtures | Their original license and attribution requirements |

### Alternative simplicity option

Use Apache-2.0 for code and repository Markdown files, while retaining separate theory licenses.

### Decision needed

Choose one:

- split code and documentation licenses,
- single Apache-2.0 repository license,
- another reviewed arrangement.

### Approval

- [ ] Approve Apache-2.0 code and CC BY 4.0 docs/examples
- [ ] Approve single Apache-2.0 repository license
- [ ] Select another arrangement

Decision notes:

```text

```

---

## UD-024. Theory PDF inclusion in the public repository

| Field | Value |
|---|---|
| Status | `APPROVED` |
| Priority | `BLOCKING-PHASE-1` |
| Owner | Theory Owner |
| Source | Migration package licensing notes |

### Options

**Option A: Include full PDFs in the repository**

**Option B: Link to canonical publications and include citations only**

**Option C: Include PDFs in the private Project source bundle but exclude them from the public repository**

### Approved decision

**Approve Option C by default.**

The public repository should include:

- full citations,
- DOI or canonical publication references,
- theory version identifiers,
- a theory-source manifest,
- no modified theory PDFs.

Full PDFs may be added later when redistribution intent and repository size policy are confirmed.

### Approval

- [ ] Approve private bundle plus public references
- [ ] Include full PDFs publicly
- [ ] Use links only everywhere
- [ ] Return for revision

Decision notes:

```text

```

---

## UD-025. Python version and dependency ceiling

| Field | Value |
|---|---|
| Status | `APPROVED` |
| Priority | `BLOCKING-PHASE-1` |
| Owner | Technical Maintainer |
| Product review | Theory Owner |

### Recommended runtime

```text
Python >= 3.11
```

### Recommended core dependencies

- standard library
- `pandas` for tabular ingestion and normalization
- `pyarrow` as an optional extra for Parquet
- `numpy` for numerical metrics and deterministic simulations
- `networkx` only if graph implementation review shows that a custom graph layer would reduce auditability less
- `pydantic` only if schema validation review justifies it

### Recommended principle

Dependencies must be justified file by file during Phase 1.

### Decision needed

Choose the graph and validation approach:

**Option A: Minimal third-party stack**

Use pandas, numpy, optional pyarrow, and small custom validation/graph code.

**Option B: Standard libraries for graph and validation**

Add networkx and pydantic.

### Approved decision

Approve Python 3.11 and defer the exact graph/validation dependency choice to the Phase 1 dependency review.

### Approval

- [ ] Approve Python 3.11 baseline
- [ ] Select another Python baseline
- [ ] Approve dependency review during Phase 1

Decision notes:

```text

```

---

## UD-026. Package and CLI naming

| Field | Value |
|---|---|
| Status | `APPROVED` |
| Priority | `BLOCKING-PHASE-1` |
| Owner | Theory Owner |
| Technical review | Technical Maintainer |

### Recommended names

| Object | Name |
|---|---|
| Repository | `recursive-integrity-toolkit` |
| Python package | `recursive_integrity_toolkit` |
| CLI executable | `rit` |
| Long CLI form | `recursive-integrity` |
| Initial version | `0.1.0` only at official release; development versions use `0.1.0.devN` |

### Decision needed

Approve or change the short CLI name.

### Approval

- [ ] Approve repository and package names
- [ ] Approve CLI name `rit`
- [ ] Select another CLI name

Decision notes:

```text

```

---

## UD-032. Release labels and approval authority

| Field | Value |
|---|---|
| Status | `APPROVED` |
| Priority | `BLOCKING-PHASE-1` |
| Owner | Theory Owner |
| Technical review | Technical Maintainer |
| Source | `GOVERNANCE_AND_HANDOFF.md` draft |

### Recommended release labels

- `experimental`
- `reviewed`
- `official-v0.1`

### Recommended approval rules

#### Experimental

May be released when:

- clearly labeled,
- tests exist for basic behavior,
- limits are documented.

#### Reviewed

Requires:

- tests,
- documentation,
- traceability mapping,
- relevant reviewer approval.

#### Official v0.1

Requires:

- Theory Owner approval,
- Technical Maintainer approval,
- all release gates,
- golden outputs,
- coherent licensing,
- no unresolved blocking decisions.

### Approval

- [ ] Approve release labels and authority
- [ ] Modify the label set
- [ ] Return for revision

Decision notes:

```text

```

---

## UD-033. Hero fixture corrections

| Field | Value |
|---|---|
| Status | `APPROVED` |
| Priority | `BLOCKING-PHASE-1` |
| Owner | Theory Owner |
| Technical review | Technical Maintainer |
| Source | `SPEC_AUDIT.md` hero fixture audit |

### Required corrections

- maximum observability level becomes 4
- capability matrix is added
- representation is declared as `topic`
- `provenance coverage` becomes `provenance row coverage`
- support contraction becomes `topic support contraction`
- top ancestor result identifies incidence-count convention
- parent references become canonical composite references or documented compatibility inputs
- model-performance conclusions remain unavailable
- universal collapse remains unavailable

### Golden values retained

```text
v1_topic_support: 8
v2_topic_support: 5
extinct_topics: [lizard, turtle, battery]
v2_provenance_row_coverage: 1.00
v2_human_share: 0.50
v2_synthetic_share: 0.50
v2_unknown_share: 0.00
distinct_external_roots_supporting_v2: 5
top_shared_external_root: v1_01
top_shared_external_root_incidence: 3
maximum_observability_level: 4
```

### Approval

- [ ] Approve all hero corrections
- [ ] Modify expected values
- [ ] Return for revision

Decision notes:

```text

```

---

## UD-035. Public use of the word `collapse`

| Field | Value |
|---|---|
| Status | `APPROVED` |
| Priority | `BLOCKING-PHASE-4` |
| Owner | Theory Owner |
| Source | Theory sources and migration-package hard constraints |

### Approved decision

The word `collapse` may appear in:

- project motivation,
- theory references,
- names of cited research phenomena,
- unavailable conclusions,
- documentation explaining what v0.1 cannot predict.

The word must not appear as:

- a metric name,
- a score,
- a direct result from support contraction alone,
- a universal prediction,
- a hidden threshold label.

### Preferred result language

Use:

- support contraction
- tail extinction
- closure exposure
- ancestry concentration
- provenance incompleteness
- unavailable functional-failure conclusion

### Approval

- [ ] Approve restricted use
- [ ] Prohibit the word entirely in reports
- [ ] Permit direct collapse warnings
- [ ] Return for revision

Decision notes:

```text

```

---

# PART II. NONBLOCKING v0.1 DECISIONS

## UD-022. OpenLineage and ML Metadata integration

| Field | Value |
|---|---|
| Status | `APPROVED` |
| Priority | `NONBLOCKING-V0.1` |
| Owner | Technical Maintainer |
| Theory review | Theory Owner |

### Options

**Option A: Native dependency in core v0.1**

**Option B: Compatible internal model with later adapters**

**Option C: No compatibility target**

### Approved decision

**Approve Option B.**

v0.1 should:

- use concepts compatible with datasets, runs, jobs/executions, artifacts, contexts, and facets,
- preserve stable IDs and sidecar manifests,
- avoid making OpenLineage or ML Metadata mandatory runtime dependencies,
- defer import/export adapters until the core schema is stable.

### Approval

- [ ] Approve compatible internal model and deferred adapters
- [ ] Require native integration
- [ ] Remove compatibility requirement

Decision notes:

```text

```

---

## UD-027. CI platform coverage

| Field | Value |
|---|---|
| Status | `APPROVED` |
| Priority | `NONBLOCKING-V0.1` |
| Owner | Technical Maintainer |

### Recommended minimum

GitHub Actions matrix:

- Ubuntu
- Windows
- Python 3.11
- Python 3.12

Optional before official release:

- macOS
- Python 3.13 after dependency verification

### Required CI jobs

- unit tests
- integration test
- hero smoke test
- golden report comparison
- no-network test where practical
- formatting and static checks chosen during Phase 1

### Approval

- [ ] Approve minimum CI matrix
- [ ] Add macOS immediately
- [ ] Modify Python versions

Decision notes:

```text

```

---

## UD-034. Additional lineage golden fixture

| Field | Value |
|---|---|
| Status | `APPROVED` |
| Priority | `BLOCKING-PHASE-3` |
| Owner | Technical Maintainer |
| Mathematical review | Required |

### Recommended fixture content

A second valid fixture must include:

- one record with two external roots,
- unequal ancestor incidence,
- one unresolved parent,
- one unknown grounding value.

Separate failure fixtures must include:

- ambiguous bare parent ID,
- self-cycle,
- multi-node cycle,
- future-version parent.

### Purpose

The current hero graph is too simple to validate fractional ancestry allocation, uncertainty, and graph failures.

### Approval

- [ ] Approve fixture requirements
- [ ] Defer advanced lineage tests
- [ ] Return for revision

Decision notes:

```text

```

---

## UD-036. HTML report support

| Field | Value |
|---|---|
| Status | `APPROVED` |
| Priority | `NONBLOCKING-V0.1` |
| Owner | Technical Maintainer |

### Approved decision

HTML remains optional.

It may be generated from the structured JSON result or Markdown report after required outputs pass.

### Restrictions

- no web server
- no client telemetry
- no external script dependency by default
- safe escaping of record IDs and user-provided metadata
- redacted mode support

### Approval

- [ ] Approve optional HTML
- [ ] Remove HTML from v0.1
- [ ] Make HTML required

Decision notes:

```text

```

---

# PART III. EXPLICITLY DEFERRED DECISIONS

## UD-028. Effective source diversity

| Field | Value |
|---|---|
| Status | `DEFERRED` |
| Priority | `DEFERRED-POST-V0.1` |
| Owner | Theory Owner |
| Source | `THEORY_SOURCE_MAP.md` deferred research queue D03 |

### Reason for deferral

A reliable metric requires decisions about:

- source identity,
- shared ownership,
- common generator ancestry,
- copied and transformed records,
- source weights,
- independence,
- correlated provenance.

### v0.1 behavior

The toolkit may report:

- source-type shares,
- distinct declared generator IDs,
- distinct external roots,
- ancestry concentration.

It must not report a universal effective source-diversity score.

### Reopening condition

Create a new Theory Map entry and metric specification after the dependence model is approved.

---

## UD-029. Universal integrity, quality, presence, and stability scores

| Field | Value |
|---|---|
| Status | `DEFERRED` |
| Priority | `DEFERRED-POST-V0.1` |
| Owner | Theory Owner |
| Source | `THEORY_SOURCE_MAP.md` TM-C03, TM-C05, TM-S01, TM-S02 |

### Frozen decision for v0.1

The following are prohibited as numeric public scores:

- universal integrity
- universal quality
- universal presence
- universal stability
- combined collapse score

The formulas

\[
Q=I\times D
\]

and

\[
S=P\times I
\]

remain theory-level structural dependencies.

### Reopening condition

A future domain-specific implementation requires units, calibration, external validation, and a defined reference structure.

---

## UD-030. Amplification-dominant analysis

| Field | Value |
|---|---|
| Status | `DEFERRED` |
| Priority | `DEFERRED-POST-V0.1` |
| Owner | Theory Owner |
| Source | `THEORY_SOURCE_MAP.md` TM-A01-TM-A04 |

### Deferred capabilities

- transfer-matrix input
- spectral-radius threshold
- defect reproduction analysis
- delayed visibility model
- path-interruption intervention model

### v0.1 behavior

The contraction-focused toolkit may preserve the taxonomy in documentation. No amplification score or threshold appears in public output.

---

## UD-031. Controlled empirical intervention ingestion

| Field | Value |
|---|---|
| Status | `DEFERRED` |
| Priority | `DEFERRED-POST-V0.1` |
| Owner | Theory Owner and Domain Validator |
| Source | `SPEC_AUDIT.md` B14 |

### Reason for deferral

No approved schema currently defines:

- treatment,
- control,
- assignment,
- timing,
- outcome,
- confounding,
- causal interpretation.

### v0.1 behavior

Only explicit mathematical or stochastic scenario comparison is permitted, and every result remains experimental.

---

# PART IV. APPROVED DEFAULTS THAT SHOULD NOT BE REOPENED SILENTLY

The following defaults are approved as a group. Any later change requires a recorded update.

| Topic | Recommended default |
|---|---|
| Execution | Local-first |
| Network calls | None required during analysis |
| Telemetry | None |
| Raw content in logs | Excluded |
| Randomness | Fixed seed when simulation is enabled |
| Unknown provenance | Preserved as unknown |
| Human review | Does not prove external grounding |
| Mixed source type | Remains a separate category |
| Default metric weighting | Unweighted |
| Core diversity metric | Gini-Simpson |
| Exact duplicates | Required |
| Near-duplicates | Optional |
| Semantic topic inference | No embedded LLM in v0.1 |
| Human-readable output | Markdown |
| Machine-readable output | JSON |
| HTML | Optional |
| Database | None required |
| Web app | Out of scope |
| Cloud service | Out of scope |
| Automatic policy enforcement | Out of scope |
| Universal failure threshold | Out of scope |
| Multimodal parity | Out of scope |
| Theory PDFs | Separate reference assets |
| Public report evidence classes | Observed, derived, proxy, simulation, unavailable |
| Phase stop rule | Complete only the approved phase |

Group approval:

- [x] Approve all defaults in this table
- [ ] Approve with exceptions listed below
- [ ] Return for revision

Exceptions:

```text

```

---

# PART V. DECISION PROPAGATION CHECKLIST

After decisions are approved, update the following files.

## `PROJECT_INSTRUCTIONS.md`

- [ ] Add dual authority model
- [ ] Add capability matrix rule
- [ ] Add no-silent-decision rule
- [ ] Add safe mapping restriction
- [ ] Add Phase 6 split
- [ ] Add evidence-class requirement

## `V0.1_PRODUCT_SPEC.md`

- [ ] Freeze ML pipeline domain
- [ ] Freeze required and optional report formats
- [ ] Freeze near-duplicate scope
- [ ] Freeze Phase 6A and Phase 6B
- [ ] Freeze OpenLineage and ML Metadata adapter status

## `DEFINITIONS_AND_UNITS.md`

- [ ] Revise `generation`
- [ ] Add `lineage_depth`
- [ ] Add provenance coverage definitions
- [ ] Add external root definition
- [ ] Add closure exposure bounds
- [ ] Add representation metadata
- [ ] Add ancestry concentration convention
- [ ] Add weighted-analysis distinctions

## `DATA_AND_PROVENANCE_SPEC.md`

- [ ] Freeze composite parent encoding
- [ ] Freeze missing-parent behavior
- [ ] Freeze version ordering
- [ ] Freeze declarative mapping operations
- [ ] Freeze local reference behavior
- [ ] Add compatibility rules

## `OBSERVABILITY_AND_REPORTING.md`

- [ ] Correct hero maximum level
- [ ] Add capability matrix
- [ ] Separate dataset and model longitudinal analysis
- [ ] Classify tail probability as simulation
- [ ] Add lineage coverage disclosures
- [ ] Restrict collapse language
- [ ] Freeze Markdown as required and HTML as optional

## `THEORY_TO_CODE_TRACEABILITY.md`

- [ ] Reconcile T1-T6 with Theory Map IDs
- [ ] Reclassify T6
- [ ] Add scenario assumptions
- [ ] Add toolkit-operationalization labels
- [ ] Add deferred objects
- [ ] Add product-only engineering rules

## `VALIDATION_PLAN.md`

- [ ] Add generation mismatch test
- [ ] Add ambiguous parent test
- [ ] Add unresolved parent test
- [ ] Add multi-root ancestry test
- [ ] Add representation compatibility test
- [ ] Add unsafe mapping rejection
- [ ] Add Level 4 hero assertion
- [ ] Add weighted-analysis opt-in test
- [ ] Add restricted report-language golden test

## Hero files

- [ ] Update parent references
- [ ] Update expected observability
- [ ] Rename provenance coverage
- [ ] Declare topic representation
- [ ] Add capability matrix expectations
- [ ] Add model-performance unavailable conclusion

---

# PART VI. FINAL APPROVAL

## Theory Owner approval

I approve the decisions selected in this register as the controlling v0.1 baseline.

Theory Owner:

```text
Xiangyu Guo
```

Approval date:

```text
2026-07-29
```

Decision register version:

```text
0.1-approved
```

Overall status:

- [x] `APPROVED FOR PHASE 1`
- [ ] `APPROVED WITH EXCEPTIONS`
- [ ] `RETURNED FOR REVISION`

Approved exceptions:

```text

```

## Technical Maintainer acknowledgment

Technical Maintainer:

```text

```

Acknowledgment date:

```text

```

Acknowledgment:

- [ ] The approved decisions can be implemented without hidden defaults.
- [ ] Remaining technical ambiguities are listed below.
- [ ] Phase 1 may begin after specification propagation is complete.

Remaining technical ambiguities:

```text

```

---

## Change-control rule

After approval:

1. each changed decision must keep its original ID,
2. the status and decision date must be updated,
3. the previous choice must remain visible in version history,
4. downstream specifications must be updated in the same change,
5. implementation may not precede specification propagation,
6. a deferred decision may enter implementation only after a new Theory Map entry, tests, report fields, limits, and approval are added.
