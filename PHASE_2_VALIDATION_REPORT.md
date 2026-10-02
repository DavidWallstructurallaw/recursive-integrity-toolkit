# PHASE_2_VALIDATION_REPORT

Status: **PASS for the Phase 2 technical acceptance gate.**

Accepted implementation/audit commit: `a9e4b5cef2f27302d3bceca070c46bd4b80c6ca6`.
Execution evidence date: 2026-09-17 UTC.
Evidence below is from actual GitHub-hosted execution, not planned commands.

## Commands and observed outcomes

The command paths below use `D="$RUNNER_TEMP/rit-delivery"` as an abbreviation for the literal delivery directory in the workflow. All successful commands completed with exit code 0.

| Actual command or executed gate | Result |
|---|---|
| `python -m pip install ".[release,test]"` | Package and approved tools installed |
| `python -c "import importlib.util; assert importlib.util.find_spec('pyarrow') is None"` | Actual absence verified before the core run |
| `RIT_TEST_PARQUET=0 python -m pytest -p no:cacheprovider -q --junitxml="$D/core.xml"` | 1159 passed in 9.45 seconds |
| `python scripts/release_check.py --junit "$D/core.xml" --minimum-tests 1131` | 1159 passed cases; zero failures, errors or skips |
| `python -m pip install ".[parquet]"` | Real PyArrow 25.0.1 installed |
| `RIT_TEST_PARQUET=1 python -m pytest -p no:cacheprovider -q --junitxml="$D/parquet.xml"` | 1162 passed in 9.77 seconds |
| `python scripts/release_check.py --junit "$D/parquet.xml" --require-parquet --minimum-tests 1134` | All three real-Parquet cases present and passed |
| Security subset with JUnit | 324 passed in 7.81 seconds |
| Hero structure and end-to-end subset with JUnit | 33 passed in 0.67 seconds |
| `python scripts/check_spec_consistency.py` | Required files, five schemas, six Hero files and four workflows passed |
| `python scripts/check_traceability.py` | 40 modules, 26 protected placeholders, exact owner/function/import boundaries passed |
| `python scripts/release_check.py --diff` | All 16 approved hashes and Step 10 scope passed |
| `python -m build --outdir "$D/dist"` | Wheel and sdist built using isolated setuptools 84.0.0 |
| `python -m twine check --strict "$D/dist/"*` | Both distributions passed |
| `python scripts/release_check.py --dist "$D/dist"` | Distribution bytes and fresh installed-package smoke passed |
| `rit version` | `recursive-integrity-toolkit 0.1.0.dev1` |
| `python scripts/release_check.py --delivery "$D"` | JUnit, distributions, archive and checksums verified |

The workflow pipes command output through `tee` under Bash with error and pipe-failure propagation. It does not turn failed commands into successful jobs. A failure-evidence upload step is conditional; its absence on a successful run is not a skipped test.

Security files executed: `test_no_network.py`, `test_optional_dependency.py`, `test_no_algorithms.py`, `test_prohibited_structure.py`, `test_license_notices.py`, `test_PR003_schema_mapping.py`, `test_PR017_content_refs.py`, and `test_partial_lineage_report.py`. The two Hero files are `test_hero_structure.py` and `test_hero_end_to_end.py`.

## Counting and platform evidence

Distinct core cases: **1159**. Extra-enabled distinct cases: **1162**, comprising the same core plus three optional-presence tests. The 324 security and 33 Hero cases are subsets. No counts from repeated runs, operating systems or subsets are added together.

The Step 9 suite had 1131 core cases. Step 10 added 20 audit/evidence cases and eight exact-restoration cases, retaining previous tests. No failed test was removed, skipped, xfailed or masked.

CI run `35192182710` passed all five jobs: the full core on Ubuntu/Python 3.11, Ubuntu/Python 3.12, Windows/Python 3.11 and Windows/Python 3.12, plus the complete real-Parquet suite on Ubuntu/Python 3.12. Security run `35192182715`, Hero run `35192182678` and Build and Delivery run `35192182750` all passed. The timings above are from delivery job `105107002841` on Python 3.12.14 and are observations, not performance targets.

## Validated families

The full suite exercises local formats and limits; duplicate keys and headers; safe mapping verbs and unsafe syntax rejection; identity and missingness preservation; canonical types and enums; provenance attachment and separate coverage; explicit chronology; immediate parent parsing/resolution; generation consistency and unavailable cases; local-reference containment and encoding; observability and independent capabilities; and complete bundle orchestration.

Negative tests preserve later-phase boundaries, network blocking, optional-dependency isolation and rejected executable behavior. Tests use synthetic local fixtures. No real private dataset is analyzed and no analytical golden is generated.

The real-Parquet tests are `test_PR002_parquet_real_roundtrip`, `test_PR002_parquet_real_row_limit` and `test_PR002_parquet_real_invalid_file`. They use real PyArrow, with no mocked substitute. Their longstanding environment-dependent validation gap is closed by the successful full extra-enabled run.

## Installed distribution verification

The build workflow compares all forty Python source files in both package distributions to the tested checkout. LICENSE and NOTICE are present in the wheel. Strict package-metadata checks pass.

A new virtual environment installs the built wheel with `--no-index --no-deps`. A Python `-I` process runs outside the checkout, verifies that the imported package is not the source-tree copy, checks its metadata version, blocks NumPy/pandas/PyArrow imports and network connections, imports all forty modules, and validates Hero input eligibility through the installed `validate_bundle` interface. Hero remains Level 4 with model longitudinal unavailable and no validation errors. All six Hero file hashes remain unchanged. Both CLI entrypoints and module startup pass.

This intentionally exercises the current input layer without analytical dependencies; it does not remove those dependencies from the approved package metadata. Dependency acquisition during installation/build is separate from offline runtime validation.

## Failure history and exact repair

Initial candidate `068cdf0baf87f279f6a4e36271f197df9c1f3696` produced 1150 passed/1 failed in the core and 1153 passed/1 failed with PyArrow. The sole failure was `test_phase2_approved_phase0_hashes_match_current_sources`, for the draft-state `VALIDATION_PLAN.md`. Initial CI run `35189874671` and delivery run `35189874618` retain the failed evidence.

The original expected SHA-256 remained `16f5fe539da2b3cff1c3e0a2854208bd7fbc1e4c5b332684265b06a03a90cf2f`. The previously stored draft was `564abf56c91141d0cd8ca09024f1cf6dda63bf4ba12acf6563bb7cbc158a84f7`. After explicit Theory Owner authorization, only the two approval-state labels were restored to the original approved bytes. The manifest, tests and substantive requirements stayed intact. The precise restoration gate rejects other files, additions/deletions, altered before/after bytes, unchanged drafts and invalid types.

The subsequent full accepted runs report zero failures and zero skipped tests. Local clone/DNS failures are environment limitations; they are not represented as passing local execution.

## Evidence retention and limits

Delivery retains `core.xml`, `parquet.xml`, `security.xml`, `hero.xml`, raw test/build/install/audit logs, package metadata checks, `phase2_execution_metadata.json`, `phase2_repository_files.sha256` and `phase2_artifacts.sha256`. The source archive includes 197 tracked files under one `recursive-integrity-toolkit/` root, with no Git metadata, virtual environment or build cache. Every archived file is compared byte-for-byte to the tested checkout.

The documentation-only finalization reruns these unchanged gates and produces a new artifact with its own commit identity. Earlier artifacts with blocked milestone text are historical evidence, not the final handoff. Workflow configuration checks and actual GitHub execution succeeded; no separate external security certification, comprehensive vulnerability database scan, static type-checking completion or production performance result is claimed.

No analytical computation was performed. Phase 3 is not authorized.
