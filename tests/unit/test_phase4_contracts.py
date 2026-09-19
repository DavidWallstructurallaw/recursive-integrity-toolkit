"""Approved Phase 4 Step 1 controls cannot authorize their own expansion.

These gates protect the current tree. Reporting contracts and calculations remain
at the accepted Phase 3 bytes until their separately authorized steps.
"""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import runpy

import pytest


ROOT = Path(__file__).resolve().parents[2]
BASELINE = "e3ffb8c0a88bfe31f669f9662d9b5213da628b3a"
BASELINE_TREE = "e2a25f8cfdc66c3317809c479f80fdae162e6ba9"
BASELINE_TEST_TREE = "6ab22cb9197a8f094f455b29a07a851062bb26c9"
PLAN_SHA256 = "5a6d65696720a426630e876d001937b2837d24774fcb6c2bd43b8e09f5ae93f0"
NEW_FILES = {
    "PHASE_4_PLAN.md", "PHASE_4_BASELINE.json", "PHASE_4_DECISIONS.md",
    "tests/unit/test_phase4_contracts.py", "tests/integration/test_phase4_gates.py",
}


@pytest.fixture(scope="module")
def phase4_tools():
    return runpy.run_path(str(ROOT / "scripts/release_check.py"), run_name="phase4_contract_tests")


@pytest.fixture
def phase4_control():
    return json.loads((ROOT / "PHASE_4_BASELINE.json").read_text(encoding="utf-8"))


def test_phase4_accepted_anchors_and_plan_bytes_are_independent(phase4_tools, phase4_control):
    assert phase4_tools["PHASE4_FINAL"] == BASELINE
    assert phase4_tools["PHASE4_TREE"] == BASELINE_TREE
    assert phase4_tools["PHASE4_TEST_TREE"] == BASELINE_TEST_TREE
    assert phase4_tools["PHASE4_PLAN_SHA256"] == PLAN_SHA256
    assert hashlib.sha256((ROOT / "PHASE_4_PLAN.md").read_bytes()).hexdigest() == PLAN_SHA256
    assert phase4_control["baseline_commit"] == BASELINE
    assert phase4_control["baseline_core_tests"] == 2489
    assert phase4_control["baseline_parquet_tests"] == 2492
    assert phase4_control["active_phase"] == 4
    assert phase4_control["active_step"] == 1
    assert phase4_control["approved_decisions"] == [f"P4-D{i:02d}" for i in range(1, 12)]
    phase4_tools["verify_phase4_control"](phase4_control, step=1)


@pytest.mark.parametrize("field,value", [
    ("active_phase", 3), ("active_phase", True),
    ("active_step", 2), ("active_step", True),
    ("baseline_commit", "0" * 40), ("baseline_tree", "0" * 40),
    ("baseline_test_tree", "0" * 40), ("approved_plan_sha256", "0" * 64),
    ("baseline_core_tests", 1), ("baseline_parquet_tests", 1),
    ("approved_decisions", []), ("approved_decisions", ["P4-D01"]),
    ("phase_complete", True), ("next_step_authorized", True),
    ("main_merge_authorized", True), ("publication_authorized", True),
    ("permitted_paths", ["src/recursive_integrity_toolkit/result.py"]),
    ("new_files_permitted", ["PHASE_4_COMPLETION.md"]),
])
def test_phase4_control_rejects_forged_authority(phase4_tools, phase4_control, field, value):
    phase4_control[field] = value
    with pytest.raises(ValueError):
        phase4_tools["verify_phase4_control"](phase4_control, step=1)


@pytest.mark.parametrize("step", [0, 2, 11, True, "1", None])
def test_phase4_control_rejects_unapproved_dispatch_steps(phase4_tools, phase4_control, step):
    with pytest.raises(ValueError):
        phase4_tools["verify_phase4_control"](phase4_control, step=step)


@pytest.mark.parametrize("field", ["active_step", "baseline_commit", "approved_decisions", "permitted_paths"])
def test_phase4_control_requires_its_approval_fields(phase4_tools, phase4_control, field):
    del phase4_control[field]
    with pytest.raises(ValueError):
        phase4_tools["verify_phase4_control"](phase4_control, step=1)


def test_phase4_manifest_cannot_mint_an_extra_permission(phase4_tools, phase4_control):
    forged = deepcopy(phase4_control)
    forged["approved_scope_expansion"] = {"step": 2, "result_implementation": True}
    with pytest.raises(ValueError):
        phase4_tools["verify_phase4_control"](forged, step=1)


def test_phase4_fixed_path_boundary_opens_only_governance(phase4_tools):
    assert phase4_tools["PHASE4_STEP1_NEW"] == NEW_FILES
    allowed = phase4_tools["PHASE4_STEP1_ALLOWED"]
    assert not any(path.startswith(("src/", "schemas/", "examples/", "tests/golden/")) for path in allowed)
    phase4_tools["verify_phase4_changes"]([
        ("A", "PHASE_4_PLAN.md"), ("A", "PHASE_4_BASELINE.json"),
        ("M", "scripts/release_check.py"), ("M", "tests/conftest.py"),
    ])


@pytest.mark.parametrize("status,path", [
    ("M", "src/recursive_integrity_toolkit/metrics/diversity.py"),
    ("M", "src/recursive_integrity_toolkit/result.py"),
    ("M", "schemas/report.schema.json"),
    ("M", "tests/golden/phase3_math_cases.json"),
    ("M", "PROJECT_INSTRUCTIONS.md"),
    ("M", "PHASE_3_BASELINE.json"),
    ("M", "PHASE_4_PLAN.md"),
    ("A", "scripts/release_check.py"),
    ("A", "PHASE_4_COMPLETION.md"),
    ("A", "tests/unit/test_unapproved.py"),
    ("A", "src/recursive_integrity_toolkit/reports/new.py"),
    ("D", "scripts/release_check.py"),
    ("R100", "scripts/release_check.py"),
    ("T", "scripts/release_check.py"),
    ("M", "./scripts/release_check.py"),
    ("M", "scripts/../scripts/release_check.py"),
])
def test_phase4_changes_reject_protected_or_unlisted_operations(phase4_tools, status, path):
    with pytest.raises(ValueError):
        phase4_tools["verify_phase4_changes"]([(status, path)])


def test_phase4_changes_reject_duplicate_path_operations(phase4_tools):
    with pytest.raises(ValueError):
        phase4_tools["verify_phase4_changes"]([
            ("M", "scripts/release_check.py"), ("M", "scripts/release_check.py"),
        ])


def test_phase4_historical_phase3_control_still_uses_its_original_contract(phase4_tools):
    original = json.loads((ROOT / "PHASE_3_BASELINE.json").read_text(encoding="utf-8"))
    assert phase4_tools["ACTIVE_PHASE"] == 3 and phase4_tools["ACTIVE_STEP"] == 11
    phase4_tools["verify_phase3_control"](original, step=11)
    original["active_phase"] = 4
    with pytest.raises(ValueError):
        phase4_tools["verify_phase3_control"](original, step=11)


def test_phase4_registered_migrations_accept_only_the_approved_inventory(phase4_tools, phase3_final_snapshot):
    approved_files = {
        "tests/unit/test_PR012_evidence_classes.py", "tests/unit/test_PR013_report_schema.py",
        "tests/unit/test_PR014_unavailable.py", "tests/unit/test_PR015_redaction.py",
        "tests/unit/test_PR016_determinism.py", "tests/unit/test_PR018_language.py",
        "tests/integration/test_no_algorithms.py", "tests/integration/test_phase3_metric_pipeline.py",
        "tests/integration/test_cli_validation.py", "tests/integration/test_ci_workflows.py",
    }
    registry = phase4_tools["PHASE4_MIGRATIONS"]
    assert set(registry) == approved_files
    assert sum(len(rows) for rows in registry.values()) == 16
    for path in sorted(approved_files):
        phase4_tools["verify_phase4_test_migration"](
            path, (phase3_final_snapshot / path).read_bytes(), (ROOT / path).read_bytes(),
        )


@pytest.mark.parametrize("mutation", ["assertion", "wrong_baseline", "duplicate_node", "unlisted_path"])
def test_phase4_migration_guard_rejects_weakening_or_wrong_identity(phase4_tools, phase3_final_snapshot, mutation):
    path = "tests/integration/test_cli_validation.py"
    before = (phase3_final_snapshot / path).read_bytes()
    after = (ROOT / path).read_bytes()
    verify = phase4_tools["verify_phase4_test_migration"]
    verify(path, before, after)
    if mutation == "assertion":
        assertion = b"assert result.returncode == 0, result.stderr"
        assert assertion in after
        after = after.replace(assertion, b"assert True", 1)
    elif mutation == "wrong_baseline":
        before += b"\n# Claimed replacement baseline.\n"
    elif mutation == "duplicate_node":
        after += b"\ndef test_cli_help_runs():\n    assert True\n"
    else:
        path = "tests/integration/test_package_install.py"
    with pytest.raises(ValueError):
        verify(path, before, after)


@pytest.mark.parametrize("statement", [
    b"PHASE3_ACTIVE_STEP += 1",
    b"ALLOWED_FUNCTIONS.clear()",
    b"PHASE4_MUTATION = ALLOWED_FUNCTIONS.clear()",
    b"def phase4_mutator(value=ALLOWED_FUNCTIONS.clear()):\n    pass",
    b"def phase4_mutator(*, value=ALLOWED_FUNCTIONS.clear()):\n    pass",
    b"@ALLOWED_FUNCTIONS.clear()\ndef phase4_mutator():\n    pass",
    b"def phase4_mutator() -> ALLOWED_FUNCTIONS.clear():\n    pass",
    b"def phase4_mutator(value: ALLOWED_FUNCTIONS.clear()):\n    pass",
])
def test_phase4_tooling_guard_rejects_appended_mutation_of_historical_state(phase4_tools, statement):
    path = "scripts/check_traceability.py"
    current = (ROOT / path).read_bytes()
    verify = phase4_tools["_phase4_preserve_tooling"]
    verify(current, current, path)
    with pytest.raises(ValueError):
        verify(current, current + b"\n" + statement + b"\n", path)


def test_phase4_append_guard_rejects_import_rebinding_an_inherited_test(phase4_tools):
    path = "tests/integration/test_cli_validation.py"
    current = (ROOT / path).read_bytes()
    verify = phase4_tools["_phase4_append_only"]
    verify(current, current, path)
    with pytest.raises(ValueError):
        verify(current, current + b"\nfrom pathlib import Path as test_cli_help_runs\n", path)


@pytest.mark.parametrize("statement", [
    b"def test_phase4_mutator(value=globals().clear()):\n    pass",
    b"def test_phase4_mutator(*, value=globals().clear()):\n    pass",
    b"@globals().clear()\ndef test_phase4_mutator():\n    pass",
])
def test_phase4_append_guard_rejects_definition_time_mutations(phase4_tools, statement):
    path = "tests/integration/test_cli_validation.py"
    current = (ROOT / path).read_bytes()
    verify = phase4_tools["_phase4_append_only"]
    verify(current, current, path)
    with pytest.raises(ValueError):
        verify(current, current + b"\n" + statement + b"\n", path)
