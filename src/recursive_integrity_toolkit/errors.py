"""Define Phase 2 structured toolkit errors and approved validation codes.

Owner IDs:
    Product-rule infrastructure for PR-001, PR-002, PR-003, PR-004, PR-007, PR-008,
    PR-009, PR-010, PR-011, PR-017

Inputs:
    Explicit configuration, ingestion, schema, provenance, parent, and security failures.

Outputs:
    Stable exception categories and approved error and warning codes.

Assumptions:
    User-visible error messages are constructed without raw source content.

Limits:
    No source-content interpolation, logging policy, report rendering, metric, lineage analysis,
    or automatic remediation is implemented here.

Current phase status:
    Phase 2 Step 1 error contracts. Import-safe. No analytical behavior.
"""

from __future__ import annotations

from enum import StrEnum


class ErrorCode(StrEnum):
    FILE_NOT_FOUND = "E_FILE_NOT_FOUND"
    FILE_FORMAT_UNSUPPORTED = "E_FILE_FORMAT_UNSUPPORTED"
    FILE_ENCODING = "E_FILE_ENCODING"
    FILE_PARSE = "E_FILE_PARSE"
    SCHEMA_REQUIRED_FIELD = "E_SCHEMA_REQUIRED_FIELD"
    SCHEMA_TYPE = "E_SCHEMA_TYPE"
    SCHEMA_ENUM = "E_SCHEMA_ENUM"
    RECORD_DUPLICATE_ID = "E_RECORD_DUPLICATE_ID"
    RECORD_EMPTY_CONTENT = "E_RECORD_EMPTY_CONTENT"
    PROVENANCE_DUPLICATE_ROW = "E_PROVENANCE_DUPLICATE_ROW"
    PROVENANCE_UNMATCHED_ROW = "E_PROVENANCE_UNMATCHED_ROW"
    PARENT_FORMAT = "E_PARENT_FORMAT"
    PARENT_AMBIGUOUS = "E_PARENT_AMBIGUOUS"
    PARENT_FUTURE_VERSION = "E_PARENT_FUTURE_VERSION"
    LINEAGE_CYCLE = "E_LINEAGE_CYCLE"
    VERSION_ORDER_CONFLICT = "E_VERSION_ORDER_CONFLICT"
    REPRESENTATION_INCOMPATIBLE = "E_REPRESENTATION_INCOMPATIBLE"
    MAPPING_SOURCE_FIELD_MISSING = "E_MAPPING_SOURCE_FIELD_MISSING"
    MAPPING_TARGET_COLLISION = "E_MAPPING_TARGET_COLLISION"
    MAPPING_UNSAFE_TRANSFORM = "E_MAPPING_UNSAFE_TRANSFORM"
    WEIGHT_INVALID = "E_WEIGHT_INVALID"
    CONTENT_REF_OUTSIDE_BASE = "E_CONTENT_REF_OUTSIDE_BASE"
    CONTENT_REF_MISSING = "E_CONTENT_REF_MISSING"
    CONFIG_INVALID = "E_CONFIG_INVALID"
    EMPTY_DATASET = "E_EMPTY_DATASET"


class WarningCode(StrEnum):
    PROVENANCE_MISSING_ROW = "W_PROVENANCE_MISSING_ROW"
    GROUNDING_UNKNOWN = "W_GROUNDING_UNKNOWN"
    PARENT_UNRESOLVED = "W_PARENT_UNRESOLVED"
    PARENT_BARE_COMPATIBILITY = "W_PARENT_BARE_COMPATIBILITY"
    PARENT_DUPLICATE_REFERENCE = "W_PARENT_DUPLICATE_REFERENCE"
    GENERATION_MISMATCH = "W_GENERATION_MISMATCH"
    REPRESENTATION_FALLBACK = "W_REPRESENTATION_FALLBACK"
    LONGITUDINAL_INCOMPATIBLE_REPRESENTATION = "W_LONGITUDINAL_INCOMPATIBLE_REPRESENTATION"
    VERSION_ORDER_MISSING = "W_VERSION_ORDER_MISSING"
    CONTENT_ANALYSIS_UNAVAILABLE = "W_CONTENT_ANALYSIS_UNAVAILABLE"
    OPTIONAL_FIELD_MISSING = "W_OPTIONAL_FIELD_MISSING"
    PARTIAL_LINEAGE = "W_PARTIAL_LINEAGE"
    PROVENANCE_ESTIMATED = "W_PROVENANCE_ESTIMATED"
    MAPPING_VALUE_UNMAPPED = "W_MAPPING_VALUE_UNMAPPED"


class ToolkitError(Exception):
    """Base content-safe toolkit exception."""

    def __init__(self, code: ErrorCode, message: str) -> None:
        self.code = code
        self.safe_message = str(message)
        super().__init__(f"{code.value}: {self.safe_message}")


class ConfigurationError(ToolkitError):
    """Invalid local configuration."""


class InputError(ToolkitError):
    """Invalid or unavailable local input."""


class SchemaError(ToolkitError):
    """Canonical schema or mapping failure."""


class SecurityError(ToolkitError):
    """Local security-boundary violation."""


class IngestionError(InputError):
    """Physical input failure with a safe location and no source-value echo."""

    def __init__(
        self,
        code: ErrorCode,
        message: str,
        *,
        file_role: str | None = None,
        file_path: str | None = None,
        row_number: int | None = None,
        line_number: int | None = None,
        byte_offset: int | None = None,
    ) -> None:
        self.file_role = file_role
        self.file_path = file_path
        self.row_number = row_number
        self.line_number = line_number
        self.byte_offset = byte_offset
        super().__init__(code, message)
