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
def phase4_mutation_tree(repo_root, tmp_path_factory, phase4_gate_tools, phase4_step1_snapshot):
    """One source copy; each individual mutation is restored in a finally block."""
    root = tmp_path_factory.mktemp("phase4-active-mutations")
    tracked = subprocess.check_output(["git", "-C", str(repo_root), "ls-files", "-z"])
    paths = set(tracked.decode().split("\0")) - {""}
    paths.update(phase4_gate_tools["PHASE4_STEP1_NEW"])
    for relative in sorted(paths):
        destination = root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(phase4_step1_snapshot / relative, destination)
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


def test_phase4_final_snapshot_preserves_all_current_runtime_bytes(repo_root, phase3_final_snapshot, phase4_step1_snapshot):
    repo_root = phase4_step1_snapshot
    package = "src/recursive_integrity_toolkit"
    current = {path.relative_to(repo_root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
               for path in (repo_root / package).rglob("*.py")}
    frozen = {path.relative_to(phase3_final_snapshot).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
              for path in (phase3_final_snapshot / package).rglob("*.py")}
    assert len(current) == len(frozen) == 40
    assert current == frozen


def test_phase4_active_workflows_preserve_full_matrix_and_use_current_dispatch(repo_root, phase4_step1_snapshot):
    repo_root = phase4_step1_snapshot
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


def test_phase4_step2_current_runtime_opens_only_the_canonical_result(repo_root, phase3_final_snapshot):
    package = "src/recursive_integrity_toolkit"
    current = {path.relative_to(repo_root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
               for path in (repo_root / package).rglob("*.py")}
    frozen = {path.relative_to(phase3_final_snapshot).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
              for path in (phase3_final_snapshot / package).rglob("*.py")}
    assert len(current) == len(frozen) == 40
    assert current.keys() == frozen.keys()
    opened = "src/recursive_integrity_toolkit/result.py"
    assert current[opened] != frozen[opened]
    assert {path: digest for path, digest in current.items() if path != opened} == {
        path: digest for path, digest in frozen.items() if path != opened
    }


def test_phase4_step2_current_workflows_preserve_matrix_and_use_active_dispatch(repo_root):
    names = {"ci.yml", "golden.yml", "security.yml", "release.yml"}
    root = repo_root / ".github/workflows"
    assert {path.name for path in root.glob("*.yml")} == names
    for name in sorted(names):
        text = (root / name).read_text(encoding="utf-8")
        assert "Phase 4 Step 2" in text, name
        assert "--phase 4 --step 2" in text, name
        assert "--phase 4 --step 1" not in text, name
        assert "--phase 3 --step 11" not in text, name
        assert "permissions:\n  contents: read" in text
        assert "persist-credentials: false" in text
        assert "timeout-minutes:" in text and "set -euo pipefail" in text
        assert "actions/upload-artifact@v4" in text
        assert "if-no-files-found: error" in text
        for line in text.splitlines():
            if "python scripts/release_check.py" in line:
                assert "--phase 4 --step 2" in line, (name, line)
        for forbidden in ("continue-on-error:", "|| true", "contents: write", "id-token: write", "twine upload", "git push"):
            assert forbidden not in text, (name, forbidden)
    ci = (root / "ci.yml").read_text(encoding="utf-8")
    for required in ('os: [ubuntu-latest, windows-latest]', 'python-version: ["3.11", "3.12"]',
                     'dependencies: [current, minimum]', '"numpy==2.0.0" "pandas==2.2.2"',
                     'RIT_TEST_PARQUET: "0"', 'RIT_TEST_PARQUET: "1"', '--require-parquet',
                     '--baseline-evidence', 'python -m pip check',
                     '--minimum-tests 2584', '--minimum-tests 2587',
                     "find_spec('pyarrow') is None", 'import pyarrow'):
        assert required in ci
    assert ci.count("python -m pytest -p no:cacheprovider -q --junitxml=") == 2
    assert " -k " not in ci
    golden = (root / "golden.yml").read_text(encoding="utf-8")
    assert "tests/golden/test_phase3_math.py" in golden
    assert "tests/integration/test_hero_structure.py" in golden
    assert "tests/integration/test_phase3_metric_pipeline.py" in golden
    security = (root / "security.yml").read_text(encoding="utf-8")
    for required in ('tests/integration/test_no_network.py', 'tests/integration/test_optional_dependency.py',
                     'tests/unit/test_PR012_evidence_classes.py', 'tests/unit/test_PR013_report_schema.py',
                     'tests/unit/test_phase4_contracts.py', 'tests/integration/test_phase4_gates.py'):
        assert required in security
    release = (root / "release.yml").read_text(encoding="utf-8")
    assert "python -m build" in release and "python -m twine check --strict" in release
    assert "--dist" in release and "--candidate" in release
    assert "--delivery" not in release
    assert "recursive-integrity-toolkit-phase4-step2-candidate" in release
    assert "rit-phase4-step1" not in release
    assert release.count("python -m pytest -p no:cacheprovider -q --junitxml=") == 2


@pytest.mark.parametrize("mutation", [
    "unchanged", "formula", "math_oracle", "frozen_model", "frozen_schema",
    "hero", "dependency", "plan", "assembly", "cli", "unknown_runtime",
    "missing_runtime", "premature_completion", "premature_report",
    "control_step", "control_scope", "control_schema_scope",
    "schema_open_root", "schema_wrong_dialect", "model_computation_import",
    "historical_assertion", "historical_tooling",
])
def test_phase4_step2_current_snapshot_checks_valid_tree_before_mutations(repo_root, tmp_path, phase4_gate_tools, mutation):
    import json

    tracked = subprocess.check_output(["git", "-C", str(repo_root), "ls-files", "-z"])
    paths = set(tracked.decode().split("\0")) - {""}
    assert len(paths) == 227
    for relative in sorted(paths):
        destination = tmp_path / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(repo_root / relative, destination)
    verify = phase4_gate_tools["verify_phase4_step2_snapshot"]
    baseline = verify(tmp_path)
    assert baseline["frozen_runtime_modules"] == 39
    assert baseline["frozen_schemas"] == 4
    assert baseline["result_contracts_enabled"] is True
    assert baseline["adapters_enabled"] is False
    assert baseline["cli_analysis_enabled"] is False
    assert baseline["phase_complete"] is False
    if mutation == "unchanged":
        return
    replacements = {
        "formula": ("src/recursive_integrity_toolkit/metrics/diversity.py",
                    b"diversity = 1.0 - concentration", b"diversity = 0.5 - concentration"),
        "math_oracle": ("tests/golden/phase3_math_cases.json", b'"v2_support":5', b'"v2_support":3'),
        "hero": ("examples/hero/records_v2.csv", b"v2_08,v2,", b"v2_99,v2,"),
        "dependency": ("pyproject.toml", b"numpy>=2.0", b"numpy>=3.0"),
        "historical_assertion": ("tests/unit/test_phase4_contracts.py",
                                 b'    assert phase4_control["active_step"] == 1\n', b"    assert True\n"),
        "historical_tooling": ("scripts/release_check.py",
                               b"def verify_phase4_control(control: dict, step: int = 1) -> None:",
                               b"def verify_phase4_control(control: dict, step: int = 1) -> None:\n    return"),
    }
    appended = {
        "frozen_model": "src/recursive_integrity_toolkit/models.py",
        "frozen_schema": "schemas/config.schema.json",
        "plan": "PHASE_4_PLAN.md",
        "assembly": "src/recursive_integrity_toolkit/reports/assembly.py",
        "cli": "src/recursive_integrity_toolkit/cli.py",
    }
    added = {
        "unknown_runtime": "src/recursive_integrity_toolkit/reports/unauthorized.py",
        "premature_completion": "PHASE_4_COMPLETION.md",
        "premature_report": "report.json",
    }
    if mutation in replacements:
        relative, original, replacement = replacements[mutation]
        path = tmp_path / relative
        source = path.read_bytes()
        assert source.count(original) == 1
        path.write_bytes(source.replace(original, replacement, 1))
    elif mutation in appended:
        path = tmp_path / appended[mutation]
        path.write_bytes(path.read_bytes() + b"\nUnauthorized Step 2 mutation\n")
    elif mutation in added:
        path = tmp_path / added[mutation]
        assert not path.exists()
        path.write_text("Unauthorized later-stage file\n", encoding="utf-8")
    elif mutation == "missing_runtime":
        (tmp_path / "src/recursive_integrity_toolkit/metrics/bounds.py").unlink()
    elif mutation.startswith("control_"):
        path = tmp_path / "PHASE_4_BASELINE.json"
        control = json.loads(path.read_text(encoding="utf-8"))
        if mutation == "control_step":
            control["active_step"] = 3
        elif mutation == "control_scope":
            control["runtime_paths_authorized"].append("src/recursive_integrity_toolkit/cli.py")
        else:
            control["schema_paths_authorized"].append("schemas/config.schema.json")
        path.write_text(json.dumps(control), encoding="utf-8")
    elif mutation.startswith("schema_"):
        path = tmp_path / "schemas/report.schema.json"
        schema = json.loads(path.read_text(encoding="utf-8"))
        if mutation == "schema_open_root":
            schema["additionalProperties"] = True
        else:
            schema["$schema"] = "http://json-schema.org/draft-07/schema#"
        path.write_text(json.dumps(schema), encoding="utf-8")
    elif mutation == "model_computation_import":
        path = tmp_path / "src/recursive_integrity_toolkit/result.py"
        path.write_bytes(path.read_bytes() + b"\nfrom .metrics.diversity import effective_state_diversity\n")
    else:
        raise AssertionError(f"Unknown active mutation case: {mutation}")
    with pytest.raises(ValueError):
        verify(tmp_path)


def test_phase4_step2_junit_dispatch_accepts_valid_subsets_and_rejects_bad_evidence(repo_root, tmp_path):
    import json

    junit = tmp_path / "subset.xml"
    command = [sys.executable, str(repo_root / "scripts/release_check.py"),
               "--phase", "4", "--step", "2", "--junit", str(junit)]
    valid = ('<testsuites><testsuite tests="1" failures="0" errors="0" skipped="0">'
             '<testcase classname="independent.subset" name="test_one" />'
             '</testsuite></testsuites>')
    junit.write_text(valid, encoding="utf-8")
    passed = subprocess.run(command, cwd=tmp_path, text=True, capture_output=True, check=False)
    assert passed.returncode == 0, passed.stderr
    assert json.loads(passed.stdout)["tests"] == 1
    assert json.loads(passed.stdout)["passed"] == 1
    too_small = subprocess.run(command + ["--minimum-tests", "2584"], cwd=tmp_path,
                               text=True, capture_output=True, check=False)
    assert too_small.returncode != 0
    assert "Insufficient or duplicate test cases" in too_small.stderr
    for outcome in ("failure", "skipped"):
        invalid = ('<testsuites><testsuite tests="1">'
                   '<testcase classname="independent.subset" name="test_one">'
                   f'<{outcome} message="independent rejection case" />'
                   '</testcase></testsuite></testsuites>')
        junit.write_text(invalid, encoding="utf-8")
        rejected = subprocess.run(command, cwd=tmp_path, text=True, capture_output=True, check=False)
        assert rejected.returncode != 0
        assert "Failed, errored or skipped test" in rejected.stderr
