"""Load Phase 5 fixtures through current input validation only.

Future lineage oracle values in the fixture documents are not executed here.
These checks detect malformed acceptance inputs, loss of parent declarations,
and incorrect reference counts before the graph implementation consumes them.
"""

import json
from pathlib import Path

import pytest

from recursive_integrity_toolkit.io.validation import validate_bundle
from recursive_integrity_toolkit.models import (
    AuditBundle,
    FileRole,
    InputSource,
    ParentResolutionStatus,
    ValidationSeverity,
)


FIXTURE_ROOT = Path(__file__).resolve().parents[1] / "fixtures"
CASES = [
    case
    for directory in ("lineage_complete", "lineage_multi_root", "lineage_cycles")
    for case in json.loads((FIXTURE_ROOT / directory / "cases.json").read_text())["cases"]
]


def _write_rows(path, rows):
    path.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")


@pytest.mark.parametrize("case", CASES, ids=lambda case: case["case_id"])
def test_lineage_acceptance_inputs_preserve_declared_evidence(case, tmp_path):
    target_keys = set(case["target_record_keys"])
    primary = [
        row for row in case["records"]
        if f"{row['dataset_version']}::{row['record_id']}" in target_keys
    ]
    context = [row for row in case["records"] if row not in primary]
    if not primary:
        # Empty target is a future in-memory selection over loaded context.
        # This does not claim support for an empty current CLI primary file.
        primary, context = context, []
    primary_path = tmp_path / "records.jsonl"
    _write_rows(primary_path, primary)
    sources = [InputSource(FileRole.RECORDS_PRIMARY, primary_path)]
    if context:
        context_path = tmp_path / "context.jsonl"
        _write_rows(context_path, context)
        # The future context role is not implemented in Step 1. The current
        # comparison role loads the same canonical rows for input checks only.
        sources.append(InputSource(FileRole.RECORDS_COMPARE, context_path))
    provenance_path = tmp_path / "provenance.jsonl"
    _write_rows(provenance_path, case["provenance"])
    sources.append(InputSource(FileRole.PROVENANCE_MANIFEST, provenance_path))
    order_path = tmp_path / "version_order.json"
    order_path.write_text(json.dumps({"version_order": case["version_order"]}), encoding="utf-8")
    sources.append(InputSource(FileRole.VERSION_ORDER, order_path))
    result = validate_bundle(AuditBundle(tuple(sources)))

    assert {str(row.record_key) for row in result.records} == {
        f"{row['dataset_version']}::{row['record_id']}" for row in case["records"]
    }
    expected = case["expected_input"]
    error_codes = {
        message.code for message in result.validation_messages
        if message.severity in (ValidationSeverity.ERROR, ValidationSeverity.FATAL)
    }
    assert error_codes == set(expected["error_codes"])
    warning_codes = {
        message.code for message in result.validation_messages
        if message.severity is ValidationSeverity.WARNING
    }
    assert set(expected["required_warning_codes"]) <= warning_codes

    if "target_declared_references" in expected:
        assert result.generation is not None
        parents = {str(item.child_key): item for item in result.generation.parents}
        references = [ref for key in target_keys for ref in parents[key].references]
        assert sum(len(ref.source_references) for ref in references) == expected[
            "target_declared_references"
        ]
        assert sum(
            len(ref.source_references) for ref in references
            if ref.resolution_status is ParentResolutionStatus.RESOLVED
        ) == expected["target_resolved_references"]
    provenance = {str(row.record_key): row for row in result.provenance}
    for key, state in expected.get("parent_field_states", {}).items():
        # Normalization materializes absent parent_ids as null in values, while
        # field_states retains the original distinction for the graph adapter.
        assert provenance[key].field_states["parent_ids"] == state
