# Phase 6A Step 2 completion

Status: **COMPLETE: ORDERED SELECTION AND DECLARATION COMPATIBILITY**.

The Theory Owner requested `Phase 6A Step 2继续` on 2026-09-27 UTC. Work starts
from Step 1 commit `6f5cc9c64a93ed6442a867f869037ec57f1d2265` on
`phase6a-longitudinal`. This completion covers Step 2 only.

## Implemented behavior

- Added `metrics/longitudinal.py` with immutable `SnapshotDeclaration`,
  `LongitudinalMapping`, `SnapshotScope`, `LongitudinalPair` and
  `LongitudinalSelection`, plus selection and consumer revalidation entry points.
- Validates complete primary/comparison populations, disjoint context roles,
  exact declaration coverage, one selected version per physical input file,
  no fragmented snapshots, retained loaded inventory and explicit chronology.
  Lexical names, file paths and invocation ordering never supply series order.
- Emits adjacent pairs and optional first-baseline pairs in chronological order,
  deduplicating overlaps. Incompatible unmapped bases retain scheduled gaps and
  independent snapshot populations. Maps are pair-local and never composed.
- Shares existing descriptor/meaning/directed mapping checks through
  `validate_representation_basis`. The legacy pair API retains its loaded-endpoint
  requirement. Exact-content metadata selection now shares its descriptor with
  the existing assignment API; no content is read or assigned by selection.
- Explicit empty Python snapshots remain distinct from actual loaded versions.
  The actual primary role is preserved. Every pre-analysis representation scope
  remains `None`; empty or all-excluded distributions are not inferred here.
- Enforces the default 100 selected-version admission limit and a positive
  built-in integer override. At 100 snapshots, first-baseline mode has 197 pairs.
  Context versions consume no snapshot slots. Over-limit admission uses the
  approved `E_LONGITUDINAL_RESOURCE_LIMIT_EXCEEDED` code.
- Binds full canonical records/provenance, roles, order and declarations with a
  private digest. Consumer revalidation rejects stale same-ID state/content or
  parent evidence, shrunken populations and altered declarations. Physical paths
  and row positions are omitted; row/declaration permutations remain equivalent.

The additive Python mapping argument, pair compatibility fields and empty-primary
interpretation are recorded in `PHASE_6A_DECISIONS.md` and
`docs/longitudinal_contract.md`. No scientific definitions or frozen acceptance
inputs changed.

## Verification

Added **97 direct selection tests** covering the Step 1 fixtures, chronology,
roles/files, mapping directions and collisions, missing-state rules, default and
override limits, stale-input reuse, permutation/renaming invariance, immutability,
and absence of assignment, numerical, graph or file-access dispatch.

The final combined regression command was:

```sh
/workspace/scratch/954124762a46/phase5_step8_env/bin/python -m pytest -q \
  tests/unit/test_longitudinal_selection.py \
  tests/unit/test_longitudinal_fixture_inputs.py \
  tests/unit/test_T1_compatibility.py \
  tests/unit/test_T1_representation.py \
  tests/unit/test_PR006_duplicates.py \
  tests/unit/test_T1_support.py \
  tests/unit/test_T1_diversity.py \
  tests/unit/test_PR007_version_order.py \
  tests/integration/test_current_verification.py \
  tests/integration/test_no_algorithms.py \
  tests/integration/test_no_network.py \
  tests/integration/test_package_import.py \
  tests/integration/test_owner_ids.py \
  tests/integration/test_hero_end_to_end.py \
  tests/integration/test_phase4_cli.py \
  -k 'not distribution_integrity and not sdist_extraction'
```

Result: **842 passed, 14 deselected, zero failures**, in 26.84 seconds on the
existing Python 3.12 environment. The 14 unselected cases concern unchanged
archive integrity/extraction, outside this step's targeted run. No skipped
cases or full candidate matrix are claimed.

The first neighboring regression run had 839 passes and one failure: an old
package import test expected 40 modules. The new selection module makes 41.
Updated the affected import/owner/installed-helper inventory assertions to 41;
the final regression above includes import and owner checks. The installed
helper's count adjustment does not claim a new wheel build or installed run.

The existing checks passed:

```sh
python scripts/check_spec_consistency.py
python scripts/check_traceability.py
python scripts/release_check.py
git diff --check
```

They validate 16 frozen specifications, seven canonical resource copies, 41
owned modules and layer/local-only boundaries. The current source gate anchors
to Step 1, protects 56 unchanged product files and opens exactly four product
paths. Added two direct negatives requiring the newly authorized module to
exist as a regular file. Unrelated mutations, extra modules, deletions and
aliased source remain rejected by the existing checks.

## Boundaries and next step

Compatibility here validates declarations only. Actual state-table map totality
(including zero mass), field availability, representation exclusions and
numerical availability still require the existing assignment/pair kernels in
Step 3. Missing/conflicting order produces a structured selection error without
changing inputs. Preserving independently valid snapshots in a failed series
report remains a later coordinator/integration obligation.

The private selection binding is neither a public identifier nor an authenticity
certificate. Step 5 must additionally validate and bind the inherited retained
parent/graph evidence when selected lineage is requested. No graph traversal or
per-version numerical computation occurs in this step.

Package metadata remains `0.1.0.dev4`; report schema remains `1.1`. CLI/config
parsing, schema 1.2, distributions/deltas, selected lineage, full performance or
compatibility matrices, package rebuilding, PR merge, tag and publication were
not performed. The canonical Hero and frozen specifications are unchanged.

**Step 2 is complete. Step 3 has not started.** Its next authorized scope will
be snapshot distributions and observed changes using these validated scopes and
the existing numerical kernels.
