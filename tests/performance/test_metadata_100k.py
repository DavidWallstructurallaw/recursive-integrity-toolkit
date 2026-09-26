"""Retained Phase 3 calculations and Phase 4 complete 100k metadata audit.

Performance observations are diagnostics, not a whole-report SLA. Synthetic input
construction is recorded separately. No user data or sparse lineage is involved.
"""
from fractions import Fraction
import sys
import pytest

from recursive_integrity_toolkit.config import RepresentationConfig
from recursive_integrity_toolkit.io.normalization import normalize_row
from recursive_integrity_toolkit.io.validation import join_provenance
from recursive_integrity_toolkit.metrics.diversity import calculate_state_distribution
from recursive_integrity_toolkit.metrics.duplicates import detect_exact_duplicates
from recursive_integrity_toolkit.metrics.provenance import summarize_provenance
from recursive_integrity_toolkit.models import CalculationScope, ContentMode
from recursive_integrity_toolkit.representations.field import assign_field_states


def _synthetic(size):
    records = tuple(normalize_row(dict(dataset_version="synthetic-v1", record_id=f"r{i:06d}",
        content=f"synthetic text {i % 1000:04d}", topic=f"state-{i % 100:03d}"), kind="records") for i in range(size))
    provenance = tuple(normalize_row(dict(dataset_version="synthetic-v1", record_id=f"r{i:06d}",
        source_type="human" if i % 2 == 0 else "synthetic", provenance_confidence="confirmed",
        external_grounding="yes" if i % 2 == 0 else "no"), kind="provenance") for i in range(size))
    return records, provenance


def _duplicates(records):
    return detect_exact_duplicates(records, dataset_versions=("synthetic-v1",), scope_id="100k-exact",
        representation_name="record_form", representation_version="exact-v1", normalization_profile="exact_utf8_v1", content_mode=ContentMode.INLINE)


def test_phase3_metadata_100k_measured_calculations(phase3_measure):
    size = 100000
    records, provenance = phase3_measure("metadata_100k_setup", lambda: _synthetic(size), record_count=size, purpose="synthetic normalization only")
    before = tuple((r.record_key, tuple(r.values.items())) for r in records)
    representation = phase3_measure("metadata_100k_field_representation", lambda: assign_field_states(records,
        dataset_versions=("synthetic-v1",), scope_id="100k-topic",
        config=RepresentationConfig("topic", "topic_field", "topic", "synthetic-topic-v1", "error")), record_count=size)
    distribution = phase3_measure("metadata_100k_support_diversity", lambda: calculate_state_distribution(representation), record_count=size)
    # Authored independent exact oracle: 100 equiprobable states, 1000 records each.
    assert distribution.unweighted.support_size.value == 100
    assert all(s.state_count == 1000 and s.state_frequency == .01 for s in distribution.unweighted.states)
    assert abs(distribution.unweighted.gini_simpson_diversity.value - float(Fraction(99, 100))) <= 1e-12
    joined = phase3_measure("metadata_100k_provenance_join", lambda: join_provenance(records, provenance), record_count=size)
    scope = CalculationScope(("synthetic-v1",), joined.scope_record_keys, (), joined.provenance_row_coverage.denominator_name, "100k-provenance")
    composition = phase3_measure("metadata_100k_composition", lambda: summarize_provenance(joined, scope=scope), record_count=size)
    assert dict(composition.source.counts) == dict(human=50000, synthetic=50000, mixed=0, sensor=0, unknown=0)
    assert dict(composition.source.shares) == dict(human=.5, synthetic=.5, mixed=0., sensor=0., unknown=0.)
    assert composition.provenance_required_field_coverage.numerator == size and not composition.input_has_errors
    duplicates = phase3_measure("metadata_100k_exact_duplicates", lambda: _duplicates(records), record_count=size)
    # 1000 exact forms, each appearing 100 times: 1000*(100-1) duplicates.
    assert duplicates.duplicate_group_count.value == 1000 and duplicates.duplicate_record_count.value == 99000
    assert len(records) == len(provenance) == size
    assert before == tuple((r.record_key, tuple(r.values.items())) for r in records)


@pytest.mark.parametrize("pattern", ["same", "unique", "groups"])
def test_phase3_duplicate_path_operation_growth_is_not_quadratic(pattern):
    """Count actual Python line events, independent of noisy wall-clock ratios.

    This regression covers current duplicate/representation/key code paths. It
    complements review of bucket grouping; it is not a proof for every input.
    """
    measurements = []
    for size in (256, 1024):
        rows = tuple(normalize_row(dict(dataset_version="synthetic-v1", record_id=f"r{i:06d}",
            content=("same synthetic payload" if pattern == "same" else f"synthetic payload {i if pattern == 'unique' else i % 16}")), kind="records") for i in range(size))
        counter = [0]
        def trace(frame, event, arg):
            if event == "line" and "recursive_integrity_toolkit" in frame.f_code.co_filename:
                counter[0] += 1
            return trace
        previous = sys.gettrace()
        try:
            sys.settrace(trace)
            result = _duplicates(rows)
        finally:
            sys.settrace(previous)
        assert result.duplicate_record_count.value == size - (1 if pattern == "same" else size if pattern == "unique" else 16)
        measurements.append(counter[0])
    assert 0 < measurements[0] < measurements[1]
    assert measurements[1] <= 6 * measurements[0], measurements


def _phase4_step10_metadata_inputs(directory, size=100000):
    """Deterministic five-class metadata with 10% absent provenance rows.

    A constant required content field is carried but never analyzed. No
    randomness, parent graph, similarity or sparse-lineage work is requested.
    Divisibility by 100 keeps the independent aggregate arithmetic exact.
    """
    import csv
    import json
    import time

    assert size > 0 and size % 100 == 0
    start = time.perf_counter()
    records, provenance, config = (directory / name for name in ("records.csv", "provenance.csv", "config.json"))
    sources = ("human", "synthetic", "mixed", "sensor", "unknown")
    with records.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(("dataset_version", "record_id", "topic", "content"))
        writer.writerows(("m", f"{i:06d}", f"s{i % 100:02d}", "synthetic metadata") for i in range(size))
    with provenance.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(("dataset_version", "record_id", "source_type", "provenance_confidence", "external_grounding"))
        for i in range(size):
            if i % 10 == 9:
                continue
            source = sources[(i // 10) % 5]
            grounding = "yes" if source in ("human", "sensor") else "no" if source == "synthetic" else "unknown"
            writer.writerow(("m", f"{i:06d}", source, "confirmed", grounding))
    config.write_text(json.dumps({"representation": {"name": "topic", "source": "topic_field",
        "field": "topic", "version": "synthetic-topic-v1", "missing_value_policy": "error"}},
        sort_keys=True) + "\n", encoding="utf-8")
    return (["--records", str(records), "--provenance", str(provenance), "--config", str(config)],
            [records, provenance, config], time.perf_counter() - start)


def _phase4_step10_assert_metadata_report(path, size=100000):
    """Arithmetic authored from the generator, without invoking metric helpers."""
    import json

    report = json.loads(path.read_bytes())
    assert report["run"]["run_status"] == "complete" and not report["errors"]
    metrics = report["derived_metrics"]
    assert metrics["support"]["by_version"]["m"]["support_size"]["value"] == 100
    assert abs(metrics["diversity"]["by_version"]["m"]["gini_simpson_diversity"]["value"] - float(Fraction(99, 100))) <= 1e-12
    assert report["observed_facts"]["state_counts"]["by_version"]["m"]["value"] == [
        {"state_id": f"s{i:02d}", "state_count": size // 100} for i in range(100)]
    facts = report["observed_facts"]["provenance"]
    assert facts["source_type_counts"]["value"] == {source: size * 18 // 100
        for source in ("human", "synthetic", "mixed", "sensor", "unknown")}
    assert metrics["provenance"]["source_type_shares"]["value"] == {source: .18
        for source in ("human", "synthetic", "mixed", "sensor", "unknown")}
    assert facts["missing_provenance_count"]["value"] == size // 10
    assert metrics["provenance"]["missing_provenance_share"]["value"] == .1
    assert facts["records_with_matching_rows"]["value"] == size * 9 // 10
    for name in ("provenance_row_coverage", "provenance_required_field_coverage"):
        assert facts[name]["value"] == .9 and facts[name]["denominator"] == size
    assert [facts[name]["value"] for name in ("known_open_count", "known_closed_count", "unresolved_grounding_count")] == [size * 36 // 100, size * 18 // 100, size * 46 // 100]
    direct = metrics["closure_exposure"]["direct"]
    assert [direct[name]["value"] for name in ("lower_bound", "upper_bound", "interval_width")] == [.18, .64, .46]
    assert report["capabilities"]["lineage"]["execution_status"] == "not_requested"
    assert report["capabilities"]["content_diagnostics"]["execution_status"] == "completed"
    assert report["capabilities"]["content_diagnostics"]["execution_scope"] == ["supplied_distribution:audit-representation"]
    assert set(metrics) == {"closure_exposure", "diversity", "provenance", "support"}
    assert report["simulations"] == {}


def test_phase4_step10_metadata_100k_complete_report_runtime(phase4_step10_measure_reports, tmp_path, request):
    """Observe the required 100k metadata audit through published JSON/Markdown."""
    import json

    arguments, inputs, setup_seconds = _phase4_step10_metadata_inputs(tmp_path)
    request.node.user_properties.append(("phase4_performance_setup", json.dumps(dict(
        name="metadata_100k_csv_construction", elapsed_seconds=setup_seconds, record_count=100000,
        measured_audit_excludes_setup=True), sort_keys=True)))
    reports, _ = phase4_step10_measure_reports("metadata_100k_complete_reports", arguments,
        inputs, record_count=100000, timeout_seconds=1800, trace_allocations=False)
    for path in reports:
        _phase4_step10_assert_metadata_report(path)


def test_phase4_step10_partial_report_output_growth_is_bounded(tmp_path, capsys, request):
    """Fourfold data growth cannot duplicate the whole scope per warning."""
    import json
    from recursive_integrity_toolkit.cli import main

    observations = []
    for size in (100, 400):
        directory = tmp_path / str(size)
        directory.mkdir()
        arguments, _, _ = _phase4_step10_metadata_inputs(directory, size)
        output = directory / "out"
        assert main(["audit", *arguments, "--out", str(output)]) == 0
        streams = capsys.readouterr()
        _phase4_step10_assert_metadata_report(output / "report.json", size)
        report = json.loads((output / "report.json").read_bytes())
        # Each missing row retains generation, input-join and provenance contexts.
        assert len(report["warnings"]) == size * 66 // 100
        assert [json.loads(line) for line in streams.err.splitlines()] == report["warnings"]
        assert len(report["inputs"]["scope"]["included_record_keys"]) == size
        assert all("included_record_keys" not in item["affected_scope"] for item in report["warnings"])
        observations.append({"records": size, "warnings": len(report["warnings"]),
            "json_bytes": (output / "report.json").stat().st_size,
            "markdown_bytes": (output / "report.md").stat().st_size,
            "stderr_bytes": len(streams.err.encode("utf-8"))})
    request.node.user_properties.append(("phase4_report_growth", json.dumps(observations, sort_keys=True)))
    for key in ("json_bytes", "markdown_bytes", "stderr_bytes"):
        assert 0 < observations[0][key] < observations[1][key] <= 6 * observations[0][key], observations


def test_phase4_step10_duplicate_report_scope_is_indexed_once_and_boundaries_survive():
    """Grouped duplicate reports reuse scope membership without relaxing checks."""
    import builtins
    from dataclasses import replace
    from types import FunctionType
    from recursive_integrity_toolkit.models import RecordKey
    from recursive_integrity_toolkit.reports import assembly

    for size in (100, 400):
        records = tuple(normalize_row(dict(dataset_version="synthetic-v1", record_id=f"r{i:06d}",
                        content=f"synthetic pair {i // 2}"), kind="records") for i in range(size))
        result = _duplicates(records)
        constructions = []
        def counted_set(values=()):
            if values is result.scope.included_record_keys:
                constructions.append(len(values))
            return builtins.set(values)
        # Clone only the adapter globals so unrelated set use is not intercepted.
        namespace = dict(assembly._duplicates.__globals__, set=counted_set)
        adapter = FunctionType(assembly._duplicates.__code__, namespace)
        payload = {"observed_facts": {}}
        adapter(payload, result, None)
        assert constructions == [size]
        content = payload["observed_facts"]["content"]
        assert content["duplicate_group_count"]["value"] == size // 2
        assert content["duplicate_record_count"]["value"] == size // 2
        groups = content["exact_duplicate_groups"]["value"]
        assert [entry["record_keys"] for entry in groups] == [[
            {"dataset_version": key.dataset_version, "record_id": key.record_id} for key in group.record_keys]
            for group in result.exact_duplicate_groups]
        first, second, *remaining = result.exact_duplicate_groups
        overlap = replace(second, record_keys=first.record_keys)
        outside = replace(first, record_keys=(first.record_keys[0], RecordKey("synthetic-v1", "outside")))
        for changed in ((first, overlap, *remaining), (outside, second, *remaining)):
            with pytest.raises(assembly.ReportAssemblyError, match="overlap or leave their scope"):
                adapter({"observed_facts": {}}, replace(result, exact_duplicate_groups=changed), None)
