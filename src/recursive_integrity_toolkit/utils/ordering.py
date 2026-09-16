"""Order validated row identifiers for deterministic internal presentation.

Owner IDs:
    PR-016; PR-001 supporting identity order.

Inputs:
    A tuple of CanonicalRow objects from one validated same-kind scope.

Outputs:
    A new tuple ordered by the exact dataset_version and record_id strings.

Assumptions:
    Identity uniqueness has been validated before this helper is called.

Limits:
    No chronology inference, version rank, metric ranking, ancestry order,
    generation derivation, source mutation, or analytical-output determinism claim.

Current phase status:
    Phase 2 Step 4 stable row ordering only. No analytical behavior.
"""

from __future__ import annotations

from ..models import CanonicalRow, RecordKey


def _record_order_key(row: CanonicalRow) -> tuple[str, str]:
    if type(row) is not CanonicalRow or type(row.record_key) is not RecordKey:
        raise TypeError("stable ordering requires canonical row identities")
    return row.record_key.dataset_version, row.record_key.record_id


def stable_record_order(rows: tuple[CanonicalRow, ...]) -> tuple[CanonicalRow, ...]:
    """Return exact lexical presentation order, never a chronological order."""
    if type(rows) is not tuple:
        raise TypeError("stable ordering requires an explicit tuple of rows")
    return tuple(sorted(rows, key=_record_order_key))
