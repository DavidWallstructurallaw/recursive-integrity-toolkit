# Performance measurements

Current Phase 6B Step 7 adds the bounded simulation observations described below.
These measurements retain the existing admission limits and introduce no new
performance SLA. The Phase 6A Step 9 reference schedule runs the actual 100k longitudinal workload
once on the designated Ubuntu/Python 3.12 reference profile. The case starts
in its own pytest process before a second invocation executes the remaining
performance cases once. Both invocations retain JUnit, complete reports and
per-attempt observations. Step 8 bounded preflights remain historical evidence.
Compatibility cells run bounded structural cases outside this performance
directory. The existing complete 100k metadata benchmark and 100k deep-chain
ancestry API measurement retain their distinct scopes.

Phase 4 Step 10 extends the retained Phase 3 calculation observations with public
CLI audit measurements ending only after both `report.json` and `report.md` have
been published. The original Phase 3 test functions and measurement fixture remain
available alongside the current lineage observations.

## Phase 6B bounded simulation reports

`test_simulation_complete_reports` executes two declared closed/reopened workloads
through the public audit command, including ordinary audit calculations, scenario
admission and sampling, report assembly, validation, JSON and Markdown publication.
Each attempt starts a fresh interpreter. The exact inputs and environment, every
outer wall time, complete output sizes, and process peak RSS are retained in the
existing measurement JSON and JUnit properties. No fastest-attempt selection occurs.

| Profile | States | Transitions | Replicates | Sample size | Models | Admitted state cells | Attempts |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Packaged small example | 2 | 6 | 3 | 2 | 2 | 84 | 3 |
| Representative bounded | 32 | 64 | 8 | 64 | 2 | 33,280 | 1 |

Both use seed 17 and reopening weight 1/4. The small case retains the packaged
initial vector `(1, 0)` and external vector `(0, 1)`. The representative case uses
32 literal states, with initial mass uniform over the first 16 and exact zero in
the rest; external mass is uniform over the last 16 and zero in the first half.
Both load exactly two independent audit records from the packaged example.
Scenario state cells are recorded separately from that actual record count.
Input construction and post-run assertions are excluded from the measured interval.

The optional timing wrapper measures the actual `run_scenario_experiment` call
inside the audit, including admission, sampling, the closed analytic baseline and
comparison. It is nested within the complete CLI interval and excludes report
assembly/publication. The outer subprocess wall includes interpreter startup,
imports and measurement bookkeeping. These intervals have different scopes; the
scenario-only interval does not represent product response time.

These runs disable `tracemalloc` to observe ordinary process cost. Linux peak RSS
uses `/proc/self/status` `VmHWM` for the executed image, avoiding the fork-parent
high-water floor retained by `getrusage().ru_maxrss` across exec. Before/after values
are process high-water marks, never incremental allocation estimates. Windows
retains `PeakWorkingSetSize`, macOS retains its byte-valued `ru_maxrss`. Native and
interpreter memory are included. The 180-second timeout only bounds runaway tests;
it is not a latency target. Full million-cell capacity, laptop performance and a
cross-platform performance envelope remain unmeasured by these bounded cases.

Independent assertions check all realized counts and frequencies, support,
diversity, exact extinction/re-entry identities, supplied mixing probabilities,
closed analytic expectation, zero-record scenario scope, experimental evidence and
retained ordinary audit results. JSON retains every admitted path and state vector.
Markdown's 100-row limits must disclose the exact omitted rows. Same-environment
replay equality is checked across all three small runs, without asserting trajectory
equality across differing NumPy versions or operating systems.

Step 7 measured all four scenario attempts successfully on Linux 6.18.44 x86_64,
glibc 2.39, Python 3.12.14, NumPy 2.3.5, pandas 2.2.3, PyArrow 25.0.1 and
pytest 9.1.1. The runtime reported AMD EPYC 9V74 80-Core Processor and nine
logical CPUs. Runs were serialized with other heavy tests paused. No failed or
timed-out performance attempt occurred. Every value below is retained, rounded
only here for display; observation JSON keeps the original precision.

| Attempt | Outer wall (s) | CLI interval (s) | Actual experiment (s) | RSS before (bytes) | RSS peak after (bytes) | JSON bytes | Markdown bytes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Small 1 | 0.365786 | 0.312016 | 0.044696 | 10,665,984 | 38,694,912 | 163,582 | 139,535 |
| Small 2 | 0.369446 | 0.319516 | 0.044991 | 10,661,888 | 38,690,816 | 163,581 | 139,534 |
| Small 3 | 0.360281 | 0.310766 | 0.045303 | 10,661,888 | 38,694,912 | 163,581 | 139,534 |
| Representative 1 | 4.673421 | 4.606455 | 0.088043 | 10,665,984 | 152,576,000 | 8,229,291 | 194,568 |

The complete two-test invocation passed in 6.14 seconds, including parent-side
report assertions. JUnit is retained at
`/workspace/scratch/954124762a46/phase6b_step7_performance.xml`; per-attempt
observations and both report formats are under the adjacent
`phase6b_step7_performance/` directory. These local observations support bounded
execution and complete publication for the declared inputs. They establish no
million-cell extrapolation or replacement for Step 8 candidate performance gates.

The existing `test_phase4_step10_hero_complete_report_runtime` separately exercised
the shared fixture's default no-profile path: one test passed in 3.50 seconds.
Its three untraced outer wall times were 0.365172, 0.353295 and 0.347950 seconds;
CLI intervals were 0.312867, 0.306678 and 0.299047 seconds. Peak RSS values were
28,188,672, 28,311,552 and 28,188,672 bytes. The separate traced attempt took
2.304133 seconds outer wall and 2.235637 seconds CLI, with peak RSS 44,830,720
bytes and traced Python peak 15,088,536 bytes. All simulation timing fields were
null, and all Hero assertions passed with no requested simulation. These four
compatibility attempts are separate from the four scenario attempts above.
Complete observations/reports and JUnit are retained under
`/workspace/scratch/954124762a46/phase6b_step7_performance_hero/` and the adjacent
`phase6b_step7_performance_hero.xml`. No attempt failed or timed out.

## Complete Hero audit

`test_phase4_step10_hero_complete_report_runtime` uses the five canonical Hero
input files, an explicit earlier/later pair and the declared literal topic meaning.
Each attempt starts a fresh Python interpreter. All three untraced attempts are
retained, followed by one separate allocation-traced attempt. There is no warm-up
exclusion or selection of the fastest run. Independent assertions retain support
8 and 5, diversity 7/8 and 3/4, support delta -3, retention 5/8, and the later
version's direct closure interval [1/2, 1/2].

The under-five-second target is compared with the outer untraced subprocess wall
time, including interpreter startup, imports, complete audit and publication, and
small measurement-wrapper bookkeeping. The separately recorded CLI interval starts
before its import and stops after publication. Container observations identify the
recorded reference hardware; they do not certify every common laptop. A repeatable
target miss requires explicit review under P4-D08 before acceptance.

`test_hero_lineage_complete_report_runtime` measures the same canonical inputs
with `--lineage` in three fresh, untraced processes. It additionally asserts
G=8, C=U=0, five roots, HHI=1/4, four effective roots and lineage bounds `[0,0]`.
All three outer wall times are reviewed against the same under-five-second
reference target. No fastest-run selection or universal laptop guarantee applies.

## Phase 6A complete longitudinal reports

`test_longitudinal_hero_complete_reports` uses the unchanged canonical Hero
files with explicit longitudinal mode, with and without lineage. Each mode
retains three fresh untraced attempts, including full JSON and Markdown
publication. The expected supports remain 8 and 5, diversity 7/8 and 3/4,
support retention 5/8, and direct closure change +1/2. Lineage additionally
requires roots 8 to 5, HHI 1/8 to 1/4 and effective roots 8 to 4. Every outer
wall time is reported against the existing under-five-second reference target;
a miss requires review and remains in the evidence.

`test_longitudinal_bounded_complete_reports` and
`test_longitudinal_100k_complete_reports` share one deterministic generator.
The loaded total includes exactly 100 context anchors and three equally sized
selected versions. Thus totals 1,000, 10,000 and 100,000 have respectively 300,
3,300 and 33,300 records per selected version. Step 8 selects the first two
sizes. The 100,000-record test remains a separately selected Step 9 candidate
measurement; a bounded observation never replaces that measurement.

For selected version indices 0, 1, 2, topic and target-supported anchor counts
are respectively 100, 50, 25. Row `i` has topic `s{i % support:03d}` and one
parent `roots::r{i % support:03d}`. All context rows are confirmed human,
parentless, explicitly externally grounded anchors. Version 1 is human and
explicitly grounded with the accepted one-parent carryover declaration.
Version 2 alternates those declarations on even rows with confirmed synthetic,
ungrounded, generated records on odd rows. Version 3 uses the latter synthetic
declaration throughout. Every target has generation 1; context has generation
0. Required content is fixed synthetic metadata and receives no content
similarity analysis. Comparison file arguments are deliberately reversed;
explicit configuration supplies chronology. Baseline `first` requests the
three unique pairs v1/v2, v1/v3 and v2/v3.

Independent exact-rational expectations, authored directly from those rules:

| Quantity | v1 | v2 | v3 |
| --- | ---: | ---: | ---: |
| Topic support | 100 | 50 | 25 |
| Diversity | 99/100 | 49/50 | 24/25 |
| Human / synthetic shares | 1 / 0 | 1/2 / 1/2 | 0 / 1 |
| Provenance row / required / grounding coverage | 1 / 1 / 1 | 1 / 1 / 1 | 1 / 1 / 1 |
| Direct closure lower and upper | 0 | 1/2 | 1 |
| Grounded / closed / unresolved target counts | N / 0 / 0 | N / 0 / 0 | N / 0 / 0 |
| Distinct roots | 100 | 50 | 25 |
| HHI | 1/100 | 1/50 | 1/25 |
| Effective roots | 100 | 50 | 25 |
| Lineage lower / upper / width | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 |

All source-share, coverage, direct-bound and lineage deltas are checked as
later minus earlier against these independent quantities. Support disappearance
and retention are checked exactly. For loaded total T, graph admissions are T
nodes and T-100 edges, stored root memberships are T, union visits are T-100,
and maximum depth is 1. The selected total is T-100; the 100 context anchors
never enter a snapshot denominator. The ordinary primary-only lineage summary
counts both comparison populations and the anchors as its context, which is
reported separately from the series context count.

No resource limits are raised: graph defaults remain 200,000 nodes, 1,000,000
edges, 1,000,000 root memberships and 10,000,000 root-union visits. The existing
measurement fixture records construction-excluded fresh-process wall time,
CLI interval, actual process peak RSS, both report sizes, exact input bytes and
hashes, environment, command and all stdout/stderr. An additional ordinary
JUnit property records selected/context populations, versions, pairs, state
counts, graph work and the separately timed input construction. There is no
allocation tracing for these workloads, no fastest-run selection and no new
benchmark service or registry.

The historical Phase 6A measurements used a counter that can report an inherited
pre-CLI RSS high-water floor across fork/exec. Both before/after values are
retained. A report that finishes below that floor cannot establish the smaller
workload's own peak; disclose the floor and do not subtract it. This occurred
for the final compact and Hero measurements after parent-side parsing of the
10,000-record report. Their wall times and scientific checks remain complete,
while their recorded RSS is explicitly subject to that inherited floor. The
1,000- and 10,000-record runs exceeded their own pre-CLI floors. The standalone
100k selection starts a separate pytest process for its single workload.

Bounded reports have a 300-second process guard. The full reference workload
has a provisional 1,800-second guard, to be reviewed with its actual Step 9
measurement. These limits bound test operation; they do not establish a new
runtime or RSS SLA, extrapolate a measured 100k result, or change analytical
resource defaults. Full attempts remain recorded even when a guard expires.

Exact selection commands:

```sh
# Step 8, initial small workload and all six Hero attempts.
python -m pytest tests/performance/test_longitudinal_runtime.py -k 'hero or 1000]' --junitxml=longitudinal-small.xml
# Step 8, bounded larger preflight after reviewing the small observation.
python -m pytest 'tests/performance/test_longitudinal_runtime.py::test_longitudinal_bounded_complete_reports[10000]' --junitxml=longitudinal-10k.xml
# Step 9 reference profile, actual full workload once.
python -m pytest tests/performance/test_longitudinal_runtime.py::test_longitudinal_100k_complete_reports --basetemp=/absolute/unused/longitudinal-100k --junitxml=longitudinal-100k.xml
```

See [Step 8 results](../../PHASE_6A_STEP_8.md) for the actual preflight evidence
and the scoped investigation of repeated work.

`test_longitudinal_many_versions_complete_reports` retains one untraced complete
CLI observation for the compact profile-investigation workload: 20 selected
versions of 10 rows each plus 20 context anchors, 220 total loaded rows. Each
selected version contains ten uniformly occupied topics and one reference per
row to the corresponding first ten context anchors. All selected provenance is
confirmed synthetic and directly ungrounded. All context is confirmed human and
externally grounded. Thus each snapshot has support 10, diversity 9/10, direct
closure [1,1], G=10, C=U=0, ten external roots, HHI=1/10, ten effective roots,
and lineage closure [0,0]. All available deltas are zero. Baseline `first`
produces 37 unique comparisons, comprising 19 adjacent and 19 baseline pairs
with their first pair shared. Shared graph work is 220 nodes, 200 edges, 220
root memberships and 200 union visits at depth 1. The test has a 180-second
guard and uses exactly the input bytes of the bounded cProfile investigation.
The profiled observations are labeled separately and never compared as ordinary
untraced wall times. Structural tests additionally verify pair scheduling and
shared work independently of runtime.

```sh
python -m pytest tests/performance/test_longitudinal_runtime.py -k many_versions --junitxml=longitudinal-many-versions.xml
```

## Current sparse lineage and fan-in

`test_sparse_lineage_100k_api` runs once on the Linux/Python 3.12 reference
profile in a fresh interpreter. It loads actual JSONL files and executes complete
input validation, including expected generation, then graph construction,
cycles/depth, roots and concentration. The 100,000 primary records use version
`m`, IDs `n000000` through `n099999`, fixed synthetic content and topic
`s{index % 20:02d}`. Only the final record is a parentless externally grounded
anchor; every preceding record declares the next ID as its parent and
generation `99999 - index`. Confidence is confirmed; non-anchor source is
synthetic, grounding is no and transformation is generate. No context is loaded.

Independent expectations are 99,999 unique edges, depth 99,999, 100,000 logical
root memberships, 99,999 union visits, G=100,000, C=U=0, one distinct root and
HHI/effective roots both 1. Every target root set and every expected generation
is checked. This API run does **not** serialize full audit JSON/Markdown or run
ordinary metric families. Its reported output size is the small API summary,
not an audit report. This distinction prevents comparison with Phase 4's full
metadata report workload.

`test_sparse_lineage_bounded_complete_reports` uses the same generator at 1,000
records through the full CLI, ending after JSON and Markdown publication.
`test_high_fan_in_lineage_complete_reports` loads 64 parentless context anchors
in `v1` and 64 targets in `v2`, each depending on all 64 anchors. It asserts
4,096 edges/visits, 4,160 memberships, depth 1, HHI=1/64 and 64 effective roots.
The context remains outside the target denominator. Separate bounded canonical
tests exercise repeated paths through multiple union layers and failure exactly
at the next rejected budget unit. Compatibility jobs run these structural tests
without repeating the expensive reference benchmark.

The API measurement records command, input sizes/hashes, environment, return
code, all stdout/stderr, elapsed time, actual process peak RSS, graph/root counts
and summary size in its ordinary JUnit observation and temporary output.
It uses no allocation tracing. The two CLI workloads reuse the existing report
measurement fixture. There is no new benchmark service, registry or receipt chain.
See [Step 9 results](../../PHASE_5_STEP_9.md) for the actual reference baseline.

## Deterministic metadata audit

`test_phase4_step10_metadata_100k_complete_report_runtime` constructs exactly
100,000 records with a simple topic representation. For zero-based row `i`:

- Dataset version is `m`; record ID is the six-digit decimal form of `i`.
- Topic is `s` followed by the two-digit decimal form of `i % 100`.
- The required content field is the fixed text `synthetic metadata` and is not
  analyzed. Exact duplicates and similarity are not requested. The topic field
  distribution is the sole completed content-diagnostics scope, reported as
  `supplied_distribution:audit-representation`.
- Provenance is omitted when `i % 10 == 9`.
- Otherwise, the source class is `(human, synthetic, mixed, sensor, unknown)` at
  index `(i // 10) % 5`, and confidence is `confirmed`.
- External grounding is `yes` for human/sensor, `no` for synthetic, and `unknown`
  for mixed/unknown. Unknown grounding and absent provenance stay unresolved.

These rules independently imply the following aggregate expectations. They are
asserted against the completed JSON report and are not generated from production
metric functions.

| Quantity | Expected value |
| --- | ---: |
| Records | 100,000 |
| Topic states | 100 |
| Records per state | 1,000 |
| Gini-Simpson diversity | 1 - 100(1/100)^2 = 0.99 |
| Supplied provenance rows | 90,000 |
| Missing provenance rows | 10,000 |
| Supplied rows per source class | 18,000 |
| Each source share over all records | 0.18 |
| Provenance row and required-field coverage | 0.9 |
| Known open / closed / unresolved | 36,000 / 18,000 / 46,000 |
| Direct lower / upper / width | 0.18 / 0.64 / 0.46 |

Synthetic CSV/config construction is timed separately and excluded from audit
wall time. One complete untraced audit records actual fresh-process peak RSS.
There is no fixed throughput threshold. The 100,000-record Python allocation peak
is explicitly not measured. A matched 1,000-record untraced/traced diagnostic pair
records allocation and tracing overhead for that bounded workload only; the same
generator, source classes and partial-provenance rules apply. Its observed tracing
overhead motivated keeping full-scale execution untraced; an additional allocation
trace was projected to take hours and was not run. The bounded observation never substitutes for
the actual 100,000-record audit or its independent correctness assertions.
The whole public report path, including warnings from partial/unknown provenance,
must complete; a smaller fixture does not substitute for the 100,000-record gate.

## Timing, memory and retained evidence

The shared `phase4_step10_measure_reports` fixture attaches every attempt as a
`phase4_performance` JUnit property and writes its complete JSON observation next
to the generated reports. It records actual commands, inputs and SHA-256/byte
sizes, CPU/Python/platform/dependency context, exit status, stdout/stderr, elapsed
times, both report byte sizes, allocation observations and RSS method.

`tracemalloc(1)` runs only in separately labeled traced processes (Hero and the
bounded metadata observation, with their actual record counts) and covers Python
allocations during CLI import and audit. It excludes allocations made before that
interval and untracked native allocations. Its runtime divided by the first
untraced runtime is a descriptive tracing-overhead observation; scheduling and
filesystem cache state can also affect that ratio.

RSS now uses `/proc/self/status` `VmHWM` on Linux,
`getrusage(RUSAGE_SELF).ru_maxrss` on macOS and other Unix systems, or
`GetProcessMemoryInfo.PeakWorkingSetSize` on Windows. It covers the fresh process,
including interpreter/native allocations, and is reported separately from Python
allocation peak. The before/after RSS high-water marks are not subtracted or
presented as exact incremental audit memory. Full-scale metadata observations
record null Python-allocation fields with an explicit omission reason, rather than
reporting a bounded-run value or extrapolation as a measured 100,000-record peak.

A 60-second per-attempt Hero timeout and 1,800-second metadata timeout bound test
execution. Lineage uses 600 seconds for the 100k API and 180 seconds for either
bounded CLI case. The measured 123.36-second API run leaves approximately 4.9x
operational headroom in that 600-second guard. The existing 75-minute reference
CI job limit is unchanged. These are resource guards, not performance targets.
A killed or failed attempt remains in the recorded evidence and fails the measurement test; it is
not silently replaced by a successful retry.

Example commands, from a prepared test environment:

```sh
python -m pytest tests/performance/test_hero_runtime.py -k phase4_step10 --junitxml=hero-performance.xml
python -m pytest tests/performance/test_metadata_100k.py -k phase4_step10 --junitxml=metadata-performance.xml
python -m pytest tests/performance/test_sparse_lineage_100k.py --junitxml=lineage-performance.xml
python -m pytest tests/performance/test_hero_runtime.py -k hero_lineage --junitxml=lineage-hero.xml
```

Only measurements with the same dataset, product path, tracing mode, environment
and practical hardware/resource conditions form a comparable regression baseline.
The inherited Phase 3 calculation-only timings do not measure the Phase 4 complete
report path. Comparable runtime growth above 20% or memory growth above 50%
requires review. Every attempt, including failed preliminary fixture construction
or target misses, belongs in execution evidence. These observations cover the
implemented audit, explicit lineage and the selected Phase 6A measurement scope.
Phase 6B experiments and model-performance claims remain outside these workloads.
