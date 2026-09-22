# Phase 4 Decisions and Step 1 Authorization

Status: **PLAN APPROVED; STEP 1 AUTHORIZED; PHASE INCOMPLETE**.

The Theory Owner instructed: `批准，开始 **Phase 4 Step 1**`.
The instruction was received on 2026-09-18 UTC. Execution continued across UTC
midnight. It approves the delivered plan without exceptions and explicitly starts
Step 1. It does not authorize Step 2, a main merge, a tag or publication.

## Frozen planning and implementation anchors

| Item | Identity |
|---|---|
| Approved plan SHA-256 | `5a6d65696720a426630e876d001937b2837d24774fcb6c2bd43b8e09f5ae93f0` |
| Phase 3 final commit | `e3ffb8c0a88bfe31f669f9662d9b5213da628b3a` |
| Phase 3 source tree | `e2a25f8cfdc66c3317809c479f80fdae162e6ba9` |
| Phase 3 tests tree | `6ab22cb9197a8f094f455b29a07a851062bb26c9` |
| Work branch | `phase4-reports-cli` |
| Main observed at authorization | `cfe1bd0941c1125498ac3d9d9ebf3adafa2c2fcb` |
| Current development version | `0.1.0.dev2`, unchanged in Step 1 |

`PHASE_4_PLAN.md` is copied verbatim from the approved deliverable. Its original
draft labels document its state when submitted. This actual approval record
establishes its approved status without rewriting its frozen bytes. Subsequent
amendments require explicit approval. `PHASE_4_BASELINE.json` records current
authorization, independent anchors, path restrictions and baseline file hashes.

## Approved decisions

| Decision | Status | Approved implementation boundary |
|---|---|---|
| P4-D01 | APPROVED | Input observability and executed analysis remain distinct; stage-specific Hero |
| P4-D02 | APPROVED | Canonical top-level capabilities and exact nested compatibility mirror |
| P4-D03 | APPROVED | One explicitly ordered, meaning-declared comparison using the existing kernel |
| P4-D04 | APPROVED | Canonical report contracts, strict local schema, no added runtime dependency |
| P4-D05 | APPROVED | Post-calculation privacy views, scoped HMAC identifiers, no secret emission |
| P4-D06 | APPROVED | Explicit CLI/configuration/exit contract, input-only validate command |
| P4-D07 | APPROVED | Safe no-overwrite publication, honest partial-write failure handling |
| P4-D08 | APPROVED | Independently reviewed report goldens, narrow normalization, measured performance |
| P4-D09 | APPROVED | Frozen packaged resources, deferred HTML, dev3 only at finalization |
| P4-D10 | APPROVED | Exact historical test migrations plus active current-stage protection |
| P4-D11 | APPROVED | Evidence-backed acceptance and disclosed consolidated review roles |

The approval resolves P4-C01 through the specified capability mirror. Scope and
contract approval do not implement those decisions ahead of their authorized
steps. Step 1 activates governance only. All forty runtime modules, five schemas,
six Hero source files, original mathematical oracles and prior phase records stay
byte-for-byte unchanged. The inherited README example discrepancy remains for the
explicitly planned Step 11 documentation correction.

## Step 1 historical-test transitions

Sixteen named nodes in ten files use dedicated pinned Phase 3 fixtures, following
plan section 7. Original names, decorators, parameters and assertion bodies remain
unchanged. The release checker retains an explicit old-to-new source replacement
recipe and verifies the inherited file prefix after only those replacements.
Append-only tests cannot redefine inherited function/constant bindings.

The shared repository/package/subprocess/owner/placeholder fixtures remain
unchanged. Five new fixtures supply the final Phase 3 snapshot and its package,
owner, placeholder and subprocess views only to expressly listed historical
assertions. The snapshot verifies its commit, tree, test tree, regular-file set
and each Git blob before use, then verifies its file set and bytes at teardown.
The existing Step 10 snapshot remains unchanged.

PR-016's ordering and resampling behavior still uses current source; only its
report-placeholder check uses the historical view. Current CLI help, current
runtime byte equality, current workflows and negative Step 1 gate tests maintain
HEAD protection. Mathematical/input/security behavior tests continue on HEAD.

Historical Phase 2/3 maintainer functions and constants remain exact. New Phase 4
dispatch validates its own control and diff rather than repurposing the old
`ACTIVE_STEP` or relaxing a prior runtime digest. Both source-level migrations and
full core/Parquet node identity reconciliation are required; counts alone cannot
establish preservation.

## Verification and handoff policy

Four workflow roles retain the eight-cell core matrix, actual optional-dependency
absence/presence, frozen mathematical tests, security boundaries, builds and
isolated installed checks. The Step 1 build emits an intermediate candidate; it
does not create final Phase 4 completion records, audit reports or new CLI
analysis commands. The package remains dev2.

The assistant performs implementation and consolidated technical, mathematical
fidelity and security-boundary reviews, with delegated assistant review where
useful. The Theory Owner remains the approval authority. No independent human
review or external certification is asserted.

Actual commits, commands, environments, failures/fixes, full regression and remote
workflow outcomes belong in the external Step 1 execution receipt and evidence
archive. This record does not claim an unexecuted check passed. Final Step 1
acceptance is recorded only after its required checks pass on the delivered
commit. Stop before Phase 4 Step 2.

## Step 2 authorization and canonical contract boundary

On 2026-09-19 UTC the Theory Owner instructed: `批准，开始 **Phase 4 Step 2**`.
This instruction advances the approved plan to Step 2. The Step 1 statements above
remain the historical record of their authorization interval. Phase 4 remains
incomplete; Step 3, a main merge, a tag and software publication are not authorized.

The Step 1 local tested commit is `5aa9cd6d06bfffec9cc280a52277aa9152a8627e`.
The corresponding GitHub commit is `a7f3c46d6ca05de36bfcb60f496ebb2d5ab4a37c`.
Both identify source tree `7f8ef492568456bf5d46fb1b7e2631cb9b94e3fd` and tests tree
`2ce77e331a0fc377387735bb55dffd3be630b59c`. Creating the commit through the
GitHub connection changed its commit identity without changing any source bytes.
The remote commit is the independently pinned Step 2 starting point. The original
Phase 3 anchors and all Step 1 functions, controls and test assertions retain their
historical semantics.

Step 2 permits modifications only in the common maintenance set and the five
additional paths named in plan section 6: `result.py`, `report.schema.json`,
`docs/report_schema.md`, PR-012 tests and PR-013 tests. All 31 paths already exist;
no additions, deletions, moves or renames are permitted. Only the report-local
canonical contract module gains runtime behavior and only the report schema may
change. The other 39 runtime modules, four schemas, six Hero files, mathematical
oracles, dependency declarations, development version and module set stay exact.
Report adapters and CLI analysis remain unopened.

### Explicit Step 1 historical bindings proposed before implementation

Five narrowly identified nodes, comprising seven exact source replacements,
consume the verified Step 1 tree where their original Step 1 assertions require it:

| File | Exact node and source binding |
|---|---|
| `tests/unit/test_phase4_contracts.py` | `phase4_control` reads the pinned Step 1 control file. |
| `tests/unit/test_phase4_contracts.py` | `test_phase4_registered_migrations_accept_only_the_approved_inventory` checks Step 1 historical-test bytes after the original sixteen migrations. |
| `tests/integration/test_phase4_gates.py` | `phase4_mutation_tree` copies the pinned Step 1 tree for the unchanged Step 1 positive and negative gate assertions. |
| `tests/integration/test_phase4_gates.py` | `test_phase4_final_snapshot_preserves_all_current_runtime_bytes` compares the Step 1 runtime with final Phase 3. |
| `tests/integration/test_phase4_gates.py` | `test_phase4_active_workflows_preserve_full_matrix_and_use_current_dispatch` checks the pinned Step 1 workflow wiring. |

Names, assertions, parametrization and rejection behavior remain unchanged. The
new session fixture verifies its commit, source tree, tests tree, regular-file set
and each Git blob before use and at teardown. Shared current repository fixtures
and all existing Phase 3 snapshot fixtures remain untouched. Current Step 2 tests
independently require a passing unmodified current tree before testing mutations,
check its own exact active control and workflow wiring, and verify the 39 frozen
runtime modules. Historical mutation tests alone are insufficient evidence that
the new current tree passes.

The new Step 2 append guard retains exact Step 1 prefixes after those seven
registered substitutions. It allows explicitly named Step 2 test/helper functions
and literal pytest parametrization/fixture decorators. It rejects shadowed names,
module-scope imports and assignments, executable decorator/default expressions,
and changes to inherited assertions. The Step 1 append and function-header guards
remain unchanged and callable on the Step 1 snapshot.

New Step 2 maintainer functions preserve all prior maintainer statements. The only
inherited function-body edits are exact CLI dispatcher branches that select the
new Step 2 functions. Old Step 1 dispatch and historical Phase 2/3 entry semantics
remain available. The control file cannot expand its own independently fixed path,
operation, runtime, schema or approval boundary.

### Step 2 verification and evidence

Acceptance requires the complete active core/real-Parquet regressions, inherited
node-identity reconciliation, independent valid and invalid schema/model fixtures,
current positive and negative gates, builds and isolated installation checks, and
all four remote workflow roles on the delivered commit. The artifact remains an
intermediate Step 2 candidate. Actual command outputs, failed attempts and fixes,
remote workflow identities, consolidated review findings and remaining limitations
are retained in the external Step 2 receipt and evidence archive. This record does
not certify a check that has not executed.

## Step 1 acceptance evidence before Step 2 execution

On 2026-09-19 UTC all four required workflow roles completed successfully on
`a7f3c46d6ca05de36bfcb60f496ebb2d5ab4a37c`. Their twelve jobs were individually
checked and all concluded `success`. The source tree exactly matches the locally
verified Step 1 tree identified above. This closes the previously pending remote
Step 1 acceptance gate before applying the Step 2 implementation.

| Workflow role | Run ID | Result |
|---|---|---|
| CI matrix and real Parquet | [35409538446](https://github.com/DavidWallstructurallaw/recursive-integrity-toolkit/actions/runs/35409538446) | Success |
| Hero and mathematical contract | [35409538423](https://github.com/DavidWallstructurallaw/recursive-integrity-toolkit/actions/runs/35409538423) | Success |
| Security boundary | [35409538376](https://github.com/DavidWallstructurallaw/recursive-integrity-toolkit/actions/runs/35409538376) | Success |
| Build and candidate evidence | [35409538478](https://github.com/DavidWallstructurallaw/recursive-integrity-toolkit/actions/runs/35409538478) | Success |

The external Step 2 evidence record retains the remote acceptance JSON, job
results and artifact metadata. Downloading the hosted candidate archive could not
be completed: materializing the connector's temporary download URL returned an
HTTP error. This acceptance uses the observed remote job results and exact source
tree equivalence; it does not claim that hosted archive bytes were downloaded and
independently verified. The previously verified local Step 1 candidate evidence
retains its separate identity.

## Step 2 acceptance before Step 3 execution

Step 2 is accepted at commit `fcea74e2b1858e83cdbfd1b8212d15343d63ff08`,
source tree `c3ce887fd393cfc6c18364546005f2b74a63b746` and tests tree
`9d6ac0cbf3827ab54c7852503d99d442a3796259`. Core and minimum-dependency
regressions each passed 2728 tests; the real-Parquet regression passed 2731.
All inherited identities and all twenty frozen mathematical cases survived.
The package retains 227 tracked source files, forty Python modules and dev2.

All four remote workflow roles and all twelve jobs concluded successfully on that
same commit. The external Step 2 receipt and evidence retain the full command,
environment, failure/fix, identity, raw-log and artifact-metadata records.

| Workflow role | Accepted run | Result |
|---|---|---|
| CI matrix and real Parquet | [35411353402](https://github.com/DavidWallstructurallaw/recursive-integrity-toolkit/actions/runs/35411353402) | Success, nine jobs |
| Hero and mathematical contract | [35411353398](https://github.com/DavidWallstructurallaw/recursive-integrity-toolkit/actions/runs/35411353398) | Success |
| Security boundary | [35411353389](https://github.com/DavidWallstructurallaw/recursive-integrity-toolkit/actions/runs/35411353389) | Success |
| Build and candidate evidence | [35411353380](https://github.com/DavidWallstructurallaw/recursive-integrity-toolkit/actions/runs/35411353380) | Success |

The hosted artifact was checked through its generating job and API metadata; it
was not downloaded. The byte-verified local candidate was created from the same
accepted commit. An API digest is not presented as an independently downloaded
archive checksum.

## Step 3 authorization and assembly boundary

On 2026-09-19 UTC the Theory Owner instructed: `开始 **Phase 4 Step 3**`.
This instruction advances the previously approved plan to Step 3. Earlier stop
statements remain the historical record of their own authorization intervals.
Phase 4 remains incomplete. Step 4, a main merge, a tag and software publication
are not authorized by this step.

The exact allowed set is the twenty-six common maintenance paths and the seven
additional Step 3 paths in the approved plan, for thirty-three existing paths.
Only modifications are permitted. No addition, deletion, rename or mode change
is authorized. The independently enforced permission registry and approval text
cannot be expanded by editing the JSON control document.

Only `src/recursive_integrity_toolkit/reports/assembly.py` gains runtime behavior.
All thirty-nine other runtime modules, all five schemas, the six Hero files,
mathematical oracles, Phase 0 authorities, dependency declarations, version and
module set remain byte-exact to Step 2. This includes the frozen canonical report
contract and public schema established by Step 2. Adapters consume accepted typed
results, preserve their original evidence and scope, disclose unavailable claims
and generate documented deterministic guidance. No metric, graph, simulation,
filesystem or network operation is permitted in assembly. Privacy conversion,
rendering and CLI analysis retain their later-step boundaries.

One exact documentation correction fixes the Step 2 field table's value-type
label for `derived_metrics.provenance.weighted_source_type_masses`: `number`
becomes `category_mass_map`, matching the already frozen canonical contract and
schema. The full old/new row is independently registered. All remaining Step 2
report documentation bytes are preserved before additive Step 3 documentation.
This correction changes neither the public schema nor an analytical value.

### Exact Step 2 historical bindings

Ten named nodes use the verified accepted Step 2 snapshot through thirteen exact
source replacements, recorded in the independent release-checker registry.
Their function names, parameterizations and substantive assertions remain intact.

| File | Exact nodes and changed binding |
|---|---|
| `tests/unit/test_phase4_contracts.py` | `test_phase4_step2_approved_control_keeps_independent_step1_anchors`, `test_phase4_step2_control_rejects_forged_scope_and_stage`, `test_phase4_step2_control_rejects_unapproved_dispatch`, `test_phase4_step2_control_requires_explicit_approval_fields`, `test_phase4_step2_control_cannot_mint_extra_permission`: read the pinned Step 2 control. |
| `tests/unit/test_phase4_contracts.py` | `test_phase4_step2_historical_migrations_are_five_explicit_step1_bindings`, `test_phase4_step2_historical_guard_rejects_assertion_and_binding_weakening`: read the pinned Step 2 migrated test bytes. |
| `tests/integration/test_phase4_gates.py` | `test_phase4_step2_current_runtime_opens_only_the_canonical_result`, `test_phase4_step2_current_workflows_preserve_matrix_and_use_active_dispatch`: inspect the pinned Step 2 runtime and workflows. |
| `tests/integration/test_phase4_gates.py` | `test_phase4_step2_current_snapshot_checks_valid_tree_before_mutations`: copy pinned Step 2 files before applying its original mutations. |

The new `phase4_step2_snapshot` fixture verifies the fixed commit, source tree,
tests tree, regular-file inventory and every Git blob before use and at teardown.
Shared current fixtures and all earlier snapshot fixtures retain their original
bytes. Current input, validation, mathematical and security behavior continues to
run against current source. Current Step 3 gate tests separately verify a passing
unmodified current tree before exercising negative mutations.

The Step 3 test guard allows only the listed historical replacements followed by
new explicitly scoped `test_phase4_step3_` and `phase4_step3_` functions. It rejects
inherited assertion edits, rebinding, module-scope imports or executable values,
and definition-time side effects. Only the named Step 2 snapshot fixture may be
added to `conftest.py`. Existing maintainer functions and constants remain exact,
apart from the registered Step 3 dispatcher additions. Historical Step 1 and
Step 2 commands remain callable with their original meanings and stage inputs.

### Step 3 verification and evidence policy

Acceptance requires independent valid and invalid supplied-result cases, useful
partial-evidence preservation, pure assembly checks, all inherited node identities,
complete current core and real-Parquet regressions, frozen mathematical evidence,
builds and isolated installed-contract/assembly checks. Four remote workflow roles
must pass on the delivered commit. The candidate remains an intermediate Step 3
artifact. No result is called accepted before its required checks execute.

The external Step 3 receipt records actual commits and trees, changed paths,
commands, environments, outcomes, failed attempts and repairs, review findings,
remote evidence and remaining limitations. Technical review is consolidated
assistant review; it does not assert independent human certification, empirical
theory validation or production readiness. Stop after accepted Step 3.

## Step 4 authorization and privacy boundary

On 2026-09-19 UTC the Theory Owner instructed: `继续`.
This instruction follows the delivered and accepted Step 3 receipt and is
interpreted in that context as authorization to execute the next approved step,
Phase 4 Step 4. The quoted instruction is the actual wording, not an invented
explicit step title. Earlier stop statements remain the historical record of
their own authorization intervals. Step 5, a main merge, tags and software
publication are not authorized by this instruction. Phase 4 remains incomplete.

The accepted Step 3 anchor is commit
`974545c456e535ba1e1c5b6bf4ae0ce25bc04b57`, source tree
`15498f3f00d0ce048c3cba2156eb7a44f096ae88`, and tests tree
`17b87858f77ee4413c98cfd76f16f52170246741`. Its final core and real-Parquet
counts were 2876 and 2879. Its four remote workflows and twelve jobs passed on
that exact commit; earlier timeout attempts remain recorded in the Step 3
receipt. The core CI timeout is retained at sixty minutes without dropping tests
or changing historical preservation helpers.

The exact allowed set is the twenty-six common maintenance paths plus the ten
additional Step 4 paths in the approved plan, for thirty-six existing paths.
Only modifications are permitted. No addition, deletion, rename, mode change,
dependency, version or module-set change is approved. The independent checker
defines this permission set; editing the JSON control cannot expand it.

Only `result.py`, `reports/assembly.py`, `config.py`, `utils/hashing.py` and
`utils/logging.py` under `src/recursive_integrity_toolkit/` may gain Step 4
runtime behavior. Inherited helpers remain preserved before additive extensions.
The five root schemas, six Hero files, frozen mathematical oracles, Phase 0
authorities and the other thirty-five runtime modules remain unchanged.
Privacy follows supplied-result assembly and cannot recompute metrics, classify
inputs, activate graph analysis, render reports or start CLI analysis.

P4-D05 selects standard and redacted output. Both exclude raw content, notes,
embeddings, secrets and complete configuration dumps. Redacted views additionally
protect nested identity-bearing values and omit paths, URIs and raw content
hashes. Explicit record-ID preservation applies only to declared record-ID
fields. Domain-separated HMAC-SHA-256 uses canonical encodings, a fresh default
secret or an explicitly supplied local secret file, with algorithm and stability
scope disclosed but no key material, file path or reversible mapping.
Aggregate values, denominators, evidence classes, availability and diagnostic
severity remain intact. This is identifier/content protection without a claim
of statistical anonymity. Existing debug labels do not activate raw logging.

### Exact Step 3 historical bindings

Ten named nodes use the verified accepted Step 3 snapshot through thirteen exact
source replacements, proposed before modification and registered independently
in the release checker. Names, parameterizations and substantive assertions are
preserved.

| File | Exact nodes and changed binding |
|---|---|
| `tests/unit/test_phase4_contracts.py` | `test_phase4_step3_approved_control_keeps_independent_step2_anchors`, `test_phase4_step3_control_rejects_forged_scope_and_stage`, `test_phase4_step3_control_rejects_unapproved_dispatch`, `test_phase4_step3_control_requires_explicit_approval_fields`, `test_phase4_step3_control_cannot_mint_extra_permission`: read the pinned Step 3 control. |
| `tests/unit/test_phase4_contracts.py` | `test_phase4_step3_historical_migrations_preserve_ten_step2_gate_nodes`, `test_phase4_step3_historical_guard_rejects_assertion_and_binding_weakening`: use the pinned Step 3 migrated test bytes as the historical after-state. |
| `tests/integration/test_phase4_gates.py` | `test_phase4_step3_current_runtime_opens_only_assembly_and_freezes_schema`, `test_phase4_step3_current_workflows_preserve_matrix_and_use_active_dispatch`: inspect the pinned Step 3 runtime and workflows. |
| `tests/integration/test_phase4_gates.py` | `test_phase4_step3_current_snapshot_checks_valid_tree_before_mutations`: copy pinned Step 3 files before applying the original mutations. |

The additive `phase4_step3_snapshot` fixture verifies the exact commit, source
and test trees, regular-file inventory and every Git blob before use and at
teardown. Shared current fixtures and all previous snapshots retain their bytes.
Current mathematical, input, configuration and hashing behavior stays on current
source. Separate Step 4 tests verify the valid current tree before negative
mutations and independently exercise privacy and inherited-helper preservation.

The Step 4 checker preserves earlier maintainer definitions and constants, with
only the explicit dispatcher additions. Current source preservation uses a new
helper without modifying or replacing older helpers. Approved runtime additions
are constrained by fixed reviewed AST identities; inherited declarations are
separately checked against the accepted Step 3 AST identities. These identities
are fixed checker data, never learned from the source under inspection.

### Step 4 verification and evidence policy

Acceptance requires nested privacy sentinels through both selected modes, safe
configuration/run summaries and diagnostic success/failure paths, stable-secret
consistency, fresh-secret separation, no analytical recomputation, exact
inherited test identities, complete core/minimum/real-Parquet regressions, frozen
mathematical cases, isolated builds and installed privacy checks. Four remote
workflow roles must pass on the delivered commit. The candidate remains an
intermediate Step 4 artifact; no unexecuted check is recorded as accepted.

The external Step 4 receipt records actual source identities, changed paths,
commands, environments, outcomes, failed attempts and repairs, review findings
and limitations. Technical review is consolidated assistant review, without
asserting independent human certification, empirical theory validation or
production readiness. Stop after accepted Step 4.

## Step 5 authorization and renderer boundary

On 2026-09-20 UTC the Theory Owner instructed: `很好，Phase 4 Step 5 继续`.
This explicitly advances the accepted plan to Step 5. Earlier stop statements
remain the historical record of their own authorization intervals. Phase 4
remains incomplete. Step 6, a main merge, tags and software publication are not
authorized by this instruction.

The accepted Step 4 anchor is commit
`49454a9b162cb8d35e38d1cb1ae32cb208d3a01c`, source tree
`79264d845e08f73ee68e160dea04f7786f18fd0a`, and tests tree
`4aa4ca0b22f8b8c25afe27feeaba713d6f0830bf`. Its accepted core and real-Parquet
counts were 3071 and 3074. Step 5 records this prior implementation identity
separately from its own current implementation and execution evidence.

The exact allowed set is the twenty-six common maintenance paths plus the six
additional Step 5 paths in the approved plan, for thirty-two existing paths.
Only modifications are permitted. No addition, deletion, rename, mode change,
dependency, version or module-set change is approved. The independently enforced
permission registry prevents the control document from expanding its own scope.

Only `reports/json_report.py` and `reports/markdown_report.py` under
`src/recursive_integrity_toolkit/` may gain runtime behavior. The other thirty-eight
runtime modules, all five schemas, six Hero source files, mathematical oracles,
Phase 0 authorities and development version `0.1.0.dev2` remain byte-exact to the
accepted Step 4 source. This includes the canonical model, privacy transformation,
configuration resolver, hashing and diagnostic helpers. The HTML placeholder
remains unchanged. Rendering cannot compute metrics, inspect source inputs,
choose a privacy policy, create identifiers, publish files or start CLI analysis.

### Rendering contract and ordering policy

Both renderers require an exact `SafeReportView` and validate its copied canonical
payload through `validate_report` before serialization. Callers explicitly apply
`privacy_view` first. A dictionary or internal `CanonicalReport` cannot silently
bypass the accepted privacy boundary. No schema, input or metric owner is imported
or executed to render the supplied safe report.

The twelve top-level sections retain their frozen order. Nested object keys use
lexical ordering. Every array preserves the accepted canonical sequence, including
state/probability associations, mappings, comparison direction, trajectories,
diagnostics and recommendation priorities. Section 32's suggested display sorting
does not authorize the renderer to infer a new ranking or independently reorder
paired arrays. Repeated rendering of the same safe view produces identical text;
fresh-key pseudonyms remain a separate Step 4 source of cross-run variation.

JSON preserves finite numerical values without display conversion. Markdown uses
exact integers and shortest round-trip finite-float spelling with original units.
This explicit display precision preserves tiny nonzero values and narrow interval
bounds. Neither percentages nor rounded analytical values are invented. Null
reasons, methods, evidence classes, denominator metadata, limitations and partial,
deferred or experimental status remain visible in the human-readable report.

Arbitrary text is data within fixed toolkit-authored headings and labels. Markdown
escaping covers table separators, link syntax, raw HTML, line breaks and control
sequences while retaining a recoverable representation of hostile labels and
Unicode. Renderer errors use fixed safe text and cannot echo supplied content.
The current renderer APIs return text only. Destination selection and publication
safety remain Step 6 work.

### Exact Step 4 historical bindings

Ten named functions use the verified accepted Step 4 snapshot through thirteen
exact source replacements registered independently in the release checker.
These definitions account for sixty-eight existing parametrized pytest nodes.
Original names, parameterizations and substantive assertions remain intact.

| File | Exact function definitions and changed binding |
|---|---|
| `tests/unit/test_phase4_contracts.py` | `test_phase4_step4_approved_control_keeps_independent_step3_anchors`, `test_phase4_step4_control_rejects_forged_scope_and_stage`, `test_phase4_step4_control_rejects_unapproved_dispatch`, `test_phase4_step4_control_requires_explicit_approval_fields`, `test_phase4_step4_control_cannot_mint_extra_permission`: read the pinned Step 4 control. |
| `tests/unit/test_phase4_contracts.py` | `test_phase4_step4_historical_migrations_preserve_ten_step3_gate_nodes`, `test_phase4_step4_historical_guard_rejects_assertion_and_binding_weakening`: use pinned Step 4 migrated test bytes as the historical after-state. |
| `tests/integration/test_phase4_gates.py` | `test_phase4_step4_current_runtime_opens_only_privacy_metadata_modules_and_freezes_schema`, `test_phase4_step4_current_workflows_preserve_matrix_and_use_active_dispatch`: inspect pinned Step 4 runtime and workflows. |
| `tests/integration/test_phase4_gates.py` | `test_phase4_step4_current_snapshot_checks_valid_tree_before_mutations`: copy pinned Step 4 files before applying its original mutations. |

The additive `phase4_step4_snapshot` verifies the fixed commit, source and test
trees, regular-file inventory and every Git blob before use and at teardown.
Earlier fixtures and maintainer functions retain their source, apart from exact
Step 5 dispatcher additions. Current privacy, configuration, mathematical, input
and security tests continue to execute current runtime code. New Step 5 gate
tests independently accept the unmodified current tree before negative mutations.
Fixed reviewed renderer AST identities constrain imports, calls, declarations and
control flow without importing the renderer under inspection. Gate execution
cannot learn a new accepted AST from that current source.

### Step 5 verification and evidence policy

Acceptance requires independent twelve-section JSON/schema and Markdown cases,
analytical parity, finite-number and interval preservation, deterministic ordering,
hostile-label escaping, status and null-reason visibility, and blocked input,
network and calculation operations. All inherited node identities must remain,
including the five-generation chain from final Phase 3 through accepted Step 4.
Four remote workflow roles retain all eight core combinations, real Parquet,
frozen Hero/math, security and isolated build/installed checks. The existing
sixty-minute core budget is unchanged. Complete local core, minimum-dependency and
real-Parquet suites must pass; no incomplete execution is reported as acceptance.

The external Step 5 receipt records actual source identities, changed paths,
commands, environments, outcomes, failed attempts and repairs, review findings
and limitations. Technical review is consolidated assistant review without
asserting independent human certification, empirical theory validation or
production readiness. Stop after accepted Step 5.

## Phase 4 Step 6 authorization and bounded implementation

User authorization recorded 2026-09-20: Phase 4 Step 6 approved.
The exact user text is `批准开始Phase 4   **Step 6**`.
Accepted Step 5 commit: `c1667179e895a798bba2349960162542efa5ef87`;
source tree: `d83f9fc8e0b569f2d796bd2a83b87422fe350fba`;
test tree: `974f8e65904c24ed4e226996eaf571aab6123965`.
The accepted baseline contains 227 files, 40 runtime modules, 3215 core tests
and 3218 tests with real Parquet. The frozen approved plan is unchanged.

Step 6 implements P4-D07 through additive helpers in `utils/paths.py` and
`utils/logging.py`, with one new `tests/unit/test_phase4_output_safety.py`.
The allowed set is the 26 common G paths plus these three paths and
`docs/privacy.md`, `docs/cli.md`: 31 paths in total. Only the two named runtime
modules open. Their inherited input/content-reference and diagnostic helper
bytes remain unchanged after the module ownership docstring. All five schemas,
38 other runtime modules, dependencies, version, Phase 0 sources, theory mapping,
mathematical oracles, and Hero fixtures remain frozen. CLI execution, Step 7,
main merge, tagging, distribution publication and Phase 4 completion stay closed.

### Publication contract and implementation choice

`publish_reports` accepts an already constructed SafeReportView, an explicit
local output directory, and an explicit list/tuple of caller input paths.
It validates path spellings before filesystem inspection and completes both pure
renderers before creating the output leaf directory or private staging directory.
Both UTF-8 payloads must be fully written and file-fsynced before publication.
The operation refuses existing target files, directories, hard links and symbolic
links, and never follows an accepted symbolic-link/reparse-point ancestor.
Inputs are checked as paths without reading their contents. Missing declared
inputs still protect their exact destination names.

POSIX publication uses same-filesystem hard-link creation and Windows uses
rename, with no overwrite or copy fallback. Python documents the Windows
existing-destination failure behavior and the different POSIX rename behavior:
[os.rename](https://docs.python.org/3.11/library/os.html#os.rename) and
[os.link](https://docs.python.org/3.11/library/os.html#os.link).
Private staging uses [tempfile.mkdtemp](https://docs.python.org/3.11/library/tempfile.html#tempfile.mkdtemp).
Ownership fingerprints and directory identities are rechecked during publication
and cleanup. Handled partial failures remove only files still identified as this
attempt's files. Unknown or externally replaced files are preserved. Completion
requires both final targets to match the attempt after staging cleanup.

Two filesystem names do not form a portable atomic transaction. Stable, trusted
ancestor directories are required. The implementation does not promise protection
from a privileged actor changing ancestors between checks, mount remapping, weak
remote filesystem semantics, sudden process death, power loss or unhandled
interrupts. File fsync is not a guarantee of directory or pair crash durability.
An interrupted attempt can leave an incomplete pair or private staging files;
callers must inspect the result and must not treat mere target existence as proof
of complete publication. Empty newly created output leaf directories may remain.

Publication outcomes are operational data and do not enter the canonical report
schema or change analytical statuses. Fixed safe diagnostics expose no source
content, paths, raw OS exception messages or caller labels. P4-D06 maps invalid
paths/configuration to 2, IO/existence/cleanup failures to 1, rendering/internal
invariant failures to 4 and complete publication to 0. Existing lineage exit 3
and cross-operation precedence remain unchanged for later CLI integration.

### Exact historical binding maintenance under common G and P4-D10

Fifteen existing definitions receive exact before/after source bindings, recorded
in `PHASE4_STEP6_MIGRATIONS`. Names, parametrizations and substantive assertions
are preserved. Seven Step 5 unit definitions and three Step 5 integration
definitions now inspect the verified accepted Step 5 snapshot. Adding the one
new test file requires all five historical snapshot inventories to come from
the corresponding immutable snapshot instead of today's expanded Git inventory.
The Step 5 inventory change is within the existing ten-definition set, so this
adds four definitions. One Step 4 AST test additionally uses the accepted Step 5
logging module for its five historical logging parameters; its other ten
parameters still inspect current source. New Step 6 output AST checks inspect
current paths and logging implementations before rejecting injected mutations.

| File | Exact definition |
|---|---|
| `tests/integration/test_phase4_gates.py` | `test_phase4_step5_current_runtime_opens_only_renderers_and_freezes_schema` |
| `tests/integration/test_phase4_gates.py` | `test_phase4_step5_current_workflows_preserve_matrix_and_use_active_dispatch` |
| `tests/integration/test_phase4_gates.py` | `test_phase4_step5_current_snapshot_checks_valid_tree_before_mutations` |
| `tests/integration/test_phase4_gates.py` | `phase4_mutation_tree` |
| `tests/integration/test_phase4_gates.py` | `test_phase4_step2_current_snapshot_checks_valid_tree_before_mutations` |
| `tests/integration/test_phase4_gates.py` | `test_phase4_step3_current_snapshot_checks_valid_tree_before_mutations` |
| `tests/integration/test_phase4_gates.py` | `test_phase4_step4_current_snapshot_checks_valid_tree_before_mutations` |
| `tests/integration/test_phase4_gates.py` | `test_phase4_step4_privacy_ast_checks_current_source_before_rejecting_scope_injection` |
| `tests/unit/test_phase4_contracts.py` | `test_phase4_step5_approved_control_keeps_independent_step4_anchors` |
| `tests/unit/test_phase4_contracts.py` | `test_phase4_step5_control_rejects_forged_scope_and_stage` |
| `tests/unit/test_phase4_contracts.py` | `test_phase4_step5_control_rejects_unapproved_dispatch` |
| `tests/unit/test_phase4_contracts.py` | `test_phase4_step5_control_requires_explicit_approval_fields` |
| `tests/unit/test_phase4_contracts.py` | `test_phase4_step5_control_cannot_mint_extra_permission` |
| `tests/unit/test_phase4_contracts.py` | `test_phase4_step5_historical_migrations_preserve_ten_step4_gate_nodes` |
| `tests/unit/test_phase4_contracts.py` | `test_phase4_step5_historical_guard_rejects_assertion_and_binding_weakening` |

The new `phase4_step5_snapshot` fixture verifies the fixed commit, source tree,
test tree and every regular Git blob before use and at teardown. Original
maintainer functions remain exact except the registered active dispatch changes.
Current guards independently enforce the 31-path boundary, one new test file,
228-file candidate inventory, unchanged helpers and fixed reviewed output ASTs.
No gate computes a fresh accepted AST from a potentially modified current file.

### Step 6 verification and evidence policy

Acceptance requires complete current core, minimum-dependency and real-Parquet
runs, inherited identity retention through all six baseline generations, pure
renderer compatibility, input immutability, safe diagnostics, no overwrite,
concurrent publisher competition, write/disk/permission/rename failure handling,
ownership-sensitive cleanup, and isolated installed-wheel execution.
Four remote workflow roles retain eight OS/Python/dependency core combinations,
real Parquet, frozen Hero/math, security and build/candidate checks. Existing
job budgets remain unchanged. Failed attempts and repairs are recorded rather
than counted as passing evidence. Exact source and test identities are sealed in
the external Step 6 receipt. Review is consolidated assistant review, without a
claim of independent human certification or whole-product performance acceptance.
Stop after Step 6 acceptance.


## Phase 4 Step 7 authorization and bounded implementation

Actual user instruction, recorded 2026-09-21: `Phase 4 Step 7 继续`.
Accepted Step 6 commit: `aa2355f2359c3af4fc05345c792f9903b0d5858c`;
source tree: `d9b6910079f49a2c739f86eceec05040918a41a5`;
test tree: `8d3a03c61da807d1fef8d26fc4af0d6f72e4546e`.
The accepted baseline contains 228 files, 40 runtime modules, 3420 core tests
and 3423 tests with real Parquet. The approved plan remains byte-identical.

Step 7 implements P4-D06 single-version `audit` and input-only `validate`.
The 31-path boundary is common G plus the two runtime paths `cli.py`, `config.py`,
`tests/integration/test_cli_validation.py`, new `tests/integration/test_phase4_cli.py`,
and `docs/cli.md`. Only CLI and additive configuration orchestration open.
All inherited config code after its ownership header stays byte-identical.
The other 38 runtime modules, all five schemas, dependencies, version dev2,
Hero fixtures, formulas, oracles and authority sources remain frozen.
Comparison, packaged example, Step 8, main merge, tags, distribution publication
and Phase 4 completion remain outside this authorization.

### Explicit orchestration decisions

Both new commands require `--records`. Competing singleton declarations fail,
including duplicates with equal values. Abbreviated options and unknown flags
fail without echoing argv. One local JSON/TOML config is read using the accepted
finite, unique-key control reader. Its hash describes the bytes actually read;
config-declared paths use its parent, CLI paths use the working directory.
The Phase 4 adapter preserves explicit-field provenance before resolving options.
Validation receives detached effective settings and already resolved input roles,
so it does not reopen the control document or silently override declarations.

Audit calls accepted provenance/direct-bound kernels for one nonempty version.
An explicit field or exact-content representation enables its accepted kernels;
there is no implicit representation, weighting, missing-state sentinel or tail
threshold. An absent provenance manifest retains the accepted unavailable direct
bounds, rather than inventing endpoints. Independent valid families survive a
failed calculation. A multiversion records input preserves inventory and counts,
returns an input error, and triggers no analytical family. Empty inputs retain
the existing input-empty failure and create no synthetic version identity.

Validate calls only the accepted input pipeline and report assembly. It retains
input observations/validation coverage and clears derived, proxy and simulation
sections before canonical revalidation. No analytical kernel or local content
reference reader executes. Tail requests on validate fail as unsupported work.
Lineage input errors use the existing codes; no Phase 5 graph work is activated.

The accepted privacy view protects the entire report before publication or
console diagnostic output. Standard success prints final report paths in an
ASCII-safe JSON line. Redacted success prints fixed `report.json`/`report.md`
names relative to the selected output directory, keeping full paths out of
stdout. The salt file joins all other input reservations. Failure reports with
unresolved configuration use a fresh redacted/omit context and the explicit CLI
output directory or local default; they do not claim resolved input evidence.
Parser failures with unresolved declarations emit safe stderr only. Existing
outputs are never replaced. Operational publication failures remain on stderr.

Exit priority is `4 > 2 > 3 > 1 > 0`. Error-bearing useful evidence is partial;
optional/deferred unavailable work alone does not force a nonzero exit. Fatal
input or internal failures can publish the schema-conforming error-only pair
when the destination is safe. No raw exception text or traceback is emitted.

### Exact historical bindings

P4-D10 and common G authorize twelve whole-definition source-binding changes,
registered with exact before/after bytes in `PHASE4_STEP7_MIGRATIONS`. Seven Step 6
unit definitions and three Step 6 integration definitions inspect the immutable
Step 6 snapshot. Its 228-file mutation inventory comes from that snapshot rather
than current Git's new 229-file inventory. The Step 4 AST injection definition
uses Step 6 config only for its two config parameters; earlier logging bindings
and every other current-module check remain intact. Names, parameters and all
substantive assertions are preserved. Current Step 7 tests replace each opened
guarantee, while all inherited identities must remain collected and executed.

| File | Exact definition |
|---|---|
| `tests/integration/test_phase4_gates.py` | `test_phase4_step6_current_runtime_opens_only_output_helpers_and_freezes_schema` |
| `tests/integration/test_phase4_gates.py` | `test_phase4_step6_current_workflows_preserve_matrix_and_use_active_dispatch` |
| `tests/integration/test_phase4_gates.py` | `test_phase4_step6_current_snapshot_checks_valid_tree_before_mutations` |
| `tests/integration/test_phase4_gates.py` | `test_phase4_step4_privacy_ast_checks_current_source_before_rejecting_scope_injection` |
| `tests/unit/test_phase4_contracts.py` | `test_phase4_step6_approved_control_keeps_independent_step5_anchors` |
| `tests/unit/test_phase4_contracts.py` | `test_phase4_step6_control_rejects_forged_scope_and_stage` |
| `tests/unit/test_phase4_contracts.py` | `test_phase4_step6_control_rejects_unapproved_dispatch` |
| `tests/unit/test_phase4_contracts.py` | `test_phase4_step6_control_requires_explicit_approval_fields` |
| `tests/unit/test_phase4_contracts.py` | `test_phase4_step6_control_cannot_mint_extra_permission` |
| `tests/unit/test_phase4_contracts.py` | `test_phase4_step6_historical_bindings_preserve_assertions_and_headers` |
| `tests/unit/test_phase4_contracts.py` | `test_phase4_step6_historical_guard_rejects_weakening` |

The new fixture verifies the accepted commit, source/test trees and every Git
blob before use and at teardown. Independent current constants fix authorization,
allowed paths and reviewed runtime ASTs; they are not derived from mutable current
code at gate time. Maintainer functions and constants are inherited unchanged
except explicit dispatcher additions. CLI documentation retains its historical
notes verbatim below a current usage section.

### Verification and acceptance boundary

Acceptance requires complete core, minimum-dependency and real-Parquet test runs;
seven inherited identity generations; current CLI contract/failure/privacy tests;
installed ordinary audit with core dependencies outside the checkout and blocked
network; prior installed input/report/publication checks; and exact candidate
archive bytes. The four workflow roles preserve the eight core OS/Python/dependency
combinations, real Parquet, Hero/math, security and build jobs. Initial job budgets
were unchanged; the observed build-budget correction below updates only that job.
All attempts, failures and repairs are retained in external evidence.
Review is consolidated assistant review, not independent human certification.
Acceptance and final source identities are recorded in the external Step 7
receipt after the required checks pass. Stop before Step 8.

### Additional obsolete Step 1 CLI assertion discovered during Step 7

The complete initial focused regression ran 802 tests, with 801 passing. Its one
failure was `test_phase4_step1_keeps_current_help_and_future_commands_unopened`,
which requires the accepted scaffold help text. Before editing, the exact source
binding was proposed in the work conversation. Under common G and P4-D10, its
subprocess PYTHONPATH now selects the verified Step 6 snapshot. The existing test
name, parameters and all assertions remain unchanged. The registry explicitly
includes this twelfth definition. Current Step 7 help/audit/validate tests cover
the newly authorized behavior; no global subprocess fixture is repurposed.

Malformed or unreadable config files map to configuration exit 2. Accepted
Phase 2 input readers remain unchanged. Known error locations are retained
through the existing safe diagnostic adapter. The outer entry point emits a
fixed safe internal error if command initialization itself fails. Run duration
is captured after input/calculation work and before report assembly/publication;
it is not the Step 10 end-to-end performance measurement.

### Observed build-budget correction within common G

The first Step 7 build run, `35553895804`, on commit
`5a5e5388e8f58727104d5797f9885eeedfcc8393`, ended as `cancelled` at
2026-09-21 02:46:33 UTC, after 25 minutes 15 seconds. Its core suite passed all
3620 cases in 831.14 seconds. The subsequent real-Parquet suite reached 85%
without a reported assertion failure before `The operation was canceled.`
The observed cancellation coincides with the configured 25-minute job limit;
the available API does not provide a more specific cancellation reason.

Under the approved common G workflow/evidence maintenance scope, the build job
now has a bounded 40-minute budget, with its current Step 7 workflow assertion
updated to require exactly 40. All other job budgets, all test selections,
failure propagation, read-only permissions and upload-on-failure behavior stay
unchanged. Historical workflow assertions continue to inspect their pinned
snapshots. No runtime or mathematical code changes in this correction.
The first run and its local acceptance evidence are retained as a prior attempt;
all four workflow roles and complete local regressions execute on the corrected
source before acceptance. No earlier success substitutes for the final commit.


## Phase 4 Step 8 authorization and bounded implementation

Actual user instruction, recorded 2026-09-21: `phase 4 step 8 开始`.
Accepted Step 7 commit: `bacd33ae65e392872776c6d976401fdc3d565f63`;
source tree: `4c16914bb0f0c5281efc36624efb8b1a1d4a174e`;
test tree: `96317cb7b25236b79efc0f2d93e1e0f5f132fdb2`.
The baseline has 229 files, 40 runtime modules, 3620 core tests and 3623
real-Parquet tests. The approved plan bytes remain unchanged.

Step 8 opens common G plus CLI/config, package-data declaration only in
pyproject.toml, the two named CLI/Hero integration files, docs/cli.md and exactly
seven packaged resource copies listed in the plan. This is a 39-path allowlist,
with only those seven new paths and a 236-file candidate. No module, dependency,
version, schema, mathematical definition, accepted kernel or canonical Hero source
changes. Config extensions are additive; inherited code stays byte-identical.

### Pair, example and failure choices

Each records role selects one distinct version; no pooling or implicit selection.
The earlier side is records_compare and the later side records_primary. The
accepted representation and comparison APIs receive explicit scopes and retained
chronology. Both sides receive the same user-supplied literal state meaning.
Existing provenance joining selects the later version before the unchanged
composition/bounds kernels execute. Tail and duplicate report slots also stay
in the later scope. Both valid distributions survive pair-family failures.

Missing/reversed chronology and incompatible/unavailable representations preserve
usable evidence with errors and nonzero exit. A conflicting chronology document
is retried through the accepted input pipeline without its ordering declaration;
the original ordering error remains attached to the pair family. This makes no
alternative ordering claim and does not silently infer chronology. Structural
record parsing/identity failures retain the accepted fatal input behavior.
State meaning is required for audit comparison, is never inferred from metadata,
and is rejected on input-only validate, which can ingest two files without analysis.
Arbitrary mappings and configured per-version compatibility claims remain rejected.
No assertion of semantic truth follows from the user's literal declaration.

The one-command example reads six exact resources with importlib.resources,
reserves a new local workspace, writes inputs with exclusive creation and calls
the same audit path. Safe path/ownership helpers are reused without modifying
their accepted code. Existing workspaces, links/reparse points and network-looking
paths fail. Extraction cleanup removes only owned identity-matched files. The
full-product EXPECTED_OUTPUTS.md is copied unchanged and explicitly distinguished
from actual Phase 4 output. Reports remain privacy-protected before all sinks.
The packaged report schema exactly matches the root schema. Installed wheel and
extracted sdist execution are checked outside the checkout with network blocked.

### Exact historical bindings and independent current checks

Eleven whole-definition migrations were proposed in the work conversation before
editing, under P4-D10/common G. Seven unit definitions bind current-control and
historical-migration source reads to the immutable Step 7 fixture. Four integration
definitions bind Step 7 workflow, AST, test-file syntax and mutation-tree reads to
that fixture. Their exact names and before/after bytes are registered in
PHASE4_STEP8_MIGRATIONS. Every original assertion and parameter remains intact.
The fixture checks commit/source/test trees and every regular blob before use and
at teardown. No global fixture meaning changes. Config-prefix checks that remain
valid continue to read current source. New Step 8 controls, AST checks, negative
mutations and exact resource/package-data checks enforce the newly opened scope.
Inherited maintainer definitions/constants remain exact except active dispatch.

### Verification and stopping boundary

Acceptance requires full core, minimum-dependency and real-Parquet regressions,
eight inherited identity generations, all 20 frozen mathematical cases, independent
pair/Hero/error/privacy/no-network cases, exact wheel/sdist resources, installed
standard/redacted examples, and a source archive matching every candidate byte.
The four workflow roles retain the eight core matrix combinations, real Parquet,
Hero/math, security and build/candidate jobs. Budgets remain core60, Parquet20,
Hero15, security20 and build40 minutes. The Hero selection adds the current Hero
integration file; security retains it once with its expanded cases. All failed attempts/repairs remain in external
evidence. The final receipt records actual results and source identities.
Reviews are consolidated assistant checks, not independent human certification.
No final-product performance acceptance is claimed; Step 10 owns end-to-end targets.
Step 9, Phase 4 completion, main merge, tag and package publication remain unopened.

### Step 8 continuation review and failure-path corrections

The Theory Owner instructed `Recursive Integrity Toolkit phase 4 step 8 继续`.
The continuation recovered implementation commit
`a24e7c7c2ba321533e23f38df8c47cb746c57b15` and its incomplete acceptance evidence.
Interrupted local suites and successful subsets of its remote workflows remain
prior-attempt observations, not acceptance of a corrected source tree.

Delegated assistant review identified three in-scope failure-path corrections:
preserve usable later-side metrics when distinct records on the two input roles
claim the same version; retain the rejected chronology document in input evidence
without accepting its order; and return the approved configuration exit code for
an invalid example output path. These corrections implement existing P4-D03,
P4-D06 and P4-D07 contracts. They add no feature, formula, dependency, public field
or later-phase behavior. Step 8 tests must verify the surviving metrics, retained
input evidence and exact exit code instead of encoding the faulty outcomes.

For the same-version rejection case, the accepted provenance assembly requires
all validated records in that version. It cannot represent provenance restricted
to one of two file roles sharing the version. Preserve later-side content metrics
and validated input observations, and report this provenance-scope limitation as
an explicit family failure. Do not pool both roles into a claimed later-side
provenance metric or alter the protected assembly contract.

The current CLI syntax guard is resealed only after reviewing these edits.
All historical source-binding migrations and protected-owner bytes remain exact.
Required complete regressions, installed checks, source-archive verification and
all four remote workflow roles apply to the corrected final source. The external
receipt records its identity, actual outcomes and all superseded attempts.

The corrected-source Windows matrix exposed a test-only native-path assumption.
`bad\path` is a native relative path on Windows; its absent parent produces the
approved I/O exit code 1. POSIX rejects the spelling with configuration exit code
2. Keep the frozen path implementation, preserve the parameterized test identity,
and assert both platform-specific results occur before resource reads or writes.
The failed Windows attempt is retained and the complete final-source gates rerun.

## Phase 4 Step 9 authorization and independent report verification

On 2026-09-22 the user authorized `Phase 4  **Step 9**  开始` after accepted
Step 8 commit `63e347a785838b64a9c32e636ea48c664458cee4`, source tree
`3ac450b5f67cad738849de18601999fefee98f63` and tests tree
`ddaaab24d83080b7c1a27229c15e6e4a3f5b3cd8`. The inherited accepted suite contains
3,768 core/minimum cases and 3,771 real-Parquet cases. Step 9 opens the 26 common G
paths and exactly fourteen additional paths in plan section 6, a 40-path allowlist.
Only the seven named new golden files may be added, yielding a 243-file candidate.
All forty runtime modules, five schemas, seven packaged resources, canonical Hero
inputs, mathematical oracles, dependencies, packaging and version remain frozen.

### Historical source bindings and active guarantees

Before editing, nine exact source-binding changes were proposed in the work
conversation under common G and P4-D10. Seven unit definitions for Step 8 control
approval, forged scope, stage dispatch, required fields, extra permission and both
historical migration checks now read the pinned Step 8 snapshot. The two Step 8
integration definitions for active workflows and mutation-tree source read that
same snapshot. Their exact names and full before/after definitions are registered
in PHASE4_STEP9_MIGRATIONS. Every inherited assertion, test name and parametrization
is unchanged. The new session fixture verifies commit, source/test trees and every
regular-file Git blob at creation and teardown; shared fixture meanings stay intact.
Runtime checks that remain valid continue to read current source.

The active control independently enforces actual authorization, exact path/operation
permissions, immutable runtime/schema/resource bytes, historical source prefixes,
exact listed migrations, safe appended test definitions and preserved maintainer
statements except the explicit Step 9 dispatch additions. New mutation checks cover
substantive oracles, schema, resources, runtime, dependency/version, test binding,
old assertions, old tooling, forged permission and premature completion/output.

### Report oracle and execution evidence

The rationale, hand-authored expected values and four literal Hero report files are
frozen by six explicit SHA-256 identities after independent expectation review.
Candidate generation uses only an explicitly requested new scratch destination;
accepted golden files are never an output target. Normalization follows P4-D08,
and adversarial checks reject substantive-value erasure and unsupported claims.
JSON and Markdown are both reviewed. All new report golden tests and the unchanged
twenty mathematical cases must appear in the retained JUnit evidence, verified
against actual collection. Full-suite candidate evidence also matches every current
core and real-Parquet test identity and preserves the inherited identity generations.

The four workflow roles retain read-only permissions, eight core matrix combinations,
real Parquet, Hero/report goldens/math, security and build/candidate jobs. Budgets
remain core 60, Parquet 20, Hero 15, security 20 and build 40 minutes. Both Hero and
security explicitly select the new report-golden module; no case is filtered out.
Installed smoke verification retains every accepted runtime behavior through Step 8.
Failures and repairs remain in the external execution evidence. Reviews are assistant
checks and do not constitute independent human certification. No end-to-end performance
claim is made here. Stop after Step 9 acceptance: Step 10, Phase 4 completion, main
merge, tag and package publication remain unopened.

### Independent oracle review corrections before the final seal

The first frozen expectation set and both initial candidate/replay attempts are
retained in external evidence. Review of frozen P4-D02 and the inherited validator
confirmed two hand-authored synthetic expectations required correction: a supplied
partial-parent row makes input lineage observability partial, and an unknown schema
mapping remains an input validation failure with exit 1. Exactly those two expected
outcomes and their rationales were revised, with unchanged case identities and Hero
literals. This adjudication follows the accepted contracts and validator behavior;
no runtime change or numerical expectation was introduced. The 32-case oracle and
four literal files received their final independent review before the six hashes
were sealed in PHASE4_STEP9_GOLDEN_SHA256.

A new governance inventory test initially included editable-install metadata under
`src/`; its scope was corrected to the exact package directory while retaining all
runtime, schema, Hero and dependency equality assertions. Its failing execution and
passing repair remain distinct evidence. Golden generation, normalization and test
harness repairs likewise retain their initial failures and successful replays; the
receipt records their actual outcomes without treating a generated candidate as its
own numerical authority.

The first golden-JUnit gate draft incorrectly equated the mathematical module's
node count with its twenty parametrized cases. The inherited module also contains
one registry test. Root review found this before source acceptance. The gate now
verifies the frozen mathematical JSON hash, requires the exact twenty named case
identities plus the separate unchanged registry node, and reports the report-golden
count independently. The initial control-suite attempt was interrupted with exit
130 before this correction and is retained without an acceptance claim. Verification
includes the real 92-node golden JUnit and a missing-registry negative case.

### Observed CI budget correction within common G

The initial budgets recorded above applied to source commit
`36d6f5da537b427606adae82149d7331b505ee4e`. In CI run `35698828150`, the first
real-Parquet job `106651721071` passed all 3,962 cases in 1,100.83 seconds,
then exhausted its 20-minute job limit during inherited identity evidence
generation. One same-source retry, job `106669886339` in attempt 2 of that
run, passed the same 3,962 cases in 1,094.76 seconds and again timed out
during the subsequent evidence step. Neither cancelled job is accepted as a
successful workflow, and both raw logs and attempt identities are retained.

The first Windows Python 3.11 minimum-dependency job `106651721351` in the
same run exhausted its 60-minute limit after pytest reached 92 percent.
It produced no final passing summary and is not counted as a passed suite.
Its same-source attempt-2 job `106669886825` was still running when this
budget correction was prepared; its eventual outcome remains separate
evidence and cannot accept the corrected source.

Common G now gives the eight core matrix jobs a bounded 75-minute limit and
the real-Parquet job a bounded 30-minute limit. The active Step 9 workflow
assertion requires those exact values. Hero 15, security 20 and build 40
remain unchanged. Test selections, assertions, matrix combinations,
dependency versions, runtime behavior, golden expectations and current case
counts are unchanged. Historical Step 1 through Step 8 budget assertions and
their pinned source bindings remain intact; no additional historical test
migration is introduced.

This correction changes maintainer verification resource limits, not any
Step 10 performance target. Acceptance still requires complete local,
installed and all four remote workflow checks on one exact corrected source
commit. Earlier successful jobs do not substitute for those final-source
checks. Timeouts, partial evidence and retries are never treated as success.

## Phase 4 Step 10 authorization and verification governance

On 2026-09-22 the user authorized `Phase 4 Step 10 开始` after accepting
Step 9 commit `ad2cb5d0cb34dac9036593bac4e91c9d993bcfc6`. That accepted source
is the starting point for end-to-end Hero and metadata performance evidence.
Step 10 completion remains pending actual measurements and review. Step 11,
Phase 4 completion, merge, tag and package publication remain unopened.

The user's intervening Verification Governance and Complexity Control
instruction applies immediately. Product correctness and security boundaries
remain highest priority. Compatibility, packaging and reproducibility checks
remain required with full supported coverage primarily at PR and release
candidates. Verification additions must detect a concrete failure that existing
controls do not adequately detect, using the smallest sufficient control.

New Tier D mechanisms require all five justifications: the exact failure, why
product/security/compatibility checks cannot detect it, why Git history or
archived evidence is insufficient, the long-term maintenance cost, and an exit
or consolidation path. General claims of greater rigor do not justify additions.
Historical behavioral guarantees remain protected; exact historical Python
bodies, wrappers and fixture layouts do not automatically require indefinite
active preservation. Consolidation at major milestones requires identified
behavior, equivalent or stronger current coverage, recoverable old evidence,
and unchanged scientific/security guarantees. Current regression, release
verification and historical evidence should be maintained separately.

This step therefore updates the existing active scope gate against the accepted
Step 9 Git commit and current authorization. It does not add another historical
snapshot fixture, migration registry, source-body chain or evidence-generation
proof layer. Earlier records remain in Git and accepted archives. Current
behavioral rejection checks retain unauthorized runtime/schema/dependency/
golden/path mutations and unapproved stage transitions. The current control
document records permissions; it cannot grant additional permissions itself.

The new direct evidence covers complete Hero execution through JSON and
Markdown publication, and a deterministic 100,000-record metadata input with
five source classes and partial provenance. Independent aggregate expectations
must remain explicit. Untraced elapsed time is measured separately from traced
Python allocation peaks; RSS scope and tracing overhead are disclosed. All
attempts, input sizes, report sizes, commands and environment observations are
retained. No sparse-lineage run, later-phase calculation or fixed 100k throughput
threshold is authorized. The under-five-second Hero target retains its stated
hardware and Phase 4 scope limitations.

Development checks follow actual impact: changed performance tests, adjacent
CLI/report tests, current scope controls and frozen mathematical/report goldens.
An ordinary Step 10 push uses bounded focused CI. Complete canonical regression
and the supported matrix remain available at pull-request and explicit candidate
dispatch gates, with final release verification in Step 11. Administrative or
documentation changes do not automatically rerun a release matrix. Meaningful
bounded mutation checks are preferred to raw test-count growth where they
detect distinct defects. No existing product or scientific guarantee is waived.

No runtime, mathematical, schema, package-resource, dependency or accepted
golden mutation is authorized by this performance step. A demonstrated
protected-owner repair must be described concretely and receive its required
scoped approval before implementation; an unresolved performance defect cannot
be converted into successful Step 10 acceptance.

### Step 10 bounded investigation: protected report repair pending

The complete Hero audit has executed successfully on the recorded container
CPU, including publication of both reports. These observations do not certify
all laptop hardware. The required 100,000-record fixture has not been executed
or accepted: bounded report-path review found a concrete quadratic expansion.

In `reports/assembly.py`, `_diagnostics` attaches the full input identity scope
to every warning and uses linear list membership to deduplicate diagnostics.
A bounded direct adapter probe with 100/400 records and 10/40 missing-row
warnings produced 1,000/16,000 repeated scope identities. Separately,
`_duplicates` rebuilds the entire scope set for every duplicate group; a
100/400-record probe with 50/200 groups processed 5,000/80,000 scope keys.
Both are sixteenfold work/data growth for a fourfold input increase.

An unapplied repair proposal is retained with the external Step 10 review.
It would keep warning scope identity/counts/denominator and exact locations,
retain the full inventory in `inputs.scope`, use equality-preserving local
diagnostic keys, and construct the duplicate scope set once. All warning entries,
classification, counts, encounter order, errors and scientific values remain
protected. The existing schema permits the proposed warning summary fields;
no schema, oracle, dependency or mathematical change is proposed.

The proposed runtime file is outside the original Step 10 permission set.
No runtime repair has been applied, and no permission is inferred from this
record. Step 10 remains blocked pending the scoped protected-owner decision,
the actual 100,000-record measurements, relevant regression and final review.

### Approved Step 10 protected-owner repair

On 2026-09-22 the user replied `批准` to the delivered Step 10 repair review
and `PHASE_4_STEP_10_PROPOSED_REPAIR.patch`. This explicitly authorizes the
single additional runtime path `src/recursive_integrity_toolkit/reports/assembly.py`
for the proposed warning-scope summary, equality-preserving local diagnostic
deduplication and duplicate-group scope-set reuse, followed by real 100,000-record
measurements and relevant regressions. The earlier pending status above records
the investigation before this approval and is not the current permission state.

The original reviewed patch is applied without expanding the runtime scope.
Every warning's location, count, classification, encounter order and capability
effects remain protected, with complete identities retained in inputs.scope.
Scope identity, counts and denominator remain in every warning's affected_scope;
its optional complete identity arrays are no longer repeated. This standard-mode
representation change does not assert redaction or missing evidence. Formulae,
denominators, unavailable states, evidence classes, privacy guarantees, schema,
accepted golden oracles and dependencies remain unchanged.

Current controls may synchronize this exact exception and directly test its
behavior. No new historical migration chain, general runtime permission or
later-step authorization is conferred. Step 10 acceptance remains pending the
actual scale measurements and relevant correctness/security review.

### Bounded allocation instrumentation for the actual 100k run

After the approved repair, a matched 1,000-record pair measured about 7.774
seconds without allocation tracing and 78.742 seconds with tracemalloc enabled,
an observed 10.13-fold instrumentation overhead. These measurements describe
that 1,000-record input only. They are not measured 100,000-record results.

The formal 100,000-record run therefore retains the complete real CLI audit,
publication and verification of both reports, untraced wall time, and fresh-child
peak RSS, with its existing 1,800-second process guard. Its Python allocation
peak is explicitly null and marked unmeasured. Hero retains three untraced runs
and one separate traced run; the matched 1,000-record diagnostic retains its
actual allocation peak and overhead. RSS and traced Python allocations have
different scopes and are reported separately. No small-input result is
extrapolated into a measured full-scale result.

This bounded instrumentation choice follows the Phase 4 performance plan's
separation of wall-time measurement from tracing and the user's complexity
control policy. The plan requires actual end-to-end 100k time and memory
observations; it does not require tracemalloc on every input size. Independent
review confirmed this reading. Measured tracing overhead and the container's
finite memory justify omitting the additional full-scale tracing pass. Actual
100k RSS remains mandatory, and no throughput target, Hero target, report
semantics, warning inventory or failure acceptance rule is relaxed. All raw
attempts and their instrumentation modes remain recoverable in the evidence.

### Step 10 accepted result and Step 11 authorization

On 2026-09-22 the user instructed `继续 Phase 4 Step 11`. Step 11 starts from
the accepted Step 10 commit `9142b344bfc2dc2b33dbc696159f07bbc81b223a`, tree
`a485078d3e7cf739e10b087acb604f317ee19854`. The external Step 10 receipt records
the completed repair, actual scale measurement and focused remote verification;
the earlier pending paragraphs above remain the historical investigation record.

The accepted 100,000-record complete report run measured 1,362.470766888 seconds
outer wall time and 7,640,743,936 bytes peak RSS. It published 442,741,529 bytes
JSON and 165,120,454 bytes Markdown, with 66,000 warnings and no errors, while
independent numerical expectations passed. Full-scale traced Python allocation
peak remains unmeasured. These observations concern that fixture and recorded
Linux reference environment; no general performance guarantee is inferred.
Remote run 35718603026 on the accepted commit passed 244 affected product,
performance and golden cases plus 89 scope-control cases. It was a focused
Step 10 run and did not establish a new complete environment matrix.

Step 11 authorizes the planned public documentation, three completion reports,
the exact package version transition to `0.1.0.dev3`, current test expectations
for that version, and maintenance of existing stage controls and workflow roles.
All other runtime bytes, scientific oracles, schemas, packaged Hero resources,
accepted literal golden files and dependency declarations remain frozen.
Historical version-specific checks use their existing accepted snapshots.
Current report tests may adapt only the expected version metadata in memory,
while checking the observed version exactly; the golden normalizer and stored
golden fixtures retain their accepted bytes.

### Step 11 verification scope and acceptance records

The user's Verification Governance and Complexity Control policy governs this
closeout. It supersedes the plan's automatic full-workflow rerun after every
acceptance-record edit. Final candidate verification retains the complete
Ubuntu/Windows, Python 3.11/3.12, current/minimum core matrix and the real-Parquet
suite, including their actual performance cases. The packaging role reuses
same-run core and Parquet evidence instead of executing those full suites again.
Security and golden roles remain independently required. Failures are retained
and must be resolved or explicitly block acceptance.

Completion reports are ordinary descriptive records. They cannot authorize a
runtime mutation or turn a failed gate into a pass. The existing permission
baseline continues to describe Step 11 candidate authority with
`phase_complete: false`; actual completion is recorded only after the required
results exist. An acceptance-only successor may update these reports with
actual outcomes after direct document and scope checks. Such a successor does
not automatically repeat the matrix when executable and authoritative bytes
are unchanged. Final source and package artifacts must identify their actual
source, and no remote binary equivalence is inferred from job status alone.

No new historical source registry, migration chain, test-body snapshot, execution
receipt framework or evidence-of-evidence layer is introduced. Existing direct
mutation rejection checks remain canonical; obsolete implementation forms are
recoverable from Git and archived phase evidence. Phase 5, merging main, tags
and package publication require later authorization.

### Step 11 first full-candidate findings

Candidate `0c2f5e4b5bb4730923ea87e54086fb077a66e996` passed the remote
Hero/mathematical job, while security job 106880586538 recorded 3,267 passes and
10 failures. The failures expose historical test preconditions still tied to
moving current files: four Step 1 CLI migration cases require dev2, a Step 1
assertion forbids completion records, three Step 4 assembly cases require the
source form preceding the approved Step 10 repair, and Step 7/8 module-difference
assertions omit later approved changes. This is a failed candidate, retained in
the evidence. No product failure is waived or converted to acceptance.

Five existing test functions may use their already available accepted stage
fixtures for these historical preconditions. Their mutation cases and behavioral
assertions remain intact, and canonical current tests continue to protect current
runtime, schema, privacy and unauthorized-mutation boundaries. This is the
user-authorized consolidation of historical implementation forms, without new
fixtures, source registries, migration chains or runtime changes. The affected
control suites and required repaired candidate gates must pass before completion.

The two complete CI suite commands also use pytest `--maxfail=1` so a known
invalid environment stops before spending further time on expensive cases.
Collection, supported profiles, successful-run counts and the exact identity
gate remain unchanged. A partial failed run cannot satisfy acceptance. Matrix
`fail-fast: false` remains in place so other environments can expose distinct
failures; the security role retains its complete diagnostic failure list.
