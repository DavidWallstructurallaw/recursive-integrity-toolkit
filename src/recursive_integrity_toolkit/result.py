"""Immutable canonical report contracts and explicit safe output views.

Owner IDs:
    PR-012, PR-013, PR-014, PR-015, PR-016; field-specific owners are in FIELD_REGISTRY.
Theory Map IDs:
    Inherited through the declared T1-T6 or explicit product-rule field owners.
Inputs:
    Explicit public JSON-shaped data, never arbitrary calculation objects.
Outputs:
    Deeply immutable CanonicalReport and a locally defined Draft 2020-12 schema.
Assumptions:
    Values are supplied by their accepted owners. Validation is not computation.
Limits:
    No ingestion, classifier, metric, simulation, adapter, renderer or CLI runs.
    A valid contract does not certify the truth of supplied evidence.
Current phase status:
    Phase 4 Step 4 adds a safe-view wrapper; the Step 2 schema remains frozen.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
import math
import re
import sys
from types import MappingProxyType
from collections.abc import Mapping


class ReportEvidenceClass(StrEnum):
    OBSERVED_FACT = "observed_fact"
    DERIVED_METRIC = "derived_metric"
    PROXY_SIGNAL = "proxy_signal"
    SIMULATION = "simulation"
    UNAVAILABLE_CONCLUSION = "unavailable_conclusion"


class ReportStatus(StrEnum):
    AVAILABLE = "available"
    PARTIAL = "partial"
    UNAVAILABLE = "unavailable"
    EXPERIMENTAL = "experimental"


class ExecutionStatus(StrEnum):
    COMPLETED = "completed"
    PARTIAL = "partial"
    NOT_REQUESTED = "not_requested"
    DEFERRED = "deferred"
    FAILED = "failed"


class RunStatus(StrEnum):
    COMPLETE = "complete"
    PARTIAL = "partial"
    FAILED = "failed"


class ReportValidationError(ValueError):
    """A public report violates its structural or semantic contract."""


SECTION_ORDER = (
    "run", "inputs", "observability", "capabilities", "observed_facts",
    "derived_metrics", "proxy_signals", "simulations", "unavailable_conclusions",
    "recommended_next_metadata", "warnings", "errors",
)
CAPABILITY_KEYS = (
    "ingestion", "content_diagnostics", "provenance", "lineage",
    "dataset_longitudinal", "model_longitudinal", "intervention_simulation",
)
LEVEL_LABELS = (
    "ingest_observability", "content_or_representation_observability",
    "provenance_observability", "lineage_observability",
    "longitudinal_dataset_observability",
    "experimental_intervention_or_scenario_observability",
)
RUN_NULLABLE_FIELDS = (
    "started_at", "completed_at", "duration_seconds", "python_version", "platform",
    "command", "config_hash", "random_seed",
)


@dataclass(frozen=True, slots=True)
class FieldDefinition:
    path: str
    owner: str
    evidence_class: str
    unit: str
    method_id: str
    minimum_level: int
    value_type: str
    requires_representation: bool = False
    status_boundary: str = "current"


_field_entries: list[FieldDefinition] = []


def _text(*, empty: bool = False) -> dict:
    return {"type": "string", "minLength": 0 if empty else 1, "pattern": "^[^\\u0000]*$"}


def _enum(*values: str) -> dict:
    return {"type": "string", "enum": list(values)}


def _number(*, minimum: int | float = -sys.float_info.max,
            maximum: int | float = sys.float_info.max) -> dict:
    return {"type": "number", "minimum": minimum, "maximum": maximum,
            "oneOf": [{"minimum": 0}, {"exclusiveMaximum": 0}]}


def _integer(*, minimum: int = 0) -> dict:
    return {"type": "integer", "minimum": minimum, "maximum": sys.float_info.max}


def _nullable(schema: dict) -> dict:
    return {"anyOf": [schema, {"type": "null"}]}


def _array(item: dict, *, minimum: int = 0, unique: bool = False) -> dict:
    result = {"type": "array", "items": item, "minItems": minimum}
    if unique:
        result["uniqueItems"] = True
    return result


def _strings(*, minimum: int = 0) -> dict:
    return _array(_text(), minimum=minimum, unique=True)


def _object(properties: dict, required: tuple | list | None = None) -> dict:
    return {"type": "object", "properties": properties,
            "required": list(properties) if required is None else list(required),
            "additionalProperties": False}


def _map(values: dict) -> dict:
    return {"type": "object", "propertyNames": _text(empty=True), "additionalProperties": values}


def _ref(name: str) -> dict:
    return {"$ref": "#/$defs/" + name}


def _base_envelope(evidence: str, unit: str, owner: str, method: str) -> dict:
    return {
        "unit": {"const": unit}, "evidence_class": {"const": evidence},
        "status": _enum("available", "partial", "unavailable"),
        "method_id": {"const": method}, "owner_ids": {"const": [owner]},
        "theory_map_ids": _array(_enum("TM-M01", "TM-M02", "TM-M03", "TM-M04", "TM-M05", "TM-M06", "TM-M07", "TM-C01", "TM-C02", "TM-C03", "TM-C04", "TM-C05", "TM-C06", "TM-C07", "TM-C08", "TM-P01", "TM-P02", "TM-P03", "TM-P04", "TM-P05", "TM-S01", "TM-S02", "TM-S03", "TM-E01", "TM-E02", "TM-E03", "TM-E04", "TM-E05", "TM-A01", "TM-A02", "TM-A03", "TM-A04"), unique=True), "trace_ids": _array(_enum("T1", "T2", "T3", "T4", "T5", "T6"), unique=True),
        "scope": _ref("scope"), "representation": _nullable(_ref("representation")),
        "coverage": _nullable(_number(minimum=0, maximum=1)),
        "coverage_reason": _nullable(_text()),
        "denominator": _nullable(_number(minimum=0)),
        "denominator_reason": _nullable(_text()),
        "assumptions": _strings(), "limitations": _strings(),
        "reason_codes": _strings(), "required_evidence": _strings(),
    }


def _field(path: str, value: dict, *, owner: str, evidence: str,
           unit: str, method: str, level: int, value_type: str,
           representation: bool = False, boundary: str = "current") -> dict:
    _field_entries.append(FieldDefinition(path, owner, evidence, unit, method, level,
                                          value_type, representation, boundary))
    properties = {"value": _nullable(value), **_base_envelope(evidence, unit, owner, method)}
    required = tuple(properties)
    properties.update({"weighting": _ref("weighting"), "input_basis": _text(),
                       "redaction": _ref("redaction"), "method": _text()})
    result = _object(properties, required)
    result["allOf"] = [
        {"if": {"properties": {"status": {"const": "unavailable"}}},
         "then": {"properties": {"value": {"type": "null"}, "reason_codes": {"minItems": 1},
                                  "required_evidence": {"minItems": 1}}},
         "else": {"properties": {"value": value}}},
    ]
    if representation:
        result["allOf"].append({
            "if": {"properties": {"status": {"enum": ["available", "partial"]}}},
            "then": {"properties": {"representation": _ref("representation")}},
        })
    if boundary == "deferred_phase5":
        result["properties"]["status"] = {"const": "unavailable"}
    return result


def _metric(path: str, value: dict, owner: str, unit: str, method: str,
            level: int, value_type: str, *, representation: bool = False,
            boundary: str = "current") -> dict:
    return _field(path, value, owner=owner, evidence="derived_metric", unit=unit,
                  method=method, level=level, value_type=value_type,
                  representation=representation, boundary=boundary)


def _observed(path: str, value: dict, owner: str, unit: str, method: str,
              level: int, value_type: str, *, boundary: str = "current", representation: bool = False) -> dict:
    return _field(path, value, owner=owner, evidence="observed_fact", unit=unit,
                  method=method, level=level, value_type=value_type, boundary=boundary, representation=representation)


def _build_contract() -> dict:
    source_categories = ("human", "synthetic", "mixed", "sensor", "unknown")
    confidence_categories = ("confirmed", "log_derived", "estimated", "unknown")
    scope = _object({
        "dataset_versions": _strings(), "record_count": _nullable(_integer()),
        "excluded_record_count": _nullable(_integer()), "denominator_basis": _text(),
        "scope_id": _text(), "included_record_keys": _array(_ref("record_key"), unique=True),
        "excluded_record_keys": _array(_ref("record_key"), unique=True),
        "exclusions": _array(_object({"record_key": _ref("record_key"), "reason_codes": _strings(minimum=1)})),
    }, ("dataset_versions", "record_count", "excluded_record_count", "denominator_basis", "scope_id"))
    representation = _object({
        "representation_name": _text(), "representation_source": _text(),
        "representation_version": _text(), "binning_or_mapping_rule": _text(),
        "field_name": _nullable(_text()),
        "missing_value_policy": _enum("error", "exclude", "explicit_missing_state"),
        "missing_state_id": _nullable(_text()),
        "normalization_profile": _nullable({"const": "exact_utf8_v1"}),
    }, ("representation_name", "representation_source", "representation_version", "binning_or_mapping_rule"))
    coverage = _object({"numerator": _integer(), "denominator": _integer(),
                        "denominator_name": _text(), "ratio": _nullable(_number(minimum=0, maximum=1)),
                        "reason": _nullable(_text())})
    capabilities = _object({key: _ref("capability") for key in CAPABILITY_KEYS}, ())
    capabilities["anyOf"] = [{"maxProperties": 0}, {"required": list(CAPABILITY_KEYS)}]
    capability = _object({
        "status": _enum("available", "partial", "unavailable", "experimental"),
        "reason_codes": _strings(), "coverage": _nullable(_number(minimum=0, maximum=1)),
        "coverage_reason": _nullable(_text()), "requirements_met": _strings(),
        "requirements_missing": _strings(), "notes": _strings(),
        "execution_status": _enum(*(item.value for item in ExecutionStatus)),
        "execution_scope": _strings(), "execution_reason_codes": _strings(),
        "coverage_details": _object({key: _ref("coverage") for key in (
            "record_coverage", "representation_coverage", "provenance_row_coverage",
            "provenance_required_field_coverage", "grounding_field_coverage",
            "source_type_field_coverage", "provenance_confidence_field_coverage",
            "resolved_parent_edge_coverage", "resolved_lineage_coverage",
            "external_ancestry_coverage")}, ()),
    }, ("status", "reason_codes", "coverage", "coverage_reason", "requirements_met",
        "requirements_missing", "notes", "execution_status", "execution_scope", "execution_reason_codes"))
    run = _object({
        "run_id": _text(), "toolkit_version": _text(), "report_schema_version": {"const": "1.0"},
        "started_at": _nullable(_text()), "completed_at": _nullable(_text()),
        "duration_seconds": _nullable(_number(minimum=0)), "python_version": _nullable(_text()),
        "platform": _nullable(_text()), "command": _nullable(_text()),
        "config_hash": _nullable(_ref("sha256")), "random_seed": _nullable(_integer()),
        "strict_mode": {"type": "boolean"}, "redacted_mode": {"type": "boolean"},
        "network_call_count": _integer(), "deterministic": {"type": "boolean"},
        "privacy_mode": _enum("standard", "redacted"), "run_status": _enum("complete", "partial", "failed"),
        "null_reasons": _object({key: _text() for key in RUN_NULLABLE_FIELDS}, ()),
        "network_count_scope": {"const": "toolkit_managed_outbound_operations"},
        "hash_algorithm": {"const": "sha256"},
        "config_hash_exclusions": _strings(), "resolved_options": _ref("resolved_options"),
        "identifier_protection": _object({
            "algorithm": {"const": "HMAC-SHA-256"},
            "stability_scope": _enum("run", "cross_run"),
            "record_id_mode": _enum("preserve", "hash", "omit"),
            "limitations": _strings(minimum=1),
        }),
    }, ("run_id", "toolkit_version", "report_schema_version", *RUN_NULLABLE_FIELDS,
        "strict_mode", "redacted_mode", "network_call_count", "deterministic", "privacy_mode", "run_status", "null_reasons"))
    artifact = _object({
        "role": _enum("records_primary", "records_compare", "provenance_manifest", "schema_mapping", "config",
                      "version_order", "embedding_data", "external_reference"),
        "path": _nullable(_text()), "path_redacted": {"type": "boolean"},
        "format": _enum("csv", "jsonl", "parquet", "json", "toml", "npy"),
        "file_hash": _nullable(_ref("sha256")), "hash_algorithm": {"const": "sha256"},
        "size_bytes": _nullable(_integer()), "row_count": _nullable(_integer()),
        "dataset_versions": _strings(), "schema_fields": _strings(),
        "parse_status": _enum("completed", "partial", "failed", "not_requested"),
        "validation_status": _enum("completed", "partial", "failed", "not_requested"),
        "reason_codes": _strings(),
    })
    inputs = _object({
        "artifacts": _array(artifact),
        "file_hashes": _array(_object({"artifact_index": _integer(), "algorithm": {"const": "sha256"}, "value": _ref("sha256")})),
        "version_order": _strings(), "version_order_source": _nullable(_text()),
        "representation": _nullable(_ref("representation")), "scope": _ref("scope"),
        "schema_mapping": _object({
            "file_hash": _nullable(_ref("sha256")), "operations": _array(_object({
                "operation": _enum("rename", "trim", "cast_string", "cast_integer", "cast_float", "cast_boolean", "parse_datetime", "parse_json_list", "constant", "coalesce", "map_values", "normalize_whitespace", "lowercase", "uppercase"),
                "source_field": _nullable(_text()), "target_field": _text(),
            })), "fields_affected": _strings(), "unmapped_field_count": _integer(), "unsafe_operation_count": {"const": 0},
        }),
        "limitations": _strings(),
    }, ())
    observability = _object({
        "maximum_level": {"type": "integer", "minimum": 0, "maximum": 5},
        "level_label": _enum(*LEVEL_LABELS), "basis": _strings(), "limitations": _strings(),
        "partial_evidence": _strings(), "capabilities": _ref("capabilities"),
    }, ())
    observability["anyOf"] = [{"maxProperties": 0}, {"required": list(observability["properties"])}]
    counts = _observed("observed_facts.record_counts.*", _integer(), "PR-002", "records", "PR-002.record_count", 0, "integer")
    content = _object({name: _observed("observed_facts.content." + name, _integer(), "PR-006", unit, "PR-006." + name, 1, "integer")
                       for name, unit in (("duplicate_record_count", "records"), ("duplicate_group_count", "groups"))}, ())
    duplicate_group = _object({
        "group_id": _text(), "record_keys": _nullable(_array(_ref("record_key"), minimum=2, unique=True)),
        "record_count": _integer(minimum=2), "normalization_profile": {"const": "exact_utf8_v1"},
        "redaction": _ref("redaction"),
    }, ("group_id", "record_keys", "record_count", "normalization_profile"))
    duplicate_group["allOf"] = [{
        "if": {"properties": {"record_keys": {"type": "null"}}},
        "then": {"required": ["redaction"], "properties": {"redaction": {"const": {
            "omitted_fields": ["record_keys"], "reason": "redacted_identity_details",
        }}}},
        "else": {"properties": {"redaction": False}},
    }]
    content["properties"]["exact_duplicate_groups"] = _observed(
        "observed_facts.content.exact_duplicate_groups", _array(duplicate_group),
        "PR-006", "groups", "PR-006.exact_duplicate_groups", 1, "duplicate_group[]")
    provenance = {}
    for name in ("provenance_row_coverage", "provenance_required_field_coverage", "grounding_field_coverage",
                 "source_type_field_coverage", "provenance_confidence_field_coverage"):
        provenance[name] = _observed("observed_facts.provenance." + name, _number(minimum=0, maximum=1),
                                     "PR-004", "ratio", "F-008" if name == "provenance_row_coverage" else "PR-004." + name, 2, "ratio")
    for name, owner, cats in (("source_type_counts", "PR-005", source_categories),
                              ("provenance_confidence_counts", "PR-004", confidence_categories)):
        provenance[name] = _observed("observed_facts.provenance." + name,
                                     _object({key: _integer() for key in cats}), owner, "records",
                                     owner + "." + name, 2, "category_count_map")
    for name in ("analyzed_record_count", "records_with_matching_rows", "missing_provenance_count"):
        provenance[name] = _observed("observed_facts.provenance." + name, _integer(), "PR-004", "records", "PR-004." + name, 2, "integer")
    for name in ("known_open_count", "known_closed_count", "unresolved_grounding_count"):
        provenance[name] = _observed("observed_facts.provenance." + name, _integer(), "T3", "records", "T3.direct_grounding_classification", 2, "integer")
    observed_lineage = {name: _observed("observed_facts.lineage." + name, _integer(), "PR-008", "edges", "PR-008." + name, 3, "integer")
                        for name in ("declared_parent_edge_count", "resolved_parent_edge_count", "unresolved_parent_edge_count")}
    observed_lineage["cycle_status"] = _observed("observed_facts.lineage.cycle_status", _enum("acyclic", "cyclic"),
                                                "T6", "status", "T6.graph_cycle_check", 3, "enum", boundary="deferred_phase5")
    observed_lineage["ordering_certificate"] = _observed("observed_facts.lineage.ordering_certificate", _object({
        "method": {"const": "declared_earlier_version_order"}, "version_order": _strings(),
        "all_resolved_edges_follow_order": {"type": "boolean"},
    }), "PR-008", "certificate", "PR-008.earlier_version_certificate", 3, "ordering_certificate")
    state_count = _observed("observed_facts.state_counts.by_version.*", _array(_object({
        "state_id": _text(empty=True), "state_count": _integer(),
    })), "T1", "records", "T1.state_counts", 1, "state_count[]", representation=True)
    observed = _object({"record_counts": _map(counts), "content": content, "provenance": _object(provenance, ()),
                        "lineage": _object(observed_lineage, ()), "state_counts": _object({"by_version": _map(state_count)}, ())}, ())
    support_version = {}
    for name in ("support_size", "weighted_support_size"):
        support_version[name] = _metric("derived_metrics.support.by_version.*." + name, _integer(), "T1", "states", "F-002", 1, "integer", representation=True)
    support = {"by_version": _map(_object(support_version, ()))}
    for name, value, unit, method, value_type in (
        ("support_delta", {"type": "integer", "minimum": -sys.float_info.max, "maximum": sys.float_info.max}, "states", "F-005", "integer"),
        ("support_retention_ratio", _number(minimum=0, maximum=1), "ratio", "F-006", "ratio"),
        ("support_loss_count", _integer(), "states", "T1.support_set_difference", "integer"),
        ("support_added_count", _integer(), "states", "T1.support_set_difference", "integer"),
        ("extinct_states", _array(_text(empty=True), unique=True), "set_of_states", "T1.earlier_minus_later", "state_id[]"),
        ("added_states", _array(_text(empty=True), unique=True), "set_of_states", "T1.later_minus_earlier", "state_id[]"),
        ("retained_states", _array(_text(empty=True), unique=True), "set_of_states", "T1.support_intersection", "state_id[]"),
    ):
        support[name] = _metric("derived_metrics.support." + name, value, "T1", unit, method, 4, value_type, representation=True)
    comparison_details = _object({
        "earlier_version": _text(), "later_version": _text(), "version_order": _strings(minimum=2),
        "version_order_source": _text(), "earlier_state_semantics": _text(), "later_state_semantics": _text(),
        "harmonized_state_semantics": _text(), "compatibility_method": _text(),
        "earlier_representation": _ref("representation"), "later_representation": _ref("representation"),
        "harmonized_representation": _ref("representation"),
        "original_earlier_support": _array(_text(empty=True), unique=True),
        "original_later_support": _array(_text(empty=True), unique=True),
        "harmonized_earlier_support": _array(_text(empty=True), unique=True),
        "harmonized_later_support": _array(_text(empty=True), unique=True),
        "retention_denominator": _nullable(_integer()), "retention_denominator_basis": _text(),
        "state_mapping": _array(_object({"source_state": _text(empty=True), "target_state": _text(empty=True)})),
        "mapping_effect": _array(_object({"dataset_version": _text(), "original_support_size": _nullable(_integer()), "harmonized_support_size": _nullable(_integer())})),
        "collision_groups": _array(_object({"target_state": _text(empty=True), "source_states": _array(_text(empty=True), minimum=2, unique=True)})),
    })
    support["comparison_details"] = _metric("derived_metrics.support.comparison_details", comparison_details, "T1", "comparison", "T1.explicit_pair_basis", 4, "comparison_basis", representation=True)
    diversity_version = {}
    for name, method in (("gini_simpson_diversity", "F-003"), ("simpson_concentration", "F-004"),
                         ("weighted_gini_simpson_diversity", "F-003"), ("weighted_simpson_concentration", "F-004")):
        diversity_version[name] = _metric("derived_metrics.diversity.by_version.*." + name, _number(minimum=0, maximum=1), "T1", "dimensionless", method, 1, "ratio", representation=True)
    for name in ("state_frequencies", "weighted_state_frequencies"):
        diversity_version[name] = _metric("derived_metrics.diversity.by_version.*." + name,
            _array(_object({"state_id": _text(empty=True), "state_frequency": _number(minimum=0, maximum=1)})),
            "T1", "ratio", "F-001", 1, "state_frequency[]", representation=True)
    diversity_version["weighted_state_masses"] = _metric("derived_metrics.diversity.by_version.*.weighted_state_masses",
        _array(_object({"state_id": _text(empty=True), "state_mass": _number(minimum=0)})),
        "T1", "user_declared_weight_mass", "T1.state_weight_mass", 1, "state_mass[]", representation=True)
    probability_basis = _observed("observed_facts.supplied_state_probabilities.by_version.*",
        _array(_ref("state_probability")), "T1", "ratio", "T1.supplied_probability_vector", 1, "state_probability[]", representation=True)
    observed["properties"]["supplied_state_probabilities"] = _object({"by_version": _map(probability_basis)}, ())
    diversity_version["distribution_basis"] = _metric("derived_metrics.diversity.by_version.*.distribution_basis", _object({
        "input_basis": _enum("empirical_assignments", "explicit_counts_divided_by_included_records", "weighted_record_mass", "explicit_probability_vector"),
        "analyzed_record_count": _integer(), "frequency_denominator": _nullable(_number(minimum=0)),
        "denominator_basis": _text(), "supplied_probability_total": _nullable(_number(minimum=0)),
        "probability_residual": _nullable(_number()), "numerical_policy": _ref("numerical_policy"),
    }), "T1", "basis", "T1.validated_distribution_basis", 1, "distribution_basis", representation=True)
    diversity = _object({"by_version": _map(_object(diversity_version, ())),
        "gini_simpson_diversity_delta": _metric("derived_metrics.diversity.gini_simpson_diversity_delta", _number(minimum=-1, maximum=1), "T1", "dimensionless", "F-018", 4, "number", representation=True)}, ())
    tail = {
        "tail_support_size": _metric("derived_metrics.tail.tail_support_size", _integer(), "T2", "states", "T2.declared_tail_rule", 1, "integer", representation=True),
        "tail_record_share": _metric("derived_metrics.tail.tail_record_share", _number(minimum=0, maximum=1), "T2", "ratio", "T2.tail_record_share", 1, "ratio", representation=True),
        "rarity_ranking": _metric("derived_metrics.tail.rarity_ranking", _array(_object({
            "state_id": _text(empty=True), "state_count": _integer(minimum=1),
            "state_frequency": _number(minimum=0, maximum=1), "rarity_rank": _integer(minimum=1), "in_tail": {"type": "boolean"},
        })), "T2", "ordinal_rank", "T2.frequency_count_unicode_order", 1, "rarity_entry[]", representation=True),
        "tail_states": _metric("derived_metrics.tail.tail_states", _array(_text(empty=True), unique=True), "T2", "set_of_states", "T2.declared_tail_rule", 1, "state_id[]", representation=True),
        "tail_rule": _enum("singleton_count", "count_at_or_below", "frequency_at_or_below", "state_list"),
        "selection": _ref("tail_selection"),
    }
    provenance_metrics = {}
    for name, unit, value, method in (
        ("source_type_shares", "ratio", _object({key: _number(minimum=0, maximum=1) for key in source_categories}), "F-007"),
        ("weighted_source_type_shares", "ratio", _object({key: _number(minimum=0, maximum=1) for key in source_categories}), "F-007"),
        ("weighted_source_type_masses", "user_declared_weight_mass", _object({key: _number(minimum=0) for key in source_categories}), "PR-005.source_weight_mass"),
        ("total_weight", "user_declared_weight_mass", _number(minimum=0), "PR-005.total_weight"),
        ("missing_provenance_weight", "user_declared_weight_mass", _number(minimum=0), "PR-005.missing_provenance_weight"),
        ("missing_provenance_share", "ratio", _number(minimum=0, maximum=1), "PR-004.one_minus_row_coverage"),
        ("weighted_missing_provenance_share", "ratio", _number(minimum=0, maximum=1), "PR-005.missing_provenance_weight_share"),
    ):
        owner = "PR-004" if name == "missing_provenance_share" else "PR-005"
        provenance_metrics[name] = _metric("derived_metrics.provenance." + name, value, owner, unit, method, 2,
                                           "category_ratio_map" if "shares" in name else "number")
    direct = {name: _metric("derived_metrics.closure_exposure.direct." + name,
        _number(minimum=0, maximum=1), "T3", "ratio", method, 2, "ratio") for name, method in (
            ("lower_bound", "F-009"), ("upper_bound", "F-010"), ("interval_width", "T3.upper_minus_lower"))}
    direct["classification_basis"] = {"const": "toolkit_operationalization"}
    direct["confidence_disclosure"] = {"const": "provenance_confidence_is_separate_and_does_not_discount_grounding"}
    lineage_bounds = {name: _metric("derived_metrics.closure_exposure.lineage." + name, _number(minimum=0, maximum=1), "T3", "ratio", "T3.lineage_closure", 3, "ratio", boundary="deferred_phase5") for name in ("lower_bound", "upper_bound", "interval_width")}
    lineage = {}
    for name, owner, unit, method, value, value_type in (
        ("resolved_parent_edge_coverage", "PR-008", "ratio", "PR-008.resolved_edges_over_declared", _number(minimum=0, maximum=1), "ratio"),
        ("resolved_lineage_coverage", "T4", "ratio", "T4.resolved_records_over_scope", _number(minimum=0, maximum=1), "ratio"),
        ("external_ancestry_coverage", "T4", "ratio", "T4.external_roots_over_scope", _number(minimum=0, maximum=1), "ratio"),
        ("distinct_external_root_count", "T4", "roots", "T4.root_set_union", _integer(), "integer"),
        ("top_shared_ancestors", "T4", "records", "T4.incidence_ranking", _array(_object({"record_key": _ref("record_key"), "incidence_count": _integer()})), "ancestor_incidence[]"),
        ("ancestry_concentration_hhi", "T4", "ratio", "F-012", _number(minimum=0, maximum=1), "ratio"),
        ("effective_external_root_count", "T4", "roots", "F-013", _number(minimum=0), "number"),
        ("lineage_depth", "PR-009", "edges", "PR-009.maximum_resolved_parent_depth", _integer(), "integer"),
    ):
        lineage[name] = _metric("derived_metrics.lineage." + name, value, owner, unit, method, 3, value_type,
                                boundary="current" if name == "resolved_parent_edge_coverage" else "deferred_phase5")
    derived = _object({"support": _object(support, ()), "diversity": diversity, "tail": _object(tail, ()),
                      "provenance": _object(provenance_metrics, ()),
                      "closure_exposure": _object({"direct": _object(direct, ()), "lineage": _object(lineage_bounds, ())}, ()),
                      "lineage": _object(lineage, ())}, ())
    proxies = {}
    for name, owner, level in (("support_contraction", "T1", 4), ("tail_fragility", "T2", 1),
                                ("shared_ancestry_dependence", "T4", 3), ("provenance_uncertainty", "T3", 2)):
        props = _base_envelope("proxy_signal", "signal", owner, owner + "." + name)
        props.update({"signal": {"const": name}, "level": _enum("present", "not_present", "indeterminate"),
                      "basis_fields": _strings(minimum=1), "trigger_rule": _text()})
        props["limitations"] = _strings(minimum=1)
        if name == "shared_ancestry_dependence":
            props["status"] = {"const": "unavailable"}
            props["level"] = {"const": "indeterminate"}
            props["reason_codes"] = _strings(minimum=1)
            props["required_evidence"] = _strings(minimum=1)
        proxies[name] = _object(props)
        proxies[name]["allOf"] = [{
            "if": {"properties": {"status": {"const": "unavailable"}}},
            "then": {"properties": {"level": {"const": "indeterminate"},
                                      "reason_codes": {"minItems": 1}, "required_evidence": {"minItems": 1}}},
        }]
        _field_entries.append(FieldDefinition("proxy_signals." + name, owner, "proxy_signal", "signal", owner + "." + name, level, "proxy", False,
                                               "deferred_phase5" if name == "shared_ancestry_dependence" else "current"))
    simulations = {}
    for name, owner, level in (("closed_resampling", "T1", 5), ("tail_extinction", "T2", 1)):
        props = _base_envelope("simulation", "scenario", owner, owner + "." + name)
        props.update({"status": {"const": "experimental"}, "model": {"const": "closed_resampling"},
                      "model_version": _text(), "method": _enum("analytic_expectation", "analytic_extinction", "sampled_path"),
                      "parameters": _ref("simulation_parameters"), "initial_distribution": _array(_ref("state_probability")),
                      "resample_size": _integer(minimum=1)})
        props["assumptions"] = _strings(minimum=1)
        props["limitations"] = _strings(minimum=1)
        props["representation"] = _ref("representation")
        required = tuple(props)
        if name == "tail_extinction":
            props["method"] = {"const": "analytic_extinction"}
            props["by_state"] = _map(_object({
                "observed_frequency": _number(minimum=0, maximum=1),
                "one_step_extinction_probability": _number(minimum=0, maximum=1),
                "numerical_underflow": {"type": "boolean"},
            }))
            props["by_state"]["minProperties"] = 1
            required += ("by_state",)
        else:
            props["method"] = _enum("analytic_expectation", "sampled_path")
            props.update({
                "initial_gini_simpson_diversity": _number(minimum=0, maximum=1),
                "contraction_factor": _number(minimum=0, maximum=1),
                "expected_diversity": _array(_number(minimum=0, maximum=1)),
                "numerical_underflow_steps": _array(_integer(), unique=True),
                "sampled_paths": _array(_ref("sampled_path")),
                "support_trajectories": _array(_object({"replicate_index": _integer(), "support_sizes": _array(_integer())})),
                "extinction_events": _array(_object({"replicate_index": _integer(), "step": _integer(minimum=1), "state_id": _text(empty=True)})),
                "input_normalization": _ref("input_normalization"),
            })
        simulations[name] = _object(props, required)
        _field_entries.append(FieldDefinition("simulations." + name, owner, "simulation", "scenario", owner + "." + name, level, "scenario", True))
    simulations["external_reopening"] = False
    _field_entries.append(FieldDefinition("simulations.external_reopening", "T5", "simulation", "scenario", "T5.external_reopening", 5, "reserved", True, "registered_future"))
    unavailable_owners = {
        "model_performance_decline": "PR-014", "causal_ancestor_effect": "T4",
        "correlated_semantic_error": "T4", "production_failure": "T1",
        "universal_integrity": "PR-014", "universal_quality": "PR-014", "universal_stability": "PR-014",
        "universal_entropy_score": "PR-014", "universal_collapse_prediction": "PR-014",
        "empirical_intervention_effect": "T5", "amplification_threshold": "PR-014",
        "lineage_analysis": "PR-014", "lineage_closure_exposure": "T3", "external_ancestry": "T4", "complete_pipeline_closure": "T3",
    }
    unavailable_variants = []
    for name, owner in unavailable_owners.items():
        props = _base_envelope("unavailable_conclusion", "conclusion", owner, owner + ".unavailable_conclusion")
        props.update({"conclusion": {"const": name}, "status": {"const": "unavailable"}, "statement": _text(),
                      "reason_codes": _strings(minimum=1), "required_evidence": _strings(minimum=1),
                      "blocking_evidence": _strings(minimum=1), "required_next_metadata": _strings(minimum=1),
                      "related_capability": _enum(*CAPABILITY_KEYS), "theory_or_product_limit": _text()})
        unavailable_variants.append(_object(props))
        _field_entries.append(FieldDefinition("unavailable_conclusions[]." + name, owner, "unavailable_conclusion", "conclusion", owner + ".unavailable_conclusion", 0, "unavailable"))
    location = _object({"file_role": _nullable(_text()), "field": _nullable(_text()),
                        "record_key": _nullable(_ref("record_key")), "row_number": _nullable(_integer(minimum=1)),
                        "line_number": _nullable(_integer(minimum=1))})
    warning = _object({"code": _text(), "message": _text(), "count": _integer(minimum=1),
                       "affected_scope": _ref("scope"), "representative_locations": _array(_ref("location")),
                       "effect_on_capabilities": _array(_enum(*CAPABILITY_KEYS), unique=True), "remediation": _strings(),
                       "coverage": _nullable(_ref("coverage")),
                       "severity": {"const": "warning"}},
                      ("code", "message", "count", "affected_scope", "representative_locations", "effect_on_capabilities", "remediation"))
    error = _object({"code": _text(), "severity": _enum("error", "fatal"), "message": _text(),
                     "file_role": _nullable(_text()), "field": _nullable(_text()), "record_key": _nullable(_ref("record_key")),
                     "row_number": _nullable(_integer(minimum=1)), "effect_on_run": _enum("partial", "failed"),
                     "effect_on_capabilities": _array(_enum(*CAPABILITY_KEYS), unique=True), "remediation": _strings()})
    defs = {
        "sha256": {"type": "string", "minLength": 64, "maxLength": 64, "pattern": "^[0-9a-f]{64}$"},
        "record_key": _object({"dataset_version": _text(), "record_id": _text()}),
        "scope": scope, "representation": representation, "coverage": coverage,
        "capability": capability, "capabilities": capabilities,
        "weighting": _object({"weighting_mode": _enum("unweighted", "weighted"), "weight_field": _nullable({"const": "weight"})}),
        "redaction": _object({"omitted_fields": _strings(minimum=1), "reason": {"const": "redacted_identity_details"}}),
        "tail_selection": _object({"rule": _enum("singleton_count", "count_at_or_below", "frequency_at_or_below", "state_list"),
            "count_threshold": _nullable(_integer()), "frequency_threshold": _nullable(_number(minimum=0, maximum=1)),
            "state_ids": _array(_text(empty=True), unique=True),
            "ranking_rule": {"const": "ascending_frequency_then_count_then_unicode_state_id"}}),
        "resolved_options": _object({"strict_mode": {"type": "boolean"}, "privacy_mode": _enum("standard", "redacted"),
            "record_id_mode": _enum("preserve", "hash", "omit"), "representation": _nullable(_ref("representation")),
            "tail_selection": _nullable(_ref("tail_selection")), "version_order": _strings(),
            "state_meaning": _nullable(_text()), "weighted": {"type": "boolean"},
            "comparison_requested": {"type": "boolean"}, "scenario_requested": {"type": "boolean"}}, ()),
        "state_probability": _object({"state_id": _text(empty=True), "probability": _number(minimum=0, maximum=1)}),
        "simulation_parameters": _object({
            "resample_size": _integer(minimum=1), "simulation_horizon": _integer(),
            "random_seed": _nullable(_integer()), "simulation_replicates": _nullable(_integer(minimum=1)),
            "rng_name": _nullable({"const": "numpy.random.Generator(PCG64)"}), "numpy_version": _nullable(_text()),
            "replicate_schedule": _nullable({"const": "replicate_major_step_major"}),
            "state_order": _array(_text(empty=True), unique=True), "input_basis": _text(),
            "reopening_weight": _nullable(_number(minimum=0, maximum=1)),
            "external_input_distribution": _array(_ref("state_probability")),
            "numerical_policy": _ref("numerical_policy"),
        }),
        "numerical_policy": _object({"absolute_tolerance": {"const": 1e-12}, "relative_tolerance": {"const": 1e-12}, "probability_mass_tolerance": {"const": 1e-12}}),
        "sampled_path": _object({"replicate_index": _integer(), "generations": _array(_object({
            "step": _integer(), "state_counts": _nullable(_array(_integer())),
            "state_frequencies": _array(_number(minimum=0, maximum=1)), "support": _array(_text(empty=True), unique=True),
            "support_size": _integer(), "gini_simpson_diversity": _number(minimum=0, maximum=1),
        }))}),
        "input_normalization": _object({
            "supplied_distribution": _array(_ref("state_probability")), "effective_distribution": _array(_ref("state_probability")),
            "supplied_probability_total": _number(minimum=0), "effective_probability_total": _number(minimum=0),
            "probability_residual": _number(), "correction_applied": {"type": "boolean"}, "correction_method": _text(),
            "normalization_divisor": _number(minimum=0), "probability_corrections": _array(_object({"state_id": _text(empty=True), "correction": _number()})),
        }),
        "location": location,
    }
    schema = _object({"run": run, "inputs": inputs, "observability": observability,
        "capabilities": _ref("capabilities"), "observed_facts": observed, "derived_metrics": derived,
        "proxy_signals": _object(proxies, ()), "simulations": _object(simulations, ()),
        "unavailable_conclusions": _array({"oneOf": unavailable_variants}),
        "recommended_next_metadata": _array(_object({"priority": _integer(minimum=1), "metadata": _text(),
            "scope": _text(), "expected_unlock": _strings(minimum=1), "reason": _text(), "owner_ids": {"const": ["PR-014"]}},
            ("priority", "metadata", "scope", "expected_unlock", "reason"))),
        "warnings": _array(warning), "errors": _array(error)})
    return {"$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": "https://recursive-integrity-toolkit.example/schemas/report.schema.json",
            "title": "Recursive Integrity Toolkit canonical report 1.0",
            "description": "Phase 4 Step 2 public contract. Product metadata and five analytical evidence classes remain separate.",
            **schema, "$defs": defs}


_REPORT_SCHEMA = _build_contract()
FIELD_REGISTRY = tuple(_field_entries)
del _field_entries


def _freeze(value):
    if type(value) is dict:
        return MappingProxyType({key: _freeze(item) for key, item in value.items()})
    if type(value) is list:
        return tuple(_freeze(item) for item in value)
    return value


def _thaw(value):
    if isinstance(value, Mapping):
        return {key: _thaw(item) for key, item in value.items()}
    if type(value) is tuple or type(value) is list:
        return [_thaw(item) for item in value]
    return value


_REPORT_SCHEMA = _freeze(_REPORT_SCHEMA)


def report_schema() -> dict:
    """Return a detached schema. No external file, URI or schema resolver is used."""
    return _thaw(_freeze(_REPORT_SCHEMA))


def _fail(path: str, rule: str) -> None:
    # Paths contain only contract field names and indices, never raw instance text.
    raise ReportValidationError(f"{path}: {rule}")


def _json_input(value, path: str = "$", active: set | None = None) -> None:
    if active is None:
        active = set()
    if type(value) not in (dict, list, str, int, float, bool, type(None)):
        _fail(path, "requires built-in JSON data")
    if type(value) in (int, float):
        try:
            finite = math.isfinite(value)
        except OverflowError:
            finite = False
        if not finite:
            _fail(path, "number must be finite")
    elif type(value) is str:
        try:
            value.encode("utf-8")
        except UnicodeEncodeError:
            _fail(path, "text must be valid UTF-8")
        if "\x00" in value:
            _fail(path, "text must not contain NUL")
    elif type(value) in (dict, list):
        if id(value) in active:
            _fail(path, "recursive data is not JSON")
        active.add(id(value))
        items = value.items() if type(value) is dict else enumerate(value)
        for key, item in items:
            if type(value) is dict:
                if type(key) is not str:
                    _fail(path, "object keys must be literal text")
                _json_input(key, path + ".<key>", active)
            _json_input(item, path + ".<item>", active)
        active.remove(id(value))


def _same(left, right) -> bool:
    if type(left) in (int, float) and type(right) in (int, float):
        return left == right
    if type(left) in (list, tuple) and type(right) in (list, tuple):
        return len(left) == len(right) and all(_same(a, b) for a, b in zip(left, right))
    if isinstance(left, Mapping) and isinstance(right, Mapping):
        return set(left) == set(right) and all(_same(left[key], right[key]) for key in left)
    return type(left) is type(right) and left == right


def _equality_key(value):
    """Hashable JSON equality key; boolean identity never aliases a number."""
    if type(value) is dict:
        return ("object", frozenset((key, _equality_key(item)) for key, item in value.items()))
    if type(value) is list:
        return ("array", tuple(_equality_key(item) for item in value))
    if type(value) in (int, float):
        return ("number", value)
    if type(value) is bool:
        return ("boolean", value)
    if value is None:
        return ("null",)
    return ("string", value)


def _matches(value, schema: dict) -> bool:
    try:
        _check(value, schema, "$")
    except ReportValidationError:
        return False
    return True


def _check(value, schema: dict, path: str) -> None:
    if schema is False:
        _fail(path, "registered future field is unavailable in Phase 4")
    if "$ref" in schema:
        reference = schema["$ref"]
        if not reference.startswith("#/$defs/"):
            _fail(path, "external references are forbidden")
        _check(value, _REPORT_SCHEMA["$defs"][reference.removeprefix("#/$defs/")], path)
    if "const" in schema and not _same(value, schema["const"]):
        _fail(path, "fixed field value mismatch")
    if "enum" in schema and not any(_same(value, choice) for choice in schema["enum"]):
        _fail(path, "value is outside the registered enum")
    expected = schema.get("type")
    valid_type = {
        "object": type(value) is dict, "array": type(value) is list,
        "string": type(value) is str, "boolean": type(value) is bool,
        "number": type(value) in (int, float), "null": value is None,
        "integer": type(value) is int or (type(value) is float and math.isfinite(value) and value.is_integer()),
    }
    if expected and not valid_type[expected]:
        _fail(path, "incorrect JSON type")
    if "anyOf" in schema and not any(_matches(value, item) for item in schema["anyOf"]):
        _fail(path, "no allowed contract variant matches")
    if "oneOf" in schema and sum(_matches(value, item) for item in schema["oneOf"]) != 1:
        _fail(path, "exactly one contract variant must match")
    for item in schema.get("allOf", ()):
        _check(value, item, path)
    if "if" in schema:
        branch = "then" if _matches(value, schema["if"]) else "else"
        if branch in schema:
            _check(value, schema[branch], path)
    if type(value) in (int, float):
        if "minimum" in schema and value < schema["minimum"]:
            _fail(path, "number below allowed minimum")
        if "maximum" in schema and value > schema["maximum"]:
            _fail(path, "number above allowed maximum")
        if "exclusiveMaximum" in schema and value >= schema["exclusiveMaximum"]:
            _fail(path, "number above exclusive maximum")
    if type(value) is str:
        if len(value) < schema.get("minLength", 0):
            _fail(path, "text is too short")
        if "maxLength" in schema and len(value) > schema["maxLength"]:
            _fail(path, "text is too long")
        if "pattern" in schema and re.search(schema["pattern"], value) is None:
            _fail(path, "text does not match the field format")
    if type(value) is list:
        if len(value) < schema.get("minItems", 0):
            _fail(path, "too few array items")
        if schema.get("uniqueItems"):
            identities = {_equality_key(item) for item in value}
            if len(identities) != len(value):
                _fail(path, "array items must be unique")
        for index, item in enumerate(value):
            if "items" in schema:
                _check(item, schema["items"], path + f"[{index}]")
    if type(value) is dict:
        if len(value) < schema.get("minProperties", 0):
            _fail(path, "too few object properties")
        if "maxProperties" in schema and len(value) > schema["maxProperties"]:
            _fail(path, "object must be empty")
        if any(key not in value for key in schema.get("required", ())):
            _fail(path, "required public field is missing")
        properties = schema.get("properties", {})
        additional = schema.get("additionalProperties", True)
        for key, item in value.items():
            if "propertyNames" in schema:
                _check(key, schema["propertyNames"], path + ".<key>")
            if key in properties:
                _check(item, properties[key], path + "." + key)
            elif additional is False:
                _fail(path, "unregistered public key")
            elif isinstance(additional, Mapping):
                _check(item, additional, path + ".<key>")


def _resolved_contract(value, contract):
    """Resolve local structural references, never names supplied as data."""
    if "$ref" in contract:
        return _resolved_contract(value, _REPORT_SCHEMA["$defs"][contract["$ref"].removeprefix("#/$defs/")])
    if "type" not in contract:
        for variant in contract.get("anyOf", contract.get("oneOf", ())):
            if _matches(value, variant):
                return _resolved_contract(value, variant)
    return contract


def _walk(value, path=(), contract=None):
    if contract is None:
        contract = _REPORT_SCHEMA
    contract = _resolved_contract(value, contract)
    yield path, value, contract
    if type(value) is dict:
        properties = contract.get("properties", {})
        additional = contract.get("additionalProperties", False)
        for key, item in value.items():
            child = properties.get(key, additional)
            if isinstance(child, Mapping):
                yield from _walk(item, path + (key,), child)
    elif type(value) is list and "items" in contract:
        for index, item in enumerate(value):
            yield from _walk(item, path + (index,), contract["items"])


def _check_nullable_reason(value: dict, name: str, reason_name: str, path: str) -> None:
    if (value[name] is None) != (value[reason_name] is not None):
        _fail(path, "null requires its reason; a present value cannot carry a null reason")


def _semantic_checks(payload: dict) -> None:
    run = payload["run"]
    null_fields = {key for key in RUN_NULLABLE_FIELDS if run[key] is None}
    if set(run["null_reasons"]) != null_fields:
        _fail("$.run.null_reasons", "must explain exactly the null run fields")
    if run["redacted_mode"] != (run["privacy_mode"] == "redacted"):
        _fail("$.run", "privacy mode and redacted flag disagree")
    if run["run_status"] == "complete" and payload["errors"]:
        _fail("$.run.run_status", "error-bearing report cannot claim complete")
    observability = payload["observability"]
    mirror = observability.get("capabilities", {})
    if mirror != payload["capabilities"]:
        _fail("$.observability.capabilities", "capability mirror differs from canonical matrix")
    if observability and observability["level_label"] != LEVEL_LABELS[int(observability["maximum_level"])]:
        _fail("$.observability.level_label", "level label disagrees with maximum level")
    for key, capability in payload["capabilities"].items():
        _check_nullable_reason(capability, "coverage", "coverage_reason", "$.capabilities")
        if capability["execution_status"] != "completed" and not capability["execution_reason_codes"]:
            _fail("$.capabilities", "noncompleted execution needs explicit reasons")
        if capability["execution_status"] in ("completed", "partial") and not capability["execution_scope"]:
            _fail("$.capabilities", "executed work must name its operation scope")
        if key == "lineage" and capability["execution_status"] in ("completed", "partial"):
            _fail("$.capabilities.lineage", "Phase 5 lineage execution is deferred")
    tail = payload["derived_metrics"].get("tail", {})
    if "tail_rule" in tail and "selection" in tail and tail["tail_rule"] != tail["selection"]["rule"]:
        _fail("$.derived_metrics.tail", "tail rule declarations disagree")
    for path, item, contract in _walk(payload):
        if type(item) is list and item and all(type(row) is dict for row in item):
            if path == ("simulations", "closed_resampling", "extinction_events"):
                event_ids = [(row["replicate_index"], row["step"], row["state_id"]) for row in item]
                if len(event_ids) != len(set(event_ids)):
                    _fail("$.table", "event composite identity must be unique")
            else:
                for identity in ("state_id", "source_state", "replicate_index"):
                    if all(identity in row for row in item):
                        identities = [row[identity] for row in item]
                        if len(identities) != len(set(identities)):
                            _fail("$.table", "typed table identity must be unique")
        if type(item) is not dict:
            continue
        if contract is _REPORT_SCHEMA["$defs"]["coverage"]:
            if item["numerator"] > item["denominator"]:
                _fail("$.coverage", "coverage numerator exceeds denominator")
            if item["denominator"] == 0:
                if item["ratio"] is not None or not item["reason"]:
                    _fail("$.coverage", "zero denominator needs unavailable ratio and reason")
            else:
                if item["ratio"] is None or item["reason"] is not None:
                    _fail("$.coverage", "positive denominator needs finite coverage")
                # Consistency check on a supplied ratio, never a computed report metric.
                if not math.isclose(item["ratio"] * item["denominator"], item["numerator"], rel_tol=1e-12, abs_tol=1e-12):
                    _fail("$.coverage", "coverage value disagrees with supplied count basis")
        if contract is _REPORT_SCHEMA["$defs"]["scope"]:
            versions = set(item["dataset_versions"])
            included = item.get("included_record_keys", [])
            excluded = item.get("excluded_record_keys", [])
            included_ids = {(key["dataset_version"], key["record_id"]) for key in included}
            excluded_ids = {(key["dataset_version"], key["record_id"]) for key in excluded}
            if included_ids & excluded_ids:
                _fail("$.scope", "included and excluded identities overlap")
            if any(key["dataset_version"] not in versions for key in included + excluded):
                _fail("$.scope", "record identity belongs to an undeclared version")
            if "included_record_keys" in item and item["record_count"] != len(included):
                _fail("$.scope", "included count and identities disagree")
            if "excluded_record_keys" in item and item["excluded_record_count"] != len(excluded):
                _fail("$.scope", "excluded count and identities disagree")
        if "evidence_class" in contract.get("properties", {}):
            _check_nullable_reason(item, "coverage", "coverage_reason", "$.envelope")
            _check_nullable_reason(item, "denominator", "denominator_reason", "$.envelope")
            if item["owner_ids"][0].startswith("T") and item["owner_ids"][0] not in item["trace_ids"]:
                _fail("$.envelope.trace_ids", "theory owner must appear in trace IDs")
            if item["status"] == "unavailable" and (not item["reason_codes"] or not item["required_evidence"]):
                _fail("$.envelope", "unavailable evidence requires reasons and required evidence")
            if item["status"] == "available" and item["reason_codes"]:
                _fail("$.envelope", "available result cannot carry unavailable reasons")
            versioned = (len(path) == 5 and path[:3] in (
                ("derived_metrics", "support", "by_version"),
                ("derived_metrics", "diversity", "by_version"),
            )) or (len(path) == 4 and path[:3] in (
                ("observed_facts", "state_counts", "by_version"),
                ("observed_facts", "supplied_state_probabilities", "by_version"),
            ))
            if versioned and item["scope"]["dataset_versions"] != [path[3]]:
                _fail("$.envelope.scope", "version key and declared scope disagree")
            if path[:2] == ("observed_facts", "record_counts") and item["scope"]["dataset_versions"] != [path[-1]]:
                _fail("$.observed_facts.record_counts", "version key and declared scope disagree")
            weighted = (len(path) == 5 and path[:3] in (
                ("derived_metrics", "support", "by_version"),
                ("derived_metrics", "diversity", "by_version"),
            ) and path[4] in ("weighted_support_size", "weighted_gini_simpson_diversity",
                "weighted_simpson_concentration", "weighted_state_frequencies", "weighted_state_masses")) or (
                len(path) == 3 and path[:2] == ("derived_metrics", "provenance") and path[2] in (
                    "weighted_source_type_shares", "weighted_source_type_masses", "total_weight",
                    "missing_provenance_weight", "weighted_missing_provenance_share"))
            if weighted and item.get("weighting") != {"weighting_mode": "weighted", "weight_field": "weight"}:
                _fail("$.envelope.weighting", "weighted companion requires explicit weight basis")
        if contract is _REPORT_SCHEMA["$defs"]["weighting"]:
            if (item["weighting_mode"] == "weighted") != (item["weight_field"] == "weight"):
                _fail("$.weighting", "weight field disagrees with weighting mode")
        if contract is _REPORT_SCHEMA["$defs"]["representation"]:
            if (item.get("missing_value_policy", "error") == "explicit_missing_state") != (item.get("missing_state_id") is not None):
                _fail("$.representation", "explicit missing-state policy requires its state ID")
        if contract is _REPORT_SCHEMA["$defs"]["tail_selection"]:
            rule = item["rule"]
            if (rule == "count_at_or_below") != (item["count_threshold"] is not None):
                _fail("$.tail_selection", "count threshold disagrees with selected rule")
            if (rule == "frequency_at_or_below") != (item["frequency_threshold"] is not None):
                _fail("$.tail_selection", "frequency threshold disagrees with selected rule")
            if (rule == "state_list") != bool(item["state_ids"]):
                _fail("$.tail_selection", "state list disagrees with selected rule")
    for family in ("direct", "lineage"):
        interval = payload["derived_metrics"].get("closure_exposure", {}).get(family, {})
        bound_names = ("lower_bound", "upper_bound", "interval_width") if family == "direct" else ("lower_bound", "upper_bound", "interval_width")
        present = [name for name in bound_names if name in interval]
        if present and len(present) != len(bound_names):
            _fail("$.derived_metrics.closure_exposure", "interval must retain all named endpoints and width")
        if not present:
            continue
        envelopes = [interval[name] for name in bound_names]
        first = envelopes[0]
        for entry in envelopes[1:]:
            for key in ("status", "scope", "representation", "coverage", "denominator", "reason_codes", "required_evidence"):
                if entry[key] != first[key]:
                    _fail("$.derived_metrics.closure_exposure", "interval components have inconsistent evidence basis")
        if first["status"] != "unavailable":
            lower, upper = interval["lower_bound"]["value"], interval["upper_bound"]["value"]
            if lower > upper:
                _fail("$.derived_metrics.closure_exposure", "interval lower bound exceeds upper bound")
            if family == "direct" and not math.isclose(interval["interval_width"]["value"], upper - lower, rel_tol=1e-12, abs_tol=1e-12):
                _fail("$.derived_metrics.closure_exposure", "interval width disagrees with endpoints")
    for name, scenario in payload["simulations"].items():
        parameters = scenario["parameters"]
        method = scenario["method"]
        if (name == "tail_extinction") != (method == "analytic_extinction"):
            _fail("$.simulations", "scenario family and method disagree")
        if scenario["resample_size"] != parameters["resample_size"]:
            _fail("$.simulations", "resample size declarations disagree")
        random_fields = ("random_seed", "simulation_replicates", "rng_name", "numpy_version", "replicate_schedule")
        if method == "sampled_path" and any(parameters[key] is None for key in random_fields):
            _fail("$.simulations", "sampled paths require seed and replay metadata")
        if method in ("analytic_extinction", "analytic_expectation") and any(parameters[key] is not None for key in random_fields):
            _fail("$.simulations", "analytic scenario cannot claim a random realization")
        results = scenario
        expected = {"analytic_extinction": ("by_state",),
                    "analytic_expectation": ("initial_gini_simpson_diversity", "contraction_factor", "expected_diversity", "numerical_underflow_steps"),
                    "sampled_path": ("sampled_paths",)}[method]
        if any(key not in results for key in expected):
            _fail("$.simulations.results", "selected method requires its typed result fields")
        if method == "analytic_extinction" and parameters["simulation_horizon"] != 1:
            _fail("$.simulations", "one-step extinction requires horizon one")
        if method == "analytic_expectation" and len(results["expected_diversity"]) != parameters["simulation_horizon"] + 1:
            _fail("$.simulations", "expectation trajectory length disagrees with horizon")
        if method == "sampled_path":
            if len(results["sampled_paths"]) != parameters["simulation_replicates"]:
                _fail("$.simulations", "path count disagrees with replicate count")
            if any(len(path_result["generations"]) != parameters["simulation_horizon"] + 1
                   for path_result in results["sampled_paths"]):
                _fail("$.simulations", "sampled trajectory length disagrees with horizon")
        if parameters["reopening_weight"] is not None or parameters["external_input_distribution"]:
            _fail("$.simulations", "closed model cannot contain external reopening parameters")


def validate_report(payload: dict) -> None:
    """Validate public structure and cross-field semantics without computing metrics."""
    _json_input(payload)
    _check(payload, _REPORT_SCHEMA, "$")
    _semantic_checks(payload)


@dataclass(frozen=True, slots=True, init=False)
class CanonicalReport:
    """Deeply immutable, detached snapshot of one fully validated public report."""

    sections: Mapping

    def __init__(self, payload: dict) -> None:
        validate_report(payload)
        ordered = {key: payload[key] for key in SECTION_ORDER}
        frozen = _freeze(ordered)
        if frozen["observability"]:
            shared_observability = MappingProxyType({
                **frozen["observability"], "capabilities": frozen["capabilities"],
            })
            frozen = MappingProxyType({**frozen, "observability": shared_observability})
        object.__setattr__(self, "sections", frozen)

    @classmethod
    def from_dict(cls, payload: dict) -> "CanonicalReport":
        return CanonicalReport(payload)

    def to_dict(self) -> dict:
        """Return detached public data; this is no calculation adapter or renderer."""
        return _thaw(self.sections)


class PrivacyMode(StrEnum):
    """The two approved Phase 4 output views; debug is not an output mode."""

    STANDARD = "standard"
    REDACTED = "redacted"


class RecordIdMode(StrEnum):
    PRESERVE = "preserve"
    HASH = "hash"
    OMIT = "omit"


@dataclass(frozen=True, slots=True, init=False, repr=False)
class SafeReportView:
    """An immutable, explicitly selected privacy view for later output sinks.

    Canonical validation alone does not make arbitrary narrative text safe. Use
    ``reports.assembly.privacy_view`` to create this boundary after calculation.
    This type is a programming contract, not protection against deliberate Python
    object introspection or reconstruction.
    """

    _report: CanonicalReport

    def __init__(self, *args, **kwargs) -> None:
        raise TypeError("create a SafeReportView through privacy_view")

    @classmethod
    def _from_safe_report(cls, report: CanonicalReport) -> "SafeReportView":
        if type(report) is not CanonicalReport:
            raise TypeError("safe view requires an exact canonical report")
        result = object.__new__(cls)
        object.__setattr__(result, "_report", report)
        return result

    @property
    def sections(self) -> Mapping:
        return self._report.sections

    @property
    def privacy_mode(self) -> PrivacyMode:
        return PrivacyMode(self.sections["run"]["privacy_mode"])

    @property
    def record_id_mode(self) -> RecordIdMode:
        protection = self.sections["run"].get("identifier_protection")
        return RecordIdMode.PRESERVE if protection is None else RecordIdMode(protection["record_id_mode"])

    def to_dict(self) -> dict:
        """Return a detached, already protected canonical payload."""
        return self._report.to_dict()
