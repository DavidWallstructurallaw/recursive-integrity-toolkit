# Development and Release Verification

## Current Phase 5 boundary

Phase 5 Step 8 is approved. Runtime remains at `0.1.0.dev3`, with executable
report schema 1.1 for every report. Explicit CLI lineage execution, repeated
context inputs, configuration limits and the installed lineage Hero are the
current implementation scope. Step 9 scale/mutation work and Step 10 candidate
verification remain pending.
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
The existing source check advances its single reference to the completed Step 7
commit; no new Phase 5 hash registry is needed. During Step 8 it permits changes
only to explicit CLI/configuration, the context input role and necessary input,
graph and report adapters, with config/report schema enum updates. It retains the exact product file inventory and
rejects unrelated runtime, package-metadata and canonical Hero changes.
The frozen Phase 0 specification hashes are unchanged. Sixteen frozen
specifications and seven packaged resource copies remain protected. The source
inventory excludes only the generated `src/recursive_integrity_toolkit.egg-info/`
metadata directory; similarly named or nested paths are not excluded, and
symlink rejection and shipped-package inventory checks remain in force.

## Risk-sensitive gates

Ordinary PR checks use the focused job for the active step. Documentation-only
changes require formatting and affected consistency checks. As implementation
scope changes, update the focused selection to affected owners and dependency
neighbors. It does not establish candidate acceptance.

Dispatch `ci.yml` with `gate=candidate` for a stable candidate. The workflow runs:

| Role | Required execution |
|---|---|
| Core | Ubuntu/Windows, Python 3.11/3.12, current/minimum compatible dependencies; PyArrow absent |
| Optional Parquet | Ubuntu/Python 3.12, real PyArrow with roundtrip, row-limit and invalid-file regressions |
| Canonical Hero and mathematics | Frozen mathematical cases, report goldens and packaged Hero behavior |
| Security | No-network, input/path, privacy/redaction and output-publication boundaries |
| Reference performance | One Ubuntu/Python 3.12 profile, including required actual 100k workloads |
| Package/delivery | Wheel/sdist integrity, clean installed execution, reproducibility and tracked-source archive |

Compatibility cells run complete canonical regression with
`--ignore=tests/performance`. The designated performance job runs
`tests/performance` once, avoiding nine repetitions of the costly 100k report
workload. The Phase 5 sparse-lineage test is still a placeholder in Step 8;
it becomes an executable graph benchmark in Step 9. No placeholder is counted as
a successful lineage measurement.

The existing minimum compatible pair remains NumPy 2.0.0/pandas 2.2.2. Record
actual resolved dependencies, `pip check`, Python/platform, commands, results
and material limitations. A skipped, failed, duplicate or uncollected required
test cannot stand in for a passing result. No raw test-count growth target is used.

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
both ordinary and explicitly enabled lineage Hero runs. The lineage smoke checks
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
It did not execute general ancestry. Phase 5 must measure its own enabled graph
workloads; comparable regression review uses the approved >20% time or >50%
memory thresholds. Operational timeouts are resource guards, not product SLAs.

Reuse unchanged successful candidate evidence for nonauthoritative administrative
successors and disclose that reuse. Repeat affected gates when executable or
authoritative content changes. Preserve failed attempts and material limitations
in the existing completion/validation record; do not generate another permanent
receipt framework. A hosted artifact that cannot be retrieved is distinct from
locally reproduced bytes and must be described accurately.

The historical Phase 4 procedure and full evidence are recoverable at
`1db3b1a460c233242ff37fbe45b8fac74d6101ef` and its phase completion records.
Stop at the authorized step. Verification never merges, tags or publishes by itself.
