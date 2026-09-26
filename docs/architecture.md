# Architecture

## Current Phase 5 architecture

Development version `0.1.0.dev4` implements the approved [lineage contract](lineage_contract.md).
The report schema is 1.1. The existing forty package modules, local-only runtime,
dependency declarations and canonical Hero inputs are retained.

| Current owner | Responsibility and boundary |
|---|---|
| `io/validation.py` | Input joins, retained parent declarations, chronology and generation dependency propagation; never executes lineage or metrics. |
| `lineage/graph.py` | Immutable canonical graph, target/context scope and pre-insertion node/edge guards. |
| `lineage/cycles.py` | Iterative cyclic components, bounded witnesses, affected descendants and structural depth independent of generation. |
| `lineage/ancestry.py` | External-root resolution, strict G/C/U partition, incidence/fractional mass, concentration, coverage and descriptive shared-root evidence. Root memberships and work have finite guards. |
| `metrics/bounds.py` | Explicit direct and lineage closure intervals with distinct denominators and evidence. |
| `models.py`, `reports/assembly.py` | Typed schema 1.1 results, supplied-result binding and canonical evidence assembly; no ancestry recomputation in rendering. |
| `reports/json_report.py`, `reports/markdown_report.py` | Deterministic bounded output, local aliases, aggregate-preserving redaction and explicit unavailable states. |
| `cli.py`, `config.py` | Explicit `audit --lineage` / `example --lineage`, repeatable local context inputs and validated finite limits. `validate` remains input-only. |

Primary records define the target population. Comparison and dedicated context
records can supply ancestors without entering primary metric denominators.
Unresolved paths, missing provenance and cycles remain visible. Topological
roots and depth do not establish independent causal evidence or semantic truth.

Current verification uses one path in the existing consistency, traceability and
release scripts. Exact historical method bodies, snapshot fixtures and migration
chains are recoverable from Git, while direct current product/security tests
remain active. [Release process](release_process.md) defines focused and candidate
gates. Step 10 changes only package version metadata in runtime/package files;
the single current source boundary protects all other accepted product bytes.

## Historical Phase 2-4 implementation notes

The following step statements describe their original stage, including then
unimplemented owners. The current ownership table above and the lineage contract
describe the supported Phase 5 behavior. Historical test bodies remain in Git.

Status: Phase 3 Step 11 development milestone. Actual acceptance is recorded in `PHASE_3_COMPLETION.md`.

The input-layer sections below describe the preserved Phase 2 implementation. Subsequent step sections retain the boundary at their historical stage. The current boundary is summarized here and in the final Step 11 section.

`REPOSITORY_ARCHITECTURE.md` remains authoritative. Forty package modules are retained, including sixteen protected docstring-only placeholders. Step 11 changes only the root version literal in runtime source.

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

An explicit `AuditBundle` drives local source loading, declared mapping, canonical normalization, validation, optional content reads and capability classification. It returns an in-memory `BundleValidationResult`. Every calculation is separately invoked with explicit scope and metadata.

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

At the historical Phase 2 checkpoint, metrics and representations were unopened. The following Phase 3 sections record their subsequently approved boundaries. General lineage and reports remain protected.


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

## Phase 3 Step 9: explicit pair comparison boundary

The input pipeline remains unchanged. Callers explicitly select two distribution
results and provide `ExplicitPairContext`, state-meaning declarations and optional
`StateMappingDeclaration`. `representations/compatibility.py` revalidates ordering
and declaration compatibility. `metrics/diversity.py::compare_support` validates
the consumed numerical basis, applies only a fully declared directed literal map,
and returns F-005/F-006/F-018 with loss/addition sets. No bundle dispatcher,
trajectory, report, lineage analysis or model-performance comparison exists here.

Mapping coarsening is disclosed through exact source/target descriptors and state
meanings, direction, dictionary, collision groups, original distributions and
harmonized distributions. Missing-policy changes and one-to-many allocation are
rejected. Source labels never become an independently validated ontology. Pair
metadata preserves both selected scopes; unavailable input does not become a zero
or a false total-loss result. Weighted and supplied-probability inputs retain
their distinct bases and cannot be mixed with incompatible denominator families.

## Phase 3 Step 10 test-only integration

All runtime implementations remain frozen at the accepted Step 9 revision.
`tests/integration/test_phase3_metric_pipeline.py` composes validation and explicit
calculation calls; `tests/golden/test_phase3_math.py` executes all twenty frozen
oracles. The shared pytest callable is not a runtime audit entry point.
`validate_bundle(...)` remains input-only. Public reports, lineage, external
reopening and longitudinal dispatch remain protected later work.

The performance tests measure synthetic 100000-record metadata, exact duplicates,
and the current Hero input-plus-calculation path. JUnit retains elapsed times and
per-call tracemalloc peaks with environment and scope. These observations do not
certify the future complete-report latency target. Step 11 has not started.

## Phase 3 Step 11 current boundary

Ten previously reserved runtime modules now implement the approved Phase 3 subset: four representations (`base`, `field`, `content_hash`, `compatibility`) and six metrics (`duplicates`, `diversity`, `provenance`, `bounds`, `tail`, `resampling`). Forty modules remain in total. Sixteen later-layer modules retain their exact protected docstring-only bodies. Runtime AST/import checks retain the accepted Step 9 mathematical definitions; Step 10 added test integration, and Step 11 changes only the package version literal.

| Layer | Explicit entry points | Current boundary |
|---|---|---|
| Representation | `assign_field_states`, `assign_content_states`, `validate_representation_compatibility` | Caller-selected scope, declared field/profile, exact states or directed map; no embedded classifier |
| Record form | `detect_exact_duplicates` | Exact UTF-8 grouping and two counts; caller-owned data unchanged |
| Distribution | `calculate_state_distribution`, `distribution_from_counts`, `distribution_from_probabilities` | Support, diversity, concentration; explicit weighted companion only |
| Provenance | `summarize_provenance`, `direct_closure_exposure`, `closure_exposure_bounds` | Full selected scope, separate missingness/coverage, direct declaration-based exposure |
| Tail | `select_tail`, `one_step_extinction_probability` | Explicit approved rule or explicit closed-model marginal |
| Closed model | `expected_diversity_after_steps`, `simulate_closed_resampling` | Explicit n/horizon, sampled-only seed/replicates and lazy NumPy |
| Explicit pair | `compare_support` | Exactly two validated compatible ordered scopes; original and harmonized bases retained |

The ordinary bundle validator never dispatches any of these calls. Metrics may reuse approved pure canonical/provenance/order validators at their exact reviewed call sites, but cannot invoke input loaders or report/CLI orchestration. Imports perform no numerical work, sampling, user file reads or network calls. Explicit invocation tests separately enforce the no-I/O/no-network boundary with numerical dependencies present.

Shared modules retain owner-specific gates. T3 direct bounds do not open lineage bounds; closed sampling does not open T5 reopening; explicit pair operations do not open Phase 6A orchestration. Reports, renderers, embeddings, general lineage, external-reference metrics and reserved logging/result assembly remain protected. No function ownership, source formula, dependency, backend, CLI command or serialized schema changes in Step 11.

Step 11 stage guards pin the original source/runtime digest after undoing exactly the two approved version literals. Historical tests use immutable Step 10 source and preserve all node identities. The two maintenance exceptions are narrow, explicitly approved and checked against exact original bytes. Build/install/archive tools operate as maintainer processes outside user-data flows. Final acceptance is bound to actual CI for the final source commit.

## Phase 4 Step 1: baseline and governance activation

This section records the current governance boundary after the historical Phase 3
sections. The accepted starting commit is
`e3ffb8c0a88bfe31f669f9662d9b5213da628b3a`. The approved `PHASE_4_PLAN.md`,
`PHASE_4_BASELINE.json` and `PHASE_4_DECISIONS.md` control the Phase 4 work.
Step 1 records approval of the plan decisions and authorizes baseline freezing,
historical-test binding and active maintainer checks. It opens no runtime module
or report schema. All forty runtime modules, their version `0.1.0.dev2`, the
mathematical inputs and the existing report schema retain their accepted bytes.

The three maintainer checkers select Phase 4 explicitly with `--phase 4 --step 1`.
The traceability and specification checkers first apply the Phase 4 control and
frozen-source verification, then call their unchanged historical checks. Their
argument-free entry points and original Phase 3 functions/constants remain
available. No global Phase 3 active-step constant is repurposed. Historical
tests that depend on an earlier stage bind only to the independently verified
final Phase 3 snapshot under the plan's exact migration inventory; the earlier
Step 10 snapshot keeps its identity and purpose.

The active control rejects unauthorized path changes, altered formula/oracle
bytes, premature runtime behavior and forged stage permission. Workflow roles
select the active phase while retaining their platform/dependency matrices,
read-only permissions and historical verification. Step 1 is a development
governance checkpoint. Canonical report contracts, redaction, renderers, result
assembly, output writing and an operational audit CLI remain later authorized
steps; no Phase 4 completion or publication is implied.


## Phase 4 Step 2: canonical report contracts

The Theory Owner authorized Step 2 with `批准，开始 **Phase 4 Step 2**`.
This step opens only `result.py` for report-local immutable structures and
validation. The other thirty-nine runtime modules retain their accepted bytes,
including all input, calculation, command, assembly and renderer bodies. The
forty-module layout and existing dependencies remain fixed.

`CanonicalReport.from_dict(...)` validates the explicit public contract before
constructing a deeply immutable report. `to_dict()` returns an independent
mutable export in the twelve-section order. The contract distinguishes the five
report evidence classes from the inherited calculation enum. Evidence placement,
finite typed values, required metadata, null reasons, denominator/scope context
and capability input/execution statuses are checked before rendering can exist.
The canonical capability matrix and its compatibility mirror must agree.

The strict local report schema and `docs/report_schema.md` register each permitted
public field. Runtime validation uses the standard library; the schema validator
remains a test dependency. Semantic cross-field checks supplement JSON Schema,
including mirror equality and interval consistency. No input ingestion, metric
calculation, report assembly, privacy transformation or user-facing report output
is introduced by this step.

Historical Phase 3 and Phase 4 Step 1 functions and test assertions remain
available on their pinned source snapshots. Dedicated current Step 2 gates check
the opened result contract and every still-frozen module. Step 2 permissions are
independent of the editable control file and do not authorize Step 3. Actual
execution, commit identities and workflow outcomes are recorded in the external
Step 2 receipt; Phase 4 remains incomplete.


## Phase 4 Step 3: explicit evidence assembly

The authorized assembly module consumes accepted validation and calculation
contracts and constructs the frozen Step 2 canonical report. Each adapter names
its public fields explicitly, retains the supplied result's scientific owner and
evidence class, and checks its scope, representation, metadata and availability.
It performs no ingestion, classification, metric, graph, simulation or file
operation. Calculations are completed by their existing owners before assembly.

Input eligibility and actual execution remain independent. Available lineage
inputs never imply that Phase 5 graph work ran. Supplied scenarios remain
experimental simulation evidence; ordinary assembly does not request them.
Family failures preserve useful compatible evidence and remain visible as
structured errors with the affected execution family.

The Step 3 maintainer boundary freezes result.py, all five root schemas, the
other 38 runtime modules, dependencies, Hero fixtures and mathematical oracles.
Historical gates retain their accepted snapshot semantics; active Step 3 gates
check the current source separately. Privacy transformation, rendering and CLI
analysis remain assigned to their later approved steps.

## Phase 4 Step 4: explicit privacy views and safe diagnostics

The Step 4 boundary is the accepted Step 3 commit
`974545c456e535ba1e1c5b6bf4ae0ce25bc04b57`. Five existing runtime modules may
receive privacy, configuration, run-metadata and diagnostic additions:
`result.py`, `reports/assembly.py`, `config.py`, `utils/hashing.py` and
`utils/logging.py`. The other 35 runtime modules, all five root schemas, six
canonical Hero files, calculation kernels and mathematical expectations retain
their accepted bytes. The module set, dependencies and package version are
unchanged. Earlier helper bodies, canonical validation and evidence assembly
remain callable with their inherited behavior.

An explicitly requested privacy view consumes an already assembled immutable
canonical report. It does not reload input, classify records, calculate metrics,
infer ancestry or activate a renderer. Standard output removes unsafe free text
and content-bearing metadata. Redacted output additionally protects nested
identities and removes paths, source/evidence URIs and raw content hashes.
Record-ID preserve/hash/omit selection is restricted to record identifiers;
it does not permit raw content, paths, notes or secrets. Domain-separated
HMAC-SHA-256 pseudonyms use an explicit context. Fresh default keys have run
scope; an explicit local secret file permits cross-run consistency. Neither key
material nor its file path is report metadata.

The Phase 4 configuration adapter leaves the Phase 2 resolver and input pipeline
unchanged. Safe summaries, normalized configuration hashes and reconstructed
commands expose approved option meaning without dumping the full configuration
or argv. Diagnostic formatting retains severity and registered codes while
replacing unsafe caller text. Sinks require explicit invocation and consume
privacy-safe diagnostics. An inherited debug label does not enable raw logging.

The Step 4 maintainer checker preserves all historical source definitions and
uses a new source-segment check that splits each source once. This is an additive
implementation of current preservation checks; prior stage checkers keep their
accepted bodies. Historical Step 3 test identities are reconciled in addition to
the prior identity chain. Installed-wheel checks exercise canonical assembly,
privacy views, configuration and diagnostic formatting, with analytical calls,
input operations, file access and network blocked during the privacy transform.
The four workflow roles retain the full operating-system, Python and dependency
matrix, real optional Parquet, and the 60-minute core-job budget.

Step 4 does not implement JSON/Markdown rendering, output transactions, the audit
CLI or a product performance certification. Identifier protection does not
assert statistical anonymity or suppress small cells.

## Phase 4 Step 5: pure JSON and Markdown rendering

The Step 5 boundary is accepted Step 4 commit
`49454a9b162cb8d35e38d1cb1ae32cb208d3a01c`. Only the two existing renderer
modules gain runtime behavior: `reports/json_report.py` and
`reports/markdown_report.py`. The other 38 package modules, all five root
schemas, calculation owners, six canonical Hero files and mathematical oracle
bytes retain their accepted identities. Package version, dependencies and the
40-module layout remain unchanged.

The explicit sequence is calculation, canonical assembly, privacy selection,
then rendering. `render_json(view)` and `render_markdown(view)` each accept an
exact `SafeReportView`, revalidate its detached canonical data and return a
string. A raw `CanonicalReport`, mapping or subclass is rejected. Neither
renderer selects a privacy mode or creates a pseudonym key. The existing safe
view is a programming boundary, not a sandbox against a Python caller that
deliberately reconstructs its private objects.

Both formats preserve all twelve sections and the same analytical fields,
units, scopes, denominators, availability, evidence classes and supplied numbers.
JSON keeps the required top-level order, sorts nested mapping keys and retains
array order. Markdown presents one capability matrix and identifies the
observability compatibility copy as that same matrix. Existing sequence order
is retained for state/probability pairs, comparison directions, simulation
trajectories, diagnostics and metadata recommendations. Rendering never sorts
one member of a parallel sequence independently or recalculates its values.

Markdown separates fixed toolkit headings and explanations from quoted literal
data. Its field paths encode dynamic keys without treating a caller label as a
heading, link, HTML element or assertion. Displayed numbers use round-trip
representations, preserving tiny nonzero values, exact integers and supplied
interval endpoints. Null values remain visibly unavailable with their retained
reason context. JSON remains the authoritative machine-readable artifact.

Rendering is an explicit, standard-library-only, in-memory operation. It does
not read files, resolve input references, import numerical owners, run a metric,
sample a scenario, traverse a graph, call a network or write to a stream.
Output destinations and publication transactions remain assigned to Step 6;
CLI analysis and packaged examples remain assigned to their later steps.
The HTML placeholder remains unchanged. No report-length performance target or
whole-product acceptance follows from this renderer boundary.

## Phase 4 Step 6: local report publication

This increment adds `utils.paths.publish_reports` and the frozen `PublicationResult`
value to consume a SafeReportView. It reuses the accepted pure JSON/Markdown
renderers; it performs no loading, analysis, hashing of source content or network
access. Inputs are explicit path reservations. A private staging directory lives
inside the explicit output directory, which keeps publication on the same
filesystem. Both payloads finish before either final name is created.

The publisher returns one of `complete`, `failed` or `incomplete`, with a fixed
code, exit code, fixed-name publication/residual lists and a temporary cleanup
flag. `published_files` records successful publication calls even if rollback
subsequently removed the files. `residual_files` records fixed names whose
attempt-related cleanup cannot be confirmed; it is not a directory inventory.
A competing target that prevented publication is preserved and is not claimed
as this attempt's residual file. `incomplete` also covers uncertain staging cleanup.
Caller-directed diagnostics are in `utils.logging`; no global logger or stream
is installed. Operational publication data stays outside the canonical schema.

Inherited helpers remain byte-preserved except module ownership documentation.
The two output modules are the only runtime changes in this step. CLI wiring
belongs to the separately authorized next step. See `privacy.md` for filesystem
limits and `cli.md` for the helper contract and safe failure handling.


## Phase 4 Step 7: single-version CLI orchestration

`cli.py` lazily dispatches `audit`/`validate` into accepted input, calculation,
assembly, privacy and safe paired-publication APIs. It owns call order and exit
precedence, and introduces no formula. `config.py` adds only local control loading
and effective validation settings. Prior configuration functions remain intact.
Control bytes are read once, and their inventory is retained with the bundle.

Calculation families return typed results or recorded failures. Independent
families can survive and produce a partial report. Validate bypasses every
calculation and clears analytical sections before canonical revalidation.
All sinks consume the accepted protected report view or fixed operational
publication diagnostics. Console path disclosure follows the selected privacy
mode. No comparison, packaged resources, simulation, weights or general lineage
work is enabled. The runtime module count remains 40 and the report schema stays
unchanged. Help/version preserve the lazy, dependency-free startup boundary.


### Phase 4 Step 8: one explicit pair and installed example

CLI selects one version per explicit records role and calls the accepted T1
comparison kernel with retained order and shared literal meaning. Later-version
provenance uses the existing scoped join; no mathematical or graph owner changes.
The example extracts exact package resources with importlib.resources into a
fresh workspace and calls the same audit path. Only CLI and additive config code
open; 38 other runtime modules and all five schemas remain frozen. Package data
contains six unchanged Hero files and the exact report schema, with 40 Python
modules and unchanged dev2/dependencies. Full longitudinal orchestration and
lineage remain deferred. Step 8 gates enforce resource equality and package-data
only changes, with installed wheel and extracted sdist offline checks.
