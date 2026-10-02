# Phase 5 Step 9 Completion

Date: 2026-09-26 UTC. Status: **COMPLETE; PHASE INCOMPLETE**.

The Theory Owner instructed `Phase 5  Step  9 开始`. Work starts from
`f1c5309deda3ae4107c78f025cb2a7bb85ba2881` on `phase5-lineage`.
This step completes bounded adversarial/mutation work and actual lineage scale
measurements under the approved plan. Step 10 candidate verification is separate.

## Concrete defect and bounded repair

The reverse-ID chain exposed two quadratic operations in
`validate_generation_declarations`: tuple membership for each provenance row,
and repeated scans when each child sorts before its parent. The initial probe
ran against the accepted Step 8 implementation, with preconstructed inputs.

| Records | Before: untraced seconds | After: untraced seconds | Before: generation line events / identity comparisons | After: same work observations |
|---|---:|---:|---:|---:|
| 128 | 0.02719 | 0.00819 | 61,652 / 17,784 | 6,542 / 1,528 |
| 512 | 0.25355 | 0.03486 | 934,676 / 267,768 | 26,126 / 6,136 |
| 2,048 | 4.20171 | 0.11949 | Not instrumented | Not instrumented |

Tracing and timing are separate runs. Four times the input formerly produced
more than fifteen times the counted work. The current bounded regression permits
six times the work, leaving sorting/implementation headroom while detecting both
observed quadratic defects without a flaky wall-clock assertion.

The sole runtime change is in `io/validation.py`: use a key set and an iterative
queue that consumes each validated immediate dependency once. Canonical input
sorting remains; the propagation itself is O(V+E) in time and auxiliary storage.
Grounding yes still resets expected generation to zero independently of its own
parents. Unknown, missing, invalid and stalled dependencies remain unavailable;
declarations never seed expectations and this validator never claims a cycle or
calculates ancestry/depth. Diagnostic contents, ordering and severity are retained.

A one-off differential check compared the entire result and messages with the
accepted implementation for 100 deterministic mixed dependency graphs in both
ordinary and selected-strict-warning modes: all 200 comparisons matched. The
old implementation was obtained from Git only for this experiment. No historical
source adapter or permanent differential framework was added.

The bounded layered fan-in check verifies 37 nodes, 133 edges and 192 logical
memberships. The full operation needs 257 candidate visits. A limit of 256 rejects
exactly visit 257 and returns unavailable root metrics, while preserving completed
structural observations. At 257 it completes with 32 roots and HHI=1/32. Existing
cycle, missing/unknown evidence, privacy and all four resource-boundary cases
remain in the canonical suite.

## Actual reference measurements

Reference: local Ubuntu 24.04.3 LTS, Linux 6.18.44 x86-64/glibc 2.39,
Intel Xeon Platinum 8370C at 2.80 GHz, nine visible logical CPUs, eight-CPU quota,
8 GiB cgroup memory limit and no swap. Python 3.12.14, NumPy 2.3.5, pandas 2.2.3,
pytest 9.1.1; PyArrow 25.0.1 was installed in the measuring environment, though
these JSONL/CSV workloads did not require it. This is local reference evidence,
not a claim that hosted CI or every supported environment has executed Step 9.

All six observations below use fresh interpreters, untraced wall time and actual
whole-process peak RSS. Inputs are built before timing; startup/imports and work
through output completion are included in outer wall time. There is no warm-up
exclusion or best-run selection. None was killed, timed out or retried.

| Workload and measured path | Wall seconds | Peak RSS bytes | Output bytes |
|---|---:|---:|---|
| 100,000 reverse-chain records, complete input validation plus ancestry API | 123.36372 | 1,836,056,576 | 939, API summary only |
| 1,000 reverse-chain records, full lineage CLI | 11.15276 | 131,334,144 | JSON 6,202,005; Markdown 1,532,005 |
| 64 roots and 64 targets, full high-fan-in lineage CLI | 2.04153 | 60,375,040 | JSON 610,673; Markdown 284,393 |
| Canonical Hero with lineage, attempt 1 | 0.98528 | 29,347,840 | JSON 240,712; Markdown 216,449 |
| Canonical Hero with lineage, attempt 2 | 1.08168 | 29,347,840 | JSON 240,713; Markdown 216,450 |
| Canonical Hero with lineage, attempt 3 | 1.01130 | 29,347,840 | JSON 240,712; Markdown 216,449 |

| Workload | Nodes / edges | Targets / context | Logical root memberships / union visits | Depth |
|---|---:|---:|---:|---:|
| 100k API chain | 100,000 / 99,999 | 100,000 / 0 | 100,000 / 99,999 | 99,999 |
| 1k CLI chain | 1,000 / 999 | 1,000 / 0 | 1,000 / 999 | 999 |
| High-fan-in CLI | 128 / 4,096 | 64 / 64 | 4,160 / 4,096 | 1 |
| Each Hero attempt | 16 / 8 | 8 / 8 | 16 / 8 | 1 |

The 100k worker spent 45.56481 seconds in import/loading/validation and 76.83787
seconds in ancestry analysis. Every expected generation and target root set was
checked. G=100,000, C=U=0, one distinct root, HHI=1 and effective roots=1; no
cycles or resource exhaustion occurred. Actual input sizes were 10,300,000 bytes
of primary JSONL, 22,388,875 bytes of provenance JSONL and 154 bytes of config.
The generator, commands and independent expectations are documented in
`tests/performance/README.md` and `test_sparse_lineage_100k.py`. Ordinary JUnit
observations retain exact input hashes, process status, stdout/stderr and sizes.

The **100k API measurement excludes full audit report serialization and ordinary
metric families**. Its small summary is not a 100k audit report. The separate
1k chain and high-fan-in CLI measurements include complete JSON and Markdown.
The 1k CLI probe and inherited large-report cost motivated keeping the expensive
100k run scoped to the approved graph requirement within this container's memory
budget. A 100k full lineage CLI audit was neither attempted nor certified.

Hero's three complete lineage-enabled runs all satisfy the reference
under-five-second target. Independent assertions retain G=8, C=U=0, five roots, HHI=1/4,
four effective roots, lineage bounds `[0,0]` and direct bounds `[1/2,1/2]`.
There is no universal laptop SLA. Phase 4's 1,362.47-second, 7.12-GiB metadata
audit is a different workload and provides no comparable lineage speedup claim.

Operational guards are 600 seconds for the actual 100k API, 180 seconds for
either bounded CLI case and the existing 60 seconds per Hero attempt. The
600-second guard is approximately 4.9 times the observed API runtime. The
existing 75-minute reference CI job is unchanged. These are execution guards,
not new product performance promises. Same-workload regressions above 20% time
or 50% memory still require review. Root-set growth beyond sparse traversal
remains constrained by the existing membership and union-visit budgets.

## Finite mutation experiment

The unmodified selected suite passed all 23 cases. Each of seven isolated
source copies received one compilable mutation and was tested against existing
behavioral assertions. Every mutant exited pytest with a test failure, not an
import/collection error. Runs stopped at the first detected failure. Test names
below omit their common `test_` prefix. No production file was mutated by the
experiment, and no mutation runner or registry is shipped.

| Seeded defect | Existing detecting case | Result |
|---|---|---|
| Use G instead of N for incidence share and its denominator | `unequal_supports_use_n_for_incidence_and_g_for_weights` | Killed |
| Charge a new root membership for every duplicate candidate in a union | `root_union_counts_duplicate_candidates_but_deduplicates_alias_edges[False]` | Killed |
| Mint a grounded carryover record as its own root | `carryover_inherits_single_canonical_parent_including_known_empty[yes-expected_roots0]` | Killed |
| Omit the unknown-grounding failure branch, allowing a closed empty set | `missing_provenance_unknown_and_undeclared_boundaries_never_become_empty_roots` | Killed |
| Empty the initial queue for cycle-descendant propagation | `frozen_cycle_oracles_and_unaffected_topology[two_node_cycle_and_descendants]` | Killed |
| Exchange lineage lower and upper formulas | `frozen_partition_bounds_and_shared_root_evidence[unknown_absent_and_null_boundaries]` | Killed |
| Return HHI instead of its reciprocal as effective root count | `unequal_supports_use_n_for_incidence_and_g_for_weights` | Killed |

The union mutation specifically checks duplicate-counting in logical storage and
the resulting premature resource failure. The cycle mutation is caught by the
existing incomplete-topology rejection. These seven results describe the bounded
experiment; they do not claim an exhaustive mutation score or prove absence of
other defects.

## Regression and attempt accounting

The final affected selection covers 34 modules and 1,602 distinct cases:
generation/parent inputs, loaders and normalization neighbors, observability,
graphs/cycles/ancestry/bounds, CLI, reports/goldens/privacy, no-network behavior
and existing source/workflow controls. Real Parquet cases ran in the environment
with PyArrow. This was not the full canonical or cross-platform candidate suite.

The first combined run yielded **1,601 passed and one failed in 160.60 seconds**.
The installed-without-PyArrow golden detected that the test interpreter still
contained the Step 8 wheel: its installed `io/validation.py` hash disagreed with
the current checkout. The source-identity check correctly rejected that stale
installation. No product assertion, golden or runtime code was changed to bypass
it. After building/installing the current wheel, **all 72 report-golden cases
passed in 19.01 seconds**, including the failed installed case.

The current effective result is passing coverage of all 1,602 distinct affected
cases, with that targeted rerun explicitly accounted for. The 72 cases are a
subset, not additional coverage. Unchanged successful cases and the source-based
performance measurements were retained; no automatic full-matrix rerun followed
the installation refresh. All 47 wheel module/resource payloads match current
source. Ordinary and lineage installed Hero checks also use a real core-only
environment with PyArrow absent and network blocked.

Specification consistency, traceability, current source/resource checks, changed
Python syntax, all four workflow YAML files and whitespace checks passed.

## Handoff and limits

The current source boundary advances to Step 8 and opens only the changed
validation owner. The other 58 product files, exact product inventory, 16 frozen
specifications and seven packaged resource copies remain protected. Existing
focused CI selects the affected input/lineage neighbors. The actual 100k test
enters only the already established reference performance job. No new Tier D
architecture, source-binding migration, approval registry or evidence-of-evidence
layer is added. Scope pooling and report semantics are unchanged.

Package version remains `0.1.0.dev3`; report schema remains `1.1`. The existing
metadata 100k candidate gate remains required and was not rerun in Step 9.
Step 10 owns complete canonical regression, OS/Python/dependency candidate
checks, build/reproducibility/delivery verification and the dev4 handoff.
No Phase 6 implementation, hosted CI success, main merge, tag or publication is
claimed. Stop after Step 9.
