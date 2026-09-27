"""Complete Phase 6A reports with independently specified series arithmetic.

The bounded preflights and the separately selected 100k candidate workload use
the same generator. Every size counts all loaded records, including context.
The existing report measurement fixture records every fresh-process attempt.
"""

from fractions import Fraction
import json
import time

import pytest


VERSIONS = ("v1", "v2", "v3")
STATES = (100, 50, 25)
CONTEXT_COUNT = 100


def _inputs(directory, *, total_records):
    """Write a uniform three-version population with complete context ancestry.

    v1 is directly open, v2 half open/half closed, and v3 directly closed.
    Every target has exactly one parent among 100 parentless external anchors.
    A yes-grounding target uses the accepted one-parent carryover declaration.
    The anchor support shrinks with topic support, independently yielding the
    concentration and effective-root changes asserted below.
    """
    assert total_records in (1000, 10000, 100000)
    per_version = (total_records - CONTEXT_COUNT) // len(VERSIONS)
    assert 3 * per_version + CONTEXT_COUNT == total_records
    assert per_version % 100 == 0
    directory.mkdir()
    context = directory / "context.jsonl"
    provenance = directory / "provenance.jsonl"
    config = directory / "config.json"
    records = [directory / f"records_{version}.jsonl" for version in VERSIONS]
    with context.open("w", encoding="utf-8") as ancestors, provenance.open("w", encoding="utf-8") as manifest:
        for index in range(CONTEXT_COUNT):
            key = {"dataset_version": "roots", "record_id": f"r{index:03d}"}
            ancestors.write(json.dumps({**key, "content": "synthetic context metadata", "topic": "context"}) + "\n")
            manifest.write(json.dumps({**key, "source_type": "human", "provenance_confidence": "confirmed",
                "external_grounding": "yes", "parent_ids": [], "generation": 0}) + "\n")
        for version_index, (version, states, path) in enumerate(zip(VERSIONS, STATES, records, strict=True)):
            with path.open("w", encoding="utf-8") as stream:
                for index in range(per_version):
                    key = {"dataset_version": version, "record_id": f"n{index:06d}"}
                    opened = version_index == 0 or version_index == 1 and index % 2 == 0
                    stream.write(json.dumps({**key, "content": "synthetic selected metadata",
                        "topic": f"s{index % states:03d}"}) + "\n")
                    manifest.write(json.dumps({**key, "source_type": "human" if opened else "synthetic",
                        "provenance_confidence": "confirmed", "external_grounding": "yes" if opened else "no",
                        "transformation": "carryover" if opened else "generate",
                        "parent_ids": [f"roots::r{index % states:03d}"], "generation": 1}) + "\n")
    config.write_text(json.dumps({
        "representation": {"name": "topic", "source": "topic_field", "field": "topic",
            "version": "literal-v1", "missing_value_policy": "error"},
        "version_order": ["roots", *VERSIONS],
        "longitudinal": {"enabled": True, "baseline": "first",
            "state_semantics": "Literal synthetic topic categories shared across supplied versions"},
    }) + "\n", encoding="utf-8")
    # Reverse comparison arguments deliberately do not encode chronology.
    arguments = ["--records", str(records[2]), "--compare", str(records[1]),
        "--compare", str(records[0]), "--lineage-records", str(context),
        "--provenance", str(provenance), "--config", str(config), "--lineage"]
    return arguments, [*records, context, provenance, config]


def _assert_number(envelope, expected):
    assert envelope["status"] == "available"
    assert envelope["value"] == pytest.approx(float(expected))


def _assert_generated_report(path, request, *, total_records, construction_seconds):
    report = json.loads(path.read_bytes())
    per_version = (total_records - CONTEXT_COUNT) // 3
    assert report["run"]["run_status"] == "complete" and not report["errors"]
    assert report["run"]["network_call_count"] == 0
    assert report["simulations"] == {}
    selected = report["inputs"]["longitudinal"]
    assert [row["dataset_version"] for row in selected["snapshots"]] == list(VERSIONS)
    assert [row["kinds"] for row in selected["comparisons"]] == [
        ["adjacent", "baseline"], ["baseline"], ["adjacent"]]
    facts = report["observed_facts"]["longitudinal"]
    metrics = report["derived_metrics"]["longitudinal"]
    execution = report["capabilities"]["dataset_longitudinal"]["longitudinal_execution"]
    assert execution["status"] == "completed"
    for index, (observed, snapshot, states) in enumerate(zip(facts["snapshots"], metrics["snapshots"], STATES, strict=True)):
        closed = Fraction(index, 2)
        assert observed["record_count"]["value"] == per_version
        assert observed["representation_eligible_record_count"]["value"] == per_version
        assert observed["representation_excluded_record_count"]["value"] == 0
        for name in ("provenance_row_coverage", "provenance_required_field_coverage", "grounding_field_coverage"):
            _assert_number(observed[name], 1)
        _assert_number(snapshot["support_size"], states)
        _assert_number(snapshot["gini_simpson_diversity"], 1 - Fraction(1, states))
        assert snapshot["source_type_shares"]["value"] == {
            "human": float(1 - closed), "synthetic": float(closed), "mixed": 0., "sensor": 0., "unknown": 0.}
        for suffix, value in (("lower_bound", closed), ("upper_bound", closed), ("interval_width", 0)):
            _assert_number(snapshot["direct_closure_" + suffix], value)
            _assert_number(snapshot["lineage_closure_" + suffix], 0)
        for name, value in (("grounded_record_count", per_version), ("closed_record_count", 0),
            ("unresolved_record_count", 0), ("distinct_external_root_count", states),
            ("ancestry_concentration_hhi", Fraction(1, states)), ("effective_external_root_count", states),
            ("resolved_parent_edge_coverage", 1), ("resolved_lineage_coverage", 1), ("external_ancestry_coverage", 1)):
            _assert_number(snapshot[name], value)
        for name, value in (("declared_parent_reference_count", per_version),
            ("resolved_parent_reference_count", per_version), ("unresolved_parent_reference_count", 0)):
            assert observed[name]["value"] == value
    for pair, (earlier, later) in zip(metrics["comparisons"], ((0, 1), (0, 2), (1, 2)), strict=True):
        previous, following = STATES[earlier], STATES[later]
        difference = Fraction(later - earlier, 2)
        expected = {
            "record_count_delta": 0, "support_delta": following - previous,
            "gini_simpson_diversity_delta": Fraction(1, previous) - Fraction(1, following),
            "support_loss_count": previous - following, "support_added_count": 0,
            "support_retention_ratio": Fraction(following, previous),
            "provenance_row_coverage_delta": 0, "provenance_required_field_coverage_delta": 0,
            "grounding_field_coverage_delta": 0, "missing_provenance_share_delta": 0,
            "direct_closure_lower_bound_delta": difference, "direct_closure_upper_bound_delta": difference,
            "direct_closure_interval_width_delta": 0,
            "distinct_external_root_count_delta": following - previous,
            "ancestry_concentration_hhi_delta": Fraction(1, following) - Fraction(1, previous),
            "effective_external_root_count_delta": following - previous,
            "unresolved_parent_reference_count_delta": 0, "resolved_parent_edge_coverage_delta": 0,
            "resolved_lineage_coverage_delta": 0, "external_ancestry_coverage_delta": 0,
            "lineage_closure_lower_bound_delta": 0, "lineage_closure_upper_bound_delta": 0,
            "lineage_closure_interval_width_delta": 0,
        }
        for name, value in expected.items():
            _assert_number(pair[name], value)
        assert pair["source_type_share_deltas"]["value"] == {
            "human": -float(difference), "synthetic": float(difference), "mixed": 0., "sensor": 0., "unknown": 0.}
        assert pair["extinct_states"]["value"]["items"] == [f"s{index:03d}" for index in range(following, previous)]
    shared = facts["shared_lineage"]
    assert shared["execution_status"] == "completed"
    assert shared["loaded_record_count"] == total_records
    assert shared["unique_edge_count"] == total_records - CONTEXT_COUNT
    assert shared["cycle_count"] == 0
    usage = shared["resource_usage"]
    assert (usage["admitted_node_count"], usage["admitted_edge_count"],
        usage["stored_root_membership_count"], usage["root_union_visit_count"]) == (
            total_records, total_records - CONTEXT_COUNT, total_records, total_records - CONTEXT_COUNT)
    assert usage["exhausted_limit"] is usage["attempted_value"] is None
    assert usage["limits"] == {"max_nodes": 200000, "max_edges": 1000000,
        "max_root_memberships": 1000000, "max_root_union_visits": 10000000}
    assert report["derived_metrics"]["lineage"]["lineage_depth"]["value"] == 1
    primary = report["observed_facts"]["lineage"]["graph_scope"]["value"]
    assert (primary["target_record_count"], primary["context_record_count"], primary["loaded_record_count"]) == (
        per_version, total_records - per_version, total_records)
    request.node.user_properties.append(("longitudinal_workload", json.dumps(dict(
        total_loaded_records=total_records, selected_records=total_records - CONTEXT_COUNT,
        context_records=CONTEXT_COUNT, per_version_records=per_version, selected_version_count=3,
        comparison_count=3, topic_supports=STATES, target_root_supports=STATES,
        resource_usage=usage, depth=1, construction_seconds=construction_seconds,
        report_path=str(path), resource_defaults_unchanged=True), sort_keys=True)))


@pytest.mark.parametrize("total_records", [1000, 10000])
def test_longitudinal_bounded_complete_reports(phase4_step10_measure_reports, tmp_path, request, total_records):
    """Step 8 preflights; select each size separately when reviewing growth."""
    start = time.perf_counter()
    arguments, paths = _inputs(tmp_path / "inputs", total_records=total_records)
    construction_seconds = time.perf_counter() - start
    reports, _ = phase4_step10_measure_reports(f"longitudinal_{total_records}", arguments, paths,
        record_count=total_records, trace_allocations=False, timeout_seconds=300)
    for path in reports:
        _assert_generated_report(path, request, total_records=total_records, construction_seconds=construction_seconds)


def test_longitudinal_100k_complete_reports(phase4_step10_measure_reports, tmp_path, request):
    """Step 9 reference gate: actual 100k combined records through both formats."""
    start = time.perf_counter()
    arguments, paths = _inputs(tmp_path / "inputs", total_records=100000)
    construction_seconds = time.perf_counter() - start
    reports, _ = phase4_step10_measure_reports("longitudinal_100000", arguments, paths,
        record_count=100000, trace_allocations=False, timeout_seconds=1800)
    for path in reports:
        _assert_generated_report(path, request, total_records=100000, construction_seconds=construction_seconds)


def _many_version_inputs(directory):
    """Keep the compact workload identical to the Step 8 profile investigation."""
    directory.mkdir()
    order = ["context", *(f"v{index:03d}" for index in range(20))]
    paths, manifest = [], []
    for ordinal, version in enumerate(order):
        rows = []
        for index in range(20 if ordinal == 0 else 10):
            key = {"dataset_version": version, "record_id": f"r{index:05d}"}
            rows.append({**key, "content": "bounded performance input", "topic": f"s{index % 10:02d}"})
            manifest.append({**key, "source_type": "human" if ordinal == 0 else "synthetic",
                "provenance_confidence": "confirmed", "external_grounding": "yes" if ordinal == 0 else "no",
                "parent_ids": [] if ordinal == 0 else [f"context::r{index % 20:05d}"],
                "transformation": "generate"})
        path = directory / f"{version}.jsonl"
        path.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")
        paths.append(path)
    provenance = directory / "provenance.jsonl"
    provenance.write_text("".join(json.dumps(row) + "\n" for row in manifest), encoding="utf-8")
    config = directory / "config.json"
    config.write_text(json.dumps({"representation": {"name": "topic", "source": "topic_field", "field": "topic",
        "version": "topics-v1", "missing_value_policy": "error"}, "version_order": order,
        "longitudinal": {"enabled": True, "state_semantics": "literal fixture topic categories", "baseline": "first"}}),
        encoding="utf-8")
    arguments = ["--records", str(paths[-1]), "--provenance", str(provenance), "--config", str(config),
        "--lineage", "--lineage-records", str(paths[0]),
        *[part for path in paths[1:-1] for part in ("--compare", str(path))]]
    return arguments, [*paths, provenance, config]


def test_longitudinal_many_versions_complete_reports(phase4_step10_measure_reports, tmp_path, request):
    """Twenty selected snapshots exercise pair scheduling and shared graph work."""
    start = time.perf_counter()
    arguments, paths = _many_version_inputs(tmp_path / "inputs")
    construction_seconds = time.perf_counter() - start
    reports, _ = phase4_step10_measure_reports("longitudinal_20_versions_220_records", arguments, paths,
        record_count=220, trace_allocations=False, timeout_seconds=180)
    for path in reports:
        report = json.loads(path.read_bytes())
        assert report["run"]["run_status"] == "complete" and not report["errors"]
        assert report["run"]["network_call_count"] == 0
        assert report["capabilities"]["dataset_longitudinal"]["longitudinal_execution"]["status"] == "completed"
        selected = report["inputs"]["longitudinal"]
        assert [item["dataset_version"] for item in selected["snapshots"]] == [f"v{index:03d}" for index in range(20)]
        pairs = selected["comparisons"]
        assert len(pairs) == 37
        assert sum("adjacent" in pair["kinds"] for pair in pairs) == 19
        assert sum("baseline" in pair["kinds"] for pair in pairs) == 19
        snapshots = report["derived_metrics"]["longitudinal"]["snapshots"]
        facts = report["observed_facts"]["longitudinal"]
        for observed, snapshot in zip(facts["snapshots"], snapshots, strict=True):
            assert observed["record_count"]["value"] == 10
            for name, value in (("support_size", 10), ("gini_simpson_diversity", Fraction(9, 10)),
                ("direct_closure_lower_bound", 1), ("direct_closure_upper_bound", 1),
                ("grounded_record_count", 10), ("closed_record_count", 0), ("unresolved_record_count", 0),
                ("distinct_external_root_count", 10), ("ancestry_concentration_hhi", Fraction(1, 10)),
                ("effective_external_root_count", 10), ("resolved_lineage_coverage", 1),
                ("external_ancestry_coverage", 1), ("lineage_closure_lower_bound", 0), ("lineage_closure_upper_bound", 0)):
                _assert_number(snapshot[name], value)
            assert snapshot["source_type_shares"]["value"] == {"human": 0., "synthetic": 1., "mixed": 0., "sensor": 0., "unknown": 0.}
        comparisons = report["derived_metrics"]["longitudinal"]["comparisons"]
        assert len(comparisons) == 37
        for pair in comparisons:
            for name, envelope in pair.items():
                if name.endswith("_delta"):
                    _assert_number(envelope, 0)
            _assert_number(pair["support_retention_ratio"], 1)
            assert pair["source_type_share_deltas"]["value"] == {
                "human": 0., "synthetic": 0., "mixed": 0., "sensor": 0., "unknown": 0.}
        usage = facts["shared_lineage"]["resource_usage"]
        assert (usage["admitted_node_count"], usage["admitted_edge_count"],
            usage["stored_root_membership_count"], usage["root_union_visit_count"]) == (220, 200, 220, 200)
        assert usage["exhausted_limit"] is usage["attempted_value"] is None
        assert report["derived_metrics"]["lineage"]["lineage_depth"]["value"] == 1
        request.node.user_properties.append(("longitudinal_workload", json.dumps(dict(
            total_loaded_records=220, selected_records=200, context_records=20,
            per_version_records=10, selected_version_count=20, comparison_count=37,
            topic_supports=[10] * 20, target_root_supports=[10] * 20,
            resource_usage=usage, depth=1, construction_seconds=construction_seconds,
            report_path=str(path), resource_defaults_unchanged=True), sort_keys=True)))


@pytest.mark.parametrize("lineage", [False, True], ids=["distribution", "lineage"])
def test_longitudinal_hero_complete_reports(phase4_step10_measure_reports, repo_root, lineage, request):
    """Retain all three fresh untraced Hero attempts for each explicit mode."""
    hero = repo_root / "examples/hero"
    names = ("records_v2.csv", "records_v1.csv", "provenance.csv", "config.json", "version_order.json")
    flags = ("--records", "--compare", "--provenance", "--config", "--version-order")
    arguments = [item for flag, name in zip(flags, names, strict=True) for item in (flag, str(hero / name))]
    arguments += ["--longitudinal", "--state-semantics", "literal Hero topic categories"]
    if lineage:
        arguments += ["--lineage"]
    reports, observations = phase4_step10_measure_reports("longitudinal_hero", arguments,
        [hero / name for name in names], record_count=16, untraced_attempts=3, trace_allocations=False)
    for path in reports:
        report = json.loads(path.read_bytes())
        assert report["run"]["run_status"] == "complete" and not report["errors"]
        assert report["run"]["network_call_count"] == 0
        snapshots = report["derived_metrics"]["longitudinal"]["snapshots"]
        facts = report["observed_facts"]["longitudinal"]
        assert [row["record_count"]["value"] for row in facts["snapshots"]] == [8, 8]
        assert [row["support_size"]["value"] for row in snapshots] == [8, 5]
        assert [row["gini_simpson_diversity"]["value"] for row in snapshots] == [float(Fraction(7, 8)), float(Fraction(3, 4))]
        pair, = report["derived_metrics"]["longitudinal"]["comparisons"]
        for name, expected in (("support_delta", -3), ("gini_simpson_diversity_delta", Fraction(-1, 8)),
            ("support_retention_ratio", Fraction(5, 8)), ("direct_closure_lower_bound_delta", Fraction(1, 2))):
            _assert_number(pair[name], expected)
        if lineage:
            assert [row["distinct_external_root_count"]["value"] for row in snapshots] == [8, 5]
            assert [row["ancestry_concentration_hhi"]["value"] for row in snapshots] == [float(Fraction(1, 8)), float(Fraction(1, 4))]
            for name, expected in (("distinct_external_root_count_delta", -3),
                ("ancestry_concentration_hhi_delta", Fraction(1, 8)), ("effective_external_root_count_delta", -4)):
                _assert_number(pair[name], expected)
        else:
            assert report["observed_facts"]["longitudinal"]["shared_lineage"] is None
            assert pair["ancestry_concentration_hhi_delta"]["status"] == "unavailable"
        usage = facts["shared_lineage"]["resource_usage"] if lineage else None
        if lineage:
            assert (usage["admitted_node_count"], usage["admitted_edge_count"],
                usage["stored_root_membership_count"], usage["root_union_visit_count"]) == (16, 8, 16, 8)
        request.node.user_properties.append(("longitudinal_workload", json.dumps(dict(
            total_loaded_records=16, selected_records=16, context_records=0,
            per_version_records=8, selected_version_count=2, comparison_count=1,
            topic_supports=[8, 5], target_root_supports=[8, 5] if lineage else None,
            resource_usage=usage, depth=1 if lineage else None,
            report_path=str(path), resource_defaults_unchanged=True), sort_keys=True)))
    assert [item["mode"] for item in observations] == ["untraced"] * 3
    request.node.user_properties.append(("longitudinal_hero_target", json.dumps(dict(
        target_seconds=5, all_outer_wall_seconds=[item["subprocess_wall_seconds"] for item in observations],
        all_under_target=all(item["subprocess_wall_seconds"] < 5 for item in observations),
        lineage=lineage, best_run_selection=False), sort_keys=True)))
    # Each reference target miss requires acceptance review; a fastest run can
    # never replace it. Runtime noise does not invalidate scientific assertions.
