# Recursive Integrity Toolkit

A local-first research toolkit for examining recursive closure exposure in synthetic-data and recursive-data pipelines under explicit representations and assumptions.

## Current milestone: Phase 5 lineage scale validation

Development version `0.1.0.dev3` provides local input validation, JSON and Markdown audit reports, privacy controls, one explicitly ordered dataset comparison and a packaged Hero example. The mathematical core includes literal topic/label and exact record-form representations, exact duplicates, support/diversity, provenance composition, direct closure-exposure bounds, tail ranking and explicitly invoked closed-resampling scenarios. Actual acceptance and execution evidence are recorded in `PHASE_4_COMPLETION.md`, `PHASE_4_VALIDATION_REPORT.md` and `PHASE_4_ARCHITECTURE_COMPLIANCE_REPORT.md`.

Phase 5 Steps 1-9 add validated graphs, cycles, depth, external ancestry, root concentration, lineage closure bounds and descriptive shared-root evidence through explicit Python calls or `audit --lineage` and `example --lineage`. Repeatable local context inputs supply ancestors while the primary version keeps its own metric scopes. JSON and Markdown use report schema 1.1. Bounded mutation checks and actual 100k lineage measurement are complete; Step 10 candidate verification remains pending. Longitudinal orchestration remains Phase 6A work; external reopening and experiment orchestration remain Phase 6B work. The CLI does not execute simulations. HTML output is deferred. No stable release, main merge or registry publication is implied by this development milestone.

## Install and run

Python 3.11 and 3.12 on Ubuntu and Windows form the verified environment matrix. From a checkout:

```bash
python -m pip install .
rit --help
rit version
```

For real Parquet input, install `".[parquet]"`. Direct dependency declarations remain `numpy>=2.0` and `pandas>=2.2`. The minimum jointly compatible profile uses NumPy 2.0.0 with pandas 2.2.2. See [release verification](docs/release_process.md) for environment coverage and its limits.

After installation, the following command works in any local working directory whose path is trusted and stable. Choose a workspace that does not already exist:

```bash
rit example --out ./hero-workspace
rit example --lineage --out ./hero-lineage-workspace
```

Each invocation copies six packaged Hero files into its workspace's `inputs/` and writes `reports/report.json` and `report.md`. It downloads nothing. The packaged `EXPECTED_OUTPUTS.md` contains the independently specified ordinary and lineage targets.

Both reports compare v1 with v2: support **8 to 5**, retention **5/8**, diversity **7/8 to 3/4**, and missing topic states `battery`, `lizard`, `turtle`. Later-version human and synthetic shares are each **1/2**, and direct closure exposure is **[1/2, 1/2]**. Input observability is Level 4 and simulations are empty. Plain `example` keeps lineage `not_requested`. With `--lineage`, all eight v2 targets have resolved external ancestry, with **5** roots, ancestry HHI **1/4**, effective roots **4**, lineage exposure **[0, 0]**, and shared-ancestry evidence `present`.

Use the extracted files for these independent commands, each with a fresh output destination:

```bash
rit validate --records ./hero-workspace/inputs/records_v2.csv --out ./validation-report
rit audit --records ./hero-workspace/inputs/records_v2.csv --config ./hero-workspace/inputs/config.json --out ./topic-report
rit audit --records ./hero-workspace/inputs/records_v2.csv --lineage --lineage-records ./hero-workspace/inputs/records_v1.csv --provenance ./hero-workspace/inputs/provenance.csv --config ./hero-workspace/inputs/config.json --version-order ./hero-workspace/inputs/version_order.json --out ./lineage-report
rit audit --records ./hero-workspace/inputs/records_v2.csv --compare ./hero-workspace/inputs/records_v1.csv --provenance ./hero-workspace/inputs/provenance.csv --config ./hero-workspace/inputs/config.json --version-order ./hero-workspace/inputs/version_order.json --state-semantics "Hero topic labels retain their literal meaning across v1 and v2." --redacted --out ./private-pair-report
```

`validate` writes a validation report without calculating metrics; it accepts context files and rejects lineage execution. `audit` uses only an explicitly declared representation; missing representation or provenance produces specific unavailable results. `--lineage-records` may repeat and requires lineage opt-in for audit. Context versions must be disjoint from primary/comparison versions, and duplicate composite keys fail. Context alone does not request comparison. In a pair, `--compare` supplies the earlier version and `--records` the later version, with explicit chronology and shared state meaning. Reports are unweighted in this CLI. Existing report targets are never overwritten. Always check the exit code, since failed runs may retain useful partial reports.

`recursive-integrity` and `python -m recursive_integrity_toolkit` provide the same commands. See [CLI options and exits](docs/cli.md), [data contracts](docs/data_schema.md), [report fields](docs/report_schema.md) and [privacy boundaries](docs/privacy.md).

Runtime requires no network connection, model, service, credential or database. Installation and CI acquire dependencies separately. All forty package modules remain importable with numerical/optional dependencies and network access blocked; explicit calculation and Parquet operations load their required dependencies when used.

## Python validation and calculation

After running the packaged example above, run these Python blocks in order from that same working directory:

```python
from pathlib import Path
from recursive_integrity_toolkit.io.validation import validate_bundle
from recursive_integrity_toolkit.models import AuditBundle, InputSource, FileRole

hero = (Path.cwd() / "hero-workspace" / "inputs").resolve()
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

`validate_bundle` stays input-only, including when a configuration declares an available capability or simulation. Explicitly calculate the v2 topic distribution:

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
assert distribution.support_size.value == 5
assert distribution.gini_simpson_diversity.value == 0.75
```

A mathematical scenario requires its own explicit parameters and call:

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

Both scenario outputs carry `simulation` evidence. Analytic expectations make no random draws. Sampled paths retain seed, NumPy version, state order, schedule and any approved roundoff correction. Repeatability is tested within a fixed environment; identical paths across future NumPy versions are not promised. These scenarios do not forecast production failure.

## Meaning, privacy and scale limits

Reports keep observed facts, derived metrics, proxy signals, simulations and unavailable conclusions separate. Each analytical envelope retains scope, denominator, representation where applicable, method, assumptions and limitations. An unavailable value is null with reasons; zero remains a measured value. Representation exclusions never erase records from provenance denominators.

Identity is `(dataset_version, record_id)`. Missing, null, declared unknown, zero and false remain distinct. Source type, grounding, human review and confidence are independent declarations. Direct exposure preserves unresolved evidence and validation errors. It does not certify provenance truth, independent ancestry or functional failure.

Standard reports exclude raw content, private notes, full embeddings and secrets. `--redacted` additionally protects paths and structural identifiers; record IDs default to keyed hashes, with explicit preserve/omit options. Aggregate values and errors remain visible. Input/configuration hashes are linkable, and pseudonyms provide no statistical anonymity. Exact content hashes describe record form and cannot establish semantic equivalence or authorship. Content references are read only through explicit Python `LOCAL_REF` requests; CLI audit/validate do not activate that reader.

The Phase 4 Step 10 reference-container measurement completed the 100,000-record synthetic metadata audit in **1,362.4708 seconds**, with **7.12 GiB peak process RSS**, approximately **443 MB JSON** and **165 MB Markdown**. This is a demanding, verbose report workload; plan memory, disk space and runtime before applying it to large datasets. Those observations are neither an SLA nor evidence for lineage performance. Full-scale Python allocation tracing was omitted after a separately recorded bounded tracing-overhead measurement.

[Phase 5 Step 9](PHASE_5_STEP_9.md) measured an actual 100,000-record deep chain through loading, complete validation and ancestry API analysis in **123.36 seconds**, with **1.71 GiB peak RSS**. This excludes full audit reports and ordinary metrics, so it is not comparable to the Phase 4 workload. A separate 1,000-record lineage CLI audit through JSON/Markdown took **11.15 seconds**; lineage-enabled Hero runs took **0.99, 1.08 and 1.01 seconds**. See the [measurement method](tests/performance/README.md) for exact workloads, resource guards and limitations.

## Verification and development artifacts

Install development tools from the checkout with `python -m pip install ".[test,release]"`. Use focused tests for affected behavior and static/document checks for documentation changes. PR and release candidates run the canonical regression and required compatibility matrix; release checks also cover wheel/sdist, clean installed execution, Hero examples, reproducibility and security boundaries. [Release verification](docs/release_process.md) lists the commands and profiles.

Historical evidence remains recoverable from Git and archived phase records. Administrative successors do not automatically repeat a full matrix when executable and authoritative bytes are unchanged. New verification controls need a concrete undetected failure mode. Supported behavior, mathematical meaning, privacy and artifact integrity remain protected.

Source/code-adjacent configuration use Apache-2.0. Reusable documentation and repository-created examples use CC BY 4.0 under `LICENSING_NOTES.md` and `NOTICE`. Theory publications and dependencies retain separate licenses. Full theory PDFs and third-party source, models or datasets are not bundled. No universal collapse, integrity or entropy score, inferred provenance, hosted service, LLM integration, telemetry or policy enforcement is provided.
