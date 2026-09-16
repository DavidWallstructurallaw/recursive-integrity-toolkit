"""Check module ownership and the approved Phase 2 Step 1 boundary.

The Theory Owner authorized this checker update on 2026-09-16. Only the
root-level models.py, errors.py, and config.py may contain the existing Step 1
contracts and explicit local configuration behavior. All other non-bootstrap
modules must remain docstring-only, including Step 2 ingestion modules.

This script inspects source syntax without importing the package or loading
hero data. Definition and import allowlists are structural checks; behavioral
correctness remains covered by the unit and security tests.
"""

from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "src" / "recursive_integrity_toolkit"
BOOTSTRAP = {"__init__.py", "__main__.py", "cli.py"}
STEP1_CORE = {"models.py", "errors.py", "config.py"}
ALLOWED_FUNCTIONS = {
    "__init__.py": set(),
    "__main__.py": set(),
    "cli.py": {"build_parser", "main"},
    "models.py": {
        "RecordKey.__post_init__", "RecordKey.__str__", "RecordKey.parse",
        "_validate_identifier", "ValidationCoverage.__post_init__",
        "ObservabilityAssessment.__post_init__",
    },
    "errors.py": {"ToolkitError.__init__"},
    "config.py": {
        "load_config", "resolve_config", "_parse_inputs", "_parse_input_source",
        "_parse_representation", "_parse_version_order", "_parse_resource_limits",
        "_parse_simulation", "_optional_string", "_string_sequence",
        "_string_mapping", "_frozen_mapping", "_bool_value",
        "_optional_positive_int", "_enum_value", "_invalid",
    },
}
ALLOWED_CLASSES = {
    "models.py": {
        "FileRole", "FileFormat", "ValidationSeverity", "CapabilityStatus",
        "CapabilityKey", "PrivacyMode", "ParentResolutionStatus", "RecordKey",
        "InputSource", "AuditBundle", "FileInventoryEntry", "ValidationMessage",
        "ValidationCoverage", "Capability", "ObservabilityAssessment",
    },
    "errors.py": {
        "ErrorCode", "WarningCode", "ToolkitError", "ConfigurationError",
        "InputError", "SchemaError", "SecurityError",
    },
    "config.py": {
        "RepresentationConfig", "ResourceLimits", "ScenarioConfig", "ResolvedConfig",
    },
}
# Exact module paths, including relative-import levels, keep later-layer imports
# out of the three narrowly authorized files. Optional dependencies stay blocked.
ALLOWED_CORE_IMPORTS = {
    "models.py": {"__future__", "dataclasses", "enum", "pathlib", "typing"},
    "errors.py": {"__future__", "enum"},
    "config.py": {
        "__future__", "json", "tomllib", "dataclasses", "pathlib", "typing",
        ".errors", ".models",
    },
}
# Preserve every import and file restriction from the Phase 1 checker.
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


def _definitions(tree: ast.AST, prefix: str = "") -> tuple[list[str], list[str]]:
    """Collect qualified definitions without executing inspected source."""
    functions: list[str] = []
    classes: list[str] = []
    for node in ast.iter_child_nodes(tree):
        child_prefix = prefix
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            name = f"{prefix}.{node.name}" if prefix else node.name
            if isinstance(node, ast.AsyncFunctionDef):
                raise SystemExit(f"Async implementation is outside Step 1: {name}")
            if isinstance(node, ast.ClassDef):
                classes.append(name)
            else:
                functions.append(name)
            child_prefix = name
        child_functions, child_classes = _definitions(node, child_prefix)
        functions.extend(child_functions)
        classes.extend(child_classes)
    return functions, classes


def main() -> int:
    paths = sorted(PACKAGE.rglob("*.py"))
    if len(paths) != 40:
        raise SystemExit(f"Expected 40 package modules, found {len(paths)}")
    relative_paths = {path.relative_to(PACKAGE).as_posix() for path in paths}
    missing = (BOOTSTRAP | STEP1_CORE) - relative_paths
    if missing:
        raise SystemExit(f"Required startup or Step 1 modules missing: {sorted(missing)}")

    imported_roots: set[str] = set()
    placeholder_count = 0

    for path in paths:
        relative = path.relative_to(PACKAGE).as_posix()
        if path.name in FORBIDDEN_FILES:
            raise SystemExit(f"Forbidden module found: {path}")
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        doc = ast.get_docstring(tree) or ""
        if "Owner IDs:" not in doc or "Current phase status:" not in doc:
            raise SystemExit(f"Owner or phase metadata missing: {path}")

        if relative not in BOOTSTRAP | STEP1_CORE:
            if not (
                len(tree.body) == 1
                and isinstance(tree.body[0], ast.Expr)
                and isinstance(tree.body[0].value, ast.Constant)
                and isinstance(tree.body[0].value.value, str)
            ):
                raise SystemExit(f"Protected non-Step-1 executable body found: {path}")
            placeholder_count += 1
        else:
            functions, classes = _definitions(tree)
            if (
                set(functions) != ALLOWED_FUNCTIONS[relative]
                or len(functions) != len(set(functions))
            ):
                raise SystemExit(f"Unexpected Step 1 functions in {relative}: {functions}")
            if (
                set(classes) != ALLOWED_CLASSES.get(relative, set())
                or len(classes) != len(set(classes))
            ):
                raise SystemExit(f"Unexpected Step 1 classes in {relative}: {classes}")

        for node in ast.walk(tree):
            imports: set[str] = set()
            if isinstance(node, ast.Import):
                imports.update(alias.name for alias in node.names)
                imported_roots.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                imports.add("." * node.level + (node.module or ""))
                if node.module:
                    imported_roots.add(node.module.split(".")[0])
            if relative in STEP1_CORE:
                unexpected = imports - ALLOWED_CORE_IMPORTS[relative]
                if unexpected:
                    raise SystemExit(
                        f"Import outside Step 1 contracts in {relative}: {sorted(unexpected)}"
                    )

    forbidden_used = sorted(imported_roots & FORBIDDEN_IMPORTS)
    if forbidden_used:
        raise SystemExit(f"Analytical dependency imported before authorization: {forbidden_used}")

    print(f"package modules checked: {len(paths)}")
    print(f"allowed startup functions: {sorted(ALLOWED_FUNCTIONS['cli.py'])}")
    print(f"authorized Step 1 contract modules: {sorted(STEP1_CORE)}")
    print(f"protected docstring-only modules: {placeholder_count}")
    print("owner metadata: PASS")
    print("Step 1 definition and import allowlists: PASS")
    print("no-algorithm phase boundary: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
