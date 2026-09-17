"""Count exact duplicates inside one explicit version without deleting records.

Owner IDs:
    PR-006; PR-016 deterministic group and member presentation.

Inputs:
    Canonical rows and explicit exact-content representation declarations.
    LOCAL_REF requires caller-supplied text from the safe input reader.

Outputs:
    Immutable exact_duplicate_groups, duplicate_record_count and duplicate_group_count.
    Counts carry observed_fact, unweighted scope and definitions 8.3/8.4 metadata.

Assumptions:
    Exact byte equality is checked when a hash repeats. Independent copies can
    share record form without sharing origin; no provenance conclusion follows.

Limits:
    No I/O, logging, redacted report, near-duplicate, semantic, support, diversity,
    weighted, lineage, simulation or cross-version analysis. Never deletes inputs.

Current phase status:
    Phase 3 Step 3 exact duplicate groups and the two approved counts only.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from ..models import (
    CalculationEvidenceClass, CalculationMetadata, CalculationScope, CalculationStatus,
    CanonicalRow, ContentMode, RecordKey, RepresentationDescriptor, ScalarCalculation,
    ValidationCoverage,
)
from ..representations.content_hash import assign_content_states


@dataclass(frozen=True, slots=True)
class ExactDuplicateGroup:
    """The first canonical member is only a stable presentation representative."""

    content_hash: str = field(repr=False)
    record_keys: tuple[RecordKey, ...] = field(repr=False)

    @property
    def representative(self) -> RecordKey:
        return self.record_keys[0]

    @property
    def record_count(self) -> int:
        return len(self.record_keys)


@dataclass(frozen=True, slots=True)
class ExactDuplicateResult:
    """In-memory observed facts. Digests and identities are not anonymized IDs."""

    scope: CalculationScope
    representation: RepresentationDescriptor
    coverage: ValidationCoverage
    exact_duplicate_groups: tuple[ExactDuplicateGroup, ...] = field(repr=False)
    duplicate_record_count: ScalarCalculation
    duplicate_group_count: ScalarCalculation
    evidence_class: CalculationEvidenceClass = CalculationEvidenceClass.OBSERVED_FACT
    limitations: tuple[str, ...] = (
        "Exact record form does not establish semantic identity, authorship or independent origin.",
        "Representative selection never removes a source record or provenance row.",
        "Content hashes remain linkable; this internal result is not a redacted report.",
    )


def detect_exact_duplicates(
    records: tuple[CanonicalRow, ...], *, dataset_versions: tuple[str, ...], scope_id: str,
    representation_name: str, representation_version: str, normalization_profile: str,
    content_mode: ContentMode, resolved_content: dict[RecordKey, str] | None = None,
) -> ExactDuplicateResult:
    """PR-006: sum(size - 1) and number of groups with size greater than one.

    Reuses the pure representation boundary instead of trusting supplied digests.
    No F-number is registered for these counts; definition and method are explicit.
    """
    exact = assign_content_states(
        records, dataset_versions=dataset_versions, scope_id=scope_id,
        representation_name=representation_name, representation_version=representation_version,
        normalization_profile=normalization_profile, content_mode=content_mode,
        resolved_content=resolved_content,
    )
    representation = exact.representation
    members = {}
    for assignment in representation.assignments:
        bucket = members.setdefault(assignment.state_id, [])
        bucket.append(assignment.record_key)
    groups = []
    duplicates = 0
    for digest in sorted(members):
        keys = tuple(sorted(members[digest]))
        if len(keys) > 1:
            groups.append(ExactDuplicateGroup(digest, keys))
            duplicates += len(keys) - 1
    counts = []
    for name, value, unit, method in (
        ("duplicate_record_count", duplicates, "records", "sum_group_size_minus_one; DEFINITIONS_AND_UNITS:8.3"),
        ("duplicate_group_count", len(groups), "groups", "count_groups_of_size_greater_than_one; DEFINITIONS_AND_UNITS:8.4"),
    ):
        metadata = CalculationMetadata(
            name, "PR-006", None, CalculationEvidenceClass.OBSERVED_FACT, unit,
            method, representation.scope, representation.selection.descriptor,
            assumptions=("exact_utf8_v1 and SHA-256; equal digests verified against exact bytes",
                         "one explicitly selected version; unweighted records"),
            limitations=("Exact record form does not establish semantic identity or independent origin.",),
        )
        counts.append(ScalarCalculation(
            metadata, representation.status,
            value if representation.status is CalculationStatus.AVAILABLE else None,
            representation.reason_codes,
        ))
    return ExactDuplicateResult(
        representation.scope, representation.selection.descriptor, representation.coverage,
        tuple(groups), counts[0], counts[1],
    )
