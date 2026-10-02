# Phase 6B Step 6: user guide and installed synthetic example

Date: 2026-09-30. Status: **TASK COMPLETE, PHASE CONTINUES**.

## Completed

The Theory Owner requested `Phase 6B Step 6继续`, authorizing this increment
from Step 5 commit `33ae8af1aaeb99ac118368148a80d563804eeff9` on
`phase6b-simulation`.

Added `examples/simulation/` with `config.json`, `records.jsonl`,
`provenance.jsonl` and independently authored `EXPECTED_OUTPUTS.md`, plus
byte-identical packaged copies. The new installed command is:

```bash
rit example --dataset simulation --simulate --out ./simulation-workspace
```

The fixture selects closed and reopened models with `p=(1,0)`, `r=(0,1)`,
lambda `1/4`, sample size 2, horizon 6, three replicates and seed 17. Two separate
fictional audit records use X/Y topics. Their two-record scope and statistics
never establish the A/B scenario inputs or its empty record membership.

The command requires explicit activation, rejects incompatible example modes
and custom overlays before extraction, preserves packaged input bytes and
never overwrites an existing workspace. Ordinary Hero, lineage and longitudinal
examples retain their behavior. Existing users can edit a copied config and
run `audit --simulate` with explicit local inputs.

The guide in `docs/simulation_example.md` covers installation, first use,
assumptions, exact first-step arithmetic, report paths, replay, validation,
custom configuration and privacy. The mixed source is `(3/4,1/4)`; possible
count-vector probabilities are `9/16,6/16,1/16`. First-step re-entry probability
is `7/16`, and expected sampled diversity is `3/16`, distinct from source
diversity `3/8`. These are independently calculated targets, not a stored random
trajectory. The closed baseline remains zero. Later reopening paths can lose
diversity, and this particular external vector cannot restore a lost A state.
No guarantee of a sampled re-entry or empirical intervention benefit is implied.

Updated README, CLI/contract documentation and existing architecture/traceability
records. The inherited closed analytic limitation prose remains scoped to that
closed result; the guide explains the separate reopened envelope. No numerical
owner, config behavior, report schema, privacy algorithm or renderer changed.

The source gate now uses accepted Step 5 and permits ten exact product paths:
CLI, the package-data declaration and eight new canonical/packaged resource
paths. It checks all other parsed package metadata against the accepted version.
The existing resource inventory, installed-example program and CI jobs were
extended without introducing a new delivery registry.

## Source and report verification

Final affected source run:

```text
tests/integration/test_simulation_example.py
tests/integration/test_scenario_cli.py
tests/integration/test_phase4_cli.py
tests/integration/test_longitudinal_cli.py
tests/integration/test_phase5_lineage_cli.py
tests/integration/test_longitudinal_example_resources.py
tests/integration/test_current_verification.py
tests/integration/test_ci_workflows.py
tests/integration/test_package_install.py
tests/integration/test_no_network.py
tests/integration/test_repository_structure.py
335 passed in 39.36s
```

The new source example file contains 18 tests covering independent rational
arithmetic, complete transition/event identities, same-environment replay,
source/sample separation, explicit scope, privacy, input-only validation,
network isolation, incompatible mode rejection and no-overwrite behavior.

The existing `tests/golden/test_phase4_reports.py` was run through the new
wheel-installed interpreter, including its installed Hero oracle:

```text
72 passed in 8.50s
```

An initial golden run passed 71 cases and found one stale installed-resource
count of 14. The expected count was updated to 18; all module/resource hashes,
Hero expectations and privacy comparisons remain enforced. During new test
development, report-field assertions were aligned with the existing closed vs
reopened wire shapes, and a requirement for a particular random re-entry outcome
was removed. Tests instead verify each actual path's complete event identities.

Current static checks pass: 16 frozen specifications, 41 owned runtime modules,
18 canonical resource copies, 73 protected product files and ten authorized
implementation paths. `git diff --check` passes.

## Actual local delivery verification

Built both distributions with the declared setuptools PEP 517 backend using
`python -m build --no-isolation --sdist --wheel`. The build environment used
Python 3.12.14 and setuptools 84.0.0. The existing distribution checker verified
the complete 41-module and 18-resource inventories, exact source/resource bytes,
version, notices and archive member boundaries.

Installed the wheel with `pip install --no-index --no-deps` in a new local
environment. Separately extracted the sdist through the existing safe extractor,
rebuilt a wheel with `pip wheel --no-index --no-deps --no-build-isolation`, and
installed it in a second new environment. Every uncompressed archive member of
the original and rebuilt wheels is identical; their archive hashes differ.
Neither environment contained the toolkit before installation.
They shared existing local NumPy 2.3.5 and pandas 2.2.3 dependencies.

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| Original wheel | 392953 | `7846afca016f873368c919281d3f351e2d7250af06839c59f31e83a80ab35b8f` |
| Source distribution | 362040 | `fd2087fbd48043014e4cc42c9edbd09009a663ae9907771a6eaba6a8a9605aed` |
| Wheel rebuilt from sdist | 392953 | `26966a7f310d3f6aa1769847d600160479128b8c5baa72f6f37dea50faf36c63` |

`tests/integration/test_simulation_installed.py` passed **7 tests in 3.08s**
against the original wheel and **7 tests in 3.21s** against the rebuilt wheel.
The subprocesses use `-I`, run outside the checkout, require a site-packages
origin, block network operations, validate actual reports and compare packaged
resources. They cover standard/redacted execution and replay, numerical/event
identities, rejected modes and fresh-process `validate` with both inert and
enabled config while sampler/NumPy imports are blocked. PyArrow imports are
blocked too; this proves optional-dependency isolation, not actual package
absence in these environments.

The existing `smoke_installed_example` program also passed from a real local
wheel installation outside the checkout. It exercises ordinary Hero, lineage,
both longitudinal examples and the synthetic scenario with standard/redacted
reports, local schema validation, exact resources, no overwrite and blocked
network. The installed `rit` console command generated the example reports;
the `recursive-integrity` alias and isolated `python -m` entry point returned
the expected version.

These are Linux/Python 3.12 local delivery checks. No supported-environment
matrix, actual PyArrow-absence installation, new performance measurement or dev6
candidate pass is claimed. Build artifacts identify the tested development
package and do not constitute registry publication.

## Handoff

Package version remains `0.1.0.dev5`, report schema `1.3`. Step 7 will perform
bounded scientific/adversarial and performance preparation; Step 8 retains the
dev6 candidate verification. No merge, tag or release is part of this increment.
