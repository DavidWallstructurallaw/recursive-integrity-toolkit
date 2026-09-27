"""Actual-primary adapters preserve shared selected evidence and legacy values."""
from dataclasses import replace

import pytest

from recursive_integrity_toolkit.errors import CanonicalValidationError
from recursive_integrity_toolkit.lineage import ancestry
from recursive_integrity_toolkit.lineage.graph import LineageLimits
from recursive_integrity_toolkit.metrics.bounds import lineage_closure_exposure
from test_longitudinal_analysis import _select
from test_longitudinal_fixture_inputs import _load_case
from test_longitudinal_selection import _case


def _inputs(tmp_path, name="lineage_complete"):
    tmp_path.mkdir(parents=True, exist_ok=True)
    case = _case(name)
    validation = _load_case(case, tmp_path)
    return case, validation, _select(case, validation)


@pytest.mark.parametrize("name", ["lineage_complete", "lineage_partial", "lineage_zero_grounded"])
def test_primary_adapter_preserves_legacy_scientific_results(tmp_path, name):
    _, validation, selection = _inputs(tmp_path, name)
    expected = ancestry.analyze_lineage(validation, target_dataset_version=selection.primary_version)
    shared = ancestry.analyze_selected_lineage(validation, selection=selection)
    actual = ancestry.primary_lineage_from_selected(validation, selection=selection, result=shared)
    primary = next(target for target in shared.targets
                   if target.scope.target_dataset_version == selection.primary_version)
    assert actual == expected
    assert actual.scope == shared.shared_graph.scope
    assert actual.cycles is shared.shared_cycles
    assert actual.records is primary.records
    assert actual.root_contributions is primary.root_contributions
    for left, right in zip(actual.records, primary.records, strict=True):
        assert left.external_root_keys is right.external_root_keys
    assert actual.input_signature == ancestry._lineage_input_signature(validation)
    assert actual.input_signature != shared.input_signature
    assert lineage_closure_exposure(actual) == lineage_closure_exposure(expected)
    assert ancestry.SharedAncestryDependence(actual) == ancestry.SharedAncestryDependence(expected)


def test_primary_adapter_runs_no_graph_cycle_or_root_algorithm(tmp_path, monkeypatch):
    _, validation, selection = _inputs(tmp_path)
    shared = ancestry.analyze_selected_lineage(validation, selection=selection)

    def forbidden(*args, **kwargs):
        pytest.fail("primary handoff reran a lineage algorithm")

    for name in ("analyze_lineage", "analyze_selected_lineage", "build_lineage_graph",
                 "analyze_cycles", "_resolve_roots"):
        monkeypatch.setattr(ancestry, name, forbidden)
    actual = ancestry.primary_lineage_from_selected(validation, selection=selection, result=shared)
    assert actual.scope.target_dataset_version == selection.primary_version
    assert actual.cycles is shared.shared_cycles


@pytest.mark.parametrize("limit", ["max_root_memberships", "max_root_union_visits"])
def test_primary_adapter_preserves_global_root_exhaustion(tmp_path, limit):
    _, validation, selection = _inputs(tmp_path)
    limits = replace(LineageLimits(), **{limit: 1})
    expected = ancestry.analyze_lineage(validation, target_dataset_version=selection.primary_version,
                                       limits=limits)
    shared = ancestry.analyze_selected_lineage(validation, selection=selection, limits=limits)
    actual = ancestry.primary_lineage_from_selected(validation, selection=selection, result=shared)
    assert actual == expected
    assert actual.records is actual.root_contributions is None
    assert actual.ancestry_concentration_hhi is None
    assert actual.resource_usage.exhausted_limit == limit
    assert actual.cycles is shared.shared_cycles
    assert actual.resolved_parent_reference_count == actual.scope.target_record_count
    assert lineage_closure_exposure(actual).lower_bound is None


def test_primary_adapter_rejects_changed_input_with_identical_keys(tmp_path):
    case, validation, selection = _inputs(tmp_path / "original")
    shared = ancestry.analyze_selected_lineage(validation, selection=selection)
    case["provenance"][-1]["parent_ids"] = []
    (tmp_path / "changed").mkdir()
    changed = _load_case(case, tmp_path / "changed")
    with pytest.raises(CanonicalValidationError):
        ancestry.primary_lineage_from_selected(changed, selection=selection, result=shared)


@pytest.mark.parametrize("name", ["primary_version", "input_signature"])
def test_primary_adapter_revalidates_selection_binding(tmp_path, name):
    _, validation, selection = _inputs(tmp_path)
    shared = ancestry.analyze_selected_lineage(validation, selection=selection)
    object.__setattr__(selection, name, selection.selected_order[0] if name == "primary_version" else "0" * 64)
    with pytest.raises(CanonicalValidationError):
        ancestry.primary_lineage_from_selected(validation, selection=selection, result=shared)


def test_primary_adapter_rejects_a_target_summary_as_shared_result(tmp_path):
    _, validation, selection = _inputs(tmp_path)
    shared = ancestry.analyze_selected_lineage(validation, selection=selection)
    with pytest.raises(CanonicalValidationError):
        ancestry.primary_lineage_from_selected(validation, selection=selection, result=shared.targets[0])


def test_primary_adapter_rejects_changed_selected_target_values(tmp_path):
    _, validation, selection = _inputs(tmp_path)
    shared = ancestry.analyze_selected_lineage(validation, selection=selection)
    primary = next(target for target in shared.targets
                   if target.scope.target_dataset_version == selection.primary_version)
    object.__setattr__(primary, "distinct_external_root_count", 99)
    with pytest.raises(CanonicalValidationError):
        ancestry.primary_lineage_from_selected(validation, selection=selection, result=shared)
