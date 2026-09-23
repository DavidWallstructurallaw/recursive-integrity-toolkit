# Phase 5 Decisions and Step 1 Authorization

Status: **PLAN APPROVED; STEP 1 AUTHORIZED; PHASE INCOMPLETE**.

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

Stop after Step 1. Phase 5 Step 2 requires its own execution instruction.
