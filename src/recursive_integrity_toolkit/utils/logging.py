"""Produce content-safe structured diagnostics for explicitly selected sinks.

Owner IDs:
    PR-015; PR-018 supporting actionable diagnostic language.
Inputs:
    Accepted validation messages or exceptions, selected privacy policy, and
    an optional shared identifier-protection context; a PublicationResult.
Outputs:
    Explicitly allowlisted diagnostic dictionaries or single-line JSON text.
Assumptions:
    A message's free text and exception details may contain private source data.
Limits:
    No logger configuration, default sink, file access, metric, network call,
    traceback, content-bearing debug mode, or import-time output. Pseudonyms
    protect identifiers but do not establish statistical anonymity.
Current phase status:
    Preserved Step 4 diagnostics plus Step 6 safe publication outcomes.
"""
from __future__ import annotations

import json

from ..errors import (
    CanonicalValidationError, ConfigurationError, ErrorCode, IngestionError,
    InputError, MappingError, SchemaError, SecurityError, ToolkitError, WarningCode,
)
from ..models import (
    CapabilityKey, FileRole, PrivacyMode, RecordKey, ValidationMessage,
    ValidationSeverity,
)
from ..result import PrivacyMode as ReportPrivacyMode, RecordIdMode
from .hashing import IdentifierProtection


# Only toolkit-authored templates are used. A producer's ``safe_message`` label
# is not proof that arbitrary caller text is safe for a selected output view.
_TEMPLATES = {
    "E_FILE_NOT_FOUND": ("A declared local input was not found.", "Check that the declared local input exists and is readable."),
    "E_FILE_FORMAT_UNSUPPORTED": ("The declared input format is unsupported.", "Use a supported local input format."),
    "E_FILE_ENCODING": ("The input encoding is invalid.", "Provide input in the required UTF-8 encoding."),
    "E_FILE_PARSE": ("A local input could not be parsed.", "Correct the input syntax at the reported location."),
    "E_SCHEMA_REQUIRED_FIELD": ("A required input field is missing.", "Supply the required canonical field or an explicit approved mapping."),
    "E_SCHEMA_TYPE": ("An input field has an invalid type.", "Use the declared canonical field type at the reported location."),
    "E_SCHEMA_ENUM": ("An input field has an unsupported declared value.", "Use one of the documented values for the canonical field."),
    "E_RECORD_DUPLICATE_ID": ("A canonical record identity is duplicated.", "Make each dataset-version and record-ID pair unique."),
    "E_RECORD_EMPTY_CONTENT": ("A record lacks usable declared content.", "Supply permitted content or an explicit supported representation."),
    "E_PROVENANCE_DUPLICATE_ROW": ("A record has duplicate provenance rows.", "Supply at most one provenance row per canonical record identity."),
    "E_PROVENANCE_UNMATCHED_ROW": ("A provenance row does not match the supplied records.", "Correct the provenance identity or supply the matching record."),
    "E_PARENT_FORMAT": ("A parent reference has an invalid format.", "Use the documented canonical parent-reference format."),
    "E_PARENT_AMBIGUOUS": ("A parent reference is ambiguous.", "Supply an explicit dataset-version and record-ID pair."),
    "E_PARENT_FUTURE_VERSION": ("A parent reference conflicts with declared version order.", "Check the parent reference against the declared version order."),
    "E_LINEAGE_CYCLE": ("Declared parent references contain a validated cycle.", "Correct the parent declarations before requesting dependent work."),
    "E_VERSION_ORDER_CONFLICT": ("Version-order declarations conflict.", "Supply one consistent explicit version order."),
    "E_REPRESENTATION_INCOMPATIBLE": ("The supplied representations are incompatible.", "Supply compatible explicit representation declarations."),
    "E_MAPPING_SOURCE_FIELD_MISSING": ("A declared mapping source field is missing.", "Correct the explicit mapping or supply its source field."),
    "E_MAPPING_TARGET_COLLISION": ("Mapping targets collide.", "Use a single unambiguous mapping for each canonical target."),
    "E_MAPPING_UNSAFE_TRANSFORM": ("A mapping operation is outside the approved language.", "Use only documented declarative mapping operations."),
    "E_WEIGHT_INVALID": ("A declared weight is invalid.", "Supply valid finite nonnegative weights for the selected weighting basis."),
    "E_CONTENT_REF_OUTSIDE_BASE": ("A content reference violates the local input boundary.", "Place the declared content inside the approved local base directory."),
    "E_CONTENT_REF_MISSING": ("A declared local content reference is unavailable.", "Check the declared reference within the approved local base directory."),
    "E_CONFIG_INVALID": ("The requested configuration is invalid or unsupported.", "Review the documented options, types, and conflicting declarations."),
    "E_EMPTY_DATASET": ("The selected input scope has no usable records.", "Supply valid records for the explicitly selected scope."),
    "W_PROVENANCE_MISSING_ROW": ("Some records lack provenance rows.", "Supply provenance rows for the affected canonical record identities."),
    "W_GROUNDING_UNKNOWN": ("External grounding is not established for the affected records.", "Supply explicit supported grounding metadata when available."),
    "W_PARENT_UNRESOLVED": ("Some declared parent references are unresolved.", "Supply the missing parent records or correct their references."),
    "W_PARENT_BARE_COMPATIBILITY": ("A bare parent reference used compatibility resolution.", "Use an explicit dataset-version and record-ID pair."),
    "W_PARENT_DUPLICATE_REFERENCE": ("A parent reference is repeated.", "Remove duplicate parent declarations for the affected record."),
    "W_GENERATION_MISMATCH": ("A generation declaration conflicts with available parent metadata.", "Review the declared generation and parent references."),
    "W_REPRESENTATION_FALLBACK": ("An explicitly permitted representation fallback was reported.", "Review the representation declaration and its disclosed limits."),
    "W_LONGITUDINAL_INCOMPATIBLE_REPRESENTATION": ("Representations do not support the requested longitudinal comparison.", "Supply compatible representations and an explicit shared state meaning."),
    "W_VERSION_ORDER_MISSING": ("An explicit version order is unavailable.", "Supply version order before requesting order-dependent comparisons."),
    "W_CONTENT_ANALYSIS_UNAVAILABLE": ("Content analysis is unavailable for the declared input.", "Supply an explicit supported representation for the requested analysis."),
    "W_OPTIONAL_FIELD_MISSING": ("An optional metadata field is missing.", "Supply the documented field when its dependent capability is required."),
    "W_PARTIAL_LINEAGE": ("Available lineage metadata is incomplete.", "Supply missing parent references and provenance where available."),
    "W_PROVENANCE_ESTIMATED": ("Some provenance declarations are estimates.", "Retain estimation labels and supply direct metadata when available."),
    "W_MAPPING_VALUE_UNMAPPED": ("A source value has no declared mapping.", "Extend the explicit mapping or correct the source declaration."),
}
_FIELDS = frozenset({
    "record_key", "dataset_version", "record_id", "content", "content_ref",
    "topic", "embedding_cluster", "source_type", "provenance_confidence",
    "external_grounding", "parent_ids", "generator_id", "generator_version",
    "transformation", "generation", "human_reviewed", "batch_id", "timestamp",
    "grounding_evidence_ref", "source_uri", "license_id", "weight",
    "representation", "version_order", "pair_order", "representation_compatibility",
})
_EXCEPTION_TYPES = (
    ToolkitError, ConfigurationError, InputError, SchemaError, SecurityError,
    IngestionError, MappingError, CanonicalValidationError,
)


def _severity(value):
    if type(value) is ValidationSeverity:
        return value.value
    if type(value) is str and value in ("info", "warning", "error", "fatal"):
        return value
    raise ValueError("diagnostic severity must be an approved value")


def _code(value):
    if type(value) in (ErrorCode, WarningCode):
        return value.value
    if type(value) is str:
        return value
    raise TypeError("diagnostic code must be a literal string or registered code")


def _protection(value):
    if value is None:
        return IdentifierProtection.create()
    if type(value) is not IdentifierProtection:
        raise TypeError("diagnostic protection requires an accepted identifier context")
    return value


def _policy(mode, record_id_mode):
    if type(mode) in (PrivacyMode, ReportPrivacyMode):
        mode = mode.value
    if type(mode) is not str or mode not in ("standard", "redacted"):
        raise ValueError("diagnostics support only standard or redacted privacy mode")
    if type(record_id_mode) is RecordIdMode:
        record_id_mode = record_id_mode.value
    chosen = ("preserve" if mode == "standard" else "hash") if record_id_mode is None else record_id_mode
    if type(chosen) is not str or chosen not in ("preserve", "hash", "omit"):
        raise ValueError("record identifier mode must be preserve, hash, or omit")
    if mode == "standard" and chosen != "preserve":
        raise ValueError("protected record identifier modes require redacted privacy mode")
    return mode, chosen


def safe_code(code, severity="error", *, protection=None):
    """Retain registered codes; protect unknown labels without inventing a class."""
    _severity(severity)
    code = _code(code)
    if code in _TEMPLATES:
        return code
    return _protection(protection).pseudonym("diagnostic_code", code)


def safe_diagnostic_text(code, severity="error"):
    """Return toolkit-authored meaning; never interpolate producer free text."""
    _severity(severity)
    return _TEMPLATES.get(_code(code), ("Unregistered diagnostic; supplied details withheld.",))[0]


def safe_remediation(code):
    """Return one actionable instruction without source fragments or URIs."""
    template = _TEMPLATES.get(_code(code))
    return [template[1] if template is not None else
            "Review the protected diagnostic and its location using the local input and declared configuration."]


def safe_field(field):
    """Keep canonical field names only; arbitrary mapping labels are withheld."""
    return field if type(field) is str and field in _FIELDS else None


def safe_role(role):
    """Keep an approved file-role label without coercing arbitrary objects."""
    if type(role) is FileRole:
        return role.value
    return role if type(role) is str and role in FileRole._value2member_map_ else None


def safe_effects(effects):
    """Preserve declared capability effects and their order without inference."""
    if type(effects) not in (tuple, list):
        raise TypeError("diagnostic capability effects must be a literal sequence")
    result = []
    for effect in effects:
        value = effect.value if type(effect) is CapabilityKey else effect
        if type(value) is not str or value not in CapabilityKey._value2member_map_:
            raise ValueError("diagnostic effect must name an approved capability")
        if value not in result:
            result.append(value)
    return result


def safe_record_key(record_key, *, mode="standard", record_id_mode=None, protection=None):
    """Apply record-ID policy only to its declared field, never to other text."""
    mode, chosen = _policy(mode, record_id_mode)
    if record_key is None:
        return None
    if type(record_key) is RecordKey:
        version, identity = record_key.dataset_version, record_key.record_id
    elif type(record_key) is dict and set(record_key) == {"dataset_version", "record_id"}:
        version, identity = record_key["dataset_version"], record_key["record_id"]
    else:
        raise TypeError("diagnostic record key requires an accepted canonical identity")
    if type(version) is not str or type(identity) is not str:
        raise TypeError("diagnostic identity components must be literal strings")
    RecordKey(version, identity)
    if mode == "standard":
        return {"dataset_version": version, "record_id": identity}
    if chosen == "omit":
        return None
    context = _protection(protection)
    return {"dataset_version": context.pseudonym("dataset_version", version),
            "record_id": identity if chosen == "preserve" else
            context.pseudonym("record_id", [version, identity])}


def _position(value):
    if value is None:
        return None
    if type(value) is not int or value < 1:
        raise ValueError("diagnostic row and line locations must be positive integers")
    return value


def safe_diagnostic(value, *, mode="standard", record_id_mode=None, protection=None,
                    effect_on_capabilities=(), effect_on_run=None):
    """Sanitize an accepted message or exception before any output sink.

    Unknown exceptions are represented by a protected generic identity. Their
    text, arguments, traceback, class name, and custom attributes are not read.
    Paths are withheld in both modes. Severity and explicitly supplied effects
    survive; no capability is inferred from untrusted narrative text.
    """
    mode, record_id_mode = _policy(mode, record_id_mode)
    context = _protection(protection)
    role = field = key = row = line = None
    if type(value) is ValidationMessage:
        code, severity = _code(value.code), _severity(value.severity)
        role, field, key = value.file_role, value.field, value.record_key
        row, line = value.row_number, value.line_number
    elif type(value) in _EXCEPTION_TYPES:
        code, severity = _code(value.code), "error"
        if type(value) in (IngestionError, CanonicalValidationError):
            role, row, line = value.file_role, value.row_number, value.line_number
        elif type(value) is MappingError:
            row, line = value.row_number, value.line_number
        if type(value) is CanonicalValidationError:
            field, severity = value.field, _severity(value.severity)
            if value.record_key is not None:
                if type(value.record_key) is not str:
                    raise TypeError("exception record key must be a literal canonical string")
                key = RecordKey.parse(value.record_key)
    elif isinstance(value, BaseException):
        code, severity = "unregistered_exception", "fatal"
    else:
        raise TypeError("diagnostics require a validation message or exception")
    if effect_on_run is None:
        effect_on_run = "failed" if severity == "fatal" else "partial" if severity == "error" else None
    if effect_on_run is not None and (type(effect_on_run) is not str or effect_on_run not in ("partial", "failed")):
        raise ValueError("diagnostic run effect must be partial or failed")
    if severity in ("info", "warning") and effect_on_run is not None:
        raise ValueError("non-error diagnostics cannot declare a failed run effect")
    if severity == "fatal" and effect_on_run != "failed":
        raise ValueError("fatal diagnostics must retain a failed run effect")
    return {
        "code": safe_code(code, severity, protection=context), "severity": severity,
        "message": safe_diagnostic_text(code, severity), "file_role": safe_role(role),
        "field": safe_field(field),
        "record_key": safe_record_key(key, mode=mode, record_id_mode=record_id_mode, protection=context),
        "row_number": _position(row), "line_number": _position(line),
        "effect_on_run": effect_on_run,
        "effect_on_capabilities": safe_effects(effect_on_capabilities),
        "remediation": safe_remediation(code),
    }


def format_diagnostic(value, *, mode="standard", record_id_mode=None, protection=None,
                      effect_on_capabilities=(), effect_on_run=None):
    """Return one ASCII-safe JSON line, without a traceback or free-text dump."""
    payload = safe_diagnostic(value, mode=mode, record_id_mode=record_id_mode,
                              protection=protection, effect_on_capabilities=effect_on_capabilities,
                              effect_on_run=effect_on_run)
    return json.dumps(payload, ensure_ascii=True, allow_nan=False, separators=(",", ":")) + "\n"


def emit_diagnostic(value, *, stream, mode="standard", record_id_mode=None, protection=None,
                    effect_on_capabilities=(), effect_on_run=None):
    """Write sanitized text only to the explicitly supplied caller-owned sink."""
    text = format_diagnostic(value, mode=mode, record_id_mode=record_id_mode,
                             protection=protection, effect_on_capabilities=effect_on_capabilities,
                             effect_on_run=effect_on_run)
    stream.write(text)


# Phase 4 Step 6: these operational results do not modify canonical evidence.
_PUBLICATION_MESSAGES = {
    "E_OUTPUT_PATH_INVALID": "The output or input path declaration is not a supported local path.",
    "E_OUTPUT_INPUT_COLLISION": "The output location collides with a declared input.",
    "E_OUTPUT_EXISTS": "A required report target already exists; it was not replaced.",
    "E_OUTPUT_UNSAFE": "The output or input directory tree cannot be used safely.",
    "E_OUTPUT_IO": "The required report files could not both be published.",
    "E_OUTPUT_RENDER": "The safe report could not be validated and rendered.",
    "E_OUTPUT_INTERNAL": "An internal failure prevented complete report publication.",
    "E_OUTPUT_CLEANUP": "Report publication finished, but temporary cleanup is incomplete.",
}


def publication_diagnostic(result):
    """Return fixed operational text, never paths, OS errors or source content."""
    from .paths import PublicationResult

    if type(result) is not PublicationResult:
        raise TypeError("publication diagnostics require an accepted publication result")
    PublicationResult.__post_init__(result)
    complete = result.status == "complete"
    return {
        "status": result.status, "code": result.code, "exit_code": result.exit_code,
        "severity": "info" if complete else "fatal" if result.exit_code == 4 else "error",
        "message": "Both required reports were published." if complete else _PUBLICATION_MESSAGES[result.code],
        "published_files": list(result.published_files),
        "residual_files": list(result.residual_files),
        "temporary_cleanup_complete": result.temporary_cleanup_complete,
        "remediation": [] if complete else [
            "Inspect the explicitly selected local directory and any disclosed residual outputs; "
            "use a safe unused destination before retrying."
        ],
    }


def format_publication_diagnostic(result):
    """Format one safe JSON line for either standard or redacted callers."""
    return json.dumps(publication_diagnostic(result), ensure_ascii=True,
                      allow_nan=False, separators=(",", ":")) + "\n"


def emit_publication_diagnostic(result, *, stream):
    """Write only to an explicit caller-owned sink; never configure a logger."""
    stream.write(format_publication_diagnostic(result))
