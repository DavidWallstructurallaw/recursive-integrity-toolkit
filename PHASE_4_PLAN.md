# PHASE_4_PLAN

## Document control

| Field | Value |
|---|---|
| Project | Recursive Integrity Toolkit |
| Target product | v0.1 |
| Phase | Phase 4: Reports and Audit CLI |
| Document version | 1.0 |
| Planning date | 2026-09-18 |
| Status | DRAFT FOR THEORY OWNER APPROVAL |
| Theory Owner | Xiangyu Guo |
| Accepted starting commit | `e3ffb8c0a88bfe31f669f9662d9b5213da628b3a` |
| Accepted source tree | `e2a25f8cfdc66c3317809c479f80fdae162e6ba9` |
| Accepted tests tree | `6ab22cb9197a8f094f455b29a07a851062bb26c9` |
| Baseline branch | `phase3-metrics` |
| Proposed implementation branch | `phase4-reports-cli`, created from the accepted commit after Step 1 authorization |
| Baseline package version | `0.1.0.dev2` |
| Proposed completed-phase version | `0.1.0.dev3` |
| Implementation authorized by this planning request | None |
| Repository changes performed by this planning task | None |
| Merge, release tag or package publication authorized | No |
| Next action | Review this plan and its P4-D decisions; then authorize an execution step |

This plan is the sole deliverable of the current task. The repository remains at the accepted Phase 3 commit. Planning does not start Phase 4 implementation, create its branch, change tests or publish a package.

All P4-D decisions below are proposed. Approval of this plan includes its expressly listed contract decisions and maintenance boundaries unless the Theory Owner states exceptions. Execution remains one explicitly authorized step at a time, following the established project workflow. Plan approval alone does not direct automatic execution of all eleven steps.

## 1. Verified starting point

### 1.1 Baseline identity and historical evidence

The local checkout was inspected during planning. HEAD and tree match the accepted identities above; the working tree is clean. All sixteen files in `PHASE_0_APPROVAL.md` match their approved SHA-256 values. There are 222 tracked files and 40 Python package modules. No new full test run was performed merely to draft this plan.

| Property | Accepted Phase 3 evidence |
|---|---|
| Core suite | 2,489 passed |
| Real-PyArrow suite | 2,492 passed, including three real-Parquet cases |
| Mathematical oracle | All 20 frozen cases executed |
| Platform/dependency matrix | Ubuntu and Windows, Python 3.11 and 3.12, current and minimum compatible dependencies |
| Final CI | Four workflow roles, twelve successful jobs on the final commit |
| Runtime layout | 40 modules; 16 protected placeholders |
| Packaging | Wheel, sdist, isolated installed checks and one-root source archive verified |
| Current input behavior | `validate_bundle(...)` performs ingestion, validation and observability only |
| Current calculation behavior | Explicitly called Phase 3 kernels; no public report assembly or audit CLI |
| Current CLI | Help, `version` and `--version` only |
| Deferred stages | Phase 5 graph/ancestry; Phase 6A full longitudinal orchestration; Phase 6B experiment/reopening orchestration |

These are historical accepted results from the Phase 3 completion/validation records and final Step 11 receipt. They are a preservation baseline, not claims that Phase 4 has passed. The final receipt distinguishes remote job logs from locally rebuilt artifacts because hosted binary retrieval returned HTTP 403. Preserve that distinction in future evidence.

### 1.2 Authority and source basis

Apply `PROJECT_INSTRUCTIONS.md` section 4.4: exact behavior follows `SPEC_AUDIT.md`, approved UD decisions, the theory-source map and the approved product specifications in their recorded order. Theory publications govern conceptual meaning. A later supplied paper does not silently add a metric or expand the approved phase.

The Phase 4 primary owners are PR-012, PR-013, PR-014, PR-015, PR-016 and PR-018. Existing input and mathematical owners supply validated evidence; their definitions remain frozen. P4-D identifiers supplement the approved decisions and do not replace UD, T, TM, PR or F identifiers.

This plan is grounded in the current repository's reporting, architecture, validation, privacy and product specifications, its accepted Phase 3 control files, actual report/CLI placeholders, package declarations and tests. It introduces no new interpretation of the attached theory papers and no new mathematical formula.

### 1.3 Inherited documentation discrepancy

At the accepted commit, the README Python example asserts v2 support `3` and diversity `0.625`. The unchanged Hero oracle and Phase 3 calculations require support `5` and diversity `0.75`. Step 11 of this plan permits correcting these two documentation assertions and executing the corrected example. The earlier delivery's claim about README execution cannot establish the correctness of these particular committed assertions. No oracle or calculation should be changed to match them.

## 2. Objective and boundaries

Phase 4 turns validated input evidence and existing calculation results into a local, inspectable audit: a canonical result, required JSON and Markdown reports, explicit limitations, privacy controls and a working command-line interface.

| Required delivery | Boundary |
|---|---|
| Canonical audit result and detailed report schema | Stable public field ownership, five evidence classes, finite numbers, explicit null reasons |
| Evidence assembly | Adapt existing results; preserve scopes, denominators, units, assumptions and errors |
| JSON and Markdown | Same canonical result, twelve ordered sections, no renderer-owned mathematics |
| Redacted mode | Post-calculation transformation, consistent identifiers, safe diagnostics |
| `audit`, `validate`, `example`, `version` | Local explicit inputs; thin orchestration; no network or plugins |
| One explicit pair | Existing Phase 3 comparison kernel only, subject to P4-D03 |
| Installed example | Frozen Hero resources, usable outside a source checkout |
| Validation and delivery | Report goldens, full regression, privacy/no-network tests, performance, builds and evidence |

Excluded: HTML implementation; graph construction/traversal and new cycle analysis; ancestry HHI/effective roots/lineage exposure; automatic version discovery or adjacent-pair sequences; provenance/lineage trajectories; relative-change formula F-019; model-performance analysis; CLI simulation/scenario workflows; external reopening; semantic inference; universal scores; external adapters; cloud service; telemetry; new runtime dependencies.

Existing Phase 3 simulations, weighted companions and directed-map results may be serialized when explicitly supplied as valid typed results to the assembly API. This does not authorize running those workflows from the Phase 4 CLI. Unsupported explicit requests must receive an actionable error, rather than be silently ignored.

## 3. Decisions proposed for approval

Each decision identifies the practical issue, selected resolution and relevant authority. A rejected or excepted decision blocks only the dependent work. Record actual approval in `PHASE_4_DECISIONS.md`; never mark it approved merely because the plan exists.

### P4-D01. Separate input observability from executed analysis

**Issue:** Full-product Hero reporting requires lineage results, while Phase 5 owns their implementation. The accepted Phase 2 classifier already assesses Hero inputs at Level 4, with lineage and dataset-longitudinal input eligibility available.

**Resolution:** Preserve `observability.maximum_level` and existing capability `status` as input-evidence assessments. Add a report-level `execution_status` to each capability, using `completed`, `partial`, `not_requested`, `deferred` or `failed`, with scope and reasons. This field describes performed work; it does not reinterpret the Phase 2 classifier. For dataset longitudinal, even a completed explicit-pair calculation must name its limited operations; unimplemented change families remain disclosed.

The Phase 4 Hero retains Level 4. Its lineage execution is `deferred`, with reasons and explicit unavailable analysis entries. Do not fabricate lineage closure, root counts, HHI, graph-cycle traversal results or ancestry proxies. Existing validation observations may be reported with their actual provenance and bounded method; an earlier-version ordering certificate must not be relabeled as general graph traversal.

Use a new, stage-specific Hero report oracle. Keep the six canonical Hero files and their full future-product expectations unchanged. Phase 4 acceptance establishes its report/CLI contract, not final v0.1 or Phase 5/6 acceptance.

**Authority:** Project instructions section 6; reporting sections 4-5, 15, 28 and 36; Phase 3 decisions P3-D01/P3-D03; traceability section 47. Change classes A/C.

### P4-D02. Resolve the two capability locations explicitly

**Conflict ID:** P4-C01. `SPEC_AUDIT.md` B02 calls for `observability.capabilities`; reporting sections 7-8, the field registry and the current schema require top-level `capabilities`.

**Resolution:** Retain top-level `capabilities` as the canonical matrix and provide `observability.capabilities` as an exact, generated compatibility mirror. Construct both from one immutable source. Runtime validation and tests reject unequal mirrors. Render one matrix in Markdown. Do not create two independently mutable interpretations. Keep the twelve top-level keys and `report_schema_version: "1.0"`.

This is an explicit additive reconciliation of the frozen sources. It does not rewrite the Phase 0 files. Before approval, the conflict is blocking for schema implementation. Change class A/C, related UD-003/004/019.

### P4-D03. Bound explicit-pair CLI execution

Wire at most one expressly requested earlier/later pair into `compare_support(...)`. Require one selected version per side, a retained explicit chronology and an explicit common state-meaning declaration. Shared representation metadata alone does not prove semantic equivalence. The CLI's supported pair uses one identical declared representation and one shared literal state-meaning declaration; arbitrary maps remain outside the CLI.

`--compare` supplies the earlier dataset and `--records` the later dataset only when their selected version IDs are consistent with the declared order. Reject ambiguous multi-version sides, missing order, contradictory chronology or incompatible representation. Preserve usable single-version results with errors when only the requested pair fails. Do not infer order from names, argument order or cached capability flags.

Allowed pair outputs: F-005 support delta, F-006 retention, F-018 diversity delta, original positive-support differences and loss/added counts already supplied by the accepted kernel. No new delta formula is implemented by the CLI, assembly or renderer.

**Authority:** Phase 3 P3-D03 and accepted Step 9; project instructions sections 10-11; product sections 16/19. Change class A/C.

### P4-D04. Canonical result, strict schema and dependency policy

Use existing `result.py` for report-local immutable contracts, including all five reporting evidence classes. Do not extend the Phase 3 calculation enum merely to accommodate proxies and unavailable conclusions. Use explicit public-field adapters, never a generic dump of internal dataclasses or mappings.

Expand `schemas/report.schema.json` in place using Draft 2020-12. Specify envelope variants, finite numerical values, exact statuses/classes, required reasons and typed sections. Keep the five root schema filenames. Enforce semantic conditions such as equal capability mirrors and interval consistency in canonical-result validation as well as tests.

Runtime construction and serialization use standard-library checks. `jsonschema` remains test/dev-only. Test every produced report against the local schema without fetching `$schema`, `$id` or remote references. No runtime dependency or build-backend change is proposed.

**Authority:** reporting sections 8-10/27/34; architecture reporting ownership; dependency strategy. Change classes A/C.

### P4-D05. Privacy transformation and deterministic identifiers

Standard output excludes raw content, notes, full embeddings, secrets and complete configuration dumps. Redacted output additionally removes full paths, content references, source/evidence URIs and raw content hashes; it transforms potentially sensitive dataset/record/state identifiers consistently in all nested locations, including messages and comparison details.

Support redacted record-ID modes `preserve`, `hash` and `omit`; `hash` is the redacted default. An explicit `preserve` selection applies only to the declared record-ID field, not to paths, content, notes or other sensitive fields. Use domain-separated HMAC-SHA-256 pseudonyms over unambiguous canonical encodings. A fresh secret by default gives run-scoped consistency; an explicitly supplied local secret file permits declared cross-run consistency. Never emit the secret, its file path or a reversible mapping. Record the algorithm and stability scope, not key material. No raw secret CLI argument.

Redaction follows calculation and precedes every renderer and diagnostic sink. Preserve aggregate numerical values, denominators, classes and availability; record any intentionally omitted identity-bearing details as redaction, without treating them as missing evidence. This is identifier/content protection, with no claim of statistical anonymity or small-cell suppression.

Use a fixed test-only secret for deterministic redacted goldens and separate tests for default unlinkability. Forbid metric recomputation from redacted values.

**Authority:** reporting section 24; privacy sections 3-13/17-22; PR-015/016. Change classes A/C/D.

### P4-D06. CLI options, configuration and exit contract

Implement `rit audit`, `rit validate`, `rit example`, existing `rit version`, `--version`, module invocation and the existing `recursive-integrity` entry point. Only `--records` is required for `audit` and `validate`. Default output is the local `./rit-report` directory, with no overwrite of existing report targets. Print final report paths on successful publication.

Phase 4 options are restricted to:

| Group | Options / meaning |
|---|---|
| Local inputs | `--records`, `--provenance`, at most one `--compare`, `--config`, `--schema-mapping`, `--version-order` |
| Pair declaration | `--state-semantics TEXT`, explicitly applied to both sides under the same representation |
| Missing state | `--missing-state-id TEXT`, required only when the declared representation policy is `explicit_missing_state` |
| Reports | `--out DIR`, `--redacted`, `--record-ids preserve\|hash\|omit`, `--id-salt-file PATH` |
| Validation | `--strict`; existing configured strict warning codes remain authoritative |
| Tail | `--tail-rule singleton_count\|count_at_or_below\|frequency_at_or_below` and a rule-appropriate `--tail-threshold`; no default tail threshold |
| Example | `rit example --out DIR`, with optional redacted output |

Use existing config fields for representation, privacy, strictness, order, resource limits and declared input roles. Preserve the current error on competing CLI/config singleton declarations; do not silently override configuration. Add a Phase 4 adapter for `output` that accepts only `directory`, `record_id_mode` and `id_salt_file`, validates their types and conflicts, and rejects unknown keys before writes. Preserve existing Phase 2 `resolve_config` and `validate_bundle` semantics. The general Phase 2 output mapping remains inert when those APIs are called directly.

Missing representation permits input/provenance reporting with explicit unavailable representation-dependent analyses. No implicit topic, content-hash or semantic fallback. An explicit missing-state policy requires the caller-supplied `--missing-state-id`, passed to the existing collision-checking representation API; another policy rejects this option. No sentinel is invented. Tail requests require the necessary representation: `singleton_count` rejects a threshold, `count_at_or_below` requires a nonnegative integer, and `frequency_at_or_below` requires a finite value within `[0,1]`. The `state_list` tail rule remains available through the existing Python API and typed-result assembly, with no CLI activation in this phase. Explicit unsupported simulation, mapping or debug-output activation fails as configuration error. Data containing weights remains eligible for disclosed unweighted calculations; this CLI does not opt into weights automatically. Local content-reference resolution is not activated by report generation; existing explicitly callable Phase 2 APIs remain available.

For calculations, each records input must contain one dataset version. Without a scope-selection option, a records-only file containing multiple versions is an input error with any valid input inventory preserved; never pool versions or select one implicitly. An empty input retains its existing empty-scope/unavailable semantics and creates no invented version ID. Input-only `validate` may still report the supplied multiversion bundle without calculations.

`validate` produces the required report structure with input/validation evidence and empty analytical sections. It never invokes calculations or simulations. Help/version never load inputs, render reports or import optional analytical dependencies for execution.

| Exit | Meaning |
|---|---|
| 0 | Requested supported work completed; no error-severity diagnostics |
| 1 | Input/validation or output-I/O failure; includes an error-bearing partial audit |
| 2 | Invalid invocation/configuration or an explicitly unsupported requested feature |
| 3 | Existing validated lineage-family error, without enabling Phase 5 graph work |
| 4 | Internal software/invariant failure |

Choose exit deterministically with precedence `4 > 2 > 3 > 1 > 0` when multiple classes remain. Warnings alone return 0 unless strict promotion applies. `run_status` is `complete`, `partial` or `failed`: partial means useful evidence survived an attempted-family failure, and returns nonzero. Known deferred/optional unavailable capabilities do not by themselves make a successful in-scope audit partial. On fatal failure, emit a schema-conforming error-only report when the output destination is safe and writable; otherwise emit safe stderr and the correct nonzero exit.

**Authority:** product section 19; reporting section 31; existing config/validation contracts. Change classes A/C/D.

### P4-D07. Safe publication of both required reports

Use `report.json` and `report.md` under the resolved output directory. Validate destinations before file resolution that could contact remote shares. Reject URLs, UNC/device paths, input-output collisions, symlink/hardlink aliases and unsafe existing targets. Never rewrite an input or silently replace an existing report. Directory creation is limited to the explicitly resolved output location.

Validate the canonical result and render both reports before publication. Stage bytes in a private temporary location under the destination filesystem, then publish without overwriting. Clean temporary files on handled failures. Two filenames do not provide a cross-platform transactional commit: report an incomplete publication honestly, clean only files created by this invocation where safe, and never announce success before both mandatory outputs are complete. Failure injection must cover disk/write/rename failures and a target appearing during publication. Document supported-platform guarantees and residual concurrent filesystem limitations.

**Authority:** privacy sections 5/8/9; product section 19; PR-013/015. Change classes C/D.

### P4-D08. Goldens, stable metadata and performance

Keep Phase 3 mathematical oracles unchanged. Create independent Phase 4 report expectations from the field registry, frozen Hero values and authored edge cases. Generated actual output may be a review candidate; it must not automatically become the expected answer.

Golden normalization is an exact field-path allowlist for run IDs, start/completion timestamps, duration, environment/platform metadata and test-root path prefixes. Do not normalize metrics, scopes, evidence classes, reasons, availability, warnings, configuration meaning or unavailable conclusions. Content/config hashes remain checked against the relevant input or independently normalized declared configuration. Do not normalize every field named `id` or `value` recursively.

Record SHA-256 input hashes and a normalized resolved-config hash. Hashes describe supplied bytes/configuration, not authenticity. Persist only an allowlisted safe summary of resolved options. Secrets are excluded; disclose the exclusion. The `command` field must be a sanitized reconstruction, not raw argv containing private paths/values in redacted mode. Runtime network count describes toolkit-managed outbound operations, with scope disclosed; blocked socket/DNS/URL execution tests provide separate no-network evidence. Do not claim an operating-system-wide network monitor.

Measure the complete Hero path through writing both reports. Target: under five seconds on recorded common-laptop/reference CPU hardware. CI/container timings are observations, not proof of all laptop performance. A reproducible miss requires investigation and recorded acceptance or a scoped performance exception; never silently waive the target. Record 100,000-row end-to-end metadata results without inventing a fixed throughput threshold. Record tracing overhead, Python allocation peak versus RSS, inputs and environment. Comparable >20% runtime or >50% memory regressions trigger review under the validation plan.

**Authority:** PR-016; reporting section 32; validation sections 51/58/61-63/86; product section 20. Change classes A/C.

### P4-D09. Installed resources, version and optional HTML

Keep the 40 Python modules. Leave `reports/html_report.py` as a placeholder. Implement the existing modules rather than adding a new orchestration framework.

Package exact copies of the six canonical Hero files and the current report schema under `src/recursive_integrity_toolkit/data/`; read them with `importlib.resources`. The approved package-data declaration is the only non-version packaging change. Copies must be byte-equal to their named canonical sources. No download, generated substitute data or runtime dependency on the checkout.

`rit example --out DIR` creates a new example workspace with `inputs/` and `reports/`, refuses overwrite, and runs the same audit path with the documented Hero order and literal state-meaning declaration. It reports Phase 4 limitations. The packaged `EXPECTED_OUTPUTS.md` remains the full-product reference, clearly distinguished from actual Phase 4 output.

Keep version `0.1.0.dev2` until final Step 11; then change only the two version declarations to `0.1.0.dev3` and their listed test/metadata expectations. A dev3 milestone is not an official stable release. No merge, tag or publication follows automatically.

**Authority:** product sections 19/23; architecture; UD-019/025/026/032/036. Change classes C/E.

### P4-D10. Preserve historical checks while opening current work

Freeze the accepted Phase 3 commit, source/test trees, control records, formulas, input behavior and oracle bytes. Add a dedicated `phase3_final_snapshot` fixture, verified against the pinned commit/tree. Do not repurpose global `repo_root`, `package_root`, subprocess or placeholder fixtures.

Rebind only the exact obsolete stage assertions in section 7 to the snapshot, preserving names, parameters and substantive assertions. Keep current mathematical, input and security behavior tests on Phase 4 HEAD. Add active Phase 4 checks for every newly opened module and migrated guarantee. Record exact transformations and verify their allowed differences against the frozen files.

Preserve old Phase 3 audit functions/constants and their historical semantics. Add explicit Phase 4 dispatch/control logic; do not change a global Phase 3 active-step constant to make HEAD pass. A changed count is not proof of preserved tests: reconcile node identities and parameterizations in core and real-Parquet collections.

**Authority:** project testing/change-control rules; Phase 3 P3-D09 and Step 11 approved exceptions. Change class C.

### P4-D11. Review and completion authority

The user remains Theory Owner and approval authority. Technical, mathematical-transcription, privacy and security review may be performed in consolidated assistant roles, with actual checks recorded. Delegated assistant review is not independent human certification.

Phase 4 completion requires the gates in section 10 and explicit implementation acceptance. New completion records appear only during finalization, with truthful pending status until evidence passes. Final acceptance-record changes require a fresh run on the final source commit. Preserve failures and fixes in the record. No claim of empirical theory validation, certified provenance truth, general security certification or production readiness follows from passing the phase.

**Authority:** governance sections 3/5/7/12/14; project phase stops. Change classes C/E.

## 4. Public report contract

### 4.1 Required sections

| Order | JSON key | Markdown section |
|---:|---|---|
| 1 | `run` | Run metadata |
| 2 | `inputs` | Input inventory |
| 3 | `observability` | Observability summary |
| 4 | `capabilities` | Capability matrix |
| 5 | `observed_facts` | Observed facts |
| 6 | `derived_metrics` | Derived metrics |
| 7 | `proxy_signals` | Proxy signals |
| 8 | `simulations` | Simulations |
| 9 | `unavailable_conclusions` | Unavailable conclusions |
| 10 | `recommended_next_metadata` | Recommended next metadata |
| 11 | `warnings` | Warnings |
| 12 | `errors` | Errors |

Every section remains present, including failed/validation-only runs. The first eight sections are objects; the last four are arrays. Empty values use `{}` or `[]` accordingly. Markdown begins with `# Recursive Integrity Audit Report`. State units, denominators and rounding; null renders as unavailable with a reason, never numerical zero. Preserve exact numerical JSON values within the accepted floating-point policy; human display rounding does not overwrite them.

### 4.2 Envelopes and traceability

Step 2 freezes the complete path registry before adapters emit fields. Every public analytical result has exactly one primary evidence class, status, unit/type, method/formula or explicit product-only rule, owner/trace identifiers, scope, applicable representation, coverage/denominator, assumptions and limitations. Unavailable values carry reason codes and required evidence. Metadata/control fields retain product ownership without pretending to be scientific measurements.

| Family | Public location / primary class | Preserved meaning |
|---|---|---|
| Run/input evidence | `run`, `inputs` | Version, hashes, sanitized config/command, order source, input role/format/size/rows, mappings and exclusions |
| Counts and exact duplicates | `observed_facts.record_counts`, `observed_facts.content.*` | Scoped record counts, exact normalization and duplicate definition |
| Provenance coverage/counts | `observed_facts.provenance.*` | Matched, required-field and grounding coverage remain distinct; supplied declarations are not verified truth |
| Support/diversity | `derived_metrics.support.by_version.*`, `derived_metrics.diversity.by_version.*` | Existing F-001 to F-004, positive support, representation and inclusion/exclusion scope |
| Source shares/direct bounds | Registry-defined provenance/bounds fields under `derived_metrics` | F-007/F-009/F-010, original denominator, unknown/missing distinction, lower/upper/width |
| Tail | `derived_metrics.tail.*` plus observed state-count basis; computed frequencies retain `derived_metric` | Explicit approved rule/threshold, counts, analyzed sample size and deterministic ranking |
| Explicit pair | Registry-defined support/diversity pair fields | Selected ordered versions, F-005/F-006/F-018, lost and added states separately |
| Proxy | `proxy_signals.*` | Named deterministic trigger, cited basis fields, limitation; no universal risk score |
| Supplied scenario results | `simulations.*` | `simulation` and `experimental`, explicit model/parameters/seed where applicable, never empirical forecast |
| Unavailable claims | `unavailable_conclusions[]` | `unavailable_conclusion`, reason, blocking evidence, next metadata and related capability |

Use the exact approved field registry in `THEORY_TO_CODE_TRACEABILITY.md` sections 30-37. Where a Phase 3 companion lacks a frozen public report path, Step 2 must register a scoped additive field with its existing owner and limits; unregistered internals are not exposed. Do not silently rename fields or change denominator families.

Proxies use existing registered presence rules, such as support contraction when the validated explicit-pair delta is negative. Tail interpretation requires its declared threshold. No ancestry proxy is emitted before ancestry computation. No default simulation runs. Recommended next metadata is a deterministic mapping from documented missing evidence and limitations, not automated policy or remediation action.

At minimum, every Hero report explicitly lists `model_performance_decline`, `causal_ancestor_effect`, `universal_integrity` and `universal_collapse_prediction` as unavailable. Deferred implementation reasons must remain distinct from absent input, incompatible representation and conclusions outside product scope.

### 4.3 Module ownership and dependency direction

| Existing module | Phase 4 responsibility |
|---|---|
| `result.py` | Canonical report contracts, field validation, report-local enums |
| `reports/assembly.py` | Explicit result adapters, evidence placement, limitations, recommendations, pure privacy view |
| `reports/json_report.py` | Stable finite JSON serialization only |
| `reports/markdown_report.py` | Ordered safe human rendering only |
| `cli.py` | Parse invocation, select explicit scopes, call accepted validation/calculations, invoke reporting/writes |
| `config.py` | Additive Phase 4 option resolution; preserve inherited parser behavior |
| `utils/hashing.py` | Additive normalized config hash/pseudonym helpers; preserve input hashing |
| `utils/logging.py` | Content-safe diagnostic formatting and sink behavior |
| `utils/paths.py` | Additive output destination/staging/publication helpers; preserve input safety |

Calculation and representation modules never import renderers or CLI. Renderers accept canonical results and perform no ingestion or recalculation. Assembly accepts validated typed results and executes no metric, graph, simulation or filesystem operation. CLI imports computational code lazily where needed; all 40 package imports and help/version remain safe under the existing analytical dependency blockers.

## 5. Protected content and file permissions

### 5.1 Frozen through this phase

- All sixteen Phase 0 authority files and `PHASE_0_APPROVAL.md`.
- All prior phase plans, baselines, decisions, acceptance and completion records.
- All six canonical `examples/hero/` files.
- `tests/golden/phase3_math_cases.json`, `tests/golden/phase3_math_cases.md` and their numerical expectations.
- All Phase 2 input/observability bodies and all Phase 3 metric/representation bodies, including `models.py` and `errors.py`.
- Root schemas other than `schemas/report.schema.json`.
- Direct/optional dependency declarations, build backend, package/entry-point names and the 40-module set.
- Existing HTML, graph, ancestry and other unselected placeholder behavior.

Exceptions are only the exact additive infrastructure functions, resources, schema and version transitions specified here. Existing functions/classes in `config.py`, `utils/hashing.py` and `utils/paths.py` remain preserved; an unavoidable behavioral repair requires its own review before modification. Approved declaration/module-header additions may identify the new owners without changing inherited semantics.

### 5.2 Common maintenance set G

After plan and step authorization, the following exact files may be synchronized for stage checks, current test wiring, traceability, workflow labels and evidence. This is not permission for arbitrary feature edits or assertion weakening.

```text
PHASE_4_BASELINE.json
PHASE_4_DECISIONS.md
scripts/check_traceability.py
scripts/check_spec_consistency.py
scripts/release_check.py
tests/conftest.py
tests/unit/test_phase4_contracts.py
tests/integration/test_phase4_gates.py
tests/integration/test_no_algorithms.py
tests/integration/test_ci_workflows.py
tests/integration/test_repository_structure.py
tests/integration/test_owner_ids.py
tests/integration/test_package_import.py
tests/integration/test_package_install.py
tests/integration/test_optional_dependency.py
tests/integration/test_no_network.py
tests/integration/test_schema_json.py
tests/integration/test_hero_structure.py
tests/integration/test_prohibited_structure.py
tests/integration/test_license_notices.py
.github/workflows/ci.yml
.github/workflows/security.yml
.github/workflows/golden.yml
.github/workflows/release.yml
docs/architecture.md
docs/theory_traceability.md
```

Step 1 copies this approved plan into the implementation branch as an add-only path, records its approved SHA-256 and freezes its bytes. Subsequent plan edits require explicit amendment approval; routine maintenance uses the two Phase 4 control files. Baseline source identities are immutable. Stage permissions advance only with actual authorization and completion evidence; the manifest cannot authorize its own expansion. Keep an independently enforced exact path/operation allowlist and negative mutation tests.

Historical test migration permissions in section 7 are also common only for the listed transformations. All other edits must be named in the step below. Unlisted paths, deletion/renaming, new dependencies, numerical changes or scope expansion require a concrete exception. Report an unexpected boundary conflict before editing it.

## 6. Execution steps

Every step produces a receipt describing its starting/ending commit, changed paths, decisions, commands, tests, failures/fixes, review findings and remaining limitations. Run focused checks during development and the required complete active gate before claiming step acceptance. Stop at the accepted step until the next step is authorized.

### Step 1. Freeze the baseline and activate Phase 4 governance

**Additional paths:** `PHASE_4_PLAN.md` as an add-only approved copy, and the exact historical test files in section 7. No runtime/schema implementation.

1. Verify pinned commit, tree, test identities, authority hashes, Hero and math oracle bytes. Create the branch and record the actual approval of P4-D01 through P4-D11.
2. Create `PHASE_4_BASELINE.json` and `PHASE_4_DECISIONS.md`, with scoped file permissions, protected bytes, migration inventory and phase status.
3. Add verified final-Phase-3 snapshot fixtures and exact historical transformations. Preserve the existing Step 10 snapshot and every inherited test node/parameter.
4. Add Phase 4 audit dispatch and active gate tests, retaining callable historical Phase 3 gate semantics. At this step no new report module behavior is allowed.
5. Wire four workflow roles to the active phase while preserving matrix, read-only permissions and historical evidence checks.

**Acceptance:** full baseline behavior survives; current and historical gates run on their correct trees; negative mutations of formulas/oracles/unopened files/forged approval are rejected. No report generated and no Phase 4 completion record created.

### Step 2. Freeze canonical results and public report fields

**Additional paths:** `src/recursive_integrity_toolkit/result.py`, `schemas/report.schema.json`, `docs/report_schema.md`, `tests/unit/test_PR012_evidence_classes.py`, `tests/unit/test_PR013_report_schema.py`.

Implement report-local immutable contracts and validation, all twelve sections, required metadata, five evidence classes, capability mirror and execution statuses. Write the complete typed field/owner registry and null rules. Reject unknown public result keys and invalid evidence placement; distinguish boolean from numeric input where appropriate. Validate constructors against independent valid/invalid schema fixtures authored within the test files.

**Acceptance:** schema and canonical model agree; zero remains distinct from unavailable; nonfinite numbers and mismatched capability mirrors fail; empty/error-only structures are valid. No adapter computes a metric and no CLI command starts analysis.

### Step 3. Assemble existing evidence, limitations and recommendations

**Additional paths:** `src/recursive_integrity_toolkit/reports/assembly.py`, `docs/report_schema.md`, `tests/unit/test_PR012_evidence_classes.py`, `tests/unit/test_PR014_unavailable.py`, `tests/unit/test_PR018_language.py`, `tests/integration/test_partial_provenance_report.py`, `tests/integration/test_partial_lineage_report.py`.

Add explicit adapters for accepted validation and calculation result types. Preserve original scoping, denominator metadata, independent coverage measures, unknown/missing distinctions, weighted companion labels and scenario assumptions. Add deterministic registered proxies, unavailable conclusions and next-metadata guidance. Preserve useful results alongside validation/family errors. No new graph operation, formula or inference.

**Acceptance:** hand-authored envelopes for full/partial/absent provenance and missing/incompatible representations match expected meaning. Actual calculation values equal the existing kernel results. Forged, mismatched or malformed supplied results cannot create stronger evidence. Supplied simulated values remain in `simulations`; defaults remain empty. Tests for partial lineage exercise disclosure and existing validation only.

### Step 4. Privacy views, run metadata and safe diagnostics

**Additional paths:** `result.py`, `reports/assembly.py`, `utils/hashing.py`, `utils/logging.py`, `config.py` under `src/recursive_integrity_toolkit/`; `docs/privacy.md`, `docs/report_schema.md`, `tests/unit/test_PR015_redaction.py`, `tests/unit/test_PR016_determinism.py`, `tests/unit/test_PR018_language.py`.

Implement P4-D05 privacy transformation, safe run/config summaries, explicit Phase 4 option resolver, identifier modes and content-safe diagnostics. Snapshot inherited helper bodies before additive extensions. Keep fresh-secret behavior distinct from determinism of calculations. Only standard/redacted output is selected for this phase; inherited debug labels do not activate raw-content logging.

**Acceptance:** privacy sentinels embedded in nested identities, labels, paths, URIs, notes, configuration and errors do not leak through the selected privacy mode. Standard mode also excludes raw content/notes/embeddings/secrets. Redaction leaves aggregate values/classes/scopes and error severity intact. Stable test key reproduces pseudonyms; fresh keys separate runs. Existing input/config hashing tests remain current and pass.

### Step 5. JSON and Markdown renderers

**Additional paths:** `src/recursive_integrity_toolkit/reports/json_report.py`, `src/recursive_integrity_toolkit/reports/markdown_report.py`, `tests/unit/test_PR013_report_schema.py`, `tests/unit/test_PR018_language.py`, `tests/unit/test_PR016_determinism.py`, `docs/report_schema.md`.

Serialize only validated canonical results. Use fixed section/key/list ordering and documented display precision. Escape arbitrary text in Markdown tables/headings, raw HTML, link syntax and control sequences so inputs cannot inject toolkit claims or executable markup. Render partial/deferred/experimental status and null reasons visibly. Keep HTML placeholder unchanged.

**Acceptance:** local-schema validation passes; all twelve headings appear in order; JSON/Markdown analytical parity holds; hostile labels and Unicode survive safely; finite-number, interval and unavailable display cases pass. Neither renderer imports or calls metric/input owners.

### Step 6. Output destination and publication safety

**Additional paths:** `src/recursive_integrity_toolkit/utils/paths.py`, `src/recursive_integrity_toolkit/utils/logging.py`, `tests/unit/test_phase4_output_safety.py`, `docs/privacy.md`, `docs/cli.md`.

Implement P4-D07 as additive output helpers. Keep input/content path checks unchanged. Stage both rendered reports, enforce no-overwrite and alias checks, and provide safe publication/error results to CLI callers. Create synthetic filesystem cases directly in temporary test directories.

**Acceptance:** POSIX/Windows path cases, network-looking paths, symlink/alias collisions, read-only destinations, partial write/rename failure and concurrent target creation have truthful outcomes. Input bytes remain unchanged; no source content is retained in temporary logs; no silent successful half-report.

### Step 7. Local `audit` and input-only `validate` commands

**Additional paths:** `src/recursive_integrity_toolkit/cli.py`, `src/recursive_integrity_toolkit/config.py`, `tests/integration/test_cli_validation.py`, `tests/integration/test_phase4_cli.py`, `docs/cli.md`.

Implement P4-D06 parsing, configuration conflict behavior, single-version input-to-report orchestration, optional explicit tail selection, diagnostics and exit/status precedence. Calls go through accepted APIs; formulas stay in their owners. Missing representation produces an honest limited report. Preserve help/version and module/alias invocation. Comparison is explicitly unavailable until Step 8; unsupported requests fail clearly.

**Acceptance:** valid, low-observability, malformed, empty and partial evidence exercise JSON/Markdown/error paths. `validate` is tested with all calculation functions blocked. Help/version and package imports retain the no-analytical-dependency guarantee. Installed ordinary audit works with local external inputs and core dependencies present, with network operations blocked.

### Step 8. Explicit pair and packaged one-command Hero

**Additional paths:** `src/recursive_integrity_toolkit/cli.py`, `src/recursive_integrity_toolkit/config.py`, `pyproject.toml` only for package-data declaration, `tests/integration/test_phase4_cli.py`, `tests/integration/test_hero_end_to_end.py`, `docs/cli.md`, plus these exact resource paths:

```text
src/recursive_integrity_toolkit/data/hero/config.json
src/recursive_integrity_toolkit/data/hero/records_v1.csv
src/recursive_integrity_toolkit/data/hero/records_v2.csv
src/recursive_integrity_toolkit/data/hero/provenance.csv
src/recursive_integrity_toolkit/data/hero/version_order.json
src/recursive_integrity_toolkit/data/hero/EXPECTED_OUTPUTS.md
src/recursive_integrity_toolkit/data/report.schema.json
```

Wire only P4-D03's explicit identity-compatible pair and P4-D09's local packaged example. Each resource is an exact copy of its named canonical source. The packaged report schema must track the authorized root schema bytes. Keep Python module count 40. Both wheel and sdist must support extraction/audit outside the checkout without downloads.

**Acceptance:** Hero target table in section 8 passes through installed CLI; order/meaning/compatibility failures retain honest status; repeated `--compare` or ambiguous multi-version sides fail; no auto-pair/trajectory or lineage computation occurs. Default simulations remain empty. Package resource equality and source input immutability pass.

### Step 9. Independent report goldens and adversarial integration

**Additional paths:** `scripts/build_golden.py`, `scripts/normalize_golden.py`, `tests/golden/phase4_report_cases.md`, `tests/golden/phase4_report_expected.json`, `tests/golden/phase4_hero_report.json`, `tests/golden/phase4_hero_report.md`, `tests/golden/phase4_hero_redacted.json`, `tests/golden/phase4_hero_redacted.md`, `tests/golden/test_phase4_reports.py`, `tests/golden/README.md`, `tests/integration/test_phase4_cli.py`, `tests/integration/test_hero_end_to_end.py`, `tests/integration/test_partial_provenance_report.py`, `tests/integration/test_partial_lineage_report.py`.

Author expectation rationale and freeze golden records before comparing production output. Use fixed injected run metadata/key for literal golden cases. Candidate generation writes to an explicitly requested scratch destination and cannot overwrite accepted fixtures. Normalize only P4-D08 fields. Add negative leakage/language/error-evidence cases and metamorphic checks for row reordering, report format parity and redaction invariance. Privacy/no-network checks cover success and failure paths, not only import.

**Acceptance:** every golden case executes; all original 20 mathematical cases still execute unchanged; forbidden claims, missing sections and normalization of substantive results are rejected. Read both JSON and Markdown artifacts during review. No new expected value is accepted solely because the implementation emitted it.

### Step 10. End-to-end performance and integration evidence

**Additional paths:** `tests/performance/test_hero_runtime.py`, `tests/performance/test_metadata_100k.py`, `tests/performance/README.md`, `tests/integration/test_phase4_cli.py`.

Preserve the original Phase 3 measurement cases and add complete report-path measurements. Measure Hero through published JSON/Markdown, and a reproducible 100,000-record metadata case with observed report size, time and memory scope. Keep the synthetic generator and independent aggregate expectations documented. Benchmark without tracing for the wall-time target, and measure allocation separately with its overhead disclosed. Capture all attempts rather than selecting a best run.

**Acceptance:** actual commands, dependency/platform/CPU context and all measurements are attached to evidence; target misses and comparable regressions are reviewed. Report generation introduces no accidental quadratic comparisons. Do not run or claim the deferred sparse-lineage benchmark. Scope-specific performance acceptance is explicit and does not certify the unimplemented final-product Hero.

### Step 11. Documentation, final verification and delivery

**Additional paths:** `README.md`, `CHANGELOG.md`, `docs/cli.md`, `docs/report_schema.md`, `docs/data_schema.md`, `docs/privacy.md`, `docs/release_process.md`, `pyproject.toml` version literal, `src/recursive_integrity_toolkit/__init__.py` version literal, `PHASE_4_COMPLETION.md`, `PHASE_4_VALIDATION_REPORT.md`, `PHASE_4_ARCHITECTURE_COMPLIANCE_REPORT.md`; version synchronization in section 7.

Correct the inherited README Hero assertions to `5` and `0.75`, document the real commands, data/evidence limits, privacy, error classes and stage-specific Hero. Execute the documented Python and CLI examples. Finalize dev3 and review the entire diff against the baseline and approved scope.

Run the full gate in section 10, collect evidence and prepare completion records. After actual candidate acceptance, record immutable implementation acceptance and rerun every workflow on the final acceptance-record commit. Rebuild final artifacts from that exact commit; identify hashes in external execution metadata/receipt to avoid a circular self-hash.

**Acceptance:** all final gates and artifacts pass; completion status is evidence-backed; main/release state remains separate. Stop before Phase 5 or any merge, tag or publication.

## 7. Exact historical-test maintenance boundary

This section is proposed approval for known stage migrations, avoiding repeated ad hoc exceptions for the same transition. Step 1 must retain exact original node IDs/parameters and register the concrete source-binding changes. It may not convert arbitrary current tests to snapshot tests.

| File | Exact node or assertion scope |
|---|---|
| `tests/unit/test_PR012_evidence_classes.py` | `test_PR012_evidence_classes_owner_and_placeholder` |
| `tests/unit/test_PR013_report_schema.py` | `test_PR013_report_schema_owner_and_placeholder` |
| `tests/unit/test_PR014_unavailable.py` | `test_PR014_unavailable_owner_and_placeholder` |
| `tests/unit/test_PR015_redaction.py` | `test_PR015_redaction_owner_and_placeholder` |
| `tests/unit/test_PR018_language.py` | `test_PR018_language_owner_and_placeholder` |
| `tests/unit/test_PR016_determinism.py` | Only report-placeholder bindings in `test_PR016_ordering_owner_and_no_later_behavior`; ordering/resampling checks remain current |
| `tests/integration/test_no_algorithms.py` | `test_only_step8_authorized_modules_gain_behavior`; `test_protected_phase3_plus_modules_remain_placeholders`; `test_PR003_traceability_script_enforces_step8_scope` |
| `tests/integration/test_phase3_metric_pipeline.py` | `test_phase3_later_implementations_remain_empty`; `test_phase3_step11_rejects_changes_beyond_version_literals`; `test_phase3_step11_test_exceptions_are_exact` |
| `tests/integration/test_cli_validation.py` | `test_cli_help_runs`, preserving its historical Phase 1-help assertion on snapshot and adding current help checks |
| `tests/integration/test_ci_workflows.py` | `test_workflows_preserve_phase_boundary`; `test_phase2_delivery_builds_both_formats_and_tests_installed_wheel`; `test_phase2_hero_workflow_preserves_scaffold_only_golden_boundary` |

The two Step 11 pipeline tests are particularly sensitive: one copies runtime source and checks frozen Phase 3 bytes; the other enforces exact prior test migration bytes. Both must consume pinned Phase 3 source copies when testing historical guarantees. Their original rejection behavior remains exercised.

Other old Phase 3 controls remain current where the referenced protected records/constants are unchanged. Preserve their semantics. If inspection or execution discovers an additional conflicting historical assertion, propose its exact binding change before editing; do not weaken an unrelated guarantee under the maintenance label.

For final dev3 version synchronization only:

- `tests/integration/test_package_install.py::test_package_metadata_and_entry_points`;
- `tests/integration/test_optional_dependency.py::test_core_import_without_optional_pyarrow`;
- `tests/integration/test_cli_validation.py::test_cli_version_runs`;
- active Phase 4 wheel/version checks in `scripts/release_check.py`.

Historical Phase 3 version checks continue to require dev2 on the snapshot. Existing no-dependency installed smoke remains an input/import test, with NumPy/pandas/PyArrow blocked; append separate installed audit checks rather than weakening that test.

## 8. Hero and failure expectations

### 8.1 Stage-specific Hero targets

| Item | Phase 4 expected result |
|---|---|
| Input sizes | v1: 8; v2: 8; provenance: 16 |
| Representation/order | Explicit topic, `hero-topic-v1`, order v1 then v2, literal Hero topic meanings |
| Maximum input observability | 4 |
| Input capability matrix | Preserve canonical accepted statuses; model longitudinal and default intervention simulation unavailable |
| Support | v1 8; v2 5; delta -3; retention 5/8 |
| Diversity | v1 7/8; v2 3/4; delta -1/8 |
| Observed missing states | `battery`, `lizard`, `turtle`, in canonical order |
| v2 provenance coverage | Row, required-field and grounding coverage each 1.0 |
| v2 source shares | Human 1/2; synthetic 1/2; mixed/sensor/unknown/missing each 0 |
| v2 direct exposure | Lower 1/2; upper 1/2; width 0 |
| Pair proxy | Support contraction present, with representation/scope and no functional-failure claim |
| Lineage metrics/proxy | Deferred with explicit reasons, no substituted zero or invented shared-ancestry signal |
| Default simulations | Empty |
| Required unavailable claims | Model decline, causal ancestor effect, universal integrity, universal collapse prediction |
| Network | No toolkit-managed outbound operation; independently blocked-network execution evidence |
| Outputs | Both `report.json` and `report.md`, locally schema-valid and numerically consistent |

The full-product Hero values for lineage interval `[0, 0]`, external roots `5`, root incidence `3`, ancestry HHI `0.25` and effective roots `4.0` remain frozen future targets. They do not appear as calculated Phase 4 results.

### 8.2 Required independent failure/partial cases

Include records-only; no provenance; matched versus missing provenance; invalid required provenance with independently usable content metrics; unknown grounding; empty/all-excluded/singleton scopes; missing representation; incompatible/missing chronology; contradictory state meanings; requested-but-deferred simulation; partial parent validation; malformed input/config; unsafe mapping; duplicate identities; output collisions/failures; hostile labels/control characters; redacted nested errors; nonfinite supplied results; corrupted capability mirror; and installed execution without optional PyArrow.

Check that missing evidence never becomes zero, human/grounded/independent status, a midpoint of an interval or a stronger capability. Family errors survive assembly and rendering and determine exit status. Optional unrequested analyses stay distinguishable from failed requested analyses.

## 9. Test and evidence policy

1. Preserve every inherited test identity and active behavioral guarantee. New report tests add evidence; counts alone do not demonstrate preservation.
2. Keep mathematical oracle bytes and expected tolerances unchanged. No output-based oracle regeneration, silent rounding relaxation, xfail or skip to pass an acceptance gate.
3. Keep input-only validation tests against current HEAD, including scenarios declared eligible without calculation dispatch.
4. Check report schema with the local test dependency; keep runtime/import tests free of accidental schema/dependency downloads.
5. Test renderer and assembly boundaries with calculations, filesystem and network hooks blocked as appropriate.
6. Test privacy in JSON, Markdown, stdout, stderr, structured errors and retained temporary diagnostics. Preserve input bytes before/after execution.
7. Test no-network installed commands with socket/DNS/URL access intercepted; include metadata containing remote-looking URIs and all supported failure paths.
8. Keep subprocesses confined to maintainer build/test tooling. User data, config and template text never become executable code or shell commands.
9. Maintain separate original math expectations, new report expectations, actual outputs and normalization evidence.
10. Run enough targeted checks to resolve concrete risks, then the mandatory phase gates. Do not create redundant tests that merely copy implementation logic.

## 10. Final acceptance gate

Phase 4 is complete only when all applicable gates below pass on the final source commit, with real commands, environment and results retained.

| Gate | Required evidence |
|---|---|
| Scope/authority | Approved decisions; exact diff allowlist; all protected authority, prior-phase, input, metric and oracle bytes preserved |
| Test identity | Reconciled inherited core/Parquet node IDs and parameters; exact approved historical transformations; new current Phase 4 protection |
| Core matrix | Ubuntu/Windows x Python 3.11/3.12 x current/minimum compatible dependencies, complete current suite |
| Minimum environment | NumPy 2.0.0 / pandas 2.2.2; successful install and `pip check`; literal pandas 2.2.0 conflict remains documented |
| Optional dependency | Actual PyArrow absence in core checks; actual PyArrow presence and all three real-Parquet tests in extra-enabled suite |
| Mathematical integrity | Original 20 cases executed unchanged; no renderer/CLI formulas |
| Reporting | Full schema, ordered sections, exact evidence placement, null/error/deferred handling, standard/redacted goldens |
| Privacy/security | No raw-content/secret leaks; safe output publication; no-network commands; no execution from input |
| Hero/usability | Installed one-command example and documented audit commands; correct explicit pair and stated Phase 4 limitations |
| Performance | Complete Hero and 100k measured evidence; target assessment and any explicitly accepted limitation |
| Build/install | Wheel and sdist, strict metadata checks, all 40 module imports, isolated installed input smoke plus installed report/example smoke |
| Resources | Packaged Hero and schema equal canonical sources; no checkout-only dependency |
| Archive | One project root, all tracked final source bytes included and compared to final commit; generated run data excluded |
| Workflows | Full CI, security, Hero/goldens, build/delivery; read-only tokens, bounded timeouts, failure propagation, logs and JUnit |
| Reviews | Recorded technical, mathematical-fidelity, public-language and privacy/security findings, with real reviewer roles |
| Final commit | All workflow roles rerun after acceptance-record edits; artifacts regenerated and checksummed from exact final source |

No active failed, errored, skipped or xfailed case can satisfy a required gate. Platform-inapplicable cases must be designed and accounted for explicitly rather than masking a required behavior. Distinguish subset counts from whole-suite counts. Do not claim a future fixed Phase 4 test count in advance.

## 11. Deliverables and stopping conditions

### 11.1 Repository deliverables after execution

- Approved `PHASE_4_PLAN.md`, baseline and decision/migration records.
- Canonical result, detailed schema/field registry, assembly, required renderers and safe CLI/output behavior.
- Updated CLI/privacy/traceability/architecture/user documentation and corrected README example.
- Independent Phase 4 goldens, new tests, preserved historical/current checks, packaged resources and full workflows.
- `PHASE_4_COMPLETION.md`, `PHASE_4_VALIDATION_REPORT.md`, `PHASE_4_ARCHITECTURE_COMPLIANCE_REPORT.md`.

### 11.2 Final execution artifacts

- `recursive-integrity-toolkit-phase4.zip` from the exact final source commit.
- `recursive_integrity_toolkit-0.1.0.dev3-py3-none-any.whl` and `recursive_integrity_toolkit-0.1.0.dev3.tar.gz`.
- Step 11 execution receipt and verification evidence archive, including environment/commands, JUnit, raw logs, test identity reconciliation, schema/golden/privacy checks, performance measurements and SHA-256 manifest.
- Example JSON/Markdown report pairs, standard and redacted, clearly labeled as Phase 4 results.

A hosted-artifact download failure does not become a claim of binary equivalence. Preserve remote status/log evidence and identify independently rebuilt local artifacts separately.

### 11.3 Stop conditions

Stop before the affected mutation for an unapproved source conflict, unlisted path, new dependency, protected-owner repair, changed formula/oracle/denominator, undisclosed evidence-class change, new public metric or later-phase behavior. Stop acceptance for unsafe disclosure, lost diagnostics, failed required checks, missing real optional-dependency evidence, fabricated review or unassessed performance failure.

Complete the authorized concrete work and retain evidence before requesting an additional decision. Ask only about the exact unresolved exception. Previous authorization for a listed migration or decision remains effective and must not be requested again.

After final Phase 4 acceptance, the next phase is Phase 5 planning/authorization. This plan confers no authority to merge main, tag a release, publish a package or start Phase 5/6.

## 12. Approval record

| Item | Current status |
|---|---|
| Plan and P4-D01 through P4-D11 | Proposed |
| Capability-location conflict P4-C01 | Resolution proposed in P4-D02 |
| Stage-specific Hero acceptance | Proposed in P4-D01/P4-D03 |
| Historical-test migrations in section 7 | Proposed, exact scope identified |
| Step 1 execution | Not started; requires explicit instruction |
| Review roles | Assistant planning review completed; implementation acceptance not claimed |
| Exceptions | None recorded yet |

On approval, record the user's actual instruction and any exceptions in `PHASE_4_DECISIONS.md`. Do not forge a date, signature or review. The final implementation reports must distinguish plan approval, step execution, technical acceptance and publication authorization.

## Appendix A. Immutable anchors

| Anchor | Identity |
|---|---|
| Phase 3 final commit | `e3ffb8c0a88bfe31f669f9662d9b5213da628b3a` |
| Phase 3 final tree | `e2a25f8cfdc66c3317809c479f80fdae162e6ba9` |
| Phase 3 tests tree | `6ab22cb9197a8f094f455b29a07a851062bb26c9` |
| Prior Phase 2 commit | `78554993febb01609cb90814cc24cce2012bf7d7` |
| Prior Step 10 commit | `150a2a105e01883672ef0c2300b41b0de3be352e` |
| Math JSON SHA-256 | `b494d50a1a9bd1009c060c998e4cb3c7433d0e8949f73a8d627e538fa38884b2` |
| Math notes SHA-256 | `5f3603ad6ad8f2b1274547f2c239461e7ee8d3b7d552b04d0dd868b862af4044` |

Step 1 derives all additional path hashes and test collections from this exact baseline and verifies the sixteen authority-file hashes against `PHASE_0_APPROVAL.md`. An observed newer branch head does not silently replace these anchors.

## Appendix B. Source and implementation review index

| Source | Relevant passages / inspection points |
|---|---|
| `PROJECT_INSTRUCTIONS.md` | Sections 4-6 authority/conflict/phases; 9 evidence; 13 metrics; 17 privacy; 20-24 tests/reports/Hero |
| `SPEC_AUDIT.md` | B02 capability location and Hero level; dual authority and approved boundaries |
| `UNRESOLVED_DECISIONS.md` | Approved UD-003/004/011/017/019/025/026/027/032/033/035; optional UD-036; deferred UD-031 and other frozen scope decisions |
| `V0.1_PRODUCT_SPEC.md` | Sections 16/18/19/20/23/25: comparisons, reports, CLI, performance, Hero, acceptance |
| `OBSERVABILITY_AND_REPORTING.md` | Sections 3-10, 14-28, 31-36: classes, capabilities, schema, fields, redaction, language, failures and gates |
| `THEORY_TO_CODE_TRACEABILITY.md` | Sections 23-29 reporting owners; 30-37 field registry; 47 Phase 4 requirements |
| `VALIDATION_PLAN.md` | Sections 40-47 report/privacy/language; 51/54/58 goldens/network/determinism; 61-63 performance; 80 Phase 4 gate |
| `PRIVACY_AND_DATA_HANDLING.md` | Sections 3-13 and 17-22: content boundaries, local processing, output, logging, identifiers and rendering |
| `REPOSITORY_ARCHITECTURE.md` | Report/CLI ownership, phase allocation, dependency direction, exact module/schema/Hero layout |
| `GOVERNANCE_AND_HANDOFF.md` | Sections 3/5/7/12/14: roles, changes, gates, review and releases |
| `PHASE_3_PLAN.md`, `PHASE_3_DECISIONS.md` | Approved kernel/stage boundaries and precise historical maintenance exceptions |
| Phase 3 milestone reports and final Step 11 receipt | Final commit/matrix/build evidence, limitations and deferred phases |
| `models.py`, `io/validation.py`, `config.py` | Accepted typed results, input-only pipeline, immutable config and inert output declarations |
| `metrics/`, `representations/` | Existing explicit pure kernels, scope/meaning checks, calculation metadata |
| `result.py`, `reports/`, `cli.py` | Actual placeholders and current help/version-only surface |
| `schemas/report.schema.json`, `docs/report_schema.md` | Current structural-only schema and missing detailed public-field contract |
| `pyproject.toml`, install tests | Core versus test-only dependencies; missing packaged resources; isolated install constraints |
| `scripts/release_check.py`, `check_traceability.py`, named historical tests | Frozen runtime/schema/Oracle guards and exact migration traps |
| `examples/hero/EXPECTED_OUTPUTS.md`, `tests/golden/phase3_math_cases.*` | Unchanged final-product Hero and mathematical expectations |
| `README.md` | Inherited v2 example assertions requiring bounded documentation correction |

End of planning deliverable. No implementation step has been executed.
