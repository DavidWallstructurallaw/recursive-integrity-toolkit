"""Phase 2 Step 1 contract tests for PR-011 capability matrix vocabulary."""

import pytest

from recursive_integrity_toolkit.models import Capability, CapabilityKey, CapabilityStatus, ObservabilityAssessment, ValidationCoverage


EXPECTED_KEYS = {"ingestion", "content_diagnostics", "provenance", "lineage", "dataset_longitudinal", "model_longitudinal", "intervention_simulation"}


def test_PR011_capability_keys_are_exact() -> None:
    assert {key.value for key in CapabilityKey} == EXPECTED_KEYS


def test_PR011_capability_status_values_are_exact() -> None:
    assert {status.value for status in CapabilityStatus} == {"available", "partial", "unavailable", "experimental"}


def test_PR011_coverage_denominator_is_named() -> None:
    coverage = ValidationCoverage(3, 4, "requested records")
    capability = Capability(CapabilityStatus.PARTIAL, coverage=coverage)
    assert capability.coverage is not None
    assert capability.coverage.denominator_name == "requested records"


def test_PR011_complete_matrix_is_required() -> None:
    with pytest.raises(ValueError):
        ObservabilityAssessment(0, {CapabilityKey.INGESTION: Capability(CapabilityStatus.AVAILABLE)})
