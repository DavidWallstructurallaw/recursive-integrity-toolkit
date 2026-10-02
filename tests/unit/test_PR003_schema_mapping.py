"""PR-003 declarative mapping and security tests on synthetic local inputs.

Independent oracles are explicit expected values, exact error codes, and denied
side-effect probes. No metric, provenance join, or canonical identity is tested.
"""

from dataclasses import FrozenInstanceError, replace
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys

import pytest
from jsonschema import Draft202012Validator

from recursive_integrity_toolkit.config import ResourceLimits
from recursive_integrity_toolkit.errors import ErrorCode, InputError, MappingError
from recursive_integrity_toolkit.io.loaders import load_table
from recursive_integrity_toolkit.io.schema_mapping import (
    compile_mapping, load_mapping, map_row, parse_mapping_json,
)
from recursive_integrity_toolkit.models import FileRole, InputSource, RawRow


FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"
APPROVED_OPERATIONS = {
    "rename", "trim", "cast_string", "cast_integer", "cast_float", "cast_boolean",
    "parse_datetime", "parse_json_list", "constant", "coalesce", "map_values",
    "normalize_whitespace", "lowercase", "uppercase",
}


def _document(spec=None, *, fields=None):
    if fields is None:
        fields = {"result": {"source": "x"} if spec is None else spec}
    return {"schema_version": "1.0", "records": {"fields": fields}}


def _map(value, *operations):
    plan = compile_mapping(_document({"source": "x", "operations": list(operations)}))
    return map_row({"x": value}, plan)


def test_PR003_schema_operation_inventory(schema_root):
    schema = json.loads((schema_root / "schema_mapping.schema.json").read_text())
    Draft202012Validator.check_schema(schema)
    assert {name.removeprefix("op_") for name in schema["$defs"] if name.startswith("op_")} == APPROVED_OPERATIONS


@pytest.mark.parametrize("operation,value,expected", [
    ({"op": "rename"}, "0001", "0001"),
    ({"op": "trim"}, "\u2003 0001\n", "0001"),
    ({"op": "lowercase"}, "CAT", "cat"),
    ({"op": "uppercase"}, "cat", "CAT"),
    ({"op": "cast_string"}, 12, "12"),
    ({"op": "cast_string"}, 1.25, "1.25"),
    ({"op": "cast_string"}, False, "false"),
    ({"op": "cast_string"}, "0001", "0001"),
    ({"op": "cast_integer"}, 2, 2),
    ({"op": "cast_integer"}, "-002", -2),
    ({"op": "cast_integer"}, "+002", 2),
    ({"op": "cast_float"}, "1e2", 100.0),
    ({"op": "cast_float"}, ".5", 0.5),
    ({"op": "cast_float"}, 2, 2.0),
    ({"op": "cast_boolean", "mapping": {"Y": True, "N": False}}, "N", False),
    ({"op": "parse_json_list"}, '["v1::a",null,0,false,{"x":1}]', ["v1::a", None, 0, False, {"x": 1}]),
    ({"op": "constant", "value": {"explicit": [1, None]}}, "ignored", {"explicit": [1, None]}),
    ({"op": "normalize_whitespace", "format": "collapse"}, " \tcat\n\ndog\u2003", " cat dog "),
])
def test_PR003_explicit_operations_match_expected_values(operation, value, expected):
    result = _map(value, operation)
    assert result.values["result"] == expected
    assert type(result.values["result"]) is type(expected)
    assert result.field_traces[0].operations == (operation["op"],)


def test_PR003_rename_target_is_literal_field_key():
    plan = compile_mapping(_document(fields={"record_id": {"source": "identifier", "operations": [{"op": "rename"}]}}))
    result = map_row({"identifier": "a::b", "other": 1}, plan)
    assert result.values == {"record_id": "a::b"}  # canonical validity is Step 4
    assert result.source_fields == ("identifier", "other")
    assert result.unmapped_fields == ("other",)


@pytest.mark.parametrize("value", [1.5, 1.0, True, "1.2", "1e2", " 1", "1 ", "1_000", "unknown", ""])
def test_PR003_integer_cast_rejects_nonexact_input(value):
    with pytest.raises(MappingError) as info:
        _map(value, {"op": "cast_integer"})
    assert info.value.code is ErrorCode.SCHEMA_TYPE


@pytest.mark.parametrize("value", [True, "NaN", "Infinity", "-Infinity", "1e999", "1_000", " 1", [], {}])
def test_PR003_float_cast_rejects_invalid_or_nonfinite_input(value):
    with pytest.raises(MappingError) as info:
        _map(value, {"op": "cast_float"})
    assert info.value.code is ErrorCode.SCHEMA_TYPE


@pytest.mark.parametrize("value", [[], {}, ["text"]])
def test_PR003_string_cast_rejects_nested_values(value):
    with pytest.raises(MappingError):
        _map(value, {"op": "cast_string"})


@pytest.mark.parametrize("value", [True, 0, 1, "yes", "y", " Y "])
def test_PR003_boolean_has_no_implicit_truthiness_or_case_coercion(value):
    with pytest.raises(MappingError):
        _map(value, {"op": "cast_boolean", "mapping": {"Y": True, "N": False}})


@pytest.mark.parametrize("operation", [
    {"op": "cast_boolean"}, {"op": "cast_boolean", "mapping": {"Y": "true"}},
    {"op": "cast_boolean", "mapping": {}}, {"op": "parse_datetime"},
    {"op": "normalize_whitespace"}, {"op": "normalize_whitespace", "format": "regex"},
    {"op": "coalesce", "sources": []}, {"op": "coalesce", "sources": [4]},
    {"op": "map_values", "mapping": {}}, {"op": "map_values", "mapping": {}, "unmapped": "guess"},
    {"op": "trim", "regex": ".*"},
])
def test_PR003_missing_or_unsupported_parameters_are_rejected(operation):
    with pytest.raises(MappingError):
        compile_mapping(_document({"source": "x", "operations": [operation]}))


@pytest.mark.parametrize("fmt,value,expected", [
    ("%Y-%m-%d", "2026-09-16", datetime(2026, 9, 16)),
    ("%d/%m/%Y %H:%M:%S", "16/09/2026 10:11:12", datetime(2026, 9, 16, 10, 11, 12)),
    ("iso8601", "2026-09-16T10:11:12+00:00", datetime(2026, 9, 16, 10, 11, 12, tzinfo=timezone.utc)),
])
def test_PR003_datetime_uses_explicit_format_and_preserves_timezone(fmt, value, expected):
    assert _map(value, {"op": "parse_datetime", "format": fmt}).values["result"] == expected


@pytest.mark.parametrize("fmt", ["%B %d %Y", "%x", "%Z", "%c", "%-d", "%"])
def test_PR003_datetime_rejects_locale_or_platform_dependent_directives(fmt):
    with pytest.raises(MappingError):
        compile_mapping(_document({"source": "x", "operations": [{"op": "parse_datetime", "format": fmt}]}))


def test_PR003_invalid_datetime_does_not_leak_parser_payload():
    with pytest.raises(MappingError) as info:
        _map("PRIVATE_INVALID_DATE", {"op": "parse_datetime", "format": "%Y-%m-%d"})
    assert "PRIVATE_INVALID_DATE" not in str(info.value)
    assert info.value.__suppress_context__


@pytest.mark.parametrize("value", ['{}', 'null', '1', '"array"', '[NaN]', '[1e999]', '[{"a":1,"a":2}]', '[1,]'])
def test_PR003_json_list_is_a_strict_array(value):
    with pytest.raises(MappingError):
        _map(value, {"op": "parse_json_list"})


def test_PR003_ordered_operations_do_not_commute():
    upper_then_map = [{"op": "uppercase"}, {"op": "map_values", "mapping": {"CAT": "feline"}, "unmapped": "keep"}]
    assert _map("cat", *upper_then_map).values["result"] == "feline"
    assert _map("cat", *reversed(upper_then_map)).values["result"] == "CAT"


@pytest.mark.parametrize("value", ["", 0, False, [], {}, "unknown"])
def test_PR003_coalesce_preserves_nonmissing_values(value):
    plan = compile_mapping(_document({"operations": [{"op": "coalesce", "sources": ["absent", "a", "b"]}]}))
    result = map_row({"a": value, "b": "fallback"}, plan)
    assert result.values["result"] == value
    assert type(result.values["result"]) is type(value)


def test_PR003_coalesce_distinguishes_missing_null_and_value():
    plan = compile_mapping(_document({"operations": [{"op": "coalesce", "sources": ["a", "b"]}]}))
    assert map_row({}, plan).values == {}
    assert map_row({"a": None}, plan).values == {"result": None}
    assert map_row({"a": None, "b": "kept"}, plan).values == {"result": "kept"}


def test_PR003_required_source_is_not_silently_optional():
    with pytest.raises(MappingError) as info:
        map_row({}, compile_mapping(_document()))
    assert info.value.code is ErrorCode.MAPPING_SOURCE_FIELD_MISSING


def test_PR003_constant_field_and_operation_are_explicit():
    plan = compile_mapping(_document(fields={"one": {"constant": None}, "two": {"operations": [{"op": "constant", "value": "v1"}]}}))
    assert map_row({}, plan).values == {"one": None, "two": "v1"}


@pytest.mark.parametrize("op", ["trim", "cast_string", "cast_integer", "cast_float", "parse_json_list", "lowercase", "uppercase"])
def test_PR003_null_is_not_promoted_by_transform(op):
    assert _map(None, {"op": op}).values["result"] is None


@pytest.mark.parametrize("policy,expected", [("keep", "unknown"), ("null", None)])
def test_PR003_unmapped_value_uses_explicit_policy_and_notice(policy, expected):
    result = _map("unknown", {"op": "map_values", "mapping": {"person": "human"}, "unmapped": policy})
    assert result.values["result"] == expected
    assert result.notices[0].code == "W_MAPPING_VALUE_UNMAPPED"
    assert result.notices[0].policy == policy


def test_PR003_unmapped_error_is_not_inferred():
    with pytest.raises(MappingError) as info:
        _map("unknown", {"op": "map_values", "mapping": {}, "unmapped": "error"})
    assert info.value.code is ErrorCode.SCHEMA_ENUM


@pytest.mark.parametrize("value", [1, True, [1], {"x": 1}])
def test_PR003_token_lookup_does_not_coerce_types(value):
    assert _map(value, {"op": "map_values", "mapping": {"1": "changed", "true": "changed"}, "unmapped": "keep"}).values["result"] == value


def test_PR003_fields_read_original_row_not_prior_targets():
    plan = compile_mapping(_document(fields={"a": {"source": "b"}, "b": {"source": "a"}}))
    row = {"a": "first", "b": "second"}
    assert map_row(row, plan).values == {"a": "second", "b": "first"}
    assert row == {"a": "first", "b": "second"}


def test_PR003_target_collision_is_rejected_before_conversion():
    with pytest.raises(MappingError) as info:
        compile_mapping(_document({"source": "x", "constant": 5}))
    assert info.value.code is ErrorCode.MAPPING_TARGET_COLLISION


def test_PR003_duplicate_json_target_is_rejected():
    with pytest.raises(MappingError) as info:
        load_mapping(FIXTURES / "schema_mapping/step3_duplicate_target.json")
    assert info.value.code is ErrorCode.MAPPING_TARGET_COLLISION


def test_PR003_static_schema_and_runtime_accept_spec_fixture(schema_root):
    text = (FIXTURES / "schema_mapping/step3_mapping.json").read_text()
    schema = json.loads((schema_root / "schema_mapping.schema.json").read_text())
    Draft202012Validator(schema).validate(json.loads(text))
    plan = parse_mapping_json(text)
    assert plan.sections == ("records",)


def test_PR003_legacy_version_spelling_is_explicit_and_exclusive(schema_root):
    doc = _document()
    doc["mapping_version"] = doc.pop("schema_version")
    schema = json.loads((schema_root / "schema_mapping.schema.json").read_text())
    Draft202012Validator(schema).validate(doc)
    assert compile_mapping(doc).schema_version == "1.0"
    doc["schema_version"] = "1.0"
    assert not Draft202012Validator(schema).is_valid(doc)
    with pytest.raises(MappingError):
        compile_mapping(doc)


@pytest.mark.parametrize("document", [
    {}, {"schema_version": "2.0", "records": {"fields": {}}},
    {"schema_version": "1.0"}, {"schema_version": "1.0", "records": []},
    {"schema_version": "1.0", "records": {"fields": []}},
    {"schema_version": "1.0", "records": {"fields": {"": {"source": "x"}}}},
])
def test_PR003_invalid_document_is_rejected(document, schema_root):
    schema = json.loads((schema_root / "schema_mapping.schema.json").read_text())
    assert not Draft202012Validator(schema).is_valid(document)
    with pytest.raises(MappingError):
        compile_mapping(document)


def test_PR003_plan_is_immutable_snapshot_and_output_is_independent():
    doc = _document({"constant": {"a": [1]}})
    plan = compile_mapping(doc)
    doc["records"]["fields"]["result"]["constant"]["a"].append(2)
    a = map_row({}, plan)
    a.values["result"]["a"].append(3)
    assert map_row({}, plan).values == {"result": {"a": [1]}}
    with pytest.raises(FrozenInstanceError):
        plan.sha256 = "changed"
    with pytest.raises(MappingError):
        map_row({}, replace(plan, sha256="changed"))


def test_PR003_extras_are_separate_explicit_and_copied():
    row = {"x": [1], "extra": {"nested": [2]}}
    plan = compile_mapping(_document())
    assert map_row(row, plan).extras == {}
    result = map_row(row, plan, preserve_extras=True)
    result.values["result"].append(3)
    result.extras["extra"]["nested"].append(4)
    assert row == {"x": [1], "extra": {"nested": [2]}}
    assert result.unmapped_fields == ("extra",)


def test_PR003_source_type_does_not_infer_grounding_or_review():
    plan = compile_mapping(_document(fields={"source_type": {"source": "origin", "operations": [{"op": "map_values", "mapping": {"person": "human"}, "unmapped": "keep"}]}}))
    assert map_row({"origin": "person"}, plan).values == {"source_type": "human"}


def test_PR003_provenance_section_maps_only_declared_fields():
    doc = {"schema_version": "1.0", "provenance": {"fields": {"source_type": {"source": "origin"}}}}
    plan = compile_mapping(doc)
    assert map_row({"origin": "unknown"}, plan, section="provenance").values == {"source_type": "unknown"}
    with pytest.raises(MappingError):
        map_row({"origin": "unknown"}, plan)


def test_PR003_mapping_file_snapshot_and_synthetic_loader_integration():
    mapping_path = FIXTURES / "schema_mapping/step3_mapping.json"
    rows_path = FIXTURES / "schema_mapping/step3_rows.jsonl"
    before = mapping_path.read_bytes(), rows_path.read_bytes()
    plan = load_mapping(mapping_path)
    loaded = load_table(InputSource(FileRole.RECORDS_PRIMARY, rows_path))
    result = map_row(loaded.rows[0], plan)
    assert result.values == {"record_id": "0001", "dataset_version": "v1", "content": "synthetic test text", "topic": "cat"}
    assert result.row_number == 1 and result.line_number == 1
    assert result.field_traces[0].operations == ("trim",)
    assert result.mapping_sha256 == plan.sha256
    assert plan.inventory is not None
    assert plan.inventory.row_count is None
    assert (mapping_path.read_bytes(), rows_path.read_bytes()) == before
    assert map_row(loaded.rows[0], plan) == result


def test_PR003_csv_spelling_and_empty_values_are_not_normalized(tmp_path):
    path = tmp_path / "input.csv"
    path.write_bytes(b'x,other\r\n"",NULL\r\n')
    raw = load_table(InputSource(FileRole.RECORDS_PRIMARY, path)).rows[0]
    result = map_row(raw, compile_mapping(_document()), preserve_extras=True)
    assert result.values == {"result": ""} and result.extras == {"other": "NULL"}
    assert raw.serialized_text == '"",NULL\r\n'


@pytest.mark.parametrize("text", ['{bad}', '{"x": NaN}', '{"x": 1e999}', '[]'])
def test_PR003_invalid_mapping_json_is_sanitized(text):
    with pytest.raises(MappingError):
        parse_mapping_json(text)


def test_PR003_resource_limits_are_enforced(tmp_path):
    path = tmp_path / "mapping.json"
    path.write_text(json.dumps(_document()))
    with pytest.raises(InputError):
        load_mapping(path, limits=ResourceLimits(max_file_bytes=1))
    with pytest.raises(MappingError):
        parse_mapping_json(path.read_text(), limits=ResourceLimits(max_json_depth=1))
    plan = compile_mapping(_document({"source": "x", "operations": [{"op": "parse_json_list"}]}), limits=ResourceLimits(max_json_depth=8))
    with pytest.raises(MappingError):
        map_row({"x": "[" * 9 + "0" + "]" * 9}, plan)


@pytest.mark.parametrize("operation", ["eval", "exec", "shell", "subprocess", "network", "dynamic_import", "environment", "callback", "template", "regex", "write_file"])
def test_PR003_unsafe_operation_rejected_before_use(operation, schema_root):
    doc = _document({"source": "x", "operations": [{"op": operation}]})
    schema = json.loads((schema_root / "schema_mapping.schema.json").read_text())
    assert not Draft202012Validator(schema).is_valid(doc)
    with pytest.raises(MappingError) as info:
        compile_mapping(doc)
    assert info.value.code is ErrorCode.MAPPING_UNSAFE_TRANSFORM


def test_PR003_security_fixture_rejects_executable_mapping():
    with pytest.raises(MappingError) as info:
        load_mapping(FIXTURES / "security/step3_unsafe_mapping.json")
    assert info.value.code is ErrorCode.MAPPING_UNSAFE_TRANSFORM


def test_PR003_foreign_object_hooks_are_not_called():
    calls = []
    class Hostile:
        def __str__(self):
            calls.append("str")
            return "pretend"
        def __deepcopy__(self, memo):
            calls.append("copy")
            return self
    with pytest.raises(MappingError):
        _map(Hostile(), {"op": "cast_string"})
    with pytest.raises(MappingError):
        compile_mapping(_document({"constant": Hostile()}))
    assert calls == []


def test_PR003_cyclic_plain_data_fails_without_recursion_trace_leak():
    cycle = []
    cycle.append(cycle)
    with pytest.raises(MappingError):
        compile_mapping(_document({"constant": cycle}))
    with pytest.raises(MappingError):
        map_row({"x": cycle}, compile_mapping(_document()))


@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf")])
def test_PR003_nonfinite_declarations_and_values_are_rejected(value):
    with pytest.raises(MappingError):
        compile_mapping(_document({"constant": value}))
    with pytest.raises(MappingError):
        _map(value, {"op": "cast_string"})


def test_PR003_payload_stays_out_of_errors_traces_and_repr(capsys):
    secret = "PRIVATE_MAPPING_SENTINEL"
    plan = compile_mapping(_document({"source": "x", "operations": [{"op": "cast_integer"}]}))
    row = RawRow({"x": secret}, 5, 9)
    with pytest.raises(MappingError) as info:
        map_row(row, plan)
    assert (info.value.row_number, info.value.line_number, info.value.operation_index) == (5, 9, 0)
    assert info.value.target == "result"
    assert secret not in str(info.value) + repr(info.value)
    plan = compile_mapping(_document({"constant": secret}))
    result = map_row({}, plan)
    assert secret not in repr(plan) + repr(result) + repr(result.field_traces)
    captured = capsys.readouterr()
    assert captured.out == captured.err == ""


def test_PR003_literal_code_templates_paths_and_env_are_inert():
    literal = "__import__('os').system('bad'); {{secret}}; $HOME; https://invalid.example/"
    assert _map(literal, {"op": "rename"}).values == {"result": literal}


def test_PR003_map_and_compile_have_no_side_effects(monkeypatch):
    import builtins
    import os
    import socket
    import urllib.request
    calls = []
    def denied(*args, **kwargs):
        calls.append("denied")
        raise AssertionError("mapping attempted a side effect")
    with monkeypatch.context() as m:
        for obj, names in [(builtins, ("open", "eval", "exec", "compile")),
                           (os, ("open", "system")), (Path, ("open", "read_text", "read_bytes", "write_text", "write_bytes")),
                           (socket, ("create_connection", "getaddrinfo")),
                           (socket.socket, ("connect", "connect_ex")),
                           (urllib.request, ("urlopen",)), (subprocess, ("Popen",))]:
            for name in names:
                m.setattr(obj, name, denied)
        result = _map(" x ", {"op": "trim"}, {"op": "uppercase"})
    assert result.values == {"result": "X"} and calls == []


def test_PR003_network_paths_rejected_by_mapping_loader():
    with pytest.raises(InputError):
        load_mapping("https://invalid.example/mapping.json")


def test_PR003_import_and_mapping_work_without_analytical_or_optional_dependencies(subprocess_env):
    script = r'''
import importlib.abc
import sys
import socket
class Block(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in {'numpy', 'pandas', 'pyarrow', 'networkx'}:
            raise ModuleNotFoundError('dependency blocked')
def blocked(*args, **kwargs):
    raise AssertionError('network blocked')
sys.meta_path.insert(0, Block())
socket.create_connection = socket.getaddrinfo = blocked
socket.socket.connect = socket.socket.connect_ex = blocked
from recursive_integrity_toolkit.io.schema_mapping import compile_mapping, map_row
p = compile_mapping({'schema_version':'1.0','records':{'fields':{'record_id':{'source':'id','operations':[{'op':'trim'}]}}}})
assert map_row({'id':' a '},p).values == {'record_id':'a'}
print('mapping completed with dependencies and network blocked')
'''
    result = subprocess.run([sys.executable, "-c", script], env=subprocess_env,
                            capture_output=True, text=True, check=False)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "mapping completed" in result.stdout
