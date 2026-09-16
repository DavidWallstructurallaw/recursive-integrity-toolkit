"""Protect Phase 2 Step 1 from premature analytical implementation."""

import ast
from pathlib import Path


STEP1_EXECUTABLE = {"__init__.py", "__main__.py", "cli.py", "config.py", "errors.py", "models.py"}
PROTECTED_PREFIXES = {"io", "lineage", "metrics", "observability", "reports", "representations", "utils"}
FORBIDDEN_ANALYTICAL_IMPORT_ROOTS = {"networkx", "scipy", "sklearn", "torch", "tensorflow", "transformers"}
FORBIDDEN_ANALYTICAL_NAMES = {"support_size", "gini_simpson", "tail_fragility", "source_type_shares", "closure_bounds", "ancestry_hhi", "effective_external_roots", "resample", "reopening"}


def _is_docstring_only(path: Path) -> bool:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    return len(tree.body) == 1 and isinstance(tree.body[0], ast.Expr) and isinstance(tree.body[0].value, ast.Constant) and isinstance(tree.body[0].value.value, str)


def test_only_step1_core_contract_modules_gain_behavior(package_root) -> None:
    for path in sorted(package_root.rglob("*.py")):
        relative = path.relative_to(package_root)
        if len(relative.parts) == 1 and path.name in STEP1_EXECUTABLE:
            continue
        assert _is_docstring_only(path), f"Premature executable body: {relative}"


def test_protected_phase3_plus_modules_remain_placeholders(package_root) -> None:
    for prefix in PROTECTED_PREFIXES:
        for path in sorted((package_root / prefix).rglob("*.py")):
            assert _is_docstring_only(path), f"Protected module changed in Step 1: {path}"
    assert _is_docstring_only(package_root / "result.py")


def test_no_prohibited_analytical_dependency_imports(package_root) -> None:
    imported_roots = set()
    for path in sorted(package_root.rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_roots.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported_roots.add(node.module.split(".")[0])
    assert not (imported_roots & FORBIDDEN_ANALYTICAL_IMPORT_ROOTS)


def test_no_analytical_function_names_exist(package_root) -> None:
    names = set()
    for path in sorted(package_root.rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        names.update(node.name for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)))
    assert not (names & FORBIDDEN_ANALYTICAL_NAMES)
