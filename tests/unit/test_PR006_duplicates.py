"""PR-006 exact decoded-record-form tests; all inputs are synthetic.

Preserve the historical placeholder-test node ID while testing the implemented
boundary. Public report/redaction tests remain in their separately gated phase.
"""
from dataclasses import FrozenInstanceError, replace
from itertools import permutations
from pathlib import Path
from types import MappingProxyType
import hashlib
import json
import pytest

from recursive_integrity_toolkit.errors import CanonicalValidationError, ErrorCode
from recursive_integrity_toolkit.io.normalization import normalize_row
from recursive_integrity_toolkit.models import (
    CalculationEvidenceClass, CalculationReason, CalculationStatus, ContentMode,
    NormalizationOptions, RecordKey,
)
from recursive_integrity_toolkit.metrics.duplicates import detect_exact_duplicates
from recursive_integrity_toolkit.representations.content_hash import assign_content_states, exact_content_bytes


def row(text="same", key="a", version="v1", **fields):
    return normalize_row({"dataset_version": version, "record_id": key, "content": text, **fields}, kind="records")


def options(**changes):
    result = dict(dataset_versions=("v1",), scope_id="synthetic-exact-scope", representation_name="record_form",
                  representation_version="declared-v1", normalization_profile="exact_utf8_v1", content_mode=ContentMode.INLINE)
    result.update(changes)
    return result


def detect(rows, **changes):
    return detect_exact_duplicates(tuple(rows), **options(**changes))


def test_PR006_identical_normalized_content_groups():
    result = detect((row(key="c"), row("different", "b"), row(key="a")))
    assert result.duplicate_record_count.value == 1
    assert result.duplicate_group_count.value == 1
    group, = result.exact_duplicate_groups
    assert group.record_keys == (RecordKey("v1", "a"), RecordKey("v1", "c"))
    assert group.representative == RecordKey("v1", "a") and group.record_count == 2
    assert group.content_hash == hashlib.sha256(b"same").hexdigest()


def test_PR006_duplicate_record_count_excludes_first_representative():
    rows = tuple(row(t, str(i)) for i, t in enumerate(("a", "a", "a", "b", "b", "c")))
    result = detect(rows)
    assert result.duplicate_record_count.value == 3
    assert result.duplicate_group_count.value == 2
    assert sorted(g.record_count for g in result.exact_duplicate_groups) == [2, 3]
    assert len(rows) == 6 and len(result.scope.included_record_keys) == 6


@pytest.mark.parametrize("size", [1, 2, 3, 10, 100])
def test_PR006_identical_group_size_definition(size):
    result = detect(tuple(row(key=str(i)) for i in range(size)))
    assert result.duplicate_record_count.value == size - 1
    assert result.duplicate_group_count.value == (1 if size > 1 else 0)


@pytest.mark.parametrize("size", [1, 2, 8])
def test_PR006_nonempty_unique_scope_has_real_zero_counts(size):
    result = detect(tuple(row(str(i), str(i)) for i in range(size)))
    assert result.duplicate_record_count.value == result.duplicate_group_count.value == 0
    assert result.duplicate_record_count.status is CalculationStatus.AVAILABLE
    assert result.exact_duplicate_groups == () and result.coverage.ratio == 1.0


def test_PR006_empty_scope_has_unavailable_counts_not_zero():
    result = detect(())
    for count in (result.duplicate_record_count, result.duplicate_group_count):
        assert count.value is None and count.status is CalculationStatus.UNAVAILABLE
        assert count.reason_codes == (CalculationReason.EMPTY_SCOPE,)
    assert result.coverage.ratio is None and result.coverage.denominator == 0
    assert result.scope.dataset_versions == ("v1",)


def test_PR006_profile_is_recorded():
    result = detect((row(),))
    assert result.representation.normalization_profile == "exact_utf8_v1"
    assert result.representation.representation_source == "content_hash"
    assert result.representation.binning_or_mapping_rule == "utf8_identity_then_sha256"
    assert result.representation.representation_version == "declared-v1"
    for count, name, unit in ((result.duplicate_record_count, "duplicate_record_count", "records"),
                              (result.duplicate_group_count, "duplicate_group_count", "groups")):
        m = count.metadata
        assert m.metric_name == name and m.owner_id == "PR-006" and m.formula_id is None
        assert m.unit == unit and m.evidence_class is CalculationEvidenceClass.OBSERVED_FACT
        assert m.weighting.weighting_mode == "unweighted" and m.scope == result.scope
        assert "DEFINITIONS_AND_UNITS:8." in m.method
        assert m.representation == result.representation


def test_PR006_content_hash_does_not_claim_semantic_identity():
    result = detect((row("Hello", "a"), row("hello", "b")))
    assert result.duplicate_record_count.value == 0
    assert "does not establish semantic identity" in " ".join(result.limitations)
    for attr in ("semantic_support", "support_size", "diversity", "authorship", "independent_origins", "report"):
        assert not hasattr(result, attr)


@pytest.mark.parametrize("text,other", [
    ("same", "Same"), ("same", " same"), ("same", "same "), ("a b", "a  b"),
    ("a b", "a\tb"), ("é", "e\u0301"), ("line\nend", "line\r\nend"),
    ("line\nend", "line\rend"), ("text", "\ufefftext"), ("x", "x\n"),
    ("1", "01"), ("unknown", "UNKNOWN"),
])
def test_PR006_profile_preserves_distinct_valid_bytes(text, other):
    exact = assign_content_states((row(text, "a"), row(other, "b")), **options())
    assert [b for _, b in exact.normalized_content] == [text.encode("utf-8"), other.encode("utf-8")]
    assert exact.representation.assignments[0].state_id != exact.representation.assignments[1].state_id
    assert detect((row(text, "a"), row(other, "b"))).duplicate_record_count.value == 0


def test_PR006_known_sha256_and_file_hash_boundary():
    exact = assign_content_states((row("abc"),), **options())
    assert exact.representation.assignments[0].state_id == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
    assert exact.representation.assignments[0].state_id != hashlib.sha256(b'{"content":"abc"}\n').hexdigest()


@pytest.mark.parametrize("profile", [None, "", "sha256", "nfkc", "exact_utf8_v2", True, 1])
def test_PR006_unsupported_profile_fails(profile):
    with pytest.raises(CanonicalValidationError) as error:
        detect((row(),), normalization_profile=profile)
    assert error.value.code is ErrorCode.CONFIG_INVALID


@pytest.mark.parametrize("text", [None, 1, True, b"abc", [], {}, "", " \t\r\n", "\x00", "x\x00y", "\ud800"])
def test_PR006_invalid_content_is_not_repaired(text):
    with pytest.raises(CanonicalValidationError):
        exact_content_bytes(text, normalization_profile="exact_utf8_v1")


@pytest.mark.parametrize("field", ["representation_name", "representation_version", "scope_id"])
@pytest.mark.parametrize("value", [None, "", 1, "\x00", "\ud800"])
def test_PR006_missing_representation_metadata_fails(field, value):
    with pytest.raises(CanonicalValidationError):
        detect((row(),), **{field: value})


@pytest.mark.parametrize("versions", [(), ("v1", "v2"), ("v1", "v1"), ["v1"], "v1", ("absent",)])
def test_PR006_ambiguous_or_absent_scope_is_rejected(versions):
    with pytest.raises(CanonicalValidationError):
        detect((row(),), dataset_versions=versions)


def test_PR006_single_version_selection_does_not_pool_equal_copies():
    records = (row(key="a"), row(key="b", version="v2"), row(key="a", version="v2"))
    assert detect(records).duplicate_record_count.value == 0
    second = detect(records, dataset_versions=("v2",))
    assert second.duplicate_record_count.value == 1 and second.scope.dataset_versions == ("v2",)


def test_PR006_duplicate_composite_identity_is_error_not_deduplication():
    with pytest.raises(CanonicalValidationError) as error:
        detect((row(), row()))
    assert error.value.code is ErrorCode.RECORD_DUPLICATE_ID


@pytest.mark.parametrize("content_mode", [None, "inline", "local_ref", True])
def test_PR006_content_mode_cannot_be_inferred(content_mode):
    with pytest.raises(CanonicalValidationError):
        detect((row(),), content_mode=content_mode)


@pytest.mark.parametrize("payload", [None, {}, {RecordKey("v1", "other"): "text"}, {"v1::a": "text"}, []])
def test_PR006_local_path_without_exact_payload_is_never_hashed(payload):
    with pytest.raises(CanonicalValidationError):
        detect((row("secret/file.txt"),), content_mode=ContentMode.LOCAL_REF, resolved_content=payload)


def test_PR006_inline_rejects_payload_substitution():
    with pytest.raises(CanonicalValidationError):
        detect((row(),), resolved_content={RecordKey("v1", "a"): "replacement"})


def test_PR006_local_reference_uses_payload_not_path(tmp_path):
    from recursive_integrity_toolkit.io.loaders import load_content_reference
    from recursive_integrity_toolkit.config import ResourceLimits
    raw = b"\xef\xbb\xbfsame\r\ntext"
    (tmp_path / "first.txt").write_bytes(raw)
    (tmp_path / "second.txt").write_bytes(raw)
    rows = tuple(normalize_row({"dataset_version": "v1", "record_id": key, "content": file},
                  kind="records", options=NormalizationOptions(content_mode=ContentMode.LOCAL_REF))
                 for key, file in (("a", "first.txt"), ("b", "second.txt")))
    loaded = {rec.record_key: load_content_reference(rec.values["content"], base_directory=tmp_path,
                                                    limits=ResourceLimits(max_content_bytes=100)) for rec in rows}
    result = detect(rows, content_mode=ContentMode.LOCAL_REF, resolved_content=loaded)
    assert result.duplicate_record_count.value == 1
    assert result.exact_duplicate_groups[0].content_hash == hashlib.sha256(raw).hexdigest()
    assert result.exact_duplicate_groups[0].content_hash != hashlib.sha256(b"first.txt").hexdigest()
    assert rows[0].values["content"] == "first.txt"
    assert (tmp_path / "first.txt").read_bytes() == raw


def test_PR006_equal_path_strings_do_not_override_different_supplied_text():
    records = (row("same_path.txt", "a"), row("same_path.txt", "b"))
    payloads = {RecordKey("v1", "a"): "first", RecordKey("v1", "b"): "second"}
    assert detect(records, content_mode=ContentMode.LOCAL_REF, resolved_content=payloads).duplicate_record_count.value == 0


@pytest.mark.parametrize("value", [None, 1, b"text", "", " \n", "x\x00", "\ud800"])
def test_PR006_supplied_payload_validation(value):
    with pytest.raises(CanonicalValidationError):
        detect((row("file.txt"),), content_mode=ContentMode.LOCAL_REF, resolved_content={RecordKey("v1", "a"): value})


def test_PR006_plain_read_only_payload_mapping_is_snapshotted():
    payload = {RecordKey("v1", "a"): "payload"}
    exact = assign_content_states((row("file.txt"),), **options(content_mode=ContentMode.LOCAL_REF,
                                   resolved_content=MappingProxyType(payload)))
    payload[RecordKey("v1", "a")] = "changed"
    assert exact.normalized_content == ((RecordKey("v1", "a"), b"payload"),)


def test_PR006_artificial_hash_collision_blocks_without_renaming(monkeypatch):
    import recursive_integrity_toolkit.representations.content_hash as module
    monkeypatch.setattr(module, "sha256_bytes", lambda _: "0" * 64)
    with pytest.raises(CanonicalValidationError) as error:
        detect((row("first", "a"), row("second", "b")))
    assert error.value.code is ErrorCode.SCHEMA_TYPE
    assert "first" not in str(error.value) and "second" not in str(error.value)
    assert detect((row("first", "a"), row("first", "b"))).duplicate_record_count.value == 1


def test_PR006_row_permutations_preserve_groups_and_representatives():
    rows = (row("z", "d"), row("a", "b"), row("z", "c"), row("a", "a"))
    expected = detect(rows)
    for permutation in permutations(rows):
        assert detect(permutation) == expected
    digests = tuple(g.content_hash for g in expected.exact_duplicate_groups)
    assert digests == tuple(sorted(digests))
    assert all(g.record_keys == tuple(sorted(g.record_keys)) for g in expected.exact_duplicate_groups)


def test_PR006_independent_copies_and_weights_do_not_imply_origin_or_change_counts():
    rows = (row(key="a", source_type="human", weight=0.0), row(key="b", source_type="sensor", weight=100.0))
    before = tuple(dict(r.values) for r in rows)
    result = detect(rows)
    assert result.duplicate_record_count.value == 1
    assert result.duplicate_record_count.metadata.weighting.weighting_mode == "unweighted"
    assert before == tuple(dict(r.values) for r in rows) and len(rows) == 2
    assert not hasattr(result, "source_type_shares") and not hasattr(result, "provenance")


def test_PR006_internal_repr_hides_content_report_deferred(capsys):
    rows = (row("PRIVATE_CONTENT", "a", notes="PRIVATE_NOTE"), row("PRIVATE_CONTENT", "b"))
    result = detect(rows)
    exact = assign_content_states(rows, **options())
    assert "PRIVATE_CONTENT" not in repr(result) + repr(exact)
    assert "PRIVATE_NOTE" not in repr(result) + repr(exact)
    assert capsys.readouterr() == ("", "")
    assert not hasattr(result, "render")


def test_PR006_results_are_immutable_and_detached():
    rows = (row(key="a"), row(key="b"))
    result = detect(rows)
    with pytest.raises(FrozenInstanceError):
        result.duplicate_record_count = None
    with pytest.raises(FrozenInstanceError):
        result.exact_duplicate_groups[0].content_hash = "changed"
    assert result.coverage.numerator == result.coverage.denominator == 2
    assert result.scope.excluded_record_keys == ()


@pytest.mark.parametrize("argument", ["near_duplicate", "similarity_threshold", "embedding", "callback", "weighting"])
def test_PR006_no_undeclared_analysis_options(argument):
    with pytest.raises(TypeError):
        detect((row(),), **{argument: True})


def test_PR006_runtime_no_files_network_logging_or_callbacks(monkeypatch, capsys):
    import builtins
    import socket
    import logging
    import subprocess
    rows = (row(key="a"), row(key="b"))
    calls = []
    class Hostile:
        def __str__(self):
            calls.append("str"); raise AssertionError("callback")
        def __bool__(self):
            calls.append("bool"); raise AssertionError("callback")
        def __iter__(self):
            calls.append("iter"); raise AssertionError("callback")
    def blocked(*args, **kwargs):
        raise AssertionError("unexpected I/O or logging")
    with monkeypatch.context() as patch:
        for owner, name in ((builtins, "open"), (Path, "open"), (Path, "read_text"), (Path, "read_bytes"),
                            (socket, "create_connection"), (socket, "getaddrinfo"),
                            (socket.socket, "connect"), (logging.Logger, "_log"), (subprocess, "run")):
            patch.setattr(owner, name, blocked)
        assert detect(rows).duplicate_record_count.value == 1
        with pytest.raises(CanonicalValidationError):
            exact_content_bytes(Hostile(), normalization_profile="exact_utf8_v1")
        with pytest.raises(CanonicalValidationError):
            detect(rows, content_mode=ContentMode.LOCAL_REF, resolved_content=Hostile())
    assert calls == [] and capsys.readouterr() == ("", "")


def test_PR006_fixture_matches_independent_literal_expectations(repo_root):
    data = [json.loads(line) for line in (repo_root / "tests/fixtures/minimal_valid/phase3_exact_content.jsonl").read_text(encoding="utf-8").splitlines()]
    rows = tuple(normalize_row(item, kind="records") for item in data)
    result = detect(rows)
    assert result.duplicate_record_count.value == 3 and result.duplicate_group_count.value == 2
    assert len(result.scope.included_record_keys) == 10
    assert {tuple(k.record_id for k in g.record_keys) for g in result.exact_duplicate_groups} == {("a1", "a2", "a3"), ("b1", "b2")}
    # These literal expected groups are authored here, never generated by the implementation.
