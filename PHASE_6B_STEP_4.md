# Phase 6B Step 4: typed scenario reports and privacy

Date: 2026-09-30. Status: **TASK COMPLETE, PHASE CONTINUES**.

## Completed

The Theory Owner requested `Phase 6B Step 4 继续`, authorizing this increment
from Step 3 commit `2e0805dba85754d78854750f692ac02ddaf44a8a` on
`phase6b-simulation`.

Integrated `assemble_report(..., scenario_experiment=...)` with the existing
typed result. Assembly verifies selected model identities, the original request,
common parameters, supplied distributions, scope, representation, seed and
metadata before adapting the evidence. It executes no kernel or RNG. Closed
experiments retain a distinct analytic baseline on the effective sampled start,
closed loss events and caller state meaning. Reopened experiments occupy the
existing T5 `simulations.external_reopening` registry slot. Legacy closed/T2
interfaces retain their shape and external-input prohibitions. Duplicate closed
slots fail; a reopened-only experiment may accompany a legacy closed result
without manufacturing a comparison.

`result.py` now owns schema 1.3 and its bounded scientific consistency checks.
Validation covers supplied/effective normalization, exact counts and frequencies,
support/diversity, constant external-source arithmetic, complete loss/re-entry
events, replicate/step coverage, initial possibilities and comparisons. Positive
sample counts require positive source mass. Recurring events use composite
replicate/step/state identities. Baseline input, model identity, denominator and
single-version scenario scope remain bound. T5 cannot claim a closed F-015
expectation. Sampled seeds agree with run metadata, and completed simulation
execution requires supplied evidence. Simulated evidence retains the unavailable
empirical intervention conclusion; failed or deferred scenario declarations do
not become successful execution.

Generated the canonical schema and packaged copy together. The unchanged JSON
renderer handles the new validated shape. Privacy preserves numeric values and
state alignment across both models while protecting new source, event,
reachability and caller-text paths. Semantic states remain pseudonymized even
when record identities are omitted. Fixed scientific disclosures remain readable;
caller state meaning cannot escape by matching a reviewed literal.

Markdown uses explicit experimental simulation labels, assumption tables and
compact support/diversity trajectories. State, source, event, comparison and
scenario scope-identity tables display at most 100 rows with exact omission
counts. Source probabilities and realized sample counts are distinct. Full
admitted evidence remains in JSON, and tiny positive floats remain positive in
both formats.

Updated current architecture, schema, traceability, README and phase records.
Focused CI includes the two new report test files. The source gate advances to
Step 3 with five exact authorized paths: the result owner, report assembly,
Markdown and the canonical/packaged schema pair. All numerical kernels remain
protected. No analytical dependency, CLI/config activation or package-version
change was introduced.

## Validation

Final experiment, numerical and boundary run:

```text
tests/unit/test_scenario_report_contract.py
tests/integration/test_scenario_reports.py
tests/unit/test_scenario_experiment.py
tests/unit/test_T1_resampling.py
tests/unit/test_T5_reopening.py
tests/unit/test_reopening_fixture_inputs.py
tests/integration/test_phase3_metric_pipeline.py
tests/integration/test_current_verification.py
tests/integration/test_ci_workflows.py
468 passed in 13.71s
```

The two new files contain 82 contract cases and 12 presentation/privacy cases.
They cover actual corrected baselines, endpoint and zero-horizon behavior,
recurrent and multi-replicate losses, explicit request binding, impossible
zero-source samples, forged sources/events/comparisons, F-015 exclusion,
denominator/model/scope binding, no resampling during report work, input-only
validation, safe diagnostics, preserved independent results on failure, all
record-ID modes, 1024-state compact presentation, exact detail caps, tiny positive
probabilities and caller-text protection.

Final existing-report source regression:

```text
tests/unit/test_PR012_evidence_classes.py
tests/unit/test_PR013_report_schema.py
tests/unit/test_PR014_unavailable.py
tests/unit/test_PR015_redaction.py
tests/unit/test_PR018_language.py
tests/unit/test_phase4_output_safety.py
tests/integration/test_longitudinal_reports.py
tests/integration/test_longitudinal_cli.py
tests/integration/test_phase5_lineage_reports.py
tests/integration/test_phase5_lineage_privacy.py
tests/integration/test_phase5_lineage_cli.py
tests/integration/test_partial_lineage_report.py
tests/integration/test_partial_provenance_report.py
tests/golden/test_phase4_reports.py
-k 'not installed_without_pyarrow'
613 passed, 1 deselected in 99.13s
```

These nonoverlapping final source runs contain **1,081 passing tests**, with no
failures or skips. One existing installed-only golden case was deselected: the
current runtime has no installed wheel. An initial attempt reached that
environment limitation; it is not reported as a pass. Installed delivery and
the supported candidate matrix remain planned later-phase checks.

Initial implementation/review runs exposed an analytic floating-point expression
ordering mismatch, schema/privacy shape handling, incomplete canonical evidence
binding and historical hand-authored fixtures whose run seed was null despite
sampled evidence. The implementation now mirrors the kernel's multiplication
order, preserves typed privacy paths and rejects inconsistent evidence. Fixtures
were corrected to declare their actual seeds and empirical-evidence limits;
their targeted negative assertions remain meaningful. Five ordinary Hero golden
files changed only schema-version literals, with all other bytes preserved.

Independent read-only review completed with no unresolved findings. Its 162
valid scenario/privacy/Markdown combinations and additional forged-evidence
probes are supplemental, outside the pytest count. Review specifically confirmed
rejection of missing execution evidence, missing empirical-limit disclosure,
false T5 claims, wrong denominators, model versions and multiple scenario scope
versions.

Verification used Python 3.12.14, pytest 9.1.1 and NumPy 2.3.5 with the current
checkout first on `PYTHONPATH`. All current specification, traceability and
source/resource checks passed: five schemas, 41 owned modules, 16 unchanged
frozen specifications, 14 matching canonical resource copies, 70 protected
product files and five authorized implementation paths. Both generated report
schemas match `result.py`. `git diff --check` passed.

## Continuation

Used approved UD-017 and P6B-D06 with the existing T1/T5 and PR-012 through
PR-016 reporting boundaries. No theory conflict or new approval mechanism was
introduced. UD-031 continues to defer empirical intervention ingestion, and
F-016 external-reference loss remains unregistered.

Current package version is `0.1.0.dev5`, report schema `1.3`. Step 5 will add
explicit configuration and CLI activation while preserving input-only validation.
Installed synthetic example delivery, performance preparation and the dev6
candidate remain subsequent steps. No merge, tag or release publication was
performed.
