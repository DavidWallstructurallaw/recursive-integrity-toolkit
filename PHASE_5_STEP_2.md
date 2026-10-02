# Phase 5 Step 2 Completion

Date: 2026-09-23 UTC. Status: **STEP 2 COMPLETE; PHASE 5 INCOMPLETE**.

The Theory Owner instructed `Phase 5 Step 2开始`. Work starts from
`5e946d1a42f87f89d4f97e9da4fd76cb05517caa` on `phase5-lineage`.
This step implements retained immediate-parent validation and immutable graph
construction. It does not authorize subsequent steps, a merge, tag or release.

## Delivered behavior

`resolve_parent_batch` shares single-reference interpretation with the existing
fail-fast resolver and builds one identity lookup per batch. Its immutable
per-record results preserve accepted and unresolved siblings when another
reference is ambiguous, malformed, a future parent or a direct self-reference.
The existing standalone resolver and generation API retain their behavior.
`validate_bundle` retains the batch without invoking analytical algorithms.

Original declaration counts include duplicate aliases. Identity-resolved counts
remain known when chronology is unavailable; cross-version graph edges require
chronology. Adjacency deduplicates canonical parent identities. Missing
provenance, absent declarations, null declarations and explicit empty lists stay
distinct. Malformed containers with unknown cardinality never become zero
declared parents. Existing ingestion still rejects malformed serialized input at
its established boundary; the retained batch also handles typed per-reference
failures without losing successful siblings.

`build_lineage_graph` supplies explicit target/context scope, canonical sorted
nodes, immutable parent and child adjacency, sanitized per-record evidence and
separate self-reference evidence. It revalidates retained input evidence and
rejects stale or forged handoffs. Same-version edges remain available for later
cycle analysis. Graph construction performs no file or network access.

`LineageLimits` enforces node and unique-edge admission. Exceeding a limit raises
a typed resource error and returns no partial exact graph. Root membership and
union-work limits are validated parameters reserved for Step 4. These limits do
not claim to bound already-loaded input memory or process RSS.

## Verification

| Check | Actual result |
|---|---|
| Final exact focused CI selection | 438 passed in 3.98 seconds |
| Provenance, observability, capability, evidence and CLI neighbors | 501 passed in 12.18 seconds |
| Direct parent-batch and graph cases within the focused selection | 15 batch cases and 40 graph cases passed |
| Current specification, traceability and source-scope checks | PASS |
| Diff formatting and independent implementation review | PASS; no remaining concrete blocker |

The earlier 398-test affected run is superseded by the final focused selection
and is not added to it. Independent review found two direct graph-construction
gaps: target nodes could be omitted with adjusted counts, and resolved reference
multiplicity could be falsified. Both are fixed and protected by direct
regressions. An initial graph static check found a missing implementation-status
annotation; it was restored and the complete static checks passed. The initial
graph test run had two empty-scope fixture-construction errors, corrected to use
the approved typed analytical input before the final passing run.

The final focused command matches `.github/workflows/ci.yml`, with local JUnit
output. The neighbor selection was:

```bash
python -m pytest -p no:cacheprovider -q \
  tests/unit/test_PR004_coverage.py \
  tests/unit/test_PR010_observability.py \
  tests/unit/test_PR011_capabilities.py \
  tests/unit/test_PR012_evidence_classes.py \
  tests/integration/test_phase4_cli.py
```

The three current static checks protect 55 unchanged product files, permit the
four approved implementation modules, retain the exact product inventory, and
verify 16 frozen specifications, 7 packaged resource copies and 40 owned modules.
The existing source-scope control and focused CI selection are updated in place;
no historical migration, approval registry or evidence framework is added.

Local environment: Python 3.12.14, pytest 9.1.1, NumPy 2.5.3 and pandas 3.0.6.
This step does not run the full regression, OS/Python/dependency matrix, optional
Parquet profile, release builds, clean installs or 100k performance workloads.
Hosted CI success is not claimed.

## Handoff

Package version remains `0.1.0.dev3`; report schema remains `1.0`. Graph execution
is a direct opt-in API. The audit/validate CLI, report assembly and ordinary
metric pipeline do not dispatch lineage analysis. General cycles, depth, roots,
ancestry metrics, schema 1.1 and lineage CLI/context inputs remain later steps.

Step 3 may consume immediate adjacency and retained self-reference evidence to
implement iterative cycle analysis and structural depth after its separate
execution instruction.
