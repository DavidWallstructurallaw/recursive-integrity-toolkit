# PHASE_1_PLAN

## Document control

| Field | Value |
|---|---|
| Project | Recursive Integrity Toolkit |
| Target release | v0.1 |
| Phase | Phase 1: Repository Scaffold |
| Status | APPROVED FOR EXECUTION |
| Primary owner | Technical Maintainer |
| Theory owner | Xiangyu Guo |
| Depends on | Approved Phase 0 baseline and `PHASE_0_APPROVAL.md` |
| Primary objective | Create an installable, import-safe, auditable repository scaffold without implementing analytical algorithms |
| Phase result | A GitHub-ready repository skeleton that passes architecture, packaging, import, schema, ownership, license, and no-network checks |

Phase 1 creates the repository structure required for later implementation.

It does not implement support calculations, diversity metrics, closure bounds, lineage analysis, simulations, or report-generation logic.

The phase succeeds when the repository can be installed, imported, inspected, and tested as a scaffold while remaining fully inside the approved v0.1 architecture.

---

## 1. Phase 1 purpose

Phase 1 converts the approved Phase 0 specification bundle into a formal software repository.

The repository must establish:

- project identity,
- package identity,
- directory structure,
- module ownership,
- package metadata,
- dependency declarations,
- schema placeholders,
- test and fixture structure,
- hero example files,
- license and governance files,
- CI workflow skeletons,
- architecture-compliance checks.

Phase 1 should make later work easier without deciding later work in code.

---

## 2. Authority

Phase 1 must follow the approved order of authority:

1. `PHASE_0_APPROVAL.md`
2. approved decisions in `UNRESOLVED_DECISIONS.md`
3. `PROJECT_INSTRUCTIONS.md`
4. `REPOSITORY_ARCHITECTURE.md`
5. `DEPENDENCY_STRATEGY.md`
6. `V0.1_PRODUCT_SPEC.md`
7. `DEFINITIONS_AND_UNITS.md`
8. `DATA_AND_PROVENANCE_SPEC.md`
9. `OBSERVABILITY_AND_REPORTING.md`
10. `THEORY_TO_CODE_TRACEABILITY.md`
11. `VALIDATION_PLAN.md`
12. privacy, licensing, success, and governance files

When files conflict, implementation stops and the conflict is recorded.

No Phase 1 file may silently choose a new product definition.

---

## 3. Phase boundary

### 3.1 Allowed work

Phase 1 may create:

- repository directories,
- package metadata,
- root project files,
- import-safe module stubs,
- ownership docstrings,
- data-model placeholders,
- JSON Schema placeholders,
- test-file placeholders,
- fixture directories,
- canonical hero files,
- GitHub workflow skeletons,
- architecture and traceability check scripts,
- package-build smoke tests,
- CLI help and version behavior,
- license and governance files.

### 3.2 Forbidden work

Phase 1 must not implement:

- state-frequency calculations,
- support-size calculations,
- Gini-Simpson diversity,
- support comparison,
- tail selection,
- extinction probabilities,
- source-share calculations,
- closure exposure bounds,
- graph traversal,
- cycle detection,
- external-root tracing,
- ancestry HHI,
- effective external-root count,
- resampling simulation,
- external reopening simulation,
- formal audit-result assembly,
- JSON analytical reports,
- Markdown analytical reports,
- HTML analytical reports,
- semantic inference,
- human-versus-synthetic inference,
- external-grounding inference,
- universal scores.

### 3.3 No premature partial implementation

A function containing an incomplete formula is still algorithm implementation.

Phase 1 should prefer:

- no public function,
- an import-safe stub,
- a clearly phase-labeled placeholder type,
- or a private placeholder raising a development-stage error.

It must not contain provisional analytical output.

---

## 4. Phase 1 deliverables

Phase 1 produces the following deliverables.

### 4.1 Repository root

```text
recursive-integrity-toolkit/
```

### 4.2 Root project files

```text
README.md
LICENSE
NOTICE
pyproject.toml
CHANGELOG.md
CONTRIBUTING.md
SECURITY.md
CODE_OF_CONDUCT.md
MAINTAINERS.md
THEORY_SOURCES.md
THIRD_PARTY_NOTICES.md
```

### 4.3 Approved Phase 0 files

The repository root must include the approved Phase 0 specification files.

### 4.4 Package scaffold

```text
src/recursive_integrity_toolkit/
```

with all approved modules and subpackages.

### 4.5 Schema scaffold

```text
schemas/
```

with the approved machine-readable schema files.

### 4.6 Documentation scaffold

```text
docs/
```

with public documentation placeholders.

### 4.7 Test scaffold

```text
tests/
```

with unit, integration, golden, performance, and fixture directories.

### 4.8 Hero example

```text
examples/hero/
```

with approved records, provenance, configuration, version order, and expected outputs.

### 4.9 Script scaffold

```text
scripts/
```

with architecture, specification, traceability, golden, and release-check scripts.

### 4.10 CI scaffold

```text
.github/workflows/
```

with initial CI, golden, security, and release workflows.

### 4.11 Phase completion artifacts

```text
PHASE_1_COMPLETION.md
ARCHITECTURE_COMPLIANCE_REPORT.md
```

### 4.12 Repository package

```text
recursive-integrity-toolkit-phase1.zip
```

---

## 5. Work sequence

Phase 1 should be completed in ten controlled work units.

---

## 6. Work Unit 1: Repository root and approved source bundle

### Objective

Create the repository root and copy the approved Phase 0 baseline into it.

### Create

```text
recursive-integrity-toolkit/
```

### Add

- all approved Phase 0 Markdown files,
- `PHASE_0_APPROVAL.md`,
- `PHASE_1_PLAN.md`.

### Validation

- every approved file exists,
- no Draft version remains,
- file names remain unchanged,
- no duplicate specification exists,
- Phase 0 approval hash manifest is preserved.

### Stop condition

Stop when any approved Phase 0 file is missing or appears to be an earlier Draft.

---

## 7. Work Unit 2: Root governance, license, and project identity files

### Objective

Create the public repository identity and governance shell.

### Files

```text
README.md
LICENSE
NOTICE
CHANGELOG.md
CONTRIBUTING.md
SECURITY.md
CODE_OF_CONDUCT.md
MAINTAINERS.md
THEORY_SOURCES.md
THIRD_PARTY_NOTICES.md
```

### Required content

#### `README.md`

Must include:

- product statement,
- current Phase 1 status,
- local-first principle,
- v0.1 scope,
- prohibited scores,
- hero example location,
- repository structure summary,
- licensing summary,
- theory-source links.

It must not claim that analytical features are already implemented.

#### `LICENSE`

Recommended:

```text
Apache License 2.0
```

#### `NOTICE`

Must separate:

- code attribution,
- specification attribution,
- theory-source attribution,
- third-party notices.

#### `CHANGELOG.md`

Initial entry:

```text
Unreleased
Phase 1 repository scaffold
```

#### `CONTRIBUTING.md`

Must include:

- traceability requirements,
- test ownership,
- private-data restriction,
- license terms,
- phase-boundary rule.

#### `SECURITY.md`

Must include:

- local-first security posture,
- supported release status,
- vulnerability-reporting route,
- no private data in public issues,
- no-network baseline.

#### `MAINTAINERS.md`

Must identify:

- Theory Owner,
- currently unassigned or acting Technical Maintainer,
- review roles.

#### `THEORY_SOURCES.md`

Must identify:

- exact theory titles,
- author,
- versions,
- license,
- toolkit role,
- canonical publication references where available.

#### `THIRD_PARTY_NOTICES.md`

May begin with approved direct dependencies and a statement that exact versions will be filled during Phase 1 verification.

### Validation

- license files exist,
- theory assets remain separately licensed,
- no full theory PDF is added to the public repository by default,
- no license statement conflicts with `LICENSING_NOTES.md`.

---

## 8. Work Unit 3: Package metadata and dependency verification

### Objective

Create a valid package manifest and verify the approved dependency baseline.

### File

```text
pyproject.toml
```

### Recommended build configuration

- build backend: Hatchling,
- package layout: `src`,
- Python: `>=3.11`,
- package name: `recursive-integrity-toolkit`,
- import package: `recursive_integrity_toolkit`,
- CLI commands:
  - `rit`
  - `recursive-integrity`.

### Required runtime dependencies

```text
NumPy
pandas
```

### Optional runtime extra

```text
PyArrow for Parquet
```

### Development groups

- test,
- lint,
- type,
- release,
- security,
- dev.

### Phase 1 verification

Verify:

- package metadata parses,
- wheel builds,
- source distribution builds,
- clean installation works,
- core import succeeds without PyArrow,
- optional Parquet absence does not break core import,
- dependency licenses are compatible,
- no dependency makes a required network call during import.

### No analytical validation

Dependency verification must not implement metrics merely to demonstrate NumPy or pandas.

---

## 9. Work Unit 4: Python package scaffold

### Objective

Create the approved import-safe package tree.

### Core files

```text
__init__.py
__main__.py
cli.py
config.py
errors.py
models.py
result.py
```

### Subpackages

```text
io/
observability/
representations/
metrics/
lineage/
reports/
utils/
```

### Required file content

Each module must contain:

- file purpose,
- primary Trace ID or Product Rule ID,
- future public responsibility,
- assumptions,
- limits,
- current phase status.

### Example module header

```python
\"\"\"
Purpose:
    Own future Gini-Simpson diversity and support calculations.

Primary trace ownership:
    T1

Current phase:
    Phase 1 scaffold only.

Implementation status:
    No analytical behavior is implemented.

Limits:
    Observed diversity remains representation-bound.
    Diversity does not establish functional failure.
\"\"\"
```

### Import behavior

Required:

- package import succeeds,
- every subpackage import succeeds,
- import causes no file loading,
- import causes no logging side effect,
- import causes no network call.

### CLI scaffold

Phase 1 CLI may support:

```text
rit --help
rit version
```

It may also display:

```text
Phase 1 scaffold. Audit functionality is not implemented.
```

It must not emit analytical results.

---

## 10. Work Unit 5: Documentation and JSON Schema scaffold

### Objective

Create public documentation paths and machine-readable structural contracts.

### Documentation files

```text
docs/architecture.md
docs/cli.md
docs/report_schema.md
docs/data_schema.md
docs/theory_traceability.md
docs/privacy.md
docs/release_process.md
```

### Schema files

```text
schemas/report.schema.json
schemas/config.schema.json
schemas/schema_mapping.schema.json
schemas/version_order.schema.json
schemas/normalized_manifest.schema.json
```

### Phase 1 schema scope

Schemas may define:

- schema version,
- top-level object,
- required top-level keys,
- basic types,
- enum registries,
- rejection of executable mapping fields,
- no additional arbitrary top-level behavior.

Schemas must not encode unapproved algorithm logic.

### Validation

- every schema is valid JSON,
- each schema identifies its draft version,
- required report top-level sections exist,
- config schema does not activate simulation by default,
- mapping schema contains only approved operations.

---

## 11. Work Unit 6: Test and fixture scaffold

### Objective

Create the full approved testing structure.

### Directories

```text
tests/fixtures/
tests/unit/
tests/integration/
tests/golden/
tests/performance/
```

### Unit test files

Create all files listed in `THEORY_TO_CODE_TRACEABILITY.md`.

### Phase 1 test scope

Phase 1 tests should verify:

- package import,
- module ownership docstrings,
- file existence,
- schema JSON validity,
- license files,
- approved tree,
- prohibited path absence,
- CLI help and version,
- optional dependency isolation,
- no-network import,
- no analytical functions exposed.

### Later-phase test placeholders

Tests belonging to later phases may contain:

- module-level docstring,
- intended owner ID,
- `pytest.skip` with a phase reason,

or remain absent until their approved phase.

Recommended approach:

- create the file with a clear phase marker,
- avoid large numbers of permanent skipped tests in the default Phase 1 CI.

### Fixture directories

Create every approved fixture directory.

Only the hero fixture must contain full data in Phase 1.

Other directories may contain a short `README.md` describing their future purpose.

---

## 12. Work Unit 7: Hero example installation

### Objective

Install the approved hero example without running analytical calculations.

### Files

```text
records_v1.csv
records_v2.csv
provenance.csv
version_order.json
config.json
EXPECTED_OUTPUTS.md
```

### Required checks

- records conform structurally to the approved columns,
- provenance uses composite parent references,
- version order lists `v1`, then `v2`,
- representation is `topic`,
- expected outputs include approved golden values,
- no value conflicts with the approved Phase 0 files.

### Forbidden Phase 1 behavior

Do not calculate:

- support,
- diversity,
- closure bounds,
- root counts,
- HHI.

Phase 1 may verify the files are present and syntactically readable.

---

## 13. Work Unit 8: Architecture and traceability scripts

### Objective

Create scaffold-level compliance scripts.

### `check_spec_consistency.py`

Phase 1 behavior may check:

- required specification files exist,
- file names match,
- approved status appears,
- referenced owner IDs have source files,
- no unresolved Phase 1 blocker remains.

### `check_traceability.py`

Phase 1 behavior may check:

- every module docstring includes ownership,
- every planned public module has an owner,
- prohibited score modules are absent,
- deferred branches are absent.

### `build_golden.py`

Phase 1 status:

```text
placeholder only
```

It must not calculate analytical output.

### `normalize_golden.py`

Phase 1 status:

```text
placeholder only
```

### `release_check.py`

Phase 1 may check:

- root files,
- package build,
- approved status,
- architecture compliance,
- license presence.

---

## 14. Work Unit 9: CI workflow scaffold

### Objective

Create GitHub Actions workflows that validate the scaffold.

### `ci.yml`

Run:

- package installation,
- package import,
- CLI help,
- CLI version,
- repository tree check,
- schema JSON validation,
- ownership-docstring check,
- no prohibited directories,
- test suite.

### `golden.yml`

Phase 1 behavior:

- verify hero expected-output file exists,
- verify golden directories exist,
- do not compare analytical reports yet.

### `security.yml`

Run:

- no-network import check,
- unsafe dependency inspection where practical,
- path and mapping schema checks,
- secret-pattern scan on fixtures where practical.

### `release.yml`

Phase 1 behavior:

- build wheel,
- build source distribution,
- verify license and notice files,
- verify package metadata.

### Matrix

Recommended:

- Ubuntu with Python 3.11,
- Ubuntu with Python 3.12,
- Windows with Python 3.11,
- Windows with Python 3.12.

---

## 15. Work Unit 10: Phase 1 completion audit

### Objective

Prove that the scaffold matches the approved architecture and contains no analytical implementation.

### Create

```text
ARCHITECTURE_COMPLIANCE_REPORT.md
PHASE_1_COMPLETION.md
```

### Architecture report contents

- required paths,
- missing paths,
- prohibited paths,
- module ownership status,
- dependency-direction status,
- schema status,
- license status,
- CI status,
- import status,
- no-network status,
- no-algorithm status.

### Completion report contents

- work units completed,
- files created,
- validation executed,
- decisions used,
- conflicts,
- deferred items,
- Phase 1 gate result.

### Final status values

Use one:

```text
PHASE COMPLETE
BLOCKED BY DECISION
FAILED ACCEPTANCE GATE
```

---

## 16. Detailed module ownership table

| Module | Primary owner | Phase 1 action |
|---|---|---|
| `cli.py` | product orchestration | help and version only |
| `config.py` | PR-007, PR-016 | config type placeholders |
| `errors.py` | product rules | error-code definitions or placeholders |
| `models.py` | shared contracts | type placeholders |
| `result.py` | PR-012, PR-013 | result-section type placeholders |
| `io/loaders.py` | PR-002, PR-017 | docstring and interface placeholder |
| `io/schema_mapping.py` | PR-003 | docstring and allowlist placeholder |
| `io/normalization.py` | PR-001, PR-008 | docstring and type placeholder |
| `io/validation.py` | PR-001, PR-004, PR-007, PR-008, PR-009 | docstring and interface placeholder |
| `observability/levels.py` | PR-010, PR-011 | docstring and status types only |
| `representations/base.py` | representation contract | protocol placeholder |
| `representations/field.py` | T1 input basis | placeholder |
| `representations/content_hash.py` | PR-006 | placeholder |
| `representations/compatibility.py` | T1, PR-011 | placeholder |
| `metrics/duplicates.py` | PR-006 | no algorithm |
| `metrics/diversity.py` | T1 | no formula |
| `metrics/tail.py` | T2 | no formula |
| `metrics/provenance.py` | PR-004, PR-005, T3 | no calculation |
| `metrics/bounds.py` | T3 | no formula |
| `metrics/resampling.py` | T1, T2, T5 | no simulation |
| `lineage/graph.py` | PR-008 | no graph construction |
| `lineage/cycles.py` | T6 | no cycle detection |
| `lineage/ancestry.py` | T4 | no ancestry calculation |
| `reports/assembly.py` | PR-012, PR-014, PR-018 | no report assembly |
| `reports/json_report.py` | PR-013, PR-016 | no analytical rendering |
| `reports/markdown_report.py` | PR-013, PR-018 | no analytical rendering |
| `reports/html_report.py` | optional | placeholder only |
| `utils/hashing.py` | PR-006, PR-015, PR-016 | interface placeholder |
| `utils/logging.py` | PR-015 | safe logging scaffold |
| `utils/ordering.py` | PR-016 | interface placeholder |
| `utils/paths.py` | PR-017 | interface placeholder |

---

## 17. Phase 1 validation suite

### 17.1 Required checks

```text
repository tree matches
package metadata parses
wheel builds
source distribution builds
package imports
subpackages import
CLI help works
CLI version works
schemas parse as JSON
license files exist
approved specification files exist
module ownership docstrings exist
no prohibited directory exists
no hidden network call occurs
optional Parquet dependency remains optional
hero files exist
hero files use canonical names
no analytical public function is exposed
```

### 17.2 No-algorithm review

The completion audit should inspect analytical modules for:

- mathematical operators,
- metric-return values,
- random sampling,
- graph traversal,
- report metric population.

Docstrings may contain formulas only when copied as documentation placeholders if necessary.

Recommended stricter rule:

- avoid formula bodies and executable examples in Phase 1 modules.

### 17.3 Import-side-effect review

Package import must not:

- read example files,
- create output directories,
- configure root logger,
- write temporary files,
- call network,
- load optional dependencies,
- run tests.

---

## 18. Phase 1 acceptance gate

Phase 1 passes only when all conditions below are satisfied.

### Repository structure

- [ ] root directory exists,
- [ ] root files exist,
- [ ] approved specification files exist,
- [ ] package tree matches architecture,
- [ ] test tree exists,
- [ ] docs and schemas exist,
- [ ] hero example exists,
- [ ] CI workflows exist.

### Packaging

- [ ] `pyproject.toml` is valid,
- [ ] wheel builds,
- [ ] source distribution builds,
- [ ] package installs,
- [ ] package imports,
- [ ] CLI help works,
- [ ] CLI version works.

### Dependencies

- [ ] Python baseline recorded,
- [ ] NumPy and pandas justified,
- [ ] PyArrow remains optional,
- [ ] dev tools remain nonruntime,
- [ ] no web, model, database, telemetry, or plugin dependency exists.

### Traceability

- [ ] every module has ownership metadata,
- [ ] every test file has intended owner,
- [ ] no deferred module exists,
- [ ] no forbidden score file exists.

### Privacy and security

- [ ] no network call at import,
- [ ] no source content in logs,
- [ ] no executable mapping framework,
- [ ] no remote content loader,
- [ ] no secrets in fixtures.

### Phase integrity

- [ ] no analysis algorithm exists,
- [ ] no analytical result is emitted,
- [ ] no Phase 2 or later gate is claimed,
- [ ] Phase 1 completion report is created.

---

## 19. Failure conditions

Phase 1 fails when:

- an approved root file is missing,
- the package cannot build,
- the package cannot import,
- optional PyArrow becomes mandatory,
- a module has no owner,
- a forbidden directory appears,
- an analytical formula is implemented,
- CLI emits audit metrics,
- import reads user or example data,
- import makes a network call,
- a Draft specification is included,
- licensing statements conflict,
- hero files conflict with approved values,
- a blocking decision reappears.

---

## 20. Deferred work after Phase 1

Phase 1 explicitly defers:

- ingestion implementation,
- schema mapping execution,
- canonical validation,
- observability classification,
- representation assignment,
- duplicate calculation,
- diversity calculation,
- tail calculation,
- provenance metrics,
- closure bounds,
- graph construction,
- ancestry metrics,
- report assembly,
- analytical CLI,
- longitudinal comparison,
- simulations.

These enter only in their approved later phases.

---

## 21. Phase 1 output package

The final package should be:

```text
recursive-integrity-toolkit-phase1.zip
```

The archive should contain one repository root:

```text
recursive-integrity-toolkit/
```

It should be directly suitable for:

- local extraction,
- Git initialization,
- GitHub upload,
- clean package installation,
- later Phase 2 implementation.

---

## 22. Execution reporting format

After each work unit, report:

### Completed

Files and directories created.

### Validation

Checks performed and results.

### Decisions used

Relevant approved `UD-*` IDs.

### Conflicts

Exact conflict or `None`.

### Deferred

Later-phase behavior intentionally excluded.

### Stop status

Use:

```text
TASK COMPLETE, PHASE CONTINUES
PHASE COMPLETE
BLOCKED BY DECISION
FAILED ACCEPTANCE GATE
```

---

## 23. Approved decisions used

Phase 1 depends especially on:

```text
UD-001
UD-002
UD-004
UD-006
UD-017
UD-019
UD-022
UD-023
UD-024
UD-025
UD-026
UD-027
UD-032
UD-033
UD-036
```

All were approved by the Theory Owner without exceptions during Phase 0 closure.

---

## 24. Approval

### Theory Owner authorization

Phase 1 was authorized by the approved Phase 0 baseline.

Theory Owner:

```text
Xiangyu Guo
```

Authorization date:

```text
2026-07-29
```

Status:

```text
APPROVED FOR EXECUTION
```

### Technical Maintainer completion acknowledgment

To be completed at the Phase 1 gate.

- [ ] Repository structure complete
- [ ] Package build complete
- [ ] Dependency verification complete
- [ ] Architecture checks complete
- [ ] No-algorithm audit complete
- [ ] Phase 1 completion report issued

Maintainer:

```text

```

Completion date:

```text

```

---

## 25. Change-control rule

After this plan is approved:

1. Phase 1 scope must not expand silently,
2. a new root or package directory requires architecture review,
3. a new dependency requires dependency review,
4. a module owner must not change silently,
5. an analytical function must not enter Phase 1,
6. hero data must not change without golden review,
7. a CI requirement may be strengthened without weakening other gates,
8. any blocker must be recorded before work continues,
9. Phase 2 cannot begin until the Phase 1 completion gate passes.
