# Phase 6A Step 4 completion

Status: **COMPLETE: PROVENANCE AND DIRECT-CLOSURE CHANGES**.

The Theory Owner requested `Phase 6A Step 4 继续` on 2026-09-26
America/Los_Angeles (2026-09-27 UTC). Work starts from Step 3 commit
`e6f8b1f8e2f83907041e972d77d74bfc7101a919` on `phase6a-longitudinal`.

## Completed scope

The existing longitudinal coordinator now retains each nonempty snapshot's
`ProvenanceCompositionResult` and `DirectClosureExposureBounds`. It invokes the
accepted join, composition and direct-bound owners once per nonempty snapshot.
Source/confidence declarations, direct classifications, formulas, denominator
conventions and evidence classes remain unchanged. Context and representation
exclusions never enter or reduce the selected provenance population.

Pair results add separate row/required-field/grounding coverage deltas,
missing-provenance share change, five declared source-share changes and direct
lower/upper/width changes. All use F-018, later minus earlier, ratio units and
derived evidence. Each retains both population scopes, endpoint values, N,
coverage and reasons. No pooled denominator or representation-dependent source
share is introduced. Source-share deltas form an immutable five-category map;
missing provenance remains separate.

Explicit unknown, missing rows and incomplete required fields keep their existing
meanings. An absent manifest has source shares zero, missing share one and no
usable direct interval. Valid explicit unknown permits the conservative [0,1]
interval. Unavailable source fields leave all five source shares unavailable;
other known coverage values survive. Confidence never discounts grounding.
An empty snapshot retains null provenance/bounds and EMPTY_SCOPE without a
fabricated legacy join. Compatible record-count changes remain available.

Representation incompatibility or incomplete mapping coverage blocks all pair
deltas, while retaining the original snapshot results. Representation assignment
failure or exclusions alone do not remove independent provenance values when
the declared comparison basis is valid.

Required provenance/direct families no longer carry deferred execution status.
Complete error-free requested values yield completed execution; useful values
with unavailable or errored work yield partial; no valid comparison values yields
failed. Scalar availability is separate from wrapper execution: required-field
errors and strict-promoted warnings retain valid numbers but make affected
families partial. Unrelated local families retain their valid status.

Strict promotion policy is forwarded from the retained validation join and enters
the private selection binding. Scoped joins preserve existing full-input required
errors, including context errors. Those errors prevent overall completion without
being attributed to unaffected endpoint populations. Repeated inherited messages
are retained once in the overall series diagnostics.

Constructors check category inventory, full population binding, direct interval
counts/values/availability, endpoint denominators and new delta values. These
checks do not authenticate caller-created results against original inputs; public
consumer revalidation remains part of Step 6.

## Verification

Added **40 direct Step 4 tests**, covering the frozen three-version and Hero
oracles, all five categories plus missing rows, source/coverage/interval arithmetic,
absent and empty manifests, explicit unknown, missing/null/malformed fields,
empty and all-excluded populations, failed assignment, compatibility/mapping
gates, strict policy and stale bindings, context errors, immutable result
integrity and one numerical owner call per nonempty snapshot. Execution spies
confirm that lineage and resampling do not run.

Existing Step 3 tests now expect completed results where Step 4 removes deferral;
their distribution/state/tail oracles are unchanged. A completed-status forgery
test now uses an actually unavailable distribution endpoint. Graph/scenario/I/O
isolation remains in force.

Final targeted regression command:

```sh
/workspace/scratch/954124762a46/phase5_step8_env/bin/python -m pytest -q \
  tests/unit/test_longitudinal_provenance.py \
  tests/unit/test_longitudinal_analysis.py \
  tests/unit/test_longitudinal_selection.py \
  tests/unit/test_longitudinal_fixture_inputs.py \
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
  tests/integration/test_current_verification.py \
  tests/integration/test_no_network.py \
  tests/integration/test_no_algorithms.py \
  tests/integration/test_package_import.py \
  tests/integration/test_owner_ids.py \
  tests/integration/test_hero_end_to_end.py \
  -k 'not distribution_integrity and not sdist_extraction'
```

Result: **1699 passed, 14 deselected, zero failures**, in 32.07 seconds in the
existing Python 3.12 environment. The 14 unselected cases are unchanged archive
integrity/extraction checks. The new test file alone passed all 40 cases.

The first distribution/selection regression had 142 passes and 15 failures from
the obsolete Step 3 deferred/completed-status assertions. Updating those staged
expectations left the scientific oracles unchanged. Independent review then
identified an error-status gap: missing grounding or strict-promoted warnings
could retain an incorrect completed wrapper. That behavior was corrected and
covered by explicit local/global execution assertions. Review also prompted
narrow constructor checks rejecting forged direct intervals and availability.

The current checks passed:

```sh
python scripts/check_spec_consistency.py
python scripts/check_traceability.py
python scripts/release_check.py
git diff --check
```

They cover 16 frozen specifications, seven canonical resource copies and 41 owned
modules with local-only/layer boundaries. The source gate advances to Step 3,
protects **59 unchanged product files** and opens only `metrics/longitudinal.py`.
No mathematical kernel, input model, schema or package version was changed.
Final post-regression edits only order two imports and update documentation.

## Observed examples and remaining boundary

For v1 to v2, row/required coverage changes by -1/4; human/synthetic/missing shares
change by -1/2, +1/4 and +1/4. Direct lower/upper/width changes are +1/4, +1/2 and
+1/4. For v2 to v3, row coverage improves +1/4 while grounding coverage changes
by -1/12. Direct lower/upper/width changes are +1/12, +1/6 and +1/12. These retain
the distinction between evidence availability and declared composition.

The unchanged Hero has human/synthetic share changes -1/2 and +1/2, all three
coverage changes zero, and direct lower/upper/width changes +1/2, +1/2 and zero.
Its snapshot provenance and direct results equal explicit single-target calls.

Per-version joins retain full-input validation scans, so that portion grows with
both loaded input size and selected version count. The planned Step 8 preflight
must assess this cost; this step makes no performance or memory claim. No full
candidate matrix, package build, installed rerun or scale benchmark was run.

Runtime remains **0.1.0.dev4**, report schema **1.1**. No lineage execution,
CLI/config/schema integration, dependency, merge, tag or publication is added.
Frozen sources, canonical Hero and independent acceptance fixtures are unchanged.

**Step 4 is complete. Step 5 has not started.** The next planned scope is shared
selected-target lineage analysis and its named changes.
