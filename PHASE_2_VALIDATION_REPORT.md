# PHASE_2_VALIDATION_REPORT

Status: **FAILED ACCEPTANCE GATE; BLOCKED BY DECISION**.
Tested candidate: `068cdf0baf87f279f6a4e36271f197df9c1f3696`.

## Actual commands and results

| Environment or command | Observed result |
|---|---|
| Core Ubuntu/Python 3.12: full `python -m pytest -p no:cacheprovider -q --junitxml=...` | 1150 passed, 1 failed, 15.37 seconds, exit 1 |
| Real extra Ubuntu/Python 3.12: same full command with `RIT_TEST_PARQUET=1` | 1153 passed, 1 failed, 9.32 seconds, exit 1 |
| `python -m pip install ".[test,parquet]"` | Succeeded; real PyArrow 25.0.1 installed |
| Three real PyArrow cases | Roundtrip, row limit and invalid-file cases passed |
| Security Boundary workflow | Completed successfully |
| Four core OS/Python jobs | All completed with a failed complete-suite gate |
| Build/Delivery workflow | Failed at core-suite gate; later delivery commands not run |
| Byte-level Phase 0 audit, with local copies matched to current Git blob identifiers | 15 approved hashes match; VALIDATION_PLAN.md differs |

The core and extra-enabled suites overlap; their counts must not be added. Twenty Step 10 evidence tests were added to the 1131-case prior core suite. The extra-enabled suite adds the existing three real-Parquet cases. No failed test is hidden through skip, xfail, ignore or continue-on-error. Subsequent workflow steps marked skipped were not run because a preceding gate failed; they are not counted as test passes.

## Sole observed test failure

`tests/integration/test_ci_workflows.py::test_phase2_approved_phase0_hashes_match_current_sources`

Expected SHA-256:
`16f5fe539da2b3cff1c3e0a2854208bd7fbc1e4c5b332684265b06a03a90cf2f`

Current SHA-256:
`564abf56c91141d0cd8ca09024f1cf6dda63bf4ba12acf6563bb7cbc158a84f7`

Current Git blob: `95f75b233d8d73c70a5b7b87691deb6b5d763c18`.
Approved archive Git blob: `cde1b7dfe254841a26b68578565de7778eb9052e`.

The exact diff contains only the approval-status line and the pending/approved decision label at source lines 10 and 36. A local byte-level comparison verified that applying exactly those two replacements yields the approved file byte for byte. The current draft was originally added in the main-branch commit named `Add missing VALIDATION_PLAN.md`; Step 10 did not change it.

## Evidence and remaining execution

CI run `35189874671`, core log job `105099873944`, real-Parquet log job `105099873767`; Security run `35189874658`; Build/Delivery run `35189874618`. Actual JUnit and raw test logs are retained as workflow artifacts, including failures. Local evidence contains a reproducible blob/hash audit and exact restoration diff. Tool-returned hosted excerpts are labelled as excerpts rather than local raw logs.

Local GitHub cloning failed due DNS resolution. Earlier local static/helper checks are not presented as a full repository test. The complete-suite results above come from the actual GitHub checkout. Full installed-wheel and source-distribution validation, final artifact integrity and final successful multi-platform acceptance remain pending after the narrow baseline repair is approved.

No package implementation changed and no analytical computation was performed. Phase 3 is not authorized.
