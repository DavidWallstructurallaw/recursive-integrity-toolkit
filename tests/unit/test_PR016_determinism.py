"""PR-016 lexical order retained; Step 8 seeded determinism has explicit boundaries."""

import ast
from itertools import permutations
import pytest

from recursive_integrity_toolkit.io.normalization import normalize_row
from recursive_integrity_toolkit.utils.ordering import stable_record_order


def _row(version, identity):
    return normalize_row({"dataset_version": version, "record_id": identity, "content": "synthetic"},
                         kind="records")


def test_PR016_ordering_owner_and_no_later_behavior(owner_checker, package_root, placeholder_checker,phase3_final_placeholder_checker):
    placeholder_checker = phase3_final_placeholder_checker
    owner_checker("utils/ordering.py", "PR-016")
    tree = ast.parse((package_root / "utils/ordering.py").read_text())
    names = {node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}
    assert names == {"_record_order_key", "stable_record_order"}
    for path in ["reports/json_report.py", "reports/markdown_report.py"]:
        placeholder_checker(path)
    # The authorized shared module is checked against its exact reviewed body.
    import runpy
    checker = runpy.run_path(str(package_root.parents[1] / "scripts/check_traceability.py"))
    source = (package_root / "metrics/resampling.py").read_text(encoding="utf-8")
    checker["_phase3_resampling_boundary"](ast.parse(source))


def test_PR016_stable_exact_lexical_order_is_not_version_chronology():
    rows = (_row("v2", "a"), _row("v10", "b"), _row("v1", "0001"))
    expected = (rows[2], rows[1], rows[0])
    for permutation in permutations(rows):
        assert stable_record_order(permutation) == expected
    assert rows[0].record_key.dataset_version == "v2"


def test_PR016_ordering_does_not_drop_repeated_rows():
    row = _row("v1", "a")
    assert stable_record_order((row, row)) == (row, row)


@pytest.mark.parametrize("rows", [[], ("invalid",)])
def test_PR016_only_canonical_tuple_rows_accepted(rows):
    with pytest.raises(TypeError):
        stable_record_order(rows)
