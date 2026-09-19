# Report Schema

Status: Phase 4 Step 2 canonical public contract. Schema version: `1.0`.

The authoritative public shape is `schemas/report.schema.json`, Draft 2020-12. Runtime validation is implemented in `result.py` using the standard library. `report_schema()` returns a detached copy of the same declarative contract. No runtime schema package, filesystem lookup or remote resolver is used. The `$schema` and `$id` identifiers are descriptive; all references are local `$defs` references.

## Scope and API

`CanonicalReport.from_dict(payload)` and direct `CanonicalReport(payload)` both validate and freeze the complete report. `validate_report(payload)` returns `None` or raises `ReportValidationError`, a `ValueError`. Input must consist of built-in JSON dictionaries, lists, strings, finite numbers, booleans and nulls. The `sections` property contains nested immutable mappings and tuples; `to_dict()` returns a detached dictionary in the required top-level order. It performs no calculation adaptation, input loading, rendering or CLI action.

Existing Phase 3 calculation contracts and their three-class enum remain unchanged. `ReportEvidenceClass` owns the five report classes. Report validation establishes structural consistency, not empirical truth or correctness of a caller-supplied analysis. Step 3 must explicitly validate and adapt accepted calculation types.

## Required sections

| Order | Path | Type | Product owner | Empty form |
|---:|---|---|---|---|
| 1 | `run` | object | PR-016 / PR-013 | Full run metadata |
| 2 | `inputs` | object | PR-002 | `{}` |
| 3 | `observability` | object | PR-010 | `{}` |
| 4 | `capabilities` | object | PR-011 | `{}` |
| 5 | `observed_facts` | object | PR-012 | `{}` |
| 6 | `derived_metrics` | object | PR-012 | `{}` |
| 7 | `proxy_signals` | object | PR-012 | `{}` |
| 8 | `simulations` | object | PR-012 | `{}` |
| 9 | `unavailable_conclusions` | array | PR-014 | `[]` |
| 10 | `recommended_next_metadata` | array | PR-014 | `[]` |
| 11 | `warnings` | array | PR-014 | `[]` |
| 12 | `errors` | array | PR-014 | `[]` |

Every section is present in empty, validation-only and error-only reports. Empty analytical sections contain no invented measurements. `run` always contains the complete required metadata, with explicitly explained nulls where no execution supplied a value. A schema-only contract fixture may use a complete run status and documented non-execution nulls. An actual failed audit uses failed or partial status and structured errors.

## Interpretation and null rules

- Analytical envelopes have exactly one primary evidence class. Product metadata, scope descriptions, controls, diagnostics and recommendations have product ownership without additional scientific evidence envelopes.
- A scalar/table `available` or `partial` value is non-null. A measured zero and a measured empty set remain valid values. An unavailable result has `value: null`, `status: unavailable`, nonempty `reason_codes` and nonempty `required_evidence`.
- `representation: null` means the field has no applicable representation, or the result is unavailable because no representation exists. Available support, diversity and tail results require their explicit descriptor.
- `coverage` and `denominator` are independently nullable. Each null requires its nonempty `coverage_reason` or `denominator_reason`; a present number requires that reason to be null. Zero coverage or zero denominator remains numeric zero and is never substituted for missing evidence.
- `scope.record_count` and `excluded_record_count` may be null only to describe a basis without empirical record counts, such as a supplied probability vector. Empty version lists mean no selected dataset scope, as in error-only/control evidence. Explicit record identities, when supplied, must match scope membership and counts.
- Required run nulls are explained exactly once in `run.null_reasons`, keyed only by the nullable run fields. Reasons for non-null fields and unregistered reason keys are rejected. `random_seed: null` is expected for nonstochastic and analytic operations.
- All numeric values are finite. Ratio/probability ranges are explicit. JSON booleans are never numbers. Integer schema fields follow JSON Schema numeric semantics, so mathematically integral JSON numbers are accepted without coercing their original representation. Strings, including dynamic state and version keys, are UTF-8 literals without NUL.
- A dynamic map permits only its declared value type. Version IDs and state IDs are literal keys, including punctuation and Unicode; they are not interpreted as field paths. Unknown metric keys, enum values, owners or method IDs fail.
- Closed interval components retain matching status, scope, representation, coverage, denominator and unavailable reasons. All endpoints and width are supplied together. Runtime verifies endpoint order and width within the inherited absolute/relative tolerance `1e-12`; it never emits a calculated replacement.

## Capability and execution contract

Input capability status is `available`, `partial`, `unavailable` or `experimental`. Execution status is independently `completed`, `partial`, `not_requested`, `deferred` or `failed`. Executed work names its operations in `execution_scope`; all noncompleted statuses carry `execution_reason_codes`. A nonempty matrix contains exactly the seven approved capability keys. Its copy at `observability.capabilities` is structurally equal on input and shares the same immutable object in the canonical result. A mismatch is rejected.

`observability` may be empty before assessment; otherwise all six fields are required. Maximum level 0–5 must match its exact registered label. Level 4 input eligibility can coexist with lineage execution deferred. Phase 4 cannot claim completed or partially executed Phase 5 lineage analysis. Existing declared/resolved edge observations and the explicitly named earlier-version ordering certificate retain their limited Phase 2 provenance.

## Analytical field registry

`*` denotes one literal dynamic-map key; `[]` denotes array membership. All entries below use the common envelope, except the registered future key which must be absent. Every entry fixes its primary class, unit, owner and method. Formula IDs retain their Phase 3 meaning. Non-formula method IDs name the explicit report mapping of an existing product/kernel rule; the optional envelope `method` preserves the original descriptive method text. T1–T6 owners must also occur in `trace_ids`. `theory_map_ids` accepts only IDs from the frozen Theory Source Map. Product-only owners need no invented Theory Map ID.

| Exact public path | Value type | Unit | Evidence class | Owner / trace | Method or rule ID | Minimum level | Null / stage boundary |
|---|---|---|---|---|---|---:|---|
| `observed_facts.record_counts.*` | integer | `records` | `observed_fact` | `PR-002` | `PR-002.record_count` | 0 | Null only with unavailable reasons |
| `observed_facts.content.duplicate_record_count` | integer | `records` | `observed_fact` | `PR-006` | `PR-006.duplicate_record_count` | 1 | Null only with unavailable reasons |
| `observed_facts.content.duplicate_group_count` | integer | `groups` | `observed_fact` | `PR-006` | `PR-006.duplicate_group_count` | 1 | Null only with unavailable reasons |
| `observed_facts.content.exact_duplicate_groups` | duplicate_group[] | `groups` | `observed_fact` | `PR-006` | `PR-006.exact_duplicate_groups` | 1 | Null only with unavailable reasons |
| `observed_facts.provenance.provenance_row_coverage` | ratio | `ratio` | `observed_fact` | `PR-004` | `F-008` | 2 | Null only with unavailable reasons |
| `observed_facts.provenance.provenance_required_field_coverage` | ratio | `ratio` | `observed_fact` | `PR-004` | `PR-004.provenance_required_field_coverage` | 2 | Null only with unavailable reasons |
| `observed_facts.provenance.grounding_field_coverage` | ratio | `ratio` | `observed_fact` | `PR-004` | `PR-004.grounding_field_coverage` | 2 | Null only with unavailable reasons |
| `observed_facts.provenance.source_type_field_coverage` | ratio | `ratio` | `observed_fact` | `PR-004` | `PR-004.source_type_field_coverage` | 2 | Null only with unavailable reasons |
| `observed_facts.provenance.provenance_confidence_field_coverage` | ratio | `ratio` | `observed_fact` | `PR-004` | `PR-004.provenance_confidence_field_coverage` | 2 | Null only with unavailable reasons |
| `observed_facts.provenance.source_type_counts` | category_count_map | `records` | `observed_fact` | `PR-005` | `PR-005.source_type_counts` | 2 | Null only with unavailable reasons |
| `observed_facts.provenance.provenance_confidence_counts` | category_count_map | `records` | `observed_fact` | `PR-004` | `PR-004.provenance_confidence_counts` | 2 | Null only with unavailable reasons |
| `observed_facts.provenance.analyzed_record_count` | integer | `records` | `observed_fact` | `PR-004` | `PR-004.analyzed_record_count` | 2 | Null only with unavailable reasons |
| `observed_facts.provenance.records_with_matching_rows` | integer | `records` | `observed_fact` | `PR-004` | `PR-004.records_with_matching_rows` | 2 | Null only with unavailable reasons |
| `observed_facts.provenance.missing_provenance_count` | integer | `records` | `observed_fact` | `PR-004` | `PR-004.missing_provenance_count` | 2 | Null only with unavailable reasons |
| `observed_facts.provenance.known_open_count` | integer | `records` | `observed_fact` | `T3` | `T3.direct_grounding_classification` | 2 | Null only with unavailable reasons |
| `observed_facts.provenance.known_closed_count` | integer | `records` | `observed_fact` | `T3` | `T3.direct_grounding_classification` | 2 | Null only with unavailable reasons |
| `observed_facts.provenance.unresolved_grounding_count` | integer | `records` | `observed_fact` | `T3` | `T3.direct_grounding_classification` | 2 | Null only with unavailable reasons |
| `observed_facts.lineage.declared_parent_edge_count` | integer | `edges` | `observed_fact` | `PR-008` | `PR-008.declared_parent_edge_count` | 3 | Null only with unavailable reasons |
| `observed_facts.lineage.resolved_parent_edge_count` | integer | `edges` | `observed_fact` | `PR-008` | `PR-008.resolved_parent_edge_count` | 3 | Null only with unavailable reasons |
| `observed_facts.lineage.unresolved_parent_edge_count` | integer | `edges` | `observed_fact` | `PR-008` | `PR-008.unresolved_parent_edge_count` | 3 | Null only with unavailable reasons |
| `observed_facts.lineage.cycle_status` | enum | `status` | `observed_fact` | `T6` | `T6.graph_cycle_check` | 3 | Unavailable only: Phase 5 deferred |
| `observed_facts.lineage.ordering_certificate` | ordering_certificate | `certificate` | `observed_fact` | `PR-008` | `PR-008.earlier_version_certificate` | 3 | Null only with unavailable reasons |
| `observed_facts.state_counts.by_version.*` | state_count[] | `records` | `observed_fact` | `T1` | `T1.state_counts` | 1 | Null only with unavailable reasons |
| `derived_metrics.support.by_version.*.support_size` | integer | `states` | `derived_metric` | `T1` | `F-002` | 1 | Null only with unavailable reasons |
| `derived_metrics.support.by_version.*.weighted_support_size` | integer | `states` | `derived_metric` | `T1` | `F-002` | 1 | Null only with unavailable reasons |
| `derived_metrics.support.support_delta` | integer | `states` | `derived_metric` | `T1` | `F-005` | 4 | Null only with unavailable reasons |
| `derived_metrics.support.support_retention_ratio` | ratio | `ratio` | `derived_metric` | `T1` | `F-006` | 4 | Null only with unavailable reasons |
| `derived_metrics.support.support_loss_count` | integer | `states` | `derived_metric` | `T1` | `T1.support_set_difference` | 4 | Null only with unavailable reasons |
| `derived_metrics.support.support_added_count` | integer | `states` | `derived_metric` | `T1` | `T1.support_set_difference` | 4 | Null only with unavailable reasons |
| `derived_metrics.support.extinct_states` | state_id[] | `set_of_states` | `derived_metric` | `T1` | `T1.earlier_minus_later` | 4 | Null only with unavailable reasons |
| `derived_metrics.support.added_states` | state_id[] | `set_of_states` | `derived_metric` | `T1` | `T1.later_minus_earlier` | 4 | Null only with unavailable reasons |
| `derived_metrics.support.retained_states` | state_id[] | `set_of_states` | `derived_metric` | `T1` | `T1.support_intersection` | 4 | Null only with unavailable reasons |
| `derived_metrics.support.comparison_details` | comparison_basis | `comparison` | `derived_metric` | `T1` | `T1.explicit_pair_basis` | 4 | Null only with unavailable reasons |
| `derived_metrics.diversity.by_version.*.gini_simpson_diversity` | ratio | `dimensionless` | `derived_metric` | `T1` | `F-003` | 1 | Null only with unavailable reasons |
| `derived_metrics.diversity.by_version.*.simpson_concentration` | ratio | `dimensionless` | `derived_metric` | `T1` | `F-004` | 1 | Null only with unavailable reasons |
| `derived_metrics.diversity.by_version.*.weighted_gini_simpson_diversity` | ratio | `dimensionless` | `derived_metric` | `T1` | `F-003` | 1 | Null only with unavailable reasons |
| `derived_metrics.diversity.by_version.*.weighted_simpson_concentration` | ratio | `dimensionless` | `derived_metric` | `T1` | `F-004` | 1 | Null only with unavailable reasons |
| `derived_metrics.diversity.by_version.*.state_frequencies` | state_frequency[] | `ratio` | `derived_metric` | `T1` | `F-001` | 1 | Null only with unavailable reasons |
| `derived_metrics.diversity.by_version.*.weighted_state_frequencies` | state_frequency[] | `ratio` | `derived_metric` | `T1` | `F-001` | 1 | Null only with unavailable reasons |
| `derived_metrics.diversity.by_version.*.weighted_state_masses` | state_mass[] | `user_declared_weight_mass` | `derived_metric` | `T1` | `T1.state_weight_mass` | 1 | Null only with unavailable reasons |
| `observed_facts.supplied_state_probabilities.by_version.*` | state_probability[] | `ratio` | `observed_fact` | `T1` | `T1.supplied_probability_vector` | 1 | Null only with unavailable reasons |
| `derived_metrics.diversity.by_version.*.distribution_basis` | distribution_basis | `basis` | `derived_metric` | `T1` | `T1.validated_distribution_basis` | 1 | Null only with unavailable reasons |
| `derived_metrics.diversity.gini_simpson_diversity_delta` | number | `dimensionless` | `derived_metric` | `T1` | `F-018` | 4 | Null only with unavailable reasons |
| `derived_metrics.tail.tail_support_size` | integer | `states` | `derived_metric` | `T2` | `T2.declared_tail_rule` | 1 | Null only with unavailable reasons |
| `derived_metrics.tail.tail_record_share` | ratio | `ratio` | `derived_metric` | `T2` | `T2.tail_record_share` | 1 | Null only with unavailable reasons |
| `derived_metrics.tail.rarity_ranking` | rarity_entry[] | `ordinal_rank` | `derived_metric` | `T2` | `T2.frequency_count_unicode_order` | 1 | Null only with unavailable reasons |
| `derived_metrics.tail.tail_states` | state_id[] | `set_of_states` | `derived_metric` | `T2` | `T2.declared_tail_rule` | 1 | Null only with unavailable reasons |
| `derived_metrics.provenance.source_type_shares` | category_ratio_map | `ratio` | `derived_metric` | `PR-005` | `F-007` | 2 | Null only with unavailable reasons |
| `derived_metrics.provenance.weighted_source_type_shares` | category_ratio_map | `ratio` | `derived_metric` | `PR-005` | `F-007` | 2 | Null only with unavailable reasons |
| `derived_metrics.provenance.weighted_source_type_masses` | category_mass_map | `user_declared_weight_mass` | `derived_metric` | `PR-005` | `PR-005.source_weight_mass` | 2 | Null only with unavailable reasons |
| `derived_metrics.provenance.total_weight` | number | `user_declared_weight_mass` | `derived_metric` | `PR-005` | `PR-005.total_weight` | 2 | Null only with unavailable reasons |
| `derived_metrics.provenance.missing_provenance_weight` | number | `user_declared_weight_mass` | `derived_metric` | `PR-005` | `PR-005.missing_provenance_weight` | 2 | Null only with unavailable reasons |
| `derived_metrics.provenance.missing_provenance_share` | number | `ratio` | `derived_metric` | `PR-004` | `PR-004.one_minus_row_coverage` | 2 | Null only with unavailable reasons |
| `derived_metrics.provenance.weighted_missing_provenance_share` | number | `ratio` | `derived_metric` | `PR-005` | `PR-005.missing_provenance_weight_share` | 2 | Null only with unavailable reasons |
| `derived_metrics.closure_exposure.direct.lower_bound` | ratio | `ratio` | `derived_metric` | `T3` | `F-009` | 2 | Null only with unavailable reasons |
| `derived_metrics.closure_exposure.direct.upper_bound` | ratio | `ratio` | `derived_metric` | `T3` | `F-010` | 2 | Null only with unavailable reasons |
| `derived_metrics.closure_exposure.direct.interval_width` | ratio | `ratio` | `derived_metric` | `T3` | `T3.upper_minus_lower` | 2 | Null only with unavailable reasons |
| `derived_metrics.closure_exposure.lineage.lower_bound` | ratio | `ratio` | `derived_metric` | `T3` | `T3.lineage_closure` | 3 | Unavailable only: Phase 5 deferred |
| `derived_metrics.closure_exposure.lineage.upper_bound` | ratio | `ratio` | `derived_metric` | `T3` | `T3.lineage_closure` | 3 | Unavailable only: Phase 5 deferred |
| `derived_metrics.closure_exposure.lineage.interval_width` | ratio | `ratio` | `derived_metric` | `T3` | `T3.lineage_closure` | 3 | Unavailable only: Phase 5 deferred |
| `derived_metrics.lineage.resolved_parent_edge_coverage` | ratio | `ratio` | `derived_metric` | `PR-008` | `PR-008.resolved_edges_over_declared` | 3 | Null only with unavailable reasons |
| `derived_metrics.lineage.resolved_lineage_coverage` | ratio | `ratio` | `derived_metric` | `T4` | `T4.resolved_records_over_scope` | 3 | Unavailable only: Phase 5 deferred |
| `derived_metrics.lineage.external_ancestry_coverage` | ratio | `ratio` | `derived_metric` | `T4` | `T4.external_roots_over_scope` | 3 | Unavailable only: Phase 5 deferred |
| `derived_metrics.lineage.distinct_external_root_count` | integer | `roots` | `derived_metric` | `T4` | `T4.root_set_union` | 3 | Unavailable only: Phase 5 deferred |
| `derived_metrics.lineage.top_shared_ancestors` | ancestor_incidence[] | `records` | `derived_metric` | `T4` | `T4.incidence_ranking` | 3 | Unavailable only: Phase 5 deferred |
| `derived_metrics.lineage.ancestry_concentration_hhi` | ratio | `ratio` | `derived_metric` | `T4` | `F-012` | 3 | Unavailable only: Phase 5 deferred |
| `derived_metrics.lineage.effective_external_root_count` | number | `roots` | `derived_metric` | `T4` | `F-013` | 3 | Unavailable only: Phase 5 deferred |
| `derived_metrics.lineage.lineage_depth` | integer | `edges` | `derived_metric` | `PR-009` | `PR-009.maximum_resolved_parent_depth` | 3 | Unavailable only: Phase 5 deferred |
| `proxy_signals.support_contraction` | proxy | `signal` | `proxy_signal` | `T1` | `T1.support_contraction` | 4 | No scalar value; typed class fields |
| `proxy_signals.tail_fragility` | proxy | `signal` | `proxy_signal` | `T2` | `T2.tail_fragility` | 1 | No scalar value; typed class fields |
| `proxy_signals.shared_ancestry_dependence` | proxy | `signal` | `proxy_signal` | `T4` | `T4.shared_ancestry_dependence` | 3 | Unavailable only: Phase 5 deferred |
| `proxy_signals.provenance_uncertainty` | proxy | `signal` | `proxy_signal` | `T3` | `T3.provenance_uncertainty` | 2 | No scalar value; typed class fields |
| `simulations.closed_resampling` | scenario | `scenario` | `simulation` | `T1` | `T1.closed_resampling` | 5 | No scalar value; typed class fields |
| `simulations.tail_extinction` | scenario | `scenario` | `simulation` | `T2` | `T2.tail_extinction` | 1 | No scalar value; typed class fields |
| `simulations.external_reopening` | reserved | `scenario` | `simulation` | `T5` | `T5.external_reopening` | 5 | Absent: registered future |
| `unavailable_conclusions[].model_performance_decline` | unavailable | `conclusion` | `unavailable_conclusion` | `PR-014` | `PR-014.unavailable_conclusion` | 0 | No scalar value; typed class fields |
| `unavailable_conclusions[].causal_ancestor_effect` | unavailable | `conclusion` | `unavailable_conclusion` | `T4` | `T4.unavailable_conclusion` | 0 | No scalar value; typed class fields |
| `unavailable_conclusions[].correlated_semantic_error` | unavailable | `conclusion` | `unavailable_conclusion` | `T4` | `T4.unavailable_conclusion` | 0 | No scalar value; typed class fields |
| `unavailable_conclusions[].production_failure` | unavailable | `conclusion` | `unavailable_conclusion` | `T1` | `T1.unavailable_conclusion` | 0 | No scalar value; typed class fields |
| `unavailable_conclusions[].universal_integrity` | unavailable | `conclusion` | `unavailable_conclusion` | `PR-014` | `PR-014.unavailable_conclusion` | 0 | No scalar value; typed class fields |
| `unavailable_conclusions[].universal_quality` | unavailable | `conclusion` | `unavailable_conclusion` | `PR-014` | `PR-014.unavailable_conclusion` | 0 | No scalar value; typed class fields |
| `unavailable_conclusions[].universal_stability` | unavailable | `conclusion` | `unavailable_conclusion` | `PR-014` | `PR-014.unavailable_conclusion` | 0 | No scalar value; typed class fields |
| `unavailable_conclusions[].universal_entropy_score` | unavailable | `conclusion` | `unavailable_conclusion` | `PR-014` | `PR-014.unavailable_conclusion` | 0 | No scalar value; typed class fields |
| `unavailable_conclusions[].universal_collapse_prediction` | unavailable | `conclusion` | `unavailable_conclusion` | `PR-014` | `PR-014.unavailable_conclusion` | 0 | No scalar value; typed class fields |
| `unavailable_conclusions[].empirical_intervention_effect` | unavailable | `conclusion` | `unavailable_conclusion` | `T5` | `T5.unavailable_conclusion` | 0 | No scalar value; typed class fields |
| `unavailable_conclusions[].amplification_threshold` | unavailable | `conclusion` | `unavailable_conclusion` | `PR-014` | `PR-014.unavailable_conclusion` | 0 | No scalar value; typed class fields |
| `unavailable_conclusions[].lineage_analysis` | unavailable | `conclusion` | `unavailable_conclusion` | `PR-014` | `PR-014.unavailable_conclusion` | 0 | No scalar value; typed class fields |
| `unavailable_conclusions[].lineage_closure_exposure` | unavailable | `conclusion` | `unavailable_conclusion` | `T3` | `T3.unavailable_conclusion` | 0 | No scalar value; typed class fields |
| `unavailable_conclusions[].external_ancestry` | unavailable | `conclusion` | `unavailable_conclusion` | `T4` | `T4.unavailable_conclusion` | 0 | No scalar value; typed class fields |
| `unavailable_conclusions[].complete_pipeline_closure` | unavailable | `conclusion` | `unavailable_conclusion` | `T3` | `T3.unavailable_conclusion` | 0 | No scalar value; typed class fields |

Weighted companions always retain `weighting_mode: weighted`, canonical `weight_field: weight`, their actual weight denominator and the unit `user_declared_weight_mass` for mass values. They never replace unweighted record counts. Gini-Simpson/Simpson values and the diversity delta use `dimensionless`; state frequency remains `ratio`; rarity ranks use `ordinal_rank`; state sets use `set_of_states`.

Supplied probability values use the observed `supplied_state_probabilities` table. Empirically computed frequencies use derived frequency fields. The explicit distribution basis retains probability residuals without rounding, clipping or repair. Provenance row, required-field and grounding coverages remain separate observed facts under the frozen registry; confidence counts never become numeric trust probabilities.

## Registered metadata and container fields

The following tables enumerate non-envelope public fields and containers. A `$defs` reference means the exact shared contract in the following section. `optional` means absence is allowed, never an arbitrary unknown field. Nested fields in an analytical payload inherit the enclosing primary class, owner, scope, method and denominator; they do not create a second evidence class.

### `run`

| Path | Type | Required | Owner | Null meaning |
|---|---|---|---|---|
| `run` | object | required | PR-016 | Not nullable |
| `run.run_id` | string | required | PR-016 | Not nullable |
| `run.toolkit_version` | string | required | PR-016 | Not nullable |
| `run.report_schema_version` | constant "1.0" | required | PR-013 | Not nullable |
| `run.started_at` | string or null | required | PR-016 | Explicitly not applicable/unavailable as described above |
| `run.completed_at` | string or null | required | PR-016 | Explicitly not applicable/unavailable as described above |
| `run.duration_seconds` | number or null | required | PR-016 | Explicitly not applicable/unavailable as described above |
| `run.python_version` | string or null | required | PR-016 | Explicitly not applicable/unavailable as described above |
| `run.platform` | string or null | required | PR-016 | Explicitly not applicable/unavailable as described above |
| `run.command` | string or null | required | PR-016 | Explicitly not applicable/unavailable as described above |
| `run.config_hash` | sha256 or null | required | PR-016 | Explicitly not applicable/unavailable as described above |
| `run.random_seed` | integer or null | required | PR-016 | Explicitly not applicable/unavailable as described above |
| `run.strict_mode` | boolean | required | PR-016 | Not nullable |
| `run.redacted_mode` | boolean | required | PR-016 | Not nullable |
| `run.network_call_count` | integer | required | PR-016 | Not nullable |
| `run.deterministic` | boolean | required | PR-016 | Not nullable |
| `run.privacy_mode` | enum: standard, redacted | required | PR-016 | Not nullable |
| `run.run_status` | enum: complete, partial, failed | required | PR-016 | Not nullable |
| `run.null_reasons` | object | required | PR-016 | Not nullable |
| `run.null_reasons.started_at` | string | optional | PR-016 | Not nullable |
| `run.null_reasons.completed_at` | string | optional | PR-016 | Not nullable |
| `run.null_reasons.duration_seconds` | string | optional | PR-016 | Not nullable |
| `run.null_reasons.python_version` | string | optional | PR-016 | Not nullable |
| `run.null_reasons.platform` | string | optional | PR-016 | Not nullable |
| `run.null_reasons.command` | string | optional | PR-016 | Not nullable |
| `run.null_reasons.config_hash` | string | optional | PR-016 | Not nullable |
| `run.null_reasons.random_seed` | string | optional | PR-016 | Not nullable |
| `run.network_count_scope` | constant "toolkit_managed_outbound_operations" | optional | PR-016 | Not nullable |
| `run.hash_algorithm` | constant "sha256" | optional | PR-016 | Not nullable |
| `run.config_hash_exclusions` | string[] | optional | PR-016 | Not nullable |
| `run.config_hash_exclusions[]` | string | required | PR-016 | Not nullable |
| `run.resolved_options` | resolved_options | optional | PR-016 | Not nullable |
| `run.identifier_protection` | object | optional | PR-016 | Not nullable |
| `run.identifier_protection.algorithm` | constant "HMAC-SHA-256" | required | PR-016 | Not nullable |
| `run.identifier_protection.stability_scope` | enum: run, cross_run | required | PR-016 | Not nullable |
| `run.identifier_protection.record_id_mode` | enum: preserve, hash, omit | required | PR-016 | Not nullable |
| `run.identifier_protection.limitations` | string[] | required | PR-016 | Not nullable |
| `run.identifier_protection.limitations[]` | string | required | PR-016 | Not nullable |

### `inputs`

| Path | Type | Required | Owner | Null meaning |
|---|---|---|---|---|
| `inputs` | object | required | PR-002 | Not nullable |
| `inputs.artifacts` | object[] | optional | PR-002 | Not nullable |
| `inputs.artifacts[]` | object | required | PR-002 | Not nullable |
| `inputs.artifacts[].role` | enum: records_primary, records_compare, provenance_manifest, schema_mapping, config, version_order, embedding_data, external_reference | required | PR-002 | Not nullable |
| `inputs.artifacts[].path` | string or null | required | PR-002 | Explicitly not applicable/unavailable as described above |
| `inputs.artifacts[].path_redacted` | boolean | required | PR-002 | Not nullable |
| `inputs.artifacts[].format` | enum: csv, jsonl, parquet, json, toml, npy | required | PR-002 | Not nullable |
| `inputs.artifacts[].file_hash` | sha256 or null | required | PR-002 | Explicitly not applicable/unavailable as described above |
| `inputs.artifacts[].hash_algorithm` | constant "sha256" | required | PR-002 | Not nullable |
| `inputs.artifacts[].size_bytes` | integer or null | required | PR-002 | Explicitly not applicable/unavailable as described above |
| `inputs.artifacts[].row_count` | integer or null | required | PR-002 | Explicitly not applicable/unavailable as described above |
| `inputs.artifacts[].dataset_versions` | string[] | required | PR-002 | Not nullable |
| `inputs.artifacts[].dataset_versions[]` | string | required | PR-002 | Not nullable |
| `inputs.artifacts[].schema_fields` | string[] | required | PR-002 | Not nullable |
| `inputs.artifacts[].schema_fields[]` | string | required | PR-002 | Not nullable |
| `inputs.artifacts[].parse_status` | enum: completed, partial, failed, not_requested | required | PR-002 | Not nullable |
| `inputs.artifacts[].validation_status` | enum: completed, partial, failed, not_requested | required | PR-002 | Not nullable |
| `inputs.artifacts[].reason_codes` | string[] | required | PR-002 | Not nullable |
| `inputs.artifacts[].reason_codes[]` | string | required | PR-002 | Not nullable |
| `inputs.file_hashes` | object[] | optional | PR-016 | Not nullable |
| `inputs.file_hashes[]` | object | required | PR-016 | Not nullable |
| `inputs.file_hashes[].artifact_index` | integer | required | PR-016 | Not nullable |
| `inputs.file_hashes[].algorithm` | constant "sha256" | required | PR-016 | Not nullable |
| `inputs.file_hashes[].value` | sha256 | required | PR-016 | Not nullable |
| `inputs.version_order` | string[] | optional | PR-007 | Not nullable |
| `inputs.version_order[]` | string | required | PR-007 | Not nullable |
| `inputs.version_order_source` | string or null | optional | PR-007 | Explicitly not applicable/unavailable as described above |
| `inputs.representation` | representation or null | optional | PR-011 / T1 / T2 | Explicitly not applicable/unavailable as described above |
| `inputs.scope` | scope | optional | PR-002 | Not nullable |
| `inputs.schema_mapping` | object | optional | PR-003 | Not nullable |
| `inputs.schema_mapping.file_hash` | sha256 or null | required | PR-003 | Explicitly not applicable/unavailable as described above |
| `inputs.schema_mapping.operations` | object[] | required | PR-003 | Not nullable |
| `inputs.schema_mapping.operations[]` | object | required | PR-003 | Not nullable |
| `inputs.schema_mapping.operations[].operation` | enum: rename, trim, cast_string, cast_integer, cast_float, cast_boolean, parse_datetime, parse_json_list, constant, coalesce, map_values, normalize_whitespace, lowercase, uppercase | required | PR-003 | Not nullable |
| `inputs.schema_mapping.operations[].source_field` | string or null | required | PR-003 | Explicitly not applicable/unavailable as described above |
| `inputs.schema_mapping.operations[].target_field` | string | required | PR-003 | Not nullable |
| `inputs.schema_mapping.fields_affected` | string[] | required | PR-003 | Not nullable |
| `inputs.schema_mapping.fields_affected[]` | string | required | PR-003 | Not nullable |
| `inputs.schema_mapping.unmapped_field_count` | integer | required | PR-003 | Not nullable |
| `inputs.schema_mapping.unsafe_operation_count` | constant 0 | required | PR-003 | Not nullable |
| `inputs.limitations` | string[] | optional | PR-002 | Not nullable |
| `inputs.limitations[]` | string | required | PR-002 | Not nullable |

### `observability`

| Path | Type | Required | Owner | Null meaning |
|---|---|---|---|---|
| `observability` | constraint or constraint | required | PR-010 | Not nullable |
| `observability.maximum_level` | integer | optional | PR-010 | Not nullable |
| `observability.level_label` | enum: ingest_observability, content_or_representation_observability, provenance_observability, lineage_observability, longitudinal_dataset_observability, experimental_intervention_or_scenario_observability | optional | PR-010 | Not nullable |
| `observability.basis` | string[] | optional | PR-010 | Not nullable |
| `observability.basis[]` | string | required | PR-010 | Not nullable |
| `observability.limitations` | string[] | optional | PR-010 | Not nullable |
| `observability.limitations[]` | string | required | PR-010 | Not nullable |
| `observability.partial_evidence` | string[] | optional | PR-010 | Not nullable |
| `observability.partial_evidence[]` | string | required | PR-010 | Not nullable |
| `observability.capabilities` | capabilities | optional | PR-011 | Not nullable |

### `capabilities`

| Path | Type | Required | Owner | Null meaning |
|---|---|---|---|---|
| `capabilities` | capabilities | required | PR-011 | Not nullable |

### `observed_facts`

| Path | Type | Required | Owner | Null meaning |
|---|---|---|---|---|
| `observed_facts` | object | required | Enclosing registered owner | Not nullable |
| `observed_facts.record_counts` | object | optional | Enclosing registered owner | Not nullable |
| `observed_facts.record_counts.*` | object | required | Enclosing registered owner | Not nullable |
| `observed_facts.content` | object | optional | Enclosing registered owner | Not nullable |
| `observed_facts.content.duplicate_record_count` | object | optional | Enclosing registered owner | Not nullable |
| `observed_facts.content.duplicate_group_count` | object | optional | Enclosing registered owner | Not nullable |
| `observed_facts.content.exact_duplicate_groups` | object | optional | Enclosing registered owner | Not nullable |
| `observed_facts.provenance` | object | optional | Enclosing registered owner | Not nullable |
| `observed_facts.provenance.provenance_row_coverage` | object | optional | Enclosing registered owner | Not nullable |
| `observed_facts.provenance.provenance_required_field_coverage` | object | optional | Enclosing registered owner | Not nullable |
| `observed_facts.provenance.grounding_field_coverage` | object | optional | Enclosing registered owner | Not nullable |
| `observed_facts.provenance.source_type_field_coverage` | object | optional | Enclosing registered owner | Not nullable |
| `observed_facts.provenance.provenance_confidence_field_coverage` | object | optional | Enclosing registered owner | Not nullable |
| `observed_facts.provenance.source_type_counts` | object | optional | Enclosing registered owner | Not nullable |
| `observed_facts.provenance.provenance_confidence_counts` | object | optional | Enclosing registered owner | Not nullable |
| `observed_facts.provenance.analyzed_record_count` | object | optional | Enclosing registered owner | Not nullable |
| `observed_facts.provenance.records_with_matching_rows` | object | optional | Enclosing registered owner | Not nullable |
| `observed_facts.provenance.missing_provenance_count` | object | optional | Enclosing registered owner | Not nullable |
| `observed_facts.provenance.known_open_count` | object | optional | Enclosing registered owner | Not nullable |
| `observed_facts.provenance.known_closed_count` | object | optional | Enclosing registered owner | Not nullable |
| `observed_facts.provenance.unresolved_grounding_count` | object | optional | Enclosing registered owner | Not nullable |
| `observed_facts.lineage` | object | optional | Enclosing registered owner | Not nullable |
| `observed_facts.lineage.declared_parent_edge_count` | object | optional | Enclosing registered owner | Not nullable |
| `observed_facts.lineage.resolved_parent_edge_count` | object | optional | Enclosing registered owner | Not nullable |
| `observed_facts.lineage.unresolved_parent_edge_count` | object | optional | Enclosing registered owner | Not nullable |
| `observed_facts.lineage.cycle_status` | object | optional | Enclosing registered owner | Not nullable |
| `observed_facts.lineage.ordering_certificate` | object | optional | Enclosing registered owner | Not nullable |
| `observed_facts.state_counts` | object | optional | Enclosing registered owner | Not nullable |
| `observed_facts.state_counts.by_version` | object | optional | Enclosing registered owner | Not nullable |
| `observed_facts.state_counts.by_version.*` | object | required | Enclosing registered owner | Not nullable |
| `observed_facts.supplied_state_probabilities` | object | optional | Enclosing registered owner | Not nullable |
| `observed_facts.supplied_state_probabilities.by_version` | object | optional | Enclosing registered owner | Not nullable |
| `observed_facts.supplied_state_probabilities.by_version.*` | object | required | Enclosing registered owner | Not nullable |

### `derived_metrics`

| Path | Type | Required | Owner | Null meaning |
|---|---|---|---|---|
| `derived_metrics` | object | required | Enclosing registered owner | Not nullable |
| `derived_metrics.support` | object | optional | Enclosing registered owner | Not nullable |
| `derived_metrics.support.by_version` | object | optional | Enclosing registered owner | Not nullable |
| `derived_metrics.support.by_version.*` | object | required | Enclosing registered owner | Not nullable |
| `derived_metrics.support.by_version.*.support_size` | object | optional | Enclosing registered owner | Not nullable |
| `derived_metrics.support.by_version.*.weighted_support_size` | object | optional | Enclosing registered owner | Not nullable |
| `derived_metrics.support.support_delta` | object | optional | Enclosing registered owner | Not nullable |
| `derived_metrics.support.support_retention_ratio` | object | optional | Enclosing registered owner | Not nullable |
| `derived_metrics.support.support_loss_count` | object | optional | Enclosing registered owner | Not nullable |
| `derived_metrics.support.support_added_count` | object | optional | Enclosing registered owner | Not nullable |
| `derived_metrics.support.extinct_states` | object | optional | Enclosing registered owner | Not nullable |
| `derived_metrics.support.added_states` | object | optional | Enclosing registered owner | Not nullable |
| `derived_metrics.support.retained_states` | object | optional | Enclosing registered owner | Not nullable |
| `derived_metrics.support.comparison_details` | object | optional | Enclosing registered owner | Not nullable |
| `derived_metrics.diversity` | object | optional | Enclosing registered owner | Not nullable |
| `derived_metrics.diversity.by_version` | object | optional | Enclosing registered owner | Not nullable |
| `derived_metrics.diversity.by_version.*` | object | required | Enclosing registered owner | Not nullable |
| `derived_metrics.diversity.by_version.*.gini_simpson_diversity` | object | optional | Enclosing registered owner | Not nullable |
| `derived_metrics.diversity.by_version.*.simpson_concentration` | object | optional | Enclosing registered owner | Not nullable |
| `derived_metrics.diversity.by_version.*.weighted_gini_simpson_diversity` | object | optional | Enclosing registered owner | Not nullable |
| `derived_metrics.diversity.by_version.*.weighted_simpson_concentration` | object | optional | Enclosing registered owner | Not nullable |
| `derived_metrics.diversity.by_version.*.state_frequencies` | object | optional | Enclosing registered owner | Not nullable |
| `derived_metrics.diversity.by_version.*.weighted_state_frequencies` | object | optional | Enclosing registered owner | Not nullable |
| `derived_metrics.diversity.by_version.*.weighted_state_masses` | object | optional | Enclosing registered owner | Not nullable |
| `derived_metrics.diversity.by_version.*.distribution_basis` | object | optional | Enclosing registered owner | Not nullable |
| `derived_metrics.diversity.gini_simpson_diversity_delta` | object | optional | Enclosing registered owner | Not nullable |
| `derived_metrics.tail` | object | optional | T2 / PR-016 | Not nullable |
| `derived_metrics.tail.tail_support_size` | object | optional | T2 / PR-016 | Not nullable |
| `derived_metrics.tail.tail_record_share` | object | optional | T2 / PR-016 | Not nullable |
| `derived_metrics.tail.rarity_ranking` | object | optional | T2 / PR-016 | Not nullable |
| `derived_metrics.tail.tail_states` | object | optional | T2 / PR-016 | Not nullable |
| `derived_metrics.tail.tail_rule` | enum: singleton_count, count_at_or_below, frequency_at_or_below, state_list | optional | T2 / PR-016 | Not nullable |
| `derived_metrics.tail.selection` | tail_selection | optional | T2 / PR-016 | Not nullable |
| `derived_metrics.provenance` | object | optional | Enclosing registered owner | Not nullable |
| `derived_metrics.provenance.source_type_shares` | object | optional | Enclosing registered owner | Not nullable |
| `derived_metrics.provenance.weighted_source_type_shares` | object | optional | Enclosing registered owner | Not nullable |
| `derived_metrics.provenance.weighted_source_type_masses` | object | optional | Enclosing registered owner | Not nullable |
| `derived_metrics.provenance.total_weight` | object | optional | Enclosing registered owner | Not nullable |
| `derived_metrics.provenance.missing_provenance_weight` | object | optional | Enclosing registered owner | Not nullable |
| `derived_metrics.provenance.missing_provenance_share` | object | optional | Enclosing registered owner | Not nullable |
| `derived_metrics.provenance.weighted_missing_provenance_share` | object | optional | Enclosing registered owner | Not nullable |
| `derived_metrics.closure_exposure` | object | optional | T3 | Not nullable |
| `derived_metrics.closure_exposure.direct` | object | optional | T3 | Not nullable |
| `derived_metrics.closure_exposure.direct.lower_bound` | object | optional | T3 | Not nullable |
| `derived_metrics.closure_exposure.direct.upper_bound` | object | optional | T3 | Not nullable |
| `derived_metrics.closure_exposure.direct.interval_width` | object | optional | T3 | Not nullable |
| `derived_metrics.closure_exposure.direct.classification_basis` | constant "toolkit_operationalization" | optional | T3 | Not nullable |
| `derived_metrics.closure_exposure.direct.confidence_disclosure` | constant "provenance_confidence_is_separate_and_does_not_discount_grounding" | optional | T3 | Not nullable |
| `derived_metrics.closure_exposure.lineage` | object | optional | T3 | Not nullable |
| `derived_metrics.closure_exposure.lineage.lower_bound` | object | optional | T3 | Not nullable |
| `derived_metrics.closure_exposure.lineage.upper_bound` | object | optional | T3 | Not nullable |
| `derived_metrics.closure_exposure.lineage.interval_width` | object | optional | T3 | Not nullable |
| `derived_metrics.lineage` | object | optional | Enclosing registered owner | Not nullable |
| `derived_metrics.lineage.resolved_parent_edge_coverage` | object | optional | Enclosing registered owner | Not nullable |
| `derived_metrics.lineage.resolved_lineage_coverage` | object | optional | Enclosing registered owner | Not nullable |
| `derived_metrics.lineage.external_ancestry_coverage` | object | optional | Enclosing registered owner | Not nullable |
| `derived_metrics.lineage.distinct_external_root_count` | object | optional | Enclosing registered owner | Not nullable |
| `derived_metrics.lineage.top_shared_ancestors` | object | optional | Enclosing registered owner | Not nullable |
| `derived_metrics.lineage.ancestry_concentration_hhi` | object | optional | Enclosing registered owner | Not nullable |
| `derived_metrics.lineage.effective_external_root_count` | object | optional | Enclosing registered owner | Not nullable |
| `derived_metrics.lineage.lineage_depth` | object | optional | Enclosing registered owner | Not nullable |

### `proxy_signals`

| Path | Type | Required | Owner | Null meaning |
|---|---|---|---|---|
| `proxy_signals` | object | required | Enclosing registered owner | Not nullable |
| `proxy_signals.support_contraction` | object | optional | Enclosing registered owner | Not nullable |
| `proxy_signals.tail_fragility` | object | optional | Enclosing registered owner | Not nullable |
| `proxy_signals.shared_ancestry_dependence` | object | optional | Enclosing registered owner | Not nullable |
| `proxy_signals.provenance_uncertainty` | object | optional | Enclosing registered owner | Not nullable |

### `simulations`

| Path | Type | Required | Owner | Null meaning |
|---|---|---|---|---|
| `simulations` | object | required | Enclosing registered owner | Not nullable |
| `simulations.closed_resampling` | object | optional | Enclosing registered owner | Not nullable |
| `simulations.tail_extinction` | object | optional | Enclosing registered owner | Not nullable |
| `simulations.external_reopening` | forbidden in Phase 4 | optional | Enclosing registered owner | Not nullable |

### `unavailable_conclusions`

| Path | Type | Required | Owner | Null meaning |
|---|---|---|---|---|
| `unavailable_conclusions` | one registered variant[] | required | Enclosing registered owner | Not nullable |
| `unavailable_conclusions[]` | one registered variant | required | Enclosing registered owner | Not nullable |

### `recommended_next_metadata`

| Path | Type | Required | Owner | Null meaning |
|---|---|---|---|---|
| `recommended_next_metadata` | object[] | required | PR-014 | Not nullable |
| `recommended_next_metadata[]` | object | required | PR-014 | Not nullable |
| `recommended_next_metadata[].priority` | integer | required | PR-014 | Not nullable |
| `recommended_next_metadata[].metadata` | string | required | PR-014 | Not nullable |
| `recommended_next_metadata[].scope` | string | required | PR-014 | Not nullable |
| `recommended_next_metadata[].expected_unlock` | string[] | required | PR-014 | Not nullable |
| `recommended_next_metadata[].expected_unlock[]` | string | required | PR-014 | Not nullable |
| `recommended_next_metadata[].reason` | string | required | PR-014 | Not nullable |
| `recommended_next_metadata[].owner_ids` | constant ["PR-014"] | optional | PR-014 | Not nullable |

### `warnings`

| Path | Type | Required | Owner | Null meaning |
|---|---|---|---|---|
| `warnings` | object[] | required | PR-014 | Not nullable |
| `warnings[]` | object | required | PR-014 | Not nullable |
| `warnings[].code` | string | required | PR-014 | Not nullable |
| `warnings[].message` | string | required | PR-014 | Not nullable |
| `warnings[].count` | integer | required | PR-014 | Not nullable |
| `warnings[].affected_scope` | scope | required | PR-014 | Not nullable |
| `warnings[].representative_locations` | location[] | required | PR-014 | Not nullable |
| `warnings[].representative_locations[]` | location | required | PR-014 | Not nullable |
| `warnings[].effect_on_capabilities` | enum: ingestion, content_diagnostics, provenance, lineage, dataset_longitudinal, model_longitudinal, intervention_simulation[] | required | PR-014 | Not nullable |
| `warnings[].effect_on_capabilities[]` | enum: ingestion, content_diagnostics, provenance, lineage, dataset_longitudinal, model_longitudinal, intervention_simulation | required | PR-014 | Not nullable |
| `warnings[].remediation` | string[] | required | PR-014 | Not nullable |
| `warnings[].remediation[]` | string | required | PR-014 | Not nullable |
| `warnings[].coverage` | coverage or null | optional | PR-014 | Explicitly not applicable/unavailable as described above |
| `warnings[].severity` | constant "warning" | optional | PR-014 | Not nullable |

### `errors`

| Path | Type | Required | Owner | Null meaning |
|---|---|---|---|---|
| `errors` | object[] | required | PR-014 | Not nullable |
| `errors[]` | object | required | PR-014 | Not nullable |
| `errors[].code` | string | required | PR-014 | Not nullable |
| `errors[].severity` | enum: error, fatal | required | PR-014 | Not nullable |
| `errors[].message` | string | required | PR-014 | Not nullable |
| `errors[].file_role` | string or null | required | PR-014 | Explicitly not applicable/unavailable as described above |
| `errors[].field` | string or null | required | PR-014 | Explicitly not applicable/unavailable as described above |
| `errors[].record_key` | record_key or null | required | PR-014 | Explicitly not applicable/unavailable as described above |
| `errors[].row_number` | integer or null | required | PR-014 | Explicitly not applicable/unavailable as described above |
| `errors[].effect_on_run` | enum: partial, failed | required | PR-014 | Not nullable |
| `errors[].effect_on_capabilities` | enum: ingestion, content_diagnostics, provenance, lineage, dataset_longitudinal, model_longitudinal, intervention_simulation[] | required | PR-014 | Not nullable |
| `errors[].effect_on_capabilities[]` | enum: ingestion, content_diagnostics, provenance, lineage, dataset_longitudinal, model_longitudinal, intervention_simulation | required | PR-014 | Not nullable |
| `errors[].remediation` | string[] | required | PR-014 | Not nullable |
| `errors[].remediation[]` | string | required | PR-014 | Not nullable |

## Shared typed contracts

These tables enumerate every public field of a shared object, including scenario arrays. Presence requirements are local to that object. `scope`, representation, coverage and weighting inherit the analytical owner where embedded; their schema validity is owned by PR-013. Run/config controls are owned by PR-016, capability metadata by PR-011, and record/diagnostic locations by PR-002/PR-014.

### `sha256`

| Relative path | Type | Required |
|---|---|---|
| `sha256` | string | required |

### `record_key`

| Relative path | Type | Required |
|---|---|---|
| `record_key` | object | required |
| `record_key.dataset_version` | string | required |
| `record_key.record_id` | string | required |

### `scope`

| Relative path | Type | Required |
|---|---|---|
| `scope` | object | required |
| `scope.dataset_versions` | string[] | required |
| `scope.dataset_versions[]` | string | required |
| `scope.record_count` | integer or null | required |
| `scope.excluded_record_count` | integer or null | required |
| `scope.denominator_basis` | string | required |
| `scope.scope_id` | string | required |
| `scope.included_record_keys` | record_key[] | optional |
| `scope.included_record_keys[]` | record_key | required |
| `scope.excluded_record_keys` | record_key[] | optional |
| `scope.excluded_record_keys[]` | record_key | required |
| `scope.exclusions` | object[] | optional |
| `scope.exclusions[]` | object | required |
| `scope.exclusions[].record_key` | record_key | required |
| `scope.exclusions[].reason_codes` | string[] | required |
| `scope.exclusions[].reason_codes[]` | string | required |

### `representation`

| Relative path | Type | Required |
|---|---|---|
| `representation` | object | required |
| `representation.representation_name` | string | required |
| `representation.representation_source` | string | required |
| `representation.representation_version` | string | required |
| `representation.binning_or_mapping_rule` | string | required |
| `representation.field_name` | string or null | optional |
| `representation.missing_value_policy` | enum: error, exclude, explicit_missing_state | optional |
| `representation.missing_state_id` | string or null | optional |
| `representation.normalization_profile` | constant "exact_utf8_v1" or null | optional |

### `coverage`

| Relative path | Type | Required |
|---|---|---|
| `coverage` | object | required |
| `coverage.numerator` | integer | required |
| `coverage.denominator` | integer | required |
| `coverage.denominator_name` | string | required |
| `coverage.ratio` | number or null | required |
| `coverage.reason` | string or null | required |

### `capability`

| Relative path | Type | Required |
|---|---|---|
| `capability` | object | required |
| `capability.status` | enum: available, partial, unavailable, experimental | required |
| `capability.reason_codes` | string[] | required |
| `capability.reason_codes[]` | string | required |
| `capability.coverage` | number or null | required |
| `capability.coverage_reason` | string or null | required |
| `capability.requirements_met` | string[] | required |
| `capability.requirements_met[]` | string | required |
| `capability.requirements_missing` | string[] | required |
| `capability.requirements_missing[]` | string | required |
| `capability.notes` | string[] | required |
| `capability.notes[]` | string | required |
| `capability.execution_status` | enum: completed, partial, not_requested, deferred, failed | required |
| `capability.execution_scope` | string[] | required |
| `capability.execution_scope[]` | string | required |
| `capability.execution_reason_codes` | string[] | required |
| `capability.execution_reason_codes[]` | string | required |
| `capability.coverage_details` | object | optional |
| `capability.coverage_details.record_coverage` | coverage | optional |
| `capability.coverage_details.representation_coverage` | coverage | optional |
| `capability.coverage_details.provenance_row_coverage` | coverage | optional |
| `capability.coverage_details.provenance_required_field_coverage` | coverage | optional |
| `capability.coverage_details.grounding_field_coverage` | coverage | optional |
| `capability.coverage_details.source_type_field_coverage` | coverage | optional |
| `capability.coverage_details.provenance_confidence_field_coverage` | coverage | optional |
| `capability.coverage_details.resolved_parent_edge_coverage` | coverage | optional |
| `capability.coverage_details.resolved_lineage_coverage` | coverage | optional |
| `capability.coverage_details.external_ancestry_coverage` | coverage | optional |

### `capabilities`

| Relative path | Type | Required |
|---|---|---|
| `capabilities` | constraint or constraint | required |
| `capabilities.ingestion` | capability | optional |
| `capabilities.content_diagnostics` | capability | optional |
| `capabilities.provenance` | capability | optional |
| `capabilities.lineage` | capability | optional |
| `capabilities.dataset_longitudinal` | capability | optional |
| `capabilities.model_longitudinal` | capability | optional |
| `capabilities.intervention_simulation` | capability | optional |

### `weighting`

| Relative path | Type | Required |
|---|---|---|
| `weighting` | object | required |
| `weighting.weighting_mode` | enum: unweighted, weighted | required |
| `weighting.weight_field` | constant "weight" or null | required |

### `redaction`

| Relative path | Type | Required |
|---|---|---|
| `redaction` | object | required |
| `redaction.omitted_fields` | string[] | required |
| `redaction.omitted_fields[]` | string | required |
| `redaction.reason` | constant "redacted_identity_details" | required |

### `tail_selection`

| Relative path | Type | Required |
|---|---|---|
| `tail_selection` | object | required |
| `tail_selection.rule` | enum: singleton_count, count_at_or_below, frequency_at_or_below, state_list | required |
| `tail_selection.count_threshold` | integer or null | required |
| `tail_selection.frequency_threshold` | number or null | required |
| `tail_selection.state_ids` | string[] | required |
| `tail_selection.state_ids[]` | string | required |
| `tail_selection.ranking_rule` | constant "ascending_frequency_then_count_then_unicode_state_id" | required |

### `resolved_options`

| Relative path | Type | Required |
|---|---|---|
| `resolved_options` | object | required |
| `resolved_options.strict_mode` | boolean | optional |
| `resolved_options.privacy_mode` | enum: standard, redacted | optional |
| `resolved_options.record_id_mode` | enum: preserve, hash, omit | optional |
| `resolved_options.representation` | representation or null | optional |
| `resolved_options.tail_selection` | tail_selection or null | optional |
| `resolved_options.version_order` | string[] | optional |
| `resolved_options.version_order[]` | string | required |
| `resolved_options.state_meaning` | string or null | optional |
| `resolved_options.weighted` | boolean | optional |
| `resolved_options.comparison_requested` | boolean | optional |
| `resolved_options.scenario_requested` | boolean | optional |

### `state_probability`

| Relative path | Type | Required |
|---|---|---|
| `state_probability` | object | required |
| `state_probability.state_id` | string | required |
| `state_probability.probability` | number | required |

### `simulation_parameters`

| Relative path | Type | Required |
|---|---|---|
| `simulation_parameters` | object | required |
| `simulation_parameters.resample_size` | integer | required |
| `simulation_parameters.simulation_horizon` | integer | required |
| `simulation_parameters.random_seed` | integer or null | required |
| `simulation_parameters.simulation_replicates` | integer or null | required |
| `simulation_parameters.rng_name` | constant "numpy.random.Generator(PCG64)" or null | required |
| `simulation_parameters.numpy_version` | string or null | required |
| `simulation_parameters.replicate_schedule` | constant "replicate_major_step_major" or null | required |
| `simulation_parameters.state_order` | string[] | required |
| `simulation_parameters.state_order[]` | string | required |
| `simulation_parameters.input_basis` | string | required |
| `simulation_parameters.reopening_weight` | number or null | required |
| `simulation_parameters.external_input_distribution` | state_probability[] | required |
| `simulation_parameters.external_input_distribution[]` | state_probability | required |
| `simulation_parameters.numerical_policy` | numerical_policy | required |

### `numerical_policy`

| Relative path | Type | Required |
|---|---|---|
| `numerical_policy` | object | required |
| `numerical_policy.absolute_tolerance` | constant 1e-12 | required |
| `numerical_policy.relative_tolerance` | constant 1e-12 | required |
| `numerical_policy.probability_mass_tolerance` | constant 1e-12 | required |

### `sampled_path`

| Relative path | Type | Required |
|---|---|---|
| `sampled_path` | object | required |
| `sampled_path.replicate_index` | integer | required |
| `sampled_path.generations` | object[] | required |
| `sampled_path.generations[]` | object | required |
| `sampled_path.generations[].step` | integer | required |
| `sampled_path.generations[].state_counts` | integer[] or null | required |
| `sampled_path.generations[].state_frequencies` | number[] | required |
| `sampled_path.generations[].state_frequencies[]` | number | required |
| `sampled_path.generations[].support` | string[] | required |
| `sampled_path.generations[].support[]` | string | required |
| `sampled_path.generations[].support_size` | integer | required |
| `sampled_path.generations[].gini_simpson_diversity` | number | required |

### `input_normalization`

| Relative path | Type | Required |
|---|---|---|
| `input_normalization` | object | required |
| `input_normalization.supplied_distribution` | state_probability[] | required |
| `input_normalization.supplied_distribution[]` | state_probability | required |
| `input_normalization.effective_distribution` | state_probability[] | required |
| `input_normalization.effective_distribution[]` | state_probability | required |
| `input_normalization.supplied_probability_total` | number | required |
| `input_normalization.effective_probability_total` | number | required |
| `input_normalization.probability_residual` | number | required |
| `input_normalization.correction_applied` | boolean | required |
| `input_normalization.correction_method` | string | required |
| `input_normalization.normalization_divisor` | number | required |
| `input_normalization.probability_corrections` | object[] | required |
| `input_normalization.probability_corrections[]` | object | required |
| `input_normalization.probability_corrections[].state_id` | string | required |
| `input_normalization.probability_corrections[].correction` | number | required |

### `location`

| Relative path | Type | Required |
|---|---|---|
| `location` | object | required |
| `location.file_role` | string or null | required |
| `location.field` | string or null | required |
| `location.record_key` | record_key or null | required |
| `location.row_number` | integer or null | required |
| `location.line_number` | integer or null | required |

## Common envelope fields

| Field | Type | Owner / null rule |
|---|---|---|
| `value` | Registered scalar/table or null | Only scalar/table envelopes; unavailable means null with reasons |
| `unit`, `evidence_class`, `method_id`, `owner_ids` | Exact registry constants | Enclosing field owner; never null |
| `theory_map_ids`, `trace_ids` | Unique registered ID arrays | Trace ownership; never null |
| `status` | Registered status enum | Available/partial/unavailable; simulation is experimental |
| `scope` | scope object | Exact included/excluded scope; never null |
| `representation` | descriptor or null | Representation-dependent available fields require a descriptor |
| `coverage`, `coverage_reason` | ratio or null, text or null | Exactly one of value/reason is non-null |
| `denominator`, `denominator_reason` | finite nonnegative number or null, text or null | Exactly one of value/reason is non-null |
| `assumptions`, `limitations` | Unique text arrays | Original limits; scenarios and proxies require limitations |
| `reason_codes`, `required_evidence` | Unique text arrays | Unavailable requires nonempty arrays |
| `weighting` | optional weighting object | Required on weighted companions; unweighted is the documented default |
| `input_basis`, `method` | optional literal text | Preserve accepted kernel basis/method; never execute |
| `redaction` | optional redaction object | Declared identity omission; no missing-evidence substitution |

## Scenario variants

All emitted scenario evidence remains `simulation` and `experimental`. The common method metadata fixes sample size, horizon, seed/replicate/RNG identities, representation, numerical policy and limitations. Closed-model parameters cannot carry an external reopening weight or distribution.

`simulations.tail_extinction` retains the frozen `model`, `resample_size` and `by_state.*.one_step_extinction_probability` paths. Each state also has `observed_frequency` and `numerical_underflow`. It represents the existing analytic one-step selected-state marginal; an empty initial-distribution array is honest when no complete vector was supplied. Seeds and random-generator metadata must be null.

`simulations.closed_resampling` retains direct `expected_diversity`, `sampled_paths`, `support_trajectories` and `extinction_events` paths. Analytic expectation requires the supplied expectation vector, initial diversity, contraction factor and underflow steps; its vector length is horizon plus one. Sampled paths require seed, replicate count, NumPy/RNG identity and scheduling metadata. Path count must equal replicate count. Optional support trajectories and events may only preserve evidence already supplied by the accepted owner; their presence does not authorize the adapter or renderer to calculate them.

`simulations.external_reopening` is a registered future field, explicitly rejected by this Phase 4 schema and constructor. `external_reference_loss` has no approved public trace and is unregistered. Neither is executed. The lack of implementation belongs in capability execution reasons and unavailable conclusions.

## Path reconciliation and unchanged meaning

| Source discrepancy | Adopted path / behavior | Basis |
|---|---|---|
| Reporting §15.2 calls provenance coverage derived | Three separate `observed_facts.provenance.*_coverage` entries | P4 §4.2 explicitly selects frozen registry §32 |
| SPEC_AUDIT B02 versus top-level capability matrix | Top-level matrix plus exact shared `observability.capabilities` mirror | P4-D02 |
| Older planned `records_missing_rows` | `observed_facts.provenance.missing_provenance_count` | Accepted Phase 3 type and later product registry; old alias rejected |
| Existing `TailSelectionResult.tail_membership` | Public `derived_metrics.tail.tail_states`, plus `tail_rule` and typed selection metadata | Frozen planned public path; explicit adapter mapping, no numerical change |
| Existing duplicate group object | `observed_facts.content.exact_duplicate_groups` | Frozen PR-006 planned public path |
| Reporting operations-applied description | `inputs.schema_mapping.operations` with the exact accepted operation enum | Frozen PR-003 planned path and Phase 2 dispatcher |
| Old `cycle_detected` and cycle-status detail sketches | Registered `observed_facts.lineage.cycle_status` is an unavailable envelope | Registry §32 and P4-D01; graph operations remain Phase 5 |
| Reporting simplified proxy example uses `status: present` | `level: present`, independent availability status | Full reporting §9.3/§16.6 |
| Older privacy enum includes debug | Public Phase 4 privacy mode is standard or redacted | Approved Phase 4 Step 4 boundary |

The record-count and provenance denominators never shrink because representation-specific rows were excluded. Missing rows remain distinct from declared unknown categories. Null, empty sets, zero, unavailable calculations and redacted identities retain separate meanings. Validation does not recompute formulas, calibrate proxies, create graph results or raise input observability.

## Class-specific and structured value fields

The following additional fields are part of the registered envelopes, with the owner/class inherited from the exact analytical path above. This enumeration supplements the common envelope table; no free-form payload fields are allowed. Local `$defs` payloads use the complete shared-contract tables.

| Envelope path | Additional field | Type | Required |
|---|---|---|---|
| `observed_facts.record_counts.*` | `method` | string | optional |
| `observed_facts.content.duplicate_record_count` | `method` | string | optional |
| `observed_facts.content.duplicate_group_count` | `method` | string | optional |
| `observed_facts.content.exact_duplicate_groups` | `method` | string | optional |
| `observed_facts.content.exact_duplicate_groups` | `value[].group_id` | string | required |
| `observed_facts.content.exact_duplicate_groups` | `value[].record_keys` | record_key[] or null | required |
| `observed_facts.content.exact_duplicate_groups` | `value[].record_count` | integer | required |
| `observed_facts.content.exact_duplicate_groups` | `value[].normalization_profile` | constant "exact_utf8_v1" | required |
| `observed_facts.content.exact_duplicate_groups` | `value[].redaction` | redaction | optional |
| `observed_facts.provenance.provenance_row_coverage` | `method` | string | optional |
| `observed_facts.provenance.provenance_required_field_coverage` | `method` | string | optional |
| `observed_facts.provenance.grounding_field_coverage` | `method` | string | optional |
| `observed_facts.provenance.source_type_field_coverage` | `method` | string | optional |
| `observed_facts.provenance.provenance_confidence_field_coverage` | `method` | string | optional |
| `observed_facts.provenance.source_type_counts` | `method` | string | optional |
| `observed_facts.provenance.source_type_counts` | `value.human` | integer | required |
| `observed_facts.provenance.source_type_counts` | `value.synthetic` | integer | required |
| `observed_facts.provenance.source_type_counts` | `value.mixed` | integer | required |
| `observed_facts.provenance.source_type_counts` | `value.sensor` | integer | required |
| `observed_facts.provenance.source_type_counts` | `value.unknown` | integer | required |
| `observed_facts.provenance.provenance_confidence_counts` | `method` | string | optional |
| `observed_facts.provenance.provenance_confidence_counts` | `value.confirmed` | integer | required |
| `observed_facts.provenance.provenance_confidence_counts` | `value.log_derived` | integer | required |
| `observed_facts.provenance.provenance_confidence_counts` | `value.estimated` | integer | required |
| `observed_facts.provenance.provenance_confidence_counts` | `value.unknown` | integer | required |
| `observed_facts.provenance.analyzed_record_count` | `method` | string | optional |
| `observed_facts.provenance.records_with_matching_rows` | `method` | string | optional |
| `observed_facts.provenance.missing_provenance_count` | `method` | string | optional |
| `observed_facts.provenance.known_open_count` | `method` | string | optional |
| `observed_facts.provenance.known_closed_count` | `method` | string | optional |
| `observed_facts.provenance.unresolved_grounding_count` | `method` | string | optional |
| `observed_facts.lineage.declared_parent_edge_count` | `method` | string | optional |
| `observed_facts.lineage.resolved_parent_edge_count` | `method` | string | optional |
| `observed_facts.lineage.unresolved_parent_edge_count` | `method` | string | optional |
| `observed_facts.lineage.cycle_status` | `method` | string | optional |
| `observed_facts.lineage.ordering_certificate` | `method` | string | optional |
| `observed_facts.lineage.ordering_certificate` | `value.method` | constant "declared_earlier_version_order" | required |
| `observed_facts.lineage.ordering_certificate` | `value.version_order` | string[] | required |
| `observed_facts.lineage.ordering_certificate` | `value.all_resolved_edges_follow_order` | boolean | required |
| `observed_facts.state_counts.by_version.*` | `method` | string | optional |
| `observed_facts.state_counts.by_version.*` | `value[].state_id` | string | required |
| `observed_facts.state_counts.by_version.*` | `value[].state_count` | integer | required |
| `observed_facts.supplied_state_probabilities.by_version.*` | `method` | string | optional |
| `derived_metrics.support.by_version.*.support_size` | `method` | string | optional |
| `derived_metrics.support.by_version.*.weighted_support_size` | `method` | string | optional |
| `derived_metrics.support.support_delta` | `method` | string | optional |
| `derived_metrics.support.support_retention_ratio` | `method` | string | optional |
| `derived_metrics.support.support_loss_count` | `method` | string | optional |
| `derived_metrics.support.support_added_count` | `method` | string | optional |
| `derived_metrics.support.extinct_states` | `method` | string | optional |
| `derived_metrics.support.added_states` | `method` | string | optional |
| `derived_metrics.support.retained_states` | `method` | string | optional |
| `derived_metrics.support.comparison_details` | `method` | string | optional |
| `derived_metrics.support.comparison_details` | `value.earlier_version` | string | required |
| `derived_metrics.support.comparison_details` | `value.later_version` | string | required |
| `derived_metrics.support.comparison_details` | `value.version_order` | string[] | required |
| `derived_metrics.support.comparison_details` | `value.version_order_source` | string | required |
| `derived_metrics.support.comparison_details` | `value.earlier_state_semantics` | string | required |
| `derived_metrics.support.comparison_details` | `value.later_state_semantics` | string | required |
| `derived_metrics.support.comparison_details` | `value.harmonized_state_semantics` | string | required |
| `derived_metrics.support.comparison_details` | `value.compatibility_method` | string | required |
| `derived_metrics.support.comparison_details` | `value.earlier_representation` | representation | required |
| `derived_metrics.support.comparison_details` | `value.later_representation` | representation | required |
| `derived_metrics.support.comparison_details` | `value.harmonized_representation` | representation | required |
| `derived_metrics.support.comparison_details` | `value.original_earlier_support` | string[] | required |
| `derived_metrics.support.comparison_details` | `value.original_later_support` | string[] | required |
| `derived_metrics.support.comparison_details` | `value.harmonized_earlier_support` | string[] | required |
| `derived_metrics.support.comparison_details` | `value.harmonized_later_support` | string[] | required |
| `derived_metrics.support.comparison_details` | `value.retention_denominator` | integer or null | required |
| `derived_metrics.support.comparison_details` | `value.retention_denominator_basis` | string | required |
| `derived_metrics.support.comparison_details` | `value.state_mapping` | object[] | required |
| `derived_metrics.support.comparison_details` | `value.state_mapping[].source_state` | string | required |
| `derived_metrics.support.comparison_details` | `value.state_mapping[].target_state` | string | required |
| `derived_metrics.support.comparison_details` | `value.mapping_effect` | object[] | required |
| `derived_metrics.support.comparison_details` | `value.mapping_effect[].dataset_version` | string | required |
| `derived_metrics.support.comparison_details` | `value.mapping_effect[].original_support_size` | integer or null | required |
| `derived_metrics.support.comparison_details` | `value.mapping_effect[].harmonized_support_size` | integer or null | required |
| `derived_metrics.support.comparison_details` | `value.collision_groups` | object[] | required |
| `derived_metrics.support.comparison_details` | `value.collision_groups[].target_state` | string | required |
| `derived_metrics.support.comparison_details` | `value.collision_groups[].source_states` | string[] | required |
| `derived_metrics.diversity.by_version.*.gini_simpson_diversity` | `method` | string | optional |
| `derived_metrics.diversity.by_version.*.simpson_concentration` | `method` | string | optional |
| `derived_metrics.diversity.by_version.*.weighted_gini_simpson_diversity` | `method` | string | optional |
| `derived_metrics.diversity.by_version.*.weighted_simpson_concentration` | `method` | string | optional |
| `derived_metrics.diversity.by_version.*.state_frequencies` | `method` | string | optional |
| `derived_metrics.diversity.by_version.*.state_frequencies` | `value[].state_id` | string | required |
| `derived_metrics.diversity.by_version.*.state_frequencies` | `value[].state_frequency` | number | required |
| `derived_metrics.diversity.by_version.*.weighted_state_frequencies` | `method` | string | optional |
| `derived_metrics.diversity.by_version.*.weighted_state_frequencies` | `value[].state_id` | string | required |
| `derived_metrics.diversity.by_version.*.weighted_state_frequencies` | `value[].state_frequency` | number | required |
| `derived_metrics.diversity.by_version.*.weighted_state_masses` | `method` | string | optional |
| `derived_metrics.diversity.by_version.*.weighted_state_masses` | `value[].state_id` | string | required |
| `derived_metrics.diversity.by_version.*.weighted_state_masses` | `value[].state_mass` | number | required |
| `derived_metrics.diversity.by_version.*.distribution_basis` | `method` | string | optional |
| `derived_metrics.diversity.by_version.*.distribution_basis` | `value.input_basis` | enum: empirical_assignments, explicit_counts_divided_by_included_records, weighted_record_mass, explicit_probability_vector | required |
| `derived_metrics.diversity.by_version.*.distribution_basis` | `value.analyzed_record_count` | integer | required |
| `derived_metrics.diversity.by_version.*.distribution_basis` | `value.frequency_denominator` | number or null | required |
| `derived_metrics.diversity.by_version.*.distribution_basis` | `value.denominator_basis` | string | required |
| `derived_metrics.diversity.by_version.*.distribution_basis` | `value.supplied_probability_total` | number or null | required |
| `derived_metrics.diversity.by_version.*.distribution_basis` | `value.probability_residual` | number or null | required |
| `derived_metrics.diversity.by_version.*.distribution_basis` | `value.numerical_policy` | numerical_policy | required |
| `derived_metrics.diversity.gini_simpson_diversity_delta` | `method` | string | optional |
| `derived_metrics.tail.tail_support_size` | `method` | string | optional |
| `derived_metrics.tail.tail_record_share` | `method` | string | optional |
| `derived_metrics.tail.rarity_ranking` | `method` | string | optional |
| `derived_metrics.tail.rarity_ranking` | `value[].state_id` | string | required |
| `derived_metrics.tail.rarity_ranking` | `value[].state_count` | integer | required |
| `derived_metrics.tail.rarity_ranking` | `value[].state_frequency` | number | required |
| `derived_metrics.tail.rarity_ranking` | `value[].rarity_rank` | integer | required |
| `derived_metrics.tail.rarity_ranking` | `value[].in_tail` | boolean | required |
| `derived_metrics.tail.tail_states` | `method` | string | optional |
| `derived_metrics.provenance.source_type_shares` | `method` | string | optional |
| `derived_metrics.provenance.source_type_shares` | `value.human` | number | required |
| `derived_metrics.provenance.source_type_shares` | `value.synthetic` | number | required |
| `derived_metrics.provenance.source_type_shares` | `value.mixed` | number | required |
| `derived_metrics.provenance.source_type_shares` | `value.sensor` | number | required |
| `derived_metrics.provenance.source_type_shares` | `value.unknown` | number | required |
| `derived_metrics.provenance.weighted_source_type_shares` | `method` | string | optional |
| `derived_metrics.provenance.weighted_source_type_shares` | `value.human` | number | required |
| `derived_metrics.provenance.weighted_source_type_shares` | `value.synthetic` | number | required |
| `derived_metrics.provenance.weighted_source_type_shares` | `value.mixed` | number | required |
| `derived_metrics.provenance.weighted_source_type_shares` | `value.sensor` | number | required |
| `derived_metrics.provenance.weighted_source_type_shares` | `value.unknown` | number | required |
| `derived_metrics.provenance.weighted_source_type_masses` | `method` | string | optional |
| `derived_metrics.provenance.weighted_source_type_masses` | `value.human` | number | required |
| `derived_metrics.provenance.weighted_source_type_masses` | `value.synthetic` | number | required |
| `derived_metrics.provenance.weighted_source_type_masses` | `value.mixed` | number | required |
| `derived_metrics.provenance.weighted_source_type_masses` | `value.sensor` | number | required |
| `derived_metrics.provenance.weighted_source_type_masses` | `value.unknown` | number | required |
| `derived_metrics.provenance.total_weight` | `method` | string | optional |
| `derived_metrics.provenance.missing_provenance_weight` | `method` | string | optional |
| `derived_metrics.provenance.missing_provenance_share` | `method` | string | optional |
| `derived_metrics.provenance.weighted_missing_provenance_share` | `method` | string | optional |
| `derived_metrics.closure_exposure.direct.lower_bound` | `method` | string | optional |
| `derived_metrics.closure_exposure.direct.upper_bound` | `method` | string | optional |
| `derived_metrics.closure_exposure.direct.interval_width` | `method` | string | optional |
| `derived_metrics.closure_exposure.lineage.lower_bound` | `method` | string | optional |
| `derived_metrics.closure_exposure.lineage.upper_bound` | `method` | string | optional |
| `derived_metrics.closure_exposure.lineage.interval_width` | `method` | string | optional |
| `derived_metrics.lineage.resolved_parent_edge_coverage` | `method` | string | optional |
| `derived_metrics.lineage.resolved_lineage_coverage` | `method` | string | optional |
| `derived_metrics.lineage.external_ancestry_coverage` | `method` | string | optional |
| `derived_metrics.lineage.distinct_external_root_count` | `method` | string | optional |
| `derived_metrics.lineage.top_shared_ancestors` | `method` | string | optional |
| `derived_metrics.lineage.top_shared_ancestors` | `value[].record_key` | record_key | required |
| `derived_metrics.lineage.top_shared_ancestors` | `value[].incidence_count` | integer | required |
| `derived_metrics.lineage.ancestry_concentration_hhi` | `method` | string | optional |
| `derived_metrics.lineage.effective_external_root_count` | `method` | string | optional |
| `derived_metrics.lineage.lineage_depth` | `method` | string | optional |
| `proxy_signals.support_contraction` | `signal` | constant "support_contraction" | required |
| `proxy_signals.support_contraction` | `level` | enum: present, not_present, indeterminate | required |
| `proxy_signals.support_contraction` | `basis_fields` | string[] | required |
| `proxy_signals.support_contraction` | `trigger_rule` | string | required |
| `proxy_signals.tail_fragility` | `signal` | constant "tail_fragility" | required |
| `proxy_signals.tail_fragility` | `level` | enum: present, not_present, indeterminate | required |
| `proxy_signals.tail_fragility` | `basis_fields` | string[] | required |
| `proxy_signals.tail_fragility` | `trigger_rule` | string | required |
| `proxy_signals.shared_ancestry_dependence` | `signal` | constant "shared_ancestry_dependence" | required |
| `proxy_signals.shared_ancestry_dependence` | `level` | constant "indeterminate" | required |
| `proxy_signals.shared_ancestry_dependence` | `basis_fields` | string[] | required |
| `proxy_signals.shared_ancestry_dependence` | `trigger_rule` | string | required |
| `proxy_signals.provenance_uncertainty` | `signal` | constant "provenance_uncertainty" | required |
| `proxy_signals.provenance_uncertainty` | `level` | enum: present, not_present, indeterminate | required |
| `proxy_signals.provenance_uncertainty` | `basis_fields` | string[] | required |
| `proxy_signals.provenance_uncertainty` | `trigger_rule` | string | required |
| `simulations.closed_resampling` | `model` | constant "closed_resampling" | required |
| `simulations.closed_resampling` | `model_version` | string | required |
| `simulations.closed_resampling` | `method` | enum: analytic_expectation, sampled_path | required |
| `simulations.closed_resampling` | `parameters` | simulation_parameters | required |
| `simulations.closed_resampling` | `initial_distribution` | state_probability[] | required |
| `simulations.closed_resampling` | `resample_size` | integer | required |
| `simulations.closed_resampling` | `initial_gini_simpson_diversity` | number | optional |
| `simulations.closed_resampling` | `contraction_factor` | number | optional |
| `simulations.closed_resampling` | `expected_diversity` | number[] | optional |
| `simulations.closed_resampling` | `numerical_underflow_steps` | integer[] | optional |
| `simulations.closed_resampling` | `sampled_paths` | sampled_path[] | optional |
| `simulations.closed_resampling` | `support_trajectories` | object[] | optional |
| `simulations.closed_resampling` | `extinction_events` | object[] | optional |
| `simulations.closed_resampling` | `input_normalization` | input_normalization | optional |
| `simulations.tail_extinction` | `model` | constant "closed_resampling" | required |
| `simulations.tail_extinction` | `model_version` | string | required |
| `simulations.tail_extinction` | `method` | constant "analytic_extinction" | required |
| `simulations.tail_extinction` | `parameters` | simulation_parameters | required |
| `simulations.tail_extinction` | `initial_distribution` | state_probability[] | required |
| `simulations.tail_extinction` | `resample_size` | integer | required |
| `simulations.tail_extinction` | `by_state` | object | required |
| `unavailable_conclusions[]` | `conclusion` | constant "model_performance_decline" | required |
| `unavailable_conclusions[]` | `statement` | string | required |
| `unavailable_conclusions[]` | `blocking_evidence` | string[] | required |
| `unavailable_conclusions[]` | `required_next_metadata` | string[] | required |
| `unavailable_conclusions[]` | `related_capability` | enum: ingestion, content_diagnostics, provenance, lineage, dataset_longitudinal, model_longitudinal, intervention_simulation | required |
| `unavailable_conclusions[]` | `theory_or_product_limit` | string | required |

`status: unavailable` on a proxy requires `level: indeterminate`; a present signal cannot simultaneously be unavailable. Dataset-version field scopes contain exactly their one literal key. SHA-256 values contain exactly 64 lowercase hexadecimal characters. Extinction-event identity is the composite `(replicate_index, step, state_id)`; distinct states within one replicate remain distinct valid events. Sampled generation arrays have `simulation_horizon + 1` entries.

Privacy identity omission can remove optional scope identity arrays while retaining count/metric envelopes. Exact duplicate groups have a bounded identity-omission variant: `record_keys` is null only with same-group `redaction: {omitted_fields: [record_keys], reason: redacted_identity_details}`. The group ID, full `record_count` and normalization profile remain present. Non-null membership lists retain at least two unique canonical keys and cannot claim that membership was omitted. This declaration does not transform identities, change availability, discard group counts or implement the Step 4 privacy operation.

## Validation ownership and limits

Independent hand-authored PR-012/PR-013 fixtures test schema and canonical construction, five-class placement, unknown keys, null/zero distinctions, nonfinite and boolean values, metadata, immutability, capability mirrors and interval consistency. Schema validation uses only the local file. Runtime additionally enforces cross-field rules such as exact null-reason keys, duplicate table identities, scope membership, mirror equality and interval/trajectory consistency. These constraints supplement JSON Schema without claiming that schema-only validation proves every semantic invariant.

This step creates no report adapters, no Markdown/JSON rendering files, no CLI analysis command and no Phase 4 completion claim.

## Phase 4 Step 3: explicit evidence assembly

The preceding Step 2 material describes the frozen schema and constructor contract. Step 3 adds `recursive_integrity_toolkit.reports.assembly` while retaining report schema version `1.0`, the twelve sections, their order and their registered field ownership. The correction of `weighted_source_type_masses` to `category_mass_map` above describes its existing category-to-mass object; it changes no schema or mathematical result.

### Public Python interface

```python
def assemble_report(
    bundle: BundleValidationResult,
    *,
    run: dict,
    distributions: tuple[StateDistributionResult | DistributionMetrics, ...] = (),
    provenance: ProvenanceCompositionResult | None = None,
    duplicates: ExactDuplicateResult | None = None,
    tail: TailSelectionResult | None = None,
    comparison: SupportComparison | None = None,
    closure: DirectClosureExposureBounds | None = None,
    expected_diversity: ExpectedDiversityResult | None = None,
    resampling: ResamplingSimulation | None = None,
    extinction: tuple[ExtinctionProbabilityResult, ...] = (),
    family_errors: tuple[FamilyFailure, ...] = (),
) -> CanonicalReport:
    ...

@dataclass(frozen=True, slots=True)
class FamilyFailure:
    capability: CapabilityKey
    messages: tuple[ValidationMessage, ...]

class ReportAssemblyError(ReportValidationError):
    ...
```

Both `bundle` and `run` are required. `bundle` is the existing typed `BundleValidationResult` handoff, including its inventory, selected provenance join, chronology, observability assessment and diagnostics. `run` supplies every required run field and exact null reasons documented above. Assembly requires `privacy_mode: standard` and `redacted_mode: false`; it creates no identifiers, timestamps, environment readings, configuration hashes or random seeds. A valid empty typed bundle can retain an empty version list and zero record count without inventing a dataset version.

Callers first obtain results through the accepted validation and calculation APIs, then explicitly pass the results they want represented. Collection arguments are immutable tuples. The adapters require their exact supported result classes and retain the registered fields through explicit field selection. A returned `CanonicalReport` supplies the same immutable sections and detached `to_dict()` export described in Step 2. Unsupported types, duplicate public slots and inconsistent handoffs raise a validation error instead of silently dropping or overwriting evidence.

Assembly validates result types, finite values, metadata ownership, accepted method declarations, scope membership, coverage and denominator consistency. These checks do not authenticate the producer or establish the truth of supplied content, provenance, state meanings or calculations. A coherent supplied result remains a declaration-bound handoff. Assembly does not rerun its owner calculation as an independent numerical oracle.

### Accepted adapters and evidence placement

| Argument or retained input | Accepted type | Public evidence |
| --- | --- | --- |
| `bundle` | `BundleValidationResult` | Input inventory, hashes already supplied by validation, record counts, independent provenance coverage, original observability, diagnostics and bounded immediate-reference validation observations |
| `distributions` | `StateDistributionResult` | Unweighted observed state counts, derived support/diversity/frequency values and an explicitly supplied weighted companion |
| `distributions` | `DistributionMetrics` | A supplied count-backed or explicit-probability distribution, its support/diversity values and exact input basis |
| `provenance` | `ProvenanceCompositionResult` | Declared source/confidence counts, independent coverage, missing-row counts/shares, direct grounding classes and optional weighted source companions |
| `duplicates` | `ExactDuplicateResult` | Exact duplicate counts and groups under the supplied normalization and scope |
| `tail` | `TailSelectionResult` | The declared rule, its parameters, supplied membership, support/share and rarity ranking |
| `comparison` | `SupportComparison` | Supplied pair support delta, retention, loss/added counts, original support differences and diversity delta with explicit comparison basis |
| `closure` | `DirectClosureExposureBounds` | Supplied lower bound, upper bound and interval width, with operationalization, coverage and separate confidence disclosure |
| `expected_diversity` | `ExpectedDiversityResult` | Experimental analytic closed-resampling expectation and supplied scenario metadata |
| `resampling` | `ResamplingSimulation` | Experimental sampled paths, support trajectories, extinction events and supplied scenario metadata |
| `extinction` | Tuple of `ExtinctionProbabilityResult` | Explicitly supplied selected-state one-step extinction marginals under one shared scenario basis |
| `family_errors` | Tuple of `FamilyFailure` | Explicit capability-bound error/fatal diagnostics alongside independently useful evidence |

Empirical frequencies remain derived metrics. Explicit supplied probabilities are observed declarations under `observed_facts.supplied_state_probabilities.by_version`, with an explicit probability basis and no invented record-count denominator. Scenario probabilities remain simulations. Product metadata, capability decisions, warnings, errors and recommendations retain their product ownership without an additional scientific evidence class.

### Scope, coverage and representation

Empirical result scopes must use identities and versions retained in the validated bundle. Included and excluded identities, scope identifiers, denominator meanings and representation descriptors remain attached to their fields. Representation exclusions do not shrink input inventory, provenance denominators or unrelated result families. A missing representation permits input/provenance reporting and an explicit metadata recommendation; assembly does not select a topic field, hash representation or missing-state sentinel.

An explicit-probability distribution, a pair of explicit-probability distributions and a supplied simulation may retain a separate mathematical scope and representation. Their declarations do not raise the bundle's input observability or establish empirical record evidence. A shared top-level representation summary is populated only when supplied empirical result descriptors agree. Multiple descriptors remain visible in their individual envelopes with an input limitation explaining the missing single summary.

The existing classifier's coverage-detail names have the following explicit public mapping. Its underlying numerators, denominators, denominator names and ratios remain unchanged.

| Existing classifier detail | Report `coverage_details` field |
| --- | --- |
| `content` | `record_coverage` |
| `representation` | `representation_coverage` |
| `row` | `provenance_row_coverage` |
| `required_fields` | `provenance_required_field_coverage` |
| `grounding` | `grounding_field_coverage` |
| Existing lineage capability coverage | `resolved_parent_edge_coverage` |

The provenance capability additionally retains all three independent join coverages. Row presence, required-field validity and known grounding are separate observations. Missing rows remain distinct from an explicit `unknown` category. A zero coverage denominator produces `ratio: null` with an empty-scope reason; corresponding scalar coverage fields are unavailable with `value: null`. A measured zero remains numeric zero. Confidence categories are retained as categories and counts, without conversion into trust probabilities or discounts on grounding.

Weighted results keep their explicit weighting mode, `weight` field, record-weight denominator and `user_declared_weight_mass` units. Weighted state masses and source masses remain derived quantities. They accompany unweighted record counts and never replace them. A weighted distribution companion must share the unweighted scope and representation; unsupported standalone or conflicting weighting declarations are rejected.

### Explicit pair and public-slot rules

`comparison` represents one supplied accepted pair. It preserves distinct earlier/later selected versions, explicit order and order source, original and harmonized representations, literal state-meaning declarations, original positive-support differences, harmonized metric basis and mapping effects. Assembly checks this retained context without inferring chronology from version names, argument order or a cached capability flag.

The existing Python calculation API supports both explicit mapping directions, `earlier_to_later` and `later_to_earlier`. A supplied result retains its direction, source/target representations, state meanings, mapping table and collision groups. Assembly exports those accepted declarations; it does not apply a new map or recompute harmonized distributions. This Python handoff does not expand the narrower future CLI comparison contract in P4-D03.

A probability-pair-only handoff preserves `input_basis: explicit_probability_vector`, pair scopes, comparison declarations, supplied deltas and support sets. It does not automatically export complete original probability tables. To include those independent tables, also pass the original `DistributionMetrics` through `distributions`; their own declared version slots must remain unambiguous. Retaining pair basis therefore does not claim that every original distribution has been serialized.

The schema has one scalar/table slot per version and weighting mode, plus singleton slots for provenance composition, duplicate summary, tail selection, direct bounds and one pair comparison. Duplicate version/weighting results are rejected. Callers must choose one explicit compatible scope for each singleton family or construct separate reports; assembly never pools versions, merges unrelated scopes or silently overwrites one result with another.

### Supplied simulations

`expected_diversity` and `resampling` are mutually exclusive because both occupy `simulations.closed_resampling`. Supplying both fails explicitly. A nonempty `extinction` tuple occupies the separate `simulations.tail_extinction` slot. Its state identities must be unique, and all entries must share scope, representation, sample size and numerical policy. Their selected-state marginals do not assert a complete empirical distribution.

Scenario model/version, assumptions, supplied/effective distributions, normalization disclosure, numerical policy, horizon, sample size, seed, RNG identity, replicate schedule, paths and underflow disclosures remain attached to the applicable result. Analytic expectations, sampled paths and analytic one-step probabilities retain their distinct method labels. Mathematical scopes may differ from the bundle's empirical scope without upgrading its observability assessment.

No scenario runs during assembly. Omitted scenario arguments leave `simulations` empty. A supplied extinction marginal alone does not select a tail or create a tail-fragility signal. External reopening remains rejected by the Phase 4 schema, and external-reference loss remains unregistered. Supplied scenarios cannot establish an empirical intervention effect or a calibrated production-failure forecast.

### Input eligibility, execution and failures

The seven capability input statuses, original reason codes, requirements and input coverage retain the existing classifier assessment. Assembly adds independent execution fields and copies the same matrix into `observability.capabilities`. The canonical constructor retains one immutable shared capability object.

| Capability | Step 3 execution interpretation |
| --- | --- |
| `ingestion` | The retained bundle-validation operation is identified explicitly; retained ingestion errors produce partial/failed execution according to surviving input evidence. |
| `content_diagnostics` | Names supplied distribution, duplicate and tail operations. With no supplied result or family error it is `not_requested`; supplied operations are `completed` unless retained family errors make execution `partial`. An error with no supplied operation is `failed`. |
| `provenance` | Names supplied provenance-composition/direct-bound operations under the same completed/partial/failed rules. Independent validation coverage remains available even when no calculation is requested. |
| `lineage` | Always `deferred` in Phase 4, including Level 4 input eligibility. Retained immediate-parent validation errors remain errors without asserting graph execution. |
| `dataset_longitudinal` | A supplied pair records its limited support/diversity operation with `partial` execution and an explicit deferred-change-families reason. Without a supplied pair it is `not_requested`, or `failed` when an explicitly bound failure exists. |
| `model_longitudinal` | `deferred`, with the missing implementation/evidence boundary retained. |
| `intervention_simulation` | Names supplied analytic expectation, sampled path or extinction-marginal operations; no supplied scenario means `not_requested`. Explicitly bound failures remain failed/partial execution. |

Every noncompleted execution status has reasons. Completed/partial execution has a nonempty operation scope. A capability marked partial because other future change families are deferred does not itself make the run partial. Deferred and unrequested work alone does not create a run error.

`FamilyFailure` requires an exact `CapabilityKey` and a nonempty tuple of existing `ValidationMessage` objects whose severity is `error` or `fatal`. A warning-only collection is rejected. This explicit binding resolves errors such as `E_SCHEMA_TYPE` that can occur in several families. Existing bundle/calculation diagnostics use their structured source, field, file role and fixed code mappings; assembly never guesses a family from message wording. Severity, code, safe message and allowed location fields remain visible.

When errors survive, a fatal diagnostic sets `run_status: failed`. Other errors yield `partial` when useful supplied evidence survives and `failed` when no usable evidence remains. Errors carry the same effective run status. Original provenance or parent errors are preserved alongside independent content results. Warnings alone do not change successful run status; upstream strict-mode promotions retain their supplied error severity. Assembly does not calculate CLI exit codes.

Input eligibility and execution can legitimately differ. Completely absent usable provenance leaves input status unavailable, yet assembly can complete an explicitly supplied composition or direct-bounds handoff. The accepted dataset-facing `direct_closure_exposure` returns null bounds when no usable required-provenance row exists. Valid explicit unknown grounding can support a numeric `[0, 1]` interval. The separate explicit count-envelope API can also supply `[0, 1]` without certifying usable dataset provenance. Assembly preserves each result and its reasons; it does not replace unavailable bounds with an interval or promote the input classifier.

### Proxies, unavailable conclusions and next metadata

The current deterministic signals are restricted to these existing bases. Comparisons to zero and complete coverage identify a documented presence condition; they do not add empirical severity thresholds.

| Signal | Rule and basis | Required interpretation |
| --- | --- | --- |
| `support_contraction` | A usable supplied explicit-pair support delta is negative. Basis fields cite the delta and supplied support differences/comparison details. | Restricted to the pair's selected scope, representation and declared common state meaning; no production failure or model-performance claim. |
| `tail_fragility` | A usable supplied tail-support count is positive under the supplied explicit tail-selection rule. | Declared tail membership, with no hidden threshold, importance claim or calibrated production forecast. |
| `provenance_uncertainty` | A supplied usable direct interval width is positive, or a cited usable row/required-field/grounding coverage is below one. | Cites actual fields with matching scopes and preserves their distinct denominator meanings; completeness does not establish truth or source independence. |

Zero/positive support delta and an empty selected tail can produce `not_present` under their own usable basis. Missing, unavailable or zero-denominator evidence is not converted into zero or a negative finding. When a signal has no usable basis it is omitted. Each emitted proxy retains basis paths, deterministic trigger text, scope, representation where applicable, coverage and limitations. No `shared_ancestry_dependence` proxy is generated in this phase.

The required unavailable-conclusion safeguards include model-performance decline, causal ancestor effect, universal integrity and universal collapse prediction. Applicable additional entries explain production failure, complete-pipeline closure, deferred lineage analysis/closure/external ancestry and empirical intervention effects. Each uses its registered owner and method, unavailable evidence class/status, specific reasons, blocking evidence, required next metadata, related capability and theory/product limit. Missing input, invalid evidence, incompatible declarations, deferred implementation and conclusions outside product scope remain distinguishable. Unavailable does not establish that a conclusion is false.

Lineage validation observations remain bounded by their source method. Retained reference-entry counts preserve the classifier's multiplicity and denominator. The earlier-version ordering certificate is described as its sufficient declared-order certificate; it is not reported as general graph-cycle traversal. Root counts, HHI, effective roots, lineage depth, graph traversal, lineage closure and ancestry proxies remain deferred with explicit disclosures.

Recommendations are deterministic requests for evidence: missing matching provenance rows, usable required fields, unresolved external grounding, an explicitly missing representation, missing chronology, unresolved composite parent references and versioned model outcomes. Their priorities follow uncertainty reduction, the next available evidence requirement, error resolution and optional enrichment. Recommendations refer to the missing fields or retained classifier reasons; the absence of a single top-level representation summary alone does not assert that representation was never declared.

Recommendations do not enforce policy, repair records or promise that metadata alone unlocks deferred implementations or universal claims. Source category, human review, confidence and external grounding remain independent declarations. A narrower direct interval does not certify complete pipeline closure, factual truth or an independent source.

### Step 3 boundaries

This interface performs in-memory assembly and validation of supplied evidence. It does not ingest files, resolve content references, assign states, classify new inputs, calculate a metric, traverse a graph, run a simulation, redact identities, render JSON/Markdown/HTML, invoke a CLI analysis, perform network calls or publish artifacts. Privacy transformation, rendering and CLI orchestration belong to later approved steps. The historical Step 2 model/schema and the existing mathematical owners remain unchanged.

## Phase 4 Step 4: privacy and execution metadata APIs

Step 4 preserves all twelve section keys, the ninety-entry field registry and the
local report schema bytes. It adds `result.SafeReportView` and an explicit
`reports.assembly.privacy_view(report, mode=..., record_id_mode=..., protection=...)`
transition after the existing canonical assembly. `SafeReportView.to_dict()`
returns detached data in the same canonical shape. Its nested sections are
immutable, and the capability compatibility mirror remains equal to the canonical
capability matrix. Canonical structure alone does not establish privacy.

`standard` retains declared structural labels and approved local inventory.
`redacted` pseudonymizes dataset, state and scope identities, including dynamic
map keys and nested comparison/simulation details. Both modes exclude arbitrary
caller narrative from diagnostics and safe metadata. Reported analytical values,
scope counts, denominators, evidence classes, availability, execution status and
error severity are preserved. Input-inventory and normalized configuration hashes
remain linkable reproducibility metadata; raw per-record content digests are
protected when they serve as state or group identities.

In redacted mode, record IDs default to `hash`; `preserve` affects only the
declared record-ID field, and `omit` removes identity-bearing lists. Duplicate
groups with omitted identities retain `record_count` and the frozen
`redaction.omitted_fields = ["record_keys"]` contract. Optional scope identity
arrays may be omitted while their counts remain. Distinct registered exclusion
reasons remain disclosed with their protected scope association under
`run.identifier_protection.limitations`. Per-record linkage is intentionally
omitted. Redaction does not introduce an unavailable analytical conclusion.

The existing optional `run.identifier_protection` object records
`HMAC-SHA-256`, `run` or `cross_run` stability, record-ID mode and limitations.
Fresh secrets separate runs; an explicitly supplied checked local secret file
permits cross-run stability. Neither secret bytes, secret paths nor a reverse
mapping is exported. Fixed injected secrets support reproducible tests.

`config.resolve_phase4_options` validates the Phase 4 declarations before use;
`phase4_config_summary` exposes a small allowlist and `phase4_config_hash` hashes
normalized declared meaning under the documented secret exclusions. Existing
Phase 2 configuration and validation entry points retain their prior behavior.
Unsupported activation and competing declarations remain explicit errors.

`reports.assembly.build_run_metadata` accepts explicit measurements and approved
operation names (`python_api`, `audit`, `validate`, `example`). It creates standard
internal metadata suitable for `assemble_report`; callers then select the final
privacy view. It reconstructs an approved command description without raw argv,
uses null reasons for unrecorded fields and describes network count scope as
`toolkit_managed_outbound_operations`. A Python API call does not claim a CLI
invocation. Output privacy is separate from determinism of supplied calculations.
When resolved options already declare privacy and record-ID modes, view selection
must match those declarations. A different view cannot silently rewrite the
configuration summary while retaining its original hash.

`utils.logging.safe_diagnostic`, `format_diagnostic` and `emit_diagnostic`
construct content-safe structured diagnostics. Registered codes use static
toolkit explanations; unrecognized labels receive protected identifiers without
being reclassified as another registered error. Severity, capability effects and
safe locations remain. An output stream must be supplied explicitly; import does
not configure a logger or emit a record. JSON-line diagnostics do not implement
the deferred JSON report renderer.

Step 4 does not render reports, publish output files, start CLI analysis, expand
the public metric set or change any mathematical owner. It provides identifier
and content protection, not statistical anonymity or authentication of evidence.
