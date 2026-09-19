"""Explicit, in-memory adapters for accepted validation and calculation evidence.

Owner IDs: PR-012, PR-014, PR-015, PR-016, PR-018; each public field retains its registered owner.
Theory Map IDs: inherited through the frozen public field registry.
Inputs: already validated BundleValidationResult and explicitly supplied Phase 3 results.
Outputs: immutable CanonicalReport and explicitly selected SafeReportView.
Assumptions: supplied typed results are evidence handoffs, not authenticity certificates.
Limits: no ingestion, classification, metric execution, graph traversal, simulation,
        filesystem access, rendering or CLI orchestration.
Current phase status: Phase 4 Step 4 additive privacy views and explicit run metadata.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, isclose
from types import MappingProxyType
from pathlib import PosixPath, WindowsPath

from ..models import (
    BundleValidationResult, CalculationEvidenceClass, CalculationMetadata,
    CalculationReason, CalculationScope, CalculationStatus, CapabilityKey,
    CanonicalRow, NumericalPolicy, RecordKey, RepresentationDescriptor,
    ScalarCalculation, ValidationCoverage, ValidationMessage, ValidationSeverity,
    WeightingOptions, Capability, CapabilityStatus, ObservabilityAssessment, FileInventoryEntry,
    FileRole, FileFormat, VersionOrderResult, ProvenanceJoinResult, ProvenanceMatch, ProvenanceAssessment,
    ExplicitPairContext, RowMappingEvidence, RowLocation, GenerationValidationResult, RecordStateAssignment, TailSelectionOptions,
)
from ..metrics.bounds import DirectClosureExposureBounds
from ..metrics.diversity import DistributionMetrics, StateDistributionResult, SupportComparison, StateFrequency
from ..metrics.duplicates import ExactDuplicateResult, ExactDuplicateGroup
from ..metrics.provenance import ProvenanceCompositionResult, DeclaredComposition, WeightedSourceComposition, DirectGroundingBasis, DirectGroundingAssignment
from ..metrics.resampling import ExpectedDiversityResult, ResamplingSimulation, ResamplingInput, ResamplingReplicate, SampledGeneration
from ..metrics.tail import TailSelectionResult, ExtinctionProbabilityResult, RarityEntry
from ..representations.compatibility import RepresentationCompatibility, StateMappingDeclaration
from ..result import CanonicalReport, FIELD_REGISTRY, LEVEL_LABELS, SECTION_ORDER, ReportValidationError


class ReportAssemblyError(ReportValidationError):
    """A supplied handoff cannot be represented without overstating its evidence."""


@dataclass(frozen=True, slots=True)
class FamilyFailure:
    """An explicit family failure, kept alongside independently usable evidence."""

    capability: CapabilityKey
    messages: tuple[ValidationMessage, ...]

    def __post_init__(self):
        if type(self.capability) is not CapabilityKey or type(self.messages) is not tuple:
            raise ReportAssemblyError("family failure requires typed capability and immutable messages")
        if not self.messages or any(type(item) is not ValidationMessage or item.severity not in
                                   (ValidationSeverity.ERROR, ValidationSeverity.FATAL) for item in self.messages):
            raise ReportAssemblyError("family failure must retain error or fatal diagnostics")


def _require(condition, message):
    if not condition:
        raise ReportAssemblyError(message)


def _typed(value, expected, name):
    _require(type(value) is expected, name + " requires its exact accepted result type")


def _number(value, name, *, integer=False, minimum=None, maximum=None):
    _require(type(value) is int if integer else type(value) in (int, float), name + " must be a built-in number")
    try:
        finite = isfinite(value)
    except OverflowError:
        finite = False
    _require(finite, name + " must be finite")
    _require(minimum is None or value >= minimum, name + " is below its accepted bound")
    _require(maximum is None or value <= maximum, name + " is above its accepted bound")


def _key(value):
    _typed(value, RecordKey, "record identity")
    return {"dataset_version": value.dataset_version, "record_id": value.record_id}


def _scope(value, bundle):
    _typed(value, CalculationScope, "calculation scope")
    CalculationScope(value.dataset_versions, value.included_record_keys, value.excluded_record_keys,
                     value.denominator_basis, value.scope_id)
    if bundle is not None:
        actual = {row.record_key for row in bundle.records}
        _require(set(value.included_record_keys + value.excluded_record_keys) <= actual,
                 "calculation scope contains records outside the validated bundle")
        _require(set(value.dataset_versions) <= set(bundle.version_order.loaded_versions),
                 "calculation scope names unloaded versions")
    return {"dataset_versions": list(value.dataset_versions),
            "record_count": len(value.included_record_keys),
            "excluded_record_count": len(value.excluded_record_keys),
            "denominator_basis": value.denominator_basis, "scope_id": value.scope_id,
            "included_record_keys": [_key(item) for item in value.included_record_keys],
            "excluded_record_keys": [_key(item) for item in value.excluded_record_keys]}


def _bundle_scope(bundle):
    return {"dataset_versions": list(bundle.version_order.loaded_versions),
            "record_count": len(bundle.records), "excluded_record_count": 0,
            "denominator_basis": "all_validated_bundle_records", "scope_id": "validated_bundle",
            "included_record_keys": [_key(row.record_key) for row in bundle.records],
            "excluded_record_keys": []}


def _representation(value):
    if value is None:
        return None
    _typed(value, RepresentationDescriptor, "representation")
    RepresentationDescriptor(value.representation_name, value.representation_source,
        value.representation_version, value.binning_or_mapping_rule, value.field_name,
        value.missing_value_policy, value.missing_state_id, value.normalization_profile)
    return {"representation_name": value.representation_name,
            "representation_source": value.representation_source,
            "representation_version": value.representation_version,
            "binning_or_mapping_rule": value.binning_or_mapping_rule,
            "field_name": value.field_name, "missing_value_policy": value.missing_value_policy,
            "missing_state_id": value.missing_state_id, "normalization_profile": value.normalization_profile}


def _coverage(value):
    _typed(value, ValidationCoverage, "coverage")
    _number(value.numerator, "coverage numerator", integer=True, minimum=0)
    _number(value.denominator, "coverage denominator", integer=True, minimum=0)
    _require(value.numerator <= value.denominator, "coverage numerator exceeds denominator")
    return {"numerator": value.numerator, "denominator": value.denominator,
            "denominator_name": value.denominator_name, "ratio": value.ratio,
            "reason": "empty_scope" if value.denominator == 0 else None}


def _policy(value):
    _typed(value, NumericalPolicy, "numerical policy")
    NumericalPolicy(value.absolute_tolerance, value.relative_tolerance, value.probability_mass_tolerance)
    return {"absolute_tolerance": value.absolute_tolerance, "relative_tolerance": value.relative_tolerance,
            "probability_mass_tolerance": value.probability_mass_tolerance}


def _definition(path):
    for definition in FIELD_REGISTRY:
        if definition.path == path:
            return definition
    raise ReportAssemblyError("adapter field is absent from the frozen registry")


def _base(path, scope, *, representation=None, coverage=None, denominator=None,
          assumptions=(), limitations=(), status="available", reasons=(), required=()):
    field = _definition(path)
    return {"unit": field.unit, "evidence_class": field.evidence_class,
            "status": status, "method_id": field.method_id, "owner_ids": [field.owner],
            "theory_map_ids": [], "trace_ids": [field.owner] if field.owner.startswith("T") else [],
            "scope": scope, "representation": representation,
            "coverage": coverage, "coverage_reason": "coverage_not_supplied_for_this_result" if coverage is None else None,
            "denominator": denominator, "denominator_reason": "denominator_not_applicable_or_unavailable" if denominator is None else None,
            "assumptions": list(dict.fromkeys(assumptions)), "limitations": list(dict.fromkeys(limitations)),
            "reason_codes": list(dict.fromkeys(reasons)), "required_evidence": list(dict.fromkeys(required))}


def _envelope(path, value, scope, **kwargs):
    return {"value": value, **_base(path, scope, **kwargs)}


def _metadata_text(value):
    """Validate owner-authored method text before preserving it in public output."""
    name = value.metric_name
    basis = ("empirical_assignments", "explicit_counts_divided_by_included_records", "weighted_record_mass", "explicit_probability_vector")
    methods = {
        "support_size": basis,
        "gini_simpson_diversity": basis,
        "simpson_concentration": basis,
        "state_frequency": basis + ("empirical_assignments; n_i/N",),
        "state_count": tuple("Definitions 7.1; " + item for item in basis) + ("count included record-state assignments",),
        "state_mass": ("Definitions 9.5; canonical record weights summed within each state",),
        "support_delta": ("later support_size minus earlier support_size",),
        "support_loss_count": ("cardinality of earlier support minus later support",),
        "support_added_count": ("cardinality of later support minus earlier support",),
        "support_retention_ratio": ("intersection support size / earlier positive-mass support size",),
        "gini_simpson_diversity_delta": ("later Gini-Simpson diversity minus earlier diversity",),
        "extinct_states": ("earlier support minus later support",),
        "added_states": ("later support minus earlier support",),
        "retained_states": ("earlier support intersect later support",),
        "source_type_counts": ("Definitions 3.3/11.1; count declared canonical categories",),
        "provenance_confidence_counts": ("Definitions 3.3/11.1; count declared canonical categories",),
        "source_type_shares": ("category count / all selected valid records",),
        "source_type_field_coverage": ("Definitions 3.13; nonmissing valid field / all selected valid records",),
        "provenance_confidence_field_coverage": ("Definitions 3.13; nonmissing valid field / all selected valid records",),
        "provenance_row_coverage": ("Reuse Phase 2 coverage; Definitions 3.10-3.12",),
        "provenance_required_field_coverage": ("Reuse Phase 2 coverage; Definitions 3.10-3.12",),
        "grounding_field_coverage": ("Reuse Phase 2 coverage; Definitions 3.10-3.12",),
        "analyzed_record_count": ("All selected valid records",),
        "records_with_matching_rows": ("Phase 2 matched-row inventory",),
        "missing_provenance_count": ("Phase 2 missing-row inventory",),
        "missing_provenance_share": ("Definitions 11.4; missing rows / all selected valid records",),
        "known_open_count": ("toolkit_operationalization; Definitions 3.7-3.9; P3-D08",),
        "known_closed_count": ("toolkit_operationalization; Definitions 3.7-3.9; P3-D08",),
        "unresolved_grounding_count": ("toolkit_operationalization; Definitions 3.7-3.9; P3-D08",),
        "weighted_source_type_masses": ("Definitions 19; sum explicit weights by source",),
        "weighted_source_type_shares": ("F-007 weighted variant; category mass / all selected record weight mass",),
        "total_weight": ("Definitions 19; all selected weights",),
        "missing_provenance_weight": ("Definitions 19; missing-row mass",),
        "weighted_missing_provenance_share": ("Definitions 11.4/19; missing-row mass / all selected record weight mass",),
        "duplicate_record_count": ("sum_group_size_minus_one; DEFINITIONS_AND_UNITS:8.3",),
        "duplicate_group_count": ("count_groups_of_size_greater_than_one; DEFINITIONS_AND_UNITS:8.4",),
        "rarity_rank": ("ascending frequency, then count, then Unicode state ID; 1-based ordinal",),
        "tail_support_size": tuple("Definitions 10.1-10.6; explicit " + rule for rule in ("singleton_count", "count_at_or_below", "frequency_at_or_below", "state_list")),
        "tail_membership": tuple("Definitions 10.1-10.6; explicit " + rule for rule in ("singleton_count", "count_at_or_below", "frequency_at_or_below", "state_list")),
        "tail_record_share": tuple("Definitions 10.1-10.6; explicit " + rule + "; selected counts / included records" for rule in ("singleton_count", "count_at_or_below", "frequency_at_or_below", "state_list")),
        "direct_closure_exposure_lower_bound": ("known_closed_count / total_record_count", "no usable required-provenance row"),
        "direct_closure_exposure_upper_bound": ("(known_closed_count + unresolved_grounding_count) / total_record_count", "no usable required-provenance row"),
        "direct_closure_exposure_interval_width": ("upper_bound - lower_bound = unresolved_grounding_count / total_record_count", "no usable required-provenance row"),
        "one_step_extinction_probability": ("F-014; (1-p_i)^n; analytic one-step closed multinomial",),
        "expected_gini_simpson_diversity": ("analytic_expectation; D0*(1-1/n)**t; t=0..steps; constant n",),
    }
    if value.evidence_class is CalculationEvidenceClass.SIMULATION and name in ("state_count", "state_frequency", "support_size", "gini_simpson_diversity"):
        allowed = ("sampled_path; sequential_binomial_complement_v1",)
    else:
        allowed = methods.get(name, ())
    _require(value.method in allowed, "method text differs from the accepted computation owner")
    _require(type(value.assumptions) is tuple and value.assumptions and all(type(item) is str and item for item in value.assumptions), "owner assumptions cannot be empty or malformed")
    _require(type(value.limitations) is tuple and value.limitations and all(type(item) is str and item for item in value.limitations), "owner limitations cannot be empty or malformed")
    pair_names = ("support_delta", "support_loss_count", "support_added_count", "support_retention_ratio",
                  "gini_simpson_diversity_delta", "extinct_states", "added_states", "retained_states")
    if value.evidence_class is CalculationEvidenceClass.SIMULATION and value.owner_id == "T1":
        assumptions = ("Fixed finite declared state space and constant positive integer resample size.",
                       "X_t conditional on p_t is Multinomial(n,p_t); p_(t+1)=X_t/n.",
                       "No mutation, migration, independent real data or external corrective input.")
        limitations = ("Experimental conditional simulation; no calibrated production-failure probability.",
                       "Diversity contraction holds in expectation, not monotonically on every sampled path.",
                       "Simulated steps are not record generations, training epochs or dataset releases.",
                       "No external-reference loss, reopening, lineage, risk score or audit workflow is implemented.",
                       "Floating-point and pseudorandom sampling are numerical realizations of the declared model.")
    elif value.owner_id == "T1" and name in pair_names:
        assumptions = ("Earlier and later scopes explicitly selected and independently validated.",
                       "State identity uses the declared common basis, including any disclosed map.")
        limitations = ("Observed/supplied support only; no permanent extinction or causal/model-performance verdict.",
                       "A coarsened comparison cannot recover distinctions lost through its mapping.")
    elif value.owner_id == "T1":
        assumptions = ("One explicitly selected version and declared representation.",
                       "No implicit pooling, probability repair, confidence weighting or sampling.")
        limitations = ("Representation-bound; does not establish functional failure or semantic completeness.",)
    elif value.owner_id == "T2":
        assumptions = (("Categorical multinomial sampling; positive explicit n; one-step horizon; no external reopening."
                        if value.evidence_class is CalculationEvidenceClass.SIMULATION else
                        "Explicit rule over positive observed unweighted count support."),)
        limitations = ("Representation-bound; no calibrated production-failure or universal risk conclusion.",)
    elif value.owner_id == "T3" and name.startswith("direct_closure_exposure_"):
        assumptions = ("Approved direct grounding partition; uncertainty remains unresolved.",)
        limitations = ("Toolkit operationalization relative to supplied metadata, without lineage or truth certification.",)
    elif value.owner_id == "PR-006":
        assumptions = ("exact_utf8_v1 and SHA-256; equal digests verified against exact bytes", "one explicitly selected version; unweighted records")
        limitations = ("Exact record form does not establish semantic identity or independent origin.",)
    else:
        assumptions = ("Exact explicit single-version Phase 2 join scope; no representation exclusions.",)
        limitations = ("Supplied declarations only; no truth or source-independence certification.",)
    _require(value.assumptions == assumptions and value.limitations == limitations,
             "required computation-owner assumptions or limitations were changed")



def _metadata(value, *, name, scope, representation, owner, evidence, unit, formula=None, weighting=None):
    _typed(value, CalculationMetadata, "calculation metadata")
    CalculationMetadata(value.metric_name, value.owner_id, value.formula_id, value.evidence_class, value.unit, value.method,
                        value.scope, value.representation, value.weighting, value.assumptions, value.limitations)
    _metadata_text(value)
    _require(value.metric_name == name and value.owner_id == owner and value.unit == unit,
             "calculation name, owner or unit differs from the accepted adapter")
    _require(value.evidence_class is evidence and value.formula_id == formula,
             "calculation evidence class or formula differs from the accepted adapter")
    _require(value.scope == scope and value.representation == representation,
             "calculation metadata is detached from its enclosing scope or representation")
    _typed(value.weighting, WeightingOptions, "weighting")
    WeightingOptions(value.weighting.weighting_mode, value.weighting.weight_field)
    expected_weighting = WeightingOptions() if weighting is None else weighting
    _require(value.weighting == expected_weighting, "calculation weighting differs from its enclosing result")
    _require(type(value.assumptions) is tuple and type(value.limitations) is tuple,
             "calculation assumptions and limitations must remain immutable")


def _scalar(path, value, scope, representation, bundle, *, name=None, denominator=None,
            coverage=None, weighting=None, limitations=(), formula=None):
    _typed(value, ScalarCalculation, "scalar calculation")
    field = _definition(path)
    _metadata(value.metadata, name=name or path.rsplit(".", 1)[-1], scope=scope,
              representation=representation, owner=field.owner,
              evidence=CalculationEvidenceClass(field.evidence_class), unit=field.unit,
              formula=field.method_id if field.method_id.startswith("F-") else formula, weighting=weighting)
    ScalarCalculation(value.metadata, value.status, value.value, value.reason_codes)
    result = _envelope(path, value.value, _scope(scope, bundle), representation=_representation(representation),
        denominator=denominator, coverage=coverage, assumptions=value.metadata.assumptions,
        limitations=value.metadata.limitations + tuple(limitations), status=value.status.value,
        reasons=tuple(reason.value for reason in value.reason_codes),
        required=("valid_nonempty_input_for_declared_scope",) if value.status is CalculationStatus.UNAVAILABLE else ())
    result["weighting"] = {"weighting_mode": value.metadata.weighting.weighting_mode,
                           "weight_field": value.metadata.weighting.weight_field}
    result["method"] = value.metadata.method
    return result


def _table(path, value, metadata, scope, representation, bundle, *, name, status, reasons=(),
           denominator=None, coverage=None, weighting=None, limitations=(), formula=None):
    field = _definition(path)
    _metadata(metadata, name=name, scope=scope, representation=representation, owner=field.owner,
              evidence=CalculationEvidenceClass(field.evidence_class), unit=field.unit,
              formula=field.method_id if field.method_id.startswith("F-") else formula, weighting=weighting)
    _require(type(status) is CalculationStatus, "table status requires CalculationStatus")
    _require(type(reasons) is tuple and all(type(reason) is CalculationReason for reason in reasons), "table reasons require the frozen reason registry")
    _require((status is CalculationStatus.UNAVAILABLE) == (value is None), "table missingness and status disagree")
    result = _envelope(path, value, _scope(scope, bundle), representation=_representation(representation),
        denominator=denominator, coverage=coverage, assumptions=metadata.assumptions,
        limitations=metadata.limitations + tuple(limitations), status=status.value,
        reasons=tuple(reason.value for reason in reasons),
        required=("valid_nonempty_input_for_declared_scope",) if status is CalculationStatus.UNAVAILABLE else ())
    result["weighting"] = {"weighting_mode": metadata.weighting.weighting_mode, "weight_field": metadata.weighting.weight_field}
    result["method"] = metadata.method
    return result


def _distribution(payload, value, bundle, *, weighted=False, coverage=None):
    _typed(value, DistributionMetrics, "distribution")
    if value.input_basis == "explicit_probability_vector":
        bundle = None
    scope = _scope(value.scope, bundle)
    _require(len(value.scope.dataset_versions) == 1, "versioned distribution requires one selected version")
    _typed(value.weighting, WeightingOptions, "distribution weighting")
    _require(value.weighting.weighting_mode == ("weighted" if weighted else "unweighted"), "distribution companion weighting mismatch")
    _require(value.analyzed_record_count == len(value.scope.included_record_keys), "analyzed count disagrees with scope")
    _require(type(value.status) is CalculationStatus and type(value.states) is tuple and type(value.support) is tuple,
             "distribution status and tables require their accepted types")
    _require(value.input_basis in ("empirical_assignments", "explicit_counts_divided_by_included_records", "weighted_record_mass", "explicit_probability_vector"), "unsupported distribution basis")
    _require(all(type(row) is StateFrequency for row in value.states), "state tables require exact StateFrequency entries")
    _require(all(type(row.state_id) is str for row in value.states), "state identifiers must be literal strings")
    _require(len({row.state_id for row in value.states}) == len(value.states), "duplicate state table identity")
    _require((value.input_basis == "weighted_record_mass") == weighted, "weighted distribution input basis disagrees with companion")
    if value.input_basis != "explicit_probability_vector":
        _require(value.count_metadata is not None, "count-backed distribution lacks count metadata")
    if not weighted:
        _require(value.mass_metadata is None, "unweighted distribution cannot claim weight masses")
    for row in value.states:
        _typed(row, StateFrequency, "state frequency")
        _number(row.state_frequency, "state frequency", minimum=0, maximum=1)
        if row.state_count is not None:
            _number(row.state_count, "state count", integer=True, minimum=0)
        if row.state_mass is not None:
            _number(row.state_mass, "state weight mass", minimum=0)
    if value.frequency_denominator is not None:
        _number(value.frequency_denominator, "frequency denominator", minimum=0)
    if value.input_basis in ("empirical_assignments", "explicit_counts_divided_by_included_records") and value.status is CalculationStatus.AVAILABLE:
        _require(value.frequency_denominator == len(value.scope.included_record_keys) and value.denominator_basis == value.scope.denominator_basis, "unweighted frequency denominator differs from declared record scope")
        _require(sum(row.state_count for row in value.states) == value.frequency_denominator, "state counts differ from supplied frequency denominator")
    if value.input_basis == "explicit_probability_vector":
        _require(value.frequency_denominator is None and value.denominator_basis == "explicit_probability_mass", "supplied probability denominator was altered")
    if weighted and value.status is CalculationStatus.AVAILABLE:
        _require(isclose(sum(row.state_mass for row in value.states), value.frequency_denominator, rel_tol=1e-12, abs_tol=1e-12) and value.denominator_basis == "included_record_weight_mass", "weighted mass denominator differs from supplied state mass")
    if value.status is CalculationStatus.AVAILABLE:
        _require(set(value.support) == {row.state_id for row in value.states if row.state_frequency > 0}, "support table disagrees with supplied positive frequencies")
        _require(value.support_size.value == len(value.support), "support size disagrees with supplied support identities")
    for scalar in (value.support_size, value.gini_simpson_diversity, value.simpson_concentration):
        _require(scalar.status is value.status and scalar.reason_codes == value.reason_codes,
                 "distribution scalar status disagrees with enclosing result")
    version = value.scope.dataset_versions[0]
    support = payload["derived_metrics"].setdefault("support", {}).setdefault("by_version", {}).setdefault(version, {})
    diversity = payload["derived_metrics"].setdefault("diversity", {}).setdefault("by_version", {}).setdefault(version, {})
    prefix = "weighted_" if weighted else ""
    _require(prefix + "support_size" not in support, "duplicate distribution for one version and weighting")
    for name, scalar, target, family in (
        ("support_size", value.support_size, support, "support"),
        ("gini_simpson_diversity", value.gini_simpson_diversity, diversity, "diversity"),
        ("simpson_concentration", value.simpson_concentration, diversity, "diversity")):
        target[prefix + name] = _scalar("derived_metrics." + family + ".by_version.*." + prefix + name,
            scalar, value.scope, value.representation, bundle, name=name,
            denominator=value.frequency_denominator, coverage=coverage, weighting=value.weighting, limitations=value.limitations)
        target[prefix + name]["input_basis"] = value.input_basis
    available = value.status is CalculationStatus.AVAILABLE
    if value.input_basis == "explicit_probability_vector":
        _require(not weighted and value.count_metadata is None and value.mass_metadata is None,
                 "supplied probabilities cannot become empirical counts or weighted mass")
        table = [{"state_id": row.state_id, "probability": row.state_frequency} for row in value.states] if available else None
        payload["observed_facts"].setdefault("supplied_state_probabilities", {}).setdefault("by_version", {})[version] = _table(
            "observed_facts.supplied_state_probabilities.by_version.*", table, value.frequency_metadata,
            value.scope, value.representation, bundle, name="state_frequency", status=value.status,
            reasons=value.reason_codes, denominator=None, coverage=coverage, weighting=value.weighting,
            limitations=value.limitations)
    else:
        table = [{"state_id": row.state_id, "state_frequency": row.state_frequency} for row in value.states] if available else None
        diversity[prefix + "state_frequencies"] = _table("derived_metrics.diversity.by_version.*." + prefix + "state_frequencies",
            table, value.frequency_metadata, value.scope, value.representation, bundle,
            name="state_frequency", status=value.status, reasons=value.reason_codes, denominator=value.frequency_denominator,
            coverage=coverage, weighting=value.weighting, limitations=value.limitations)
    if not weighted and value.count_metadata is not None:
        _require(all(row.state_count is not None for row in value.states), "count-backed distribution has missing counts")
        table = [{"state_id": row.state_id, "state_count": row.state_count} for row in value.states] if available else None
        payload["observed_facts"].setdefault("state_counts", {}).setdefault("by_version", {})[version] = _table(
            "observed_facts.state_counts.by_version.*", table, value.count_metadata, value.scope, value.representation,
            bundle, name="state_count", status=value.status, reasons=value.reason_codes,
            denominator=value.frequency_denominator, coverage=coverage, weighting=WeightingOptions())
    if weighted:
        _require(value.mass_metadata is not None, "weighted distribution lacks mass metadata")
        _require(all(row.state_mass is not None for row in value.states), "weighted distribution has missing masses")
        table = [{"state_id": row.state_id, "state_mass": row.state_mass} for row in value.states] if available else None
        diversity["weighted_state_masses"] = _table("derived_metrics.diversity.by_version.*.weighted_state_masses",
            table, value.mass_metadata, value.scope, value.representation, bundle, name="state_mass",
            status=value.status, reasons=value.reason_codes, denominator=value.frequency_denominator,
            coverage=coverage, weighting=value.weighting)
    else:
        basis = {"input_basis": value.input_basis, "analyzed_record_count": value.analyzed_record_count,
                 "frequency_denominator": value.frequency_denominator, "denominator_basis": value.denominator_basis,
                 "supplied_probability_total": value.supplied_probability_total, "probability_residual": value.probability_residual,
                 "numerical_policy": _policy(value.numerical_policy)}
        diversity["distribution_basis"] = _envelope("derived_metrics.diversity.by_version.*.distribution_basis", basis,
            scope, representation=_representation(value.representation), coverage=coverage,
            denominator=value.frequency_denominator, limitations=value.limitations)


def _distribution_exclusions(payload, value):
    """Retain owner-supplied exclusion reasons without selecting records again."""
    _require(type(value.excluded_assignments) is tuple and all(type(item) is RecordStateAssignment for item in value.excluded_assignments),
             "distribution exclusions require accepted immutable assignments")
    scope = value.unweighted.scope
    _require({item.record_key for item in value.excluded_assignments} == set(scope.excluded_record_keys) and
             len(value.excluded_assignments) == len(scope.excluded_record_keys), "exclusion inventory differs from calculation scope")
    exclusions = []
    for item in value.excluded_assignments:
        _require(item.state_id is None and type(item.exclusion_reason) is CalculationReason,
                 "excluded assignments must preserve their unavailable reason")
        exclusions.append({"record_key": _key(item.record_key), "reason_codes": [item.exclusion_reason.value]})
    version = scope.dataset_versions[0]
    for section, family in (("derived_metrics", "support"), ("derived_metrics", "diversity")):
        for envelope in payload[section].get(family, {}).get("by_version", {}).get(version, {}).values():
            envelope["scope"]["exclusions"] = exclusions
    for family in ("state_counts", "supplied_state_probabilities"):
        envelope = payload["observed_facts"].get(family, {}).get("by_version", {}).get(version)
        if envelope is not None:
            envelope["scope"]["exclusions"] = exclusions


def _provenance_consistency(value, bundle):
    """Reject contradicting handoffs using retained join observations only."""
    keys = set(value.scope.included_record_keys)
    _require(len(value.scope.dataset_versions) == 1 and not value.scope.excluded_record_keys,
             "provenance composition requires one complete selected version")
    _require(keys == {row.record_key for row in bundle.records if row.record_key.dataset_version in value.scope.dataset_versions},
             "provenance scope cannot discard validated records within its selected version")
    matches = tuple(match for match in bundle.provenance_join.matches if match.record_key in keys)
    _require(len(matches) == len(keys), "provenance result scope lacks retained join matches")
    _require(value.provenance_supplied is bundle.provenance_join.provenance_supplied,
             "provenance supplied status differs from validated join")
    missing = tuple(match.record_key for match in matches if match.provenance is None)
    messages = tuple(message for message in bundle.provenance_join.messages
                     if message.record_key is None or message.record_key in keys)
    _require(value.input_has_errors == any(message.severity in (ValidationSeverity.ERROR, ValidationSeverity.FATAL) for message in messages),
             "provenance result omitted its retained input validity")
    _require(set(value.validation_messages) == set(messages), "provenance result omitted or invented validation diagnostics")
    expected_coverages = (
        sum(match.provenance is not None for match in matches),
        sum(match.provenance is not None and match.provenance.required_fields_valid for match in matches),
        sum(match.provenance is not None and match.provenance.grounding_known for match in matches),
    )
    for coverage, expected in zip((value.provenance_row_coverage, value.provenance_required_field_coverage,
                                  value.grounding_field_coverage), expected_coverages):
        _coverage(coverage)
        _require(coverage.numerator == expected and coverage.denominator == len(keys) and
                 coverage.denominator_name == value.scope.denominator_basis, "provenance coverage contradicts retained join observations")
    _require(value.analyzed_record_count.value == len(keys) and value.records_with_matching_rows.value == len(keys) - len(missing) and
             value.missing_provenance_count.value == len(missing), "provenance inventory count contradicts retained join")
    for composition, field, categories in ((value.source, "source_type", ("human", "synthetic", "mixed", "sensor", "unknown")),
                                           (value.confidence, "provenance_confidence", ("confirmed", "log_derived", "estimated", "unknown"))):
        _typed(composition, DeclaredComposition, "declared composition")
        unavailable = tuple(match.record_key for match in matches if match.provenance is not None and match.provenance.values.get(field) is None)
        expected = {category: sum(match.provenance is not None and match.provenance.values.get(field) == category for match in matches)
                    for category in categories}
        _require(set(composition.unavailable_record_keys) == set(unavailable), "provenance missing-field identities differ from join")
        _require(composition.field_coverage.numerator == sum(expected.values()) and composition.field_coverage.denominator == len(keys) and
                 composition.field_coverage.denominator_name == value.scope.denominator_basis, "provenance field coverage differs from its retained declarations")
        if unavailable:
            _require(composition.status is CalculationStatus.UNAVAILABLE and composition.counts is None and composition.shares is None,
                     "missing provenance field cannot become a complete category table")
        else:
            _require(composition.status is CalculationStatus.AVAILABLE and type(composition.counts) is tuple and dict(composition.counts) == expected,
                     "provenance category counts contradict supplied declarations")
    grounding = value.direct_grounding
    _typed(grounding, DirectGroundingBasis, "direct grounding basis")
    _require(type(grounding.assignments) is tuple and all(type(item) is DirectGroundingAssignment for item in grounding.assignments), "grounding assignment types are invalid")
    assignments = {item.record_key: item for item in grounding.assignments}
    _require(len(assignments) == len(grounding.assignments) and set(assignments) == keys, "grounding assignment identities differ from join")
    for match in matches:
        row = match.provenance
        assignment = assignments[match.record_key]
        if row is None:
            classification, basis, missing_fields = "unresolved_grounding", "missing_provenance_row", ()
        elif not row.required_fields_valid:
            classification, basis, missing_fields = "unresolved_grounding", "incomplete_required_provenance", row.missing_required_fields
        elif row.values["external_grounding"] == "yes":
            classification, basis, missing_fields = "known_open", "valid_direct_grounding_yes", ()
        elif row.values["external_grounding"] == "no":
            classification, basis, missing_fields = "known_closed", "valid_direct_grounding_no", ()
        else:
            classification, basis, missing_fields = "unresolved_grounding", "declared_unknown_grounding", ()
        _require((assignment.classification, assignment.basis, assignment.missing_required_fields) == (classification, basis, missing_fields),
                 "grounding assignment contradicts retained provenance declarations")
    for classification, scalar in (("known_open", grounding.known_open_count), ("known_closed", grounding.known_closed_count),
                                   ("unresolved_grounding", grounding.unresolved_grounding_count)):
        _require(scalar.value == sum(item.classification == classification for item in grounding.assignments), "grounding count contradicts typed assignments")
    _require(grounding.input_has_errors == value.input_has_errors and set(grounding.validation_messages) == set(value.validation_messages), "grounding input validity differs from provenance")
    return matches


def _provenance(payload, value, bundle):
    _typed(value, ProvenanceCompositionResult, "provenance composition")
    scope = _scope(value.scope, bundle)
    join = bundle.provenance_join
    matches = _provenance_consistency(value, bundle)
    observed = payload["observed_facts"].setdefault("provenance", {})
    derived = payload["derived_metrics"].setdefault("provenance", {})
    total = len(value.scope.included_record_keys)
    for name, result in (("analyzed_record_count", value.analyzed_record_count),
                         ("records_with_matching_rows", value.records_with_matching_rows),
                         ("missing_provenance_count", value.missing_provenance_count)):
        observed[name] = _scalar("observed_facts.provenance." + name, result, value.scope, None, bundle,
                                 denominator=total, limitations=value.limitations)
    _require(value.analyzed_record_count.value == total and value.missing_provenance_count.value == sum(match.provenance is None for match in matches),
             "provenance counts disagree with validated join inventory")
    derived["missing_provenance_share"] = _scalar("derived_metrics.provenance.missing_provenance_share",
        value.missing_provenance_share, value.scope, None, bundle, denominator=total, limitations=value.limitations)
    covers = (("provenance_row_coverage", value.provenance_row_coverage, join.provenance_row_coverage),
              ("provenance_required_field_coverage", value.provenance_required_field_coverage, join.provenance_required_field_coverage),
              ("grounding_field_coverage", value.grounding_field_coverage, join.grounding_field_coverage))
    _require(len(value.coverage_metadata) == 3, "provenance coverage metadata is incomplete")
    for (name, coverage, original), metadata in zip(covers, value.coverage_metadata):
        _coverage(coverage)
        observed[name] = _table("observed_facts.provenance." + name, coverage.ratio, metadata,
            value.scope, None, bundle, name=name,
            status=CalculationStatus.UNAVAILABLE if coverage.ratio is None else CalculationStatus.AVAILABLE,
            reasons=(CalculationReason.EMPTY_SCOPE,) if coverage.ratio is None else (),
            denominator=coverage.denominator, coverage=coverage.ratio)
    for item, field in ((value.source, "source_type"), (value.confidence, "provenance_confidence")):
        _typed(item, DeclaredComposition, "declared provenance composition")
        _require(item.field_name == field, "provenance category namespace mismatch")
        _coverage(item.field_coverage)
        counts = dict(item.counts) if item.counts is not None else None
        _require(item.counts is None or len(counts) == len(item.counts), "duplicate provenance category")
        observed[field + "_counts"] = _table("observed_facts.provenance." + field + "_counts", counts,
            item.counts_metadata, value.scope, None, bundle, name=field + "_counts", status=item.status,
            reasons=item.reason_codes, denominator=total, coverage=item.field_coverage.ratio, limitations=value.limitations)
        observed[field + "_field_coverage"] = _table("observed_facts.provenance." + field + "_field_coverage",
            item.field_coverage.ratio, item.field_coverage_metadata, value.scope, None, bundle,
            name=field + "_field_coverage", status=CalculationStatus.UNAVAILABLE if item.field_coverage.ratio is None else CalculationStatus.AVAILABLE,
            reasons=(CalculationReason.EMPTY_SCOPE,) if item.field_coverage.ratio is None else (),
            denominator=item.field_coverage.denominator, coverage=item.field_coverage.ratio)
        if field == "source_type":
            derived["source_type_shares"] = _table("derived_metrics.provenance.source_type_shares",
                dict(item.shares) if item.shares is not None else None, item.shares_metadata, value.scope, None,
                bundle, name="source_type_shares", status=item.status, reasons=item.reason_codes,
                denominator=total, coverage=item.field_coverage.ratio, limitations=value.limitations)
    grounding = value.direct_grounding
    _typed(grounding, DirectGroundingBasis, "direct grounding basis")
    _require(type(grounding.assignments) is tuple and all(type(item) is DirectGroundingAssignment for item in grounding.assignments), "grounding assignments require exact immutable types")
    _require(grounding.scope == value.scope, "grounding scope differs from provenance scope")
    _require({item.record_key for item in grounding.assignments} == set(value.scope.included_record_keys),
             "grounding assignments omit or invent scoped identities")
    for name, result in (("known_open_count", grounding.known_open_count), ("known_closed_count", grounding.known_closed_count),
                         ("unresolved_grounding_count", grounding.unresolved_grounding_count)):
        observed[name] = _scalar("observed_facts.provenance." + name, result, value.scope, None, bundle,
                                 denominator=total, coverage=value.grounding_field_coverage.ratio,
                                 limitations=grounding.limitations)
    if value.weighted_source is not None:
        weighted = value.weighted_source
        _typed(weighted, WeightedSourceComposition, "weighted provenance companion")
        denominator = weighted.total_weight.value
        weighting = WeightingOptions("weighted", "weight")
        for name, table, metadata in (
            ("weighted_source_type_masses", weighted.weighted_source_type_masses, weighted.mass_metadata),
            ("weighted_source_type_shares", weighted.weighted_source_type_shares, weighted.shares_metadata)):
            derived[name] = _table("derived_metrics.provenance." + name, dict(table) if table is not None else None,
                metadata, value.scope, None, bundle, name=name, status=weighted.status, reasons=weighted.reason_codes,
                denominator=denominator, weighting=weighting, limitations=value.limitations)
        for name, scalar in (("total_weight", weighted.total_weight), ("missing_provenance_weight", weighted.missing_provenance_weight),
                             ("weighted_missing_provenance_share", weighted.weighted_missing_provenance_share)):
            derived[name] = _scalar("derived_metrics.provenance." + name, scalar, value.scope, None, bundle,
                                   denominator=denominator, weighting=weighting, limitations=value.limitations)


def _duplicates(payload, value, bundle):
    _typed(value, ExactDuplicateResult, "exact duplicates")
    _require(value.evidence_class is CalculationEvidenceClass.OBSERVED_FACT, "duplicate evidence class was altered")
    scope = _scope(value.scope, bundle)
    coverage = _coverage(value.coverage)
    groups = []
    seen = set()
    for index, group in enumerate(value.exact_duplicate_groups):
        _typed(group, ExactDuplicateGroup, "duplicate group")
        _require(len(group.record_keys) >= 2 and len(set(group.record_keys)) == len(group.record_keys), "duplicate group must retain unique members")
        _require(set(group.record_keys) <= set(value.scope.included_record_keys) and not seen.intersection(group.record_keys),
                 "duplicate groups overlap or leave their scope")
        seen.update(group.record_keys)
        groups.append({"group_id": "exact_duplicate_group_" + str(index + 1),
                       "record_keys": [_key(key) for key in group.record_keys],
                       "record_count": len(group.record_keys), "normalization_profile": "exact_utf8_v1"})
    content = payload["observed_facts"].setdefault("content", {})
    for name, scalar in (("duplicate_record_count", value.duplicate_record_count), ("duplicate_group_count", value.duplicate_group_count)):
        content[name] = _scalar("observed_facts.content." + name, scalar, value.scope, value.representation,
            bundle, denominator=coverage["denominator"], coverage=coverage["ratio"], limitations=value.limitations)
    _require(value.duplicate_group_count.value is None or value.duplicate_group_count.value == len(groups), "duplicate group count disagrees with typed groups")
    _require(value.duplicate_record_count.value is None or value.duplicate_record_count.value == sum(group["record_count"] - 1 for group in groups), "duplicate record count disagrees with typed groups")
    status = value.duplicate_group_count.status
    content["exact_duplicate_groups"] = _envelope("observed_facts.content.exact_duplicate_groups",
        groups if status is CalculationStatus.AVAILABLE else None, scope,
        representation=_representation(value.representation), denominator=coverage["denominator"], coverage=coverage["ratio"],
        status=status.value, reasons=tuple(item.value for item in value.duplicate_group_count.reason_codes),
        required=("usable_exact_content",) if status is CalculationStatus.UNAVAILABLE else (), limitations=value.limitations)


def _tail(payload, value, bundle):
    _typed(value, TailSelectionResult, "tail selection")
    scope = _scope(value.scope, bundle)
    selection = {"rule": value.options.rule, "count_threshold": value.options.count_threshold,
                 "frequency_threshold": value.options.frequency_threshold, "state_ids": list(value.options.state_ids),
                 "ranking_rule": value.ranking_rule}
    target = {"tail_rule": value.options.rule, "selection": selection}
    for name, scalar in (("tail_support_size", value.tail_support_size), ("tail_record_share", value.tail_record_share)):
        _require(scalar.status is value.status and scalar.reason_codes == value.reason_codes, "tail scalar status differs from result")
        target[name] = _scalar("derived_metrics.tail." + name, scalar, value.scope, value.representation,
                              bundle, denominator=value.denominator, limitations=value.limitations)
    ranking = []
    for item in value.rarity_ranking:
        _typed(item, RarityEntry, "rarity entry")
        ranking.append({"state_id": item.state_id, "state_count": item.state_count,
                        "state_frequency": item.state_frequency, "rarity_rank": item.rarity_rank, "in_tail": item.in_tail})
    _require(set(value.tail_membership) == {item.state_id for item in value.rarity_ranking if item.in_tail}, "tail membership differs from ranked entries")
    available = value.status is CalculationStatus.AVAILABLE
    for name, table, metadata, metric in (("rarity_ranking", ranking, value.ranking_metadata, "rarity_rank"),
                                         ("tail_states", list(value.tail_membership), value.membership_metadata, "tail_membership")):
        target[name] = _table("derived_metrics.tail." + name, table if available else None, metadata,
            value.scope, value.representation, bundle, name=metric, status=value.status,
            reasons=value.reason_codes, denominator=value.denominator, limitations=value.limitations)
    payload["derived_metrics"]["tail"] = target


def _comparison(payload, value, bundle):
    _typed(value, SupportComparison, "support comparison")
    compatibility = value.compatibility
    _typed(compatibility, RepresentationCompatibility, "comparison compatibility")
    context = compatibility.context
    _typed(context, ExplicitPairContext, "explicit pair context")
    _typed(value.original_earlier, DistributionMetrics, "original earlier distribution")
    _typed(value.original_later, DistributionMetrics, "original later distribution")
    _typed(value.harmonized_earlier, DistributionMetrics, "harmonized earlier distribution")
    _typed(value.harmonized_later, DistributionMetrics, "harmonized later distribution")
    _require(value.original_earlier.weighting == value.original_later.weighting and value.original_earlier.denominator_basis == value.original_later.denominator_basis and
             (value.original_earlier.input_basis == "explicit_probability_vector") == (value.original_later.input_basis == "explicit_probability_vector"), "comparison cannot mix incompatible weighting or probability/count bases")
    for original, harmonized in ((value.original_earlier, value.harmonized_earlier), (value.original_later, value.harmonized_later)):
        _require(original.input_basis == harmonized.input_basis and original.weighting == harmonized.weighting and original.frequency_denominator == harmonized.frequency_denominator and original.denominator_basis == harmonized.denominator_basis, "harmonization cannot replace input basis or denominators")
    probability_pair = value.original_earlier.input_basis == value.original_later.input_basis == "explicit_probability_vector"
    _require(probability_pair or context.version_order == bundle.version_order, "comparison chronology differs from validated bundle order")
    if probability_pair:
        bundle = None
    earlier = context.earlier_scope.dataset_versions
    later = context.later_scope.dataset_versions
    _require(len(earlier) == len(later) == 1 and earlier != later, "comparison requires one distinct version per side")
    order = context.version_order.order
    _require(earlier[0] in order and later[0] in order and order.index(earlier[0]) < order.index(later[0]),
             "comparison lacks explicit earlier/later chronology")
    _require(context.earlier_scope == value.original_earlier.scope and context.later_scope == value.original_later.scope and
             context.earlier_representation == value.original_earlier.representation and
             context.later_representation == value.original_later.representation,
             "comparison context differs from original inputs")
    _require(value.harmonized_earlier.scope == context.earlier_scope and value.harmonized_later.scope == context.later_scope,
             "harmonization cannot replace selected record scopes")
    _require(value.harmonized_earlier.representation == compatibility.harmonized_representation and
             value.harmonized_later.representation == compatibility.harmonized_representation,
             "harmonized representation differs from compatibility declaration")
    _require(compatibility.earlier_state_semantics and compatibility.later_state_semantics and compatibility.harmonized_state_semantics,
             "comparison requires explicit state meanings")
    if compatibility.mapping is None:
        _require(compatibility.method == "identical_declared_basis" and context.earlier_representation == context.later_representation == compatibility.harmonized_representation and
                 compatibility.earlier_state_semantics == compatibility.later_state_semantics == compatibility.harmonized_state_semantics and
                 compatibility.collision_groups == () and value.harmonized_earlier == value.original_earlier and value.harmonized_later == value.original_later,
                 "unmapped comparison does not preserve its identical declared basis")
    else:
        _require(compatibility.method == "explicit_directed_state_mapping", "mapped comparison has an unsupported method")
    temporary = {"observed_facts": {}, "derived_metrics": {}}
    for item in (value.original_earlier, value.original_later):
        _distribution(temporary, item, bundle, weighted=item.weighting.weighting_mode == "weighted")
    temporary = {"observed_facts": {}, "derived_metrics": {}}
    for item in (value.harmonized_earlier, value.harmonized_later):
        _distribution(temporary, item, bundle, weighted=item.weighting.weighting_mode == "weighted")
    scalar_scope = value.support_delta.metadata.scope
    _require(scalar_scope.dataset_versions == earlier + later and
             scalar_scope.included_record_keys == context.earlier_scope.included_record_keys + context.later_scope.included_record_keys and
             scalar_scope.excluded_record_keys == context.earlier_scope.excluded_record_keys + context.later_scope.excluded_record_keys,
             "comparison result scope differs from its ordered pair")
    _require(scalar_scope.denominator_basis == "separate_ordered_representation_scopes" and scalar_scope.scope_id == context.earlier_scope.scope_id + " -> " + context.later_scope.scope_id, "comparison scope declaration changed")
    _require(value.gini_simpson_diversity_delta.status is value.status and value.gini_simpson_diversity_delta.reason_codes == value.reason_codes, "comparison diversity status mismatch")
    representation = compatibility.harmonized_representation
    support = payload["derived_metrics"].setdefault("support", {})
    weighting = value.harmonized_earlier.weighting
    _require(weighting == value.harmonized_later.weighting, "comparison mixes weighting families")
    for name, scalar in (("support_delta", value.support_delta), ("support_loss_count", value.support_loss_count),
                         ("support_added_count", value.support_added_count), ("support_retention_ratio", value.support_retention_ratio)):
        _require(scalar.status is value.status and scalar.reason_codes == value.reason_codes, "comparison scalar status mismatch")
        support[name] = _scalar("derived_metrics.support." + name, scalar, scalar_scope, representation,
            bundle, denominator=value.retention_denominator, weighting=weighting, limitations=value.limitations)
    for envelope in support.values():
        if type(envelope) is dict and "evidence_class" in envelope:
            envelope["input_basis"] = value.original_earlier.input_basis
    payload["derived_metrics"].setdefault("diversity", {})["gini_simpson_diversity_delta"] = _scalar(
        "derived_metrics.diversity.gini_simpson_diversity_delta", value.gini_simpson_diversity_delta,
        scalar_scope, representation, bundle, denominator=value.retention_denominator, weighting=weighting,
        limitations=value.limitations)
    payload["derived_metrics"]["diversity"]["gini_simpson_diversity_delta"]["input_basis"] = value.original_earlier.input_basis
    _require(len(value.set_metadata) == 3, "comparison set metadata is incomplete")
    for (name, states), metadata in zip((("extinct_states", value.extinct_states), ("added_states", value.added_states),
                                        ("retained_states", value.retained_states)), value.set_metadata):
        support[name] = _table("derived_metrics.support." + name, list(states) if states is not None else None,
            metadata, scalar_scope, representation, bundle, name=name, status=value.status,
            reasons=value.reason_codes, denominator=value.retention_denominator, weighting=weighting,
            limitations=value.limitations)
    for name in ("extinct_states", "added_states", "retained_states"):
        support[name]["input_basis"] = value.original_earlier.input_basis
    state_mapping = []
    if compatibility.mapping is not None:
        mapping = compatibility.mapping
        _typed(mapping, StateMappingDeclaration, "directed state mapping")
        _require(mapping.direction in ("earlier_to_later", "later_to_earlier"), "unsupported mapping direction")
        source_rep = context.earlier_representation if mapping.direction == "earlier_to_later" else context.later_representation
        target_rep = context.later_representation if mapping.direction == "earlier_to_later" else context.earlier_representation
        source_meaning = compatibility.earlier_state_semantics if mapping.direction == "earlier_to_later" else compatibility.later_state_semantics
        target_meaning = compatibility.later_state_semantics if mapping.direction == "earlier_to_later" else compatibility.earlier_state_semantics
        _require(mapping.source_representation == source_rep and mapping.target_representation == target_rep and mapping.source_state_semantics == source_meaning and mapping.target_state_semantics == target_meaning, "mapping representation or meaning mismatch")
        _require(compatibility.harmonized_representation == target_rep and compatibility.harmonized_state_semantics == target_meaning, "mapping harmonized target mismatch")
        _require(type(mapping.state_mapping) in (dict, MappingProxyType), "state mapping requires literal retained data")
        state_mapping = [{"source_state": source, "target_state": target} for source, target in mapping.state_mapping.items()]
    _require(value.mapping_effect == (("earlier", value.original_earlier.support_size.value, value.harmonized_earlier.support_size.value), ("later", value.original_later.support_size.value, value.harmonized_later.support_size.value)), "mapping effects differ from retained original/harmonized results")
    effects = []
    for side, original, harmonized in value.mapping_effect:
        _require(side in ("earlier", "later"), "mapping effect side must be explicit")
        effects.append({"dataset_version": earlier[0] if side == "earlier" else later[0],
                        "original_support_size": original, "harmonized_support_size": harmonized})
    details = {"earlier_version": earlier[0], "later_version": later[0], "version_order": list(order),
               "version_order_source": context.version_order.order_source,
               "earlier_state_semantics": compatibility.earlier_state_semantics,
               "later_state_semantics": compatibility.later_state_semantics,
               "harmonized_state_semantics": compatibility.harmonized_state_semantics,
               "compatibility_method": compatibility.method,
               "earlier_representation": _representation(context.earlier_representation),
               "later_representation": _representation(context.later_representation),
               "harmonized_representation": _representation(representation),
               "original_earlier_support": list(value.original_earlier.support),
               "original_later_support": list(value.original_later.support),
               "harmonized_earlier_support": list(value.harmonized_earlier.support),
               "harmonized_later_support": list(value.harmonized_later.support),
               "retention_denominator": value.retention_denominator,
               "retention_denominator_basis": value.retention_denominator_basis,
               "state_mapping": state_mapping, "mapping_effect": effects,
               "collision_groups": [{"target_state": target, "source_states": list(sources)}
                                    for target, sources in compatibility.collision_groups]}
    support["comparison_details"] = _envelope("derived_metrics.support.comparison_details", details,
        _scope(scalar_scope, bundle), representation=_representation(representation),
        denominator=value.retention_denominator, assumptions=value.support_delta.metadata.assumptions,
        limitations=value.limitations + compatibility.limitations)


def _closure(payload, value, bundle, provenance):
    _typed(value, DirectClosureExposureBounds, "direct closure exposure")
    _scope(value.scope, bundle)
    _require(value.denominator == len(value.scope.included_record_keys) and
             value.denominator_basis == value.scope.denominator_basis, "closure denominator differs from selected scope")
    _require(value.classification_basis == value.operationalization_label == "toolkit_operationalization",
             "direct closure must preserve its operationalization label")
    _require(value.confidence_disclosure == "provenance_confidence_is_separate_and_does_not_discount_grounding",
             "confidence cannot discount grounding")
    for number in (value.known_open_count, value.known_closed_count, value.unresolved_grounding_count):
        _number(number, "grounding count", integer=True, minimum=0)
    _require(sum((value.known_open_count, value.known_closed_count, value.unresolved_grounding_count)) == value.denominator,
             "grounding partition differs from closure denominator")
    if provenance is not None:
        _require(value.input_has_errors == provenance.input_has_errors and set(value.validation_messages) == set(provenance.validation_messages), "closure input validity differs from supplied provenance")
        _require(value.provenance_row_coverage == provenance.provenance_row_coverage and value.provenance_required_field_coverage == provenance.provenance_required_field_coverage and value.grounding_field_coverage == provenance.grounding_field_coverage and value.confidence_field_coverage == provenance.confidence.field_coverage, "closure coverage differs from supplied provenance")
        _require(value.confidence_status == provenance.confidence.status and value.confidence_counts == provenance.confidence.counts, "closure confidence disclosure differs from supplied provenance")
        _require(value.scope == provenance.scope and value.known_open_count == provenance.direct_grounding.known_open_count.value and
                 value.known_closed_count == provenance.direct_grounding.known_closed_count.value and
                 value.unresolved_grounding_count == provenance.direct_grounding.unresolved_grounding_count.value,
                 "direct closure disagrees with supplied provenance basis")
    coverage = None if value.grounding_field_coverage is None else _coverage(value.grounding_field_coverage)["ratio"]
    target = {"classification_basis": value.classification_basis, "confidence_disclosure": value.confidence_disclosure}
    for name, scalar, metric in (("lower_bound", value.lower_bound, "direct_closure_exposure_lower_bound"),
                                ("upper_bound", value.upper_bound, "direct_closure_exposure_upper_bound"),
                                ("interval_width", value.interval_width, "direct_closure_exposure_interval_width")):
        target[name] = _scalar("derived_metrics.closure_exposure.direct." + name, scalar, value.scope, None, bundle,
            name=metric, denominator=value.denominator, coverage=coverage, limitations=value.limitations)
    payload["derived_metrics"].setdefault("closure_exposure", {})["direct"] = target


def _simulation_inputs(value):
    _typed(value, ResamplingInput, "resampling input")
    _scope(value.scope, None)
    _representation(value.representation)
    _policy(value.numerical_policy)
    for table in (value.supplied_distribution, value.effective_distribution):
        _require(type(table) is tuple and all(type(pair) is tuple and len(pair) == 2 and type(pair[0]) is str for pair in table), "scenario distributions require literal immutable state pairs")
        _require(type(table) is tuple and len({state for state, probability in table}) == len(table), "scenario states must be unique immutable pairs")
        for state, probability in table:
            _require(type(state) is str, "scenario state requires literal text")
            _number(probability, "scenario probability", minimum=0, maximum=1)
    return {"supplied_distribution": [{"state_id": state, "probability": probability} for state, probability in value.supplied_distribution],
            "effective_distribution": [{"state_id": state, "probability": probability} for state, probability in value.effective_distribution],
            "supplied_probability_total": value.supplied_probability_total, "effective_probability_total": value.effective_probability_total,
            "probability_residual": value.probability_residual, "correction_applied": value.correction_applied,
            "correction_method": value.correction_method, "normalization_divisor": value.normalization_divisor,
            "probability_corrections": [{"state_id": state, "correction": correction} for state, correction in value.probability_corrections]}


def _closed_simulation(payload, value):
    _require(type(value) in (ExpectedDiversityResult, ResamplingSimulation), "closed scenario requires its exact accepted type")
    inputs = value.inputs
    normalization = _simulation_inputs(inputs)
    _require(value.evidence_class is CalculationEvidenceClass.SIMULATION and value.experimental is True and value.model_name == "closed_resampling",
             "closed scenario evidence class or model was altered")
    _require(value.method_version == "closed_categorical_v1", "unsupported scenario model version")
    _require(value.assumptions == ("Fixed finite declared state space and constant positive integer resample size.", "X_t conditional on p_t is Multinomial(n,p_t); p_(t+1)=X_t/n.", "No mutation, migration, independent real data or external corrective input."), "scenario assumptions cannot be replaced or removed")
    expected = type(value) is ExpectedDiversityResult
    _require(value.method == ("analytic_expectation" if expected else "sampled_path"), "scenario result type and method disagree")
    target = _base("simulations.closed_resampling", _scope(inputs.scope, None),
        representation=_representation(inputs.representation), denominator=value.resample_size,
        assumptions=value.assumptions, limitations=value.limitations, status="experimental")
    target.update({"model": value.model_name, "model_version": value.method_version, "method": value.method,
                   "resample_size": value.resample_size, "initial_distribution": normalization["effective_distribution"],
                   "input_normalization": normalization,
                   "parameters": {"resample_size": value.resample_size, "simulation_horizon": value.simulation_horizon,
                        "random_seed": value.random_seed, "simulation_replicates": value.simulation_replicates,
                        "rng_name": value.rng_name, "numpy_version": None if expected else value.numpy_version,
                        "replicate_schedule": None if expected else value.replicate_schedule,
                        "state_order": [state for state, probability in inputs.effective_distribution],
                        "input_basis": inputs.input_basis, "reopening_weight": None, "external_input_distribution": [],
                        "numerical_policy": _policy(inputs.numerical_policy)}})
    if expected:
        _metadata(value.expected_diversity_metadata, name="expected_gini_simpson_diversity", scope=inputs.scope,
                  representation=inputs.representation, owner="T1", evidence=CalculationEvidenceClass.SIMULATION,
                  unit="ratio", formula="F-015", weighting=WeightingOptions())
        target.update({"initial_gini_simpson_diversity": value.initial_gini_simpson_diversity,
                       "contraction_factor": value.contraction_factor, "expected_diversity": list(value.expected_diversity),
                       "numerical_underflow_steps": list(value.numerical_underflow_steps)})
    else:
        _require(value.state_order == tuple(state for state, probability in inputs.effective_distribution), "sampled state order differs from declared distribution")
        _require(value.sampler_algorithm == "sequential_binomial_complement_v1" and
                 value.state_schedule == "ascending_unicode_state_id_skip_zero", "unsupported sampled algorithm or ordering")
        _require(len(value.trajectory_metadata) == 4, "sampled trajectory metadata is incomplete")
        for metadata, (name, formula, unit) in zip(value.trajectory_metadata,
                (("state_count", None, "sampled_records"), ("state_frequency", "F-001", "ratio"),
                 ("support_size", "F-002", "states"), ("gini_simpson_diversity", "F-003", "ratio"))):
            _metadata(metadata, name=name, scope=inputs.scope, representation=inputs.representation,
                      owner="T1", evidence=CalculationEvidenceClass.SIMULATION, unit=unit, formula=formula,
                      weighting=WeightingOptions())
        paths = []
        trajectories = []
        for replicate in value.sampled_paths:
            _typed(replicate, ResamplingReplicate, "sampled replicate")
            generations = []
            for generation in replicate.generations:
                _typed(generation, SampledGeneration, "sampled generation")
                _require(len(generation.state_frequencies) == len(value.state_order), "sampled frequencies differ from state order")
                _require(generation.state_counts is None or len(generation.state_counts) == len(value.state_order), "sampled counts differ from state order")
                _require((generation.step == 0) == (generation.state_counts is None), "sampled initial counts must remain unavailable and later counts present")
                _require(generation.support_size == len(generation.support) and set(generation.support) <= set(value.state_order), "sampled support identity mismatch")
                generations.append({"step": generation.step,
                    "state_counts": None if generation.state_counts is None else list(generation.state_counts),
                    "state_frequencies": list(generation.state_frequencies), "support": list(generation.support),
                    "support_size": generation.support_size, "gini_simpson_diversity": generation.gini_simpson_diversity})
            _require([row["step"] for row in generations] == list(range(value.simulation_horizon + 1)), "sampled generation sequence is incomplete")
            paths.append({"replicate_index": replicate.replicate_index, "generations": generations})
            trajectories.append({"replicate_index": replicate.replicate_index,
                                 "support_sizes": [generation.support_size for generation in replicate.generations]})
        _require([item["replicate_index"] for item in paths] == list(range(value.simulation_replicates)), "replicate indices must retain the accepted schedule")
        target["sampled_paths"] = paths
        target["support_trajectories"] = trajectories
        target["limitations"] = list(dict.fromkeys(target["limitations"] + ["Extinction events are not separately inferred by the assembly adapter; inspect the supplied sampled support paths."]))
    payload["simulations"]["closed_resampling"] = target


def _extinction(payload, values):
    _require(type(values) is tuple and values, "extinction scenarios require an immutable nonempty tuple")
    first = values[0]
    _typed(first, ExtinctionProbabilityResult, "one-step extinction scenario")
    target = _base("simulations.tail_extinction", _scope(first.scope, None),
        representation=_representation(first.representation), denominator=first.resample_size,
        assumptions=first.one_step_extinction_probability.metadata.assumptions,
        limitations=first.limitations, status="experimental")
    target.update({"model": "closed_resampling", "model_version": "closed_categorical_v1",
                   "method": "analytic_extinction", "resample_size": first.resample_size,
                   "initial_distribution": [], "parameters": {"resample_size": first.resample_size,
                       "simulation_horizon": 1, "random_seed": None, "simulation_replicates": None,
                       "rng_name": None, "numpy_version": None, "replicate_schedule": None,
                       "state_order": [], "input_basis": first.input_basis, "reopening_weight": None,
                       "external_input_distribution": [], "numerical_policy": _policy(first.numerical_policy)}, "by_state": {}})
    for value in values:
        _typed(value, ExtinctionProbabilityResult, "one-step extinction scenario")
        _require(value.scope == first.scope and value.representation == first.representation and
                 value.resample_size == first.resample_size and value.numerical_policy == first.numerical_policy,
                 "extinction marginals must share one explicit scenario basis")
        _require(value.method == "analytic_extinction" and value.model_name == "closed_resampling" and value.simulation_horizon == 1 and
                 value.experimental is True and value.evidence_class is CalculationEvidenceClass.SIMULATION and value.random_seed is None,
                 "extinction scenario declarations were altered")
        _require(value.input_basis == "supplied_selected_state_marginal" and value.evaluation_method == "exp(resample_size * log1p(-state_frequency)); exact endpoints", "extinction marginal basis or method was altered")
        scalar = value.one_step_extinction_probability
        _metadata(scalar.metadata, name="one_step_extinction_probability", scope=value.scope, representation=value.representation,
                  owner="T2", evidence=CalculationEvidenceClass.SIMULATION, unit="probability", formula="F-014", weighting=WeightingOptions())
        ScalarCalculation(scalar.metadata, scalar.status, scalar.value, scalar.reason_codes)
        _require(scalar.status is CalculationStatus.AVAILABLE and value.state_id not in target["by_state"], "extinction marginal is unavailable or duplicated")
        target["by_state"][value.state_id] = {"observed_frequency": value.state_frequency,
            "one_step_extinction_probability": scalar.value, "numerical_underflow": value.numerical_underflow}
        target["parameters"]["state_order"].append(value.state_id)
        target["initial_distribution"].append({"state_id": value.state_id, "probability": value.state_frequency})
    payload["simulations"]["tail_extinction"] = target


def _message_family(message):
    if message.field in ("parent_ids", "generation") or message.code in (
            "E_PARENT_AMBIGUOUS", "E_PARENT_FORMAT", "E_PARENT_FUTURE_VERSION", "E_LINEAGE_CYCLE", "W_GENERATION_MISMATCH"):
        return ["lineage"]
    if message.field in ("source_type", "provenance_confidence", "external_grounding") or message.file_role is not None and message.file_role.value == "provenance_manifest":
        return ["provenance"]
    if message.field in ("version_order", "pair_order", "representation_compatibility"):
        return ["dataset_longitudinal"]
    if message.field in ("representation", "topic", "embedding_cluster", "content", "content_ref"):
        return ["content_diagnostics"]
    return ["ingestion"]


def _diagnostics(payload, messages, family=None):
    _require(type(messages) is tuple, "diagnostic collections must be immutable tuples")
    for message in messages:
        _typed(message, ValidationMessage, "validation message")
        _require(type(message.severity) is ValidationSeverity, "diagnostic severity requires accepted enum")
        _require(type(message.code) is str and type(message.message) is str and (message.field is None or type(message.field) is str), "diagnostic text must be literal strings")
        if message.file_role is not None:
            _typed(message.file_role, FileRole, "diagnostic file role")
        effects = [family] if family is not None else _message_family(message)
        if message.severity is ValidationSeverity.INFO:
            payload["inputs"]["limitations"].append("Validation notice " + message.code + ": " + message.message)
            continue
        if message.severity is ValidationSeverity.WARNING:
            location = {"file_role": None if message.file_role is None else message.file_role.value,
                        "field": message.field, "record_key": None if message.record_key is None else _key(message.record_key),
                        "row_number": message.row_number, "line_number": message.line_number}
            item = {"code": message.code, "message": message.message, "count": 1,
                    "affected_scope": payload["inputs"]["scope"], "representative_locations": [location],
                    "effect_on_capabilities": effects, "remediation": [], "severity": "warning"}
            if item not in payload["warnings"]:
                payload["warnings"].append(item)
        else:
            item = {"code": message.code, "severity": message.severity.value, "message": message.message,
                    "file_role": None if message.file_role is None else message.file_role.value,
                    "field": message.field, "record_key": None if message.record_key is None else _key(message.record_key),
                    "row_number": message.row_number, "effect_on_run": "partial" if payload["inputs"]["scope"]["record_count"] else "failed",
                    "effect_on_capabilities": effects, "remediation": []}
            if item not in payload["errors"]:
                payload["errors"].append(item)


def _inputs(payload, bundle):
    scope = _bundle_scope(bundle)
    payload["inputs"] = {"scope": scope, "version_order": list(bundle.version_order.order),
                         "version_order_source": bundle.version_order.order_source or None,
                         "representation": None, "artifacts": [], "file_hashes": [],
                         "limitations": ["Input hashes identify supplied bytes and do not certify authenticity.",
                                         "Only allowlisted evidence fields are assembled; raw content, extras, notes and embeddings are not exported."]}
    records_by_version = {}
    versions_by_location = {}
    messages_by_location = {}
    for row in bundle.records:
        records_by_version.setdefault(row.record_key.dataset_version, []).append(row.record_key)
    for row in bundle.records + (() if bundle.provenance is None else bundle.provenance):
        _require(type(row) in (CanonicalRow, ProvenanceAssessment), "input row must retain an accepted typed location")
        versions_by_location.setdefault((row.location.file_role, row.location.file_path), set()).add(row.record_key.dataset_version)
    for message in bundle.validation_messages:
        messages_by_location.setdefault((message.file_role, message.file_path), []).append(message)
    for index, artifact in enumerate(bundle.inventory):
        messages = tuple(messages_by_location.get((artifact.role, str(artifact.path)), ()))
        uncertain = tuple(messages_by_location.get((artifact.role, "[redacted]"), ())) + tuple(messages_by_location.get((artifact.role, None), ()))
        errors = any(message.severity in (ValidationSeverity.ERROR, ValidationSeverity.FATAL) for message in messages + uncertain)
        versions = sorted(versions_by_location.get((artifact.role, str(artifact.path)), ()))
        inventory_only = artifact.role in (FileRole.EMBEDDING_DATA, FileRole.EXTERNAL_REFERENCE)
        payload["inputs"]["artifacts"].append({"role": artifact.role.value, "path": str(artifact.path), "path_redacted": False,
            "format": artifact.file_format.value, "file_hash": artifact.sha256, "hash_algorithm": "sha256",
            "size_bytes": artifact.size_bytes, "row_count": artifact.row_count, "dataset_versions": versions,
            "schema_fields": list(artifact.fields), "parse_status": "not_requested" if inventory_only else "completed",
            "validation_status": "not_requested" if inventory_only else "partial" if errors else "completed", "reason_codes": ["R_INVENTORY_ONLY_ROLE"] if inventory_only else list(dict.fromkeys(message.code for message in messages + uncertain))})
        payload["inputs"]["file_hashes"].append({"artifact_index": index, "algorithm": "sha256", "value": artifact.sha256})
    versions = bundle.version_order.loaded_versions
    counts = {}
    for version in versions:
        keys = records_by_version.get(version, [])
        version_scope = {"dataset_versions": [version], "record_count": len(keys), "excluded_record_count": 0,
                         "denominator_basis": "validated_records_in_version", "scope_id": "validated_version:" + version,
                         "included_record_keys": [_key(key) for key in keys], "excluded_record_keys": []}
        counts[version] = _envelope("observed_facts.record_counts.*", len(keys), version_scope, denominator=len(keys))
    payload["observed_facts"]["record_counts"] = counts
    join = bundle.provenance_join
    join_scope = {"dataset_versions": list(join.selected_dataset_versions), "record_count": len(join.scope_record_keys),
                  "excluded_record_count": 0, "denominator_basis": join.provenance_row_coverage.denominator_name,
                  "scope_id": "validated_provenance_join", "included_record_keys": [_key(key) for key in join.scope_record_keys],
                  "excluded_record_keys": []}
    provenance = {}
    for name, coverage in (("provenance_row_coverage", join.provenance_row_coverage),
                           ("provenance_required_field_coverage", join.provenance_required_field_coverage),
                           ("grounding_field_coverage", join.grounding_field_coverage)):
        checked = _coverage(coverage)
        _require(coverage.denominator == len(join.scope_record_keys), "join coverage denominator differs from join scope")
        provenance[name] = _envelope("observed_facts.provenance." + name, checked["ratio"], join_scope,
            denominator=coverage.denominator, coverage=checked["ratio"],
            status="unavailable" if checked["ratio"] is None else "available",
            reasons=("R_CALC_EMPTY_SCOPE",) if checked["ratio"] is None else (),
            required=("nonempty_validated_record_scope",) if checked["ratio"] is None else (),
            limitations=("Validation coverage describes supplied declarations without certifying their truth.",))
    payload["observed_facts"]["provenance"] = provenance
    if bundle.mapping_traces:
        operations = []
        affected = []
        unmapped = set()
        hashes = set()
        for trace in bundle.mapping_traces:
            hashes.add(trace.mapping_sha256)
            unmapped.update(trace.unmapped_fields)
            for target, selector, sources, names in trace.fields:
                if target not in affected:
                    affected.append(target)
                for name in names:
                    entry = {"operation": name, "source_field": sources[0] if len(sources) == 1 else None, "target_field": target}
                    if entry not in operations:
                        operations.append(entry)
        _require(len(hashes) == 1, "one schema mapping summary cannot collapse distinct mapping declarations")
        payload["inputs"]["schema_mapping"] = {"file_hash": next(iter(hashes)), "operations": operations,
            "fields_affected": affected, "unmapped_field_count": len(unmapped), "unsafe_operation_count": 0}
    _diagnostics(payload, bundle.validation_messages)
    _diagnostics(payload, join.messages)
    _diagnostics(payload, bundle.observability.validation_messages)
    if bundle.generation is not None:
        _diagnostics(payload, bundle.generation.messages)


def _capabilities(payload, bundle, operations, failures):
    matrix = {}
    for key in CapabilityKey:
        original = bundle.observability.capabilities[key]
        _typed(original, Capability, "input capability")
        _typed(original.status, CapabilityStatus, "input capability status")
        _require(type(original.coverage_details) in (dict, MappingProxyType), "capability coverage details require literal retained data")
        coverage = None if original.coverage is None else _coverage(original.coverage)["ratio"]
        completed = operations[key.value]
        reasons = []
        execution = "completed" if completed else "not_requested"
        if not completed:
            reasons.append("R_ANALYSIS_NOT_REQUESTED")
        if key is CapabilityKey.DATASET_LONGITUDINAL and completed:
            execution, reasons = "partial", ["R_LONGITUDINAL_FAMILIES_DEFERRED"]
        if key in (CapabilityKey.LINEAGE, CapabilityKey.MODEL_LONGITUDINAL):
            execution, reasons = "deferred", ["R_LINEAGE_EXECUTION_DEFERRED" if key is CapabilityKey.LINEAGE else "R_MODEL_ANALYSIS_DEFERRED"]
        family_codes = [error["code"] for error in payload["errors"] if key.value in error["effect_on_capabilities"]]
        if family_codes and key not in (CapabilityKey.LINEAGE, CapabilityKey.MODEL_LONGITUDINAL):
            execution = "partial" if completed else "failed"
            reasons = list(dict.fromkeys(reasons + family_codes))
        if key is CapabilityKey.INGESTION and any("ingestion" in error["effect_on_capabilities"] for error in payload["errors"]):
            execution = "partial" if bundle.records else "failed"
            reasons = ["R_INPUT_VALIDATION_ERROR"]
        detail_names = {"content": "record_coverage", "representation": "representation_coverage",
                        "row": "provenance_row_coverage", "required_fields": "provenance_required_field_coverage", "grounding": "grounding_field_coverage"}
        _require(set(original.coverage_details) <= set(detail_names), "unknown input capability coverage detail")
        entry = {"status": original.status.value, "reason_codes": list(original.reason_codes),
                 "coverage": coverage, "coverage_reason": "coverage_not_supplied_or_empty_denominator" if coverage is None else None,
                 "requirements_met": list(original.requirements_met), "requirements_missing": list(original.requirements_missing),
                 "notes": list(original.notes), "execution_status": execution, "execution_scope": list(completed),
                 "execution_reason_codes": reasons,
                 "coverage_details": {detail_names[name]: _coverage(value) for name, value in original.coverage_details.items()}}
        if key is CapabilityKey.PROVENANCE:
            for name, value in (("provenance_row_coverage", bundle.provenance_join.provenance_row_coverage),
                                ("provenance_required_field_coverage", bundle.provenance_join.provenance_required_field_coverage),
                                ("grounding_field_coverage", bundle.provenance_join.grounding_field_coverage)):
                entry["coverage_details"][name] = _coverage(value)
        if key is CapabilityKey.LINEAGE and original.coverage is not None:
            entry["coverage_details"]["resolved_parent_edge_coverage"] = _coverage(original.coverage)
        if key is CapabilityKey.DATASET_LONGITUDINAL and completed:
            entry["notes"].append("Executed only the supplied explicit-pair support/diversity comparison; no adjacent-pair discovery, lineage/provenance trajectory or relative-change calculation.")
        if key is CapabilityKey.INTERVENTION_SIMULATION and completed:
            entry["notes"].append("Execution records assembly of explicitly supplied closed-model results; the input assessment is unchanged and no scenario ran during assembly.")
        matrix[key.value] = entry
    payload["capabilities"] = matrix
    payload["observability"] = {"maximum_level": bundle.observability.maximum_level,
        "level_label": LEVEL_LABELS[bundle.observability.maximum_level], "basis": list(bundle.observability.basis),
        "limitations": list(dict.fromkeys(bundle.observability.limitations + ("Input eligibility is distinct from executed analysis; Phase 5 lineage remains deferred.",))),
        "partial_evidence": list(dict.fromkeys(reason for capability in matrix.values() for reason in capability["reason_codes"])),
        "capabilities": matrix}


def _lineage_observations(payload, bundle):
    capability = bundle.observability.capabilities[CapabilityKey.LINEAGE]
    coverage = capability.coverage
    scope = payload["inputs"]["scope"]
    target = {}
    if coverage is not None:
        checked = _coverage(coverage)
        for name, count in (("declared_parent_edge_count", coverage.denominator),
                            ("resolved_parent_edge_count", coverage.numerator),
                            ("unresolved_parent_edge_count", coverage.denominator - coverage.numerator)):
            target[name] = _envelope("observed_facts.lineage." + name, count, scope, denominator=coverage.denominator,
                coverage=checked["ratio"], limitations=("Counts preserve validation reference-entry multiplicity; they do not describe an ancestry graph.",))
        payload["derived_metrics"]["lineage"] = {"resolved_parent_edge_coverage": _envelope(
            "derived_metrics.lineage.resolved_parent_edge_coverage", checked["ratio"], scope,
            denominator=coverage.denominator, coverage=checked["ratio"],
            status="unavailable" if checked["ratio"] is None else "available",
            reasons=("R_NO_DECLARED_PARENT_ENTRIES",) if checked["ratio"] is None else (),
            required=("declared_parent_reference_entries",) if checked["ratio"] is None else (),
            limitations=("Immediate-reference validation coverage does not establish resolved ancestry or external roots.",))}
    if "earlier_version_acyclicity_certificate" in capability.requirements_met:
        target["ordering_certificate"] = _envelope("observed_facts.lineage.ordering_certificate",
            {"method": "declared_earlier_version_order", "version_order": list(bundle.version_order.order),
             "all_resolved_edges_follow_order": True}, scope,
            limitations=("This retained earlier-version ordering certificate is not general graph-cycle traversal.",))
    target["cycle_status"] = _envelope("observed_facts.lineage.cycle_status", None, scope,
        status="unavailable", reasons=("R_GRAPH_EXECUTION_DEFERRED",), required=("Phase_5_graph_analysis",),
        limitations=("No general graph-cycle traversal executes in Phase 4.",))
    payload["observed_facts"]["lineage"] = target


def _bundle_check(bundle):
    _typed(bundle, BundleValidationResult, "validated bundle")
    _typed(bundle.version_order, VersionOrderResult, "retained version order")
    _typed(bundle.observability, ObservabilityAssessment, "observability assessment")
    _typed(bundle.provenance_join, ProvenanceJoinResult, "retained provenance join")
    if bundle.provenance is not None:
        _require(type(bundle.provenance) is tuple and all(type(row) in (CanonicalRow, ProvenanceAssessment) for row in bundle.provenance), "provenance input must retain exact row types")
        for row in bundle.provenance:
            _typed(row.record_key, RecordKey, "provenance record key")
            _typed(row.location, RowLocation, "provenance row location")
    if bundle.generation is not None:
        _typed(bundle.generation, GenerationValidationResult, "retained generation validation")
    _require(bundle.provenance is None or type(bundle.provenance) is tuple, "provenance rows require immutable accepted collection")
    for strings in (bundle.version_order.loaded_versions, bundle.version_order.order):
        _require(type(strings) is tuple and all(type(item) is str for item in strings), "version order must retain literal immutable declarations")
    _require(type(bundle.records) is tuple and all(type(row) is CanonicalRow for row in bundle.records), "bundle records require canonical row tuples")
    for row in bundle.records:
        _typed(row.record_key, RecordKey, "canonical record key")
        _require(type(row.values) in (dict, MappingProxyType), "canonical row values require retained literal data")
        _typed(row.location, RowLocation, "canonical row location")
    _require(type(bundle.inventory) is tuple and all(type(item) is FileInventoryEntry for item in bundle.inventory), "inventory requires exact immutable entries")
    for item in bundle.inventory:
        _typed(item.role, FileRole, "inventory role")
        _typed(item.file_format, FileFormat, "inventory format")
        _require(type(item.path) in (PosixPath, WindowsPath), "inventory path requires a literal concrete path")
    _require(type(bundle.validation_messages) is tuple and all(type(item) is ValidationMessage for item in bundle.validation_messages), "validation diagnostics require typed immutable entries")
    _require(type(bundle.mapping_traces) is tuple and all(type(item) is RowMappingEvidence for item in bundle.mapping_traces), "mapping traces require typed immutable entries")
    assessment = bundle.observability
    _require(type(assessment.maximum_level) is int and 0 <= assessment.maximum_level <= 5, "observability level is invalid")
    _require(type(assessment.capabilities) in (dict, MappingProxyType) and set(assessment.capabilities) == set(CapabilityKey), "bundle capability matrix is incomplete")
    for key, capability in assessment.capabilities.items():
        _typed(key, CapabilityKey, "capability family")
        _typed(capability, Capability, "input capability")
        _typed(capability.status, CapabilityStatus, "input capability status")
        if capability.coverage is not None:
            _coverage(capability.coverage)
        _require(type(capability.coverage_details) in (dict, MappingProxyType), "capability details require retained literal data")
        _require(all(type(name) is str for name in capability.coverage_details), "capability coverage names must be literal strings")
        for coverage in capability.coverage_details.values():
            _coverage(coverage)
        for strings in (capability.reason_codes, capability.requirements_met, capability.requirements_missing, capability.notes):
            _require(type(strings) is tuple and all(type(item) is str for item in strings), "capability text must be immutable literal strings")
    join = bundle.provenance_join
    _require(type(join.matches) is tuple and all(type(item) is ProvenanceMatch for item in join.matches), "join matches require exact immutable entries")
    _require(type(join.scope_record_keys) is tuple and type(join.missing_record_keys) is tuple and type(join.selected_dataset_versions) is tuple,
             "join scope requires immutable declarations")
    _require(type(join.provenance_supplied) is bool, "join availability must be boolean")
    keys = {row.record_key for row in bundle.records}
    _require(set(join.scope_record_keys) <= keys and len(set(join.scope_record_keys)) == len(join.scope_record_keys), "join scope identities leave validated records or duplicate")
    _require({match.record_key for match in join.matches} == set(join.scope_record_keys) and len(join.matches) == len(join.scope_record_keys), "join match inventory disagrees with scope")
    for match in join.matches:
        _typed(match.record_key, RecordKey, "join identity")
        if match.provenance is not None:
            row = match.provenance
            _typed(row, ProvenanceAssessment, "provenance assessment")
            _require(type(row.values) in (dict, MappingProxyType), "provenance fields require retained literal data")
            _require(all(row.values.get(field) is None or type(row.values.get(field)) is str for field in ("source_type", "external_grounding", "provenance_confidence")), "provenance enum fields must contain literal strings")
            _require(row.record_key == match.record_key and type(row.required_fields_valid) is bool and type(row.grounding_known) is bool,
                     "provenance assessment identity or flag type disagrees")
    _require(set(join.missing_record_keys) == {match.record_key for match in join.matches if match.provenance is None}, "missing provenance identities disagree with matches")
    for coverage, numerator in ((join.provenance_row_coverage, sum(match.provenance is not None for match in join.matches)),
                               (join.provenance_required_field_coverage, sum(match.provenance is not None and match.provenance.required_fields_valid for match in join.matches)),
                               (join.grounding_field_coverage, sum(match.provenance is not None and match.provenance.grounding_known for match in join.matches))):
        _coverage(coverage)
        _require(coverage.numerator == numerator and coverage.denominator == len(join.scope_record_keys), "join coverage contradicts retained match inventory")


def assemble_report(bundle: BundleValidationResult, *, run: dict,
                    distributions: tuple[StateDistributionResult | DistributionMetrics, ...] = (),
                    provenance: ProvenanceCompositionResult | None = None,
                    duplicates: ExactDuplicateResult | None = None,
                    tail: TailSelectionResult | None = None,
                    comparison: SupportComparison | None = None,
                    closure: DirectClosureExposureBounds | None = None,
                    expected_diversity: ExpectedDiversityResult | None = None,
                    resampling: ResamplingSimulation | None = None,
                    extinction: tuple[ExtinctionProbabilityResult, ...] = (),
                    family_errors: tuple[FamilyFailure, ...] = ()) -> CanonicalReport:
    """Adapt explicit typed evidence; never run an analysis or resolve input files.

    Caller supplies complete standard-mode run metadata. Mathematical probability
    inputs and scenarios retain their own declared scopes; empirical results must
    bind to validated bundle identities. Each singleton family has one report slot.
    """
    _bundle_check(bundle)
    _require(type(run) is dict, "run metadata must be a public JSON object")
    _require(run.get("privacy_mode") == "standard" and run.get("redacted_mode") is False,
             "Step 3 assembles standard evidence; a redacted declaration requires the later privacy transform")
    _require(type(bundle.records) is tuple and all(type(row) is CanonicalRow for row in bundle.records), "bundle records require canonical row tuples")
    _require(len({row.record_key for row in bundle.records}) == len(bundle.records), "bundle record identities are duplicated")
    _require(set(bundle.version_order.loaded_versions) == {row.record_key.dataset_version for row in bundle.records}, "bundle loaded versions disagree with validated records")
    _require(set(bundle.observability.capabilities) == set(CapabilityKey), "bundle capability matrix is incomplete")
    _require(type(distributions) is tuple and type(extinction) is tuple and type(family_errors) is tuple, "explicit result collections require immutable tuples")
    _require(expected_diversity is None or resampling is None, "one closed-resampling report slot cannot hold two different method results")
    payload = {key: {} if index < 8 else [] for index, key in enumerate(SECTION_ORDER)}
    payload["run"] = dict(run)
    _inputs(payload, bundle)
    operations = {key.value: [] for key in CapabilityKey}
    operations["ingestion"] = ["existing_bundle_validation"] if bundle.inventory or bundle.records else []
    failures = {}
    for failure in family_errors:
        _typed(failure, FamilyFailure, "family failure")
        FamilyFailure(failure.capability, failure.messages)
        failures.setdefault(failure.capability.value, []).extend(failure.messages)
        _diagnostics(payload, failure.messages, failure.capability.value)
    empirical_representations = []
    for supplied in distributions:
        if type(supplied) is StateDistributionResult:
            _coverage(supplied.coverage)
            _require(supplied.coverage.denominator == len(supplied.unweighted.scope.included_record_keys + supplied.unweighted.scope.excluded_record_keys) and
                     supplied.coverage.numerator == len(supplied.unweighted.scope.included_record_keys), "distribution coverage differs from its selected record scope")
            _distribution(payload, supplied.unweighted, bundle, coverage=supplied.coverage.ratio)
            if supplied.weighted is not None:
                _require(supplied.weighted.scope == supplied.unweighted.scope and supplied.weighted.representation == supplied.unweighted.representation,
                         "weighted companion must preserve unweighted scope and representation")
                _distribution(payload, supplied.weighted, bundle, weighted=True, coverage=supplied.coverage.ratio)
            _distribution_exclusions(payload, supplied)
            _diagnostics(payload, supplied.selection_messages, "content_diagnostics")
            empirical_representations.append(supplied.unweighted.representation)
        else:
            _distribution(payload, supplied, bundle)
            if supplied.input_basis != "explicit_probability_vector":
                empirical_representations.append(supplied.representation)
        operations["content_diagnostics"].append("supplied_distribution:" + (supplied.unweighted.scope.scope_id if type(supplied) is StateDistributionResult else supplied.scope.scope_id))
    if provenance is not None:
        _provenance(payload, provenance, bundle)
        _diagnostics(payload, provenance.validation_messages, "provenance")
        operations["provenance"].append("supplied_provenance_composition:" + provenance.scope.scope_id)
    if duplicates is not None:
        _duplicates(payload, duplicates, bundle)
        operations["content_diagnostics"].append("supplied_exact_duplicates:" + duplicates.scope.scope_id)
        empirical_representations.append(duplicates.representation)
    if tail is not None:
        _tail(payload, tail, bundle)
        operations["content_diagnostics"].append("supplied_declared_tail:" + tail.scope.scope_id)
        empirical_representations.append(tail.representation)
    if comparison is not None:
        _comparison(payload, comparison, bundle)
        operations["dataset_longitudinal"].append("supplied_explicit_pair_support_and_diversity")
    if closure is not None:
        _closure(payload, closure, bundle, provenance)
        _diagnostics(payload, closure.validation_messages, "provenance")
        operations["provenance"].append("supplied_direct_closure_interval:" + closure.scope.scope_id)
    if expected_diversity is not None:
        _closed_simulation(payload, expected_diversity)
        operations["intervention_simulation"].append("supplied_analytic_closed_resampling")
    if resampling is not None:
        _closed_simulation(payload, resampling)
        operations["intervention_simulation"].append("supplied_sampled_closed_resampling")
    if extinction:
        _extinction(payload, extinction)
        operations["intervention_simulation"].append("supplied_one_step_extinction_marginals")
    if empirical_representations and all(item == empirical_representations[0] for item in empirical_representations):
        payload["inputs"]["representation"] = _representation(empirical_representations[0])
    elif empirical_representations:
        payload["inputs"]["limitations"].append("Supplied calculation families use multiple explicit representations; inspect each result envelope.")
    _lineage_observations(payload, bundle)
    _capabilities(payload, bundle, operations, failures)
    if payload["errors"]:
        payload["run"]["run_status"] = "failed" if any(error["severity"] == "fatal" for error in payload["errors"]) else "partial" if bundle.records or distributions or payload["simulations"] else "failed"
        for error in payload["errors"]:
            error["effect_on_run"] = payload["run"]["run_status"]
    _disclosures(payload)
    return CanonicalReport.from_dict(payload)


def _disclosure_scope(payload):
    return payload["inputs"].get("scope", {
        "dataset_versions": [], "record_count": None,
        "excluded_record_count": None,
        "denominator_basis": "no_selected_record_scope_supplied",
        "scope_id": "report_inputs",
    })


def _disclosure_base(owner, evidence_class, method, scope, basis=None):
    return {
        "unit": "signal" if evidence_class == "proxy_signal" else "conclusion",
        "evidence_class": evidence_class,
        "status": "available" if evidence_class == "proxy_signal" else "unavailable",
        "method_id": method, "owner_ids": [owner], "theory_map_ids": [],
        "trace_ids": [owner] if owner in ("T1", "T2", "T3", "T4", "T5", "T6") else [],
        "scope": scope,
        "representation": basis["representation"] if basis is not None else None,
        "coverage": basis["coverage"] if basis is not None else None,
        "coverage_reason": basis["coverage_reason"] if basis is not None else "This conclusion has no measured evidence coverage.",
        "denominator": basis["denominator"] if basis is not None else None,
        "denominator_reason": basis["denominator_reason"] if basis is not None else "This conclusion has no scalar denominator.",
        "assumptions": [], "limitations": [], "reason_codes": [],
        "required_evidence": [],
    }


def _disclosure_signal(name, owner, basis, paths, present, rule, limitations):
    result = _disclosure_base(owner, "proxy_signal", owner + "." + name,
                              basis["scope"], basis)
    result.update({
        "signal": name, "level": "present" if present else "not_present",
        "basis_fields": paths, "trigger_rule": rule,
        "assumptions": list(basis["assumptions"]),
        "limitations": list(dict.fromkeys(list(basis["limitations"]) + limitations)),
    })
    return result


def _disclosure_unavailable(payload, name, owner, capability, statement,
                            reasons, blockers, next_metadata, limit):
    result = _disclosure_base(owner, "unavailable_conclusion",
                              owner + ".unavailable_conclusion", _disclosure_scope(payload))
    result.update({
        "conclusion": name, "statement": statement, "reason_codes": reasons,
        "required_evidence": next_metadata, "blocking_evidence": blockers,
        "required_next_metadata": next_metadata, "related_capability": capability,
        "theory_or_product_limit": limit,
        "limitations": [
            "Unavailable means the supplied evidence does not support this conclusion; it does not establish that the conclusion is false."
        ],
    })
    payload["unavailable_conclusions"].append(result)


def _disclosure_recommend(payload, priority, metadata, scope, unlock, reason):
    payload["recommended_next_metadata"].append({
        "priority": priority, "metadata": metadata, "scope": scope,
        "expected_unlock": unlock, "reason": reason, "owner_ids": ["PR-014"],
    })


def _disclosures(payload):
    """Add registered disclosures; preserve absent evidence without zero filling."""
    derived = payload["derived_metrics"]
    support = derived.get("support", {})
    delta = support.get("support_delta")
    if delta is not None and delta["status"] in ("available", "partial"):
        paths = ["derived_metrics.support.support_delta"]
        if "extinct_states" in support:
            paths.append("derived_metrics.support.extinct_states")
        if "comparison_details" in support:
            paths.append("derived_metrics.support.comparison_details")
        payload["proxy_signals"]["support_contraction"] = _disclosure_signal(
            "support_contraction", "T1", delta, paths, delta["value"] < 0,
            "Present exactly when the supplied validated explicit-pair support delta is negative.",
            ["The signal is restricted to the selected versions and their declared common state meaning.",
             "An observed support decrease does not establish model-performance decline, production failure or universal collapse."],
        )
    tail = derived.get("tail", {})
    size = tail.get("tail_support_size")
    if size is not None and size["status"] in ("available", "partial") and "selection" in tail:
        payload["proxy_signals"]["tail_fragility"] = _disclosure_signal(
            "tail_fragility", "T2", size,
            ["derived_metrics.tail.tail_support_size", "derived_metrics.tail.selection"],
            size["value"] > 0,
            "Present exactly when at least one observed state is selected by the caller's declared tail rule.",
            ["Tail membership depends on the explicit rule and selected representation.",
             "This signal is not a calibrated forecast of the production pipeline.",
             "No simulation is run by this signal, and tail membership does not establish importance or harm."],
        )
    provenance = payload["observed_facts"].get("provenance", {})
    direct = derived.get("closure_exposure", {}).get("direct", {})
    width = direct.get("interval_width")
    basis = []
    present = False
    if width is not None and width["status"] in ("available", "partial"):
        basis.append(("derived_metrics.closure_exposure.direct.interval_width", width))
        present = width["value"] > 0
    for key in ("provenance_row_coverage", "provenance_required_field_coverage", "grounding_field_coverage"):
        item = provenance.get(key)
        if (item is not None and item["status"] in ("available", "partial")
                and (not basis or item["scope"] == basis[0][1]["scope"])):
            basis.append(("observed_facts.provenance." + key, item))
            present = present or item["value"] < 1
    if basis:
        payload["proxy_signals"]["provenance_uncertainty"] = _disclosure_signal(
            "provenance_uncertainty", "T3", basis[0][1], [item[0] for item in basis], present,
            "Present when a supplied direct closure interval has positive width or a supplied provenance row, required-field or grounding coverage is below one.",
            ["Each coverage keeps its own field meaning and denominator.",
             "This signal reports unresolved supplied provenance evidence and does not estimate factual truth or source independence.",
             "A not_present signal is limited to the cited fields and does not certify universal integrity."],
        )
    # No shared_ancestry_dependence proxy: P4-D01 prohibits Phase 4 ancestry inference.
    _disclosure_unavailable(
        payload, "model_performance_decline", "PR-014", "model_longitudinal",
        "The supplied audit evidence cannot establish model-performance decline.",
        ["R_MODEL_EVIDENCE_MISSING"], ["No accepted versioned model-outcome analysis is supplied."],
        ["Versioned model evaluation outcomes with comparable tasks and evaluation conditions."],
        "Dataset structure does not measure model performance.",
    )
    _disclosure_unavailable(
        payload, "causal_ancestor_effect", "T4", "lineage",
        "A causal effect of an ancestor is unavailable.",
        ["R_CAUSAL_EVIDENCE_MISSING", "R_LINEAGE_EXECUTION_DEFERRED"],
        ["Phase 4 does not compute ancestry; topology alone would not identify a causal contribution."],
        ["An identified ancestor, measured outcomes and a controlled or otherwise justified causal design."],
        "Parent declarations and graph topology do not establish causal effects.",
    )
    _disclosure_unavailable(
        payload, "universal_integrity", "PR-014", "provenance",
        "Universal integrity is unavailable.", ["R_UNIVERSAL_OPERATIONAL_DEFINITION_ABSENT"],
        ["This product defines no universal integrity scalar or operational test."],
        ["A bounded operational definition and evidence matched to that definition."],
        "A domain-specific future audit does not unlock a universal integrity claim.",
    )
    _disclosure_unavailable(
        payload, "universal_collapse_prediction", "PR-014", "model_longitudinal",
        "Universal collapse prediction is unavailable.", ["R_OUTSIDE_PRODUCT_SCOPE"],
        ["No universal collapse prediction is defined by the approved toolkit."],
        ["A separately defined bounded outcome and appropriately validated predictive evidence."],
        "No additional metadata by itself unlocks universal collapse prediction in this product.",
    )
    if any(key in derived for key in ("support", "diversity", "tail")):
        _disclosure_unavailable(
            payload, "production_failure", "T1", "content_diagnostics",
            "The supplied structural measurements cannot establish production failure.",
            ["R_OUTCOME_EVIDENCE_MISSING"], ["No operational failure outcome is measured by these structural fields."],
            ["A stated production-failure criterion and corresponding versioned outcome measurements."],
            "Represented support, diversity and tail membership do not measure functional failure.",
        )
    _disclosure_unavailable(
            payload, "complete_pipeline_closure", "T3", "provenance",
            "Complete pipeline closure is unavailable from direct grounding declarations.",
            ["R_PIPELINE_BOUNDARY_EVIDENCE_MISSING"],
            ["Direct closure exposure describes the selected declared grounding scope, without tracing every pipeline input."],
            ["An explicit pipeline boundary and evidence for its relevant external inputs and transformations."],
            "Even a direct closure interval of [1, 1] does not certify complete pipeline closure.",
        )
    lineage = payload["capabilities"].get("lineage")
    if lineage is not None:
        reasons = ["R_LINEAGE_EXECUTION_DEFERRED"]
        if lineage["status"] != "available":
            reasons.extend(reason for reason in lineage["reason_codes"] if reason not in reasons)
        for name, owner, statement in (
            ("lineage_analysis", "PR-014", "General lineage graph analysis is deferred to Phase 5."),
            ("lineage_closure_exposure", "T3", "Lineage closure exposure is deferred to Phase 5."),
            ("external_ancestry", "T4", "External ancestry results are deferred to Phase 5."),
        ):
            _disclosure_unavailable(
                payload, name, owner, "lineage", statement, list(reasons),
                ["Only existing reference validation observations can be reported; no graph traversal, root tracing or ancestry metric executes."],
                ["Preserve explicit composite parent references, chronology and external-grounding metadata for the future Phase 5 analysis."],
                "Implementation is deferred even when the existing input classifier marks lineage available.",
            )
    if payload["simulations"]:
        _disclosure_unavailable(
            payload, "empirical_intervention_effect", "T5", "intervention_simulation",
            "An empirical intervention effect is unavailable from supplied scenarios.",
            ["R_CONTROLLED_EMPIRICAL_DESIGN_MISSING"],
            ["Supplied scenario outputs are conditional mathematical or stochastic results."],
            ["A controlled empirical intervention design with measured comparable outcomes."],
            "A closed-resampling scenario does not establish production causality or an intervention effect.",
        )
    missing_rows = provenance.get("missing_provenance_count")
    row_coverage = provenance.get("provenance_row_coverage")
    row_gap = (missing_rows is not None and missing_rows["value"] is not None and missing_rows["value"] > 0)
    row_gap = row_gap or (row_coverage is not None and row_coverage["value"] is not None and row_coverage["value"] < 1)
    if row_gap:
        _disclosure_recommend(payload, 1, "matching_provenance_rows", "records with no matching provenance row",
                              ["more complete declared provenance coverage"],
                              "The supplied provenance result explicitly identifies missing matching rows.")
    for key, metadata, scope, unlock in (
        ("provenance_required_field_coverage", "required_provenance_fields", "records lacking usable required provenance",
         "usable declared provenance without discarding independently valid calculations"),
        ("grounding_field_coverage", "external_grounding", "records whose grounding remains unresolved",
         "a narrower direct closure exposure interval when the additional evidence resolves grounding"),
    ):
        item = provenance.get(key)
        if item is not None and item["value"] is not None and item["value"] < 1:
            _disclosure_recommend(payload, 1, metadata, scope, [unlock],
                                  "The corresponding supplied field coverage is incomplete.")
    content_cap = payload["capabilities"].get("content_diagnostics", {})
    longitudinal_cap = payload["capabilities"].get("dataset_longitudinal", {})
    reasons = set(content_cap.get("reason_codes", ())) | set(longitudinal_cap.get("reason_codes", ()))
    if "R_REPRESENTATION_NOT_DECLARED" in reasons and not any(key in derived for key in ("support", "diversity", "tail")):
        _disclosure_recommend(payload, 2, "explicit_representation", "the selected calculation scope",
                              ["representation-dependent support, diversity and tail diagnostics"],
                              "No representation is declared; assembly does not select a field or hash fallback.")
    if "R_VERSION_ORDER_MISSING" in reasons:
        _disclosure_recommend(payload, 2, "version_order", "the intended earlier and later versions",
                              ["eligibility for an explicitly requested comparison after state-meaning compatibility is supplied"],
                              "The supplied capability assessment identifies missing chronology.")
    if lineage is not None and any(reason in lineage["reason_codes"] for reason in ("R_PARENT_UNRESOLVED", "R_PARENT_AMBIGUOUS", "R_PARENT_DECLARATION_MISSING", "R_PARENT_INVALID")):
        _disclosure_recommend(payload, 3, "composite_parent_references", "records with unresolved or invalid parent declarations",
                              ["more complete immediate-parent validation; future Phase 5 analysis remains deferred"],
                              "The existing classifier identifies incomplete or invalid parent evidence.")
    _disclosure_recommend(payload, 4, "versioned_model_outcomes", "models and comparable evaluation conditions",
                          ["evidence needed by a future model-longitudinal implementation"],
                          "Dataset audit fields do not supply model-performance outcomes.")


# PR-015: exact public literals from the accepted Step 3 assembly and input
# capability owners. Unknown caller prose never becomes trusted by a prefix,
# regular expression, or similarity to one of these reviewed literal strings.
_PRIVACY_SAFE_TEXT = frozenset((
    'earlier_positive_mass_support_in_harmonized_representation',
    'explicit_version_order',
    'identifier_secret_file_path',
    '\x00',
    ' -> ',
    ' is above its accepted bound',
    ' is below its accepted bound',
    ' must be a built-in number',
    ' must be finite',
    ' requires its exact accepted result type',
    '(known_closed_count + unresolved_grounding_count) / total_record_count',
    '.',
    '.by_version.*.',
    '.unavailable_conclusion',
    ': ',
    '; selected counts / included records',
    'A bounded operational definition and evidence matched to that definition.',
    'A causal effect of an ancestor is unavailable.',
    'A closed-resampling scenario does not establish production causality or an intervention effect.',
    'A coarsened comparison cannot recover distinctions lost through its mapping.',
    'A controlled empirical intervention design with measured comparable outcomes.',
    'A domain-specific future audit does not unlock a universal integrity claim.',
    'A not_present signal is limited to the cited fields and does not certify universal integrity.',
    'A separately defined bounded outcome and appropriately validated predictive evidence.',
    'A stated production-failure criterion and corresponding versioned outcome measurements.',
    'A supplied handoff cannot be represented without overstating its evidence.',
    'A zero-frequency boundary case describes continued absence, not a newly observed loss.',
    'Accepted input round-off is corrected only by division by its validated total.',
    'Accepted round-off residuals are disclosed and left unchanged.',
    'Add registered disclosures; preserve absent evidence without zero filling.',
    'All selected valid records',
    'An empirical intervention effect is unavailable from supplied scenarios.',
    'An explicit family failure, kept alongside independently usable evidence.',
    'An explicit pipeline boundary and evidence for its relevant external inputs and transformations.',
    'An identified ancestor, measured outcomes and a controlled or otherwise justified causal design.',
    'An observed support decrease does not establish model-performance decline, production failure or universal collapse.',
    'Analytic input residuals within the approved tolerance are disclosed and left unchanged.',
    'Approved direct grounding partition; uncertainty remains unresolved.',
    'Bit-identical paths across dependency versions or platforms are not promised.',
    'Categorical multinomial sampling; positive explicit n; one-step horizon; no external reopening.',
    'Chronology alone does not establish lineage, causality or functional failure.',
    'Complete pipeline closure is unavailable from direct grounding declarations.',
    'Conditional on the supplied current frequency and the closed multinomial model.',
    'Confidence remains separate; no lineage, midpoint, threshold or causal claim.',
    'Content hashes remain linkable; this internal result is not a redacted report.',
    'Count-backed unweighted records only; probability-only vectors do not supply record shares.',
    'Counts preserve validation reference-entry multiplicity; they do not describe an ancestry graph.',
    'Coverage uses selected valid records; provenance scope is unchanged.',
    'Dataset audit fields do not supply model-performance outcomes.',
    'Dataset structure does not measure model performance.',
    'Dataset versions do not establish model-performance change.',
    'Declared composition does not certify input validity or increase observability.',
    'Declared zero-count states are outside observed support and are not ranked.',
    'Definitions 10.1-10.6; explicit ',
    'Definitions 10.1-10.6; explicit count_at_or_below',
    'Definitions 10.1-10.6; explicit count_at_or_below; selected counts / included records',
    'Definitions 10.1-10.6; explicit frequency_at_or_below',
    'Definitions 10.1-10.6; explicit frequency_at_or_below; selected counts / included records',
    'Definitions 10.1-10.6; explicit singleton_count',
    'Definitions 10.1-10.6; explicit singleton_count; selected counts / included records',
    'Definitions 10.1-10.6; explicit state_list',
    'Definitions 10.1-10.6; explicit state_list; selected counts / included records',
    'Definitions 11.4/19; missing-row mass / all selected record weight mass',
    'Definitions 11.4; missing rows / all selected valid records',
    'Definitions 19; all selected weights',
    'Definitions 19; missing-row mass',
    'Definitions 19; sum explicit weights by source',
    'Definitions 3.13; nonmissing valid field / all selected valid records',
    'Definitions 3.3/11.1; count declared canonical categories',
    'Definitions 7.1; ',
    'Definitions 7.1; empirical_assignments',
    'Definitions 7.1; explicit_counts_divided_by_included_records',
    'Definitions 7.1; explicit_probability_vector',
    'Definitions 7.1; weighted_record_mass',
    'Definitions 9.5; canonical record weights summed within each state',
    'Direct classes are relative to supplied grounding about the audited loop.',
    'Direct closure exposure describes the selected declared grounding scope, without tracing every pipeline input.',
    'Direct exposure is relative to the audited loop and supplied metadata.',
    'Distributional concentration does not establish functional failure.',
    'Diversity contraction holds in expectation, not monotonically on every sampled path.',
    'E_CONFIG_INVALID',
    'E_CONTENT_REF_MISSING',
    'E_CONTENT_REF_OUTSIDE_BASE',
    'E_EMPTY_DATASET',
    'E_FILE_ENCODING',
    'E_FILE_FORMAT_UNSUPPORTED',
    'E_FILE_NOT_FOUND',
    'E_FILE_PARSE',
    'E_LINEAGE_CYCLE',
    'E_MAPPING_SOURCE_FIELD_MISSING',
    'E_MAPPING_TARGET_COLLISION',
    'E_MAPPING_UNSAFE_TRANSFORM',
    'E_PARENT_AMBIGUOUS',
    'E_PARENT_FORMAT',
    'E_PARENT_FUTURE_VERSION',
    'E_PROVENANCE_DUPLICATE_ROW',
    'E_PROVENANCE_UNMATCHED_ROW',
    'E_RECORD_DUPLICATE_ID',
    'E_RECORD_EMPTY_CONTENT',
    'E_REPRESENTATION_INCOMPATIBLE',
    'E_SCHEMA_ENUM',
    'E_SCHEMA_REQUIRED_FIELD',
    'E_SCHEMA_TYPE',
    'E_VERSION_ORDER_CONFLICT',
    'E_WEIGHT_INVALID',
    'Each coverage keeps its own field meaning and denominator.',
    'Earlier and later scopes explicitly selected and independently validated.',
    'Even a direct closure interval of [1, 1] does not certify complete pipeline closure.',
    'Exact explicit single-version Phase 2 join scope; no representation exclusions.',
    'Exact record form does not establish semantic identity or independent origin.',
    'Exact record form does not establish semantic identity, authorship or independent origin.',
    'Executed only the supplied explicit-pair support/diversity comparison; no adjacent-pair discovery, lineage/provenance trajectory or relative-change calculation.',
    'Execution records assembly of explicitly supplied closed-model results; the input assessment is unchanged and no scenario ran during assembly.',
    'Experimental conditional simulation; no calibrated production-failure probability.',
    'Experimental scenario eligibility only; no simulation has run.',
    'Explicit directed state aggregation changes this basis; inspect original distributions separately.',
    'Explicit rule over positive observed unweighted count support.',
    'External ancestry results are deferred to Phase 5.',
    'Extinct means absent from the supplied later support in the harmonized representation.',
    'Extinction events are not separately inferred by the assembly adapter; inspect the supplied sampled support paths.',
    'F-',
    'F-001',
    'F-002',
    'F-003',
    'F-007 weighted variant; category mass / all selected record weight mass',
    'F-014',
    'F-014; (1-p_i)^n; analytic one-step closed multinomial',
    'F-015',
    'Fixed finite declared state space and constant positive integer resample size.',
    'Floating-point and pseudorandom sampling are numerical realizations of the declared model.',
    'General graph validation is deferred; no roots or ancestors are traced.',
    'General lineage graph analysis is deferred to Phase 5.',
    'Immediate-reference validation coverage does not establish resolved ancestry or external roots.',
    'Implementation is deferred even when the existing input classifier marks lineage available.',
    'Incomplete required provenance remains unresolved with original errors retained.',
    'Input eligibility is distinct from executed analysis; Phase 5 lineage remains deferred.',
    'Input eligibility only; downstream analytical implementations remain deferred.',
    'Input hashes identify supplied bytes and do not certify authenticity.',
    'Lineage closure exposure is deferred to Phase 5.',
    'Literal declared field labels do not certify semantic validity.',
    'Many-to-one mapping can conceal original distinctions; original inputs remain separately visible.',
    'Many-to-one mapping can hide original distinctions; original bases remain separately visible.',
    'No accepted versioned model-outcome analysis is supplied.',
    'No additional metadata by itself unlocks universal collapse prediction in this product.',
    'No cross-version metric or state mapping executes here.',
    'No external-reference loss, reopening, lineage, risk score or audit workflow is implemented.',
    'No frequencies or analytical metrics have been calculated.',
    'No general graph-cycle traversal executes in Phase 4.',
    'No implicit pooling, probability repair, confidence weighting or sampling.',
    'No independent truth, source independence, ancestry or complete closure is certified.',
    'No mutation, migration, independent real data or external corrective input.',
    'No operational failure outcome is measured by these structural fields.',
    'No permanent process extinction, causality, model-performance or source-independence claim follows.',
    'No representation is declared; assembly does not select a field or hash fallback.',
    'No simulation is run by this signal, and tail membership does not establish importance or harm.',
    'No source, grounding, independence, ancestry or model-performance claim follows.',
    'No universal collapse prediction is defined by the approved toolkit.',
    'Observed/supplied support only; no permanent extinction or causal/model-performance verdict.',
    'One explicitly selected earlier/later pair only; no trajectory or automatic adjacent comparison.',
    'One explicitly selected version and declared representation.',
    'One step only; no training-epoch countdown or calibrated production-failure forecast.',
    'Only allowlisted evidence fields are assembled; raw content, extras, notes and embeddings are not exported.',
    'Only existing reference validation observations can be reported; no graph traversal, root tracing or ancestry metric executes.',
    'PR-006',
    'PR-014',
    'Parent declarations and graph topology do not establish causal effects.',
    'Phase 2 matched-row inventory',
    'Phase 2 missing-row inventory',
    'Phase 4 does not compute ancestry; topology alone would not identify a causal contribution.',
    'Phase_5_graph_analysis',
    "Present exactly when at least one observed state is selected by the caller's declared tail rule.",
    'Present exactly when the supplied validated explicit-pair support delta is negative.',
    'Present when a supplied direct closure interval has positive width or a supplied provenance row, required-field or grounding coverage is below one.',
    'Preserve explicit composite parent references, chronology and external-grounding metadata for the future Phase 5 analysis.',
    'R_ANALYSIS_NOT_REQUESTED',
    'R_CALC_ALL_EXCLUDED',
    'R_CALC_CONTENT_UNAVAILABLE',
    'R_CALC_EMPTY_SCOPE',
    'R_CALC_NUMERICAL_INPUT_INVALID',
    'R_CALC_ORDER_MISSING',
    'R_CALC_PROVENANCE_FIELD_UNAVAILABLE',
    'R_CALC_REPRESENTATION_INCOMPATIBLE',
    'R_CALC_REPRESENTATION_MISSING',
    'R_CALC_UNSUPPORTED_OPTION',
    'R_CALC_WEIGHT_BASIS_INVALID',
    'R_CAUSAL_EVIDENCE_MISSING',
    'R_CONTENT_REFERENCE_UNAVAILABLE',
    'R_CONTROLLED_EMPIRICAL_DESIGN_MISSING',
    'R_GRAPH_EXECUTION_DEFERRED',
    'R_GRAPH_VALIDATION_DEFERRED',
    'R_GROUNDING_UNKNOWN',
    'R_INPUT_PARTIAL',
    'R_INPUT_VALIDATION_ERROR',
    'R_INVENTORY_ONLY_ROLE',
    'R_LINEAGE_EXECUTION_DEFERRED',
    'R_LONGITUDINAL_FAMILIES_DEFERRED',
    'R_MODEL_ANALYSIS_DEFERRED',
    'R_MODEL_EVIDENCE_MISSING',
    'R_MODEL_EVIDENCE_VALIDATION_DEFERRED',
    'R_NO_ANALYZABLE_CONTENT',
    'R_NO_DECLARED_PARENT_ENTRIES',
    'R_NO_PARENT_PATH',
    'R_NO_VALID_PROVENANCE_ROW',
    'R_OUTCOME_EVIDENCE_MISSING',
    'R_OUTSIDE_PRODUCT_SCOPE',
    'R_PARENT_AMBIGUOUS',
    'R_PARENT_DECLARATION_MISSING',
    'R_PARENT_INVALID',
    'R_PARENT_UNRESOLVED',
    'R_PIPELINE_BOUNDARY_EVIDENCE_MISSING',
    'R_PROVENANCE_NOT_SUPPLIED',
    'R_PROVENANCE_PARTIAL',
    'R_REPRESENTATION_FIELD_MISSING',
    'R_REPRESENTATION_INCOMPATIBLE',
    'R_REPRESENTATION_MAPPING_DEFERRED',
    'R_REPRESENTATION_NOT_DECLARED',
    'R_REPRESENTATION_PARTIAL',
    'R_REPRESENTATION_VALIDATION_DEFERRED',
    'R_ROOT_GROUNDING_UNAVAILABLE',
    'R_SCENARIO_DISTRIBUTION_MISSING',
    'R_SCENARIO_EXECUTION_DEFERRED',
    'R_SCENARIO_NOT_CONFIGURED',
    'R_SCENARIO_PARAMETERS_INVALID',
    'R_SCENARIO_PARAMETERS_MISSING',
    'R_SEMANTIC_EVIDENCE_MISSING',
    'R_SINGLE_VERSION',
    'R_UNIVERSAL_OPERATIONAL_DEFINITION_ABSENT',
    'R_VERSION_ORDER_MISSING',
    'Rarity does not establish importance, harm, production failure or permanent extinction.',
    'Raw content and exact record form do not certify semantic capability.',
    'Record-form support and declared field support do not certify semantic coverage.',
    'Reference-entry resolution coverage is not ancestry or external-root coverage.',
    'Reject contradicting handoffs using retained join observations only.',
    'Replay requires the same method, NumPy build/environment, seed and parameters.',
    'Representation exclusions cannot reduce the provenance denominator.',
    'Representation-bound; does not establish functional failure or semantic completeness.',
    'Representation-bound; no calibrated production-failure or universal risk conclusion.',
    'Representative selection never removes a source record or provenance row.',
    'Represented support, diversity and tail membership do not measure functional failure.',
    'Retain owner-supplied exclusion reasons without selecting records again.',
    'Reuse Phase 2 coverage; Definitions 3.10-3.12',
    'Simulated steps are not record generations, training epochs or dataset releases.',
    'Source, confidence, human review and grounding are independent declarations.',
    'State identity uses the declared common basis, including any disclosed map.',
    'State meaning is declared, not independently inferred or verified.',
    'Step 3 assembles standard evidence; a redacted declaration requires the later privacy transform',
    'Supplied calculation families use multiple explicit representations; inspect each result envelope.',
    'Supplied declarations only; no truth or source-independence certification.',
    'Supplied probability vectors remain mathematical inputs, not empirical record-frequency observations.',
    'Supplied scenario outputs are conditional mathematical or stochastic results.',
    'T',
    'T1',
    'T2',
    'T3',
    'T4',
    'T5',
    'T6',
    'Tail membership depends on the explicit rule and declared representation.',
    'Tail membership depends on the explicit rule and selected representation.',
    'The corresponding supplied field coverage is incomplete.',
    'The existing classifier identifies incomplete or invalid parent evidence.',
    'The input is a selected-state marginal; no complete empirical distribution is inferred.',
    'The signal is restricted to the selected versions and their declared common state meaning.',
    'The supplied audit evidence cannot establish model-performance decline.',
    'The supplied capability assessment identifies missing chronology.',
    'The supplied provenance result explicitly identifies missing matching rows.',
    'The supplied structural measurements cannot establish production failure.',
    'This conclusion has no measured evidence coverage.',
    'This conclusion has no scalar denominator.',
    'This product defines no universal integrity scalar or operational test.',
    'This retained earlier-version ordering certificate is not general graph-cycle traversal.',
    'This signal is not a calibrated forecast of the production pipeline.',
    'This signal reports unresolved supplied provenance evidence and does not estimate factual truth or source independence.',
    'Toolkit operationalization relative to supplied metadata, without lineage or truth certification.',
    'Toolkit operationalization; metadata can be incorrect and hidden dependencies unobserved.',
    'Unavailable means the supplied evidence does not support this conclusion; it does not establish that the conclusion is false.',
    'Underflow is disclosed; a rounded zero for an interior frequency is not impossibility.',
    'Universal collapse prediction is unavailable.',
    'Universal integrity is unavailable.',
    'Validate declared source-field readiness without creating state labels.',
    'Validate owner-authored method text before preserving it in public output.',
    'Validation coverage describes supplied declarations without certifying their truth.',
    'Validation notice ',
    'Versioned model evaluation outcomes with comparable tasks and evaluation conditions.',
    'W_CONTENT_ANALYSIS_UNAVAILABLE',
    'W_GENERATION_MISMATCH',
    'W_GROUNDING_UNKNOWN',
    'W_LONGITUDINAL_INCOMPATIBLE_REPRESENTATION',
    'W_MAPPING_VALUE_UNMAPPED',
    'W_OPTIONAL_FIELD_MISSING',
    'W_PARENT_BARE_COMPATIBILITY',
    'W_PARENT_DUPLICATE_REFERENCE',
    'W_PARENT_UNRESOLVED',
    'W_PARTIAL_LINEAGE',
    'W_PROVENANCE_ESTIMATED',
    'W_PROVENANCE_MISSING_ROW',
    'W_REPRESENTATION_FALLBACK',
    'W_VERSION_ORDER_MISSING',
    'Weighted support is positive weight mass, not unweighted record presence.',
    'X_t conditional on p_t is Multinomial(n,p_t); p_(t+1)=X_t/n.',
    '[redacted]',
    '_counts',
    '_field_coverage',
    'a narrower direct closure exposure interval when the additional evidence resolves grounding',
    'absolute_tolerance',
    'adapter field is absent from the frozen registry',
    'added_states',
    'affected_scope',
    'algorithm',
    'all_resolved_edges_follow_order',
    'all_selected_record_weight_mass',
    'all_valid_records',
    'all_valid_records_in_selected_dataset_scope',
    'all_validated_bundle_records',
    'analytic_expectation',
    'analytic_expectation; D0*(1-1/n)**t; t=0..steps; constant n',
    'analytic_extinction',
    'analyzed count disagrees with scope',
    'analyzed_record_count',
    'approved_model_performance_evidence',
    'artifact_index',
    'artifacts',
    'ascending frequency, then count, then Unicode state ID; 1-based ordinal',
    'ascending_unicode_state_id_skip_zero',
    'assumptions',
    'available',
    'basis',
    'basis_fields',
    'binning_or_mapping_rule',
    'blocking_evidence',
    'bundle capability matrix is incomplete',
    'bundle loaded versions disagree with validated records',
    'bundle record identities are duplicated',
    'bundle records require canonical row tuples',
    'by_state',
    'by_version',
    'calculation assumptions and limitations must remain immutable',
    'calculation evidence class or formula differs from the accepted adapter',
    'calculation metadata',
    'calculation metadata is detached from its enclosing scope or representation',
    'calculation name, owner or unit differs from the accepted adapter',
    'calculation scope',
    'calculation scope contains records outside the validated bundle',
    'calculation scope names unloaded versions',
    'calculation weighting differs from its enclosing result',
    'canonical record key',
    'canonical row location',
    'canonical row values must be plain or read-only dictionaries',
    'canonical row values require retained literal data',
    'capabilities',
    'capability coverage details require literal retained data',
    'capability coverage names must be literal strings',
    'capability details require retained literal data',
    'capability family',
    'capability text must be immutable literal strings',
    'cardinality of earlier support minus later support',
    'cardinality of later support minus earlier support',
    'category count / all selected valid records',
    'causal_ancestor_effect',
    'classification flags must be explicit booleans',
    'classification used an unregistered reason code',
    'classification_basis',
    'closed scenario evidence class or model was altered',
    'closed scenario requires its exact accepted type',
    'closed_categorical_v1',
    'closed_resampling',
    'closure confidence disclosure differs from supplied provenance',
    'closure coverage differs from supplied provenance',
    'closure denominator differs from selected scope',
    'closure input validity differs from supplied provenance',
    'closure_exposure',
    'code',
    'collision_groups',
    'comparison cannot mix incompatible weighting or probability/count bases',
    'comparison chronology differs from validated bundle order',
    'comparison compatibility',
    'comparison context differs from original inputs',
    'comparison diversity status mismatch',
    'comparison lacks explicit earlier/later chronology',
    'comparison mixes weighting families',
    'comparison requires explicit state meanings',
    'comparison requires one distinct version per side',
    'comparison result scope differs from its ordered pair',
    'comparison scalar status mismatch',
    'comparison scope declaration changed',
    'comparison set metadata is incomplete',
    'comparison_details',
    'compatibility_method',
    'complete_pipeline_closure',
    'completed',
    'composite_parent_references',
    'conclusion',
    'confidence cannot discount grounding',
    'confidence_disclosure',
    'confirmed',
    'content',
    'content-read evidence does not match the record scope',
    'content-read evidence must be nonempty text without NUL',
    'content-read evidence must be valid UTF-8 text',
    'content_diagnostics',
    'content_hash',
    'content_mode must use ContentMode',
    'content_or_declared_field_available',
    'content_or_declared_representation',
    'content_ref',
    'contraction_factor',
    'correction',
    'correction_applied',
    'correction_method',
    'count',
    'count included record-state assignments',
    'count-backed distribution has missing counts',
    'count-backed distribution lacks count metadata',
    'count_at_or_below',
    'count_groups_of_size_greater_than_one; DEFINITIONS_AND_UNITS:8.4',
    'count_threshold',
    'coverage',
    'coverage denominator',
    'coverage numerator',
    'coverage numerator exceeds denominator',
    'coverage_details',
    'coverage_not_supplied_for_this_result',
    'coverage_not_supplied_or_empty_denominator',
    'coverage_reason',
    'cycle_status',
    'dataset_longitudinal',
    'dataset_version',
    'dataset_versions',
    'declared composition',
    'declared provenance composition',
    'declared_distributions',
    'declared_earlier_version_order',
    'declared_parent_edge_count',
    'declared_parent_reference_entries',
    'declared_unknown_grounding',
    'deferred',
    'denominator',
    'denominator_basis',
    'denominator_name',
    'denominator_not_applicable_or_unavailable',
    'denominator_reason',
    'derived_metrics',
    'derived_metrics.',
    'derived_metrics.closure_exposure.direct.',
    'derived_metrics.closure_exposure.direct.interval_width',
    'derived_metrics.diversity.by_version.*.',
    'derived_metrics.diversity.by_version.*.distribution_basis',
    'derived_metrics.diversity.by_version.*.weighted_state_masses',
    'derived_metrics.diversity.gini_simpson_diversity_delta',
    'derived_metrics.lineage.resolved_parent_edge_coverage',
    'derived_metrics.provenance.',
    'derived_metrics.provenance.missing_provenance_share',
    'derived_metrics.provenance.source_type_shares',
    'derived_metrics.support.',
    'derived_metrics.support.comparison_details',
    'derived_metrics.support.extinct_states',
    'derived_metrics.support.support_delta',
    'derived_metrics.tail.',
    'derived_metrics.tail.selection',
    'derived_metrics.tail.tail_support_size',
    'diagnostic collections must be immutable tuples',
    'diagnostic file role',
    'diagnostic severity requires accepted enum',
    'diagnostic text must be literal strings',
    'direct',
    'direct closure disagrees with supplied provenance basis',
    'direct closure exposure',
    'direct closure must preserve its operationalization label',
    'direct grounding basis',
    'direct_closure_exposure_',
    'direct_closure_exposure_interval_width',
    'direct_closure_exposure_lower_bound',
    'direct_closure_exposure_upper_bound',
    'directed state mapping',
    'distribution',
    'distribution companion weighting mismatch',
    'distribution coverage differs from its selected record scope',
    'distribution exclusions require accepted immutable assignments',
    'distribution scalar status disagrees with enclosing result',
    'distribution status and tables require their accepted types',
    'distribution weighting',
    'distribution_basis',
    'diversity',
    'divide_by_validated_total',
    'duplicate distribution for one version and weighting',
    'duplicate evidence class was altered',
    'duplicate group',
    'duplicate group count disagrees with typed groups',
    'duplicate group must retain unique members',
    'duplicate groups overlap or leave their scope',
    'duplicate provenance category',
    'duplicate record count disagrees with typed groups',
    'duplicate state table identity',
    'duplicate_group_count',
    'duplicate_record_count',
    'earlier',
    'earlier support intersect later support',
    'earlier support minus later support',
    'earlier_representation',
    'earlier_state_semantics',
    'earlier_to_later',
    'earlier_version',
    'earlier_version_acyclicity_certificate',
    'effect_on_capabilities',
    'effect_on_run',
    'effective_distribution',
    'effective_probability_total',
    'eligibility for an explicitly requested comparison after state-meaning compatibility is supplied',
    'embedding_cluster',
    'empirical_assignments',
    'empirical_assignments; n_i/N',
    'empirical_intervention_effect',
    'empty_scope',
    'error',
    'errors',
    'estimated',
    'evidence needed by a future model-longitudinal implementation',
    'evidence_class',
    'exact duplicates',
    'exact_duplicate_group_',
    'exact_duplicate_groups',
    'exact_utf8_v1',
    'exact_utf8_v1 and SHA-256; equal digests verified against exact bytes',
    'exclude',
    'excluded assignments must preserve their unavailable reason',
    'excluded_record_count',
    'excluded_record_keys',
    'exclusion inventory differs from calculation scope',
    'exclusions',
    'execution_reason_codes',
    'execution_scope',
    'execution_status',
    'existing_bundle_validation',
    'exp(resample_size * log1p(-state_frequency)); exact endpoints',
    'expected_diversity',
    'expected_gini_simpson_diversity',
    'expected_unlock',
    'experimental',
    'explicit pair context',
    'explicit result collections require immutable tuples',
    'explicit_configuration',
    'explicit_counts_divided_by_included_records',
    'explicit_directed_state_mapping',
    'explicit_missing_state',
    'explicit_order_and_compatible_representation',
    'explicit_probability_mass',
    'explicit_probability_vector',
    'explicit_representation',
    'explicit_scenario_activation',
    'explicit_supplied_state_probability_vector',
    'external_ancestry',
    'external_grounding',
    'external_input_distribution',
    'extinct_states',
    'extinction marginal basis or method was altered',
    'extinction marginal is unavailable or duplicated',
    'extinction marginals must share one explicit scenario basis',
    'extinction scenario declarations were altered',
    'extinction scenarios require an immutable nonempty tuple',
    'failed',
    'family failure',
    'family failure must retain error or fatal diagnostics',
    'family failure requires typed capability and immutable messages',
    'fatal',
    'field',
    'field representations require an explicit field',
    'field_name',
    'fields_affected',
    'file_hash',
    'file_hashes',
    'file_role',
    'format',
    'frequency denominator',
    'frequency_at_or_below',
    'frequency_denominator',
    'frequency_threshold',
    'generation',
    'generations',
    'gini_simpson_diversity',
    'gini_simpson_diversity_delta',
    'grounding',
    'grounding assignment contradicts retained provenance declarations',
    'grounding assignment identities differ from join',
    'grounding assignment types are invalid',
    'grounding assignments omit or invent scoped identities',
    'grounding assignments require exact immutable types',
    'grounding count',
    'grounding count contradicts typed assignments',
    'grounding input validity differs from provenance',
    'grounding partition differs from closure denominator',
    'grounding scope differs from provenance scope',
    'grounding_field_coverage',
    'group_id',
    'harmonization cannot replace input basis or denominators',
    'harmonization cannot replace selected record scopes',
    'harmonized earlier distribution',
    'harmonized later distribution',
    'harmonized representation differs from compatibility declaration',
    'harmonized_earlier_support',
    'harmonized_later_support',
    'harmonized_representation',
    'harmonized_state_semantics',
    'harmonized_support_size',
    'hash_algorithm',
    'human',
    'id_salt_file',
    'identical_declared_basis',
    'identifier_secret_material',
    'in_tail',
    'included_record_keys',
    'included_record_weight_mass',
    'included_representation_records',
    'incomplete capabilities must state a reason',
    'incomplete_required_provenance',
    'ingestion',
    'initial_distribution',
    'initial_gini_simpson_diversity',
    'input capability',
    'input capability status',
    'input diagnostics must use ValidationMessage objects',
    'input row must retain an accepted typed location',
    'input_basis',
    'input_normalization',
    'inputs',
    'intersection support size / earlier positive-mass support size',
    'interval_width',
    'intervention_simulation',
    'inventory format',
    'inventory path requires a literal concrete path',
    'inventory requires exact immutable entries',
    'inventory role',
    'invocation_order',
    'join availability must be boolean',
    'join coverage contradicts retained match inventory',
    'join coverage denominator differs from join scope',
    'join identity',
    'join match inventory disagrees with scope',
    'join matches require exact immutable entries',
    'join scope identities leave validated records or duplicate',
    'join scope requires immutable declarations',
    'known_closed',
    'known_closed_count',
    'known_closed_count / total_record_count',
    'known_open',
    'known_open_count',
    'label_field',
    'later',
    'later Gini-Simpson diversity minus earlier diversity',
    'later support minus earlier support',
    'later support_size minus earlier support_size',
    'later_representation',
    'later_state_semantics',
    'later_to_earlier',
    'later_version',
    'level',
    'level_label',
    'limitations',
    'line_number',
    'lineage',
    'lineage_analysis',
    'lineage_closure_exposure',
    'log_derived',
    'lower_bound',
    'mapped comparison has an unsupported method',
    'mapping effect side must be explicit',
    'mapping effects differ from retained original/harmonized results',
    'mapping harmonized target mismatch',
    'mapping representation or meaning mismatch',
    'mapping traces require typed immutable entries',
    'mapping_effect',
    'matching_provenance_rows',
    'maximum_level',
    'message',
    'metadata',
    'method',
    'method text differs from the accepted computation owner',
    'method_id',
    'missing provenance field cannot become a complete category table',
    'missing provenance identities disagree with matches',
    'missing_provenance_count',
    'missing_provenance_row',
    'missing_provenance_share',
    'missing_provenance_weight',
    'missing_state_id',
    'missing_value_policy',
    'mixed',
    'model',
    'model_longitudinal',
    'model_performance_decline',
    'model_version',
    'models and comparable evaluation conditions',
    'more complete declared provenance coverage',
    'more complete immediate-parent validation; future Phase 5 analysis remains deferred',
    'no',
    'no usable required-provenance row',
    'no valid records; no observability level can be certified',
    'no_selected_record_scope_supplied',
    'none',
    'nonempty_validated_record_scope',
    'normalization_divisor',
    'normalization_profile',
    'not_present',
    'not_requested',
    'notes',
    'numerator',
    'numerical policy',
    'numerical_policy',
    'numerical_underflow',
    'numerical_underflow_steps',
    'numpy_version',
    'observability',
    'observability assessment',
    'observability level is invalid',
    'observed_facts',
    'observed_facts.content.',
    'observed_facts.content.exact_duplicate_groups',
    'observed_facts.lineage.',
    'observed_facts.lineage.cycle_status',
    'observed_facts.lineage.ordering_certificate',
    'observed_facts.provenance.',
    'observed_facts.record_counts.*',
    'observed_facts.state_counts.by_version.*',
    'observed_facts.supplied_state_probabilities.by_version.*',
    'observed_frequency',
    'one closed-resampling report slot cannot hold two different method results',
    'one explicitly selected version; unweighted records',
    'one schema mapping summary cannot collapse distinct mapping declarations',
    'one-step extinction scenario',
    'one_step_extinction_probability',
    'operation',
    'operations',
    'ordered_compatible_dataset_versions',
    'ordering_certificate',
    'original earlier distribution',
    'original later distribution',
    'original_earlier_support',
    'original_later_support',
    'original_support_size',
    'owner assumptions cannot be empty or malformed',
    'owner limitations cannot be empty or malformed',
    'owner_ids',
    'pair_order',
    'parameters',
    'parent_ids',
    'parse_status',
    'partial',
    'partial_evidence',
    'path',
    'path_redacted',
    'present',
    'priority',
    'privacy_mode',
    'probability',
    'probability_corrections',
    'probability_mass_tolerance',
    'probability_residual',
    'production_failure',
    'provenance',
    'provenance assessment',
    'provenance assessment identity or flag type disagrees',
    'provenance category counts contradict supplied declarations',
    'provenance category namespace mismatch',
    'provenance composition',
    'provenance composition requires one complete selected version',
    'provenance counts disagree with validated join inventory',
    'provenance coverage contradicts retained join observations',
    'provenance coverage metadata is incomplete',
    'provenance enum fields must contain literal strings',
    'provenance field coverage differs from its retained declarations',
    'provenance fields require retained literal data',
    'provenance input must retain exact row types',
    'provenance inventory count contradicts retained join',
    'provenance missing-field identities differ from join',
    'provenance record key',
    'provenance result omitted its retained input validity',
    'provenance result omitted or invented validation diagnostics',
    'provenance result scope lacks retained join matches',
    'provenance row location',
    'provenance rows require immutable accepted collection',
    'provenance scope cannot discard validated records within its selected version',
    'provenance supplied status differs from validated join',
    'provenance_confidence',
    'provenance_confidence_counts',
    'provenance_confidence_field_coverage',
    'provenance_confidence_is_separate_and_does_not_discount_grounding',
    'provenance_manifest',
    'provenance_required_field_coverage',
    'provenance_row_coverage',
    'provenance_uncertainty',
    'proxy_signal',
    'proxy_signals',
    'random_seed',
    'ranking_rule',
    'rarity entry',
    'rarity_rank',
    'rarity_ranking',
    'ratio',
    'reason',
    'reason_codes',
    'recommended_next_metadata',
    'record identity',
    'record identity disagrees with canonical fields',
    'record_count',
    'record_counts',
    'record_coverage',
    'record_id',
    'record_key',
    'record_keys',
    'recorded_seed',
    'records',
    'records lacking usable required provenance',
    'records must be an explicit tuple of canonical rows',
    'records whose grounding remains unresolved',
    'records with no matching provenance row',
    'records with unresolved or invalid parent declarations',
    'records_with_matching_rows',
    'redacted_mode',
    'related_capability',
    'relative_tolerance',
    'remediation',
    'reopened_resampling',
    'reopening_weight',
    'replicate indices must retain the accepted schedule',
    'replicate_index',
    'replicate_schedule',
    'report_inputs',
    'representation',
    'representation compatibility must use explicit string pairs',
    'representation compatibility must use unique nonempty string pairs',
    'representation declarations must be nonempty literal strings',
    'representation field must contain strings or null',
    'representation missing-value policy is unsupported',
    'representation must use RepresentationConfig',
    'representation name and source must be explicit',
    'representation-dependent support, diversity and tail diagnostics',
    'representation_compatibility',
    'representation_coverage',
    'representation_name',
    'representation_source',
    'representation_version',
    'representative_locations',
    'requested_record_count must include every supplied valid record',
    'required computation-owner assumptions or limitations were changed',
    'required_evidence',
    'required_fields',
    'required_next_metadata',
    'required_provenance_fields',
    'requirements_met',
    'requirements_missing',
    'resample_size',
    'resampling input',
    'resolved_content must map record keys to already-read text',
    'resolved_content requires explicit local_ref mode',
    'resolved_parent_edge_count',
    'resolved_parent_edge_coverage',
    'retained generation validation',
    'retained provenance join',
    'retained version order',
    'retained_states',
    'retention_denominator',
    'retention_denominator_basis',
    'rng_name',
    'role',
    'row',
    'row_count',
    'row_number',
    'rule',
    'run',
    'run metadata must be a public JSON object',
    'run_status',
    'same_version',
    'sampled counts differ from state order',
    'sampled frequencies differ from state order',
    'sampled generation',
    'sampled generation sequence is incomplete',
    'sampled initial counts must remain unavailable and later counts present',
    'sampled replicate',
    'sampled state order differs from declared distribution',
    'sampled support identity mismatch',
    'sampled trajectory metadata is incomplete',
    'sampled_path',
    'sampled_path; sequential_binomial_complement_v1',
    'sampled_paths',
    'sampled_records',
    'scalar calculation',
    'scenario activation must use explicit ScenarioConfig',
    'scenario assumptions cannot be replaced or removed',
    'scenario distributions require literal immutable state pairs',
    'scenario parameters require ScenarioParameters with a literal model name',
    'scenario probability',
    'scenario result type and method disagree',
    'scenario state requires literal text',
    'scenario states must be unique immutable pairs',
    'schema_fields',
    'schema_mapping',
    'scope',
    'scope_id',
    'selected_valid_records',
    'selection',
    'sensor',
    'separate_ordered_representation_scopes',
    'sequential_binomial_complement_v1',
    'severity',
    'sha256',
    'signal',
    'simpson_concentration',
    'simulation_horizon',
    'simulation_replicates',
    'simulations',
    'simulations.closed_resampling',
    'simulations.tail_extinction',
    'single_version',
    'singleton_count',
    'size_bytes',
    'some_input_validation_failed',
    'source_field',
    'source_state',
    'source_states',
    'source_type',
    'source_type_counts',
    'source_type_field_coverage',
    'source_type_shares',
    'standard',
    'state count',
    'state counts differ from supplied frequency denominator',
    'state frequency',
    'state identifiers must be literal strings',
    'state mapping requires literal retained data',
    'state tables require exact StateFrequency entries',
    'state weight mass',
    'state_count',
    'state_counts',
    'state_frequencies',
    'state_frequency',
    'state_id',
    'state_ids',
    'state_list',
    'state_mapping',
    'state_mass',
    'state_order',
    'statement',
    'states',
    'status',
    'step',
    'submitted_record_scope',
    'sum_group_size_minus_one; DEFINITIONS_AND_UNITS:8.3',
    'supplied probabilities cannot become empirical counts or weighted mass',
    'supplied probability denominator was altered',
    'supplied_analytic_closed_resampling',
    'supplied_declared_tail:',
    'supplied_direct_closure_interval:',
    'supplied_distribution',
    'supplied_distribution:',
    'supplied_exact_duplicates:',
    'supplied_explicit_pair_support_and_diversity',
    'supplied_one_step_extinction_marginals',
    'supplied_probability_total',
    'supplied_provenance_composition:',
    'supplied_sampled_closed_resampling',
    'supplied_selected_state_marginal',
    'supplied_state_probabilities',
    'support',
    'support comparison',
    'support size disagrees with supplied support identities',
    'support table disagrees with supplied positive frequencies',
    'support_added_count',
    'support_contraction',
    'support_delta',
    'support_loss_count',
    'support_retention_ratio',
    'support_size',
    'support_sizes',
    'support_trajectories',
    'synthetic',
    'table missingness and status disagree',
    'table reasons require the frozen reason registry',
    'table status requires CalculationStatus',
    'tail',
    'tail membership differs from ranked entries',
    'tail scalar status differs from result',
    'tail selection',
    'tail_extinction',
    'tail_fragility',
    'tail_membership',
    'tail_record_share',
    'tail_rule',
    'tail_states',
    'tail_support_size',
    'target_field',
    'target_state',
    'the intended earlier and later versions',
    'the selected calculation scope',
    'theory_map_ids',
    'theory_or_product_limit',
    'toolkit_operationalization',
    'toolkit_operationalization; Definitions 3.7-3.9; P3-D08',
    'topic',
    'topic_field',
    'total_weight',
    'trace_ids',
    'trigger_rule',
    'unavailable',
    'unavailable_conclusion',
    'unavailable_conclusions',
    'unit',
    'universal_collapse_prediction',
    'universal_integrity',
    'unknown',
    'unknown input capability coverage detail',
    'unmapped comparison does not preserve its identical declared basis',
    'unmapped_field_count',
    'unresolved_grounding',
    'unresolved_grounding_count',
    'unresolved_parent_edge_count',
    'unsafe_operation_count',
    'unsupported distribution basis',
    'unsupported mapping direction',
    'unsupported sampled algorithm or ordering',
    'unsupported scenario model version',
    'unweighted',
    'unweighted distribution cannot claim weight masses',
    'unweighted frequency denominator differs from declared record scope',
    'upper_bound',
    'upper_bound - lower_bound = unresolved_grounding_count / total_record_count',
    'usable declared provenance without discarding independently valid calculations',
    'usable_exact_content',
    'utf-8',
    'valid_direct_grounding_no',
    'valid_direct_grounding_yes',
    'valid_experimental_scenario_declaration',
    'valid_matching_provenance',
    'valid_nonempty_input_for_declared_scope',
    'valid_parameters',
    'valid_record_scope',
    'valid_records_in_requested_scope',
    'validated bundle',
    'validated_bundle',
    'validated_ingest_scope',
    'validated_provenance_join',
    'validated_records_in_version',
    'validated_version:',
    'validation diagnostics require typed immutable entries',
    'validation message',
    'validation_status',
    'value',
    'version order must retain literal immutable declarations',
    'version_index',
    'version_order',
    'version_order_source',
    'version_timestamps',
    'versioned distribution requires one selected version',
    'versioned_model_outcomes',
    'warning',
    'warnings',
    'weight',
    'weight_field',
    'weighted',
    'weighted companion must preserve unweighted scope and representation',
    'weighted distribution has missing masses',
    'weighted distribution input basis disagrees with companion',
    'weighted distribution lacks mass metadata',
    'weighted mass denominator differs from supplied state mass',
    'weighted provenance companion',
    'weighted_',
    'weighted_missing_provenance_share',
    'weighted_record_mass',
    'weighted_source_type_masses',
    'weighted_source_type_shares',
    'weighted_state_masses',
    'weighting',
    'weighting_mode',
    'yes',
))


def _privacy_contract(value, contract, schema):
    if "$ref" in contract:
        return _privacy_contract(value, schema["$defs"][contract["$ref"].removeprefix("#/$defs/")], schema)
    if "type" not in contract:
        for variant in contract.get("anyOf", contract.get("oneOf", ())):
            if value is None and variant.get("type") == "null":
                return variant
            if value is not None and variant.get("type") != "null":
                return _privacy_contract(value, variant, schema)
    return contract


def _privacy_alias(protection, domain, value):
    return protection.pseudonym(domain, value)


def _privacy_text(value, field, *, mode, protection):
    """Keep reviewed owner prose; treat caller-authored prose as private data."""
    if value in _PRIVACY_SAFE_TEXT:
        return value
    if field == "basis_fields" and any(value == definition.path for definition in FIELD_REGISTRY):
        return value
    if field in ("reason_codes", "execution_reason_codes", "partial_evidence"):
        return _privacy_alias(protection, "diagnostic_code", value)
    if field == "execution_scope":
        operation, separator, scope_id = value.partition(":")
        if separator and operation in ("supplied_distribution", "supplied_provenance_composition", "supplied_exact_duplicates", "supplied_declared_tail", "supplied_direct_closure_interval"):
            return operation + ":" + (_privacy_alias(protection, "scope_id", scope_id) if mode == "redacted" else scope_id)
    if field == "numpy_version":
        import re
        if re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", value) is not None:
            return value
    return _privacy_alias(protection, "private_" + field, value)


def _privacy_value(value, contract, schema, *, mode, record_id_mode, protection, path=(), omissions=None):
    contract = _privacy_contract(value, contract, schema)
    field = path[-1] if path else "report"
    if "const" in contract or "enum" in contract or value is None or type(value) in (int, float, bool):
        return value
    if type(value) is dict:
        if set(value) == {"dataset_version", "record_id"}:
            return {"dataset_version": _privacy_alias(protection, "dataset_version", value["dataset_version"]) if mode == "redacted" else value["dataset_version"],
                    "record_id": _privacy_alias(protection, "record_id", [value["dataset_version"], value["record_id"]]) if record_id_mode == "hash" else value["record_id"]}
        properties = contract.get("properties", {})
        additional = contract.get("additionalProperties", {})
        result = {}
        scope = "denominator_basis" in value and "excluded_record_count" in value and "scope_id" in value
        duplicate = "group_id" in value and "record_keys" in value and "normalization_profile" in value
        for key, item in value.items():
            if record_id_mode == "omit" and scope and key in ("included_record_keys", "excluded_record_keys", "exclusions"):
                omissions.append(("field", "scope." + key, ""))
                if key == "exclusions":
                    for row in item:
                        for reason in row["reason_codes"]:
                            safe_reason = _privacy_text(reason, "reason_codes", mode=mode, protection=protection)
                            safe_scope = _privacy_alias(protection, "scope_id", value["scope_id"]) if mode == "redacted" else value["scope_id"]
                            omissions.append(("exclusion_reason", safe_scope, safe_reason))
                continue
            if record_id_mode == "omit" and key == "record_key":
                result[key] = None
                omissions.append(("field", "diagnostic.record_key", ""))
                continue
            if record_id_mode == "omit" and duplicate and key == "record_keys":
                result[key] = None
                result["redaction"] = {"omitted_fields": ["record_keys"], "reason": "redacted_identity_details"}
                omissions.append(("field", "duplicate_group.record_keys", ""))
                continue
            if mode == "redacted" and key == "path" and "path_redacted" in value:
                result[key] = None
                continue
            if mode == "redacted" and key == "path_redacted":
                result[key] = True
                continue
            output_key = key
            if mode == "redacted" and field in ("record_counts", "by_version", "by_state"):
                domain = "state_id" if field == "by_state" else "dataset_version"
                output_key = _privacy_alias(protection, domain, key)
            result[output_key] = _privacy_value(item, properties.get(key, additional), schema,
                mode=mode, record_id_mode=record_id_mode, protection=protection, path=path + (key,), omissions=omissions)
        return result
    if type(value) is list:
        return [_privacy_value(item, contract.get("items", {}), schema, mode=mode,
            record_id_mode=record_id_mode, protection=protection, path=path, omissions=omissions) for item in value]
    version_fields = ("dataset_version", "dataset_versions", "version_order", "earlier_version", "later_version")
    state_fields = ("state_id", "state_ids", "missing_state_id", "state_order", "source_state", "source_states", "target_state",
                    "original_earlier_support", "original_later_support", "harmonized_earlier_support", "harmonized_later_support", "support")
    identity_fields = ("run_id", "scope_id", "group_id", "representation_name", "representation_source", "representation_version",
                       "binning_or_mapping_rule", "field_name", "state_meaning", "earlier_state_semantics", "later_state_semantics",
                       "harmonized_state_semantics", "schema_fields", "source_field", "target_field", "fields_affected")
    if field in version_fields:
        return _privacy_alias(protection, "dataset_version", value) if mode == "redacted" else value
    if field in state_fields or (field == "value" and len(path) > 1 and path[-2] in ("extinct_states", "added_states", "retained_states", "tail_states")):
        return _privacy_alias(protection, "state_id", value) if mode == "redacted" else value
    if field in identity_fields:
        domain = "state_semantics" if field in ("state_meaning", "earlier_state_semantics", "later_state_semantics", "harmonized_state_semantics") else "schema_field" if field in ("field_name", "schema_fields", "source_field", "target_field", "fields_affected") else field
        return _privacy_alias(protection, domain, value) if mode == "redacted" else value
    if field in ("file_hash", "config_hash") or contract.get("pattern") == "^[0-9a-f]{64}$":
        return value
    if field in ("code", "message", "remediation", "file_role", "field") and path[0] in ("warnings", "errors"):
        return value
    if path == ("run", "command") or path[:2] == ("run", "null_reasons") or path in (("run", "toolkit_version"), ("run", "started_at"), ("run", "completed_at"), ("run", "python_version"), ("run", "platform")):
        return value
    if field == "path" and mode == "standard":
        return value
    return _privacy_text(value, str(field), mode=mode, protection=protection)


def _privacy_run_fields(run):
    """Sanitize volatile metadata independently of user-controlled narratives."""
    import re
    if re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+(?:\.(?:dev|rc|a|b)[0-9]+)?", run["toolkit_version"]) is None:
        run["toolkit_version"] = "private_or_nonstandard_version_label_omitted"
    date_pattern = r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]+)?(?:Z|[+-][0-9]{2}:[0-9]{2})"
    for name in ("started_at", "completed_at", "python_version", "platform"):
        value = run[name]
        safe = value is None or (name in ("started_at", "completed_at") and re.fullmatch(date_pattern, value) is not None) or (name == "python_version" and re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", value) is not None) or (name == "platform" and value in ("Linux", "Windows", "Darwin", "linux", "win32", "darwin"))
        if not safe:
            run[name] = None
            run["null_reasons"][name] = "private_or_nonstandard_metadata_omitted"
    command = run["command"]
    commands = tuple("rit " + operation + suffix for operation in ("audit", "validate", "example")
                     for suffix in ("", " --strict", " --redacted", " --strict --redacted"))
    if command not in commands:
        run["command"] = None
        run["null_reasons"]["command"] = "raw_command_not_exported"
    for name in tuple(run["null_reasons"]):
        run["null_reasons"][name] = "not_recorded" if run["null_reasons"][name] not in ("private_or_nonstandard_metadata_omitted", "raw_command_not_exported") else run["null_reasons"][name]


def privacy_view(report: CanonicalReport, *, mode="standard", record_id_mode=None, protection=None):
    """Select a content-safe view after all calculations, before any output sink.

    Standard retains declared identifiers and input inventory paths. Both modes
    suppress arbitrary narrative text and regenerate diagnostics. Redacted mode
    pseudonymizes nested labels consistently; preserve applies only to record_id.
    No calculation is repeated and no file is read. A caller-supplied protection
    context permits deterministic output without drawing a fresh run secret.
    """
    from ..result import PrivacyMode, RecordIdMode, SafeReportView, report_schema
    from ..models import PrivacyMode as InputPrivacyMode
    from ..utils.hashing import IdentifierProtection
    from ..utils.logging import safe_code, safe_diagnostic_text, safe_remediation, safe_field, safe_role
    if type(report) is not CanonicalReport:
        raise TypeError("privacy view requires an exact canonical report")
    if type(mode) not in (str, PrivacyMode, InputPrivacyMode) or mode not in ("standard", "redacted"):
        raise ValueError("privacy mode must be standard or redacted")
    if record_id_mode is None:
        record_id_mode = "hash" if mode == "redacted" else "preserve"
    if type(record_id_mode) not in (str, RecordIdMode) or record_id_mode not in ("preserve", "hash", "omit"):
        raise ValueError("record identity mode must be preserve, hash or omit")
    if mode == "standard" and record_id_mode != "preserve":
        raise ValueError("standard privacy mode requires preserved record identities")
    configured = report.sections["run"].get("resolved_options", {})
    if ("privacy_mode" in configured and configured["privacy_mode"] != mode) or (
            "record_id_mode" in configured and configured["record_id_mode"] != record_id_mode):
        raise ValueError("selected privacy view differs from the resolved configuration")
    if protection is None:
        protection = IdentifierProtection.create()
    if type(protection) is not IdentifierProtection:
        raise TypeError("privacy view requires an exact identifier protection context")
    payload = report.to_dict()
    if payload["run"]["privacy_mode"] != "standard" or payload["run"]["redacted_mode"]:
        raise ValueError("privacy view requires original standard evidence, not an already redacted report")
    _privacy_run_fields(payload["run"])
    for family in ("warnings", "errors"):
        for diagnostic in payload[family]:
            severity = diagnostic.get("severity", "warning")
            original_code = diagnostic["code"]
            diagnostic["code"] = safe_code(original_code, severity, protection=protection)
            diagnostic["message"] = safe_diagnostic_text(original_code, severity)
            diagnostic["remediation"] = list(safe_remediation(original_code))
            locations = diagnostic.get("representative_locations", [diagnostic])
            for location in locations:
                location["field"] = safe_field(location["field"])
                location["file_role"] = safe_role(location["file_role"])
    schema = report_schema()
    omissions = []
    protected = _privacy_value(payload, schema, schema, mode=str(mode), record_id_mode=str(record_id_mode),
                               protection=protection, omissions=omissions)
    run = protected["run"]
    run["privacy_mode"], run["redacted_mode"] = str(mode), mode == "redacted"
    run["network_count_scope"] = "toolkit_managed_outbound_operations"
    limitations = ["Identifier/content protection does not provide statistical anonymity or small-cell suppression.",
                  "Aggregate analytical values, evidence classes, availability, scope counts and diagnostic severity are unchanged.",
                  "Only reviewed toolkit narrative is retained; caller-authored narrative is replaced by nonreversible aliases.",
                  "Fresh identifier secrets affect output identity, not determinism of supplied calculations."]
    if record_id_mode == "preserve":
        limitations.append("Record identifiers are explicitly preserved; other redacted fields remain protected.")
    if omissions:
        limitations.append("Identity details were intentionally omitted, not treated as missing analytical evidence.")
        for kind, scope_or_field, reason in sorted(set(omissions)):
            if kind == "exclusion_reason":
                limitations.append("Record identities omitted; original exclusion reason " + reason + " for scope " + scope_or_field + ". Per-record linkage is intentionally omitted.")
            else:
                limitations.append("Omitted identity field: " + scope_or_field + ".")
    run["identifier_protection"] = {"algorithm": "HMAC-SHA-256", "stability_scope": protection.stability_scope,
                                   "record_id_mode": str(record_id_mode), "limitations": limitations}
    if "resolved_options" in run:
        run["resolved_options"]["privacy_mode"] = str(mode)
        run["resolved_options"]["record_id_mode"] = str(record_id_mode)
    return SafeReportView._from_safe_report(CanonicalReport.from_dict(protected))


def build_run_metadata(*, options, run_id: str, operation="python_api", started_at=None, completed_at=None,
                       duration_seconds=None, python_version=None, platform=None, random_seed=None,
                       network_call_count=0, deterministic=True, run_status="complete") -> dict:
    """Build standard internal metadata from explicit declarations, without I/O.

    The requested output options are retained as a safe summary. Assemble the
    report first, then pass its requested mode to ``privacy_view``. Dates, clocks,
    runtime version and platform are never inferred or read from the environment.
    """
    from .. import __version__
    from ..config import Phase4Options, phase4_config_summary, phase4_config_hash
    from ..result import RUN_NULLABLE_FIELDS
    if type(options) is not Phase4Options:
        raise TypeError("run metadata requires resolved Phase 4 options")
    if operation not in ("python_api", "audit", "validate", "example") or type(operation) is not str:
        raise ValueError("run operation is outside the approved command vocabulary")
    if type(run_id) is not str or not run_id or "\x00" in run_id:
        raise ValueError("run identifier must be nonempty literal text")
    command = None if operation == "python_api" else "rit " + operation + (" --strict" if options.strict_mode else "") + (" --redacted" if options.privacy_mode == "redacted" else "")
    result = {"run_id": run_id, "toolkit_version": __version__, "report_schema_version": "1.0",
              "started_at": started_at, "completed_at": completed_at, "duration_seconds": duration_seconds,
              "python_version": python_version, "platform": platform, "command": command,
              "config_hash": phase4_config_hash(options), "random_seed": random_seed,
              "strict_mode": options.strict_mode, "redacted_mode": False, "privacy_mode": "standard",
              "network_call_count": network_call_count, "deterministic": deterministic, "run_status": run_status,
              "network_count_scope": "toolkit_managed_outbound_operations", "hash_algorithm": "sha256",
              "config_hash_exclusions": ["id_salt_file", "identifier_secret_material"],
              "resolved_options": phase4_config_summary(options)}
    result["null_reasons"] = {name: "not_recorded" for name in RUN_NULLABLE_FIELDS if result[name] is None}
    _privacy_run_fields(result)
    # The complete canonical validator is reused without constructing evidence.
    empty = {key: {} if index < 8 else [] for index, key in enumerate(SECTION_ORDER)}
    empty["run"] = result
    return CanonicalReport.from_dict(empty).to_dict()["run"]
