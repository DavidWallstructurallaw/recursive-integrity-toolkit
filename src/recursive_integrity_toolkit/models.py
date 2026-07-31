"""Define the future home of shared canonical data contracts.

Owner IDs:
    PR-001, PR-008, PR-010, PR-011

Future inputs:
    Future normalized records, provenance rows, lineage edges, and capability metadata.

Future outputs:
    Future project-owned typed records used across package layers.

Assumptions:
    Canonical identity will use dataset_version and record_id together.

Limits:
    No dataclasses, enums, coercion, normalization, or analytical behavior is implemented here.

Current phase status:
    Phase 1 package scaffold only. Import-safe. No analytical or data-processing logic.
"""
