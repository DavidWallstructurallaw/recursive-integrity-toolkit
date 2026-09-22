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
def phase4_control(phase4_step1_snapshot):
    return json.loads((phase4_step1_snapshot / "PHASE_4_BASELINE.json").read_text(encoding="utf-8"))


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


def test_phase4_registered_migrations_accept_only_the_approved_inventory(phase4_tools, phase3_final_snapshot, phase4_step1_snapshot):
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
            path, (phase3_final_snapshot / path).read_bytes(), (phase4_step1_snapshot / path).read_bytes(),
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


def test_phase4_step2_approved_control_keeps_independent_step1_anchors(phase4_tools, phase4_step2_snapshot):
    control = json.loads((phase4_step2_snapshot / "PHASE_4_BASELINE.json").read_text(encoding="utf-8"))
    assert phase4_tools["PHASE4_STEP1_FINAL"] == "a7f3c46d6ca05de36bfcb60f496ebb2d5ab4a37c"
    assert phase4_tools["PHASE4_STEP1_TREE"] == "7f8ef492568456bf5d46fb1b7e2631cb9b94e3fd"
    assert phase4_tools["PHASE4_STEP1_TEST_TREE"] == "2ce77e331a0fc377387735bb55dffd3be630b59c"
    assert control["active_phase"] == 4 and control["active_step"] == 2
    assert control["approval_basis"] == "批准，开始 **Phase 4 Step 2**"
    assert control["baseline_commit"] == BASELINE
    assert control["previous_step_commit"] == "a7f3c46d6ca05de36bfcb60f496ebb2d5ab4a37c"
    assert control["previous_step_tree"] == "7f8ef492568456bf5d46fb1b7e2631cb9b94e3fd"
    assert control["previous_step_test_tree"] == "2ce77e331a0fc377387735bb55dffd3be630b59c"
    assert control["previous_step_core_tests"] == 2584
    assert control["previous_step_parquet_tests"] == 2587
    assert len(control["previous_step_files_sha256"]) == 227
    assert control["runtime_paths_authorized"] == ["src/recursive_integrity_toolkit/result.py"]
    assert control["schema_paths_authorized"] == ["schemas/report.schema.json"]
    assert control["new_files_permitted"] == []
    for name in ("phase_complete", "next_step_authorized", "main_merge_authorized", "publication_authorized"):
        assert control[name] is False
    phase4_tools["verify_phase4_step2_control"](control, step=2)
    with pytest.raises(ValueError):
        phase4_tools["verify_phase4_control"](control, step=1)


@pytest.mark.parametrize("field,value", [
    ("active_phase", 3), ("active_phase", True),
    ("active_step", 1), ("active_step", 3), ("active_step", True),
    ("approval_basis", "approved by this manifest"),
    ("previous_step_commit", "0000000000000000000000000000000000000000"), ("previous_step_tree", "0000000000000000000000000000000000000000"),
    ("previous_step_test_tree", "0000000000000000000000000000000000000000"), ("previous_step_files_sha256", {}),
    ("baseline_commit", "0000000000000000000000000000000000000000"), ("baseline_files_sha256", {}),
    ("previous_step_core_tests", 1), ("previous_step_parquet_tests", 1),
    ("runtime_paths_authorized", ["src/recursive_integrity_toolkit/metrics/diversity.py"]),
    ("schema_paths_authorized", ["schemas/config.schema.json"]),
    ("new_files_permitted", ["src/recursive_integrity_toolkit/reports/new.py"]),
    ("permitted_paths", ["src/recursive_integrity_toolkit/cli.py"]),
    ("phase_complete", True), ("next_step_authorized", True),
    ("main_merge_authorized", True), ("publication_authorized", True),
])
def test_phase4_step2_control_rejects_forged_scope_and_stage(phase4_tools, field, value, phase4_step2_snapshot):
    control = json.loads((phase4_step2_snapshot / "PHASE_4_BASELINE.json").read_text(encoding="utf-8"))
    verify = phase4_tools["verify_phase4_step2_control"]
    verify(control, step=2)
    control[field] = value
    with pytest.raises(ValueError):
        verify(control, step=2)


@pytest.mark.parametrize("step", [0, 1, 3, 11, True, "2", None])
def test_phase4_step2_control_rejects_unapproved_dispatch(phase4_tools, step, phase4_step2_snapshot):
    control = json.loads((phase4_step2_snapshot / "PHASE_4_BASELINE.json").read_text(encoding="utf-8"))
    with pytest.raises(ValueError):
        phase4_tools["verify_phase4_step2_control"](control, step=step)


@pytest.mark.parametrize("field", ["active_step", "previous_step_commit", "runtime_paths_authorized", "schema_paths_authorized"])
def test_phase4_step2_control_requires_explicit_approval_fields(phase4_tools, field, phase4_step2_snapshot):
    control = json.loads((phase4_step2_snapshot / "PHASE_4_BASELINE.json").read_text(encoding="utf-8"))
    phase4_tools["verify_phase4_step2_control"](control)
    del control[field]
    with pytest.raises(ValueError):
        phase4_tools["verify_phase4_step2_control"](control)


def test_phase4_step2_control_cannot_mint_extra_permission(phase4_tools, phase4_step2_snapshot):
    control = json.loads((phase4_step2_snapshot / "PHASE_4_BASELINE.json").read_text(encoding="utf-8"))
    phase4_tools["verify_phase4_step2_control"](control)
    control["approved_scope_expansion"] = {"step": 3, "assembly": True}
    with pytest.raises(ValueError):
        phase4_tools["verify_phase4_step2_control"](control)


def test_phase4_step2_fixed_boundary_opens_only_approved_existing_paths(phase4_tools):
    approved = {
        "PHASE_4_BASELINE.json", "PHASE_4_DECISIONS.md", "scripts/check_traceability.py",
        "scripts/check_spec_consistency.py", "scripts/release_check.py", "tests/conftest.py",
        "tests/unit/test_phase4_contracts.py", "tests/integration/test_phase4_gates.py",
        "tests/integration/test_no_algorithms.py", "tests/integration/test_ci_workflows.py",
        "tests/integration/test_repository_structure.py", "tests/integration/test_owner_ids.py",
        "tests/integration/test_package_import.py", "tests/integration/test_package_install.py",
        "tests/integration/test_optional_dependency.py", "tests/integration/test_no_network.py",
        "tests/integration/test_schema_json.py", "tests/integration/test_hero_structure.py",
        "tests/integration/test_prohibited_structure.py", "tests/integration/test_license_notices.py",
        ".github/workflows/ci.yml", ".github/workflows/security.yml",
        ".github/workflows/golden.yml", ".github/workflows/release.yml",
        "docs/architecture.md", "docs/theory_traceability.md",
        "src/recursive_integrity_toolkit/result.py", "schemas/report.schema.json",
        "docs/report_schema.md", "tests/unit/test_PR012_evidence_classes.py",
        "tests/unit/test_PR013_report_schema.py",
    }
    assert set(phase4_tools["PHASE4_STEP2_ALLOWED"]) == approved
    assert set(phase4_tools["PHASE4_STEP2_NEW"]) == set()
    phase4_tools["verify_phase4_step2_changes"]([("M", path) for path in sorted(approved)])


@pytest.mark.parametrize("status,path", [
    ("M", "src/recursive_integrity_toolkit/metrics/diversity.py"),
    ("M", "src/recursive_integrity_toolkit/models.py"),
    ("M", "src/recursive_integrity_toolkit/reports/assembly.py"),
    ("M", "src/recursive_integrity_toolkit/cli.py"),
    ("M", "schemas/config.schema.json"),
    ("M", "tests/golden/phase3_math_cases.json"),
    ("M", "PHASE_4_PLAN.md"), ("M", "pyproject.toml"),
    ("A", "src/recursive_integrity_toolkit/result.py"),
    ("A", "tests/unit/test_phase4_step2_new.py"),
    ("A", "PHASE_4_COMPLETION.md"),
    ("D", "schemas/report.schema.json"), ("R100", "docs/report_schema.md"),
    ("T", "scripts/release_check.py"), ("M", "./scripts/release_check.py"),
    ("M", "scripts/../scripts/release_check.py"),
])
def test_phase4_step2_diff_rejects_unopened_paths_and_nonmodification_operations(phase4_tools, status, path):
    with pytest.raises(ValueError):
        phase4_tools["verify_phase4_step2_changes"]([(status, path)])


def test_phase4_step2_diff_rejects_duplicate_operations(phase4_tools):
    with pytest.raises(ValueError):
        phase4_tools["verify_phase4_step2_changes"]([
            ("M", "schemas/report.schema.json"), ("M", "schemas/report.schema.json"),
        ])


def test_phase4_step2_historical_migrations_are_five_explicit_step1_bindings(phase4_tools, phase4_step1_snapshot, phase4_step2_snapshot):
    registry = phase4_tools["PHASE4_STEP2_MIGRATIONS"]
    assert {path: {row["node"] for row in rows} for path, rows in registry.items()} == {
        "tests/unit/test_phase4_contracts.py": {
            "phase4_control", "test_phase4_registered_migrations_accept_only_the_approved_inventory",
        },
        "tests/integration/test_phase4_gates.py": {
            "phase4_mutation_tree", "test_phase4_final_snapshot_preserves_all_current_runtime_bytes",
            "test_phase4_active_workflows_preserve_full_matrix_and_use_current_dispatch",
        },
    }
    for path in sorted(registry):
        phase4_tools["verify_phase4_step2_test_migration"](
            path, (phase4_step1_snapshot / path).read_bytes(), (phase4_step2_snapshot / path).read_bytes(),
        )


@pytest.mark.parametrize("mutation", ["old_assertion", "wrong_snapshot", "rebind_node", "definition_effect"])
def test_phase4_step2_historical_guard_rejects_assertion_and_binding_weakening(phase4_tools, phase4_step1_snapshot, mutation, phase4_step2_snapshot):
    path = "tests/unit/test_phase4_contracts.py"
    before = (phase4_step1_snapshot / path).read_bytes()
    after = (phase4_step2_snapshot / path).read_bytes()
    verify = phase4_tools["verify_phase4_step2_test_migration"]
    verify(path, before, after)
    if mutation == "old_assertion":
        original = b'    assert phase4_control["active_step"] == 1\n'
        assert after.count(original) == 1
        after = after.replace(original, b"    assert True\n", 1)
    elif mutation == "wrong_snapshot":
        original = b'    return json.loads((phase4_step1_snapshot / "PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\n'
        assert after.count(original) == 1
        after = after.replace(original, b'    return json.loads((ROOT / "PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\n', 1)
    elif mutation == "rebind_node":
        after += b"\ndef test_phase4_fixed_path_boundary_opens_only_governance():\n    assert True\n"
    else:
        after += b"\ndef test_phase4_step2_mutator(value=globals().clear()):\n    pass\n"
    with pytest.raises(ValueError):
        verify(path, before, after)


def test_phase4_step3_approved_control_keeps_independent_step2_anchors(phase4_tools, phase4_step3_snapshot):
    control = json.loads((phase4_step3_snapshot / "PHASE_4_BASELINE.json").read_text(encoding="utf-8"))
    assert phase4_tools["PHASE4_STEP2_FINAL"] == "fcea74e2b1858e83cdbfd1b8212d15343d63ff08"
    assert phase4_tools["PHASE4_STEP2_TREE"] == "c3ce887fd393cfc6c18364546005f2b74a63b746"
    assert phase4_tools["PHASE4_STEP2_TEST_TREE"] == "9d6ac0cbf3827ab54c7852503d99d442a3796259"
    assert control["active_phase"] == 4 and control["active_step"] == 3
    assert control["approval_basis"] == "开始 **Phase 4 Step 3**"
    assert control["baseline_commit"] == BASELINE
    assert control["previous_step_commit"] == "fcea74e2b1858e83cdbfd1b8212d15343d63ff08"
    assert control["previous_step_tree"] == "c3ce887fd393cfc6c18364546005f2b74a63b746"
    assert control["previous_step_test_tree"] == "9d6ac0cbf3827ab54c7852503d99d442a3796259"
    assert control["previous_step_core_tests"] == 2728
    assert control["previous_step_parquet_tests"] == 2731
    assert len(control["previous_step_files_sha256"]) == 227
    assert control["runtime_paths_authorized"] == ["src/recursive_integrity_toolkit/reports/assembly.py"]
    assert control["schema_changes_authorized"] is False
    assert control["schema_paths_authorized"] == []
    assert control["new_files_permitted"] == []
    for name in ("phase_complete", "next_step_authorized", "main_merge_authorized", "publication_authorized"):
        assert control[name] is False
    phase4_tools["verify_phase4_step3_control"](control, step=3)
    with pytest.raises(ValueError):
        phase4_tools["verify_phase4_step2_control"](control, step=2)


@pytest.mark.parametrize("field,value", [
    ("active_phase", 3), ("active_phase", True),
    ("active_step", 2), ("active_step", 4), ("active_step", True),
    ("approval_basis", "approved by this manifest"),
    ("previous_step_commit", "0000000000000000000000000000000000000000"),
    ("previous_step_tree", "0000000000000000000000000000000000000000"),
    ("previous_step_test_tree", "0000000000000000000000000000000000000000"),
    ("previous_step_files_sha256", {}), ("baseline_files_sha256", {}),
    ("previous_step_core_tests", 1), ("previous_step_parquet_tests", 1),
    ("runtime_paths_authorized", ["src/recursive_integrity_toolkit/result.py"]),
    ("schema_changes_authorized", True), ("schema_paths_authorized", ["schemas/report.schema.json"]),
    ("new_files_permitted", ["src/recursive_integrity_toolkit/reports/new.py"]),
    ("permitted_paths", ["src/recursive_integrity_toolkit/cli.py"]),
    ("phase_complete", True), ("next_step_authorized", True),
    ("main_merge_authorized", True), ("publication_authorized", True),
])
def test_phase4_step3_control_rejects_forged_scope_and_stage(phase4_tools, field, value, phase4_step3_snapshot):
    control = json.loads((phase4_step3_snapshot / "PHASE_4_BASELINE.json").read_text(encoding="utf-8"))
    verify = phase4_tools["verify_phase4_step3_control"]
    verify(control, step=3)
    control[field] = value
    with pytest.raises(ValueError):
        verify(control, step=3)


@pytest.mark.parametrize("step", [0, 1, 2, 4, 11, True, "3", None])
def test_phase4_step3_control_rejects_unapproved_dispatch(phase4_tools, step, phase4_step3_snapshot):
    control = json.loads((phase4_step3_snapshot / "PHASE_4_BASELINE.json").read_text(encoding="utf-8"))
    with pytest.raises(ValueError):
        phase4_tools["verify_phase4_step3_control"](control, step=step)


@pytest.mark.parametrize("field", ["active_step", "previous_step_commit", "runtime_paths_authorized", "schema_paths_authorized"])
def test_phase4_step3_control_requires_explicit_approval_fields(phase4_tools, field, phase4_step3_snapshot):
    control = json.loads((phase4_step3_snapshot / "PHASE_4_BASELINE.json").read_text(encoding="utf-8"))
    phase4_tools["verify_phase4_step3_control"](control)
    del control[field]
    with pytest.raises(ValueError):
        phase4_tools["verify_phase4_step3_control"](control)


def test_phase4_step3_control_cannot_mint_extra_permission(phase4_tools, phase4_step3_snapshot):
    control = json.loads((phase4_step3_snapshot / "PHASE_4_BASELINE.json").read_text(encoding="utf-8"))
    phase4_tools["verify_phase4_step3_control"](control)
    control["approved_scope_expansion"] = {"step": 4, "privacy": True}
    with pytest.raises(ValueError):
        phase4_tools["verify_phase4_step3_control"](control)


def test_phase4_step3_fixed_boundary_opens_only_approved_existing_paths(phase4_tools):
    approved = {
        "PHASE_4_BASELINE.json", "PHASE_4_DECISIONS.md", "scripts/check_traceability.py",
        "scripts/check_spec_consistency.py", "scripts/release_check.py", "tests/conftest.py",
        "tests/unit/test_phase4_contracts.py", "tests/integration/test_phase4_gates.py",
        "tests/integration/test_no_algorithms.py", "tests/integration/test_ci_workflows.py",
        "tests/integration/test_repository_structure.py", "tests/integration/test_owner_ids.py",
        "tests/integration/test_package_import.py", "tests/integration/test_package_install.py",
        "tests/integration/test_optional_dependency.py", "tests/integration/test_no_network.py",
        "tests/integration/test_schema_json.py", "tests/integration/test_hero_structure.py",
        "tests/integration/test_prohibited_structure.py", "tests/integration/test_license_notices.py",
        ".github/workflows/ci.yml", ".github/workflows/security.yml",
        ".github/workflows/golden.yml", ".github/workflows/release.yml",
        "docs/architecture.md", "docs/theory_traceability.md",
        "src/recursive_integrity_toolkit/reports/assembly.py", "docs/report_schema.md",
        "tests/unit/test_PR012_evidence_classes.py", "tests/unit/test_PR014_unavailable.py",
        "tests/unit/test_PR018_language.py", "tests/integration/test_partial_provenance_report.py",
        "tests/integration/test_partial_lineage_report.py",
    }
    assert set(phase4_tools["PHASE4_STEP3_ALLOWED"]) == approved
    assert set(phase4_tools["PHASE4_STEP3_NEW"]) == set()
    phase4_tools["verify_phase4_step3_changes"]([("M", path) for path in sorted(approved)])


@pytest.mark.parametrize("status,path", [
    ("M", "src/recursive_integrity_toolkit/metrics/diversity.py"),
    ("M", "src/recursive_integrity_toolkit/models.py"),
    ("M", "src/recursive_integrity_toolkit/result.py"),
    ("M", "src/recursive_integrity_toolkit/cli.py"),
    ("M", "schemas/report.schema.json"), ("M", "schemas/config.schema.json"),
    ("M", "tests/golden/phase3_math_cases.json"),
    ("M", "tests/unit/test_PR013_report_schema.py"),
    ("M", "PHASE_4_PLAN.md"), ("M", "pyproject.toml"),
    ("A", "src/recursive_integrity_toolkit/reports/assembly.py"),
    ("A", "tests/unit/test_phase4_step3_new.py"), ("A", "PHASE_4_COMPLETION.md"),
    ("D", "docs/report_schema.md"), ("R100", "docs/report_schema.md"),
    ("T", "scripts/release_check.py"), ("M", "./scripts/release_check.py"),
    ("M", "scripts/../scripts/release_check.py"),
])
def test_phase4_step3_diff_rejects_unopened_paths_and_nonmodification_operations(phase4_tools, status, path):
    with pytest.raises(ValueError):
        phase4_tools["verify_phase4_step3_changes"]([(status, path)])


def test_phase4_step3_diff_rejects_duplicate_operations(phase4_tools):
    with pytest.raises(ValueError):
        phase4_tools["verify_phase4_step3_changes"]([
            ("M", "docs/report_schema.md"), ("M", "docs/report_schema.md"),
        ])


def test_phase4_step3_historical_migrations_preserve_ten_step2_gate_nodes(phase4_tools, phase4_step2_snapshot, phase4_step3_snapshot):
    registry = phase4_tools["PHASE4_STEP3_MIGRATIONS"]
    expected = {
        "tests/unit/test_phase4_contracts.py": {
            "test_phase4_step2_approved_control_keeps_independent_step1_anchors",
            "test_phase4_step2_control_rejects_forged_scope_and_stage",
            "test_phase4_step2_control_rejects_unapproved_dispatch",
            "test_phase4_step2_control_requires_explicit_approval_fields",
            "test_phase4_step2_control_cannot_mint_extra_permission",
            "test_phase4_step2_historical_migrations_are_five_explicit_step1_bindings",
            "test_phase4_step2_historical_guard_rejects_assertion_and_binding_weakening",
        },
        "tests/integration/test_phase4_gates.py": {
            "test_phase4_step2_current_runtime_opens_only_the_canonical_result",
            "test_phase4_step2_current_workflows_preserve_matrix_and_use_active_dispatch",
            "test_phase4_step2_current_snapshot_checks_valid_tree_before_mutations",
        },
    }
    for path, nodes in expected.items():
        assert {row["node"] for row in registry[path]} == nodes
        phase4_tools["verify_phase4_step3_test_migration"](
            path, (phase4_step2_snapshot / path).read_bytes(), (phase4_step3_snapshot / path).read_bytes(),
        )


@pytest.mark.parametrize("mutation", ["old_assertion", "wrong_snapshot", "rebind_node", "definition_effect"])
def test_phase4_step3_historical_guard_rejects_assertion_and_binding_weakening(phase4_tools, phase4_step2_snapshot, mutation, phase4_step3_snapshot):
    path = "tests/unit/test_phase4_contracts.py"
    before = (phase4_step2_snapshot / path).read_bytes()
    after = (phase4_step3_snapshot / path).read_bytes()
    verify = phase4_tools["verify_phase4_step3_test_migration"]
    verify(path, before, after)
    if mutation == "old_assertion":
        original = b'    assert control["active_phase"] == 4 and control["active_step"] == 2\n'
        assert after.count(original) == 1
        after = after.replace(original, b"    assert True\n", 1)
    elif mutation == "wrong_snapshot":
        original = (b'def test_phase4_step2_control_cannot_mint_extra_permission(phase4_tools, phase4_step2_snapshot):\n'
                    b'    control = json.loads((phase4_step2_snapshot / "PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\n')
        assert after.count(original) == 1
        after = after.replace(original, original.replace(b'(phase4_step2_snapshot /', b'(ROOT /'), 1)
    elif mutation == "rebind_node":
        after += b"\ndef test_phase4_step2_fixed_boundary_opens_only_approved_existing_paths():\n    assert True\n"
    else:
        after += b"\ndef test_phase4_step3_mutator(value=globals().clear()):\n    pass\n"
    with pytest.raises(ValueError):
        verify(path, before, after)


def test_phase4_step4_approved_control_keeps_independent_step3_anchors(phase4_tools, phase4_step4_snapshot):
    control = json.loads((phase4_step4_snapshot / "PHASE_4_BASELINE.json").read_text(encoding="utf-8"))
    assert phase4_tools["PHASE4_STEP3_FINAL"] == "974545c456e535ba1e1c5b6bf4ae0ce25bc04b57"
    assert phase4_tools["PHASE4_STEP3_TREE"] == "15498f3f00d0ce048c3cba2156eb7a44f096ae88"
    assert phase4_tools["PHASE4_STEP3_TEST_TREE"] == "17b87858f77ee4413c98cfd76f16f52170246741"
    assert control["active_phase"] == 4 and control["active_step"] == 4
    assert control["approval_basis"] == "继续"
    assert control["baseline_commit"] == BASELINE
    assert control["previous_step_commit"] == "974545c456e535ba1e1c5b6bf4ae0ce25bc04b57"
    assert control["previous_step_tree"] == "15498f3f00d0ce048c3cba2156eb7a44f096ae88"
    assert control["previous_step_test_tree"] == "17b87858f77ee4413c98cfd76f16f52170246741"
    assert control["previous_step_core_tests"] == 2876
    assert control["previous_step_parquet_tests"] == 2879
    assert len(control["previous_step_files_sha256"]) == 227
    assert set(control["runtime_paths_authorized"]) == {
        "src/recursive_integrity_toolkit/result.py",
        "src/recursive_integrity_toolkit/reports/assembly.py",
        "src/recursive_integrity_toolkit/config.py",
        "src/recursive_integrity_toolkit/utils/hashing.py",
        "src/recursive_integrity_toolkit/utils/logging.py",
    }
    assert control["schema_changes_authorized"] is False
    assert control["schema_paths_authorized"] == []
    assert control["new_files_permitted"] == []
    for name in ("phase_complete", "next_step_authorized", "main_merge_authorized", "publication_authorized"):
        assert control[name] is False
    phase4_tools["verify_phase4_step4_control"](control, step=4)
    with pytest.raises(ValueError):
        phase4_tools["verify_phase4_step3_control"](control, step=3)


@pytest.mark.parametrize("field,value", [
    ("active_phase", 3), ("active_phase", True),
    ("active_step", 3), ("active_step", 5), ("active_step", True),
    ("approval_basis", "approved by this manifest"),
    ("previous_step_commit", "0000000000000000000000000000000000000000"),
    ("previous_step_tree", "0000000000000000000000000000000000000000"),
    ("previous_step_test_tree", "0000000000000000000000000000000000000000"),
    ("previous_step_files_sha256", {}), ("baseline_files_sha256", {}),
    ("previous_step_core_tests", 1), ("previous_step_parquet_tests", 1),
    ("runtime_paths_authorized", ["src/recursive_integrity_toolkit/cli.py"]),
    ("schema_changes_authorized", True), ("schema_paths_authorized", ["schemas/report.schema.json"]),
    ("new_files_permitted", ["src/recursive_integrity_toolkit/reports/privacy.py"]),
    ("permitted_paths", ["src/recursive_integrity_toolkit/reports/json_report.py"]),
    ("phase_complete", True), ("next_step_authorized", True),
    ("main_merge_authorized", True), ("publication_authorized", True),
])
def test_phase4_step4_control_rejects_forged_scope_and_stage(phase4_tools, field, value, phase4_step4_snapshot):
    control = json.loads((phase4_step4_snapshot / "PHASE_4_BASELINE.json").read_text(encoding="utf-8"))
    verify = phase4_tools["verify_phase4_step4_control"]
    verify(control, step=4)
    control[field] = value
    with pytest.raises(ValueError):
        verify(control, step=4)


@pytest.mark.parametrize("step", [0, 1, 2, 3, 5, 11, True, "4", None])
def test_phase4_step4_control_rejects_unapproved_dispatch(phase4_tools, step, phase4_step4_snapshot):
    control = json.loads((phase4_step4_snapshot / "PHASE_4_BASELINE.json").read_text(encoding="utf-8"))
    phase4_tools["verify_phase4_step4_control"](control, step=4)
    with pytest.raises(ValueError):
        phase4_tools["verify_phase4_step4_control"](control, step=step)


@pytest.mark.parametrize("field", ["active_step", "previous_step_commit", "runtime_paths_authorized", "schema_paths_authorized"])
def test_phase4_step4_control_requires_explicit_approval_fields(phase4_tools, field, phase4_step4_snapshot):
    control = json.loads((phase4_step4_snapshot / "PHASE_4_BASELINE.json").read_text(encoding="utf-8"))
    phase4_tools["verify_phase4_step4_control"](control)
    del control[field]
    with pytest.raises(ValueError):
        phase4_tools["verify_phase4_step4_control"](control)


def test_phase4_step4_control_cannot_mint_extra_permission(phase4_tools, phase4_step4_snapshot):
    control = json.loads((phase4_step4_snapshot / "PHASE_4_BASELINE.json").read_text(encoding="utf-8"))
    phase4_tools["verify_phase4_step4_control"](control)
    control["approved_scope_expansion"] = {"step": 5, "renderers": True}
    with pytest.raises(ValueError):
        phase4_tools["verify_phase4_step4_control"](control)


def test_phase4_step4_fixed_boundary_opens_only_approved_existing_paths(phase4_tools):
    approved = {
        "PHASE_4_BASELINE.json", "PHASE_4_DECISIONS.md", "scripts/check_traceability.py",
        "scripts/check_spec_consistency.py", "scripts/release_check.py", "tests/conftest.py",
        "tests/unit/test_phase4_contracts.py", "tests/integration/test_phase4_gates.py",
        "tests/integration/test_no_algorithms.py", "tests/integration/test_ci_workflows.py",
        "tests/integration/test_repository_structure.py", "tests/integration/test_owner_ids.py",
        "tests/integration/test_package_import.py", "tests/integration/test_package_install.py",
        "tests/integration/test_optional_dependency.py", "tests/integration/test_no_network.py",
        "tests/integration/test_schema_json.py", "tests/integration/test_hero_structure.py",
        "tests/integration/test_prohibited_structure.py", "tests/integration/test_license_notices.py",
        ".github/workflows/ci.yml", ".github/workflows/security.yml",
        ".github/workflows/golden.yml", ".github/workflows/release.yml",
        "docs/architecture.md", "docs/theory_traceability.md",
        "src/recursive_integrity_toolkit/result.py", "src/recursive_integrity_toolkit/reports/assembly.py",
        "src/recursive_integrity_toolkit/config.py", "src/recursive_integrity_toolkit/utils/hashing.py",
        "src/recursive_integrity_toolkit/utils/logging.py", "docs/privacy.md", "docs/report_schema.md",
        "tests/unit/test_PR015_redaction.py", "tests/unit/test_PR016_determinism.py",
        "tests/unit/test_PR018_language.py",
    }
    assert set(phase4_tools["PHASE4_STEP4_ALLOWED"]) == approved
    assert set(phase4_tools["PHASE4_STEP4_NEW"]) == set()
    phase4_tools["verify_phase4_step4_changes"]([("M", path) for path in sorted(approved)])


@pytest.mark.parametrize("status,path", [
    ("M", "src/recursive_integrity_toolkit/metrics/diversity.py"),
    ("M", "src/recursive_integrity_toolkit/models.py"),
    ("M", "src/recursive_integrity_toolkit/utils/paths.py"),
    ("M", "src/recursive_integrity_toolkit/cli.py"),
    ("M", "src/recursive_integrity_toolkit/reports/json_report.py"),
    ("M", "src/recursive_integrity_toolkit/reports/markdown_report.py"),
    ("M", "schemas/report.schema.json"), ("M", "schemas/config.schema.json"),
    ("M", "tests/golden/phase3_math_cases.json"),
    ("M", "tests/unit/test_PR012_evidence_classes.py"),
    ("M", "tests/unit/test_PR013_report_schema.py"),
    ("M", "tests/unit/test_PR014_unavailable.py"),
    ("M", "PHASE_4_PLAN.md"), ("M", "pyproject.toml"),
    ("A", "src/recursive_integrity_toolkit/utils/hashing.py"),
    ("A", "tests/unit/test_phase4_step4_new.py"), ("A", "PHASE_4_COMPLETION.md"),
    ("D", "docs/privacy.md"), ("R100", "docs/privacy.md"),
    ("T", "scripts/release_check.py"), ("M", "./scripts/release_check.py"),
    ("M", "scripts/../scripts/release_check.py"),
])
def test_phase4_step4_diff_rejects_unopened_paths_and_nonmodification_operations(phase4_tools, status, path):
    with pytest.raises(ValueError):
        phase4_tools["verify_phase4_step4_changes"]([(status, path)])


def test_phase4_step4_diff_rejects_duplicate_operations(phase4_tools):
    with pytest.raises(ValueError):
        phase4_tools["verify_phase4_step4_changes"]([
            ("M", "docs/privacy.md"), ("M", "docs/privacy.md"),
        ])


def test_phase4_step4_historical_migrations_preserve_ten_step3_gate_nodes(phase4_tools, phase4_step3_snapshot, phase4_step4_snapshot):
    registry = phase4_tools["PHASE4_STEP4_MIGRATIONS"]
    expected = {
        "tests/unit/test_phase4_contracts.py": {
            "test_phase4_step3_approved_control_keeps_independent_step2_anchors",
            "test_phase4_step3_control_rejects_forged_scope_and_stage",
            "test_phase4_step3_control_rejects_unapproved_dispatch",
            "test_phase4_step3_control_requires_explicit_approval_fields",
            "test_phase4_step3_control_cannot_mint_extra_permission",
            "test_phase4_step3_historical_migrations_preserve_ten_step2_gate_nodes",
            "test_phase4_step3_historical_guard_rejects_assertion_and_binding_weakening",
        },
        "tests/integration/test_phase4_gates.py": {
            "test_phase4_step3_current_runtime_opens_only_assembly_and_freezes_schema",
            "test_phase4_step3_current_workflows_preserve_matrix_and_use_active_dispatch",
            "test_phase4_step3_current_snapshot_checks_valid_tree_before_mutations",
        },
    }
    assert set(registry) == set(expected)
    assert sum(len(rows) for rows in registry.values()) == 13
    for path, nodes in expected.items():
        assert {row["node"] for row in registry[path]} == nodes
        phase4_tools["verify_phase4_step4_test_migration"](
            path, (phase4_step3_snapshot / path).read_bytes(), (phase4_step4_snapshot / path).read_bytes(),
        )


@pytest.mark.parametrize("mutation", ["old_assertion", "wrong_snapshot", "rebind_node", "definition_effect"])
def test_phase4_step4_historical_guard_rejects_assertion_and_binding_weakening(phase4_tools, phase4_step3_snapshot, mutation, phase4_step4_snapshot):
    path = "tests/unit/test_phase4_contracts.py"
    before = (phase4_step3_snapshot / path).read_bytes()
    after = (phase4_step4_snapshot / path).read_bytes()
    verify = phase4_tools["verify_phase4_step4_test_migration"]
    verify(path, before, after)
    if mutation == "old_assertion":
        original = b'    assert control["active_phase"] == 4 and control["active_step"] == 3\n'
        assert after.count(original) == 1
        after = after.replace(original, b"    assert True\n", 1)
    elif mutation == "wrong_snapshot":
        original = (b'def test_phase4_step3_control_cannot_mint_extra_permission(phase4_tools, phase4_step3_snapshot):\n'
                    b'    control = json.loads((phase4_step3_snapshot / "PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\n')
        assert after.count(original) == 1
        after = after.replace(original, original.replace(b'(phase4_step3_snapshot /', b'(ROOT /'), 1)
    elif mutation == "rebind_node":
        after += b"\ndef test_phase4_step3_fixed_boundary_opens_only_approved_existing_paths():\n    assert True\n"
    else:
        after += b"\ndef test_phase4_step4_mutator(value=globals().clear()):\n    pass\n"
    with pytest.raises(ValueError):
        verify(path, before, after)


def test_phase4_step4_inherited_config_and_file_hash_helpers_preserve_exact_bodies(phase4_step3_snapshot):
    import ast

    for relative in ("config.py", "utils/hashing.py"):
        path = "src/recursive_integrity_toolkit/" + relative
        old = (phase4_step3_snapshot / path).read_text(encoding="utf-8")
        current = (ROOT / path).read_text(encoding="utf-8")
        original_nodes = [node for node in ast.parse(old).body
                          if isinstance(node, (ast.FunctionDef, ast.ClassDef))]
        current_nodes = [node for node in ast.parse(current).body
                         if isinstance(node, (ast.FunctionDef, ast.ClassDef))]
        assert original_nodes
        for node in original_nodes:
            matches = [candidate for candidate in current_nodes if candidate.name == node.name]
            assert len(matches) == 1, (relative, node.name)
            assert ast.get_source_segment(old, node) == ast.get_source_segment(current, matches[0]), (relative, node.name)


def test_phase4_step4_reviewed_ast_identity_is_portable_without_ignoring_semantics():
    import ast

    checker = runpy.run_path(str(ROOT / "scripts/check_traceability.py"), run_name="phase4_step4_portable_ast")
    digest = checker["_phase4_step4_ast_digest"]
    source = 'def protect(value: str) -> str:\n    return "safe:" + value\n\nclass View:\n    enabled = True\n'
    with_empty_parameters = ast.parse(source).body
    without_parameters = ast.parse(source).body
    for node in with_empty_parameters:
        if "type_params" not in node._fields:
            node._fields = (*node._fields, "type_params")
        node.type_params = []
    for node in without_parameters:
        if hasattr(node, "type_params"):
            del node.type_params
    assert digest(with_empty_parameters) == digest(without_parameters)
    for changed in (source.replace('"safe:"', '"raw:"'), source.replace("enabled = True", "enabled = False"),
                    source.replace("value: str", "value: bytes")):
        assert digest(ast.parse(changed).body) != digest(without_parameters)
    with_empty_parameters[0].type_params = [ast.Name(id="UnapprovedGeneric", ctx=ast.Load())]
    assert digest(with_empty_parameters) != digest(without_parameters)


def test_phase4_step5_approved_control_keeps_independent_step4_anchors(phase4_tools, phase4_step5_snapshot):
    control = json.loads((phase4_step5_snapshot / "PHASE_4_BASELINE.json").read_text(encoding="utf-8"))
    assert phase4_tools["PHASE4_STEP4_FINAL"] == "49454a9b162cb8d35e38d1cb1ae32cb208d3a01c"
    assert phase4_tools["PHASE4_STEP4_TREE"] == "79264d845e08f73ee68e160dea04f7786f18fd0a"
    assert phase4_tools["PHASE4_STEP4_TEST_TREE"] == "4aa4ca0b22f8b8c25afe27feeaba713d6f0830bf"
    assert control["active_phase"] == 4 and control["active_step"] == 5
    assert control["approval_basis"] == "很好，Phase 4 Step 5 继续"
    assert control["baseline_commit"] == BASELINE
    assert control["previous_step_commit"] == "49454a9b162cb8d35e38d1cb1ae32cb208d3a01c"
    assert control["previous_step_tree"] == "79264d845e08f73ee68e160dea04f7786f18fd0a"
    assert control["previous_step_test_tree"] == "4aa4ca0b22f8b8c25afe27feeaba713d6f0830bf"
    assert control["previous_step_core_tests"] == 3071
    assert control["previous_step_parquet_tests"] == 3074
    assert len(control["previous_step_files_sha256"]) == 227
    assert set(control["runtime_paths_authorized"]) == {
        "src/recursive_integrity_toolkit/reports/json_report.py",
        "src/recursive_integrity_toolkit/reports/markdown_report.py",
    }
    assert control["schema_changes_authorized"] is False
    assert control["schema_paths_authorized"] == []
    assert control["new_files_permitted"] == []
    for name in ("phase_complete", "next_step_authorized", "main_merge_authorized", "publication_authorized"):
        assert control[name] is False
    phase4_tools["verify_phase4_step5_control"](control, step=5)
    with pytest.raises(ValueError):
        phase4_tools["verify_phase4_step4_control"](control, step=4)


@pytest.mark.parametrize("field,value", [
    ("active_phase", 3), ("active_phase", True),
    ("active_step", 4), ("active_step", 6), ("active_step", True),
    ("approval_basis", "approved by this manifest"),
    ("previous_step_commit", "0000000000000000000000000000000000000000"),
    ("previous_step_tree", "0000000000000000000000000000000000000000"),
    ("previous_step_test_tree", "0000000000000000000000000000000000000000"),
    ("previous_step_files_sha256", {}), ("baseline_files_sha256", {}),
    ("previous_step_core_tests", 1), ("previous_step_parquet_tests", 1),
    ("runtime_paths_authorized", ["src/recursive_integrity_toolkit/cli.py"]),
    ("schema_changes_authorized", True), ("schema_paths_authorized", ["schemas/report.schema.json"]),
    ("new_files_permitted", ["src/recursive_integrity_toolkit/reports/privacy.py"]),
    ("permitted_paths", ["src/recursive_integrity_toolkit/cli.py"]),
    ("phase_complete", True), ("next_step_authorized", True),
    ("main_merge_authorized", True), ("publication_authorized", True),
])
def test_phase4_step5_control_rejects_forged_scope_and_stage(phase4_tools, field, value, phase4_step5_snapshot):
    control = json.loads((phase4_step5_snapshot / "PHASE_4_BASELINE.json").read_text(encoding="utf-8"))
    verify = phase4_tools["verify_phase4_step5_control"]
    verify(control, step=5)
    control[field] = value
    with pytest.raises(ValueError):
        verify(control, step=5)


@pytest.mark.parametrize("step", [0, 1, 2, 3, 4, 6, 11, True, "5", None])
def test_phase4_step5_control_rejects_unapproved_dispatch(phase4_tools, step, phase4_step5_snapshot):
    control = json.loads((phase4_step5_snapshot / "PHASE_4_BASELINE.json").read_text(encoding="utf-8"))
    phase4_tools["verify_phase4_step5_control"](control, step=5)
    with pytest.raises(ValueError):
        phase4_tools["verify_phase4_step5_control"](control, step=step)


@pytest.mark.parametrize("field", ["active_step", "previous_step_commit", "runtime_paths_authorized", "schema_paths_authorized"])
def test_phase4_step5_control_requires_explicit_approval_fields(phase4_tools, field, phase4_step5_snapshot):
    control = json.loads((phase4_step5_snapshot / "PHASE_4_BASELINE.json").read_text(encoding="utf-8"))
    phase4_tools["verify_phase4_step5_control"](control)
    del control[field]
    with pytest.raises(ValueError):
        phase4_tools["verify_phase4_step5_control"](control)


def test_phase4_step5_control_cannot_mint_extra_permission(phase4_tools, phase4_step5_snapshot):
    control = json.loads((phase4_step5_snapshot / "PHASE_4_BASELINE.json").read_text(encoding="utf-8"))
    phase4_tools["verify_phase4_step5_control"](control)
    control["approved_scope_expansion"] = {"step": 6, "publication": True}
    with pytest.raises(ValueError):
        phase4_tools["verify_phase4_step5_control"](control)


def test_phase4_step5_fixed_boundary_opens_only_approved_existing_paths(phase4_tools):
    approved = {
        "PHASE_4_BASELINE.json", "PHASE_4_DECISIONS.md", "scripts/check_traceability.py",
        "scripts/check_spec_consistency.py", "scripts/release_check.py", "tests/conftest.py",
        "tests/unit/test_phase4_contracts.py", "tests/integration/test_phase4_gates.py",
        "tests/integration/test_no_algorithms.py", "tests/integration/test_ci_workflows.py",
        "tests/integration/test_repository_structure.py", "tests/integration/test_owner_ids.py",
        "tests/integration/test_package_import.py", "tests/integration/test_package_install.py",
        "tests/integration/test_optional_dependency.py", "tests/integration/test_no_network.py",
        "tests/integration/test_schema_json.py", "tests/integration/test_hero_structure.py",
        "tests/integration/test_prohibited_structure.py", "tests/integration/test_license_notices.py",
        ".github/workflows/ci.yml", ".github/workflows/security.yml",
        ".github/workflows/golden.yml", ".github/workflows/release.yml",
        "docs/architecture.md", "docs/theory_traceability.md",
        "src/recursive_integrity_toolkit/reports/json_report.py",
        "src/recursive_integrity_toolkit/reports/markdown_report.py", "docs/report_schema.md",
        "tests/unit/test_PR013_report_schema.py", "tests/unit/test_PR016_determinism.py",
        "tests/unit/test_PR018_language.py",
    }
    assert set(phase4_tools["PHASE4_STEP5_ALLOWED"]) == approved
    assert set(phase4_tools["PHASE4_STEP5_NEW"]) == set()
    phase4_tools["verify_phase4_step5_changes"]([("M", path) for path in sorted(approved)])


@pytest.mark.parametrize("status,path", [
    ("M", "src/recursive_integrity_toolkit/metrics/diversity.py"),
    ("M", "src/recursive_integrity_toolkit/models.py"),
    ("M", "src/recursive_integrity_toolkit/utils/paths.py"),
    ("M", "src/recursive_integrity_toolkit/cli.py"),
    ("M", "src/recursive_integrity_toolkit/reports/assembly.py"),
    ("M", "src/recursive_integrity_toolkit/reports/html_report.py"),
    ("M", "src/recursive_integrity_toolkit/result.py"),
    ("M", "src/recursive_integrity_toolkit/config.py"),
    ("M", "src/recursive_integrity_toolkit/utils/hashing.py"),
    ("M", "src/recursive_integrity_toolkit/utils/logging.py"),
    ("M", "schemas/report.schema.json"), ("M", "schemas/config.schema.json"),
    ("M", "tests/golden/phase3_math_cases.json"),
    ("M", "tests/unit/test_PR012_evidence_classes.py"),
    ("M", "tests/unit/test_PR015_redaction.py"),
    ("M", "tests/unit/test_PR014_unavailable.py"),
    ("M", "PHASE_4_PLAN.md"), ("M", "pyproject.toml"),
    ("A", "src/recursive_integrity_toolkit/reports/json_report.py"),
    ("A", "tests/unit/test_phase4_step5_new.py"), ("A", "PHASE_4_COMPLETION.md"),
    ("D", "docs/report_schema.md"), ("R100", "docs/report_schema.md"),
    ("T", "scripts/release_check.py"), ("M", "./scripts/release_check.py"),
    ("M", "scripts/../scripts/release_check.py"),
])
def test_phase4_step5_diff_rejects_unopened_paths_and_nonmodification_operations(phase4_tools, status, path):
    with pytest.raises(ValueError):
        phase4_tools["verify_phase4_step5_changes"]([(status, path)])


def test_phase4_step5_diff_rejects_duplicate_operations(phase4_tools):
    with pytest.raises(ValueError):
        phase4_tools["verify_phase4_step5_changes"]([
            ("M", "docs/report_schema.md"), ("M", "docs/report_schema.md"),
        ])


def test_phase4_step5_historical_migrations_preserve_ten_step4_gate_nodes(phase4_tools, phase4_step4_snapshot, phase4_step5_snapshot):
    registry = phase4_tools["PHASE4_STEP5_MIGRATIONS"]
    expected = {
        "tests/unit/test_phase4_contracts.py": {
            "test_phase4_step4_approved_control_keeps_independent_step3_anchors",
            "test_phase4_step4_control_rejects_forged_scope_and_stage",
            "test_phase4_step4_control_rejects_unapproved_dispatch",
            "test_phase4_step4_control_requires_explicit_approval_fields",
            "test_phase4_step4_control_cannot_mint_extra_permission",
            "test_phase4_step4_historical_migrations_preserve_ten_step3_gate_nodes",
            "test_phase4_step4_historical_guard_rejects_assertion_and_binding_weakening",
        },
        "tests/integration/test_phase4_gates.py": {
            "test_phase4_step4_current_runtime_opens_only_privacy_metadata_modules_and_freezes_schema",
            "test_phase4_step4_current_workflows_preserve_matrix_and_use_active_dispatch",
            "test_phase4_step4_current_snapshot_checks_valid_tree_before_mutations",
        },
    }
    assert set(registry) == set(expected)
    assert sum(len(rows) for rows in registry.values()) == 13
    for path, nodes in expected.items():
        assert {row["node"] for row in registry[path]} == nodes
        phase4_tools["verify_phase4_step5_test_migration"](
            path, (phase4_step4_snapshot / path).read_bytes(), (phase4_step5_snapshot / path).read_bytes(),
        )


@pytest.mark.parametrize("mutation", ["old_assertion", "wrong_snapshot", "rebind_node", "definition_effect"])
def test_phase4_step5_historical_guard_rejects_assertion_and_binding_weakening(phase4_tools, phase4_step4_snapshot, mutation, phase4_step5_snapshot):
    path = "tests/unit/test_phase4_contracts.py"
    before = (phase4_step4_snapshot / path).read_bytes()
    after = (phase4_step5_snapshot / path).read_bytes()
    verify = phase4_tools["verify_phase4_step5_test_migration"]
    verify(path, before, after)
    if mutation == "old_assertion":
        original = b'    assert control["active_phase"] == 4 and control["active_step"] == 4\n'
        assert after.count(original) == 1
        after = after.replace(original, b"    assert True\n", 1)
    elif mutation == "wrong_snapshot":
        original = (b'def test_phase4_step4_control_cannot_mint_extra_permission(phase4_tools, phase4_step4_snapshot):\n'
                    b'    control = json.loads((phase4_step4_snapshot / "PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\n')
        assert after.count(original) == 1
        after = after.replace(original, original.replace(b'(phase4_step4_snapshot /', b'(ROOT /'), 1)
    elif mutation == "rebind_node":
        after += b"\ndef test_phase4_step4_fixed_boundary_opens_only_approved_existing_paths():\n    assert True\n"
    else:
        after += b"\ndef test_phase4_step5_mutator(value=globals().clear()):\n    pass\n"
    with pytest.raises(ValueError):
        verify(path, before, after)


def test_phase4_step6_approved_control_keeps_independent_step5_anchors(phase4_tools, phase4_step6_snapshot):
    control = json.loads((phase4_step6_snapshot / "PHASE_4_BASELINE.json").read_text(encoding="utf-8"))
    assert phase4_tools["PHASE4_STEP5_FINAL"] == "c1667179e895a798bba2349960162542efa5ef87"
    assert phase4_tools["PHASE4_STEP5_TREE"] == "d83f9fc8e0b569f2d796bd2a83b87422fe350fba"
    assert phase4_tools["PHASE4_STEP5_TEST_TREE"] == "974f8e65904c24ed4e226996eaf571aab6123965"
    assert control["active_phase"] == 4 and control["active_step"] == 6
    assert control["approval_basis"] == "批准开始Phase 4   **Step 6**"
    assert control["baseline_commit"] == BASELINE
    assert control["previous_step_commit"] == "c1667179e895a798bba2349960162542efa5ef87"
    assert control["previous_step_tree"] == "d83f9fc8e0b569f2d796bd2a83b87422fe350fba"
    assert control["previous_step_test_tree"] == "974f8e65904c24ed4e226996eaf571aab6123965"
    assert control["previous_step_core_tests"] == 3215
    assert control["previous_step_parquet_tests"] == 3218
    assert len(control["previous_step_files_sha256"]) == 227
    assert set(control["runtime_paths_authorized"]) == {
        "src/recursive_integrity_toolkit/utils/paths.py",
        "src/recursive_integrity_toolkit/utils/logging.py",
    }
    assert control["schema_changes_authorized"] is False
    assert control["schema_paths_authorized"] == []
    assert control["new_files_permitted"] == ["tests/unit/test_phase4_output_safety.py"]
    for name in ("phase_complete", "next_step_authorized", "main_merge_authorized", "publication_authorized"):
        assert control[name] is False
    phase4_tools["verify_phase4_step6_control"](control, step=6)
    with pytest.raises(ValueError):
        phase4_tools["verify_phase4_step4_control"](control, step=4)


@pytest.mark.parametrize("field,value", [
    ("active_phase", 3), ("active_phase", True),
    ("active_step", 5), ("active_step", 7), ("active_step", True),
    ("approval_basis", "approved by this manifest"),
    ("previous_step_commit", "0000000000000000000000000000000000000000"),
    ("previous_step_tree", "0000000000000000000000000000000000000000"),
    ("previous_step_test_tree", "0000000000000000000000000000000000000000"),
    ("previous_step_files_sha256", {}), ("baseline_files_sha256", {}),
    ("previous_step_core_tests", 1), ("previous_step_parquet_tests", 1),
    ("runtime_paths_authorized", ["src/recursive_integrity_toolkit/cli.py"]),
    ("schema_changes_authorized", True), ("schema_paths_authorized", ["schemas/report.schema.json"]),
    ("new_files_permitted", ["src/recursive_integrity_toolkit/reports/privacy.py"]),
    ("permitted_paths", ["src/recursive_integrity_toolkit/cli.py"]),
    ("phase_complete", True), ("next_step_authorized", True),
    ("main_merge_authorized", True), ("publication_authorized", True),
])
def test_phase4_step6_control_rejects_forged_scope_and_stage(phase4_tools, field, value, phase4_step6_snapshot):
    control = json.loads((phase4_step6_snapshot / "PHASE_4_BASELINE.json").read_text(encoding="utf-8"))
    verify = phase4_tools["verify_phase4_step6_control"]
    verify(control, step=6)
    control[field] = value
    with pytest.raises(ValueError):
        verify(control, step=6)


@pytest.mark.parametrize("step", [0, 1, 2, 3, 4, 5, 7, 11, True, "6", None])
def test_phase4_step6_control_rejects_unapproved_dispatch(phase4_tools, step, phase4_step6_snapshot):
    control = json.loads((phase4_step6_snapshot / "PHASE_4_BASELINE.json").read_text(encoding="utf-8"))
    phase4_tools["verify_phase4_step6_control"](control, step=6)
    with pytest.raises(ValueError):
        phase4_tools["verify_phase4_step6_control"](control, step=step)


@pytest.mark.parametrize("field", ["active_step", "previous_step_commit", "runtime_paths_authorized", "schema_paths_authorized"])
def test_phase4_step6_control_requires_explicit_approval_fields(phase4_tools, field, phase4_step6_snapshot):
    control = json.loads((phase4_step6_snapshot / "PHASE_4_BASELINE.json").read_text(encoding="utf-8"))
    phase4_tools["verify_phase4_step6_control"](control)
    del control[field]
    with pytest.raises(ValueError):
        phase4_tools["verify_phase4_step6_control"](control)


def test_phase4_step6_control_cannot_mint_extra_permission(phase4_tools, phase4_step6_snapshot):
    control = json.loads((phase4_step6_snapshot / "PHASE_4_BASELINE.json").read_text(encoding="utf-8"))
    phase4_tools["verify_phase4_step6_control"](control)
    control["approved_scope_expansion"] = {"step": 6, "publication": True}
    with pytest.raises(ValueError):
        phase4_tools["verify_phase4_step6_control"](control)


def test_phase4_step6_fixed_boundary_opens_only_approved_existing_paths(phase4_tools):
    approved = {
        "PHASE_4_BASELINE.json", "PHASE_4_DECISIONS.md", "scripts/check_traceability.py",
        "scripts/check_spec_consistency.py", "scripts/release_check.py", "tests/conftest.py",
        "tests/unit/test_phase4_contracts.py", "tests/integration/test_phase4_gates.py",
        "tests/integration/test_no_algorithms.py", "tests/integration/test_ci_workflows.py",
        "tests/integration/test_repository_structure.py", "tests/integration/test_owner_ids.py",
        "tests/integration/test_package_import.py", "tests/integration/test_package_install.py",
        "tests/integration/test_optional_dependency.py", "tests/integration/test_no_network.py",
        "tests/integration/test_schema_json.py", "tests/integration/test_hero_structure.py",
        "tests/integration/test_prohibited_structure.py", "tests/integration/test_license_notices.py",
        ".github/workflows/ci.yml", ".github/workflows/security.yml",
        ".github/workflows/golden.yml", ".github/workflows/release.yml",
        "docs/architecture.md", "docs/theory_traceability.md",
        "src/recursive_integrity_toolkit/utils/paths.py",
        "src/recursive_integrity_toolkit/utils/logging.py", "docs/privacy.md", "docs/cli.md",
        "tests/unit/test_phase4_output_safety.py",
    }
    assert set(phase4_tools["PHASE4_STEP6_ALLOWED"]) == approved
    assert set(phase4_tools["PHASE4_STEP6_NEW"]) == {"tests/unit/test_phase4_output_safety.py"}
    phase4_tools["verify_phase4_step6_changes"]([("A" if path == "tests/unit/test_phase4_output_safety.py" else "M", path) for path in sorted(approved)])


@pytest.mark.parametrize("status,path", [
    ("M", "src/recursive_integrity_toolkit/cli.py"),
    ("M", "src/recursive_integrity_toolkit/reports/json_report.py"),
    ("M", "src/recursive_integrity_toolkit/reports/markdown_report.py"),
    ("M", "src/recursive_integrity_toolkit/result.py"),
    ("M", "src/recursive_integrity_toolkit/metrics/diversity.py"),
    ("M", "schemas/report.schema.json"), ("M", "pyproject.toml"),
    ("M", "PHASE_4_PLAN.md"), ("M", "tests/unit/test_phase4_output_safety.py"),
    ("A", "tests/unit/test_phase4_unknown.py"), ("A", "PHASE_4_COMPLETION.md"),
    ("A", "src/recursive_integrity_toolkit/utils/paths.py"),
    ("D", "docs/cli.md"), ("R100", "docs/privacy.md"),
    ("T", "scripts/release_check.py"), ("M", "./scripts/release_check.py"),
])
def test_phase4_step6_diff_rejects_paths_and_operations(phase4_tools, status, path):
    with pytest.raises(ValueError):
        phase4_tools["verify_phase4_step6_changes"]([(status, path)])


def test_phase4_step6_diff_rejects_duplicate_operations(phase4_tools):
    with pytest.raises(ValueError):
        phase4_tools["verify_phase4_step6_changes"]([("M", "docs/cli.md"), ("M", "docs/cli.md")])


def test_phase4_step6_historical_bindings_preserve_assertions_and_headers(phase4_tools, phase4_step5_snapshot, phase4_step6_snapshot):
    import ast

    registry = phase4_tools["PHASE4_STEP6_MIGRATIONS"]
    assert set(registry) == {"tests/unit/test_phase4_contracts.py", "tests/integration/test_phase4_gates.py"}
    assert sorted(len(rows) for rows in registry.values()) == [7, 8]
    expected_inventory = {"phase4_mutation_tree"} | {
        "test_phase4_step" + str(step) + "_current_snapshot_checks_valid_tree_before_mutations"
        for step in (2, 3, 4, 5)
    }
    inventory_seen = set()
    for path, rows in registry.items():
        phase4_tools["verify_phase4_step6_test_migration"](
            path, (phase4_step5_snapshot / path).read_bytes(), (phase4_step6_snapshot / path).read_bytes())
        for row in rows:
            trees = [ast.parse(row[key]) for key in ("old", "new")]
            assertions = [[ast.dump(n) for n in ast.walk(tree) if isinstance(n, ast.Assert)] for tree in trees]
            assert assertions[0] == assertions[1]
            assert trees[0].body[0].name == trees[1].body[0].name == row["node"]
            if row["node"] in expected_inventory:
                inventory_seen.add(row["node"])
                assert '"ls-files"' in row["old"] and 'rglob("*")' in row["new"]
    assert inventory_seen == expected_inventory


@pytest.mark.parametrize("mutation", ["assertion", "binding", "inventory", "logging", "shadow", "default"])
def test_phase4_step6_historical_guard_rejects_weakening(phase4_tools, phase4_step5_snapshot, mutation, phase4_step6_snapshot):
    path = "tests/integration/test_phase4_gates.py" if mutation in ("inventory", "logging") else "tests/unit/test_phase4_contracts.py"
    before = (phase4_step5_snapshot / path).read_bytes()
    after = (phase4_step6_snapshot / path).read_bytes()
    verify = phase4_tools["verify_phase4_step6_test_migration"]
    verify(path, before, after)
    if mutation == "assertion":
        needle = b'    assert control["active_phase"] == 4 and control["active_step"] == 5\n'
        assert after.count(needle) == 1
        after = after.replace(needle, b"    assert True\n", 1)
    elif mutation == "binding":
        needle = b'json.loads((phase4_step5_snapshot / "PHASE_4_BASELINE.json").read_text(encoding="utf-8"))'
        assert needle in after
        after = after.replace(needle, needle.replace(b"phase4_step5_snapshot", b"ROOT"), 1)
    elif mutation == "inventory":
        needle = b'for path in phase4_step1_snapshot.rglob("*") if path.is_file()'
        assert after.count(needle) == 1
        after = after.replace(needle, needle.replace(b"phase4_step1_snapshot", b"repo_root"), 1)
    elif mutation == "logging":
        needle = b'(phase4_step5_snapshot if relative == "utils/logging.py" else repo_root)'
        assert after.count(needle) == 1
        after = after.replace(needle, b"repo_root", 1)
    elif mutation == "shadow":
        after += b"\ndef test_phase4_step5_fixed_boundary_opens_only_approved_existing_paths():\n    assert True\n"
    else:
        after += b"\ndef test_phase4_step6_bad(value=globals().clear()):\n    pass\n"
    with pytest.raises(ValueError):
        verify(path, before, after)


def test_phase4_step7_approved_control_keeps_independent_step6_anchors(phase4_tools, phase4_step7_snapshot):
    control = json.loads((phase4_step7_snapshot / "PHASE_4_BASELINE.json").read_text(encoding="utf-8"))
    assert phase4_tools["PHASE4_STEP6_FINAL"] == "aa2355f2359c3af4fc05345c792f9903b0d5858c"
    assert phase4_tools["PHASE4_STEP6_TREE"] == "d9b6910079f49a2c739f86eceec05040918a41a5"
    assert phase4_tools["PHASE4_STEP6_TEST_TREE"] == "8d3a03c61da807d1fef8d26fc4af0d6f72e4546e"
    assert control["active_phase"] == 4 and control["active_step"] == 7
    assert control["approval_basis"] == "Phase 4 Step 7 继续"
    assert control["baseline_commit"] == BASELINE
    assert control["previous_step_commit"] == "aa2355f2359c3af4fc05345c792f9903b0d5858c"
    assert control["previous_step_tree"] == "d9b6910079f49a2c739f86eceec05040918a41a5"
    assert control["previous_step_test_tree"] == "8d3a03c61da807d1fef8d26fc4af0d6f72e4546e"
    assert control["previous_step_core_tests"] == 3420
    assert control["previous_step_parquet_tests"] == 3423
    assert len(control["previous_step_files_sha256"]) == 228
    assert set(control["runtime_paths_authorized"]) == {
        "src/recursive_integrity_toolkit/cli.py",
        "src/recursive_integrity_toolkit/config.py",
    }
    assert control["schema_changes_authorized"] is False
    assert control["schema_paths_authorized"] == []
    assert control["new_files_permitted"] == ["tests/integration/test_phase4_cli.py"]
    for name in ("phase_complete", "next_step_authorized", "main_merge_authorized", "publication_authorized"):
        assert control[name] is False
    phase4_tools["verify_phase4_step7_control"](control, step=7)
    with pytest.raises(ValueError):
        phase4_tools["verify_phase4_step4_control"](control, step=4)


@pytest.mark.parametrize("field,value", [
    ("active_phase", 3), ("active_phase", True),
    ("active_step", 6), ("active_step", 8), ("active_step", True),
    ("approval_basis", "approved by this manifest"),
    ("previous_step_commit", "0000000000000000000000000000000000000000"),
    ("previous_step_tree", "0000000000000000000000000000000000000000"),
    ("previous_step_test_tree", "0000000000000000000000000000000000000000"),
    ("previous_step_files_sha256", {}), ("baseline_files_sha256", {}),
    ("previous_step_core_tests", 1), ("previous_step_parquet_tests", 1),
    ("runtime_paths_authorized", ["src/recursive_integrity_toolkit/cli.py"]),
    ("schema_changes_authorized", True), ("schema_paths_authorized", ["schemas/report.schema.json"]),
    ("new_files_permitted", ["src/recursive_integrity_toolkit/reports/privacy.py"]),
    ("permitted_paths", ["src/recursive_integrity_toolkit/cli.py"]),
    ("phase_complete", True), ("next_step_authorized", True),
    ("main_merge_authorized", True), ("publication_authorized", True),
])
def test_phase4_step7_control_rejects_forged_scope_and_stage(phase4_tools, field, value, phase4_step7_snapshot):
    control = json.loads((phase4_step7_snapshot / "PHASE_4_BASELINE.json").read_text(encoding="utf-8"))
    verify = phase4_tools["verify_phase4_step7_control"]
    verify(control, step=7)
    control[field] = value
    with pytest.raises(ValueError):
        verify(control, step=7)


@pytest.mark.parametrize("step", [0, 1, 2, 3, 4, 5, 6, 8, 11, True, "7", None])
def test_phase4_step7_control_rejects_unapproved_dispatch(phase4_tools, step, phase4_step7_snapshot):
    control = json.loads((phase4_step7_snapshot / "PHASE_4_BASELINE.json").read_text(encoding="utf-8"))
    phase4_tools["verify_phase4_step7_control"](control, step=7)
    with pytest.raises(ValueError):
        phase4_tools["verify_phase4_step7_control"](control, step=step)


@pytest.mark.parametrize("field", ["active_step", "previous_step_commit", "runtime_paths_authorized", "schema_paths_authorized"])
def test_phase4_step7_control_requires_explicit_approval_fields(phase4_tools, field, phase4_step7_snapshot):
    control = json.loads((phase4_step7_snapshot / "PHASE_4_BASELINE.json").read_text(encoding="utf-8"))
    phase4_tools["verify_phase4_step7_control"](control)
    del control[field]
    with pytest.raises(ValueError):
        phase4_tools["verify_phase4_step7_control"](control)


def test_phase4_step7_control_cannot_mint_extra_permission(phase4_tools, phase4_step7_snapshot):
    control = json.loads((phase4_step7_snapshot / "PHASE_4_BASELINE.json").read_text(encoding="utf-8"))
    phase4_tools["verify_phase4_step7_control"](control)
    control["approved_scope_expansion"] = {"step": 7, "publication": True}
    with pytest.raises(ValueError):
        phase4_tools["verify_phase4_step7_control"](control)


def test_phase4_step7_fixed_boundary_opens_only_approved_existing_paths(phase4_tools):
    approved = {
        "PHASE_4_BASELINE.json", "PHASE_4_DECISIONS.md", "scripts/check_traceability.py",
        "scripts/check_spec_consistency.py", "scripts/release_check.py", "tests/conftest.py",
        "tests/unit/test_phase4_contracts.py", "tests/integration/test_phase4_gates.py",
        "tests/integration/test_no_algorithms.py", "tests/integration/test_ci_workflows.py",
        "tests/integration/test_repository_structure.py", "tests/integration/test_owner_ids.py",
        "tests/integration/test_package_import.py", "tests/integration/test_package_install.py",
        "tests/integration/test_optional_dependency.py", "tests/integration/test_no_network.py",
        "tests/integration/test_schema_json.py", "tests/integration/test_hero_structure.py",
        "tests/integration/test_prohibited_structure.py", "tests/integration/test_license_notices.py",
        ".github/workflows/ci.yml", ".github/workflows/security.yml",
        ".github/workflows/golden.yml", ".github/workflows/release.yml",
        "docs/architecture.md", "docs/theory_traceability.md",
        "src/recursive_integrity_toolkit/cli.py",
        "src/recursive_integrity_toolkit/config.py", "tests/integration/test_cli_validation.py", "docs/cli.md",
        "tests/integration/test_phase4_cli.py",
    }
    assert set(phase4_tools["PHASE4_STEP7_ALLOWED"]) == approved
    assert set(phase4_tools["PHASE4_STEP7_NEW"]) == {"tests/integration/test_phase4_cli.py"}
    phase4_tools["verify_phase4_step7_changes"]([("A" if path == "tests/integration/test_phase4_cli.py" else "M", path) for path in sorted(approved)])


@pytest.mark.parametrize("status,path", [
    ("M", "src/recursive_integrity_toolkit/utils/paths.py"),
    ("M", "src/recursive_integrity_toolkit/utils/logging.py"),
    ("M", "src/recursive_integrity_toolkit/reports/assembly.py"),
    ("M", "src/recursive_integrity_toolkit/metrics/diversity.py"),
    ("M", "schemas/report.schema.json"), ("M", "pyproject.toml"),
    ("M", "PHASE_4_PLAN.md"), ("M", "tests/integration/test_phase4_cli.py"),
    ("A", "tests/unit/test_phase4_unknown.py"), ("A", "PHASE_4_COMPLETION.md"),
    ("A", "src/recursive_integrity_toolkit/cli.py"), ("M", "docs/privacy.md"),
    ("D", "docs/cli.md"), ("R100", "docs/cli.md"),
    ("T", "scripts/release_check.py"), ("M", "./scripts/release_check.py"),
])
def test_phase4_step7_diff_rejects_paths_and_operations(phase4_tools, status, path):
    with pytest.raises(ValueError):
        phase4_tools["verify_phase4_step7_changes"]([(status, path)])


def test_phase4_step7_diff_rejects_duplicate_operations(phase4_tools):
    with pytest.raises(ValueError):
        phase4_tools["verify_phase4_step7_changes"]([("M", "docs/cli.md"), ("M", "docs/cli.md")])


def test_phase4_step7_historical_bindings_preserve_assertions(phase4_tools, phase4_step6_snapshot, phase4_step7_snapshot):
    import ast
    registry = phase4_tools["PHASE4_STEP7_MIGRATIONS"]
    assert set(registry) == {"tests/unit/test_phase4_contracts.py", "tests/integration/test_phase4_gates.py"}
    assert sorted(len(rows) for rows in registry.values()) == [5, 7]
    for path, rows in registry.items():
        phase4_tools["verify_phase4_step7_test_migration"](path, (phase4_step6_snapshot / path).read_bytes(), (phase4_step7_snapshot / path).read_bytes())
        for row in rows:
            trees = [ast.parse(row[key]) for key in ("old", "new")]
            assert trees[0].body[0].name == trees[1].body[0].name == row["node"]
            assertions = [[ast.dump(n) for n in ast.walk(tree) if isinstance(n, ast.Assert)] for tree in trees]
            assert assertions[0] == assertions[1]


@pytest.mark.parametrize("mutation", ["assertion", "binding", "config", "shadow", "default"])
def test_phase4_step7_historical_guard_rejects_weakening(phase4_tools, phase4_step6_snapshot, mutation, phase4_step7_snapshot):
    path = "tests/integration/test_phase4_gates.py" if mutation == "config" else "tests/unit/test_phase4_contracts.py"
    before, after = (phase4_step6_snapshot / path).read_bytes(), (phase4_step7_snapshot / path).read_bytes()
    verify = phase4_tools["verify_phase4_step7_test_migration"]
    verify(path, before, after)
    if mutation == "assertion":
        needle = b'    assert control["active_phase"] == 4 and control["active_step"] == 6\n'
        assert after.count(needle) == 1
        after = after.replace(needle, b"    assert True\n", 1)
    elif mutation == "binding":
        needle = b'json.loads((phase4_step6_snapshot / "PHASE_4_BASELINE.json").read_text(encoding="utf-8"))'
        assert needle in after
        after = after.replace(needle, needle.replace(b"phase4_step6_snapshot", b"ROOT"), 1)
    elif mutation == "config":
        needle = b'else phase4_step6_snapshot if relative == "config.py" else repo_root'
        assert after.count(needle) == 1
        after = after.replace(needle, b"else repo_root", 1)
    elif mutation == "shadow":
        after += b"\ndef test_phase4_step6_fixed_boundary_opens_only_approved_existing_paths():\n    assert True\n"
    else:
        after += b"\ndef test_phase4_step7_bad(value=globals().clear()):\n    pass\n"
    with pytest.raises(ValueError):
        verify(path, before, after)


def test_phase4_step8_approved_control_keeps_independent_step7_anchors(phase4_tools, phase4_step8_snapshot):
    control = json.loads((phase4_step8_snapshot / "PHASE_4_BASELINE.json").read_text(encoding="utf-8"))
    assert phase4_tools["PHASE4_STEP7_FINAL"] == "bacd33ae65e392872776c6d976401fdc3d565f63"
    assert phase4_tools["PHASE4_STEP7_TREE"] == "4c16914bb0f0c5281efc36624efb8b1a1d4a174e"
    assert phase4_tools["PHASE4_STEP7_TEST_TREE"] == "96317cb7b25236b79efc0f2d93e1e0f5f132fdb2"
    assert control["active_phase"] == 4 and control["active_step"] == 8
    assert control["approval_basis"] == "phase 4 step 8 开始"
    assert control["baseline_commit"] == BASELINE
    assert control["previous_step_commit"] == "bacd33ae65e392872776c6d976401fdc3d565f63"
    assert control["previous_step_tree"] == "4c16914bb0f0c5281efc36624efb8b1a1d4a174e"
    assert control["previous_step_test_tree"] == "96317cb7b25236b79efc0f2d93e1e0f5f132fdb2"
    assert control["previous_step_core_tests"] == 3620
    assert control["previous_step_parquet_tests"] == 3623
    assert len(control["previous_step_files_sha256"]) == 229
    assert set(control["runtime_paths_authorized"]) == {
        "src/recursive_integrity_toolkit/cli.py",
        "src/recursive_integrity_toolkit/config.py",
    }
    assert control["schema_changes_authorized"] is False
    assert control["schema_paths_authorized"] == []
    assert control["new_files_permitted"] == ['src/recursive_integrity_toolkit/data/hero/EXPECTED_OUTPUTS.md', 'src/recursive_integrity_toolkit/data/hero/config.json', 'src/recursive_integrity_toolkit/data/hero/provenance.csv', 'src/recursive_integrity_toolkit/data/hero/records_v1.csv', 'src/recursive_integrity_toolkit/data/hero/records_v2.csv', 'src/recursive_integrity_toolkit/data/hero/version_order.json', 'src/recursive_integrity_toolkit/data/report.schema.json']
    for name in ("phase_complete", "next_step_authorized", "main_merge_authorized", "publication_authorized"):
        assert control[name] is False
    phase4_tools["verify_phase4_step8_control"](control, step=8)
    with pytest.raises(ValueError):
        phase4_tools["verify_phase4_step4_control"](control, step=4)


@pytest.mark.parametrize("field,value", [
    ("active_phase", 3), ("active_phase", True),
    ("active_step", 7), ("active_step", 9), ("active_step", True),
    ("approval_basis", "approved by this manifest"),
    ("previous_step_commit", "0000000000000000000000000000000000000000"),
    ("previous_step_tree", "0000000000000000000000000000000000000000"),
    ("previous_step_test_tree", "0000000000000000000000000000000000000000"),
    ("previous_step_files_sha256", {}), ("baseline_files_sha256", {}),
    ("previous_step_core_tests", 1), ("previous_step_parquet_tests", 1),
    ("runtime_paths_authorized", ["src/recursive_integrity_toolkit/cli.py"]),
    ("schema_changes_authorized", True), ("schema_paths_authorized", ["schemas/report.schema.json"]),
    ("new_files_permitted", ["src/recursive_integrity_toolkit/reports/privacy.py"]),
    ("permitted_paths", ["src/recursive_integrity_toolkit/cli.py"]),
    ("phase_complete", True), ("next_step_authorized", True),
    ("main_merge_authorized", True), ("publication_authorized", True),
])
def test_phase4_step8_control_rejects_forged_scope_and_stage(phase4_tools, field, value, phase4_step8_snapshot):
    control = json.loads((phase4_step8_snapshot / "PHASE_4_BASELINE.json").read_text(encoding="utf-8"))
    verify = phase4_tools["verify_phase4_step8_control"]
    verify(control, step=8)
    control[field] = value
    with pytest.raises(ValueError):
        verify(control, step=8)


@pytest.mark.parametrize("step", [0, 1, 2, 3, 4, 5, 6, 7, 9, 11, True, "8", None])
def test_phase4_step8_control_rejects_unapproved_dispatch(phase4_tools, step, phase4_step8_snapshot):
    control = json.loads((phase4_step8_snapshot / "PHASE_4_BASELINE.json").read_text(encoding="utf-8"))
    phase4_tools["verify_phase4_step8_control"](control, step=8)
    with pytest.raises(ValueError):
        phase4_tools["verify_phase4_step8_control"](control, step=step)


@pytest.mark.parametrize("field", ["active_step", "previous_step_commit", "runtime_paths_authorized", "schema_paths_authorized"])
def test_phase4_step8_control_requires_explicit_approval_fields(phase4_tools, field, phase4_step8_snapshot):
    control = json.loads((phase4_step8_snapshot / "PHASE_4_BASELINE.json").read_text(encoding="utf-8"))
    phase4_tools["verify_phase4_step8_control"](control)
    del control[field]
    with pytest.raises(ValueError):
        phase4_tools["verify_phase4_step8_control"](control)


def test_phase4_step8_control_cannot_mint_extra_permission(phase4_tools, phase4_step8_snapshot):
    control = json.loads((phase4_step8_snapshot / "PHASE_4_BASELINE.json").read_text(encoding="utf-8"))
    phase4_tools["verify_phase4_step8_control"](control)
    control["approved_scope_expansion"] = {"step": 8, "publication": True}
    with pytest.raises(ValueError):
        phase4_tools["verify_phase4_step8_control"](control)


def test_phase4_step8_fixed_boundary_opens_only_approved_existing_paths(phase4_tools):
    approved = {
        "PHASE_4_BASELINE.json", "PHASE_4_DECISIONS.md", "scripts/check_traceability.py",
        "scripts/check_spec_consistency.py", "scripts/release_check.py", "tests/conftest.py",
        "tests/unit/test_phase4_contracts.py", "tests/integration/test_phase4_gates.py",
        "tests/integration/test_no_algorithms.py", "tests/integration/test_ci_workflows.py",
        "tests/integration/test_repository_structure.py", "tests/integration/test_owner_ids.py",
        "tests/integration/test_package_import.py", "tests/integration/test_package_install.py",
        "tests/integration/test_optional_dependency.py", "tests/integration/test_no_network.py",
        "tests/integration/test_schema_json.py", "tests/integration/test_hero_structure.py",
        "tests/integration/test_prohibited_structure.py", "tests/integration/test_license_notices.py",
        ".github/workflows/ci.yml", ".github/workflows/security.yml",
        ".github/workflows/golden.yml", ".github/workflows/release.yml",
        "docs/architecture.md", "docs/theory_traceability.md",
        "src/recursive_integrity_toolkit/cli.py",
        "src/recursive_integrity_toolkit/config.py", "pyproject.toml", "tests/integration/test_hero_end_to_end.py", "docs/cli.md",
        "tests/integration/test_phase4_cli.py",
    }
    resources = {'src/recursive_integrity_toolkit/data/report.schema.json', 'src/recursive_integrity_toolkit/data/hero/version_order.json', 'src/recursive_integrity_toolkit/data/hero/config.json', 'src/recursive_integrity_toolkit/data/hero/EXPECTED_OUTPUTS.md', 'src/recursive_integrity_toolkit/data/hero/records_v2.csv', 'src/recursive_integrity_toolkit/data/hero/provenance.csv', 'src/recursive_integrity_toolkit/data/hero/records_v1.csv'}
    approved.update(resources)
    assert len(approved) == 39
    assert set(phase4_tools["PHASE4_STEP8_ALLOWED"]) == approved
    assert set(phase4_tools["PHASE4_STEP8_NEW"]) == resources
    phase4_tools["verify_phase4_step8_changes"]([("A" if path in resources else "M", path) for path in sorted(approved)])


@pytest.mark.parametrize("status,path", [
    ("M", "src/recursive_integrity_toolkit/metrics/diversity.py"),
    ("M", "src/recursive_integrity_toolkit/reports/assembly.py"),
    ("M", "schemas/report.schema.json"), ("M", "examples/hero/config.json"),
    ("M", "PHASE_4_PLAN.md"), ("A", "tests/integration/test_phase4_cli.py"),
    ("M", "src/recursive_integrity_toolkit/data/hero/config.json"),
    ("A", "src/recursive_integrity_toolkit/data/other.json"),
    ("A", "PHASE_4_COMPLETION.md"), ("D", "docs/cli.md"),
    ("R100", "pyproject.toml"), ("T", "scripts/release_check.py"),
])
def test_phase4_step8_diff_rejects_paths_and_operations(phase4_tools, status, path):
    with pytest.raises(ValueError):
        phase4_tools["verify_phase4_step8_changes"]([(status, path)])


def test_phase4_step8_historical_bindings_preserve_assertions(phase4_tools, phase4_step7_snapshot, phase4_step8_snapshot):
    import ast
    registry = phase4_tools["PHASE4_STEP8_MIGRATIONS"]
    assert sorted(len(rows) for rows in registry.values()) == [4, 7]
    for path, rows in registry.items():
        phase4_tools["verify_phase4_step8_test_migration"](path, (phase4_step7_snapshot / path).read_bytes(), (phase4_step8_snapshot / path).read_bytes())
        for row in rows:
            trees = [ast.parse(row[key]) for key in ("old", "new")]
            assert trees[0].body[0].name == trees[1].body[0].name == row["node"]
            assert [[ast.dump(n) for n in ast.walk(t) if isinstance(n, ast.Assert)] for t in trees][0] == [[ast.dump(n) for n in ast.walk(t) if isinstance(n, ast.Assert)] for t in trees][1]


@pytest.mark.parametrize("mutation", ["assertion", "binding", "shadow", "default"])
def test_phase4_step8_historical_guard_rejects_weakening(phase4_tools, phase4_step7_snapshot, mutation, phase4_step8_snapshot):
    path = "tests/unit/test_phase4_contracts.py"
    before, after = (phase4_step7_snapshot / path).read_bytes(), (phase4_step8_snapshot / path).read_bytes()
    verify = phase4_tools["verify_phase4_step8_test_migration"]
    verify(path, before, after)
    if mutation == "assertion":
        needle = b'    assert control["active_phase"] == 4 and control["active_step"] == 7\n'
        assert after.count(needle) == 1
        after = after.replace(needle, b"    assert True\n", 1)
    elif mutation == "binding":
        needle = b'json.loads((phase4_step7_snapshot / "PHASE_4_BASELINE.json").read_text(encoding="utf-8"))'
        assert needle in after
        after = after.replace(needle, needle.replace(b"phase4_step7_snapshot", b"ROOT"), 1)
    elif mutation == "shadow":
        after += b"\ndef test_phase4_step7_fixed_boundary_opens_only_approved_existing_paths():\n    assert True\n"
    else:
        after += b"\ndef test_phase4_step8_bad(value=globals().clear()):\n    pass\n"
    with pytest.raises(ValueError): verify(path, before, after)


def test_phase4_step9_control_keeps_step8_acceptance_and_freezes_runtime(phase4_tools):
    control = json.loads((ROOT / "PHASE_4_BASELINE.json").read_text(encoding="utf-8"))
    assert control["active_phase"] == 4 and control["active_step"] == 10
    assert control["approval_basis"] == "Phase 4 Step 10 开始"
    assert control["previous_step_commit"] == "ad2cb5d0cb34dac9036593bac4e91c9d993bcfc6"
    assert control["previous_step_tree"] == "64d81ceed83304dca5a5c2cfccf82641819549f1"
    assert control["previous_step_test_tree"] == "a6c60ed13c274da73ad085d0989c6a7a4641e203"
    assert control["previous_step_core_tests"] == 3959
    assert control["previous_step_parquet_tests"] == 3962
    assert "previous_step_files_sha256" not in control
    assert control["runtime_paths_authorized"] == ["src/recursive_integrity_toolkit/reports/assembly.py"]
    assert control["schema_paths_authorized"] == []
    assert control["runtime_changes_authorized"] is True
    assert control["runtime_repair_approval_basis"] == "批准"
    assert control["package_resource_copies"] == {}
    assert control["report_goldens_authorized"] is False
    for key in ("schema_changes_authorized", "package_data_declaration_only", "phase_complete", "next_step_authorized", "main_merge_authorized", "publication_authorized"):
        assert control[key] is False
    phase4_tools["verify_phase4_current_control"](control, step=10)
    with pytest.raises(ValueError):
        phase4_tools["verify_phase4_step8_control"](control, step=8)


@pytest.mark.parametrize("field,value", [
    ("active_step", 8), ("active_step", 9), ("active_phase", True),
    ("approval_basis", "approved by manifest"), ("previous_step_commit", "0000000000000000000000000000000000000000"),
    ("previous_step_tree", "0000000000000000000000000000000000000000"), ("previous_step_test_tree", "0000000000000000000000000000000000000000"),
    ("previous_step_files_sha256", {}), ("previous_step_core_tests", 1),
    ("runtime_changes_authorized", False), ("runtime_paths_authorized", ["src/recursive_integrity_toolkit/cli.py"]),
    ("schema_changes_authorized", True), ("package_data_declaration_only", True),
    ("new_files_permitted", ["src/recursive_integrity_toolkit/data/extra.json"]),
    ("report_goldens_authorized", True), ("permitted_paths", []),
    ("next_step_authorized", True), ("phase_complete", True), ("publication_authorized", True),
])
def test_phase4_step9_control_rejects_forged_permission(phase4_tools, field, value):
    control = json.loads((ROOT / "PHASE_4_BASELINE.json").read_text(encoding="utf-8"))
    verify = phase4_tools["verify_phase4_current_control"]
    verify(control)
    control[field] = value
    with pytest.raises(ValueError):
        verify(control)


@pytest.mark.parametrize("step", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, True, "10", None])
def test_phase4_step9_control_requires_exact_stage(phase4_tools, step):
    control = json.loads((ROOT / "PHASE_4_BASELINE.json").read_text(encoding="utf-8"))
    with pytest.raises(ValueError):
        phase4_tools["verify_phase4_current_control"](control, step=step)


def test_phase4_step9_allowlist_is_exact_common_g_plus_named_report_paths(phase4_tools):
    """The current canonical scope permits Step 10 performance, common maintenance and the approved assembly repair."""
    additional = {"tests/performance/test_hero_runtime.py", "tests/performance/test_metadata_100k.py",
                  "tests/performance/README.md", "tests/integration/test_phase4_cli.py",
                  "src/recursive_integrity_toolkit/reports/assembly.py"}
    allowed = phase4_tools["PHASE4_G"] | additional
    assert len(allowed) == 31
    assert phase4_tools["PHASE4_CURRENT_ALLOWED"] == allowed
    phase4_tools["verify_phase4_current_changes"]([("M", p) for p in sorted(allowed)])


@pytest.mark.parametrize("status,path", [
    ("M", "src/recursive_integrity_toolkit/cli.py"), ("M", "schemas/report.schema.json"),
    ("M", "src/recursive_integrity_toolkit/data/hero/config.json"), ("M", "pyproject.toml"),
    ("M", "PHASE_4_PLAN.md"), ("M", "tests/golden/phase3_math_cases.json"),
    ("M", "tests/golden/test_phase4_reports.py"), ("A", "PHASE_4_COMPLETION.md"),
    ("A", "scripts/build_golden.py"), ("M", "tests/golden/phase4_hero_report.json"),
    ("D", "tests/golden/README.md"), ("R100", "scripts/release_check.py"),
    ("T", "scripts/normalize_golden.py"), ("M", "./scripts/build_golden.py"),
])
def test_phase4_step9_diff_rejects_wrong_paths_or_operations(phase4_tools, status, path):
    with pytest.raises(ValueError):
        phase4_tools["verify_phase4_current_changes"]([(status, path)])


def test_phase4_step9_rejects_duplicate_diff_entries(phase4_tools):
    with pytest.raises(ValueError):
        phase4_tools["verify_phase4_current_changes"]([("M", "tests/performance/test_hero_runtime.py"), ("M", "tests/performance/test_hero_runtime.py")])


def test_phase4_step9_exact_historical_migrations_preserve_assertions_and_parameters(phase4_tools, phase4_step8_snapshot):
    import ast
    registry = phase4_tools["PHASE4_STEP9_MIGRATIONS"]
    assert sorted(len(rows) for rows in registry.values()) == [2, 7]
    for path, rows in registry.items():
        phase4_tools["verify_phase4_step9_test_migration"](path, (phase4_step8_snapshot / path).read_bytes(), (ROOT / path).read_bytes())
        for row in rows:
            old, new = [ast.parse(row[k]) for k in ("old", "new")]
            assert old.body[0].name == new.body[0].name == row["node"]
            assert [ast.dump(n) for n in ast.walk(old) if isinstance(n, ast.Assert)] == [ast.dump(n) for n in ast.walk(new) if isinstance(n, ast.Assert)]
            assert [n.arg for n in new.body[0].args.args] == [n.arg for n in old.body[0].args.args] + ["phase4_step8_snapshot"]


@pytest.mark.parametrize("mutation", ["assertion", "binding", "shadow", "default", "decorator", "import"])
def test_phase4_step9_historical_migration_rejects_weakening(phase4_tools, phase4_step8_snapshot, mutation):
    path = "tests/unit/test_phase4_contracts.py"
    before, after = (phase4_step8_snapshot / path).read_bytes(), (ROOT / path).read_bytes()
    verify = phase4_tools["verify_phase4_step9_test_migration"]
    verify(path, before, after)
    if mutation == "assertion":
        after = after.replace(b'    assert control["active_phase"] == 4 and control["active_step"] == 8\n', b"    assert True\n", 1)
    elif mutation == "binding":
        after = after.replace(b'json.loads((phase4_step8_snapshot / "PHASE_4_BASELINE.json")', b'json.loads((ROOT / "PHASE_4_BASELINE.json")', 1)
    elif mutation == "shadow":
        after += b"\ndef test_phase4_step8_control_cannot_mint_extra_permission():\n    pass\n"
    elif mutation == "default":
        after += b"\ndef test_phase4_step9_bad(value=globals().clear()):\n    pass\n"
    elif mutation == "decorator":
        after += b"\n@pytest.mark.parametrize('x', list(range(1)))\ndef test_phase4_step9_bad(x):\n    pass\n"
    else:
        after += b"\nimport socket\n"
    with pytest.raises(ValueError):
        verify(path, before, after)


@pytest.mark.parametrize("mutation", ["complete", "missing_golden", "missing_math", "missing_registry", "extra_golden", "duplicate", "skipped", "empty_golden_collection"])
def test_phase4_step9_golden_evidence_requires_complete_collected_identity_set(phase4_tools, monkeypatch, tmp_path, mutation):
    import subprocess
    import xml.etree.ElementTree as ET
    from types import SimpleNamespace
    cases = json.loads((ROOT / "tests/golden/phase3_math_cases.json").read_bytes())["cases"]
    math = ["tests/golden/test_phase3_math.py::test_phase3_frozen_case[" + case["case_id"] + "]" for case in cases]
    registry = ["tests/golden/test_phase3_math.py::test_phase3_all_twenty_oracles_have_unique_traceable_identity"]
    reports = ["tests/golden/test_phase4_reports.py::test_literal[standard]", "tests/golden/test_phase4_reports.py::test_literal[redacted]"]
    collected = math + registry + ([] if mutation == "empty_golden_collection" else reports)
    def collect(command, **kwargs):
        assert command[-2:] == ["tests/golden/test_phase4_reports.py", "tests/golden/test_phase3_math.py"]
        assert "--collect-only" in command
        return SimpleNamespace(stdout="\n".join(collected) + "\n")
    monkeypatch.setattr(subprocess, "run", collect)
    executed = math + registry + reports
    if mutation == "missing_golden":
        executed = math + registry + reports[:1]
    elif mutation == "missing_math":
        executed = math[:-1] + registry + reports
    elif mutation == "missing_registry":
        executed = math + reports
    elif mutation == "extra_golden":
        executed += ["tests/golden/test_phase4_reports.py::test_uncollected"]
    elif mutation == "duplicate":
        executed += reports[:1]
    root = ET.Element("testsuite", tests=str(len(executed)), failures="0", errors="0", skipped="1" if mutation == "skipped" else "0")
    for node in executed:
        owner, name = node.split("::", 1)
        case = ET.SubElement(root, "testcase", classname=owner.removesuffix(".py").replace("/", "."), name=name)
        if mutation == "skipped" and node == reports[0]:
            ET.SubElement(case, "skipped")
    path = tmp_path / "golden.xml"
    ET.ElementTree(root).write(path, encoding="utf-8")
    if mutation == "complete":
        result = phase4_tools["phase4_step9_golden_evidence"](path)
        assert result["mathematical_cases"] == 20 and result["report_golden_tests"] == 2
        assert result["report_golden_nodeids"] == reports and result["mathematical_nodeids"] == math
        assert result["mathematical_registry_nodeid"] == registry[0]
        assert result["missing_nodeids"] == []
    else:
        with pytest.raises(ValueError):
            phase4_tools["phase4_step9_golden_evidence"](path)
