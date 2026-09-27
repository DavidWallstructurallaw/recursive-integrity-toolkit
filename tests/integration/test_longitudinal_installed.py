"""Explicit clean-install Step 7 checks, run outside the source checkout.

This file uses sys.executable by default, as in wheel-installed CI. A separate
wheel-installed environment can be selected explicitly:
RIT_STEP7_INSTALLED_PYTHON=/absolute/environment/bin/python pytest <this file>
The tests never invoke pip or download dependencies. A missing installed
distribution is a setup error, not a silent skip. Source-only runs can provide
the override or exclude this file with --ignore.
"""
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

from test_longitudinal_cli import FORMATS, ROOT, _inputs


RUNNER = r'''
import pathlib, runpy, socket, sys, urllib.request
def denied(*args, **kwargs):
    raise AssertionError("installed longitudinal CLI attempted network access")
socket.socket.connect = denied
socket.socket.connect_ex = denied
socket.create_connection = denied
urllib.request.urlopen = denied
import recursive_integrity_toolkit
repo = pathlib.Path(sys.argv.pop(1)).resolve()
package = pathlib.Path(recursive_integrity_toolkit.__file__).resolve()
assert not package.is_relative_to(repo), "installed check imported the source checkout"
assert "site-packages" in package.parts, "installed check requires a real installed distribution"
assert not pathlib.Path.cwd().is_relative_to(repo), "installed check ran inside the checkout"
sys.argv[0] = "rit"
runpy.run_module("recursive_integrity_toolkit", run_name="__main__")
'''


@pytest.fixture(scope="module")
def installed_python():
    value = os.environ.get("RIT_STEP7_INSTALLED_PYTHON", sys.executable)
    path = Path(value)
    assert path.is_absolute() and path.is_file(), "Installed interpreter must be an existing absolute path"
    return path


def _invoke(python, directory, args):
    directory.mkdir(parents=True, exist_ok=True)
    assert not directory.resolve().is_relative_to(ROOT.resolve())
    env = os.environ.copy()
    env.pop("PYTHONPATH", None)
    env.pop("PYTHONHOME", None)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run([str(python), "-I", "-c", RUNNER, str(ROOT), *args],
                            cwd=directory, env=env, text=True, capture_output=True,
                            timeout=60, check=False)
    assert "Traceback" not in result.stderr, result.stderr
    return result


def _report(directory):
    from recursive_integrity_toolkit.result import validate_report
    payload = json.loads((directory / "report.json").read_text())
    validate_report(payload)
    assert payload["run"]["report_schema_version"] == "1.2"
    assert payload["run"]["toolkit_version"] == "0.1.0.dev4"
    assert payload["run"]["network_call_count"] == 0
    assert payload["simulations"] == {}
    assert payload["capabilities"] == payload["observability"]["capabilities"]
    assert (directory / "report.md").read_text().startswith("# Recursive Integrity Audit Report\n")
    return payload


@pytest.mark.parametrize("dataset", ["hero", "longitudinal"])
@pytest.mark.parametrize("redacted", [False, True])
@pytest.mark.parametrize("lineage", [False, True])
def test_packaged_examples_outside_checkout_with_network_blocked(installed_python, tmp_path, dataset, redacted, lineage):
    out = tmp_path / "example"
    args = ["example", "--longitudinal", "--dataset", dataset, "--out", str(out)]
    if redacted:
        args += ["--redacted"]
    if lineage:
        args += ["--lineage"]
    result = _invoke(installed_python, tmp_path, args)
    assert result.returncode == 0, result.stderr
    report = _report(out / "reports")
    snapshots = report["derived_metrics"]["longitudinal"]["snapshots"]
    comparisons = report["derived_metrics"]["longitudinal"]["comparisons"]
    assert len(snapshots) == (2 if dataset == "hero" else 3)
    assert len(comparisons) == (1 if dataset == "hero" else 2)
    if dataset == "hero":
        assert comparisons[0]["direct_closure_lower_bound_delta"]["value"] == 0.5
        if lineage:
            assert comparisons[0]["distinct_external_root_count_delta"]["value"] == -3
            assert comparisons[0]["ancestry_concentration_hhi_delta"]["value"] == 0.125
            assert comparisons[0]["effective_external_root_count_delta"]["value"] == -4
        for name in ("records_v1.csv", "records_v2.csv", "provenance.csv", "config.json", "version_order.json"):
            assert (out / "inputs" / name).read_bytes() == (ROOT / "examples/hero" / name).read_bytes()
    else:
        assert [row["support_size"]["value"] for row in snapshots] == [3, 2, 3]
        assert [row["gini_simpson_diversity_delta"]["value"] for row in comparisons] == pytest.approx([-1 / 8, 1 / 6])
        assert [row["direct_closure_lower_bound_delta"]["value"] for row in comparisons] == pytest.approx([1 / 4, 1 / 12])
        for name in ("records_v1.jsonl", "records_v2.jsonl", "records_v3.jsonl", "provenance.jsonl", "config.json", "version_order.json"):
            assert (out / "inputs" / name).read_bytes() == (ROOT / "examples/longitudinal" / name).read_bytes()
    if not lineage:
        assert report["observed_facts"]["longitudinal"]["shared_lineage"] is None
    if redacted:
        sinks = json.dumps(report) + (out / "reports/report.md").read_text() + result.stdout + result.stderr
        assert str(tmp_path) not in sinks
    assert report["run"]["privacy_mode"] == ("redacted" if redacted else "standard")


@pytest.mark.parametrize("format", FORMATS)
@pytest.mark.parametrize("record_ids", ["preserve", "hash", "omit"])
def test_installed_record_loaders_baseline_and_privacy_modes(installed_python, tmp_path, format, record_ids):
    _, args, _, _, _ = _inputs(tmp_path / "inputs", format=format)
    out = tmp_path / "out"
    extra = [] if record_ids == "preserve" else ["--redacted", "--record-ids", record_ids]
    result = _invoke(installed_python, tmp_path, ["audit", *args, "--baseline", "first", *extra, "--out", str(out)])
    assert result.returncode == 0, result.stderr
    report = _report(out)
    pairs = report["derived_metrics"]["longitudinal"]["comparisons"]
    assert [row["support_delta"]["value"] for row in pairs] == [-1, 0, 1]
    assert [row["gini_simpson_diversity_delta"]["value"] for row in pairs] == pytest.approx([-1 / 8, 1 / 24, 1 / 6])
    if record_ids != "preserve":
        sinks = json.dumps(report) + (out / "report.md").read_text() + result.stdout + result.stderr
        assert str(tmp_path) not in sinks and "Fixture v1 record" not in sinks


def test_installed_validate_enabled_config_keeps_series_unrequested(installed_python, tmp_path):
    _, args, _, _, _ = _inputs(tmp_path / "inputs", config_inputs=True)
    out = tmp_path / "validated"
    result = _invoke(installed_python, tmp_path, ["validate", *args, "--out", str(out)])
    assert result.returncode == 0, result.stderr
    report = _report(out)
    assert report["derived_metrics"] == {"longitudinal": {"snapshots": [], "comparisons": []}}
    assert report["capabilities"]["dataset_longitudinal"]["execution_status"] == "not_requested"
