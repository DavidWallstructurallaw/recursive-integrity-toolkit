"""Phase 2 Step 1 contract tests for PR-001 canonical record identity."""

import pytest

from recursive_integrity_toolkit.models import RecordKey


def test_PR001_composite_key_serialization() -> None:
    key = RecordKey(dataset_version="v1", record_id="row_001")
    assert str(key) == "v1::row_001"
    assert RecordKey.parse(str(key)) == key


def test_PR001_same_record_id_allowed_across_versions() -> None:
    assert RecordKey("v1", "row_001") != RecordKey("v2", "row_001")


@pytest.mark.parametrize(
    "dataset_version,record_id",
    [("", "row"), ("v1", ""), (" v1", "row"), ("v1", "row "), ("v::1", "row"), ("v1", "row::1"), ("v1\x00", "row"), ("v1", "row\x00")],
)
def test_PR001_invalid_identifier_is_rejected(dataset_version: str, record_id: str) -> None:
    with pytest.raises((TypeError, ValueError)):
        RecordKey(dataset_version, record_id)


def test_PR001_reserved_separator_parse_is_unambiguous() -> None:
    with pytest.raises(ValueError):
        RecordKey.parse("v1::row::extra")
