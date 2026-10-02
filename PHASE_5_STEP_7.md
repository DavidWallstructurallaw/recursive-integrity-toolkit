# Phase 5 Step 7 Completion

Date: 2026-09-23 UTC. Status: **COMPLETE; PHASE INCOMPLETE**.

The Theory Owner instructed `Phase 5 Step 7 开始`. Work starts from
`e2666515d98cfe41483b5c43345c642bab02ced0` on `phase5-lineage`.
This step integrates explicitly computed lineage evidence with canonical reports,
schema 1.1, privacy protection and the existing JSON/Markdown renderers.

## Delivered behavior

`assemble_report` accepts explicit `lineage`, `lineage_bounds` and
`shared_ancestry` results. Bounds and proxy must refer to the supplied ancestry
result. Assembly does not execute ingestion, graph traversal, root propagation
or metric kernels. A private input digest binds the result to relevant validated
declarations, roles, chronology and diagnostic classifications. Same record keys
with changed grounding or parent declarations cannot silently reuse old results.
Raw content, URIs, paths and notes are excluded from that digest, and the digest
is never serialized. This is a product handoff check, not a new evidence registry.

All reports now declare schema `1.1`, retaining the twelve top-level sections,
equal capability mirrors and existing non-lineage values and scopes. Reports
expose loaded graph scope separately from the target population, cycle members
and affected descendants, depth, resource usage, G/C/U, coverage, roots, incidence,
fractional mass, concentration, lineage bounds and the descriptive shared-root
signal. Hero retains G=8, C=U=0, five roots, HHI=1/4, four effective roots and
lineage bounds `[0,0]`; its independent direct bounds remain `[1/2,1/2]`.

Lineage defaults to `not_requested`. Completed, partial and failed execution
remain distinct from input eligibility and individual field availability.
Pregraph failure cannot claim an acyclic graph; a root-budget failure retains
already completed cycle, depth and reference observations without inventing root
results. Empty and unresolved populations retain explicit unavailable reasons.

Five identity-bearing detail collections are bounded to 100 rows. Cycle witnesses
contain at most 64 edges and 65 keys. Full counts, root metrics and denominators
are calculated before display truncation. Existing scoped HMAC protection covers
new versions, roots, cycle witnesses and record identities. Omit mode removes
whole detail collections with explicit counts and reasons; it retains prior
diagnostic-limit reasons. JSON and Markdown share the validated safe view.
Resource-limit diagnostics now have a fixed readable message and remediation.

## Verification

Local checks used Python 3.12.14 and the core dependency profile without PyArrow.

| Check | Result |
|---|---|
| New report semantics and integration cases | 29 passed |
| New privacy and identity-boundary cases | 14 passed |
| Combined affected regression selection | 1,583 passed; four setup-related failures resolved below |
| Installed Hero and source-boundary failure rechecks | 4 passed in 1.58 seconds |
| Current verification and CI checks after metadata fix | 41 passed |
| Wheel module/resource identity and schema mirror | PASS; all 47 current files match |
| Specification consistency and module boundaries | PASS |
| Four workflow YAML files and whitespace check | PASS |
| Independent implementation, schema and privacy review | PASS; no remaining blockers |

The combined gate covered report contracts, both validators, malformed wire
values, privacy, CLI isolation, safe publication, golden reports, optional
dependency absence, no-network behavior, lineage algorithms and affected input
neighbors. It also ran the bounded Hero runtime checks. The 43 new cases include
same-key stale handoffs, no-recalculation guards, 100-row detail limits, 64/65-edge
witness boundaries, malicious identifiers and unknown diagnostic text. Independent
review found and corrected a post-HMAC reason-order validation error; all four
supported privacy modes now preserve source ordering without requiring alias
lexical ordering. Unsupported standard/hash and standard/omit remain rejected.

The initial legacy check found a registered resource-limit code missing from safe
diagnostic templates. Its existing behavior test detected the omission; the
template and privacy whitelist were corrected. Initial golden candidate generation
also required the source import path. The installed golden first lacked a wheel,
then correctly rejected a wheel built before the final schema-validator edit.
Rebuilding and reinstalling the current wheel resolved that mismatch.

Three source-boundary checks encountered setuptools metadata produced by the
local build. The existing control now excludes only the exact external package
metadata prefix `src/recursive_integrity_toolkit.egg-info/`, after its symlink
check. Product bytes and package inventory stay protected. Existing unauthorized
mutation tests run with that metadata present; similarly named and nested
directories remain rejected. The four setup failures passed targeted rechecks;
the subsequent boundary gate passed all 41 cases. Together, 1,589 distinct cases
in the affected selection and these two added boundary cases have passed.

No full OS/Python/dependency matrix, 100k lineage measurement or release-candidate
execution was repeated. Those remain their designated candidate/scale gates.

## Verification consolidation

Current report goldens and independently authored expected status/version fields
advance to schema 1.1. Before promotion, both standard and redacted candidates
were compared with the previous fixtures: all non-lineage numerical metrics,
scopes, proxy signals, simulations, diagnostics and metadata recommendations were
unchanged. Current literal fixtures now carry package `0.1.0.dev3`, removing the
old package-version substitution adapter. Original numerical oracles and the six
canonical Hero files remain unchanged. Prior fixture forms and authority records
remain recoverable from Git history.

The single source boundary advances to completed Step 6 and permits the seven
changed product files. The remaining 52 product files, exact package inventory,
16 frozen specifications and seven resource copies remain protected. No new
historical migration chain, approval registry or evidence-of-evidence mechanism
is introduced.

## Handoff

Package version stays `0.1.0.dev3`; report schema is now `1.1`. Strict schema-1.0
readers must explicitly adopt 1.1. Step 8 remains the separately authorized CLI
lineage flag, context-input role and dispatch work. No merge, tag, release
publication or hosted CI success is claimed here.
