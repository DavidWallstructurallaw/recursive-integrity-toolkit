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


def phase4_step3_provenance(bundle, *, weights=None):
    from recursive_integrity_toolkit.metrics.provenance import summarize_provenance
    from recursive_integrity_toolkit.models import CalculationScope, WeightingOptions

    joined = bundle.provenance_join
    scope = CalculationScope(("v1",), joined.scope_record_keys, (),
                             joined.provenance_row_coverage.denominator_name, "provenance-v1")
    if weights is None:
        return summarize_provenance(joined, scope=scope)
    return summarize_provenance(joined, scope=scope,
                                weighting=WeightingOptions("weighted", "weight"), weights=weights)


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


def phase4_step3_provenance_rows():
    return [
        {"dataset_version": "v1", "record_id": "r0", "source_type": "human",
         "provenance_confidence": "confirmed", "external_grounding": "yes"},
        {"dataset_version": "v1", "record_id": "r1", "source_type": "synthetic",
         "provenance_confidence": "confirmed", "external_grounding": "no"},
        {"dataset_version": "v1", "record_id": "r2", "source_type": "unknown",
         "provenance_confidence": "unknown", "external_grounding": "unknown"},
        {"dataset_version": "v1", "record_id": "r3", "source_type": "sensor",
         "provenance_confidence": "estimated", "external_grounding": "yes"},
    ]


def test_phase4_step3_full_provenance_keeps_three_independent_coverage_measures(tmp_path, repo_root):
    from recursive_integrity_toolkit.reports.assembly import assemble_report

    bundle = phase4_step3_bundle(tmp_path, provenance_rows=phase4_step3_provenance_rows())
    provenance = phase4_step3_provenance(bundle)
    report = phase4_step3_schema(assemble_report(bundle, run=phase4_step3_run(), provenance=provenance), repo_root)
    facts = report["observed_facts"]["provenance"]
    assert facts["provenance_row_coverage"]["value"] == 1
    assert facts["provenance_required_field_coverage"]["value"] == 1
    assert facts["grounding_field_coverage"]["value"] == 3 / 4
    assert facts["source_type_counts"]["value"] == {"human": 1, "synthetic": 1, "mixed": 0, "sensor": 1, "unknown": 1}
    assert facts["missing_provenance_count"]["value"] == 0
    shares = report["derived_metrics"]["provenance"]["source_type_shares"]
    assert shares["value"] == {"human": 1 / 4, "synthetic": 1 / 4, "mixed": 0, "sensor": 1 / 4, "unknown": 1 / 4}
    assert shares["denominator"] == 4 and shares["evidence_class"] == "derived_metric"


def test_phase4_step3_partial_provenance_distinguishes_missing_row_unknown_and_missing_field(tmp_path, repo_root):
    from recursive_integrity_toolkit.reports.assembly import assemble_report

    rows = phase4_step3_provenance_rows()[:3]
    del rows[1]["provenance_confidence"]
    bundle = phase4_step3_bundle(tmp_path, provenance_rows=rows)
    provenance = phase4_step3_provenance(bundle)
    report = phase4_step3_schema(assemble_report(bundle, run=phase4_step3_run(), provenance=provenance), repo_root)
    facts = report["observed_facts"]["provenance"]
    assert facts["provenance_row_coverage"]["value"] == 3 / 4
    assert facts["provenance_required_field_coverage"]["value"] == 1 / 2
    assert facts["grounding_field_coverage"]["value"] == 1 / 2
    assert facts["missing_provenance_count"]["value"] == 1
    assert facts["source_type_counts"]["value"]["unknown"] == 1
    assert facts["provenance_confidence_counts"]["value"] is None
    assert facts["provenance_confidence_counts"]["status"] == "unavailable"
    assert report["derived_metrics"]["provenance"]["missing_provenance_share"]["value"] == 1 / 4
    assert report["derived_metrics"]["provenance"]["source_type_shares"]["value"]["unknown"] == 1 / 4
    assert report["run"]["run_status"] == "partial" and report["errors"]
    assert report["capabilities"]["provenance"]["execution_status"] == "partial"
    assert any(item["code"] == "E_SCHEMA_REQUIRED_FIELD" for item in report["errors"])


def test_phase4_step3_absent_provenance_never_infers_unknown_or_grounded_records(tmp_path, repo_root):
    from recursive_integrity_toolkit.reports.assembly import assemble_report

    bundle = phase4_step3_bundle(tmp_path)
    provenance = phase4_step3_provenance(bundle)
    report = phase4_step3_schema(assemble_report(bundle, run=phase4_step3_run(), provenance=provenance), repo_root)
    facts = report["observed_facts"]["provenance"]
    assert facts["missing_provenance_count"]["value"] == 4
    assert facts["provenance_row_coverage"]["value"] == 0
    assert facts["source_type_counts"]["value"]["unknown"] == 0
    assert facts["known_open_count"]["value"] == facts["known_closed_count"]["value"] == 0
    assert facts["unresolved_grounding_count"]["value"] == 4
    assert report["derived_metrics"]["provenance"]["missing_provenance_share"]["value"] == 1
    assert report["capabilities"]["provenance"]["status"] == "unavailable"


def test_phase4_step3_representation_exclusions_never_shrink_provenance_denominator(tmp_path, repo_root):
    from recursive_integrity_toolkit.reports.assembly import assemble_report

    bundle = phase4_step3_bundle(tmp_path, ("a", None, "b", None),
                                provenance_rows=phase4_step3_provenance_rows()[:3])
    distribution, provenance = phase4_step3_distribution(bundle), phase4_step3_provenance(bundle)
    report = phase4_step3_schema(assemble_report(bundle, run=phase4_step3_run(),
        distributions=(distribution,), provenance=provenance), repo_root)
    metric = report["derived_metrics"]["diversity"]["by_version"]["v1"]["gini_simpson_diversity"]
    assert metric["denominator"] == 2 and metric["value"] == 1 / 2
    assert metric["scope"]["excluded_record_count"] == 2
    assert metric["scope"]["exclusions"] == [
        {"record_key": {"dataset_version": "v1", "record_id": "r1"},
         "reason_codes": ["R_CALC_REPRESENTATION_MISSING"]},
        {"record_key": {"dataset_version": "v1", "record_id": "r3"},
         "reason_codes": ["R_CALC_REPRESENTATION_MISSING"]},
    ]
    assert report["observed_facts"]["provenance"]["provenance_row_coverage"]["denominator"] == 4
    assert report["observed_facts"]["provenance"]["provenance_row_coverage"]["value"] == 3 / 4


def test_phase4_step3_weighted_provenance_preserves_zero_weight_missing_row_separation(tmp_path, repo_root):
    from recursive_integrity_toolkit.models import RecordKey
    from recursive_integrity_toolkit.reports.assembly import assemble_report

    bundle = phase4_step3_bundle(tmp_path, provenance_rows=phase4_step3_provenance_rows()[:3])
    weights = {RecordKey("v1", "r" + str(i)): value for i, value in enumerate((1, 2, 0, 5))}
    provenance = phase4_step3_provenance(bundle, weights=weights)
    report = phase4_step3_schema(assemble_report(bundle, run=phase4_step3_run(), provenance=provenance), repo_root)
    values = report["derived_metrics"]["provenance"]
    assert values["source_type_shares"]["value"]["unknown"] == 1 / 4
    assert values["weighted_source_type_shares"]["value"]["unknown"] == 0
    assert values["weighted_source_type_shares"]["value"]["human"] == 1 / 8
    assert values["missing_provenance_share"]["value"] == 1 / 4
    assert values["weighted_missing_provenance_share"]["value"] == 5 / 8
    assert values["total_weight"]["value"] == 8 and values["missing_provenance_weight"]["value"] == 5
    for field in ("total_weight", "missing_provenance_weight", "weighted_missing_provenance_share"):
        assert values[field]["owner_ids"] == ["PR-005"]
        assert values[field]["weighting"]["weighting_mode"] == "weighted"


def test_phase4_step3_direct_closure_remains_interval_without_confidence_discount(tmp_path, repo_root):
    from recursive_integrity_toolkit.metrics.bounds import direct_closure_exposure
    from recursive_integrity_toolkit.reports.assembly import assemble_report

    bundle = phase4_step3_bundle(tmp_path, provenance_rows=phase4_step3_provenance_rows()[:3])
    provenance = phase4_step3_provenance(bundle)
    closure = direct_closure_exposure(provenance)
    report = phase4_step3_schema(assemble_report(bundle, run=phase4_step3_run(),
        provenance=provenance, closure=closure), repo_root)
    interval = report["derived_metrics"]["closure_exposure"]["direct"]
    assert interval["lower_bound"]["value"] == 1 / 4
    assert interval["upper_bound"]["value"] == 3 / 4
    assert interval["interval_width"]["value"] == 1 / 2
    assert interval["confidence_disclosure"] == "provenance_confidence_is_separate_and_does_not_discount_grounding"
    assert "midpoint" not in interval


def test_phase4_step3_forged_provenance_coverage_and_source_metadata_are_rejected(tmp_path):
    from dataclasses import replace
    import pytest
    from recursive_integrity_toolkit.models import ValidationCoverage
    from recursive_integrity_toolkit.reports.assembly import assemble_report

    bundle = phase4_step3_bundle(tmp_path, provenance_rows=phase4_step3_provenance_rows()[:3])
    result = phase4_step3_provenance(bundle)
    bad = (replace(result, provenance_row_coverage=ValidationCoverage(4, 4, "selected_valid_records")),
           replace(result, source=replace(result.source,
                   counts_metadata=replace(result.source.counts_metadata, owner_id="T4"))))
    for forged in bad:
        with pytest.raises((TypeError, ValueError)):
            assemble_report(bundle, run=phase4_step3_run(), provenance=forged)


def test_phase4_step3_source_counts_and_grounding_cannot_contradict_supplied_rows(tmp_path):
    from dataclasses import replace
    import pytest
    from recursive_integrity_toolkit.models import WeightingOptions
    from recursive_integrity_toolkit.reports.assembly import assemble_report

    bundle = phase4_step3_bundle(tmp_path, provenance_rows=phase4_step3_provenance_rows()[:3])
    result = phase4_step3_provenance(bundle)
    counts = (("human", 2), ("synthetic", 0), ("mixed", 0), ("sensor", 0), ("unknown", 1))
    forged = (replace(result, source=replace(result.source, counts=counts)),
              replace(result, direct_grounding=replace(result.direct_grounding,
                  known_open_count=replace(result.direct_grounding.known_open_count, value=3))),
              replace(result, source=replace(result.source, counts_metadata=replace(
                  result.source.counts_metadata, weighting=WeightingOptions("weighted", "weight")))))
    for value in forged:
        with pytest.raises((TypeError, ValueError)):
            assemble_report(bundle, run=phase4_step3_run(), provenance=value)


@pytest.mark.parametrize("redacted", [False, True])
def test_phase4_step9_partial_provenance_reordering_preserves_evidence_not_inventory(
        tmp_path, capsys, redacted):
    import hashlib
    import json
    from recursive_integrity_toolkit.cli import main
    from recursive_integrity_toolkit.result import validate_report

    # Four records, three joined rows, two complete declarations, two known
    # grounding values. P3-D08 keeps incomplete r1 unresolved: C=0, U=3.
    # Unknown is r2; absent is r3; neither means human/open.
    records = [{"dataset_version": "v1", "record_id": "r" + str(i),
                "content": "NEVER_REPORT_CONTENT_917", "topic": label}
               for i, label in enumerate(("A", "A", "B", "C"))]
    provenance = phase4_step3_provenance_rows()[:3]
    del provenance[1]["provenance_confidence"]
    paths = [tmp_path / "records.jsonl", tmp_path / "provenance.jsonl"]
    config = tmp_path / "config.json"
    config.write_text(json.dumps({"representation": {"name": "topic", "source": "topic_field",
        "field": "topic", "version": "taxonomy-v1", "missing_value_policy": "exclude"}}), encoding="utf-8")
    salt = tmp_path / "salt.bin"
    salt.write_bytes(b"fixed-step9-reorder-secret-32-bytes")
    reports = []
    for index in range(2):
        for path, rows in zip(paths, (records, provenance)):
            ordered = rows if index == 0 else list(reversed(rows))
            path.write_text("\n".join(json.dumps(row) for row in ordered), encoding="utf-8")
        before = {path: path.read_bytes() for path in (*paths, config, salt)}
        output = tmp_path / ("out" + str(index))
        args = ["audit", "--records", str(paths[0]), "--provenance", str(paths[1]),
                "--config", str(config), "--out", str(output)]
        if redacted:
            args += ["--redacted", "--id-salt-file", str(salt)]
        assert main(args) == 1
        streams = capsys.readouterr()
        report = json.loads((output / "report.json").read_bytes())
        validate_report(report)
        markdown = (output / "report.md").read_text(encoding="utf-8")
        assert all(path.read_bytes() == raw for path, raw in before.items())
        facts = report["observed_facts"]["provenance"]
        assert [facts[name]["value"] for name in ("provenance_row_coverage",
            "provenance_required_field_coverage", "grounding_field_coverage")] == [0.75, 0.5, 0.5]
        assert facts["missing_provenance_count"]["value"] == 1
        assert facts["source_type_counts"]["value"] == {"human": 1, "synthetic": 1,
            "mixed": 0, "sensor": 0, "unknown": 1}
        assert facts["provenance_confidence_counts"]["value"] is None
        assert facts["provenance_confidence_counts"]["status"] == "unavailable"
        direct = report["derived_metrics"]["closure_exposure"]["direct"]
        assert [direct[key]["value"] for key in ("lower_bound", "upper_bound", "interval_width")] == [0, 0.75, 0.75]
        assert [facts[key]["value"] for key in ("known_open_count", "known_closed_count",
            "unresolved_grounding_count")] == [1, 0, 3]
        assert "midpoint" not in direct
        assert "- `\"direct\"` (ratio): 0.0 to 0.75; interval width: 0.75." in markdown
        version = next(iter(report["derived_metrics"]["diversity"]["by_version"]))
        assert report["derived_metrics"]["diversity"]["by_version"][version]["gini_simpson_diversity"]["value"] == 0.625
        assert report["run"]["run_status"] == "partial"
        required_errors = [error for error in report["errors"] if error["code"] == "E_SCHEMA_REQUIRED_FIELD"]
        assert required_errors and all(error["field"] == "provenance_confidence" for error in required_errors)
        assert "E_SCHEMA_REQUIRED_FIELD" in markdown and "Unavailable (null)" in markdown
        assert [json.loads(line) for line in streams.err.splitlines()] == report["warnings"] + report["errors"]
        assert "NEVER_REPORT_CONTENT_917" not in json.dumps(report) + markdown + streams.out + streams.err
        artifacts = {entry["role"]: entry for entry in report["inputs"]["artifacts"]}
        for role, path in zip(("records_primary", "provenance_manifest"), paths):
            assert artifacts[role]["file_hash"] == hashlib.sha256(before[path]).hexdigest()
        if redacted:
            assert str(tmp_path) not in json.dumps(report) + markdown + streams.out + streams.err
        reports.append(report)
    # Row numbers describe physical input evidence. Aggregate sections and
    # identities remain equal with one fixed protection key; file hashes do not.
    for section in ("derived_metrics", "proxy_signals", "simulations", "capabilities"):
        assert reports[0][section] == reports[1][section]
    assert reports[0]["observed_facts"] == reports[1]["observed_facts"]
    artifacts = [{item["role"]: item for item in report["inputs"]["artifacts"]} for report in reports]
    for role in ("records_primary", "provenance_manifest"):
        assert artifacts[0][role]["file_hash"] != artifacts[1][role]["file_hash"]
    assert artifacts[0]["config"]["file_hash"] == artifacts[1]["config"]["file_hash"]
    def semantic_diagnostics(report):
        def without_positions(value):
            if isinstance(value, dict):
                return {key: without_positions(item) for key, item in value.items()
                        if key not in {"row_number", "line_number"}}
            if isinstance(value, list):
                return [without_positions(item) for item in value]
            return value
        return without_positions(report["warnings"] + report["errors"])
    assert semantic_diagnostics(reports[0]) == semantic_diagnostics(reports[1])
    assert reports[0]["warnings"] != reports[1]["warnings"]
