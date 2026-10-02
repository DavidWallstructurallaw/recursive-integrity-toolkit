# Phase 6B development candidate and handoff

Date: 2026-09-30. Status: **PHASE COMPLETE**.

The Theory Owner requested `Phase 6B Step 8`. The accepted starting point is
Step 7 commit `9af8462bee86c367b6d0f5ae560e97f96cc58409`, tree
`2f7e57e09bfbc0463c717570b271580b0f823257`, on `phase6b-simulation`.
This increment prepares package `0.1.0.dev6`, retaining report schema 1.3.

## Candidate scope

Steps 1-7 implement explicit closed and constant-source reopened categorical
experiments, with immutable declarations, same-environment PCG64 replay,
aggregate admission, separate closed expectation, complete transition events
and per-path comparison. Reports preserve experimental simulation evidence,
declared assumptions, protected identities and independent audit scope.
Configuration and CLI require explicit activation; input-only validation never
samples. The installed synthetic example has independently authored rational
expectations and a user walkthrough.

Step 8 changes only the two package-version literals in product files. All
other product bytes, 41 runtime modules, 18 canonical resources and 16 frozen
specifications retain their accepted identities. Five current report goldens
change only toolkit-version metadata. The existing candidate workflow supplies
the supported compatibility matrix, real optional dependency checks, security,
complete performance and installed artifact verification.

## Candidate identity and verification

| Item | Identity |
| --- | --- |
| Tested candidate | `1e1fcd1466db92c3a39591cf5740331a79f910eb` |
| Tested tree | `d32e26997d1c8f357c4b79a81ae35e56d967d4f9` |
| Candidate workflow | [Run 36784026671](https://github.com/DavidWallstructurallaw/recursive-integrity-toolkit/actions/runs/36784026671) |
| Branch / draft PR | `phase6b-simulation`; [PR #4](https://github.com/DavidWallstructurallaw/recursive-integrity-toolkit/pull/4), based on the accepted unmerged Phase 6A branch |

The following eleven nonperformance jobs passed on the exact candidate. All
actual JUnit cases have zero failures, errors and skips. Downloaded archives
match GitHub's SHA-256 and byte count and pass ZIP CRC checks. Exact checkout
logs bind every job to the candidate; core and Parquet artifacts additionally
retain their source-commit files.

| Job | Job ID | Python | NumPy | pandas | PyArrow | Passed | pytest seconds |
|---|---:|---|---|---|---|---:|---:|
| Core (current) on ubuntu-latest with Python 3.11 | 110120989043 | 3.11.16 | 2.4.6 | 3.0.6 | absent, asserted | 4044 | 262.42 |
| Core (current) on ubuntu-latest with Python 3.12 | 110120989278 | 3.12.14 | 2.5.3 | 3.0.6 | absent, asserted | 4044 | 436.74 |
| Core (current) on windows-latest with Python 3.11 | 110120989249 | 3.11.9 | 2.4.6 | 3.0.6 | absent, asserted | 4044 | 427.66 |
| Core (current) on windows-latest with Python 3.12 | 110120989283 | 3.12.10 | 2.5.3 | 3.0.6 | absent, asserted | 4044 | 502.53 |
| Core (minimum) on ubuntu-latest with Python 3.11 | 110120989573 | 3.11.16 | 2.0.0 | 2.2.2 | absent, asserted | 4044 | 373.05 |
| Core (minimum) on ubuntu-latest with Python 3.12 | 110120989122 | 3.12.14 | 2.0.0 | 2.2.2 | absent, asserted | 4044 | 346.89 |
| Core (minimum) on windows-latest with Python 3.11 | 110120989624 | 3.11.9 | 2.0.0 | 2.2.2 | absent, asserted | 4044 | 326.40 |
| Core (minimum) on windows-latest with Python 3.12 | 110120989293 | 3.12.10 | 2.0.0 | 2.2.2 | absent, asserted | 4044 | 339.24 |
| Real optional Parquet on Ubuntu with Python 3.12 | 110120989085 | 3.12.14 | 2.5.3 | 3.0.6 | 25.0.1 | 4054 | 319.22 |
| hero / hero-contract | 110120989256 | 3.12.14 | 2.5.3 | 3.0.6 | core-only install | 311 | 43.62 |
| security / local-first-boundary | 110120989224 | 3.12.14 | 2.5.3 | 3.0.6 | core-only install | 2027 | 119.58 |

All eight core JUnit identity sets equal the current 4,044-case canonical
collection. The real-Parquet collection contains those cases plus exactly ten
required optional cases, for 4,054. Counts overlap across jobs. Core profiles
verified actual PyArrow absence through both a direct import-availability
assertion and the resolved dependency list. The Parquet profile used PyArrow
25.0.1. Hero/security artifacts contain JUnit and test logs; their exact checkout
and dependency versions were independently checked in full job logs. The
supported profiles do not certify every combination allowed by broad dependency
constraints. Within-environment replay does not promise identical sampled paths
across NumPy versions or operating systems.

The separate focused PR run
[36784012396](https://github.com/DavidWallstructurallaw/recursive-integrity-toolkit/actions/runs/36784012396)
passed its four selections: 1,153 in 9.63s, 483 in 140.92s, 637 in 79.98s and
508 in 25.37s. The candidate run intentionally leaves this alternative focused
job unselected. No failed or skipped testcase is counted as candidate success.

## Local preparation and corrected setup attempt

The affected version/report regression passed **326 tests in 65.51 seconds**
through a newly wheel-installed dev6 interpreter. The gate/workflow selection
passed **67 tests in 6.01 seconds**. Current source checks confirm 81 fully
frozen product files and two exact version-token owners, 41 runtime modules,
18 canonical resource copies and 16 frozen specifications. The five golden
files were independently checked to differ only in dev5/dev6 version tokens.

An existing 100/400-record metadata performance assertion passed in 2.48 seconds
before the full-scale run. The sparse-lineage API worker's Linux RSS reading
was aligned with Step 7's `VmHWM` method to remove the inherited parent peak.
The same worker passed its independent 1,000-record assertions in a bounded
preflight, at 0.510382 seconds outer wall and 39,432,192 bytes peak RSS. These
preflights do not stand in for the hosted actual 100k workloads. Scientific
oracles, workload sizes, timeout guards and product algorithms were unchanged.

Local delivery used Python 3.12.14, build 1.6.1 and setuptools 84.0.0 from a
scratch source snapshot. It built a wheel and sdist, safely extracted the sdist,
rebuilt a wheel, and installed each wheel with `pip --no-index --no-deps` in a
separate new environment. Both environments had no toolkit before installation
and shared existing NumPy/pandas dependencies. All 41 module and 18 resource
files matched the source. Every uncompressed original/rebuilt wheel member was
identical. These local archive identities retain their own build scope:

| Local artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| Original wheel | 392956 | `aa377e1d43d6d5ca5b418f72e2eba5ffd851266d2b8f5907e105193a0c8593f8` |
| Source distribution | 362072 | `44fc56e116578c30566c99ba0b4115a3c8b18e0d20858f3ebcedda6d750c4537` |
| Wheel rebuilt from sdist | 392956 | `62850d29b3d280a13705c884a998bb9570c6e431cd756aff967b76388b7976fa` |

Installed simulation tests passed **7 cases in 2.95s** on the original wheel
and **7 in 3.07s** on the rebuilt wheel. Both console aliases and isolated module
invocation reported dev6. The combined installed example smoke passed all
ordinary, lineage, longitudinal and simulation examples, standard/redacted
views, replay, resource identities, no overwrite and blocked network.

The first combined local smoke found a missing `jsonschema` test dependency
after successful Hero execution. That failed setup attempt is retained. A fresh
workspace rerun supplied the existing test dependencies after installed
site-packages and asserted the package origin, then passed. Import blockers in
these shared local environments establish isolation; actual optional-dependency
absence is established separately by the eight hosted core profiles.

## Performance acceptance

Performance job `110120988683` passed all 21 required cases. The separate 100k
series invocation passed in 985.18 seconds of pytest console time; the retained
20-case invocation passed in 1058.34 seconds. Its single deselection is the
independently executed 100k case. Neither JUnit contains failures, errors or
skips. Every required performance identity was collected exactly once.

Artifact `11129988043` is 97,210,017 bytes with SHA-256
`7a0778519ba7d98df149300d8d989cd204fb5ebbf13cbedf994beabba81dface`.
GitHub digest, size and all 260 ZIP-member CRCs were checked. The complete ZIP
is retained; 148 ordinary members were extracted and redundant `*current`
aliases excluded from observation counts. There are 24 complete CLI attempts,
one ancestry API attempt and seven separately traced calculation observations.
All measured processes exited zero without timeout. No retry or fastest-attempt
selection occurred. All 131 recorded input references match their byte counts
and SHA-256; all 48 report files match their recorded lengths.

CPU: AMD EPYC 9V74 80-Core Processor, 4 visible logical CPUs. Platform: Linux-6.17.0-1022-azure-x86_64-with-glibc2.39. Python 3.12.14; NumPy 2.5.3, pandas 3.0.6, pytest 9.1.1, PyArrow absent. Host RAM 16,766,410,752 bytes; configured swap 3,221,221,376 bytes.

Outer wall includes fresh interpreter startup, imports, complete audit/publication and measurement bookkeeping. CLI time starts before imports and ends after both JSON and Markdown publication. Input construction and parent report assertions are excluded from these intervals. Ancestry API time includes validation/graph/root assertions and summary work, without full audit output. Optional scenario timing wraps the actual experiment call inside the CLI and excludes report assembly/publication.

Linux CLI peak RSS is `/proc/self/status` VmHWM for the executed process. The API uses the same VmHWM measure in KiB converted to bytes. Before/after values are high-water marks with no subtraction. The prior Phase 6A reference used `ru_maxrss`, which retained the fork-parent floor in several smaller workloads. Lower new peaks in those cases cannot establish a runtime memory optimization.

## Every publication and API attempt

| Case / attempt | Mode | Outer s | CLI / worker s | Scenario s | RSS before B | RSS peak B | JSON / API B | Markdown B |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| test_longitudinal_100k_complete_reports, 1 | untraced | 979.555272 | 979.364604 | n/a | 14,024,704 | 7,352,225,792 | 427,983,691 | 266,479,098 |
| test_phase4_step10_hero_complete_report_runtime, 1 | untraced | 0.731586 | 0.668620 | n/a | 14,135,296 | 42,500,096 | 209,421 | 185,634 |
| test_phase4_step10_hero_complete_report_runtime, 2 | untraced | 0.730256 | 0.668039 | n/a | 14,041,088 | 42,450,944 | 209,421 | 185,634 |
| test_phase4_step10_hero_complete_report_runtime, 3 | untraced | 0.744570 | 0.682176 | n/a | 14,143,488 | 42,508,288 | 209,421 | 185,634 |
| test_phase4_step10_hero_complete_report_runtime, 4 | traced | 3.773388 | 3.690848 | n/a | 14,036,992 | 58,384,384 | 209,421 | 185,634 |
| test_hero_lineage_complete_report_runtime, 1 | untraced | 0.751019 | 0.688506 | n/a | 14,028,800 | 42,979,328 | 242,119 | 218,651 |
| test_hero_lineage_complete_report_runtime, 2 | untraced | 0.766769 | 0.704317 | n/a | 14,069,760 | 43,061,248 | 242,119 | 218,651 |
| test_hero_lineage_complete_report_runtime, 3 | untraced | 0.748315 | 0.686140 | n/a | 14,061,568 | 43,094,016 | 242,119 | 218,651 |
| test_longitudinal_bounded_complete_reports[1000], 1 | untraced | 8.974056 | 8.906827 | n/a | 14,147,584 | 110,108,672 | 4,417,806 | 3,020,671 |
| test_longitudinal_bounded_complete_reports[10000], 1 | untraced | 91.764119 | 91.681260 | n/a | 14,045,184 | 773,312,512 | 42,908,004 | 26,943,390 |
| test_longitudinal_many_versions_complete_reports, 1 | untraced | 5.220275 | 5.155471 | n/a | 14,123,008 | 76,394,496 | 3,377,588 | 4,086,967 |
| test_longitudinal_hero_complete_reports[distribution], 1 | untraced | 0.852382 | 0.790221 | n/a | 14,110,720 | 43,458,560 | 283,860 | 318,676 |
| test_longitudinal_hero_complete_reports[distribution], 2 | untraced | 0.855210 | 0.793041 | n/a | 14,221,312 | 43,524,096 | 283,860 | 318,676 |
| test_longitudinal_hero_complete_reports[distribution], 3 | untraced | 0.853437 | 0.791401 | n/a | 14,135,296 | 43,466,752 | 283,860 | 318,676 |
| test_longitudinal_hero_complete_reports[lineage], 1 | untraced | 0.907717 | 0.844275 | n/a | 14,204,928 | 43,503,616 | 312,580 | 342,632 |
| test_longitudinal_hero_complete_reports[lineage], 2 | untraced | 0.908753 | 0.845791 | n/a | 14,106,624 | 43,397,120 | 312,579 | 342,631 |
| test_longitudinal_hero_complete_reports[lineage], 3 | untraced | 0.901176 | 0.839619 | n/a | 14,213,120 | 43,503,616 | 312,580 | 342,632 |
| test_phase4_step10_metadata_100k_complete_report_runtime, 1 | untraced | 767.005265 | 766.886903 | n/a | 14,127,104 | 7,677,620,224 | 442,741,954 | 165,121,778 |
| test_simulation_complete_reports[small-3], 1 | untraced | 0.735097 | 0.666795 | 0.062847 | 14,200,832 | 55,021,568 | 163,610 | 139,563 |
| test_simulation_complete_reports[small-3], 2 | untraced | 0.736369 | 0.666746 | 0.061645 | 14,204,928 | 55,103,488 | 163,609 | 139,562 |
| test_simulation_complete_reports[small-3], 3 | untraced | 0.730632 | 0.662543 | 0.062078 | 14,098,432 | 54,943,744 | 163,610 | 139,563 |
| test_simulation_complete_reports[representative-1], 1 | untraced | 7.454670 | 7.380979 | 0.140189 | 14,188,544 | 168,853,504 | 8,229,320 | 194,597 |
| test_sparse_lineage_bounded_complete_reports, 1 | untraced | 8.114025 | 8.045780 | n/a | 14,118,912 | 145,293,312 | 6,203,345 | 1,534,140 |
| test_sparse_lineage_100k_api, 1 | untraced API | 66.822817 | 66.288744 | n/a | not recorded | 1,851,809,792 | 940 | not produced |
| test_high_fan_in_lineage_complete_reports, 1 | untraced | 1.679744 | 1.616115 | n/a | 14,036,992 | 50,552,832 | 612,015 | 286,530 |

## Scientific and resource scopes

The 100k series retains 100 context anchors and three selected populations of 33,300 rows, with three unique comparisons. The generator, exact rational per-version/delta oracles and default limits are unchanged. Recorded shared graph work is 100,000 nodes, 99,900 edges, 100,000 root memberships and 99,900 union visits. Complete JSON and Markdown total 694,462,789 bytes. Its 979.555272-second outer interval remains within the unchanged 1,800-second guard.

Ordinary 100k metadata retains 100 equally occupied states, source shares 0.18 each, 10% missing provenance and direct closure interval [0.18, 0.64]. Its complete-report interval remains within 1,800 seconds. The 100k reverse-chain API retains depth 99,999, one root, G/C/U=100,000/0/0, HHI and effective roots 1; validation took 25.962679 seconds and ancestry 40.273318 seconds. Its 66.822817-second outer interval remains within the unchanged 600-second guard.

Both scenario profiles contain exactly two audit records independent of zero-record scenario scopes. The small profile admits 84 state cells (2 models, K=2, horizon=6, replicates=3, n=2); the representative admits 33,280 cells (2 models, K=32, horizon=64, replicates=8, n=64). Seed is 17 and reopening weight is 1/4. Every path/count/source/event oracle passes, with exact full JSON and truthful 100-row Markdown omission disclosures. The representative scenario completes publication in 7.454670 seconds; 0.140189 seconds measures only its actual experiment call. These are bounded observations, with no new latency SLA or million-cell extrapolation.

### Reference comparison and remaining limits

The retained Phase 6A reference is candidate
`157109717079c9db9f02ac65ec1493709f37d8a4`, run `36327281529`.
Workloads, attempt order, tracing modes and input hashes match. Python,
dependency and OS/kernel versions match; the CPU changed from EPYC 7763 to
EPYC 9V74. Physical host allocation and load were uncontrolled, and the RSS
measurement method changed. These observations do not isolate a product-code
cause or establish a memory optimization where the old parent floor dominated.

The 100k series outer time changed from 965.342692 to 979.555272 seconds
(+1.4723%); ordinary 100k metadata changed from 770.636094 to 767.005265
seconds (-0.4711%); the ancestry API changed from 66.231542 to 66.822817
seconds (+0.8927%). No retained observation crossed the review thresholds of
+20% runtime or +50% recorded memory. Maximum observed runtime increase was
4.3418%; maximum raw process-RSS increase was 7.0602%. The separately traced
Hero Python peak was 19,454,282 bytes versus 16,365,785 (+18.8717%), also
below the memory review threshold. All twelve untraced Hero attempts were below
the existing five-second reference target.

The full 100k report workloads still require roughly 7.35-7.68 billion bytes of
peak process RSS and hundreds of megabytes of output. Their operational guards
are not latency or memory SLAs. The ancestry API omits full report construction.
The two simulation profiles use state/step/replicate cells, with only two loaded
fictional audit records; they establish no million-cell report-performance claim.
The 20-version/220-record workload is distinct from the tiny canonical Hero.
The candidate measurements do not certify every laptop or supported matrix cell.

### Retained calculation observations

| Calculation | Traced wall s | Traced Python peak B |
|---|---:|---:|
| hero_input_plus_calculations | 0.117161 | 1,695,001 |
| metadata_100k_setup | 25.590688 | 265,131,522 |
| metadata_100k_field_representation | 6.718919 | 66,295,688 |
| metadata_100k_support_diversity | 4.715740 | 39,070,984 |
| metadata_100k_provenance_join | 14.255223 | 112,088,900 |
| metadata_100k_composition | 13.661607 | 70,367,904 |
| metadata_100k_exact_duplicates | 7.054850 | 88,422,856 |

## Output growth and diagnostic completeness

| Input records | Warning entries | JSON B | Markdown B | stderr B |
|---:|---:|---:|---:|---:|
| 100 | 66 | 548,281 | 273,317 | 41,692 |
| 400 | 264 | 1,875,289 | 767,061 | 166,930 |

Fourfold input growth yields json_bytes: 3.420306x, markdown_bytes: 2.806488x, stderr_bytes: 4.003886x. All remain within the existing 6x structural bound. This in-process check is not an independent timing/RSS observation.

| Complete workload | stderr B | Diagnostic entries by code |
|---|---:|---|
| longitudinal_100000 | 97,991,102 | {"W_GENERATION_MISMATCH": 149850} |
| longitudinal_1000 | 879,300 | {"W_GENERATION_MISMATCH": 1350} |
| longitudinal_10000 | 9,691,201 | {"W_GENERATION_MISMATCH": 14850} |
| metadata_100k_complete_reports | 42,049,360 | {"W_GROUNDING_UNKNOWN": 36000, "W_PROVENANCE_MISSING_ROW": 30000} |

## Hosted delivery

Delivery job `110131955104` completed successfully on the same candidate.
Its 3,417,852-byte artifact `11130302309` matches GitHub SHA-256
`f837b505bc5b04c705e0aee072f805dfcf2bcf4f29100d6c654486fa9beafa0e`
and passes ZIP CRC checks. The reused 4,044-case core and 4,054-case Parquet
JUnit files match the previously verified matrix artifacts byte-for-byte.

The build environment used Python 3.12.14, build 1.6.1, setuptools 84.0.0 and
twine 7.0.0. `SOURCE_DATE_EPOCH=1790806207` matches the candidate's Git timestamp.
Strict distribution checks, exact module/resource inventories, notices and
installed behavior passed. The workflow's default `python -m build` creates an
sdist and builds the wheel from it. Repeating that build produced identical
wheel bytes; every sdist regular-file payload matched, while compressed archive
bytes differed.

| Candidate artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| Wheel | 392954 | `310212fa2e46185cc40baa7013fde026583479064ebeb4ee6e97725692ef8f38` |
| Source distribution | 361349 | `d04af0009d64d5d410a60557e5ad0e9f6c41ab80700cc560da365cf8a790aebf` |
| Tracked-source ZIP | 1761543 | `e5e9b311c91ba04ecd0980182ad22f6c33223efd352d446d503173ab4f2fbc9d` |

The repeated sdist SHA-256 was
`7e88f8f17adae376359d27462ebafb5f6410ba6186d4553f994399f946e93778`.
No claim of identical sdist archive bytes is made. The source ZIP contains
exactly 354 tracked files under one root, each byte-identical to `git archive`
of the tested candidate. Git internals, caches, environments and uploaded theory
PDFs are absent from that source archive. Wheels and sdists retain their own
package scope, with all 41 runtime modules and 18 canonical resources verified.

The actual wheel was installed into clean temporary targets outside the
checkout with `pip --no-index --no-deps`. Existing installed checks passed input,
mathematics, privacy, protected JSON/Markdown, output safety, ordinary CLI and
packaged Hero/lineage/longitudinal/simulation behavior. The safely extracted
sdist was separately exercised directly from its source tree. This hosted sdist
smoke is distinct from the second pip-installed rebuilt wheel in the local
preflight. Both paths retain their exact scope. Installed example checks verify
independent arithmetic, source/sample separation, event completeness, replay,
standard/redacted views, exact resources, no overwrite and blocked network.

## Final handoff

All required candidate jobs passed in this single candidate run. There was no
hosted retry or failed candidate attempt. The local missing-test-dependency
attempt remains disclosed above. Source/golden review, matrix evidence,
performance extraction and delivery were cross-checked by separate assistant
review roles. No blocking theory or implementation conflict remains.

The administrative handoff following the tested candidate updates only completion
and status documentation. Runtime, schemas, resources, tests and verification
scripts retain the candidate's bytes. All wheel, sdist and source-archive hashes
above identify the tested `1e1fcd1` source, not a new build from the documentation
successor. The successor's README description can differ from the archived
package long description; installation evidence remains bound to the named
candidate. Existing nonauthoritative-documentation reuse policy applies.

UD-017 authorizes the experimental scenarios. UD-031 keeps empirical intervention
ingestion deferred. F-016 external-reference loss, causal/model-performance
claims, parameter sweeps, time-varying external schedules and HTML remain outside
the completed scope. Main merge, release tagging and registry publication are
separate actions. Phase 6B ends with this dev6 development handoff.
