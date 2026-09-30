# Phase 6B Step 5: explicit configuration and CLI execution

Date: 2026-09-30. Status: **TASK COMPLETE, PHASE CONTINUES**.

## Completed

The Theory Owner requested `Phase 6B Step 5 go`, authorizing this increment
from Step 4 commit `f5d94d9aa250bbb63c7317884966946bc1d44533` on
`phase6b-simulation`.

Expanded the existing immutable `ScenarioConfig` with ordered selected models,
explicit internal/external distributions, reopening weight, numerical parameters,
full representation, shared state meaning and scenario scope labels. Supplied
declarations survive JSON/TOML loading, normalized serialization and configuration
hashing. JSON duplicate keys are rejected. Safe summaries expose only the request
flag; distributions and caller context are excluded from declaration reprs.

Input-only shared predicates validate literal states, including empty strings,
finite built-in probabilities, absolute mass residual, exact scalar bounds,
matching declared state sets and combined state/step/replicate admission. They
never normalize a vector, evaluate a mixture, import a numerical owner or create
an RNG. Observability uses these predicates and preserves the separate legacy
`ScenarioParameters` API; competing scientific declarations fail.

`audit --simulate --config PATH` activates complete declarations. An enabled
complete block also requests execution without the flag; an explicitly false
value conflicts with it. Disabled declarations, including partial legacy
enabled/seed blocks, remain inert. Activated audits require every scientific declaration.
`validate` accepts enabled declarations as input only, retaining eligibility
separately from execution and empty simulation output.

The CLI constructs the accepted experiment request lazily. Its scope contains
the supplied version/scope labels, empty record identities and
`explicit_scenario_probability_vector`; audit records never imply a scenario
distribution or population. Run and result seeds agree. Simulation failures use
the existing family-error mechanism, preserving completed independent audit
evidence and safe failure exit codes.

`example --simulate --config PATH` accepts a local scenario-only overlay. It is
validated before workspace creation and retained in the extracted configuration.
Enabled complete overlays may omit the flag. Ordinary Hero/longitudinal examples
and all packaged resources remain unchanged. A dedicated installed synthetic
example remains Step 6 work.

Fresh-process tests identified that the existing report assembly module imported
the sampler owner while loading, even without execution. Scenario type/constant
imports now occur only when adapting supplied simulation evidence. Reviewed
scenario privacy prose is loaded only for such reports and passed immutably
through the existing privacy traversal. Numerical kernels, report schema and
renderers did not change.

The existing source gate advances to Step 4 and authorizes five exact product
paths: configuration, CLI, observability, config schema and the assembly import
adjustment. The existing traceability checker now includes configuration in its
input-only module set. Focused CI includes the two new scenario test files.

## Validation

Final input, configuration and boundary run:

```text
tests/unit/test_scenario_config.py
tests/integration/test_scenario_cli.py
tests/unit/test_PR010_observability.py
tests/unit/test_PR011_capabilities.py
tests/unit/test_longitudinal_config.py
tests/unit/test_phase5_lineage_config.py
tests/unit/test_PR016_determinism.py
tests/integration/test_no_network.py
tests/integration/test_no_algorithms.py
tests/integration/test_repository_structure.py
tests/integration/test_hero_end_to_end.py
tests/integration/test_current_verification.py
tests/integration/test_ci_workflows.py
470 passed in 13.42s
```

Final report, privacy and CLI regression:

```text
tests/unit/test_scenario_report_contract.py
tests/integration/test_scenario_reports.py
tests/unit/test_PR012_evidence_classes.py
tests/unit/test_PR013_report_schema.py
tests/unit/test_PR014_unavailable.py
tests/unit/test_PR015_redaction.py
tests/unit/test_PR018_language.py
tests/integration/test_phase4_cli.py
tests/integration/test_longitudinal_cli.py
tests/integration/test_phase5_lineage_cli.py
tests/golden/test_phase4_reports.py
-k 'not installed_without_pyarrow'
529 passed, 1 deselected in 82.18s
```

These two nonoverlapping final source runs contain **999 passing tests**. One
installed-only case was deliberately deselected; there were no failures or skips.
The new files contain 44 configuration cases and 26 CLI cases. These include
same-seed/model-order replay, configuration detachment and hash binding, strict
absolute tolerance, aggregate refusal, duplicate declarations, typed-object
privacy, explicit zero-record scenario scope, all supported model selections,
fresh-process validation with sampler/NumPy imports blocked, missing NumPy and
pre-RNG numerical rejection with retained audit evidence, redacted sinks and
example preflight failure before extraction.

Initial attempts are retained honestly: the two new validation import-blocker
cases failed before the assembly fix. A broader regression exposed one stale
PR016 renderer test that permuted extinction events, which Step 4 now requires
in canonical transition order. It now tests a freely ordered conclusion list;
scientific event validation remains strict. An intermediate assertion compared
raw caller text with privacy-transformed output and was corrected to compare
the actual privacy views. Final runs above include these corrections.

All three current static checks pass: 16 frozen specifications, 41 owned runtime
modules, 14 canonical resource copies, 70 protected product files and five
authorized implementation paths. `git diff --check` passes. Tests ran from source
on Linux/Python 3.12 with NumPy 2.3.5 and pandas 2.2.3. One existing installed-only
golden case is excluded because this runtime has no installed wheel. Installed
delivery, the supported environment matrix and performance remain assigned to
later planned steps; none is claimed here.

## Handoff

Package version remains `0.1.0.dev5`, report schema `1.3`. Step 6 will add user
documentation and the small installed synthetic example. No merge, release tag
or publication is part of this increment.
