# Recursive Integrity Audit Report

**Summary**

- Run ID: `"phase4-step9-golden"`.
- Maximum observability level: 4; `"longitudinal_dataset_observability"`.
- Capability statuses: Ingestion: `"available"` (execution `"completed"`); Content diagnostics: `"available"` (execution `"completed"`); Provenance: `"available"` (execution `"completed"`); Lineage: `"available"` (execution `"deferred"`); Dataset longitudinal: `"available"` (execution `"partial"`); Model longitudinal: `"unavailable"` (execution `"deferred"`); Intervention simulation: `"unavailable"` (execution `"not_requested"`).
- Record scope: `"hmac-sha256:fe3080b69d042a9eca2d392f8429412803f06dd3eb9e71fd16178d05e5971ac3"`; dataset versions `["hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4", "hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"]`; records 16; excluded records 0.
- Representation: `"hmac-sha256:220b787af129ef50eab4ee9f3c90a00a7bce0a525c6e49bfc40fe9bb8af1d0b8"`; source `"hmac-sha256:1faa75c58dd3f727bec66d81de5cab7c2e64afbebcd03c32653ba5432a5c4369"`; version `"hmac-sha256:b6d6724490a6778f4b6e234f43fff3602f2707d6b9ab74acb0cc8e83c96d3da8"`. Complete mapping metadata appears in Input inventory.
- Warning entries: 0; error entries: 0.

Display policy: numbers use shortest round-trip decimal notation without rounding; scientific notation retains tiny nonzero values. Ratios and probabilities remain unscaled. Units, denominators and interval endpoints are supplied evidence. JSON is the machine-readable authority.

Quoted code literals represent supplied data, including identifiers and labels. JSON escapes visibly preserve markup characters and invisible controls. Unavailable (null) carries its declared reason or an explicit field-level null explanation. Empty objects and lists are shown explicitly. Object keys are sorted; supplied list order is preserved.

## Run metadata

| Field | Value |
|---|---|
| `["command"]` | `"rit example --redacted"` |
| `["completed_at"]` | `"2000-01-01T00:00:00+00:00"` |
| `["config_hash"]` | `"152adcf6378cba3fd09232c867f3cd4b5fdf569e6e5ef82ea02deaaa4f6e90f3"` |
| `["config_hash_exclusions"]` | `["id_salt_file", "identifier_secret_material"]` |
| `["deterministic"]` | true |
| `["duration_seconds"]` | 0.0 |
| `["hash_algorithm"]` | `"sha256"` |
| `["identifier_protection"]["algorithm"]` | `"HMAC-SHA-256"` |
| `["identifier_protection"]["record_id_mode"]` | `"hash"` |
| `["identifier_protection"]["stability_scope"]` | `"run"` |
| `["network_call_count"]` | 0 |
| `["network_count_scope"]` | `"toolkit_managed_outbound_operations"` |
| `["null_reasons"]["platform"]` | `"private_or_nonstandard_metadata_omitted"` |
| `["null_reasons"]["python_version"]` | `"private_or_nonstandard_metadata_omitted"` |
| `["null_reasons"]["random_seed"]` | `"not_recorded"` |
| `["platform"]` | Unavailable (null): `"private_or_nonstandard_metadata_omitted"` |
| `["privacy_mode"]` | `"redacted"` |
| `["python_version"]` | Unavailable (null): `"private_or_nonstandard_metadata_omitted"` |
| `["random_seed"]` | Unavailable (null): `"not_recorded"` |
| `["redacted_mode"]` | true |
| `["report_schema_version"]` | `"1.0"` |
| `["resolved_options"]["comparison_requested"]` | true |
| `["resolved_options"]["privacy_mode"]` | `"redacted"` |
| `["resolved_options"]["record_id_mode"]` | `"hash"` |
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

## Input inventory

| Field | Value |
|---|---|
| `["artifacts"][0]["dataset_versions"]` | `[]` |
| `["artifacts"][0]["file_hash"]` | `"2e069eb9c0105bf05c145ca15eec47834eb66f4408e8cdde9ff4935f5b920241"` |
| `["artifacts"][0]["format"]` | `"json"` |
| `["artifacts"][0]["hash_algorithm"]` | `"sha256"` |
| `["artifacts"][0]["parse_status"]` | `"completed"` |
| `["artifacts"][0]["path"]` | Unavailable (null): Withheld by the selected privacy view. |
| `["artifacts"][0]["path_redacted"]` | true |
| `["artifacts"][0]["reason_codes"]` | `[]` |
| `["artifacts"][0]["role"]` | `"config"` |
| `["artifacts"][0]["row_count"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["artifacts"][0]["schema_fields"]` | `[]` |
| `["artifacts"][0]["size_bytes"]` | 170 |
| `["artifacts"][0]["validation_status"]` | `"completed"` |
| `["artifacts"][1]["dataset_versions"]` | `["hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4", "hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"]` |
| `["artifacts"][1]["file_hash"]` | `"fc4ed3921d087e37996228dd8a37c4c51a0a3c3c91ded3e62a21e1b10f407438"` |
| `["artifacts"][1]["format"]` | `"csv"` |
| `["artifacts"][1]["hash_algorithm"]` | `"sha256"` |
| `["artifacts"][1]["parse_status"]` | `"completed"` |
| `["artifacts"][1]["path"]` | Unavailable (null): Withheld by the selected privacy view. |
| `["artifacts"][1]["path_redacted"]` | true |
| `["artifacts"][1]["reason_codes"]` | `[]` |
| `["artifacts"][1]["role"]` | `"provenance_manifest"` |
| `["artifacts"][1]["row_count"]` | 16 |
| `["artifacts"][1]["schema_fields"]` | `["hmac-sha256:2deeaf4e2293c400e4f20629b6bba139cc8e12ea8a535e2c32b4d3da58accab7", "hmac-sha256:065f53dbd37374e0f98a3f49f8bca82c7a5ee64760b3d46ab336753b069929cc", "hmac-sha256:0f994ec3a77364f4b5024bb30ee1271e70a136e0589962f8f9b003d272c8c57d", "hmac-sha256:a857b5660e6eff740c7654909958791fbfb32bddc672ae4b7409acb451d35c13", "hmac-sha256:aa939706eece99c8a2f03d10195bda99ea2534f8e051d76062b79a647f4aff2f", "hmac-sha256:ca1d20990ef057e14560b27817a2257db2fd2208366a74469ff69d358a10fa1f", "hmac-sha256:d2375a7026b95a6981fe3d2e5d6d824089967fe9a5f9c309802566b9df15f4aa", "hmac-sha256:6ace5f5ef2cba0d1bc79f704e6a7937b739ae243f53d9e49578ede2bcdfe3731", "hmac-sha256:c7a5e0cf3dc8e3bdf73faefe15ac386acf6de3b71d4c9826112dc8e3e41c1ee9", "hmac-sha256:1de2e894bcb45f1513ac3cae32e46574c7d9af1993a6dd2dab4264072b95e0e2", "hmac-sha256:804b1979f9819464d434860b0ce67bbbc23a3fc3983753bc7affba182e4c8386"]` |
| `["artifacts"][1]["size_bytes"]` | 1294 |
| `["artifacts"][1]["validation_status"]` | `"completed"` |
| `["artifacts"][2]["dataset_versions"]` | `["hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"]` |
| `["artifacts"][2]["file_hash"]` | `"b62c9aee057c61f641009b949acb110e003acbea6a399cc607a78ee6e6f0543d"` |
| `["artifacts"][2]["format"]` | `"csv"` |
| `["artifacts"][2]["hash_algorithm"]` | `"sha256"` |
| `["artifacts"][2]["parse_status"]` | `"completed"` |
| `["artifacts"][2]["path"]` | Unavailable (null): Withheld by the selected privacy view. |
| `["artifacts"][2]["path_redacted"]` | true |
| `["artifacts"][2]["reason_codes"]` | `[]` |
| `["artifacts"][2]["role"]` | `"records_compare"` |
| `["artifacts"][2]["row_count"]` | 8 |
| `["artifacts"][2]["schema_fields"]` | `["hmac-sha256:065f53dbd37374e0f98a3f49f8bca82c7a5ee64760b3d46ab336753b069929cc", "hmac-sha256:2deeaf4e2293c400e4f20629b6bba139cc8e12ea8a535e2c32b4d3da58accab7", "hmac-sha256:287bdbb8726ab8ea37f763ce20cc5e1a782a16604270bb38ca54d65d0be0efaa", "hmac-sha256:47e6ffdde83ab627afa8a2c8617571bf1cf11f84faf6415e021a437406b58765"]` |
| `["artifacts"][2]["size_bytes"]` | 437 |
| `["artifacts"][2]["validation_status"]` | `"completed"` |
| `["artifacts"][3]["dataset_versions"]` | `["hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"]` |
| `["artifacts"][3]["file_hash"]` | `"d691605fd6bb37e785945ae34c8c18ea8409201f7d78449d39df08df7770599b"` |
| `["artifacts"][3]["format"]` | `"csv"` |
| `["artifacts"][3]["hash_algorithm"]` | `"sha256"` |
| `["artifacts"][3]["parse_status"]` | `"completed"` |
| `["artifacts"][3]["path"]` | Unavailable (null): Withheld by the selected privacy view. |
| `["artifacts"][3]["path_redacted"]` | true |
| `["artifacts"][3]["reason_codes"]` | `[]` |
| `["artifacts"][3]["role"]` | `"records_primary"` |
| `["artifacts"][3]["row_count"]` | 8 |
| `["artifacts"][3]["schema_fields"]` | `["hmac-sha256:065f53dbd37374e0f98a3f49f8bca82c7a5ee64760b3d46ab336753b069929cc", "hmac-sha256:2deeaf4e2293c400e4f20629b6bba139cc8e12ea8a535e2c32b4d3da58accab7", "hmac-sha256:287bdbb8726ab8ea37f763ce20cc5e1a782a16604270bb38ca54d65d0be0efaa", "hmac-sha256:47e6ffdde83ab627afa8a2c8617571bf1cf11f84faf6415e021a437406b58765"]` |
| `["artifacts"][3]["size_bytes"]` | 442 |
| `["artifacts"][3]["validation_status"]` | `"completed"` |
| `["artifacts"][4]["dataset_versions"]` | `[]` |
| `["artifacts"][4]["file_hash"]` | `"3e33ca8b2095f35f55d22265071bce00119c9282b72bb02cee3275c646898387"` |
| `["artifacts"][4]["format"]` | `"json"` |
| `["artifacts"][4]["hash_algorithm"]` | `"sha256"` |
| `["artifacts"][4]["parse_status"]` | `"completed"` |
| `["artifacts"][4]["path"]` | Unavailable (null): Withheld by the selected privacy view. |
| `["artifacts"][4]["path_redacted"]` | true |
| `["artifacts"][4]["reason_codes"]` | `[]` |
| `["artifacts"][4]["role"]` | `"version_order"` |
| `["artifacts"][4]["row_count"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["artifacts"][4]["schema_fields"]` | `[]` |
| `["artifacts"][4]["size_bytes"]` | 36 |
| `["artifacts"][4]["validation_status"]` | `"completed"` |
| `["representation"]["binning_or_mapping_rule"]` | `"hmac-sha256:18da0fd476e3b47330cd178d9efef7c39c415771e8f8bd5cb6a7f13e9681a9b3"` |
| `["representation"]["field_name"]` | `"hmac-sha256:47e6ffdde83ab627afa8a2c8617571bf1cf11f84faf6415e021a437406b58765"` |
| `["representation"]["missing_state_id"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["missing_value_policy"]` | `"error"` |
| `["representation"]["normalization_profile"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["representation_name"]` | `"hmac-sha256:220b787af129ef50eab4ee9f3c90a00a7bce0a525c6e49bfc40fe9bb8af1d0b8"` |
| `["representation"]["representation_source"]` | `"hmac-sha256:1faa75c58dd3f727bec66d81de5cab7c2e64afbebcd03c32653ba5432a5c4369"` |
| `["representation"]["representation_version"]` | `"hmac-sha256:b6d6724490a6778f4b6e234f43fff3602f2707d6b9ab74acb0cc8e83c96d3da8"` |
| `["scope"]["dataset_versions"]` | `["hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4", "hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"]` |
| `["scope"]["denominator_basis"]` | `"all_validated_bundle_records"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 16 |
| `["scope"]["scope_id"]` | `"hmac-sha256:fe3080b69d042a9eca2d392f8429412803f06dd3eb9e71fd16178d05e5971ac3"` |
| `["version_order"]` | `["hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4", "hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"]` |
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
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:a130e0b7f4696e3bc1ed555d0170b426ca57c7efed97c9c27766355dd842ec1c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:6da9164abc2800aec9b384c96483bc3bc128008df04704ad7050851f8b3f9a2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:52d7e4984062cff58f5ee2ab4592f4174277c11213b23be0f66b0da6c2801b15"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:b09664f79e8df7595b88db8e5d4fd40a678384e2b4816e04044a63b901c6dc3d"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:18eea61d82b38372f77e43b8596c93ef577d554d1cb4dba3545cd509026b1c2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:d829ae28c8f6422156149b7d293896efb88703427b4b31d13996703e67d35aae"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:41770f394bc6316c571ecb74ac4e07554113bb8f92d0c56603009a81daeeff12"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:3913f4a00a32e7b06211da44f3d156e37509bf8aefde1ba61f221717eaae8c8d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:aae75164d165f5a4c0e499d094250b126cb2c634f1f3c5a55226be1fd115c101"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:0a8b103130fe77d9b2a8d6f9ab9e4d69cc7146f7f342b859fdf9ce0c703fed5d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c40d9ce71dce69af2ccfd0c4396f6fcea650358a04107008cfa34ec73e82fc4"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:8167cf7b096bcf02b20dbc95d47de65bf2b7eb2902495b089aae8ad6cc2ffae7"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c808566f31ad17b61c8700c5ecf0e95be4fd01ca4b2edf3bb12f80f4de49255"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c45259baf1db3285bd3b9cb81d1637bfcd7ac34589868894e6ad63ee93577a0a"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c60be35d2fffdab2e6c81834408613d778914041c0ecd3f4a0f5be53541dc7bd"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:27864c18901ea515a772984044b552f7cb3a0d2a058bd1a67a9b53dc49c4ab5d"` |

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
| `["execution_scope"]` | `["supplied_distribution:hmac-sha256:e8d3d329142ddbec8c51b0affa3d8ade12402bebc6e9d4b1e2a994e17ed56f05", "supplied_distribution:hmac-sha256:62f240a66b38ae21fd6453c60b78d6ee2712c8ef1933c6c15983da3e393cbffc"]` |
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
| `["execution_scope"]` | `["supplied_provenance_composition:hmac-sha256:41c8e31c7545a4277beda762e2ba57b6a564fa2d3be40bd892b8cf353afa6475", "supplied_direct_closure_interval:hmac-sha256:41c8e31c7545a4277beda762e2ba57b6a564fa2d3be40bd892b8cf353afa6475"]` |
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
| `["scope"]["dataset_versions"]` | `["hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4", "hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"]` |
| `["scope"]["denominator_basis"]` | `"all_validated_bundle_records"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 16 |
| `["scope"]["scope_id"]` | `"hmac-sha256:fe3080b69d042a9eca2d392f8429412803f06dd3eb9e71fd16178d05e5971ac3"` |
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
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:a130e0b7f4696e3bc1ed555d0170b426ca57c7efed97c9c27766355dd842ec1c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:6da9164abc2800aec9b384c96483bc3bc128008df04704ad7050851f8b3f9a2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:52d7e4984062cff58f5ee2ab4592f4174277c11213b23be0f66b0da6c2801b15"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:b09664f79e8df7595b88db8e5d4fd40a678384e2b4816e04044a63b901c6dc3d"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:18eea61d82b38372f77e43b8596c93ef577d554d1cb4dba3545cd509026b1c2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:d829ae28c8f6422156149b7d293896efb88703427b4b31d13996703e67d35aae"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:41770f394bc6316c571ecb74ac4e07554113bb8f92d0c56603009a81daeeff12"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:3913f4a00a32e7b06211da44f3d156e37509bf8aefde1ba61f221717eaae8c8d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:aae75164d165f5a4c0e499d094250b126cb2c634f1f3c5a55226be1fd115c101"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:0a8b103130fe77d9b2a8d6f9ab9e4d69cc7146f7f342b859fdf9ce0c703fed5d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c40d9ce71dce69af2ccfd0c4396f6fcea650358a04107008cfa34ec73e82fc4"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:8167cf7b096bcf02b20dbc95d47de65bf2b7eb2902495b089aae8ad6cc2ffae7"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c808566f31ad17b61c8700c5ecf0e95be4fd01ca4b2edf3bb12f80f4de49255"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c45259baf1db3285bd3b9cb81d1637bfcd7ac34589868894e6ad63ee93577a0a"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c60be35d2fffdab2e6c81834408613d778914041c0ecd3f4a0f5be53541dc7bd"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:27864c18901ea515a772984044b552f7cb3a0d2a058bd1a67a9b53dc49c4ab5d"` |

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
| `["scope"]["dataset_versions"]` | `["hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4", "hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"]` |
| `["scope"]["denominator_basis"]` | `"all_validated_bundle_records"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 16 |
| `["scope"]["scope_id"]` | `"hmac-sha256:fe3080b69d042a9eca2d392f8429412803f06dd3eb9e71fd16178d05e5971ac3"` |
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
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:a130e0b7f4696e3bc1ed555d0170b426ca57c7efed97c9c27766355dd842ec1c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:6da9164abc2800aec9b384c96483bc3bc128008df04704ad7050851f8b3f9a2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:52d7e4984062cff58f5ee2ab4592f4174277c11213b23be0f66b0da6c2801b15"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:b09664f79e8df7595b88db8e5d4fd40a678384e2b4816e04044a63b901c6dc3d"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:18eea61d82b38372f77e43b8596c93ef577d554d1cb4dba3545cd509026b1c2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:d829ae28c8f6422156149b7d293896efb88703427b4b31d13996703e67d35aae"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:41770f394bc6316c571ecb74ac4e07554113bb8f92d0c56603009a81daeeff12"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:3913f4a00a32e7b06211da44f3d156e37509bf8aefde1ba61f221717eaae8c8d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:aae75164d165f5a4c0e499d094250b126cb2c634f1f3c5a55226be1fd115c101"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:0a8b103130fe77d9b2a8d6f9ab9e4d69cc7146f7f342b859fdf9ce0c703fed5d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c40d9ce71dce69af2ccfd0c4396f6fcea650358a04107008cfa34ec73e82fc4"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:8167cf7b096bcf02b20dbc95d47de65bf2b7eb2902495b089aae8ad6cc2ffae7"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c808566f31ad17b61c8700c5ecf0e95be4fd01ca4b2edf3bb12f80f4de49255"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c45259baf1db3285bd3b9cb81d1637bfcd7ac34589868894e6ad63ee93577a0a"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c60be35d2fffdab2e6c81834408613d778914041c0ecd3f4a0f5be53541dc7bd"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:27864c18901ea515a772984044b552f7cb3a0d2a058bd1a67a9b53dc49c4ab5d"` |

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
| `["scope"]["dataset_versions"]` | `["hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4", "hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"]` |
| `["scope"]["denominator_basis"]` | `"all_validated_bundle_records"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 16 |
| `["scope"]["scope_id"]` | `"hmac-sha256:fe3080b69d042a9eca2d392f8429412803f06dd3eb9e71fd16178d05e5971ac3"` |
| `["status"]` | `"available"` |
| `["theory_map_ids"]` | `[]` |
| `["trace_ids"]` | `[]` |
| `["unit"]` | `"certificate"` |
| `["value"]["all_resolved_edges_follow_order"]` | true |
| `["value"]["method"]` | `"declared_earlier_version_order"` |
| `["value"]["version_order"]` | `["hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4", "hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"]` |

**`["limitations"]`**

- `"This retained earlier-version ordering certificate is not general graph-cycle traversal."`

**`["scope"]["included_record_keys"]`**

| `"dataset_version"` | `"record_id"` |
|---|---|
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:a130e0b7f4696e3bc1ed555d0170b426ca57c7efed97c9c27766355dd842ec1c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:6da9164abc2800aec9b384c96483bc3bc128008df04704ad7050851f8b3f9a2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:52d7e4984062cff58f5ee2ab4592f4174277c11213b23be0f66b0da6c2801b15"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:b09664f79e8df7595b88db8e5d4fd40a678384e2b4816e04044a63b901c6dc3d"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:18eea61d82b38372f77e43b8596c93ef577d554d1cb4dba3545cd509026b1c2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:d829ae28c8f6422156149b7d293896efb88703427b4b31d13996703e67d35aae"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:41770f394bc6316c571ecb74ac4e07554113bb8f92d0c56603009a81daeeff12"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:3913f4a00a32e7b06211da44f3d156e37509bf8aefde1ba61f221717eaae8c8d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:aae75164d165f5a4c0e499d094250b126cb2c634f1f3c5a55226be1fd115c101"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:0a8b103130fe77d9b2a8d6f9ab9e4d69cc7146f7f342b859fdf9ce0c703fed5d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c40d9ce71dce69af2ccfd0c4396f6fcea650358a04107008cfa34ec73e82fc4"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:8167cf7b096bcf02b20dbc95d47de65bf2b7eb2902495b089aae8ad6cc2ffae7"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c808566f31ad17b61c8700c5ecf0e95be4fd01ca4b2edf3bb12f80f4de49255"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c45259baf1db3285bd3b9cb81d1637bfcd7ac34589868894e6ad63ee93577a0a"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c60be35d2fffdab2e6c81834408613d778914041c0ecd3f4a0f5be53541dc7bd"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:27864c18901ea515a772984044b552f7cb3a0d2a058bd1a67a9b53dc49c4ab5d"` |

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
| `["scope"]["dataset_versions"]` | `["hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4", "hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"]` |
| `["scope"]["denominator_basis"]` | `"all_validated_bundle_records"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 16 |
| `["scope"]["scope_id"]` | `"hmac-sha256:fe3080b69d042a9eca2d392f8429412803f06dd3eb9e71fd16178d05e5971ac3"` |
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
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:a130e0b7f4696e3bc1ed555d0170b426ca57c7efed97c9c27766355dd842ec1c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:6da9164abc2800aec9b384c96483bc3bc128008df04704ad7050851f8b3f9a2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:52d7e4984062cff58f5ee2ab4592f4174277c11213b23be0f66b0da6c2801b15"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:b09664f79e8df7595b88db8e5d4fd40a678384e2b4816e04044a63b901c6dc3d"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:18eea61d82b38372f77e43b8596c93ef577d554d1cb4dba3545cd509026b1c2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:d829ae28c8f6422156149b7d293896efb88703427b4b31d13996703e67d35aae"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:41770f394bc6316c571ecb74ac4e07554113bb8f92d0c56603009a81daeeff12"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:3913f4a00a32e7b06211da44f3d156e37509bf8aefde1ba61f221717eaae8c8d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:aae75164d165f5a4c0e499d094250b126cb2c634f1f3c5a55226be1fd115c101"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:0a8b103130fe77d9b2a8d6f9ab9e4d69cc7146f7f342b859fdf9ce0c703fed5d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c40d9ce71dce69af2ccfd0c4396f6fcea650358a04107008cfa34ec73e82fc4"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:8167cf7b096bcf02b20dbc95d47de65bf2b7eb2902495b089aae8ad6cc2ffae7"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c808566f31ad17b61c8700c5ecf0e95be4fd01ca4b2edf3bb12f80f4de49255"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c45259baf1db3285bd3b9cb81d1637bfcd7ac34589868894e6ad63ee93577a0a"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c60be35d2fffdab2e6c81834408613d778914041c0ecd3f4a0f5be53541dc7bd"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:27864c18901ea515a772984044b552f7cb3a0d2a058bd1a67a9b53dc49c4ab5d"` |

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
| `["scope"]["dataset_versions"]` | `["hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4", "hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"]` |
| `["scope"]["denominator_basis"]` | `"all_validated_bundle_records"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 16 |
| `["scope"]["scope_id"]` | `"hmac-sha256:fe3080b69d042a9eca2d392f8429412803f06dd3eb9e71fd16178d05e5971ac3"` |
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
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:a130e0b7f4696e3bc1ed555d0170b426ca57c7efed97c9c27766355dd842ec1c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:6da9164abc2800aec9b384c96483bc3bc128008df04704ad7050851f8b3f9a2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:52d7e4984062cff58f5ee2ab4592f4174277c11213b23be0f66b0da6c2801b15"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:b09664f79e8df7595b88db8e5d4fd40a678384e2b4816e04044a63b901c6dc3d"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:18eea61d82b38372f77e43b8596c93ef577d554d1cb4dba3545cd509026b1c2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:d829ae28c8f6422156149b7d293896efb88703427b4b31d13996703e67d35aae"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:41770f394bc6316c571ecb74ac4e07554113bb8f92d0c56603009a81daeeff12"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:3913f4a00a32e7b06211da44f3d156e37509bf8aefde1ba61f221717eaae8c8d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:aae75164d165f5a4c0e499d094250b126cb2c634f1f3c5a55226be1fd115c101"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:0a8b103130fe77d9b2a8d6f9ab9e4d69cc7146f7f342b859fdf9ce0c703fed5d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c40d9ce71dce69af2ccfd0c4396f6fcea650358a04107008cfa34ec73e82fc4"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:8167cf7b096bcf02b20dbc95d47de65bf2b7eb2902495b089aae8ad6cc2ffae7"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c808566f31ad17b61c8700c5ecf0e95be4fd01ca4b2edf3bb12f80f4de49255"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c45259baf1db3285bd3b9cb81d1637bfcd7ac34589868894e6ad63ee93577a0a"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c60be35d2fffdab2e6c81834408613d778914041c0ecd3f4a0f5be53541dc7bd"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:27864c18901ea515a772984044b552f7cb3a0d2a058bd1a67a9b53dc49c4ab5d"` |

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
| `["scope"]["dataset_versions"]` | `["hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"]` |
| `["scope"]["denominator_basis"]` | `"all_valid_records_in_selected_dataset_scope"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"hmac-sha256:41c8e31c7545a4277beda762e2ba57b6a564fa2d3be40bd892b8cf353afa6475"` |
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
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:aae75164d165f5a4c0e499d094250b126cb2c634f1f3c5a55226be1fd115c101"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:0a8b103130fe77d9b2a8d6f9ab9e4d69cc7146f7f342b859fdf9ce0c703fed5d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c40d9ce71dce69af2ccfd0c4396f6fcea650358a04107008cfa34ec73e82fc4"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:8167cf7b096bcf02b20dbc95d47de65bf2b7eb2902495b089aae8ad6cc2ffae7"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c808566f31ad17b61c8700c5ecf0e95be4fd01ca4b2edf3bb12f80f4de49255"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c45259baf1db3285bd3b9cb81d1637bfcd7ac34589868894e6ad63ee93577a0a"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c60be35d2fffdab2e6c81834408613d778914041c0ecd3f4a0f5be53541dc7bd"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:27864c18901ea515a772984044b552f7cb3a0d2a058bd1a67a9b53dc49c4ab5d"` |

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
| `["scope"]["dataset_versions"]` | `["hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"]` |
| `["scope"]["denominator_basis"]` | `"all_valid_records_in_selected_dataset_scope"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"hmac-sha256:41c8e31c7545a4277beda762e2ba57b6a564fa2d3be40bd892b8cf353afa6475"` |
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
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:aae75164d165f5a4c0e499d094250b126cb2c634f1f3c5a55226be1fd115c101"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:0a8b103130fe77d9b2a8d6f9ab9e4d69cc7146f7f342b859fdf9ce0c703fed5d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c40d9ce71dce69af2ccfd0c4396f6fcea650358a04107008cfa34ec73e82fc4"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:8167cf7b096bcf02b20dbc95d47de65bf2b7eb2902495b089aae8ad6cc2ffae7"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c808566f31ad17b61c8700c5ecf0e95be4fd01ca4b2edf3bb12f80f4de49255"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c45259baf1db3285bd3b9cb81d1637bfcd7ac34589868894e6ad63ee93577a0a"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c60be35d2fffdab2e6c81834408613d778914041c0ecd3f4a0f5be53541dc7bd"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:27864c18901ea515a772984044b552f7cb3a0d2a058bd1a67a9b53dc49c4ab5d"` |

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
| `["scope"]["dataset_versions"]` | `["hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"]` |
| `["scope"]["denominator_basis"]` | `"all_valid_records_in_selected_dataset_scope"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"hmac-sha256:41c8e31c7545a4277beda762e2ba57b6a564fa2d3be40bd892b8cf353afa6475"` |
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
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:aae75164d165f5a4c0e499d094250b126cb2c634f1f3c5a55226be1fd115c101"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:0a8b103130fe77d9b2a8d6f9ab9e4d69cc7146f7f342b859fdf9ce0c703fed5d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c40d9ce71dce69af2ccfd0c4396f6fcea650358a04107008cfa34ec73e82fc4"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:8167cf7b096bcf02b20dbc95d47de65bf2b7eb2902495b089aae8ad6cc2ffae7"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c808566f31ad17b61c8700c5ecf0e95be4fd01ca4b2edf3bb12f80f4de49255"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c45259baf1db3285bd3b9cb81d1637bfcd7ac34589868894e6ad63ee93577a0a"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c60be35d2fffdab2e6c81834408613d778914041c0ecd3f4a0f5be53541dc7bd"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:27864c18901ea515a772984044b552f7cb3a0d2a058bd1a67a9b53dc49c4ab5d"` |

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
| `["scope"]["dataset_versions"]` | `["hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"]` |
| `["scope"]["denominator_basis"]` | `"all_valid_records_in_selected_dataset_scope"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"hmac-sha256:41c8e31c7545a4277beda762e2ba57b6a564fa2d3be40bd892b8cf353afa6475"` |
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
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:aae75164d165f5a4c0e499d094250b126cb2c634f1f3c5a55226be1fd115c101"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:0a8b103130fe77d9b2a8d6f9ab9e4d69cc7146f7f342b859fdf9ce0c703fed5d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c40d9ce71dce69af2ccfd0c4396f6fcea650358a04107008cfa34ec73e82fc4"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:8167cf7b096bcf02b20dbc95d47de65bf2b7eb2902495b089aae8ad6cc2ffae7"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c808566f31ad17b61c8700c5ecf0e95be4fd01ca4b2edf3bb12f80f4de49255"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c45259baf1db3285bd3b9cb81d1637bfcd7ac34589868894e6ad63ee93577a0a"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c60be35d2fffdab2e6c81834408613d778914041c0ecd3f4a0f5be53541dc7bd"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:27864c18901ea515a772984044b552f7cb3a0d2a058bd1a67a9b53dc49c4ab5d"` |

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
| `["scope"]["dataset_versions"]` | `["hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"]` |
| `["scope"]["denominator_basis"]` | `"all_valid_records_in_selected_dataset_scope"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"hmac-sha256:41c8e31c7545a4277beda762e2ba57b6a564fa2d3be40bd892b8cf353afa6475"` |
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
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:aae75164d165f5a4c0e499d094250b126cb2c634f1f3c5a55226be1fd115c101"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:0a8b103130fe77d9b2a8d6f9ab9e4d69cc7146f7f342b859fdf9ce0c703fed5d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c40d9ce71dce69af2ccfd0c4396f6fcea650358a04107008cfa34ec73e82fc4"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:8167cf7b096bcf02b20dbc95d47de65bf2b7eb2902495b089aae8ad6cc2ffae7"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c808566f31ad17b61c8700c5ecf0e95be4fd01ca4b2edf3bb12f80f4de49255"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c45259baf1db3285bd3b9cb81d1637bfcd7ac34589868894e6ad63ee93577a0a"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c60be35d2fffdab2e6c81834408613d778914041c0ecd3f4a0f5be53541dc7bd"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:27864c18901ea515a772984044b552f7cb3a0d2a058bd1a67a9b53dc49c4ab5d"` |

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
| `["scope"]["dataset_versions"]` | `["hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"]` |
| `["scope"]["denominator_basis"]` | `"all_valid_records_in_selected_dataset_scope"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"hmac-sha256:41c8e31c7545a4277beda762e2ba57b6a564fa2d3be40bd892b8cf353afa6475"` |
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
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:aae75164d165f5a4c0e499d094250b126cb2c634f1f3c5a55226be1fd115c101"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:0a8b103130fe77d9b2a8d6f9ab9e4d69cc7146f7f342b859fdf9ce0c703fed5d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c40d9ce71dce69af2ccfd0c4396f6fcea650358a04107008cfa34ec73e82fc4"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:8167cf7b096bcf02b20dbc95d47de65bf2b7eb2902495b089aae8ad6cc2ffae7"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c808566f31ad17b61c8700c5ecf0e95be4fd01ca4b2edf3bb12f80f4de49255"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c45259baf1db3285bd3b9cb81d1637bfcd7ac34589868894e6ad63ee93577a0a"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c60be35d2fffdab2e6c81834408613d778914041c0ecd3f4a0f5be53541dc7bd"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:27864c18901ea515a772984044b552f7cb3a0d2a058bd1a67a9b53dc49c4ab5d"` |

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
| `["scope"]["dataset_versions"]` | `["hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"]` |
| `["scope"]["denominator_basis"]` | `"all_valid_records_in_selected_dataset_scope"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"hmac-sha256:41c8e31c7545a4277beda762e2ba57b6a564fa2d3be40bd892b8cf353afa6475"` |
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
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:aae75164d165f5a4c0e499d094250b126cb2c634f1f3c5a55226be1fd115c101"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:0a8b103130fe77d9b2a8d6f9ab9e4d69cc7146f7f342b859fdf9ce0c703fed5d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c40d9ce71dce69af2ccfd0c4396f6fcea650358a04107008cfa34ec73e82fc4"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:8167cf7b096bcf02b20dbc95d47de65bf2b7eb2902495b089aae8ad6cc2ffae7"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c808566f31ad17b61c8700c5ecf0e95be4fd01ca4b2edf3bb12f80f4de49255"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c45259baf1db3285bd3b9cb81d1637bfcd7ac34589868894e6ad63ee93577a0a"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c60be35d2fffdab2e6c81834408613d778914041c0ecd3f4a0f5be53541dc7bd"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:27864c18901ea515a772984044b552f7cb3a0d2a058bd1a67a9b53dc49c4ab5d"` |

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
| `["scope"]["dataset_versions"]` | `["hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"]` |
| `["scope"]["denominator_basis"]` | `"all_valid_records_in_selected_dataset_scope"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"hmac-sha256:41c8e31c7545a4277beda762e2ba57b6a564fa2d3be40bd892b8cf353afa6475"` |
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
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:aae75164d165f5a4c0e499d094250b126cb2c634f1f3c5a55226be1fd115c101"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:0a8b103130fe77d9b2a8d6f9ab9e4d69cc7146f7f342b859fdf9ce0c703fed5d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c40d9ce71dce69af2ccfd0c4396f6fcea650358a04107008cfa34ec73e82fc4"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:8167cf7b096bcf02b20dbc95d47de65bf2b7eb2902495b089aae8ad6cc2ffae7"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c808566f31ad17b61c8700c5ecf0e95be4fd01ca4b2edf3bb12f80f4de49255"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c45259baf1db3285bd3b9cb81d1637bfcd7ac34589868894e6ad63ee93577a0a"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c60be35d2fffdab2e6c81834408613d778914041c0ecd3f4a0f5be53541dc7bd"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:27864c18901ea515a772984044b552f7cb3a0d2a058bd1a67a9b53dc49c4ab5d"` |

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
| `["scope"]["dataset_versions"]` | `["hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"]` |
| `["scope"]["denominator_basis"]` | `"all_valid_records_in_selected_dataset_scope"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"hmac-sha256:41c8e31c7545a4277beda762e2ba57b6a564fa2d3be40bd892b8cf353afa6475"` |
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
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:aae75164d165f5a4c0e499d094250b126cb2c634f1f3c5a55226be1fd115c101"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:0a8b103130fe77d9b2a8d6f9ab9e4d69cc7146f7f342b859fdf9ce0c703fed5d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c40d9ce71dce69af2ccfd0c4396f6fcea650358a04107008cfa34ec73e82fc4"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:8167cf7b096bcf02b20dbc95d47de65bf2b7eb2902495b089aae8ad6cc2ffae7"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c808566f31ad17b61c8700c5ecf0e95be4fd01ca4b2edf3bb12f80f4de49255"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c45259baf1db3285bd3b9cb81d1637bfcd7ac34589868894e6ad63ee93577a0a"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c60be35d2fffdab2e6c81834408613d778914041c0ecd3f4a0f5be53541dc7bd"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:27864c18901ea515a772984044b552f7cb3a0d2a058bd1a67a9b53dc49c4ab5d"` |

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
| `["scope"]["dataset_versions"]` | `["hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"]` |
| `["scope"]["denominator_basis"]` | `"all_valid_records_in_selected_dataset_scope"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"hmac-sha256:41c8e31c7545a4277beda762e2ba57b6a564fa2d3be40bd892b8cf353afa6475"` |
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
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:aae75164d165f5a4c0e499d094250b126cb2c634f1f3c5a55226be1fd115c101"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:0a8b103130fe77d9b2a8d6f9ab9e4d69cc7146f7f342b859fdf9ce0c703fed5d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c40d9ce71dce69af2ccfd0c4396f6fcea650358a04107008cfa34ec73e82fc4"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:8167cf7b096bcf02b20dbc95d47de65bf2b7eb2902495b089aae8ad6cc2ffae7"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c808566f31ad17b61c8700c5ecf0e95be4fd01ca4b2edf3bb12f80f4de49255"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c45259baf1db3285bd3b9cb81d1637bfcd7ac34589868894e6ad63ee93577a0a"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c60be35d2fffdab2e6c81834408613d778914041c0ecd3f4a0f5be53541dc7bd"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:27864c18901ea515a772984044b552f7cb3a0d2a058bd1a67a9b53dc49c4ab5d"` |

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
| `["scope"]["dataset_versions"]` | `["hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"]` |
| `["scope"]["denominator_basis"]` | `"all_valid_records_in_selected_dataset_scope"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"hmac-sha256:41c8e31c7545a4277beda762e2ba57b6a564fa2d3be40bd892b8cf353afa6475"` |
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
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:aae75164d165f5a4c0e499d094250b126cb2c634f1f3c5a55226be1fd115c101"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:0a8b103130fe77d9b2a8d6f9ab9e4d69cc7146f7f342b859fdf9ce0c703fed5d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c40d9ce71dce69af2ccfd0c4396f6fcea650358a04107008cfa34ec73e82fc4"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:8167cf7b096bcf02b20dbc95d47de65bf2b7eb2902495b089aae8ad6cc2ffae7"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c808566f31ad17b61c8700c5ecf0e95be4fd01ca4b2edf3bb12f80f4de49255"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c45259baf1db3285bd3b9cb81d1637bfcd7ac34589868894e6ad63ee93577a0a"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c60be35d2fffdab2e6c81834408613d778914041c0ecd3f4a0f5be53541dc7bd"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:27864c18901ea515a772984044b552f7cb3a0d2a058bd1a67a9b53dc49c4ab5d"` |

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
| `["scope"]["dataset_versions"]` | `["hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"]` |
| `["scope"]["denominator_basis"]` | `"all_valid_records_in_selected_dataset_scope"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"hmac-sha256:41c8e31c7545a4277beda762e2ba57b6a564fa2d3be40bd892b8cf353afa6475"` |
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
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:aae75164d165f5a4c0e499d094250b126cb2c634f1f3c5a55226be1fd115c101"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:0a8b103130fe77d9b2a8d6f9ab9e4d69cc7146f7f342b859fdf9ce0c703fed5d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c40d9ce71dce69af2ccfd0c4396f6fcea650358a04107008cfa34ec73e82fc4"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:8167cf7b096bcf02b20dbc95d47de65bf2b7eb2902495b089aae8ad6cc2ffae7"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c808566f31ad17b61c8700c5ecf0e95be4fd01ca4b2edf3bb12f80f4de49255"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c45259baf1db3285bd3b9cb81d1637bfcd7ac34589868894e6ad63ee93577a0a"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c60be35d2fffdab2e6c81834408613d778914041c0ecd3f4a0f5be53541dc7bd"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:27864c18901ea515a772984044b552f7cb3a0d2a058bd1a67a9b53dc49c4ab5d"` |

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
| `["scope"]["dataset_versions"]` | `["hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"]` |
| `["scope"]["denominator_basis"]` | `"all_valid_records_in_selected_dataset_scope"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"hmac-sha256:41c8e31c7545a4277beda762e2ba57b6a564fa2d3be40bd892b8cf353afa6475"` |
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
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:aae75164d165f5a4c0e499d094250b126cb2c634f1f3c5a55226be1fd115c101"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:0a8b103130fe77d9b2a8d6f9ab9e4d69cc7146f7f342b859fdf9ce0c703fed5d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c40d9ce71dce69af2ccfd0c4396f6fcea650358a04107008cfa34ec73e82fc4"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:8167cf7b096bcf02b20dbc95d47de65bf2b7eb2902495b089aae8ad6cc2ffae7"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c808566f31ad17b61c8700c5ecf0e95be4fd01ca4b2edf3bb12f80f4de49255"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c45259baf1db3285bd3b9cb81d1637bfcd7ac34589868894e6ad63ee93577a0a"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c60be35d2fffdab2e6c81834408613d778914041c0ecd3f4a0f5be53541dc7bd"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:27864c18901ea515a772984044b552f7cb3a0d2a058bd1a67a9b53dc49c4ab5d"` |

### Analytical result

`["observed_facts"]["record_counts"]["hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"]`

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
| `["scope"]["dataset_versions"]` | `["hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"]` |
| `["scope"]["denominator_basis"]` | `"validated_records_in_version"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"hmac-sha256:f91f97dd16048a4640ee459ea5fe334d4ca5d31dad27c79f9203c28006ae64f5"` |
| `["status"]` | `"available"` |
| `["theory_map_ids"]` | `[]` |
| `["trace_ids"]` | `[]` |
| `["unit"]` | `"records"` |
| `["value"]` | 8 |

**`["scope"]["included_record_keys"]`**

| `"dataset_version"` | `"record_id"` |
|---|---|
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:a130e0b7f4696e3bc1ed555d0170b426ca57c7efed97c9c27766355dd842ec1c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:6da9164abc2800aec9b384c96483bc3bc128008df04704ad7050851f8b3f9a2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:52d7e4984062cff58f5ee2ab4592f4174277c11213b23be0f66b0da6c2801b15"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:b09664f79e8df7595b88db8e5d4fd40a678384e2b4816e04044a63b901c6dc3d"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:18eea61d82b38372f77e43b8596c93ef577d554d1cb4dba3545cd509026b1c2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:d829ae28c8f6422156149b7d293896efb88703427b4b31d13996703e67d35aae"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:41770f394bc6316c571ecb74ac4e07554113bb8f92d0c56603009a81daeeff12"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:3913f4a00a32e7b06211da44f3d156e37509bf8aefde1ba61f221717eaae8c8d"` |

### Analytical result

`["observed_facts"]["record_counts"]["hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"]`

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
| `["scope"]["dataset_versions"]` | `["hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"]` |
| `["scope"]["denominator_basis"]` | `"validated_records_in_version"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"hmac-sha256:5bf9b0396ebb8414a0bef2f30f4d9386e32bda5202861477002e23404c70dc12"` |
| `["status"]` | `"available"` |
| `["theory_map_ids"]` | `[]` |
| `["trace_ids"]` | `[]` |
| `["unit"]` | `"records"` |
| `["value"]` | 8 |

**`["scope"]["included_record_keys"]`**

| `"dataset_version"` | `"record_id"` |
|---|---|
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:aae75164d165f5a4c0e499d094250b126cb2c634f1f3c5a55226be1fd115c101"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:0a8b103130fe77d9b2a8d6f9ab9e4d69cc7146f7f342b859fdf9ce0c703fed5d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c40d9ce71dce69af2ccfd0c4396f6fcea650358a04107008cfa34ec73e82fc4"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:8167cf7b096bcf02b20dbc95d47de65bf2b7eb2902495b089aae8ad6cc2ffae7"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c808566f31ad17b61c8700c5ecf0e95be4fd01ca4b2edf3bb12f80f4de49255"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c45259baf1db3285bd3b9cb81d1637bfcd7ac34589868894e6ad63ee93577a0a"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c60be35d2fffdab2e6c81834408613d778914041c0ecd3f4a0f5be53541dc7bd"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:27864c18901ea515a772984044b552f7cb3a0d2a058bd1a67a9b53dc49c4ab5d"` |

### Analytical result

`["observed_facts"]["state_counts"]["by_version"]["hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"]`

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
| `["representation"]["binning_or_mapping_rule"]` | `"hmac-sha256:18da0fd476e3b47330cd178d9efef7c39c415771e8f8bd5cb6a7f13e9681a9b3"` |
| `["representation"]["field_name"]` | `"hmac-sha256:47e6ffdde83ab627afa8a2c8617571bf1cf11f84faf6415e021a437406b58765"` |
| `["representation"]["missing_state_id"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["missing_value_policy"]` | `"error"` |
| `["representation"]["normalization_profile"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["representation_name"]` | `"hmac-sha256:220b787af129ef50eab4ee9f3c90a00a7bce0a525c6e49bfc40fe9bb8af1d0b8"` |
| `["representation"]["representation_source"]` | `"hmac-sha256:1faa75c58dd3f727bec66d81de5cab7c2e64afbebcd03c32653ba5432a5c4369"` |
| `["representation"]["representation_version"]` | `"hmac-sha256:b6d6724490a6778f4b6e234f43fff3602f2707d6b9ab74acb0cc8e83c96d3da8"` |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"]` |
| `["scope"]["denominator_basis"]` | `"included_representation_records"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["exclusions"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"hmac-sha256:e8d3d329142ddbec8c51b0affa3d8ade12402bebc6e9d4b1e2a994e17ed56f05"` |
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
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:a130e0b7f4696e3bc1ed555d0170b426ca57c7efed97c9c27766355dd842ec1c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:6da9164abc2800aec9b384c96483bc3bc128008df04704ad7050851f8b3f9a2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:52d7e4984062cff58f5ee2ab4592f4174277c11213b23be0f66b0da6c2801b15"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:b09664f79e8df7595b88db8e5d4fd40a678384e2b4816e04044a63b901c6dc3d"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:18eea61d82b38372f77e43b8596c93ef577d554d1cb4dba3545cd509026b1c2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:d829ae28c8f6422156149b7d293896efb88703427b4b31d13996703e67d35aae"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:41770f394bc6316c571ecb74ac4e07554113bb8f92d0c56603009a81daeeff12"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:3913f4a00a32e7b06211da44f3d156e37509bf8aefde1ba61f221717eaae8c8d"` |

**`["value"]`**

| `"state_count"` | `"state_id"` |
|---|---|
| 1 | `"hmac-sha256:f130effa18aee11b975751d07fec071c7ebe83aa6d8210757e5ec8615b3108a7"` |
| 1 | `"hmac-sha256:65497bf5eab3b43cfbca481d2fd21635c2c9e701c962aed90ab94eff7e76f62d"` |
| 1 | `"hmac-sha256:9b4818bf9968505a3e9dc65c9f4f3210f99fb91600ce7bcbef1f77e7ed626250"` |
| 1 | `"hmac-sha256:fac7b92af75bb73c87cf215ab7489fac158c8e431c07eea0fc45df31c09d5233"` |
| 1 | `"hmac-sha256:c26a74b0b747e213a83215b0fc9f25f7a8880a232796267c3bbd849205106edc"` |
| 1 | `"hmac-sha256:cce2bc33c7dd4c9eb9222b63c7781aeaf97698fcab3d9f1838dc70d8b75fe210"` |
| 1 | `"hmac-sha256:51607e4e3a5be5845e6b4f520a9d0a1599f5e00a2989fb7ed2dfb5339b44e32a"` |
| 1 | `"hmac-sha256:1cd134c257cbcb62c641a411712154ed9e5e5c0119fef89ebd98d7b33a90c159"` |

### Analytical result

`["observed_facts"]["state_counts"]["by_version"]["hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"]`

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
| `["representation"]["binning_or_mapping_rule"]` | `"hmac-sha256:18da0fd476e3b47330cd178d9efef7c39c415771e8f8bd5cb6a7f13e9681a9b3"` |
| `["representation"]["field_name"]` | `"hmac-sha256:47e6ffdde83ab627afa8a2c8617571bf1cf11f84faf6415e021a437406b58765"` |
| `["representation"]["missing_state_id"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["missing_value_policy"]` | `"error"` |
| `["representation"]["normalization_profile"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["representation_name"]` | `"hmac-sha256:220b787af129ef50eab4ee9f3c90a00a7bce0a525c6e49bfc40fe9bb8af1d0b8"` |
| `["representation"]["representation_source"]` | `"hmac-sha256:1faa75c58dd3f727bec66d81de5cab7c2e64afbebcd03c32653ba5432a5c4369"` |
| `["representation"]["representation_version"]` | `"hmac-sha256:b6d6724490a6778f4b6e234f43fff3602f2707d6b9ab74acb0cc8e83c96d3da8"` |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"]` |
| `["scope"]["denominator_basis"]` | `"included_representation_records"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["exclusions"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"hmac-sha256:62f240a66b38ae21fd6453c60b78d6ee2712c8ef1933c6c15983da3e393cbffc"` |
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
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:aae75164d165f5a4c0e499d094250b126cb2c634f1f3c5a55226be1fd115c101"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:0a8b103130fe77d9b2a8d6f9ab9e4d69cc7146f7f342b859fdf9ce0c703fed5d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c40d9ce71dce69af2ccfd0c4396f6fcea650358a04107008cfa34ec73e82fc4"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:8167cf7b096bcf02b20dbc95d47de65bf2b7eb2902495b089aae8ad6cc2ffae7"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c808566f31ad17b61c8700c5ecf0e95be4fd01ca4b2edf3bb12f80f4de49255"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c45259baf1db3285bd3b9cb81d1637bfcd7ac34589868894e6ad63ee93577a0a"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c60be35d2fffdab2e6c81834408613d778914041c0ecd3f4a0f5be53541dc7bd"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:27864c18901ea515a772984044b552f7cb3a0d2a058bd1a67a9b53dc49c4ab5d"` |

**`["value"]`**

| `"state_count"` | `"state_id"` |
|---|---|
| 1 | `"hmac-sha256:65497bf5eab3b43cfbca481d2fd21635c2c9e701c962aed90ab94eff7e76f62d"` |
| 3 | `"hmac-sha256:9b4818bf9968505a3e9dc65c9f4f3210f99fb91600ce7bcbef1f77e7ed626250"` |
| 2 | `"hmac-sha256:fac7b92af75bb73c87cf215ab7489fac158c8e431c07eea0fc45df31c09d5233"` |
| 1 | `"hmac-sha256:c26a74b0b747e213a83215b0fc9f25f7a8880a232796267c3bbd849205106edc"` |
| 1 | `"hmac-sha256:51607e4e3a5be5845e6b4f520a9d0a1599f5e00a2989fb7ed2dfb5339b44e32a"` |

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
| `["scope"]["dataset_versions"]` | `["hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"]` |
| `["scope"]["denominator_basis"]` | `"all_valid_records_in_selected_dataset_scope"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"hmac-sha256:41c8e31c7545a4277beda762e2ba57b6a564fa2d3be40bd892b8cf353afa6475"` |
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
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:aae75164d165f5a4c0e499d094250b126cb2c634f1f3c5a55226be1fd115c101"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:0a8b103130fe77d9b2a8d6f9ab9e4d69cc7146f7f342b859fdf9ce0c703fed5d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c40d9ce71dce69af2ccfd0c4396f6fcea650358a04107008cfa34ec73e82fc4"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:8167cf7b096bcf02b20dbc95d47de65bf2b7eb2902495b089aae8ad6cc2ffae7"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c808566f31ad17b61c8700c5ecf0e95be4fd01ca4b2edf3bb12f80f4de49255"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c45259baf1db3285bd3b9cb81d1637bfcd7ac34589868894e6ad63ee93577a0a"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c60be35d2fffdab2e6c81834408613d778914041c0ecd3f4a0f5be53541dc7bd"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:27864c18901ea515a772984044b552f7cb3a0d2a058bd1a67a9b53dc49c4ab5d"` |

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
| `["scope"]["dataset_versions"]` | `["hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"]` |
| `["scope"]["denominator_basis"]` | `"all_valid_records_in_selected_dataset_scope"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"hmac-sha256:41c8e31c7545a4277beda762e2ba57b6a564fa2d3be40bd892b8cf353afa6475"` |
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
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:aae75164d165f5a4c0e499d094250b126cb2c634f1f3c5a55226be1fd115c101"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:0a8b103130fe77d9b2a8d6f9ab9e4d69cc7146f7f342b859fdf9ce0c703fed5d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c40d9ce71dce69af2ccfd0c4396f6fcea650358a04107008cfa34ec73e82fc4"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:8167cf7b096bcf02b20dbc95d47de65bf2b7eb2902495b089aae8ad6cc2ffae7"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c808566f31ad17b61c8700c5ecf0e95be4fd01ca4b2edf3bb12f80f4de49255"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c45259baf1db3285bd3b9cb81d1637bfcd7ac34589868894e6ad63ee93577a0a"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c60be35d2fffdab2e6c81834408613d778914041c0ecd3f4a0f5be53541dc7bd"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:27864c18901ea515a772984044b552f7cb3a0d2a058bd1a67a9b53dc49c4ab5d"` |

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
| `["scope"]["dataset_versions"]` | `["hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"]` |
| `["scope"]["denominator_basis"]` | `"all_valid_records_in_selected_dataset_scope"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"hmac-sha256:41c8e31c7545a4277beda762e2ba57b6a564fa2d3be40bd892b8cf353afa6475"` |
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
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:aae75164d165f5a4c0e499d094250b126cb2c634f1f3c5a55226be1fd115c101"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:0a8b103130fe77d9b2a8d6f9ab9e4d69cc7146f7f342b859fdf9ce0c703fed5d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c40d9ce71dce69af2ccfd0c4396f6fcea650358a04107008cfa34ec73e82fc4"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:8167cf7b096bcf02b20dbc95d47de65bf2b7eb2902495b089aae8ad6cc2ffae7"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c808566f31ad17b61c8700c5ecf0e95be4fd01ca4b2edf3bb12f80f4de49255"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c45259baf1db3285bd3b9cb81d1637bfcd7ac34589868894e6ad63ee93577a0a"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c60be35d2fffdab2e6c81834408613d778914041c0ecd3f4a0f5be53541dc7bd"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:27864c18901ea515a772984044b552f7cb3a0d2a058bd1a67a9b53dc49c4ab5d"` |

### Analytical result

`["derived_metrics"]["diversity"]["by_version"]["hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"]["distribution_basis"]`

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
| `["representation"]["binning_or_mapping_rule"]` | `"hmac-sha256:18da0fd476e3b47330cd178d9efef7c39c415771e8f8bd5cb6a7f13e9681a9b3"` |
| `["representation"]["field_name"]` | `"hmac-sha256:47e6ffdde83ab627afa8a2c8617571bf1cf11f84faf6415e021a437406b58765"` |
| `["representation"]["missing_state_id"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["missing_value_policy"]` | `"error"` |
| `["representation"]["normalization_profile"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["representation_name"]` | `"hmac-sha256:220b787af129ef50eab4ee9f3c90a00a7bce0a525c6e49bfc40fe9bb8af1d0b8"` |
| `["representation"]["representation_source"]` | `"hmac-sha256:1faa75c58dd3f727bec66d81de5cab7c2e64afbebcd03c32653ba5432a5c4369"` |
| `["representation"]["representation_version"]` | `"hmac-sha256:b6d6724490a6778f4b6e234f43fff3602f2707d6b9ab74acb0cc8e83c96d3da8"` |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"]` |
| `["scope"]["denominator_basis"]` | `"included_representation_records"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["exclusions"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"hmac-sha256:e8d3d329142ddbec8c51b0affa3d8ade12402bebc6e9d4b1e2a994e17ed56f05"` |
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
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:a130e0b7f4696e3bc1ed555d0170b426ca57c7efed97c9c27766355dd842ec1c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:6da9164abc2800aec9b384c96483bc3bc128008df04704ad7050851f8b3f9a2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:52d7e4984062cff58f5ee2ab4592f4174277c11213b23be0f66b0da6c2801b15"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:b09664f79e8df7595b88db8e5d4fd40a678384e2b4816e04044a63b901c6dc3d"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:18eea61d82b38372f77e43b8596c93ef577d554d1cb4dba3545cd509026b1c2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:d829ae28c8f6422156149b7d293896efb88703427b4b31d13996703e67d35aae"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:41770f394bc6316c571ecb74ac4e07554113bb8f92d0c56603009a81daeeff12"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:3913f4a00a32e7b06211da44f3d156e37509bf8aefde1ba61f221717eaae8c8d"` |

### Analytical result

`["derived_metrics"]["diversity"]["by_version"]["hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"]["gini_simpson_diversity"]`

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
| `["representation"]["binning_or_mapping_rule"]` | `"hmac-sha256:18da0fd476e3b47330cd178d9efef7c39c415771e8f8bd5cb6a7f13e9681a9b3"` |
| `["representation"]["field_name"]` | `"hmac-sha256:47e6ffdde83ab627afa8a2c8617571bf1cf11f84faf6415e021a437406b58765"` |
| `["representation"]["missing_state_id"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["missing_value_policy"]` | `"error"` |
| `["representation"]["normalization_profile"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["representation_name"]` | `"hmac-sha256:220b787af129ef50eab4ee9f3c90a00a7bce0a525c6e49bfc40fe9bb8af1d0b8"` |
| `["representation"]["representation_source"]` | `"hmac-sha256:1faa75c58dd3f727bec66d81de5cab7c2e64afbebcd03c32653ba5432a5c4369"` |
| `["representation"]["representation_version"]` | `"hmac-sha256:b6d6724490a6778f4b6e234f43fff3602f2707d6b9ab74acb0cc8e83c96d3da8"` |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"]` |
| `["scope"]["denominator_basis"]` | `"included_representation_records"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["exclusions"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"hmac-sha256:e8d3d329142ddbec8c51b0affa3d8ade12402bebc6e9d4b1e2a994e17ed56f05"` |
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
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:a130e0b7f4696e3bc1ed555d0170b426ca57c7efed97c9c27766355dd842ec1c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:6da9164abc2800aec9b384c96483bc3bc128008df04704ad7050851f8b3f9a2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:52d7e4984062cff58f5ee2ab4592f4174277c11213b23be0f66b0da6c2801b15"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:b09664f79e8df7595b88db8e5d4fd40a678384e2b4816e04044a63b901c6dc3d"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:18eea61d82b38372f77e43b8596c93ef577d554d1cb4dba3545cd509026b1c2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:d829ae28c8f6422156149b7d293896efb88703427b4b31d13996703e67d35aae"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:41770f394bc6316c571ecb74ac4e07554113bb8f92d0c56603009a81daeeff12"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:3913f4a00a32e7b06211da44f3d156e37509bf8aefde1ba61f221717eaae8c8d"` |

### Analytical result

`["derived_metrics"]["diversity"]["by_version"]["hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"]["simpson_concentration"]`

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
| `["representation"]["binning_or_mapping_rule"]` | `"hmac-sha256:18da0fd476e3b47330cd178d9efef7c39c415771e8f8bd5cb6a7f13e9681a9b3"` |
| `["representation"]["field_name"]` | `"hmac-sha256:47e6ffdde83ab627afa8a2c8617571bf1cf11f84faf6415e021a437406b58765"` |
| `["representation"]["missing_state_id"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["missing_value_policy"]` | `"error"` |
| `["representation"]["normalization_profile"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["representation_name"]` | `"hmac-sha256:220b787af129ef50eab4ee9f3c90a00a7bce0a525c6e49bfc40fe9bb8af1d0b8"` |
| `["representation"]["representation_source"]` | `"hmac-sha256:1faa75c58dd3f727bec66d81de5cab7c2e64afbebcd03c32653ba5432a5c4369"` |
| `["representation"]["representation_version"]` | `"hmac-sha256:b6d6724490a6778f4b6e234f43fff3602f2707d6b9ab74acb0cc8e83c96d3da8"` |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"]` |
| `["scope"]["denominator_basis"]` | `"included_representation_records"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["exclusions"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"hmac-sha256:e8d3d329142ddbec8c51b0affa3d8ade12402bebc6e9d4b1e2a994e17ed56f05"` |
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
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:a130e0b7f4696e3bc1ed555d0170b426ca57c7efed97c9c27766355dd842ec1c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:6da9164abc2800aec9b384c96483bc3bc128008df04704ad7050851f8b3f9a2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:52d7e4984062cff58f5ee2ab4592f4174277c11213b23be0f66b0da6c2801b15"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:b09664f79e8df7595b88db8e5d4fd40a678384e2b4816e04044a63b901c6dc3d"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:18eea61d82b38372f77e43b8596c93ef577d554d1cb4dba3545cd509026b1c2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:d829ae28c8f6422156149b7d293896efb88703427b4b31d13996703e67d35aae"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:41770f394bc6316c571ecb74ac4e07554113bb8f92d0c56603009a81daeeff12"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:3913f4a00a32e7b06211da44f3d156e37509bf8aefde1ba61f221717eaae8c8d"` |

### Analytical result

`["derived_metrics"]["diversity"]["by_version"]["hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"]["state_frequencies"]`

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
| `["representation"]["binning_or_mapping_rule"]` | `"hmac-sha256:18da0fd476e3b47330cd178d9efef7c39c415771e8f8bd5cb6a7f13e9681a9b3"` |
| `["representation"]["field_name"]` | `"hmac-sha256:47e6ffdde83ab627afa8a2c8617571bf1cf11f84faf6415e021a437406b58765"` |
| `["representation"]["missing_state_id"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["missing_value_policy"]` | `"error"` |
| `["representation"]["normalization_profile"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["representation_name"]` | `"hmac-sha256:220b787af129ef50eab4ee9f3c90a00a7bce0a525c6e49bfc40fe9bb8af1d0b8"` |
| `["representation"]["representation_source"]` | `"hmac-sha256:1faa75c58dd3f727bec66d81de5cab7c2e64afbebcd03c32653ba5432a5c4369"` |
| `["representation"]["representation_version"]` | `"hmac-sha256:b6d6724490a6778f4b6e234f43fff3602f2707d6b9ab74acb0cc8e83c96d3da8"` |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"]` |
| `["scope"]["denominator_basis"]` | `"included_representation_records"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["exclusions"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"hmac-sha256:e8d3d329142ddbec8c51b0affa3d8ade12402bebc6e9d4b1e2a994e17ed56f05"` |
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
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:a130e0b7f4696e3bc1ed555d0170b426ca57c7efed97c9c27766355dd842ec1c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:6da9164abc2800aec9b384c96483bc3bc128008df04704ad7050851f8b3f9a2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:52d7e4984062cff58f5ee2ab4592f4174277c11213b23be0f66b0da6c2801b15"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:b09664f79e8df7595b88db8e5d4fd40a678384e2b4816e04044a63b901c6dc3d"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:18eea61d82b38372f77e43b8596c93ef577d554d1cb4dba3545cd509026b1c2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:d829ae28c8f6422156149b7d293896efb88703427b4b31d13996703e67d35aae"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:41770f394bc6316c571ecb74ac4e07554113bb8f92d0c56603009a81daeeff12"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:3913f4a00a32e7b06211da44f3d156e37509bf8aefde1ba61f221717eaae8c8d"` |

**`["value"]`**

| `"state_frequency"` | `"state_id"` |
|---|---|
| 0.125 | `"hmac-sha256:f130effa18aee11b975751d07fec071c7ebe83aa6d8210757e5ec8615b3108a7"` |
| 0.125 | `"hmac-sha256:65497bf5eab3b43cfbca481d2fd21635c2c9e701c962aed90ab94eff7e76f62d"` |
| 0.125 | `"hmac-sha256:9b4818bf9968505a3e9dc65c9f4f3210f99fb91600ce7bcbef1f77e7ed626250"` |
| 0.125 | `"hmac-sha256:fac7b92af75bb73c87cf215ab7489fac158c8e431c07eea0fc45df31c09d5233"` |
| 0.125 | `"hmac-sha256:c26a74b0b747e213a83215b0fc9f25f7a8880a232796267c3bbd849205106edc"` |
| 0.125 | `"hmac-sha256:cce2bc33c7dd4c9eb9222b63c7781aeaf97698fcab3d9f1838dc70d8b75fe210"` |
| 0.125 | `"hmac-sha256:51607e4e3a5be5845e6b4f520a9d0a1599f5e00a2989fb7ed2dfb5339b44e32a"` |
| 0.125 | `"hmac-sha256:1cd134c257cbcb62c641a411712154ed9e5e5c0119fef89ebd98d7b33a90c159"` |

### Analytical result

`["derived_metrics"]["diversity"]["by_version"]["hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"]["distribution_basis"]`

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
| `["representation"]["binning_or_mapping_rule"]` | `"hmac-sha256:18da0fd476e3b47330cd178d9efef7c39c415771e8f8bd5cb6a7f13e9681a9b3"` |
| `["representation"]["field_name"]` | `"hmac-sha256:47e6ffdde83ab627afa8a2c8617571bf1cf11f84faf6415e021a437406b58765"` |
| `["representation"]["missing_state_id"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["missing_value_policy"]` | `"error"` |
| `["representation"]["normalization_profile"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["representation_name"]` | `"hmac-sha256:220b787af129ef50eab4ee9f3c90a00a7bce0a525c6e49bfc40fe9bb8af1d0b8"` |
| `["representation"]["representation_source"]` | `"hmac-sha256:1faa75c58dd3f727bec66d81de5cab7c2e64afbebcd03c32653ba5432a5c4369"` |
| `["representation"]["representation_version"]` | `"hmac-sha256:b6d6724490a6778f4b6e234f43fff3602f2707d6b9ab74acb0cc8e83c96d3da8"` |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"]` |
| `["scope"]["denominator_basis"]` | `"included_representation_records"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["exclusions"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"hmac-sha256:62f240a66b38ae21fd6453c60b78d6ee2712c8ef1933c6c15983da3e393cbffc"` |
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
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:aae75164d165f5a4c0e499d094250b126cb2c634f1f3c5a55226be1fd115c101"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:0a8b103130fe77d9b2a8d6f9ab9e4d69cc7146f7f342b859fdf9ce0c703fed5d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c40d9ce71dce69af2ccfd0c4396f6fcea650358a04107008cfa34ec73e82fc4"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:8167cf7b096bcf02b20dbc95d47de65bf2b7eb2902495b089aae8ad6cc2ffae7"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c808566f31ad17b61c8700c5ecf0e95be4fd01ca4b2edf3bb12f80f4de49255"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c45259baf1db3285bd3b9cb81d1637bfcd7ac34589868894e6ad63ee93577a0a"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c60be35d2fffdab2e6c81834408613d778914041c0ecd3f4a0f5be53541dc7bd"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:27864c18901ea515a772984044b552f7cb3a0d2a058bd1a67a9b53dc49c4ab5d"` |

### Analytical result

`["derived_metrics"]["diversity"]["by_version"]["hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"]["gini_simpson_diversity"]`

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
| `["representation"]["binning_or_mapping_rule"]` | `"hmac-sha256:18da0fd476e3b47330cd178d9efef7c39c415771e8f8bd5cb6a7f13e9681a9b3"` |
| `["representation"]["field_name"]` | `"hmac-sha256:47e6ffdde83ab627afa8a2c8617571bf1cf11f84faf6415e021a437406b58765"` |
| `["representation"]["missing_state_id"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["missing_value_policy"]` | `"error"` |
| `["representation"]["normalization_profile"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["representation_name"]` | `"hmac-sha256:220b787af129ef50eab4ee9f3c90a00a7bce0a525c6e49bfc40fe9bb8af1d0b8"` |
| `["representation"]["representation_source"]` | `"hmac-sha256:1faa75c58dd3f727bec66d81de5cab7c2e64afbebcd03c32653ba5432a5c4369"` |
| `["representation"]["representation_version"]` | `"hmac-sha256:b6d6724490a6778f4b6e234f43fff3602f2707d6b9ab74acb0cc8e83c96d3da8"` |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"]` |
| `["scope"]["denominator_basis"]` | `"included_representation_records"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["exclusions"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"hmac-sha256:62f240a66b38ae21fd6453c60b78d6ee2712c8ef1933c6c15983da3e393cbffc"` |
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
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:aae75164d165f5a4c0e499d094250b126cb2c634f1f3c5a55226be1fd115c101"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:0a8b103130fe77d9b2a8d6f9ab9e4d69cc7146f7f342b859fdf9ce0c703fed5d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c40d9ce71dce69af2ccfd0c4396f6fcea650358a04107008cfa34ec73e82fc4"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:8167cf7b096bcf02b20dbc95d47de65bf2b7eb2902495b089aae8ad6cc2ffae7"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c808566f31ad17b61c8700c5ecf0e95be4fd01ca4b2edf3bb12f80f4de49255"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c45259baf1db3285bd3b9cb81d1637bfcd7ac34589868894e6ad63ee93577a0a"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c60be35d2fffdab2e6c81834408613d778914041c0ecd3f4a0f5be53541dc7bd"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:27864c18901ea515a772984044b552f7cb3a0d2a058bd1a67a9b53dc49c4ab5d"` |

### Analytical result

`["derived_metrics"]["diversity"]["by_version"]["hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"]["simpson_concentration"]`

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
| `["representation"]["binning_or_mapping_rule"]` | `"hmac-sha256:18da0fd476e3b47330cd178d9efef7c39c415771e8f8bd5cb6a7f13e9681a9b3"` |
| `["representation"]["field_name"]` | `"hmac-sha256:47e6ffdde83ab627afa8a2c8617571bf1cf11f84faf6415e021a437406b58765"` |
| `["representation"]["missing_state_id"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["missing_value_policy"]` | `"error"` |
| `["representation"]["normalization_profile"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["representation_name"]` | `"hmac-sha256:220b787af129ef50eab4ee9f3c90a00a7bce0a525c6e49bfc40fe9bb8af1d0b8"` |
| `["representation"]["representation_source"]` | `"hmac-sha256:1faa75c58dd3f727bec66d81de5cab7c2e64afbebcd03c32653ba5432a5c4369"` |
| `["representation"]["representation_version"]` | `"hmac-sha256:b6d6724490a6778f4b6e234f43fff3602f2707d6b9ab74acb0cc8e83c96d3da8"` |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"]` |
| `["scope"]["denominator_basis"]` | `"included_representation_records"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["exclusions"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"hmac-sha256:62f240a66b38ae21fd6453c60b78d6ee2712c8ef1933c6c15983da3e393cbffc"` |
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
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:aae75164d165f5a4c0e499d094250b126cb2c634f1f3c5a55226be1fd115c101"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:0a8b103130fe77d9b2a8d6f9ab9e4d69cc7146f7f342b859fdf9ce0c703fed5d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c40d9ce71dce69af2ccfd0c4396f6fcea650358a04107008cfa34ec73e82fc4"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:8167cf7b096bcf02b20dbc95d47de65bf2b7eb2902495b089aae8ad6cc2ffae7"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c808566f31ad17b61c8700c5ecf0e95be4fd01ca4b2edf3bb12f80f4de49255"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c45259baf1db3285bd3b9cb81d1637bfcd7ac34589868894e6ad63ee93577a0a"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c60be35d2fffdab2e6c81834408613d778914041c0ecd3f4a0f5be53541dc7bd"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:27864c18901ea515a772984044b552f7cb3a0d2a058bd1a67a9b53dc49c4ab5d"` |

### Analytical result

`["derived_metrics"]["diversity"]["by_version"]["hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"]["state_frequencies"]`

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
| `["representation"]["binning_or_mapping_rule"]` | `"hmac-sha256:18da0fd476e3b47330cd178d9efef7c39c415771e8f8bd5cb6a7f13e9681a9b3"` |
| `["representation"]["field_name"]` | `"hmac-sha256:47e6ffdde83ab627afa8a2c8617571bf1cf11f84faf6415e021a437406b58765"` |
| `["representation"]["missing_state_id"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["missing_value_policy"]` | `"error"` |
| `["representation"]["normalization_profile"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["representation_name"]` | `"hmac-sha256:220b787af129ef50eab4ee9f3c90a00a7bce0a525c6e49bfc40fe9bb8af1d0b8"` |
| `["representation"]["representation_source"]` | `"hmac-sha256:1faa75c58dd3f727bec66d81de5cab7c2e64afbebcd03c32653ba5432a5c4369"` |
| `["representation"]["representation_version"]` | `"hmac-sha256:b6d6724490a6778f4b6e234f43fff3602f2707d6b9ab74acb0cc8e83c96d3da8"` |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"]` |
| `["scope"]["denominator_basis"]` | `"included_representation_records"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["exclusions"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"hmac-sha256:62f240a66b38ae21fd6453c60b78d6ee2712c8ef1933c6c15983da3e393cbffc"` |
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
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:aae75164d165f5a4c0e499d094250b126cb2c634f1f3c5a55226be1fd115c101"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:0a8b103130fe77d9b2a8d6f9ab9e4d69cc7146f7f342b859fdf9ce0c703fed5d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c40d9ce71dce69af2ccfd0c4396f6fcea650358a04107008cfa34ec73e82fc4"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:8167cf7b096bcf02b20dbc95d47de65bf2b7eb2902495b089aae8ad6cc2ffae7"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c808566f31ad17b61c8700c5ecf0e95be4fd01ca4b2edf3bb12f80f4de49255"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c45259baf1db3285bd3b9cb81d1637bfcd7ac34589868894e6ad63ee93577a0a"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c60be35d2fffdab2e6c81834408613d778914041c0ecd3f4a0f5be53541dc7bd"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:27864c18901ea515a772984044b552f7cb3a0d2a058bd1a67a9b53dc49c4ab5d"` |

**`["value"]`**

| `"state_frequency"` | `"state_id"` |
|---|---|
| 0.125 | `"hmac-sha256:65497bf5eab3b43cfbca481d2fd21635c2c9e701c962aed90ab94eff7e76f62d"` |
| 0.375 | `"hmac-sha256:9b4818bf9968505a3e9dc65c9f4f3210f99fb91600ce7bcbef1f77e7ed626250"` |
| 0.25 | `"hmac-sha256:fac7b92af75bb73c87cf215ab7489fac158c8e431c07eea0fc45df31c09d5233"` |
| 0.125 | `"hmac-sha256:c26a74b0b747e213a83215b0fc9f25f7a8880a232796267c3bbd849205106edc"` |
| 0.125 | `"hmac-sha256:51607e4e3a5be5845e6b4f520a9d0a1599f5e00a2989fb7ed2dfb5339b44e32a"` |

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
| `["representation"]["binning_or_mapping_rule"]` | `"hmac-sha256:18da0fd476e3b47330cd178d9efef7c39c415771e8f8bd5cb6a7f13e9681a9b3"` |
| `["representation"]["field_name"]` | `"hmac-sha256:47e6ffdde83ab627afa8a2c8617571bf1cf11f84faf6415e021a437406b58765"` |
| `["representation"]["missing_state_id"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["missing_value_policy"]` | `"error"` |
| `["representation"]["normalization_profile"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["representation_name"]` | `"hmac-sha256:220b787af129ef50eab4ee9f3c90a00a7bce0a525c6e49bfc40fe9bb8af1d0b8"` |
| `["representation"]["representation_source"]` | `"hmac-sha256:1faa75c58dd3f727bec66d81de5cab7c2e64afbebcd03c32653ba5432a5c4369"` |
| `["representation"]["representation_version"]` | `"hmac-sha256:b6d6724490a6778f4b6e234f43fff3602f2707d6b9ab74acb0cc8e83c96d3da8"` |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4", "hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"]` |
| `["scope"]["denominator_basis"]` | `"separate_ordered_representation_scopes"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 16 |
| `["scope"]["scope_id"]` | `"hmac-sha256:565dbad623917e17596723cd5a3913a687c595118c10dfc2472c88f31282765f"` |
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
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:a130e0b7f4696e3bc1ed555d0170b426ca57c7efed97c9c27766355dd842ec1c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:6da9164abc2800aec9b384c96483bc3bc128008df04704ad7050851f8b3f9a2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:52d7e4984062cff58f5ee2ab4592f4174277c11213b23be0f66b0da6c2801b15"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:b09664f79e8df7595b88db8e5d4fd40a678384e2b4816e04044a63b901c6dc3d"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:18eea61d82b38372f77e43b8596c93ef577d554d1cb4dba3545cd509026b1c2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:d829ae28c8f6422156149b7d293896efb88703427b4b31d13996703e67d35aae"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:41770f394bc6316c571ecb74ac4e07554113bb8f92d0c56603009a81daeeff12"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:3913f4a00a32e7b06211da44f3d156e37509bf8aefde1ba61f221717eaae8c8d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:aae75164d165f5a4c0e499d094250b126cb2c634f1f3c5a55226be1fd115c101"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:0a8b103130fe77d9b2a8d6f9ab9e4d69cc7146f7f342b859fdf9ce0c703fed5d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c40d9ce71dce69af2ccfd0c4396f6fcea650358a04107008cfa34ec73e82fc4"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:8167cf7b096bcf02b20dbc95d47de65bf2b7eb2902495b089aae8ad6cc2ffae7"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c808566f31ad17b61c8700c5ecf0e95be4fd01ca4b2edf3bb12f80f4de49255"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c45259baf1db3285bd3b9cb81d1637bfcd7ac34589868894e6ad63ee93577a0a"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c60be35d2fffdab2e6c81834408613d778914041c0ecd3f4a0f5be53541dc7bd"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:27864c18901ea515a772984044b552f7cb3a0d2a058bd1a67a9b53dc49c4ab5d"` |

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
| `["scope"]["dataset_versions"]` | `["hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4", "hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"]` |
| `["scope"]["denominator_basis"]` | `"all_validated_bundle_records"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 16 |
| `["scope"]["scope_id"]` | `"hmac-sha256:fe3080b69d042a9eca2d392f8429412803f06dd3eb9e71fd16178d05e5971ac3"` |
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
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:a130e0b7f4696e3bc1ed555d0170b426ca57c7efed97c9c27766355dd842ec1c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:6da9164abc2800aec9b384c96483bc3bc128008df04704ad7050851f8b3f9a2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:52d7e4984062cff58f5ee2ab4592f4174277c11213b23be0f66b0da6c2801b15"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:b09664f79e8df7595b88db8e5d4fd40a678384e2b4816e04044a63b901c6dc3d"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:18eea61d82b38372f77e43b8596c93ef577d554d1cb4dba3545cd509026b1c2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:d829ae28c8f6422156149b7d293896efb88703427b4b31d13996703e67d35aae"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:41770f394bc6316c571ecb74ac4e07554113bb8f92d0c56603009a81daeeff12"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:3913f4a00a32e7b06211da44f3d156e37509bf8aefde1ba61f221717eaae8c8d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:aae75164d165f5a4c0e499d094250b126cb2c634f1f3c5a55226be1fd115c101"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:0a8b103130fe77d9b2a8d6f9ab9e4d69cc7146f7f342b859fdf9ce0c703fed5d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c40d9ce71dce69af2ccfd0c4396f6fcea650358a04107008cfa34ec73e82fc4"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:8167cf7b096bcf02b20dbc95d47de65bf2b7eb2902495b089aae8ad6cc2ffae7"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c808566f31ad17b61c8700c5ecf0e95be4fd01ca4b2edf3bb12f80f4de49255"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c45259baf1db3285bd3b9cb81d1637bfcd7ac34589868894e6ad63ee93577a0a"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c60be35d2fffdab2e6c81834408613d778914041c0ecd3f4a0f5be53541dc7bd"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:27864c18901ea515a772984044b552f7cb3a0d2a058bd1a67a9b53dc49c4ab5d"` |

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
| `["scope"]["dataset_versions"]` | `["hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"]` |
| `["scope"]["denominator_basis"]` | `"all_valid_records_in_selected_dataset_scope"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"hmac-sha256:41c8e31c7545a4277beda762e2ba57b6a564fa2d3be40bd892b8cf353afa6475"` |
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
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:aae75164d165f5a4c0e499d094250b126cb2c634f1f3c5a55226be1fd115c101"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:0a8b103130fe77d9b2a8d6f9ab9e4d69cc7146f7f342b859fdf9ce0c703fed5d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c40d9ce71dce69af2ccfd0c4396f6fcea650358a04107008cfa34ec73e82fc4"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:8167cf7b096bcf02b20dbc95d47de65bf2b7eb2902495b089aae8ad6cc2ffae7"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c808566f31ad17b61c8700c5ecf0e95be4fd01ca4b2edf3bb12f80f4de49255"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c45259baf1db3285bd3b9cb81d1637bfcd7ac34589868894e6ad63ee93577a0a"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c60be35d2fffdab2e6c81834408613d778914041c0ecd3f4a0f5be53541dc7bd"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:27864c18901ea515a772984044b552f7cb3a0d2a058bd1a67a9b53dc49c4ab5d"` |

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
| `["scope"]["dataset_versions"]` | `["hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"]` |
| `["scope"]["denominator_basis"]` | `"all_valid_records_in_selected_dataset_scope"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"hmac-sha256:41c8e31c7545a4277beda762e2ba57b6a564fa2d3be40bd892b8cf353afa6475"` |
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
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:aae75164d165f5a4c0e499d094250b126cb2c634f1f3c5a55226be1fd115c101"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:0a8b103130fe77d9b2a8d6f9ab9e4d69cc7146f7f342b859fdf9ce0c703fed5d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c40d9ce71dce69af2ccfd0c4396f6fcea650358a04107008cfa34ec73e82fc4"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:8167cf7b096bcf02b20dbc95d47de65bf2b7eb2902495b089aae8ad6cc2ffae7"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c808566f31ad17b61c8700c5ecf0e95be4fd01ca4b2edf3bb12f80f4de49255"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c45259baf1db3285bd3b9cb81d1637bfcd7ac34589868894e6ad63ee93577a0a"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c60be35d2fffdab2e6c81834408613d778914041c0ecd3f4a0f5be53541dc7bd"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:27864c18901ea515a772984044b552f7cb3a0d2a058bd1a67a9b53dc49c4ab5d"` |

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
| `["representation"]["binning_or_mapping_rule"]` | `"hmac-sha256:18da0fd476e3b47330cd178d9efef7c39c415771e8f8bd5cb6a7f13e9681a9b3"` |
| `["representation"]["field_name"]` | `"hmac-sha256:47e6ffdde83ab627afa8a2c8617571bf1cf11f84faf6415e021a437406b58765"` |
| `["representation"]["missing_state_id"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["missing_value_policy"]` | `"error"` |
| `["representation"]["normalization_profile"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["representation_name"]` | `"hmac-sha256:220b787af129ef50eab4ee9f3c90a00a7bce0a525c6e49bfc40fe9bb8af1d0b8"` |
| `["representation"]["representation_source"]` | `"hmac-sha256:1faa75c58dd3f727bec66d81de5cab7c2e64afbebcd03c32653ba5432a5c4369"` |
| `["representation"]["representation_version"]` | `"hmac-sha256:b6d6724490a6778f4b6e234f43fff3602f2707d6b9ab74acb0cc8e83c96d3da8"` |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4", "hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"]` |
| `["scope"]["denominator_basis"]` | `"separate_ordered_representation_scopes"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 16 |
| `["scope"]["scope_id"]` | `"hmac-sha256:565dbad623917e17596723cd5a3913a687c595118c10dfc2472c88f31282765f"` |
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
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:a130e0b7f4696e3bc1ed555d0170b426ca57c7efed97c9c27766355dd842ec1c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:6da9164abc2800aec9b384c96483bc3bc128008df04704ad7050851f8b3f9a2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:52d7e4984062cff58f5ee2ab4592f4174277c11213b23be0f66b0da6c2801b15"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:b09664f79e8df7595b88db8e5d4fd40a678384e2b4816e04044a63b901c6dc3d"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:18eea61d82b38372f77e43b8596c93ef577d554d1cb4dba3545cd509026b1c2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:d829ae28c8f6422156149b7d293896efb88703427b4b31d13996703e67d35aae"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:41770f394bc6316c571ecb74ac4e07554113bb8f92d0c56603009a81daeeff12"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:3913f4a00a32e7b06211da44f3d156e37509bf8aefde1ba61f221717eaae8c8d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:aae75164d165f5a4c0e499d094250b126cb2c634f1f3c5a55226be1fd115c101"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:0a8b103130fe77d9b2a8d6f9ab9e4d69cc7146f7f342b859fdf9ce0c703fed5d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c40d9ce71dce69af2ccfd0c4396f6fcea650358a04107008cfa34ec73e82fc4"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:8167cf7b096bcf02b20dbc95d47de65bf2b7eb2902495b089aae8ad6cc2ffae7"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c808566f31ad17b61c8700c5ecf0e95be4fd01ca4b2edf3bb12f80f4de49255"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c45259baf1db3285bd3b9cb81d1637bfcd7ac34589868894e6ad63ee93577a0a"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c60be35d2fffdab2e6c81834408613d778914041c0ecd3f4a0f5be53541dc7bd"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:27864c18901ea515a772984044b552f7cb3a0d2a058bd1a67a9b53dc49c4ab5d"` |

### Analytical result

`["derived_metrics"]["support"]["by_version"]["hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"]["support_size"]`

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
| `["representation"]["binning_or_mapping_rule"]` | `"hmac-sha256:18da0fd476e3b47330cd178d9efef7c39c415771e8f8bd5cb6a7f13e9681a9b3"` |
| `["representation"]["field_name"]` | `"hmac-sha256:47e6ffdde83ab627afa8a2c8617571bf1cf11f84faf6415e021a437406b58765"` |
| `["representation"]["missing_state_id"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["missing_value_policy"]` | `"error"` |
| `["representation"]["normalization_profile"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["representation_name"]` | `"hmac-sha256:220b787af129ef50eab4ee9f3c90a00a7bce0a525c6e49bfc40fe9bb8af1d0b8"` |
| `["representation"]["representation_source"]` | `"hmac-sha256:1faa75c58dd3f727bec66d81de5cab7c2e64afbebcd03c32653ba5432a5c4369"` |
| `["representation"]["representation_version"]` | `"hmac-sha256:b6d6724490a6778f4b6e234f43fff3602f2707d6b9ab74acb0cc8e83c96d3da8"` |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"]` |
| `["scope"]["denominator_basis"]` | `"included_representation_records"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["exclusions"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"hmac-sha256:e8d3d329142ddbec8c51b0affa3d8ade12402bebc6e9d4b1e2a994e17ed56f05"` |
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
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:a130e0b7f4696e3bc1ed555d0170b426ca57c7efed97c9c27766355dd842ec1c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:6da9164abc2800aec9b384c96483bc3bc128008df04704ad7050851f8b3f9a2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:52d7e4984062cff58f5ee2ab4592f4174277c11213b23be0f66b0da6c2801b15"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:b09664f79e8df7595b88db8e5d4fd40a678384e2b4816e04044a63b901c6dc3d"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:18eea61d82b38372f77e43b8596c93ef577d554d1cb4dba3545cd509026b1c2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:d829ae28c8f6422156149b7d293896efb88703427b4b31d13996703e67d35aae"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:41770f394bc6316c571ecb74ac4e07554113bb8f92d0c56603009a81daeeff12"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:3913f4a00a32e7b06211da44f3d156e37509bf8aefde1ba61f221717eaae8c8d"` |

### Analytical result

`["derived_metrics"]["support"]["by_version"]["hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"]["support_size"]`

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
| `["representation"]["binning_or_mapping_rule"]` | `"hmac-sha256:18da0fd476e3b47330cd178d9efef7c39c415771e8f8bd5cb6a7f13e9681a9b3"` |
| `["representation"]["field_name"]` | `"hmac-sha256:47e6ffdde83ab627afa8a2c8617571bf1cf11f84faf6415e021a437406b58765"` |
| `["representation"]["missing_state_id"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["missing_value_policy"]` | `"error"` |
| `["representation"]["normalization_profile"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["representation_name"]` | `"hmac-sha256:220b787af129ef50eab4ee9f3c90a00a7bce0a525c6e49bfc40fe9bb8af1d0b8"` |
| `["representation"]["representation_source"]` | `"hmac-sha256:1faa75c58dd3f727bec66d81de5cab7c2e64afbebcd03c32653ba5432a5c4369"` |
| `["representation"]["representation_version"]` | `"hmac-sha256:b6d6724490a6778f4b6e234f43fff3602f2707d6b9ab74acb0cc8e83c96d3da8"` |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"]` |
| `["scope"]["denominator_basis"]` | `"included_representation_records"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["exclusions"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"hmac-sha256:62f240a66b38ae21fd6453c60b78d6ee2712c8ef1933c6c15983da3e393cbffc"` |
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
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:aae75164d165f5a4c0e499d094250b126cb2c634f1f3c5a55226be1fd115c101"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:0a8b103130fe77d9b2a8d6f9ab9e4d69cc7146f7f342b859fdf9ce0c703fed5d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c40d9ce71dce69af2ccfd0c4396f6fcea650358a04107008cfa34ec73e82fc4"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:8167cf7b096bcf02b20dbc95d47de65bf2b7eb2902495b089aae8ad6cc2ffae7"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c808566f31ad17b61c8700c5ecf0e95be4fd01ca4b2edf3bb12f80f4de49255"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c45259baf1db3285bd3b9cb81d1637bfcd7ac34589868894e6ad63ee93577a0a"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c60be35d2fffdab2e6c81834408613d778914041c0ecd3f4a0f5be53541dc7bd"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:27864c18901ea515a772984044b552f7cb3a0d2a058bd1a67a9b53dc49c4ab5d"` |

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
| `["representation"]["binning_or_mapping_rule"]` | `"hmac-sha256:18da0fd476e3b47330cd178d9efef7c39c415771e8f8bd5cb6a7f13e9681a9b3"` |
| `["representation"]["field_name"]` | `"hmac-sha256:47e6ffdde83ab627afa8a2c8617571bf1cf11f84faf6415e021a437406b58765"` |
| `["representation"]["missing_state_id"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["missing_value_policy"]` | `"error"` |
| `["representation"]["normalization_profile"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["representation_name"]` | `"hmac-sha256:220b787af129ef50eab4ee9f3c90a00a7bce0a525c6e49bfc40fe9bb8af1d0b8"` |
| `["representation"]["representation_source"]` | `"hmac-sha256:1faa75c58dd3f727bec66d81de5cab7c2e64afbebcd03c32653ba5432a5c4369"` |
| `["representation"]["representation_version"]` | `"hmac-sha256:b6d6724490a6778f4b6e234f43fff3602f2707d6b9ab74acb0cc8e83c96d3da8"` |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4", "hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"]` |
| `["scope"]["denominator_basis"]` | `"separate_ordered_representation_scopes"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 16 |
| `["scope"]["scope_id"]` | `"hmac-sha256:565dbad623917e17596723cd5a3913a687c595118c10dfc2472c88f31282765f"` |
| `["status"]` | `"available"` |
| `["theory_map_ids"]` | `[]` |
| `["trace_ids"]` | `["T1"]` |
| `["unit"]` | `"comparison"` |
| `["value"]["collision_groups"]` | `[]` |
| `["value"]["compatibility_method"]` | `"identical_declared_basis"` |
| `["value"]["earlier_representation"]["binning_or_mapping_rule"]` | `"hmac-sha256:18da0fd476e3b47330cd178d9efef7c39c415771e8f8bd5cb6a7f13e9681a9b3"` |
| `["value"]["earlier_representation"]["field_name"]` | `"hmac-sha256:47e6ffdde83ab627afa8a2c8617571bf1cf11f84faf6415e021a437406b58765"` |
| `["value"]["earlier_representation"]["missing_state_id"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["value"]["earlier_representation"]["missing_value_policy"]` | `"error"` |
| `["value"]["earlier_representation"]["normalization_profile"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["value"]["earlier_representation"]["representation_name"]` | `"hmac-sha256:220b787af129ef50eab4ee9f3c90a00a7bce0a525c6e49bfc40fe9bb8af1d0b8"` |
| `["value"]["earlier_representation"]["representation_source"]` | `"hmac-sha256:1faa75c58dd3f727bec66d81de5cab7c2e64afbebcd03c32653ba5432a5c4369"` |
| `["value"]["earlier_representation"]["representation_version"]` | `"hmac-sha256:b6d6724490a6778f4b6e234f43fff3602f2707d6b9ab74acb0cc8e83c96d3da8"` |
| `["value"]["earlier_state_semantics"]` | `"hmac-sha256:0d9b624753cf37a4e9177858c9c1730b784041e76b44762d272fb3441129705a"` |
| `["value"]["earlier_version"]` | `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` |
| `["value"]["harmonized_earlier_support"]` | `["hmac-sha256:f130effa18aee11b975751d07fec071c7ebe83aa6d8210757e5ec8615b3108a7", "hmac-sha256:65497bf5eab3b43cfbca481d2fd21635c2c9e701c962aed90ab94eff7e76f62d", "hmac-sha256:9b4818bf9968505a3e9dc65c9f4f3210f99fb91600ce7bcbef1f77e7ed626250", "hmac-sha256:fac7b92af75bb73c87cf215ab7489fac158c8e431c07eea0fc45df31c09d5233", "hmac-sha256:c26a74b0b747e213a83215b0fc9f25f7a8880a232796267c3bbd849205106edc", "hmac-sha256:cce2bc33c7dd4c9eb9222b63c7781aeaf97698fcab3d9f1838dc70d8b75fe210", "hmac-sha256:51607e4e3a5be5845e6b4f520a9d0a1599f5e00a2989fb7ed2dfb5339b44e32a", "hmac-sha256:1cd134c257cbcb62c641a411712154ed9e5e5c0119fef89ebd98d7b33a90c159"]` |
| `["value"]["harmonized_later_support"]` | `["hmac-sha256:65497bf5eab3b43cfbca481d2fd21635c2c9e701c962aed90ab94eff7e76f62d", "hmac-sha256:9b4818bf9968505a3e9dc65c9f4f3210f99fb91600ce7bcbef1f77e7ed626250", "hmac-sha256:fac7b92af75bb73c87cf215ab7489fac158c8e431c07eea0fc45df31c09d5233", "hmac-sha256:c26a74b0b747e213a83215b0fc9f25f7a8880a232796267c3bbd849205106edc", "hmac-sha256:51607e4e3a5be5845e6b4f520a9d0a1599f5e00a2989fb7ed2dfb5339b44e32a"]` |
| `["value"]["harmonized_representation"]["binning_or_mapping_rule"]` | `"hmac-sha256:18da0fd476e3b47330cd178d9efef7c39c415771e8f8bd5cb6a7f13e9681a9b3"` |
| `["value"]["harmonized_representation"]["field_name"]` | `"hmac-sha256:47e6ffdde83ab627afa8a2c8617571bf1cf11f84faf6415e021a437406b58765"` |
| `["value"]["harmonized_representation"]["missing_state_id"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["value"]["harmonized_representation"]["missing_value_policy"]` | `"error"` |
| `["value"]["harmonized_representation"]["normalization_profile"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["value"]["harmonized_representation"]["representation_name"]` | `"hmac-sha256:220b787af129ef50eab4ee9f3c90a00a7bce0a525c6e49bfc40fe9bb8af1d0b8"` |
| `["value"]["harmonized_representation"]["representation_source"]` | `"hmac-sha256:1faa75c58dd3f727bec66d81de5cab7c2e64afbebcd03c32653ba5432a5c4369"` |
| `["value"]["harmonized_representation"]["representation_version"]` | `"hmac-sha256:b6d6724490a6778f4b6e234f43fff3602f2707d6b9ab74acb0cc8e83c96d3da8"` |
| `["value"]["harmonized_state_semantics"]` | `"hmac-sha256:0d9b624753cf37a4e9177858c9c1730b784041e76b44762d272fb3441129705a"` |
| `["value"]["later_representation"]["binning_or_mapping_rule"]` | `"hmac-sha256:18da0fd476e3b47330cd178d9efef7c39c415771e8f8bd5cb6a7f13e9681a9b3"` |
| `["value"]["later_representation"]["field_name"]` | `"hmac-sha256:47e6ffdde83ab627afa8a2c8617571bf1cf11f84faf6415e021a437406b58765"` |
| `["value"]["later_representation"]["missing_state_id"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["value"]["later_representation"]["missing_value_policy"]` | `"error"` |
| `["value"]["later_representation"]["normalization_profile"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["value"]["later_representation"]["representation_name"]` | `"hmac-sha256:220b787af129ef50eab4ee9f3c90a00a7bce0a525c6e49bfc40fe9bb8af1d0b8"` |
| `["value"]["later_representation"]["representation_source"]` | `"hmac-sha256:1faa75c58dd3f727bec66d81de5cab7c2e64afbebcd03c32653ba5432a5c4369"` |
| `["value"]["later_representation"]["representation_version"]` | `"hmac-sha256:b6d6724490a6778f4b6e234f43fff3602f2707d6b9ab74acb0cc8e83c96d3da8"` |
| `["value"]["later_state_semantics"]` | `"hmac-sha256:0d9b624753cf37a4e9177858c9c1730b784041e76b44762d272fb3441129705a"` |
| `["value"]["later_version"]` | `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` |
| `["value"]["original_earlier_support"]` | `["hmac-sha256:f130effa18aee11b975751d07fec071c7ebe83aa6d8210757e5ec8615b3108a7", "hmac-sha256:65497bf5eab3b43cfbca481d2fd21635c2c9e701c962aed90ab94eff7e76f62d", "hmac-sha256:9b4818bf9968505a3e9dc65c9f4f3210f99fb91600ce7bcbef1f77e7ed626250", "hmac-sha256:fac7b92af75bb73c87cf215ab7489fac158c8e431c07eea0fc45df31c09d5233", "hmac-sha256:c26a74b0b747e213a83215b0fc9f25f7a8880a232796267c3bbd849205106edc", "hmac-sha256:cce2bc33c7dd4c9eb9222b63c7781aeaf97698fcab3d9f1838dc70d8b75fe210", "hmac-sha256:51607e4e3a5be5845e6b4f520a9d0a1599f5e00a2989fb7ed2dfb5339b44e32a", "hmac-sha256:1cd134c257cbcb62c641a411712154ed9e5e5c0119fef89ebd98d7b33a90c159"]` |
| `["value"]["original_later_support"]` | `["hmac-sha256:65497bf5eab3b43cfbca481d2fd21635c2c9e701c962aed90ab94eff7e76f62d", "hmac-sha256:9b4818bf9968505a3e9dc65c9f4f3210f99fb91600ce7bcbef1f77e7ed626250", "hmac-sha256:fac7b92af75bb73c87cf215ab7489fac158c8e431c07eea0fc45df31c09d5233", "hmac-sha256:c26a74b0b747e213a83215b0fc9f25f7a8880a232796267c3bbd849205106edc", "hmac-sha256:51607e4e3a5be5845e6b4f520a9d0a1599f5e00a2989fb7ed2dfb5339b44e32a"]` |
| `["value"]["retention_denominator"]` | 8 |
| `["value"]["retention_denominator_basis"]` | `"earlier_positive_mass_support_in_harmonized_representation"` |
| `["value"]["state_mapping"]` | `[]` |
| `["value"]["version_order"]` | `["hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4", "hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"]` |
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
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:a130e0b7f4696e3bc1ed555d0170b426ca57c7efed97c9c27766355dd842ec1c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:6da9164abc2800aec9b384c96483bc3bc128008df04704ad7050851f8b3f9a2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:52d7e4984062cff58f5ee2ab4592f4174277c11213b23be0f66b0da6c2801b15"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:b09664f79e8df7595b88db8e5d4fd40a678384e2b4816e04044a63b901c6dc3d"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:18eea61d82b38372f77e43b8596c93ef577d554d1cb4dba3545cd509026b1c2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:d829ae28c8f6422156149b7d293896efb88703427b4b31d13996703e67d35aae"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:41770f394bc6316c571ecb74ac4e07554113bb8f92d0c56603009a81daeeff12"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:3913f4a00a32e7b06211da44f3d156e37509bf8aefde1ba61f221717eaae8c8d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:aae75164d165f5a4c0e499d094250b126cb2c634f1f3c5a55226be1fd115c101"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:0a8b103130fe77d9b2a8d6f9ab9e4d69cc7146f7f342b859fdf9ce0c703fed5d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c40d9ce71dce69af2ccfd0c4396f6fcea650358a04107008cfa34ec73e82fc4"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:8167cf7b096bcf02b20dbc95d47de65bf2b7eb2902495b089aae8ad6cc2ffae7"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c808566f31ad17b61c8700c5ecf0e95be4fd01ca4b2edf3bb12f80f4de49255"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c45259baf1db3285bd3b9cb81d1637bfcd7ac34589868894e6ad63ee93577a0a"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c60be35d2fffdab2e6c81834408613d778914041c0ecd3f4a0f5be53541dc7bd"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:27864c18901ea515a772984044b552f7cb3a0d2a058bd1a67a9b53dc49c4ab5d"` |

**`["value"]["mapping_effect"]`**

| `"dataset_version"` | `"harmonized_support_size"` | `"original_support_size"` |
|---|---|---|
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | 8 | 8 |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | 5 | 5 |

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
| `["representation"]["binning_or_mapping_rule"]` | `"hmac-sha256:18da0fd476e3b47330cd178d9efef7c39c415771e8f8bd5cb6a7f13e9681a9b3"` |
| `["representation"]["field_name"]` | `"hmac-sha256:47e6ffdde83ab627afa8a2c8617571bf1cf11f84faf6415e021a437406b58765"` |
| `["representation"]["missing_state_id"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["missing_value_policy"]` | `"error"` |
| `["representation"]["normalization_profile"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["representation_name"]` | `"hmac-sha256:220b787af129ef50eab4ee9f3c90a00a7bce0a525c6e49bfc40fe9bb8af1d0b8"` |
| `["representation"]["representation_source"]` | `"hmac-sha256:1faa75c58dd3f727bec66d81de5cab7c2e64afbebcd03c32653ba5432a5c4369"` |
| `["representation"]["representation_version"]` | `"hmac-sha256:b6d6724490a6778f4b6e234f43fff3602f2707d6b9ab74acb0cc8e83c96d3da8"` |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4", "hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"]` |
| `["scope"]["denominator_basis"]` | `"separate_ordered_representation_scopes"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 16 |
| `["scope"]["scope_id"]` | `"hmac-sha256:565dbad623917e17596723cd5a3913a687c595118c10dfc2472c88f31282765f"` |
| `["status"]` | `"available"` |
| `["theory_map_ids"]` | `[]` |
| `["trace_ids"]` | `["T1"]` |
| `["unit"]` | `"set_of_states"` |
| `["value"]` | `["hmac-sha256:f130effa18aee11b975751d07fec071c7ebe83aa6d8210757e5ec8615b3108a7", "hmac-sha256:cce2bc33c7dd4c9eb9222b63c7781aeaf97698fcab3d9f1838dc70d8b75fe210", "hmac-sha256:1cd134c257cbcb62c641a411712154ed9e5e5c0119fef89ebd98d7b33a90c159"]` |
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
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:a130e0b7f4696e3bc1ed555d0170b426ca57c7efed97c9c27766355dd842ec1c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:6da9164abc2800aec9b384c96483bc3bc128008df04704ad7050851f8b3f9a2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:52d7e4984062cff58f5ee2ab4592f4174277c11213b23be0f66b0da6c2801b15"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:b09664f79e8df7595b88db8e5d4fd40a678384e2b4816e04044a63b901c6dc3d"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:18eea61d82b38372f77e43b8596c93ef577d554d1cb4dba3545cd509026b1c2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:d829ae28c8f6422156149b7d293896efb88703427b4b31d13996703e67d35aae"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:41770f394bc6316c571ecb74ac4e07554113bb8f92d0c56603009a81daeeff12"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:3913f4a00a32e7b06211da44f3d156e37509bf8aefde1ba61f221717eaae8c8d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:aae75164d165f5a4c0e499d094250b126cb2c634f1f3c5a55226be1fd115c101"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:0a8b103130fe77d9b2a8d6f9ab9e4d69cc7146f7f342b859fdf9ce0c703fed5d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c40d9ce71dce69af2ccfd0c4396f6fcea650358a04107008cfa34ec73e82fc4"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:8167cf7b096bcf02b20dbc95d47de65bf2b7eb2902495b089aae8ad6cc2ffae7"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c808566f31ad17b61c8700c5ecf0e95be4fd01ca4b2edf3bb12f80f4de49255"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c45259baf1db3285bd3b9cb81d1637bfcd7ac34589868894e6ad63ee93577a0a"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c60be35d2fffdab2e6c81834408613d778914041c0ecd3f4a0f5be53541dc7bd"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:27864c18901ea515a772984044b552f7cb3a0d2a058bd1a67a9b53dc49c4ab5d"` |

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
| `["representation"]["binning_or_mapping_rule"]` | `"hmac-sha256:18da0fd476e3b47330cd178d9efef7c39c415771e8f8bd5cb6a7f13e9681a9b3"` |
| `["representation"]["field_name"]` | `"hmac-sha256:47e6ffdde83ab627afa8a2c8617571bf1cf11f84faf6415e021a437406b58765"` |
| `["representation"]["missing_state_id"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["missing_value_policy"]` | `"error"` |
| `["representation"]["normalization_profile"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["representation_name"]` | `"hmac-sha256:220b787af129ef50eab4ee9f3c90a00a7bce0a525c6e49bfc40fe9bb8af1d0b8"` |
| `["representation"]["representation_source"]` | `"hmac-sha256:1faa75c58dd3f727bec66d81de5cab7c2e64afbebcd03c32653ba5432a5c4369"` |
| `["representation"]["representation_version"]` | `"hmac-sha256:b6d6724490a6778f4b6e234f43fff3602f2707d6b9ab74acb0cc8e83c96d3da8"` |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4", "hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"]` |
| `["scope"]["denominator_basis"]` | `"separate_ordered_representation_scopes"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 16 |
| `["scope"]["scope_id"]` | `"hmac-sha256:565dbad623917e17596723cd5a3913a687c595118c10dfc2472c88f31282765f"` |
| `["status"]` | `"available"` |
| `["theory_map_ids"]` | `[]` |
| `["trace_ids"]` | `["T1"]` |
| `["unit"]` | `"set_of_states"` |
| `["value"]` | `["hmac-sha256:65497bf5eab3b43cfbca481d2fd21635c2c9e701c962aed90ab94eff7e76f62d", "hmac-sha256:9b4818bf9968505a3e9dc65c9f4f3210f99fb91600ce7bcbef1f77e7ed626250", "hmac-sha256:fac7b92af75bb73c87cf215ab7489fac158c8e431c07eea0fc45df31c09d5233", "hmac-sha256:c26a74b0b747e213a83215b0fc9f25f7a8880a232796267c3bbd849205106edc", "hmac-sha256:51607e4e3a5be5845e6b4f520a9d0a1599f5e00a2989fb7ed2dfb5339b44e32a"]` |
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
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:a130e0b7f4696e3bc1ed555d0170b426ca57c7efed97c9c27766355dd842ec1c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:6da9164abc2800aec9b384c96483bc3bc128008df04704ad7050851f8b3f9a2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:52d7e4984062cff58f5ee2ab4592f4174277c11213b23be0f66b0da6c2801b15"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:b09664f79e8df7595b88db8e5d4fd40a678384e2b4816e04044a63b901c6dc3d"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:18eea61d82b38372f77e43b8596c93ef577d554d1cb4dba3545cd509026b1c2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:d829ae28c8f6422156149b7d293896efb88703427b4b31d13996703e67d35aae"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:41770f394bc6316c571ecb74ac4e07554113bb8f92d0c56603009a81daeeff12"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:3913f4a00a32e7b06211da44f3d156e37509bf8aefde1ba61f221717eaae8c8d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:aae75164d165f5a4c0e499d094250b126cb2c634f1f3c5a55226be1fd115c101"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:0a8b103130fe77d9b2a8d6f9ab9e4d69cc7146f7f342b859fdf9ce0c703fed5d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c40d9ce71dce69af2ccfd0c4396f6fcea650358a04107008cfa34ec73e82fc4"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:8167cf7b096bcf02b20dbc95d47de65bf2b7eb2902495b089aae8ad6cc2ffae7"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c808566f31ad17b61c8700c5ecf0e95be4fd01ca4b2edf3bb12f80f4de49255"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c45259baf1db3285bd3b9cb81d1637bfcd7ac34589868894e6ad63ee93577a0a"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c60be35d2fffdab2e6c81834408613d778914041c0ecd3f4a0f5be53541dc7bd"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:27864c18901ea515a772984044b552f7cb3a0d2a058bd1a67a9b53dc49c4ab5d"` |

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
| `["representation"]["binning_or_mapping_rule"]` | `"hmac-sha256:18da0fd476e3b47330cd178d9efef7c39c415771e8f8bd5cb6a7f13e9681a9b3"` |
| `["representation"]["field_name"]` | `"hmac-sha256:47e6ffdde83ab627afa8a2c8617571bf1cf11f84faf6415e021a437406b58765"` |
| `["representation"]["missing_state_id"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["missing_value_policy"]` | `"error"` |
| `["representation"]["normalization_profile"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["representation_name"]` | `"hmac-sha256:220b787af129ef50eab4ee9f3c90a00a7bce0a525c6e49bfc40fe9bb8af1d0b8"` |
| `["representation"]["representation_source"]` | `"hmac-sha256:1faa75c58dd3f727bec66d81de5cab7c2e64afbebcd03c32653ba5432a5c4369"` |
| `["representation"]["representation_version"]` | `"hmac-sha256:b6d6724490a6778f4b6e234f43fff3602f2707d6b9ab74acb0cc8e83c96d3da8"` |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4", "hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"]` |
| `["scope"]["denominator_basis"]` | `"separate_ordered_representation_scopes"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 16 |
| `["scope"]["scope_id"]` | `"hmac-sha256:565dbad623917e17596723cd5a3913a687c595118c10dfc2472c88f31282765f"` |
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
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:a130e0b7f4696e3bc1ed555d0170b426ca57c7efed97c9c27766355dd842ec1c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:6da9164abc2800aec9b384c96483bc3bc128008df04704ad7050851f8b3f9a2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:52d7e4984062cff58f5ee2ab4592f4174277c11213b23be0f66b0da6c2801b15"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:b09664f79e8df7595b88db8e5d4fd40a678384e2b4816e04044a63b901c6dc3d"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:18eea61d82b38372f77e43b8596c93ef577d554d1cb4dba3545cd509026b1c2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:d829ae28c8f6422156149b7d293896efb88703427b4b31d13996703e67d35aae"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:41770f394bc6316c571ecb74ac4e07554113bb8f92d0c56603009a81daeeff12"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:3913f4a00a32e7b06211da44f3d156e37509bf8aefde1ba61f221717eaae8c8d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:aae75164d165f5a4c0e499d094250b126cb2c634f1f3c5a55226be1fd115c101"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:0a8b103130fe77d9b2a8d6f9ab9e4d69cc7146f7f342b859fdf9ce0c703fed5d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c40d9ce71dce69af2ccfd0c4396f6fcea650358a04107008cfa34ec73e82fc4"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:8167cf7b096bcf02b20dbc95d47de65bf2b7eb2902495b089aae8ad6cc2ffae7"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c808566f31ad17b61c8700c5ecf0e95be4fd01ca4b2edf3bb12f80f4de49255"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c45259baf1db3285bd3b9cb81d1637bfcd7ac34589868894e6ad63ee93577a0a"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c60be35d2fffdab2e6c81834408613d778914041c0ecd3f4a0f5be53541dc7bd"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:27864c18901ea515a772984044b552f7cb3a0d2a058bd1a67a9b53dc49c4ab5d"` |

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
| `["representation"]["binning_or_mapping_rule"]` | `"hmac-sha256:18da0fd476e3b47330cd178d9efef7c39c415771e8f8bd5cb6a7f13e9681a9b3"` |
| `["representation"]["field_name"]` | `"hmac-sha256:47e6ffdde83ab627afa8a2c8617571bf1cf11f84faf6415e021a437406b58765"` |
| `["representation"]["missing_state_id"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["missing_value_policy"]` | `"error"` |
| `["representation"]["normalization_profile"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["representation_name"]` | `"hmac-sha256:220b787af129ef50eab4ee9f3c90a00a7bce0a525c6e49bfc40fe9bb8af1d0b8"` |
| `["representation"]["representation_source"]` | `"hmac-sha256:1faa75c58dd3f727bec66d81de5cab7c2e64afbebcd03c32653ba5432a5c4369"` |
| `["representation"]["representation_version"]` | `"hmac-sha256:b6d6724490a6778f4b6e234f43fff3602f2707d6b9ab74acb0cc8e83c96d3da8"` |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4", "hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"]` |
| `["scope"]["denominator_basis"]` | `"separate_ordered_representation_scopes"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 16 |
| `["scope"]["scope_id"]` | `"hmac-sha256:565dbad623917e17596723cd5a3913a687c595118c10dfc2472c88f31282765f"` |
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
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:a130e0b7f4696e3bc1ed555d0170b426ca57c7efed97c9c27766355dd842ec1c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:6da9164abc2800aec9b384c96483bc3bc128008df04704ad7050851f8b3f9a2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:52d7e4984062cff58f5ee2ab4592f4174277c11213b23be0f66b0da6c2801b15"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:b09664f79e8df7595b88db8e5d4fd40a678384e2b4816e04044a63b901c6dc3d"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:18eea61d82b38372f77e43b8596c93ef577d554d1cb4dba3545cd509026b1c2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:d829ae28c8f6422156149b7d293896efb88703427b4b31d13996703e67d35aae"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:41770f394bc6316c571ecb74ac4e07554113bb8f92d0c56603009a81daeeff12"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:3913f4a00a32e7b06211da44f3d156e37509bf8aefde1ba61f221717eaae8c8d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:aae75164d165f5a4c0e499d094250b126cb2c634f1f3c5a55226be1fd115c101"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:0a8b103130fe77d9b2a8d6f9ab9e4d69cc7146f7f342b859fdf9ce0c703fed5d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c40d9ce71dce69af2ccfd0c4396f6fcea650358a04107008cfa34ec73e82fc4"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:8167cf7b096bcf02b20dbc95d47de65bf2b7eb2902495b089aae8ad6cc2ffae7"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c808566f31ad17b61c8700c5ecf0e95be4fd01ca4b2edf3bb12f80f4de49255"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c45259baf1db3285bd3b9cb81d1637bfcd7ac34589868894e6ad63ee93577a0a"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c60be35d2fffdab2e6c81834408613d778914041c0ecd3f4a0f5be53541dc7bd"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:27864c18901ea515a772984044b552f7cb3a0d2a058bd1a67a9b53dc49c4ab5d"` |

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
| `["representation"]["binning_or_mapping_rule"]` | `"hmac-sha256:18da0fd476e3b47330cd178d9efef7c39c415771e8f8bd5cb6a7f13e9681a9b3"` |
| `["representation"]["field_name"]` | `"hmac-sha256:47e6ffdde83ab627afa8a2c8617571bf1cf11f84faf6415e021a437406b58765"` |
| `["representation"]["missing_state_id"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["missing_value_policy"]` | `"error"` |
| `["representation"]["normalization_profile"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["representation_name"]` | `"hmac-sha256:220b787af129ef50eab4ee9f3c90a00a7bce0a525c6e49bfc40fe9bb8af1d0b8"` |
| `["representation"]["representation_source"]` | `"hmac-sha256:1faa75c58dd3f727bec66d81de5cab7c2e64afbebcd03c32653ba5432a5c4369"` |
| `["representation"]["representation_version"]` | `"hmac-sha256:b6d6724490a6778f4b6e234f43fff3602f2707d6b9ab74acb0cc8e83c96d3da8"` |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4", "hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"]` |
| `["scope"]["denominator_basis"]` | `"separate_ordered_representation_scopes"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 16 |
| `["scope"]["scope_id"]` | `"hmac-sha256:565dbad623917e17596723cd5a3913a687c595118c10dfc2472c88f31282765f"` |
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
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:a130e0b7f4696e3bc1ed555d0170b426ca57c7efed97c9c27766355dd842ec1c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:6da9164abc2800aec9b384c96483bc3bc128008df04704ad7050851f8b3f9a2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:52d7e4984062cff58f5ee2ab4592f4174277c11213b23be0f66b0da6c2801b15"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:b09664f79e8df7595b88db8e5d4fd40a678384e2b4816e04044a63b901c6dc3d"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:18eea61d82b38372f77e43b8596c93ef577d554d1cb4dba3545cd509026b1c2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:d829ae28c8f6422156149b7d293896efb88703427b4b31d13996703e67d35aae"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:41770f394bc6316c571ecb74ac4e07554113bb8f92d0c56603009a81daeeff12"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:3913f4a00a32e7b06211da44f3d156e37509bf8aefde1ba61f221717eaae8c8d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:aae75164d165f5a4c0e499d094250b126cb2c634f1f3c5a55226be1fd115c101"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:0a8b103130fe77d9b2a8d6f9ab9e4d69cc7146f7f342b859fdf9ce0c703fed5d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c40d9ce71dce69af2ccfd0c4396f6fcea650358a04107008cfa34ec73e82fc4"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:8167cf7b096bcf02b20dbc95d47de65bf2b7eb2902495b089aae8ad6cc2ffae7"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c808566f31ad17b61c8700c5ecf0e95be4fd01ca4b2edf3bb12f80f4de49255"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c45259baf1db3285bd3b9cb81d1637bfcd7ac34589868894e6ad63ee93577a0a"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c60be35d2fffdab2e6c81834408613d778914041c0ecd3f4a0f5be53541dc7bd"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:27864c18901ea515a772984044b552f7cb3a0d2a058bd1a67a9b53dc49c4ab5d"` |

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
| `["representation"]["binning_or_mapping_rule"]` | `"hmac-sha256:18da0fd476e3b47330cd178d9efef7c39c415771e8f8bd5cb6a7f13e9681a9b3"` |
| `["representation"]["field_name"]` | `"hmac-sha256:47e6ffdde83ab627afa8a2c8617571bf1cf11f84faf6415e021a437406b58765"` |
| `["representation"]["missing_state_id"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["missing_value_policy"]` | `"error"` |
| `["representation"]["normalization_profile"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["representation_name"]` | `"hmac-sha256:220b787af129ef50eab4ee9f3c90a00a7bce0a525c6e49bfc40fe9bb8af1d0b8"` |
| `["representation"]["representation_source"]` | `"hmac-sha256:1faa75c58dd3f727bec66d81de5cab7c2e64afbebcd03c32653ba5432a5c4369"` |
| `["representation"]["representation_version"]` | `"hmac-sha256:b6d6724490a6778f4b6e234f43fff3602f2707d6b9ab74acb0cc8e83c96d3da8"` |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4", "hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"]` |
| `["scope"]["denominator_basis"]` | `"separate_ordered_representation_scopes"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 16 |
| `["scope"]["scope_id"]` | `"hmac-sha256:565dbad623917e17596723cd5a3913a687c595118c10dfc2472c88f31282765f"` |
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
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:a130e0b7f4696e3bc1ed555d0170b426ca57c7efed97c9c27766355dd842ec1c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:6da9164abc2800aec9b384c96483bc3bc128008df04704ad7050851f8b3f9a2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:52d7e4984062cff58f5ee2ab4592f4174277c11213b23be0f66b0da6c2801b15"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:b09664f79e8df7595b88db8e5d4fd40a678384e2b4816e04044a63b901c6dc3d"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:18eea61d82b38372f77e43b8596c93ef577d554d1cb4dba3545cd509026b1c2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:d829ae28c8f6422156149b7d293896efb88703427b4b31d13996703e67d35aae"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:41770f394bc6316c571ecb74ac4e07554113bb8f92d0c56603009a81daeeff12"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:3913f4a00a32e7b06211da44f3d156e37509bf8aefde1ba61f221717eaae8c8d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:aae75164d165f5a4c0e499d094250b126cb2c634f1f3c5a55226be1fd115c101"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:0a8b103130fe77d9b2a8d6f9ab9e4d69cc7146f7f342b859fdf9ce0c703fed5d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c40d9ce71dce69af2ccfd0c4396f6fcea650358a04107008cfa34ec73e82fc4"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:8167cf7b096bcf02b20dbc95d47de65bf2b7eb2902495b089aae8ad6cc2ffae7"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c808566f31ad17b61c8700c5ecf0e95be4fd01ca4b2edf3bb12f80f4de49255"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c45259baf1db3285bd3b9cb81d1637bfcd7ac34589868894e6ad63ee93577a0a"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c60be35d2fffdab2e6c81834408613d778914041c0ecd3f4a0f5be53541dc7bd"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:27864c18901ea515a772984044b552f7cb3a0d2a058bd1a67a9b53dc49c4ab5d"` |

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
| `["scope"]["dataset_versions"]` | `["hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"]` |
| `["scope"]["denominator_basis"]` | `"all_valid_records_in_selected_dataset_scope"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 8 |
| `["scope"]["scope_id"]` | `"hmac-sha256:41c8e31c7545a4277beda762e2ba57b6a564fa2d3be40bd892b8cf353afa6475"` |
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
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:aae75164d165f5a4c0e499d094250b126cb2c634f1f3c5a55226be1fd115c101"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:0a8b103130fe77d9b2a8d6f9ab9e4d69cc7146f7f342b859fdf9ce0c703fed5d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c40d9ce71dce69af2ccfd0c4396f6fcea650358a04107008cfa34ec73e82fc4"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:8167cf7b096bcf02b20dbc95d47de65bf2b7eb2902495b089aae8ad6cc2ffae7"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c808566f31ad17b61c8700c5ecf0e95be4fd01ca4b2edf3bb12f80f4de49255"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c45259baf1db3285bd3b9cb81d1637bfcd7ac34589868894e6ad63ee93577a0a"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c60be35d2fffdab2e6c81834408613d778914041c0ecd3f4a0f5be53541dc7bd"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:27864c18901ea515a772984044b552f7cb3a0d2a058bd1a67a9b53dc49c4ab5d"` |

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
| `["representation"]["binning_or_mapping_rule"]` | `"hmac-sha256:18da0fd476e3b47330cd178d9efef7c39c415771e8f8bd5cb6a7f13e9681a9b3"` |
| `["representation"]["field_name"]` | `"hmac-sha256:47e6ffdde83ab627afa8a2c8617571bf1cf11f84faf6415e021a437406b58765"` |
| `["representation"]["missing_state_id"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["missing_value_policy"]` | `"error"` |
| `["representation"]["normalization_profile"]` | Unavailable (null): No value supplied for this optional or inapplicable field. |
| `["representation"]["representation_name"]` | `"hmac-sha256:220b787af129ef50eab4ee9f3c90a00a7bce0a525c6e49bfc40fe9bb8af1d0b8"` |
| `["representation"]["representation_source"]` | `"hmac-sha256:1faa75c58dd3f727bec66d81de5cab7c2e64afbebcd03c32653ba5432a5c4369"` |
| `["representation"]["representation_version"]` | `"hmac-sha256:b6d6724490a6778f4b6e234f43fff3602f2707d6b9ab74acb0cc8e83c96d3da8"` |
| `["required_evidence"]` | `[]` |
| `["scope"]["dataset_versions"]` | `["hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4", "hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"]` |
| `["scope"]["denominator_basis"]` | `"separate_ordered_representation_scopes"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 16 |
| `["scope"]["scope_id"]` | `"hmac-sha256:565dbad623917e17596723cd5a3913a687c595118c10dfc2472c88f31282765f"` |
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
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:a130e0b7f4696e3bc1ed555d0170b426ca57c7efed97c9c27766355dd842ec1c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:6da9164abc2800aec9b384c96483bc3bc128008df04704ad7050851f8b3f9a2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:52d7e4984062cff58f5ee2ab4592f4174277c11213b23be0f66b0da6c2801b15"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:b09664f79e8df7595b88db8e5d4fd40a678384e2b4816e04044a63b901c6dc3d"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:18eea61d82b38372f77e43b8596c93ef577d554d1cb4dba3545cd509026b1c2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:d829ae28c8f6422156149b7d293896efb88703427b4b31d13996703e67d35aae"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:41770f394bc6316c571ecb74ac4e07554113bb8f92d0c56603009a81daeeff12"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:3913f4a00a32e7b06211da44f3d156e37509bf8aefde1ba61f221717eaae8c8d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:aae75164d165f5a4c0e499d094250b126cb2c634f1f3c5a55226be1fd115c101"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:0a8b103130fe77d9b2a8d6f9ab9e4d69cc7146f7f342b859fdf9ce0c703fed5d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c40d9ce71dce69af2ccfd0c4396f6fcea650358a04107008cfa34ec73e82fc4"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:8167cf7b096bcf02b20dbc95d47de65bf2b7eb2902495b089aae8ad6cc2ffae7"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c808566f31ad17b61c8700c5ecf0e95be4fd01ca4b2edf3bb12f80f4de49255"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c45259baf1db3285bd3b9cb81d1637bfcd7ac34589868894e6ad63ee93577a0a"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c60be35d2fffdab2e6c81834408613d778914041c0ecd3f4a0f5be53541dc7bd"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:27864c18901ea515a772984044b552f7cb3a0d2a058bd1a67a9b53dc49c4ab5d"` |

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
| `["scope"]["dataset_versions"]` | `["hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4", "hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"]` |
| `["scope"]["denominator_basis"]` | `"all_validated_bundle_records"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 16 |
| `["scope"]["scope_id"]` | `"hmac-sha256:fe3080b69d042a9eca2d392f8429412803f06dd3eb9e71fd16178d05e5971ac3"` |
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
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:a130e0b7f4696e3bc1ed555d0170b426ca57c7efed97c9c27766355dd842ec1c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:6da9164abc2800aec9b384c96483bc3bc128008df04704ad7050851f8b3f9a2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:52d7e4984062cff58f5ee2ab4592f4174277c11213b23be0f66b0da6c2801b15"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:b09664f79e8df7595b88db8e5d4fd40a678384e2b4816e04044a63b901c6dc3d"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:18eea61d82b38372f77e43b8596c93ef577d554d1cb4dba3545cd509026b1c2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:d829ae28c8f6422156149b7d293896efb88703427b4b31d13996703e67d35aae"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:41770f394bc6316c571ecb74ac4e07554113bb8f92d0c56603009a81daeeff12"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:3913f4a00a32e7b06211da44f3d156e37509bf8aefde1ba61f221717eaae8c8d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:aae75164d165f5a4c0e499d094250b126cb2c634f1f3c5a55226be1fd115c101"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:0a8b103130fe77d9b2a8d6f9ab9e4d69cc7146f7f342b859fdf9ce0c703fed5d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c40d9ce71dce69af2ccfd0c4396f6fcea650358a04107008cfa34ec73e82fc4"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:8167cf7b096bcf02b20dbc95d47de65bf2b7eb2902495b089aae8ad6cc2ffae7"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c808566f31ad17b61c8700c5ecf0e95be4fd01ca4b2edf3bb12f80f4de49255"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c45259baf1db3285bd3b9cb81d1637bfcd7ac34589868894e6ad63ee93577a0a"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c60be35d2fffdab2e6c81834408613d778914041c0ecd3f4a0f5be53541dc7bd"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:27864c18901ea515a772984044b552f7cb3a0d2a058bd1a67a9b53dc49c4ab5d"` |

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
| `["scope"]["dataset_versions"]` | `["hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4", "hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"]` |
| `["scope"]["denominator_basis"]` | `"all_validated_bundle_records"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 16 |
| `["scope"]["scope_id"]` | `"hmac-sha256:fe3080b69d042a9eca2d392f8429412803f06dd3eb9e71fd16178d05e5971ac3"` |
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
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:a130e0b7f4696e3bc1ed555d0170b426ca57c7efed97c9c27766355dd842ec1c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:6da9164abc2800aec9b384c96483bc3bc128008df04704ad7050851f8b3f9a2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:52d7e4984062cff58f5ee2ab4592f4174277c11213b23be0f66b0da6c2801b15"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:b09664f79e8df7595b88db8e5d4fd40a678384e2b4816e04044a63b901c6dc3d"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:18eea61d82b38372f77e43b8596c93ef577d554d1cb4dba3545cd509026b1c2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:d829ae28c8f6422156149b7d293896efb88703427b4b31d13996703e67d35aae"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:41770f394bc6316c571ecb74ac4e07554113bb8f92d0c56603009a81daeeff12"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:3913f4a00a32e7b06211da44f3d156e37509bf8aefde1ba61f221717eaae8c8d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:aae75164d165f5a4c0e499d094250b126cb2c634f1f3c5a55226be1fd115c101"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:0a8b103130fe77d9b2a8d6f9ab9e4d69cc7146f7f342b859fdf9ce0c703fed5d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c40d9ce71dce69af2ccfd0c4396f6fcea650358a04107008cfa34ec73e82fc4"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:8167cf7b096bcf02b20dbc95d47de65bf2b7eb2902495b089aae8ad6cc2ffae7"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c808566f31ad17b61c8700c5ecf0e95be4fd01ca4b2edf3bb12f80f4de49255"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c45259baf1db3285bd3b9cb81d1637bfcd7ac34589868894e6ad63ee93577a0a"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c60be35d2fffdab2e6c81834408613d778914041c0ecd3f4a0f5be53541dc7bd"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:27864c18901ea515a772984044b552f7cb3a0d2a058bd1a67a9b53dc49c4ab5d"` |

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
| `["scope"]["dataset_versions"]` | `["hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4", "hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"]` |
| `["scope"]["denominator_basis"]` | `"all_validated_bundle_records"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 16 |
| `["scope"]["scope_id"]` | `"hmac-sha256:fe3080b69d042a9eca2d392f8429412803f06dd3eb9e71fd16178d05e5971ac3"` |
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
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:a130e0b7f4696e3bc1ed555d0170b426ca57c7efed97c9c27766355dd842ec1c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:6da9164abc2800aec9b384c96483bc3bc128008df04704ad7050851f8b3f9a2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:52d7e4984062cff58f5ee2ab4592f4174277c11213b23be0f66b0da6c2801b15"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:b09664f79e8df7595b88db8e5d4fd40a678384e2b4816e04044a63b901c6dc3d"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:18eea61d82b38372f77e43b8596c93ef577d554d1cb4dba3545cd509026b1c2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:d829ae28c8f6422156149b7d293896efb88703427b4b31d13996703e67d35aae"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:41770f394bc6316c571ecb74ac4e07554113bb8f92d0c56603009a81daeeff12"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:3913f4a00a32e7b06211da44f3d156e37509bf8aefde1ba61f221717eaae8c8d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:aae75164d165f5a4c0e499d094250b126cb2c634f1f3c5a55226be1fd115c101"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:0a8b103130fe77d9b2a8d6f9ab9e4d69cc7146f7f342b859fdf9ce0c703fed5d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c40d9ce71dce69af2ccfd0c4396f6fcea650358a04107008cfa34ec73e82fc4"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:8167cf7b096bcf02b20dbc95d47de65bf2b7eb2902495b089aae8ad6cc2ffae7"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c808566f31ad17b61c8700c5ecf0e95be4fd01ca4b2edf3bb12f80f4de49255"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c45259baf1db3285bd3b9cb81d1637bfcd7ac34589868894e6ad63ee93577a0a"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c60be35d2fffdab2e6c81834408613d778914041c0ecd3f4a0f5be53541dc7bd"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:27864c18901ea515a772984044b552f7cb3a0d2a058bd1a67a9b53dc49c4ab5d"` |

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
| `["scope"]["dataset_versions"]` | `["hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4", "hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"]` |
| `["scope"]["denominator_basis"]` | `"all_validated_bundle_records"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 16 |
| `["scope"]["scope_id"]` | `"hmac-sha256:fe3080b69d042a9eca2d392f8429412803f06dd3eb9e71fd16178d05e5971ac3"` |
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
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:a130e0b7f4696e3bc1ed555d0170b426ca57c7efed97c9c27766355dd842ec1c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:6da9164abc2800aec9b384c96483bc3bc128008df04704ad7050851f8b3f9a2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:52d7e4984062cff58f5ee2ab4592f4174277c11213b23be0f66b0da6c2801b15"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:b09664f79e8df7595b88db8e5d4fd40a678384e2b4816e04044a63b901c6dc3d"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:18eea61d82b38372f77e43b8596c93ef577d554d1cb4dba3545cd509026b1c2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:d829ae28c8f6422156149b7d293896efb88703427b4b31d13996703e67d35aae"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:41770f394bc6316c571ecb74ac4e07554113bb8f92d0c56603009a81daeeff12"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:3913f4a00a32e7b06211da44f3d156e37509bf8aefde1ba61f221717eaae8c8d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:aae75164d165f5a4c0e499d094250b126cb2c634f1f3c5a55226be1fd115c101"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:0a8b103130fe77d9b2a8d6f9ab9e4d69cc7146f7f342b859fdf9ce0c703fed5d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c40d9ce71dce69af2ccfd0c4396f6fcea650358a04107008cfa34ec73e82fc4"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:8167cf7b096bcf02b20dbc95d47de65bf2b7eb2902495b089aae8ad6cc2ffae7"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c808566f31ad17b61c8700c5ecf0e95be4fd01ca4b2edf3bb12f80f4de49255"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c45259baf1db3285bd3b9cb81d1637bfcd7ac34589868894e6ad63ee93577a0a"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c60be35d2fffdab2e6c81834408613d778914041c0ecd3f4a0f5be53541dc7bd"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:27864c18901ea515a772984044b552f7cb3a0d2a058bd1a67a9b53dc49c4ab5d"` |

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
| `["scope"]["dataset_versions"]` | `["hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4", "hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"]` |
| `["scope"]["denominator_basis"]` | `"all_validated_bundle_records"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 16 |
| `["scope"]["scope_id"]` | `"hmac-sha256:fe3080b69d042a9eca2d392f8429412803f06dd3eb9e71fd16178d05e5971ac3"` |
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
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:a130e0b7f4696e3bc1ed555d0170b426ca57c7efed97c9c27766355dd842ec1c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:6da9164abc2800aec9b384c96483bc3bc128008df04704ad7050851f8b3f9a2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:52d7e4984062cff58f5ee2ab4592f4174277c11213b23be0f66b0da6c2801b15"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:b09664f79e8df7595b88db8e5d4fd40a678384e2b4816e04044a63b901c6dc3d"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:18eea61d82b38372f77e43b8596c93ef577d554d1cb4dba3545cd509026b1c2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:d829ae28c8f6422156149b7d293896efb88703427b4b31d13996703e67d35aae"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:41770f394bc6316c571ecb74ac4e07554113bb8f92d0c56603009a81daeeff12"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:3913f4a00a32e7b06211da44f3d156e37509bf8aefde1ba61f221717eaae8c8d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:aae75164d165f5a4c0e499d094250b126cb2c634f1f3c5a55226be1fd115c101"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:0a8b103130fe77d9b2a8d6f9ab9e4d69cc7146f7f342b859fdf9ce0c703fed5d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c40d9ce71dce69af2ccfd0c4396f6fcea650358a04107008cfa34ec73e82fc4"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:8167cf7b096bcf02b20dbc95d47de65bf2b7eb2902495b089aae8ad6cc2ffae7"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c808566f31ad17b61c8700c5ecf0e95be4fd01ca4b2edf3bb12f80f4de49255"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c45259baf1db3285bd3b9cb81d1637bfcd7ac34589868894e6ad63ee93577a0a"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c60be35d2fffdab2e6c81834408613d778914041c0ecd3f4a0f5be53541dc7bd"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:27864c18901ea515a772984044b552f7cb3a0d2a058bd1a67a9b53dc49c4ab5d"` |

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
| `["scope"]["dataset_versions"]` | `["hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4", "hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"]` |
| `["scope"]["denominator_basis"]` | `"all_validated_bundle_records"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 16 |
| `["scope"]["scope_id"]` | `"hmac-sha256:fe3080b69d042a9eca2d392f8429412803f06dd3eb9e71fd16178d05e5971ac3"` |
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
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:a130e0b7f4696e3bc1ed555d0170b426ca57c7efed97c9c27766355dd842ec1c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:6da9164abc2800aec9b384c96483bc3bc128008df04704ad7050851f8b3f9a2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:52d7e4984062cff58f5ee2ab4592f4174277c11213b23be0f66b0da6c2801b15"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:b09664f79e8df7595b88db8e5d4fd40a678384e2b4816e04044a63b901c6dc3d"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:18eea61d82b38372f77e43b8596c93ef577d554d1cb4dba3545cd509026b1c2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:d829ae28c8f6422156149b7d293896efb88703427b4b31d13996703e67d35aae"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:41770f394bc6316c571ecb74ac4e07554113bb8f92d0c56603009a81daeeff12"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:3913f4a00a32e7b06211da44f3d156e37509bf8aefde1ba61f221717eaae8c8d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:aae75164d165f5a4c0e499d094250b126cb2c634f1f3c5a55226be1fd115c101"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:0a8b103130fe77d9b2a8d6f9ab9e4d69cc7146f7f342b859fdf9ce0c703fed5d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c40d9ce71dce69af2ccfd0c4396f6fcea650358a04107008cfa34ec73e82fc4"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:8167cf7b096bcf02b20dbc95d47de65bf2b7eb2902495b089aae8ad6cc2ffae7"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c808566f31ad17b61c8700c5ecf0e95be4fd01ca4b2edf3bb12f80f4de49255"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c45259baf1db3285bd3b9cb81d1637bfcd7ac34589868894e6ad63ee93577a0a"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c60be35d2fffdab2e6c81834408613d778914041c0ecd3f4a0f5be53541dc7bd"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:27864c18901ea515a772984044b552f7cb3a0d2a058bd1a67a9b53dc49c4ab5d"` |

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
| `["scope"]["dataset_versions"]` | `["hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4", "hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"]` |
| `["scope"]["denominator_basis"]` | `"all_validated_bundle_records"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 16 |
| `["scope"]["scope_id"]` | `"hmac-sha256:fe3080b69d042a9eca2d392f8429412803f06dd3eb9e71fd16178d05e5971ac3"` |
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
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:a130e0b7f4696e3bc1ed555d0170b426ca57c7efed97c9c27766355dd842ec1c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:6da9164abc2800aec9b384c96483bc3bc128008df04704ad7050851f8b3f9a2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:52d7e4984062cff58f5ee2ab4592f4174277c11213b23be0f66b0da6c2801b15"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:b09664f79e8df7595b88db8e5d4fd40a678384e2b4816e04044a63b901c6dc3d"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:18eea61d82b38372f77e43b8596c93ef577d554d1cb4dba3545cd509026b1c2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:d829ae28c8f6422156149b7d293896efb88703427b4b31d13996703e67d35aae"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:41770f394bc6316c571ecb74ac4e07554113bb8f92d0c56603009a81daeeff12"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:3913f4a00a32e7b06211da44f3d156e37509bf8aefde1ba61f221717eaae8c8d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:aae75164d165f5a4c0e499d094250b126cb2c634f1f3c5a55226be1fd115c101"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:0a8b103130fe77d9b2a8d6f9ab9e4d69cc7146f7f342b859fdf9ce0c703fed5d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c40d9ce71dce69af2ccfd0c4396f6fcea650358a04107008cfa34ec73e82fc4"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:8167cf7b096bcf02b20dbc95d47de65bf2b7eb2902495b089aae8ad6cc2ffae7"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c808566f31ad17b61c8700c5ecf0e95be4fd01ca4b2edf3bb12f80f4de49255"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c45259baf1db3285bd3b9cb81d1637bfcd7ac34589868894e6ad63ee93577a0a"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c60be35d2fffdab2e6c81834408613d778914041c0ecd3f4a0f5be53541dc7bd"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:27864c18901ea515a772984044b552f7cb3a0d2a058bd1a67a9b53dc49c4ab5d"` |

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
| `["scope"]["dataset_versions"]` | `["hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4", "hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"]` |
| `["scope"]["denominator_basis"]` | `"all_validated_bundle_records"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 16 |
| `["scope"]["scope_id"]` | `"hmac-sha256:fe3080b69d042a9eca2d392f8429412803f06dd3eb9e71fd16178d05e5971ac3"` |
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
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:a130e0b7f4696e3bc1ed555d0170b426ca57c7efed97c9c27766355dd842ec1c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:6da9164abc2800aec9b384c96483bc3bc128008df04704ad7050851f8b3f9a2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:52d7e4984062cff58f5ee2ab4592f4174277c11213b23be0f66b0da6c2801b15"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:b09664f79e8df7595b88db8e5d4fd40a678384e2b4816e04044a63b901c6dc3d"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:18eea61d82b38372f77e43b8596c93ef577d554d1cb4dba3545cd509026b1c2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:d829ae28c8f6422156149b7d293896efb88703427b4b31d13996703e67d35aae"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:41770f394bc6316c571ecb74ac4e07554113bb8f92d0c56603009a81daeeff12"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:3913f4a00a32e7b06211da44f3d156e37509bf8aefde1ba61f221717eaae8c8d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:aae75164d165f5a4c0e499d094250b126cb2c634f1f3c5a55226be1fd115c101"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:0a8b103130fe77d9b2a8d6f9ab9e4d69cc7146f7f342b859fdf9ce0c703fed5d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c40d9ce71dce69af2ccfd0c4396f6fcea650358a04107008cfa34ec73e82fc4"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:8167cf7b096bcf02b20dbc95d47de65bf2b7eb2902495b089aae8ad6cc2ffae7"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c808566f31ad17b61c8700c5ecf0e95be4fd01ca4b2edf3bb12f80f4de49255"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c45259baf1db3285bd3b9cb81d1637bfcd7ac34589868894e6ad63ee93577a0a"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c60be35d2fffdab2e6c81834408613d778914041c0ecd3f4a0f5be53541dc7bd"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:27864c18901ea515a772984044b552f7cb3a0d2a058bd1a67a9b53dc49c4ab5d"` |

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
| `["scope"]["dataset_versions"]` | `["hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4", "hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"]` |
| `["scope"]["denominator_basis"]` | `"all_validated_bundle_records"` |
| `["scope"]["excluded_record_count"]` | 0 |
| `["scope"]["excluded_record_keys"]` | `[]` |
| `["scope"]["record_count"]` | 16 |
| `["scope"]["scope_id"]` | `"hmac-sha256:fe3080b69d042a9eca2d392f8429412803f06dd3eb9e71fd16178d05e5971ac3"` |
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
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:a130e0b7f4696e3bc1ed555d0170b426ca57c7efed97c9c27766355dd842ec1c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:6da9164abc2800aec9b384c96483bc3bc128008df04704ad7050851f8b3f9a2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:52d7e4984062cff58f5ee2ab4592f4174277c11213b23be0f66b0da6c2801b15"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:b09664f79e8df7595b88db8e5d4fd40a678384e2b4816e04044a63b901c6dc3d"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:18eea61d82b38372f77e43b8596c93ef577d554d1cb4dba3545cd509026b1c2c"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:d829ae28c8f6422156149b7d293896efb88703427b4b31d13996703e67d35aae"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:41770f394bc6316c571ecb74ac4e07554113bb8f92d0c56603009a81daeeff12"` |
| `"hmac-sha256:4e02dbb7e57fd003c1b4a2d16e058bca5c848e94f5b8730261ad64c1175dfef4"` | `"hmac-sha256:3913f4a00a32e7b06211da44f3d156e37509bf8aefde1ba61f221717eaae8c8d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:aae75164d165f5a4c0e499d094250b126cb2c634f1f3c5a55226be1fd115c101"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:0a8b103130fe77d9b2a8d6f9ab9e4d69cc7146f7f342b859fdf9ce0c703fed5d"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c40d9ce71dce69af2ccfd0c4396f6fcea650358a04107008cfa34ec73e82fc4"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:8167cf7b096bcf02b20dbc95d47de65bf2b7eb2902495b089aae8ad6cc2ffae7"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:7c808566f31ad17b61c8700c5ecf0e95be4fd01ca4b2edf3bb12f80f4de49255"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c45259baf1db3285bd3b9cb81d1637bfcd7ac34589868894e6ad63ee93577a0a"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:c60be35d2fffdab2e6c81834408613d778914041c0ecd3f4a0f5be53541dc7bd"` |
| `"hmac-sha256:70696b56c6ef6dbd4145752d88c4da6f71498a8f35a521e3946d89acc2a56a5d"` | `"hmac-sha256:27864c18901ea515a772984044b552f7cb3a0d2a058bd1a67a9b53dc49c4ab5d"` |

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
