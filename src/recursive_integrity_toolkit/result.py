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
    Phase 6B Step 4 adds explicit scenario evidence under schema 1.3.
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


def _lineage_details(item: dict) -> dict:
    """Bound identity-bearing diagnostics independently of analytical values."""
    items = _array(item)
    items["maxItems"] = 100
    result = _object({
        "items": _nullable(items), "total_count": _integer(),
        "returned_count": {**_integer(), "maximum": 100}, "omitted_count": _integer(),
        "limit": {"const": 100}, "detail_status": _enum("complete", "truncated", "omitted"),
        "omission_reasons": _array(_enum("diagnostic_limit", "redacted_identity_details"), unique=True),
    })
    result["allOf"] = [
        {"if": {"properties": {"detail_status": {"const": "omitted"}}},
         "then": {"properties": {"items": {"type": "null"}, "returned_count": {"const": 0},
                                   "omission_reasons": {"minItems": 1}}},
         "else": {"properties": {"items": items}}},
        {"if": {"properties": {"detail_status": {"const": "complete"}}},
         "then": {"properties": {"omitted_count": {"const": 0}, "omission_reasons": {"maxItems": 0}}}},
        {"if": {"properties": {"detail_status": {"const": "truncated"}}},
         "then": {"properties": {"omitted_count": {"minimum": 1},
                                   "returned_count": {"const": 100},
                                   "omission_reasons": {"const": ["diagnostic_limit"]}}}},
    ]
    return result


def _scenario_assumption_table(reopened: bool) -> list[dict]:
    rows = [
        ("Fixed state space", "One declared representation and shared state meaning.",
         "Declared state meaning is supplied by the caller."),
        ("Multinomial transition", "Each sampled step contains the constant declared resample size.",
         "Simulation steps are distinct from observed dataset generations."),
        ("Input basis", "Explicit supplied probability vectors with retained numerical corrections.",
         "The initial distribution is not inferred from audit records."),
        ("Replay schedule", "The same seed is reset independently for each selected model.",
         "Matching replicate indices do not establish common-random-number precision."),
        ("Numerical corrections", "Supplied and effective vectors, totals and correction entries are retained.",
         "Replay requires the recorded sampler and compatible NumPy environment."),
    ]
    if reopened:
        rows.extend((
            ("Constant external input", "The declared external distribution and reopening weight remain constant.",
             "Positive source probability permits re-entry without guaranteeing a sampled count."),
            ("External quality", "External independence, reliability and relevance remain supplied assumptions.",
             "No empirical intervention effect or integrity score is established."),
        ))
    else:
        rows.append(("Closed source", "Every transition resamples its preceding internal state.",
                     "No mutation, migration or external corrective input is modeled."))
    return [{"assumption": rule, "declaration": declaration, "limitation": limitation}
            for rule, declaration, limitation in rows]


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


LONGITUDINAL_FAMILIES = ("distribution", "provenance", "direct_closure", "tail", "lineage")


def _series_field(path: str, value: dict, owner: str, unit: str, method: str,
                  *, observed: bool = False, pair: bool = False, delta: bool = False,
                  representation: bool = False) -> dict:
    """Keep ordinary envelope meaning while storing report-local references."""
    result = _field(path, value, owner=owner,
                    evidence="observed_fact" if observed else "derived_metric",
                    unit=unit, method=method, level=4, value_type="longitudinal_value",
                    representation=False)
    properties = result["properties"]
    del properties["scope"], properties["representation"]
    properties.update({"scope_id": _nullable(_text()), "basis_id": _nullable(_text())})
    properties["weighting"] = {"const": {"weighting_mode": "unweighted", "weight_field": None}}
    properties["input_basis"] = {"const": "empirical_assignments"}
    properties["theory_map_ids"] = {"const": []}
    properties["trace_ids"] = {"const": [owner] if owner.startswith("T") else []}
    required = [key for key in result["required"] if key not in ("scope", "representation")]
    required.extend(("scope_id", "basis_id", "weighting", "input_basis"))
    if pair:
        properties["scope_id"] = {"type": "null"}
        properties.update({"earlier_scope_id": _text(), "later_scope_id": _text()})
        required.extend(("earlier_scope_id", "later_scope_id"))
    else:
        properties["scope_id"] = _text()
    if delta:
        properties.update({"earlier_value": _nullable(value), "later_value": _nullable(value),
            "earlier_denominator": _nullable(_number(minimum=0)),
            "later_denominator": _nullable(_number(minimum=0)),
            "earlier_coverage": _nullable(_ref("coverage")),
            "later_coverage": _nullable(_ref("coverage")),
            "earlier_reason_codes": _strings(), "later_reason_codes": _strings()})
        required.extend(("earlier_value", "later_value", "earlier_denominator", "later_denominator",
                         "earlier_coverage", "later_coverage", "earlier_reason_codes", "later_reason_codes"))
        properties["denominator"] = {"type": "null"}
        properties["denominator_reason"] = {"const": "not_applicable_to_difference"}
    if representation:
        result["allOf"].append({"if": {"properties": {"status": {"enum": ["available", "partial"]}}},
                                  "then": {"properties": {"basis_id": _text()}}})
    else:
        properties["basis_id"] = {"type": "null"}
    result["required"] = required
    return result


def _longitudinal_contract(resource_usage: dict) -> tuple[dict, dict, dict, dict]:
    """The complete public series inventory, with no identity-bearing object keys."""
    ratio = _number(minimum=0, maximum=1)
    signed = _number()
    signed_integer = {**_integer(), "minimum": -sys.float_info.max}
    source_categories = ("human", "synthetic", "mixed", "sensor", "unknown")
    confidence_categories = ("confirmed", "log_derived", "estimated", "unknown")
    snapshot = _object({
        "snapshot_id": _text(), "dataset_version": _nullable(_text()), "ordinal": _integer(minimum=1),
        "input_role": _enum("records_primary", "records_compare", "declared_empty"),
        "empty_scope": {"type": "boolean"}, "population_scope_id": _text(),
        "representation_scope_id": _nullable(_text()), "basis_id": _nullable(_text()),
        "redaction": _nullable(_ref("redaction")),
    })
    mapping = _object({"direction": _enum("earlier_to_later", "later_to_earlier"),
        "source_basis_id": _text(), "target_basis_id": _text(),
        "entries": _lineage_details(_object({"source_state": _text(empty=True), "target_state": _text(empty=True)}))})
    pair = _object({
        "comparison_id": _text(), "earlier_snapshot_id": _text(), "later_snapshot_id": _text(),
        "kinds": _array(_enum("adjacent", "baseline"), minimum=1, unique=True),
        "compatibility_status": _enum("available", "unavailable"), "reason_codes": _strings(),
        "earlier_basis_id": _nullable(_text()), "later_basis_id": _nullable(_text()),
        "harmonized_basis_id": _nullable(_text()), "mapping": _nullable(mapping),
        "mapping_collisions": _nullable(_lineage_details(_object({
            "target_state": _text(empty=True), "source_states": _lineage_details(_text(empty=True))}))),
    })
    inputs = _object({
        "requested": {"type": "boolean"}, "baseline": _enum("none", "first"),
        "primary_snapshot_id": _nullable(_text()), "selected_version_count": _integer(),
        "comparison_count": _integer(), "order_source": _nullable(_text()),
        "snapshots": _array(snapshot), "comparisons": _array(pair),
        "representations": _array(_object({"basis_id": _text(), "representation": _ref("representation"),
            "state_semantics": _nullable(_text()), "redaction": _nullable(_ref("redaction"))})),
        "scopes": _array(_object({"scope_id": _text(), "snapshot_id": _text(),
            "record_count": _integer(), "excluded_record_count": _integer(), "denominator_basis": _text()})),
        "context_versions": _lineage_details(_text()), "context_version_count": _integer(),
        "max_versions": _integer(minimum=1), "detail_limit": {"const": 100},
        "redaction": _nullable(_ref("redaction")),
    })
    observed_fields = {}
    observed_specs = (
        ("record_count", "PR-002", "records", "PR-002.record_count", _integer()),
        ("representation_eligible_record_count", "PR-011", "records", "PR-011.representation_eligible_record_count", _integer()),
        ("representation_excluded_record_count", "PR-011", "records", "PR-011.representation_excluded_record_count", _integer()),
        ("provenance_row_coverage", "PR-004", "ratio", "F-008", ratio),
        ("provenance_required_field_coverage", "PR-004", "ratio", "PR-004.provenance_required_field_coverage", ratio),
        ("grounding_field_coverage", "PR-004", "ratio", "PR-004.grounding_field_coverage", ratio),
        ("source_type_counts", "PR-005", "records", "PR-005.source_type_counts", _object({k: _integer() for k in source_categories})),
        ("missing_provenance_count", "PR-004", "records", "PR-004.missing_provenance_count", _integer()),
        ("provenance_confidence_counts", "PR-004", "records", "PR-004.provenance_confidence_counts", _object({k: _integer() for k in confidence_categories})),
        *((name, "PR-008", "reference_entries", "PR-008." + name, _integer()) for name in (
            "declared_parent_reference_count", "resolved_parent_reference_count", "unresolved_parent_reference_count")),
    )
    for name, owner, unit, method, value in observed_specs:
        observed_fields[name] = _series_field("observed_facts.longitudinal.snapshots." + name,
                                               value, owner, unit, method, observed=True)
    snapshot_fields = {}
    metric_specs = (
        ("support_size", "T1", "states", "F-002", _integer()),
        ("gini_simpson_diversity", "T1", "dimensionless", "F-003", ratio),
        ("source_type_shares", "PR-005", "ratio", "F-007", _object({k: ratio for k in source_categories})),
        ("missing_provenance_share", "PR-004", "ratio", "PR-004.one_minus_row_coverage", ratio),
        *(("direct_closure_" + name, "T3", "ratio", method, ratio) for name, method in (
            ("lower_bound", "F-009"), ("upper_bound", "F-010"), ("interval_width", "T3.upper_minus_lower"))),
        *((name, "T4", "records", "T4." + name, _integer()) for name in (
            "grounded_record_count", "closed_record_count", "unresolved_record_count", "records_with_resolved_external_ancestry")),
        ("distinct_external_root_count", "T4", "roots", "T4.root_set_union", _integer()),
        ("ancestry_concentration_hhi", "T4", "ratio", "F-012", ratio),
        ("effective_external_root_count", "T4", "roots", "F-013", _number(minimum=0)),
        ("resolved_parent_edge_coverage", "PR-008", "ratio", "PR-008.resolved_edges_over_declared", ratio),
        ("resolved_lineage_coverage", "T4", "ratio", "T4.resolved_records_over_scope", ratio),
        ("external_ancestry_coverage", "T4", "ratio", "T4.external_roots_over_scope", ratio),
        *(("lineage_closure_" + name, "T3", "ratio", "T3.lineage_closure", ratio)
          for name in ("lower_bound", "upper_bound", "interval_width")),
    )
    for name, owner, unit, method, value in metric_specs:
        snapshot_fields[name] = _series_field("derived_metrics.longitudinal.snapshots." + name,
            value, owner, unit, method, representation=name in ("support_size", "gini_simpson_diversity"))
    reference_coverage = snapshot_fields["resolved_parent_edge_coverage"]
    reference_coverage["properties"]["no_declared_parents"] = _nullable({"type": "boolean"})
    reference_coverage["required"].append("no_declared_parents")
    comparisons = {}
    delta_specs = (
        ("record_count_delta", "T1", "records", "F-018", signed_integer),
        ("support_delta", "T1", "states", "F-005", signed_integer),
        ("gini_simpson_diversity_delta", "T1", "dimensionless", "F-018", signed),
        *((name + "_delta", "PR-004", "ratio", "F-018", signed) for name in (
            "provenance_row_coverage", "provenance_required_field_coverage", "grounding_field_coverage", "missing_provenance_share")),
        ("source_type_share_deltas", "PR-005", "ratio", "F-018", _object({k: signed for k in source_categories})),
        *(("direct_closure_" + name + "_delta", "T3", "ratio", "F-018", signed)
          for name in ("lower_bound", "upper_bound", "interval_width")),
        ("distinct_external_root_count_delta", "T4", "roots", "F-018", signed_integer),
        ("ancestry_concentration_hhi_delta", "T4", "ratio", "F-018", signed),
        ("effective_external_root_count_delta", "T4", "roots", "F-018", signed),
        ("unresolved_parent_reference_count_delta", "PR-008", "reference_entries", "F-018", signed_integer),
        ("resolved_parent_edge_coverage_delta", "PR-008", "ratio", "F-018", signed),
        *((name + "_delta", "T4", "ratio", "F-018", signed) for name in ("resolved_lineage_coverage", "external_ancestry_coverage")),
        *(("lineage_closure_" + name + "_delta", "T3", "ratio", "F-018", signed)
          for name in ("lower_bound", "upper_bound", "interval_width")),
    )
    for name, owner, unit, method, value in delta_specs:
        comparisons[name] = _series_field("derived_metrics.longitudinal.comparisons." + name,
            value, owner, unit, method, pair=True, delta=True,
            representation=name in ("support_delta", "gini_simpson_diversity_delta"))
        if name in ("unresolved_parent_reference_count_delta", "resolved_parent_edge_coverage_delta"):
            for side in ("earlier", "later"):
                flag = side + "_no_declared_parents"
                comparisons[name]["properties"][flag] = _nullable({"type": "boolean"})
                comparisons[name]["required"].append(flag)
    for name, owner, unit, method, value in (
        ("support_loss_count", "T1", "states", "T1.support_set_difference", _integer()),
        ("support_added_count", "T1", "states", "T1.support_set_difference", _integer()),
        ("support_retention_ratio", "T1", "ratio", "F-006", ratio),
        ("extinct_states", "T1", "set_of_states", "T1.earlier_minus_later", _lineage_details(_text(empty=True))),
        ("added_states", "T1", "set_of_states", "T1.later_minus_earlier", _lineage_details(_text(empty=True))),
        ("retained_states", "T1", "set_of_states", "T1.support_intersection", _lineage_details(_text(empty=True))),
        ("tail_extinction_count", "T2", "states", "T2.earlier_tail_intersect_missing", _integer()),
        ("tail_extinct_states", "T2", "set_of_states", "T2.earlier_tail_intersect_missing", _lineage_details(_text(empty=True))),
    ):
        comparisons[name] = _series_field("derived_metrics.longitudinal.comparisons." + name,
            value, owner, unit, method, pair=True, representation=True)
        if owner == "T2":
            comparisons[name]["properties"].update({"tail_selection": _nullable(_ref("tail_selection")),
                                                     "earlier_sample_size": _nullable(_integer())})
            comparisons[name]["required"].extend(("tail_selection", "earlier_sample_size"))
    shared = _object({"execution_status": _enum("completed", "partial", "failed"),
        "reason_codes": _strings(), "loaded_record_count": _nullable(_integer()),
        "unique_edge_count": _nullable(_integer()), "cycle_status": _nullable(_enum("acyclic", "cyclic")),
        "cycle_count": _nullable(_integer()), "resource_usage": _nullable(resource_usage),
        "graph_diagnostics": _lineage_details(_object({"code": _text(),
            "severity": _enum("warning", "error", "fatal"), "message": _text()})),
        "evidence_scope": {"const": "common_supplied_retrospective_graph"}})
    observed = _object({"snapshots": _array(_object({"snapshot_id": _text(), **observed_fields})),
                         "shared_lineage": _nullable(shared)})
    derived = _object({"snapshots": _array(_object({"snapshot_id": _text(), **snapshot_fields})),
        "comparisons": _array(_object({"comparison_id": _text(), **comparisons}))})
    family = _object({"execution_status": _enum("completed", "partial", "failed", "not_requested"),
                      "reason_codes": _strings()})
    execution = _object({"status": _enum("completed", "partial", "failed", "not_requested"),
        "reason_codes": _strings(), "requested_families": _array(_enum(*LONGITUDINAL_FAMILIES), unique=True),
        "snapshot_statuses": _array(_object({"snapshot_id": _text(),
            "families": _object({name: family for name in LONGITUDINAL_FAMILIES})})),
        "comparison_statuses": _array(_object({"comparison_id": _text(),
            "families": _object({name: family for name in LONGITUDINAL_FAMILIES})}))})
    return inputs, observed, derived, execution


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
        "run_id": _text(), "toolkit_version": _text(), "report_schema_version": {"const": "1.3"},
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
        "role": _enum("records_primary", "records_compare", "lineage_context", "provenance_manifest", "schema_mapping", "config",
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
                                                "T6", "status", "T6.graph_cycle_check", 3, "enum")
    graph_scope = _object({
        "target_dataset_version": _nullable(_text()), "target_record_count": _integer(),
        "loaded_record_count": _integer(), "context_record_count": _integer(),
        "loaded_dataset_versions": _strings(),
    })
    witness = _array(_ref("record_key"), minimum=2)
    witness["maxItems"] = 65
    component = _object({
        "component_index": _integer(minimum=1), "member_count": _integer(minimum=1),
        "target_member_count": _integer(), "witness_record_keys": _nullable(witness),
        "witness_edge_count": _nullable({**_integer(minimum=1), "maximum": 64}),
        "witness_reason": _nullable({"const": "diagnostic_limit"}),
    })
    cycle_analysis = _object({
        "detected": {"type": "boolean"}, "cycle_count": _integer(),
        "counting_method": {"const": "cyclic_strongly_connected_components"},
        "cycle_member_count": _integer(), "target_cycle_member_count": _integer(),
        "affected_record_count": _integer(), "target_affected_record_count": _integer(),
        "components": _lineage_details(component),
        "cycle_member_record_keys": _lineage_details(_ref("record_key")),
        "affected_record_keys": _lineage_details(_ref("record_key")),
    })
    depth_summary = _object({"depth_resolved_record_count": _integer(),
        "maximum_resolved_target_depth": _nullable(_integer()), "target_record_count": _integer()})
    resource_usage = _object({
        "admitted_node_count": _integer(), "admitted_edge_count": _integer(),
        "stored_root_membership_count": _integer(), "root_union_visit_count": _integer(),
        "limits": _object({name: _integer(minimum=1) for name in (
            "max_nodes", "max_edges", "max_root_memberships", "max_root_union_visits")}),
        "exhausted_limit": _nullable(_enum("max_nodes", "max_edges", "max_root_memberships", "max_root_union_visits")),
        "attempted_value": _nullable(_integer(minimum=1)),
    })
    for name, value, owner, unit, method, value_type in (
        ("graph_scope", graph_scope, "T4", "scope", "T4.graph_scope", "lineage_scope"),
        ("cycle_analysis", cycle_analysis, "T6", "cycles", "T6.cyclic_strongly_connected_components", "cycle_analysis"),
        ("depth_summary", depth_summary, "PR-009", "edges", "PR-009.resolved_depth_summary", "depth_summary"),
        ("unresolved_record_details", _lineage_details(_object({"record_key": _ref("record_key"),
            "reason_codes": _strings(minimum=1)})), "T4", "records", "T4.unresolved_record_details", "unresolved_record_details"),
        ("resource_usage", resource_usage, "PR-015", "work_units", "PR-015.lineage_resource_usage", "lineage_resource_usage"),
    ):
        observed_lineage[name] = _observed("observed_facts.lineage." + name, value,
                                         owner, unit, method, 3, value_type)
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
    lineage_bounds = {name: _metric("derived_metrics.closure_exposure.lineage." + name, _number(minimum=0, maximum=1), "T3", "ratio", "T3.lineage_closure", 3, "ratio") for name in ("lower_bound", "upper_bound", "interval_width")}
    root_contribution = _object({
        "record_key": _ref("record_key"), "incidence_count": _integer(minimum=1),
        "incidence_share": _number(minimum=0, maximum=1), "incidence_denominator": _integer(minimum=1),
        "fractional_mass": _number(minimum=0), "normalized_weight": _number(minimum=0, maximum=1),
        "weight_denominator": _integer(minimum=1),
    })
    lineage = {}
    for name, owner, unit, method, value, value_type in (
        ("resolved_parent_edge_coverage", "PR-008", "ratio", "PR-008.resolved_edges_over_declared", _number(minimum=0, maximum=1), "ratio"),
        ("resolved_lineage_coverage", "T4", "ratio", "T4.resolved_records_over_scope", _number(minimum=0, maximum=1), "ratio"),
        ("external_ancestry_coverage", "T4", "ratio", "T4.external_roots_over_scope", _number(minimum=0, maximum=1), "ratio"),
        ("distinct_external_root_count", "T4", "roots", "T4.root_set_union", _integer(), "integer"),
        ("top_shared_ancestors", "T4", "records", "T4.incidence_ranking", _lineage_details(root_contribution), "root_contribution_details"),
        ("grounded_record_count", "T4", "records", "T4.grounded_record_count", _integer(), "integer"),
        ("closed_record_count", "T4", "records", "T4.closed_record_count", _integer(), "integer"),
        ("unresolved_record_count", "T4", "records", "T4.unresolved_record_count", _integer(), "integer"),
        ("records_with_resolved_external_ancestry", "T4", "records", "T4.records_with_resolved_external_ancestry", _integer(), "integer"),
        ("ancestry_concentration_hhi", "T4", "ratio", "F-012", _number(minimum=0, maximum=1), "ratio"),
        ("effective_external_root_count", "T4", "roots", "F-013", _number(minimum=0), "number"),
        ("lineage_depth", "PR-009", "edges", "PR-009.maximum_resolved_parent_depth", _integer(), "integer"),
    ):
        lineage[name] = _metric("derived_metrics.lineage." + name, value, owner, unit, method, 3, value_type)
    lineage["resolved_parent_edge_coverage"]["properties"]["no_declared_parents"] = {"type": "boolean"}
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
        proxies[name] = _object(props)
        proxies[name]["allOf"] = [{
            "if": {"properties": {"status": {"const": "unavailable"}}},
            "then": {"properties": {"level": {"const": "indeterminate"},
                                      "reason_codes": {"minItems": 1}, "required_evidence": {"minItems": 1}}},
        }]
        _field_entries.append(FieldDefinition("proxy_signals." + name, owner, "proxy_signal", "signal", owner + "." + name, level, "proxy"))
    simulations = {}
    for name, owner, level in (("closed_resampling", "T1", 5), ("tail_extinction", "T2", 1)):
        props = _base_envelope("simulation", "scenario", owner, owner + "." + name)
        props.update({"status": {"const": "experimental"}, "model": {"const": "closed_resampling"},
                      "model_version": _text(), "method": _enum("analytic_expectation", "analytic_extinction", "sampled_path"),
                      "parameters": {**_ref("simulation_parameters"), "properties": {"reopening_weight": {"type": "null"}, "external_input_distribution": {"maxItems": 0}}}, "initial_distribution": _array(_ref("state_probability")),
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
    closed = simulations["closed_resampling"]["properties"]
    baseline_properties = {key: value for key, value in closed.items() if key not in
        ("sampled_paths", "support_trajectories", "extinction_events")}
    baseline_properties["method"] = {"const": "analytic_expectation"}
    baseline_properties["baseline_basis"] = {"const": "closed_sampled_effective_distribution"}
    baseline = _object(baseline_properties)
    closed.update({"state_semantics": _text(), "analytic_baseline": _ref("closed_analytic_baseline"),
                   "assumption_table": _ref("scenario_assumption_table")})
    reopened = _base_envelope("simulation", "scenario", "T5", "T5.external_reopening")
    reopened.update({
        "status": {"const": "experimental"}, "model": {"const": "reopened_resampling"},
        "model_version": {"const": "reopened_categorical_constant_v1"}, "method": {"const": "sampled_path"},
        "parameters": _ref("simulation_parameters"), "resample_size": _integer(minimum=1),
        "initial_distribution": _array(_ref("state_probability"), minimum=1),
        "input_normalization": _ref("input_normalization"), "state_semantics": _text(),
        "external_input_distribution": _array(_ref("state_probability"), minimum=1),
        "external_input_normalization": _ref("input_normalization"),
        "sampled_paths": _array(_ref("sampled_path"), minimum=1),
        "mixed_sources": _array(_object({"replicate_index": _integer(), "step": _integer(minimum=1),
            "input_normalization": _ref("input_normalization"),
            "input_basis": _enum("effective_internal_distribution", "effective_external_distribution",
                "computed_external_mixture", "sampled_integer_counts_over_resample_size"),
            "possible_reentry_states": _array(_text(empty=True), unique=True)})),
        "state_reentry_events": _array(_ref("state_transition_event")),
        "extinction_events": _array(_ref("state_transition_event")),
        "support_trajectory": _array(_object({"replicate_index": _integer(), "support_sizes": _array(_integer())})),
        "diversity_trajectory": _array(_object({"replicate_index": _integer(),
            "gini_simpson_diversities": _array(_number(minimum=0, maximum=1))})),
        "assumption_table": _ref("scenario_assumption_table"),
    })
    reopened["representation"] = _ref("representation")
    reopened["trace_ids"] = {"const": ["T5"]}
    reopened["theory_map_ids"] = {"const": []}
    reopened["assumptions"] = {"const": [
        "Fixed finite declared state space and constant positive integer resample size.",
        "The internal and external vectors have the same explicitly declared state meaning.",
        "External input distribution r and reopening weight lambda are constant across steps.",
        "s_t=(1-lambda)*p_t+lambda*r; X_t conditional on s_t is Multinomial(n,s_t).",
        "p_(t+1)=X_t/n; no other source of state restoration is modeled.",
    ]}
    reopened["limitations"] = {"const": [
        "Experimental conditional simulation; no empirical intervention effect is established.",
        "Positive mixed probability permits re-entry without guaranteeing a positive sample count.",
        "External independence, reliability and relevance are supplied assumptions, not verified facts.",
        "Reopening weight is not an integrity or Presence score; greater weight need not improve fidelity.",
        "Closed multi-step expected contraction is not an expectation for a reopened trajectory.",
        "Simulated steps are not record generations, training epochs or dataset releases.",
        "The reopened kernel alone performs no comparison, external-reference loss, report or audit dispatch.",
        "Floating-point and pseudorandom sampling are numerical realizations of the declared model.",
        "Replay requires the same method, NumPy build/environment, seed and parameters.",
        "Bit-identical paths across dependency versions or platforms are not promised.",
        "Accepted input round-off is corrected only by division by its validated total.",
        "Lambda endpoints reuse the already effective source; lambda zero retains integer count sampling.",
    ]}
    reopened_required = tuple(reopened)
    reopened["scenario_comparison"] = _object({
        "difference_direction": {"const": "reopened_minus_closed"},
        "initial_reachability": _array(_object({
            "model_name": _enum("closed_resampling", "reopened_resampling"),
            "reachable_states": _array(_text(empty=True), unique=True),
            "possible_reentry_states": _array(_text(empty=True), unique=True),
            "timing": {"const": "before_first_draw"}}), minimum=2),
        "rows": _array(_object({"replicate_index": _integer(), "step": _integer(),
            "closed_support_size": _integer(), "reopened_support_size": _integer(),
            "support_size_difference": _integer(minimum=-4096),
            "closed_gini_simpson_diversity": _number(minimum=0, maximum=1),
            "reopened_gini_simpson_diversity": _number(minimum=0, maximum=1),
            "diversity_difference": _number(minimum=-1, maximum=1)})),
        "limitations": _strings(minimum=1),
    })
    simulations["external_reopening"] = _object(reopened, reopened_required)
    _field_entries.append(FieldDefinition("simulations.external_reopening", "T5", "simulation", "scenario", "T5.external_reopening", 5, "scenario", True))
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
            "comparison_requested": {"type": "boolean"}, "scenario_requested": {"type": "boolean"},
            "lineage_requested": {"type": "boolean"}}, ()),
        "state_probability": _object({"state_id": _text(empty=True), "probability": _number(minimum=0, maximum=1)}),
        "closed_analytic_baseline": baseline,
        "state_transition_event": _object({"replicate_index": _integer(), "step": _integer(minimum=1), "state_id": _text(empty=True)}),
        "scenario_assumption_table": {"oneOf": [{"const": _scenario_assumption_table(False)}, {"const": _scenario_assumption_table(True)}]},
        "simulation_parameters": _object({
            "resample_size": _integer(minimum=1), "simulation_horizon": _integer(),
            "random_seed": _nullable(_integer()), "simulation_replicates": _nullable(_integer(minimum=1)),
            "rng_name": _nullable({"const": "numpy.random.Generator(PCG64)"}), "numpy_version": _nullable(_text()),
            "replicate_schedule": _nullable({"const": "replicate_major_step_major"}),
            "state_order": _array(_text(empty=True), unique=True), "input_basis": _text(),
            "reopening_weight": _nullable(_number(minimum=0, maximum=1)),
            "external_input_distribution": _array(_ref("state_probability")),
            "numerical_policy": _ref("numerical_policy"),
            "sampler_algorithm": {"const": "sequential_binomial_complement_v1"},
            "state_schedule": {"const": "ascending_unicode_state_id_skip_zero"},
            "scenario_schedule": {"const": "reset_same_seed_per_model"},
        }, ("resample_size", "simulation_horizon", "random_seed", "simulation_replicates", "rng_name", "numpy_version",
            "replicate_schedule", "state_order", "input_basis", "reopening_weight", "external_input_distribution", "numerical_policy")),
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
    series_inputs, series_observed, series_derived, series_execution = _longitudinal_contract(resource_usage)
    inputs["properties"]["longitudinal"] = series_inputs
    observed["properties"]["longitudinal"] = series_observed
    derived["properties"]["longitudinal"] = series_derived
    capability["properties"]["longitudinal_execution"] = series_execution
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
            "title": "Recursive Integrity Toolkit canonical report 1.3",
            "description": "Phase 6B public contract with explicit experimental scenarios, referenced longitudinal and bounded lineage evidence. Product metadata and five analytical evidence classes remain separate.",
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
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            _fail(path, "too many array items")
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


def _lineage_detail_checks(detail: dict, *, unique: bool = True) -> None:
    path = "$.lineage.details"
    for name in ("total_count", "returned_count", "omitted_count", "limit"):
        if type(detail[name]) is not int:
            _fail(path, "detail counts require exact integers")
    total, returned, omitted = (detail[name] for name in ("total_count", "returned_count", "omitted_count"))
    if total != returned + omitted:
        _fail(path, "detail counts do not partition the total")
    status, items, reasons = detail["detail_status"], detail["items"], detail["omission_reasons"]
    if status == "omitted":
        expected = {"redacted_identity_details"}
        if total > 100:
            expected.add("diagnostic_limit")
        if items is not None or returned or omitted != total or set(reasons) != expected:
            _fail(path, "privacy omission must retain the complete aggregate and applicable cap reason")
    elif items is None or returned != len(items) or returned != min(total, 100):
        _fail(path, "visible detail must contain the bounded prefix of the supplied total")
    elif (status == "complete") != (omitted == 0):
        _fail(path, "detail status disagrees with omitted count")
    if items and unique:
        identities = [row.get("record_key", row) if type(row) is dict else row for row in items]
        if len({_equality_key(key) for key in identities}) != len(identities):
            _fail(path, "detail identities must be unique")


def _lineage_usage_checks(usage: dict, execution: str) -> None:
    """Validate exact supplied work accounting for admitted and aborted graphs."""
    counter_names = {
        "max_nodes": "admitted_node_count", "max_edges": "admitted_edge_count",
        "max_root_memberships": "stored_root_membership_count", "max_root_union_visits": "root_union_visit_count",
    }
    for limit, counter in counter_names.items():
        if (type(usage[counter]) is not int or type(usage["limits"][limit]) is not int
                or not 0 <= usage[counter] <= usage["limits"][limit] or usage["limits"][limit] <= 0):
            _fail("$.lineage.resource_usage", "consumed work must remain within its positive integer limit")
    exhausted = usage["exhausted_limit"]
    if exhausted is None:
        if usage["attempted_value"] is not None:
            _fail("$.lineage.resource_usage", "unexhausted work cannot contain a rejected attempt")
    elif (execution != "failed" or type(usage["attempted_value"]) is not int
          or usage["attempted_value"] != usage["limits"][exhausted] + 1
          or usage[counter_names[exhausted]] != usage["limits"][exhausted]):
        _fail("$.lineage.resource_usage", "resource exhaustion requires failed execution and its next rejected unit")


def _lineage_semantic_checks(payload: dict) -> None:
    """Check supplied lineage evidence consistency without traversing a graph."""
    observed = payload["observed_facts"].get("lineage", {})
    metrics = payload["derived_metrics"].get("lineage", {})
    bounds = payload["derived_metrics"].get("closure_exposure", {}).get("lineage", {})
    proxy = payload["proxy_signals"].get("shared_ancestry_dependence")
    capability = payload["capabilities"].get("lineage", {})
    execution = capability.get("execution_status", "not_requested")
    new_observed = ("graph_scope", "cycle_analysis", "depth_summary", "unresolved_record_details", "resource_usage", "cycle_status")
    new_metrics = tuple(name for name in metrics if name != "resolved_parent_edge_coverage")

    def value(group, name):
        return group.get(name, {}).get("value")

    active = (any(value(observed, name) is not None for name in new_observed)
              or any(value(metrics, name) is not None for name in new_metrics)
              or any(entry["value"] is not None for entry in bounds.values())
              or (proxy is not None and proxy["status"] != "unavailable"))
    if execution in ("not_requested", "deferred"):
        if active or "no_declared_parents" in metrics.get("resolved_parent_edge_coverage", {}):
            _fail("$.capabilities.lineage", "unexecuted lineage cannot contain analytical results")
        return
    scope = value(observed, "graph_scope")
    if scope is None:
        if execution == "failed" and not active:
            return
        usage = value(observed, "resource_usage")
        if execution == "failed" and usage is not None:
            _lineage_usage_checks(usage, execution)
            if (any(value(observed, name) is not None for name in new_observed if name != "resource_usage")
                    or any(value(metrics, name) is not None for name in new_metrics)
                    or any(entry["value"] is not None for entry in bounds.values())
                    or (proxy is not None and proxy["status"] != "unavailable")):
                _fail("$.lineage", "failed graph admission cannot contain subsequent analytical results")
            loaded_scope = payload["inputs"].get("scope")
            if loaded_scope is None or observed["resource_usage"]["scope"] != loaded_scope:
                _fail("$.lineage.resource_usage", "admission accounting must retain the complete loaded input scope")
            loaded = loaded_scope["record_count"]
            exhausted = usage["exhausted_limit"]
            if (exhausted not in ("max_nodes", "max_edges")
                    or usage["stored_root_membership_count"] or usage["root_union_visit_count"]
                    or type(loaded) is not int
                    or exhausted == "max_nodes" and (usage["admitted_node_count"] >= loaded or usage["admitted_edge_count"])
                    or exhausted == "max_edges" and usage["admitted_node_count"] != loaded):
                _fail("$.lineage.resource_usage", "admission exhaustion is inconsistent with the loaded records or later-stage work")
            if not any(error["code"] == "E_LINEAGE_RESOURCE_LIMIT_EXCEEDED"
                       and "lineage" in error["effect_on_capabilities"] for error in payload["errors"]):
                _fail("$.lineage.resource_usage", "admission exhaustion requires its matching lineage error")
            return
        _fail("$.observed_facts.lineage.graph_scope", "executed lineage requires its explicit target and loaded scope")
    target, loaded, context = (scope[name] for name in ("target_record_count", "loaded_record_count", "context_record_count"))
    if any(type(number) is not int for number in (target, loaded, context)) or loaded != target + context:
        _fail("$.observed_facts.lineage.graph_scope", "loaded scope must partition into target and context")
    version = scope["target_dataset_version"]
    versions = scope["loaded_dataset_versions"]
    if (target and (version is None or version not in versions)) or (loaded and not versions):
        _fail("$.observed_facts.lineage.graph_scope", "scope counts require their declared versions")
    target_versions = [] if version is None else [version]
    graph_fields = {"graph_scope", "cycle_analysis", "cycle_status", "resource_usage"}
    for name in graph_fields & observed.keys():
        entry_scope = observed[name]["scope"]
        if entry_scope["record_count"] != loaded or set(entry_scope["dataset_versions"]) != set(versions):
            _fail("$.lineage.scope", "graph diagnostics must retain the complete loaded population")
    entries = [entry for name, entry in observed.items() if name not in graph_fields] + list(metrics.values()) + list(bounds.values())
    if proxy is not None:
        entries.append(proxy)
    for entry in entries:
        if entry["scope"]["record_count"] != target or entry["scope"]["dataset_versions"] != target_versions:
            _fail("$.lineage.scope", "lineage evidence must retain the selected target population")
    usage = value(observed, "resource_usage")
    if usage is None:
        _fail("$.observed_facts.lineage.resource_usage", "executed lineage requires work accounting")
    _lineage_usage_checks(usage, execution)
    exhausted = usage["exhausted_limit"]
    cycles, depth = value(observed, "cycle_analysis"), value(observed, "depth_summary")
    if execution in ("completed", "partial") and (cycles is None or depth is None):
        _fail("$.capabilities.lineage", "completed traversal requires cycle and depth observations")
    if cycles is None:
        if value(observed, "cycle_status") is not None:
            _fail("$.lineage.cycle_status", "cycle status requires a completed cycle analysis")
    else:
        if usage["admitted_node_count"] != loaded:
            _fail("$.lineage.resource_usage", "completed graph evidence requires every loaded node")
        if any(type(cycles[name]) is not int for name in (
                "cycle_count", "cycle_member_count", "target_cycle_member_count",
                "affected_record_count", "target_affected_record_count")):
            _fail("$.lineage.cycle_analysis", "cycle counts require exact integers")
        total_members, target_members = cycles["cycle_member_count"], cycles["target_cycle_member_count"]
        affected, target_affected = cycles["affected_record_count"], cycles["target_affected_record_count"]
        if (cycles["detected"] != (cycles["cycle_count"] > 0)
                or not cycles["cycle_count"] <= total_members <= affected <= loaded
                or not target_members <= total_members or not target_members <= target_affected <= target
                or target_affected > affected or (not cycles["detected"] and affected)):
            _fail("$.lineage.cycle_analysis", "cycle counts disagree with their loaded and target scopes")
        if execution == "completed" and cycles["detected"]:
            _fail("$.capabilities.lineage", "cyclic input cannot claim completed valid lineage")
        if value(observed, "cycle_status") != ("cyclic" if cycles["detected"] else "acyclic"):
            _fail("$.lineage.cycle_status", "cycle status disagrees with cycle diagnostics")
        for name, expected in (("components", cycles["cycle_count"]), ("cycle_member_record_keys", total_members), ("affected_record_keys", affected)):
            if cycles[name]["total_count"] != expected:
                _fail("$.lineage.cycle_analysis", "detail total disagrees with its aggregate")
        rows = cycles["components"]["items"]
        if rows is not None:
            for index, row in enumerate(rows, 1):
                if (any(type(row[name]) is not int for name in ("component_index", "member_count", "target_member_count"))
                        or row["component_index"] != index or row["target_member_count"] > row["member_count"]):
                    _fail("$.lineage.cycle_analysis", "component order or member counts are inconsistent")
                witness = row["witness_record_keys"]
                if witness is None:
                    if row["witness_edge_count"] is not None or row["witness_reason"] != "diagnostic_limit":
                        _fail("$.lineage.cycle_analysis", "omitted witness requires a diagnostic-limit reason")
                elif (type(row["witness_edge_count"]) is not int or witness[0] != witness[-1]
                      or row["witness_edge_count"] != len(witness) - 1
                      or row["witness_reason"] is not None or len(witness) - 1 > row["member_count"]):
                    _fail("$.lineage.cycle_analysis", "witness must be closed with a consistent bounded edge count")
            if cycles["components"]["detail_status"] == "complete" and (
                    sum(row["member_count"] for row in rows) != total_members
                    or sum(row["target_member_count"] for row in rows) != target_members):
                _fail("$.lineage.cycle_analysis", "component rows disagree with aggregate membership")
    if depth is not None:
        resolved_depth = depth["depth_resolved_record_count"]
        maximum = depth["maximum_resolved_target_depth"]
        if (type(resolved_depth) is not int or type(depth["target_record_count"]) is not int
                or (maximum is not None and type(maximum) is not int)
                or depth["target_record_count"] != target or resolved_depth > target
                or (maximum is None) != (resolved_depth == 0)):
            _fail("$.lineage.depth_summary", "depth subset must retain its actual target coverage")
        expected_depth = maximum if target and resolved_depth == target else None
        if value(metrics, "lineage_depth") != expected_depth:
            _fail("$.derived_metrics.lineage.lineage_depth", "whole-target depth cannot claim a subset maximum")
    count_names = ("grounded_record_count", "closed_record_count", "unresolved_record_count", "records_with_resolved_external_ancestry")
    counts = [value(metrics, name) for name in count_names]
    if any(count is None for count in counts):
        if any(count is not None for count in counts) or execution in ("completed", "partial"):
            _fail("$.derived_metrics.lineage", "an exact target partition requires all G/C/U counts")
        if any(value(metrics, name) is not None for name in new_metrics if name != "lineage_depth") or any(entry["value"] is not None for entry in bounds.values()):
            _fail("$.derived_metrics.lineage", "incomplete root traversal cannot supply dependent values")
    else:
        grounded, closed, unresolved, resolved = counts
        if any(type(count) is not int for count in counts) or grounded + closed + unresolved != target or resolved != grounded + closed:
            _fail("$.derived_metrics.lineage", "G/C/U counts must exactly partition the target")
        if any(metrics[name]["denominator"] != target for name in count_names):
            _fail("$.derived_metrics.lineage", "partition counts must disclose the complete target denominator")
        if exhausted is not None or (execution == "completed" and unresolved):
            _fail("$.capabilities.lineage", "execution status disagrees with root completeness")
        for name, numerator in (("resolved_lineage_coverage", resolved), ("external_ancestry_coverage", grounded)):
            entry = metrics.get(name)
            if entry is None or entry["denominator"] != target:
                _fail("$.derived_metrics.lineage", "ancestry coverage must disclose the whole target denominator")
            ratio = entry["value"]
            if (target == 0 and ratio is not None) or (target and (ratio is None or not math.isclose(ratio * target, numerator, rel_tol=1e-12, abs_tol=1e-12))):
                _fail("$.derived_metrics.lineage", "ancestry coverage disagrees with the supplied partition")
        details = value(observed, "unresolved_record_details")
        if details is None or details["total_count"] != unresolved:
            _fail("$.lineage.unresolved_record_details", "unresolved detail total disagrees with the target partition")
        root_details = value(metrics, "top_shared_ancestors")
        distinct = value(metrics, "distinct_external_root_count")
        if type(distinct) is not int or root_details is None or root_details["total_count"] != distinct:
            _fail("$.lineage.top_shared_ancestors", "root detail total disagrees with distinct roots")
        if grounded == 0 and (distinct != 0 or any(value(metrics, name) is not None for name in ("ancestry_concentration_hhi", "effective_external_root_count"))):
            _fail("$.derived_metrics.lineage", "empty grounded population has no concentration value")
        if grounded and (not distinct or any(value(metrics, name) is None for name in ("ancestry_concentration_hhi", "effective_external_root_count"))):
            _fail("$.derived_metrics.lineage", "grounded population requires its root distribution and concentration")
        if grounded and (value(metrics, "ancestry_concentration_hhi") <= 0
                or value(metrics, "effective_external_root_count") <= 0
                or not math.isclose(value(metrics, "ancestry_concentration_hhi")
                                    * value(metrics, "effective_external_root_count"),
                                    1.0, rel_tol=1e-12, abs_tol=1e-12)):
            _fail("$.derived_metrics.lineage", "effective roots and positive concentration must be reciprocal")
        for name in ("distinct_external_root_count", "top_shared_ancestors", "ancestry_concentration_hhi", "effective_external_root_count"):
            entry = metrics[name]
            concentration = name in ("ancestry_concentration_hhi", "effective_external_root_count")
            expected_status = "unavailable" if concentration and not grounded else "partial" if unresolved else "available"
            if (entry["status"] != expected_status or entry["denominator"] != (grounded if concentration else target)
                    or entry["coverage"] != value(metrics, "external_ancestry_coverage")):
                _fail("$.derived_metrics.lineage", "root metrics must disclose their grounded subset and unresolved coverage")
        rows = root_details["items"]
        if rows is not None:
            for row in rows:
                if (any(type(row[name]) is not int for name in ("incidence_count", "incidence_denominator", "weight_denominator"))
                        or row["incidence_denominator"] != target or row["weight_denominator"] != grounded
                        or row["incidence_count"] > grounded or row["fractional_mass"] <= 0
                        or row["fractional_mass"] > row["incidence_count"]
                        or row["incidence_share"] <= 0 or row["normalized_weight"] <= 0
                        or not math.isclose(row["incidence_share"] * target, row["incidence_count"], rel_tol=1e-12, abs_tol=1e-12)
                        or not math.isclose(row["normalized_weight"] * grounded, row["fractional_mass"], rel_tol=1e-12, abs_tol=1e-12)):
                    _fail("$.lineage.top_shared_ancestors", "root contribution contradicts its explicit count basis")
            if any(left["incidence_count"] < right["incidence_count"] for left, right in zip(rows, rows[1:])):
                _fail("$.lineage.top_shared_ancestors", "root contributions must retain decreasing incidence rank")
        for name, numerator in (("lower_bound", closed), ("upper_bound", closed + unresolved), ("interval_width", unresolved)):
            if name not in bounds:
                continue
            entry = bounds[name]
            invalid_ratio = (entry["value"] is not None) if target == 0 else (
                entry["value"] is None or not math.isclose(
                    entry["value"] * target, numerator, rel_tol=1e-12, abs_tol=1e-12))
            if entry["denominator"] != target or invalid_ratio:
                _fail("$.derived_metrics.closure_exposure.lineage", "lineage interval contradicts its target partition")
        if proxy is not None:
            required_basis = {"derived_metrics.lineage.top_shared_ancestors", "derived_metrics.lineage.resolved_lineage_coverage", "derived_metrics.lineage.external_ancestry_coverage"}
            if not required_basis.issubset(proxy["basis_fields"]):
                _fail("$.proxy_signals.shared_ancestry_dependence", "shared-root signal must cite incidence and coverage evidence")
            if proxy["denominator"] != target or proxy["coverage"] != value(metrics, "resolved_lineage_coverage"):
                _fail("$.proxy_signals.shared_ancestry_dependence", "shared-root signal must disclose its target coverage")
            if proxy["level"] == "not_present" and (not target or unresolved or proxy["status"] != "available"):
                _fail("$.proxy_signals.shared_ancestry_dependence", "absence requires complete nonempty target evidence")
            if proxy["level"] == "not_present" and rows and rows[0]["incidence_count"] >= 2:
                _fail("$.proxy_signals.shared_ancestry_dependence", "absence contradicts a supplied shared-root witness")
            if proxy["level"] == "present" and (grounded < 2 or proxy["status"] != ("partial" if unresolved else "available") or (rows is not None and (not rows or rows[0]["incidence_count"] < 2))):
                _fail("$.proxy_signals.shared_ancestry_dependence", "presence requires a shared-root witness with honest coverage")
    reference_counts = [value(observed, name) for name in ("declared_parent_edge_count", "resolved_parent_edge_count", "unresolved_parent_edge_count")]
    reference = metrics.get("resolved_parent_edge_coverage")
    if reference is None or "no_declared_parents" not in reference:
        _fail("$.derived_metrics.lineage.resolved_parent_edge_coverage", "executed reference coverage requires its explicit zero-reference state")
    if any(count is None for count in reference_counts):
        if any(count is not None for count in reference_counts) or reference["value"] is not None or reference["no_declared_parents"]:
            _fail("$.lineage.reference_coverage", "unknown reference cardinality cannot become a zero declaration")
    else:
        declared, resolved, unresolved = reference_counts
        ratio = reference["value"]
        if any(type(count) is not int for count in reference_counts) or declared != resolved + unresolved or reference["no_declared_parents"] != (declared == 0) or reference["denominator"] != declared or ratio is None or (declared == 0 and ratio != 1) or (declared and not math.isclose(ratio * declared, resolved, rel_tol=1e-12, abs_tol=1e-12)):
            _fail("$.lineage.reference_coverage", "reference coverage contradicts its declared count basis")


def _series_equal(actual, expected) -> bool:
    if type(actual) is dict and type(expected) is dict:
        return set(actual) == set(expected) and all(_series_equal(actual[k], expected[k]) for k in actual)
    if type(actual) in (int, float) and type(expected) in (int, float):
        return math.isclose(actual, expected, rel_tol=1e-12, abs_tol=1e-12)
    return _same(actual, expected)


def _series_snapshot_checks(observed: dict, metrics: dict, population: dict) -> None:
    """Check supplied count partitions and ratios without reconstructing inputs."""
    path = "$.longitudinal.snapshots"
    n = population["record_count"]
    value = lambda name: (observed if name in observed else metrics)[name]["value"]
    if value("record_count") != n:
        _fail(path, "record count disagrees with its complete population")
    eligible, excluded = value("representation_eligible_record_count"), value("representation_excluded_record_count")
    if eligible is not None and excluded is not None and eligible + excluded != n:
        _fail(path, "representation counts must partition the population")
    for row in (observed, metrics):
        for name, envelope in row.items():
            if name == "snapshot_id":
                continue
            denominator = n
            if name in ("support_size", "gini_simpson_diversity"):
                denominator = eligible or None
            elif name in ("ancestry_concentration_hhi", "effective_external_root_count"):
                denominator = value("grounded_record_count")
            elif name in ("declared_parent_reference_count", "resolved_parent_reference_count",
                          "unresolved_parent_reference_count", "resolved_parent_edge_coverage"):
                denominator = value("declared_parent_reference_count")
            if envelope["denominator"] != denominator:
                _fail(path, "snapshot metric must retain its declared population or allocation denominator")
    missing = value("missing_provenance_count")
    if missing is not None and missing > n:
        _fail(path, "missing provenance exceeds the population")
    for name in ("source_type_counts", "provenance_confidence_counts"):
        counts = value(name)
        if counts is not None and sum(counts.values()) > n:
            _fail(path, "category counts exceed the population")
    if n and missing is not None:
        for name, expected in (("missing_provenance_share", missing / n),
                               ("provenance_row_coverage", (n - missing) / n)):
            if value(name) is not None and not _series_equal(value(name), expected):
                _fail(path, "provenance coverage disagrees with its complete population")
        counts, shares = value("source_type_counts"), value("source_type_shares")
        if counts is not None and shares is not None:
            if sum(counts.values()) + missing != n:
                _fail(path, "source counts and missing rows must partition the population")
            if any(not _series_equal(shares[key], count / n) for key, count in counts.items()):
                _fail(path, "source shares disagree with the complete population")
    for family in ("direct", "lineage"):
        entries = [metrics[f"{family}_closure_{name}"] for name in ("lower_bound", "upper_bound", "interval_width")]
        values = [entry["value"] for entry in entries]
        if any(x is not None for x in values):
            if any(x is None for x in values) or values[0] > values[1] or not _series_equal(values[2], values[1] - values[0]):
                _fail(path, "closure interval must retain consistent endpoints and width")
            if any(entry["denominator"] != n for entry in entries):
                _fail(path, "closure interval must disclose its complete population denominator")
    grounded, closed, unresolved = (value(name) for name in (
        "grounded_record_count", "closed_record_count", "unresolved_record_count"))
    if any(x is not None for x in (grounded, closed, unresolved)):
        if any(x is None for x in (grounded, closed, unresolved)) or grounded + closed + unresolved != n:
            _fail(path, "lineage classifications must partition the complete population")
        if value("records_with_resolved_external_ancestry") != grounded + closed:
            _fail(path, "resolved ancestry count disagrees with classifications")
        for name, numerator in (("resolved_lineage_coverage", grounded + closed),
                                ("external_ancestry_coverage", grounded)):
            expected = numerator / n if n else None
            if not _series_equal(value(name), expected):
                _fail(path, "lineage coverage disagrees with its complete population")
        hhi, effective, roots = (value(name) for name in (
            "ancestry_concentration_hhi", "effective_external_root_count", "distinct_external_root_count"))
        if grounded == 0:
            if hhi is not None or effective is not None or roots != 0:
                _fail(path, "empty grounded population has no concentration or supporting roots")
        elif (hhi is None or hhi <= 0 or effective is None or roots is None or roots < 1
              or not _series_equal(hhi * effective, 1)):
            _fail(path, "positive grounded population requires reciprocal concentration values")
        for name in ("ancestry_concentration_hhi", "effective_external_root_count"):
            if metrics[name]["denominator"] != grounded:
                _fail(path, "concentration must retain its grounded allocation denominator")
            if grounded and unresolved and metrics[name]["status"] != "partial":
                _fail(path, "incomplete ancestry cannot claim complete concentration")
        if n:
            for name, numerator in (("lower_bound", closed), ("upper_bound", closed + unresolved), ("interval_width", unresolved)):
                if not _series_equal(value("lineage_closure_" + name), numerator / n):
                    _fail(path, "lineage interval disagrees with classifications")
    elif any(value(name) is not None for name in ("distinct_external_root_count", "ancestry_concentration_hhi",
            "effective_external_root_count", "resolved_lineage_coverage", "external_ancestry_coverage")):
        _fail(path, "uncomputed ancestry cannot supply dependent metrics")
    declared, resolved, unresolved_refs = (value(name) for name in (
        "declared_parent_reference_count", "resolved_parent_reference_count", "unresolved_parent_reference_count"))
    reference_coverage = metrics["resolved_parent_edge_coverage"]
    if any(x is not None for x in (declared, resolved, unresolved_refs)):
        if any(x is None for x in (declared, resolved, unresolved_refs)) or resolved + unresolved_refs != declared:
            _fail(path, "resolved and unresolved declarations must partition reference entries")
        if (reference_coverage["no_declared_parents"] != (declared == 0)
                or reference_coverage["denominator"] != declared
                or not _series_equal(reference_coverage["value"], resolved / declared if declared else 1)):
            _fail(path, "reference coverage must retain the inherited zero-declaration convention")
    elif reference_coverage["value"] is not None or reference_coverage["no_declared_parents"] is not None:
        _fail(path, "uncomputed references cannot supply coverage or zero-reference assertions")


def _longitudinal_semantic_checks(payload: dict) -> None:
    path = "$.longitudinal"
    inputs = payload["inputs"].get("longitudinal")
    observed = payload["observed_facts"].get("longitudinal")
    derived = payload["derived_metrics"].get("longitudinal")
    execution = payload["capabilities"].get("dataset_longitudinal", {}).get("longitudinal_execution")
    if inputs is None and observed is None and derived is None and execution is None:
        return
    if any(value is None for value in (inputs, observed, derived, execution)):
        _fail(path, "longitudinal inputs, evidence and execution must appear together")
    if any("longitudinal_execution" in value for key, value in payload["capabilities"].items() if key != "dataset_longitudinal"):
        _fail(path, "series execution belongs to the dataset-longitudinal capability")
    snapshots, pairs, scopes, bases = (inputs[name] for name in ("snapshots", "comparisons", "scopes", "representations"))
    snapshot_ids = [row["snapshot_id"] for row in snapshots]
    pair_ids = [row["comparison_id"] for row in pairs]
    if snapshot_ids != [f"s{index:04d}" for index in range(1, len(snapshots) + 1)]:
        _fail(path, "snapshot structural IDs must follow their declared sequence")
    if pair_ids != [f"p{index:04d}" for index in range(1, len(pairs) + 1)]:
        _fail(path, "comparison structural IDs must follow the exact schedule")
    basis_ids = [row["basis_id"] for row in bases]
    if basis_ids != [f"b{index:04d}" for index in range(1, len(bases) + 1)]:
        _fail(path, "basis declarations require distinct structural IDs in encounter order")
    scope_ids = [row["scope_id"] for row in scopes]
    if len(scope_ids) != len(set(scope_ids)):
        _fail(path, "scope IDs must be unique")
    scope_map = {row["scope_id"]: row for row in scopes}
    snapshot_map = {row["snapshot_id"]: row for row in snapshots}
    observed_map = {row["snapshot_id"]: row for row in observed["snapshots"]}
    metric_map = {row["snapshot_id"]: row for row in derived["snapshots"]}
    for rows in (observed["snapshots"], derived["snapshots"], execution["snapshot_statuses"]):
        if [row["snapshot_id"] for row in rows] != snapshot_ids:
            _fail(path, "snapshot evidence and status rows must match the complete declared sequence")
    for rows in (derived["comparisons"], execution["comparison_statuses"]):
        if [row["comparison_id"] for row in rows] != pair_ids:
            _fail(path, "comparison evidence and status rows must match the intended schedule")
    if inputs["comparison_count"] != len(pairs) or inputs["context_version_count"] != inputs["context_versions"]["total_count"]:
        _fail(path, "exact public counts disagree with their declared inventories")
    reasons = execution["reason_codes"]
    if (execution["status"] == "completed") != (not reasons):
        _fail(path, "execution status must retain explicit noncompleted reasons")
    if not inputs["requested"]:
        if (execution["status"] != "not_requested" or execution["requested_families"] or snapshots or pairs or scopes or bases
                or inputs["selected_version_count"] or inputs["primary_snapshot_id"] is not None
                or inputs["order_source"] is not None or observed["shared_lineage"] is not None):
            _fail(path, "unrequested series cannot contain calculated work")
        return
    requested = execution["requested_families"]
    if requested[:3] != list(LONGITUDINAL_FAMILIES[:3]) or requested != [name for name in LONGITUDINAL_FAMILIES if name in requested]:
        _fail(path, "requested series must declare its required families in canonical order")
    if execution["status"] == "not_requested":
        _fail(path, "requested series requires an execution outcome")
    outer = payload["capabilities"]["dataset_longitudinal"]
    if (outer["execution_status"] != execution["status"]
            or outer["execution_reason_codes"] != execution["reason_codes"]):
        _fail(path, "requested series execution must agree with its capability execution mirror")
    admission_failed = ("R_LONGITUDINAL_RESOURCE_LIMIT" in reasons and execution["status"] == "failed" and not snapshots)
    selection_failed = ("R_LONGITUDINAL_SELECTION_INVALID" in reasons and execution["status"] == "failed"
                        and inputs["order_source"] is None and not pairs)
    if not admission_failed and not selection_failed and inputs["selected_version_count"] != len(snapshots):
        _fail(path, "selected-version count must preserve every selected snapshot")
    if selection_failed and inputs["selected_version_count"] < len(snapshots):
        _fail(path, "failed selection cannot retain more populations than supplied declarations")
    if inputs["selected_version_count"] > inputs["max_versions"] and not admission_failed:
        _fail(path, "version admission cannot silently truncate selected work")
    if inputs["order_source"] is None:
        if execution["status"] != "failed" or pairs or inputs["primary_snapshot_id"] is not None:
            _fail(path, "failed selection cannot fabricate chronology or comparisons")
    else:
        if len(snapshots) < 2 or inputs["primary_snapshot_id"] not in snapshot_map:
            _fail(path, "ordered series requires its primary snapshot and at least two versions")
        if snapshot_map[inputs["primary_snapshot_id"]]["input_role"] != "records_primary":
            _fail(path, "primary snapshot reference must name the primary input population")
        schedule = []
        for later in range(1, len(snapshots)):
            if inputs["baseline"] == "first":
                schedule.append((snapshot_ids[0], snapshot_ids[later], ["adjacent", "baseline"] if later == 1 else ["baseline"]))
            if inputs["baseline"] == "none" or later > 1:
                schedule.append((snapshot_ids[later - 1], snapshot_ids[later], ["adjacent"]))
        if [(row["earlier_snapshot_id"], row["later_snapshot_id"], row["kinds"]) for row in pairs] != schedule:
            _fail(path, "comparisons must retain the exact adjacent and optional first-baseline schedule")
    literal_versions = [row["dataset_version"] for row in snapshots if row["dataset_version"] is not None]
    if len(literal_versions) != len(set(literal_versions)):
        _fail(path, "selected version literals must be distinct")
    if inputs["order_source"] is not None and len(literal_versions) == len(snapshots):
        retained_order = payload["inputs"].get("version_order", [])
        if retained_order and [version for version in retained_order if version in literal_versions] != literal_versions:
            _fail(path, "selected snapshot chronology must be a subsequence of the retained input order")
    if inputs["order_source"] is not None:
        primary = inputs["primary_snapshot_id"]
        if [row["snapshot_id"] for row in snapshots if row["input_role"] == "records_primary"] != [primary]:
            _fail(path, "ordered series requires exactly one primary snapshot")
        nonempty = [row["snapshot_id"] for row in snapshots if not row["empty_scope"]]
        if not nonempty or primary != nonempty[-1]:
            _fail(path, "primary snapshot must be the latest nonempty selected population")
    allowed_scopes = set()
    for ordinal, descriptor in enumerate(snapshots, 1):
        sid = descriptor["snapshot_id"]
        population_id, representation_id = descriptor["population_scope_id"], descriptor["representation_scope_id"]
        if descriptor["ordinal"] != ordinal or population_id != sid + ".population" or population_id not in scope_map:
            _fail(path, "snapshot ordinals and complete population scopes must match their structural identity")
        allowed_scopes.add(population_id)
        population = scope_map[population_id]
        if (population["snapshot_id"] != sid or population["excluded_record_count"] != 0
                or population["denominator_basis"] != "selected_valid_records"
                or descriptor["empty_scope"] != (population["record_count"] == 0)
                or (descriptor["input_role"] == "declared_empty") != descriptor["empty_scope"]):
            _fail(path, "snapshot population scope must retain exact membership totals and empty declarations")
        if descriptor["basis_id"] is not None and descriptor["basis_id"] not in basis_ids:
            _fail(path, "snapshot basis reference is foreign")
        if representation_id is not None:
            if representation_id != sid + ".representation" or representation_id not in scope_map:
                _fail(path, "representation scope must resolve within its selected snapshot")
            allowed_scopes.add(representation_id)
            scope = scope_map[representation_id]
            if (scope["snapshot_id"] != sid or scope["record_count"] + scope["excluded_record_count"] != population["record_count"]
                    or scope["denominator_basis"] != "included_representation_records"):
                _fail(path, "representation scope must partition the complete population")
        redaction = descriptor["redaction"]
        if (descriptor["dataset_version"] is None) != (redaction is not None and "dataset_version" in redaction["omitted_fields"]):
            _fail(path, "omitted version literal must retain explicit identity redaction metadata")
        for row in (observed_map[sid], metric_map[sid]):
            for name, envelope in row.items():
                if name == "snapshot_id":
                    continue
                expected_scope = representation_id if name in ("support_size", "gini_simpson_diversity") else population_id
                if envelope["scope_id"] != (expected_scope or population_id):
                    _fail(path, "snapshot envelope references the wrong selected scope")
                if envelope["basis_id"] is not None and envelope["basis_id"] != descriptor["basis_id"]:
                    _fail(path, "snapshot envelope references the wrong representation basis")
        _series_snapshot_checks(observed_map[sid], metric_map[sid], population)
    for basis in bases:
        omitted = basis["redaction"] is not None and "state_semantics" in basis["redaction"]["omitted_fields"]
        if (basis["state_semantics"] is None) != omitted:
            _fail(path, "omitted state meaning requires explicit redaction metadata")
        if payload["run"]["redacted_mode"] and basis["state_semantics"] is not None:
            _fail(path, "redacted reports cannot retain user state-meaning text")
    for descriptor, row in zip(pairs, derived["comparisons"]):
        pid = descriptor["comparison_id"]
        earlier, later = (snapshot_map[descriptor[key]] for key in ("earlier_snapshot_id", "later_snapshot_id"))
        for side, endpoint in (("earlier", earlier), ("later", later)):
            if descriptor[side + "_basis_id"] != endpoint["basis_id"]:
                _fail(path, "comparison basis does not match its endpoint declaration")
            optional_scope = pid + "." + side
            if optional_scope in scope_map:
                allowed_scopes.add(optional_scope)
                scope = scope_map[optional_scope]
                population = scope_map[endpoint["population_scope_id"]]
                if scope["snapshot_id"] != endpoint["snapshot_id"] or scope["record_count"] + scope["excluded_record_count"] != population["record_count"]:
                    _fail(path, "harmonized endpoint scope must retain its selected population")
        basis = descriptor["harmonized_basis_id"]
        if descriptor["compatibility_status"] == "available":
            if basis not in basis_ids or descriptor["reason_codes"]:
                _fail(path, "compatible comparison requires its declared harmonized basis")
        elif basis is not None or not descriptor["reason_codes"]:
            _fail(path, "blocked comparison must preserve its gap and reasons")
        mapping = descriptor["mapping"]
        if mapping is not None:
            source, target = (earlier, later) if mapping["direction"] == "earlier_to_later" else (later, earlier)
            if mapping["source_basis_id"] != source["basis_id"] or mapping["target_basis_id"] != target["basis_id"]:
                _fail(path, "directed mapping basis references do not match its endpoints")
            if descriptor["mapping_collisions"] is None and descriptor["compatibility_status"] == "available":
                _fail(path, "mapping summary requires bounded collision evidence")
            groups = descriptor["mapping_collisions"]
            if groups is not None and groups["items"] is not None:
                targets = [group["target_state"] for group in groups["items"]]
                if len(targets) != len(set(targets)):
                    _fail(path, "mapping collision groups require distinct target identities")
            for group in (() if groups is None else groups["items"] or ()):
                if group["source_states"]["total_count"] < 2:
                    _fail(path, "collision group requires at least two source states")
        elif descriptor["mapping_collisions"] is not None:
            _fail(path, "unmapped comparison cannot contain mapping collision evidence")
        for name, envelope in row.items():
            if name == "comparison_id":
                continue
            for side, endpoint in (("earlier", earlier), ("later", later)):
                scope_id = envelope[side + "_scope_id"]
                if scope_id not in scope_map or scope_map[scope_id]["snapshot_id"] != endpoint["snapshot_id"]:
                    _fail(path, "comparison envelope references a foreign endpoint scope")
            if envelope["basis_id"] is not None and envelope["basis_id"] != basis:
                _fail(path, "comparison envelope references a foreign harmonized basis")
            if descriptor["compatibility_status"] == "unavailable" and envelope["status"] != "unavailable":
                _fail(path, "blocked comparison cannot contain a completed metric")
            if "earlier_value" in envelope:
                a, b, value = (envelope[key] for key in ("earlier_value", "later_value", "value"))
                if value is not None:
                    if a is None or b is None:
                        _fail(path, "available difference requires both explicit endpoint values")
                    expected = {key: b[key] - a[key] for key in value} if type(value) is dict else b - a
                    if not _series_equal(value, expected):
                        _fail(path, "difference must equal later minus earlier")
                endpoint_name = "source_type_shares" if name == "source_type_share_deltas" else name.removesuffix("_delta")
                if endpoint_name == "support":
                    endpoint_name = "support_size"
                if name not in ("support_delta", "gini_simpson_diversity_delta") or mapping is None:
                    for side, endpoint in (("earlier", earlier), ("later", later)):
                        sid = endpoint["snapshot_id"]
                        source = observed_map[sid] if endpoint_name in observed_map[sid] else metric_map[sid]
                        source_envelope = source[endpoint_name]
                        if not _series_equal(envelope[side + "_value"], source_envelope["value"]):
                            _fail(path, "difference endpoint value disagrees with its declared snapshot")
                        not_requested = "R_LONGITUDINAL_FAMILY_NOT_REQUESTED" in envelope["reason_codes"]
                        expected_denominator = None if name == "record_count_delta" or not_requested else source_envelope["denominator"]
                        if envelope[side + "_denominator"] != expected_denominator:
                            _fail(path, "difference endpoint denominator disagrees with its declared snapshot")
                        if envelope[side + "_reason_codes"] != source_envelope["reason_codes"]:
                            _fail(path, "difference endpoint must preserve the source reason list")
                        endpoint_coverage = envelope[side + "_coverage"]
                        count = scope_map[endpoint["population_scope_id"]]["record_count"]
                        coverage_denominator = count
                        coverage_name = "all_valid_records_in_selected_dataset_scope"
                        source_coverage = source_envelope["coverage"]
                        if name == "record_count_delta" or not_requested:
                            coverage_expected = False
                        elif endpoint_name in ("support_size", "gini_simpson_diversity"):
                            coverage_expected = endpoint["representation_scope_id"] is not None
                            coverage_name = "selected_valid_records"
                        elif endpoint_name in ("unresolved_parent_reference_count", "resolved_parent_edge_coverage"):
                            coverage_denominator = observed_map[sid]["declared_parent_reference_count"]["value"]
                            coverage_expected = coverage_denominator is not None
                            coverage_name = "declared_parent_references"
                        elif endpoint_name in ("distinct_external_root_count", "ancestry_concentration_hhi", "effective_external_root_count"):
                            coverage_expected = metric_map[sid]["grounded_record_count"]["value"] is not None
                        elif endpoint_name in ("resolved_lineage_coverage", "external_ancestry_coverage") or endpoint_name.startswith("lineage_closure_"):
                            coverage_expected = metric_map[sid]["records_with_resolved_external_ancestry"]["value"] is not None
                        else:
                            coverage_expected = count > 0
                        if (endpoint_coverage is not None) != coverage_expected:
                            _fail(path, "difference endpoint must preserve source coverage presence")
                        if endpoint_coverage is not None:
                            if (endpoint_coverage["denominator"] != coverage_denominator
                                    or endpoint_coverage["denominator_name"] != coverage_name):
                                _fail(path, "difference endpoint must preserve its named coverage population")
                            expected_coverage = endpoint_coverage["ratio"]
                            if endpoint_name in ("unresolved_parent_reference_count", "resolved_parent_edge_coverage") and endpoint_coverage["denominator"] == 0:
                                expected_coverage = 1
                            if not _series_equal(source_coverage, expected_coverage):
                                _fail(path, "difference endpoint coverage disagrees with its declared snapshot")
                        flag = side + "_no_declared_parents"
                        if flag in envelope and envelope[flag] != metric_map[sid]["resolved_parent_edge_coverage"]["no_declared_parents"]:
                            _fail(path, "difference endpoint lost its zero-reference convention")
        for count, table in (("support_loss_count", "extinct_states"), ("support_added_count", "added_states"),
                             ("tail_extinction_count", "tail_extinct_states")):
            if row[table]["value"] is not None and row[count]["value"] != row[table]["value"]["total_count"]:
                _fail(path, "bounded state detail must preserve its exact count")
        retention = row["support_retention_ratio"]
        retained = row["retained_states"]["value"]
        if retention["value"] is not None:
            if retained is None or not retention["denominator"] or not _series_equal(retention["value"], retained["total_count"] / retention["denominator"]):
                _fail(path, "retention must use its earlier positive-mass support denominator")
    if set(scope_ids) != allowed_scopes:
        _fail(path, "scope inventory contains foreign or unreferenced scopes")
    statuses = []
    for row in (*execution["snapshot_statuses"], *execution["comparison_statuses"]):
        for family, status in row["families"].items():
            if (status["execution_status"] == "completed") != (not status["reason_codes"]):
                _fail(path, "family execution state must retain its explicit reasons")
            if family not in requested and status["execution_status"] != "not_requested":
                _fail(path, "omitted optional families cannot claim executed work")
            if "snapshot_id" in row:
                sid = row["snapshot_id"]
                candidates = (*observed_map[sid].items(), *metric_map[sid].items())
            else:
                candidates = next(item for item in derived["comparisons"] if item["comparison_id"] == row["comparison_id"]).items()
            for name, envelope in candidates:
                if name in ("snapshot_id", "comparison_id"):
                    continue
                lineage_metric = (name.startswith("lineage_closure_") or "parent_reference_count" in name
                    or name.startswith("resolved_parent_edge_coverage") or name.startswith("resolved_lineage_coverage")
                    or name.startswith("external_ancestry_coverage") or name.startswith("distinct_external_root_count")
                    or name.startswith("ancestry_concentration_hhi") or name.startswith("effective_external_root_count")
                    or name in ("grounded_record_count", "closed_record_count", "unresolved_record_count", "records_with_resolved_external_ancestry"))
                field_family = ("lineage" if lineage_metric else "tail" if name.startswith("tail_") else
                    "direct_closure" if name.startswith("direct_closure_") else
                    "provenance" if any(part in name for part in ("provenance", "source_type", "grounding_field")) else "distribution")
                if field_family == family:
                    if status["execution_status"] == "completed" and envelope["status"] != "available":
                        _fail(path, "completed family cannot contain partial or unavailable required evidence")
                    if family not in requested:
                        if envelope["value"] is not None or "R_LONGITUDINAL_FAMILY_NOT_REQUESTED" not in envelope["reason_codes"]:
                            _fail(path, "unrequested optional family must retain null evidence and its explicit reason")
            if family in requested and status["execution_status"] == "not_requested" and not (family == "tail" and "snapshot_id" in row):
                _fail(path, "requested family cannot claim it was not requested")
            if family in requested and not (family == "tail" and "snapshot_id" in row and status["execution_status"] == "not_requested"):
                statuses.append(status["execution_status"])
    if execution["status"] == "completed" and any(status != "completed" for status in statuses):
        _fail(path, "completed series requires every requested family and comparison to complete")
    useful = any(envelope["value"] is not None for row in derived["comparisons"]
                 for name, envelope in row.items() if name != "comparison_id" and "earlier_value" in envelope)
    if ((execution["status"] == "partial" and not useful)
            or (execution["status"] == "failed" and useful)):
        _fail(path, "partial and failed execution must distinguish useful supplied comparison values")
    shared = observed["shared_lineage"]
    if (shared is not None) != ("lineage" in requested):
        _fail(path, "shared graph evidence must reflect explicit lineage enablement")
    if shared is not None:
        if shared["execution_status"] != "completed" and not shared["reason_codes"]:
            _fail(path, "incomplete shared graph requires explicit reasons")
        if shared["cycle_status"] is not None and ((shared["cycle_status"] == "cyclic") != bool(shared["cycle_count"])):
            _fail(path, "shared cycle count and status disagree")
        if shared["resource_usage"] is not None:
            _lineage_usage_checks(shared["resource_usage"], shared["execution_status"])
            usage = shared["resource_usage"]
            if shared["loaded_record_count"] is not None and (shared["loaded_record_count"] != usage["admitted_node_count"]
                    or shared["loaded_record_count"] < sum(scope_map[row["population_scope_id"]]["record_count"] for row in snapshots)):
                _fail(path, "shared loaded scope must include every selected population and agree with admitted nodes")
            if shared["unique_edge_count"] is not None and shared["unique_edge_count"] != usage["admitted_edge_count"]:
                _fail(path, "shared unique edge count must agree with admitted graph evidence")


def _scenario_distribution(rows: list, state_order: list, path: str) -> list:
    if [row["state_id"] for row in rows] != state_order:
        _fail(path, "probability vector identities must agree with the declared state order")
    return [row["probability"] for row in rows]


def _scenario_normalization(record: dict, state_order: list, *, sampled: bool, path: str) -> list:
    """Validate supplied normalization evidence without importing a metric owner."""
    supplied = _scenario_distribution(record["supplied_distribution"], state_order, path)
    effective = _scenario_distribution(record["effective_distribution"], state_order, path)
    total = math.fsum(supplied)
    corrected = sampled and total != 1.0
    if total <= 0 or abs(total - 1.0) > 1e-12:
        _fail(path, "probability mass exceeds the declared absolute tolerance")
    expected = [value / total for value in supplied] if corrected else supplied
    corrections = [value - original for value, original in zip(expected, supplied)]
    if (effective != expected or any(original > 0 and value == 0 for original, value in zip(supplied, effective))
            or any(abs(value) > 1e-12 for value in corrections)):
        _fail(path, "effective probabilities disagree with the bounded normalization policy")
    if (record["supplied_probability_total"] != total
            or record["effective_probability_total"] != math.fsum(effective)
            or record["probability_residual"] != total - 1.0
            or record["correction_applied"] is not corrected
            or record["correction_method"] != ("divide_by_validated_total" if corrected else "none")
            or record["normalization_divisor"] != (total if corrected else 1.0)
            or [row["state_id"] for row in record["probability_corrections"]] != state_order
            or [row["correction"] for row in record["probability_corrections"]] != corrections):
        _fail(path, "normalization disclosure disagrees with its supplied and effective vectors")
    return effective


def _scenario_integer(value, lower: int, upper: int, path: str) -> None:
    if type(value) is not int or not lower <= value <= upper:
        _fail(path, "scenario integer is outside its explicit admission range")


def _scenario_paths(scenario: dict, path: str) -> tuple[list, list]:
    parameters = scenario["parameters"]
    states, n = parameters["state_order"], parameters["resample_size"]
    initial = [row["probability"] for row in scenario["initial_distribution"]]
    horizon, replicates = parameters["simulation_horizon"], parameters["simulation_replicates"]
    paths = scenario["sampled_paths"]
    if [row["replicate_index"] for row in paths] != list(range(replicates)):
        _fail(path, "sampled paths must cover every replicate in the declared schedule")
    losses, returns = [], []
    reopened = scenario["model"] == "reopened_resampling"
    sources = scenario.get("mixed_sources", [])
    expected_source_keys = [(replicate, step) for replicate in range(replicates) for step in range(1, horizon + 1)]
    if reopened and [(row["replicate_index"], row["step"]) for row in sources] != expected_source_keys:
        _fail(path, "mixed sources must cover every transition in the declared schedule")
    external = [row["probability"] for row in scenario.get("external_input_distribution", [])]
    weight = parameters["reopening_weight"]
    source_index = 0
    for replicate, sampled in enumerate(paths):
        generations = sampled["generations"]
        if [row["step"] for row in generations] != list(range(horizon + 1)):
            _fail(path, "sampled generations must cover step zero through the horizon")
        previous = None
        for step, generation in enumerate(generations):
            frequencies, counts = generation["state_frequencies"], generation["state_counts"]
            if len(frequencies) != len(states):
                _fail(path, "sampled frequency vector must preserve the declared states")
            if step == 0:
                if counts is not None or frequencies != initial:
                    _fail(path, "step zero must preserve the effective start without invented counts")
            elif (counts is None or len(counts) != len(states)
                    or any(type(count) is not int for count in counts) or sum(counts) != n
                    or frequencies != [count / n for count in counts]):
                _fail(path, "sampled counts and frequencies must agree with the resample size")
            support = [state for state, frequency in zip(states, frequencies) if frequency > 0]
            diversity = 1.0 - math.fsum(frequency * frequency for frequency in frequencies)
            if (generation["support"] != support or generation["support_size"] != len(support)
                    or generation["gini_simpson_diversity"] != diversity or not 0 <= diversity < 1):
                _fail(path, "support and diversity must agree with the supplied frequencies")
            if step:
                effective_source = previous
                if reopened:
                    source = sources[source_index]
                    source_index += 1
                    if weight == 0:
                        raw_source = previous
                        input_basis = "effective_internal_distribution" if step == 1 else "sampled_integer_counts_over_resample_size"
                    elif weight == 1:
                        raw_source = external
                        input_basis = "effective_external_distribution"
                    else:
                        raw_source = [math.fsum(((1.0 - weight) * p, weight * r)) for p, r in zip(previous, external)]
                        if any((p > 0 or r > 0) and mass == 0 for p, r, mass in zip(previous, external, raw_source)):
                            _fail(path, "mixture arithmetic cannot erase a positive source")
                        input_basis = "computed_external_mixture"
                    record = source["input_normalization"]
                    if ([row["probability"] for row in record["supplied_distribution"]] != raw_source
                            or source["input_basis"] != input_basis):
                        _fail(path, "transition source must be the declared constant-source mixture")
                    effective_source = _scenario_normalization(record, states, sampled=0 < weight < 1, path=path)
                    possible = [state for state, p, mass, r in zip(states, previous, effective_source, external)
                                if p == 0 and mass > 0 and weight > 0 and r > 0]
                    if source["possible_reentry_states"] != possible:
                        _fail(path, "possible reentry identities disagree with the transition source")
                if any(count > 0 and mass <= 0 for count, mass in zip(counts, effective_source)):
                    _fail(path, "positive sampled counts require positive transition source probability")
                for state, before, after in zip(states, previous, counts):
                    event = {"replicate_index": replicate, "step": step, "state_id": state}
                    if before > 0 and after == 0:
                        losses.append(event)
                    if reopened and before == 0 and after > 0:
                        returns.append(event)
            previous = frequencies
    for field, value_field, source_field in (
        ("support_trajectories", "support_sizes", "support_size"),
        ("support_trajectory", "support_sizes", "support_size"),
        ("diversity_trajectory", "gini_simpson_diversities", "gini_simpson_diversity"),
    ):
        if field in scenario:
            expected = [{"replicate_index": index, value_field: [row[source_field] for row in sampled["generations"]]}
                        for index, sampled in enumerate(paths)]
            if scenario[field] != expected:
                _fail(path, "trajectory summaries must agree with every sampled generation")
    if "extinction_events" in scenario and scenario["extinction_events"] != losses:
        _fail(path, "extinction events must cover exactly the positive-to-zero transitions")
    if reopened and scenario["state_reentry_events"] != returns:
        _fail(path, "reentry events must cover exactly the realized absent-to-positive transitions")
    return losses, returns


def _scenario_analytic(scenario: dict, path: str) -> None:
    parameters = scenario["parameters"]
    n, horizon = parameters["resample_size"], parameters["simulation_horizon"]
    initial = 1.0 - math.fsum(row["probability"] * row["probability"] for row in scenario["initial_distribution"])
    expected, underflow = [initial], []
    for step in range(1, horizon + 1):
        value = 0.0 if n == 1 or initial == 0 else initial * math.exp(step * math.log1p(-1.0 / n))
        expected.append(value)
        if initial > 0 and n > 1 and value == 0:
            underflow.append(step)
    if (scenario["initial_gini_simpson_diversity"] != initial
            or scenario["contraction_factor"] != 1.0 - 1.0 / n
            or scenario["expected_diversity"] != expected
            or scenario["numerical_underflow_steps"] != underflow):
        _fail(path, "closed analytic expectation and underflow disclosure disagree with the supplied basis")


def _scenario_envelope(scenario: dict, *, name: str, run_seed, path: str) -> None:
    parameters, method = scenario["parameters"], scenario["method"]
    reopened = name == "external_reopening"
    experiment = reopened or "scenario_schedule" in parameters
    if (name == "tail_extinction") != (method == "analytic_extinction"):
        _fail(path, "scenario family and method disagree")
    if (scenario["resample_size"] != parameters["resample_size"]
            or scenario["denominator"] != parameters["resample_size"] or scenario["denominator_reason"] is not None):
        _fail(path, "scenario resample size and denominator declarations must agree")
    stochastic = ("random_seed", "simulation_replicates", "rng_name", "numpy_version", "replicate_schedule")
    replay = ("sampler_algorithm", "state_schedule", "scenario_schedule")
    if method == "sampled_path":
        if any(parameters[key] is None for key in stochastic) or parameters["random_seed"] != run_seed:
            _fail(path, "sampled paths require replay metadata and the common run seed")
    elif any(parameters[key] is not None for key in stochastic) or any(key in parameters for key in replay):
        _fail(path, "analytic evidence cannot claim a random realization or sampling schedule")
    if not reopened and (parameters["reopening_weight"] is not None or parameters["external_input_distribution"]):
        _fail(path, "closed and tail models cannot contain external reopening inputs")
    if reopened and (parameters["reopening_weight"] is None or not parameters["external_input_distribution"]):
        _fail(path, "reopened evidence requires its explicit external distribution and weight")
    required_results = {"analytic_extinction": ("by_state",),
        "analytic_expectation": ("initial_gini_simpson_diversity", "contraction_factor", "expected_diversity", "numerical_underflow_steps"),
        "sampled_path": ("sampled_paths",)}[method]
    if any(key not in scenario for key in required_results):
        _fail(path, "selected method requires its typed result fields")
    if method == "analytic_extinction":
        if parameters["simulation_horizon"] != 1:
            _fail(path, "one-step extinction requires horizon one")
        return
    if len(scenario["scope"]["dataset_versions"]) != 1:
        _fail(path, "scenario scope must declare exactly one supplied version")
    if (experiment or "baseline_basis" in scenario) and not reopened and scenario["model_version"] != "closed_categorical_v1":
        _fail(path, "closed experiment and baseline require their declared method version")
    states = parameters["state_order"]
    if not 1 <= len(states) <= 4096:
        _fail(path, "declared state count exceeds scenario admission bounds")
    _scenario_integer(parameters["resample_size"], 1, 2147483647, path)
    _scenario_integer(parameters["simulation_horizon"], 0, 10000, path)
    if method == "sampled_path":
        _scenario_integer(parameters["simulation_replicates"], 1, 10000, path)
        if len(states) * (parameters["simulation_horizon"] + 1) * parameters["simulation_replicates"] > 1000000:
            _fail(path, "sampled path evidence exceeds the admitted work bound")
    initial = _scenario_distribution(scenario["initial_distribution"], states, path)
    if "input_normalization" in scenario:
        normalized = _scenario_normalization(scenario["input_normalization"], states, sampled=method == "sampled_path", path=path)
        if initial != normalized:
            _fail(path, "initial distribution differs from the effective input")
    elif experiment:
        _fail(path, "experiment must retain its input normalization evidence")
    elif abs(math.fsum(initial) - 1.0) > 1e-12:
        _fail(path, "legacy initial probability vector exceeds the absolute mass tolerance")
    if parameters["input_basis"] != "explicit_supplied_state_probability_vector":
        _fail(path, "scenario input basis must retain its explicit supplied declaration")
    if experiment:
        _scenario_integer(parameters["random_seed"], 0, 2**53 - 1, path)
        if any(key not in parameters for key in replay) or "state_semantics" not in scenario or "assumption_table" not in scenario:
            _fail(path, "experiment evidence requires shared meaning, assumptions and all replay identities")
        if scenario["assumption_table"] != _scenario_assumption_table(reopened):
            _fail(path, "experiment assumption table must retain its model-specific fixed declarations")
        if not reopened and any(key not in scenario for key in ("analytic_baseline", "extinction_events")):
            _fail(path, "closed experiment must retain its separate baseline and complete event evidence")
    elif any(key in scenario for key in ("state_semantics", "analytic_baseline", "assumption_table")):
        _fail(path, "experiment-only fields require the explicit experiment replay schedule")
    if reopened:
        external = _scenario_normalization(scenario["external_input_normalization"], states, sampled=True, path=path)
        if (_scenario_distribution(scenario["external_input_distribution"], states, path) != external
                or parameters["external_input_distribution"] != scenario["external_input_distribution"]):
            _fail(path, "external parameter declaration and effective distribution disagree")
        if parameters["simulation_horizon"] >= 2 and parameters["reopening_weight"] > 0 and any(
                r > 0 and parameters["reopening_weight"] * r == 0 for r in external):
            _fail(path, "external mixture would erase future positive reachability")
    if method == "sampled_path":
        if any(key in scenario for key in ("expected_diversity", "contraction_factor", "initial_gini_simpson_diversity", "numerical_underflow_steps")):
            _fail(path, "sampled paths cannot also claim the distinct analytic expectation fields")
        _scenario_paths(scenario, path)
    else:
        if any(key in scenario for key in ("sampled_paths", "support_trajectories", "extinction_events")):
            _fail(path, "analytic expectation cannot contain realized sampled evidence")
        _scenario_analytic(scenario, path)
    if "analytic_baseline" in scenario:
        analytic = scenario["analytic_baseline"]
        _scenario_envelope(analytic, name="closed_resampling", run_seed=run_seed, path=path + ".analytic_baseline")
        if any(analytic[key] != scenario[key] for key in ("scope", "representation", "resample_size", "initial_distribution")):
            _fail(path, "analytic baseline must share the sampled closed basis")
        if (analytic["parameters"]["simulation_horizon"] != parameters["simulation_horizon"]
                or analytic["parameters"]["state_order"] != states
                or analytic["input_normalization"]["supplied_distribution"] != scenario["initial_distribution"]
                or analytic["baseline_basis"] != "closed_sampled_effective_distribution"):
            _fail(path, "analytic baseline must use the actual effective sampled start")


def _scenario_comparison(scenarios: dict) -> None:
    reopened, closed = scenarios.get("external_reopening"), scenarios.get("closed_resampling")
    if reopened is None:
        return
    comparison = reopened.get("scenario_comparison")
    both = closed is not None and "scenario_schedule" in closed["parameters"]
    if (comparison is not None) != both:
        _fail("$.simulations", "comparison evidence must occur exactly when both experiment models are supplied")
    if not both:
        return
    path = "$.simulations.external_reopening.scenario_comparison"
    for key in ("scope", "representation", "initial_distribution", "input_normalization", "state_semantics"):
        if closed[key] != reopened[key]:
            _fail(path, "compared scenarios must share the same declared starting basis")
    common = ("resample_size", "simulation_horizon", "random_seed", "simulation_replicates", "rng_name", "numpy_version",
              "replicate_schedule", "state_order", "input_basis", "numerical_policy", "sampler_algorithm", "state_schedule", "scenario_schedule")
    if any(closed["parameters"][key] != reopened["parameters"][key] for key in common):
        _fail(path, "compared scenarios must share all common parameters and sampling identities")
    parameters = closed["parameters"]
    if 2 * len(parameters["state_order"]) * (parameters["simulation_horizon"] + 1) * parameters["simulation_replicates"] > 1000000:
        _fail(path, "combined sampled evidence exceeds the aggregate work bound")
    rows = []
    for left, right in zip(closed["sampled_paths"], reopened["sampled_paths"]):
        for a, b in zip(left["generations"], right["generations"]):
            rows.append({"replicate_index": left["replicate_index"], "step": a["step"],
                "closed_support_size": a["support_size"], "reopened_support_size": b["support_size"],
                "support_size_difference": b["support_size"] - a["support_size"],
                "closed_gini_simpson_diversity": a["gini_simpson_diversity"],
                "reopened_gini_simpson_diversity": b["gini_simpson_diversity"],
                "diversity_difference": b["gini_simpson_diversity"] - a["gini_simpson_diversity"]})
    if comparison["rows"] != rows:
        _fail(path, "comparison rows must bind both supplied paths and labeled differences")
    states = parameters["state_order"]
    initial = [row["probability"] for row in closed["initial_distribution"]]
    external = [row["probability"] for row in reopened["external_input_distribution"]]
    weight = reopened["parameters"]["reopening_weight"]
    reachability = [
        {"model_name": "closed_resampling", "reachable_states": [s for s, p in zip(states, initial) if p > 0],
         "possible_reentry_states": [], "timing": "before_first_draw"},
        {"model_name": "reopened_resampling", "reachable_states": [s for s, p, r in zip(states, initial, external)
            if (weight < 1 and p > 0) or (weight > 0 and r > 0)],
         "possible_reentry_states": [s for s, p, r in zip(states, initial, external) if p == 0 and weight > 0 and r > 0],
         "timing": "before_first_draw"},
    ]
    if comparison["initial_reachability"] != reachability:
        _fail(path, "initial reachability must describe coefficient-positive possibilities before the first draw")


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
    _lineage_semantic_checks(payload)
    _longitudinal_semantic_checks(payload)
    tail = payload["derived_metrics"].get("tail", {})
    if "tail_rule" in tail and "selection" in tail and tail["tail_rule"] != tail["selection"]["rule"]:
        _fail("$.derived_metrics.tail", "tail rule declarations disagree")
    for path, item, contract in _walk(payload):
        if type(item) is list and item and all(type(row) is dict for row in item):
            if path[:1] == ("simulations",) and path[-1] in ("extinction_events", "state_reentry_events"):
                event_ids = [(row["replicate_index"], row["step"], row["state_id"]) for row in item]
                if len(event_ids) != len(set(event_ids)):
                    _fail("$.table", "event composite identity must be unique")
            elif path[:1] == ("simulations",) and path[-1] in ("mixed_sources", "rows"):
                row_ids = [(row["replicate_index"], row["step"]) for row in item]
                if len(row_ids) != len(set(row_ids)):
                    _fail("$.table", "transition composite identity must be unique")
            else:
                for identity in ("state_id", "source_state", "replicate_index"):
                    if all(identity in row for row in item):
                        identities = [row[identity] for row in item]
                        if len(identities) != len(set(identities)):
                            _fail("$.table", "typed table identity must be unique")
        if type(item) is not dict:
            continue
        if "detail_status" in contract.get("properties", {}):
            _lineage_detail_checks(item, unique=path != (
                "observed_facts", "longitudinal", "shared_lineage", "graph_diagnostics"))
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
            if not math.isclose(interval["interval_width"]["value"], upper - lower, rel_tol=1e-12, abs_tol=1e-12):
                _fail("$.derived_metrics.closure_exposure", "interval width disagrees with endpoints")
    for name, scenario in payload["simulations"].items():
        _scenario_envelope(scenario, name=name, run_seed=payload["run"]["random_seed"], path="$.simulations." + name)
    _scenario_comparison(payload["simulations"])
    capability = payload["capabilities"].get("intervention_simulation")
    if capability is not None and capability["execution_status"] in ("completed", "partial") and not payload["simulations"]:
        _fail("$.capabilities.intervention_simulation", "executed simulation capability requires actually supplied results")
    if payload["simulations"] and not any(row["conclusion"] == "empirical_intervention_effect"
                                        for row in payload["unavailable_conclusions"]):
        _fail("$.unavailable_conclusions", "simulation evidence must retain the unavailable empirical intervention effect")


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
