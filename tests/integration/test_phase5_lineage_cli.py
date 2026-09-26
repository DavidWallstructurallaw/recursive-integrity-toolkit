"""Explicit lineage orchestration, target scope and local input boundaries."""

from __future__ import annotations

import csv
import importlib
import inspect
import json
import os
from pathlib import Path
import socket

import pytest
from jsonschema import Draft202012Validator


def _write(path, rows):
    if path.suffix == ".csv":
        with path.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
    elif path.suffix == ".parquet":
        import pyarrow as arrow
        import pyarrow.parquet as parquet
        parquet.write_table(arrow.Table.from_pylist(rows), path)
    else:
        path.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")


def _inputs(directory, *, context_format="jsonl", content=False):
    directory.mkdir(parents=True, exist_ok=True)
    rows = [
        {"dataset_version": "v1", "record_id": "root1", "content": "PRIVATE_CONTENT_A", "topic": "A"},
        {"dataset_version": "v2", "record_id": "root2", "content": "PRIVATE_CONTENT_B", "topic": "B"},
        {"dataset_version": "v3", "record_id": "t1", "content": "PRIVATE_CONTENT_A", "topic": "A"},
        {"dataset_version": "v3", "record_id": "t2", "content": "PRIVATE_CONTENT_A", "topic": "A"},
    ]
    primary = directory / "primary.jsonl"
    contexts = [directory / f"context{i}.{context_format}" for i in (1, 2)]
    _write(primary, rows[2:])
    for path, row in zip(contexts, rows[:2]):
        _write(path, [row])
    provenance = directory / "provenance.jsonl"
    manifests = []
    for index, row in enumerate(rows):
        manifests.append({"dataset_version": row["dataset_version"], "record_id": row["record_id"],
            "source_type": "human" if index < 2 else "synthetic", "provenance_confidence": "confirmed",
            "external_grounding": "yes" if index < 2 else "no", "transformation": "generate",
            "parent_ids": [] if index < 2 else [f"v{index - 1}::root{index - 1}"]})
    _write(provenance, manifests)
    config = directory / "config.json"
    representation = {"name": "exact" if content else "topic", "source": "content_hash" if content else "topic_field",
                      "field": "content" if content else "topic", "version": "1", "missing_value_policy": "error"}
    if content:
        representation["normalization_profile"] = "exact_utf8_v1"
    config.write_text(json.dumps({"representation": representation, "version_order": ["v1", "v2", "v3"]}), encoding="utf-8")
    return ["--records", str(primary), "--provenance", str(provenance), "--config", str(config)], primary, contexts, provenance, config


def _context_args(contexts):
    return [value for path in contexts for value in ("--lineage-records", str(path))]


def _invoke(args, out, capsys, *, command="audit"):
    from recursive_integrity_toolkit.cli import main
    code = main([command, *args, "--out", str(out)])
    streams = capsys.readouterr()
    directory = out / "reports" if command == "example" else out
    report = json.loads((directory / "report.json").read_text(encoding="utf-8")) if (directory / "report.json").exists() else None
    markdown = (directory / "report.md").read_text(encoding="utf-8") if (directory / "report.md").exists() else ""
    if report is not None:
        from recursive_integrity_toolkit.result import validate_report
        validate_report(report)
        assert report["run"]["report_schema_version"] == "1.1"
        assert report["capabilities"] == report["observability"].get("capabilities", {})
        assert report["run"]["network_call_count"] == 0
        assert markdown.startswith("# Recursive Integrity Audit Report\n")
    assert "PRIVATE_CONTENT_" not in json.dumps(report) + markdown + streams.out + streams.err
    return code, report, markdown, streams


def _bounds(report, family):
    value = report["derived_metrics"]["closure_exposure"][family]
    return tuple(value[name]["value"] for name in ("lower_bound", "upper_bound", "interval_width"))


def _assert_primary_metrics(report, *, content=False):
    metrics = report["derived_metrics"]
    assert set(metrics["support"]["by_version"]) == {"v3"}
    support = metrics["support"]["by_version"]["v3"]["support_size"]
    assert support["value"] == 1 and support["scope"]["record_count"] == 2
    assert report["observed_facts"]["provenance"]["analyzed_record_count"]["value"] == 2
    shares = metrics["provenance"]["source_type_shares"]
    assert shares["value"]["synthetic"] == 1.0 and shares["value"]["human"] == 0.0
    assert shares["denominator"] == 2
    assert _bounds(report, "direct") == (1.0, 1.0, 0.0)
    if content:
        duplicates = report["observed_facts"]["content"]["duplicate_record_count"]
        assert duplicates["value"] == 1 and duplicates["scope"]["record_count"] == 2


@pytest.mark.parametrize("context_format", ["csv", "jsonl"] + (["parquet"] if os.environ.get("RIT_TEST_PARQUET") == "1" else []))
def test_context_loaders_and_repeated_inputs_keep_primary_only_denominators(tmp_path, capsys, repo_root, context_format):
    args, primary, contexts, provenance, config = _inputs(tmp_path, context_format=context_format, content=True)
    before = {path: path.read_bytes() for path in (primary, *contexts, provenance, config)}
    code, report, markdown, streams = _invoke(args + ["--lineage"] + _context_args(contexts), tmp_path / "out", capsys)
    assert code == 0 and report["run"]["run_status"] == "complete"
    _assert_primary_metrics(report, content=True)
    scope = report["observed_facts"]["lineage"]["graph_scope"]["value"]
    assert scope == {"target_dataset_version": "v3", "target_record_count": 2, "loaded_record_count": 4,
                     "context_record_count": 2, "loaded_dataset_versions": ["v1", "v2", "v3"]}
    assert report["derived_metrics"]["lineage"]["grounded_record_count"]["value"] == 2
    assert report["derived_metrics"]["lineage"]["ancestry_concentration_hhi"]["value"] == 0.5
    assert _bounds(report, "lineage") == (0.0, 0.0, 0.0)
    assert report["capabilities"]["lineage"]["execution_status"] == "completed"
    assert report["capabilities"]["dataset_longitudinal"]["execution_status"] == "not_requested"
    assert "comparison_details" not in report["derived_metrics"]["support"] and report["simulations"] == {}
    assert sum(item["role"] == "lineage_context" for item in report["inputs"]["artifacts"]) == 2
    Draft202012Validator(json.loads((repo_root / "schemas/report.schema.json").read_text())).validate(report)
    assert all(path.read_bytes() == data for path, data in before.items())


def test_plain_audit_does_not_dispatch_graph_even_when_provenance_has_parents(tmp_path, capsys, monkeypatch):
    args, primary, contexts, provenance, config = _inputs(tmp_path)
    _write(provenance, [json.loads(line) for line in provenance.read_text().splitlines()
                        if json.loads(line)["dataset_version"] == "v3"])
    graph = importlib.import_module("recursive_integrity_toolkit.lineage.graph")
    ancestry = importlib.import_module("recursive_integrity_toolkit.lineage.ancestry")
    def denied(*args, **kwargs):
        pytest.fail("plain audit dispatched graph work")
    monkeypatch.setattr(graph, "build_lineage_graph", denied)
    monkeypatch.setattr(ancestry, "analyze_lineage", denied)
    code, report, _, _ = _invoke(args, tmp_path / "out", capsys)
    assert code == 0
    _assert_primary_metrics(report)
    assert report["capabilities"]["lineage"]["execution_status"] == "not_requested"
    assert report["observed_facts"]["lineage"]["cycle_status"]["value"] is None


def test_explicit_comparison_can_supply_ancestors_without_context_entering_pair(tmp_path, capsys):
    args, primary, contexts, provenance, config = _inputs(tmp_path)
    code, report, _, _ = _invoke(args + ["--lineage", "--compare", str(contexts[1]),
        "--state-semantics", "literal shared topics"] + _context_args(contexts[:1]), tmp_path / "out", capsys)
    assert code == 0
    assert set(report["derived_metrics"]["support"]["by_version"]) == {"v2", "v3"}
    retention = report["derived_metrics"]["support"]["support_retention_ratio"]
    assert retention["value"] == 0.0 and retention["scope"]["dataset_versions"] == ["v2", "v3"]
    assert report["capabilities"]["dataset_longitudinal"]["execution_status"] == "partial"
    assert report["capabilities"]["dataset_longitudinal"]["execution_scope"] == ["supplied_explicit_pair_support_and_diversity"]
    assert report["capabilities"]["lineage"]["execution_status"] == "completed"
    assert report["observed_facts"]["provenance"]["analyzed_record_count"]["value"] == 2
    assert report["observed_facts"]["lineage"]["graph_scope"]["value"]["target_record_count"] == 2
    assert _bounds(report, "direct") == (1.0, 1.0, 0.0)
    assert _bounds(report, "lineage") == (0.0, 0.0, 0.0)


@pytest.mark.parametrize("configured", [False, True])
def test_context_requires_explicit_audit_opt_in(tmp_path, capsys, configured):
    args, primary, contexts, provenance, config = _inputs(tmp_path)
    if configured:
        raw = json.loads(config.read_text()); raw["inputs"] = {"lineage_context": [str(path) for path in contexts]}
        config.write_text(json.dumps(raw))
    else:
        args += _context_args(contexts)
    code, report, _, streams = _invoke(args, tmp_path / "out", capsys)
    assert code == 2
    assert "E_CONFIG_INVALID" in streams.err
    assert report is None or report["derived_metrics"] == {}


def test_config_and_cli_context_paths_keep_their_own_relative_bases(tmp_path, capsys, monkeypatch):
    directory = tmp_path / "settings"
    args, primary, contexts, provenance, config = _inputs(directory)
    raw = json.loads(config.read_text())
    raw.update(lineage=True, inputs={"lineage_context": contexts[0].name})
    config.write_text(json.dumps(raw))
    cli_context = tmp_path / "cli-context.jsonl"
    cli_context.write_bytes(contexts[1].read_bytes())
    monkeypatch.chdir(tmp_path)
    code, report, _, _ = _invoke(args + ["--lineage-records", cli_context.name], tmp_path / "out", capsys)
    assert code == 0
    _assert_primary_metrics(report)
    assert report["observed_facts"]["lineage"]["graph_scope"]["value"]["loaded_record_count"] == 4


@pytest.mark.parametrize("case", ["primary_multiversion", "primary_overlap", "comparison_overlap", "duplicate_context", "empty_primary"])
def test_invalid_role_scope_cannot_produce_completed_lineage(tmp_path, capsys, case):
    args, primary, contexts, provenance, config = _inputs(tmp_path)
    extra = ["--lineage"] + _context_args(contexts)
    if case == "primary_multiversion":
        rows = [json.loads(line) for line in primary.read_text().splitlines()]
        rows[0]["dataset_version"] = "v4"
        _write(primary, rows)
        manifests = [json.loads(line) for line in provenance.read_text().splitlines()]
        manifests[2]["dataset_version"] = "v4"
        _write(provenance, manifests)
        raw = json.loads(config.read_text()); raw["version_order"].append("v4")
        config.write_text(json.dumps(raw))
    elif case == "primary_overlap":
        _write(contexts[0], [{"dataset_version": "v3", "record_id": "separate", "content": "separate", "topic": "C"}])
    elif case == "comparison_overlap":
        comparison = tmp_path / "compare.jsonl"
        _write(comparison, [{"dataset_version": "v2", "record_id": "separate", "content": "separate", "topic": "C"}])
        extra += ["--compare", str(comparison), "--state-semantics", "literal shared topics"]
    elif case == "duplicate_context":
        extra += _context_args(contexts[:1])
    else:
        primary.write_bytes(b"")
    code, report, _, _ = _invoke(args + extra, tmp_path / "out", capsys)
    assert code != 0 and report is not None and report["errors"]
    assert report["capabilities"].get("lineage", {}).get("execution_status") != "completed"
    if case == "empty_primary":
        assert report["observed_facts"] == report["derived_metrics"] == {}


def test_validate_context_remains_input_only(tmp_path, capsys, monkeypatch):
    from recursive_integrity_toolkit import cli
    args, primary, contexts, provenance, config = _inputs(tmp_path)
    names = ("metrics.diversity", "metrics.provenance", "metrics.bounds", "metrics.duplicates", "metrics.tail",
             "metrics.resampling", "representations.base", "representations.field", "representations.content_hash",
             "representations.compatibility", "lineage.graph", "lineage.cycles", "lineage.ancestry")
    modules = [importlib.import_module("recursive_integrity_toolkit." + name) for name in names]
    touched = []
    def denied(*args, **kwargs):
        touched.append(True)
        raise AssertionError("validate dispatched calculation")
    for module in modules:
        for name, value in vars(module).copy().items():
            if inspect.isfunction(value) and value.__module__ == module.__name__:
                monkeypatch.setattr(module, name, denied)
    monkeypatch.setattr(cli, "_calculations", denied)
    code, report, _, _ = _invoke(args + _context_args(contexts), tmp_path / "out", capsys, command="validate")
    assert code == 0 and touched == []
    assert report["derived_metrics"] == report["proxy_signals"] == report["simulations"] == {}
    assert report["capabilities"]["lineage"]["execution_status"] == "not_requested"
    assert set(report["observed_facts"]["record_counts"]) == {"v1", "v2", "v3"}


@pytest.mark.parametrize("configured", [False, True])
def test_validate_rejects_lineage_execution_request(tmp_path, capsys, configured):
    args, primary, contexts, provenance, config = _inputs(tmp_path)
    if configured:
        raw = json.loads(config.read_text()); raw["lineage"] = True
        config.write_text(json.dumps(raw))
    else:
        args += ["--lineage"]
    code, report, _, streams = _invoke(args + _context_args(contexts), tmp_path / "out", capsys, command="validate")
    assert code == 2 and "E_CONFIG_INVALID" in streams.err
    assert report is None or report["derived_metrics"] == {}


@pytest.mark.parametrize("case,expected_exit,execution", [
    ("cycle", 3, "partial"), ("missing", 0, "partial"),
    ("nodes", 1, "failed"), ("edges", 1, "failed"), ("roots", 1, "failed"), ("visits", 1, "failed"),
])
def test_partial_and_resource_failures_preserve_independent_primary_values(tmp_path, capsys, case, expected_exit, execution):
    args, primary, contexts, provenance, config = _inputs(tmp_path)
    rows = [json.loads(line) for line in provenance.read_text().splitlines()]
    if case == "cycle":
        rows[2]["parent_ids"] = ["v3::t1"]
    elif case == "missing":
        rows[2]["parent_ids"] = ["v1::missing"]
    else:
        raw = json.loads(config.read_text())
        limit, value = {"nodes": ("max_lineage_nodes", 3), "edges": ("max_lineage_edges", 1),
                        "roots": ("max_lineage_root_memberships", 2),
                        "visits": ("max_lineage_root_union_visits", 1)}[case]
        raw["resource_limits"] = {limit: value}
        config.write_text(json.dumps(raw))
    _write(provenance, rows)
    code, report, _, _ = _invoke(args + ["--lineage"] + _context_args(contexts), tmp_path / "out", capsys)
    assert code == expected_exit
    _assert_primary_metrics(report)
    assert report["capabilities"]["lineage"]["execution_status"] == execution
    expected_run = "complete" if case == "missing" else "failed" if case in ("nodes", "edges") else "partial"
    assert report["run"]["run_status"] == expected_run
    if case in ("cycle", "missing"):
        assert report["derived_metrics"]["lineage"]["unresolved_record_count"]["value"] == 1
        assert _bounds(report, "lineage") == (0.0, 0.5, 0.5)
    else:
        if case in ("nodes", "edges"):
            assert "lineage" not in report["derived_metrics"]["closure_exposure"]
        else:
            assert _bounds(report, "lineage") == (None, None, None)
        assert any(row["code"] == "E_LINEAGE_RESOURCE_LIMIT_EXCEEDED" for row in report["errors"])
        facts = report["observed_facts"]["lineage"]
        usage = facts["resource_usage"]["value"]
        exhausted, admitted_field, admitted, attempted = {
            "nodes": ("max_nodes", "admitted_node_count", 3, 4),
            "edges": ("max_edges", "admitted_edge_count", 1, 2),
            "roots": ("max_root_memberships", "stored_root_membership_count", 2, 3),
            "visits": ("max_root_union_visits", "root_union_visit_count", 1, 2),
        }[case]
        assert usage["exhausted_limit"] == exhausted and usage["attempted_value"] == attempted
        assert usage["limits"][exhausted] == admitted and usage[admitted_field] == admitted
        if case in ("roots", "visits"):
            assert facts["cycle_status"]["value"] == "acyclic"
            assert facts["depth_summary"]["value"]["maximum_resolved_target_depth"] == 1
        else:
            assert facts["cycle_status"]["value"] is None
            assert "graph_scope" not in facts


def test_conflicting_context_chronology_preserves_primary_metrics_without_lineage_claim(tmp_path, capsys):
    args, primary, contexts, provenance, config = _inputs(tmp_path)
    raw = json.loads(config.read_text()); del raw["version_order"]
    config.write_text(json.dumps(raw))
    order = tmp_path / "conflicting-order.json"
    order.write_text(json.dumps({"version_order": ["v1", "v2", "v3"],
                                "version_rank": {"v1": 1, "v2": 0, "v3": 2}}), encoding="utf-8")
    code, report, _, _ = _invoke(args + ["--lineage", "--version-order", str(order)]
        + _context_args(contexts), tmp_path / "out", capsys)
    assert code != 0 and report["errors"]
    assert any(item["code"] == "E_VERSION_ORDER_CONFLICT" for item in report["errors"])
    _assert_primary_metrics(report)
    assert report["capabilities"]["lineage"]["execution_status"] == "failed"
    assert report["observed_facts"]["lineage"]["cycle_status"]["value"] is None
    assert "comparison_details" not in report["derived_metrics"]["support"]
    assert any(item["role"] == "version_order" for item in report["inputs"]["artifacts"])


@pytest.mark.parametrize("record_ids", ["hash", "omit"])
def test_lineage_context_redaction_protects_every_sink_and_never_fetches_sources(tmp_path, capsys, monkeypatch, record_ids):
    directory = tmp_path / "PRIVATE_PATH"
    args, primary, contexts, provenance, config = _inputs(directory)
    for path in (primary, *contexts, provenance):
        rows = [json.loads(line) for line in path.read_text().splitlines()]
        for row in rows:
            row["dataset_version"] = "PRIVATE_VERSION_" + row["dataset_version"]
            row["record_id"] = "PRIVATE_ID_" + row["record_id"]
            if "parent_ids" in row:
                row["parent_ids"] = ["PRIVATE_VERSION_" + ref.replace("::", "::PRIVATE_ID_") for ref in row["parent_ids"]]
                row["source_uri"] = "https://invalid.example/PRIVATE_URI?token=secret"
        _write(path, rows)
    raw = json.loads(config.read_text()); raw["version_order"] = ["PRIVATE_VERSION_" + item for item in raw["version_order"]]
    config.write_text(json.dumps(raw))
    touched = []
    def denied(*args, **kwargs):
        touched.append(True)
        raise AssertionError("network attempted")
    monkeypatch.setattr(socket, "create_connection", denied)
    monkeypatch.setattr(socket.socket, "connect", denied)
    code, report, markdown, streams = _invoke(args + ["--lineage", "--redacted", "--record-ids", record_ids]
        + _context_args(contexts), directory / "PRIVATE_OUTPUT", capsys)
    assert code == 0 and touched == []
    rendered = json.dumps(report) + markdown + streams.out + streams.err
    assert not any(value in rendered for value in ("PRIVATE_PATH", "PRIVATE_VERSION", "PRIVATE_ID", "PRIVATE_URI", "PRIVATE_OUTPUT"))
    roots = report["derived_metrics"]["lineage"]["top_shared_ancestors"]["value"]
    assert roots["total_count"] == 2
    if record_ids == "omit":
        assert roots["items"] is None and roots["detail_status"] == "omitted"
    else:
        assert roots["returned_count"] == 2
        assert all(row["record_key"]["record_id"].startswith("hmac-sha256:") for row in roots["items"])


def test_invalid_context_input_cannot_be_overwritten_by_failure_report(tmp_path, capsys):
    args, primary, contexts, provenance, config = _inputs(tmp_path)
    out = tmp_path / "out"
    out.mkdir()
    collision = out / "report.json"
    collision.write_text("{PRIVATE_MALFORMED_CONTEXT", encoding="utf-8")
    before = collision.read_bytes()
    from recursive_integrity_toolkit.cli import main
    assert main(["audit", *args, "--lineage", "--lineage-records", str(collision), "--out", str(out)]) != 0
    streams = capsys.readouterr()
    assert collision.read_bytes() == before and not (out / "report.md").exists()
    assert "PRIVATE_MALFORMED_CONTEXT" not in streams.out + streams.err


@pytest.mark.parametrize("enabled", [False, True])
def test_literal_hero_has_exact_requested_lineage_and_plain_default(tmp_path, capsys, enabled):
    code, report, _, streams = _invoke(["--lineage"] if enabled else [], tmp_path / "hero", capsys, command="example")
    assert code == 0
    assert report["derived_metrics"]["support"]["by_version"]["v1"]["support_size"]["value"] == 8
    assert report["derived_metrics"]["support"]["by_version"]["v2"]["support_size"]["value"] == 5
    assert _bounds(report, "direct") == (0.5, 0.5, 0.0)
    assert report["capabilities"]["lineage"]["execution_status"] == ("completed" if enabled else "not_requested")
    if enabled:
        lineage = report["derived_metrics"]["lineage"]
        assert lineage["distinct_external_root_count"]["value"] == 5
        assert lineage["ancestry_concentration_hhi"]["value"] == 0.25
        assert lineage["effective_external_root_count"]["value"] == 4.0
        assert lineage["top_shared_ancestors"]["value"]["items"][0]["incidence_share"] == 3 / 8
        assert _bounds(report, "lineage") == (0.0, 0.0, 0.0)
        assert report["proxy_signals"]["shared_ancestry_dependence"]["level"] == "present"
    assert "lineage execution is deferred" not in streams.err
