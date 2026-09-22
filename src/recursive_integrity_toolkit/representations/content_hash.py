"""Represent exact decoded record form under the approved UTF-8 profile.

Owner IDs:
    PR-006; T1 record-form input basis; PR-016 deterministic ordering.

Inputs:
    Canonical rows, one explicit version, representation identity and content mode.
    LOCAL_REF additionally requires caller-supplied safely loaded text by RecordKey.

Outputs:
    Immutable exact-content representation, hidden byte snapshots, and named scope.

Assumptions:
    exact_utf8_v1 encodes validated text unchanged. Supplied local-reference payload
    provenance is the caller's responsibility; no in-memory type certifies origin.

Limits:
    No I/O, path resolution, callback, semantic inference, near-duplicate method,
    frequency, support metric, diversity, cross-version pooling or report generation.
    Hashes describe record form, not authorship, independent origin or semantics.

Current phase status:
    Phase 3 Step 3 exact record-form states only; no later analytical families.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType

from ..errors import ErrorCode
from ..models import (
    CalculationReason, CalculationScope, CalculationStatus, CanonicalRow, ContentMode,
    RecordKey, RecordStateAssignment, RepresentationDescriptor, ValidationCoverage,
)
from ..utils.hashing import sha256_bytes
from .base import (
    RepresentationResult, RepresentationSelection, _literal_text,
    _representation_error, _selected_records,
)


@dataclass(frozen=True, slots=True)
class ExactContentRepresentation:
    """Private byte snapshots support equality verification, never provenance proof."""

    representation: RepresentationResult
    content_mode: ContentMode
    normalized_content: tuple[tuple[RecordKey, bytes], ...] = field(repr=False)


def exact_content_bytes(text: str, *, normalization_profile: str) -> bytes:
    """Validate and encode without transforming any valid code point or newline."""
    if type(normalization_profile) is not str or normalization_profile != "exact_utf8_v1":
        raise _representation_error(ErrorCode.CONFIG_INVALID, "unsupported exact-content profile")
    if type(text) is not str or "\x00" in text:
        raise _representation_error(ErrorCode.SCHEMA_TYPE, "content must be literal Unicode text without NUL")
    if not text.strip():
        raise _representation_error(ErrorCode.RECORD_EMPTY_CONTENT, "content cannot be empty or whitespace-only")
    try:
        return text.encode("utf-8")
    except UnicodeEncodeError:
        raise _representation_error(ErrorCode.SCHEMA_TYPE, "content must be encodable as UTF-8") from None


def _payload_snapshot(resolved_content, selected, content_mode: ContentMode) -> dict[RecordKey, str]:
    if type(content_mode) is not ContentMode:
        raise _representation_error(ErrorCode.CONFIG_INVALID, "content mode must be explicitly declared")
    if content_mode is ContentMode.INLINE:
        if resolved_content is not None:
            raise _representation_error(ErrorCode.CONFIG_INVALID, "inline content cannot be replaced by external payloads")
        return {}
    if resolved_content is None:
        raise _representation_error(ErrorCode.CONTENT_REF_MISSING, "LOCAL_REF requires explicitly supplied loaded text")
    if type(resolved_content) not in (dict, MappingProxyType):
        raise _representation_error(ErrorCode.SCHEMA_TYPE, "resolved content must be a plain canonical-key mapping")
    payloads = {}
    for key, value in resolved_content.items():
        if (type(key) is not RecordKey or type(key.dataset_version) is not str
                or type(key.record_id) is not str or type(value) is not str):
            raise _representation_error(ErrorCode.SCHEMA_TYPE, "resolved content requires canonical keys and literal text")
        payloads[key] = value
    selected_keys = {key for key, _, _ in selected}
    if set(payloads) - selected_keys:
        raise _representation_error(ErrorCode.CONFIG_INVALID, "resolved content includes identities outside the selected scope")
    if selected_keys - set(payloads):
        raise _representation_error(ErrorCode.CONTENT_REF_MISSING, "selected content payload is unavailable")
    return payloads


def assign_content_states(
    records: tuple[CanonicalRow, ...], *, dataset_versions: tuple[str, ...], scope_id: str,
    representation_name: str, representation_version: str, normalization_profile: str,
    content_mode: ContentMode, resolved_content: dict[RecordKey, str] | None = None,
) -> ExactContentRepresentation:
    """Assign exact states without reading paths or pooling versions.

    LOCAL_REF consumes only supplied text, never its path-valued canonical cell.
    A collision of one digest with different bytes blocks the entire operation.
    Empty input retains an explicit unavailable reason, with no invented state.
    """
    if type(dataset_versions) is not tuple or len(dataset_versions) != 1:
        raise _representation_error(ErrorCode.CONFIG_INVALID, "exact-content analysis requires one selected version")
    for value in (scope_id, representation_name, representation_version):
        if not _literal_text(value):
            raise _representation_error(ErrorCode.CONFIG_INVALID, "exact-content identity declarations must be complete")
    if type(normalization_profile) is not str or normalization_profile != "exact_utf8_v1":
        raise _representation_error(ErrorCode.CONFIG_INVALID, "unsupported exact-content profile")
    selected = _selected_records(records, dataset_versions)
    payloads = _payload_snapshot(resolved_content, selected, content_mode)
    descriptor = RepresentationDescriptor(
        representation_name, "content_hash", representation_version, "utf8_identity_then_sha256",
        field_name="content", missing_value_policy="error", normalization_profile=normalization_profile,
    )
    assignments, snapshots, keys, states = [], [], [], []
    seen_bytes = {}
    for key, values, location in selected:
        text = values["content"] if content_mode is ContentMode.INLINE else payloads[key]
        raw = exact_content_bytes(text, normalization_profile=normalization_profile)
        digest = sha256_bytes(raw)
        if digest in seen_bytes and seen_bytes[digest] != raw:
            raise _representation_error(ErrorCode.SCHEMA_TYPE, "equal content digests have unequal bytes",
                                        field_name="content", key=key, location=location)
        seen_bytes[digest] = raw
        assignments.append(RecordStateAssignment(key, digest))
        snapshots.append((key, raw))
        keys.append(key)
        states.append((key, "value"))
    scope = CalculationScope(dataset_versions, tuple(keys), (), "included_representation_records", scope_id)
    result = RepresentationResult(
        RepresentationSelection(descriptor, "explicit_content_configuration", ("content",)),
        scope, tuple(assignments), tuple(states),
        ValidationCoverage(len(keys), len(keys), "selected_valid_records"),
        CalculationStatus.AVAILABLE if keys else CalculationStatus.UNAVAILABLE,
        () if keys else (CalculationReason.EMPTY_SCOPE,),
        ("Exact decoded record form does not establish semantic identity or independent origin.",
         "LOCAL_REF text is supplied explicitly; no source path is read or hashed in that mode.",
         "No frequency, diversity or semantic-support metric is calculated."),
    )
    return ExactContentRepresentation(result, content_mode, tuple(snapshots))
