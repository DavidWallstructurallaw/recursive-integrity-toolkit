"""PR-009 Step 4 declared generation types only; parent-based derivation is deferred."""

import ast
import pytest

from recursive_integrity_toolkit.errors import CanonicalValidationError, ErrorCode
from recursive_integrity_toolkit.io.normalization import normalize_row, normalize_table
from recursive_integrity_toolkit.io.loaders import load_table
from recursive_integrity_toolkit.models import InputSource, FileRole


def _row(generation):
    return {"dataset_version": "v1", "record_id": "a", "source_type": "human",
            "provenance_confidence": "unknown", "external_grounding": "yes", "generation": generation}


def test_PR009_generation_owner_and_no_derivation(owner_checker, package_root, placeholder_checker):
    owner_checker("io/validation.py", "PR-009")
    tree = ast.parse((package_root / "io/validation.py").read_text())
    names = {node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}
    assert not names & {"expected_generation", "derive_generation", "lineage_depth", "detect_cycles"}
    for path in ["lineage/graph.py", "lineage/cycles.py", "lineage/ancestry.py"]:
        placeholder_checker(path)


@pytest.mark.parametrize("value", [0, 1, 2, 1000, None])
def test_PR009_declared_generation_is_preserved_without_inference(value):
    row = normalize_row(_row(value), kind="provenance")
    assert row.values["generation"] == value
    assert "expected_generation" not in row.values and "lineage_depth" not in row.values
    # Even yes-grounding with a nonzero declaration is retained for Step 6 consistency checks.
    assert row.values["external_grounding"] == "yes"


@pytest.mark.parametrize("value", [-1, True, False, 1.0, 1.5, "1", [], {}])
def test_PR009_invalid_native_generation_type(value):
    with pytest.raises(CanonicalValidationError) as exc:
        normalize_row(_row(value), kind="provenance")
    assert exc.value.code is ErrorCode.SCHEMA_TYPE and exc.value.field == "generation"


@pytest.mark.parametrize("token,expected", [("0", 0), ("001", 1), ("2", 2), ("", None), ("null", None)])
def test_PR009_csv_integer_serialization(tmp_path, token, expected):
    path = tmp_path / "generation.csv"
    path.write_text("dataset_version,record_id,source_type,provenance_confidence,external_grounding,generation\n"
                    "v1,a,unknown,unknown,unknown," + token + "\n")
    row = normalize_table(load_table(InputSource(FileRole.PROVENANCE_MANIFEST, path)))[0]
    assert row.values["generation"] == expected


@pytest.mark.parametrize("token", ["1.0", "1.5", "1e1", "-1", "true", "NaN"])
def test_PR009_fractional_or_invalid_csv_generation_fails(tmp_path, token):
    path = tmp_path / "bad-generation.csv"
    path.write_text("dataset_version,record_id,source_type,provenance_confidence,external_grounding,generation\n"
                    "v1,a,unknown,unknown,unknown," + token + "\n")
    with pytest.raises(CanonicalValidationError):
        normalize_table(load_table(InputSource(FileRole.PROVENANCE_MANIFEST, path)))
