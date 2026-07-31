# REPOSITORY_ARCHITECTURE

## Document control

| Field | Value |
|---|---|
| Project | Recursive Integrity Toolkit |
| Target release | v0.1 |
| Phase | Phase 0 |
| Status | APPROVED PHASE 0 BASELINE |
| Primary owner | Technical Maintainer |
| Theory owner | Xiangyu Guo |
| Reviewers | Theory Owner, Mathematical Reviewer, Security Reviewer |
| Depends on | `PROJECT_INSTRUCTIONS.md`, `V0.1_PRODUCT_SPEC.md`, `DEFINITIONS_AND_UNITS.md`, `DATA_AND_PROVENANCE_SPEC.md`, `OBSERVABILITY_AND_REPORTING.md`, `THEORY_TO_CODE_TRACEABILITY.md`, `VALIDATION_PLAN.md`, `PRIVACY_AND_DATA_HANDLING.md`, `LICENSING_NOTES.md`, `SUCCESS_CRITERIA.md`, `GOVERNANCE_AND_HANDOFF.md`, `UNRESOLVED_DECISIONS.md` |
| Purpose | Freeze the repository tree, module boundaries, ownership, data flow, dependency direction, phase allocation, test layout, and release artifacts |
| Implementation code authorized | No |

This file defines where every v0.1 responsibility belongs before implementation begins.

The repository must remain locally executable, auditable, phase-gated, and traceable from theory or product rule through code, tests, and reports.

---

## 1. Architectural objectives

The repository must provide:

- clear module ownership,
- one-way dependency flow,
- explicit input-to-report data flow,
- small single-purpose modules,
- representation-bound metrics,
- provenance-bound closure claims,
- graph validation before ancestry analysis,
- one canonical result object before rendering,
- local-first privacy,
- deterministic tests,
- a transferable handoff structure.

The architecture must avoid:

- a general scoring engine,
- hidden provenance inference,
- report renderers that recalculate metrics,
- mandatory web, cloud, database, model, or telemetry layers,
- Phase 2 through Phase 6 implementation during Phase 1.

---

## 2. Canonical repository tree

```text
recursive-integrity-toolkit/
├── README.md
├── LICENSE
├── NOTICE
├── pyproject.toml
├── CHANGELOG.md
├── CONTRIBUTING.md
├── SECURITY.md
├── CODE_OF_CONDUCT.md
├── MAINTAINERS.md
├── THEORY_SOURCES.md
├── THIRD_PARTY_NOTICES.md
├── PROJECT_INSTRUCTIONS.md
├── SPEC_AUDIT.md
├── THEORY_SOURCE_MAP.md
├── UNRESOLVED_DECISIONS.md
├── REPOSITORY_ARCHITECTURE.md
├── DEPENDENCY_STRATEGY.md
├── PHASE_0_APPROVAL.md
├── V0.1_PRODUCT_SPEC.md
├── DEFINITIONS_AND_UNITS.md
├── DATA_AND_PROVENANCE_SPEC.md
├── OBSERVABILITY_AND_REPORTING.md
├── THEORY_TO_CODE_TRACEABILITY.md
├── VALIDATION_PLAN.md
├── PRIVACY_AND_DATA_HANDLING.md
├── LICENSING_NOTES.md
├── SUCCESS_CRITERIA.md
├── GOVERNANCE_AND_HANDOFF.md
├── docs/
│   ├── architecture.md
│   ├── cli.md
│   ├── report_schema.md
│   ├── data_schema.md
│   ├── theory_traceability.md
│   ├── privacy.md
│   └── release_process.md
├── schemas/
│   ├── report.schema.json
│   ├── config.schema.json
│   ├── schema_mapping.schema.json
│   ├── version_order.schema.json
│   └── normalized_manifest.schema.json
├── src/
│   └── recursive_integrity_toolkit/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py
│       ├── config.py
│       ├── errors.py
│       ├── models.py
│       ├── result.py
│       ├── io/
│       │   ├── __init__.py
│       │   ├── loaders.py
│       │   ├── schema_mapping.py
│       │   ├── normalization.py
│       │   └── validation.py
│       ├── observability/
│       │   ├── __init__.py
│       │   └── levels.py
│       ├── representations/
│       │   ├── __init__.py
│       │   ├── base.py
│       │   ├── field.py
│       │   ├── content_hash.py
│       │   └── compatibility.py
│       ├── metrics/
│       │   ├── __init__.py
│       │   ├── duplicates.py
│       │   ├── diversity.py
│       │   ├── tail.py
│       │   ├── provenance.py
│       │   ├── bounds.py
│       │   └── resampling.py
│       ├── lineage/
│       │   ├── __init__.py
│       │   ├── graph.py
│       │   ├── cycles.py
│       │   └── ancestry.py
│       ├── reports/
│       │   ├── __init__.py
│       │   ├── assembly.py
│       │   ├── json_report.py
│       │   ├── markdown_report.py
│       │   └── html_report.py
│       └── utils/
│           ├── __init__.py
│           ├── hashing.py
│           ├── logging.py
│           ├── ordering.py
│           └── paths.py
├── tests/
│   ├── conftest.py
│   ├── fixtures/
│   │   ├── hero/
│   │   ├── minimal_valid/
│   │   ├── invalid_schema/
│   │   ├── provenance_partial/
│   │   ├── provenance_unknown/
│   │   ├── lineage_complete/
│   │   ├── lineage_multi_root/
│   │   ├── lineage_unresolved/
│   │   ├── lineage_ambiguous/
│   │   ├── lineage_cycles/
│   │   ├── version_order/
│   │   ├── representation_compatible/
│   │   ├── representation_incompatible/
│   │   ├── schema_mapping/
│   │   ├── content_references/
│   │   ├── weighted/
│   │   ├── resampling/
│   │   ├── reopening/
│   │   └── security/
│   ├── unit/
│   ├── integration/
│   ├── golden/
│   └── performance/
├── examples/
│   └── hero/
│       ├── records_v1.csv
│       ├── records_v2.csv
│       ├── provenance.csv
│       ├── version_order.json
│       ├── config.json
│       └── EXPECTED_OUTPUTS.md
├── scripts/
│   ├── check_spec_consistency.py
│   ├── check_traceability.py
│   ├── build_golden.py
│   ├── normalize_golden.py
│   └── release_check.py
└── .github/
    ├── workflows/
    │   ├── ci.yml
    │   ├── golden.yml
    │   ├── security.yml
    │   └── release.yml
    ├── ISSUE_TEMPLATE/
    └── pull_request_template.md
```

---

## 3. Root-file responsibilities

### `README.md`

Provides product introduction, quick start, hero command, current release status, limitations, specification links, and licensing summary.

### `LICENSE` and `NOTICE`

Carry the code license and required attribution notices.

### `pyproject.toml`

Defines package metadata, Python version, build backend, dependencies, optional extras, and CLI entrypoint.

### Governance files

`CONTRIBUTING.md`, `SECURITY.md`, `MAINTAINERS.md`, `CHANGELOG.md`, `THEORY_SOURCES.md`, and `THIRD_PARTY_NOTICES.md` support contribution, security, release history, theory versioning, and licensing.

### Phase 0 specifications

The controlling Markdown specifications remain in the repository root so reviewers can locate them without navigating an internal documentation hierarchy.

---

## 4. Documentation and schema directories

### `docs/`

Contains user-facing summaries of the approved contracts:

- architecture,
- CLI,
- data schema,
- report schema,
- theory traceability,
- privacy,
- release process.

These files summarize controlling root specifications. They must not redefine them.

### `schemas/`

Contains machine-readable JSON schemas for:

- reports,
- configuration,
- schema mapping,
- version order,
- normalized manifest export.

Schemas validate structure. Metric formulas remain in calculation modules and specifications.

---

## 5. Package-level modules

### `__init__.py`

Exposes package version and intentionally stable imports.

It must not read files, configure global logging, run analysis, or contact a network.

### `__main__.py`

Invokes the CLI entrypoint.

### `cli.py`

Owns command parsing, orchestration, exit codes, concise status, and output paths.

It must not own formulas, lineage algorithms, schema meaning, or evidence-class decisions.

### `config.py`

Owns configuration parsing, CLI and file merging, declared defaults, and stable configuration hashing.

It must not infer version order from filenames, choose a semantic representation silently, or activate simulations silently.

### `errors.py`

Owns canonical exceptions, warning and error codes, and conversion to safe user-visible records.

### `models.py`

Owns shared immutable or typed data structures such as records, provenance rows, record keys, edges, representations, and capability objects.

It must not contain metric formulas.

### `result.py`

Owns the canonical structured audit result matching the report sections.

Renderers consume this object rather than recalculating results.

---

## 6. I/O layer

The I/O layer converts physical files into canonical internal data.

### `io/loaders.py`

Owns CSV, JSONL, optional Parquet, UTF-8 handling, file inventory, and local content loading.

Trace ownership:

```text
PR-002
PR-017
```

### `io/schema_mapping.py`

Owns allowlisted declarative mapping operations and mapping audit records.

Trace ownership:

```text
PR-003
```

### `io/normalization.py`

Owns canonical field names, nulls, parent-list normalization, stable ordering, and composite record-key construction.

Trace ownership:

```text
PR-001
PR-008
```

### `io/validation.py`

Owns required fields, enum validation, uniqueness, joins, parent-reference validation, generation checks, version-order checks, and validation messages.

Trace ownership:

```text
PR-001
PR-004
PR-007
PR-008
PR-009
```

The I/O layer must not calculate diversity, closure bounds, ancestry HHI, or support deltas.

---

## 7. Observability layer

### `observability/levels.py`

Owns:

- maximum observability level,
- capability matrix,
- available, partial, unavailable, and experimental status,
- requirement and coverage reason codes.

Trace ownership:

```text
PR-010
PR-011
```

The layer decides eligibility. It does not calculate analytical metrics.

---

## 8. Representation layer

### `representations/base.py`

Defines the representation protocol and output contract.

### `representations/field.py`

Owns topic and label representations, missing-value policies, and explicit state mappings.

### `representations/content_hash.py`

Owns exact normalized record-form states.

Trace ownership:

```text
PR-006
```

### `representations/compatibility.py`

Owns representation-version compatibility and longitudinal mapping checks.

The representation layer assigns states. It does not calculate diversity or tail probabilities.

---

## 9. Metrics layer

Metric modules should prefer pure functions.

### `metrics/duplicates.py`

Owns exact duplicate groups and duplicate counts.

Owner:

```text
PR-006
```

### `metrics/diversity.py`

Owns state counts, frequencies, support, Gini-Simpson diversity, support comparison, and diversity deltas.

Owner:

```text
T1
```

### `metrics/tail.py`

Owns tail selection, rarity ranking, and one-step extinction scenario calculations.

Owner:

```text
T2
```

### `metrics/provenance.py`

Owns coverage, source counts, source shares, confidence counts, and direct grounding classes.

Owners:

```text
PR-004
PR-005
T3 input basis
```

### `metrics/bounds.py`

Owns direct and lineage closure intervals.

Owner:

```text
T3
```

### `metrics/resampling.py`

Owns closed-resampling simulation, expected contraction, extinction events, and experimental external reopening.

Owners:

```text
T1
T2
T5
```

Metric modules must not read files, render reports, infer provenance, mutate inputs, or create a universal score.

---

## 10. Lineage layer

### `lineage/graph.py`

Owns graph construction, parent resolution, node inventory, and edge inventory.

Owner:

```text
PR-008
```

### `lineage/cycles.py`

Owns cycle detection and graph-validity status.

Owner:

```text
T6
```

### `lineage/ancestry.py`

Owns roots, external roots, reachable root sets, ancestor incidence, fractional root mass, ancestry HHI, effective roots, and lineage coverage.

Owner:

```text
T4
```

The lineage layer must not infer semantic contribution, causal effect, content quality, or biological relation.

---

## 11. Reporting layer

### `reports/assembly.py`

Owns evidence-section assembly, unavailable conclusions, recommendations, and proxy construction from approved basis fields.

Owners:

```text
PR-012
PR-014
PR-018
```

### `reports/json_report.py`

Owns JSON serialization, report-schema validation, stable structure, and finite-number enforcement.

Owners:

```text
PR-013
PR-016
```

### `reports/markdown_report.py`

Owns section order, tables, numeric display, unavailable rendering, and limitations.

Owners:

```text
PR-013
PR-018
```

### `reports/html_report.py`

Optional offline renderer.

Renderers must not recalculate metrics, change evidence classes, fill unavailable values, or convert intervals into point estimates.

---

## 12. Utility layer

### `utils/hashing.py`

File hashes, content hashes, and redacted identifier hashes.

### `utils/logging.py`

Content-safe logging and privacy-mode handling.

### `utils/ordering.py`

Stable deterministic ordering and tie-breaking.

### `utils/paths.py`

Local path resolution, base-directory enforcement, symlink safety, and path redaction.

Utilities should remain free of theory interpretation.

---

## 13. Canonical run flow

```text
CLI arguments
-> resolved configuration
-> file inventory and loading
-> declarative schema mapping
-> canonical normalization
-> validation and joins
-> representation assignment
-> observability classification
-> eligible metrics
-> eligible lineage analysis
-> eligible longitudinal comparison
-> optional explicit simulation
-> canonical result assembly
-> redaction
-> JSON and Markdown rendering
```

A family-specific failure should block the affected capability while preserving valid unrelated results when a partial report remains safe.

A fatal input failure should produce a sanitized error result and no unsupported metrics.

---

## 14. Dependency direction

Intended direction:

```text
utils
^
models and errors
^
io and representations
^
observability
^
metrics and lineage
^
result assembly
^
report renderers
^
cli
```

Forbidden reverse dependencies include:

- metrics importing report renderers,
- loaders importing metrics,
- utilities importing CLI,
- ancestry importing report serializers.

Circular imports are prohibited.

Shared data types belong in `models.py`, `result.py`, and `errors.py`.

---

## 15. Phase allocation

### Phase 0

Specifications, architecture, dependency strategy, and approval records only.

### Phase 1

Repository tree, package metadata, empty modules, docstrings, schema placeholders, test skeletons, hero files, license files, and CI skeleton.

No algorithms.

### Phase 2

Primary paths:

```text
io/
observability/
config.py
errors.py
models.py
utils/paths.py
```

### Phase 3

Primary paths:

```text
representations/
metrics/
```

### Phase 4

Primary paths:

```text
result.py
reports/
cli.py
utils/logging.py
utils/hashing.py
```

### Phase 5

Primary paths:

```text
lineage/
```

### Phase 6A

Longitudinal extensions in approved metrics, lineage, and report assembly.

### Phase 6B

Experimental resampling and reopening extensions.

---

## 16. Phase 1 scaffold rules

Allowed:

- module docstrings,
- type placeholders,
- import-safe stubs,
- package metadata,
- test placeholders,
- fixtures,
- CI structure.

Forbidden:

- support calculation,
- diversity formula,
- closure bounds,
- ancestry HHI,
- simulation algorithms,
- report metric assembly,
- hidden thresholds,
- inferred provenance.

Phase 1 should not publicly expose later-phase functions.

---

## 17. Testing architecture

### Unit tests

Verify one module, formula, or product rule.

### Integration tests

Verify complete workflows and partial capability behavior.

### Golden tests

Protect public JSON and Markdown contracts.

### Performance tests

Protect declared local runtime and scale.

### Security tests

Protect mapping, path, no-network, logging, and redaction behavior.

Test files must use `T*` or `PR-*` ownership in their names.

No test requires a remote download.

---

## 18. Hero architecture

Canonical files:

```text
examples/hero/records_v1.csv
examples/hero/records_v2.csv
examples/hero/provenance.csv
examples/hero/version_order.json
examples/hero/config.json
examples/hero/EXPECTED_OUTPUTS.md
```

Golden reports belong under `tests/golden/`.

One canonical hero fixture should be reused by README, CLI docs, integration tests, and release checks.

Hero changes require decision, validation, and golden review.

---

## 19. CI architecture

### `ci.yml`

Runs specification lint, unit tests, integration tests, package build, and hero smoke.

### `golden.yml`

Runs normalized JSON and Markdown comparison plus forbidden-language checks.

### `security.yml`

Runs mapping, path, no-network, logging, and redaction tests.

### `release.yml`

Runs package build, validation summary, license checks, and release-artifact checks.

Recommended initial matrix:

- Ubuntu,
- Windows,
- Python 3.11,
- Python 3.12.

Core CI should not require secrets.

---

## 20. Script architecture

### `check_spec_consistency.py`

Checks required files, canonical names, IDs, and decision status.

### `check_traceability.py`

Checks public-field ownership, tests, deferred-field absence, and forbidden-field absence.

### `build_golden.py`

May generate candidate outputs during development.

It does not define correctness.

### `normalize_golden.py`

Removes variable run metadata before comparison.

### `release_check.py`

Aggregates test, traceability, licensing, approval, and hero status.

---

## 21. Privacy and security architecture

Privacy behavior is distributed across loaders, paths, logging, result assembly, and renderers.

A single resolved privacy-mode object should control standard, redacted, and debug behavior.

Core v0.1 contains:

- no HTTP client,
- no remote fetch layer,
- no executable schema language,
- no global persistent content cache,
- no server,
- no telemetry.

All local references pass through `utils/paths.py`.

Redaction occurs after calculation.

Raw content should not enter the canonical result object by default.

---

## 22. Licensing architecture

Required root files:

```text
LICENSE
NOTICE
LICENSING_NOTES.md
```

Recommended asset classes:

- Python code: Apache-2.0
- specifications and reusable docs: CC BY 4.0
- repository-created examples: CC BY 4.0
- theory sources: existing theory license
- third-party files: original license

The public repository should contain theory citations and a source manifest. Full theory PDFs remain outside the public repository by default.

---

## 23. Extension boundaries

Deferred future locations may include:

```text
adapters/openlineage.py
adapters/ml_metadata.py
amplification/
representations/providers/
```

These directories must not appear in core v0.1 without approved scope changes.

No v0.1 directories should be created for:

```text
server
webapp
cloud
telemetry
plugins
agents
llm
auth
database
policy_enforcement
```

Files such as `collapse_score.py`, `integrity_score.py`, or `universal_score.py` are prohibited.

---

## 24. Architecture risks and controls

| Risk | Control |
|---|---|
| oversized central module | small ownership boundaries |
| renderer recalculates values | canonical result object |
| hidden inference in validation | declarative mapping and unknown tests |
| ancestry becomes workflow engine | record-ancestry scope |
| optional dependency becomes mandatory | extras and absence tests |
| theory terms drift | Theory Map and Trace IDs |
| Phase 1 writes algorithms | scaffold acceptance review |
| reverse dependencies | import and architecture checks |
| private data enters fixtures | fixture governance and review |

---

## 25. Architecture acceptance tests

Verify:

- required paths exist,
- prohibited paths do not exist,
- package imports without side effects,
- CLI help and version import,
- no network call occurs at import,
- no circular imports exist,
- optional dependencies remain isolated,
- module headers contain owners,
- public fields have owners,
- deferred modules are absent,
- no Phase 1 formula implementation exists.

Recommended output:

```text
architecture_compliance_report.json
```

---

## 26. Phase 1 acceptance checklist

Phase 1 passes when:

- [ ] root files exist,
- [ ] source tree matches this file,
- [ ] test and fixture trees exist,
- [ ] hero files exist,
- [ ] module docstrings identify ownership,
- [ ] package imports,
- [ ] CLI skeleton supports help and version,
- [ ] schemas exist as placeholders or approved initial contracts,
- [ ] CI skeleton exists,
- [ ] license files exist,
- [ ] dependency strategy exists,
- [ ] no analytical algorithm exists,
- [ ] no hidden network dependency exists,
- [ ] no prohibited directory exists,
- [ ] no public metric is emitted.

---

## 27. Decision dependencies

| Decision | Architectural effect |
|---|---|
| `UD-001` | authority model |
| `UD-002` | primary ML domain |
| `UD-004` | capability matrix |
| `UD-006` | composite identity and parent encoding |
| `UD-017` | Phase 6 split |
| `UD-019` | Markdown required |
| `UD-022` | adapters deferred |
| `UD-023` | license split |
| `UD-024` | theory-PDF policy |
| `UD-025` | Python and dependency baseline |
| `UD-026` | repository, package, and CLI names |
| `UD-027` | CI matrix |
| `UD-032` | release labels |
| `UD-036` | optional HTML |

---

## 28. Approval

### Theory Owner decision

- [ ] Approve repository architecture baseline
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

- [ ] Tree is implementable.
- [ ] Module boundaries are clear.
- [ ] Dependency direction is enforceable.
- [ ] Phase allocation is practical.
- [ ] Test layout supports traceability.
- [ ] Phase 1 can remain algorithm-free.

Technical notes:

```text

```

Maintainer:

```text

```

Date:

```text

```

### Mathematical Reviewer acknowledgment

- [ ] Mathematical modules have clear ownership.
- [ ] Renderers cannot own calculations.
- [ ] Theory-derived and operational metrics remain separated.

Reviewer notes:

```text

```

Reviewer:

```text

```

Date:

```text

```

### Security Reviewer acknowledgment

- [ ] No network layer exists in core architecture.
- [ ] Mapping remains non-executable.
- [ ] Path handling is centralized.
- [ ] Redaction and logging remain separate from metrics.
- [ ] Optional HTML remains local.

Security notes:

```text

```

Reviewer:

```text

```

Date:

```text

```

---

## 29. Change-control rule

After approval:

1. a new top-level directory requires architecture review,
2. a public calculation requires one primary module owner,
3. report renderers must not gain metric ownership,
4. I/O modules must not infer provenance,
5. optional dependencies must remain isolated,
6. network behavior requires security and product approval,
7. deferred branches must not enter core v0.1,
8. a module move requires traceability and test updates,
9. public-field ownership must remain stable,
10. Phase 1 scaffolding must remain free of analytical algorithms.
