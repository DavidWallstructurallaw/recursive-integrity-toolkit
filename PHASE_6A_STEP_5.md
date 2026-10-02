# Phase 6A Step 5 completion

Status: **COMPLETE: SHARED SELECTED LINEAGE AND AVAILABLE CHANGES**.

The Theory Owner requested `Phase 6A Step 5 继续` on 2026-09-26
America/Los_Angeles (2026-09-27 UTC). Work starts from Step 4 commit
`390f5f6d11fcc1d54a3008dd9c09cd60a86ebde4` on `phase6a-longitudinal`.

## Completed scope

`lineage/ancestry.py` now provides `analyze_selected_lineage`,
`TargetLineageSummary`, `SelectedLineageResult` and
`validate_selected_lineage_result`. Explicit selection is revalidated before
building one loaded graph, running one cycle analysis and propagating roots once
under one common budget. Metadata is reassessed once. Each chronological target
uses its full selected population and the same retrospective graph evidence.

The ordinary primary-only graph and ancestry APIs retain their existing rules.
Shared graph/cycle objects remain anchored to the primary scope. Target-only
summaries carry their own scope, ancestry rows, root contributions, G/C/U,
coverage, original reference counts and depth summaries. No file role or retained
validation object is relabeled, and no full graph/cycle object is copied per
target. Immutable root sets, resource usage and diagnostics are shared within
the invocation.

The existing lineage bounds wrapper accepts the new target summary without
fabricating a legacy ancestry result. It retains C/N, (C+U)/N and U/N. Direct
bounds and existing single-target formulas are unchanged.

`analyze_longitudinal(..., lineage=True)` attaches the shared result, target
summaries and target bounds. Its ten named lineage deltas cover supporting-root
count, HHI, effective roots, unresolved parent references, reference coverage,
resolved/external ancestry coverage and interval lower/upper/width. Every delta
uses F-018, later minus earlier, original units, null representation and separate
complete target scopes. N, G and declared-reference denominators remain distinct.
The same representation compatibility and mapping-coverage gate controls these
comparisons, including their representation-independent values.

Lineage deltas use available/partial/unavailable report wrapper status while
leaving CalculationStatus unchanged. Partially resolved grounded-subset HHI can
remain finite with explicit partial coverage. G=0 concentration stays null.
Zero declared references preserve coverage one with explicit endpoint flags and
denominator zero. Known empty targets create no graph nodes, retain an empty
partition/root count zero and have unavailable population ratios/concentration.

Node/edge admission failure remains a typed exception in the standalone API.
The series coordinator catches it, preserves distribution/provenance/direct
results and reports failed lineage rows with exact resource usage. Known N
denominators survive. Root-stage exhaustion retains shared graph, cycle,
reference and depth evidence but removes every target's root partition and
concentration, including any earlier visited prefix. The shared budget never
resets between targets. Disconnected cycles retain global errors, so unaffected
finite values cannot produce an incorrect completed series.

Private binding combines the existing lineage evidence signature, selected input
binding and all four limits. The consumer validator rejects stale inputs,
selection, populations or retained parent evidence without rerunning graph
algorithms. Constructor checks bind target arithmetic and pair deltas to their
actual endpoints. These are consistency checks; public report consumers must
still revalidate caller-supplied root derivations during Step 6.

## Verification

Added **47 direct Step 5 tests**. Coverage includes the frozen complete, partial,
zero-grounded and Hero oracles; shared graph/cycle/root execution counts;
target-supported roots versus loaded anchors; full populations/context isolation;
multiple-root fractional allocation; N/G/reference denominators; reference alias
multiplicity; empty targets; zero-declaration convention; representation failure
and incompatible pairs; all four resource stages; disconnected cycles; future
parents; strict option types; changed parent/context/selection bindings; limit
binding; permutation invariance; and immutable result/status/value checks.

The old malformed-option test now rejects `lineage=True` with malformed limits,
because a valid explicit lineage request is implemented. No independent fixture,
Hero input or mathematical expectation changed. Existing malformed-parent syntax
continues to fail the selection boundary before graph construction.

The first joint analysis/provenance/lineage integration run had 124 passes and
five failures: two exposed a missing explicit later-side zero-grounded reason,
which was added; the other three were staged/test setup assumptions about the
old lineage gate, a missing Hero representation declaration and missing-parent
reference cardinality. Tests were aligned with the unchanged input contracts.
Further direct tests cover those distinctions. Independent review found no
remaining normal-calculation blocker.

Final targeted regression command:

```sh
/workspace/scratch/954124762a46/phase5_step8_env/bin/python -m pytest -q \
  tests/unit/test_longitudinal_lineage.py \
  tests/unit/test_longitudinal_provenance.py \
  tests/unit/test_longitudinal_analysis.py \
  tests/unit/test_longitudinal_selection.py \
  tests/unit/test_longitudinal_fixture_inputs.py \
  tests/unit/test_T4_ancestry.py \
  tests/unit/test_T6_cycles.py \
  tests/unit/test_lineage_graph.py \
  tests/unit/test_lineage_root_resources.py \
  tests/unit/test_lineage_concentration.py \
  tests/unit/test_lineage_bounds_proxy.py \
  tests/unit/test_lineage_fixture_inputs.py \
  tests/unit/test_lineage_context_inputs.py \
  tests/unit/test_phase5_lineage_config.py \
  tests/unit/test_PR004_coverage.py \
  tests/unit/test_PR005_source_shares.py \
  tests/unit/test_T3_provenance.py \
  tests/unit/test_T3_bounds.py \
  tests/unit/test_T1_compatibility.py \
  tests/unit/test_T1_representation.py \
  tests/unit/test_T1_diversity.py \
  tests/unit/test_T1_support.py \
  tests/unit/test_T2_tail.py \
  tests/unit/test_PR006_duplicates.py \
  tests/unit/test_PR007_version_order.py \
  tests/unit/test_PR017_content_refs.py \
  tests/unit/test_phase3_contracts.py \
  tests/integration/test_phase3_metric_pipeline.py \
  tests/integration/test_partial_provenance_report.py \
  tests/integration/test_cli_validation.py \
  tests/integration/test_phase4_cli.py \
  tests/integration/test_phase5_lineage_cli.py \
  tests/integration/test_phase5_lineage_reports.py \
  tests/integration/test_partial_lineage_report.py \
  tests/integration/test_phase5_lineage_privacy.py \
  tests/integration/test_current_verification.py \
  tests/integration/test_no_network.py \
  tests/integration/test_no_algorithms.py \
  tests/integration/test_package_import.py \
  tests/integration/test_owner_ids.py \
  tests/integration/test_hero_end_to_end.py \
  -k 'not distribution_integrity and not sdist_extraction'
```

Result: **2090 passed, 14 deselected, zero failures**, in 65.90 seconds in the
existing Python 3.12 environment. The 14 unselected cases are unchanged archive
integrity/extraction checks. The new test file separately passed all 47 cases.
Earlier targeted checks also passed 194 legacy graph/root/bounds cases, 269
existing longitudinal/bounds cases and 304 lineage/report-boundary cases; these
overlap the final suite and are not additional unique coverage.

The current protection checks passed:

```sh
python scripts/check_spec_consistency.py
python scripts/check_traceability.py
python scripts/release_check.py
git diff --check
```

They cover 16 frozen specifications, seven canonical resource copies and 41 owned
modules with local-only/layer boundaries. The source gate advances to Step 4 and
protects 57 unchanged product files, opening only `lineage/ancestry.py`,
`metrics/longitudinal.py` and `metrics/bounds.py`. Graph/cycle implementations,
configuration, report schema, canonical resources and package version stay
protected. No new module or dependency is added.

## Observed examples and remaining boundary

The complete three-version fixture has supporting roots 2/1/2, HHI 1/2, 1, 1/2,
and effective roots 2/1/2. Adjacent root changes are -1/+1, HHI changes +1/2/-1/2,
and effective-root changes -1/+1. The partial final target retains G=2, U=1,
HHI=1/2 and effective roots=2 over its grounded subset, with partial comparisons.
Its interval is [0,1/3]. The zero-grounded case preserves unavailable
concentration and its explicit later-side reason.

The unchanged Hero targets have supporting roots 8 to 5, HHI 1/8 to 1/4 and
effective roots 8 to 4. Their corresponding changes are -3, +1/8 and -4.
Direct and ancestry closure remain separately named and independently computed.

This step does not implement public series serialization, schema 1.2, CLI/config
enablement or installed longitudinal commands. Step 6 owns canonical report
assembly/privacy and the stronger consumer validation needed there. The earlier
selection-failure reporting boundary remains unchanged. Full-input provenance
join scans and complete series performance remain Step 8/9 measurement work.
No scale benchmark, full candidate matrix, wheel/sdist build or clean installed
rerun was performed here.

Runtime remains **0.1.0.dev4**, report schema **1.1**. No merge, tag, release or
Phase 6B work is included. Frozen sources and independent fixtures are unchanged.

**Step 5 is complete. Step 6 has not started.** The next planned scope is report
schema 1.2 and privacy integration.
