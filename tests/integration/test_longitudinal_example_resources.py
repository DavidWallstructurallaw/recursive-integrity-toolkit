"""Public example resources preserve the independently authored three-version case."""
from fractions import Fraction
from importlib.resources import files
import json
from pathlib import Path

import pytest

from recursive_integrity_toolkit.config import RepresentationConfig
from recursive_integrity_toolkit.io.validation import validate_bundle
from recursive_integrity_toolkit.metrics import longitudinal as series
from recursive_integrity_toolkit.models import AuditBundle, FileRole, InputSource, TailSelectionOptions


ROOT = Path(__file__).resolve().parents[2]
EXAMPLE = ROOT / "examples/longitudinal"
NAMES = ("config.json", "records_v1.jsonl", "records_v2.jsonl", "records_v3.jsonl",
         "provenance.jsonl", "version_order.json", "EXPECTED_OUTPUTS.md")


def _resources():
    return files("recursive_integrity_toolkit").joinpath("data", "longitudinal")


def _rows(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


@pytest.mark.parametrize("name", NAMES)
def test_packaged_longitudinal_resources_match_public_inputs(name):
    assert _resources().joinpath(name).read_bytes() == (EXAMPLE / name).read_bytes()


def test_public_rows_preserve_independent_fixture_including_missing_provenance():
    cases = json.loads((ROOT / "tests/fixtures/longitudinal/cases.json").read_text())
    oracle = next(case for case in cases["cases"] if case["case_id"] == "observed_three_version")
    assert [row for version in ("v1", "v2", "v3")
            for row in _rows(EXAMPLE / f"records_{version}.jsonl")] == oracle["records"]
    assert _rows(EXAMPLE / "provenance.jsonl") == oracle["provenance"]
    assert json.loads((EXAMPLE / "version_order.json").read_text()) == oracle["order_document"]
    configuration = json.loads((EXAMPLE / "config.json").read_text())
    assert configuration["longitudinal"] == {
        "state_semantics": oracle["representations"]["v1"]["state_semantics"]}
    assert configuration["representation"] == {
        key: value for key, value in oracle["representations"]["v1"].items()
        if key != "state_semantics"}


@pytest.mark.parametrize("baseline,tail", [("none", False), ("first", True)])
def test_copied_package_inputs_execute_with_independent_expected_values(tmp_path, monkeypatch,
                                                                       baseline, tail):
    # The working directory and every input path are outside the checkout.
    monkeypatch.chdir(tmp_path)
    for name in NAMES:
        (tmp_path / name).write_bytes(_resources().joinpath(name).read_bytes())
    configuration = json.loads((tmp_path / "config.json").read_text())
    validation = validate_bundle(AuditBundle((
        InputSource(FileRole.RECORDS_PRIMARY, tmp_path / "records_v3.jsonl"),
        InputSource(FileRole.RECORDS_COMPARE, tmp_path / "records_v2.jsonl"),
        InputSource(FileRole.RECORDS_COMPARE, tmp_path / "records_v1.jsonl"),
        InputSource(FileRole.PROVENANCE_MANIFEST, tmp_path / "provenance.jsonl"),
        InputSource(FileRole.VERSION_ORDER, tmp_path / "version_order.json"),
    )))
    representation = RepresentationConfig(**configuration["representation"])
    declarations = tuple(series.SnapshotDeclaration(version, representation,
        configuration["longitudinal"]["state_semantics"]) for version in ("v1", "v2", "v3"))
    selection = series.select_longitudinal_versions(validation, declarations=declarations,
                                                    baseline=baseline)
    result = series.analyze_longitudinal(validation, selection=selection,
        tail_options=TailSelectionOptions("singleton_count") if tail else None)
    assert result.execution_status.value == "completed"
    assert selection.selected_order == ("v1", "v2", "v3")
    assert "W_PROVENANCE_MISSING_ROW" in {message.code for message in validation.validation_messages}
    assert [item.record_count.value for item in result.snapshots] == [4, 4, 3]
    assert [item.distribution.unweighted.support_size.value for item in result.snapshots] == [3, 2, 3]
    assert [item.distribution.unweighted.gini_simpson_diversity.value
            for item in result.snapshots] == pytest.approx([5 / 8, 1 / 2, 2 / 3])
    assert [item.provenance.missing_provenance_count.value for item in result.snapshots] == [0, 1, 0]
    for item, expected in zip(result.snapshots,
            (("0", "0", "0"), ("1/4", "1/2", "1/4"), ("1/3", "2/3", "1/3")), strict=True):
        assert [getattr(item.direct_closure, field).value
                for field in ("lower_bound", "upper_bound", "interval_width")] == pytest.approx(
                    [float(Fraction(value)) for value in expected])
    expected_pairs = {
        ("v1", "v2"): (0, -1, "-1/8", ("B", "C"), ("D",), "-1/4", "1/4"),
        ("v2", "v3"): (-1, 1, "1/6", (), ("B",), "1/4", "1/12"),
    }
    if baseline == "first":
        expected_pairs["v1", "v3"] = (-1, 0, "1/24", ("C",), ("D",), "0", "1/3")
    assert len(result.comparisons) == len(expected_pairs)
    for pair in result.comparisons:
        expected = expected_pairs[pair.pair.earlier_version, pair.pair.later_version]
        deltas = {delta.metric_name: delta.value for delta in pair.deltas}
        assert deltas["record_count_delta"] == expected[0]
        assert deltas["support_delta"] == expected[1]
        assert deltas["gini_simpson_diversity_delta"] == pytest.approx(float(Fraction(expected[2])))
        assert pair.support_comparison.extinct_states == expected[3]
        assert pair.support_comparison.added_states == expected[4]
        assert deltas["provenance_row_coverage_delta"] == pytest.approx(float(Fraction(expected[5])))
        assert deltas["direct_closure_lower_bound_delta"] == pytest.approx(float(Fraction(expected[6])))
        if tail:
            assert pair.tail_disappearance.tail_extinct_states == expected[3]
        else:
            assert pair.tail_disappearance is None
        assert pair.lineage_deltas == ()
