# PHASE_6A_PLAN

## Document control

| Field | Value |
|---|---|
| Project | Recursive Integrity Toolkit |
| Phase | Phase 6A: longitudinal dataset comparison |
| Document version / date | 1.0 / 2026-09-26 |
| Status | APPROVED; Steps 1 through 8 authorized |
| Theory Owner | Xiangyu Guo |
| Accepted starting commit | `f09521907558a193e6438d9acb316adb9e191195` |
| Accepted source tree | `da6b0bc3ab64b417ef5be86050f9f932149bc712` |
| Baseline branch / package / report schema | `phase5-lineage` / `0.1.0.dev4` / `1.1` |
| Implementation branch | `phase6a-longitudinal`, from plan commit `753829a79fb6aa550d58dcd6fced360399c597e9` on the accepted Phase 5 history |
| Proposed completed-phase package / schema | `0.1.0.dev5` / `1.2` |
| Current authorization | Step 8 explicitly requested on 2026-09-26 America/Los_Angeles (2026-09-27 UTC) |
| Merge, tag, publication authorization | None |

The Theory Owner instructed “phase 6a step 1开始” on 2026-09-26 America/Los_Angeles (2026-09-27 UTC), authorizing Step 1 under this plan with no stated exceptions. P6A-D01 through P6A-D08 are approved. The subsequent instructions “Phase 6A Step 2继续”, “Phase 6A Step 3 开始”, “Phase 6A Step 4 继续”, “Phase 6A Step 5 继续”, “Phase 6A Step 6 继续”, “Phase 6A Step 7 继续” and “Phase 6A Step 8 开始” authorize those steps. Execution continues one authorized step at a time. See `PHASE_6A_DECISIONS.md` and `docs/longitudinal_contract.md` for the contract record. Step 8 bounded adversarial and scale preparation is complete; see `PHASE_6A_STEP_8.md` for results. Step 9 and Phase 6B have not started.

## 1. Starting point and authority

Phase 5 is complete. Its accepted checkout contains 273 tracked files and 40 Python package modules. The verified code candidate was `53802fb0e99ea867a27bb82210cc9fa32d8e02d1`; `f095219` adds the final completion record. All 13 required candidate jobs passed, including eight OS/Python/dependency profiles, real Parquet, security, performance and delivery. These are historical baseline results, not Phase 6A test results. No product regression or environment matrix is needed merely to write this plan.

The existing implementation provides:

- validated explicit chronology and representation declarations;
- a Python `compare_support` API with directed literal mappings, original and harmonized distributions, support sets, retention and diversity deltas;
- an audit CLI for one primary version and one explicitly requested earlier comparison;
- single-target provenance, direct closure and opt-in ancestry calculations;
- canonical JSON/Markdown, report schema 1.1, privacy handling and installed Hero resources.

The remaining work is multi-version orchestration and truthful change reporting. The current CLI computes only content distributions for its earlier side. Its provenance and lineage summaries belong to the primary version. The existing graph API deliberately rejects comparison/context versions as primary targets. Those boundaries require explicit extensions before any multi-version loop is valid.

Apply the contract order in `PROJECT_INSTRUCTIONS.md` section 4.4, approved UD decisions and accepted Phase 3-5 clarifications. Primary Phase 6A owners are **T1 observed longitudinal comparison, PR-007 ordering and PR-011 dataset-longitudinal capability**. Existing T2/T3/T4/T6, representation, coverage and report owners remain responsible for their reused calculations. Formula F-018 supplies the later-minus-earlier delta convention. No new theory formula is proposed.

Continue the user's Verification Governance and Complexity Control policy and P5-D11: direct semantic correctness stays strict; candidate compatibility and delivery checks run at appropriate milestones; obsolete historical implementation checks remain recoverable through Git. This phase adds no approval registry, receipt chain, source-body migration framework or evidence-of-evidence layer.

## 2. Objective and bounded scope

Produce an explicitly requested series of two or more ordered dataset snapshots, their per-version summaries, adjacent comparisons and optional first-version comparisons. Report observed support/diversity changes, observed label/topic disappearance, provenance changes and available lineage changes with each side's scope, denominator, compatibility and coverage.

Required outputs from product specification section 16.3 are record-count delta, support delta, diversity delta, added/missing states, provenance-coverage delta and source-share delta. This plan also implements earlier-tail disappearance when requested, the existing direct-closure interval changes, and the specified lineage changes when lineage is requested and computable.

Excluded: Phase 6B experiment/reopening orchestration, automatic simulations, model-performance trends, causal intervention claims, permanent population extinction claims, universal scores or thresholds, automatic semantic remapping, all-pairs matrices, temporal regression/forecasting, HTML/dashboard work, remote retrieval and new runtime analytical dependencies. The approved relative-change formula remains available for a future explicit addition; this phase uses absolute deltas only. Avoid introducing percentages or ratios whose extra interpretation is unnecessary for the required outputs.

## 3. Approved contract decisions

### P6A-D01. Require explicit series selection and retained chronology

Add an explicit longitudinal request to the Python/report workflow and `--longitudinal` to `audit` and `example`. `audit --records` continues to identify exactly one primary version, which must be the latest selected snapshot. In longitudinal mode, repeatable `--compare PATH` inputs identify the other selected snapshots. Each CLI records file identifies one nonempty version; repeated version selections and duplicate canonical keys are rejected. Without longitudinal mode, retain the existing single-version/one-pair interface and behavior.

The series contains the selected primary and comparison versions only. Ancestor/context inputs and versions mentioned only in a chronology document do not become snapshots. At least two selected versions are required. File enumeration order, filename spelling, CLI path order and lexical version order cannot supply chronology for the new series. Use retained explicit config/order-file declarations or valid timestamps through the existing order resolver, including conflict and timestamp-tie rules. The existing explicit two-version invocation-order contract remains supported in legacy pair mode.

Order all selected snapshots by that validated chronology and retain its source. Chronology must also cover loaded context when cross-version parent validation requires it. A missing or conflicting order blocks cross-version results while valid independent snapshot results remain reportable. Do not silently sort conflicting evidence into a usable sequence.

An empty file cannot identify a version by itself. The CLI returns a specific input/selection error instead of deriving a version from its filename. Typed Python calls may represent an explicitly identified empty snapshot; all zero-denominator and empty-distribution rules still apply. A nonempty snapshot whose representation excludes every row remains selected, with unavailable representation metrics.

### P6A-D02. Compare adjacent snapshots; make baseline comparison explicit

For selected order `v1, ..., vk`, default to `k-1` adjacent pairs. An optional `baseline=first` declaration additionally requests the first snapshot against each later snapshot. Deduplicate the first adjacent pair, so at most `2k-3` distinct comparisons execute. Default baseline is `none`. A baseline is a selected observed snapshot, not a model of the underlying population.

Keep per-version original summaries separate from pair results. Each pair records its two version IDs, pair kind(s), compatibility evidence, original/harmonized basis and status. No hidden all-pairs expansion, endpoint substitution, pooled distribution or average-of-deltas is permitted. If an intermediate pair is unavailable, keep that gap. Independently requested valid baseline pairs can still be calculated.

No regression slope, overall collapse classification, or inferred causal trajectory is generated. Loss, gain and reappearance remain local observations at their declared positions.

### P6A-D03. Preserve exact representation and population contracts

Reuse `RepresentationDescriptor`, `ExplicitPairContext`, `StateMappingDeclaration` and `validate_representation_compatibility`; do not create a competing interpretation of compatibility. Every selected snapshot has an explicit representation and literal state-meaning declaration. A common declaration may apply to all selected snapshots only when the user actually declares it.

Support exact compatible descriptors and explicitly supplied directed literal mappings through the existing pair kernel. Mappings must identify source/target descriptors and meanings, cover the required supplied states, preserve missing-state rules and expose many-to-one collisions. No automatic mapping composition, semantic inference or silent fallback is allowed. Configuration may serialize these existing typed declarations; the currently accepted bare mapping/compatibility fields must not be promoted into sufficient mapping authority.

Pair-local harmonization does not establish one common multi-version basis. Display original snapshot values with their descriptors; label mapped comparisons with their own harmonized basis. A connected common-basis trajectory is available only when all included snapshots explicitly share that basis and meaning. Otherwise retain separate basis groups and pair-local results, without a global trend claim or hidden transitive mapping.

An incompatible pair blocks its comparison results and records the reason; valid single-version observations remain. This phase does not introduce a separate provenance-only bypass around the approved Level 4 representation gate. A failure in an unrelated optional calculation need not invalidate an otherwise eligible pair.

Keep count-backed and probability-only inputs distinct. Reuse existing weighting and denominator checks: compare like with like; do not replace unweighted values with weighted values. CLI series uses the existing unweighted record analysis. Preserve supported explicit weighted Python pairs without automatically expanding them into a new CLI feature.

Representation eligibility exclusions affect representation metrics only. Record count, provenance and lineage use their independently declared complete version populations. Every snapshot and pair records both sides' population counts, eligible/excluded counts, denominator basis and relevant weighting. Context records enter none of these target denominators.

### P6A-D04. Define observed distribution changes and tail disappearance

All deltas use `later - earlier` in the original metric's unit and have evidence class `derived_metric`; their source snapshots retain their existing evidence classes. Counts use record or state units; share and coverage deltas use ratios in `[-1,1]`, not a percentage-change formula. Reuse `compare_support` for support delta, loss/addition counts, retained states, retention and diversity delta. Add record-count delta from the complete version populations.

For eligible pair supports `S_e` and `S_l`:

```text
missing states = S_e \ S_l
added states = S_l \ S_e
retained states = S_e intersection S_l
support retention = |retained states| / |S_e|
```

State disappearance has evidence class `derived_metric` and the required interpretation: **extinct from the observed later version under the declared representation**. It does not establish permanent absence from the production process. A state absent at v2 and present at v3 appears in the relevant missing and added sets; earlier outputs remain valid observations.

Tail disappearance is optional and requires the existing explicit tail rule/threshold. Select the earlier tail on the pair's comparison basis using that side's counts/frequencies, then intersect it with the pair's missing-state set. Retain the rule, threshold, earlier sample size and representation. Do not select the later tail or silently import a threshold from another snapshot. For mapped pairs, disclose that tail membership uses the harmonized earlier distribution and preserve its original distribution separately. No one-step extinction probability or resampling scenario executes.

Empty/all-excluded distributions retain the accepted Phase 3 behavior: unavailable pair distribution values and null state sets. Do not report all earlier states extinct when later evidence is absent. An eligible comparison with no missing states reports an empty set and zero loss. Do not collapse this distinction during rendering or redaction. Independently defined record-count deltas may still exist for explicitly identified empty snapshots.

### P6A-D05. Calculate provenance and direct closure per version

Reuse validated joins, `summarize_provenance` and the current direct-closure kernel for each selected version. Calculate each snapshot once. Expose separate changes in provenance-row coverage, required-field coverage and grounding-field coverage. Never label all three as one unspecified coverage measure.

Source-share changes retain `human`, `synthetic`, `mixed`, `sensor`, explicit `unknown` and missing-provenance categories under the existing denominator convention. Missing rows remain distinct from declared unknown; estimates remain distinct from confirmed/log-derived assertions. `mixed` is not redistributed. Changes in metadata availability are visible alongside changes in declared composition.

Report direct-closure lower-bound, upper-bound and interval-width changes as endpoint/width arithmetic, preserving both original intervals and their populations. A narrower interval can result from improved evidence. An endpoint delta does not prove an equivalent change in a hidden true closure rate.

Null values propagate to the affected delta with side-specific reasons; valid zero remains zero. Malformed provenance follows existing family failure rules. Do not pool versions to repair a missing side or interpolate unavailable shares. All provenance quantities remain based on supplied declarations.

### P6A-D06. Extend target selection safely for lineage changes

Lineage remains separately opt-in. Without `--lineage`, longitudinal lineage rows show `not_requested`; loading several versions never triggers graph analysis by itself. With lineage requested, use the union of explicitly loaded selected snapshots and disjoint context records as a common graph evidence scope for this invocation.

Introduce a validated series-target selection interface that admits only versions explicitly selected as snapshots. Keep the current ordinary graph API's primary-only default and its context exclusion. Do not implement the series by loosely relabeling context rows, editing validation objects or bypassing the existing graph/result identity checks. Bind each result to the actual selected version, full target key set and retained input declarations. Step 1 fixes the narrow typed interface before this change is implemented.

Reuse parent parsing, identity resolution, chronology, cycles, depth, grounding/carryover rules and G/C/U classification. Validate and build shared graph structure once where the existing integrity checks permit it; cache only invocation-local, immutable, input-bound work. Derive each selected target summary from that shared evidence without recomputing every entire audit or creating a persistent cache. A disconnected cycle remains a graph error under the Phase 5 contract.

Compare distinct supporting external-root count, HHI, effective root count, unresolved reference count, resolved-reference coverage, resolved-lineage/external-ancestry coverage and lineage-closure interval endpoints/width. Retain each version's N/G/C/U and reference denominators. Count target-supported roots, not every anchor loaded into the graph. Root identity, allocation method and graph rules remain those approved in Phase 5.

Both finite, semantically compatible values are needed for a numerical delta. A partially resolved result may provide its valid grounded-subset metric, with a partial delta and both sides' coverage attached. Such arithmetic describes the observed subsets; it must not claim a full-population ancestry change or that a change in visibility proves a change in actual roots. G=0 concentration, failed resource stages, unresolved metrics and unrequested analysis produce unavailable/unrequested affected deltas, never artificial zeros. Shared-root proxy states remain categorical; do not subtract or rank them.

All snapshots in a run use the disclosed common loaded evidence scope. This is a retrospective comparison of the supplied versions, not a reconstruction of what was known at each historical date. Parent links to later versions under the validated chronology remain invalid. No historical visibility inference is added. Evidence additions in a later invocation can legitimately revise an earlier snapshot's coverage; reports must make the different context/input basis identifiable.

### P6A-D07. Extend the canonical report once and protect every new field

Use report schema `1.2` for the completed phase, including ordinary reports. Retain the twelve top-level sections, capability mirrors and finite-number/null rules. Add a typed longitudinal family under the existing sections, with ordered snapshot summaries, explicit pair results, selection/order evidence, representation bases, per-family statuses, resource limits and bounded details. Step 1 records the exact public field inventory and units before runtime work.

Preserve existing single-target and explicit-pair values and meanings. Multi-version results have their own named fields; do not silently fill an old singular-pair field with an arbitrary adjacent or endpoint pair. The primary version can continue to populate existing ordinary summary fields. Strict schema-1.1 consumers must opt into 1.2; no report migration framework is introduced.

JSON and Markdown consume the same canonical typed calculations. Renderers own no comparison, mapping, graph or delta arithmetic. Input observability remains distinct from execution status. Series execution distinguishes `not_requested`, `completed`, `partial` and `failed`, with family/pair reasons. No complete-series claim is allowed while a requested pair/family is unresolved, incompatible or uncomputed. Optional families not requested do not make an otherwise completed requested analysis partial. Replace the current blanket `R_LONGITUDINAL_FAMILIES_DEFERRED` classification only for the families actually implemented and requested; preserve accurate legacy pair capability limits. Existing error exit behavior still applies to actual validation/resource errors.

Apply privacy to version/state/root identifiers, mapping keys and values, pair references, context evidence, paths, diagnostics and omitted-detail metadata. Consistent pseudonyms must join the same version/state across this report; hash/omit modes must not leak identifiers through a new dictionary key or prose field. Arbitrary user state-meaning declarations also require safe handling. Reuse canonical identifier protection and aggregate-only representations, preserving exact aggregates and schema validity. Standard output remains local, and no-network/output-path protections continue unchanged.

### P6A-D08. Bound orchestration and keep configuration explicit

Proposed engineering guard: at most **100 selected versions** by default, with a validated positive finite integer override. Adjacent plus optional first-baseline selection therefore has at most 197 distinct pairs at the default limit. Reject an over-limit request before materializing per-version calculations. Context inputs remain subject to inherited input/graph limits and never consume snapshot slots.

Keep Phase 5 default guards for the union of loaded records: 200,000 nodes, 1,000,000 unique edges, 1,000,000 stored record/root memberships and 10,000,000 root-union candidate visits, alongside existing input byte/row/parent-list limits. Shared lineage work must retain meaningful deterministic counters. Independent reprocessing must not reset a work counter to evade the guard. Additional aggregate summaries should not duplicate all per-record ancestry evidence for every version.

Limit new state/root detail tables to the current 100-row report convention per table, with exact total/shown/omitted counts. Compute aggregate counts and metrics from complete eligible data before applying the display cap. Do not emit all paths, all-pairs intersections or a full ordinary report for every snapshot. Reuse immutable per-version scopes internally and avoid copying complete identity lists into every new pair or metric. Step 1 defines any explicit scope-reference serialization needed for the new series fields. Retain bounded diagnostics and disclose known pre-existing ordinary-report size costs.

Resource failure preserves independently completed results with explicit scope and failure reasons. Do not calculate a series aggregate from a truncated selection, label uncomputed pairs as zero, or quietly raise limits to pass a benchmark. These guards are operational limits, not scientific thresholds or a memory/time SLA.

Configuration extends existing input-role lists with a bounded longitudinal options object for enablement, baseline selection, per-version declarations and explicit pair mappings. Exact serialization names and conflict validation are frozen in Step 1. The common-representation CLI form uses `--state-semantics`; richer declarations use local declarative config. Reject competing CLI/config singleton declarations. Preserve established Python/config input multiplicity outside the new CLI mode.

`validate` may load repeated comparison/context inputs for input validation, but never executes a series, graph, metric or simulation. Reject execution-only flags there. Package imports and `validate_bundle` remain inert; extend the existing direct isolation checks to the new orchestrator. `example --longitudinal` runs the unchanged two-version Hero; adding `--lineage` also requests both versions' lineage snapshots. A separate compact three-version example exercises actual multi-step change. Existing `example` and `example --lineage` behavior remains available.

## 4. Nine implementation steps

Each step records actual changes, relevant checks and remaining limits in a concise completion note. Preserve the existing phased authorization model. Exact identifiers and serialization choices may be settled within the approved meaning; a material semantic change requires a specific owner decision before dependent implementation.

| Step | Deliverable and dependency | Smallest sufficient acceptance gate |
|---|---|---|
| **1. Contracts and independent examples** | Record actual approval/exceptions in `PHASE_6A_DECISIONS.md`; freeze typed snapshot/pair/series fields, selection API, config declarations, statuses, limits and independent expectations. No runtime series execution. | Reconcile required fields to existing owners/formulas; hand-check the three-version oracle and incompatible/empty/partial cases; affected document/contract consistency only. |
| **2. Ordered selection and compatibility** | Validate selected versions, retained order, adjacent/baseline pair selection, per-version declarations and explicit pair mappings. Depends on 1. | Lexically misleading names, unloaded/context versions, conflicting timestamps/order, missing/repeated versions, pair deduplication, mapping direction/collisions and incompatible-basis gaps. Reuse order/compatibility regression. |
| **3. Snapshot distributions and observed changes** | Reuse distribution and pair kernels; add record-count delta, ordered summaries, support/diversity changes and optional earlier-tail disappearance. Depends on 2. | Independent oracle, reappearance, zero versus null, all-excluded/empty evidence, denominator separation, renaming/permutation invariance and pair-local mapping behavior. No new stochastic execution. |
| **4. Provenance and direct-closure changes** | Compute per-version provenance and direct bounds, then named coverage/source-share/interval deltas. Depends on 2-3. | Unknown versus missing, changing coverage, malformed rows, source categories, zero/partial/unavailable propagation and unchanged single-target values. Relevant provenance/bounds neighbors only. |
| **5. Available lineage changes** | Add validated selected-version targeting and shared immutable graph work; integrate target-specific summaries and compatible deltas. Depends on 2-4. | Primary/context isolation, full target selection, input-signature mismatch rejection, root-support counts, N/G/C/U, partial concentration, same shared context, disconnected cycles and resource-stage failure. Relevant graph/root/report-binding tests. |
| **6. Report schema and privacy integration** | Add canonical series results, schema 1.2 and packaged mirror, JSON/Markdown, capability execution and protected identities. Depends on 3-5. | Two/three-version available/partial/failed/not-requested reports, exact values, bounded details, null states, stable privacy joins, no dictionary-key leakage and legacy pair values. Update report goldens from independent expectations. |
| **7. CLI, configuration and installed examples** | Wire explicit longitudinal mode, repeated comparisons, optional baseline/lineage, richer config and separate three-version example; preserve input-only validate. Depends on 6. | Actual CSV/JSONL plus real optional Parquet, order/config conflict messages, output safety, meaningful exits, standard/redacted installed examples outside checkout and no-network boundaries. |
| **8. Bounded adversarial and scale preparation** | Resolve remaining semantic/resource defects; run the finite mutation set and small/medium multi-version end-to-end measurements; establish the large reference workload. Depends on 2-7. | Mutations detected by direct tests, many-version/pair-limit behavior, capped details with exact aggregates, shared-work scaling, and complete CLI serialization timing/RSS. No new permanent verification framework. |
| **9. Candidate verification and handoff** | Update docs, traceability, changelog and package to dev5; run canonical regression, supported candidate matrix, designated full-scale measurements and delivery checks; record completion. Depends on 1-8. | Required outputs and owners implemented; Hero and three-version oracles hold; installed wheel/sdist, privacy and reproducibility pass; exact limitations and remaining release work documented. No merge, release or Phase 6B execution implied. |

## 5. Independent acceptance oracles

### 5.1 Preserve the canonical Hero

Keep all six canonical Hero source/expectation files unchanged. The existing pair remains v1 to v2: record counts 8/8, support 8/5, diversity 7/8 and 3/4, support delta -3, diversity delta -1/8, retention 5/8, and missing states `battery`, `lizard`, `turtle`. The new record-count delta is 0. Existing v2 direct bounds [1/2,1/2], five supporting roots, HHI 1/4, effective roots 4 and lineage bounds [0,0] remain unchanged.

Step 1 derives new per-v1 provenance/lineage and cross-version expectations directly from the frozen input rows and approved formulas, without editing that oracle or copying implementation output. A two-version series must agree with the existing pair kernel on all shared fields. Schema/package metadata changes must not alter scientific values.

### 5.2 Three-version observed-change fixture

Use one unchanged declared topic representation and these record-count distributions:

| Snapshot | A | B | C | D | Records | Support | Gini-Simpson diversity |
|---|---:|---:|---:|---:|---:|---:|---:|
| v1 | 2 | 1 | 1 | 0 | 4 | 3 | 5/8 |
| v2 | 2 | 0 | 0 | 2 | 4 | 2 | 1/2 |
| v3 | 1 | 1 | 0 | 1 | 3 | 3 | 2/3 |

| Quantity | v1 to v2 | v2 to v3 | v1 to v3, only when baseline requested |
|---|---|---|---|
| Record-count delta | 0 | -1 | -1 |
| Support delta | -1 | +1 | 0 |
| Diversity delta | -1/8 | +1/6 | +1/24 |
| Missing states | {B,C} | empty | {C} |
| Added states | {D} | {B} | {D} |
| Support retention | 1/3 | 1 | 2/3 |
| Earlier-tail disappearance under singleton-count rule | {B,C} | empty | {C} |

B disappears and then reappears. The equal first/last support sizes must not erase that intermediate loss. Compare exact rational expectations with the existing declared numerical tolerance, independently of report generation.

For a separate provenance scenario over the same snapshot sizes:

| Declared provenance population | v1 | v2 | v3 |
|---|---|---|---|
| Human / synthetic / explicit unknown / missing rows | 4 / 0 / 0 / 0 | 2 / 1 / 0 / 1 | 1 / 1 / 1 / 0 |
| Provenance-row coverage | 1 | 3/4 | 1 |
| Human share | 1 | 1/2 | 1/3 |
| Synthetic share | 0 | 1/4 | 1/3 |
| Explicit unknown share | 0 | 0 | 1/3 |
| Missing-provenance share | 0 | 1/4 | 0 |
| Grounding yes / no / unresolved counts | 4 / 0 / 0 | 2 / 1 / 1 | 1 / 1 / 1 |
| Direct-closure interval | [0,0] | [1/4,1/2] | [1/3,2/3] |

Thus row-coverage deltas are -1/4 and +1/4; human-share deltas -1/2 and -1/6; synthetic-share deltas +1/4 and +1/12. Lower-bound deltas are +1/4 and +1/12; upper-bound deltas +1/2 and +1/6. Explicit unknown is never repaired into missing or synthetic. Freeze the remaining field-coverage expectations after specifying every manifest field in Step 1.

### 5.3 Separate lineage oracle and failure variants

Use two explicit parentless grounded context anchors a and b. In a complete scenario, v1 has four targets with root sets `{a},{a},{b},{b}`; v2 has four targets all supported by `{a}`; v3 has two targets supported by `{a},{b}`. All targets truthfully declare grounding `no` and reference their anchor.

| Quantity | v1 | v2 | v3 |
|---|---:|---:|---:|
| N / G / C / U | 4/4/0/0 | 4/4/0/0 | 2/2/0/0 |
| Supporting external roots | 2 | 1 | 2 |
| HHI | 1/2 | 1 | 1/2 |
| Effective root count | 2 | 1 | 2 |
| Resolved-lineage coverage | 1 | 1 | 1 |
| Lineage-closure interval | [0,0] | [0,0] | [0,0] |

Adjacent root-count deltas are -1/+1; HHI deltas +1/2/-1/2; effective-root deltas -1/+1. Loaded anchor count is two throughout and must not replace target-supported root count.

Then add a third v3 target with an unresolved parent. Its G/C/U becomes 2/0/1, coverage 2/3 and bounds [0,1/3]. HHI remains 1/2 over its grounded subset; its delta is explicitly partial. A separate G=0 variant makes HHI/effective roots and their deltas unavailable. Further bounded cases cover unknown grounding, known-empty root sets, a disconnected cycle, resource exhaustion, unchanged record IDs with altered parent declarations, and a context-only version that never becomes a snapshot.

### 5.4 Required semantic distinctions

Include incompatible middle-version representation with valid independent snapshots; different pair-local mapping bases; many-to-one collision disclosure; missing timestamps/order; tied timestamps; v2/v10 lexical traps; unloaded versions in declared order; empty versus all-excluded snapshots; literal zero-mass states; unequal record populations; earlier-tail versus later-tail membership; changed context visibility; pair failures without zero-filled gaps; renamed/shuffled input invariance; and redaction across repeated state/version identities.

Use a finite mutation set for distinct failure modes: reversed delta sign, lexical chronology, context inclusion in N, missing provenance folded into unknown, later-tail selection, incompatible pair accepted, unavailable value replaced with zero, and all-loaded roots substituted for target-supported roots. Record whether current tests detect each defect and fix genuine gaps. Do not create a new mutation registry or a numerical test-count target.

## 6. Verification, performance and delivery policy

| Change or boundary | Verification |
|---|---|
| This plan and later administrative notes | Document/authority consistency and independent review; no product matrix |
| Selection, compatibility or arithmetic | Direct examples/properties and affected existing kernel neighbors |
| Target selection, input roles, report schema, CLI or privacy | Relevant integration and boundary regression |
| Stable candidate | Complete current regression; Ubuntu/Windows, Python 3.11/3.12, minimum/current compatible direct dependencies |
| Optional input support | Actual no-PyArrow core profiles and a real-PyArrow profile |
| Delivery candidate | Existing build, wheel/sdist, clean installs, installed examples, no-network/security and documented reproducibility checks |
| Administrative successor with unchanged applicable runtime/authority | Direct consistency plus clearly identified reusable candidate evidence |

Reuse existing CI, release and traceability tooling. Update the current path rather than adding a permanent phase dispatch layer. Full matrices belong to the stable candidate; ordinary implementation steps run affected gates. A failed check requires the relevant correction and rerun. Additional testing must address a concrete remaining risk.

Measure complete series CLI execution, including input validation, selected per-version work, optional lineage, report assembly and JSON/Markdown publication. Record selected/context records, version/pair counts, states, graph edges/root memberships/union visits, elapsed time, fresh-process peak RSS and output bytes. Report inherited high-water marks if a fresh process cannot be used. Kernel timing cannot certify complete CLI performance.

Use a compact many-version workload to detect repeated global scans and unintended quadratic pairing. Establish a three-version **100,000-record total loaded-input** workload, counting context in that total, and execute it on one designated reference profile at the candidate boundary. It must exercise longitudinal CLI serialization and available lineage changes. This is 100k combined records, not 100k per snapshot. Keep bounded cases across the compatibility matrix. Step 8 performs smaller preflight measurements; it need not repeat the eventual full-scale run.

Retain required existing candidate gates. Run each required expensive workload once on the reference profile, not once per version, pair or OS/dependency combination. Reuse unchanged historical evidence only where the existing governance permits it and the workload/runtime relationship is demonstrated; do not present Phase 5 results as new Phase 6A measurements. There is no approved hard wall-time/RSS SLA for the new 100k series workload. Establish an observed baseline and a practical CI timeout without silently loosening resource defaults.

Measure the two-version Hero with longitudinal mode, both with and without lineage, against the existing under-five-second reference target. Disclose profile and every retained attempt. A greater-than-20% time or greater-than-50% memory regression on a comparable workload triggers review; changed workloads require separate labels.

Phase 5's hosted results provide scale context: 100k ancestry API took 66.23 seconds and about 1.85 GB peak RSS, excluding full reports; the ordinary 100k metadata report took 780.73 seconds and about 7.68 GB peak RSS, producing about 443 MB JSON and 165 MB Markdown. Those observations make one-full-report-per-version an unsuitable default design. Share validated work and scope references, cap new detail, and report actual total output size. If measurement reveals a bottleneck, permit a narrow behavior-preserving fix in the affected assembly or orchestration path, with direct regression. Broader redesign requires a separate scoped decision.

## 7. Ownership, completion and next boundary

Expected implementation locations are existing config/models/result types, `io/validation.py` selection adapters, `representations/compatibility.py`, `metrics/diversity.py`, `metrics/provenance.py`, `metrics/bounds.py`, lineage target/summary interfaces, report assembly/rendering, CLI, schemas and packaged resources. A small `metrics/longitudinal.py` orchestration owner is appropriate if it keeps reusable calculation outside the CLI; it must delegate existing kernels and must not become a generic plugin framework. Tests, a compact example, docs, traceability and existing candidate tools may change as needed.

Preserve frozen Phase 0 files, canonical Hero inputs/expectations and approved scientific meanings. Record clarifications additively. Do not modify theory source PDFs, unrelated mathematical kernels, source-type meaning, direct grounding rules, generation meaning or parent identity conventions. Any actual authority conflict is reported with the affected step and proposed resolution before dependent implementation.

Phase 6A completes when all required version deltas, explicit selection/compatibility, observed disappearance, provenance changes, available lineage changes, truthful partial states, schema/privacy, installed commands, candidate compatibility and delivery checks pass. Completion reports identify the tested candidate, actual checks, performance scope and known limitations. They do not require historical source-code forms to remain executable forever.

The handoff leaves two distinct choices: optional Phase 6B, if separately approved, and formal v0.1 release preparation/acceptance. Phase 6A completion itself does not merge draft PRs, approve a release, create a tag, publish a package or claim model-performance validation. An unmerged accepted Phase 5 branch can serve as the development base; prior PR merges are not a prerequisite for writing or implementing this plan.

## 8. Source basis

- `PROJECT_INSTRUCTIONS.md`: authority order; Phase 6A/6B boundaries; evidence, chronology, representation and unavailable-conclusion rules.
- `SPEC_AUDIT.md` and `UNRESOLVED_DECISIONS.md`: approved UD-007 ordering and UD-017 phase split, plus representation and report decisions.
- `V0.1_PRODUCT_SPEC.md` section 16: required version deltas, observed-extinction wording, available lineage change and model boundary.
- `DEFINITIONS_AND_UNITS.md` sections 6, 10.10 and 14: representation/support, earlier-tail extinction, delta and relative-change definitions.
- `DATA_AND_PROVENANCE_SPEC.md`: identity, ordering, joins, grounding and parent declarations.
- `THEORY_TO_CODE_TRACEABILITY.md`: T1 observed support contraction, existing provenance/ancestry owners, PR-007/PR-011 and Phase 6A requirements.
- `VALIDATION_PLAN.md` section 82 and `SUCCESS_CRITERIA.md`: Phase 6A acceptance and candidate obligations.
- `PHASE_3_DECISIONS.md`: explicit-pair compatibility, mapping, weighting and empty-distribution contracts.
- `PHASE_5_PLAN.md`, `PHASE_5_DECISIONS.md`, `PHASE_5_COMPLETION.md`: accepted target/context, root/coverage, report-binding, resource and verification boundaries.
- `examples/hero/EXPECTED_OUTPUTS.md` and its canonical inputs: immutable two-version scientific oracle.
- Current code: `metrics/diversity.py`, `metrics/provenance.py`, `representations/compatibility.py`, `lineage/graph.py`, `lineage/ancestry.py`, `observability/levels.py`, `reports/assembly.py`, `config.py` and `cli.py`.
- User instruction: Verification Governance and Complexity Control, applied through the accepted Phase 5 consolidation.
