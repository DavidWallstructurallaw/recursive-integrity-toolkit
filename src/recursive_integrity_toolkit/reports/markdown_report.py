"""Render an explicitly protected canonical report as deterministic Markdown.

Owner IDs:
    PR-013, PR-018

Inputs:
    An exact, validated SafeReportView selected after calculation and assembly.

Outputs:
    A UTF-8-compatible string, LF line endings and one final newline.

Assumptions:
    Supplied evidence and declared list ordering belong to upstream owners.
    Numbers use shortest round-trip display; ratios remain unscaled ratios.

Limits:
    No calculations, input loading, redaction, file writing or network access.
    A valid safe view does not certify the truth of supplied evidence.

Current phase status:
    Phase 4 Step 5: required human-readable rendering only. Import-safe.
"""
from __future__ import annotations

import json
import unicodedata

from ..result import CAPABILITY_KEYS, SECTION_ORDER, SafeReportView, validate_report


_HEADINGS = (
    "Run metadata", "Input inventory", "Observability summary",
    "Capability matrix", "Observed facts", "Derived metrics", "Proxy signals",
    "Simulations", "Unavailable conclusions", "Recommended next metadata",
    "Warnings", "Errors",
)
_LIST_FIELDS = frozenset({"assumptions", "limitations"})
_CAPABILITY_LABELS = {
    "ingestion": "Ingestion",
    "content_diagnostics": "Content diagnostics",
    "provenance": "Provenance",
    "lineage": "Lineage",
    "dataset_longitudinal": "Dataset longitudinal",
    "model_longitudinal": "Model longitudinal",
    "intervention_simulation": "Intervention simulation",
}


def _code(value: object) -> str:
    """Keep literal data distinct from prose and inert in Markdown renderers.

    The code span contains a reversible JSON literal. Escaping the delimiter,
    table separator, HTML characters and invisible controls prevents either a
    Markdown parser or a subsequent HTML interpretation from promoting data to
    markup. Ordinary Unicode remains literal, without normalization.
    """
    encoded = json.dumps(
        value, ensure_ascii=False, allow_nan=False, sort_keys=True,
        separators=(", ", ": "),
    )
    safe = []
    for character in encoded:
        if (character in "`|<>&" or
                unicodedata.category(character) in {"Cc", "Cf", "Zl", "Zp"}):
            number = ord(character)
            if number <= 0xFFFF:
                safe.append(f"\\u{number:04x}")
            else:
                number -= 0x10000
                safe.append(f"\\u{0xD800 + (number >> 10):04x}")
                safe.append(f"\\u{0xDC00 + (number & 0x3FF):04x}")
        else:
            safe.append(character)
    return "`" + "".join(safe) + "`"


def _field(path: tuple[str | int, ...]) -> str:
    """Use literal bracket segments, keeping dynamic dots and slashes intact."""
    if not path:
        return "Value"
    segments = []
    for part in path:
        segments.append("[" + _code(part)[1:-1] + "]")
    return "`" + "".join(segments) + "`"


def _null_reason(key: str | int, owner: dict) -> str:
    reasons = owner.get("null_reasons", {})
    if key in reasons:
        return _code(reasons[key])
    if key in {"coverage", "denominator"} and owner.get(f"{key}_reason"):
        return _code(owner[f"{key}_reason"])
    if key == "ratio" and owner.get("reason"):
        return _code(owner["reason"])
    if key == "value" and owner.get("reason_codes"):
        return "reason codes " + _code(owner["reason_codes"])
    if key in {"coverage_reason", "denominator_reason"}:
        return "No null reason is required when the associated value is supplied."
    if key == "reason" and owner.get("ratio") is not None:
        return "No null reason is required when the associated ratio is supplied."
    if key == "path" and owner.get("path_redacted"):
        return "Withheld by the selected privacy view."
    if key == "record_keys" and owner.get("redaction"):
        return "Identity details omitted by the declared redaction policy."
    if key == "items" and owner.get("omission_reasons"):
        return "Detail omitted: " + _code(owner["omission_reasons"])
    if key in {"witness_record_keys", "witness_edge_count"} and owner.get("witness_reason"):
        return "Cycle witness omitted: " + _code(owner["witness_reason"])
    if key == "representation":
        return "No applicable representation supplied; consult status and required evidence."
    if key in {"record_count", "excluded_record_count"}:
        return "No empirical count supplied for this scope."
    return "No value supplied for this optional or inapplicable field."


def _value(value: object, *, key: str | int = "", owner: dict | None = None) -> str:
    if value is None:
        return "Unavailable (null): " + _null_reason(key, owner or {})
    if type(value) is bool:
        return "true" if value else "false"
    if type(value) in {int, float}:
        return repr(value)
    return _code(value)


def _table(lines: list[str], rows: list[tuple[str, str]]) -> None:
    if not rows:
        return
    lines.extend(("| Field | Value |", "|---|---|"))
    lines.extend(f"| {field} | {value} |" for field, value in rows)
    lines.append("")


def _details(lines: list[str], value: object) -> None:
    """Render every field, with narrative arrays displayed as readable lists."""
    rows: list[tuple[str, str]] = []
    lists: list[tuple[tuple[str | int, ...], list]] = []
    tables: list[tuple[tuple[str | int, ...], list[str], list[dict]]] = []

    def visit(node: object, path: tuple[str | int, ...], owner: dict) -> None:
        if type(node) is dict:
            if not node:
                rows.append((_field(path), _code({})))
            for key in sorted(node):
                item = node[key]
                item_path = (*path, key)
                if key in _LIST_FIELDS and type(item) is list and item:
                    lists.append((item_path, item))
                else:
                    visit(item, item_path, node)
        elif type(node) is list:
            if all(type(item) not in {dict, list} for item in node):
                rows.append((_field(path), _code(node)))
            elif (all(type(item) is dict and item for item in node) and
                  all(type(cell) not in {dict, list} for item in node for cell in item.values()) and
                  all(item.keys() == node[0].keys() for item in node) and len(node[0]) <= 8):
                tables.append((path, sorted(node[0]), node))
            else:
                for index, item in enumerate(node):
                    visit(item, (*path, index), {})
        else:
            key = path[-1] if path else ""
            rows.append((_field(path), _value(node, key=key, owner=owner)))

    visit(value, (), {})
    _table(lines, rows)
    for path, items in lists:
        lines.extend((f"**{_field(path)}**", ""))
        lines.extend("- " + _value(item) for item in items)
        lines.append("")
    for path, keys, items in tables:
        lines.extend((f"**{_field(path)}**", ""))
        lines.append("| " + " | ".join(_code(key) for key in keys) + " |")
        lines.append("|" + "---|" * len(keys))
        for item in items:
            lines.append("| " + " | ".join(_value(item[key], key=key, owner=item) for key in keys) + " |")
        lines.append("")


def _envelope(lines: list[str], node: dict, path: tuple[str | int, ...]) -> None:
    lines.extend(("### Analytical result", "", _field(path), ""))
    lines.append(
        "Status: " + _code(node["status"]) +
        "; evidence class: " + _code(node["evidence_class"]) +
        "; unit: " + _code(node["unit"]) +
        "; method: " + _code(node["method_id"]) + "."
    )
    lines.append("")
    if "value" in node and type(node["value"]) not in {dict, list}:
        lines.extend(("Value: " + _value(node["value"], key="value", owner=node) + ".", ""))
    lines.extend((
        "Denominator: " + _value(node["denominator"], key="denominator", owner=node) +
        "; coverage (ratio): " + _value(node["coverage"], key="coverage", owner=node) + ".",
        "",
    ))
    _details(lines, node)


def _analytical(lines: list[str], node: object, path: tuple[str | int, ...]) -> None:
    if type(node) is dict and {"evidence_class", "status", "method_id"} <= node.keys():
        _envelope(lines, node, path)
    elif type(node) is dict and node:
        for key in sorted(node):
            _analytical(lines, node[key], (*path, key))
    elif type(node) is list and node:
        for index, item in enumerate(node):
            _analytical(lines, item, (*path, index))
    else:
        lines.extend((_field(path), ""))
        _details(lines, node)


def _intervals(lines: list[str], metrics: dict) -> None:
    exposure = metrics.get("closure_exposure", {})
    if not exposure:
        return
    lines.extend(("### Closure exposure intervals", ""))
    for name in sorted(exposure):
        interval = exposure[name]
        lower = interval.get("lower_bound")
        upper = interval.get("upper_bound")
        width = interval.get("interval_width")
        if lower is None or upper is None or width is None:
            continue
        lines.append(
            "- " + _code(name) + " (ratio): " +
            _value(lower["value"], key="value", owner=lower) + " to " +
            _value(upper["value"], key="value", owner=upper) +
            "; interval width: " + _value(width["value"], key="value", owner=width) + "."
        )
    lines.append("")


def _capabilities(lines: list[str], capabilities: dict) -> None:
    if not capabilities:
        lines.extend(("Unavailable: capability assessment was not supplied. Empty object: `{}`.", ""))
        return
    lines.extend((
        "| Capability | Status | Coverage (ratio) | Reason | Execution | Execution reason |",
        "|---|---|---|---|---|---|",
    ))
    in_matrix = {"status", "coverage", "reason_codes", "execution_status", "execution_reason_codes"}
    for key in CAPABILITY_KEYS:
        item = capabilities[key]
        lines.append("| " + " | ".join((
            _CAPABILITY_LABELS[key], _code(item["status"]),
            _value(item["coverage"], key="coverage", owner=item),
            _code(item["reason_codes"]), _code(item["execution_status"]),
            _code(item["execution_reason_codes"]),
        )) + " |")
    lines.extend(("", "Coverage details and unresolved counts, when supplied, follow below. Related diagnostic entries appear in the Warnings and Errors sections.", ""))
    for key in CAPABILITY_KEYS:
        lines.extend(("**" + _CAPABILITY_LABELS[key] + " details**", ""))
        details = {name: value for name, value in capabilities[key].items() if name not in in_matrix}
        _details(lines, details)


def _items(lines: list[str], items: list, label: str) -> None:
    if not items:
        lines.extend(("No entries supplied. Empty list: `[]`.", ""))
    for index, item in enumerate(items):
        lines.extend((f"- **{label} {index + 1}**", ""))
        _details(lines, item)


def _summary(lines: list[str], payload: dict) -> None:
    run = payload["run"]
    observability = payload["observability"]
    inputs = payload["inputs"]
    lines.extend(("**Summary**", ""))
    lines.append("- Run ID: " + _code(run["run_id"]) + ".")
    if observability:
        lines.append("- Maximum observability level: " + _value(observability["maximum_level"]) + "; " + _code(observability["level_label"]) + ".")
    else:
        lines.append("- Maximum observability level: Unavailable; assessment was not supplied.")
    if payload["capabilities"]:
        statuses = [
            _CAPABILITY_LABELS[key] + ": " + _code(payload["capabilities"][key]["status"]) +
            " (execution " + _code(payload["capabilities"][key]["execution_status"]) + ")"
            for key in CAPABILITY_KEYS
        ]
        lines.append("- Capability statuses: " + "; ".join(statuses) + ".")
    else:
        lines.append("- Capability statuses: Unavailable; assessment was not supplied.")
    scope = inputs.get("scope")
    if scope is None:
        lines.append("- Record scope: Unavailable; no input scope supplied.")
    else:
        lines.append(
            "- Record scope: " + _code(scope["scope_id"]) +
            "; dataset versions " + _code(scope["dataset_versions"]) +
            "; records " + _value(scope["record_count"], key="record_count", owner=scope) +
            "; excluded records " + _value(scope["excluded_record_count"], key="excluded_record_count", owner=scope) + "."
        )
    representation = inputs.get("representation")
    if representation is None:
        lines.append("- Representation: Unavailable; no applicable input representation supplied.")
    else:
        lines.append(
            "- Representation: " + _code(representation["representation_name"]) +
            "; source " + _code(representation["representation_source"]) +
            "; version " + _code(representation["representation_version"]) +
            ". Complete mapping metadata appears in Input inventory."
        )
    lines.append(f"- Warning entries: {len(payload['warnings'])}; error entries: {len(payload['errors'])}.")
    lines.extend((
        "",
        "Display policy: numbers use shortest round-trip decimal notation without rounding; scientific notation retains tiny nonzero values. Ratios and probabilities remain unscaled. Units, denominators and interval endpoints are supplied evidence. JSON is the machine-readable authority.",
        "",
        "Quoted code literals represent supplied data, including identifiers and labels. JSON escapes visibly preserve markup characters and invisible controls. Unavailable (null) carries its declared reason or an explicit field-level null explanation. Empty objects and lists are shown explicitly. Object keys are sorted; supplied list order is preserved.",
        "",
    ))


def _footer(lines: list[str], run: dict) -> None:
    lines.extend((
        "***", "", "**Report footer**", "",
        "Toolkit version: " + _code(run["toolkit_version"]) + "; report schema version: " + _code(run["report_schema_version"]) + ".",
        "",
        "Evidence-class legend:", "",
        "- `observed_fact`: supplied or exactly counted evidence.",
        "- `derived_metric`: a deterministic function of supplied evidence.",
        "- `proxy_signal`: a bounded interpretation with stated limitations.",
        "- `simulation`: a scenario under explicit assumptions; experimental outputs retain that status.",
        "- `unavailable_conclusion`: required evidence is absent, implementation is deferred, or the conclusion lies outside approved scope.",
        "",
        "Unavailable conclusions are not false conclusions. Input observability and execution status describe separate facts. Supplied provenance declarations do not establish independently verified truth.",
        "",
        "Traceability reference: THEORY_TO_CODE_TRACEABILITY.md and docs/report_schema.md; individual results retain their owner IDs, theory-map IDs, trace IDs and method IDs.",
        "",
    ))


def render_markdown(report: SafeReportView) -> str:
    """Render only an explicit privacy view; never infer or calculate evidence.

    Registered section order is fixed. Nested map keys use Unicode lexical order
    and arrays retain their supplied order, including trajectories and paired
    lists. Analytical summaries precede complete field tables. No field is
    dropped except the exactly equal capability compatibility mirror, which
    points to the single canonical matrix.
    """
    if type(report) is not SafeReportView:
        raise TypeError("render_markdown requires an exact SafeReportView from privacy_view")
    payload = report.to_dict()
    validate_report(payload)
    lines = ["# Recursive Integrity Audit Report", ""]
    _summary(lines, payload)
    for section, heading in zip(SECTION_ORDER, _HEADINGS, strict=True):
        lines.extend(("## " + heading, ""))
        value = payload[section]
        if section == "capabilities":
            _capabilities(lines, value)
        elif section == "observability":
            _details(lines, {key: item for key, item in value.items() if key != "capabilities"})
            if value:
                lines.extend(("The equal observability.capabilities compatibility mirror is represented once in the Capability matrix section.", ""))
        elif section in {"observed_facts", "derived_metrics", "proxy_signals", "simulations", "unavailable_conclusions"}:
            if section == "derived_metrics":
                _intervals(lines, value)
            _analytical(lines, value, (section,))
        elif section in {"warnings", "errors", "recommended_next_metadata"}:
            label = {"warnings": "Warning", "errors": "Error", "recommended_next_metadata": "Recommended metadata"}[section]
            _items(lines, value, label)
        else:
            _details(lines, value)
    _footer(lines, payload["run"])
    return "\n".join(lines).rstrip("\n") + "\n"
