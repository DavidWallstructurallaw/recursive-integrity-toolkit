# PHASE_3_PLAN

## Document control

| Field | Value |
|---|---|
| Project | Recursive Integrity Toolkit |
| Target product | v0.1 |
| Phase | Phase 3: Deterministic Metrics and Closed-Resampling Mathematical Core |
| Document version | 1.0 |
| Planning date | 2026-09-17 |
| Status | DRAFT FOR THEORY OWNER APPROVAL |
| Prior milestone | Phase 2 final delivery accepted by the Theory Owner in the current conversation |
| Planning baseline | `78554993febb01609cb90814cc24cce2012bf7d7` |
| Baseline branch | `phase2-step1-core-contracts` |
| Main observed during planning | `cfe1bd0941c1125498ac3d9d9ebf3adafa2c2fcb`, unchanged |
| Primary implementation owners | Technical Maintainer and Mathematical Reviewer |
| Theory Owner | Xiangyu Guo |
| Implementation authorized by this document now | No |
| Repository changes authorized by this planning task | None |
| Main merge, tag, or package publication authorized | No |
| Next action | Review this plan, including the explicit decisions in section 3 |

This document is the sole deliverable of the current planning task. It does not execute any implementation step, update the repository, create a branch, or merge `main`.

The approved Phase 0 definitions remain the numerical and conceptual basis. Section 3 identifies overlaps and underspecified implementation details rather than silently resolving them. Its recommendations require approval before the affected implementation begins. Approval of Phase 2 does not itself approve these new recommendations.

After plan approval, execution remains one explicitly authorized step at a time. Approval of the plan alone does not instruct an automatic run through the phase.

---

## 1. Verified starting point and source basis

### 1.1 Accepted implementation snapshot

The GitHub branch was read during planning and still points to the baseline commit above. Planning uses that immutable commit, not an assumed future branch head.

The Phase 2 completion and validation records establish the following historical results:

| Baseline property | Accepted Phase 2 evidence |
|---|---|
| Core suite | 1,159 passed, with actual PyArrow absence |
| Complete extra-enabled suite | 1,162 passed with real PyArrow, including the three additional presence cases |
| Required platform matrix | Ubuntu and Windows, Python 3.11 and 3.12, all successful |
| Security and Hero subsets | 324 and 33 passed respectively; both are subsets, not additional distinct totals |
| Package | 40 Python modules; 26 protected docstring-only modules |
| Approved authority | 16 Phase 0 source hashes match the current approval manifest |
| Distribution verification | Wheel, sdist, strict metadata checks, and fresh installed-wheel checks passed |
| Hero | Installed `validate_bundle(...)` recognizes Level 4; model longitudinal remains unavailable |
| Source delivery | 197 tracked files in the final single-root repository ZIP |
| Runtime declarations | Python `>=3.11`; NumPy `>=2.0`; pandas `>=2.2`; PyArrow remains optional |
| Package version | `0.1.0.dev1` |
| Main/release status | No main merge and no stable v0.1 publication |

These are accepted baseline results, not tests newly executed while writing this plan. Phase 3 must rerun the applicable gates on its own commits. The old PyArrow validation gap is closed and must not reappear as an accepted omission. [P2-C; P2-V; P2-A; P2-F]

### 1.2 Documents actually used

The sixteen approved Phase 0 texts were read from the supplied final Phase 1 archive and checked against its approval manifest. Those manifest entries match the current GitHub `PHASE_0_APPROVAL.md` at the pinned baseline. Earlier standalone copies in the conversation have different hashes; they must not replace these approved bytes.

The three supplied Phase 2 milestone Markdown files also match their current Git blob identities. Current repository reads additionally establish the executable boundaries, configuration types, workflow tests, shared-module placeholder tests, and the release script's Phase 2-specific restrictions.

Appendix A lists every controlling Phase 0 file and its approved SHA-256. Appendix B supplies section-level citations and the relevant current-code inspection points. The project-supplied `PHASE_2_PLAN.md` and its conversation approvals are historical execution context; the current Phase 2 milestone records distinguish the delivered implementation from that original plan.

### 1.3 Authority without silent replacement

Apply the dual authority model in `SPEC_AUDIT.md` section 3 and `PROJECT_INSTRUCTIONS.md` section 4:

- Theory publications control conceptual meaning and the limits of their mathematical claims.
- Approved product decisions control operational definitions, denominators, fields, and product scope.
- The exact-contract sequence in `PROJECT_INSTRUCTIONS.md` section 4.4 remains in force.
- This plan controls execution order and file permissions only after approval. A proposed departure or refinement must be expressly recorded under section 3 and the governance change classes.

Do not reinterpret an obsolete unchecked approval box as an open decision when the blanket approval and decision status already establish approval. Do not alter a frozen source's hash to resolve a conflict.

The authoritative theory corpus for this milestone remains TS1, TS2, and TS3 in `THEORY_SOURCE_MAP.md`: the Universal Inbreeding Law v2; the entropy boundary paper v2; and the Supplementary Case Registry v2.0. Their source passages govern the exact resampling model and its limits. Other supplied papers, including Evaluation Closure, the Heat Death of Language, Boundary Vacuum Law, and the Source Integrity Layer, do not automatically add new owners, formulas, or capabilities to this approved product baseline. [S01; S02; S04]

---

## 2. Phase objective and precise scope

Phase 3 supplies the calculation layer above the accepted input layer. It converts valid, explicitly scoped inputs into inspectable mathematical results with units, evidence classes, assumptions, and traceability.

### 2.1 Required owner coverage

| Owner | Phase 3 delivery |
|---|---|
| T1 | State frequencies, support, Gini-Simpson diversity, approved pairwise mathematical comparisons, expected closed-resampling contraction, and explicitly invoked fixed-seed closed-resampling kernels |
| T2 | Declared tail selection, rarity ranking, and analytic one-step closed-multinomial extinction probabilities |
| T3 | Direct grounding classification and direct closure-exposure intervals only |
| PR-005 | Source-type counts/shares and separately disclosed provenance-confidence composition |
| PR-006 | Exact record-form representation, duplicate groups, duplicate counts |
| PR-004 supporting basis | Reuse and expose accepted validation coverage without changing its definitions or duplicating join semantics |
| PR-007 / PR-011 supporting basis | Explicit pair-order and representation-compatibility checks; preserve input eligibility and its limitations |
| PR-016 supporting basis | Stable ordering, numerical reproducibility, seeds and method metadata for the implemented calculations |

The required owner set follows `VALIDATION_PLAN.md` section 79 and `THEORY_TO_CODE_TRACEABILITY.md` section 46. Supporting owners do not authorize their complete later-phase feature families. [S09; S10]

### 2.2 Selected representation scope

Required: explicit topic fields, explicit label fields, and exact UTF-8 record-form hashing with a declared profile. Implement the three approved missing-value policies for these modes. State identifiers remain literal and case-sensitive unless an explicit approved mapping says otherwise.

The priority policy from UD-011 may be used when the caller explicitly requests selection: explicit configuration, topic, label, supported user-provided bins, then exact record form. Selection must record its basis and emit the applicable fallback warning. An invalid explicit configuration must not be silently replaced by a different representation.

Raw embedding loading, embedding generation, cluster fitting, a generic executable representation plugin, and automatic semantic classification are excluded. The optional preassigned-embedding mode has additional metadata requirements; this plan does not invent the missing runtime input contract for it. An unsupported mode must remain explicit and unavailable, rather than being relabeled as topic or label data. A caller may separately map supplied categorical labels into the approved label representation without claiming that the toolkit validated their embedding origin. [S03 UD-011/020; S05 section 11; S07 section 13]

### 2.3 Formula allocation

| Formula IDs | Phase 3 treatment |
|---|---|
| F-001, F-002, F-003, F-004 | Implement frequencies, positive-mass support, Gini-Simpson diversity and its explicitly named Simpson companion |
| F-007 | Implement unweighted source shares and expressly requested weighted source-share variants |
| F-008 | Preserve the Phase 2 coverage basis and all three distinct coverage measures |
| F-009, F-010 | Implement direct closure lower and upper bounds, with width derived from the same unresolved count |
| F-014 | Implement analytic one-step extinction as a simulation quantity |
| F-015 | Implement expected contraction and its fixed-size, multi-step extension as scenario quantities |
| F-005, F-006, F-018 | Implement only the explicit pairwise kernels described in decision P3-D03 |
| F-011, F-012, F-013 | Phase 5; no ancestor incidence, ancestry HHI, or effective roots here |
| F-016, F-017 | Not selected for this phase; external-reference loss and external reopening remain for separately approved Phase 6B work |
| F-019 | Not selected here; relative-change orchestration remains with longitudinal work |

A formula's approval for v0.1 does not make every use of it part of Phase 3. This table is an implementation allocation, not a revision of the formula registry. [S06 section 26; S09 sections 6-11, 46-50]

### 2.4 Mathematical core to transcribe, not extend

For the selected nonempty record scope and its declared representation:

\[
p_i=\frac{n_i}{N},\qquad
K=|\{i:p_i>0\}|,\qquad
D=1-\sum_i p_i^2.
\]

For the direct grounding partition:

\[
C_{\min}^{\mathrm{direct}}=\frac{N_C}{N},\qquad
C_{\max}^{\mathrm{direct}}=\frac{N_C+N_U}{N},\qquad
W_C^{\mathrm{direct}}=\frac{N_U}{N}.
\]

For the explicitly declared closed categorical scenario:

\[
X_t\mid p_t\sim\operatorname{Multinomial}(n,p_t),\qquad
p_{t+1}=X_t/n,
\]

\[
\Pr(p_{t+1,i}=0\mid p_{t,i})=(1-p_{t,i})^n,
\]

\[
\mathbb E[D_{t+1}\mid p_t]=(1-1/n)D_t,\qquad
\mathbb E[D_t]=(1-1/n)^tD_0\quad\text{for fixed }n.
\]

These equations retain their source meanings. The expectation statement does not assert monotonicity of every sampled diversity path. The direct interval is a toolkit operationalization; it is not presented as a theorem quoted from TS1. [S06 sections 5, 7, 9, 12; S09 T1/T2/T3; TS1 pages 6-9]

---

## 3. Explicit decisions requiring approval

All P3-D entries below are **PROPOSED, NOT YET APPROVED**. They are local Phase 3 decision identifiers, not replacements for UD identifiers.

A complete approval of this plan should expressly include the recommended resolutions. An approval with exceptions leaves the affected step blocked. The subsequent implementation record must identify the decision, affected owners and tests, and the real reviewer roles. No reviewer approval is implied by generating this document.

### P3-D01. Phase 3 versus Phase 5: ancestry stays together with graph validity

**Sources:** `PROJECT_INSTRUCTIONS.md` section 6 lists approved ancestry metrics under Phase 3; `REPOSITORY_ARCHITECTURE.md` sections 10 and 15 allocate the lineage layer to Phase 5; `VALIDATION_PLAN.md` sections 79 and 81 and traceability sections 46 and 48 explicitly reserve T4, T6, full lineage behavior, lineage depth, and T3 lineage bounds for Phase 5.

**Conflict consequence:** A broad reading of the Phase 3 paragraph would allow ancestry calculations before the graph-validity implementation on which their meaning depends.

**Recommended resolution:** Implement no T4 or T6 behavior in Phase 3. Preserve existing immediate-parent and generation validation from Phase 2. Do not trace roots, accumulate ancestor sets, calculate fractional root mass, compute ancestry HHI, classify lineage closure, or claim general acyclicity. Even a generic square-and-sum helper must not be exposed as `ancestry_hhi` using unvalidated root inputs.

**Affected ownership:** T3 lineage branch, T4, T6, PR-008 full graph branch, PR-009 lineage depth; UD-014, UD-018, UD-034. Their required multi-root and cycle tests remain Phase 5 acceptance, with structural protection tests retained now.

### P3-D02. Phase 3 versus Phase 6B: mathematical kernel versus experiment workflow

**Sources:** Phase 3 expressly requires resampling and fixed-seed tests in `PROJECT_INSTRUCTIONS.md` section 6, `SUCCESS_CRITERIA.md` section 15, validation sections 17 and 79, and traceability section 6. UD-017 and traceability section 50 also place closed scenarios, extinction scenarios and reopening scenarios in Phase 6B.

**Recommended resolution:** Phase 3 implements the explicit mathematical functions for a fixed finite closed categorical model, including sampled paths required by the Phase 3 gate. Their calls require supplied parameters; their results are labeled `simulation` and `experimental`. They are library kernels and mathematical tests, not an experimental audit workflow.

Phase 6B remains responsible for configured experiment orchestration, closed-versus-open comparisons, external distribution ingestion/use, reopening weight, re-entry events, experiment grids, and experimental report integration. T5 and F-016/F-017 are not selected here. Do not accept a reopening parameter and silently ignore it.

The existing `validate_bundle(...)` and `ScenarioConfig.enabled` must not start simulations. The default Hero must still perform no simulation. A separately configured mathematical test may call the closed kernel explicitly. The presence of a kernel or an eligible scenario must never be reported as execution of the complete Phase 6B workflow.

**Affected ownership:** T1.C/D/E, T2.C, T5, PR-011; UD-013/017. No Phase 6B completion is claimed.

### P3-D03. Phase 3 versus Phase 6A: pairwise formulas without longitudinal orchestration

**Sources:** Validation sections 13 and 14 prescribe hand-calculated Hero diversity deltas, support deltas, retention and extinct-state sets. Traceability section 6 includes `compare_support` and related tests. UD-017, validation section 82 and traceability section 49 place longitudinal comparisons in Phase 6A.

**Recommended resolution:** Phase 3 may implement pure pairwise support/diversity kernels and the compatibility checks needed to give those kernels a valid meaning. Their invocation requires explicitly selected earlier/later scopes, validated order and compatible representation descriptors. Hero tests may call these kernels directly.

Do not implement version discovery, automatic comparison of every adjacent version, longitudinal audit dispatch, comparison report sections, provenance trajectories, model-performance changes, or lineage change orchestration. Those remain Phase 6A. Missing order or incompatible representations block the pairwise result; they do not suppress separately valid single-version metrics.

**Affected ownership:** T1.A/B, PR-007, PR-011; F-005/F-006/F-018. Pure formula readiness does not constitute the Phase 6A release gate.

### P3-D04. Evidence class of analytic expected contraction

**Sources:** `THEORY_SOURCE_MAP.md` TM-M02/M03 permits a `derived_metric` description and shows a derived-metric report path. `DEFINITIONS_AND_UNITS.md` section 12.5 calls the expectation a derived scenario quantity. `OBSERVABILITY_AND_REPORTING.md` sections 17.1 and 17.4 place scenario quantities under simulations. Traceability T1.C also distinguishes the scenario from observed change.

**Recommended resolution:** Use `simulation` as the single primary evidence class for both analytic expected contraction and sampled paths. Add a method distinction such as `analytic_expectation` versus `sampled_path`; an analytic calculation has no random realization and needs no fabricated seed. Preserve the exact equation and all closed-model assumptions. Future report destinations belong under `simulations`, not observed dataset deltas.

This is an explicit evidence-placement resolution requiring Theory Owner approval. Do not silently rewrite TM-M03 or its frozen source file.

### P3-D05. Exact-content profile needs a concrete byte rule

**Sources:** Data specification sections 4.3 and 13.5 name a separately declared profile and give `exact_utf8_v1` as an example. Definitions sections 6.10, 8 and 20 require deterministic normalization/hashing, but do not supply a complete transformation algorithm for that profile.

**Recommended resolution:** For Phase 3, define `exact_utf8_v1` as the UTF-8 encoding of the already validated text value, without additional trimming, case folding, Unicode normalization, whitespace collapsing, or line-ending rewriting. It describes exact equality at this documented decoded-text boundary. It does not claim equality of entire original CSV files or provenance.

A local-reference value requires explicitly supplied text produced by the existing safe loader; the path string must never become the hashed content. No other profile is accepted without a separately frozen rule. Keep source-file hashing and content hashing distinct.

**Affected ownership:** PR-006; T1 record-form input basis. Add Unicode, case, whitespace, LF/CRLF and path-versus-payload tests. This profile decision does not alter Phase 2 parsing behavior.

### P3-D06. Explicit missing states and optional tail rules

**Sources:** Data specification section 13.4 requires a configured missing-state ID without collision. The current `RepresentationConfig` has a missing policy but no such ID field. Definitions section 10 lists candidate tail rules but does not freeze a bottom-quantile algorithm.

**Recommended resolution:** Supply the missing-state ID as a required explicit argument to the internal representation interface when `explicit_missing_state` is requested. Do not invent a default `__MISSING__`, mutate the canonical record, or add a serialized config key during this phase. A missing ID or collision blocks that representation.

Implement `singleton_count`, `count_at_or_below`, `frequency_at_or_below`, and an explicit user state-list selection. A count threshold is an exact nonnegative integer; frequency threshold is a finite ratio in [0,1]; zero-probability declarations are outside observed support. Rarity sorts by ascending frequency, then the already prescribed count tie-break where relevant, then ascending Unicode state ID. State-list requests must identify observed states rather than fabricating frequencies for absent labels.

Bottom-frequency-quantile selection remains an optional unimplemented mode until rounding and boundary-tie semantics are separately approved. Requesting it must fail clearly. Weighted tail membership and near-duplicate methods are likewise not selected for this phase. No optional omission may be described as an implemented feature. [UD-012/020/021]

### P3-D07. Numerical and random-generator contract

**Sources:** Definitions sections 1, 12 and 19; validation section 9 and section 17; dependency strategy section 12.

**Recommended resolution:** Exact integer counts and finite double-precision numerical values; default scalar test tolerances `atol=1e-12`, `rtol=1e-12`; probability-mass acceptance uses the explicit absolute tolerance `1e-12`. Reject negative/nonfinite components before tolerance checks, reject empty or zero-total distributions, and do not use probability tolerance to forgive a negative component.

For a sampler, an accepted round-off residual may be corrected by division by the validated total only within this tolerance. Record the supplied total, applied correction and effective distribution. Preserve exact zero components. A material mass discrepancy is an error; arbitrary count vectors must pass through the explicit count-to-frequency calculation instead. This bounded, disclosed convention must be approved and tested before use; hidden renormalization is prohibited.

Use an explicitly created `numpy.random.Generator` with a named `PCG64` bit generator, an explicit nonnegative integer seed and no global RNG state. Boolean seeds/counts are invalid. Negative seeds are rejected, not converted. Canonical state ordering and replicate scheduling are frozen and recorded. Same implementation, generator/dependency version, parameters and seed must reproduce the path. Bit-identical paths across different NumPy versions are not promised; exact mathematical invariants remain required across supported versions.

This proposal makes the missing seed-domain and round-off conventions explicit. No fixed seed, sample size, horizon or replicate count is inferred from dataset filenames, weights or a default Hero call.

### P3-D08. Incomplete provenance cannot create stronger composition results

**Sources:** Definitions sections 3.7-3.13 and 11; data specification sections 17 and 18; accepted Phase 2 `ProvenanceAssessment` and `ProvenanceJoinResult` behavior.

**Recommended resolution:** Reuse Phase 2's exact matches and coverage. A row missing another required provenance field cannot count as known open/closed merely because its grounding cell says yes/no; it enters unresolved direct grounding with the original error retained. Valid estimated provenance is not automatically discounted.

For source/confidence composition, preserve the distinction between explicit `unknown`, no matched row, and a missing/invalid field in a matched row. Do not invent a new public bucket or silently normalize away missing field mass. When a matched field is unavailable and the approved category partition cannot represent it, the affected complete composition is unavailable with coverage/reasons. Other independently valid calculations may remain available. The direct bound can still account conservatively for unresolved evidence, subject to its own requirements.

Do not modify the Phase 2 grounding-field coverage formula to force it to equal direct closure classification completeness; they measure different input conditions. Tests must make that difference visible.

### P3-D09. Continuous maintenance of phase-specific gates

**Sources:** Current `check_traceability.py`, `release_check.py`, `test_no_algorithms.py`, `test_ci_workflows.py`, and the shared `test_T5_reopening.py` placeholder. Prior conversation exceptions authorized synchronized Phase 2 maintenance only.

**Recommended resolution:** Approve the common maintenance set in section 6 for every explicitly authorized Phase 3 step, limited to its exact current scope. A file's permission does not authorize every owner sharing that file. In particular, opening `metrics/resampling.py` for T1 must not activate T5, and opening `metrics/bounds.py` must not activate lineage bounds.

The old exact source hashes, restoration guard, offline input behavior, optional-dependency tests and prohibited-product checks remain. Replace stale stage assertions with equally specific current-stage assertions and a documented old-to-new test mapping. Never remove a failing safety or numerical condition merely because it obstructs implementation.

### P3-D10. Version and review completion

**Recommended resolution:** Keep `0.1.0.dev1` during intermediate work. In the final authorized step only, move both `pyproject.toml` and the literal root `__version__` to `0.1.0.dev2`. This development milestone label does not imply stable v0.1 publication. No dependency or build-backend change accompanies it.

Theory, mathematical, technical and security reviews must identify their actual roles and evidence. Governance permits role consolidation; disclose it when used. Automated checks and this plan do not create an independent human reviewer or a security certification. [S12; S13; S14]

---

## 4. Protected boundaries

### 4.1 Runtime operations that remain prohibited

No universal collapse/integrity/entropy/quality/presence/stability score; no use of `Q=I×D` or `S=P×I` as a numerical public product score; no epoch countdown; no source-independence inference from document counts; no human-versus-synthetic classifier; no calibrated production-failure probability without an approved empirical model.

No general graph construction/traversal, cycle enumeration, topological ancestry ordering, external-root tracing, lineage depth, ancestor incidence, ancestry HHI, effective roots, fractional-root allocation or lineage closure calculation. Existing Phase 2 input checks remain available without claiming these later results.

No T5 reopening, external-reference loss, automatically derived external truth distribution, intervention-data ingestion, causal-effect estimation, experiment scheduler, simulation grid or automatic scenario execution.

No report assembly, JSON/Markdown/HTML audit rendering, redaction engine, new audit CLI, top-level audit-result contract, background service, web/API server, cloud integration, database, LLM, model download, plugin, telemetry, automatic policy enforcement or network runtime access.

No mutual-information estimator, semantic-gradient or Blackwell calculation, evaluation benchmark platform, source registry, boundary-vacuum flow model, or other feature imported from adjacent supplied papers.

### 4.2 Protected paths

These remain unchanged except where an exact later exception is explicitly approved:

- All sixteen Phase 0 specification files and `PHASE_0_APPROVAL.md`.
- All Phase 1 and Phase 2 completion/audit records.
- `src/recursive_integrity_toolkit/io/` and `src/recursive_integrity_toolkit/config.py`.
- `src/recursive_integrity_toolkit/observability/levels.py` and its existing input-only semantics.
- `src/recursive_integrity_toolkit/lineage/`, `src/recursive_integrity_toolkit/reports/`, `src/recursive_integrity_toolkit/result.py`, and `src/recursive_integrity_toolkit/utils/logging.py`.
- `src/recursive_integrity_toolkit/cli.py` and `__main__.py`.
- All five existing schemas and all six `examples/hero/` files.
- `scripts/build_golden.py` and `scripts/normalize_golden.py`, which must not become report generators here.
- Existing package `__init__.py` files, except the single final version literal authorized by P3-D10.

Directory notation in this protected list means every file underneath, not a license to add new siblings. Tests may import and exercise protected implementations without modifying them.

### 4.3 No metrics inside the input pipeline

Keep `validate_bundle(...)` validation-only. Do not add an analytical dispatch function to `io/validation.py`, import metrics from loaders or the classifier, or calculate anything merely because a capability says `available`.

Phase 3 integration occurs in tests and documented internal examples that explicitly call the new calculation functions after validation. Phase 4 owns production orchestration and reporting. In-memory calculation records may carry future report-field identities; they must not instantiate the final report schema. [S15 sections 6-15]

---

## 5. Data, numerical and result contracts

### 5.1 Scope is part of every calculation

Every dataset-derived result must identify its selected dataset version(s), included record keys or auditable scope identity, analyzed count, exclusions, representation descriptor, weighting mode, method, applicable owner/formula IDs and limitations.

Do not pool different versions merely because the input bundle holds one canonical table. Single-version metrics require an explicit scope. Pairwise metrics require the separately validated pair context from P3-D03.

Representation exclusions reduce only the representation denominator. They must not shrink the provenance denominator by accident. Unavailable results use a reason and no numerical value; zero remains a real value. [S06 sections 1, 7, 19; S08 sections 9, 26]

### 5.2 Field representation

Use approved canonical rows. Missing, null, an explicitly configured missing state, and the literal string `unknown` remain distinct. Empty strings follow the existing canonical/mapping policy; the representation layer must not reinterpret every blank-looking value as missing.

`exclude` retains the record outside the representation calculation; `error` blocks the affected representation; `explicit_missing_state` uses the caller's collision-checked ID. An all-excluded scope produces an unavailable metric, not diversity zero.

Representations assign states and record coverage. Metric modules calculate frequencies/diversity. Neither layer reads files, guesses provenance or rewrites inputs.

### 5.3 Exact duplicates

Use PR-006's declared exact profile. Count duplicate records as the sum of group size minus one; count only groups of size greater than one as duplicate groups. Preserve every source record and provenance row. Group order and representative order must be deterministic. Scope defaults must not join records from different versions without an explicit request.

A content hash is a record-form identity under the profile; it establishes neither semantic equivalence nor independent origin. Groups may be verified against the same normalized bytes to avoid treating an artificial digest collision as established equality. Any additional collision representation rule must be documented before implementing it; it must not silently change state identifiers.

### 5.4 Distribution and weighting

Unweighted counts are exact nonnegative integers. Empirical frequencies use the named included-record denominator. Zero-probability declared states are outside support; zero states may remain in a scenario's declared state space so absorption can be tested.

Opt-in weighted state frequencies/diversity and source shares remain separate from unweighted outputs. Weights must be finite, nonnegative, complete for the selected weighted scope and have positive total mass. No confidence-to-weight conversion, zero filling of missing weights or automatic activation merely because `weight` exists. Weight zero does not delete a record from the unweighted audit.

A weight total is not an integer resample size. Weighted closure and weighted tail variants are not selected here. [S03 UD-021; S06 sections 9, 19; S09 PR-005]

### 5.5 Direct provenance and closure

The full selected valid-record scope is the denominator. Preserve explicit source types and confidence categories, missing matches, incomplete assessments and original diagnostics. For a valid matched provenance row, `external_grounding=yes` determines known open and `no` determines known closed. Unknown or invalid/missing required provenance enters unresolved grounding as specified in P3-D08.

Compute direct lower/upper bounds and width from one reconciling classification. An interval is not a confidence interval and has no inferred midpoint. Use the `toolkit_operationalization` label. Estimated confidence remains disclosed separately and does not silently move a valid grounding declaration to another class. [S07 section 18; S09 section 8]

### 5.6 Scenario result metadata

Analytic and sampled scenario records must state the model, closed-process assumptions, effective input distribution, representation, resample size, horizon and method. Stochastic records additionally state seed, RNG/bit-generator identity, dependency version, replicate count and scheduling convention.

Do not identify simulated time with the supplied record's `generation`, a training epoch, or a dataset release. Do not infer a scenario from a negative observed delta. Support cannot gain absent states inside the closed model, but an individual sampled diversity path need not decrease at every step; the contraction theorem is about expectation.

### 5.7 Public names and evidence classes

Use the registered metric names from definitions and traceability. Metadata/supporting records are project-owned immutable structures. No public DataFrame index becomes an identity; no public API depends on pandas object inference.

| Result family | Primary evidence class |
|---|---|
| Exact duplicate counts/groups; declared source counts | `observed_fact` |
| Support, frequency, diversity, tail membership/rank, source shares, direct bounds, explicit observed pair deltas | `derived_metric` |
| Analytic one-step extinction and expected contraction; sampled closed paths | `simulation`, subject to P3-D04 |
| Narrative risk/fragility signals | Not generated in this phase; later `proxy_signal` work |
| A blocked calculation | No value plus reason; never zero or a silently substituted formula |

Preserve Phase 2 coverage's established evidence meaning. New reason identifiers, if needed for a calculation interface, must be listed with meaning and tests in the Step 1 contract record. Do not silently extend existing enums or loosen the report schema.

---

## 6. File-permission model and continuous checks

### 6.1 Planning remains read-only

No path listed below is authorized for modification by the current request. The lists apply only after this plan and the corresponding execution step are approved.

An execution step may modify its explicit step list plus the common maintenance set below, subject to the stated purpose restrictions. Unlisted additions, renames, deletions or edits require a new exception. No wildcard permits every test, fixture or package file.

### 6.2 Common maintenance set G

The following exact files may be synchronized during each approved step, exclusively for active-stage boundaries, corresponding test wiring, traceability and recorded approvals:

```text
scripts/check_traceability.py
scripts/check_spec_consistency.py
scripts/release_check.py
tests/conftest.py
tests/integration/test_no_algorithms.py
tests/integration/test_ci_workflows.py
tests/integration/test_repository_structure.py
tests/integration/test_owner_ids.py
tests/integration/test_package_import.py
tests/integration/test_package_install.py
tests/integration/test_optional_dependency.py
tests/integration/test_no_network.py
tests/unit/test_PR016_determinism.py
.github/workflows/ci.yml
.github/workflows/security.yml
.github/workflows/golden.yml
.github/workflows/release.yml
docs/architecture.md
docs/theory_traceability.md
PHASE_3_DECISIONS.md
PHASE_3_BASELINE.json
```

The last two are proposed new milestone-control files, created in Step 1. They are not runtime input or schema files. `PHASE_3_BASELINE.json` records the immutable source/test baseline, approved stage, permitted paths and protected content identities. Do not modify its original baseline entries when advancing the active stage. `PHASE_3_DECISIONS.md` records actual decisions, review roles, current implementation contracts and gate-test migrations.

No G permission may be used to edit a numerical expectation, declare an unapproved decision approved, add a dependency, open a future module, hide a failure, or enable a new runtime command.

### 6.3 Boundary conversion requirements

Current gates explicitly reject all mathematical implementations and use the old Step 9/Step 10 diff and packaging rules. Convert them at Step 1, before any math implementation:

1. Preserve the Phase 2 accepted snapshot, all sixteen authority hashes and the exact restoration helper/tests.
2. Replace the blanket no-algorithm rule with exact current-stage function/class/import and operation-family boundaries. Do not remove the checker because metrics are now allowed.
3. Keep all newly opened module permissions narrow. T3 direct functions do not authorize lineage functions; T1 resampling functions do not authorize T5 reopening.
4. Maintain a mapping for every changed inherited test identity, distinguishing a replaced stale stage assertion from an unchanged behavioral guarantee.
5. Parameterize the active phase audit explicitly. Do not keep running the Phase 2 `no src changes` gate against Phase 3 HEAD, and do not change old accepted commits or reports.
6. Retain read-only workflow permissions, nonpersistent credentials, actual optional absence/presence jobs, bounded timeouts, LF-preserving checkout, failure propagation, raw logs and JUnit validation.
7. Intermediate delivery jobs may build/test the current development package but must not claim Phase 3 completion or manufacture final completion files. Final delivery requires the final gate.

Functions and classes are registered as they are implemented within the approved step, not all opened at the start. Before a step commit, the executable set must equal the actually approved set for completed/current work. Names alone do not prove safety: keep negative injection, runtime no-I/O and no-execution tests alongside AST inspection.

### 6.4 Dependency/import boundaries

Keep the two existing direct dependencies and the current build backend. No dependency installation during import or runtime. NumPy use is localized and explicitly authorized in applicable math modules; use a lazy import for sampled resampling so all forty module imports and the existing input-only workflow still work under the Phase 2 analytical-import blocker.

The no-dependency installed-wheel smoke remains an input-only/import check. Add a separate installed-metrics smoke with the approved numerical dependencies present. Do not weaken the former merely to pass the latter.

Runtime metrics must not import I/O loaders, report renderers, CLI, network clients, subprocess or unapproved graph/model libraries. Test and maintainer processes may build, install and archive; user data and declarative mappings must never reach those mechanisms.

---

# Part I. Execution steps

## Step 1. Freeze the Phase 3 baseline, decisions, contracts and gates

**Purpose:** Establish the approved interpretation and operational boundary before opening any metric module.

**Allowed files, in addition to G:**

```text
PHASE_3_PLAN.md
src/recursive_integrity_toolkit/models.py
src/recursive_integrity_toolkit/errors.py
tests/unit/test_phase3_contracts.py
tests/golden/phase3_math_cases.json
tests/golden/phase3_math_cases.md
```

The last three are new files. Add the approved plan byte-for-byte only after it is approved. No Phase 0 source is changed.

**Work:** Confirm the branch head and clean checkout; create a separate `phase3-metrics` branch from the accepted Phase 2 commit when execution is authorized. A merge to main is not required to start this branch. Freeze baseline file hashes and inherited test identities. Record P3-D decisions and review roles. Define only supporting contracts for representation assignments, numerical calculation records, weighting/tail options, explicit pair context and scenario metadata; no formulas yet.

Transcribe the source-derived exact/rational mathematical cases in section 8 into the small golden manifest with source sections, owners and tolerances. Expectations must come from the approved sources or a separately reviewed derivation, not by running the future implementation to manufacture its own answer.

Convert active-phase gate and workflow assumptions using section 6. Preserve the historical restoration test behavior and all accepted input behaviors.

**Tests:** Complete Phase 2 regression with and without real PyArrow; contract/type tests; source/hash audit; safe imports; all forbidden future modules still docstring-only; wrong-baseline, unauthorized-path and forged-stage negative cases.

**Acceptance:** Every applicable baseline guarantee passes. All required P3-D decisions are explicitly recorded. No metric is implemented. CI works on the new branch, including build evidence without a false completion claim.

**Stop:** Missing or qualified approval of a necessary decision, a changed baseline, or any failed inherited guarantee blocks continuation. Stop after the Step 1 report for approval.

## Step 2. Field representations and missing-state handling

**Allowed files, in addition to G:**

```text
src/recursive_integrity_toolkit/representations/base.py
src/recursive_integrity_toolkit/representations/field.py
src/recursive_integrity_toolkit/models.py
src/recursive_integrity_toolkit/errors.py
tests/unit/test_T1_representation.py
tests/fixtures/minimal_valid/phase3_field_records.jsonl
tests/fixtures/invalid_schema/phase3_representation_cases.json
docs/data_schema.md
```

The test and two fixture files are new.

**Work:** Create the representation protocol and pure topic/label assignment. Preserve exact state spelling, identity and declared taxonomy/version. Implement explicit selection/fallback audit metadata and the three missing policies using P3-D06. Return assignments, exclusions, selected count and named coverage without calculating diversity or tail values.

**Tests:** Topic versus label selection; explicit-config precedence; unsupported source; missing field; null versus literal `unknown`; empty string policy; case/Unicode distinctions; all-excluded scope; missing-state collision; no raw-record mutation; row permutation; no I/O/network/callbacks. Preserve the existing Phase 2 capability tests without changing their expected input-only behavior.

**Acceptance:** Every included record has exactly one explicit state, and included/excluded counts reconcile. Unknown or missing values never become fabricated semantic evidence. No metric or hash implementation occurs yet.

**Stop:** A desired representation requires embeddings, arbitrary callbacks, an undeclared config field, or an unapproved state-normalization rule. Stop after acceptance.

## Step 3. Exact record-form representation and duplicates

**Allowed files, in addition to G:**

```text
src/recursive_integrity_toolkit/representations/content_hash.py
src/recursive_integrity_toolkit/metrics/duplicates.py
src/recursive_integrity_toolkit/models.py
src/recursive_integrity_toolkit/errors.py
tests/unit/test_PR006_duplicates.py
tests/unit/test_T1_representation.py
tests/fixtures/minimal_valid/phase3_exact_content.jsonl
docs/data_schema.md
docs/privacy.md
```

The fixture is new. Reuse the existing byte-hash helper without modifying it.

**Work:** Implement only the approved `exact_utf8_v1` profile, stable record-form states, duplicate groups and the two registered duplicate counts. Inputs are validated text or explicitly provided safely loaded text. Do not open a file from this layer.

**Tests:** Same text/equal digest; case and whitespace differences; composed/decomposed Unicode; LF versus CRLF at the documented boundary; unsupported profile; local path without payload; independent copies; group-size-minus-one definition; deterministic group/member ordering; unchanged rows/provenance; no near-duplicate method; no content/notes logging. Replace the existing PR-006 placeholder assertion with its implemented boundary checks.

**Acceptance:** Exact counts match hand cases, duplicate grouping never deletes inputs, and record-form support is never labeled semantic support.

**Stop:** An undocumented profile transform, semantic similarity method, content read, or cross-version pooling is required. Stop after acceptance.

## Step 4. Frequencies, support and diversity

**Allowed files, in addition to G:**

```text
src/recursive_integrity_toolkit/metrics/diversity.py
src/recursive_integrity_toolkit/models.py
src/recursive_integrity_toolkit/errors.py
tests/unit/test_T1_support.py
tests/unit/test_T1_diversity.py
tests/unit/test_phase3_contracts.py
tests/fixtures/weighted/phase3_distribution_cases.json
```

The weighted fixture is new.

**Work:** Implement F-001 through F-004 for explicit single scopes. Separate state counts, empirical frequencies, positive-mass support, Gini-Simpson diversity and Simpson concentration. Add explicit weighted frequency/diversity variants alongside unchanged unweighted results. Introduce no pairwise comparison in this step.

**Tests:** All approved F001-F003 cases; nonempty positive denominators; zero-probability support exclusion; negative/fractional/boolean counts; nonfinite or malformed distributions; one state; equal states; permutation invariance; duplication of all records leaves frequencies/diversity unchanged; weight opt-in; zero-weight behavior; incomplete/negative/all-zero weights; family-specific denominators.

Both T1 support and diversity unit files share the same implementation module and must migrate their placeholder checks in this step.

**Acceptance:** Exact integer invariants and tolerance-based numerical cases pass. No simulated model is needed to compute an observed dataset diversity. Representation and weighting metadata survive every result.

**Stop:** A calculation lacks a declared scope/representation, needs implicit probability repair beyond P3-D07, or is being presented as functional failure. Stop after acceptance.

## Step 5. Source and confidence composition; direct grounding basis

**Allowed files, in addition to G:**

```text
src/recursive_integrity_toolkit/metrics/provenance.py
src/recursive_integrity_toolkit/models.py
src/recursive_integrity_toolkit/errors.py
tests/unit/test_PR004_coverage.py
tests/unit/test_PR005_source_shares.py
tests/unit/test_T3_provenance.py
tests/fixtures/provenance_partial/phase3_composition.json
tests/fixtures/provenance_unknown/phase3_grounding_crossed.json
tests/fixtures/weighted/phase3_source_weights.json
```

The three fixtures are new. All three unit files sharing `metrics/provenance.py` may update stale placeholder checks; their Phase 2 validation tests remain intact.

**Work:** Consume validated matches and explicit scope. Compute source counts/shares, separate confidence composition, and the direct known-open/known-closed/unresolved basis. Preserve Phase 2 row, required-field and grounding-field coverage without reimplementing joins. Add only the approved explicit weighted source-share variant.

**Tests:** Complete and partial provenance; unknown versus missing row; incomplete required field; invalid present field; full crossed source/grounding matrix; human review independence; estimated confidence preserved; denominator reconciliation; source shares independent of representation exclusions; weights not used by default; weighted/unweighted outputs distinct; no source-independence or closure inference from source class.

**Acceptance:** The classification partition reconciles to the selected record count. Complete composition either uses an exhaustive approved partition or is explicitly unavailable as P3-D08 requires. No closure interval is computed yet.

**Stop:** An incomplete matched field would require an invented bucket, unknown reassignment, source inference, confidence discount, or a Phase 2 semantic change. Stop after acceptance.

## Step 6. Direct closure-exposure bounds

**Allowed files, in addition to G:**

```text
src/recursive_integrity_toolkit/metrics/bounds.py
src/recursive_integrity_toolkit/models.py
src/recursive_integrity_toolkit/errors.py
tests/unit/test_T3_bounds.py
tests/unit/test_T3_provenance.py
tests/fixtures/provenance_unknown/phase3_direct_bounds.json
```

The fixture is new.

**Work:** Implement only the direct interval using known-closed, unresolved and total counts from Step 5. Return lower bound, upper bound, width, denominator, classification basis, confidence disclosure and the operationalization label. Do not import or traverse parents.

**Tests:** N=8, C=3, U=2 gives [3/8, 5/8] and width 1/4; all open; all closed; all unknown; missing row; incomplete row; zero/invalid totals; invalid partitions; lower <= upper; width=U/N. Masking an open/closed classification to unresolved must not narrow the interval. Restore stronger evidence only from valid declarations, never inference.

A pure count-kernel test may evaluate the all-unresolved [0,1] envelope. Dataset-facing invocation still preserves capability and valid-provenance requirements; absence of all usable provenance cannot be promoted into a successful provenance audit.

**Acceptance:** Intervals remain intervals with their real uncertainty and provenance limitations. No lineage value, midpoint, risk threshold or universal score exists.

**Stop:** Computing a proposed value needs roots, ancestors, lineage closure classes or empirical truth verification. Stop after acceptance.

## Step 7. Tail selection, rarity and analytic extinction

**Allowed files, in addition to G:**

```text
src/recursive_integrity_toolkit/metrics/tail.py
src/recursive_integrity_toolkit/models.py
src/recursive_integrity_toolkit/errors.py
tests/unit/test_T2_tail.py
tests/unit/test_phase3_contracts.py
tests/fixtures/minimal_valid/phase3_tail_cases.json
```

The fixture is new.

**Work:** Implement the selected explicit rules from P3-D06, tail membership, tail support size, tail record share and deterministic rarity ranking. Implement F-014 for a supplied state frequency and positive integer resample size, with the simulation evidence class and one-step closed-model assumptions. No random sampling yet.

**Tests:** Threshold inclusion/exclusion and boundary values; singleton Hero tail; no selected states; deterministic frequency ties; absent user-list state; unsupported quantile; missing representation; all exact F014 cases; p=0 and p=1; invalid frequency/size; monotonicity in frequency and sample size; no universal alert severity. Compare exact rational expectations, not source prose rounded to ten decimals.

**Acceptance:** Tail membership/rank is a derived metric; extinction probability remains simulation; a fragility narrative is not generated. The default validation workflow does not execute the probability calculation.

**Stop:** A threshold is inferred, a missing quantile rule is invented, or a scenario number is presented as production failure probability. Stop after acceptance.

## Step 8. Expected contraction and explicit closed-resampling kernels

**Allowed files, in addition to G:**

```text
src/recursive_integrity_toolkit/metrics/resampling.py
src/recursive_integrity_toolkit/models.py
src/recursive_integrity_toolkit/errors.py
tests/unit/test_T1_resampling.py
tests/unit/test_T5_reopening.py
tests/unit/test_phase3_contracts.py
tests/fixtures/resampling/phase3_closed_cases.json
```

The fixture is new. The T5 unit file is included only to replace its shared-module-empty assertion with an equally strict prohibition of reopening behavior.

**Work:** Implement F-015 one-step and fixed-size multi-step expectations, and the explicit closed categorical sampler required by P3-D02. Validate size, horizon, replicates, seed, probability vector and declared state space. Use the P3-D07 generator and ordering convention. Keep analytic expectation separate from a sampled path; keep each replicate distinguishable.

No external q/r/lambda input, reopening branch, grid search, automatic experiment selection or run-level simulation dispatcher is introduced. Bounded work/memory validation must occur before allocating requested paths. An unsupported resource request fails clearly rather than silently truncating the horizon, states or replicates.

**Tests:** All F015 cases; horizon zero; n=1; one-state distribution; zero-state absorption; integer sample totals; frequencies in multiples of 1/n; same-seed same-environment repeatability; global RNG untouched; explicit seed used; arbitrary different seeds need not produce different outcomes; analytic expectation checked by small exact enumeration and Monte Carlo sanity checks; reported numerical correction is bounded and preserves zero support.

**Acceptance:** The source model assumptions, RNG/method versions, parameters and limitations accompany all scenario outputs. All imports and the original input-only installed smoke still pass with numerical dependencies blocked. Separate installed calculation tests run with NumPy present. T5 remains unimplemented.

**Stop:** A result requires external reopening/loss, graph behavior, nondisclosed random state, hidden parameter defaults or probability repair outside the approved rule. Stop after acceptance.

## Step 9. Explicit representation compatibility and pairwise mathematical comparisons

**Allowed files, in addition to G:**

```text
src/recursive_integrity_toolkit/representations/compatibility.py
src/recursive_integrity_toolkit/representations/field.py
src/recursive_integrity_toolkit/metrics/diversity.py
src/recursive_integrity_toolkit/models.py
src/recursive_integrity_toolkit/errors.py
tests/unit/test_T1_support.py
tests/unit/test_T1_diversity.py
tests/unit/test_T1_representation.py
tests/unit/test_T1_compatibility.py
tests/fixtures/representation_compatible/phase3_pair.json
tests/fixtures/representation_incompatible/phase3_pair.json
```

The compatibility test and two fixtures are new.

**Work:** Implement P3-D03's explicit pair context. Compare representation name, version, rule, missing policy and state meaning declarations. Use accepted version-order validation; do not infer chronology. Calculate support delta, loss/added sets, retention and diversity delta only for the explicitly supplied eligible pair.

A many-to-one map requires a declared source representation, target representation, mapping direction and exact literal dictionary. Record its effect on the comparison basis; no one-to-many allocation, automatic map inference or equivalence claim based on two version strings. A bare global `state_mapping` declaration without sufficient context is not executed speculatively.

**Tests:** Approved Hero pair values; same support with changed frequencies; equal-sized but different supports; added and lost states simultaneously; zero earlier denominator; reversed order; absent chronology; incompatible version/rule; mapping collisions and ambiguous direction; explicitly declared many-to-one map; rejection of one-to-many; unchanged original assignments.

**Acceptance:** The pure comparison records identify both scopes and the harmonized representation. No longitudinal dispatcher, trajectory, model-performance result or lineage delta exists. Existing `dataset_longitudinal` input eligibility is not treated as proof that every comparison is now implemented.

**Stop:** Pair selection or state semantics must be guessed, or implementation starts iterating automatically over bundle versions. Stop after acceptance.

## Step 10. Mathematical integration, reviewed goldens and performance evidence

**Allowed files, in addition to G:**

```text
tests/integration/test_phase3_metric_pipeline.py
tests/golden/test_phase3_math.py
tests/golden/phase3_math_cases.json
tests/golden/phase3_math_cases.md
tests/performance/test_hero_runtime.py
tests/performance/test_metadata_100k.py
```

The integration and golden test runners are new. No package implementation is opened by this step. A newly found implementation defect returns to its owning approved step or requires an explicit repair authorization.

**Work:** Exercise Phase 2 loading/mapping/validation followed by explicit representation and metric calls in a test-only composition. Validate the in-scope mathematical Hero values from section 8. Independently demonstrate that a plain `validate_bundle(...)` invocation still executes no metric or simulation.

Create no `hero_report.json`, `hero_report.md`, lineage report or cycle report. The Phase 3 golden manifest is a calculation test oracle, not the public report schema. Changes to the prewritten expected values require an identified source correction or separately reviewed derivation and explicit approval; the implementation never rewrites its own expectations.

Measure single-version support/diversity/composition and exact duplicates on a synthetic 100,000-record case, plus the current Hero input-plus-calculation path. Record environment, elapsed time and memory method. These measurements do not certify the complete under-five-second report target, whose JSON/Markdown stages do not yet exist. Do not activate sparse-lineage performance tests.

**Tests:** Full mathematical integration; all source hashes; no source mutation; error-bearing partial inputs do not yield silently successful calculations; representation exclusion versus provenance denominator; explicit scenario opt-in; no raw content in diagnostic output; no imports/calls into protected later layers; no hidden quadratic duplicate pass.

**Acceptance:** Every in-scope Hero number has an independently traceable expected value. Mathematical and safety regressions pass; performance observations are recorded without unsupported whole-product claims. No public analytical report is created.

**Stop:** A golden discrepancy is unresolved, an expected value would be changed merely to match code, or a protected later feature is required for the integration. Stop after acceptance.

## Step 11. Final documentation, complete CI, build, installation and delivery

**Allowed files, in addition to G:**

```text
README.md
CHANGELOG.md
docs/data_schema.md
docs/privacy.md
docs/release_process.md
pyproject.toml
src/recursive_integrity_toolkit/__init__.py
tests/integration/test_cli_validation.py
tests/integration/test_license_notices.py
tests/integration/test_prohibited_structure.py
PHASE_3_COMPLETION.md
PHASE_3_VALIDATION_REPORT.md
PHASE_3_ARCHITECTURE_COMPLIANCE_REPORT.md
```

The three Phase 3 milestone reports are new. The package/root metadata edits are limited to the version change in P3-D10; CLI test changes may only synchronize literal version expectations. No new command or dependency is authorized.

**Work:** Finish implemented-versus-deferred documentation and per-field traceability. Retain the accepted Phase 2 records untouched. Execute every final gate in section 10, including real PyArrow, minimum direct-dependency environments, current compatible environments, fresh installed-wheel input and metric checks, both distribution formats and source archive verification.

Keep all four workflow roles: complete CI, security, Hero/mathematical goldens, and build/delivery. The golden workflow may run the approved calculation-oracle tests and Hero structure tests; it may not create report goldens. Workflows never publish to a package registry, create a tag or merge a branch.

Prepare final records only from actual results. If documentation finalization changes the commit, rerun the required workflows on that exact final commit and regenerate its delivery artifact. Distinguish implementation-acceptance and documentation-only commit IDs to avoid a circular self-hash assertion.

**Acceptance:** All required gates pass on the final source commit, all required reviews are recorded, archive/distribution contents match that source, and retained limitations are explicit. Report actual tests, versions, commands, exit codes, failures and repairs. No final count is predicted by this plan.

**Stop:** Produce the final deliverables and stop. Main merge, stable v0.1 publication, Phase 4, Phase 5, Phase 6A and Phase 6B require separate authorization.

---

# Part II. Mathematical acceptance and test requirements

## 7. Test policy

Every implemented family requires valid, invalid, missing/unavailable, boundary and deterministic-order cases where applicable. Each numerical test identifies its owner, formula, exact input, expected value/derivation, denominator, tolerance and assumptions. Tests use synthetic fixtures and no private production data. [S10 sections 9, 64-70]

Retain the entire applicable inherited suite. A total count alone does not establish regression preservation: compare collected node identities against the frozen baseline and explain every stage-assertion migration. No active test may be hidden by skip, xfail, a narrowed full-suite selector, swallowed errors or `continue-on-error`. Unimplemented later-phase features retain explicit prohibition/placeholder tests, not pretend behavioral success.

Use independent test oracles: rational arithmetic or hand derivation for small exact cases, independent enumeration for small stochastic cases, then statistical sanity checks. Do not use one implementation function to generate the expected output of another supposedly independent correctness test.

### 7.1 Required mathematical families

| Family | Minimum required coverage |
|---|---|
| Representation | Explicit field/profile, stable IDs, every missing policy, collision, fallback disclosure, unsupported mode, no semantic inference |
| Duplicate | Group and extra-record counts, scope isolation, byte/profile distinctions, no record deletion |
| Distribution | Exact count denominator, positive support, finite probability validation, Gini-Simpson range/invariants |
| Weights | Explicit opt-in, complete finite nonnegative values, positive mass, preserved unweighted output |
| Composition | All five source categories, missing rows, missing matched fields, separate confidence and grounding, unweighted denominator |
| Direct bounds | Exhaustive basis, width identity, uncertainty monotonicity, no midpoint or lineage substitution |
| Tail | Chosen rules and thresholds, deterministic ties, empty tail, no fabricated absent states |
| Analytic scenarios | Boundary p values, positive n, one-step meaning, expected versus observed separation |
| Closed sampler | Seed use, generator isolation, mass/count conservation, absorption, horizon zero, n=1, replicate identity |
| Explicit pair | Scope order, compatibility, support intersection/loss/addition, diversity delta, missing denominator |
| Boundary | Future modules/owners blocked, metrics do not read files or call network, no automatic simulation/report |

### 7.2 Fixed-seed and statistical tests

For conditional unbiasedness, retain the approved recommended distribution [0.5, 0.3, 0.2], resample size 100 and 50,000 independent replicates, with a fixed recorded seed. Freeze component tolerances before observing output, using the standard error sqrt(p_i(1-p_i)/(nR)) and a documented simultaneous margin. A failed run must not be repaired by choosing a more favorable seed.

Use deterministic enumeration for selected small multinomial spaces to verify conditional means, F-015 and F-014 independently of the sampler. Statistical tolerance for sample means must not be confused with `1e-12` deterministic formula tolerance. Repeated paths within the same recorded environment must match exactly; different dependency-version environments validate their own repeatability and the same mathematical properties. [S10 sections 9, 17; P3-D07]

### 7.3 No unsafe strengthening through a higher capability level

Test direct calculation prerequisites, retained validation errors and actual representation coverage rather than trusting `maximum_level` alone. A Level 4 input bundle with an invalid explicit state mapping must not produce a valid pairwise metric. A valid single-version distribution may remain calculable when lineage is unavailable. A sampled scenario does not improve the input evidence about the real pipeline.

---

## 8. Source-derived hand cases and Hero targets

These values are transcribed from approved validation sections 10-19 and the unchanged Hero contract. They are targets for future tests, not calculations executed in this planning task.

### 8.1 Core exact cases

| Case | Input | Exact expected value |
|---|---|---|
| F001-A | Counts a=2, b=1, c=1 | N=4; frequencies 1/2, 1/4, 1/4 |
| F002-A | p=(1/2, 1/2, 0) | Support size 2 |
| F003-A | p=(1) | D=0 |
| F003-B | p=(1/2, 1/2) | D=1/2 |
| F003-C | Four equal states | D=3/4 |
| F003-D | p=(1/2, 1/4, 1/4) | D=5/8 |
| Direct interval | N=8, known closed=3, unresolved=2 | Lower=3/8; upper=5/8; width=1/4 |
| F014-C | p=1/2, n=2 | 1/4 |
| F014-D | p=1/4, n=4 | 81/256 |
| F015-A | D=1/2, n=2 | Expected next D=1/4 |
| F015-B | D=3/4, n=4 | Expected next D=9/16 |
| F015 multi-step | D0=3/4, n=4, t=2 | Expected D2=27/64 |

Additional edge and metamorphic cases are proposed validation design and must be labeled as such in the oracle notes. They are not attributed to a source that does not contain them.

### 8.2 In-scope Hero calculation targets

| Quantity | Expected |
|---|---|
| Topic representation/version | `topic` / `hero-topic-v1` |
| Per-version record counts | v1=8; v2=8 |
| v1 support/diversity | 8; 7/8 |
| v2 counts | cat=3, dog=2, bird=1, fish=1, refund=1 |
| v2 support/diversity | 5; 3/4 |
| Explicit pair support delta/retention | -3; 5/8 |
| Explicit pair diversity delta | -1/8 |
| Explicit pair lost states | `battery`, `lizard`, `turtle`, in that stable order |
| Explicit pair added states | Empty set |
| v2 source shares | human=1/2; synthetic=1/2; mixed/sensor/unknown/missing-provenance=0 |
| v2 accepted validation coverage | All three coverage measures remain 1 |
| v2 direct closure interval | [1/2, 1/2]; width 0 |
| Default Hero validation | Level 4; model longitudinal unavailable; no simulation executed |

The pair targets depend on approval of P3-D03. They do not assert completion of the Phase 6A longitudinal workflow.

### 8.3 Separately invoked Hero mathematical scenarios

The unchanged default Hero config does not enable simulations. The following are separate test invocations with explicit n=8:

| Scenario | Exact expected value |
|---|---|
| Singleton state extinction, p=1/8 | 5,764,801 / 16,777,216 |
| Dog extinction, p=1/4 | 6,561 / 65,536 |
| Cat extinction, p=3/8 | 390,625 / 16,777,216 |
| Expected next diversity from v1 | 49/64 |
| Expected next diversity from v2 | 21/32 |

Use the rational values as expected results rather than rounded printed approximations. No observed v1-to-v2 transition is asserted to have been generated by this model.

### 8.4 Hero expectations intentionally not calculated

Retain the source contract but leave these for their owning phases: general cycle status, external-root count, top shared ancestor, ancestor incidence, ancestry HHI, effective roots, lineage closure bounds, shared-ancestry proxy signals, final report sections, and all model-performance/causal/universal-integrity claims.

Do not set those unimplemented results to the known golden constants. Do not count their preserved static text as a passing implementation test. [S09 sections 41-42; S10 sections 20-24; Hero contract]

---

## 9. File-specific regression and safety requirements

1. Preserve every active Phase 2 loader, mapper, canonical validator, provenance join, chronology, generation, local-reference, classifier and bundle regression. Preserve real-PyArrow collection and success in the extra-enabled job.
2. Keep all sixteen approved hashes and the restored validation plan immutable. Keep the eight digest-bounded restoration tests. A new phase-control file does not authorize editing the original approval manifest.
3. For each newly opened metric module, inject prohibited extra definitions and forbidden I/O/network/graph/report behavior into temporary copies; the gate must reject them. A shared module's deferred owner needs its own negative cases.
4. Block raw file access, network calls, environment lookups, dynamic imports of user code, eval/exec, subprocess and callbacks during explicit representation/metric calls. The existing approved loader remains the only content-reading route used by the test caller.
5. Keep errors/content traces safe. Full record text, notes and private filesystem paths must not appear in routine calculation exceptions or diagnostic representations. Hashes are not claimed to be anonymization.
6. Run all module imports with network and analytical/optional import blockers. Then run numerical invocation tests with the approved numerical dependencies present and network blocked. Report these as distinct guarantees.
7. Ensure ordinary input validation leaves metric modules uninvoked, even when configuration contains an enabled simulation declaration or a capability is available. This is checked by fail-on-call stubs in tests, not by merely inspecting output fields.

---

# Part III. Final acceptance, stopping and delivery

## 10. Required final gate

Phase 3 is technically complete only when all applicable items below pass and required reviews are recorded.

| Gate | Required evidence |
|---|---|
| Scope | Every change lies in the approved completed-step union; no unapproved file or owner |
| Authority | All 16 approved Phase 0 hashes and prior milestone records preserved |
| Core correctness | Complete active suite, zero failed/errored/skipped cases; test-identity migration reconciled |
| Real optional input | Complete suite with real PyArrow, all three original real-Parquet cases present and passed |
| Platform matrix | Ubuntu/Windows with Python 3.11/3.12 all pass |
| Dependency coverage | Existing minimum direct dependency versions and a recorded current compatible set tested; no new direct dependency |
| Mathematical correctness | Exact/rational cases, reviewed goldens, boundary/property cases and declared Monte Carlo checks |
| Traceability | Every new numeric field maps to definition, owner, formula or product rule, tests, units, evidence class and limitation |
| Security | No network or execution path; existing mapping/content-reference boundaries pass; protected-owner negative cases pass |
| Hero | Explicit in-scope calculations match the unchanged contract; input-only Hero still performs no calculation |
| Imports | All 40 modules import safely; no import-time file/network/RNG execution |
| Build | Wheel and sdist built from the final commit and pass strict metadata checks |
| Installed behavior | Fresh wheel import/input smoke plus separate installed math smoke run outside the checkout; packaged modules match source |
| Archive | One-root tracked-source ZIP; no cache/private input/venv; archived bytes verified against final commit |
| Documentation | Actual command, failure, repair, limit, review-role and artifact records; no fictional execution evidence |
| Later phases | Reports/CLI, T4/T6, lineage bounds, full longitudinal workflow and T5/Phase 6B experiment orchestration remain excluded |

Commands in the eventual execution report must be the actual commands used. Planned examples include full pytest invocations for core and real-Parquet environments, the three existing audit scripts in their approved Phase 3 modes, isolated package builds, strict Twine checks and installed-wheel smoke checks. This plan has not run those future commands.

Counts from operating systems, repeat runs, optional jobs and subsets must not be summed as distinct tests. The final count is measured, not precommitted. A green targeted subset cannot replace full regression.

The full product's report-time performance and empirical usefulness gates remain in their assigned later stages. Do not claim production readiness, independent security certification, proof of provenance truth or stable v0.1 completion from this mathematical milestone.

## 11. Step reports and stop rules

Every step report must state its base/head commit, modified/added files, exact implemented owners and functions, commands with exit codes, test counts, failures and repairs, protected-path audit, dependency/import results, and the next unstarted step. Retain original failure evidence.

Use one of:

```text
TASK COMPLETE, PHASE CONTINUES
BLOCKED BY DECISION
FAILED ACCEPTANCE GATE
```

Stop immediately for an unapproved P3-D decision, source contradiction, undefined operational rule, unlisted file edit, missing numeric traceability, unsafe input behavior, unknown-value inference, unsupported numerator/denominator, hidden probability repair, unexplained golden change, failing inherited test, unavailable full verification, or a need to implement a protected later owner.

Do not force-push, overwrite concurrent work, merge main, publish packages, change authority hashes, update a theoretical claim through a code comment, or use a skipped/xfail test to claim an active requirement passed. Remote write/CI unavailability leaves a candidate pending; it does not create successful execution evidence.

A confirmed in-scope bug may be repaired within its current authorized file list. A defect in a protected prior-phase module requires a precise repair proposal and approval, rather than opportunistic refactoring.

After each successful step, stop for the user's approval. Final phase acceptance is separate from authorizing the next phase.

## 12. Phase 3 deliverables

### 12.1 Repository contents

The completed milestone will contain the selected field/record-form representations, exact duplicates, single-scope distributions/diversity, source/confidence composition, direct bounds, tail/extinction calculations, expected contraction and explicit closed sampler, and the approved pure pairwise kernels. It will include their tests, synthetic fixtures, mathematical oracle, active-stage gate records and synchronized documentation.

The existing forty-module package layout remains. Opening the four representation implementation files and six metric files leaves sixteen other modules as placeholders when no additional module is authorized. The checker must verify actual names and contents, not trust this arithmetic as proof.

### 12.2 Completion records

```text
PHASE_3_COMPLETION.md
PHASE_3_VALIDATION_REPORT.md
PHASE_3_ARCHITECTURE_COMPLIANCE_REPORT.md
```

Record implemented and deferred owners, formula coverage, adopted P3-D decisions, actual reviewer roles, regression migration, true final counts, dependency environments, mathematical and stochastic validation, scope/security evidence, performance observations, build/install results, final commits, artifacts, deviations and remaining limits.

Only mark `PHASE COMPLETE` when the final gate passes. Prior failed candidates and unperformed checks remain distinguishable from successful runs.

### 12.3 Distribution and source artifacts

Subject to P3-D10:

```text
recursive_integrity_toolkit-0.1.0.dev2-py3-none-any.whl
recursive_integrity_toolkit-0.1.0.dev2.tar.gz
recursive-integrity-toolkit-phase3.zip
```

The repository ZIP must have exactly one `recursive-integrity-toolkit/` root and contain the full tested tracked tree. The wheel and sdist have their documented package-distribution scope; they are not substitutes for the full source archive. No registry publication, tag creation or main merge is performed.

### 12.4 Execution evidence

Retain raw command logs, core/Parquet/security/Hero/mathematical JUnit where separated, baseline/current file hashes, golden fixture identities, environment and RNG metadata, installed-wheel results, performance observations, and SHA-256 manifests. Suggested names include:

```text
phase3_test_results.log
phase3_build_results.log
phase3_security_results.log
phase3_math_validation.log
phase3_execution_metadata.json
phase3_repository_files.sha256
phase3_artifacts.sha256
```

Actual artifact names and downloadable locations must be reported only after generation and verification. If hosted retention is finite, record its actual expiry. Never present a local evidence summary as the full built repository or package.

## 13. Approval record and handoff

The decision requested is approval of this bounded Phase 3 plan, including P3-D01 through P3-D10, the continuous gate-maintenance scope, and the per-step file lists. The plan can instead be approved with named exceptions, in which case dependent steps stay blocked.

| Decision field | Current state |
|---|---|
| Phase 2 final delivery | Accepted by the Theory Owner in the current conversation |
| Phase 3 plan | Pending |
| P3-D01 through P3-D10 | Pending |
| Theory/numerical/security review roles for implementation | Must be recorded before their affected work; no invented sign-offs |
| First implementation step | Not started; requires explicit instruction after plan approval |
| Main merge | Not authorized |
| Later-phase implementation or publication | Not authorized |

Final Phase 3 handoff must distinguish the implemented mathematical core from the still-deferred full product: representation-bound numbers and closed-model scenarios are available under declared assumptions; complete report/CLI integration, full lineage, longitudinal orchestration and external-reopening experiments retain their separate gates.

**Planning stop:** `PHASE_3_PLAN.md` generated. No repository file modified. No implementation written. No main merge. Await Theory Owner approval.

---

# Appendix A. Immutable source inventory

The following values are from the approval manifest at the pinned Phase 2 baseline. Retain them as source identity, not as editable expectations for future implementation.

| ID | Approved Phase 0 file | SHA-256 |
|---|---|---|
| S01 | `SPEC_AUDIT.md` | `f846cc56524beefaaf9e53a08d7e881cc9782b879e22f2d517928f2179e9c99a` |
| S02 | `THEORY_SOURCE_MAP.md` | `9a16cfa67838ae4cbbf3ccaef21dc0cbbbeeaff952c20f67ec6b71c420bb9d04` |
| S03 | `UNRESOLVED_DECISIONS.md` | `6078dbb85da80bf406f4a995fc84549484b202e4e49ddefd7249ed2c8cdd8490` |
| S04 | `PROJECT_INSTRUCTIONS.md` | `19137a3fd3cecb221ea02e2375239a5b20ceb27808dadc589cf693579debf84c` |
| S05 | `V0.1_PRODUCT_SPEC.md` | `8c89076a7f982221d07ab030709aed410250a2417ca2b01a62c4bbe4c97c60ae` |
| S06 | `DEFINITIONS_AND_UNITS.md` | `2a52c45cc6f0c00d9565ddc70c63232fe11585f7ceba9d7ff58f925c2e37b048` |
| S07 | `DATA_AND_PROVENANCE_SPEC.md` | `b48971c7742130eb5aca08dd87d15d801c1a144647ed39d3519535dd52e2280a` |
| S08 | `OBSERVABILITY_AND_REPORTING.md` | `3599f478894dcab89867849243e837a2995fcfb733d5585d778ed72d6dbae3f2` |
| S09 | `THEORY_TO_CODE_TRACEABILITY.md` | `c5ecfcd1919eea7cb2591689e2a29d0497db4351b0c057b9adc67ddbb57df54c` |
| S10 | `VALIDATION_PLAN.md` | `16f5fe539da2b3cff1c3e0a2854208bd7fbc1e4c5b332684265b06a03a90cf2f` |
| S11 | `PRIVACY_AND_DATA_HANDLING.md` | `5701441fe126e4539d51bfe0c550e88c65920920b0f52246b186fe1d159656a5` |
| S12 | `LICENSING_NOTES.md` | `2dcf3ff967c258695622c0321a4310d361f4252ec8bab41df0c108fe6b71ed33` |
| S13 | `SUCCESS_CRITERIA.md` | `498536bf891f8add998cc0390a4691c75c71a3460cd93600612d3c7ae2ca70de` |
| S14 | `GOVERNANCE_AND_HANDOFF.md` | `1c0fe93eab01deb0b3481215d3ff6555a300552eac41a6313b34357e6c3b2e45` |
| S15 | `REPOSITORY_ARCHITECTURE.md` | `d4d9c1ff657934cf2a70d1c2038dd8a5f8c519271695b0cc395d833fac06a0e4` |
| S16 | `DEPENDENCY_STRATEGY.md` | `38bf20a176fb04efe882c37ec6188e5886e653c8340915892523d8bec56c8dce` |

# Appendix B. Source locators and review trail

All repository references below are pinned to `78554993febb01609cb90814cc24cce2012bf7d7` unless explicitly historical.

| Source | Sections used and role |
|---|---|
| S01 | 3-7, B08-B14, N01/N02/N05/N09/N10: authority, exact core, operationalization and scope boundaries |
| S02 | TM-M01 through TM-M07, TM-P01 through TM-P05, TM-E01 through TM-E05, sections 10-14: theory/field trace and deferred claims |
| S03 | Blanket approval; UD-007 through UD-025, UD-027 through UD-036 as applicable: order, grounding, representation, tails, weights, licensing, phase split and non-goals |
| S04 | 4-12: dual authority, exact-contract order, phase allocation, theory/evidence/data/representation constraints |
| S05 | 6-17, 20-29: target functions, optional inputs, limits, Hero and phase mapping |
| S06 | 1, 3, 5-13, 19-20, 23-26: canonical meanings, formulas, units, weights and normalization |
| S07 | 4, 13, 17-18, 21-23, 26, 31: representation inputs, missing policy, grounding, internal forms and Hero |
| S08 | 2-3, 9, 15-17, 25-27, 28, 32-36: evidence classes, scenario placement, names, reporting boundaries and gates |
| S09 | 6-11, 15-17, 27, 30-50: owner APIs/fields, code header rules, mathematical tests and phase traceability |
| S10 | 9-26, 33, 38-39, 48-50, 54-60, 61-70, 79-96: independent math cases, security, performance, review and release gates |
| S11 | 1-3, 15-18 and field handling rules: local-only behavior, no hidden persistence, safe diagnostics, trusted filesystem limits |
| S12 | Asset split and code/specification/fixture/theory-reference rules: preserve existing licenses and reference-only theory assets |
| S13 | 4-9, 11, 13-19: correctness, usefulness, reproducibility, phase success and limits of milestone claims |
| S14 | 2-7, 10-15, 25-29: review roles, conflicts, changes, releases, metrics and repository authority |
| S15 | 5-15 and canonical tree: package ownership, representation/metric/lineage separation and dependency direction |
| S16 | 2, 5, 10-14, 21-24, 27-28: supported environments, two-dependency ceiling, RNG, import isolation and version testing |
| P2-C | `PHASE_2_COMPLETION.md`: accepted owner scope, technical results, deviations and later-phase stop |
| P2-V | `PHASE_2_VALIDATION_REPORT.md`: actual baseline commands, full core/Parquet results, review limits and failure history |
| P2-A | `PHASE_2_ARCHITECTURE_COMPLIANCE_REPORT.md`: 40/26 module boundary, restored authority, dependencies, CI and retained limitations |
| P2-F | Supplied `PHASE_2_FINAL_EXECUTION_REPORT.md`: final documentation commit and final-delivery execution identities |
| Historical plans | Supplied `PHASE_2_PLAN.md` plus step approvals; `PHASE_1_PLAN.md` and `PHASE_1_COMPLETION.md`: phase history and preservation requirements |
| Hero | `examples/hero/config.json`, `version_order.json`, `EXPECTED_OUTPUTS.md` and the three CSV files: immutable fixture and expected outcomes |
| Current code inspection | `config.py`: existing representation/scenario/control fields; `check_traceability.py`: exact active functions/imports; `release_check.py`: frozen Phase 2 diff/delivery assumptions; `test_ci_workflows.py`: real optional runs, JUnit, authority and restoration tests; `test_T5_reopening.py`: shared-module placeholder conflict |

Theory page anchors, read as conceptual/formula sources rather than new feature authorization:

- TS1, *The Universal Inbreeding Law v2*, pages 5-9: structural formulas versus the finite-resampling mathematical model, Gini-Simpson expectation, extinction, absorption and reopening; pages 15-17: domain and failure interpretation.
- TS2, *Entropy as a Structural Boundary Condition, Not a Causal Force v2*, pages 1-4 and 7-11: entropy as descriptive boundary, local mechanism and explanatory-scale limits.
- TS3, *Supplementary Case Registry for the Universal Inbreeding Law, Version 2.0*, as mapped by S02: supporting contraction witness and the separately deferred amplification branch. No new amplification feature is selected.

This plan adds no new empirical claim about model collapse, industry behavior or production failure. Proposed implementation conventions are labeled in section 3; approved source content and observed repository state remain separately identifiable.
