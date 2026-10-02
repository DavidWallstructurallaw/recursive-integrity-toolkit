"""Phase 2 Step 1 contract tests for PR-010 observability levels."""

import pytest

from recursive_integrity_toolkit.models import Capability, CapabilityKey, CapabilityStatus, ObservabilityAssessment


def _matrix() -> dict[CapabilityKey, Capability]:
    return {key: Capability(status=CapabilityStatus.UNAVAILABLE, reason_codes=("R_NOT_CLASSIFIED",)) for key in CapabilityKey}


def test_PR010_level_range_contract() -> None:
    for level in range(6):
        assert ObservabilityAssessment(level, _matrix()).maximum_level == level


@pytest.mark.parametrize("level", [-1, 6])
def test_PR010_out_of_range_level_rejected(level: int) -> None:
    with pytest.raises(ValueError):
        ObservabilityAssessment(level, _matrix())


def test_PR010_boolean_is_not_an_observability_level() -> None:
    with pytest.raises(TypeError):
        ObservabilityAssessment(True, _matrix())


# Phase 2 Step 8: evidence-bounded classification, no metrics or report assembly.
from dataclasses import replace
from types import MappingProxyType
import csv
import json

from recursive_integrity_toolkit.config import RepresentationConfig, ScenarioConfig
from recursive_integrity_toolkit.errors import CanonicalValidationError, ErrorCode
from recursive_integrity_toolkit.io.validation import assess_provenance_row, resolve_version_order, validate_canonical_values
from recursive_integrity_toolkit.models import CanonicalRow, ContentMode, ScenarioParameters
from recursive_integrity_toolkit.observability.levels import classify_observability


def _s8_record(identifier="a", version="v1", **fields):
    values = {"dataset_version": version, "record_id": identifier, "content": "synthetic", **fields}
    key = validate_canonical_values(values, kind="records")
    return CanonicalRow("records", key, MappingProxyType(values), MappingProxyType({}), MappingProxyType({}))


def _s8_provenance(identifier="a", version="v1", **fields):
    return assess_provenance_row({"dataset_version": version, "record_id": identifier,
        "source_type": "human", "provenance_confidence": "confirmed", "external_grounding": "yes",
        "parent_ids": (), **fields})


def _s8_order():
    return resolve_version_order(("v1", "v2"), document={"version_order": ["v1", "v2"]})


def _s8_rep(**changes):
    return replace(RepresentationConfig("topic", "topic_field", "topic", "topic-v1", "exclude"), **changes)


def _s8_parameters(**changes):
    return replace(ScenarioParameters("closed_resampling", 8, 4, 2, (("a", 0.25), ("b", 0.75))), **changes)


def test_PR010_minimal_file_is_level_zero():
    result = classify_observability((_s8_record(content="unread.txt"),), content_mode=ContentMode.LOCAL_REF)
    assert result.maximum_level == 0
    assert result.capabilities[CapabilityKey.INGESTION].status is CapabilityStatus.AVAILABLE
    assert result.capabilities[CapabilityKey.CONTENT_DIAGNOSTICS].status is CapabilityStatus.UNAVAILABLE


def test_PR010_records_only_is_level_one():
    assert classify_observability((_s8_record(),)).maximum_level == 1


def test_PR010_declared_field_can_qualify_without_reading_content():
    result = classify_observability((_s8_record(content="unread.txt", topic="cat"),),
                                    content_mode=ContentMode.LOCAL_REF, representation=_s8_rep())
    assert result.maximum_level == 1
    assert result.capabilities[CapabilityKey.CONTENT_DIAGNOSTICS].coverage_details["content"].numerator == 0


def test_PR010_partial_provenance_reaches_level_two():
    result = classify_observability((_s8_record("a"), _s8_record("b")),
                                    provenance=(_s8_provenance("a", external_grounding="unknown"),))
    assert result.maximum_level == 2
    assert result.capabilities[CapabilityKey.PROVENANCE].status is CapabilityStatus.PARTIAL


def test_PR010_valid_lineage_reaches_level_three():
    result = classify_observability((_s8_record("p"), _s8_record("c", "v2")),
        provenance=(_s8_provenance("p"), _s8_provenance("c", "v2", parent_ids=("v1::p",), external_grounding="no")),
        version_order=_s8_order())
    assert result.maximum_level == 3
    assert result.capabilities[CapabilityKey.LINEAGE].status is CapabilityStatus.AVAILABLE
    assert result.capabilities[CapabilityKey.DATASET_LONGITUDINAL].status is CapabilityStatus.UNAVAILABLE


def test_PR010_ordered_versions_reach_level_four():
    result = classify_observability((_s8_record("a", topic="cat"), _s8_record("b", "v2", topic="dog")),
                                    version_order=_s8_order(), representation=_s8_rep())
    assert result.maximum_level == 4
    assert result.capabilities[CapabilityKey.LINEAGE].status is CapabilityStatus.UNAVAILABLE
    assert result.capabilities[CapabilityKey.MODEL_LONGITUDINAL].status is CapabilityStatus.UNAVAILABLE


def test_PR010_valid_scenario_reaches_level_five():
    result = classify_observability((_s8_record(),), scenario=ScenarioConfig(True, 42), scenario_parameters=_s8_parameters())
    assert result.maximum_level == 5
    assert result.capabilities[CapabilityKey.INTERVENTION_SIMULATION].status is CapabilityStatus.EXPERIMENTAL
    assert result.capabilities[CapabilityKey.DATASET_LONGITUDINAL].status is CapabilityStatus.UNAVAILABLE
    assert "R_SCENARIO_EXECUTION_DEFERRED" in result.limitations
    assert not hasattr(result, "simulations")


def test_PR010_hero_reaches_level_four(repo_root):
    # Full load/map/normalize orchestration remains Step 9. This test independently
    # parses the synthetic fixed CSVs and checks classification only.
    folder = repo_root / "examples/hero"
    paths = tuple(folder / name for name in ("records_v1.csv", "records_v2.csv", "provenance.csv", "config.json", "version_order.json", "EXPECTED_OUTPUTS.md"))
    before = tuple(path.read_bytes() for path in paths)
    records = []
    for path in paths[:2]:
        with path.open(encoding="utf-8", newline="") as stream:
            for values in csv.DictReader(stream):
                key = validate_canonical_values(dict(values), kind="records")
                records.append(CanonicalRow("records", key, MappingProxyType(values), MappingProxyType({}), MappingProxyType({})))
    provenance = []
    with paths[2].open(encoding="utf-8", newline="") as stream:
        for values in csv.DictReader(stream):
            values["parent_ids"] = tuple(json.loads(values["parent_ids"]))
            values["generation"] = int(values["generation"])
            values["human_reviewed"] = {"true": True, "false": False}[values["human_reviewed"]]
            provenance.append(assess_provenance_row(values))
    declaration = json.loads(paths[3].read_text(encoding="utf-8"))["representation"]
    order = resolve_version_order(("v1", "v2"), document=json.loads(paths[4].read_text(encoding="utf-8")))
    result = classify_observability(tuple(records), provenance=tuple(provenance),
                                    representation=RepresentationConfig(**declaration), version_order=order)
    assert result.maximum_level == 4
    for key in (CapabilityKey.INGESTION, CapabilityKey.CONTENT_DIAGNOSTICS, CapabilityKey.PROVENANCE,
                CapabilityKey.LINEAGE, CapabilityKey.DATASET_LONGITUDINAL):
        assert result.capabilities[key].status is CapabilityStatus.AVAILABLE
    assert result.capabilities[CapabilityKey.MODEL_LONGITUDINAL].status is CapabilityStatus.UNAVAILABLE
    assert result.capabilities[CapabilityKey.INTERVENTION_SIMULATION].status is CapabilityStatus.UNAVAILABLE
    assert not result.validation_messages
    assert tuple(path.read_bytes() for path in paths) == before
    # EXPECTED_OUTPUTS is compared byte-for-byte only; no analytical value is used.


def test_PR010_no_valid_records_does_not_certify_level_zero():
    with pytest.raises(CanonicalValidationError) as exc:
        classify_observability(())
    assert exc.value.code is ErrorCode.EMPTY_DATASET


def test_PR010_duplicate_keys_fail_before_classification():
    with pytest.raises(CanonicalValidationError) as exc:
        classify_observability((_s8_record(), _s8_record()))
    assert exc.value.code is ErrorCode.RECORD_DUPLICATE_ID


@pytest.mark.parametrize("value", [0, -1, True, 1.0, "1"])
def test_PR010_invalid_requested_count_rejected(value):
    with pytest.raises(CanonicalValidationError):
        classify_observability((_s8_record(),), requested_record_count=value)


@pytest.mark.parametrize("flag", ["semantic_requested", "model_evidence_present", "state_mapping_present", "strict_mode"])
def test_PR010_no_implicit_flag_truthiness(flag):
    with pytest.raises(CanonicalValidationError):
        classify_observability((_s8_record(),), **{flag: 1})


def test_PR010_forged_record_contract_is_not_trusted():
    record = _s8_record()
    with pytest.raises(CanonicalValidationError):
        classify_observability((replace(record, values={"record_id": "a", "dataset_version": "v2", "content": "data"}),))


def test_PR010_forged_order_flags_are_not_trusted():
    order = replace(_s8_order(), order=(), order_source="unavailable")
    result = classify_observability((_s8_record("a", topic="cat"), _s8_record("b", "v2", topic="dog")),
                                    representation=_s8_rep(), version_order=order)
    assert result.maximum_level == 4


def test_PR010_enabled_and_seed_alone_never_grant_level_five():
    result = classify_observability((_s8_record(),), scenario=ScenarioConfig(True, 42))
    assert result.maximum_level == 1
    assert "R_SCENARIO_PARAMETERS_MISSING" in result.limitations


@pytest.mark.parametrize("seed", [None, True, 1.5, "2"])
def test_PR010_scenario_requires_recorded_integer_seed(seed):
    result = classify_observability((_s8_record(),), scenario=ScenarioConfig(True, seed), scenario_parameters=_s8_parameters())
    assert result.maximum_level != 5


@pytest.mark.parametrize("field,value", [
    ("resample_size", None), ("resample_size", 0), ("resample_size", True), ("resample_size", 1.5),
    ("simulation_horizon", None), ("simulation_horizon", -1), ("simulation_horizon", True),
    ("simulation_replicates", None), ("simulation_replicates", 0), ("simulation_replicates", False),
    ("model_name", "arbitrary_model"), ("state_distribution", None), ("state_distribution", ()),
    ("state_distribution", (("a", 0.3), ("b", 0.6))), ("state_distribution", (("a", 0.5), ("a", 0.5))),
    ("state_distribution", (("a", float("nan")),)), ("state_distribution", (("a", float("inf")),)),
    ("state_distribution", (("a", True),)), ("state_distribution", (("a", -0.1), ("b", 1.1))),
    ("state_distribution", (("", 1.0),)), ("state_distribution", (("a", 10 ** 1000),)), ("reopening_weight", 0.5),
])
def test_PR010_invalid_scenario_parameters_do_not_unlock(field, value):
    result = classify_observability((_s8_record(),), scenario=ScenarioConfig(True, 42),
                                    scenario_parameters=_s8_parameters(**{field: value}))
    assert result.maximum_level == 1
    assert result.capabilities[CapabilityKey.INTERVENTION_SIMULATION].status is CapabilityStatus.UNAVAILABLE


@pytest.mark.parametrize("weight", [0, 0.2, 1])
def test_PR010_reopening_eligibility_is_only_parameter_validation(weight):
    parameters = _s8_parameters(model_name="reopened_resampling", reopening_weight=weight,
                                external_input_distribution=(("a", 0.1), ("b", 0.9)))
    result = classify_observability((_s8_record(),), scenario=ScenarioConfig(True, 42), scenario_parameters=parameters)
    assert result.maximum_level == 5
    assert "R_SCENARIO_EXECUTION_DEFERRED" in result.limitations


@pytest.mark.parametrize("weight,external", [
    (None, (("a", 0.1), ("b", 0.9))), (float("nan"), (("a", 0.1), ("b", 0.9))),
    (-0.1, (("a", 0.1), ("b", 0.9))), (True, (("a", 0.1), ("b", 0.9))),
    (0.5, None), (0.5, (("z", 1.0),)), (0.5, (("a", 0.1), ("b", 0.8))),
])
def test_PR010_invalid_reopening_inputs_remain_unavailable(weight, external):
    parameters = _s8_parameters(model_name="reopened_resampling", reopening_weight=weight,
                                external_input_distribution=external)
    result = classify_observability((_s8_record(),), scenario=ScenarioConfig(True, 42), scenario_parameters=parameters)
    assert result.maximum_level == 1


def test_PR010_disabled_scenario_does_not_promote_with_valid_parameters():
    assert classify_observability((_s8_record(),), scenario=ScenarioConfig(False, 42),
                                   scenario_parameters=_s8_parameters()).maximum_level == 1


def test_PR010_zero_horizon_is_valid_but_does_not_execute():
    assert classify_observability((_s8_record(),), scenario=ScenarioConfig(True, 42),
                                   scenario_parameters=_s8_parameters(simulation_horizon=0)).maximum_level == 5


def test_PR010_unsafe_model_name_rejected_before_equality_callback():
    class Unsafe:
        def __eq__(self, other):
            raise AssertionError("untrusted callback")
    with pytest.raises(CanonicalValidationError):
        classify_observability((_s8_record(),), scenario=ScenarioConfig(True, 42),
                               scenario_parameters=_s8_parameters(model_name=Unsafe()))
