# Phase 3 Validation Report

Status: technical implementation acceptance verified at `9dc321c6997a231209653a0f86d0476824e96e3a`. All results below are observed. The acceptance-record revision must independently pass the same four workflow roles on its exact HEAD before final handoff; the external receipt binds that final HEAD and regenerated artifacts.

## Source and commands

Step 11 base: `150a2a105e01883672ef0c2300b41b0de3be352e`; accepted tree: `a1086ca95075aff3ea8a83afae548806b2079dc9`. Version: `0.1.0.dev2`. The initial Step 11 change set contains 25 modified files and three new reports. The full tree contains 222 tracked files. Original Phase 2 commit/tree/test tree and all sixteen approval hashes remain frozen.

Commands below were executed from the repository root. Local Python paths are `../.venv-step11-current/bin/python` and `../.venv-step11-minimum/bin/python`. Local paths, exact argv, timestamps and exit codes are retained in `evidence/local/validation-commands.json` and `evidence/candidate-build/commands.json`; raw GitHub logs retain actual workflow paths and command lines.

| Executed command family | Mode / result |
|---|---|
| `python -m pytest -p no:cacheprovider -q --junitxml=...` | Complete core, minimum and real-Parquet suites; successful repaired runs exit 0 |
| `python scripts/release_check.py --junit ... --minimum-tests 2472` | Core JUnit, zero failures/errors/skips and unique identities; exit 0 |
| Same with `--require-parquet --minimum-tests 2475` | All three real-Parquet cases present and passed; exit 0 |
| `python scripts/release_check.py --baseline-evidence ...` | Original/current identities in both optional modes; exit 0 |
| `python scripts/check_spec_consistency.py` | Approved document/schema/Hero/workflow structure; exit 0 |
| `python scripts/check_traceability.py` | Forty modules, sixteen placeholders, exact definitions/imports/owners; exit 0 |
| `python scripts/release_check.py --phase 3 --step 11 --diff` | Frozen anchors, permissions, snapshots, test migrations and clean source; exit 0 |
| `python -m build --outdir ...` | Isolated wheel and sdist; exit 0 |
| `python -m twine check --strict ...` | Both formats passed; exit 0 |
| `python scripts/release_check.py --phase 3 --step 11 --dist ...` | Byte equality and fresh installed input/math checks; exit 0 |
| `python scripts/release_check.py --phase 3 --step 11 --delivery ...` | Full source ZIP and retained evidence/checksums; exit 0 |
| `python -m pip check` | Current, minimum and PyArrow local profiles plus CI profiles; exit 0 |
| README Python blocks executed in order | Hero input, explicit distribution, analytic and seeded calls; exit 0 |

Core runs use `RIT_TEST_PARQUET=0` with actual PyArrow absence. Real-input runs use `RIT_TEST_PARQUET=1` with installed PyArrow. Bytecode/cache output is disabled by the recorded commands. No active regression is hidden by skip, xfail, subset selection or continue-on-error.

## Platform and dependency results

| Complete core environment | Actual Python | NumPy | pandas | Result | Seconds |
|---|---|---|---|---|---|
| Core (current) on ubuntu-latest with Python 3.11 | 3.11.16 | 2.4.6 | 3.0.6 | 2489 passed | 127.98 |
| Core (current) on ubuntu-latest with Python 3.12 | 3.12.14 | 2.5.3 | 3.0.6 | 2489 passed | 141.94 |
| Core (current) on windows-latest with Python 3.11 | 3.11.9 | 2.4.6 | 3.0.6 | 2489 passed | 196.33 |
| Core (current) on windows-latest with Python 3.12 | 3.12.10 | 2.5.3 | 3.0.6 | 2489 passed | 118.86 |
| Core (minimum) on ubuntu-latest with Python 3.11 | 3.11.16 | 2.0.0 | 2.2.2 | 2489 passed | 77.34 |
| Core (minimum) on ubuntu-latest with Python 3.12 | 3.12.14 | 2.0.0 | 2.2.2 | 2489 passed | 141.55 |
| Core (minimum) on windows-latest with Python 3.11 | 3.11.9 | 2.0.0 | 2.2.2 | 2489 passed | 196.10 |
| Core (minimum) on windows-latest with Python 3.12 | 3.12.10 | 2.0.0 | 2.2.2 | 2489 passed | 170.62 |

The separate Ubuntu/Python 3.12 real-input job used PyArrow **25.0.1**, passed **2492 tests** in **144.09 seconds**, and retained all three original Parquet identities. The build workflow independently repeated complete core (2489, 144.05 seconds) and Parquet (2492, 143.09 seconds) suites. Security passed 1678 in 51.67 seconds. Hero/math passed 83 in 2.01 seconds. Those are subsets/repeats of the same active regression surface.

Local Linux/Python **3.12.14** runs passed current core 2489 in **99.12 seconds**, minimum 2489 in **97.86 seconds**, and real Parquet 2492 in **98.21 seconds**. Local current NumPy/pandas were 2.5.3/3.0.6; minimum was 2.0.0/2.2.2. pytest 9.1.1, build 1.6.1 and Twine 7.0.0 were used. The build backend remains setuptools, isolated under the existing `setuptools>=82` declaration; it is not installed in the outer local venv. Full environment lists are retained rather than inferring a backend version from that outer environment.

The literal NumPy 2.0.0 / pandas 2.2.0 resolver failed with exit 1 and `ResolutionImpossible`, because pandas 2.2.0 requires NumPy below 2. NumPy 2.0.0 / pandas 2.2.2 is the lowest jointly compatible tested direct-dependency pair, consistent with the [pandas 2.2.2 release notes](https://pandas.pydata.org/docs/whatsnew/v2.2.2.html). Original declarations remain unchanged. No claim is made that the impossible pair, every intermediate version, or optional PyArrow's lowest version was tested.

## Mathematical and inherited evidence

All twenty frozen source-indexed mathematical cases executed without changing their JSON or source-note bytes. Inherited exact/rational, boundary, weighting, unavailable-value, permutation, count-conservation, mapping, unknown-provenance and no-inference checks passed. Closed sampling retains PCG64 and environment/schedule metadata. The Monte Carlo test uses p=(1/2,1/2), n=4, three generations, 8000 replicates, seed 812 and absolute mean-diversity tolerance 0.025 against independent rational expectations. It passed in every complete environment; no cross-version sampled-path identity is claimed.

| Frozen checkpoint | Core identities retained | Real-Parquet identities retained |
|---|---|---|
| Phase 2 | 1159 | 1162 |
| Step 1 | 1270 | 1273 |
| Step 2 | 1429 | 1432 |
| Step 3 | 1575 | 1578 |
| Step 4 | 1714 | 1717 |
| Step 5 | 1888 | 1891 |
| Step 6 | 1987 | 1990 |
| Step 7 | 2117 | 2120 |
| Step 8 | 2268 | 2271 |
| Step 9 | 2404 | 2407 |
| Step 10 | 2472 | 2475 |
| Current | 2489 | 2492 |

The retained JSON contains every node ID, baseline file blob/SHA identity and digest, with zero missing IDs. Counts alone are not the preservation proof. Historical Step 10 scope/control/source and final-report-absence tests use its immutable archived source. The completion-forgery test negates the actual current flag. Byte guards reject any wider changes; current Step 11 tests enforce current report presence and protected boundaries.

## Performance observations

The following are actual repaired local-current measurements with tracing enabled. Each operation has its own tracemalloc interval. Setup measures synthetic normalization separately. Allocations existing before each operation and native allocations outside tracemalloc are excluded; peak values are not process RSS. Host contention and instrumentation affect elapsed time.

| Operation | Seconds | Peak traced MiB |
|---|---|---|
| hero_input_plus_calculations | 0.033502 | 0.157 |
| metadata_100k_composition | 10.925117 | 67.108 |
| metadata_100k_exact_duplicates | 5.342645 | 84.327 |
| metadata_100k_field_representation | 5.227824 | 63.224 |
| metadata_100k_provenance_join | 10.778443 | 106.896 |
| metadata_100k_setup | 20.280936 | 252.849 |
| metadata_100k_support_diversity | 3.661939 | 37.261 |

The synthetic dataset has 100000 records, 100 equiprobable topic states and 1000 exact forms. Independent oracles check support 100, diversity 0.99, 50000/50000 source counts and 99000 duplicate records in 1000 groups. All seven required observations were retained and validated in each local complete profile. These measurements do not certify whole-product report performance, sparse-lineage performance or an SLA.

## Build, installation and artifact evidence

Both local and GitHub builds passed strict Twine checks. Wheel and sdist contain the same forty module files and exact bytes as source, with LICENSE/NOTICE. Fresh environments outside the checkout install the wheel with `--no-index --no-deps`. The first smoke blocks network and numerical/optional imports while importing all forty modules and validating the Hero input. A separate installed numerical smoke exercises prior metrics, direct bounds, tail/F-014, F-015/seeded paths and explicit pair calculations with numerical dependencies available and no I/O/network during calls.

The one-root ZIP contains all 222 tracked files and no Git internals, environment, cache, generated bytecode, private input or full theory PDFs. Every archived file is compared with the tested source. `phase3_repository_files.sha256` covers tracked bytes; `phase3_artifacts.sha256` covers retained artifacts. Locally, manifests are finalized after command logs close. Finalization requires rebuilding/rearchiving the final commit, so candidate binary hashes are not presented as final hashes.

Accepted hosted delivery: artifact **10572032089**, workflow **35404377857**, API digest `sha256:a7f753087f632546bc1fc7052753e35cf3ed2db76cf96e9246758f82cd29fe66`, actual expiry **2026-12-17T23:06:38Z**. Ordinary CI/security/math retention is 30 days; delivery retention is 90 days. A requested hosted ZIP transfer returned HTTP 403 (`error code: 1010`); no access-control bypass was attempted. Hosted digest/identity and successful raw build logs are recorded as server evidence. Locally regenerated artifacts are independently inspected and hashed; equality to unavailable hosted binary bytes is not claimed.

## Failures, repairs and review

1. Literal minimum resolution failed as described above. No dependency declaration was changed to force it.
2. Two initial local installs collided while building the same checkout concurrently. Generated build/egg-info output was removed and sequential retries both exited 0. Runtime was unchanged.
3. The first complete core run produced **2488 passed, one failed** in 97.45 seconds, exit 1. The inherited final-report-absence test still inspected the current checkout. After explicit Theory Owner approval, only its fixture/root binding moved to frozen Step 10. Its original name and three absence assertions remain. The failed JUnit/log and successful reruns are retained separately.
4. Hosted artifact transfer returned 403; raw job-log/API evidence and locally verified artifacts preserve the verifiable boundary stated above.

The assistant conducted implementation, mathematical traceability/transcription and security-boundary reviews under the approved consolidated-role arrangement. The Theory Owner supplied scope/exception approval. Automated checks are execution evidence; no independent human certification, external vulnerability audit or production-readiness claim is made. Final source/workflow acceptance and final artifact hashes are bound in the external receipt after the mandatory rerun.
