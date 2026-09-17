# Architecture

Status: Phase 2 input workflow. Actual milestone acceptance is recorded in `PHASE_2_COMPLETION.md`.

`REPOSITORY_ARCHITECTURE.md` remains authoritative. Forty package modules are retained, including twenty-six docstring-only later-layer placeholders. Step 10 changes no package module.

## Ownership and flow

| Layer | Modules | Responsibility |
|---|---|---|
| Contracts | models, errors, config | Project-owned metadata, structured failures and explicit settings |
| Ingestion | io/loaders, utils/hashing, utils/paths | Local snapshots, inventory and explicit contained text reads |
| Mapping | io/schema_mapping | Fixed declarative row transformations |
| Canonical boundary | io/normalization, utils/ordering | Row typing, identity and presentation order |
| Validation | io/validation | Joins, chronology, immediate parents, generation and bundle orchestration |
| Classification | observability/levels | Evidence-bounded levels and independent capabilities |

Implemented owners are PR-001, PR-002, PR-003, PR-004 input basis, PR-007, PR-008 input basis, PR-009 validation, PR-010, PR-011 and PR-017. PR-016 supports input determinism and hashing. Similar terminology does not authorize later analytical owners.

```text
explicit AuditBundle
-> source roles and local paths
-> inventory and strict control parsing
-> table loading
-> explicit mapping
-> canonical normalization and identity
-> provenance attachment and validation coverage
-> explicit chronology and immediate dependencies
-> optional explicit PR-017 content reads
-> independent capability classification
-> BundleValidationResult in memory
```

Adjacent-layer imports in the orchestrator occur only at invocation, because normalization/classification reuse validators. The checker authorizes exact import and IO-call sites; the validation module is not broadly exempted. Existing validators retain their earlier no-IO boundaries. Output configuration is not executed. No directory scan, report, cache, worker or public audit CLI is created.

## Input observability

The classifier accepts already normalized records, typed provenance, explicit representation and VersionOrderResult. It never reads files, applies mapping, assigns states, hashes content, traverses ancestry or samples. ObservabilityAssessment retains levels, all seven independent capability keys, reasons, requirements, named coverage and validation messages. Result mappings are read-only. Zero valid records raise E_EMPTY_DATASET rather than qualifying as Level 0.

Unread local-reference strings are not analyzable text. Supplied resolved-content identities/text are checked, but the classifier cannot certify a caller's IO history. The bundle obtains text through the explicit PR-017 reader. A usable declared topic/label field can qualify independently.

Representation checks cover declarations, field types and coverage. Missing exclude values reduce coverage; error blocks requested representation. Explicit-missing-state gaps and embedding/config-derived states remain deferred. Exact form requires normalization_profile=exact_utf8_v1, without computing hashes or semantic certification. Shared explicit representation IDs or a complete compatible map can permit comparison. Conflicts/missing IDs or unvalidated state mappings block it. Version-order flags are rechecked from declarations, never filenames.

Provenance availability needs valid matching rows and known grounding. Unknown grounding preserves Level 2 but yields partial provenance. Missing required fields stay errors despite complete row coverage. Source category and human review never substitute for grounding.

Lineage readiness uses a sufficient input certificate: complete declarations, resolved immediate references and strictly earlier explicitly ordered versions without affected errors. Acyclicity follows from those conditions without a graph algorithm. Unknown grounding and ungrounded terminal declarations keep the capability partial. Same-version edges defer graph validation. Reference coverage counts original entries, including aliases/duplicates, not ancestry or external-root coverage. Invalid parents do not erase independent valid dataset evidence.

Model longitudinal remains unavailable without an approved evidence validator. A presence flag cannot certify it. Dataset Level 4 does not imply model performance.

## Experimental declarations

Activation and seed alone do not grant Level 5. Internal ScenarioParameters carries explicitly declared approved model parameters. Only closed_resampling and reopened_resampling are recognized. Distribution tuples require unique states, finite nonnegative masses and total one within approved 1e-12 tolerances. Reopening needs an external distribution on the same declared state space and weight in [0,1]. Size/replicates are positive integers; horizon may be zero. No distribution is inferred, renormalized or mixed. Qualification remains experimental with R_SCENARIO_EXECUTION_DEFERRED, without execution.

## Errors and limits

Reason codes remain separate from E_*/W_* diagnostics. Higher maximum level never erases a family's missing requirements or errors. Unknown input denominators remain unavailable. Check has_errors separately.

Fatal parsing, identity, unsafe mapping and invalid present fields raise. Incomplete provenance and content/parent-family failures may coexist with other valid metadata and retained diagnostics. Aggregate diagnostic paths are redacted; internal records/inventory still contain caller-sensitive information and are not public redacted reports.

Generation uses flat indexes and bounded monotone scans. Some same-version chains have quadratic worst case. No 100,000-row performance claim or independent security certification is made. Content containment assumes a trusted stable directory; see docs/privacy.md.

No protected metric, representation-execution, lineage or report module is opened. The conceptual dependency direction remains utilities/contracts, input boundaries, observability, later metrics/lineage, assembly, renderers and CLI. Phase 3 is not authorized.
