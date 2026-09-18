# Recursive Integrity Toolkit

A local-first research toolkit for examining recursive closure exposure in synthetic-data and recursive-data pipelines under explicit representations and assumptions.

## Current milestone: Phase 3 mathematical core

Development version `0.1.0.dev2` includes validated local input, literal topic/label and exact record-form representations, exact duplicates, support/diversity, provenance composition, direct closure-exposure bounds, tail ranking, closed-resampling scenarios and explicit compatible-pair calculations. Final acceptance and actual execution evidence are recorded in `PHASE_3_COMPLETION.md`, `PHASE_3_VALIDATION_REPORT.md` and `PHASE_3_ARCHITECTURE_COMPLIANCE_REPORT.md`.

Calculations use explicit Python calls. `validate_bundle(...)` remains input-only, even with a simulation declaration or an available capability. The CLI offers help and version. Report generation and audit commands belong to Phase 4; general lineage/ancestry to Phase 5; longitudinal orchestration to Phase 6A; external reopening and experiment orchestration to Phase 6B.

## Install

Python 3.11 and 3.12 on Ubuntu and Windows form the verification matrix. From a checkout:

```bash
python -m pip install .
rit --help
rit version
```

For real Parquet input, install `".[parquet]"`. Direct dependency declarations remain `numpy>=2.0` and `pandas>=2.2`. The lowest jointly installable tested pair is NumPy 2.0.0 with pandas 2.2.2; pandas 2.2.0 requires NumPy below 2. See `docs/release_process.md` for the resolver evidence and test profiles.

Runtime requires no network connection, model, service, credential or database. Installation and CI acquire dependencies separately. All forty package modules can be imported while NumPy, pandas, PyArrow and network access are blocked; sampled resampling imports NumPy only when explicitly invoked.

## Validate and calculate the included Hero example

Run these Python examples in order from the checkout root after installation:

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
validated = validate_bundle(bundle)
assert validated.observability.maximum_level == 4
assert not validated.has_errors
```

That call performs input validation only. To calculate the declared v2 topic distribution, explicitly select the scope and representation:

```python
from recursive_integrity_toolkit.config import load_config
from recursive_integrity_toolkit.representations.field import assign_field_states
from recursive_integrity_toolkit.metrics.diversity import calculate_state_distribution

config = load_config(hero / "config.json")
represented = assign_field_states(
    validated.records,
    dataset_versions=("v2",),
    scope_id="hero-v2-topics",
    config=config.representation,
)
distribution = calculate_state_distribution(represented).unweighted
assert distribution.support_size.value == 3
assert distribution.gini_simpson_diversity.value == 0.625
```

A scenario needs its own explicit parameters and call:

```python
from recursive_integrity_toolkit.metrics.resampling import (
    expected_diversity_after_steps,
    simulate_closed_resampling,
)

probabilities = tuple((s.state_id, s.state_frequency) for s in distribution.states)
expected = expected_diversity_after_steps(
    probabilities, resample_size=8, steps=3,
    scope=distribution.scope, representation=distribution.representation,
)
sampled = simulate_closed_resampling(
    probabilities, resample_size=8, steps=3, seed=812, replicates=2,
    scope=distribution.scope, representation=distribution.representation,
)
assert expected.method == "analytic_expectation"
assert expected.random_seed is None
assert sampled.method == "sampled_path"
assert sampled.rng_name == "numpy.random.Generator(PCG64)"
```

Both scenario outputs have `simulation` evidence. Analytic expectations make no random draws. Sampled paths retain the seed, NumPy version, state order, schedule and any approved roundoff correction. Same-environment repeatability is tested; identical paths across future NumPy versions are not promised. These scenarios do not forecast production failure.

## Meaning and limits

Each calculation retains a named scope, denominator, representation where applicable, method, evidence class, assumptions and limitations. Unavailable values remain `None` with reasons; zero remains a measured value. Representation exclusions never erase records from provenance denominators.

Identity is `(dataset_version, record_id)`. Missing, null, declared unknown, zero and false remain distinct. Source type, grounding, human review and confidence are independent declarations. Missing provenance stays missing. Direct exposure uses declared open/closed/unresolved partitions and preserves validation errors; it does not certify provenance truth or ancestry.

Exact content hashes describe record form and remain linkable. They do not establish semantic equivalence or authorship. Explicit ordered-pair comparisons require compatible representations and chronology. A declared many-to-one map retains its direction, collapsed groups and original distributions. Full temporal analysis remains separately gated.

Content references are read only through explicit `LOCAL_REF` requests in the existing input layer. Calculation kernels operate on supplied memory. See `docs/privacy.md` for trusted-filesystem and internal-object limitations, `docs/data_schema.md` for call contracts, and `docs/theory_traceability.md` for field-to-definition/test mappings.

## Verification and development artifacts

```bash
python -m pip install ".[test,release]"
python -m pytest -p no:cacheprovider -q
python scripts/check_spec_consistency.py
python scripts/check_traceability.py
python scripts/release_check.py --phase 3 --step 11 --diff
python -m build
```

History-dependent stage checks require a full Git checkout. CI runs complete suites across both operating systems, both Python versions and both dependency profiles. A separate real-PyArrow job executes all three real-Parquet regressions. The four workflow roles cover complete CI, security boundaries, Hero/mathematical oracles and build/delivery. No active test is skipped or xfailed to pass a gate.

The full tracked-source archive, wheel and sdist have distinct scopes. The build workflow compares packaged module bytes, installs outside the checkout, runs separate import/input and numerical smoke checks, and retains logs/checksums. It creates no tag, registry publication or main merge. Performance measurements concern explicit calculation operations; full report-time performance and production validation remain later-stage work.

## Authority and licensing

The sixteen approved Phase 0 files, `PHASE_0_APPROVAL.md`, `PHASE_3_PLAN.md`, accepted Phase 2 records and frozen mathematical oracles retain their identities. `PHASE_3_DECISIONS.md` records adopted P3-D01 through P3-D10 and explicitly approved maintenance exceptions. Review roles are consolidated under the project governance allowance; no independent certification is claimed.

Source/code-adjacent configuration use Apache-2.0. Reusable documentation and repository-created examples use CC BY 4.0 under `LICENSING_NOTES.md` and `NOTICE`. Theory publications and dependencies retain separate licenses. Full theory PDFs and third-party source, models or datasets are not bundled. No universal collapse, integrity or entropy score, inferred provenance, hosted service, LLM integration, telemetry or policy enforcement is provided.
