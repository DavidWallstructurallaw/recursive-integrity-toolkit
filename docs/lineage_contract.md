# Phase 5 Lineage Contract

Status: **approved implementation target, fixed in Phase 5 Step 1**.

Authority: [Phase 5 decisions](../PHASE_5_DECISIONS.md), approved Phase 5 plan,
`PROJECT_INSTRUCTIONS.md` section 4.4 and the approved UD decisions. Relevant
frozen owners are T4, T6, PR-008, PR-009 and T3 lineage bounds. The original
definitions/specifications remain unchanged.

This document defines interfaces for Steps 2-8. Step 2 implements retained batch
parent evidence and `build_lineage_graph` with immutable scope, adjacency and
node/edge limits. Step 3 adds `analyze_cycles` for iterative cycle detection,
unaffected topology and structural depth. Step 4 adds `analyze_lineage` for
external-root resolution, G/C/U counts and coverage. Step 5 adds root incidence,
fractional mass and ancestry concentration. Step 6 adds explicit lineage closure
and shared-root proxy calls. Step 7 integrates explicitly supplied lineage
results into schema 1.1, canonical assembly and privacy-safe JSON/Markdown.
CLI lineage invocation and context input options remain Step 8 targets.
The package remains at
`0.1.0.dev3`; the executable report schema is `1.1`.

## 1. Scope and reference semantics

Canonical identity is the existing `RecordKey(dataset_version, record_id)`;
transport spelling is `version::id`. Compare keys using their two string fields
in that order. Records in the primary version define the target population N.
Loaded comparison/context records support the graph without changing N.

`LineageScope` has these immutable fields:

| Field | Python type | Meaning |
|---|---|---|
| `target_dataset_version` | `str \| None` | Explicit selected primary version; null only when an empty input has no declared version. |
| `target_record_keys` | `tuple[RecordKey, ...]` | Unique sorted target identities; no representation eligibility exclusions. |
| `target_record_count` | `int` | N, equal to the tuple length. |
| `loaded_record_count` | `int` | Unique loaded nodes across all admitted roles. |
| `context_record_count` | `int` | Loaded nodes outside the target. |
| `loaded_dataset_versions` | `tuple[str, ...]` | Lexical inventory, not inferred chronological order. |

The target keys must be a subset of the loaded keys. Counts are nonnegative
integers and never booleans. Context versions are disjoint from primary and
comparison versions. Same-version edges are supported within a loaded primary
version; split target/context roles for one version are outside this phase.
Duplicate canonical keys across any roles fail validation.

Keep `ParentValidationResult.declaration_state` values `absent`, `null`, `empty`
and `declared`. The current generation adapter normalizes absent parent fields to null; Step 2 must recover the retained `CanonicalRow.field_states` distinction when constructing its batch result. Only `empty` explicitly declares no parents. Missing provenance
is separately identified. Reuse `ParentReference`, its canonical identity,
`source_references`, resolution status and chronology. The Step 2 batch resolver
retains a per-record result or per-record failure, original declaration counts
where knowable, and explicit self-parent evidence. It constructs one lookup
index for the batch. It never treats an ambiguous/future/invalid reference as an
accepted ancestry edge.

For each syntactically valid reference list, declared count is the original
list length, including repeated aliases. Absent/null declarations and missing
provenance have zero original reference entries; this does not establish an
explicitly parentless record. Resolved count sums the lengths of
`source_references` whose existing resolution status is `resolved`, including
known identities with unavailable chronology. Graph edge admission separately
requires known chronology. Unresolved reference count is
declared minus resolved and includes invalid references whose entries can be
counted. A malformed declaration with unknown reference cardinality makes the
whole-target reference totals/coverage unavailable; retain known-subset counts
only with an explicitly named subset. Never turn malformed input into zero
declared parents.

Graph adjacency deduplicates canonical edges. Grounded carryover with two
spellings of the same resolved parent still has one parent. An additional
unresolved spelling that cannot resolve to that key prevents complete ancestry.
Cross-version edges require the existing declared chronology; missing chronology
cannot certify a resolved required path. Same-version edges require cycle
analysis. Default missing-parent warnings and existing strict-mode error
promotion remain unchanged. Ambiguity, future-parent and cycle errors remain
errors.

## 2. Computation ownership and immutable targets

The target high-level computation entry is:

```python
analyze_lineage(
    validation: BundleValidationResult,
    *,
    target_dataset_version: str | None,
    limits: LineageLimits = LineageLimits(),
) -> LineageAnalysisResult
```

`validation` supplies retained record, provenance, chronology and parent evidence
after the Step 2 retention refactor. It must cover context as well as target
records. Selection is explicit, revalidated and independent of ordinary metric
eligibility. `validate_bundle` remains input-only and never calls this function.
CLI orchestration calls it only after an explicit lineage request.

Steps 4-5 implement this direct API for root resolution, coverage and concentration. Its
`LineageAnalysisResult.records` contains target records in canonical order;
context roots are intermediate computation data and do not enter target
denominators. The existing `ExecutionStatus` vocabulary applies. Step 6 derives
bounds and the descriptive proxy through separate explicit calls over that
typed result; `analyze_lineage` does not invoke either automatically.

Graph admission failures retain the existing `LineageResourceLimitError` before
a valid analytical result can be created. A root-membership or union-work
failure after graph/cycle analysis returns a failed result with root records,
G/C/U counts and root coverage unavailable. Completed cycle/depth observations,
original-reference coverage and exact consumed-work counters survive. No partial
root traversal is converted into an exact target partition.

Step 2 supplies the lower-level input-only handoff in `models.py`:
`ParentRecordValidation` retains provenance presence, an optional
`ParentValidationResult`, declared/resolved/self-reference counts and diagnostics;
`ParentBatchValidationResult` covers every loaded key in canonical order.
`io.validation.resolve_parent_batch` shares reference interpretation with the
existing fail-fast resolver and creates one identity lookup per batch.
`BundleValidationResult.parent_validation` is an appended optional field for
source compatibility. Graph construction requires this retained evidence and
revalidates it against the canonical inputs, rejecting stale or forged handoffs.

`lineage.graph.build_lineage_graph(validation, *, target_dataset_version, limits)`
constructs the immediate graph only. When explicit primary record roles exist,
the selected version must be that primary version. Context-only typed inputs can
represent an empty target with no declared version; an explicit empty version
must be present in the declared version order. Input loading and its limits stay
independent of graph limits. Root-membership and union-work limits are reserved
for the later ancestry implementation.

Ownership stays in existing modules:

| Module | Typed handoff and responsibilities |
|---|---|
| `lineage/graph.py` | `LineageGraph`: scope, sorted node keys, deduplicated immutable `parents_by_child` and `children_by_parent`, retained per-record reference/declaration evidence, invalid-self-reference evidence and validation messages. |
| `lineage/cycles.py` | `CycleAnalysis`: cyclic components, member keys, affected descendant keys, topology for unaffected nodes and structural depth assessments. Iterative algorithms only. |
| `lineage/ancestry.py` | `RecordAncestry`, `RootContribution`, `LineageAnalysisResult`; complete root resolution, G/C/U partition, root incidence/mass and concentration. `SharedAncestryDependence` describes shared-root evidence. |
| `metrics/bounds.py` | `LineageClosureExposureBounds` from the typed G/C/U counts, preserving the direct-bound branch. |
| `result.py`, `reports/assembly.py` | Validate/assemble supplied typed results, scope/status metadata and canonical schema 1.1 values. No graph traversal or metric recomputation. |
| `reports/json_report.py`, `reports/markdown_report.py` | Render the same privacy-safe canonical result. No computation ownership. |

All result objects use frozen typed data. Sequences are tuples; sets of roots are
frozensets; mappings are detached read-only mappings whose contents are also
immutable. Raw row content, raw URIs and local paths are not copied into ancestry
results. Invalid handoffs are rejected instead of silently trusted.

`RecordAncestry` contains `record_key: RecordKey`,
`classification: Literal["grounded", "closed", "unresolved"]`,
`external_root_keys: frozenset[RecordKey] | None`,
`reason_codes: tuple[str, ...]`, `lineage_depth: int | None`, and
`depth_reason_codes: tuple[str, ...]`. A null root set means unresolved; an empty
frozenset means complete known-empty ancestry. Unknown and empty never collapse
into the same value. Complete records have no root-resolution failure reasons.
Internal complete sets are bounded by the resource budget and are not exported
as a full transitive-closure table.

`RootContribution` contains `record_key: RecordKey`, `incidence_count: int`,
`incidence_share: float`, `incidence_denominator: int`, `fractional_mass: float`,
`normalized_weight: float`, and `weight_denominator: int`. Runtime values must be
finite. Independent fixture expectations use exact fractions where possible;
deterministic numeric reduction uses canonical target/root order.

Step 5 returns all `root_contributions` in decreasing incidence order, with
canonical root-key ties. Its aggregate fields are
`distinct_external_root_count`, `ancestry_concentration_hhi` and
`effective_external_root_count`. These computations precede the Step 7 detail
limit; the direct result does not truncate the root distribution.

Read-only `root_metrics_status` and `concentration_status` properties use the
existing `ReportStatus` vocabulary. A completed partition has available root
observations when U=0 and partial observations when U>0. A G-only concentration
uses that status when G>0; existing G/N coverage and contribution denominators
disclose its conditional population. With G=0, the contribution tuple is empty
and the distinct-root count is zero, while concentration is unavailable with
`concentration_reason_codes=("NO_RESOLVED_EXTERNAL_ROOTS",)`. A root-resource
abort instead makes contributions and all three aggregates null, with unavailable
statuses and `LINEAGE_RESOURCE_LIMIT_EXCEEDED`. These field states remain
separate from the overall execution status and its input diagnostics.

`LineageAnalysisResult` contains `scope: LineageScope`,
`execution_status: ExecutionStatus`, `execution_reason_codes: tuple[str, ...]`,
`records: tuple[RecordAncestry, ...] | None`, `cycles: CycleAnalysis | None`,
`root_contributions: tuple[RootContribution, ...] | None`, typed counts/coverage,
concentration and depth values described below, `resource_usage: LineageResourceUsage`
and existing typed validation messages. Failed resource-dependent values are
nullable with reasons; the result never fills unprocessed records with a guessed
closed classification. A failed intermediate field uses null and its reason,
while the result identifies which computation stages actually completed.

## 3. Cycles and structural depth

The direct Step 3 entry is `lineage.cycles.analyze_cycles(graph: LineageGraph)`.
It revalidates the typed graph and returns immutable `CycleAnalysis` data without
calling loaders, generation, root propagation, metrics or rendering. Full SCC
membership, affected keys, unaffected topology and per-record depth assessments
are internal computation inputs for subsequent ancestry work. They retain all
loaded nodes. `component_details` holds at most 100 canonical component rows;
omitted component counts remain explicit. The general report detail envelope
and identity protection in section 5 belong to Step 7.

Cycle status explicitly covers accepted edges and retained self-reference
evidence. Structural input reasons and validation errors remain separate, so an
acyclic accepted subgraph does not certify rejected declarations. A detected
cycle adds `E_LINEAGE_CYCLE` even when its component is disconnected from targets.

Cycle analysis uses accepted resolved edges plus separately retained explicit
self-parent evidence. The self-edge remains invalid ancestry evidence while
permitting a truthful self-cycle diagnostic. Rejected ambiguous/future/malformed
references remain disclosed and cannot certify whole-input graph validity.

`cycle_count` is the number of strongly connected components having more than one
node or a self-loop. The method label is `cyclic_strongly_connected_components`.
Components are ordered by their smallest canonical member. Members are the nodes
inside those components; affected records are the union of members and their
descendants along parent-to-child edges. Report total and target counts for both
sets. A disconnected loaded cycle remains detected even if no target descends
from it.

A cycle witness is a closed directed sequence whose adjacent keys are actual
parent-to-child edges. Use a deterministic canonical-neighbor traversal within
each component. For a self-loop it is `(key, key)`. Return a witness only if it
contains at most 64 edges; otherwise return null with
`witness_reason="diagnostic_limit"`. A bounded search that does not find a short
witness may omit it; absence of a witness does not erase an SCC-based finding.
Do not enumerate all simple cycles or store every ancestry path.

Depth is the maximum number of structural edges from a record to loaded,
explicitly parentless records, provided every required structural path is valid
and complete. Such a parentless node has depth zero even when its grounding is
unknown. A missing/invalid edge, unavailable parent declaration/chronology or
cycle on a required path makes depth null. Unknown grounding alone prevents an
exact external-root set but does not invalidate an otherwise complete structural
depth. Generation remains its existing non-grounding step count; it is not depth.

`lineage_depth` is the whole-target maximum and is null for an empty target or
when any target depth is unavailable. `maximum_resolved_target_depth` and
`depth_resolved_record_count` may separately describe the complete-depth subset;
the former is null if that subset is empty. A subset maximum must not occupy the
whole-target field.

## 4. External roots, coverage and values

An explicit parentless grounded-yes record supports itself with root set `{key}`.
Strict ancestry still excludes self. Explicit parentless grounding-no produces a
known-empty set. Grounding-unknown, missing required provenance, conflicting
declarations or an undeclared boundary produces an unresolved set.

Conflicts here concern grounding or required ancestry, as defined in frozen
`DEFINITIONS_AND_UNITS.md` section 5.8. Record/provenance `batch_id` or `timestamp`
differences remain separate metadata observations under
`DATA_AND_PROVENANCE_SPEC.md` section 9.12; they do not alone invalidate roots.
Provenance-specific declarations retain their manifest authority. Labels, URI
spelling and metadata disagreements do not introduce inferred grounding values.

A grounding-yes carryover with exactly one deduplicated resolved canonical parent
inherits the parent's set. Any unresolved additional declaration blocks it.
Other grounded-with-parent forms, including multi-parent grounded carryover,
remain unresolved under `GROUNDED_PARENT_RULE_UNSUPPORTED`. Evidence labels and
URIs do not mint independent roots. A new external input is a separately loaded,
explicitly parentless grounded anchor linked as an ordinary parent; actual child
grounding must never be relabeled to fit the supported rule.

Grounding-no descendants union their parents' complete unique root sets. Unknown
grounding anywhere on a required path propagates unresolved ancestry. Every
required branch must resolve; observed roots on incomplete branches are excluded
from exact incidence and mass. Cycle-affected records remain unresolved. Topology
and roots are never inferred from record IDs, filenames or semantic content.

For complete nonempty-root targets G, complete empty-root targets C and unresolved
targets U, `N=G+C+U`. The report field contracts are:

| Field under `derived_metrics.lineage` unless stated | Type of envelope value | Exact meaning |
|---|---|---|
| `grounded_record_count` | integer | G, targets with complete nonempty roots. |
| `closed_record_count` | integer | C, targets with complete known-empty roots. |
| `unresolved_record_count` | integer | U, targets with incomplete/invalid ancestry. |
| `records_with_resolved_external_ancestry` | integer | G+C, including known-empty sets. |
| `resolved_lineage_coverage` | number or null | `(G+C)/N`. |
| `external_ancestry_coverage` | number or null | `G/N`. |
| `resolved_parent_edge_coverage` | number or null | Accepted resolved original target references / declared original target references. Exact zero declared count yields 1.0. |
| `distinct_external_root_count` | integer or null | Unique roots in the union over G, zero when the complete partition has G=0. |
| `top_shared_ancestors` | detail object or null | Bounded `RootContribution` rows, descending incidence then canonical key; despite the inherited name, roots with incidence one remain eligible. |
| `ancestry_concentration_hhi` | number or null | `sum((M_a/G)**2)`, where `M_a=sum(1/len(A_r))` over complete grounded targets containing a. |
| `effective_external_root_count` | number or null | Reciprocal HHI. |
| `lineage_depth` | integer or null | Exact whole-target maximum structural depth. |

`no_declared_parents: bool` accompanies executed reference coverage. It is true
only when the exact total is zero. With lineage not requested, retain schema
1.0's immediate-validation observation semantics and its null ratio for zero
references; do not manufacture an executed coverage value.

Root incidence shares divide by N; normalized fractional weights divide by G.
Each target in G contributes total fractional mass one. Multiple paths or alias
declarations do not multiply mass. Concentration is computed from all complete
root contributions before report-detail caps or redaction. If U>0, quantities
restricted to G carry partial status and explicit G/N coverage, even when their
conditional values are exact. No completeness of excluded targets is implied.

Existing closure fields stay at
`derived_metrics.closure_exposure.lineage.{lower_bound,upper_bound,interval_width}`
with values `C/N`, `(C+U)/N`, `U/N`. G/C/U counts must cover all targets before
these values are emitted. A resource-aborted partial traversal provides no such
partition and therefore no numeric bounds. A fully classified unresolved record
may contribute to U and the conservative bound without having an exact root set.

When N=0, counts are zero, version remains explicitly declared or null, and all
population ratios/bounds are null with `EMPTY_TARGET_SCOPE`. Distinct roots are
zero after successful empty analysis; HHI/effective roots are null with
`NO_RESOLVED_EXTERNAL_ROOTS`. When N>0 and G=0, those concentration fields remain
null with that reason, including all-closed and all-unresolved cases. No infinity,
NaN, fake version or zero-valued unavailable concentration is allowed.

`proxy_signals.shared_ancestry_dependence` retains the current proxy vocabulary:

| Condition | `status` | `level` |
|---|---|---|
| Some exact root incidence >=2, U=0 | `available` | `present` |
| Some exact root incidence >=2, U>0 | `partial` | `present` |
| N>0, U=0, every exact root incidence <=1 | `available` | `not_present` |
| N=0, incomplete evidence without a witness, or resource failure | `unavailable` | `indeterminate` |

The proxy cites actual root/incidence and coverage fields. Topological allocation
does not certify causal contribution, semantic error, independent information,
biological relatedness, universal diversity, integrity or collapse. T4 retains
its theory-guided operationalization label; T6 is an engineering graph-validity
rule. Existing unavailable scientific conclusions remain explicit.

### Step 6 direct calculation interfaces

`metrics.bounds.lineage_closure_exposure(result)` returns immutable
`LineageClosureExposureBounds`. Its only stored field, `source`, is a revalidated
`LineageAnalysisResult`, excluded from the wrapper representation. Scope, target
G/C/U counts, denominator, coverage, unresolved reasons and input diagnostics
remain accessible without copying another record or root table. `lower_bound`,
`upper_bound` and `interval_width` expose the three ratios as floats or null.

The interval's `status` is `available` for a completed nonempty target partition,
including U>0 and the all-unresolved interval `[0,1]`. This status describes the
conservative interval. Input execution status, errors and unresolved reasons
retain their separate meaning. Empty scope yields unavailable values with
`EMPTY_TARGET_SCOPE`; an aborted root traversal yields unavailable values with
`LINEAGE_RESOURCE_LIMIT_EXCEEDED`. The original direct-bound functions preserve
their formulas, classifications and input-only dependency behavior.

`lineage.ancestry.shared_ancestry_dependence(result)` returns immutable
`SharedAncestryDependence`, retaining one revalidated `source` and deriving the
status/level table above. A positive witness is the first already ranked
`RootContribution` with incidence at least two. The proxy exposes actual
incidence and coverage field references, target scope and source diagnostics.
It adds no calibrated severity, risk threshold or causal conclusion. Both calls
consume already computed ancestry and perform no graph traversal, ingestion,
report rendering or network/file access. Step 7 serializes these explicitly
supplied results without invoking either calculation automatically.

## 5. Schema 1.1 placement, detail bounds and privacy

Step 7 changes every current output to report schema 1.1, including requests
without lineage. Strict 1.0 readers must adopt the new schema. Preserve the twelve
top-level sections, existing envelopes and all non-lineage numerical meanings.
Root and packaged report schemas must agree. No migration-loader framework is
introduced.

The implemented `assemble_report` keywords are `lineage`, `lineage_bounds` and
`shared_ancestry`. Bounds and proxy handoffs require their matching explicit
lineage source. Assembly checks exact target/context scope and a private
computation-owner input signature against retained declarations, policy and
diagnostics, rejecting stale same-identity results. This consistency check does
not authenticate a hostile Python caller. It does not rerun graph traversal or
the root/concentration kernel, and the private signature is never reported.

Without a lineage result, execution is `not_requested` and immediate-validation
observations retain their limited meanings. An explicit existing
`FamilyFailure(CapabilityKey.LINEAGE, ...)` can report a failure before graph
admission; it supplies no completed graph or root observations. Root-resource
failures with a typed result retain completed graph/depth/reference observations
and consumed-work counters. A separate family failure cannot contradict a
supplied lineage result. Step 8 owns CLI dispatch and graph-admission exception
orchestration.

New observed fields are `observed_facts.lineage.graph_scope` (the public scope
counts/version inventory), `cycle_analysis`, `depth_summary`,
`unresolved_record_details`, and `resource_usage`. Existing declared/resolved/
unresolved parent counts remain in their current observed locations.
`cycle_status` remains `acyclic` or `cyclic` when a completed graph check can
establish that value; its scope and reasons disclose rejected declarations.
An acyclic accepted-edge subgraph never certifies validity of rejected input.
Incomplete graph traversal gives null/unavailable, not `acyclic`.

Every bounded collection uses this exact detail object:

```text
{
  items: tuple[T, ...] | null,
  total_count: int,
  returned_count: int,
  omitted_count: int,
  limit: 100,
  detail_status: "complete" | "truncated" | "omitted",
  omission_reasons: tuple["diagnostic_limit" | "redacted_identity_details", ...]
}
```

`total_count=returned_count+omitted_count`. For visible detail, `items` is an array,
`returned_count=len(items)`, and at most 100 items appear. Complete detail has zero
omissions/reasons, including an empty array. Truncated detail has positive
omissions and `diagnostic_limit`. Privacy omission uses `items:null`, returned
zero, omitted equal to total, status omitted and reason
`redacted_identity_details`. Applying privacy to a previously capped collection
retains that diagnostic-limit reason when applicable. These presentation counts
do not change analytical status or denominators.

`cycle_analysis` includes `detected: bool`, `cycle_count: int`,
`counting_method: "cyclic_strongly_connected_components"`, total/target member and
affected counts, and three bounded collections: `components`,
`cycle_member_record_keys`, `affected_record_keys`. Component rows contain
`component_index: int` (one-based canonical order), `member_count: int`,
`target_member_count: int`, `witness_record_keys: tuple[RecordKey,...] | None`,
`witness_edge_count: int | None`, and
`witness_reason: Literal["diagnostic_limit"] | None`. A returned witness is closed
and has at most 65 keys; omitted witness edge count is null. The detail object
around components provides the privacy omission shape for the entire row list.

`unresolved_record_details` rows contain only `record_key` and sorted unique
`reason_codes`, ordered by canonical key. Root rows are the seven fields in
`RootContribution`. `depth_summary` contains `depth_resolved_record_count`,
`maximum_resolved_target_depth` and the explicit target count. No arbitrary
message, URI, path or content payload is admitted into these shapes.

Standard mode preserves declared structural identities and record IDs.
Redacted mode supports record-ID `hash` (default), `omit` and explicit `preserve`;
record-ID overrides require redacted mode. In redacted/hash,
dataset IDs, root keys, witness keys and dynamic identities use the existing
scoped HMAC mechanism consistently; sort/rank before privacy transformation.
In record-ID omit mode, each identity-bearing collection uses its whole-list
omission variant. Never remove a required `record_key` while retaining an invalid
row. Aggregate values, counts, severity and execution status remain visible.
Redacted/preserve retains only declared record-ID fields while dataset versions
and other protected identities still use their existing transformation. Both
renderers consume the same schema-valid safe result.

## 6. Resource and invocation interfaces

`LineageLimits` has four required positive integer fields with these defaults;
the existing `ResourceLimits` gains corresponding configuration fields when
the configuration integration is implemented:

| `LineageLimits` field | `ResourceLimits` / JSON `resource_limits` field | Default |
|---|---|---|
| `max_nodes` | `max_lineage_nodes` | 200000 |
| `max_edges` | `max_lineage_edges` | 1000000 |
| `max_root_memberships` | `max_lineage_root_memberships` | 1000000 |
| `max_root_union_visits` | `max_lineage_root_union_visits` | 10000000 |

Defaults apply only to explicitly requested lineage. A supplied override is an
exact integer greater than zero; bool, null, fractional, infinite and nonpositive
values are invalid. Existing input byte/row/parent-list/depth limits remain
independent and retain their existing optional semantics.

Check cumulative node admission across all batches before graph materialization,
unique-edge admission before insertion, stored membership before storing each
new `(record, root)` association, and union work before each candidate root visit.
A union visit is processing one parent's candidate root into a child's union,
including a candidate already present there. An anchor self-membership consumes
one stored membership and zero union visits. Shared immutable set storage may
reduce actual memory but does not reduce the logical membership accounting.

`LineageResourceUsage` contains `admitted_node_count`, `admitted_edge_count`,
`stored_root_membership_count`, `root_union_visit_count`, `limits: LineageLimits`,
and `exhausted_limit: str | None`. On exhaustion, include
`attempted_value: int | None` for the rejected next admission/visit, stop dependent
work, and emit a typed error with `LINEAGE_RESOURCE_LIMIT_EXCEEDED`. Distinguish
these operational reason codes from the existing `ErrorCode` namespace; add the
smallest needed error constant during implementation without renaming existing
errors. A successfully completed earlier stage may retain its exact observations,
but no truncated partition, root distribution or bound is reported as exact.
Independently completed non-lineage families survive.

Iteration order for budgeting is canonical nodes, canonical parent keys and
canonical root keys. Budget exhaustion must be deterministic for permuted input.
Limits bound defined work units, not peak RSS, loader allocations, decompression
or scientific thresholds. Step 9 measures actual time/RSS and may propose an
explicitly documented limit adjustment. It must not silently raise limits to
turn a failing check into a pass.

The future inert configuration field is `ResolvedConfig.lineage: bool = False`,
serialized as top-level `lineage: false` when explicit. The dedicated input role
is `FileRole.LINEAGE_CONTEXT` with value `lineage_context`; it permits repeated
existing local input declarations. Preserve all existing multi-role Python/config
behavior. Config resolution neither reads inputs nor starts analysis.

`audit --lineage` and `example --lineage` enable computation. Repeatable
`--lineage-records PATH` supplies context to audit only with lineage enabled.
`validate` may ingest a configured/context input role for input/reference
validation, but rejects any true lineage execution request. Ordinary metric calls
select the primary version explicitly. Context does not request comparison,
trajectories, simulations or network access. Existing CLI comparison stays one
explicit earlier input; broader Python/config multiplicity stays unchanged.

## 7. Execution and error states

Input observability stays separate from actual computation. Completed/partial
execution names performed operations. All other execution states have explicit
reasons. Use these rules in order:

| Situation | Lineage execution | Value handling |
|---|---|---|
| No explicit request | `not_requested` | No graph execution claim; ordinary validation evidence may remain. |
| Fatal admission/resource failure | `failed` | No exact result from incomplete stages; earlier completed observations and other families may survive. |
| Invalid graph/input, with useful unaffected target results | `partial` | Preserve errors, complete subset values and precise target coverage. |
| Invalid graph/input, with no usable target ancestry result | `failed` | Preserve valid diagnostics; exact root metrics unavailable. |
| No lineage error, with U>0 | `partial` | Complete partition/bounds may be available; G-only metrics disclose partial coverage. |
| No lineage error and U=0, including a successful empty analysis | `completed` | Defined values available; empty-denominator metrics remain unavailable. |

A disconnected loaded cycle remains a lineage error even with complete target
ancestry. Missing parents promoted by strict mode follow the error rows; ordinary
missing-parent warnings follow the unresolved-coverage row. A known all-closed
target can complete successfully while HHI remains unavailable. Root uncertainty
does not erase independently valid graph observations.

Existing run-status behavior is preserved: fatal errors fail the run; other
errors yield partial when useful evidence survives and failed otherwise.
Warnings alone retain their existing run-status behavior. Any surviving lineage
error produces a non-success CLI audit exit under the existing error policy.
Redaction and capped detail do not themselves turn completed analysis into
partial execution.

## 8. Direct verification and completion boundary

Independent fixture expectations cover the frozen Hero, rational multi-root
allocation, missing and unknown branches separately, carryover aliases, known
empty versus unknown ancestry, empty targets, disconnected cycles, affected
descendants and target/context isolation. They describe future behavior and are
not successful runtime results in Step 1.

Implementation checks protect those behaviors directly. New graph boundaries
receive bounded adversarial/resource cases. Candidate verification retains the
supported OS/Python/dependency and packaging gates. The actual 100k sparse lineage
measurement runs on the designated reference profile; ordinary step checks do
not repeat a release matrix. Historical behavior is consolidated under P5-D11,
without new source-body chains or evidence-of-evidence frameworks.

No automatic longitudinal analysis, new independent-input evidence schema,
causal weighting, semantic inference, HTML implementation or theory-source change
is authorized by this contract.
