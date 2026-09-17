"""Check module ownership and the approved Phase 2 Step 6 boundary.

The Theory Owner authorized synchronized checker maintenance for each explicitly
approved Phase 2 step on 2026-09-16. Step 6 adds only declared chronology,
immediate parent-reference checks and bounded generation consistency validation.
General graphs, cycles, roots, ancestors, metrics and later layers stay protected.

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
STEP3_MAPPING = {"io/schema_mapping.py"}
ALLOWED_FUNCTIONS = {
    "__init__.py": set(),
    "__main__.py": set(),
    "cli.py": {"build_parser", "main"},
    "config.py": {
        "_bool_value", "_enum_value", "_frozen_mapping", "_invalid",
        "_optional_positive_int", "_optional_string", "_parse_input_source",
        "_parse_inputs", "_parse_representation", "_parse_resource_limits",
        "_parse_simulation", "_parse_version_order", "_string_mapping",
        "_string_sequence", "load_config", "resolve_config",
    },
    "errors.py": {"IngestionError.__init__", "ToolkitError.__init__", "MappingError.__init__"},
    "io/loaders.py": {
        "_check_csv_quotes", "_check_depth", "_failure", "_finite_float", "_headers",
        "_limits", "_parse_csv", "_parse_jsonl", "_parse_parquet", "_read_source",
        "_reject_constant", "_row_limit", "_select_format", "_text",
        "_unique_object", "inventory_source", "load_table",
    },
    "models.py": {
        "ObservabilityAssessment.__post_init__", "RecordKey.__post_init__",
        "RecordKey.__str__", "RecordKey.parse", "ValidationCoverage.__post_init__",
        "_validate_identifier",
    },
    "utils/hashing.py": {"sha256_bytes"},
    "utils/paths.py": {"local_input_path"},
    "io/schema_mapping.py": {
        "_error", "_copy_value", "_unique_object", "_reject_constant", "_finite_float",
        "_json_value", "_name", "_validate_operation", "_validate_document",
        "compile_mapping", "parse_mapping_json", "load_mapping", "_select",
        "_coalesce", "_apply_operation", "map_row",
    },
}
ALLOWED_CLASSES = {
    "config.py": {"RepresentationConfig", "ResourceLimits", "ScenarioConfig", "ResolvedConfig"},
    "errors.py": {
        "ConfigurationError", "ErrorCode", "IngestionError", "InputError",
        "SchemaError", "SecurityError", "ToolkitError", "WarningCode", "MappingError",
    },
    "models.py": {
        "AuditBundle", "Capability", "CapabilityKey", "CapabilityStatus", "FileFormat",
        "FileInventoryEntry", "FileRole", "InputSource", "LoadedTable",
        "ObservabilityAssessment", "ParentResolutionStatus", "PrivacyMode", "RawRow",
        "RecordKey", "ValidationCoverage", "ValidationMessage", "ValidationSeverity",
    },
    "io/schema_mapping.py": {"MappingPlan", "FieldMappingTrace", "MappingNotice", "MappedRow"},
}
ALLOWED_CORE_IMPORTS = {
    "config.py": {".errors", ".models", "__future__", "dataclasses", "json", "pathlib", "tomllib", "typing"},
    "errors.py": {"enum", "__future__"},
    "io/loaders.py": {
        "..config", "..errors", "..models", "..utils.hashing", "..utils.paths",
        "__future__", "csv", "io", "json", "math", "os", "pathlib", "pyarrow",
        "pyarrow.parquet", "stat", "threading",
    },
    "models.py": {"__future__", "dataclasses", "typing", "enum", "pathlib"},
    "utils/hashing.py": {"__future__", "hashlib"},
    "utils/paths.py": {"__future__", "re", "os", "pathlib", "..errors"},
    "io/schema_mapping.py": {
        "..config", "..errors", "..models", "..utils.hashing", ".loaders", "__future__",
        "dataclasses", "datetime", "json", "math", "pathlib", "re",
    },
}

# Step 4 permission covers row-local normalization, base validation and ordering.
# Step 5 join definitions are authorized individually below, never by wildcard.
STEP4_ROWS = {"io/normalization.py", "io/validation.py", "utils/ordering.py"}
ALLOWED_FUNCTIONS.update({
    "io/normalization.py": {
        "_policy", "_location", "_csv_quotes", "_input", "_state", "_timestamp",
        "_parent_list", "_field_value", "_freeze", "normalize_row", "normalize_table",
    },
    "io/validation.py": {
        "_fail", "canonical_fields", "validate_canonical_values", "validate_unique_keys",
    },
    "utils/ordering.py": {"_record_order_key", "stable_record_order"},
})
ALLOWED_FUNCTIONS["errors.py"].add("CanonicalValidationError.__init__")
ALLOWED_CLASSES["errors.py"].add("CanonicalValidationError")
ALLOWED_CLASSES["models.py"].update({
    "SourceType", "ProvenanceConfidence", "ExternalGrounding", "Transformation",
    "ContentMode", "NormalizationOptions", "RowLocation", "CanonicalRow",
})
ALLOWED_CORE_IMPORTS.update({
    "io/normalization.py": {
        "__future__", "math", "re", "datetime", "zoneinfo", "types", "json", "..config",
        "..errors", "..models", "..utils.ordering", ".schema_mapping", ".loaders", ".validation",
    },
    "io/validation.py": {"__future__", "math", "datetime", "..errors", "..models"},
    "utils/ordering.py": {"__future__", "..models"},
})

# Step 5 changes no module-level allowlist. Only these exact definitions are added.
ALLOWED_FUNCTIONS["io/validation.py"].update({
    "_validate_present_fields", "_join_location", "_join_fields", "_join_identity",
    "assess_provenance_row", "_join_message", "_join_options", "join_provenance",
})
ALLOWED_FUNCTIONS["models.py"].update({"ValidationCoverage.ratio", "ProvenanceJoinResult.has_errors"})
ALLOWED_CLASSES["models.py"].update({"ProvenanceAssessment", "ProvenanceMatch", "ProvenanceJoinResult"})
ALLOWED_CORE_IMPORTS["io/validation.py"].add("types")

# Step 6 adds only chronology, immediate references and generation validation.
# The executable module set is unchanged; no future module is opened.
ALLOWED_FUNCTIONS["io/validation.py"].update({
    "_version_failure", "_version_labels", "_version_map", "_version_timestamp",
    "resolve_version_order", "_checked_order", "_parent_keys", "parse_parent_ids",
    "_reference_key", "_parent_notice", "_parent_lookup", "_resolve_parent_list",
    "resolve_parent_references", "validate_generation_declarations",
})
ALLOWED_FUNCTIONS["models.py"].add("GenerationValidationResult.has_errors")
ALLOWED_CLASSES["models.py"].update({
    "VersionOrderResult", "ParentReference", "ParentValidationResult",
    "GenerationAssessment", "GenerationValidationResult",
})
ALLOWED_CORE_IMPORTS["io/validation.py"].add("json")

# Preserve every import and file restriction from the Phase 1 checker.
FORBIDDEN_IMPORTS = {
    "numpy", "pandas", "pyarrow", "networkx", "scipy", "sklearn", "torch",
    "tensorflow", "transformers",
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
                raise SystemExit(f"Async implementation is outside Step 6: {name}")
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
    missing = (BOOTSTRAP | STEP1_CORE | STEP2_IO | STEP3_MAPPING | STEP4_ROWS) - relative_paths
    if missing:
        raise SystemExit(f"Required startup or Step 6 modules missing: {sorted(missing)}")

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

        if relative not in BOOTSTRAP | STEP1_CORE | STEP2_IO | STEP3_MAPPING | STEP4_ROWS:
            if not (
                len(tree.body) == 1
                and isinstance(tree.body[0], ast.Expr)
                and isinstance(tree.body[0].value, ast.Constant)
                and isinstance(tree.body[0].value.value, str)
            ):
                raise SystemExit(f"Protected non-Step-6 executable body found: {path}")
            placeholder_count += 1
        else:
            functions, classes = _definitions(tree)
            if set(functions) != ALLOWED_FUNCTIONS[relative] or len(functions) != len(set(functions)):
                raise SystemExit(f"Unexpected Step 6 functions in {relative}: {functions}")
            if set(classes) != ALLOWED_CLASSES.get(relative, set()) or len(classes) != len(set(classes)):
                raise SystemExit(f"Unexpected Step 6 classes in {relative}: {classes}")

        for node in ast.walk(tree):
            if relative in STEP3_MAPPING | STEP4_ROWS | {"models.py"}:
                if isinstance(node, ast.Lambda):
                    raise SystemExit(f"Unexpected dynamic callback in {relative}")
                if isinstance(node, ast.Call):
                    dangerous = {"eval", "exec", "compile", "__import__", "getattr", "setattr",
                                 "delattr", "globals", "locals", "vars", "open", "input", "breakpoint"}
                    io_methods = {"open", "read_text", "read_bytes", "write_text", "write_bytes",
                                  "mkdir", "unlink", "system", "popen", "connect", "urlopen"}
                    if (isinstance(node.func, ast.Name) and node.func.id in dangerous) or (
                        isinstance(node.func, ast.Attribute) and node.func.attr in io_methods
                    ):
                        raise SystemExit(f"Unexpected executable or IO capability in {relative}")
                    if isinstance(node.func, ast.Name) and node.func.id == "_read_source":
                        if relative not in STEP3_MAPPING or not any(
                            isinstance(fn, ast.FunctionDef) and fn.name == "load_mapping"
                            and any(child is node for child in ast.walk(fn)) for fn in tree.body
                        ):
                            raise SystemExit(f"Unexpected file read outside explicit mapping loader in {relative}")
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
            if relative in STEP1_CORE | STEP2_IO | STEP3_MAPPING | STEP4_ROWS:
                unexpected = imports - ALLOWED_CORE_IMPORTS[relative]
                if unexpected:
                    raise SystemExit(f"Import outside Step 6 contracts in {relative}: {sorted(unexpected)}")

    if forbidden_locations:
        raise SystemExit(f"Dependency outside the approved scope: {forbidden_locations}")

    print(f"package modules checked: {len(paths)}")
    print(f"allowed startup functions: {sorted(ALLOWED_FUNCTIONS['cli.py'])}")
    print(f"authorized Step 2 contract modules: {sorted(STEP1_CORE)}")
    print(f"authorized Step 2 file modules: {sorted(STEP2_IO)}")
    print(f"authorized Step 3 mapping modules: {sorted(STEP3_MAPPING)}")
    print(f"authorized Step 4 row modules: {sorted(STEP4_ROWS)}")
    print(f"protected docstring-only modules: {placeholder_count}")
    print("owner metadata: PASS")
    print("Step 6 definition and import allowlists: PASS")
    print("no-algorithm phase boundary: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
