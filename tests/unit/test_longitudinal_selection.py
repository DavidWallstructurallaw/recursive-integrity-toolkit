"""Step 2 selection boundaries, independent fixture order and legacy isolation."""
from copy import deepcopy
from dataclasses import FrozenInstanceError, replace

import pytest

from recursive_integrity_toolkit.config import RepresentationConfig
from recursive_integrity_toolkit.errors import CanonicalValidationError, ErrorCode
from recursive_integrity_toolkit.io.validation import resolve_version_order
from recursive_integrity_toolkit.metrics.longitudinal import (
    LongitudinalMapping, SnapshotDeclaration, select_longitudinal_versions,
    validate_longitudinal_selection,
)
from recursive_integrity_toolkit.models import (
    CalculationReason, CalculationStatus, ContentMode, ExplicitPairContext,
    FileRole,
)
from recursive_integrity_toolkit.representations.compatibility import (
    StateMappingDeclaration, validate_representation_basis, validate_representation_compatibility,
)
from recursive_integrity_toolkit.representations.content_hash import (
    assign_content_states, select_content_representation,
)
from recursive_integrity_toolkit.representations.field import select_field_representation
from test_longitudinal_fixture_inputs import CASES, _load_case


def _case(name="observed_three_version"):
    return deepcopy(next(item for item in CASES if item["case_id"] == name))


def _declarations(case):
    loaded = {row["dataset_version"] for row in case["records"]}
    return tuple(SnapshotDeclaration(version, RepresentationConfig(**{
        key: value for key, value in declaration.items() if key != "state_semantics"
    }), declaration["state_semantics"], empty_scope=version not in loaded)
        for version, declaration in case["representations"].items())


def _descriptor(declaration):
    return select_field_representation((), dataset_versions=(declaration.dataset_version,),
        config=declaration.representation, missing_state_id=declaration.missing_state_id).descriptor


def _mapping(declarations, *, states=None, direction="earlier_to_later"):
    earlier, later = declarations[:2]
    source, target = (earlier, later) if direction == "earlier_to_later" else (later, earlier)
    return LongitudinalMapping(earlier.dataset_version, later.dataset_version,
        StateMappingDeclaration(direction, _descriptor(source), _descriptor(target),
            source.state_semantics, target.state_semantics,
            {"red": "apple", "green": "apple", "pear": "pear"} if states is None else states))


@pytest.fixture
def inputs(tmp_path):
    case = _case()
    return _load_case(case, tmp_path), _declarations(case)


@pytest.mark.parametrize("case", [case for case in CASES if case["case_id"] != "missing_order"],
                         ids=lambda case: case["case_id"])
@pytest.mark.parametrize("baseline", ["none", "first"])
def test_fixture_selection_populations_and_pair_schedule(case, tmp_path, baseline):
    validation = _load_case(case, tmp_path)
    declarations = _declarations(case)
    mappings = (_mapping(declarations),) if case["case_id"] == "directed_many_to_one" else ()
    selection = select_longitudinal_versions(validation, declarations=declarations,
                                             baseline=baseline, mappings=mappings)
    versions = tuple(case["selected_versions"])
    assert selection.selected_order == versions
    assert selection.selected_versions == tuple(sorted(versions))
    assert selection.context_versions == tuple(sorted(case["context_versions"]))
    assert selection.version_order.loaded_versions == validation.version_order.loaded_versions
    expected = {(versions[i - 1], versions[i]): ("adjacent",) for i in range(1, len(versions))}
    if baseline == "first":
        for version in versions[1:]:
            key = versions[0], version
            expected[key] = expected.get(key, ()) + ("baseline",)
    expected_order = sorted(expected, key=lambda pair: (versions.index(pair[1]), versions.index(pair[0])))
    assert [(pair.earlier_version, pair.later_version, pair.kinds) for pair in selection.pairs] == [
        (*pair, expected[pair]) for pair in expected_order]
    for snapshot in selection.snapshots:
        assert snapshot.representation_scope is None
        assert snapshot.population_scope.excluded_record_keys == ()
        assert snapshot.population_scope.included_record_keys == tuple(sorted(
            row.record_key for row in validation.records
            if row.record_key.dataset_version == snapshot.dataset_version))
    assert validate_longitudinal_selection(validation, selection) == selection


def test_incompatible_middle_retains_both_adjacent_gaps_and_valid_baseline(tmp_path):
    case = _case("incompatible_middle")
    validation = _load_case(case, tmp_path)
    selection = select_longitudinal_versions(validation, declarations=_declarations(case), baseline="first")
    assert len(selection.snapshots) == 3
    assert [pair.status for pair in selection.pairs] == [
        CalculationStatus.UNAVAILABLE, CalculationStatus.AVAILABLE, CalculationStatus.UNAVAILABLE]
    assert selection.pairs[0].reason_codes == (CalculationReason.REPRESENTATION_INCOMPATIBLE,)
    assert selection.pairs[-1].compatibility is None


def test_empty_python_snapshot_does_not_claim_loaded_evidence(tmp_path):
    case = _case("identified_empty_later")
    validation = _load_case(case, tmp_path)
    before = validation.version_order
    selection = select_longitudinal_versions(validation, declarations=_declarations(case))
    empty = selection.snapshots[-1]
    assert selection.primary_version == "v1"
    assert empty.population_scope.included_record_keys == ()
    assert empty.representation_scope is None
    assert selection.pairs[0].status is CalculationStatus.AVAILABLE  # declarations only
    assert validation.version_order is before
    assert selection.version_order.loaded_versions == ("v1",)
    basis = selection.pairs[0].compatibility
    context = ExplicitPairContext(selection.snapshots[0].population_scope, empty.population_scope,
        basis.earlier_representation, basis.later_representation, selection.version_order)
    with pytest.raises(CanonicalValidationError) as error:
        validate_representation_compatibility(context, earlier_state_semantics=basis.earlier_state_semantics,
                                             later_state_semantics=basis.later_state_semantics)
    assert error.value.code is ErrorCode.VERSION_ORDER_CONFLICT


def test_empty_earlier_snapshot_is_explicit_baseline(inputs):
    validation, declarations = inputs
    extra = replace(declarations[0], dataset_version="empty", empty_scope=True)
    order = resolve_version_order(validation.version_order.loaded_versions,
                                  document={"version_order": ("empty", "v1", "v2", "v3")})
    validation = replace(validation, version_order=order)
    selection = select_longitudinal_versions(validation, declarations=(*declarations, extra), baseline="first")
    assert selection.selected_order[0] == "empty"
    assert selection.version_order.loaded_versions == ("v1", "v2", "v3")
    assert len(selection.pairs) == 5


def test_missing_chronology_rejects_selection_without_affecting_inputs(tmp_path):
    case = _case("missing_order")
    validation = _load_case(case, tmp_path)
    with pytest.raises(CanonicalValidationError) as error:
        select_longitudinal_versions(validation, declarations=_declarations(case))
    assert error.value.code is ErrorCode.VERSION_ORDER_CONFLICT
    assert validation.records and validation.version_order.order == ()


@pytest.mark.parametrize("change", ["invocation_only", "invocation_plus_explicit", "conflict", "timestamp_conflict", "timestamp_tie"])
def test_series_rejects_invalid_order_evidence(inputs, change):
    validation, declarations = inputs
    retained = validation.version_order
    if change.startswith("invocation"):
        order = resolve_version_order(retained.loaded_versions,
            document=None if change == "invocation_only" else dict(retained.declarations),
            invocation_order=("v1", "v2", "v3"))
    else:
        document = dict(retained.declarations)
        if change == "conflict":
            document["version_rank"] = {"v1": 2, "v2": 1, "v3": 3}
        elif change == "timestamp_conflict":
            document["version_timestamps"] = {"v1": "2026-02-01T00:00:00Z",
                "v2": "2026-01-01T00:00:00Z", "v3": "2026-03-01T00:00:00Z"}
        else:
            document = {"version_timestamps": {v: "2026-01-01T00:00:00Z" for v in retained.loaded_versions}}
        order = replace(retained, declarations=document)
    with pytest.raises(CanonicalValidationError) as error:
        select_longitudinal_versions(replace(validation, version_order=order), declarations=declarations)
    assert error.value.code is ErrorCode.VERSION_ORDER_CONFLICT


def test_retained_sources_override_forged_cached_order(inputs):
    validation, declarations = inputs
    forged = replace(validation, version_order=replace(validation.version_order,
        order=("v3", "v2", "v1"), order_source="fabricated"))
    assert select_longitudinal_versions(forged, declarations=declarations) == select_longitudinal_versions(
        validation, declarations=declarations)


@pytest.mark.parametrize("change", ["missing", "extra", "list"])
def test_loaded_inventory_must_equal_all_actual_versions(inputs, change):
    validation, declarations = inputs
    loaded = validation.version_order.loaded_versions
    loaded = loaded[:-1] if change == "missing" else (*loaded, "unloaded") if change == "extra" else list(loaded)
    with pytest.raises(CanonicalValidationError):
        select_longitudinal_versions(replace(validation, version_order=replace(
            validation.version_order, loaded_versions=loaded)), declarations=declarations)


@pytest.mark.parametrize("change", ["duplicate", "missing", "unloaded", "false_empty", "undeclared_empty", "single", "list"])
def test_snapshot_declarations_require_exact_selected_coverage(inputs, change):
    validation, declarations = inputs
    bad = {
        "duplicate": (*declarations, declarations[0]),
        "missing": declarations[:2],
        "unloaded": (*declarations, replace(declarations[0], dataset_version="unloaded")),
        "false_empty": (replace(declarations[0], empty_scope=True), *declarations[1:]),
        "undeclared_empty": (*declarations, replace(declarations[0], dataset_version="empty", empty_scope=True)),
        "single": declarations[:1],
        "list": list(declarations),
    }[change]
    with pytest.raises(CanonicalValidationError):
        select_longitudinal_versions(validation, declarations=bad)


def test_context_cannot_be_admitted_even_with_empty_declaration(tmp_path):
    case = _case("lexical_order_context_unloaded")
    validation = _load_case(case, tmp_path)
    declarations = _declarations(case)
    for empty in (True, False):
        extra = replace(declarations[0], dataset_version=case["context_versions"][0], empty_scope=empty)
        with pytest.raises(CanonicalValidationError):
            select_longitudinal_versions(validation, declarations=(*declarations, extra))


@pytest.mark.parametrize("change", ["role_overlap", "context_overlap", "fragmented_file", "multi_version_file", "no_role", "old_primary"])
def test_input_role_and_file_partitions_cannot_redefine_snapshots(inputs, change):
    validation, declarations = inputs
    rows = list(validation.records)
    first = rows[0]
    if change in ("role_overlap", "context_overlap", "no_role"):
        role = {"role_overlap": FileRole.RECORDS_PRIMARY, "context_overlap": FileRole.LINEAGE_CONTEXT,
                "no_role": None}[change]
        rows[0] = replace(first, location=replace(first.location, file_role=role))
    elif change == "fragmented_file":
        rows[0] = replace(first, location=replace(first.location, file_path="another-file.jsonl"))
    elif change == "multi_version_file":
        rows = [replace(row, location=replace(row.location, file_path="same.jsonl"))
                if row.location.file_role is FileRole.RECORDS_COMPARE else row for row in rows]
    else:
        rows = [replace(row, location=replace(row.location, file_role=(
            FileRole.RECORDS_PRIMARY if row.record_key.dataset_version == "v1" else FileRole.RECORDS_COMPARE)))
            for row in rows]
    with pytest.raises(CanonicalValidationError):
        select_longitudinal_versions(replace(validation, records=tuple(rows)), declarations=declarations)


@pytest.mark.parametrize("value", [None, True, False, 0, -1, 2.0, 1.5, float("nan"), float("inf"), "100"])
def test_limit_requires_positive_builtin_integer(inputs, value):
    validation, declarations = inputs
    with pytest.raises(CanonicalValidationError) as error:
        select_longitudinal_versions(validation, declarations=declarations, max_versions=value)
    assert error.value.code is ErrorCode.CONFIG_INVALID


def test_limit_admits_exact_boundary_and_rejects_excess(inputs):
    validation, declarations = inputs
    assert len(select_longitudinal_versions(validation, declarations=declarations, max_versions=3).snapshots) == 3
    with pytest.raises(CanonicalValidationError) as error:
        select_longitudinal_versions(validation, declarations=declarations, max_versions=2)
    assert error.value.code is ErrorCode.LONGITUDINAL_RESOURCE_LIMIT_EXCEEDED


def test_default_limit_has_linear_pair_count_and_context_uses_no_slots(tmp_path):
    case = _case("lexical_order_context_unloaded")
    small = select_longitudinal_versions(_load_case(case, tmp_path), declarations=_declarations(case), max_versions=2)
    assert len(small.context_versions) == 1 and len(small.snapshots) == 2
    original = _case("identified_empty_later")
    declarations = _declarations(original)
    # Two loaded records and 99 separately identified empty Python snapshots.
    validation = _load_case(original, tmp_path)
    declarations = (declarations[0], *(replace(declarations[1], dataset_version=f"e{i}") for i in range(99)))
    order = resolve_version_order(("v1",), document={"version_order": tuple(d.dataset_version for d in declarations)})
    validation = replace(validation, version_order=order)
    result = select_longitudinal_versions(validation, declarations=declarations, baseline="first")
    assert result.max_versions == 100 and len(result.pairs) == 197
    assert result.version_order.loaded_versions == ("v1",)
    with pytest.raises(CanonicalValidationError) as error:
        select_longitudinal_versions(validation, declarations=(*declarations,
            replace(declarations[-1], dataset_version="extra")))
    assert error.value.code is ErrorCode.LONGITUDINAL_RESOURCE_LIMIT_EXCEEDED


@pytest.mark.parametrize("kind", ["ranks", "timestamps"])
def test_retained_nonlexical_rank_or_timestamp_order_is_sufficient(inputs, kind):
    validation, declarations = inputs
    document = ({"version_rank": {"v1": -2, "v2": 0, "v3": 5}} if kind == "ranks" else
                {"version_timestamps": {v: f"2026-01-0{i}T00:00:00+00:00"
                                        for i, v in enumerate(("v1", "v2", "v3"), 1)}})
    order = resolve_version_order(validation.version_order.loaded_versions, document=document)
    result = select_longitudinal_versions(replace(validation, version_order=order), declarations=declarations)
    assert result.selected_order == ("v1", "v2", "v3")
    for mapping in document.values():
        mapping["v1"] = "modified caller dictionary"
    assert validate_longitudinal_selection(replace(validation, version_order=order), result) == result


@pytest.mark.parametrize("baseline", [True, None, "all", "last", 1])
def test_baseline_requires_literal_known_policy(inputs, baseline):
    validation, declarations = inputs
    with pytest.raises(CanonicalValidationError):
        select_longitudinal_versions(validation, declarations=declarations, baseline=baseline)


@pytest.mark.parametrize("kwargs", [
    {"dataset_version": " v1"}, {"dataset_version": "bad::version"}, {"dataset_version": ""},
    {"state_semantics": ""}, {"state_semantics": []}, {"empty_scope": 1},
    {"missing_state_id": "M"}, {"representation": {}},
    {"representation": RepresentationConfig("topic", "topic_field", "topic", None, "exclude")},
    {"representation": RepresentationConfig("topic", "topic_field", "topic", "r1", "guess")},
])
def test_declaration_constructor_validates_literal_contract(inputs, kwargs):
    _, declarations = inputs
    with pytest.raises(CanonicalValidationError):
        replace(declarations[0], **kwargs)


@pytest.mark.parametrize("direction", ["earlier_to_later", "later_to_earlier"])
def test_directed_maps_retain_collisions_and_detach_literal_dictionary(tmp_path, direction):
    case = _case("directed_many_to_one")
    validation = _load_case(case, tmp_path)
    declarations = _declarations(case)
    states = {"red": "apple", "green": "apple", "pear": "pear"}
    supplied = _mapping(declarations, states=states, direction=direction)
    selection = select_longitudinal_versions(validation, declarations=declarations, mappings=(supplied,))
    pair = selection.pairs[0]
    assert pair.compatibility.collision_groups == (("apple", ("green", "red")),)
    assert pair.compatibility.harmonized_representation == _descriptor(
        declarations[-1] if direction == "earlier_to_later" else declarations[0])
    states["red"] = "changed"
    assert pair.mapping.state_mapping["red"] == "apple"
    with pytest.raises(TypeError):
        pair.mapping.state_mapping["red"] = "changed"
    assert validate_longitudinal_selection(validation, selection) == selection


@pytest.mark.parametrize("change", ["duplicate", "unscheduled", "reversed", "bare", "wrong_meaning", "wrong_descriptor", "direction"])
def test_explicit_pair_map_errors_are_rejected(inputs, change):
    validation, declarations = inputs
    supplied = _mapping(declarations, states={"A": "A"})
    with pytest.raises(CanonicalValidationError):
        if change == "duplicate":
            maps = (supplied, supplied)
        elif change == "unscheduled":
            maps = (replace(supplied, later_version="v3"),)
        elif change == "reversed":
            maps = (replace(supplied, earlier_version="v2", later_version="v1"),)
        elif change == "bare":
            maps = (supplied.declaration,)
        else:
            kwargs = {"wrong_meaning": {"source_state_semantics": "different"},
                      "wrong_descriptor": {"source_representation": replace(_descriptor(declarations[0]), representation_version="other")},
                      "direction": {"direction": "sideways"}}[change]
            maps = (replace(supplied, declaration=replace(supplied.declaration, **kwargs)),)
        select_longitudinal_versions(validation, declarations=declarations, mappings=maps)


def test_mapping_does_not_compose_across_adjacent_pairs(inputs):
    validation, declarations = inputs
    declarations = tuple(replace(item, state_semantics=f"meaning {index}") for index, item in enumerate(declarations))
    maps = (_mapping(declarations, states={"A": "A"}), _mapping(declarations[1:], states={"A": "A"}))
    selection = select_longitudinal_versions(validation, declarations=declarations, mappings=maps, baseline="first")
    assert [pair.status for pair in selection.pairs] == [
        CalculationStatus.AVAILABLE, CalculationStatus.UNAVAILABLE, CalculationStatus.AVAILABLE]


@pytest.mark.parametrize("states", [{"A": "M2", "M1": "M2"}, {"A": "A"}, {"M1": "wrong"}])
def test_mapping_preserves_missing_state_rules(inputs, states):
    validation, declarations = inputs
    declarations = tuple(replace(item, representation=replace(item.representation,
        missing_value_policy="explicit_missing_state"), missing_state_id=f"M{index}")
        for index, item in enumerate(declarations, 1))
    with pytest.raises(CanonicalValidationError):
        select_longitudinal_versions(validation, declarations=declarations,
                                     mappings=(_mapping(declarations, states=states),))


def test_shared_basis_helper_never_relaxes_missing_policy(inputs):
    _, declarations = inputs
    a = _descriptor(declarations[0])
    b = replace(a, missing_value_policy="error")
    with pytest.raises(CanonicalValidationError):
        validate_representation_basis(a, b, earlier_state_semantics="meaning", later_state_semantics="meaning",
            state_mapping=StateMappingDeclaration("earlier_to_later", a, b, "meaning", "meaning", {"A": "A"}))


def test_consumer_revalidates_same_key_record_and_parent_evidence(inputs):
    validation, declarations = inputs
    selection = select_longitudinal_versions(validation, declarations=declarations)
    for column, value in (("topic", "changed"), ("content", "changed text")):
        rows = (replace(validation.records[0], values={**validation.records[0].values, column: value}), *validation.records[1:])
        with pytest.raises(CanonicalValidationError):
            validate_longitudinal_selection(replace(validation, records=rows), selection)
    for column, value in (("parent_ids", ("v1::unseen",)), ("external_grounding", "unknown")):
        rows = (replace(validation.provenance[0], values={**validation.provenance[0].values, column: value}), *validation.provenance[1:])
        with pytest.raises(CanonicalValidationError):
            validate_longitudinal_selection(replace(validation, provenance=rows), selection)


def test_consumer_rejects_shrunken_population_and_changed_declaration(inputs):
    validation, declarations = inputs
    selection = select_longitudinal_versions(validation, declarations=declarations)
    first = selection.snapshots[0]
    shortened = replace(first, population_scope=replace(first.population_scope,
        included_record_keys=first.population_scope.included_record_keys[:-1]))
    changed = replace(first, declaration=replace(first.declaration, state_semantics="altered"))
    for snapshot in (shortened, changed):
        forged = replace(selection, snapshots=(snapshot, *selection.snapshots[1:]))
        with pytest.raises(CanonicalValidationError):
            validate_longitudinal_selection(validation, forged)


def test_selection_is_immutable_and_binding_is_private(inputs):
    validation, declarations = inputs
    selection = select_longitudinal_versions(validation, declarations=declarations)
    with pytest.raises(FrozenInstanceError):
        selection.primary_version = "v1"
    with pytest.raises(TypeError):
        selection.version_order.declarations["version_order"] = ("v3", "v2", "v1")
    assert selection.input_signature not in repr(selection)
    with pytest.raises(CanonicalValidationError):
        replace(selection, pairs=selection.pairs[:1])
    with pytest.raises(CanonicalValidationError):
        replace(selection, snapshots=selection.snapshots[::-1])


def test_permutations_and_physical_paths_do_not_change_selection(inputs):
    validation, declarations = inputs
    before = select_longitudinal_versions(validation, declarations=declarations, baseline="first")
    rows = tuple(replace(row, location=replace(row.location,
        file_path=f"renamed-{row.record_key.dataset_version}.jsonl", row_number=999, line_number=999))
        for row in reversed(validation.records))
    after = select_longitudinal_versions(replace(validation, records=rows,
        provenance=tuple(reversed(validation.provenance))), declarations=declarations[::-1], baseline="first")
    assert before == after


def test_nonsemantic_version_renaming_preserves_ordinal_pair_structure(tmp_path):
    case = _case()
    renamed = {"v1": "z-last-lexically", "v2": "v10", "v3": "v2"}
    for row in (*case["records"], *case["provenance"]):
        row["dataset_version"] = renamed[row["dataset_version"]]
    case["selected_versions"] = [renamed[v] for v in case["selected_versions"]]
    case["order_document"] = {"version_order": case["selected_versions"]}
    case["representations"] = {renamed[v]: value for v, value in case["representations"].items()}
    selection = select_longitudinal_versions(_load_case(case, tmp_path), declarations=_declarations(case), baseline="first")
    assert selection.selected_order == ("z-last-lexically", "v10", "v2")
    assert [(p.earlier_version, p.later_version) for p in selection.pairs] == [
        ("z-last-lexically", "v10"), ("z-last-lexically", "v2"), ("v10", "v2")]


def test_exact_content_declarations_reuse_actual_descriptor(inputs):
    validation, declarations = inputs
    config = RepresentationConfig("exact form", "content_hash", None, "r1", None, "exact_utf8_v1")
    declarations = tuple(replace(item, representation=config, state_semantics="exact record form") for item in declarations)
    selection = select_longitudinal_versions(validation, declarations=declarations)
    metadata = select_content_representation(representation_name="exact form",
        representation_version="r1", normalization_profile="exact_utf8_v1")
    actual = assign_content_states((), dataset_versions=("v1",), scope_id="empty",
        representation_name="exact form", representation_version="r1", normalization_profile="exact_utf8_v1",
        content_mode=ContentMode.INLINE)
    assert metadata == actual.representation.selection
    assert selection.pairs[0].compatibility.earlier_representation == metadata.descriptor


def test_selection_runs_no_assignment_metric_graph_report_or_file_access(inputs, monkeypatch):
    import builtins
    from recursive_integrity_toolkit.lineage import ancestry, graph
    from recursive_integrity_toolkit.metrics import diversity
    from recursive_integrity_toolkit.representations import content_hash, field

    validation, declarations = inputs
    def forbidden(*args, **kwargs):
        pytest.fail("selection executed a later analysis or accessed a file")
    for module, name in ((field, "assign_field_states"), (content_hash, "assign_content_states"),
            (diversity, "calculate_state_distribution"), (diversity, "compare_support"),
            (graph, "build_lineage_graph"), (ancestry, "analyze_lineage"), (builtins, "open")):
        monkeypatch.setattr(module, name, forbidden)
    selection = select_longitudinal_versions(validation, declarations=declarations)
    assert all(item.representation_scope is None for item in selection.snapshots)
