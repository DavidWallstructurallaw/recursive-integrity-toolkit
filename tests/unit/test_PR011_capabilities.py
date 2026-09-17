"""Phase 2 Step 1 contract tests for PR-011 capability matrix vocabulary."""

import pytest

from recursive_integrity_toolkit.models import Capability, CapabilityKey, CapabilityStatus, ObservabilityAssessment, ValidationCoverage


EXPECTED_KEYS = {"ingestion", "content_diagnostics", "provenance", "lineage", "dataset_longitudinal", "model_longitudinal", "intervention_simulation"}


def test_PR011_capability_keys_are_exact() -> None:
    assert {key.value for key in CapabilityKey} == EXPECTED_KEYS


def test_PR011_capability_status_values_are_exact() -> None:
    assert {status.value for status in CapabilityStatus} == {"available", "partial", "unavailable", "experimental"}


def test_PR011_coverage_denominator_is_named() -> None:
    coverage = ValidationCoverage(3, 4, "requested records")
    capability = Capability(CapabilityStatus.PARTIAL, coverage=coverage)
    assert capability.coverage is not None
    assert capability.coverage.denominator_name == "requested records"


def test_PR011_complete_matrix_is_required() -> None:
    with pytest.raises(ValueError):
        ObservabilityAssessment(0, {CapabilityKey.INGESTION: Capability(CapabilityStatus.AVAILABLE)})


# Phase 2 Step 8: independent capability eligibility and retained limitations.
from dataclasses import replace
from types import MappingProxyType
import json

from recursive_integrity_toolkit.config import RepresentationConfig, ScenarioConfig
from recursive_integrity_toolkit.errors import CanonicalValidationError, ErrorCode, WarningCode
from recursive_integrity_toolkit.io.validation import assess_provenance_row, resolve_version_order, validate_canonical_values
from recursive_integrity_toolkit.models import CanonicalRow, ContentMode, RecordKey, ValidationMessage, ValidationSeverity
from recursive_integrity_toolkit.observability.levels import REASON_CODES, classify_observability


def _c8_record(identifier="a", version="v1", **fields):
    values = {"dataset_version": version, "record_id": identifier, "content": "synthetic", **fields}
    key = validate_canonical_values(values, kind="records")
    return CanonicalRow("records", key, MappingProxyType(values), MappingProxyType({}), MappingProxyType({}))


def _c8_prov(identifier="a", version="v1", **fields):
    return assess_provenance_row({"dataset_version": version, "record_id": identifier,
        "source_type": "human", "provenance_confidence": "confirmed", "external_grounding": "yes",
        "parent_ids": (), **fields})


def _c8_rep(**changes):
    return replace(RepresentationConfig("topic", "topic_field", "topic", "topic-v1", "exclude"), **changes)


def _c8_order():
    return resolve_version_order(("v1", "v2"), invocation_order=("v1", "v2"))


def test_PR011_complete_independent_matrix_and_readonly_result():
    result = classify_observability((_c8_record(),))
    assert set(result.capabilities) == set(CapabilityKey)
    for capability in result.capabilities.values():
        if capability.status in (CapabilityStatus.PARTIAL, CapabilityStatus.UNAVAILABLE):
            assert capability.reason_codes and capability.requirements_missing
        assert set(capability.reason_codes) <= REASON_CODES
        assert capability.notes
        if capability.coverage:
            assert capability.coverage.denominator_name
    with pytest.raises(TypeError):
        result.capabilities[CapabilityKey.INGESTION] = Capability(CapabilityStatus.UNAVAILABLE)


def test_PR011_input_partial_preserves_error_and_valid_scope():
    message = ValidationMessage("E_FILE_PARSE", ValidationSeverity.ERROR, "input row failed")
    result = classify_observability((_c8_record(),), requested_record_count=2, input_messages=(message,))
    assert result.capabilities[CapabilityKey.INGESTION].status is CapabilityStatus.PARTIAL
    assert result.capabilities[CapabilityKey.INGESTION].coverage.ratio == 0.5
    assert result.validation_messages[0] == message


def test_PR011_unknown_failed_input_denominator_remains_none():
    message = ValidationMessage("E_FILE_PARSE", ValidationSeverity.ERROR, "input file failed")
    result = classify_observability((_c8_record(),), input_messages=(message,))
    assert result.capabilities[CapabilityKey.INGESTION].coverage is None
    assert result.capabilities[CapabilityKey.INGESTION].status is CapabilityStatus.PARTIAL


@pytest.mark.parametrize("source", ["human", "synthetic", "mixed", "sensor", "unknown"])
@pytest.mark.parametrize("grounding", ["yes", "no", "unknown"])
def test_PR011_source_type_never_substitutes_for_grounding(source, grounding):
    provenance = _c8_prov(source_type=source, external_grounding=grounding, human_reviewed=True)
    result = classify_observability((_c8_record(),), provenance=(provenance,))
    cap = result.capabilities[CapabilityKey.PROVENANCE]
    assert cap.status is (CapabilityStatus.PARTIAL if grounding == "unknown" else CapabilityStatus.AVAILABLE)
    assert cap.coverage_details["grounding"].numerator == (0 if grounding == "unknown" else 1)
    assert provenance.values["source_type"] == source and provenance.values["external_grounding"] == grounding


def test_PR011_three_provenance_coverage_bases_stay_separate():
    incomplete = assess_provenance_row({"dataset_version": "v1", "record_id": "b",
                                       "source_type": "human", "external_grounding": "yes"})
    result = classify_observability((_c8_record("a"), _c8_record("b"), _c8_record("c")),
                                    provenance=(_c8_prov("a", external_grounding="unknown"), incomplete))
    cap = result.capabilities[CapabilityKey.PROVENANCE]
    assert cap.status is CapabilityStatus.PARTIAL
    assert tuple(cap.coverage_details[name].numerator for name in ("row", "required_fields", "grounding")) == (2, 1, 1)
    assert all(value.denominator == 3 for value in cap.coverage_details.values())
    assert any(message.code == ErrorCode.SCHEMA_REQUIRED_FIELD.value for message in result.validation_messages)
    assert "provenance_confidence" not in incomplete.values


def test_PR011_no_valid_provenance_does_not_unlock_level_two():
    incomplete = assess_provenance_row({"dataset_version": "v1", "record_id": "a", "external_grounding": "yes"})
    result = classify_observability((_c8_record(),), provenance=(incomplete,))
    assert result.maximum_level == 1
    assert result.capabilities[CapabilityKey.PROVENANCE].status is CapabilityStatus.UNAVAILABLE
    assert result.validation_messages


def test_PR011_unknown_is_distinct_from_missing_manifest():
    a = classify_observability((_c8_record(),))
    b = classify_observability((_c8_record(),), provenance=())
    c = classify_observability((_c8_record(),), provenance=(_c8_prov(external_grounding="unknown"),))
    assert "R_PROVENANCE_NOT_SUPPLIED" in a.limitations
    assert "R_PROVENANCE_NOT_SUPPLIED" not in b.limitations
    assert c.maximum_level == 2 and c.capabilities[CapabilityKey.PROVENANCE].coverage.ratio == 1.0


def test_PR011_partial_lineage_has_named_reference_coverage():
    result = classify_observability((_c8_record("p"), _c8_record("c", "v2")),
        provenance=(_c8_prov("p"), _c8_prov("c", "v2", parent_ids=("v1::p", "v1::unloaded"))),
        version_order=_c8_order())
    cap = result.capabilities[CapabilityKey.LINEAGE]
    assert cap.status is CapabilityStatus.PARTIAL and cap.coverage.ratio == 0.5
    assert cap.coverage.denominator_name == "declared_parent_reference_entries"
    assert "R_PARENT_UNRESOLVED" in cap.reason_codes
    assert result.maximum_level == 2


def test_PR011_alias_entries_reconcile_without_ancestry_claim():
    result = classify_observability((_c8_record("p"), _c8_record("c", "v2")),
        provenance=(_c8_prov("p"), _c8_prov("c", "v2", parent_ids=("v1::p", "p", "v1::missing"))),
        version_order=_c8_order())
    cap = result.capabilities[CapabilityKey.LINEAGE]
    assert cap.coverage.numerator == 2 and cap.coverage.denominator == 3
    assert not hasattr(cap, "resolved_ancestry")


def test_PR011_same_version_cycle_is_deferred_not_diagnosed():
    result = classify_observability((_c8_record("a"), _c8_record("b")),
        provenance=(_c8_prov("a", parent_ids=("v1::b",)), _c8_prov("b", parent_ids=("v1::a",))))
    cap = result.capabilities[CapabilityKey.LINEAGE]
    assert cap.status is CapabilityStatus.PARTIAL
    assert "R_GRAPH_VALIDATION_DEFERRED" in cap.reason_codes
    assert result.maximum_level == 2
    assert not any(message.code == ErrorCode.LINEAGE_CYCLE.value for message in result.validation_messages)


@pytest.mark.parametrize("parents,code,reason", [
    (("v2::c",), ErrorCode.LINEAGE_CYCLE, "R_PARENT_INVALID"),
    (("v3::future",), ErrorCode.PARENT_FUTURE_VERSION, "R_PARENT_INVALID"),
    (("p",), ErrorCode.PARENT_AMBIGUOUS, "R_PARENT_AMBIGUOUS"),
])
def test_PR011_bad_lineage_does_not_destroy_valid_dataset_capability(parents, code, reason):
    records = (_c8_record("p", topic="cat"), _c8_record("p", "v2", topic="cat"), _c8_record("c", "v2", topic="dog"))
    order = resolve_version_order(("v1", "v2"), document={"version_order": ["v1", "v2", "v3"]})
    result = classify_observability(records, provenance=(_c8_prov("p"), _c8_prov("p", "v2"),
                                    _c8_prov("c", "v2", parent_ids=parents)),
                                    representation=_c8_rep(), version_order=order)
    assert result.maximum_level == 4
    assert result.capabilities[CapabilityKey.LINEAGE].status is CapabilityStatus.UNAVAILABLE
    assert reason in result.limitations
    assert any(message.code == code.value and message.severity is ValidationSeverity.ERROR
               for message in result.validation_messages)


def test_PR011_strict_promotion_blocks_affected_eligibility_without_changing_counts():
    rows = (_c8_record("p"), _c8_record("c", "v2"))
    provenance = (_c8_prov("p"), _c8_prov("c", "v2", parent_ids=("p",)))
    result = classify_observability(rows, provenance=provenance, version_order=_c8_order(),
             strict_mode=True, strict_warning_codes=(WarningCode.PARENT_BARE_COMPATIBILITY.value,))
    assert result.maximum_level == 2
    assert result.capabilities[CapabilityKey.LINEAGE].status is CapabilityStatus.PARTIAL
    assert result.capabilities[CapabilityKey.LINEAGE].coverage.ratio == 1.0
    assert any(message.severity is ValidationSeverity.ERROR for message in result.validation_messages)


@pytest.mark.parametrize("grounding", ["unknown", "no"])
def test_PR011_unknown_or_ungrounded_root_prevents_full_lineage(grounding):
    result = classify_observability((_c8_record("p"), _c8_record("c", "v2")),
        provenance=(_c8_prov("p", external_grounding=grounding), _c8_prov("c", "v2", parent_ids=("v1::p",))),
        version_order=_c8_order())
    assert result.capabilities[CapabilityKey.LINEAGE].status is CapabilityStatus.PARTIAL
    assert result.maximum_level == 3  # Acyclic path evidence remains separate from grounding coverage.


def test_PR011_missing_parent_declaration_never_certifies_complete_ancestry():
    result = classify_observability((_c8_record("p"), _c8_record("c", "v2")),
        provenance=(_c8_prov("p", parent_ids=None), _c8_prov("c", "v2", parent_ids=("v1::p",))),
        version_order=_c8_order())
    assert result.capabilities[CapabilityKey.LINEAGE].status is CapabilityStatus.PARTIAL
    assert result.maximum_level == 2


def test_PR011_unread_local_references_do_not_become_analyzable_strings():
    row = _c8_record(content="sub/secret.txt")
    a = classify_observability((row,), content_mode=ContentMode.LOCAL_REF)
    b = classify_observability((row,), content_mode=ContentMode.LOCAL_REF,
                              resolved_content={row.record_key: "already read synthetic text"})
    assert a.maximum_level == 0 and b.maximum_level == 1
    assert row.values["content"] == "sub/secret.txt"


@pytest.mark.parametrize("text", ["", "  ", "binary\x00data", "\ud800", 1, True])
def test_PR011_invalid_content_evidence_is_rejected(text):
    row = _c8_record(content="local.txt")
    with pytest.raises(CanonicalValidationError):
        classify_observability((row,), content_mode=ContentMode.LOCAL_REF, resolved_content={row.record_key: text})


def test_PR011_content_evidence_must_match_scope_and_mode():
    with pytest.raises(CanonicalValidationError):
        classify_observability((_c8_record(),), resolved_content={RecordKey("v1", "a"): "data"})
    with pytest.raises(CanonicalValidationError):
        classify_observability((_c8_record(),), content_mode=ContentMode.LOCAL_REF,
                               resolved_content={RecordKey("v1", "other"): "data"})


@pytest.mark.parametrize("policy,expected", [("exclude", CapabilityStatus.PARTIAL),
                                           ("error", CapabilityStatus.UNAVAILABLE),
                                           ("explicit_missing_state", CapabilityStatus.UNAVAILABLE)])
def test_PR011_missing_representation_policy_does_not_impute_states(policy, expected):
    records = (_c8_record("a", topic="cat"), _c8_record("b", "v2", topic="dog"), _c8_record("c", "v2"))
    result = classify_observability(records, representation=_c8_rep(missing_value_policy=policy), version_order=_c8_order())
    assert result.capabilities[CapabilityKey.DATASET_LONGITUDINAL].status is expected
    assert "topic" not in records[-1].values
    assert result.capabilities[CapabilityKey.CONTENT_DIAGNOSTICS].status is CapabilityStatus.PARTIAL


def test_PR011_record_form_does_not_claim_semantic_capability():
    rep = RepresentationConfig("record_form", "content_hash", normalization_profile="exact_utf8_v1")
    result = classify_observability((_c8_record(),), representation=rep, semantic_requested=True)
    assert result.capabilities[CapabilityKey.CONTENT_DIAGNOSTICS].status is CapabilityStatus.PARTIAL
    assert "R_SEMANTIC_EVIDENCE_MISSING" in result.limitations
    assert result.maximum_level == 1


def test_PR011_no_representation_means_no_longitudinal_state_comparison():
    result = classify_observability((_c8_record("a"), _c8_record("b", "v2")), version_order=_c8_order())
    assert result.capabilities[CapabilityKey.DATASET_LONGITUDINAL].status is CapabilityStatus.UNAVAILABLE
    assert result.maximum_level == 1


@pytest.mark.parametrize("source", ["embedding_clusters", "config", "unapproved"])
def test_PR011_unimplemented_representation_validation_never_becomes_semantic(source):
    result = classify_observability((_c8_record(),), representation=_c8_rep(source=source), semantic_requested=True)
    assert "R_REPRESENTATION_VALIDATION_DEFERRED" in result.limitations
    assert result.capabilities[CapabilityKey.CONTENT_DIAGNOSTICS].status is CapabilityStatus.PARTIAL


@pytest.mark.parametrize("directory,expected", [("representation_compatible", CapabilityStatus.AVAILABLE),
                                                ("representation_incompatible", CapabilityStatus.UNAVAILABLE)])
def test_PR011_explicit_compatibility_fixture(repo_root, directory, expected):
    path = repo_root / "tests/fixtures" / directory / "step8_declarations.json"
    before = path.read_bytes()
    declaration = json.loads(before)
    result = classify_observability((_c8_record("a", topic="cat"), _c8_record("b", "v2", topic="dog")),
                representation=_c8_rep(version=None), version_order=_c8_order(),
                representation_compatibility=tuple(sorted(declaration["representation_compatibility"].items())))
    assert result.capabilities[CapabilityKey.DATASET_LONGITUDINAL].status is expected
    assert path.read_bytes() == before


def test_PR011_state_mapping_presence_does_not_execute_or_certify_it():
    result = classify_observability((_c8_record("a", topic="cat"), _c8_record("b", "v2", topic="dog")),
                representation=_c8_rep(), version_order=_c8_order(), state_mapping_present=True)
    assert "R_REPRESENTATION_MAPPING_DEFERRED" in result.limitations and result.maximum_level == 1


@pytest.mark.parametrize("pairs", [(("v1", "x"),), (("v1", "x"), ("v2", "y")), (("v1", "x"), ("v2", "x"))])
def test_PR011_conflicting_or_missing_representation_ids_block_comparison(pairs):
    result = classify_observability((_c8_record("a", topic="cat"), _c8_record("b", "v2", topic="dog")),
                representation=_c8_rep(), version_order=_c8_order(), representation_compatibility=pairs)
    assert result.capabilities[CapabilityKey.DATASET_LONGITUDINAL].status is CapabilityStatus.UNAVAILABLE


@pytest.mark.parametrize("evidence_present", [False, True])
def test_PR011_model_evidence_presence_never_substitutes_for_validation(evidence_present):
    result = classify_observability((_c8_record("a", topic="cat"), _c8_record("b", "v2", topic="dog")),
                representation=_c8_rep(), version_order=_c8_order(), model_evidence_present=evidence_present)
    assert result.maximum_level == 4
    assert result.capabilities[CapabilityKey.MODEL_LONGITUDINAL].status is CapabilityStatus.UNAVAILABLE


def test_PR011_order_permutation_and_source_payloads_do_not_change_classification():
    records = (_c8_record("a", topic="cat", notes="PRIVATE_SENTINEL"), _c8_record("b", "v2", topic="dog"))
    provenance = (_c8_prov("a"), _c8_prov("b", "v2", parent_ids=("v1::a",)))
    left = classify_observability(records, provenance=provenance, representation=_c8_rep(), version_order=_c8_order())
    right = classify_observability(tuple(reversed(records)), provenance=tuple(reversed(provenance)),
                                  representation=_c8_rep(), version_order=_c8_order())
    assert left == right and "PRIVATE_SENTINEL" not in repr(left)


def test_PR011_classifier_is_offline_side_effect_free_and_does_not_import_later_layers(monkeypatch, tmp_path, capsys):
    import builtins
    import socket
    import sys
    from pathlib import Path
    records = (_c8_record("a", content="PRIVATE_SENTINEL", topic="https://inert.example/value"),)
    modules_before = set(sys.modules)
    def blocked(*args, **kwargs):
        raise AssertionError("classifier attempted IO or execution")
    with monkeypatch.context() as patch:
        patch.setattr(builtins, "open", blocked)
        patch.setattr(builtins, "eval", blocked)
        patch.setattr(builtins, "exec", blocked)
        patch.setattr(Path, "open", blocked)
        patch.setattr(socket, "getaddrinfo", blocked)
        patch.setattr(socket, "create_connection", blocked)
        result = classify_observability(records, provenance=(_c8_prov(),), representation=_c8_rep())
    assert not set(sys.modules) - modules_before
    assert list(tmp_path.iterdir()) == []
    assert capsys.readouterr() == ("", "")
    assert "PRIVATE_SENTINEL" not in repr(result)
    for name in ("derived_metrics", "proxy_signals", "simulations", "report", "source_type_shares", "ancestry_hhi"):
        assert not hasattr(result, name)
