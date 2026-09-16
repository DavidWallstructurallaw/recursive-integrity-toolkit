"""PR-004 Phase 2 Step 5 join/coverage validation, never a report.

The historical filename is retained. All fixtures are synthetic. Coverage here
is validation input for Step 8; no metric modules or report renderers are called.
"""

from dataclasses import replace
from datetime import datetime, timezone
from types import MappingProxyType

import pytest

from recursive_integrity_toolkit.errors import CanonicalValidationError, ErrorCode, WarningCode
from recursive_integrity_toolkit.io.validation import (
    assess_provenance_row, join_provenance, validate_canonical_values,
)
from recursive_integrity_toolkit.models import (
    CanonicalRow, FileRole, ProvenanceAssessment, RecordKey, RowLocation,
    ValidationCoverage, ValidationSeverity,
)


def _s5_record(identifier="a", version="v1", **fields):
    values = {"dataset_version": version, "record_id": identifier, "content": "synthetic", **fields}
    key = validate_canonical_values(values, kind="records")
    return CanonicalRow("records", key, MappingProxyType(values), MappingProxyType({}),
                        MappingProxyType({}), location=RowLocation(FileRole.RECORDS_PRIMARY, None, 1, 2))


def _s5_values(identifier="a", version="v1", **fields):
    return {"dataset_version": version, "record_id": identifier, "source_type": "unknown",
            "provenance_confidence": "confirmed", "external_grounding": "unknown", **fields}


def _s5_prov(identifier="a", version="v1", **fields):
    return assess_provenance_row(_s5_values(identifier, version, **fields),
                                location=RowLocation(FileRole.PROVENANCE_MANIFEST, None, 1, 2))


def _s5_scope(n):
    return tuple(_s5_record(str(i)) for i in range(n))


def test_PR004_full_row_coverage():
    result = join_provenance(_s5_scope(8), tuple(_s5_prov(str(i)) for i in range(8)))
    assert result.provenance_row_coverage.ratio == 1.0
    assert result.provenance_required_field_coverage.ratio == 1.0
    assert result.grounding_field_coverage.ratio == 0.0
    assert not result.missing_record_keys and not result.has_errors


def test_PR004_partial_row_coverage():
    result = join_provenance(_s5_scope(8), tuple(_s5_prov(str(i)) for i in range(6)))
    assert result.provenance_row_coverage.ratio == 0.75
    assert result.provenance_row_coverage.numerator == 6
    assert result.provenance_row_coverage.denominator == 8
    assert len(result.matches) == 8 and len(result.missing_record_keys) == 2
    assert [m.provenance for m in result.matches[-2:]] == [None, None]
    assert len([m for m in result.messages if m.code == WarningCode.PROVENANCE_MISSING_ROW.value]) == 2


def test_PR004_required_field_coverage_separate():
    rows = [_s5_prov(str(i), external_grounding="yes") for i in range(7)]
    values = _s5_values("7", external_grounding="yes")
    del values["provenance_confidence"]
    rows.append(assess_provenance_row(values))
    result = join_provenance(_s5_scope(8), tuple(rows))
    assert result.provenance_row_coverage.ratio == 1.0
    assert result.provenance_required_field_coverage.ratio == 0.875
    assert result.grounding_field_coverage.ratio == 1.0
    assert result.has_errors
    assert any(m.code == ErrorCode.SCHEMA_REQUIRED_FIELD.value for m in result.messages)
    assert "provenance_confidence" not in result.matches[-1].provenance.values


def test_PR004_grounding_known_excludes_unknown():
    rows = tuple(_s5_prov(str(i), external_grounding=value)
                 for i, value in enumerate(["yes"] * 4 + ["no"] * 2 + ["unknown"] * 2))
    result = join_provenance(_s5_scope(8), rows)
    assert result.provenance_row_coverage.ratio == 1.0
    assert result.grounding_field_coverage.ratio == 0.75
    assert result.provenance_required_field_coverage.ratio == 1.0


@pytest.mark.parametrize("field", ["source_type", "provenance_confidence", "external_grounding"])
@pytest.mark.parametrize("form", ["absent", "null"])
def test_PR004_missing_required_fields_are_errors_but_not_missing_rows(field, form):
    values = _s5_values()
    if form == "absent":
        del values[field]
    else:
        values[field] = None
    assessed = assess_provenance_row(values)
    result = join_provenance((_s5_record(),), (assessed,))
    assert result.provenance_row_coverage.ratio == 1.0
    assert result.provenance_required_field_coverage.ratio == 0.0
    assert result.has_errors and assessed.missing_required_fields == (field,)
    assert (field in result.matches[0].provenance.values) == (form == "null")
    assert not result.missing_record_keys


@pytest.mark.parametrize("source", ["human", "synthetic", "mixed", "sensor", "unknown"])
@pytest.mark.parametrize("grounding", ["yes", "no", "unknown"])
@pytest.mark.parametrize("review", [True, False, None])
def test_PR004_join_preserves_source_grounding_and_review(source, grounding, review):
    result = join_provenance((_s5_record(),), (_s5_prov(source_type=source,
                              external_grounding=grounding, human_reviewed=review),))
    value = result.matches[0].provenance.values
    assert value["source_type"] == source and value["external_grounding"] == grounding
    assert value["human_reviewed"] is review
    assert result.grounding_field_coverage.numerator == (0 if grounding == "unknown" else 1)


@pytest.mark.parametrize("confidence", ["confirmed", "log_derived", "estimated", "unknown"])
def test_PR004_join_confidence_preservation(confidence):
    result = join_provenance((_s5_record(),), (_s5_prov(provenance_confidence=confidence),))
    assert result.matches[0].provenance.values["provenance_confidence"] == confidence
    assert result.provenance_required_field_coverage.ratio == 1.0
    assert any(m.code == WarningCode.PROVENANCE_ESTIMATED.value for m in result.messages) == (confidence == "estimated")


@pytest.mark.parametrize("field,bad", [
    ("source_type", "person"), ("source_type", "Human"), ("source_type", True),
    ("external_grounding", "Yes"), ("external_grounding", False),
    ("provenance_confidence", "certain"), ("transformation", "unknown"),
])
def test_PR004_invalid_present_enums_fail(field, bad):
    with pytest.raises(CanonicalValidationError) as caught:
        _s5_prov(**{field: bad})
    assert caught.value.code is ErrorCode.SCHEMA_ENUM and caught.value.field == field


@pytest.mark.parametrize("field,bad", [
    ("generation", -1), ("generation", True), ("generation", "0"),
    ("human_reviewed", 1), ("human_reviewed", "true"), ("timestamp", "2026-01-01Z"),
    ("timestamp", datetime(2026, 1, 1)), ("parent_ids", "[]"), ("parent_ids", [1]),
])
def test_PR004_typed_assessment_never_normalizes_invalid_values(field, bad):
    with pytest.raises(CanonicalValidationError):
        _s5_prov(**{field: bad})


@pytest.mark.parametrize("field", ["dataset_version", "record_id"])
@pytest.mark.parametrize("bad", [None, "", " v1", "v::a", 0, False])
def test_PR004_invalid_identity_cannot_count_as_matching_row(field, bad):
    with pytest.raises(CanonicalValidationError):
        _s5_prov(**{field: bad})


def test_PR004_duplicate_provenance_row_fails():
    with pytest.raises(CanonicalValidationError) as caught:
        join_provenance((_s5_record(),), (_s5_prov(), _s5_prov(external_grounding="yes")))
    assert caught.value.code is ErrorCode.PROVENANCE_DUPLICATE_ROW


def test_PR004_duplicate_record_scope_fails():
    with pytest.raises(CanonicalValidationError) as caught:
        join_provenance((_s5_record(), _s5_record()), ())
    assert caught.value.code is ErrorCode.RECORD_DUPLICATE_ID


def test_PR004_unmatched_provenance_row_fails():
    with pytest.raises(CanonicalValidationError) as caught:
        join_provenance((_s5_record(),), (_s5_prov("missing"),))
    assert caught.value.code is ErrorCode.PROVENANCE_UNMATCHED_ROW


def test_PR004_join_uses_composite_identity_not_record_id():
    result = join_provenance((_s5_record(version="v1"), _s5_record(version="v2")),
                             (_s5_prov(version="v2"),))
    assert result.missing_record_keys == (RecordKey("v1", "a"),)
    assert result.matches[1].provenance.record_key == RecordKey("v2", "a")


def test_PR004_selected_scope_excludes_other_loaded_versions_without_false_unmatched_error():
    result = join_provenance((_s5_record(version="v1"), _s5_record(version="v2")),
                             (_s5_prov(version="v1"), _s5_prov(version="v2", external_grounding="yes")),
                             dataset_versions=("v2",))
    assert result.provenance_row_coverage.denominator == 1
    assert result.grounding_field_coverage.ratio == 1.0
    assert not result.messages
    assert result.selected_dataset_versions == ("v2",)


def test_PR004_scope_never_silently_ignores_truly_unmatched_provenance():
    with pytest.raises(CanonicalValidationError) as caught:
        join_provenance((_s5_record(version="v1"), _s5_record(version="v2")),
                         (_s5_prov(version="v3"),), dataset_versions=("v2",))
    assert caught.value.code is ErrorCode.PROVENANCE_UNMATCHED_ROW


@pytest.mark.parametrize("scope", [(), ("absent",), ("v1", "v1"), ["v1"], (True,)])
def test_PR004_invalid_selected_scope_rejected(scope):
    with pytest.raises(CanonicalValidationError):
        join_provenance((_s5_record(),), (), dataset_versions=scope)


def test_PR004_empty_record_denominator_is_error():
    with pytest.raises(CanonicalValidationError) as caught:
        join_provenance((), ())
    assert caught.value.code is ErrorCode.EMPTY_DATASET
    assert ValidationCoverage(0, 0, "empty").ratio is None


def test_PR004_absent_manifest_distinct_from_supplied_empty_manifest():
    absent = join_provenance((_s5_record(),))
    empty = join_provenance((_s5_record(),), ())
    assert not absent.provenance_supplied and empty.provenance_supplied
    assert absent.provenance_row_coverage.ratio == empty.provenance_row_coverage.ratio == 0.0
    assert absent.matches[0].provenance is None and empty.matches[0].provenance is None


def test_PR004_unknown_declaration_distinct_from_missing_row():
    result = join_provenance((_s5_record("a"), _s5_record("b")), (_s5_prov("a"),))
    assert result.matches[0].provenance.values["source_type"] == "unknown"
    assert result.matches[1].provenance is None
    assert result.provenance_row_coverage.ratio == 0.5
    assert result.provenance_required_field_coverage.ratio == 0.5
    assert result.grounding_field_coverage.ratio == 0.0


def test_PR004_all_coverage_denominators_are_same_and_named():
    result = join_provenance(_s5_scope(2), (_s5_prov("0", external_grounding="yes"),))
    for coverage in (result.provenance_row_coverage, result.provenance_required_field_coverage,
                     result.grounding_field_coverage):
        assert coverage.denominator == 2
        assert coverage.denominator_name == "all_valid_records_in_selected_dataset_scope"


def test_PR004_record_weights_do_not_change_unweighted_coverage():
    result = join_provenance((_s5_record("a", weight=0), _s5_record("b", weight=100000)), (_s5_prov("a"),))
    assert result.provenance_row_coverage.ratio == 0.5


def test_PR004_order_is_deterministic_without_chronology_inference():
    records = (_s5_record("a", "v2"), _s5_record("b", "v10"), _s5_record("a", "v10"))
    provenance = (_s5_prov("a", "v2"), _s5_prov("a", "v10"))
    left = join_provenance(records, provenance)
    assert left == join_provenance(tuple(reversed(records)), tuple(reversed(provenance)))
    assert left.scope_record_keys == (RecordKey("v10", "a"), RecordKey("v10", "b"), RecordKey("v2", "a"))
    assert not hasattr(left, "version_order")


def test_PR004_assessment_and_result_detach_and_hide_private_values(capsys):
    values = _s5_values(notes="PRIVATE_SENTINEL", parent_ids=["v1::a", "v1::a"], generation=99,
                        source_uri="https://invalid.example/private", external_grounding="yes")
    assessed = assess_provenance_row(values)
    values["notes"] = "changed"
    values["parent_ids"].clear()
    result = join_provenance((_s5_record(content="PRIVATE_RECORD_SENTINEL"),), (assessed,))
    assert result.matches[0].provenance.values["notes"] == "PRIVATE_SENTINEL"
    assert result.matches[0].provenance.values["parent_ids"] == ("v1::a", "v1::a")
    assert result.matches[0].provenance.values["generation"] == 99
    assert "PRIVATE_SENTINEL" not in repr(result) + repr(assessed)
    assert "PRIVATE_RECORD_SENTINEL" not in repr(result)
    with pytest.raises(TypeError):
        result.matches[0].provenance.values["source_type"] = "human"
    assert capsys.readouterr() == ("", "")


def test_PR004_forged_assessment_flags_are_not_trusted():
    assessed = replace(_s5_prov(), grounding_known=True, required_fields_valid=False,
                       missing_required_fields=("source_type",))
    result = join_provenance((_s5_record(),), (assessed,))
    assert result.grounding_field_coverage.ratio == 0.0
    assert result.provenance_required_field_coverage.ratio == 1.0


def test_PR004_forged_record_identity_is_error():
    record = replace(_s5_record(), record_key=RecordKey("v2", "a"))
    with pytest.raises(CanonicalValidationError):
        join_provenance((record,), ())


def test_PR004_incomplete_row_cannot_masquerade_as_canonical():
    fields = _s5_values()
    del fields["source_type"]
    row = CanonicalRow("provenance", RecordKey("v1", "a"), fields, {}, {})
    with pytest.raises(CanonicalValidationError):
        join_provenance((_s5_record(),), (row,))


def test_PR004_strict_promotion_is_explicit_and_does_not_change_coverage():
    normal = join_provenance((_s5_record(),), (_s5_prov(),))
    strict = join_provenance((_s5_record(),), (_s5_prov(),), strict_mode=True,
                             strict_warning_codes=(WarningCode.GROUNDING_UNKNOWN.value,))
    assert not normal.has_errors and strict.has_errors
    assert strict.provenance_row_coverage == normal.provenance_row_coverage
    assert strict.promoted_warning_codes == (WarningCode.GROUNDING_UNKNOWN.value,)
    assert strict.messages[0].severity is ValidationSeverity.ERROR
    assert strict.messages[0].code == WarningCode.GROUNDING_UNKNOWN.value


@pytest.mark.parametrize("codes", [("invented",), (True,), [WarningCode.GROUNDING_UNKNOWN.value],
                                    (WarningCode.GROUNDING_UNKNOWN.value,) * 2])
def test_PR004_invalid_warning_promotion_rejected(codes):
    with pytest.raises(CanonicalValidationError):
        join_provenance((_s5_record(),), (), strict_mode=True, strict_warning_codes=codes)


def test_PR004_join_error_location_without_payload_echo():
    p = _s5_prov("other", notes="PRIVATE_SENTINEL")
    with pytest.raises(CanonicalValidationError) as caught:
        join_provenance((_s5_record(),), (p,))
    error = caught.value
    assert error.file_role == FileRole.PROVENANCE_MANIFEST.value
    assert error.row_number == 1 and error.line_number == 2 and error.record_key == "v1::other"
    assert "PRIVATE_SENTINEL" not in str(error)


def test_PR004_shared_metadata_is_not_overwritten():
    earlier = datetime(2020, 1, 1, tzinfo=timezone.utc)
    later = datetime(2020, 1, 2, tzinfo=timezone.utc)
    result = join_provenance((_s5_record(batch_id="record-batch", timestamp=earlier),),
                             (_s5_prov(batch_id="provenance-batch", timestamp=later),))
    match = result.matches[0]
    assert match.conflicting_fields == ("batch_id", "timestamp")
    assert match.record_metadata == {"batch_id": "record-batch", "timestamp": earlier}
    assert match.provenance.values["batch_id"] == "provenance-batch"
    assert match.provenance.values["timestamp"] == later


def test_PR004_join_has_no_file_network_or_analysis_side_effects(monkeypatch, tmp_path):
    import builtins
    import socket
    from pathlib import Path
    calls = []
    def blocked(*args, **kwargs):
        calls.append(True)
        raise AssertionError("unexpected IO")
    records, rows = (_s5_record(content="https://invalid.example/record"),), (_s5_prov(),)
    with monkeypatch.context() as patch:
        patch.setattr(builtins, "open", blocked)
        patch.setattr(Path, "open", blocked)
        patch.setattr(socket, "create_connection", blocked)
        patch.setattr(socket, "getaddrinfo", blocked)
        result = join_provenance(records, rows)
    assert not calls and list(tmp_path.iterdir()) == []
    for name in ("source_type_shares", "closure_bounds", "ancestors", "derived_metrics", "maximum_level"):
        assert not hasattr(result, name)



def test_PR004_required_field_errors_are_not_hidden_outside_selected_scope():
    incomplete = _s5_values(version="v1")
    del incomplete["source_type"]
    result = join_provenance((_s5_record(version="v1"), _s5_record(version="v2")),
                             (assess_provenance_row(incomplete), _s5_prov(version="v2")),
                             dataset_versions=("v2",))
    assert result.provenance_required_field_coverage.ratio == 1.0
    assert result.has_errors
    assert any(m.record_key == RecordKey("v1", "a") and m.severity is ValidationSeverity.ERROR
               for m in result.messages)

def test_PR004_pipeline_with_existing_loader_and_normalizer(repo_root):
    from recursive_integrity_toolkit.io.loaders import load_table
    from recursive_integrity_toolkit.io.normalization import normalize_table
    from recursive_integrity_toolkit.models import InputSource
    folder = repo_root / "tests/fixtures/provenance_partial"
    paths = (folder / "step5_records.jsonl", folder / "step5_provenance.jsonl")
    before = tuple(path.read_bytes() for path in paths)
    records = normalize_table(load_table(InputSource(FileRole.RECORDS_PRIMARY, paths[0])))
    rows = normalize_table(load_table(InputSource(FileRole.PROVENANCE_MANIFEST, paths[1])))
    result = join_provenance(records, rows)
    assert result.provenance_row_coverage.ratio == 0.75
    assert result.provenance_required_field_coverage.ratio == 0.75
    assert result.grounding_field_coverage.ratio == 0.5
    assert not result.has_errors and len(result.matches) == 4
    assert tuple(path.read_bytes() for path in paths) == before


def test_PR004_pipeline_incomplete_assessment_preserves_failure_evidence(repo_root):
    import json
    from recursive_integrity_toolkit.io.normalization import normalize_row
    from recursive_integrity_toolkit.io.validation import assess_provenance_row
    path = repo_root / "tests/fixtures/invalid_schema/step5_missing_confidence.json"
    before = path.read_bytes()
    # This typed JSON fixture deliberately bypasses strict row certification.
    # Its incomplete assessment remains a validation error, never a CanonicalRow.
    incomplete = assess_provenance_row(json.loads(before))
    record = normalize_row({"dataset_version": "v1", "record_id": "a", "content": "synthetic"}, kind="records")
    result = join_provenance((record,), (incomplete,))
    assert result.has_errors
    assert result.provenance_row_coverage.ratio == 1.0
    assert result.provenance_required_field_coverage.ratio == 0.0
    assert result.grounding_field_coverage.ratio == 1.0
    assert path.read_bytes() == before
