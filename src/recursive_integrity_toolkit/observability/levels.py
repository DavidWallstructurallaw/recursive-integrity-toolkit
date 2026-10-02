"""Classify input observability and independent capability eligibility.

Owner IDs:
    PR-010, PR-011; PR-004, PR-007 and PR-008 validation bases are reused.

Inputs:
    Canonical records, typed provenance, explicit representation and chronology,
    optional already-read local text, and explicitly declared scenario parameters.

Outputs:
    ObservabilityAssessment with seven capabilities, named coverage, requirements,
    reason codes and retained validation diagnostics.

Assumptions:
    Ingestion and normalization precede this call. Local text is explicitly
    supplied after PR-017 reading. Capability availability is input eligibility,
    not evidence that a metric is implemented or that an assertion is true.

Limits:
    No state assignment, content hashing, distribution estimation, metric,
    graph traversal, root tracing, simulation, report, or file/network IO.
    Lineage uses only the sufficient all-edges-earlier-version certificate.
    Scenario parameters are internal declarations, not a new config format.

Current phase status:
    Phase 2 Step 8 observability and capability classification only.
"""
from __future__ import annotations

import math
from types import MappingProxyType

from ..config import RepresentationConfig, ScenarioConfig
from ..errors import CanonicalValidationError, ErrorCode
from ..io.validation import (
    _checked_order, _parent_lookup, _resolve_parent_list, join_provenance,
    parse_parent_ids, validate_canonical_values, validate_unique_keys,
)
from ..models import (
    CanonicalRow, Capability, CapabilityKey, CapabilityStatus, ContentMode,
    ObservabilityAssessment, ParentResolutionStatus, ProvenanceAssessment,
    ProvenanceJoinResult, RecordKey, ScenarioParameters, ValidationCoverage,
    ValidationMessage, ValidationSeverity, VersionOrderResult,
)

REASON_CODES = frozenset({
    "R_INPUT_PARTIAL", "R_NO_ANALYZABLE_CONTENT", "R_CONTENT_REFERENCE_UNAVAILABLE",
    "R_REPRESENTATION_NOT_DECLARED", "R_REPRESENTATION_FIELD_MISSING",
    "R_REPRESENTATION_PARTIAL", "R_REPRESENTATION_VALIDATION_DEFERRED",
    "R_REPRESENTATION_INCOMPATIBLE", "R_REPRESENTATION_MAPPING_DEFERRED",
    "R_SEMANTIC_EVIDENCE_MISSING", "R_PROVENANCE_NOT_SUPPLIED",
    "R_NO_VALID_PROVENANCE_ROW", "R_PROVENANCE_PARTIAL", "R_GROUNDING_UNKNOWN",
    "R_NO_PARENT_PATH", "R_PARENT_UNRESOLVED", "R_PARENT_AMBIGUOUS", "R_PARENT_INVALID",
    "R_PARENT_DECLARATION_MISSING", "R_GRAPH_VALIDATION_DEFERRED",
    "R_ROOT_GROUNDING_UNAVAILABLE", "R_VERSION_ORDER_MISSING", "R_SINGLE_VERSION",
    "R_MODEL_EVIDENCE_MISSING", "R_MODEL_EVIDENCE_VALIDATION_DEFERRED",
    "R_SCENARIO_NOT_CONFIGURED", "R_SCENARIO_PARAMETERS_MISSING",
    "R_SCENARIO_PARAMETERS_INVALID", "R_SCENARIO_DISTRIBUTION_MISSING",
    "R_SCENARIO_EXECUTION_DEFERRED",
})
_INPUT_NOTE = "Input eligibility only; downstream analytical implementations remain deferred."


def _invalid(message: str) -> CanonicalValidationError:
    return CanonicalValidationError(ErrorCode.CONFIG_INVALID, message)


def _cap(status: CapabilityStatus, coverage: ValidationCoverage | None = None, *,
         reasons: tuple[str, ...] = (), met: tuple[str, ...] = (),
         missing: tuple[str, ...] = (), notes: tuple[str, ...] = (),
         details: dict[str, ValidationCoverage] | None = None) -> Capability:
    if set(reasons) - REASON_CODES:
        raise _invalid("classification used an unregistered reason code")
    if status in (CapabilityStatus.PARTIAL, CapabilityStatus.UNAVAILABLE) and not reasons:
        raise _invalid("incomplete capabilities must state a reason")
    return Capability(status, coverage, tuple(sorted(set(met))), tuple(sorted(set(missing))),
                      tuple(sorted(set(reasons))), (_INPUT_NOTE,) + notes,
                      MappingProxyType(dict(details or {})))


def _row_key(row: CanonicalRow) -> RecordKey:
    return row.record_key


def _records(records: tuple[CanonicalRow, ...], mode: ContentMode) -> tuple[CanonicalRow, ...]:
    if type(mode) is not ContentMode:
        raise _invalid("content_mode must use ContentMode")
    if type(records) is not tuple or any(type(row) is not CanonicalRow or type(row.kind) is not str for row in records):
        raise _invalid("records must be an explicit tuple of canonical rows")
    validate_unique_keys(records, kind="records")
    if not records:
        raise CanonicalValidationError(ErrorCode.EMPTY_DATASET,
                                       "no valid records; no observability level can be certified")
    for row in records:
        if type(row.values) not in (dict, MappingProxyType):
            raise _invalid("canonical row values must be plain or read-only dictionaries")
        key = validate_canonical_values(dict(row.values), kind="records", location=row.location, content_mode=mode)
        if key != row.record_key:
            raise _invalid("record identity disagrees with canonical fields")
    return tuple(sorted(records, key=_row_key))


def _content_keys(records: tuple[CanonicalRow, ...], mode: ContentMode,
                  resolved_content: dict[RecordKey, str] | None) -> set[RecordKey]:
    keys = {row.record_key for row in records}
    if resolved_content is not None:
        if type(resolved_content) not in (dict, MappingProxyType):
            raise _invalid("resolved_content must map record keys to already-read text")
        for key, value in resolved_content.items():
            if type(key) is not RecordKey or key not in keys or type(value) is not str:
                raise _invalid("content-read evidence does not match the record scope")
            try:
                value.encode("utf-8")
            except UnicodeEncodeError:
                raise _invalid("content-read evidence must be valid UTF-8 text") from None
            if not value.strip() or "\x00" in value:
                raise _invalid("content-read evidence must be nonempty text without NUL")
        if mode is not ContentMode.LOCAL_REF:
            raise _invalid("resolved_content requires explicit local_ref mode")
    return keys if mode is ContentMode.INLINE else set(resolved_content or {})


def _representation(records: tuple[CanonicalRow, ...], rep: RepresentationConfig | None,
                    content: set[RecordKey]) -> tuple[set[RecordKey], bool, tuple[str, ...]]:
    """Validate declared source-field readiness without creating state labels."""
    if rep is None:
        return set(), False, ("R_REPRESENTATION_NOT_DECLARED",)
    if type(rep) is not RepresentationConfig:
        raise _invalid("representation must use RepresentationConfig")
    for value in (rep.name, rep.source, rep.field, rep.version, rep.missing_value_policy, rep.normalization_profile):
        if value is not None and (type(value) is not str or not value):
            raise _invalid("representation declarations must be nonempty literal strings")
    if rep.name is None or rep.source is None:
        raise _invalid("representation name and source must be explicit")
    if rep.missing_value_policy not in (None, "exclude", "error", "explicit_missing_state"):
        raise _invalid("representation missing-value policy is unsupported")
    if rep.source == "content_hash":
        if rep.normalization_profile != "exact_utf8_v1":
            return set(), False, ("R_REPRESENTATION_VALIDATION_DEFERRED",)
        return set(content), True, (() if len(content) == len(records) else ("R_CONTENT_REFERENCE_UNAVAILABLE",))
    if rep.source not in ("topic_field", "label_field"):
        return set(), False, ("R_REPRESENTATION_VALIDATION_DEFERRED",)
    if rep.field is None:
        raise _invalid("field representations require an explicit field")
    present: set[RecordKey] = set()
    found = False
    for row in records:
        found = found or rep.field in row.values
        value = row.values.get(rep.field)
        if value is not None and type(value) is not str:
            raise _invalid("representation field must contain strings or null")
        if type(value) is str and value != "":
            present.add(row.record_key)
    if len(present) == len(records):
        return present, True, ()
    reason = "R_REPRESENTATION_PARTIAL" if found else "R_REPRESENTATION_FIELD_MISSING"
    if rep.missing_value_policy == "error":
        return set(), True, (reason,)
    if rep.missing_value_policy == "explicit_missing_state":
        return present, False, (reason, "R_REPRESENTATION_VALIDATION_DEFERRED")
    return present, True, (reason,)


def _content_capability(records: tuple[CanonicalRow, ...], content: set[RecordKey], represented: set[RecordKey],
                        rep: RepresentationConfig | None, rep_reasons: tuple[str, ...], semantic_requested: bool) -> Capability:
    total = len(records)
    usable = content | represented
    semantic = rep is not None and rep.source in ("topic_field", "label_field")
    reasons = list(rep_reasons if rep is not None else ())
    if not usable:
        reasons.append("R_NO_ANALYZABLE_CONTENT")
    if len(usable) < total:
        reasons.append("R_CONTENT_REFERENCE_UNAVAILABLE")
    if semantic_requested and (not semantic or len(represented) < total):
        reasons.append("R_SEMANTIC_EVIDENCE_MISSING")
    status = CapabilityStatus.UNAVAILABLE if not usable else CapabilityStatus.PARTIAL if reasons else CapabilityStatus.AVAILABLE
    return _cap(status, ValidationCoverage(len(usable), total, "valid_records_in_requested_scope"),
                reasons=tuple(reasons), met=("content_or_declared_field_available",) if usable else (),
                missing=tuple(reasons), notes=("Raw content and exact record form do not certify semantic capability.",),
                details={"content": ValidationCoverage(len(content), total, "valid_records_in_requested_scope"),
                         "representation": ValidationCoverage(len(represented), total, "valid_records_in_requested_scope")})


def _provenance_capability(join: ProvenanceJoinResult) -> Capability:
    valid = join.provenance_required_field_coverage.numerator
    total = join.provenance_required_field_coverage.denominator
    reasons: list[str] = []
    if not join.provenance_supplied:
        reasons.append("R_PROVENANCE_NOT_SUPPLIED")
    if not valid:
        reasons.append("R_NO_VALID_PROVENANCE_ROW")
    elif valid < total or join.has_errors:
        reasons.append("R_PROVENANCE_PARTIAL")
    if valid and join.grounding_field_coverage.numerator < total:
        reasons.append("R_GROUNDING_UNKNOWN")
    status = CapabilityStatus.UNAVAILABLE if not valid else CapabilityStatus.PARTIAL if reasons else CapabilityStatus.AVAILABLE
    return _cap(status, join.provenance_required_field_coverage, reasons=tuple(reasons),
                met=("valid_matching_provenance",) if valid else (), missing=tuple(reasons),
                details={"row": join.provenance_row_coverage, "required_fields": join.provenance_required_field_coverage,
                         "grounding": join.grounding_field_coverage})


def _lineage_capability(join: ProvenanceJoinResult, order: VersionOrderResult) -> tuple[Capability, bool, tuple[ValidationMessage, ...]]:
    reasons: set[str] = set()
    messages: list[ValidationMessage] = []
    declared = resolved = earlier = 0
    complete = all_earlier = grounding_sufficient = True
    invalid = False
    lookup = _parent_lookup(join.scope_record_keys, order)
    for match in join.matches:
        row = match.provenance
        if row is None or not row.required_fields_valid:
            complete = False
            reasons.add("R_PROVENANCE_PARTIAL")
            continue
        raw = row.values.get("parent_ids")
        if raw is None:
            complete = False
            reasons.add("R_PARENT_DECLARATION_MISSING")
        if row.values["external_grounding"] == "unknown":
            grounding_sufficient = False
            reasons.add("R_GROUNDING_UNKNOWN")
        if raw is not None and not raw and row.values["external_grounding"] != "yes":
            grounding_sufficient = False
            reasons.add("R_ROOT_GROUNDING_UNAVAILABLE")
        declared += 0 if raw is None else len(raw)
        try:
            result = _resolve_parent_list(row.record_key, parse_parent_ids(raw), lookup,
                                          row.location, join.promoted_warning_codes)
        except CanonicalValidationError as exc:
            invalid = True
            reasons.add("R_PARENT_AMBIGUOUS" if exc.code is ErrorCode.PARENT_AMBIGUOUS else "R_PARENT_INVALID")
            messages.append(ValidationMessage(exc.code.value, ValidationSeverity.ERROR, exc.safe_message,
                row.location.file_role, "[redacted]", "parent_ids", row.record_key, row.location.row_number))
            continue
        messages.extend(result.messages)
        if result.graph_validation_deferred:
            all_earlier = False
            reasons.add("R_GRAPH_VALIDATION_DEFERRED")
        for ref in result.references:
            if ref.resolution_status is ParentResolutionStatus.RESOLVED:
                resolved += len(ref.source_references)
                if ref.temporal_status == "earlier_version":
                    earlier += len(ref.source_references)
                else:
                    all_earlier = False
                    reasons.add("R_GRAPH_VALIDATION_DEFERRED" if ref.temporal_status == "same_version" else "R_VERSION_ORDER_MISSING")
            else:
                complete = False
                reasons.add("R_PARENT_UNRESOLVED")
    if not resolved:
        reasons.add("R_NO_PARENT_PATH")
    parent_errors = any(message.severity in (ValidationSeverity.ERROR, ValidationSeverity.FATAL) for message in messages)
    certificate = bool(earlier and complete and all_earlier and not invalid and resolved == declared
                       and not parent_errors and not join.has_errors)
    ready = certificate and grounding_sufficient
    status = CapabilityStatus.AVAILABLE if ready else CapabilityStatus.PARTIAL if resolved and not invalid else CapabilityStatus.UNAVAILABLE
    if ready:
        reasons.clear()
    elif resolved and not reasons:
        reasons.add("R_PROVENANCE_PARTIAL")
    coverage = ValidationCoverage(resolved, declared, "declared_parent_reference_entries") if declared else None
    return (_cap(status, coverage, reasons=tuple(sorted(reasons)),
                 met=("earlier_version_acyclicity_certificate",) if certificate else (), missing=tuple(sorted(reasons)),
                 notes=("Reference-entry resolution coverage is not ancestry or external-root coverage.",
                        "General graph validation is deferred; no roots or ancestors are traced.")),
            certificate, tuple(messages))


def _compatibility(value: tuple[tuple[str, str], ...]) -> dict[str, str]:
    if type(value) is not tuple:
        raise _invalid("representation compatibility must use explicit string pairs")
    result: dict[str, str] = {}
    for pair in value:
        if (type(pair) is not tuple or len(pair) != 2
                or any(type(item) is not str or not item for item in pair) or pair[0] in result):
            raise _invalid("representation compatibility must use unique nonempty string pairs")
        result[pair[0]] = pair[1]
    return result


def _longitudinal_capability(records: tuple[CanonicalRow, ...], order: VersionOrderResult,
        rep: RepresentationConfig | None, represented: set[RecordKey], supported: bool,
        compatibility: tuple[tuple[str, str], ...], state_mapping_present: bool) -> Capability:
    versions = {row.record_key.dataset_version for row in records}
    labels = _compatibility(compatibility)
    reasons: list[str] = []
    if len(versions) < 2:
        reasons.append("R_SINGLE_VERSION")
    if not order.order:
        reasons.append("R_VERSION_ORDER_MISSING")
    if rep is None:
        reasons.append("R_REPRESENTATION_NOT_DECLARED")
    elif not supported:
        reasons.append("R_REPRESENTATION_VALIDATION_DEFERRED")
    elif labels:
        if not versions <= set(labels) or len({labels.get(version) for version in versions}) != 1:
            reasons.append("R_REPRESENTATION_INCOMPATIBLE")
        if rep.version is not None and any(labels.get(version) != rep.version for version in versions):
            reasons.append("R_REPRESENTATION_INCOMPATIBLE")
    elif rep.version is None and not (rep.source == "content_hash" and rep.normalization_profile == "exact_utf8_v1"):
        reasons.append("R_REPRESENTATION_INCOMPATIBLE")
    if state_mapping_present:
        reasons.append("R_REPRESENTATION_MAPPING_DEFERRED")
    if not versions <= {key.dataset_version for key in represented}:
        reasons.append("R_REPRESENTATION_FIELD_MISSING")
    ready = not reasons
    if ready and len(represented) < len(records):
        reasons.append("R_REPRESENTATION_PARTIAL")
    status = CapabilityStatus.UNAVAILABLE if not ready else CapabilityStatus.PARTIAL if reasons else CapabilityStatus.AVAILABLE
    return _cap(status, ValidationCoverage(len(represented), len(records), "valid_records_in_requested_scope"),
                reasons=tuple(reasons), met=("explicit_order_and_compatible_representation",) if ready else (),
                missing=tuple(reasons), notes=("No cross-version metric or state mapping executes here.",))


def _distribution(value: object) -> tuple[bool, frozenset[str]]:
    if type(value) is not tuple or not value:
        return False, frozenset()
    names: set[str] = set()
    masses: list[float] = []
    for pair in value:
        if type(pair) is not tuple or len(pair) != 2:
            return False, frozenset()
        name, mass = pair
        if type(name) is not str or not name or name in names or type(mass) not in (int, float):
            return False, frozenset()
        try:
            if not math.isfinite(mass) or not 0 <= mass <= 1:
                return False, frozenset()
        except OverflowError:
            return False, frozenset()
        names.add(name)
        masses.append(mass)
    return math.isclose(math.fsum(masses), 1.0, rel_tol=1e-12, abs_tol=1e-12), frozenset(names)


def _scenario_capability(scenario: ScenarioConfig | None, parameters: ScenarioParameters | None) -> Capability:
    if scenario is None:
        scenario = ScenarioConfig()
    if type(scenario) is not ScenarioConfig or type(scenario.enabled) is not bool:
        raise _invalid("scenario activation must use explicit ScenarioConfig")
    if not scenario.enabled:
        return _cap(CapabilityStatus.UNAVAILABLE, reasons=("R_SCENARIO_NOT_CONFIGURED",), missing=("explicit_scenario_activation",))
    reasons: list[str] = []
    if scenario.seed is None or parameters is None:
        reasons.append("R_SCENARIO_PARAMETERS_MISSING")
    if scenario.seed is not None and type(scenario.seed) is not int:
        reasons.append("R_SCENARIO_PARAMETERS_INVALID")
    if parameters is not None:
        if type(parameters) is not ScenarioParameters or type(parameters.model_name) is not str:
            raise _invalid("scenario parameters require ScenarioParameters with a literal model name")
        if parameters.model_name not in ("closed_resampling", "reopened_resampling"):
            reasons.append("R_SCENARIO_PARAMETERS_INVALID")
        for number, minimum in ((parameters.resample_size, 1), (parameters.simulation_horizon, 0), (parameters.simulation_replicates, 1)):
            if number is None:
                reasons.append("R_SCENARIO_PARAMETERS_MISSING")
            elif type(number) is not int or number < minimum:
                reasons.append("R_SCENARIO_PARAMETERS_INVALID")
        valid, names = _distribution(parameters.state_distribution)
        if parameters.state_distribution is None:
            reasons.append("R_SCENARIO_DISTRIBUTION_MISSING")
        elif not valid:
            reasons.append("R_SCENARIO_PARAMETERS_INVALID")
        if parameters.model_name == "reopened_resampling":
            external_valid, external_names = _distribution(parameters.external_input_distribution)
            if parameters.external_input_distribution is None:
                reasons.append("R_SCENARIO_DISTRIBUTION_MISSING")
            elif not external_valid or names != external_names:
                reasons.append("R_SCENARIO_PARAMETERS_INVALID")
            weight = parameters.reopening_weight
            if weight is None:
                reasons.append("R_SCENARIO_PARAMETERS_MISSING")
            elif type(weight) not in (int, float) or not 0 <= weight <= 1:
                reasons.append("R_SCENARIO_PARAMETERS_INVALID")
        elif parameters.external_input_distribution is not None or parameters.reopening_weight is not None:
            reasons.append("R_SCENARIO_PARAMETERS_INVALID")
    if reasons:
        return _cap(CapabilityStatus.UNAVAILABLE, reasons=tuple(reasons), missing=tuple(reasons))
    return _cap(CapabilityStatus.EXPERIMENTAL, reasons=("R_SCENARIO_EXECUTION_DEFERRED",),
                met=("explicit_configuration", "valid_parameters", "declared_distributions", "recorded_seed"),
                notes=("Experimental scenario eligibility only; no simulation has run.",))


def classify_observability(records: tuple[CanonicalRow, ...], *,
    provenance: tuple[CanonicalRow | ProvenanceAssessment, ...] | None = None,
    representation: RepresentationConfig | None = None,
    representation_compatibility: tuple[tuple[str, str], ...] = (),
    version_order: VersionOrderResult | None = None,
    content_mode: ContentMode = ContentMode.INLINE,
    resolved_content: dict[RecordKey, str] | None = None,
    semantic_requested: bool = False,
    requested_record_count: int | None = None,
    input_messages: tuple[ValidationMessage, ...] = (),
    model_evidence_present: bool = False,
    state_mapping_present: bool = False,
    scenario: ScenarioConfig | None = None,
    scenario_parameters: ScenarioParameters | None = None,
    strict_mode: bool = False,
    strict_warning_codes: tuple[str, ...] = (),
) -> ObservabilityAssessment:
    """Assess an explicit validation scope without loading data or running metrics.

    Local text is supplied after PR-017 validation. Presence of model evidence is
    insufficient to certify it; scenario enabled/seed alone never grants Level 5.
    Independent dataset evidence may grant Level 4 with partial lineage.
    """
    for value in (semantic_requested, model_evidence_present, state_mapping_present):
        if type(value) is not bool:
            raise _invalid("classification flags must be explicit booleans")
    checked = _records(records, content_mode)
    total = len(checked)
    if requested_record_count is not None and (type(requested_record_count) is not int or requested_record_count < total):
        raise _invalid("requested_record_count must include every supplied valid record")
    if type(input_messages) is not tuple or any(type(item) is not ValidationMessage
            or type(item.severity) is not ValidationSeverity or type(item.code) is not str
            or type(item.message) is not str for item in input_messages):
        raise _invalid("input diagnostics must use ValidationMessage objects")
    versions = tuple(sorted({row.record_key.dataset_version for row in checked}))
    order = _checked_order(version_order, versions)
    join = join_provenance(checked, provenance, strict_mode=strict_mode, strict_warning_codes=strict_warning_codes)
    content = _content_keys(checked, content_mode, resolved_content)
    represented, supported, rep_reasons = _representation(checked, representation, content)
    partial = (requested_record_count is not None and requested_record_count > total) or any(
        item.severity in (ValidationSeverity.ERROR, ValidationSeverity.FATAL) for item in input_messages)
    denominator = total if requested_record_count is None else requested_record_count
    ingestion = _cap(CapabilityStatus.PARTIAL if partial else CapabilityStatus.AVAILABLE,
        ValidationCoverage(total, denominator, "submitted_record_scope") if not partial or requested_record_count is not None else None,
        reasons=("R_INPUT_PARTIAL",) if partial else (), met=("valid_record_scope",),
        missing=("some_input_validation_failed",) if partial else ())
    content_cap = _content_capability(checked, content, represented, representation, rep_reasons, semantic_requested)
    provenance_cap = _provenance_capability(join)
    lineage_cap, path_certified, parent_messages = _lineage_capability(join, order)
    dataset_cap = _longitudinal_capability(checked, order, representation, represented, supported,
                                         representation_compatibility, state_mapping_present)
    model_cap = _cap(CapabilityStatus.UNAVAILABLE,
        reasons=("R_MODEL_EVIDENCE_VALIDATION_DEFERRED" if model_evidence_present else "R_MODEL_EVIDENCE_MISSING",),
        missing=("approved_model_performance_evidence",), notes=("Dataset versions do not establish model-performance change.",))
    scenario_cap = _scenario_capability(scenario, scenario_parameters)
    maximum = 0
    basis = ["validated_ingest_scope"]
    if content_cap.status is not CapabilityStatus.UNAVAILABLE:
        maximum = 1
        basis.append("content_or_declared_representation")
    if join.provenance_required_field_coverage.numerator:
        maximum = 2
        basis.append("valid_matching_provenance")
    if path_certified:
        maximum = 3
        basis.append("earlier_version_acyclicity_certificate")
    if dataset_cap.status in (CapabilityStatus.AVAILABLE, CapabilityStatus.PARTIAL):
        maximum = 4
        basis.append("ordered_compatible_dataset_versions")
    if scenario_cap.status is CapabilityStatus.EXPERIMENTAL:
        maximum = 5
        basis.append("valid_experimental_scenario_declaration")
    matrix = dict(zip(CapabilityKey, (ingestion, content_cap, provenance_cap, lineage_cap, dataset_cap, model_cap, scenario_cap)))
    limitations = tuple(sorted({reason for capability in matrix.values() for reason in capability.reason_codes}))
    return ObservabilityAssessment(maximum, MappingProxyType(matrix), tuple(basis), limitations,
                                   input_messages + join.messages + order.messages + parent_messages)
