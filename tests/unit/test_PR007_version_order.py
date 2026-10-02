"""Phase 2 Step 1 configuration-contract tests for PR-007."""

import pytest

from recursive_integrity_toolkit.config import resolve_config
from recursive_integrity_toolkit.errors import ConfigurationError, ErrorCode


def test_PR007_explicit_list_order_is_preserved() -> None:
    config = resolve_config({"version_order": ["v1", "v2", "v3"]})
    assert config.version_order == ("v1", "v2", "v3")


def test_PR007_duplicate_explicit_version_is_invalid() -> None:
    with pytest.raises(ConfigurationError) as exc_info:
        resolve_config({"version_order": ["v1", "v1"]})
    assert exc_info.value.code is ErrorCode.CONFIG_INVALID


def test_PR007_no_filename_or_lexical_inference_in_step1() -> None:
    config = resolve_config({})
    assert config.version_order == ()


# Phase 2 Step 6: PR-007 ordering evidence.
from dataclasses import replace
from types import MappingProxyType
import pytest
from recursive_integrity_toolkit.errors import CanonicalValidationError, ErrorCode, WarningCode
from recursive_integrity_toolkit.io.validation import resolve_version_order, resolve_parent_references
from recursive_integrity_toolkit.models import RecordKey


def test_PR007_explicit_order_list():
    result = resolve_version_order(("v10", "v2"), document={"version_order": ["v2", "v10"]})
    assert result.order == ("v2", "v10") and result.order_source == "explicit_version_order"


def test_PR007_rank_map_order():
    result = resolve_version_order(("b", "a"), document={"version_rank": {"a": -10, "b": 40}})
    assert result.order == ("a", "b") and result.order_source == "integer_rank"
    assert result.declarations["version_rank"] == {"a": -10, "b": 40}


def test_PR007_timezone_timestamp_order():
    result = resolve_version_order(("a", "b"), document={"version_timestamps": {
        "a": "2026-01-01T10:00:00+05:00", "b": "2026-01-01T04:59:59Z"}})
    assert result.order == ("b", "a") and result.order_source == "version_timestamps"


def test_PR007_explicit_invocation_order_recorded():
    result = resolve_version_order(("b", "a"), invocation_order=("b", "a"))
    assert result.order == ("b", "a") and result.order_source == "invocation_order"
    assert result.invocation_order == ("b", "a")


@pytest.mark.parametrize("document,invoked", [
    ({"version_order": ["a", "b"], "version_rank": {"a": 1, "b": 0}}, None),
    ({"version_order": ["a", "b"]}, ("b", "a")),
    ({"version_timestamps": {"a": "2026-01-02T00:00:00Z", "b": "2026-01-01T00:00:00Z"},
      "version_order": ["a", "b"]}, None),
])
def test_PR007_conflicting_order_fails(document, invoked):
    with pytest.raises(CanonicalValidationError) as exc:
        resolve_version_order(("a", "b"), document=document, invocation_order=invoked)
    assert exc.value.code is ErrorCode.VERSION_ORDER_CONFLICT


@pytest.mark.parametrize("ranks", [{"a": 0, "b": 0}, {"a": True, "b": 1},
                                    {"a": 1.0, "b": 2}, {"a": "0", "b": 1}])
def test_PR007_duplicate_rank_fails(ranks):
    with pytest.raises(CanonicalValidationError):
        resolve_version_order(("a", "b"), document={"version_rank": ranks})


def test_PR007_equal_timestamp_without_tiebreak_fails():
    with pytest.raises(CanonicalValidationError):
        resolve_version_order(("a", "b"), document={"version_timestamps": {
            "a": "2026-01-01T01:00:00+01:00", "b": "2026-01-01T00:00:00Z"}})


@pytest.mark.parametrize("extra", [{"timestamp_tiebreak": ["b", "a"]},
                                    {"version_order": ["b", "a"]},
                                    {"version_rank": {"a": 9, "b": 3}}])
def test_PR007_equal_timestamp_accepts_explicit_tiebreak(extra):
    result = resolve_version_order(("a", "b"), document={"version_timestamps": {
        "a": "2026-01-01T00:00:00Z", "b": "2026-01-01T00:00:00Z"}, **extra})
    assert result.order == ("b", "a")


def test_PR007_missing_order_blocks_longitudinal():
    result = resolve_version_order(("v2", "v10"))
    assert result.order == () and result.order_source == "unavailable"
    assert result.messages[0].code == WarningCode.VERSION_ORDER_MISSING.value


def test_PR007_lexical_filename_order_not_used():
    result = resolve_version_order(("z_earliest.csv", "a_latest.csv"))
    assert result.order == ()
    single = resolve_version_order(("final",))
    assert single.order == ("final",) and single.order_source == "single_version"


@pytest.mark.parametrize("document", [{"version_order": ["a"]}, {"version_rank": {"a": 0}},
    {"version_timestamps": {"a": "2026-01-01T00:00:00Z"}}])
def test_PR007_order_source_cannot_omit_loaded_version(document):
    with pytest.raises(CanonicalValidationError):
        resolve_version_order(("a", "b"), document=document)


@pytest.mark.parametrize("stamp", ["2026-01-01", "2026-01-01T00:00:00", "bad", 0, None, True])
def test_PR007_bad_timestamp_is_error(stamp):
    with pytest.raises(CanonicalValidationError):
        resolve_version_order(("a",), document={"version_timestamps": {"a": stamp}})


@pytest.mark.parametrize("labels", [(), ("a", "a"), ("",), (" a",), ("a::b",),
                                    (1,), (None,), (True,), ("x\x00y",), ("a" * 257,)])
def test_PR007_bad_loaded_version_contract(labels):
    with pytest.raises(CanonicalValidationError):
        resolve_version_order(labels)


@pytest.mark.parametrize("document", [{"version_order": []}, {"version_order": ["a", "a"]},
    {"version_order": "a"}, {"version_rank": {}}, {"surprise": ["a"]},
    {"timestamp_tiebreak": ["a"]}, {"version_timestamps": {}}])
def test_PR007_closed_document_rejects_bad_forms(document):
    with pytest.raises(CanonicalValidationError):
        resolve_version_order(("a",), document=document)


def test_PR007_priority_preserves_all_agreeing_sources_and_extra_declared_versions():
    result = resolve_version_order(("b", "a"), document={"version_order": ["a", "b", "c"],
        "version_rank": {"a": 2, "b": 6, "c": 8}, "version_timestamps": {
        "a": "2026-01-01T00:00:00Z", "b": "2026-01-02T00:00:00Z", "c": "2026-01-03T00:00:00Z"}},
        invocation_order=("a", "b"))
    assert result.order_source == "explicit_version_order" and result.order == ("a", "b", "c")
    assert len(result.source_orders) == 4


def test_PR007_input_is_detached_and_order_flags_are_revalidated():
    document = {"version_order": ["a", "b"]}
    result = resolve_version_order(("a", "b"), document=document)
    document["version_order"].reverse()
    assert result.declarations["version_order"] == ("a", "b")
    with pytest.raises(TypeError):
        result.declarations["version_order"] = ("b", "a")
    forged = replace(result, order=("b", "a"), order_source="invented")
    left, right = RecordKey("a", "p"), RecordKey("b", "c")
    reference = resolve_parent_references(right, ["a::p"], (left, right), version_order=forged)
    assert reference.references[0].temporal_status == "earlier_version"


def test_PR007_explicit_empty_document_is_invalid():
    with pytest.raises(CanonicalValidationError):
        resolve_version_order(("a", "b"), document={})


def test_PR007_unsafe_python_object_is_rejected_without_callbacks():
    class Unsafe:
        def __bool__(self):
            raise AssertionError("executed unsafe callback")
    with pytest.raises(CanonicalValidationError):
        resolve_version_order(("a",), document=Unsafe())


@pytest.mark.parametrize("document,valid", [
    ({"version_order": ["a", "b"]}, True),
    ({"version_rank": {"a": -5, "b": 9}}, True),
    ({"version_timestamps": {"a": "2026-01-01T00:00:00Z"}}, True),
    ({"version_timestamps": {"a": "2026-01-01T00:00:00Z"}, "timestamp_tiebreak": ["a"]}, True),
    ({}, False), ({"version_order": []}, False), ({"version_order": ["a", "a"]}, False),
    ({"version_rank": {"a": True}}, False), ({"version_order": ["a\nb::c"]}, False),
    ({"version_order": ["a\n"]}, False), ({"version_order": ["a\nb"]}, True),
    ({"timestamp_tiebreak": ["a"]}, False), ({"version_order": ["a"], "plugin": "x"}, False),
])
def test_PR007_version_schema_basic_forms(repo_root, document, valid):
    import json
    import jsonschema
    schema = json.loads((repo_root / "schemas/version_order.schema.json").read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator.check_schema(schema)
    assert jsonschema.Draft202012Validator(schema).is_valid(document) is valid


def test_PR007_step6_fixture(repo_root):
    import json
    path = repo_root / "tests/fixtures/version_order/step6_order.json"
    before = path.read_bytes()
    order = resolve_version_order(("release", "archive"), document=json.loads(before))
    assert order.order == ("archive", "release") and path.read_bytes() == before
