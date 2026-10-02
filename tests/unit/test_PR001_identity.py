"""Phase 2 Step 1 contract tests for PR-001 canonical record identity."""

import pytest

from recursive_integrity_toolkit.models import RecordKey


def test_PR001_composite_key_serialization() -> None:
    key = RecordKey(dataset_version="v1", record_id="row_001")
    assert str(key) == "v1::row_001"
    assert RecordKey.parse(str(key)) == key


def test_PR001_same_record_id_allowed_across_versions() -> None:
    assert RecordKey("v1", "row_001") != RecordKey("v2", "row_001")


@pytest.mark.parametrize(
    "dataset_version,record_id",
    [("", "row"), ("v1", ""), (" v1", "row"), ("v1", "row "), ("v::1", "row"), ("v1", "row::1"), ("v1\x00", "row"), ("v1", "row\x00")],
)
def test_PR001_invalid_identifier_is_rejected(dataset_version: str, record_id: str) -> None:
    with pytest.raises((TypeError, ValueError)):
        RecordKey(dataset_version, record_id)


def test_PR001_reserved_separator_parse_is_unambiguous() -> None:
    with pytest.raises(ValueError):
        RecordKey.parse("v1::row::extra")


# Phase 2 Step 4 tests use only synthetic rows. No metric or join runs.
from datetime import datetime, timedelta, timezone
from pathlib import Path

from recursive_integrity_toolkit.config import ResourceLimits
from recursive_integrity_toolkit.errors import CanonicalValidationError, ErrorCode
from recursive_integrity_toolkit.io.loaders import load_table
from recursive_integrity_toolkit.io.normalization import normalize_row, normalize_table
from recursive_integrity_toolkit.io.schema_mapping import compile_mapping, map_row
from recursive_integrity_toolkit.io.validation import validate_unique_keys, validate_canonical_values
from recursive_integrity_toolkit.models import (
    ContentMode, FileFormat, FileRole, InputSource, NormalizationOptions, RawRow, RowLocation,
)


def _record(**updates):
    return {"dataset_version": "v1", "record_id": "0001", "content": "synthetic record", **updates}


def _csv_row(tmp_path, text):
    path = tmp_path / "step4.csv"
    path.write_text(text, encoding="utf-8", newline="")
    return load_table(InputSource(FileRole.RECORDS_PRIMARY, path)).rows[0]


def test_PR001_step4_owner_metadata(owner_checker):
    for path, owner in [("io/normalization.py", "PR-001"), ("io/validation.py", "PR-001")]:
        owner_checker(path, owner)


@pytest.mark.parametrize("field", ["dataset_version", "record_id", "content"])
@pytest.mark.parametrize("missing", [True, False])
def test_PR001_required_field_missing_or_null(field, missing):
    value = _record()
    if missing:
        del value[field]
    else:
        value[field] = None
    with pytest.raises(CanonicalValidationError) as exc:
        normalize_row(value, kind="records")
    assert exc.value.code is ErrorCode.SCHEMA_REQUIRED_FIELD and exc.value.field == field


@pytest.mark.parametrize("field", ["dataset_version", "record_id"])
@pytest.mark.parametrize("value", [0, 1, True, [], {}, " leading", "trailing ", "v::id", "\x00", ""])
def test_PR001_step4_invalid_identity_fields(field, value):
    with pytest.raises(CanonicalValidationError) as exc:
        normalize_row(_record(**{field: value}), kind="records")
    assert exc.value.code is ErrorCode.SCHEMA_TYPE and exc.value.field == field


@pytest.mark.parametrize("field,limit", [("dataset_version", 256), ("record_id", 512)])
def test_PR001_identifier_length_is_codepoints(field, limit):
    normalize_row(_record(**{field: "水" * limit}), kind="records")
    with pytest.raises(CanonicalValidationError):
        normalize_row(_record(**{field: "水" * (limit + 1)}), kind="records")


def test_PR001_unicode_case_and_numeric_spelling_preserved():
    row = normalize_row(_record(dataset_version="V1", record_id="e\u0301", topic="CAT", label="cat"), kind="records")
    assert row.record_key == RecordKey("V1", "e\u0301")
    assert row.values["topic"] == "CAT" and row.values["label"] == "cat"
    assert normalize_row(_record(), kind="records").record_key.record_id == "0001"


@pytest.mark.parametrize("value", ["", " ", "\t\r\n", 123, False, [], {}])
def test_PR001_empty_or_nonstring_content_rejected(value):
    with pytest.raises(CanonicalValidationError) as exc:
        normalize_row(_record(content=value), kind="records")
    assert exc.value.code is (ErrorCode.RECORD_EMPTY_CONTENT if type(value) is str else ErrorCode.SCHEMA_TYPE)


def test_PR001_inline_content_byte_limit_and_no_normalization():
    row = _record(content="水\r\n text ")
    assert normalize_row(row, kind="records").values["content"] == "水\r\n text "
    with pytest.raises(CanonicalValidationError, match="max_content_bytes"):
        normalize_row(row, kind="records", limits=ResourceLimits(max_content_bytes=3))
    assert normalize_row(_record(content="水"), kind="records",
                         limits=ResourceLimits(max_content_bytes=3)).values["content"] == "水"


@pytest.mark.parametrize("field", ["topic", "label", "embedding_ref", "batch_id", "notes", "content_type", "language"])
@pytest.mark.parametrize("value", [1, False, [], {}])
def test_PR001_optional_string_has_no_implicit_cast(field, value):
    with pytest.raises(CanonicalValidationError) as exc:
        normalize_row(_record(**{field: value}), kind="records")
    assert exc.value.code is ErrorCode.SCHEMA_TYPE and exc.value.field == field


@pytest.mark.parametrize("value", [0, 1, 0.5, 1e100])
def test_PR001_valid_native_weight_is_finite(value):
    assert normalize_row(_record(weight=value), kind="records").values["weight"] == float(value)


@pytest.mark.parametrize("value", [-1, float("nan"), float("inf"), -float("inf"), True, "1", "1.0", "25%", [], {}])
def test_PR001_bad_native_weight_rejected(value):
    with pytest.raises(CanonicalValidationError) as exc:
        normalize_row(_record(weight=value), kind="records")
    assert exc.value.code is ErrorCode.WEIGHT_INVALID


@pytest.mark.parametrize("text,expected", [("0", 0.0), ("0.25", 0.25), ("1e2", 100.0), ("", None)])
def test_PR001_csv_weight_conversion_is_serialization_only(tmp_path, text, expected):
    row = _csv_row(tmp_path, f"dataset_version,record_id,content,weight\nv1,0001,x,{text}\n")
    assert normalize_row(row, kind="records", file_format=FileFormat.CSV).values["weight"] == expected


@pytest.mark.parametrize("text", ["NaN", "Infinity", "-1", "25%", '"1,000"', "true"])
def test_PR001_csv_bad_weight_rejected(tmp_path, text):
    row = _csv_row(tmp_path, f"dataset_version,record_id,content,weight\nv1,0001,x,{text}\n")
    with pytest.raises(CanonicalValidationError) as exc:
        normalize_row(row, kind="records", file_format=FileFormat.CSV)
    assert exc.value.code is ErrorCode.WEIGHT_INVALID


def test_PR001_datetime_is_explicit_and_utc():
    result = normalize_row(_record(timestamp="2026-01-02T03:04:05+02:00"), kind="records")
    assert result.values["timestamp"] == datetime(2026, 1, 2, 1, 4, 5, tzinfo=timezone.utc)
    native = datetime(2026, 1, 2, 3, 4, 5, tzinfo=timezone(timedelta(hours=2)))
    assert normalize_row(_record(timestamp=native), kind="records").values["timestamp"] == result.values["timestamp"]


@pytest.mark.parametrize("timestamp", ["2026-01-02", "2026-01-02T00:00:00", "not-a-date", 0, False, datetime(2026, 1, 2)])
def test_PR001_missing_timezone_or_invalid_timestamp_rejected(timestamp):
    with pytest.raises(CanonicalValidationError) as exc:
        normalize_row(_record(timestamp=timestamp), kind="records")
    assert exc.value.code is ErrorCode.SCHEMA_TYPE and exc.value.field == "timestamp"


def test_PR001_null_unknown_zero_and_absence_remain_distinct():
    result = normalize_row(_record(topic="unknown", label=None, notes="", weight=0), kind="records")
    assert result.values["topic"] == "unknown" and result.values["label"] is None
    assert result.values["notes"] == "" and result.values["weight"] == 0.0
    assert "batch_id" not in result.values
    assert result.field_states["batch_id"] == "absent"
    assert result.field_states["label"] == "null"
    assert result.field_states["notes"] == "empty_string"
    assert result.defaulted_fields == ("content_type",)
    assert result.field_states["content_type"] == "absent"


def test_PR001_csv_quoted_empty_and_null_token_remain_distinct(tmp_path):
    template = "dataset_version,record_id,content,notes\nv1,0001,x,{}\n"
    checks = [("", None, "csv_unquoted_blank"), ('""', "", "csv_quoted_empty"),
              ("null", None, "csv_null_token"), ('"null"', "null", "value"),
              ("unknown", "unknown", "value"), ("NULL", None, "csv_null_token")]
    for spelling, expected, state in checks:
        row = _csv_row(tmp_path, template.format(spelling))
        out = normalize_row(row, kind="records", file_format=FileFormat.CSV)
        assert out.values["notes"] == expected and out.field_states["notes"] == state


def test_PR001_csv_blank_content_invalid_and_embedded_quote_preserved(tmp_path):
    raw = _csv_row(tmp_path, 'dataset_version,record_id,content,notes\nv1,0001,"a,\r\n""q""",x\n')
    assert normalize_row(raw, kind="records", file_format=FileFormat.CSV).values["content"] == 'a,\r\n"q"'
    raw = _csv_row(tmp_path, "dataset_version,record_id,content\nv1,0001,\n")
    with pytest.raises(CanonicalValidationError):
        normalize_row(raw, kind="records", file_format=FileFormat.CSV)


def test_PR001_custom_null_and_blank_policy_is_explicit(tmp_path):
    opts = NormalizationOptions(null_tokens=("NA",), blank_as_null=True)
    row = _csv_row(tmp_path, "dataset_version,record_id,content,notes,topic\nv1,0001,x,NA,null\n")
    out = normalize_row(row, kind="records", file_format=FileFormat.CSV, options=opts)
    assert out.values["notes"] is None and out.values["topic"] == "null"
    assert normalize_row(_record(notes=""), kind="records", options=opts).values["notes"] is None


def test_PR001_mapped_csv_requires_original_quoting_evidence(tmp_path):
    raw = _csv_row(tmp_path, 'id,text,note\n0001,x,\n')
    plan = compile_mapping({"schema_version": "1.0", "records": {"fields": {
        "dataset_version": {"constant": "v1"}, "record_id": {"source": "id"},
        "content": {"source": "text"}, "notes": {"source": "note"}}}})
    mapped = map_row(raw, plan)
    with pytest.raises(CanonicalValidationError, match="original"):
        normalize_row(mapped, kind="records", file_format=FileFormat.CSV)
    out = normalize_row(mapped, kind="records", file_format=FileFormat.CSV, source_row=raw)
    assert out.values["notes"] is None and out.field_states["notes"] == "csv_unquoted_blank"
    assert out.location.row_number == 1 and out.location.line_number == 2


def test_PR001_explicit_mapping_and_canonical_validation_are_separate():
    original = {"id": " 0001 ", "text": "x", "origin": "unknown"}
    plan = compile_mapping({"schema_version": "1.0", "records": {"fields": {
        "dataset_version": {"constant": "v1"}, "record_id": {"source": "id", "operations": [{"op": "trim"}]},
        "content": {"source": "text"}}}})
    mapped = map_row(original, plan, preserve_extras=True)
    row = normalize_row(mapped, kind="records", options=NormalizationOptions(preserve_extras=True))
    assert row.record_key == RecordKey("v1", "0001") and row.extras["origin"] == "unknown"
    assert original["id"] == " 0001 " and "origin" not in row.values


def test_PR001_no_source_mutation_and_read_only_result():
    source = _record(custom={"items": [1, 2]})
    result = normalize_row(source, kind="records", options=NormalizationOptions(preserve_extras=True))
    source["custom"]["items"].append(3)
    assert result.extras["custom"]["items"] == (1, 2)
    with pytest.raises(TypeError):
        result.values["content"] = "changed"
    with pytest.raises(TypeError):
        result.extras["custom"]["items"] = ()
    assert normalize_row(source, kind="records").extras == {}


def test_PR001_duplicate_scope_fails_without_content_deduplication():
    a = normalize_row(_record(), kind="records")
    b = normalize_row(_record(record_id="0002"), kind="records")
    validate_unique_keys((a, b), kind="records")
    with pytest.raises(CanonicalValidationError) as exc:
        validate_unique_keys((a, a), kind="records")
    assert exc.value.code is ErrorCode.RECORD_DUPLICATE_ID
    validate_unique_keys((a, normalize_row(_record(dataset_version="v2"), kind="records")), kind="records")


def test_PR001_duplicate_across_files_requires_same_explicit_scope(tmp_path):
    tables = []
    for name in ("one.csv", "two.csv"):
        path = tmp_path / name
        path.write_text("dataset_version,record_id,content\nv1,0001,x\n")
        tables.append(normalize_table(load_table(InputSource(FileRole.RECORDS_PRIMARY, path))))
    with pytest.raises(CanonicalValidationError):
        validate_unique_keys(tables[0] + tables[1], kind="records")


def test_PR001_errors_and_repr_do_not_echo_content(tmp_path, capsys):
    secret = "PRIVATE_SENTINEL_STEP4"
    raw = _record(notes=secret, content=secret, topic=123)
    loc = RowLocation(FileRole.RECORDS_PRIMARY, str(tmp_path/"source"), 3, 7)
    with pytest.raises(CanonicalValidationError) as exc:
        normalize_row(raw, kind="records", location=loc)
    assert secret not in str(exc.value) + repr(exc.value)
    assert exc.value.field == "topic" and exc.value.row_number == 3 and exc.value.line_number == 7
    assert exc.value.file_role == "records_primary" and exc.value.severity == "error"
    result = normalize_row(_record(content=secret, notes=secret), kind="records")
    assert secret not in repr(result)
    capture = capsys.readouterr()
    assert secret not in capture.out + capture.err


def test_PR001_local_ref_is_not_opened_or_certified(tmp_path, monkeypatch):
    def forbidden(*a, **kw):
        raise AssertionError("reference was accessed")
    monkeypatch.setattr(Path, "open", forbidden)
    monkeypatch.setattr(Path, "stat", forbidden)
    result = normalize_row(_record(content="unopened.txt"), kind="records",
                          options=NormalizationOptions(content_mode=ContentMode.LOCAL_REF))
    assert result.values["content"] == "unopened.txt"
    assert not hasattr(result, "capabilities")


def test_PR001_native_strings_never_acquire_csv_null_semantics():
    out = normalize_row(_record(content="null", notes="NULL"), kind="records", file_format=FileFormat.JSONL)
    assert out.values["content"] == "null" and out.values["notes"] == "NULL"


def test_PR001_input_key_disagreement_rejected():
    with pytest.raises(CanonicalValidationError):
        normalize_row(_record(record_key="v1::other"), kind="records")


@pytest.mark.parametrize("options", [
    NormalizationOptions(content_mode="inline"), NormalizationOptions(null_tokens=["null"]),
    NormalizationOptions(null_tokens=("unknown",)), NormalizationOptions(null_tokens=("",)),
    NormalizationOptions(preserve_extras=1), NormalizationOptions(blank_as_null="true"),
])
def test_PR001_invalid_normalization_policy_rejected(options):
    with pytest.raises(CanonicalValidationError) as exc:
        normalize_row(_record(), kind="records", options=options)
    assert exc.value.code is ErrorCode.CONFIG_INVALID


def test_PR001_no_python_object_coercion():
    class Payload:
        def __str__(self):
            raise AssertionError("implicit object hook")
    with pytest.raises(CanonicalValidationError):
        normalize_row(_record(record_id=Payload()), kind="records")


def test_PR001_repository_fixture_is_read_only(repo_root):
    path = repo_root / "tests/fixtures/minimal_valid/step4_records.csv"
    before = path.read_bytes()
    normalized = normalize_table(load_table(InputSource(FileRole.RECORDS_PRIMARY, path)))
    assert tuple(row.record_key.record_id for row in normalized) == ("0001", "0002")
    assert path.read_bytes() == before


def test_PR001_mapping_constant_has_no_invented_csv_quote_state(tmp_path):
    raw = _csv_row(tmp_path, "id,text\n0001,x\n")
    plan = compile_mapping({"schema_version": "1.0", "records": {"fields": {
        "dataset_version": {"constant": "v1"}, "record_id": {"source": "id"},
        "content": {"source": "text"}, "notes": {"constant": ""}, "topic": {"constant": "null"}}}})
    result = normalize_row(map_row(raw, plan), kind="records", file_format=FileFormat.CSV, source_row=raw)
    assert result.field_states["notes"] == "empty_string"
    assert result.values["notes"] == "" and result.values["topic"] == "null"


def test_PR001_step4_executes_without_files_or_network(monkeypatch):
    import builtins
    import socket
    import urllib.request
    def blocked(*a, **kw):
        raise AssertionError("IO during row normalization")
    for target, name in [(builtins, "open"), (Path, "read_text"), (Path, "read_bytes"),
                         (Path, "open"), (socket, "create_connection"),
                         (socket, "getaddrinfo"), (urllib.request, "urlopen")]:
        monkeypatch.setattr(target, name, blocked)
    row = normalize_row(_record(timestamp="2026-01-02T00:00:00Z"), kind="records")
    validate_unique_keys((row,), kind="records")
    assert row.values["timestamp"].tzinfo is timezone.utc


def test_PR001_invalid_serialization_does_not_invoke_comparison_hook():
    class BadFormat:
        def __eq__(self, other):
            raise AssertionError("foreign comparison invoked")
    with pytest.raises(CanonicalValidationError) as exc:
        normalize_row(_record(), kind="records", file_format=BadFormat())
    assert exc.value.code is ErrorCode.CONFIG_INVALID


def test_PR001_inline_blank_csv_uses_empty_content_code(tmp_path):
    raw = _csv_row(tmp_path, "dataset_version,record_id,content\nv1,a,\n")
    with pytest.raises(CanonicalValidationError) as exc:
        normalize_row(raw, kind="records", file_format=FileFormat.CSV)
    assert exc.value.code is ErrorCode.RECORD_EMPTY_CONTENT


def test_PR001_missing_csv_spelling_does_not_guess_nulls():
    raw = RawRow(_record(notes=""), 1)
    with pytest.raises(CanonicalValidationError, match="spelling"):
        normalize_row(raw, kind="records", file_format=FileFormat.CSV)
