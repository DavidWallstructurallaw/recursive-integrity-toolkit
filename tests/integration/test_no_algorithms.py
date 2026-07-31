"""Check that Phase 1 contains no analytical or data-processing implementation."""

import ast


BOOTSTRAP_FILES = {"__init__.py", "__main__.py", "cli.py"}
ALLOWED_FUNCTIONS = {"build_parser", "main"}
FORBIDDEN_IMPORT_ROOTS = {
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


def test_non_bootstrap_modules_are_docstring_only(package_root) -> None:
    for path in sorted(package_root.rglob("*.py")):
        if path.name in BOOTSTRAP_FILES and path.parent == package_root:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        assert len(tree.body) == 1, f"Unexpected executable body: {path}"
        node = tree.body[0]
        assert isinstance(node, ast.Expr)
        assert isinstance(node.value, ast.Constant)
        assert isinstance(node.value.value, str)


def test_only_startup_functions_exist(package_root) -> None:
    function_names = []
    for path in sorted(package_root.rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        function_names.extend(
            node.name for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        )
    assert set(function_names) == ALLOWED_FUNCTIONS


def test_no_analytical_dependency_imports(package_root) -> None:
    imported_roots = set()
    for path in sorted(package_root.rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_roots.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported_roots.add(node.module.split(".")[0])
    assert not (imported_roots & FORBIDDEN_IMPORT_ROOTS)
