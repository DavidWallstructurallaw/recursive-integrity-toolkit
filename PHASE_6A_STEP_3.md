# Phase 6A Step 3 completion

Status: **COMPLETE: SNAPSHOT DISTRIBUTIONS AND OBSERVED CHANGES**.

The Theory Owner requested `Phase 6A Step 3 开始` on 2026-09-26
America/Los_Angeles (2026-09-27 UTC). Work starts from Step 2 commit
`72123128366363231cb96cc23912bb608a69807e` on `phase6a-longitudinal`.

## Completed scope

Implemented `analyze_longitudinal` in the existing coordinator. It revalidates
selection, groups the input once, computes each original unweighted snapshot
distribution once and executes the already selected adjacent/baseline schedule.
There is no all-pairs expansion. Assignment, distribution, harmonization,
comparison and tail selection retain their existing owners and formulas.

Snapshot summaries retain complete population scopes, actual representation
scopes, observed record/eligible/excluded counts and existing distribution
results. Pair summaries retain original and harmonized bases, F-005 support
change, F-018 diversity change, state loss/addition/intersection and retention.
The new F-018 record-count delta uses complete populations, independently of
representation exclusions. Delta wrappers reference both endpoint scopes,
values, denominators, coverage and reasons without a pooled denominator.

Optional earlier-tail disappearance selects the harmonized earlier distribution
with the supplied rule and intersects that tail with the observed missing set.
It retains the rule, sample size, descriptor, count and state set. A valid empty
tail or missing set has zero loss. Empty/all-excluded endpoint distributions
have null comparison state sets and explicit unavailable reasons. They never
imply that every earlier state disappeared.

Incompatible bases or missing mapping coverage block the pair, including record
delta, while preserving original snapshots and unrelated comparisons. Missing
field assignment preserves full record counts; optional-tail failures preserve
otherwise valid distribution comparisons. Constructor checks bind typed result
rows to populations, pair endpoints, formula ownership and execution state.

Added the existing content-mode declaration to the internal validation handoff.
This prevents local-reference paths from being treated as inline record text.
No content files are reopened during analysis. Nonempty local-reference
exact-content analysis remains unavailable because this handoff stores no
resolved payloads; field representations remain usable. Selection signatures
bind content mode along with their existing inputs.

## Verification

Added **60 direct analysis tests**. They cover the independent snapshot/pair
oracles, reappearance, null versus zero, mapped and unmapped bases, both mapping
directions, earlier-tail rules, pair-local failures, empty and excluded evidence,
denominator separation, context exclusion, permutation/renaming, stale binding,
typed results, retained content mode and the unchanged Hero pair. Execution
spies verify one distribution per snapshot and one comparison per scheduled
available pair. Blocked graph, provenance, bounds, scenario and I/O calls confirm
that Step 3 stays within its authorized scope.

Final targeted regression command:

```sh
/workspace/scratch/954124762a46/phase5_step8_env/bin/python -m pytest -q \
  tests/unit/test_longitudinal_analysis.py \
  tests/unit/test_longitudinal_selection.py \
  tests/unit/test_longitudinal_fixture_inputs.py \
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

Result: **1188 passed, 14 deselected, zero failures**, in 28.97 seconds in the
existing Python 3.12 environment. The 14 unselected cases are unchanged archive
integrity/extraction checks, outside this targeted run. The first direct analysis
test run had 48 passes and one test-only failure from an incorrect import in the
isolation test; it was corrected to the existing `metrics/resampling.py` owner.
No production behavior was changed to satisfy that test.

The current checks also passed:

```sh
python scripts/check_spec_consistency.py
python scripts/check_traceability.py
python scripts/release_check.py
git diff --check
```

They verify 16 frozen specifications, seven canonical resource copies, 41 owned
modules and layer/local-only boundaries. The source gate anchors to Step 2,
protects 57 unchanged product files and opens only `metrics/longitudinal.py`,
`models.py` and `io/validation.py`. The last two changes only retain the content
mode in the internal handoff. No mathematical kernel was modified.

## Observed examples and remaining boundary

The three-version oracle yields support 3/2/3, diversity 5/8, 1/2, 2/3 and
adjacent diversity deltas -1/8 and +1/6. B disappears and reappears; the baseline
comparison preserves its return while still showing C missing. The final
record-count change is -1. Mapping coarsens the earlier fine distribution in
the comparison only, and tail membership uses those harmonized counts.

The unchanged Hero pair retains support change -3, retention 5/8 and diversity
change -1/8. Its full-population record delta is zero. The explicit empty later
snapshot retains record delta -2 with unavailable support/diversity/state sets.
The all-excluded later snapshot retains record delta zero and unavailable
representation changes. These distinguish missing observations from zero loss.

Required provenance/direct-closure families remain explicitly `deferred` until
Step 4. Therefore a useful staged result has overall status `partial`; no valid
comparison values yields `failed`. This does not claim a completed full-series
report. Unrequested tail/lineage are explicitly not requested; lineage execution
is rejected until Step 5. Missing/conflicting chronology still fails selection
without modifying inputs; preserving independent snapshots in a failed public
series report remains a later integration obligation.

Package metadata stays `0.1.0.dev4`; report schema stays `1.1`. This step adds no
CLI/config integration, schema field, simulation, graph, provenance/direct-bound
change, dependency, full candidate matrix, performance claim, package build,
merge, tag or publication. Frozen specifications, canonical Hero inputs and
independent acceptance fixtures are unchanged.

**Step 3 is complete. Step 4 has not started.** The next planned scope is
per-version provenance and direct-closure summaries with their named deltas.
