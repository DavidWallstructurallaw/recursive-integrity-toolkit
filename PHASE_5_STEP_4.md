# Phase 5 Step 4 Completion

Date: 2026-09-23 UTC. Status: **COMPLETE; PHASE INCOMPLETE**.

The Theory Owner instructed `Phase 5 Step 4 继续`. Work starts from
`11192a3c353292f11d85eb3725c8edc73a71967b` on `phase5-lineage`.
This step implements external-root resolution and coverage. It does not
authorize incidence/concentration, bounds/proxy, report or CLI integration,
subsequent steps, a merge, tag or release.

## Delivered behavior

`lineage.ancestry.analyze_lineage` consumes the retained validation handoff,
reuses the existing graph and cycle owners, and revalidates provenance metadata.
An explicitly parentless grounded-yes record supports itself. A grounded-no
parentless record has a complete empty root set. Missing or unknown evidence is
represented by a null root set with reasons, preserving the distinction between
unknown ancestry and known closure.

A grounded-yes single-parent carryover inherits its parent's complete root set,
including an empty set. Repeated aliases still mean one canonical parent.
Other grounded-with-parent forms remain unresolved under the approved rule.
Grounding-no descendants union unique roots only when every required branch is
complete. Cycles, invalid/unresolved parents, missing required provenance,
unknown grounding and undeclared boundaries propagate unresolved ancestry.
Source labels, evidence URIs and record content never mint roots.

Only targets enter G/C/U classification and coverage denominators. Context nodes
support propagation without entering N. Original reference multiplicity remains
separate from deduplicated adjacency and root sets. Known identity resolution
with unavailable chronology can retain reference coverage while ancestry remains
unavailable. Malformed declarations with unknown cardinality do not become zero
declared references. Structural depth remains independent of root uncertainty.

The conflict interpretation follows frozen definitions: blocking grounding or
ancestry contradictions are distinct from `batch_id` or `timestamp` differences
between metadata namespaces. Those metadata differences alone do not erase valid
roots, and their original values are not overwritten.

## Resource boundaries

Propagation processes loaded nodes in deterministic dependency order, choosing
canonical ready nodes and canonical parent/root order. Logical memberships are
charged before each new stored `(record, root)` association. Every candidate
parent-root visit is charged, including duplicates already seen from another
parent. An anchor self-membership costs one membership and zero union visits.
Unknown branches do not contribute partial observed-root sets as exact ancestry.

Root-stage exhaustion yields a failed result with no records, G/C/U partition or
root coverage. Previously completed graph/cycle/depth observations and immediate
reference coverage remain available. Existing graph node/edge admission failures
continue to raise their typed error before an analytical result exists. Limits
describe defined work units, not process RSS or already-loaded input memory.

The current implementation processes loaded context as well as targets; resource
usage includes context associations actually stored. Returned ancestry records
contain targets only. Result containers are immutable and exclude raw content,
locations and provenance URI values.

## Verification

Local verification used Python 3.12.14 with the core dependency profile.

| Check | Result |
|---|---|
| Combined Step 4 direct and affected regression gate | 541 passed in 5.17 seconds |
| Additional provenance coverage/source-share neighbors | 203 passed in 0.51 seconds |
| Separate validation/pair CLI isolation checks | 2 passed in 0.48 seconds |
| Specification consistency, traceability and source scope | PASS |
| Workflow YAML parsing and whitespace check | PASS |
| Independent implementation and test review | PASS; no outstanding blockers |

The combined gate includes 48 ancestry cases and 12 resource cases. Direct
checks cover all twelve frozen root/classification fixtures and Hero exact root
sets, separate unknown/missing branches, conservative carryover rules, original
reference multiplicity, context exclusion from target denominators, strict and
fatal outcomes, immutable results and input-only/no-I/O guarantees. Resource
checks cover exact membership and candidate-visit boundaries, duplicate roots
versus duplicate aliases, canonical ordering, failure retention and a 1,200-node
chain without recursion. Existing cycle, graph, parent, generation, metric and
current boundary checks remain in the same focused selection.

The initial direct-test draft had two fixture-construction failures: an incorrect
provenance-match field name and invalid empty content rejected before lineage.
Both were corrected in the tests without changing frozen inputs. Independent
review also found a missing fatal-status branch and opportunities to construct
inconsistent result statuses or boolean coverage ratios. These were fixed with
direct regression cases. Completed cycle diagnostics remain preserved, and
complete root identities must belong to the loaded scope.

The existing source check advances its single comparison commit to completed
Step 3 and opens only `lineage/ancestry.py`. The other 58 product files, exact
file inventory, 16 frozen specifications and seven packaged resource copies
remain protected. No new registry, historical migration or evidence framework
is added.

## Handoff

Package version remains `0.1.0.dev3`; report schema remains `1.0`. Current report
assembly and ordinary CLI flows continue their existing behavior. Step 5 may
add root incidence and fractional concentration from complete target root sets
after its separate execution instruction.

No full regression matrix, release build, clean install, optional Parquet profile
or 100k performance measurement is claimed here. Those remain their designated
candidate/performance gates. Hosted CI success is not claimed.
