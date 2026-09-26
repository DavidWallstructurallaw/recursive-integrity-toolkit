"""Phase 1 placeholder for PR-008.

Planned scope:
    Future parent-resolution tests are deferred to Phase 5.

Current Phase 1 scope:
    Verify the approved owner ID and confirm that the target module remains a
    docstring-only, import-safe placeholder.

Limits:
    No mathematical metric, data loading, graph operation, or report result is tested.
"""


# Phase 2 Step 6: PR-008 immediate references, without graph algorithms.
import pytest
from recursive_integrity_toolkit.errors import CanonicalValidationError, ErrorCode, WarningCode
from recursive_integrity_toolkit.io.validation import parse_parent_ids, resolve_parent_references, resolve_version_order
from recursive_integrity_toolkit.models import RecordKey, ParentResolutionStatus, RowLocation, FileRole, ValidationSeverity


def _s6_parent_case(values, **kwargs):
    keys = (RecordKey("v1", "p"), RecordKey("v1", "q"), RecordKey("v2", "c"))
    order = resolve_version_order(("v1", "v2"), document={"version_order": ["v1", "v2"]})
    return resolve_parent_references(keys[-1], values, keys, version_order=order, **kwargs)


def test_PR008_blank_parent_field_is_empty_list():
    assert parse_parent_ids("", csv_encoded=True) == ()
    assert parse_parent_ids(None) is None


def test_PR008_json_empty_array_is_empty_list():
    assert parse_parent_ids("[]", csv_encoded=True) == ()
    assert parse_parent_ids([]) == ()


def test_PR008_multiple_parent_array_parses():
    assert parse_parent_ids('["v1::p","v1::q"]', csv_encoded=True) == ("v1::p", "v1::q")


@pytest.mark.parametrize("value", ['["a",]', '[bad]', '[', '{"x":1}', 'null', 'NaN', '1', 'true'])
def test_PR008_malformed_parent_json_fails(value):
    with pytest.raises(CanonicalValidationError) as exc:
        parse_parent_ids(value, csv_encoded=True)
    assert exc.value.code is ErrorCode.PARENT_FORMAT


@pytest.mark.parametrize("value", ["[]", "a", 1, True, {}, 1.2])
def test_PR008_parent_scalar_fails(value):
    with pytest.raises(CanonicalValidationError):
        parse_parent_ids(value)


@pytest.mark.parametrize("value", [[1], [False], [None], [[]], [{}]])
def test_PR008_parent_non_string_item_fails(value):
    with pytest.raises(CanonicalValidationError):
        parse_parent_ids(value)


def test_PR008_duplicate_parent_warns():
    result = _s6_parent_case(["v1::p", "v1::p"])
    assert len(result.references) == 1
    assert result.references[0].source_references == ("v1::p", "v1::p")
    assert any(m.code == WarningCode.PARENT_DUPLICATE_REFERENCE.value for m in result.messages)


def test_PR008_alias_duplicate_is_one_target_without_losing_source_spelling():
    result = _s6_parent_case(["v1::p", "p"])
    assert len(result.references) == 1 and result.references[0].canonical_reference == "v1::p"
    assert result.references[0].source_references == ("p", "v1::p")
    assert len(result.messages) == 2


def test_PR008_composite_parent_resolves():
    ref = _s6_parent_case(["v1::p"]).references[0]
    assert ref.parent_key == RecordKey("v1", "p")
    assert ref.resolution_status is ParentResolutionStatus.RESOLVED


def test_PR008_multiple_composite_parents_resolve():
    result = _s6_parent_case(["v1::q", "v1::p"])
    assert tuple(ref.canonical_reference for ref in result.references) == ("v1::p", "v1::q")


def test_PR008_unique_bare_parent_warns():
    result = _s6_parent_case(["p"])
    assert result.references[0].canonical_reference == "v1::p"
    assert result.messages[0].code == WarningCode.PARENT_BARE_COMPATIBILITY.value


def test_PR008_unresolved_bare_parent_warns():
    result = _s6_parent_case(["missing"])
    assert result.references[0].parent_key is None and result.references[0].canonical_reference is None
    assert result.references[0].resolution_status is ParentResolutionStatus.UNRESOLVED
    assert any(m.code == WarningCode.PARENT_UNRESOLVED.value for m in result.messages)


def test_PR008_ambiguous_bare_parent_fails():
    keys = (RecordKey("v1", "p"), RecordKey("v2", "p"), RecordKey("v3", "c"))
    with pytest.raises(CanonicalValidationError) as exc:
        resolve_parent_references(keys[-1], ["p"], keys)
    assert exc.value.code is ErrorCode.PARENT_AMBIGUOUS


def test_PR008_future_parent_fails():
    keys = (RecordKey("v1", "c"), RecordKey("v2", "p"))
    order = resolve_version_order(("v1", "v2"), invocation_order=("v1", "v2"))
    with pytest.raises(CanonicalValidationError) as exc:
        resolve_parent_references(keys[0], ["v2::p"], keys, version_order=order)
    assert exc.value.code is ErrorCode.PARENT_FUTURE_VERSION


def test_PR008_unloaded_future_parent_still_fails_when_order_is_declared():
    key = RecordKey("v1", "c")
    order = resolve_version_order(("v1",), document={"version_order": ["v1", "v2"]})
    with pytest.raises(CanonicalValidationError) as exc:
        resolve_parent_references(key, ["v2::p"], (key,), version_order=order)
    assert exc.value.code is ErrorCode.PARENT_FUTURE_VERSION


def test_PR008_same_version_parent_is_input_valid():
    p, c = RecordKey("v1", "p"), RecordKey("v1", "c")
    result = resolve_parent_references(c, ["v1::p"], (p, c))
    assert result.references[0].temporal_status == "same_version"
    assert result.graph_validation_deferred


@pytest.mark.parametrize("ref", ["v1::c", "c"])
def test_PR008_self_parent_rejected_without_general_cycle_analysis(ref):
    key = RecordKey("v1", "c")
    with pytest.raises(CanonicalValidationError) as exc:
        resolve_parent_references(key, [ref], (key,))
    assert exc.value.code is ErrorCode.LINEAGE_CYCLE
    assert "direct self-parent" in exc.value.safe_message


@pytest.mark.parametrize("ref", ["", " p", "p ", "v1::", "::p", "v1::p::x", "v1 ::p", "v1:: p",
                                  "p\x00", "p" * 513, "v" * 257 + "::p"])
def test_PR008_invalid_composite_format_fails(ref):
    with pytest.raises(CanonicalValidationError) as exc:
        _s6_parent_case([ref])
    assert exc.value.code is ErrorCode.PARENT_FORMAT


def test_PR008_missing_chronology_never_invents_future_or_earlier():
    p, c = RecordKey("v10", "p"), RecordKey("v2", "c")
    result = resolve_parent_references(c, ["v10::p"], (p, c))
    assert result.references[0].temporal_status == "unavailable"
    assert any(m.code == WarningCode.VERSION_ORDER_MISSING.value for m in result.messages)


def test_PR008_explicit_strict_promotion_and_error_location():
    result = _s6_parent_case(["missing"], strict_mode=True,
                strict_warning_codes=(WarningCode.PARENT_UNRESOLVED.value,))
    assert any(m.code == WarningCode.PARENT_UNRESOLVED.value and m.severity is ValidationSeverity.ERROR
               for m in result.messages)
    with pytest.raises(CanonicalValidationError) as exc:
        _s6_parent_case([" private_ref "], location=RowLocation(FileRole.PROVENANCE_MANIFEST, "/local/input", 5, 6))
    assert exc.value.row_number == 5 and exc.value.line_number == 6
    assert "private_ref" not in str(exc.value) and exc.value.record_key == "v2::c"


def test_PR008_limit_is_enforced_before_deduplication():
    with pytest.raises(CanonicalValidationError):
        _s6_parent_case(["p", "p"], max_parent_list_length=1)


def test_PR008_order_and_input_immutability():
    values = ["v1::q", "v1::p", "p"]
    before = list(values)
    left = _s6_parent_case(values)
    assert values == before and left == _s6_parent_case(list(reversed(values)))


@pytest.mark.parametrize("option,value", [("csv_encoded", 1), ("max_parent_list_length", 0),
                                         ("max_parent_list_length", True)])
def test_PR008_invalid_parser_options_fail(option, value):
    with pytest.raises(CanonicalValidationError) as exc:
        parse_parent_ids([], **{option: value})
    assert exc.value.code is ErrorCode.CONFIG_INVALID


def test_PR008_deep_malformed_json_does_not_escape_as_recursion_error():
    with pytest.raises(CanonicalValidationError) as exc:
        parse_parent_ids("[" * 2000 + "]" * 2000, csv_encoded=True)
    assert exc.value.code is ErrorCode.PARENT_FORMAT


@pytest.mark.parametrize("mode", ["unresolved", "ambiguous"])
def test_PR008_step6_fixtures(repo_root, mode):
    import json
    path = repo_root / ("tests/fixtures/lineage_" + mode) / ("step6_" + mode + ".json")
    before = path.read_bytes()
    data = json.loads(before)
    keys = tuple(RecordKey.parse(key) for key in data["loaded_keys"])
    child = RecordKey.parse(data["child"])
    if mode == "ambiguous":
        with pytest.raises(CanonicalValidationError) as exc:
            resolve_parent_references(child, data["parent_ids"], keys)
        assert exc.value.code is ErrorCode.PARENT_AMBIGUOUS
    else:
        result = resolve_parent_references(child, data["parent_ids"], keys)
        assert result.references[0].resolution_status is ParentResolutionStatus.UNRESOLVED
    assert path.read_bytes() == before
