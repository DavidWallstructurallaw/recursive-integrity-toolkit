# Recursive Integrity Audit Report

**Summary**

- Run ID: `"phase4-step9-golden"`.
- Maximum observability level: 4; `"longitudinal_dataset_observability"`.
- Capability statuses: Ingestion: `"available"` (execution `"completed"`); Content diagnostics: `"available"` (execution `"completed"`); Provenance: `"available"` (execution `"completed"`); Lineage: `"available"` (execution `"deferred"`); Dataset longitudinal: `"available"` (execution `"partial"`); Model longitudinal: `"unavailable"` (execution `"deferred"`); Intervention simulation: `"unavailable"` (execution `"not_requested"`).
- Record scope: `"validated_bundle"`; dataset versions `["v1", "v2"]`; records 16; excluded records 0.
- Representation: `"topic"`; source `"topic_field"`; version `"hero-topic-v1"`. Complete mapping metadata appears in Input inventory.
- Warning entries: 0; error entries: 0.

Display policy: numbers use shortest round-trip decimal notation without rounding; scientific notation retains tiny nonzero values. Ratios and probabilities remain unscaled. Units, denominators and interval endpoints are supplied evidence. JSON is the machine-readable authority.

Quoted code literals represent supplied data, including identifiers and labels. JSON escapes visibly preserve markup characters and invisible controls. Unavailable (null) carries its declared reason or an explicit field-level null explanation. Empty objects and lists are shown explicitly. Object keys are sorted; supplied list order is preserved.

## Run metadata

| Field | Value |
|---|---|
| `["command"]` | `"rit example"` |
| `["completed_at"]` | `"2000-01-01T00:00:00+00:00"` |
| `["config_hash"]` | `"66f46415c08afe350f2741dd72f77c0c48015e37b500938758b1d09d69e5abba"` |
| `["config_hash_exclusions"]` | `["id_salt_file", "identifier_secret_material"]` |
| `["deterministic"]` | true |
| `["duration_seconds"]` | 0.0 |
| `["hash_algorithm"]` | `"sha256"` |
| `["identifier_protection"]["algorithm"]` | `"HMAC-SHA-256"` |
| `["identifier_protection"]["record_id_mode"]` | `"preserve"` |
| `["identifier_protection"]["stability_scope"]` | `"run"` |
| `["network_call_count"]` | 0 |
| `["network_count_scope"]` | `"toolkit_managed_outbound_operations"` |
| `["null_reasons"]["platform"]` | `"private_or_nonstandard_metadata_omitted"` |
| `["null_reasons"]["python_version"]` | `"private_or_nonstandard_metadata_omitted"` |
| `["null_reasons"]["random_seed"]` | `"not_recorded"` |
| `["platform"]` | Unavailable (null): `"private_or_nonstandard_metadata_omitted"` |
| `["privacy_mode"]` | `"standard"` |
| `["python_version"]` | Unavailable (null): `"private_or_nonstandard_metadata_omitted"` |
| `["random_seed"]` | Unavailable (null): `"not_recorded"` |
| `["redacted_mode"]` | false |
| `["report_schema_version"]` | `"1.0"` |
| `["resolved_options"]["comparison_requested"]` | true |
| `["resolved_options"]["privacy_mode"]` | `"standard"` |
| `["resolved_options"]["record_id_mode"]` | `"preserve"` |
| `["resolved_options"]["scenario_requested"]` | false |
| `["resolved_options"]["strict_mode"]` | false |
| `["resolved_options"]["tail_selection"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["resolved_options"]["weighted"]` | false |
| `["run_id"]` | `"phase4-step9-golden"` |
| `["run_status"]` | `"complete"` |
| `["started_at"]` | `"2000-01-01T00:00:00+00:00"` |
| `["strict_mode"]` | false |
| `["toolkit_version"]` | `"0.1.0.dev2"` |

**`["identifier_protection"]["limitations"]`**

- `"Identifier/content protection does not provide statistical anonymity or small-cell suppression."`
- `"Aggregate analytical values, evidence classes, availability, scope counts and diagnostic severity are unchanged."`
- `"Only reviewed toolkit narrative is retained; caller-authored narrative is replaced by nonreversible aliases."`
- `"Fresh identifier secrets affect output identity, not determinism of supplied calculations."`
- `"Record identifiers are explicitly preserved; other redacted fields remain protected."`

## Input inventory

| Field | Value |
|---|---|
| `["artifacts"][0]["dataset_versions"]` | `[]` |
| `["artifacts"][0]["file_hash"]` | `"2e069eb9c0105bf05c145ca15eec47834eb66f4408e8cdde9ff4935f5b920241"` |
| `["artifacts"][0]["format"]` | `"json"` |
| `["artifacts"][0]["hash_algorithm"]` | `"sha256"` |
| `["artifacts"][0]["parse_status"]` | `"completed"` |
| `["artifacts"][0]["path"]` | `"\u003cTEST_ROOT\u003e/inputs/config.json"` |
| `["artifacts"][0]["path_redacted"]` | false |
| `["artifacts"][0]["reason_codes"]` | `[]` |
| `["artifacts"][0]["role"]` | `"config"` |
| `["artifacts"][0]["row_count"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["artifacts"][0]["schema_fields"]` | `[]` |
| `["artifacts"][0]["size_bytes"]` | 170 |
| `["artifacts"][0]["validation_status"]` | `"completed"` |
| `["artifacts"][1]["dataset_versions"]` | `["v1", "v2"]` |
| `["artifacts"][1]["file_hash"]` | `"fc4ed3921d087e37996228dd8a37c4c51a0a3c3c91ded3e62a21e1b10f407438"` |
| `["artifacts"][1]["format"]` | `"csv"` |
| `["artifacts"][1]["hash_algorithm"]` | `"sha256"` |
| `["artifacts"][1]["parse_status"]` | `"completed"` |
| `["artifacts"][1]["path"]` | `"\u003cTEST_ROOT\u003e/inputs/provenance.csv"` |
| `["artifacts"][1]["path_redacted"]` | false |
| `["artifacts"][1]["reason_codes"]` | `[]` |
| `["artifacts"][1]["role"]` | `"provenance_manifest"` |
| `["artifacts"][1]["row_count"]` | 16 |
| `["artifacts"][1]["schema_fields"]` | `["dataset_version", "record_id", "source_type", "provenance_confidence", "parent_ids", "generator_id", "generator_version", "transformation", "generation", "human_reviewed", "external_grounding"]` |
| `["artifacts"][1]["size_bytes"]` | 1294 |
| `["artifacts"][1]["validation_status"]` | `"completed"` |
| `["artifacts"][2]["dataset_versions"]` | `["v1"]` |
| `["artifacts"][2]["file_hash"]` | `"b62c9aee057c61f641009b949acb110e003acbea6a399cc607a78ee6e6f0543d"` |
| `["artifacts"][2]["format"]` | `"csv"` |
| `["artifacts"][2]["hash_algorithm"]` | `"sha256"` |
| `["artifacts"][2]["parse_status"]` | `"completed"` |
| `["artifacts"][2]["path"]` | `"\u003cTEST_ROOT\u003e/inputs/records_v1.csv"` |
| `["artifacts"][2]["path_redacted"]` | false |
| `["artifacts"][2]["reason_codes"]` | `[]` |
| `["artifacts"][2]["role"]` | `"records_compare"` |
| `["artifacts"][2]["row_count"]` | 8 |
| `["artifacts"][2]["schema_fields"]` | `["record_id", "dataset_version", "content", "topic"]` |
| `["artifacts"][2]["size_bytes"]` | 437 |
| `["artifacts"][2]["validation_status"]` | `"completed"` |
| `["artifacts"][3]["dataset_versions"]` | `["v2"]` |
| `["artifacts"][3]["file_hash"]` | `"d691605fd6bb37e785945ae34c8c18ea8409201f7d78449d39df08df7770599b"` |
| `["artifacts"][3]["format"]` | `"csv"` |
| `["artifacts"][3]["hash_algorithm"]` | `"sha256"` |
| `["artifacts"][3]["parse_status"]` | `"completed"` |
| `["artifacts"][3]["path"]` | `"\u003cTEST_ROOT\u003e/inputs/records_v2.csv"` |
| `["artifacts"][3]["path_redacted"]` | false |
| `["artifacts"][3]["reason_codes"]` | `[]` |
| `["artifacts"][3]["role"]` | `"records_primary"` |
| `["artifacts"][3]["row_count"]` | 8 |
| `["artifacts"][3]["schema_fields"]` | `["record_id", "dataset_version", "content", "topic"]` |
| `["artifacts"][3]["size_bytes"]` | 442 |
| `["artifacts"][3]["validation_status"]` | `"completed"` |
| `["artifacts"][4]["dataset_versions"]` | `[]` |
| `["artifacts"][4]["file_hash"]` | `"3e33ca8b2095f35f55d22265071bce00119c9282b72bb02cee3275c646898387"` |
| `["artifacts"][4]["format"]` | `"json"` |
| `["artifacts"][4]["hash_algorithm"]` | `"sha256"` |
| `["artifacts"][4]["parse_status"]` | `"completed"` |
| `["artifacts"][4]["path"]` | `"\u003cTEST_ROOT\u003e/inputs/version_order.json"` |
| `["artifacts"][4]["path_redacted"]` | false |
| `["artifacts"][4]["reason_codes"]` | `[]` |
| `["artifacts"][4]["role"]` | `"version_order"` |
| `["artifacts"][4]["row_count"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["artifacts"][4]["schema_fields"]` | `[]` |
| `["artifacts"][4]["size_bytes"]` | 36 |
| `["artifacts"][4]["validation_status"]` | `"completed"` |
| `["representation"]["binning_or_mapping_rule"]` | `"literal_field_value"` |
| `["representation"]["field_name"]` | `"topic"` |
| `["representation"]["missing_state_id"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["missing_value_policy"]` | `"error"` |
| `["representation"]["normalization_profile"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["representation_name"]` | `"topic"` |
| `["representation"]["representation_source"]` | `"topic_field"` |
| `["representation"]["representation_version"]` | `"hero-topic-v1"` |
| `["scope"]["dataset_versions"]` | `["v1", "v2"]` |
| `["scope"]["denominator_basis"]` | `"all_validated_bundle_records"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 16 |
| `["scope"]["scope_id"]` | `"validated_bundle"` |
| `["version_order"]` | `["v1", "v2"]` |
| `["version_order_source"]` | `"explicit_version_order"` |

**`["limitations"]`**

- `"Input hashes identify supplied bytes and do not certify authenticity."`
- `"Only allowlisted evidence fields are assembled; raw content, extras, notes and embeddings are not exported."`

**`["file_hashes"]`**

| `"algorithm"` | `"artifact_index"` | `"value"` |
|---|---|---|
| `"sha256"` | 0 | `"2e069eb9c0105bf05c145ca15eec47834eb66f4408e8cdde9ff4935f5b920241"` |
| `"sha256"` | 1 | `"fc4ed3921d087e37996228dd8a37c4c51a0a3c3c91ded3e62a21e1b10f407438"` |
| `"sha256"` | 2 | `"b62c9aee057c61f641009b949acb110e003acbea6a399cc607a78ee6e6f0543d"` |
| `"sha256"` | 3 | `"d691605fd6bb37e785945ae34c8c18ea8409201f7d78449d39df08df7770599b"` |
| `"sha256"` | 4 | `"3e33ca8b2095f35f55d22265071bce00119c9282b72bb02cee3275c646898387"` |

**`["scope"]["included_record_keys"]`**

| `"dataset_version"` | `"record_id"` |
|---|---|
| `"v1"` | `"v1_01"` |
| `"v1"` | `"v1_02"` |
| `"v1"` | `"v1_03"` |
| `"v1"` | `"v1_04"` |
| `"v1"` | `"v1_05"` |
| `"v1"` | `"v1_06"` |
| `"v1"` | `"v1_07"` |
| `"v1"` | `"v1_08"` |
| `"v2"` | `"v2_01"` |
| `"v2"` | `"v2_02"` |
| `"v2"` | `"v2_03"` |
| `"v2"` | `"v2_04"` |
| `"v2"` | `"v2_05"` |
| `"v2"` | `"v2_06"` |
| `"v2"` | `"v2_07"` |
| `"v2"` | `"v2_08"` |

## Observability summary

| Field | Value |
|---|---|
| `["basis"]` | `["validated_ingest_scope", "content_or_declared_representation", "valid_matching_provenance", "earlier_version_acyclicity_certificate", "ordered_compatible_dataset_versions"]` |
| `["level_label"]` | `"longitudinal_dataset_observability"` |
| `["maximum_level"]` | 4 |
| `["partial_evidence"]` | `["R_MODEL_EVIDENCE_MISSING", "R_SCENARIO_NOT_CONFIGURED"]` |

**`["limitations"]`**

- `"R_MODEL_EVIDENCE_MISSING"`
- `"R_SCENARIO_NOT_CONFIGURED"`
- `"Input eligibility is distinct from executed analysis; Phase 5 lineage remains deferred."`

The equal observability.capabilities compatibility mirror is represented once in the Capability matrix section.

## Capability matrix

| Capability | Status | Coverage (ratio) | Reason | Execution | Execution reason |
|---|---|---|---|---|---|
| Ingestion | `"available"` | 1.0 | `[]` | `"completed"` | `[]` |
| Content diagnostics | `"available"` | 1.0 | `[]` | `"completed"` | `[]` |
| Provenance | `"available"` | 1.0 | `[]` | `"completed"` | `[]` |
| Lineage | `"available"` | 1.0 | `[]` | `"deferred"` | `["R_LINEAGE_EXECUTION_DEFERRED"]` |
| Dataset longitudinal | `"available"` | 1.0 | `[]` | `"partial"` | `["R_LONGITUDINAL_FAMILIES_DEFERRED"]` |
| Model longitudinal | `"unavailable"` | Unavailable (null): `"coverage_not_supplied_or_empty_denominator"` | `["R_MODEL_EVIDENCE_MISSING"]` | `"deferred"` | `["R_MODEL_ANALYSIS_DEFERRED"]` |
| Intervention simulation | `"unavailable"` | Unavailable (null): `"coverage_not_supplied_or_empty_denominator"` | `["R_SCENARIO_NOT_CONFIGURED"]` | `"not_requested"` | `["R_ANALYSIS_NOT_REQUESTED"]` |

Coverage details and unresolved counts, when supplied, follow below. Related diagnostic entries appear in the Warnings and Errors sections.

**Ingestion details**

| Field | Value |
|---|---|
| `["coverage_details"]` | `{}` |
| `["coverage_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["execution_scope"]` | `["existing_bundle_validation"]` |
| `["notes"]` | `["Input eligibility only; downstream analytical implementations remain deferred."]` |
| `["requirements_met"]` | `["valid_record_scope"]` |
| `["requirements_missing"]` | `[]` |

**Content diagnostics details**

| Field | Value |
|---|---|
| `["coverage_details"]["record_coverage"]["denominator"]` | 16 |
| `["coverage_details"]["record_coverage"]["denominator_name"]` | `"valid_records_in_requested_scope"` |
| `["coverage_details"]["record_coverage"]["numerator"]` | 16 |
| `["coverage_details"]["record_coverage"]["ratio"]` | 1.0 |
| `["coverage_details"]["record_coverage"]["reason"]` | Unavailable (null): No null reason is required when the associated ratio is supplied. |
| `["coverage_details"]["representation_coverage"]["denominator"]` | 16 |
| `["coverage_details"]["representation_coverage"]["denominator_name"]` | `"valid_records_in_requested_scope"` |
| `["coverage_details"]["representation_coverage"]["numerator"]` | 16 |
| `["coverage_details"]["representation_coverage"]["ratio"]` | 1.0 |
| `["coverage_details"]["representation_coverage"]["reason"]` | Unavailable (null): No null reason is required when the associated ratio is supplied. |
| `["coverage_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["execution_scope"]` | `["supplied_distribution:audit-representation-earlier", "supplied_distribution:audit-representation"]` |
| `["notes"]` | `["Input eligibility only; downstream analytical implementations remain deferred.", "Raw content and exact record form do not certify semantic capability."]` |
| `["requirements_met"]` | `["content_or_declared_field_available"]` |
| `["requirements_missing"]` | `[]` |

**Provenance details**

| Field | Value |
|---|---|
| `["coverage_details"]["grounding_field_coverage"]["denominator"]` | 16 |
| `["coverage_details"]["grounding_field_coverage"]["denominator_name"]` | `"all_valid_records_in_selected_dataset_scope"` |
| `["coverage_details"]["grounding_field_coverage"]["numerator"]` | 16 |
| `["coverage_details"]["grounding_field_coverage"]["ratio"]` | 1.0 |
| `["coverage_details"]["grounding_field_coverage"]["reason"]` | Unavailable (null): No null reason is required when the associated ratio is supplied. |
| `["coverage_details"]["provenance_required_field_coverage"]["denominator"]` | 16 |
| `["coverage_details"]["provenance_required_field_coverage"]["denominator_name"]` | `"all_valid_records_in_selected_dataset_scope"` |
| `["coverage_details"]["provenance_required_field_coverage"]["numerator"]` | 16 |
| `["coverage_details"]["provenance_required_field_coverage"]["ratio"]` | 1.0 |
| `["coverage_details"]["provenance_required_field_coverage"]["reason"]` | Unavailable (null): No null reason is required when the associated ratio is supplied. |
| `["coverage_details"]["provenance_row_coverage"]["denominator"]` | 16 |
| `["coverage_details"]["provenance_row_coverage"]["denominator_name"]` | `"all_valid_records_in_selected_dataset_scope"` |
| `["coverage_details"]["provenance_row_coverage"]["numerator"]` | 16 |
| `["coverage_details"]["provenance_row_coverage"]["ratio"]` | 1.0 |
| `["coverage_details"]["provenance_row_coverage"]["reason"]` | Unavailable (null): No null reason is required when the associated ratio is supplied. |
| `["coverage_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["execution_scope"]` | `["supplied_provenance_composition:audit-provenance", "supplied_direct_closure_interval:audit-provenance"]` |
| `["notes"]` | `["Input eligibility only; downstream analytical implementations remain deferred."]` |
| `["requirements_met"]` | `["valid_matching_provenance"]` |
| `["requirements_missing"]` | `[]` |

**Lineage details**

| Field | Value |
|---|---|
| `["coverage_details"]["resolved_parent_edge_coverage"]["denominator"]` | 8 |
| `["coverage_details"]["resolved_parent_edge_coverage"]["denominator_name"]` | `"declared_parent_reference_entries"` |
| `["coverage_details"]["resolved_parent_edge_coverage"]["numerator"]` | 8 |
| `["coverage_details"]["resolved_parent_edge_coverage"]["ratio"]` | 1.0 |
| `["coverage_details"]["resolved_parent_edge_coverage"]["reason"]` | Unavailable (null): No null reason is required when the associated ratio is supplied. |
| `["coverage_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["execution_scope"]` | `[]` |
| `["notes"]` | `["Input eligibility only; downstream analytical implementations remain deferred.", "Reference-entry resolution coverage is not ancestry or external-root coverage.", "General graph validation is deferred; no roots or ancestors are traced."]` |
| `["requirements_met"]` | `["earlier_version_acyclicity_certificate"]` |
| `["requirements_missing"]` | `[]` |

**Dataset longitudinal details**

| Field | Value |
|---|---|
| `["coverage_details"]` | `{}` |
| `["coverage_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["execution_scope"]` | `["supplied_explicit_pair_support_and_diversity"]` |
| `["notes"]` | `["Input eligibility only; downstream analytical implementations remain deferred.", "No cross-version metric or state mapping executes here.", "Executed only the supplied explicit-pair support/diversity comparison; no adjacent-pair discovery, lineage/provenance trajectory or relative-change calculation."]` |
| `["requirements_met"]` | `["explicit_order_and_compatible_representation"]` |
| `["requirements_missing"]` | `[]` |

**Model longitudinal details**

| Field | Value |
|---|---|
| `["coverage_details"]` | `{}` |
| `["coverage_reason"]` | `"coverage_not_supplied_or_empty_denominator"` |
| `["execution_scope"]` | `[]` |
| `["notes"]` | `["Input eligibility only; downstream analytical implementations remain deferred.", "Dataset versions do not establish model-performance change."]` |
| `["requirements_met"]` | `[]` |
| `["requirements_missing"]` | `["approved_model_performance_evidence"]` |

**Intervention simulation details**

| Field | Value |
|---|---|
| `["coverage_details"]` | `{}` |
| `["coverage_reason"]` | `"coverage_not_supplied_or_empty_denominator"` |
| `["execution_scope"]` | `[]` |
| `["notes"]` | `["Input eligibility only; downstream analytical implementations remain deferred."]` |
| `["requirements_met"]` | `[]` |
| `["requirements_missing"]` | `["explicit_scenario_activation"]` |

## Observed facts

### Analytical result

`["observed_facts"]["lineage"]["cycle_status"]`

Status: `"unavailable"`; evidence class: `"observed_fact"`; unit: `"status"`; method: `"T6.graph_cycle_check"`.

Value: Unavailable (null): reason codes `["R_GRAPH_EXECUTION_DEFERRED"]`.

Denominator: Unavailable (null): `"denominator_not_applicable_or_unavailable"`; coverage (ratio): Unavailable (null): `"coverage_not_supplied_for_this_result"`.

| Field | Value |
|---|---|
| `["assumptions"]` | `[]` |
| `["coverage"]` | Unavailable (null): `"coverage_not_supplied_for_this_result"` |
| `["coverage_reason"]` | `"coverage_not_supplied_for_this_result"` |
| `["denominator"]` | Unavailable (null): `"denominator_not_applicable_or_unavailable"` |
| `["denominator_reason"]` | `"denominator_not_applicable_or_unavailable"` |
| `["evidence_class"]` | `"observed_fact"` |
| `["method_id"]` | `"T6.graph_cycle_check"` |
| `["owner_ids"]` | `["T6"]` |
| `["reason_codes"]` | `["R_GRAPH_EXECUTION_DEFERRED"]` |
| `["representation"]` | Unavailable (null): No applicable representation supplied; consult status and required evidence. |
| `["required_evidence"]` | `["Phase_5_graph_analysis"]` |
| `["scope"]["dataset_versions"]` | `["v1", "v2"]` |
| `["scope"]["denominator_basis"]` | `"all_validated_bundle_records"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 16 |
| `["scope"]["scope_id"]` | `"validated_bundle"` |
| `["status"]` | `"unavailable"` |
| `["theory_map_ids"]` | `[]` |
| `["trace_ids"]` | `["T6"]` |
| `["unit"]` | `"status"` |
| `["value"]` | Unavailable (null): reason codes `["R_GRAPH_EXECUTION_DEFERRED"]` |

**`["limitations"]`**

- `"No general graph-cycle traversal executes in Phase 4."`

**`["scope"]["included_record_keys"]`**

| `"dataset_version"` | `"record_id"` |
|---|---|
| `"v1"` | `"v1_01"` |
| `"v1"` | `"v1_02"` |
| `"v1"` | `"v1_03"` |
| `"v1"` | `"v1_04"` |
| `"v1"` | `"v1_05"` |
| `"v1"` | `"v1_06"` |
| `"v1"` | `"v1_07"` |
| `"v1"` | `"v1_08"` |
| `"v2"` | `"v2_01"` |
| `"v2"` | `"v2_02"` |
| `"v2"` | `"v2_03"` |
| `"v2"` | `"v2_04"` |
| `"v2"` | `"v2_05"` |
| `"v2"` | `"v2_06"` |
| `"v2"` | `"v2_07"` |
| `"v2"` | `"v2_08"` |

### Analytical result

`["observed_facts"]["lineage"]["declared_parent_edge_count"]`

Status: `"available"`; evidence class: `"observed_fact"`; unit: `"edges"`; method: `"PR-008.declared_parent_edge_count"`.

Value: 8.

Denominator: 8; coverage (ratio): 1.0.

| Field | Value |
|---|---|
| `["assumptions"]` | `[]` |
| `["coverage"]` | 1.0 |
| `["coverage_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["denominator"]` | 8 |
| `["denominator_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["evidence_class"]` | `"observed_fact"` |
| `["method_id"]` | `"PR-008.declared_parent_edge_count"` |
| `["owner_ids"]` | `["PR-008"]` |
| `["reason_codes"]` | `[]` |
| `["representation"]` | Unavailable (null): No applicable representation supplied; consult status and required evidence. |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["v1", "v2"]` |
| `["scope"]["denominator_basis"]` | `"all_validated_bundle_records"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 16 |
| `["scope"]["scope_id"]` | `"validated_bundle"` |
| `["status"]` | `"available"` |
| `["theory_map_ids"]` | `[]` |
| `["trace_ids"]` | `[]` |
| `["unit"]` | `"edges"` |
| `["value"]` | 8 |

**`["limitations"]`**

- `"Counts preserve validation reference-entry multiplicity; they do not describe an ancestry graph."`

**`["scope"]["included_record_keys"]`**

| `"dataset_version"` | `"record_id"` |
|---|---|
| `"v1"` | `"v1_01"` |
| `"v1"` | `"v1_02"` |
| `"v1"` | `"v1_03"` |
| `"v1"` | `"v1_04"` |
| `"v1"` | `"v1_05"` |
| `"v1"` | `"v1_06"` |
| `"v1"` | `"v1_07"` |
| `"v1"` | `"v1_08"` |
| `"v2"` | `"v2_01"` |
| `"v2"` | `"v2_02"` |
| `"v2"` | `"v2_03"` |
| `"v2"` | `"v2_04"` |
| `"v2"` | `"v2_05"` |
| `"v2"` | `"v2_06"` |
| `"v2"` | `"v2_07"` |
| `"v2"` | `"v2_08"` |

### Analytical result

`["observed_facts"]["lineage"]["ordering_certificate"]`

Status: `"available"`; evidence class: `"observed_fact"`; unit: `"certificate"`; method: `"PR-008.earlier_version_certificate"`.

Denominator: Unavailable (null): `"denominator_not_applicable_or_unavailable"`; coverage (ratio): Unavailable (null): `"coverage_not_supplied_for_this_result"`.

| Field | Value |
|---|---|
| `["assumptions"]` | `[]` |
| `["coverage"]` | Unavailable (null): `"coverage_not_supplied_for_this_result"` |
| `["coverage_reason"]` | `"coverage_not_supplied_for_this_result"` |
| `["denominator"]` | Unavailable (null): `"denominator_not_applicable_or_unavailable"` |
| `["denominator_reason"]` | `"denominator_not_applicable_or_unavailable"` |
| `["evidence_class"]` | `"observed_fact"` |
| `["method_id"]` | `"PR-008.earlier_version_certificate"` |
| `["owner_ids"]` | `["PR-008"]` |
| `["reason_codes"]` | `[]` |
| `["representation"]` | Unavailable (null): No applicable representation supplied; consult status and required evidence. |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["v1", "v2"]` |
| `["scope"]["denominator_basis"]` | `"all_validated_bundle_records"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 16 |
| `["scope"]["scope_id"]` | `"validated_bundle"` |
| `["status"]` | `"available"` |
| `["theory_map_ids"]` | `[]` |
| `["trace_ids"]` | `[]` |
| `["unit"]` | `"certificate"` |
| `["value"]["all_resolved_edges_follow_order"]` | true |
| `["value"]["method"]` | `"declared_earlier_version_order"` |
| `["value"]["version_order"]` | `["v1", "v2"]` |

**`["limitations"]`**

- `"This retained earlier-version ordering certificate is not general graph-cycle traversal."`

**`["scope"]["included_record_keys"]`**

| `"dataset_version"` | `"record_id"` |
|---|---|
| `"v1"` | `"v1_01"` |
| `"v1"` | `"v1_02"` |
| `"v1"` | `"v1_03"` |
| `"v1"` | `"v1_04"` |
| `"v1"` | `"v1_05"` |
| `"v1"` | `"v1_06"` |
| `"v1"` | `"v1_07"` |
| `"v1"` | `"v1_08"` |
| `"v2"` | `"v2_01"` |
| `"v2"` | `"v2_02"` |
| `"v2"` | `"v2_03"` |
| `"v2"` | `"v2_04"` |
| `"v2"` | `"v2_05"` |
| `"v2"` | `"v2_06"` |
| `"v2"` | `"v2_07"` |
| `"v2"` | `"v2_08"` |

### Analytical result

`["observed_facts"]["lineage"]["resolved_parent_edge_count"]`

Status: `"available"`; evidence class: `"observed_fact"`; unit: `"edges"`; method: `"PR-008.resolved_parent_edge_count"`.

Value: 8.

Denominator: 8; coverage (ratio): 1.0.

| Field | Value |
|---|---|
| `["assumptions"]` | `[]` |
| `["coverage"]` | 1.0 |
| `["coverage_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["denominator"]` | 8 |
| `["denominator_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["evidence_class"]` | `"observed_fact"` |
| `["method_id"]` | `"PR-008.resolved_parent_edge_count"` |
| `["owner_ids"]` | `["PR-008"]` |
| `["reason_codes"]` | `[]` |
| `["representation"]` | Unavailable (null): No applicable representation supplied; consult status and required evidence. |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["v1", "v2"]` |
| `["scope"]["denominator_basis"]` | `"all_validated_bundle_records"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 16 |
| `["scope"]["scope_id"]` | `"validated_bundle"` |
| `["status"]` | `"available"` |
| `["theory_map_ids"]` | `[]` |
| `["trace_ids"]` | `[]` |
| `["unit"]` | `"edges"` |
| `["value"]` | 8 |

**`["limitations"]`**

- `"Counts preserve validation reference-entry multiplicity; they do not describe an ancestry graph."`

**`["scope"]["included_record_keys"]`**

| `"dataset_version"` | `"record_id"` |
|---|---|
| `"v1"` | `"v1_01"` |
| `"v1"` | `"v1_02"` |
| `"v1"` | `"v1_03"` |
| `"v1"` | `"v1_04"` |
| `"v1"` | `"v1_05"` |
| `"v1"` | `"v1_06"` |
| `"v1"` | `"v1_07"` |
| `"v1"` | `"v1_08"` |
| `"v2"` | `"v2_01"` |
| `"v2"` | `"v2_02"` |
| `"v2"` | `"v2_03"` |
| `"v2"` | `"v2_04"` |
| `"v2"` | `"v2_05"` |
| `"v2"` | `"v2_06"` |
| `"v2"` | `"v2_07"` |
| `"v2"` | `"v2_08"` |

### Analytical result

`["observed_facts"]["lineage"]["unresolved_parent_edge_count"]`

Status: `"available"`; evidence class: `"observed_fact"`; unit: `"edges"`; method: `"PR-008.unresolved_parent_edge_count"`.

Value: 0.

Denominator: 8; coverage (ratio): 1.0.

| Field | Value |
|---|---|
| `["assumptions"]` | `[]` |
| `["coverage"]` | 1.0 |
| `["coverage_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["denominator"]` | 8 |
| `["denominator_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["evidence_class"]` | `"observed_fact"` |
| `["method_id"]` | `"PR-008.unresolved_parent_edge_count"` |
| `["owner_ids"]` | `["PR-008"]` |
| `["reason_codes"]` | `[]` |
| `["representation"]` | Unavailable (null): No applicable representation supplied; consult status and required evidence. |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["v1", "v2"]` |
| `["scope"]["denominator_basis"]` | `"all_validated_bundle_records"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 16 |
| `["scope"]["scope_id"]` | `"validated_bundle"` |
| `["status"]` | `"available"` |
| `["theory_map_ids"]` | `[]` |
| `["trace_ids"]` | `[]` |
| `["unit"]` | `"edges"` |
| `["value"]` | 0 |

**`["limitations"]`**

- `"Counts preserve validation reference-entry multiplicity; they do not describe an ancestry graph."`

**`["scope"]["included_record_keys"]`**

| `"dataset_version"` | `"record_id"` |
|---|---|
| `"v1"` | `"v1_01"` |
| `"v1"` | `"v1_02"` |
| `"v1"` | `"v1_03"` |
| `"v1"` | `"v1_04"` |
| `"v1"` | `"v1_05"` |
| `"v1"` | `"v1_06"` |
| `"v1"` | `"v1_07"` |
| `"v1"` | `"v1_08"` |
| `"v2"` | `"v2_01"` |
| `"v2"` | `"v2_02"` |
| `"v2"` | `"v2_03"` |
| `"v2"` | `"v2_04"` |
| `"v2"` | `"v2_05"` |
| `"v2"` | `"v2_06"` |
| `"v2"` | `"v2_07"` |
| `"v2"` | `"v2_08"` |

### Analytical result

`["observed_facts"]["provenance"]["analyzed_record_count"]`

Status: `"available"`; evidence class: `"observed_fact"`; unit: `"records"`; method: `"PR-004.analyzed_record_count"`.

Value: 8.

Denominator: 8; coverage (ratio): Unavailable (null): `"coverage_not_supplied_for_this_result"`.

| Field | Value |
|---|---|
| `["coverage"]` | Unavailable (null): `"coverage_not_supplied_for_this_result"` |
| `["coverage_reason"]` | `"coverage_not_supplied_for_this_result"` |
| `["denominator"]` | 8 |
| `["denominator_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["evidence_class"]` | `"observed_fact"` |
| `["method"]` | `"All selected valid records"` |
| `["method_id"]` | `"PR-004.analyzed_record_count"` |
| `["owner_ids"]` | `["PR-004"]` |
| `["reason_codes"]` | `[]` |
| `["representation"]` | Unavailable (null): No applicable representation supplied; consult status and required evidence. |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["v2"]` |
| `["scope"]["denominator_basis"]` | `"all_valid_records_in_selected_dataset_scope"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"audit-provenance"` |
| `["status"]` | `"available"` |
| `["theory_map_ids"]` | `[]` |
| `["trace_ids"]` | `[]` |
| `["unit"]` | `"records"` |
| `["value"]` | 8 |
| `["weighting"]["weight_field"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["weighting"]["weighting_mode"]` | `"unweighted"` |

**`["assumptions"]`**

- `"Exact explicit single-version Phase 2 join scope; no representation exclusions."`

**`["limitations"]`**

- `"Supplied declarations only; no truth or source-independence certification."`
- `"Declared composition does not certify input validity or increase observability."`
- `"Source, confidence, human review and grounding are independent declarations."`
- `"Representation exclusions cannot reduce the provenance denominator."`

**`["scope"]["included_record_keys"]`**

| `"dataset_version"` | `"record_id"` |
|---|---|
| `"v2"` | `"v2_01"` |
| `"v2"` | `"v2_02"` |
| `"v2"` | `"v2_03"` |
| `"v2"` | `"v2_04"` |
| `"v2"` | `"v2_05"` |
| `"v2"` | `"v2_06"` |
| `"v2"` | `"v2_07"` |
| `"v2"` | `"v2_08"` |

### Analytical result

`["observed_facts"]["provenance"]["grounding_field_coverage"]`

Status: `"available"`; evidence class: `"observed_fact"`; unit: `"ratio"`; method: `"PR-004.grounding_field_coverage"`.

Value: 1.0.

Denominator: 8; coverage (ratio): 1.0.

| Field | Value |
|---|---|
| `["coverage"]` | 1.0 |
| `["coverage_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["denominator"]` | 8 |
| `["denominator_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["evidence_class"]` | `"observed_fact"` |
| `["method"]` | `"Reuse Phase 2 coverage; Definitions 3.10-3.12"` |
| `["method_id"]` | `"PR-004.grounding_field_coverage"` |
| `["owner_ids"]` | `["PR-004"]` |
| `["reason_codes"]` | `[]` |
| `["representation"]` | Unavailable (null): No applicable representation supplied; consult status and required evidence. |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["v2"]` |
| `["scope"]["denominator_basis"]` | `"all_valid_records_in_selected_dataset_scope"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"audit-provenance"` |
| `["status"]` | `"available"` |
| `["theory_map_ids"]` | `[]` |
| `["trace_ids"]` | `[]` |
| `["unit"]` | `"ratio"` |
| `["value"]` | 1.0 |
| `["weighting"]["weight_field"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["weighting"]["weighting_mode"]` | `"unweighted"` |

**`["assumptions"]`**

- `"Exact explicit single-version Phase 2 join scope; no representation exclusions."`

**`["limitations"]`**

- `"Supplied declarations only; no truth or source-independence certification."`

**`["scope"]["included_record_keys"]`**

| `"dataset_version"` | `"record_id"` |
|---|---|
| `"v2"` | `"v2_01"` |
| `"v2"` | `"v2_02"` |
| `"v2"` | `"v2_03"` |
| `"v2"` | `"v2_04"` |
| `"v2"` | `"v2_05"` |
| `"v2"` | `"v2_06"` |
| `"v2"` | `"v2_07"` |
| `"v2"` | `"v2_08"` |

### Analytical result

`["observed_facts"]["provenance"]["known_closed_count"]`

Status: `"available"`; evidence class: `"observed_fact"`; unit: `"records"`; method: `"T3.direct_grounding_classification"`.

Value: 4.

Denominator: 8; coverage (ratio): 1.0.

| Field | Value |
|---|---|
| `["coverage"]` | 1.0 |
| `["coverage_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["denominator"]` | 8 |
| `["denominator_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["evidence_class"]` | `"observed_fact"` |
| `["method"]` | `"toolkit_operationalization; Definitions 3.7-3.9; P3-D08"` |
| `["method_id"]` | `"T3.direct_grounding_classification"` |
| `["owner_ids"]` | `["T3"]` |
| `["reason_codes"]` | `[]` |
| `["representation"]` | Unavailable (null): No applicable representation supplied; consult status and required evidence. |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["v2"]` |
| `["scope"]["denominator_basis"]` | `"all_valid_records_in_selected_dataset_scope"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"audit-provenance"` |
| `["status"]` | `"available"` |
| `["theory_map_ids"]` | `[]` |
| `["trace_ids"]` | `["T3"]` |
| `["unit"]` | `"records"` |
| `["value"]` | 4 |
| `["weighting"]["weight_field"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["weighting"]["weighting_mode"]` | `"unweighted"` |

**`["assumptions"]`**

- `"Exact explicit single-version Phase 2 join scope; no representation exclusions."`

**`["limitations"]`**

- `"Supplied declarations only; no truth or source-independence certification."`
- `"Direct classes are relative to supplied grounding about the audited loop."`
- `"No independent truth, source independence, ancestry or complete closure is certified."`
- `"Incomplete required provenance remains unresolved with original errors retained."`

**`["scope"]["included_record_keys"]`**

| `"dataset_version"` | `"record_id"` |
|---|---|
| `"v2"` | `"v2_01"` |
| `"v2"` | `"v2_02"` |
| `"v2"` | `"v2_03"` |
| `"v2"` | `"v2_04"` |
| `"v2"` | `"v2_05"` |
| `"v2"` | `"v2_06"` |
| `"v2"` | `"v2_07"` |
| `"v2"` | `"v2_08"` |

### Analytical result

`["observed_facts"]["provenance"]["known_open_count"]`

Status: `"available"`; evidence class: `"observed_fact"`; unit: `"records"`; method: `"T3.direct_grounding_classification"`.

Value: 4.

Denominator: 8; coverage (ratio): 1.0.

| Field | Value |
|---|---|
| `["coverage"]` | 1.0 |
| `["coverage_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["denominator"]` | 8 |
| `["denominator_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["evidence_class"]` | `"observed_fact"` |
| `["method"]` | `"toolkit_operationalization; Definitions 3.7-3.9; P3-D08"` |
| `["method_id"]` | `"T3.direct_grounding_classification"` |
| `["owner_ids"]` | `["T3"]` |
| `["reason_codes"]` | `[]` |
| `["representation"]` | Unavailable (null): No applicable representation supplied; consult status and required evidence. |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["v2"]` |
| `["scope"]["denominator_basis"]` | `"all_valid_records_in_selected_dataset_scope"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"audit-provenance"` |
| `["status"]` | `"available"` |
| `["theory_map_ids"]` | `[]` |
| `["trace_ids"]` | `["T3"]` |
| `["unit"]` | `"records"` |
| `["value"]` | 4 |
| `["weighting"]["weight_field"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["weighting"]["weighting_mode"]` | `"unweighted"` |

**`["assumptions"]`**

- `"Exact explicit single-version Phase 2 join scope; no representation exclusions."`

**`["limitations"]`**

- `"Supplied declarations only; no truth or source-independence certification."`
- `"Direct classes are relative to supplied grounding about the audited loop."`
- `"No independent truth, source independence, ancestry or complete closure is certified."`
- `"Incomplete required provenance remains unresolved with original errors retained."`

**`["scope"]["included_record_keys"]`**

| `"dataset_version"` | `"record_id"` |
|---|---|
| `"v2"` | `"v2_01"` |
| `"v2"` | `"v2_02"` |
| `"v2"` | `"v2_03"` |
| `"v2"` | `"v2_04"` |
| `"v2"` | `"v2_05"` |
| `"v2"` | `"v2_06"` |
| `"v2"` | `"v2_07"` |
| `"v2"` | `"v2_08"` |

### Analytical result

`["observed_facts"]["provenance"]["missing_provenance_count"]`

Status: `"available"`; evidence class: `"observed_fact"`; unit: `"records"`; method: `"PR-004.missing_provenance_count"`.

Value: 0.

Denominator: 8; coverage (ratio): Unavailable (null): `"coverage_not_supplied_for_this_result"`.

| Field | Value |
|---|---|
| `["coverage"]` | Unavailable (null): `"coverage_not_supplied_for_this_result"` |
| `["coverage_reason"]` | `"coverage_not_supplied_for_this_result"` |
| `["denominator"]` | 8 |
| `["denominator_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["evidence_class"]` | `"observed_fact"` |
| `["method"]` | `"Phase 2 missing-row inventory"` |
| `["method_id"]` | `"PR-004.missing_provenance_count"` |
| `["owner_ids"]` | `["PR-004"]` |
| `["reason_codes"]` | `[]` |
| `["representation"]` | Unavailable (null): No applicable representation supplied; consult status and required evidence. |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["v2"]` |
| `["scope"]["denominator_basis"]` | `"all_valid_records_in_selected_dataset_scope"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"audit-provenance"` |
| `["status"]` | `"available"` |
| `["theory_map_ids"]` | `[]` |
| `["trace_ids"]` | `[]` |
| `["unit"]` | `"records"` |
| `["value"]` | 0 |
| `["weighting"]["weight_field"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["weighting"]["weighting_mode"]` | `"unweighted"` |

**`["assumptions"]`**

- `"Exact explicit single-version Phase 2 join scope; no representation exclusions."`

**`["limitations"]`**

- `"Supplied declarations only; no truth or source-independence certification."`
- `"Declared composition does not certify input validity or increase observability."`
- `"Source, confidence, human review and grounding are independent declarations."`
- `"Representation exclusions cannot reduce the provenance denominator."`

**`["scope"]["included_record_keys"]`**

| `"dataset_version"` | `"record_id"` |
|---|---|
| `"v2"` | `"v2_01"` |
| `"v2"` | `"v2_02"` |
| `"v2"` | `"v2_03"` |
| `"v2"` | `"v2_04"` |
| `"v2"` | `"v2_05"` |
| `"v2"` | `"v2_06"` |
| `"v2"` | `"v2_07"` |
| `"v2"` | `"v2_08"` |

### Analytical result

`["observed_facts"]["provenance"]["provenance_confidence_counts"]`

Status: `"available"`; evidence class: `"observed_fact"`; unit: `"records"`; method: `"PR-004.provenance_confidence_counts"`.

Denominator: 8; coverage (ratio): 1.0.

| Field | Value |
|---|---|
| `["coverage"]` | 1.0 |
| `["coverage_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["denominator"]` | 8 |
| `["denominator_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["evidence_class"]` | `"observed_fact"` |
| `["method"]` | `"Definitions 3.3/11.1; count declared canonical categories"` |
| `["method_id"]` | `"PR-004.provenance_confidence_counts"` |
| `["owner_ids"]` | `["PR-004"]` |
| `["reason_codes"]` | `[]` |
| `["representation"]` | Unavailable (null): No applicable representation supplied; consult status and required evidence. |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["v2"]` |
| `["scope"]["denominator_basis"]` | `"all_valid_records_in_selected_dataset_scope"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"audit-provenance"` |
| `["status"]` | `"available"` |
| `["theory_map_ids"]` | `[]` |
| `["trace_ids"]` | `[]` |
| `["unit"]` | `"records"` |
| `["value"]["confirmed"]` | 8 |
| `["value"]["estimated"]` | 0 |
| `["value"]["log_derived"]` | 0 |
| `["value"]["unknown"]` | 0 |
| `["weighting"]["weight_field"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["weighting"]["weighting_mode"]` | `"unweighted"` |

**`["assumptions"]`**

- `"Exact explicit single-version Phase 2 join scope; no representation exclusions."`

**`["limitations"]`**

- `"Supplied declarations only; no truth or source-independence certification."`
- `"Declared composition does not certify input validity or increase observability."`
- `"Source, confidence, human review and grounding are independent declarations."`
- `"Representation exclusions cannot reduce the provenance denominator."`

**`["scope"]["included_record_keys"]`**

| `"dataset_version"` | `"record_id"` |
|---|---|
| `"v2"` | `"v2_01"` |
| `"v2"` | `"v2_02"` |
| `"v2"` | `"v2_03"` |
| `"v2"` | `"v2_04"` |
| `"v2"` | `"v2_05"` |
| `"v2"` | `"v2_06"` |
| `"v2"` | `"v2_07"` |
| `"v2"` | `"v2_08"` |

### Analytical result

`["observed_facts"]["provenance"]["provenance_confidence_field_coverage"]`

Status: `"available"`; evidence class: `"observed_fact"`; unit: `"ratio"`; method: `"PR-004.provenance_confidence_field_coverage"`.

Value: 1.0.

Denominator: 8; coverage (ratio): 1.0.

| Field | Value |
|---|---|
| `["coverage"]` | 1.0 |
| `["coverage_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["denominator"]` | 8 |
| `["denominator_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["evidence_class"]` | `"observed_fact"` |
| `["method"]` | `"Definitions 3.13; nonmissing valid field / all selected valid records"` |
| `["method_id"]` | `"PR-004.provenance_confidence_field_coverage"` |
| `["owner_ids"]` | `["PR-004"]` |
| `["reason_codes"]` | `[]` |
| `["representation"]` | Unavailable (null): No applicable representation supplied; consult status and required evidence. |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["v2"]` |
| `["scope"]["denominator_basis"]` | `"all_valid_records_in_selected_dataset_scope"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"audit-provenance"` |
| `["status"]` | `"available"` |
| `["theory_map_ids"]` | `[]` |
| `["trace_ids"]` | `[]` |
| `["unit"]` | `"ratio"` |
| `["value"]` | 1.0 |
| `["weighting"]["weight_field"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["weighting"]["weighting_mode"]` | `"unweighted"` |

**`["assumptions"]`**

- `"Exact explicit single-version Phase 2 join scope; no representation exclusions."`

**`["limitations"]`**

- `"Supplied declarations only; no truth or source-independence certification."`

**`["scope"]["included_record_keys"]`**

| `"dataset_version"` | `"record_id"` |
|---|---|
| `"v2"` | `"v2_01"` |
| `"v2"` | `"v2_02"` |
| `"v2"` | `"v2_03"` |
| `"v2"` | `"v2_04"` |
| `"v2"` | `"v2_05"` |
| `"v2"` | `"v2_06"` |
| `"v2"` | `"v2_07"` |
| `"v2"` | `"v2_08"` |

### Analytical result

`["observed_facts"]["provenance"]["provenance_required_field_coverage"]`

Status: `"available"`; evidence class: `"observed_fact"`; unit: `"ratio"`; method: `"PR-004.provenance_required_field_coverage"`.

Value: 1.0.

Denominator: 8; coverage (ratio): 1.0.

| Field | Value |
|---|---|
| `["coverage"]` | 1.0 |
| `["coverage_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["denominator"]` | 8 |
| `["denominator_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["evidence_class"]` | `"observed_fact"` |
| `["method"]` | `"Reuse Phase 2 coverage; Definitions 3.10-3.12"` |
| `["method_id"]` | `"PR-004.provenance_required_field_coverage"` |
| `["owner_ids"]` | `["PR-004"]` |
| `["reason_codes"]` | `[]` |
| `["representation"]` | Unavailable (null): No applicable representation supplied; consult status and required evidence. |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["v2"]` |
| `["scope"]["denominator_basis"]` | `"all_valid_records_in_selected_dataset_scope"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"audit-provenance"` |
| `["status"]` | `"available"` |
| `["theory_map_ids"]` | `[]` |
| `["trace_ids"]` | `[]` |
| `["unit"]` | `"ratio"` |
| `["value"]` | 1.0 |
| `["weighting"]["weight_field"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["weighting"]["weighting_mode"]` | `"unweighted"` |

**`["assumptions"]`**

- `"Exact explicit single-version Phase 2 join scope; no representation exclusions."`

**`["limitations"]`**

- `"Supplied declarations only; no truth or source-independence certification."`

**`["scope"]["included_record_keys"]`**

| `"dataset_version"` | `"record_id"` |
|---|---|
| `"v2"` | `"v2_01"` |
| `"v2"` | `"v2_02"` |
| `"v2"` | `"v2_03"` |
| `"v2"` | `"v2_04"` |
| `"v2"` | `"v2_05"` |
| `"v2"` | `"v2_06"` |
| `"v2"` | `"v2_07"` |
| `"v2"` | `"v2_08"` |

### Analytical result

`["observed_facts"]["provenance"]["provenance_row_coverage"]`

Status: `"available"`; evidence class: `"observed_fact"`; unit: `"ratio"`; method: `"F-008"`.

Value: 1.0.

Denominator: 8; coverage (ratio): 1.0.

| Field | Value |
|---|---|
| `["coverage"]` | 1.0 |
| `["coverage_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["denominator"]` | 8 |
| `["denominator_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["evidence_class"]` | `"observed_fact"` |
| `["method"]` | `"Reuse Phase 2 coverage; Definitions 3.10-3.12"` |
| `["method_id"]` | `"F-008"` |
| `["owner_ids"]` | `["PR-004"]` |
| `["reason_codes"]` | `[]` |
| `["representation"]` | Unavailable (null): No applicable representation supplied; consult status and required evidence. |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["v2"]` |
| `["scope"]["denominator_basis"]` | `"all_valid_records_in_selected_dataset_scope"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"audit-provenance"` |
| `["status"]` | `"available"` |
| `["theory_map_ids"]` | `[]` |
| `["trace_ids"]` | `[]` |
| `["unit"]` | `"ratio"` |
| `["value"]` | 1.0 |
| `["weighting"]["weight_field"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["weighting"]["weighting_mode"]` | `"unweighted"` |

**`["assumptions"]`**

- `"Exact explicit single-version Phase 2 join scope; no representation exclusions."`

**`["limitations"]`**

- `"Supplied declarations only; no truth or source-independence certification."`

**`["scope"]["included_record_keys"]`**

| `"dataset_version"` | `"record_id"` |
|---|---|
| `"v2"` | `"v2_01"` |
| `"v2"` | `"v2_02"` |
| `"v2"` | `"v2_03"` |
| `"v2"` | `"v2_04"` |
| `"v2"` | `"v2_05"` |
| `"v2"` | `"v2_06"` |
| `"v2"` | `"v2_07"` |
| `"v2"` | `"v2_08"` |

### Analytical result

`["observed_facts"]["provenance"]["records_with_matching_rows"]`

Status: `"available"`; evidence class: `"observed_fact"`; unit: `"records"`; method: `"PR-004.records_with_matching_rows"`.

Value: 8.

Denominator: 8; coverage (ratio): Unavailable (null): `"coverage_not_supplied_for_this_result"`.

| Field | Value |
|---|---|
| `["coverage"]` | Unavailable (null): `"coverage_not_supplied_for_this_result"` |
| `["coverage_reason"]` | `"coverage_not_supplied_for_this_result"` |
| `["denominator"]` | 8 |
| `["denominator_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["evidence_class"]` | `"observed_fact"` |
| `["method"]` | `"Phase 2 matched-row inventory"` |
| `["method_id"]` | `"PR-004.records_with_matching_rows"` |
| `["owner_ids"]` | `["PR-004"]` |
| `["reason_codes"]` | `[]` |
| `["representation"]` | Unavailable (null): No applicable representation supplied; consult status and required evidence. |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["v2"]` |
| `["scope"]["denominator_basis"]` | `"all_valid_records_in_selected_dataset_scope"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"audit-provenance"` |
| `["status"]` | `"available"` |
| `["theory_map_ids"]` | `[]` |
| `["trace_ids"]` | `[]` |
| `["unit"]` | `"records"` |
| `["value"]` | 8 |
| `["weighting"]["weight_field"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["weighting"]["weighting_mode"]` | `"unweighted"` |

**`["assumptions"]`**

- `"Exact explicit single-version Phase 2 join scope; no representation exclusions."`

**`["limitations"]`**

- `"Supplied declarations only; no truth or source-independence certification."`
- `"Declared composition does not certify input validity or increase observability."`
- `"Source, confidence, human review and grounding are independent declarations."`
- `"Representation exclusions cannot reduce the provenance denominator."`

**`["scope"]["included_record_keys"]`**

| `"dataset_version"` | `"record_id"` |
|---|---|
| `"v2"` | `"v2_01"` |
| `"v2"` | `"v2_02"` |
| `"v2"` | `"v2_03"` |
| `"v2"` | `"v2_04"` |
| `"v2"` | `"v2_05"` |
| `"v2"` | `"v2_06"` |
| `"v2"` | `"v2_07"` |
| `"v2"` | `"v2_08"` |

### Analytical result

`["observed_facts"]["provenance"]["source_type_counts"]`

Status: `"available"`; evidence class: `"observed_fact"`; unit: `"records"`; method: `"PR-005.source_type_counts"`.

Denominator: 8; coverage (ratio): 1.0.

| Field | Value |
|---|---|
| `["coverage"]` | 1.0 |
| `["coverage_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["denominator"]` | 8 |
| `["denominator_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["evidence_class"]` | `"observed_fact"` |
| `["method"]` | `"Definitions 3.3/11.1; count declared canonical categories"` |
| `["method_id"]` | `"PR-005.source_type_counts"` |
| `["owner_ids"]` | `["PR-005"]` |
| `["reason_codes"]` | `[]` |
| `["representation"]` | Unavailable (null): No applicable representation supplied; consult status and required evidence. |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["v2"]` |
| `["scope"]["denominator_basis"]` | `"all_valid_records_in_selected_dataset_scope"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"audit-provenance"` |
| `["status"]` | `"available"` |
| `["theory_map_ids"]` | `[]` |
| `["trace_ids"]` | `[]` |
| `["unit"]` | `"records"` |
| `["value"]["human"]` | 4 |
| `["value"]["mixed"]` | 0 |
| `["value"]["sensor"]` | 0 |
| `["value"]["synthetic"]` | 4 |
| `["value"]["unknown"]` | 0 |
| `["weighting"]["weight_field"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["weighting"]["weighting_mode"]` | `"unweighted"` |

**`["assumptions"]`**

- `"Exact explicit single-version Phase 2 join scope; no representation exclusions."`

**`["limitations"]`**

- `"Supplied declarations only; no truth or source-independence certification."`
- `"Declared composition does not certify input validity or increase observability."`
- `"Source, confidence, human review and grounding are independent declarations."`
- `"Representation exclusions cannot reduce the provenance denominator."`

**`["scope"]["included_record_keys"]`**

| `"dataset_version"` | `"record_id"` |
|---|---|
| `"v2"` | `"v2_01"` |
| `"v2"` | `"v2_02"` |
| `"v2"` | `"v2_03"` |
| `"v2"` | `"v2_04"` |
| `"v2"` | `"v2_05"` |
| `"v2"` | `"v2_06"` |
| `"v2"` | `"v2_07"` |
| `"v2"` | `"v2_08"` |

### Analytical result

`["observed_facts"]["provenance"]["source_type_field_coverage"]`

Status: `"available"`; evidence class: `"observed_fact"`; unit: `"ratio"`; method: `"PR-004.source_type_field_coverage"`.

Value: 1.0.

Denominator: 8; coverage (ratio): 1.0.

| Field | Value |
|---|---|
| `["coverage"]` | 1.0 |
| `["coverage_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["denominator"]` | 8 |
| `["denominator_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["evidence_class"]` | `"observed_fact"` |
| `["method"]` | `"Definitions 3.13; nonmissing valid field / all selected valid records"` |
| `["method_id"]` | `"PR-004.source_type_field_coverage"` |
| `["owner_ids"]` | `["PR-004"]` |
| `["reason_codes"]` | `[]` |
| `["representation"]` | Unavailable (null): No applicable representation supplied; consult status and required evidence. |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["v2"]` |
| `["scope"]["denominator_basis"]` | `"all_valid_records_in_selected_dataset_scope"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"audit-provenance"` |
| `["status"]` | `"available"` |
| `["theory_map_ids"]` | `[]` |
| `["trace_ids"]` | `[]` |
| `["unit"]` | `"ratio"` |
| `["value"]` | 1.0 |
| `["weighting"]["weight_field"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["weighting"]["weighting_mode"]` | `"unweighted"` |

**`["assumptions"]`**

- `"Exact explicit single-version Phase 2 join scope; no representation exclusions."`

**`["limitations"]`**

- `"Supplied declarations only; no truth or source-independence certification."`

**`["scope"]["included_record_keys"]`**

| `"dataset_version"` | `"record_id"` |
|---|---|
| `"v2"` | `"v2_01"` |
| `"v2"` | `"v2_02"` |
| `"v2"` | `"v2_03"` |
| `"v2"` | `"v2_04"` |
| `"v2"` | `"v2_05"` |
| `"v2"` | `"v2_06"` |
| `"v2"` | `"v2_07"` |
| `"v2"` | `"v2_08"` |

### Analytical result

`["observed_facts"]["provenance"]["unresolved_grounding_count"]`

Status: `"available"`; evidence class: `"observed_fact"`; unit: `"records"`; method: `"T3.direct_grounding_classification"`.

Value: 0.

Denominator: 8; coverage (ratio): 1.0.

| Field | Value |
|---|---|
| `["coverage"]` | 1.0 |
| `["coverage_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["denominator"]` | 8 |
| `["denominator_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["evidence_class"]` | `"observed_fact"` |
| `["method"]` | `"toolkit_operationalization; Definitions 3.7-3.9; P3-D08"` |
| `["method_id"]` | `"T3.direct_grounding_classification"` |
| `["owner_ids"]` | `["T3"]` |
| `["reason_codes"]` | `[]` |
| `["representation"]` | Unavailable (null): No applicable representation supplied; consult status and required evidence. |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["v2"]` |
| `["scope"]["denominator_basis"]` | `"all_valid_records_in_selected_dataset_scope"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"audit-provenance"` |
| `["status"]` | `"available"` |
| `["theory_map_ids"]` | `[]` |
| `["trace_ids"]` | `["T3"]` |
| `["unit"]` | `"records"` |
| `["value"]` | 0 |
| `["weighting"]["weight_field"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["weighting"]["weighting_mode"]` | `"unweighted"` |

**`["assumptions"]`**

- `"Exact explicit single-version Phase 2 join scope; no representation exclusions."`

**`["limitations"]`**

- `"Supplied declarations only; no truth or source-independence certification."`
- `"Direct classes are relative to supplied grounding about the audited loop."`
- `"No independent truth, source independence, ancestry or complete closure is certified."`
- `"Incomplete required provenance remains unresolved with original errors retained."`

**`["scope"]["included_record_keys"]`**

| `"dataset_version"` | `"record_id"` |
|---|---|
| `"v2"` | `"v2_01"` |
| `"v2"` | `"v2_02"` |
| `"v2"` | `"v2_03"` |
| `"v2"` | `"v2_04"` |
| `"v2"` | `"v2_05"` |
| `"v2"` | `"v2_06"` |
| `"v2"` | `"v2_07"` |
| `"v2"` | `"v2_08"` |

### Analytical result

`["observed_facts"]["record_counts"]["v1"]`

Status: `"available"`; evidence class: `"observed_fact"`; unit: `"records"`; method: `"PR-002.record_count"`.

Value: 8.

Denominator: 8; coverage (ratio): Unavailable (null): `"coverage_not_supplied_for_this_result"`.

| Field | Value |
|---|---|
| `["assumptions"]` | `[]` |
| `["coverage"]` | Unavailable (null): `"coverage_not_supplied_for_this_result"` |
| `["coverage_reason"]` | `"coverage_not_supplied_for_this_result"` |
| `["denominator"]` | 8 |
| `["denominator_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["evidence_class"]` | `"observed_fact"` |
| `["limitations"]` | `[]` |
| `["method_id"]` | `"PR-002.record_count"` |
| `["owner_ids"]` | `["PR-002"]` |
| `["reason_codes"]` | `[]` |
| `["representation"]` | Unavailable (null): No applicable representation supplied; consult status and required evidence. |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["v1"]` |
| `["scope"]["denominator_basis"]` | `"validated_records_in_version"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"validated_version:v1"` |
| `["status"]` | `"available"` |
| `["theory_map_ids"]` | `[]` |
| `["trace_ids"]` | `[]` |
| `["unit"]` | `"records"` |
| `["value"]` | 8 |

**`["scope"]["included_record_keys"]`**

| `"dataset_version"` | `"record_id"` |
|---|---|
| `"v1"` | `"v1_01"` |
| `"v1"` | `"v1_02"` |
| `"v1"` | `"v1_03"` |
| `"v1"` | `"v1_04"` |
| `"v1"` | `"v1_05"` |
| `"v1"` | `"v1_06"` |
| `"v1"` | `"v1_07"` |
| `"v1"` | `"v1_08"` |

### Analytical result

`["observed_facts"]["record_counts"]["v2"]`

Status: `"available"`; evidence class: `"observed_fact"`; unit: `"records"`; method: `"PR-002.record_count"`.

Value: 8.

Denominator: 8; coverage (ratio): Unavailable (null): `"coverage_not_supplied_for_this_result"`.

| Field | Value |
|---|---|
| `["assumptions"]` | `[]` |
| `["coverage"]` | Unavailable (null): `"coverage_not_supplied_for_this_result"` |
| `["coverage_reason"]` | `"coverage_not_supplied_for_this_result"` |
| `["denominator"]` | 8 |
| `["denominator_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["evidence_class"]` | `"observed_fact"` |
| `["limitations"]` | `[]` |
| `["method_id"]` | `"PR-002.record_count"` |
| `["owner_ids"]` | `["PR-002"]` |
| `["reason_codes"]` | `[]` |
| `["representation"]` | Unavailable (null): No applicable representation supplied; consult status and required evidence. |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["v2"]` |
| `["scope"]["denominator_basis"]` | `"validated_records_in_version"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"validated_version:v2"` |
| `["status"]` | `"available"` |
| `["theory_map_ids"]` | `[]` |
| `["trace_ids"]` | `[]` |
| `["unit"]` | `"records"` |
| `["value"]` | 8 |

**`["scope"]["included_record_keys"]`**

| `"dataset_version"` | `"record_id"` |
|---|---|
| `"v2"` | `"v2_01"` |
| `"v2"` | `"v2_02"` |
| `"v2"` | `"v2_03"` |
| `"v2"` | `"v2_04"` |
| `"v2"` | `"v2_05"` |
| `"v2"` | `"v2_06"` |
| `"v2"` | `"v2_07"` |
| `"v2"` | `"v2_08"` |

### Analytical result

`["observed_facts"]["state_counts"]["by_version"]["v1"]`

Status: `"available"`; evidence class: `"observed_fact"`; unit: `"records"`; method: `"T1.state_counts"`.

Denominator: 8; coverage (ratio): 1.0.

| Field | Value |
|---|---|
| `["coverage"]` | 1.0 |
| `["coverage_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["denominator"]` | 8 |
| `["denominator_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["evidence_class"]` | `"observed_fact"` |
| `["method"]` | `"count included record-state assignments"` |
| `["method_id"]` | `"T1.state_counts"` |
| `["owner_ids"]` | `["T1"]` |
| `["reason_codes"]` | `[]` |
| `["representation"]["binning_or_mapping_rule"]` | `"literal_field_value"` |
| `["representation"]["field_name"]` | `"topic"` |
| `["representation"]["missing_state_id"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["missing_value_policy"]` | `"error"` |
| `["representation"]["normalization_profile"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["representation_name"]` | `"topic"` |
| `["representation"]["representation_source"]` | `"topic_field"` |
| `["representation"]["representation_version"]` | `"hero-topic-v1"` |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["v1"]` |
| `["scope"]["denominator_basis"]` | `"included_representation_records"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["exclusions"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"audit-representation-earlier"` |
| `["status"]` | `"available"` |
| `["theory_map_ids"]` | `[]` |
| `["trace_ids"]` | `["T1"]` |
| `["unit"]` | `"records"` |
| `["weighting"]["weight_field"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["weighting"]["weighting_mode"]` | `"unweighted"` |

**`["assumptions"]`**

- `"One explicitly selected version and declared representation."`
- `"No implicit pooling, probability repair, confidence weighting or sampling."`

**`["limitations"]`**

- `"Representation-bound; does not establish functional failure or semantic completeness."`

**`["scope"]["included_record_keys"]`**

| `"dataset_version"` | `"record_id"` |
|---|---|
| `"v1"` | `"v1_01"` |
| `"v1"` | `"v1_02"` |
| `"v1"` | `"v1_03"` |
| `"v1"` | `"v1_04"` |
| `"v1"` | `"v1_05"` |
| `"v1"` | `"v1_06"` |
| `"v1"` | `"v1_07"` |
| `"v1"` | `"v1_08"` |

**`["value"]`**

| `"state_count"` | `"state_id"` |
|---|---|
| 1 | `"battery"` |
| 1 | `"bird"` |
| 1 | `"cat"` |
| 1 | `"dog"` |
| 1 | `"fish"` |
| 1 | `"lizard"` |
| 1 | `"refund"` |
| 1 | `"turtle"` |

### Analytical result

`["observed_facts"]["state_counts"]["by_version"]["v2"]`

Status: `"available"`; evidence class: `"observed_fact"`; unit: `"records"`; method: `"T1.state_counts"`.

Denominator: 8; coverage (ratio): 1.0.

| Field | Value |
|---|---|
| `["coverage"]` | 1.0 |
| `["coverage_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["denominator"]` | 8 |
| `["denominator_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["evidence_class"]` | `"observed_fact"` |
| `["method"]` | `"count included record-state assignments"` |
| `["method_id"]` | `"T1.state_counts"` |
| `["owner_ids"]` | `["T1"]` |
| `["reason_codes"]` | `[]` |
| `["representation"]["binning_or_mapping_rule"]` | `"literal_field_value"` |
| `["representation"]["field_name"]` | `"topic"` |
| `["representation"]["missing_state_id"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["missing_value_policy"]` | `"error"` |
| `["representation"]["normalization_profile"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["representation_name"]` | `"topic"` |
| `["representation"]["representation_source"]` | `"topic_field"` |
| `["representation"]["representation_version"]` | `"hero-topic-v1"` |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["v2"]` |
| `["scope"]["denominator_basis"]` | `"included_representation_records"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["exclusions"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"audit-representation"` |
| `["status"]` | `"available"` |
| `["theory_map_ids"]` | `[]` |
| `["trace_ids"]` | `["T1"]` |
| `["unit"]` | `"records"` |
| `["weighting"]["weight_field"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["weighting"]["weighting_mode"]` | `"unweighted"` |

**`["assumptions"]`**

- `"One explicitly selected version and declared representation."`
- `"No implicit pooling, probability repair, confidence weighting or sampling."`

**`["limitations"]`**

- `"Representation-bound; does not establish functional failure or semantic completeness."`

**`["scope"]["included_record_keys"]`**

| `"dataset_version"` | `"record_id"` |
|---|---|
| `"v2"` | `"v2_01"` |
| `"v2"` | `"v2_02"` |
| `"v2"` | `"v2_03"` |
| `"v2"` | `"v2_04"` |
| `"v2"` | `"v2_05"` |
| `"v2"` | `"v2_06"` |
| `"v2"` | `"v2_07"` |
| `"v2"` | `"v2_08"` |

**`["value"]`**

| `"state_count"` | `"state_id"` |
|---|---|
| 1 | `"bird"` |
| 3 | `"cat"` |
| 2 | `"dog"` |
| 1 | `"fish"` |
| 1 | `"refund"` |

## Derived metrics

### Closure exposure intervals

- `"direct"` (ratio): 0.5 to 0.5; interval width: 0.0.

`["derived_metrics"]["closure_exposure"]["direct"]["classification_basis"]`

| Field | Value |
|---|---|
| Value | `"toolkit_operationalization"` |

`["derived_metrics"]["closure_exposure"]["direct"]["confidence_disclosure"]`

| Field | Value |
|---|---|
| Value | `"provenance_confidence_is_separate_and_does_not_discount_grounding"` |

### Analytical result

`["derived_metrics"]["closure_exposure"]["direct"]["interval_width"]`

Status: `"available"`; evidence class: `"derived_metric"`; unit: `"ratio"`; method: `"T3.upper_minus_lower"`.

Value: 0.0.

Denominator: 8; coverage (ratio): 1.0.

| Field | Value |
|---|---|
| `["coverage"]` | 1.0 |
| `["coverage_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["denominator"]` | 8 |
| `["denominator_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["evidence_class"]` | `"derived_metric"` |
| `["method"]` | `"upper_bound - lower_bound = unresolved_grounding_count / total_record_count"` |
| `["method_id"]` | `"T3.upper_minus_lower"` |
| `["owner_ids"]` | `["T3"]` |
| `["reason_codes"]` | `[]` |
| `["representation"]` | Unavailable (null): No applicable representation supplied; consult status and required evidence. |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["v2"]` |
| `["scope"]["denominator_basis"]` | `"all_valid_records_in_selected_dataset_scope"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"audit-provenance"` |
| `["status"]` | `"available"` |
| `["theory_map_ids"]` | `[]` |
| `["trace_ids"]` | `["T3"]` |
| `["unit"]` | `"ratio"` |
| `["value"]` | 0.0 |
| `["weighting"]["weight_field"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["weighting"]["weighting_mode"]` | `"unweighted"` |

**`["assumptions"]`**

- `"Approved direct grounding partition; uncertainty remains unresolved."`

**`["limitations"]`**

- `"Toolkit operationalization relative to supplied metadata, without lineage or truth certification."`
- `"Direct exposure is relative to the audited loop and supplied metadata."`
- `"Toolkit operationalization; metadata can be incorrect and hidden dependencies unobserved."`
- `"Confidence remains separate; no lineage, midpoint, threshold or causal claim."`

**`["scope"]["included_record_keys"]`**

| `"dataset_version"` | `"record_id"` |
|---|---|
| `"v2"` | `"v2_01"` |
| `"v2"` | `"v2_02"` |
| `"v2"` | `"v2_03"` |
| `"v2"` | `"v2_04"` |
| `"v2"` | `"v2_05"` |
| `"v2"` | `"v2_06"` |
| `"v2"` | `"v2_07"` |
| `"v2"` | `"v2_08"` |

### Analytical result

`["derived_metrics"]["closure_exposure"]["direct"]["lower_bound"]`

Status: `"available"`; evidence class: `"derived_metric"`; unit: `"ratio"`; method: `"F-009"`.

Value: 0.5.

Denominator: 8; coverage (ratio): 1.0.

| Field | Value |
|---|---|
| `["coverage"]` | 1.0 |
| `["coverage_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["denominator"]` | 8 |
| `["denominator_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["evidence_class"]` | `"derived_metric"` |
| `["method"]` | `"known_closed_count / total_record_count"` |
| `["method_id"]` | `"F-009"` |
| `["owner_ids"]` | `["T3"]` |
| `["reason_codes"]` | `[]` |
| `["representation"]` | Unavailable (null): No applicable representation supplied; consult status and required evidence. |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["v2"]` |
| `["scope"]["denominator_basis"]` | `"all_valid_records_in_selected_dataset_scope"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"audit-provenance"` |
| `["status"]` | `"available"` |
| `["theory_map_ids"]` | `[]` |
| `["trace_ids"]` | `["T3"]` |
| `["unit"]` | `"ratio"` |
| `["value"]` | 0.5 |
| `["weighting"]["weight_field"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["weighting"]["weighting_mode"]` | `"unweighted"` |

**`["assumptions"]`**

- `"Approved direct grounding partition; uncertainty remains unresolved."`

**`["limitations"]`**

- `"Toolkit operationalization relative to supplied metadata, without lineage or truth certification."`
- `"Direct exposure is relative to the audited loop and supplied metadata."`
- `"Toolkit operationalization; metadata can be incorrect and hidden dependencies unobserved."`
- `"Confidence remains separate; no lineage, midpoint, threshold or causal claim."`

**`["scope"]["included_record_keys"]`**

| `"dataset_version"` | `"record_id"` |
|---|---|
| `"v2"` | `"v2_01"` |
| `"v2"` | `"v2_02"` |
| `"v2"` | `"v2_03"` |
| `"v2"` | `"v2_04"` |
| `"v2"` | `"v2_05"` |
| `"v2"` | `"v2_06"` |
| `"v2"` | `"v2_07"` |
| `"v2"` | `"v2_08"` |

### Analytical result

`["derived_metrics"]["closure_exposure"]["direct"]["upper_bound"]`

Status: `"available"`; evidence class: `"derived_metric"`; unit: `"ratio"`; method: `"F-010"`.

Value: 0.5.

Denominator: 8; coverage (ratio): 1.0.

| Field | Value |
|---|---|
| `["coverage"]` | 1.0 |
| `["coverage_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["denominator"]` | 8 |
| `["denominator_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["evidence_class"]` | `"derived_metric"` |
| `["method"]` | `"(known_closed_count + unresolved_grounding_count) / total_record_count"` |
| `["method_id"]` | `"F-010"` |
| `["owner_ids"]` | `["T3"]` |
| `["reason_codes"]` | `[]` |
| `["representation"]` | Unavailable (null): No applicable representation supplied; consult status and required evidence. |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["v2"]` |
| `["scope"]["denominator_basis"]` | `"all_valid_records_in_selected_dataset_scope"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"audit-provenance"` |
| `["status"]` | `"available"` |
| `["theory_map_ids"]` | `[]` |
| `["trace_ids"]` | `["T3"]` |
| `["unit"]` | `"ratio"` |
| `["value"]` | 0.5 |
| `["weighting"]["weight_field"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["weighting"]["weighting_mode"]` | `"unweighted"` |

**`["assumptions"]`**

- `"Approved direct grounding partition; uncertainty remains unresolved."`

**`["limitations"]`**

- `"Toolkit operationalization relative to supplied metadata, without lineage or truth certification."`
- `"Direct exposure is relative to the audited loop and supplied metadata."`
- `"Toolkit operationalization; metadata can be incorrect and hidden dependencies unobserved."`
- `"Confidence remains separate; no lineage, midpoint, threshold or causal claim."`

**`["scope"]["included_record_keys"]`**

| `"dataset_version"` | `"record_id"` |
|---|---|
| `"v2"` | `"v2_01"` |
| `"v2"` | `"v2_02"` |
| `"v2"` | `"v2_03"` |
| `"v2"` | `"v2_04"` |
| `"v2"` | `"v2_05"` |
| `"v2"` | `"v2_06"` |
| `"v2"` | `"v2_07"` |
| `"v2"` | `"v2_08"` |

### Analytical result

`["derived_metrics"]["diversity"]["by_version"]["v1"]["distribution_basis"]`

Status: `"available"`; evidence class: `"derived_metric"`; unit: `"basis"`; method: `"T1.validated_distribution_basis"`.

Denominator: 8; coverage (ratio): 1.0.

| Field | Value |
|---|---|
| `["assumptions"]` | `[]` |
| `["coverage"]` | 1.0 |
| `["coverage_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["denominator"]` | 8 |
| `["denominator_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["evidence_class"]` | `"derived_metric"` |
| `["method_id"]` | `"T1.validated_distribution_basis"` |
| `["owner_ids"]` | `["T1"]` |
| `["reason_codes"]` | `[]` |
| `["representation"]["binning_or_mapping_rule"]` | `"literal_field_value"` |
| `["representation"]["field_name"]` | `"topic"` |
| `["representation"]["missing_state_id"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["missing_value_policy"]` | `"error"` |
| `["representation"]["normalization_profile"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["representation_name"]` | `"topic"` |
| `["representation"]["representation_source"]` | `"topic_field"` |
| `["representation"]["representation_version"]` | `"hero-topic-v1"` |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["v1"]` |
| `["scope"]["denominator_basis"]` | `"included_representation_records"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["exclusions"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"audit-representation-earlier"` |
| `["status"]` | `"available"` |
| `["theory_map_ids"]` | `[]` |
| `["trace_ids"]` | `["T1"]` |
| `["unit"]` | `"basis"` |
| `["value"]["analyzed_record_count"]` | 8 |
| `["value"]["denominator_basis"]` | `"included_representation_records"` |
| `["value"]["frequency_denominator"]` | 8 |
| `["value"]["input_basis"]` | `"empirical_assignments"` |
| `["value"]["numerical_policy"]["absolute_tolerance"]` | 1e-12 |
| `["value"]["numerical_policy"]["probability_mass_tolerance"]` | 1e-12 |
| `["value"]["numerical_policy"]["relative_tolerance"]` | 1e-12 |
| `["value"]["probability_residual"]` | 0.0 |
| `["value"]["supplied_probability_total"]` | 1.0 |

**`["limitations"]`**

- `"Distributional concentration does not establish functional failure."`
- `"Record-form support and declared field support do not certify semantic coverage."`
- `"No source, grounding, independence, ancestry or model-performance claim follows."`
- `"Accepted round-off residuals are disclosed and left unchanged."`

**`["scope"]["included_record_keys"]`**

| `"dataset_version"` | `"record_id"` |
|---|---|
| `"v1"` | `"v1_01"` |
| `"v1"` | `"v1_02"` |
| `"v1"` | `"v1_03"` |
| `"v1"` | `"v1_04"` |
| `"v1"` | `"v1_05"` |
| `"v1"` | `"v1_06"` |
| `"v1"` | `"v1_07"` |
| `"v1"` | `"v1_08"` |

### Analytical result

`["derived_metrics"]["diversity"]["by_version"]["v1"]["gini_simpson_diversity"]`

Status: `"available"`; evidence class: `"derived_metric"`; unit: `"dimensionless"`; method: `"F-003"`.

Value: 0.875.

Denominator: 8; coverage (ratio): 1.0.

| Field | Value |
|---|---|
| `["coverage"]` | 1.0 |
| `["coverage_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["denominator"]` | 8 |
| `["denominator_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["evidence_class"]` | `"derived_metric"` |
| `["input_basis"]` | `"empirical_assignments"` |
| `["method"]` | `"explicit_counts_divided_by_included_records"` |
| `["method_id"]` | `"F-003"` |
| `["owner_ids"]` | `["T1"]` |
| `["reason_codes"]` | `[]` |
| `["representation"]["binning_or_mapping_rule"]` | `"literal_field_value"` |
| `["representation"]["field_name"]` | `"topic"` |
| `["representation"]["missing_state_id"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["missing_value_policy"]` | `"error"` |
| `["representation"]["normalization_profile"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["representation_name"]` | `"topic"` |
| `["representation"]["representation_source"]` | `"topic_field"` |
| `["representation"]["representation_version"]` | `"hero-topic-v1"` |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["v1"]` |
| `["scope"]["denominator_basis"]` | `"included_representation_records"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["exclusions"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"audit-representation-earlier"` |
| `["status"]` | `"available"` |
| `["theory_map_ids"]` | `[]` |
| `["trace_ids"]` | `["T1"]` |
| `["unit"]` | `"dimensionless"` |
| `["value"]` | 0.875 |
| `["weighting"]["weight_field"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["weighting"]["weighting_mode"]` | `"unweighted"` |

**`["assumptions"]`**

- `"One explicitly selected version and declared representation."`
- `"No implicit pooling, probability repair, confidence weighting or sampling."`

**`["limitations"]`**

- `"Representation-bound; does not establish functional failure or semantic completeness."`
- `"Distributional concentration does not establish functional failure."`
- `"Record-form support and declared field support do not certify semantic coverage."`
- `"No source, grounding, independence, ancestry or model-performance claim follows."`
- `"Accepted round-off residuals are disclosed and left unchanged."`

**`["scope"]["included_record_keys"]`**

| `"dataset_version"` | `"record_id"` |
|---|---|
| `"v1"` | `"v1_01"` |
| `"v1"` | `"v1_02"` |
| `"v1"` | `"v1_03"` |
| `"v1"` | `"v1_04"` |
| `"v1"` | `"v1_05"` |
| `"v1"` | `"v1_06"` |
| `"v1"` | `"v1_07"` |
| `"v1"` | `"v1_08"` |

### Analytical result

`["derived_metrics"]["diversity"]["by_version"]["v1"]["simpson_concentration"]`

Status: `"available"`; evidence class: `"derived_metric"`; unit: `"dimensionless"`; method: `"F-004"`.

Value: 0.125.

Denominator: 8; coverage (ratio): 1.0.

| Field | Value |
|---|---|
| `["coverage"]` | 1.0 |
| `["coverage_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["denominator"]` | 8 |
| `["denominator_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["evidence_class"]` | `"derived_metric"` |
| `["input_basis"]` | `"empirical_assignments"` |
| `["method"]` | `"explicit_counts_divided_by_included_records"` |
| `["method_id"]` | `"F-004"` |
| `["owner_ids"]` | `["T1"]` |
| `["reason_codes"]` | `[]` |
| `["representation"]["binning_or_mapping_rule"]` | `"literal_field_value"` |
| `["representation"]["field_name"]` | `"topic"` |
| `["representation"]["missing_state_id"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["missing_value_policy"]` | `"error"` |
| `["representation"]["normalization_profile"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["representation_name"]` | `"topic"` |
| `["representation"]["representation_source"]` | `"topic_field"` |
| `["representation"]["representation_version"]` | `"hero-topic-v1"` |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["v1"]` |
| `["scope"]["denominator_basis"]` | `"included_representation_records"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["exclusions"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"audit-representation-earlier"` |
| `["status"]` | `"available"` |
| `["theory_map_ids"]` | `[]` |
| `["trace_ids"]` | `["T1"]` |
| `["unit"]` | `"dimensionless"` |
| `["value"]` | 0.125 |
| `["weighting"]["weight_field"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["weighting"]["weighting_mode"]` | `"unweighted"` |

**`["assumptions"]`**

- `"One explicitly selected version and declared representation."`
- `"No implicit pooling, probability repair, confidence weighting or sampling."`

**`["limitations"]`**

- `"Representation-bound; does not establish functional failure or semantic completeness."`
- `"Distributional concentration does not establish functional failure."`
- `"Record-form support and declared field support do not certify semantic coverage."`
- `"No source, grounding, independence, ancestry or model-performance claim follows."`
- `"Accepted round-off residuals are disclosed and left unchanged."`

**`["scope"]["included_record_keys"]`**

| `"dataset_version"` | `"record_id"` |
|---|---|
| `"v1"` | `"v1_01"` |
| `"v1"` | `"v1_02"` |
| `"v1"` | `"v1_03"` |
| `"v1"` | `"v1_04"` |
| `"v1"` | `"v1_05"` |
| `"v1"` | `"v1_06"` |
| `"v1"` | `"v1_07"` |
| `"v1"` | `"v1_08"` |

### Analytical result

`["derived_metrics"]["diversity"]["by_version"]["v1"]["state_frequencies"]`

Status: `"available"`; evidence class: `"derived_metric"`; unit: `"ratio"`; method: `"F-001"`.

Denominator: 8; coverage (ratio): 1.0.

| Field | Value |
|---|---|
| `["coverage"]` | 1.0 |
| `["coverage_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["denominator"]` | 8 |
| `["denominator_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["evidence_class"]` | `"derived_metric"` |
| `["method"]` | `"empirical_assignments; n_i/N"` |
| `["method_id"]` | `"F-001"` |
| `["owner_ids"]` | `["T1"]` |
| `["reason_codes"]` | `[]` |
| `["representation"]["binning_or_mapping_rule"]` | `"literal_field_value"` |
| `["representation"]["field_name"]` | `"topic"` |
| `["representation"]["missing_state_id"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["missing_value_policy"]` | `"error"` |
| `["representation"]["normalization_profile"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["representation_name"]` | `"topic"` |
| `["representation"]["representation_source"]` | `"topic_field"` |
| `["representation"]["representation_version"]` | `"hero-topic-v1"` |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["v1"]` |
| `["scope"]["denominator_basis"]` | `"included_representation_records"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["exclusions"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"audit-representation-earlier"` |
| `["status"]` | `"available"` |
| `["theory_map_ids"]` | `[]` |
| `["trace_ids"]` | `["T1"]` |
| `["unit"]` | `"ratio"` |
| `["weighting"]["weight_field"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["weighting"]["weighting_mode"]` | `"unweighted"` |

**`["assumptions"]`**

- `"One explicitly selected version and declared representation."`
- `"No implicit pooling, probability repair, confidence weighting or sampling."`

**`["limitations"]`**

- `"Representation-bound; does not establish functional failure or semantic completeness."`
- `"Distributional concentration does not establish functional failure."`
- `"Record-form support and declared field support do not certify semantic coverage."`
- `"No source, grounding, independence, ancestry or model-performance claim follows."`
- `"Accepted round-off residuals are disclosed and left unchanged."`

**`["scope"]["included_record_keys"]`**

| `"dataset_version"` | `"record_id"` |
|---|---|
| `"v1"` | `"v1_01"` |
| `"v1"` | `"v1_02"` |
| `"v1"` | `"v1_03"` |
| `"v1"` | `"v1_04"` |
| `"v1"` | `"v1_05"` |
| `"v1"` | `"v1_06"` |
| `"v1"` | `"v1_07"` |
| `"v1"` | `"v1_08"` |

**`["value"]`**

| `"state_frequency"` | `"state_id"` |
|---|---|
| 0.125 | `"battery"` |
| 0.125 | `"bird"` |
| 0.125 | `"cat"` |
| 0.125 | `"dog"` |
| 0.125 | `"fish"` |
| 0.125 | `"lizard"` |
| 0.125 | `"refund"` |
| 0.125 | `"turtle"` |

### Analytical result

`["derived_metrics"]["diversity"]["by_version"]["v2"]["distribution_basis"]`

Status: `"available"`; evidence class: `"derived_metric"`; unit: `"basis"`; method: `"T1.validated_distribution_basis"`.

Denominator: 8; coverage (ratio): 1.0.

| Field | Value |
|---|---|
| `["assumptions"]` | `[]` |
| `["coverage"]` | 1.0 |
| `["coverage_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["denominator"]` | 8 |
| `["denominator_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["evidence_class"]` | `"derived_metric"` |
| `["method_id"]` | `"T1.validated_distribution_basis"` |
| `["owner_ids"]` | `["T1"]` |
| `["reason_codes"]` | `[]` |
| `["representation"]["binning_or_mapping_rule"]` | `"literal_field_value"` |
| `["representation"]["field_name"]` | `"topic"` |
| `["representation"]["missing_state_id"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["missing_value_policy"]` | `"error"` |
| `["representation"]["normalization_profile"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["representation_name"]` | `"topic"` |
| `["representation"]["representation_source"]` | `"topic_field"` |
| `["representation"]["representation_version"]` | `"hero-topic-v1"` |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["v2"]` |
| `["scope"]["denominator_basis"]` | `"included_representation_records"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["exclusions"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"audit-representation"` |
| `["status"]` | `"available"` |
| `["theory_map_ids"]` | `[]` |
| `["trace_ids"]` | `["T1"]` |
| `["unit"]` | `"basis"` |
| `["value"]["analyzed_record_count"]` | 8 |
| `["value"]["denominator_basis"]` | `"included_representation_records"` |
| `["value"]["frequency_denominator"]` | 8 |
| `["value"]["input_basis"]` | `"empirical_assignments"` |
| `["value"]["numerical_policy"]["absolute_tolerance"]` | 1e-12 |
| `["value"]["numerical_policy"]["probability_mass_tolerance"]` | 1e-12 |
| `["value"]["numerical_policy"]["relative_tolerance"]` | 1e-12 |
| `["value"]["probability_residual"]` | 0.0 |
| `["value"]["supplied_probability_total"]` | 1.0 |

**`["limitations"]`**

- `"Distributional concentration does not establish functional failure."`
- `"Record-form support and declared field support do not certify semantic coverage."`
- `"No source, grounding, independence, ancestry or model-performance claim follows."`
- `"Accepted round-off residuals are disclosed and left unchanged."`

**`["scope"]["included_record_keys"]`**

| `"dataset_version"` | `"record_id"` |
|---|---|
| `"v2"` | `"v2_01"` |
| `"v2"` | `"v2_02"` |
| `"v2"` | `"v2_03"` |
| `"v2"` | `"v2_04"` |
| `"v2"` | `"v2_05"` |
| `"v2"` | `"v2_06"` |
| `"v2"` | `"v2_07"` |
| `"v2"` | `"v2_08"` |

### Analytical result

`["derived_metrics"]["diversity"]["by_version"]["v2"]["gini_simpson_diversity"]`

Status: `"available"`; evidence class: `"derived_metric"`; unit: `"dimensionless"`; method: `"F-003"`.

Value: 0.75.

Denominator: 8; coverage (ratio): 1.0.

| Field | Value |
|---|---|
| `["coverage"]` | 1.0 |
| `["coverage_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["denominator"]` | 8 |
| `["denominator_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["evidence_class"]` | `"derived_metric"` |
| `["input_basis"]` | `"empirical_assignments"` |
| `["method"]` | `"explicit_counts_divided_by_included_records"` |
| `["method_id"]` | `"F-003"` |
| `["owner_ids"]` | `["T1"]` |
| `["reason_codes"]` | `[]` |
| `["representation"]["binning_or_mapping_rule"]` | `"literal_field_value"` |
| `["representation"]["field_name"]` | `"topic"` |
| `["representation"]["missing_state_id"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["missing_value_policy"]` | `"error"` |
| `["representation"]["normalization_profile"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["representation_name"]` | `"topic"` |
| `["representation"]["representation_source"]` | `"topic_field"` |
| `["representation"]["representation_version"]` | `"hero-topic-v1"` |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["v2"]` |
| `["scope"]["denominator_basis"]` | `"included_representation_records"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["exclusions"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"audit-representation"` |
| `["status"]` | `"available"` |
| `["theory_map_ids"]` | `[]` |
| `["trace_ids"]` | `["T1"]` |
| `["unit"]` | `"dimensionless"` |
| `["value"]` | 0.75 |
| `["weighting"]["weight_field"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["weighting"]["weighting_mode"]` | `"unweighted"` |

**`["assumptions"]`**

- `"One explicitly selected version and declared representation."`
- `"No implicit pooling, probability repair, confidence weighting or sampling."`

**`["limitations"]`**

- `"Representation-bound; does not establish functional failure or semantic completeness."`
- `"Distributional concentration does not establish functional failure."`
- `"Record-form support and declared field support do not certify semantic coverage."`
- `"No source, grounding, independence, ancestry or model-performance claim follows."`
- `"Accepted round-off residuals are disclosed and left unchanged."`

**`["scope"]["included_record_keys"]`**

| `"dataset_version"` | `"record_id"` |
|---|---|
| `"v2"` | `"v2_01"` |
| `"v2"` | `"v2_02"` |
| `"v2"` | `"v2_03"` |
| `"v2"` | `"v2_04"` |
| `"v2"` | `"v2_05"` |
| `"v2"` | `"v2_06"` |
| `"v2"` | `"v2_07"` |
| `"v2"` | `"v2_08"` |

### Analytical result

`["derived_metrics"]["diversity"]["by_version"]["v2"]["simpson_concentration"]`

Status: `"available"`; evidence class: `"derived_metric"`; unit: `"dimensionless"`; method: `"F-004"`.

Value: 0.25.

Denominator: 8; coverage (ratio): 1.0.

| Field | Value |
|---|---|
| `["coverage"]` | 1.0 |
| `["coverage_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["denominator"]` | 8 |
| `["denominator_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["evidence_class"]` | `"derived_metric"` |
| `["input_basis"]` | `"empirical_assignments"` |
| `["method"]` | `"explicit_counts_divided_by_included_records"` |
| `["method_id"]` | `"F-004"` |
| `["owner_ids"]` | `["T1"]` |
| `["reason_codes"]` | `[]` |
| `["representation"]["binning_or_mapping_rule"]` | `"literal_field_value"` |
| `["representation"]["field_name"]` | `"topic"` |
| `["representation"]["missing_state_id"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["missing_value_policy"]` | `"error"` |
| `["representation"]["normalization_profile"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["representation_name"]` | `"topic"` |
| `["representation"]["representation_source"]` | `"topic_field"` |
| `["representation"]["representation_version"]` | `"hero-topic-v1"` |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["v2"]` |
| `["scope"]["denominator_basis"]` | `"included_representation_records"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["exclusions"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"audit-representation"` |
| `["status"]` | `"available"` |
| `["theory_map_ids"]` | `[]` |
| `["trace_ids"]` | `["T1"]` |
| `["unit"]` | `"dimensionless"` |
| `["value"]` | 0.25 |
| `["weighting"]["weight_field"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["weighting"]["weighting_mode"]` | `"unweighted"` |

**`["assumptions"]`**

- `"One explicitly selected version and declared representation."`
- `"No implicit pooling, probability repair, confidence weighting or sampling."`

**`["limitations"]`**

- `"Representation-bound; does not establish functional failure or semantic completeness."`
- `"Distributional concentration does not establish functional failure."`
- `"Record-form support and declared field support do not certify semantic coverage."`
- `"No source, grounding, independence, ancestry or model-performance claim follows."`
- `"Accepted round-off residuals are disclosed and left unchanged."`

**`["scope"]["included_record_keys"]`**

| `"dataset_version"` | `"record_id"` |
|---|---|
| `"v2"` | `"v2_01"` |
| `"v2"` | `"v2_02"` |
| `"v2"` | `"v2_03"` |
| `"v2"` | `"v2_04"` |
| `"v2"` | `"v2_05"` |
| `"v2"` | `"v2_06"` |
| `"v2"` | `"v2_07"` |
| `"v2"` | `"v2_08"` |

### Analytical result

`["derived_metrics"]["diversity"]["by_version"]["v2"]["state_frequencies"]`

Status: `"available"`; evidence class: `"derived_metric"`; unit: `"ratio"`; method: `"F-001"`.

Denominator: 8; coverage (ratio): 1.0.

| Field | Value |
|---|---|
| `["coverage"]` | 1.0 |
| `["coverage_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["denominator"]` | 8 |
| `["denominator_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["evidence_class"]` | `"derived_metric"` |
| `["method"]` | `"empirical_assignments; n_i/N"` |
| `["method_id"]` | `"F-001"` |
| `["owner_ids"]` | `["T1"]` |
| `["reason_codes"]` | `[]` |
| `["representation"]["binning_or_mapping_rule"]` | `"literal_field_value"` |
| `["representation"]["field_name"]` | `"topic"` |
| `["representation"]["missing_state_id"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["missing_value_policy"]` | `"error"` |
| `["representation"]["normalization_profile"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["representation_name"]` | `"topic"` |
| `["representation"]["representation_source"]` | `"topic_field"` |
| `["representation"]["representation_version"]` | `"hero-topic-v1"` |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["v2"]` |
| `["scope"]["denominator_basis"]` | `"included_representation_records"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["exclusions"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"audit-representation"` |
| `["status"]` | `"available"` |
| `["theory_map_ids"]` | `[]` |
| `["trace_ids"]` | `["T1"]` |
| `["unit"]` | `"ratio"` |
| `["weighting"]["weight_field"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["weighting"]["weighting_mode"]` | `"unweighted"` |

**`["assumptions"]`**

- `"One explicitly selected version and declared representation."`
- `"No implicit pooling, probability repair, confidence weighting or sampling."`

**`["limitations"]`**

- `"Representation-bound; does not establish functional failure or semantic completeness."`
- `"Distributional concentration does not establish functional failure."`
- `"Record-form support and declared field support do not certify semantic coverage."`
- `"No source, grounding, independence, ancestry or model-performance claim follows."`
- `"Accepted round-off residuals are disclosed and left unchanged."`

**`["scope"]["included_record_keys"]`**

| `"dataset_version"` | `"record_id"` |
|---|---|
| `"v2"` | `"v2_01"` |
| `"v2"` | `"v2_02"` |
| `"v2"` | `"v2_03"` |
| `"v2"` | `"v2_04"` |
| `"v2"` | `"v2_05"` |
| `"v2"` | `"v2_06"` |
| `"v2"` | `"v2_07"` |
| `"v2"` | `"v2_08"` |

**`["value"]`**

| `"state_frequency"` | `"state_id"` |
|---|---|
| 0.125 | `"bird"` |
| 0.375 | `"cat"` |
| 0.25 | `"dog"` |
| 0.125 | `"fish"` |
| 0.125 | `"refund"` |

### Analytical result

`["derived_metrics"]["diversity"]["gini_simpson_diversity_delta"]`

Status: `"available"`; evidence class: `"derived_metric"`; unit: `"dimensionless"`; method: `"F-018"`.

Value: -0.125.

Denominator: 8; coverage (ratio): Unavailable (null): `"coverage_not_supplied_for_this_result"`.

| Field | Value |
|---|---|
| `["coverage"]` | Unavailable (null): `"coverage_not_supplied_for_this_result"` |
| `["coverage_reason"]` | `"coverage_not_supplied_for_this_result"` |
| `["denominator"]` | 8 |
| `["denominator_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["evidence_class"]` | `"derived_metric"` |
| `["input_basis"]` | `"empirical_assignments"` |
| `["method"]` | `"later Gini-Simpson diversity minus earlier diversity"` |
| `["method_id"]` | `"F-018"` |
| `["owner_ids"]` | `["T1"]` |
| `["reason_codes"]` | `[]` |
| `["representation"]["binning_or_mapping_rule"]` | `"literal_field_value"` |
| `["representation"]["field_name"]` | `"topic"` |
| `["representation"]["missing_state_id"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["missing_value_policy"]` | `"error"` |
| `["representation"]["normalization_profile"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["representation_name"]` | `"topic"` |
| `["representation"]["representation_source"]` | `"topic_field"` |
| `["representation"]["representation_version"]` | `"hero-topic-v1"` |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["v1", "v2"]` |
| `["scope"]["denominator_basis"]` | `"separate_ordered_representation_scopes"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 16 |
| `["scope"]["scope_id"]` | `"audit-representation-earlier -\u003e audit-representation"` |
| `["status"]` | `"available"` |
| `["theory_map_ids"]` | `[]` |
| `["trace_ids"]` | `["T1"]` |
| `["unit"]` | `"dimensionless"` |
| `["value"]` | -0.125 |
| `["weighting"]["weight_field"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["weighting"]["weighting_mode"]` | `"unweighted"` |

**`["assumptions"]`**

- `"Earlier and later scopes explicitly selected and independently validated."`
- `"State identity uses the declared common basis, including any disclosed map."`

**`["limitations"]`**

- `"Observed/supplied support only; no permanent extinction or causal/model-performance verdict."`
- `"A coarsened comparison cannot recover distinctions lost through its mapping."`
- `"One explicitly selected earlier/later pair only; no trajectory or automatic adjacent comparison."`
- `"Extinct means absent from the supplied later support in the harmonized representation."`
- `"No permanent process extinction, causality, model-performance or source-independence claim follows."`
- `"Supplied probability vectors remain mathematical inputs, not empirical record-frequency observations."`
- `"Many-to-one mapping can conceal original distinctions; original inputs remain separately visible."`
- `"Weighted support is positive weight mass, not unweighted record presence."`

**`["scope"]["included_record_keys"]`**

| `"dataset_version"` | `"record_id"` |
|---|---|
| `"v1"` | `"v1_01"` |
| `"v1"` | `"v1_02"` |
| `"v1"` | `"v1_03"` |
| `"v1"` | `"v1_04"` |
| `"v1"` | `"v1_05"` |
| `"v1"` | `"v1_06"` |
| `"v1"` | `"v1_07"` |
| `"v1"` | `"v1_08"` |
| `"v2"` | `"v2_01"` |
| `"v2"` | `"v2_02"` |
| `"v2"` | `"v2_03"` |
| `"v2"` | `"v2_04"` |
| `"v2"` | `"v2_05"` |
| `"v2"` | `"v2_06"` |
| `"v2"` | `"v2_07"` |
| `"v2"` | `"v2_08"` |

### Analytical result

`["derived_metrics"]["lineage"]["resolved_parent_edge_coverage"]`

Status: `"available"`; evidence class: `"derived_metric"`; unit: `"ratio"`; method: `"PR-008.resolved_edges_over_declared"`.

Value: 1.0.

Denominator: 8; coverage (ratio): 1.0.

| Field | Value |
|---|---|
| `["assumptions"]` | `[]` |
| `["coverage"]` | 1.0 |
| `["coverage_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["denominator"]` | 8 |
| `["denominator_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["evidence_class"]` | `"derived_metric"` |
| `["method_id"]` | `"PR-008.resolved_edges_over_declared"` |
| `["owner_ids"]` | `["PR-008"]` |
| `["reason_codes"]` | `[]` |
| `["representation"]` | Unavailable (null): No applicable representation supplied; consult status and required evidence. |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["v1", "v2"]` |
| `["scope"]["denominator_basis"]` | `"all_validated_bundle_records"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 16 |
| `["scope"]["scope_id"]` | `"validated_bundle"` |
| `["status"]` | `"available"` |
| `["theory_map_ids"]` | `[]` |
| `["trace_ids"]` | `[]` |
| `["unit"]` | `"ratio"` |
| `["value"]` | 1.0 |

**`["limitations"]`**

- `"Immediate-reference validation coverage does not establish resolved ancestry or external roots."`

**`["scope"]["included_record_keys"]`**

| `"dataset_version"` | `"record_id"` |
|---|---|
| `"v1"` | `"v1_01"` |
| `"v1"` | `"v1_02"` |
| `"v1"` | `"v1_03"` |
| `"v1"` | `"v1_04"` |
| `"v1"` | `"v1_05"` |
| `"v1"` | `"v1_06"` |
| `"v1"` | `"v1_07"` |
| `"v1"` | `"v1_08"` |
| `"v2"` | `"v2_01"` |
| `"v2"` | `"v2_02"` |
| `"v2"` | `"v2_03"` |
| `"v2"` | `"v2_04"` |
| `"v2"` | `"v2_05"` |
| `"v2"` | `"v2_06"` |
| `"v2"` | `"v2_07"` |
| `"v2"` | `"v2_08"` |

### Analytical result

`["derived_metrics"]["provenance"]["missing_provenance_share"]`

Status: `"available"`; evidence class: `"derived_metric"`; unit: `"ratio"`; method: `"PR-004.one_minus_row_coverage"`.

Value: 0.0.

Denominator: 8; coverage (ratio): Unavailable (null): `"coverage_not_supplied_for_this_result"`.

| Field | Value |
|---|---|
| `["coverage"]` | Unavailable (null): `"coverage_not_supplied_for_this_result"` |
| `["coverage_reason"]` | `"coverage_not_supplied_for_this_result"` |
| `["denominator"]` | 8 |
| `["denominator_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["evidence_class"]` | `"derived_metric"` |
| `["method"]` | `"Definitions 11.4; missing rows / all selected valid records"` |
| `["method_id"]` | `"PR-004.one_minus_row_coverage"` |
| `["owner_ids"]` | `["PR-004"]` |
| `["reason_codes"]` | `[]` |
| `["representation"]` | Unavailable (null): No applicable representation supplied; consult status and required evidence. |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["v2"]` |
| `["scope"]["denominator_basis"]` | `"all_valid_records_in_selected_dataset_scope"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"audit-provenance"` |
| `["status"]` | `"available"` |
| `["theory_map_ids"]` | `[]` |
| `["trace_ids"]` | `[]` |
| `["unit"]` | `"ratio"` |
| `["value"]` | 0.0 |
| `["weighting"]["weight_field"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["weighting"]["weighting_mode"]` | `"unweighted"` |

**`["assumptions"]`**

- `"Exact explicit single-version Phase 2 join scope; no representation exclusions."`

**`["limitations"]`**

- `"Supplied declarations only; no truth or source-independence certification."`
- `"Declared composition does not certify input validity or increase observability."`
- `"Source, confidence, human review and grounding are independent declarations."`
- `"Representation exclusions cannot reduce the provenance denominator."`

**`["scope"]["included_record_keys"]`**

| `"dataset_version"` | `"record_id"` |
|---|---|
| `"v2"` | `"v2_01"` |
| `"v2"` | `"v2_02"` |
| `"v2"` | `"v2_03"` |
| `"v2"` | `"v2_04"` |
| `"v2"` | `"v2_05"` |
| `"v2"` | `"v2_06"` |
| `"v2"` | `"v2_07"` |
| `"v2"` | `"v2_08"` |

### Analytical result

`["derived_metrics"]["provenance"]["source_type_shares"]`

Status: `"available"`; evidence class: `"derived_metric"`; unit: `"ratio"`; method: `"F-007"`.

Denominator: 8; coverage (ratio): 1.0.

| Field | Value |
|---|---|
| `["coverage"]` | 1.0 |
| `["coverage_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["denominator"]` | 8 |
| `["denominator_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["evidence_class"]` | `"derived_metric"` |
| `["method"]` | `"category count / all selected valid records"` |
| `["method_id"]` | `"F-007"` |
| `["owner_ids"]` | `["PR-005"]` |
| `["reason_codes"]` | `[]` |
| `["representation"]` | Unavailable (null): No applicable representation supplied; consult status and required evidence. |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["v2"]` |
| `["scope"]["denominator_basis"]` | `"all_valid_records_in_selected_dataset_scope"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"audit-provenance"` |
| `["status"]` | `"available"` |
| `["theory_map_ids"]` | `[]` |
| `["trace_ids"]` | `[]` |
| `["unit"]` | `"ratio"` |
| `["value"]["human"]` | 0.5 |
| `["value"]["mixed"]` | 0.0 |
| `["value"]["sensor"]` | 0.0 |
| `["value"]["synthetic"]` | 0.5 |
| `["value"]["unknown"]` | 0.0 |
| `["weighting"]["weight_field"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["weighting"]["weighting_mode"]` | `"unweighted"` |

**`["assumptions"]`**

- `"Exact explicit single-version Phase 2 join scope; no representation exclusions."`

**`["limitations"]`**

- `"Supplied declarations only; no truth or source-independence certification."`
- `"Declared composition does not certify input validity or increase observability."`
- `"Source, confidence, human review and grounding are independent declarations."`
- `"Representation exclusions cannot reduce the provenance denominator."`

**`["scope"]["included_record_keys"]`**

| `"dataset_version"` | `"record_id"` |
|---|---|
| `"v2"` | `"v2_01"` |
| `"v2"` | `"v2_02"` |
| `"v2"` | `"v2_03"` |
| `"v2"` | `"v2_04"` |
| `"v2"` | `"v2_05"` |
| `"v2"` | `"v2_06"` |
| `"v2"` | `"v2_07"` |
| `"v2"` | `"v2_08"` |

### Analytical result

`["derived_metrics"]["support"]["added_states"]`

Status: `"available"`; evidence class: `"derived_metric"`; unit: `"set_of_states"`; method: `"T1.later_minus_earlier"`.

Denominator: 8; coverage (ratio): Unavailable (null): `"coverage_not_supplied_for_this_result"`.

| Field | Value |
|---|---|
| `["coverage"]` | Unavailable (null): `"coverage_not_supplied_for_this_result"` |
| `["coverage_reason"]` | `"coverage_not_supplied_for_this_result"` |
| `["denominator"]` | 8 |
| `["denominator_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["evidence_class"]` | `"derived_metric"` |
| `["input_basis"]` | `"empirical_assignments"` |
| `["method"]` | `"later support minus earlier support"` |
| `["method_id"]` | `"T1.later_minus_earlier"` |
| `["owner_ids"]` | `["T1"]` |
| `["reason_codes"]` | `[]` |
| `["representation"]["binning_or_mapping_rule"]` | `"literal_field_value"` |
| `["representation"]["field_name"]` | `"topic"` |
| `["representation"]["missing_state_id"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["missing_value_policy"]` | `"error"` |
| `["representation"]["normalization_profile"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["representation_name"]` | `"topic"` |
| `["representation"]["representation_source"]` | `"topic_field"` |
| `["representation"]["representation_version"]` | `"hero-topic-v1"` |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["v1", "v2"]` |
| `["scope"]["denominator_basis"]` | `"separate_ordered_representation_scopes"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 16 |
| `["scope"]["scope_id"]` | `"audit-representation-earlier -\u003e audit-representation"` |
| `["status"]` | `"available"` |
| `["theory_map_ids"]` | `[]` |
| `["trace_ids"]` | `["T1"]` |
| `["unit"]` | `"set_of_states"` |
| `["value"]` | `[]` |
| `["weighting"]["weight_field"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["weighting"]["weighting_mode"]` | `"unweighted"` |

**`["assumptions"]`**

- `"Earlier and later scopes explicitly selected and independently validated."`
- `"State identity uses the declared common basis, including any disclosed map."`

**`["limitations"]`**

- `"Observed/supplied support only; no permanent extinction or causal/model-performance verdict."`
- `"A coarsened comparison cannot recover distinctions lost through its mapping."`
- `"One explicitly selected earlier/later pair only; no trajectory or automatic adjacent comparison."`
- `"Extinct means absent from the supplied later support in the harmonized representation."`
- `"No permanent process extinction, causality, model-performance or source-independence claim follows."`
- `"Supplied probability vectors remain mathematical inputs, not empirical record-frequency observations."`
- `"Many-to-one mapping can conceal original distinctions; original inputs remain separately visible."`
- `"Weighted support is positive weight mass, not unweighted record presence."`

**`["scope"]["included_record_keys"]`**

| `"dataset_version"` | `"record_id"` |
|---|---|
| `"v1"` | `"v1_01"` |
| `"v1"` | `"v1_02"` |
| `"v1"` | `"v1_03"` |
| `"v1"` | `"v1_04"` |
| `"v1"` | `"v1_05"` |
| `"v1"` | `"v1_06"` |
| `"v1"` | `"v1_07"` |
| `"v1"` | `"v1_08"` |
| `"v2"` | `"v2_01"` |
| `"v2"` | `"v2_02"` |
| `"v2"` | `"v2_03"` |
| `"v2"` | `"v2_04"` |
| `"v2"` | `"v2_05"` |
| `"v2"` | `"v2_06"` |
| `"v2"` | `"v2_07"` |
| `"v2"` | `"v2_08"` |

### Analytical result

`["derived_metrics"]["support"]["by_version"]["v1"]["support_size"]`

Status: `"available"`; evidence class: `"derived_metric"`; unit: `"states"`; method: `"F-002"`.

Value: 8.

Denominator: 8; coverage (ratio): 1.0.

| Field | Value |
|---|---|
| `["coverage"]` | 1.0 |
| `["coverage_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["denominator"]` | 8 |
| `["denominator_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["evidence_class"]` | `"derived_metric"` |
| `["input_basis"]` | `"empirical_assignments"` |
| `["method"]` | `"explicit_counts_divided_by_included_records"` |
| `["method_id"]` | `"F-002"` |
| `["owner_ids"]` | `["T1"]` |
| `["reason_codes"]` | `[]` |
| `["representation"]["binning_or_mapping_rule"]` | `"literal_field_value"` |
| `["representation"]["field_name"]` | `"topic"` |
| `["representation"]["missing_state_id"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["missing_value_policy"]` | `"error"` |
| `["representation"]["normalization_profile"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["representation_name"]` | `"topic"` |
| `["representation"]["representation_source"]` | `"topic_field"` |
| `["representation"]["representation_version"]` | `"hero-topic-v1"` |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["v1"]` |
| `["scope"]["denominator_basis"]` | `"included_representation_records"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["exclusions"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"audit-representation-earlier"` |
| `["status"]` | `"available"` |
| `["theory_map_ids"]` | `[]` |
| `["trace_ids"]` | `["T1"]` |
| `["unit"]` | `"states"` |
| `["value"]` | 8 |
| `["weighting"]["weight_field"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["weighting"]["weighting_mode"]` | `"unweighted"` |

**`["assumptions"]`**

- `"One explicitly selected version and declared representation."`
- `"No implicit pooling, probability repair, confidence weighting or sampling."`

**`["limitations"]`**

- `"Representation-bound; does not establish functional failure or semantic completeness."`
- `"Distributional concentration does not establish functional failure."`
- `"Record-form support and declared field support do not certify semantic coverage."`
- `"No source, grounding, independence, ancestry or model-performance claim follows."`
- `"Accepted round-off residuals are disclosed and left unchanged."`

**`["scope"]["included_record_keys"]`**

| `"dataset_version"` | `"record_id"` |
|---|---|
| `"v1"` | `"v1_01"` |
| `"v1"` | `"v1_02"` |
| `"v1"` | `"v1_03"` |
| `"v1"` | `"v1_04"` |
| `"v1"` | `"v1_05"` |
| `"v1"` | `"v1_06"` |
| `"v1"` | `"v1_07"` |
| `"v1"` | `"v1_08"` |

### Analytical result

`["derived_metrics"]["support"]["by_version"]["v2"]["support_size"]`

Status: `"available"`; evidence class: `"derived_metric"`; unit: `"states"`; method: `"F-002"`.

Value: 5.

Denominator: 8; coverage (ratio): 1.0.

| Field | Value |
|---|---|
| `["coverage"]` | 1.0 |
| `["coverage_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["denominator"]` | 8 |
| `["denominator_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["evidence_class"]` | `"derived_metric"` |
| `["input_basis"]` | `"empirical_assignments"` |
| `["method"]` | `"explicit_counts_divided_by_included_records"` |
| `["method_id"]` | `"F-002"` |
| `["owner_ids"]` | `["T1"]` |
| `["reason_codes"]` | `[]` |
| `["representation"]["binning_or_mapping_rule"]` | `"literal_field_value"` |
| `["representation"]["field_name"]` | `"topic"` |
| `["representation"]["missing_state_id"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["missing_value_policy"]` | `"error"` |
| `["representation"]["normalization_profile"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["representation_name"]` | `"topic"` |
| `["representation"]["representation_source"]` | `"topic_field"` |
| `["representation"]["representation_version"]` | `"hero-topic-v1"` |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["v2"]` |
| `["scope"]["denominator_basis"]` | `"included_representation_records"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["exclusions"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"audit-representation"` |
| `["status"]` | `"available"` |
| `["theory_map_ids"]` | `[]` |
| `["trace_ids"]` | `["T1"]` |
| `["unit"]` | `"states"` |
| `["value"]` | 5 |
| `["weighting"]["weight_field"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["weighting"]["weighting_mode"]` | `"unweighted"` |

**`["assumptions"]`**

- `"One explicitly selected version and declared representation."`
- `"No implicit pooling, probability repair, confidence weighting or sampling."`

**`["limitations"]`**

- `"Representation-bound; does not establish functional failure or semantic completeness."`
- `"Distributional concentration does not establish functional failure."`
- `"Record-form support and declared field support do not certify semantic coverage."`
- `"No source, grounding, independence, ancestry or model-performance claim follows."`
- `"Accepted round-off residuals are disclosed and left unchanged."`

**`["scope"]["included_record_keys"]`**

| `"dataset_version"` | `"record_id"` |
|---|---|
| `"v2"` | `"v2_01"` |
| `"v2"` | `"v2_02"` |
| `"v2"` | `"v2_03"` |
| `"v2"` | `"v2_04"` |
| `"v2"` | `"v2_05"` |
| `"v2"` | `"v2_06"` |
| `"v2"` | `"v2_07"` |
| `"v2"` | `"v2_08"` |

### Analytical result

`["derived_metrics"]["support"]["comparison_details"]`

Status: `"available"`; evidence class: `"derived_metric"`; unit: `"comparison"`; method: `"T1.explicit_pair_basis"`.

Denominator: 8; coverage (ratio): Unavailable (null): `"coverage_not_supplied_for_this_result"`.

| Field | Value |
|---|---|
| `["coverage"]` | Unavailable (null): `"coverage_not_supplied_for_this_result"` |
| `["coverage_reason"]` | `"coverage_not_supplied_for_this_result"` |
| `["denominator"]` | 8 |
| `["denominator_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["evidence_class"]` | `"derived_metric"` |
| `["method_id"]` | `"T1.explicit_pair_basis"` |
| `["owner_ids"]` | `["T1"]` |
| `["reason_codes"]` | `[]` |
| `["representation"]["binning_or_mapping_rule"]` | `"literal_field_value"` |
| `["representation"]["field_name"]` | `"topic"` |
| `["representation"]["missing_state_id"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["missing_value_policy"]` | `"error"` |
| `["representation"]["normalization_profile"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["representation_name"]` | `"topic"` |
| `["representation"]["representation_source"]` | `"topic_field"` |
| `["representation"]["representation_version"]` | `"hero-topic-v1"` |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["v1", "v2"]` |
| `["scope"]["denominator_basis"]` | `"separate_ordered_representation_scopes"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 16 |
| `["scope"]["scope_id"]` | `"audit-representation-earlier -\u003e audit-representation"` |
| `["status"]` | `"available"` |
| `["theory_map_ids"]` | `[]` |
| `["trace_ids"]` | `["T1"]` |
| `["unit"]` | `"comparison"` |
| `["value"]["collision_groups"]` | `[]` |
| `["value"]["compatibility_method"]` | `"identical_declared_basis"` |
| `["value"]["earlier_representation"]["binning_or_mapping_rule"]` | `"literal_field_value"` |
| `["value"]["earlier_representation"]["field_name"]` | `"topic"` |
| `["value"]["earlier_representation"]["missing_state_id"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["value"]["earlier_representation"]["missing_value_policy"]` | `"error"` |
| `["value"]["earlier_representation"]["normalization_profile"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["value"]["earlier_representation"]["representation_name"]` | `"topic"` |
| `["value"]["earlier_representation"]["representation_source"]` | `"topic_field"` |
| `["value"]["earlier_representation"]["representation_version"]` | `"hero-topic-v1"` |
| `["value"]["earlier_state_semantics"]` | `"Hero topic labels retain their literal meaning across v1 and v2."` |
| `["value"]["earlier_version"]` | `"v1"` |
| `["value"]["harmonized_earlier_support"]` | `["battery", "bird", "cat", "dog", "fish", "lizard", "refund", "turtle"]` |
| `["value"]["harmonized_later_support"]` | `["bird", "cat", "dog", "fish", "refund"]` |
| `["value"]["harmonized_representation"]["binning_or_mapping_rule"]` | `"literal_field_value"` |
| `["value"]["harmonized_representation"]["field_name"]` | `"topic"` |
| `["value"]["harmonized_representation"]["missing_state_id"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["value"]["harmonized_representation"]["missing_value_policy"]` | `"error"` |
| `["value"]["harmonized_representation"]["normalization_profile"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["value"]["harmonized_representation"]["representation_name"]` | `"topic"` |
| `["value"]["harmonized_representation"]["representation_source"]` | `"topic_field"` |
| `["value"]["harmonized_representation"]["representation_version"]` | `"hero-topic-v1"` |
| `["value"]["harmonized_state_semantics"]` | `"Hero topic labels retain their literal meaning across v1 and v2."` |
| `["value"]["later_representation"]["binning_or_mapping_rule"]` | `"literal_field_value"` |
| `["value"]["later_representation"]["field_name"]` | `"topic"` |
| `["value"]["later_representation"]["missing_state_id"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["value"]["later_representation"]["missing_value_policy"]` | `"error"` |
| `["value"]["later_representation"]["normalization_profile"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["value"]["later_representation"]["representation_name"]` | `"topic"` |
| `["value"]["later_representation"]["representation_source"]` | `"topic_field"` |
| `["value"]["later_representation"]["representation_version"]` | `"hero-topic-v1"` |
| `["value"]["later_state_semantics"]` | `"Hero topic labels retain their literal meaning across v1 and v2."` |
| `["value"]["later_version"]` | `"v2"` |
| `["value"]["original_earlier_support"]` | `["battery", "bird", "cat", "dog", "fish", "lizard", "refund", "turtle"]` |
| `["value"]["original_later_support"]` | `["bird", "cat", "dog", "fish", "refund"]` |
| `["value"]["retention_denominator"]` | 8 |
| `["value"]["retention_denominator_basis"]` | `"earlier_positive_mass_support_in_harmonized_representation"` |
| `["value"]["state_mapping"]` | `[]` |
| `["value"]["version_order"]` | `["v1", "v2"]` |
| `["value"]["version_order_source"]` | `"explicit_version_order"` |

**`["assumptions"]`**

- `"Earlier and later scopes explicitly selected and independently validated."`
- `"State identity uses the declared common basis, including any disclosed map."`

**`["limitations"]`**

- `"One explicitly selected earlier/later pair only; no trajectory or automatic adjacent comparison."`
- `"Extinct means absent from the supplied later support in the harmonized representation."`
- `"No permanent process extinction, causality, model-performance or source-independence claim follows."`
- `"Supplied probability vectors remain mathematical inputs, not empirical record-frequency observations."`
- `"Many-to-one mapping can conceal original distinctions; original inputs remain separately visible."`
- `"Weighted support is positive weight mass, not unweighted record presence."`
- `"State meaning is declared, not independently inferred or verified."`
- `"Many-to-one mapping can hide original distinctions; original bases remain separately visible."`
- `"Chronology alone does not establish lineage, causality or functional failure."`

**`["scope"]["included_record_keys"]`**

| `"dataset_version"` | `"record_id"` |
|---|---|
| `"v1"` | `"v1_01"` |
| `"v1"` | `"v1_02"` |
| `"v1"` | `"v1_03"` |
| `"v1"` | `"v1_04"` |
| `"v1"` | `"v1_05"` |
| `"v1"` | `"v1_06"` |
| `"v1"` | `"v1_07"` |
| `"v1"` | `"v1_08"` |
| `"v2"` | `"v2_01"` |
| `"v2"` | `"v2_02"` |
| `"v2"` | `"v2_03"` |
| `"v2"` | `"v2_04"` |
| `"v2"` | `"v2_05"` |
| `"v2"` | `"v2_06"` |
| `"v2"` | `"v2_07"` |
| `"v2"` | `"v2_08"` |

**`["value"]["mapping_effect"]`**

| `"dataset_version"` | `"harmonized_support_size"` | `"original_support_size"` |
|---|---|---|
| `"v1"` | 8 | 8 |
| `"v2"` | 5 | 5 |

### Analytical result

`["derived_metrics"]["support"]["extinct_states"]`

Status: `"available"`; evidence class: `"derived_metric"`; unit: `"set_of_states"`; method: `"T1.earlier_minus_later"`.

Denominator: 8; coverage (ratio): Unavailable (null): `"coverage_not_supplied_for_this_result"`.

| Field | Value |
|---|---|
| `["coverage"]` | Unavailable (null): `"coverage_not_supplied_for_this_result"` |
| `["coverage_reason"]` | `"coverage_not_supplied_for_this_result"` |
| `["denominator"]` | 8 |
| `["denominator_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["evidence_class"]` | `"derived_metric"` |
| `["input_basis"]` | `"empirical_assignments"` |
| `["method"]` | `"earlier support minus later support"` |
| `["method_id"]` | `"T1.earlier_minus_later"` |
| `["owner_ids"]` | `["T1"]` |
| `["reason_codes"]` | `[]` |
| `["representation"]["binning_or_mapping_rule"]` | `"literal_field_value"` |
| `["representation"]["field_name"]` | `"topic"` |
| `["representation"]["missing_state_id"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["missing_value_policy"]` | `"error"` |
| `["representation"]["normalization_profile"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["representation_name"]` | `"topic"` |
| `["representation"]["representation_source"]` | `"topic_field"` |
| `["representation"]["representation_version"]` | `"hero-topic-v1"` |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["v1", "v2"]` |
| `["scope"]["denominator_basis"]` | `"separate_ordered_representation_scopes"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 16 |
| `["scope"]["scope_id"]` | `"audit-representation-earlier -\u003e audit-representation"` |
| `["status"]` | `"available"` |
| `["theory_map_ids"]` | `[]` |
| `["trace_ids"]` | `["T1"]` |
| `["unit"]` | `"set_of_states"` |
| `["value"]` | `["battery", "lizard", "turtle"]` |
| `["weighting"]["weight_field"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["weighting"]["weighting_mode"]` | `"unweighted"` |

**`["assumptions"]`**

- `"Earlier and later scopes explicitly selected and independently validated."`
- `"State identity uses the declared common basis, including any disclosed map."`

**`["limitations"]`**

- `"Observed/supplied support only; no permanent extinction or causal/model-performance verdict."`
- `"A coarsened comparison cannot recover distinctions lost through its mapping."`
- `"One explicitly selected earlier/later pair only; no trajectory or automatic adjacent comparison."`
- `"Extinct means absent from the supplied later support in the harmonized representation."`
- `"No permanent process extinction, causality, model-performance or source-independence claim follows."`
- `"Supplied probability vectors remain mathematical inputs, not empirical record-frequency observations."`
- `"Many-to-one mapping can conceal original distinctions; original inputs remain separately visible."`
- `"Weighted support is positive weight mass, not unweighted record presence."`

**`["scope"]["included_record_keys"]`**

| `"dataset_version"` | `"record_id"` |
|---|---|
| `"v1"` | `"v1_01"` |
| `"v1"` | `"v1_02"` |
| `"v1"` | `"v1_03"` |
| `"v1"` | `"v1_04"` |
| `"v1"` | `"v1_05"` |
| `"v1"` | `"v1_06"` |
| `"v1"` | `"v1_07"` |
| `"v1"` | `"v1_08"` |
| `"v2"` | `"v2_01"` |
| `"v2"` | `"v2_02"` |
| `"v2"` | `"v2_03"` |
| `"v2"` | `"v2_04"` |
| `"v2"` | `"v2_05"` |
| `"v2"` | `"v2_06"` |
| `"v2"` | `"v2_07"` |
| `"v2"` | `"v2_08"` |

### Analytical result

`["derived_metrics"]["support"]["retained_states"]`

Status: `"available"`; evidence class: `"derived_metric"`; unit: `"set_of_states"`; method: `"T1.support_intersection"`.

Denominator: 8; coverage (ratio): Unavailable (null): `"coverage_not_supplied_for_this_result"`.

| Field | Value |
|---|---|
| `["coverage"]` | Unavailable (null): `"coverage_not_supplied_for_this_result"` |
| `["coverage_reason"]` | `"coverage_not_supplied_for_this_result"` |
| `["denominator"]` | 8 |
| `["denominator_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["evidence_class"]` | `"derived_metric"` |
| `["input_basis"]` | `"empirical_assignments"` |
| `["method"]` | `"earlier support intersect later support"` |
| `["method_id"]` | `"T1.support_intersection"` |
| `["owner_ids"]` | `["T1"]` |
| `["reason_codes"]` | `[]` |
| `["representation"]["binning_or_mapping_rule"]` | `"literal_field_value"` |
| `["representation"]["field_name"]` | `"topic"` |
| `["representation"]["missing_state_id"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["missing_value_policy"]` | `"error"` |
| `["representation"]["normalization_profile"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["representation_name"]` | `"topic"` |
| `["representation"]["representation_source"]` | `"topic_field"` |
| `["representation"]["representation_version"]` | `"hero-topic-v1"` |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["v1", "v2"]` |
| `["scope"]["denominator_basis"]` | `"separate_ordered_representation_scopes"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 16 |
| `["scope"]["scope_id"]` | `"audit-representation-earlier -\u003e audit-representation"` |
| `["status"]` | `"available"` |
| `["theory_map_ids"]` | `[]` |
| `["trace_ids"]` | `["T1"]` |
| `["unit"]` | `"set_of_states"` |
| `["value"]` | `["bird", "cat", "dog", "fish", "refund"]` |
| `["weighting"]["weight_field"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["weighting"]["weighting_mode"]` | `"unweighted"` |

**`["assumptions"]`**

- `"Earlier and later scopes explicitly selected and independently validated."`
- `"State identity uses the declared common basis, including any disclosed map."`

**`["limitations"]`**

- `"Observed/supplied support only; no permanent extinction or causal/model-performance verdict."`
- `"A coarsened comparison cannot recover distinctions lost through its mapping."`
- `"One explicitly selected earlier/later pair only; no trajectory or automatic adjacent comparison."`
- `"Extinct means absent from the supplied later support in the harmonized representation."`
- `"No permanent process extinction, causality, model-performance or source-independence claim follows."`
- `"Supplied probability vectors remain mathematical inputs, not empirical record-frequency observations."`
- `"Many-to-one mapping can conceal original distinctions; original inputs remain separately visible."`
- `"Weighted support is positive weight mass, not unweighted record presence."`

**`["scope"]["included_record_keys"]`**

| `"dataset_version"` | `"record_id"` |
|---|---|
| `"v1"` | `"v1_01"` |
| `"v1"` | `"v1_02"` |
| `"v1"` | `"v1_03"` |
| `"v1"` | `"v1_04"` |
| `"v1"` | `"v1_05"` |
| `"v1"` | `"v1_06"` |
| `"v1"` | `"v1_07"` |
| `"v1"` | `"v1_08"` |
| `"v2"` | `"v2_01"` |
| `"v2"` | `"v2_02"` |
| `"v2"` | `"v2_03"` |
| `"v2"` | `"v2_04"` |
| `"v2"` | `"v2_05"` |
| `"v2"` | `"v2_06"` |
| `"v2"` | `"v2_07"` |
| `"v2"` | `"v2_08"` |

### Analytical result

`["derived_metrics"]["support"]["support_added_count"]`

Status: `"available"`; evidence class: `"derived_metric"`; unit: `"states"`; method: `"T1.support_set_difference"`.

Value: 0.

Denominator: 8; coverage (ratio): Unavailable (null): `"coverage_not_supplied_for_this_result"`.

| Field | Value |
|---|---|
| `["coverage"]` | Unavailable (null): `"coverage_not_supplied_for_this_result"` |
| `["coverage_reason"]` | `"coverage_not_supplied_for_this_result"` |
| `["denominator"]` | 8 |
| `["denominator_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["evidence_class"]` | `"derived_metric"` |
| `["input_basis"]` | `"empirical_assignments"` |
| `["method"]` | `"cardinality of later support minus earlier support"` |
| `["method_id"]` | `"T1.support_set_difference"` |
| `["owner_ids"]` | `["T1"]` |
| `["reason_codes"]` | `[]` |
| `["representation"]["binning_or_mapping_rule"]` | `"literal_field_value"` |
| `["representation"]["field_name"]` | `"topic"` |
| `["representation"]["missing_state_id"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["missing_value_policy"]` | `"error"` |
| `["representation"]["normalization_profile"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["representation_name"]` | `"topic"` |
| `["representation"]["representation_source"]` | `"topic_field"` |
| `["representation"]["representation_version"]` | `"hero-topic-v1"` |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["v1", "v2"]` |
| `["scope"]["denominator_basis"]` | `"separate_ordered_representation_scopes"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 16 |
| `["scope"]["scope_id"]` | `"audit-representation-earlier -\u003e audit-representation"` |
| `["status"]` | `"available"` |
| `["theory_map_ids"]` | `[]` |
| `["trace_ids"]` | `["T1"]` |
| `["unit"]` | `"states"` |
| `["value"]` | 0 |
| `["weighting"]["weight_field"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["weighting"]["weighting_mode"]` | `"unweighted"` |

**`["assumptions"]`**

- `"Earlier and later scopes explicitly selected and independently validated."`
- `"State identity uses the declared common basis, including any disclosed map."`

**`["limitations"]`**

- `"Observed/supplied support only; no permanent extinction or causal/model-performance verdict."`
- `"A coarsened comparison cannot recover distinctions lost through its mapping."`
- `"One explicitly selected earlier/later pair only; no trajectory or automatic adjacent comparison."`
- `"Extinct means absent from the supplied later support in the harmonized representation."`
- `"No permanent process extinction, causality, model-performance or source-independence claim follows."`
- `"Supplied probability vectors remain mathematical inputs, not empirical record-frequency observations."`
- `"Many-to-one mapping can conceal original distinctions; original inputs remain separately visible."`
- `"Weighted support is positive weight mass, not unweighted record presence."`

**`["scope"]["included_record_keys"]`**

| `"dataset_version"` | `"record_id"` |
|---|---|
| `"v1"` | `"v1_01"` |
| `"v1"` | `"v1_02"` |
| `"v1"` | `"v1_03"` |
| `"v1"` | `"v1_04"` |
| `"v1"` | `"v1_05"` |
| `"v1"` | `"v1_06"` |
| `"v1"` | `"v1_07"` |
| `"v1"` | `"v1_08"` |
| `"v2"` | `"v2_01"` |
| `"v2"` | `"v2_02"` |
| `"v2"` | `"v2_03"` |
| `"v2"` | `"v2_04"` |
| `"v2"` | `"v2_05"` |
| `"v2"` | `"v2_06"` |
| `"v2"` | `"v2_07"` |
| `"v2"` | `"v2_08"` |

### Analytical result

`["derived_metrics"]["support"]["support_delta"]`

Status: `"available"`; evidence class: `"derived_metric"`; unit: `"states"`; method: `"F-005"`.

Value: -3.

Denominator: 8; coverage (ratio): Unavailable (null): `"coverage_not_supplied_for_this_result"`.

| Field | Value |
|---|---|
| `["coverage"]` | Unavailable (null): `"coverage_not_supplied_for_this_result"` |
| `["coverage_reason"]` | `"coverage_not_supplied_for_this_result"` |
| `["denominator"]` | 8 |
| `["denominator_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["evidence_class"]` | `"derived_metric"` |
| `["input_basis"]` | `"empirical_assignments"` |
| `["method"]` | `"later support_size minus earlier support_size"` |
| `["method_id"]` | `"F-005"` |
| `["owner_ids"]` | `["T1"]` |
| `["reason_codes"]` | `[]` |
| `["representation"]["binning_or_mapping_rule"]` | `"literal_field_value"` |
| `["representation"]["field_name"]` | `"topic"` |
| `["representation"]["missing_state_id"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["missing_value_policy"]` | `"error"` |
| `["representation"]["normalization_profile"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["representation_name"]` | `"topic"` |
| `["representation"]["representation_source"]` | `"topic_field"` |
| `["representation"]["representation_version"]` | `"hero-topic-v1"` |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["v1", "v2"]` |
| `["scope"]["denominator_basis"]` | `"separate_ordered_representation_scopes"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 16 |
| `["scope"]["scope_id"]` | `"audit-representation-earlier -\u003e audit-representation"` |
| `["status"]` | `"available"` |
| `["theory_map_ids"]` | `[]` |
| `["trace_ids"]` | `["T1"]` |
| `["unit"]` | `"states"` |
| `["value"]` | -3 |
| `["weighting"]["weight_field"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["weighting"]["weighting_mode"]` | `"unweighted"` |

**`["assumptions"]`**

- `"Earlier and later scopes explicitly selected and independently validated."`
- `"State identity uses the declared common basis, including any disclosed map."`

**`["limitations"]`**

- `"Observed/supplied support only; no permanent extinction or causal/model-performance verdict."`
- `"A coarsened comparison cannot recover distinctions lost through its mapping."`
- `"One explicitly selected earlier/later pair only; no trajectory or automatic adjacent comparison."`
- `"Extinct means absent from the supplied later support in the harmonized representation."`
- `"No permanent process extinction, causality, model-performance or source-independence claim follows."`
- `"Supplied probability vectors remain mathematical inputs, not empirical record-frequency observations."`
- `"Many-to-one mapping can conceal original distinctions; original inputs remain separately visible."`
- `"Weighted support is positive weight mass, not unweighted record presence."`

**`["scope"]["included_record_keys"]`**

| `"dataset_version"` | `"record_id"` |
|---|---|
| `"v1"` | `"v1_01"` |
| `"v1"` | `"v1_02"` |
| `"v1"` | `"v1_03"` |
| `"v1"` | `"v1_04"` |
| `"v1"` | `"v1_05"` |
| `"v1"` | `"v1_06"` |
| `"v1"` | `"v1_07"` |
| `"v1"` | `"v1_08"` |
| `"v2"` | `"v2_01"` |
| `"v2"` | `"v2_02"` |
| `"v2"` | `"v2_03"` |
| `"v2"` | `"v2_04"` |
| `"v2"` | `"v2_05"` |
| `"v2"` | `"v2_06"` |
| `"v2"` | `"v2_07"` |
| `"v2"` | `"v2_08"` |

### Analytical result

`["derived_metrics"]["support"]["support_loss_count"]`

Status: `"available"`; evidence class: `"derived_metric"`; unit: `"states"`; method: `"T1.support_set_difference"`.

Value: 3.

Denominator: 8; coverage (ratio): Unavailable (null): `"coverage_not_supplied_for_this_result"`.

| Field | Value |
|---|---|
| `["coverage"]` | Unavailable (null): `"coverage_not_supplied_for_this_result"` |
| `["coverage_reason"]` | `"coverage_not_supplied_for_this_result"` |
| `["denominator"]` | 8 |
| `["denominator_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["evidence_class"]` | `"derived_metric"` |
| `["input_basis"]` | `"empirical_assignments"` |
| `["method"]` | `"cardinality of earlier support minus later support"` |
| `["method_id"]` | `"T1.support_set_difference"` |
| `["owner_ids"]` | `["T1"]` |
| `["reason_codes"]` | `[]` |
| `["representation"]["binning_or_mapping_rule"]` | `"literal_field_value"` |
| `["representation"]["field_name"]` | `"topic"` |
| `["representation"]["missing_state_id"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["missing_value_policy"]` | `"error"` |
| `["representation"]["normalization_profile"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["representation_name"]` | `"topic"` |
| `["representation"]["representation_source"]` | `"topic_field"` |
| `["representation"]["representation_version"]` | `"hero-topic-v1"` |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["v1", "v2"]` |
| `["scope"]["denominator_basis"]` | `"separate_ordered_representation_scopes"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 16 |
| `["scope"]["scope_id"]` | `"audit-representation-earlier -\u003e audit-representation"` |
| `["status"]` | `"available"` |
| `["theory_map_ids"]` | `[]` |
| `["trace_ids"]` | `["T1"]` |
| `["unit"]` | `"states"` |
| `["value"]` | 3 |
| `["weighting"]["weight_field"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["weighting"]["weighting_mode"]` | `"unweighted"` |

**`["assumptions"]`**

- `"Earlier and later scopes explicitly selected and independently validated."`
- `"State identity uses the declared common basis, including any disclosed map."`

**`["limitations"]`**

- `"Observed/supplied support only; no permanent extinction or causal/model-performance verdict."`
- `"A coarsened comparison cannot recover distinctions lost through its mapping."`
- `"One explicitly selected earlier/later pair only; no trajectory or automatic adjacent comparison."`
- `"Extinct means absent from the supplied later support in the harmonized representation."`
- `"No permanent process extinction, causality, model-performance or source-independence claim follows."`
- `"Supplied probability vectors remain mathematical inputs, not empirical record-frequency observations."`
- `"Many-to-one mapping can conceal original distinctions; original inputs remain separately visible."`
- `"Weighted support is positive weight mass, not unweighted record presence."`

**`["scope"]["included_record_keys"]`**

| `"dataset_version"` | `"record_id"` |
|---|---|
| `"v1"` | `"v1_01"` |
| `"v1"` | `"v1_02"` |
| `"v1"` | `"v1_03"` |
| `"v1"` | `"v1_04"` |
| `"v1"` | `"v1_05"` |
| `"v1"` | `"v1_06"` |
| `"v1"` | `"v1_07"` |
| `"v1"` | `"v1_08"` |
| `"v2"` | `"v2_01"` |
| `"v2"` | `"v2_02"` |
| `"v2"` | `"v2_03"` |
| `"v2"` | `"v2_04"` |
| `"v2"` | `"v2_05"` |
| `"v2"` | `"v2_06"` |
| `"v2"` | `"v2_07"` |
| `"v2"` | `"v2_08"` |

### Analytical result

`["derived_metrics"]["support"]["support_retention_ratio"]`

Status: `"available"`; evidence class: `"derived_metric"`; unit: `"ratio"`; method: `"F-006"`.

Value: 0.625.

Denominator: 8; coverage (ratio): Unavailable (null): `"coverage_not_supplied_for_this_result"`.

| Field | Value |
|---|---|
| `["coverage"]` | Unavailable (null): `"coverage_not_supplied_for_this_result"` |
| `["coverage_reason"]` | `"coverage_not_supplied_for_this_result"` |
| `["denominator"]` | 8 |
| `["denominator_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["evidence_class"]` | `"derived_metric"` |
| `["input_basis"]` | `"empirical_assignments"` |
| `["method"]` | `"intersection support size / earlier positive-mass support size"` |
| `["method_id"]` | `"F-006"` |
| `["owner_ids"]` | `["T1"]` |
| `["reason_codes"]` | `[]` |
| `["representation"]["binning_or_mapping_rule"]` | `"literal_field_value"` |
| `["representation"]["field_name"]` | `"topic"` |
| `["representation"]["missing_state_id"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["missing_value_policy"]` | `"error"` |
| `["representation"]["normalization_profile"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["representation_name"]` | `"topic"` |
| `["representation"]["representation_source"]` | `"topic_field"` |
| `["representation"]["representation_version"]` | `"hero-topic-v1"` |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["v1", "v2"]` |
| `["scope"]["denominator_basis"]` | `"separate_ordered_representation_scopes"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 16 |
| `["scope"]["scope_id"]` | `"audit-representation-earlier -\u003e audit-representation"` |
| `["status"]` | `"available"` |
| `["theory_map_ids"]` | `[]` |
| `["trace_ids"]` | `["T1"]` |
| `["unit"]` | `"ratio"` |
| `["value"]` | 0.625 |
| `["weighting"]["weight_field"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["weighting"]["weighting_mode"]` | `"unweighted"` |

**`["assumptions"]`**

- `"Earlier and later scopes explicitly selected and independently validated."`
- `"State identity uses the declared common basis, including any disclosed map."`

**`["limitations"]`**

- `"Observed/supplied support only; no permanent extinction or causal/model-performance verdict."`
- `"A coarsened comparison cannot recover distinctions lost through its mapping."`
- `"One explicitly selected earlier/later pair only; no trajectory or automatic adjacent comparison."`
- `"Extinct means absent from the supplied later support in the harmonized representation."`
- `"No permanent process extinction, causality, model-performance or source-independence claim follows."`
- `"Supplied probability vectors remain mathematical inputs, not empirical record-frequency observations."`
- `"Many-to-one mapping can conceal original distinctions; original inputs remain separately visible."`
- `"Weighted support is positive weight mass, not unweighted record presence."`

**`["scope"]["included_record_keys"]`**

| `"dataset_version"` | `"record_id"` |
|---|---|
| `"v1"` | `"v1_01"` |
| `"v1"` | `"v1_02"` |
| `"v1"` | `"v1_03"` |
| `"v1"` | `"v1_04"` |
| `"v1"` | `"v1_05"` |
| `"v1"` | `"v1_06"` |
| `"v1"` | `"v1_07"` |
| `"v1"` | `"v1_08"` |
| `"v2"` | `"v2_01"` |
| `"v2"` | `"v2_02"` |
| `"v2"` | `"v2_03"` |
| `"v2"` | `"v2_04"` |
| `"v2"` | `"v2_05"` |
| `"v2"` | `"v2_06"` |
| `"v2"` | `"v2_07"` |
| `"v2"` | `"v2_08"` |

## Proxy signals

### Analytical result

`["proxy_signals"]["provenance_uncertainty"]`

Status: `"available"`; evidence class: `"proxy_signal"`; unit: `"signal"`; method: `"T3.provenance_uncertainty"`.

Denominator: 8; coverage (ratio): 1.0.

| Field | Value |
|---|---|
| `["basis_fields"]` | `["derived_metrics.closure_exposure.direct.interval_width", "observed_facts.provenance.provenance_row_coverage", "observed_facts.provenance.provenance_required_field_coverage", "observed_facts.provenance.grounding_field_coverage"]` |
| `["coverage"]` | 1.0 |
| `["coverage_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["denominator"]` | 8 |
| `["denominator_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["evidence_class"]` | `"proxy_signal"` |
| `["level"]` | `"not_present"` |
| `["method_id"]` | `"T3.provenance_uncertainty"` |
| `["owner_ids"]` | `["T3"]` |
| `["reason_codes"]` | `[]` |
| `["representation"]` | Unavailable (null): No applicable representation supplied; consult status and required evidence. |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["v2"]` |
| `["scope"]["denominator_basis"]` | `"all_valid_records_in_selected_dataset_scope"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"audit-provenance"` |
| `["signal"]` | `"provenance_uncertainty"` |
| `["status"]` | `"available"` |
| `["theory_map_ids"]` | `[]` |
| `["trace_ids"]` | `["T3"]` |
| `["trigger_rule"]` | `"Present when a supplied direct closure interval has positive width or a supplied provenance row, required-field or grounding coverage is below one."` |
| `["unit"]` | `"signal"` |

**`["assumptions"]`**

- `"Approved direct grounding partition; uncertainty remains unresolved."`

**`["limitations"]`**

- `"Toolkit operationalization relative to supplied metadata, without lineage or truth certification."`
- `"Direct exposure is relative to the audited loop and supplied metadata."`
- `"Toolkit operationalization; metadata can be incorrect and hidden dependencies unobserved."`
- `"Confidence remains separate; no lineage, midpoint, threshold or causal claim."`
- `"Each coverage keeps its own field meaning and denominator."`
- `"This signal reports unresolved supplied provenance evidence and does not estimate factual truth or source independence."`
- `"A not_present signal is limited to the cited fields and does not certify universal integrity."`

**`["scope"]["included_record_keys"]`**

| `"dataset_version"` | `"record_id"` |
|---|---|
| `"v2"` | `"v2_01"` |
| `"v2"` | `"v2_02"` |
| `"v2"` | `"v2_03"` |
| `"v2"` | `"v2_04"` |
| `"v2"` | `"v2_05"` |
| `"v2"` | `"v2_06"` |
| `"v2"` | `"v2_07"` |
| `"v2"` | `"v2_08"` |

### Analytical result

`["proxy_signals"]["support_contraction"]`

Status: `"available"`; evidence class: `"proxy_signal"`; unit: `"signal"`; method: `"T1.support_contraction"`.

Denominator: 8; coverage (ratio): Unavailable (null): `"coverage_not_supplied_for_this_result"`.

| Field | Value |
|---|---|
| `["basis_fields"]` | `["derived_metrics.support.support_delta", "derived_metrics.support.extinct_states", "derived_metrics.support.comparison_details"]` |
| `["coverage"]` | Unavailable (null): `"coverage_not_supplied_for_this_result"` |
| `["coverage_reason"]` | `"coverage_not_supplied_for_this_result"` |
| `["denominator"]` | 8 |
| `["denominator_reason"]` | Unavailable (null): No null reason is required when the associated value is supplied. |
| `["evidence_class"]` | `"proxy_signal"` |
| `["level"]` | `"present"` |
| `["method_id"]` | `"T1.support_contraction"` |
| `["owner_ids"]` | `["T1"]` |
| `["reason_codes"]` | `[]` |
| `["representation"]["binning_or_mapping_rule"]` | `"literal_field_value"` |
| `["representation"]["field_name"]` | `"topic"` |
| `["representation"]["missing_state_id"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["missing_value_policy"]` | `"error"` |
| `["representation"]["normalization_profile"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["representation_name"]` | `"topic"` |
| `["representation"]["representation_source"]` | `"topic_field"` |
| `["representation"]["representation_version"]` | `"hero-topic-v1"` |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["v1", "v2"]` |
| `["scope"]["denominator_basis"]` | `"separate_ordered_representation_scopes"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 16 |
| `["scope"]["scope_id"]` | `"audit-representation-earlier -\u003e audit-representation"` |
| `["signal"]` | `"support_contraction"` |
| `["status"]` | `"available"` |
| `["theory_map_ids"]` | `[]` |
| `["trace_ids"]` | `["T1"]` |
| `["trigger_rule"]` | `"Present exactly when the supplied validated explicit-pair support delta is negative."` |
| `["unit"]` | `"signal"` |

**`["assumptions"]`**

- `"Earlier and later scopes explicitly selected and independently validated."`
- `"State identity uses the declared common basis, including any disclosed map."`

**`["limitations"]`**

- `"Observed/supplied support only; no permanent extinction or causal/model-performance verdict."`
- `"A coarsened comparison cannot recover distinctions lost through its mapping."`
- `"One explicitly selected earlier/later pair only; no trajectory or automatic adjacent comparison."`
- `"Extinct means absent from the supplied later support in the harmonized representation."`
- `"No permanent process extinction, causality, model-performance or source-independence claim follows."`
- `"Supplied probability vectors remain mathematical inputs, not empirical record-frequency observations."`
- `"Many-to-one mapping can conceal original distinctions; original inputs remain separately visible."`
- `"Weighted support is positive weight mass, not unweighted record presence."`
- `"The signal is restricted to the selected versions and their declared common state meaning."`
- `"An observed support decrease does not establish model-performance decline, production failure or universal collapse."`

**`["scope"]["included_record_keys"]`**

| `"dataset_version"` | `"record_id"` |
|---|---|
| `"v1"` | `"v1_01"` |
| `"v1"` | `"v1_02"` |
| `"v1"` | `"v1_03"` |
| `"v1"` | `"v1_04"` |
| `"v1"` | `"v1_05"` |
| `"v1"` | `"v1_06"` |
| `"v1"` | `"v1_07"` |
| `"v1"` | `"v1_08"` |
| `"v2"` | `"v2_01"` |
| `"v2"` | `"v2_02"` |
| `"v2"` | `"v2_03"` |
| `"v2"` | `"v2_04"` |
| `"v2"` | `"v2_05"` |
| `"v2"` | `"v2_06"` |
| `"v2"` | `"v2_07"` |
| `"v2"` | `"v2_08"` |

## Simulations

`["simulations"]`

| Field | Value |
|---|---|
| Value | `{}` |

## Unavailable conclusions

### Analytical result

`["unavailable_conclusions"][0]`

Status: `"unavailable"`; evidence class: `"unavailable_conclusion"`; unit: `"conclusion"`; method: `"PR-014.unavailable_conclusion"`.

Denominator: Unavailable (null): `"This conclusion has no scalar denominator."`; coverage (ratio): Unavailable (null): `"This conclusion has no measured evidence coverage."`.

| Field | Value |
|---|---|
| `["assumptions"]` | `[]` |
| `["blocking_evidence"]` | `["No accepted versioned model-outcome analysis is supplied."]` |
| `["conclusion"]` | `"model_performance_decline"` |
| `["coverage"]` | Unavailable (null): `"This conclusion has no measured evidence coverage."` |
| `["coverage_reason"]` | `"This conclusion has no measured evidence coverage."` |
| `["denominator"]` | Unavailable (null): `"This conclusion has no scalar denominator."` |
| `["denominator_reason"]` | `"This conclusion has no scalar denominator."` |
| `["evidence_class"]` | `"unavailable_conclusion"` |
| `["method_id"]` | `"PR-014.unavailable_conclusion"` |
| `["owner_ids"]` | `["PR-014"]` |
| `["reason_codes"]` | `["R_MODEL_EVIDENCE_MISSING"]` |
| `["related_capability"]` | `"model_longitudinal"` |
| `["representation"]` | Unavailable (null): No applicable representation supplied; consult status and required evidence. |
| `["required_evidence"]` | `["Versioned model evaluation outcomes with comparable tasks and evaluation conditions."]` |
| `["required_next_metadata"]` | `["Versioned model evaluation outcomes with comparable tasks and evaluation conditions."]` |
| `["scope"]["dataset_versions"]` | `["v1", "v2"]` |
| `["scope"]["denominator_basis"]` | `"all_validated_bundle_records"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 16 |
| `["scope"]["scope_id"]` | `"validated_bundle"` |
| `["statement"]` | `"The supplied audit evidence cannot establish model-performance decline."` |
| `["status"]` | `"unavailable"` |
| `["theory_map_ids"]` | `[]` |
| `["theory_or_product_limit"]` | `"Dataset structure does not measure model performance."` |
| `["trace_ids"]` | `[]` |
| `["unit"]` | `"conclusion"` |

**`["limitations"]`**

- `"Unavailable means the supplied evidence does not support this conclusion; it does not establish that the conclusion is false."`

**`["scope"]["included_record_keys"]`**

| `"dataset_version"` | `"record_id"` |
|---|---|
| `"v1"` | `"v1_01"` |
| `"v1"` | `"v1_02"` |
| `"v1"` | `"v1_03"` |
| `"v1"` | `"v1_04"` |
| `"v1"` | `"v1_05"` |
| `"v1"` | `"v1_06"` |
| `"v1"` | `"v1_07"` |
| `"v1"` | `"v1_08"` |
| `"v2"` | `"v2_01"` |
| `"v2"` | `"v2_02"` |
| `"v2"` | `"v2_03"` |
| `"v2"` | `"v2_04"` |
| `"v2"` | `"v2_05"` |
| `"v2"` | `"v2_06"` |
| `"v2"` | `"v2_07"` |
| `"v2"` | `"v2_08"` |

### Analytical result

`["unavailable_conclusions"][1]`

Status: `"unavailable"`; evidence class: `"unavailable_conclusion"`; unit: `"conclusion"`; method: `"T4.unavailable_conclusion"`.

Denominator: Unavailable (null): `"This conclusion has no scalar denominator."`; coverage (ratio): Unavailable (null): `"This conclusion has no measured evidence coverage."`.

| Field | Value |
|---|---|
| `["assumptions"]` | `[]` |
| `["blocking_evidence"]` | `["Phase 4 does not compute ancestry; topology alone would not identify a causal contribution."]` |
| `["conclusion"]` | `"causal_ancestor_effect"` |
| `["coverage"]` | Unavailable (null): `"This conclusion has no measured evidence coverage."` |
| `["coverage_reason"]` | `"This conclusion has no measured evidence coverage."` |
| `["denominator"]` | Unavailable (null): `"This conclusion has no scalar denominator."` |
| `["denominator_reason"]` | `"This conclusion has no scalar denominator."` |
| `["evidence_class"]` | `"unavailable_conclusion"` |
| `["method_id"]` | `"T4.unavailable_conclusion"` |
| `["owner_ids"]` | `["T4"]` |
| `["reason_codes"]` | `["R_CAUSAL_EVIDENCE_MISSING", "R_LINEAGE_EXECUTION_DEFERRED"]` |
| `["related_capability"]` | `"lineage"` |
| `["representation"]` | Unavailable (null): No applicable representation supplied; consult status and required evidence. |
| `["required_evidence"]` | `["An identified ancestor, measured outcomes and a controlled or otherwise justified causal design."]` |
| `["required_next_metadata"]` | `["An identified ancestor, measured outcomes and a controlled or otherwise justified causal design."]` |
| `["scope"]["dataset_versions"]` | `["v1", "v2"]` |
| `["scope"]["denominator_basis"]` | `"all_validated_bundle_records"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 16 |
| `["scope"]["scope_id"]` | `"validated_bundle"` |
| `["statement"]` | `"A causal effect of an ancestor is unavailable."` |
| `["status"]` | `"unavailable"` |
| `["theory_map_ids"]` | `[]` |
| `["theory_or_product_limit"]` | `"Parent declarations and graph topology do not establish causal effects."` |
| `["trace_ids"]` | `["T4"]` |
| `["unit"]` | `"conclusion"` |

**`["limitations"]`**

- `"Unavailable means the supplied evidence does not support this conclusion; it does not establish that the conclusion is false."`

**`["scope"]["included_record_keys"]`**

| `"dataset_version"` | `"record_id"` |
|---|---|
| `"v1"` | `"v1_01"` |
| `"v1"` | `"v1_02"` |
| `"v1"` | `"v1_03"` |
| `"v1"` | `"v1_04"` |
| `"v1"` | `"v1_05"` |
| `"v1"` | `"v1_06"` |
| `"v1"` | `"v1_07"` |
| `"v1"` | `"v1_08"` |
| `"v2"` | `"v2_01"` |
| `"v2"` | `"v2_02"` |
| `"v2"` | `"v2_03"` |
| `"v2"` | `"v2_04"` |
| `"v2"` | `"v2_05"` |
| `"v2"` | `"v2_06"` |
| `"v2"` | `"v2_07"` |
| `"v2"` | `"v2_08"` |

### Analytical result

`["unavailable_conclusions"][2]`

Status: `"unavailable"`; evidence class: `"unavailable_conclusion"`; unit: `"conclusion"`; method: `"PR-014.unavailable_conclusion"`.

Denominator: Unavailable (null): `"This conclusion has no scalar denominator."`; coverage (ratio): Unavailable (null): `"This conclusion has no measured evidence coverage."`.

| Field | Value |
|---|---|
| `["assumptions"]` | `[]` |
| `["blocking_evidence"]` | `["This product defines no universal integrity scalar or operational test."]` |
| `["conclusion"]` | `"universal_integrity"` |
| `["coverage"]` | Unavailable (null): `"This conclusion has no measured evidence coverage."` |
| `["coverage_reason"]` | `"This conclusion has no measured evidence coverage."` |
| `["denominator"]` | Unavailable (null): `"This conclusion has no scalar denominator."` |
| `["denominator_reason"]` | `"This conclusion has no scalar denominator."` |
| `["evidence_class"]` | `"unavailable_conclusion"` |
| `["method_id"]` | `"PR-014.unavailable_conclusion"` |
| `["owner_ids"]` | `["PR-014"]` |
| `["reason_codes"]` | `["R_UNIVERSAL_OPERATIONAL_DEFINITION_ABSENT"]` |
| `["related_capability"]` | `"provenance"` |
| `["representation"]` | Unavailable (null): No applicable representation supplied; consult status and required evidence. |
| `["required_evidence"]` | `["A bounded operational definition and evidence matched to that definition."]` |
| `["required_next_metadata"]` | `["A bounded operational definition and evidence matched to that definition."]` |
| `["scope"]["dataset_versions"]` | `["v1", "v2"]` |
| `["scope"]["denominator_basis"]` | `"all_validated_bundle_records"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 16 |
| `["scope"]["scope_id"]` | `"validated_bundle"` |
| `["statement"]` | `"Universal integrity is unavailable."` |
| `["status"]` | `"unavailable"` |
| `["theory_map_ids"]` | `[]` |
| `["theory_or_product_limit"]` | `"A domain-specific future audit does not unlock a universal integrity claim."` |
| `["trace_ids"]` | `[]` |
| `["unit"]` | `"conclusion"` |

**`["limitations"]`**

- `"Unavailable means the supplied evidence does not support this conclusion; it does not establish that the conclusion is false."`

**`["scope"]["included_record_keys"]`**

| `"dataset_version"` | `"record_id"` |
|---|---|
| `"v1"` | `"v1_01"` |
| `"v1"` | `"v1_02"` |
| `"v1"` | `"v1_03"` |
| `"v1"` | `"v1_04"` |
| `"v1"` | `"v1_05"` |
| `"v1"` | `"v1_06"` |
| `"v1"` | `"v1_07"` |
| `"v1"` | `"v1_08"` |
| `"v2"` | `"v2_01"` |
| `"v2"` | `"v2_02"` |
| `"v2"` | `"v2_03"` |
| `"v2"` | `"v2_04"` |
| `"v2"` | `"v2_05"` |
| `"v2"` | `"v2_06"` |
| `"v2"` | `"v2_07"` |
| `"v2"` | `"v2_08"` |

### Analytical result

`["unavailable_conclusions"][3]`

Status: `"unavailable"`; evidence class: `"unavailable_conclusion"`; unit: `"conclusion"`; method: `"PR-014.unavailable_conclusion"`.

Denominator: Unavailable (null): `"This conclusion has no scalar denominator."`; coverage (ratio): Unavailable (null): `"This conclusion has no measured evidence coverage."`.

| Field | Value |
|---|---|
| `["assumptions"]` | `[]` |
| `["blocking_evidence"]` | `["No universal collapse prediction is defined by the approved toolkit."]` |
| `["conclusion"]` | `"universal_collapse_prediction"` |
| `["coverage"]` | Unavailable (null): `"This conclusion has no measured evidence coverage."` |
| `["coverage_reason"]` | `"This conclusion has no measured evidence coverage."` |
| `["denominator"]` | Unavailable (null): `"This conclusion has no scalar denominator."` |
| `["denominator_reason"]` | `"This conclusion has no scalar denominator."` |
| `["evidence_class"]` | `"unavailable_conclusion"` |
| `["method_id"]` | `"PR-014.unavailable_conclusion"` |
| `["owner_ids"]` | `["PR-014"]` |
| `["reason_codes"]` | `["R_OUTSIDE_PRODUCT_SCOPE"]` |
| `["related_capability"]` | `"model_longitudinal"` |
| `["representation"]` | Unavailable (null): No applicable representation supplied; consult status and required evidence. |
| `["required_evidence"]` | `["A separately defined bounded outcome and appropriately validated predictive evidence."]` |
| `["required_next_metadata"]` | `["A separately defined bounded outcome and appropriately validated predictive evidence."]` |
| `["scope"]["dataset_versions"]` | `["v1", "v2"]` |
| `["scope"]["denominator_basis"]` | `"all_validated_bundle_records"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 16 |
| `["scope"]["scope_id"]` | `"validated_bundle"` |
| `["statement"]` | `"Universal collapse prediction is unavailable."` |
| `["status"]` | `"unavailable"` |
| `["theory_map_ids"]` | `[]` |
| `["theory_or_product_limit"]` | `"No additional metadata by itself unlocks universal collapse prediction in this product."` |
| `["trace_ids"]` | `[]` |
| `["unit"]` | `"conclusion"` |

**`["limitations"]`**

- `"Unavailable means the supplied evidence does not support this conclusion; it does not establish that the conclusion is false."`

**`["scope"]["included_record_keys"]`**

| `"dataset_version"` | `"record_id"` |
|---|---|
| `"v1"` | `"v1_01"` |
| `"v1"` | `"v1_02"` |
| `"v1"` | `"v1_03"` |
| `"v1"` | `"v1_04"` |
| `"v1"` | `"v1_05"` |
| `"v1"` | `"v1_06"` |
| `"v1"` | `"v1_07"` |
| `"v1"` | `"v1_08"` |
| `"v2"` | `"v2_01"` |
| `"v2"` | `"v2_02"` |
| `"v2"` | `"v2_03"` |
| `"v2"` | `"v2_04"` |
| `"v2"` | `"v2_05"` |
| `"v2"` | `"v2_06"` |
| `"v2"` | `"v2_07"` |
| `"v2"` | `"v2_08"` |

### Analytical result

`["unavailable_conclusions"][4]`

Status: `"unavailable"`; evidence class: `"unavailable_conclusion"`; unit: `"conclusion"`; method: `"T1.unavailable_conclusion"`.

Denominator: Unavailable (null): `"This conclusion has no scalar denominator."`; coverage (ratio): Unavailable (null): `"This conclusion has no measured evidence coverage."`.

| Field | Value |
|---|---|
| `["assumptions"]` | `[]` |
| `["blocking_evidence"]` | `["No operational failure outcome is measured by these structural fields."]` |
| `["conclusion"]` | `"production_failure"` |
| `["coverage"]` | Unavailable (null): `"This conclusion has no measured evidence coverage."` |
| `["coverage_reason"]` | `"This conclusion has no measured evidence coverage."` |
| `["denominator"]` | Unavailable (null): `"This conclusion has no scalar denominator."` |
| `["denominator_reason"]` | `"This conclusion has no scalar denominator."` |
| `["evidence_class"]` | `"unavailable_conclusion"` |
| `["method_id"]` | `"T1.unavailable_conclusion"` |
| `["owner_ids"]` | `["T1"]` |
| `["reason_codes"]` | `["R_OUTCOME_EVIDENCE_MISSING"]` |
| `["related_capability"]` | `"content_diagnostics"` |
| `["representation"]` | Unavailable (null): No applicable representation supplied; consult status and required evidence. |
| `["required_evidence"]` | `["A stated production-failure criterion and corresponding versioned outcome measurements."]` |
| `["required_next_metadata"]` | `["A stated production-failure criterion and corresponding versioned outcome measurements."]` |
| `["scope"]["dataset_versions"]` | `["v1", "v2"]` |
| `["scope"]["denominator_basis"]` | `"all_validated_bundle_records"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 16 |
| `["scope"]["scope_id"]` | `"validated_bundle"` |
| `["statement"]` | `"The supplied structural measurements cannot establish production failure."` |
| `["status"]` | `"unavailable"` |
| `["theory_map_ids"]` | `[]` |
| `["theory_or_product_limit"]` | `"Represented support, diversity and tail membership do not measure functional failure."` |
| `["trace_ids"]` | `["T1"]` |
| `["unit"]` | `"conclusion"` |

**`["limitations"]`**

- `"Unavailable means the supplied evidence does not support this conclusion; it does not establish that the conclusion is false."`

**`["scope"]["included_record_keys"]`**

| `"dataset_version"` | `"record_id"` |
|---|---|
| `"v1"` | `"v1_01"` |
| `"v1"` | `"v1_02"` |
| `"v1"` | `"v1_03"` |
| `"v1"` | `"v1_04"` |
| `"v1"` | `"v1_05"` |
| `"v1"` | `"v1_06"` |
| `"v1"` | `"v1_07"` |
| `"v1"` | `"v1_08"` |
| `"v2"` | `"v2_01"` |
| `"v2"` | `"v2_02"` |
| `"v2"` | `"v2_03"` |
| `"v2"` | `"v2_04"` |
| `"v2"` | `"v2_05"` |
| `"v2"` | `"v2_06"` |
| `"v2"` | `"v2_07"` |
| `"v2"` | `"v2_08"` |

### Analytical result

`["unavailable_conclusions"][5]`

Status: `"unavailable"`; evidence class: `"unavailable_conclusion"`; unit: `"conclusion"`; method: `"T3.unavailable_conclusion"`.

Denominator: Unavailable (null): `"This conclusion has no scalar denominator."`; coverage (ratio): Unavailable (null): `"This conclusion has no measured evidence coverage."`.

| Field | Value |
|---|---|
| `["assumptions"]` | `[]` |
| `["blocking_evidence"]` | `["Direct closure exposure describes the selected declared grounding scope, without tracing every pipeline input."]` |
| `["conclusion"]` | `"complete_pipeline_closure"` |
| `["coverage"]` | Unavailable (null): `"This conclusion has no measured evidence coverage."` |
| `["coverage_reason"]` | `"This conclusion has no measured evidence coverage."` |
| `["denominator"]` | Unavailable (null): `"This conclusion has no scalar denominator."` |
| `["denominator_reason"]` | `"This conclusion has no scalar denominator."` |
| `["evidence_class"]` | `"unavailable_conclusion"` |
| `["method_id"]` | `"T3.unavailable_conclusion"` |
| `["owner_ids"]` | `["T3"]` |
| `["reason_codes"]` | `["R_PIPELINE_BOUNDARY_EVIDENCE_MISSING"]` |
| `["related_capability"]` | `"provenance"` |
| `["representation"]` | Unavailable (null): No applicable representation supplied; consult status and required evidence. |
| `["required_evidence"]` | `["An explicit pipeline boundary and evidence for its relevant external inputs and transformations."]` |
| `["required_next_metadata"]` | `["An explicit pipeline boundary and evidence for its relevant external inputs and transformations."]` |
| `["scope"]["dataset_versions"]` | `["v1", "v2"]` |
| `["scope"]["denominator_basis"]` | `"all_validated_bundle_records"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 16 |
| `["scope"]["scope_id"]` | `"validated_bundle"` |
| `["statement"]` | `"Complete pipeline closure is unavailable from direct grounding declarations."` |
| `["status"]` | `"unavailable"` |
| `["theory_map_ids"]` | `[]` |
| `["theory_or_product_limit"]` | `"Even a direct closure interval of [1, 1] does not certify complete pipeline closure."` |
| `["trace_ids"]` | `["T3"]` |
| `["unit"]` | `"conclusion"` |

**`["limitations"]`**

- `"Unavailable means the supplied evidence does not support this conclusion; it does not establish that the conclusion is false."`

**`["scope"]["included_record_keys"]`**

| `"dataset_version"` | `"record_id"` |
|---|---|
| `"v1"` | `"v1_01"` |
| `"v1"` | `"v1_02"` |
| `"v1"` | `"v1_03"` |
| `"v1"` | `"v1_04"` |
| `"v1"` | `"v1_05"` |
| `"v1"` | `"v1_06"` |
| `"v1"` | `"v1_07"` |
| `"v1"` | `"v1_08"` |
| `"v2"` | `"v2_01"` |
| `"v2"` | `"v2_02"` |
| `"v2"` | `"v2_03"` |
| `"v2"` | `"v2_04"` |
| `"v2"` | `"v2_05"` |
| `"v2"` | `"v2_06"` |
| `"v2"` | `"v2_07"` |
| `"v2"` | `"v2_08"` |

### Analytical result

`["unavailable_conclusions"][6]`

Status: `"unavailable"`; evidence class: `"unavailable_conclusion"`; unit: `"conclusion"`; method: `"PR-014.unavailable_conclusion"`.

Denominator: Unavailable (null): `"This conclusion has no scalar denominator."`; coverage (ratio): Unavailable (null): `"This conclusion has no measured evidence coverage."`.

| Field | Value |
|---|---|
| `["assumptions"]` | `[]` |
| `["blocking_evidence"]` | `["Only existing reference validation observations can be reported; no graph traversal, root tracing or ancestry metric executes."]` |
| `["conclusion"]` | `"lineage_analysis"` |
| `["coverage"]` | Unavailable (null): `"This conclusion has no measured evidence coverage."` |
| `["coverage_reason"]` | `"This conclusion has no measured evidence coverage."` |
| `["denominator"]` | Unavailable (null): `"This conclusion has no scalar denominator."` |
| `["denominator_reason"]` | `"This conclusion has no scalar denominator."` |
| `["evidence_class"]` | `"unavailable_conclusion"` |
| `["method_id"]` | `"PR-014.unavailable_conclusion"` |
| `["owner_ids"]` | `["PR-014"]` |
| `["reason_codes"]` | `["R_LINEAGE_EXECUTION_DEFERRED"]` |
| `["related_capability"]` | `"lineage"` |
| `["representation"]` | Unavailable (null): No applicable representation supplied; consult status and required evidence. |
| `["required_evidence"]` | `["Preserve explicit composite parent references, chronology and external-grounding metadata for the future Phase 5 analysis."]` |
| `["required_next_metadata"]` | `["Preserve explicit composite parent references, chronology and external-grounding metadata for the future Phase 5 analysis."]` |
| `["scope"]["dataset_versions"]` | `["v1", "v2"]` |
| `["scope"]["denominator_basis"]` | `"all_validated_bundle_records"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 16 |
| `["scope"]["scope_id"]` | `"validated_bundle"` |
| `["statement"]` | `"General lineage graph analysis is deferred to Phase 5."` |
| `["status"]` | `"unavailable"` |
| `["theory_map_ids"]` | `[]` |
| `["theory_or_product_limit"]` | `"Implementation is deferred even when the existing input classifier marks lineage available."` |
| `["trace_ids"]` | `[]` |
| `["unit"]` | `"conclusion"` |

**`["limitations"]`**

- `"Unavailable means the supplied evidence does not support this conclusion; it does not establish that the conclusion is false."`

**`["scope"]["included_record_keys"]`**

| `"dataset_version"` | `"record_id"` |
|---|---|
| `"v1"` | `"v1_01"` |
| `"v1"` | `"v1_02"` |
| `"v1"` | `"v1_03"` |
| `"v1"` | `"v1_04"` |
| `"v1"` | `"v1_05"` |
| `"v1"` | `"v1_06"` |
| `"v1"` | `"v1_07"` |
| `"v1"` | `"v1_08"` |
| `"v2"` | `"v2_01"` |
| `"v2"` | `"v2_02"` |
| `"v2"` | `"v2_03"` |
| `"v2"` | `"v2_04"` |
| `"v2"` | `"v2_05"` |
| `"v2"` | `"v2_06"` |
| `"v2"` | `"v2_07"` |
| `"v2"` | `"v2_08"` |

### Analytical result

`["unavailable_conclusions"][7]`

Status: `"unavailable"`; evidence class: `"unavailable_conclusion"`; unit: `"conclusion"`; method: `"T3.unavailable_conclusion"`.

Denominator: Unavailable (null): `"This conclusion has no scalar denominator."`; coverage (ratio): Unavailable (null): `"This conclusion has no measured evidence coverage."`.

| Field | Value |
|---|---|
| `["assumptions"]` | `[]` |
| `["blocking_evidence"]` | `["Only existing reference validation observations can be reported; no graph traversal, root tracing or ancestry metric executes."]` |
| `["conclusion"]` | `"lineage_closure_exposure"` |
| `["coverage"]` | Unavailable (null): `"This conclusion has no measured evidence coverage."` |
| `["coverage_reason"]` | `"This conclusion has no measured evidence coverage."` |
| `["denominator"]` | Unavailable (null): `"This conclusion has no scalar denominator."` |
| `["denominator_reason"]` | `"This conclusion has no scalar denominator."` |
| `["evidence_class"]` | `"unavailable_conclusion"` |
| `["method_id"]` | `"T3.unavailable_conclusion"` |
| `["owner_ids"]` | `["T3"]` |
| `["reason_codes"]` | `["R_LINEAGE_EXECUTION_DEFERRED"]` |
| `["related_capability"]` | `"lineage"` |
| `["representation"]` | Unavailable (null): No applicable representation supplied; consult status and required evidence. |
| `["required_evidence"]` | `["Preserve explicit composite parent references, chronology and external-grounding metadata for the future Phase 5 analysis."]` |
| `["required_next_metadata"]` | `["Preserve explicit composite parent references, chronology and external-grounding metadata for the future Phase 5 analysis."]` |
| `["scope"]["dataset_versions"]` | `["v1", "v2"]` |
| `["scope"]["denominator_basis"]` | `"all_validated_bundle_records"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 16 |
| `["scope"]["scope_id"]` | `"validated_bundle"` |
| `["statement"]` | `"Lineage closure exposure is deferred to Phase 5."` |
| `["status"]` | `"unavailable"` |
| `["theory_map_ids"]` | `[]` |
| `["theory_or_product_limit"]` | `"Implementation is deferred even when the existing input classifier marks lineage available."` |
| `["trace_ids"]` | `["T3"]` |
| `["unit"]` | `"conclusion"` |

**`["limitations"]`**

- `"Unavailable means the supplied evidence does not support this conclusion; it does not establish that the conclusion is false."`

**`["scope"]["included_record_keys"]`**

| `"dataset_version"` | `"record_id"` |
|---|---|
| `"v1"` | `"v1_01"` |
| `"v1"` | `"v1_02"` |
| `"v1"` | `"v1_03"` |
| `"v1"` | `"v1_04"` |
| `"v1"` | `"v1_05"` |
| `"v1"` | `"v1_06"` |
| `"v1"` | `"v1_07"` |
| `"v1"` | `"v1_08"` |
| `"v2"` | `"v2_01"` |
| `"v2"` | `"v2_02"` |
| `"v2"` | `"v2_03"` |
| `"v2"` | `"v2_04"` |
| `"v2"` | `"v2_05"` |
| `"v2"` | `"v2_06"` |
| `"v2"` | `"v2_07"` |
| `"v2"` | `"v2_08"` |

### Analytical result

`["unavailable_conclusions"][8]`

Status: `"unavailable"`; evidence class: `"unavailable_conclusion"`; unit: `"conclusion"`; method: `"T4.unavailable_conclusion"`.

Denominator: Unavailable (null): `"This conclusion has no scalar denominator."`; coverage (ratio): Unavailable (null): `"This conclusion has no measured evidence coverage."`.

| Field | Value |
|---|---|
| `["assumptions"]` | `[]` |
| `["blocking_evidence"]` | `["Only existing reference validation observations can be reported; no graph traversal, root tracing or ancestry metric executes."]` |
| `["conclusion"]` | `"external_ancestry"` |
| `["coverage"]` | Unavailable (null): `"This conclusion has no measured evidence coverage."` |
| `["coverage_reason"]` | `"This conclusion has no measured evidence coverage."` |
| `["denominator"]` | Unavailable (null): `"This conclusion has no scalar denominator."` |
| `["denominator_reason"]` | `"This conclusion has no scalar denominator."` |
| `["evidence_class"]` | `"unavailable_conclusion"` |
| `["method_id"]` | `"T4.unavailable_conclusion"` |
| `["owner_ids"]` | `["T4"]` |
| `["reason_codes"]` | `["R_LINEAGE_EXECUTION_DEFERRED"]` |
| `["related_capability"]` | `"lineage"` |
| `["representation"]` | Unavailable (null): No applicable representation supplied; consult status and required evidence. |
| `["required_evidence"]` | `["Preserve explicit composite parent references, chronology and external-grounding metadata for the future Phase 5 analysis."]` |
| `["required_next_metadata"]` | `["Preserve explicit composite parent references, chronology and external-grounding metadata for the future Phase 5 analysis."]` |
| `["scope"]["dataset_versions"]` | `["v1", "v2"]` |
| `["scope"]["denominator_basis"]` | `"all_validated_bundle_records"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 16 |
| `["scope"]["scope_id"]` | `"validated_bundle"` |
| `["statement"]` | `"External ancestry results are deferred to Phase 5."` |
| `["status"]` | `"unavailable"` |
| `["theory_map_ids"]` | `[]` |
| `["theory_or_product_limit"]` | `"Implementation is deferred even when the existing input classifier marks lineage available."` |
| `["trace_ids"]` | `["T4"]` |
| `["unit"]` | `"conclusion"` |

**`["limitations"]`**

- `"Unavailable means the supplied evidence does not support this conclusion; it does not establish that the conclusion is false."`

**`["scope"]["included_record_keys"]`**

| `"dataset_version"` | `"record_id"` |
|---|---|
| `"v1"` | `"v1_01"` |
| `"v1"` | `"v1_02"` |
| `"v1"` | `"v1_03"` |
| `"v1"` | `"v1_04"` |
| `"v1"` | `"v1_05"` |
| `"v1"` | `"v1_06"` |
| `"v1"` | `"v1_07"` |
| `"v1"` | `"v1_08"` |
| `"v2"` | `"v2_01"` |
| `"v2"` | `"v2_02"` |
| `"v2"` | `"v2_03"` |
| `"v2"` | `"v2_04"` |
| `"v2"` | `"v2_05"` |
| `"v2"` | `"v2_06"` |
| `"v2"` | `"v2_07"` |
| `"v2"` | `"v2_08"` |

## Recommended next metadata

- **Recommended metadata 1**

| Field | Value |
|---|---|
| `["expected_unlock"]` | `["evidence needed by a future model-longitudinal implementation"]` |
| `["metadata"]` | `"versioned_model_outcomes"` |
| `["owner_ids"]` | `["PR-014"]` |
| `["priority"]` | 4 |
| `["reason"]` | `"Dataset audit fields do not supply model-performance outcomes."` |
| `["scope"]` | `"models and comparable evaluation conditions"` |

## Warnings

No entries supplied. Empty list: `[]`.

## Errors

No entries supplied. Empty list: `[]`.

***

**Report footer**

Toolkit version: `"0.1.0.dev2"`; report schema version: `"1.0"`.

Evidence-class legend:

- `observed_fact`: supplied or exactly counted evidence.
- `derived_metric`: a deterministic function of supplied evidence.
- `proxy_signal`: a bounded interpretation with stated limitations.
- `simulation`: a scenario under explicit assumptions; experimental outputs retain that status.
- `unavailable_conclusion`: required evidence is absent, implementation is deferred, or the conclusion lies outside approved scope.

Unavailable conclusions are not false conclusions. Input observability and execution status describe separate facts. Supplied provenance declarations do not establish independently verified truth.

Traceability reference: THEORY_TO_CODE_TRACEABILITY.md and docs/report_schema.md; individual results retain their owner IDs, theory-map IDs, trace IDs and method IDs.
