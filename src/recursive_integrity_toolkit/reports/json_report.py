"""Serialize an explicitly protected canonical report as stable finite JSON.

Owner IDs:
    PR-013, PR-016

Inputs:
    An exact SafeReportView created by the explicit privacy_view transition.

Outputs:
    A UTF-8-compatible string with two-space indentation and a trailing LF.

Assumptions:
    Accepted evidence and privacy choices are supplied by their existing owners.
    Object insertion order has no meaning; supplied array order is preserved.

Limits:
    No input reading, calculation, redaction, clock, network or file publication.
    Canonical validation establishes structure, not the truth of supplied data.

Current phase status:
    Phase 4 Step 5: required JSON rendering only; import-safe standard library.
"""
from __future__ import annotations

import json

from ..result import SECTION_ORDER, SafeReportView, validate_report


def _ordered(value):
    """Order object keys without changing values or declared array relationships."""
    if type(value) is dict:
        return {key: _ordered(value[key]) for key in sorted(value)}
    if type(value) is list:
        return [_ordered(item) for item in value]
    return value


def render_json(report: SafeReportView) -> str:
    """Return the complete safe report with exact finite numerical values.

    The twelve top-level sections retain the public contract order. Nested keys
    use Unicode lexical order, and all arrays retain the supplied canonical
    sequence, including parallel identities, probabilities and trajectories.
    No caller-owned data is changed and no output is written.
    """
    if type(report) is not SafeReportView:
        raise TypeError("render_json requires a SafeReportView created by privacy_view")
    payload = report.to_dict()
    validate_report(payload)
    ordered = {section: _ordered(payload[section]) for section in SECTION_ORDER}
    return json.dumps(ordered, ensure_ascii=False, allow_nan=False, indent=2) + "\n"
