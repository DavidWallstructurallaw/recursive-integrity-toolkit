# Recursive Integrity Toolkit

A local-first research toolkit for examining recursive closure exposure in synthetic-data and recursive-data pipelines under explicit representations and assumptions.

## Current milestone: Phase 6B installed scenario example

Development version `0.1.0.dev6` provides local input validation, JSON and Markdown audit reports, privacy controls, explicit pair and multi-version comparison, and packaged local examples. The mathematical core includes literal topic/label and exact record-form representations, exact duplicates, support/diversity, provenance composition, direct closure-exposure bounds, tail ranking and explicitly invoked closed and constant-source reopened scenarios.

`audit --longitudinal` compares ordered selected snapshots through adjacent pairs and an optional first-snapshot baseline. It reports observed distribution changes, provenance coverage/source changes and direct closure changes. Adding `--lineage` calculates every selected target from one shared supplied graph, including cycles, depth, external roots, concentration and lineage closure changes. JSON and Markdown use report schema **1.3**. `audit --simulate --config PATH` explicitly runs declared closed/reopened experiments, including a distinct closed expectation, transition events and per-path comparisons. A complete configuration with `simulation.enabled: true` also requests execution. `validate` checks the declarations without sampling. Step 6 adds an installed synthetic example and a [walkthrough of its assumptions and outputs](docs/simulation_example.md). See the [simulation contract](docs/simulation_contract.md) and [CLI options](docs/cli.md) for the complete interface. HTML output is deferred.

The [longitudinal contract](docs/longitudinal_contract.md) describes the accepted series behavior. The [Phase 6B candidate record](PHASE_6B_COMPLETION.md) identifies the dev6 verification status, supported matrix, installed delivery and actual performance observations. Earlier [Phase 6A results](PHASE_6A_COMPLETION.md) retain their named source and workloads. Candidate verification is in progress. No stable release, main merge or registry publication is implied by this development milestone.

## Install and run

Python 3.11 and 3.12 on Ubuntu and Windows form the supported candidate matrix. From a checkout:

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
rit example --longitudinal --lineage --out ./hero-series-workspace
rit example --dataset longitudinal --longitudinal --out ./three-version-workspace
rit example --dataset simulation --simulate --out ./simulation-workspace
```

Hero invocations copy six unchanged packaged files into the workspace's `inputs/`; the separate three-version example copies seven files, and the simulation example copies four. Each writes `reports/report.json` and `report.md` and downloads nothing. Each packaged `EXPECTED_OUTPUTS.md` contains the independent expectations. Add `--redacted` to protect identifiers and paths in the reports. Extracted inputs retain their original declarations.

The ordinary Hero reports compare v1 with v2: support **8 to 5**, retention **5/8**, diversity **7/8 to 3/4**, and missing topic states `battery`, `lizard`, `turtle`. Later-version human and synthetic shares are each **1/2**, and direct closure exposure is **[1/2, 1/2]**. Input observability is Level 4 and simulations are empty. Plain `example` keeps lineage `not_requested`. With `--lineage`, all eight v2 targets have resolved external ancestry, with **5** roots, ancestry HHI **1/4**, effective roots **4**, lineage exposure **[0, 0]**, and shared-ancestry evidence `present`.

Hero series mode retains those values in explicit snapshot/pair rows. With lineage requested, supporting roots change **8 to 5**, HHI **1/8 to 1/4** and effective roots **8 to 4**. The separate three-version example shows support **3 to 2 to 3**, including state `B` disappearing and reappearing. Series fields preserve the intermediate change. Neither example selects a tail rule or first baseline by default.

The simulation example compares closed and reopened sampling from declared fictional states `A` and `B`. Its initial distribution is `(1, 0)`, external input `(0, 1)`, reopening weight `1/4` and sample size `2`, with six transitions, three replicates and seed `17`. The first reopened source is `(3/4, 1/4)`; state `B` has a `7/16` chance of appearing in that next sample. Re-entry remains stochastic. Two separate audit records use states `X` and `Y`; they do not supply the scenario probabilities. This example requires `--simulate` and rejects `--lineage`, `--longitudinal` and a custom `--config`. Ordinary examples retain their existing behavior. The [simulation guide](docs/simulation_example.md) explains report fields, validation and explicit reruns with an edited local config.

Use the extracted files for these independent commands, each with a fresh output destination:

```bash
rit validate --records ./hero-workspace/inputs/records_v2.csv --out ./validation-report
rit audit --records ./hero-workspace/inputs/records_v2.csv --config ./hero-workspace/inputs/config.json --out ./topic-report
rit audit --records ./hero-workspace/inputs/records_v2.csv --lineage --lineage-records ./hero-workspace/inputs/records_v1.csv --provenance ./hero-workspace/inputs/provenance.csv --config ./hero-workspace/inputs/config.json --version-order ./hero-workspace/inputs/version_order.json --out ./lineage-report
rit audit --records ./hero-workspace/inputs/records_v2.csv --compare ./hero-workspace/inputs/records_v1.csv --provenance ./hero-workspace/inputs/provenance.csv --config ./hero-workspace/inputs/config.json --version-order ./hero-workspace/inputs/version_order.json --state-semantics "Hero topic labels retain their literal meaning across v1 and v2." --redacted --out ./private-pair-report
```

`validate` writes a validation report without calculating metrics; it accepts context files and rejects lineage execution. `audit` uses only an explicitly declared representation; missing representation or provenance produces specific unavailable results. `--lineage-records` may repeat and requires lineage opt-in for audit. Context versions must be disjoint from primary/comparison versions, and duplicate composite keys fail. Context alone does not request comparison. In a pair, `--compare` supplies the earlier version and `--records` the later version, with explicit chronology and shared state meaning. Reports are unweighted in this CLI. Existing report targets are never overwritten. Always check the exit code, since failed runs may retain useful partial reports.

For a series, repeat `--compare` and add `--longitudinal`. Each selected file must contain one distinct nonempty version, and `--records` must be latest. Supply chronology through config or a local order document; argument order and filenames do not establish series chronology. Add `--baseline first` for first-to-later comparisons alongside adjacent pairs. Common representation/meaning declarations or per-version declarations with directed pair mappings are supported through local config. `validate` accepts repeated comparisons and inert longitudinal config, including `enabled: true`, while executing no series calculations. Its report retains explicit `not_requested` series metadata.

Using the extracted three-version example, request all three adjacent/baseline comparisons with:

```bash
rit audit --records ./three-version-workspace/inputs/records_v3.jsonl \
  --compare ./three-version-workspace/inputs/records_v1.jsonl \
  --compare ./three-version-workspace/inputs/records_v2.jsonl \
  --config ./three-version-workspace/inputs/config.json \
  --provenance ./three-version-workspace/inputs/provenance.jsonl \
  --version-order ./three-version-workspace/inputs/version_order.json \
  --longitudinal --baseline first --out ./series-baseline-report
```

`recursive-integrity` and `python -m recursive_integrity_toolkit` provide the same commands. See [CLI options and exits](docs/cli.md), [data contracts](docs/data_schema.md), [report fields](docs/report_schema.md) and [privacy boundaries](docs/privacy.md).

Runtime requires no network connection, model, service, credential or database. Installation and CI acquire dependencies separately. All 41 package modules remain importable with numerical/optional dependencies and network access blocked; explicit calculation and Parquet operations load their required dependencies when used.

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

Series differences are later minus earlier, with separate endpoint scopes, coverage and denominators. Missing provenance is separate from the five declared source categories. Context may supply ancestors but never enters a selected snapshot's population. Disappearance means absence from the supplied later snapshot under the declared representation; reappearance remains visible and no permanent-extinction or causal-failure claim follows. Lineage uses one common supplied retrospective graph, so changes do not reconstruct what an auditor knew at each historical date.

The default selected-version limit is 100: at most 99 adjacent pairs or 197 adjacent/first-baseline pairs. Admission failure does not silently truncate the request. New series detail tables retain at most 100 rows and disclose exact total/omitted counts; full-report size can still grow with loaded records through ordinary sections. Shared lineage defaults are 200,000 nodes, 1,000,000 edges, 1,000,000 root memberships and 10,000,000 root-union visits. Exhaustion makes unfinished evidence unavailable, with independent valid results retained.

Standard reports exclude raw content, private notes, full embeddings and secrets. `--redacted` additionally protects paths and structural identifiers; record IDs default to keyed hashes, with explicit preserve/omit options. Aggregate values and errors remain visible. Input/configuration hashes are linkable, and pseudonyms provide no statistical anonymity. Exact content hashes describe record form and cannot establish semantic equivalence or authorship. Content references are read only through explicit Python `LOCAL_REF` requests; CLI audit/validate do not activate that reader.

[Phase 6A Step 8](PHASE_6A_STEP_8.md) measured complete longitudinal CLI publication with lineage at **11.46 seconds for 1,000 loaded records** and **124.65 seconds for 10,000** on its Linux/Python 3.12 reference container. The latter used **766,644,224 bytes peak process RSS**, producing **42,908,064 bytes JSON** and **26,943,450 bytes Markdown**. Both totals include 100 context anchors. All six final Hero series attempts, with and without lineage, took **0.94 to 1.11 seconds**. Their RSS counters inherited a parent-process high-water floor and cannot isolate Hero memory. These bounded observations do not replace the [candidate's actual 100k measurement](PHASE_6A_COMPLETION.md) or establish a new wall-time/memory SLA.

The Phase 4 Step 10 reference-container measurement completed the 100,000-record synthetic metadata audit in **1,362.4708 seconds**, with **7.12 GiB peak process RSS**, approximately **443 MB JSON** and **165 MB Markdown**. This is a demanding, verbose report workload; plan memory, disk space and runtime before applying it to large datasets. Those observations are neither an SLA nor evidence for lineage performance. Full-scale Python allocation tracing was omitted after a separately recorded bounded tracing-overhead measurement.

[Phase 5 Step 9](PHASE_5_STEP_9.md) measured an actual 100,000-record deep chain through loading, complete validation and ancestry API analysis in **123.36 seconds**, with **1.71 GiB peak RSS**. This excludes full audit reports and ordinary metrics, so it is not comparable to the Phase 4 workload. A separate 1,000-record lineage CLI audit through JSON/Markdown took **11.15 seconds**; lineage-enabled Hero runs took **0.99, 1.08 and 1.01 seconds**. See the [measurement method](tests/performance/README.md) for exact workloads, resource guards and limitations.

## Verification and development artifacts

Install development tools from the checkout with `python -m pip install ".[test,release]"`. Use focused tests for affected behavior and static/document checks for documentation changes. PR and release candidates run the canonical regression and required compatibility matrix; release checks also cover wheel/sdist, clean installed execution, Hero examples, reproducibility and security boundaries. [Release verification](docs/release_process.md) lists the commands and profiles.

Historical evidence remains recoverable from Git and archived phase records. Administrative successors do not automatically repeat a full matrix when executable and authoritative bytes are unchanged. New verification controls need a concrete undetected failure mode. Supported behavior, mathematical meaning, privacy and artifact integrity remain protected.

Source/code-adjacent configuration use Apache-2.0. Reusable documentation and repository-created examples use CC BY 4.0 under `LICENSING_NOTES.md` and `NOTICE`. Theory publications and dependencies retain separate licenses. Full theory PDFs and third-party source, models or datasets are not bundled. No universal collapse, integrity or entropy score, inferred provenance, hosted service, LLM integration, telemetry or policy enforcement is provided.
