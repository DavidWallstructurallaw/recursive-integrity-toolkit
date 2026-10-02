"""Execute all twenty frozen Step 1 oracles without regenerating expected values.

Authorities: PHASE_3_PLAN sections 8.1-8.3 and each case's source_sections.
Probability vectors used for diversity-only F-015 inputs are explicit mathematical
witnesses of the supplied initial diversity, not invented empirical records.
"""
from fractions import Fraction
from dataclasses import replace
from pathlib import Path
import hashlib
import json
import pytest

from recursive_integrity_toolkit.metrics.diversity import distribution_from_counts, distribution_from_probabilities
from recursive_integrity_toolkit.metrics.bounds import closure_exposure_bounds
from recursive_integrity_toolkit.metrics.tail import one_step_extinction_probability
from recursive_integrity_toolkit.metrics.resampling import expected_diversity_after_steps
from recursive_integrity_toolkit.models import CalculationScope, RecordKey, RepresentationDescriptor, CalculationEvidenceClass, CapabilityKey, CapabilityStatus

ORACLE = Path(__file__).with_name("phase3_math_cases.json")
CASES = json.loads(ORACLE.read_bytes())["cases"]


def _exact(value):
    return pytest.approx(float(Fraction(value)), abs=1e-12, rel=1e-12)


def _scope(size):
    return CalculationScope(("math-v1",), tuple(RecordKey("math-v1", str(i)) for i in range(size)), (), "declared_mathematical_scope", "frozen-hand-case")


def _representation():
    return RepresentationDescriptor("mathematical_states", "explicit_state_distribution", "v1", "literal_named_states")


@pytest.mark.parametrize("case", CASES, ids=[c["case_id"] for c in CASES])
def test_phase3_frozen_case(case, phase3_hero_pipeline):
    before = ORACLE.read_bytes()
    inputs, expected, identity = case["inputs"], case["expected"], case["case_id"]
    assert case["source_sections"] and case["owner_ids"]
    if identity == "F001-A":
        result = distribution_from_counts(inputs["counts"], scope=_scope(expected["record_count"]), representation=_representation())
        assert result.analyzed_record_count == expected["record_count"]
        assert {s.state_id:s.state_frequency for s in result.states} == {k:_exact(v) for k,v in expected["frequencies"].items()}
    elif identity.startswith(("F002-", "F003-")):
        probabilities = tuple((str(i), float(Fraction(v))) for i,v in enumerate(inputs["probabilities"]))
        result = distribution_from_probabilities(probabilities, scope=_scope(1), representation=_representation())
        if "support_size" in expected:
            assert result.support_size.value == expected["support_size"]
        if "gini_simpson_diversity" in expected:
            assert result.gini_simpson_diversity.value == _exact(expected["gini_simpson_diversity"])
    elif identity == "DIRECT-A":
        result = closure_exposure_bounds(known_closed=inputs["known_closed"], unresolved=inputs["unresolved"], total=inputs["record_count"], scope=replace(_scope(inputs["record_count"]), denominator_basis="all_valid_records_in_selected_dataset_scope"))
        assert result.lower_bound.value == _exact(expected["lower"])
        assert result.upper_bound.value == _exact(expected["upper"])
        assert result.interval_width.value == _exact(expected["width"])
    elif identity.startswith(("F014-", "HERO-EXTINCTION-")):
        result = one_step_extinction_probability(float(Fraction(inputs["probability"])), resample_size=inputs["resample_size"], state_id="selected", scope=_scope(1), representation=_representation())
        assert result.one_step_extinction_probability.value == _exact(expected["one_step_extinction_probability"])
        assert result.evidence_class is CalculationEvidenceClass.SIMULATION and result.random_seed is None
    elif identity.startswith(("F015-", "HERO-EXPECTATION-")):
        witnesses = {"1/2": ("1/2", "1/2"), "3/4": ("1/4",)*4, "7/8": ("1/8",)*8}
        probabilities = tuple((str(i), float(Fraction(v))) for i,v in enumerate(witnesses[inputs["gini_simpson_diversity"]]))
        result = expected_diversity_after_steps(probabilities, resample_size=inputs["resample_size"], steps=inputs["simulation_horizon"], scope=_scope(1), representation=_representation())
        assert result.initial_gini_simpson_diversity == _exact(inputs["gini_simpson_diversity"])
        assert result.expected_diversity[-1] == _exact(expected["expected_gini_simpson_diversity"])
        assert result.evidence_class is CalculationEvidenceClass.SIMULATION and result.random_seed is None
    elif identity == "HERO-SINGLE":
        result = phase3_hero_pipeline()
        v1, v2 = (result["distributions"][v].unweighted for v in ("v1", "v2"))
        for version, distribution in (("v1",v1),("v2",v2)):
            assert distribution.analyzed_record_count == expected["record_count"][version]
            assert distribution.representation.representation_name == inputs["representation_name"]
            assert distribution.representation.representation_version == inputs["representation_version"]
            assert distribution.support_size.value == expected[version+"_support"]
            assert distribution.gini_simpson_diversity.value == _exact(expected[version+"_diversity"])
        assert {s.state_id:s.state_count for s in v2.states} == expected["v2_counts"]
        provenance = result["provenance"]["v2"]
        shares = dict(provenance.source.shares, missing_provenance=provenance.missing_provenance_share.value)
        assert shares == {k:_exact(v) for k,v in expected["v2_source_shares"].items()}
        for field, name in (("row","provenance_row_coverage"),("required_fields","provenance_required_field_coverage"),("grounding","grounding_field_coverage")):
            assert getattr(provenance,name).ratio == _exact(expected["v2_coverage"][field])
        bounds = result["bounds"]["v2"]
        for key,name in (("lower","lower_bound"),("upper","upper_bound"),("width","interval_width")):
            assert getattr(bounds,name).value == _exact(expected["v2_direct_bounds"][key])
    elif identity == "HERO-PAIR":
        pair = phase3_hero_pipeline()["pair"]
        assert pair.support_delta.value == expected["support_delta"]
        assert pair.support_retention_ratio.value == _exact(expected["support_retention"])
        assert pair.gini_simpson_diversity_delta.value == _exact(expected["diversity_delta"])
        assert pair.extinct_states == tuple(expected["lost_states"])
        assert pair.added_states == tuple(expected["added_states"])
    elif identity == "HERO-INPUT":
        result = phase3_hero_pipeline()
        assert result["bundle"].observability.maximum_level == expected["maximum_level"]
        assert result["bundle"].observability.capabilities[CapabilityKey.MODEL_LONGITUDINAL].status is CapabilityStatus.UNAVAILABLE
        assert expected["model_longitudinal"] == "unavailable" and expected["simulation_executed"] is False
        assert result["config"].simulation.enabled is False
        assert "simulation" not in result
    else:
        pytest.fail("Frozen case has no explicit executor: " + identity)
    assert ORACLE.read_bytes() == before


def test_phase3_all_twenty_oracles_have_unique_traceable_identity():
    data = json.loads(ORACLE.read_bytes())
    assert len(CASES) == len({c["case_id"] for c in CASES}) == 20
    assert data["expectations_generated_by_implementation"] is False
    assert data["excluded_owners"] == ["T4", "T5", "T6", "T3 lineage branch"]
    assert data["scalar_tolerances"] == dict(atol=1e-12, rtol=1e-12)
    plan = ORACLE.parents[2] / "PHASE_3_PLAN.md"
    assert hashlib.sha256(plan.read_bytes()).hexdigest() == data["approved_plan_sha256"]
