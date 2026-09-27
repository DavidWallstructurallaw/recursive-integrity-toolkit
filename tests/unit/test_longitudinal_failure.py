"""Failed selection preserves independent evidence without inferred chronology."""
from dataclasses import replace

import pytest

from recursive_integrity_toolkit.errors import CanonicalValidationError
from recursive_integrity_toolkit.metrics import longitudinal as module
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
