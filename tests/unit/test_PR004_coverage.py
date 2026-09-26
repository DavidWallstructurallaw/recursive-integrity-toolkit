"""PR-004 Phase 3 Step 5 tests. Earlier Phase 2 checks are preserved.

Only declared composition, inherited coverage and direct classifications are
active. No closure interval, confidence score or report is produced.
"""


# Step 4 row-field validation only. Joins and coverage remain unimplemented.
from datetime import datetime, timezone
import json
import pytest

from recursive_integrity_toolkit.config import ResourceLimits
from recursive_integrity_toolkit.errors import CanonicalValidationError, ErrorCode
from recursive_integrity_toolkit.io.normalization import normalize_row, normalize_table
from recursive_integrity_toolkit.io.loaders import load_table
from recursive_integrity_toolkit.io.validation import validate_unique_keys
from recursive_integrity_toolkit.models import (
    SourceType, ProvenanceConfidence, ExternalGrounding, Transformation,
    FileFormat, FileRole, InputSource, NormalizationOptions,
)


def _prov(**fields):
    return {"dataset_version": "v1", "record_id": "a", "source_type": "unknown",
            "provenance_confidence": "unknown", "external_grounding": "unknown", **fields}


def _csv_prov(tmp_path, extra_header="", extra_value=""):
    path = tmp_path / "prov.csv"
    path.write_text("dataset_version,record_id,source_type,provenance_confidence,external_grounding"
                    + extra_header + "\nv1,a,unknown,unknown,unknown" + extra_value + "\n")
    return load_table(InputSource(FileRole.PROVENANCE_MANIFEST, path))


def test_PR004_step4_enum_registries_are_exact():
    assert {v.value for v in SourceType} == {"human", "synthetic", "mixed", "sensor", "unknown"}
    assert {v.value for v in ProvenanceConfidence} == {"confirmed", "log_derived", "estimated", "unknown"}
    assert {v.value for v in ExternalGrounding} == {"yes", "no", "unknown"}
    assert {v.value for v in Transformation} == {"generate", "rewrite", "summarize", "translate", "filter", "label", "carryover", "other"}


@pytest.mark.parametrize("name", ["dataset_version", "record_id", "source_type", "provenance_confidence", "external_grounding"])
@pytest.mark.parametrize("mode", ["absent", "null"])
def test_PR004_required_provenance_fields(name, mode):
    row = _prov()
    if mode == "absent":
        del row[name]
    else:
        row[name] = None
    with pytest.raises(CanonicalValidationError) as exc:
        normalize_row(row, kind="provenance")
    assert exc.value.code is ErrorCode.SCHEMA_REQUIRED_FIELD and exc.value.field == name


@pytest.mark.parametrize("name,value", [
    ("source_type", "Human"), ("source_type", "person"), ("source_type", True),
    ("provenance_confidence", "Confirmed"), ("provenance_confidence", "certain"),
    ("external_grounding", "Yes"), ("external_grounding", True),
    ("transformation", "unknown"), ("transformation", "GENERATE"),
])
def test_PR004_unknown_enum_tokens_are_not_mapped(name, value):
    with pytest.raises(CanonicalValidationError) as exc:
        normalize_row(_prov(**{name: value}), kind="provenance")
    assert exc.value.code is ErrorCode.SCHEMA_ENUM and exc.value.field == name


@pytest.mark.parametrize("source", ["human", "synthetic", "mixed", "sensor", "unknown"])
@pytest.mark.parametrize("grounding", ["yes", "no", "unknown"])
@pytest.mark.parametrize("review", [True, False, None])
def test_PR004_source_grounding_review_cross_product_preserved(source, grounding, review):
    row = normalize_row(_prov(source_type=source, external_grounding=grounding, human_reviewed=review), kind="provenance")
    assert row.values["source_type"] == source
    assert row.values["external_grounding"] == grounding
    assert row.values["human_reviewed"] is review


@pytest.mark.parametrize("confidence", ["confirmed", "log_derived", "estimated", "unknown"])
def test_PR004_confidence_remains_declared_category(confidence):
    row = normalize_row(_prov(provenance_confidence=confidence), kind="provenance")
    assert row.values["provenance_confidence"] == confidence
    assert not hasattr(row, "coverage") and not hasattr(row, "grounding_class")


@pytest.mark.parametrize("field", ["generator_id", "generator_version", "batch_id", "grounding_evidence_ref", "source_uri", "license_id"])
def test_PR004_optional_identifier_empty_is_null(field):
    row = normalize_row(_prov(**{field: ""}), kind="provenance")
    assert row.values[field] is None and row.field_states[field] == "empty_string"


@pytest.mark.parametrize("field", ["generator_id", "generator_version", "batch_id", "grounding_evidence_ref", "source_uri", "license_id", "notes"])
def test_PR004_optional_strings_never_convert_numbers(field):
    with pytest.raises(CanonicalValidationError):
        normalize_row(_prov(**{field: 1}), kind="provenance")


def test_PR004_parent_absence_null_and_empty_list_are_different():
    absent = normalize_row(_prov(), kind="provenance")
    null = normalize_row(_prov(parent_ids=None), kind="provenance")
    empty = normalize_row(_prov(parent_ids=[]), kind="provenance")
    assert absent.values["parent_ids"] is None and absent.field_states["parent_ids"] == "absent"
    assert null.values["parent_ids"] is None and null.field_states["parent_ids"] == "null"
    assert empty.values["parent_ids"] == () and empty.field_states["parent_ids"] == "value"


@pytest.mark.parametrize("parents", [1, False, "[]", ["a", 2], {"a": 1}, [None], [["a"]]])
def test_PR004_native_parent_list_only_checks_types(parents):
    with pytest.raises(CanonicalValidationError) as exc:
        normalize_row(_prov(parent_ids=parents), kind="provenance")
    assert exc.value.code is ErrorCode.PARENT_FORMAT


def test_PR004_parent_order_is_stable_without_resolution_or_deduplication():
    source = ["v9::z", "bare", "v1::a", "v9::z"]
    row = normalize_row(_prov(parent_ids=source), kind="provenance")
    assert row.values["parent_ids"] == ("bare", "v1::a", "v9::z", "v9::z")
    assert source == ["v9::z", "bare", "v1::a", "v9::z"]
    assert row.values["parent_ids"].count("v9::z") == 2
    assert not hasattr(row, "ancestors") and not hasattr(row, "parent_resolution")


@pytest.mark.parametrize("spelling,expected", [("", ()), ('"[]"', ()), ('"[""v1::a""]"', ("v1::a",)), ("null", None)])
def test_PR004_csv_parent_serialization(tmp_path, spelling, expected):
    rows = normalize_table(_csv_prov(tmp_path, ",parent_ids", "," + spelling))
    assert rows[0].values["parent_ids"] == expected


@pytest.mark.parametrize("spelling", ['"{}"', '"1"', '"[1]"', '"[bad]"'])
def test_PR004_bad_csv_parent_array_rejected(tmp_path, spelling):
    with pytest.raises(CanonicalValidationError) as exc:
        normalize_table(_csv_prov(tmp_path, ",parent_ids", "," + spelling))
    assert exc.value.code is ErrorCode.PARENT_FORMAT


def test_PR004_parent_limit_is_input_bound_only():
    with pytest.raises(CanonicalValidationError):
        normalize_row(_prov(parent_ids=["a", "b"]), kind="provenance",
                      limits=ResourceLimits(max_parent_list_length=1))


@pytest.mark.parametrize("token,value", [("true", True), ("TRUE", True), ("false", False), ("False", False), ("", None)])
def test_PR004_csv_native_boolean_tokens(tmp_path, token, value):
    rows = normalize_table(_csv_prov(tmp_path, ",human_reviewed", "," + token))
    assert rows[0].values["human_reviewed"] is value


@pytest.mark.parametrize("token,value", [("yes", True), ("no", False), ("1", True), ("0", False)])
def test_PR004_csv_boolean_compatibility_requires_explicit_option(tmp_path, token, value):
    table = _csv_prov(tmp_path, ",human_reviewed", "," + token)
    with pytest.raises(CanonicalValidationError):
        normalize_table(table)
    rows = normalize_table(table, options=NormalizationOptions(csv_boolean_compatibility=True))
    assert rows[0].values["human_reviewed"] is value
    assert rows[0].values["external_grounding"] == "unknown"


@pytest.mark.parametrize("value", ["true", "false", 0, 1, "yes", [], {}])
def test_PR004_native_review_boolean_has_no_truthiness_coercion(value):
    with pytest.raises(CanonicalValidationError):
        normalize_row(_prov(human_reviewed=value), kind="provenance")


def test_PR004_duplicate_provenance_is_detected_without_a_join():
    row = normalize_row(_prov(), kind="provenance")
    with pytest.raises(CanonicalValidationError) as exc:
        validate_unique_keys((row, row), kind="provenance")
    assert exc.value.code is ErrorCode.PROVENANCE_DUPLICATE_ROW
    validate_unique_keys((row,), kind="provenance")


def test_PR004_manifest_schema_is_structural_and_closed(repo_root):
    import jsonschema
    schema = json.loads((repo_root / "schemas/normalized_manifest.schema.json").read_text())
    jsonschema.Draft202012Validator.check_schema(schema)
    validator = jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())
    payload = _prov(parent_ids=[], generation=0, human_reviewed=True)
    assert not list(validator.iter_errors(payload))
    for invalid in (_prov(parent_ids=[], generation=-1), _prov(parent_ids=[], source_type="Human"),
                    _prov(parent_ids=[], human_reviewed=1), _prov(parent_ids=[], surprise=1)):
        assert list(validator.iter_errors(invalid))
    assert schema["additionalProperties"] is False


def test_PR004_fixture_provenance_fields_only(repo_root):
    path = repo_root / "tests/fixtures/minimal_valid/step4_provenance.jsonl"
    before = path.read_bytes()
    rows = normalize_table(load_table(InputSource(FileRole.PROVENANCE_MANIFEST, path)))
    assert rows[0].values["source_type"] == "human" and rows[0].values["external_grounding"] == "no"
    assert path.read_bytes() == before


def test_PR004_header_only_provenance_validates_required_columns(tmp_path):
    path = tmp_path / "header-only.csv"
    path.write_text("dataset_version,record_id,source_type,provenance_confidence,external_grounding\n")
    table = load_table(InputSource(FileRole.PROVENANCE_MANIFEST, path))
    assert normalize_table(table) == ()


def test_PR004_header_only_provenance_cannot_bypass_schema(tmp_path):
    path = tmp_path / "missing-columns.csv"
    path.write_text("dataset_version,record_id\n")
    table = load_table(InputSource(FileRole.PROVENANCE_MANIFEST, path))
    with pytest.raises(CanonicalValidationError) as exc:
        normalize_table(table)
    assert exc.value.code is ErrorCode.SCHEMA_REQUIRED_FIELD
    assert exc.value.field == "source_type"


# Phase 3 Step 5 consumes existing validation evidence without changing it.
from dataclasses import replace
from types import MappingProxyType
from recursive_integrity_toolkit.io.validation import assess_provenance_row, join_provenance
from recursive_integrity_toolkit.metrics.provenance import summarize_provenance
from recursive_integrity_toolkit.models import CalculationScope, RecordKey, ValidationCoverage, ValidationMessage, ValidationSeverity
from recursive_integrity_toolkit.errors import WarningCode


def _p5_join(**fields):
    r=normalize_row({'dataset_version':'v1','record_id':'a','content':'synthetic'},kind='records')
    p=assess_provenance_row({'dataset_version':'v1','record_id':'a','source_type':'unknown','provenance_confidence':'confirmed','external_grounding':'unknown',**fields})
    j=join_provenance((r,),(p,));s=CalculationScope(('v1',),(r.record_key,),(),j.provenance_row_coverage.denominator_name,'coverage')
    return j,s


def test_PR004_step5_three_coverage_meanings_preserved():
    j,s=_p5_join(provenance_confidence=None,external_grounding='yes');r=summarize_provenance(j,scope=s)
    for name in ('provenance_row_coverage','provenance_required_field_coverage','grounding_field_coverage'):
        assert getattr(r,name)==getattr(j,name)
    assert (r.provenance_row_coverage.ratio,r.provenance_required_field_coverage.ratio,r.grounding_field_coverage.ratio)==(1,0,1)
    assert r.direct_grounding.known_open_count.value==0 and r.direct_grounding.unresolved_grounding_count.value==1
    assert r.validation_messages==j.messages and r.input_has_errors
    assert tuple(m.owner_id for m in r.coverage_metadata)==('PR-004',)*3
    assert tuple(m.formula_id for m in r.coverage_metadata)==('F-008',None,None)


@pytest.mark.parametrize('name',['provenance_row_coverage','provenance_required_field_coverage','grounding_field_coverage'])
@pytest.mark.parametrize('change',['numerator','denominator','denominator_name','bool'])
def test_PR004_step5_coverage_forgery_rejected(name,change):
    j,s=_p5_join();c=replace(getattr(j,name))
    value=1-c.numerator if change=='numerator' else 2 if change=='denominator' else 'represented_records' if change=='denominator_name' else bool(c.numerator)
    object.__setattr__(c,'numerator' if change=='bool' else change,value)
    with pytest.raises(CanonicalValidationError):summarize_provenance(replace(j,**{name:c}),scope=s)


@pytest.mark.parametrize('change',[{'source_type':'Human'},{'source_type':False},{'provenance_confidence':'invented'},
    {'external_grounding':True},{'generation':-1},{'human_reviewed':1},{'parent_ids':['ok',1]}])
def test_PR004_step5_invalid_fields_in_forged_assessment_fail(change):
    j,s=_p5_join();m=j.matches[0];bad=replace(m.provenance,values=MappingProxyType({**m.provenance.values,**change}))
    with pytest.raises(CanonicalValidationError):summarize_provenance(replace(j,matches=(replace(m,provenance=bad),)),scope=s)


@pytest.mark.parametrize('change',[{'required_fields_valid':False},{'required_fields_valid':1},{'grounding_known':True},{'grounding_known':0},{'missing_required_fields':('source_type',)}])
def test_PR004_step5_flags_do_not_override_evidence(change):
    j,s=_p5_join();m=j.matches[0]
    with pytest.raises(CanonicalValidationError):summarize_provenance(replace(j,matches=(replace(m,provenance=replace(m.provenance,**change)),)),scope=s)


@pytest.mark.parametrize('change',['missing_error','downgraded_error','missing_warning'])
def test_PR004_step5_failures_cannot_be_suppressed(change):
    j,s=_p5_join(provenance_confidence=None) if 'error' in change else _p5_join()
    if change=='missing_error':messages=tuple(m for m in j.messages if m.severity is not ValidationSeverity.ERROR)
    elif change=='downgraded_error':messages=tuple(replace(m,severity=ValidationSeverity.WARNING) for m in j.messages)
    else:messages=()
    with pytest.raises(CanonicalValidationError):summarize_provenance(replace(j,messages=messages),scope=s)


@pytest.mark.parametrize('change',[{'scope_record_keys':()},{'scope_record_keys':[]},{'selected_dataset_versions':('v2',)},
    {'matches':()},{'matches':[]},{'provenance_supplied':1},{'provenance_supplied':False},
    {'missing_record_keys':(RecordKey('v1','a'),)},{'promoted_warning_codes':('invented',)},{'messages':[]}])
def test_PR004_step5_join_forgery_rejected(change):
    j,s=_p5_join()
    with pytest.raises(CanonicalValidationError):summarize_provenance(replace(j,**change),scope=s)


def test_PR004_step5_duplicate_match_and_wrong_identity_fail():
    j,s=_p5_join()
    for matches in (j.matches*2,(replace(j.matches[0],record_key=RecordKey('v1','other')),)):
        with pytest.raises(CanonicalValidationError):summarize_provenance(replace(j,matches=matches),scope=s)


@pytest.mark.parametrize('change',[{'dataset_versions':('v1','v2')},{'included_record_keys':()},
    {'excluded_record_keys':(RecordKey('v1','x'),)},{'denominator_basis':'representation_records'},{'scope_id':''}])
def test_PR004_step5_scope_mismatch_fails(change):
    j,s=_p5_join()
    for name,value in change.items():object.__setattr__(s,name,value)
    with pytest.raises(CanonicalValidationError):summarize_provenance(j,scope=s)


def test_PR004_step5_selected_scope_keeps_outside_error():
    rows=tuple(normalize_row({'dataset_version':v,'record_id':'a','content':'s'},kind='records') for v in ('v1','v2'))
    prov=tuple(assess_provenance_row({'dataset_version':v,'record_id':'a','source_type':'human',
        'provenance_confidence':None if v=='v1' else 'confirmed','external_grounding':'yes'}) for v in ('v1','v2'))
    j=join_provenance(rows,prov,dataset_versions=('v2',));s=CalculationScope(('v2',),j.scope_record_keys,(),j.provenance_row_coverage.denominator_name,'selected')
    r=summarize_provenance(j,scope=s)
    assert r.provenance_required_field_coverage.ratio==1 and r.direct_grounding.known_open_count.value==1
    assert r.input_has_errors and r.validation_messages==j.messages
    assert r.validation_messages[0].record_key==RecordKey('v1','a')


def test_PR004_step5_strict_promotion_does_not_discount_grounding():
    row=normalize_row({'dataset_version':'v1','record_id':'a','content':'s'},kind='records')
    p=assess_provenance_row({'dataset_version':'v1','record_id':'a','source_type':'synthetic','provenance_confidence':'estimated','external_grounding':'yes'})
    j=join_provenance((row,),(p,),strict_mode=True,strict_warning_codes=(WarningCode.PROVENANCE_ESTIMATED.value,))
    s=CalculationScope(('v1',),j.scope_record_keys,(),j.provenance_row_coverage.denominator_name,'strict')
    r=summarize_provenance(j,scope=s)
    assert r.input_has_errors and r.direct_grounding.known_open_count.value==1
    assert r.promoted_warning_codes==j.promoted_warning_codes and r.validation_messages==j.messages


def test_PR004_step5_hostile_object_hooks_never_execute():
    class Hostile:
        def __str__(self):raise AssertionError('str')
        def __iter__(self):raise AssertionError('iter')
        def __bool__(self):raise AssertionError('bool')
        def __eq__(self,other):raise AssertionError('eq')
        def __hash__(self):raise AssertionError('hash')
    j,s=_p5_join()
    for bad in (Hostile(),{},()):
        with pytest.raises(CanonicalValidationError):summarize_provenance(bad,scope=s)
        with pytest.raises(CanonicalValidationError):summarize_provenance(j,scope=bad)
    for change in ({'selected_dataset_versions':(Hostile(),)},{'promoted_warning_codes':(Hostile(),)}):
        with pytest.raises(CanonicalValidationError):summarize_provenance(replace(j,**change),scope=s)
    key=RecordKey('v1','a');object.__setattr__(key,'dataset_version',Hostile())
    with pytest.raises(CanonicalValidationError):summarize_provenance(replace(j,scope_record_keys=(key,)),scope=s)
