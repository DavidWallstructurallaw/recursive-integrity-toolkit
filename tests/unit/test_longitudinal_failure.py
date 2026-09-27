"""Failed selection preserves independent evidence without inferred chronology."""
from dataclasses import replace

import pytest

from recursive_integrity_toolkit.errors import CanonicalValidationError
from recursive_integrity_toolkit.metrics import longitudinal as module
from recursive_integrity_toolkit.models import FileRole, ValidationMessage, ValidationSeverity
from recursive_integrity_toolkit.result import ExecutionStatus
from test_longitudinal_fixture_inputs import _load_case
from test_longitudinal_selection import _case, _declarations


def test_missing_order_retains_independent_snapshots(tmp_path):
    case = _case("missing_order")
    bundle = _load_case(case, tmp_path)
    result = module.analyze_longitudinal_failure(bundle, declarations=_declarations(case), lineage=True)
    assert result.execution_status is ExecutionStatus.FAILED
    assert result.reason_codes == ("R_LONGITUDINAL_SELECTION_INVALID", "E_VERSION_ORDER_CONFLICT")
    assert [s.record_count.value for s in result.snapshots] == [1, 1]
    assert all(s.distribution is not None and s.provenance is not None for s in result.snapshots)
    assert all(s.family_statuses[-1].execution_status is ExecutionStatus.FAILED for s in result.snapshots)
    assert module.validate_longitudinal_failure(bundle, result=result) is result


def test_failed_admission_never_computes_snapshot_prefix(tmp_path, monkeypatch):
    case = _case()
    bundle = _load_case(case, tmp_path)
    def forbidden(*args, **kwargs):
        raise AssertionError("admission must precede every snapshot calculation")
    monkeypatch.setattr(module, "_snapshot_distribution", forbidden)
    result = module.analyze_longitudinal_failure(bundle, declarations=_declarations(case), max_versions=2)
    assert result.snapshots == ()
    assert result.selected_version_count == 3
    assert result.reason_codes == ("R_LONGITUDINAL_RESOURCE_LIMIT", "E_LONGITUDINAL_RESOURCE_LIMIT_EXCEEDED")
    module.validate_longitudinal_failure(bundle, result=result)


def test_successful_selection_cannot_claim_failure(tmp_path):
    case = _case()
    bundle = _load_case(case, tmp_path)
    with pytest.raises(CanonicalValidationError, match="valid selection"):
        module.analyze_longitudinal_failure(bundle, declarations=_declarations(case))


def test_failure_consumer_rejects_dropped_snapshot_and_mutated_reason(tmp_path):
    case = _case("missing_order")
    bundle = _load_case(case, tmp_path)
    result = module.analyze_longitudinal_failure(bundle, declarations=_declarations(case))
    for forged in (replace(result, snapshots=result.snapshots[:-1]),
                   replace(result, reason_codes=("R_LONGITUDINAL_RESOURCE_LIMIT",))):
        with pytest.raises(CanonicalValidationError):
            module.validate_longitudinal_failure(bundle, result=forged)


def test_failure_validation_runs_no_calculation(tmp_path, monkeypatch):
    case = _case("missing_order")
    bundle = _load_case(case, tmp_path)
    result = module.analyze_longitudinal_failure(bundle, declarations=_declarations(case))
    def forbidden(*args, **kwargs):
        raise AssertionError("consumer cannot run an analytical kernel")
    for name in ("_snapshot_distribution", "calculate_state_distribution", "summarize_provenance",
                 "direct_closure_exposure", "compare_support", "analyze_longitudinal"):
        monkeypatch.setattr(module, name, forbidden)
    module.validate_longitudinal_failure(bundle, result=result)


def _retained_order_error(bundle):
    error = ValidationMessage("E_VERSION_ORDER_CONFLICT", ValidationSeverity.ERROR,
        "original ordering sources disagree", FileRole.VERSION_ORDER, field="version_order")
    return replace(bundle, validation_messages=(*bundle.validation_messages, error)), error


def test_retained_original_chronology_error_survives_fallback(tmp_path):
    case = _case("missing_order")
    bundle, error = _retained_order_error(_load_case(case, tmp_path))
    result = module.analyze_longitudinal_failure(bundle, declarations=_declarations(case),
        selection_errors=(error,))
    assert result.messages[0] is error
    assert len(result.snapshots) == 2
    assert module.validate_longitudinal_failure(bundle, result=result) is result
    for altered in (replace(bundle, validation_messages=()),
                    replace(bundle, inventory=tuple(replace(entry, sha256="0" * 64)
                        for entry in bundle.inventory))):
        with pytest.raises(CanonicalValidationError):
            module.validate_longitudinal_failure(altered, result=result)


def test_retained_order_rejection_cannot_be_erased_by_usable_fallback_order(tmp_path):
    case = _case()
    bundle, error = _retained_order_error(_load_case(case, tmp_path))
    result = module.analyze_longitudinal_failure(bundle, declarations=_declarations(case),
        selection_errors=(error,))
    assert result.reason_codes == ("R_LONGITUDINAL_SELECTION_INVALID", "E_VERSION_ORDER_CONFLICT")
    assert len(result.snapshots) == 3
    module.validate_longitudinal_failure(bundle, result=result)


@pytest.mark.parametrize("change", ["absent", "warning", "role", "field", "code", "location", "duplicate"])
def test_retained_order_errors_require_exact_typed_input_evidence(tmp_path, change):
    case = _case()
    bundle, error = _retained_order_error(_load_case(case, tmp_path))
    if change == "absent":
        bundle = replace(bundle, validation_messages=())
    elif change != "duplicate":
        changes = {"warning": {"severity": ValidationSeverity.WARNING},
            "role": {"file_role": FileRole.RECORDS_PRIMARY}, "field": {"field": "content"},
            "code": {"code": "E_CONFIG_INVALID"}, "location": {"row_number": 1}}
        error = replace(error, **changes[change])
        bundle = replace(bundle, validation_messages=(*bundle.validation_messages, error))
    with pytest.raises(CanonicalValidationError):
        module.analyze_longitudinal_failure(bundle, declarations=_declarations(case),
            selection_errors=(error, error) if change == "duplicate" else (error,))


def test_empty_comparison_file_retains_loaded_independent_snapshots(tmp_path):
    case = _case()
    bundle = _load_case(case, tmp_path)
    sample = next(entry for entry in bundle.inventory if entry.role is FileRole.RECORDS_COMPARE)
    empty = replace(sample, path=tmp_path / "empty.jsonl", row_count=0, size_bytes=0)
    error = ValidationMessage("E_SCHEMA_TYPE", ValidationSeverity.ERROR,
        "selected file has no version", FileRole.RECORDS_COMPARE, str(empty.path), "dataset_version")
    bundle = replace(bundle, inventory=(*bundle.inventory, empty),
        validation_messages=(*bundle.validation_messages, error))
    result = module.analyze_longitudinal_failure(bundle, declarations=_declarations(case),
        selection_errors=(error,))
    assert len(result.snapshots) == 3
    assert result.selected_version_count == 3
    module.validate_longitudinal_failure(bundle, result=result)


@pytest.mark.parametrize("change", ["valid_file", "missing_file", "context", "wrong_field"])
def test_file_rejection_requires_actual_invalid_selected_file(tmp_path, change):
    case = _case()
    bundle = _load_case(case, tmp_path)
    entry = next(entry for entry in bundle.inventory if entry.role is FileRole.RECORDS_COMPARE)
    error = ValidationMessage("E_SCHEMA_TYPE", ValidationSeverity.ERROR,
        "selected file has invalid version count", FileRole.RECORDS_COMPARE, str(entry.path), "dataset_version")
    if change == "missing_file":
        error = replace(error, file_path=str(tmp_path / "not-loaded.jsonl"))
    elif change == "context":
        error = replace(error, file_role=FileRole.LINEAGE_CONTEXT)
    elif change == "wrong_field":
        error = replace(error, field="record_id")
    bundle = replace(bundle, validation_messages=(*bundle.validation_messages, error))
    with pytest.raises(CanonicalValidationError):
        module.analyze_longitudinal_failure(bundle, declarations=_declarations(case), selection_errors=(error,))
