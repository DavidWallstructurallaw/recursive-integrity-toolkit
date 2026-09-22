"""Assign literal topic or label states under an explicitly selected scope.

Owner IDs:
    T1 input basis; PR-011 representation selection; PR-016 stable presentation.

Inputs:
    Canonical rows, explicit selected versions, a scope ID and field declarations.

Outputs:
    RepresentationResult with detached assignments, exclusions, field states,
    selection warnings and named coverage. No metric or hash result.

Assumptions:
    Mapping and null-token handling have already run. Empty and whitespace-only
    strings that survive normalization are literal states; unknown is literal too.
    Optional fallback uses field presence in the selected scope, then topic before
    label. Missing cells do not trigger per-record fallback or change the taxonomy.

Limits:
    No frequency, diversity, support, tail, content hashing, embeddings, semantic
    inference, file/network access, arbitrary callbacks or Phase 4 orchestration.
    A configuration error never falls back silently. No invented taxonomy version.

Current phase status:
    Phase 3 Step 2 pure field representations and missing-state handling.
"""

from __future__ import annotations

from ..config import RepresentationConfig
from ..errors import ErrorCode, WarningCode
from ..models import (
    CalculationReason, CalculationScope, CalculationStatus, CanonicalRow, RecordKey,
    RecordStateAssignment, RepresentationDescriptor, ValidationCoverage,
    ValidationMessage, ValidationSeverity,
)
from .base import (
    RepresentationResult, RepresentationSelection, _literal_text,
    _representation_error, _selected_records,
)


def _selection(
    selected, config: RepresentationConfig | None, allow_fallback: bool,
    fallback_version: str | None, fallback_missing_policy: str | None,
    missing_state_id: str | None,
) -> RepresentationSelection:
    if type(allow_fallback) is not bool:
        raise _representation_error(ErrorCode.CONFIG_INVALID, "fallback activation must be an explicit boolean")
    for value in (fallback_version, fallback_missing_policy, missing_state_id):
        if value is not None and not _literal_text(value):
            raise _representation_error(ErrorCode.CONFIG_INVALID, "representation options require literal nonempty text")
    messages = ()
    if config is not None:
        if type(config) is not RepresentationConfig:
            raise _representation_error(ErrorCode.CONFIG_INVALID, "configuration must use RepresentationConfig")
        for value in (config.name, config.source, config.field, config.version, config.missing_value_policy):
            if not _literal_text(value):
                raise _representation_error(ErrorCode.CONFIG_INVALID, "field representation declarations must be complete")
        if config.normalization_profile is not None:
            raise _representation_error(ErrorCode.CONFIG_INVALID, "field representations do not apply content profiles")
        if config.source not in ("topic_field", "label_field"):
            raise _representation_error(ErrorCode.CONFIG_INVALID, "representation source is outside the field-only step")
        if config.field not in ("topic", "label"):
            raise _representation_error(ErrorCode.CONFIG_INVALID, "this step supports canonical topic or label fields")
        chosen, source, name, version, policy = (
            config.field, config.source, config.name, config.version, config.missing_value_policy,
        )
        basis, considered = "explicit_configuration", (chosen,)
    else:
        if not allow_fallback:
            raise _representation_error(ErrorCode.CONFIG_INVALID, "supply explicit configuration or request field fallback")
        if not _literal_text(fallback_version) or not _literal_text(fallback_missing_policy):
            raise _representation_error(ErrorCode.CONFIG_INVALID, "fallback requires a declared version and missing policy")
        chosen = None
        considered = ("topic", "label")
        for candidate in considered:
            if any(candidate in values for _, values, _ in selected):
                chosen = candidate
                break
        if chosen is None:
            raise _representation_error(ErrorCode.SCHEMA_REQUIRED_FIELD, "no supported field representation is present")
        considered = ("topic",) if chosen == "topic" else ("topic", "label")
        source = "topic_field" if chosen == "topic" else "label_field"
        name, version, policy = chosen, fallback_version, fallback_missing_policy
        basis = "fallback_topic" if chosen == "topic" else "fallback_label"
        messages = (ValidationMessage(
            WarningCode.REPRESENTATION_FALLBACK.value, ValidationSeverity.WARNING,
            "explicitly requested field selection used the approved priority order", field=chosen,
        ),)
    if policy not in ("error", "exclude", "explicit_missing_state"):
        raise _representation_error(ErrorCode.CONFIG_INVALID, "unsupported representation missing policy")
    if (policy == "explicit_missing_state") != (missing_state_id is not None):
        raise _representation_error(ErrorCode.CONFIG_INVALID, "missing-state ID must match its explicit policy")
    if selected and not any(chosen in values for _, values, _ in selected):
        raise _representation_error(ErrorCode.SCHEMA_REQUIRED_FIELD, "configured field does not exist in the selected scope",
                                    field_name=chosen)
    descriptor = RepresentationDescriptor(
        name, source, version, "literal_field_value", field_name=chosen,
        missing_value_policy=policy, missing_state_id=missing_state_id,
    )
    return RepresentationSelection(descriptor, basis, considered, messages)


def select_field_representation(
    records: tuple[CanonicalRow, ...], *, dataset_versions: tuple[str, ...],
    config: RepresentationConfig | None = None, allow_fallback: bool = False,
    fallback_version: str | None = None, fallback_missing_policy: str | None = None,
    missing_state_id: str | None = None,
) -> RepresentationSelection:
    """Select metadata only. An explicit config takes precedence over fallback."""
    selected = _selected_records(records, dataset_versions)
    return _selection(selected, config, allow_fallback, fallback_version,
                      fallback_missing_policy, missing_state_id)


def assign_field_states(
    records: tuple[CanonicalRow, ...], *, dataset_versions: tuple[str, ...],
    scope_id: str, config: RepresentationConfig | None = None,
    allow_fallback: bool = False, fallback_version: str | None = None,
    fallback_missing_policy: str | None = None, missing_state_id: str | None = None,
) -> RepresentationResult:
    """Assign each selected record once, retaining every exclusion and input state.

    Explicitly empty input may return EMPTY_SCOPE with complete configuration.
    An entirely absent configured column is a schema error for nonempty input.
    A present column containing only nulls can produce ALL_EXCLUDED. No record is
    dropped from the caller's data and no missing value becomes inferred evidence.
    """
    if not _literal_text(scope_id):
        raise _representation_error(ErrorCode.CONFIG_INVALID, "scope_id must be explicit nonempty text")
    selected = _selected_records(records, dataset_versions)
    selection = _selection(selected, config, allow_fallback, fallback_version,
                           fallback_missing_policy, missing_state_id)
    descriptor = selection.descriptor
    chosen = descriptor.field_name
    for key, values, location in selected:
        value = values.get(chosen)
        if value is not None:
            if type(value) is not str or "\x00" in value:
                raise _representation_error(ErrorCode.SCHEMA_TYPE, "state values must be literal text or null",
                                            field_name=chosen, key=key, location=location)
            try:
                value.encode("utf-8")
            except UnicodeEncodeError:
                raise _representation_error(ErrorCode.SCHEMA_TYPE, "state value is not valid Unicode text",
                                            field_name=chosen, key=key, location=location) from None
            if missing_state_id is not None and value == missing_state_id:
                raise _representation_error(ErrorCode.CONFIG_INVALID, "missing-state ID collides with an observed value",
                                            field_name=chosen, key=key, location=location)
    assignments, states, included, excluded = [], [], [], []
    for key, values, location in selected:
        input_state = "absent" if chosen not in values else "null" if values[chosen] is None else "value"
        states.append((key, input_state))
        if input_state != "value":
            if descriptor.missing_value_policy == "error":
                raise _representation_error(ErrorCode.SCHEMA_REQUIRED_FIELD, "missing state blocks this representation",
                                            field_name=chosen, key=key, location=location)
            if descriptor.missing_value_policy == "exclude":
                assignments.append(RecordStateAssignment(key, None, CalculationReason.REPRESENTATION_MISSING))
                excluded.append(key)
                continue
            value = missing_state_id
        else:
            value = values[chosen]
        assignments.append(RecordStateAssignment(key, value))
        included.append(key)
    scope = CalculationScope(
        tuple(sorted(dataset_versions)), tuple(included), tuple(excluded),
        "included_representation_records", scope_id,
    )
    reason = CalculationReason.EMPTY_SCOPE if not selected else CalculationReason.ALL_EXCLUDED if not included else None
    return RepresentationResult(
        selection, scope, tuple(assignments), tuple(states),
        ValidationCoverage(len(included), len(selected), "selected_valid_records"),
        CalculationStatus.UNAVAILABLE if reason is not None else CalculationStatus.AVAILABLE,
        (reason,) if reason is not None else (),
    )
