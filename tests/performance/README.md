# Performance measurements

Current scheduling: Phase 5 candidate verification runs this directory once on
the designated Ubuntu/Python 3.12 reference profile. Compatibility cells run the
canonical suite without this performance directory. The existing complete 100k
report benchmark remains required. The sparse-lineage placeholder gains actual
execution in Phase 5 Step 9 and currently makes no graph performance claim.

Phase 4 Step 10 extends the retained Phase 3 calculation observations with public
CLI audit measurements ending only after both `report.json` and `report.md` have
been published. The original Phase 3 test functions and measurement fixture remain
unchanged. Sparse lineage remains deferred and is not measured here.

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

RSS is the peak resident process size from `getrusage(RUSAGE_SELF)` on Unix or
`GetProcessMemoryInfo.PeakWorkingSetSize` on Windows. It covers the fresh process,
including interpreter/native allocations, and is reported separately from Python
allocation peak. The before/after RSS high-water marks are not subtracted or
presented as exact incremental audit memory. Full-scale metadata observations
record null Python-allocation fields with an explicit omission reason, rather than
reporting a bounded-run value or extrapolation as a measured 100,000-record peak.

A 60-second per-attempt Hero timeout and 1,800-second metadata timeout bound test
execution. They are resource guards, not performance targets. A killed or failed
attempt remains in the recorded evidence and fails the measurement test; it is
not silently replaced by a successful retry.

Example commands, from a prepared test environment:

```sh
python -m pytest tests/performance/test_hero_runtime.py -k phase4_step10 --junitxml=hero-performance.xml
python -m pytest tests/performance/test_metadata_100k.py -k phase4_step10 --junitxml=metadata-performance.xml
```

Only measurements with the same dataset, product path, tracing mode, environment
and practical hardware/resource conditions form a comparable regression baseline.
The inherited Phase 3 calculation-only timings do not measure the Phase 4 complete
report path. Comparable runtime growth above 20% or memory growth above 50%
requires review. Every attempt, including failed preliminary fixture construction
or target misses, belongs in execution evidence. These observations cover the
implemented Phase 4 audit and do not certify deferred final-product Hero behavior.
