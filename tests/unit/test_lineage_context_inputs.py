"""Direct input and scope boundaries for dedicated lineage context records."""

from dataclasses import replace
import json
import os

import pytest

from recursive_integrity_toolkit.errors import CanonicalValidationError, ErrorCode, IngestionError
from recursive_integrity_toolkit.io.loaders import load_table
from recursive_integrity_toolkit.io.normalization import normalize_table
from recursive_integrity_toolkit.io.validation import validate_bundle
from recursive_integrity_toolkit.lineage.graph import build_lineage_graph
from recursive_integrity_toolkit.models import AuditBundle, FileRole, InputSource, RecordKey


def _records(path, rows):
    path.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")
    return path


def _bundle(tmp_path, declarations):
    sources, provenance = [], []
    for index, (role, version, identity) in enumerate(declarations):
        fields = {"dataset_version": version, "record_id": identity}
        path = _records(tmp_path / f"records-{index}.jsonl", [{**fields, "content": "private content"}])
        sources.append(InputSource(role, path))
        provenance.append({**fields, "source_type": "human", "provenance_confidence": "confirmed",
                           "external_grounding": "yes", "parent_ids": []})
    sources.append(InputSource(FileRole.PROVENANCE_MANIFEST,
                               _records(tmp_path / "provenance.jsonl", provenance)))
    return AuditBundle(tuple(sources))


@pytest.mark.parametrize("file_format", ("csv", "jsonl") + (("parquet",) if os.environ.get("RIT_TEST_PARQUET") == "1" else ()))
def test_context_table_uses_existing_local_parsers_and_normalizer(tmp_path, file_format):
    path = tmp_path / f"context.{file_format}"
    row = {"dataset_version": "v1", "record_id": "a", "content": "private content"}
    if file_format == "csv":
        path.write_text("dataset_version,record_id,content\nv1,a,private content\n", encoding="utf-8")
    elif file_format == "jsonl":
        _records(path, [row])
    else:
        import pyarrow as arrow
        import pyarrow.parquet as parquet
        parquet.write_table(arrow.Table.from_pylist([row]), path)
    loaded = load_table(InputSource(FileRole.LINEAGE_CONTEXT, path))
    normalized = normalize_table(loaded)
    assert loaded.inventory.role is FileRole.LINEAGE_CONTEXT
    assert normalized[0].kind == "records"
    assert normalized[0].record_key == RecordKey("v1", "a")
    assert normalized[0].location.file_role is FileRole.LINEAGE_CONTEXT


def test_repeated_context_files_join_all_versions_without_graph_execution(tmp_path, monkeypatch):
    from recursive_integrity_toolkit.lineage import ancestry, cycles, graph

    def forbidden(*args, **kwargs):
        pytest.fail("input validation invoked lineage analysis")

    for module, function in ((ancestry, "analyze_lineage"), (cycles, "analyze_cycles"),
                             (graph, "build_lineage_graph")):
        monkeypatch.setattr(module, function, forbidden)
    declarations = ((FileRole.RECORDS_PRIMARY, "v3", "target"),
                    (FileRole.RECORDS_COMPARE, "v2", "comparison"),
                    (FileRole.LINEAGE_CONTEXT, "v1", "a"),
                    (FileRole.LINEAGE_CONTEXT, "v1", "b"))
    result = validate_bundle(_bundle(tmp_path, declarations),
                             configuration={"version_order": ["v1", "v2", "v3"], "lineage": True})
    assert not result.has_errors
    assert len(result.records) == len(result.provenance) == 4
    assert len(result.parent_validation.assessments) == 4
    assert result.provenance_join.provenance_row_coverage.numerator == 4
    assert sum(row.location.file_role is FileRole.LINEAGE_CONTEXT for row in result.records) == 2


@pytest.mark.parametrize("other_role", (FileRole.RECORDS_PRIMARY, FileRole.RECORDS_COMPARE))
def test_context_version_cannot_overlap_selected_roles(tmp_path, other_role):
    declarations = [(FileRole.RECORDS_PRIMARY, "v3", "target")]
    overlap_version = "v3"
    if other_role is FileRole.RECORDS_COMPARE:
        declarations.append((other_role, "v2", "comparison"))
        overlap_version = "v2"
    declarations.append((FileRole.LINEAGE_CONTEXT, overlap_version, "different-id"))
    with pytest.raises(CanonicalValidationError) as caught:
        validate_bundle(_bundle(tmp_path, declarations))
    assert caught.value.code is ErrorCode.CONFIG_INVALID
    assert caught.value.file_role == FileRole.LINEAGE_CONTEXT.value


@pytest.mark.parametrize("other_role", (FileRole.RECORDS_PRIMARY, FileRole.RECORDS_COMPARE,
                                        FileRole.LINEAGE_CONTEXT))
def test_duplicate_context_identity_is_rejected_before_join(tmp_path, other_role):
    declarations = [(FileRole.RECORDS_PRIMARY, "v3", "target")]
    version, identity = "v3", "target"
    if other_role is not FileRole.RECORDS_PRIMARY:
        declarations.append((other_role, "v1", "duplicate"))
        version, identity = "v1", "duplicate"
    declarations.append((FileRole.LINEAGE_CONTEXT, version, identity))
    with pytest.raises(CanonicalValidationError) as caught:
        validate_bundle(_bundle(tmp_path, declarations))
    assert caught.value.code is ErrorCode.RECORD_DUPLICATE_ID


def test_context_graph_preserves_target_and_existing_multiple_comparison_inputs(tmp_path):
    declarations = ((FileRole.RECORDS_PRIMARY, "v3", "target"),
                    (FileRole.RECORDS_COMPARE, "v2", "comparison-two"),
                    (FileRole.RECORDS_COMPARE, "v1", "comparison-one"),
                    (FileRole.LINEAGE_CONTEXT, "v0", "root"))
    bundle = validate_bundle(_bundle(tmp_path, declarations),
                             configuration={"version_order": ["v0", "v1", "v2", "v3"]})
    graph = build_lineage_graph(bundle, target_dataset_version="v3")
    assert graph.scope.target_record_keys == (RecordKey("v3", "target"),)
    assert (graph.scope.target_record_count, graph.scope.loaded_record_count,
            graph.scope.context_record_count) == (1, 4, 3)
    for version in (None, "v0", "v1", "v2"):
        with pytest.raises(CanonicalValidationError) as caught:
            build_lineage_graph(bundle, target_dataset_version=version)
        assert caught.value.code is ErrorCode.CONFIG_INVALID


def test_context_only_typed_graph_can_have_empty_target_but_cannot_select_context(tmp_path):
    bundle = validate_bundle(_bundle(tmp_path, ((FileRole.RECORDS_PRIMARY, "v1", "root"),)))
    row = bundle.records[0]
    context_row = replace(row, location=replace(row.location, file_role=FileRole.LINEAGE_CONTEXT))
    context_only = replace(bundle, records=(context_row,))
    graph = build_lineage_graph(context_only, target_dataset_version=None)
    assert graph.scope.target_record_count == 0
    assert graph.scope.loaded_record_count == graph.scope.context_record_count == 1
    with pytest.raises(CanonicalValidationError) as caught:
        build_lineage_graph(context_only, target_dataset_version="v1")
    assert caught.value.code is ErrorCode.CONFIG_INVALID


def test_empty_context_table_preserves_existing_records_admission_rule(tmp_path):
    path = tmp_path / "empty.csv"
    path.write_text("dataset_version,record_id,content\n", encoding="utf-8")
    with pytest.raises(IngestionError) as caught:
        load_table(InputSource(FileRole.LINEAGE_CONTEXT, path))
    assert caught.value.code is ErrorCode.EMPTY_DATASET


def _admission_report(tmp_path, exhausted, *, mode="standard", record_ids="preserve"):
    from recursive_integrity_toolkit.config import resolve_phase4_options
    from recursive_integrity_toolkit.errors import LineageResourceLimitError
    from recursive_integrity_toolkit.lineage.ancestry import analyze_lineage
    from recursive_integrity_toolkit.lineage.graph import LineageLimits
    from recursive_integrity_toolkit.models import CapabilityKey, ValidationMessage, ValidationSeverity
    from recursive_integrity_toolkit.reports.assembly import (
        FamilyFailure, assemble_report, build_run_metadata, privacy_view,
    )

    declarations = ((FileRole.RECORDS_PRIMARY, "v2", "target"),
                    (FileRole.LINEAGE_CONTEXT, "v1", "a"),
                    (FileRole.LINEAGE_CONTEXT, "v1", "b"))
    sources = _bundle(tmp_path, declarations)
    provenance_path = tmp_path / "provenance.jsonl"
    provenance = [json.loads(line) for line in provenance_path.read_text().splitlines()]
    provenance[0]["parent_ids"] = ["v1::a", "v1::b"]
    _records(provenance_path, provenance)
    bundle = validate_bundle(sources, configuration={"version_order": ["v1", "v2"]})
    with pytest.raises(LineageResourceLimitError) as caught:
        analyze_lineage(bundle, target_dataset_version="v2", limits=LineageLimits(**{exhausted: 1}))
    failure = FamilyFailure(CapabilityKey.LINEAGE,
        (ValidationMessage(caught.value.code.value, ValidationSeverity.ERROR, caught.value.safe_message),),
        lineage_resource_usage=caught.value.resource_usage)
    cli = {"lineage": True}
    if mode == "redacted":
        cli.update(redacted=True, record_ids=record_ids)
    options = resolve_phase4_options(cli=cli)
    report = assemble_report(bundle, run=build_run_metadata(options=options, run_id="admission-case"),
                             family_errors=(failure,))
    return privacy_view(report, mode=mode, record_id_mode=record_ids).to_dict(), failure


@pytest.mark.parametrize("exhausted", ("max_nodes", "max_edges"))
@pytest.mark.parametrize("mode,record_ids", (("standard", "preserve"), ("redacted", "hash"),
                                            ("redacted", "omit")))
def test_admission_failure_keeps_exact_counters_in_each_privacy_view(tmp_path, exhausted, mode, record_ids):
    from jsonschema import Draft202012Validator
    from recursive_integrity_toolkit.result import report_schema, validate_report

    payload, _ = _admission_report(tmp_path, exhausted, mode=mode, record_ids=record_ids)
    Draft202012Validator(report_schema()).validate(payload)
    validate_report(payload)
    lineage = payload["observed_facts"]["lineage"]
    assert payload["capabilities"]["lineage"]["execution_status"] == "failed"
    assert lineage["cycle_status"]["value"] is None
    assert "graph_scope" not in lineage and "cycle_analysis" not in lineage
    assert lineage["resource_usage"]["scope"] == payload["inputs"]["scope"]
    usage = lineage["resource_usage"]["value"]
    assert usage["exhausted_limit"] == exhausted
    assert usage["limits"][exhausted] == 1 and usage["attempted_value"] == 2
    assert usage["stored_root_membership_count"] == usage["root_union_visit_count"] == 0
    assert usage["admitted_node_count"] == (1 if exhausted == "max_nodes" else 3)
    assert usage["admitted_edge_count"] == (0 if exhausted == "max_nodes" else 1)
    notes = payload["capabilities"]["lineage"]["notes"]
    assert not any("remain deferred" in note or "no roots or ancestors are traced" in note for note in notes)


@pytest.mark.parametrize("invalid", ("other_family", "wrong_diagnostic", "completed", "root_stage", "wrong_type"))
def test_admission_failure_rejects_inconsistent_typed_handoff(tmp_path, invalid):
    from recursive_integrity_toolkit.lineage.graph import LineageLimits, LineageResourceUsage
    from recursive_integrity_toolkit.models import CapabilityKey, ValidationMessage, ValidationSeverity
    from recursive_integrity_toolkit.reports.assembly import ReportAssemblyError

    _, failure = _admission_report(tmp_path, "max_nodes")
    changes = {
        "other_family": {"capability": CapabilityKey.PROVENANCE},
        "wrong_diagnostic": {"messages": (ValidationMessage("E_PARENT_FORMAT", ValidationSeverity.ERROR, "Invalid parent."),)},
        "completed": {"lineage_resource_usage": LineageResourceUsage(1, 0, 0, 0, LineageLimits())},
        "root_stage": {"lineage_resource_usage": LineageResourceUsage(1, 0, 1, 0,
            LineageLimits(max_root_memberships=1), "max_root_memberships", 2)},
        "wrong_type": {"lineage_resource_usage": {}},
    }
    with pytest.raises(ReportAssemblyError):
        replace(failure, **changes[invalid])


@pytest.mark.parametrize("mutation", ("attempt", "unfilled_limit", "later_work", "invented_cycle", "missing_error"))
def test_redacted_admission_wire_rejects_false_stage_or_counter_claims(tmp_path, mutation):
    from recursive_integrity_toolkit.result import ReportValidationError, validate_report

    payload, _ = _admission_report(tmp_path, "max_nodes", mode="redacted", record_ids="omit")
    lineage = payload["observed_facts"]["lineage"]
    usage = lineage["resource_usage"]["value"]
    if mutation == "attempt":
        usage["attempted_value"] = 3
    elif mutation == "unfilled_limit":
        usage["admitted_node_count"] = 0
    elif mutation == "later_work":
        usage["root_union_visit_count"] = 1
    elif mutation == "invented_cycle":
        lineage["cycle_status"]["value"] = "acyclic"
        lineage["cycle_status"]["status"] = "available"
        lineage["cycle_status"]["reason_codes"] = []
    else:
        payload["errors"] = []
    with pytest.raises(ReportValidationError):
        validate_report(payload)
