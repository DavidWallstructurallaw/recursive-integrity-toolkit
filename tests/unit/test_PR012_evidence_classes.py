"""Phase 1 placeholder for PR-012.

Planned scope:
    Future evidence-class tests are deferred to Phase 4.

Current Phase 1 scope:
    Verify the approved owner ID and confirm that the target module remains a
    docstring-only, import-safe placeholder.

Limits:
    No mathematical metric, data loading, graph operation, or report result is tested.
"""


def test_PR012_evidence_classes_owner_and_placeholder(owner_checker, placeholder_checker,phase3_final_owner_checker,phase3_final_placeholder_checker):
    owner_checker = phase3_final_owner_checker
    placeholder_checker = phase3_final_placeholder_checker
    owner_checker("reports/assembly.py", "PR-012")
    placeholder_checker("reports/assembly.py")


def phase4_step2_evidence_report_fixture():
    """Independent literal control data, never generated from production code."""
    return {
        "run": {
            "run_id": "independent-evidence-case", "toolkit_version": "0.1.0.dev2",
            "report_schema_version": "1.0", "started_at": None, "completed_at": None,
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
