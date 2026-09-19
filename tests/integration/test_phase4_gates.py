"""Current Phase 4 governance, immutable-source mutations and active workflows."""
import hashlib
import runpy
import shutil
import subprocess
import sys

import pytest


@pytest.fixture(scope="module")
def phase4_gate_tools(repo_root):
    return runpy.run_path(str(repo_root / "scripts/release_check.py"), run_name="phase4_gate_tests")


@pytest.fixture(scope="module")
def phase4_mutation_tree(repo_root, tmp_path_factory, phase4_gate_tools):
    """One source copy; each individual mutation is restored in a finally block."""
    root = tmp_path_factory.mktemp("phase4-active-mutations")
    tracked = subprocess.check_output(["git", "-C", str(repo_root), "ls-files", "-z"])
    paths = set(tracked.decode().split("\0")) - {""}
    paths.update(phase4_gate_tools["PHASE4_STEP1_NEW"])
    for relative in sorted(paths):
        destination = root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(repo_root / relative, destination)
    return root


def test_phase4_current_tree_passes_governance_snapshot(phase4_gate_tools, phase4_mutation_tree):
    phase4_gate_tools["verify_phase4_snapshot"](phase4_mutation_tree)


@pytest.mark.parametrize("relative", [
    "PROJECT_INSTRUCTIONS.md",
    "SPEC_AUDIT.md",
    "PHASE_3_BASELINE.json",
    "PHASE_3_COMPLETION.md",
    "PHASE_4_PLAN.md",
    "pyproject.toml",
    "schemas/report.schema.json",
    "tests/golden/phase3_math_cases.json",
    "examples/hero/records_v2.csv",
    "examples/hero/EXPECTED_OUTPUTS.md",
    "src/recursive_integrity_toolkit/models.py",
    "src/recursive_integrity_toolkit/metrics/diversity.py",
    "src/recursive_integrity_toolkit/io/validation.py",
    "src/recursive_integrity_toolkit/reports/assembly.py",
    "src/recursive_integrity_toolkit/cli.py",
])
def test_phase4_snapshot_rejects_protected_byte_changes(phase4_gate_tools, phase4_mutation_tree, relative):
    path = phase4_mutation_tree / relative
    original = path.read_bytes()
    # Exercise actual formula/oracle/dependency changes as well as any-byte
    # preservation. These mutations never enter the source checkout.
    replacements = {
        "src/recursive_integrity_toolkit/metrics/diversity.py":
            (b"diversity = 1.0 - concentration", b"diversity = 0.5 - concentration"),
        "tests/golden/phase3_math_cases.json":
            (b'"v2_support":5', b'"v2_support":3'),
        "pyproject.toml": (b"numpy>=2.0", b"numpy>=3.0"),
        "examples/hero/records_v2.csv": (b"v2_08,v2,", b"v2_99,v2,"),
    }
    if relative in replacements:
        before, after = replacements[relative]
        assert original.count(before) == 1
        changed = original.replace(before, after, 1)
    else:
        changed = original + b"\nunauthorized Phase 4 Step 1 mutation\n"
    try:
        path.write_bytes(changed)
        with pytest.raises(ValueError):
            phase4_gate_tools["verify_phase4_snapshot"](phase4_mutation_tree)
    finally:
        path.write_bytes(original)


@pytest.mark.parametrize("relative", [
    "PHASE_4_COMPLETION.md", "PHASE_4_VALIDATION_REPORT.md",
    "PHASE_4_ARCHITECTURE_COMPLIANCE_REPORT.md", "report.json", "report.md",
    "src/recursive_integrity_toolkit/reports/unauthorized.py",
])
def test_phase4_snapshot_rejects_premature_outputs_and_new_runtime(phase4_gate_tools, phase4_mutation_tree, relative):
    path = phase4_mutation_tree / relative
    assert not path.exists()
    try:
        path.write_text("Unauthorized later-stage artifact\n", encoding="utf-8")
        with pytest.raises(ValueError):
            phase4_gate_tools["verify_phase4_snapshot"](phase4_mutation_tree)
    finally:
        path.unlink()


def test_phase4_snapshot_rejects_missing_protected_runtime(phase4_gate_tools, phase4_mutation_tree):
    path = phase4_mutation_tree / "src/recursive_integrity_toolkit/metrics/bounds.py"
    original = path.read_bytes()
    try:
        path.unlink()
        with pytest.raises(ValueError):
            phase4_gate_tools["verify_phase4_snapshot"](phase4_mutation_tree)
    finally:
        path.write_bytes(original)


def test_phase4_current_snapshot_enforces_migrated_historical_assertions(phase4_gate_tools, phase4_mutation_tree):
    path = phase4_mutation_tree / "tests/integration/test_cli_validation.py"
    original = path.read_bytes()
    assertion = b"assert result.returncode == 0, result.stderr"
    assert assertion in original
    try:
        path.write_bytes(original.replace(assertion, b"assert True", 1))
        with pytest.raises(ValueError):
            phase4_gate_tools["verify_phase4_snapshot"](phase4_mutation_tree)
    finally:
        path.write_bytes(original)


def test_phase4_final_snapshot_preserves_all_current_runtime_bytes(repo_root, phase3_final_snapshot):
    package = "src/recursive_integrity_toolkit"
    current = {path.relative_to(repo_root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
               for path in (repo_root / package).rglob("*.py")}
    frozen = {path.relative_to(phase3_final_snapshot).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
              for path in (phase3_final_snapshot / package).rglob("*.py")}
    assert len(current) == len(frozen) == 40
    assert current == frozen


def test_phase4_active_workflows_preserve_full_matrix_and_use_current_dispatch(repo_root):
    names = {"ci.yml", "golden.yml", "security.yml", "release.yml"}
    root = repo_root / ".github/workflows"
    assert {path.name for path in root.glob("*.yml")} == names
    for name in sorted(names):
        text = (root / name).read_text(encoding="utf-8")
        assert "--phase 4 --step 1" in text, name
        assert "--phase 3 --step 11" not in text, name
        assert "permissions:\n  contents: read" in text
        assert "persist-credentials: false" in text
        assert "timeout-minutes:" in text and "set -euo pipefail" in text
        assert "actions/upload-artifact@v4" in text
        assert "if-no-files-found: error" in text
        for forbidden in ("continue-on-error:", "|| true", "contents: write", "id-token: write", "twine upload", "git push"):
            assert forbidden not in text, (name, forbidden)
    ci = (root / "ci.yml").read_text(encoding="utf-8")
    for required in ('os: [ubuntu-latest, windows-latest]', 'python-version: ["3.11", "3.12"]',
                     'dependencies: [current, minimum]', '"numpy==2.0.0" "pandas==2.2.2"',
                     'RIT_TEST_PARQUET: "0"', 'RIT_TEST_PARQUET: "1"', '--require-parquet',
                     '--baseline-evidence', 'python -m pip check'):
        assert required in ci
    assert ci.count("python -m pytest -p no:cacheprovider -q --junitxml=") == 2
    assert " -k " not in ci
    release = (root / "release.yml").read_text(encoding="utf-8")
    assert "python -m build" in release and "python -m twine check --strict" in release
    assert "--dist" in release and "--candidate" in release


def test_phase4_step1_keeps_current_help_and_future_commands_unopened(subprocess_env, tmp_path):
    before = set(tmp_path.iterdir())
    result = subprocess.run(
        [sys.executable, "-m", "recursive_integrity_toolkit", "--help"],
        cwd=tmp_path, env=subprocess_env, text=True, capture_output=True, check=False,
    )
    assert result.returncode == 0 and "version" in result.stdout
    assert "Analytical audit functionality is not implemented" in " ".join(result.stdout.split())
    rejected = subprocess.run(
        [sys.executable, "-m", "recursive_integrity_toolkit", "audit"],
        cwd=tmp_path, env=subprocess_env, text=True, capture_output=True, check=False,
    )
    assert rejected.returncode == 2
    assert set(tmp_path.iterdir()) == before


def test_phase4_step1_has_no_completion_records_or_reports(repo_root):
    for relative in ("PHASE_4_COMPLETION.md", "PHASE_4_VALIDATION_REPORT.md",
                     "PHASE_4_ARCHITECTURE_COMPLIANCE_REPORT.md", "report.json", "report.md"):
        assert not (repo_root / relative).exists(), relative
