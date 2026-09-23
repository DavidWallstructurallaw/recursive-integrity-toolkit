"""Current workflow scheduling, frozen specifications and release result integrity.

Complete compatibility and delivery gates run for an explicitly selected candidate.
Historical dispatch and source-body migration tests remain in Git history.
"""

import ast
import hashlib
import re
import runpy
import tomllib

import pytest


def test_workflow_file_set_and_read_only_permissions(repo_root):
    paths = list((repo_root / ".github/workflows").glob("*.yml"))
    assert {p.name for p in paths} == {"ci.yml", "golden.yml", "security.yml", "release.yml"}
    for path in paths:
        text = path.read_text(encoding="utf-8")
        assert "permissions:\n  contents: read" in text
        assert "persist-credentials: false" in text
        assert "--phase " not in text and "--step " not in text
        assert "twine upload" not in text and "git push" not in text


def test_full_matrix_requires_explicit_candidate_selection(repo_root):
    text = (repo_root / ".github/workflows/ci.yml").read_text(encoding="utf-8")
    assert "pull_request:" in text
    assert "docs/**" not in text and "docs/lineage_contract.md" not in text.split("  workflow_dispatch:", 1)[0]
    assert "default: focused" in text and "options: [focused, candidate]" in text
    for job in ("core", "parquet", "performance", "hero", "security"):
        body = re.search(r"^  " + job + r":\n(.*?)(?=^  [a-z_]+:|\Z)", text, re.M | re.S).group(1)
        assert "github.event_name == 'workflow_dispatch' && inputs.gate == 'candidate'" in body
    focused = text.split("  focused:\n", 1)[1].split("\n  core:", 1)[0]
    assert "inputs.gate != 'candidate'" in focused
    assert "test_current_verification.py" in focused and "test_lineage_fixture_inputs.py" in focused
    assert "--ignore=tests/performance" not in focused and "tests/performance " not in focused
    assert 'os: [ubuntu-latest, windows-latest]' in text
    assert 'python-version: ["3.11", "3.12"]' in text
    assert 'dependencies: [current, minimum]' in text
    assert '"numpy==2.0.0" "pandas==2.2.2"' in text
    assert "find_spec('pyarrow') is None" in text and "--require-parquet" in text
    assert text.count("--ignore=tests/performance") == 2
    assert text.count("-q tests/performance --junitxml=") == 1
    assert "needs: [core, parquet, performance, hero, security]" in text


def test_candidate_checks_preserve_behavior_and_package_roles(repo_root):
    workflows = repo_root / ".github/workflows"
    for filename in ("golden.yml", "security.yml"):
        text = (workflows / filename).read_text(encoding="utf-8")
        assert "workflow_call:" in text and "workflow_dispatch:" in text
        assert "pull_request:" not in text
    golden = (workflows / "golden.yml").read_text(encoding="utf-8")
    assert "test_phase3_math.py" in golden and "test_phase4_reports.py" in golden
    assert "build_golden.py" not in golden
    security = (workflows / "security.yml").read_text(encoding="utf-8")
    for name in ("test_no_network.py", "test_PR015_redaction.py", "test_PR017_content_refs.py", "test_phase4_output_safety.py"):
        assert name in security
    release = (workflows / "release.yml").read_text(encoding="utf-8")
    for required in ("python -m build", "python -m twine check --strict", "--candidate", "SOURCE_DATE_EPOCH", "assert same_bytes", "assert payload_equal", "actions/download-artifact@v4", "source-commit.txt"):
        assert required in release
    assert "python -m pytest" not in release

def _release_tools(repo_root):
    return runpy.run_path(str(repo_root / "scripts/release_check.py"), run_name="phase2_release_test")


def test_current_workflows_never_mask_failed_commands(repo_root):
    for path in (repo_root / ".github/workflows").glob("*.yml"):
        text = path.read_text(encoding="utf-8")
        for unsafe in ("continue-on-error:", "|| true", "allow-failure:", "contents: write",
                       "id-token: write", "pull_request_target:", "ACTIONS_ALLOW_USE_UNSECURE_NODE_VERSION"):
            assert unsafe not in text, (path.name, unsafe)
        assert "shell: bash" in text
        assert "timeout-minutes:" in text
        assert "persist-credentials: false" in text


def test_current_approved_phase0_hashes_match_current_sources(repo_root):
    entries = re.findall(r"\| `([^`]+\.md)` \| `([0-9a-f]{64})` \|", (repo_root / "PHASE_0_APPROVAL.md").read_text(encoding="utf-8"))
    assert len(entries) == 16
    for name, expected in entries:
        assert hashlib.sha256((repo_root / name).read_bytes()).hexdigest() == expected, name


def test_current_package_version_is_consistent_without_protected_module_edit(repo_root):
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


def test_current_junit_gate_counts_passes(repo_root, tmp_path):
    result = _release_tools(repo_root)["verify_junit"](_junit(tmp_path, '<testcase classname="unit" name="valid"/>'))
    assert result == {"tests": 1, "passed": 1, "failed": 0, "skipped": 0, "real_parquet_cases": 0}


@pytest.mark.parametrize("tag", ["failure", "error", "skipped"])
def test_current_junit_gate_rejects_hidden_failures_and_skips(repo_root, tmp_path, tag):
    with pytest.raises(ValueError):
        _release_tools(repo_root)["verify_junit"](_junit(tmp_path, f'<testcase name="failed"><{tag}/></testcase>'))


@pytest.mark.parametrize("counter", ["failures", "errors", "skipped"])
def test_current_junit_gate_checks_suite_counters(repo_root, tmp_path, counter):
    with pytest.raises(ValueError):
        _release_tools(repo_root)["verify_junit"](_junit(tmp_path, '<testcase name="valid"/>', f'{counter}="1"'))


def test_current_junit_gate_requires_collected_cases(repo_root, tmp_path):
    with pytest.raises(ValueError):
        _release_tools(repo_root)["verify_junit"](_junit(tmp_path, ""))


def test_current_junit_gate_rejects_duplicate_case_identity(repo_root, tmp_path):
    with pytest.raises(ValueError):
        _release_tools(repo_root)["verify_junit"](_junit(tmp_path, '<testcase name="same"/><testcase name="same"/>'))


def test_current_junit_gate_rejects_insufficient_requested_count(repo_root, tmp_path):
    with pytest.raises(ValueError):
        _release_tools(repo_root)["verify_junit"](_junit(tmp_path, '<testcase name="one"/>'), minimum=2)


def test_current_junit_gate_requires_actual_parquet_cases(repo_root, tmp_path):
    with pytest.raises(ValueError):
        _release_tools(repo_root)["verify_junit"](_junit(tmp_path, '<testcase name="mock_parquet"/>'), require_parquet=True)


def test_current_junit_gate_accepts_three_real_case_names(repo_root, tmp_path):
    names = ("test_PR002_parquet_real_roundtrip", "test_PR002_parquet_real_row_limit", "test_PR002_parquet_real_invalid_file")
    body = "".join(f'<testcase classname="real" name="{name}"/>' for name in names)
    result = _release_tools(repo_root)["verify_junit"](_junit(tmp_path, body, 'tests="3"'), require_parquet=True)
    assert result["real_parquet_cases"] == 3
