"""T4 complete external roots, target classification and evidence boundaries.

Frozen fixture root sets and rational coverages predate implementation. These
tests make no incidence, concentration, bound, report or performance claim.
"""

from dataclasses import FrozenInstanceError, replace
from fractions import Fraction
import json
from pathlib import Path
import socket
from types import MappingProxyType

import pytest

from recursive_integrity_toolkit.config import RepresentationConfig
from recursive_integrity_toolkit.errors import CanonicalValidationError
from recursive_integrity_toolkit.io.validation import (
    assess_provenance_row, join_provenance, resolve_parent_batch,
    resolve_version_order, validate_bundle,
)
from recursive_integrity_toolkit.lineage import ancestry
from recursive_integrity_toolkit.models import (
    AuditBundle, FileRole, InputSource, RecordKey, ValidationMessage, ValidationSeverity,
)
from recursive_integrity_toolkit.representations.field import assign_field_states
from recursive_integrity_toolkit.result import ExecutionStatus


_ABSENT = object()
_MISSING = object()
_ROOT = Path(__file__).resolve().parents[2]
_FIXTURES = _ROOT / "tests" / "fixtures"
_CASES = [
    case
    for directory in ("lineage_complete", "lineage_multi_root", "lineage_cycles")
    for case in json.loads((_FIXTURES / directory / "cases.json").read_text())["cases"]
]
_FIXTURE_REASONS = {
    "unknown_grounding": "UNKNOWN_GROUNDING",
    "undeclared_parent_boundary": "PARENT_DECLARATION_UNAVAILABLE",
    "unsupported_grounded_parent_rule": "GROUNDED_PARENT_RULE_UNSUPPORTED",
    "missing_parent": "UNRESOLVED_PARENT_REFERENCE",
}


def _key(identity):
    return RecordKey.parse(identity)


def _load_rows(tmp_path, records, provenance, *, target="v2", order=None, strict=False):
    """Construct real validated inputs; only empty selection needs a typed role."""
    tmp_path.mkdir(parents=True, exist_ok=True)
    primary = [row for row in records if row["dataset_version"] == target]
    context = [row for row in records if row["dataset_version"] != target]
    empty_target = not primary
    if empty_target:
        primary, context = context, []
    sources = []
    for name, role, rows in (
        ("primary.jsonl", FileRole.RECORDS_PRIMARY, primary),
        ("context.jsonl", FileRole.RECORDS_COMPARE, context),
        ("provenance.jsonl", FileRole.PROVENANCE_MANIFEST, provenance),
    ):
        if rows:
            path = tmp_path / name
            path.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")
            sources.append(InputSource(role, path))
    if order is not None:
        path = tmp_path / "order.json"
        path.write_text(json.dumps({"version_order": order}), encoding="utf-8")
        sources.append(InputSource(FileRole.VERSION_ORDER, path))
    config = {"strict_mode": True, "strict_warning_codes": ["W_PARENT_UNRESOLVED"]} if strict else None
    result = validate_bundle(AuditBundle(tuple(sources)), configuration=config)
    if empty_target:
        # The API permits an empty selection over loaded context. Current CLI
        # ingestion still requires a primary file, so change only role metadata.
        result = replace(result, records=tuple(
            replace(row, location=replace(row.location, file_role=FileRole.RECORDS_COMPARE))
            for row in result.records
        ))
    return result


def _validation(tmp_path, declarations, *, grounding=None, transformation=None,
                target="v2", chronology=True, strict=False, reverse=False):
    records, provenance = [], []
    for identity, parents in declarations.items():
        key = _key(identity)
        identity_fields = {"dataset_version": key.dataset_version, "record_id": key.record_id}
        records.append({**identity_fields, "content": "Private ancestry fixture"})
        if parents is _MISSING:
            continue
        grounding_value = (grounding or {}).get(identity, "no")
        row = {
            **identity_fields, "source_type": "human" if grounding_value == "yes" else "synthetic",
            "provenance_confidence": "confirmed", "external_grounding": grounding_value,
            "transformation": (transformation or {}).get(identity, "generate"),
        }
        if parents is not _ABSENT:
            row["parent_ids"] = list(reversed(parents)) if reverse and isinstance(parents, list) else parents
        provenance.append(row)
    if reverse:
        records.reverse()
        provenance.reverse()
    versions = sorted({row["dataset_version"] for row in records} | ({target} if target else set()))
    return _load_rows(tmp_path, records, provenance, target=target,
                      order=versions if chronology else None, strict=strict)


def _fixture_validation(tmp_path, case):
    targets = case["target_record_keys"]
    target = _key(targets[0]).dataset_version if targets else None
    return _load_rows(tmp_path, case["records"], case["provenance"],
                      target=target, order=case["version_order"]), target


def _by_key(result):
    assert result.records is not None
    return {str(item.record_key): item for item in result.records}


def _analyze(validation, target="v2"):
    return ancestry.analyze_lineage(validation, target_dataset_version=target)


def _replace_provenance(validation, rows, *, rebuild_join=False):
    keys = tuple(sorted(row.record_key for row in validation.records))
    batch = resolve_parent_batch(keys, rows, version_order=validation.version_order)
    changes = {"provenance": rows, "parent_validation": batch, "generation": None}
    if rebuild_join:
        changes["provenance_join"] = join_provenance(validation.records, rows)
    return replace(validation, **changes)


@pytest.mark.parametrize("case", _CASES, ids=lambda case: case["case_id"])
def test_frozen_ancestry_oracles_cover_complete_sets_and_target_partition(case, tmp_path):
    validation, target = _fixture_validation(tmp_path, case)
    result = _analyze(validation, target)
    expected = case["expected_lineage"]
    counts = expected["counts"]
    records = _by_key(result)
    assert tuple(records) == tuple(case["target_record_keys"])
    assert result.scope.target_record_count == counts["target"]
    assert result.scope.loaded_record_count == len(case["records"])
    assert result.scope.context_record_count == len(case["records"]) - counts["target"]
    assert (result.grounded_record_count, result.closed_record_count, result.unresolved_record_count) == (
        counts["grounded"], counts["closed"], counts["unresolved"])
    assert result.records_with_resolved_external_ancestry == counts["grounded"] + counts["closed"]
    assert sum((result.grounded_record_count, result.closed_record_count, result.unresolved_record_count)) == len(records)
    actual_complete = {key: sorted(map(str, item.external_root_keys)) for key, item in records.items()
                       if item.external_root_keys is not None}
    assert actual_complete == expected["complete_root_sets"]
    for key, item in records.items():
        if key not in expected["complete_root_sets"]:
            assert item.classification == "unresolved"
            assert item.external_root_keys is None
            assert item.reason_codes
        else:
            assert item.classification == ("grounded" if expected["complete_root_sets"][key] else "closed")
            assert item.reason_codes == ()
        for reason in expected.get("unresolved_reasons", {}).get(key, ()):
            assert _FIXTURE_REASONS[reason] in item.reason_codes
        if key in expected.get("depth_by_record", {}):
            assert item.lineage_depth == expected["depth_by_record"][key]
    for fixture_name, result_name in (
        ("resolved_lineage_coverage", "resolved_lineage_coverage"),
        ("external_ancestry_coverage", "external_ancestry_coverage"),
        ("edge_coverage", "resolved_parent_edge_coverage"),
    ):
        if fixture_name in expected:
            value = getattr(result, result_name)
            if expected[fixture_name] is None:
                assert value is None
            else:
                assert value == pytest.approx(float(Fraction(expected[fixture_name])))
    if "no_declared_parents" in expected:
        assert result.no_declared_parents is expected["no_declared_parents"]
    input_expected = case["expected_input"]
    if "target_declared_references" in input_expected:
        assert result.declared_parent_reference_count == input_expected["target_declared_references"]
        assert result.resolved_parent_reference_count == input_expected["target_resolved_references"]
    if expected.get("lineage_error") or counts["unresolved"]:
        assert result.execution_status is ExecutionStatus.PARTIAL
    else:
        assert result.execution_status is ExecutionStatus.COMPLETED
    assert result.cycles.detected is expected.get("cycle_detected", False)


def test_hero_all_targets_have_the_frozen_single_root_assignments():
    hero = _ROOT / "examples" / "hero"
    expected = json.loads((_FIXTURES / "lineage_complete" / "hero_expected.json").read_text())
    validation = validate_bundle(AuditBundle((
        InputSource(FileRole.RECORDS_PRIMARY, hero / "records_v2.csv"),
        InputSource(FileRole.RECORDS_COMPARE, hero / "records_v1.csv"),
        InputSource(FileRole.PROVENANCE_MANIFEST, hero / "provenance.csv"),
        InputSource(FileRole.VERSION_ORDER, hero / "version_order.json"),
    )))
    result = _analyze(validation)
    assert result.execution_status is ExecutionStatus.COMPLETED
    assert result.scope.target_record_count == expected["target_records"]
    assert result.scope.loaded_record_count == expected["loaded_records"]
    assert (result.grounded_record_count, result.closed_record_count, result.unresolved_record_count) == (8, 0, 0)
    expected_roots = {
        "v2::v2_01": "v1::v1_01", "v2::v2_02": "v1::v1_02",
        "v2::v2_03": "v1::v1_03", "v2::v2_04": "v1::v1_04",
        "v2::v2_05": "v1::v1_01", "v2::v2_06": "v1::v1_02",
        "v2::v2_07": "v1::v1_07", "v2::v2_08": "v1::v1_01",
    }
    assert {key: item.external_root_keys for key, item in _by_key(result).items()} == {
        key: frozenset({_key(root)}) for key, root in expected_roots.items()
    }
    assert result.declared_parent_reference_count == expected["declared_target_references"]
    assert result.resolved_parent_reference_count == expected["resolved_target_references"]
    assert result.resolved_lineage_coverage == result.external_ancestry_coverage == 1.0


def test_missing_provenance_unknown_and_undeclared_boundaries_never_become_empty_roots(tmp_path):
    result = _analyze(_validation(tmp_path, {
        "v2::absent": _ABSENT, "v2::null": None, "v2::missing": _MISSING,
        "v2::unknown": [], "v2::closed": [], "v2::anchor": [],
    }, grounding={"v2::unknown": "unknown", "v2::anchor": "yes"}))
    records = _by_key(result)
    for identity in ("v2::absent", "v2::null", "v2::missing", "v2::unknown"):
        assert records[identity].external_root_keys is None
    assert records["v2::closed"].external_root_keys == frozenset()
    assert records["v2::anchor"].external_root_keys == frozenset({_key("v2::anchor")})
    assert "MISSING_PROVENANCE" in records["v2::missing"].reason_codes
    assert records["v2::unknown"].lineage_depth == 0
    assert result.no_declared_parents is True
    assert result.resolved_parent_edge_coverage == 1.0
    assert (result.grounded_record_count, result.closed_record_count, result.unresolved_record_count) == (1, 1, 4)
    assert result.resolved_lineage_coverage == pytest.approx(1 / 3)
    assert result.external_ancestry_coverage == pytest.approx(1 / 6)


@pytest.mark.parametrize("parent_grounding,expected_roots", [("yes", {"v1::a"}), ("no", set()), ("unknown", None)])
def test_carryover_inherits_single_canonical_parent_including_known_empty(tmp_path, parent_grounding, expected_roots):
    result = _analyze(_validation(tmp_path, {"v1::a": [], "v2::carry": ["a", "v1::a", "a"]},
        grounding={"v1::a": parent_grounding, "v2::carry": "yes"},
        transformation={"v2::carry": "carryover"}))
    record = _by_key(result)["v2::carry"]
    assert record.external_root_keys == (None if expected_roots is None else frozenset(map(_key, expected_roots)))
    assert record.lineage_depth == 1
    assert result.declared_parent_reference_count == result.resolved_parent_reference_count == 3


@pytest.mark.parametrize("transformation,parents", [
    ("generate", ["v1::a"]), ("carryover", ["v1::a", "v1::b"]),
])
def test_unsupported_grounded_parent_rule_never_mints_new_root(tmp_path, transformation, parents):
    result = _analyze(_validation(tmp_path, {"v1::a": [], "v1::b": [], "v2::child": parents},
        grounding={"v1::a": "yes", "v1::b": "yes", "v2::child": "yes"},
        transformation={"v2::child": transformation}))
    child = _by_key(result)["v2::child"]
    assert child.external_root_keys is None
    assert "GROUNDED_PARENT_RULE_UNSUPPORTED" in child.reason_codes
    assert child.lineage_depth == 1
    assert result.execution_status is ExecutionStatus.PARTIAL


def test_unresolved_branch_propagates_without_promoting_observed_roots(tmp_path):
    result = _analyze(_validation(tmp_path, {
        "v1::a": [], "v1::u": [], "v2::incomplete": ["v1::a", "v1::u", "v1::missing"],
        "v2::next": ["v2::incomplete", "v1::a"], "v2::closed": [],
    }, grounding={"v1::a": "yes", "v1::u": "unknown"}))
    records = _by_key(result)
    for key in ("v2::incomplete", "v2::next"):
        assert records[key].external_root_keys is None
        assert records[key].classification == "unresolved"
        assert {"UNKNOWN_GROUNDING", "UNRESOLVED_PARENT_REFERENCE"} <= set(records[key].reason_codes)
    assert (result.grounded_record_count, result.closed_record_count, result.unresolved_record_count) == (0, 1, 2)


def test_unknown_chronology_preserves_identity_coverage_and_blocks_exact_ancestry(tmp_path):
    result = _analyze(_validation(tmp_path, {"v10::anchor": [], "v2::child": ["v10::anchor"]},
        grounding={"v10::anchor": "yes"}, chronology=False))
    record = _by_key(result)["v2::child"]
    assert record.external_root_keys is None
    assert "VERSION_ORDER_UNAVAILABLE" in record.reason_codes
    assert record.lineage_depth is None
    assert result.declared_parent_reference_count == result.resolved_parent_reference_count == 1
    assert result.resolved_parent_edge_coverage == 1.0
    assert result.cycles.cycle_count == 0
    assert result.execution_status is ExecutionStatus.PARTIAL


@pytest.mark.parametrize("invalid,error_code", [
    ("p", "E_PARENT_AMBIGUOUS"), ("v3::future", "E_PARENT_FUTURE_VERSION"),
    (" malformed ", "E_PARENT_FORMAT"), ("v2::child", "E_LINEAGE_CYCLE"),
])
def test_invalid_parent_with_valid_sibling_never_yields_partial_exact_root_set(tmp_path, invalid, error_code):
    result = _analyze(_validation(tmp_path, {
        "v1::a": [], "v1::p": [], "v2::p": [], "v3::future": [],
        "v2::child": ["v1::a", invalid],
    }, grounding={"v1::a": "yes"}))
    assert _by_key(result)["v2::child"].external_root_keys is None
    assert result.declared_parent_reference_count == 2
    assert result.resolved_parent_reference_count == 1
    assert result.unresolved_parent_reference_count == 1
    assert result.resolved_parent_edge_coverage == 0.5
    assert error_code in {message.code for message in result.messages}
    assert result.execution_status is ExecutionStatus.PARTIAL  # Independent target p is known closed.


@pytest.mark.parametrize("safe_target,expected_status", [(False, ExecutionStatus.FAILED), (True, ExecutionStatus.PARTIAL)])
def test_strict_missing_parent_preserves_severity_and_usable_target_rule(tmp_path, safe_target, expected_status):
    declarations = {"v2::child": ["missing"]}
    if safe_target:
        declarations["v2::closed"] = []
    ordinary = _analyze(_validation(tmp_path / "ordinary", declarations))
    strict = _analyze(_validation(tmp_path / "strict", declarations, strict=True))
    assert ordinary.execution_status is ExecutionStatus.PARTIAL
    assert strict.execution_status is expected_status
    assert ordinary.records == strict.records
    assert strict.unresolved_record_count == 1
    assert strict.closed_record_count == int(safe_target)
    assert [m.severity for m in ordinary.messages if m.code == "W_PARENT_UNRESOLVED"] == [ValidationSeverity.WARNING]
    assert [m.severity for m in strict.messages if m.code == "W_PARENT_UNRESOLVED"] == [ValidationSeverity.ERROR]


def test_all_cycle_targets_fail_without_discarding_completed_partition(tmp_path):
    result = _analyze(_validation(tmp_path, {"v2::a": ["v2::b"], "v2::b": ["v2::a"]}))
    assert result.execution_status is ExecutionStatus.FAILED
    assert (result.grounded_record_count, result.closed_record_count, result.unresolved_record_count) == (0, 0, 2)
    assert result.records_with_resolved_external_ancestry == 0
    assert result.resolved_lineage_coverage == result.external_ancestry_coverage == 0.0
    assert result.resolved_parent_edge_coverage == 1.0
    assert all(item.external_root_keys is None and "CYCLE_AFFECTED" in item.reason_codes for item in result.records)


@pytest.mark.parametrize("selection", [None, "v2"])
def test_empty_selected_population_keeps_context_out_of_ratios(tmp_path, selection):
    validation = _validation(tmp_path, {"v1::anchor": []}, target=None,
                             grounding={"v1::anchor": "yes"})
    if selection is not None:
        order = resolve_version_order(("v1",), document={"version_order": ["v1", "v2"]})
        validation = replace(validation, version_order=order,
                             parent_validation=replace(validation.parent_validation, version_order=order))
    result = _analyze(validation, selection)
    assert result.execution_status is ExecutionStatus.COMPLETED
    assert result.scope.target_dataset_version == selection
    assert result.scope.target_record_count == 0
    assert result.scope.context_record_count == 1
    assert result.records == ()
    assert (result.grounded_record_count, result.closed_record_count, result.unresolved_record_count) == (0, 0, 0)
    assert result.resolved_lineage_coverage is result.external_ancestry_coverage is None
    assert "EMPTY_TARGET_SCOPE" in result.ancestry_coverage_reason_codes
    assert result.no_declared_parents is True
    assert result.resolved_parent_edge_coverage == 1.0


def test_missing_required_provenance_is_unresolved_with_error_and_intact_depth(tmp_path):
    validation = _validation(tmp_path, {"v2::incomplete": [], "v2::closed": []},
                             grounding={"v2::incomplete": "yes"})
    rows = []
    for row in validation.provenance:
        if str(row.record_key) == "v2::incomplete":
            values = dict(row.values)
            del values["source_type"]
            rows.append(assess_provenance_row(values, location=row.location))
        else:
            rows.append(row)
    result = _analyze(_replace_provenance(validation, tuple(rows), rebuild_join=True))
    incomplete = _by_key(result)["v2::incomplete"]
    assert incomplete.external_root_keys is None
    assert "MISSING_REQUIRED_PROVENANCE" in incomplete.reason_codes
    assert incomplete.lineage_depth == 0
    assert result.execution_status is ExecutionStatus.PARTIAL
    assert any(m.code == "E_SCHEMA_REQUIRED_FIELD" and m.severity is ValidationSeverity.ERROR for m in result.messages)


def test_record_and_provenance_metadata_namespaces_do_not_invalidate_grounding(tmp_path):
    records = [{"dataset_version": "v2", "record_id": "anchor", "content": "Fixture", "batch_id": "one"}]
    provenance = [{"dataset_version": "v2", "record_id": "anchor", "batch_id": "two",
                   "source_type": "human", "provenance_confidence": "confirmed",
                   "external_grounding": "yes", "parent_ids": []}]
    validation = _load_rows(tmp_path, records, provenance, order=["v2"])
    assert validation.provenance_join.matches[0].conflicting_fields == ("batch_id",)
    result = _analyze(validation)
    record = _by_key(result)["v2::anchor"]
    assert record.external_root_keys == frozenset({_key("v2::anchor")})
    assert record.reason_codes == ()
    assert record.lineage_depth == 0
    assert result.execution_status is ExecutionStatus.COMPLETED
    assert validation.records[0].values["batch_id"] == "one"
    assert validation.provenance[0].values["batch_id"] == "two"


@pytest.mark.parametrize("malformed,expected_declared,expected_resolved", [
    ("not-a-parent-list", None, None), (("v1::a", 7), 2, 1),
])
def test_malformed_parent_container_never_becomes_zero_declared_parents(tmp_path, malformed, expected_declared, expected_resolved):
    validation = _validation(tmp_path, {"v1::a": [], "v2::child": ["v1::a"], "v2::closed": []},
                             grounding={"v1::a": "yes"})
    rows = tuple(replace(row, values=MappingProxyType({**row.values, "parent_ids": malformed}))
                 if str(row.record_key) == "v2::child" else row for row in validation.provenance)
    result = _analyze(_replace_provenance(validation, rows))
    assert _by_key(result)["v2::child"].external_root_keys is None
    assert result.declared_parent_reference_count == expected_declared
    assert result.resolved_parent_reference_count == expected_resolved
    assert result.no_declared_parents is False
    if expected_declared is None:
        assert result.unresolved_parent_reference_count is None
        assert result.resolved_parent_edge_coverage is None
        assert "PARENT_REFERENCE_COUNT_UNAVAILABLE" in result.reference_coverage_reason_codes
    else:
        assert result.unresolved_parent_reference_count == 1
        assert result.resolved_parent_edge_coverage == 0.5
    assert result.execution_status is ExecutionStatus.PARTIAL


def test_representation_ineligible_records_remain_in_target_population(tmp_path):
    records = [{"dataset_version": "v2", "record_id": name, "content": "Fixture", "topic": None}
               for name in ("anchor", "closed")]
    provenance = [{"dataset_version": "v2", "record_id": name, "source_type": "unknown",
                   "provenance_confidence": "confirmed", "external_grounding": grounding, "parent_ids": []}
                  for name, grounding in (("anchor", "yes"), ("closed", "no"))]
    validation = _load_rows(tmp_path, records, provenance, order=["v2"])
    represented = assign_field_states(validation.records, dataset_versions=("v2",), scope_id="missing-topic",
        config=RepresentationConfig("topic", "topic_field", "topic", "fixture-v1", "exclude"))
    assert represented.excluded_count == 2
    assert represented.included_count == 0
    result = _analyze(validation)
    assert result.scope.target_record_count == 2
    assert (result.grounded_record_count, result.closed_record_count, result.unresolved_record_count) == (1, 1, 0)
    assert result.external_ancestry_coverage == 0.5


def test_results_are_permutation_invariant_and_immutable(tmp_path):
    declarations = {"v1::b": [], "v1::a": [], "v2::child": ["v1::b", "a", "v1::a"]}
    grounding = {"v1::a": "yes", "v1::b": "yes"}
    left = _analyze(_validation(tmp_path / "left", declarations, grounding=grounding))
    right = _analyze(_validation(tmp_path / "right", declarations, grounding=grounding, reverse=True))
    assert left == right
    record = left.records[0]
    assert type(record.external_root_keys) is frozenset
    with pytest.raises(FrozenInstanceError):
        left.grounded_record_count = 0
    with pytest.raises(FrozenInstanceError):
        record.external_root_keys = frozenset()
    with pytest.raises(AttributeError):
        record.external_root_keys.add(_key("v1::new"))
    with pytest.raises(TypeError):
        left.cycles.depths_by_record[_key("v2::child")] = None


def test_analysis_consumes_in_memory_evidence_without_io_or_content_leakage(tmp_path, monkeypatch):
    validation = _validation(tmp_path, {"v1::a": [], "v2::child": ["v1::a", "secret-missing-parent"]},
                             grounding={"v1::a": "yes"})
    def forbidden(*args, **kwargs):
        raise AssertionError("Lineage must consume the validated in-memory handoff")
    monkeypatch.setattr("builtins.open", forbidden)
    monkeypatch.setattr(Path, "open", forbidden)
    monkeypatch.setattr(socket, "socket", forbidden)
    monkeypatch.setattr("recursive_integrity_toolkit.io.validation.validate_bundle", forbidden)
    result = _analyze(validation)
    rendered = repr(result)
    assert "Private ancestry fixture" not in rendered
    assert "secret-missing-parent" not in rendered
    assert str(tmp_path) not in rendered
    assert all(message.file_path is None for message in result.messages)


def test_validation_remains_input_only_after_ancestry_is_implemented(tmp_path, monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("Input validation must never dispatch ancestry")
    monkeypatch.setattr(ancestry, "analyze_lineage", forbidden)
    validation = _validation(tmp_path, {"v2::a": [], "v2::b": ["v2::a"]})
    assert validation.parent_validation is not None


@pytest.mark.parametrize("mutation", ["missing_batch", "duplicate_record", "changed_parent_counter"])
def test_forged_validation_handoff_cannot_certify_ancestry(tmp_path, mutation):
    validation = _validation(tmp_path, {"v1::a": [], "v2::child": ["v1::a"]},
                             grounding={"v1::a": "yes"})
    if mutation == "missing_batch":
        validation = replace(validation, parent_validation=None)
    elif mutation == "duplicate_record":
        validation = replace(validation, records=validation.records + (validation.records[0],))
    else:
        batch = validation.parent_validation
        assessments = tuple(replace(item, resolved_reference_count=0)
                            if str(item.child_key) == "v2::child" else item for item in batch.assessments)
        validation = replace(validation, parent_validation=replace(batch, assessments=assessments))
    with pytest.raises(CanonicalValidationError):
        _analyze(validation)


def test_fatal_input_diagnostic_cannot_be_hidden_by_complete_target_roots(tmp_path):
    validation = _validation(tmp_path, {"v2::anchor": []}, grounding={"v2::anchor": "yes"})
    fatal = ValidationMessage("E_SCHEMA_TYPE", ValidationSeverity.FATAL, "Malformed declared input")
    result = _analyze(replace(validation, validation_messages=validation.validation_messages + (fatal,)))
    assert result.execution_status is ExecutionStatus.FAILED
    assert result.execution_reason_codes == ("INVALID_LINEAGE_INPUT",)
    assert result.grounded_record_count == 1
    assert _by_key(result)["v2::anchor"].external_root_keys == frozenset({_key("v2::anchor")})
    assert any(message.severity is ValidationSeverity.FATAL for message in result.messages)


def test_typed_result_rejects_promoting_unknown_partition_to_completed(tmp_path):
    result = _analyze(_validation(tmp_path, {"v2::unknown": []}, grounding={"v2::unknown": "unknown"}))
    with pytest.raises(CanonicalValidationError):
        replace(result, execution_status=ExecutionStatus.COMPLETED, execution_reason_codes=())


@pytest.mark.parametrize("field", ["resolved_lineage_coverage", "external_ancestry_coverage", "resolved_parent_edge_coverage"])
def test_typed_result_rejects_boolean_coverage_equal_to_one(tmp_path, field):
    result = _analyze(_validation(tmp_path, {"v2::anchor": []}, grounding={"v2::anchor": "yes"}))
    with pytest.raises(CanonicalValidationError):
        replace(result, **{field: True})


def test_typed_result_rejects_unloaded_root_identity_and_incomplete_complete_record(tmp_path):
    result = _analyze(_validation(tmp_path, {"v2::anchor": []}, grounding={"v2::anchor": "yes"}))
    with pytest.raises(CanonicalValidationError):
        replace(result.records[0], lineage_depth=None, depth_reason_codes=("PARENT_DECLARATION_UNAVAILABLE",))
    forged_record = replace(result.records[0], external_root_keys=frozenset({_key("v1::unloaded")}))
    with pytest.raises(CanonicalValidationError):
        replace(result, records=(forged_record,))


def test_typed_result_preserves_disconnected_cycle_error(tmp_path):
    result = _analyze(_validation(tmp_path, {
        "v1::a": ["v1::b"], "v1::b": ["v1::a"], "v2::anchor": [],
    }, grounding={"v2::anchor": "yes"}))
    assert result.execution_status is ExecutionStatus.PARTIAL
    with pytest.raises(CanonicalValidationError):
        replace(result, messages=tuple(message for message in result.messages if message.code != "E_LINEAGE_CYCLE"),
                execution_status=ExecutionStatus.COMPLETED, execution_reason_codes=())
