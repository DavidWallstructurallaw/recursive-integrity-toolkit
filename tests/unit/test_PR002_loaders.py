"""PR-002 physical ingestion checks, using synthetic local text only.

No canonical normalization, metrics, lineage, or report values are tested.
The optional real-PyArrow tests are explicitly selected with RIT_TEST_PARQUET=1;
selection without the dependency is a failure, never a skip or mocked pass.
"""

import csv
import hashlib
import os
from pathlib import Path

import pytest

from recursive_integrity_toolkit.config import ResourceLimits
from recursive_integrity_toolkit.errors import ConfigurationError, ErrorCode, IngestionError, InputError
from recursive_integrity_toolkit.io.loaders import inventory_source, load_table
from recursive_integrity_toolkit.models import FileFormat, FileRole, InputSource
from recursive_integrity_toolkit.utils.hashing import sha256_bytes


FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"


def _source(tmp_path, content, suffix=".csv", role=FileRole.RECORDS_PRIMARY, declared=None):
    path = tmp_path / ("input" + suffix)
    path.write_bytes(content if isinstance(content, bytes) else content.encode("utf-8"))
    return InputSource(role, path, declared)


def test_PR002_loader_owner(owner_checker):
    owner_checker("io/loaders.py", "PR-002")
    owner_checker("utils/hashing.py", "PR-016")


@pytest.mark.parametrize("name,fmt", [("step2_records.csv", FileFormat.CSV), ("step2_records.jsonl", FileFormat.JSONL)])
def test_PR002_minimal_local_fixture_loads(name, fmt):
    source = InputSource(FileRole.RECORDS_PRIMARY, FIXTURES / "minimal_valid" / name)
    loaded = load_table(source)
    assert loaded.inventory.file_format is fmt
    assert loaded.inventory.fields == ("record_id", "dataset_version", "content")
    assert loaded.inventory.row_count == 1
    assert loaded.rows[0].values == {"record_id": "0001", "dataset_version": "v1", "content": "local fixture"}


@pytest.mark.parametrize("role", [FileRole.RECORDS_PRIMARY, FileRole.RECORDS_COMPARE, FileRole.PROVENANCE_MANIFEST])
def test_PR002_declared_table_role_is_preserved(tmp_path, role):
    result = load_table(_source(tmp_path, "id,value\na,x\n", role=role))
    assert result.inventory.role is role
    assert result.rows[0].values == {"id": "a", "value": "x"}


def test_PR002_csv_quoted_comma_quotes_crlf_and_spelling_preserved(tmp_path):
    raw = b'id,content,notes,other\r\n0001,"a,b\r\n""quoted""","",\r\n'
    loaded = load_table(_source(tmp_path, raw))
    row = loaded.rows[0]
    assert row.values["id"] == "0001"
    assert row.values["content"] == 'a,b\r\n"quoted"'
    assert row.values["notes"] == row.values["other"] == ""
    assert row.serialized_text == '0001,"a,b\r\n""quoted""","",\r\n'
    assert row.line_number == 2
    assert loaded.inventory.size_bytes == len(raw)
    assert loaded.inventory.sha256 == hashlib.sha256(raw).hexdigest()


@pytest.mark.parametrize("suffix,content", [
    (".csv", '\ufeffid,content\r\n0001,水\r\n'),
    (".jsonl", '\ufeff{"id":"0001","content":"水"}\r\n'),
])
def test_PR002_utf8_bom_and_unicode_preserved(tmp_path, suffix, content):
    loaded = load_table(_source(tmp_path, content, suffix))
    assert loaded.rows[0].values == {"id": "0001", "content": "水"}


def test_PR002_jsonl_native_types_missing_null_and_unknown_preserved(tmp_path):
    content = '\n{"id":1,"flag":false,"value":null,"origin":"unknown","parents":["v1::a"]}\n\n{"id":2,"value":0}\n'
    result = load_table(_source(tmp_path, content, ".jsonl"))
    a, b = result.rows
    assert a.line_number == 2 and b.line_number == 4
    assert a.values["id"] == 1 and type(a.values["id"]) is int
    assert a.values["value"] is None and b.values["value"] == 0
    assert a.values["flag"] is False and "flag" not in b.values
    assert a.values["origin"] == "unknown"
    assert a.values["parents"] == ["v1::a"]
    assert result.inventory.fields == ("id", "flag", "value", "origin", "parents")


@pytest.mark.parametrize("content", ["id,id\na,b\n", "id,\na,b\n", 'id,content\na,"unterminated\n', "id,content\na,b,c\n", "id,content\na\n"])
def test_PR002_invalid_csv_rejected(tmp_path, content):
    with pytest.raises(IngestionError) as info:
        load_table(_source(tmp_path, content))
    assert info.value.code is ErrorCode.FILE_PARSE


@pytest.mark.parametrize("content", ['[]', 'null', 'true', '1', '"scalar"', '{bad}', '{"a":1,}', '{"a":1,"a":2}', '{"a":{"k":1,"k":2}}', '{"a":NaN}', '{"a":Infinity}', '{"a":-Infinity}', '{"a":1e999}', '# comment'])
def test_PR002_invalid_jsonl_rejected_with_location(tmp_path, content):
    with pytest.raises(IngestionError) as info:
        load_table(_source(tmp_path, '\n'+content+'\n', ".jsonl"))
    assert info.value.code is ErrorCode.FILE_PARSE
    assert info.value.line_number == 2
    assert info.value.row_number == 1


@pytest.mark.parametrize("suffix", [".csv", ".jsonl"])
def test_PR002_invalid_utf8_has_byte_location(tmp_path, suffix):
    with pytest.raises(IngestionError) as info:
        load_table(_source(tmp_path, b'id\n\xff', suffix))
    assert info.value.code is ErrorCode.FILE_ENCODING
    assert info.value.byte_offset == 3


@pytest.mark.parametrize("content,suffix", [("", ".csv"), ("\n \n", ".csv"), ("id,content\n", ".csv"), ("\n \n", ".jsonl")])
def test_PR002_empty_records_table_rejected(tmp_path, content, suffix):
    with pytest.raises(IngestionError) as info:
        load_table(_source(tmp_path, content, suffix))
    assert info.value.code is ErrorCode.EMPTY_DATASET


def test_PR002_header_only_provenance_preserves_zero_rows(tmp_path):
    result = load_table(_source(tmp_path, "id,origin\n", role=FileRole.PROVENANCE_MANIFEST))
    assert result.inventory.row_count == 0
    assert result.rows == ()


def test_PR002_blank_lines_ignored_and_physical_line_retained(tmp_path):
    result = load_table(_source(tmp_path, "\nid,content\n\n\na,x\n"))
    assert result.rows[0].line_number == 5


def test_PR002_large_csv_field_has_no_hidden_parser_limit(tmp_path):
    before = csv.field_size_limit()
    payload = "x" * (before + 1)
    result = load_table(_source(tmp_path, "content\n" + payload + "\n"))
    assert result.rows[0].values["content"] == payload
    assert csv.field_size_limit() == before


def test_PR002_csv_parser_setting_restored_on_error(tmp_path):
    before = csv.field_size_limit()
    with pytest.raises(IngestionError):
        load_table(_source(tmp_path, 'id\n"unterminated'))
    assert csv.field_size_limit() == before


def test_PR002_missing_file_rejected(tmp_path):
    with pytest.raises(IngestionError) as info:
        load_table(InputSource(FileRole.RECORDS_PRIMARY, tmp_path / "missing.csv"))
    assert info.value.code is ErrorCode.FILE_NOT_FOUND


def test_PR002_directory_is_not_a_table(tmp_path):
    path = tmp_path / "table.csv"
    path.mkdir()
    with pytest.raises(IngestionError) as info:
        load_table(InputSource(FileRole.RECORDS_PRIMARY, path))
    assert info.value.code is ErrorCode.FILE_PARSE


def test_PR002_unknown_extension_requires_explicit_format(tmp_path):
    source = _source(tmp_path, "id\na\n", ".data")
    with pytest.raises(InputError) as info:
        load_table(source)
    assert info.value.code is ErrorCode.FILE_FORMAT_UNSUPPORTED
    assert load_table(InputSource(source.role, source.path, FileFormat.CSV)).inventory.row_count == 1


def test_PR002_declared_format_overrides_extension_if_parser_succeeds(tmp_path):
    source = _source(tmp_path, '{"id":"a"}\n', ".csv", declared=FileFormat.JSONL)
    assert load_table(source).inventory.file_format is FileFormat.JSONL


def test_PR002_declared_format_must_parse_no_fallback(tmp_path):
    source = _source(tmp_path, 'id,content\na,x\n', declared=FileFormat.JSONL)
    with pytest.raises(IngestionError) as info:
        load_table(source)
    assert info.value.code is ErrorCode.FILE_PARSE


def test_PR002_role_format_conflict_rejected(tmp_path):
    source = _source(tmp_path, "{}", declared=FileFormat.JSON)
    with pytest.raises(IngestionError) as info:
        load_table(source)
    assert info.value.code is ErrorCode.FILE_FORMAT_UNSUPPORTED


def test_PR002_uppercase_extension_supported(tmp_path):
    assert load_table(_source(tmp_path, "id\na\n", ".CSV")).inventory.file_format is FileFormat.CSV


def test_PR002_hash_is_exact_known_sha256():
    assert sha256_bytes(b"abc") == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
    with pytest.raises(TypeError):
        sha256_bytes("abc")


def test_PR002_inventory_does_not_parse_control_file(tmp_path):
    source = _source(tmp_path, "unparsed control source", ".json", FileRole.SCHEMA_MAPPING)
    result = inventory_source(source)
    assert result.row_count is None and result.fields == ()
    assert result.sha256 == hashlib.sha256(source.path.read_bytes()).hexdigest()
    with pytest.raises(IngestionError):
        load_table(source)


@pytest.mark.parametrize("suffix,raw", [(".csv", "id\na\nb\n"), (".jsonl", '{"id":"a"}\n{"id":"b"}\n')])
def test_PR002_row_limit_exact_boundary(tmp_path, suffix, raw):
    source = _source(tmp_path, raw, suffix)
    assert load_table(source, limits=ResourceLimits(max_rows=2)).inventory.row_count == 2
    with pytest.raises(IngestionError, match="max_rows"):
        load_table(source, limits=ResourceLimits(max_rows=1))


def test_PR002_byte_limit_exact_boundary(tmp_path):
    source = _source(tmp_path, "id\na\n")
    size = source.path.stat().st_size
    assert load_table(source, limits=ResourceLimits(max_file_bytes=size)).inventory.size_bytes == size
    with pytest.raises(IngestionError, match="max_file_bytes"):
        load_table(source, limits=ResourceLimits(max_file_bytes=size-1))


@pytest.mark.parametrize("invalid", [0, -1, True, 1.5, "10"])
def test_PR002_bad_limit_is_configuration_error(tmp_path, invalid):
    source = _source(tmp_path, "id\na\n")
    with pytest.raises(ConfigurationError):
        load_table(source, limits=ResourceLimits(max_rows=invalid))


def test_PR002_json_depth_limit_checks_containers_not_brackets_in_strings(tmp_path):
    source = _source(tmp_path, '{"value":{"text":"[[["}}\n', ".jsonl")
    assert load_table(source, limits=ResourceLimits(max_json_depth=2)).inventory.row_count == 1
    with pytest.raises(IngestionError):
        load_table(source, limits=ResourceLimits(max_json_depth=1))


def test_PR002_payload_is_not_echoed_in_errors_or_repr(tmp_path, capsys):
    secret = "SENTINEL_PRIVATE_PAYLOAD"
    source = _source(tmp_path, '{"x":"' + secret + '"}\n', ".jsonl")
    result = load_table(source)
    assert secret not in repr(result) and secret not in repr(result.rows[0])
    source.path.write_text('{"x":"' + secret + '",bad}\n', encoding="utf-8")
    with pytest.raises(IngestionError) as info:
        load_table(source)
    assert secret not in str(info.value) and secret not in repr(info.value)
    captured = capsys.readouterr()
    assert secret not in captured.out + captured.err


def test_PR002_loader_preserves_unvalidated_keys_and_never_resolves_content(tmp_path):
    raw = 'id,content,origin\na,https://invalid.example/item,unknown\na,,human\n'
    source = _source(tmp_path, raw)
    before = source.path.read_bytes()
    result = load_table(source)
    assert result.rows[0].values["id"] == result.rows[1].values["id"] == "a"
    assert result.rows[1].values["content"] == ""
    assert result.rows[0].values["origin"] == "unknown"
    assert source.path.read_bytes() == before
    assert load_table(source) == result


# Explicit optional suite: no skip/xfail and no dependency installation in tests.
if os.environ.get("RIT_TEST_PARQUET") == "1":
    def test_PR002_parquet_real_roundtrip(tmp_path):
        import pyarrow as pa
        import pyarrow.parquet as pq
        path = tmp_path / "input.parquet"
        pq.write_table(pa.table({"id": ["0001", "0002"], "parents": [["v1::a"], []],
                                 "flag": [True, None]}), path)
        result = load_table(InputSource(FileRole.PROVENANCE_MANIFEST, path))
        assert result.inventory.row_count == 2
        assert result.rows[0].values == {"id": "0001", "parents": ["v1::a"], "flag": True}
        assert result.rows[1].values["flag"] is None
        assert result.rows[0].line_number is None

    def test_PR002_parquet_real_row_limit(tmp_path):
        import pyarrow as pa
        import pyarrow.parquet as pq
        path = tmp_path / "input.parquet"
        pq.write_table(pa.table({"id": ["a", "b"]}), path)
        with pytest.raises(IngestionError, match="max_rows"):
            load_table(InputSource(FileRole.RECORDS_PRIMARY, path), limits=ResourceLimits(max_rows=1))

    def test_PR002_parquet_real_invalid_file(tmp_path):
        import pyarrow
        with pytest.raises(IngestionError) as info:
            load_table(_source(tmp_path, b"not parquet", ".parquet"))
        assert info.value.code is ErrorCode.FILE_PARSE


@pytest.mark.parametrize("name", ["step2_duplicate_header.csv", "step2_duplicate_key.jsonl"])
def test_PR002_invalid_repository_fixture_is_rejected(name):
    with pytest.raises(IngestionError):
        load_table(InputSource(FileRole.RECORDS_PRIMARY, FIXTURES / "invalid_schema" / name))


@pytest.mark.parametrize("raw", ['id,content\na,b"c\n', 'id,content\na, "text"\n', 'id,content\na,"text"other\n'])
def test_PR002_noncanonical_csv_quote_placement_rejected(tmp_path, raw):
    with pytest.raises(IngestionError) as info:
        load_table(_source(tmp_path, raw))
    assert info.value.code is ErrorCode.FILE_PARSE


def test_PR002_file_inventory_does_not_load_numpy_or_execute_npy(tmp_path):
    source = _source(tmp_path, b"unexecuted bytes", ".npy", FileRole.EMBEDDING_DATA)
    assert inventory_source(source).row_count is None
    with pytest.raises(IngestionError):
        load_table(source)
