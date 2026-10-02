# PHASE_5_PLAN

## Document control

| Field | Value |
|---|---|
| Project | Recursive Integrity Toolkit |
| Phase | Phase 5: lineage graph and ancestry |
| Document version / date | 1.0 / 2026-09-23 |
| Status | APPROVED; Step 1 authorized |
| Theory Owner | Xiangyu Guo |
| Accepted starting commit | `1db3b1a460c233242ff37fbe45b8fac74d6101ef` |
| Accepted source tree | `51d8854d9869b8a0aeb498230e02b03797ed8634` |
| Baseline branch / package | `phase4-reports-cli` / `0.1.0.dev3` |
| Proposed implementation branch | `phase5-lineage`, from the accepted commit after Step 1 authorization |
| Proposed completed-phase version | `0.1.0.dev4`; this is not a final v0.1 release |
| Authorization recorded | Plan approved and Step 1 started by the Theory Owner on 2026-09-23 |
| Merge, tag, publication authorization | None |

The Theory Owner approved this plan and authorized Step 1 on 2026-09-23: “批准，Phase 5 step 1开始”. All P5-D decisions below are approved without stated exceptions. Execution continues one authorized step at a time; this approval does not automatically execute all ten steps. See `PHASE_5_DECISIONS.md` for the Step 1 contract record.

## 1. Starting point and governing constraints

The inspected checkout is clean at the accepted commit: 246 tracked files and 40 Python package modules. All sixteen frozen Phase 0 specifications match the existing approved baseline. PR #1 remains open and draft, with the accepted commit as its head. Starting the proposed Phase 5 branch does not require merging that PR.

Phase 4 delivers input validation, existing metrics, JSON/Markdown reports, privacy modes, a local audit CLI, one explicitly requested comparison pair and an installed Hero example. General graph traversal and ancestry remain deferred. The lineage modules and their designated tests/fixtures provide the intended implementation locations.

Historical Phase 4 evidence includes twelve successful candidate jobs: eight supported core profiles at 3,965 tests each, a real-Parquet profile at 3,968, Hero at 203 and security at 3,277, plus delivery checks. The verified code candidate was `ceb0cf702284dbdbe50b14722026ec26fbcc21ba`; the accepted successor changed three administrative reports. These are preservation evidence, not Phase 5 results. No product tests were rerun to write this plan.

Apply `PROJECT_INSTRUCTIONS.md` section 4.4 and the approved UD decisions. The primary Phase 5 owners are **T4, T6, PR-008 full graph behavior, PR-009 lineage depth, and T3 lineage bounds**. P3-D01 reserves these functions for Phase 5 despite older overlapping roadmap wording. The plan introduces no new interpretation of the theory papers or new scientific formula.

The user's Verification Governance and Complexity Control instruction governs this phase:

- Strengthen direct product/scientific correctness and real security boundaries.
- Keep compatibility, packaging and reproducibility gates at suitable candidate milestones.
- Consolidate historical implementation checks when equivalent current behavioral coverage exists and Git/archive evidence remains recoverable.
- Add no new approval registry, source-body migration chain, execution-receipt framework or evidence-of-evidence layer by default.

## 2. Objective and exclusions

Deliver an explicitly requested, local lineage analysis over validated records: parent graph, cycle detection, ancestry resolution, external-root incidence and concentration, lineage coverage, depth and lineage-aware closure bounds. Integrate the results into typed reports and the CLI while preserving existing metric scopes and privacy guarantees.

Phase 6A retains automatic multi-version orchestration, trajectories, lineage-change comparisons and additional longitudinal formulas. Phase 6B retains experiment/reopening workflows. Also excluded are network retrieval, inferred parents, causal root weights, semantic ancestry, HTML implementation, model-performance conclusions, universal risk thresholds, new runtime graph dependencies and unrestricted graph/path exports.

## 3. Approved contract decisions

### P5-D01. Separate the target population from the supporting graph

Use canonical `RecordKey(dataset_version, record_id)` identities. The analyzed target contains N selected records from one primary version. The loaded graph may also contain explicitly supplied ancestor records. Only target records enter target counts, provenance shares, closure denominators, ancestry incidence shares and concentration allocation. Context records can supply roots and paths without becoming additional observations.

Reports identify the target version/count and loaded graph counts separately. Existing representation eligibility exclusions remain specific to their metrics; they must not silently shrink the provenance or lineage denominator. An empty target produces explicit unavailable ratios and no invented version identity.

### P5-D02. Reuse validated references and preserve declaration semantics

Consume existing parent-resolution results, aliases, version order and declaration states. Do not implement a competing interpretation of parent IDs. Preserve the distinction between an absent/null declaration and explicit `parent_ids=[]`.

The current bundle validator loses its aggregate generation/parent result after the first malformed, ambiguous, future-parent or self-parent exception. Step 2 therefore permits a narrow batch resolver refactor that retains per-record successes, failures and explicit self-reference evidence, reusing one identity lookup index. Preserve public validation/error and generation semantics. Invalid references never become accepted ancestry edges; self-reference evidence remains available for cycle diagnostics. This retention is necessary to report unaffected records honestly and must not require rebuilding an O(V) index for each record.

Resolve cross-version edges only under the existing explicit chronology. Same-version edges are allowed when acyclic. Duplicate canonical identities fail validation. Missing parents remain unresolved and warning-level by default, with existing strict-mode escalation; ambiguity and future-parent violations remain errors.

Reference coverage counts original declared references, including aliases or repeated references, using the existing resolver's denominator. Graph adjacency and root unions deduplicate canonical edges/roots. Thus repeated declarations cannot inflate ancestry mass. With no declared references, edge coverage is 1.0 and `no_declared_parents=true`; this alone proves neither grounding nor ancestry completeness.

This zero-reference convention follows the frozen definition and deliberately replaces the current report's null/unavailable convention when lineage executes under schema 1.1. With lineage disabled, retain the existing immediate-reference observation and null reason for its zero denominator, clearly labeled as validation evidence; do not synthesize executed graph coverage. Test both modes explicitly.

### P5-D03. Define cycles, affected records and depth precisely

Use iterative graph algorithms. Report `cycle_count` as the number of **cyclic strongly connected components**, explicitly labeled with that method: a component has multiple nodes or a self-loop. This resolves the previously unspecified counting convention without enumerating every simple cycle.

Distinguish cycle members from affected descendants along parent-to-child edges. Return a bounded deterministic witness per reported component, total counts and explicit detail-omission metadata. A detected cycle is a lineage validation error. Affected target records have unresolved ancestry; independent families and unaffected target ancestry may remain reportable with partial status and precise scope. Never label the entire loaded graph acyclic when a disconnected cycle exists, and never return a successful CLI audit status for a lineage error.

Depth is the maximum number of edges to loaded parentless roots on fully resolved paths. An incomplete or invalid required path produces null with a reason. Known partial depth may be diagnostic only when labeled as a lower bound. Generation and lineage depth remain distinct: a carryover can have generation zero and positive depth.

### P5-D04. Adopt a conservative, schema-preserving external-root rule

An explicitly parentless record with validated `external_grounding=yes` anchors an external root. A parentless record with grounding `no` has a known-empty root set; grounding `unknown`, missing required provenance or an undeclared parent boundary makes root resolution incomplete.

A grounded `transformation=carryover` record with exactly one resolved parent inherits that parent's external roots. It does not create a new root merely because its own grounding is `yes`. A carryover with additional unresolved declarations is incomplete.

Represent a new independent external input as a separately loaded, explicitly parentless, grounded record and link it as an ordinary parent. No evidence URI, source label, review flag or transformation string alone certifies independence in Phase 5. This pattern supports truthfully ungrounded child transformations and unambiguous single-parent grounded carryovers.

A grounded record with parents outside the single-parent carryover rule remains unresolved in Phase 5, even when a separate grounded anchor is present. A different rule would require an explicit contract decision. Multi-parent carryover is not silently collapsed. Never change a child's actual grounding label merely to fit the supported representation.

Strict ancestors exclude the record itself. Separately, an external root supports itself: its support-root set is `{its own key}`. This convention must be named explicitly wherever root support is exposed.

### P5-D05. Require complete root sets for exact ancestry metrics

For each target record r, compute its unique external-root set A_r only when every required path is resolved under P5-D02 through P5-D04. Unknown grounding anywhere on a required path propagates uncertainty. One known root plus an unresolved branch is insufficient for an exact root distribution.

Partition targets into grounded G, closed C and unresolved U:

- G: complete, nonempty external-root set.
- C: complete, known-empty external-root set.
- U: incomplete or invalid ancestry, including missing/ambiguous links, cycles, unknown grounding, conflicting declarations and undeclared boundaries.

N = |G| + |C| + |U|. `records_with_resolved_external_ancestry` includes G and C. Resolved lineage coverage is (|G|+|C|)/N; external ancestry coverage is |G|/N. Optional observed roots on incomplete paths are diagnostics only and cannot enter exact root metrics.

### P5-D06. Preserve the approved incidence and fractional-mass formulas

For each unique root a among G:

```text
I_a = count of r in G for which a belongs to A_r
incidence_share_a = I_a / N
M_a = sum over r in G containing a of 1 / |A_r|
w_a = M_a / |G|
ancestry_HHI = sum_a w_a^2
effective_external_root_count = 1 / ancestry_HHI
```

Each grounded target contributes total mass one, including a target that is itself an external root. Rank roots by decreasing incidence, breaking ties with canonical record key. Distinct roots are the union over G. All reported shares state their denominators. If G is empty, HHI and effective-root count are unavailable/undefined with reasons; they are not zero or infinity.

These are topological allocation conventions. They do not estimate causal contribution, semantic error, independent information, biological relatedness or universal integrity. Multiple paths to the same root must not multiply that root's contribution.

### P5-D07. Add lineage bounds without changing direct bounds

For nonempty targets, lineage closure bounds are:

```text
lower = |C| / N
upper = (|C| + |U|) / N
width = |U| / N
```

Keep direct closure calculations and their classifications unchanged. Report coverage and unresolved reasons alongside lineage bounds. A shared-root dependence signal is a descriptive proxy: `present` when a completely resolved root supports at least two targets; `absent` only when all target ancestry is resolved and no such root exists; otherwise `unavailable`. A witnessed `present` on partial coverage discloses that coverage. This is not a calibrated risk level.

T4 retains its theory-guided operationalization label. T6 is an engineering graph-validity rule, not a theorem establishing the theory's scientific claims.

### P5-D08. Use one report schema revision and protect new identifiers

Use `report_schema_version: "1.1"` for all Phase 5 reports. Retain the twelve top-level sections, equal capability mirrors, finite values, explicit unavailable reasons and unchanged non-lineage numerical semantics. The root schema and packaged schema remain identical.

Extend typed immutable results for lineage scope, resolution counts, roots/incidence, concentration, bounds, depth and cycles. Values are computed before rendering. JSON and Markdown share the same canonical result; renderers own no graph or mathematical logic.

Lineage execution defaults to `not_requested`; explicit execution yields `completed`, `partial` or `failed` according to actual coverage/errors. Input observability remains distinct from execution. More loaded versions do not mean a comparison ran.

Apply existing privacy modes to every new key, path and witness. Redacted output supports an explicit aggregate-only or omitted-detail representation that still validates against the schema. Removing required row fields while leaving invalid rows is unacceptable. Preserve no-network, safe-output and deterministic identifier behavior.

Strict schema-1.0 consumers must explicitly adopt 1.1. This plan does not promise backward acceptance by those readers or add a report migration framework.

### P5-D09. Make lineage opt-in and context inputs explicit

Add `--lineage` to `audit` and `example`. Add repeatable `--lineage-records PATH`, backed by a dedicated `FileRole.LINEAGE_CONTEXT` and existing local loaders. For `audit`, context inputs require lineage opt-in. Record/provenance row schemas remain unchanged; config input-role and report inventory enums expand coherently.

`--records` selects exactly one primary version. `--compare` retains its existing CLI limit of one explicit earlier comparison input and all current compatibility declarations. With lineage requested, that comparison input may also supply ancestors; supplying context does not automatically request comparison.

Context versions must be disjoint from primary and comparison versions. This keeps the existing whole-version provenance join unambiguous. Same-version lineage is supported when the needed same-version records are in the primary input. Splitting one version across target and context roles is outside this phase. Duplicate keys across repeated context inputs are rejected.

All ordinary metric calls explicitly select the primary population instead of pooling loaded versions. Preserve existing Python/config multiplicity for other supported input roles; a CLI restriction must not accidentally narrow those APIs.

`validate` may ingest context inputs for existing input/reference validation, but rejects the lineage execution flag and never runs graph metrics. `validate_bundle(...)` remains input-only. `rit example --lineage --out ...` executes the frozen Hero with installed resources outside the checkout. Plain `rit example` retains ordinary calculations with lineage `not_requested` under schema 1.1.

### P5-D10. Bound graph work and disclose resource failures

Use standard-library iterative adjacency/SCC/topological algorithms. Graph traversal should be O(V+E); root-set propagation can grow with V times the number of roots. Sparse edges alone do not guarantee bounded root-set memory.

Approved initial configurable limits for explicitly requested lineage are 200,000 loaded nodes, 1,000,000 unique edges, 1,000,000 stored record/root memberships and 10,000,000 root-union candidate visits. A visit means processing one candidate root identity into a child's union. These finite engineering guards bound algorithmic work; they do not guarantee a particular peak RSS or establish scientific thresholds. Check cumulative node admission across primary, comparison and context batches before graph materialization, edge admission before adjacency insertion, and root memberships/work before union insertion. Retain the separate inherited input byte/row/parent-list limits: graph guards do not bound allocations already incurred while loading a table. Caller overrides must be explicit positive finite integers.

Guard details and counters must be deterministic. On exhaustion, provide a resource-limit reason and no exact lineage values based on truncated work. Preserve independently completed non-lineage families. Bound report diagnostics and witness output separately, disclosing omitted counts; do not export all paths or a full transitive closure. Step 1 fixes the diagnostic row cap using existing report conventions; Step 9 measures whether the proposed defaults need a documented adjustment. No silent limit increase is permitted to make a gate pass.

### P5-D11. Consolidate current verification instead of extending its history

Maintain three practical bodies: current canonical regression, candidate/release verification, and historical evidence recoverable from Git and archived phase records. Use existing test locations and tooling; this classification does not require new registries.

At this phase boundary, replace obsolete placeholder, exact historical test-body and source-wrapper assertions with equivalent or stronger current behavioral tests. Identify the protected behavior in the existing decision/PR explanation, retain its direct test and keep the old evidence recoverable. For example, unauthorized product mutation must still be rejected where that boundary applies; the exact old Python method body need not remain executable forever.

Consolidate the existing phase dispatch in spec/traceability/release checks and workflows into one current path. Do not clone the Phase 4 framework into a new permanent chain. Preserve frozen source specifications and historical evidence; do not rewrite them to manufacture approval.

Any proposed new Tier D control needs all five justifications: exact failure; why A/B/C cannot detect it; why Git/archive is insufficient; maintenance cost; consolidation/exit path. Otherwise omit it. No new mechanism of that kind is proposed here.

## 4. Ten implementation steps

Each step ends with its actual changes, relevant checks and remaining limitations. Dependent work starts only after its preceding contracts are settled. Failed checks are repaired before dependent execution; no step is complete merely because its files exist.

| Step | Deliverable and dependencies | Acceptance and smallest sufficient gate |
|---|---|---|
| **1. Contracts and current verification boundary** | Record actual approval/any exceptions in a concise Phase 5 decision document; finalize typed field names, bounded diagnostic detail and resource interfaces; specify independent fixture expectations. Consolidate obsolete current-phase dispatch/assertions under P5-D11. | Every behavior retired from historical execution has current equivalent coverage and recoverable evidence. Check affected consistency/dispatch and behavioral boundary tests only. No graph completion claims. |
| **2. Validated parent graph** | Implement graph types/construction in `lineage/graph.py`, consuming the resolver with the bounded retention refactor in P5-D02. Establish target/context scope and immutable adjacency. Depends on 1. | Identity, duplicate declarations, aliases, same-version edges, chronology, missing/ambiguous parents, retained partial results and role scope cases pass. Run parent-resolution and relevant generation neighbors. |
| **3. Cycles, topology and depth** | Implement iterative SCC detection, affected descendants, bounded witnesses, topological ordering and depth. Depends on 2. | Self-loop, two-node/long/disconnected cycles, descendant propagation and a chain beyond Python recursion depth behave as specified. Errors never claim completed whole-graph lineage. |
| **4. Root resolution and coverage** | Implement external anchors, carryover inheritance, unique root unions and G/C/U classification in `lineage/ancestry.py`. Depends on 2-3. | Parentless yes/no/unknown, absent versus empty declarations, multi-parent unions, incomplete branches and conservative grounded-parent cases match independent fixtures. |
| **5. Incidence and concentration** | Add typed root incidence, denominator metadata, fractional mass, HHI and effective roots. Depends on 4. | Hero and multi-root arithmetic match exact/rational oracles; renaming, permutation and duplicate-path invariance hold. Empty G has explicit unavailable values. |
| **6. Lineage closure and descriptive proxy** | Integrate lineage bounds and shared-root proxy, leaving direct bounds unchanged. Depends on 4-5. | G/C/U partition and interval identities hold; missing and unknown propagation are tested independently; direct-bound regressions remain unchanged. |
| **7. Canonical reports and privacy** | Integrate typed results, schema 1.1 and its packaged mirror, assembly, JSON/Markdown and redaction. Depends on 3-6. | Non-lineage values/scopes remain stable; complete/partial/failed/not-requested results validate; new keys and witnesses obey privacy; no renderer-owned calculation or invalid redacted row. |
| **8. Explicit CLI and installed Hero** | Wire `--lineage`, context role/flags and explicit primary selection; document usable commands. Depends on 7. | Audit opt-in, context-only ancestry, existing comparison behavior, input-only validate, meaningful exit codes and installed Hero pass. Exercise core inputs and real Parquet where the new role crosses that loader boundary. |
| **9. Bounded adversarial, mutation and scale work** | Resolve remaining graph/resource defects, measure lineage workloads, run a finite meaningful mutation set. Depends on 2-8. | Resource failure is honest; no recursion dependence; 100k sparse graph completes on the designated reference profile; end-to-end lineage is measured; meaningful seeded mutations are killed or remaining gaps explained and corrected. |
| **10. Candidate verification and handoff** | Update public docs/traceability and package to dev4; complete canonical regression, supported candidate matrix and delivery checks; record concise completion and limitations. Depends on 1-9. | Frozen Hero expectations hold, required owners implemented, supported installs and reproducibility verified, no Phase 6 execution or publication implied. Administrative report successors reuse unchanged candidate evidence. |

The existing generation validator uses repeated propagation scans. If the deep-chain/100k workload demonstrates a bottleneck there, Steps 3 or 9 may replace that propagation with a behavior-preserving iterative dependency algorithm. Preserve existing generation semantics and run its direct/dependency-neighbor tests. This narrow allowance does not authorize unrelated input or metric redesign.

## 5. Independent acceptance oracles

### 5.1 Frozen Hero

Keep the six canonical Hero input/expectation files unchanged. Construct current report goldens from their approved values rather than editing the oracle to fit output.

| Quantity | Required value |
|---|---|
| Primary target / loaded records | v2: 8 / v1 plus v2: 16 |
| v1/v2 support | 8 / 5 |
| v1/v2 diversity / retention | 0.875 / 0.75 / 0.625 |
| v2 human/synthetic shares | 0.5 / 0.5 |
| Direct / lineage closure interval | [0.5, 0.5] / [0, 0] |
| Declared / resolved target references | 8 / 8 |
| Cycle detected / unresolved references | false / 0 |
| Distinct supporting external roots | 5 |
| Top root / incidence / share | `v1::v1_01` / 3 / 3/8 |
| Root masses / normalized shares | [3, 2, 1, 1, 1] / 8 |
| Ancestry HHI / effective roots | 0.25 / 4.0 |
| Input observability / lineage execution | Level 4 / completed when requested |
| Shared-ancestry proxy | present, with topological limitations |

Required unavailable conclusions remain model-performance decline, causal ancestor effect, universal integrity and universal collapse prediction. No simulation runs by default.

### 5.2 Proposed multi-root and uncertainty oracle

Use four ungrounded target records in a later version. Context anchors a and b are explicitly parentless and grounded; context u is explicitly parentless with unknown grounding. Target t1 has parent a; t2 has parents a,b; t3 has explicit empty parents; t4 has parents a,u,and a missing key.

| Quantity | Independent expected value |
|---|---|
| Complete root sets | t1: {a}; t2: {a,b}; t3: {}; t4: unresolved |
| N / G / C / U | 4 / 2 / 1 / 1 |
| Declared/resolved target references | 6 / 5; edge coverage 5/6 |
| Resolved lineage / external ancestry coverage | 3/4 / 1/2 |
| Incidence a,b / shares using N | 2,1 / 1/2,1/4 |
| Fractional masses a,b / normalized weights | 3/2,1/2 / 3/4,1/4 |
| Distinct roots / HHI / effective roots | 2 / 5/8 / 8/5 |
| Lineage lower / upper / width | 1/4 / 1/2 / 1/4 |

Create separate variants removing the missing branch while retaining unknown grounding, and resolving unknown grounding while retaining the missing branch. Either defect independently keeps t4 unresolved. Additional compact fixtures cover carryover, repeated paths, tied ranks, all-closed, all-unresolved, empty targets, cycle components and context/target denominator isolation.

## 6. Verification effort and performance policy

| Change/risk | Gate |
|---|---|
| Documentation or non-authoritative metadata | Formatting and affected consistency only |
| Graph/root/math implementation | Affected unit/oracle tests plus resolver, generation or bounds neighbors |
| Input role, public schema, API/CLI or privacy boundary | Relevant integration, compatibility and boundary regression |
| Stable PR candidate | Complete canonical regression and supported OS/Python/dependency matrix |
| Release/delivery candidate | Candidate checks plus build, wheel/sdist, clean install, canonical examples, reproducibility and required security checks |
| Administrative successor with unchanged executable/authoritative bytes | Direct document consistency and evidence reuse; no automatic matrix rerun |

Keep Ubuntu/Windows, Python 3.11/3.12, current/minimum dependency coverage and a real optional-Parquet profile. Adapt existing workflow triggers or dispatch so ordinary implementation updates use the affected gate and a stable candidate receives the full matrix. Reuse existing jobs instead of creating parallel governance workflows.

Run the expensive 100,000-record sparse lineage benchmark on one designated reference profile; use bounded structural cases across the compatibility matrix. Preserve the required actual 100k execution without multiplying it across every environment. Candidate failures require rerunning affected gates; unchanged successful environments may be reused only when their tested candidate remains applicable and that relationship is clear.

Measure elapsed time, peak RSS, graph size, target/context counts, total root memberships and output size. Test a deep sparse chain and a small high-fan-in graph, because root-set growth can dominate graph traversal. Include at least one full CLI lineage measurement through report serialization. Kernel timing alone cannot establish end-to-end performance.

The existing Hero target is under five seconds on its stated reference environment, including input loading, validation, observability, required metrics and JSON/Markdown. Measure it afresh with lineage enabled. The sparse-lineage 100k requirement has no approved hard wall-time/RSS SLA. Establish a reproducible baseline and a measured operational CI timeout; an execution timeout is not a product performance target.

Phase 4's metadata-only 100k audit took approximately 1,362.47 seconds and 7,640,743,936 bytes peak RSS. It did not execute general ancestry. Use that result to understand inherited report overhead, not to claim Phase 5 performance. A >20% time or >50% memory regression on a comparable workload requires review; changed workloads must be labeled. Reuse the existing scope pooling and avoid duplicating per-record graph evidence across report sections.

Bound mutation work to meaningful deterministic defects: wrong N versus G denominator, set union replaced by duplicate counting, carryover minted as a root, unknown treated as closed, omitted cycle propagation, reversed bounds and incorrect HHI inversion. Record the attempted mutation and whether a current test detects it in the existing validation report. No permanent mutation registry or test-count target is required.

## 7. Change scope and completion boundary

Expected implementation locations are `lineage/`, narrowly shared models/config/errors, input-role adapters, bounded parent-result retention and necessary generation propagation, lineage branches of bounds, result/report assembly, JSON/Markdown, CLI, config/report schemas and their packaged mirrors. Relevant fixtures, tests, public docs, existing verification tooling and version declarations may change. These are ownership boundaries, not a new hash-based file authorization system.

Do not change unrelated mathematical kernels, normalization semantics, direct provenance definitions or theory-source documents. Preserve frozen Phase 0 files. Approved Phase 5 clarifications are additive decisions with source references. An actual conflict or newly required independent-input evidence schema is surfaced before dependent implementation, with the affected step identified.

Phase 5 is complete when its required owners, Hero and advanced oracles, privacy/resource boundaries, installed CLI, candidate compatibility and delivery checks pass, and limitations accurately describe partial evidence and topological meaning. Completion records identify the tested candidate and actual results without requiring historical implementation forms to execute forever.

The handoff leaves Phase 6A and Phase 6B explicitly deferred. It does not merge a PR, tag a release, publish a package or claim final v0.1 completion. Future verification growth should primarily follow new product capabilities.

## 8. Source basis for review

Repository-relative references below identify the existing authority; they are not additional executable approval artifacts.

- `PROJECT_INSTRUCTIONS.md`, Phase 5 and lineage/ancestry rules; section 4.4 authority order.
- `V0.1_PRODUCT_SPEC.md`, phase sequence and lineage requirements.
- `PHASE_3_DECISIONS.md`, P3-D01 scope reservation.
- `DEFINITIONS_AND_UNITS.md`, strict ancestry, roots, incidence, mass/concentration, coverage and bounds.
- `DATA_AND_PROVENANCE_SPEC.md`, sections 11.7-11.10 and version-order rules.
- `THEORY_TO_CODE_TRACEABILITY.md`, Phase 5 owners T4/T6/PR-008/PR-009/T3.
- `REPOSITORY_ARCHITECTURE.md`, lineage ownership and phase responsibilities.
- `OBSERVABILITY_AND_REPORTING.md`, typed evidence, explicit unavailable states and interpretive boundaries.
- `VALIDATION_PLAN.md`, sections 61.1, 62.3 and 81; `SUCCESS_CRITERIA.md`.
- `examples/hero/EXPECTED_OUTPUTS.md`, frozen full-product Hero expectations.
- `PHASE_4_COMPLETION.md`, `PHASE_4_VALIDATION_REPORT.md`, `PHASE_4_ARCHITECTURE_COMPLIANCE_REPORT.md` and accepted candidate evidence.
- User instruction: Verification Governance and Complexity Control, supplied during Phase 4.
