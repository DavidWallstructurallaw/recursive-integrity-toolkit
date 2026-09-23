# Phase 5 Step 3 Completion

Date: 2026-09-23 UTC. Status: **STEP 3 COMPLETE; PHASE 5 INCOMPLETE**.

The Theory Owner instructed `Phase 5 Step 3 继续`. Work starts from
`e40543ff5ed3d2793a41bf58d7e4831bd2a9bfe9` on `phase5-lineage`.
This step covers cycle detection, topology and structural depth. It does not
authorize later steps, a merge, tag or release.

## Implementation

`lineage.cycles.analyze_cycles` consumes and revalidates the immutable Step 2
graph. Iterative strongly connected component detection counts cyclic components
once, including explicit self-parent evidence retained outside accepted adjacency.
Affected records include members and descendants along parent-to-child edges.
Disconnected loaded cycles remain errors even when target paths are unaffected.

Canonical traversal makes component ordering, witnesses, unaffected topology and
depth deterministic. Component detail is limited to 100 rows. A witness is a
closed path of actual edges, with explicit self-reference evidence permitted for
a self-loop. Witnesses longer than 64 edges are omitted with a reason. Internal
membership and affected sets remain complete for the next computation stage.

Structural depth is zero for an explicitly parentless record and one plus the
maximum parent depth only when all required paths are valid and complete.
Unknown grounding alone leaves structural depth available. Missing provenance,
absent/null declarations, invalid or unresolved parents, unavailable chronology
and cycle-affected paths produce explicit unavailable reasons. Whole-target depth
is unavailable if any target is unresolved or the target is empty; the resolved
subset maximum is separate. Generation semantics are unchanged.

Results use frozen data and detached read-only mappings. Diagnostics retain only
safe codes, severity and canonical identities. Analysis performs no file/network
access and is not dispatched by current validation, CLI audit or comparison.

## Verification

| Check | Actual result |
|---|---|
| Final focused regression command in `ci.yml` | 481 passed in 4.48 seconds |
| Separate focused CLI validation/comparison isolation command | 2 passed in 0.59 seconds |
| Direct T6 cases included in the 481-test run | 43 passed |
| Current specification, traceability and source-scope checks | PASS |
| Workflow YAML parsing and diff formatting | PASS |
| Independent implementation and oracle review | PASS; no remaining blocker |

The focused gate covers T6 behavior, parent graph/retention, reference resolution,
generation, input-only metric boundaries and current source/workflow checks.
The 43 T6 cases include the frozen cycle and depth fixtures, an independent
reachability oracle over 64 three-node directed graphs, a 1,500-node chain,
64/65-edge witness boundaries and 101 cyclic components. These bounded cases
establish direct behavior; they are not substitutes for the Step 9 measurements.
No raw test-count target was used.

Independent review found typed graph handoffs could retain a resolved reference
with no parent key, hide a self-reference outside retained self evidence, or
mislabel same-version chronology. Step 3 rejects these inconsistent inputs before
producing analytical results. Regression cases cover each failure. Fatal input
diagnostics also remain errors. Missing unrelated provenance metadata does not
erase complete structural depth.

The first separate CLI isolation run had one pass and one failure. The existing
test imported dependent modules while their helpers were already patched, leaving
a temporary blocking function cached in another module. Importing all relevant
modules before applying patches fixes the test-order dependency. The final two
cases pass and explicitly block graph/cycle/ancestry dispatch. No product CLI
code changed, and no failed run is counted as success.

Commands match the two focused invocations in `.github/workflows/ci.yml`; the
local regression also produced JUnit output. The local environment used Python
3.12.14 and pytest 9.1.1. No full matrix or release-level verification was run.

The existing source-scope check advances its single comparison commit to the
completed Step 2 and permits only `lineage/cycles.py`. The remaining 58 product
files and exact file inventory stay protected. Sixteen frozen specifications and
seven packaged resource copies remain unchanged. No new registry, historical
source migration or evidence framework is introduced.

## Handoff

Package version remains `0.1.0.dev3`; report schema remains `1.0`. This direct API
does not compute external roots, ancestry metrics or lineage bounds, and does
not integrate lineage into reports or CLI dispatch. The full environment matrix,
release builds, optional Parquet profile and actual 100k workloads remain their
designated candidate/performance gates. Hosted CI success is not claimed.

Step 4 can consume cycle membership, affected records and unaffected topology to
propagate complete external-root sets after its separate execution instruction.
