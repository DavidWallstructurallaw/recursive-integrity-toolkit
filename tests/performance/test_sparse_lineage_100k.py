"""Current lineage scale observations, once per designated reference profile.

The 100k API run includes loading, generation validation and complete ancestry.
Bounded end-to-end runs reuse the existing CLI fixture through both report
formats. No allocation tracing or wall-clock performance SLA is applied at 100k.
"""

import json
from pathlib import Path


def _inputs(directory, *, size=None, width=None):
    """Deterministic reverse chain or a two-version dense parent fan-in."""
    directory.mkdir()
    primary = directory / "primary.jsonl"
    context = directory / "context.jsonl"
    provenance = directory / "provenance.jsonl"
    config = directory / "config.json"
    with primary.open("w", encoding="utf-8") as records, provenance.open("w", encoding="utf-8") as manifest:
        for index in range(size if size is not None else width):
            key = dict(dataset_version="m" if size is not None else "v2", record_id=f"n{index:06d}")
            records.write(json.dumps({**key, "content": "synthetic lineage input", "topic": f"s{index % 20:02d}"}) + "\n")
            anchor = size is not None and index == size - 1
            parents = ([] if anchor else [f"m::n{index + 1:06d}"]) if size is not None else [f"v1::r{i:06d}" for i in range(width)]
            manifest.write(json.dumps({**key, "source_type": "human" if anchor else "synthetic",
                "provenance_confidence": "confirmed", "external_grounding": "yes" if anchor else "no",
                "transformation": "generate", "parent_ids": parents,
                "generation": size - 1 - index if size is not None else 1}) + "\n")
        if width is not None:
            with context.open("w", encoding="utf-8") as ancestors:
                for index in range(width):
                    key = dict(dataset_version="v1", record_id=f"r{index:06d}")
                    ancestors.write(json.dumps({**key, "content": "synthetic context", "topic": "context"}) + "\n")
                    manifest.write(json.dumps({**key, "source_type": "human", "provenance_confidence": "confirmed",
                        "external_grounding": "yes", "parent_ids": [], "generation": 0}) + "\n")
    config.write_text(json.dumps({"representation": {"name": "topic", "source": "topic_field",
        "field": "topic", "version": "1", "missing_value_policy": "error"},
        "version_order": ["m"] if size is not None else ["v1", "v2"]}) + "\n", encoding="utf-8")
    paths = [primary, provenance, config]
    args = ["--records", str(primary), "--provenance", str(provenance), "--config", str(config), "--lineage"]
    if width is not None:
        paths.append(context)
        args += ["--lineage-records", str(context)]
    return args, paths


def _assert_reports(reports, request, *, nodes, edges, targets, contexts, memberships, visits, roots, depth):
    for path in reports:
        report = json.loads(path.read_bytes())
        assert report["run"]["run_status"] == "complete" and not report["errors"]
        assert report["run"]["network_call_count"] == 0
        assert report["capabilities"]["lineage"]["execution_status"] == "completed"
        facts = report["observed_facts"]["lineage"]
        scope = facts["graph_scope"]["value"]
        assert (scope["loaded_record_count"], scope["target_record_count"], scope["context_record_count"]) == (nodes, targets, contexts)
        usage = facts["resource_usage"]["value"]
        assert (usage["admitted_node_count"], usage["admitted_edge_count"]) == (nodes, edges)
        assert (usage["stored_root_membership_count"], usage["root_union_visit_count"]) == (memberships, visits)
        assert usage["exhausted_limit"] is usage["attempted_value"] is None
        metrics = report["derived_metrics"]["lineage"]
        for name, expected in (("grounded_record_count", targets), ("closed_record_count", 0),
            ("unresolved_record_count", 0), ("distinct_external_root_count", roots),
            ("ancestry_concentration_hhi", 1 / roots), ("effective_external_root_count", float(roots)),
            ("lineage_depth", depth), ("resolved_lineage_coverage", 1.0)):
            assert metrics[name]["value"] == expected
        bounds = report["derived_metrics"]["closure_exposure"]["lineage"]
        assert [bounds[name]["value"] for name in ("lower_bound", "upper_bound", "interval_width")] == [0.0, 0.0, 0.0]
        assert facts["cycle_analysis"]["value"]["cycle_count"] == 0
        request.node.user_properties.append(("lineage_workload", json.dumps(dict(
            scope=scope, resource_usage=usage, lineage_depth=depth, distinct_roots=roots,
            report_path=str(path)), sort_keys=True)))


def test_sparse_lineage_bounded_complete_reports(phase4_step10_measure_reports, tmp_path, request):
    size = 1000
    args, paths = _inputs(tmp_path / "chain-inputs", size=size)
    reports, _ = phase4_step10_measure_reports("lineage_chain_1000", args, paths,
        record_count=size, trace_allocations=False, timeout_seconds=180)
    _assert_reports(reports, request, nodes=size, edges=size - 1, targets=size, contexts=0,
        memberships=size, visits=size - 1, roots=1, depth=size - 1)


def _api_worker(directory):
    """Linux reference worker; no reports or ordinary metric families executed."""
    import resource
    import time
    start = time.perf_counter()
    from dataclasses import asdict
    from recursive_integrity_toolkit.io.validation import validate_bundle
    from recursive_integrity_toolkit.lineage.ancestry import analyze_lineage
    from recursive_integrity_toolkit.models import AuditBundle, FileRole, InputSource

    validation = validate_bundle(AuditBundle(tuple(InputSource(role, directory / name) for role, name in (
        (FileRole.RECORDS_PRIMARY, "primary.jsonl"), (FileRole.PROVENANCE_MANIFEST, "provenance.jsonl"),
        (FileRole.CONFIG, "config.json")))))
    validated = time.perf_counter()
    assert not validation.has_errors
    result = analyze_lineage(validation, target_dataset_version="m")
    analyzed = time.perf_counter()
    size = len(validation.records)
    root = validation.records[-1].record_key
    assert [item.expected_generation for item in validation.generation.assessments] == list(reversed(range(size)))
    assert all(record.external_root_keys == frozenset((root,)) for record in result.records)
    assert result.root_contributions[0].incidence_count == size
    summary = dict(scope={name: getattr(result.scope, name) for name in
        ("target_record_count", "loaded_record_count", "context_record_count", "target_dataset_version")},
        resource_usage=asdict(result.resource_usage), execution_status=result.execution_status.value,
        grounded=result.grounded_record_count, closed=result.closed_record_count, unresolved=result.unresolved_record_count,
        distinct_roots=result.distinct_external_root_count, hhi=result.ancestry_concentration_hhi,
        effective_roots=result.effective_external_root_count, depth=result.cycles.lineage_depth,
        cycle_count=result.cycles.cycle_count, expected_generation_max=size - 1,
        validation_seconds=validated - start, ancestry_seconds=analyzed - validated,
        worker_elapsed_seconds=time.perf_counter() - start,
        rss_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024)
    (directory / "lineage-api-summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def test_sparse_lineage_100k_api(tmp_path, request, subprocess_env):
    """Actual 100k deep chain on Linux/Python 3.12, in its own fresh process."""
    import hashlib
    import importlib.metadata
    import os
    import platform
    import subprocess
    import sys
    import time

    size = 100000
    directory = tmp_path / "chain-inputs"
    _, paths = _inputs(directory, size=size)
    inputs = {path.name: dict(bytes=path.stat().st_size, sha256=hashlib.sha256(path.read_bytes()).hexdigest()) for path in paths}
    command = [sys.executable, str(Path(__file__).resolve()), str(directory)]
    start = time.perf_counter()
    timed_out = False
    try:
        process = subprocess.run(command, env=subprocess_env, capture_output=True, text=True, timeout=600, check=False)
    except subprocess.TimeoutExpired as error:
        timed_out = True
        def captured(value):
            return value.decode("utf-8", errors="replace") if isinstance(value, bytes) else value or ""
        process = subprocess.CompletedProcess(command, -1, captured(error.stdout), captured(error.stderr))
    elapsed = time.perf_counter() - start
    summary_path = directory / "lineage-api-summary.json"
    summary = json.loads(summary_path.read_text()) if summary_path.exists() else {}
    observation = dict(name="lineage_reverse_chain_100000_api", command=command, record_count=size,
        subprocess_wall_seconds=elapsed, timed_out=timed_out, timeout_seconds=600,
        process_exit_code=process.returncode, stdout=process.stdout, stderr=process.stderr,
        inputs=inputs, summary=summary, output_bytes=summary_path.stat().st_size if summary_path.exists() else None,
        environment=dict(python=platform.python_version(), platform=platform.platform(), machine=platform.machine(),
            logical_cpu_count=os.cpu_count(), versions={name: importlib.metadata.version(name) for name in ("numpy", "pandas", "pytest")}),
        includes="fresh interpreter, imports, JSONL loading, complete validation including generation, graph, cycles, depth, complete roots and concentration, API assertions and summary serialization",
        excludes="synthetic input construction, ordinary metric families and JSON/Markdown audit reports; those use separately labeled CLI measurements",
        rss_method="Linux getrusage(RUSAGE_SELF).ru_maxrss * 1024; whole fresh process including native allocations",
        tracing=False, best_run_selection=False)
    (tmp_path / "measurement.json").write_text(json.dumps(observation, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    request.node.user_properties.append(("lineage_performance", json.dumps(observation, sort_keys=True)))
    assert process.returncode == 0, observation
    assert summary["scope"] == dict(target_record_count=size, loaded_record_count=size, context_record_count=0, target_dataset_version="m")
    usage = summary["resource_usage"]
    assert (usage["admitted_node_count"], usage["admitted_edge_count"], usage["stored_root_membership_count"], usage["root_union_visit_count"]) == (size, size - 1, size, size - 1)
    assert usage["exhausted_limit"] is usage["attempted_value"] is None
    assert summary["execution_status"] == "completed"
    assert [summary[key] for key in ("grounded", "closed", "unresolved", "distinct_roots", "hhi", "effective_roots", "depth", "cycle_count")] == [size, 0, 0, 1, 1.0, 1.0, size - 1, 0]
    assert inputs == {path.name: dict(bytes=path.stat().st_size, sha256=hashlib.sha256(path.read_bytes()).hexdigest()) for path in paths}


def test_high_fan_in_lineage_complete_reports(phase4_step10_measure_reports, tmp_path, request):
    width = 64
    args, paths = _inputs(tmp_path / "fan-in-inputs", width=width)
    reports, _ = phase4_step10_measure_reports("lineage_fan_in_64", args, paths,
        record_count=2 * width, trace_allocations=False, timeout_seconds=180)
    _assert_reports(reports, request, nodes=2 * width, edges=width ** 2, targets=width, contexts=width,
        memberships=width * (width + 1), visits=width ** 2, roots=width, depth=1)


if __name__ == "__main__":
    import sys
    _api_worker(Path(sys.argv[1]))
