"""Resolve external roots, coverage, concentration and shared-root evidence.

Owner IDs: T4; Phase 5 Step 6.

Validated explicit grounding supplies anchors. Iterative dependency scheduling
unions complete root sets; unknown branches never supply exact roots. Logical
membership and candidate-visit budgets bound propagation before each work unit.
The allocation is topological and makes no causal or scientific quality claim.

Current phase status:
    Phase 5 Step 6 adds an explicitly requested descriptive shared-root proxy.
    Reports remain a later step. No file or network I/O, generation calculation
    or implicit invocation.
"""
from __future__ import annotations

from dataclasses import dataclass, field, replace
from heapq import heapify, heappop, heappush
from math import fsum, isfinite
from types import MappingProxyType
from typing import Literal

from ..errors import ErrorCode, LineageResourceLimitError
from ..io.validation import join_provenance
from ..models import BundleValidationResult, RecordKey, ValidationMessage, ValidationSeverity
from ..result import ExecutionStatus, ReportStatus
from .cycles import CycleAnalysis, DepthAssessment, analyze_cycles, _local_depth_reasons
from .graph import (
    LineageGraph, LineageLimits, LineageResourceUsage, LineageScope,
    _integer, _invalid, _key, _messages, build_lineage_graph,
)


_ROOT_REASONS = frozenset({
    "MISSING_PROVENANCE", "MISSING_REQUIRED_PROVENANCE", "UNKNOWN_GROUNDING",
    "PARENT_DECLARATION_UNAVAILABLE", "INVALID_PARENT_REFERENCE",
    "UNRESOLVED_PARENT_REFERENCE", "VERSION_ORDER_UNAVAILABLE", "CYCLE_AFFECTED",
    "INCOMPLETE_PARENT_ANCESTRY", "GROUNDED_PARENT_RULE_UNSUPPORTED",
})
_EXECUTION_REASONS = frozenset({
    "INVALID_LINEAGE_INPUT", "UNRESOLVED_ANCESTRY", "LINEAGE_RESOURCE_LIMIT_EXCEEDED",
})


def _reasons(values: object, allowed: frozenset[str]) -> tuple[str, ...]:
    if (type(values) is not tuple
            or any(type(value) is not str or value not in allowed for value in values)
            or values != tuple(sorted(set(values)))):
        raise _invalid("ancestry reasons require canonical known codes")
    return values


def _coverage(value: object, expected: float | None) -> bool:
    return value is None if expected is None else type(value) is float and value == expected


def _execution(messages: tuple[ValidationMessage, ...], complete: int, unresolved: int):
    if any(message.severity is ValidationSeverity.FATAL for message in messages):
        return ExecutionStatus.FAILED, ("INVALID_LINEAGE_INPUT",)
    if any(message.severity is ValidationSeverity.ERROR for message in messages):
        return (ExecutionStatus.PARTIAL if complete else ExecutionStatus.FAILED), ("INVALID_LINEAGE_INPUT",)
    if unresolved:
        return ExecutionStatus.PARTIAL, ("UNRESOLVED_ANCESTRY",)
    return ExecutionStatus.COMPLETED, ()


@dataclass(frozen=True, slots=True)
class RecordAncestry:
    """Exact complete roots, including known-empty, or explicit uncertainty."""
    record_key: RecordKey
    classification: Literal["grounded", "closed", "unresolved"]
    external_root_keys: frozenset[RecordKey] | None
    reason_codes: tuple[str, ...]
    lineage_depth: int | None
    depth_reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        _key(self.record_key)
        if type(self.classification) is not str:
            raise _invalid("ancestry classification requires a literal status")
        reasons = _reasons(self.reason_codes, _ROOT_REASONS)
        roots = self.external_root_keys
        if roots is None:
            if self.classification != "unresolved" or not reasons:
                raise _invalid("unresolved ancestry requires null roots and explicit reasons")
        else:
            if type(roots) is not frozenset:
                raise _invalid("complete ancestry requires an immutable root set")
            for root in roots:
                _key(root)
            if reasons or self.classification != ("grounded" if roots else "closed"):
                raise _invalid("ancestry classification disagrees with its complete root set")
            if self.lineage_depth is None:
                raise _invalid("complete ancestry requires complete structural paths")
        DepthAssessment(self.lineage_depth, self.depth_reason_codes)


@dataclass(frozen=True, slots=True)
class RootContribution:
    """One root's target incidence and equal-per-record fractional allocation."""
    record_key: RecordKey
    incidence_count: int
    incidence_share: float
    incidence_denominator: int
    fractional_mass: float
    normalized_weight: float
    weight_denominator: int

    def __post_init__(self) -> None:
        _key(self.record_key)
        for value in (self.incidence_count, self.incidence_denominator, self.weight_denominator):
            _integer(value)
        if not 1 <= self.incidence_count <= self.weight_denominator <= self.incidence_denominator:
            raise _invalid("root incidence requires positive target and grounded denominators")
        for value in (self.incidence_share, self.fractional_mass, self.normalized_weight):
            if type(value) is not float or not isfinite(value) or value <= 0:
                raise _invalid("root contributions require finite positive floating-point values")
        try:
            incidence_share = self.incidence_count / self.incidence_denominator
            normalized_weight = self.fractional_mass / self.weight_denominator
        except OverflowError:
            raise _invalid("root contribution denominators exceed the supported numeric range") from None
        if (self.fractional_mass > self.incidence_count
                or self.incidence_share != incidence_share
                or self.normalized_weight != normalized_weight):
            raise _invalid("root contribution values disagree with their declared denominators")


def _root_metrics(records: tuple[RecordAncestry, ...], total: int, grounded: int):
    """Aggregate complete target sets before any future display truncation.

    Input targets and each root visit use canonical identity order. fsum retains
    small fractional contributions without order-sensitive running totals. The
    temporary terms are bounded by the already admitted target memberships.
    """
    terms: dict[RecordKey, list[float]] = {}
    for record in records:
        roots = record.external_root_keys
        if roots:
            mass = 1.0 / len(roots)
            for root in sorted(roots):
                terms.setdefault(root, []).append(mass)
    contributions = []
    for root in sorted(terms):
        incidence = len(terms[root])
        mass = fsum(terms[root])
        contributions.append(RootContribution(
            root, incidence, incidence / total, total, mass, mass / grounded, grounded))
    hhi = fsum(row.normalized_weight ** 2 for row in contributions) if contributions else None
    effective = 1.0 / hhi if hhi is not None else None
    contributions.sort(key=lambda row: (-row.incidence_count, row.record_key))
    return tuple(contributions), len(contributions), hhi, effective


@dataclass(frozen=True, slots=True)
class LineageAnalysisResult:
    """Targets, complete root metrics and completed structural observations.

    Resource-aborted root propagation supplies no partition or record rows.
    Earlier graph/depth/reference observations survive. Node/edge admission
    failures precede this result and retain the graph typed exception contract.
    """
    scope: LineageScope
    execution_status: ExecutionStatus
    execution_reason_codes: tuple[str, ...]
    records: tuple[RecordAncestry, ...] | None
    cycles: CycleAnalysis
    grounded_record_count: int | None
    closed_record_count: int | None
    unresolved_record_count: int | None
    records_with_resolved_external_ancestry: int | None
    resolved_lineage_coverage: float | None
    external_ancestry_coverage: float | None
    ancestry_coverage_reason_codes: tuple[str, ...]
    declared_parent_reference_count: int | None
    resolved_parent_reference_count: int | None
    unresolved_parent_reference_count: int | None
    resolved_parent_edge_coverage: float | None
    no_declared_parents: bool
    reference_coverage_reason_codes: tuple[str, ...]
    root_contributions: tuple[RootContribution, ...] | None
    distinct_external_root_count: int | None
    ancestry_concentration_hhi: float | None
    effective_external_root_count: float | None
    resource_usage: LineageResourceUsage
    messages: tuple[ValidationMessage, ...]

    def __post_init__(self) -> None:
        if type(self.scope) is not LineageScope or type(self.cycles) is not CycleAnalysis:
            raise _invalid("ancestry analysis requires typed scope and cycle observations")
        scope = replace(self.scope)
        cycles = replace(self.cycles)
        messages = _messages(self.messages)
        if cycles.scope != scope:
            raise _invalid("ancestry and structural scopes disagree")
        if not set(cycles.messages) <= set(messages):
            raise _invalid("ancestry must preserve completed structural diagnostics")
        if type(self.resource_usage) is not LineageResourceUsage:
            raise _invalid("ancestry analysis requires typed resource usage")
        usage = replace(self.resource_usage)
        if usage.admitted_node_count != scope.loaded_record_count:
            raise _invalid("ancestry resource usage disagrees with the loaded scope")
        if type(self.execution_status) is not ExecutionStatus:
            raise _invalid("ancestry analysis requires a typed execution status")
        _reasons(self.execution_reason_codes, _EXECUTION_REASONS)
        counts = (self.grounded_record_count, self.closed_record_count,
                  self.unresolved_record_count, self.records_with_resolved_external_ancestry)
        root_metrics = (self.root_contributions, self.distinct_external_root_count,
                        self.ancestry_concentration_hhi, self.effective_external_root_count)
        if self.records is None:
            if (self.execution_status is not ExecutionStatus.FAILED
                    or self.execution_reason_codes != ("LINEAGE_RESOURCE_LIMIT_EXCEEDED",)
                    or usage.exhausted_limit not in ("max_root_memberships", "max_root_union_visits")
                    or any(value is not None for value in counts)
                    or self.resolved_lineage_coverage is not None
                    or self.external_ancestry_coverage is not None
                    or self.ancestry_coverage_reason_codes != ("LINEAGE_RESOURCE_LIMIT_EXCEEDED",)
                    or any(value is not None for value in root_metrics)
                    or not any(message.code == ErrorCode.LINEAGE_RESOURCE_LIMIT_EXCEEDED.value
                               and message.severity in (ValidationSeverity.ERROR, ValidationSeverity.FATAL)
                               for message in messages)):
                raise _invalid("aborted ancestry cannot expose a partial partition as exact")
        else:
            if type(self.records) is not tuple or usage.exhausted_limit is not None:
                raise _invalid("complete ancestry rows require an immutable completed partition")
            for record in self.records:
                if type(record) is not RecordAncestry:
                    raise _invalid("ancestry records require typed assessments")
                replace(record)
                depth = cycles.depths_by_record.get(record.record_key)
                if depth != DepthAssessment(record.lineage_depth, record.depth_reason_codes):
                    raise _invalid("ancestry depth disagrees with structural observations")
                if record.external_root_keys is not None and any(
                        root not in cycles.depths_by_record for root in record.external_root_keys):
                    raise _invalid("external roots require loaded canonical identities")
            if tuple(record.record_key for record in self.records) != scope.target_record_keys:
                raise _invalid("ancestry records must cover the entire canonical target scope")
            for count in counts:
                _integer(count)
            ground = sum(record.classification == "grounded" for record in self.records)
            closed = sum(record.classification == "closed" for record in self.records)
            unresolved = len(self.records) - ground - closed
            if counts != (ground, closed, unresolved, ground + closed):
                raise _invalid("ancestry counts disagree with the complete target partition")
            total = scope.target_record_count
            if (not _coverage(self.resolved_lineage_coverage, (ground + closed) / total if total else None)
                    or not _coverage(self.external_ancestry_coverage, ground / total if total else None)
                    or self.ancestry_coverage_reason_codes != (() if total else ("EMPTY_TARGET_SCOPE",))):
                raise _invalid("ancestry coverage must use the full explicit target denominator")
            if (self.execution_status, self.execution_reason_codes) != _execution(messages, ground + closed, unresolved):
                raise _invalid("ancestry execution status disagrees with its target partition and diagnostics")
            if type(self.root_contributions) is not tuple:
                raise _invalid("completed root metrics require immutable contribution rows")
            for contribution in self.root_contributions:
                if type(contribution) is not RootContribution:
                    raise _invalid("root contributions require typed values")
                replace(contribution)
            _integer(self.distinct_external_root_count)
            expected_roots, expected_count, expected_hhi, expected_effective = _root_metrics(
                self.records, total, ground)
            if (self.root_contributions != expected_roots
                    or self.distinct_external_root_count != expected_count
                    or not _coverage(self.ancestry_concentration_hhi, expected_hhi)
                    or not _coverage(self.effective_external_root_count, expected_effective)):
                raise _invalid("root metrics disagree with complete target root sets")
        references = (self.declared_parent_reference_count, self.resolved_parent_reference_count,
                      self.unresolved_parent_reference_count)
        if type(self.no_declared_parents) is not bool:
            raise _invalid("ancestry declaration status requires an explicit boolean")
        if self.declared_parent_reference_count is None:
            if (any(value is not None for value in references)
                    or self.resolved_parent_edge_coverage is not None or self.no_declared_parents
                    or self.reference_coverage_reason_codes != ("PARENT_REFERENCE_COUNT_UNAVAILABLE",)):
                raise _invalid("unknown reference cardinality cannot imply zero declared parents")
        else:
            for count in references:
                _integer(count)
            declared, resolved, unresolved = references
            if (declared != resolved + unresolved or self.no_declared_parents != (declared == 0)
                    or not _coverage(self.resolved_parent_edge_coverage, resolved / declared if declared else 1.0)
                    or self.reference_coverage_reason_codes != ()):
                raise _invalid("ancestry reference coverage disagrees with original declarations")
        object.__setattr__(self, "scope", scope)
        object.__setattr__(self, "cycles", cycles)
        object.__setattr__(self, "resource_usage", usage)
        object.__setattr__(self, "messages", messages)

    @property
    def root_metrics_status(self) -> ReportStatus:
        if self.records is None:
            return ReportStatus.UNAVAILABLE
        return ReportStatus.PARTIAL if self.unresolved_record_count else ReportStatus.AVAILABLE

    @property
    def concentration_status(self) -> ReportStatus:
        return self.root_metrics_status if self.grounded_record_count else ReportStatus.UNAVAILABLE

    @property
    def concentration_reason_codes(self) -> tuple[str, ...]:
        if self.records is None:
            return ("LINEAGE_RESOURCE_LIMIT_EXCEEDED",)
        return () if self.grounded_record_count else ("NO_RESOLVED_EXTERNAL_ROOTS",)

    @property
    def lineage_depth(self) -> int | None:
        return self.cycles.lineage_depth

    @property
    def maximum_resolved_target_depth(self) -> int | None:
        return self.cycles.maximum_resolved_target_depth

    @property
    def depth_resolved_record_count(self) -> int:
        return self.cycles.depth_resolved_record_count


@dataclass(frozen=True, slots=True)
class SharedAncestryDependence:
    """Descriptive exact-root witness with its original coverage and errors.

    A single ranked contribution is sufficient to witness shared support. The
    immutable source retains all evidence without copying the contribution list.
    Unresolved targets can preserve a witnessed presence but cannot prove absence.
    """
    source: LineageAnalysisResult = field(repr=False)

    def __post_init__(self) -> None:
        if type(self.source) is not LineageAnalysisResult:
            raise _invalid("shared ancestry requires a typed lineage analysis")
        object.__setattr__(self, "source", replace(self.source))

    @property
    def witness(self) -> RootContribution | None:
        roots = self.source.root_contributions
        return roots[0] if roots and roots[0].incidence_count >= 2 else None

    @property
    def status(self) -> ReportStatus:
        if self.witness is not None:
            return ReportStatus.PARTIAL if self.unresolved_record_count else ReportStatus.AVAILABLE
        if self.source.records is not None and self.scope.target_record_count and not self.unresolved_record_count:
            return ReportStatus.AVAILABLE
        return ReportStatus.UNAVAILABLE

    @property
    def level(self) -> Literal["present", "not_present", "indeterminate"]:
        if self.witness is not None:
            return "present"
        return "not_present" if self.status is ReportStatus.AVAILABLE else "indeterminate"

    @property
    def reason_codes(self) -> tuple[str, ...]:
        if self.source.records is None:
            return ("LINEAGE_RESOURCE_LIMIT_EXCEEDED",)
        if not self.scope.target_record_count:
            return ("EMPTY_TARGET_SCOPE",)
        return ("UNRESOLVED_ANCESTRY",) if self.unresolved_record_count else ()

    @property
    def scope(self) -> LineageScope:
        return self.source.scope

    @property
    def grounded_record_count(self) -> int | None:
        return self.source.grounded_record_count

    @property
    def closed_record_count(self) -> int | None:
        return self.source.closed_record_count

    @property
    def unresolved_record_count(self) -> int | None:
        return self.source.unresolved_record_count

    @property
    def resolved_lineage_coverage(self) -> float | None:
        return self.source.resolved_lineage_coverage

    @property
    def external_ancestry_coverage(self) -> float | None:
        return self.source.external_ancestry_coverage

    @property
    def ancestry_coverage_reason_codes(self) -> tuple[str, ...]:
        return self.source.ancestry_coverage_reason_codes

    @property
    def unresolved_reason_codes(self) -> tuple[str, ...]:
        return tuple(sorted({reason for record in self.source.records or () for reason in record.reason_codes}))

    @property
    def input_execution_status(self) -> ExecutionStatus:
        return self.source.execution_status

    @property
    def input_execution_reason_codes(self) -> tuple[str, ...]:
        return self.source.execution_reason_codes

    @property
    def input_has_errors(self) -> bool:
        return any(message.severity in (ValidationSeverity.ERROR, ValidationSeverity.FATAL)
                   for message in self.source.messages)

    @property
    def validation_messages(self) -> tuple[ValidationMessage, ...]:
        return self.source.messages

    @property
    def evidence_fields(self) -> tuple[str, ...]:
        return ("root_contributions.incidence_count", "resolved_lineage_coverage", "external_ancestry_coverage")

    @property
    def operationalization_label(self) -> str:
        return "theory_guided_operationalization"

    @property
    def limitations(self) -> tuple[str, ...]:
        return ("Descriptive shared-root topology under supplied metadata; no calibrated risk level.",
                "Does not establish causal contribution, semantic error, independent information, "
                "biological relatedness, universal integrity or collapse.")


def shared_ancestry_dependence(result: LineageAnalysisResult) -> SharedAncestryDependence:
    """Explicit pure proxy request; never reload data or rerun graph analysis."""
    return SharedAncestryDependence(result)


class _RootBudget:
    """Charge each logical unit before performing it; never expose partial roots."""
    def __init__(self, usage: LineageResourceUsage) -> None:
        self.initial = usage
        self.memberships = 0
        self.visits = 0

    def usage(self, exhausted: str | None = None) -> LineageResourceUsage:
        attempted = None if exhausted is None else getattr(self.initial.limits, exhausted) + 1
        return replace(self.initial, stored_root_membership_count=self.memberships,
                       root_union_visit_count=self.visits, exhausted_limit=exhausted,
                       attempted_value=attempted)

    def membership(self) -> None:
        if self.memberships == self.initial.limits.max_root_memberships:
            raise LineageResourceLimitError(self.usage("max_root_memberships"))
        self.memberships += 1

    def visit(self) -> None:
        if self.visits == self.initial.limits.max_root_union_visits:
            raise LineageResourceLimitError(self.usage("max_root_union_visits"))
        self.visits += 1


def _metadata(validation: BundleValidationResult, graph: LineageGraph):
    """Reassess original metadata while the shared graph owns parent syntax.

    Excluding parent_ids from this metadata-only join preserves the graph's
    per-record malformed declaration failures. No declaration is reinterpreted.
    """
    if not graph.node_keys:
        return {}, ()
    provenance = None if validation.provenance is None else tuple(
        replace(row, values=MappingProxyType({name: value for name, value in row.values.items()
                                             if name != "parent_ids"}))
        for row in validation.provenance)
    promoted = validation.parent_validation.promoted_warning_codes
    joined = join_provenance(validation.records, provenance, strict_mode=bool(promoted),
                             strict_warning_codes=promoted)
    return {match.record_key: match for match in joined.matches}, joined.messages


def _resolve_roots(graph: LineageGraph, cycles: CycleAnalysis, metadata, budget: _RootBudget):
    affected = set(cycles.affected_record_keys)
    roots: dict[RecordKey, frozenset[RecordKey] | None] = {}
    reasons: dict[RecordKey, tuple[str, ...]] = {}
    for key in cycles.affected_record_keys:
        roots[key] = None
        reasons[key] = tuple(sorted(_local_depth_reasons(graph, key) | {"CYCLE_AFFECTED"}))
    indegree = {key: len(graph.parents_by_child[key]) for key in graph.node_keys if key not in affected}
    pending = [key for key, count in indegree.items() if count == 0]
    heapify(pending)
    while pending:
        key = heappop(pending)
        parents = graph.parents_by_child[key]
        failures = _local_depth_reasons(graph, key)
        row = metadata[key].provenance
        if row is None:
            failures.add("MISSING_PROVENANCE")
        else:
            if not row.required_fields_valid:
                failures.add("MISSING_REQUIRED_PROVENANCE")
            grounding = row.values.get("external_grounding")
            if grounding == "unknown":
                failures.add("UNKNOWN_GROUNDING")
            if (grounding == "yes" and parents
                    and (len(parents) != 1 or row.values.get("transformation") != "carryover")):
                failures.add("GROUNDED_PARENT_RULE_UNSUPPORTED")
        for parent in parents:
            if roots[parent] is None:
                failures.add("INCOMPLETE_PARENT_ANCESTRY")
                failures.update(reasons[parent])
        if failures:
            roots[key] = None
            reasons[key] = tuple(sorted(failures))
        elif not parents:
            if row.values["external_grounding"] == "yes":
                budget.membership()
                roots[key] = frozenset((key,))
            else:
                roots[key] = frozenset()
            reasons[key] = ()
        else:
            combined = set()
            for parent in parents:
                for root in sorted(roots[parent]):
                    budget.visit()
                    if root not in combined:
                        budget.membership()
                        combined.add(root)
            roots[key] = frozenset(combined)
            reasons[key] = ()
        for child in graph.children_by_parent[key]:
            if child in indegree:
                indegree[child] -= 1
                if indegree[child] == 0:
                    heappush(pending, child)
    return roots, reasons


def analyze_lineage(
    validation: BundleValidationResult, *, target_dataset_version: str | None,
    limits: LineageLimits = LineageLimits(),
) -> LineageAnalysisResult:
    """Compute explicit ancestry and root metrics, stopping on exhaustion.

    All loaded context nodes participate in resolution and resource accounting.
    Only selected targets enter returned rows, G/C/U, coverage and root metrics.
    Canonical dependency-ready nodes precede canonical parent and root visits.
    """
    graph = build_lineage_graph(validation, target_dataset_version=target_dataset_version, limits=limits)
    cycles = analyze_cycles(graph)
    metadata, metadata_messages = _metadata(validation, graph)
    messages = _messages(cycles.messages + metadata_messages)
    target_evidence = tuple(graph.parent_evidence_by_record[key] for key in graph.scope.target_record_keys)
    count_known = all(item.declared_reference_count is not None for item in target_evidence)
    declared = sum(item.declared_reference_count for item in target_evidence) if count_known else None
    resolved = sum(item.resolved_reference_count for item in target_evidence) if count_known else None
    reference_fields = dict(
        declared_parent_reference_count=declared, resolved_parent_reference_count=resolved,
        unresolved_parent_reference_count=None if declared is None else declared - resolved,
        resolved_parent_edge_coverage=None if declared is None else (resolved / declared if declared else 1.0),
        no_declared_parents=declared == 0,
        reference_coverage_reason_codes=() if count_known else ("PARENT_REFERENCE_COUNT_UNAVAILABLE",),
    )
    budget = _RootBudget(graph.resource_usage)
    try:
        roots, reasons = _resolve_roots(graph, cycles, metadata, budget)
    except LineageResourceLimitError as error:
        messages += (ValidationMessage(ErrorCode.LINEAGE_RESOURCE_LIMIT_EXCEEDED.value,
                                       ValidationSeverity.ERROR, "Lineage root propagation exhausted its resource budget."),)
        return LineageAnalysisResult(
            graph.scope, ExecutionStatus.FAILED, (error.reason_code,), None, cycles,
            None, None, None, None, None, None, (error.reason_code,),
            **reference_fields, root_contributions=None, distinct_external_root_count=None,
            ancestry_concentration_hhi=None, effective_external_root_count=None,
            resource_usage=error.resource_usage, messages=messages)
    records = tuple(RecordAncestry(
        key, "unresolved" if roots[key] is None else "grounded" if roots[key] else "closed",
        roots[key], reasons[key], cycles.depths_by_record[key].lineage_depth,
        cycles.depths_by_record[key].reason_codes) for key in graph.scope.target_record_keys)
    ground = sum(record.classification == "grounded" for record in records)
    closed = sum(record.classification == "closed" for record in records)
    unresolved = len(records) - ground - closed
    status, execution_reasons = _execution(messages, ground + closed, unresolved)
    total = graph.scope.target_record_count
    contributions, distinct, hhi, effective = _root_metrics(records, total, ground)
    return LineageAnalysisResult(
        graph.scope, status, execution_reasons, records, cycles,
        ground, closed, unresolved, ground + closed,
        (ground + closed) / total if total else None, ground / total if total else None,
        () if total else ("EMPTY_TARGET_SCOPE",),
        **reference_fields, root_contributions=contributions, distinct_external_root_count=distinct,
        ancestry_concentration_hhi=hhi, effective_external_root_count=effective,
        resource_usage=budget.usage(), messages=messages)
