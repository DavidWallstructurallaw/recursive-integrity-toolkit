"""Check Phase 1 module ownership and no-algorithm boundaries.

This script inspects Python syntax and docstrings. It does not execute any audit
calculation or load hero data.
"""

from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "src" / "recursive_integrity_toolkit"
BOOTSTRAP = {"__init__.py", "__main__.py", "cli.py"}
ALLOWED_FUNCTIONS = {"build_parser", "main"}
FORBIDDEN_IMPORTS = {
    "numpy",
    "pandas",
    "pyarrow",
    "networkx",
    "scipy",
    "sklearn",
    "torch",
    "tensorflow",
    "transformers",
}
FORBIDDEN_FILES = {"collapse_score.py", "integrity_score.py", "universal_score.py"}


def main() -> int:
    paths = sorted(PACKAGE.rglob("*.py"))
    if len(paths) != 40:
        raise SystemExit(f"Expected 40 package modules, found {len(paths)}")

    function_names: set[str] = set()
    imported_roots: set[str] = set()

    for path in paths:
        if path.name in FORBIDDEN_FILES:
            raise SystemExit(f"Forbidden module found: {path}")
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        doc = ast.get_docstring(tree) or ""
        if "Owner IDs:" not in doc or "Current phase status:" not in doc:
            raise SystemExit(f"Owner or phase metadata missing: {path}")

        if not (path.parent == PACKAGE and path.name in BOOTSTRAP):
            if len(tree.body) != 1 or not isinstance(tree.body[0], ast.Expr):
                raise SystemExit(f"Non-bootstrap executable body found: {path}")

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                function_names.add(node.name)
            elif isinstance(node, ast.Import):
                imported_roots.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported_roots.add(node.module.split(".")[0])

    if function_names != ALLOWED_FUNCTIONS:
        raise SystemExit(f"Unexpected package functions: {sorted(function_names)}")
    forbidden_used = sorted(imported_roots & FORBIDDEN_IMPORTS)
    if forbidden_used:
        raise SystemExit(f"Analytical dependency imported in scaffold: {forbidden_used}")

    print(f"package modules checked: {len(paths)}")
    print(f"allowed startup functions: {sorted(function_names)}")
    print("owner metadata: PASS")
    print("no-algorithm boundary: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
