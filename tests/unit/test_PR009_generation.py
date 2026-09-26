"""PR-009 declared generation types, expected counts and bounded dependency work."""

import pytest

from recursive_integrity_toolkit.errors import CanonicalValidationError, ErrorCode
from recursive_integrity_toolkit.io.normalization import normalize_row, normalize_table
from recursive_integrity_toolkit.io.loaders import load_table
from recursive_integrity_toolkit.models import InputSource, FileRole


def _row(generation):
    return {"dataset_version": "v1", "record_id": "a", "source_type": "human",
            "provenance_confidence": "unknown", "external_grounding": "yes", "generation": generation}


@pytest.mark.parametrize("value", [0, 1, 2, 1000, None])
def test_PR009_declared_generation_is_preserved_without_inference(value):
    row = normalize_row(_row(value), kind="provenance")
    assert row.values["generation"] == value
    assert "expected_generation" not in row.values and "lineage_depth" not in row.values
    # Even yes-grounding with a nonzero declaration is retained for Step 6 consistency checks.
    assert row.values["external_grounding"] == "yes"


@pytest.mark.parametrize("value", [-1, True, False, 1.0, 1.5, "1", [], {}])
def test_PR009_invalid_native_generation_type(value):
    with pytest.raises(CanonicalValidationError) as exc:
        normalize_row(_row(value), kind="provenance")
    assert exc.value.code is ErrorCode.SCHEMA_TYPE and exc.value.field == "generation"


@pytest.mark.parametrize("token,expected", [("0", 0), ("001", 1), ("2", 2), ("", None), ("null", None)])
def test_PR009_csv_integer_serialization(tmp_path, token, expected):
    path = tmp_path / "generation.csv"
    path.write_text("dataset_version,record_id,source_type,provenance_confidence,external_grounding,generation\n"
                    "v1,a,unknown,unknown,unknown," + token + "\n")
    row = normalize_table(load_table(InputSource(FileRole.PROVENANCE_MANIFEST, path)))[0]
    assert row.values["generation"] == expected


@pytest.mark.parametrize("token", ["1.0", "1.5", "1e1", "-1", "true", "NaN"])
def test_PR009_fractional_or_invalid_csv_generation_fails(tmp_path, token):
    path = tmp_path / "bad-generation.csv"
    path.write_text("dataset_version,record_id,source_type,provenance_confidence,external_grounding,generation\n"
                    "v1,a,unknown,unknown,unknown," + token + "\n")
    with pytest.raises(CanonicalValidationError):
        normalize_table(load_table(InputSource(FileRole.PROVENANCE_MANIFEST, path)))


# Phase 2 Step 6: PR-009 declaration consistency, never lineage depth.
from dataclasses import replace
from types import MappingProxyType
import pytest
from recursive_integrity_toolkit.errors import CanonicalValidationError, ErrorCode, WarningCode
from recursive_integrity_toolkit.io.validation import assess_provenance_row, validate_generation_declarations, resolve_version_order
from recursive_integrity_toolkit.models import RecordKey, RowLocation, FileRole, ValidationSeverity


def _s6_gen_row(identifier, grounding="no", parents=(), generation=None, version="v1", **extra):
    return assess_provenance_row({"dataset_version": version, "record_id": identifier,
        "source_type": "unknown", "provenance_confidence": "confirmed", "external_grounding": grounding,
        "parent_ids": parents, "generation": generation, **extra},
        location=RowLocation(FileRole.PROVENANCE_MANIFEST, None, 1, 2))


def _s6_generations(rows, **options):
    keys = tuple(row.record_key for row in rows)
    return validate_generation_declarations(keys, tuple(rows), **options)


@pytest.mark.parametrize("value", [-1, True, 1.0, "1"])
def test_PR009_negative_generation_fails(value):
    with pytest.raises(CanonicalValidationError):
        _s6_gen_row("a", generation=value)


def test_PR009_grounded_root_generation_zero():
    result = _s6_generations([_s6_gen_row("a", "yes", generation=0)])
    assert result.assessments[0].expected_generation == 0 and not result.has_errors


def test_PR009_grounded_carryover_generation_zero_depth_one():
    result = _s6_generations([_s6_gen_row("a", "yes", generation=0),
                _s6_gen_row("b", "yes", ["v1::a"], 0, transformation="carryover")])
    assert result.assessments[1].expected_generation == 0
    assert result.parents[1].references[0].parent_key == RecordKey("v1", "a")
    assert not hasattr(result.assessments[1], "lineage_depth")
    assert result.parents[1].graph_validation_deferred


def test_PR009_ungrounded_child_generation_one():
    result = _s6_generations([_s6_gen_row("a", "yes", generation=0), _s6_gen_row("b", parents=["v1::a"], generation=1)])
    assert tuple(item.expected_generation for item in result.assessments) == (0, 1)


def test_PR009_second_ungrounded_descendant_generation_two():
    result = _s6_generations([_s6_gen_row("z", "yes", generation=0),
        _s6_gen_row("m", parents=["v1::z"], generation=1), _s6_gen_row("a", parents=["v1::m"], generation=2)])
    assert tuple(item.expected_generation for item in result.assessments) == (2, 1, 0)


def test_PR009_reverse_chain_propagation_and_identity_lookup_have_bounded_work():
    """Catch repeated scans and linear key lookup without a wall-clock gate."""
    import sys

    observations = []
    for size in (128, 512):
        rows = tuple(_s6_gen_row(f"n{index:06d}",
            "yes" if index == size - 1 else "no",
            [] if index == size - 1 else [f"v1::n{index + 1:06d}"],
            size - 1 - index) for index in range(size))
        keys = tuple(row.record_key for row in rows)
        counts = [0, 0]

        def trace(frame, event, arg):
            if frame.f_code is validate_generation_declarations.__code__:
                if event == "line":
                    counts[0] += 1
                return trace
            if frame.f_code is RecordKey.__eq__.__code__ and event == "call":
                counts[1] += 1
            return None

        previous = sys.gettrace()
        sys.settrace(trace)
        try:
            result = validate_generation_declarations(keys, rows)
        finally:
            sys.settrace(previous)
        assert [item.expected_generation for item in result.assessments] == list(reversed(range(size)))
        assert not any(item.mismatch for item in result.assessments)
        observations.append(counts)
    # Four times the records permits sorting overhead, but excludes quadratic
    # dependency scans and tuple-membership comparisons (both formerly >15x).
    assert all(0 < large < small * 6 for small, large in zip(*observations))


def test_PR009_grounding_reset_and_blocked_branches_propagate_independently():
    result = _s6_generations([
        _s6_gen_row("anchor", "yes", ["cycle"], 0),
        _s6_gen_row("cycle", parents=["anchor"], generation=1),
        _s6_gen_row("unknown", "unknown", generation=0),
        _s6_gen_row("mixed", parents=["cycle", "unknown"], generation=2),
        _s6_gen_row("descendant", parents=["mixed"], generation=3),
    ])
    values = {item.record_key.record_id: item for item in result.assessments}
    assert values["anchor"].expected_generation == 0
    assert values["cycle"].expected_generation == 1
    assert values["unknown"].reason_codes == ("GROUNDING_UNKNOWN",)
    for name in ("mixed", "descendant"):
        assert values[name].expected_generation is None
        assert values[name].reason_codes == ("PARENT_GENERATION_UNAVAILABLE",)
    assert not any(message.code == ErrorCode.LINEAGE_CYCLE.value for message in result.messages)


def test_PR009_unknown_grounding_expected_generation_unavailable():
    result = _s6_generations([_s6_gen_row("a", "unknown", generation=0)])
    assert result.assessments[0].expected_generation is None
    assert result.assessments[0].declared_generation == 0
    assert result.assessments[0].reason_codes == ("GROUNDING_UNKNOWN",)


def test_PR009_unresolved_parent_expected_generation_unavailable():
    result = _s6_generations([_s6_gen_row("a", parents=["v1::missing"], generation=9)])
    assert result.assessments[0].expected_generation is None
    assert result.assessments[0].reason_codes == ("PARENT_UNRESOLVED",)


def test_PR009_mismatch_emits_warning():
    result = _s6_generations([_s6_gen_row("a", "yes", generation=8)])
    assert result.assessments[0].mismatch and not result.has_errors
    assert result.messages[-1].code == WarningCode.GENERATION_MISMATCH.value


def test_PR009_strict_mode_promotes_selected_mismatch():
    result = _s6_generations([_s6_gen_row("a", "yes", generation=8)], strict_mode=True,
                strict_warning_codes=(WarningCode.GENERATION_MISMATCH.value,))
    assert result.has_errors and result.messages[-1].severity is ValidationSeverity.ERROR
    assert result.assessments[0].declared_generation == 8


def test_PR009_unresolvable_dependency_does_not_claim_cycle():
    result = _s6_generations([_s6_gen_row("a", parents=["v1::b"], generation=4),
                             _s6_gen_row("b", parents=["v1::a"], generation=5)])
    assert all(item.expected_generation is None for item in result.assessments)
    assert all(item.reason_codes == ("PARENT_GENERATION_UNAVAILABLE",) for item in result.assessments)
    assert not any(message.code == ErrorCode.LINEAGE_CYCLE.value for message in result.messages)
    assert not hasattr(result, "cycles")


def test_PR009_declared_values_never_seed_dependency_expectations():
    result = _s6_generations([_s6_gen_row("a", "yes", generation=50),
                             _s6_gen_row("b", parents=["v1::a"], generation=51)])
    assert tuple(item.expected_generation for item in result.assessments) == (0, 1)
    assert all(item.mismatch for item in result.assessments)


def test_PR009_multiple_parents_use_max_validated_value_not_sum():
    rows = [_s6_gen_row("a", "yes", generation=0), _s6_gen_row("b", parents=["v1::a"], generation=1),
            _s6_gen_row("c", parents=["v1::a", "v1::b", "b"], generation=2)]
    result = _s6_generations(rows)
    assert result.assessments[-1].expected_generation == 2
    assert len(result.parents[-1].references) == 2


def test_PR009_unknown_parent_declaration_is_not_parentlessness():
    result = _s6_generations([_s6_gen_row("a", parents=None, generation=7)])
    assert result.assessments[0].reason_codes == ("PARENT_DECLARATION_UNAVAILABLE",)
    assert result.assessments[0].expected_generation is None


def test_PR009_no_parent_does_not_invent_a_grounded_origin():
    result = _s6_generations([_s6_gen_row("a", generation=0)])
    assert result.assessments[0].reason_codes == ("NO_GROUNDED_DEPENDENCY",)


def test_PR009_cross_version_requires_chronology_for_ungrounded_dependency():
    rows = [_s6_gen_row("a", "yes", generation=0, version="v1"),
            _s6_gen_row("b", parents=["v1::a"], generation=1, version="v2")]
    missing = _s6_generations(rows)
    assert missing.assessments[-1].reason_codes == ("PARENT_CHRONOLOGY_UNAVAILABLE",)
    order = resolve_version_order(("v1", "v2"), invocation_order=("v1", "v2"))
    valid = _s6_generations(rows, version_order=order)
    assert valid.assessments[-1].expected_generation == 1


def test_PR009_incomplete_provenance_keeps_error_and_no_expected_value():
    row = _s6_gen_row("a", "yes", generation=0)
    fields = dict(row.values)
    del fields["provenance_confidence"]
    result = _s6_generations([assess_provenance_row(fields)])
    assert result.has_errors and result.assessments[0].expected_generation is None
    assert any(message.code == ErrorCode.SCHEMA_REQUIRED_FIELD.value for message in result.messages)


def test_PR009_missing_provenance_never_disappears_from_scope():
    keys = (RecordKey("v1", "a"), RecordKey("v1", "b"))
    result = validate_generation_declarations(keys, (_s6_gen_row("a", "yes", generation=0),))
    assert len(result.assessments) == 2
    assert result.assessments[-1].reason_codes == ("PROVENANCE_MISSING",)


def test_PR009_reorders_deterministically_without_mutating_declarations():
    rows = [_s6_gen_row("z", "yes", generation=0), _s6_gen_row("a", parents=["v1::z"], generation=1)]
    left = _s6_generations(rows)
    assert left == _s6_generations(list(reversed(rows)))
    assert rows[1].values["parent_ids"] == ("v1::z",)


def test_PR009_no_file_network_optional_dependency_or_analytic_side_effects(monkeypatch):
    import builtins
    import socket
    from pathlib import Path
    rows = [_s6_gen_row("a", "yes", generation=0, notes="PRIVATE_SENTINEL", source_uri="https://invalid.example")]
    calls = []
    def blocked(*args, **kwargs):
        calls.append(True)
        raise AssertionError("unexpected IO")
    with monkeypatch.context() as patch:
        patch.setattr(builtins, "open", blocked)
        patch.setattr(Path, "open", blocked)
        patch.setattr(socket, "create_connection", blocked)
        patch.setattr(socket, "getaddrinfo", blocked)
        result = _s6_generations(rows)
    assert not calls and "PRIVATE_SENTINEL" not in repr(result)
    for name in ("lineage_depth", "roots", "ancestors", "hhi", "support_size", "maximum_level"):
        assert not hasattr(result, name)


def test_PR009_direct_grounding_reset_does_not_certify_unresolved_parent():
    result = _s6_generations([_s6_gen_row("a", "yes", ["v1::missing"], 0)])
    assert result.assessments[0].expected_generation == 0
    assert result.parents[0].references[0].resolution_status.value == "unresolved"
    assert any(message.code == WarningCode.PARENT_UNRESOLVED.value for message in result.messages)


def test_PR009_forged_assessment_flags_do_not_change_expected_generation():
    row = replace(_s6_gen_row("a", "unknown", generation=0), grounding_known=True, required_fields_valid=True)
    result = _s6_generations([row])
    assert result.assessments[0].expected_generation is None


@pytest.mark.parametrize("mode", ["duplicate_provenance", "unmatched_provenance", "duplicate_keys"])
def test_PR009_invalid_scopes_fail(mode):
    a, b = RecordKey("v1", "a"), RecordKey("v1", "b")
    row = _s6_gen_row("a", "yes", generation=0)
    keys = (a, a) if mode == "duplicate_keys" else ((b,) if mode == "unmatched_provenance" else (a,))
    rows = (row, row) if mode == "duplicate_provenance" else (row,)
    with pytest.raises(CanonicalValidationError):
        validate_generation_declarations(keys, rows)


def test_PR009_step6_generation_fixture(repo_root):
    import json
    path = repo_root / "tests/fixtures/minimal_valid/step6_generation.jsonl"
    before = path.read_bytes()
    rows = tuple(assess_provenance_row(json.loads(line)) for line in before.splitlines())
    order = resolve_version_order(("v1", "v2", "v3"), document={"version_order": ["v1", "v2", "v3"]})
    result = _s6_generations(rows, version_order=order)
    assert tuple(item.expected_generation for item in result.assessments) == (0, 1, 2)
    assert not result.has_errors and path.read_bytes() == before
