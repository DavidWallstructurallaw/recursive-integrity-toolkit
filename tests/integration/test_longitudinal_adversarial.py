"""Bounded Step 8 adversarial cases at the public series boundary.

The arithmetic expectations come from constructed populations and parent sets.
These cases cover loaded snapshots, late shared-budget exhaustion, and complete
aggregates whose displayed identities cross the existing 100-row boundary.
"""
from collections import Counter

import pytest

from recursive_integrity_toolkit.errors import CanonicalValidationError, ErrorCode
from recursive_integrity_toolkit.lineage.graph import LineageLimits
from recursive_integrity_toolkit.metrics import longitudinal as series
from recursive_integrity_toolkit.models import TailSelectionOptions
from recursive_integrity_toolkit.reports.assembly import assemble_report, privacy_view
from recursive_integrity_toolkit.reports.json_report import render_json
from recursive_integrity_toolkit.reports.markdown_report import render_markdown
from recursive_integrity_toolkit.utils.hashing import IdentifierProtection
from test_longitudinal_reports import _checked, _declarations, _load, _run, _value


def _case(selected, *, context=(), states=None, parents=None):
    """Create ordinary loaded files with explicit chronology and full provenance."""
    rows, provenance = [], []
    for version in (*context, *selected):
        for index, state in enumerate((states or {}).get(version, ("topic",))):
            record_id = f"r{index:04d}"
            parent_ids = (parents or {}).get((version, index), [])
            rows.append({"dataset_version": version, "record_id": record_id,
                         "content": f"bounded {version} {record_id}", "topic": state})
            provenance.append({"dataset_version": version, "record_id": record_id,
                "source_type": "synthetic" if parent_ids else "human",
                "provenance_confidence": "confirmed",
                "external_grounding": "no" if parent_ids else "yes",
                "parent_ids": parent_ids,
                "transformation": "generate"})
    representation = {"name": "topic", "source": "topic_field", "field": "topic",
        "version": "adversarial-topics-v1", "missing_value_policy": "exclude",
        "state_semantics": "Literal declared topic identity"}
    return {"selected_versions": list(selected), "context_versions": list(context),
        "records": rows, "provenance": provenance,
        "representations": {version: dict(representation) for version in selected},
        "order_document": {"version_order": [*context, *selected]}}


def _selection(case, bundle, baseline="none"):
    return series.select_longitudinal_versions(bundle, declarations=_declarations(case),
                                               baseline=baseline)


def _assert_no_identity_copies(value):
    """Series rows must refer to scopes instead of embedding complete populations."""
    if isinstance(value, dict):
        assert not {"included_record_keys", "excluded_record_keys", "external_root_keys",
                    "root_contributions", "records"}.intersection(value)
        for item in value.values():
            _assert_no_identity_copies(item)
    elif isinstance(value, list):
        for item in value:
            _assert_no_identity_copies(item)


@pytest.mark.parametrize("baseline,expected_count", [("none", 99), ("first", 197)])
def test_one_hundred_loaded_snapshots_execute_only_the_linear_schedule(
        tmp_path, monkeypatch, baseline, expected_count):
    selected = tuple(f"v{index:03d}" for index in range(100))
    case = _case(selected, context=("context_a", "context_b"))
    bundle = _load(case, tmp_path)
    selection = _selection(case, bundle, baseline)
    counts = Counter()
    snapshot_kernel, pair_kernel = series._snapshot_distribution, series._pair_result

    def snapshot(scope, *args, **kwargs):
        counts[scope.dataset_version] += 1
        return snapshot_kernel(scope, *args, **kwargs)

    def pair(descriptor, *args, **kwargs):
        counts[descriptor.earlier_version, descriptor.later_version] += 1
        return pair_kernel(descriptor, *args, **kwargs)

    monkeypatch.setattr(series, "_snapshot_distribution", snapshot)
    monkeypatch.setattr(series, "_pair_result", pair)
    result = series.analyze_longitudinal(bundle, selection=selection)
    expected = {(selected[index - 1], selected[index]) for index in range(1, 100)}
    if baseline == "first":
        expected |= {(selected[0], version) for version in selected[1:]}
    assert len(expected) == expected_count
    assert counts == Counter({key: 1 for key in (*selected, *expected)})
    assert len(bundle.version_order.loaded_versions) == 102
    assert selection.max_versions == len(result.snapshots) == 100
    assert selection.context_versions == ("context_a", "context_b")
    payload = _checked(assemble_report(bundle, run=_run(), longitudinal=result))
    inputs = payload["inputs"]["longitudinal"]
    versions = {row["snapshot_id"]: row["dataset_version"] for row in inputs["snapshots"]}
    assert {(versions[row["earlier_snapshot_id"]], versions[row["later_snapshot_id"]])
            for row in inputs["comparisons"]} == expected
    assert inputs["comparison_count"] == expected_count
    assert len(inputs["scopes"]) == 200 + 2 * expected_count
    assert len(payload["derived_metrics"]["longitudinal"]["comparisons"]) == expected_count
    for section in ("inputs", "observed_facts", "derived_metrics"):
        _assert_no_identity_copies(payload[section]["longitudinal"])
    # Assembly must not dispatch any extra snapshot or pair kernel.
    assert counts == Counter({key: 1 for key in (*selected, *expected)})


def test_one_hundred_one_loaded_snapshots_fail_before_any_snapshot_kernel(tmp_path, monkeypatch):
    case = _case(tuple(f"v{index:03d}" for index in range(101)))
    bundle = _load(case, tmp_path)

    def forbidden(*args, **kwargs):
        raise AssertionError("over-limit selection performed analytical work")

    monkeypatch.setattr(series, "_snapshot_distribution", forbidden)
    monkeypatch.setattr(series, "_pair_result", forbidden)
    with pytest.raises(CanonicalValidationError) as error:
        _selection(case, bundle, "first")
    assert error.value.code is ErrorCode.LONGITUDINAL_RESOURCE_LIMIT_EXCEEDED
    failed = series.analyze_longitudinal_failure(bundle, declarations=_declarations(case),
                                                baseline="first")
    assert failed.snapshots == () and failed.selected_version_count == 101
    payload = _checked(assemble_report(bundle, run=_run(), longitudinal_failure=failed))
    inputs = payload["inputs"]["longitudinal"]
    assert inputs["selected_version_count"] == 101 and inputs["comparison_count"] == 0
    assert inputs["snapshots"] == inputs["scopes"] == inputs["comparisons"] == []
    assert payload["capabilities"]["dataset_longitudinal"]["longitudinal_execution"]["status"] == "failed"


def _assert_detail(table, expected):
    assert table["limit"] == 100
    assert table["total_count"] == len(expected)
    assert table["returned_count"] == 100
    assert table["omitted_count"] == len(expected) - 100
    assert table["items"] == sorted(expected)[:100]


def test_large_state_sets_and_context_are_capped_after_complete_aggregate_calculation(tmp_path):
    old = {f"OLD_{index:03d}" for index in range(125)}
    new = {f"NEW_{index:03d}" for index in range(125)}
    retained = {f"SAME_{index:03d}" for index in range(125)}
    context = tuple(f"context_{index:03d}" for index in range(101))
    case = _case(("v1", "v2"), context=context,
                 states={"v1": sorted(old | retained), "v2": sorted(new | retained)})
    bundle = _load(case, tmp_path)
    result = series.analyze_longitudinal(bundle, selection=_selection(case, bundle),
        lineage=True, tail_options=TailSelectionOptions("singleton_count"))
    report = assemble_report(bundle, run=_run(), longitudinal=result)
    payload = _checked(report)
    inputs = payload["inputs"]["longitudinal"]
    assert inputs["selected_version_count"] == 2 and inputs["context_version_count"] == 101
    _assert_detail(inputs["context_versions"], context)
    comparison = payload["derived_metrics"]["longitudinal"]["comparisons"][0]
    for name, expected in (("extinct_states", old), ("added_states", new),
                           ("retained_states", retained), ("tail_extinct_states", old)):
        _assert_detail(_value(comparison, name), expected)
    assert _value(comparison, "support_loss_count") == 125
    assert _value(comparison, "support_added_count") == 125
    assert _value(comparison, "tail_extinction_count") == 125
    assert _value(comparison, "support_retention_ratio") == 0.5
    assert _value(comparison, "support_delta") == 0
    for row in payload["derived_metrics"]["longitudinal"]["snapshots"]:
        assert _value(row, "support_size") == 250
        assert _value(row, "gini_simpson_diversity") == pytest.approx(249 / 250)
        assert _value(row, "distinct_external_root_count") == 250
        assert _value(row, "ancestry_concentration_hhi") == pytest.approx(1 / 250)
        assert _value(row, "effective_external_root_count") == pytest.approx(250)
    assert payload["observed_facts"]["longitudinal"]["shared_lineage"]["loaded_record_count"] == 601
    for section in ("inputs", "observed_facts", "derived_metrics"):
        _assert_no_identity_copies(payload[section]["longitudinal"])
    for mode in ("hash", "omit"):
        view = privacy_view(report, mode="redacted", record_id_mode=mode,
            protection=IdentifierProtection(secret=b"step-eight-adversarial-privacy-key"))
        safe = _checked(view)
        states = safe["derived_metrics"]["longitudinal"]["comparisons"][0]["extinct_states"]["value"]
        assert states["total_count"] == 125
        assert states["returned_count"] == (100 if mode == "hash" else 0)
        assert states["omitted_count"] == (25 if mode == "hash" else 125)
        assert (states["items"] is None) == (mode == "omit")
        wire = render_json(view) + render_markdown(view)
        assert "OLD_" not in wire and "NEW_" not in wire and "SAME_" not in wire
        assert "context_100" not in wire


@pytest.mark.parametrize("limit,maximum,attempted", [
    ("max_root_memberships", 350, 351), ("max_root_union_visits", 299, 300)])
def test_late_root_budget_exhaustion_is_shared_across_snapshots_and_baseline_pairs(
        tmp_path, limit, maximum, attempted):
    versions = ("v1", "v2", "v3")
    states = {version: ("topic",) * 100 for version in ("roots", *versions)}
    parents = {(version, index): [f"roots::r{index:04d}"]
               for version in versions for index in range(100)}
    case = _case(versions, context=("roots",), states=states, parents=parents)
    bundle = _load(case, tmp_path)
    selection = _selection(case, bundle, "first")
    result = series.analyze_longitudinal(bundle, selection=selection, lineage=True,
        lineage_limits=LineageLimits(**{limit: maximum}))
    usage = result.shared_lineage.resource_usage
    assert usage.exhausted_limit == limit and usage.attempted_value == attempted
    assert len(result.comparisons) == 3
    assert all(target.resource_usage is usage for target in result.shared_lineage.targets)
    assert all(target.records is None and target.root_contributions is None
               for target in result.shared_lineage.targets)
    payload = _checked(assemble_report(bundle, run=_run(), longitudinal=result))
    for row in payload["derived_metrics"]["longitudinal"]["snapshots"]:
        assert _value(row, "support_size") == 1
        assert _value(row, "distinct_external_root_count") is None
        assert _value(row, "ancestry_concentration_hhi") is None
        assert _value(row, "resolved_parent_edge_coverage") == 1
    for row in payload["derived_metrics"]["longitudinal"]["comparisons"]:
        assert _value(row, "distinct_external_root_count_delta") is None
        assert _value(row, "resolved_parent_edge_coverage_delta") == 0
        assert _value(row, "record_count_delta") == 0
    execution = payload["capabilities"]["dataset_longitudinal"]["longitudinal_execution"]
    assert execution["status"] == "partial"
