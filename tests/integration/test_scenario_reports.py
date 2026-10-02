"""Scenario presentation preserves supplied evidence and protected identities."""
import json
import re

import numpy as np
import pytest

from recursive_integrity_toolkit.io.validation import validate_bundle
from recursive_integrity_toolkit.metrics import resampling
from recursive_integrity_toolkit.models import (
    AuditBundle, CalculationScope, FileRole, InputSource, RecordKey, RepresentationDescriptor,
    ScenarioParameters,
)
from recursive_integrity_toolkit.reports.assembly import assemble_report, privacy_view
from recursive_integrity_toolkit.reports.json_report import render_json
from recursive_integrity_toolkit.reports.markdown_report import render_markdown
from recursive_integrity_toolkit.result import validate_report
from recursive_integrity_toolkit.utils.hashing import IdentifierProtection


CLOSED = "closed_resampling"
REOPENED = "reopened_resampling"
PRIVATE_STATE = "PRIVATE_STATE_`|<script>"
PRIVATE_OTHER = "PRIVATE_OTHER_STATE"
PRIVATE_SCOPE = "PRIVATE_SCENARIO_SCOPE"
PRIVATE_VERSION = "PRIVATE_SCENARIO_VERSION"
PRIVATE_SEMANTICS = "PRIVATE_SCENARIO_MEANING_`|<script>"
SECRET = b"scenario-report-privacy-test-secret"


def _report(tmp_path, *, models=(CLOSED, REOPENED), steps=3, replicates=2,
            states=None, external=None, weight=.5, semantics=PRIVATE_SEMANTICS, record_keys=()):
    states = states if states is not None else ((PRIVATE_STATE, .5), (PRIVATE_OTHER, .5))
    external = external if external is not None else tuple((state, probability) for state, probability in states)
    scenarios = tuple(ScenarioParameters(model, resample_size=4, simulation_horizon=steps,
        simulation_replicates=replicates, state_distribution=states,
        external_input_distribution=external if model == REOPENED else None,
        reopening_weight=weight if model == REOPENED else None) for model in models)
    request = resampling.ScenarioExperimentRequest(scenarios,
        CalculationScope((PRIVATE_VERSION,), record_keys, (), "explicit_scenario_probability_vector", PRIVATE_SCOPE),
        RepresentationDescriptor("topic", "topic_field", "v1", "literal_field_value", field_name="topic"),
        semantics, 29)
    result = resampling.run_scenario_experiment(request)
    path = tmp_path / "records.jsonl"
    path.write_text(json.dumps({"dataset_version": "v1", "record_id": "r1", "content": "synthetic"}) + "\n")
    bundle = validate_bundle(AuditBundle((InputSource(FileRole.RECORDS_PRIMARY, path),)))
    nullable = ("started_at", "completed_at", "duration_seconds", "python_version", "platform", "command", "config_hash")
    run = {"run_id": "scenario-report", "toolkit_version": "0.1.0.dev6",
        "report_schema_version": "1.3", **dict.fromkeys(nullable), "random_seed": 29,
        "strict_mode": False, "redacted_mode": False, "network_call_count": 0,
        "deterministic": True, "privacy_mode": "standard", "run_status": "complete",
        "null_reasons": {name: "not_recorded" for name in nullable}}
    return assemble_report(bundle, run=run, scenario_experiment=result)


def _view(report, *, mode="standard", record_id_mode=None):
    return privacy_view(report, mode=mode, record_id_mode=record_id_mode,
        protection=IdentifierProtection(secret=SECRET))


def _numbers(value, path=()):
    if type(value) in (int, float):
        yield path, value
    elif type(value) is dict:
        for key, item in value.items():
            yield from _numbers(item, (*path, key))
    elif type(value) is list:
        for index, item in enumerate(value):
            yield from _numbers(item, (*path, index))


@pytest.mark.parametrize("record_id_mode", ["preserve", "hash", "omit"])
def test_scenario_privacy_preserves_state_alignment_in_all_record_modes(tmp_path, record_id_mode, monkeypatch):
    # An initially absent state enters, disappears and enters again. It must keep
    # one identity across sources, repeated events, both models and comparison.
    draws = iter(((4, 0), (4, 0), (4, 0), (0, 4), (4, 0), (0, 4)))
    monkeypatch.setattr(resampling, "_sample_counts", lambda *_: next(draws))
    states = (("a_PRIVATE", 1.), ("b_PRIVATE", 0.))
    report = _report(tmp_path, states=states, external=(("a_PRIVATE", .5), ("b_PRIVATE", .5)),
        replicates=1, weight=1.)
    original = report.to_dict()
    view = _view(report, mode="redacted", record_id_mode=record_id_mode)
    protected = json.loads(render_json(view))
    markdown = render_markdown(view)
    validate_report(protected)
    for private in ("a_PRIVATE", "b_PRIVATE", PRIVATE_SCOPE, PRIVATE_VERSION, PRIVATE_SEMANTICS):
        assert private not in json.dumps(protected) and private not in markdown
    assert dict(_numbers(protected["simulations"])) == dict(_numbers(original["simulations"]))
    closed = protected["simulations"][CLOSED]
    reopened = protected["simulations"]["external_reopening"]
    order = reopened["parameters"]["state_order"]
    assert order == closed["parameters"]["state_order"]
    assert order == closed["analytic_baseline"]["parameters"]["state_order"]
    assert [row["state_id"] for row in reopened["external_input_distribution"]] == order
    assert [row["state_id"] for row in reopened["input_normalization"]["probability_corrections"]] == order
    for source in reopened["mixed_sources"]:
        assert [row["state_id"] for row in source["input_normalization"]["effective_distribution"]] == order
    assert [event["state_id"] for event in reopened["state_reentry_events"]] == [order[1], order[0], order[1]]
    assert [event["state_id"] for event in reopened["extinction_events"]] == [order[0], order[1], order[0]]
    reachability = reopened["scenario_comparison"]["initial_reachability"]
    assert reachability[0]["reachable_states"] == [order[0]]
    assert reachability[1]["reachable_states"] == order
    assert reachability[1]["possible_reentry_states"] == [order[1]]
    assert reopened["sampled_paths"][0]["generations"][1]["support"] == [order[1]]
    assert closed["scope"]["scope_id"] == reopened["scope"]["scope_id"]
    assert closed["state_semantics"] == reopened["state_semantics"] != PRIVATE_SEMANTICS
    assert report.to_dict() == original


def test_owner_assumptions_remain_readable_and_caller_meaning_never_bypasses_privacy(tmp_path):
    phrase = "Fixed finite declared state space and constant positive integer resample size."
    report = _report(tmp_path, semantics=phrase)
    for mode in ("standard", "redacted"):
        payload = _view(report, mode=mode).to_dict()
        for node in payload["simulations"].values():
            assert phrase in node["assumptions"]
            assert node["state_semantics"] == phrase if mode == "standard" else node["state_semantics"] != phrase
            assert all("private_" not in text for row in node["assumption_table"] for text in row.values())
        reopened = payload["simulations"]["external_reopening"]
        assert "External independence, reliability and relevance are supplied assumptions, not verified facts." in reopened["limitations"]
        assert "No pooled summary, significance, causal benefit or external-quality ranking is established." in reopened["scenario_comparison"]["limitations"]


@pytest.mark.parametrize("models", [(CLOSED,), (REOPENED,), (CLOSED, REOPENED)])
def test_simulation_markdown_distinguishes_sources_samples_and_baseline(tmp_path, models):
    view = _view(_report(tmp_path, models=models))
    text = render_markdown(view)
    assert "### Experimental simulation" in text
    assert "Simulation step" in text and "Scenario assumptions" in text
    assert "Realized count" in text and "State frequency" in text
    assert ("Distinct closed analytic baseline" in text) == (CLOSED in models)
    assert ("**Pre-draw source probabilities**" in text) == (REOPENED in models)
    assert ("Per-path comparison" in text) == (len(models) == 2)
    assert ("Diversity difference (reopened_minus_closed)" in text) == (len(models) == 2)
    assert "<script>" not in text and "\\u003cscript\\u003e" in text
    assert json.loads(render_json(view)) == view.to_dict()


def test_every_scenario_detail_table_has_at_most_100_rows_and_truthful_omissions(tmp_path, monkeypatch):
    draws = iter((0, 4) if step % 2 == 0 else (4, 0) for step in range(103))
    monkeypatch.setattr(resampling, "_sample_counts", lambda *_: next(draws))
    view = _view(_report(tmp_path, models=(REOPENED,), steps=103, replicates=1,
        states=(("a", 1.), ("b", 0.)), external=(("a", .5), ("b", .5)), weight=1.))
    text = render_markdown(view)
    assert "Displayed 100 of 104 rows; omitted 4 rows." in text
    assert "Displayed 100 of 103 rows; omitted 3 rows." in text
    assert "Displayed 100 of 208 rows; omitted 108 rows." in text
    assert "Displayed 100 of 206 rows; omitted 106 rows." in text
    tables = re.findall(r"(?m)(?:^\|.*\n)+", text)
    assert tables and all(len(table.splitlines()) - 2 <= 100 for table in tables)
    payload = json.loads(render_json(view))["simulations"]["external_reopening"]
    assert len(payload["sampled_paths"][0]["generations"]) == 104
    assert len(payload["mixed_sources"]) == 103
    assert len(payload["extinction_events"]) == 103
    assert len(payload["state_reentry_events"]) == 103


def test_large_state_vectors_do_not_expand_trajectory_cells(tmp_path):
    states = tuple((f"s{index:04}", 1 / 1024) for index in range(1024))
    view = _view(_report(tmp_path, states=states, models=(REOPENED,), steps=0, replicates=1))
    text = render_markdown(view)
    assert "Displayed 100 of 1024 rows; omitted 924 rows." in text
    trajectory = text.split("**Sampled trajectory**", 1)[1].split("**Realized sample detail**", 1)[0]
    assert "s0000" not in trajectory and "s1023" not in trajectory
    assert max(map(len, text.splitlines())) < 1500
    assert len(json.loads(render_json(view))["simulations"]["external_reopening"]["initial_distribution"]) == 1024


def test_tiny_positive_probability_survives_rendering(tmp_path):
    view = _view(_report(tmp_path, models=(REOPENED,), steps=0, replicates=1,
        states=(("a", 1.), ("tiny", 5e-324))))
    text = render_markdown(view)
    assert "5e-324" in text
    rows = json.loads(render_json(view))["simulations"]["external_reopening"]["initial_distribution"]
    assert rows[1]["probability"] == 5e-324 > 0


def test_explicit_scenario_scope_record_details_remain_bounded(tmp_path):
    identities = tuple(RecordKey(PRIVATE_VERSION, f"r{index:04}") for index in range(103))
    view = _view(_report(tmp_path, models=(CLOSED,), steps=0, replicates=1,
        states=(("a", 1.),), record_keys=identities))
    text = render_markdown(view)
    assert "Displayed 100 of 103 rows; omitted 3 rows." in text
    tables = re.findall(r"(?m)(?:^\|.*\n)+", text)
    assert all(len(table.splitlines()) - 2 <= 100 for table in tables)
    closed = json.loads(render_json(view))["simulations"][CLOSED]
    assert closed["scope"]["record_count"] == 103
    assert len(closed["scope"]["included_record_keys"]) == 103


def test_privacy_and_rendering_never_dispatch_numerics_or_rng(tmp_path, monkeypatch):
    report = _report(tmp_path)
    def forbidden(*_args, **_kwargs):
        pytest.fail("Scenario presentation crossed into numerical execution")
    for name in ("run_scenario_experiment", "simulate_closed_resampling", "simulate_reopened_resampling",
                 "mix_external_input", "expected_diversity_after_steps", "_sample_counts"):
        monkeypatch.setattr(resampling, name, forbidden)
    monkeypatch.setattr(np.random, "PCG64", forbidden)
    for mode in ("standard", "redacted"):
        view = _view(report, mode=mode)
        assert render_json(view) and render_markdown(view)
