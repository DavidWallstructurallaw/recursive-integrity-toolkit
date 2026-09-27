"""Shared input work preserves owner joins, diagnostics and consumer checks."""
from dataclasses import replace

import pytest

from recursive_integrity_toolkit.errors import ErrorCode, WarningCode
from recursive_integrity_toolkit.io.validation import join_provenance
from recursive_integrity_toolkit.metrics import longitudinal as series
from recursive_integrity_toolkit.models import ValidationSeverity
from test_longitudinal_fixture_inputs import _load_case
from test_longitudinal_selection import _case, _declarations


@pytest.mark.parametrize("case_name", ["observed_three_version", "lineage_complete", "identified_empty_later"])
@pytest.mark.parametrize("strict", [False, True])
def test_shared_projection_is_exactly_equal_to_independent_owner_join(tmp_path, case_name, strict):
    case = _case(case_name)
    # Exercise required-field errors outside each local scope, missing rows,
    # promoted warnings, unknown grounding and detached metadata conflicts.
    first = case["provenance"][0]
    first.pop("source_type")
    first.update(provenance_confidence="estimated", external_grounding="unknown", batch_id="manifest-batch")
    matching = next(row for row in case["records"] if
        (row["dataset_version"], row["record_id"]) == (first["dataset_version"], first["record_id"]))
    matching["batch_id"] = "records-batch"
    case["provenance"].pop()
    validation = _load_case(case, tmp_path)
    promoted = tuple(code.value for code in (WarningCode.PROVENANCE_MISSING_ROW,
        WarningCode.GROUNDING_UNKNOWN, WarningCode.PROVENANCE_ESTIMATED)) if strict else ()
    full = join_provenance(validation.records, validation.provenance,
        strict_mode=strict, strict_warning_codes=promoted)
    validation = replace(validation, provenance_join=full)
    versions = tuple(case["representations"])
    grouped = series._snapshot_inputs(validation, versions)
    for version in versions:
        rows, joined = grouped[version]
        assert rows == tuple(row for row in validation.records if row.record_key.dataset_version == version)
        if not rows:
            assert joined is None
            continue
        expected = join_provenance(validation.records, validation.provenance, dataset_versions=(version,),
            strict_mode=strict, strict_warning_codes=promoted)
        assert joined == expected
        assert any(message.code == ErrorCode.SCHEMA_REQUIRED_FIELD.value for message in joined.messages)
        for message in joined.messages:
            if message.code != ErrorCode.SCHEMA_REQUIRED_FIELD.value:
                assert message.record_key.dataset_version == version
                assert message.severity is (ValidationSeverity.ERROR if strict else ValidationSeverity.WARNING)
        # Reusing one freshly checked owner join retains its immutable matches.
        reused = series._snapshot_inputs(validation, versions, joined=full)[version][1]
        assert reused == expected
        assert all(match is original for match, original in zip(reused.matches,
            (match for match in full.matches if match.record_key.dataset_version == version)))


def _many_versions(count):
    case = _case()
    versions = tuple(f"version-{index}" for index in range(count))
    record, provenance = case["records"][0], case["provenance"][0]
    declaration = next(iter(case["representations"].values()))
    case.update(selected_versions=list(versions), context_versions=[],
        order_document={"version_order": list(versions)},
        records=[{**record, "dataset_version": version, "record_id": "r"} for version in versions],
        provenance=[{**provenance, "dataset_version": version, "record_id": "r", "parent_ids": []}
                    for version in versions],
        representations={version: declaration for version in versions})
    return case


@pytest.mark.parametrize("count", [2, 12])
def test_full_join_work_does_not_grow_per_snapshot_at_series_boundaries(tmp_path, monkeypatch, count):
    case = _many_versions(count)
    validation = _load_case(case, tmp_path)
    selection = series.select_longitudinal_versions(validation, declarations=_declarations(case), baseline="first")
    calls = []
    def counted(records, provenance, **kwargs):
        calls.append((len(records), kwargs.get("dataset_versions")))
        return join_provenance(records, provenance, **kwargs)
    monkeypatch.setattr(series, "join_provenance", counted)
    result = series.analyze_longitudinal(validation, selection=selection)
    series.validate_longitudinal_result(validation, result=result)
    # Each public boundary checks selection and prepares one fresh full join;
    # no extra full-input join is performed for each individual snapshot.
    assert calls == [(count, None)] * 4
    assert len(result.comparisons) == 2 * count - 3
    assert all(snapshot.provenance.analyzed_record_count.value == 1 for snapshot in result.snapshots)


def test_stale_retained_join_cannot_replace_fresh_source_validation(tmp_path):
    case = _case()
    validation = _load_case(case, tmp_path)
    declarations = _declarations(case)
    source = series.analyze_longitudinal(validation,
        selection=series.select_longitudinal_versions(validation, declarations=declarations))
    stale = replace(validation, provenance_join=replace(validation.provenance_join, matches=(), messages=()))
    result = series.analyze_longitudinal(stale,
        selection=series.select_longitudinal_versions(stale, declarations=declarations))
    assert result == source
    series.validate_longitudinal_result(stale, result=result)
    for snapshot in result.snapshots:
        series.validate_longitudinal_snapshot(stale, snapshot)


def test_standalone_explicit_empty_snapshot_keeps_its_no_provenance_contract(tmp_path):
    case = _case("identified_empty_later")
    validation = _load_case(case, tmp_path)
    source = series.analyze_longitudinal(validation,
        selection=series.select_longitudinal_versions(validation, declarations=_declarations(case)))
    empty_input = replace(validation, records=(), provenance=None)
    series.validate_longitudinal_snapshot(empty_input, source.snapshots[-1])
