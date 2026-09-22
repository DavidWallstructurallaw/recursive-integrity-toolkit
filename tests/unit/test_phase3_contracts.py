"""Phase 3 Step 1 contract/baseline tests. No metric or state assignment runs."""
import ast
from copy import deepcopy
from dataclasses import FrozenInstanceError, replace
import hashlib
import json
from pathlib import Path
import runpy

import pytest
from recursive_integrity_toolkit.models import (
    CalculationEvidenceClass, CalculationStatus, CalculationReason, NumericalPolicy,
    RepresentationDescriptor, RecordStateAssignment, CalculationScope, WeightingOptions,
    TailSelectionOptions, CalculationMetadata, ScalarCalculation, ClosedResamplingMetadata,
    ExplicitPairContext, RecordKey,
)

ROOT = Path(__file__).resolve().parents[2]


def descriptor():
    return RepresentationDescriptor("topic", "topic_field", "test-v1", "literal topic", field_name="topic")


def scope():
    return CalculationScope(("v1",), (RecordKey("v1", "a"),), (), "represented_records", "test-scope")


def metadata():
    return CalculationMetadata("gini_simpson_diversity", "T1", "F-003", CalculationEvidenceClass.DERIVED_METRIC,
                               "dimensionless", "supplied-not-computed", scope(), descriptor())


def tools():
    return runpy.run_path(str(ROOT / "scripts/release_check.py"), run_name="contract_test_tools")


def scenario(**changes):
    values = dict(method="analytic_expectation", resample_size=8, simulation_horizon=1,
                  representation=descriptor(), state_order=("a", "b"), assumptions=("finite closed categorical model",))
    values.update(changes)
    return ClosedResamplingMetadata(**values)


def test_phase3_vocabulary_and_documented_reasons():
    assert {x.value for x in CalculationEvidenceClass} == {"observed_fact", "derived_metric", "simulation"}
    assert {x.value for x in CalculationStatus} == {"available", "unavailable"}
    assert len(CalculationReason) == 10
    decisions = (ROOT / "PHASE_3_DECISIONS.md").read_text(encoding="utf-8")
    for reason in CalculationReason:
        assert reason.value in decisions


def test_phase3_frozen_contracts():
    value = scope()
    with pytest.raises(FrozenInstanceError):
        value.scope_id = "changed"
    assert value.included_record_keys == (RecordKey("v1", "a"),)
    assert not hasattr(value, "diversity")


@pytest.mark.parametrize("changes", [
    {"dataset_versions": ()}, {"dataset_versions": ("v1", "v1")},
    {"included_record_keys": [RecordKey("v1", "a")]},
    {"included_record_keys": (RecordKey("v2", "a"),)},
    {"included_record_keys": (RecordKey("v1", "a"), RecordKey("v1", "a"))},
    {"excluded_record_keys": (RecordKey("v1", "a"),)}, {"denominator_basis": ""},
])
def test_phase3_scope_rejects_ambiguous_declarations(changes):
    with pytest.raises((ValueError, TypeError)):
        replace(scope(), **changes)


def test_phase3_unknown_zero_and_unavailable_stay_distinct():
    key = RecordKey("v1", "a")
    assert RecordStateAssignment(key, "unknown").state_id == "unknown"
    assert RecordStateAssignment(key, None, CalculationReason.ALL_EXCLUDED).state_id is None
    zero = ScalarCalculation(metadata(), CalculationStatus.AVAILABLE, 0)
    unavailable = ScalarCalculation(metadata(), CalculationStatus.UNAVAILABLE, None, (CalculationReason.ALL_EXCLUDED,))
    assert zero.value == 0 and unavailable.value is None
    with pytest.raises(ValueError):
        RecordStateAssignment(key, None)
    with pytest.raises(ValueError):
        RecordStateAssignment(key, "a", CalculationReason.ALL_EXCLUDED)
    with pytest.raises(ValueError):
        ScalarCalculation(metadata(), CalculationStatus.UNAVAILABLE, 0, (CalculationReason.ALL_EXCLUDED,))
    with pytest.raises(ValueError):
        ScalarCalculation(metadata(), CalculationStatus.UNAVAILABLE, None)


@pytest.mark.parametrize("changes", [
    {"missing_value_policy": "explicit_missing_state"}, {"missing_state_id": "MISSING"},
    {"missing_value_policy": "impute"}, {"normalization_profile": "case_fold"},
    {"representation_version": ""}, {"field_name": lambda: "a"}, {"representation_source": 1},
])
def test_phase3_descriptor_has_only_explicit_rules(changes):
    with pytest.raises((ValueError, TypeError)):
        replace(descriptor(), **changes)


def test_phase3_declared_payloads_do_not_appear_in_repr():
    rep = replace(descriptor(), missing_value_policy="explicit_missing_state", missing_state_id="PRIVATE_SENTINEL")
    assignment = RecordStateAssignment(RecordKey("v1", "a"), "PRIVATE_SENTINEL")
    assert "PRIVATE_SENTINEL" not in repr(rep) + repr(assignment)
    assert replace(descriptor(), normalization_profile="exact_utf8_v1").normalization_profile == "exact_utf8_v1"


@pytest.mark.parametrize("mode,field", [("auto", None), ("weighted", None), ("weighted", "confidence"),
                                         ("unweighted", "weight"), (True, None)])
def test_phase3_weighting_requires_opt_in(mode, field):
    with pytest.raises((ValueError, TypeError)):
        WeightingOptions(mode, field)


def test_phase3_weighting_declarations_do_not_weigh_data():
    assert WeightingOptions().weighting_mode == "unweighted"
    assert WeightingOptions("weighted", "weight").weight_field == "weight"


@pytest.mark.parametrize("rule,parameters", [
    ("singleton_count", {}), ("count_at_or_below", {"count_threshold": 0}),
    ("frequency_at_or_below", {"frequency_threshold": 0.125}), ("state_list", {"state_ids": ("a", "b")}),
])
def test_phase3_tail_contract_does_not_select_a_tail(rule, parameters):
    result = TailSelectionOptions(rule, **parameters)
    assert result.rule == rule and not hasattr(result, "tail_membership")


@pytest.mark.parametrize("parameters", [
    {"rule":"bottom_frequency_quantile"}, {"rule":"weighted_tail"},
    {"rule":"count_at_or_below","count_threshold":True}, {"rule":"count_at_or_below","count_threshold":-1},
    {"rule":"count_at_or_below","count_threshold":1.5},
    {"rule":"frequency_at_or_below","frequency_threshold":float("nan")},
    {"rule":"frequency_at_or_below","frequency_threshold":float("inf")},
    {"rule":"frequency_at_or_below","frequency_threshold":-0.1},
    {"rule":"frequency_at_or_below","frequency_threshold":1.1},
    {"rule":"singleton_count","count_threshold":1}, {"rule":"state_list","state_ids":("a","a")},
])
def test_phase3_tail_rejects_undefined_or_invalid_options(parameters):
    with pytest.raises((ValueError, TypeError)):
        TailSelectionOptions(**parameters)


@pytest.mark.parametrize("value", [None, True, False, "1", float("nan"), float("inf"), float("-inf"), 10**1000])
def test_phase3_available_scalar_is_finite_builtin_number(value):
    with pytest.raises((ValueError, TypeError)):
        ScalarCalculation(metadata(), CalculationStatus.AVAILABLE, value)


def test_phase3_supplied_scalar_has_trace_metadata_not_calculation():
    result = ScalarCalculation(metadata(), CalculationStatus.AVAILABLE, 0.625)
    assert result.value == 0.625 and result.metadata.formula_id == "F-003"
    assert result.metadata.owner_id == "T1" and result.metadata.scope.denominator_basis == "represented_records"
    assert not hasattr(result, "compute") and not hasattr(result, "render")


@pytest.mark.parametrize("field", ["absolute_tolerance", "relative_tolerance", "probability_mass_tolerance"])
@pytest.mark.parametrize("value", [1e-6, 0.0, True, float("nan")])
def test_phase3_tolerance_policy_cannot_be_silently_changed(field, value):
    with pytest.raises(ValueError):
        NumericalPolicy(**{field:value})


def test_phase3_analytic_metadata_has_no_random_realization():
    result = scenario()
    assert result.random_seed is None and result.evidence_class is CalculationEvidenceClass.SIMULATION
    assert result.experimental is True and not hasattr(result, "sample")


@pytest.mark.parametrize("changes", [
    {"resample_size":0}, {"resample_size":True}, {"resample_size":1.5}, {"simulation_horizon":-1},
    {"simulation_horizon":False}, {"random_seed":1}, {"simulation_replicates":2}, {"experimental":False},
    {"model_name":"reopening"}, {"evidence_class":CalculationEvidenceClass.DERIVED_METRIC},
    {"state_order":()}, {"state_order":("a","a")}, {"assumptions":()}, {"method":"auto"},
])
def test_phase3_scenario_rejects_invalid_or_unsupported_declaration(changes):
    with pytest.raises((ValueError, TypeError)):
        scenario(**changes)


def test_phase3_sampled_metadata_records_method_without_rng_creation():
    result = scenario(method="sampled_path", random_seed=17, simulation_replicates=2,
        rng_name="numpy.random.Generator(PCG64)", numpy_version="test-only-record", replicate_schedule="replicate_major_step_major")
    assert result.random_seed == 17 and result.simulation_replicates == 2
    assert not hasattr(result,"state_distribution") and not hasattr(result,"reopening_weight")


@pytest.mark.parametrize("seed", [None,-1,True,1.0])
def test_phase3_sampled_seed_domain_is_explicit(seed):
    with pytest.raises((ValueError, TypeError)):
        scenario(method="sampled_path",random_seed=seed,simulation_replicates=1,
          rng_name="numpy.random.Generator(PCG64)",numpy_version="test",replicate_schedule="replicate_major_step_major")


def test_phase3_pair_context_requires_retained_order_evidence():
    with pytest.raises(TypeError):
        ExplicitPairContext(scope(),scope(),descriptor(),descriptor(),("v1","v2"))


def test_phase3_contracts_do_not_execute_user_callbacks_or_io(monkeypatch,capsys):
    import builtins
    import socket
    calls=[]
    class Hostile:
        def __str__(self):
            calls.append(True); raise AssertionError("callback")
        def __bool__(self):
            calls.append(True); raise AssertionError("callback")
    def blocked(*args,**kwargs):
        raise AssertionError("unexpected IO")
    with monkeypatch.context() as patch:
        patch.setattr(builtins,"open",blocked)
        patch.setattr(socket,"create_connection",blocked)
        patch.setattr(socket,"getaddrinfo",blocked)
        assert NumericalPolicy().absolute_tolerance == 1e-12 and scenario().random_seed is None
        with pytest.raises((TypeError,ValueError)):
            replace(descriptor(),representation_name=Hostile())
    assert not calls and capsys.readouterr() == ("", "")


def test_phase3_approved_plan_and_baseline_control():
    control=json.loads((ROOT/"PHASE_3_BASELINE.json").read_text(encoding="utf-8"))
    assert hashlib.sha256((ROOT/"PHASE_3_PLAN.md").read_bytes()).hexdigest()==control["approved_plan_sha256"]
    tools()["verify_phase3_control"](control)


@pytest.mark.parametrize("key", ["baseline_commit","baseline_tree","baseline_test_tree","approved_plan_sha256",
                                 "active_phase","active_step","permitted_paths","approved_decisions","phase_complete"])
def test_phase3_forged_manifest_does_not_authorize_a_change(key):
    control=deepcopy(json.loads((ROOT/"PHASE_3_BASELINE.json").read_text(encoding="utf-8")))
    if key in ("active_phase","active_step"): control[key]+=1
    elif key=="phase_complete": control[key]=not control[key]
    elif key=="permitted_paths": control[key].append("src/recursive_integrity_toolkit/metrics/diversity.py")
    elif key=="approved_decisions": control[key].pop()
    else: control[key]="0"*40
    with pytest.raises(ValueError): tools()["verify_phase3_control"](control)


@pytest.mark.parametrize("status,path", [
    ("M","VALIDATION_PLAN.md"), ("M","src/recursive_integrity_toolkit/io/validation.py"),
    ("M","src/recursive_integrity_toolkit/metrics/diversity.py"), ("M","src/recursive_integrity_toolkit/cli.py"),
    ("A","tests/unit/test_arbitrary.py"), ("D","tests/conftest.py"), ("M","pyproject.toml"),
])
def test_phase3_unauthorized_path_change_fails(status,path):
    with pytest.raises(ValueError): tools()["verify_prior_step_changes"]([(status,path)], step=1)


def test_phase3_exact_new_file_set():
    t=tools(); t["verify_phase3_changes"]([("A",p) for p in t["STEP1_NEW"]])
    assert len(t["STEP1_NEW"])==6 and "VALIDATION_PLAN.md" not in t["STEP1_ALLOWED"]


def test_phase3_oracle_is_independent_source_transcription():
    path=ROOT/"tests/golden/phase3_math_cases.json"
    assert hashlib.sha256(path.read_bytes()).hexdigest()=="b494d50a1a9bd1009c060c998e4cb3c7433d0e8949f73a8d627e538fa38884b2"
    data=json.loads(path.read_text(encoding="utf-8")); cases=data["cases"]
    assert data["expectations_generated_by_implementation"] is False
    assert len(cases)==20 and len({c["case_id"] for c in cases})==20
    assert data["scalar_tolerances"]=={"atol":1e-12,"rtol":1e-12}
    for case in cases:
        assert case["source_sections"] and case["owner_ids"]
        assert not {"T4","T5","T6"} & set(case["owner_ids"])
    by_id={c["case_id"]:c for c in cases}
    assert by_id["F003-D"]["expected"]["gini_simpson_diversity"]=="5/8"
    assert by_id["HERO-PAIR"]["expected"]["lost_states"]==["battery","lizard","turtle"]
    assert by_id["HERO-EXTINCTION-CAT"]["expected"]["one_step_extinction_probability"]=="390625/16777216"
    # Authored literal comparisons only; no implementation calculates the oracle.


@pytest.mark.parametrize("body", ["return value ** 2", "return value / 2", "return sum(value)",
    "return open('private')", "return eval(value)", "return __import__('numpy')", "return math.sqrt(value)",
    "return (lambda: value)()"])
def test_phase3_contract_gate_rejects_hidden_calculation_or_execution(body):
    checker=runpy.run_path(str(ROOT/"scripts/check_traceability.py"),run_name="contract_boundary_test")
    with pytest.raises(SystemExit): checker["_phase3_contract_boundary"](ast.parse("def _calculation_number(value):\n    "+body+"\n"))


def test_phase3_current_model_passes_restricted_contract_gate():
    checker=runpy.run_path(str(ROOT/"scripts/check_traceability.py"),run_name="contract_boundary_test")
    checker["_phase3_contract_boundary"](ast.parse((ROOT/"src/recursive_integrity_toolkit/models.py").read_text(encoding="utf-8")))


def test_phase3_final_completion_records_not_created(phase3_step10_snapshot):
    for name in ("PHASE_3_COMPLETION.md","PHASE_3_VALIDATION_REPORT.md","PHASE_3_ARCHITECTURE_COMPLIANCE_REPORT.md"):
        assert not (phase3_step10_snapshot/name).exists()
