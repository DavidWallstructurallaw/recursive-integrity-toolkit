# Cycle components and affected descendants

These Phase 5 Step 1 fixtures distinguish cycle members from descendants affected
along parent-to-child edges and from independent target records. A disconnected
cycle in the loaded context remains a whole-graph lineage error even when every
selected target has complete ancestry. General cycle detection starts in Step 3.

Current input validation accepts valid same-version references in the general
cycle cases, without establishing acyclicity. A direct self-parent already
produces `E_LINEAGE_CYCLE`; its expected input error is recorded separately.
Future graph construction must retain self-reference evidence for diagnosis while
rejecting it as a valid ancestry edge.

`cycle_count` counts cyclic strongly connected components. It never counts all
simple cycles, individual members or affected descendants. Future cycle failures
must preserve independent results and return an unsuccessful audit exit status.
Step 1 does not execute or claim any of those future graph results.

Shared fixture format and execution limits are documented in
`../lineage_complete/README.md`.
