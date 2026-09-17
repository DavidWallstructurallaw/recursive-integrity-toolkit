# Architecture

Status: Phase 2 Step 8 input eligibility implemented.

The controlling architecture is `REPOSITORY_ARCHITECTURE.md`.

The approved dependency direction is:

```text
utilities and shared models
-> input and representation boundaries
-> observability eligibility
-> metrics and lineage
-> result assembly
-> renderers
-> CLI
```

Phase 1 provides import-safe module locations and owner metadata. Analytical behavior begins only in later approved phases.

## Phase 2 Step 8: input eligibility

`observability.levels.classify_observability` accepts already normalized canonical
records, optional typed provenance, an explicit `RepresentationConfig`, and a
`VersionOrderResult`. It reuses identity, provenance and immediate-parent
validators. It never reads a file, executes a mapping, assigns states, hashes
content, traverses ancestors, renders a report or samples. Full audit-bundle
orchestration remains Step 9; no public CLI command is introduced here.

The internal `ObservabilityAssessment` carries the maximum supported Level 0-5,
all seven independent capabilities, requirements/reason codes, named coverage,
and retained `validation_messages`. Internal `coverage_details` keeps provenance
row, required-field and grounding coverage distinct. No report schema is changed.
Output mappings are read-only; source payloads are not copied into this result.
Fatal identity/schema failures raise errors. A zero-record valid scope raises
`E_EMPTY_DATASET` and cannot be certified as Level 0.

One call uses one explicit content mode. In local_ref mode, unread path strings
are not analyzable content. Callers can pass `resolved_content` only after an
explicit PR-017 read. Matching record keys and nonempty UTF-8 text are checked,
but the classifier neither reopens the file nor certifies a caller's IO history.
Missing or failed reads stay unavailable. A declared usable topic/label field
can qualify independently. In inline mode the canonical content is already text.

Representation validation checks declarations, field types and coverage only.
No state assignments are created. Missing exclude values reduce coverage; error
blocks the requested representation; explicit_missing_state with gaps remains
deferred until that configured identity can be validated. Embedding/config-derived
representations and cross-version state mapping are not executed. The supported
exact-form declaration requires `normalization_profile=exact_utf8_v1`; no hash
is calculated. Raw content and record form never certify semantic capability.

A shared explicit representation version can apply to every supplied version.
Alternatively, a complete compatibility map can name one common representation
version. Conflicting/missing IDs block comparison. Each compared dataset version
must have usable represented records. Partial coverage remains disclosed.
`state_mapping_present=True` does not certify the mapping; it makes comparison
unavailable pending its validation. Version-order flags are reconstructed from
retained declarations, never from filenames.

Provenance availability requires valid matching rows and known grounding.
Unknown grounding preserves Level 2 but lowers this capability to partial.
Incomplete required-field assessments preserve errors and cannot become valid
merely because row coverage is high. Source type, grounding and review remain
independent declarations.

Lineage uses a sufficient input certificate: references resolve and every edge
crosses strictly to an earlier explicitly ordered version, with complete parent
declarations and no affected errors. Acyclicity follows from version order; no
cycle detector or graph traversal runs. Unknown grounding and ungrounded terminal
declarations keep lineage partial even when a path is certified. Same-version
edges leave general graph validation deferred. Ambiguous/invalid parents preserve
errors and block lineage without erasing independent dataset evidence. Coverage
counts resolved declared reference entries, including original duplicate/alias
occurrences. It is not ancestry coverage or external-root coverage.

The seven capabilities are ingestion, content_diagnostics, provenance, lineage,
dataset_longitudinal, model_longitudinal and intervention_simulation. A high
maximum level cannot erase another family's limitations. Model longitudinal is
unavailable without an approved model-evidence validator. Merely setting
`model_evidence_present` cannot certify evidence or promote its capability.

### Experimental scenario declarations

Existing JSON/TOML config still accepts only simulation enabled/seed. These alone
never grant Level 5. An internal `ScenarioParameters` object can carry already
approved parameters from `DEFINITIONS_AND_UNITS` sections 12-13: model_name,
resample_size, simulation_horizon, simulation_replicates, state_distribution,
external_input_distribution and reopening_weight. Activation and integer seed
remain in the existing `ScenarioConfig`. There is no new run-config syntax.

Only closed_resampling and reopened_resampling are recognized. Distribution
inputs are explicit unique (state, mass) tuples. Values must be finite, nonnegative
and sum to one within the approved 1e-12 absolute/relative tolerances. No distribution
is inferred, renormalized or mixed. Reopening needs an external distribution over
the same explicitly declared state space and a weight in [0,1]. A zero mass can
preserve a named re-entry state. Resample size/replicates are positive integers;
horizon may be zero. Valid declarations grant experimental input eligibility only,
with `R_SCENARIO_EXECUTION_DEFERRED`. No simulated or empirical intervention result
is produced.

### Reason codes and preserved diagnostics

The closed `REASON_CODES` registry in `observability/levels.py` is separate from
existing E_* and W_* validation codes. Every unavailable/partial capability has
registered reasons and missing requirements; original validation messages remain
visible. Input failures with unknown record denominators keep coverage unavailable
rather than inventing a denominator. Probabilities are checked only as declared
scenario inputs. No analytical score, aggregate integrity rating or conclusion
about model collapse is introduced.

All prior validation/normalization implementations and security limits remain.
Real optional Parquet-presence verification is still outstanding from Step 2.
