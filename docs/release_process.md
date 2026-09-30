# Development and Release Verification

## Current Phase 6B implementation boundary

Phase 6B Step 4 integrates explicit experiment reports in schema 1.3 while the
package remains `0.1.0.dev5`. Current focused evidence is recorded in
[the Step 4 record](../PHASE_6B_STEP_4.md). The dev6 candidate, supported matrix
and installed simulation example checks belong to later planned steps.

## Accepted Phase 6A candidate boundary

Phase 6A Step 9 verifies development version `0.1.0.dev5`, with executable
report schema 1.2 for every report. Ordered series selection, distribution,
provenance and closure changes, selected lineage, CLI/configuration and bounded
adversarial/preflight checks are implemented. Candidate status, exact source,
actual jobs, measurement attempts and delivery limits are recorded in
[Phase 6A completion](../PHASE_6A_COMPLETION.md).
Stable v0.1 publication, a tag and main merge require
separate authorization.

Use one current verification path:

```bash
python scripts/check_spec_consistency.py
python scripts/check_traceability.py
python scripts/release_check.py
```

Historical `--phase` and `--step` dispatch is retired. Earlier source forms,
migrations and receipts remain recoverable from Git and archived phase records.
The existing source check uses accepted Phase 6B Step 3 commit
`2e0805dba85754d78854750f692ac02ddaf44a8a`. Step 4 permits only `result.py`,
the report assembly and Markdown owners, and the canonical/packaged report
schema pair. It protects the numerical kernels and all other product files.
It retains the exact product file inventory and
rejects unrelated runtime, package-metadata and canonical Hero changes.
The frozen Phase 0 specification hashes are unchanged. Sixteen frozen
specifications, 41 package modules and fourteen packaged resource copies remain
protected. The source
inventory excludes only the generated `src/recursive_integrity_toolkit.egg-info/`
metadata directory; similarly named or nested paths are not excluded, and
symlink rejection and shipped-package inventory checks remain in force.

## Risk-sensitive gates

Ordinary PR checks use the focused job for the active step. Documentation-only
changes require formatting and affected consistency checks. As implementation
scope changes, update the focused selection to affected owners and dependency
neighbors. It does not establish candidate acceptance.

Dispatch `ci.yml` with `gate=candidate` for a stable candidate. When the default
branch does not yet contain the dispatch-capable workflow, add the
`verification:candidate` label to its PR to select the same jobs. Only that label
event selects the matrix; subsequent commits use the ordinary affected gate.
Remove and re-add the label to select a changed candidate. A label is a scheduling
choice and does not grant source authority, merge permission or release approval.
The workflow runs:

| Role | Required execution |
|---|---|
| Core | Ubuntu/Windows, Python 3.11/3.12, current/minimum compatible dependencies; PyArrow absent |
| Optional Parquet | Ubuntu/Python 3.12, real PyArrow with roundtrip, row-limit, invalid-file, context-input, longitudinal CLI and installed privacy regressions |
| Canonical Hero and mathematics | Frozen mathematical cases, report goldens and packaged Hero behavior |
| Security | No-network, input/path, privacy/redaction and output-publication boundaries |
| Reference performance | One Ubuntu/Python 3.12 profile, including required actual 100k workloads |
| Package/delivery | Wheel/sdist integrity, clean installed execution, reproducibility and tracked-source archive |

Compatibility cells run complete canonical regression with
`--ignore=tests/performance`. The designated Ubuntu/Python 3.12 performance job
runs the actual 100k longitudinal case in its own pytest process, then runs
the remaining `tests/performance` cases once. Each invocation has a separate
JUnit and retained temporary directory. This prevents a prior large workload's
pytest-parent high-water mark from setting the longitudinal child's RSS floor.
Every existing performance case remains selected exactly once; the expensive
workloads are not repeated across compatibility cells. The job timeout is
75 minutes. The sparse-lineage benchmark executes a real 100k reverse chain
through file loading, complete input/generation validation and ancestry analysis.
Separate bounded deep-chain and high-fan-in cases measure the full lineage CLI
through JSON/Markdown. Longitudinal measurements cover three-version workloads,
a 20-version/37-pair workload and the canonical Hero with and without lineage.
The full series case loads 100,000 total records: 100 context anchors and three
selected populations of 33,300. All three pairs and complete JSON/Markdown
publication are measured, with unchanged default lineage guards. Its practical
1,800-second subprocess timeout is an operational guard, not an approved SLA.

The reference job uses these separate selections, retaining both XML files and
attempt directories in its performance artifact:

```bash
python -m pytest -q tests/performance/test_longitudinal_runtime.py::test_longitudinal_100k_complete_reports \
  --basetemp=/absolute/evidence/longitudinal-100k-attempts \
  --junitxml=/absolute/evidence/longitudinal-100k.xml
python -m pytest -q tests/performance -k 'not test_longitudinal_100k_complete_reports' \
  --basetemp=/absolute/evidence/performance-attempts \
  --junitxml=/absolute/evidence/performance.xml
```

The existing minimum compatible pair remains NumPy 2.0.0/pandas 2.2.2. Record
actual resolved dependencies, `pip check`, Python/platform, commands, results
and material limitations. A skipped, failed, duplicate or uncollected required
test cannot stand in for a passing result. No raw test-count growth target is used.

`RIT_TEST_PARQUET=1` collects all ten designated real-PyArrow cases and missing PyArrow is a
failure. Core profiles set it to `0`, verify PyArrow is absent and collect the
complete non-Parquet suite. Selecting a supported profile never uses skip/xfail
to represent success.

Hero and security are reusable candidate roles and may also be dispatched
explicitly for a relevant change. Delivery requires core, Parquet, performance,
Hero and security success. A failing command cannot be masked by evidence upload.

## Package and candidate checks

```bash
python -m build --outdir /absolute/evidence/dist
python -m twine check --strict /absolute/evidence/dist/*
python scripts/release_check.py --junit /absolute/evidence/core.xml
python scripts/release_check.py --junit /absolute/evidence/parquet.xml --require-parquet
python scripts/release_check.py --dist /absolute/evidence/dist
python scripts/release_check.py --candidate /absolute/evidence
```

Delivery reuses same-commit core/Parquet XML instead of rerunning those suites.
Candidate validation checks complete current canonical test identities against
collection, exact committed source, wheel/sdist module and resource bytes, safe
archive handling and clean installed behavior outside the checkout. Synthetic
archive/XML negatives test corruption detection; they never count as a real
build or installed execution.

Build twice from the same committed source and recorded environment with
`SOURCE_DATE_EPOCH`; compare wheel bytes and every sdist file payload. Sdist archive
timestamps may differ. Keep installed import/input-only checks with numerical
and optional imports blocked separate from actual mathematical/audit execution.
Installed checks cover the existing public APIs, CLI, privacy, safe output and
ordinary, explicitly enabled lineage and longitudinal Hero runs, plus the
packaged three-version example. They exercise installed CSV, JSONL and real
Parquet series with standard, hashed and omitted identifier views. The lineage smoke checks
the frozen G/C/U partition, root incidence/concentration, direct and lineage
bounds, proxy status, privacy and schema outside the checkout with network
blocked. Schema and Hero resources must match their canonical source bytes.

The source archive contains one project root and the complete tracked tree.
Exclude Git internals, environments, caches, generated bytecode, private inputs
and full theory PDFs. Wheel, sdist and source archives retain their distinct scopes.

## Performance and evidence reuse

Measure complete output publication separately from report
`run.duration_seconds`. Untraced Hero wall time supports the under-five-second
target on the stated reference environment. Traced allocation and process peak
RSS are separate observations. Do not substitute a small workload or extrapolation
for required actual 100k execution. See [performance details](../tests/performance/README.md).

Phase 4's metadata-only 100k run took about 1,362.47 seconds and 7.12 GiB peak RSS.
It did not execute general ancestry. Phase 5 Step 9's actual 100k ancestry API run took
123.36 seconds and 1.71 GiB peak RSS, excluding full audit serialization and
ordinary metrics. Its 1,000-record full CLI run took 11.15 seconds. Those scopes
are distinct from the Phase 4 workload and do not imply a comparable speedup.
See [Phase 5 Step 9 results](../PHASE_5_STEP_9.md) for environment and all attempts.
Comparable regression review uses the approved >20% time or >50%
memory thresholds. Operational timeouts are resource guards, not product SLAs.

[Phase 6A Step 8](../PHASE_6A_STEP_8.md) retains the bounded longitudinal
preflights: complete 1,000/10,000-record CLI runs took 11.46/124.65 seconds;
the latter reached 766,644,224 bytes peak process RSS and wrote 42,908,064 JSON
bytes plus 26,943,450 Markdown bytes. These totals include 100 context anchors.
All final Hero series runs took 0.94-1.11 seconds; their inherited RSS floor
prevents a workload-specific memory comparison. The new series, ordinary
metadata report and reverse-chain ancestry API have different workload scopes.
The candidate record reports actual 100k results without extrapolating the
bounded series timings or treating cross-workload differences as a speedup.

Reuse unchanged successful candidate evidence for nonauthoritative administrative
successors and disclose that reuse. Repeat affected gates when executable or
authoritative content changes. Preserve failed attempts and material limitations
in the existing completion/validation record; do not generate another permanent
receipt framework. A hosted artifact that cannot be retrieved is distinct from
locally reproduced bytes and must be described accurately.

The historical Phase 4 procedure and full evidence are recoverable at
`1db3b1a460c233242ff37fbe45b8fac74d6101ef` and its phase completion records.
Stop at the authorized step. Verification never merges, tags or publishes by itself.
