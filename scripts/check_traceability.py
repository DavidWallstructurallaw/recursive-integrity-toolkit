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
PHASE3_ACTIVE_STEP = 9
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
    print("Phase 3 Step 9 reviewed explicit-pair and inherited definition/import boundaries: PASS")
    print("no-algorithm phase boundary: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
