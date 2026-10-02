"""Phase 3 Step 2 literal-field representations. All data are synthetic."""
from dataclasses import FrozenInstanceError, replace
from pathlib import Path
import json
import pytest

from recursive_integrity_toolkit.config import RepresentationConfig
from recursive_integrity_toolkit.errors import CanonicalValidationError, ErrorCode, WarningCode
from recursive_integrity_toolkit.io.normalization import normalize_row
from recursive_integrity_toolkit.models import (
    CalculationReason, CalculationStatus, FileFormat, FileRole,
    NormalizationOptions, RawRow, RecordKey, RecordStateAssignment, RowLocation,
)
from recursive_integrity_toolkit.representations.field import assign_field_states, select_field_representation


def row(identifier="a", version="v1", **fields):
    return normalize_row({"dataset_version": version, "record_id": identifier,
                          "content": "synthetic input", **fields}, kind="records")


def config(selected="topic", policy="exclude", **overrides):
    return replace(RepresentationConfig(selected, selected + "_field", selected,
                                       "declared-taxonomy-v1", policy), **overrides)


def assign(rows, **options):
    kwargs = dict(dataset_versions=("v1",), scope_id="synthetic-scope", config=config())
    kwargs.update(options)
    return assign_field_states(tuple(rows), **kwargs)


def test_T1_field_assignments_are_literal_not_metrics():
    records = (row("c", topic="dog"), row("a", topic="cat"), row("b", topic="cat"))
    result = assign(records)
    assert [a.state_id for a in result.assignments] == ["cat", "cat", "dog"]
    assert result.selected_count == result.included_count == 3 and result.excluded_count == 0
    assert result.coverage.denominator_name == "selected_valid_records"
    assert result.scope.denominator_basis == "included_representation_records"
    assert result.coverage.ratio == 1.0 and result.status is CalculationStatus.AVAILABLE
    assert result.selection.descriptor.representation_version == "declared-taxonomy-v1"
    assert result.selection.descriptor.binning_or_mapping_rule == "literal_field_value"
    for name in ("frequencies", "support_size", "diversity", "tail", "sha256", "report"):
        assert not hasattr(result, name)
    assert len(records) == 3


@pytest.mark.parametrize("field", ["topic", "label"])
@pytest.mark.parametrize("policy", ["error", "exclude", "explicit_missing_state"])
def test_T1_explicit_field_precedence(field, policy):
    selected = config(field, policy)
    result = assign((row(topic="topic-value", label="label-value"),), config=selected,
                    allow_fallback=True, fallback_version="ignored-fallback-version",
                    fallback_missing_policy="error",
                    missing_state_id="MISSING" if policy == "explicit_missing_state" else None)
    assert result.assignments[0].state_id == field + "-value"
    assert result.selection.selection_basis == "explicit_configuration"
    assert not result.selection.messages
    assert result.selection.descriptor.representation_version == selected.version


@pytest.mark.parametrize("fields,expected,basis,considered", [
    ({"topic": "A", "label": "B"}, "A", "fallback_topic", ("topic",)),
    ({"label": "B"}, "B", "fallback_label", ("topic", "label")),
    ({"topic": "", "label": "B"}, "", "fallback_topic", ("topic",)),
])
def test_T1_explicit_fallback_priority(fields, expected, basis, considered):
    result = assign((row(**fields),), config=None, allow_fallback=True,
                    fallback_version="fallback-v1", fallback_missing_policy="exclude")
    assert result.assignments[0].state_id == expected
    assert result.selection.selection_basis == basis
    assert result.selection.considered_fields == considered
    assert result.selection.messages[0].code == WarningCode.REPRESENTATION_FALLBACK.value


def test_T1_fallback_never_substitutes_another_field_per_row():
    result = assign((row("a", topic=None, label="one"), row("b", topic="two", label="three")),
                    config=None, allow_fallback=True, fallback_version="v1",
                    fallback_missing_policy="exclude")
    assert [a.state_id for a in result.assignments] == [None, "two"]
    assert result.included_count == 1


def test_T1_fallback_uses_field_presence_not_null_imputation():
    result = assign((row(topic=None, label="present"),), config=None, allow_fallback=True,
                    fallback_version="v1", fallback_missing_policy="exclude")
    assert result.selection.selection_basis == "fallback_topic"
    assert result.reason_codes == (CalculationReason.ALL_EXCLUDED,)


@pytest.mark.parametrize("options", [
    {"config": None}, {"config": None, "allow_fallback": True},
    {"config": None, "allow_fallback": True, "fallback_version": "v1"},
    {"config": None, "allow_fallback": True, "fallback_missing_policy": "exclude"},
    {"allow_fallback": 1}, {"scope_id": ""}, {"scope_id": "\ud800"},
    {"fallback_version": "\x00"}, {"fallback_version": 1},
])
def test_T1_incomplete_or_nonliteral_options_fail(options):
    with pytest.raises(CanonicalValidationError):
        assign((row(topic="A"),), **options)


@pytest.mark.parametrize("source", ["config", "embedding_clusters", "content_hash", "llm", "plugin", "unknown"])
def test_T1_unimplemented_source_never_falls_back(source):
    with pytest.raises(CanonicalValidationError) as error:
        assign((row(topic="A", label="B"),), config=config(source=source), allow_fallback=True,
               fallback_version="v1", fallback_missing_policy="exclude")
    assert error.value.code is ErrorCode.CONFIG_INVALID


@pytest.mark.parametrize("changes", [
    {"name": None}, {"name": ""}, {"version": None}, {"version": ""},
    {"field": None}, {"field": "embedding_ref"}, {"field": "custom"}, {"field": "content"},
    {"missing_value_policy": None}, {"missing_value_policy": "fill"},
    {"normalization_profile": "exact_utf8_v1"}, {"version": "\ud800"},
])
def test_T1_explicit_invalid_config_blocks_without_substitution(changes):
    with pytest.raises(CanonicalValidationError):
        assign((row(topic="A", label="B"),), config=config(**changes), allow_fallback=True)


@pytest.mark.parametrize("policy", ["error", "exclude", "explicit_missing_state"])
def test_T1_absent_configured_column_is_schema_error(policy):
    with pytest.raises(CanonicalValidationError) as error:
        assign((row(label="B"),), config=config(policy=policy),
               missing_state_id="MISSING" if policy == "explicit_missing_state" else None)
    assert error.value.code is ErrorCode.SCHEMA_REQUIRED_FIELD and error.value.field == "topic"


def test_T1_no_supported_fallback_stops_without_hash_or_embedding():
    with pytest.raises(CanonicalValidationError):
        assign((row(),), config=None, allow_fallback=True, fallback_version="v1",
               fallback_missing_policy="exclude")


@pytest.mark.parametrize("policy", ["exclude", "explicit_missing_state"])
def test_T1_missing_and_null_are_distinct_from_unknown(policy):
    records = (row("absent"), row("null", topic=None), row("unknown", topic="unknown"))
    result = assign(records, config=config(policy=policy),
                    missing_state_id="MISSING" if policy == "explicit_missing_state" else None)
    assert dict(result.field_states) == {RecordKey("v1", "absent"): "absent",
        RecordKey("v1", "null"): "null", RecordKey("v1", "unknown"): "value"}
    assert result.assignments[-1].state_id == "unknown"
    assert "topic" not in records[0].values and records[1].values["topic"] is None
    assert result.selected_count == result.included_count + result.excluded_count
    if policy == "exclude":
        assert result.included_count == 1 and result.excluded_count == 2
        assert result.assignments[0].exclusion_reason is CalculationReason.REPRESENTATION_MISSING
    else:
        assert [a.state_id for a in result.assignments] == ["MISSING", "MISSING", "unknown"]
        assert result.included_count == 3


@pytest.mark.parametrize("missing", ["absent", "null"])
def test_T1_error_policy_blocks_missing_cell(missing):
    incomplete = row("b") if missing == "absent" else row("b", topic=None)
    with pytest.raises(CanonicalValidationError) as error:
        assign((row("a", topic="A"), incomplete), config=config(policy="error"))
    assert error.value.field == "topic" and error.value.record_key == "v1::b"


@pytest.mark.parametrize("value", ["", " ", "\t", "unknown", "null", "NULL", "0", "false",
                                 "cat", "Cat", "é", "e\u0301", "猫", " a ", "a\nb"])
def test_T1_literal_states_preserve_exact_spelling(value):
    result = assign((row(topic=value),))
    assert result.assignments[0].state_id == value
    assert result.included_count == 1 and dict(result.field_states)[RecordKey("v1", "a")] == "value"


def test_T1_case_and_unicode_forms_are_not_merged():
    values = ("Cat", "cat", "é", "e\u0301")
    result = assign(tuple(row(str(i), topic=v) for i, v in enumerate(values)))
    assert tuple(a.state_id for a in result.assignments) == values


def test_T1_assignment_contract_preserves_empty_string():
    assert RecordStateAssignment(RecordKey("v1", "a"), "").state_id == ""
    with pytest.raises(ValueError):
        RecordStateAssignment(RecordKey("v1", "a"), "\x00")


@pytest.mark.parametrize("policy,state_id", [
    ("explicit_missing_state", None), ("explicit_missing_state", ""),
    ("explicit_missing_state", "\ud800"), ("explicit_missing_state", "\x00"),
    ("exclude", "MISSING"), ("error", "MISSING"),
])
def test_T1_missing_id_requires_its_explicit_policy(policy, state_id):
    with pytest.raises(CanonicalValidationError):
        assign((row(topic=None),), config=config(policy=policy), missing_state_id=state_id)


@pytest.mark.parametrize("missing", [True, False])
@pytest.mark.parametrize("token", ["MISSING", "unknown", "cat", "é"])
def test_T1_missing_id_collision_always_blocks(token, missing):
    records = (row("a", topic=token),)
    if missing:
        records += (row("b", topic=None),)
    with pytest.raises(CanonicalValidationError) as error:
        assign(records, config=config(policy="explicit_missing_state"), missing_state_id=token)
    assert error.value.code is ErrorCode.CONFIG_INVALID


def test_T1_missing_id_collision_is_selected_scope_only():
    records = (row("a", topic=None), row("a", "v2", topic="MISSING"))
    result = assign(records, config=config(policy="explicit_missing_state"), missing_state_id="MISSING")
    assert result.included_count == 1 and result.scope.dataset_versions == ("v1",)


@pytest.mark.parametrize("policy", ["error", "exclude", "explicit_missing_state"])
def test_T1_empty_scope_is_unavailable_never_zero_diversity(policy):
    result = assign((), config=config(policy=policy),
                    missing_state_id="MISSING" if policy == "explicit_missing_state" else None)
    assert result.selected_count == 0 and result.coverage.ratio is None
    assert result.status is CalculationStatus.UNAVAILABLE
    assert result.reason_codes == (CalculationReason.EMPTY_SCOPE,)


def test_T1_all_excluded_scope_retains_records_and_denominator():
    records = (row("a", topic=None), row("b", topic=None))
    result = assign(records)
    assert result.reason_codes == (CalculationReason.ALL_EXCLUDED,)
    assert result.selected_count == result.excluded_count == 2 and result.included_count == 0
    assert result.coverage.denominator == 2 and result.coverage.ratio == 0
    assert len(records) == 2


def test_T1_version_scope_is_explicit_and_pooling_is_opt_in():
    records = (row("a", topic="A"), row("a", "v2", topic="B"))
    assert tuple(a.state_id for a in assign(records).assignments) == ("A",)
    pooled = assign(records, dataset_versions=("v2", "v1"))
    assert pooled.scope.dataset_versions == ("v1", "v2")
    assert tuple(a.state_id for a in pooled.assignments) == ("A", "B")
    with pytest.raises(TypeError):
        assign_field_states(records, scope_id="missing explicit scope", config=config())


@pytest.mark.parametrize("versions", [(), ("v1", "v1"), ("absent",), ("",), ("v1::x",),
    (" v1",), (True,), (1,), ("v" * 257,), ("v\x00",), ["v1"], ("v1", "absent")])
def test_T1_bad_scope_rejected(versions):
    with pytest.raises(CanonicalValidationError):
        assign((row(topic="A"),), dataset_versions=versions)


def test_T1_duplicate_composite_identity_fails():
    with pytest.raises(CanonicalValidationError) as error:
        assign((row(topic="A"), row(topic="B")))
    assert error.value.code is ErrorCode.RECORD_DUPLICATE_ID
    assert assign((row(topic="A"), row(version="v2", topic="B"))).selected_count == 1


def test_T1_result_is_detached_readonly_and_permutation_invariant():
    original = row(topic="PRIVATE_SENTINEL")
    mutable = dict(original.values)
    original = replace(original, values=mutable)
    result = assign((row("b", topic=None), original))
    assert result == assign((original, row("b", topic=None)))
    mutable["topic"] = "changed"
    assert result.assignments[0].state_id == "PRIVATE_SENTINEL"
    assert "PRIVATE_SENTINEL" not in repr(result)
    with pytest.raises(FrozenInstanceError):
        result.status = CalculationStatus.UNAVAILABLE


@pytest.mark.parametrize("bad", [0, False, [], {}, "\x00", "\ud800"])
def test_T1_invalid_state_values_fail_without_casting(bad):
    original = row(topic="A")
    with pytest.raises(CanonicalValidationError):
        assign((replace(original, values={**original.values, "topic": bad}),))


@pytest.mark.parametrize("field,bad", [("kind", "provenance"), ("record_key", RecordKey("v2", "a")),
    ("values", []), ("location", {}), ("location", RowLocation("invalid")),
    ("location", RowLocation(row_number=True))])
def test_T1_forged_canonical_rows_are_rechecked(field, bad):
    with pytest.raises(CanonicalValidationError):
        assign((replace(row(topic="A"), **{field: bad}),))


def test_T1_unsafe_objects_are_rejected_without_hooks():
    calls = []
    class Hostile:
        def __str__(self):
            calls.append("str")
            raise AssertionError("callback")
        def __bool__(self):
            calls.append("bool")
            raise AssertionError("callback")
        def __eq__(self, other):
            calls.append("eq")
            raise AssertionError("callback")
    hostile = Hostile()
    for options in ({"config": hostile}, {"scope_id": hostile}, {"dataset_versions": (hostile,)},
                    {"config": config(name=hostile)}, {"missing_state_id": hostile}, {"allow_fallback": hostile}):
        with pytest.raises(CanonicalValidationError):
            assign((row(topic="A"),), **options)
    assert not calls


def test_T1_no_io_network_execution_or_later_import(monkeypatch, tmp_path, capsys):
    import builtins
    import socket
    import sys
    records = (row(topic="https://inert.example/a"),)
    modules = set(sys.modules)
    def blocked(*args, **kwargs):
        raise AssertionError("unexpected IO or execution")
    with monkeypatch.context() as patch:
        for name in ("open", "eval", "exec"):
            patch.setattr(builtins, name, blocked)
        patch.setattr(Path, "open", blocked)
        patch.setattr(socket, "create_connection", blocked)
        patch.setattr(socket, "getaddrinfo", blocked)
        result = assign(records)
    assert result.assignments[0].state_id == "https://inert.example/a"
    assert not set(sys.modules) - modules and not list(tmp_path.iterdir())
    assert capsys.readouterr() == ("", "")


def test_T1_csv_empty_blank_and_null_remain_distinct():
    canonical = []
    for index, spelling in enumerate(('""', "", "null", '"null"')):
        value = "" if index < 2 else "null"
        values = {"dataset_version": "v1", "record_id": str(index), "content": "text", "topic": value}
        raw = RawRow(values, index + 1, index + 2, f'v1,{index},text,{spelling}\n')
        canonical.append(normalize_row(raw, kind="records", file_format=FileFormat.CSV))
    assert [a.state_id for a in assign(canonical).assignments] == ["", None, None, "null"]
    blank_as_null = normalize_row({"dataset_version": "v1", "record_id": "b", "content": "text", "topic": ""},
        kind="records", options=NormalizationOptions(blank_as_null=True))
    assert assign((blank_as_null,)).reason_codes == (CalculationReason.ALL_EXCLUDED,)


def test_T1_inherited_classifier_behavior_is_unchanged():
    from recursive_integrity_toolkit.observability.levels import classify_observability
    records = (row(topic=""),)
    before = classify_observability(records, representation=config())
    result = assign(records)
    assert before == classify_observability(records, representation=config())
    assert result.assignments[0].state_id == ""


def test_T1_selector_returns_only_declarations():
    selection = select_field_representation((row(topic="A"),), dataset_versions=("v1",), config=config())
    assert selection.descriptor.field_name == "topic" and not hasattr(selection, "assignments")


def test_T1_real_loader_fixture_is_unmodified(repo_root):
    from recursive_integrity_toolkit.io.loaders import load_table
    from recursive_integrity_toolkit.io.normalization import normalize_table
    from recursive_integrity_toolkit.models import InputSource
    path = repo_root / "tests/fixtures/minimal_valid/phase3_field_records.jsonl"
    before = path.read_bytes()
    records = normalize_table(load_table(InputSource(FileRole.RECORDS_PRIMARY, path)))
    result = assign(records)
    assert result.selected_count == 6 and result.included_count == 4 and result.excluded_count == 2
    assert [a.state_id for a in result.assignments] == ["Cat", "cat", None, None, "unknown", ""]
    assert path.read_bytes() == before


def test_T1_invalid_fixture_retains_closed_options(repo_root):
    path = repo_root / "tests/fixtures/invalid_schema/phase3_representation_cases.json"
    before = path.read_bytes()
    for case in json.loads(before)["cases"]:
        with pytest.raises(CanonicalValidationError):
            assign((row(topic="cat"),), config=config(**case))
    assert path.read_bytes() == before


def test_T1_mapping_runs_only_when_explicitly_done_first():
    from recursive_integrity_toolkit.io.schema_mapping import parse_mapping_json, map_row
    plan = parse_mapping_json(json.dumps({"schema_version": "1.0", "records": {"fields": {
        "dataset_version": {"constant": "v1"}, "record_id": {"source": "id"},
        "content": {"source": "text"}, "topic": {"source": "category", "operations": [{"op": "trim"}]},
    }}}))
    raw = RawRow({"id": "1", "text": "synthetic", "category": " Cat "}, 1)
    record = normalize_row(map_row(raw, plan, section="records"), kind="records")
    assert assign((record,)).assignments[0].state_id == "Cat"
    assert raw.values["category"] == " Cat "
