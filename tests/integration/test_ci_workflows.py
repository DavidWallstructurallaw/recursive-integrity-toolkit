"""Preserve workflow guarantees while moving active gates to Phase 3 Step 1."""

from pathlib import Path

EXPECTED = {"ci.yml", "golden.yml", "security.yml", "release.yml"}
FORBIDDEN_WORKFLOW_TERMS = {"services:", "docker run", "fastapi", "streamlit", "telemetry", "publish-package"}


def test_workflow_file_set_and_basic_contract(repo_root: Path) -> None:
    workflow_root = repo_root / ".github" / "workflows"
    assert {path.name for path in workflow_root.glob("*.yml")} == EXPECTED
    for path in sorted(workflow_root.glob("*.yml")):
        text = path.read_text(encoding="utf-8")
        assert text.startswith("name:")
        assert "permissions:\n  contents: read" in text
        assert "actions/checkout@v4" in text
        assert "actions/setup-python@v5" in text
        assert "\t" not in text


def test_workflows_preserve_phase_boundary(repo_root: Path) -> None:
    combined = "\n".join(p.read_text(encoding="utf-8").lower() for p in (repo_root / ".github/workflows").glob("*.yml"))
    for term in FORBIDDEN_WORKFLOW_TERMS:
        assert term not in combined
    assert "test_no_algorithms.py" in combined
    assert "test_no_network.py" in combined
    assert "python -m build" in combined
    assert "rit version" in combined
    assert "--phase 3 --step 1" in combined
    assert "release_check.py --diff" not in combined


import ast
import hashlib
import re
import runpy
import tomllib
import pytest


def _release_tools(repo_root):
    return runpy.run_path(str(repo_root / "scripts/release_check.py"), run_name="phase2_release_test")


def test_phase2_workflows_never_mask_failed_commands(repo_root):
    for path in (repo_root / ".github/workflows").glob("*.yml"):
        text = path.read_text(encoding="utf-8")
        for unsafe in ("continue-on-error:", "|| true", "allow-failure:", "contents: write",
                       "id-token: write", "pull_request_target:", "ACTIONS_ALLOW_USE_UNSECURE_NODE_VERSION"):
            assert unsafe not in text, (path.name, unsafe)
        assert "shell: bash" in text
        assert "timeout-minutes:" in text
        assert "persist-credentials: false" in text


def test_phase2_core_and_real_parquet_have_independent_complete_runs(repo_root):
    text = (repo_root / ".github/workflows/ci.yml").read_text(encoding="utf-8")
    assert 'os: [ubuntu-latest, windows-latest]' in text
    assert 'python-version: ["3.11", "3.12"]' in text
    assert 'RIT_TEST_PARQUET: "0"' in text and 'RIT_TEST_PARQUET: "1"' in text
    assert 'python -m pip install ".[test,parquet]"' in text
    assert "--require-parquet" in text
    assert "find_spec('pyarrow') is None" in text
    assert text.count("python -m pytest -p no:cacheprovider -q --junitxml=") == 2
    assert " -k " not in text


def test_phase2_delivery_builds_both_formats_and_tests_installed_wheel(repo_root):
    # Same identity and safety guarantees; only the active artifact stage changes.
    text = (repo_root / ".github/workflows/release.yml").read_text(encoding="utf-8")
    for required in ("python -m build", "python -m twine check --strict", "--dist", "--candidate",
                     "--require-parquet", "actions/upload-artifact@v4", "retention-days: 90",
                     "if-no-files-found: error", "phase3_test_results.log", "phase3_build_results.log"):
        assert required in text
    assert "--delivery" not in text and "twine upload" not in text and "git push" not in text
    script = (repo_root / "scripts/release_check.py").read_text(encoding="utf-8")
    for required in ('"--no-index", "--no-deps"', '"-I"', '"--prefix=recursive-integrity-toolkit/"',
                     '"recursive-integrity-toolkit-phase3-step1-candidate.zip"', '"phase3_artifacts.sha256"'):
        assert required in script


def test_phase2_hero_workflow_preserves_scaffold_only_golden_boundary(repo_root):
    text = (repo_root / ".github/workflows/golden.yml").read_text(encoding="utf-8")
    body = "\n".join(line for line in text.splitlines() if not line.lstrip().startswith("#"))
    assert "test_hero_structure.py" in body
    assert "build_golden.py" not in body and "normalize_golden.py" not in body


def test_phase2_completion_records_exist_and_do_not_authorize_phase3(repo_root):
    for name in ("PHASE_2_COMPLETION.md", "PHASE_2_VALIDATION_REPORT.md", "PHASE_2_ARCHITECTURE_COMPLIANCE_REPORT.md"):
        text = (repo_root / name).read_text(encoding="utf-8")
        assert "Phase 3" in text and "not authorized" in text


def test_phase2_approved_phase0_hashes_match_current_sources(repo_root):
    entries = re.findall(r"\| `([^`]+\.md)` \| `([0-9a-f]{64})` \|", (repo_root / "PHASE_0_APPROVAL.md").read_text(encoding="utf-8"))
    assert len(entries) == 16
    for name, expected in entries:
        assert hashlib.sha256((repo_root / name).read_bytes()).hexdigest() == expected, name


def test_phase2_package_version_is_consistent_without_protected_module_edit(repo_root):
    project = tomllib.loads((repo_root / "pyproject.toml").read_text(encoding="utf-8"))["project"]
    tree = ast.parse((repo_root / "src/recursive_integrity_toolkit/__init__.py").read_text(encoding="utf-8"))
    value = [ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign)
             and any(isinstance(t, ast.Name) and t.id == "__version__" for t in n.targets)]
    assert value == [project["version"]]
    assert project["dependencies"] == ["numpy>=2.0", "pandas>=2.2"]


def _junit(tmp_path, body, counts='tests="1" errors="0" failures="0" skipped="0"'):
    path = tmp_path / "synthetic-junit.xml"
    path.write_text(f'<testsuites><testsuite {counts}>{body}</testsuite></testsuites>', encoding="utf-8")
    return path


def test_phase2_junit_gate_counts_passes(repo_root, tmp_path):
    result = _release_tools(repo_root)["verify_junit"](_junit(tmp_path, '<testcase classname="unit" name="valid"/>'))
    assert result == {"tests": 1, "passed": 1, "failed": 0, "skipped": 0, "real_parquet_cases": 0}


@pytest.mark.parametrize("tag", ["failure", "error", "skipped"])
def test_phase2_junit_gate_rejects_hidden_failures_and_skips(repo_root, tmp_path, tag):
    with pytest.raises(ValueError):
        _release_tools(repo_root)["verify_junit"](_junit(tmp_path, f'<testcase name="failed"><{tag}/></testcase>'))


@pytest.mark.parametrize("counter", ["failures", "errors", "skipped"])
def test_phase2_junit_gate_checks_suite_counters(repo_root, tmp_path, counter):
    with pytest.raises(ValueError):
        _release_tools(repo_root)["verify_junit"](_junit(tmp_path, '<testcase name="valid"/>', f'{counter}="1"'))


def test_phase2_junit_gate_requires_collected_cases(repo_root, tmp_path):
    with pytest.raises(ValueError):
        _release_tools(repo_root)["verify_junit"](_junit(tmp_path, ""))


def test_phase2_junit_gate_rejects_duplicate_case_identity(repo_root, tmp_path):
    with pytest.raises(ValueError):
        _release_tools(repo_root)["verify_junit"](_junit(tmp_path, '<testcase name="same"/><testcase name="same"/>'))


def test_phase2_junit_gate_requires_full_core_count(repo_root, tmp_path):
    with pytest.raises(ValueError):
        _release_tools(repo_root)["verify_junit"](_junit(tmp_path, '<testcase name="one"/>'), minimum=1131)


def test_phase2_junit_gate_requires_actual_parquet_cases(repo_root, tmp_path):
    with pytest.raises(ValueError):
        _release_tools(repo_root)["verify_junit"](_junit(tmp_path, '<testcase name="mock_parquet"/>'), require_parquet=True)


def test_phase2_junit_gate_accepts_three_real_case_names(repo_root, tmp_path):
    names = ("test_PR002_parquet_real_roundtrip", "test_PR002_parquet_real_row_limit", "test_PR002_parquet_real_invalid_file")
    body = "".join(f'<testcase classname="real" name="{name}"/>' for name in names)
    result = _release_tools(repo_root)["verify_junit"](_junit(tmp_path, body, 'tests="3"'), require_parquet=True)
    assert result["real_parquet_cases"] == 3


def test_phase2_runtime_gates_remain_exact_allowlists(repo_root):
    script = (repo_root / "scripts/check_traceability.py").read_text(encoding="utf-8")
    assert "ALLOWED_FUNCTIONS" in script and "ALLOWED_CORE_IMPORTS" in script
    for term in ("numpy", "pandas", "networkx", "transformers"):
        assert term in script
    assert "protected docstring-only modules" in script


def _restoration_bytes(repo_root):
    after = (repo_root / "VALIDATION_PLAN.md").read_bytes()
    before = after.replace(b"| Status | APPROVED PHASE 0 BASELINE |", b"| Status | DRAFT VALIDATION BASELINE |", 1)
    before = before.replace(b"Definitions marked `APPROVED DECISION`", b"Definitions marked `PENDING DECISION`", 1)
    return before, after


def test_phase2_restoration_accepts_only_original_approved_transition(repo_root):
    tools = _release_tools(repo_root)
    before, after = _restoration_bytes(repo_root)
    result = tools["verify_approved_restoration"]("VALIDATION_PLAN.md", "M", before, after)
    assert result["after_sha256"] == "16f5fe539da2b3cff1c3e0a2854208bd7fbc1e4c5b332684265b06a03a90cf2f"
    assert "VALIDATION_PLAN.md" not in tools["STEP10_ALLOWED"]


@pytest.mark.parametrize("change", ["path", "added", "deleted", "before", "after", "unchanged", "type"])
def test_phase2_restoration_rejects_wider_changes(repo_root, change):
    verify = _release_tools(repo_root)["verify_approved_restoration"]
    before, after = _restoration_bytes(repo_root)
    path, status = "VALIDATION_PLAN.md", "M"
    if change == "path": path = "DEFINITIONS_AND_UNITS.md"
    elif change == "added": status = "A"
    elif change == "deleted": status = "D"
    elif change == "before": before += b"\n"
    elif change == "after": after += b"\n"
    elif change == "unchanged": after = before
    elif change == "type": after = after.decode("utf-8")
    with pytest.raises(ValueError):
        verify(path, status, before, after)
