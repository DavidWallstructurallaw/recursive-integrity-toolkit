"""Retained Phase 3 Hero calculations and Phase 4 complete report observations."""
from fractions import Fraction
import hashlib


def test_phase3_hero_input_and_calculation_runtime(phase3_hero_pipeline, phase3_measure, repo_root):
    hero = repo_root / "examples/hero"
    before = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in hero.iterdir() if p.is_file()}
    result = phase3_measure("hero_input_plus_calculations", phase3_hero_pipeline, record_count=16,
        includes="input loading/validation, representation, single-version metrics, provenance, direct bounds, exact duplicates, tail and explicit pair",
        excludes="JSON/Markdown report assembly, redaction, audit CLI, lineage, simulation")
    assert result["pair"].support_delta.value == -3
    assert result["pair"].support_retention_ratio.value == float(Fraction(5, 8))
    assert result["bundle"].observability.maximum_level == 4 and not result["bundle"].has_errors
    assert before == {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in hero.iterdir() if p.is_file()}


def test_phase4_step10_hero_complete_report_runtime(phase4_step10_measure_reports, repo_root):
    """Observe every cold-process attempt through both published report formats."""
    import json

    hero = repo_root / "examples/hero"
    names = ("records_v2.csv", "records_v1.csv", "provenance.csv", "config.json", "version_order.json")
    flags = ("--records", "--compare", "--provenance", "--config", "--version-order")
    arguments = [item for flag, name in zip(flags, names) for item in (flag, str(hero / name))]
    arguments += ["--state-semantics", "literal Hero topic categories"]
    reports, observations = phase4_step10_measure_reports("hero_complete_reports", arguments,
        [hero / name for name in names], record_count=16, untraced_attempts=3)
    for path in reports:
        report = json.loads(path.read_bytes())
        assert report["run"]["run_status"] == "complete" and not report["errors"]
        metrics = report["derived_metrics"]
        assert [metrics["support"]["by_version"][version]["support_size"]["value"]
                for version in ("v1", "v2")] == [8, 5]
        assert [metrics["diversity"]["by_version"][version]["gini_simpson_diversity"]["value"]
                for version in ("v1", "v2")] == [float(Fraction(7, 8)), float(Fraction(3, 4))]
        assert metrics["support"]["support_delta"]["value"] == -3
        assert metrics["support"]["support_retention_ratio"]["value"] == float(Fraction(5, 8))
        direct = metrics["closure_exposure"]["direct"]
        assert [direct[name]["value"] for name in ("lower_bound", "upper_bound", "interval_width")] == [.5, .5, 0.]
        assert report["capabilities"]["lineage"]["execution_status"] == "not_requested"
        assert report["simulations"] == {}
    assert [item["mode"] for item in observations] == ["untraced"] * 3 + ["traced"]
    # A noisy CI observation is not a universal laptop SLA. Every target miss
    # remains visible for explicit acceptance review, without best-run selection.


def test_hero_lineage_complete_report_runtime(phase4_step10_measure_reports, repo_root):
    """Measure current opt-in Hero end to end, preserving all three attempts."""
    import json

    hero = repo_root / "examples/hero"
    names = ("records_v2.csv", "records_v1.csv", "provenance.csv", "config.json", "version_order.json")
    flags = ("--records", "--compare", "--provenance", "--config", "--version-order")
    arguments = [item for flag, name in zip(flags, names) for item in (flag, str(hero / name))]
    arguments += ["--state-semantics", "literal Hero topic categories", "--lineage"]
    reports, observations = phase4_step10_measure_reports("hero_lineage_complete_reports", arguments,
        [hero / name for name in names], record_count=16, untraced_attempts=3, trace_allocations=False)
    for path in reports:
        report = json.loads(path.read_bytes())
        assert report["run"]["run_status"] == "complete" and not report["errors"]
        assert report["capabilities"]["lineage"]["execution_status"] == "completed"
        metrics = report["derived_metrics"]["lineage"]
        assert [metrics[name]["value"] for name in ("grounded_record_count", "closed_record_count",
            "unresolved_record_count", "distinct_external_root_count", "ancestry_concentration_hhi",
            "effective_external_root_count")] == [8, 0, 0, 5, .25, 4.0]
        bounds = report["derived_metrics"]["closure_exposure"]
        assert [bounds["lineage"][name]["value"] for name in ("lower_bound", "upper_bound")] == [0.0, 0.0]
        assert [bounds["direct"][name]["value"] for name in ("lower_bound", "upper_bound")] == [.5, .5]
    assert [item["mode"] for item in observations] == ["untraced"] * 3
    # The recorded outer times are reviewed against the reference under-5s
    # target. A shared-runner miss is visible, never replaced with the best run.
