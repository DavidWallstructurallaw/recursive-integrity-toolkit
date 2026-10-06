# 0.1.0 handoff rehearsal

Rehearsal date: 2026-10-06 UTC. Status: **all nine rehearsal steps executed;
human review and acceptance of this report pending; official publication pending**.

This is a fresh assistant review by a reviewer that did not author the
implementation. The reviewer cloned the public branch into a separate checkout,
installed fresh dependencies in a new virtual environment, and performed the
commands below. A second assistant supplied a read-only trace cross-check.
This is not external human review, a human role appointment, or a Theory Owner,
Technical Maintainer, mathematical, security, or domain sign-off.
GOVERNANCE_AND_HANDOFF.md section 28.4 still requires human review of this
assistant-authored document for accuracy, licensing, traceability and public tone.

No implementation, frozen specification, golden, workflow or dependency declaration
was edited. No GitHub mutation, merge, tag, Release or registry upload was performed.
The existing full candidate and performance evidence was read in
[RELEASE_0_1_0.md](RELEASE_0_1_0.md), not rerun or independently re-downloaded here.
This bounded rehearsal does not replace that evidence or the broader maintainer
onboarding requirements in governance section 21.

## 1. Clone repository: completed

The following commands use public source and relative paths. Run them in a fresh
parent directory; the sibling execution directory keeps Hero execution outside
the checkout. Subsequent repository commands start in `release_handoff_review`.

```bash
git clone --branch release-0.1.0 --single-branch \
  https://github.com/DavidWallstructurallaw/recursive-integrity-toolkit.git \
  release_handoff_review
cd release_handoff_review
git rev-parse HEAD
git rev-parse 'HEAD^{tree}'
git status --short
git diff --name-status c5837845da603167e6f0c8216766d0a3a874835e HEAD
```

Observed HEAD: `9fac436dc619900b19bc0ad4fa3cd38d3087435c`.
Tree: `3b2ccf2f98e09d138f6f4012057bf199a236254a`.
The initial working tree was clean. The only difference from tested candidate
`c5837845da603167e6f0c8216766d0a3a874835e` was `RELEASE_0_1_0.md`.
The remote was the HTTPS repository above. No `AGENTS.md` existed in the checkout
or its containing workspace directories.

Read the relevant requirements in `PROJECT_INSTRUCTIONS.md`,
`GOVERNANCE_AND_HANDOFF.md` (including sections 14, 28.4 and 31),
`docs/release_process.md`, `MAINTAINERS.md`, `UNRESOLVED_DECISIONS.md`,
`RELEASE_0_1_0.md`, `README.md` and the definition/trace documents below.
The frozen Phase 0 instructions retain their historical phase wording; the current
release preparation record describes the accepted later implementation boundary.

## 2. Install package: completed

```bash
python -m venv .venv-handoff
.venv-handoff/bin/python -m pip install '.[test,release]'
.venv-handoff/bin/python -m pip check
.venv-handoff/bin/rit version
.venv-handoff/bin/recursive-integrity version
```

All commands exited zero. Installation was non-editable, into a new venv without
system site-packages; dependencies were downloaded rather than supplied through
an older toolkit installation. `pip check` reported no broken requirements.
Both console aliases reported `recursive-integrity-toolkit 0.1.0`.

| Executed environment | Value |
| --- | --- |
| OS / architecture | Linux 6.18.44, x86_64, glibc 2.39 |
| Python | 3.12.14, Clang 22.1.3 |
| venv pip | 25.0.1 |
| NumPy / pandas | 2.5.3 / 3.0.6 |
| pytest / build / twine | 9.1.1 / 1.6.1 / 7.0.0 |
| Build backend | setuptools 84.0.0, recorded in wheel `WHEEL` metadata |
| PyArrow | Absent; `importlib.util.find_spec("pyarrow")` returned `None` |

Isolated `python -I` import reported matching `__version__` and installed
distribution metadata of `0.1.0`. Its origin was
`.venv-handoff/lib/python3.12/site-packages/recursive_integrity_toolkit/__init__.py`,
under the new venv, not `src/`. This origin/version assertion was repeated after
installing the separately built wheel in step 7.

## 3. Run Hero: completed

```bash
mkdir ../release_handoff_execution
RIT_REPO="$PWD"
cd ../release_handoff_execution
env -u PYTHONPATH "$RIT_REPO/.venv-handoff/bin/python" -I -c \
  'from pathlib import Path; import sys, importlib.metadata as m, recursive_integrity_toolkit as r; assert Path(r.__file__).resolve().is_relative_to(Path(sys.prefix).resolve() / "lib"); assert r.__version__ == m.version("recursive-integrity-toolkit") == "0.1.0"; print(r.__file__)'
env -u PYTHONPATH "$RIT_REPO/.venv-handoff/bin/rit" example \
  --out ./hero-workspace > hero.stdout.log 2> hero.stderr.log
env -u PYTHONPATH "$RIT_REPO/.venv-handoff/bin/rit" example --lineage \
  --out ./hero-lineage-workspace > hero-lineage.stdout.log 2> hero-lineage.stderr.log
cd "$RIT_REPO"
```

Both runs exited zero and wrote `reports/report.json` and `reports/report.md`.
The actual execution directory was the sibling of the fresh checkout. Both
stderr files were empty. The installed built-wheel repeat in step 7 also passed.
Parsed JSON assertions confirmed the following for all applicable runs:

| Observation | Ordinary Hero | Lineage Hero, including built-wheel repeat |
| --- | --- | --- |
| Toolkit / schema / run status | 0.1.0 / 1.3 / complete | Same |
| Errors / warnings / simulations | 0 / 0 / empty object | Same |
| Maximum input observability | Level 4 | Level 4 |
| Topic support v1 → v2 | 8 → 5 | Same |
| Gini-Simpson diversity v1 → v2 | 0.875 → 0.75 | Same |
| Support retention | 0.625 | Same |
| Missing later states | battery, lizard, turtle | Same |
| v2 human / synthetic shares | 0.5 / 0.5 | Same |
| Direct closure bounds | [0.5, 0.5] | Same |
| Lineage execution | `not_requested` | `completed` |
| Distinct external roots / HHI / effective roots | Not executed | 5 / 0.25 / 4 |
| Grounded / closed / unresolved targets | Not executed | 8 / 0 / 0 |
| Lineage closure bounds | Not executed | [0, 0] |

All six extracted input files matched `examples/hero/` byte for byte in each
of the three workspaces. Expectations were checked against the documented Hero
values and existing arithmetic, not generated from a new golden. The reported
zero toolkit-managed network calls is not a process-wide network-isolation test;
this rehearsal did not rerun the blocked-network security suite. No performance
claim is drawn from these tiny examples.

## 4. Locate definitions: completed

`DEFINITIONS_AND_UNITS.md` section 9.2 defines `gini_simpson_diversity` as
`1 - sum(p_i squared)`: dimensionless, a derived metric, zero for one occupied
state, and at most `1 - 1/K` for fixed finite support size K. Its formula registry
names F-003. Support and comparisons require an explicit representation;
unavailable results are not interchangeable with measured zero.

`THEORY_SOURCE_MAP.md` TM-C04 supplies the declared-representation meaning and
the prohibition against calling exact text uniqueness semantic diversity.
`THEORY_TO_CODE_TRACEABILITY.md` T1.A distinguishes observed diversity from
the separate closed-resampling expectation/scenario. The Hero uses literal
`topic` values with representation version `hero-topic-v1`.

## 5. Trace one metric to its owner: completed

| Link | Located evidence |
| --- | --- |
| Definition / formula | `DEFINITIONS_AND_UNITS.md` section 9.2 / F-003 |
| Theory / trace | `THEORY_SOURCE_MAP.md` TM-C04; `THEORY_TO_CODE_TRACEABILITY.md` section 6, T1.A |
| Current trace index | `docs/theory_traceability.md`, “Phase 3 Step 4 traceability” and “Phase 3 final field index” |
| Arithmetic owner | `src/recursive_integrity_toolkit/metrics/diversity.py`, `_metrics`; trace T1, formula F-003 |
| Public API | `calculate_state_distribution`, `distribution_from_counts`, `distribution_from_probabilities` |
| Unit test | `tests/unit/test_T1_diversity.py::test_F003_A_to_D` |
| Report adapter | `src/recursive_integrity_toolkit/reports/assembly.py`, `_distribution` |
| Report field | `derived_metrics.diversity.by_version.<version>.gini_simpson_diversity`; numeric result under `.value` |
| Report contract | `docs/report_schema.md`, “Analytical field registry”; `schemas/report.schema.json` |

The installed Hero v2 envelope had value `0.75`, denominator `8`, unit
`dimensionless`, evidence `derived_metric`, method `F-003`, owner/trace `T1`,
and the declared topic representation. The source arithmetic uses `fsum` of
squared probabilities and subtracts from one, without clipping or normalization.
Its limits exclude functional-failure, semantic-completeness, source-independence,
grounding and model-performance conclusions.

**Documentation navigation discrepancy for human review:** frozen
`THEORY_SOURCE_MAP.md` TM-C04 lists the older short path
`derived_metrics.diversity.gini_simpson`. The current trace field table,
schema documentation and actual report use the versioned field above.
Likewise, planned APIs in the frozen trace document are sketches, not collected
Python symbols. This did not prevent locating or executing the current owner;
no mathematical disagreement or new runtime defect was found. No frozen
specification was changed or approval inferred from this observation.

## 6. Run a meaningful unit test: completed

```bash
.venv-handoff/bin/python -m pytest -q \
  tests/unit/test_T1_diversity.py::test_F003_A_to_D
```

Result: **4 passed in 0.76 seconds**, exit zero, no failures or skips.
The parameterized test uses independently authored rational expectations:
singleton → 0; two equal states → 1/2; four equal states → 3/4;
(1/2, 1/4, 1/4) → 5/8. It also checks complementary Simpson concentration and
F-003/F-004 identifiers. `tests/conftest.py` inserts the checkout's `src/` path,
so this is a source unit test; installed behavior is separately evidenced by Hero.
No full CI, compatibility matrix or performance suite was rerun.

## 7. Build package: completed

The execution directory from step 3 must exist. The build actually ran before
the first Hero calls and before writing this document, with unchanged tracked
source. Logical steps are grouped here to match governance section 31.

```bash
RIT_BUILD_EPOCH="$(git show -s --format=%ct HEAD)"
SOURCE_DATE_EPOCH="$RIT_BUILD_EPOCH" .venv-handoff/bin/python -m build \
  --outdir ../release_handoff_execution/dist \
  > ../release_handoff_execution/build.log 2>&1
.venv-handoff/bin/python -m twine check --strict ../release_handoff_execution/dist/*
.venv-handoff/bin/python -m pip install --no-index --no-deps --force-reinstall \
  ../release_handoff_execution/dist/recursive_integrity_toolkit-0.1.0-py3-none-any.whl
RIT_REPO="$PWD"
cd ../release_handoff_execution
env -u PYTHONPATH "$RIT_REPO/.venv-handoff/bin/python" -I -c \
  'from pathlib import Path; import sys, importlib.metadata as m, recursive_integrity_toolkit as r; assert Path(r.__file__).resolve().is_relative_to(Path(sys.prefix).resolve() / "lib"); assert r.__version__ == m.version("recursive-integrity-toolkit") == "0.1.0"; print(r.__file__)'
env -u PYTHONPATH "$RIT_REPO/.venv-handoff/bin/rit" example --lineage \
  --out ./hero-built-wheel-workspace \
  > hero-built-wheel.stdout.log 2> hero-built-wheel.stderr.log
cd "$RIT_REPO"
```

All build, strict Twine, exact-wheel installation and repeat Hero commands exited
zero. The build used `SOURCE_DATE_EPOCH=1790927603` and built the wheel from its
sdist. Both archive metadata versions were `0.1.0`. Direct archive reads verified
all 41 runtime modules and 18 packaged resources against this checkout byte for
byte in both wheel and sdist. Wheel license members included `LICENSE` and `NOTICE`.
The sdist did not contain the rehearsal venv. No second independent sdist
installation or reproducible-build comparison is claimed.

| Locally built artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `recursive_integrity_toolkit-0.1.0-py3-none-any.whl` | 393068 | `85dbe7a0a9dcf27371111c314a953f54c00e32531209b3fed75952903678ff14` |
| `recursive_integrity_toolkit-0.1.0.tar.gz` | 361579 | `8aa4ffef20e2f2b920ea58eaf678001c454a251f3b24c083e2b143d0c66d8a56` |

These are rehearsal builds from `9fac436d` with its timestamp, not the hosted
candidate artifacts from `c5837845`. Their compressed hashes differ from the
release preparation record and must not replace the candidate hashes there.
The fresh source-install wheel also had its own build hash
`166cf434d61d28ae881307a675432b97d80d3415415fd41b3e80fa5dd6bfa564`;
the explicit build/install above identifies the artifact used for the final Hero.

## 8. Identify release blockers: completed

No new executable or mathematical blocker was found in this bounded rehearsal.
The decision register contains 32 `APPROVED` and four `DEFERRED` decision entries,
with no entry whose status is `OPEN` or `RECOMMENDED`. Deferred scope is not
publication authority. `LICENSE`, `NOTICE`, `THIRD_PARTY_NOTICES.md`,
`LICENSING_NOTES.md` and `THEORY_SOURCES.md` are present; the source manifest
keeps full theory PDFs separate.

Official publication still requires the following concrete actions:

1. Human review and acceptance of this report under governance section 28.4,
   including whether this assistant non-author rehearsal satisfies section 31.
2. Identify the Technical Maintainer or explicitly declare any consolidation of
   roles, then record that maintainer's approval of the exact official release.
   `MAINTAINERS.md` still says “Unassigned or acting maintainer”, status Open.
3. Record Theory Owner approval of `official-v0.1` and the exact target commit
   under UD-032 and governance sections 9.3/14.2. The prior instruction authorizes
   merging and preparation, not an invented publication approval. Required
   mathematical, security and domain approvals must also be confirmed where
   applicable; this rehearsal grants none of those roles or approvals.
4. After those approvals and explicit publication authorization, confirm artifact
   provenance for the selected target, create tag `v0.1.0` and the GitHub Release.
   A package-registry upload remains a separately requested action.

The current candidate evidence remains bound to `c5837845`; the existing
administrative-successor policy permits disclosed reuse where executable and
authoritative bytes are unchanged. Adding this report does not silently rerun
or broaden that evidence.

## 9. Explain unavailable conclusions: completed

The installed reports retain these six unavailable conclusions even after
successful lineage execution:

| Conclusion | Why it remains unavailable |
| --- | --- |
| `model_performance_decline` | Dataset structure is not comparable, versioned model-outcome evidence. |
| `causal_ancestor_effect` | Parent topology and fractional root allocation do not identify a causal effect. |
| `universal_integrity` | No approved universal scalar or operational test exists in v0.1. |
| `universal_collapse_prediction` | Outside approved product scope; support loss does not supply a universal prediction. |
| `production_failure` | Structural fields do not measure an operational failure outcome. |
| `complete_pipeline_closure` | Declared grounding and supplied lineage do not cover every possible pipeline input or hidden dependency. |

Ordinary Hero additionally marks `lineage_analysis`, `external_ancestry` and
`lineage_closure_exposure` unavailable with `R_ANALYSIS_NOT_REQUESTED`.
The explicit lineage run removes those execution-specific unavailable entries
and reports its completed partition; it does not remove the six limitations above.
Level 4 is input eligibility, not a guarantee that every capability executed.
No scenario was requested, so simulations remained empty. UD-031 empirical
intervention ingestion remains deferred; an experimental scenario would not
establish an empirical causal effect. “Unavailable” means the supplied evidence
does not establish the conclusion, not that the conclusion is false.

## Execution errors and scope limits

The installation, selected unit test, package build, strict metadata checks and
all three Hero executions succeeded on their first actual invocation. Exploratory
lookups for guessed `tests/unit/test_diversity.py` and `MANIFEST.in` paths failed;
the real test was found as `test_T1_diversity.py`, and packaging is configured in
`pyproject.toml`. A build-log search found no verbose installed-backend line;
the backend version was read from wheel metadata instead. A one-off inspection
helper initially indexed the source-share envelope as `['human']`, raising
`KeyError`; correcting it to `['value']['human']` made the complete Hero assertions
pass. These were reviewer lookup/helper errors, not failed product executions.

This report contains the commands, source identity, resolved environment and
observations needed to repeat the bounded rehearsal from a public clone. Scratch
logs and generated artifacts are supplementary, not prerequisites for future
reviewers. Windows, Python 3.11, optional Parquet, the full candidate suite,
process-wide network blocking and large-workload performance were not repeated.
The report does not claim PDF re-derivation, general scientific validation,
external human independence or official release approval.

Stop status: **TASK COMPLETE, PHASE CONTINUES**. Rehearsal execution is complete;
human acceptance and official release approvals remain pending.
