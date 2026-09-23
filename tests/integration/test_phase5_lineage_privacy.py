"""Lineage identities cross the existing privacy boundary without data loss.

Small real inputs exercise roots, cycle witnesses, unresolved rows and public
scope labels. One 202-record case reaches the existing 100-row presentation cap.
"""

from copy import deepcopy
import json

import pytest
from jsonschema import Draft202012Validator

from recursive_integrity_toolkit.io.validation import validate_bundle
from recursive_integrity_toolkit.lineage.ancestry import analyze_lineage, shared_ancestry_dependence
from recursive_integrity_toolkit.metrics.bounds import lineage_closure_exposure
from recursive_integrity_toolkit.models import AuditBundle, FileRole, InputSource
from recursive_integrity_toolkit.reports.assembly import assemble_report, privacy_view
from recursive_integrity_toolkit.reports.json_report import render_json
from recursive_integrity_toolkit.reports.markdown_report import render_markdown
from recursive_integrity_toolkit.result import CanonicalReport
from recursive_integrity_toolkit.utils.hashing import IdentifierProtection


_VERSION_OLD = "VERSION_SENTINEL_old"
_VERSION_TARGET = "VERSION_SENTINEL_target"
_ROOT_ID = "RECORD_SENTINEL_root<script>alert(1)</script>|`"
_SECRET = b"lineage-privacy-test-secret-only!!"
_RAW_PAYLOAD = ("CONTENT_SENTINEL", "NOTES_SENTINEL", "URI_SENTINEL")


def _run():
    nullable = ("started_at", "completed_at", "duration_seconds", "python_version",
                "platform", "command", "config_hash", "random_seed")
    return {
        "run_id": "RUN_SENTINEL", "toolkit_version": "0.1.0.dev3",
        "report_schema_version": "1.1", **dict.fromkeys(nullable),
        "strict_mode": False, "redacted_mode": False, "network_call_count": 0,
        "deterministic": True, "privacy_mode": "standard", "run_status": "complete",
        "null_reasons": {key: "No execution metadata supplied." for key in nullable},
    }


def _report(tmp_path, *, capped=False):
    tmp_path.mkdir(parents=True, exist_ok=True)
    # A matching record_id in different versions is two distinct identities.
    if capped:
        declarations = {
            **{(_VERSION_TARGET, f"RECORD_SENTINEL_root_{i:03}"): ([], "yes") for i in range(101)},
            **{(_VERSION_TARGET, f"RECORD_SENTINEL_cycle_{i:03}"):
               ([f"{_VERSION_TARGET}::RECORD_SENTINEL_cycle_{i:03}"], "no") for i in range(101)},
        }
    else:
        declarations = {
            (_VERSION_OLD, _ROOT_ID): ([], "yes"),
            (_VERSION_OLD, "RECORD_SENTINEL_cycle_a"):
                ([f"{_VERSION_OLD}::RECORD_SENTINEL_cycle_b"], "no"),
            (_VERSION_OLD, "RECORD_SENTINEL_cycle_b"):
                ([f"{_VERSION_OLD}::RECORD_SENTINEL_cycle_a"], "no"),
            (_VERSION_TARGET, _ROOT_ID): ([], "yes"),
            (_VERSION_TARGET, "RECORD_SENTINEL_child"):
                ([f"{_VERSION_OLD}::{_ROOT_ID}"], "no"),
            (_VERSION_TARGET, "RECORD_SENTINEL_child_two"):
                ([f"{_VERSION_OLD}::{_ROOT_ID}"], "no"),
            (_VERSION_TARGET, "RECORD_SENTINEL_closed"): ([], "no"),
            (_VERSION_TARGET, "RECORD_SENTINEL_unknown"): ([], "unknown"),
            (_VERSION_TARGET, "RECORD_SENTINEL_affected"):
                ([f"{_VERSION_OLD}::RECORD_SENTINEL_cycle_a"], "no"),
        }
    records, provenance = [], []
    for (version, record_id), (parents, grounding) in declarations.items():
        identity = {"dataset_version": version, "record_id": record_id}
        records.append({**identity, "content": "CONTENT_SENTINEL",
                        "notes": "NOTES_SENTINEL"})
        provenance.append({**identity, "source_type": "human" if grounding == "yes" else "synthetic",
                           "provenance_confidence": "confirmed", "external_grounding": grounding,
                           "parent_ids": parents, "transformation": "generate",
                           "source_uri": "https://invalid.example/URI_SENTINEL",
                           "notes": "NOTES_SENTINEL"})
    sources = []
    for name, role, rows in (
        ("primary", FileRole.RECORDS_PRIMARY, [row for row in records if row["dataset_version"] == _VERSION_TARGET]),
        ("context", FileRole.RECORDS_COMPARE, [row for row in records if row["dataset_version"] != _VERSION_TARGET]),
        ("provenance", FileRole.PROVENANCE_MANIFEST, provenance),
    ):
        if rows:
            path = tmp_path / ("PATH_SENTINEL_" + name + ".jsonl")
            path.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")
            sources.append(InputSource(role, path))
    versions = [_VERSION_TARGET] if capped else [_VERSION_OLD, _VERSION_TARGET]
    bundle = validate_bundle(AuditBundle(tuple(sources)), configuration={"version_order": versions})
    lineage = analyze_lineage(bundle, target_dataset_version=_VERSION_TARGET)
    return assemble_report(bundle, run=_run(), lineage=lineage,
                           lineage_bounds=lineage_closure_exposure(lineage),
                           shared_ancestry=shared_ancestry_dependence(lineage))


def _view(report, mode="redacted", record_id_mode="hash", *, secret=_SECRET):
    return privacy_view(report, mode=mode, record_id_mode=record_id_mode,
                        protection=IdentifierProtection.create(secret=secret))


def _validate(view, repo_root):
    value = view.to_dict()
    schema = json.loads((repo_root / "schemas/report.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator(schema).validate(value)
    CanonicalReport.from_dict(value)
    assert json.loads(render_json(view)) == value
    return value


def _details(value):
    observed = value["observed_facts"]["lineage"]
    cycle = observed["cycle_analysis"]["value"]
    return {
        **{name: cycle[name] for name in ("components", "cycle_member_record_keys", "affected_record_keys")},
        "unresolved_record_details": observed["unresolved_record_details"]["value"],
        "top_shared_ancestors": value["derived_metrics"]["lineage"]["top_shared_ancestors"]["value"],
    }


def _identities(value, path=()):
    if isinstance(value, dict):
        if set(value) == {"dataset_version", "record_id"}:
            yield path, value
        else:
            for name, item in value.items():
                yield from _identities(item, (*path, name))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from _identities(item, (*path, index))


def _lineage_identity_evidence(value):
    return {
        "observations": value["observed_facts"]["lineage"],
        "metrics": value["derived_metrics"]["lineage"],
        "bounds": value["derived_metrics"]["closure_exposure"]["lineage"],
        "proxy": value["proxy_signals"]["shared_ancestry_dependence"],
        "errors": value["errors"], "warnings": value["warnings"],
    }


def _quantitative_evidence(value):
    """Exclude presentation identities while comparing exact analytical values."""
    observed = value["observed_facts"]["lineage"]
    cycle = observed["cycle_analysis"]["value"]
    metrics = value["derived_metrics"]["lineage"]
    graph_scope = observed["graph_scope"]["value"]
    return {
        "run_status": value["run"]["run_status"],
        "capability": value["capabilities"]["lineage"],
        "cycle_counts": {name: item for name, item in cycle.items() if not isinstance(item, dict)},
        "graph_counts": {name: item for name, item in graph_scope.items() if type(item) is int},
        "depth": observed["depth_summary"]["value"],
        "resources": observed["resource_usage"]["value"],
        "metrics": {name: {field: item for field, item in envelope.items()
                            if field in {"value", "status", "coverage", "denominator", "evidence_class", "unit"}}
                    for name, envelope in metrics.items() if name != "top_shared_ancestors"},
        "closure": {name: {field: item for field, item in envelope.items()
                            if field in {"value", "status", "coverage", "denominator", "evidence_class", "unit"}}
                    for name, envelope in value["derived_metrics"]["closure_exposure"]["lineage"].items()},
        "proxy": {name: item for name, item in value["proxy_signals"]["shared_ancestry_dependence"].items()
                  if name in {"status", "level", "coverage", "denominator", "evidence_class"}},
        "diagnostics": [(name, row["severity"], row.get("effect_on_run"), row["effect_on_capabilities"])
                        for name in ("errors", "warnings") for row in value[name]],
    }


@pytest.mark.parametrize("mode,record_id_mode", [
    ("standard", "preserve"), ("redacted", "hash"),
    ("redacted", "omit"), ("redacted", "preserve"),
])
def test_lineage_privacy_modes_preserve_analytical_values_and_safe_rendering(
        tmp_path, repo_root, mode, record_id_mode):
    report = _report(tmp_path)
    original = deepcopy(report.to_dict())
    view = _view(report, mode, record_id_mode)
    actual = _validate(view, repo_root)
    assert _quantitative_evidence(actual) == _quantitative_evidence(original)
    assert report.to_dict() == original
    for rendered in (render_json(view), render_markdown(view)):
        assert all(sentinel not in rendered for sentinel in _RAW_PAYLOAD)
        assert ("VERSION_SENTINEL" in rendered) is (mode == "standard")
        assert ("PATH_SENTINEL" in rendered) is (mode == "standard")
        assert ("RECORD_SENTINEL" in rendered) is (record_id_mode == "preserve")
    markdown = render_markdown(view)
    assert "<script>" not in markdown
    assert actual["observability"]["capabilities"] == actual["capabilities"]


@pytest.mark.parametrize("record_id_mode", ["hash", "omit"])
def test_standard_lineage_does_not_expand_existing_identity_mode_policy(tmp_path, record_id_mode):
    with pytest.raises(ValueError, match="standard privacy mode requires preserved record identities"):
        _view(_report(tmp_path), "standard", record_id_mode)


def test_lineage_hashes_share_identity_domains_without_reordering_rows(tmp_path, repo_root):
    report = _report(tmp_path)
    original = report.to_dict()
    actual = _validate(_view(report), repo_root)
    before = dict(_identities(_lineage_identity_evidence(original)))
    after = dict(_identities(_lineage_identity_evidence(actual)))
    assert before.keys() == after.keys()
    mapping = {}
    for path, identity in before.items():
        key = (identity["dataset_version"], identity["record_id"])
        protected = after[path]
        assert protected["dataset_version"].startswith("hmac-sha256:")
        assert protected["record_id"].startswith("hmac-sha256:")
        assert mapping.setdefault(key, protected) == protected
    # Cycle witness closure and member/affected appearances share one alias.
    assert len(before) > len(mapping)
    cycle = actual["observed_facts"]["lineage"]["cycle_analysis"]["value"]
    witness = cycle["components"]["items"][0]["witness_record_keys"]
    assert witness[0] == witness[-1]
    assert all(identity in cycle["cycle_member_record_keys"]["items"] for identity in witness)
    scope = actual["observed_facts"]["lineage"]["graph_scope"]["value"]
    target_alias = scope["target_dataset_version"]
    assert target_alias in scope["loaded_dataset_versions"]
    for (version, _), identity in mapping.items():
        assert identity["dataset_version"] in scope["loaded_dataset_versions"]
        if version == _VERSION_TARGET:
            assert identity["dataset_version"] == target_alias
    # The same text in separate version scopes remains a different record key.
    old_id = mapping[(_VERSION_OLD, _ROOT_ID)]["record_id"]
    new_id = mapping[(_VERSION_TARGET, _ROOT_ID)]["record_id"]
    assert old_id != new_id
    original_roots = _details(original)["top_shared_ancestors"]["items"]
    protected_roots = _details(actual)["top_shared_ancestors"]["items"]
    assert [{name: value for name, value in row.items() if name != "record_key"} for row in protected_roots] == [
        {name: value for name, value in row.items() if name != "record_key"} for row in original_roots]


def test_lineage_hash_secret_changes_identities_only(tmp_path, repo_root):
    report = _report(tmp_path)
    first = _view(report)
    again = _view(report)
    other = _view(report, secret=b"a-different-lineage-test-secret!!")
    assert render_json(first) == render_json(again)
    assert render_markdown(first) == render_markdown(again)
    first_value, other_value = (_validate(view, repo_root) for view in (first, other))
    assert _quantitative_evidence(first_value) == _quantitative_evidence(other_value)
    first_ids, other_ids = (dict(_identities(_lineage_identity_evidence(value)))
                            for value in (first_value, other_value))
    assert first_ids.keys() == other_ids.keys()
    assert all(first_ids[path] != other_ids[path] for path in first_ids)
    assert first_value["run"]["identifier_protection"]["stability_scope"] == "run"


@pytest.mark.parametrize("mode,record_id_mode", [
    ("standard", "preserve"), ("redacted", "hash"),
    ("redacted", "omit"), ("redacted", "preserve"),
])
def test_private_unresolved_reasons_keep_supplied_order_after_protection(
        tmp_path, repo_root, mode, record_id_mode):
    payload = _report(tmp_path).to_dict()
    private_reasons = ["SECRET_A", "SECRET_B", "SECRET_C"]
    payload["observed_facts"]["lineage"]["unresolved_record_details"]["value"]["items"][0]["reason_codes"] = private_reasons
    report = CanonicalReport.from_dict(payload)
    view = _view(report, mode, record_id_mode)
    actual = _validate(view, repo_root)
    for rendered in (render_json(view), render_markdown(view)):
        assert all(reason not in rendered for reason in private_reasons)
    detail = _details(actual)["unresolved_record_details"]
    if record_id_mode == "omit":
        assert detail["items"] is None
    else:
        protection = IdentifierProtection.create(secret=_SECRET)
        expected = [protection.pseudonym("diagnostic_code", reason) for reason in private_reasons]
        assert expected != sorted(expected)
        assert detail["items"][0]["reason_codes"] == expected
    assert _quantitative_evidence(actual) == _quantitative_evidence(payload)


@pytest.mark.parametrize("capped", [False, True])
def test_lineage_omit_uses_whole_collections_and_retains_cap_reasons(tmp_path, repo_root, capped):
    report = _report(tmp_path, capped=capped)
    original = report.to_dict()
    view = _view(report, record_id_mode="omit")
    actual = _validate(view, repo_root)
    for name, detail in _details(actual).items():
        previous = _details(original)[name]
        assert detail["items"] is None
        assert detail["returned_count"] == 0
        assert detail["omitted_count"] == detail["total_count"] == previous["total_count"]
        assert detail["detail_status"] == "omitted"
        assert detail["limit"] == 100
        expected_reasons = {"redacted_identity_details"}
        if capped:
            assert previous["total_count"] == 101
            assert previous["returned_count"] == 100
            assert previous["omitted_count"] == 1
            assert previous["omission_reasons"] == ["diagnostic_limit"]
            expected_reasons.add("diagnostic_limit")
        assert set(detail["omission_reasons"]) == expected_reasons
    assert _quantitative_evidence(actual) == _quantitative_evidence(original)
    assert not list(_identities(actual))
    for rendered in (render_json(view), render_markdown(view)):
        assert "redacted_identity_details" in rendered
        if capped:
            assert "diagnostic_limit" in rendered
