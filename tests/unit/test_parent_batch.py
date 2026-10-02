"""Direct parent-retention behavior, shared interpretation and boundary tests."""

from dataclasses import FrozenInstanceError, replace
from types import MappingProxyType

import pytest

from recursive_integrity_toolkit.errors import CanonicalValidationError, ErrorCode, WarningCode
from recursive_integrity_toolkit.io.normalization import normalize_row
from recursive_integrity_toolkit.io import validation
from recursive_integrity_toolkit.models import (
    ParentResolutionStatus, RecordKey, ValidationSeverity,
)


_ABSENT = object()


def row(identifier, parents=_ABSENT, *, version="v1", grounding="no"):
    values = {"dataset_version": version, "record_id": identifier,
              "source_type": "unknown", "provenance_confidence": "confirmed",
              "external_grounding": grounding}
    if parents is not _ABSENT:
        values["parent_ids"] = parents
    return normalize_row(values, kind="provenance")


def batch(rows, **options):
    return validation.resolve_parent_batch(tuple(item.record_key for item in rows), rows, **options)


def test_parent_batch_preserves_declaration_states_and_missing_provenance():
    rows = (row("absent"), row("null", None), row("empty", []), row("child", ["v1::empty"]))
    missing = RecordKey("v1", "missing")
    result = validation.resolve_parent_batch(tuple(item.record_key for item in rows) + (missing,), rows)
    by_key = {item.child_key.record_id: item for item in result.assessments}
    assert {key: item.result.declaration_state for key, item in by_key.items()} == {
        "absent": "absent", "null": "null", "empty": "empty", "child": "declared", "missing": "absent"}
    assert by_key["missing"].provenance_available is False
    assert all(by_key[key].provenance_available for key in ("absent", "null", "empty", "child"))
    assert sum(item.declared_reference_count for item in result.assessments) == 1
    assert sum(item.resolved_reference_count for item in result.assessments) == 1


def test_parent_batch_retains_all_failures_valid_siblings_and_alias_counts():
    rows = (row("p", [], grounding="yes"), row("p", [], version="v2", grounding="yes"),
            row("future", [], version="v3"),
            row("child", ["v1::p", "v1::p", "v1::missing", "p", "v3::future",
                          "v2::child", "child", "private malformed reference "], version="v2"))
    order = validation.resolve_version_order(("v1", "v2", "v3"), invocation_order=("v1", "v2", "v3"))
    result = batch(rows, version_order=order)
    evidence = next(item for item in result.assessments if item.child_key.record_id == "child")
    assert evidence.declared_reference_count == 8
    assert evidence.resolved_reference_count == 2
    assert evidence.invalid_self_reference_count == 2
    assert {item.code for item in evidence.messages} >= {
        ErrorCode.PARENT_AMBIGUOUS.value, ErrorCode.PARENT_FUTURE_VERSION.value,
        ErrorCode.LINEAGE_CYCLE.value, ErrorCode.PARENT_FORMAT.value,
        WarningCode.PARENT_UNRESOLVED.value, WarningCode.PARENT_DUPLICATE_REFERENCE.value}
    assert tuple(ref.parent_key for ref in evidence.result.references) == (
        RecordKey("v1", "missing"), RecordKey("v1", "p"))
    assert all("private malformed" not in message.message for message in result.messages)
    assert "private malformed" not in repr(result)


@pytest.mark.parametrize("parents,declared,retained", [
    ("private scalar", None, 0), ({"private": "value"}, None, 0),
    (["v1::p", 17, None], 3, 1), ([None], 1, 0),
])
def test_parent_batch_malformed_entries_do_not_erase_known_counts(parents, declared, retained):
    parent, child = row("p", []), row("child", [])
    values = dict(child.values)
    values["parent_ids"] = parents
    child = replace(child, values=MappingProxyType(values))
    result = batch((parent, child))
    evidence = result.assessments[0]
    assert evidence.child_key.record_id == "child"
    assert evidence.declared_reference_count == declared
    assert evidence.resolved_reference_count == retained
    assert (evidence.result is None) == (declared is None)
    assert any(message.code == ErrorCode.PARENT_FORMAT.value for message in evidence.messages)
    if type(parents) is list:
        parents.append("v1::new")
        assert evidence.declared_reference_count == declared


def test_parent_batch_uses_one_lookup_and_matches_existing_successful_resolver(monkeypatch):
    rows = (row("a", [], grounding="yes"), row("b", ["a", "v1::a"]), row("c", ["b", "missing"]))
    real = validation._parent_lookup
    calls = []

    def tracked(keys, order):
        calls.append(keys)
        return real(keys, order)

    monkeypatch.setattr(validation, "_parent_lookup", tracked)
    retained = batch(rows)
    assert len(calls) == 1
    for item in rows:
        previous = validation.resolve_parent_references(item.record_key, item.values["parent_ids"],
                                                        retained.record_keys)
        current = next(value for value in retained.assessments if value.child_key == item.record_key)
        assert current.result == previous


def test_parent_batch_missing_chronology_preserves_identity_resolution():
    rows = (row("root", [], grounding="yes"), row("child", ["v1::root"], version="v2"))
    retained = batch(rows)
    child = retained.assessments[1]
    assert child.resolved_reference_count == 1
    assert child.result.references[0].resolution_status is ParentResolutionStatus.RESOLVED
    assert child.result.references[0].temporal_status == "unavailable"


def test_parent_batch_missing_parent_strict_promotion_does_not_change_resolution():
    rows = (row("a", ["absent"]),)
    warning = batch(rows)
    strict = batch(rows, strict_mode=True, strict_warning_codes=(WarningCode.PARENT_UNRESOLVED.value,))
    assert warning.assessments[0].result.references == strict.assessments[0].result.references
    assert warning.messages[0].severity is ValidationSeverity.WARNING
    assert strict.messages[0].severity is ValidationSeverity.ERROR


def test_parent_batch_order_and_input_permutation_do_not_change_retained_evidence():
    rows = (row("a", []), row("b", ["a", "v1::a", "missing"]))
    changed = (replace(rows[1], values=MappingProxyType({**rows[1].values,
                                                       "parent_ids": ("missing", "v1::a", "a")})), rows[0])
    assert batch(rows) == batch(changed)


def test_parent_batch_rejects_duplicate_and_forged_identity_evidence():
    valid = row("a", [])
    with pytest.raises(CanonicalValidationError) as failure:
        validation.resolve_parent_batch((valid.record_key, valid.record_key), (valid,))
    assert failure.value.code is ErrorCode.RECORD_DUPLICATE_ID
    with pytest.raises(CanonicalValidationError) as failure:
        validation.resolve_parent_batch((valid.record_key,), (valid, valid))
    assert failure.value.code is ErrorCode.PROVENANCE_DUPLICATE_ROW
    with pytest.raises(CanonicalValidationError):
        validation.resolve_parent_batch((valid.record_key,), (replace(valid, record_key=RecordKey("v1", "forged")),))
    with pytest.raises(CanonicalValidationError) as failure:
        validation.resolve_parent_batch((RecordKey("v1", "other"),), (valid,))
    assert failure.value.code is ErrorCode.PROVENANCE_UNMATCHED_ROW


def test_parent_batch_rejects_forged_resolved_order_and_declaration_state():
    rows = (row("a", []), row("b", ["v1::a"], version="v2"))
    order = validation.resolve_version_order(("v1", "v2"), invocation_order=("v1", "v2"))
    with pytest.raises(CanonicalValidationError) as failure:
        batch(rows, version_order=replace(order, order=("v2", "v1")))
    assert failure.value.code is ErrorCode.VERSION_ORDER_CONFLICT
    forged = replace(rows[1], field_states=MappingProxyType({"parent_ids": "absent"}))
    with pytest.raises(CanonicalValidationError):
        batch((rows[0], forged), version_order=order)


def test_parent_batch_empty_scope_and_immutable_results():
    empty = validation.resolve_parent_batch((), None)
    assert empty.record_keys == empty.assessments == empty.messages == ()
    assert empty.version_order.loaded_versions == ()
    result = batch((row("a", []),))
    with pytest.raises(FrozenInstanceError):
        result.assessments[0].resolved_reference_count = 2
    with pytest.raises(TypeError):
        result.version_order.declarations["version_order"] = ("v2",)
    for value in (True, -1, None):
        with pytest.raises(ValueError):
            replace(result.assessments[0], resolved_reference_count=value)


def test_parent_batch_empty_scope_preserves_explicit_declared_version_inventory():
    declared = validation.resolve_version_order(("v1", "v2"), invocation_order=("v1", "v2"))
    order = replace(declared, loaded_versions=())
    result = validation.resolve_parent_batch((), None, version_order=order)
    assert result.version_order == order
    assert result.version_order.order == ("v1", "v2")
    with pytest.raises(CanonicalValidationError):
        validation.resolve_parent_batch((), None, version_order=replace(order, order=("v2", "v1")))


def test_parent_batch_missing_required_provenance_stays_an_error():
    row_value = validation.assess_provenance_row({"dataset_version": "v1", "record_id": "a", "parent_ids": []})
    result = validation.resolve_parent_batch((row_value.record_key,), (row_value,))
    assert result.assessments[0].provenance_available is True
    assert result.assessments[0].declared_reference_count == 0
    assert {message.field for message in result.messages} == {
        "source_type", "provenance_confidence", "external_grounding"}
    assert all(message.severity is ValidationSeverity.ERROR for message in result.messages)
