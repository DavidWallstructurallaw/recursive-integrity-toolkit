"""Check inherited Phase 2 rules and approved Phase 3 Step 8 boundaries.

The Theory Owner authorized synchronized checker maintenance for each explicitly
approved Phase 2 step on 2026-09-16. Step 9 adds explicit local bundle orchestration only. Earlier
validation and explicit local content-read definitions stay intact.
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
STEP8_OBSERVABILITY = {"observability/levels.py"}
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
        "FileInventoryEntry", "InputSource", "LoadedTable", "FileRole",
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
        "..config", "..models", "..errors", "..utils.hashing", ".loaders", "__future__",
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

# Step 7 opens no new module. Content paths and explicit reads stay in IO helpers.
ALLOWED_FUNCTIONS["utils/paths.py"].update({
    "_content_error", "_content_lexical", "_content_base", "_inside_base",
    "resolve_content_reference", "_open_content_fd",
})
ALLOWED_FUNCTIONS["io/loaders.py"].add("load_content_reference")
ALLOWED_CORE_IMPORTS["utils/paths.py"].add("stat")

# Step 8 opens exactly one classifier. No analytical or IO permission is added.
ALLOWED_FUNCTIONS["observability/levels.py"] = {
    "_invalid", "_cap", "_records", "_row_key", "_content_keys", "_representation",
    "_content_capability", "_provenance_capability", "_lineage_capability",
    "_compatibility", "_longitudinal_capability", "_distribution",
    "_scenario_capability", "classify_observability",
}
ALLOWED_CLASSES["models.py"].add("ScenarioParameters")
ALLOWED_CORE_IMPORTS["observability/levels.py"] = {
    "__future__", "math", "types", "..config", "..errors", "..io.validation", "..models",
}


# Step 9 delegates to existing input layers. Exact call sites keep all reads
# within explicit invocation; no eager orchestration or later-layer permission.
ALLOWED_FUNCTIONS["io/validation.py"].update({
    "_bundle_source", "_bundle_source_key", "_bundle_control", "_bundle_plain",
    "_bundle_document", "_bundle_setup", "_bundle_incomplete_provenance",
    "_bundle_table", "_bundle_order", "_bundle_message_key", "_bundle_messages",
    "_bundle_error_message", "validate_bundle", "_bundle_row_key", "_bundle_inventory_key",
})
ALLOWED_FUNCTIONS["models.py"].add("BundleValidationResult.has_errors")
ALLOWED_CLASSES["models.py"].update({"RowMappingEvidence", "BundleValidationResult"})
ALLOWED_CORE_IMPORTS["io/validation.py"].update({
    "pathlib", "dataclasses", "tomllib", "..config", "..utils.paths", "..utils.hashing",
    ".loaders", ".normalization", ".schema_mapping", "..observability.levels",
})
PIPELINE_CALL_SITES = {
    "_read_source": {"_bundle_control"},
    "load_table": {"_bundle_table"},
    "inventory_source": {"validate_bundle"},
    "load_content_reference": {"validate_bundle"},
    "parse_mapping_json": {"validate_bundle"},
    "map_row": {"_bundle_table"},
    "normalize_row": {"_bundle_table"},
    "classify_observability": {"validate_bundle"},
    "_bundle_control": {"_bundle_setup", "validate_bundle"},
    "_bundle_table": {"validate_bundle"},
    "_bundle_setup": {"validate_bundle"},
    "validate_bundle": set(),
}
PIPELINE_IMPORT_NAMES = {
    ".loaders": {"_limits", "_read_source", "_select_format", "_text", "_check_depth",
                 "_finite_float", "_reject_constant", "_unique_object", "load_table",
                 "inventory_source", "load_content_reference"},
    ".normalization": {"_field_value", "_input", "_policy", "_state", "normalize_row"},
    ".schema_mapping": {"map_row", "parse_mapping_json"},
    "..observability.levels": {"classify_observability"},
}

# Preserve every import and file restriction from the Phase 1 checker.
FORBIDDEN_IMPORTS = {
    "numpy", "pandas", "pyarrow", "networkx", "scipy", "sklearn", "torch",
    "tensorflow", "transformers",
}
FORBIDDEN_FILES = {"collapse_score.py", "integrity_score.py", "universal_score.py"}



# Phase 3 Step 1: declarations and validation contracts only.
PHASE3_ACTIVE_STEP = 11
PHASE3_CONTRACT_CLASSES = {
    "CalculationEvidenceClass", "CalculationStatus", "CalculationReason", "NumericalPolicy",
    "RepresentationDescriptor", "RecordStateAssignment", "CalculationScope", "WeightingOptions",
    "TailSelectionOptions", "CalculationMetadata", "ScalarCalculation", "ExplicitPairContext",
    "ClosedResamplingMetadata",
}
PHASE3_CONTRACT_FUNCTIONS = {
    "_calculation_text", "_calculation_strings", "_calculation_integer", "_calculation_number",
    "NumericalPolicy.__post_init__", "RepresentationDescriptor.__post_init__",
    "RecordStateAssignment.__post_init__", "CalculationScope.__post_init__",
    "WeightingOptions.__post_init__", "TailSelectionOptions.__post_init__",
    "CalculationMetadata.__post_init__", "ScalarCalculation.__post_init__",
    "ExplicitPairContext.__post_init__", "ClosedResamplingMetadata.__post_init__",
}
ALLOWED_FUNCTIONS["models.py"].update(PHASE3_CONTRACT_FUNCTIONS)
ALLOWED_CLASSES["models.py"].update(PHASE3_CONTRACT_CLASSES)
ALLOWED_CORE_IMPORTS["models.py"].add("math")


# Step 2 opens only literal-field representation, not any mathematical metric.
PHASE3_FIELD_MODULES = {"representations/base.py", "representations/field.py"}
ALLOWED_FUNCTIONS["representations/base.py"] = {
    "RepresentationResult.selected_count", "RepresentationResult.included_count",
    "RepresentationResult.excluded_count", "RepresentationProtocol.__call__",
    "_representation_error", "_literal_text", "_selected_records", "_selected_key",
}
ALLOWED_CLASSES["representations/base.py"] = {
    "RepresentationSelection", "RepresentationResult", "RepresentationProtocol",
}
ALLOWED_FUNCTIONS["representations/field.py"] = {
    "_selection", "select_field_representation", "assign_field_states",
}
REPRESENTATION_IMPORT_NAMES = {
    "representations/base.py": {
        "__future__": {"annotations"}, "dataclasses": {"dataclass", "field"},
        "types": {"MappingProxyType"}, "typing": {"Protocol"}, "..config": {"RepresentationConfig"},
        "..errors": {"CanonicalValidationError", "ErrorCode"}, "..io.validation": {"validate_canonical_values"},
        "..models": {"CalculationReason", "CalculationScope", "CalculationStatus", "CanonicalRow",
                     "FileRole", "RecordKey", "RecordStateAssignment", "RepresentationDescriptor",
                     "RowLocation", "ValidationCoverage", "ValidationMessage"},
    },
    "representations/field.py": {
        "__future__": {"annotations"}, "..config": {"RepresentationConfig"},
        "..errors": {"ErrorCode", "WarningCode"},
        "..models": {"CalculationReason", "CalculationScope", "CalculationStatus", "CanonicalRow",
                     "RecordKey", "RecordStateAssignment", "RepresentationDescriptor",
                     "ValidationCoverage", "ValidationMessage", "ValidationSeverity"},
        ".base": {"RepresentationResult", "RepresentationSelection", "_literal_text",
                  "_representation_error", "_selected_records"},
    },
}
ALLOWED_CORE_IMPORTS["representations/base.py"] = set(REPRESENTATION_IMPORT_NAMES["representations/base.py"])
ALLOWED_CORE_IMPORTS["representations/field.py"] = set(REPRESENTATION_IMPORT_NAMES["representations/field.py"])


def _phase3_representation_boundary(tree: ast.Module, relative: str) -> None:
    """Reject hidden computation, I/O, aliases and user callback execution."""
    direct_calls = {
        "representations/base.py": {
            "dataclass", "field", "len", "type", "bool", "any", "set", "tuple", "dict", "sorted", "str",
            "CanonicalValidationError", "RowLocation", "_representation_error", "_literal_text",
            "validate_canonical_values",
        },
        "representations/field.py": {
            "type", "any", "len", "tuple", "sorted", "_representation_error", "_literal_text",
            "_selected_records", "_selection", "RepresentationDescriptor", "RepresentationSelection",
            "ValidationMessage", "RecordStateAssignment", "CalculationScope",
            "RepresentationResult", "ValidationCoverage",
        },
    }
    method_calls = {
        "representations/base.py": {("value", "encode"), ("version", "strip"),
                                    ("seen", "add"), ("loaded", "add"), ("selected", "append")},
        "representations/field.py": {("values", "get"), ("value", "encode"),
                                     ("assignments", "append"), ("states", "append"),
                                     ("included", "append"), ("excluded", "append")},
    }
    for top in tree.body:
        doc = (isinstance(top, ast.Expr) and isinstance(top.value, ast.Constant)
               and isinstance(top.value.value, str))
        if not doc and not isinstance(top, (ast.ImportFrom, ast.FunctionDef, ast.ClassDef)):
            raise SystemExit("Unexpected eager representation operation")
    for node in ast.walk(tree):
        if isinstance(node, (ast.Lambda, ast.AsyncFunctionDef, ast.Await, ast.Yield, ast.YieldFrom)):
            raise SystemExit("Unexpected callback in field representations")
        if isinstance(node, ast.Import):
            raise SystemExit("Import must use exact representation symbols")
        if isinstance(node, ast.ImportFrom):
            module = "." * node.level + (node.module or "")
            allowed = REPRESENTATION_IMPORT_NAMES[relative].get(module, set())
            if any(a.name not in allowed or a.asname is not None for a in node.names):
                raise SystemExit("Import symbol outside representation scope")
        if isinstance(node, ast.BinOp):
            difference = (relative == "representations/base.py" and isinstance(node.op, ast.Sub)
                          and isinstance(node.left, ast.Call) and isinstance(node.left.func, ast.Name)
                          and node.left.func.id == "set" and len(node.left.args) == 1
                          and isinstance(node.left.args[0], ast.Name) and node.left.args[0].id == "dataset_versions"
                          and isinstance(node.right, ast.Name) and node.right.id == "loaded")
            if not isinstance(node.op, ast.BitOr) and not difference:
                raise SystemExit("Unexpected metric arithmetic in representations")
        if isinstance(node, ast.Call):
            direct = isinstance(node.func, ast.Name) and node.func.id in direct_calls[relative]
            method = (isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name)
                      and (node.func.value.id, node.func.attr) in method_calls[relative])
            if not direct and not method:
                raise SystemExit("Unexpected call in pure field representations")



# Step 3 opens only exact record-form states and PR-006 duplicate counts.
PHASE3_EXACT_MODULES = {"representations/content_hash.py", "metrics/duplicates.py"}
ALLOWED_FUNCTIONS["representations/content_hash.py"] = {
    "exact_content_bytes", "_payload_snapshot", "assign_content_states",
}
ALLOWED_CLASSES["representations/content_hash.py"] = {"ExactContentRepresentation"}
ALLOWED_FUNCTIONS["metrics/duplicates.py"] = {
    "ExactDuplicateGroup.representative", "ExactDuplicateGroup.record_count", "detect_exact_duplicates",
}
ALLOWED_CLASSES["metrics/duplicates.py"] = {"ExactDuplicateGroup", "ExactDuplicateResult"}
EXACT_IMPORT_NAMES = {
    "representations/content_hash.py": {
        "__future__": {"annotations"}, "dataclasses": {"dataclass", "field"},
        "types": {"MappingProxyType"}, "..errors": {"ErrorCode"},
        "..models": {"CalculationReason", "CalculationScope", "CalculationStatus", "CanonicalRow",
                     "ContentMode", "RecordKey", "RecordStateAssignment", "RepresentationDescriptor", "ValidationCoverage"},
        "..utils.hashing": {"sha256_bytes"},
        ".base": {"RepresentationResult", "RepresentationSelection", "_literal_text",
                  "_representation_error", "_selected_records"},
    },
    "metrics/duplicates.py": {
        "__future__": {"annotations"}, "dataclasses": {"dataclass", "field"},
        "..models": {"CalculationEvidenceClass", "CalculationMetadata", "CalculationScope", "CalculationStatus",
                     "CanonicalRow", "ContentMode", "RecordKey", "RepresentationDescriptor", "ScalarCalculation",
                     "ValidationCoverage"},
        "..representations.content_hash": {"assign_content_states"},
    },
}
for _exact_module, _exact_imports in EXACT_IMPORT_NAMES.items():
    ALLOWED_CORE_IMPORTS[_exact_module] = set(_exact_imports)


def _phase3_exact_boundary(tree: ast.Module, relative: str) -> None:
    """Exact imports and calls; only PR-006 counting arithmetic is admitted."""
    direct_calls = {
        "representations/content_hash.py": {
            "dataclass", "field", "type", "len", "set", "tuple", "_literal_text", "_representation_error",
            "_selected_records", "_payload_snapshot", "exact_content_bytes", "sha256_bytes",
            "RepresentationDescriptor", "RepresentationSelection", "RepresentationResult",
            "RecordStateAssignment", "CalculationScope", "ValidationCoverage", "ExactContentRepresentation",
        },
        "metrics/duplicates.py": {
            "dataclass", "field", "assign_content_states", "sorted", "tuple", "len",
            "ExactDuplicateGroup", "CalculationMetadata", "ScalarCalculation", "ExactDuplicateResult",
        },
    }
    methods = {
        "representations/content_hash.py": {
            ("text", "strip"), ("text", "encode"), ("resolved_content", "items"),
            ("assignments", "append"), ("snapshots", "append"), ("keys", "append"), ("states", "append"),
        },
        "metrics/duplicates.py": {
            ("members", "setdefault"), ("bucket", "append"), ("groups", "append"), ("counts", "append"),
        },
    }
    expected_subtractions = {
        "representations/content_hash.py": {ast.dump(ast.parse(expr, mode="eval").body) for expr in
                                             ("set(payloads) - selected_keys", "selected_keys - set(payloads)")},
        "metrics/duplicates.py": {ast.dump(ast.parse("len(keys) - 1", mode="eval").body)},
    }
    for top in tree.body:
        doc = (isinstance(top, ast.Expr) and isinstance(top.value, ast.Constant)
               and isinstance(top.value.value, str))
        if not doc and not isinstance(top, (ast.ImportFrom, ast.FunctionDef, ast.ClassDef)):
            raise SystemExit("Unexpected eager exact-content operation")
    for node in ast.walk(tree):
        if isinstance(node, (ast.Lambda, ast.AsyncFunctionDef, ast.Await, ast.Yield, ast.YieldFrom, ast.Import)):
            raise SystemExit("Unexpected dynamic or import operation in exact-content scope")
        if isinstance(node, ast.ImportFrom):
            module = "." * node.level + (node.module or "")
            allowed = EXACT_IMPORT_NAMES[relative].get(module, set())
            if any(a.name not in allowed or a.asname is not None for a in node.names):
                raise SystemExit("Import symbol outside exact-content scope")
        if isinstance(node, ast.BinOp) and not isinstance(node.op, ast.BitOr):
            if ast.dump(node) not in expected_subtractions[relative]:
                raise SystemExit("Unexpected arithmetic outside exact duplicate definitions")
        if isinstance(node, ast.AugAssign):
            expected = ast.parse("duplicates += len(keys) - 1").body[0]
            if relative != "metrics/duplicates.py" or ast.dump(node) != ast.dump(expected):
                raise SystemExit("Unexpected augmented arithmetic outside PR-006")
        if isinstance(node, ast.Call):
            direct = isinstance(node.func, ast.Name) and node.func.id in direct_calls[relative]
            method = (isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name)
                      and (node.func.value.id, node.func.attr) in methods[relative])
            if not direct and not method:
                raise SystemExit("Unexpected call in pure exact-content scope")



# Step 4 opens only the reviewed single-scope F-001 through F-004 kernels.
PHASE3_DISTRIBUTION_MODULES = {"metrics/diversity.py"}
ALLOWED_FUNCTIONS["metrics/diversity.py"] = {
    "_invalid", "_text", "_key", "_context", "_number", "_pairs", "_probabilities",
    "_metadata", "_metrics", "distribution_from_counts", "distribution_from_probabilities",
    "_assignments", "_weights", "calculate_state_distribution",
}
ALLOWED_CLASSES["metrics/diversity.py"] = {"StateFrequency", "DistributionMetrics", "StateDistributionResult"}
ALLOWED_CORE_IMPORTS["metrics/diversity.py"] = {
    "__future__", "dataclasses", "math", "types", "..errors", "..models", "..representations.base",
}
DISTRIBUTION_SOURCE_SHA256 = "34b1b77d00b9a2169aa7680d0edf77b05d5aec0bdc26b3bd141d38853f9728a9"


def _phase3_distribution_boundary(tree: ast.Module) -> None:
    """Pin the Step 9 additive body and compare in this interpreter, not across AST formats."""
    import hashlib
    raw = (PACKAGE / "metrics/diversity.py").read_bytes()
    if hashlib.sha256(raw).hexdigest() != DISTRIBUTION_SOURCE_SHA256:
        raise SystemExit("Unexpected distribution source outside the reviewed Step 9 body")
    if ast.dump(tree, include_attributes=False) != ast.dump(ast.parse(raw), include_attributes=False):
        raise SystemExit("Unexpected distribution AST outside the reviewed Step 9 body")


ALLOWED_FUNCTIONS["metrics/diversity.py"].update({'_pair_distribution', '_pair_scalar_check', 'compare_support', '_pair_metadata_check', '_pair_metadata', '_harmonize_distribution'})
ALLOWED_CLASSES["metrics/diversity.py"].update({'SupportComparison'})
ALLOWED_CORE_IMPORTS["metrics/diversity.py"].add("..representations.compatibility")


# Step 5 opens only declared provenance composition and direct classification.
PHASE3_PROVENANCE_MODULES = {"metrics/provenance.py"}
ALLOWED_FUNCTIONS["metrics/provenance.py"] = set(['_checked_join', '_composition', '_direct', '_invalid', '_key', '_keys', '_messages', '_metadata', '_scalar', '_text', '_weighted', '_weights', 'classify_direct_grounding', 'summarize_provenance'])
ALLOWED_CLASSES["metrics/provenance.py"] = set(['DeclaredComposition', 'DirectGroundingAssignment', 'DirectGroundingBasis', 'ProvenanceCompositionResult', 'WeightedSourceComposition'])
ALLOWED_CORE_IMPORTS["metrics/provenance.py"] = {
    "__future__", "dataclasses", "math", "types", "..errors", "..models", "..io.validation",
}
PROVENANCE_AST_SHA256 = "554e40896edf5c0e30432015ad357a82e3b3419b6f7529d4e22a09894b4569c2"


def _phase3_provenance_boundary(tree: ast.Module) -> None:
    """Pin the reviewed Step 5 body, never learn a new body at gate execution.

    Independent rational tests cover mathematics; mutation tests cover change
    control. Only empty Python-version type_params metadata is omitted.
    """
    import hashlib
    for node in ast.walk(tree):
        if "type_params" in node._fields:
            if getattr(node, "type_params", []):
                raise SystemExit("Unexpected generic declaration in provenance metrics")
            node._fields = tuple(name for name in node._fields if name != "type_params")
    try:
        serialized = ast.dump(tree, include_attributes=False, show_empty=True)
    except TypeError:
        serialized = ast.dump(tree, include_attributes=False)
    if hashlib.sha256(serialized.encode("utf-8")).hexdigest() != PROVENANCE_AST_SHA256:
        raise SystemExit("Unexpected provenance implementation outside reviewed Step 5 body")




# Step 6 opens only direct F-009/F-010 bounds, with no lineage branch.
PHASE3_BOUNDS_MODULES = {"metrics/bounds.py"}
ALLOWED_FUNCTIONS["metrics/bounds.py"] = {'_metric', 'closure_exposure_bounds', '_messages', '_confidence', '_text', '_invalid', '_key', '_scope', '_coverage', '_count', '_basis', 'DirectClosureExposureBounds.status', 'direct_closure_exposure', '_observed'}
ALLOWED_CLASSES["metrics/bounds.py"] = {'DirectClosureExposureBounds'}
ALLOWED_CORE_IMPORTS["metrics/bounds.py"] = {"__future__", "dataclasses", "math", "..errors", "..models", ".provenance"}
BOUNDS_SOURCE_SHA256 = "01693a92ab9c0a78cba5addf7bd778fca5d14051599d7878dd682ddc5c9707a4"


def _phase3_bounds_boundary(tree: ast.Module) -> None:
    """Pin reviewed bytes, then compare ASTs in the same interpreter.

    The digest is a reviewed literal. It is never reset from inspected input.
    Both actual file edits and injected executable nodes are rejected.
    """
    import hashlib
    raw = (PACKAGE / "metrics/bounds.py").read_bytes()
    if hashlib.sha256(raw).hexdigest() != BOUNDS_SOURCE_SHA256:
        raise SystemExit("Direct bounds source differs from the reviewed Step 6 body")
    if ast.dump(tree, include_attributes=False) != ast.dump(ast.parse(raw), include_attributes=False):
        raise SystemExit("Unexpected direct bounds executable syntax outside Step 6")


# Step 7 opens only explicit observed-tail diagnostics and analytic F-014.
PHASE3_TAIL_MODULES = {"metrics/tail.py"}
ALLOWED_FUNCTIONS["metrics/tail.py"] = {'_state', '_metadata', 'select_tail', '_distribution', 'one_step_extinction_probability', '_rarity_key', '_invalid', '_options'}
ALLOWED_CLASSES["metrics/tail.py"] = {'TailSelectionResult', 'RarityEntry', 'ExtinctionProbabilityResult'}
ALLOWED_CORE_IMPORTS["metrics/tail.py"] = {"__future__", "dataclasses", "math", "..errors", "..models", ".diversity"}
TAIL_SOURCE_SHA256 = "b7618dea6a28fd69aa951d7ae5170c772bc2bea2999906ed61bca9079b8d5cf7"


def _phase3_tail_boundary(tree: ast.Module) -> None:
    """Fixed reviewed bytes and same-interpreter syntax; no later T2 behaviors."""
    import hashlib
    raw = (PACKAGE / "metrics/tail.py").read_bytes()
    if hashlib.sha256(raw).hexdigest() != TAIL_SOURCE_SHA256:
        raise SystemExit("Tail source differs from the reviewed Step 7 body")
    if ast.dump(tree, include_attributes=False) != ast.dump(ast.parse(raw), include_attributes=False):
        raise SystemExit("Unexpected tail/scenario executable syntax outside Step 7")


# Step 8 opens only explicit closed resampling, never T5 reopening.
PHASE3_RESAMPLING_MODULES = {"metrics/resampling.py"}
ALLOWED_FUNCTIONS["metrics/resampling.py"] = set(['_diversity', '_generation', '_inputs', '_integer', '_invalid', '_metadata', '_resources', '_sample_counts', '_state', 'expected_diversity_after_steps', 'simulate_closed_resampling'])
ALLOWED_CLASSES["metrics/resampling.py"] = set(['ExpectedDiversityResult', 'ResamplingInput', 'ResamplingReplicate', 'ResamplingSimulation', 'SampledGeneration'])
ALLOWED_CORE_IMPORTS["metrics/resampling.py"] = {"__future__", "dataclasses", "math", "types", "..errors", "..models", ".diversity", "numpy"}
RESAMPLING_SOURCE_SHA256 = "0896b80c26ad0b9865e24957202b54c2ab9217921d1c19e84ab22d84928f2e40"


def _phase3_resampling_boundary(tree: ast.Module) -> None:
    """Fixed reviewed source and exact AST; lazy NumPy only in the sampler."""
    import hashlib
    raw = (PACKAGE / "metrics/resampling.py").read_bytes()
    if hashlib.sha256(raw).hexdigest() != RESAMPLING_SOURCE_SHA256:
        raise SystemExit("Resampling source differs from the reviewed Step 8 body")
    if ast.dump(tree, include_attributes=False) != ast.dump(ast.parse(raw), include_attributes=False):
        raise SystemExit("Unexpected resampling syntax outside Step 8")


def _phase3_contract_boundary(tree: ast.Module) -> None:
    """Reject calculation or execution inside the newly authorized declarations."""
    permitted = {"type", "len", "set", "any", "ValueError", "TypeError", "field", "dataclass",
                 "WeightingOptions", "_calculation_text", "_calculation_strings",
                 "_calculation_integer", "_calculation_number"}
    roots = {name.split(".")[0] for name in PHASE3_CONTRACT_FUNCTIONS} | PHASE3_CONTRACT_CLASSES
    for top in tree.body:
        if not isinstance(top, (ast.FunctionDef, ast.ClassDef)) or top.name not in roots:
            continue
        for node in ast.walk(top):
            if isinstance(node, (ast.Lambda, ast.AsyncFunctionDef, ast.Await, ast.Yield, ast.YieldFrom)):
                raise SystemExit("Unexpected callback in Phase 3 contracts")
            if isinstance(node, ast.BinOp) and not isinstance(node.op, (ast.BitOr, ast.BitAnd)):
                raise SystemExit("Unexpected metric arithmetic in Phase 3 contracts")
            if isinstance(node, ast.Call):
                direct = isinstance(node.func, ast.Name) and node.func.id in permitted
                finite = (isinstance(node.func, ast.Attribute) and node.func.attr == "isfinite"
                          and isinstance(node.func.value, ast.Name) and node.func.value.id == "math"
                          and isinstance(top, ast.FunctionDef) and top.name == "_calculation_number")
                if not (direct or finite):
                    raise SystemExit("Unexpected call in Phase 3 contracts")
    for node in ast.walk(tree):
        if isinstance(node, ast.Import) and any(alias.name == "math" for alias in node.names):
            if len(node.names) != 1 or node.names[0].asname is not None or not any(
                    isinstance(fn, ast.FunctionDef) and fn.name == "_calculation_number"
                    and any(child is node for child in ast.walk(fn)) for fn in tree.body):
                raise SystemExit("Unexpected math import outside finite-type validation")


def _definitions(tree: ast.AST, prefix: str = "") -> tuple[list[str], list[str]]:
    """Collect qualified definitions without executing inspected source."""
    functions: list[str] = []
    classes: list[str] = []
    for node in ast.iter_child_nodes(tree):
        child_prefix = prefix
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            name = f"{prefix}.{node.name}" if prefix else node.name
            if isinstance(node, ast.AsyncFunctionDef):
                raise SystemExit(f"Async implementation is outside Step 8: {name}")
            if isinstance(node, ast.ClassDef):
                classes.append(name)
            else:
                functions.append(name)
            child_prefix = name
        child_functions, child_classes = _definitions(node, child_prefix)
        functions.extend(child_functions)
        classes.extend(child_classes)
    return functions, classes


# Step 9 opens only explicit pair compatibility; no metric dispatch here.
PHASE3_PAIR_MODULES = {"representations/compatibility.py"}
ALLOWED_FUNCTIONS["representations/compatibility.py"] = {'_scope', '_mapping', '_descriptor', 'validate_representation_compatibility', '_invalid', '_context', '_text'}
ALLOWED_CLASSES["representations/compatibility.py"] = {'StateMappingDeclaration', 'RepresentationCompatibility'}
ALLOWED_CORE_IMPORTS["representations/compatibility.py"] = {'..models', 'types', '..io.validation', '..errors', '__future__', 'dataclasses'}
PAIR_SOURCE_SHA256 = "c4ce8e30d8026dd7ac1e10ac09e7b70a23ae2c4fc451f2e37890b919965d4509"


def _phase3_pair_boundary(tree: ast.Module) -> None:
    """Exact reviewed declaration checks; reject source changes and injected bodies."""
    import hashlib
    raw = (PACKAGE / "representations/compatibility.py").read_bytes()
    if hashlib.sha256(raw).hexdigest() != PAIR_SOURCE_SHA256:
        raise SystemExit("Unexpected compatibility source outside reviewed Step 9")
    if ast.dump(tree, include_attributes=False) != ast.dump(ast.parse(raw), include_attributes=False):
        raise SystemExit("Unexpected compatibility AST outside reviewed Step 9")


def main() -> int:
    paths = sorted(PACKAGE.rglob("*.py"))
    if len(paths) != 40:
        raise SystemExit(f"Expected 40 package modules, found {len(paths)}")
    relative_paths = {path.relative_to(PACKAGE).as_posix() for path in paths}
    missing = (BOOTSTRAP | STEP1_CORE | STEP2_IO | STEP3_MAPPING | STEP4_ROWS | STEP8_OBSERVABILITY | PHASE3_FIELD_MODULES | PHASE3_EXACT_MODULES | PHASE3_DISTRIBUTION_MODULES | PHASE3_PROVENANCE_MODULES | PHASE3_BOUNDS_MODULES | PHASE3_TAIL_MODULES | PHASE3_RESAMPLING_MODULES | PHASE3_PAIR_MODULES) - relative_paths
    if missing:
        raise SystemExit(f"Required startup or Step 8 modules missing: {sorted(missing)}")

    imported_roots: set[str] = set()
    forbidden_locations: list[str] = []
    placeholder_count = 0

    for path in paths:
        relative = path.relative_to(PACKAGE).as_posix()
        if path.name in FORBIDDEN_FILES:
            raise SystemExit(f"Forbidden module found: {path}")
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        if relative == "models.py":
            _phase3_contract_boundary(tree)
        if relative in PHASE3_FIELD_MODULES:
            _phase3_representation_boundary(tree, relative)
        if relative in PHASE3_EXACT_MODULES:
            _phase3_exact_boundary(tree, relative)
        if relative in PHASE3_DISTRIBUTION_MODULES:
            _phase3_distribution_boundary(tree)
        if relative in PHASE3_PROVENANCE_MODULES:
            _phase3_provenance_boundary(tree)
        if relative in PHASE3_BOUNDS_MODULES:
            _phase3_bounds_boundary(tree)
        if relative in PHASE3_TAIL_MODULES:
            _phase3_tail_boundary(tree)
        if relative in PHASE3_RESAMPLING_MODULES:
            _phase3_resampling_boundary(tree)
        if relative in PHASE3_PAIR_MODULES:
            _phase3_pair_boundary(tree)
        doc = ast.get_docstring(tree) or ""
        if "Owner IDs:" not in doc or "Current phase status:" not in doc:
            raise SystemExit(f"Owner or phase metadata missing: {path}")

        if relative not in BOOTSTRAP | STEP1_CORE | STEP2_IO | STEP3_MAPPING | STEP4_ROWS | STEP8_OBSERVABILITY | PHASE3_FIELD_MODULES | PHASE3_EXACT_MODULES | PHASE3_DISTRIBUTION_MODULES | PHASE3_PROVENANCE_MODULES | PHASE3_BOUNDS_MODULES | PHASE3_TAIL_MODULES | PHASE3_RESAMPLING_MODULES | PHASE3_PAIR_MODULES:
            if not (
                len(tree.body) == 1
                and isinstance(tree.body[0], ast.Expr)
                and isinstance(tree.body[0].value, ast.Constant)
                and isinstance(tree.body[0].value.value, str)
            ):
                raise SystemExit(f"Protected non-Step-8 executable body found: {path}")
            placeholder_count += 1
        else:
            functions, classes = _definitions(tree)
            if set(functions) != ALLOWED_FUNCTIONS[relative] or len(functions) != len(set(functions)):
                raise SystemExit(f"Unexpected Step 9 functions in {relative}: {functions}")
            if set(classes) != ALLOWED_CLASSES.get(relative, set()) or len(classes) != len(set(classes)):
                raise SystemExit(f"Unexpected Step 9 classes in {relative}: {classes}")

        for node in ast.walk(tree):
            if relative == "io/validation.py":
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in PIPELINE_CALL_SITES:
                    if not any(isinstance(fn, ast.FunctionDef) and fn.name in PIPELINE_CALL_SITES[node.func.id]
                               and any(child is node for child in ast.walk(fn)) for fn in tree.body):
                        raise SystemExit(f"Unexpected bundle read or orchestration call site: {node.func.id}")
                if isinstance(node, ast.ImportFrom):
                    imported_path = "." * node.level + (node.module or "")
                    if imported_path in PIPELINE_IMPORT_NAMES:
                        if any(alias.name not in PIPELINE_IMPORT_NAMES[imported_path] or alias.asname is not None for alias in node.names):
                            raise SystemExit(f"Unexpected adjacent-layer import in {relative}")
                        if not any(isinstance(fn, ast.FunctionDef) and fn.name in ALLOWED_FUNCTIONS["io/validation.py"]
                                   and (fn.name.startswith("_bundle_") or fn.name == "validate_bundle")
                                   and any(child is node for child in ast.walk(fn)) for fn in tree.body):
                            raise SystemExit(f"Unexpected eager adjacent-layer import in {relative}")
            if relative in STEP8_OBSERVABILITY:
                if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Mult, ast.Div, ast.FloorDiv, ast.Mod, ast.Pow, ast.MatMult)):
                    raise SystemExit(f"Unexpected analytical arithmetic in {relative}")
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name) and node.func.value.id == "math":
                    if node.func.attr not in {"isfinite", "fsum", "isclose"} or not any(
                        isinstance(fn, ast.FunctionDef) and fn.name == "_distribution"
                        and any(child is node for child in ast.walk(fn)) for fn in tree.body
                    ):
                        raise SystemExit(f"Unexpected math use outside input validation in {relative}")
            if relative in STEP2_IO:
                if isinstance(node, ast.Lambda):
                    raise SystemExit(f"Unexpected dynamic callback in {relative}")
                if isinstance(node, ast.Call):
                    blocked_calls = {"eval", "exec", "compile", "__import__", "globals", "locals", "vars", "input", "breakpoint"}
                    blocked_methods = {"write_text", "write_bytes", "mkdir", "unlink", "remove", "system", "popen", "connect", "urlopen", "urlretrieve", "send", "sendall"}
                    if (isinstance(node.func, ast.Name) and node.func.id in blocked_calls) or (
                        isinstance(node.func, ast.Attribute) and node.func.attr in blocked_methods
                    ):
                        raise SystemExit(f"Unexpected executable, write or network capability in {relative}")
            if relative in STEP3_MAPPING | STEP4_ROWS | STEP8_OBSERVABILITY | PHASE3_FIELD_MODULES | PHASE3_EXACT_MODULES | PHASE3_DISTRIBUTION_MODULES | PHASE3_PROVENANCE_MODULES | PHASE3_BOUNDS_MODULES | PHASE3_TAIL_MODULES | PHASE3_RESAMPLING_MODULES | PHASE3_PAIR_MODULES | {"models.py"}:
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
                        if not ((relative in STEP3_MAPPING and any(
                            isinstance(fn, ast.FunctionDef) and fn.name == "load_mapping"
                            and any(child is node for child in ast.walk(fn)) for fn in tree.body
                        )) or (relative == "io/validation.py" and any(
                            isinstance(fn, ast.FunctionDef) and fn.name == "_bundle_control"
                            and any(child is node for child in ast.walk(fn)) for fn in tree.body
                        ))):
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
                    lazy_numpy = (
                        relative == "metrics/resampling.py" and imported == "numpy"
                        and isinstance(node, ast.Import)
                        and len(node.names) == 1 and node.names[0].name == "numpy" and node.names[0].asname == "np"
                        and any(isinstance(fn, ast.FunctionDef) and fn.name == "simulate_closed_resampling"
                                and any(child is node for child in ast.walk(fn)) for fn in tree.body)
                    )
                    if not (lazy_parquet or lazy_numpy):
                        forbidden_locations.append(f"{relative}: {imported}")
            if relative in STEP1_CORE | STEP2_IO | STEP3_MAPPING | STEP4_ROWS | STEP8_OBSERVABILITY | PHASE3_FIELD_MODULES | PHASE3_EXACT_MODULES | PHASE3_DISTRIBUTION_MODULES | PHASE3_PROVENANCE_MODULES | PHASE3_BOUNDS_MODULES | PHASE3_TAIL_MODULES | PHASE3_RESAMPLING_MODULES | PHASE3_PAIR_MODULES:
                unexpected = imports - ALLOWED_CORE_IMPORTS[relative]
                if unexpected:
                    raise SystemExit(f"Import outside Step 9 contracts in {relative}: {sorted(unexpected)}")

    if forbidden_locations:
        raise SystemExit(f"Dependency outside the approved scope: {forbidden_locations}")

    print(f"package modules checked: {len(paths)}")
    print(f"allowed startup functions: {sorted(ALLOWED_FUNCTIONS['cli.py'])}")
    print(f"authorized Step 2 contract modules: {sorted(STEP1_CORE)}")
    print(f"authorized Step 2 file modules: {sorted(STEP2_IO)}")
    print(f"authorized Step 3 mapping modules: {sorted(STEP3_MAPPING)}")
    print(f"authorized Step 4 row modules: {sorted(STEP4_ROWS)}")
    print(f"authorized Step 8 observability modules: {sorted(STEP8_OBSERVABILITY)}")
    print(f"protected docstring-only modules: {placeholder_count}")
    print("owner metadata: PASS")
    print("Phase 3 Step 11: retained Step 9 explicit-pair and inherited definition/import boundaries: PASS")
    print("no-algorithm phase boundary: PASS")
    return 0


def phase4_main(step: int = 1) -> int:
    """Apply the approved Step 1 control before the frozen Phase 3 AST gate."""
    import runpy

    if type(step) is not int or step != 1:
        raise ValueError("Only authorized Phase 4 Step 1 traceability is available")
    control = runpy.run_path(str(ROOT / "scripts/release_check.py"),
                            run_name="phase4_traceability_control")
    control["audit_phase4"](step=step)
    result = main()
    print("Phase 4 Step 1: approved governance and frozen Phase 3 traceability: PASS")
    return result


PHASE4_STEP2_REPORT_SCHEMA_SHA256 = "34b7edb8e8672fca3f3d4f6fe647b4d8967acb6f0435544ba449c1c44f7bc1f6"
PHASE4_STEP2_RESULT_IMPORTS = ["Import(names=[alias(name='math')])",
 "Import(names=[alias(name='re')])",
 "Import(names=[alias(name='sys')])",
 "ImportFrom(module='__future__', names=[alias(name='annotations')], level=0)",
 "ImportFrom(module='collections.abc', names=[alias(name='Mapping')], level=0)",
 "ImportFrom(module='dataclasses', names=[alias(name='dataclass')], level=0)",
 "ImportFrom(module='enum', names=[alias(name='StrEnum')], level=0)",
 "ImportFrom(module='types', names=[alias(name='MappingProxyType')], level=0)"]
PHASE4_STEP2_RESULT_FUNCTIONS = ['CanonicalReport.__init__',
 'CanonicalReport.from_dict',
 'CanonicalReport.to_dict',
 '_array',
 '_base_envelope',
 '_build_contract',
 '_check',
 '_check_nullable_reason',
 '_enum',
 '_equality_key',
 '_fail',
 '_field',
 '_freeze',
 '_integer',
 '_json_input',
 '_map',
 '_matches',
 '_metric',
 '_nullable',
 '_number',
 '_object',
 '_observed',
 '_ref',
 '_resolved_contract',
 '_same',
 '_semantic_checks',
 '_strings',
 '_text',
 '_thaw',
 '_walk',
 'report_schema',
 'validate_report']
PHASE4_STEP2_RESULT_CLASSES = ['CanonicalReport',
 'ExecutionStatus',
 'FieldDefinition',
 'ReportEvidenceClass',
 'ReportStatus',
 'ReportValidationError',
 'RunStatus']
PHASE4_STEP2_RESULT_CALLS = {'<module>': ['_build_contract', '_freeze', 'tuple'],
 'CanonicalReport': ['dataclass'],
 'CanonicalReport.__init__': ['MappingProxyType',
                              'MappingProxyType',
                              '_freeze',
                              'object.__setattr__',
                              'validate_report'],
 'CanonicalReport.from_dict': ['CanonicalReport'],
 'CanonicalReport.to_dict': ['_thaw'],
 'FieldDefinition': ['dataclass'],
 '_base_envelope': ['_array',
                    '_array',
                    '_enum',
                    '_enum',
                    '_enum',
                    '_nullable',
                    '_nullable',
                    '_nullable',
                    '_nullable',
                    '_nullable',
                    '_number',
                    '_number',
                    '_ref',
                    '_ref',
                    '_strings',
                    '_strings',
                    '_strings',
                    '_strings',
                    '_text',
                    '_text'],
 '_build_contract': ['FieldDefinition',
                     'FieldDefinition',
                     'FieldDefinition',
                     'FieldDefinition',
                     '_array',
                     '_array',
                     '_array',
                     '_array',
                     '_array',
                     '_array',
                     '_array',
                     '_array',
                     '_array',
                     '_array',
                     '_array',
                     '_array',
                     '_array',
                     '_array',
                     '_array',
                     '_array',
                     '_array',
                     '_array',
                     '_array',
                     '_array',
                     '_array',
                     '_array',
                     '_array',
                     '_array',
                     '_array',
                     '_array',
                     '_array',
                     '_array',
                     '_array',
                     '_array',
                     '_array',
                     '_array',
                     '_array',
                     '_array',
                     '_array',
                     '_array',
                     '_array',
                     '_array',
                     '_array',
                     '_array',
                     '_array',
                     '_array',
                     '_array',
                     '_array',
                     '_array',
                     '_array',
                     '_array',
                     '_array',
                     '_array',
                     '_array',
                     '_base_envelope',
                     '_base_envelope',
                     '_base_envelope',
                     '_enum',
                     '_enum',
                     '_enum',
                     '_enum',
                     '_enum',
                     '_enum',
                     '_enum',
                     '_enum',
                     '_enum',
                     '_enum',
                     '_enum',
                     '_enum',
                     '_enum',
                     '_enum',
                     '_enum',
                     '_enum',
                     '_enum',
                     '_enum',
                     '_enum',
                     '_enum',
                     '_enum',
                     '_enum',
                     '_enum',
                     '_enum',
                     '_enum',
                     '_enum',
                     '_enum',
                     '_enum',
                     '_field_entries.append',
                     '_field_entries.append',
                     '_field_entries.append',
                     '_field_entries.append',
                     '_integer',
                     '_integer',
                     '_integer',
                     '_integer',
                     '_integer',
                     '_integer',
                     '_integer',
                     '_integer',
                     '_integer',
                     '_integer',
                     '_integer',
                     '_integer',
                     '_integer',
                     '_integer',
                     '_integer',
                     '_integer',
                     '_integer',
                     '_integer',
                     '_integer',
                     '_integer',
                     '_integer',
                     '_integer',
                     '_integer',
                     '_integer',
                     '_integer',
                     '_integer',
                     '_integer',
                     '_integer',
                     '_integer',
                     '_integer',
                     '_integer',
                     '_integer',
                     '_integer',
                     '_integer',
                     '_integer',
                     '_integer',
                     '_integer',
                     '_integer',
                     '_integer',
                     '_integer',
                     '_integer',
                     '_integer',
                     '_integer',
                     '_integer',
                     '_integer',
                     '_integer',
                     '_integer',
                     '_integer',
                     '_integer',
                     '_integer',
                     '_integer',
                     '_map',
                     '_map',
                     '_map',
                     '_map',
                     '_map',
                     '_map',
                     '_metric',
                     '_metric',
                     '_metric',
                     '_metric',
                     '_metric',
                     '_metric',
                     '_metric',
                     '_metric',
                     '_metric',
                     '_metric',
                     '_metric',
                     '_metric',
                     '_metric',
                     '_metric',
                     '_metric',
                     '_metric',
                     '_nullable',
                     '_nullable',
                     '_nullable',
                     '_nullable',
                     '_nullable',
                     '_nullable',
                     '_nullable',
                     '_nullable',
                     '_nullable',
                     '_nullable',
                     '_nullable',
                     '_nullable',
                     '_nullable',
                     '_nullable',
                     '_nullable',
                     '_nullable',
                     '_nullable',
                     '_nullable',
                     '_nullable',
                     '_nullable',
                     '_nullable',
                     '_nullable',
                     '_nullable',
                     '_nullable',
                     '_nullable',
                     '_nullable',
                     '_nullable',
                     '_nullable',
                     '_nullable',
                     '_nullable',
                     '_nullable',
                     '_nullable',
                     '_nullable',
                     '_nullable',
                     '_nullable',
                     '_nullable',
                     '_nullable',
                     '_nullable',
                     '_nullable',
                     '_nullable',
                     '_nullable',
                     '_nullable',
                     '_nullable',
                     '_nullable',
                     '_nullable',
                     '_nullable',
                     '_nullable',
                     '_nullable',
                     '_nullable',
                     '_nullable',
                     '_nullable',
                     '_nullable',
                     '_nullable',
                     '_nullable',
                     '_nullable',
                     '_number',
                     '_number',
                     '_number',
                     '_number',
                     '_number',
                     '_number',
                     '_number',
                     '_number',
                     '_number',
                     '_number',
                     '_number',
                     '_number',
                     '_number',
                     '_number',
                     '_number',
                     '_number',
                     '_number',
                     '_number',
                     '_number',
                     '_number',
                     '_number',
                     '_number',
                     '_number',
                     '_number',
                     '_number',
                     '_number',
                     '_number',
                     '_number',
                     '_number',
                     '_number',
                     '_number',
                     '_number',
                     '_number',
                     '_number',
                     '_number',
                     '_number',
                     '_number',
                     '_number',
                     '_number',
                     '_number',
                     '_number',
                     '_number',
                     '_number',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_object',
                     '_observed',
                     '_observed',
                     '_observed',
                     '_observed',
                     '_observed',
                     '_observed',
                     '_observed',
                     '_observed',
                     '_observed',
                     '_observed',
                     '_observed',
                     '_observed',
                     '_ref',
                     '_ref',
                     '_ref',
                     '_ref',
                     '_ref',
                     '_ref',
                     '_ref',
                     '_ref',
                     '_ref',
                     '_ref',
                     '_ref',
                     '_ref',
                     '_ref',
                     '_ref',
                     '_ref',
                     '_ref',
                     '_ref',
                     '_ref',
                     '_ref',
                     '_ref',
                     '_ref',
                     '_ref',
                     '_ref',
                     '_ref',
                     '_ref',
                     '_ref',
                     '_ref',
                     '_ref',
                     '_ref',
                     '_ref',
                     '_ref',
                     '_ref',
                     '_ref',
                     '_ref',
                     '_ref',
                     '_ref',
                     '_ref',
                     '_ref',
                     '_ref',
                     '_strings',
                     '_strings',
                     '_strings',
                     '_strings',
                     '_strings',
                     '_strings',
                     '_strings',
                     '_strings',
                     '_strings',
                     '_strings',
                     '_strings',
                     '_strings',
                     '_strings',
                     '_strings',
                     '_strings',
                     '_strings',
                     '_strings',
                     '_strings',
                     '_strings',
                     '_strings',
                     '_strings',
                     '_strings',
                     '_strings',
                     '_strings',
                     '_strings',
                     '_strings',
                     '_strings',
                     '_strings',
                     '_strings',
                     '_strings',
                     '_strings',
                     '_strings',
                     '_strings',
                     '_strings',
                     '_strings',
                     '_strings',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     '_text',
                     'list',
                     'list',
                     'props.update',
                     'props.update',
                     'props.update',
                     'props.update',
                     'tuple',
                     'unavailable_owners.items',
                     'unavailable_variants.append'],
 '_check': ['_check',
            '_check',
            '_check',
            '_check',
            '_check',
            '_check',
            '_check',
            '_equality_key',
            '_fail',
            '_fail',
            '_fail',
            '_fail',
            '_fail',
            '_fail',
            '_fail',
            '_fail',
            '_fail',
            '_fail',
            '_fail',
            '_fail',
            '_fail',
            '_fail',
            '_fail',
            '_fail',
            '_fail',
            '_fail',
            '_fail',
            '_matches',
            '_matches',
            '_matches',
            '_same',
            '_same',
            'any',
            'any',
            'any',
            'enumerate',
            'isinstance',
            'len',
            'len',
            'len',
            'len',
            'len',
            'len',
            'len',
            'math.isfinite',
            're.search',
            'reference.removeprefix',
            'reference.startswith',
            'schema.get',
            'schema.get',
            'schema.get',
            'schema.get',
            'schema.get',
            'schema.get',
            'schema.get',
            'schema.get',
            'schema.get',
            'sum',
            'type',
            'type',
            'type',
            'type',
            'type',
            'type',
            'type',
            'type',
            'type',
            'type',
            'type',
            'value.is_integer',
            'value.items'],
 '_check_nullable_reason': ['_fail'],
 '_enum': ['list'],
 '_equality_key': ['_equality_key',
                   '_equality_key',
                   'frozenset',
                   'tuple',
                   'type',
                   'type',
                   'type',
                   'type',
                   'value.items'],
 '_fail': ['ReportValidationError'],
 '_field': ['FieldDefinition',
            '_base_envelope',
            '_field_entries.append',
            '_nullable',
            '_object',
            '_ref',
            '_ref',
            '_ref',
            '_text',
            '_text',
            'properties.update',
            "result['allOf'].append",
            'tuple'],
 '_freeze': ['MappingProxyType', '_freeze', '_freeze', 'tuple', 'type', 'type', 'value.items'],
 '_json_input': ['_fail',
                 '_fail',
                 '_fail',
                 '_fail',
                 '_fail',
                 '_fail',
                 '_json_input',
                 '_json_input',
                 'active.add',
                 'active.remove',
                 'enumerate',
                 'id',
                 'id',
                 'id',
                 'math.isfinite',
                 'set',
                 'type',
                 'type',
                 'type',
                 'type',
                 'type',
                 'type',
                 'type',
                 'type',
                 'value.encode',
                 'value.items'],
 '_map': ['_text'],
 '_matches': ['_check'],
 '_metric': ['_field'],
 '_object': ['list', 'list'],
 '_observed': ['_field'],
 '_resolved_contract': ['_matches',
                        '_resolved_contract',
                        '_resolved_contract',
                        'contract.get',
                        'contract.get',
                        "contract['$ref'].removeprefix"],
 '_same': ['_same',
           '_same',
           'all',
           'all',
           'isinstance',
           'isinstance',
           'len',
           'len',
           'set',
           'set',
           'type',
           'type',
           'type',
           'type',
           'type',
           'type',
           'zip'],
 '_semantic_checks': ['_check_nullable_reason',
                      '_check_nullable_reason',
                      '_check_nullable_reason',
                      '_fail',
                      '_fail',
                      '_fail',
                      '_fail',
                      '_fail',
                      '_fail',
                      '_fail',
                      '_fail',
                      '_fail',
                      '_fail',
                      '_fail',
                      '_fail',
                      '_fail',
                      '_fail',
                      '_fail',
                      '_fail',
                      '_fail',
                      '_fail',
                      '_fail',
                      '_fail',
                      '_fail',
                      '_fail',
                      '_fail',
                      '_fail',
                      '_fail',
                      '_fail',
                      '_fail',
                      '_fail',
                      '_fail',
                      '_fail',
                      '_fail',
                      '_fail',
                      '_fail',
                      '_fail',
                      '_fail',
                      '_fail',
                      '_fail',
                      '_fail',
                      '_fail',
                      '_fail',
                      '_fail',
                      '_fail',
                      '_fail',
                      '_fail',
                      '_walk',
                      'all',
                      'all',
                      'any',
                      'any',
                      'any',
                      'any',
                      'any',
                      'bool',
                      'contract.get',
                      'int',
                      'item.get',
                      'item.get',
                      'item.get',
                      'item.get',
                      'item.get',
                      "item['owner_ids'][0].startswith",
                      'len',
                      'len',
                      'len',
                      'len',
                      'len',
                      'len',
                      'len',
                      'len',
                      'len',
                      'len',
                      'len',
                      'len',
                      'len',
                      'len',
                      'len',
                      'math.isclose',
                      'math.isclose',
                      'observability.get',
                      "payload['capabilities'].items",
                      "payload['derived_metrics'].get",
                      "payload['derived_metrics'].get",
                      "payload['derived_metrics'].get('closure_exposure', {}).get",
                      "payload['simulations'].items",
                      'set',
                      'set',
                      'set',
                      'set',
                      'type',
                      'type',
                      'type'],
 '_strings': ['_array', '_text'],
 '_thaw': ['_thaw', '_thaw', 'isinstance', 'type', 'type', 'value.items'],
 '_walk': ['_resolved_contract',
           '_walk',
           '_walk',
           'contract.get',
           'contract.get',
           'enumerate',
           'isinstance',
           'properties.get',
           'type',
           'type',
           'value.items'],
 'report_schema': ['_freeze', '_thaw'],
 'validate_report': ['_check', '_json_input', '_semantic_checks']}
PHASE4_STEP2_RESULT_ARITHMETIC = {'_build_contract': ["'PR-004.' + name",
                     "'PR-004.' + name",
                     "'PR-006.' + name",
                     "'PR-008.' + name",
                     "'derived_metrics.closure_exposure.direct.' + name",
                     "'derived_metrics.closure_exposure.lineage.' + name",
                     "'derived_metrics.diversity.by_version.*.' + name",
                     "'derived_metrics.diversity.by_version.*.' + name",
                     "'derived_metrics.lineage.' + name",
                     "'derived_metrics.provenance.' + name",
                     "'derived_metrics.support.' + name",
                     "'derived_metrics.support.by_version.*.' + name",
                     "'observed_facts.content.' + name",
                     "'observed_facts.lineage.' + name",
                     "'observed_facts.provenance.' + name",
                     "'observed_facts.provenance.' + name",
                     "'observed_facts.provenance.' + name",
                     "'observed_facts.provenance.' + name",
                     "'proxy_signals.' + name",
                     "'simulations.' + name",
                     "'unavailable_conclusions[].' + name",
                     '-1',
                     '-sys.float_info.max',
                     "owner + '.'",
                     "owner + '.'",
                     "owner + '.'",
                     "owner + '.'",
                     "owner + '.'",
                     "owner + '.' + name",
                     "owner + '.' + name",
                     "owner + '.' + name",
                     "owner + '.' + name",
                     "owner + '.' + name",
                     "owner + '.unavailable_conclusion'",
                     "owner + '.unavailable_conclusion'",
                     "required += ('by_state',)"],
 '_check': ["not _same(value, schema['const'])",
            "not any((_matches(value, item) for item in schema['anyOf']))",
            "not any((_same(value, choice) for choice in schema['enum']))",
            "not reference.startswith('#/$defs/')",
            'not valid_type[expected]',
            "path + '.'",
            "path + '.' + key",
            "path + '.<key>'",
            "path + '.<key>'",
            "path + f'[{index}]'"],
 '_json_input': ['not finite', "path + '.<item>'", "path + '.<key>'", 'set | None'],
 '_number': ['-sys.float_info.max', 'int | float', 'int | float'],
 '_object': ['tuple | list', 'tuple | list | None'],
 '_ref': ["'#/$defs/' + name"],
 '_semantic_checks': ['-1',
                      'included + excluded',
                      'included_ids & excluded_ids',
                      "item['ratio'] * item['denominator']",
                      "not capability['execution_reason_codes']",
                      "not capability['execution_scope']",
                      "not item['reason']",
                      "not item['reason_codes']",
                      "not item['required_evidence']",
                      "not math.isclose(interval['interval_width']['value'], upper - lower, rel_tol=1e-12, "
                      'abs_tol=1e-12)',
                      "not math.isclose(item['ratio'] * item['denominator'], item['numerator'], "
                      'rel_tol=1e-12, abs_tol=1e-12)',
                      'not present',
                      "parameters['simulation_horizon'] + 1",
                      "parameters['simulation_horizon'] + 1",
                      'upper - lower'],
 '_walk': ['path + (index,)', 'path + (key,)']}
PHASE4_STEP2_RESULT_MUTATIONS = [('CanonicalReport.__init__', "object.__setattr__(self, 'sections', frozen)")]
PHASE4_STEP2_RESULT_DECLARATIONS = [('<module>',
  "CAPABILITY_KEYS = ('ingestion', 'content_diagnostics', 'provenance', 'lineage', 'dataset_longitudinal', "
  "'model_longitudinal', 'intervention_simulation')"),
 ('<module>', 'FIELD_REGISTRY = tuple(_field_entries)'),
 ('<module>',
  "LEVEL_LABELS = ('ingest_observability', 'content_or_representation_observability', "
  "'provenance_observability', 'lineage_observability', 'longitudinal_dataset_observability', "
  "'experimental_intervention_or_scenario_observability')"),
 ('<module>',
  "RUN_NULLABLE_FIELDS = ('started_at', 'completed_at', 'duration_seconds', 'python_version', 'platform', "
  "'command', 'config_hash', 'random_seed')"),
 ('<module>',
  "SECTION_ORDER = ('run', 'inputs', 'observability', 'capabilities', 'observed_facts', 'derived_metrics', "
  "'proxy_signals', 'simulations', 'unavailable_conclusions', 'recommended_next_metadata', 'warnings', "
  "'errors')"),
 ('<module>', '_REPORT_SCHEMA = _build_contract()'),
 ('<module>', '_REPORT_SCHEMA = _freeze(_REPORT_SCHEMA)'),
 ('<module>', '_field_entries: list[FieldDefinition] = []'),
 ('<module>', 'del _field_entries'),
 ('CanonicalReport', 'sections: Mapping'),
 ('ExecutionStatus', "COMPLETED = 'completed'"),
 ('ExecutionStatus', "DEFERRED = 'deferred'"),
 ('ExecutionStatus', "FAILED = 'failed'"),
 ('ExecutionStatus', "NOT_REQUESTED = 'not_requested'"),
 ('ExecutionStatus', "PARTIAL = 'partial'"),
 ('FieldDefinition', 'evidence_class: str'),
 ('FieldDefinition', 'method_id: str'),
 ('FieldDefinition', 'minimum_level: int'),
 ('FieldDefinition', 'owner: str'),
 ('FieldDefinition', 'path: str'),
 ('FieldDefinition', 'requires_representation: bool = False'),
 ('FieldDefinition', "status_boundary: str = 'current'"),
 ('FieldDefinition', 'unit: str'),
 ('FieldDefinition', 'value_type: str'),
 ('ReportEvidenceClass', "DERIVED_METRIC = 'derived_metric'"),
 ('ReportEvidenceClass', "OBSERVED_FACT = 'observed_fact'"),
 ('ReportEvidenceClass', "PROXY_SIGNAL = 'proxy_signal'"),
 ('ReportEvidenceClass', "SIMULATION = 'simulation'"),
 ('ReportEvidenceClass', "UNAVAILABLE_CONCLUSION = 'unavailable_conclusion'"),
 ('ReportStatus', "AVAILABLE = 'available'"),
 ('ReportStatus', "EXPERIMENTAL = 'experimental'"),
 ('ReportStatus', "PARTIAL = 'partial'"),
 ('ReportStatus', "UNAVAILABLE = 'unavailable'"),
 ('RunStatus', "COMPLETE = 'complete'"),
 ('RunStatus', "FAILED = 'failed'"),
 ('RunStatus', "PARTIAL = 'partial'")]
PHASE4_STEP2_RESULT_TRAVERSAL = [('<module>', 'del _field_entries'),
 ('_walk', '(yield (path, value, contract))'),
 ('_walk', "(yield from _walk(item, path + (index,), contract['items']))"),
 ('_walk', '(yield from _walk(item, path + (key,), child))')]
PHASE4_STEP2_RESULT_ATTRIBUTES = {'CanonicalReport.__init__': ['object.__setattr__'],
 'CanonicalReport.to_dict': ['self.sections'],
 '_build_contract': ['_field_entries.append',
                     '_field_entries.append',
                     '_field_entries.append',
                     '_field_entries.append',
                     'item.value',
                     'props.update',
                     'props.update',
                     'props.update',
                     'props.update',
                     'sys.float_info',
                     'sys.float_info',
                     'sys.float_info.max',
                     'sys.float_info.max',
                     'unavailable_owners.items',
                     'unavailable_variants.append'],
 '_check': ['math.isfinite',
            're.search',
            'reference.removeprefix',
            'reference.startswith',
            'schema.get',
            'schema.get',
            'schema.get',
            'schema.get',
            'schema.get',
            'schema.get',
            'schema.get',
            'schema.get',
            'schema.get',
            'value.is_integer',
            'value.items'],
 '_equality_key': ['value.items'],
 '_field': ['_field_entries.append', 'properties.update', "result['allOf'].append"],
 '_freeze': ['value.items'],
 '_integer': ['sys.float_info', 'sys.float_info.max'],
 '_json_input': ['active.add', 'active.remove', 'math.isfinite', 'value.encode', 'value.items'],
 '_number': ['sys.float_info', 'sys.float_info', 'sys.float_info.max', 'sys.float_info.max'],
 '_resolved_contract': ['contract.get', 'contract.get', "contract['$ref'].removeprefix"],
 '_semantic_checks': ['contract.get',
                      'item.get',
                      'item.get',
                      'item.get',
                      'item.get',
                      'item.get',
                      "item['owner_ids'][0].startswith",
                      'math.isclose',
                      'math.isclose',
                      'observability.get',
                      "payload['capabilities'].items",
                      "payload['derived_metrics'].get",
                      "payload['derived_metrics'].get",
                      "payload['derived_metrics'].get('closure_exposure', {}).get",
                      "payload['simulations'].items"],
 '_thaw': ['value.items'],
 '_walk': ['contract.get', 'contract.get', 'properties.get', 'value.items']}
PHASE4_STEP2_RESULT_HEADERS = [('CanonicalReport', (), (), ('dataclass(frozen=True, slots=True, init=False)',)),
 ('CanonicalReport.__init__',
  "arguments(posonlyargs=[], args=[arg(arg='self'), arg(arg='payload', annotation=Name(id='dict', "
  'ctx=Load()))], kwonlyargs=[], kw_defaults=[], defaults=[])',
  (),
  'None'),
 ('CanonicalReport.from_dict',
  "arguments(posonlyargs=[], args=[arg(arg='cls'), arg(arg='payload', annotation=Name(id='dict', "
  'ctx=Load()))], kwonlyargs=[], kw_defaults=[], defaults=[])',
  ('classmethod',),
  "'CanonicalReport'"),
 ('CanonicalReport.to_dict',
  "arguments(posonlyargs=[], args=[arg(arg='self')], kwonlyargs=[], kw_defaults=[], defaults=[])",
  (),
  'dict'),
 ('ExecutionStatus', ('StrEnum',), (), ()),
 ('FieldDefinition', (), (), ('dataclass(frozen=True, slots=True)',)),
 ('ReportEvidenceClass', ('StrEnum',), (), ()),
 ('ReportStatus', ('StrEnum',), (), ()),
 ('ReportValidationError', ('ValueError',), (), ()),
 ('RunStatus', ('StrEnum',), (), ()),
 ('_array',
  "arguments(posonlyargs=[], args=[arg(arg='item', annotation=Name(id='dict', ctx=Load()))], "
  "kwonlyargs=[arg(arg='minimum', annotation=Name(id='int', ctx=Load())), arg(arg='unique', "
  "annotation=Name(id='bool', ctx=Load()))], kw_defaults=[Constant(value=0), Constant(value=False)], "
  'defaults=[])',
  (),
  'dict'),
 ('_base_envelope',
  "arguments(posonlyargs=[], args=[arg(arg='evidence', annotation=Name(id='str', ctx=Load())), "
  "arg(arg='unit', annotation=Name(id='str', ctx=Load())), arg(arg='owner', annotation=Name(id='str', "
  "ctx=Load())), arg(arg='method', annotation=Name(id='str', ctx=Load()))], kwonlyargs=[], kw_defaults=[], "
  'defaults=[])',
  (),
  'dict'),
 ('_build_contract',
  'arguments(posonlyargs=[], args=[], kwonlyargs=[], kw_defaults=[], defaults=[])',
  (),
  'dict'),
 ('_check',
  "arguments(posonlyargs=[], args=[arg(arg='value'), arg(arg='schema', annotation=Name(id='dict', "
  "ctx=Load())), arg(arg='path', annotation=Name(id='str', ctx=Load()))], kwonlyargs=[], kw_defaults=[], "
  'defaults=[])',
  (),
  'None'),
 ('_check_nullable_reason',
  "arguments(posonlyargs=[], args=[arg(arg='value', annotation=Name(id='dict', ctx=Load())), arg(arg='name', "
  "annotation=Name(id='str', ctx=Load())), arg(arg='reason_name', annotation=Name(id='str', ctx=Load())), "
  "arg(arg='path', annotation=Name(id='str', ctx=Load()))], kwonlyargs=[], kw_defaults=[], defaults=[])",
  (),
  'None'),
 ('_enum',
  "arguments(posonlyargs=[], args=[], vararg=arg(arg='values', annotation=Name(id='str', ctx=Load())), "
  'kwonlyargs=[], kw_defaults=[], defaults=[])',
  (),
  'dict'),
 ('_equality_key',
  "arguments(posonlyargs=[], args=[arg(arg='value')], kwonlyargs=[], kw_defaults=[], defaults=[])",
  (),
  ''),
 ('_fail',
  "arguments(posonlyargs=[], args=[arg(arg='path', annotation=Name(id='str', ctx=Load())), arg(arg='rule', "
  "annotation=Name(id='str', ctx=Load()))], kwonlyargs=[], kw_defaults=[], defaults=[])",
  (),
  'None'),
 ('_field',
  "arguments(posonlyargs=[], args=[arg(arg='path', annotation=Name(id='str', ctx=Load())), arg(arg='value', "
  "annotation=Name(id='dict', ctx=Load()))], kwonlyargs=[arg(arg='owner', annotation=Name(id='str', "
  "ctx=Load())), arg(arg='evidence', annotation=Name(id='str', ctx=Load())), arg(arg='unit', "
  "annotation=Name(id='str', ctx=Load())), arg(arg='method', annotation=Name(id='str', ctx=Load())), "
  "arg(arg='level', annotation=Name(id='int', ctx=Load())), arg(arg='value_type', annotation=Name(id='str', "
  "ctx=Load())), arg(arg='representation', annotation=Name(id='bool', ctx=Load())), arg(arg='boundary', "
  "annotation=Name(id='str', ctx=Load()))], kw_defaults=[None, None, None, None, None, None, "
  "Constant(value=False), Constant(value='current')], defaults=[])",
  (),
  'dict'),
 ('_freeze',
  "arguments(posonlyargs=[], args=[arg(arg='value')], kwonlyargs=[], kw_defaults=[], defaults=[])",
  (),
  ''),
 ('_integer',
  "arguments(posonlyargs=[], args=[], kwonlyargs=[arg(arg='minimum', annotation=Name(id='int', "
  'ctx=Load()))], kw_defaults=[Constant(value=0)], defaults=[])',
  (),
  'dict'),
 ('_json_input',
  "arguments(posonlyargs=[], args=[arg(arg='value'), arg(arg='path', annotation=Name(id='str', ctx=Load())), "
  "arg(arg='active', annotation=BinOp(left=Name(id='set', ctx=Load()), op=BitOr(), "
  "right=Constant(value=None)))], kwonlyargs=[], kw_defaults=[], defaults=[Constant(value='$'), "
  'Constant(value=None)])',
  (),
  'None'),
 ('_map',
  "arguments(posonlyargs=[], args=[arg(arg='values', annotation=Name(id='dict', ctx=Load()))], "
  'kwonlyargs=[], kw_defaults=[], defaults=[])',
  (),
  'dict'),
 ('_matches',
  "arguments(posonlyargs=[], args=[arg(arg='value'), arg(arg='schema', annotation=Name(id='dict', "
  'ctx=Load()))], kwonlyargs=[], kw_defaults=[], defaults=[])',
  (),
  'bool'),
 ('_metric',
  "arguments(posonlyargs=[], args=[arg(arg='path', annotation=Name(id='str', ctx=Load())), arg(arg='value', "
  "annotation=Name(id='dict', ctx=Load())), arg(arg='owner', annotation=Name(id='str', ctx=Load())), "
  "arg(arg='unit', annotation=Name(id='str', ctx=Load())), arg(arg='method', annotation=Name(id='str', "
  "ctx=Load())), arg(arg='level', annotation=Name(id='int', ctx=Load())), arg(arg='value_type', "
  "annotation=Name(id='str', ctx=Load()))], kwonlyargs=[arg(arg='representation', annotation=Name(id='bool', "
  "ctx=Load())), arg(arg='boundary', annotation=Name(id='str', ctx=Load()))], "
  "kw_defaults=[Constant(value=False), Constant(value='current')], defaults=[])",
  (),
  'dict'),
 ('_nullable',
  "arguments(posonlyargs=[], args=[arg(arg='schema', annotation=Name(id='dict', ctx=Load()))], "
  'kwonlyargs=[], kw_defaults=[], defaults=[])',
  (),
  'dict'),
 ('_number',
  "arguments(posonlyargs=[], args=[], kwonlyargs=[arg(arg='minimum', annotation=BinOp(left=Name(id='int', "
  "ctx=Load()), op=BitOr(), right=Name(id='float', ctx=Load()))), arg(arg='maximum', "
  "annotation=BinOp(left=Name(id='int', ctx=Load()), op=BitOr(), right=Name(id='float', ctx=Load())))], "
  "kw_defaults=[UnaryOp(op=USub(), operand=Attribute(value=Attribute(value=Name(id='sys', ctx=Load()), "
  "attr='float_info', ctx=Load()), attr='max', ctx=Load())), Attribute(value=Attribute(value=Name(id='sys', "
  "ctx=Load()), attr='float_info', ctx=Load()), attr='max', ctx=Load())], defaults=[])",
  (),
  'dict'),
 ('_object',
  "arguments(posonlyargs=[], args=[arg(arg='properties', annotation=Name(id='dict', ctx=Load())), "
  "arg(arg='required', annotation=BinOp(left=BinOp(left=Name(id='tuple', ctx=Load()), op=BitOr(), "
  "right=Name(id='list', ctx=Load())), op=BitOr(), right=Constant(value=None)))], kwonlyargs=[], "
  'kw_defaults=[], defaults=[Constant(value=None)])',
  (),
  'dict'),
 ('_observed',
  "arguments(posonlyargs=[], args=[arg(arg='path', annotation=Name(id='str', ctx=Load())), arg(arg='value', "
  "annotation=Name(id='dict', ctx=Load())), arg(arg='owner', annotation=Name(id='str', ctx=Load())), "
  "arg(arg='unit', annotation=Name(id='str', ctx=Load())), arg(arg='method', annotation=Name(id='str', "
  "ctx=Load())), arg(arg='level', annotation=Name(id='int', ctx=Load())), arg(arg='value_type', "
  "annotation=Name(id='str', ctx=Load()))], kwonlyargs=[arg(arg='boundary', annotation=Name(id='str', "
  "ctx=Load())), arg(arg='representation', annotation=Name(id='bool', ctx=Load()))], "
  "kw_defaults=[Constant(value='current'), Constant(value=False)], defaults=[])",
  (),
  'dict'),
 ('_ref',
  "arguments(posonlyargs=[], args=[arg(arg='name', annotation=Name(id='str', ctx=Load()))], kwonlyargs=[], "
  'kw_defaults=[], defaults=[])',
  (),
  'dict'),
 ('_resolved_contract',
  "arguments(posonlyargs=[], args=[arg(arg='value'), arg(arg='contract')], kwonlyargs=[], kw_defaults=[], "
  'defaults=[])',
  (),
  ''),
 ('_same',
  "arguments(posonlyargs=[], args=[arg(arg='left'), arg(arg='right')], kwonlyargs=[], kw_defaults=[], "
  'defaults=[])',
  (),
  'bool'),
 ('_semantic_checks',
  "arguments(posonlyargs=[], args=[arg(arg='payload', annotation=Name(id='dict', ctx=Load()))], "
  'kwonlyargs=[], kw_defaults=[], defaults=[])',
  (),
  'None'),
 ('_strings',
  "arguments(posonlyargs=[], args=[], kwonlyargs=[arg(arg='minimum', annotation=Name(id='int', "
  'ctx=Load()))], kw_defaults=[Constant(value=0)], defaults=[])',
  (),
  'dict'),
 ('_text',
  "arguments(posonlyargs=[], args=[], kwonlyargs=[arg(arg='empty', annotation=Name(id='bool', ctx=Load()))], "
  'kw_defaults=[Constant(value=False)], defaults=[])',
  (),
  'dict'),
 ('_thaw',
  "arguments(posonlyargs=[], args=[arg(arg='value')], kwonlyargs=[], kw_defaults=[], defaults=[])",
  (),
  ''),
 ('_walk',
  "arguments(posonlyargs=[], args=[arg(arg='value'), arg(arg='path'), arg(arg='contract')], kwonlyargs=[], "
  'kw_defaults=[], defaults=[Tuple(elts=[], ctx=Load()), Constant(value=None)])',
  (),
  ''),
 ('report_schema',
  'arguments(posonlyargs=[], args=[], kwonlyargs=[], kw_defaults=[], defaults=[])',
  (),
  'dict'),
 ('validate_report',
  "arguments(posonlyargs=[], args=[arg(arg='payload', annotation=Name(id='dict', ctx=Load()))], "
  'kwonlyargs=[], kw_defaults=[], defaults=[])',
  (),
  'None')]


def phase4_step2_result_boundary(path: Path) -> None:
    """Inspect only the supplied canonical-result source without executing it.

    Fixed reviewed inventories constrain definitions, imports, call targets and
    validation arithmetic. They are never regenerated from inspected source.
    The release controller separately freezes the other 39 runtime modules.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (OSError, UnicodeError, SyntaxError) as exc:
        raise ValueError("Phase 4 Step 2 result source cannot be inspected") from exc
    doc = ast.get_docstring(tree) or ""
    if "Owner IDs:" not in doc or "Current phase status:" not in doc:
        raise ValueError("Phase 4 Step 2 result ownership metadata is missing")
    allowed_top = (ast.Import, ast.ImportFrom, ast.Assign, ast.AnnAssign,
                   ast.FunctionDef, ast.ClassDef, ast.Delete)
    for index, node in enumerate(tree.body):
        if index == 0 and isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            continue
        if not isinstance(node, allowed_top):
            raise ValueError("Phase 4 Step 2 result has an unapproved module statement")
    imports = []
    functions = []
    classes = []
    calls = {}
    arithmetic = {}
    mutations = []
    declarations = []
    traversal = []
    attributes = {}
    headers = []
    call_names = {node.func.id for node in ast.walk(tree)
                  if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)}
    forbidden = (ast.Lambda, ast.AsyncFunctionDef, ast.Await, ast.With,
                 ast.AsyncWith, ast.Global, ast.Nonlocal, ast.NamedExpr)
    forbidden_names = {"eval", "exec", "compile", "__import__", "getattr",
                       "setattr", "delattr", "globals", "locals", "vars",
                       "open", "input", "breakpoint", "print", "exit", "quit"}
    forbidden_attributes = {"__builtins__", "__globals__", "__code__", "__subclasses__",
                            "__class__", "__dict__", "__getattribute__", "__getattr__",
                            "open", "read", "read_text", "read_bytes", "write", "write_text",
                            "write_bytes", "mkdir", "unlink", "system", "popen", "connect",
                            "connect_ex", "getaddrinfo", "urlopen", "urlretrieve", "send", "sendall"}
    stack = [(tree, "<module>")]
    while stack:
        node, scope = stack.pop()
        if isinstance(node, forbidden):
            raise ValueError("Phase 4 Step 2 result has a callback or executable control outside scope")
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            scope = node.name if scope == "<module>" else scope + "." + node.name
            if isinstance(node, ast.FunctionDef):
                functions.append(scope)
                headers.append((scope, ast.dump(node.args, include_attributes=False),
                                tuple(ast.unparse(item) for item in node.decorator_list),
                                ast.unparse(node.returns) if node.returns is not None else ""))
            else:
                classes.append(scope)
                headers.append((scope, tuple(ast.unparse(item) for item in node.bases),
                                tuple(ast.unparse(item) for item in node.keywords),
                                tuple(ast.unparse(item) for item in node.decorator_list)))
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            if scope != "<module>" or node not in tree.body:
                raise ValueError("Phase 4 Step 2 result imports must be explicit and at module scope")
            imports.append(ast.dump(node, include_attributes=False))
        if isinstance(node, ast.Name) and node.id in forbidden_names:
            raise ValueError("Phase 4 Step 2 result names a forbidden execution capability")
        if scope != "<module>" and ((isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store) and node.id in call_names)
                                    or (isinstance(node, ast.arg) and node.arg in call_names)):
            raise ValueError("Phase 4 Step 2 result shadows an approved call target")
        if isinstance(node, ast.Attribute):
            attributes.setdefault(scope, []).append(ast.unparse(node))
        if isinstance(node, ast.Attribute) and node.attr in forbidden_attributes:
            raise ValueError("Phase 4 Step 2 result names a forbidden IO or dynamic capability")
        if isinstance(node, ast.Call):
            if not isinstance(node.func, (ast.Name, ast.Attribute)):
                raise ValueError("Phase 4 Step 2 result invokes a dynamic call target")
            calls.setdefault(scope, []).append(ast.unparse(node.func))
            if isinstance(node.func, ast.Attribute) and node.func.attr == "__setattr__":
                mutations.append((scope, ast.unparse(node)))
        if isinstance(node, (ast.BinOp, ast.UnaryOp, ast.AugAssign)):
            arithmetic.setdefault(scope, []).append(ast.unparse(node))
        if (scope == "<module>" or scope in classes) and isinstance(node, (ast.Assign, ast.AnnAssign, ast.Delete)):
            declarations.append((scope, ast.unparse(node)))
        if isinstance(node, (ast.Yield, ast.YieldFrom, ast.Delete)):
            traversal.append((scope, ast.unparse(node)))
        if isinstance(node, ast.Attribute) and isinstance(node.ctx, (ast.Store, ast.Del)):
            raise ValueError("Phase 4 Step 2 result has an unapproved attribute mutation")
        stack.extend((child, scope) for child in ast.iter_child_nodes(node))
    if sorted(imports) != PHASE4_STEP2_RESULT_IMPORTS:
        raise ValueError("Phase 4 Step 2 result imports differ from the reviewed stdlib inventory")
    if sorted(functions) != PHASE4_STEP2_RESULT_FUNCTIONS or sorted(classes) != PHASE4_STEP2_RESULT_CLASSES:
        raise ValueError("Phase 4 Step 2 result definitions differ from the approved contract")
    if {name: sorted(values) for name, values in calls.items()} != PHASE4_STEP2_RESULT_CALLS:
        raise ValueError("Phase 4 Step 2 result call targets differ from the reviewed inventory")
    if {name: sorted(values) for name, values in arithmetic.items()} != PHASE4_STEP2_RESULT_ARITHMETIC:
        raise ValueError("Phase 4 Step 2 result arithmetic exceeds reviewed semantic validation")
    if sorted(mutations) != PHASE4_STEP2_RESULT_MUTATIONS:
        raise ValueError("Phase 4 Step 2 result mutation differs from reviewed immutable construction")
    if sorted(declarations) != PHASE4_STEP2_RESULT_DECLARATIONS:
        raise ValueError("Phase 4 Step 2 result module declarations differ from the approved contract")
    if sorted(traversal) != PHASE4_STEP2_RESULT_TRAVERSAL:
        raise ValueError("Phase 4 Step 2 result generator or teardown differs from reviewed local traversal")
    if {name: sorted(values) for name, values in attributes.items()} != PHASE4_STEP2_RESULT_ATTRIBUTES:
        raise ValueError("Phase 4 Step 2 result attributes exceed the reviewed pure contract")
    if sorted(headers) != PHASE4_STEP2_RESULT_HEADERS:
        raise ValueError("Phase 4 Step 2 result definition headers differ from the reviewed contract")


def phase4_step2_main(step: int = 2) -> int:
    """Validate Step 2 control, reviewed schema bytes and the result AST only."""
    import hashlib
    import runpy

    if type(step) is not int or step != 2:
        raise ValueError("Only authorized Phase 4 Step 2 traceability is available")
    control = runpy.run_path(str(ROOT / "scripts/release_check.py"),
                            run_name="phase4_step2_traceability_control")
    control["audit_phase4_step2"](step=step)
    schema_path = ROOT / "schemas/report.schema.json"
    if hashlib.sha256(schema_path.read_bytes()).hexdigest() != PHASE4_STEP2_REPORT_SCHEMA_SHA256:
        raise ValueError("Phase 4 Step 2 report schema differs from the reviewed contract")
    phase4_step2_result_boundary(PACKAGE / "result.py")
    print("Phase 4 Step 2: canonical results and reviewed local schema: PASS")
    return 0




# Step 3 reviewed pure adapters. These independent inventories are never
# regenerated by the active gate from inspected source.
PHASE4_STEP3_ASSEMBLY_IMPORTS = ["ImportFrom(module='__future__', names=[alias(name='annotations')], level=0)",
 "ImportFrom(module='dataclasses', names=[alias(name='dataclass')], level=0)",
 "ImportFrom(module='math', names=[alias(name='isfinite'), alias(name='isclose')], level=0)",
 "ImportFrom(module='metrics.bounds', names=[alias(name='DirectClosureExposureBounds')], level=2)",
 "ImportFrom(module='metrics.diversity', names=[alias(name='DistributionMetrics'), "
 "alias(name='StateDistributionResult'), alias(name='SupportComparison'), alias(name='StateFrequency')], "
 'level=2)',
 "ImportFrom(module='metrics.duplicates', names=[alias(name='ExactDuplicateResult'), "
 "alias(name='ExactDuplicateGroup')], level=2)",
 "ImportFrom(module='metrics.provenance', names=[alias(name='ProvenanceCompositionResult'), "
 "alias(name='DeclaredComposition'), alias(name='WeightedSourceComposition'), "
 "alias(name='DirectGroundingBasis'), alias(name='DirectGroundingAssignment')], level=2)",
 "ImportFrom(module='metrics.resampling', names=[alias(name='ExpectedDiversityResult'), "
 "alias(name='ResamplingSimulation'), alias(name='ResamplingInput'), alias(name='ResamplingReplicate'), "
 "alias(name='SampledGeneration')], level=2)",
 "ImportFrom(module='metrics.tail', names=[alias(name='TailSelectionResult'), "
 "alias(name='ExtinctionProbabilityResult'), alias(name='RarityEntry')], level=2)",
 "ImportFrom(module='models', names=[alias(name='BundleValidationResult'), "
 "alias(name='CalculationEvidenceClass'), alias(name='CalculationMetadata'), "
 "alias(name='CalculationReason'), alias(name='CalculationScope'), alias(name='CalculationStatus'), "
 "alias(name='CapabilityKey'), alias(name='CanonicalRow'), alias(name='NumericalPolicy'), "
 "alias(name='RecordKey'), alias(name='RepresentationDescriptor'), alias(name='ScalarCalculation'), "
 "alias(name='ValidationCoverage'), alias(name='ValidationMessage'), alias(name='ValidationSeverity'), "
 "alias(name='WeightingOptions'), alias(name='Capability'), alias(name='CapabilityStatus'), "
 "alias(name='ObservabilityAssessment'), alias(name='FileInventoryEntry'), alias(name='FileRole'), "
 "alias(name='FileFormat'), alias(name='VersionOrderResult'), alias(name='ProvenanceJoinResult'), "
 "alias(name='ProvenanceMatch'), alias(name='ProvenanceAssessment'), alias(name='ExplicitPairContext'), "
 "alias(name='RowMappingEvidence'), alias(name='RowLocation'), alias(name='GenerationValidationResult'), "
 "alias(name='RecordStateAssignment'), alias(name='TailSelectionOptions')], level=2)",
 "ImportFrom(module='pathlib', names=[alias(name='PosixPath'), alias(name='WindowsPath')], level=0)",
 "ImportFrom(module='representations.compatibility', names=[alias(name='RepresentationCompatibility'), "
 "alias(name='StateMappingDeclaration')], level=2)",
 "ImportFrom(module='result', names=[alias(name='CanonicalReport'), alias(name='FIELD_REGISTRY'), "
 "alias(name='LEVEL_LABELS'), alias(name='SECTION_ORDER'), alias(name='ReportValidationError')], level=2)",
 "ImportFrom(module='types', names=[alias(name='MappingProxyType')], level=0)"]

PHASE4_STEP3_ASSEMBLY_FUNCTIONS = ['FamilyFailure.__post_init__',
 '_base',
 '_bundle_check',
 '_bundle_scope',
 '_capabilities',
 '_closed_simulation',
 '_closure',
 '_comparison',
 '_coverage',
 '_definition',
 '_diagnostics',
 '_disclosure_base',
 '_disclosure_recommend',
 '_disclosure_scope',
 '_disclosure_signal',
 '_disclosure_unavailable',
 '_disclosures',
 '_distribution',
 '_distribution_exclusions',
 '_duplicates',
 '_envelope',
 '_extinction',
 '_inputs',
 '_key',
 '_lineage_observations',
 '_message_family',
 '_metadata',
 '_metadata_text',
 '_number',
 '_policy',
 '_provenance',
 '_provenance_consistency',
 '_representation',
 '_require',
 '_scalar',
 '_scope',
 '_simulation_inputs',
 '_table',
 '_tail',
 '_typed',
 'assemble_report']

PHASE4_STEP3_ASSEMBLY_CLASSES = ['FamilyFailure', 'ReportAssemblyError']

PHASE4_STEP3_ASSEMBLY_MUTATIONS = []

PHASE4_STEP3_ASSEMBLY_DECLARATIONS = [('FamilyFailure', 'capability: CapabilityKey'), ('FamilyFailure', 'messages: tuple[ValidationMessage, ...]')]

PHASE4_STEP3_ASSEMBLY_TRAVERSAL = []

PHASE4_STEP3_ASSEMBLY_HEADERS = [('FamilyFailure', (), (), ('dataclass(frozen=True, slots=True)',)),
 ('FamilyFailure.__post_init__',
  "arguments(posonlyargs=[], args=[arg(arg='self')], kwonlyargs=[], kw_defaults=[], defaults=[])",
  (),
  ''),
 ('ReportAssemblyError', ('ReportValidationError',), (), ()),
 ('_base',
  "arguments(posonlyargs=[], args=[arg(arg='path'), arg(arg='scope')], "
  "kwonlyargs=[arg(arg='representation'), arg(arg='coverage'), arg(arg='denominator'), "
  "arg(arg='assumptions'), arg(arg='limitations'), arg(arg='status'), arg(arg='reasons'), "
  "arg(arg='required')], kw_defaults=[Constant(value=None), Constant(value=None), Constant(value=None), "
  "Tuple(elts=[], ctx=Load()), Tuple(elts=[], ctx=Load()), Constant(value='available'), Tuple(elts=[], "
  'ctx=Load()), Tuple(elts=[], ctx=Load())], defaults=[])',
  (),
  ''),
 ('_bundle_check',
  "arguments(posonlyargs=[], args=[arg(arg='bundle')], kwonlyargs=[], kw_defaults=[], defaults=[])",
  (),
  ''),
 ('_bundle_scope',
  "arguments(posonlyargs=[], args=[arg(arg='bundle')], kwonlyargs=[], kw_defaults=[], defaults=[])",
  (),
  ''),
 ('_capabilities',
  "arguments(posonlyargs=[], args=[arg(arg='payload'), arg(arg='bundle'), arg(arg='operations'), "
  "arg(arg='failures')], kwonlyargs=[], kw_defaults=[], defaults=[])",
  (),
  ''),
 ('_closed_simulation',
  "arguments(posonlyargs=[], args=[arg(arg='payload'), arg(arg='value')], kwonlyargs=[], kw_defaults=[], "
  'defaults=[])',
  (),
  ''),
 ('_closure',
  "arguments(posonlyargs=[], args=[arg(arg='payload'), arg(arg='value'), arg(arg='bundle'), "
  "arg(arg='provenance')], kwonlyargs=[], kw_defaults=[], defaults=[])",
  (),
  ''),
 ('_comparison',
  "arguments(posonlyargs=[], args=[arg(arg='payload'), arg(arg='value'), arg(arg='bundle')], kwonlyargs=[], "
  'kw_defaults=[], defaults=[])',
  (),
  ''),
 ('_coverage',
  "arguments(posonlyargs=[], args=[arg(arg='value')], kwonlyargs=[], kw_defaults=[], defaults=[])",
  (),
  ''),
 ('_definition',
  "arguments(posonlyargs=[], args=[arg(arg='path')], kwonlyargs=[], kw_defaults=[], defaults=[])",
  (),
  ''),
 ('_diagnostics',
  "arguments(posonlyargs=[], args=[arg(arg='payload'), arg(arg='messages'), arg(arg='family')], "
  'kwonlyargs=[], kw_defaults=[], defaults=[Constant(value=None)])',
  (),
  ''),
 ('_disclosure_base',
  "arguments(posonlyargs=[], args=[arg(arg='owner'), arg(arg='evidence_class'), arg(arg='method'), "
  "arg(arg='scope'), arg(arg='basis')], kwonlyargs=[], kw_defaults=[], defaults=[Constant(value=None)])",
  (),
  ''),
 ('_disclosure_recommend',
  "arguments(posonlyargs=[], args=[arg(arg='payload'), arg(arg='priority'), arg(arg='metadata'), "
  "arg(arg='scope'), arg(arg='unlock'), arg(arg='reason')], kwonlyargs=[], kw_defaults=[], defaults=[])",
  (),
  ''),
 ('_disclosure_scope',
  "arguments(posonlyargs=[], args=[arg(arg='payload')], kwonlyargs=[], kw_defaults=[], defaults=[])",
  (),
  ''),
 ('_disclosure_signal',
  "arguments(posonlyargs=[], args=[arg(arg='name'), arg(arg='owner'), arg(arg='basis'), arg(arg='paths'), "
  "arg(arg='present'), arg(arg='rule'), arg(arg='limitations')], kwonlyargs=[], kw_defaults=[], defaults=[])",
  (),
  ''),
 ('_disclosure_unavailable',
  "arguments(posonlyargs=[], args=[arg(arg='payload'), arg(arg='name'), arg(arg='owner'), "
  "arg(arg='capability'), arg(arg='statement'), arg(arg='reasons'), arg(arg='blockers'), "
  "arg(arg='next_metadata'), arg(arg='limit')], kwonlyargs=[], kw_defaults=[], defaults=[])",
  (),
  ''),
 ('_disclosures',
  "arguments(posonlyargs=[], args=[arg(arg='payload')], kwonlyargs=[], kw_defaults=[], defaults=[])",
  (),
  ''),
 ('_distribution',
  "arguments(posonlyargs=[], args=[arg(arg='payload'), arg(arg='value'), arg(arg='bundle')], "
  "kwonlyargs=[arg(arg='weighted'), arg(arg='coverage')], kw_defaults=[Constant(value=False), "
  'Constant(value=None)], defaults=[])',
  (),
  ''),
 ('_distribution_exclusions',
  "arguments(posonlyargs=[], args=[arg(arg='payload'), arg(arg='value')], kwonlyargs=[], kw_defaults=[], "
  'defaults=[])',
  (),
  ''),
 ('_duplicates',
  "arguments(posonlyargs=[], args=[arg(arg='payload'), arg(arg='value'), arg(arg='bundle')], kwonlyargs=[], "
  'kw_defaults=[], defaults=[])',
  (),
  ''),
 ('_envelope',
  "arguments(posonlyargs=[], args=[arg(arg='path'), arg(arg='value'), arg(arg='scope')], kwonlyargs=[], "
  "kw_defaults=[], kwarg=arg(arg='kwargs'), defaults=[])",
  (),
  ''),
 ('_extinction',
  "arguments(posonlyargs=[], args=[arg(arg='payload'), arg(arg='values')], kwonlyargs=[], kw_defaults=[], "
  'defaults=[])',
  (),
  ''),
 ('_inputs',
  "arguments(posonlyargs=[], args=[arg(arg='payload'), arg(arg='bundle')], kwonlyargs=[], kw_defaults=[], "
  'defaults=[])',
  (),
  ''),
 ('_key',
  "arguments(posonlyargs=[], args=[arg(arg='value')], kwonlyargs=[], kw_defaults=[], defaults=[])",
  (),
  ''),
 ('_lineage_observations',
  "arguments(posonlyargs=[], args=[arg(arg='payload'), arg(arg='bundle')], kwonlyargs=[], kw_defaults=[], "
  'defaults=[])',
  (),
  ''),
 ('_message_family',
  "arguments(posonlyargs=[], args=[arg(arg='message')], kwonlyargs=[], kw_defaults=[], defaults=[])",
  (),
  ''),
 ('_metadata',
  "arguments(posonlyargs=[], args=[arg(arg='value')], kwonlyargs=[arg(arg='name'), arg(arg='scope'), "
  "arg(arg='representation'), arg(arg='owner'), arg(arg='evidence'), arg(arg='unit'), arg(arg='formula'), "
  "arg(arg='weighting')], kw_defaults=[None, None, None, None, None, None, Constant(value=None), "
  'Constant(value=None)], defaults=[])',
  (),
  ''),
 ('_metadata_text',
  "arguments(posonlyargs=[], args=[arg(arg='value')], kwonlyargs=[], kw_defaults=[], defaults=[])",
  (),
  ''),
 ('_number',
  "arguments(posonlyargs=[], args=[arg(arg='value'), arg(arg='name')], kwonlyargs=[arg(arg='integer'), "
  "arg(arg='minimum'), arg(arg='maximum')], kw_defaults=[Constant(value=False), Constant(value=None), "
  'Constant(value=None)], defaults=[])',
  (),
  ''),
 ('_policy',
  "arguments(posonlyargs=[], args=[arg(arg='value')], kwonlyargs=[], kw_defaults=[], defaults=[])",
  (),
  ''),
 ('_provenance',
  "arguments(posonlyargs=[], args=[arg(arg='payload'), arg(arg='value'), arg(arg='bundle')], kwonlyargs=[], "
  'kw_defaults=[], defaults=[])',
  (),
  ''),
 ('_provenance_consistency',
  "arguments(posonlyargs=[], args=[arg(arg='value'), arg(arg='bundle')], kwonlyargs=[], kw_defaults=[], "
  'defaults=[])',
  (),
  ''),
 ('_representation',
  "arguments(posonlyargs=[], args=[arg(arg='value')], kwonlyargs=[], kw_defaults=[], defaults=[])",
  (),
  ''),
 ('_require',
  "arguments(posonlyargs=[], args=[arg(arg='condition'), arg(arg='message')], kwonlyargs=[], kw_defaults=[], "
  'defaults=[])',
  (),
  ''),
 ('_scalar',
  "arguments(posonlyargs=[], args=[arg(arg='path'), arg(arg='value'), arg(arg='scope'), "
  "arg(arg='representation'), arg(arg='bundle')], kwonlyargs=[arg(arg='name'), arg(arg='denominator'), "
  "arg(arg='coverage'), arg(arg='weighting'), arg(arg='limitations'), arg(arg='formula')], "
  'kw_defaults=[Constant(value=None), Constant(value=None), Constant(value=None), Constant(value=None), '
  'Tuple(elts=[], ctx=Load()), Constant(value=None)], defaults=[])',
  (),
  ''),
 ('_scope',
  "arguments(posonlyargs=[], args=[arg(arg='value'), arg(arg='bundle')], kwonlyargs=[], kw_defaults=[], "
  'defaults=[])',
  (),
  ''),
 ('_simulation_inputs',
  "arguments(posonlyargs=[], args=[arg(arg='value')], kwonlyargs=[], kw_defaults=[], defaults=[])",
  (),
  ''),
 ('_table',
  "arguments(posonlyargs=[], args=[arg(arg='path'), arg(arg='value'), arg(arg='metadata'), arg(arg='scope'), "
  "arg(arg='representation'), arg(arg='bundle')], kwonlyargs=[arg(arg='name'), arg(arg='status'), "
  "arg(arg='reasons'), arg(arg='denominator'), arg(arg='coverage'), arg(arg='weighting'), "
  "arg(arg='limitations'), arg(arg='formula')], kw_defaults=[None, None, Tuple(elts=[], ctx=Load()), "
  'Constant(value=None), Constant(value=None), Constant(value=None), Tuple(elts=[], ctx=Load()), '
  'Constant(value=None)], defaults=[])',
  (),
  ''),
 ('_tail',
  "arguments(posonlyargs=[], args=[arg(arg='payload'), arg(arg='value'), arg(arg='bundle')], kwonlyargs=[], "
  'kw_defaults=[], defaults=[])',
  (),
  ''),
 ('_typed',
  "arguments(posonlyargs=[], args=[arg(arg='value'), arg(arg='expected'), arg(arg='name')], kwonlyargs=[], "
  'kw_defaults=[], defaults=[])',
  (),
  ''),
 ('assemble_report',
  "arguments(posonlyargs=[], args=[arg(arg='bundle', annotation=Name(id='BundleValidationResult', "
  "ctx=Load()))], kwonlyargs=[arg(arg='run', annotation=Name(id='dict', ctx=Load())), "
  "arg(arg='distributions', annotation=Subscript(value=Name(id='tuple', ctx=Load()), "
  "slice=Tuple(elts=[BinOp(left=Name(id='StateDistributionResult', ctx=Load()), op=BitOr(), "
  "right=Name(id='DistributionMetrics', ctx=Load())), Constant(value=Ellipsis)], ctx=Load()), ctx=Load())), "
  "arg(arg='provenance', annotation=BinOp(left=Name(id='ProvenanceCompositionResult', ctx=Load()), "
  "op=BitOr(), right=Constant(value=None))), arg(arg='duplicates', "
  "annotation=BinOp(left=Name(id='ExactDuplicateResult', ctx=Load()), op=BitOr(), "
  "right=Constant(value=None))), arg(arg='tail', annotation=BinOp(left=Name(id='TailSelectionResult', "
  "ctx=Load()), op=BitOr(), right=Constant(value=None))), arg(arg='comparison', "
  "annotation=BinOp(left=Name(id='SupportComparison', ctx=Load()), op=BitOr(), right=Constant(value=None))), "
  "arg(arg='closure', annotation=BinOp(left=Name(id='DirectClosureExposureBounds', ctx=Load()), op=BitOr(), "
  "right=Constant(value=None))), arg(arg='expected_diversity', "
  "annotation=BinOp(left=Name(id='ExpectedDiversityResult', ctx=Load()), op=BitOr(), "
  "right=Constant(value=None))), arg(arg='resampling', annotation=BinOp(left=Name(id='ResamplingSimulation', "
  "ctx=Load()), op=BitOr(), right=Constant(value=None))), arg(arg='extinction', "
  "annotation=Subscript(value=Name(id='tuple', ctx=Load()), "
  "slice=Tuple(elts=[Name(id='ExtinctionProbabilityResult', ctx=Load()), Constant(value=Ellipsis)], "
  "ctx=Load()), ctx=Load())), arg(arg='family_errors', annotation=Subscript(value=Name(id='tuple', "
  "ctx=Load()), slice=Tuple(elts=[Name(id='FamilyFailure', ctx=Load()), Constant(value=Ellipsis)], "
  'ctx=Load()), ctx=Load()))], kw_defaults=[None, Tuple(elts=[], ctx=Load()), Constant(value=None), '
  'Constant(value=None), Constant(value=None), Constant(value=None), Constant(value=None), '
  'Constant(value=None), Constant(value=None), Tuple(elts=[], ctx=Load()), Tuple(elts=[], ctx=Load())], '
  'defaults=[])',
  (),
  'CanonicalReport')]

PHASE4_STEP3_ASSEMBLY_LITERAL_DECLARATIONS = [('_metadata_text', "allowed = ('sampled_path; sequential_binomial_complement_v1',)"),
 ('_metadata_text', 'allowed = methods.get(name, ())'),
 ('_metadata_text',
  "assumptions = ('Approved direct grounding partition; uncertainty remains unresolved.',)"),
 ('_metadata_text',
  "assumptions = ('Categorical multinomial sampling; positive explicit n; one-step horizon; no external "
  "reopening.' if value.evidence_class is CalculationEvidenceClass.SIMULATION else 'Explicit rule over "
  "positive observed unweighted count support.',)"),
 ('_metadata_text',
  "assumptions = ('Earlier and later scopes explicitly selected and independently validated.', 'State "
  "identity uses the declared common basis, including any disclosed map.')"),
 ('_metadata_text',
  "assumptions = ('Exact explicit single-version Phase 2 join scope; no representation exclusions.',)"),
 ('_metadata_text',
  "assumptions = ('Fixed finite declared state space and constant positive integer resample size.', 'X_t "
  "conditional on p_t is Multinomial(n,p_t); p_(t+1)=X_t/n.', 'No mutation, migration, independent real data "
  "or external corrective input.')"),
 ('_metadata_text',
  "assumptions = ('One explicitly selected version and declared representation.', 'No implicit pooling, "
  "probability repair, confidence weighting or sampling.')"),
 ('_metadata_text',
  "assumptions = ('exact_utf8_v1 and SHA-256; equal digests verified against exact bytes', 'one explicitly "
  "selected version; unweighted records')"),
 ('_metadata_text',
  "basis = ('empirical_assignments', 'explicit_counts_divided_by_included_records', 'weighted_record_mass', "
  "'explicit_probability_vector')"),
 ('_metadata_text',
  "limitations = ('Exact record form does not establish semantic identity or independent origin.',)"),
 ('_metadata_text',
  "limitations = ('Experimental conditional simulation; no calibrated production-failure probability.', "
  "'Diversity contraction holds in expectation, not monotonically on every sampled path.', 'Simulated steps "
  "are not record generations, training epochs or dataset releases.', 'No external-reference loss, "
  "reopening, lineage, risk score or audit workflow is implemented.', 'Floating-point and pseudorandom "
  "sampling are numerical realizations of the declared model.')"),
 ('_metadata_text',
  "limitations = ('Observed/supplied support only; no permanent extinction or causal/model-performance "
  "verdict.', 'A coarsened comparison cannot recover distinctions lost through its mapping.')"),
 ('_metadata_text',
  "limitations = ('Representation-bound; does not establish functional failure or semantic completeness.',)"),
 ('_metadata_text',
  "limitations = ('Representation-bound; no calibrated production-failure or universal risk conclusion.',)"),
 ('_metadata_text',
  "limitations = ('Supplied declarations only; no truth or source-independence certification.',)"),
 ('_metadata_text',
  "limitations = ('Toolkit operationalization relative to supplied metadata, without lineage or truth "
  "certification.',)"),
 ('_metadata_text',
  "methods = {'support_size': basis, 'gini_simpson_diversity': basis, 'simpson_concentration': basis, "
  "'state_frequency': basis + ('empirical_assignments; n_i/N',), 'state_count': tuple(('Definitions 7.1; ' + "
  "item for item in basis)) + ('count included record-state assignments',), 'state_mass': ('Definitions 9.5; "
  "canonical record weights summed within each state',), 'support_delta': ('later support_size minus earlier "
  "support_size',), 'support_loss_count': ('cardinality of earlier support minus later support',), "
  "'support_added_count': ('cardinality of later support minus earlier support',), "
  "'support_retention_ratio': ('intersection support size / earlier positive-mass support size',), "
  "'gini_simpson_diversity_delta': ('later Gini-Simpson diversity minus earlier diversity',), "
  "'extinct_states': ('earlier support minus later support',), 'added_states': ('later support minus earlier "
  "support',), 'retained_states': ('earlier support intersect later support',), 'source_type_counts': "
  "('Definitions 3.3/11.1; count declared canonical categories',), 'provenance_confidence_counts': "
  "('Definitions 3.3/11.1; count declared canonical categories',), 'source_type_shares': ('category count / "
  "all selected valid records',), 'source_type_field_coverage': ('Definitions 3.13; nonmissing valid field / "
  "all selected valid records',), 'provenance_confidence_field_coverage': ('Definitions 3.13; nonmissing "
  "valid field / all selected valid records',), 'provenance_row_coverage': ('Reuse Phase 2 coverage; "
  "Definitions 3.10-3.12',), 'provenance_required_field_coverage': ('Reuse Phase 2 coverage; Definitions "
  "3.10-3.12',), 'grounding_field_coverage': ('Reuse Phase 2 coverage; Definitions 3.10-3.12',), "
  "'analyzed_record_count': ('All selected valid records',), 'records_with_matching_rows': ('Phase 2 "
  "matched-row inventory',), 'missing_provenance_count': ('Phase 2 missing-row inventory',), "
  "'missing_provenance_share': ('Definitions 11.4; missing rows / all selected valid records',), "
  "'known_open_count': ('toolkit_operationalization; Definitions 3.7-3.9; P3-D08',), 'known_closed_count': "
  "('toolkit_operationalization; Definitions 3.7-3.9; P3-D08',), 'unresolved_grounding_count': "
  "('toolkit_operationalization; Definitions 3.7-3.9; P3-D08',), 'weighted_source_type_masses': "
  "('Definitions 19; sum explicit weights by source',), 'weighted_source_type_shares': ('F-007 weighted "
  "variant; category mass / all selected record weight mass',), 'total_weight': ('Definitions 19; all "
  "selected weights',), 'missing_provenance_weight': ('Definitions 19; missing-row mass',), "
  "'weighted_missing_provenance_share': ('Definitions 11.4/19; missing-row mass / all selected record weight "
  "mass',), 'duplicate_record_count': ('sum_group_size_minus_one; DEFINITIONS_AND_UNITS:8.3',), "
  "'duplicate_group_count': ('count_groups_of_size_greater_than_one; DEFINITIONS_AND_UNITS:8.4',), "
  "'rarity_rank': ('ascending frequency, then count, then Unicode state ID; 1-based ordinal',), "
  "'tail_support_size': tuple(('Definitions 10.1-10.6; explicit ' + rule for rule in ('singleton_count', "
  "'count_at_or_below', 'frequency_at_or_below', 'state_list'))), 'tail_membership': tuple(('Definitions "
  "10.1-10.6; explicit ' + rule for rule in ('singleton_count', 'count_at_or_below', "
  "'frequency_at_or_below', 'state_list'))), 'tail_record_share': tuple(('Definitions 10.1-10.6; explicit ' "
  "+ rule + '; selected counts / included records' for rule in ('singleton_count', 'count_at_or_below', "
  "'frequency_at_or_below', 'state_list'))), 'direct_closure_exposure_lower_bound': ('known_closed_count / "
  "total_record_count', 'no usable required-provenance row'), 'direct_closure_exposure_upper_bound': "
  "('(known_closed_count + unresolved_grounding_count) / total_record_count', 'no usable required-provenance "
  "row'), 'direct_closure_exposure_interval_width': ('upper_bound - lower_bound = unresolved_grounding_count "
  "/ total_record_count', 'no usable required-provenance row'), 'one_step_extinction_probability': ('F-014; "
  "(1-p_i)^n; analytic one-step closed multinomial',), 'expected_gini_simpson_diversity': "
  "('analytic_expectation; D0*(1-1/n)**t; t=0..steps; constant n',)}"),
 ('_metadata_text', 'name = value.metric_name'),
 ('_metadata_text',
  "pair_names = ('support_delta', 'support_loss_count', 'support_added_count', 'support_retention_ratio', "
  "'gini_simpson_diversity_delta', 'extinct_states', 'added_states', 'retained_states')")]

PHASE4_STEP3_ASSEMBLY_LITERAL_CONTAINERS = [('_bundle_check', "('source_type', 'external_grounding', 'provenance_confidence')"),
 ('_capabilities',
  "('Input eligibility is distinct from executed analysis; Phase 5 lineage remains deferred.',)"),
 ('_capabilities', "('partial', ['R_LONGITUDINAL_FAMILIES_DEFERRED'])"),
 ('_capabilities', "['R_INPUT_VALIDATION_ERROR']"),
 ('_capabilities', "['R_LONGITUDINAL_FAMILIES_DEFERRED']"),
 ('_capabilities',
  "{'content': 'record_coverage', 'representation': 'representation_coverage', 'row': "
  "'provenance_row_coverage', 'required_fields': 'provenance_required_field_coverage', 'grounding': "
  "'grounding_field_coverage'}"),
 ('_closed_simulation',
  "('Fixed finite declared state space and constant positive integer resample size.', 'X_t conditional on "
  "p_t is Multinomial(n,p_t); p_(t+1)=X_t/n.', 'No mutation, migration, independent real data or external "
  "corrective input.')"),
 ('_closed_simulation', "('gini_simpson_diversity', 'F-003', 'ratio')"),
 ('_closed_simulation', "('state_count', None, 'sampled_records')"),
 ('_closed_simulation', "('state_frequency', 'F-001', 'ratio')"),
 ('_closed_simulation', "('support_size', 'F-002', 'states')"),
 ('_closed_simulation',
  "(('state_count', None, 'sampled_records'), ('state_frequency', 'F-001', 'ratio'), ('support_size', "
  "'F-002', 'states'), ('gini_simpson_diversity', 'F-003', 'ratio'))"),
 ('_closed_simulation',
  "['Extinction events are not separately inferred by the assembly adapter; inspect the supplied sampled "
  "support paths.']"),
 ('_comparison', "('earlier', 'later')"),
 ('_comparison', "('earlier_to_later', 'later_to_earlier')"),
 ('_comparison', "('extinct_states', 'added_states', 'retained_states')"),
 ('_comparison', "{'observed_facts': {}, 'derived_metrics': {}}"),
 ('_comparison', "{'observed_facts': {}, 'derived_metrics': {}}"),
 ('_disclosure_base', "('T1', 'T2', 'T3', 'T4', 'T5', 'T6')"),
 ('_disclosure_recommend', "['PR-014']"),
 ('_disclosure_scope',
  "{'dataset_versions': [], 'record_count': None, 'excluded_record_count': None, 'denominator_basis': "
  "'no_selected_record_scope_supplied', 'scope_id': 'report_inputs'}"),
 ('_disclosure_unavailable',
  "['Unavailable means the supplied evidence does not support this conclusion; it does not establish that "
  "the conclusion is false.']"),
 ('_disclosures',
  "('R_PARENT_UNRESOLVED', 'R_PARENT_AMBIGUOUS', 'R_PARENT_DECLARATION_MISSING', 'R_PARENT_INVALID')"),
 ('_disclosures', "('available', 'partial')"),
 ('_disclosures', "('available', 'partial')"),
 ('_disclosures', "('available', 'partial')"),
 ('_disclosures', "('available', 'partial')"),
 ('_disclosures', "('external_ancestry', 'T4', 'External ancestry results are deferred to Phase 5.')"),
 ('_disclosures',
  "('grounding_field_coverage', 'external_grounding', 'records whose grounding remains unresolved', 'a "
  "narrower direct closure exposure interval when the additional evidence resolves grounding')"),
 ('_disclosures', "('lineage_analysis', 'PR-014', 'General lineage graph analysis is deferred to Phase 5.')"),
 ('_disclosures', "('lineage_closure_exposure', 'T3', 'Lineage closure exposure is deferred to Phase 5.')"),
 ('_disclosures',
  "('provenance_required_field_coverage', 'required_provenance_fields', 'records lacking usable required "
  "provenance', 'usable declared provenance without discarding independently valid calculations')"),
 ('_disclosures',
  "('provenance_row_coverage', 'provenance_required_field_coverage', 'grounding_field_coverage')"),
 ('_disclosures', "('support', 'diversity', 'tail')"),
 ('_disclosures', "('support', 'diversity', 'tail')"),
 ('_disclosures',
  "(('lineage_analysis', 'PR-014', 'General lineage graph analysis is deferred to Phase 5.'), "
  "('lineage_closure_exposure', 'T3', 'Lineage closure exposure is deferred to Phase 5.'), "
  "('external_ancestry', 'T4', 'External ancestry results are deferred to Phase 5.'))"),
 ('_disclosures',
  "(('provenance_required_field_coverage', 'required_provenance_fields', 'records lacking usable required "
  "provenance', 'usable declared provenance without discarding independently valid calculations'), "
  "('grounding_field_coverage', 'external_grounding', 'records whose grounding remains unresolved', 'a "
  "narrower direct closure exposure interval when the additional evidence resolves grounding'))"),
 ('_disclosures', "['A bounded operational definition and evidence matched to that definition.']"),
 ('_disclosures', "['A controlled empirical intervention design with measured comparable outcomes.']"),
 ('_disclosures',
  "['A separately defined bounded outcome and appropriately validated predictive evidence.']"),
 ('_disclosures',
  "['A stated production-failure criterion and corresponding versioned outcome measurements.']"),
 ('_disclosures',
  "['An explicit pipeline boundary and evidence for its relevant external inputs and transformations.']"),
 ('_disclosures',
  "['An identified ancestor, measured outcomes and a controlled or otherwise justified causal design.']"),
 ('_disclosures',
  "['Direct closure exposure describes the selected declared grounding scope, without tracing every pipeline "
  "input.']"),
 ('_disclosures',
  "['Each coverage keeps its own field meaning and denominator.', 'This signal reports unresolved supplied "
  "provenance evidence and does not estimate factual truth or source independence.', 'A not_present signal "
  "is limited to the cited fields and does not certify universal integrity.']"),
 ('_disclosures', "['No accepted versioned model-outcome analysis is supplied.']"),
 ('_disclosures', "['No operational failure outcome is measured by these structural fields.']"),
 ('_disclosures', "['No universal collapse prediction is defined by the approved toolkit.']"),
 ('_disclosures',
  "['Only existing reference validation observations can be reported; no graph traversal, root tracing or "
  "ancestry metric executes.']"),
 ('_disclosures',
  "['Phase 4 does not compute ancestry; topology alone would not identify a causal contribution.']"),
 ('_disclosures',
  "['Preserve explicit composite parent references, chronology and external-grounding metadata for the "
  "future Phase 5 analysis.']"),
 ('_disclosures', "['R_CAUSAL_EVIDENCE_MISSING', 'R_LINEAGE_EXECUTION_DEFERRED']"),
 ('_disclosures', "['R_CONTROLLED_EMPIRICAL_DESIGN_MISSING']"),
 ('_disclosures', "['R_LINEAGE_EXECUTION_DEFERRED']"),
 ('_disclosures', "['R_MODEL_EVIDENCE_MISSING']"),
 ('_disclosures', "['R_OUTCOME_EVIDENCE_MISSING']"),
 ('_disclosures', "['R_OUTSIDE_PRODUCT_SCOPE']"),
 ('_disclosures', "['R_PIPELINE_BOUNDARY_EVIDENCE_MISSING']"),
 ('_disclosures', "['R_UNIVERSAL_OPERATIONAL_DEFINITION_ABSENT']"),
 ('_disclosures', "['Supplied scenario outputs are conditional mathematical or stochastic results.']"),
 ('_disclosures',
  "['Tail membership depends on the explicit rule and selected representation.', 'This signal is not a "
  "calibrated forecast of the production pipeline.', 'No simulation is run by this signal, and tail "
  "membership does not establish importance or harm.']"),
 ('_disclosures',
  "['The signal is restricted to the selected versions and their declared common state meaning.', 'An "
  'observed support decrease does not establish model-performance decline, production failure or universal '
  "collapse.']"),
 ('_disclosures', "['This product defines no universal integrity scalar or operational test.']"),
 ('_disclosures', "['Versioned model evaluation outcomes with comparable tasks and evaluation conditions.']"),
 ('_disclosures', "['derived_metrics.support.support_delta']"),
 ('_disclosures', "['derived_metrics.tail.tail_support_size', 'derived_metrics.tail.selection']"),
 ('_disclosures',
  "['eligibility for an explicitly requested comparison after state-meaning compatibility is supplied']"),
 ('_disclosures', "['evidence needed by a future model-longitudinal implementation']"),
 ('_disclosures', "['more complete declared provenance coverage']"),
 ('_disclosures', "['more complete immediate-parent validation; future Phase 5 analysis remains deferred']"),
 ('_disclosures', "['representation-dependent support, diversity and tail diagnostics']"),
 ('_distribution', "('empirical_assignments', 'explicit_counts_divided_by_included_records')"),
 ('_distribution',
  "('empirical_assignments', 'explicit_counts_divided_by_included_records', 'weighted_record_mass', "
  "'explicit_probability_vector')"),
 ('_distribution_exclusions', "('derived_metrics', 'diversity')"),
 ('_distribution_exclusions', "('derived_metrics', 'support')"),
 ('_distribution_exclusions', "('state_counts', 'supplied_state_probabilities')"),
 ('_distribution_exclusions', "(('derived_metrics', 'support'), ('derived_metrics', 'diversity'))"),
 ('_duplicates', "('usable_exact_content',)"),
 ('_inputs', "('R_CALC_EMPTY_SCOPE',)"),
 ('_inputs', "('Validation coverage describes supplied declarations without certifying their truth.',)"),
 ('_inputs', "('nonempty_validated_record_scope',)"),
 ('_inputs',
  "['Input hashes identify supplied bytes and do not certify authenticity.', 'Only allowlisted evidence "
  "fields are assembled; raw content, extras, notes and embeddings are not exported.']"),
 ('_inputs', "['R_INVENTORY_ONLY_ROLE']"),
 ('_lineage_observations',
  "('Counts preserve validation reference-entry multiplicity; they do not describe an ancestry graph.',)"),
 ('_lineage_observations',
  "('Immediate-reference validation coverage does not establish resolved ancestry or external roots.',)"),
 ('_lineage_observations', "('No general graph-cycle traversal executes in Phase 4.',)"),
 ('_lineage_observations', "('Phase_5_graph_analysis',)"),
 ('_lineage_observations', "('R_GRAPH_EXECUTION_DEFERRED',)"),
 ('_lineage_observations', "('R_NO_DECLARED_PARENT_ENTRIES',)"),
 ('_lineage_observations',
  "('This retained earlier-version ordering certificate is not general graph-cycle traversal.',)"),
 ('_lineage_observations', "('declared_parent_reference_entries',)"),
 ('_message_family',
  "('E_PARENT_AMBIGUOUS', 'E_PARENT_FORMAT', 'E_PARENT_FUTURE_VERSION', 'E_LINEAGE_CYCLE', "
  "'W_GENERATION_MISMATCH')"),
 ('_message_family', "('parent_ids', 'generation')"),
 ('_message_family', "('representation', 'topic', 'embedding_cluster', 'content', 'content_ref')"),
 ('_message_family', "('source_type', 'provenance_confidence', 'external_grounding')"),
 ('_message_family', "('version_order', 'pair_order', 'representation_compatibility')"),
 ('_message_family', "['content_diagnostics']"),
 ('_message_family', "['dataset_longitudinal']"),
 ('_message_family', "['ingestion']"),
 ('_message_family', "['lineage']"),
 ('_message_family', "['provenance']"),
 ('_metadata_text',
  "('(known_closed_count + unresolved_grounding_count) / total_record_count', 'no usable required-provenance "
  "row')"),
 ('_metadata_text', "('All selected valid records',)"),
 ('_metadata_text', "('Approved direct grounding partition; uncertainty remains unresolved.',)"),
 ('_metadata_text', "('Definitions 11.4/19; missing-row mass / all selected record weight mass',)"),
 ('_metadata_text', "('Definitions 11.4; missing rows / all selected valid records',)"),
 ('_metadata_text', "('Definitions 19; all selected weights',)"),
 ('_metadata_text', "('Definitions 19; missing-row mass',)"),
 ('_metadata_text', "('Definitions 19; sum explicit weights by source',)"),
 ('_metadata_text', "('Definitions 3.13; nonmissing valid field / all selected valid records',)"),
 ('_metadata_text', "('Definitions 3.13; nonmissing valid field / all selected valid records',)"),
 ('_metadata_text', "('Definitions 3.3/11.1; count declared canonical categories',)"),
 ('_metadata_text', "('Definitions 3.3/11.1; count declared canonical categories',)"),
 ('_metadata_text', "('Definitions 9.5; canonical record weights summed within each state',)"),
 ('_metadata_text',
  "('Earlier and later scopes explicitly selected and independently validated.', 'State identity uses the "
  "declared common basis, including any disclosed map.')"),
 ('_metadata_text', "('Exact explicit single-version Phase 2 join scope; no representation exclusions.',)"),
 ('_metadata_text', "('Exact record form does not establish semantic identity or independent origin.',)"),
 ('_metadata_text',
  "('Experimental conditional simulation; no calibrated production-failure probability.', 'Diversity "
  "contraction holds in expectation, not monotonically on every sampled path.', 'Simulated steps are not "
  "record generations, training epochs or dataset releases.', 'No external-reference loss, reopening, "
  "lineage, risk score or audit workflow is implemented.', 'Floating-point and pseudorandom sampling are "
  "numerical realizations of the declared model.')"),
 ('_metadata_text', "('F-007 weighted variant; category mass / all selected record weight mass',)"),
 ('_metadata_text', "('F-014; (1-p_i)^n; analytic one-step closed multinomial',)"),
 ('_metadata_text',
  "('Fixed finite declared state space and constant positive integer resample size.', 'X_t conditional on "
  "p_t is Multinomial(n,p_t); p_(t+1)=X_t/n.', 'No mutation, migration, independent real data or external "
  "corrective input.')"),
 ('_metadata_text',
  "('Observed/supplied support only; no permanent extinction or causal/model-performance verdict.', 'A "
  "coarsened comparison cannot recover distinctions lost through its mapping.')"),
 ('_metadata_text',
  "('One explicitly selected version and declared representation.', 'No implicit pooling, probability "
  "repair, confidence weighting or sampling.')"),
 ('_metadata_text', "('Phase 2 matched-row inventory',)"),
 ('_metadata_text', "('Phase 2 missing-row inventory',)"),
 ('_metadata_text',
  "('Representation-bound; does not establish functional failure or semantic completeness.',)"),
 ('_metadata_text',
  "('Representation-bound; no calibrated production-failure or universal risk conclusion.',)"),
 ('_metadata_text', "('Reuse Phase 2 coverage; Definitions 3.10-3.12',)"),
 ('_metadata_text', "('Reuse Phase 2 coverage; Definitions 3.10-3.12',)"),
 ('_metadata_text', "('Reuse Phase 2 coverage; Definitions 3.10-3.12',)"),
 ('_metadata_text', "('Supplied declarations only; no truth or source-independence certification.',)"),
 ('_metadata_text',
  "('Toolkit operationalization relative to supplied metadata, without lineage or truth certification.',)"),
 ('_metadata_text', "('analytic_expectation; D0*(1-1/n)**t; t=0..steps; constant n',)"),
 ('_metadata_text', "('ascending frequency, then count, then Unicode state ID; 1-based ordinal',)"),
 ('_metadata_text', "('cardinality of earlier support minus later support',)"),
 ('_metadata_text', "('cardinality of later support minus earlier support',)"),
 ('_metadata_text', "('category count / all selected valid records',)"),
 ('_metadata_text', "('count included record-state assignments',)"),
 ('_metadata_text', "('count_groups_of_size_greater_than_one; DEFINITIONS_AND_UNITS:8.4',)"),
 ('_metadata_text', "('earlier support intersect later support',)"),
 ('_metadata_text', "('earlier support minus later support',)"),
 ('_metadata_text',
  "('empirical_assignments', 'explicit_counts_divided_by_included_records', 'weighted_record_mass', "
  "'explicit_probability_vector')"),
 ('_metadata_text', "('empirical_assignments; n_i/N',)"),
 ('_metadata_text',
  "('exact_utf8_v1 and SHA-256; equal digests verified against exact bytes', 'one explicitly selected "
  "version; unweighted records')"),
 ('_metadata_text', "('intersection support size / earlier positive-mass support size',)"),
 ('_metadata_text', "('known_closed_count / total_record_count', 'no usable required-provenance row')"),
 ('_metadata_text', "('later Gini-Simpson diversity minus earlier diversity',)"),
 ('_metadata_text', "('later support minus earlier support',)"),
 ('_metadata_text', "('later support_size minus earlier support_size',)"),
 ('_metadata_text', "('sampled_path; sequential_binomial_complement_v1',)"),
 ('_metadata_text', "('singleton_count', 'count_at_or_below', 'frequency_at_or_below', 'state_list')"),
 ('_metadata_text', "('singleton_count', 'count_at_or_below', 'frequency_at_or_below', 'state_list')"),
 ('_metadata_text', "('singleton_count', 'count_at_or_below', 'frequency_at_or_below', 'state_list')"),
 ('_metadata_text', "('state_count', 'state_frequency', 'support_size', 'gini_simpson_diversity')"),
 ('_metadata_text', "('sum_group_size_minus_one; DEFINITIONS_AND_UNITS:8.3',)"),
 ('_metadata_text',
  "('support_delta', 'support_loss_count', 'support_added_count', 'support_retention_ratio', "
  "'gini_simpson_diversity_delta', 'extinct_states', 'added_states', 'retained_states')"),
 ('_metadata_text', "('toolkit_operationalization; Definitions 3.7-3.9; P3-D08',)"),
 ('_metadata_text', "('toolkit_operationalization; Definitions 3.7-3.9; P3-D08',)"),
 ('_metadata_text', "('toolkit_operationalization; Definitions 3.7-3.9; P3-D08',)"),
 ('_metadata_text',
  "('upper_bound - lower_bound = unresolved_grounding_count / total_record_count', 'no usable "
  "required-provenance row')"),
 ('_provenance_consistency', "('confirmed', 'log_derived', 'estimated', 'unknown')"),
 ('_provenance_consistency', "('human', 'synthetic', 'mixed', 'sensor', 'unknown')"),
 ('_provenance_consistency', "('known_closed', 'valid_direct_grounding_no', ())"),
 ('_provenance_consistency', "('known_open', 'valid_direct_grounding_yes', ())"),
 ('_provenance_consistency', "('unresolved_grounding', 'declared_unknown_grounding', ())"),
 ('_provenance_consistency', "('unresolved_grounding', 'missing_provenance_row', ())"),
 ('_scalar', "('valid_nonempty_input_for_declared_scope',)"),
 ('_table', "('valid_nonempty_input_for_declared_scope',)"),
 ('assemble_report', "['existing_bundle_validation']")]

PHASE4_STEP3_ASSEMBLY_CALLS = {'FamilyFailure': ['dataclass'],
 'FamilyFailure.__post_init__': ['ReportAssemblyError', 'ReportAssemblyError', 'any', 'type', 'type', 'type'],
 '_base': ['_definition',
           'dict.fromkeys',
           'dict.fromkeys',
           'dict.fromkeys',
           'dict.fromkeys',
           'field.owner.startswith',
           'list',
           'list',
           'list',
           'list'],
 '_bundle_check': ['_coverage',
                   '_coverage',
                   '_coverage',
                   '_require',
                   '_require',
                   '_require',
                   '_require',
                   '_require',
                   '_require',
                   '_require',
                   '_require',
                   '_require',
                   '_require',
                   '_require',
                   '_require',
                   '_require',
                   '_require',
                   '_require',
                   '_require',
                   '_require',
                   '_require',
                   '_require',
                   '_require',
                   '_require',
                   '_require',
                   '_require',
                   '_require',
                   '_typed',
                   '_typed',
                   '_typed',
                   '_typed',
                   '_typed',
                   '_typed',
                   '_typed',
                   '_typed',
                   '_typed',
                   '_typed',
                   '_typed',
                   '_typed',
                   '_typed',
                   '_typed',
                   '_typed',
                   '_typed',
                   'all',
                   'all',
                   'all',
                   'all',
                   'all',
                   'all',
                   'all',
                   'all',
                   'all',
                   'all',
                   'assessment.capabilities.items',
                   'capability.coverage_details.values',
                   'len',
                   'len',
                   'len',
                   'len',
                   'len',
                   'row.values.get',
                   'row.values.get',
                   'set',
                   'set',
                   'set',
                   'set',
                   'set',
                   'set',
                   'sum',
                   'sum',
                   'sum',
                   'type',
                   'type',
                   'type',
                   'type',
                   'type',
                   'type',
                   'type',
                   'type',
                   'type',
                   'type',
                   'type',
                   'type',
                   'type',
                   'type',
                   'type',
                   'type',
                   'type',
                   'type',
                   'type',
                   'type',
                   'type',
                   'type',
                   'type',
                   'type',
                   'type',
                   'type',
                   'type',
                   'type',
                   'type',
                   'type',
                   'type'],
 '_bundle_scope': ['_key', 'len', 'list'],
 '_capabilities': ['_coverage',
                   '_coverage',
                   '_coverage',
                   '_coverage',
                   '_require',
                   '_require',
                   '_typed',
                   '_typed',
                   'any',
                   'dict.fromkeys',
                   'dict.fromkeys',
                   'dict.fromkeys',
                   "entry['notes'].append",
                   "entry['notes'].append",
                   'list',
                   'list',
                   'list',
                   'list',
                   'list',
                   'list',
                   'list',
                   'list',
                   'list',
                   'matrix.values',
                   'original.coverage_details.items',
                   'reasons.append',
                   'set',
                   'set',
                   'type'],
 '_closed_simulation': ['WeightingOptions',
                        'WeightingOptions',
                        '_base',
                        '_metadata',
                        '_metadata',
                        '_policy',
                        '_representation',
                        '_require',
                        '_require',
                        '_require',
                        '_require',
                        '_require',
                        '_require',
                        '_require',
                        '_require',
                        '_require',
                        '_require',
                        '_require',
                        '_require',
                        '_require',
                        '_require',
                        '_scope',
                        '_simulation_inputs',
                        '_typed',
                        '_typed',
                        'dict.fromkeys',
                        'generations.append',
                        'len',
                        'len',
                        'len',
                        'len',
                        'len',
                        'len',
                        'list',
                        'list',
                        'list',
                        'list',
                        'list',
                        'list',
                        'list',
                        'list',
                        'paths.append',
                        'range',
                        'range',
                        'set',
                        'set',
                        'target.update',
                        'target.update',
                        'trajectories.append',
                        'tuple',
                        'type',
                        'type',
                        'zip'],
 '_closure': ['_coverage',
              '_number',
              '_require',
              '_require',
              '_require',
              '_require',
              '_require',
              '_require',
              '_require',
              '_require',
              '_scalar',
              '_scope',
              '_typed',
              'len',
              "payload['derived_metrics'].setdefault",
              'set',
              'set',
              'sum'],
 '_comparison': ['_distribution',
                 '_distribution',
                 '_envelope',
                 '_representation',
                 '_representation',
                 '_representation',
                 '_representation',
                 '_require',
                 '_require',
                 '_require',
                 '_require',
                 '_require',
                 '_require',
                 '_require',
                 '_require',
                 '_require',
                 '_require',
                 '_require',
                 '_require',
                 '_require',
                 '_require',
                 '_require',
                 '_require',
                 '_require',
                 '_require',
                 '_require',
                 '_require',
                 '_require',
                 '_require',
                 '_require',
                 '_scalar',
                 '_scalar',
                 '_scope',
                 '_table',
                 '_typed',
                 '_typed',
                 '_typed',
                 '_typed',
                 '_typed',
                 '_typed',
                 '_typed',
                 '_typed',
                 'effects.append',
                 'len',
                 'len',
                 'len',
                 'list',
                 'list',
                 'list',
                 'list',
                 'list',
                 'list',
                 'list',
                 'mapping.state_mapping.items',
                 'order.index',
                 'order.index',
                 "payload['derived_metrics'].setdefault",
                 "payload['derived_metrics'].setdefault",
                 'support.values',
                 'type',
                 'type',
                 'zip'],
 '_coverage': ['_number', '_number', '_require', '_typed'],
 '_definition': ['ReportAssemblyError'],
 '_diagnostics': ['_key',
                  '_key',
                  '_message_family',
                  '_require',
                  '_require',
                  '_require',
                  '_typed',
                  '_typed',
                  "payload['errors'].append",
                  "payload['inputs']['limitations'].append",
                  "payload['warnings'].append",
                  'type',
                  'type',
                  'type',
                  'type',
                  'type'],
 '_disclosure_recommend': ["payload['recommended_next_metadata'].append"],
 '_disclosure_scope': ["payload['inputs'].get"],
 '_disclosure_signal': ['_disclosure_base', 'dict.fromkeys', 'list', 'list', 'list', 'result.update'],
 '_disclosure_unavailable': ['_disclosure_base',
                             '_disclosure_scope',
                             "payload['unavailable_conclusions'].append",
                             'result.update'],
 '_disclosures': ['_disclosure_recommend',
                  '_disclosure_recommend',
                  '_disclosure_recommend',
                  '_disclosure_recommend',
                  '_disclosure_recommend',
                  '_disclosure_recommend',
                  '_disclosure_signal',
                  '_disclosure_signal',
                  '_disclosure_signal',
                  '_disclosure_unavailable',
                  '_disclosure_unavailable',
                  '_disclosure_unavailable',
                  '_disclosure_unavailable',
                  '_disclosure_unavailable',
                  '_disclosure_unavailable',
                  '_disclosure_unavailable',
                  '_disclosure_unavailable',
                  'any',
                  'any',
                  'any',
                  'basis.append',
                  'basis.append',
                  'content_cap.get',
                  'derived.get',
                  'derived.get',
                  'derived.get',
                  "derived.get('closure_exposure', {}).get",
                  'direct.get',
                  'list',
                  'longitudinal_cap.get',
                  'paths.append',
                  'paths.append',
                  "payload['capabilities'].get",
                  "payload['capabilities'].get",
                  "payload['capabilities'].get",
                  "payload['observed_facts'].get",
                  'provenance.get',
                  'provenance.get',
                  'provenance.get',
                  'provenance.get',
                  'reasons.extend',
                  'set',
                  'set',
                  'support.get',
                  'tail.get'],
 '_distribution': ['WeightingOptions',
                   '_envelope',
                   '_number',
                   '_number',
                   '_number',
                   '_number',
                   '_policy',
                   '_representation',
                   '_require',
                   '_require',
                   '_require',
                   '_require',
                   '_require',
                   '_require',
                   '_require',
                   '_require',
                   '_require',
                   '_require',
                   '_require',
                   '_require',
                   '_require',
                   '_require',
                   '_require',
                   '_require',
                   '_require',
                   '_require',
                   '_require',
                   '_require',
                   '_require',
                   '_require',
                   '_require',
                   '_scalar',
                   '_scope',
                   '_table',
                   '_table',
                   '_table',
                   '_table',
                   '_typed',
                   '_typed',
                   '_typed',
                   'all',
                   'all',
                   'all',
                   'all',
                   'isclose',
                   'len',
                   'len',
                   'len',
                   'len',
                   'len',
                   'len',
                   "payload['derived_metrics'].setdefault",
                   "payload['derived_metrics'].setdefault",
                   "payload['derived_metrics'].setdefault('diversity', {}).setdefault",
                   "payload['derived_metrics'].setdefault('diversity', {}).setdefault('by_version', "
                   '{}).setdefault',
                   "payload['derived_metrics'].setdefault('support', {}).setdefault",
                   "payload['derived_metrics'].setdefault('support', {}).setdefault('by_version', "
                   '{}).setdefault',
                   "payload['observed_facts'].setdefault",
                   "payload['observed_facts'].setdefault",
                   "payload['observed_facts'].setdefault('state_counts', {}).setdefault",
                   "payload['observed_facts'].setdefault('supplied_state_probabilities', {}).setdefault",
                   'set',
                   'sum',
                   'sum',
                   'type',
                   'type',
                   'type',
                   'type',
                   'type'],
 '_distribution_exclusions': ['_key',
                              '_require',
                              '_require',
                              '_require',
                              'all',
                              'exclusions.append',
                              'len',
                              'len',
                              "payload['observed_facts'].get",
                              "payload['observed_facts'].get(family, {}).get",
                              "payload['observed_facts'].get(family, {}).get('by_version', {}).get",
                              'payload[section].get',
                              'payload[section].get(family, {}).get',
                              "payload[section].get(family, {}).get('by_version', {}).get",
                              "payload[section].get(family, {}).get('by_version', {}).get(version, "
                              '{}).values',
                              'set',
                              'type',
                              'type',
                              'type'],
 '_duplicates': ['_coverage',
                 '_envelope',
                 '_key',
                 '_representation',
                 '_require',
                 '_require',
                 '_require',
                 '_require',
                 '_require',
                 '_scalar',
                 '_scope',
                 '_typed',
                 '_typed',
                 'enumerate',
                 'groups.append',
                 'len',
                 'len',
                 'len',
                 'len',
                 'len',
                 "payload['observed_facts'].setdefault",
                 'seen.intersection',
                 'seen.update',
                 'set',
                 'set',
                 'set',
                 'set',
                 'str',
                 'sum',
                 'tuple'],
 '_envelope': ['_base'],
 '_extinction': ['ScalarCalculation',
                 'WeightingOptions',
                 '_base',
                 '_metadata',
                 '_policy',
                 '_representation',
                 '_require',
                 '_require',
                 '_require',
                 '_require',
                 '_require',
                 '_scope',
                 '_typed',
                 '_typed',
                 'target.update',
                 "target['initial_distribution'].append",
                 "target['parameters']['state_order'].append",
                 'type'],
 '_inputs': ['_bundle_scope',
             '_coverage',
             '_diagnostics',
             '_diagnostics',
             '_diagnostics',
             '_diagnostics',
             '_envelope',
             '_envelope',
             '_key',
             '_key',
             '_require',
             '_require',
             '_require',
             'affected.append',
             'any',
             'dict.fromkeys',
             'enumerate',
             'hashes.add',
             'iter',
             'len',
             'len',
             'len',
             'len',
             'len',
             'len',
             'len',
             'len',
             'list',
             'list',
             'list',
             'list',
             'messages_by_location.get',
             'messages_by_location.get',
             'messages_by_location.get',
             'messages_by_location.setdefault',
             'messages_by_location.setdefault((message.file_role, message.file_path), []).append',
             'next',
             'operations.append',
             "payload['inputs']['artifacts'].append",
             "payload['inputs']['file_hashes'].append",
             'records_by_version.get',
             'records_by_version.setdefault',
             'records_by_version.setdefault(row.record_key.dataset_version, []).append',
             'set',
             'set',
             'set',
             'sorted',
             'str',
             'str',
             'str',
             'tuple',
             'tuple',
             'tuple',
             'type',
             'unmapped.update',
             'versions_by_location.get',
             'versions_by_location.setdefault',
             'versions_by_location.setdefault((row.location.file_role, row.location.file_path), set()).add'],
 '_key': ['_typed'],
 '_lineage_observations': ['_coverage', '_envelope', '_envelope', '_envelope', '_envelope', 'list'],
 '_metadata': ['CalculationMetadata',
               'WeightingOptions',
               'WeightingOptions',
               '_metadata_text',
               '_require',
               '_require',
               '_require',
               '_require',
               '_require',
               '_typed',
               '_typed',
               'type',
               'type'],
 '_metadata_text': ['_require',
                    '_require',
                    '_require',
                    '_require',
                    'all',
                    'all',
                    'methods.get',
                    'name.startswith',
                    'tuple',
                    'tuple',
                    'tuple',
                    'tuple',
                    'type',
                    'type',
                    'type',
                    'type'],
 '_number': ['_require', '_require', '_require', '_require', 'isfinite', 'type', 'type'],
 '_policy': ['NumericalPolicy', '_typed'],
 '_provenance': ['WeightingOptions',
                 '_coverage',
                 '_coverage',
                 '_provenance_consistency',
                 '_require',
                 '_require',
                 '_require',
                 '_require',
                 '_require',
                 '_require',
                 '_require',
                 '_scalar',
                 '_scalar',
                 '_scalar',
                 '_scalar',
                 '_scope',
                 '_table',
                 '_table',
                 '_table',
                 '_table',
                 '_table',
                 '_typed',
                 '_typed',
                 '_typed',
                 '_typed',
                 'all',
                 'dict',
                 'dict',
                 'dict',
                 'len',
                 'len',
                 'len',
                 'len',
                 "payload['derived_metrics'].setdefault",
                 "payload['observed_facts'].setdefault",
                 'set',
                 'sum',
                 'type',
                 'type',
                 'zip'],
 '_provenance_consistency': ['_coverage',
                             '_require',
                             '_require',
                             '_require',
                             '_require',
                             '_require',
                             '_require',
                             '_require',
                             '_require',
                             '_require',
                             '_require',
                             '_require',
                             '_require',
                             '_require',
                             '_require',
                             '_require',
                             '_require',
                             '_require',
                             '_typed',
                             '_typed',
                             'all',
                             'any',
                             'dict',
                             'expected.values',
                             'len',
                             'len',
                             'len',
                             'len',
                             'len',
                             'len',
                             'len',
                             'len',
                             'len',
                             'len',
                             'len',
                             'match.provenance.values.get',
                             'match.provenance.values.get',
                             'set',
                             'set',
                             'set',
                             'set',
                             'set',
                             'set',
                             'set',
                             'set',
                             'sum',
                             'sum',
                             'sum',
                             'sum',
                             'sum',
                             'sum',
                             'tuple',
                             'tuple',
                             'tuple',
                             'tuple',
                             'type',
                             'type',
                             'type',
                             'zip'],
 '_representation': ['RepresentationDescriptor', '_typed'],
 '_require': ['ReportAssemblyError'],
 '_scalar': ['CalculationEvidenceClass',
             'ScalarCalculation',
             '_definition',
             '_envelope',
             '_metadata',
             '_representation',
             '_scope',
             '_typed',
             'field.method_id.startswith',
             'path.rsplit',
             'tuple',
             'tuple'],
 '_scope': ['CalculationScope',
            '_key',
            '_key',
            '_require',
            '_require',
            '_typed',
            'len',
            'len',
            'list',
            'set',
            'set',
            'set'],
 '_simulation_inputs': ['_number',
                        '_policy',
                        '_representation',
                        '_require',
                        '_require',
                        '_require',
                        '_scope',
                        '_typed',
                        'all',
                        'len',
                        'len',
                        'len',
                        'type',
                        'type',
                        'type',
                        'type',
                        'type'],
 '_table': ['CalculationEvidenceClass',
            '_definition',
            '_envelope',
            '_metadata',
            '_representation',
            '_require',
            '_require',
            '_require',
            '_scope',
            'all',
            'field.method_id.startswith',
            'tuple',
            'tuple',
            'type',
            'type',
            'type'],
 '_tail': ['_require',
           '_require',
           '_scalar',
           '_scope',
           '_table',
           '_typed',
           '_typed',
           'list',
           'list',
           'ranking.append',
           'set'],
 '_typed': ['_require', 'type'],
 'assemble_report': ['CanonicalReport.from_dict',
                     'FamilyFailure',
                     '_bundle_check',
                     '_capabilities',
                     '_closed_simulation',
                     '_closed_simulation',
                     '_closure',
                     '_comparison',
                     '_coverage',
                     '_diagnostics',
                     '_diagnostics',
                     '_diagnostics',
                     '_diagnostics',
                     '_disclosures',
                     '_distribution',
                     '_distribution',
                     '_distribution',
                     '_distribution_exclusions',
                     '_duplicates',
                     '_extinction',
                     '_inputs',
                     '_lineage_observations',
                     '_provenance',
                     '_representation',
                     '_require',
                     '_require',
                     '_require',
                     '_require',
                     '_require',
                     '_require',
                     '_require',
                     '_require',
                     '_require',
                     '_require',
                     '_tail',
                     '_typed',
                     'all',
                     'all',
                     'any',
                     'dict',
                     'empirical_representations.append',
                     'empirical_representations.append',
                     'empirical_representations.append',
                     'empirical_representations.append',
                     'enumerate',
                     'failures.setdefault',
                     'failures.setdefault(failure.capability.value, []).extend',
                     'len',
                     'len',
                     'len',
                     'len',
                     "operations['content_diagnostics'].append",
                     "operations['content_diagnostics'].append",
                     "operations['content_diagnostics'].append",
                     "operations['dataset_longitudinal'].append",
                     "operations['intervention_simulation'].append",
                     "operations['intervention_simulation'].append",
                     "operations['intervention_simulation'].append",
                     "operations['provenance'].append",
                     "operations['provenance'].append",
                     "payload['inputs']['limitations'].append",
                     'run.get',
                     'run.get',
                     'set',
                     'set',
                     'set',
                     'type',
                     'type',
                     'type',
                     'type',
                     'type',
                     'type',
                     'type',
                     'type']}

PHASE4_STEP3_ASSEMBLY_ARITHMETIC = {'FamilyFailure.__post_init__': ['not self.messages'],
 '_capabilities': ["bundle.observability.limitations + ('Input eligibility is distinct from executed "
                   "analysis; Phase 5 lineage remains deferred.',)",
                   'not completed',
                   'reasons + family_codes'],
 '_closed_simulation': ["target['limitations'] + ['Extinction events are not separately inferred by the "
                        "assembly adapter; inspect the supplied sampled support paths.']",
                        'value.simulation_horizon + 1'],
 '_closure': ["'derived_metrics.closure_exposure.direct.' + name"],
 '_comparison': ["'derived_metrics.support.' + name",
                 "'derived_metrics.support.' + name",
                 'context.earlier_scope.excluded_record_keys + context.later_scope.excluded_record_keys',
                 'context.earlier_scope.included_record_keys + context.later_scope.included_record_keys',
                 "context.earlier_scope.scope_id + ' -> '",
                 "context.earlier_scope.scope_id + ' -> ' + context.later_scope.scope_id",
                 'earlier + later',
                 'value.limitations + compatibility.limitations'],
 '_diagnostics': ["'Validation notice ' + message.code",
                  "'Validation notice ' + message.code + ': '",
                  "'Validation notice ' + message.code + ': ' + message.message"],
 '_disclosure_signal': ["list(basis['limitations']) + limitations", "owner + '.'", "owner + '.' + name"],
 '_disclosure_unavailable': ["owner + '.unavailable_conclusion'"],
 '_disclosures': ["'observed_facts.provenance.' + key",
                  "not any((key in derived for key in ('support', 'diversity', 'tail')))",
                  'not basis',
                  "set(content_cap.get('reason_codes', ())) | set(longitudinal_cap.get('reason_codes', ()))"],
 '_distribution': ["'derived_metrics.' + family",
                   "'derived_metrics.' + family + '.by_version.*.'",
                   "'derived_metrics.' + family + '.by_version.*.' + prefix",
                   "'derived_metrics.' + family + '.by_version.*.' + prefix + name",
                   "'derived_metrics.diversity.by_version.*.' + prefix",
                   "'derived_metrics.diversity.by_version.*.' + prefix + 'state_frequencies'",
                   'not weighted',
                   'not weighted',
                   'not weighted',
                   "prefix + 'state_frequencies'",
                   "prefix + 'support_size'",
                   'prefix + name',
                   'prefix + name'],
 '_duplicates': ["'exact_duplicate_group_' + str(index + 1)",
                 "'observed_facts.content.' + name",
                 "group['record_count'] - 1",
                 'index + 1',
                 'not seen.intersection(group.record_keys)'],
 '_inputs': ["'observed_facts.provenance.' + name",
             "'validated_version:' + version",
             'bundle.records + (() if bundle.provenance is None else bundle.provenance)',
             'messages + uncertain',
             'messages + uncertain',
             "tuple(messages_by_location.get((artifact.role, '[redacted]'), ())) + "
             'tuple(messages_by_location.get((artifact.role, None), ()))'],
 '_lineage_observations': ["'observed_facts.lineage.' + name", 'coverage.denominator - coverage.numerator'],
 '_metadata_text': ["'Definitions 10.1-10.6; explicit ' + rule",
                    "'Definitions 10.1-10.6; explicit ' + rule",
                    "'Definitions 10.1-10.6; explicit ' + rule",
                    "'Definitions 10.1-10.6; explicit ' + rule + '; selected counts / included records'",
                    "'Definitions 7.1; ' + item",
                    "basis + ('empirical_assignments; n_i/N',)",
                    "tuple(('Definitions 7.1; ' + item for item in basis)) + ('count included record-state "
                    "assignments',)"],
 '_number': ["name + ' is above its accepted bound'",
             "name + ' is below its accepted bound'",
             "name + ' must be a built-in number'",
             "name + ' must be finite'"],
 '_provenance': ["'derived_metrics.provenance.' + name",
                 "'derived_metrics.provenance.' + name",
                 "'observed_facts.provenance.' + field",
                 "'observed_facts.provenance.' + field",
                 "'observed_facts.provenance.' + field + '_counts'",
                 "'observed_facts.provenance.' + field + '_field_coverage'",
                 "'observed_facts.provenance.' + name",
                 "'observed_facts.provenance.' + name",
                 "'observed_facts.provenance.' + name",
                 "field + '_counts'",
                 "field + '_counts'",
                 "field + '_field_coverage'",
                 "field + '_field_coverage'"],
 '_provenance_consistency': ['len(keys) - len(missing)',
                             'not row.required_fields_valid',
                             'not value.scope.excluded_record_keys'],
 '_require': ['not condition'],
 '_scalar': ['-1', 'value.metadata.limitations + tuple(limitations)'],
 '_scope': ['value.included_record_keys + value.excluded_record_keys'],
 '_table': ['metadata.limitations + tuple(limitations)'],
 '_tail': ["'derived_metrics.tail.' + name", "'derived_metrics.tail.' + name"],
 '_typed': ["name + ' requires its exact accepted result type'"],
 'assemble_report': ["'supplied_declared_tail:' + tail.scope.scope_id",
                     "'supplied_direct_closure_interval:' + closure.scope.scope_id",
                     "'supplied_distribution:' + (supplied.unweighted.scope.scope_id if type(supplied) is "
                     'StateDistributionResult else supplied.scope.scope_id)',
                     "'supplied_exact_duplicates:' + duplicates.scope.scope_id",
                     "'supplied_provenance_composition:' + provenance.scope.scope_id",
                     'DirectClosureExposureBounds | None',
                     'ExactDuplicateResult | None',
                     'ExpectedDiversityResult | None',
                     'ProvenanceCompositionResult | None',
                     'ResamplingSimulation | None',
                     'StateDistributionResult | DistributionMetrics',
                     'SupportComparison | None',
                     'TailSelectionResult | None',
                     'supplied.unweighted.scope.included_record_keys + '
                     'supplied.unweighted.scope.excluded_record_keys']}

PHASE4_STEP3_ASSEMBLY_ATTRIBUTES = {'FamilyFailure.__post_init__': ['ValidationSeverity.ERROR',
                                 'ValidationSeverity.FATAL',
                                 'item.severity',
                                 'self.capability',
                                 'self.messages',
                                 'self.messages',
                                 'self.messages'],
 '_base': ['dict.fromkeys',
           'dict.fromkeys',
           'dict.fromkeys',
           'dict.fromkeys',
           'field.evidence_class',
           'field.method_id',
           'field.owner',
           'field.owner',
           'field.owner',
           'field.owner.startswith',
           'field.unit'],
 '_bundle_check': ['assessment.capabilities',
                   'assessment.capabilities',
                   'assessment.capabilities',
                   'assessment.capabilities.items',
                   'assessment.maximum_level',
                   'assessment.maximum_level',
                   'bundle.generation',
                   'bundle.generation',
                   'bundle.inventory',
                   'bundle.inventory',
                   'bundle.inventory',
                   'bundle.mapping_traces',
                   'bundle.mapping_traces',
                   'bundle.observability',
                   'bundle.observability',
                   'bundle.provenance',
                   'bundle.provenance',
                   'bundle.provenance',
                   'bundle.provenance',
                   'bundle.provenance',
                   'bundle.provenance',
                   'bundle.provenance_join',
                   'bundle.provenance_join',
                   'bundle.records',
                   'bundle.records',
                   'bundle.records',
                   'bundle.records',
                   'bundle.validation_messages',
                   'bundle.validation_messages',
                   'bundle.version_order',
                   'bundle.version_order',
                   'bundle.version_order',
                   'bundle.version_order.loaded_versions',
                   'bundle.version_order.order',
                   'capability.coverage',
                   'capability.coverage',
                   'capability.coverage_details',
                   'capability.coverage_details',
                   'capability.coverage_details',
                   'capability.coverage_details.values',
                   'capability.notes',
                   'capability.reason_codes',
                   'capability.requirements_met',
                   'capability.requirements_missing',
                   'capability.status',
                   'coverage.denominator',
                   'coverage.numerator',
                   'item.file_format',
                   'item.path',
                   'item.role',
                   'join.grounding_field_coverage',
                   'join.matches',
                   'join.matches',
                   'join.matches',
                   'join.matches',
                   'join.matches',
                   'join.matches',
                   'join.matches',
                   'join.matches',
                   'join.matches',
                   'join.missing_record_keys',
                   'join.missing_record_keys',
                   'join.provenance_required_field_coverage',
                   'join.provenance_row_coverage',
                   'join.provenance_supplied',
                   'join.scope_record_keys',
                   'join.scope_record_keys',
                   'join.scope_record_keys',
                   'join.scope_record_keys',
                   'join.scope_record_keys',
                   'join.scope_record_keys',
                   'join.scope_record_keys',
                   'join.selected_dataset_versions',
                   'match.provenance',
                   'match.provenance',
                   'match.provenance',
                   'match.provenance',
                   'match.provenance',
                   'match.provenance',
                   'match.provenance',
                   'match.provenance',
                   'match.provenance.grounding_known',
                   'match.provenance.required_fields_valid',
                   'match.record_key',
                   'match.record_key',
                   'match.record_key',
                   'match.record_key',
                   'row.grounding_known',
                   'row.location',
                   'row.location',
                   'row.record_key',
                   'row.record_key',
                   'row.record_key',
                   'row.record_key',
                   'row.required_fields_valid',
                   'row.values',
                   'row.values',
                   'row.values',
                   'row.values',
                   'row.values.get',
                   'row.values.get'],
 '_bundle_scope': ['bundle.records',
                   'bundle.records',
                   'bundle.version_order',
                   'bundle.version_order.loaded_versions',
                   'row.record_key'],
 '_capabilities': ['CapabilityKey.DATASET_LONGITUDINAL',
                   'CapabilityKey.DATASET_LONGITUDINAL',
                   'CapabilityKey.INGESTION',
                   'CapabilityKey.INTERVENTION_SIMULATION',
                   'CapabilityKey.LINEAGE',
                   'CapabilityKey.LINEAGE',
                   'CapabilityKey.LINEAGE',
                   'CapabilityKey.LINEAGE',
                   'CapabilityKey.MODEL_LONGITUDINAL',
                   'CapabilityKey.MODEL_LONGITUDINAL',
                   'CapabilityKey.PROVENANCE',
                   'bundle.observability',
                   'bundle.observability',
                   'bundle.observability',
                   'bundle.observability',
                   'bundle.observability',
                   'bundle.observability.basis',
                   'bundle.observability.capabilities',
                   'bundle.observability.limitations',
                   'bundle.observability.maximum_level',
                   'bundle.observability.maximum_level',
                   'bundle.provenance_join',
                   'bundle.provenance_join',
                   'bundle.provenance_join',
                   'bundle.provenance_join.grounding_field_coverage',
                   'bundle.provenance_join.provenance_required_field_coverage',
                   'bundle.provenance_join.provenance_row_coverage',
                   'bundle.records',
                   'dict.fromkeys',
                   'dict.fromkeys',
                   'dict.fromkeys',
                   "entry['notes'].append",
                   "entry['notes'].append",
                   'key.value',
                   'key.value',
                   'key.value',
                   'matrix.values',
                   'original.coverage',
                   'original.coverage',
                   'original.coverage',
                   'original.coverage',
                   'original.coverage_details',
                   'original.coverage_details',
                   'original.coverage_details',
                   'original.coverage_details.items',
                   'original.notes',
                   'original.reason_codes',
                   'original.requirements_met',
                   'original.requirements_missing',
                   'original.status',
                   'original.status',
                   'original.status.value',
                   'reasons.append'],
 '_closed_simulation': ['CalculationEvidenceClass.SIMULATION',
                        'CalculationEvidenceClass.SIMULATION',
                        'CalculationEvidenceClass.SIMULATION',
                        'dict.fromkeys',
                        'generation.gini_simpson_diversity',
                        'generation.state_counts',
                        'generation.state_counts',
                        'generation.state_counts',
                        'generation.state_counts',
                        'generation.state_counts',
                        'generation.state_frequencies',
                        'generation.state_frequencies',
                        'generation.step',
                        'generation.step',
                        'generation.support',
                        'generation.support',
                        'generation.support',
                        'generation.support_size',
                        'generation.support_size',
                        'generation.support_size',
                        'generations.append',
                        'inputs.effective_distribution',
                        'inputs.effective_distribution',
                        'inputs.input_basis',
                        'inputs.numerical_policy',
                        'inputs.representation',
                        'inputs.representation',
                        'inputs.representation',
                        'inputs.scope',
                        'inputs.scope',
                        'inputs.scope',
                        'paths.append',
                        'replicate.generations',
                        'replicate.generations',
                        'replicate.replicate_index',
                        'replicate.replicate_index',
                        'target.update',
                        'target.update',
                        'trajectories.append',
                        'value.assumptions',
                        'value.assumptions',
                        'value.contraction_factor',
                        'value.evidence_class',
                        'value.expected_diversity',
                        'value.expected_diversity_metadata',
                        'value.experimental',
                        'value.initial_gini_simpson_diversity',
                        'value.inputs',
                        'value.limitations',
                        'value.method',
                        'value.method',
                        'value.method_version',
                        'value.method_version',
                        'value.model_name',
                        'value.model_name',
                        'value.numerical_underflow_steps',
                        'value.numpy_version',
                        'value.random_seed',
                        'value.replicate_schedule',
                        'value.resample_size',
                        'value.resample_size',
                        'value.resample_size',
                        'value.rng_name',
                        'value.sampled_paths',
                        'value.sampler_algorithm',
                        'value.simulation_horizon',
                        'value.simulation_horizon',
                        'value.simulation_replicates',
                        'value.simulation_replicates',
                        'value.state_order',
                        'value.state_order',
                        'value.state_order',
                        'value.state_order',
                        'value.state_schedule',
                        'value.trajectory_metadata',
                        'value.trajectory_metadata'],
 '_closure': ["payload['derived_metrics'].setdefault",
              'provenance.confidence',
              'provenance.confidence',
              'provenance.confidence',
              'provenance.confidence.counts',
              'provenance.confidence.field_coverage',
              'provenance.confidence.status',
              'provenance.direct_grounding',
              'provenance.direct_grounding',
              'provenance.direct_grounding',
              'provenance.direct_grounding.known_closed_count',
              'provenance.direct_grounding.known_closed_count.value',
              'provenance.direct_grounding.known_open_count',
              'provenance.direct_grounding.known_open_count.value',
              'provenance.direct_grounding.unresolved_grounding_count',
              'provenance.direct_grounding.unresolved_grounding_count.value',
              'provenance.grounding_field_coverage',
              'provenance.input_has_errors',
              'provenance.provenance_required_field_coverage',
              'provenance.provenance_row_coverage',
              'provenance.scope',
              'provenance.validation_messages',
              'value.classification_basis',
              'value.classification_basis',
              'value.confidence_counts',
              'value.confidence_disclosure',
              'value.confidence_disclosure',
              'value.confidence_field_coverage',
              'value.confidence_status',
              'value.denominator',
              'value.denominator',
              'value.denominator',
              'value.denominator_basis',
              'value.grounding_field_coverage',
              'value.grounding_field_coverage',
              'value.grounding_field_coverage',
              'value.input_has_errors',
              'value.interval_width',
              'value.known_closed_count',
              'value.known_closed_count',
              'value.known_closed_count',
              'value.known_open_count',
              'value.known_open_count',
              'value.known_open_count',
              'value.limitations',
              'value.lower_bound',
              'value.operationalization_label',
              'value.provenance_required_field_coverage',
              'value.provenance_row_coverage',
              'value.scope',
              'value.scope',
              'value.scope',
              'value.scope',
              'value.scope',
              'value.scope.denominator_basis',
              'value.scope.included_record_keys',
              'value.unresolved_grounding_count',
              'value.unresolved_grounding_count',
              'value.unresolved_grounding_count',
              'value.upper_bound',
              'value.validation_messages'],
 '_comparison': ['bundle.version_order',
                 'compatibility.collision_groups',
                 'compatibility.collision_groups',
                 'compatibility.context',
                 'compatibility.earlier_state_semantics',
                 'compatibility.earlier_state_semantics',
                 'compatibility.earlier_state_semantics',
                 'compatibility.earlier_state_semantics',
                 'compatibility.earlier_state_semantics',
                 'compatibility.harmonized_representation',
                 'compatibility.harmonized_representation',
                 'compatibility.harmonized_representation',
                 'compatibility.harmonized_representation',
                 'compatibility.harmonized_representation',
                 'compatibility.harmonized_state_semantics',
                 'compatibility.harmonized_state_semantics',
                 'compatibility.harmonized_state_semantics',
                 'compatibility.harmonized_state_semantics',
                 'compatibility.later_state_semantics',
                 'compatibility.later_state_semantics',
                 'compatibility.later_state_semantics',
                 'compatibility.later_state_semantics',
                 'compatibility.later_state_semantics',
                 'compatibility.limitations',
                 'compatibility.mapping',
                 'compatibility.mapping',
                 'compatibility.mapping',
                 'compatibility.method',
                 'compatibility.method',
                 'compatibility.method',
                 'context.earlier_representation',
                 'context.earlier_representation',
                 'context.earlier_representation',
                 'context.earlier_representation',
                 'context.earlier_representation',
                 'context.earlier_scope',
                 'context.earlier_scope',
                 'context.earlier_scope',
                 'context.earlier_scope',
                 'context.earlier_scope',
                 'context.earlier_scope',
                 'context.earlier_scope.dataset_versions',
                 'context.earlier_scope.excluded_record_keys',
                 'context.earlier_scope.included_record_keys',
                 'context.earlier_scope.scope_id',
                 'context.later_representation',
                 'context.later_representation',
                 'context.later_representation',
                 'context.later_representation',
                 'context.later_representation',
                 'context.later_scope',
                 'context.later_scope',
                 'context.later_scope',
                 'context.later_scope',
                 'context.later_scope',
                 'context.later_scope',
                 'context.later_scope.dataset_versions',
                 'context.later_scope.excluded_record_keys',
                 'context.later_scope.included_record_keys',
                 'context.later_scope.scope_id',
                 'context.version_order',
                 'context.version_order',
                 'context.version_order',
                 'context.version_order.order',
                 'context.version_order.order_source',
                 'effects.append',
                 'harmonized.denominator_basis',
                 'harmonized.frequency_denominator',
                 'harmonized.input_basis',
                 'harmonized.weighting',
                 'item.weighting',
                 'item.weighting',
                 'item.weighting.weighting_mode',
                 'item.weighting.weighting_mode',
                 'mapping.direction',
                 'mapping.direction',
                 'mapping.direction',
                 'mapping.direction',
                 'mapping.direction',
                 'mapping.source_representation',
                 'mapping.source_state_semantics',
                 'mapping.state_mapping',
                 'mapping.state_mapping',
                 'mapping.state_mapping.items',
                 'mapping.target_representation',
                 'mapping.target_state_semantics',
                 'order.index',
                 'order.index',
                 'original.denominator_basis',
                 'original.frequency_denominator',
                 'original.input_basis',
                 'original.weighting',
                 "payload['derived_metrics'].setdefault",
                 "payload['derived_metrics'].setdefault",
                 'scalar.reason_codes',
                 'scalar.status',
                 'scalar_scope.dataset_versions',
                 'scalar_scope.denominator_basis',
                 'scalar_scope.excluded_record_keys',
                 'scalar_scope.included_record_keys',
                 'scalar_scope.scope_id',
                 'support.values',
                 'value.added_states',
                 'value.compatibility',
                 'value.extinct_states',
                 'value.gini_simpson_diversity_delta',
                 'value.gini_simpson_diversity_delta',
                 'value.gini_simpson_diversity_delta',
                 'value.gini_simpson_diversity_delta.reason_codes',
                 'value.gini_simpson_diversity_delta.status',
                 'value.harmonized_earlier',
                 'value.harmonized_earlier',
                 'value.harmonized_earlier',
                 'value.harmonized_earlier',
                 'value.harmonized_earlier',
                 'value.harmonized_earlier',
                 'value.harmonized_earlier',
                 'value.harmonized_earlier',
                 'value.harmonized_earlier',
                 'value.harmonized_earlier.representation',
                 'value.harmonized_earlier.scope',
                 'value.harmonized_earlier.support',
                 'value.harmonized_earlier.support_size',
                 'value.harmonized_earlier.support_size.value',
                 'value.harmonized_earlier.weighting',
                 'value.harmonized_later',
                 'value.harmonized_later',
                 'value.harmonized_later',
                 'value.harmonized_later',
                 'value.harmonized_later',
                 'value.harmonized_later',
                 'value.harmonized_later',
                 'value.harmonized_later',
                 'value.harmonized_later',
                 'value.harmonized_later.representation',
                 'value.harmonized_later.scope',
                 'value.harmonized_later.support',
                 'value.harmonized_later.support_size',
                 'value.harmonized_later.support_size.value',
                 'value.harmonized_later.weighting',
                 'value.limitations',
                 'value.limitations',
                 'value.limitations',
                 'value.limitations',
                 'value.mapping_effect',
                 'value.mapping_effect',
                 'value.original_earlier',
                 'value.original_earlier',
                 'value.original_earlier',
                 'value.original_earlier',
                 'value.original_earlier',
                 'value.original_earlier',
                 'value.original_earlier',
                 'value.original_earlier',
                 'value.original_earlier',
                 'value.original_earlier',
                 'value.original_earlier',
                 'value.original_earlier',
                 'value.original_earlier',
                 'value.original_earlier',
                 'value.original_earlier',
                 'value.original_earlier.denominator_basis',
                 'value.original_earlier.input_basis',
                 'value.original_earlier.input_basis',
                 'value.original_earlier.input_basis',
                 'value.original_earlier.input_basis',
                 'value.original_earlier.input_basis',
                 'value.original_earlier.representation',
                 'value.original_earlier.scope',
                 'value.original_earlier.support',
                 'value.original_earlier.support_size',
                 'value.original_earlier.support_size.value',
                 'value.original_earlier.weighting',
                 'value.original_later',
                 'value.original_later',
                 'value.original_later',
                 'value.original_later',
                 'value.original_later',
                 'value.original_later',
                 'value.original_later',
                 'value.original_later',
                 'value.original_later',
                 'value.original_later',
                 'value.original_later',
                 'value.original_later',
                 'value.original_later.denominator_basis',
                 'value.original_later.input_basis',
                 'value.original_later.input_basis',
                 'value.original_later.representation',
                 'value.original_later.scope',
                 'value.original_later.support',
                 'value.original_later.support_size',
                 'value.original_later.support_size.value',
                 'value.original_later.weighting',
                 'value.reason_codes',
                 'value.reason_codes',
                 'value.reason_codes',
                 'value.retained_states',
                 'value.retention_denominator',
                 'value.retention_denominator',
                 'value.retention_denominator',
                 'value.retention_denominator',
                 'value.retention_denominator',
                 'value.retention_denominator_basis',
                 'value.set_metadata',
                 'value.set_metadata',
                 'value.status',
                 'value.status',
                 'value.status',
                 'value.support_added_count',
                 'value.support_delta',
                 'value.support_delta',
                 'value.support_delta',
                 'value.support_delta.metadata',
                 'value.support_delta.metadata',
                 'value.support_delta.metadata.assumptions',
                 'value.support_delta.metadata.scope',
                 'value.support_loss_count',
                 'value.support_retention_ratio'],
 '_coverage': ['value.denominator',
               'value.denominator',
               'value.denominator',
               'value.denominator',
               'value.denominator_name',
               'value.numerator',
               'value.numerator',
               'value.numerator',
               'value.ratio'],
 '_definition': ['definition.path'],
 '_diagnostics': ['ValidationSeverity.INFO',
                  'ValidationSeverity.WARNING',
                  'message.code',
                  'message.code',
                  'message.code',
                  'message.code',
                  'message.field',
                  'message.field',
                  'message.field',
                  'message.field',
                  'message.file_role',
                  'message.file_role',
                  'message.file_role',
                  'message.file_role',
                  'message.file_role',
                  'message.file_role',
                  'message.file_role.value',
                  'message.file_role.value',
                  'message.line_number',
                  'message.message',
                  'message.message',
                  'message.message',
                  'message.message',
                  'message.record_key',
                  'message.record_key',
                  'message.record_key',
                  'message.record_key',
                  'message.row_number',
                  'message.row_number',
                  'message.severity',
                  'message.severity',
                  'message.severity',
                  'message.severity',
                  'message.severity.value',
                  "payload['errors'].append",
                  "payload['inputs']['limitations'].append",
                  "payload['warnings'].append"],
 '_disclosure_recommend': ["payload['recommended_next_metadata'].append"],
 '_disclosure_scope': ["payload['inputs'].get"],
 '_disclosure_signal': ['dict.fromkeys', 'result.update'],
 '_disclosure_unavailable': ["payload['unavailable_conclusions'].append", 'result.update'],
 '_disclosures': ['basis.append',
                  'basis.append',
                  'content_cap.get',
                  'derived.get',
                  'derived.get',
                  'derived.get',
                  "derived.get('closure_exposure', {}).get",
                  'direct.get',
                  'longitudinal_cap.get',
                  'paths.append',
                  'paths.append',
                  "payload['capabilities'].get",
                  "payload['capabilities'].get",
                  "payload['capabilities'].get",
                  "payload['observed_facts'].get",
                  'provenance.get',
                  'provenance.get',
                  'provenance.get',
                  'provenance.get',
                  'reasons.extend',
                  'support.get',
                  'tail.get'],
 '_distribution': ['CalculationStatus.AVAILABLE',
                   'CalculationStatus.AVAILABLE',
                   'CalculationStatus.AVAILABLE',
                   'CalculationStatus.AVAILABLE',
                   "payload['derived_metrics'].setdefault",
                   "payload['derived_metrics'].setdefault",
                   "payload['derived_metrics'].setdefault('diversity', {}).setdefault",
                   "payload['derived_metrics'].setdefault('diversity', {}).setdefault('by_version', "
                   '{}).setdefault',
                   "payload['derived_metrics'].setdefault('support', {}).setdefault",
                   "payload['derived_metrics'].setdefault('support', {}).setdefault('by_version', "
                   '{}).setdefault',
                   "payload['observed_facts'].setdefault",
                   "payload['observed_facts'].setdefault",
                   "payload['observed_facts'].setdefault('state_counts', {}).setdefault",
                   "payload['observed_facts'].setdefault('supplied_state_probabilities', {}).setdefault",
                   'row.state_count',
                   'row.state_count',
                   'row.state_count',
                   'row.state_count',
                   'row.state_count',
                   'row.state_frequency',
                   'row.state_frequency',
                   'row.state_frequency',
                   'row.state_frequency',
                   'row.state_id',
                   'row.state_id',
                   'row.state_id',
                   'row.state_id',
                   'row.state_id',
                   'row.state_id',
                   'row.state_id',
                   'row.state_mass',
                   'row.state_mass',
                   'row.state_mass',
                   'row.state_mass',
                   'row.state_mass',
                   'scalar.reason_codes',
                   'scalar.status',
                   'value.analyzed_record_count',
                   'value.analyzed_record_count',
                   'value.count_metadata',
                   'value.count_metadata',
                   'value.count_metadata',
                   'value.count_metadata',
                   'value.denominator_basis',
                   'value.denominator_basis',
                   'value.denominator_basis',
                   'value.denominator_basis',
                   'value.frequency_denominator',
                   'value.frequency_denominator',
                   'value.frequency_denominator',
                   'value.frequency_denominator',
                   'value.frequency_denominator',
                   'value.frequency_denominator',
                   'value.frequency_denominator',
                   'value.frequency_denominator',
                   'value.frequency_denominator',
                   'value.frequency_denominator',
                   'value.frequency_denominator',
                   'value.frequency_denominator',
                   'value.frequency_metadata',
                   'value.frequency_metadata',
                   'value.gini_simpson_diversity',
                   'value.gini_simpson_diversity',
                   'value.input_basis',
                   'value.input_basis',
                   'value.input_basis',
                   'value.input_basis',
                   'value.input_basis',
                   'value.input_basis',
                   'value.input_basis',
                   'value.input_basis',
                   'value.input_basis',
                   'value.limitations',
                   'value.limitations',
                   'value.limitations',
                   'value.limitations',
                   'value.mass_metadata',
                   'value.mass_metadata',
                   'value.mass_metadata',
                   'value.mass_metadata',
                   'value.numerical_policy',
                   'value.probability_residual',
                   'value.reason_codes',
                   'value.reason_codes',
                   'value.reason_codes',
                   'value.reason_codes',
                   'value.reason_codes',
                   'value.representation',
                   'value.representation',
                   'value.representation',
                   'value.representation',
                   'value.representation',
                   'value.representation',
                   'value.scope',
                   'value.scope',
                   'value.scope',
                   'value.scope',
                   'value.scope',
                   'value.scope',
                   'value.scope',
                   'value.scope',
                   'value.scope',
                   'value.scope',
                   'value.scope',
                   'value.scope.dataset_versions',
                   'value.scope.dataset_versions',
                   'value.scope.denominator_basis',
                   'value.scope.included_record_keys',
                   'value.scope.included_record_keys',
                   'value.simpson_concentration',
                   'value.simpson_concentration',
                   'value.states',
                   'value.states',
                   'value.states',
                   'value.states',
                   'value.states',
                   'value.states',
                   'value.states',
                   'value.states',
                   'value.states',
                   'value.states',
                   'value.states',
                   'value.states',
                   'value.states',
                   'value.states',
                   'value.states',
                   'value.status',
                   'value.status',
                   'value.status',
                   'value.status',
                   'value.status',
                   'value.status',
                   'value.status',
                   'value.status',
                   'value.status',
                   'value.status',
                   'value.supplied_probability_total',
                   'value.support',
                   'value.support',
                   'value.support',
                   'value.support_size',
                   'value.support_size',
                   'value.support_size',
                   'value.support_size.value',
                   'value.weighting',
                   'value.weighting',
                   'value.weighting',
                   'value.weighting',
                   'value.weighting',
                   'value.weighting',
                   'value.weighting.weighting_mode'],
 '_distribution_exclusions': ['exclusions.append',
                              'item.exclusion_reason',
                              'item.exclusion_reason',
                              'item.exclusion_reason.value',
                              'item.record_key',
                              'item.record_key',
                              'item.state_id',
                              "payload['observed_facts'].get",
                              "payload['observed_facts'].get(family, {}).get",
                              "payload['observed_facts'].get(family, {}).get('by_version', {}).get",
                              'payload[section].get',
                              'payload[section].get(family, {}).get',
                              "payload[section].get(family, {}).get('by_version', {}).get",
                              "payload[section].get(family, {}).get('by_version', {}).get(version, "
                              '{}).values',
                              'scope.dataset_versions',
                              'scope.excluded_record_keys',
                              'scope.excluded_record_keys',
                              'value.excluded_assignments',
                              'value.excluded_assignments',
                              'value.excluded_assignments',
                              'value.excluded_assignments',
                              'value.excluded_assignments',
                              'value.unweighted',
                              'value.unweighted.scope'],
 '_duplicates': ['CalculationEvidenceClass.OBSERVED_FACT',
                 'CalculationStatus.AVAILABLE',
                 'CalculationStatus.UNAVAILABLE',
                 'group.record_keys',
                 'group.record_keys',
                 'group.record_keys',
                 'group.record_keys',
                 'group.record_keys',
                 'group.record_keys',
                 'group.record_keys',
                 'group.record_keys',
                 'groups.append',
                 'item.value',
                 "payload['observed_facts'].setdefault",
                 'seen.intersection',
                 'seen.update',
                 'status.value',
                 'value.coverage',
                 'value.duplicate_group_count',
                 'value.duplicate_group_count',
                 'value.duplicate_group_count',
                 'value.duplicate_group_count',
                 'value.duplicate_group_count',
                 'value.duplicate_group_count.reason_codes',
                 'value.duplicate_group_count.status',
                 'value.duplicate_group_count.value',
                 'value.duplicate_group_count.value',
                 'value.duplicate_record_count',
                 'value.duplicate_record_count',
                 'value.duplicate_record_count',
                 'value.duplicate_record_count.value',
                 'value.duplicate_record_count.value',
                 'value.evidence_class',
                 'value.exact_duplicate_groups',
                 'value.limitations',
                 'value.limitations',
                 'value.representation',
                 'value.representation',
                 'value.scope',
                 'value.scope',
                 'value.scope',
                 'value.scope.included_record_keys'],
 '_extinction': ['CalculationEvidenceClass.SIMULATION',
                 'CalculationEvidenceClass.SIMULATION',
                 'CalculationStatus.AVAILABLE',
                 'first.input_basis',
                 'first.limitations',
                 'first.numerical_policy',
                 'first.numerical_policy',
                 'first.one_step_extinction_probability',
                 'first.one_step_extinction_probability.metadata',
                 'first.one_step_extinction_probability.metadata.assumptions',
                 'first.representation',
                 'first.representation',
                 'first.resample_size',
                 'first.resample_size',
                 'first.resample_size',
                 'first.resample_size',
                 'first.scope',
                 'first.scope',
                 'scalar.metadata',
                 'scalar.metadata',
                 'scalar.reason_codes',
                 'scalar.status',
                 'scalar.status',
                 'scalar.value',
                 'scalar.value',
                 'target.update',
                 "target['initial_distribution'].append",
                 "target['parameters']['state_order'].append",
                 'value.evaluation_method',
                 'value.evidence_class',
                 'value.experimental',
                 'value.input_basis',
                 'value.method',
                 'value.model_name',
                 'value.numerical_policy',
                 'value.numerical_underflow',
                 'value.one_step_extinction_probability',
                 'value.random_seed',
                 'value.representation',
                 'value.representation',
                 'value.resample_size',
                 'value.scope',
                 'value.scope',
                 'value.simulation_horizon',
                 'value.state_frequency',
                 'value.state_frequency',
                 'value.state_id',
                 'value.state_id',
                 'value.state_id',
                 'value.state_id'],
 '_inputs': ['FileRole.EMBEDDING_DATA',
             'FileRole.EXTERNAL_REFERENCE',
             'ValidationSeverity.ERROR',
             'ValidationSeverity.FATAL',
             'affected.append',
             'artifact.fields',
             'artifact.file_format',
             'artifact.file_format.value',
             'artifact.path',
             'artifact.path',
             'artifact.path',
             'artifact.role',
             'artifact.role',
             'artifact.role',
             'artifact.role',
             'artifact.role',
             'artifact.role',
             'artifact.role.value',
             'artifact.row_count',
             'artifact.sha256',
             'artifact.sha256',
             'artifact.size_bytes',
             'bundle.generation',
             'bundle.generation',
             'bundle.generation.messages',
             'bundle.inventory',
             'bundle.mapping_traces',
             'bundle.mapping_traces',
             'bundle.observability',
             'bundle.observability.validation_messages',
             'bundle.provenance',
             'bundle.provenance',
             'bundle.provenance_join',
             'bundle.records',
             'bundle.records',
             'bundle.validation_messages',
             'bundle.validation_messages',
             'bundle.version_order',
             'bundle.version_order',
             'bundle.version_order',
             'bundle.version_order.loaded_versions',
             'bundle.version_order.order',
             'bundle.version_order.order_source',
             'coverage.denominator',
             'coverage.denominator',
             'dict.fromkeys',
             'hashes.add',
             'join.grounding_field_coverage',
             'join.messages',
             'join.provenance_required_field_coverage',
             'join.provenance_row_coverage',
             'join.provenance_row_coverage',
             'join.provenance_row_coverage.denominator_name',
             'join.scope_record_keys',
             'join.scope_record_keys',
             'join.scope_record_keys',
             'join.selected_dataset_versions',
             'message.code',
             'message.file_path',
             'message.file_role',
             'message.severity',
             'messages_by_location.get',
             'messages_by_location.get',
             'messages_by_location.get',
             'messages_by_location.setdefault',
             'messages_by_location.setdefault((message.file_role, message.file_path), []).append',
             'operations.append',
             "payload['inputs']['artifacts'].append",
             "payload['inputs']['file_hashes'].append",
             'records_by_version.get',
             'records_by_version.setdefault',
             'records_by_version.setdefault(row.record_key.dataset_version, []).append',
             'row.location',
             'row.location',
             'row.location.file_path',
             'row.location.file_role',
             'row.record_key',
             'row.record_key',
             'row.record_key',
             'row.record_key.dataset_version',
             'row.record_key.dataset_version',
             'trace.fields',
             'trace.mapping_sha256',
             'trace.unmapped_fields',
             'unmapped.update',
             'versions_by_location.get',
             'versions_by_location.setdefault',
             'versions_by_location.setdefault((row.location.file_role, row.location.file_path), set()).add'],
 '_key': ['value.dataset_version', 'value.record_id'],
 '_lineage_observations': ['CapabilityKey.LINEAGE',
                           'bundle.observability',
                           'bundle.observability.capabilities',
                           'bundle.version_order',
                           'bundle.version_order.order',
                           'capability.coverage',
                           'capability.requirements_met',
                           'coverage.denominator',
                           'coverage.denominator',
                           'coverage.denominator',
                           'coverage.denominator',
                           'coverage.numerator',
                           'coverage.numerator'],
 '_message_family': ['message.code',
                     'message.field',
                     'message.field',
                     'message.field',
                     'message.field',
                     'message.file_role',
                     'message.file_role',
                     'message.file_role.value'],
 '_metadata': ['value.assumptions',
               'value.assumptions',
               'value.evidence_class',
               'value.evidence_class',
               'value.formula_id',
               'value.formula_id',
               'value.limitations',
               'value.limitations',
               'value.method',
               'value.metric_name',
               'value.metric_name',
               'value.owner_id',
               'value.owner_id',
               'value.representation',
               'value.representation',
               'value.scope',
               'value.scope',
               'value.unit',
               'value.unit',
               'value.weighting',
               'value.weighting',
               'value.weighting',
               'value.weighting',
               'value.weighting',
               'value.weighting.weight_field',
               'value.weighting.weighting_mode'],
 '_metadata_text': ['CalculationEvidenceClass.SIMULATION',
                    'CalculationEvidenceClass.SIMULATION',
                    'CalculationEvidenceClass.SIMULATION',
                    'methods.get',
                    'name.startswith',
                    'value.assumptions',
                    'value.assumptions',
                    'value.assumptions',
                    'value.assumptions',
                    'value.evidence_class',
                    'value.evidence_class',
                    'value.evidence_class',
                    'value.limitations',
                    'value.limitations',
                    'value.limitations',
                    'value.limitations',
                    'value.method',
                    'value.metric_name',
                    'value.owner_id',
                    'value.owner_id',
                    'value.owner_id',
                    'value.owner_id',
                    'value.owner_id',
                    'value.owner_id'],
 '_policy': ['value.absolute_tolerance',
             'value.absolute_tolerance',
             'value.probability_mass_tolerance',
             'value.probability_mass_tolerance',
             'value.relative_tolerance',
             'value.relative_tolerance'],
 '_provenance': ['CalculationReason.EMPTY_SCOPE',
                 'CalculationReason.EMPTY_SCOPE',
                 'CalculationStatus.AVAILABLE',
                 'CalculationStatus.AVAILABLE',
                 'CalculationStatus.UNAVAILABLE',
                 'CalculationStatus.UNAVAILABLE',
                 'bundle.provenance_join',
                 'coverage.denominator',
                 'coverage.ratio',
                 'coverage.ratio',
                 'coverage.ratio',
                 'coverage.ratio',
                 'grounding.assignments',
                 'grounding.assignments',
                 'grounding.assignments',
                 'grounding.known_closed_count',
                 'grounding.known_open_count',
                 'grounding.limitations',
                 'grounding.scope',
                 'grounding.unresolved_grounding_count',
                 'item.counts',
                 'item.counts',
                 'item.counts',
                 'item.counts',
                 'item.counts_metadata',
                 'item.field_coverage',
                 'item.field_coverage',
                 'item.field_coverage',
                 'item.field_coverage',
                 'item.field_coverage',
                 'item.field_coverage',
                 'item.field_coverage',
                 'item.field_coverage',
                 'item.field_coverage.denominator',
                 'item.field_coverage.ratio',
                 'item.field_coverage.ratio',
                 'item.field_coverage.ratio',
                 'item.field_coverage.ratio',
                 'item.field_coverage.ratio',
                 'item.field_coverage.ratio',
                 'item.field_coverage_metadata',
                 'item.field_name',
                 'item.reason_codes',
                 'item.reason_codes',
                 'item.record_key',
                 'item.shares',
                 'item.shares',
                 'item.shares_metadata',
                 'item.status',
                 'item.status',
                 'join.grounding_field_coverage',
                 'join.provenance_required_field_coverage',
                 'join.provenance_row_coverage',
                 'match.provenance',
                 "payload['derived_metrics'].setdefault",
                 "payload['observed_facts'].setdefault",
                 'value.analyzed_record_count',
                 'value.analyzed_record_count',
                 'value.analyzed_record_count.value',
                 'value.confidence',
                 'value.coverage_metadata',
                 'value.coverage_metadata',
                 'value.direct_grounding',
                 'value.grounding_field_coverage',
                 'value.grounding_field_coverage',
                 'value.grounding_field_coverage.ratio',
                 'value.limitations',
                 'value.limitations',
                 'value.limitations',
                 'value.limitations',
                 'value.limitations',
                 'value.limitations',
                 'value.missing_provenance_count',
                 'value.missing_provenance_count',
                 'value.missing_provenance_count.value',
                 'value.missing_provenance_share',
                 'value.provenance_required_field_coverage',
                 'value.provenance_row_coverage',
                 'value.records_with_matching_rows',
                 'value.scope',
                 'value.scope',
                 'value.scope',
                 'value.scope',
                 'value.scope',
                 'value.scope',
                 'value.scope',
                 'value.scope',
                 'value.scope',
                 'value.scope',
                 'value.scope',
                 'value.scope',
                 'value.scope',
                 'value.scope.included_record_keys',
                 'value.scope.included_record_keys',
                 'value.source',
                 'value.weighted_source',
                 'value.weighted_source',
                 'weighted.mass_metadata',
                 'weighted.missing_provenance_weight',
                 'weighted.reason_codes',
                 'weighted.shares_metadata',
                 'weighted.status',
                 'weighted.total_weight',
                 'weighted.total_weight',
                 'weighted.total_weight.value',
                 'weighted.weighted_missing_provenance_share',
                 'weighted.weighted_source_type_masses',
                 'weighted.weighted_source_type_shares'],
 '_provenance_consistency': ['CalculationStatus.AVAILABLE',
                             'CalculationStatus.UNAVAILABLE',
                             'ValidationSeverity.ERROR',
                             'ValidationSeverity.FATAL',
                             'assignment.basis',
                             'assignment.classification',
                             'assignment.missing_required_fields',
                             'bundle.provenance_join',
                             'bundle.provenance_join',
                             'bundle.provenance_join',
                             'bundle.provenance_join.matches',
                             'bundle.provenance_join.messages',
                             'bundle.provenance_join.provenance_supplied',
                             'bundle.records',
                             'composition.counts',
                             'composition.counts',
                             'composition.counts',
                             'composition.field_coverage',
                             'composition.field_coverage',
                             'composition.field_coverage',
                             'composition.field_coverage.denominator',
                             'composition.field_coverage.denominator_name',
                             'composition.field_coverage.numerator',
                             'composition.shares',
                             'composition.status',
                             'composition.status',
                             'composition.unavailable_record_keys',
                             'coverage.denominator',
                             'coverage.denominator_name',
                             'coverage.numerator',
                             'expected.values',
                             'grounding.assignments',
                             'grounding.assignments',
                             'grounding.assignments',
                             'grounding.assignments',
                             'grounding.assignments',
                             'grounding.input_has_errors',
                             'grounding.known_closed_count',
                             'grounding.known_open_count',
                             'grounding.unresolved_grounding_count',
                             'grounding.validation_messages',
                             'item.classification',
                             'item.record_key',
                             'match.provenance',
                             'match.provenance',
                             'match.provenance',
                             'match.provenance',
                             'match.provenance',
                             'match.provenance',
                             'match.provenance',
                             'match.provenance',
                             'match.provenance',
                             'match.provenance',
                             'match.provenance',
                             'match.provenance.grounding_known',
                             'match.provenance.required_fields_valid',
                             'match.provenance.values',
                             'match.provenance.values',
                             'match.provenance.values.get',
                             'match.provenance.values.get',
                             'match.record_key',
                             'match.record_key',
                             'match.record_key',
                             'match.record_key',
                             'message.record_key',
                             'message.record_key',
                             'message.severity',
                             'row.missing_required_fields',
                             'row.record_key',
                             'row.record_key',
                             'row.record_key.dataset_version',
                             'row.required_fields_valid',
                             'row.values',
                             'row.values',
                             'scalar.value',
                             'value.analyzed_record_count',
                             'value.analyzed_record_count.value',
                             'value.confidence',
                             'value.direct_grounding',
                             'value.grounding_field_coverage',
                             'value.input_has_errors',
                             'value.input_has_errors',
                             'value.missing_provenance_count',
                             'value.missing_provenance_count.value',
                             'value.provenance_required_field_coverage',
                             'value.provenance_row_coverage',
                             'value.provenance_supplied',
                             'value.records_with_matching_rows',
                             'value.records_with_matching_rows.value',
                             'value.scope',
                             'value.scope',
                             'value.scope',
                             'value.scope',
                             'value.scope',
                             'value.scope',
                             'value.scope.dataset_versions',
                             'value.scope.dataset_versions',
                             'value.scope.denominator_basis',
                             'value.scope.denominator_basis',
                             'value.scope.excluded_record_keys',
                             'value.scope.included_record_keys',
                             'value.source',
                             'value.validation_messages',
                             'value.validation_messages'],
 '_representation': ['value.binning_or_mapping_rule',
                     'value.binning_or_mapping_rule',
                     'value.field_name',
                     'value.field_name',
                     'value.missing_state_id',
                     'value.missing_state_id',
                     'value.missing_value_policy',
                     'value.missing_value_policy',
                     'value.normalization_profile',
                     'value.normalization_profile',
                     'value.representation_name',
                     'value.representation_name',
                     'value.representation_source',
                     'value.representation_source',
                     'value.representation_version',
                     'value.representation_version'],
 '_scalar': ['CalculationStatus.UNAVAILABLE',
             'field.evidence_class',
             'field.method_id',
             'field.method_id',
             'field.method_id.startswith',
             'field.owner',
             'field.unit',
             'path.rsplit',
             'reason.value',
             'value.metadata',
             'value.metadata',
             'value.metadata',
             'value.metadata',
             'value.metadata',
             'value.metadata',
             'value.metadata',
             'value.metadata.assumptions',
             'value.metadata.limitations',
             'value.metadata.method',
             'value.metadata.weighting',
             'value.metadata.weighting',
             'value.metadata.weighting.weight_field',
             'value.metadata.weighting.weighting_mode',
             'value.reason_codes',
             'value.reason_codes',
             'value.status',
             'value.status',
             'value.status',
             'value.status.value',
             'value.value',
             'value.value'],
 '_scope': ['bundle.records',
            'bundle.version_order',
            'bundle.version_order.loaded_versions',
            'row.record_key',
            'value.dataset_versions',
            'value.dataset_versions',
            'value.dataset_versions',
            'value.denominator_basis',
            'value.denominator_basis',
            'value.excluded_record_keys',
            'value.excluded_record_keys',
            'value.excluded_record_keys',
            'value.excluded_record_keys',
            'value.included_record_keys',
            'value.included_record_keys',
            'value.included_record_keys',
            'value.included_record_keys',
            'value.scope_id',
            'value.scope_id'],
 '_simulation_inputs': ['value.correction_applied',
                        'value.correction_method',
                        'value.effective_distribution',
                        'value.effective_distribution',
                        'value.effective_probability_total',
                        'value.normalization_divisor',
                        'value.numerical_policy',
                        'value.probability_corrections',
                        'value.probability_residual',
                        'value.representation',
                        'value.scope',
                        'value.supplied_distribution',
                        'value.supplied_distribution',
                        'value.supplied_probability_total'],
 '_table': ['CalculationStatus.UNAVAILABLE',
            'CalculationStatus.UNAVAILABLE',
            'field.evidence_class',
            'field.method_id',
            'field.method_id',
            'field.method_id.startswith',
            'field.owner',
            'field.unit',
            'metadata.assumptions',
            'metadata.limitations',
            'metadata.method',
            'metadata.weighting',
            'metadata.weighting',
            'metadata.weighting.weight_field',
            'metadata.weighting.weighting_mode',
            'reason.value',
            'status.value'],
 '_tail': ['CalculationStatus.AVAILABLE',
           'item.in_tail',
           'item.in_tail',
           'item.rarity_rank',
           'item.state_count',
           'item.state_frequency',
           'item.state_id',
           'item.state_id',
           'ranking.append',
           'scalar.reason_codes',
           'scalar.status',
           'value.denominator',
           'value.denominator',
           'value.limitations',
           'value.limitations',
           'value.membership_metadata',
           'value.options',
           'value.options',
           'value.options',
           'value.options',
           'value.options',
           'value.options.count_threshold',
           'value.options.frequency_threshold',
           'value.options.rule',
           'value.options.rule',
           'value.options.state_ids',
           'value.ranking_metadata',
           'value.ranking_rule',
           'value.rarity_ranking',
           'value.rarity_ranking',
           'value.reason_codes',
           'value.reason_codes',
           'value.representation',
           'value.representation',
           'value.scope',
           'value.scope',
           'value.scope',
           'value.status',
           'value.status',
           'value.status',
           'value.tail_membership',
           'value.tail_membership',
           'value.tail_record_share',
           'value.tail_support_size'],
 'assemble_report': ['CanonicalReport.from_dict',
                     'bundle.inventory',
                     'bundle.observability',
                     'bundle.observability.capabilities',
                     'bundle.records',
                     'bundle.records',
                     'bundle.records',
                     'bundle.records',
                     'bundle.records',
                     'bundle.records',
                     'bundle.records',
                     'bundle.version_order',
                     'bundle.version_order.loaded_versions',
                     'closure.scope',
                     'closure.scope.scope_id',
                     'closure.validation_messages',
                     'duplicates.representation',
                     'duplicates.scope',
                     'duplicates.scope.scope_id',
                     'empirical_representations.append',
                     'empirical_representations.append',
                     'empirical_representations.append',
                     'empirical_representations.append',
                     'failure.capability',
                     'failure.capability',
                     'failure.capability',
                     'failure.capability.value',
                     'failure.capability.value',
                     'failure.messages',
                     'failure.messages',
                     'failure.messages',
                     'failures.setdefault',
                     'failures.setdefault(failure.capability.value, []).extend',
                     'key.value',
                     "operations['content_diagnostics'].append",
                     "operations['content_diagnostics'].append",
                     "operations['content_diagnostics'].append",
                     "operations['dataset_longitudinal'].append",
                     "operations['intervention_simulation'].append",
                     "operations['intervention_simulation'].append",
                     "operations['intervention_simulation'].append",
                     "operations['provenance'].append",
                     "operations['provenance'].append",
                     "payload['inputs']['limitations'].append",
                     'provenance.scope',
                     'provenance.scope.scope_id',
                     'provenance.validation_messages',
                     'row.record_key',
                     'row.record_key',
                     'row.record_key.dataset_version',
                     'run.get',
                     'run.get',
                     'supplied.coverage',
                     'supplied.coverage',
                     'supplied.coverage',
                     'supplied.coverage',
                     'supplied.coverage',
                     'supplied.coverage.denominator',
                     'supplied.coverage.numerator',
                     'supplied.coverage.ratio',
                     'supplied.coverage.ratio',
                     'supplied.input_basis',
                     'supplied.representation',
                     'supplied.scope',
                     'supplied.scope.scope_id',
                     'supplied.selection_messages',
                     'supplied.unweighted',
                     'supplied.unweighted',
                     'supplied.unweighted',
                     'supplied.unweighted',
                     'supplied.unweighted',
                     'supplied.unweighted',
                     'supplied.unweighted',
                     'supplied.unweighted',
                     'supplied.unweighted.representation',
                     'supplied.unweighted.representation',
                     'supplied.unweighted.scope',
                     'supplied.unweighted.scope',
                     'supplied.unweighted.scope',
                     'supplied.unweighted.scope',
                     'supplied.unweighted.scope',
                     'supplied.unweighted.scope.excluded_record_keys',
                     'supplied.unweighted.scope.included_record_keys',
                     'supplied.unweighted.scope.included_record_keys',
                     'supplied.unweighted.scope.scope_id',
                     'supplied.weighted',
                     'supplied.weighted',
                     'supplied.weighted',
                     'supplied.weighted',
                     'supplied.weighted.representation',
                     'supplied.weighted.scope',
                     'tail.representation',
                     'tail.scope',
                     'tail.scope.scope_id']}


def phase4_step3_assembly_boundary(path: Path) -> None:
    """Inspect only the supplied assembly source without executing it.

    Fixed reviewed inventories constrain definitions, imports, call targets and
    validation arithmetic. They are never regenerated from inspected source.
    The release controller separately freezes result and the other runtime modules.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (OSError, UnicodeError, SyntaxError) as exc:
        raise ValueError("Phase 4 Step 3 assembly source cannot be inspected") from exc
    doc = ast.get_docstring(tree) or ""
    if "Owner IDs:" not in doc or "Current phase status:" not in doc:
        raise ValueError("Phase 4 Step 3 assembly ownership metadata is missing")
    allowed_top = (ast.Import, ast.ImportFrom, ast.Assign, ast.AnnAssign,
                   ast.FunctionDef, ast.ClassDef)
    for index, node in enumerate(tree.body):
        if index == 0 and isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            continue
        if not isinstance(node, allowed_top):
            raise ValueError("Phase 4 Step 3 assembly has an unapproved module statement")
    imports = []
    functions = []
    classes = []
    calls = {}
    arithmetic = {}
    mutations = []
    declarations = []
    traversal = []
    attributes = {}
    headers = []
    literal_declarations = []
    literal_containers = []
    call_names = {node.func.id for node in ast.walk(tree)
                  if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)}
    forbidden = (ast.Lambda, ast.AsyncFunctionDef, ast.Await, ast.With,
                 ast.AsyncWith, ast.Global, ast.Nonlocal, ast.NamedExpr)
    forbidden_names = {"eval", "exec", "compile", "__import__", "getattr",
                       "setattr", "delattr", "globals", "locals", "vars",
                       "open", "input", "breakpoint", "print", "exit", "quit",
                       "asdict", "astuple"}
    forbidden_attributes = {"__builtins__", "__globals__", "__code__", "__subclasses__",
                            "__class__", "__dict__", "__getattribute__", "__getattr__", "__setattr__",
                            "__reduce__", "__reduce_ex__", "__mro__", "__bases__",
                            "open", "read", "read_text", "read_bytes", "write", "write_text",
                            "write_bytes", "mkdir", "unlink", "system", "popen", "connect",
                            "connect_ex", "getaddrinfo", "urlopen", "urlretrieve", "send", "sendall"}
    stack = [(tree, "<module>")]
    while stack:
        node, scope = stack.pop()
        if isinstance(node, forbidden):
            raise ValueError("Phase 4 Step 3 assembly has a callback or executable control outside scope")
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            scope = node.name if scope == "<module>" else scope + "." + node.name
            if isinstance(node, ast.FunctionDef):
                functions.append(scope)
                headers.append((scope, ast.dump(node.args, include_attributes=False),
                                tuple(ast.unparse(item) for item in node.decorator_list),
                                ast.unparse(node.returns) if node.returns is not None else ""))
            else:
                classes.append(scope)
                headers.append((scope, tuple(ast.unparse(item) for item in node.bases),
                                tuple(ast.unparse(item) for item in node.keywords),
                                tuple(ast.unparse(item) for item in node.decorator_list)))
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            if scope != "<module>" or node not in tree.body:
                raise ValueError("Phase 4 Step 3 assembly imports must be explicit and at module scope")
            imports.append(ast.dump(node, include_attributes=False))
        if isinstance(node, ast.Name) and node.id in forbidden_names:
            raise ValueError("Phase 4 Step 3 assembly names a forbidden execution capability")
        if scope != "<module>" and ((isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store) and node.id in call_names)
                                    or (isinstance(node, ast.arg) and node.arg in call_names)):
            raise ValueError("Phase 4 Step 3 assembly shadows an approved call target")
        if isinstance(node, ast.Attribute):
            attributes.setdefault(scope, []).append(ast.unparse(node))
        if isinstance(node, ast.Attribute) and node.attr in forbidden_attributes:
            raise ValueError("Phase 4 Step 3 assembly names a forbidden IO or dynamic capability")
        if isinstance(node, ast.Call):
            if not isinstance(node.func, (ast.Name, ast.Attribute)):
                raise ValueError("Phase 4 Step 3 assembly invokes a dynamic call target")
            calls.setdefault(scope, []).append(ast.unparse(node.func))
            if isinstance(node.func, ast.Attribute) and node.func.attr == "__setattr__":
                mutations.append((scope, ast.unparse(node)))
        if isinstance(node, (ast.BinOp, ast.UnaryOp, ast.AugAssign)):
            arithmetic.setdefault(scope, []).append(ast.unparse(node))
        if (scope == "<module>" or scope in classes) and isinstance(node, (ast.Assign, ast.AnnAssign, ast.Delete)):
            declarations.append((scope, ast.unparse(node)))
        if scope == "_metadata_text" and isinstance(node, (ast.Assign, ast.AnnAssign)):
            literal_declarations.append((scope, ast.unparse(node)))
        if isinstance(node, (ast.Dict, ast.Tuple, ast.List, ast.Set)):
            try:
                literal = ast.literal_eval(node)
            except (ValueError, TypeError, SyntaxError):
                literal = None
            if literal:
                literal_containers.append((scope, ast.unparse(node)))
        if isinstance(node, (ast.Yield, ast.YieldFrom, ast.Delete)):
            traversal.append((scope, ast.unparse(node)))
        if isinstance(node, ast.Attribute) and isinstance(node.ctx, (ast.Store, ast.Del)):
            raise ValueError("Phase 4 Step 3 assembly has an unapproved attribute mutation")
        stack.extend((child, scope) for child in ast.iter_child_nodes(node))
    if sorted(imports) != PHASE4_STEP3_ASSEMBLY_IMPORTS:
        raise ValueError("Phase 4 Step 3 assembly imports differ from the reviewed import-safe typed-result inventory")
    if sorted(functions) != PHASE4_STEP3_ASSEMBLY_FUNCTIONS or sorted(classes) != PHASE4_STEP3_ASSEMBLY_CLASSES:
        raise ValueError("Phase 4 Step 3 assembly definitions differ from the approved contract")
    if {name: sorted(values) for name, values in calls.items()} != PHASE4_STEP3_ASSEMBLY_CALLS:
        raise ValueError("Phase 4 Step 3 assembly call targets differ from the reviewed inventory")
    if {name: sorted(values) for name, values in arithmetic.items()} != PHASE4_STEP3_ASSEMBLY_ARITHMETIC:
        raise ValueError("Phase 4 Step 3 assembly arithmetic exceeds reviewed semantic validation")
    if sorted(mutations) != PHASE4_STEP3_ASSEMBLY_MUTATIONS:
        raise ValueError("Phase 4 Step 3 assembly mutation differs from reviewed immutable construction")
    if sorted(declarations) != PHASE4_STEP3_ASSEMBLY_DECLARATIONS:
        raise ValueError("Phase 4 Step 3 assembly module declarations differ from the approved contract")
    if sorted(traversal) != PHASE4_STEP3_ASSEMBLY_TRAVERSAL:
        raise ValueError("Phase 4 Step 3 assembly generator or teardown differs from reviewed local traversal")
    if {name: sorted(values) for name, values in attributes.items()} != PHASE4_STEP3_ASSEMBLY_ATTRIBUTES:
        raise ValueError("Phase 4 Step 3 assembly attributes exceed the reviewed pure contract")
    if sorted(literal_declarations) != PHASE4_STEP3_ASSEMBLY_LITERAL_DECLARATIONS:
        raise ValueError("Phase 4 Step 3 assembly method registry differs from reviewed owner declarations")
    if sorted(literal_containers) != PHASE4_STEP3_ASSEMBLY_LITERAL_CONTAINERS:
        raise ValueError("Phase 4 Step 3 assembly literal evidence boundaries differ from reviewed declarations")
    if sorted(headers) != PHASE4_STEP3_ASSEMBLY_HEADERS:
        raise ValueError("Phase 4 Step 3 assembly definition headers differ from the reviewed contract")



def phase4_step3_main(step: int = 3) -> int:
    """Validate Step 3 control, the frozen canonical contract and pure assembly."""
    import hashlib
    import runpy

    if type(step) is not int or step != 3:
        raise ValueError("Only authorized Phase 4 Step 3 traceability is available")
    control = runpy.run_path(str(ROOT / "scripts/release_check.py"),
                            run_name="phase4_step3_traceability_control")
    control["audit_phase4_step3"](step=step)
    schema_path = ROOT / "schemas/report.schema.json"
    if hashlib.sha256(schema_path.read_bytes()).hexdigest() != PHASE4_STEP2_REPORT_SCHEMA_SHA256:
        raise ValueError("Phase 4 Step 3 report schema differs from the frozen Step 2 contract")
    phase4_step2_result_boundary(PACKAGE / "result.py")
    phase4_step3_assembly_boundary(PACKAGE / "reports/assembly.py")
    print("Phase 4 Step 3: frozen canonical results and reviewed evidence assembly: PASS")
    return 0


# Step 4 adds privacy after canonical assembly. Historical stage checkers above
# retain their original source. Fixed identities below are review data; none is
# derived from the current source when the boundary runs.
PHASE4_STEP4_INHERITED_AST_SHA256 = {
    "src/recursive_integrity_toolkit/result.py": "4cbf8f28cb0aa04edc0a931c8a27b64c18ee1975b7e93a51edf62d34f6615ca9",
    "src/recursive_integrity_toolkit/reports/assembly.py": "23b0574b56baa9b147a221742c53a37d995352d52d51f528bda0316eef30fd72",
    "src/recursive_integrity_toolkit/utils/hashing.py": "d263ee776c8c2c9751106b959589cb7c49f5bbc3be0cbf7634717c88dccb8b98",
    "src/recursive_integrity_toolkit/utils/logging.py": "35ad89e78bf13acf4ca8adea239b5c79db8001f5cbabbf2cfc7e27680e9c3e57",
    "src/recursive_integrity_toolkit/config.py": "a85a8bab70aa2e2625be4943d1769ac33301d8a6725396925c7dbf44ac28f3b2",
}
PHASE4_STEP4_RUNTIME_AST_SHA256 = {
    "src/recursive_integrity_toolkit/config.py": "92fb35fe0895f799c0b90c20d80f0262c92da8afb2b96e17154a870837ed71d5",
    "src/recursive_integrity_toolkit/reports/assembly.py": "e96f66d5fcaa45e2eea53f19e78db345d703b4d565b4d635944682c728eb2329",
    "src/recursive_integrity_toolkit/result.py": "a5f9f85b2e10128202feb1bc122f912315b0b46ccf1e2c67e0c7127229160a12",
    "src/recursive_integrity_toolkit/utils/hashing.py": "6774dbc0177e876731da2d163f85acd583430dee1747a092528e0edaa869c0da",
    "src/recursive_integrity_toolkit/utils/logging.py": "973a746221ea3d83fd1ab42a5687075bed6ad962a0c727cfa6350e94f71c94d3"
}
PHASE4_STEP4_ADDITIVE_BINDINGS = {
    "src/recursive_integrity_toolkit/result.py": [
        "PrivacyMode",
        "RecordIdMode",
        "SafeReportView"
    ],
    "src/recursive_integrity_toolkit/reports/assembly.py": [
        "_PRIVACY_SAFE_TEXT",
        "_privacy_contract",
        "_privacy_alias",
        "_privacy_text",
        "_privacy_value",
        "_privacy_run_fields",
        "privacy_view",
        "build_run_metadata"
    ],
    "src/recursive_integrity_toolkit/utils/hashing.py": [
        "canonical_json_bytes",
        "sha256_canonical",
        "_phase4_secret_file",
        "IdentifierProtection"
    ],
    "src/recursive_integrity_toolkit/utils/logging.py": [
        "_TEMPLATES",
        "_FIELDS",
        "_EXCEPTION_TYPES",
        "_severity",
        "_code",
        "_protection",
        "_policy",
        "safe_code",
        "safe_diagnostic_text",
        "safe_remediation",
        "safe_field",
        "safe_role",
        "safe_effects",
        "safe_record_key",
        "_position",
        "safe_diagnostic",
        "format_diagnostic",
        "emit_diagnostic"
    ],
    "src/recursive_integrity_toolkit/config.py": [
        "Phase4Options",
        "_phase4_config_data",
        "_phase4_option_path",
        "_phase4_literal",
        "resolve_phase4_options",
        "phase4_config_summary",
        "phase4_config_hash"
    ]
}


def _phase4_step4_ast_digest(nodes: list) -> str:
    """Hash a location-free AST consistently on supported Python 3.11/3.12."""
    import hashlib
    import json

    def canonical(value):
        if isinstance(value, ast.AST):
            return [type(value).__name__, [[name, canonical(item)]
                    for name, item in ast.iter_fields(value)
                    if name != "type_params" or item]]
        if isinstance(value, list):
            return [canonical(item) for item in value]
        return [type(value).__name__, repr(value)]

    # Python 3.12 adds empty type_params fields. Ignoring only empty ones makes
    # the same non-generic source portable; nonempty type parameters remain data.
    module = ast.Module(body=nodes, type_ignores=[])
    payload = json.dumps(canonical(module), ensure_ascii=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _phase4_step4_bound_names(node) -> set[str]:
    """Return only explicit top-level definition or assignment targets."""
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        return {node.name}
    if isinstance(node, ast.Assign):
        targets = node.targets
    elif isinstance(node, ast.AnnAssign):
        targets = [node.target]
    else:
        return set()
    return {item.id for target in targets for item in ast.walk(target)
            if isinstance(item, ast.Name) and isinstance(item.ctx, ast.Store)}


def phase4_step4_runtime_boundary(path: Path, relative: str) -> None:
    """Check one reviewed Step 4 runtime module without importing its code.

    The complete reviewed AST constrains calls, imports, declarations, arithmetic,
    sink use and control flow. A separate accepted-Step-3 identity freezes all
    inherited non-import declarations after the explicitly named additions are
    removed. Only the module ownership documentation is outside the AST digest.
    """
    if relative not in PHASE4_STEP4_INHERITED_AST_SHA256:
        raise ValueError("Phase 4 Step 4 runtime path is outside the approved five modules")
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (OSError, UnicodeError, SyntaxError) as exc:
        raise ValueError("Phase 4 Step 4 runtime source cannot be inspected") from exc
    doc = ast.get_docstring(tree) or ""
    if "Owner IDs:" not in doc or "Current phase status:" not in doc:
        raise ValueError("Phase 4 Step 4 runtime ownership metadata is missing")
    body = tree.body[1:] if ast.get_docstring(tree) is not None else tree.body
    if _phase4_step4_ast_digest(body) != PHASE4_STEP4_RUNTIME_AST_SHA256.get(relative):
        raise ValueError("Phase 4 Step 4 runtime differs from the reviewed privacy implementation")
    additions = set(PHASE4_STEP4_ADDITIVE_BINDINGS.get(relative, ()))
    inherited = []
    observed_additions = set()
    for node in body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            continue
        names = _phase4_step4_bound_names(node)
        if names & additions:
            if not names <= additions or names & observed_additions:
                raise ValueError("Phase 4 Step 4 additions rebind an inherited or duplicate name")
            observed_additions.update(names)
        else:
            inherited.append(node)
    if observed_additions != additions:
        raise ValueError("Phase 4 Step 4 reviewed additive declaration is missing")
    if _phase4_step4_ast_digest(inherited) != PHASE4_STEP4_INHERITED_AST_SHA256[relative]:
        raise ValueError("Phase 4 Step 4 changed an inherited runtime helper or contract")


def phase4_step4_privacy_boundary(root: Path) -> None:
    """Enforce the five explicit privacy modules and frozen public schema."""
    import hashlib

    for relative in sorted(PHASE4_STEP4_INHERITED_AST_SHA256):
        phase4_step4_runtime_boundary(root / relative, relative)
    schema = root / "schemas/report.schema.json"
    if hashlib.sha256(schema.read_bytes()).hexdigest() != PHASE4_STEP2_REPORT_SCHEMA_SHA256:
        raise ValueError("Phase 4 Step 4 changed the frozen public report schema")


def phase4_step4_main(step: int = 4) -> int:
    """Validate Step 4 control, additive privacy and inherited helper identities."""
    import runpy

    if type(step) is not int or step != 4:
        raise ValueError("Only authorized Phase 4 Step 4 traceability is available")
    control = runpy.run_path(str(ROOT / "scripts/release_check.py"),
                            run_name="phase4_step4_traceability_control")
    control["audit_phase4_step4"](step=step)
    phase4_step4_privacy_boundary(ROOT)
    print("Phase 4 Step 4: inherited contracts and reviewed privacy, metadata and diagnostics: PASS")
    return 0


# Step 5 opens only two rendering placeholders. These review identities are
# fixed checker data, independent of the source being inspected at gate time.
PHASE4_STEP5_RUNTIME_AST_SHA256 = {
    "src/recursive_integrity_toolkit/reports/json_report.py": "04c46cdd644021b01b285dd6e62a2b026be27ac60607cc6117582d9581c0a283",
    "src/recursive_integrity_toolkit/reports/markdown_report.py": "08ece6fc0ba3ea57dab335508978a974439c7f37aa84e4dcd652615fa6628e84",
}
PHASE4_STEP5_RUNTIME_OWNERS = {
    "src/recursive_integrity_toolkit/reports/json_report.py": ["PR-013", "PR-016"],
    "src/recursive_integrity_toolkit/reports/markdown_report.py": ["PR-013", "PR-018"],
}


def phase4_step5_runtime_boundary(path: Path, relative: str) -> None:
    """Inspect the complete reviewed renderer AST without importing its code.

    A fixed identity covers imports, function signatures, literal declarations,
    calls, effects and control flow. The two accepted placeholders contained no
    inherited functions or assignments. Every other runtime module is frozen by
    the separately verified accepted Step 4 file inventory.
    """
    if relative not in PHASE4_STEP5_RUNTIME_AST_SHA256:
        raise ValueError("Phase 4 Step 5 runtime path is outside the two approved renderers")
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (OSError, UnicodeError, SyntaxError) as exc:
        raise ValueError("Phase 4 Step 5 runtime source cannot be inspected") from exc
    doc = ast.get_docstring(tree) or ""
    if ("Owner IDs:" not in doc or "Current phase status:" not in doc
            or not all(owner in doc for owner in PHASE4_STEP5_RUNTIME_OWNERS[relative])):
        raise ValueError("Phase 4 Step 5 renderer ownership metadata is missing")
    body = tree.body[1:] if ast.get_docstring(tree) is not None else tree.body
    if _phase4_step4_ast_digest(body) != PHASE4_STEP5_RUNTIME_AST_SHA256[relative]:
        raise ValueError("Phase 4 Step 5 runtime differs from the reviewed rendering implementation")


def phase4_step5_renderers_boundary(root: Path) -> None:
    """Enforce both pure renderer implementations and the frozen public schema."""
    import hashlib

    for relative in sorted(PHASE4_STEP5_RUNTIME_AST_SHA256):
        phase4_step5_runtime_boundary(root / relative, relative)
    if hashlib.sha256((root / "schemas/report.schema.json").read_bytes()).hexdigest() != PHASE4_STEP2_REPORT_SCHEMA_SHA256:
        raise ValueError("Phase 4 Step 5 changed the frozen public report schema")


def phase4_step5_main(step: int = 5) -> int:
    """Validate explicit Step 5 authorization and reviewed renderer boundaries."""
    import runpy

    if type(step) is not int or step != 5:
        raise ValueError("Only authorized Phase 4 Step 5 traceability is available")
    control = runpy.run_path(str(ROOT / "scripts/release_check.py"),
                            run_name="phase4_step5_traceability_control")
    control["audit_phase4_step5"](step=step)
    phase4_step5_renderers_boundary(ROOT)
    print("Phase 4 Step 5: reviewed JSON and Markdown rendering and frozen prior contracts: PASS")
    return 0


PHASE4_STEP6_RUNTIME_AST_SHA256 = {'src/recursive_integrity_toolkit/utils/logging.py': '1ce0d0c77339f4c63e9f091fa218cfcb0202c709b235643f550a8c3d4c0160b5',
 'src/recursive_integrity_toolkit/utils/paths.py': 'f9e77ed3638b520f81769ae2c09095572913b501383d53124d51cde2826a5efa'}

PHASE4_STEP6_INHERITED_AST_SHA256 = {'src/recursive_integrity_toolkit/utils/logging.py': '973a746221ea3d83fd1ab42a5687075bed6ad962a0c727cfa6350e94f71c94d3',
 'src/recursive_integrity_toolkit/utils/paths.py': '0010c7bbf86e389ac2599eae023a89caaabe48b10a65cfaeddb01aa619112824'}

PHASE4_STEP6_INHERITED_NODES = {'src/recursive_integrity_toolkit/utils/logging.py': 24,
 'src/recursive_integrity_toolkit/utils/paths.py': 17}

def phase4_step6_runtime_boundary(path: Path, relative: str) -> None:
    """Enforce reviewed output code and unchanged inherited input/diagnostic AST."""
    if relative not in PHASE4_STEP6_RUNTIME_AST_SHA256:
        raise ValueError("Step 6 runtime is limited to output paths and diagnostics")
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, SyntaxError) as error:
        raise ValueError("Step 6 output helper cannot be inspected") from error
    doc = ast.get_docstring(tree) or ""
    if "Owner IDs:" not in doc or "Current phase status:" not in doc or "PR-015" not in doc:
        raise ValueError("Step 6 output ownership metadata is missing")
    body = tree.body[1:] if ast.get_docstring(tree) is not None else tree.body
    if _phase4_step4_ast_digest(body) != PHASE4_STEP6_RUNTIME_AST_SHA256[relative]:
        raise ValueError("Step 6 output implementation differs from the reviewed AST")
    if _phase4_step4_ast_digest(body[:PHASE4_STEP6_INHERITED_NODES[relative]]) != PHASE4_STEP6_INHERITED_AST_SHA256[relative]:
        raise ValueError("Step 6 changed an inherited input or diagnostic helper")


def phase4_step6_output_boundary(root: Path) -> None:
    for relative in sorted(PHASE4_STEP6_RUNTIME_AST_SHA256):
        phase4_step6_runtime_boundary(root / relative, relative)
    phase4_step5_renderers_boundary(root)


def phase4_step6_main(step: int = 6) -> int:
    import runpy
    if type(step) is not int or step != 6:
        raise ValueError("Only authorized Phase 4 Step 6 traceability is available")
    control = runpy.run_path(str(ROOT / "scripts/release_check.py"), run_name="phase4_step6_traceability_control")
    control["audit_phase4_step6"](step=step)
    phase4_step6_output_boundary(ROOT)
    print("Phase 4 Step 6: safe publication and preserved input/report contracts: PASS")
    return 0


PHASE4_STEP7_RUNTIME_AST_SHA256 = {'src/recursive_integrity_toolkit/cli.py': 'c1791ddf073a9ca5ddf08268b7a66e1a67f359a1b8d97a636d37e914dbb0f40b',
 'src/recursive_integrity_toolkit/config.py': 'cbb96ab25130e4fe45a94cc03299aaa27015a496e38e7dcc6bec1c5d2f7e2573'}

PHASE4_STEP7_CONFIG_INHERITED_AST_SHA256 = '92fb35fe0895f799c0b90c20d80f0262c92da8afb2b96e17154a870837ed71d5'

PHASE4_STEP7_CONFIG_INHERITED_NODES = 40

def phase4_step7_runtime_boundary(path: Path, relative: str) -> None:
    """Inspect fixed reviewed orchestration AST and unchanged inherited config."""
    if relative not in PHASE4_STEP7_RUNTIME_AST_SHA256:
        raise ValueError("Step 7 runtime is limited to CLI and additive configuration")
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, SyntaxError) as error:
        raise ValueError("Step 7 runtime cannot be inspected") from error
    doc = ast.get_docstring(tree) or ""
    if "Owner IDs:" not in doc or "Current phase status:" not in doc or "PR-016" not in doc:
        raise ValueError("Step 7 ownership documentation is missing")
    body = tree.body[1:]
    if _phase4_step4_ast_digest(body) != PHASE4_STEP7_RUNTIME_AST_SHA256[relative]:
        raise ValueError("Step 7 runtime differs from the reviewed orchestration")
    if relative.endswith("/config.py") and _phase4_step4_ast_digest(body[:PHASE4_STEP7_CONFIG_INHERITED_NODES]) != PHASE4_STEP7_CONFIG_INHERITED_AST_SHA256:
        raise ValueError("Step 7 changed inherited configuration behavior")


def phase4_step7_cli_boundary(root: Path) -> None:
    for relative in sorted(PHASE4_STEP7_RUNTIME_AST_SHA256):
        phase4_step7_runtime_boundary(root / relative, relative)
    phase4_step6_output_boundary(root)


def phase4_step7_main(step: int = 7) -> int:
    import runpy
    if type(step) is not int or step != 7:
        raise ValueError("Only authorized Phase 4 Step 7 traceability is available")
    control = runpy.run_path(str(ROOT / "scripts/release_check.py"), run_name="phase4_step7_traceability_control")
    control["audit_phase4_step7"](step=step)
    phase4_step7_cli_boundary(ROOT)
    print("Phase 4 Step 7: local audit/validate orchestration and frozen calculation/report owners: PASS")
    return 0


PHASE4_STEP8_RUNTIME_AST_SHA256 = {'src/recursive_integrity_toolkit/cli.py': 'c4bd7981153974857c03ebe79b7daca6cc68ab324980b8434e6ef8dd3d7fd9c8',
 'src/recursive_integrity_toolkit/config.py': 'df7f8d96997cf0bcae5c53d78a130f07ca847c3bbc609e8e6d5c507d926507fa'}

PHASE4_STEP8_CONFIG_INHERITED_AST_SHA256 = 'cbb96ab25130e4fe45a94cc03299aaa27015a496e38e7dcc6bec1c5d2f7e2573'

PHASE4_STEP8_CONFIG_INHERITED_NODES = 42

def phase4_step8_runtime_boundary(path: Path, relative: str) -> None:
    """Inspect fixed reviewed orchestration AST and unchanged inherited config."""
    if relative not in PHASE4_STEP8_RUNTIME_AST_SHA256:
        raise ValueError("Step 8 runtime is limited to CLI and additive configuration")
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, SyntaxError) as error:
        raise ValueError("Step 8 runtime cannot be inspected") from error
    doc = ast.get_docstring(tree) or ""
    if "Owner IDs:" not in doc or "Current phase status:" not in doc or "PR-016" not in doc:
        raise ValueError("Step 8 ownership documentation is missing")
    body = tree.body[1:]
    if _phase4_step4_ast_digest(body) != PHASE4_STEP8_RUNTIME_AST_SHA256[relative]:
        raise ValueError("Step 8 runtime differs from the reviewed orchestration")
    if relative.endswith("/config.py") and _phase4_step4_ast_digest(body[:PHASE4_STEP8_CONFIG_INHERITED_NODES]) != PHASE4_STEP8_CONFIG_INHERITED_AST_SHA256:
        raise ValueError("Step 8 changed inherited configuration behavior")


def phase4_step8_cli_boundary(root: Path) -> None:
    for relative in sorted(PHASE4_STEP8_RUNTIME_AST_SHA256):
        phase4_step8_runtime_boundary(root / relative, relative)
    phase4_step6_output_boundary(root)


def phase4_step8_main(step: int = 8) -> int:
    import runpy
    if type(step) is not int or step != 8:
        raise ValueError("Only authorized Phase 4 Step 8 traceability is available")
    control = runpy.run_path(str(ROOT / "scripts/release_check.py"), run_name="phase4_step8_traceability_control")
    control["audit_phase4_step8"](step=step)
    phase4_step8_cli_boundary(ROOT)
    print("Phase 4 Step 8: explicit pair and packaged Hero orchestration and frozen calculation/report owners: PASS")
    return 0


def cli_main(argv: list[str] | None = None) -> int:
    """Select the active phase without changing historical checker semantics."""
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", type=int, choices=(3, 4))
    parser.add_argument("--step", type=int)
    args = parser.parse_args(argv)
    if args.phase is None and args.step is None:
        return main()
    if args.phase == 3 and args.step == PHASE3_ACTIVE_STEP:
        return main()
    if args.phase == 4 and args.step == 1:
        return phase4_main(step=args.step)
    if args.phase == 4 and args.step == 2:
        return phase4_step2_main(step=args.step)
    if args.phase == 4 and args.step == 3:
        return phase4_step3_main(step=args.step)
    if args.phase == 4 and args.step == 4:
        return phase4_step4_main(step=args.step)
    if args.phase == 4 and args.step == 5:
        return phase4_step5_main(step=args.step)
    if args.phase == 4 and args.step == 6:
        return phase4_step6_main(step=args.step)
    if args.phase == 4 and args.step == 7:
        return phase4_step7_main(step=args.step)
    if args.phase == 4 and args.step == 8:
        return phase4_step8_main(step=args.step)
    parser.error("Choose explicit --phase 3 --step 11 or --phase 4 --step 1 or --phase 4 --step 2 or --phase 4 --step 3 or --phase 4 --step 4 or --phase 4 --step 5 or --phase 4 --step 6 or --phase 4 --step 7 or --phase 4 --step 8")
    return 2


if __name__ == "__main__":
    raise SystemExit(cli_main())
