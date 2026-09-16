"""Check module ownership and the approved Phase 2 Step 2 boundary.

The Theory Owner authorized the Step 2 checker exception on 2026-09-16.
Only io/loaders.py, utils/hashing.py, and utils/paths.py gain local physical
file behavior in addition to Step 2 contracts. Every other non-bootstrap
module remains docstring-only. No mapping, normalization, metrics, graph,
observability classification, or report implementation is authorized here.

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
STEP2_IO = {"io/loaders.py", "utils/hashing.py", "utils/paths.py"}
ALLOWED_FUNCTIONS = {'__init__.py': set(),
 '__main__.py': set(),
 'cli.py': {'build_parser', 'main'},
 'config.py': {'_bool_value',
               '_enum_value',
               '_frozen_mapping',
               '_invalid',
               '_optional_positive_int',
               '_optional_string',
               '_parse_input_source',
               '_parse_inputs',
               '_parse_representation',
               '_parse_resource_limits',
               '_parse_simulation',
               '_parse_version_order',
               '_string_mapping',
               '_string_sequence',
               'load_config',
               'resolve_config'},
 'errors.py': {'IngestionError.__init__', 'ToolkitError.__init__'},
 'io/loaders.py': {'_check_csv_quotes',
                   '_check_depth',
                   '_failure',
                   '_finite_float',
                   '_headers',
                   '_limits',
                   '_parse_csv',
                   '_parse_jsonl',
                   '_parse_parquet',
                   '_read_source',
                   '_reject_constant',
                   '_row_limit',
                   '_select_format',
                   '_text',
                   '_unique_object',
                   'inventory_source',
                   'load_table'},
 'models.py': {'ObservabilityAssessment.__post_init__',
               'RecordKey.__post_init__',
               'RecordKey.__str__',
               'RecordKey.parse',
               'ValidationCoverage.__post_init__',
               '_validate_identifier'},
 'utils/hashing.py': {'sha256_bytes'},
 'utils/paths.py': {'local_input_path'}}
ALLOWED_CLASSES = {'config.py': {'RepresentationConfig', 'ResourceLimits', 'ScenarioConfig', 'ResolvedConfig'},
 'errors.py': {'ConfigurationError',
               'ErrorCode',
               'IngestionError',
               'InputError',
               'SchemaError',
               'SecurityError',
               'ToolkitError',
               'WarningCode'},
 'models.py': {'AuditBundle',
               'Capability',
               'CapabilityKey',
               'CapabilityStatus',
               'FileFormat',
               'FileInventoryEntry',
               'FileRole',
               'InputSource',
               'LoadedTable',
               'ObservabilityAssessment',
               'ParentResolutionStatus',
               'PrivacyMode',
               'RawRow',
               'RecordKey',
               'ValidationCoverage',
               'ValidationMessage',
               'ValidationSeverity'}}
ALLOWED_CORE_IMPORTS = {'config.py': {'.errors',
               '.models',
               '__future__',
               'dataclasses',
               'json',
               'pathlib',
               'tomllib',
               'typing'},
 'errors.py': {'enum', '__future__'},
 'io/loaders.py': {'..config',
                   '..errors',
                   '..models',
                   '..utils.hashing',
                   '..utils.paths',
                   '__future__',
                   'csv',
                   'io',
                   'json',
                   'math',
                   'os',
                   'pathlib',
                   'pyarrow',
                   'pyarrow.parquet',
                   'stat',
                   'threading'},
 'models.py': {'__future__', 'dataclasses', 'typing', 'enum', 'pathlib'},
 'utils/hashing.py': {'__future__', 'hashlib'},
 'utils/paths.py': {'__future__', 're', 'os', 'pathlib', '..errors'}}
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
                raise SystemExit(f"Async implementation is outside Step 2: {name}")
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
    missing = (BOOTSTRAP | STEP1_CORE | STEP2_IO) - relative_paths
    if missing:
        raise SystemExit(f"Required startup or Step 2 modules missing: {sorted(missing)}")

    imported_roots: set[str] = set()
    forbidden_locations: list[str] = []
    placeholder_count = 0

    for path in paths:
        relative = path.relative_to(PACKAGE).as_posix()
        if path.name in FORBIDDEN_FILES:
            raise SystemExit(f"Forbidden module found: {path}")
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        doc = ast.get_docstring(tree) or ""
        if "Owner IDs:" not in doc or "Current phase status:" not in doc:
            raise SystemExit(f"Owner or phase metadata missing: {path}")

        if relative not in BOOTSTRAP | STEP1_CORE | STEP2_IO:
            if not (
                len(tree.body) == 1
                and isinstance(tree.body[0], ast.Expr)
                and isinstance(tree.body[0].value, ast.Constant)
                and isinstance(tree.body[0].value.value, str)
            ):
                raise SystemExit(f"Protected non-Step-2 executable body found: {path}")
            placeholder_count += 1
        else:
            functions, classes = _definitions(tree)
            if (
                set(functions) != ALLOWED_FUNCTIONS[relative]
                or len(functions) != len(set(functions))
            ):
                raise SystemExit(f"Unexpected Step 2 functions in {relative}: {functions}")
            if (
                set(classes) != ALLOWED_CLASSES.get(relative, set())
                or len(classes) != len(set(classes))
            ):
                raise SystemExit(f"Unexpected Step 2 classes in {relative}: {classes}")

        for node in ast.walk(tree):
            imports: set[str] = set()
            if isinstance(node, ast.Import):
                imports.update(alias.name for alias in node.names)
                imported_roots.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                imports.add("." * node.level + (node.module or ""))
                if node.module:
                    imported_roots.add(node.module.split(".")[0])
            for imported in imports:
                root = imported.lstrip(".").split(".")[0]
                if root in FORBIDDEN_IMPORTS:
                    lazy_parquet = (
                        relative == "io/loaders.py"
                        and imported in {"pyarrow", "pyarrow.parquet"}
                        and any(
                            isinstance(function, ast.FunctionDef)
                            and function.name == "_parse_parquet"
                            and any(child is node for child in ast.walk(function))
                            for function in tree.body
                        )
                    )
                    if not lazy_parquet:
                        forbidden_locations.append(f"{relative}: {imported}")
            if relative in STEP1_CORE | STEP2_IO:
                unexpected = imports - ALLOWED_CORE_IMPORTS[relative]
                if unexpected:
                    raise SystemExit(
                        f"Import outside Step 2 contracts in {relative}: {sorted(unexpected)}"
                    )

    if forbidden_locations:
        raise SystemExit(f"Dependency outside the approved scope: {forbidden_locations}")

    print(f"package modules checked: {len(paths)}")
    print(f"allowed startup functions: {sorted(ALLOWED_FUNCTIONS['cli.py'])}")
    print(f"authorized Step 2 contract modules: {sorted(STEP1_CORE)}")
    print(f"authorized Step 2 file modules: {sorted(STEP2_IO)}")
    print(f"protected docstring-only modules: {placeholder_count}")
    print("owner metadata: PASS")
    print("Step 2 definition and import allowlists: PASS")
    print("no-algorithm phase boundary: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
