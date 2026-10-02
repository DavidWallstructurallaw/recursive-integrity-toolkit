"""Cycle-certificate verification shares its loaded affected population once."""
from types import FunctionType

import pytest

from recursive_integrity_toolkit.lineage import ancestry
from recursive_integrity_toolkit.models import RecordKey
from test_longitudinal_analysis import _select
from test_longitudinal_fixture_inputs import _load_case
from test_longitudinal_selection import _case


@pytest.mark.parametrize("descendants", [12, 300])
def test_cycle_descendant_membership_set_is_prepared_once(tmp_path, descendants):
    case = _case("lineage_complete")
    for row in case["provenance"]:
        if row["dataset_version"] == "anchors":
            row["parent_ids"] = ["anchors::b" if row["record_id"] == "a" else "anchors::a"]
            row["external_grounding"] = "no"
    for index in range(descendants):
        key = {"dataset_version": "v3", "record_id": f"extra{index:04d}"}
        case["records"].append({**key, "content": "bounded cycle descendant", "topic": "A"})
        case["provenance"].append({**key, "source_type": "synthetic",
            "provenance_confidence": "confirmed", "external_grounding": "no",
            "parent_ids": ["anchors::a"], "transformation": "generate"})
    # An unrelated context root must remain outside the affected population.
    key = {"dataset_version": "anchors", "record_id": "isolated"}
    case["records"].append({**key, "content": "independent context root", "topic": "context"})
    case["provenance"].append({**key, "source_type": "human",
        "provenance_confidence": "confirmed", "external_grounding": "yes",
        "parent_ids": [], "transformation": "generate"})
    validation = _load_case(case, tmp_path)
    selection = _select(case, validation)
    result = ancestry.analyze_selected_lineage(validation, selection=selection)
    cycles, graph = result.shared_cycles, result.shared_graph
    assert cycles.cycle_count == 1
    assert cycles.affected_record_count == len(validation.records) - 1
    assert RecordKey("anchors", "isolated") not in cycles.affected_record_keys
    assert all(target.unresolved_record_count == target.scope.target_record_count
               for target in result.targets)

    differences = []

    class MeasuredSet(set):
        def __sub__(self, other):
            differences.append((len(self), len(other)))
            return super().__sub__(other)

    # Instrument only the real certificate validator's set creation. No graph,
    # cycle, depth, root, or supplied-certificate computation is replaced.
    owner = ancestry._validate_selected_structure
    measured = FunctionType(owner.__code__, {**owner.__globals__, "set": MeasuredSet})
    measured(graph, cycles, result.certificate)
    assert differences == [(cycles.affected_record_count, 2)]
    ancestry.validate_selected_lineage_result(validation, selection=selection, result=result)
