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
