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
