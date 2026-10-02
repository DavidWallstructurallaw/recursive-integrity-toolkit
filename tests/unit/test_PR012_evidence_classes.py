"""Phase 1 placeholder for PR-012.

Planned scope:
    Future evidence-class tests are deferred to Phase 4.

Current Phase 1 scope:
    Verify the approved owner ID and confirm that the target module remains a
    docstring-only, import-safe placeholder.

Limits:
    No mathematical metric, data loading, graph operation, or report result is tested.
"""


def phase4_step2_evidence_report_fixture():
    """Independent literal control data, never generated from production code."""
    return {
        "run": {
            "run_id": "independent-evidence-case", "toolkit_version": "0.1.0.dev2",
            "report_schema_version": "1.1", "started_at": None, "completed_at": None,
            "duration_seconds": None, "python_version": None, "platform": None,
            "command": None, "config_hash": None, "random_seed": None,
            "strict_mode": False, "redacted_mode": False, "network_call_count": 0,
            "deterministic": True, "privacy_mode": "standard", "run_status": "complete",
            "null_reasons": {
                "started_at": "Fixed contract fixture has no executed run.",
                "completed_at": "Fixed contract fixture has no executed run.",
                "duration_seconds": "Fixed contract fixture has no executed run.",
                "python_version": "No execution environment is asserted.",
                "platform": "No execution environment is asserted.",
                "command": "Direct contract construction, no command invoked.",
                "config_hash": "No resolved configuration was supplied.",
                "random_seed": "No stochastic scenario was requested.",
            },
        },
        "inputs": {}, "observability": {}, "capabilities": {}, "observed_facts": {},
        "derived_metrics": {}, "proxy_signals": {}, "simulations": {},
        "unavailable_conclusions": [], "recommended_next_metadata": [],
        "warnings": [], "errors": [],
    }


def phase4_step2_metric_fixture(*, observed=False):
    """A hand-worked count or Gini-Simpson zero on two identical state labels."""
    return {
        "value": 0,
        "unit": "records" if observed else "dimensionless",
        "evidence_class": "observed_fact" if observed else "derived_metric",
        "status": "available",
        "method_id": "PR-006.duplicate_record_count" if observed else "F-003",
        "owner_ids": ["PR-006"] if observed else ["T1"],
        "theory_map_ids": [],
        "trace_ids": [] if observed else ["T1"],
        "scope": {
            "dataset_versions": ["v1"], "record_count": 2, "excluded_record_count": 0,
            "denominator_basis": "included_records", "scope_id": "v1",
        },
        "representation": None if observed else {
            "representation_name": "topic", "representation_source": "field:topic", "representation_version": "1",
            "binning_or_mapping_rule": "identity", "field_name": "topic",
            "missing_value_policy": "error",
        },
        "coverage": 1.0,
        "coverage_reason": None,
        "denominator": 2,
        "denominator_reason": None,
        "assumptions": [],
        "limitations": ["Declared topic labels do not establish semantic truth."],
        "reason_codes": [],
        "required_evidence": [],
    }


def phase4_step2_metric_report_fixture(*, observed=False):
    payload = phase4_step2_evidence_report_fixture()
    if observed:
        payload["observed_facts"] = {
            "content": {"duplicate_record_count": phase4_step2_metric_fixture(observed=True)},
        }
    else:
        payload["derived_metrics"] = {"diversity": {"by_version": {"v1": {
            "gini_simpson_diversity": phase4_step2_metric_fixture(),
        }}}}
    return payload


def test_phase4_step2_count_and_diversity_have_independent_primary_classes():
    from recursive_integrity_toolkit.result import CanonicalReport

    observed = CanonicalReport.from_dict(phase4_step2_metric_report_fixture(observed=True)).to_dict()
    derived = CanonicalReport.from_dict(phase4_step2_metric_report_fixture()).to_dict()
    assert observed["observed_facts"]["content"]["duplicate_record_count"]["evidence_class"] == "observed_fact"
    assert derived["derived_metrics"]["diversity"]["by_version"]["v1"]["gini_simpson_diversity"]["evidence_class"] == "derived_metric"
    assert observed["derived_metrics"] == {}
    assert derived["observed_facts"] == {}


def test_phase4_step2_zero_is_an_available_value_and_never_missingness():
    from recursive_integrity_toolkit.result import CanonicalReport

    exported = CanonicalReport.from_dict(phase4_step2_metric_report_fixture()).to_dict()
    metric = exported["derived_metrics"]["diversity"]["by_version"]["v1"]["gini_simpson_diversity"]
    assert metric["value"] == 0
    assert type(metric["value"]) is int
    assert metric["status"] == "available"
    assert metric["reason_codes"] == []


def test_phase4_step2_unavailable_metric_is_null_with_blocking_evidence():
    import pytest

    from recursive_integrity_toolkit.result import CanonicalReport

    payload = phase4_step2_metric_report_fixture()
    metric = payload["derived_metrics"]["diversity"]["by_version"]["v1"]["gini_simpson_diversity"]
    metric.update({
        "value": None, "status": "unavailable", "reason_codes": ["R_REPRESENTATION_MISSING"],
        "required_evidence": ["An explicit state representation is required."],
        "representation": None,
    })
    exported = CanonicalReport.from_dict(payload).to_dict()
    assert exported["derived_metrics"]["diversity"]["by_version"]["v1"]["gini_simpson_diversity"]["value"] is None
    for field in ("reason_codes", "required_evidence"):
        saved = metric[field]
        metric[field] = []
        with pytest.raises(ValueError):
            CanonicalReport.from_dict(payload)
        metric[field] = saved
    metric["value"] = 0
    with pytest.raises(ValueError):
        CanonicalReport.from_dict(payload)


def test_phase4_step2_available_metric_cannot_silently_be_null():
    import pytest

    from recursive_integrity_toolkit.result import CanonicalReport

    payload = phase4_step2_metric_report_fixture()
    payload["derived_metrics"]["diversity"]["by_version"]["v1"]["gini_simpson_diversity"]["value"] = None
    with pytest.raises(ValueError):
        CanonicalReport.from_dict(payload)


def test_phase4_step2_evidence_classes_cannot_be_relabelled_in_place():
    import pytest

    from recursive_integrity_toolkit.result import CanonicalReport

    for observed in (True, False):
        for wrong_class in ("observed_fact", "derived_metric", "proxy_signal", "simulation",
                            "unavailable_conclusion", "unknown", None):
            expected_class = "observed_fact" if observed else "derived_metric"
            if wrong_class == expected_class:
                continue
            payload = phase4_step2_metric_report_fixture(observed=observed)
            metric = payload["observed_facts"]["content"]["duplicate_record_count"] if observed else (
                payload["derived_metrics"]["diversity"]["by_version"]["v1"]["gini_simpson_diversity"]
            )
            metric["evidence_class"] = wrong_class
            with pytest.raises(ValueError):
                CanonicalReport.from_dict(payload)


def test_phase4_step2_public_metric_cannot_move_to_another_section():
    import pytest

    from recursive_integrity_toolkit.result import CanonicalReport

    for section in ("observed_facts", "proxy_signals", "simulations"):
        payload = phase4_step2_evidence_report_fixture()
        payload[section] = {"gini_simpson_diversity": phase4_step2_metric_fixture()}
        with pytest.raises(ValueError):
            CanonicalReport.from_dict(payload)


def test_phase4_step2_metric_metadata_is_required():
    import pytest

    from recursive_integrity_toolkit.result import CanonicalReport

    for field in phase4_step2_metric_fixture():
        payload = phase4_step2_metric_report_fixture()
        metric = payload["derived_metrics"]["diversity"]["by_version"]["v1"]["gini_simpson_diversity"]
        del metric[field]
        with pytest.raises(ValueError):
            CanonicalReport.from_dict(payload)


def test_phase4_step2_metric_keys_owner_and_method_cannot_be_forged():
    import pytest

    from recursive_integrity_toolkit.result import CanonicalReport

    for field, value in (
        ("private_cache", {"raw_content": "unregistered"}), ("unit", "seconds"),
        ("method_id", "F-999"), ("owner_ids", ["PR-002"]), ("trace_ids", ["T999"]),
    ):
        payload = phase4_step2_metric_report_fixture()
        metric = payload["derived_metrics"]["diversity"]["by_version"]["v1"]["gini_simpson_diversity"]
        metric[field] = value
        with pytest.raises(ValueError):
            CanonicalReport.from_dict(payload)


def test_phase4_step2_numeric_metric_values_reject_bools_and_nonfinite_numbers():
    import pytest

    from recursive_integrity_toolkit.result import CanonicalReport

    for field in ("value", "coverage", "denominator"):
        for wrong in (True, False, float("nan"), float("inf"), float("-inf")):
            payload = phase4_step2_metric_report_fixture()
            metric = payload["derived_metrics"]["diversity"]["by_version"]["v1"]["gini_simpson_diversity"]
            metric[field] = wrong
            with pytest.raises(ValueError):
                CanonicalReport.from_dict(payload)
    for field in ("record_count", "excluded_record_count"):
        payload = phase4_step2_metric_report_fixture()
        payload["derived_metrics"]["diversity"]["by_version"]["v1"]["gini_simpson_diversity"]["scope"][field] = True
        with pytest.raises(ValueError):
            CanonicalReport.from_dict(payload)


def test_phase4_step2_metric_unit_range_and_representation_are_meaningful():
    import pytest

    from recursive_integrity_toolkit.result import CanonicalReport

    for field, value in (("value", -0.1), ("value", 1.1), ("coverage", -0.1),
                         ("coverage", 1.1), ("denominator", -1), ("representation", None)):
        payload = phase4_step2_metric_report_fixture()
        metric = payload["derived_metrics"]["diversity"]["by_version"]["v1"]["gini_simpson_diversity"]
        metric[field] = value
        with pytest.raises(ValueError):
            CanonicalReport.from_dict(payload)


def test_phase4_step2_dynamic_version_keys_preserve_literal_identifiers():
    import copy

    from recursive_integrity_toolkit.result import CanonicalReport

    for version in ("版本.甲", "__proto__", "v[1]/a"):
        payload = phase4_step2_metric_report_fixture()
        metric = copy.deepcopy(payload["derived_metrics"]["diversity"]["by_version"].pop("v1"))
        metric["gini_simpson_diversity"]["scope"]["dataset_versions"] = [version]
        metric["gini_simpson_diversity"]["scope"]["scope_id"] = version
        payload["derived_metrics"]["diversity"]["by_version"][version] = metric
        assert CanonicalReport.from_dict(payload).to_dict() == payload


def test_phase4_step2_version_key_cannot_claim_a_different_scope():
    import pytest

    from recursive_integrity_toolkit.result import CanonicalReport

    payload = phase4_step2_metric_report_fixture()
    payload["derived_metrics"]["diversity"]["by_version"]["v1"]["gini_simpson_diversity"]["scope"]["dataset_versions"] = ["v2"]
    with pytest.raises(ValueError):
        CanonicalReport.from_dict(payload)


def test_phase4_step2_nested_result_input_and_export_mutation_are_isolated():
    from recursive_integrity_toolkit.result import CanonicalReport

    payload = phase4_step2_metric_report_fixture()
    report = CanonicalReport.from_dict(payload)
    payload["derived_metrics"]["diversity"]["by_version"]["v1"]["gini_simpson_diversity"]["scope"]["dataset_versions"].append("forged")
    payload["derived_metrics"]["diversity"]["by_version"]["v1"]["gini_simpson_diversity"]["value"] = 0.5
    first = report.to_dict()
    first["derived_metrics"]["diversity"]["by_version"]["v1"]["gini_simpson_diversity"]["representation"]["field_name"] = "secret"
    first["derived_metrics"]["diversity"]["by_version"]["v1"]["gini_simpson_diversity"]["limitations"].clear()
    assert report.to_dict() == phase4_step2_metric_report_fixture()


def test_phase4_step2_report_evidence_enum_does_not_extend_calculation_enum():
    from recursive_integrity_toolkit.models import CalculationEvidenceClass
    from recursive_integrity_toolkit.result import ReportEvidenceClass

    assert {item.value for item in ReportEvidenceClass} == {
        "observed_fact", "derived_metric", "proxy_signal", "simulation", "unavailable_conclusion",
    }
    assert {item.value for item in CalculationEvidenceClass} == {
        "observed_fact", "derived_metric", "simulation",
    }
    assert ReportEvidenceClass is not CalculationEvidenceClass


def phase4_step2_additional_evidence_fixture(evidence_class):
    """Values and reasons are supplied explicitly, with no computed expectations."""
    item = phase4_step2_metric_fixture()
    del item["value"]
    item["evidence_class"] = evidence_class
    if evidence_class == "proxy_signal":
        item.update({
            "unit": "signal", "method_id": "T1.support_contraction",
            "signal": "support_contraction", "level": "present",
            "basis_fields": ["derived_metrics.support.support_delta"],
            "trigger_rule": "The supplied explicit-pair support delta is negative.",
            "limitations": ["A state-support change does not prove production failure."],
        })
    elif evidence_class == "unavailable_conclusion":
        item.update({
            "unit": "conclusion", "method_id": "PR-014.unavailable_conclusion",
            "owner_ids": ["PR-014"], "trace_ids": [], "representation": None,
            "status": "unavailable", "conclusion": "model_performance_decline",
            "statement": "Supplied metadata cannot establish model-performance decline.",
            "reason_codes": ["MODEL_OUTCOME_DATA_MISSING"],
            "required_evidence": ["Versioned model evaluation results."],
            "blocking_evidence": ["No model outcome measurements were supplied."],
            "required_next_metadata": ["Versioned model evaluation results."],
            "related_capability": "model_longitudinal",
            "theory_or_product_limit": "Structural dataset observations do not measure model performance.",
        })
    elif evidence_class == "simulation":
        item.update({
            "unit": "scenario", "method_id": "T2.tail_extinction",
            "owner_ids": ["T2"], "trace_ids": ["T2"], "status": "experimental",
            "model": "closed_resampling", "model_version": "1",
            "method": "analytic_extinction",
            "assumptions": ["Two independent draws from a fixed selected-state marginal."],
            "limitations": ["The probability is conditional on a closed-resampling model."],
            "parameters": {
                "resample_size": 2, "simulation_horizon": 1,
                "random_seed": None, "simulation_replicates": None,
                "rng_name": None, "numpy_version": None, "replicate_schedule": None,
                "state_order": [], "input_basis": "supplied_selected_state_marginal",
                "reopening_weight": None, "external_input_distribution": [],
                "numerical_policy": {
                    "absolute_tolerance": 1e-12, "relative_tolerance": 1e-12,
                    "probability_mass_tolerance": 1e-12,
                },
            },
            "initial_distribution": [],
            "resample_size": 2,
            "by_state": {"rare": {
                "observed_frequency": 0.5, "one_step_extinction_probability": 0.25,
                "numerical_underflow": False,
            }},
        })
    else:
        raise AssertionError("Fixture case must name one of the three explicit evidence classes.")
    return item


def test_phase4_step2_proxy_simulation_and_unavailable_classes_have_valid_locations():
    from recursive_integrity_toolkit.result import CanonicalReport

    for evidence_class, section, name in (
        ("proxy_signal", "proxy_signals", "support_contraction"),
        ("simulation", "simulations", "tail_extinction"),
        ("unavailable_conclusion", "unavailable_conclusions", None),
    ):
        payload = phase4_step2_evidence_report_fixture()
        item = phase4_step2_additional_evidence_fixture(evidence_class)
        payload[section] = [item] if name is None else {name: item}
        exported = CanonicalReport.from_dict(payload).to_dict()
        result = exported[section][0] if name is None else exported[section][name]
        assert result["evidence_class"] == evidence_class
        assert result == item


def test_phase4_step2_all_five_class_fixtures_also_satisfy_local_schema(schema_root):
    import json

    from jsonschema import Draft202012Validator
    from referencing import Registry

    def refuse_remote(uri):
        raise AssertionError(f"Schema test attempted external lookup: {uri}")

    schema = json.loads((schema_root / "report.schema.json").read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, registry=Registry(retrieve=refuse_remote))
    fixtures = [phase4_step2_metric_report_fixture(observed=True), phase4_step2_metric_report_fixture()]
    for evidence_class, section, name in (
        ("proxy_signal", "proxy_signals", "support_contraction"),
        ("simulation", "simulations", "tail_extinction"),
        ("unavailable_conclusion", "unavailable_conclusions", None),
    ):
        payload = phase4_step2_evidence_report_fixture()
        item = phase4_step2_additional_evidence_fixture(evidence_class)
        payload[section] = [item] if name is None else {name: item}
        fixtures.append(payload)
    for payload in fixtures:
        validator.validate(payload)


def test_phase4_step2_additional_evidence_classes_cannot_be_relabelled():
    import pytest

    from recursive_integrity_toolkit.result import CanonicalReport

    for original, section, name in (
        ("proxy_signal", "proxy_signals", "support_contraction"),
        ("simulation", "simulations", "tail_extinction"),
        ("unavailable_conclusion", "unavailable_conclusions", None),
    ):
        for wrong in ("observed_fact", "derived_metric", "proxy_signal", "simulation", "unavailable_conclusion"):
            if original == wrong:
                continue
            payload = phase4_step2_evidence_report_fixture()
            item = phase4_step2_additional_evidence_fixture(original)
            item["evidence_class"] = wrong
            payload[section] = [item] if name is None else {name: item}
            with pytest.raises(ValueError):
                CanonicalReport.from_dict(payload)


def test_phase4_step2_simulations_are_experimental_and_require_model_metadata():
    import pytest

    from recursive_integrity_toolkit.result import CanonicalReport

    for field in ("model", "model_version", "method", "parameters", "initial_distribution", "by_state", "resample_size"):
        payload = phase4_step2_evidence_report_fixture()
        item = phase4_step2_additional_evidence_fixture("simulation")
        del item[field]
        payload["simulations"] = {"tail_extinction": item}
        with pytest.raises(ValueError):
            CanonicalReport.from_dict(payload)
    for wrong in ("available", "completed", "partial"):
        payload = phase4_step2_evidence_report_fixture()
        item = phase4_step2_additional_evidence_fixture("simulation")
        item["status"] = wrong
        payload["simulations"] = {"tail_extinction": item}
        with pytest.raises(ValueError):
            CanonicalReport.from_dict(payload)


def test_phase4_step2_nonfinite_values_cannot_hide_inside_simulation_metadata():
    import pytest

    from recursive_integrity_toolkit.result import CanonicalReport

    for branch, field in (("by_state", "observed_frequency"),
                          ("by_state", "one_step_extinction_probability"),
                          ("parameters", "resample_size"),
                          ("numerical_policy", "relative_tolerance")):
        for wrong in (float("nan"), float("inf"), float("-inf"), True):
            payload = phase4_step2_evidence_report_fixture()
            item = phase4_step2_additional_evidence_fixture("simulation")
            target = (item["parameters"]["numerical_policy"] if branch == "numerical_policy" else
                      item["by_state"]["rare"] if branch == "by_state" else item[branch])
            target[field] = wrong
            payload["simulations"] = {"tail_extinction": item}
            with pytest.raises(ValueError):
                CanonicalReport.from_dict(payload)


def test_phase4_step2_unavailable_conclusions_require_why_and_what_is_needed():
    import pytest

    from recursive_integrity_toolkit.result import CanonicalReport

    for field in ("statement", "blocking_evidence", "required_next_metadata", "related_capability",
                  "theory_or_product_limit", "reason_codes", "required_evidence"):
        payload = phase4_step2_evidence_report_fixture()
        item = phase4_step2_additional_evidence_fixture("unavailable_conclusion")
        del item[field]
        payload["unavailable_conclusions"] = [item]
        with pytest.raises(ValueError):
            CanonicalReport.from_dict(payload)


def test_phase4_step2_proxy_requires_basis_trigger_and_limits():
    import pytest

    from recursive_integrity_toolkit.result import CanonicalReport

    for field, empty in (("basis_fields", []), ("trigger_rule", ""), ("limitations", [])):
        payload = phase4_step2_evidence_report_fixture()
        item = phase4_step2_additional_evidence_fixture("proxy_signal")
        item[field] = empty
        payload["proxy_signals"] = {"support_contraction": item}
        with pytest.raises(ValueError):
            CanonicalReport.from_dict(payload)


def test_phase4_step2_unapproved_external_reference_simulation_is_rejected():
    import pytest

    from recursive_integrity_toolkit.result import CanonicalReport

    payload = phase4_step2_evidence_report_fixture()
    payload["simulations"] = {"external_reference_loss": phase4_step2_additional_evidence_fixture("simulation")}
    with pytest.raises(ValueError):
        CanonicalReport.from_dict(payload)


def phase4_step2_interval_report_fixture():
    payload = phase4_step2_evidence_report_fixture()
    interval = {}
    for name, value, method in (("lower_bound", 0.25, "F-009"), ("upper_bound", 0.75, "F-010"),
                                ("interval_width", 0.5, "T3.upper_minus_lower")):
        item = phase4_step2_metric_fixture()
        item.update({
            "value": value, "unit": "ratio", "method_id": method, "owner_ids": ["T3"], "trace_ids": ["T3"],
            "representation": None, "denominator": 4,
            "limitations": ["Supplied grounding declarations have not been independently verified."],
        })
        item["scope"]["record_count"] = 4
        interval[name] = item
    payload["derived_metrics"] = {"closure_exposure": {"direct": interval}}
    return payload


def test_phase4_step2_closure_interval_retains_lower_upper_and_width():
    from recursive_integrity_toolkit.result import CanonicalReport

    report = CanonicalReport.from_dict(phase4_step2_interval_report_fixture()).to_dict()
    interval = report["derived_metrics"]["closure_exposure"]["direct"]
    assert set(interval) == {"lower_bound", "upper_bound", "interval_width"}
    assert interval["lower_bound"]["value"] == 0.25
    assert interval["upper_bound"]["value"] == 0.75
    assert interval["interval_width"]["value"] == 0.5


def test_phase4_step2_closure_interval_rejects_inconsistent_values_or_single_point():
    import pytest

    from recursive_integrity_toolkit.result import CanonicalReport

    for field, value in (("lower_bound", 0.8), ("upper_bound", 0.2), ("interval_width", 0.25)):
        payload = phase4_step2_interval_report_fixture()
        payload["derived_metrics"]["closure_exposure"]["direct"][field]["value"] = value
        with pytest.raises(ValueError):
            CanonicalReport.from_dict(payload)
    payload = phase4_step2_interval_report_fixture()
    payload["derived_metrics"]["closure_exposure"]["direct"]["midpoint"] = phase4_step2_metric_fixture()
    with pytest.raises(ValueError):
        CanonicalReport.from_dict(payload)
    for field in ("lower_bound", "upper_bound", "interval_width"):
        payload = phase4_step2_interval_report_fixture()
        del payload["derived_metrics"]["closure_exposure"]["direct"][field]
        with pytest.raises(ValueError):
            CanonicalReport.from_dict(payload)


def test_phase4_step2_reserved_looking_version_ids_do_not_change_metric_semantics():
    from recursive_integrity_toolkit.result import CanonicalReport

    for version in ("weighted_v1", "by_version", "evidence_class", "weighting_mode",
                    "representation_name", "coverage", "coverage_reason", "denominator",
                    "denominator_reason", "status", "scope", "value", "reason_codes"):
        payload = phase4_step2_metric_report_fixture()
        by_version = payload["derived_metrics"]["diversity"]["by_version"]
        metrics = by_version.pop("v1")
        metrics["gini_simpson_diversity"]["scope"]["dataset_versions"] = [version]
        metrics["gini_simpson_diversity"]["scope"]["scope_id"] = version
        by_version[version] = metrics
        exported = CanonicalReport.from_dict(payload).to_dict()
        item = exported["derived_metrics"]["diversity"]["by_version"][version]["gini_simpson_diversity"]
        assert item["value"] == 0
        assert "weighting" not in item
        assert item["scope"]["dataset_versions"] == [version]


def test_phase4_step2_actual_weighted_metric_requires_its_explicit_weight_basis():
    import copy
    import pytest

    from recursive_integrity_toolkit.result import CanonicalReport

    payload = phase4_step2_evidence_report_fixture()
    metric = phase4_step2_metric_fixture()
    metric["weighting"] = {"weighting_mode": "weighted", "weight_field": "weight"}
    metric["scope"]["denominator_basis"] = "included_record_weight_mass"
    payload["derived_metrics"] = {"diversity": {"by_version": {"v1": {
        "weighted_gini_simpson_diversity": metric,
    }}}}
    exported = CanonicalReport.from_dict(payload).to_dict()
    weighted = exported["derived_metrics"]["diversity"]["by_version"]["v1"]["weighted_gini_simpson_diversity"]
    assert weighted["value"] == 0
    assert weighted["denominator"] == 2
    assert weighted["weighting"] == {"weighting_mode": "weighted", "weight_field": "weight"}
    for replacement in (None, {}, {"weighting_mode": "unweighted", "weight_field": None},
                        {"weighting_mode": "weighted", "weight_field": None},
                        {"weighting_mode": "weighted", "weight_field": "inferred_confidence"}):
        invalid = copy.deepcopy(payload)
        item = invalid["derived_metrics"]["diversity"]["by_version"]["v1"]["weighted_gini_simpson_diversity"]
        if replacement is None:
            del item["weighting"]
        else:
            item["weighting"] = replacement
        with pytest.raises(ValueError):
            CanonicalReport.from_dict(invalid)


def test_phase4_step2_available_state_counts_need_declared_representation():
    import pytest

    from recursive_integrity_toolkit.result import CanonicalReport

    payload = phase4_step2_evidence_report_fixture()
    counts = phase4_step2_metric_fixture()
    counts.update({
        "value": [{"state_id": "single", "state_count": 2}],
        "unit": "records", "evidence_class": "observed_fact", "method_id": "T1.state_counts",
    })
    payload["observed_facts"] = {"state_counts": {"by_version": {"v1": counts}}}
    exported = CanonicalReport.from_dict(payload).to_dict()
    assert exported["observed_facts"]["state_counts"]["by_version"]["v1"]["value"] == [
        {"state_id": "single", "state_count": 2},
    ]
    counts["representation"] = None
    with pytest.raises(ValueError):
        CanonicalReport.from_dict(payload)


def test_phase4_step2_contract_keyword_state_ids_are_literal_simulation_labels():
    from recursive_integrity_toolkit.result import CanonicalReport

    for state in ("weighted_v1", "by_version", "evidence_class", "weighting_mode",
                  "representation_name", "coverage", "coverage_reason", "denominator",
                  "denominator_reason", "status", "scope", "value", "reason_codes"):
        payload = phase4_step2_evidence_report_fixture()
        scenario = phase4_step2_additional_evidence_fixture("simulation")
        expected = scenario["by_state"].pop("rare")
        scenario["by_state"][state] = expected
        payload["simulations"] = {"tail_extinction": scenario}
        exported = CanonicalReport.from_dict(payload).to_dict()
        assert exported["simulations"]["tail_extinction"]["by_state"][state] == {
            "observed_frequency": 0.5, "one_step_extinction_probability": 0.25,
            "numerical_underflow": False,
        }


def phase4_step2_sampled_path_report_fixture():
    """Literal two-draw outcome loses two states in the same sampled step."""
    payload = phase4_step2_evidence_report_fixture()
    scenario = phase4_step2_additional_evidence_fixture("simulation")
    scenario.update({
        "method_id": "T1.closed_resampling", "owner_ids": ["T1"], "trace_ids": ["T1"],
        "method": "sampled_path",
        "assumptions": ["Independent draws from a fixed finite state distribution."],
        "limitations": ["One sampled path is a scenario, with no empirical forecast claim."],
    })
    del scenario["by_state"]
    scenario["parameters"].update({
        "random_seed": 1, "simulation_replicates": 1,
        "rng_name": "numpy.random.Generator(PCG64)", "numpy_version": "2.0.0",
        "replicate_schedule": "replicate_major_step_major", "state_order": ["a", "b", "c"],
        "input_basis": "explicit_supplied_state_probability_vector",
    })
    scenario["initial_distribution"] = [
        {"state_id": "a", "probability": 0.25}, {"state_id": "b", "probability": 0.25},
        {"state_id": "c", "probability": 0.5},
    ]
    scenario["sampled_paths"] = [{"replicate_index": 0, "generations": [
        {"step": 0, "state_counts": None, "state_frequencies": [0.25, 0.25, 0.5],
         "support": ["a", "b", "c"], "support_size": 3, "gini_simpson_diversity": 0.625},
        {"step": 1, "state_counts": [0, 0, 2], "state_frequencies": [0, 0, 1],
         "support": ["c"], "support_size": 1, "gini_simpson_diversity": 0},
    ]}]
    scenario["extinction_events"] = [
        {"replicate_index": 0, "step": 1, "state_id": "a"},
        {"replicate_index": 0, "step": 1, "state_id": "b"},
    ]
    payload["simulations"] = {"closed_resampling": scenario}
    return payload


def test_phase4_step2_distinct_state_extinctions_can_share_replicate_and_step():
    from recursive_integrity_toolkit.result import CanonicalReport

    payload = phase4_step2_sampled_path_report_fixture()
    exported = CanonicalReport.from_dict(payload).to_dict()
    assert exported["simulations"]["closed_resampling"]["extinction_events"] == [
        {"replicate_index": 0, "step": 1, "state_id": "a"},
        {"replicate_index": 0, "step": 1, "state_id": "b"},
    ]


def test_phase4_step2_identical_extinction_event_identity_is_rejected():
    import copy
    import pytest

    from recursive_integrity_toolkit.result import CanonicalReport

    payload = phase4_step2_sampled_path_report_fixture()
    events = payload["simulations"]["closed_resampling"]["extinction_events"]
    events.append(copy.deepcopy(events[0]))
    with pytest.raises(ValueError):
        CanonicalReport.from_dict(payload)


def test_phase4_step2_repeated_state_identity_in_a_state_count_table_is_rejected():
    import pytest

    from recursive_integrity_toolkit.result import CanonicalReport

    payload = phase4_step2_evidence_report_fixture()
    counts = phase4_step2_metric_fixture()
    counts.update({
        "value": [{"state_id": "a", "state_count": 1}, {"state_id": "a", "state_count": 2}],
        "unit": "records", "evidence_class": "observed_fact", "method_id": "T1.state_counts",
        "denominator": 3,
    })
    counts["scope"]["record_count"] = 3
    payload["observed_facts"] = {"state_counts": {"by_version": {"v1": counts}}}
    with pytest.raises(ValueError):
        CanonicalReport.from_dict(payload)


def test_phase4_step2_unavailable_proxy_cannot_assert_signal_presence():
    import pytest

    from recursive_integrity_toolkit.result import CanonicalReport

    payload = phase4_step2_evidence_report_fixture()
    signal = phase4_step2_additional_evidence_fixture("proxy_signal")
    signal.update({
        "status": "unavailable", "reason_codes": ["MISSING_PAIR"],
        "required_evidence": ["An explicitly ordered compatible dataset pair."],
        "level": "indeterminate",
    })
    payload["proxy_signals"] = {"support_contraction": signal}
    exported = CanonicalReport.from_dict(payload).to_dict()
    assert exported["proxy_signals"]["support_contraction"]["level"] == "indeterminate"
    for invalid_level in ("present", "absent"):
        signal["level"] = invalid_level
        with pytest.raises(ValueError):
            CanonicalReport.from_dict(payload)


def test_phase4_step2_sampled_path_must_cover_its_declared_horizon():
    import copy
    import pytest

    from recursive_integrity_toolkit.result import CanonicalReport

    payload = phase4_step2_sampled_path_report_fixture()
    CanonicalReport.from_dict(payload)
    for generation_count in (0, 1):
        invalid = copy.deepcopy(payload)
        generations = invalid["simulations"]["closed_resampling"]["sampled_paths"][0]["generations"]
        del generations[generation_count:]
        with pytest.raises(ValueError):
            CanonicalReport.from_dict(invalid)


def test_phase4_step2_single_version_maps_reject_aggregate_scope():
    import pytest

    from recursive_integrity_toolkit.result import CanonicalReport

    payload = phase4_step2_metric_report_fixture()
    metric = payload["derived_metrics"]["diversity"]["by_version"]["v1"]["gini_simpson_diversity"]
    metric["scope"]["dataset_versions"] = ["v1", "v2"]
    with pytest.raises(ValueError):
        CanonicalReport.from_dict(payload)
    payload = phase4_step2_evidence_report_fixture()
    counts = phase4_step2_metric_fixture(observed=True)
    counts.update({"value": 2, "method_id": "PR-002.record_count", "owner_ids": ["PR-002"]})
    payload["observed_facts"] = {"record_counts": {"v1": counts}}
    CanonicalReport.from_dict(payload)
    counts["scope"]["dataset_versions"] = ["v1", "v2"]
    with pytest.raises(ValueError):
        CanonicalReport.from_dict(payload)


def phase4_step2_duplicate_group_report_fixture():
    payload = phase4_step2_evidence_report_fixture()
    groups = phase4_step2_metric_fixture(observed=True)
    groups.update({
        "unit": "groups", "method_id": "PR-006.exact_duplicate_groups",
        "value": [{
            "group_id": "group-1", "record_count": 2, "normalization_profile": "exact_utf8_v1",
            "record_keys": [
                {"dataset_version": "v1", "record_id": "a"},
                {"dataset_version": "v1", "record_id": "b"},
            ],
        }],
        "limitations": ["Exact normalized duplicate groups do not establish semantic equivalence."],
    })
    payload["observed_facts"] = {"content": {"exact_duplicate_groups": groups}}
    return payload


def test_phase4_step2_duplicate_group_identity_omission_preserves_aggregate_count(schema_root):
    import json

    from jsonschema import Draft202012Validator
    from recursive_integrity_toolkit.result import CanonicalReport

    validator = Draft202012Validator(json.loads(
        (schema_root / "report.schema.json").read_text(encoding="utf-8"),
    ))
    payload = phase4_step2_duplicate_group_report_fixture()
    validator.validate(payload)
    original = CanonicalReport.from_dict(payload).to_dict()
    group = payload["observed_facts"]["content"]["exact_duplicate_groups"]["value"][0]
    group["record_keys"] = None
    group["redaction"] = {"omitted_fields": ["record_keys"], "reason": "redacted_identity_details"}
    payload["run"]["privacy_mode"] = "redacted"
    payload["run"]["redacted_mode"] = True
    validator.validate(payload)
    exported = CanonicalReport.from_dict(payload).to_dict()
    result = exported["observed_facts"]["content"]["exact_duplicate_groups"]
    assert result["value"][0]["record_count"] == 2
    assert result["value"][0]["record_count"] == original["observed_facts"]["content"]["exact_duplicate_groups"]["value"][0]["record_count"]
    assert result["value"][0]["record_keys"] is None
    assert result["value"][0]["redaction"] == {
        "omitted_fields": ["record_keys"], "reason": "redacted_identity_details",
    }
    assert result["coverage"] == 1.0
    assert result["denominator"] == 2
    assert result["evidence_class"] == "observed_fact"
    assert result["status"] == "available"


def test_phase4_step2_null_duplicate_identity_list_requires_same_group_redaction(schema_root):
    import json
    import pytest

    from jsonschema import Draft202012Validator
    from recursive_integrity_toolkit.result import CanonicalReport

    validator = Draft202012Validator(json.loads(
        (schema_root / "report.schema.json").read_text(encoding="utf-8"),
    ))
    for declaration in (None, {"omitted_fields": ["group_id"], "reason": "redacted_identity_details"},
                        {"omitted_fields": ["record_keys"], "reason": "missing_evidence"}):
        payload = phase4_step2_duplicate_group_report_fixture()
        group = payload["observed_facts"]["content"]["exact_duplicate_groups"]["value"][0]
        group["record_keys"] = None
        if declaration is not None:
            group["redaction"] = declaration
        assert not validator.is_valid(payload), declaration
        with pytest.raises(ValueError):
            CanonicalReport.from_dict(payload)


def test_phase4_step2_visible_duplicate_identities_remain_at_least_two_and_unique():
    import pytest

    from recursive_integrity_toolkit.result import CanonicalReport

    first = {"dataset_version": "v1", "record_id": "a"}
    for identities in ([], [first], [first, first]):
        payload = phase4_step2_duplicate_group_report_fixture()
        group = payload["observed_facts"]["content"]["exact_duplicate_groups"]["value"][0]
        group["record_keys"] = identities
        with pytest.raises(ValueError):
            CanonicalReport.from_dict(payload)
    payload = phase4_step2_duplicate_group_report_fixture()
    group = payload["observed_facts"]["content"]["exact_duplicate_groups"]["value"][0]
    group["redaction"] = {"omitted_fields": ["record_keys"], "reason": "redacted_identity_details"}
    with pytest.raises(ValueError):
        CanonicalReport.from_dict(payload)


# Phase 4 Step 3: independently authored report assembly expectations.
def phase4_step3_run():
    return {
        "run_id": "step3-independent-case", "toolkit_version": "0.1.0.dev2",
        "report_schema_version": "1.1", "started_at": None, "completed_at": None,
        "duration_seconds": None, "python_version": None, "platform": None,
        "command": None, "config_hash": None, "random_seed": None,
        "strict_mode": False, "redacted_mode": False, "network_call_count": 0,
        "deterministic": True, "privacy_mode": "standard", "run_status": "complete",
        "null_reasons": {
            "started_at": "Pure assembly does not start a clock.",
            "completed_at": "Pure assembly does not start a clock.",
            "duration_seconds": "Pure assembly does not measure execution.",
            "python_version": "No execution environment is asserted.",
            "platform": "No execution environment is asserted.",
            "command": "Direct Python API, no command invoked.",
            "config_hash": "No resolved configuration hash was supplied.",
            "random_seed": "No run-wide random generator was requested.",
        },
    }


def phase4_step3_bundle(tmp_path, labels=("a", "a", "b", "c"), *,
                        provenance_rows=None, versions=None, representation=True):
    import json
    from recursive_integrity_toolkit.io.validation import validate_bundle
    from recursive_integrity_toolkit.models import AuditBundle, FileRole, InputSource

    if not labels:
        from recursive_integrity_toolkit.models import (
            BundleValidationResult, Capability, CapabilityKey, CapabilityStatus,
            ObservabilityAssessment, ProvenanceJoinResult, ValidationCoverage, VersionOrderResult,
        )
        coverage = ValidationCoverage(0, 0, "selected_valid_records")
        joined = ProvenanceJoinResult((), (), False, (), (), coverage, coverage, coverage, ())
        order = VersionOrderResult((), (), "unavailable", {}, {})
        assessment = ObservabilityAssessment(0, {
            key: Capability(CapabilityStatus.UNAVAILABLE, coverage,
                            requirements_missing=("valid records",), reason_codes=("R_EMPTY_SCOPE",))
            for key in CapabilityKey
        }, limitations=("No records were supplied.",))
        return BundleValidationResult((), (), None, joined, order, None, assessment, (), (), ())
    versions = ("v1",) * len(labels) if versions is None else versions
    records = [dict(dataset_version=version, record_id="r" + str(index),
                    content="synthetic public fixture", topic=label)
               for index, (version, label) in enumerate(zip(versions, labels))]
    tmp_path.mkdir(parents=True, exist_ok=True)
    path = tmp_path / "records.jsonl"
    path.write_text("".join(json.dumps(row) + "\n" for row in records), encoding="utf-8")
    sources = [InputSource(FileRole.RECORDS_PRIMARY, path)]
    if provenance_rows is not None:
        path = tmp_path / "provenance.jsonl"
        path.write_text("".join(json.dumps(row) + "\n" for row in provenance_rows), encoding="utf-8")
        sources.append(InputSource(FileRole.PROVENANCE_MANIFEST, path))
    config = {}
    if representation:
        config["representation"] = {
            "name": "topic", "source": "topic_field", "field": "topic",
            "version": "taxonomy-v1", "missing_value_policy": "exclude",
        }
    if len(set(versions)) > 1:
        config["version_order"] = list(dict.fromkeys(versions))
    return validate_bundle(AuditBundle(tuple(sources)), configuration=config)


def phase4_step3_distribution(bundle, version="v1", *, weights=None):
    from recursive_integrity_toolkit.config import RepresentationConfig
    from recursive_integrity_toolkit.metrics.diversity import calculate_state_distribution
    from recursive_integrity_toolkit.models import WeightingOptions
    from recursive_integrity_toolkit.representations.field import assign_field_states

    represented = assign_field_states(
        bundle.records, dataset_versions=(version,), scope_id="report-" + version,
        config=RepresentationConfig("topic", "topic_field", "topic", "taxonomy-v1", "exclude"),
    )
    if weights is None:
        return calculate_state_distribution(represented)
    return calculate_state_distribution(represented, weighting=WeightingOptions("weighted", "weight"),
                                        weights=weights)


def phase4_step3_schema(report, repo_root):
    import json
    from jsonschema import Draft202012Validator

    payload = report.to_dict()
    schema = json.loads((repo_root / "schemas/report.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator(schema).validate(payload)
    assert tuple(payload) == (
        "run", "inputs", "observability", "capabilities", "observed_facts",
        "derived_metrics", "proxy_signals", "simulations", "unavailable_conclusions",
        "recommended_next_metadata", "warnings", "errors",
    )
    assert payload["observability"]["capabilities"] == payload["capabilities"]
    return payload


def test_phase4_step3_distribution_keeps_hand_computed_counts_diversity_and_classes(tmp_path, repo_root):
    from recursive_integrity_toolkit.reports.assembly import assemble_report

    bundle = phase4_step3_bundle(tmp_path)
    result = phase4_step3_distribution(bundle)
    report = phase4_step3_schema(assemble_report(bundle, run=phase4_step3_run(), distributions=(result,)), repo_root)
    counts = report["observed_facts"]["state_counts"]["by_version"]["v1"]
    diversity = report["derived_metrics"]["diversity"]["by_version"]["v1"]
    support = report["derived_metrics"]["support"]["by_version"]["v1"]["support_size"]
    assert counts["value"] == [{"state_id": "a", "state_count": 2},
                               {"state_id": "b", "state_count": 1},
                               {"state_id": "c", "state_count": 1}]
    assert counts["evidence_class"] == "observed_fact"
    assert support["value"] == 3 and support["method_id"] == "F-002"
    assert diversity["gini_simpson_diversity"]["value"] == 5 / 8
    assert diversity["simpson_concentration"]["value"] == 3 / 8
    assert diversity["gini_simpson_diversity"]["value"] == result.unweighted.gini_simpson_diversity.value
    for name in ("gini_simpson_diversity", "simpson_concentration", "state_frequencies"):
        assert diversity[name]["evidence_class"] == "derived_metric"
        assert diversity[name]["denominator"] == 4
        assert diversity[name]["scope"]["record_count"] == 4
    assert report["simulations"] == {}
    assert "support_delta" not in report["derived_metrics"]["support"]


def test_phase4_step3_weighted_companions_keep_distinct_mass_and_record_denominators(tmp_path, repo_root):
    from recursive_integrity_toolkit.models import RecordKey
    from recursive_integrity_toolkit.reports.assembly import assemble_report

    bundle = phase4_step3_bundle(tmp_path)
    weights = {RecordKey("v1", "r" + str(i)): value for i, value in enumerate((1, 1, 0, 2))}
    result = phase4_step3_distribution(bundle, weights=weights)
    report = phase4_step3_schema(assemble_report(bundle, run=phase4_step3_run(), distributions=(result,)), repo_root)
    values = report["derived_metrics"]["diversity"]["by_version"]["v1"]
    assert values["gini_simpson_diversity"]["value"] == 5 / 8
    assert values["weighted_gini_simpson_diversity"]["value"] == 1 / 2
    assert values["weighted_state_masses"]["value"] == [
        {"state_id": "a", "state_mass": 2}, {"state_id": "b", "state_mass": 0},
        {"state_id": "c", "state_mass": 2},
    ]
    assert values["weighted_state_masses"]["unit"] == "user_declared_weight_mass"
    for name in ("weighted_gini_simpson_diversity", "weighted_simpson_concentration",
                 "weighted_state_frequencies", "weighted_state_masses"):
        assert values[name]["weighting"]["weighting_mode"] == "weighted"
        assert values[name]["weighting"]["weight_field"] == "weight"
        assert values[name]["evidence_class"] == "derived_metric"
    assert report["derived_metrics"]["support"]["by_version"]["v1"]["weighted_support_size"]["value"] == 2
    assert report["observed_facts"]["state_counts"]["by_version"]["v1"]["value"][1]["state_count"] == 1


def test_phase4_step3_explicit_pair_preserves_only_accepted_delta_families(tmp_path, repo_root):
    from recursive_integrity_toolkit.metrics.diversity import compare_support
    from recursive_integrity_toolkit.models import ExplicitPairContext
    from recursive_integrity_toolkit.reports.assembly import assemble_report

    bundle = phase4_step3_bundle(tmp_path, ("a", "a", "b", "c", "a", "a", "a", "c"),
                                versions=("v1",) * 4 + ("v2",) * 4)
    earlier, later = phase4_step3_distribution(bundle), phase4_step3_distribution(bundle, "v2")
    a, b = earlier.unweighted, later.unweighted
    comparison = compare_support(a, b, context=ExplicitPairContext(a.scope, b.scope,
        a.representation, b.representation, bundle.version_order),
        earlier_state_semantics="literal shared topic meaning", later_state_semantics="literal shared topic meaning")
    report = phase4_step3_schema(assemble_report(bundle, run=phase4_step3_run(),
        distributions=(earlier, later), comparison=comparison), repo_root)
    support = report["derived_metrics"]["support"]
    assert support["support_delta"]["value"] == -1
    assert support["support_retention_ratio"]["value"] == 2 / 3
    assert support["support_loss_count"]["value"] == 1
    assert support["support_added_count"]["value"] == 0
    assert support["extinct_states"]["value"] == ["b"]
    assert report["derived_metrics"]["diversity"]["gini_simpson_diversity_delta"]["value"] == -1 / 4
    capability = report["capabilities"]["dataset_longitudinal"]
    assert capability["execution_status"] in ("partial", "completed")
    assert capability["execution_scope"]
    assert report["proxy_signals"]["support_contraction"]["level"] == "present"
    assert "relative_change" not in support and "source_share_delta" not in report["derived_metrics"]


def test_phase4_step3_supplied_analytic_scenario_stays_simulation_and_default_is_empty(tmp_path, repo_root):
    from recursive_integrity_toolkit.metrics.resampling import expected_diversity_after_steps
    from recursive_integrity_toolkit.reports.assembly import assemble_report

    bundle = phase4_step3_bundle(tmp_path)
    distribution = phase4_step3_distribution(bundle).unweighted
    expected = expected_diversity_after_steps({"a": 1 / 2, "b": 1 / 4, "c": 1 / 4},
        resample_size=4, steps=2, scope=distribution.scope, representation=distribution.representation)
    empty = phase4_step3_schema(assemble_report(bundle, run=phase4_step3_run()), repo_root)
    assert empty["simulations"] == {}
    report = phase4_step3_schema(assemble_report(bundle, run=phase4_step3_run(), expected_diversity=expected), repo_root)
    scenario = report["simulations"]["closed_resampling"]
    assert scenario["evidence_class"] == "simulation" and scenario["status"] == "experimental"
    assert scenario["expected_diversity"] == [5 / 8, 15 / 32, 45 / 128]
    assert scenario["assumptions"] and scenario["limitations"]
    assert report["observability"]["maximum_level"] == bundle.observability.maximum_level
    assert "closed_resampling" not in report["derived_metrics"]


def test_phase4_step3_supplied_sampled_paths_are_copied_without_rng_execution(tmp_path, repo_root, monkeypatch):
    import numpy
    from recursive_integrity_toolkit.metrics.resampling import simulate_closed_resampling
    from recursive_integrity_toolkit.reports.assembly import assemble_report

    bundle = phase4_step3_bundle(tmp_path)
    distribution = phase4_step3_distribution(bundle).unweighted
    simulation = simulate_closed_resampling({"a": 1 / 2, "b": 1 / 4, "c": 1 / 4},
        resample_size=4, steps=2, seed=17, replicates=2,
        scope=distribution.scope, representation=distribution.representation)
    def phase4_step3_forbid(*args, **kwargs):
        raise AssertionError("Assembly attempted RNG execution")
    monkeypatch.setattr(numpy.random, "default_rng", phase4_step3_forbid)
    monkeypatch.setattr(numpy.random, "Generator", phase4_step3_forbid)
    report = phase4_step3_schema(assemble_report(bundle, run=phase4_step3_run(), resampling=simulation), repo_root)
    scenario = report["simulations"]["closed_resampling"]
    assert len(scenario["sampled_paths"]) == 2
    for actual, original in zip(scenario["sampled_paths"], simulation.sampled_paths):
        assert actual["replicate_index"] == original.replicate_index
        assert [row["support_size"] for row in actual["generations"]] == [row.support_size for row in original.generations]
        assert [row["gini_simpson_diversity"] for row in actual["generations"]] == [row.gini_simpson_diversity for row in original.generations]


def test_phase4_step3_extinction_probability_preserves_hand_worked_conditional_value(tmp_path, repo_root):
    import pytest
    from recursive_integrity_toolkit.metrics.tail import one_step_extinction_probability
    from recursive_integrity_toolkit.reports.assembly import assemble_report

    bundle = phase4_step3_bundle(tmp_path)
    distribution = phase4_step3_distribution(bundle).unweighted
    extinction = one_step_extinction_probability(state_id="b", state_frequency=1 / 4,
        resample_size=4, scope=distribution.scope, representation=distribution.representation)
    report = phase4_step3_schema(assemble_report(bundle, run=phase4_step3_run(), extinction=(extinction,)), repo_root)
    scenario = report["simulations"]["tail_extinction"]
    value = scenario["by_state"]["b"]["one_step_extinction_probability"]
    assert value == pytest.approx(81 / 256, abs=1e-12)
    assert scenario["evidence_class"] == "simulation" and scenario["resample_size"] == 4
    assert scenario["limitations"]


def test_phase4_step3_rejects_forged_result_types_and_duplicate_version_slots(tmp_path):
    import pytest
    from recursive_integrity_toolkit.reports.assembly import assemble_report

    bundle = phase4_step3_bundle(tmp_path)
    distribution = phase4_step3_distribution(bundle)
    for bad in ({"unweighted": distribution.unweighted}, object(), 0, True):
        with pytest.raises((TypeError, ValueError)):
            assemble_report(bundle, run=phase4_step3_run(), distributions=(bad,))
    with pytest.raises((TypeError, ValueError)):
        assemble_report(bundle, run=phase4_step3_run(), distributions=(distribution, distribution))
    with pytest.raises((TypeError, ValueError)):
        assemble_report(bundle, run=phase4_step3_run(), distributions=[distribution])


def test_phase4_step3_rejects_mismatched_formula_owner_class_unit_and_denominator(tmp_path):
    from dataclasses import replace
    import pytest
    from recursive_integrity_toolkit.models import CalculationEvidenceClass
    from recursive_integrity_toolkit.reports.assembly import assemble_report

    bundle = phase4_step3_bundle(tmp_path)
    distribution = phase4_step3_distribution(bundle).unweighted
    scalar = distribution.gini_simpson_diversity
    for changes in ({"formula_id": "F-004"}, {"owner_id": "T4"},
                    {"evidence_class": CalculationEvidenceClass.OBSERVED_FACT},
                    {"unit": "records"}):
        with pytest.raises((TypeError, ValueError)):
            forged = replace(distribution, gini_simpson_diversity=replace(scalar,
                             metadata=replace(scalar.metadata, **changes)))
            assemble_report(bundle, run=phase4_step3_run(), distributions=(forged,))


def test_phase4_step3_rejects_boolean_nonfinite_and_out_of_range_metric_values(tmp_path):
    from dataclasses import replace
    import pytest
    from recursive_integrity_toolkit.reports.assembly import assemble_report

    bundle = phase4_step3_bundle(tmp_path)
    distribution = phase4_step3_distribution(bundle).unweighted
    for value in (True, False, float("nan"), float("inf"), -0.1, 1.1):
        with pytest.raises((TypeError, ValueError)):
            scalar = replace(distribution.gini_simpson_diversity)
            object.__setattr__(scalar, "value", value)
            assemble_report(bundle, run=phase4_step3_run(), distributions=(replace(distribution, gini_simpson_diversity=scalar),))


def test_phase4_step3_rejects_result_scope_from_another_bundle(tmp_path):
    import pytest
    from recursive_integrity_toolkit.reports.assembly import assemble_report

    bundle = phase4_step3_bundle(tmp_path / "source")
    foreign = phase4_step3_bundle(tmp_path / "foreign", versions=("v9",) * 4)
    distribution = phase4_step3_distribution(foreign, "v9")
    with pytest.raises((TypeError, ValueError)):
        assemble_report(bundle, run=phase4_step3_run(), distributions=(distribution,))


def test_phase4_step3_all_calculation_entrypoints_are_blocked_during_assembly(tmp_path, repo_root, monkeypatch):
    import inspect
    from recursive_integrity_toolkit.metrics import bounds, diversity, duplicates, provenance, resampling, tail
    from recursive_integrity_toolkit.models import CalculationScope, ContentMode, TailSelectionOptions
    from recursive_integrity_toolkit.reports import assembly

    rows = [{"dataset_version": "v1", "record_id": "r" + str(i), "source_type": "human",
             "provenance_confidence": "confirmed", "external_grounding": "yes"} for i in range(4)]
    bundle = phase4_step3_bundle(tmp_path, provenance_rows=rows)
    distribution = phase4_step3_distribution(bundle)
    scope = CalculationScope(("v1",), bundle.provenance_join.scope_record_keys, (),
                             bundle.provenance_join.provenance_row_coverage.denominator_name, "provenance-v1")
    composition = provenance.summarize_provenance(bundle.provenance_join, scope=scope)
    closure = bounds.direct_closure_exposure(composition)
    duplicate = duplicates.detect_exact_duplicates(bundle.records, dataset_versions=("v1",), scope_id="duplicates-v1",
        representation_name="record_form", representation_version="exact-v1",
        normalization_profile="exact_utf8_v1", content_mode=ContentMode.INLINE)
    tail_result = tail.select_tail(distribution.unweighted, options=TailSelectionOptions("singleton_count"))
    scenario = resampling.expected_diversity_after_steps({"a": 1 / 2, "b": 1 / 4, "c": 1 / 4},
        resample_size=4, steps=2, scope=distribution.unweighted.scope, representation=distribution.unweighted.representation)
    extinction = tail.one_step_extinction_probability(1 / 4, resample_size=4, state_id="b",
        scope=distribution.unweighted.scope, representation=distribution.unweighted.representation)
    def phase4_step3_forbid(*args, **kwargs):
        raise AssertionError("Assembly attempted a calculation")
    for module in (bounds, diversity, duplicates, provenance, resampling, tail):
        for name, value in tuple(vars(module).items()):
            if inspect.isfunction(value) and value.__module__ == module.__name__:
                monkeypatch.setattr(module, name, phase4_step3_forbid)
    for name, value in tuple(vars(assembly).items()):
        if inspect.isfunction(value) and value.__module__.startswith("recursive_integrity_toolkit.metrics"):
            monkeypatch.setattr(assembly, name, phase4_step3_forbid)
    report = phase4_step3_schema(assembly.assemble_report(bundle, run=phase4_step3_run(), distributions=(distribution,),
        provenance=composition, closure=closure, duplicates=duplicate, tail=tail_result,
        expected_diversity=scenario, extinction=(extinction,)), repo_root)
    assert report["derived_metrics"]["diversity"]["by_version"]["v1"]["gini_simpson_diversity"]["value"] == 5 / 8
    assert report["derived_metrics"]["closure_exposure"]["direct"]["lower_bound"]["value"] == 0
    assert report["observed_facts"]["content"]["duplicate_record_count"]["value"] == 3
    assert report["simulations"]["closed_resampling"]["expected_diversity"] == [5 / 8, 15 / 32, 45 / 128]


def test_phase4_step3_assembly_performs_no_file_or_network_access(tmp_path, repo_root, monkeypatch):
    import builtins
    import io
    import socket
    import urllib.request
    from pathlib import Path
    from recursive_integrity_toolkit.reports.assembly import assemble_report

    bundle = phase4_step3_bundle(tmp_path)
    distribution = phase4_step3_distribution(bundle)
    def phase4_step3_forbid(*args, **kwargs):
        raise AssertionError("Assembly attempted file or network access")
    with monkeypatch.context() as blocked:
        for owner, name in ((builtins, "open"), (io, "open"), (Path, "open"),
                            (socket, "socket"), (socket, "create_connection"),
                            (socket, "getaddrinfo"), (urllib.request, "urlopen")):
            blocked.setattr(owner, name, phase4_step3_forbid)
        report = assemble_report(bundle, run=phase4_step3_run(), distributions=(distribution,))
    payload = phase4_step3_schema(report, repo_root)
    assert payload["run"]["network_call_count"] == 0


def test_phase4_step3_assembly_does_not_mutate_inputs_or_return_mutable_state(tmp_path, repo_root):
    from copy import deepcopy
    from recursive_integrity_toolkit.reports.assembly import assemble_report

    bundle = phase4_step3_bundle(tmp_path)
    distribution = phase4_step3_distribution(bundle)
    run = phase4_step3_run()
    before = deepcopy(run)
    report = assemble_report(bundle, run=run, distributions=(distribution,))
    exported = phase4_step3_schema(report, repo_root)
    exported["derived_metrics"]["support"]["by_version"]["v1"]["support_size"]["value"] = 99
    run["run_id"] = "caller-mutated"
    again = report.to_dict()
    assert again["run"]["run_id"] == before["run_id"]
    assert again["derived_metrics"]["support"]["by_version"]["v1"]["support_size"]["value"] == 3
    assert distribution.unweighted.support_size.value == 3


def test_phase4_step3_rejects_boolean_coverage_and_mismatched_distribution_denominator(tmp_path):
    from dataclasses import replace
    import pytest
    from recursive_integrity_toolkit.models import ValidationCoverage
    from recursive_integrity_toolkit.reports.assembly import assemble_report

    bundle = phase4_step3_bundle(tmp_path)
    result = phase4_step3_distribution(bundle)
    forged = (replace(result, coverage=ValidationCoverage(True, 4, "selected_valid_records")),
              replace(result, unweighted=replace(result.unweighted, frequency_denominator=100)))
    for value in forged:
        with pytest.raises((TypeError, ValueError)):
            assemble_report(bundle, run=phase4_step3_run(), distributions=(value,))


def test_phase4_step3_rejects_mismatched_representation_and_weighting_metadata(tmp_path):
    from dataclasses import replace
    import pytest
    from recursive_integrity_toolkit.models import WeightingOptions
    from recursive_integrity_toolkit.reports.assembly import assemble_report

    bundle = phase4_step3_bundle(tmp_path)
    result = phase4_step3_distribution(bundle).unweighted
    scalar = result.gini_simpson_diversity
    changes = ({"representation": replace(result.representation, representation_version="unrelated-taxonomy")},
               {"weighting": WeightingOptions("weighted", "weight")},
               {"scope": replace(result.scope, scope_id="unrelated-scope")})
    for change in changes:
        forged = replace(result, gini_simpson_diversity=replace(scalar, metadata=replace(scalar.metadata, **change)))
        with pytest.raises((TypeError, ValueError)):
            assemble_report(bundle, run=phase4_step3_run(), distributions=(forged,))


def test_phase4_step3_untrusted_mapping_callbacks_are_never_executed(tmp_path):
    from collections.abc import Mapping
    import pytest
    from recursive_integrity_toolkit.reports.assembly import assemble_report

    class phase4_step3_UntrustedMapping(Mapping):
        def __getitem__(self, key):
            raise AssertionError("Untrusted lookup executed")
        def __iter__(self):
            raise AssertionError("Untrusted iterator executed")
        def __len__(self):
            raise AssertionError("Untrusted length executed")
    bundle = phase4_step3_bundle(tmp_path)
    with pytest.raises((TypeError, ValueError)):
        assemble_report(bundle, run=phase4_step3_UntrustedMapping())


def test_phase4_step3_conflicting_closed_scenario_slots_are_rejected(tmp_path):
    import pytest
    from recursive_integrity_toolkit.metrics.resampling import expected_diversity_after_steps, simulate_closed_resampling
    from recursive_integrity_toolkit.reports.assembly import assemble_report

    bundle = phase4_step3_bundle(tmp_path)
    distribution = phase4_step3_distribution(bundle).unweighted
    context = {"scope": distribution.scope, "representation": distribution.representation}
    expected = expected_diversity_after_steps({"a": 1.0}, resample_size=4, steps=1, **context)
    sampled = simulate_closed_resampling({"a": 1.0}, resample_size=4, steps=1, seed=2, replicates=1, **context)
    with pytest.raises((TypeError, ValueError)):
        assemble_report(bundle, run=phase4_step3_run(), expected_diversity=expected, resampling=sampled)


def test_phase4_step3_standalone_probability_evidence_does_not_invent_empirical_records(tmp_path, repo_root):
    from recursive_integrity_toolkit.metrics.diversity import distribution_from_probabilities
    from recursive_integrity_toolkit.models import CalculationScope, RecordKey, RepresentationDescriptor
    from recursive_integrity_toolkit.reports.assembly import assemble_report

    bundle = phase4_step3_bundle(tmp_path, ())
    scope = CalculationScope(("scenario-v1",), (RecordKey("scenario-v1", "declared-basis"),), (),
                             "explicit_scenario_basis", "supplied-vector")
    descriptor = RepresentationDescriptor("topic", "topic_field", "taxonomy-v1", "literal_field_value", field_name="topic")
    supplied = distribution_from_probabilities({"a": 1 / 2, "b": 1 / 2}, scope=scope, representation=descriptor)
    report = phase4_step3_schema(assemble_report(bundle, run=phase4_step3_run(), distributions=(supplied,)), repo_root)
    assert report["inputs"]["scope"]["record_count"] == 0
    assert report["observability"]["maximum_level"] == 0
    assert not report["observed_facts"].get("state_counts", {}).get("by_version")
    probabilities = report["observed_facts"]["supplied_state_probabilities"]["by_version"]["scenario-v1"]
    assert probabilities["value"] == [{"state_id": "a", "probability": 1 / 2},
                                       {"state_id": "b", "probability": 1 / 2}]
    assert report["derived_metrics"]["diversity"]["by_version"]["scenario-v1"]["gini_simpson_diversity"]["value"] == 1 / 2


def test_phase4_step3_standalone_simulation_cannot_promote_empty_input_observability(tmp_path, repo_root):
    from recursive_integrity_toolkit.metrics.resampling import expected_diversity_after_steps
    from recursive_integrity_toolkit.models import CalculationScope, RecordKey, RepresentationDescriptor
    from recursive_integrity_toolkit.reports.assembly import assemble_report

    bundle = phase4_step3_bundle(tmp_path, ())
    scope = CalculationScope(("scenario-v1",), (RecordKey("scenario-v1", "declared-basis"),), (),
                             "explicit_scenario_basis", "standalone-scenario")
    representation = RepresentationDescriptor("topic", "topic_field", "taxonomy-v1", "literal_field_value", field_name="topic")
    simulation = expected_diversity_after_steps({"a": 1 / 2, "b": 1 / 2}, resample_size=2,
                                                steps=1, scope=scope, representation=representation)
    report = phase4_step3_schema(assemble_report(bundle, run=phase4_step3_run(), expected_diversity=simulation), repo_root)
    assert report["simulations"]["closed_resampling"]["expected_diversity"] == [1 / 2, 1 / 4]
    assert report["observability"]["maximum_level"] == 0
    capability = report["capabilities"]["intervention_simulation"]
    assert capability["status"] == "unavailable" and capability["execution_status"] == "completed"
    assert report["inputs"]["scope"]["dataset_versions"] == []


def test_phase4_step3_exact_duplicate_adapter_preserves_existing_record_form_counts(tmp_path, repo_root):
    from recursive_integrity_toolkit.metrics.duplicates import detect_exact_duplicates
    from recursive_integrity_toolkit.models import ContentMode
    from recursive_integrity_toolkit.reports.assembly import assemble_report

    bundle = phase4_step3_bundle(tmp_path)
    duplicates = detect_exact_duplicates(bundle.records, dataset_versions=("v1",), scope_id="duplicates-v1",
        representation_name="record_form", representation_version="exact-v1",
        normalization_profile="exact_utf8_v1", content_mode=ContentMode.INLINE)
    report = phase4_step3_schema(assemble_report(bundle, run=phase4_step3_run(), duplicates=duplicates), repo_root)
    facts = report["observed_facts"]["content"]
    assert facts["duplicate_record_count"]["value"] == 3
    assert facts["duplicate_group_count"]["value"] == 1
    groups = facts["exact_duplicate_groups"]["value"]
    assert len(groups) == 1 and groups[0]["record_count"] == 4
    assert groups[0]["record_keys"] == [{"dataset_version": "v1", "record_id": "r" + str(i)} for i in range(4)]
    assert facts["exact_duplicate_groups"]["evidence_class"] == "observed_fact"


def test_phase4_step3_forged_duplicate_count_cannot_contradict_supplied_groups(tmp_path):
    from dataclasses import replace
    import pytest
    from recursive_integrity_toolkit.metrics.duplicates import detect_exact_duplicates
    from recursive_integrity_toolkit.models import ContentMode
    from recursive_integrity_toolkit.reports.assembly import assemble_report

    bundle = phase4_step3_bundle(tmp_path)
    duplicates = detect_exact_duplicates(bundle.records, dataset_versions=("v1",), scope_id="duplicates-v1",
        representation_name="record_form", representation_version="exact-v1",
        normalization_profile="exact_utf8_v1", content_mode=ContentMode.INLINE)
    forged = replace(duplicates, duplicate_record_count=replace(duplicates.duplicate_record_count, value=1))
    with pytest.raises((TypeError, ValueError)):
        assemble_report(bundle, run=phase4_step3_run(), duplicates=forged)


def phase4_step3_mapped_pair(tmp_path, direction):
    from recursive_integrity_toolkit.metrics.diversity import compare_support, distribution_from_counts
    from recursive_integrity_toolkit.models import CalculationScope, ExplicitPairContext, RepresentationDescriptor
    from recursive_integrity_toolkit.representations.compatibility import StateMappingDeclaration

    fine = RepresentationDescriptor("topic", "topic_field", "fine-v1", "literal_field_value", field_name="topic")
    coarse = RepresentationDescriptor("topic", "topic_field", "coarse-v1", "literal_coarse_labels", field_name="topic")
    fine_labels, coarse_labels = ("red", "red", "green", "pear"), ("apple", "pear", "pear", "pear")
    labels = fine_labels + coarse_labels if direction == "earlier_to_later" else coarse_labels + fine_labels
    bundle = phase4_step3_bundle(tmp_path, labels, versions=("v1",) * 4 + ("v2",) * 4)
    first = CalculationScope(("v1",), tuple(row.record_key for row in bundle.records[:4]), (), "included_representation_records", "map-v1")
    second = CalculationScope(("v2",), tuple(row.record_key for row in bundle.records[4:]), (), "included_representation_records", "map-v2")
    if direction == "earlier_to_later":
        a = distribution_from_counts({"red": 2, "green": 1, "pear": 1}, scope=first, representation=fine)
        b = distribution_from_counts({"apple": 1, "pear": 3}, scope=second, representation=coarse)
        earlier_meaning, later_meaning = "fine-meaning", "coarse-meaning"
    else:
        a = distribution_from_counts({"apple": 1, "pear": 3}, scope=first, representation=coarse)
        b = distribution_from_counts({"red": 2, "green": 1, "pear": 1}, scope=second, representation=fine)
        earlier_meaning, later_meaning = "coarse-meaning", "fine-meaning"
    mapping = StateMappingDeclaration(direction, fine, coarse, "fine-meaning", "coarse-meaning",
                                      {"red": "apple", "green": "apple", "pear": "pear"})
    result = compare_support(a, b, context=ExplicitPairContext(first, second, a.representation,
        b.representation, bundle.version_order), earlier_state_semantics=earlier_meaning,
        later_state_semantics=later_meaning, state_mapping=mapping)
    return bundle, result


def test_phase4_step3_both_directed_maps_preserve_original_and_harmonized_support(tmp_path, repo_root):
    from recursive_integrity_toolkit.reports.assembly import assemble_report

    for direction in ("earlier_to_later", "later_to_earlier"):
        bundle, comparison = phase4_step3_mapped_pair(tmp_path / direction, direction)
        report = phase4_step3_schema(assemble_report(bundle, run=phase4_step3_run(), comparison=comparison), repo_root)
        support = report["derived_metrics"]["support"]
        assert support["support_delta"]["value"] == 0
        assert support["support_retention_ratio"]["value"] == 1
        details = support["comparison_details"]["value"]
        assert details["compatibility_method"] == "explicit_directed_state_mapping"
        assert details["state_mapping"] == [{"source_state": "green", "target_state": "apple"},
                                            {"source_state": "pear", "target_state": "pear"},
                                            {"source_state": "red", "target_state": "apple"}]
        assert details["harmonized_earlier_support"] == details["harmonized_later_support"] == ["apple", "pear"]
        assert len(details["original_earlier_support"]) == (3 if direction == "earlier_to_later" else 2)
        assert len(details["original_later_support"]) == (2 if direction == "earlier_to_later" else 3)
        assert report["proxy_signals"]["support_contraction"]["level"] == "not_present"


def test_phase4_step3_forged_mapping_effect_and_pair_scalar_status_are_rejected(tmp_path):
    from dataclasses import replace
    import pytest
    from recursive_integrity_toolkit.models import CalculationReason, CalculationStatus
    from recursive_integrity_toolkit.reports.assembly import assemble_report

    bundle, comparison = phase4_step3_mapped_pair(tmp_path, "earlier_to_later")
    bad_delta = replace(comparison.gini_simpson_diversity_delta, status=CalculationStatus.UNAVAILABLE,
                        value=None, reason_codes=(CalculationReason.EMPTY_SCOPE,))
    forged = (replace(comparison, mapping_effect=(("earlier", 99, 2), ("later", 2, 2))),
              replace(comparison, gini_simpson_diversity_delta=bad_delta))
    for value in forged:
        with pytest.raises((TypeError, ValueError)):
            assemble_report(bundle, run=phase4_step3_run(), comparison=value)


def test_phase4_step3_nomap_pair_rejects_forged_common_semantic_claim(tmp_path):
    from dataclasses import replace
    import pytest
    from recursive_integrity_toolkit.metrics.diversity import compare_support
    from recursive_integrity_toolkit.models import ExplicitPairContext
    from recursive_integrity_toolkit.reports.assembly import assemble_report

    bundle = phase4_step3_bundle(tmp_path, ("a", "b", "a", "b"), versions=("v1", "v1", "v2", "v2"))
    a, b = phase4_step3_distribution(bundle).unweighted, phase4_step3_distribution(bundle, "v2").unweighted
    comparison = compare_support(a, b, context=ExplicitPairContext(a.scope, b.scope,
        a.representation, b.representation, bundle.version_order),
        earlier_state_semantics="same meaning", later_state_semantics="same meaning")
    forged = replace(comparison, compatibility=replace(comparison.compatibility, later_state_semantics="another meaning"))
    with pytest.raises((TypeError, ValueError)):
        assemble_report(bundle, run=phase4_step3_run(), comparison=forged)


def test_phase4_step3_inventory_only_artifacts_do_not_claim_parse_or_validation(tmp_path, repo_root):
    from dataclasses import replace
    from recursive_integrity_toolkit.models import FileFormat, FileInventoryEntry, FileRole
    from recursive_integrity_toolkit.reports.assembly import assemble_report

    bundle = phase4_step3_bundle(tmp_path)
    inventory = bundle.inventory + (
        FileInventoryEntry(FileRole.EMBEDDING_DATA, tmp_path / "declared.npy", FileFormat.NPY, 0, "0" * 64),
        FileInventoryEntry(FileRole.EXTERNAL_REFERENCE, tmp_path / "declared.jsonl", FileFormat.JSONL, 0, "1" * 64),
    )
    report = phase4_step3_schema(assemble_report(replace(bundle, inventory=inventory), run=phase4_step3_run()), repo_root)
    artifacts = {entry["role"]: entry for entry in report["inputs"]["artifacts"]}
    for role in ("embedding_data", "external_reference"):
        assert artifacts[role]["parse_status"] == "not_requested"
        assert artifacts[role]["validation_status"] == "not_requested"
        assert artifacts[role]["row_count"] is None
    assert artifacts["records_primary"]["parse_status"] == "completed"


def test_phase4_step3_standalone_probability_pair_uses_its_own_explicit_order(tmp_path, repo_root):
    from recursive_integrity_toolkit.io.validation import resolve_version_order
    from recursive_integrity_toolkit.metrics.diversity import compare_support, distribution_from_probabilities
    from recursive_integrity_toolkit.models import CalculationScope, ExplicitPairContext, RecordKey, RepresentationDescriptor
    from recursive_integrity_toolkit.reports.assembly import assemble_report

    bundle = phase4_step3_bundle(tmp_path, ())
    representation = RepresentationDescriptor("topic", "topic_field", "taxonomy-v1", "literal_field_value", field_name="topic")
    first = CalculationScope(("p1",), (RecordKey("p1", "declared-basis"),), (), "explicit_scenario_basis", "p1")
    second = CalculationScope(("p2",), (RecordKey("p2", "declared-basis"),), (), "explicit_scenario_basis", "p2")
    a = distribution_from_probabilities({"a": 1 / 2, "b": 1 / 2}, scope=first, representation=representation)
    b = distribution_from_probabilities({"a": 1.0}, scope=second, representation=representation)
    order = resolve_version_order(("p1", "p2"), invocation_order=("p1", "p2"))
    comparison = compare_support(a, b, context=ExplicitPairContext(first, second, representation, representation, order),
                                 earlier_state_semantics="literal shared meaning", later_state_semantics="literal shared meaning")
    report = phase4_step3_schema(assemble_report(bundle, run=phase4_step3_run(), comparison=comparison), repo_root)
    assert report["derived_metrics"]["support"]["support_delta"]["value"] == -1
    assert report["derived_metrics"]["support"]["support_retention_ratio"]["value"] == 1 / 2
    assert report["derived_metrics"]["diversity"]["gini_simpson_diversity_delta"]["value"] == -1 / 2
    assert report["observability"]["maximum_level"] == 0
    assert report["capabilities"]["dataset_longitudinal"]["status"] == "unavailable"
    assert report["inputs"]["scope"]["record_count"] == 0


def test_phase4_step3_pair_rejects_mixed_probability_and_empirical_input_bases(tmp_path):
    from dataclasses import replace
    import pytest
    from recursive_integrity_toolkit.errors import CanonicalValidationError
    from recursive_integrity_toolkit.metrics.diversity import compare_support, distribution_from_probabilities
    from recursive_integrity_toolkit.models import ExplicitPairContext
    from recursive_integrity_toolkit.reports.assembly import assemble_report

    bundle = phase4_step3_bundle(tmp_path, ("a", "b", "a", "b"), versions=("v1", "v1", "v2", "v2"))
    a, b = phase4_step3_distribution(bundle).unweighted, phase4_step3_distribution(bundle, "v2").unweighted
    context = ExplicitPairContext(a.scope, b.scope, a.representation, b.representation, bundle.version_order)
    options = {"context": context, "earlier_state_semantics": "same meaning", "later_state_semantics": "same meaning"}
    comparison = compare_support(a, b, **options)
    supplied = distribution_from_probabilities({"a": 1 / 2, "b": 1 / 2}, scope=a.scope, representation=a.representation)
    with pytest.raises(CanonicalValidationError):
        compare_support(supplied, b, **options)
    forged = replace(comparison, original_earlier=supplied, harmonized_earlier=supplied)
    with pytest.raises((TypeError, ValueError)):
        assemble_report(bundle, run=phase4_step3_run(), comparison=forged)
