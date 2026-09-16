"""Phase 2 Step 1 contract tests for PR-010 observability levels."""

import pytest

from recursive_integrity_toolkit.models import Capability, CapabilityKey, CapabilityStatus, ObservabilityAssessment


def _matrix() -> dict[CapabilityKey, Capability]:
    return {key: Capability(status=CapabilityStatus.UNAVAILABLE, reason_codes=("R_NOT_CLASSIFIED",)) for key in CapabilityKey}


def test_PR010_level_range_contract() -> None:
    for level in range(6):
        assert ObservabilityAssessment(level, _matrix()).maximum_level == level


@pytest.mark.parametrize("level", [-1, 6])
def test_PR010_out_of_range_level_rejected(level: int) -> None:
    with pytest.raises(ValueError):
        ObservabilityAssessment(level, _matrix())


def test_PR010_boolean_is_not_an_observability_level() -> None:
    with pytest.raises(TypeError):
        ObservabilityAssessment(True, _matrix())
