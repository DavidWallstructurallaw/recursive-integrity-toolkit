# Recursive Integrity Toolkit

**Audit synthetic training data for missing categories, provenance gaps, and concentrated ancestry.**

Recursive Integrity Toolkit is a local Python CLI for **synthetic data auditing**,
**dataset diversity**, and **training data provenance**. Compare dataset snapshots
after generation, filtering, or reuse. See which declared topics or labels remain,
where source records are missing, and how supplied parent links concentrate around
shared roots. Export inspectable **JSON and Markdown reports** from CSV, JSONL,
or optional Parquet files.

Runtime works offline with no API key, model download, telemetry, or data upload.
Version **0.1.0** is available through [GitHub Releases](https://github.com/DavidWallstructurallaw/recursive-integrity-toolkit/releases/tag/v0.1.0).
See the [validation and release record](RELEASE_0_1_0.md). Install from the release
files or the tagged source below; no package-registry publication is claimed.

[Quick start](#quick-start) · [Your data](#audit-your-own-data) ·
[Examples and Python API](docs/getting_started.md) · [CLI reference](docs/cli.md)

## What can I check?

| Your question | What the report shows |
| --- | --- |
| Did filtering or another generation round remove categories? | Topic/label support, frequencies, diversity, and states lost or regained across explicitly ordered versions. |
| Are rare categories disappearing? | Declared-tail counts and version comparisons under a compatible representation. |
| How much of this dataset has recorded provenance? | Matching-row coverage, declared source-type shares, unknown grounding, and missing evidence. |
| Do many records trace back to a few shared ancestors? | Supplied lineage coverage, external roots, ancestry concentration and unresolved ancestry. |
| What happens in a closed or externally reopened sampling scenario? | Explicit categorical simulations with seeds, assumptions, trajectories and separate analytic expectations. |

Use it between dataset preparation steps, before another training round, or when
reviewing a dataset handoff. You supply the labels, provenance and parent links;
the report makes their coverage and limits visible.

## Quick start

Use Python **3.11 or 3.12** on Linux or Windows. Install the tagged release
from source, preferably in a virtual environment:

```bash
git clone --branch v0.1.0 https://github.com/DavidWallstructurallaw/recursive-integrity-toolkit.git
cd recursive-integrity-toolkit
python -m pip install .
rit example --lineage --out ./rit-demo
```

Open `rit-demo/reports/report.md` to read the result, or
`rit-demo/reports/report.json` for structured output. The example creates its own
tiny inputs locally. Choose a new workspace path on each run.

The included two-version example produces:

| Check | Earlier dataset | Later dataset |
| --- | ---: | ---: |
| Topic categories present | 8 | 5 |
| Gini-Simpson diversity | 0.875 | 0.750 |

The report names the three missing topics: `battery`, `lizard`, and `turtle`.
The later dataset's eight records have five declared external roots and ancestry
HHI `0.25`. These are inspectable results from the supplied example, with
[independent expected values](examples/hero/EXPECTED_OUTPUTS.md).

## Choose your next workflow

After installation, run any example into a new local workspace:

| Goal | Command | What to inspect |
| --- | --- | --- |
| Compare three dataset versions | `rit example --dataset longitudinal --longitudinal --out ./version-demo` | Topic support changes `3 → 2 → 3`; state `B` disappears and reappears. |
| Compare supplied ancestry across versions | `rit example --longitudinal --lineage --out ./ancestry-demo` | Root counts, concentration, coverage and per-pair changes. |
| Explore external input in a sampling model | `rit example --dataset simulation --simulate --out ./sampling-demo` | Closed/reopened trajectories under explicitly declared fictional probabilities. |

Each workspace contains `inputs/`, `reports/report.md`, and `reports/report.json`.
See the [full walkthrough](docs/getting_started.md),
[version-comparison guide](docs/longitudinal_contract.md), or
[simulation guide](docs/simulation_example.md).

## Audit your own data

Start with the demo's [records CSV](examples/hero/records_v2.csv) and
[representation config](examples/hero/config.json). Records use
`dataset_version`, `record_id`, and `content`; add `topic` or `label` for
categorical analysis and declare that field's meaning in the config. Adapt the
example to your data while keeping IDs unique within each version.

For a single dataset version saved as `records.csv` with `config.json`:

```bash
rit validate --records ./records.csv --out ./validation-report
rit audit --records ./records.csv --config ./config.json --out ./audit-report
```

The audit can calculate declared category coverage without provenance. A matching
provenance manifest unlocks source-type and grounding results; supplied parent
records and links unlock lineage analysis. See [input fields and mapping](docs/data_schema.md)
and the [complete own-data commands](docs/getting_started.md#install-and-run).
Always check the exit code and reported errors. Existing report files are protected
against overwrite.

For Parquet, install `python -m pip install ".[parquet]"` from the checkout.
For reports with protected identifiers and paths, add `--redacted`; review the
[privacy limits](docs/privacy.md) before sharing. The Python API and the
`recursive-integrity` console alias are also available.

## Fit and interpretation

**Diversity** is measured within your declared topic, label, or exact record-form
representation. Exact duplicate diagnostics use an explicit content-hash
representation. Semantic similarity, paraphrase detection and automatic topic
labeling require separate tools.

**Provenance and lineage** describe your supplied declarations. Missing ancestry
stays unresolved. Human/synthetic labels do not by themselves establish external
grounding, source truth, or independence.

**Studying model collapse?** Use the toolkit to document category loss, diversity
changes, provenance gaps and shared ancestry between dataset generations, or to
explore its bounded sampling models. Model-quality evaluation and empirical
failure evidence remain separate requirements; these reports provide no universal
collapse prediction or integrity score. Simulation results remain experimental.

Reports separate observed facts, derived metrics, proxy signals, simulations and
unavailable conclusions. See the [report field reference](docs/report_schema.md)
for definitions, denominators and limitations. Complete 100,000-record reports
can take minutes and several GB of memory; [measured workloads](RELEASE_0_1_0.md)
record exact environments and output sizes. Start with a small export.

## Documentation and verification

- [Examples, Python API and detailed limits](docs/getting_started.md)
- [CLI options and exit codes](docs/cli.md)
- [Data schema](docs/data_schema.md) and [report schema 1.3](docs/report_schema.md)
- [Theory-to-code guide](docs/theory_traceability.md) and [theory sources](THEORY_SOURCES.md)
- [Release preparation and validation](RELEASE_0_1_0.md)
- [Development verification](docs/release_process.md), [security](SECURITY.md), and [maintainers](MAINTAINERS.md)

Code and code-adjacent configuration use **Apache-2.0**. Reusable documentation
and repository-created examples use **CC BY 4.0** under
[LICENSING_NOTES.md](LICENSING_NOTES.md) and [NOTICE](NOTICE). Theory publications
and dependencies retain their own licenses; full theory PDFs are not bundled.
