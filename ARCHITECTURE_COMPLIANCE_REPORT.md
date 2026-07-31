# ARCHITECTURE_COMPLIANCE_REPORT

## Document control

| Field | Value |
|---|---|
| Project | Recursive Integrity Toolkit |
| Release target | v0.1 |
| Phase | Phase 1: Repository Scaffold |
| Audit date | 2026-07-30 |
| Result | PASS |
| Scope | Repository, package, schemas, tests, hero fixture, CI scaffold, licensing, build, installation, import safety, and no-algorithm boundary |

## 1. Audit conclusion

The Phase 1 repository scaffold complies with the approved architecture and phase boundary.

The package builds, installs, imports safely, exposes only scaffold startup commands, contains all approved package modules, and contains no analytical implementation.

Phase 2 has not begun.

## 2. Repository structure

| Area | Required | Found | Result |
|---|---:|---:|---|
| Python package modules | 40 | 40 | PASS |
| JSON Schema files | 5 | 5 | PASS |
| Hero example files | 6 | 6 | PASS |
| GitHub workflow files | 4 | 4 | PASS |
| Public documentation files | 7 | 7 | PASS |
| Scaffold scripts | 5 | 5 | PASS |
| Python test files | approved scaffold and placeholders | 46 | PASS |

Required repository areas are present:

```text
src/recursive_integrity_toolkit/
schemas/
docs/
tests/
examples/hero/
scripts/
.github/workflows/
.github/ISSUE_TEMPLATE/
```

The final delivery archive excludes generated build caches, virtual environments, bytecode, pytest caches, and local execution logs.

## 3. Package ownership and import boundary

| Check | Actual result |
|---|---|
| Package modules with owner metadata | 40 of 40 |
| Package modules with current-phase metadata | 40 of 40 |
| Non-bootstrap modules | 37 docstring-only modules |
| Bootstrap modules | `__init__.py`, `__main__.py`, `cli.py` |
| Allowed functions found | `build_parser`, `main` |
| Other package functions found | 0 |
| Analytical third-party imports in package | 0 |
| Safe import with network blocked | PASS, 40 modules |
| Safe core import with PyArrow blocked | PASS |

No package import loads hero data, writes output, starts a service, contacts a network, or imports optional PyArrow.

## 4. No-algorithm audit

The package AST was inspected.

Results:

```text
non-bootstrap executable analytical bodies: 0
support calculation implementations: 0
diversity implementations: 0
tail implementations: 0
provenance metric implementations: 0
closure-bound implementations: 0
lineage graph implementations: 0
ancestry implementations: 0
simulation implementations: 0
analytical report assembly implementations: 0
universal score modules: 0
```

The following prohibited files are absent:

```text
collapse_score.py
integrity_score.py
universal_score.py
```

## 5. Prohibited architecture audit

The following directory names were searched recursively and were not found:

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

No background service, hosted application, remote model, database layer, telemetry layer, or plugin framework was created.

## 6. Schema audit

All five schema files:

- are legal JSON,
- parse successfully,
- declare JSON Schema Draft 2020-12,
- define a top-level object,
- set `additionalProperties` to `false`,
- remain structural placeholders,
- contain no analytical formula or cross-field calculation.

Result:

```text
5 parsed
0 failed
```

## 7. Hero fixture audit

The hero fixture contains exactly the six approved files.

Format checks confirmed:

- three CSV files parse,
- two JSON files parse,
- record and provenance headers match the approved specification,
- v1 parent arrays are empty,
- v2 parent references use `dataset_version::record_id`,
- version order is `v1`, then `v2`,
- representation is `topic`,
- `EXPECTED_OUTPUTS.md` contains the approved reference contract.

No approved analytical value was recalculated during Phase 1.

## 8. CI configuration audit

Workflow files:

```text
ci.yml
golden.yml
security.yml
release.yml
```

Local YAML parsing result:

```text
4 parsed
4 contained jobs
0 syntax failures
0 service blocks
permissions: contents read in all workflows
```

The workflows cover:

- Python 3.11 and 3.12 on Ubuntu and Windows for the main scaffold test,
- complete Phase 1 pytest execution,
- structural hero validation,
- no-network and optional-dependency tests,
- no-algorithm and prohibited-structure checks,
- wheel and source-distribution build,
- installed CLI verification.

The workflow configuration was parsed locally. GitHub-hosted jobs have not run because the repository has not yet been pushed to GitHub.

## 9. Build and installation audit

Local execution environment:

```text
Python 3.13.5
setuptools 82.0.1
```

Build results:

| Artifact | Size | SHA-256 |
|---|---:|---|
| `recursive_integrity_toolkit-0.1.0.dev1-py3-none-any.whl` | 30,247 bytes | `6c689dd738ae3729a900bb53c044197bd82b8b3d3ed6d30bace68345005b7c2b` |
| `recursive_integrity_toolkit-0.1.0.dev1.tar.gz` | 16,501 bytes | `fdd35565e605548bba59191b49c9a748254021089c84136a21efb250689a2440` |

Both builds completed with exit code 0.

The wheel was installed into a separate virtual environment with exit code 0.

Installed-package checks:

```text
package version: 0.1.0.dev1
license expression: Apache-2.0
rit --help: exit 0
rit version: exit 0
recursive-integrity version: exit 0
all installed modules imported with network blocked: 40
core import with PyArrow blocked: exit 0
```

## 10. Licensing audit

Required files are present and mutually consistent:

```text
LICENSE
NOTICE
LICENSING_NOTES.md
THEORY_SOURCES.md
THIRD_PARTY_NOTICES.md
```

The software license is Apache-2.0. Theory publications retain their stated licenses. Direct runtime, optional, development, and security-tool declarations are present.

## 11. Preservation audit

Baseline before Step 7:

```text
preexisting files: 144
missing preexisting files: 0
unauthorized modifications: 0
```

Five existing test files were deliberately updated because their Step 5 phase-boundary wording had become obsolete after the approved creation of `examples/hero/` and the final CI scaffold:

```text
tests/integration/test_prohibited_structure.py
tests/integration/test_repository_structure.py
tests/integration/test_hero_end_to_end.py
tests/integration/test_partial_lineage_report.py
tests/integration/test_partial_provenance_report.py
```

Other preexisting files remained unchanged.

## 12. Recorded deviations and limits

### Build backend

`DEPENDENCY_STRATEGY.md` recommended Hatchling. Step 2 adopted setuptools after the execution environment could not complete the initial isolated build path. The Theory Owner approved the Step 2 result, and this final scaffold retains setuptools 82.0.1.

This is an approved implementation deviation. It does not change runtime behavior or theory meaning.

### Local Python version

The final local execution ran on Python 3.13.5. The CI configuration covers the approved Python 3.11 and 3.12 matrix, but those hosted matrix jobs have not yet run.

### Analytical golden outputs

The hero reference values are present as approved text. Phase 1 does not generate or compare analytical reports.

## 13. Compliance result

```text
repository structure: PASS
package build: PASS
package installation: PASS
safe import: PASS
CLI startup: PASS
schema parsing: PASS
owner metadata: PASS
hero format: PASS
CI configuration parsing: PASS
license and notice consistency: PASS
no-network import: PASS
optional dependency isolation: PASS
no-algorithm boundary: PASS
prohibited architecture: PASS
Phase 2 implementation present: NO
```

Final result:

```text
PHASE 1 ARCHITECTURE COMPLIANCE: PASS
```
