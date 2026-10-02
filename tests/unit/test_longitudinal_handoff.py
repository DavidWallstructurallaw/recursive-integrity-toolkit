"""Step 6 consumer validation checks supplied evidence without analytical dispatch."""
from copy import copy
from dataclasses import replace
from types import MappingProxyType

import pytest

from recursive_integrity_toolkit.config import RepresentationConfig
from recursive_integrity_toolkit.errors import CanonicalValidationError
from recursive_integrity_toolkit.lineage.graph import LineageLimits
from recursive_integrity_toolkit.metrics import longitudinal as series
from recursive_integrity_toolkit.models import ContentMode, TailSelectionOptions
from test_longitudinal_analysis import _select
from test_longitudinal_fixture_inputs import CASES, LINEAGE_CASES, _load_case
from test_longitudinal_selection import _case, _declarations, _mapping


def _input(tmp_path, name="observed_three_version", **kwargs):
    case = _case(name)
    validation = _load_case(case, tmp_path)
    result = series.analyze_longitudinal(validation, selection=_select(case, validation), **kwargs)
    return validation, result


def _forge(original, **changes):
    """Model an arbitrary caller-created frozen value without relying on constructors."""
    value = copy(original)
    for name, changed in changes.items():
        object.__setattr__(value, name, changed)
    return value


def _snapshot(result, snapshot):
    return _forge(result, snapshots=(snapshot, *result.snapshots[1:]))


@pytest.mark.parametrize("case", [case for case in CASES if case["case_id"] != "missing_order"],
                         ids=lambda case: case["case_id"])
@pytest.mark.parametrize("tail", [False, True])
def test_frozen_series_handoffs_validate(case, tail, tmp_path):
    validation = _load_case(case, tmp_path)
    result = series.analyze_longitudinal(validation, selection=_select(case, validation),
        tail_options=TailSelectionOptions("singleton_count") if tail else None)
    assert series.validate_longitudinal_result(validation, result=result) is None


@pytest.mark.parametrize("case", LINEAGE_CASES, ids=lambda case: case["case_id"])
@pytest.mark.parametrize("limits", [None, LineageLimits(max_nodes=1), LineageLimits(max_edges=1),
    LineageLimits(max_root_memberships=1), LineageLimits(max_root_union_visits=1)])
def test_shared_and_exhausted_lineage_handoffs_validate(case, limits, tmp_path):
    validation = _load_case(case, tmp_path)
    result = series.analyze_longitudinal(validation, selection=_select(case, validation),
        lineage=True, lineage_limits=limits)
    series.validate_longitudinal_result(validation, result=result)


@pytest.mark.parametrize("rule", [TailSelectionOptions("singleton_count"),
    TailSelectionOptions("count_at_or_below", count_threshold=2),
    TailSelectionOptions("frequency_at_or_below", frequency_threshold=0.5),
    TailSelectionOptions("state_list", state_ids=("A",))])
def test_tail_rule_arithmetic_and_unavailable_selection_validate(rule, tmp_path):
    validation, result = _input(tmp_path, tail_options=rule)
    series.validate_longitudinal_result(validation, result=result)


@pytest.mark.parametrize("mode", ["inline", "local_ref", "missing_column", "missing_cell", "collision"])
def test_assignment_availability_is_revalidated(mode, tmp_path):
    case = _case("observed_three_version")
    if mode == "missing_column":
        for row in case["records"]:
            if row["dataset_version"] == "v1":
                row.pop("topic", None)
    elif mode == "missing_cell":
        case["records"][0]["topic"] = None
    validation = _load_case(case, tmp_path)
    declarations = _declarations(case)
    if mode in ("inline", "local_ref"):
        declarations = tuple(replace(item, representation=RepresentationConfig(
            "exact", "content_hash", "content", "r1", "error", "exact_utf8_v1"),
            state_semantics="exact record form") for item in declarations)
        if mode == "local_ref":
            validation = replace(validation, content_mode=ContentMode.LOCAL_REF)
    elif mode == "missing_cell":
        declarations = tuple(replace(item, representation=replace(item.representation,
                             missing_value_policy="error")) for item in declarations)
    elif mode == "collision":
        declarations = tuple(replace(item, representation=replace(item.representation,
            missing_value_policy="explicit_missing_state"), missing_state_id="A") for item in declarations)
    result = series.analyze_longitudinal(validation,
        selection=_select(case, validation, declarations=declarations))
    series.validate_longitudinal_result(validation, result=result)


def test_incomplete_mapping_handoff_validates_without_silently_repairing(tmp_path):
    case = _case("directed_many_to_one")
    validation = _load_case(case, tmp_path)
    declarations = _declarations(case)
    mapping = _mapping(declarations, states={"red": "apple", "pear": "pear"})
    result = series.analyze_longitudinal(validation,
        selection=_select(case, validation, declarations=declarations, mappings=(mapping,)))
    assert result.comparisons[0].compatibility is None
    series.validate_longitudinal_result(validation, result=result)


def test_public_handoff_dispatches_no_analysis_assignment_graph_or_io(tmp_path, monkeypatch):
    import builtins
    from recursive_integrity_toolkit.lineage import ancestry, cycles, graph
    from recursive_integrity_toolkit.metrics import bounds, diversity, provenance, tail
    from recursive_integrity_toolkit.representations import content_hash, field

    validation, result = _input(tmp_path, "lineage_complete", lineage=True,
                               tail_options=TailSelectionOptions("singleton_count"))

    def forbidden(*args, **kwargs):
        pytest.fail("consumer dispatched a calculation or I/O entry point")

    for module, names in (
        (series, ("analyze_longitudinal", "_snapshot_distribution", "_pair_result", "_attach_lineage",
                  "calculate_state_distribution", "compare_support", "select_tail", "summarize_provenance",
                  "direct_closure_exposure", "lineage_closure_exposure", "assign_field_states", "assign_content_states")),
        (diversity, ("calculate_state_distribution", "compare_support", "distribution_from_counts")),
        (tail, ("select_tail", "one_step_extinction_probability")),
        (provenance, ("summarize_provenance", "classify_direct_grounding")),
        (bounds, ("direct_closure_exposure", "closure_exposure_bounds", "lineage_closure_exposure")),
        (field, ("assign_field_states",)), (content_hash, ("assign_content_states",)),
        (graph, ("build_lineage_graph",)), (cycles, ("analyze_cycles",)),
        (ancestry, ("analyze_lineage", "analyze_selected_lineage", "build_lineage_graph", "analyze_cycles", "_resolve_roots")),
        (builtins, ("open",)),
    ):
        for name in names:
            monkeypatch.setattr(module, name, forbidden)
    series.validate_longitudinal_result(validation, result=result)


@pytest.mark.parametrize("mutation", ["state_count", "frequency", "support", "diversity", "metadata",
    "count_type", "coverage", "selection_basis", "scope_id", "diagnostic"])
def test_forged_distribution_evidence_rejected_with_unchanged_signature(mutation, tmp_path):
    validation, result = _input(tmp_path)
    snapshot = result.snapshots[0]
    distribution, metric = snapshot.distribution, snapshot.distribution.unweighted
    if mutation in ("state_count", "frequency"):
        row = metric.states[0]
        row = replace(row, **({"state_count": row.state_count + 1} if mutation == "state_count" else
                              {"state_frequency": row.state_frequency / 2}))
        metric = replace(metric, states=(row, *metric.states[1:]))
    elif mutation == "support":
        metric = replace(metric, support=metric.support[:-1])
    elif mutation == "diversity":
        metric = replace(metric, gini_simpson_diversity=replace(metric.gini_simpson_diversity, value=0.0))
    elif mutation == "metadata":
        metric = replace(metric, frequency_metadata=replace(metric.frequency_metadata,
                         method="unchecked private declaration", owner_id="T6"))
    elif mutation == "count_type":
        snapshot = _forge(snapshot, record_count=_forge(snapshot.record_count, value=4.0))
    elif mutation == "coverage":
        distribution = replace(distribution, coverage=replace(distribution.coverage,
                                 denominator_name="different denominator"))
    elif mutation == "selection_basis":
        distribution = replace(distribution, selection_basis="inferred")
    elif mutation == "scope_id":
        snapshot = _forge(snapshot, scope=_forge(snapshot.scope,
            representation_scope=replace(snapshot.scope.representation_scope, scope_id="foreign-scope")))
    elif mutation == "diagnostic":
        snapshot = _forge(snapshot, messages=())
        # This fixture has no diagnostics in its first snapshot; inject one from another scope.
        snapshot = _forge(snapshot, messages=result.snapshots[1].messages)
    snapshot = _forge(snapshot, distribution=replace(distribution, unweighted=metric))
    forged = _snapshot(result, snapshot)
    assert forged.input_signature == result.input_signature
    with pytest.raises(CanonicalValidationError):
        series.validate_longitudinal_result(validation, result=forged)


@pytest.mark.parametrize("mutation", ["source_counts", "source_shares", "grounding_assignment",
    "grounding_count", "confidence", "coverage", "scalar_metadata", "bounds_confidence", "bounds_method"])
def test_forged_provenance_and_bound_handoffs_rejected(mutation, tmp_path):
    validation, result = _input(tmp_path)
    snapshot, provenance = result.snapshots[0], result.snapshots[0].provenance
    bounds = snapshot.direct_closure
    if mutation == "source_counts":
        provenance = replace(provenance, source=replace(provenance.source,
            counts=tuple((key, value + 1) for key, value in provenance.source.counts)))
    elif mutation == "source_shares":
        provenance = replace(provenance, source=replace(provenance.source,
            shares=tuple((key, 0.0) for key, value in provenance.source.shares)))
    elif mutation == "grounding_assignment":
        grounding = provenance.direct_grounding
        row = replace(grounding.assignments[0], classification="known_closed")
        provenance = replace(provenance, direct_grounding=replace(grounding,
                             assignments=(row, *grounding.assignments[1:])))
    elif mutation == "grounding_count":
        grounding = provenance.direct_grounding
        provenance = replace(provenance, direct_grounding=replace(grounding,
            known_open_count=replace(grounding.known_open_count, value=0)))
    elif mutation == "confidence":
        provenance = replace(provenance, confidence=replace(provenance.confidence,
            counts=tuple((key, 0) for key, value in provenance.confidence.counts)))
    elif mutation == "coverage":
        provenance = replace(provenance, grounding_field_coverage=replace(provenance.grounding_field_coverage,
                             numerator=0))
    elif mutation == "scalar_metadata":
        scalar = provenance.missing_provenance_share
        provenance = replace(provenance, missing_provenance_share=replace(scalar,
                             metadata=replace(scalar.metadata, assumptions=("unchecked text",))))
    elif mutation == "bounds_confidence":
        bounds = replace(bounds, confidence_counts=(("unknown", 4),))
    elif mutation == "bounds_method":
        bounds = replace(bounds, lower_bound=replace(bounds.lower_bound,
            metadata=replace(bounds.lower_bound.metadata, method="different numerical method")))
    with pytest.raises(CanonicalValidationError):
        series.validate_longitudinal_result(validation,
            result=_snapshot(result, _forge(snapshot, provenance=provenance, direct_closure=bounds)))


@pytest.mark.parametrize("mutation", ["state_set", "retention", "mapping_effect", "scalar_metadata",
    "original_endpoint", "delta_coverage", "tail_membership", "tail_ranking", "duplicate_pair", "wrong_order"])
def test_forged_pair_and_tail_handoffs_rejected(mutation, tmp_path):
    validation, result = _input(tmp_path, tail_options=TailSelectionOptions("singleton_count"))
    pair = result.comparisons[0]
    comparison = pair.support_comparison
    if mutation == "state_set":
        comparison = replace(comparison, extinct_states=())
    elif mutation == "retention":
        comparison = replace(comparison, support_retention_ratio=replace(comparison.support_retention_ratio, value=0.0))
    elif mutation == "mapping_effect":
        comparison = replace(comparison, mapping_effect=(("earlier", 999, 999), ("later", 999, 999)))
    elif mutation == "scalar_metadata":
        scalar = comparison.support_loss_count
        comparison = replace(comparison, support_loss_count=replace(scalar,
                             metadata=replace(scalar.metadata, owner_id="T6")))
    elif mutation == "original_endpoint":
        comparison = replace(comparison, original_earlier=comparison.original_later)
    elif mutation == "delta_coverage":
        delta = pair.deltas[1]
        pair = _forge(pair, deltas=(pair.deltas[0], _forge(delta,
            earlier_coverage=replace(delta.earlier_coverage, numerator=0)), *pair.deltas[2:]))
    elif mutation in ("tail_membership", "tail_ranking"):
        tail = pair.tail_disappearance
        earlier_tail = tail.earlier_tail
        if mutation == "tail_membership":
            earlier_tail = replace(earlier_tail, tail_membership=())
        else:
            earlier_tail = replace(earlier_tail, rarity_ranking=tuple(reversed(earlier_tail.rarity_ranking)))
        pair = _forge(pair, tail_disappearance=_forge(tail, earlier_tail=earlier_tail))
    pair = _forge(pair, support_comparison=comparison)
    comparisons = (pair, *result.comparisons[1:])
    if mutation == "duplicate_pair":
        comparisons = (pair, pair, *result.comparisons[2:])
    elif mutation == "wrong_order":
        comparisons = tuple(reversed(comparisons))
    with pytest.raises(CanonicalValidationError):
        series.validate_longitudinal_result(validation, result=_forge(result, comparisons=comparisons))


def test_self_consistent_forged_source_counts_cannot_use_original_signature(tmp_path):
    validation, result = _input(tmp_path)
    snapshot = result.snapshots[0]
    source = snapshot.provenance.source
    counts = dict(source.counts)
    counts["human"], counts["synthetic"] = counts["synthetic"], counts["human"]
    source = replace(source, counts=tuple(counts.items()),
                     shares=tuple((key, count / snapshot.record_count.value) for key, count in counts.items()))
    snapshot = replace(snapshot, provenance=replace(snapshot.provenance, source=source))
    snapshots = (snapshot, *result.snapshots[1:])
    by_version = {item.scope.dataset_version: item for item in snapshots}
    comparisons = tuple(series._pair_result(pair, by_version[pair.earlier_version], by_version[pair.later_version],
        result.selection.version_order, result.tail_options) for pair in result.selection.pairs)
    forged = replace(result, snapshots=snapshots, comparisons=comparisons)
    assert forged.input_signature == result.input_signature
    with pytest.raises(CanonicalValidationError, match="snapshot provenance"):
        series.validate_longitudinal_result(validation, result=forged)


def test_stale_same_id_record_input_rejected(tmp_path):
    validation, result = _input(tmp_path)
    row = validation.records[0]
    changed = replace(row, values=MappingProxyType({**row.values, "topic": "changed-state"}))
    validation = replace(validation, records=(changed, *validation.records[1:]))
    with pytest.raises(CanonicalValidationError):
        series.validate_longitudinal_result(validation, result=result)


def test_self_consistent_forged_state_table_cannot_use_original_signature(tmp_path):
    validation, result = _input(tmp_path)
    snapshot, metric = result.snapshots[0], result.snapshots[0].distribution.unweighted
    old_state = metric.states[0].state_id
    metric = replace(metric,
        states=tuple(sorted((replace(row, state_id="fabricated-state") if row.state_id == old_state else row
                             for row in metric.states), key=lambda row: row.state_id)),
        support=tuple(sorted("fabricated-state" if state == old_state else state for state in metric.support)))
    snapshot = replace(snapshot, distribution=replace(snapshot.distribution, unweighted=metric))
    snapshots = (snapshot, *result.snapshots[1:])
    by_version = {item.scope.dataset_version: item for item in snapshots}
    comparisons = tuple(series._pair_result(pair, by_version[pair.earlier_version], by_version[pair.later_version],
        result.selection.version_order, result.tail_options) for pair in result.selection.pairs)
    forged = replace(result, snapshots=snapshots, comparisons=comparisons)
    assert forged.input_signature == result.input_signature
    with pytest.raises(CanonicalValidationError, match="snapshot distribution"):
        series.validate_longitudinal_result(validation, result=forged)
