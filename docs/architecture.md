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


## Phase 3 Step 2 active boundary

Earlier Phase 2 sections remain historical input-layer documentation. Current
field-only behavior resides in representations/base.py and representations/field.py.
It reuses the existing pure canonical validator, never ingestion or bundle
orchestration. Results contain immutable selection metadata, assignments,
exclusions and named coverage. Metrics, hashing, comparison, graph, sampling and
report/CLI integration remain deferred.

There are still forty modules, with twenty-four protected placeholders. Exact
function, class, named-import, call and operation-family checks apply to the new
modules. Original Phase 2 file/test anchors remain frozen; accepted Step 1 is an
additional checkpoint for incremental scope and regression identities. Ordinary
validate_bundle calls retain input-only behavior.

## Phase 3 Step 3: exact record form and PR-006 counts

`representations/content_hash.py` now encodes explicit validated content under
`exact_utf8_v1` and uses the unchanged `utils/hashing.py` byte helper. It reuses
Step 2's scope-validation helpers without modifying their implementation.
`metrics/duplicates.py` delegates to this pure representation boundary and returns
only exact groups plus the two PR-006 counts. Its output does not retain source
text, notes or provenance. A caller-supplied digest is never trusted as equality.

Exactly two previously empty modules gain behavior; 22 package modules remain
protected placeholders. All field-representation behavior and Phase 2 ingestion,
normalization, provenance, observability and CLI behavior remain unchanged.
No metric is dispatched automatically from an input capability. No file/network
access, content transform beyond the declared byte profile, cross-version pooling,
semantic similarity, sampler, graph traversal or report assembly is added.

Step 3 retains all accepted Phase 2, Step 1 and Step 2 test identities. Historical
source hashes and the Step 2 test exception remain frozen. Current-stage function,
import, call, arithmetic and path gates are explicit. Installed validation includes
both the inherited no-dependency input check and a separate exact-count check with
NumPy/pandas present. Intermediate artifacts do not declare phase completion.

## Phase 3 Step 4: single-scope distribution calculations

`metrics/diversity.py` exposes `calculate_state_distribution`,
`distribution_from_counts` and `distribution_from_probabilities`. These are
pure in-memory calls for one explicitly selected version and representation.
The input-only `validate_bundle` workflow remains unchanged and does not call
metrics. No loader, CLI, report, graph or simulator is imported by this module.

Each result binds counts, frequencies, positive support, Gini-Simpson diversity
and Simpson concentration to its declared scope and denominator. Optional
weighted results require an explicit included-key map and remain alongside the
unweighted output. Supplying probabilities does not create empirical counts.
Their original total and permitted rounding residual remain visible.

Assignments, exclusions, summary flags and scope identities are revalidated.
A point-mass diversity of zero is available; an empty or all-excluded
representation has unavailable scalar values and reasons. No result certifies
semantic completeness, independent provenance or functional failure. Later
metric families and the formal report workflow remain deferred.

Twenty-one modules remain protected placeholders. All prior source anchors and
test identities are retained. The new module has explicit symbol permissions
and a reviewed, version-neutral AST-body fingerprint in addition to behavioral
mathematical tests. Build checks also exercise the actual installed distribution
kernel, separately from the no-dependency import and input-only checks.

## Phase 3 Step 5: declared provenance calculations

Only `metrics/provenance.py` gains runtime behavior. `summarize_provenance`
consumes an existing exact Phase 2 join and its unfiltered single-version scope.
`classify_direct_grounding` exposes the same direct partition independently.
Neither function loads data, attaches rows, inspects content, resolves parents,
opens files, writes reports or certifies source truth. `validate_bundle` does not
invoke these functions automatically.

Source categories and a separate missing-provenance share complete the declared
partition. Confidence remains four counts. Missing fields in matched rows make
their own complete composition unavailable, retaining errors and all three
Phase 2 coverage measures. Explicit source weights have a separate mass denominator.
The direct partition requires valid mandatory fields and yes/no grounding;
otherwise it stays unresolved. Source class/review/confidence are independent.
No closure interval is implemented until Step 6. Twenty pure runtime placeholders
remain protected, together with all earlier formulas and input-layer behavior.


## Phase 3 Step 6: direct closure-exposure interval

`metrics/bounds.py` now exposes explicit pure `closure_exposure_bounds(...)` and
`direct_closure_exposure(...)`. Both use the full unweighted single-version scope.
T3 F-009 = C/N, F-010 = (C+U)/N, width = U/N. Results are derived metrics labeled
`toolkit_operationalization`, not a lineage measure or a universal risk score.

The dataset adapter consumes Step 5 results, preserves input errors and independent
coverage/confidence disclosure, and rejects inconsistent partitions or altered
availability summaries. No usable required provenance means unavailable dataset
scalars; valid explicit unknown grounding can support [0,1]. No confidence weighting,
midpoint, graph, file access, or automatic input-pipeline invocation is introduced.
All later-stage boundaries and immutable earlier implementations remain.

## Phase 3 Step 7: explicit tail and analytic extinction

`metrics/tail.py` adds `select_tail` over unweighted count-backed Step 4 results,
with explicit rule, positive-support membership, deterministic rarity ordering,
record denominator and unavailable scope handling. `one_step_extinction_probability`
is a separate explicit analytic closed-multinomial call. No RNG, weighted tail,
quantile, inference of thresholds, input-pipeline dispatch or later-phase workflow
is introduced. The other 39 package modules remain unchanged in this step.

## Phase 3 Step 8: explicit closed mathematical kernels

`metrics/resampling.py` implements `expected_diversity_after_steps` and
`simulate_closed_resampling`. Both require a declared probability vector, scope,
representation, n and horizon; sampling additionally requires seed and replicates.
Analytic expectations and sampled paths remain distinct simulation outputs.
Only the explicit sampler lazily imports NumPy, constructs PCG64 and records its
version and scheduling. Work limits apply before allocation; no global RNG,
automatic invocation or parameter inference is introduced. Existing input-only
validation remains unchanged. T5 loss/reopening and experiment orchestration are
still deferred. Numerical corrections, deterministic replay limits and resource
bounds are documented in PHASE_3_DECISIONS.md.
