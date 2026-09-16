"""Phase 1 placeholder for PR-005.

Planned scope:
    Future source-share tests are deferred to Phase 3.

Current Phase 1 scope:
    Verify the approved owner ID and confirm that the target module remains a
    docstring-only, import-safe placeholder.

Limits:
    No mathematical metric, data loading, graph operation, or report result is tested.
"""


def test_PR005_source_shares_owner_and_placeholder(owner_checker, placeholder_checker):
    owner_checker("metrics/provenance.py", "PR-005")
    placeholder_checker("metrics/provenance.py")


# Step 5 tests only declared-field separation. No source counts or shares.
def test_PR005_join_keeps_crossed_declarations_without_inference(repo_root):
    from recursive_integrity_toolkit.io.loaders import load_table
    from recursive_integrity_toolkit.io.normalization import normalize_row, normalize_table
    from recursive_integrity_toolkit.io.validation import join_provenance
    from recursive_integrity_toolkit.models import FileRole, InputSource
    path = repo_root / "tests/fixtures/provenance_unknown/step5_crossed.jsonl"
    before = path.read_bytes()
    provenance = normalize_table(load_table(InputSource(FileRole.PROVENANCE_MANIFEST, path)))
    records = tuple(normalize_row({"dataset_version": "v1", "record_id": row.record_key.record_id,
                                   "content": "synthetic"}, kind="records") for row in provenance)
    result = join_provenance(records, provenance)
    for match, declared in zip(result.matches, provenance):
        for field in ("source_type", "external_grounding", "human_reviewed", "provenance_confidence"):
            assert match.provenance.values[field] == declared.values[field]
    assert result.matches[1].provenance.values["source_type"] == "human"
    assert result.matches[1].provenance.values["external_grounding"] == "no"
    assert result.matches[3].provenance.values["source_type"] == "synthetic"
    assert result.matches[3].provenance.values["external_grounding"] == "yes"
    assert not hasattr(result, "source_type_shares") and not hasattr(result, "source_type_counts")
    assert path.read_bytes() == before
