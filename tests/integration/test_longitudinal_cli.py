"""Step 7 CLI series execution, literal configuration and publication boundaries.

Scientific expectations come from the frozen Phase 6A input fixtures. Optional
Parquet execution is selected explicitly with RIT_TEST_PARQUET=1 and imports
the real Arrow engine; no stand-in loader or silent dependency skip is used.
"""
from copy import deepcopy
import csv
from fractions import Fraction
import importlib
import inspect
import json
import os
from pathlib import Path
import socket
import urllib.request

import pytest


ROOT = Path(__file__).resolve().parents[2]
CASES = json.loads((ROOT / "tests/fixtures/longitudinal/cases.json").read_text())["cases"]
FORMATS = ["csv", "jsonl"] + (["parquet"] if os.environ.get("RIT_TEST_PARQUET") == "1" else [])


@pytest.fixture(autouse=True)
def _no_network(monkeypatch):
    def denied(*args, **kwargs):
        pytest.fail("local longitudinal CLI attempted a network connection")
    monkeypatch.setattr(socket.socket, "connect", denied)
    monkeypatch.setattr(socket.socket, "connect_ex", denied)
    monkeypatch.setattr(socket, "create_connection", denied)
    monkeypatch.setattr(urllib.request, "urlopen", denied)


def _case(name="observed_three_version"):
    return deepcopy(next(case for case in CASES if case["case_id"] == name))


def _write(path, rows):
    if path.suffix == ".csv":
        with path.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows({key: json.dumps(value) if isinstance(value, (list, dict)) else value
                              for key, value in row.items()} for row in rows)
    elif path.suffix == ".parquet":
        import pyarrow as arrow
        import pyarrow.parquet as parquet
        parquet.write_table(arrow.Table.from_pylist(rows), path)
    else:
        path.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")


def _descriptor(raw):
    return {"representation_name": raw["name"], "representation_source": raw["source"],
            "representation_version": raw["version"], "binning_or_mapping_rule": "literal_field_value",
            "field_name": raw["field"], "missing_value_policy": raw["missing_value_policy"],
            "missing_state_id": None, "normalization_profile": None}


def _inputs(directory, name="observed_three_version", *, format="jsonl", per_version=False,
            enable=True, config_inputs=False):
    case = _case(name)
    directory.mkdir(parents=True, exist_ok=True)
    paths = {}
    for index, version in enumerate(case["selected_versions"] + case["context_versions"]):
        path = directory / f"records-{index}.{format}"
        _write(path, [row for row in case["records"] if row["dataset_version"] == version])
        paths[version] = path
    primary = paths[case["selected_versions"][-1]]
    compares = [paths[version] for version in reversed(case["selected_versions"][:-1])]
    contexts = [paths[version] for version in case["context_versions"]]
    provenance = directory / "provenance.jsonl"
    _write(provenance, case["provenance"])
    raw = {"longitudinal": {"enabled": enable}}
    if per_version:
        raw["longitudinal"]["versions"] = [{"dataset_version": version,
            "representation": {key: value for key, value in declaration.items() if key != "state_semantics"},
            "state_semantics": declaration["state_semantics"]}
            for version, declaration in case["representations"].items()]
    else:
        declaration = next(iter(case["representations"].values()))
        raw["representation"] = {key: value for key, value in declaration.items() if key != "state_semantics"}
        raw["longitudinal"]["state_semantics"] = declaration["state_semantics"]
    if name == "directed_many_to_one":
        earlier, later = case["selected_versions"]
        mapping = case["expected_pairs"][0]["mapping"]
        raw["longitudinal"]["mappings"] = [{"earlier_version": earlier, "later_version": later,
            "declaration": {**mapping, "source_representation": _descriptor(case["representations"][earlier]),
                "target_representation": _descriptor(case["representations"][later]),
                "source_state_semantics": case["representations"][earlier]["state_semantics"],
                "target_state_semantics": case["representations"][later]["state_semantics"]}}]
    config = directory / "config.json"
    args = ["--records", str(primary), "--provenance", str(provenance), "--config", str(config)]
    if config_inputs:
        raw["inputs"] = {"records_compare": [path.name for path in compares]}
    else:
        args += [part for path in compares for part in ("--compare", str(path))]
    if case["order_document"] is not None:
        order = directory / "order.json"
        order.write_text(json.dumps(case["order_document"]))
        args += ["--version-order", str(order)]
    if contexts:
        args += ["--lineage"] + [part for path in contexts for part in ("--lineage-records", str(path))]
    config.write_text(json.dumps(raw), encoding="utf-8")
    return case, args, paths, provenance, config


def _change_config(path, update):
    raw = json.loads(path.read_text())
    update(raw)
    path.write_text(json.dumps(raw), encoding="utf-8")


def _invoke(args, out, capsys, *, command="audit"):
    from recursive_integrity_toolkit.cli import main
    code = main([command, *args, "--out", str(out)])
    streams = capsys.readouterr()
    directory = out / "reports" if command == "example" else out
    report_path = directory / "report.json"
    report = json.loads(report_path.read_text()) if report_path.is_file() else None
    markdown_path = directory / "report.md"
    markdown = markdown_path.read_text() if markdown_path.is_file() else ""
    if report is not None:
        from recursive_integrity_toolkit.result import validate_report
        validate_report(report)
        assert report["run"]["report_schema_version"] == "1.3"
        assert report["run"]["network_call_count"] == 0
        assert report["capabilities"] == report["observability"].get("capabilities", {})
        assert report["simulations"] == {}
        assert markdown.startswith("# Recursive Integrity Audit Report\n")
    return code, report, markdown, streams


def _series(report):
    return report["derived_metrics"]["longitudinal"]


def _assert_snapshots(report, case):
    inputs = report["inputs"]["longitudinal"]["snapshots"]
    assert [row["dataset_version"] for row in inputs] == case["selected_versions"]
    for descriptor, facts, metrics in zip(inputs, report["observed_facts"]["longitudinal"]["snapshots"],
                                         _series(report)["snapshots"], strict=True):
        expected = case["expected_snapshots"][descriptor["dataset_version"]]
        assert facts["record_count"]["value"] == expected["record_count"]
        assert metrics["support_size"]["value"] == expected["support_size"]
        expected_diversity = expected["diversity"]
        assert metrics["gini_simpson_diversity"]["value"] == (
            None if expected_diversity is None else pytest.approx(float(Fraction(expected_diversity))))


@pytest.mark.parametrize("format", FORMATS)
@pytest.mark.parametrize("config_inputs", [False, True])
def test_real_loaders_order_by_declaration_and_keep_all_snapshot_populations(tmp_path, capsys, format, config_inputs):
    case, args, paths, provenance, config = _inputs(tmp_path, format=format, config_inputs=config_inputs)
    before = {path: path.read_bytes() for path in (*paths.values(), provenance, config)}
    code, report, markdown, _ = _invoke(args, tmp_path / "out", capsys)
    assert code == 0
    _assert_snapshots(report, case)
    pairs = _series(report)["comparisons"]
    assert len(pairs) == 2
    assert [row["support_delta"]["value"] for row in pairs] == [-1, 1]
    assert [row["gini_simpson_diversity_delta"]["value"] for row in pairs] == pytest.approx([-1 / 8, 1 / 6])
    assert all(path.read_bytes() == content for path, content in before.items())
    assert "Ordered longitudinal snapshots" in markdown and "Ordered longitudinal comparisons" in markdown
    assert all(row["families"][family]["execution_status"] == "not_requested"
               for row in report["capabilities"]["dataset_longitudinal"]["longitudinal_execution"]["comparison_statuses"]
               for family in ("lineage", "tail"))
    assert set(report["derived_metrics"]["support"]["by_version"]) == {"v3"}


@pytest.mark.parametrize("configured", [False, True])
def test_explicit_first_baseline_adds_only_unique_pairs(tmp_path, capsys, configured):
    case, args, _, _, config = _inputs(tmp_path)
    if configured:
        _change_config(config, lambda raw: raw["longitudinal"].update(baseline="first"))
    else:
        args += ["--baseline", "first"]
    code, report, _, _ = _invoke(args, tmp_path / "out", capsys)
    assert code == 0
    assert [row["kinds"] for row in report["inputs"]["longitudinal"]["comparisons"]] == [
        ["adjacent", "baseline"], ["baseline"], ["adjacent"]]
    assert [row["support_delta"]["value"] for row in _series(report)["comparisons"]] == [-1, 0, 1]


@pytest.mark.parametrize("name", ["lexical_order_context_unloaded", "tied_timestamps_explicit_order"])
def test_declared_chronology_accepts_lexical_traps_and_timestamp_tiebreak(tmp_path, capsys, name):
    case, args, _, _, _ = _inputs(tmp_path, name)
    code, report, _, _ = _invoke(args, tmp_path / "out", capsys)
    assert code == 0
    assert [row["dataset_version"] for row in report["inputs"]["longitudinal"]["snapshots"]] == case["selected_versions"]
    assert len(_series(report)["comparisons"]) == len(case["selected_versions"]) - 1


def test_explicit_tail_uses_earlier_snapshot_and_observed_later_disappearance(tmp_path, capsys):
    _, args, _, _, _ = _inputs(tmp_path)
    code, report, _, _ = _invoke(args + ["--tail-rule", "singleton_count"], tmp_path / "out", capsys)
    assert code == 0
    pairs = _series(report)["comparisons"]
    assert [row["tail_extinct_states"]["value"]["items"] for row in pairs] == [["B", "C"], []]
    assert all(row["tail_extinct_states"]["status"] == "available" for row in pairs)


def test_incompatible_middle_preserves_snapshot_values_and_adjacent_gaps(tmp_path, capsys):
    case, args, _, _, _ = _inputs(tmp_path, "incompatible_middle", per_version=True)
    code, report, _, _ = _invoke(args + ["--baseline", "first"], tmp_path / "out", capsys)
    assert code == 1
    _assert_snapshots(report, case)
    pairs = _series(report)["comparisons"]
    assert [row["support_delta"]["status"] for row in pairs] == ["unavailable", "available", "unavailable"]
    assert report["capabilities"]["dataset_longitudinal"]["longitudinal_execution"]["status"] == "partial"


def test_per_version_directed_mapping_keeps_original_and_harmonized_values(tmp_path, capsys):
    case, args, _, _, _ = _inputs(tmp_path, "directed_many_to_one", per_version=True)
    code, report, _, _ = _invoke(args, tmp_path / "out", capsys)
    assert code == 0
    _assert_snapshots(report, case)
    pair = _series(report)["comparisons"][0]
    assert pair["support_delta"]["value"] == 0
    assert pair["gini_simpson_diversity_delta"]["value"] == 0
    assert pair["support_retention_ratio"]["value"] == 1
    declaration = report["inputs"]["longitudinal"]["comparisons"][0]
    assert declaration["mapping"]["direction"] == "earlier_to_later"
    assert declaration["mapping"]["entries"]["total_count"] == 3
    assert declaration["mapping_collisions"]["total_count"] == 1
    assert set(report["derived_metrics"]["support"]["by_version"]) == {"v2"}


def test_partial_mapping_reports_failure_and_keeps_independent_snapshots(tmp_path, capsys):
    case, args, _, _, config = _inputs(tmp_path, "directed_many_to_one", per_version=True)
    _change_config(config, lambda raw: raw["longitudinal"]["mappings"][0]["declaration"]["state_mapping"].pop("red"))
    code, report, _, _ = _invoke(args, tmp_path / "out", capsys)
    assert code == 1
    _assert_snapshots(report, case)
    assert all(row["support_delta"]["value"] is None for row in _series(report)["comparisons"])
    assert report["capabilities"]["dataset_longitudinal"]["longitudinal_execution"]["status"] == "failed"


@pytest.mark.parametrize("flag", ["--longitudinal", "--baseline", "--lineage"])
def test_validate_rejects_execution_flags(tmp_path, capsys, flag):
    _, args, _, _, _ = _inputs(tmp_path)
    extra = [flag, "first"] if flag == "--baseline" else [flag]
    code, report, _, streams = _invoke(args + extra, tmp_path / "out", capsys, command="validate")
    assert code == 2 and "E_CONFIG_INVALID" in streams.err
    assert report is None or not report["derived_metrics"].get("longitudinal", {}).get("snapshots")


@pytest.mark.parametrize("configured", [False, True])
def test_validate_repeated_comparisons_and_enabled_config_never_execute(tmp_path, capsys, monkeypatch, configured):
    _, args, _, _, _ = _inputs(tmp_path, config_inputs=configured)
    names = ("metrics.longitudinal", "metrics.diversity", "metrics.provenance", "metrics.bounds", "metrics.tail",
             "representations.field", "representations.content_hash", "representations.compatibility",
             "lineage.graph", "lineage.cycles", "lineage.ancestry")
    def denied(*args, **kwargs):
        pytest.fail("validate executed an analytical owner")
    for name in names:
        module = importlib.import_module("recursive_integrity_toolkit." + name)
        for key, value in vars(module).copy().items():
            if inspect.isfunction(value) and value.__module__ == module.__name__:
                monkeypatch.setattr(module, key, denied)
    code, report, _, _ = _invoke(args, tmp_path / "out", capsys, command="validate")
    assert code == 0
    assert report["derived_metrics"] == {"longitudinal": {"snapshots": [], "comparisons": []}}
    assert report["capabilities"]["dataset_longitudinal"]["execution_status"] == "not_requested"
    assert set(report["observed_facts"]["record_counts"]) == {"v1", "v2", "v3"}


@pytest.mark.parametrize("case", ["enabled_duplicate", "baseline_duplicate", "semantics_duplicate", "compare_sources",
                                  "disabled_execution", "per_version_common", "ordinary_repeated", "order_sources"])
def test_competing_sources_and_disabled_execution_are_configuration_errors(tmp_path, capsys, case):
    _, args, paths, _, config = _inputs(tmp_path, per_version=case == "per_version_common")
    raw = json.loads(config.read_text())
    if case == "enabled_duplicate":
        args += ["--longitudinal"]
    elif case == "baseline_duplicate":
        raw["longitudinal"]["baseline"] = "first"
        args += ["--baseline", "first"]
    elif case == "semantics_duplicate":
        args += ["--state-semantics", raw["longitudinal"]["state_semantics"]]
    elif case == "compare_sources":
        raw["inputs"] = {"records_compare": [str(paths["v1"])]}
    elif case == "disabled_execution":
        raw["longitudinal"]["enabled"] = False
    elif case == "per_version_common":
        args += ["--state-semantics", "competing meaning"]
    elif case == "ordinary_repeated":
        raw.pop("longitudinal")
    else:
        raw["version_order"] = ["v1", "v2", "v3"]
    config.write_text(json.dumps(raw))
    code, report, _, streams = _invoke(args, tmp_path / "out", capsys)
    assert code == 2 and "E_CONFIG_INVALID" in streams.err
    assert report is None or not report["derived_metrics"].get("longitudinal", {}).get("snapshots")


@pytest.mark.parametrize("case", ["empty_primary", "empty_comparison", "mixed_primary", "mixed_comparison",
                                  "duplicate_version", "primary_not_latest", "context_overlap"])
def test_file_roles_require_distinct_nonempty_single_versions_and_latest_primary(tmp_path, capsys, case):
    _, args, paths, _, _ = _inputs(tmp_path)
    if case.startswith("empty"):
        paths["v3" if case == "empty_primary" else "v1"].write_bytes(b"")
    elif case.startswith("mixed"):
        path = paths["v3" if case == "mixed_primary" else "v1"]
        with path.open("a") as stream:
            stream.write(json.dumps({"dataset_version": "v4", "record_id": "extra", "topic": "A", "content": "x"}) + "\n")
    elif case == "duplicate_version":
        extra = tmp_path / "duplicate-version.jsonl"
        _write(extra, [{"dataset_version": "v1", "record_id": "other", "topic": "A", "content": "x"}])
        args += ["--compare", str(extra)]
    elif case == "primary_not_latest":
        first, last = args.index(str(paths["v1"])), args.index(str(paths["v3"]))
        args[first], args[last] = args[last], args[first]
    else:
        extra = tmp_path / "overlapping-context.jsonl"
        _write(extra, [{"dataset_version": "v1", "record_id": "context", "topic": "A", "content": "x"}])
        args += ["--lineage", "--lineage-records", str(extra)]
    code, report, _, _ = _invoke(args, tmp_path / "out", capsys)
    assert code in (1, 2)
    assert report is not None and report["errors"]
    assert report["capabilities"].get("dataset_longitudinal", {}).get("execution_status") != "completed"


@pytest.mark.parametrize("case", ["missing_order", "conflicting_order"])
def test_incomplete_series_metadata_preserves_independent_snapshot_values(tmp_path, capsys, case):
    fixture, args, _, _, config = _inputs(tmp_path, "missing_order" if case == "missing_order" else "observed_three_version")
    if case == "conflicting_order":
        order = Path(args[args.index("--version-order") + 1])
        order.write_text(json.dumps({"version_order": ["v1", "v2", "v3"],
            "version_timestamps": {"v1": "2026-03-01T00:00:00Z", "v2": "2026-02-01T00:00:00Z", "v3": "2026-01-01T00:00:00Z"}}))
    code, report, _, _ = _invoke(args, tmp_path / "out", capsys)
    assert code in (1, 2)
    assert report is not None
    observed = report["observed_facts"]["longitudinal"]["snapshots"]
    metrics = _series(report)["snapshots"]
    assert len(observed) == len(fixture["selected_versions"])
    assert sorted(row["record_count"]["value"] for row in observed) == sorted(
        sum(record["dataset_version"] == version for record in fixture["records"])
        for version in fixture["selected_versions"])
    assert all(row["support_size"]["value"] is not None for row in metrics)
    assert report["capabilities"]["dataset_longitudinal"]["longitudinal_execution"]["status"] == "failed"
    assert not _series(report)["comparisons"]


def test_missing_required_common_semantics_is_a_configuration_error(tmp_path, capsys):
    _, args, _, _, config = _inputs(tmp_path)
    _change_config(config, lambda raw: raw["longitudinal"].pop("state_semantics"))
    code, report, _, streams = _invoke(args, tmp_path / "out", capsys)
    assert code == 2 and "E_CONFIG_INVALID" in streams.err
    assert report is None or not report["derived_metrics"].get("longitudinal", {}).get("snapshots")


@pytest.mark.parametrize("record_ids", [None, "hash", "omit"])
def test_redacted_output_hides_literal_mapping_keys_values_and_paths(tmp_path, capsys, record_ids):
    _, args, paths, provenance, config = _inputs(tmp_path, "directed_many_to_one", per_version=True)
    labels = {label: "PRIVATE_STATE_" + label for label in ("red", "green", "pear", "apple")}
    for path in paths.values():
        rows = [json.loads(line) for line in path.read_text().splitlines()]
        for row in rows:
            row["topic"] = labels[row["topic"]]
            row["content"] = "PRIVATE_CONTENT_SENTINEL"
        _write(path, rows)
    def update(raw):
        mapping = raw["longitudinal"]["mappings"][0]["declaration"]["state_mapping"]
        raw["longitudinal"]["mappings"][0]["declaration"]["state_mapping"] = {
            labels[key]: labels[value] for key, value in mapping.items()}
        raw["longitudinal"]["versions"][0]["state_semantics"] = "PRIVATE_MEANING_FINE"
        raw["longitudinal"]["mappings"][0]["declaration"]["source_state_semantics"] = "PRIVATE_MEANING_FINE"
    _change_config(config, update)
    extra = ["--redacted"] + ([] if record_ids is None else ["--record-ids", record_ids])
    code, report, markdown, streams = _invoke(args + extra, tmp_path / "out", capsys)
    assert code == 0
    sinks = json.dumps(report) + markdown + streams.out + streams.err
    assert "PRIVATE_" not in sinks and str(tmp_path) not in sinks
    assert _series(report)["comparisons"][0]["support_delta"]["value"] == 0
    assert report["run"]["privacy_mode"] == "redacted"


def test_plain_series_does_not_traverse_graph_or_run_tail(tmp_path, capsys, monkeypatch):
    _, args, _, _, _ = _inputs(tmp_path)
    def denied(*args, **kwargs):
        pytest.fail("unrequested optional analysis was dispatched")
    for module_name, function_name in (("lineage.graph", "build_lineage_graph"),
            ("lineage.ancestry", "analyze_selected_lineage"), ("metrics.tail", "select_tail")):
        monkeypatch.setattr(importlib.import_module("recursive_integrity_toolkit." + module_name), function_name, denied)
    code, report, _, _ = _invoke(args, tmp_path / "out", capsys)
    assert code == 0
    assert report["observed_facts"]["longitudinal"]["shared_lineage"] is None


def test_selected_lineage_context_is_loaded_once_and_excluded_from_snapshots(tmp_path, capsys, monkeypatch):
    case, args, _, _, _ = _inputs(tmp_path, "lineage_complete")
    ancestry = importlib.import_module("recursive_integrity_toolkit.lineage.ancestry")
    calls = {"build_lineage_graph": 0, "analyze_cycles": 0}
    for name in calls:
        original = getattr(ancestry, name)
        def counted(*args, _name=name, _original=original, **kwargs):
            calls[_name] += 1
            return _original(*args, **kwargs)
        monkeypatch.setattr(ancestry, name, counted)
    code, report, _, _ = _invoke(args, tmp_path / "out", capsys)
    assert code == 0
    assert calls == {"build_lineage_graph": 1, "analyze_cycles": 1}
    assert [row["dataset_version"] for row in report["inputs"]["longitudinal"]["snapshots"]] == case["selected_versions"]
    shared = report["observed_facts"]["longitudinal"]["shared_lineage"]
    assert shared["loaded_record_count"] == len(case["records"])
    assert [row["distinct_external_root_count"]["value"] for row in _series(report)["snapshots"]] == [2, 1, 2]
    assert [row["ancestry_concentration_hhi_delta"]["value"] for row in _series(report)["comparisons"]] == [0.5, -0.5]


def test_lineage_limit_reports_nonzero_exit_and_preserves_series_distribution(tmp_path, capsys):
    _, args, _, _, config = _inputs(tmp_path, "lineage_complete")
    _change_config(config, lambda raw: raw.update(resource_limits={"max_lineage_root_memberships": 1}))
    code, report, _, _ = _invoke(args, tmp_path / "out", capsys)
    assert code == 1
    assert [row["support_size"]["value"] for row in _series(report)["snapshots"]] == [2, 1, 2]
    assert all(row["distinct_external_root_count"]["value"] is None for row in _series(report)["snapshots"])
    assert any(row["code"] == "E_LINEAGE_RESOURCE_LIMIT_EXCEEDED" for row in report["errors"])


def test_existing_output_is_preserved_byte_for_byte(tmp_path, capsys):
    _, args, _, _, _ = _inputs(tmp_path)
    out = tmp_path / "existing"
    out.mkdir()
    sentinel = out / "report.json"
    sentinel.write_bytes(b"KEEP_EXISTING_BYTES")
    from recursive_integrity_toolkit.cli import main
    assert main(["audit", *args, "--out", str(out)]) == 1
    capsys.readouterr()
    assert sentinel.read_bytes() == b"KEEP_EXISTING_BYTES"
    assert sorted(path.name for path in out.iterdir()) == ["report.json"]


@pytest.mark.parametrize("lineage", [False, True])
def test_hero_example_explicit_series_uses_unchanged_two_snapshot_oracle(tmp_path, capsys, lineage):
    args = ["--longitudinal"] + (["--lineage"] if lineage else [])
    code, report, _, _ = _invoke(args, tmp_path / "example", capsys, command="example")
    assert code == 0
    assert [row["dataset_version"] for row in report["inputs"]["longitudinal"]["snapshots"]] == ["v1", "v2"]
    assert len(_series(report)["comparisons"]) == 1
    row = _series(report)["comparisons"][0]
    assert row["direct_closure_lower_bound_delta"]["value"] == 0.5
    if lineage:
        assert row["distinct_external_root_count_delta"]["value"] == -3
        assert row["ancestry_concentration_hhi_delta"]["value"] == 0.125
        assert row["effective_external_root_count_delta"]["value"] == -4
    else:
        assert row["distinct_external_root_count_delta"]["value"] is None
    for name in ("records_v1.csv", "records_v2.csv", "provenance.csv", "config.json", "version_order.json"):
        assert (tmp_path / "example/inputs" / name).read_bytes() == (ROOT / "examples/hero" / name).read_bytes()
