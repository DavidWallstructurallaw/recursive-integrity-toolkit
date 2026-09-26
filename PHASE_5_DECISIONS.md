# Phase 5 Decisions and Current Authorization

Status: **PLAN APPROVED; STEPS 1-8 COMPLETE; PHASE INCOMPLETE**.

On 2026-09-23 UTC the Theory Owner instructed:
`批准，Phase 5  step 1开始`.
This accepts the delivered Phase 5 plan and its eleven decisions without stated
exceptions, and authorizes Step 1. Execution remains one authorized step at a
time. Step 2, a main merge, a tag and software publication are not authorized by
this instruction.

The accepted starting commit is
`1db3b1a460c233242ff37fbe45b8fac74d6101ef`, on `phase4-reports-cli`.
The Phase 5 implementation branch is `phase5-lineage`. The package remains
`0.1.0.dev3` and the executable report schema remains `1.0` during Step 1.
The original standalone plan records its draft submission; the repository copy
and this document record the subsequent actual approval. No new machine-readable
approval registry or historical source-binding chain is introduced.

## Approved contract decisions

| Decision | Status | Implementation boundary |
|---|---|---|
| P5-D01 | APPROVED | One primary target population; explicitly loaded context supplies paths and roots without entering target denominators. Empty targets have unavailable ratios and no invented version. |
| P5-D02 | APPROVED | Reuse canonical reference resolution, chronology, aliases and declaration states. Retain per-record failures and successful reference evidence in a bounded batch refactor. Original declarations determine reference coverage; unique edges determine graph behavior. |
| P5-D03 | APPROVED | Iterative cycle analysis; cycle count means cyclic strongly connected components. Distinguish cycle members and affected descendants. Depth measures fully resolved structural parent paths. |
| P5-D04 | APPROVED | Explicitly parentless grounded anchors; grounded single-parent carryover inherits roots. Unsupported grounded-with-parent forms remain unresolved. New external inputs use separately loaded explicit anchors. |
| P5-D05 | APPROVED | Complete root sets only for exact ancestry metrics; partition targets into grounded, closed and unresolved. Unknown required-path grounding and unresolved branches propagate uncertainty. |
| P5-D06 | APPROVED | Incidence shares use all targets N; fractional root weights use the complete nonempty-root population G. HHI and effective roots retain F-012/F-013 and their topological meaning. |
| P5-D07 | APPROVED | Lineage closure is `[C/N, (C+U)/N]`; direct closure is unchanged. Shared-root presence is descriptive and discloses partial coverage. |
| P5-D08 | APPROVED | Schema 1.1 in Step 7; typed immutable results, twelve existing report sections and equal capability mirrors. Protect every new identity; omitted detail remains schema-valid. |
| P5-D09 | APPROVED | Explicit `--lineage` on audit/example and repeatable local lineage context inputs. Primary/context versions stay disjoint; validation remains input-only. |
| P5-D10 | APPROVED | Finite graph, edge, root-membership and root-union work limits; bounded diagnostics; honest unavailable outcomes after exhaustion. |
| P5-D11 | APPROVED | Consolidate current verification around behavior and bounded candidate gates. Recover obsolete implementation checks from Git/history without requiring them in every execution. |

The operational field names, shapes, defaults and edge cases are fixed in
[docs/lineage_contract.md](docs/lineage_contract.md). That document specifies
future implementation contracts; Step 1 adds no graph execution or schema 1.1
runtime support. Implementation steps retain their dependencies in the approved
plan.

## Step 1 clarifications within the approved decisions

1. **Carryover aliases:** exactly one parent means one canonical resolved parent
   after the existing resolver groups aliases/repeated declarations. Extra
   unresolved declarations still prevent complete inheritance. Multiplicity is
   retained in reference coverage, never ancestry mass.
2. **Depth versus grounding:** depth depends on complete structural parent paths.
   An explicitly parentless unknown-grounding record has depth zero while its
   external-root set remains unresolved. A whole-target maximum is unavailable if
   any target's required structural path is incomplete. A resolved-subset maximum
   is a separately labeled diagnostic.
3. **Proxy wire vocabulary:** the conceptual absent outcome uses the existing
   `not_present` value. Unavailable uses `status: unavailable` with
   `level: indeterminate`; no synonymous enum or risk scale is added.
4. **Diagnostic bounds:** each lineage detail table/key collection returns at most
   100 entries. A cycle witness contains at most 64 edges. Longer witnesses are
   omitted with an explicit size reason; a nonclosed prefix is never presented as
   a cycle witness. Exact aggregate counts survive detail omission.
5. **Resource interface:** the approved defaults are 200,000 loaded nodes,
   1,000,000 unique edges, 1,000,000 stored root memberships and 10,000,000 root-union
   candidate visits. Limits reject booleans, nulls, nonintegers and nonpositive
   values. Existing input limits retain their separate meaning.
6. **Empty scope:** N = G = C = U = 0 is a valid empty analytical scope. Coverage,
   closure and concentration ratios are unavailable. Exact zero declared
   references retain the executed-lineage convention of coverage 1.0 with
   `no_declared_parents=true`; this does not establish external grounding or a
   negative shared-root finding.

These clarify implementation details requested by Step 1. They add no scientific
formula, inferred parent, external-input evidence schema or automatic longitudinal
behavior. A genuine conflict with the approved contracts must be surfaced before
dependent implementation.

## Current verification boundary

The user-approved Verification Governance and Complexity Control instruction
governs consolidation. Preserve direct mathematical, input, provenance, privacy,
CLI and packaging guarantees. Identify the behavior of each retired historical
check in the Step 1 change explanation and retain its equivalent current check.
Git history and archived phase records preserve prior bodies and receipts.

Current consistency/dispatch checks continue to reject unauthorized product
changes where that boundary applies. Frozen Phase 0 specifications, the six
canonical Hero files, runtime modules, executable schemas and package version
remain unchanged in Step 1. Current canonical regression remains executable;
release verification retains compatibility, clean installs, reproducibility and
artifact integrity at suitable candidate gates.

Do not add a new Tier D mechanism without identifying its exact failure, why
Tier A/B/C cannot detect it, why Git/archive cannot suffice, maintenance cost and
an exit/consolidation path. This step proposes no such mechanism. Historical
Phase 4 approval records retain their historical scope and are not rewritten as
new Phase 5 authority.

The Step 1 consolidation retains these current protections while retiring the
corresponding historical execution machinery:

| Historical mechanism consolidated | Protected behavior retained in current checks |
|---|---|
| Snapshot fixtures, staged path/migration assertions and historical-only Phase 4 gate suites | Current positive checks and negative tests reject unauthorized Step 1 product changes and frozen-specification tampering. |
| Exact owner-wrapper/docstring/placeholder assertions around implemented modules | Direct mathematical, representation, provenance, bounds, reference, generation, report, privacy and CLI tests exercise current supported behavior. The PR-003 operation inventory and T5 deferred public boundary remain explicit. |
| Historical package/schema/Hero source bindings | Current checks reject packaged schema or Hero corruption and protect frozen Hero inputs/expectations. |
| Repeated historical workflow/phase dispatch assertions | One current dispatch path and current workflow behavior checks retain focused ordinary gates and candidate compatibility/delivery roles. |

Input-only validation and absence of analytical/network/IO side effects retain
their direct integration/security cases. Historical source forms remain
recoverable from the accepted starting commit and archived Phase 4 evidence.
This table explains consolidation; it is not a new executable registry.

## Acceptance and handoff

Step 1 requires reviewed typed contracts, independent fixture expectations and
affected consistency/dispatch/behavioral boundary checks. It does not require a
release matrix or demonstrate graph correctness. Actual changes, check results,
failures and unresolved limitations belong in the Step 1 completion report.
This approval record makes no claim that those checks have already passed.

Step 1 completed before the following separate execution instruction.

## Step 2 execution instruction

On 2026-09-23 UTC the Theory Owner instructed `Phase 5 Step 2开始`.
This authorizes the bounded reference-retention refactor and immutable validated
parent graph in the approved plan. Work starts from Step 1 commit
`5e946d1a42f87f89d4f97e9da4fd76cb05517caa` on `phase5-lineage`.

The current source boundary opens four existing modules: `models.py`, `errors.py`,
`io/validation.py` and `lineage/graph.py`. Direct reference/graph tests, affected
generation/input neighbors, documentation and the current focused gate are in
scope. This updates the single current control without adding a registry or
historical migration. Package version and executable report schema remain
`0.1.0.dev3` and `1.0`. No cycle/depth/root algorithm, lineage metric, new CLI role,
full environment matrix or performance measurement is authorized by this step.

Stop after Step 2; subsequent execution needs its own instruction. Existing
authorization to synchronize this branch is retained. Merge, tag and publication
remain separate actions.

## Step 3 execution instruction

On 2026-09-23 UTC the Theory Owner instructed `Phase 5 Step 3 继续`.
This authorizes iterative strongly connected component detection, affected
descendants, bounded cycle witnesses, topological ordering and structural depth.
Work starts from Step 2 commit
`e40543ff5ed3d2793a41bf58d7e4831bd2a9bfe9` on `phase5-lineage`.

Runtime implementation is confined to the existing `lineage/cycles.py` owner.
The existing T6 test module becomes a direct behavior suite; input/graph and
generation neighbors remain the affected gate. The single current source check
advances to the completed Step 2 tree and opens only this implementation module.
No additional historical dispatcher or source-binding registry is introduced.
Root propagation, ancestry metrics, schema/report integration and CLI lineage
dispatch remain subsequent steps. Stop after Step 3; merge, tag and publication
remain outside this instruction.

## Step 4 execution instruction

On 2026-09-23 UTC the Theory Owner instructed `Phase 5 Step 4 继续`.
This authorizes external-root anchors, carryover inheritance, complete root
unions, G/C/U classification and coverage, including the approved root resource
guards. Work starts from Step 3 commit
`11192a3c353292f11d85eb3725c8edc73a71967b` on `phase5-lineage`.

Runtime changes are confined to `lineage/ancestry.py`. Direct T4 and root-resource
tests exercise the new behavior; graph/cycle, provenance and input-only neighbors
retain their relevant checks. The existing source boundary advances its single
comparison commit to Step 3 and opens only the ancestry module. No new registry
or historical migration is added. Incidence, concentration, bounds, shared-root
proxy, report/schema integration and CLI lineage dispatch remain later steps.

The conflict rule follows frozen `DEFINITIONS_AND_UNITS.md` section 5.8 and
`DATA_AND_PROVENANCE_SPEC.md` section 9.12: unresolved grounding/ancestry conflicts
block root classification. A `batch_id` or `timestamp` difference between record
and provenance namespaces alone does not establish such a conflict. Original
metadata is preserved; no new grounding inference is made from labels or URIs.

Stop after Step 4; merge, tag and publication remain outside this instruction.

## Step 5 execution instruction

On 2026-09-23 UTC the Theory Owner instructed `Phase 5 Step 5 继续`.
This authorizes typed root contributions, incidence with the full target
denominator, fractional root mass with the grounded target denominator,
ancestry HHI and effective external-root count. Work starts from Step 4 commit
`2450100d08355d8cb1e0be931345f44572861e4a` on `phase5-lineage`.

Runtime changes remain confined to `lineage/ancestry.py`. Direct rational
oracles, deterministic invariance checks and affected ancestry/resource
neighbors verify the new calculations. The current source check advances its
single comparison commit to Step 4 and continues to open only the ancestry
module. No additional governance framework or historical migration is added.
Package version and executable report schema remain `0.1.0.dev3` and `1.0`.

Stop after Step 5. Bounds, shared-root proxy, report/schema integration and CLI
lineage dispatch remain later steps. Existing branch synchronization approval
continues; merge, tag and publication remain separate actions.

## Step 6 execution instruction

On 2026-09-23 UTC the Theory Owner instructed `ok 继续Phase 5 Step 6`.
This authorizes lineage closure bounds and the descriptive shared-ancestry
dependence proxy under P5-D07. Work starts from Step 5 commit
`d81966561502b94701712a3d4b4b7fd50783cba9` on `phase5-lineage`.

Runtime changes are confined to `metrics/bounds.py` and `lineage/ancestry.py`.
Lineage bounds use the complete target G/C/U partition and preserve direct
bounds. The proxy uses exact root incidence with explicit coverage and no
calibrated risk interpretation. Its absence requires complete nonempty target
evidence; incomplete evidence without a witness remains unavailable.

The current source check advances its single comparison commit to Step 5 and
opens these two existing owners. Direct oracle, uncertainty, input-boundary and
direct-bound regression checks cover the change; no additional governance
architecture is introduced. Package version and executable report schema stay
`0.1.0.dev3` and `1.0`.

Stop after Step 6. Report/schema and CLI integration remain Steps 7-8. Existing
branch synchronization approval continues; merge, tag and publication remain
separate actions.

## Step 7 execution instruction

On 2026-09-23 UTC the Theory Owner instructed `Phase 5 Step 7 开始`.
This authorizes schema 1.1, explicit lineage report assembly and identity-safe
JSON/Markdown output under P5-D08. Work starts from Step 6 commit
`e2666515d98cfe41483b5c43345c642bab02ced0` on `phase5-lineage`.

Runtime changes are confined to the existing result/schema, report assembly,
Markdown renderer, safe diagnostics and ancestry owners. The ancestry change binds supplied
results to relevant validated declarations so that same-key stale results cannot
enter a new report; it performs no graph or metric recalculation. Both report
schema resources advance together. No new product module is introduced.

Current report fixtures are consolidated to schema 1.1 with their independently
authored scientific values preserved. Schema 1.0 fixtures remain recoverable in
Git history. Direct semantic, malformed-wire, redaction and report compatibility
checks cover this public boundary. The single current source control advances
to Step 6 and opens only the seven changed product paths. No new migration registry
or meta-verification architecture is added.

Package version stays `0.1.0.dev3`. Step 8 CLI flags, context-role ingestion and
dispatch remain separate work. Stop after Step 7. Existing branch synchronization
approval continues; merge, tag and publication remain separate actions.

## Step 8 execution instruction

On 2026-09-26 UTC the Theory Owner instructed `Phase 5  Step 8  开始`.
This authorizes the explicit CLI and installed Hero integration under P5-D09,
including the finite configured resource limits already specified under P5-D10.
Work starts from Step 7 commit
`267504e8fee4784f6d041e445a9e690c982e61a3` on `phase5-lineage`.

`audit` and `example` gain explicit lineage opt-in. Repeatable local context
inputs supply ancestors without entering the primary population's denominators
or automatically requesting comparison. Context versions must remain disjoint
from primary and comparison versions. Configuration resolution remains inert;
`validate` may load context for input/reference validation and never executes
lineage or analytical families. Existing empty-file rejection remains unchanged.

The current source check advances its single comparison commit to Step 7 and
opens the existing configuration, input-role, CLI and report-schema owners needed
for this integration. Direct CLI/config/input tests, affected metric/report
neighbors and installed Hero checks protect the public boundary. CSV/JSONL and
real Parquet context inputs receive relevant loader checks. No new historical
migration mechanism or meta-verification registry is authorized or required.

Package version stays `0.1.0.dev3`; report schema stays `1.1`. Step 9 scale work
and Step 10 candidate verification remain subsequent steps. Stop after Step 8.
Existing branch synchronization approval continues; merge, tag and publication
remain separate actions.
