"""Phase 5 supplied lineage values, bounded details and report semantics.

The small graphs exercise report integration. Frozen Hero fractions remain the
independent numerical oracle; graph and root algorithms retain their own tests.
"""

from copy import deepcopy
from dataclasses import replace
from fractions import Fraction
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from recursive_integrity_toolkit.errors import LineageResourceLimitError
from recursive_integrity_toolkit.io.validation import join_provenance, validate_bundle
from recursive_integrity_toolkit.lineage.ancestry import analyze_lineage, shared_ancestry_dependence
from recursive_integrity_toolkit.lineage.graph import LineageLimits
from recursive_integrity_toolkit.metrics.bounds import direct_closure_exposure, lineage_closure_exposure
from recursive_integrity_toolkit.metrics.provenance import summarize_provenance
from recursive_integrity_toolkit.models import (
    AuditBundle, CalculationScope, CapabilityKey, FileRole, InputSource,
    ValidationMessage, ValidationSeverity,
)
from recursive_integrity_toolkit.reports.assembly import (
    assemble_report, privacy_view, FamilyFailure, ReportAssemblyError,
)
from recursive_integrity_toolkit.reports.json_report import render_json
from recursive_integrity_toolkit.reports.markdown_report import render_markdown
from recursive_integrity_toolkit.result import CanonicalReport, ReportValidationError, validate_report


_ROOT = Path(__file__).resolve().parents[2]


def _run():
    nullable = ("started_at", "completed_at", "duration_seconds", "python_version",
                "platform", "command", "config_hash", "random_seed")
    return {
        "run_id": "lineage-report-integration", "toolkit_version": "0.1.0.dev3",
        "report_schema_version": "1.1", **dict.fromkeys(nullable),
        "strict_mode": False, "redacted_mode": False, "network_call_count": 0,
        "deterministic": True, "privacy_mode": "standard", "run_status": "complete",
        "null_reasons": {name: "not_recorded" for name in nullable},
    }


def _validation(tmp_path, declarations, *, grounding=None, transformation=None,
                target="v2", order=None, content="fixture text"):
    """Load a small real bundle with explicit roles, including empty targets."""
    tmp_path.mkdir(parents=True, exist_ok=True)
    primary, context, provenance = [], [], []
    for identity, parents in declarations.items():
        version, record_id = identity.split("::")
        key = {"dataset_version": version, "record_id": record_id}
        (primary if version == target else context).append({**key, "content": content})
        value = (grounding or {}).get(identity, "no")
        provenance.append({**key, "source_type": "human" if value == "yes" else "synthetic",
            "provenance_confidence": "confirmed", "external_grounding": value,
            "transformation": (transformation or {}).get(identity, "generate"), "parent_ids": parents})
    empty_target = not primary
    if empty_target:
        primary, context = context, []
    sources = []
    for name, role, rows in (("records.jsonl", FileRole.RECORDS_PRIMARY, primary),
                             ("context.jsonl", FileRole.RECORDS_COMPARE, context),
                             ("provenance.jsonl", FileRole.PROVENANCE_MANIFEST, provenance)):
        if rows:
            path = tmp_path / name
            path.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")
            sources.append(InputSource(role, path))
    versions = sorted({identity.split("::")[0] for identity in declarations} | ({target} if target else set()))
    bundle = validate_bundle(AuditBundle(tuple(sources)), configuration={"version_order": order or versions})
    if empty_target:
        bundle = replace(bundle, records=tuple(replace(row,
            location=replace(row.location, file_role=FileRole.RECORDS_COMPARE)) for row in bundle.records))
    return bundle


def _report(bundle, *, target="v2", limits=None, derived=True, **kwargs):
    result = analyze_lineage(bundle, target_dataset_version=target,
                             **({"limits": limits} if limits else {}))
    if derived:
        kwargs.update(lineage_bounds=lineage_closure_exposure(result),
                      shared_ancestry=shared_ancestry_dependence(result))
    return assemble_report(bundle, run=_run(), lineage=result, **kwargs), result


def _checked(report):
    payload = report.to_dict()
    root_schema = json.loads((_ROOT / "schemas/report.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator(root_schema).validate(payload)
    validate_report(payload)
    assert len(payload) == 12
    assert payload["run"]["report_schema_version"] == "1.1"
    assert payload["capabilities"] == payload["observability"]["capabilities"]
    return payload


def _values(family):
    return {name: field["value"] for name, field in family.items() if isinstance(field, dict) and "value" in field}


def _bounds(payload):
    family = payload["derived_metrics"]["closure_exposure"]["lineage"]
    return tuple(family[name]["value"] for name in ("lower_bound", "upper_bound", "interval_width"))


def _hero():
    hero = _ROOT / "examples/hero"
    bundle = validate_bundle(AuditBundle((
        InputSource(FileRole.RECORDS_PRIMARY, hero / "records_v2.csv"),
        InputSource(FileRole.RECORDS_COMPARE, hero / "records_v1.csv"),
        InputSource(FileRole.PROVENANCE_MANIFEST, hero / "provenance.csv"),
        InputSource(FileRole.VERSION_ORDER, hero / "version_order.json"),
    )))
    joined = join_provenance(bundle.records, bundle.provenance, dataset_versions=("v2",))
    scope = CalculationScope(("v2",), joined.scope_record_keys, (),
                             joined.provenance_row_coverage.denominator_name, "hero-provenance-v2")
    provenance = summarize_provenance(joined, scope=scope)
    return bundle, provenance, direct_closure_exposure(provenance)


def test_unrequested_lineage_uses_schema_11_without_execution_claims(tmp_path):
    bundle = _validation(tmp_path, {"v2::anchor": []}, grounding={"v2::anchor": "yes"})
    payload = _checked(assemble_report(bundle, run=_run()))
    lineage = payload["capabilities"]["lineage"]
    assert lineage["execution_status"] == "not_requested"
    assert lineage["execution_scope"] == [] and lineage["execution_reason_codes"]
    assert payload["observability"]["maximum_level"] == bundle.observability.maximum_level
    assert payload["observed_facts"]["lineage"]["cycle_status"]["value"] is None
    for name, field in payload["derived_metrics"].get("lineage", {}).items():
        if name != "resolved_parent_edge_coverage":
            assert field["value"] is None and field["status"] == "unavailable"
    proxy = payload["proxy_signals"].get("shared_ancestry_dependence")
    assert proxy is None or (proxy["status"], proxy["level"]) == ("unavailable", "indeterminate")


def test_hero_report_retains_exact_lineage_and_independent_direct_values():
    bundle, provenance, direct = _hero()
    report, result = _report(bundle, provenance=provenance, closure=direct)
    payload = _checked(report)
    expected = json.loads((_ROOT / "tests/fixtures/lineage_complete/hero_expected.json").read_text())
    facts = payload["observed_facts"]["lineage"]
    scope = facts["graph_scope"]["value"]
    assert scope == {"target_dataset_version": "v2", "target_record_count": 8,
                     "loaded_record_count": 16, "context_record_count": 8,
                     "loaded_dataset_versions": ["v1", "v2"]}
    metrics = payload["derived_metrics"]["lineage"]
    assert {key: metrics[key]["value"] for key in (
        "grounded_record_count", "closed_record_count", "unresolved_record_count",
        "records_with_resolved_external_ancestry")} == {
        "grounded_record_count": 8, "closed_record_count": 0, "unresolved_record_count": 0,
        "records_with_resolved_external_ancestry": 8}
    for name in ("resolved_lineage_coverage", "external_ancestry_coverage", "resolved_parent_edge_coverage"):
        assert metrics[name]["value"] == 1.0
        assert metrics[name]["scope"]["record_count"] == 8
    assert facts["declared_parent_edge_count"]["value"] == 8
    assert facts["resolved_parent_edge_count"]["value"] == 8
    assert metrics["distinct_external_root_count"]["value"] == 5
    assert metrics["ancestry_concentration_hhi"]["value"] == float(Fraction(expected["ancestry_hhi"]))
    assert metrics["effective_external_root_count"]["value"] == 4.0
    details = metrics["top_shared_ancestors"]["value"]
    assert (details["total_count"], details["returned_count"], details["omitted_count"], details["detail_status"]) == (5, 5, 0, "complete")
    rows = details["items"]
    assert [row["record_key"]["dataset_version"] + "::" + row["record_key"]["record_id"] for row in rows] == expected["root_order"]
    for name, oracle in (("incidence_count", "incidence"), ("incidence_share", "incidence_shares"),
                         ("fractional_mass", "fractional_masses"), ("normalized_weight", "normalized_weights")):
        assert [row[name] for row in rows] == [float(Fraction(value)) for value in expected[oracle]]
    assert all(row["incidence_denominator"] == row["weight_denominator"] == 8 for row in rows)
    assert _bounds(payload) == (0.0, 0.0, 0.0)
    direct_values = payload["derived_metrics"]["closure_exposure"]["direct"]
    assert tuple(direct_values[name]["value"] for name in ("lower_bound", "upper_bound", "interval_width")) == (0.5, 0.5, 0.0)
    assert payload["proxy_signals"]["shared_ancestry_dependence"]["level"] == "present"
    assert payload["capabilities"]["lineage"]["execution_status"] == "completed"
    assert facts["cycle_status"]["value"] == "acyclic"
    assert metrics["lineage_depth"]["value"] == result.lineage_depth
    assert {"causal_ancestor_effect", "complete_pipeline_closure"} <= {
        item["conclusion"] for item in payload["unavailable_conclusions"]}


@pytest.mark.parametrize("case,execution,counts,bounds,proxy_status,level", [
    ("partial_witness", "partial", (2, 0, 1), (0, 1 / 3, 1 / 3), "partial", "present"),
    ("partial_no_witness", "partial", (1, 0, 1), (0, 1 / 2, 1 / 2), "unavailable", "indeterminate"),
    ("all_closed", "completed", (0, 1, 0), (1, 1, 0), "available", "not_present"),
    ("all_unknown", "partial", (0, 0, 1), (0, 1, 1), "unavailable", "indeterminate"),
    ("all_cycle", "failed", (0, 0, 2), (0, 1, 1), "unavailable", "indeterminate"),
    ("empty", "completed", (0, 0, 0), (None, None, None), "unavailable", "indeterminate"),
])
def test_report_preserves_partition_uncertainty_and_execution_separately(
        tmp_path, case, execution, counts, bounds, proxy_status, level):
    declarations, grounding = {"v1::root": [], "v2::a": ["v1::root"]}, {"v1::root": "yes"}
    if case.startswith("partial"):
        declarations["v2::unknown"] = []
        grounding["v2::unknown"] = "unknown"
        if case == "partial_witness":
            declarations["v2::b"] = ["v1::root"]
    elif case == "all_closed":
        declarations = {"v2::closed": []}
    elif case == "all_unknown":
        declarations, grounding = {"v2::unknown": []}, {"v2::unknown": "unknown"}
    elif case == "all_cycle":
        declarations = {"v2::a": ["b"], "v2::b": ["a"]}
    elif case == "empty":
        declarations = {"v1::root": []}
    bundle = _validation(tmp_path, declarations, grounding=grounding)
    report, result = _report(bundle)
    payload = _checked(report)
    metrics = payload["derived_metrics"]["lineage"]
    assert tuple(metrics[name]["value"] for name in (
        "grounded_record_count", "closed_record_count", "unresolved_record_count")) == counts
    assert _bounds(payload) == bounds
    assert payload["capabilities"]["lineage"]["execution_status"] == execution
    original = bundle.observability.capabilities
    for key, capability in original.items():
        assert payload["capabilities"][key.value]["status"] == capability.status.value
    proxy = payload["proxy_signals"]["shared_ancestry_dependence"]
    assert (proxy["status"], proxy["level"]) == (proxy_status, level)
    if not counts[0]:
        assert metrics["ancestry_concentration_hhi"]["value"] is None
        assert "NO_RESOLVED_EXTERNAL_ROOTS" in metrics["ancestry_concentration_hhi"]["reason_codes"]
        assert metrics["distinct_external_root_count"]["value"] == 0
    if case == "empty":
        assert "EMPTY_TARGET_SCOPE" in metrics["resolved_lineage_coverage"]["reason_codes"]
        assert metrics["resolved_lineage_coverage"]["value"] is None
    assert payload["observability"]["maximum_level"] == bundle.observability.maximum_level
    assert result.scope.target_record_count == sum(counts)


def test_root_budget_failure_retains_completed_graph_depth_and_reference_observations(tmp_path):
    bundle = _validation(tmp_path, {"v1::root": [], "v2::child": ["root"]},
                         grounding={"v1::root": "yes"})
    report, result = _report(bundle, limits=LineageLimits(max_root_memberships=1))
    payload = _checked(report)
    facts, metrics = payload["observed_facts"]["lineage"], payload["derived_metrics"]["lineage"]
    assert payload["capabilities"]["lineage"]["execution_status"] == "failed"
    assert facts["cycle_status"]["value"] == "acyclic"
    assert facts["cycle_analysis"]["value"]["cycle_count"] == 0
    assert facts["depth_summary"]["value"]["maximum_resolved_target_depth"] == 1
    assert metrics["lineage_depth"]["value"] == 1
    assert metrics["resolved_parent_edge_coverage"]["value"] == 1.0
    assert facts["declared_parent_edge_count"]["value"] == 1
    for name in ("grounded_record_count", "closed_record_count", "unresolved_record_count",
                 "distinct_external_root_count", "top_shared_ancestors", "ancestry_concentration_hhi",
                 "effective_external_root_count", "resolved_lineage_coverage", "external_ancestry_coverage"):
        assert metrics[name]["value"] is None and metrics[name]["status"] == "unavailable"
        assert "LINEAGE_RESOURCE_LIMIT_EXCEEDED" in metrics[name]["reason_codes"]
    assert _bounds(payload) == (None, None, None)
    usage = facts["resource_usage"]["value"]
    assert usage["exhausted_limit"] == "max_root_memberships"
    assert usage["stored_root_membership_count"] == 1 and usage["attempted_value"] == 2
    assert result.records is None
    assert any(item["code"] == "E_LINEAGE_RESOURCE_LIMIT_EXCEEDED" for item in payload["errors"])


def test_graph_admission_failure_never_claims_an_acyclic_completed_graph(tmp_path):
    bundle = _validation(tmp_path, {"v1::root": [], "v2::child": ["root"]}, grounding={"v1::root": "yes"})
    with pytest.raises(LineageResourceLimitError) as caught:
        analyze_lineage(bundle, target_dataset_version="v2", limits=LineageLimits(max_nodes=1))
    diagnostic = ValidationMessage(caught.value.code.value, ValidationSeverity.ERROR, caught.value.safe_message)
    payload = _checked(assemble_report(bundle, run=_run(),
        family_errors=(FamilyFailure(CapabilityKey.LINEAGE, (diagnostic,)),)))
    assert payload["capabilities"]["lineage"]["execution_status"] == "failed"
    facts = payload["observed_facts"]["lineage"]
    assert facts["cycle_status"]["value"] is None
    assert "cycle_analysis" not in facts and "graph_scope" not in facts
    assert "resource_usage" not in facts
    assert any(item["code"] == "E_LINEAGE_RESOURCE_LIMIT_EXCEEDED" for item in payload["errors"])


def test_detail_caps_preserve_full_root_metrics_partition_and_cycle_counts(tmp_path):
    declarations = {f"v2::root{i:03d}": [] for i in range(105)}
    grounding = {key: "yes" for key in declarations}
    declarations.update({f"v2::cycle{i:03d}": [f"cycle{i:03d}"] for i in range(101)})
    payload = _checked(_report(_validation(tmp_path, declarations, grounding=grounding))[0])
    facts, metrics = payload["observed_facts"]["lineage"], payload["derived_metrics"]["lineage"]
    cycles = facts["cycle_analysis"]["value"]
    collections = ((metrics["top_shared_ancestors"]["value"], 105),
                   (facts["unresolved_record_details"]["value"], 101),
                   (cycles["components"], 101), (cycles["cycle_member_record_keys"], 101),
                   (cycles["affected_record_keys"], 101))
    for detail, total in collections:
        assert detail["limit"] == detail["returned_count"] == len(detail["items"]) == 100
        assert detail["total_count"] == total and detail["omitted_count"] == total - 100
        assert detail["detail_status"] == "truncated" and detail["omission_reasons"] == ["diagnostic_limit"]
    assert cycles["cycle_count"] == cycles["cycle_member_count"] == cycles["affected_record_count"] == 101
    assert metrics["distinct_external_root_count"]["value"] == 105
    assert metrics["ancestry_concentration_hhi"]["value"] == pytest.approx(1 / 105)
    assert metrics["effective_external_root_count"]["value"] == pytest.approx(105)
    assert metrics["grounded_record_count"]["value"] == 105
    assert metrics["unresolved_record_count"]["value"] == 101
    assert _bounds(payload) == (0, 101 / 206, 101 / 206)


@pytest.mark.parametrize("size", [64, 65])
def test_cycle_witness_limit_preserves_truthful_component_observation(tmp_path, size):
    declarations = {f"v2::n{i:03d}": [f"n{(i + 1) % size:03d}"] for i in range(size)}
    payload = _checked(_report(_validation(tmp_path, declarations))[0])
    cycle = payload["observed_facts"]["lineage"]["cycle_analysis"]["value"]
    assert cycle["cycle_count"] == 1 and cycle["cycle_member_count"] == size
    component = cycle["components"]["items"][0]
    assert component["component_index"] == 1 and component["member_count"] == size
    if size == 64:
        witness = component["witness_record_keys"]
        assert component["witness_edge_count"] == 64 and len(witness) == 65
        assert witness[0] == witness[-1] and component["witness_reason"] is None
        for parent, child in zip(witness, witness[1:]):
            assert parent["record_id"] in declarations["v2::" + child["record_id"]]
    else:
        assert component["witness_record_keys"] is None and component["witness_edge_count"] is None
        assert component["witness_reason"] == "diagnostic_limit"


def test_foreign_lineage_and_derived_handoffs_cannot_be_attached_to_another_bundle(tmp_path):
    a = _validation(tmp_path / "a", {"v2::a": []}, grounding={"v2::a": "yes"})
    b = _validation(tmp_path / "b", {"v2::b": []}, grounding={"v2::b": "yes"})
    first, second = (analyze_lineage(bundle, target_dataset_version="v2") for bundle in (a, b))
    for kwargs in ({"lineage": second},
                   {"lineage": first, "lineage_bounds": lineage_closure_exposure(second)},
                   {"lineage": first, "shared_ancestry": shared_ancestry_dependence(second)},
                   {"lineage_bounds": lineage_closure_exposure(first)},
                   {"shared_ancestry": shared_ancestry_dependence(first)}):
        with pytest.raises(ReportAssemblyError):
            assemble_report(a, run=_run(), **kwargs)


@pytest.mark.parametrize("change", ["grounding", "parent_declaration", "content"])
def test_handoff_binding_checks_relevant_evidence_even_when_identities_are_unchanged(tmp_path, change):
    declarations = {"v1::root": [], "v2::child": ["root"]}
    grounding = {"v1::root": "yes"}
    original = _validation(tmp_path / "original", declarations, grounding=grounding)
    result = analyze_lineage(original, target_dataset_version="v2")
    if change == "grounding":
        grounding = {"v1::root": "no"}
    elif change == "parent_declaration":
        declarations = {"v1::root": [], "v2::child": []}
    modified = _validation(tmp_path / "modified", declarations, grounding=grounding,
                           content="A different content payload, without altered lineage evidence.")
    assert {row.record_key for row in original.records} == {row.record_key for row in modified.records}
    if change == "content":
        payload = _checked(assemble_report(modified, run=_run(), lineage=result))
        assert payload["derived_metrics"]["lineage"]["grounded_record_count"]["value"] == 1
    else:
        with pytest.raises(ReportAssemblyError):
            assemble_report(modified, run=_run(), lineage=result)


def test_assembly_and_rendering_never_recalculate_supplied_lineage(tmp_path, monkeypatch):
    from recursive_integrity_toolkit.io import validation
    from recursive_integrity_toolkit.lineage import graph, cycles, ancestry
    from recursive_integrity_toolkit.metrics import bounds
    from recursive_integrity_toolkit.reports import assembly

    bundle = _validation(tmp_path, {"v1::root": [], "v2::a": ["root"], "v2::b": ["root"]},
                         grounding={"v1::root": "yes"})
    result = analyze_lineage(bundle, target_dataset_version="v2")
    interval, proxy = lineage_closure_exposure(result), shared_ancestry_dependence(result)
    forbidden_calls = [(graph, "build_lineage_graph"), (cycles, "analyze_cycles"),
        (ancestry, "analyze_lineage"), (ancestry, "_root_metrics"),
        (ancestry, "shared_ancestry_dependence"), (bounds, "lineage_closure_exposure"),
        (validation, "validate_bundle"), (validation, "resolve_parent_batch"),
        (validation, "resolve_parent_references"), (validation, "validate_generation_declarations")]
    def forbidden(*args, **kwargs):
        raise AssertionError("report adapter recalculated lineage or loaded input")
    for module, name in forbidden_calls:
        original = getattr(module, name)
        for alias, value in vars(assembly).copy().items():
            if value is original:
                monkeypatch.setattr(assembly, alias, forbidden)
        monkeypatch.setattr(module, name, forbidden)
    payload = _checked(assembly.assemble_report(bundle, run=_run(), lineage=result,
        lineage_bounds=interval, shared_ancestry=proxy))
    view = privacy_view(CanonicalReport.from_dict(payload))
    assert json.loads(render_json(view)) == view.to_dict()
    assert "shared_ancestry_dependence" in render_markdown(view)


def test_input_validation_remains_input_only_with_lineage_reporting_available(tmp_path, monkeypatch):
    from recursive_integrity_toolkit.lineage import graph, cycles, ancestry
    def forbidden(*args, **kwargs):
        raise AssertionError("input validation started lineage analysis")
    for module, name in ((graph, "build_lineage_graph"), (cycles, "analyze_cycles"), (ancestry, "analyze_lineage")):
        monkeypatch.setattr(module, name, forbidden)
    bundle = _validation(tmp_path, {"v2::anchor": []}, grounding={"v2::anchor": "yes"})
    assert len(bundle.records) == 1


def test_json_and_markdown_display_the_same_lineage_values_and_evidence():
    bundle, provenance, direct = _hero()
    report, _ = _report(bundle, provenance=provenance, closure=direct)
    view = privacy_view(report)
    payload = json.loads(render_json(view))
    assert payload == view.to_dict()
    markdown = render_markdown(view)
    assert len([line for line in markdown.splitlines() if line.startswith("## ")]) == 12
    blocks = markdown.split("### Analytical result\n\n")
    for name in ("grounded_record_count", "closed_record_count", "unresolved_record_count",
                 "distinct_external_root_count", "ancestry_concentration_hhi", "effective_external_root_count"):
        marker = '`["derived_metrics"]["lineage"]["' + name + '"]`\n'
        block = next(block for block in blocks if block.startswith(marker))
        field = payload["derived_metrics"]["lineage"][name]
        assert "Value: " + repr(field["value"]) + "." in block
        assert "Status: " + json.dumps(field["status"]).join(("`", "`")) in block
        assert json.dumps(field["evidence_class"]).join(("`", "`")) in block
    assert '- `"lineage"` (ratio): 0.0 to 0.0; interval width: 0.0.' in markdown
    assert '- `"direct"` (ratio): 0.5 to 0.5; interval width: 0.0.' in markdown


@pytest.mark.parametrize("mutation", ["detail_arithmetic", "root_denominator", "partition_count",
    "scope_context_count", "coverage", "unavailable_with_value", "capability_mirror",
    "unresolved_row_payload", "root_row_missing_identity"])
def test_report_validation_rejects_inconsistent_or_untyped_lineage_wire(mutation):
    bundle, _, _ = _hero()
    payload = deepcopy(_report(bundle)[0].to_dict())
    metrics, facts = payload["derived_metrics"]["lineage"], payload["observed_facts"]["lineage"]
    if mutation == "detail_arithmetic":
        metrics["top_shared_ancestors"]["value"]["omitted_count"] = 1
    elif mutation == "root_denominator":
        metrics["top_shared_ancestors"]["value"]["items"][0]["incidence_denominator"] = 16
    elif mutation == "partition_count":
        metrics["closed_record_count"]["value"] = 1
    elif mutation == "scope_context_count":
        facts["graph_scope"]["value"]["context_record_count"] = 0
    elif mutation == "coverage":
        metrics["external_ancestry_coverage"]["value"] = 0.5
    elif mutation == "unavailable_with_value":
        metrics["ancestry_concentration_hhi"]["status"] = "unavailable"
    elif mutation == "capability_mirror":
        payload["observability"]["capabilities"]["lineage"]["execution_status"] = "not_requested"
    elif mutation == "unresolved_row_payload":
        facts["unresolved_record_details"]["value"]["items"] = [{"record_key": {"dataset_version": "v2", "record_id": "v2_01"},
            "reason_codes": ["UNKNOWN_GROUNDING"], "raw_content": "forbidden extra input"}]
    else:
        del metrics["top_shared_ancestors"]["value"]["items"][0]["record_key"]
    with pytest.raises(ReportValidationError):
        validate_report(payload)
