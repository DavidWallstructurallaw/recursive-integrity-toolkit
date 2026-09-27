# Phase 6A Step 7: CLI, configuration and installed examples

## Authority and scope

The Theory Owner requested `Phase 6A Step 7 继续` on 2026-09-26
America/Los_Angeles (2026-09-27 UTC). This step starts from accepted commit
`edbcf9ac2ba152f17db6f722750275a1cb235cb3` on `phase6a-longitudinal`.
The approved plan and longitudinal contract section 2 govern the integration.
Package/schema remain `0.1.0.dev4` / `1.2`.

## Implemented behavior

`audit --longitudinal` accepts repeated comparison inputs and explicit retained
chronology. The primary must be the latest selected version. Each selected
physical file must contain exactly one nonempty version, with disjoint populations.
Adjacent pairs are the default; `--baseline first` adds deduplicated first-snapshot
pairs. Tail and lineage remain explicit requests. The shared selected lineage
graph and SCC analysis each execute once.

Inert configuration supports a common representation/semantics or exact
per-version declarations, full directed mapping descriptors, and a positive
integer `max_longitudinal_versions` defaulting to 100. Competing singleton
declarations are errors, including equal CLI/config values. Ordinary default
configuration hashes are unchanged; effective series options affect their hash.
Legacy ordinary single-version/pair and Hero behavior remains available.

Primary ordinary distribution, provenance and direct bounds reuse the selected
snapshot. A narrow validated adapter exposes the actual primary's selected
lineage through the existing ordinary result type, sharing cycle/root evidence
without graph, SCC or root recomputation. It rejects comparison/context targets
and stale or malformed handoffs.

Missing/conflicting chronology retains independent snapshots when their
declarations and populations remain valid. Original order/file diagnostics are
retained and bound to the failed handoff; no fallback order becomes an inferred
successful series. Invalid population shapes produce a safe error-only report.
Missing required semantics/representation fails configuration before analysis.
Admission failure computes no snapshot prefix. `validate` accepts repeated
inputs and inert series config, including enabled config, while executing no
metrics, graph, series or simulation.

`example --longitudinal` runs the unchanged two-version Hero, optionally with
`--lineage`. `example --dataset longitudinal --longitudinal` extracts a separate
three-version example. Its seven packaged resources exactly mirror canonical
files; the explanatory README is examples-only. Rational expectations come from
the frozen `observed_three_version` fixture, which remains unchanged. The example's
missing provenance is intentional evidence and produces a warning.

## Verification

The focused new tests passed with real PyArrow 25.0.1:

| Boundary | Passing cases |
|---|---:|
| Inert config, schema, modes, mappings, conflicts and hashes | 75 |
| Actual-primary lineage adapter and evidence reuse | 11 |
| Source CLI, CSV/JSONL/Parquet, chronology, failures, privacy, exits and output safety | 46 |
| Fresh installed wheel, external working directories and blocked network | 18 |
| Example mirror bytes, frozen inputs and independent rational values | 10 |
| Extended retained-selection-error and failure handoff checks | 19, including 5 existing |

Installed tests cover both examples in standard/redacted modes with and without
lineage, three real input formats in preserve/hash/omit modes, and input-only
validate. Each subprocess uses `-I`, removes `PYTHONPATH`, checks that imports
come from `site-packages` outside the checkout, and blocks socket/urllib network
connections. No dependency fallback or silent skip is used.

The wheel and sdist were built through the available setuptools 84 backend.
A fresh virtual environment received the wheel with `pip --no-index --no-deps`.
It inherits the existing runtime's NumPy 2.3.5 and pandas 2.2.3; PyArrow 25.0.1
was reused from the local dependency environment through package/metadata links.
This establishes a fresh toolkit installation, not an independently downloaded
dependency environment or a complete compatibility matrix.

The final Python 3.12.14 broad regression completed with **3612 passed in
293.15 seconds**, zero failures, skips or deselections. It includes the focused
cases above, so their counts are not additive. The test environment's previously
installed toolkit was replaced with the current wheel before this run; the new
installed-series checks target the separate fresh virtual environment.

```sh
RIT_TEST_PARQUET=1 \
RIT_STEP7_INSTALLED_PYTHON=/workspace/scratch/954124762a46/phase6a_step7_work/step7_installed_env/bin/python \
/workspace/scratch/954124762a46/phase5_step8_env/bin/python -m pytest -q \
  tests/unit tests/integration tests/golden \
  --junitxml=/workspace/scratch/954124762a46/phase6a_step7_work/regression.xml
```

This covers current unit, integration, golden, import-isolation, input-only,
privacy, output-safety and archive-boundary tests. Performance tests and the
supported platform/dependency candidate matrix are outside this run.

Archive verification confirms that all 41 package modules and 14 canonical
resources in both distributions match the current source bytes. All nine
existing wheel installation smoke groups and the sdist Hero smoke passed.
The initial full archive-smoke invocation reached the final wheel Hero check
and found missing test-only `jsonschema` in the fresh environment. Reusing the
local schema-validation dependencies resolved that environment issue; the
affected wheel Hero and remaining sdist checks then passed. Previously passing
groups were not repeated. No product change was needed for this correction.

| Development artifact | SHA-256 |
|---|---|
| Wheel | `def28a429aec917857fb5baeeea052161009ecf6f288e98fdd4edea75e4b177f` |
| Source archive | `8bcc985da58fdf69faa465d6fcfb294da7dabfbadcb5585af7fdad028cac50a5` |

The final protection checks passed:

```sh
python scripts/check_spec_consistency.py
python scripts/check_traceability.py
python scripts/release_check.py
git diff --check
```

They retain 16 frozen specifications, five schemas, six unchanged Hero files,
14 exact packaged resource mirrors and 41 owned modules. The current source
gate protects 54 product files and admits 21 Step 7 implementation paths.
The canonical report schema and longitudinal acceptance fixture/oracles remain
unchanged from Step 6. New resource-corruption tests cover both wheel and sdist.

## Remaining scope

No version bump, full OS/Python/dependency matrix, scale measurements, merge,
tag or release is part of this step. Step 8 owns bounded adversarial/scale
preparation; Step 9 owns dev5 and candidate verification. No new runtime
dependency or Python package module is added. Steps 8-9 and Phase 6B remain
unstarted.
