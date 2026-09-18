# Phase 3 Validation Report

Status: Step 11 candidate; final execution acceptance pending. This file will be finalized from actual results after the required workflows pass.

Base commit: `150a2a105e01883672ef0c2300b41b0de3be352e`. The accepted base contains 2472 core identities and 2475 real-Parquet identities. These historical counts are preservation requirements, not predicted final counts.

## Executed preparation and repairs

The literal minimum resolver command for `numpy==2.0.0` and `pandas==2.2.0` exited 1 with `ResolutionImpossible`: pandas requires NumPy below 2. This is retained as failed compatibility evidence. The minimum compatible profile uses NumPy 2.0.0 and pandas 2.2.2; dependency declarations are unchanged.

Two initial local environment installations failed while concurrently building the same checkout, with build-directory file/directory collisions. These were maintainer execution failures. Generated build/egg-info directories were removed and installation was repeated sequentially; both retry commands exited 0. No runtime repair or dependency declaration change was made. Original and retry logs are retained.

Exact runtime/dependency/Hero/schema/oracle checks and both approved test-migration byte checks passed locally. Specification consistency, traceability and active-stage audit commands exited 0. Both environment `pip check` commands exited 0. All README Python examples executed in order and exited 0.

The first complete current-core run executed 2489 tests: 2488 passed and 1 failed, exit 1, 97.45 seconds. The failure is the inherited `tests/unit/test_phase3_contracts.py::test_phase3_final_completion_records_not_created`, which still asserts that all three final report files are absent from the active checkout. Step 11 explicitly requires those files. The already approved unit-file exception only permits the completion-forgery expression; this additional stage assertion was outside the initial approval and triggered a separate authorization request. Its failure is retained without skip, xfail or altered expectations.

Approved narrow repair, after the Theory Owner explicitly replied `批准`: bind that one historical test to the immutable Step 10 snapshot while retaining its node name and three absence assertions. The already updated current-stage repository-structure test requires all three Step 11 reports. Extend the exact byte-migration guard to allow only that binding plus the previously approved completion-forgery edit. No mathematical/security assertion changes. No final acceptance or remote result is claimed.

Actual local current versions: Python 3.12.14, NumPy 2.5.3, pandas 3.0.6, pytest 9.1.1; PyArrow absent. The repaired complete current-core run passed all 2489 cases with zero failures, errors or skips in 99.12 seconds, exit 0. The minimum environment uses NumPy 2.0.0 and pandas 2.2.2; its independent regression is in progress. Real-Parquet, remote matrices, build/install and final archive remain pending execution following the additional approval.

## Required evidence

The workflow matrix, commands, artifact definitions and finalization rules are in `docs/release_process.md`. Required mathematical evidence includes twenty frozen cases, independent rational/enumeration cases, the retained 8000-replicate Monte Carlo check, deterministic seeded paths, boundaries and metamorphic properties. JUnit must report zero failed, errored and skipped cases.

Coverage must include all original Phase 2 and Steps 1-10 node IDs; real PyArrow must collect/pass all three original tests. Safe import/input checks and numerical invocation checks remain separate. Build evidence must include wheel/sdist module-byte equality, strict Twine metadata, fresh outside-checkout installed behavior and a one-root tracked-source ZIP.

Raw logs and environment/version lists will be retained with measured performance observations and checksums. Counts from repeated/subset runs will not be added together. The minimum direct-dependency profile does not certify optional PyArrow's lowest version. Synthetic calculations do not certify whole-report performance, production readiness or independent security review.
