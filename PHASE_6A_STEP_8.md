# Phase 6A Step 8: bounded adversarial and scale preparation

## Authority and scope

The Theory Owner requested `Phase 6A Step 8 开始` on 2026-09-26
America/Los_Angeles (2026-09-27 UTC). This step starts from accepted commit
`9897ac7f531c3b1cbcd3b04ef4205f2c277540df` on `phase6a-longitudinal`.
The approved plan sections 5-6 govern the finite mutations, resource boundaries,
complete CLI preflights and reference workload. Package/schema remain
`0.1.0.dev4` / `1.2`. Step 9 candidate verification has not started.

## Narrow shared-work corrections

Complete CLI profiling found a full-input provenance join in every snapshot
calculation and consumer check. The coordinator now creates one fresh owner join
per consuming invocation and groups complete populations, immutable matches and
diagnostics once. Required-field errors retain their full-input visibility;
warnings, strict promotions, coverage, source categories and denominators retain
the independent scoped owner's semantics and ordering. Public consumers still
validate the original complete inputs. The retained input join is never trusted
as a cache. Failed-series validation reuses its own freshly checked join, and
standalone explicitly empty Python snapshots retain their prior behavior.

Report assembly groups input roles once after the series consumer check.
Selected-lineage certificate validation prepares `affected - members` once
before traversing nodes. The latter repeated set construction was demonstrated
at 25 and 313 loaded nodes, then reduced to one in each case. All edge, cycle,
depth, root, input-binding and arithmetic checks remain in place.

Only `metrics/longitudinal.py`, `reports/assembly.py` and `lineage/ancestry.py`
change in the product. There is no persistent cache, dependency, new package
module, public result type, schema change or new benchmark/mutation framework.

Ten shared-input tests compare projections against independent owner joins,
including strict mode, global errors, local warnings, metadata conflicts,
missing manifest rows, stale retained joins and explicit empty snapshots.
Two shared-structure tests count the actual certificate validator's set
construction. Full joins across public analysis plus result validation remain
four for both 2 and 12 selected versions. The complete CLI profile includes
additional existing boundaries, as recorded below.

## Finite semantic mutations

All eight concrete mutations were first run in an isolated checkout at the
accepted Step 7 baseline and rerun against the final three Step 8 production
files. Each experiment had eight passing unmodified controls and eight detected
mutants. Every mutant compiled and ran its intended existing test, with no
collection error or skip. Mutants were removed between attempts and are absent
from the delivered source.

| Injected fault | Existing test under `tests/unit/` | Actual detection |
|---|---|---|
| Reversed delta sign | `test_longitudinal_analysis.py::test_frozen_snapshot_and_pair_oracles[False-observed_three_version]` | Typed delta guard rejects disagreement with later-minus-earlier endpoints |
| Lexical chronology | `test_longitudinal_selection.py::test_fixture_selection_populations_and_pair_schedule[none-lexical_order_context_unloaded]` | Explicit primary chronology guard |
| Context included in N | `test_longitudinal_provenance.py::test_context_records_and_unused_order_entries_do_not_enter_provenance_denominators` | Typed snapshot population guard |
| Missing provenance folded into unknown | `test_longitudinal_provenance.py::test_all_five_source_categories_keep_missing_as_sixth_component` | Numerical assertion, unknown count 2 instead of 1 |
| Later-tail selection | `test_longitudinal_analysis.py::test_tail_uses_harmonized_earlier_counts_and_never_later_tail` | Typed tail guard rejects later selection in earlier scope |
| Incompatible pair accepted | `test_longitudinal_selection.py::test_incompatible_middle_retains_both_adjacent_gaps_and_valid_baseline` | Availability status assertion |
| Unavailable replaced by zero | `test_longitudinal_analysis.py::test_unavailable_evidence_does_not_execute_numerical_pair_or_imply_extinction[identified_empty_later]` | Typed unavailable-value guard |
| All-loaded roots replace target roots | `test_longitudinal_lineage.py::test_context_anchor_inventory_does_not_become_target_root_count` | Typed ancestry guard rejects inconsistent target root aggregates |

Five mutants stopped at typed semantic guards and one at the chronology guard;
their later numerical assertions were not reached. Two reached direct assertions.
This verifies the listed concrete faults without claiming exhaustive mutation
coverage. No new product fix was needed to detect them.

## Resource and detail boundaries

Six new integration cases exercise actual loaded populations:

- 100 selected versions execute exactly 99 adjacent or 197 deduplicated
  adjacent/first-baseline comparisons. A 101st selected version is rejected
  before snapshot kernels execute; no accepted prefix is calculated.
- 101 context versions do not consume selected-version slots. Two selected
  snapshots each have 250 states and 250 target-supported roots. Exact loss,
  addition and retention counts are 125 each, while displayed state/context
  details stop at 100. Hash/omit modes retain correct aggregate and omitted
  counts, and scopes use structural references without full identity inventories.
- A 400-node, 300-edge graph exhausts shared root-membership or union-visit
  budgets late in the traversal. Limits 350 and 299 reject attempted counts 351
  and 300 respectively. Every snapshot loses incomplete root outputs together;
  independent distribution/reference evidence and all three scheduled pairs
  remain. Budgets are not reset per target or comparison.

The initial two budget cases used invalid synthetic fixture transformation
`derive`; correcting it to the approved `generate` made the intended cases run.
The final regression includes the complete corrected module. No resource default
was raised and these cases found no additional production defect.

## Complete CLI measurements

Reference environment: Linux 6.18.44 x86_64, glibc 2.39, Intel Xeon Platinum
8370C at 2.80 GHz, nine visible logical CPUs, Python 3.12.14, NumPy 2.3.5,
pandas 2.2.3, PyArrow 25.0.1 and pytest 9.1.1. Measurements use the existing
`phase4_step10_measure_reports` fixture. Each attempt starts a fresh interpreter
and finishes after complete JSON and Markdown publication. Outer wall time
includes interpreter startup and wrapper bookkeeping; the CLI interval starts
before CLI import. Synthetic input construction is separately recorded and
excluded. These observations establish this container profile only.

The three-version workloads have 100 context anchors and equal selected
populations: 300 each at 1,000 total records and 3,300 each at 10,000. Explicit
chronology and baseline `first` produce three pairs. Topic/root supports are
100, 50 and 25; direct closure is 0, 1/2 and 1, and resolved lineage closure is
zero. Independent rational assertions check snapshots, every delta, missing
shares, disappearance, retention and graph work. Nodes/memberships equal the
loaded total; edges/union visits equal total minus 100; depth is one.

The compact workload has 20 selected versions of ten rows, plus 20 context
anchors, for 220 total rows and 37 pairs. Each snapshot has ten topics and
ten roots, HHI 1/10, direct closure one and lineage closure zero. All available
changes are zero. Shared graph work is 220 nodes, 200 edges, 220 memberships and
200 union visits. Its 23 input files match the profile investigation byte for byte.

Hero loads the unchanged two eight-record versions, with no series context,
one pair, supports 8 and 5 and diversity 7/8 and 3/4. Lineage uses 16 nodes,
eight edges, 16 memberships and eight union visits, with target roots 8 and 5.

All seven initial untraced attempts are retained in the following table.
Their JUnit includes commands, environment, input hashes, timing and output
sizes; the original temporary report directories were later cleaned by pytest.

| Workload / attempt | Outer seconds | CLI seconds | RSS counter bytes | JSON bytes | Markdown bytes |
|---|---:|---:|---:|---:|---:|
| 1,000 records, initial 1 | 12.276385 | 12.028554 | 98,222,080 | 4,417,638 | 3,020,503 |
| Hero, initial 1 | 0.959621 | 0.821057 | 47,714,304 | 283,790 | 318,606 |
| Hero, initial 2 | 0.902119 | 0.757718 | 47,714,304 | 283,791 | 318,607 |
| Hero, initial 3 | 0.998475 | 0.856228 | 47,714,304 | 283,791 | 318,607 |
| Hero + lineage, initial 1 | 1.110036 | 0.927026 | 47,714,304 | 312,509 | 342,561 |
| Hero + lineage, initial 2 | 1.156400 | 0.970304 | 47,714,304 | 312,510 | 342,562 |
| Hero + lineage, initial 3 | 1.013130 | 0.863719 | 47,714,304 | 312,510 | 342,562 |

All nine final untraced attempts are retained below. Known project CPU-heavy
jobs were paused for this run. All attempts exited zero, completed their
scientific/resource assertions and published both formats; no timeout fired.

| Workload / attempt | Outer seconds | CLI seconds | RSS counter bytes | JSON bytes | Markdown bytes |
|---|---:|---:|---:|---:|---:|
| 1,000 records, final 1 | 11.460723 | 11.287414 | 98,222,080 | 4,417,865 | 3,020,730 |
| 10,000 records, final 1 | 124.648722 | 124.284667 | 766,644,224 | 42,908,064 | 26,943,450 |
| 20 versions / 220 records, final 1 | 6.349237 | 6.163467 | 217,128,960 | 3,377,817 | 4,087,196 |
| Hero, final 1 | 0.987995 | 0.840246 | 217,128,960 | 283,790 | 318,606 |
| Hero, final 2 | 0.971557 | 0.825515 | 217,128,960 | 283,790 | 318,606 |
| Hero, final 3 | 0.935824 | 0.787099 | 217,128,960 | 283,790 | 318,606 |
| Hero + lineage, final 1 | 1.062200 | 0.886004 | 217,128,960 | 312,510 | 342,562 |
| Hero + lineage, final 2 | 1.110279 | 0.978555 | 217,128,960 | 312,510 | 342,562 |
| Hero + lineage, final 3 | 0.962738 | 0.827737 | 217,128,960 | 312,510 | 342,562 |

RSS is the process high-water mark, without subtraction. Initial Hero attempts
had an inherited pre-CLI floor of 47,714,304 bytes equal to their final counter.
Final compact/Hero attempts similarly inherited 217,128,960 bytes after the
pytest parent parsed the 10,000-record report. These values cannot isolate the
smaller workload's own peak or establish a memory regression. Initial/final
1,000-record floors were 30,945,280 / 29,929,472 bytes; the final 10,000-record
floor was 47,366,144 bytes. Those larger runs exceeded their respective floors.

Every initial and final Hero wall time is below the existing five-second
reference target. Matched initial/final timings show no greater-than-20% increase;
the 1,000-record RSS is unchanged. Hero RSS cannot support the comparable-memory
threshold review because of the inherited floors. Workload growth from 1,000
to 10,000 records is separately labeled and is not a same-workload regression.
No fastest-run selection, allocation-traced timing or 100k extrapolation is
used for acceptance.

The final selection reports **5 passed, 1 deselected in 151.25 seconds**;
the deselected case is the unexecuted 100k workload.

```sh
python -m pytest -q tests/performance/test_longitudinal_runtime.py -k 'not 100k' \
  --basetemp=/workspace/scratch/954124762a46/phase6a_step8_work/performance_final \
  --junitxml=/workspace/scratch/954124762a46/phase6a_step8_work/performance-final.xml
```

## Diagnostic profiling and output equivalence

All six cProfile attempts follow. Each uses 220 loaded records, including 20
context anchors; selected populations are 2 x 100 or 20 x 10, giving one or
37 pairs. Profiling includes its own overhead and excludes prior imports/input
construction. Initial successful profiles ran concurrently, so these timings
are diagnostic observations. Call counts provide the evidence for repeated work.

| Attempt | Seconds | RSS bytes | JSON bytes | Markdown bytes | Exit |
|---|---:|---:|---:|---:|---:|
| before v2 n220 | 5.498129 | 38,019,072 | unpublished | unpublished | 2 |
| before v20 n220 | 13.778959 | 46,256,128 | unpublished | unpublished | 2 |
| before v2 n220 absolute | 8.542082 | 42,975,232 | 1,030,409 | 529,197 | 0 |
| before v20 n220 absolute | 23.699841 | 67,743,744 | 3,377,426 | 4,086,805 | 0 |
| after v2 n220 absolute | 8.285001 | 42,975,232 | 1,030,405 | 529,193 | 0 |
| after v20 n220 absolute | 23.578917 | 67,698,688 | 3,377,403 | 4,086,782 | 0 |

The two rejected attempts used paths containing `..` and correctly returned
`E_OUTPUT_PATH_INVALID`, exit 2, with no report publication. The fixture was
corrected to resolved absolute paths without changing the product path policy.
All four complete attempts exited zero.

| Complete CLI work | 2 versions before / after | 20 versions before / after |
|---|---:|---:|
| Full provenance joins | 15 / 13 | 51 / 13 |
| Graph construction | 1 / 1 | 1 / 1 |
| Cycle analysis | 1 / 1 | 1 / 1 |
| Root propagation | 1 / 1 | 1 / 1 |
| Population preparation | 6 / 6 | 6 / 6 |
| Selection consumer checks | 5 / 5 | 5 / 5 |
| Full lineage input signatures | 7 / 7 | 7 / 7 |
| Selected-lineage consumer checks | 2 / 2 | 2 / 2 |
| Complete report validations | 5 / 5 | 5 / 5 |

Twenty-version provenance join cumulative profile time fell from 0.9457 to
0.2959 seconds. Complete report validation still dominates: its cumulative
time was 12.8862 seconds before and 13.1080 seconds after. The observations
support removal of version-dependent repeated joins, without establishing a
large overall speedup or justifying removal of public boundary validation.

Both complete JSON and Markdown formats match before/after for each workload
after normalizing only the exact per-attempt directory and five run fields:
`completed_at`, `config_hash`, `duration_seconds`, `run_id`, `started_at`.
All scientific, scope, status, diagnostic, resource and capability content is
preserved. The normalized format SHA-256 values are:

| Workload / format | SHA-256 |
|---|---|
| 2 versions, JSON | `b7562c77dd0d48fddcf8941002dd70e37aec663be68085c4524eed720983f020` |
| 2 versions, Markdown | `1aff38fb07eeb79f76ba9b0879c194a242f7c6c7f9caf476c8a0d09c5578975b` |
| 20 versions, JSON | `9a20bb5602820e7f473f883a6db457db8fe6a5cbf3d2ea3b82b62c0f02fd7aca` |
| 20 versions, Markdown | `a1cf90196c138c81ae557ab898102eaecf409493678bc567abff0995ef8954b0` |

## Reference workload and remaining limits

The same deterministic generator establishes **100,000 total loaded records**:
100 context anchors and 33,300 records in each of three selected versions.
It retains the same 100/50/25 topic and root supports, three pairs, depth one
and independent rational expected values. Expected graph work is 100,000 nodes,
99,900 edges, 100,000 root memberships and 99,900 union visits. This describes
the fixture and oracle; the full workload has not been executed in Step 8.

Step 9 selects that case once in a separate reference-profile pytest process.
Its 1,800-second guard is provisional. Bounded three-version guards remain
300 seconds, and the compact guard is 180 seconds. These operational guards
establish no wall-time/RSS SLA. Default node/edge/membership/union limits remain
200,000 / 1,000,000 / 1,000,000 / 10,000,000.

The 100-item detail cap bounds new displayed lists; ordinary report sections
still grow with loaded records. The 10,000-record report pair is about 69.85 MB
combined. Neither a constant-size full report nor measured 100k feasibility is
claimed. Broader report/validation redesign would require separate scope.

## Regression and integrity

The final source-focused run completed with **1962 passed, 1 deselected in
426.91 seconds**, zero failures and zero skips, across 47 selected test modules.
It includes all six new adversarial cases and all twelve shared-work cases.
The final performance selection separately passed five tests representing nine
complete CLI attempts. Finite mutation controls and expected mutant failures
are recorded separately above; they are not included in the regression count.

```sh
RIT_TEST_PARQUET=1 /workspace/scratch/954124762a46/phase5_step8_env/bin/python -m pytest -q \
  tests/unit/test_longitudinal*.py tests/unit/test_lineage*.py tests/unit/test_selected*.py \
  tests/unit/test_T3*.py tests/unit/test_T4*.py tests/unit/test_T6*.py \
  tests/unit/test_PR004*.py tests/unit/test_PR005*.py tests/unit/test_PR013*.py \
  tests/unit/test_PR014*.py tests/unit/test_PR015*.py tests/unit/test_PR016*.py tests/unit/test_PR017*.py \
  tests/integration/test_longitudinal_adversarial.py tests/integration/test_longitudinal_cli.py \
  tests/integration/test_longitudinal_example_resources.py tests/integration/test_longitudinal_reports.py \
  tests/integration/test_phase5_lineage*.py tests/integration/test_phase4_cli.py \
  tests/integration/test_partial*.py tests/integration/test_hero*.py \
  tests/integration/test_no_algorithms.py tests/integration/test_no_network.py \
  tests/integration/test_current_verification.py tests/integration/test_ci_workflows.py \
  tests/golden/test_phase4_reports.py -k 'not installed_without_pyarrow' \
  --junitxml=/workspace/scratch/954124762a46/phase6a_step8_work/regression.xml
```

The source regression covers all longitudinal unit cases, selected/legacy
lineage, provenance and closure owners, report schema/privacy/unavailable
semantics, source longitudinal CLI/examples/adversarial reports, legacy CLI
and lineage reports, partial evidence, Hero, no-network/no-algorithm boundaries,
current verification controls, CI declarations and ordinary report goldens.
Real PyArrow is enabled. The single installed-without-PyArrow golden is explicitly
deselected because existing local installations still contain Step 7 bytes;
the installed longitudinal module is outside this source-focused selection.
No current installed-wheel or full candidate-matrix result is claimed. Those
delivery checks belong to Step 9. Earlier focused passing counts overlap this
regression and are not added to its total.

The specification, traceability and current source gates passed. They retain
16 frozen specifications, five schemas, six canonical Hero files, 14 exact
packaged resource mirrors and 41 owned modules. Local-only/layer checks pass.
The current gate uses accepted Step 7 as its baseline, protects 72 product files
and admits only the three measured implementation paths. The frozen acceptance
fixtures, examples, schemas and package metadata are byte-identical to Step 7.
An independent read-only review found no remaining semantic, validation or
privacy defect in the three production changes and their direct regressions.

```sh
python scripts/check_spec_consistency.py
python scripts/check_traceability.py
python scripts/release_check.py
git diff --check
```

Execution evidence is under `phase6a_step8_work`: `regression.xml`/`.log`, the exact `regression-command.txt`,
`performance-final.xml`, `performance-final-summary.json`, complete final
attempt directories in `performance_final`, all six diagnostic attempts plus
`comparison.json` in `profile_review`, and both finite mutation experiments
in `mutations` and `mutations/current_runtime`. Initial untraced metadata is in
`step8-performance-baseline.xml` at the workspace root. These are execution
artifacts; reusable tests and this completion record are committed to the branch.

Step 8 is complete. Step 9 retains dev5 preparation, canonical regression,
supported OS/Python/dependency profiles, installed wheel/sdist checks, the actual
100k series measurement and candidate handoff. No merge, tag, release, registry
publication or Phase 6B execution is included.
