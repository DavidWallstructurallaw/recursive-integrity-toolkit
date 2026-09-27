"""Resolve external roots, coverage, concentration and shared-root evidence.

Owner IDs: T4; Phase 6A Step 6.

Validated explicit grounding supplies anchors. Iterative dependency scheduling
unions complete root sets; unknown branches never supply exact roots. Logical
membership and candidate-visit budgets bound propagation before each work unit.
The allocation is topological and makes no causal or scientific quality claim.

Current phase status:
    Phase 6A Step 6 verifies selected handoffs through retained certificates.
    Legacy primary-only analysis and its input-bound handoffs remain supported.
    No file or network I/O, generation calculation or implicit invocation.
"""
from __future__ import annotations

from dataclasses import dataclass, field, replace
from heapq import heapify, heappop, heappush
from math import fsum, isfinite
from types import MappingProxyType
from typing import Literal, Mapping

from ..errors import ErrorCode, LineageResourceLimitError
from ..io.validation import join_provenance
from ..models import (
    BundleValidationResult, CalculationScope, RecordKey, ValidationMessage, ValidationSeverity,
)
from ..result import ExecutionStatus, ReportStatus
from ..utils.hashing import canonical_json_bytes, sha256_canonical
from .cycles import (
    CycleAnalysis, DepthAssessment, analyze_cycles, _local_depth_reasons, _WITNESS_EDGE_LIMIT,
)
from .graph import (
    LineageGraph, LineageLimits, LineageResourceUsage, LineageScope,
    _accepted_parents, _integer, _invalid, _key, _limits, _messages, _safe_evidence,
    build_lineage_graph,
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


def _lineage_input_signature(validation: BundleValidationResult) -> str:
    """Bind report handoffs to relevant declarations without retaining raw input.

    This internal digest detects stale same-key evidence, not authenticity.
    Content, URI, path, notes and extras are excluded. No graph or metric runs.
    """
    if type(validation) is not BundleValidationResult or validation.parent_validation is None:
        raise _invalid("lineage input binding requires retained validation evidence")
    names = ("dataset_version", "record_id", "parent_ids", "external_grounding",
             "source_type", "provenance_confidence", "transformation", "batch_id", "timestamp")

    def identity(key):
        return None if key is None else (key.dataset_version, key.record_id)

    def diagnostics(messages):
        return sorted([(message.code, message.severity.value, identity(message.record_key),
                       message.field, None if message.file_role is None else message.file_role.value)
                      for message in messages], key=canonical_json_bytes)

    def rows(items):
        return tuple((identity(row.record_key),
                      getattr(row, "kind", None),
                      None if row.location.file_role is None else row.location.file_role.value,
                      tuple((name, name in row.values, row.values.get(name)) for name in names),
                      tuple((name, row.field_states.get(name)) for name in names)
                      if hasattr(row, "field_states") else ())
                     for row in sorted(items, key=lambda row: row.record_key))

    def chronology(order):
        return (order.loaded_versions, order.order, order.order_source, dict(order.source_orders),
                dict(order.declarations), order.invocation_order, diagnostics(order.messages))

    batch = validation.parent_validation
    parents = []
    for item in batch.assessments:
        parent = item.result
        refs = None if parent is None else tuple(sorted([(
            tuple(sorted(ref.source_references)), ref.canonical_reference,
            identity(ref.parent_key), ref.resolution_status.value, ref.temporal_status)
            for ref in parent.references], key=canonical_json_bytes))
        parents.append((identity(item.child_key), item.provenance_available,
                        item.declared_reference_count, item.resolved_reference_count,
                        item.invalid_self_reference_count,
                        None if parent is None else parent.declaration_state, refs,
                        None if parent is None else parent.graph_validation_deferred,
                        None if parent is None else diagnostics(parent.messages),
                        diagnostics(item.messages)))
    try:
        return sha256_canonical((
            rows(validation.records), None if validation.provenance is None else rows(validation.provenance),
            chronology(validation.version_order), chronology(batch.version_order),
            tuple(parents), batch.promoted_warning_codes, diagnostics(batch.messages),
            diagnostics(validation.validation_messages)))
    except (ValueError, TypeError):
        raise _invalid("lineage input binding requires canonical declarations") from None


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
    input_signature: str = field(repr=False)

    def __post_init__(self) -> None:
        if (type(self.input_signature) is not str or len(self.input_signature) != 64
                or any(character not in "0123456789abcdef" for character in self.input_signature)):
            raise _invalid("lineage result requires its internal declaration binding")
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
    input_signature = _lineage_input_signature(validation)
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
            resource_usage=error.resource_usage, messages=messages, input_signature=input_signature)
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
        resource_usage=budget.usage(), messages=messages, input_signature=input_signature)


def _signature(value: object) -> None:
    if (type(value) is not str or len(value) != 64
            or any(character not in "0123456789abcdef" for character in value)):
        raise _invalid("selected lineage requires its internal input binding")


def _selected_lineage_signature(validation, selection, limits: LineageLimits) -> str:
    """Private invocation binding, including target selection and shared limits."""
    return sha256_canonical((
        _lineage_input_signature(validation), selection.input_signature,
        (limits.max_nodes, limits.max_edges, limits.max_root_memberships,
         limits.max_root_union_visits)))


def _reference_summary(graph: LineageGraph, keys: tuple[RecordKey, ...]):
    evidence = tuple(graph.parent_evidence_by_record[key] for key in keys)
    known = all(item.declared_reference_count is not None for item in evidence)
    declared = sum(item.declared_reference_count for item in evidence) if known else None
    resolved = sum(item.resolved_reference_count for item in evidence) if known else None
    return dict(
        declared_parent_reference_count=declared, resolved_parent_reference_count=resolved,
        unresolved_parent_reference_count=None if declared is None else declared - resolved,
        resolved_parent_edge_coverage=None if declared is None else (resolved / declared if declared else 1.0),
        no_declared_parents=declared == 0,
        reference_coverage_reason_codes=() if known else ("PARENT_REFERENCE_COUNT_UNAVAILABLE",))


def _target_depths(cycles: CycleAnalysis, keys: tuple[RecordKey, ...]):
    complete = tuple(cycles.depths_by_record[key].lineage_depth for key in keys
                     if cycles.depths_by_record[key].lineage_depth is not None)
    maximum = max(complete, default=None)
    return dict(lineage_depth=maximum if len(complete) == len(keys) else None,
                maximum_resolved_target_depth=maximum,
                depth_resolved_record_count=len(complete))


@dataclass(frozen=True, slots=True)
class TargetLineageSummary:
    """One full selected population derived from common retrospective evidence.

    Graph and cycle collections belong to SelectedLineageResult. These summaries
    retain only target ancestry rows, target arithmetic and shared immutable
    diagnostics/resource usage. Empty populations preserve explicit uncertainty.
    """
    scope: LineageScope
    population_scope: CalculationScope
    execution_status: ExecutionStatus
    execution_reason_codes: tuple[str, ...]
    records: tuple[RecordAncestry, ...] | None
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
    lineage_depth: int | None
    maximum_resolved_target_depth: int | None
    depth_resolved_record_count: int
    resource_usage: LineageResourceUsage
    messages: tuple[ValidationMessage, ...]
    input_signature: str = field(repr=False)

    def __post_init__(self) -> None:
        _signature(self.input_signature)
        if type(self.scope) is not LineageScope or type(self.population_scope) is not CalculationScope:
            raise _invalid("selected ancestry requires typed lineage and population scopes")
        replace(self.scope)
        try:
            replace(self.population_scope)
        except (TypeError, ValueError):
            raise _invalid("selected ancestry population scope is invalid") from None
        scope, population = self.scope, self.population_scope
        if (population.dataset_versions != (scope.target_dataset_version,)
                or population.included_record_keys != scope.target_record_keys
                or population.excluded_record_keys):
            raise _invalid("selected ancestry must use its complete version population")
        if type(self.resource_usage) is not LineageResourceUsage:
            raise _invalid("selected ancestry requires typed shared resource usage")
        replace(self.resource_usage)
        if self.resource_usage.admitted_node_count != scope.loaded_record_count:
            raise _invalid("selected ancestry shared node count disagrees with its scope")
        if self.messages != _messages(self.messages):
            raise _invalid("selected ancestry requires canonical shared diagnostics")
        if type(self.execution_status) is not ExecutionStatus:
            raise _invalid("selected ancestry requires a typed execution status")
        _reasons(self.execution_reason_codes, _EXECUTION_REASONS)
        counts = (self.grounded_record_count, self.closed_record_count,
                  self.unresolved_record_count, self.records_with_resolved_external_ancestry)
        metrics = (self.root_contributions, self.distinct_external_root_count,
                   self.ancestry_concentration_hhi, self.effective_external_root_count)
        if self.records is None:
            reason = ("LINEAGE_RESOURCE_LIMIT_EXCEEDED",)
            if (self.execution_status is not ExecutionStatus.FAILED
                    or self.execution_reason_codes != reason
                    or self.resource_usage.exhausted_limit not in (
                        "max_root_memberships", "max_root_union_visits")
                    or any(value is not None for value in counts + metrics)
                    or self.resolved_lineage_coverage is not None
                    or self.external_ancestry_coverage is not None
                    or self.ancestry_coverage_reason_codes != reason
                    or not any(message.code == ErrorCode.LINEAGE_RESOURCE_LIMIT_EXCEEDED.value
                               and message.severity in (ValidationSeverity.ERROR, ValidationSeverity.FATAL)
                               for message in self.messages)):
                raise _invalid("aborted selected ancestry cannot expose an exact prefix partition")
        else:
            if (type(self.records) is not tuple or self.resource_usage.exhausted_limit is not None
                    or any(type(record) is not RecordAncestry for record in self.records)):
                raise _invalid("selected ancestry requires an immutable completed partition")
            for record in self.records:
                replace(record)
            if tuple(record.record_key for record in self.records) != scope.target_record_keys:
                raise _invalid("selected ancestry must cover every target record exactly once")
            for count in counts:
                _integer(count)
            grounded = sum(record.classification == "grounded" for record in self.records)
            closed = sum(record.classification == "closed" for record in self.records)
            unresolved = len(self.records) - grounded - closed
            total = scope.target_record_count
            if (counts != (grounded, closed, unresolved, grounded + closed)
                    or not _coverage(self.resolved_lineage_coverage,
                                     (grounded + closed) / total if total else None)
                    or not _coverage(self.external_ancestry_coverage, grounded / total if total else None)
                    or self.ancestry_coverage_reason_codes != (() if total else ("EMPTY_TARGET_SCOPE",))
                    or (self.execution_status, self.execution_reason_codes)
                    != _execution(self.messages, grounded + closed, unresolved)):
                raise _invalid("selected ancestry counts, coverage or execution disagree with its partition")
            if (type(self.root_contributions) is not tuple
                    or any(type(row) is not RootContribution for row in self.root_contributions)):
                raise _invalid("selected root metrics require immutable typed contributions")
            for row in self.root_contributions:
                replace(row)
            _integer(self.distinct_external_root_count)
            expected = _root_metrics(self.records, total, grounded)
            if (metrics[:2] != expected[:2]
                    or not _coverage(metrics[2], expected[2])
                    or not _coverage(metrics[3], expected[3])):
                raise _invalid("selected root metrics disagree with complete target root sets")
        references = (self.declared_parent_reference_count, self.resolved_parent_reference_count,
                      self.unresolved_parent_reference_count)
        if type(self.no_declared_parents) is not bool:
            raise _invalid("selected parent declaration status requires a boolean")
        if references[0] is None:
            if (any(value is not None for value in references)
                    or self.resolved_parent_edge_coverage is not None or self.no_declared_parents
                    or self.reference_coverage_reason_codes != ("PARENT_REFERENCE_COUNT_UNAVAILABLE",)):
                raise _invalid("unknown parent cardinality cannot imply zero declared parents")
        else:
            for count in references:
                _integer(count)
            declared, resolved, unresolved = references
            if (declared != resolved + unresolved or self.no_declared_parents != (declared == 0)
                    or not _coverage(self.resolved_parent_edge_coverage,
                                     resolved / declared if declared else 1.0)
                    or self.reference_coverage_reason_codes != ()):
                raise _invalid("selected reference coverage disagrees with its denominators")
        _integer(self.depth_resolved_record_count)
        for depth in (self.lineage_depth, self.maximum_resolved_target_depth):
            if depth is not None:
                _integer(depth)
        if (self.depth_resolved_record_count > scope.target_record_count
                or (self.maximum_resolved_target_depth is None) != (self.depth_resolved_record_count == 0)
                or self.lineage_depth != (self.maximum_resolved_target_depth
                    if self.depth_resolved_record_count == scope.target_record_count else None)):
            raise _invalid("selected depth summary disagrees with target coverage")
        if self.records is not None:
            complete = tuple(row.lineage_depth for row in self.records if row.lineage_depth is not None)
            if (self.depth_resolved_record_count != len(complete)
                    or self.maximum_resolved_target_depth != max(complete, default=None)):
                raise _invalid("selected depth summary disagrees with target ancestry rows")

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


@dataclass(frozen=True, slots=True)
class _SelectedLineageCertificate:
    """Internal local-equation evidence; never a report identity collection.

    Complete root sets include context so a consumer can check each parent
    equation without invoking the resolver. Condensation ranks certify that
    declared cyclic components contain every cycle in the retained graph.
    Resource-aborted runs retain no partial root sets.
    """
    component_ranks: Mapping[RecordKey, int]
    roots: Mapping[RecordKey, frozenset[RecordKey] | None] | None
    reasons: Mapping[RecordKey, tuple[str, ...]] | None

    def __post_init__(self) -> None:
        if type(self.component_ranks) not in (dict, MappingProxyType):
            raise _invalid("selected lineage certificate requires immutable rank evidence")
        ranks = {}
        for key, rank in self.component_ranks.items():
            _key(key)
            _integer(rank)
            ranks[key] = rank
        if (self.roots is None) != (self.reasons is None):
            raise _invalid("selected lineage root certificate must be complete or absent")
        if self.roots is not None:
            if (type(self.roots) not in (dict, MappingProxyType)
                    or type(self.reasons) not in (dict, MappingProxyType)
                    or set(self.roots) != set(ranks) or set(self.reasons) != set(ranks)):
                raise _invalid("selected lineage root certificate must cover all loaded nodes")
            for key, roots in self.roots.items():
                if roots is not None:
                    if type(roots) is not frozenset or not roots <= ranks.keys():
                        raise _invalid("selected lineage certificate has unsupported root identities")
                _reasons(self.reasons[key], _ROOT_REASONS)
                if (roots is None) != bool(self.reasons[key]):
                    raise _invalid("selected lineage certificate roots and reasons disagree")
            object.__setattr__(self, "roots", MappingProxyType(dict(self.roots)))
            object.__setattr__(self, "reasons", MappingProxyType(dict(self.reasons)))
        object.__setattr__(self, "component_ranks", MappingProxyType(ranks))


def _selected_certificate(graph, cycles, roots, reasons):
    """Retain a condensation ordering from already discovered components."""
    owners = {key: component[0] for component in cycles.cyclic_components for key in component}
    owners.update((key, key) for key in graph.node_keys if key not in owners)
    parents = {owner: set() for owner in owners.values()}
    children = {owner: set() for owner in owners.values()}
    for child in graph.node_keys:
        for parent in graph.parents_by_child[child]:
            a, b = owners[parent], owners[child]
            if a != b:
                parents[b].add(a)
                children[a].add(b)
    remaining = {key: len(values) for key, values in parents.items()}
    ready = [key for key, count in remaining.items() if count == 0]
    heapify(ready)
    ranks = {}
    while ready:
        owner = heappop(ready)
        ranks[owner] = len(ranks)
        for child in children[owner]:
            remaining[child] -= 1
            if not remaining[child]:
                heappush(ready, child)
    if len(ranks) != len(parents):
        raise _invalid("selected lineage component certificate has incomplete coverage")
    return _SelectedLineageCertificate(
        {key: ranks[owners[key]] for key in graph.node_keys}, roots, reasons)


@dataclass(frozen=True, slots=True)
class SelectedLineageResult:
    """Chronological target summaries with one shared graph and cycle result."""
    selected_versions: tuple[str, ...]
    shared_graph: LineageGraph
    shared_cycles: CycleAnalysis
    targets: tuple[TargetLineageSummary, ...]
    resource_usage: LineageResourceUsage
    execution_status: ExecutionStatus
    reason_codes: tuple[str, ...]
    messages: tuple[ValidationMessage, ...]
    input_signature: str = field(repr=False)
    selection_signature: str = field(repr=False)
    certificate: _SelectedLineageCertificate = field(repr=False, compare=False)

    def __post_init__(self) -> None:
        _signature(self.input_signature)
        _signature(self.selection_signature)
        graph, cycles = self.shared_graph, self.shared_cycles
        if type(graph) is not LineageGraph or type(cycles) is not CycleAnalysis:
            raise _invalid("selected lineage requires shared typed graph and cycle evidence")
        if type(self.certificate) is not _SelectedLineageCertificate:
            raise _invalid("selected lineage requires retained handoff evidence")
        replace(self.certificate)
        if (cycles.scope != graph.scope or tuple(sorted(cycles.depths_by_record)) != graph.node_keys
                or not set(graph.messages) <= set(cycles.messages)):
            raise _invalid("selected graph and cycle evidence disagree")
        if (type(self.selected_versions) is not tuple or len(self.selected_versions) < 2
                or len(set(self.selected_versions)) != len(self.selected_versions)
                or type(self.targets) is not tuple
                or any(type(target) is not TargetLineageSummary for target in self.targets)
                or tuple(target.scope.target_dataset_version for target in self.targets) != self.selected_versions
                or graph.scope.target_dataset_version not in self.selected_versions):
            raise _invalid("selected lineage requires one ordered target per selected version")
        if type(self.resource_usage) is not LineageResourceUsage:
            raise _invalid("selected lineage requires a typed shared work counter")
        replace(self.resource_usage)
        if (set(self.certificate.component_ranks) != set(graph.node_keys)
                or (self.certificate.roots is None) != (self.resource_usage.exhausted_limit is not None)):
            raise _invalid("selected lineage handoff evidence disagrees with its loaded work")
        if (self.resource_usage.admitted_node_count != graph.resource_usage.admitted_node_count
                or self.resource_usage.admitted_edge_count != graph.resource_usage.admitted_edge_count
                or self.resource_usage.limits != graph.resource_usage.limits):
            raise _invalid("selected lineage resource accounting must cover the shared graph once")
        if self.messages != _messages(self.messages) or not set(cycles.messages) <= set(self.messages):
            raise _invalid("selected lineage must preserve canonical shared structural diagnostics")
        nodes = set(graph.node_keys)
        by_version: dict[str, list[RecordKey]] = {}
        for key in graph.node_keys:
            by_version.setdefault(key.dataset_version, []).append(key)
        aborted = self.resource_usage.exhausted_limit is not None
        for target in self.targets:
            # Validate only target-sized collections, never replace graph/cycles.
            replace(target)
            scope = target.scope
            if (scope.target_record_keys != tuple(by_version.get(scope.target_dataset_version, ()))
                    or scope.loaded_record_count != len(nodes)
                    or scope.loaded_dataset_versions != graph.scope.loaded_dataset_versions
                    or target.resource_usage is not self.resource_usage
                    or target.messages is not self.messages
                    or target.input_signature != self.input_signature
                    or (target.records is None) != aborted):
                raise _invalid("selected targets must retain full populations and common bound evidence")
            if any(getattr(target, name) != value for name, value in
                   _reference_summary(graph, scope.target_record_keys).items()):
                raise _invalid("selected references disagree with shared parent declarations")
            if any(getattr(target, name) != value for name, value in
                   _target_depths(cycles, scope.target_record_keys).items()):
                raise _invalid("selected target depths disagree with shared structural observations")
            for row in target.records or ():
                if (DepthAssessment(row.lineage_depth, row.depth_reason_codes)
                        != cycles.depths_by_record[row.record_key]
                        or row.external_root_keys is not None and not row.external_root_keys <= nodes):
                    raise _invalid("selected ancestry contains unsupported depth or root identity")
        if type(self.execution_status) is not ExecutionStatus:
            raise _invalid("selected lineage requires a typed execution status")
        _reasons(self.reason_codes, _EXECUTION_REASONS)
        expected = ((ExecutionStatus.FAILED, ("LINEAGE_RESOURCE_LIMIT_EXCEEDED",)) if aborted else
                    _execution(self.messages,
                               sum(target.grounded_record_count + target.closed_record_count
                                   for target in self.targets),
                               sum(target.unresolved_record_count for target in self.targets)))
        if (self.execution_status, self.reason_codes) != expected:
            raise _invalid("selected execution status disagrees with all target outcomes")


def analyze_selected_lineage(
    validation: BundleValidationResult, *, selection, limits: LineageLimits | None = None,
) -> SelectedLineageResult:
    """Resolve all loaded ancestry once, then summarize the full selected targets.

    Context and selected nodes consume common guards. Root-stage exhaustion
    invalidates every target root partition while completed depth/reference
    evidence survives. Graph-stage exhaustion retains the legacy exception.
    """
    from ..metrics.longitudinal import validate_longitudinal_selection

    validate_longitudinal_selection(validation, selection)
    bounded = _limits(LineageLimits() if limits is None else limits)
    signature = _selected_lineage_signature(validation, selection, bounded)
    graph = build_lineage_graph(validation, target_dataset_version=selection.primary_version, limits=bounded)
    cycles = analyze_cycles(graph)
    metadata, metadata_messages = _metadata(validation, graph)
    messages = _messages(cycles.messages + metadata_messages)
    budget = _RootBudget(graph.resource_usage)
    try:
        roots, reasons = _resolve_roots(graph, cycles, metadata, budget)
        usage = budget.usage()
    except LineageResourceLimitError as error:
        roots = reasons = None
        usage = error.resource_usage
        messages = _messages(messages + (ValidationMessage(
            ErrorCode.LINEAGE_RESOURCE_LIMIT_EXCEEDED.value, ValidationSeverity.ERROR,
            "Lineage root propagation exhausted its resource budget."),))
    targets = []
    for snapshot in selection.snapshots:
        population = snapshot.population_scope
        keys = population.included_record_keys
        scope = LineageScope(snapshot.dataset_version, keys, len(keys), len(graph.node_keys),
                             len(graph.node_keys) - len(keys), graph.scope.loaded_dataset_versions)
        common = dict(scope=scope, population_scope=population,
                      **_reference_summary(graph, keys), **_target_depths(cycles, keys),
                      resource_usage=usage, messages=messages, input_signature=signature)
        if roots is None:
            target = TargetLineageSummary(
                **common, execution_status=ExecutionStatus.FAILED,
                execution_reason_codes=("LINEAGE_RESOURCE_LIMIT_EXCEEDED",), records=None,
                grounded_record_count=None, closed_record_count=None, unresolved_record_count=None,
                records_with_resolved_external_ancestry=None, resolved_lineage_coverage=None,
                external_ancestry_coverage=None,
                ancestry_coverage_reason_codes=("LINEAGE_RESOURCE_LIMIT_EXCEEDED",),
                root_contributions=None, distinct_external_root_count=None,
                ancestry_concentration_hhi=None, effective_external_root_count=None)
        else:
            records = tuple(RecordAncestry(
                key, "unresolved" if roots[key] is None else "grounded" if roots[key] else "closed",
                roots[key], reasons[key], cycles.depths_by_record[key].lineage_depth,
                cycles.depths_by_record[key].reason_codes) for key in keys)
            grounded = sum(record.classification == "grounded" for record in records)
            closed = sum(record.classification == "closed" for record in records)
            unresolved = len(records) - grounded - closed
            status, status_reasons = _execution(messages, grounded + closed, unresolved)
            contributions, distinct, hhi, effective = _root_metrics(records, len(keys), grounded)
            target = TargetLineageSummary(
                **common, execution_status=status, execution_reason_codes=status_reasons,
                records=records, grounded_record_count=grounded, closed_record_count=closed,
                unresolved_record_count=unresolved, records_with_resolved_external_ancestry=grounded + closed,
                resolved_lineage_coverage=(grounded + closed) / len(keys) if keys else None,
                external_ancestry_coverage=grounded / len(keys) if keys else None,
                ancestry_coverage_reason_codes=() if keys else ("EMPTY_TARGET_SCOPE",),
                root_contributions=contributions, distinct_external_root_count=distinct,
                ancestry_concentration_hhi=hhi, effective_external_root_count=effective)
        targets.append(target)
    status, status_reasons = ((ExecutionStatus.FAILED, ("LINEAGE_RESOURCE_LIMIT_EXCEEDED",))
                             if roots is None else _execution(messages,
                                 sum(target.grounded_record_count + target.closed_record_count for target in targets),
                                 sum(target.unresolved_record_count for target in targets)))
    return SelectedLineageResult(selection.selected_order, graph, cycles, tuple(targets), usage,
                                 status, status_reasons, messages, signature, selection.input_signature,
                                 _selected_certificate(graph, cycles, roots, reasons))


def validate_selected_lineage_result(validation: BundleValidationResult, *, selection, result) -> None:
    """Check supplied local equations without running analysis or root resolution.

    Completed certificates bind every context and selected root to its parent
    evidence. Aborted work has no root values; its counters are checked for
    consistency, not treated as an authoritative runtime attestation.
    """
    from ..metrics.longitudinal import validate_longitudinal_selection

    validate_longitudinal_selection(validation, selection)
    if type(result) is not SelectedLineageResult:
        raise _invalid("selected lineage handoff requires its typed result")
    replace(result)
    replace(result.shared_graph)
    replace(result.shared_cycles)
    if (result.selected_versions != selection.selected_order
            or result.selection_signature != selection.input_signature
            or result.input_signature != _selected_lineage_signature(
                validation, selection, result.resource_usage.limits)
            or result.shared_graph.scope.target_dataset_version != selection.primary_version
            or result.shared_graph.node_keys != tuple(sorted(row.record_key for row in validation.records))
            or tuple(target.population_scope for target in result.targets)
            != tuple(snapshot.population_scope for snapshot in selection.snapshots)):
        raise _invalid("selected lineage handoff disagrees with its current input and selection")
    retained = validation.parent_validation
    if (retained is None
            or tuple(item.child_key for item in retained.assessments) != result.shared_graph.node_keys
            or any(_safe_evidence(item, item.child_key) !=
                   result.shared_graph.parent_evidence_by_record[item.child_key]
                   for item in retained.assessments)):
        raise _invalid("selected lineage graph disagrees with retained parent evidence")
    graph, cycles = result.shared_graph, result.shared_cycles
    if graph.messages != _messages(validation.validation_messages + retained.messages):
        raise _invalid("selected lineage graph diagnostics disagree with retained input")
    _validate_selected_structure(graph, cycles, result.certificate)
    metadata, metadata_messages = _metadata(validation, graph)
    expected_messages = cycles.messages + metadata_messages
    if result.resource_usage.exhausted_limit is not None:
        expected_messages += (ValidationMessage(
            ErrorCode.LINEAGE_RESOURCE_LIMIT_EXCEEDED.value, ValidationSeverity.ERROR,
            "Lineage root propagation exhausted its resource budget."),)
    if result.messages != _messages(expected_messages):
        raise _invalid("selected lineage diagnostics disagree with retained metadata")
    _validate_selected_roots(result, metadata)


def _validate_selected_structure(graph, cycles, certificate):
    """Verify claimed SCCs, quotient ranks and depth equations, not discover SCCs."""
    owners = {key: component[0] for component in cycles.cyclic_components for key in component}
    owners.update((key, key) for key in graph.node_keys if key not in owners)
    ranks = certificate.component_ranks
    self_keys = set(graph.self_parent_record_keys)
    for component in cycles.cyclic_components:
        members = set(component)
        if len(component) == 1 and component[0] not in self_keys:
            raise _invalid("selected lineage singleton cycle lacks self-parent evidence")
        if any(ranks[key] != ranks[component[0]] for key in component):
            raise _invalid("selected lineage component ranks split a claimed cycle")
        # Two restricted reachability checks certify strong connectivity of
        # each supplied component without searching for new components.
        for adjacency in (graph.parents_by_child, graph.children_by_parent):
            visited, pending = {component[0]}, [component[0]]
            while pending:
                for neighbor in adjacency[pending.pop()]:
                    if neighbor in members and neighbor not in visited:
                        visited.add(neighbor)
                        pending.append(neighbor)
            if visited != members:
                raise _invalid("selected lineage component is not strongly connected")
    if not self_keys <= set(cycles.cycle_member_record_keys):
        raise _invalid("selected lineage cycles omit retained self-parent evidence")
    owner_ranks = {owner: ranks[owner] for owner in set(owners.values())}
    if set(owner_ranks.values()) != set(range(len(owner_ranks))):
        raise _invalid("selected lineage quotient ranks must uniquely cover every component")
    affected, members = set(cycles.affected_record_keys), set(cycles.cycle_member_record_keys)
    positions = {key: index for index, key in enumerate(cycles.topological_order)}
    for child in graph.node_keys:
        parents = graph.parents_by_child[child]
        for parent in parents:
            if owners[parent] != owners[child] and ranks[parent] >= ranks[child]:
                raise _invalid("selected lineage quotient rank contradicts an accepted edge")
            if parent in affected and child not in affected:
                raise _invalid("selected lineage affected scope omits a cycle descendant")
            if child not in affected and positions[parent] >= positions[child]:
                raise _invalid("selected lineage topology contradicts an accepted edge")
        if child in affected - members and not any(parent in affected for parent in parents):
            raise _invalid("selected lineage affected scope includes an unsupported record")
        reasons = _local_depth_reasons(graph, child)
        if child in affected:
            reasons.add("CYCLE_AFFECTED")
            depth = None
        else:
            parent_depths = [cycles.depths_by_record[parent].lineage_depth for parent in parents]
            if any(value is None for value in parent_depths):
                reasons.add("INCOMPLETE_PARENT_DEPTH")
            depth = None if reasons else 1 + max(parent_depths, default=-1)
        if cycles.depths_by_record[child] != DepthAssessment(depth, tuple(sorted(reasons))):
            raise _invalid("selected lineage depth contradicts its parent equation")
    for detail in cycles.component_details:
        witness = detail.witness_record_keys
        if witness is None and detail.member_count <= _WITNESS_EDGE_LIMIT:
            raise _invalid("selected lineage cycle witness omission lacks a diagnostic limit")
        if witness is not None and any(
                b not in graph.children_by_parent[a] and not (a == b and a in self_keys)
                for a, b in zip(witness, witness[1:])):
            raise _invalid("selected lineage cycle witness includes an unsupported edge")
    expected_messages = graph.messages
    if cycles.cyclic_components:
        expected_messages += (ValidationMessage(
            ErrorCode.LINEAGE_CYCLE.value, ValidationSeverity.ERROR,
            "A cyclic component was detected in the loaded lineage graph."),)
    if cycles.messages != _messages(expected_messages):
        raise _invalid("selected lineage cycle diagnostics disagree with structural evidence")


def _validate_selected_roots(result, metadata):
    """Check complete root memberships and reasons against local parent evidence."""
    graph, cycles, certificate = result.shared_graph, result.shared_cycles, result.certificate
    if certificate.roots is None:
        return
    roots, reasons = certificate.roots, certificate.reasons
    affected = set(cycles.affected_record_keys)
    membership_count = union_count = 0
    for key in graph.node_keys:
        parents = graph.parents_by_child[key]
        failures = _local_depth_reasons(graph, key)
        if key in affected:
            failures.add("CYCLE_AFFECTED")
        else:
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
        if reasons[key] != tuple(sorted(failures)) or (roots[key] is None) != bool(failures):
            raise _invalid("selected lineage root uncertainty contradicts retained evidence")
        if failures:
            continue
        if not parents:
            expected = frozenset((key,)) if row.values["external_grounding"] == "yes" else frozenset()
            if roots[key] != expected:
                raise _invalid("selected lineage root anchor contradicts retained grounding")
        else:
            unsupported = set(roots[key])
            for parent in parents:
                if not roots[parent] <= roots[key]:
                    raise _invalid("selected lineage roots omit a complete parent contribution")
                unsupported.difference_update(roots[parent])
                union_count += len(roots[parent])
            if unsupported:
                raise _invalid("selected lineage roots include an unsupported parent contribution")
        membership_count += len(roots[key])
    usage = result.resource_usage
    if (usage.stored_root_membership_count != membership_count
            or usage.root_union_visit_count != union_count):
        raise _invalid("selected lineage completed work counters disagree with its root certificate")
    for target in result.targets:
        for record in target.records:
            if (record.external_root_keys != roots[record.record_key]
                    or record.reason_codes != reasons[record.record_key]):
                raise _invalid("selected lineage target roots disagree with verified parent evidence")


def validate_lineage_graph_exhaustion(validation: BundleValidationResult, *, usage) -> None:
    """Validate node/edge rejection from retained counts without building a graph."""
    if type(usage) is not LineageResourceUsage:
        raise _invalid("lineage graph exhaustion requires typed usage evidence")
    replace(usage)
    if type(validation) is not BundleValidationResult or validation.parent_validation is None:
        raise _invalid("lineage graph exhaustion requires retained parent evidence")
    limits = usage.limits
    node_count = len(validation.records)
    if node_count > limits.max_nodes:
        expected = LineageResourceUsage(limits.max_nodes, 0, 0, 0, limits,
                                        "max_nodes", limits.max_nodes + 1)
    else:
        edge_count = sum(len(_accepted_parents(_safe_evidence(item, item.child_key)))
                         for item in validation.parent_validation.assessments)
        if edge_count <= limits.max_edges:
            raise _invalid("lineage graph exhaustion has no rejected node or edge admission")
        expected = LineageResourceUsage(node_count, limits.max_edges, 0, 0, limits,
                                        "max_edges", limits.max_edges + 1)
    if usage != expected:
        raise _invalid("lineage graph exhaustion disagrees with retained admission evidence")
