# Recursive Integrity Toolkit

A local-first, theory-led research toolkit for examining recursive closure risk in synthetic-data and recursive-data pipelines.

## Current milestone: Phase 2 input validation

The Python input layer reads explicitly declared local inputs, applies safe declarative field mapping, normalizes canonical records, validates provenance and immediate dependencies, and classifies input observability. `validate_bundle(...)` combines those steps in one call and returns an internal, in-memory result.

**Analytical metrics, an audit CLI, report generation, general lineage analysis and simulations remain unimplemented.** An `available` capability describes input eligibility for a later analytical layer. It does not certify model quality, external truth, complete ancestry or deployment safety.

The package remains development build `0.1.0.dev1`. Actual milestone acceptance is recorded in `PHASE_2_COMPLETION.md`; no stable v0.1 release or package-registry publication is made. The optional recommended dev2 bump is deferred so Step 10 does not modify the protected package version constant merely for a label.

## Install and startup

Use Python 3.11 or 3.12 on Ubuntu or Windows for the tested matrix. From a checkout:

```bash
python -m pip install .
rit --help
rit version
```

The CLI still offers help and version only. Its historical scaffold wording does not expose an audit command. Phase 2 uses the Python interface. Parquet requires the optional extra:

```bash
python -m pip install ".[parquet]"
```

No model, service, database, credential or network connection is required for input validation. Installation and CI acquire dependencies separately from toolkit execution.

## Validate the included Hero bundle

Run from the repository root after installation:

```python
from pathlib import Path
from recursive_integrity_toolkit.io.validation import validate_bundle
from recursive_integrity_toolkit.models import AuditBundle, InputSource, FileRole

hero = (Path.cwd() / "examples" / "hero").resolve()
bundle = AuditBundle((
    InputSource(FileRole.RECORDS_PRIMARY, hero / "records_v1.csv"),
    InputSource(FileRole.RECORDS_COMPARE, hero / "records_v2.csv"),
    InputSource(FileRole.PROVENANCE_MANIFEST, hero / "provenance.csv"),
    InputSource(FileRole.CONFIG, hero / "config.json"),
    InputSource(FileRole.VERSION_ORDER, hero / "version_order.json"),
))
result = validate_bundle(bundle)
assert result.observability.maximum_level == 4
assert not result.has_errors
for family, capability in result.observability.capabilities.items():
    print(family.value, capability.status.value, capability.reason_codes)
```

This checks input qualification. It does not calculate the values in `examples/hero/EXPECTED_OUTPUTS.md`, which remains a future analytical contract and is never input data.

Inspect `has_errors` and retained validation messages independently of the maximum level. Valid dataset eligibility can coexist with unavailable lineage or failed content references. Fatal parsing, identity, unsafe mapping and invalid present fields remain exceptions.

## Implemented boundaries

Identity is `(dataset_version, record_id)`; parent references use `dataset_version::record_id`. Missing, null, literal unknown, zero and false stay distinct. Source type, external grounding and human review remain separate declarations.

Provenance row coverage, required-field coverage and known-grounding coverage retain separate numerators and a named denominator. No source-share or closure-bound metric is calculated. Chronology needs explicit evidence. Same-version parent edges defer general graph validation. Generation expectations use independently established dependencies, never the declared count itself.

Content references are read only by explicit request in `LOCAL_REF` mode. Containment and UTF-8 checks assume a trusted, stable directory. They are not an operating-system sandbox or universally race-proof containment. See `docs/privacy.md`.

## Validation and delivery

```bash
python -m pip install ".[test,release]"
python -m pytest -p no:cacheprovider -q
python scripts/check_spec_consistency.py
python scripts/check_traceability.py
python scripts/release_check.py
python -m build
```

CI runs the entire core suite on both operating systems and Python versions. A separate extra-enabled job runs the entire suite including the three real PyArrow tests. Independent Security and Hero-contract workflows remain. The build workflow verifies a fresh dependency-free wheel install, all forty module imports, CLI startup and Hero input validation. Its checksummed development archive contains tracked source, completion records and actual test evidence. It never publishes or merges.

The completion, validation and architecture reports state observed results and limitations. Synthetic regression tests do not establish production performance or independent security certification.

## Governing specifications and theory

Start with `PHASE_0_APPROVAL.md`, `PROJECT_INSTRUCTIONS.md`, `V0.1_PRODUCT_SPEC.md`, `REPOSITORY_ARCHITECTURE.md`, `DEPENDENCY_STRATEGY.md`, `THEORY_TO_CODE_TRACEABILITY.md` and `VALIDATION_PLAN.md`. The Phase 2 execution plan and narrow per-step exceptions were approved in the project conversation; this milestone does not rewrite the source specifications.

Theory sources are identified in `THEORY_SOURCES.md` and mapped in `THEORY_SOURCE_MAP.md`. Full theory PDFs are not redistributed. No universal collapse, integrity or entropy score, inferred provenance, hosted service, LLM integration, telemetry or policy enforcement is provided.

## Licensing

Source and code-adjacent configuration use Apache-2.0. Reusable specifications/documentation and repository-created examples use CC BY 4.0 as governed by `LICENSING_NOTES.md` and `NOTICE`. Theory publications and dependencies retain their separate licenses. This milestone bundles no third-party source, datasets, models or fonts.

Phase 2 establishes validated input observability. It does not produce recursive-integrity metrics. Phase 3 is not authorized by Phase 2 completion.
