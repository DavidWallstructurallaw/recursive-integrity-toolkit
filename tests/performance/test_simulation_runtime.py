"""Bounded explicit scenarios measured through complete audit publication."""
from __future__ import annotations

from fractions import Fraction
import json

import pytest


CLOSED = "closed_resampling"
REOPENED = "external_reopening"


def _inputs(tmp_path, repo_root, profile):
    example = repo_root / "examples/simulation"
    configuration = json.loads((example / "config.json").read_bytes())
    scenario = configuration["simulation"]
    if profile == "representative":
        states = [f"state-{index:02d}" for index in range(32)]
        scenario.update(state_distribution={state: 1 / 16 if index < 16 else 0
                                            for index, state in enumerate(states)},
            external_input_distribution={state: 0 if index < 16 else 1 / 16
                                         for index, state in enumerate(states)},
            resample_size=64, simulation_horizon=64, simulation_replicates=8,
            state_semantics="Literal fictional states for bounded performance observation",
            scope_id="bounded-performance-scenario")
    config = tmp_path / "config.json"
    config.write_text(json.dumps(configuration) + "\n", encoding="utf-8")
    records, provenance = (example / name for name in ("records.jsonl", "provenance.jsonl"))
    arguments = ["--records", str(records), "--provenance", str(provenance),
                 "--config", str(config), "--simulate"]
    return arguments, [records, provenance, config], scenario


def _probabilities(rows):
    return {row["state_id"]: row["probability"] for row in rows}


def _assert_report(path, scenario):
    report = json.loads(path.read_bytes())
    assert report["run"]["run_status"] == "complete" and not report["errors"]
    assert report["run"]["network_call_count"] == 0
    assert report["run"]["random_seed"] == scenario["seed"]
    assert report["capabilities"]["intervention_simulation"]["execution_status"] == "completed"
    # These are the actual audit records; scenario cells are never record IDs.
    assert report["observed_facts"]["record_counts"]["audit-v1"]["value"] == 2
    assert report["derived_metrics"]["diversity"]["by_version"]["audit-v1"]["gini_simpson_diversity"]["value"] == .5
    assert any(row["conclusion"] == "empirical_intervention_effect" and row["status"] == "unavailable"
               for row in report["unavailable_conclusions"])
    assert set(report["simulations"]) == {CLOSED, REOPENED}
    order = sorted(scenario["state_distribution"])
    k, h, repeats, n = len(order), scenario["simulation_horizon"], scenario["simulation_replicates"], scenario["resample_size"]
    initial = [Fraction(scenario["state_distribution"][state]) for state in order]
    external = [Fraction(scenario["external_input_distribution"][state]) for state in order]
    weight = Fraction(scenario["reopening_weight"])
    for name, node in report["simulations"].items():
        assert node["status"] == "experimental" and node["evidence_class"] == "simulation"
        assert node["parameters"]["state_order"] == order
        assert node["parameters"]["random_seed"] == scenario["seed"]
        assert node["scope"]["record_count"] == 0
        assert node["scope"]["included_record_keys"] == node["scope"]["excluded_record_keys"] == []
        assert node["denominator"] == n
        assert _probabilities(node["initial_distribution"]) == scenario["state_distribution"]
        assert len(node["sampled_paths"]) == repeats
        extinctions, reentries = [], []
        sources = {(row["replicate_index"], row["step"]): row for row in node.get("mixed_sources", [])}
        if name == REOPENED:
            assert len(sources) == repeats * h
            assert _probabilities(node["external_input_distribution"]) == scenario["external_input_distribution"]
        for replicate, sampled in enumerate(node["sampled_paths"]):
            assert sampled["replicate_index"] == replicate
            generations = sampled["generations"]
            assert len(generations) == h + 1
            previous = initial
            for step, row in enumerate(generations):
                assert row["step"] == step and len(row["state_frequencies"]) == k
                if step == 0:
                    assert row["state_counts"] is None
                    frequencies = initial
                else:
                    counts = row["state_counts"]
                    assert len(counts) == k and all(type(count) is int and count >= 0 for count in counts)
                    assert sum(counts) == n
                    frequencies = [Fraction(count, n) for count in counts]
                    for state, before, after in zip(order, previous, frequencies, strict=True):
                        if before > 0 and after == 0:
                            extinctions.append((replicate, step, state))
                        if before == 0 and after > 0:
                            reentries.append((replicate, step, state))
                    if name == REOPENED:
                        source = sources[replicate, step]
                        expected = [(1 - weight) * old + weight * supplied
                                    for old, supplied in zip(previous, external, strict=True)]
                        normalization = source["input_normalization"]
                        assert len(normalization["effective_distribution"]) == k
                        assert _probabilities(normalization["effective_distribution"]) == dict(zip(order, map(float, expected), strict=True))
                        assert source["possible_reentry_states"] == [state for state, old, new in
                            zip(order, previous, expected, strict=True) if old == 0 and new > 0]
                    else:
                        assert all(old > 0 or new == 0 for old, new in zip(previous, frequencies, strict=True))
                assert row["state_frequencies"] == list(map(float, frequencies))
                assert row["support"] == [state for state, value in zip(order, frequencies, strict=True) if value > 0]
                assert row["support_size"] == len(row["support"])
                assert row["gini_simpson_diversity"] == float(1 - sum(value * value for value in frequencies))
                previous = frequencies
        identities = lambda rows: [(row["replicate_index"], row["step"], row["state_id"]) for row in rows]
        assert identities(node["extinction_events"]) == extinctions
        if name == REOPENED:
            assert identities(node["state_reentry_events"]) == reentries
        else:
            assert not reentries
            expected_initial = 1 - sum(value * value for value in initial)
            assert node["analytic_baseline"]["expected_diversity"] == pytest.approx([
                float(expected_initial * Fraction(n - 1, n) ** step) for step in range(h + 1)])
    comparison = report["simulations"][REOPENED]["scenario_comparison"]
    assert len(comparison["rows"]) == repeats * (h + 1)
    assert comparison["difference_direction"] == "reopened_minus_closed"
    markdown = path.with_suffix(".md").read_text(encoding="utf-8")
    for total in (repeats * (h + 1), repeats * (h + 1) * k, repeats * h * k):
        assert f"Displayed {min(total, 100)} of {total} rows; omitted {max(total - 100, 0)} rows. Full evidence is retained in JSON." in markdown
    return report["simulations"]


@pytest.mark.parametrize("profile,attempts", [("small", 3), ("representative", 1)])
def test_simulation_complete_reports(phase4_step10_measure_reports, tmp_path, repo_root, profile, attempts):
    """Every attempt includes actual sampling and complete JSON/Markdown output."""
    arguments, paths, scenario = _inputs(tmp_path, repo_root, profile)
    k = len(scenario["state_distribution"])
    cells = len(scenario["models"]) * k * (scenario["simulation_horizon"] + 1) * scenario["simulation_replicates"]
    reports, observations = phase4_step10_measure_reports(f"simulation_{profile}", arguments, paths,
        record_count=2, untraced_attempts=attempts, trace_allocations=False,
        timeout_seconds=180, profile_simulation=True, workload_details=dict(
            profile=profile, declared_state_count=k, models=scenario["models"],
            resample_size=scenario["resample_size"], simulation_horizon=scenario["simulation_horizon"],
            simulation_replicates=scenario["simulation_replicates"], seed=scenario["seed"],
            reopening_weight=scenario["reopening_weight"], admitted_state_cells=cells,
            admission_limit=1_000_000, actual_audit_record_count=2))
    previous = None
    for path, observation in zip(reports, observations, strict=True):
        assert observation["tracing"] is False
        assert len(observation["simulation_elapsed_seconds"]) == 1
        assert 0 <= observation["simulation_elapsed_seconds"][0] <= observation["cli_elapsed_seconds"] <= observation["subprocess_wall_seconds"]
        assert observation["rss_peak_after_cli_bytes"] >= observation["rss_peak_before_cli_bytes"] > 0
        actual = _assert_report(path, scenario)
        if previous is not None:
            # Fresh processes share the same pinned local environment. No
            # cross-NumPy or cross-platform trajectory equality is asserted.
            assert actual == previous
        previous = actual
