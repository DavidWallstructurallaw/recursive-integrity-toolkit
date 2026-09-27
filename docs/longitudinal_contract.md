# Longitudinal comparison contract

Status: **APPROVED CONTRACT; STEP 3 DISTRIBUTION ANALYSIS IMPLEMENTED**.

Authority: `PHASE_6A_PLAN.md`, P6A-D01 through P6A-D08, and
`PHASE_6A_DECISIONS.md`. Existing definitions and Phase 3-5 meanings remain in
force. This document fixes the staged interfaces. Current package dev4 and
schema 1.1 implement Python selection, compatibility and the Step 3 distribution
analysis portion. Provenance/direct-closure changes, selected lineage, config/CLI
and public series reports remain future work. Implementation clarifications are
recorded in `PHASE_6A_DECISIONS.md`.

## 1. Scope and ownership

The record-based series compares at least two explicitly selected, ordered
snapshots. Its required families are `distribution`, `provenance` and
`direct_closure`. Optional families are `tail` and `lineage`. A source manifest
is optional input; its absence is missing evidence in a requested provenance
analysis. Lineage and tail must be explicitly requested. Simulations never run.

| Concern | Owner |
|---|---|
| Selection, order, pair schedule | PR-007, PR-011; `metrics/longitudinal.py` orchestrates existing validation |
| Representation and mappings | T1, PR-011; existing representation/compatibility modules |
| Support, diversity, observed change | T1; `metrics/diversity.py` and the longitudinal coordinator |
| Earlier-tail disappearance | T2; existing tail selection plus T1 pair state sets |
| Provenance/coverage | PR-004, PR-005; existing provenance joins and metrics |
| Direct and lineage closure bounds | T3; `metrics/bounds.py` |
| Shared graph and selected ancestry | PR-008, T6, T4; existing lineage modules |
| Public schema, rendering and privacy | PR-012 through PR-016; existing result/report owners |

All numerical differences are `derived_metric`, measured as later minus earlier
under F-018 in the endpoint unit. Support delta retains its specific method
`F-005`; the other new deltas use `F-018`. Snapshot values preserve their current
evidence classes and owner methods. Set differences/intersections retain their
explicit T1/T2 methods. No relative changes, fitted trend or composite score is
added. Missing evidence never becomes a measured zero.

## 2. Configuration and CLI contract

### 2.1 New fields

Add top-level `longitudinal` as an inert object. Unknown keys are rejected.

| Key | Type/default | Rule |
|---|---|---|
| `enabled` | boolean, default `false` | Only explicit true requests series execution in audit/example. |
| `baseline` | `none` or `first`, default `none` | Requests adjacent pairs plus optional first-baseline pairs. |
| `state_semantics` | nonempty string, optional | Common declaration for all selected versions in common mode. |
| `versions` | array, default `[]` | Per-version declarations in heterogeneous mode; exact selected-version coverage required. |
| `mappings` | array, default `[]` | Directed declarations for explicitly requested pairs only. |

Add `resource_limits.max_longitudinal_versions`, default 100, a positive built-in
integer. Reject boolean, null, fractional, nonfinite and nonpositive values.
Existing input/lineage limits keep their fields, defaults and independent units.
Do not accept a mapping file URL, callback, dotted Python name or executable rule.

A nonempty `longitudinal` object may carry declarations while execution is false,
as other inert configuration does; it must not trigger calculation. Audit rejects
execution-specific nondefault declarations when enablement is false, with a
configuration error rather than silently ignoring them. `validate` can check
inert declaration structure, but does not execute it even if config enablement
is true. Explicit execution flags are rejected by the validate CLI.

### 2.2 Representation modes

**Common mode:** `versions=[]`; use the existing top-level `representation` and
one common semantics declaration from `longitudinal.state_semantics` or
`--state-semantics`. Existing `--missing-state-id` supplies the common explicit
missing-state ID when required. No representation selection is inferred.

**Per-version mode:** `versions` contains exactly one object per selected
snapshot with these fields:

```text
dataset_version: canonical nonempty version string
representation: existing RepresentationConfig JSON object
state_semantics: nonempty literal string
missing_state_id: nonempty string exactly when policy is explicit_missing_state
```

The `representation` object uses existing keys `name`, `source`, `field`,
`version`, `missing_value_policy`, `normalization_profile` and current supported
values. No new representation algorithm is implied. `missing_state_id` is a
sibling because current RepresentationConfig does not contain it. Reject common
top-level representation/common semantics/common missing-state declarations in
this mode; do not silently apply precedence. Context-only or unloaded versions
cannot acquire snapshot membership through this array. Primary ordinary metrics
use the primary snapshot's explicit declaration.

Declarations are validated against the descriptor actually produced by current
representation selection. `binning_or_mapping_rule` describes that existing
method; supplying arbitrary text does not select a new algorithm.

### 2.3 Mapping declarations

Each `mappings` item is exactly:

```text
earlier_version: selected earlier version
later_version: selected later version
declaration:
  direction: earlier_to_later | later_to_earlier
  source_representation: full existing RepresentationDescriptor
  target_representation: full existing RepresentationDescriptor
  source_state_semantics: nonempty literal string
  target_state_semantics: nonempty literal string
  state_mapping: object of literal state IDs to literal state IDs
```

Descriptor keys are `representation_name`, `representation_source`,
`representation_version`, `binning_or_mapping_rule`, `field_name`,
`missing_value_policy`, `missing_state_id`, `normalization_profile`, using the
existing type/null rules. Serialize all eight keys in the full descriptor.
Mapping direction and source/target descriptors/meanings must match the actual
pair. Require totality on supplied source states, including explicit zero-mass
states. Retain existing collision/missing-state rules. No fallback identity map
or composition across pairs is allowed. Reject duplicate pair declarations and
mappings for unscheduled pairs. Legacy bare `state_mapping` and
`representation_compatibility` cannot substitute for this declaration and are
rejected when competing with series declarations.

### 2.4 CLI/input roles

```text
rit audit --records v3.jsonl --compare v1.jsonl --compare v2.jsonl \
  --longitudinal --version-order order.json --config config.json \
  --state-semantics "Literal topic meanings are shared across these versions." \
  --out new-report-directory
```

Add `--longitudinal` to audit/example. Add `--baseline {none,first}` to audit,
requiring longitudinal enablement. CLI and config declarations for the same
singleton compete even when textually equal; retain the established rejection
policy. Repeated `--compare` is accepted in longitudinal audit and input-only
validate; ordinary audit continues to accept at most one comparison input.
Append repeated comparison paths only within the selected input source; do not
combine competing CLI and config comparison-source declarations silently.

Each CLI primary/comparison file must contain exactly one nonempty version,
different from every other selected file. The primary version is latest among
selected versions. Chronology comes from accepted config/order-file declarations
or timezone-aware timestamp declarations with current tie/conflict handling.
The order of repeated CLI paths is not chronology. Existing legacy two-version
invocation ordering remains valid outside longitudinal mode.

Context inputs use `LINEAGE_CONTEXT` and remain disjoint from all selected
versions. Audit context still requires lineage opt-in. `--lineage` with a series
requests every selected snapshot's ancestry; plain series does not traverse a
graph. `validate` loads the records for current input/reference checks only.
`example --longitudinal` requests the unchanged Hero pair; adding `--lineage`
requests both Hero lineage snapshots. It uses no first-baseline default or tail
default. Standard/redacted output and exclusive output-directory rules remain.

## 3. Immutable internal interfaces

The following names/fields define the forthcoming record-series interface.
Types may reuse existing immutable leaves. Constructors and consumers validate
literal types, unique identities and binding; a caller-created object is not
proof of correctness. Step 1 added no runtime types. Step 2 implemented declarations,
mapping envelopes, scopes, pairs and selection. Step 3 adds snapshot/pair/series
results for distribution work; configuration options and later families remain
deferred.

| Type | Required fields |
|---|---|
| `LongitudinalOptions` | `enabled`, `baseline`, `state_semantics`, `versions`, `mappings`; defaults as above |
| `SnapshotDeclaration` | `dataset_version`, `representation`, `state_semantics`, `missing_state_id`, `empty_scope` (Python only, false by default) |
| `LongitudinalMapping` | `earlier_version`, `later_version`, `declaration`; Python envelope for the approved mapping shape |
| `LongitudinalSelection` | `primary_version`, `selected_versions`, `context_versions`, `version_order`, `selected_order`, `snapshots`, `pairs`, `max_versions`, `input_signature` |
| `SnapshotScope` | `dataset_version`, `population_scope`, `representation_scope`, `declaration`; scopes are existing CalculationScope objects |
| `LongitudinalPair` | `earlier_version`, `later_version`, `kinds`, `mapping`; kinds is an immutable nonempty subset of `adjacent`, `baseline` in that order |
| `SnapshotSummary` | `scope`, `distribution`, `provenance`, `direct_closure`, `lineage`, `family_statuses`, `messages` |
| `LongitudinalPairResult` | `pair`, `compatibility`, `support_comparison`, `deltas`, `tail_disappearance`, `family_statuses`, `messages` |
| `LongitudinalResult` | `selection`, `snapshots`, `comparisons`, `shared_lineage`, `execution_status`, `reason_codes`, `messages`, `input_signature` |

`snapshots`, `pairs`, result rows and diagnostics use immutable tuples; maps are
detached immutable literal mappings. `distribution`, provenance/bounds and
support comparisons reuse existing result types when present. An absent result
has its explicit family status/reasons. Series calculation is unweighted and
record-backed; the existing weighted/probability-only pair APIs stay separate.

The public computational entry points are:

```python
select_longitudinal_versions(validation, *, declarations, baseline="none",
                             max_versions=100, mappings=()) -> LongitudinalSelection
validate_longitudinal_selection(validation, selection) -> LongitudinalSelection
analyze_longitudinal(validation, *, selection, lineage=False,
                     tail_options=None, lineage_limits=None) -> LongitudinalResult
analyze_selected_lineage(validation, *, selection, limits=None) -> SelectedLineageResult
assemble_report(..., longitudinal=None) -> CanonicalReport
```

Selection is pure input/contract validation, not calculation. The coordinator
lives in `metrics/longitudinal.py`; it calls existing representation/metric owners.
Input-only modules cannot import that analytical coordinator. Per-snapshot
representation validation constructs final representation scopes during analysis;
selection need only bind complete population scopes and declarations before then.
Do not fabricate an empty representation scope to imply that assignment ran.

Step 2 retains `baseline` in the selection and adds declaration-only
`compatibility`/`reason_codes` to each pair. `pair.status` reflects that limited
check. A compatible basis says nothing about distribution availability or map
totality on actual states. Malformed explicit maps and missing/conflicting
chronology raise structured input errors. Valid independent snapshots remain
usable by the existing APIs; preserving them in a failed series report belongs
to later orchestration. The selector has no file access or analytical dispatch.

Step 3 implements `analyze_longitudinal` for distributions and optional pair-tail
disappearance. It groups records once, assigns each snapshot once, and invokes
the existing pair kernel once per available scheduled pair. Original summaries
retain `StateDistributionResult`; successful comparisons retain `SupportComparison`.
Unavailable endpoints have `support_comparison=None`, explicit delta/family
reasons and null state sets. Their record delta can remain available after the
comparison gate. Snapshot summaries carry observed full/eligible/excluded counts.

The internal `LongitudinalDelta` keeps separate scope references, endpoint values,
denominators, coverage and reasons. `TailDisappearanceResult` keeps its explicit
rule and earlier harmonized selection. These are staged Python results, not new
schema-1.1 output fields. Required provenance/direct-closure families retain
`ExecutionStatus.DEFERRED` and `R_LONGITUDINAL_FAMILIES_DEFERRED` until Step 4;
the overall staged execution cannot yet be `completed`. This temporary internal
state does not extend the final public status inventory below. `lineage=True`
or a non-null `lineage_limits` remains a structured error until Step 5.

The input bundle retains its existing `ContentMode`, and selection includes it
in its private binding. Inline content uses the existing exact-content owner.
Nonempty local-reference content is unavailable to this series API because the
bundle does not retain the actual resolved text. Neither reference paths nor
earlier read-success markers substitute for that text. Field-based distributions
remain usable under local-reference mode; analysis performs no file access.

### 3.1 Selection invariants and empty scopes

`selected_versions` is the complete set represented in accepted selection
declarations; `selected_order` is the unique chronological tuple for that set.
Every nonempty snapshot contains every canonical key of its selected version.
No context version may be selected; no duplicate/disjoint fragment of a selected
version creates an extra snapshot. Each lineage target is precisely its full
population scope. The ordinary API's primary-only target rule remains intact.

The retained `VersionOrderResult.loaded_versions` always means actual loaded
versions. Additional chronology entries are not data. Python may identify a
snapshot with `empty_scope=true` only when no records of that version are loaded,
the version is separately declared in the chronology, and no context role claims
it. CLI empty files remain input/selection errors. Selected empty declarations
remain explicit in the selection, never added as fake loaded rows or versions.

For the Python empty-snapshot path, `primary_version` remains the nonempty input
primary and is latest among loaded selected versions. An explicitly identified
empty snapshot can follow that primary. This does not relax the CLI rule, where
every selected file is nonempty. Empty declarations require chronology membership
and explicit `empty_scope=true`; ordinary unloaded order entries remain unselected.

For empty endpoints, a narrow compatibility helper reuses existing descriptor,
meaning and directed mapping checks with selected chronology. It does not forge
an ExplicitPairContext that claims the empty version was loaded. Do not invoke
the numerical pair kernel when a distribution is unavailable. Record-count delta
may remain available after order/descriptor compatibility, even though support,
diversity, retention and state-set results are unavailable.

### 3.2 Pair schedule

For k selected versions emit k-1 adjacent pairs. `baseline=first` adds first to
each later version; deduplicate the first adjacent pair and mark both kinds.
Order the final distinct pairs by `(later ordinal, earlier ordinal)`. Default
pair count is k-1; baseline pair count is 2k-3. Never skip an incompatible middle
version to manufacture adjacency. Do not use a context or unloaded version as
the baseline. Ordinal order and pair count remain deterministic under file/row
permutation and nonsemantic renaming.

### 3.3 Binding and narrow lineage extension

`input_signature` is internal, not a public identifier or authenticity claim.
It binds selected roles/keys, retained chronology, representation declarations,
the relevant state-assignment basis and provenance/parent evidence consumed.
Use existing canonical digest utilities and lineage input binding. Do not place
raw text, URI/path strings or secret material into public signatures. A content
representation may bind existing content hashes internally; never expose that
binding as a cross-report fingerprint. Changed same-ID input must fail stale
result reuse. Consumers revalidate scopes/declarations and signatures rather
than trusting cached status labels.

`SelectedLineageResult` contains `selected_versions`, `shared_graph`,
`shared_cycles`, `targets`, `resource_usage`, `execution_status`, `reason_codes`,
`messages`, `input_signature`. Each target summary contains its immutable full
`population_scope` and the inherited Phase 5 ancestry/coverage/concentration
values, plus its target statuses/reasons and bound input signature. Target data
must be a partition of the selected version populations, excluding context.

Shared graph/cycle/root evidence is validated once and referenced within this
invocation. Existing CycleAnalysis and LineageAnalysisResult validate/copy
target-bound structures; repeatedly replacing their scope is not a zero-copy
adapter. Introduce target-only summaries without k copies of all node evidence.
The legacy `analyze_lineage` result and primary-only default remain supported.
No temporary role mutation, forged validation result or relaxed parent identity
rule is permitted. All loaded graph nodes count against inherited limits once;
root work counters cover the shared operation without resets between targets.

All snapshots use this invocation's common supplied graph. Describe the result
as retrospective evidence analysis, not historical knowledge at release time.
A parent in a later version under validated chronology remains invalid.
Disconnected cycles retain graph error status; unaffected values may survive
with explicit scope. Root-stage exhaustion leaves graph/reference diagnostics
already computed but no truncated root partition or concentration metrics.

## 4. Public report contract, schema 1.2

Preserve the twelve top-level sections. New series fields use structural IDs
`s0001`, `p0001`, `b0001` for ordered snapshots, scheduled comparisons and first
encountered distinct descriptor/meaning bases. These are report-local references;
they encode no literal record/state identity. Their sequence follows selected
chronology/pair schedule, never lexicographic version spelling. Scope IDs use
`s0001.population` and `s0001.representation`. Optional harmonized pair scopes
use `p0001.earlier` and `p0001.later`.

### 4.1 Inputs and references

`inputs.longitudinal` has exactly these fields:

| Field | Shape |
|---|---|
| `requested` | boolean |
| `baseline` | `none` or `first` |
| `primary_snapshot_id` | snapshot reference or null when selection fails/unrequested |
| `selected_version_count` | nonnegative integer |
| `comparison_count` | nonnegative integer; intended schedule, not count of successes |
| `order_source` | retained order-source label or null |
| `snapshots` | array of the snapshot descriptors below |
| `comparisons` | array of the scheduled pair descriptors below |
| `representations` | array of basis declarations below |
| `scopes` | array of the scope summaries below |
| `context_versions` | bounded protected version-detail table; empty when no context |
| `context_version_count` | exact nonnegative integer |
| `max_versions` | positive integer, default 100 |
| `detail_limit` | constant 100 |
| `redaction` | existing omission metadata or null |

Snapshot descriptor: `snapshot_id`, `dataset_version` (nullable only under
identity omission), `ordinal` (one-based), `input_role` (`records_primary`,
`records_compare`, or `declared_empty`), `empty_scope` (boolean),
`population_scope_id`, `representation_scope_id` (nullable until assignment),
`basis_id` (nullable until valid declaration), `redaction` (nullable).

Pair descriptor: `comparison_id`, `earlier_snapshot_id`, `later_snapshot_id`,
`kinds`, `compatibility_status` (`available`, `unavailable`), `reason_codes`,
`earlier_basis_id`, `later_basis_id` (nullable when that declaration is invalid),
`harmonized_basis_id` (nullable when blocked),
`mapping` (null or the bounded public summary below),
`mapping_collisions` (bounded detail or null when no mapping/blocked).

The public mapping summary contains `direction`, `source_basis_id`,
`target_basis_id`, and `entries`, a bounded detail table of
`{source_state, target_state}` rows. Full mapping dictionaries remain internal
and in the user's explicit config. Each public collision group contains
`target_state` and `source_states`, itself a bounded detail table. Bound both
the number of groups and the source-state list within a group; one large
many-to-one collision cannot bypass the 100-row detail convention. Every level
retains exact total/returned/omitted counts before privacy transforms.

Basis declaration: `basis_id`, `representation` (existing descriptor wire shape),
`state_semantics` (nullable when omitted), `redaction` (nullable). Equal raw
labels in distinct bases do not establish shared meanings. Mapped pair bases
remain local; one connected trajectory requires one common descriptor and
declared meaning across all its original snapshots. No new global trend field.

Scope summary: `scope_id`, `snapshot_id`, `record_count`,
`excluded_record_count`, `denominator_basis`. Scope membership remains exact
internally. New series serialization stores these summaries once and references
them; it does not repeat complete key arrays. Legacy scope schemas remain
unchanged. All scope references must resolve within the same canonical report.

### 4.2 Value envelopes

Reuse existing envelope meaning and fixed per-field owner/evidence/method/unit.
For the new series family only, replace inline `scope`/`representation` with
`scope_id`/`basis_id` references. Retain `value`, `status`, `reason_codes`,
`required_evidence`, `owner_ids`, `trace_ids`, `theory_map_ids`, `method_id`, `unit`,
`evidence_class`, `coverage`, `coverage_reason`, `denominator`,
`denominator_reason`, `assumptions`, `limitations`, `weighting`, `input_basis`.
Use established weighting/input-basis values. `basis_id=null` is correct for
representation-independent quantities. The enclosing comparison still obeys
the approved pair compatibility gate.

Every pair envelope carries `scope_id=null` and explicit `earlier_scope_id` and
`later_scope_id`; its two endpoints must resolve to the declared comparison.
Delta envelopes additionally carry
`earlier_value`, `later_value`, `earlier_denominator`, `later_denominator`,
`earlier_coverage`, `later_coverage`, `earlier_reason_codes`, `later_reason_codes`.
For deltas, the single `denominator=null` and reason
`not_applicable_to_difference`; preserve both endpoint denominators instead of
inventing a common one. Nondelta set/count results use their exact set method and
endpoint scope references without fictitious scalar delta endpoints. Retention's
denominator is earlier positive-mass support.
These schema-local envelope additions do not alter ordinary schema-1.1 field
meanings. Null endpoint values/reasons remain explicit, including optional
families that were not requested.

`status` is `available`, `partial` or `unavailable`; finite values are required
for available/partial scalars. Unavailable `value` is null and requires a reason.
Boolean is not an integer/number. Partial is a report/series wrapper status;
do not reinterpret the old two-value CalculationStatus enum or coerce a partial
lineage result into a completed legacy kernel result.

### 4.3 Snapshot field inventory

Rows in `observed_facts.longitudinal.snapshots` have `snapshot_id` plus these
enveloped fields, preserving inherited observed evidence:

| Fields | Unit / owner |
|---|---|
| `record_count` | records / PR-002 / inherited `PR-002.record_count` |
| `representation_eligible_record_count`, `representation_excluded_record_count` | records / PR-011 |
| `provenance_row_coverage`, `provenance_required_field_coverage`, `grounding_field_coverage` | ratio / PR-004 |
| `source_type_counts` | five-category count object / PR-005 |
| `missing_provenance_count` | records / PR-004 |
| `provenance_confidence_counts` | four-category count object / PR-004 |
| `declared_parent_reference_count`, `resolved_parent_reference_count`, `unresolved_parent_reference_count` | reference entries / PR-008 |

The reference field names explicitly mean declarations, preserving aliases and
repeated references. Unique graph edge count belongs to shared graph evidence.
No new alias is introduced for legacy ordinary `*_parent_edge_count` fields.

Rows in `derived_metrics.longitudinal.snapshots` have `snapshot_id` plus:

| Fields | Unit / owner / inherited method |
|---|---|
| `support_size`, `gini_simpson_diversity` | states, dimensionless / T1 / F-002, F-003 |
| `source_type_shares` | ratio object, human/synthetic/mixed/sensor/unknown / PR-005 / F-007 |
| `missing_provenance_share` | ratio / PR-004 / missing rows divided by N |
| `direct_closure_lower_bound`, `direct_closure_upper_bound`, `direct_closure_interval_width` | ratio / T3 / F-009, F-010 and upper-minus-lower |
| `grounded_record_count`, `closed_record_count`, `unresolved_record_count`, `records_with_resolved_external_ancestry` | records / T4 / accepted G/C/U classifications |
| `distinct_external_root_count` | roots / T4 / union of target supporting root sets |
| `ancestry_concentration_hhi`, `effective_external_root_count` | ratio, roots / T4 / F-012, F-013 |
| `resolved_parent_edge_coverage` | ratio / PR-008 / resolved declaration entries divided by declared entries |
| `resolved_lineage_coverage`, `external_ancestry_coverage` | ratio / T4 / (G+C)/N, G/N |
| `lineage_closure_lower_bound`, `lineage_closure_upper_bound`, `lineage_closure_interval_width` | ratio / T3 / C/N, (C+U)/N, U/N |

Each lineage coverage envelope retains Phase 5 zero-denominator convention;
`resolved_parent_edge_coverage` includes `no_declared_parents`. Concentration
uses G as its allocation denominator; incidence retains N. G=0 concentration
is null even if distinct known supporting roots is the valid value zero.
Resource-aborted root stages have no exact root-count zero.

### 4.4 Comparison field inventory

Rows in `derived_metrics.longitudinal.comparisons` have `comparison_id` and:

| Fields | Unit / owner / method |
|---|---|
| `record_count_delta` | records / T1 / F-018 |
| `support_delta`, `gini_simpson_diversity_delta` | states, dimensionless / T1 / F-005, F-018 |
| `support_loss_count`, `support_added_count` | states / T1 / exact pair set cardinalities |
| `support_retention_ratio` | ratio / T1 / F-006 |
| `extinct_states`, `added_states`, `retained_states` | bounded state sets / T1 / earlier-minus-later, later-minus-earlier, intersection |
| `tail_extinction_count`, `tail_extinct_states` | states, bounded state set / T2 / earlier tail intersect missing states |
| `provenance_row_coverage_delta`, `provenance_required_field_coverage_delta`, `grounding_field_coverage_delta` | ratio / PR-004 / F-018 |
| `source_type_share_deltas` | five-category signed ratio object / PR-005 / F-018 per category |
| `missing_provenance_share_delta` | ratio / PR-004 / F-018 |
| `direct_closure_lower_bound_delta`, `direct_closure_upper_bound_delta`, `direct_closure_interval_width_delta` | ratio / T3 / F-018 |
| `distinct_external_root_count_delta`, `ancestry_concentration_hhi_delta`, `effective_external_root_count_delta` | roots, ratio, roots / T4 / F-018 |
| `unresolved_parent_reference_count_delta`, `resolved_parent_edge_coverage_delta` | reference entries, ratio / PR-008 / F-018 |
| `resolved_lineage_coverage_delta`, `external_ancestry_coverage_delta` | ratio / T4 / F-018 |
| `lineage_closure_lower_bound_delta`, `lineage_closure_upper_bound_delta`, `lineage_closure_interval_width_delta` | ratio / T3 / F-018 |

All listed deltas are later-minus-earlier. Source shares are five categories;
missing provenance is its separate sixth population component. Tail envelopes
add `tail_selection` with the existing TailSelectionOptions serialization and
`earlier_sample_size`. CLI supports its existing three threshold rules; Python
may retain explicit `state_list`. On mapped comparisons, tail selection uses
the harmonized earlier basis. A raw label in a different representation is not
automatically a requested tail state.

`extinct_states` always means **extinct from the observed later version under
the declared representation**. Preserve reappearance at a later position.
Empty/all-excluded sides make state sets null, not all-lost or empty-successful.
An available empty set uses a complete detail table with zero total/items.

There is no new longitudinal proxy aggregate. Existing ordinary proxies remain
bound to the results that actually supplied them. Model-performance decline,
causal ancestor effect, universal integrity and universal collapse conclusions
remain unavailable. `simulations` is unchanged and no scenario executes.

### 4.5 Shared graph and capability status

`observed_facts.longitudinal.shared_lineage` is null unless lineage was requested;
otherwise it contains `execution_status`, `reason_codes`, `loaded_record_count`,
`unique_edge_count`, `cycle_status`, `cycle_count`, `resource_usage`,
`graph_diagnostics` (bounded existing safe diagnostics) and `evidence_scope`
constant `common_supplied_retrospective_graph`. Uncomputed values are null with
reasons. These facts share the existing Phase 5 evidence classes/definitions.
Internal graph signatures, full paths and all-node root tables are not public.

Extend both equal dataset-longitudinal capability mirrors with
`longitudinal_execution` containing `status`, `reason_codes`,
`requested_families`, `snapshot_statuses`, `comparison_statuses`. Snapshot/pair
status rows reference their structural ID and contain `families`, a map of the
five fixed family names to `{execution_status, reason_codes}`. Omitted optional
families have `not_requested`; they do not make the series partial.

| Execution state | Exact condition |
|---|---|
| `not_requested` | Explicit series enablement is false; no series calculation ran. |
| `completed` | Every requested family/pair completed with its valid required values and no partial-coverage dependency or error. |
| `partial` | At least one requested comparison family has useful completed values, but some requested family/pair is unavailable, partial or errored. |
| `failed` | Selection/order/resource admission prevents every requested comparison family, or a requested execution produces no valid comparison-family values. Preserve independently computed snapshots. |

For family rows, `partial` can preserve valid counts alongside unavailable
ratios. `completed` does not mean complete information in the universe: a valid
coverage ratio of 0 or a conservative direct interval [0,1] can be completed
results with their inherited uncertainty disclosures. A partial ancestry subset
stays partial even if its HHI is finite. Optional unrequested families have null
metric values with an explicit not-requested reason.

Capability eligibility continues to describe inputs. It does not certify that
the series ran. Remove `R_LONGITUDINAL_FAMILIES_DEFERRED` for implemented,
requested scope only; a legacy pair still has its narrower execution record.
Run failure/CLI exit retain existing error precedence: config errors 2,
parent/cycle errors 3, other input/calculation/resource errors 1, with successful
publication not erasing prior errors. Warning-only incomplete evidence remains
reportable with existing strict-mode promotion. Representation incompatibility
is a pair error, even if other pairs and snapshots survive.

## 5. Reasons, resource guards and privacy

### 5.1 New series reasons

Prefer existing owner reason/error codes on source results. Add only these
series-specific reasons to explain orchestration rather than new scientific
classifications:

```text
R_LONGITUDINAL_NOT_REQUESTED
R_LONGITUDINAL_FAMILY_NOT_REQUESTED
R_LONGITUDINAL_SELECTION_INVALID
R_LONGITUDINAL_PAIR_BLOCKED
R_LONGITUDINAL_ENDPOINT_UNAVAILABLE
R_LONGITUDINAL_PARTIAL_COVERAGE
R_LONGITUDINAL_RESOURCE_LIMIT
```

Selection failures preserve existing `E_CONFIG_INVALID`, `E_SCHEMA_TYPE`,
`E_VERSION_ORDER_CONFLICT` or representation error as applicable. Add
`E_LONGITUDINAL_RESOURCE_LIMIT_EXCEEDED` for selected-version admission only;
existing lineage errors remain unchanged. Missing order uses existing missing
chronology reasons; endpoint fields retain both exact source reason lists.
Codes are fixed text, never arbitrary identifiers. Do not duplicate warnings
once per metric when one scoped family diagnostic identifies the same failure.

An unavailable pair metric caused by missing endpoint evidence carries
`R_LONGITUDINAL_ENDPOINT_UNAVAILABLE` plus source reasons. A compatibility/order
block carries `R_LONGITUDINAL_PAIR_BLOCKED` plus its owner reason. Partial
lineage arithmetic carries `R_LONGITUDINAL_PARTIAL_COVERAGE`. A failed resource
stage cannot be represented merely as no roots observed.

### 5.2 Bounds

At default version limit 100, execute at most 99 adjacent or 197 distinct
adjacent-plus-first pairs. Check admission before per-snapshot calculations.
Do not truncate selection to fit. Inherited graph/input guards apply to the
combined loaded scope, not independently per selected version. No all-pairs
matrix, automatic full path export or replicated full ordinary report is added.

New detail tables use the existing shape: `items`, `total_count`,
`returned_count`, `omitted_count`, `limit=100`, `detail_status` and
`omission_reasons`. Exact counts/metrics precede display limits. Sort visible
state rows by the existing canonical state ordering before privacy transforms.
Raw semantic ordering is not recomputed from pseudonym text. Internal full
sets remain available to existing kernels; new public detail is bounded.

### 5.3 Privacy and invalid handoffs

Use established identifier protection consistently across each report. Literal
versions, states, root keys, mapping keys/values, user declaration text, context
labels, paths and diagnostics all pass through the safe view. In redacted mode,
state-meaning text is omitted. Stable basis-local state pseudonyms preserve
within-basis joins without equating different declared meanings. Version
pseudonyms join snapshots, context and mappings consistently. Do not publish
internal input digests. Structural IDs and exact aggregate counts can remain.

Hash/omit modes follow existing semantics. Under omit, retain structurally valid
rows/references but null the protected literals and mark their redaction; omit
whole identity-bearing detail tables with the existing aggregate-only shape.
Do not leave required string fields missing, leak mapping labels in keys or use
reason prose to reintroduce hidden paths. Required evidence/assumption strings
use approved safe wording, not exception arguments or unchecked input text.

Report assembly checks full target membership, signatures, endpoint references,
owner metadata, scope totals, chronology and statuses. It rejects stale same-ID
results, incomplete selected targets, unresolved foreign scope references,
duplicate pair rows, wrong order, altered arithmetic or invalid redacted rows.
It validates supplied arithmetic; it does not run the series or rebuild graphs.
Renderers consume the validated canonical report without calculation or I/O.

## 6. Independent acceptance and implementation boundary

Use `tests/fixtures/longitudinal/cases.json`, its README and
`hero_expected.json`. Rational strings are test expectations, not JSON report
number encodings. Existing NumericalPolicy tolerances remain 1e-12; counts,
sets, identities and classifications compare exactly. Step 1 tests exercise
current inputs and existing explicit kernels only. They make no claim that the
new coordinator, selected lineage interface, config or report already runs.

Keep canonical Hero source rows/expectations unchanged. The three-version case
must retain intermediate disappearance and subsequent reappearance even when
endpoint support counts match. Coverage/source/lineage cases keep each version's
own denominator. Mapping, incompatible/empty, context-only, all-unknown/G=0 and
partial variants supply independent future acceptance expectations.

Step 2 implements selection/contracts. Later steps add calculations, selected
lineage, schema/CLI, bounded adversarial measurement and candidate acceptance in
the approved order. This document adds no metadata service, approval framework,
new source evidence ontology, persistent cache or empirical causal claim.
