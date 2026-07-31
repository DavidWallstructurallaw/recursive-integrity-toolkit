# DEPENDENCY_STRATEGY

## Document control

| Field | Value |
|---|---|
| Project | Recursive Integrity Toolkit |
| Target release | v0.1 |
| Phase | Phase 0 |
| Status | APPROVED PHASE 0 BASELINE |
| Primary owner | Technical Maintainer |
| Reviewers | Theory Owner, Security Reviewer, Mathematical Reviewer |
| Depends on | `PROJECT_INSTRUCTIONS.md`, `V0.1_PRODUCT_SPEC.md`, `REPOSITORY_ARCHITECTURE.md`, `PRIVACY_AND_DATA_HANDLING.md`, `LICENSING_NOTES.md`, `VALIDATION_PLAN.md`, `SUCCESS_CRITERIA.md`, `UNRESOLVED_DECISIONS.md` |
| Purpose | Freeze the dependency philosophy, runtime baseline, required and optional package classes, version policy, review gates, security constraints, and Phase 1 dependency decisions |
| Implementation code authorized | No |

This file defines how Recursive Integrity Toolkit v0.1 selects, constrains, tests, and documents software dependencies.

The governing rule is:

> Add a dependency only when it creates clear product value that cannot be achieved more safely and transparently with the supported Python standard library or an already approved dependency.

Dependencies must support auditability.

They must not hide analytical behavior, introduce network requirements, execute user code, download models, or expand v0.1 beyond its approved scope.

---

## 1. Dependency objectives

The dependency strategy should provide:

- local-first execution,
- readable implementation,
- deterministic behavior,
- support for up to approximately 100,000 rows in standard metadata audits,
- exact numerical metrics,
- optional Parquet support,
- cross-platform installation,
- low attack surface,
- low maintenance burden,
- clear license compatibility,
- replaceable internal abstractions,
- no mandatory web, cloud, database, model, or telemetry stack.

---

## 2. Runtime baseline

### 2.1 Python

Recommended baseline:

```text
Python >= 3.11
```

Related decision:

```text
UD-025
```

### 2.2 Supported release matrix

Recommended initial support:

```text
Python 3.11
Python 3.12
```

A later Python version may be added after dependency and CI validation.

### 2.3 Operating systems

Recommended required CI coverage:

```text
Ubuntu
Windows
```

Recommended later coverage:

```text
macOS
```

### 2.4 No alternate runtime requirement

v0.1 does not require:

- Java,
- Node.js,
- Rust toolchain,
- Go toolchain,
- Docker,
- database server,
- browser runtime.

A Python dependency may include compiled wheels.

The user should not need a compiler on common supported platforms when published wheels are available.

---

## 3. Dependency tiers

Dependencies are divided into five tiers.

| Tier | Meaning |
|---|---|
| Tier 0 | Python standard library |
| Tier 1 | Required runtime dependency |
| Tier 2 | Optional runtime extra |
| Tier 3 | Development and validation dependency |
| Tier 4 | Deferred or prohibited dependency class |

---

## 4. Tier 0: Python standard library

The standard library should own as much infrastructure as practical.

Recommended standard-library modules include:

```text
argparse
csv
json
tomllib
dataclasses
enum
typing
collections
pathlib
hashlib
logging
tempfile
shutil
datetime
platform
importlib.metadata
html
statistics
random
secrets
```

### 4.1 Standard-library ownership

Use the standard library for:

- CLI parsing,
- CSV and JSONL orchestration,
- TOML configuration reading,
- path handling,
- hashing,
- logging,
- temporary directories,
- platform metadata,
- HTML escaping,
- enum definitions,
- immutable configuration models where practical.

### 4.2 Standard-library limits

The standard library should not be forced into areas where doing so would create:

- opaque numerical code,
- inefficient tabular joins,
- excessive custom parsing,
- difficult cross-platform behavior,
- avoidable test burden.

---

## 5. Tier 1: required runtime dependencies

The recommended required runtime set is intentionally small.

### 5.1 NumPy

Recommended status:

```text
required
```

Purpose:

- probability vectors,
- numerical validation,
- Gini-Simpson calculations,
- finite-resampling simulation,
- stable numerical arrays,
- deterministic seeded random generation.

Primary importing modules:

```text
metrics/diversity.py
metrics/tail.py
metrics/resampling.py
lineage/ancestry.py
```

Reasons to approve:

- direct fit for the mathematical core,
- mature numerical behavior,
- transparent array operations,
- broad platform support,
- avoids implementing numerical primitives manually.

Restrictions:

- no hidden random state,
- use an explicit generator object,
- record seeds,
- validate finite values,
- avoid object-dtype calculations for public metrics.

### 5.2 pandas

Recommended status:

```text
required
```

Purpose:

- CSV and JSONL tabular ingestion,
- canonical normalization,
- joins between records and provenance,
- per-version grouping,
- coverage calculations,
- efficient handling near the v0.1 target scale.

Primary importing modules:

```text
io/loaders.py
io/normalization.py
io/validation.py
representations/field.py
metrics/provenance.py
```

Reasons to approve:

- reduces custom table and join logic,
- supports exact field-oriented audits,
- is understandable to research engineers,
- fits the intended 100,000-row metadata scale.

Restrictions:

- public metric semantics remain defined by project formulas,
- pandas defaults must not silently determine missingness meaning,
- categorical inference must not replace canonical enum validation,
- index behavior must remain internal,
- canonical identity remains `(dataset_version, record_id)`.

### 5.3 Required runtime dependency ceiling

Recommended v0.1 required runtime dependency count:

```text
no more than 2 direct third-party packages
```

The required baseline is therefore:

```text
NumPy
pandas
```

Adding another required runtime dependency requires a recorded architecture and dependency review.

---

## 6. Tier 2: optional runtime extras

Optional extras must remain isolated.

A user who installs the core package should still be able to run CSV and JSONL audits.

### 6.1 Parquet extra

Recommended extra name:

```text
parquet
```

Recommended dependency:

```text
PyArrow
```

Purpose:

- Parquet input,
- Parquet normalized export where implemented.

Import boundary:

```text
io/loaders.py
```

Required behavior when absent:

- CSV and JSONL continue to work,
- Parquet request produces a clear installation message,
- package import does not fail.

Recommended user message:

```text
Install the parquet extra to enable Parquet support.
```

### 6.2 HTML extra

Recommended status:

```text
no third-party runtime dependency required
```

The optional HTML report should initially use:

- standard-library HTML escaping,
- local template strings,
- self-contained CSS.

A template engine should not be added for v0.1 unless the standard-library implementation becomes materially harder to audit.

### 6.3 Embedding extra

Recommended v0.1 status:

```text
deferred
```

v0.1 may read user-provided clusters or vectors through existing NumPy or Parquet support.

It should not add:

- transformer library,
- remote embedding client,
- model download manager,
- GPU framework.

### 6.4 OpenLineage extra

Recommended v0.1 status:

```text
deferred
```

The internal schema should remain conceptually compatible.

A runtime adapter is not required.

### 6.5 ML Metadata extra

Recommended v0.1 status:

```text
deferred
```

### 6.6 Graph extra

Recommended v0.1 status:

```text
not required
```

A small custom adjacency representation should support:

- parent edges,
- cycle detection,
- root traversal,
- ancestor sets,
- coverage.

NetworkX should be reconsidered only if custom graph code becomes less auditable or substantially more error-prone.

### 6.7 Validation-model extra

Recommended v0.1 status:

```text
not required
```

Pydantic is not required for the first implementation.

Canonical types may use:

- dataclasses,
- enums,
- explicit validation functions.

Pydantic may be reconsidered if schema and serialization complexity materially increase.

---

## 7. Tier 3: development and validation dependencies

Development dependencies do not ship as required runtime dependencies.

### 7.1 Test runner

Recommended:

```text
pytest
```

Purpose:

- unit tests,
- integration tests,
- fixture management,
- parametrized exact cases.

### 7.2 Coverage

Recommended:

```text
pytest-cov
```

Purpose:

- code coverage visibility.

Coverage percentage does not replace traceability or behavioral tests.

### 7.3 Property testing

Recommended:

```text
Hypothesis
```

Purpose:

- distribution invariants,
- closure-bound properties,
- ancestry-share invariants,
- parser edge cases.

Property tests supplement hand-calculated cases.

### 7.4 JSON Schema validation

Recommended development dependency:

```text
jsonschema
```

Purpose:

- validate report JSON,
- validate configuration schemas,
- validate mapping schemas,
- validate normalized manifests.

Recommended status:

```text
development and CI dependency
```

Runtime report generation should not require JSON Schema validation unless explicitly enabled.

### 7.5 Linting and formatting

Recommended:

```text
Ruff
```

Purpose:

- lint,
- import rules,
- formatting,
- basic static checks.

Use one tool rather than multiple overlapping lint and formatting tools.

### 7.6 Type checking

Recommended:

```text
mypy
```

Status:

```text
development dependency
```

Type checking may begin with project-owned modules and expand gradually.

Third-party type gaps should not force unsafe casts into public calculations.

### 7.7 Package build

Recommended:

```text
build
```

Purpose:

- wheel,
- source distribution.

### 7.8 Package publication check

Recommended:

```text
twine
```

Purpose:

- validate distribution metadata before publication.

### 7.9 Dependency security audit

Recommended:

```text
pip-audit
```

Purpose:

- identify known dependency vulnerabilities during CI or release review.

A vulnerability report requires human interpretation.

### 7.10 Development dependency grouping

Recommended optional groups in `pyproject.toml`:

```text
test
lint
type
release
security
dev
```

A single `dev` group may aggregate them for contributor convenience.

---

## 8. Build backend

Recommended build backend:

```text
Hatchling
```

Purpose:

- standards-based package build,
- compact `pyproject.toml`,
- source-layout support,
- no runtime dependency.

Alternative:

```text
setuptools
```

### 8.1 Recommended choice

Use Hatchling unless Phase 1 package-build testing identifies a concrete compatibility problem.

### 8.2 Build isolation

Build dependencies belong under:

```text
[build-system]
```

They must not become runtime dependencies.

### 8.3 No framework lock-in

The build backend should remain replaceable without changing public analytical behavior.

---

## 9. Dependencies explicitly not selected for core v0.1

### 9.1 Typer and Click

Not selected initially.

Reason:

- `argparse` can support the small v0.1 CLI,
- avoids another required runtime dependency,
- CLI complexity is limited.

Reconsider when command structure becomes materially larger.

### 9.2 Rich

Not selected initially.

Reason:

- output correctness matters more than terminal styling,
- Markdown reports carry the human-readable result,
- avoids ANSI and cross-platform presentation complexity.

### 9.3 Pydantic

Not selected initially.

Reason:

- explicit dataclasses and validators remain auditable,
- avoids mixing model coercion with canonical validation semantics.

### 9.4 NetworkX

Not selected initially.

Reason:

- v0.1 lineage graph needs a narrow DAG feature set,
- custom functions can remain small and traceable.

Reconsider if custom implementation exceeds the approved complexity threshold.

### 9.5 SciPy

Not selected.

Reason:

- current formulas do not require SciPy,
- NumPy is sufficient.

### 9.6 scikit-learn

Not selected.

Reason:

- v0.1 does not train classifiers or create default semantic clusters,
- user-provided representations are sufficient.

### 9.7 PyTorch, TensorFlow, JAX

Not selected.

Reason:

- no model training,
- no GPU requirement,
- no embedded model,
- excessive dependency and attack surface.

### 9.8 Transformers and sentence-transformers

Not selected.

Reason:

- no model download,
- no embedded LLM or embedding model,
- representation must remain user-provided or deterministic.

### 9.9 FastAPI, Flask, Django, Streamlit, Gradio

Prohibited in core v0.1.

Reason:

- no web server,
- no hosted dashboard,
- local CLI is the approved interface.

### 9.10 SQLAlchemy and database drivers

Not selected.

Reason:

- no mandatory database backend,
- file-based sidecars are the approved v0.1 model.

### 9.11 Telemetry and analytics SDKs

Prohibited.

### 9.12 Plugin and dynamic-loading frameworks

Prohibited.

Reason:

- no plugin API,
- no remote execution,
- no hidden capability expansion.

---

## 10. Version policy

### 10.1 Library package principle

Recursive Integrity Toolkit is a library and CLI.

Its published runtime dependencies should use compatible version ranges rather than exact transitive pins.

### 10.2 Phase 1 version selection

Phase 1 should select exact lower bounds only after:

- supported Python matrix is confirmed,
- package installation succeeds,
- required APIs are verified,
- license review passes,
- security review passes.

### 10.3 Upper bounds

Avoid unnecessary upper bounds.

Use an upper bound only when:

- a known incompatible major release exists,
- public behavior cannot be preserved,
- test evidence justifies the constraint.

### 10.4 Exact environment recording

Release validation records exact installed versions.

### 10.5 No mandatory repository lockfile

Recommended v0.1 policy:

```text
no mandatory runtime lockfile in the source distribution
```

Reasons:

- library users need compatible dependency resolution,
- transitive pins can conflict with host environments,
- CI matrix testing provides broader compatibility evidence.

### 10.6 Development reproducibility

Contributors may use a local environment lock.

An official project lockfile may be added later through architecture review.

### 10.7 Minimum-version testing

CI should test:

- supported Python versions,
- selected minimum direct dependency versions,
- a current compatible dependency set.

### 10.8 Dependency update policy

Routine dependency updates require:

- CI,
- hero golden test,
- no-network test,
- license check,
- release note when user-visible.

---

## 11. Import boundaries

### 11.1 Core imports

Required runtime imports should remain localized.

### 11.2 Optional imports

Optional dependencies must use lazy or guarded imports.

Example behavior:

```text
Importing the package does not require PyArrow.
Requesting Parquet without PyArrow produces a clear error.
```

### 11.3 No dependency imports in root package

`__init__.py` should not import pandas, NumPy, or optional extras merely to expose the package version.

### 11.4 Report renderers

Report renderers should not import metric modules.

### 11.5 Dependency inversion

Internal data models should prevent pandas DataFrames from becoming the public API.

Pandas may be used internally.

Public analytical functions should prefer project-owned typed inputs and outputs where practical.

---

## 12. Numerical dependency rules

### 12.1 Random generator

Use:

```text
numpy.random.Generator
```

with explicit seed creation.

Do not use a hidden global random seed.

### 12.2 Floating values

Reject:

- NaN,
- positive infinity,
- negative infinity.

### 12.3 Public precision

Internal calculations retain full supported precision.

Report display precision is controlled by reporting specifications.

### 12.4 Determinism

Numerical operations used in golden tests should avoid platform-sensitive parallel reductions where practical.

### 12.5 BLAS variability

The mathematical core is small.

Implementation should avoid depending on nondeterministic parallel linear algebra.

---

## 13. pandas dependency rules

### 13.1 Canonical missingness

Pandas missing-value behavior must not define project semantics.

The project should normalize missingness explicitly.

### 13.2 Identity

Do not use a DataFrame row index as canonical record identity.

### 13.3 Joins

Joins must explicitly validate:

- one-to-one provenance relation,
- unmatched rows,
- duplicate keys,
- missing rows.

### 13.4 Type inference

Loader inference should be followed by canonical type validation.

### 13.5 String handling

Identifiers should use explicit string semantics.

### 13.6 Copy behavior

Avoid unnecessary whole-table copies.

Performance optimization must not mutate user inputs or change semantics.

---

## 14. Optional PyArrow rules

### 14.1 Isolation

Only Parquet-related code may require PyArrow.

### 14.2 Graceful absence

Core tests must pass without PyArrow.

### 14.3 Presence tests

The optional CI job should confirm:

- Parquet load,
- list-of-string parent field,
- timestamps,
- nullable values,
- schema conflict handling.

### 14.4 No remote filesystem requirement

PyArrow filesystem connectors are not part of approved v0.1 behavior.

---

## 15. Security rules for dependencies

Every direct dependency must be reviewed for:

- network behavior,
- telemetry,
- dynamic code execution,
- native extensions,
- parser attack surface,
- release maintenance,
- known vulnerabilities,
- transitive dependency size,
- license.

### 15.1 No automatic download

No dependency may automatically download:

- model,
- tokenizer,
- dataset,
- binary asset,
- remote schema.

### 15.2 No runtime plugin discovery

Dependencies must not load arbitrary user plugins.

### 15.3 Vulnerability review

A known vulnerability is evaluated by:

- affected code path,
- exploitability in v0.1,
- available fix,
- release timing.

Critical exploitable vulnerabilities block release.

### 15.4 Supply-chain review

Release should record:

- direct dependencies,
- exact release environment versions,
- third-party notices,
- security audit result.

---

## 16. Licensing rules for dependencies

### 16.1 Required compatibility

Direct dependencies must be compatible with the planned Apache-2.0 code distribution.

### 16.2 Third-party notices

Maintain:

```text
THIRD_PARTY_NOTICES.md
```

### 16.3 Unknown license

A dependency with unclear licensing must not be added.

### 16.4 Bundled data or models

A package that bundles data or models requires separate asset-license review.

### 16.5 Optional dependencies

Optional status does not remove license-review requirements.

---

## 17. Dependency proposal template

A proposed dependency must include:

```text
Package:
Tier:
Required or optional:
Exact purpose:
Importing modules:
Public behavior enabled:
Standard-library alternative:
Existing-dependency alternative:
Security behavior:
Network behavior:
Telemetry behavior:
Native-code behavior:
License:
Transitive dependency impact:
Platform support:
Testing plan:
Removal plan:
Decision required:
```

No dependency should be added from a code-generation suggestion alone.

---

## 18. Dependency acceptance criteria

A dependency may be approved when:

- purpose is concrete,
- no approved dependency already provides the function,
- standard-library alternative is materially worse,
- public behavior remains traceable,
- network behavior is acceptable,
- telemetry is absent,
- licensing is compatible,
- supported platforms have viable installation,
- tests cover presence and absence where optional,
- removal remains feasible.

---

## 19. Dependency rejection criteria

Reject a dependency when:

- it exists mainly for convenience,
- it downloads models,
- it requires an account,
- it starts a server,
- it adds telemetry,
- it executes user code,
- it obscures formulas,
- it duplicates an approved dependency,
- it has unclear licensing,
- it lacks supported-platform installation,
- it expands product scope,
- it creates a universal score or hidden inference layer.

---

## 20. Phase 1 `pyproject.toml` strategy

Phase 1 may create the package manifest.

Recommended conceptual structure:

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "recursive-integrity-toolkit"
requires-python = ">=3.11"
dependencies = [
  "numpy",
  "pandas",
]

[project.optional-dependencies]
parquet = [
  "pyarrow",
]
test = [
  "pytest",
  "pytest-cov",
  "hypothesis",
  "jsonschema",
]
lint = [
  "ruff",
]
type = [
  "mypy",
]
release = [
  "build",
  "twine",
]
security = [
  "pip-audit",
]
dev = [
  "pytest",
  "pytest-cov",
  "hypothesis",
  "jsonschema",
  "ruff",
  "mypy",
  "build",
  "twine",
  "pip-audit",
]

[project.scripts]
rit = "recursive_integrity_toolkit.cli:main"
recursive-integrity = "recursive_integrity_toolkit.cli:main"
```

The snippet is a structural template.

Exact version bounds must be chosen during Phase 1 dependency verification.

### 20.1 Optional HTML

Do not add an HTML dependency in the initial manifest.

### 20.2 Optional graph package

Do not add NetworkX in the initial manifest.

### 20.3 Optional validation model

Do not add Pydantic in the initial manifest.

---

## 21. Phase allocation

### Phase 0

Produces this strategy.

No dependency is installed or imported as implementation evidence.

### Phase 1

May:

- create `pyproject.toml`,
- verify package build,
- verify supported Python versions,
- justify each dependency,
- create import-safe stubs,
- configure development tools.

Must not implement algorithms.

### Phase 2

Activates:

- pandas ingestion and joins,
- standard-library mapping and validation,
- observability logic.

### Phase 3

Activates:

- NumPy numerical metrics and simulations,
- optional PyArrow input.

### Phase 4

Activates:

- JSON and Markdown output,
- standard-library HTML if implemented,
- packaging and CLI.

### Phase 5

Uses custom graph code unless a later approved dependency review changes the decision.

### Phase 6B

Uses NumPy random generation for simulations.

---

## 22. Testing strategy by dependency

### NumPy

Required tests:

- explicit seed determinism,
- finite-value checks,
- probability normalization,
- hand-calculated metric values,
- supported Python matrix.

### pandas

Required tests:

- canonical string IDs,
- duplicate-key detection,
- one-to-one joins,
- missingness normalization,
- CSV and JSONL parity,
- no semantic dependence on row index.

### PyArrow

Optional tests:

- absence message,
- valid Parquet load,
- parent-list round trip,
- timestamp behavior,
- schema conflict.

### pytest and Hypothesis

Development-only.

They must not become runtime imports.

### jsonschema

Development or validation-tooling only unless runtime schema validation is explicitly approved.

### Ruff and mypy

Development-only.

### pip-audit

Release tooling only.

It must not run during normal user audits.

---

## 23. Dependency isolation tests

Required tests:

```text
test_core_import_without_parquet_extra
test_csv_audit_without_parquet_extra
test_parquet_request_without_extra_has_clear_error
test_package_import_has_no_network_call
test_runtime_does_not_import_test_dependencies
test_runtime_does_not_import_release_dependencies
test_html_report_requires_no_remote_assets
test_no_dynamic_plugin_loading
```

---

## 24. Dependency performance review

Before adding a required dependency, review:

- import time,
- installed size,
- memory impact,
- runtime impact,
- compiled binary availability.

The dependency should not make the hero example exceed its target without clear justification.

---

## 25. Dependency-removal strategy

Each dependency should be replaceable.

### NumPy removal impact

High.

It owns core numerical behavior.

Replacement would require mathematical and performance review.

### pandas removal impact

Moderate to high.

Internal table adapters should reduce public API dependence.

### PyArrow removal impact

Low for core.

It disables optional Parquet support.

### Development-tool removal impact

Low for runtime.

A replacement must preserve equivalent validation evidence.

---

## 26. Dependency documentation

README should list:

- core dependencies,
- optional extras,
- install commands,
- no-network behavior,
- Parquet extra.

Recommended examples:

```bash
pip install recursive-integrity-toolkit
```

```bash
pip install "recursive-integrity-toolkit[parquet]"
```

```bash
pip install "recursive-integrity-toolkit[dev]"
```

Exact publication commands are added only after package release.

---

## 27. CI dependency matrix

Recommended jobs:

### Minimum environment

- supported minimum Python,
- approved minimum direct dependency versions.

### Current environment

- supported Python,
- current compatible dependency resolution.

### Optional Parquet

- core plus PyArrow.

### Security

- pip-audit,
- malicious input tests,
- no-network tests.

### Package build

- wheel and source distribution in clean environment.

---

## 28. Release dependency evidence

Official v0.1 should preserve:

- direct dependency list,
- exact release environment versions,
- build backend version,
- optional extras,
- security audit summary,
- license notice summary,
- supported Python matrix,
- package-install smoke results.

---

## 29. Dependency failure conditions

Release must stop if:

- required dependency lacks compatible licensing,
- required dependency makes a hidden network call,
- runtime imports a development-only dependency,
- optional dependency absence breaks core import,
- fixed-seed numerical output is unstable,
- a parser accepts executable configuration,
- a dependency silently downloads a model,
- a critical exploitable vulnerability remains,
- supported platforms cannot install the core package,
- the hero exceeds its performance target because of unjustified dependency overhead.

---

## 30. Phase 1 dependency acceptance checklist

Phase 1 passes when:

- [ ] Python baseline is recorded,
- [ ] build backend works,
- [ ] package imports in a clean environment,
- [ ] NumPy justification is documented,
- [ ] pandas justification is documented,
- [ ] PyArrow remains optional,
- [ ] test dependencies remain development-only,
- [ ] no web or model dependency exists,
- [ ] no graph framework is required,
- [ ] no runtime validation framework is required,
- [ ] optional-extra absence is tested,
- [ ] dependency licenses are reviewed,
- [ ] no hidden telemetry or network behavior is found,
- [ ] exact version bounds are recorded in `pyproject.toml`,
- [ ] CI matrix installs successfully,
- [ ] no algorithm implementation was added merely to test dependencies.

---

## 31. Decision dependencies

| Decision | Dependency effect |
|---|---|
| `UD-019` | Markdown required, no rich terminal dependency needed |
| `UD-020` | near-duplicate method remains optional |
| `UD-022` | OpenLineage and ML Metadata adapters deferred |
| `UD-023` | dependency license compatibility |
| `UD-025` | Python baseline and dependency ceiling |
| `UD-026` | package and CLI names |
| `UD-027` | CI matrix |
| `UD-036` | HTML optional |

---

## 32. Recommended v0.1 dependency baseline

### Required runtime

```text
Python 3.11 or later
NumPy
pandas
```

### Optional runtime

```text
PyArrow for Parquet
```

### Standard-library implementation

```text
argparse CLI
dataclasses and enums
JSON and TOML config
CSV and JSONL orchestration
logging
hashing
paths
offline HTML
custom narrow lineage graph
```

### Development and validation

```text
pytest
pytest-cov
Hypothesis
jsonschema
Ruff
mypy
build
twine
pip-audit
```

### Deferred or prohibited

```text
NetworkX
Pydantic
Typer
Click
Rich
SciPy
scikit-learn
PyTorch
TensorFlow
JAX
Transformers
sentence-transformers
FastAPI
Flask
Django
Streamlit
Gradio
SQLAlchemy
telemetry SDKs
plugin frameworks
```

A deferred dependency may be reconsidered through the formal proposal template.

---

## 33. Approval

### Theory Owner decision

- [ ] Approve dependency strategy baseline
- [ ] Approve with exceptions
- [ ] Return for revision

Exceptions:

```text

```

Theory Owner:

```text
Xiangyu Guo
```

Approval date:

```text

```

Approved status:

```text
PENDING
```

### Technical Maintainer acknowledgment

- [ ] Required runtime set is sufficient.
- [ ] Optional extras are isolated.
- [ ] Standard-library boundaries are practical.
- [ ] Build backend is acceptable.
- [ ] Version policy is implementable.
- [ ] Phase 1 can verify the baseline without writing algorithms.

Technical notes:

```text

```

Maintainer:

```text

```

Date:

```text

```

### Security Reviewer acknowledgment

- [ ] No dependency requires network access.
- [ ] No model downloader is present.
- [ ] No executable mapping framework is present.
- [ ] Optional extras do not weaken core privacy.
- [ ] Security audit tooling is appropriate.

Security notes:

```text

```

Reviewer:

```text

```

Date:

```text

```

### Mathematical Reviewer acknowledgment

- [ ] NumPy supports the approved mathematical core.
- [ ] Numerical behavior remains explicit and testable.
- [ ] No dependency hides formulas behind a black box.
- [ ] Graph metrics remain project-defined.

Reviewer notes:

```text

```

Reviewer:

```text

```

Date:

```text

```

---


## 34. Change-control rule

After approval:

1. a new required dependency requires architecture, security, license, and performance review,
2. a new optional dependency requires absence and presence tests,
3. a runtime dependency must not be added for development convenience,
4. a dependency must not introduce hidden network behavior,
5. a model or dataset downloader requires separate product approval,
6. a graph or validation framework must not redefine canonical semantics,
7. exact version changes require CI and hero validation,
8. a dependency vulnerability requires documented triage,
9. a dependency removal requires migration and compatibility review,
10. dependency count should remain as small as the product can reasonably sustain.
