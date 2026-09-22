"""Audit explicit phase boundaries and retain tested intermediate artifacts.

Maintainer tooling only. Phase 2 authority and restoration guards stay frozen.
Phase 3 Step 11 verifies the final development milestone and its retained evidence.
Only the approved dev2 version literals change in the frozen runtime/metadata.
Publication, merge and later-phase implementation remain unauthorized.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tarfile
import tempfile
import tomllib
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
STEP9_BASELINE = "e1790d60b88370651eb59dc31fbb2343e2daec1f"
PHASE2_FINAL = "78554993febb01609cb90814cc24cce2012bf7d7"
PHASE2_TREE = "706b99e27c2d284a7435ae03e2eb2376214bfa46"
PHASE2_TEST_TREE = "d787d9b06c41a91f8587f6b57a8af710419d114f"
PLAN_SHA256 = "e1c9a6776e3cd2511d37a6bbbdb4a9d5a33b66ff6b00bc00bf3e08a01e6576f1"
ACTIVE_PHASE, ACTIVE_STEP = 3, 11
PHASE3_COMPLETE = True  # Accepted implementation below; final handoff still requires all roles on HEAD.
PHASE3_IMPLEMENTATION_ACCEPTANCE = "9dc321c6997a231209653a0f86d0476824e96e3a"
PHASE3_IMPLEMENTATION_TREE = "a1086ca95075aff3ea8a83afae548806b2079dc9"
STEP10_ALLOWED = {
    "README.md", "CHANGELOG.md", "docs/architecture.md", "docs/data_schema.md",
    "docs/privacy.md", ".github/workflows/ci.yml", ".github/workflows/security.yml",
    ".github/workflows/release.yml", ".github/workflows/golden.yml",
    "tests/integration/test_ci_workflows.py", "tests/integration/test_license_notices.py",
    "tests/integration/test_no_algorithms.py", "tests/integration/test_prohibited_structure.py",
    "tests/integration/test_repository_structure.py", "scripts/check_spec_consistency.py",
    "scripts/check_traceability.py", "scripts/release_check.py", "pyproject.toml",
    "PHASE_2_COMPLETION.md", "PHASE_2_VALIDATION_REPORT.md", "PHASE_2_ARCHITECTURE_COMPLIANCE_REPORT.md",
}
PHASE3_G = {
    "scripts/check_traceability.py", "scripts/check_spec_consistency.py", "scripts/release_check.py",
    "tests/conftest.py", "tests/integration/test_no_algorithms.py", "tests/integration/test_ci_workflows.py",
    "tests/integration/test_repository_structure.py", "tests/integration/test_owner_ids.py",
    "tests/integration/test_package_import.py", "tests/integration/test_package_install.py",
    "tests/integration/test_optional_dependency.py", "tests/integration/test_no_network.py",
    "tests/unit/test_PR016_determinism.py", ".github/workflows/ci.yml", ".github/workflows/security.yml",
    ".github/workflows/golden.yml", ".github/workflows/release.yml", "docs/architecture.md",
    "docs/theory_traceability.md", "PHASE_3_DECISIONS.md", "PHASE_3_BASELINE.json",
}
STEP1_NEW = {"PHASE_3_PLAN.md", "PHASE_3_DECISIONS.md", "PHASE_3_BASELINE.json",
             "tests/unit/test_phase3_contracts.py", "tests/golden/phase3_math_cases.json", "tests/golden/phase3_math_cases.md"}
STEP1_ALLOWED = PHASE3_G | STEP1_NEW | {
    "src/recursive_integrity_toolkit/models.py", "src/recursive_integrity_toolkit/errors.py"}
STEP1_FINAL = "20487e356239d5b5642b6fff595b381d0faa2a4e"
STEP1_TREE = "7d9867fb7543bfd50a9b01bb48530a3411121d31"
STEP2_NEW = {"tests/unit/test_T1_representation.py",
             "tests/fixtures/minimal_valid/phase3_field_records.jsonl",
             "tests/fixtures/invalid_schema/phase3_representation_cases.json"}
STEP2_EXCEPTION = "tests/unit/test_phase3_contracts.py"
STEP2_ALLOWED = PHASE3_G | STEP2_NEW | {
    "src/recursive_integrity_toolkit/representations/base.py",
    "src/recursive_integrity_toolkit/representations/field.py",
    "src/recursive_integrity_toolkit/models.py", "src/recursive_integrity_toolkit/errors.py",
    "docs/data_schema.md", STEP2_EXCEPTION,
}
STEP2_FINAL = "9e5d4c4f38834c42a5b7c19de4e67f471ab9bbca"
STEP2_TREE = "096e038145bced4b01f2c0059659082a72501112"
STEP3_NEW = {"tests/fixtures/minimal_valid/phase3_exact_content.jsonl"}
STEP3_ALLOWED = PHASE3_G | STEP3_NEW | {
    "src/recursive_integrity_toolkit/representations/content_hash.py",
    "src/recursive_integrity_toolkit/metrics/duplicates.py",
    "src/recursive_integrity_toolkit/models.py", "src/recursive_integrity_toolkit/errors.py",
    "tests/unit/test_PR006_duplicates.py", "tests/unit/test_T1_representation.py",
    "docs/data_schema.md", "docs/privacy.md",
}
STEP3_FINAL = "d2651ca755c82af2e2fec3963bcb6fe270a23be6"
STEP3_TREE = "7871e6253d770d1561d9f732dd5c0b0f842a4138"
STEP4_NEW = {"tests/fixtures/weighted/phase3_distribution_cases.json"}
STEP4_ALLOWED = PHASE3_G | STEP4_NEW | {
    "src/recursive_integrity_toolkit/metrics/diversity.py",
    "src/recursive_integrity_toolkit/models.py", "src/recursive_integrity_toolkit/errors.py",
    "tests/unit/test_T1_support.py", "tests/unit/test_T1_diversity.py",
    "tests/unit/test_phase3_contracts.py",
}
STEP4_FINAL = "b943a9712ed1e5b64e09c2c394077fdeed78114f"
STEP4_TREE = "e8f503b44cee0d3db059c03da6599fe44503f03b"
STEP5_NEW = {"tests/fixtures/provenance_partial/phase3_composition.json",
             "tests/fixtures/provenance_unknown/phase3_grounding_crossed.json",
             "tests/fixtures/weighted/phase3_source_weights.json"}
STEP5_ALLOWED = PHASE3_G | STEP5_NEW | {
    "src/recursive_integrity_toolkit/metrics/provenance.py",
    "src/recursive_integrity_toolkit/models.py", "src/recursive_integrity_toolkit/errors.py",
    "tests/unit/test_PR004_coverage.py", "tests/unit/test_PR005_source_shares.py", "tests/unit/test_T3_provenance.py",
}
STEP5_FINAL = "4611f897d054b352733cc90543eef6f6d71cd811"
STEP5_TREE = "faffd5717dc1bf99e0081a122a338c65a68a13a7"
STEP6_NEW = {"tests/fixtures/provenance_unknown/phase3_direct_bounds.json"}
STEP6_ALLOWED = PHASE3_G | STEP6_NEW | {
    "src/recursive_integrity_toolkit/metrics/bounds.py",
    "src/recursive_integrity_toolkit/models.py", "src/recursive_integrity_toolkit/errors.py",
    "tests/unit/test_T3_bounds.py", "tests/unit/test_T3_provenance.py",
}
STEP6_FINAL = "c7d5ceed2f154bd2ccffbe49961dbf1b65b9df63"
STEP6_TREE = "bc1878e10a9fd056afd196e85126af7ddb9555e5"
STEP7_NEW = {"tests/fixtures/minimal_valid/phase3_tail_cases.json"}
STEP7_ALLOWED = PHASE3_G | STEP7_NEW | {
    "src/recursive_integrity_toolkit/metrics/tail.py",
    "src/recursive_integrity_toolkit/models.py", "src/recursive_integrity_toolkit/errors.py",
    "tests/unit/test_T2_tail.py", "tests/unit/test_phase3_contracts.py",
}
STEP7_FINAL = "d3d95bde50762e60b4dd03cb2bd988618c9a10fe"
STEP7_TREE = "5cb81772542ebfa87c634572068dbf9ee49f41d0"
STEP8_NEW = {"tests/fixtures/resampling/phase3_closed_cases.json"}
STEP8_ALLOWED = PHASE3_G | STEP8_NEW | {
    "src/recursive_integrity_toolkit/metrics/resampling.py",
    "src/recursive_integrity_toolkit/models.py", "src/recursive_integrity_toolkit/errors.py",
    "tests/unit/test_T1_resampling.py", "tests/unit/test_T5_reopening.py", "tests/unit/test_phase3_contracts.py",
}
STEP8_FINAL = "a43cba0e81fd89c3b20a64737bfa89cd2bac4de9"
STEP8_TREE = "f7ecf2326770b362b51ba67357ec450e311a086a"
STEP9_NEW = {"tests/unit/test_T1_compatibility.py",
             "tests/fixtures/representation_compatible/phase3_pair.json",
             "tests/fixtures/representation_incompatible/phase3_pair.json"}
STEP9_ALLOWED = PHASE3_G | STEP9_NEW | {
    "src/recursive_integrity_toolkit/representations/compatibility.py",
    "src/recursive_integrity_toolkit/representations/field.py",
    "src/recursive_integrity_toolkit/metrics/diversity.py",
    "src/recursive_integrity_toolkit/models.py", "src/recursive_integrity_toolkit/errors.py",
    "tests/unit/test_T1_support.py", "tests/unit/test_T1_diversity.py", "tests/unit/test_T1_representation.py",
}
STEP9_FINAL = "03fe1e7e99c8170e6be7714649ab0d926e01b6d6"
STEP9_TREE = "765d28e6ff4715fa6d59f44760f1a937489d7120"
PHASE3_STEP10_NEW = {'tests/golden/test_phase3_math.py', 'tests/integration/test_phase3_metric_pipeline.py'}
PHASE3_STEP10_ALLOWED = PHASE3_G | PHASE3_STEP10_NEW | {'tests/golden/phase3_math_cases.md', 'tests/performance/test_hero_runtime.py', 'tests/golden/phase3_math_cases.json', 'tests/performance/test_metadata_100k.py'}
STEP10_FINAL = "150a2a105e01883672ef0c2300b41b0de3be352e"
STEP10_TREE = "b609cb75913fc6352729086819a24795caae1dd8"
STEP10_CONTROL_SHA256 = "8c48a575005b6b0ed78bba8dae21703b1edd6a42bd4a548ae57b083d4f5cc9bc"
PHASE3_STEP11_NEW = {"PHASE_3_COMPLETION.md", "PHASE_3_VALIDATION_REPORT.md",
                     "PHASE_3_ARCHITECTURE_COMPLIANCE_REPORT.md"}
STEP11_TEST_EXCEPTIONS = {"tests/integration/test_phase3_metric_pipeline.py",
                          "tests/unit/test_phase3_contracts.py"}
PHASE3_STEP11_ALLOWED = PHASE3_G | PHASE3_STEP11_NEW | STEP11_TEST_EXCEPTIONS | {
    "README.md", "CHANGELOG.md", "docs/data_schema.md", "docs/privacy.md", "docs/release_process.md",
    "pyproject.toml", "src/recursive_integrity_toolkit/__init__.py",
    "tests/integration/test_cli_validation.py", "tests/integration/test_license_notices.py",
    "tests/integration/test_prohibited_structure.py",
}
STEP10_RUNTIME_SHA256 = '11b427fa9add50bcd7b2230170ed84d2e4cb4985ade9ee8f9829da0460f12f35'
STEP10_FROZEN_FILES = {
    "PHASE_3_PLAN.md": "e1c9a6776e3cd2511d37a6bbbdb4a9d5a33b66ff6b00bc00bf3e08a01e6576f1",
    "examples/hero/EXPECTED_OUTPUTS.md": "64d5e696c5e6067b7c34fe85b4d75760588c77fbf19bdd61ee18120385ce8c67",
    "examples/hero/config.json": "2e069eb9c0105bf05c145ca15eec47834eb66f4408e8cdde9ff4935f5b920241",
    "examples/hero/provenance.csv": "fc4ed3921d087e37996228dd8a37c4c51a0a3c3c91ded3e62a21e1b10f407438",
    "examples/hero/records_v1.csv": "b62c9aee057c61f641009b949acb110e003acbea6a399cc607a78ee6e6f0543d",
    "examples/hero/records_v2.csv": "d691605fd6bb37e785945ae34c8c18ea8409201f7d78449d39df08df7770599b",
    "examples/hero/version_order.json": "3e33ca8b2095f35f55d22265071bce00119c9282b72bb02cee3275c646898387",
    "pyproject.toml": "bf3954bc42f3bd9c8275bd7c6858b32266ef014a8c17148b68453a97f3625033",
    "schemas/config.schema.json": "cc73411e59d77ded0f9a2a493a507c71901e0a30c7dbca548763a237241927d1",
    "schemas/normalized_manifest.schema.json": "13598968bd3ed9ec017759ac4e71a118965ee8895c8c6ba503d0e225fdfad766",
    "schemas/report.schema.json": "17130701fc683b3813f649bec45332fe923cd7259a76e6e8e261910207afc23b",
    "schemas/schema_mapping.schema.json": "31ef2691dbb11c7861caf15853d7bd0a6dcae25fd10bf26a7b4b1aaa968df85d",
    "schemas/version_order.schema.json": "94b10a5842b9f432703789d3388ec3c3d5d07e9224df4266ab29010c0390836d",
    "tests/golden/phase3_math_cases.json": "b494d50a1a9bd1009c060c998e4cb3c7433d0e8949f73a8d627e538fa38884b2",
    "tests/golden/phase3_math_cases.md": "5f3603ad6ad8f2b1274547f2c239461e7ee8d3b7d552b04d0dd868b862af4044"
}
CUMULATIVE_ALLOWED = STEP1_ALLOWED | STEP2_ALLOWED | STEP3_ALLOWED | STEP4_ALLOWED | STEP5_ALLOWED | STEP6_ALLOWED | STEP7_ALLOWED | STEP8_ALLOWED | STEP9_ALLOWED | PHASE3_STEP10_ALLOWED | PHASE3_STEP11_ALLOWED
CUMULATIVE_NEW = STEP1_NEW | STEP2_NEW | STEP3_NEW | STEP4_NEW | STEP5_NEW | STEP6_NEW | STEP7_NEW | STEP8_NEW | STEP9_NEW | PHASE3_STEP10_NEW | PHASE3_STEP11_NEW
COMPLETION = {"PHASE_2_COMPLETION.md", "PHASE_2_VALIDATION_REPORT.md", "PHASE_2_ARCHITECTURE_COMPLIANCE_REPORT.md"}
PROHIBITED = {"server", "webapp", "cloud", "telemetry", "plugins", "agents", "llm", "auth", "database", "policy_enforcement"}
PARQUET_CASES = {"test_PR002_parquet_real_roundtrip", "test_PR002_parquet_real_row_limit", "test_PR002_parquet_real_invalid_file"}
RESTORATION_PATH = "VALIDATION_PLAN.md"
RESTORATION_BEFORE_SHA256 = "564abf56c91141d0cd8ca09024f1cf6dda63bf4ba12acf6563bb7cbc158a84f7"
RESTORATION_AFTER_SHA256 = "16f5fe539da2b3cff1c3e0a2854208bd7fbc1e4c5b332684265b06a03a90cf2f"


def verify_approved_restoration(path: str, status: str, before: bytes, after: bytes) -> dict:
    """Historical guard; no new restoration permission is created."""
    if path != RESTORATION_PATH or status != "M":
        raise ValueError("Restoration exception does not authorize this path or change kind")
    if (type(before) is not bytes or type(after) is not bytes
            or hashlib.sha256(before).hexdigest() != RESTORATION_BEFORE_SHA256
            or hashlib.sha256(after).hexdigest() != RESTORATION_AFTER_SHA256):
        raise ValueError("Restoration exception requires the exact approved byte transition")
    return {"path": path, "before_sha256": RESTORATION_BEFORE_SHA256,
            "after_sha256": RESTORATION_AFTER_SHA256, "authorization": "Theory Owner exact restoration"}


def git(*args: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(ROOT), *args])


def verify_phase3_control(control: dict, step: int = ACTIVE_STEP) -> None:
    expected = {"active_phase": 3, "active_step": ACTIVE_STEP, "baseline_commit": PHASE2_FINAL,
                "baseline_tree": PHASE2_TREE, "baseline_test_tree": PHASE2_TEST_TREE,
                "approved_plan_sha256": PLAN_SHA256, "baseline_core_tests": 1159, "baseline_parquet_tests": 1162,
                "permitted_paths": sorted(PHASE3_STEP11_ALLOWED), "approved_decisions": [f"P3-D{i:02d}" for i in range(1, 11)],
                "phase_complete": PHASE3_COMPLETE, "next_step_authorized": False,
                "previous_step_commit": STEP10_FINAL, "previous_step_tree": STEP10_TREE,
                "new_files_permitted": sorted(PHASE3_STEP11_NEW), "main_merge_authorized": False,
                "publication_authorized": False,
                "implementation_acceptance_commit": PHASE3_IMPLEMENTATION_ACCEPTANCE,
                "implementation_acceptance_tree": PHASE3_IMPLEMENTATION_TREE}
    if type(control) is not dict or type(step) is not int or step != ACTIVE_STEP:
        raise ValueError("Unsupported active phase or step")
    for key, value in expected.items():
        if type(control.get(key)) is not type(value) or control[key] != value:
            raise ValueError(f"Frozen Phase 3 control mismatch: {key}")


def verify_phase3_changes(changes: list[tuple[str, str]], *, incremental: bool = False) -> None:
    allowed = PHASE3_STEP11_ALLOWED if incremental else CUMULATIVE_ALLOWED
    new_files = PHASE3_STEP11_NEW if incremental else CUMULATIVE_NEW
    for status, path in changes:
        if path not in allowed or status not in ("M", "A"):
            raise ValueError(f"Unauthorized active-stage change: {status} {path}")
        if status == "A" and path not in new_files:
            raise ValueError(f"Unapproved new file: {path}")


def verify_prior_step_changes(changes: list[tuple[str, str]], *, step: int) -> None:
    """Retain historical negative tests against their original permission sets."""
    boundaries = {1: (STEP1_ALLOWED, STEP1_NEW), 2: (STEP2_ALLOWED, STEP2_NEW),
                  3: (STEP3_ALLOWED, STEP3_NEW), 4: (STEP4_ALLOWED, STEP4_NEW), 5: (STEP5_ALLOWED, STEP5_NEW), 6: (STEP6_ALLOWED, STEP6_NEW), 7: (STEP7_ALLOWED, STEP7_NEW), 8: (STEP8_ALLOWED, STEP8_NEW), 9: (STEP9_ALLOWED, STEP9_NEW), 10: (PHASE3_STEP10_ALLOWED, PHASE3_STEP10_NEW)}
    if type(step) is not int or step not in boundaries:
        raise ValueError("Unsupported historical step")
    allowed, new_files = boundaries[step]
    for status, path in changes:
        if path not in allowed or status not in ("M", "A") or (status == "A" and path not in new_files):
            raise ValueError("Change was not authorized in the historical step")


def verify_step2_contract_test_migration(before: bytes, after: bytes) -> None:
    """Only the explicitly authorized forged-stage expression may change."""
    old = b'if key in ("active_phase","active_step"): control[key]=2'
    new = b'if key in ("active_phase","active_step"): control[key]+=1'
    if (type(before) is not bytes or type(after) is not bytes
            or before.count(old) != 1 or after != before.replace(old, new, 1)):
        raise ValueError("Step 2 contract-test exception exceeded its exact approved edit")


def verify_step10_control(control: dict) -> None:
    """Verify the immutable historical control independently of the active stage."""
    if (type(control) is not dict
            or hashlib.sha256(json.dumps(control, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
            != STEP10_CONTROL_SHA256):
        raise ValueError("Historical Step 10 control changed")


def verify_step11_contract_test_migration(before: bytes, after: bytes) -> None:
    """Only the two explicitly approved historical-stage bindings may change."""
    replacements = (
        (b'elif key=="phase_complete": control[key]=True',
         b'elif key=="phase_complete": control[key]=not control[key]'),
        (b'def test_phase3_final_completion_records_not_created():',
         b'def test_phase3_final_completion_records_not_created(phase3_step10_snapshot):'),
        (b'assert not (ROOT/name).exists()',
         b'assert not (phase3_step10_snapshot/name).exists()'),
    )
    if type(before) is not bytes or type(after) is not bytes:
        raise ValueError("Test migration requires source bytes")
    expected = before
    for old, new in replacements:
        if expected.count(old) != 1:
            raise ValueError("Historical contract test binding missing or duplicated")
        expected = expected.replace(old, new, 1)
    if after != expected:
        raise ValueError("Step 11 contract-test exception exceeded its exact approved edits")


def verify_step11_pipeline_test_migration(before: bytes, after: bytes) -> None:
    """Freeze every inherited test byte except the three approved stage bindings.

    Fresh Step 11 tests may only be appended. No inherited numerical assertion,
    parameter, fixture identity or test name is removed or weakened.
    """
    replacements = (
        (b'gate["verify_phase3_changes"]([("M",path)],incremental=True)',
         b'gate["verify_prior_step_changes"]([("M",path)],step=10)'),
        (b'def test_phase3_step10_scope_is_fixed_not_self_authorized(repo_root):',
         b'def test_phase3_step10_scope_is_fixed_not_self_authorized(repo_root,phase3_step10_snapshot):'),
        (b'control = json.loads((repo_root/"PHASE_3_BASELINE.json").read_bytes())',
         b'control = json.loads((phase3_step10_snapshot/"PHASE_3_BASELINE.json").read_bytes())'),
        (b'gate["verify_phase3_control"](control,10)', b'gate["verify_step10_control"](control)'),
        (b'gate["verify_phase3_control"](altered,10)', b'gate["verify_step10_control"](altered)'),
        (b'gate["verify_step10_snapshot"]()["runtime_modules_unchanged"]',
         b'gate["verify_step10_snapshot"](phase3_step10_snapshot)["runtime_modules_unchanged"]'),
        (b'def test_phase3_step10_snapshot_rejects_byte_changes(repo_root,tmp_path,path):',
         b'def test_phase3_step10_snapshot_rejects_byte_changes(repo_root,tmp_path,path,phase3_step10_snapshot):'),
        (b'shutil.copytree(repo_root/"src/recursive_integrity_toolkit",',
         b'shutil.copytree(phase3_step10_snapshot/"src/recursive_integrity_toolkit",'),
        (b'target.write_bytes((repo_root/name).read_bytes())',
         b'target.write_bytes((phase3_step10_snapshot/name).read_bytes())'),
    )
    if type(before) is not bytes or type(after) is not bytes:
        raise ValueError("Test migration requires source bytes")
    expected = before
    for old, new in replacements:
        if old not in expected:
            raise ValueError("Historical pipeline test binding missing")
        expected = expected.replace(old, new)
    if not after.startswith(expected):
        raise ValueError("Step 11 changed an unapproved inherited pipeline test")
    additions = ast.parse(after[len(expected):])
    if not additions.body or any(not isinstance(node, ast.FunctionDef)
                                or not node.name.startswith("test_phase3_step11_") for node in additions.body):
        raise ValueError("Only new Step 11 test functions may be appended")


def verify_step11_snapshot(root: Path = ROOT) -> dict:
    """Require accepted bytes after undoing exactly the two approved version edits."""
    digest = hashlib.sha256()
    paths = sorted((root / "src/recursive_integrity_toolkit").rglob("*.py"))
    for path in paths:
        raw = path.read_bytes()
        if path.relative_to(root).as_posix() == "src/recursive_integrity_toolkit/__init__.py":
            current = b'__version__ = "0.1.0.dev2"'
            if raw.count(current) != 1:
                raise ValueError("Expected the single approved root version literal")
            raw = raw.replace(current, b'__version__ = "0.1.0.dev1"', 1)
        digest.update(path.relative_to(root).as_posix().encode() + b"\0" + raw + b"\0")
    if len(paths) != 40 or digest.hexdigest() != STEP10_RUNTIME_SHA256:
        raise ValueError("Step 11 changed runtime beyond the approved version literal")
    for name, expected in STEP10_FROZEN_FILES.items():
        raw = (root / name).read_bytes()
        if name == "pyproject.toml":
            current = b'version = "0.1.0.dev2"'
            if raw.count(current) != 1:
                raise ValueError("Expected the single approved package version literal")
            raw = raw.replace(current, b'version = "0.1.0.dev1"', 1)
        if hashlib.sha256(raw).hexdigest() != expected:
            raise ValueError(f"Step 11 frozen input, dependency or oracle changed: {name}")
    return {"package_modules": 40, "approved_version_literals": 2,
            "all_other_runtime_bytes_unchanged": True, "frozen_input_files": len(STEP10_FROZEN_FILES)}


def verify_step10_snapshot(root: Path = ROOT) -> dict:
    """Require all forty accepted runtime modules and frozen inputs byte-for-byte."""
    digest = hashlib.sha256()
    paths = sorted((root / "src/recursive_integrity_toolkit").rglob("*.py"))
    for path in paths:
        digest.update(path.relative_to(root).as_posix().encode() + b"\0" + path.read_bytes() + b"\0")
    if len(paths) != 40 or digest.hexdigest() != STEP10_RUNTIME_SHA256:
        raise ValueError("Step 10 cannot change the accepted runtime implementation")
    for name, expected in STEP10_FROZEN_FILES.items():
        if hashlib.sha256((root / name).read_bytes()).hexdigest() != expected:
            raise ValueError(f"Step 10 frozen input or oracle changed: {name}")
    return {"runtime_modules_unchanged": 40, "frozen_input_files": len(STEP10_FROZEN_FILES)}


def audit(phase: int = 2, step: int = ACTIVE_STEP) -> dict:
    required = {"LICENSE", "NOTICE", "THIRD_PARTY_NOTICES.md", "THEORY_SOURCES.md"} | COMPLETION
    if phase == 3:
        required |= CUMULATIVE_NEW
    elif phase != 2:
        raise ValueError("Unsupported audit phase")
    for name in required:
        if not (ROOT / name).is_file():
            raise ValueError(f"Missing required file: {name}")
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]
    if (project["name"] != "recursive-integrity-toolkit" or project["requires-python"] != ">=3.11"
            or project["license"] != "Apache-2.0" or project["version"] != "0.1.0.dev2"
            or project["dependencies"] != ["numpy>=2.0", "pandas>=2.2"]):
        raise ValueError("Unapproved package identity, version or dependency change")
    tree = ast.parse((ROOT / "src/recursive_integrity_toolkit/__init__.py").read_text(encoding="utf-8"))
    versions = [ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == "__version__" for t in n.targets)]
    if versions != [project["version"]]:
        raise ValueError("Package version mismatch")
    entries = re.findall(r"\| `([^`]+\.md)` \| `([0-9a-f]{64})` \|", (ROOT / "PHASE_0_APPROVAL.md").read_text(encoding="utf-8"))
    if len(entries) != 16 or any(hashlib.sha256((ROOT / n).read_bytes()).hexdigest() != h for n, h in entries):
        raise ValueError("Approved Phase 0 hash mismatch")
    if "Apache License" not in (ROOT / "LICENSE").read_text(encoding="utf-8"):
        raise ValueError("License text missing")
    notices = (ROOT / "THIRD_PARTY_NOTICES.md").read_text(encoding="utf-8")
    if any(name not in notices for name in ("NumPy", "pandas", "PyArrow", "pytest", "pip-audit")):
        raise ValueError("Dependency notices incomplete")
    if len(list((ROOT / "src/recursive_integrity_toolkit").rglob("*.py"))) != 40:
        raise ValueError("Expected forty package modules")
    if any(p.is_dir() and p.name in PROHIBITED for p in ROOT.rglob("*")):
        raise ValueError("Prohibited directory")
    if phase == 3:
        control = json.loads((ROOT / "PHASE_3_BASELINE.json").read_text(encoding="utf-8"))
        verify_phase3_control(control, step)
        verify_step11_snapshot()
        if hashlib.sha256((ROOT / "PHASE_3_PLAN.md").read_bytes()).hexdigest() != PLAN_SHA256:
            raise ValueError("Approved plan bytes changed")
        if control["phase0_sha256"] != dict(entries):
            raise ValueError("Authority hashes differ from original approval")
    result = {"phase": phase, "active_step": step if phase == 3 else None, "package_modules": 40,
              "phase0_hashes_verified": 16, "license_notices": "PASS", "runtime_dependencies": "UNCHANGED",
              "phase_complete": PHASE3_COMPLETE if phase == 3 else None, "publication_authorized": False}
    print(json.dumps(result, indent=2))
    return result


def audit_step10_diff() -> dict:
    """Historical gate, restricted to its original final checkout."""
    if git("rev-parse", "HEAD").decode().strip() != PHASE2_FINAL:
        raise ValueError("Historical Phase 2 gate requires its frozen checkout; choose --phase 3")
    changes, restorations = [], []
    for line in git("diff", "--name-status", "--no-renames", STEP9_BASELINE, "HEAD").decode().splitlines():
        status, path = line.split("\t", 1)
        if path == RESTORATION_PATH:
            restorations.append(verify_approved_restoration(path, status, git("show", f"{STEP9_BASELINE}:{path}"), git("show", f"HEAD:{path}")))
        elif path not in STEP10_ALLOWED or status not in ("M", "A"):
            raise ValueError("Unapproved historical change")
        if status == "A" and path not in COMPLETION:
            raise ValueError("Unapproved historical new file")
        changes.append((status, path))
    if git("diff", "--name-only", STEP9_BASELINE, "HEAD", "--", "src", "schemas", "examples/hero", "pyproject.toml"):
        raise ValueError("Historical protected files changed")
    return {"changes": changes, "approved_exact_restorations": restorations}


def audit_phase3_diff(step: int = ACTIVE_STEP) -> dict:
    audit(3, step)
    if git("rev-parse", PHASE3_IMPLEMENTATION_ACCEPTANCE + "^{tree}").decode().strip() != PHASE3_IMPLEMENTATION_TREE:
        raise ValueError("Accepted Phase 3 implementation tree mismatch")
    subprocess.run(["git", "-C", str(ROOT), "merge-base", "--is-ancestor", PHASE3_IMPLEMENTATION_ACCEPTANCE, "HEAD"], check=True)
    if git("rev-parse", PHASE2_FINAL + "^{tree}").decode().strip() != PHASE2_TREE:
        raise ValueError("Baseline tree mismatch")
    if git("rev-parse", PHASE2_FINAL + ":tests").decode().strip() != PHASE2_TEST_TREE:
        raise ValueError("Baseline test tree mismatch")
    subprocess.run(["git", "-C", str(ROOT), "merge-base", "--is-ancestor", PHASE2_FINAL, "HEAD"], check=True)
    changes = [tuple(line.split("\t", 1)) for line in git("diff", "--name-status", "--no-renames", PHASE2_FINAL, "HEAD").decode().splitlines()]
    verify_phase3_changes(changes)
    if git("rev-parse", STEP1_FINAL + "^{tree}").decode().strip() != STEP1_TREE:
        raise ValueError("Previous accepted Step 1 tree mismatch")
    subprocess.run(["git", "-C", str(ROOT), "merge-base", "--is-ancestor", STEP1_FINAL, "HEAD"], check=True)
    if git("rev-parse", STEP2_FINAL + "^{tree}").decode().strip() != STEP2_TREE:
        raise ValueError("Previous accepted Step 2 tree mismatch")
    subprocess.run(["git", "-C", str(ROOT), "merge-base", "--is-ancestor", STEP2_FINAL, "HEAD"], check=True)
    if git("rev-parse", STEP3_FINAL + "^{tree}").decode().strip() != STEP3_TREE:
        raise ValueError("Previous accepted Step 3 tree mismatch")
    subprocess.run(["git", "-C", str(ROOT), "merge-base", "--is-ancestor", STEP3_FINAL, "HEAD"], check=True)
    if git("rev-parse", STEP4_FINAL + "^{tree}").decode().strip() != STEP4_TREE:
        raise ValueError("Previous accepted Step 4 tree mismatch")
    subprocess.run(["git", "-C", str(ROOT), "merge-base", "--is-ancestor", STEP4_FINAL, "HEAD"], check=True)
    if git("rev-parse", STEP5_FINAL + "^{tree}").decode().strip() != STEP5_TREE:
        raise ValueError("Previous accepted Step 5 tree mismatch")
    subprocess.run(["git", "-C", str(ROOT), "merge-base", "--is-ancestor", STEP5_FINAL, "HEAD"], check=True)
    if git("rev-parse", STEP6_FINAL + "^{tree}").decode().strip() != STEP6_TREE:
        raise ValueError("Previous accepted Step 6 tree mismatch")
    subprocess.run(["git", "-C", str(ROOT), "merge-base", "--is-ancestor", STEP6_FINAL, "HEAD"], check=True)
    if git("rev-parse", STEP7_FINAL + "^{tree}").decode().strip() != STEP7_TREE:
        raise ValueError("Previous accepted Step 7 tree mismatch")
    subprocess.run(["git", "-C", str(ROOT), "merge-base", "--is-ancestor", STEP7_FINAL, "HEAD"], check=True)
    if git("rev-parse", STEP8_FINAL + "^{tree}").decode().strip() != STEP8_TREE:
        raise ValueError("Previous accepted Step 8 tree mismatch")
    subprocess.run(["git", "-C", str(ROOT), "merge-base", "--is-ancestor", STEP8_FINAL, "HEAD"], check=True)
    if git("rev-parse", STEP9_FINAL + "^{tree}").decode().strip() != STEP9_TREE:
        raise ValueError("Accepted Step 9 tree mismatch")
    subprocess.run(["git", "-C", str(ROOT), "merge-base", "--is-ancestor", STEP9_FINAL, "HEAD"], check=True)
    if git("diff", "--name-only", STEP9_FINAL, STEP10_FINAL, "--", "src", "schemas", "examples/hero", "pyproject.toml"):
        raise ValueError("Step 10 changed a protected implementation or input")
    if git("rev-parse", STEP10_FINAL + "^{tree}").decode().strip() != STEP10_TREE:
        raise ValueError("Accepted Step 10 tree mismatch")
    subprocess.run(["git", "-C", str(ROOT), "merge-base", "--is-ancestor", STEP10_FINAL, "HEAD"], check=True)
    historical = [tuple(line.split("\t", 1)) for line in
                  git("diff", "--name-status", "--no-renames", STEP9_FINAL, STEP10_FINAL).decode().splitlines()]
    verify_prior_step_changes(historical, step=10)
    verify_step11_contract_test_migration(git("show", f"{STEP10_FINAL}:tests/unit/test_phase3_contracts.py"),
                                          (ROOT / "tests/unit/test_phase3_contracts.py").read_bytes())
    verify_step11_pipeline_test_migration(git("show", f"{STEP10_FINAL}:tests/integration/test_phase3_metric_pipeline.py"),
                                          (ROOT / "tests/integration/test_phase3_metric_pipeline.py").read_bytes())
    # Step 9 may add pair functions but cannot alter any preexisting single-scope formula.
    diversity_path = "src/recursive_integrity_toolkit/metrics/diversity.py"
    before = ast.parse(git("show", f"{STEP8_FINAL}:{diversity_path}"))
    current = ast.parse((ROOT / diversity_path).read_bytes())
    definitions = {n.name: ast.dump(n, include_attributes=False) for n in current.body
                   if isinstance(n, (ast.ClassDef, ast.FunctionDef))}
    for node in before.body:
        if isinstance(node, (ast.ClassDef, ast.FunctionDef)) and definitions.get(node.name) != ast.dump(node, include_attributes=False):
            raise ValueError("Step 9 altered an inherited single-scope calculation")
    incremental = [tuple(line.split("\t", 1)) for line in
                   git("diff", "--name-status", "--no-renames", STEP10_FINAL, "HEAD").decode().splitlines()]
    verify_phase3_changes(incremental, incremental=True)
    verify_step2_contract_test_migration(git("show", f"{STEP1_FINAL}:{STEP2_EXCEPTION}"),
                                         git("show", f"{STEP2_FINAL}:{STEP2_EXCEPTION}"))
    if git("diff", "--name-only", "HEAD", "--"):
        raise ValueError("Tracked checkout differs from tested commit")
    for path in ("src/recursive_integrity_toolkit/models.py", "src/recursive_integrity_toolkit/errors.py"):
        before, current = ast.parse(git("show", f"{PHASE2_FINAL}:{path}")), ast.parse((ROOT / path).read_bytes())
        definitions = {n.name: ast.dump(n, include_attributes=False) for n in current.body if isinstance(n, (ast.ClassDef, ast.FunctionDef))}
        for node in before.body:
            if isinstance(node, (ast.ClassDef, ast.FunctionDef)) and definitions.get(node.name) != ast.dump(node, include_attributes=False):
                raise ValueError(f"Inherited contract changed: {path}:{node.name}")
    result = {"baseline": PHASE2_FINAL, "head": git("rev-parse", "HEAD").decode().strip(),
              "changes": changes, "incremental_changes": incremental, "previous_step": STEP10_FINAL,
              "old_runtime_definitions": "UNCHANGED", "active_step": step}
    print(json.dumps(result, indent=2))
    return result


def verify_junit(path: Path, *, require_parquet: bool = False, minimum: int = 1) -> dict:
    root = ET.parse(path).getroot()
    cases = list(root.iter("testcase"))
    identities = [(c.get("classname", ""), c.get("name", "")) for c in cases]
    if len(cases) < minimum or len(identities) != len(set(identities)):
        raise ValueError("Insufficient or duplicate test cases")
    if any(child.tag in ("failure", "error", "skipped") for c in cases for child in c):
        raise ValueError("Failed, errored or skipped test")
    if any(int(s.get(k, "0")) for s in root.iter("testsuite") for k in ("failures", "errors", "skipped")):
        raise ValueError("Failed, errored or skipped test suite")
    actual = PARQUET_CASES & {c.get("name", "") for c in cases}
    if require_parquet and actual != PARQUET_CASES:
        raise ValueError("Real PyArrow cases were not all collected")
    result = {"tests": len(cases), "passed": len(cases), "failed": 0, "skipped": 0, "real_parquet_cases": len(actual)}
    print(json.dumps(result, indent=2))
    return result


def _collect(root: Path) -> tuple[list[str], str]:
    env = dict(os.environ, PYTHONPATH=str(root / "src"), PYTHONDONTWRITEBYTECODE="1")
    result = subprocess.run([sys.executable, "-m", "pytest", "-p", "no:cacheprovider", "--collect-only", "-q"],
                            cwd=root, env=env, capture_output=True, text=True, encoding="utf-8", check=True)
    nodes = sorted(line.strip() for line in result.stdout.splitlines() if line.startswith("tests/") and "::" in line)
    if len(nodes) != len(set(nodes)):
        raise ValueError("Duplicate test node identity")
    return nodes, result.stdout


def baseline_evidence(output: Path) -> dict:
    output.mkdir(parents=True, exist_ok=True)
    files = {}
    with tempfile.TemporaryDirectory(prefix="rit-p3-baseline-") as temp:
        root = Path(temp)
        for entry in git("ls-tree", "-rz", PHASE2_FINAL).split(b"\0"):
            if not entry:
                continue
            info, path_bytes = entry.split(b"\t", 1)
            mode, kind, blob = info.decode().split()
            if kind != "blob":
                raise ValueError("Unexpected baseline object kind")
            path = path_bytes.decode(); raw = git("show", f"{PHASE2_FINAL}:{path}")
            target = root / path; target.parent.mkdir(parents=True, exist_ok=True); target.write_bytes(raw)
            files[path] = {"mode": mode, "git_blob": blob, "sha256": hashlib.sha256(raw).hexdigest()}
        old, old_log = _collect(root)
    new, new_log = _collect(ROOT)
    import io
    with tempfile.TemporaryDirectory(prefix="rit-p3-step1-tests-") as temp:
        prior_root = Path(temp)
        with zipfile.ZipFile(io.BytesIO(git("archive", "--format=zip", STEP1_FINAL))) as archive:
            archive.extractall(prior_root)
        prior, prior_log = _collect(prior_root)
    expected_prior = 1273 if os.environ.get("RIT_TEST_PARQUET") == "1" else 1270
    if len(prior) != expected_prior or set(prior) - set(new):
        raise ValueError("Accepted Step 1 test identities were lost")
    (output / "step1-collection.log").write_text(prior_log, encoding="utf-8")
    with tempfile.TemporaryDirectory(prefix="rit-p3-step2-tests-") as temp:
        prior2_root = Path(temp)
        with zipfile.ZipFile(io.BytesIO(git("archive", "--format=zip", STEP2_FINAL))) as archive:
            archive.extractall(prior2_root)
        prior2, prior2_log = _collect(prior2_root)
    expected_prior2 = 1432 if os.environ.get("RIT_TEST_PARQUET") == "1" else 1429
    if len(prior2) != expected_prior2 or set(prior2) - set(new):
        raise ValueError("Accepted Step 2 test identities were lost")
    (output / "step2-collection.log").write_text(prior2_log, encoding="utf-8")
    with tempfile.TemporaryDirectory(prefix="rit-p3-step3-tests-") as temp:
        prior3_root = Path(temp)
        with zipfile.ZipFile(io.BytesIO(git("archive", "--format=zip", STEP3_FINAL))) as archive:
            archive.extractall(prior3_root)
        prior3, prior3_log = _collect(prior3_root)
    expected_prior3 = 1578 if os.environ.get("RIT_TEST_PARQUET") == "1" else 1575
    if len(prior3) != expected_prior3 or set(prior3) - set(new):
        raise ValueError("Accepted Step 3 test identities were lost")
    (output / "step3-collection.log").write_text(prior3_log, encoding="utf-8")
    with tempfile.TemporaryDirectory(prefix="rit-p3-step4-tests-") as temp:
        prior4_root = Path(temp)
        with zipfile.ZipFile(io.BytesIO(git("archive", "--format=zip", STEP4_FINAL))) as archive:
            archive.extractall(prior4_root)
        prior4, prior4_log = _collect(prior4_root)
    expected_prior4 = 1717 if os.environ.get("RIT_TEST_PARQUET") == "1" else 1714
    if len(prior4) != expected_prior4 or set(prior4) - set(new):
        raise ValueError("Accepted Step 4 test identities were lost")
    (output / "step4-collection.log").write_text(prior4_log, encoding="utf-8")
    with tempfile.TemporaryDirectory(prefix="rit-p3-step5-tests-") as temp:
        prior5_root = Path(temp)
        with zipfile.ZipFile(io.BytesIO(git("archive", "--format=zip", STEP5_FINAL))) as archive:
            archive.extractall(prior5_root)
        prior5, prior5_log = _collect(prior5_root)
    expected_prior5 = 1891 if os.environ.get("RIT_TEST_PARQUET") == "1" else 1888
    if len(prior5) != expected_prior5 or set(prior5) - set(new):
        raise ValueError("Accepted Step 5 test identities were lost")
    (output / "step5-collection.log").write_text(prior5_log, encoding="utf-8")
    with tempfile.TemporaryDirectory(prefix="rit-p3-step6-tests-") as temp:
        prior6_root = Path(temp)
        with zipfile.ZipFile(io.BytesIO(git("archive", "--format=zip", STEP6_FINAL))) as archive:
            archive.extractall(prior6_root)
        prior6, prior6_log = _collect(prior6_root)
    expected_prior6 = 1990 if os.environ.get("RIT_TEST_PARQUET") == "1" else 1987
    if len(prior6) != expected_prior6 or set(prior6) - set(new):
        raise ValueError("Accepted Step 6 test identities were lost")
    (output / "step6-collection.log").write_text(prior6_log, encoding="utf-8")
    with tempfile.TemporaryDirectory(prefix="rit-p3-step7-tests-") as temp:
        prior7_root = Path(temp)
        with zipfile.ZipFile(io.BytesIO(git("archive", "--format=zip", STEP7_FINAL))) as archive:
            archive.extractall(prior7_root)
        prior7, prior7_log = _collect(prior7_root)
    expected_prior7 = 2120 if os.environ.get("RIT_TEST_PARQUET") == "1" else 2117
    if len(prior7) != expected_prior7 or set(prior7) - set(new):
        raise ValueError("Accepted Step 7 test identities were lost")
    (output / "step7-collection.log").write_text(prior7_log, encoding="utf-8")
    with tempfile.TemporaryDirectory(prefix="rit-p3-step8-tests-") as temp:
        prior8_root = Path(temp)
        with zipfile.ZipFile(io.BytesIO(git("archive", "--format=zip", STEP8_FINAL))) as archive:
            archive.extractall(prior8_root)
        prior8, prior8_log = _collect(prior8_root)
    expected_prior8 = 2271 if os.environ.get("RIT_TEST_PARQUET") == "1" else 2268
    if len(prior8) != expected_prior8 or set(prior8) - set(new):
        raise ValueError("Accepted Step 8 test identities were lost")
    (output / "step8-collection.log").write_text(prior8_log, encoding="utf-8")
    with tempfile.TemporaryDirectory(prefix="rit-p3-step9-tests-") as temp:
        prior9_root = Path(temp)
        with zipfile.ZipFile(io.BytesIO(git("archive", "--format=zip", STEP9_FINAL))) as archive:
            archive.extractall(prior9_root)
        prior9, prior9_log = _collect(prior9_root)
    expected_prior9 = 2407 if os.environ.get("RIT_TEST_PARQUET") == "1" else 2404
    if len(prior9) != expected_prior9 or set(prior9) - set(new):
        raise ValueError("Accepted Step 9 test identities were lost")
    (output / "step9-collection.log").write_text(prior9_log, encoding="utf-8")
    with tempfile.TemporaryDirectory(prefix="rit-p3-step10-tests-") as temp:
        prior10_root = Path(temp)
        with zipfile.ZipFile(io.BytesIO(git("archive", "--format=zip", STEP10_FINAL))) as archive:
            archive.extractall(prior10_root)
        prior10, prior10_log = _collect(prior10_root)
    expected_prior10 = 2475 if os.environ.get("RIT_TEST_PARQUET") == "1" else 2472
    if len(prior10) != expected_prior10 or set(prior10) - set(new):
        raise ValueError("Accepted Step 10 test identities were lost")
    (output / "step10-collection.log").write_text(prior10_log, encoding="utf-8")
    expected = 1162 if os.environ.get("RIT_TEST_PARQUET") == "1" else 1159
    if len(files) != 197 or len(old) != expected or set(old) - set(new):
        raise ValueError(f"Frozen file/test identities do not reconcile: {len(files)} files, {len(old)} baseline tests, {len(set(old)-set(new))} missing")
    payload = {"baseline_commit": PHASE2_FINAL, "files": files, "baseline_nodeids": old, "current_nodeids": new,
               "previous_step_commit": STEP10_FINAL, "previous_step_nodeids": prior10,
               "step9_commit": STEP9_FINAL, "step9_nodeids": prior9,
               "step8_commit": STEP8_FINAL, "step8_nodeids": prior8,
               "step7_commit": STEP7_FINAL, "step7_nodeids": prior7,
               "step6_commit": STEP6_FINAL, "step6_nodeids": prior6,
               "step5_commit": STEP5_FINAL, "step5_nodeids": prior5,
               "step4_commit": STEP4_FINAL, "step4_nodeids": prior4,
               "step3_commit": STEP3_FINAL, "step3_nodeids": prior3,
               "step2_commit": STEP2_FINAL, "step2_nodeids": prior2,
               "step1_commit": STEP1_FINAL, "step1_nodeids": prior,
               "missing_nodeids": [], "nodeids_sha256": hashlib.sha256(("\n".join(old)+"\n").encode()).hexdigest()}
    (output / "baseline-identities.json").write_text(json.dumps(payload, indent=2)+"\n", encoding="utf-8")
    (output / "baseline-collection.log").write_text(old_log, encoding="utf-8")
    (output / "current-collection.log").write_text(new_log, encoding="utf-8")
    summary = {"baseline_files": len(files), "inherited_tests": len(old), "current_tests": len(new), "missing_tests": 0, "previous_step_tests": len(prior10), "step9_tests": len(prior9), "step8_tests": len(prior8), "step7_tests": len(prior7), "step6_tests": len(prior6), "step5_tests": len(prior5), "step4_tests": len(prior4), "step3_tests": len(prior3), "step2_tests": len(prior2), "step1_tests": len(prior),
               "nodeids_sha256": payload["nodeids_sha256"]}
    print(json.dumps(summary, indent=2))
    return summary


def verify_distributions(directory: Path, expected_version: str = "0.1.0.dev2") -> tuple[Path, Path]:
    wheels, sdists = list(directory.glob("*.whl")), list(directory.glob("*.tar.gz"))
    if len(wheels) != 1 or len(sdists) != 1:
        raise ValueError("Require one wheel and one sdist")
    expected = {p.relative_to(ROOT / "src").as_posix(): p.read_bytes() for p in (ROOT / "src/recursive_integrity_toolkit").rglob("*.py")}
    with zipfile.ZipFile(wheels[0]) as wheel:
        for path, raw in expected.items():
            if wheel.read(path) != raw:
                raise ValueError(f"Wheel code mismatch: {path}")
        names = wheel.namelist()
        if {n for n in names if n.endswith(".py")} != set(expected):
            raise ValueError("Wheel module set differs from the forty source modules")
        metadata = [n for n in names if n.endswith(".dist-info/METADATA")]
        if len(metadata) != 1 or f"Version: {expected_version}\n" not in wheel.read(metadata[0]).decode():
            raise ValueError("Wheel metadata mismatch")
        for notice in ("LICENSE", "NOTICE"):
            if not any(n.endswith("/"+notice) for n in names):
                raise ValueError(f"Wheel lacks {notice}")
    with tarfile.open(sdists[0], "r:gz") as archive:
        members = {m.name: m for m in archive.getmembers()}
        roots = {n.split("/", 1)[0] for n in members}
        if len(roots) != 1:
            raise ValueError("Source archive requires one root")
        prefix = next(iter(roots))
        if {n.removeprefix(prefix + "/src/") for n in members
                if n.startswith(prefix + "/src/recursive_integrity_toolkit/") and n.endswith(".py")} != set(expected):
            raise ValueError("Sdist module set differs from the forty source modules")
        for notice in ("LICENSE", "NOTICE"):
            if f"{prefix}/{notice}" not in members:
                raise ValueError(f"Sdist lacks {notice}")
        for path, raw in expected.items():
            stream = archive.extractfile(members[f"{prefix}/src/{path}"])
            if stream is None or stream.read() != raw:
                raise ValueError(f"Sdist code mismatch: {path}")
    print("wheel/sdist: 40 packaged modules match source")
    return wheels[0], sdists[0]


def smoke_installed(wheel: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="rit-p3-installed-") as temp:
        work = Path(temp)
        subprocess.run([sys.executable, "-m", "venv", str(work / "venv")], check=True)
        bindir = work / "venv" / ("Scripts" if os.name == "nt" else "bin")
        python = bindir / ("python.exe" if os.name == "nt" else "python")
        subprocess.run([str(python), "-m", "pip", "install", "--no-index", "--no-deps", str(wheel.resolve())], cwd=work, check=True)
        program = '''import hashlib, importlib, importlib.abc, importlib.metadata, pkgutil, socket, sys
from pathlib import Path
class DenyOptional(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in {'numpy','pandas','pyarrow'}:
            raise ModuleNotFoundError('blocked numerical/optional import')
sys.meta_path.insert(0,DenyOptional())
def blocked(*args, **kwargs):
    raise AssertionError('network call')
socket.create_connection=blocked
socket.getaddrinfo=blocked
socket.socket.connect=blocked
import recursive_integrity_toolkit as package
assert not Path(package.__file__).resolve().is_relative_to(Path(sys.argv[1])/'src')
assert package.__version__==importlib.metadata.version('recursive-integrity-toolkit')
names=[package.__name__]+[m.name for m in pkgutil.walk_packages(package.__path__,package.__name__+'.')]
assert len(names)==40
for name in names: importlib.import_module(name)
from recursive_integrity_toolkit.models import AuditBundle,InputSource,FileRole,CapabilityKey,CapabilityStatus,NumericalPolicy
from recursive_integrity_toolkit.io.validation import validate_bundle
assert NumericalPolicy().absolute_tolerance==1e-12
from recursive_integrity_toolkit.io.normalization import normalize_row
from recursive_integrity_toolkit.config import RepresentationConfig
from recursive_integrity_toolkit.representations.field import assign_field_states
row=normalize_row({"dataset_version":"v1","record_id":"literal","content":"synthetic","topic":""},kind="records")
field_result=assign_field_states((row,),dataset_versions=("v1",),scope_id="installed-field-check",
    config=RepresentationConfig("topic","topic_field","topic","smoke-v1","exclude"))
assert field_result.included_count==1 and field_result.assignments[0].state_id==""
hero=Path(sys.argv[1])/'examples'/'hero'
files=('records_v1.csv','records_v2.csv','provenance.csv','config.json','version_order.json','EXPECTED_OUTPUTS.md')
before={n:hashlib.sha256((hero/n).read_bytes()).hexdigest() for n in files}
roles=(FileRole.RECORDS_PRIMARY,FileRole.RECORDS_COMPARE,FileRole.PROVENANCE_MANIFEST,FileRole.CONFIG,FileRole.VERSION_ORDER)
result=validate_bundle(AuditBundle(tuple(InputSource(r,hero/n) for r,n in zip(roles,files))))
assert result.observability.maximum_level==4 and not result.has_errors
assert result.observability.capabilities[CapabilityKey.MODEL_LONGITUDINAL].status is CapabilityStatus.UNAVAILABLE
assert before=={n:hashlib.sha256((hero/n).read_bytes()).hexdigest() for n in files}
assert not {'numpy','pandas','pyarrow'} & set(sys.modules)
print('installed: 40 imports, Step 2 field assignment, input-only Hero Level 4, no dependencies/network: PASS')
'''
        subprocess.run([str(python), "-I", "-c", program, str(ROOT)], cwd=work, check=True)
        for arg in ("--help", "version"):
            subprocess.run([str(python), "-I", "-m", "recursive_integrity_toolkit", arg], cwd=work, check=True)
        for name, arg in (("rit", "version"), ("recursive-integrity", "--help")):
            subprocess.run([str(bindir / (name+".exe" if os.name == "nt" else name)), arg], cwd=work, check=True)



def smoke_installed_duplicates(wheel: Path) -> None:
    """A separate installed calculation check with approved dependencies present."""
    with tempfile.TemporaryDirectory(prefix="rit-p3-installed-duplicates-") as temp:
        work = Path(temp)
        subprocess.run([sys.executable, "-m", "venv", "--system-site-packages", str(work / "venv")], check=True)
        bindir = work / "venv" / ("Scripts" if os.name == "nt" else "bin")
        python = bindir / ("python.exe" if os.name == "nt" else "python")
        subprocess.run([str(python), "-m", "pip", "install", "--no-index", "--no-deps", "--force-reinstall",
                        str(wheel.resolve())], cwd=work, check=True)
        program = """import builtins, socket, sys
from pathlib import Path
import numpy, pandas
import recursive_integrity_toolkit as package
assert Path(package.__file__).resolve().is_relative_to(Path(sys.argv[1]) / 'venv')
from recursive_integrity_toolkit.io.normalization import normalize_row
from recursive_integrity_toolkit.models import ContentMode, CalculationEvidenceClass
from recursive_integrity_toolkit.metrics.duplicates import detect_exact_duplicates
from recursive_integrity_toolkit.metrics.diversity import calculate_state_distribution
from recursive_integrity_toolkit.metrics.provenance import summarize_provenance
from recursive_integrity_toolkit.metrics.bounds import direct_closure_exposure
from recursive_integrity_toolkit.io.validation import assess_provenance_row, join_provenance
from recursive_integrity_toolkit.models import CalculationScope
from recursive_integrity_toolkit.representations.content_hash import assign_content_states
from recursive_integrity_toolkit.models import WeightingOptions
rows=tuple(normalize_row({'dataset_version':'v1','record_id':str(i),'content':text},kind='records')
           for i,text in enumerate(('same','same','different')))
def blocked(*args, **kwargs):
    raise AssertionError('unexpected file or network access during installed calculation')
builtins.open=blocked
socket.create_connection=blocked
socket.getaddrinfo=blocked
socket.socket.connect=blocked
result=detect_exact_duplicates(rows,dataset_versions=('v1',),scope_id='installed-duplicates',
    representation_name='record_form',representation_version='v1',normalization_profile='exact_utf8_v1',
    content_mode=ContentMode.INLINE)
assert result.duplicate_record_count.value==1 and result.duplicate_group_count.value==1
assert result.evidence_class is CalculationEvidenceClass.OBSERVED_FACT
assert len(rows)==3
exact=assign_content_states(rows,dataset_versions=('v1',),scope_id='installed-distribution',
    representation_name='record_form',representation_version='v1',normalization_profile='exact_utf8_v1',
    content_mode=ContentMode.INLINE)
metrics=calculate_state_distribution(exact.representation,weighting=WeightingOptions('weighted','weight'),
    weights={row.record_key: weight for row,weight in zip(rows,(1,1,2))})
assert metrics.unweighted.support_size.value==2
assert abs(metrics.unweighted.gini_simpson_diversity.value - 4/9)<1e-12
assert metrics.weighted.gini_simpson_diversity.value==0.5
assert metrics.unweighted.analyzed_record_count==3
prov=tuple(assess_provenance_row({'dataset_version':'v1','record_id':str(i),'source_type':kind,
    'provenance_confidence':'confirmed','external_grounding':grounding})
    for i,(kind,grounding) in enumerate((('human','no'),('synthetic','yes'))))
joined=join_provenance(rows,prov)
scope=CalculationScope(('v1',),joined.scope_record_keys,(),joined.provenance_row_coverage.denominator_name,'installed-provenance')
composition=summarize_provenance(joined,scope=scope,weighting=WeightingOptions('weighted','weight'),
    weights={row.record_key: weight for row,weight in zip(rows,(1,2,3))})
assert dict(composition.source.counts)=={'human':1,'synthetic':1,'mixed':0,'sensor':0,'unknown':0}
assert composition.missing_provenance_share.value==1/3
assert composition.direct_grounding.known_open_count.value==1
assert composition.direct_grounding.known_closed_count.value==1
assert composition.direct_grounding.unresolved_grounding_count.value==1
assert composition.weighted_source.weighted_missing_provenance_share.value==0.5
assert not composition.input_has_errors and len(rows)==3
bounds=direct_closure_exposure(composition)
assert (bounds.lower_bound.value,bounds.upper_bound.value,bounds.interval_width.value)==(1/3,2/3,1/3)
assert bounds.classification_basis=='toolkit_operationalization' and bounds.confidence_counts==composition.confidence.counts
print('installed prior metrics and Step 6 direct bounds with NumPy/pandas present; no I/O/network: PASS')

from recursive_integrity_toolkit.metrics.tail import select_tail, one_step_extinction_probability
from recursive_integrity_toolkit.metrics.diversity import distribution_from_counts
from recursive_integrity_toolkit.models import TailSelectionOptions
frequency = metrics.unweighted
tail = select_tail(frequency,options=TailSelectionOptions('singleton_count'))
assert tail.tail_support_size.value==1 and tail.tail_record_share.value==1/3
scenario = one_step_extinction_probability(.25,resample_size=4,state_id=tail.tail_membership[0],scope=frequency.scope,representation=frequency.representation)
assert abs(scenario.one_step_extinction_probability.value - 81/256) < 1e-12
assert scenario.evidence_class is CalculationEvidenceClass.SIMULATION and scenario.simulation_horizon==1
assert scenario.random_seed is None
print('installed Step 7 tail/rank and F-014: PASS; no random sampling or automatic invocation')
from recursive_integrity_toolkit.metrics.resampling import expected_diversity_after_steps, simulate_closed_resampling
parameters=dict(resample_size=4,steps=2,scope=frequency.scope,representation=frequency.representation)
dist={'a':.5,'b':.25,'c':.25,'zero':0.}
expectation=expected_diversity_after_steps(dist,**parameters)
assert abs(expectation.expected_diversity[-1] - 45/128)<1e-12
simulation=simulate_closed_resampling(dist,seed=17,replicates=3,**parameters)
assert simulation==simulate_closed_resampling(dist,seed=17,replicates=3,**parameters)
assert simulation.evidence_class is CalculationEvidenceClass.SIMULATION
for path in simulation.sampled_paths:
    for generation in path.generations[1:]:
        assert sum(generation.state_counts)==4 and generation.state_counts[-1]==0
assert expectation.random_seed is None and simulation.numpy_version==numpy.__version__
print('installed Step 8 F-015 and seeded closed paths: PASS; zero absorption, replay, no I/O/network')
from recursive_integrity_toolkit.metrics.diversity import compare_support, distribution_from_counts
from recursive_integrity_toolkit.models import ExplicitPairContext, CalculationScope, RecordKey, RepresentationDescriptor
from recursive_integrity_toolkit.io.validation import resolve_version_order
pair_rep=RepresentationDescriptor('topic','topic_field','installed-taxonomy-v1','literal_field_value',field_name='topic',missing_value_policy='exclude')
earlier_scope=CalculationScope(('v1',),tuple(RecordKey('v1',str(i)) for i in range(4)),(),'included_representation_records','installed-earlier')
later_scope=CalculationScope(('v2',),tuple(RecordKey('v2',str(i)) for i in range(4)),(),'included_representation_records','installed-later')
earlier=distribution_from_counts({'a':2,'b':1,'c':1},scope=earlier_scope,representation=pair_rep)
later=distribution_from_counts({'a':3,'z':1},scope=later_scope,representation=pair_rep)
order=resolve_version_order(('v1','v2'),invocation_order=('v1','v2'))
context=ExplicitPairContext(earlier.scope,later.scope,pair_rep,pair_rep,order)
comparison=compare_support(earlier,later,context=context,earlier_state_semantics='installed-taxonomy',later_state_semantics='installed-taxonomy')
assert comparison.support_delta.value==-1 and comparison.support_retention_ratio.value==1/3
assert comparison.extinct_states==('b','c') and comparison.added_states==('z',)
assert comparison.gini_simpson_diversity_delta.value==-1/4
print('installed Step 9 explicit pair: PASS; support delta, loss/addition, retention, diversity delta, no I/O/network')

"""
        subprocess.run([str(python), "-I", "-c", program, str(work)], cwd=work, check=True)


def verify_step10_evidence(junit: Path, output: Path | None = None) -> dict:
    """Require twenty executed frozen cases and seven measured operation records.

    These are test-run observations, not a public analytical report or speed SLA.
    General JUnit validation rejects failures and skips before evidence extraction.
    """
    from math import isfinite
    verify_junit(junit)
    root = ET.parse(junit).getroot()
    cases = list(root.iter("testcase"))
    expected_ids = {"test_phase3_frozen_case[" + case["case_id"] + "]"
                    for case in json.loads((ROOT / "tests/golden/phase3_math_cases.json").read_bytes())["cases"]}
    actual = {case.get("name") for case in cases if case.get("classname", "").endswith("test_phase3_math")}
    if len(expected_ids) != 20 or not expected_ids <= actual:
        raise ValueError("All twenty frozen mathematical cases must actually execute")
    required = {"hero_input_plus_calculations", "metadata_100k_setup", "metadata_100k_field_representation",
                "metadata_100k_support_diversity", "metadata_100k_provenance_join",
                "metadata_100k_composition", "metadata_100k_exact_duplicates"}
    observations = []
    seen = set()
    for case in cases:
        for prop in case.findall("./properties/property"):
            if prop.get("name") != "phase3_performance":
                continue
            data = json.loads(prop.get("value", ""))
            name = data.get("name")
            if name not in required or name in seen:
                raise ValueError("Missing, duplicated or unexpected performance observation")
            for key in ("elapsed_seconds", "traced_current_bytes", "traced_peak_bytes"):
                value = data.get(key)
                if type(value) not in (int, float) or not isfinite(value) or value < 0:
                    raise ValueError("Performance evidence requires finite nonnegative measurements")
            if data["traced_peak_bytes"] < data["traced_current_bytes"]:
                raise ValueError("Invalid traced-memory evidence")
            if data.get("whole_product_report_target_certified") is not False:
                raise ValueError("A calculation observation cannot certify the final report target")
            if data.get("record_count") != (16 if name == "hero_input_plus_calculations" else 100000):
                raise ValueError("Performance evidence used an incorrect dataset size")
            for key in ("memory_method", "timing_method", "python", "platform"):
                if type(data.get(key)) is not str or not data[key]:
                    raise ValueError("Performance environment and measurement methods must be disclosed")
            seen.add(name)
            observations.append(data)
    if seen != required:
        raise ValueError("Required Step 10 performance measurements were not all executed")
    result = {"frozen_cases_executed": 20, "performance_observations": sorted(observations, key=lambda d: d["name"]),
              "whole_product_report_target_certified": False}
    if output is not None:
        output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result


def candidate(output: Path, step: int = ACTIVE_STEP) -> None:
    result = {"audit": audit_phase3_diff(step), "phase_complete": PHASE3_COMPLETE,
              "acceptance_requires_all_four_workflow_roles": True, "next_step_authorized": False}
    output.mkdir(parents=True, exist_ok=True)
    result["core"] = verify_junit(output / "core.xml", minimum=2472)
    result["parquet"] = verify_junit(output / "parquet.xml", require_parquet=True, minimum=2475)
    result["core_integration"] = verify_step10_evidence(output / "core.xml", output / "phase3-core-observations.json")
    result["parquet_integration"] = verify_step10_evidence(output / "parquet.xml", output / "phase3-parquet-observations.json")
    result["identities"] = baseline_evidence(output)
    verify_distributions(output / "dist")
    archive = output / "recursive-integrity-toolkit-phase3.zip"
    subprocess.run(["git", "-C", str(ROOT), "archive", "--format=zip", "--prefix=recursive-integrity-toolkit/", "HEAD", "-o", str(archive.resolve())], check=True)
    tracked = {n for n in git("ls-files", "-z").decode().split("\0") if n}
    with zipfile.ZipFile(archive) as zipped:
        actual = {n.removeprefix("recursive-integrity-toolkit/") for n in zipped.namelist() if not n.endswith("/")}
        if actual != tracked:
            raise ValueError("Candidate archive file set mismatch")
        for path in actual:
            if any(p in {".git", "__pycache__", ".pytest_cache", ".venv", "venv", "build", "dist"} for p in Path(path).parts) or path.endswith((".pyc", ".pyo")):
                raise ValueError("Generated file in source archive")
            if zipped.read("recursive-integrity-toolkit/"+path) != (ROOT / path).read_bytes():
                raise ValueError("Candidate archive byte mismatch")
    (output / "phase3_repository_files.sha256").write_text(
        "".join(f"{hashlib.sha256((ROOT / name).read_bytes()).hexdigest()}  {name}\n" for name in sorted(tracked)), encoding="utf-8")
    result["source_archive"] = archive.name
    result["tracked_files"] = len(tracked)
    result["python"] = sys.version; result["platform"] = sys.platform; result["versions"] = {}
    for name in ("numpy", "pandas", "pyarrow", "pytest", "build", "setuptools", "twine"):
        try:
            result["versions"][name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            result["versions"][name] = None
    (output / "phase3_execution_metadata.json").write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    files = sorted(p for p in output.rglob("*") if p.is_file() and p.name != "phase3_artifacts.sha256")
    (output / "phase3_artifacts.sha256").write_text("".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(output).as_posix()}\n" for p in files), encoding="utf-8")
    print(f"Step 11 source artifact: {len(tracked)} tracked files verified. Final acceptance also requires all workflow roles on this commit.")


# Phase 4 gates are additive. Historical Phase 2/3 functions and constants above
# keep their original contracts; the active Phase 4 dispatcher is separate.
from functools import lru_cache
import io
import importlib.util
from types import MappingProxyType

PHASE4_FINAL = "e3ffb8c0a88bfe31f669f9662d9b5213da628b3a"
PHASE4_TREE = "e2a25f8cfdc66c3317809c479f80fdae162e6ba9"
PHASE4_TEST_TREE = "6ab22cb9197a8f094f455b29a07a851062bb26c9"
PHASE4_PLAN_SHA256 = "5a6d65696720a426630e876d001937b2837d24774fcb6c2bd43b8e09f5ae93f0"
PHASE4_STEP1_NEW = {
    "PHASE_4_PLAN.md", "PHASE_4_BASELINE.json", "PHASE_4_DECISIONS.md",
    "tests/unit/test_phase4_contracts.py", "tests/integration/test_phase4_gates.py",
}
PHASE4_G = {
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
}
PHASE4_MIGRATION_PATHS = {
    "tests/unit/test_PR012_evidence_classes.py", "tests/unit/test_PR013_report_schema.py",
    "tests/unit/test_PR014_unavailable.py", "tests/unit/test_PR015_redaction.py",
    "tests/unit/test_PR016_determinism.py", "tests/unit/test_PR018_language.py",
    "tests/integration/test_no_algorithms.py", "tests/integration/test_phase3_metric_pipeline.py",
    "tests/integration/test_cli_validation.py", "tests/integration/test_ci_workflows.py",
}
PHASE4_STEP1_ALLOWED = PHASE4_G | PHASE4_STEP1_NEW | PHASE4_MIGRATION_PATHS
PHASE4_FORBIDDEN_OUTPUTS = {
    "PHASE_4_COMPLETION.md", "PHASE_4_VALIDATION_REPORT.md",
    "PHASE_4_ARCHITECTURE_COMPLIANCE_REPORT.md", "report.json", "report.md",
}
PHASE4_APPROVAL = "批准，开始 **Phase 4 Step 1**"
PHASE4_MIGRATIONS = {'tests/integration/test_ci_workflows.py': [{'new': 'def '
                                                    'test_workflows_preserve_phase_boundary(repo_root: '
                                                    'Path,phase3_final_snapshot) -> None:\n'
                                                    '    repo_root = phase3_final_snapshot\n',
                                             'node': 'test_workflows_preserve_phase_boundary',
                                             'old': 'def '
                                                    'test_workflows_preserve_phase_boundary(repo_root: '
                                                    'Path) -> None:\n'},
                                            {'new': 'def '
                                                    'test_phase2_delivery_builds_both_formats_and_tests_installed_wheel(repo_root,phase3_final_snapshot):\n'
                                                    '    repo_root = phase3_final_snapshot\n',
                                             'node': 'test_phase2_delivery_builds_both_formats_and_tests_installed_wheel',
                                             'old': 'def '
                                                    'test_phase2_delivery_builds_both_formats_and_tests_installed_wheel(repo_root):\n'},
                                            {'new': 'def '
                                                    'test_phase2_hero_workflow_preserves_scaffold_only_golden_boundary(repo_root,phase3_final_snapshot):\n'
                                                    '    repo_root = phase3_final_snapshot\n',
                                             'node': 'test_phase2_hero_workflow_preserves_scaffold_only_golden_boundary',
                                             'old': 'def '
                                                    'test_phase2_hero_workflow_preserves_scaffold_only_golden_boundary(repo_root):\n'}],
 'tests/integration/test_cli_validation.py': [{'new': 'def '
                                                      'test_cli_help_runs(subprocess_env,phase3_final_subprocess_env) '
                                                      '-> None:\n'
                                                      '    subprocess_env = '
                                                      'phase3_final_subprocess_env\n',
                                               'node': 'test_cli_help_runs',
                                               'old': 'def test_cli_help_runs(subprocess_env) -> '
                                                      'None:\n'}],
 'tests/integration/test_no_algorithms.py': [{'new': 'def '
                                                     'test_only_step8_authorized_modules_gain_behavior(package_root,phase3_final_package_root) '
                                                     '-> None:\n'
                                                     '    package_root = phase3_final_package_root\n',
                                              'node': 'test_only_step8_authorized_modules_gain_behavior',
                                              'old': 'def '
                                                     'test_only_step8_authorized_modules_gain_behavior(package_root) '
                                                     '-> None:\n'},
                                             {'new': 'def '
                                                     'test_protected_phase3_plus_modules_remain_placeholders(package_root,phase3_final_package_root) '
                                                     '-> None:\n'
                                                     '    package_root = phase3_final_package_root\n',
                                              'node': 'test_protected_phase3_plus_modules_remain_placeholders',
                                              'old': 'def '
                                                     'test_protected_phase3_plus_modules_remain_placeholders(package_root) '
                                                     '-> None:\n'},
                                             {'new': 'def '
                                                     'test_PR003_traceability_script_enforces_step8_scope(repo_root,phase3_final_snapshot) '
                                                     '-> None:\n'
                                                     '    repo_root = phase3_final_snapshot\n',
                                              'node': 'test_PR003_traceability_script_enforces_step8_scope',
                                              'old': 'def '
                                                     'test_PR003_traceability_script_enforces_step8_scope(repo_root) '
                                                     '-> None:\n'}],
 'tests/integration/test_phase3_metric_pipeline.py': [{'new': 'def '
                                                              'test_phase3_later_implementations_remain_empty(package_root,module,phase3_final_package_root):\n'
                                                              '    package_root = '
                                                              'phase3_final_package_root\n',
                                                       'node': 'test_phase3_later_implementations_remain_empty',
                                                       'old': 'def '
                                                              'test_phase3_later_implementations_remain_empty(package_root,module):\n'},
                                                      {'new': 'def '
                                                              'test_phase3_step11_rejects_changes_beyond_version_literals(repo_root,tmp_path,path,phase3_final_snapshot):\n'
                                                              '    repo_root = phase3_final_snapshot\n',
                                                       'node': 'test_phase3_step11_rejects_changes_beyond_version_literals',
                                                       'old': 'def '
                                                              'test_phase3_step11_rejects_changes_beyond_version_literals(repo_root,tmp_path,path):\n'},
                                                      {'new': 'def '
                                                              'test_phase3_step11_test_exceptions_are_exact(repo_root,phase3_step10_snapshot,phase3_final_snapshot):\n'
                                                              '    repo_root = phase3_final_snapshot\n',
                                                       'node': 'test_phase3_step11_test_exceptions_are_exact',
                                                       'old': 'def '
                                                              'test_phase3_step11_test_exceptions_are_exact(repo_root,phase3_step10_snapshot):\n'}],
 'tests/unit/test_PR012_evidence_classes.py': [{'new': 'def '
                                                       'test_PR012_evidence_classes_owner_and_placeholder(owner_checker, '
                                                       'placeholder_checker,phase3_final_owner_checker,phase3_final_placeholder_checker):\n'
                                                       '    owner_checker = phase3_final_owner_checker\n'
                                                       '    placeholder_checker = '
                                                       'phase3_final_placeholder_checker\n',
                                                'node': 'test_PR012_evidence_classes_owner_and_placeholder',
                                                'old': 'def '
                                                       'test_PR012_evidence_classes_owner_and_placeholder(owner_checker, '
                                                       'placeholder_checker):\n'}],
 'tests/unit/test_PR013_report_schema.py': [{'new': 'def '
                                                    'test_PR013_report_schema_owner_and_placeholder(owner_checker, '
                                                    'placeholder_checker,phase3_final_owner_checker,phase3_final_placeholder_checker):\n'
                                                    '    owner_checker = phase3_final_owner_checker\n'
                                                    '    placeholder_checker = '
                                                    'phase3_final_placeholder_checker\n',
                                             'node': 'test_PR013_report_schema_owner_and_placeholder',
                                             'old': 'def '
                                                    'test_PR013_report_schema_owner_and_placeholder(owner_checker, '
                                                    'placeholder_checker):\n'}],
 'tests/unit/test_PR014_unavailable.py': [{'new': 'def '
                                                  'test_PR014_unavailable_owner_and_placeholder(owner_checker, '
                                                  'placeholder_checker,phase3_final_owner_checker,phase3_final_placeholder_checker):\n'
                                                  '    owner_checker = phase3_final_owner_checker\n'
                                                  '    placeholder_checker = '
                                                  'phase3_final_placeholder_checker\n',
                                           'node': 'test_PR014_unavailable_owner_and_placeholder',
                                           'old': 'def '
                                                  'test_PR014_unavailable_owner_and_placeholder(owner_checker, '
                                                  'placeholder_checker):\n'}],
 'tests/unit/test_PR015_redaction.py': [{'new': 'def '
                                                'test_PR015_redaction_owner_and_placeholder(owner_checker, '
                                                'placeholder_checker,phase3_final_owner_checker,phase3_final_placeholder_checker):\n'
                                                '    owner_checker = phase3_final_owner_checker\n'
                                                '    placeholder_checker = '
                                                'phase3_final_placeholder_checker\n',
                                         'node': 'test_PR015_redaction_owner_and_placeholder',
                                         'old': 'def '
                                                'test_PR015_redaction_owner_and_placeholder(owner_checker, '
                                                'placeholder_checker):\n'}],
 'tests/unit/test_PR016_determinism.py': [{'new': 'def '
                                                  'test_PR016_ordering_owner_and_no_later_behavior(owner_checker, '
                                                  'package_root, '
                                                  'placeholder_checker,phase3_final_placeholder_checker):\n'
                                                  '    placeholder_checker = '
                                                  'phase3_final_placeholder_checker\n',
                                           'node': 'test_PR016_ordering_owner_and_no_later_behavior',
                                           'old': 'def '
                                                  'test_PR016_ordering_owner_and_no_later_behavior(owner_checker, '
                                                  'package_root, placeholder_checker):\n'}],
 'tests/unit/test_PR018_language.py': [{'new': 'def '
                                               'test_PR018_language_owner_and_placeholder(owner_checker, '
                                               'placeholder_checker,phase3_final_owner_checker,phase3_final_placeholder_checker):\n'
                                               '    owner_checker = phase3_final_owner_checker\n'
                                               '    placeholder_checker = '
                                               'phase3_final_placeholder_checker\n',
                                        'node': 'test_PR018_language_owner_and_placeholder',
                                        'old': 'def '
                                               'test_PR018_language_owner_and_placeholder(owner_checker, '
                                               'placeholder_checker):\n'}]}


@lru_cache(maxsize=1)
def _phase4_baseline_files():
    """Read immutable Git objects once, independently of the editable manifest."""
    for suffix, expected in (("^{commit}", PHASE4_FINAL), ("^{tree}", PHASE4_TREE),
                             (":tests", PHASE4_TEST_TREE)):
        if git("rev-parse", PHASE4_FINAL + suffix).decode().strip() != expected:
            raise ValueError("Pinned Phase 3 baseline identity mismatch")
    blobs = {}
    for entry in git("ls-tree", "-rz", PHASE4_FINAL).split(b"\0"):
        if not entry:
            continue
        info, name = entry.split(b"\t", 1)
        mode, kind, oid = info.split()
        path = name.decode("utf-8")
        if mode not in (b"100644", b"100755") or kind != b"blob":
            raise ValueError("Unexpected baseline file type")
        if Path(path).is_absolute() or ".." in Path(path).parts or path in blobs:
            raise ValueError("Unsafe baseline path")
        blobs[path] = oid.decode("ascii")
    result = {}
    with zipfile.ZipFile(io.BytesIO(git("archive", "--format=zip", PHASE4_FINAL))) as archive:
        names = [n for n in archive.namelist() if not n.endswith("/")]
        if len(names) != len(set(names)) or set(names) != set(blobs) or len(names) != 222:
            raise ValueError("Pinned baseline archive file set mismatch")
        for name in names:
            raw = archive.read(name)
            oid = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
            if oid != blobs[name]:
                raise ValueError(f"Pinned baseline blob mismatch: {name}")
            result[name] = raw
    return MappingProxyType(result)


def phase4_expected_control() -> dict:
    """Independent exact authorization, protected-byte and migration registry."""
    files = _phase4_baseline_files()
    authority = re.findall(r"\| `([^`]+\.md)` \| `([0-9a-f]{64})` \|",
                           files["PHASE_0_APPROVAL.md"].decode())
    if len(authority) != 16:
        raise ValueError("Expected sixteen original authority hashes")
    return {
        "control_version": "1.0", "active_phase": 4, "active_step": 1,
        "baseline_commit": PHASE4_FINAL, "baseline_tree": PHASE4_TREE,
        "baseline_test_tree": PHASE4_TEST_TREE, "baseline_branch": "phase3-metrics",
        "work_branch": "phase4-reports-cli",
        "main_at_authorization": "cfe1bd0941c1125498ac3d9d9ebf3adafa2c2fcb",
        "approved_plan_sha256": PHASE4_PLAN_SHA256, "approval_date": "2026-09-18",
        "approval_basis": PHASE4_APPROVAL,
        "approved_decisions": [f"P4-D{i:02d}" for i in range(1, 12)],
        "baseline_core_tests": 2489, "baseline_parquet_tests": 2492,
        "baseline_tracked_files": 222, "baseline_package_modules": 40,
        "baseline_placeholders": 16, "phase0_sha256": dict(authority),
        "baseline_files_sha256": {p: hashlib.sha256(raw).hexdigest() for p, raw in sorted(files.items())},
        "permitted_paths": sorted(PHASE4_STEP1_ALLOWED),
        "new_files_permitted": sorted(PHASE4_STEP1_NEW),
        "historical_migration_nodes": {p: [r["node"] for r in rows]
                                       for p, rows in sorted(PHASE4_MIGRATIONS.items())},
        "runtime_changes_authorized": False, "schema_changes_authorized": False,
        "phase_complete": False, "next_step_authorized": False,
        "main_merge_authorized": False, "publication_authorized": False,
    }


def verify_phase4_control(control: dict, step: int = 1) -> None:
    if type(step) is not int or step != 1 or type(control) is not dict:
        raise ValueError("Unsupported Phase 4 stage/control")
    try:
        actual = json.dumps(control, sort_keys=True, ensure_ascii=True, allow_nan=False)
        expected = json.dumps(phase4_expected_control(), sort_keys=True, ensure_ascii=True, allow_nan=False)
    except (TypeError, ValueError) as error:
        raise ValueError("Invalid Phase 4 control") from error
    if actual != expected:
        raise ValueError("Phase 4 control differs from the fixed approved Step 1 contract")


def verify_phase4_changes(changes: list[tuple[str, str]]) -> None:
    seen = set()
    for status, path in changes:
        if path in seen or path not in PHASE4_STEP1_ALLOWED:
            raise ValueError(f"Unapproved or repeated Phase 4 path: {path}")
        seen.add(path)
        required_status = "A" if path in PHASE4_STEP1_NEW else "M"
        if status != required_status:
            raise ValueError(f"Unapproved Phase 4 change kind: {status} {path}")


def verify_phase4_test_migration(path: str, before: bytes, after: bytes) -> None:
    """Permit exact source bindings, retaining original assertions/parameters."""
    if path not in PHASE4_MIGRATIONS or before != _phase4_baseline_files()[path]:
        raise ValueError("Migration requires the named pinned Phase 3 source")
    expected = before
    for row in PHASE4_MIGRATIONS[path]:
        old, new = row["old"].encode(), row["new"].encode()
        if expected.count(old) != 1:
            raise ValueError("Historical binding is not unique")
        expected = expected.replace(old, new, 1)
    if not after.startswith(expected):
        raise ValueError(f"Inherited test changed beyond its approved binding: {path}")
    _phase4_append_only(expected, after, path)


def _phase4_preserve_function_header(node, path):
    """Reject import-time effects in newly permitted function definitions."""
    decorators = [ast.unparse(value) for value in node.decorator_list]
    expected = []
    if path == "tests/conftest.py" and node.name.startswith("phase3_final_"):
        expected = ["pytest.fixture(scope='session')"]
    elif path == "scripts/release_check.py" and node.name == "_phase4_baseline_files":
        expected = ["lru_cache(maxsize=1)"]
    if decorators != expected:
        raise ValueError(f"Unapproved added function decorator: {path}:{node.name}")
    for value in [*node.args.defaults, *node.args.kw_defaults]:
        if value is None or isinstance(value, ast.Name) and value.id == "ROOT":
            continue
        try:
            ast.literal_eval(value)
        except (ValueError, TypeError, SyntaxError) as error:
            raise ValueError(f"Nonliteral added function default: {path}:{node.name}") from error
    arguments = [*node.args.posonlyargs, *node.args.args, *node.args.kwonlyargs]
    arguments.extend(value for value in (node.args.vararg, node.args.kwarg) if value is not None)
    annotations = [value.annotation for value in arguments] + [node.returns]
    allowed_nodes = (ast.Name, ast.Constant, ast.Subscript, ast.Tuple, ast.List,
                     ast.BinOp, ast.BitOr, ast.Load)
    allowed_names = {"Path", "list", "str", "bytes", "dict", "int", "bool", "tuple", "set"}
    for value in annotations:
        if value is not None and any(
                not isinstance(child, allowed_nodes)
                or isinstance(child, ast.Name) and child.id not in allowed_names
                for child in ast.walk(value)):
            raise ValueError(f"Unapproved added function annotation: {path}:{node.name}")


def _phase4_append_only(before: bytes, after: bytes, path: str) -> None:
    if not after.startswith(before):
        raise ValueError(f"Inherited source prefix changed: {path}")
    # Appended tests/helpers cannot shadow inherited globals or redefine nodes.
    old_tree, new_tree = ast.parse(before), ast.parse(after)
    def bindings(tree):
        names = []
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                names.append(node.name)
            elif isinstance(node, (ast.Assign, ast.AnnAssign)):
                targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                names.extend(n.id for target in targets for n in ast.walk(target) if isinstance(n, ast.Name))
        return names
    names = bindings(new_tree)
    if len(names) != len(set(names)) or any(names.count(n) != 1 for n in bindings(old_tree)):
        raise ValueError(f"Appended source redefines an inherited binding: {path}")
    for node in new_tree.body[len(old_tree.body):]:
        if not isinstance(node, ast.FunctionDef):
            raise ValueError(f"Appended test source executes or rebinds at module scope: {path}")
        prefix = "phase3_final_" if path == "tests/conftest.py" else "test_phase4_"
        if not node.name.startswith(prefix):
            raise ValueError(f"Appended function is outside the Step 1 test/fixture scope: {path}")
        _phase4_preserve_function_header(node, path)


def _phase4_preserve_tooling(before: bytes, after: bytes, path: str) -> None:
    """All inherited maintainer definitions/constants remain exact."""
    old_text, new_text = before.decode(), after.decode()
    old, new = ast.parse(old_text), ast.parse(new_text)
    def entry_guard(node):
        return isinstance(node, ast.If) and isinstance(node.test, ast.Compare) and "__name__" in ast.unparse(node.test)
    historical = [n for n in old.body if not entry_guard(n)]
    guards = [n for n in new.body if entry_guard(n)]
    expected_guard = ast.parse('if __name__ == "__main__":\n    raise SystemExit(cli_main())').body[0]
    if len(guards) != 1 or ast.dump(guards[0]) != ast.dump(expected_guard):
        raise ValueError(f"Unapproved maintainer entrypoint: {path}")
    cursor = 0
    allowed_imports = {"from functools import lru_cache", "import io", "import importlib.util", "from types import MappingProxyType"}
    for node in new.body:
        if entry_guard(node):
            continue
        segment = ast.get_source_segment(new_text, node)
        if cursor < len(historical) and segment == ast.get_source_segment(old_text, historical[cursor]):
            cursor += 1
            continue
        if isinstance(node, ast.FunctionDef) and (node.name == "cli_main" or node.name.startswith(
                ("phase4_", "_phase4_", "verify_phase4_", "audit_phase4"))):
            _phase4_preserve_function_header(node, path)
            continue
        if isinstance(node, ast.Assign) and all(isinstance(t, ast.Name) and t.id.startswith("PHASE4_") for t in node.targets):
            approved_union = ast.parse("PHASE4_G | PHASE4_STEP1_NEW | PHASE4_MIGRATION_PATHS", mode="eval").body
            if ([target.id for target in node.targets] == ["PHASE4_STEP1_ALLOWED"]
                    and ast.dump(node.value) == ast.dump(approved_union)):
                continue
            try:
                ast.literal_eval(node.value)
            except (ValueError, TypeError, SyntaxError) as error:
                raise ValueError(f"Nonliteral added maintainer constant: {path}") from error
            continue
        if isinstance(node, (ast.Import, ast.ImportFrom)) and ast.unparse(node) in allowed_imports:
            continue
        raise ValueError(f"Unapproved executable maintainer addition: {path}")
    if cursor != len(historical):
        raise ValueError(f"Historical maintainer statement changed: {path}")
    def named(tree):
        result = {}
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                keys = [node.name]
            elif isinstance(node, ast.Assign):
                keys = []
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        keys.append(target.id)
                    elif isinstance(target, (ast.Tuple, ast.List)):
                        keys.extend(n.id for n in ast.walk(target) if isinstance(n, ast.Name))
            else:
                continue
            for key in keys:
                if key in result:
                    raise ValueError(f"Duplicate maintainer binding: {key}")
                result[key] = node
        return result
    current = named(new)
    for key, node in named(old).items():
        if key not in current or ast.get_source_segment(old_text, node) != ast.get_source_segment(new_text, current[key]):
            raise ValueError(f"Historical maintainer contract changed: {path}:{key}")


def verify_phase4_snapshot(root: Path = ROOT) -> dict:
    files = _phase4_baseline_files()
    for path, raw in files.items():
        target = root / path
        if not target.is_file() or target.is_symlink():
            raise ValueError(f"Missing or aliased inherited file: {path}")
        current = target.read_bytes()
        if path not in PHASE4_STEP1_ALLOWED and current != raw:
            raise ValueError(f"Protected Phase 3 bytes changed: {path}")
        if path in PHASE4_MIGRATIONS:
            verify_phase4_test_migration(path, raw, current)
        elif path.startswith("tests/") and path in PHASE4_STEP1_ALLOWED:
            _phase4_append_only(raw, current, path)
        elif path.startswith("scripts/") and path in PHASE4_STEP1_ALLOWED:
            _phase4_preserve_tooling(raw, current, path)
    actual_modules = {p.relative_to(root).as_posix() for p in (root / "src/recursive_integrity_toolkit").rglob("*.py")}
    expected_modules = {p for p in files if p.startswith("src/") and p.endswith(".py")}
    if actual_modules != expected_modules or len(actual_modules) != 40:
        raise ValueError("Step 1 cannot change the runtime module set")
    if {p.name for p in (root / "schemas").iterdir()} != {Path(p).name for p in files if p.startswith("schemas/")}:
        raise ValueError("Step 1 cannot change the schema set")
    for path in PHASE4_STEP1_NEW:
        if not (root / path).is_file() or (root / path).is_symlink():
            raise ValueError(f"Missing or unsafe Step 1 control/test file: {path}")
    if hashlib.sha256((root / "PHASE_4_PLAN.md").read_bytes()).hexdigest() != PHASE4_PLAN_SHA256:
        raise ValueError("Approved Phase 4 plan bytes changed")
    verify_phase4_control(json.loads((root / "PHASE_4_BASELINE.json").read_text(encoding="utf-8")))
    decisions = (root / "PHASE_4_DECISIONS.md").read_text(encoding="utf-8")
    if PHASE4_APPROVAL not in decisions or any(f"P4-D{i:02d}" not in decisions for i in range(1, 12)):
        raise ValueError("Actual Phase 4 approval record missing")
    if any((root / name).exists() for name in PHASE4_FORBIDDEN_OUTPUTS):
        raise ValueError("Step 1 cannot create Phase 4 completion records or audit reports")
    return {"package_modules_unchanged": 40, "schemas_unchanged": 5,
            "hero_files_unchanged": 6, "historical_migrated_nodes": 16,
            "phase_complete": False, "runtime_behavior_added": False}


def audit_phase4(step: int = 1) -> dict:
    verify_phase4_control(json.loads((ROOT / "PHASE_4_BASELINE.json").read_text(encoding="utf-8")), step)
    result = {"phase": 4, "active_step": step, **verify_phase4_snapshot(),
              "phase0_hashes_verified": 16, "publication_authorized": False}
    print(json.dumps(result, indent=2))
    return result


def audit_phase4_diff(step: int = 1) -> dict:
    if type(step) is not int or step != 1:
        raise ValueError("Unsupported Phase 4 step")
    subprocess.run(["git", "-C", str(ROOT), "merge-base", "--is-ancestor", PHASE4_FINAL, "HEAD"], check=True)
    raw = git("diff", "--name-status", "--no-renames", "-z", PHASE4_FINAL, "--").split(b"\0")
    raw = [part.decode("utf-8") for part in raw if part]
    if len(raw) % 2:
        raise ValueError("Malformed Git difference records")
    changes = list(zip(raw[::2], raw[1::2]))
    changes.extend(("A", p.decode()) for p in git("ls-files", "--others", "--exclude-standard", "-z").split(b"\0") if p)
    verify_phase4_changes(changes)
    result = {"baseline_commit": PHASE4_FINAL, "changed_files": len(changes),
              "changes": changes, "step": 1, "scope": "PASS"}
    print(json.dumps(result, indent=2))
    return result


def phase4_baseline_evidence(output: Path) -> dict:
    """Reconcile final Phase 3 identities plus all previously required identities."""
    output.mkdir(parents=True, exist_ok=True)
    inherited = baseline_evidence(output / "phase3-inherited")
    with tempfile.TemporaryDirectory(prefix="rit-p4-baseline-") as temp:
        baseline = Path(temp)
        for name, raw in _phase4_baseline_files().items():
            target = baseline / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(raw)
        old, old_log = _collect(baseline)
    current, current_log = _collect(ROOT)
    expected = 2492 if os.environ.get("RIT_TEST_PARQUET") == "1" else 2489
    if len(old) != expected or set(old) - set(current):
        raise ValueError("Accepted final Phase 3 test identities were lost")
    result = {"baseline_commit": PHASE4_FINAL, "baseline_test_tree": PHASE4_TEST_TREE,
              "baseline_nodeids": old, "current_nodeids": current, "missing_nodeids": [],
              "baseline_tests": len(old), "current_tests": len(current), "inherited": inherited,
              "nodeids_sha256": hashlib.sha256(("\n".join(old)+"\n").encode()).hexdigest()}
    (output / "phase4_test_identity_manifest.json").write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    (output / "phase3-final-collection.log").write_text(old_log, encoding="utf-8")
    (output / "phase4-current-collection.log").write_text(current_log, encoding="utf-8")
    print(json.dumps({k: result[k] for k in ("baseline_tests", "current_tests", "missing_nodeids")}, indent=2))
    return result


def phase4_candidate(output: Path, step: int = 1) -> None:
    """Archive a tested intermediate Step 1; never certify phase completion."""
    if os.environ.get("RIT_TEST_PARQUET") != "1":
        raise ValueError("Step 1 candidate evidence requires RIT_TEST_PARQUET=1 and real PyArrow")
    if importlib.util.find_spec("pyarrow") is None:
        raise ValueError("Step 1 candidate evidence requires real PyArrow")
    output.mkdir(parents=True, exist_ok=True)
    result = audit_phase4(step)
    result["diff"] = audit_phase4_diff(step)
    if git("status", "--porcelain").strip():
        raise ValueError("Candidate archive requires committed, clean source")
    result["core"] = verify_junit(output / "core.xml", minimum=2489)
    result["parquet"] = verify_junit(output / "parquet.xml", require_parquet=True, minimum=2492)
    result["core_math_measurements"] = verify_step10_evidence(output / "core.xml", output / "phase4-core-observations.json")
    result["parquet_math_measurements"] = verify_step10_evidence(output / "parquet.xml", output / "phase4-parquet-observations.json")
    identity = phase4_baseline_evidence(output)
    result["test_identity"] = {k: identity[k] for k in ("baseline_tests", "current_tests", "nodeids_sha256")}
    expected = set()
    for node in identity["current_nodeids"]:
        base, bracket, parameter = node.partition("[")
        owner, name = base.rsplit("::", 1)
        expected.add((owner.removesuffix(".py").replace("/", ".").replace("::", "."),
                      name + bracket + parameter))
    for name, parquet in (("core.xml", False), ("parquet.xml", True)):
        cases = {(c.get("classname", ""), c.get("name", "")) for c in ET.parse(output / name).getroot().iter("testcase")}
        target = expected if parquet else {c for c in expected if c[1] not in PARQUET_CASES}
        if cases != target:
            raise ValueError(f"Candidate JUnit does not execute the entire current suite: {name}")
    verify_distributions(output / "dist")
    archive = output / "recursive-integrity-toolkit-phase4-step1-candidate.zip"
    subprocess.run(["git", "-C", str(ROOT), "archive", "--format=zip", "--prefix=recursive-integrity-toolkit/", "HEAD", "-o", str(archive.resolve())], check=True)
    tracked = {p for p in git("ls-files", "-z").decode().split("\0") if p}
    with zipfile.ZipFile(archive) as zipped:
        names = {p.removeprefix("recursive-integrity-toolkit/") for p in zipped.namelist() if not p.endswith("/")}
        if names != tracked:
            raise ValueError("Step 1 source archive file set mismatch")
        for name in names:
            if zipped.read("recursive-integrity-toolkit/"+name) != (ROOT / name).read_bytes():
                raise ValueError(f"Step 1 source archive byte mismatch: {name}")
    result.update({"commit": git("rev-parse", "HEAD").decode().strip(),
                   "tree": git("rev-parse", "HEAD^{tree}").decode().strip(),
                   "source_archive": archive.name, "tracked_files": len(tracked),
                   "python": sys.version, "platform": sys.platform,
                   "versions": {name: importlib.metadata.version(name) for name in ("numpy", "pandas", "pytest")}})
    (output / "phase4_execution_metadata.json").write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    (output / "phase4_repository_files.sha256").write_text("".join(f"{hashlib.sha256((ROOT/name).read_bytes()).hexdigest()}  {name}\n" for name in sorted(tracked)), encoding="utf-8")
    paths = sorted(p for p in output.rglob("*") if p.is_file() and p.name != "phase4_artifacts.sha256")
    (output / "phase4_artifacts.sha256").write_text("".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(output).as_posix()}\n" for p in paths), encoding="utf-8")
    print(f"Phase 4 Step 1 candidate: {len(tracked)} source files verified; Phase 4 remains incomplete.")


def phase4_cli_main() -> int:
    parser = argparse.ArgumentParser(description="Phase 4 Step 1 maintainer gate")
    parser.add_argument("--phase", type=int, choices=(4,), required=True)
    parser.add_argument("--step", type=int, choices=(1,), required=True)
    parser.add_argument("--diff", action="store_true")
    parser.add_argument("--junit", type=Path)
    parser.add_argument("--require-parquet", action="store_true")
    parser.add_argument("--minimum-tests", type=int, default=1)
    parser.add_argument("--baseline-evidence", type=Path)
    parser.add_argument("--dist", type=Path)
    parser.add_argument("--smoke-wheel", type=Path)
    parser.add_argument("--candidate", type=Path)
    parser.add_argument("--delivery", type=Path)
    args = parser.parse_args()
    if args.delivery is not None:
        raise ValueError("Phase 4 Step 1 cannot certify a final phase delivery")
    if args.junit is not None:
        verify_junit(args.junit, require_parquet=args.require_parquet, minimum=args.minimum_tests)
    elif args.baseline_evidence is not None:
        phase4_baseline_evidence(args.baseline_evidence)
    elif args.dist is not None:
        audit_phase4(args.step)
        wheel, _ = verify_distributions(args.dist)
        smoke_installed(wheel)
        smoke_installed_duplicates(wheel)
    elif args.smoke_wheel is not None:
        smoke_installed(args.smoke_wheel)
    elif args.candidate is not None:
        phase4_candidate(args.candidate, args.step)
    else:
        audit_phase4(args.step)
        if args.diff:
            audit_phase4_diff(args.step)
    return 0


# Phase 4 Step 2 is additive. Step 1 gates above retain their original semantics.
PHASE4_STEP1_FINAL = "a7f3c46d6ca05de36bfcb60f496ebb2d5ab4a37c"
PHASE4_STEP1_LOCAL = "5aa9cd6d06bfffec9cc280a52277aa9152a8627e"
PHASE4_STEP1_TREE = "7f8ef492568456bf5d46fb1b7e2631cb9b94e3fd"
PHASE4_STEP1_TEST_TREE = "2ce77e331a0fc377387735bb55dffd3be630b59c"
PHASE4_STEP2_APPROVAL = "批准，开始 **Phase 4 Step 2**"
PHASE4_STEP2_APPROVAL_DATE = "2026-09-19"
PHASE4_STEP2_REPORT_SCHEMA_SHA256 = "34b7edb8e8672fca3f3d4f6fe647b4d8967acb6f0435544ba449c1c44f7bc1f6"
PHASE4_STEP2_ALLOWED = {
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
PHASE4_STEP2_NEW = ()
PHASE4_STEP2_MIGRATIONS = {'tests/integration/test_phase4_gates.py': [{'new': 'def phase4_mutation_tree(repo_root, '
                                                    'tmp_path_factory, phase4_gate_tools, '
                                                    'phase4_step1_snapshot):',
                                             'node': 'phase4_mutation_tree',
                                             'old': 'def phase4_mutation_tree(repo_root, '
                                                    'tmp_path_factory, phase4_gate_tools):'},
                                            {'new': 'shutil.copyfile(phase4_step1_snapshot / '
                                                    'relative, destination)',
                                             'node': 'phase4_mutation_tree',
                                             'old': 'shutil.copyfile(repo_root / relative, '
                                                    'destination)'},
                                            {'new': 'def '
                                                    'test_phase4_final_snapshot_preserves_all_current_runtime_bytes(repo_root, '
                                                    'phase3_final_snapshot, '
                                                    'phase4_step1_snapshot):\n'
                                                    '    repo_root = phase4_step1_snapshot',
                                             'node': 'test_phase4_final_snapshot_preserves_all_current_runtime_bytes',
                                             'old': 'def '
                                                    'test_phase4_final_snapshot_preserves_all_current_runtime_bytes(repo_root, '
                                                    'phase3_final_snapshot):'},
                                            {'new': 'def '
                                                    'test_phase4_active_workflows_preserve_full_matrix_and_use_current_dispatch(repo_root, '
                                                    'phase4_step1_snapshot):\n'
                                                    '    repo_root = phase4_step1_snapshot',
                                             'node': 'test_phase4_active_workflows_preserve_full_matrix_and_use_current_dispatch',
                                             'old': 'def '
                                                    'test_phase4_active_workflows_preserve_full_matrix_and_use_current_dispatch(repo_root):'}],
 'tests/unit/test_phase4_contracts.py': [{'new': 'def phase4_control(phase4_step1_snapshot):\n'
                                                 '    return json.loads((phase4_step1_snapshot / '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))',
                                          'node': 'phase4_control',
                                          'old': 'def phase4_control():\n'
                                                 '    return json.loads((ROOT / '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))'},
                                         {'new': 'def '
                                                 'test_phase4_registered_migrations_accept_only_the_approved_inventory(phase4_tools, '
                                                 'phase3_final_snapshot, phase4_step1_snapshot):',
                                          'node': 'test_phase4_registered_migrations_accept_only_the_approved_inventory',
                                          'old': 'def '
                                                 'test_phase4_registered_migrations_accept_only_the_approved_inventory(phase4_tools, '
                                                 'phase3_final_snapshot):'},
                                         {'new': 'path, (phase3_final_snapshot / '
                                                 'path).read_bytes(), (phase4_step1_snapshot / '
                                                 'path).read_bytes(),',
                                          'node': 'test_phase4_registered_migrations_accept_only_the_approved_inventory',
                                          'old': 'path, (phase3_final_snapshot / '
                                                 'path).read_bytes(), (ROOT / '
                                                 'path).read_bytes(),'}]}


def _phase4_step1_files():
    """Read the exact accepted Step 1 Git tree and verify every blob identity."""
    for suffix, expected in (("^{commit}", PHASE4_STEP1_FINAL), ("^{tree}", PHASE4_STEP1_TREE),
                             (":tests", PHASE4_STEP1_TEST_TREE)):
        if git("rev-parse", PHASE4_STEP1_FINAL + suffix).decode().strip() != expected:
            raise ValueError("Pinned Phase 4 Step 1 identity mismatch")
    objects = {}
    for entry in git("ls-tree", "-rz", PHASE4_STEP1_FINAL).split(b"\0"):
        if not entry:
            continue
        metadata, raw_path = entry.split(b"\t", 1)
        mode, kind, oid = metadata.split()
        path = raw_path.decode("utf-8")
        if (mode not in (b"100644", b"100755") or kind != b"blob" or path in objects
                or path.startswith("/") or ".." in path.split("/") or ".git" in path.split("/")):
            raise ValueError("Unsafe pinned Step 1 Git object")
        objects[path] = oid.decode("ascii")
    if len(objects) != 227:
        raise ValueError("Pinned Step 1 must contain exactly 227 files")
    files = {}
    with zipfile.ZipFile(io.BytesIO(git("archive", "--format=zip", PHASE4_STEP1_FINAL))) as archive:
        names = [item.filename for item in archive.infolist() if not item.is_dir()]
        if len(names) != len(objects) or set(names) != set(objects):
            raise ValueError("Pinned Step 1 archive identity mismatch")
        for name in names:
            raw = archive.read(name)
            oid = hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()
            if oid != objects[name]:
                raise ValueError(f"Pinned Step 1 blob mismatch: {name}")
            files[name] = raw
    return MappingProxyType(files)


def phase4_step2_expected_control() -> dict:
    """Actual Step 2 approval is independent of the mutable control document."""
    prior = _phase4_step1_files()
    result = phase4_expected_control()
    result.update({
        "control_version": "1.1", "active_step": 2,
        "approval_date": PHASE4_STEP2_APPROVAL_DATE, "approval_basis": PHASE4_STEP2_APPROVAL,
        "previous_step_commit": PHASE4_STEP1_FINAL,
        "previous_step_local_commit": PHASE4_STEP1_LOCAL,
        "previous_step_tree": PHASE4_STEP1_TREE,
        "previous_step_test_tree": PHASE4_STEP1_TEST_TREE,
        "previous_step_core_tests": 2584, "previous_step_parquet_tests": 2587,
        "previous_step_files_sha256": {p: hashlib.sha256(raw).hexdigest() for p, raw in sorted(prior.items())},
        "permitted_paths": sorted(PHASE4_STEP2_ALLOWED), "new_files_permitted": [],
        "runtime_changes_authorized": True, "schema_changes_authorized": True,
        "runtime_paths_authorized": ["src/recursive_integrity_toolkit/result.py"],
        "schema_paths_authorized": ["schemas/report.schema.json"],
        "step1_historical_binding_nodes": {p: sorted({r["node"] for r in rows})
                                          for p, rows in sorted(PHASE4_STEP2_MIGRATIONS.items())},
    })
    return result


def verify_phase4_step2_control(control: dict, step: int = 2) -> None:
    if type(step) is not int or step != 2 or type(control) is not dict:
        raise ValueError("Unsupported Phase 4 Step 2 stage/control")
    try:
        actual = json.dumps(control, sort_keys=True, ensure_ascii=True, allow_nan=False)
        expected = json.dumps(phase4_step2_expected_control(), sort_keys=True, ensure_ascii=True, allow_nan=False)
    except (TypeError, ValueError) as error:
        raise ValueError("Invalid Phase 4 Step 2 control") from error
    if actual != expected:
        raise ValueError("Phase 4 control differs from the independently approved Step 2 contract")


def verify_phase4_step2_changes(changes: list[tuple[str, str]]) -> None:
    seen = set()
    for status, path in changes:
        if path in seen or path not in PHASE4_STEP2_ALLOWED or status != "M":
            raise ValueError(f"Unapproved Phase 4 Step 2 path/operation: {status} {path}")
        seen.add(path)


def _phase4_step2_header(node, path):
    """Allow explicit test parametrization/fixtures, never definition-time effects."""
    for decorator in node.decorator_list:
        if not isinstance(decorator, ast.Call) or ast.unparse(decorator.func) not in {
                "pytest.fixture", "pytest.mark.parametrize"}:
            raise ValueError(f"Unapproved Step 2 test decorator: {path}:{node.name}")
        if ast.unparse(decorator.func) == "pytest.fixture" and not node.name.startswith("phase4_step"):
            raise ValueError("A Step 2 fixture must have an explicit scoped name")
        if any(keyword.arg is None for keyword in decorator.keywords):
            raise ValueError("Decorator expansion is outside the Step 2 contract")
        for value in [*decorator.args, *(keyword.value for keyword in decorator.keywords)]:
            try:
                ast.literal_eval(value)
            except (ValueError, TypeError, SyntaxError) as error:
                raise ValueError("Step 2 decorator arguments must be literal") from error
    clone = ast.parse(ast.unparse(node)).body[0]
    clone.decorator_list = []
    _phase4_preserve_function_header(clone, path)


def _phase4_step2_append_only(before: bytes, after: bytes, path: str) -> None:
    if not after.startswith(before):
        raise ValueError(f"Inherited Step 1 prefix changed: {path}")
    old, new = ast.parse(before), ast.parse(after)
    bindings = set()
    for node in old.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            bindings.add(node.name)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            bindings.update(alias.asname or alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            bindings.update(child.id for target in targets for child in ast.walk(target) if isinstance(child, ast.Name))
    for node in new.body[len(old.body):]:
        if not isinstance(node, ast.FunctionDef) or node.name in bindings:
            raise ValueError(f"Step 2 addition executes, rebinds or shadows inherited source: {path}")
        if not node.name.startswith(("test_phase4_step2_", "phase4_step2_", "phase4_step1_")):
            raise ValueError(f"Step 2 added test/helper is not explicitly scoped: {path}:{node.name}")
        if path == "tests/conftest.py" and node.name != "phase4_step1_snapshot":
            raise ValueError("Only the pinned Step 1 shared fixture is authorized")
        bindings.add(node.name)
        _phase4_step2_header(node, path)


def verify_phase4_step2_test_migration(path: str, before: bytes, after: bytes) -> None:
    prior = _phase4_step1_files()
    if path not in prior or path not in PHASE4_STEP2_ALLOWED or before != prior[path] or not path.startswith("tests/"):
        raise ValueError("Step 2 migration requires the exact named Step 1 source")
    _phase4_step2_check_test_migration(path, before, after)


def _phase4_step2_check_test_migration(path: str, before: bytes, after: bytes) -> None:
    """Check a source already read from the verified Step 1 immutable mapping."""
    expected = before
    for row in PHASE4_STEP2_MIGRATIONS.get(path, []):
        old, new = row["old"].encode(), row["new"].encode()
        if expected.count(old) != 1:
            raise ValueError("Step 1 historical binding is not unique")
        expected = expected.replace(old, new, 1)
    _phase4_step2_append_only(expected, after, path)


def _phase4_step2_preserve_tooling(before: bytes, after: bytes, path: str) -> None:
    """Normalize only the exact new dispatch branch, then preserve all old code."""
    if path == "scripts/release_check.py":
        old = '    return phase4_cli_main() if explicit_phase4 else main()'
        new = ('    explicit_step2 = "--step=2" in argv or any(a == "--step" and b == "2" for a, b in zip(argv, argv[1:]))\n'
               '    if explicit_phase4 and explicit_step2:\n'
               '        return phase4_step2_cli_main()\n'
               '    return phase4_cli_main() if explicit_phase4 else main()')
        replacements = [(old, new)]
    else:
        old = '    if args.phase == 4 and args.step == 1:\n        return phase4_main(step=args.step)\n'
        new = old + '    if args.phase == 4 and args.step == 2:\n        return phase4_step2_main(step=args.step)\n'
        replacements = [(old, new),
                        ('Choose explicit --phase 3 --step 11 or --phase 4 --step 1',
                         'Choose explicit --phase 3 --step 11 or --phase 4 --step 1 or --phase 4 --step 2')]
    expected = before
    for old, new in replacements:
        if expected.count(old.encode()) != 1:
            raise ValueError(f"Historical dispatcher identity mismatch: {path}")
        expected = expected.replace(old.encode(), new.encode(), 1)
    _phase4_preserve_tooling(expected, after, path)


def verify_phase4_step2_snapshot(root: Path = ROOT) -> dict:
    prior = _phase4_step1_files()
    for path, raw in prior.items():
        target = root / path
        if not target.is_file() or target.is_symlink():
            raise ValueError(f"Missing or aliased inherited Step 1 file: {path}")
        current = target.read_bytes()
        if path not in PHASE4_STEP2_ALLOWED and current != raw:
            raise ValueError(f"Protected Step 1 bytes changed: {path}")
        if path.startswith("tests/") and path in PHASE4_STEP2_ALLOWED:
            _phase4_step2_check_test_migration(path, raw, current)
        elif path.startswith("scripts/") and path in PHASE4_STEP2_ALLOWED:
            _phase4_step2_preserve_tooling(raw, current, path)
        elif path in {"docs/architecture.md", "docs/theory_traceability.md", "PHASE_4_DECISIONS.md"}:
            if not current.startswith(raw):
                raise ValueError(f"Step 1 historical documentation prefix changed: {path}")
    actual_modules = {p.relative_to(root).as_posix() for p in (root / "src/recursive_integrity_toolkit").rglob("*.py")}
    expected_modules = {p for p in prior if p.startswith("src/") and p.endswith(".py")}
    if actual_modules != expected_modules or len(actual_modules) != 40:
        raise ValueError("Step 2 cannot change the runtime module set")
    if {p.name for p in (root / "schemas").iterdir()} != {Path(p).name for p in prior if p.startswith("schemas/")}:
        raise ValueError("Step 2 cannot change the schema set")
    if hashlib.sha256((root / "PHASE_4_PLAN.md").read_bytes()).hexdigest() != PHASE4_PLAN_SHA256:
        raise ValueError("Approved Phase 4 plan changed")
    verify_phase4_step2_control(json.loads((root / "PHASE_4_BASELINE.json").read_text(encoding="utf-8")))
    decisions = (root / "PHASE_4_DECISIONS.md").read_text(encoding="utf-8")
    if PHASE4_STEP2_APPROVAL not in decisions or PHASE4_STEP1_FINAL not in decisions:
        raise ValueError("Actual Step 2 authorization or Step 1 evidence anchor missing")
    if any((root / name).exists() for name in PHASE4_FORBIDDEN_OUTPUTS):
        raise ValueError("Step 2 cannot create Phase 4 completion records or audit outputs")
    import runpy
    checker = runpy.run_path(str(root / "scripts/check_traceability.py"), run_name="phase4_step2_contract_boundary")
    checker["phase4_step2_result_boundary"](root / "src/recursive_integrity_toolkit/result.py")
    schema_bytes = (root / "schemas/report.schema.json").read_bytes()
    if hashlib.sha256(schema_bytes).hexdigest() != PHASE4_STEP2_REPORT_SCHEMA_SHA256:
        raise ValueError("Step 2 report schema differs from its independently reviewed bytes")
    schema = json.loads(schema_bytes)
    if (schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema"
            or schema.get("type") != "object" or schema.get("additionalProperties") is not False):
        raise ValueError("Step 2 report schema dialect/closed root mismatch")
    return {"package_modules": 40, "frozen_runtime_modules": 39, "frozen_schemas": 4,
            "hero_files_unchanged": 6, "historical_phase3_migrated_nodes": 16,
            "phase_complete": False, "result_contracts_enabled": True,
            "adapters_enabled": False, "cli_analysis_enabled": False}


def audit_phase4_step2(step: int = 2) -> dict:
    verify_phase4_step2_control(json.loads((ROOT / "PHASE_4_BASELINE.json").read_text(encoding="utf-8")), step)
    result = {"phase": 4, "active_step": step, **verify_phase4_step2_snapshot(),
              "phase0_hashes_verified": 16, "publication_authorized": False}
    print(json.dumps(result, indent=2))
    return result


def audit_phase4_step2_diff(step: int = 2) -> dict:
    if type(step) is not int or step != 2:
        raise ValueError("Unsupported Phase 4 Step 2 stage")
    _phase4_step1_files()
    subprocess.run(["git", "-C", str(ROOT), "merge-base", "--is-ancestor", PHASE4_STEP1_FINAL, "HEAD"], check=True)
    raw = git("diff", "--name-status", "--no-renames", "-z", PHASE4_STEP1_FINAL, "--").split(b"\0")
    raw = [part.decode("utf-8") for part in raw if part]
    if len(raw) % 2:
        raise ValueError("Malformed Step 2 Git difference records")
    changes = list(zip(raw[::2], raw[1::2]))
    changes.extend(("A", p.decode()) for p in git("ls-files", "--others", "--exclude-standard", "-z").split(b"\0") if p)
    verify_phase4_step2_changes(changes)
    result = {"previous_step_commit": PHASE4_STEP1_FINAL, "changed_files": len(changes),
              "changes": changes, "step": 2, "scope": "PASS"}
    print(json.dumps(result, indent=2))
    return result


def phase4_step2_baseline_evidence(output: Path) -> dict:
    """Reconcile all inherited identities, including the accepted Step 1 suite."""
    output.mkdir(parents=True, exist_ok=True)
    inherited = phase4_baseline_evidence(output / "phase4-step1-inherited")
    with tempfile.TemporaryDirectory(prefix="rit-p4-step1-identities-") as temp:
        baseline = Path(temp)
        for name, raw in _phase4_step1_files().items():
            target = baseline / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(raw)
        old, old_log = _collect(baseline)
    current, current_log = _collect(ROOT)
    expected = 2587 if os.environ.get("RIT_TEST_PARQUET") == "1" else 2584
    if len(old) != expected or set(old) - set(current):
        raise ValueError("Accepted Phase 4 Step 1 test identities were lost")
    result = {"baseline_commit": PHASE4_STEP1_FINAL, "baseline_test_tree": PHASE4_STEP1_TEST_TREE,
              "baseline_nodeids": old, "current_nodeids": current, "missing_nodeids": [],
              "baseline_tests": len(old), "current_tests": len(current), "inherited": inherited,
              "nodeids_sha256": hashlib.sha256(("\n".join(old)+"\n").encode()).hexdigest()}
    (output / "phase4_step2_test_identity_manifest.json").write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    (output / "phase4-step1-collection.log").write_text(old_log, encoding="utf-8")
    (output / "phase4-step2-collection.log").write_text(current_log, encoding="utf-8")
    print(json.dumps({k: result[k] for k in ("baseline_tests", "current_tests", "missing_nodeids")}, indent=2))
    return result


def phase4_step2_candidate(output: Path, step: int = 2) -> None:
    """Build tested Step 2 intermediate evidence without declaring Phase 4 complete."""
    if os.environ.get("RIT_TEST_PARQUET") != "1" or importlib.util.find_spec("pyarrow") is None:
        raise ValueError("Step 2 candidate evidence requires RIT_TEST_PARQUET=1 and real PyArrow")
    output.mkdir(parents=True, exist_ok=True)
    result = audit_phase4_step2(step)
    result["diff"] = audit_phase4_step2_diff(step)
    if git("status", "--porcelain").strip():
        raise ValueError("Step 2 candidate archive requires committed, clean source")
    result["core"] = verify_junit(output / "core.xml", minimum=2584)
    result["parquet"] = verify_junit(output / "parquet.xml", require_parquet=True, minimum=2587)
    result["core_math_measurements"] = verify_step10_evidence(output / "core.xml", output / "phase4-step2-core-observations.json")
    result["parquet_math_measurements"] = verify_step10_evidence(output / "parquet.xml", output / "phase4-step2-parquet-observations.json")
    identity = phase4_step2_baseline_evidence(output)
    result["test_identity"] = {k: identity[k] for k in ("baseline_tests", "current_tests", "nodeids_sha256")}
    expected = set()
    for node in identity["current_nodeids"]:
        base, bracket, parameter = node.partition("[")
        owner, name = base.rsplit("::", 1)
        expected.add((owner.removesuffix(".py").replace("/", ".").replace("::", "."), name + bracket + parameter))
    for name, parquet in (("core.xml", False), ("parquet.xml", True)):
        cases = {(c.get("classname", ""), c.get("name", "")) for c in ET.parse(output / name).getroot().iter("testcase")}
        target = expected if parquet else {c for c in expected if c[1] not in PARQUET_CASES}
        if cases != target:
            raise ValueError(f"Step 2 JUnit does not execute the entire current suite: {name}")
    wheel, _ = verify_distributions(output / "dist")
    phase4_step2_installed_contract_smoke(wheel)
    archive = output / "recursive-integrity-toolkit-phase4-step2-candidate.zip"
    subprocess.run(["git", "-C", str(ROOT), "archive", "--format=zip", "--prefix=recursive-integrity-toolkit/", "HEAD", "-o", str(archive.resolve())], check=True)
    tracked = {p for p in git("ls-files", "-z").decode().split("\0") if p}
    with zipfile.ZipFile(archive) as zipped:
        names = {p.removeprefix("recursive-integrity-toolkit/") for p in zipped.namelist() if not p.endswith("/")}
        if names != tracked or len(tracked) != 227:
            raise ValueError("Step 2 source archive file set mismatch")
        for name in names:
            if zipped.read("recursive-integrity-toolkit/"+name) != (ROOT / name).read_bytes():
                raise ValueError(f"Step 2 source archive byte mismatch: {name}")
    result.update({"commit": git("rev-parse", "HEAD").decode().strip(),
                   "tree": git("rev-parse", "HEAD^{tree}").decode().strip(),
                   "source_archive": archive.name, "tracked_files": len(tracked),
                   "python": sys.version, "platform": sys.platform,
                   "versions": {name: importlib.metadata.version(name) for name in ("numpy", "pandas", "pytest")}})
    (output / "phase4_step2_execution_metadata.json").write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    (output / "phase4_step2_repository_files.sha256").write_text("".join(f"{hashlib.sha256((ROOT/name).read_bytes()).hexdigest()}  {name}\n" for name in sorted(tracked)), encoding="utf-8")
    paths = sorted(p for p in output.rglob("*") if p.is_file() and p.name != "phase4_step2_artifacts.sha256")
    (output / "phase4_step2_artifacts.sha256").write_text("".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(output).as_posix()}\n" for p in paths), encoding="utf-8")
    print(f"Phase 4 Step 2 candidate: {len(tracked)} source files verified; Phase 4 remains incomplete.")


def phase4_step2_installed_contract_smoke(wheel: Path) -> None:
    """Exercise installed canonical contracts with no optional or analytical imports."""
    with tempfile.TemporaryDirectory(prefix="rit-p4-step2-installed-contract-") as temp:
        work = Path(temp)
        subprocess.run([sys.executable, "-m", "venv", str(work / "venv")], check=True)
        bindir = work / "venv" / ("Scripts" if os.name == "nt" else "bin")
        python = bindir / ("python.exe" if os.name == "nt" else "python")
        subprocess.run([str(python), "-m", "pip", "install", "--no-index", "--no-deps", str(wheel.resolve())],
                       cwd=work, check=True)
        program = '''import builtins, copy, importlib.abc, io, socket, sys
from dataclasses import FrozenInstanceError
from pathlib import Path
blocked_roots = {'numpy', 'pandas', 'pyarrow', 'jsonschema', 'referencing', 'networkx', 'scipy', 'sklearn'}
blocked_layers = tuple('recursive_integrity_toolkit.' + name for name in (
    'metrics', 'io', 'representations', 'observability', 'lineage', 'reports', 'cli', 'config', 'models', 'errors'))
class DenyAnalysis(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in blocked_roots or any(
                fullname == layer or fullname.startswith(layer + '.') for layer in blocked_layers):
            raise AssertionError('installed contract attempted analytical or optional import: ' + fullname)
sys.meta_path.insert(0, DenyAnalysis())
def blocked(*args, **kwargs):
    raise AssertionError('installed contract attempted file or network access')
socket.create_connection = blocked
socket.getaddrinfo = blocked
socket.socket.connect = blocked
socket.socket.connect_ex = blocked
def reject_schema_files(event, args):
    if event == 'open' and isinstance(args[0], (str, bytes)):
        path = str(args[0]).lower()
        if path.endswith('.json') or 'report.schema' in path:
            raise AssertionError('installed contract attempted schema file access')
sys.addaudithook(reject_schema_files)
import recursive_integrity_toolkit.result as result_module
from recursive_integrity_toolkit.result import CanonicalReport, validate_report, report_schema
assert Path(result_module.__file__).resolve().is_relative_to(Path(sys.argv[1]) / 'venv')
assert not Path(result_module.__file__).resolve().is_relative_to(Path(sys.argv[2]) / 'src')
# All subsequent contract operations must be entirely in memory.
builtins.open = blocked
io.open = blocked
sections = ('run', 'inputs', 'observability', 'capabilities', 'observed_facts',
            'derived_metrics', 'proxy_signals', 'simulations', 'unavailable_conclusions',
            'recommended_next_metadata', 'warnings', 'errors')
payload = {
    'run': {
        'run_id': 'installed-empty-case', 'toolkit_version': '0.1.0.dev2',
        'report_schema_version': '1.0', 'started_at': '2026-09-19T00:00:00+00:00',
        'completed_at': '2026-09-19T00:00:00+00:00', 'duration_seconds': 0,
        'python_version': '3.12', 'platform': 'isolated-installed-smoke',
        'command': 'rit validate', 'config_hash': '0123456789abcdef' * 4,
        'random_seed': None, 'strict_mode': False, 'redacted_mode': False,
        'network_call_count': 0, 'deterministic': True, 'privacy_mode': 'standard',
        'run_status': 'complete',
        'null_reasons': {'random_seed': 'No stochastic scenario was requested.'},
    },
    'inputs': {}, 'observability': {}, 'capabilities': {}, 'observed_facts': {},
    'derived_metrics': {}, 'proxy_signals': {}, 'simulations': {},
    'unavailable_conclusions': [], 'recommended_next_metadata': [], 'warnings': [], 'errors': [],
}
expected = copy.deepcopy(payload)
validate_report(payload)
report = CanonicalReport.from_dict(payload)
assert report.to_dict() == expected and tuple(report.to_dict()) == sections
assert report.sections['run']['duration_seconds'] == 0
assert report.sections['run']['random_seed'] is None
payload['run']['run_id'] = 'caller-mutated-input'
payload['errors'].append({'invalid': 'caller-only'})
assert report.to_dict() == expected
try:
    report.sections['run']['run_id'] = 'invalid-mutation'
except TypeError:
    pass
else:
    raise AssertionError('nested canonical report is mutable')
try:
    report.sections = {}
except (FrozenInstanceError, AttributeError):
    pass
else:
    raise AssertionError('canonical report attribute is mutable')
exported = report.to_dict()
exported['run']['run_id'] = 'caller-mutated-output'
exported['warnings'].append({'invalid': 'caller-only'})
assert report.to_dict() == expected
schema = report_schema()
assert schema['$schema'] == 'https://json-schema.org/draft/2020-12/schema'
assert schema['type'] == 'object' and schema['additionalProperties'] is False
assert tuple(schema['required']) == sections
schema['required'].clear()
schema['properties'].clear()
fresh = report_schema()
assert tuple(fresh['required']) == sections and tuple(fresh['properties']) == sections
error_payload = copy.deepcopy(expected)
error_payload['run']['run_status'] = 'failed'
error_payload['errors'] = [{
    'code': 'INPUT_PARSE_FAILED', 'severity': 'fatal',
    'message': 'The records artifact could not be parsed.', 'file_role': 'records',
    'field': None, 'record_key': None, 'row_number': None, 'effect_on_run': 'failed',
    'effect_on_capabilities': ['ingestion'], 'remediation': ['Supply a supported local records artifact.'],
}]
validate_report(error_payload)
error_report = CanonicalReport(error_payload)
assert error_report.to_dict() == error_payload
assert error_report.to_dict()['errors'][0]['severity'] == 'fatal'
assert all(error_report.to_dict()[name] == {} for name in (
    'observed_facts', 'derived_metrics', 'proxy_signals', 'simulations'))
for field, value in (('duration_seconds', True), ('duration_seconds', float('inf')), ('unregistered_key', 0)):
    invalid = copy.deepcopy(expected)
    invalid['run'][field] = value
    try:
        CanonicalReport.from_dict(invalid)
    except ValueError:
        pass
    else:
        raise AssertionError('installed canonical report accepted invalid field: ' + field)
assert not blocked_roots.intersection(sys.modules)
assert not any(name == layer or name.startswith(layer + '.') for name in sys.modules for layer in blocked_layers)
print('installed Step 2: empty/error contracts, finite strict validation, immutable detached result/schema; no analysis imports, optional dependencies, file reads or network: PASS')
'''
        subprocess.run([str(python), "-I", "-c", program, str(work), str(ROOT)], cwd=work, check=True)


def phase4_step2_cli_main() -> int:
    parser = argparse.ArgumentParser(description="Phase 4 Step 2 maintainer gate")
    parser.add_argument("--phase", type=int, choices=(4,), required=True)
    parser.add_argument("--step", type=int, choices=(2,), required=True)
    parser.add_argument("--diff", action="store_true")
    parser.add_argument("--junit", type=Path)
    parser.add_argument("--require-parquet", action="store_true")
    parser.add_argument("--minimum-tests", type=int, default=1)
    parser.add_argument("--baseline-evidence", type=Path)
    parser.add_argument("--dist", type=Path)
    parser.add_argument("--smoke-wheel", type=Path)
    parser.add_argument("--candidate", type=Path)
    parser.add_argument("--delivery", type=Path)
    args = parser.parse_args()
    if args.delivery is not None:
        raise ValueError("Phase 4 Step 2 cannot certify a final phase delivery")
    if args.junit is not None:
        verify_junit(args.junit, require_parquet=args.require_parquet, minimum=args.minimum_tests)
    elif args.baseline_evidence is not None:
        phase4_step2_baseline_evidence(args.baseline_evidence)
    elif args.dist is not None:
        audit_phase4_step2(args.step)
        wheel, _ = verify_distributions(args.dist)
        smoke_installed(wheel)
        smoke_installed_duplicates(wheel)
        phase4_step2_installed_contract_smoke(wheel)
    elif args.smoke_wheel is not None:
        smoke_installed(args.smoke_wheel)
    elif args.candidate is not None:
        phase4_step2_candidate(args.candidate, args.step)
    else:
        audit_phase4_step2(args.step)
        if args.diff:
            audit_phase4_step2_diff(args.step)
    return 0


# Phase 4 Step 3 adds pure adapters. All earlier stage gates remain callable.
PHASE4_STEP2_FINAL = "fcea74e2b1858e83cdbfd1b8212d15343d63ff08"
PHASE4_STEP2_TREE = "c3ce887fd393cfc6c18364546005f2b74a63b746"
PHASE4_STEP2_TEST_TREE = "9d6ac0cbf3827ab54c7852503d99d442a3796259"
PHASE4_STEP3_APPROVAL = "开始 **Phase 4 Step 3**"
PHASE4_STEP3_APPROVAL_DATE = "2026-09-19"
PHASE4_STEP3_ALLOWED = {'.github/workflows/ci.yml',
 '.github/workflows/golden.yml',
 '.github/workflows/release.yml',
 '.github/workflows/security.yml',
 'PHASE_4_BASELINE.json',
 'PHASE_4_DECISIONS.md',
 'docs/architecture.md',
 'docs/report_schema.md',
 'docs/theory_traceability.md',
 'scripts/check_spec_consistency.py',
 'scripts/check_traceability.py',
 'scripts/release_check.py',
 'src/recursive_integrity_toolkit/reports/assembly.py',
 'tests/conftest.py',
 'tests/integration/test_ci_workflows.py',
 'tests/integration/test_hero_structure.py',
 'tests/integration/test_license_notices.py',
 'tests/integration/test_no_algorithms.py',
 'tests/integration/test_no_network.py',
 'tests/integration/test_optional_dependency.py',
 'tests/integration/test_owner_ids.py',
 'tests/integration/test_package_import.py',
 'tests/integration/test_package_install.py',
 'tests/integration/test_partial_lineage_report.py',
 'tests/integration/test_partial_provenance_report.py',
 'tests/integration/test_phase4_gates.py',
 'tests/integration/test_prohibited_structure.py',
 'tests/integration/test_repository_structure.py',
 'tests/integration/test_schema_json.py',
 'tests/unit/test_PR012_evidence_classes.py',
 'tests/unit/test_PR014_unavailable.py',
 'tests/unit/test_PR018_language.py',
 'tests/unit/test_phase4_contracts.py'}
PHASE4_STEP3_NEW = ()
PHASE4_STEP3_DOCUMENT_CORRECTIONS = {
    "docs/report_schema.md": [{
        "old": "| `derived_metrics.provenance.weighted_source_type_masses` | number | `user_declared_weight_mass` | `derived_metric` | `PR-005` | `PR-005.source_weight_mass` | 2 | Null only with unavailable reasons |",
        "new": "| `derived_metrics.provenance.weighted_source_type_masses` | category_mass_map | `user_declared_weight_mass` | `derived_metric` | `PR-005` | `PR-005.source_weight_mass` | 2 | Null only with unavailable reasons |",
    }],
}
PHASE4_STEP3_MIGRATIONS = {'tests/integration/test_phase4_gates.py': [{'new': 'def '
                                                    'test_phase4_step2_current_runtime_opens_only_the_canonical_result(repo_root, '
                                                    'phase3_final_snapshot, '
                                                    'phase4_step2_snapshot):\n'
                                                    '    repo_root = phase4_step2_snapshot\n',
                                             'node': 'test_phase4_step2_current_runtime_opens_only_the_canonical_result',
                                             'old': 'def '
                                                    'test_phase4_step2_current_runtime_opens_only_the_canonical_result(repo_root, '
                                                    'phase3_final_snapshot):\n'},
                                            {'new': 'def '
                                                    'test_phase4_step2_current_workflows_preserve_matrix_and_use_active_dispatch(repo_root, '
                                                    'phase4_step2_snapshot):\n'
                                                    '    repo_root = phase4_step2_snapshot\n',
                                             'node': 'test_phase4_step2_current_workflows_preserve_matrix_and_use_active_dispatch',
                                             'old': 'def '
                                                    'test_phase4_step2_current_workflows_preserve_matrix_and_use_active_dispatch(repo_root):\n'},
                                            {'new': 'def '
                                                    'test_phase4_step2_current_snapshot_checks_valid_tree_before_mutations(repo_root, '
                                                    'tmp_path, phase4_gate_tools, mutation, '
                                                    'phase4_step2_snapshot):',
                                             'node': 'test_phase4_step2_current_snapshot_checks_valid_tree_before_mutations',
                                             'old': 'def '
                                                    'test_phase4_step2_current_snapshot_checks_valid_tree_before_mutations(repo_root, '
                                                    'tmp_path, phase4_gate_tools, mutation):'},
                                            {'new': '        shutil.copyfile(phase4_step2_snapshot '
                                                    '/ relative, destination)',
                                             'node': 'test_phase4_step2_current_snapshot_checks_valid_tree_before_mutations',
                                             'old': '        shutil.copyfile(repo_root / relative, '
                                                    'destination)'}],
 'tests/unit/test_phase4_contracts.py': [{'new': 'def '
                                                 'test_phase4_step2_approved_control_keeps_independent_step1_anchors(phase4_tools, '
                                                 'phase4_step2_snapshot):\n'
                                                 '    control = json.loads((phase4_step2_snapshot '
                                                 '/ '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))',
                                          'node': 'test_phase4_step2_approved_control_keeps_independent_step1_anchors',
                                          'old': 'def '
                                                 'test_phase4_step2_approved_control_keeps_independent_step1_anchors(phase4_tools):\n'
                                                 '    control = json.loads((ROOT / '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))'},
                                         {'new': 'def '
                                                 'test_phase4_step2_control_rejects_forged_scope_and_stage(phase4_tools, '
                                                 'field, value, phase4_step2_snapshot):\n'
                                                 '    control = json.loads((phase4_step2_snapshot '
                                                 '/ '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))',
                                          'node': 'test_phase4_step2_control_rejects_forged_scope_and_stage',
                                          'old': 'def '
                                                 'test_phase4_step2_control_rejects_forged_scope_and_stage(phase4_tools, '
                                                 'field, value):\n'
                                                 '    control = json.loads((ROOT / '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))'},
                                         {'new': 'def '
                                                 'test_phase4_step2_control_rejects_unapproved_dispatch(phase4_tools, '
                                                 'step, phase4_step2_snapshot):\n'
                                                 '    control = json.loads((phase4_step2_snapshot '
                                                 '/ '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))',
                                          'node': 'test_phase4_step2_control_rejects_unapproved_dispatch',
                                          'old': 'def '
                                                 'test_phase4_step2_control_rejects_unapproved_dispatch(phase4_tools, '
                                                 'step):\n'
                                                 '    control = json.loads((ROOT / '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))'},
                                         {'new': 'def '
                                                 'test_phase4_step2_control_requires_explicit_approval_fields(phase4_tools, '
                                                 'field, phase4_step2_snapshot):\n'
                                                 '    control = json.loads((phase4_step2_snapshot '
                                                 '/ '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))',
                                          'node': 'test_phase4_step2_control_requires_explicit_approval_fields',
                                          'old': 'def '
                                                 'test_phase4_step2_control_requires_explicit_approval_fields(phase4_tools, '
                                                 'field):\n'
                                                 '    control = json.loads((ROOT / '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))'},
                                         {'new': 'def '
                                                 'test_phase4_step2_control_cannot_mint_extra_permission(phase4_tools, '
                                                 'phase4_step2_snapshot):\n'
                                                 '    control = json.loads((phase4_step2_snapshot '
                                                 '/ '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))',
                                          'node': 'test_phase4_step2_control_cannot_mint_extra_permission',
                                          'old': 'def '
                                                 'test_phase4_step2_control_cannot_mint_extra_permission(phase4_tools):\n'
                                                 '    control = json.loads((ROOT / '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))'},
                                         {'new': 'def '
                                                 'test_phase4_step2_historical_migrations_are_five_explicit_step1_bindings(phase4_tools, '
                                                 'phase4_step1_snapshot, phase4_step2_snapshot):',
                                          'node': 'test_phase4_step2_historical_migrations_are_five_explicit_step1_bindings',
                                          'old': 'def '
                                                 'test_phase4_step2_historical_migrations_are_five_explicit_step1_bindings(phase4_tools, '
                                                 'phase4_step1_snapshot):'},
                                         {'new': 'def '
                                                 'test_phase4_step2_historical_guard_rejects_assertion_and_binding_weakening(phase4_tools, '
                                                 'phase4_step1_snapshot, mutation, '
                                                 'phase4_step2_snapshot):',
                                          'node': 'test_phase4_step2_historical_guard_rejects_assertion_and_binding_weakening',
                                          'old': 'def '
                                                 'test_phase4_step2_historical_guard_rejects_assertion_and_binding_weakening(phase4_tools, '
                                                 'phase4_step1_snapshot, mutation):'},
                                         {'new': '            path, (phase4_step1_snapshot / '
                                                 'path).read_bytes(), (phase4_step2_snapshot / '
                                                 'path).read_bytes(),',
                                          'node': 'test_phase4_step2_historical_migrations_are_five_explicit_step1_bindings',
                                          'old': '            path, (phase4_step1_snapshot / '
                                                 'path).read_bytes(), (ROOT / path).read_bytes(),'},
                                         {'new': '    before = (phase4_step1_snapshot / '
                                                 'path).read_bytes()\n'
                                                 '    after = (phase4_step2_snapshot / '
                                                 'path).read_bytes()',
                                          'node': 'test_phase4_step2_historical_guard_rejects_assertion_and_binding_weakening',
                                          'old': '    before = (phase4_step1_snapshot / '
                                                 'path).read_bytes()\n'
                                                 '    after = (ROOT / path).read_bytes()'}]}


def _phase4_step2_files():
    """Read the exact accepted Step 2 Git tree and verify every blob identity."""
    for suffix, expected in (("^{commit}", PHASE4_STEP2_FINAL), ("^{tree}", PHASE4_STEP2_TREE),
                             (":tests", PHASE4_STEP2_TEST_TREE)):
        if git("rev-parse", PHASE4_STEP2_FINAL + suffix).decode().strip() != expected:
            raise ValueError("Pinned Phase 4 Step 2 identity mismatch")
    objects = {}
    for entry in git("ls-tree", "-rz", PHASE4_STEP2_FINAL).split(b"\0"):
        if not entry:
            continue
        metadata, raw_path = entry.split(b"\t", 1)
        mode, kind, oid = metadata.split()
        path = raw_path.decode("utf-8")
        if (mode not in (b"100644", b"100755") or kind != b"blob" or path in objects
                or path.startswith("/") or ".." in path.split("/") or ".git" in path.split("/")):
            raise ValueError("Unsafe pinned Step 2 Git object")
        objects[path] = oid.decode("ascii")
    if len(objects) != 227:
        raise ValueError("Pinned Step 2 must contain exactly 227 files")
    files = {}
    with zipfile.ZipFile(io.BytesIO(git("archive", "--format=zip", PHASE4_STEP2_FINAL))) as archive:
        names = [item.filename for item in archive.infolist() if not item.is_dir()]
        if len(names) != len(objects) or set(names) != set(objects):
            raise ValueError("Pinned Step 2 archive identity mismatch")
        for name in names:
            raw = archive.read(name)
            oid = hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()
            if oid != objects[name]:
                raise ValueError(f"Pinned Step 2 blob mismatch: {name}")
            files[name] = raw
    return MappingProxyType(files)


def phase4_step3_expected_control() -> dict:
    """Actual Step 3 approval is independent of the mutable control document."""
    prior = _phase4_step2_files()
    result = phase4_step2_expected_control()
    result.pop("previous_step_local_commit")
    result.update({
        "control_version": "1.2", "active_step": 3,
        "approval_date": PHASE4_STEP3_APPROVAL_DATE, "approval_basis": PHASE4_STEP3_APPROVAL,
        "previous_step_commit": PHASE4_STEP2_FINAL,
        "previous_step_tree": PHASE4_STEP2_TREE,
        "previous_step_test_tree": PHASE4_STEP2_TEST_TREE,
        "previous_step_core_tests": 2728, "previous_step_parquet_tests": 2731,
        "previous_step_files_sha256": {p: hashlib.sha256(raw).hexdigest() for p, raw in sorted(prior.items())},
        "permitted_paths": sorted(PHASE4_STEP3_ALLOWED), "new_files_permitted": [],
        "runtime_changes_authorized": True, "schema_changes_authorized": False,
        "runtime_paths_authorized": ["src/recursive_integrity_toolkit/reports/assembly.py"],
        "schema_paths_authorized": [],
        "step2_historical_binding_nodes": {p: sorted({r["node"] for r in rows})
                                          for p, rows in sorted(PHASE4_STEP3_MIGRATIONS.items())},
    })
    return result


def verify_phase4_step3_control(control: dict, step: int = 3) -> None:
    if type(step) is not int or step != 3 or type(control) is not dict:
        raise ValueError("Unsupported Phase 4 Step 3 stage/control")
    try:
        actual = json.dumps(control, sort_keys=True, ensure_ascii=True, allow_nan=False)
        expected = json.dumps(phase4_step3_expected_control(), sort_keys=True, ensure_ascii=True, allow_nan=False)
    except (TypeError, ValueError) as error:
        raise ValueError("Invalid Phase 4 Step 3 control") from error
    if actual != expected:
        raise ValueError("Phase 4 control differs from the independently approved Step 3 contract")


def verify_phase4_step3_changes(changes: list[tuple[str, str]]) -> None:
    seen = set()
    for status, path in changes:
        if path in seen or path not in PHASE4_STEP3_ALLOWED or status != "M":
            raise ValueError(f"Unapproved Phase 4 Step 3 path/operation: {status} {path}")
        seen.add(path)


def _phase4_step3_header(node, path):
    """Allow explicit test parametrization/fixtures, never definition-time effects."""
    for decorator in node.decorator_list:
        if not isinstance(decorator, ast.Call) or ast.unparse(decorator.func) not in {
                "pytest.fixture", "pytest.mark.parametrize"}:
            raise ValueError(f"Unapproved Step 3 test decorator: {path}:{node.name}")
        if ast.unparse(decorator.func) == "pytest.fixture" and not node.name.startswith("phase4_step"):
            raise ValueError("A Step 3 fixture must have an explicit scoped name")
        if any(keyword.arg is None for keyword in decorator.keywords):
            raise ValueError("Decorator expansion is outside the Step 3 contract")
        for value in [*decorator.args, *(keyword.value for keyword in decorator.keywords)]:
            try:
                ast.literal_eval(value)
            except (ValueError, TypeError, SyntaxError) as error:
                raise ValueError("Step 3 decorator arguments must be literal") from error
    clone = ast.parse(ast.unparse(node)).body[0]
    clone.decorator_list = []
    _phase4_preserve_function_header(clone, path)


def _phase4_step3_append_only(before: bytes, after: bytes, path: str) -> None:
    if not after.startswith(before):
        raise ValueError(f"Inherited Step 2 prefix changed: {path}")
    old, new = ast.parse(before), ast.parse(after)
    bindings = set()
    for node in old.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            bindings.add(node.name)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            bindings.update(alias.asname or alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            bindings.update(child.id for target in targets for child in ast.walk(target) if isinstance(child, ast.Name))
    for node in new.body[len(old.body):]:
        if not isinstance(node, ast.FunctionDef) or node.name in bindings:
            raise ValueError(f"Step 3 addition executes, rebinds or shadows inherited source: {path}")
        allowed_snapshot = path == "tests/conftest.py" and node.name == "phase4_step2_snapshot"
        if not allowed_snapshot and not node.name.startswith(("test_phase4_step3_", "phase4_step3_")):
            raise ValueError(f"Step 3 added test/helper is not explicitly scoped: {path}:{node.name}")
        if path == "tests/conftest.py" and node.name != "phase4_step2_snapshot":
            raise ValueError("Only the pinned Step 2 shared fixture is authorized")
        bindings.add(node.name)
        _phase4_step3_header(node, path)


def verify_phase4_step3_test_migration(path: str, before: bytes, after: bytes) -> None:
    prior = _phase4_step2_files()
    if path not in prior or path not in PHASE4_STEP3_ALLOWED or before != prior[path] or not path.startswith("tests/"):
        raise ValueError("Step 3 migration requires the exact named Step 2 source")
    _phase4_step3_check_test_migration(path, before, after)


def _phase4_step3_check_test_migration(path: str, before: bytes, after: bytes) -> None:
    """Check a source already read from the verified Step 2 immutable mapping."""
    expected = before
    for row in PHASE4_STEP3_MIGRATIONS.get(path, []):
        old, new = row["old"].encode(), row["new"].encode()
        if expected.count(old) != 1:
            raise ValueError("Step 2 historical binding is not unique")
        expected = expected.replace(old, new, 1)
    _phase4_step3_append_only(expected, after, path)


def _phase4_step3_preserve_tooling(before: bytes, after: bytes, path: str) -> None:
    """Permit the exact Step 3 dispatch addition and preserve every older statement."""
    if path == "scripts/release_check.py":
        old = ('def cli_main() -> int:\n'
               '    argv = sys.argv[1:]\n'
               '    explicit_phase4 = "--phase=4" in argv or any(a == "--phase" and b == "4" for a, b in zip(argv, argv[1:]))\n'
               '    explicit_step2 = "--step=2" in argv or any(a == "--step" and b == "2" for a, b in zip(argv, argv[1:]))\n'
               '    if explicit_phase4 and explicit_step2:\n'
               '        return phase4_step2_cli_main()\n'
               '    return phase4_cli_main() if explicit_phase4 else main()')
        new = old.replace('    return phase4_cli_main() if explicit_phase4 else main()',
                          '    explicit_step3 = "--step=3" in argv or any(a == "--step" and b == "3" for a, b in zip(argv, argv[1:]))\n'
                          '    if explicit_phase4 and explicit_step3:\n'
                          '        return phase4_step3_cli_main()\n'
                          '    return phase4_cli_main() if explicit_phase4 else main()')
        replacements = [(old, new)]
    else:
        old = '    if args.phase == 4 and args.step == 2:\n        return phase4_step2_main(step=args.step)\n'
        new = old + '    if args.phase == 4 and args.step == 3:\n        return phase4_step3_main(step=args.step)\n'
        replacements = [(old, new),
                        ('Choose explicit --phase 3 --step 11 or --phase 4 --step 1 or --phase 4 --step 2',
                         'Choose explicit --phase 3 --step 11 or --phase 4 --step 1 or --phase 4 --step 2 or --phase 4 --step 3')]
    expected = before
    for old, new in replacements:
        if expected.count(old.encode()) != 1:
            raise ValueError(f"Historical dispatcher identity mismatch: {path}")
        expected = expected.replace(old.encode(), new.encode(), 1)
    _phase4_preserve_tooling(expected, after, path)


def verify_phase4_step3_snapshot(root: Path = ROOT) -> dict:
    prior = _phase4_step2_files()
    for path, raw in prior.items():
        target = root / path
        if not target.is_file() or target.is_symlink():
            raise ValueError(f"Missing or aliased inherited Step 2 file: {path}")
        current = target.read_bytes()
        if path not in PHASE4_STEP3_ALLOWED and current != raw:
            raise ValueError(f"Protected Step 2 bytes changed: {path}")
        if path.startswith("tests/") and path in PHASE4_STEP3_ALLOWED:
            _phase4_step3_check_test_migration(path, raw, current)
        elif path.startswith("scripts/") and path in PHASE4_STEP3_ALLOWED:
            _phase4_step3_preserve_tooling(raw, current, path)
        elif path in {"docs/architecture.md", "docs/theory_traceability.md", "docs/report_schema.md", "PHASE_4_DECISIONS.md"}:
            expected = raw
            for correction in PHASE4_STEP3_DOCUMENT_CORRECTIONS.get(path, []):
                old, new = correction["old"].encode(), correction["new"].encode()
                if expected.count(old) != 1:
                    raise ValueError(f"Historical documentation correction is not unique: {path}")
                expected = expected.replace(old, new, 1)
            if not current.startswith(expected):
                raise ValueError(f"Step 2 historical documentation prefix changed: {path}")
    actual_modules = {p.relative_to(root).as_posix() for p in (root / "src/recursive_integrity_toolkit").rglob("*.py")}
    expected_modules = {p for p in prior if p.startswith("src/") and p.endswith(".py")}
    if actual_modules != expected_modules or len(actual_modules) != 40:
        raise ValueError("Step 3 cannot change the runtime module set")
    if {p.name for p in (root / "schemas").iterdir()} != {Path(p).name for p in prior if p.startswith("schemas/")}:
        raise ValueError("Step 3 cannot change the schema set")
    if hashlib.sha256((root / "PHASE_4_PLAN.md").read_bytes()).hexdigest() != PHASE4_PLAN_SHA256:
        raise ValueError("Approved Phase 4 plan changed")
    verify_phase4_step3_control(json.loads((root / "PHASE_4_BASELINE.json").read_text(encoding="utf-8")))
    decisions = (root / "PHASE_4_DECISIONS.md").read_text(encoding="utf-8")
    if PHASE4_STEP3_APPROVAL not in decisions or PHASE4_STEP2_FINAL not in decisions:
        raise ValueError("Actual Step 3 authorization or Step 2 evidence anchor missing")
    if any((root / name).exists() for name in PHASE4_FORBIDDEN_OUTPUTS):
        raise ValueError("Step 3 cannot create Phase 4 completion records or audit outputs")
    import runpy
    checker = runpy.run_path(str(root / "scripts/check_traceability.py"), run_name="phase4_step3_assembly_boundary")
    checker["phase4_step2_result_boundary"](root / "src/recursive_integrity_toolkit/result.py")
    checker["phase4_step3_assembly_boundary"](root / "src/recursive_integrity_toolkit/reports/assembly.py")
    schema_bytes = (root / "schemas/report.schema.json").read_bytes()
    if hashlib.sha256(schema_bytes).hexdigest() != PHASE4_STEP2_REPORT_SCHEMA_SHA256:
        raise ValueError("Step 3 report schema differs from its independently reviewed bytes")
    schema = json.loads(schema_bytes)
    if (schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema"
            or schema.get("type") != "object" or schema.get("additionalProperties") is not False):
        raise ValueError("Step 3 report schema dialect/closed root mismatch")
    return {"package_modules": 40, "frozen_runtime_modules": 39, "frozen_schemas": 5,
            "hero_files_unchanged": 6, "historical_phase3_migrated_nodes": 16,
            "phase_complete": False, "result_contracts_enabled": True,
            "adapters_enabled": True, "cli_analysis_enabled": False}


def audit_phase4_step3(step: int = 3) -> dict:
    verify_phase4_step3_control(json.loads((ROOT / "PHASE_4_BASELINE.json").read_text(encoding="utf-8")), step)
    result = {"phase": 4, "active_step": step, **verify_phase4_step3_snapshot(),
              "phase0_hashes_verified": 16, "publication_authorized": False}
    print(json.dumps(result, indent=2))
    return result


def audit_phase4_step3_diff(step: int = 3) -> dict:
    if type(step) is not int or step != 3:
        raise ValueError("Unsupported Phase 4 Step 3 stage")
    _phase4_step2_files()
    subprocess.run(["git", "-C", str(ROOT), "merge-base", "--is-ancestor", PHASE4_STEP2_FINAL, "HEAD"], check=True)
    raw = git("diff", "--name-status", "--no-renames", "-z", PHASE4_STEP2_FINAL, "--").split(b"\0")
    raw = [part.decode("utf-8") for part in raw if part]
    if len(raw) % 2:
        raise ValueError("Malformed Step 3 Git difference records")
    changes = list(zip(raw[::2], raw[1::2]))
    changes.extend(("A", p.decode()) for p in git("ls-files", "--others", "--exclude-standard", "-z").split(b"\0") if p)
    verify_phase4_step3_changes(changes)
    result = {"previous_step_commit": PHASE4_STEP2_FINAL, "changed_files": len(changes),
              "changes": changes, "step": 3, "scope": "PASS"}
    print(json.dumps(result, indent=2))
    return result


def phase4_step3_baseline_evidence(output: Path) -> dict:
    """Reconcile all inherited identities, including the accepted Step 2 suite."""
    output.mkdir(parents=True, exist_ok=True)
    inherited = phase4_step2_baseline_evidence(output / "phase4-step2-inherited")
    with tempfile.TemporaryDirectory(prefix="rit-p4-step2-identities-") as temp:
        baseline = Path(temp)
        for name, raw in _phase4_step2_files().items():
            target = baseline / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(raw)
        old, old_log = _collect(baseline)
    current, current_log = _collect(ROOT)
    expected = 2731 if os.environ.get("RIT_TEST_PARQUET") == "1" else 2728
    if len(old) != expected or set(old) - set(current):
        raise ValueError("Accepted Phase 4 Step 2 test identities were lost")
    result = {"baseline_commit": PHASE4_STEP2_FINAL, "baseline_test_tree": PHASE4_STEP2_TEST_TREE,
              "baseline_nodeids": old, "current_nodeids": current, "missing_nodeids": [],
              "baseline_tests": len(old), "current_tests": len(current), "inherited": inherited,
              "nodeids_sha256": hashlib.sha256(("\n".join(old)+"\n").encode()).hexdigest()}
    (output / "phase4_step3_test_identity_manifest.json").write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    (output / "phase4-step2-collection.log").write_text(old_log, encoding="utf-8")
    (output / "phase4-step3-collection.log").write_text(current_log, encoding="utf-8")
    print(json.dumps({k: result[k] for k in ("baseline_tests", "current_tests", "missing_nodeids")}, indent=2))
    return result


def phase4_step3_candidate(output: Path, step: int = 3) -> None:
    """Build tested Step 3 intermediate evidence without declaring Phase 4 complete."""
    if os.environ.get("RIT_TEST_PARQUET") != "1" or importlib.util.find_spec("pyarrow") is None:
        raise ValueError("Step 3 candidate evidence requires RIT_TEST_PARQUET=1 and real PyArrow")
    output.mkdir(parents=True, exist_ok=True)
    result = audit_phase4_step3(step)
    result["diff"] = audit_phase4_step3_diff(step)
    if git("status", "--porcelain").strip():
        raise ValueError("Step 3 candidate archive requires committed, clean source")
    result["core"] = verify_junit(output / "core.xml", minimum=2728)
    result["parquet"] = verify_junit(output / "parquet.xml", require_parquet=True, minimum=2731)
    result["core_math_measurements"] = verify_step10_evidence(output / "core.xml", output / "phase4-step3-core-observations.json")
    result["parquet_math_measurements"] = verify_step10_evidence(output / "parquet.xml", output / "phase4-step3-parquet-observations.json")
    identity = phase4_step3_baseline_evidence(output)
    result["test_identity"] = {k: identity[k] for k in ("baseline_tests", "current_tests", "nodeids_sha256")}
    expected = set()
    for node in identity["current_nodeids"]:
        base, bracket, parameter = node.partition("[")
        owner, name = base.rsplit("::", 1)
        expected.add((owner.removesuffix(".py").replace("/", ".").replace("::", "."), name + bracket + parameter))
    for name, parquet in (("core.xml", False), ("parquet.xml", True)):
        cases = {(c.get("classname", ""), c.get("name", "")) for c in ET.parse(output / name).getroot().iter("testcase")}
        target = expected if parquet else {c for c in expected if c[1] not in PARQUET_CASES}
        if cases != target:
            raise ValueError(f"Step 3 JUnit does not execute the entire current suite: {name}")
    wheel, _ = verify_distributions(output / "dist")
    phase4_step2_installed_contract_smoke(wheel)
    phase4_step3_installed_assembly_smoke(wheel)
    archive = output / "recursive-integrity-toolkit-phase4-step3-candidate.zip"
    subprocess.run(["git", "-C", str(ROOT), "archive", "--format=zip", "--prefix=recursive-integrity-toolkit/", "HEAD", "-o", str(archive.resolve())], check=True)
    tracked = {p for p in git("ls-files", "-z").decode().split("\0") if p}
    with zipfile.ZipFile(archive) as zipped:
        names = {p.removeprefix("recursive-integrity-toolkit/") for p in zipped.namelist() if not p.endswith("/")}
        if names != tracked or len(tracked) != 227:
            raise ValueError("Step 3 source archive file set mismatch")
        for name in names:
            if zipped.read("recursive-integrity-toolkit/"+name) != (ROOT / name).read_bytes():
                raise ValueError(f"Step 3 source archive byte mismatch: {name}")
    result.update({"commit": git("rev-parse", "HEAD").decode().strip(),
                   "tree": git("rev-parse", "HEAD^{tree}").decode().strip(),
                   "source_archive": archive.name, "tracked_files": len(tracked),
                   "python": sys.version, "platform": sys.platform,
                   "versions": {name: importlib.metadata.version(name) for name in ("numpy", "pandas", "pytest")}})
    (output / "phase4_step3_execution_metadata.json").write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    (output / "phase4_step3_repository_files.sha256").write_text("".join(f"{hashlib.sha256((ROOT/name).read_bytes()).hexdigest()}  {name}\n" for name in sorted(tracked)), encoding="utf-8")
    paths = sorted(p for p in output.rglob("*") if p.is_file() and p.name != "phase4_step3_artifacts.sha256")
    (output / "phase4_step3_artifacts.sha256").write_text("".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(output).as_posix()}\n" for p in paths), encoding="utf-8")
    print(f"Phase 4 Step 3 candidate: {len(tracked)} source files verified; Phase 4 remains incomplete.")


def phase4_step3_cli_main() -> int:
    parser = argparse.ArgumentParser(description="Phase 4 Step 3 maintainer gate")
    parser.add_argument("--phase", type=int, choices=(4,), required=True)
    parser.add_argument("--step", type=int, choices=(3,), required=True)
    parser.add_argument("--diff", action="store_true")
    parser.add_argument("--junit", type=Path)
    parser.add_argument("--require-parquet", action="store_true")
    parser.add_argument("--minimum-tests", type=int, default=1)
    parser.add_argument("--baseline-evidence", type=Path)
    parser.add_argument("--dist", type=Path)
    parser.add_argument("--smoke-wheel", type=Path)
    parser.add_argument("--candidate", type=Path)
    parser.add_argument("--delivery", type=Path)
    args = parser.parse_args()
    if args.delivery is not None:
        raise ValueError("Phase 4 Step 3 cannot certify a final phase delivery")
    if args.junit is not None:
        verify_junit(args.junit, require_parquet=args.require_parquet, minimum=args.minimum_tests)
    elif args.baseline_evidence is not None:
        phase4_step3_baseline_evidence(args.baseline_evidence)
    elif args.dist is not None:
        audit_phase4_step3(args.step)
        wheel, _ = verify_distributions(args.dist)
        smoke_installed(wheel)
        smoke_installed_duplicates(wheel)
        phase4_step2_installed_contract_smoke(wheel)
        phase4_step3_installed_assembly_smoke(wheel)
    elif args.smoke_wheel is not None:
        smoke_installed(args.smoke_wheel)
    elif args.candidate is not None:
        phase4_step3_candidate(args.candidate, args.step)
    else:
        audit_phase4_step3(args.step)
        if args.diff:
            audit_phase4_step3_diff(args.step)
    return 0


def phase4_step3_installed_assembly_smoke(wheel: Path) -> None:
    """Exercise an installed, hand-authored typed handoff with every effect blocked."""
    with tempfile.TemporaryDirectory(prefix="rit-p4-step3-installed-assembly-") as temp:
        work = Path(temp)
        subprocess.run([sys.executable, "-m", "venv", str(work / "venv")], check=True)
        bindir = work / "venv" / ("Scripts" if os.name == "nt" else "bin")
        python = bindir / ("python.exe" if os.name == "nt" else "python")
        subprocess.run([str(python), "-m", "pip", "install", "--no-index", "--no-deps", str(wheel.resolve())],
                       cwd=work, check=True)
        program = '''import builtins, copy, importlib.abc, io, json, socket, sys
from dataclasses import replace
from pathlib import Path
from types import MappingProxyType
blocked_roots = {'numpy', 'pandas', 'pyarrow', 'jsonschema', 'referencing', 'networkx', 'scipy', 'sklearn'}
blocked_import_layers = tuple('recursive_integrity_toolkit.' + name for name in (
    'cli', 'reports.json_report', 'reports.markdown_report', 'reports.html_report'))
class DenyAnalysis(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in blocked_roots or any(
                fullname == layer or fullname.startswith(layer + '.') for layer in blocked_import_layers):
            raise AssertionError('installed assembly attempted optional, CLI or renderer import: ' + fullname)
sys.meta_path.insert(0, DenyAnalysis())
def blocked(*args, **kwargs):
    raise AssertionError('installed assembly attempted file or network access')
socket.create_connection = blocked
socket.getaddrinfo = blocked
socket.socket.connect = blocked
socket.socket.connect_ex = blocked
from recursive_integrity_toolkit.models import (
    BundleValidationResult, Capability, CapabilityKey, CapabilityStatus,
    CanonicalRow, FileFormat, FileInventoryEntry, FileRole, ProvenanceMatch, RecordKey, RowLocation,
    ObservabilityAssessment, ProvenanceJoinResult, ValidationCoverage,
    ValidationMessage, ValidationSeverity, VersionOrderResult,
)
import recursive_integrity_toolkit.reports.assembly as assembly
from recursive_integrity_toolkit.result import CanonicalReport
assert Path(assembly.__file__).resolve().is_relative_to(Path(sys.argv[1]) / 'venv')
assert not Path(assembly.__file__).resolve().is_relative_to(Path(sys.argv[2]) / 'src')
# Prepare real installed-kernel evidence before enabling the assembly execution barrier.
from recursive_integrity_toolkit.config import RepresentationConfig
from recursive_integrity_toolkit.representations.field import assign_field_states
from recursive_integrity_toolkit.metrics.diversity import calculate_state_distribution
rows = tuple(CanonicalRow('records', RecordKey('v1', identifier),
             MappingProxyType({'dataset_version': 'v1', 'record_id': identifier,
                               'content': 'synthetic installed fixture', 'topic': topic}),
             MappingProxyType({}), MappingProxyType({}),
             location=RowLocation(FileRole.RECORDS_PRIMARY, 'fixture.jsonl', index, index))
             for index, (identifier, topic) in enumerate((('a', 'one'), ('b', 'two')), 1))
represented = assign_field_states(rows, dataset_versions=('v1',), scope_id='installed:v1',
    config=RepresentationConfig('topic', 'topic_field', 'topic', 'installed-fixture-v1', 'error'))
distribution = calculate_state_distribution(represented)
expected_support = distribution.unweighted.support_size.value
expected_diversity = distribution.unweighted.gini_simpson_diversity.value
expected_concentration = distribution.unweighted.simpson_concentration.value
assert (expected_support, expected_diversity, expected_concentration) == (2, 0.5, 0.5)
record_keys = tuple(row.record_key for row in rows)
empirical_coverage = ValidationCoverage(0, 2, 'all_valid_records')
empirical_join = ProvenanceJoinResult(('v1',), record_keys, False,
    tuple(ProvenanceMatch(key, None) for key in record_keys), record_keys,
    empirical_coverage, empirical_coverage, empirical_coverage, ())
empirical_caps = {key: Capability(CapabilityStatus.UNAVAILABLE, reason_codes=('R_MISSING_EVIDENCE',))
                  for key in CapabilityKey}
empirical_caps[CapabilityKey.INGESTION] = Capability(CapabilityStatus.AVAILABLE)
empirical_caps[CapabilityKey.CONTENT_DIAGNOSTICS] = Capability(CapabilityStatus.AVAILABLE)
empirical_bundle = BundleValidationResult(
    inventory=(FileInventoryEntry(FileRole.RECORDS_PRIMARY, Path('fixture.jsonl'), FileFormat.JSONL,
                                  128, '0' * 64, 2, ('dataset_version', 'record_id', 'content', 'topic')),),
    records=rows, provenance=None, provenance_join=empirical_join,
    version_order=VersionOrderResult(('v1',), ('v1',), 'single_version', {}, {}), generation=None,
    observability=ObservabilityAssessment(1, empirical_caps), mapping_traces=(), content_read_keys=(),
    validation_messages=(),
)
# Result type imports are permitted; executing a calculation or input operation is not.
def deny_execution(frame, event, argument):
    if event == 'call':
        source = frame.f_code.co_filename.replace(chr(92), '/')
        if any('/recursive_integrity_toolkit/' + layer + '/' in source for layer in (
                'metrics', 'io', 'representations', 'observability', 'lineage')):
            raise AssertionError('installed assembly executed an analytical/input function: ' + frame.f_code.co_name)
sys.setprofile(deny_execution)
builtins.open = blocked
io.open = blocked
def deny_effects(event, arguments):
    if event in ('open', 'os.listdir', 'os.scandir', 'os.system', 'subprocess.Popen') or event.startswith('socket.'):
        raise AssertionError('installed assembly attempted an external effect: ' + event)
sys.addaudithook(deny_effects)
coverage = ValidationCoverage(0, 0, 'all_valid_records')
join = ProvenanceJoinResult((), (), False, (), (), coverage, coverage, coverage, ())
observability = ObservabilityAssessment(0, {
    key: Capability(CapabilityStatus.UNAVAILABLE, reason_codes=('R_EMPTY_SCOPE',))
    for key in CapabilityKey
})
bundle = BundleValidationResult(
    inventory=(), records=(), provenance=None, provenance_join=join,
    version_order=VersionOrderResult((), (), 'not_available', {}, {}), generation=None,
    observability=observability, mapping_traces=(), content_read_keys=(), validation_messages=(),
)
run = {
    'run_id': 'installed-typed-empty-case', 'toolkit_version': '0.1.0.dev2',
    'report_schema_version': '1.0', 'started_at': None, 'completed_at': None,
    'duration_seconds': None, 'python_version': None, 'platform': None,
    'command': None, 'config_hash': None, 'random_seed': None,
    'strict_mode': False, 'redacted_mode': False, 'network_call_count': 0,
    'deterministic': True, 'privacy_mode': 'standard', 'run_status': 'complete',
    'null_reasons': {
        'started_at': 'Pure assembly does not start a clock.',
        'completed_at': 'Pure assembly does not start a clock.',
        'duration_seconds': 'Pure assembly does not measure execution.',
        'python_version': 'No execution environment is asserted.',
        'platform': 'No execution environment is asserted.',
        'command': 'Direct installed Python API, no command invoked.',
        'config_hash': 'No resolved configuration hash was supplied.',
        'random_seed': 'No stochastic scenario was requested.',
    },
}
original_run = copy.deepcopy(run)
report = assembly.assemble_report(bundle, run=run)
assert type(report) is CanonicalReport
payload = report.to_dict()
assert tuple(payload) == ('run', 'inputs', 'observability', 'capabilities', 'observed_facts',
                         'derived_metrics', 'proxy_signals', 'simulations', 'unavailable_conclusions',
                         'recommended_next_metadata', 'warnings', 'errors')
assert payload['run'] == original_run and run == original_run
assert payload['inputs']['scope']['record_count'] == 0
assert payload['inputs']['artifacts'] == [] and payload['inputs']['file_hashes'] == []
assert payload['simulations'] == {} and payload['errors'] == []
assert payload['capabilities']['lineage']['execution_status'] == 'deferred'
assert report.sections['observability']['capabilities'] is report.sections['capabilities']
assert {'model_performance_decline', 'causal_ancestor_effect', 'universal_integrity',
        'universal_collapse_prediction'} <= {item['conclusion'] for item in payload['unavailable_conclusions']}
for name in ('provenance_row_coverage', 'provenance_required_field_coverage', 'grounding_field_coverage'):
    field = payload['observed_facts']['provenance'][name]
    assert field['value'] is None and field['status'] == 'unavailable'
    assert field['denominator'] == 0 and field['reason_codes']
assert assembly.assemble_report(bundle, run=run).to_dict() == payload
empirical = assembly.assemble_report(empirical_bundle, run=run, distributions=(distribution,)).to_dict()
assert empirical['observed_facts']['record_counts']['v1']['value'] == 2
assert empirical['derived_metrics']['support']['by_version']['v1']['support_size']['value'] == expected_support
assert empirical['derived_metrics']['diversity']['by_version']['v1']['gini_simpson_diversity']['value'] == expected_diversity
assert empirical['derived_metrics']['diversity']['by_version']['v1']['simpson_concentration']['value'] == expected_concentration
assert empirical['simulations'] == {} and empirical['errors'] == []
assert empirical['capabilities']['content_diagnostics']['execution_status'] == 'completed'
assert 'synthetic installed fixture' not in json.dumps(empirical)
run['run_id'] = 'caller-input-mutation'
payload['unavailable_conclusions'].clear()
assert report.to_dict()['run']['run_id'] == original_run['run_id']
assert report.to_dict()['unavailable_conclusions']
failure = ValidationMessage('E_FILE_PARSE', ValidationSeverity.FATAL,
                            'The supplied records artifact could not be parsed.')
failed_bundle = replace(bundle, validation_messages=(failure,))
failed = assembly.assemble_report(failed_bundle, run=original_run).to_dict()
assert failed['run']['run_status'] == 'failed'
assert len(failed['errors']) == 1
assert failed['errors'][0]['code'] == 'E_FILE_PARSE'
assert failed['errors'][0]['severity'] == 'fatal'
assert failed['errors'][0]['effect_on_run'] == 'failed'
assert failed['simulations'] == {}
assert failed['capabilities']['ingestion']['execution_status'] == 'failed'
for supplied in ({}, object()):
    try:
        assembly.assemble_report(supplied, run=original_run)
    except assembly.ReportAssemblyError:
        pass
    else:
        raise AssertionError('installed assembly accepted an untyped validation handoff')
for changes in ({'privacy_mode': 'redacted', 'redacted_mode': True}, {'duration_seconds': float('inf')}):
    invalid = dict(original_run)
    invalid.update(changes)
    try:
        assembly.assemble_report(bundle, run=invalid)
    except ValueError:
        pass
    else:
        raise AssertionError('installed assembly accepted an invalid run declaration')
assert not blocked_roots.intersection(sys.modules)
assert not any(name == layer or name.startswith(layer + '.') for name in sys.modules for layer in blocked_import_layers)
sys.setprofile(None)
print('installed Step 3: typed empty/error and prepared empirical handoffs, exact kernel values, null coverage, immutable mirror, deterministic disclosures, no default scenarios; analytical execution, optional imports, file I/O and network blocked during assembly: PASS')
'''
        subprocess.run([str(python), "-I", "-c", program, str(work), str(ROOT)], cwd=work, check=True)


# Phase 4 Step 4 adds explicit privacy views without changing inherited gates.
PHASE4_STEP3_FINAL = "974545c456e535ba1e1c5b6bf4ae0ce25bc04b57"
PHASE4_STEP3_TREE = "15498f3f00d0ce048c3cba2156eb7a44f096ae88"
PHASE4_STEP3_TEST_TREE = "17b87858f77ee4413c98cfd76f16f52170246741"
PHASE4_STEP4_APPROVAL = "继续"
PHASE4_STEP4_APPROVAL_DATE = "2026-09-19"
PHASE4_STEP4_NEW = ()
PHASE4_STEP4_MIGRATIONS = {'tests/integration/test_phase4_gates.py': [{'new': 'def '
                                                    'test_phase4_step3_current_runtime_opens_only_assembly_and_freezes_schema(repo_root, '
                                                    'phase4_step2_snapshot, '
                                                    'phase4_step3_snapshot):\n'
                                                    '    repo_root = '
                                                    'phase4_step3_snapshot\n',
                                             'node': 'test_phase4_step3_current_runtime_opens_only_assembly_and_freezes_schema',
                                             'old': 'def '
                                                    'test_phase4_step3_current_runtime_opens_only_assembly_and_freezes_schema(repo_root, '
                                                    'phase4_step2_snapshot):\n'},
                                            {'new': 'def '
                                                    'test_phase4_step3_current_workflows_preserve_matrix_and_use_active_dispatch(repo_root, '
                                                    'phase4_step3_snapshot):\n'
                                                    '    repo_root = '
                                                    'phase4_step3_snapshot\n',
                                             'node': 'test_phase4_step3_current_workflows_preserve_matrix_and_use_active_dispatch',
                                             'old': 'def '
                                                    'test_phase4_step3_current_workflows_preserve_matrix_and_use_active_dispatch(repo_root):\n'},
                                            {'new': 'def '
                                                    'test_phase4_step3_current_snapshot_checks_valid_tree_before_mutations(repo_root, '
                                                    'tmp_path, '
                                                    'phase4_gate_tools, '
                                                    'mutation, '
                                                    'phase4_step3_snapshot):\n',
                                             'node': 'test_phase4_step3_current_snapshot_checks_valid_tree_before_mutations',
                                             'old': 'def '
                                                    'test_phase4_step3_current_snapshot_checks_valid_tree_before_mutations(repo_root, '
                                                    'tmp_path, '
                                                    'phase4_gate_tools, '
                                                    'mutation):\n'},
                                            {'new': '        '
                                                    'shutil.copyfile(phase4_step3_snapshot '
                                                    '/ relative, '
                                                    'destination)\n',
                                             'node': 'test_phase4_step3_current_snapshot_checks_valid_tree_before_mutations',
                                             'old': '        '
                                                    'shutil.copyfile(repo_root '
                                                    '/ relative, '
                                                    'destination)\n'}],
 'tests/unit/test_phase4_contracts.py': [{'new': 'def '
                                                 'test_phase4_step3_approved_control_keeps_independent_step2_anchors(phase4_tools, '
                                                 'phase4_step3_snapshot):\n'
                                                 '    control = '
                                                 'json.loads((phase4_step3_snapshot '
                                                 '/ '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\n',
                                          'node': 'test_phase4_step3_approved_control_keeps_independent_step2_anchors',
                                          'old': 'def '
                                                 'test_phase4_step3_approved_control_keeps_independent_step2_anchors(phase4_tools):\n'
                                                 '    control = '
                                                 'json.loads((ROOT / '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\n'},
                                         {'new': 'def '
                                                 'test_phase4_step3_control_rejects_forged_scope_and_stage(phase4_tools, '
                                                 'field, value, '
                                                 'phase4_step3_snapshot):\n'
                                                 '    control = '
                                                 'json.loads((phase4_step3_snapshot '
                                                 '/ '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\n',
                                          'node': 'test_phase4_step3_control_rejects_forged_scope_and_stage',
                                          'old': 'def '
                                                 'test_phase4_step3_control_rejects_forged_scope_and_stage(phase4_tools, '
                                                 'field, value):\n'
                                                 '    control = '
                                                 'json.loads((ROOT / '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\n'},
                                         {'new': 'def '
                                                 'test_phase4_step3_control_rejects_unapproved_dispatch(phase4_tools, '
                                                 'step, '
                                                 'phase4_step3_snapshot):\n'
                                                 '    control = '
                                                 'json.loads((phase4_step3_snapshot '
                                                 '/ '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\n',
                                          'node': 'test_phase4_step3_control_rejects_unapproved_dispatch',
                                          'old': 'def '
                                                 'test_phase4_step3_control_rejects_unapproved_dispatch(phase4_tools, '
                                                 'step):\n'
                                                 '    control = '
                                                 'json.loads((ROOT / '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\n'},
                                         {'new': 'def '
                                                 'test_phase4_step3_control_requires_explicit_approval_fields(phase4_tools, '
                                                 'field, '
                                                 'phase4_step3_snapshot):\n'
                                                 '    control = '
                                                 'json.loads((phase4_step3_snapshot '
                                                 '/ '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\n',
                                          'node': 'test_phase4_step3_control_requires_explicit_approval_fields',
                                          'old': 'def '
                                                 'test_phase4_step3_control_requires_explicit_approval_fields(phase4_tools, '
                                                 'field):\n'
                                                 '    control = '
                                                 'json.loads((ROOT / '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\n'},
                                         {'new': 'def '
                                                 'test_phase4_step3_control_cannot_mint_extra_permission(phase4_tools, '
                                                 'phase4_step3_snapshot):\n'
                                                 '    control = '
                                                 'json.loads((phase4_step3_snapshot '
                                                 '/ '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\n',
                                          'node': 'test_phase4_step3_control_cannot_mint_extra_permission',
                                          'old': 'def '
                                                 'test_phase4_step3_control_cannot_mint_extra_permission(phase4_tools):\n'
                                                 '    control = '
                                                 'json.loads((ROOT / '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\n'},
                                         {'new': 'def '
                                                 'test_phase4_step3_historical_migrations_preserve_ten_step2_gate_nodes(phase4_tools, '
                                                 'phase4_step2_snapshot, '
                                                 'phase4_step3_snapshot):\n',
                                          'node': 'test_phase4_step3_historical_migrations_preserve_ten_step2_gate_nodes',
                                          'old': 'def '
                                                 'test_phase4_step3_historical_migrations_preserve_ten_step2_gate_nodes(phase4_tools, '
                                                 'phase4_step2_snapshot):\n'},
                                         {'new': '            path, '
                                                 '(phase4_step2_snapshot / '
                                                 'path).read_bytes(), '
                                                 '(phase4_step3_snapshot / '
                                                 'path).read_bytes(),\n',
                                          'node': 'test_phase4_step3_historical_migrations_preserve_ten_step2_gate_nodes',
                                          'old': '            path, '
                                                 '(phase4_step2_snapshot / '
                                                 'path).read_bytes(), (ROOT / '
                                                 'path).read_bytes(),\n'},
                                         {'new': 'def '
                                                 'test_phase4_step3_historical_guard_rejects_assertion_and_binding_weakening(phase4_tools, '
                                                 'phase4_step2_snapshot, '
                                                 'mutation, '
                                                 'phase4_step3_snapshot):\n',
                                          'node': 'test_phase4_step3_historical_guard_rejects_assertion_and_binding_weakening',
                                          'old': 'def '
                                                 'test_phase4_step3_historical_guard_rejects_assertion_and_binding_weakening(phase4_tools, '
                                                 'phase4_step2_snapshot, '
                                                 'mutation):\n'},
                                         {'new': '    after = '
                                                 '(phase4_step3_snapshot / '
                                                 'path).read_bytes()\n'
                                                 '    verify = '
                                                 'phase4_tools["verify_phase4_step3_test_migration"]\n',
                                          'node': 'test_phase4_step3_historical_guard_rejects_assertion_and_binding_weakening',
                                          'old': '    after = (ROOT / '
                                                 'path).read_bytes()\n'
                                                 '    verify = '
                                                 'phase4_tools["verify_phase4_step3_test_migration"]\n'}]}
PHASE4_STEP4_ALLOWED = {'.github/workflows/ci.yml',
 '.github/workflows/golden.yml',
 '.github/workflows/release.yml',
 '.github/workflows/security.yml',
 'PHASE_4_BASELINE.json',
 'PHASE_4_DECISIONS.md',
 'docs/architecture.md',
 'docs/privacy.md',
 'docs/report_schema.md',
 'docs/theory_traceability.md',
 'scripts/check_spec_consistency.py',
 'scripts/check_traceability.py',
 'scripts/release_check.py',
 'src/recursive_integrity_toolkit/config.py',
 'src/recursive_integrity_toolkit/reports/assembly.py',
 'src/recursive_integrity_toolkit/result.py',
 'src/recursive_integrity_toolkit/utils/hashing.py',
 'src/recursive_integrity_toolkit/utils/logging.py',
 'tests/conftest.py',
 'tests/integration/test_ci_workflows.py',
 'tests/integration/test_hero_structure.py',
 'tests/integration/test_license_notices.py',
 'tests/integration/test_no_algorithms.py',
 'tests/integration/test_no_network.py',
 'tests/integration/test_optional_dependency.py',
 'tests/integration/test_owner_ids.py',
 'tests/integration/test_package_import.py',
 'tests/integration/test_package_install.py',
 'tests/integration/test_phase4_gates.py',
 'tests/integration/test_prohibited_structure.py',
 'tests/integration/test_repository_structure.py',
 'tests/integration/test_schema_json.py',
 'tests/unit/test_PR015_redaction.py',
 'tests/unit/test_PR016_determinism.py',
 'tests/unit/test_PR018_language.py',
 'tests/unit/test_phase4_contracts.py'}


def _phase4_step3_files():
    """Read the exact accepted Step 3 Git tree and verify every blob identity."""
    for suffix, expected in (("^{commit}", PHASE4_STEP3_FINAL), ("^{tree}", PHASE4_STEP3_TREE),
                             (":tests", PHASE4_STEP3_TEST_TREE)):
        if git("rev-parse", PHASE4_STEP3_FINAL + suffix).decode().strip() != expected:
            raise ValueError("Pinned Phase 4 Step 3 identity mismatch")
    objects = {}
    for entry in git("ls-tree", "-rz", PHASE4_STEP3_FINAL).split(b"\0"):
        if not entry:
            continue
        metadata, raw_path = entry.split(b"\t", 1)
        mode, kind, oid = metadata.split()
        path = raw_path.decode("utf-8")
        if (mode not in (b"100644", b"100755") or kind != b"blob" or path in objects
                or path.startswith("/") or ".." in path.split("/") or ".git" in path.split("/")):
            raise ValueError("Unsafe pinned Step 3 Git object")
        objects[path] = oid.decode("ascii")
    if len(objects) != 227:
        raise ValueError("Pinned Step 3 must contain exactly 227 files")
    files = {}
    with zipfile.ZipFile(io.BytesIO(git("archive", "--format=zip", PHASE4_STEP3_FINAL))) as archive:
        names = [item.filename for item in archive.infolist() if not item.is_dir()]
        if len(names) != len(objects) or set(names) != set(objects):
            raise ValueError("Pinned Step 3 archive identity mismatch")
        for name in names:
            raw = archive.read(name)
            oid = hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()
            if oid != objects[name]:
                raise ValueError(f"Pinned Step 3 blob mismatch: {name}")
            files[name] = raw
    return MappingProxyType(files)


def phase4_step4_expected_control() -> dict:
    """Actual Step 4 approval is independent of the mutable control document."""
    prior = _phase4_step3_files()
    result = phase4_step3_expected_control()
    result.update({
        "control_version": "1.3", "active_step": 4,
        "approval_date": PHASE4_STEP4_APPROVAL_DATE, "approval_basis": PHASE4_STEP4_APPROVAL,
        "previous_step_commit": PHASE4_STEP3_FINAL,
        "previous_step_tree": PHASE4_STEP3_TREE,
        "previous_step_test_tree": PHASE4_STEP3_TEST_TREE,
        "previous_step_core_tests": 2876, "previous_step_parquet_tests": 2879,
        "previous_step_files_sha256": {p: hashlib.sha256(raw).hexdigest() for p, raw in sorted(prior.items())},
        "permitted_paths": sorted(PHASE4_STEP4_ALLOWED), "new_files_permitted": [],
        "runtime_changes_authorized": True, "schema_changes_authorized": False,
        "runtime_paths_authorized": sorted(p for p in PHASE4_STEP4_ALLOWED if p.startswith("src/")),
        "schema_paths_authorized": [],
        "step3_historical_binding_nodes": {p: sorted({r["node"] for r in rows})
                                          for p, rows in sorted(PHASE4_STEP4_MIGRATIONS.items())},
    })
    return result


def verify_phase4_step4_control(control: dict, step: int = 4) -> None:
    if type(step) is not int or step != 4 or type(control) is not dict:
        raise ValueError("Unsupported Phase 4 Step 4 stage/control")
    try:
        actual = json.dumps(control, sort_keys=True, ensure_ascii=True, allow_nan=False)
        expected = json.dumps(phase4_step4_expected_control(), sort_keys=True, ensure_ascii=True, allow_nan=False)
    except (TypeError, ValueError) as error:
        raise ValueError("Invalid Phase 4 Step 4 control") from error
    if actual != expected:
        raise ValueError("Phase 4 control differs from the independently approved Step 4 contract")


def verify_phase4_step4_changes(changes: list[tuple[str, str]]) -> None:
    seen = set()
    for status, path in changes:
        if path in seen or path not in PHASE4_STEP4_ALLOWED or status != "M":
            raise ValueError(f"Unapproved Phase 4 Step 4 path/operation: {status} {path}")
        seen.add(path)


def _phase4_step4_header(node, path):
    """Allow explicit test parametrization/fixtures, never definition-time effects."""
    for decorator in node.decorator_list:
        if not isinstance(decorator, ast.Call) or ast.unparse(decorator.func) not in {
                "pytest.fixture", "pytest.mark.parametrize"}:
            raise ValueError(f"Unapproved Step 4 test decorator: {path}:{node.name}")
        if ast.unparse(decorator.func) == "pytest.fixture" and not node.name.startswith("phase4_step"):
            raise ValueError("A Step 4 fixture must have an explicit scoped name")
        if any(keyword.arg is None for keyword in decorator.keywords):
            raise ValueError("Decorator expansion is outside the Step 4 contract")
        for value in [*decorator.args, *(keyword.value for keyword in decorator.keywords)]:
            try:
                ast.literal_eval(value)
            except (ValueError, TypeError, SyntaxError) as error:
                raise ValueError("Step 4 decorator arguments must be literal") from error
    clone = ast.parse(ast.unparse(node)).body[0]
    clone.decorator_list = []
    _phase4_preserve_function_header(clone, path)


def _phase4_step4_append_only(before: bytes, after: bytes, path: str) -> None:
    if not after.startswith(before):
        raise ValueError(f"Inherited Step 3 prefix changed: {path}")
    old, new = ast.parse(before), ast.parse(after)
    bindings = set()
    for node in old.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            bindings.add(node.name)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            bindings.update(alias.asname or alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            bindings.update(child.id for target in targets for child in ast.walk(target) if isinstance(child, ast.Name))
    for node in new.body[len(old.body):]:
        if not isinstance(node, ast.FunctionDef) or node.name in bindings:
            raise ValueError(f"Step 4 addition executes, rebinds or shadows inherited source: {path}")
        allowed_snapshot = path == "tests/conftest.py" and node.name == "phase4_step3_snapshot"
        if not allowed_snapshot and not node.name.startswith(("test_phase4_step4_", "phase4_step4_")):
            raise ValueError(f"Step 4 added test/helper is not explicitly scoped: {path}:{node.name}")
        if path == "tests/conftest.py" and node.name != "phase4_step3_snapshot":
            raise ValueError("Only the pinned Step 3 shared fixture is authorized")
        bindings.add(node.name)
        _phase4_step4_header(node, path)


def verify_phase4_step4_test_migration(path: str, before: bytes, after: bytes) -> None:
    prior = _phase4_step3_files()
    if path not in prior or path not in PHASE4_STEP4_ALLOWED or before != prior[path] or not path.startswith("tests/"):
        raise ValueError("Step 4 migration requires the exact named Step 3 source")
    _phase4_step4_check_test_migration(path, before, after)


def _phase4_step4_check_test_migration(path: str, before: bytes, after: bytes) -> None:
    """Check a source already read from the verified Step 3 immutable mapping."""
    expected = before
    for row in PHASE4_STEP4_MIGRATIONS.get(path, []):
        old, new = row["old"].encode(), row["new"].encode()
        if expected.count(old) != 1:
            raise ValueError("Step 3 historical binding is not unique")
        expected = expected.replace(old, new, 1)
    _phase4_step4_append_only(expected, after, path)


def _phase4_step4_preserve_tooling(before: bytes, after: bytes, path: str) -> None:
    """Preserve exact inherited statements using one source-line split per tree."""
    if path == "scripts/release_check.py":
        old = '    return phase4_cli_main() if explicit_phase4 else main()'
        new = ('    explicit_step4 = "--step=4" in argv or any(a == "--step" and b == "4" for a, b in zip(argv, argv[1:]))\n'
               '    if explicit_phase4 and explicit_step4:\n'
               '        return phase4_step4_cli_main()\n' + old)
        # Earlier preserved dispatch functions contain this source too; bind cli_main only.
        parsed = ast.parse(before)
        entry = next(node for node in parsed.body if isinstance(node, ast.FunctionDef) and node.name == "cli_main")
        old_entry = ast.get_source_segment(before.decode(), entry)
        if old_entry.count(old) != 1:
            raise ValueError("Step 3 release dispatcher identity mismatch")
        replacements = [(old_entry, old_entry.replace(old, new, 1))]
    else:
        old = '    if args.phase == 4 and args.step == 3:\n        return phase4_step3_main(step=args.step)\n'
        new = old + '    if args.phase == 4 and args.step == 4:\n        return phase4_step4_main(step=args.step)\n'
        replacements = [(old, new),
                        ('Choose explicit --phase 3 --step 11 or --phase 4 --step 1 or --phase 4 --step 2 or --phase 4 --step 3',
                         'Choose explicit --phase 3 --step 11 or --phase 4 --step 1 or --phase 4 --step 2 or --phase 4 --step 3 or --phase 4 --step 4')]
    expected = before
    for old, new in replacements:
        if expected.count(old.encode()) != 1:
            raise ValueError(f"Historical dispatcher identity mismatch: {path}")
        expected = expected.replace(old.encode(), new.encode(), 1)
    trees = [ast.parse(expected), ast.parse(after)]
    lines = [expected.splitlines(keepends=True), after.splitlines(keepends=True)]
    def segment(index, node):
        if node.lineno == node.end_lineno:
            return lines[index][node.lineno - 1][node.col_offset:node.end_col_offset]
        return (lines[index][node.lineno - 1][node.col_offset:]
                + b"".join(lines[index][node.lineno:node.end_lineno - 1])
                + lines[index][node.end_lineno - 1][:node.end_col_offset])
    def entry_guard(node):
        return isinstance(node, ast.If) and isinstance(node.test, ast.Compare) and "__name__" in ast.unparse(node.test)
    guards = [n for n in trees[1].body if entry_guard(n)]
    expected_guard = ast.parse('if __name__ == "__main__":\n    raise SystemExit(cli_main())').body[0]
    if len(guards) != 1 or ast.dump(guards[0]) != ast.dump(expected_guard):
        raise ValueError(f"Unapproved Step 4 maintainer entrypoint: {path}")
    historical = [n for n in trees[0].body if not entry_guard(n)]
    current = [n for n in trees[1].body if not entry_guard(n)]
    old_entries = [(segment(0, n), ast.dump(n)) for n in historical]
    cursor = 0
    for node in current:
        if cursor < len(old_entries) and (segment(1, node), ast.dump(node)) == old_entries[cursor]:
            cursor += 1
            continue
        if isinstance(node, ast.FunctionDef) and (node.name == "_phase4_step3_files" or node.name.startswith(
                ("phase4_step4_", "_phase4_step4_", "verify_phase4_step4_", "audit_phase4_step4"))):
            _phase4_preserve_function_header(node, path)
            continue
        if isinstance(node, ast.Assign) and all(isinstance(target, ast.Name) and target.id.startswith(
                ("PHASE4_STEP4_", "PHASE4_STEP3_")) for target in node.targets):
            try:
                ast.literal_eval(node.value)
            except (ValueError, TypeError, SyntaxError) as error:
                raise ValueError(f"Nonliteral added Step 4 maintainer constant: {path}") from error
            continue
        raise ValueError(f"Unapproved Step 4 maintainer addition: {path}")
    if cursor != len(historical):
        raise ValueError(f"Inherited Step 3 maintainer statement changed: {path}")
    def binding_counts(tree):
        counts = {}
        for node in tree.body:
            names = []
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                names = [node.name]
            elif isinstance(node, (ast.Assign, ast.AnnAssign)):
                targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                names = [child.id for target in targets for child in ast.walk(target) if isinstance(child, ast.Name)]
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                names = [alias.asname or alias.name.split(".")[0] for alias in node.names]
            for name in names:
                counts[name] = counts.get(name, 0) + 1
        return counts
    inherited_counts = binding_counts(trees[0])
    for name, count in binding_counts(trees[1]).items():
        if count > inherited_counts.get(name, 1):
            raise ValueError(f"Duplicate Step 4 maintainer binding: {path}:{name}")


def verify_phase4_step4_snapshot(root: Path = ROOT) -> dict:
    prior = _phase4_step3_files()
    for path, raw in prior.items():
        target = root / path
        if not target.is_file() or target.is_symlink():
            raise ValueError(f"Missing or aliased inherited Step 3 file: {path}")
        current = target.read_bytes()
        if path not in PHASE4_STEP4_ALLOWED and current != raw:
            raise ValueError(f"Protected Step 3 bytes changed: {path}")
        if path.startswith("tests/") and path in PHASE4_STEP4_ALLOWED:
            _phase4_step4_check_test_migration(path, raw, current)
        elif path.startswith("scripts/") and path in PHASE4_STEP4_ALLOWED:
            _phase4_step4_preserve_tooling(raw, current, path)
        elif path in {"docs/architecture.md", "docs/theory_traceability.md", "docs/report_schema.md", "docs/privacy.md", "PHASE_4_DECISIONS.md"}:
            if not current.startswith(raw):
                raise ValueError(f"Step 3 historical documentation prefix changed: {path}")
    actual_modules = {p.relative_to(root).as_posix() for p in (root / "src/recursive_integrity_toolkit").rglob("*.py")}
    expected_modules = {p for p in prior if p.startswith("src/") and p.endswith(".py")}
    if actual_modules != expected_modules or len(actual_modules) != 40:
        raise ValueError("Step 4 cannot change the runtime module set")
    if {p.name for p in (root / "schemas").iterdir()} != {Path(p).name for p in prior if p.startswith("schemas/")}:
        raise ValueError("Step 4 cannot change the schema set")
    if hashlib.sha256((root / "PHASE_4_PLAN.md").read_bytes()).hexdigest() != PHASE4_PLAN_SHA256:
        raise ValueError("Approved Phase 4 plan changed")
    verify_phase4_step4_control(json.loads((root / "PHASE_4_BASELINE.json").read_text(encoding="utf-8")))
    decisions = (root / "PHASE_4_DECISIONS.md").read_text(encoding="utf-8")
    if PHASE4_STEP4_APPROVAL not in decisions or PHASE4_STEP3_FINAL not in decisions:
        raise ValueError("Actual Step 4 authorization or Step 3 evidence anchor missing")
    if any((root / name).exists() for name in PHASE4_FORBIDDEN_OUTPUTS):
        raise ValueError("Step 4 cannot create Phase 4 completion records or audit outputs")
    import runpy
    checker = runpy.run_path(str(root / "scripts/check_traceability.py"), run_name="phase4_step4_assembly_boundary")
    checker["phase4_step4_privacy_boundary"](root)
    schema_bytes = (root / "schemas/report.schema.json").read_bytes()
    if hashlib.sha256(schema_bytes).hexdigest() != PHASE4_STEP2_REPORT_SCHEMA_SHA256:
        raise ValueError("Step 4 report schema differs from its independently reviewed bytes")
    schema = json.loads(schema_bytes)
    if (schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema"
            or schema.get("type") != "object" or schema.get("additionalProperties") is not False):
        raise ValueError("Step 4 report schema dialect/closed root mismatch")
    return {"package_modules": 40, "frozen_runtime_modules": 35, "frozen_schemas": 5,
            "hero_files_unchanged": 6, "historical_phase3_migrated_nodes": 16,
            "phase_complete": False, "result_contracts_enabled": True,
            "adapters_enabled": True, "privacy_views_enabled": True, "cli_analysis_enabled": False}


def audit_phase4_step4(step: int = 4) -> dict:
    verify_phase4_step4_control(json.loads((ROOT / "PHASE_4_BASELINE.json").read_text(encoding="utf-8")), step)
    result = {"phase": 4, "active_step": step, **verify_phase4_step4_snapshot(),
              "phase0_hashes_verified": 16, "publication_authorized": False}
    print(json.dumps(result, indent=2))
    return result


def audit_phase4_step4_diff(step: int = 4) -> dict:
    if type(step) is not int or step != 4:
        raise ValueError("Unsupported Phase 4 Step 4 stage")
    _phase4_step3_files()
    subprocess.run(["git", "-C", str(ROOT), "merge-base", "--is-ancestor", PHASE4_STEP3_FINAL, "HEAD"], check=True)
    raw = git("diff", "--name-status", "--no-renames", "-z", PHASE4_STEP3_FINAL, "--").split(b"\0")
    raw = [part.decode("utf-8") for part in raw if part]
    if len(raw) % 2:
        raise ValueError("Malformed Step 4 Git difference records")
    changes = list(zip(raw[::2], raw[1::2]))
    changes.extend(("A", p.decode()) for p in git("ls-files", "--others", "--exclude-standard", "-z").split(b"\0") if p)
    verify_phase4_step4_changes(changes)
    result = {"previous_step_commit": PHASE4_STEP3_FINAL, "changed_files": len(changes),
              "changes": changes, "step": 4, "scope": "PASS"}
    print(json.dumps(result, indent=2))
    return result


def phase4_step4_baseline_evidence(output: Path) -> dict:
    """Reconcile all inherited identities, including the accepted Step 3 suite."""
    output.mkdir(parents=True, exist_ok=True)
    inherited = phase4_step3_baseline_evidence(output / "phase4-step3-inherited")
    with tempfile.TemporaryDirectory(prefix="rit-p4-step3-identities-") as temp:
        baseline = Path(temp)
        for name, raw in _phase4_step3_files().items():
            target = baseline / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(raw)
        old, old_log = _collect(baseline)
    current, current_log = _collect(ROOT)
    expected = 2879 if os.environ.get("RIT_TEST_PARQUET") == "1" else 2876
    if len(old) != expected or set(old) - set(current):
        raise ValueError("Accepted Phase 4 Step 3 test identities were lost")
    result = {"baseline_commit": PHASE4_STEP3_FINAL, "baseline_test_tree": PHASE4_STEP3_TEST_TREE,
              "baseline_nodeids": old, "current_nodeids": current, "missing_nodeids": [],
              "baseline_tests": len(old), "current_tests": len(current), "inherited": inherited,
              "nodeids_sha256": hashlib.sha256(("\n".join(old)+"\n").encode()).hexdigest()}
    (output / "phase4_step4_test_identity_manifest.json").write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    (output / "phase4-step3-collection.log").write_text(old_log, encoding="utf-8")
    (output / "phase4-step4-collection.log").write_text(current_log, encoding="utf-8")
    print(json.dumps({k: result[k] for k in ("baseline_tests", "current_tests", "missing_nodeids")}, indent=2))
    return result


def phase4_step4_candidate(output: Path, step: int = 4) -> None:
    """Build tested Step 4 intermediate evidence without declaring Phase 4 complete."""
    if os.environ.get("RIT_TEST_PARQUET") != "1" or importlib.util.find_spec("pyarrow") is None:
        raise ValueError("Step 4 candidate evidence requires RIT_TEST_PARQUET=1 and real PyArrow")
    output.mkdir(parents=True, exist_ok=True)
    result = audit_phase4_step4(step)
    result["diff"] = audit_phase4_step4_diff(step)
    if git("status", "--porcelain").strip():
        raise ValueError("Step 4 candidate archive requires committed, clean source")
    result["core"] = verify_junit(output / "core.xml", minimum=2876)
    result["parquet"] = verify_junit(output / "parquet.xml", require_parquet=True, minimum=2879)
    result["core_math_measurements"] = verify_step10_evidence(output / "core.xml", output / "phase4-step4-core-observations.json")
    result["parquet_math_measurements"] = verify_step10_evidence(output / "parquet.xml", output / "phase4-step4-parquet-observations.json")
    identity = phase4_step4_baseline_evidence(output)
    result["test_identity"] = {k: identity[k] for k in ("baseline_tests", "current_tests", "nodeids_sha256")}
    expected = set()
    for node in identity["current_nodeids"]:
        base, bracket, parameter = node.partition("[")
        owner, name = base.rsplit("::", 1)
        expected.add((owner.removesuffix(".py").replace("/", ".").replace("::", "."), name + bracket + parameter))
    for name, parquet in (("core.xml", False), ("parquet.xml", True)):
        cases = {(c.get("classname", ""), c.get("name", "")) for c in ET.parse(output / name).getroot().iter("testcase")}
        target = expected if parquet else {c for c in expected if c[1] not in PARQUET_CASES}
        if cases != target:
            raise ValueError(f"Step 4 JUnit does not execute the entire current suite: {name}")
    wheel, _ = verify_distributions(output / "dist")
    phase4_step2_installed_contract_smoke(wheel)
    phase4_step3_installed_assembly_smoke(wheel)
    phase4_step4_installed_privacy_smoke(wheel)
    archive = output / "recursive-integrity-toolkit-phase4-step4-candidate.zip"
    subprocess.run(["git", "-C", str(ROOT), "archive", "--format=zip", "--prefix=recursive-integrity-toolkit/", "HEAD", "-o", str(archive.resolve())], check=True)
    tracked = {p for p in git("ls-files", "-z").decode().split("\0") if p}
    with zipfile.ZipFile(archive) as zipped:
        names = {p.removeprefix("recursive-integrity-toolkit/") for p in zipped.namelist() if not p.endswith("/")}
        if names != tracked or len(tracked) != 227:
            raise ValueError("Step 4 source archive file set mismatch")
        for name in names:
            if zipped.read("recursive-integrity-toolkit/"+name) != (ROOT / name).read_bytes():
                raise ValueError(f"Step 4 source archive byte mismatch: {name}")
    result.update({"commit": git("rev-parse", "HEAD").decode().strip(),
                   "tree": git("rev-parse", "HEAD^{tree}").decode().strip(),
                   "source_archive": archive.name, "tracked_files": len(tracked),
                   "python": sys.version, "platform": sys.platform,
                   "versions": {name: importlib.metadata.version(name) for name in ("numpy", "pandas", "pytest")}})
    (output / "phase4_step4_execution_metadata.json").write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    (output / "phase4_step4_repository_files.sha256").write_text("".join(f"{hashlib.sha256((ROOT/name).read_bytes()).hexdigest()}  {name}\n" for name in sorted(tracked)), encoding="utf-8")
    paths = sorted(p for p in output.rglob("*") if p.is_file() and p.name != "phase4_step4_artifacts.sha256")
    (output / "phase4_step4_artifacts.sha256").write_text("".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(output).as_posix()}\n" for p in paths), encoding="utf-8")
    print(f"Phase 4 Step 4 candidate: {len(tracked)} source files verified; Phase 4 remains incomplete.")


def phase4_step4_cli_main() -> int:
    parser = argparse.ArgumentParser(description="Phase 4 Step 4 maintainer gate")
    parser.add_argument("--phase", type=int, choices=(4,), required=True)
    parser.add_argument("--step", type=int, choices=(4,), required=True)
    parser.add_argument("--diff", action="store_true")
    parser.add_argument("--junit", type=Path)
    parser.add_argument("--require-parquet", action="store_true")
    parser.add_argument("--minimum-tests", type=int, default=1)
    parser.add_argument("--baseline-evidence", type=Path)
    parser.add_argument("--dist", type=Path)
    parser.add_argument("--smoke-wheel", type=Path)
    parser.add_argument("--candidate", type=Path)
    parser.add_argument("--delivery", type=Path)
    args = parser.parse_args()
    if args.delivery is not None:
        raise ValueError("Phase 4 Step 4 cannot certify a final phase delivery")
    if args.junit is not None:
        verify_junit(args.junit, require_parquet=args.require_parquet, minimum=args.minimum_tests)
    elif args.baseline_evidence is not None:
        phase4_step4_baseline_evidence(args.baseline_evidence)
    elif args.dist is not None:
        audit_phase4_step4(args.step)
        wheel, _ = verify_distributions(args.dist)
        smoke_installed(wheel)
        smoke_installed_duplicates(wheel)
        phase4_step2_installed_contract_smoke(wheel)
        phase4_step3_installed_assembly_smoke(wheel)
        phase4_step4_installed_privacy_smoke(wheel)
    elif args.smoke_wheel is not None:
        smoke_installed(args.smoke_wheel)
    elif args.candidate is not None:
        phase4_step4_candidate(args.candidate, args.step)
    else:
        audit_phase4_step4(args.step)
        if args.diff:
            audit_phase4_step4_diff(args.step)
    return 0


def phase4_step4_installed_privacy_smoke(wheel: Path) -> None:
    """Exercise installed privacy, config and diagnostics after accepted calculation."""
    with tempfile.TemporaryDirectory(prefix="rit-p4-step4-installed-privacy-") as temp:
        work = Path(temp)
        subprocess.run([sys.executable, "-m", "venv", str(work / "venv")], check=True)
        bindir = work / "venv" / ("Scripts" if os.name == "nt" else "bin")
        python = bindir / ("python.exe" if os.name == "nt" else "python")
        subprocess.run([str(python), "-m", "pip", "install", "--no-index", "--no-deps", str(wheel.resolve())],
                       cwd=work, check=True)
        program = '''import builtins, copy, importlib.abc, io, json, socket, sys
from dataclasses import replace
from pathlib import Path
from types import MappingProxyType
blocked_roots = {'numpy', 'pandas', 'pyarrow', 'jsonschema', 'referencing', 'networkx', 'scipy', 'sklearn'}
blocked_import_layers = tuple('recursive_integrity_toolkit.' + name for name in (
    'cli', 'reports.json_report', 'reports.markdown_report', 'reports.html_report'))
class DenyAnalysis(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in blocked_roots or any(
                fullname == layer or fullname.startswith(layer + '.') for layer in blocked_import_layers):
            raise AssertionError('installed assembly attempted optional, CLI or renderer import: ' + fullname)
sys.meta_path.insert(0, DenyAnalysis())
def blocked(*args, **kwargs):
    raise AssertionError('installed assembly attempted file or network access')
socket.create_connection = blocked
socket.getaddrinfo = blocked
socket.socket.connect = blocked
socket.socket.connect_ex = blocked
from recursive_integrity_toolkit.models import (
    BundleValidationResult, Capability, CapabilityKey, CapabilityStatus,
    CanonicalRow, FileFormat, FileInventoryEntry, FileRole, ProvenanceMatch, RecordKey, RowLocation,
    ObservabilityAssessment, ProvenanceJoinResult, ValidationCoverage,
    ValidationMessage, ValidationSeverity, VersionOrderResult,
)
import recursive_integrity_toolkit.reports.assembly as assembly
from recursive_integrity_toolkit.result import CanonicalReport, SafeReportView
from recursive_integrity_toolkit.config import resolve_phase4_options, phase4_config_summary, phase4_config_hash
from recursive_integrity_toolkit.utils.hashing import IdentifierProtection
from recursive_integrity_toolkit.utils.logging import safe_diagnostic, format_diagnostic
from recursive_integrity_toolkit.reports.assembly import privacy_view, build_run_metadata
assert Path(assembly.__file__).resolve().is_relative_to(Path(sys.argv[1]) / 'venv')
assert not Path(assembly.__file__).resolve().is_relative_to(Path(sys.argv[2]) / 'src')
# Prepare real installed-kernel evidence before enabling the assembly execution barrier.
from recursive_integrity_toolkit.config import RepresentationConfig
from recursive_integrity_toolkit.representations.field import assign_field_states
from recursive_integrity_toolkit.metrics.diversity import calculate_state_distribution
rows = tuple(CanonicalRow('records', RecordKey('v1', identifier),
             MappingProxyType({'dataset_version': 'v1', 'record_id': identifier,
                               'content': 'synthetic installed fixture', 'topic': topic}),
             MappingProxyType({}), MappingProxyType({}),
             location=RowLocation(FileRole.RECORDS_PRIMARY, 'fixture.jsonl', index, index))
             for index, (identifier, topic) in enumerate((('a', 'one'), ('b', 'two')), 1))
represented = assign_field_states(rows, dataset_versions=('v1',), scope_id='installed:v1',
    config=RepresentationConfig('topic', 'topic_field', 'topic', 'installed-fixture-v1', 'error'))
distribution = calculate_state_distribution(represented)
expected_support = distribution.unweighted.support_size.value
expected_diversity = distribution.unweighted.gini_simpson_diversity.value
expected_concentration = distribution.unweighted.simpson_concentration.value
assert (expected_support, expected_diversity, expected_concentration) == (2, 0.5, 0.5)
record_keys = tuple(row.record_key for row in rows)
empirical_coverage = ValidationCoverage(0, 2, 'all_valid_records')
empirical_join = ProvenanceJoinResult(('v1',), record_keys, False,
    tuple(ProvenanceMatch(key, None) for key in record_keys), record_keys,
    empirical_coverage, empirical_coverage, empirical_coverage, ())
empirical_caps = {key: Capability(CapabilityStatus.UNAVAILABLE, reason_codes=('R_MISSING_EVIDENCE',))
                  for key in CapabilityKey}
empirical_caps[CapabilityKey.INGESTION] = Capability(CapabilityStatus.AVAILABLE)
empirical_caps[CapabilityKey.CONTENT_DIAGNOSTICS] = Capability(CapabilityStatus.AVAILABLE)
empirical_bundle = BundleValidationResult(
    inventory=(FileInventoryEntry(FileRole.RECORDS_PRIMARY, Path('fixture.jsonl'), FileFormat.JSONL,
                                  128, '0' * 64, 2, ('dataset_version', 'record_id', 'content', 'topic')),),
    records=rows, provenance=None, provenance_join=empirical_join,
    version_order=VersionOrderResult(('v1',), ('v1',), 'single_version', {}, {}), generation=None,
    observability=ObservabilityAssessment(1, empirical_caps), mapping_traces=(), content_read_keys=(),
    validation_messages=(),
)
# Result type imports are permitted; executing a calculation or input operation is not.
def deny_execution(frame, event, argument):
    if event == 'call':
        source = frame.f_code.co_filename.replace(chr(92), '/')
        if any('/recursive_integrity_toolkit/' + layer + '/' in source for layer in (
                'metrics', 'io', 'representations', 'observability', 'lineage')):
            raise AssertionError('installed assembly executed an analytical/input function: ' + frame.f_code.co_name)
sys.setprofile(deny_execution)
builtins.open = blocked
io.open = blocked
def deny_effects(event, arguments):
    if event in ('open', 'os.listdir', 'os.scandir', 'os.system', 'subprocess.Popen') or event.startswith('socket.'):
        raise AssertionError('installed assembly attempted an external effect: ' + event)
sys.addaudithook(deny_effects)
coverage = ValidationCoverage(0, 0, 'all_valid_records')
join = ProvenanceJoinResult((), (), False, (), (), coverage, coverage, coverage, ())
observability = ObservabilityAssessment(0, {
    key: Capability(CapabilityStatus.UNAVAILABLE, reason_codes=('R_EMPTY_SCOPE',))
    for key in CapabilityKey
})
bundle = BundleValidationResult(
    inventory=(), records=(), provenance=None, provenance_join=join,
    version_order=VersionOrderResult((), (), 'not_available', {}, {}), generation=None,
    observability=observability, mapping_traces=(), content_read_keys=(), validation_messages=(),
)
run = {
    'run_id': 'installed-typed-empty-case', 'toolkit_version': '0.1.0.dev2',
    'report_schema_version': '1.0', 'started_at': None, 'completed_at': None,
    'duration_seconds': None, 'python_version': None, 'platform': None,
    'command': None, 'config_hash': None, 'random_seed': None,
    'strict_mode': False, 'redacted_mode': False, 'network_call_count': 0,
    'deterministic': True, 'privacy_mode': 'standard', 'run_status': 'complete',
    'null_reasons': {
        'started_at': 'Pure assembly does not start a clock.',
        'completed_at': 'Pure assembly does not start a clock.',
        'duration_seconds': 'Pure assembly does not measure execution.',
        'python_version': 'No execution environment is asserted.',
        'platform': 'No execution environment is asserted.',
        'command': 'Direct installed Python API, no command invoked.',
        'config_hash': 'No resolved configuration hash was supplied.',
        'random_seed': 'No stochastic scenario was requested.',
    },
}
original_run = copy.deepcopy(run)
report = assembly.assemble_report(bundle, run=run)
assert type(report) is CanonicalReport
payload = report.to_dict()
assert tuple(payload) == ('run', 'inputs', 'observability', 'capabilities', 'observed_facts',
                         'derived_metrics', 'proxy_signals', 'simulations', 'unavailable_conclusions',
                         'recommended_next_metadata', 'warnings', 'errors')
assert payload['run'] == original_run and run == original_run
assert payload['inputs']['scope']['record_count'] == 0
assert payload['inputs']['artifacts'] == [] and payload['inputs']['file_hashes'] == []
assert payload['simulations'] == {} and payload['errors'] == []
assert payload['capabilities']['lineage']['execution_status'] == 'deferred'
assert report.sections['observability']['capabilities'] is report.sections['capabilities']
assert {'model_performance_decline', 'causal_ancestor_effect', 'universal_integrity',
        'universal_collapse_prediction'} <= {item['conclusion'] for item in payload['unavailable_conclusions']}
for name in ('provenance_row_coverage', 'provenance_required_field_coverage', 'grounding_field_coverage'):
    field = payload['observed_facts']['provenance'][name]
    assert field['value'] is None and field['status'] == 'unavailable'
    assert field['denominator'] == 0 and field['reason_codes']
assert assembly.assemble_report(bundle, run=run).to_dict() == payload
empirical = assembly.assemble_report(empirical_bundle, run=run, distributions=(distribution,)).to_dict()
assert empirical['observed_facts']['record_counts']['v1']['value'] == 2
assert empirical['derived_metrics']['support']['by_version']['v1']['support_size']['value'] == expected_support
assert empirical['derived_metrics']['diversity']['by_version']['v1']['gini_simpson_diversity']['value'] == expected_diversity
assert empirical['derived_metrics']['diversity']['by_version']['v1']['simpson_concentration']['value'] == expected_concentration
assert empirical['simulations'] == {} and empirical['errors'] == []
assert empirical['capabilities']['content_diagnostics']['execution_status'] == 'completed'
assert 'synthetic installed fixture' not in json.dumps(empirical)
run['run_id'] = 'caller-input-mutation'
payload['unavailable_conclusions'].clear()
assert report.to_dict()['run']['run_id'] == original_run['run_id']
assert report.to_dict()['unavailable_conclusions']
failure = ValidationMessage('E_FILE_PARSE', ValidationSeverity.FATAL,
                            'The supplied records artifact could not be parsed.')
failed_bundle = replace(bundle, validation_messages=(failure,))
failed = assembly.assemble_report(failed_bundle, run=original_run).to_dict()
assert failed['run']['run_status'] == 'failed'
assert len(failed['errors']) == 1
assert failed['errors'][0]['code'] == 'E_FILE_PARSE'
assert failed['errors'][0]['severity'] == 'fatal'
assert failed['errors'][0]['effect_on_run'] == 'failed'
assert failed['simulations'] == {}
assert failed['capabilities']['ingestion']['execution_status'] == 'failed'
for supplied in ({}, object()):
    try:
        assembly.assemble_report(supplied, run=original_run)
    except assembly.ReportAssemblyError:
        pass
    else:
        raise AssertionError('installed assembly accepted an untyped validation handoff')
for changes in ({'privacy_mode': 'redacted', 'redacted_mode': True}, {'duration_seconds': float('inf')}):
    invalid = dict(original_run)
    invalid.update(changes)
    try:
        assembly.assemble_report(bundle, run=invalid)
    except ValueError:
        pass
    else:
        raise AssertionError('installed assembly accepted an invalid run declaration')
assert not blocked_roots.intersection(sys.modules)
assert not any(name == layer or name.startswith(layer + '.') for name in sys.modules for layer in blocked_import_layers)
# Step 4 operates on already assembled evidence under the same execution barrier.
fixed = IdentifierProtection.create(secret=b'rit-installed-privacy-test-secret-2026')
options = resolve_phase4_options(cli={'redacted': True, 'record_ids': 'hash'})
summary = phase4_config_summary(options)
assert summary['privacy_mode'] == 'redacted' and summary['record_id_mode'] == 'hash'
assert summary['scenario_requested'] is False and summary['weighted'] is False
assert phase4_config_hash(options) == phase4_config_hash(options)
assert len(phase4_config_hash(options)) == 64
metadata = build_run_metadata(options=options, run_id='installed-safe-run', operation='audit')
assert metadata['command'] == 'rit audit --redacted'
assert metadata['config_hash'] == phase4_config_hash(options)
assert metadata['resolved_options'] == summary
assert metadata['privacy_mode'] == 'standard' and metadata['redacted_mode'] is False
assert metadata['network_count_scope'] == 'toolkit_managed_outbound_operations'
assert 'identifier_secret_material' in metadata['config_hash_exclusions']
assert metadata['started_at'] is None and metadata['duration_seconds'] is None
assert fixed.algorithm == 'HMAC-SHA-256' and fixed.stability_scope == 'run'
assert fixed.pseudonym('dataset_version', 'v1') != fixed.pseudonym('state_id', 'v1')
assert 'rit-installed-privacy-test-secret-2026' not in repr(fixed)
private_payload = copy.deepcopy(failed)
private_payload['errors'][0]['message'] = 'PRIVATE_CONTENT_SENTINEL /secret/private-input.jsonl'
private_payload['errors'][0]['record_key'] = {'dataset_version': 'v1', 'record_id': 'PRIVATE_RECORD_SENTINEL'}
private_report = CanonicalReport(private_payload)
standard = privacy_view(private_report)
assert type(standard) is SafeReportView
assert 'PRIVATE_CONTENT_SENTINEL' not in json.dumps(standard.to_dict())
assert '/secret/private-input.jsonl' not in json.dumps(standard.to_dict())
assert standard.to_dict()['errors'][0]['severity'] == 'fatal'
protected = privacy_view(private_report, mode='redacted', protection=fixed)
assert type(protected) is SafeReportView
protected_payload = protected.to_dict()
assert protected_payload == privacy_view(private_report, mode='redacted', protection=fixed).to_dict()
assert 'PRIVATE_RECORD_SENTINEL' not in json.dumps(protected_payload)
assert 'PRIVATE_CONTENT_SENTINEL' not in json.dumps(protected_payload)
assert protected_payload['errors'][0]['severity'] == 'fatal'
assert protected_payload['run']['run_status'] == private_payload['run']['run_status']
preserved = privacy_view(private_report, mode='redacted', record_id_mode='preserve', protection=fixed).to_dict()
assert preserved['errors'][0]['record_key']['record_id'] == 'PRIVATE_RECORD_SENTINEL'
assert preserved['errors'][0]['record_key']['dataset_version'] != 'v1'
omitted = privacy_view(private_report, mode='redacted', record_id_mode='omit', protection=fixed).to_dict()
assert 'PRIVATE_RECORD_SENTINEL' not in json.dumps(omitted)
assert omitted['errors'][0]['severity'] == 'fatal'
fresh_one = privacy_view(private_report, mode='redacted').to_dict()
fresh_two = privacy_view(private_report, mode='redacted').to_dict()
assert fresh_one['errors'][0]['record_key'] != fresh_two['errors'][0]['record_key']
empirical_report = CanonicalReport(empirical)
redacted_empirical = privacy_view(empirical_report, mode='redacted', protection=fixed).to_dict()
for capability, original in empirical['capabilities'].items():
    protected_capability = redacted_empirical['capabilities'][capability]
    for field in ('status', 'coverage', 'execution_status'):
        assert protected_capability[field] == original[field]
    for coverage_name, original_coverage in original['coverage_details'].items():
        protected_coverage = protected_capability['coverage_details'][coverage_name]
        for field in ('numerator', 'denominator', 'ratio', 'denominator_name'):
            assert protected_coverage[field] == original_coverage[field]
protected_version = next(iter(redacted_empirical['derived_metrics']['support']['by_version']))
assert protected_version != 'v1'
assert redacted_empirical['observed_facts']['record_counts'][protected_version]['value'] == 2
assert redacted_empirical['derived_metrics']['support']['by_version'][protected_version]['support_size']['value'] == expected_support
assert redacted_empirical['derived_metrics']['diversity']['by_version'][protected_version]['gini_simpson_diversity']['value'] == expected_diversity
assert redacted_empirical['derived_metrics']['diversity']['by_version'][protected_version]['simpson_concentration']['value'] == expected_concentration
assert redacted_empirical['simulations'] == {}
assert private_report.to_dict() == private_payload and empirical_report.to_dict() == empirical
exported = protected.to_dict()
exported['errors'].clear()
assert protected.to_dict()['errors']
message = ValidationMessage('E_FILE_PARSE', ValidationSeverity.ERROR, 'PRIVATE_CONTENT_SENTINEL',
                            field='content', file_path='PRIVATE_PATH_SENTINEL')
diagnostic = safe_diagnostic(message, mode='redacted', protection=fixed)
formatted = format_diagnostic(message, mode='redacted', protection=fixed)
assert diagnostic['code'] == 'E_FILE_PARSE' and diagnostic['severity'] == 'error'
assert 'PRIVATE_CONTENT_SENTINEL' not in formatted and 'PRIVATE_PATH_SENTINEL' not in formatted
assert json.loads(formatted) == diagnostic
assert formatted.count(chr(10)) <= 1
assert not blocked_roots.intersection(sys.modules)
assert not any(name == layer or name.startswith(layer + '.') for name in sys.modules for layer in blocked_import_layers)
print('installed Step 4: privacy/config/diagnostic APIs, standard and three redacted record-ID modes, stable fixed context, fresh unlinkability, immutable views, unchanged accepted aggregates; metric/input execution, file I/O, optional imports and network blocked: PASS')
sys.setprofile(None)
print('installed Step 3: typed empty/error and prepared empirical handoffs, exact kernel values, null coverage, immutable mirror, deterministic disclosures, no default scenarios; analytical execution, optional imports, file I/O and network blocked during assembly: PASS')
'''
        subprocess.run([str(python), "-I", "-c", program, str(work), str(ROOT)], cwd=work, check=True)


# Phase 4 Step 5 adds pure renderers while retaining every inherited gate.


PHASE4_STEP4_FINAL = "49454a9b162cb8d35e38d1cb1ae32cb208d3a01c"


PHASE4_STEP4_TREE = "79264d845e08f73ee68e160dea04f7786f18fd0a"


PHASE4_STEP4_TEST_TREE = "4aa4ca0b22f8b8c25afe27feeaba713d6f0830bf"


PHASE4_STEP5_APPROVAL = "很好，Phase 4 Step 5 继续"


PHASE4_STEP5_APPROVAL_DATE = "2026-09-20"


PHASE4_STEP5_NEW = ()


PHASE4_STEP5_MIGRATIONS = {'tests/integration/test_phase4_gates.py': [{'new': 'def '
                                                    'test_phase4_step4_current_runtime_opens_only_privacy_metadata_modules_and_freezes_schema(repo_root, '
                                                    'phase4_step3_snapshot, phase4_step4_snapshot):\n'
                                                    '    repo_root = phase4_step4_snapshot\n',
                                             'node': 'test_phase4_step4_current_runtime_opens_only_privacy_metadata_modules_and_freezes_schema',
                                             'old': 'def '
                                                    'test_phase4_step4_current_runtime_opens_only_privacy_metadata_modules_and_freezes_schema(repo_root, '
                                                    'phase4_step3_snapshot):\n'},
                                            {'new': 'def '
                                                    'test_phase4_step4_current_workflows_preserve_matrix_and_use_active_dispatch(repo_root, '
                                                    'phase4_step4_snapshot):\n'
                                                    '    repo_root = phase4_step4_snapshot\n',
                                             'node': 'test_phase4_step4_current_workflows_preserve_matrix_and_use_active_dispatch',
                                             'old': 'def '
                                                    'test_phase4_step4_current_workflows_preserve_matrix_and_use_active_dispatch(repo_root):\n'},
                                            {'new': 'def '
                                                    'test_phase4_step4_current_snapshot_checks_valid_tree_before_mutations(repo_root, '
                                                    'tmp_path, phase4_gate_tools, mutation, '
                                                    'phase4_step4_snapshot):\n',
                                             'node': 'test_phase4_step4_current_snapshot_checks_valid_tree_before_mutations',
                                             'old': 'def '
                                                    'test_phase4_step4_current_snapshot_checks_valid_tree_before_mutations(repo_root, '
                                                    'tmp_path, phase4_gate_tools, mutation):\n'},
                                            {'new': '        shutil.copyfile(phase4_step4_snapshot / '
                                                    'relative, destination)\n'
                                                    '    verify = '
                                                    'phase4_gate_tools["verify_phase4_step4_snapshot"]\n',
                                             'node': 'test_phase4_step4_current_snapshot_checks_valid_tree_before_mutations',
                                             'old': '        shutil.copyfile(repo_root / relative, '
                                                    'destination)\n'
                                                    '    verify = '
                                                    'phase4_gate_tools["verify_phase4_step4_snapshot"]\n'}],
 'tests/unit/test_phase4_contracts.py': [{'new': 'def '
                                                 'test_phase4_step4_approved_control_keeps_independent_step3_anchors(phase4_tools, '
                                                 'phase4_step4_snapshot):\n'
                                                 '    control = json.loads((phase4_step4_snapshot / '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\n',
                                          'node': 'test_phase4_step4_approved_control_keeps_independent_step3_anchors',
                                          'old': 'def '
                                                 'test_phase4_step4_approved_control_keeps_independent_step3_anchors(phase4_tools):\n'
                                                 '    control = json.loads((ROOT / '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\n'},
                                         {'new': 'def '
                                                 'test_phase4_step4_control_rejects_forged_scope_and_stage(phase4_tools, '
                                                 'field, value, phase4_step4_snapshot):\n'
                                                 '    control = json.loads((phase4_step4_snapshot / '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\n',
                                          'node': 'test_phase4_step4_control_rejects_forged_scope_and_stage',
                                          'old': 'def '
                                                 'test_phase4_step4_control_rejects_forged_scope_and_stage(phase4_tools, '
                                                 'field, value):\n'
                                                 '    control = json.loads((ROOT / '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\n'},
                                         {'new': 'def '
                                                 'test_phase4_step4_control_rejects_unapproved_dispatch(phase4_tools, '
                                                 'step, phase4_step4_snapshot):\n'
                                                 '    control = json.loads((phase4_step4_snapshot / '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\n',
                                          'node': 'test_phase4_step4_control_rejects_unapproved_dispatch',
                                          'old': 'def '
                                                 'test_phase4_step4_control_rejects_unapproved_dispatch(phase4_tools, '
                                                 'step):\n'
                                                 '    control = json.loads((ROOT / '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\n'},
                                         {'new': 'def '
                                                 'test_phase4_step4_control_requires_explicit_approval_fields(phase4_tools, '
                                                 'field, phase4_step4_snapshot):\n'
                                                 '    control = json.loads((phase4_step4_snapshot / '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\n',
                                          'node': 'test_phase4_step4_control_requires_explicit_approval_fields',
                                          'old': 'def '
                                                 'test_phase4_step4_control_requires_explicit_approval_fields(phase4_tools, '
                                                 'field):\n'
                                                 '    control = json.loads((ROOT / '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\n'},
                                         {'new': 'def '
                                                 'test_phase4_step4_control_cannot_mint_extra_permission(phase4_tools, '
                                                 'phase4_step4_snapshot):\n'
                                                 '    control = json.loads((phase4_step4_snapshot / '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\n',
                                          'node': 'test_phase4_step4_control_cannot_mint_extra_permission',
                                          'old': 'def '
                                                 'test_phase4_step4_control_cannot_mint_extra_permission(phase4_tools):\n'
                                                 '    control = json.loads((ROOT / '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\n'},
                                         {'new': 'def '
                                                 'test_phase4_step4_historical_migrations_preserve_ten_step3_gate_nodes(phase4_tools, '
                                                 'phase4_step3_snapshot, phase4_step4_snapshot):\n',
                                          'node': 'test_phase4_step4_historical_migrations_preserve_ten_step3_gate_nodes',
                                          'old': 'def '
                                                 'test_phase4_step4_historical_migrations_preserve_ten_step3_gate_nodes(phase4_tools, '
                                                 'phase4_step3_snapshot):\n'},
                                         {'new': '            path, (phase4_step3_snapshot / '
                                                 'path).read_bytes(), (phase4_step4_snapshot / '
                                                 'path).read_bytes(),\n',
                                          'node': 'test_phase4_step4_historical_migrations_preserve_ten_step3_gate_nodes',
                                          'old': '            path, (phase4_step3_snapshot / '
                                                 'path).read_bytes(), (ROOT / path).read_bytes(),\n'},
                                         {'new': 'def '
                                                 'test_phase4_step4_historical_guard_rejects_assertion_and_binding_weakening(phase4_tools, '
                                                 'phase4_step3_snapshot, mutation, phase4_step4_snapshot):\n',
                                          'node': 'test_phase4_step4_historical_guard_rejects_assertion_and_binding_weakening',
                                          'old': 'def '
                                                 'test_phase4_step4_historical_guard_rejects_assertion_and_binding_weakening(phase4_tools, '
                                                 'phase4_step3_snapshot, mutation):\n'},
                                         {'new': '    after = (phase4_step4_snapshot / path).read_bytes()\n'
                                                 '    verify = '
                                                 'phase4_tools["verify_phase4_step4_test_migration"]\n',
                                          'node': 'test_phase4_step4_historical_guard_rejects_assertion_and_binding_weakening',
                                          'old': '    after = (ROOT / path).read_bytes()\n'
                                                 '    verify = '
                                                 'phase4_tools["verify_phase4_step4_test_migration"]\n'}]}


PHASE4_STEP5_ALLOWED = {'.github/workflows/ci.yml',
 '.github/workflows/golden.yml',
 '.github/workflows/release.yml',
 '.github/workflows/security.yml',
 'PHASE_4_BASELINE.json',
 'PHASE_4_DECISIONS.md',
 'docs/architecture.md',
 'docs/report_schema.md',
 'docs/theory_traceability.md',
 'scripts/check_spec_consistency.py',
 'scripts/check_traceability.py',
 'scripts/release_check.py',
 'src/recursive_integrity_toolkit/reports/json_report.py',
 'src/recursive_integrity_toolkit/reports/markdown_report.py',
 'tests/conftest.py',
 'tests/integration/test_ci_workflows.py',
 'tests/integration/test_hero_structure.py',
 'tests/integration/test_license_notices.py',
 'tests/integration/test_no_algorithms.py',
 'tests/integration/test_no_network.py',
 'tests/integration/test_optional_dependency.py',
 'tests/integration/test_owner_ids.py',
 'tests/integration/test_package_import.py',
 'tests/integration/test_package_install.py',
 'tests/integration/test_phase4_gates.py',
 'tests/integration/test_prohibited_structure.py',
 'tests/integration/test_repository_structure.py',
 'tests/integration/test_schema_json.py',
 'tests/unit/test_PR013_report_schema.py',
 'tests/unit/test_PR016_determinism.py',
 'tests/unit/test_PR018_language.py',
 'tests/unit/test_phase4_contracts.py'}


def _phase4_step4_files():
    """Read the exact accepted Step 4 Git tree and verify every blob identity."""
    for suffix, expected in (("^{commit}", PHASE4_STEP4_FINAL), ("^{tree}", PHASE4_STEP4_TREE),
                             (":tests", PHASE4_STEP4_TEST_TREE)):
        if git("rev-parse", PHASE4_STEP4_FINAL + suffix).decode().strip() != expected:
            raise ValueError("Pinned Phase 4 Step 4 identity mismatch")
    objects = {}
    for entry in git("ls-tree", "-rz", PHASE4_STEP4_FINAL).split(b"\0"):
        if not entry:
            continue
        metadata, raw_path = entry.split(b"\t", 1)
        mode, kind, oid = metadata.split()
        path = raw_path.decode("utf-8")
        if (mode not in (b"100644", b"100755") or kind != b"blob" or path in objects
                or path.startswith("/") or ".." in path.split("/") or ".git" in path.split("/")):
            raise ValueError("Unsafe pinned Step 4 Git object")
        objects[path] = oid.decode("ascii")
    if len(objects) != 227:
        raise ValueError("Pinned Step 4 must contain exactly 227 files")
    files = {}
    with zipfile.ZipFile(io.BytesIO(git("archive", "--format=zip", PHASE4_STEP4_FINAL))) as archive:
        names = [item.filename for item in archive.infolist() if not item.is_dir()]
        if len(names) != len(objects) or set(names) != set(objects):
            raise ValueError("Pinned Step 4 archive identity mismatch")
        for name in names:
            raw = archive.read(name)
            oid = hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()
            if oid != objects[name]:
                raise ValueError(f"Pinned Step 4 blob mismatch: {name}")
            files[name] = raw
    return MappingProxyType(files)


def phase4_step5_expected_control() -> dict:
    """Actual Step 5 approval is independent of the mutable control document."""
    prior = _phase4_step4_files()
    result = phase4_step4_expected_control()
    result.update({
        "control_version": "1.4", "active_step": 5,
        "approval_date": PHASE4_STEP5_APPROVAL_DATE, "approval_basis": PHASE4_STEP5_APPROVAL,
        "previous_step_commit": PHASE4_STEP4_FINAL,
        "previous_step_tree": PHASE4_STEP4_TREE,
        "previous_step_test_tree": PHASE4_STEP4_TEST_TREE,
        "previous_step_core_tests": 3071, "previous_step_parquet_tests": 3074,
        "previous_step_files_sha256": {p: hashlib.sha256(raw).hexdigest() for p, raw in sorted(prior.items())},
        "permitted_paths": sorted(PHASE4_STEP5_ALLOWED), "new_files_permitted": [],
        "runtime_changes_authorized": True, "schema_changes_authorized": False,
        "runtime_paths_authorized": sorted(p for p in PHASE4_STEP5_ALLOWED if p.startswith("src/")),
        "schema_paths_authorized": [],
        "step4_historical_binding_nodes": {p: sorted({r["node"] for r in rows})
                                          for p, rows in sorted(PHASE4_STEP5_MIGRATIONS.items())},
    })
    return result


def verify_phase4_step5_control(control: dict, step: int = 5) -> None:
    if type(step) is not int or step != 5 or type(control) is not dict:
        raise ValueError("Unsupported Phase 4 Step 5 stage/control")
    try:
        actual = json.dumps(control, sort_keys=True, ensure_ascii=True, allow_nan=False)
        expected = json.dumps(phase4_step5_expected_control(), sort_keys=True, ensure_ascii=True, allow_nan=False)
    except (TypeError, ValueError) as error:
        raise ValueError("Invalid Phase 4 Step 5 control") from error
    if actual != expected:
        raise ValueError("Phase 4 control differs from the independently approved Step 5 contract")


def verify_phase4_step5_changes(changes: list[tuple[str, str]]) -> None:
    seen = set()
    for status, path in changes:
        if path in seen or path not in PHASE4_STEP5_ALLOWED or status != "M":
            raise ValueError(f"Unapproved Phase 4 Step 5 path/operation: {status} {path}")
        seen.add(path)


def _phase4_step5_header(node, path):
    """Allow explicit test parametrization/fixtures, never definition-time effects."""
    for decorator in node.decorator_list:
        if not isinstance(decorator, ast.Call) or ast.unparse(decorator.func) not in {
                "pytest.fixture", "pytest.mark.parametrize"}:
            raise ValueError(f"Unapproved Step 5 test decorator: {path}:{node.name}")
        if ast.unparse(decorator.func) == "pytest.fixture" and not node.name.startswith("phase4_step"):
            raise ValueError("A Step 5 fixture must have an explicit scoped name")
        if any(keyword.arg is None for keyword in decorator.keywords):
            raise ValueError("Decorator expansion is outside the Step 5 contract")
        for value in [*decorator.args, *(keyword.value for keyword in decorator.keywords)]:
            try:
                ast.literal_eval(value)
            except (ValueError, TypeError, SyntaxError) as error:
                raise ValueError("Step 5 decorator arguments must be literal") from error
    clone = ast.parse(ast.unparse(node)).body[0]
    clone.decorator_list = []
    _phase4_preserve_function_header(clone, path)


def _phase4_step5_append_only(before: bytes, after: bytes, path: str) -> None:
    if not after.startswith(before):
        raise ValueError(f"Inherited Step 4 prefix changed: {path}")
    old, new = ast.parse(before), ast.parse(after)
    bindings = set()
    for node in old.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            bindings.add(node.name)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            bindings.update(alias.asname or alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            bindings.update(child.id for target in targets for child in ast.walk(target) if isinstance(child, ast.Name))
    for node in new.body[len(old.body):]:
        if not isinstance(node, ast.FunctionDef) or node.name in bindings:
            raise ValueError(f"Step 5 addition executes, rebinds or shadows inherited source: {path}")
        allowed_snapshot = path == "tests/conftest.py" and node.name == "phase4_step4_snapshot"
        if not allowed_snapshot and not node.name.startswith(("test_phase4_step5_", "phase4_step5_")):
            raise ValueError(f"Step 5 added test/helper is not explicitly scoped: {path}:{node.name}")
        if path == "tests/conftest.py" and node.name != "phase4_step4_snapshot":
            raise ValueError("Only the pinned Step 4 shared fixture is authorized")
        bindings.add(node.name)
        _phase4_step5_header(node, path)


def verify_phase4_step5_test_migration(path: str, before: bytes, after: bytes) -> None:
    prior = _phase4_step4_files()
    if path not in prior or path not in PHASE4_STEP5_ALLOWED or before != prior[path] or not path.startswith("tests/"):
        raise ValueError("Step 5 migration requires the exact named Step 4 source")
    _phase4_step5_check_test_migration(path, before, after)


def _phase4_step5_check_test_migration(path: str, before: bytes, after: bytes) -> None:
    """Check a source already read from the verified Step 4 immutable mapping."""
    expected = before
    for row in PHASE4_STEP5_MIGRATIONS.get(path, []):
        old, new = row["old"].encode(), row["new"].encode()
        if expected.count(old) != 1:
            raise ValueError("Step 4 historical binding is not unique")
        expected = expected.replace(old, new, 1)
    _phase4_step5_append_only(expected, after, path)


def _phase4_step5_preserve_tooling(before: bytes, after: bytes, path: str) -> None:
    """Preserve exact inherited statements using one source-line split per tree."""
    if path == "scripts/release_check.py":
        old = '    return phase4_cli_main() if explicit_phase4 else main()'
        new = ('    explicit_step5 = "--step=5" in argv or any(a == "--step" and b == "5" for a, b in zip(argv, argv[1:]))\n'
               '    if explicit_phase4 and explicit_step5:\n'
               '        return phase4_step5_cli_main()\n' + old)
        # Earlier preserved dispatch functions contain this source too; bind cli_main only.
        parsed = ast.parse(before)
        entry = next(node for node in parsed.body if isinstance(node, ast.FunctionDef) and node.name == "cli_main")
        old_entry = ast.get_source_segment(before.decode(), entry)
        if old_entry.count(old) != 1:
            raise ValueError("Step 4 release dispatcher identity mismatch")
        replacements = [(old_entry, old_entry.replace(old, new, 1))]
    else:
        old = '    if args.phase == 4 and args.step == 4:\n        return phase4_step4_main(step=args.step)\n'
        new = old + '    if args.phase == 4 and args.step == 5:\n        return phase4_step5_main(step=args.step)\n'
        replacements = [(old, new),
                        ('Choose explicit --phase 3 --step 11 or --phase 4 --step 1 or --phase 4 --step 2 or --phase 4 --step 3 or --phase 4 --step 4',
                         'Choose explicit --phase 3 --step 11 or --phase 4 --step 1 or --phase 4 --step 2 or --phase 4 --step 3 or --phase 4 --step 4 or --phase 4 --step 5')]
    expected = before
    for old, new in replacements:
        if expected.count(old.encode()) != 1:
            raise ValueError(f"Historical dispatcher identity mismatch: {path}")
        expected = expected.replace(old.encode(), new.encode(), 1)
    trees = [ast.parse(expected), ast.parse(after)]
    lines = [expected.splitlines(keepends=True), after.splitlines(keepends=True)]
    def segment(index, node):
        if node.lineno == node.end_lineno:
            return lines[index][node.lineno - 1][node.col_offset:node.end_col_offset]
        return (lines[index][node.lineno - 1][node.col_offset:]
                + b"".join(lines[index][node.lineno:node.end_lineno - 1])
                + lines[index][node.end_lineno - 1][:node.end_col_offset])
    def entry_guard(node):
        return isinstance(node, ast.If) and isinstance(node.test, ast.Compare) and "__name__" in ast.unparse(node.test)
    guards = [n for n in trees[1].body if entry_guard(n)]
    expected_guard = ast.parse('if __name__ == "__main__":\n    raise SystemExit(cli_main())').body[0]
    if len(guards) != 1 or ast.dump(guards[0]) != ast.dump(expected_guard):
        raise ValueError(f"Unapproved Step 5 maintainer entrypoint: {path}")
    historical = [n for n in trees[0].body if not entry_guard(n)]
    current = [n for n in trees[1].body if not entry_guard(n)]
    old_entries = [(segment(0, n), ast.dump(n)) for n in historical]
    cursor = 0
    for node in current:
        if cursor < len(old_entries) and (segment(1, node), ast.dump(node)) == old_entries[cursor]:
            cursor += 1
            continue
        if isinstance(node, ast.FunctionDef) and (node.name == "_phase4_step4_files" or node.name.startswith(
                ("phase4_step5_", "_phase4_step5_", "verify_phase4_step5_", "audit_phase4_step5"))):
            _phase4_preserve_function_header(node, path)
            continue
        if isinstance(node, ast.Assign) and all(isinstance(target, ast.Name) and target.id.startswith(
                ("PHASE4_STEP5_", "PHASE4_STEP4_")) for target in node.targets):
            try:
                ast.literal_eval(node.value)
            except (ValueError, TypeError, SyntaxError) as error:
                raise ValueError(f"Nonliteral added Step 5 maintainer constant: {path}") from error
            continue
        raise ValueError(f"Unapproved Step 5 maintainer addition: {path}")
    if cursor != len(historical):
        raise ValueError(f"Inherited Step 4 maintainer statement changed: {path}")
    def binding_counts(tree):
        counts = {}
        for node in tree.body:
            names = []
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                names = [node.name]
            elif isinstance(node, (ast.Assign, ast.AnnAssign)):
                targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                names = [child.id for target in targets for child in ast.walk(target) if isinstance(child, ast.Name)]
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                names = [alias.asname or alias.name.split(".")[0] for alias in node.names]
            for name in names:
                counts[name] = counts.get(name, 0) + 1
        return counts
    inherited_counts = binding_counts(trees[0])
    for name, count in binding_counts(trees[1]).items():
        if count > inherited_counts.get(name, 1):
            raise ValueError(f"Duplicate Step 5 maintainer binding: {path}:{name}")


def verify_phase4_step5_snapshot(root: Path = ROOT) -> dict:
    prior = _phase4_step4_files()
    for path, raw in prior.items():
        target = root / path
        if not target.is_file() or target.is_symlink():
            raise ValueError(f"Missing or aliased inherited Step 4 file: {path}")
        current = target.read_bytes()
        if path not in PHASE4_STEP5_ALLOWED and current != raw:
            raise ValueError(f"Protected Step 4 bytes changed: {path}")
        if path.startswith("tests/") and path in PHASE4_STEP5_ALLOWED:
            _phase4_step5_check_test_migration(path, raw, current)
        elif path.startswith("scripts/") and path in PHASE4_STEP5_ALLOWED:
            _phase4_step5_preserve_tooling(raw, current, path)
        elif path in {"docs/architecture.md", "docs/theory_traceability.md", "docs/report_schema.md", "PHASE_4_DECISIONS.md"}:
            if not current.startswith(raw):
                raise ValueError(f"Step 4 historical documentation prefix changed: {path}")
    actual_modules = {p.relative_to(root).as_posix() for p in (root / "src/recursive_integrity_toolkit").rglob("*.py")}
    expected_modules = {p for p in prior if p.startswith("src/") and p.endswith(".py")}
    if actual_modules != expected_modules or len(actual_modules) != 40:
        raise ValueError("Step 5 cannot change the runtime module set")
    if {p.name for p in (root / "schemas").iterdir()} != {Path(p).name for p in prior if p.startswith("schemas/")}:
        raise ValueError("Step 5 cannot change the schema set")
    if hashlib.sha256((root / "PHASE_4_PLAN.md").read_bytes()).hexdigest() != PHASE4_PLAN_SHA256:
        raise ValueError("Approved Phase 4 plan changed")
    verify_phase4_step5_control(json.loads((root / "PHASE_4_BASELINE.json").read_text(encoding="utf-8")))
    decisions = (root / "PHASE_4_DECISIONS.md").read_text(encoding="utf-8")
    if PHASE4_STEP5_APPROVAL not in decisions or PHASE4_STEP4_FINAL not in decisions:
        raise ValueError("Actual Step 5 authorization or Step 4 evidence anchor missing")
    if any((root / name).exists() for name in PHASE4_FORBIDDEN_OUTPUTS):
        raise ValueError("Step 5 cannot create Phase 4 completion records or audit outputs")
    import runpy
    checker = runpy.run_path(str(root / "scripts/check_traceability.py"), run_name="phase4_step5_renderer_boundary")
    checker["phase4_step5_renderers_boundary"](root)
    schema_bytes = (root / "schemas/report.schema.json").read_bytes()
    if hashlib.sha256(schema_bytes).hexdigest() != PHASE4_STEP2_REPORT_SCHEMA_SHA256:
        raise ValueError("Step 5 report schema differs from its independently reviewed bytes")
    schema = json.loads(schema_bytes)
    if (schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema"
            or schema.get("type") != "object" or schema.get("additionalProperties") is not False):
        raise ValueError("Step 5 report schema dialect/closed root mismatch")
    return {"package_modules": 40, "frozen_runtime_modules": 38, "frozen_schemas": 5,
            "hero_files_unchanged": 6, "historical_phase3_migrated_nodes": 16,
            "phase_complete": False, "result_contracts_enabled": True,
            "adapters_enabled": True, "privacy_views_enabled": True, "renderers_enabled": True, "cli_analysis_enabled": False}


def audit_phase4_step5(step: int = 5) -> dict:
    verify_phase4_step5_control(json.loads((ROOT / "PHASE_4_BASELINE.json").read_text(encoding="utf-8")), step)
    result = {"phase": 4, "active_step": step, **verify_phase4_step5_snapshot(),
              "phase0_hashes_verified": 16, "publication_authorized": False}
    print(json.dumps(result, indent=2))
    return result


def audit_phase4_step5_diff(step: int = 5) -> dict:
    if type(step) is not int or step != 5:
        raise ValueError("Unsupported Phase 4 Step 5 stage")
    _phase4_step4_files()
    subprocess.run(["git", "-C", str(ROOT), "merge-base", "--is-ancestor", PHASE4_STEP4_FINAL, "HEAD"], check=True)
    raw = git("diff", "--name-status", "--no-renames", "-z", PHASE4_STEP4_FINAL, "--").split(b"\0")
    raw = [part.decode("utf-8") for part in raw if part]
    if len(raw) % 2:
        raise ValueError("Malformed Step 5 Git difference records")
    changes = list(zip(raw[::2], raw[1::2]))
    changes.extend(("A", p.decode()) for p in git("ls-files", "--others", "--exclude-standard", "-z").split(b"\0") if p)
    verify_phase4_step5_changes(changes)
    result = {"previous_step_commit": PHASE4_STEP4_FINAL, "changed_files": len(changes),
              "changes": changes, "step": 5, "scope": "PASS"}
    print(json.dumps(result, indent=2))
    return result


def phase4_step5_baseline_evidence(output: Path) -> dict:
    """Reconcile all inherited identities, including the accepted Step 4 suite."""
    output.mkdir(parents=True, exist_ok=True)
    inherited = phase4_step4_baseline_evidence(output / "phase4-step4-inherited")
    with tempfile.TemporaryDirectory(prefix="rit-p4-step4-identities-") as temp:
        baseline = Path(temp)
        for name, raw in _phase4_step4_files().items():
            target = baseline / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(raw)
        old, old_log = _collect(baseline)
    current, current_log = _collect(ROOT)
    expected = 3074 if os.environ.get("RIT_TEST_PARQUET") == "1" else 3071
    if len(old) != expected or set(old) - set(current):
        raise ValueError("Accepted Phase 4 Step 4 test identities were lost")
    result = {"baseline_commit": PHASE4_STEP4_FINAL, "baseline_test_tree": PHASE4_STEP4_TEST_TREE,
              "baseline_nodeids": old, "current_nodeids": current, "missing_nodeids": [],
              "baseline_tests": len(old), "current_tests": len(current), "inherited": inherited,
              "nodeids_sha256": hashlib.sha256(("\n".join(old)+"\n").encode()).hexdigest()}
    (output / "phase4_step5_test_identity_manifest.json").write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    (output / "phase4-step4-collection.log").write_text(old_log, encoding="utf-8")
    (output / "phase4-step5-collection.log").write_text(current_log, encoding="utf-8")
    print(json.dumps({k: result[k] for k in ("baseline_tests", "current_tests", "missing_nodeids")}, indent=2))
    return result


def phase4_step5_candidate(output: Path, step: int = 5) -> None:
    """Build tested Step 5 intermediate evidence without declaring Phase 4 complete."""
    if os.environ.get("RIT_TEST_PARQUET") != "1" or importlib.util.find_spec("pyarrow") is None:
        raise ValueError("Step 5 candidate evidence requires RIT_TEST_PARQUET=1 and real PyArrow")
    output.mkdir(parents=True, exist_ok=True)
    result = audit_phase4_step5(step)
    result["diff"] = audit_phase4_step5_diff(step)
    if git("status", "--porcelain").strip():
        raise ValueError("Step 5 candidate archive requires committed, clean source")
    result["core"] = verify_junit(output / "core.xml", minimum=3071)
    result["parquet"] = verify_junit(output / "parquet.xml", require_parquet=True, minimum=3074)
    result["core_math_measurements"] = verify_step10_evidence(output / "core.xml", output / "phase4-step5-core-observations.json")
    result["parquet_math_measurements"] = verify_step10_evidence(output / "parquet.xml", output / "phase4-step5-parquet-observations.json")
    identity = phase4_step5_baseline_evidence(output)
    result["test_identity"] = {k: identity[k] for k in ("baseline_tests", "current_tests", "nodeids_sha256")}
    expected = set()
    for node in identity["current_nodeids"]:
        base, bracket, parameter = node.partition("[")
        owner, name = base.rsplit("::", 1)
        expected.add((owner.removesuffix(".py").replace("/", ".").replace("::", "."), name + bracket + parameter))
    for name, parquet in (("core.xml", False), ("parquet.xml", True)):
        cases = {(c.get("classname", ""), c.get("name", "")) for c in ET.parse(output / name).getroot().iter("testcase")}
        target = expected if parquet else {c for c in expected if c[1] not in PARQUET_CASES}
        if cases != target:
            raise ValueError(f"Step 5 JUnit does not execute the entire current suite: {name}")
    wheel, _ = verify_distributions(output / "dist")
    smoke_installed(wheel)
    smoke_installed_duplicates(wheel)
    phase4_step2_installed_contract_smoke(wheel)
    phase4_step3_installed_assembly_smoke(wheel)
    phase4_step4_installed_privacy_smoke(wheel)
    phase4_step5_installed_renderers_smoke(wheel)
    archive = output / "recursive-integrity-toolkit-phase4-step5-candidate.zip"
    subprocess.run(["git", "-C", str(ROOT), "archive", "--format=zip", "--prefix=recursive-integrity-toolkit/", "HEAD", "-o", str(archive.resolve())], check=True)
    tracked = {p for p in git("ls-files", "-z").decode().split("\0") if p}
    with zipfile.ZipFile(archive) as zipped:
        entries = [item.filename for item in zipped.infolist() if not item.is_dir()]
        prefix = "recursive-integrity-toolkit/"
        if (len(entries) != len(set(entries)) or any(not name.startswith(prefix) for name in entries)):
            raise ValueError("Step 5 source archive has duplicate or unprefixed entries")
        names = {name.removeprefix(prefix) for name in entries}
        if names != tracked or len(tracked) != 227 or len(entries) != 227:
            raise ValueError("Step 5 source archive file set mismatch")
        for name in names:
            if zipped.read("recursive-integrity-toolkit/"+name) != (ROOT / name).read_bytes():
                raise ValueError(f"Step 5 source archive byte mismatch: {name}")
    result.update({"commit": git("rev-parse", "HEAD").decode().strip(),
                   "tree": git("rev-parse", "HEAD^{tree}").decode().strip(),
                   "source_archive": archive.name, "tracked_files": len(tracked),
                   "python": sys.version, "platform": sys.platform,
                   "versions": {name: importlib.metadata.version(name) for name in ("numpy", "pandas", "pytest")}})
    (output / "phase4_step5_execution_metadata.json").write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    (output / "phase4_step5_repository_files.sha256").write_text("".join(f"{hashlib.sha256((ROOT/name).read_bytes()).hexdigest()}  {name}\n" for name in sorted(tracked)), encoding="utf-8")
    paths = sorted(p for p in output.rglob("*") if p.is_file() and p.name != "phase4_step5_artifacts.sha256")
    (output / "phase4_step5_artifacts.sha256").write_text("".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(output).as_posix()}\n" for p in paths), encoding="utf-8")
    print(f"Phase 4 Step 5 candidate: {len(tracked)} source files verified; Phase 4 remains incomplete.")


def phase4_step5_cli_main() -> int:
    parser = argparse.ArgumentParser(description="Phase 4 Step 5 maintainer gate")
    parser.add_argument("--phase", type=int, choices=(4,), required=True)
    parser.add_argument("--step", type=int, choices=(5,), required=True)
    parser.add_argument("--diff", action="store_true")
    parser.add_argument("--junit", type=Path)
    parser.add_argument("--require-parquet", action="store_true")
    parser.add_argument("--minimum-tests", type=int, default=1)
    parser.add_argument("--baseline-evidence", type=Path)
    parser.add_argument("--dist", type=Path)
    parser.add_argument("--smoke-wheel", type=Path)
    parser.add_argument("--candidate", type=Path)
    parser.add_argument("--delivery", type=Path)
    args = parser.parse_args()
    if args.delivery is not None:
        raise ValueError("Phase 4 Step 5 cannot certify a final phase delivery")
    if args.junit is not None:
        verify_junit(args.junit, require_parquet=args.require_parquet, minimum=args.minimum_tests)
    elif args.baseline_evidence is not None:
        phase4_step5_baseline_evidence(args.baseline_evidence)
    elif args.dist is not None:
        audit_phase4_step5(args.step)
        wheel, _ = verify_distributions(args.dist)
        smoke_installed(wheel)
        smoke_installed_duplicates(wheel)
        phase4_step2_installed_contract_smoke(wheel)
        phase4_step3_installed_assembly_smoke(wheel)
        phase4_step4_installed_privacy_smoke(wheel)
        phase4_step5_installed_renderers_smoke(wheel)
    elif args.smoke_wheel is not None:
        smoke_installed(args.smoke_wheel)
    elif args.candidate is not None:
        phase4_step5_candidate(args.candidate, args.step)
    else:
        audit_phase4_step5(args.step)
        if args.diff:
            audit_phase4_step5_diff(args.step)
    return 0


def phase4_step5_installed_renderers_smoke(wheel: Path) -> None:
    """Exercise the installed pure renderers against prepared protected evidence."""
    with tempfile.TemporaryDirectory(prefix="rit-p4-step5-installed-renderers-") as temp:
        work = Path(temp)
        subprocess.run([sys.executable, "-m", "venv", str(work / "venv")], check=True)
        bindir = work / "venv" / ("Scripts" if os.name == "nt" else "bin")
        python = bindir / ("python.exe" if os.name == "nt" else "python")
        subprocess.run([str(python), "-m", "pip", "install", "--no-index", "--no-deps", str(wheel.resolve())],
                       cwd=work, check=True)
        program = r'''import builtins, copy, importlib.abc, io, json, socket, sys
from pathlib import Path
from types import MappingProxyType
blocked_roots = {'numpy', 'pandas', 'pyarrow', 'jsonschema', 'referencing', 'networkx', 'scipy', 'sklearn'}
owner_layers = tuple('recursive_integrity_toolkit.' + name for name in (
    'metrics', 'io', 'representations', 'observability', 'lineage', 'config', 'reports.assembly',
    'utils.hashing', 'utils.logging', 'cli', 'reports.html_report'))
class DenyOwnerImports(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in blocked_roots or any(
                fullname == layer or fullname.startswith(layer + '.') for layer in owner_layers):
            raise AssertionError('installed renderer imported an analytical/input/effect owner: ' + fullname)
barrier = DenyOwnerImports()
sys.meta_path.insert(0, barrier)
import recursive_integrity_toolkit.reports.json_report as json_renderer
import recursive_integrity_toolkit.reports.markdown_report as markdown_renderer
from recursive_integrity_toolkit.result import CanonicalReport, SafeReportView, SECTION_ORDER
for module in (json_renderer, markdown_renderer):
    assert Path(module.__file__).resolve().is_relative_to(Path(sys.argv[1]) / 'venv')
    assert not Path(module.__file__).resolve().is_relative_to(Path(sys.argv[2]) / 'src')
assert not blocked_roots.intersection(sys.modules)
assert not any(name == layer or name.startswith(layer + '.') for name in sys.modules for layer in owner_layers)
sys.meta_path.remove(barrier)
# Prepare accepted calculation and privacy results before testing the pure render boundary.
from recursive_integrity_toolkit.models import (
    BundleValidationResult, Capability, CapabilityKey, CapabilityStatus,
    CanonicalRow, FileFormat, FileInventoryEntry, FileRole, ProvenanceMatch, RecordKey, RowLocation,
    ObservabilityAssessment, ProvenanceJoinResult, ValidationCoverage,
    ValidationMessage, ValidationSeverity, VersionOrderResult,
)
from recursive_integrity_toolkit.config import RepresentationConfig, resolve_phase4_options
from recursive_integrity_toolkit.representations.field import assign_field_states
from recursive_integrity_toolkit.metrics.diversity import calculate_state_distribution
from recursive_integrity_toolkit.metrics.resampling import expected_diversity_after_steps
from recursive_integrity_toolkit.reports.assembly import assemble_report, privacy_view, build_run_metadata
from recursive_integrity_toolkit.utils.hashing import IdentifierProtection
hostile = 'v1|<script>alert(1)</script>[link](javascript:run)' + chr(10) + '## Forged heading' + chr(27) + chr(0x202e) + '中文🙂'
rows = tuple(CanonicalRow('records', RecordKey(hostile, identifier),
    MappingProxyType({'dataset_version': hostile, 'record_id': identifier,
                      'content': 'RAW_CONTENT_MUST_NOT_APPEAR', 'topic': topic}),
    MappingProxyType({}), MappingProxyType({}),
    location=RowLocation(FileRole.RECORDS_PRIMARY, 'fixture.jsonl', index, index))
    for index, (identifier, topic) in enumerate((('a', 'one'), ('b', 'two')), 1))
represented = assign_field_states(rows, dataset_versions=(hostile,), scope_id='installed:v1',
    config=RepresentationConfig('topic', 'topic_field', 'topic', 'installed-fixture-v1', 'error'))
distribution = calculate_state_distribution(represented)
expected = expected_diversity_after_steps({'one': 0.5, 'two': 0.5}, resample_size=2,
    steps=2, scope=distribution.unweighted.scope, representation=distribution.unweighted.representation)
assert distribution.unweighted.gini_simpson_diversity.value == 0.5
assert expected.expected_diversity == (0.5, 0.25, 0.125)
keys = tuple(row.record_key for row in rows)
coverage = ValidationCoverage(0, 2, 'all_valid_records')
join = ProvenanceJoinResult((hostile,), keys, False,
    tuple(ProvenanceMatch(key, None) for key in keys), keys, coverage, coverage, coverage, ())
caps = {key: Capability(CapabilityStatus.UNAVAILABLE, reason_codes=('R_MISSING_EVIDENCE',))
    for key in CapabilityKey}
caps[CapabilityKey.INGESTION] = Capability(CapabilityStatus.AVAILABLE)
caps[CapabilityKey.CONTENT_DIAGNOSTICS] = Capability(CapabilityStatus.AVAILABLE)
bundle = BundleValidationResult(
    inventory=(FileInventoryEntry(FileRole.RECORDS_PRIMARY, Path('fixture.jsonl'), FileFormat.JSONL,
        128, '0' * 64, 2, ('dataset_version', 'record_id', 'content', 'topic')),),
    records=rows, provenance=None, provenance_join=join,
    version_order=VersionOrderResult((hostile,), (hostile,), 'single_version', {}, {}), generation=None,
    observability=ObservabilityAssessment(1, caps), mapping_traces=(), content_read_keys=(),
    validation_messages=(ValidationMessage('E_FILE_PARSE', ValidationSeverity.ERROR,
        'PRIVATE_MESSAGE_MUST_NOT_APPEAR'),),
)
fixed = IdentifierProtection.create(secret=b'rit-step5-installed-render-secret-2026')
views = []
for mode, cli in (('standard', {}), ('redacted', {'redacted': True, 'record_ids': 'hash'})):
    run = build_run_metadata(options=resolve_phase4_options(cli=cli), run_id='installed-render-case')
    report = assemble_report(bundle, run=run, distributions=(distribution,), expected_diversity=expected)
    view = privacy_view(report, mode=mode, protection=fixed)
    assert type(view) is SafeReportView
    views.append((report, view, copy.deepcopy(view.to_dict())))
assert views[0][2]['run']['run_status'] == 'partial'
assert views[0][2]['simulations']['closed_resampling']['status'] == 'experimental'
assert views[0][2]['capabilities']['lineage']['execution_status'] == 'deferred'
# After this point even an already imported owner cannot execute a function.
def denied(*args, **kwargs):
    raise AssertionError('installed renderer attempted file, network or process access')
def deny_execution(frame, event, argument):
    if event == 'call':
        source = frame.f_code.co_filename.replace(chr(92), '/')
        if any('/recursive_integrity_toolkit/' + layer in source for layer in (
                'metrics/', 'io/', 'representations/', 'observability/', 'lineage/',
                'reports/assembly.py', 'config.py', 'utils/hashing.py', 'utils/logging.py')):
            raise AssertionError('installed renderer executed an evidence/input/effect owner: ' + frame.f_code.co_name)
def deny_effects(event, arguments):
    if event in ('open', 'os.listdir', 'os.scandir', 'os.system', 'subprocess.Popen') or event.startswith('socket.'):
        raise AssertionError('installed renderer attempted an external effect: ' + event)
sys.meta_path.insert(0, barrier)
socket.create_connection = denied
socket.getaddrinfo = denied
socket.socket.connect = denied
socket.socket.connect_ex = denied
builtins.open = denied
io.open = denied
sys.setprofile(deny_execution)
sys.addaudithook(deny_effects)
headings = ['Run metadata', 'Input inventory', 'Observability summary', 'Capability matrix',
    'Observed facts', 'Derived metrics', 'Proxy signals', 'Simulations', 'Unavailable conclusions',
    'Recommended next metadata', 'Warnings', 'Errors']
for report, view, original in views:
    rendered_json = json_renderer.render_json(view)
    rendered_markdown = markdown_renderer.render_markdown(view)
    assert type(rendered_json) is str and type(rendered_markdown) is str
    assert json.loads(rendered_json) == original
    assert tuple(json.loads(rendered_json)) == SECTION_ORDER
    assert rendered_json.endswith(chr(10)) and not rendered_json.endswith(chr(10) * 2)
    assert rendered_markdown.endswith(chr(10)) and not rendered_markdown.endswith(chr(10) * 2)
    assert chr(13) not in rendered_json and chr(13) not in rendered_markdown
    assert rendered_json.encode('utf-8').decode('utf-8') == rendered_json
    assert rendered_markdown.encode('utf-8').decode('utf-8') == rendered_markdown
    assert rendered_markdown.splitlines()[0] == '# Recursive Integrity Audit Report'
    assert [line[3:] for line in rendered_markdown.splitlines() if line.startswith('## ')] == headings
    assert rendered_json == json_renderer.render_json(view)
    assert rendered_markdown == markdown_renderer.render_markdown(view)
    for required in ('observed_fact', 'derived_metric', 'proxy_signal', 'simulation', 'unavailable_conclusion',
                     'partial', 'deferred', 'experimental', 'unavailable', 'not_recorded',
                     '0.5', '0.25', '0.125', 'denominator', 'ratio', 'record_count'):
        assert required in rendered_markdown, required
    for forbidden in ('RAW_CONTENT_MUST_NOT_APPEAR', 'PRIVATE_MESSAGE_MUST_NOT_APPEAR',
                      '<script>', '</script>', chr(27), chr(0x202e)):
        assert forbidden not in rendered_markdown, repr(forbidden)
    outside_code = ''.join(rendered_markdown.split('`')[::2])
    assert '[link](javascript:run)' not in outside_code
    assert view.to_dict() == original
    for bad in (report, original, None, object()):
        for renderer in (json_renderer.render_json, markdown_renderer.render_markdown):
            try:
                renderer(bad)
            except (TypeError, ValueError):
                pass
            else:
                raise AssertionError('installed renderer accepted an unprotected input')
standard_json = json_renderer.render_json(views[0][1])
standard_markdown = markdown_renderer.render_markdown(views[0][1])
assert hostile in json.loads(standard_json)['inputs']['scope']['dataset_versions']
assert '中文🙂' in standard_markdown and '\\u003cscript\\u003e' in standard_markdown
assert '\\u007c' in standard_markdown and '\\n## Forged heading' in standard_markdown
assert hostile not in json_renderer.render_json(views[1][1])
assert not blocked_roots.intersection(sys.modules)
sys.setprofile(None)
print('installed Step 5: exact protected JSON roundtrip, twelve ordered Markdown sections, five evidence classes, partial/deferred/experimental status, null reasons, exact prepared values, Unicode/injection escaping and deterministic immutable views; analytical/input imports and execution, file I/O, network and process effects blocked: PASS')
'''
        subprocess.run([str(python), "-I", "-c", program, str(work), str(ROOT)], cwd=work, check=True)


# Phase 4 Step 6: safe local publication; no CLI or analytical expansion.


PHASE4_STEP5_FINAL = 'c1667179e895a798bba2349960162542efa5ef87'


PHASE4_STEP5_TREE = 'd83f9fc8e0b569f2d796bd2a83b87422fe350fba'


PHASE4_STEP5_TEST_TREE = '974f8e65904c24ed4e226996eaf571aab6123965'


PHASE4_STEP6_APPROVAL = '批准开始Phase 4   **Step 6**'


PHASE4_STEP6_APPROVAL_DATE = '2026-09-20'


PHASE4_STEP6_NEW = ('tests/unit/test_phase4_output_safety.py',)


PHASE4_STEP6_MIGRATIONS = {'tests/integration/test_phase4_gates.py': [{'new': 'def '
                                                    'test_phase4_step5_current_runtime_opens_only_renderers_and_freezes_schema(repo_root, '
                                                    'phase4_step4_snapshot, phase4_step5_snapshot):\n'
                                                    '    repo_root = phase4_step5_snapshot\n'
                                                    '    package = "src/recursive_integrity_toolkit"\n'
                                                    '    current = {path.relative_to(repo_root).as_posix(): '
                                                    'hashlib.sha256(path.read_bytes()).hexdigest()\n'
                                                    '               for path in (repo_root / '
                                                    'package).rglob("*.py")}\n'
                                                    '    frozen = '
                                                    '{path.relative_to(phase4_step4_snapshot).as_posix(): '
                                                    'hashlib.sha256(path.read_bytes()).hexdigest()\n'
                                                    '              for path in (phase4_step4_snapshot / '
                                                    'package).rglob("*.py")}\n'
                                                    '    assert len(current) == len(frozen) == 40\n'
                                                    '    assert current.keys() == frozen.keys()\n'
                                                    '    opened = {package + "/" + relative for relative in '
                                                    '(\n'
                                                    '        "reports/json_report.py", '
                                                    '"reports/markdown_report.py",\n'
                                                    '    )}\n'
                                                    '    assert {path for path in current if current[path] '
                                                    '!= frozen[path]} == opened\n'
                                                    '    assert {path: digest for path, digest in '
                                                    'current.items() if path not in opened} == {\n'
                                                    '        path: digest for path, digest in frozen.items() '
                                                    'if path not in opened\n'
                                                    '    }\n'
                                                    '    schemas = {path.name: path.read_bytes() for path in '
                                                    '(repo_root / "schemas").glob("*.json")}\n'
                                                    '    assert len(schemas) == 5\n'
                                                    '    assert schemas == {path.name: path.read_bytes() for '
                                                    'path in (phase4_step4_snapshot / '
                                                    '"schemas").glob("*.json")}',
                                             'node': 'test_phase4_step5_current_runtime_opens_only_renderers_and_freezes_schema',
                                             'old': 'def '
                                                    'test_phase4_step5_current_runtime_opens_only_renderers_and_freezes_schema(repo_root, '
                                                    'phase4_step4_snapshot):\n'
                                                    '    package = "src/recursive_integrity_toolkit"\n'
                                                    '    current = {path.relative_to(repo_root).as_posix(): '
                                                    'hashlib.sha256(path.read_bytes()).hexdigest()\n'
                                                    '               for path in (repo_root / '
                                                    'package).rglob("*.py")}\n'
                                                    '    frozen = '
                                                    '{path.relative_to(phase4_step4_snapshot).as_posix(): '
                                                    'hashlib.sha256(path.read_bytes()).hexdigest()\n'
                                                    '              for path in (phase4_step4_snapshot / '
                                                    'package).rglob("*.py")}\n'
                                                    '    assert len(current) == len(frozen) == 40\n'
                                                    '    assert current.keys() == frozen.keys()\n'
                                                    '    opened = {package + "/" + relative for relative in '
                                                    '(\n'
                                                    '        "reports/json_report.py", '
                                                    '"reports/markdown_report.py",\n'
                                                    '    )}\n'
                                                    '    assert {path for path in current if current[path] '
                                                    '!= frozen[path]} == opened\n'
                                                    '    assert {path: digest for path, digest in '
                                                    'current.items() if path not in opened} == {\n'
                                                    '        path: digest for path, digest in frozen.items() '
                                                    'if path not in opened\n'
                                                    '    }\n'
                                                    '    schemas = {path.name: path.read_bytes() for path in '
                                                    '(repo_root / "schemas").glob("*.json")}\n'
                                                    '    assert len(schemas) == 5\n'
                                                    '    assert schemas == {path.name: path.read_bytes() for '
                                                    'path in (phase4_step4_snapshot / '
                                                    '"schemas").glob("*.json")}'},
                                            {'new': 'def '
                                                    'test_phase4_step5_current_workflows_preserve_matrix_and_use_active_dispatch(repo_root, '
                                                    'phase4_step5_snapshot):\n'
                                                    '    repo_root = phase4_step5_snapshot\n'
                                                    '    names = {"ci.yml", "golden.yml", "security.yml", '
                                                    '"release.yml"}\n'
                                                    '    root = repo_root / ".github/workflows"\n'
                                                    '    expected_timeouts = {"ci.yml": [60, 20], '
                                                    '"golden.yml": [15], "security.yml": [20], '
                                                    '"release.yml": [25]}\n'
                                                    '    assert {path.name for path in root.glob("*.yml")} '
                                                    '== names\n'
                                                    '    for name in sorted(names):\n'
                                                    '        text = (root / '
                                                    'name).read_text(encoding="utf-8")\n'
                                                    '        assert [int(line.split(":", 1)[1]) for line in '
                                                    'text.splitlines()\n'
                                                    '                if '
                                                    'line.strip().startswith("timeout-minutes:")] == '
                                                    'expected_timeouts[name]\n'
                                                    '        assert "Phase 4 Step 5" in text, name\n'
                                                    '        assert "--phase 4 --step 5" in text, name\n'
                                                    '        for older in ("--phase 4 --step 4", "--phase 4 '
                                                    '--step 3", "--phase 4 --step 2", "--phase 4 --step 1", '
                                                    '"--phase 3 --step 11"):\n'
                                                    '            assert older not in text, (name, older)\n'
                                                    '        assert "permissions:\\n  contents: read" in '
                                                    'text\n'
                                                    '        assert "persist-credentials: false" in text\n'
                                                    '        assert "timeout-minutes:" in text and "set -euo '
                                                    'pipefail" in text\n'
                                                    '        assert "actions/upload-artifact@v4" in text and '
                                                    '"if-no-files-found: error" in text\n'
                                                    '        for line in text.splitlines():\n'
                                                    '            if "python scripts/release_check.py" in '
                                                    'line:\n'
                                                    '                assert "--phase 4 --step 5" in line, '
                                                    '(name, line)\n'
                                                    '        for forbidden in ("continue-on-error:", "|| '
                                                    'true", "contents: write", "id-token: write", "twine '
                                                    'upload", "git push"):\n'
                                                    '            assert forbidden not in text, (name, '
                                                    'forbidden)\n'
                                                    '    ci = (root / "ci.yml").read_text(encoding="utf-8")\n'
                                                    "    for required in ('os: [ubuntu-latest, "
                                                    'windows-latest]\', \'python-version: ["3.11", '
                                                    '"3.12"]\',\n'
                                                    "                     'dependencies: [current, "
                                                    'minimum]\', \'"numpy==2.0.0" "pandas==2.2.2"\',\n'
                                                    '                     \'RIT_TEST_PARQUET: "0"\', '
                                                    '\'RIT_TEST_PARQUET: "1"\', \'--require-parquet\',\n'
                                                    "                     '--baseline-evidence', 'python -m "
                                                    "pip check',\n"
                                                    "                     '--minimum-tests 3071', "
                                                    "'--minimum-tests 3074',\n"
                                                    '                     "find_spec(\'pyarrow\') is None", '
                                                    "'import pyarrow'):\n"
                                                    '        assert required in ci\n'
                                                    '    assert ci.count("python -m pytest -p '
                                                    'no:cacheprovider -q --junitxml=") == 2\n'
                                                    '    assert " -k " not in ci\n'
                                                    '    golden = (root / '
                                                    '"golden.yml").read_text(encoding="utf-8")\n'
                                                    '    for required in '
                                                    '("tests/golden/test_phase3_math.py", '
                                                    '"tests/integration/test_hero_structure.py",\n'
                                                    '                     '
                                                    '"tests/integration/test_phase3_metric_pipeline.py"):\n'
                                                    '        assert required in golden\n'
                                                    '    security = (root / '
                                                    '"security.yml").read_text(encoding="utf-8")\n'
                                                    '    for required in '
                                                    "('tests/integration/test_no_network.py', "
                                                    "'tests/integration/test_optional_dependency.py',\n"
                                                    '                     '
                                                    "'tests/unit/test_PR012_evidence_classes.py', "
                                                    "'tests/unit/test_PR013_report_schema.py',\n"
                                                    '                     '
                                                    "'tests/unit/test_PR014_unavailable.py', "
                                                    "'tests/unit/test_PR015_redaction.py',\n"
                                                    '                     '
                                                    "'tests/unit/test_PR016_determinism.py', "
                                                    "'tests/unit/test_PR018_language.py',\n"
                                                    '                     '
                                                    "'tests/integration/test_partial_provenance_report.py',\n"
                                                    '                     '
                                                    "'tests/integration/test_partial_lineage_report.py',\n"
                                                    '                     '
                                                    "'tests/unit/test_phase4_contracts.py', "
                                                    "'tests/integration/test_phase4_gates.py'):\n"
                                                    '        assert required in security\n'
                                                    '    release = (root / '
                                                    '"release.yml").read_text(encoding="utf-8")\n'
                                                    '    assert "python -m build" in release and "python -m '
                                                    'twine check --strict" in release\n'
                                                    '    assert "--dist" in release and "--candidate" in '
                                                    'release\n'
                                                    '    assert "--delivery" not in release\n'
                                                    '    assert '
                                                    '"recursive-integrity-toolkit-phase4-step5-candidate" in '
                                                    'release\n'
                                                    '    assert "rit-phase4-step4" not in release\n'
                                                    '    assert "--minimum-tests 3071" in release and '
                                                    '"--minimum-tests 3074" in release\n'
                                                    '    assert release.count("python -m pytest -p '
                                                    'no:cacheprovider -q --junitxml=") == 2',
                                             'node': 'test_phase4_step5_current_workflows_preserve_matrix_and_use_active_dispatch',
                                             'old': 'def '
                                                    'test_phase4_step5_current_workflows_preserve_matrix_and_use_active_dispatch(repo_root):\n'
                                                    '    names = {"ci.yml", "golden.yml", "security.yml", '
                                                    '"release.yml"}\n'
                                                    '    root = repo_root / ".github/workflows"\n'
                                                    '    expected_timeouts = {"ci.yml": [60, 20], '
                                                    '"golden.yml": [15], "security.yml": [20], '
                                                    '"release.yml": [25]}\n'
                                                    '    assert {path.name for path in root.glob("*.yml")} '
                                                    '== names\n'
                                                    '    for name in sorted(names):\n'
                                                    '        text = (root / '
                                                    'name).read_text(encoding="utf-8")\n'
                                                    '        assert [int(line.split(":", 1)[1]) for line in '
                                                    'text.splitlines()\n'
                                                    '                if '
                                                    'line.strip().startswith("timeout-minutes:")] == '
                                                    'expected_timeouts[name]\n'
                                                    '        assert "Phase 4 Step 5" in text, name\n'
                                                    '        assert "--phase 4 --step 5" in text, name\n'
                                                    '        for older in ("--phase 4 --step 4", "--phase 4 '
                                                    '--step 3", "--phase 4 --step 2", "--phase 4 --step 1", '
                                                    '"--phase 3 --step 11"):\n'
                                                    '            assert older not in text, (name, older)\n'
                                                    '        assert "permissions:\\n  contents: read" in '
                                                    'text\n'
                                                    '        assert "persist-credentials: false" in text\n'
                                                    '        assert "timeout-minutes:" in text and "set -euo '
                                                    'pipefail" in text\n'
                                                    '        assert "actions/upload-artifact@v4" in text and '
                                                    '"if-no-files-found: error" in text\n'
                                                    '        for line in text.splitlines():\n'
                                                    '            if "python scripts/release_check.py" in '
                                                    'line:\n'
                                                    '                assert "--phase 4 --step 5" in line, '
                                                    '(name, line)\n'
                                                    '        for forbidden in ("continue-on-error:", "|| '
                                                    'true", "contents: write", "id-token: write", "twine '
                                                    'upload", "git push"):\n'
                                                    '            assert forbidden not in text, (name, '
                                                    'forbidden)\n'
                                                    '    ci = (root / "ci.yml").read_text(encoding="utf-8")\n'
                                                    "    for required in ('os: [ubuntu-latest, "
                                                    'windows-latest]\', \'python-version: ["3.11", '
                                                    '"3.12"]\',\n'
                                                    "                     'dependencies: [current, "
                                                    'minimum]\', \'"numpy==2.0.0" "pandas==2.2.2"\',\n'
                                                    '                     \'RIT_TEST_PARQUET: "0"\', '
                                                    '\'RIT_TEST_PARQUET: "1"\', \'--require-parquet\',\n'
                                                    "                     '--baseline-evidence', 'python -m "
                                                    "pip check',\n"
                                                    "                     '--minimum-tests 3071', "
                                                    "'--minimum-tests 3074',\n"
                                                    '                     "find_spec(\'pyarrow\') is None", '
                                                    "'import pyarrow'):\n"
                                                    '        assert required in ci\n'
                                                    '    assert ci.count("python -m pytest -p '
                                                    'no:cacheprovider -q --junitxml=") == 2\n'
                                                    '    assert " -k " not in ci\n'
                                                    '    golden = (root / '
                                                    '"golden.yml").read_text(encoding="utf-8")\n'
                                                    '    for required in '
                                                    '("tests/golden/test_phase3_math.py", '
                                                    '"tests/integration/test_hero_structure.py",\n'
                                                    '                     '
                                                    '"tests/integration/test_phase3_metric_pipeline.py"):\n'
                                                    '        assert required in golden\n'
                                                    '    security = (root / '
                                                    '"security.yml").read_text(encoding="utf-8")\n'
                                                    '    for required in '
                                                    "('tests/integration/test_no_network.py', "
                                                    "'tests/integration/test_optional_dependency.py',\n"
                                                    '                     '
                                                    "'tests/unit/test_PR012_evidence_classes.py', "
                                                    "'tests/unit/test_PR013_report_schema.py',\n"
                                                    '                     '
                                                    "'tests/unit/test_PR014_unavailable.py', "
                                                    "'tests/unit/test_PR015_redaction.py',\n"
                                                    '                     '
                                                    "'tests/unit/test_PR016_determinism.py', "
                                                    "'tests/unit/test_PR018_language.py',\n"
                                                    '                     '
                                                    "'tests/integration/test_partial_provenance_report.py',\n"
                                                    '                     '
                                                    "'tests/integration/test_partial_lineage_report.py',\n"
                                                    '                     '
                                                    "'tests/unit/test_phase4_contracts.py', "
                                                    "'tests/integration/test_phase4_gates.py'):\n"
                                                    '        assert required in security\n'
                                                    '    release = (root / '
                                                    '"release.yml").read_text(encoding="utf-8")\n'
                                                    '    assert "python -m build" in release and "python -m '
                                                    'twine check --strict" in release\n'
                                                    '    assert "--dist" in release and "--candidate" in '
                                                    'release\n'
                                                    '    assert "--delivery" not in release\n'
                                                    '    assert '
                                                    '"recursive-integrity-toolkit-phase4-step5-candidate" in '
                                                    'release\n'
                                                    '    assert "rit-phase4-step4" not in release\n'
                                                    '    assert "--minimum-tests 3071" in release and '
                                                    '"--minimum-tests 3074" in release\n'
                                                    '    assert release.count("python -m pytest -p '
                                                    'no:cacheprovider -q --junitxml=") == 2'},
                                            {'new': 'def '
                                                    'test_phase4_step5_current_snapshot_checks_valid_tree_before_mutations(repo_root, '
                                                    'tmp_path, phase4_gate_tools, mutation, '
                                                    'phase4_step5_snapshot):\n'
                                                    '    import json\n'
                                                    '\n'
                                                    '    paths = '
                                                    '{path.relative_to(phase4_step5_snapshot).as_posix()\n'
                                                    '             for path in '
                                                    'phase4_step5_snapshot.rglob("*") if path.is_file()}\n'
                                                    '    assert len(paths) == 227\n'
                                                    '    for relative in sorted(paths):\n'
                                                    '        destination = tmp_path / relative\n'
                                                    '        destination.parent.mkdir(parents=True, '
                                                    'exist_ok=True)\n'
                                                    '        shutil.copyfile(phase4_step5_snapshot / '
                                                    'relative, destination)\n'
                                                    '    verify = '
                                                    'phase4_gate_tools["verify_phase4_step5_snapshot"]\n'
                                                    '    baseline = verify(tmp_path)\n'
                                                    '    assert baseline["package_modules"] == 40\n'
                                                    '    assert baseline["frozen_runtime_modules"] == 38\n'
                                                    '    assert baseline["frozen_schemas"] == 5\n'
                                                    '    assert baseline["result_contracts_enabled"] is '
                                                    'True\n'
                                                    '    assert baseline["adapters_enabled"] is True\n'
                                                    '    assert baseline["privacy_views_enabled"] is True\n'
                                                    '    assert baseline["renderers_enabled"] is True\n'
                                                    '    assert baseline["cli_analysis_enabled"] is False\n'
                                                    '    assert baseline["phase_complete"] is False\n'
                                                    '    if mutation == "unchanged":\n'
                                                    '        return\n'
                                                    '    replacements = {\n'
                                                    '        "formula": '
                                                    '("src/recursive_integrity_toolkit/metrics/diversity.py",\n'
                                                    '                    b"diversity = 1.0 - concentration", '
                                                    'b"diversity = 0.5 - concentration"),\n'
                                                    '        "math_oracle": '
                                                    '("tests/golden/phase3_math_cases.json", '
                                                    'b\'"v2_support":5\', b\'"v2_support":3\'),\n'
                                                    '        "hero": ("examples/hero/records_v2.csv", '
                                                    'b"v2_08,v2,", b"v2_99,v2,"),\n'
                                                    '        "dependency": ("pyproject.toml", b"numpy>=2.0", '
                                                    'b"numpy>=3.0"),\n'
                                                    '        "historical_assertion": '
                                                    '("tests/unit/test_phase4_contracts.py",\n'
                                                    "                                 b'    assert "
                                                    'control["active_phase"] == 4 and control["active_step"] '
                                                    "== 4\\n',\n"
                                                    '                                 b"    assert '
                                                    'True\\n"),\n'
                                                    '        "historical_tooling": '
                                                    '("scripts/release_check.py",\n'
                                                    '                               b"def '
                                                    'verify_phase4_step4_control(control: dict, step: int = '
                                                    '4) -> None:",\n'
                                                    '                               b"def '
                                                    'verify_phase4_step4_control(control: dict, step: int = '
                                                    '4) -> None:\\n    return"),\n'
                                                    '        "historical_binding": '
                                                    '("tests/integration/test_phase4_gates.py",\n'
                                                    '                               b"def '
                                                    'test_phase4_step4_current_workflows_preserve_matrix_and_use_active_dispatch(repo_root, '
                                                    'phase4_step4_snapshot):\\n    repo_root = '
                                                    'phase4_step4_snapshot\\n",\n'
                                                    '                               b"def '
                                                    'test_phase4_step4_current_workflows_preserve_matrix_and_use_active_dispatch(repo_root, '
                                                    'phase4_step4_snapshot):\\n"),\n'
                                                    '        "historical_document": '
                                                    '("docs/report_schema.md", b"# Report Schema\\n",\n'
                                                    '                                b"# Unauthorized '
                                                    'historical document\\n"),\n'
                                                    '        "input_hash_helper": '
                                                    '("src/recursive_integrity_toolkit/utils/hashing.py",\n'
                                                    '                              b"return '
                                                    'hashlib.sha256(data).hexdigest()", b"return '
                                                    'hashlib.sha256(b\'changed\').hexdigest()"),\n'
                                                    '        "config_resolver_helper": '
                                                    '("src/recursive_integrity_toolkit/config.py",\n'
                                                    '                                   b"def '
                                                    'resolve_config(", b"def resolve_config_disabled("),\n'
                                                    '    }\n'
                                                    '    appended = {\n'
                                                    '        "frozen_model": '
                                                    '"src/recursive_integrity_toolkit/models.py",\n'
                                                    '        "frozen_schema": "schemas/report.schema.json",\n'
                                                    '        "plan": "PHASE_4_PLAN.md",\n'
                                                    '        "cli": '
                                                    '"src/recursive_integrity_toolkit/cli.py",\n'
                                                    '        "html": '
                                                    '"src/recursive_integrity_toolkit/reports/html_report.py",\n'
                                                    '        "assembly": '
                                                    '"src/recursive_integrity_toolkit/reports/assembly.py",\n'
                                                    '        "result": '
                                                    '"src/recursive_integrity_toolkit/result.py",\n'
                                                    '        "config": '
                                                    '"src/recursive_integrity_toolkit/config.py",\n'
                                                    '        "hashing": '
                                                    '"src/recursive_integrity_toolkit/utils/hashing.py",\n'
                                                    '        "logging": '
                                                    '"src/recursive_integrity_toolkit/utils/logging.py",\n'
                                                    '        "output_paths": '
                                                    '"src/recursive_integrity_toolkit/utils/paths.py",\n'
                                                    '    }\n'
                                                    '    added = {\n'
                                                    '        "unknown_runtime": '
                                                    '"src/recursive_integrity_toolkit/reports/unauthorized.py",\n'
                                                    '        "premature_completion": '
                                                    '"PHASE_4_COMPLETION.md", "premature_report": '
                                                    '"report.json",\n'
                                                    '    }\n'
                                                    '    if mutation in replacements:\n'
                                                    '        relative, original, replacement = '
                                                    'replacements[mutation]\n'
                                                    '        path = tmp_path / relative\n'
                                                    '        source = path.read_bytes()\n'
                                                    '        assert source.count(original) == 1\n'
                                                    '        path.write_bytes(source.replace(original, '
                                                    'replacement, 1))\n'
                                                    '    elif mutation in appended:\n'
                                                    '        path = tmp_path / appended[mutation]\n'
                                                    '        path.write_bytes(path.read_bytes() + '
                                                    'b"\\nUnauthorized Step 5 mutation\\n")\n'
                                                    '    elif mutation in added:\n'
                                                    '        path = tmp_path / added[mutation]\n'
                                                    '        assert not path.exists()\n'
                                                    '        path.write_text("Unauthorized later-stage '
                                                    'file\\n", encoding="utf-8")\n'
                                                    '    elif mutation == "missing_runtime":\n'
                                                    '        (tmp_path / '
                                                    '"src/recursive_integrity_toolkit/metrics/bounds.py").unlink()\n'
                                                    '    elif mutation.startswith("control_"):\n'
                                                    '        path = tmp_path / "PHASE_4_BASELINE.json"\n'
                                                    '        control = '
                                                    'json.loads(path.read_text(encoding="utf-8"))\n'
                                                    '        if mutation == "control_step":\n'
                                                    '            control["active_step"] = 6\n'
                                                    '        elif mutation == "control_scope":\n'
                                                    '            '
                                                    'control["runtime_paths_authorized"].append("src/recursive_integrity_toolkit/reports/assembly.py")\n'
                                                    '        else:\n'
                                                    '            control["schema_changes_authorized"] = '
                                                    'True\n'
                                                    '            '
                                                    'control["schema_paths_authorized"].append("schemas/report.schema.json")\n'
                                                    '        path.write_text(json.dumps(control), '
                                                    'encoding="utf-8")\n'
                                                    '    else:\n'
                                                    '        raise AssertionError(f"Unknown active mutation '
                                                    'case: {mutation}")\n'
                                                    '    with pytest.raises(ValueError):\n'
                                                    '        verify(tmp_path)',
                                             'node': 'test_phase4_step5_current_snapshot_checks_valid_tree_before_mutations',
                                             'old': 'def '
                                                    'test_phase4_step5_current_snapshot_checks_valid_tree_before_mutations(repo_root, '
                                                    'tmp_path, phase4_gate_tools, mutation):\n'
                                                    '    import json\n'
                                                    '\n'
                                                    '    tracked = subprocess.check_output(["git", "-C", '
                                                    'str(repo_root), "ls-files", "-z"])\n'
                                                    '    paths = set(tracked.decode().split("\\0")) - {""}\n'
                                                    '    assert len(paths) == 227\n'
                                                    '    for relative in sorted(paths):\n'
                                                    '        destination = tmp_path / relative\n'
                                                    '        destination.parent.mkdir(parents=True, '
                                                    'exist_ok=True)\n'
                                                    '        shutil.copyfile(repo_root / relative, '
                                                    'destination)\n'
                                                    '    verify = '
                                                    'phase4_gate_tools["verify_phase4_step5_snapshot"]\n'
                                                    '    baseline = verify(tmp_path)\n'
                                                    '    assert baseline["package_modules"] == 40\n'
                                                    '    assert baseline["frozen_runtime_modules"] == 38\n'
                                                    '    assert baseline["frozen_schemas"] == 5\n'
                                                    '    assert baseline["result_contracts_enabled"] is '
                                                    'True\n'
                                                    '    assert baseline["adapters_enabled"] is True\n'
                                                    '    assert baseline["privacy_views_enabled"] is True\n'
                                                    '    assert baseline["renderers_enabled"] is True\n'
                                                    '    assert baseline["cli_analysis_enabled"] is False\n'
                                                    '    assert baseline["phase_complete"] is False\n'
                                                    '    if mutation == "unchanged":\n'
                                                    '        return\n'
                                                    '    replacements = {\n'
                                                    '        "formula": '
                                                    '("src/recursive_integrity_toolkit/metrics/diversity.py",\n'
                                                    '                    b"diversity = 1.0 - concentration", '
                                                    'b"diversity = 0.5 - concentration"),\n'
                                                    '        "math_oracle": '
                                                    '("tests/golden/phase3_math_cases.json", '
                                                    'b\'"v2_support":5\', b\'"v2_support":3\'),\n'
                                                    '        "hero": ("examples/hero/records_v2.csv", '
                                                    'b"v2_08,v2,", b"v2_99,v2,"),\n'
                                                    '        "dependency": ("pyproject.toml", b"numpy>=2.0", '
                                                    'b"numpy>=3.0"),\n'
                                                    '        "historical_assertion": '
                                                    '("tests/unit/test_phase4_contracts.py",\n'
                                                    "                                 b'    assert "
                                                    'control["active_phase"] == 4 and control["active_step"] '
                                                    "== 4\\n',\n"
                                                    '                                 b"    assert '
                                                    'True\\n"),\n'
                                                    '        "historical_tooling": '
                                                    '("scripts/release_check.py",\n'
                                                    '                               b"def '
                                                    'verify_phase4_step4_control(control: dict, step: int = '
                                                    '4) -> None:",\n'
                                                    '                               b"def '
                                                    'verify_phase4_step4_control(control: dict, step: int = '
                                                    '4) -> None:\\n    return"),\n'
                                                    '        "historical_binding": '
                                                    '("tests/integration/test_phase4_gates.py",\n'
                                                    '                               b"def '
                                                    'test_phase4_step4_current_workflows_preserve_matrix_and_use_active_dispatch(repo_root, '
                                                    'phase4_step4_snapshot):\\n    repo_root = '
                                                    'phase4_step4_snapshot\\n",\n'
                                                    '                               b"def '
                                                    'test_phase4_step4_current_workflows_preserve_matrix_and_use_active_dispatch(repo_root, '
                                                    'phase4_step4_snapshot):\\n"),\n'
                                                    '        "historical_document": '
                                                    '("docs/report_schema.md", b"# Report Schema\\n",\n'
                                                    '                                b"# Unauthorized '
                                                    'historical document\\n"),\n'
                                                    '        "input_hash_helper": '
                                                    '("src/recursive_integrity_toolkit/utils/hashing.py",\n'
                                                    '                              b"return '
                                                    'hashlib.sha256(data).hexdigest()", b"return '
                                                    'hashlib.sha256(b\'changed\').hexdigest()"),\n'
                                                    '        "config_resolver_helper": '
                                                    '("src/recursive_integrity_toolkit/config.py",\n'
                                                    '                                   b"def '
                                                    'resolve_config(", b"def resolve_config_disabled("),\n'
                                                    '    }\n'
                                                    '    appended = {\n'
                                                    '        "frozen_model": '
                                                    '"src/recursive_integrity_toolkit/models.py",\n'
                                                    '        "frozen_schema": "schemas/report.schema.json",\n'
                                                    '        "plan": "PHASE_4_PLAN.md",\n'
                                                    '        "cli": '
                                                    '"src/recursive_integrity_toolkit/cli.py",\n'
                                                    '        "html": '
                                                    '"src/recursive_integrity_toolkit/reports/html_report.py",\n'
                                                    '        "assembly": '
                                                    '"src/recursive_integrity_toolkit/reports/assembly.py",\n'
                                                    '        "result": '
                                                    '"src/recursive_integrity_toolkit/result.py",\n'
                                                    '        "config": '
                                                    '"src/recursive_integrity_toolkit/config.py",\n'
                                                    '        "hashing": '
                                                    '"src/recursive_integrity_toolkit/utils/hashing.py",\n'
                                                    '        "logging": '
                                                    '"src/recursive_integrity_toolkit/utils/logging.py",\n'
                                                    '        "output_paths": '
                                                    '"src/recursive_integrity_toolkit/utils/paths.py",\n'
                                                    '    }\n'
                                                    '    added = {\n'
                                                    '        "unknown_runtime": '
                                                    '"src/recursive_integrity_toolkit/reports/unauthorized.py",\n'
                                                    '        "premature_completion": '
                                                    '"PHASE_4_COMPLETION.md", "premature_report": '
                                                    '"report.json",\n'
                                                    '    }\n'
                                                    '    if mutation in replacements:\n'
                                                    '        relative, original, replacement = '
                                                    'replacements[mutation]\n'
                                                    '        path = tmp_path / relative\n'
                                                    '        source = path.read_bytes()\n'
                                                    '        assert source.count(original) == 1\n'
                                                    '        path.write_bytes(source.replace(original, '
                                                    'replacement, 1))\n'
                                                    '    elif mutation in appended:\n'
                                                    '        path = tmp_path / appended[mutation]\n'
                                                    '        path.write_bytes(path.read_bytes() + '
                                                    'b"\\nUnauthorized Step 5 mutation\\n")\n'
                                                    '    elif mutation in added:\n'
                                                    '        path = tmp_path / added[mutation]\n'
                                                    '        assert not path.exists()\n'
                                                    '        path.write_text("Unauthorized later-stage '
                                                    'file\\n", encoding="utf-8")\n'
                                                    '    elif mutation == "missing_runtime":\n'
                                                    '        (tmp_path / '
                                                    '"src/recursive_integrity_toolkit/metrics/bounds.py").unlink()\n'
                                                    '    elif mutation.startswith("control_"):\n'
                                                    '        path = tmp_path / "PHASE_4_BASELINE.json"\n'
                                                    '        control = '
                                                    'json.loads(path.read_text(encoding="utf-8"))\n'
                                                    '        if mutation == "control_step":\n'
                                                    '            control["active_step"] = 6\n'
                                                    '        elif mutation == "control_scope":\n'
                                                    '            '
                                                    'control["runtime_paths_authorized"].append("src/recursive_integrity_toolkit/reports/assembly.py")\n'
                                                    '        else:\n'
                                                    '            control["schema_changes_authorized"] = '
                                                    'True\n'
                                                    '            '
                                                    'control["schema_paths_authorized"].append("schemas/report.schema.json")\n'
                                                    '        path.write_text(json.dumps(control), '
                                                    'encoding="utf-8")\n'
                                                    '    else:\n'
                                                    '        raise AssertionError(f"Unknown active mutation '
                                                    'case: {mutation}")\n'
                                                    '    with pytest.raises(ValueError):\n'
                                                    '        verify(tmp_path)'},
                                            {'new': 'def phase4_mutation_tree(repo_root, tmp_path_factory, '
                                                    'phase4_gate_tools, phase4_step1_snapshot):\n'
                                                    '    """One source copy; each individual mutation is '
                                                    'restored in a finally block."""\n'
                                                    '    root = '
                                                    'tmp_path_factory.mktemp("phase4-active-mutations")\n'
                                                    '    paths = '
                                                    '{path.relative_to(phase4_step1_snapshot).as_posix()\n'
                                                    '             for path in '
                                                    'phase4_step1_snapshot.rglob("*") if path.is_file()}\n'
                                                    '    '
                                                    'paths.update(phase4_gate_tools["PHASE4_STEP1_NEW"])\n'
                                                    '    for relative in sorted(paths):\n'
                                                    '        destination = root / relative\n'
                                                    '        destination.parent.mkdir(parents=True, '
                                                    'exist_ok=True)\n'
                                                    '        shutil.copyfile(phase4_step1_snapshot / '
                                                    'relative, destination)\n'
                                                    '    return root',
                                             'node': 'phase4_mutation_tree',
                                             'old': 'def phase4_mutation_tree(repo_root, tmp_path_factory, '
                                                    'phase4_gate_tools, phase4_step1_snapshot):\n'
                                                    '    """One source copy; each individual mutation is '
                                                    'restored in a finally block."""\n'
                                                    '    root = '
                                                    'tmp_path_factory.mktemp("phase4-active-mutations")\n'
                                                    '    tracked = subprocess.check_output(["git", "-C", '
                                                    'str(repo_root), "ls-files", "-z"])\n'
                                                    '    paths = set(tracked.decode().split("\\0")) - {""}\n'
                                                    '    '
                                                    'paths.update(phase4_gate_tools["PHASE4_STEP1_NEW"])\n'
                                                    '    for relative in sorted(paths):\n'
                                                    '        destination = root / relative\n'
                                                    '        destination.parent.mkdir(parents=True, '
                                                    'exist_ok=True)\n'
                                                    '        shutil.copyfile(phase4_step1_snapshot / '
                                                    'relative, destination)\n'
                                                    '    return root'},
                                            {'new': 'def '
                                                    'test_phase4_step2_current_snapshot_checks_valid_tree_before_mutations(repo_root, '
                                                    'tmp_path, phase4_gate_tools, mutation, '
                                                    'phase4_step2_snapshot):\n'
                                                    '    import json\n'
                                                    '\n'
                                                    '    paths = '
                                                    '{path.relative_to(phase4_step2_snapshot).as_posix()\n'
                                                    '             for path in '
                                                    'phase4_step2_snapshot.rglob("*") if path.is_file()}\n'
                                                    '    assert len(paths) == 227\n'
                                                    '    for relative in sorted(paths):\n'
                                                    '        destination = tmp_path / relative\n'
                                                    '        destination.parent.mkdir(parents=True, '
                                                    'exist_ok=True)\n'
                                                    '        shutil.copyfile(phase4_step2_snapshot / '
                                                    'relative, destination)\n'
                                                    '    verify = '
                                                    'phase4_gate_tools["verify_phase4_step2_snapshot"]\n'
                                                    '    baseline = verify(tmp_path)\n'
                                                    '    assert baseline["frozen_runtime_modules"] == 39\n'
                                                    '    assert baseline["frozen_schemas"] == 4\n'
                                                    '    assert baseline["result_contracts_enabled"] is '
                                                    'True\n'
                                                    '    assert baseline["adapters_enabled"] is False\n'
                                                    '    assert baseline["cli_analysis_enabled"] is False\n'
                                                    '    assert baseline["phase_complete"] is False\n'
                                                    '    if mutation == "unchanged":\n'
                                                    '        return\n'
                                                    '    replacements = {\n'
                                                    '        "formula": '
                                                    '("src/recursive_integrity_toolkit/metrics/diversity.py",\n'
                                                    '                    b"diversity = 1.0 - concentration", '
                                                    'b"diversity = 0.5 - concentration"),\n'
                                                    '        "math_oracle": '
                                                    '("tests/golden/phase3_math_cases.json", '
                                                    'b\'"v2_support":5\', b\'"v2_support":3\'),\n'
                                                    '        "hero": ("examples/hero/records_v2.csv", '
                                                    'b"v2_08,v2,", b"v2_99,v2,"),\n'
                                                    '        "dependency": ("pyproject.toml", b"numpy>=2.0", '
                                                    'b"numpy>=3.0"),\n'
                                                    '        "historical_assertion": '
                                                    '("tests/unit/test_phase4_contracts.py",\n'
                                                    "                                 b'    assert "
                                                    'phase4_control["active_step"] == 1\\n\', b"    assert '
                                                    'True\\n"),\n'
                                                    '        "historical_tooling": '
                                                    '("scripts/release_check.py",\n'
                                                    '                               b"def '
                                                    'verify_phase4_control(control: dict, step: int = 1) -> '
                                                    'None:",\n'
                                                    '                               b"def '
                                                    'verify_phase4_control(control: dict, step: int = 1) -> '
                                                    'None:\\n    return"),\n'
                                                    '    }\n'
                                                    '    appended = {\n'
                                                    '        "frozen_model": '
                                                    '"src/recursive_integrity_toolkit/models.py",\n'
                                                    '        "frozen_schema": "schemas/config.schema.json",\n'
                                                    '        "plan": "PHASE_4_PLAN.md",\n'
                                                    '        "assembly": '
                                                    '"src/recursive_integrity_toolkit/reports/assembly.py",\n'
                                                    '        "cli": '
                                                    '"src/recursive_integrity_toolkit/cli.py",\n'
                                                    '    }\n'
                                                    '    added = {\n'
                                                    '        "unknown_runtime": '
                                                    '"src/recursive_integrity_toolkit/reports/unauthorized.py",\n'
                                                    '        "premature_completion": '
                                                    '"PHASE_4_COMPLETION.md",\n'
                                                    '        "premature_report": "report.json",\n'
                                                    '    }\n'
                                                    '    if mutation in replacements:\n'
                                                    '        relative, original, replacement = '
                                                    'replacements[mutation]\n'
                                                    '        path = tmp_path / relative\n'
                                                    '        source = path.read_bytes()\n'
                                                    '        assert source.count(original) == 1\n'
                                                    '        path.write_bytes(source.replace(original, '
                                                    'replacement, 1))\n'
                                                    '    elif mutation in appended:\n'
                                                    '        path = tmp_path / appended[mutation]\n'
                                                    '        path.write_bytes(path.read_bytes() + '
                                                    'b"\\nUnauthorized Step 2 mutation\\n")\n'
                                                    '    elif mutation in added:\n'
                                                    '        path = tmp_path / added[mutation]\n'
                                                    '        assert not path.exists()\n'
                                                    '        path.write_text("Unauthorized later-stage '
                                                    'file\\n", encoding="utf-8")\n'
                                                    '    elif mutation == "missing_runtime":\n'
                                                    '        (tmp_path / '
                                                    '"src/recursive_integrity_toolkit/metrics/bounds.py").unlink()\n'
                                                    '    elif mutation.startswith("control_"):\n'
                                                    '        path = tmp_path / "PHASE_4_BASELINE.json"\n'
                                                    '        control = '
                                                    'json.loads(path.read_text(encoding="utf-8"))\n'
                                                    '        if mutation == "control_step":\n'
                                                    '            control["active_step"] = 3\n'
                                                    '        elif mutation == "control_scope":\n'
                                                    '            '
                                                    'control["runtime_paths_authorized"].append("src/recursive_integrity_toolkit/cli.py")\n'
                                                    '        else:\n'
                                                    '            '
                                                    'control["schema_paths_authorized"].append("schemas/config.schema.json")\n'
                                                    '        path.write_text(json.dumps(control), '
                                                    'encoding="utf-8")\n'
                                                    '    elif mutation.startswith("schema_"):\n'
                                                    '        path = tmp_path / "schemas/report.schema.json"\n'
                                                    '        schema = '
                                                    'json.loads(path.read_text(encoding="utf-8"))\n'
                                                    '        if mutation == "schema_open_root":\n'
                                                    '            schema["additionalProperties"] = True\n'
                                                    '        else:\n'
                                                    '            schema["$schema"] = '
                                                    '"http://json-schema.org/draft-07/schema#"\n'
                                                    '        path.write_text(json.dumps(schema), '
                                                    'encoding="utf-8")\n'
                                                    '    elif mutation == "model_computation_import":\n'
                                                    '        path = tmp_path / '
                                                    '"src/recursive_integrity_toolkit/result.py"\n'
                                                    '        path.write_bytes(path.read_bytes() + b"\\nfrom '
                                                    '.metrics.diversity import '
                                                    'effective_state_diversity\\n")\n'
                                                    '    else:\n'
                                                    '        raise AssertionError(f"Unknown active mutation '
                                                    'case: {mutation}")\n'
                                                    '    with pytest.raises(ValueError):\n'
                                                    '        verify(tmp_path)',
                                             'node': 'test_phase4_step2_current_snapshot_checks_valid_tree_before_mutations',
                                             'old': 'def '
                                                    'test_phase4_step2_current_snapshot_checks_valid_tree_before_mutations(repo_root, '
                                                    'tmp_path, phase4_gate_tools, mutation, '
                                                    'phase4_step2_snapshot):\n'
                                                    '    import json\n'
                                                    '\n'
                                                    '    tracked = subprocess.check_output(["git", "-C", '
                                                    'str(repo_root), "ls-files", "-z"])\n'
                                                    '    paths = set(tracked.decode().split("\\0")) - {""}\n'
                                                    '    assert len(paths) == 227\n'
                                                    '    for relative in sorted(paths):\n'
                                                    '        destination = tmp_path / relative\n'
                                                    '        destination.parent.mkdir(parents=True, '
                                                    'exist_ok=True)\n'
                                                    '        shutil.copyfile(phase4_step2_snapshot / '
                                                    'relative, destination)\n'
                                                    '    verify = '
                                                    'phase4_gate_tools["verify_phase4_step2_snapshot"]\n'
                                                    '    baseline = verify(tmp_path)\n'
                                                    '    assert baseline["frozen_runtime_modules"] == 39\n'
                                                    '    assert baseline["frozen_schemas"] == 4\n'
                                                    '    assert baseline["result_contracts_enabled"] is '
                                                    'True\n'
                                                    '    assert baseline["adapters_enabled"] is False\n'
                                                    '    assert baseline["cli_analysis_enabled"] is False\n'
                                                    '    assert baseline["phase_complete"] is False\n'
                                                    '    if mutation == "unchanged":\n'
                                                    '        return\n'
                                                    '    replacements = {\n'
                                                    '        "formula": '
                                                    '("src/recursive_integrity_toolkit/metrics/diversity.py",\n'
                                                    '                    b"diversity = 1.0 - concentration", '
                                                    'b"diversity = 0.5 - concentration"),\n'
                                                    '        "math_oracle": '
                                                    '("tests/golden/phase3_math_cases.json", '
                                                    'b\'"v2_support":5\', b\'"v2_support":3\'),\n'
                                                    '        "hero": ("examples/hero/records_v2.csv", '
                                                    'b"v2_08,v2,", b"v2_99,v2,"),\n'
                                                    '        "dependency": ("pyproject.toml", b"numpy>=2.0", '
                                                    'b"numpy>=3.0"),\n'
                                                    '        "historical_assertion": '
                                                    '("tests/unit/test_phase4_contracts.py",\n'
                                                    "                                 b'    assert "
                                                    'phase4_control["active_step"] == 1\\n\', b"    assert '
                                                    'True\\n"),\n'
                                                    '        "historical_tooling": '
                                                    '("scripts/release_check.py",\n'
                                                    '                               b"def '
                                                    'verify_phase4_control(control: dict, step: int = 1) -> '
                                                    'None:",\n'
                                                    '                               b"def '
                                                    'verify_phase4_control(control: dict, step: int = 1) -> '
                                                    'None:\\n    return"),\n'
                                                    '    }\n'
                                                    '    appended = {\n'
                                                    '        "frozen_model": '
                                                    '"src/recursive_integrity_toolkit/models.py",\n'
                                                    '        "frozen_schema": "schemas/config.schema.json",\n'
                                                    '        "plan": "PHASE_4_PLAN.md",\n'
                                                    '        "assembly": '
                                                    '"src/recursive_integrity_toolkit/reports/assembly.py",\n'
                                                    '        "cli": '
                                                    '"src/recursive_integrity_toolkit/cli.py",\n'
                                                    '    }\n'
                                                    '    added = {\n'
                                                    '        "unknown_runtime": '
                                                    '"src/recursive_integrity_toolkit/reports/unauthorized.py",\n'
                                                    '        "premature_completion": '
                                                    '"PHASE_4_COMPLETION.md",\n'
                                                    '        "premature_report": "report.json",\n'
                                                    '    }\n'
                                                    '    if mutation in replacements:\n'
                                                    '        relative, original, replacement = '
                                                    'replacements[mutation]\n'
                                                    '        path = tmp_path / relative\n'
                                                    '        source = path.read_bytes()\n'
                                                    '        assert source.count(original) == 1\n'
                                                    '        path.write_bytes(source.replace(original, '
                                                    'replacement, 1))\n'
                                                    '    elif mutation in appended:\n'
                                                    '        path = tmp_path / appended[mutation]\n'
                                                    '        path.write_bytes(path.read_bytes() + '
                                                    'b"\\nUnauthorized Step 2 mutation\\n")\n'
                                                    '    elif mutation in added:\n'
                                                    '        path = tmp_path / added[mutation]\n'
                                                    '        assert not path.exists()\n'
                                                    '        path.write_text("Unauthorized later-stage '
                                                    'file\\n", encoding="utf-8")\n'
                                                    '    elif mutation == "missing_runtime":\n'
                                                    '        (tmp_path / '
                                                    '"src/recursive_integrity_toolkit/metrics/bounds.py").unlink()\n'
                                                    '    elif mutation.startswith("control_"):\n'
                                                    '        path = tmp_path / "PHASE_4_BASELINE.json"\n'
                                                    '        control = '
                                                    'json.loads(path.read_text(encoding="utf-8"))\n'
                                                    '        if mutation == "control_step":\n'
                                                    '            control["active_step"] = 3\n'
                                                    '        elif mutation == "control_scope":\n'
                                                    '            '
                                                    'control["runtime_paths_authorized"].append("src/recursive_integrity_toolkit/cli.py")\n'
                                                    '        else:\n'
                                                    '            '
                                                    'control["schema_paths_authorized"].append("schemas/config.schema.json")\n'
                                                    '        path.write_text(json.dumps(control), '
                                                    'encoding="utf-8")\n'
                                                    '    elif mutation.startswith("schema_"):\n'
                                                    '        path = tmp_path / "schemas/report.schema.json"\n'
                                                    '        schema = '
                                                    'json.loads(path.read_text(encoding="utf-8"))\n'
                                                    '        if mutation == "schema_open_root":\n'
                                                    '            schema["additionalProperties"] = True\n'
                                                    '        else:\n'
                                                    '            schema["$schema"] = '
                                                    '"http://json-schema.org/draft-07/schema#"\n'
                                                    '        path.write_text(json.dumps(schema), '
                                                    'encoding="utf-8")\n'
                                                    '    elif mutation == "model_computation_import":\n'
                                                    '        path = tmp_path / '
                                                    '"src/recursive_integrity_toolkit/result.py"\n'
                                                    '        path.write_bytes(path.read_bytes() + b"\\nfrom '
                                                    '.metrics.diversity import '
                                                    'effective_state_diversity\\n")\n'
                                                    '    else:\n'
                                                    '        raise AssertionError(f"Unknown active mutation '
                                                    'case: {mutation}")\n'
                                                    '    with pytest.raises(ValueError):\n'
                                                    '        verify(tmp_path)'},
                                            {'new': 'def '
                                                    'test_phase4_step3_current_snapshot_checks_valid_tree_before_mutations(repo_root, '
                                                    'tmp_path, phase4_gate_tools, mutation, '
                                                    'phase4_step3_snapshot):\n'
                                                    '    import json\n'
                                                    '\n'
                                                    '    paths = '
                                                    '{path.relative_to(phase4_step3_snapshot).as_posix()\n'
                                                    '             for path in '
                                                    'phase4_step3_snapshot.rglob("*") if path.is_file()}\n'
                                                    '    assert len(paths) == 227\n'
                                                    '    for relative in sorted(paths):\n'
                                                    '        destination = tmp_path / relative\n'
                                                    '        destination.parent.mkdir(parents=True, '
                                                    'exist_ok=True)\n'
                                                    '        shutil.copyfile(phase4_step3_snapshot / '
                                                    'relative, destination)\n'
                                                    '    verify = '
                                                    'phase4_gate_tools["verify_phase4_step3_snapshot"]\n'
                                                    '    baseline = verify(tmp_path)\n'
                                                    '    assert baseline["package_modules"] == 40\n'
                                                    '    assert baseline["frozen_runtime_modules"] == 39\n'
                                                    '    assert baseline["frozen_schemas"] == 5\n'
                                                    '    assert baseline["result_contracts_enabled"] is '
                                                    'True\n'
                                                    '    assert baseline["adapters_enabled"] is True\n'
                                                    '    assert baseline["cli_analysis_enabled"] is False\n'
                                                    '    assert baseline["phase_complete"] is False\n'
                                                    '    if mutation == "unchanged":\n'
                                                    '        return\n'
                                                    '    replacements = {\n'
                                                    '        "formula": '
                                                    '("src/recursive_integrity_toolkit/metrics/diversity.py",\n'
                                                    '                    b"diversity = 1.0 - concentration", '
                                                    'b"diversity = 0.5 - concentration"),\n'
                                                    '        "math_oracle": '
                                                    '("tests/golden/phase3_math_cases.json", '
                                                    'b\'"v2_support":5\', b\'"v2_support":3\'),\n'
                                                    '        "hero": ("examples/hero/records_v2.csv", '
                                                    'b"v2_08,v2,", b"v2_99,v2,"),\n'
                                                    '        "dependency": ("pyproject.toml", b"numpy>=2.0", '
                                                    'b"numpy>=3.0"),\n'
                                                    '        "historical_assertion": '
                                                    '("tests/unit/test_phase4_contracts.py",\n'
                                                    "                                 b'    assert "
                                                    'control["active_phase"] == 4 and control["active_step"] '
                                                    "== 2\\n',\n"
                                                    '                                 b"    assert '
                                                    'True\\n"),\n'
                                                    '        "historical_tooling": '
                                                    '("scripts/release_check.py",\n'
                                                    '                               b"def '
                                                    'verify_phase4_step2_control(control: dict, step: int = '
                                                    '2) -> None:",\n'
                                                    '                               b"def '
                                                    'verify_phase4_step2_control(control: dict, step: int = '
                                                    '2) -> None:\\n    return"),\n'
                                                    '        "historical_binding": '
                                                    '("tests/integration/test_phase4_gates.py",\n'
                                                    '                               b"def '
                                                    'test_phase4_step2_current_workflows_preserve_matrix_and_use_active_dispatch(repo_root, '
                                                    'phase4_step2_snapshot):\\n    repo_root = '
                                                    'phase4_step2_snapshot\\n",\n'
                                                    '                               b"def '
                                                    'test_phase4_step2_current_workflows_preserve_matrix_and_use_active_dispatch(repo_root, '
                                                    'phase4_step2_snapshot):\\n"),\n'
                                                    '        "historical_document": '
                                                    '("docs/report_schema.md", b"# Report Schema\\n", b"# '
                                                    'Modified Report Schema\\n"),\n'
                                                    '    }\n'
                                                    '    appended = {\n'
                                                    '        "frozen_model": '
                                                    '"src/recursive_integrity_toolkit/models.py",\n'
                                                    '        "frozen_result": '
                                                    '"src/recursive_integrity_toolkit/result.py",\n'
                                                    '        "frozen_schema": "schemas/config.schema.json",\n'
                                                    '        "plan": "PHASE_4_PLAN.md",\n'
                                                    '        "cli": '
                                                    '"src/recursive_integrity_toolkit/cli.py",\n'
                                                    '        "renderer": '
                                                    '"src/recursive_integrity_toolkit/reports/json_report.py",\n'
                                                    '    }\n'
                                                    '    added = {\n'
                                                    '        "unknown_runtime": '
                                                    '"src/recursive_integrity_toolkit/reports/unauthorized.py",\n'
                                                    '        "premature_completion": '
                                                    '"PHASE_4_COMPLETION.md",\n'
                                                    '        "premature_report": "report.json",\n'
                                                    '    }\n'
                                                    '    assembly_injections = {\n'
                                                    '        "assembly_metric_import": b"\\nfrom '
                                                    '..metrics.diversity import '
                                                    'effective_state_diversity\\n",\n'
                                                    '        "assembly_calculation_import": b"\\nfrom '
                                                    '..metrics import coverage\\n",\n'
                                                    '        "assembly_numeric_import": b"\\nimport '
                                                    'numpy\\n",\n'
                                                    '        "assembly_network_import": b"\\nimport '
                                                    'socket\\n",\n'
                                                    '        "assembly_file_io": '
                                                    'b"\\nopen(\'unapproved.txt\', '
                                                    '\'w\').write(\'data\')\\n",\n'
                                                    '        "assembly_dynamic_execution": '
                                                    'b"\\nexec(\'forged = True\')\\n",\n'
                                                    '        "assembly_new_formula": b"\\ndef '
                                                    'invented_metric(values):\\n    return sum(value * value '
                                                    'for value in values)\\n",\n'
                                                    '    }\n'
                                                    '    if mutation in replacements:\n'
                                                    '        relative, original, replacement = '
                                                    'replacements[mutation]\n'
                                                    '        path = tmp_path / relative\n'
                                                    '        source = path.read_bytes()\n'
                                                    '        assert source.count(original) == 1\n'
                                                    '        path.write_bytes(source.replace(original, '
                                                    'replacement, 1))\n'
                                                    '    elif mutation in appended:\n'
                                                    '        path = tmp_path / appended[mutation]\n'
                                                    '        path.write_bytes(path.read_bytes() + '
                                                    'b"\\nUnauthorized Step 3 mutation\\n")\n'
                                                    '    elif mutation in added:\n'
                                                    '        path = tmp_path / added[mutation]\n'
                                                    '        assert not path.exists()\n'
                                                    '        path.write_text("Unauthorized later-stage '
                                                    'file\\n", encoding="utf-8")\n'
                                                    '    elif mutation == "missing_runtime":\n'
                                                    '        (tmp_path / '
                                                    '"src/recursive_integrity_toolkit/metrics/bounds.py").unlink()\n'
                                                    '    elif mutation.startswith("control_"):\n'
                                                    '        path = tmp_path / "PHASE_4_BASELINE.json"\n'
                                                    '        control = '
                                                    'json.loads(path.read_text(encoding="utf-8"))\n'
                                                    '        if mutation == "control_step":\n'
                                                    '            control["active_step"] = 4\n'
                                                    '        elif mutation == "control_scope":\n'
                                                    '            '
                                                    'control["runtime_paths_authorized"].append("src/recursive_integrity_toolkit/result.py")\n'
                                                    '        else:\n'
                                                    '            control["schema_changes_authorized"] = '
                                                    'True\n'
                                                    '            '
                                                    'control["schema_paths_authorized"].append("schemas/report.schema.json")\n'
                                                    '        path.write_text(json.dumps(control), '
                                                    'encoding="utf-8")\n'
                                                    '    elif mutation == "schema_open_root":\n'
                                                    '        path = tmp_path / "schemas/report.schema.json"\n'
                                                    '        schema = '
                                                    'json.loads(path.read_text(encoding="utf-8"))\n'
                                                    '        schema["additionalProperties"] = True\n'
                                                    '        path.write_text(json.dumps(schema), '
                                                    'encoding="utf-8")\n'
                                                    '    elif mutation in assembly_injections:\n'
                                                    '        path = tmp_path / '
                                                    '"src/recursive_integrity_toolkit/reports/assembly.py"\n'
                                                    '        path.write_bytes(path.read_bytes() + '
                                                    'assembly_injections[mutation])\n'
                                                    '    else:\n'
                                                    '        raise AssertionError(f"Unknown active mutation '
                                                    'case: {mutation}")\n'
                                                    '    with pytest.raises(ValueError):\n'
                                                    '        verify(tmp_path)',
                                             'node': 'test_phase4_step3_current_snapshot_checks_valid_tree_before_mutations',
                                             'old': 'def '
                                                    'test_phase4_step3_current_snapshot_checks_valid_tree_before_mutations(repo_root, '
                                                    'tmp_path, phase4_gate_tools, mutation, '
                                                    'phase4_step3_snapshot):\n'
                                                    '    import json\n'
                                                    '\n'
                                                    '    tracked = subprocess.check_output(["git", "-C", '
                                                    'str(repo_root), "ls-files", "-z"])\n'
                                                    '    paths = set(tracked.decode().split("\\0")) - {""}\n'
                                                    '    assert len(paths) == 227\n'
                                                    '    for relative in sorted(paths):\n'
                                                    '        destination = tmp_path / relative\n'
                                                    '        destination.parent.mkdir(parents=True, '
                                                    'exist_ok=True)\n'
                                                    '        shutil.copyfile(phase4_step3_snapshot / '
                                                    'relative, destination)\n'
                                                    '    verify = '
                                                    'phase4_gate_tools["verify_phase4_step3_snapshot"]\n'
                                                    '    baseline = verify(tmp_path)\n'
                                                    '    assert baseline["package_modules"] == 40\n'
                                                    '    assert baseline["frozen_runtime_modules"] == 39\n'
                                                    '    assert baseline["frozen_schemas"] == 5\n'
                                                    '    assert baseline["result_contracts_enabled"] is '
                                                    'True\n'
                                                    '    assert baseline["adapters_enabled"] is True\n'
                                                    '    assert baseline["cli_analysis_enabled"] is False\n'
                                                    '    assert baseline["phase_complete"] is False\n'
                                                    '    if mutation == "unchanged":\n'
                                                    '        return\n'
                                                    '    replacements = {\n'
                                                    '        "formula": '
                                                    '("src/recursive_integrity_toolkit/metrics/diversity.py",\n'
                                                    '                    b"diversity = 1.0 - concentration", '
                                                    'b"diversity = 0.5 - concentration"),\n'
                                                    '        "math_oracle": '
                                                    '("tests/golden/phase3_math_cases.json", '
                                                    'b\'"v2_support":5\', b\'"v2_support":3\'),\n'
                                                    '        "hero": ("examples/hero/records_v2.csv", '
                                                    'b"v2_08,v2,", b"v2_99,v2,"),\n'
                                                    '        "dependency": ("pyproject.toml", b"numpy>=2.0", '
                                                    'b"numpy>=3.0"),\n'
                                                    '        "historical_assertion": '
                                                    '("tests/unit/test_phase4_contracts.py",\n'
                                                    "                                 b'    assert "
                                                    'control["active_phase"] == 4 and control["active_step"] '
                                                    "== 2\\n',\n"
                                                    '                                 b"    assert '
                                                    'True\\n"),\n'
                                                    '        "historical_tooling": '
                                                    '("scripts/release_check.py",\n'
                                                    '                               b"def '
                                                    'verify_phase4_step2_control(control: dict, step: int = '
                                                    '2) -> None:",\n'
                                                    '                               b"def '
                                                    'verify_phase4_step2_control(control: dict, step: int = '
                                                    '2) -> None:\\n    return"),\n'
                                                    '        "historical_binding": '
                                                    '("tests/integration/test_phase4_gates.py",\n'
                                                    '                               b"def '
                                                    'test_phase4_step2_current_workflows_preserve_matrix_and_use_active_dispatch(repo_root, '
                                                    'phase4_step2_snapshot):\\n    repo_root = '
                                                    'phase4_step2_snapshot\\n",\n'
                                                    '                               b"def '
                                                    'test_phase4_step2_current_workflows_preserve_matrix_and_use_active_dispatch(repo_root, '
                                                    'phase4_step2_snapshot):\\n"),\n'
                                                    '        "historical_document": '
                                                    '("docs/report_schema.md", b"# Report Schema\\n", b"# '
                                                    'Modified Report Schema\\n"),\n'
                                                    '    }\n'
                                                    '    appended = {\n'
                                                    '        "frozen_model": '
                                                    '"src/recursive_integrity_toolkit/models.py",\n'
                                                    '        "frozen_result": '
                                                    '"src/recursive_integrity_toolkit/result.py",\n'
                                                    '        "frozen_schema": "schemas/config.schema.json",\n'
                                                    '        "plan": "PHASE_4_PLAN.md",\n'
                                                    '        "cli": '
                                                    '"src/recursive_integrity_toolkit/cli.py",\n'
                                                    '        "renderer": '
                                                    '"src/recursive_integrity_toolkit/reports/json_report.py",\n'
                                                    '    }\n'
                                                    '    added = {\n'
                                                    '        "unknown_runtime": '
                                                    '"src/recursive_integrity_toolkit/reports/unauthorized.py",\n'
                                                    '        "premature_completion": '
                                                    '"PHASE_4_COMPLETION.md",\n'
                                                    '        "premature_report": "report.json",\n'
                                                    '    }\n'
                                                    '    assembly_injections = {\n'
                                                    '        "assembly_metric_import": b"\\nfrom '
                                                    '..metrics.diversity import '
                                                    'effective_state_diversity\\n",\n'
                                                    '        "assembly_calculation_import": b"\\nfrom '
                                                    '..metrics import coverage\\n",\n'
                                                    '        "assembly_numeric_import": b"\\nimport '
                                                    'numpy\\n",\n'
                                                    '        "assembly_network_import": b"\\nimport '
                                                    'socket\\n",\n'
                                                    '        "assembly_file_io": '
                                                    'b"\\nopen(\'unapproved.txt\', '
                                                    '\'w\').write(\'data\')\\n",\n'
                                                    '        "assembly_dynamic_execution": '
                                                    'b"\\nexec(\'forged = True\')\\n",\n'
                                                    '        "assembly_new_formula": b"\\ndef '
                                                    'invented_metric(values):\\n    return sum(value * value '
                                                    'for value in values)\\n",\n'
                                                    '    }\n'
                                                    '    if mutation in replacements:\n'
                                                    '        relative, original, replacement = '
                                                    'replacements[mutation]\n'
                                                    '        path = tmp_path / relative\n'
                                                    '        source = path.read_bytes()\n'
                                                    '        assert source.count(original) == 1\n'
                                                    '        path.write_bytes(source.replace(original, '
                                                    'replacement, 1))\n'
                                                    '    elif mutation in appended:\n'
                                                    '        path = tmp_path / appended[mutation]\n'
                                                    '        path.write_bytes(path.read_bytes() + '
                                                    'b"\\nUnauthorized Step 3 mutation\\n")\n'
                                                    '    elif mutation in added:\n'
                                                    '        path = tmp_path / added[mutation]\n'
                                                    '        assert not path.exists()\n'
                                                    '        path.write_text("Unauthorized later-stage '
                                                    'file\\n", encoding="utf-8")\n'
                                                    '    elif mutation == "missing_runtime":\n'
                                                    '        (tmp_path / '
                                                    '"src/recursive_integrity_toolkit/metrics/bounds.py").unlink()\n'
                                                    '    elif mutation.startswith("control_"):\n'
                                                    '        path = tmp_path / "PHASE_4_BASELINE.json"\n'
                                                    '        control = '
                                                    'json.loads(path.read_text(encoding="utf-8"))\n'
                                                    '        if mutation == "control_step":\n'
                                                    '            control["active_step"] = 4\n'
                                                    '        elif mutation == "control_scope":\n'
                                                    '            '
                                                    'control["runtime_paths_authorized"].append("src/recursive_integrity_toolkit/result.py")\n'
                                                    '        else:\n'
                                                    '            control["schema_changes_authorized"] = '
                                                    'True\n'
                                                    '            '
                                                    'control["schema_paths_authorized"].append("schemas/report.schema.json")\n'
                                                    '        path.write_text(json.dumps(control), '
                                                    'encoding="utf-8")\n'
                                                    '    elif mutation == "schema_open_root":\n'
                                                    '        path = tmp_path / "schemas/report.schema.json"\n'
                                                    '        schema = '
                                                    'json.loads(path.read_text(encoding="utf-8"))\n'
                                                    '        schema["additionalProperties"] = True\n'
                                                    '        path.write_text(json.dumps(schema), '
                                                    'encoding="utf-8")\n'
                                                    '    elif mutation in assembly_injections:\n'
                                                    '        path = tmp_path / '
                                                    '"src/recursive_integrity_toolkit/reports/assembly.py"\n'
                                                    '        path.write_bytes(path.read_bytes() + '
                                                    'assembly_injections[mutation])\n'
                                                    '    else:\n'
                                                    '        raise AssertionError(f"Unknown active mutation '
                                                    'case: {mutation}")\n'
                                                    '    with pytest.raises(ValueError):\n'
                                                    '        verify(tmp_path)'},
                                            {'new': 'def '
                                                    'test_phase4_step4_current_snapshot_checks_valid_tree_before_mutations(repo_root, '
                                                    'tmp_path, phase4_gate_tools, mutation, '
                                                    'phase4_step4_snapshot):\n'
                                                    '    import json\n'
                                                    '\n'
                                                    '    paths = '
                                                    '{path.relative_to(phase4_step4_snapshot).as_posix()\n'
                                                    '             for path in '
                                                    'phase4_step4_snapshot.rglob("*") if path.is_file()}\n'
                                                    '    assert len(paths) == 227\n'
                                                    '    for relative in sorted(paths):\n'
                                                    '        destination = tmp_path / relative\n'
                                                    '        destination.parent.mkdir(parents=True, '
                                                    'exist_ok=True)\n'
                                                    '        shutil.copyfile(phase4_step4_snapshot / '
                                                    'relative, destination)\n'
                                                    '    verify = '
                                                    'phase4_gate_tools["verify_phase4_step4_snapshot"]\n'
                                                    '    baseline = verify(tmp_path)\n'
                                                    '    assert baseline["package_modules"] == 40\n'
                                                    '    assert baseline["frozen_runtime_modules"] == 35\n'
                                                    '    assert baseline["frozen_schemas"] == 5\n'
                                                    '    assert baseline["result_contracts_enabled"] is '
                                                    'True\n'
                                                    '    assert baseline["adapters_enabled"] is True\n'
                                                    '    assert baseline["privacy_views_enabled"] is True\n'
                                                    '    assert baseline["cli_analysis_enabled"] is False\n'
                                                    '    assert baseline["phase_complete"] is False\n'
                                                    '    if mutation == "unchanged":\n'
                                                    '        return\n'
                                                    '    replacements = {\n'
                                                    '        "formula": '
                                                    '("src/recursive_integrity_toolkit/metrics/diversity.py",\n'
                                                    '                    b"diversity = 1.0 - concentration", '
                                                    'b"diversity = 0.5 - concentration"),\n'
                                                    '        "math_oracle": '
                                                    '("tests/golden/phase3_math_cases.json", '
                                                    'b\'"v2_support":5\', b\'"v2_support":3\'),\n'
                                                    '        "hero": ("examples/hero/records_v2.csv", '
                                                    'b"v2_08,v2,", b"v2_99,v2,"),\n'
                                                    '        "dependency": ("pyproject.toml", b"numpy>=2.0", '
                                                    'b"numpy>=3.0"),\n'
                                                    '        "historical_assertion": '
                                                    '("tests/unit/test_phase4_contracts.py",\n'
                                                    "                                 b'    assert "
                                                    'control["active_phase"] == 4 and control["active_step"] '
                                                    "== 3\\n',\n"
                                                    '                                 b"    assert '
                                                    'True\\n"),\n'
                                                    '        "historical_tooling": '
                                                    '("scripts/release_check.py",\n'
                                                    '                               b"def '
                                                    'verify_phase4_step3_control(control: dict, step: int = '
                                                    '3) -> None:",\n'
                                                    '                               b"def '
                                                    'verify_phase4_step3_control(control: dict, step: int = '
                                                    '3) -> None:\\n    return"),\n'
                                                    '        "historical_binding": '
                                                    '("tests/integration/test_phase4_gates.py",\n'
                                                    '                               b"def '
                                                    'test_phase4_step3_current_workflows_preserve_matrix_and_use_active_dispatch(repo_root, '
                                                    'phase4_step3_snapshot):\\n    repo_root = '
                                                    'phase4_step3_snapshot\\n",\n'
                                                    '                               b"def '
                                                    'test_phase4_step3_current_workflows_preserve_matrix_and_use_active_dispatch(repo_root, '
                                                    'phase4_step3_snapshot):\\n"),\n'
                                                    '        "historical_document": ("docs/privacy.md", b"# '
                                                    'Privacy and Local Input Boundaries\\n",\n'
                                                    '                                b"# Unauthorized '
                                                    'Privacy and Local Input Boundaries\\n"),\n'
                                                    '        "input_hash_helper": '
                                                    '("src/recursive_integrity_toolkit/utils/hashing.py",\n'
                                                    '                              b"return '
                                                    'hashlib.sha256(data).hexdigest()", b"return '
                                                    'hashlib.sha256(b\'changed\').hexdigest()"),\n'
                                                    '        "config_resolver_helper": '
                                                    '("src/recursive_integrity_toolkit/config.py",\n'
                                                    '                                   b"def '
                                                    'resolve_config(", b"def resolve_config_disabled("),\n'
                                                    '    }\n'
                                                    '    appended = {\n'
                                                    '        "frozen_model": '
                                                    '"src/recursive_integrity_toolkit/models.py",\n'
                                                    '        "frozen_schema": "schemas/report.schema.json",\n'
                                                    '        "plan": "PHASE_4_PLAN.md",\n'
                                                    '        "cli": '
                                                    '"src/recursive_integrity_toolkit/cli.py",\n'
                                                    '        "renderer": '
                                                    '"src/recursive_integrity_toolkit/reports/json_report.py",\n'
                                                    '        "output_paths": '
                                                    '"src/recursive_integrity_toolkit/utils/paths.py",\n'
                                                    '    }\n'
                                                    '    added = {\n'
                                                    '        "unknown_runtime": '
                                                    '"src/recursive_integrity_toolkit/reports/unauthorized.py",\n'
                                                    '        "premature_completion": '
                                                    '"PHASE_4_COMPLETION.md", "premature_report": '
                                                    '"report.json",\n'
                                                    '    }\n'
                                                    '    if mutation in replacements:\n'
                                                    '        relative, original, replacement = '
                                                    'replacements[mutation]\n'
                                                    '        path = tmp_path / relative\n'
                                                    '        source = path.read_bytes()\n'
                                                    '        assert source.count(original) == 1\n'
                                                    '        path.write_bytes(source.replace(original, '
                                                    'replacement, 1))\n'
                                                    '    elif mutation in appended:\n'
                                                    '        path = tmp_path / appended[mutation]\n'
                                                    '        path.write_bytes(path.read_bytes() + '
                                                    'b"\\nUnauthorized Step 4 mutation\\n")\n'
                                                    '    elif mutation in added:\n'
                                                    '        path = tmp_path / added[mutation]\n'
                                                    '        assert not path.exists()\n'
                                                    '        path.write_text("Unauthorized later-stage '
                                                    'file\\n", encoding="utf-8")\n'
                                                    '    elif mutation == "missing_runtime":\n'
                                                    '        (tmp_path / '
                                                    '"src/recursive_integrity_toolkit/metrics/bounds.py").unlink()\n'
                                                    '    elif mutation.startswith("control_"):\n'
                                                    '        path = tmp_path / "PHASE_4_BASELINE.json"\n'
                                                    '        control = '
                                                    'json.loads(path.read_text(encoding="utf-8"))\n'
                                                    '        if mutation == "control_step":\n'
                                                    '            control["active_step"] = 5\n'
                                                    '        elif mutation == "control_scope":\n'
                                                    '            '
                                                    'control["runtime_paths_authorized"].append("src/recursive_integrity_toolkit/reports/json_report.py")\n'
                                                    '        else:\n'
                                                    '            control["schema_changes_authorized"] = '
                                                    'True\n'
                                                    '            '
                                                    'control["schema_paths_authorized"].append("schemas/report.schema.json")\n'
                                                    '        path.write_text(json.dumps(control), '
                                                    'encoding="utf-8")\n'
                                                    '    else:\n'
                                                    '        raise AssertionError(f"Unknown active mutation '
                                                    'case: {mutation}")\n'
                                                    '    with pytest.raises(ValueError):\n'
                                                    '        verify(tmp_path)',
                                             'node': 'test_phase4_step4_current_snapshot_checks_valid_tree_before_mutations',
                                             'old': 'def '
                                                    'test_phase4_step4_current_snapshot_checks_valid_tree_before_mutations(repo_root, '
                                                    'tmp_path, phase4_gate_tools, mutation, '
                                                    'phase4_step4_snapshot):\n'
                                                    '    import json\n'
                                                    '\n'
                                                    '    tracked = subprocess.check_output(["git", "-C", '
                                                    'str(repo_root), "ls-files", "-z"])\n'
                                                    '    paths = set(tracked.decode().split("\\0")) - {""}\n'
                                                    '    assert len(paths) == 227\n'
                                                    '    for relative in sorted(paths):\n'
                                                    '        destination = tmp_path / relative\n'
                                                    '        destination.parent.mkdir(parents=True, '
                                                    'exist_ok=True)\n'
                                                    '        shutil.copyfile(phase4_step4_snapshot / '
                                                    'relative, destination)\n'
                                                    '    verify = '
                                                    'phase4_gate_tools["verify_phase4_step4_snapshot"]\n'
                                                    '    baseline = verify(tmp_path)\n'
                                                    '    assert baseline["package_modules"] == 40\n'
                                                    '    assert baseline["frozen_runtime_modules"] == 35\n'
                                                    '    assert baseline["frozen_schemas"] == 5\n'
                                                    '    assert baseline["result_contracts_enabled"] is '
                                                    'True\n'
                                                    '    assert baseline["adapters_enabled"] is True\n'
                                                    '    assert baseline["privacy_views_enabled"] is True\n'
                                                    '    assert baseline["cli_analysis_enabled"] is False\n'
                                                    '    assert baseline["phase_complete"] is False\n'
                                                    '    if mutation == "unchanged":\n'
                                                    '        return\n'
                                                    '    replacements = {\n'
                                                    '        "formula": '
                                                    '("src/recursive_integrity_toolkit/metrics/diversity.py",\n'
                                                    '                    b"diversity = 1.0 - concentration", '
                                                    'b"diversity = 0.5 - concentration"),\n'
                                                    '        "math_oracle": '
                                                    '("tests/golden/phase3_math_cases.json", '
                                                    'b\'"v2_support":5\', b\'"v2_support":3\'),\n'
                                                    '        "hero": ("examples/hero/records_v2.csv", '
                                                    'b"v2_08,v2,", b"v2_99,v2,"),\n'
                                                    '        "dependency": ("pyproject.toml", b"numpy>=2.0", '
                                                    'b"numpy>=3.0"),\n'
                                                    '        "historical_assertion": '
                                                    '("tests/unit/test_phase4_contracts.py",\n'
                                                    "                                 b'    assert "
                                                    'control["active_phase"] == 4 and control["active_step"] '
                                                    "== 3\\n',\n"
                                                    '                                 b"    assert '
                                                    'True\\n"),\n'
                                                    '        "historical_tooling": '
                                                    '("scripts/release_check.py",\n'
                                                    '                               b"def '
                                                    'verify_phase4_step3_control(control: dict, step: int = '
                                                    '3) -> None:",\n'
                                                    '                               b"def '
                                                    'verify_phase4_step3_control(control: dict, step: int = '
                                                    '3) -> None:\\n    return"),\n'
                                                    '        "historical_binding": '
                                                    '("tests/integration/test_phase4_gates.py",\n'
                                                    '                               b"def '
                                                    'test_phase4_step3_current_workflows_preserve_matrix_and_use_active_dispatch(repo_root, '
                                                    'phase4_step3_snapshot):\\n    repo_root = '
                                                    'phase4_step3_snapshot\\n",\n'
                                                    '                               b"def '
                                                    'test_phase4_step3_current_workflows_preserve_matrix_and_use_active_dispatch(repo_root, '
                                                    'phase4_step3_snapshot):\\n"),\n'
                                                    '        "historical_document": ("docs/privacy.md", b"# '
                                                    'Privacy and Local Input Boundaries\\n",\n'
                                                    '                                b"# Unauthorized '
                                                    'Privacy and Local Input Boundaries\\n"),\n'
                                                    '        "input_hash_helper": '
                                                    '("src/recursive_integrity_toolkit/utils/hashing.py",\n'
                                                    '                              b"return '
                                                    'hashlib.sha256(data).hexdigest()", b"return '
                                                    'hashlib.sha256(b\'changed\').hexdigest()"),\n'
                                                    '        "config_resolver_helper": '
                                                    '("src/recursive_integrity_toolkit/config.py",\n'
                                                    '                                   b"def '
                                                    'resolve_config(", b"def resolve_config_disabled("),\n'
                                                    '    }\n'
                                                    '    appended = {\n'
                                                    '        "frozen_model": '
                                                    '"src/recursive_integrity_toolkit/models.py",\n'
                                                    '        "frozen_schema": "schemas/report.schema.json",\n'
                                                    '        "plan": "PHASE_4_PLAN.md",\n'
                                                    '        "cli": '
                                                    '"src/recursive_integrity_toolkit/cli.py",\n'
                                                    '        "renderer": '
                                                    '"src/recursive_integrity_toolkit/reports/json_report.py",\n'
                                                    '        "output_paths": '
                                                    '"src/recursive_integrity_toolkit/utils/paths.py",\n'
                                                    '    }\n'
                                                    '    added = {\n'
                                                    '        "unknown_runtime": '
                                                    '"src/recursive_integrity_toolkit/reports/unauthorized.py",\n'
                                                    '        "premature_completion": '
                                                    '"PHASE_4_COMPLETION.md", "premature_report": '
                                                    '"report.json",\n'
                                                    '    }\n'
                                                    '    if mutation in replacements:\n'
                                                    '        relative, original, replacement = '
                                                    'replacements[mutation]\n'
                                                    '        path = tmp_path / relative\n'
                                                    '        source = path.read_bytes()\n'
                                                    '        assert source.count(original) == 1\n'
                                                    '        path.write_bytes(source.replace(original, '
                                                    'replacement, 1))\n'
                                                    '    elif mutation in appended:\n'
                                                    '        path = tmp_path / appended[mutation]\n'
                                                    '        path.write_bytes(path.read_bytes() + '
                                                    'b"\\nUnauthorized Step 4 mutation\\n")\n'
                                                    '    elif mutation in added:\n'
                                                    '        path = tmp_path / added[mutation]\n'
                                                    '        assert not path.exists()\n'
                                                    '        path.write_text("Unauthorized later-stage '
                                                    'file\\n", encoding="utf-8")\n'
                                                    '    elif mutation == "missing_runtime":\n'
                                                    '        (tmp_path / '
                                                    '"src/recursive_integrity_toolkit/metrics/bounds.py").unlink()\n'
                                                    '    elif mutation.startswith("control_"):\n'
                                                    '        path = tmp_path / "PHASE_4_BASELINE.json"\n'
                                                    '        control = '
                                                    'json.loads(path.read_text(encoding="utf-8"))\n'
                                                    '        if mutation == "control_step":\n'
                                                    '            control["active_step"] = 5\n'
                                                    '        elif mutation == "control_scope":\n'
                                                    '            '
                                                    'control["runtime_paths_authorized"].append("src/recursive_integrity_toolkit/reports/json_report.py")\n'
                                                    '        else:\n'
                                                    '            control["schema_changes_authorized"] = '
                                                    'True\n'
                                                    '            '
                                                    'control["schema_paths_authorized"].append("schemas/report.schema.json")\n'
                                                    '        path.write_text(json.dumps(control), '
                                                    'encoding="utf-8")\n'
                                                    '    else:\n'
                                                    '        raise AssertionError(f"Unknown active mutation '
                                                    'case: {mutation}")\n'
                                                    '    with pytest.raises(ValueError):\n'
                                                    '        verify(tmp_path)'},
                                            {'new': 'def '
                                                    'test_phase4_step4_privacy_ast_checks_current_source_before_rejecting_scope_injection(repo_root, '
                                                    'tmp_path, relative, injection, phase4_step5_snapshot):\n'
                                                    '    checker = runpy.run_path(str(repo_root / '
                                                    '"scripts/check_traceability.py"), '
                                                    'run_name="phase4_step4_ast_tests")\n'
                                                    '    verify = checker["phase4_step4_runtime_boundary"]\n'
                                                    '    repository_path = '
                                                    '"src/recursive_integrity_toolkit/" + relative\n'
                                                    '    current = (phase4_step5_snapshot if relative == '
                                                    '"utils/logging.py" else repo_root) / repository_path\n'
                                                    '    verify(current, repository_path)\n'
                                                    '    copy = tmp_path / "source.py"\n'
                                                    '    copy.write_bytes(current.read_bytes() + injection)\n'
                                                    '    with pytest.raises(ValueError):\n'
                                                    '        verify(copy, repository_path)',
                                             'node': 'test_phase4_step4_privacy_ast_checks_current_source_before_rejecting_scope_injection',
                                             'old': 'def '
                                                    'test_phase4_step4_privacy_ast_checks_current_source_before_rejecting_scope_injection(repo_root, '
                                                    'tmp_path, relative, injection):\n'
                                                    '    checker = runpy.run_path(str(repo_root / '
                                                    '"scripts/check_traceability.py"), '
                                                    'run_name="phase4_step4_ast_tests")\n'
                                                    '    verify = checker["phase4_step4_runtime_boundary"]\n'
                                                    '    repository_path = '
                                                    '"src/recursive_integrity_toolkit/" + relative\n'
                                                    '    current = repo_root / repository_path\n'
                                                    '    verify(current, repository_path)\n'
                                                    '    copy = tmp_path / "source.py"\n'
                                                    '    copy.write_bytes(current.read_bytes() + injection)\n'
                                                    '    with pytest.raises(ValueError):\n'
                                                    '        verify(copy, repository_path)'}],
 'tests/unit/test_phase4_contracts.py': [{'new': 'def '
                                                 'test_phase4_step5_approved_control_keeps_independent_step4_anchors(phase4_tools, '
                                                 'phase4_step5_snapshot):\n'
                                                 '    control = json.loads((phase4_step5_snapshot / '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\n'
                                                 '    assert phase4_tools["PHASE4_STEP4_FINAL"] == '
                                                 '"49454a9b162cb8d35e38d1cb1ae32cb208d3a01c"\n'
                                                 '    assert phase4_tools["PHASE4_STEP4_TREE"] == '
                                                 '"79264d845e08f73ee68e160dea04f7786f18fd0a"\n'
                                                 '    assert phase4_tools["PHASE4_STEP4_TEST_TREE"] == '
                                                 '"4aa4ca0b22f8b8c25afe27feeaba713d6f0830bf"\n'
                                                 '    assert control["active_phase"] == 4 and '
                                                 'control["active_step"] == 5\n'
                                                 '    assert control["approval_basis"] == "很好，Phase 4 Step 5 '
                                                 '继续"\n'
                                                 '    assert control["baseline_commit"] == BASELINE\n'
                                                 '    assert control["previous_step_commit"] == '
                                                 '"49454a9b162cb8d35e38d1cb1ae32cb208d3a01c"\n'
                                                 '    assert control["previous_step_tree"] == '
                                                 '"79264d845e08f73ee68e160dea04f7786f18fd0a"\n'
                                                 '    assert control["previous_step_test_tree"] == '
                                                 '"4aa4ca0b22f8b8c25afe27feeaba713d6f0830bf"\n'
                                                 '    assert control["previous_step_core_tests"] == 3071\n'
                                                 '    assert control["previous_step_parquet_tests"] == 3074\n'
                                                 '    assert len(control["previous_step_files_sha256"]) == '
                                                 '227\n'
                                                 '    assert set(control["runtime_paths_authorized"]) == {\n'
                                                 '        '
                                                 '"src/recursive_integrity_toolkit/reports/json_report.py",\n'
                                                 '        '
                                                 '"src/recursive_integrity_toolkit/reports/markdown_report.py",\n'
                                                 '    }\n'
                                                 '    assert control["schema_changes_authorized"] is False\n'
                                                 '    assert control["schema_paths_authorized"] == []\n'
                                                 '    assert control["new_files_permitted"] == []\n'
                                                 '    for name in ("phase_complete", "next_step_authorized", '
                                                 '"main_merge_authorized", "publication_authorized"):\n'
                                                 '        assert control[name] is False\n'
                                                 '    phase4_tools["verify_phase4_step5_control"](control, '
                                                 'step=5)\n'
                                                 '    with pytest.raises(ValueError):\n'
                                                 '        '
                                                 'phase4_tools["verify_phase4_step4_control"](control, '
                                                 'step=4)',
                                          'node': 'test_phase4_step5_approved_control_keeps_independent_step4_anchors',
                                          'old': 'def '
                                                 'test_phase4_step5_approved_control_keeps_independent_step4_anchors(phase4_tools):\n'
                                                 '    control = json.loads((ROOT / '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\n'
                                                 '    assert phase4_tools["PHASE4_STEP4_FINAL"] == '
                                                 '"49454a9b162cb8d35e38d1cb1ae32cb208d3a01c"\n'
                                                 '    assert phase4_tools["PHASE4_STEP4_TREE"] == '
                                                 '"79264d845e08f73ee68e160dea04f7786f18fd0a"\n'
                                                 '    assert phase4_tools["PHASE4_STEP4_TEST_TREE"] == '
                                                 '"4aa4ca0b22f8b8c25afe27feeaba713d6f0830bf"\n'
                                                 '    assert control["active_phase"] == 4 and '
                                                 'control["active_step"] == 5\n'
                                                 '    assert control["approval_basis"] == "很好，Phase 4 Step 5 '
                                                 '继续"\n'
                                                 '    assert control["baseline_commit"] == BASELINE\n'
                                                 '    assert control["previous_step_commit"] == '
                                                 '"49454a9b162cb8d35e38d1cb1ae32cb208d3a01c"\n'
                                                 '    assert control["previous_step_tree"] == '
                                                 '"79264d845e08f73ee68e160dea04f7786f18fd0a"\n'
                                                 '    assert control["previous_step_test_tree"] == '
                                                 '"4aa4ca0b22f8b8c25afe27feeaba713d6f0830bf"\n'
                                                 '    assert control["previous_step_core_tests"] == 3071\n'
                                                 '    assert control["previous_step_parquet_tests"] == 3074\n'
                                                 '    assert len(control["previous_step_files_sha256"]) == '
                                                 '227\n'
                                                 '    assert set(control["runtime_paths_authorized"]) == {\n'
                                                 '        '
                                                 '"src/recursive_integrity_toolkit/reports/json_report.py",\n'
                                                 '        '
                                                 '"src/recursive_integrity_toolkit/reports/markdown_report.py",\n'
                                                 '    }\n'
                                                 '    assert control["schema_changes_authorized"] is False\n'
                                                 '    assert control["schema_paths_authorized"] == []\n'
                                                 '    assert control["new_files_permitted"] == []\n'
                                                 '    for name in ("phase_complete", "next_step_authorized", '
                                                 '"main_merge_authorized", "publication_authorized"):\n'
                                                 '        assert control[name] is False\n'
                                                 '    phase4_tools["verify_phase4_step5_control"](control, '
                                                 'step=5)\n'
                                                 '    with pytest.raises(ValueError):\n'
                                                 '        '
                                                 'phase4_tools["verify_phase4_step4_control"](control, '
                                                 'step=4)'},
                                         {'new': 'def '
                                                 'test_phase4_step5_control_rejects_forged_scope_and_stage(phase4_tools, '
                                                 'field, value, phase4_step5_snapshot):\n'
                                                 '    control = json.loads((phase4_step5_snapshot / '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\n'
                                                 '    verify = phase4_tools["verify_phase4_step5_control"]\n'
                                                 '    verify(control, step=5)\n'
                                                 '    control[field] = value\n'
                                                 '    with pytest.raises(ValueError):\n'
                                                 '        verify(control, step=5)',
                                          'node': 'test_phase4_step5_control_rejects_forged_scope_and_stage',
                                          'old': 'def '
                                                 'test_phase4_step5_control_rejects_forged_scope_and_stage(phase4_tools, '
                                                 'field, value):\n'
                                                 '    control = json.loads((ROOT / '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\n'
                                                 '    verify = phase4_tools["verify_phase4_step5_control"]\n'
                                                 '    verify(control, step=5)\n'
                                                 '    control[field] = value\n'
                                                 '    with pytest.raises(ValueError):\n'
                                                 '        verify(control, step=5)'},
                                         {'new': 'def '
                                                 'test_phase4_step5_control_rejects_unapproved_dispatch(phase4_tools, '
                                                 'step, phase4_step5_snapshot):\n'
                                                 '    control = json.loads((phase4_step5_snapshot / '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\n'
                                                 '    phase4_tools["verify_phase4_step5_control"](control, '
                                                 'step=5)\n'
                                                 '    with pytest.raises(ValueError):\n'
                                                 '        '
                                                 'phase4_tools["verify_phase4_step5_control"](control, '
                                                 'step=step)',
                                          'node': 'test_phase4_step5_control_rejects_unapproved_dispatch',
                                          'old': 'def '
                                                 'test_phase4_step5_control_rejects_unapproved_dispatch(phase4_tools, '
                                                 'step):\n'
                                                 '    control = json.loads((ROOT / '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\n'
                                                 '    phase4_tools["verify_phase4_step5_control"](control, '
                                                 'step=5)\n'
                                                 '    with pytest.raises(ValueError):\n'
                                                 '        '
                                                 'phase4_tools["verify_phase4_step5_control"](control, '
                                                 'step=step)'},
                                         {'new': 'def '
                                                 'test_phase4_step5_control_requires_explicit_approval_fields(phase4_tools, '
                                                 'field, phase4_step5_snapshot):\n'
                                                 '    control = json.loads((phase4_step5_snapshot / '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\n'
                                                 '    phase4_tools["verify_phase4_step5_control"](control)\n'
                                                 '    del control[field]\n'
                                                 '    with pytest.raises(ValueError):\n'
                                                 '        '
                                                 'phase4_tools["verify_phase4_step5_control"](control)',
                                          'node': 'test_phase4_step5_control_requires_explicit_approval_fields',
                                          'old': 'def '
                                                 'test_phase4_step5_control_requires_explicit_approval_fields(phase4_tools, '
                                                 'field):\n'
                                                 '    control = json.loads((ROOT / '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\n'
                                                 '    phase4_tools["verify_phase4_step5_control"](control)\n'
                                                 '    del control[field]\n'
                                                 '    with pytest.raises(ValueError):\n'
                                                 '        '
                                                 'phase4_tools["verify_phase4_step5_control"](control)'},
                                         {'new': 'def '
                                                 'test_phase4_step5_control_cannot_mint_extra_permission(phase4_tools, '
                                                 'phase4_step5_snapshot):\n'
                                                 '    control = json.loads((phase4_step5_snapshot / '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\n'
                                                 '    phase4_tools["verify_phase4_step5_control"](control)\n'
                                                 '    control["approved_scope_expansion"] = {"step": 6, '
                                                 '"publication": True}\n'
                                                 '    with pytest.raises(ValueError):\n'
                                                 '        '
                                                 'phase4_tools["verify_phase4_step5_control"](control)',
                                          'node': 'test_phase4_step5_control_cannot_mint_extra_permission',
                                          'old': 'def '
                                                 'test_phase4_step5_control_cannot_mint_extra_permission(phase4_tools):\n'
                                                 '    control = json.loads((ROOT / '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\n'
                                                 '    phase4_tools["verify_phase4_step5_control"](control)\n'
                                                 '    control["approved_scope_expansion"] = {"step": 6, '
                                                 '"publication": True}\n'
                                                 '    with pytest.raises(ValueError):\n'
                                                 '        '
                                                 'phase4_tools["verify_phase4_step5_control"](control)'},
                                         {'new': 'def '
                                                 'test_phase4_step5_historical_migrations_preserve_ten_step4_gate_nodes(phase4_tools, '
                                                 'phase4_step4_snapshot, phase4_step5_snapshot):\n'
                                                 '    registry = phase4_tools["PHASE4_STEP5_MIGRATIONS"]\n'
                                                 '    expected = {\n'
                                                 '        "tests/unit/test_phase4_contracts.py": {\n'
                                                 '            '
                                                 '"test_phase4_step4_approved_control_keeps_independent_step3_anchors",\n'
                                                 '            '
                                                 '"test_phase4_step4_control_rejects_forged_scope_and_stage",\n'
                                                 '            '
                                                 '"test_phase4_step4_control_rejects_unapproved_dispatch",\n'
                                                 '            '
                                                 '"test_phase4_step4_control_requires_explicit_approval_fields",\n'
                                                 '            '
                                                 '"test_phase4_step4_control_cannot_mint_extra_permission",\n'
                                                 '            '
                                                 '"test_phase4_step4_historical_migrations_preserve_ten_step3_gate_nodes",\n'
                                                 '            '
                                                 '"test_phase4_step4_historical_guard_rejects_assertion_and_binding_weakening",\n'
                                                 '        },\n'
                                                 '        "tests/integration/test_phase4_gates.py": {\n'
                                                 '            '
                                                 '"test_phase4_step4_current_runtime_opens_only_privacy_metadata_modules_and_freezes_schema",\n'
                                                 '            '
                                                 '"test_phase4_step4_current_workflows_preserve_matrix_and_use_active_dispatch",\n'
                                                 '            '
                                                 '"test_phase4_step4_current_snapshot_checks_valid_tree_before_mutations",\n'
                                                 '        },\n'
                                                 '    }\n'
                                                 '    assert set(registry) == set(expected)\n'
                                                 '    assert sum(len(rows) for rows in registry.values()) == '
                                                 '13\n'
                                                 '    for path, nodes in expected.items():\n'
                                                 '        assert {row["node"] for row in registry[path]} == '
                                                 'nodes\n'
                                                 '        '
                                                 'phase4_tools["verify_phase4_step5_test_migration"](\n'
                                                 '            path, (phase4_step4_snapshot / '
                                                 'path).read_bytes(), (phase4_step5_snapshot / '
                                                 'path).read_bytes(),\n'
                                                 '        )',
                                          'node': 'test_phase4_step5_historical_migrations_preserve_ten_step4_gate_nodes',
                                          'old': 'def '
                                                 'test_phase4_step5_historical_migrations_preserve_ten_step4_gate_nodes(phase4_tools, '
                                                 'phase4_step4_snapshot):\n'
                                                 '    registry = phase4_tools["PHASE4_STEP5_MIGRATIONS"]\n'
                                                 '    expected = {\n'
                                                 '        "tests/unit/test_phase4_contracts.py": {\n'
                                                 '            '
                                                 '"test_phase4_step4_approved_control_keeps_independent_step3_anchors",\n'
                                                 '            '
                                                 '"test_phase4_step4_control_rejects_forged_scope_and_stage",\n'
                                                 '            '
                                                 '"test_phase4_step4_control_rejects_unapproved_dispatch",\n'
                                                 '            '
                                                 '"test_phase4_step4_control_requires_explicit_approval_fields",\n'
                                                 '            '
                                                 '"test_phase4_step4_control_cannot_mint_extra_permission",\n'
                                                 '            '
                                                 '"test_phase4_step4_historical_migrations_preserve_ten_step3_gate_nodes",\n'
                                                 '            '
                                                 '"test_phase4_step4_historical_guard_rejects_assertion_and_binding_weakening",\n'
                                                 '        },\n'
                                                 '        "tests/integration/test_phase4_gates.py": {\n'
                                                 '            '
                                                 '"test_phase4_step4_current_runtime_opens_only_privacy_metadata_modules_and_freezes_schema",\n'
                                                 '            '
                                                 '"test_phase4_step4_current_workflows_preserve_matrix_and_use_active_dispatch",\n'
                                                 '            '
                                                 '"test_phase4_step4_current_snapshot_checks_valid_tree_before_mutations",\n'
                                                 '        },\n'
                                                 '    }\n'
                                                 '    assert set(registry) == set(expected)\n'
                                                 '    assert sum(len(rows) for rows in registry.values()) == '
                                                 '13\n'
                                                 '    for path, nodes in expected.items():\n'
                                                 '        assert {row["node"] for row in registry[path]} == '
                                                 'nodes\n'
                                                 '        '
                                                 'phase4_tools["verify_phase4_step5_test_migration"](\n'
                                                 '            path, (phase4_step4_snapshot / '
                                                 'path).read_bytes(), (ROOT / path).read_bytes(),\n'
                                                 '        )'},
                                         {'new': 'def '
                                                 'test_phase4_step5_historical_guard_rejects_assertion_and_binding_weakening(phase4_tools, '
                                                 'phase4_step4_snapshot, mutation, phase4_step5_snapshot):\n'
                                                 '    path = "tests/unit/test_phase4_contracts.py"\n'
                                                 '    before = (phase4_step4_snapshot / path).read_bytes()\n'
                                                 '    after = (phase4_step5_snapshot / path).read_bytes()\n'
                                                 '    verify = '
                                                 'phase4_tools["verify_phase4_step5_test_migration"]\n'
                                                 '    verify(path, before, after)\n'
                                                 '    if mutation == "old_assertion":\n'
                                                 '        original = b\'    assert control["active_phase"] '
                                                 '== 4 and control["active_step"] == 4\\n\'\n'
                                                 '        assert after.count(original) == 1\n'
                                                 '        after = after.replace(original, b"    assert '
                                                 'True\\n", 1)\n'
                                                 '    elif mutation == "wrong_snapshot":\n'
                                                 "        original = (b'def "
                                                 'test_phase4_step4_control_cannot_mint_extra_permission(phase4_tools, '
                                                 "phase4_step4_snapshot):\\n'\n"
                                                 "                    b'    control = "
                                                 'json.loads((phase4_step4_snapshot / '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\\n\')\n'
                                                 '        assert after.count(original) == 1\n'
                                                 '        after = after.replace(original, '
                                                 "original.replace(b'(phase4_step4_snapshot /', b'(ROOT /'), "
                                                 '1)\n'
                                                 '    elif mutation == "rebind_node":\n'
                                                 '        after += b"\\ndef '
                                                 'test_phase4_step4_fixed_boundary_opens_only_approved_existing_paths():\\n    '
                                                 'assert True\\n"\n'
                                                 '    else:\n'
                                                 '        after += b"\\ndef '
                                                 'test_phase4_step5_mutator(value=globals().clear()):\\n    '
                                                 'pass\\n"\n'
                                                 '    with pytest.raises(ValueError):\n'
                                                 '        verify(path, before, after)',
                                          'node': 'test_phase4_step5_historical_guard_rejects_assertion_and_binding_weakening',
                                          'old': 'def '
                                                 'test_phase4_step5_historical_guard_rejects_assertion_and_binding_weakening(phase4_tools, '
                                                 'phase4_step4_snapshot, mutation):\n'
                                                 '    path = "tests/unit/test_phase4_contracts.py"\n'
                                                 '    before = (phase4_step4_snapshot / path).read_bytes()\n'
                                                 '    after = (ROOT / path).read_bytes()\n'
                                                 '    verify = '
                                                 'phase4_tools["verify_phase4_step5_test_migration"]\n'
                                                 '    verify(path, before, after)\n'
                                                 '    if mutation == "old_assertion":\n'
                                                 '        original = b\'    assert control["active_phase"] '
                                                 '== 4 and control["active_step"] == 4\\n\'\n'
                                                 '        assert after.count(original) == 1\n'
                                                 '        after = after.replace(original, b"    assert '
                                                 'True\\n", 1)\n'
                                                 '    elif mutation == "wrong_snapshot":\n'
                                                 "        original = (b'def "
                                                 'test_phase4_step4_control_cannot_mint_extra_permission(phase4_tools, '
                                                 "phase4_step4_snapshot):\\n'\n"
                                                 "                    b'    control = "
                                                 'json.loads((phase4_step4_snapshot / '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\\n\')\n'
                                                 '        assert after.count(original) == 1\n'
                                                 '        after = after.replace(original, '
                                                 "original.replace(b'(phase4_step4_snapshot /', b'(ROOT /'), "
                                                 '1)\n'
                                                 '    elif mutation == "rebind_node":\n'
                                                 '        after += b"\\ndef '
                                                 'test_phase4_step4_fixed_boundary_opens_only_approved_existing_paths():\\n    '
                                                 'assert True\\n"\n'
                                                 '    else:\n'
                                                 '        after += b"\\ndef '
                                                 'test_phase4_step5_mutator(value=globals().clear()):\\n    '
                                                 'pass\\n"\n'
                                                 '    with pytest.raises(ValueError):\n'
                                                 '        verify(path, before, after)'}]}


PHASE4_STEP6_ALLOWED = {'.github/workflows/ci.yml',
 '.github/workflows/golden.yml',
 '.github/workflows/release.yml',
 '.github/workflows/security.yml',
 'PHASE_4_BASELINE.json',
 'PHASE_4_DECISIONS.md',
 'docs/architecture.md',
 'docs/cli.md',
 'docs/privacy.md',
 'docs/theory_traceability.md',
 'scripts/check_spec_consistency.py',
 'scripts/check_traceability.py',
 'scripts/release_check.py',
 'src/recursive_integrity_toolkit/utils/logging.py',
 'src/recursive_integrity_toolkit/utils/paths.py',
 'tests/conftest.py',
 'tests/integration/test_ci_workflows.py',
 'tests/integration/test_hero_structure.py',
 'tests/integration/test_license_notices.py',
 'tests/integration/test_no_algorithms.py',
 'tests/integration/test_no_network.py',
 'tests/integration/test_optional_dependency.py',
 'tests/integration/test_owner_ids.py',
 'tests/integration/test_package_import.py',
 'tests/integration/test_package_install.py',
 'tests/integration/test_phase4_gates.py',
 'tests/integration/test_prohibited_structure.py',
 'tests/integration/test_repository_structure.py',
 'tests/integration/test_schema_json.py',
 'tests/unit/test_phase4_contracts.py',
 'tests/unit/test_phase4_output_safety.py'}


def _phase4_step5_files():
    """Read the exact accepted Step 5 Git tree and verify every blob identity."""
    for suffix, expected in (("^{commit}", PHASE4_STEP5_FINAL), ("^{tree}", PHASE4_STEP5_TREE),
                             (":tests", PHASE4_STEP5_TEST_TREE)):
        if git("rev-parse", PHASE4_STEP5_FINAL + suffix).decode().strip() != expected:
            raise ValueError("Pinned Phase 4 Step 5 identity mismatch")
    objects = {}
    for entry in git("ls-tree", "-rz", PHASE4_STEP5_FINAL).split(b"\0"):
        if not entry:
            continue
        metadata, raw_path = entry.split(b"\t", 1)
        mode, kind, oid = metadata.split()
        path = raw_path.decode("utf-8")
        if (mode not in (b"100644", b"100755") or kind != b"blob" or path in objects
                or path.startswith("/") or ".." in path.split("/") or ".git" in path.split("/")):
            raise ValueError("Unsafe pinned Step 5 Git object")
        objects[path] = oid.decode("ascii")
    if len(objects) != 227:
        raise ValueError("Pinned Step 5 must contain exactly 227 files")
    files = {}
    with zipfile.ZipFile(io.BytesIO(git("archive", "--format=zip", PHASE4_STEP5_FINAL))) as archive:
        names = [item.filename for item in archive.infolist() if not item.is_dir()]
        if len(names) != len(objects) or set(names) != set(objects):
            raise ValueError("Pinned Step 5 archive identity mismatch")
        for name in names:
            raw = archive.read(name)
            oid = hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()
            if oid != objects[name]:
                raise ValueError(f"Pinned Step 5 blob mismatch: {name}")
            files[name] = raw
    return MappingProxyType(files)


def phase4_step6_expected_control() -> dict:
    """Actual Step 6 approval is independent of the mutable control document."""
    prior = _phase4_step5_files()
    result = phase4_step5_expected_control()
    result.update({
        "control_version": "1.5", "active_step": 6,
        "approval_date": PHASE4_STEP6_APPROVAL_DATE, "approval_basis": PHASE4_STEP6_APPROVAL,
        "previous_step_commit": PHASE4_STEP5_FINAL,
        "previous_step_tree": PHASE4_STEP5_TREE,
        "previous_step_test_tree": PHASE4_STEP5_TEST_TREE,
        "previous_step_core_tests": 3215, "previous_step_parquet_tests": 3218,
        "previous_step_files_sha256": {p: hashlib.sha256(raw).hexdigest() for p, raw in sorted(prior.items())},
        "permitted_paths": sorted(PHASE4_STEP6_ALLOWED), "new_files_permitted": list(PHASE4_STEP6_NEW),
        "runtime_changes_authorized": True, "schema_changes_authorized": False,
        "runtime_paths_authorized": sorted(p for p in PHASE4_STEP6_ALLOWED if p.startswith("src/")),
        "schema_paths_authorized": [],
        "step5_historical_binding_nodes": {p: sorted({r["node"] for r in rows})
                                          for p, rows in sorted(PHASE4_STEP6_MIGRATIONS.items())},
    })
    return result


def verify_phase4_step6_control(control: dict, step: int = 6) -> None:
    if type(step) is not int or step != 6 or type(control) is not dict:
        raise ValueError("Unsupported Phase 4 Step 6 stage/control")
    try:
        actual = json.dumps(control, sort_keys=True, ensure_ascii=True, allow_nan=False)
        expected = json.dumps(phase4_step6_expected_control(), sort_keys=True, ensure_ascii=True, allow_nan=False)
    except (TypeError, ValueError) as error:
        raise ValueError("Invalid Phase 4 Step 6 control") from error
    if actual != expected:
        raise ValueError("Phase 4 control differs from the independently approved Step 6 contract")


def verify_phase4_step6_changes(changes: list[tuple[str, str]]) -> None:
    seen = set()
    for status, path in changes:
        if path in seen or path not in PHASE4_STEP6_ALLOWED or status != ("A" if path in PHASE4_STEP6_NEW else "M"):
            raise ValueError(f"Unapproved Phase 4 Step 6 path/operation: {status} {path}")
        seen.add(path)


def _phase4_step6_header(node, path):
    """Allow explicit test parametrization/fixtures, never definition-time effects."""
    for decorator in node.decorator_list:
        if not isinstance(decorator, ast.Call) or ast.unparse(decorator.func) not in {
                "pytest.fixture", "pytest.mark.parametrize"}:
            raise ValueError(f"Unapproved Step 6 test decorator: {path}:{node.name}")
        if ast.unparse(decorator.func) == "pytest.fixture" and not node.name.startswith("phase4_step"):
            raise ValueError("A Step 6 fixture must have an explicit scoped name")
        if any(keyword.arg is None for keyword in decorator.keywords):
            raise ValueError("Decorator expansion is outside the Step 6 contract")
        for value in [*decorator.args, *(keyword.value for keyword in decorator.keywords)]:
            try:
                ast.literal_eval(value)
            except (ValueError, TypeError, SyntaxError) as error:
                raise ValueError("Step 6 decorator arguments must be literal") from error
    clone = ast.parse(ast.unparse(node)).body[0]
    clone.decorator_list = []
    _phase4_preserve_function_header(clone, path)


def _phase4_step6_append_only(before: bytes, after: bytes, path: str) -> None:
    if not after.startswith(before):
        raise ValueError(f"Inherited Step 5 prefix changed: {path}")
    old, new = ast.parse(before), ast.parse(after)
    bindings = set()
    for node in old.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            bindings.add(node.name)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            bindings.update(alias.asname or alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            bindings.update(child.id for target in targets for child in ast.walk(target) if isinstance(child, ast.Name))
    for node in new.body[len(old.body):]:
        if not isinstance(node, ast.FunctionDef) or node.name in bindings:
            raise ValueError(f"Step 6 addition executes, rebinds or shadows inherited source: {path}")
        allowed_snapshot = path == "tests/conftest.py" and node.name == "phase4_step5_snapshot"
        if not allowed_snapshot and not node.name.startswith(("test_phase4_step6_", "phase4_step6_")):
            raise ValueError(f"Step 6 added test/helper is not explicitly scoped: {path}:{node.name}")
        if path == "tests/conftest.py" and node.name != "phase4_step5_snapshot":
            raise ValueError("Only the pinned Step 5 shared fixture is authorized")
        bindings.add(node.name)
        _phase4_step6_header(node, path)


def verify_phase4_step6_test_migration(path: str, before: bytes, after: bytes) -> None:
    prior = _phase4_step5_files()
    if path not in prior or path not in PHASE4_STEP6_ALLOWED or before != prior[path] or not path.startswith("tests/"):
        raise ValueError("Step 6 migration requires the exact named Step 5 source")
    _phase4_step6_check_test_migration(path, before, after)


def _phase4_step6_check_test_migration(path: str, before: bytes, after: bytes) -> None:
    """Check a source already read from the verified Step 5 immutable mapping."""
    expected = before
    for row in PHASE4_STEP6_MIGRATIONS.get(path, []):
        old, new = row["old"].encode(), row["new"].encode()
        if expected.count(old) != 1:
            raise ValueError("Step 5 historical binding is not unique")
        expected = expected.replace(old, new, 1)
    _phase4_step6_append_only(expected, after, path)


def _phase4_step6_preserve_tooling(before: bytes, after: bytes, path: str) -> None:
    """Preserve exact inherited statements using one source-line split per tree."""
    if path == "scripts/release_check.py":
        old = '    return phase4_cli_main() if explicit_phase4 else main()'
        new = ('    explicit_step6 = "--step=6" in argv or any(a == "--step" and b == "6" for a, b in zip(argv, argv[1:]))\n'
               '    if explicit_phase4 and explicit_step6:\n'
               '        return phase4_step6_cli_main()\n' + old)
        # Earlier preserved dispatch functions contain this source too; bind cli_main only.
        parsed = ast.parse(before)
        entry = next(node for node in parsed.body if isinstance(node, ast.FunctionDef) and node.name == "cli_main")
        old_entry = ast.get_source_segment(before.decode(), entry)
        if old_entry.count(old) != 1:
            raise ValueError("Step 5 release dispatcher identity mismatch")
        replacements = [(old_entry, old_entry.replace(old, new, 1))]
    else:
        old = '    if args.phase == 4 and args.step == 5:\n        return phase4_step5_main(step=args.step)\n'
        new = old + '    if args.phase == 4 and args.step == 6:\n        return phase4_step6_main(step=args.step)\n'
        replacements = [(old, new),
                        ('Choose explicit --phase 3 --step 11 or --phase 4 --step 1 or --phase 4 --step 2 or --phase 4 --step 3 or --phase 4 --step 4 or --phase 4 --step 5',
                         'Choose explicit --phase 3 --step 11 or --phase 4 --step 1 or --phase 4 --step 2 or --phase 4 --step 3 or --phase 4 --step 4 or --phase 4 --step 5 or --phase 4 --step 6')]
    expected = before
    for old, new in replacements:
        if expected.count(old.encode()) != 1:
            raise ValueError(f"Historical dispatcher identity mismatch: {path}")
        expected = expected.replace(old.encode(), new.encode(), 1)
    trees = [ast.parse(expected), ast.parse(after)]
    lines = [expected.splitlines(keepends=True), after.splitlines(keepends=True)]
    def segment(index, node):
        if node.lineno == node.end_lineno:
            return lines[index][node.lineno - 1][node.col_offset:node.end_col_offset]
        return (lines[index][node.lineno - 1][node.col_offset:]
                + b"".join(lines[index][node.lineno:node.end_lineno - 1])
                + lines[index][node.end_lineno - 1][:node.end_col_offset])
    def entry_guard(node):
        return isinstance(node, ast.If) and isinstance(node.test, ast.Compare) and "__name__" in ast.unparse(node.test)
    guards = [n for n in trees[1].body if entry_guard(n)]
    expected_guard = ast.parse('if __name__ == "__main__":\n    raise SystemExit(cli_main())').body[0]
    if len(guards) != 1 or ast.dump(guards[0]) != ast.dump(expected_guard):
        raise ValueError(f"Unapproved Step 6 maintainer entrypoint: {path}")
    historical = [n for n in trees[0].body if not entry_guard(n)]
    current = [n for n in trees[1].body if not entry_guard(n)]
    old_entries = [(segment(0, n), ast.dump(n)) for n in historical]
    cursor = 0
    for node in current:
        if cursor < len(old_entries) and (segment(1, node), ast.dump(node)) == old_entries[cursor]:
            cursor += 1
            continue
        if isinstance(node, ast.FunctionDef) and (node.name == "_phase4_step5_files" or node.name.startswith(
                ("phase4_step6_", "_phase4_step6_", "verify_phase4_step6_", "audit_phase4_step6"))):
            _phase4_preserve_function_header(node, path)
            continue
        if isinstance(node, ast.Assign) and all(isinstance(target, ast.Name) and target.id.startswith(
                ("PHASE4_STEP6_", "PHASE4_STEP5_")) for target in node.targets):
            try:
                ast.literal_eval(node.value)
            except (ValueError, TypeError, SyntaxError) as error:
                raise ValueError(f"Nonliteral added Step 6 maintainer constant: {path}") from error
            continue
        raise ValueError(f"Unapproved Step 6 maintainer addition: {path}")
    if cursor != len(historical):
        raise ValueError(f"Inherited Step 5 maintainer statement changed: {path}")
    def binding_counts(tree):
        counts = {}
        for node in tree.body:
            names = []
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                names = [node.name]
            elif isinstance(node, (ast.Assign, ast.AnnAssign)):
                targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                names = [child.id for target in targets for child in ast.walk(target) if isinstance(child, ast.Name)]
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                names = [alias.asname or alias.name.split(".")[0] for alias in node.names]
            for name in names:
                counts[name] = counts.get(name, 0) + 1
        return counts
    inherited_counts = binding_counts(trees[0])
    for name, count in binding_counts(trees[1]).items():
        if count > inherited_counts.get(name, 1):
            raise ValueError(f"Duplicate Step 6 maintainer binding: {path}:{name}")


def verify_phase4_step6_snapshot(root: Path = ROOT) -> dict:
    prior = _phase4_step5_files()
    for path, raw in prior.items():
        target = root / path
        if not target.is_file() or target.is_symlink():
            raise ValueError(f"Missing or aliased inherited Step 5 file: {path}")
        current = target.read_bytes()
        if path not in PHASE4_STEP6_ALLOWED and current != raw:
            raise ValueError(f"Protected Step 5 bytes changed: {path}")
        if path.startswith("tests/") and path in PHASE4_STEP6_ALLOWED:
            _phase4_step6_check_test_migration(path, raw, current)
        elif path.startswith("scripts/") and path in PHASE4_STEP6_ALLOWED:
            _phase4_step6_preserve_tooling(raw, current, path)
        elif path in {"docs/architecture.md", "docs/theory_traceability.md", "docs/privacy.md", "docs/cli.md", "PHASE_4_DECISIONS.md"}:
            if not current.startswith(raw):
                raise ValueError(f"Step 5 historical documentation prefix changed: {path}")
    for path in PHASE4_STEP6_NEW:
        target = root / path
        if not target.is_file() or target.is_symlink():
            raise ValueError("Missing Step 6 output safety tests")
        _phase4_step6_new_test(target.read_bytes(), path)
    for path in sorted(p for p in PHASE4_STEP6_ALLOWED if p.startswith("src/")):
        _phase4_step6_preserve_runtime(prior[path], (root / path).read_bytes(), path)
    actual_modules = {p.relative_to(root).as_posix() for p in (root / "src/recursive_integrity_toolkit").rglob("*.py")}
    expected_modules = {p for p in prior if p.startswith("src/") and p.endswith(".py")}
    if actual_modules != expected_modules or len(actual_modules) != 40:
        raise ValueError("Step 6 cannot change the runtime module set")
    if {p.name for p in (root / "schemas").iterdir()} != {Path(p).name for p in prior if p.startswith("schemas/")}:
        raise ValueError("Step 6 cannot change the schema set")
    if hashlib.sha256((root / "PHASE_4_PLAN.md").read_bytes()).hexdigest() != PHASE4_PLAN_SHA256:
        raise ValueError("Approved Phase 4 plan changed")
    verify_phase4_step6_control(json.loads((root / "PHASE_4_BASELINE.json").read_text(encoding="utf-8")))
    decisions = (root / "PHASE_4_DECISIONS.md").read_text(encoding="utf-8")
    if PHASE4_STEP6_APPROVAL not in decisions or PHASE4_STEP5_FINAL not in decisions:
        raise ValueError("Actual Step 6 authorization or Step 5 evidence anchor missing")
    if any((root / name).exists() for name in PHASE4_FORBIDDEN_OUTPUTS):
        raise ValueError("Step 6 cannot create Phase 4 completion records or audit outputs")
    import runpy
    checker = runpy.run_path(str(root / "scripts/check_traceability.py"), run_name="phase4_step6_renderer_boundary")
    checker["phase4_step6_output_boundary"](root)
    schema_bytes = (root / "schemas/report.schema.json").read_bytes()
    if hashlib.sha256(schema_bytes).hexdigest() != PHASE4_STEP2_REPORT_SCHEMA_SHA256:
        raise ValueError("Step 6 report schema differs from its independently reviewed bytes")
    schema = json.loads(schema_bytes)
    if (schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema"
            or schema.get("type") != "object" or schema.get("additionalProperties") is not False):
        raise ValueError("Step 6 report schema dialect/closed root mismatch")
    return {"package_modules": 40, "frozen_runtime_modules": 38, "frozen_schemas": 5,
            "hero_files_unchanged": 6, "historical_phase3_migrated_nodes": 16,
            "phase_complete": False, "result_contracts_enabled": True,
            "adapters_enabled": True, "privacy_views_enabled": True, "renderers_enabled": True, "output_publication_enabled": True, "cli_analysis_enabled": False}


def audit_phase4_step6(step: int = 6) -> dict:
    verify_phase4_step6_control(json.loads((ROOT / "PHASE_4_BASELINE.json").read_text(encoding="utf-8")), step)
    result = {"phase": 4, "active_step": step, **verify_phase4_step6_snapshot(),
              "phase0_hashes_verified": 16, "publication_authorized": False}
    print(json.dumps(result, indent=2))
    return result


def audit_phase4_step6_diff(step: int = 6) -> dict:
    if type(step) is not int or step != 6:
        raise ValueError("Unsupported Phase 4 Step 6 stage")
    _phase4_step5_files()
    subprocess.run(["git", "-C", str(ROOT), "merge-base", "--is-ancestor", PHASE4_STEP5_FINAL, "HEAD"], check=True)
    raw = git("diff", "--name-status", "--no-renames", "-z", PHASE4_STEP5_FINAL, "--").split(b"\0")
    raw = [part.decode("utf-8") for part in raw if part]
    if len(raw) % 2:
        raise ValueError("Malformed Step 6 Git difference records")
    changes = list(zip(raw[::2], raw[1::2]))
    changes.extend(("A", p.decode()) for p in git("ls-files", "--others", "--exclude-standard", "-z").split(b"\0") if p)
    verify_phase4_step6_changes(changes)
    result = {"previous_step_commit": PHASE4_STEP5_FINAL, "changed_files": len(changes),
              "changes": changes, "step": 6, "scope": "PASS"}
    print(json.dumps(result, indent=2))
    return result


def phase4_step6_baseline_evidence(output: Path) -> dict:
    """Reconcile all inherited identities, including the accepted Step 5 suite."""
    output.mkdir(parents=True, exist_ok=True)
    inherited = phase4_step5_baseline_evidence(output / "phase4-step5-inherited")
    with tempfile.TemporaryDirectory(prefix="rit-p4-step5-identities-") as temp:
        baseline = Path(temp)
        for name, raw in _phase4_step5_files().items():
            target = baseline / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(raw)
        old, old_log = _collect(baseline)
    current, current_log = _collect(ROOT)
    expected = 3218 if os.environ.get("RIT_TEST_PARQUET") == "1" else 3215
    if len(old) != expected or set(old) - set(current):
        raise ValueError("Accepted Phase 4 Step 5 test identities were lost")
    result = {"baseline_commit": PHASE4_STEP5_FINAL, "baseline_test_tree": PHASE4_STEP5_TEST_TREE,
              "baseline_nodeids": old, "current_nodeids": current, "missing_nodeids": [],
              "baseline_tests": len(old), "current_tests": len(current), "inherited": inherited,
              "nodeids_sha256": hashlib.sha256(("\n".join(old)+"\n").encode()).hexdigest()}
    (output / "phase4_step6_test_identity_manifest.json").write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    (output / "phase4-step5-collection.log").write_text(old_log, encoding="utf-8")
    (output / "phase4-step6-collection.log").write_text(current_log, encoding="utf-8")
    print(json.dumps({k: result[k] for k in ("baseline_tests", "current_tests", "missing_nodeids")}, indent=2))
    return result


def phase4_step6_candidate(output: Path, step: int = 6) -> None:
    """Build tested Step 6 intermediate evidence without declaring Phase 4 complete."""
    if os.environ.get("RIT_TEST_PARQUET") != "1" or importlib.util.find_spec("pyarrow") is None:
        raise ValueError("Step 6 candidate evidence requires RIT_TEST_PARQUET=1 and real PyArrow")
    output.mkdir(parents=True, exist_ok=True)
    result = audit_phase4_step6(step)
    result["diff"] = audit_phase4_step6_diff(step)
    if git("status", "--porcelain").strip():
        raise ValueError("Step 6 candidate archive requires committed, clean source")
    result["core"] = verify_junit(output / "core.xml", minimum=3215)
    result["parquet"] = verify_junit(output / "parquet.xml", require_parquet=True, minimum=3218)
    result["core_math_measurements"] = verify_step10_evidence(output / "core.xml", output / "phase4-step6-core-observations.json")
    result["parquet_math_measurements"] = verify_step10_evidence(output / "parquet.xml", output / "phase4-step6-parquet-observations.json")
    identity = phase4_step6_baseline_evidence(output)
    result["test_identity"] = {k: identity[k] for k in ("baseline_tests", "current_tests", "nodeids_sha256")}
    expected = set()
    for node in identity["current_nodeids"]:
        base, bracket, parameter = node.partition("[")
        owner, name = base.rsplit("::", 1)
        expected.add((owner.removesuffix(".py").replace("/", ".").replace("::", "."), name + bracket + parameter))
    for name, parquet in (("core.xml", False), ("parquet.xml", True)):
        cases = {(c.get("classname", ""), c.get("name", "")) for c in ET.parse(output / name).getroot().iter("testcase")}
        target = expected if parquet else {c for c in expected if c[1] not in PARQUET_CASES}
        if cases != target:
            raise ValueError(f"Step 6 JUnit does not execute the entire current suite: {name}")
    wheel, _ = verify_distributions(output / "dist")
    smoke_installed(wheel)
    smoke_installed_duplicates(wheel)
    phase4_step2_installed_contract_smoke(wheel)
    phase4_step3_installed_assembly_smoke(wheel)
    phase4_step4_installed_privacy_smoke(wheel)
    phase4_step5_installed_renderers_smoke(wheel)
    phase4_step6_installed_publication_smoke(wheel)
    archive = output / "recursive-integrity-toolkit-phase4-step6-candidate.zip"
    subprocess.run(["git", "-C", str(ROOT), "archive", "--format=zip", "--prefix=recursive-integrity-toolkit/", "HEAD", "-o", str(archive.resolve())], check=True)
    tracked = {p for p in git("ls-files", "-z").decode().split("\0") if p}
    with zipfile.ZipFile(archive) as zipped:
        entries = [item.filename for item in zipped.infolist() if not item.is_dir()]
        prefix = "recursive-integrity-toolkit/"
        if (len(entries) != len(set(entries)) or any(not name.startswith(prefix) for name in entries)):
            raise ValueError("Step 6 source archive has duplicate or unprefixed entries")
        names = {name.removeprefix(prefix) for name in entries}
        if names != tracked or len(tracked) != 228 or len(entries) != 228:
            raise ValueError("Step 6 source archive file set mismatch")
        for name in names:
            if zipped.read("recursive-integrity-toolkit/"+name) != (ROOT / name).read_bytes():
                raise ValueError(f"Step 6 source archive byte mismatch: {name}")
    result.update({"commit": git("rev-parse", "HEAD").decode().strip(),
                   "tree": git("rev-parse", "HEAD^{tree}").decode().strip(),
                   "source_archive": archive.name, "tracked_files": len(tracked),
                   "python": sys.version, "platform": sys.platform,
                   "versions": {name: importlib.metadata.version(name) for name in ("numpy", "pandas", "pytest")}})
    (output / "phase4_step6_execution_metadata.json").write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    (output / "phase4_step6_repository_files.sha256").write_text("".join(f"{hashlib.sha256((ROOT/name).read_bytes()).hexdigest()}  {name}\n" for name in sorted(tracked)), encoding="utf-8")
    paths = sorted(p for p in output.rglob("*") if p.is_file() and p.name != "phase4_step6_artifacts.sha256")
    (output / "phase4_step6_artifacts.sha256").write_text("".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(output).as_posix()}\n" for p in paths), encoding="utf-8")
    print(f"Phase 4 Step 6 candidate: {len(tracked)} source files verified; Phase 4 remains incomplete.")


def phase4_step6_cli_main() -> int:
    parser = argparse.ArgumentParser(description="Phase 4 Step 6 maintainer gate")
    parser.add_argument("--phase", type=int, choices=(4,), required=True)
    parser.add_argument("--step", type=int, choices=(6,), required=True)
    parser.add_argument("--diff", action="store_true")
    parser.add_argument("--junit", type=Path)
    parser.add_argument("--require-parquet", action="store_true")
    parser.add_argument("--minimum-tests", type=int, default=1)
    parser.add_argument("--baseline-evidence", type=Path)
    parser.add_argument("--dist", type=Path)
    parser.add_argument("--smoke-wheel", type=Path)
    parser.add_argument("--candidate", type=Path)
    parser.add_argument("--delivery", type=Path)
    args = parser.parse_args()
    if args.delivery is not None:
        raise ValueError("Phase 4 Step 6 cannot certify a final phase delivery")
    if args.junit is not None:
        verify_junit(args.junit, require_parquet=args.require_parquet, minimum=args.minimum_tests)
    elif args.baseline_evidence is not None:
        phase4_step6_baseline_evidence(args.baseline_evidence)
    elif args.dist is not None:
        audit_phase4_step6(args.step)
        wheel, _ = verify_distributions(args.dist)
        smoke_installed(wheel)
        smoke_installed_duplicates(wheel)
        phase4_step2_installed_contract_smoke(wheel)
        phase4_step3_installed_assembly_smoke(wheel)
        phase4_step4_installed_privacy_smoke(wheel)
        phase4_step5_installed_renderers_smoke(wheel)
        phase4_step6_installed_publication_smoke(wheel)
    elif args.smoke_wheel is not None:
        smoke_installed(args.smoke_wheel)
    elif args.candidate is not None:
        phase4_step6_candidate(args.candidate, args.step)
    else:
        audit_phase4_step6(args.step)
        if args.diff:
            audit_phase4_step6_diff(args.step)
    return 0


def _phase4_step6_new_test(raw: bytes, path: str) -> None:
    """Only literal test declarations and explicitly listed safe imports."""
    allowed = {"__future__", "errno", "io", "json", "os", "pathlib", "types", "pytest",
               "recursive_integrity_toolkit.utils"}
    for index, node in enumerate(ast.parse(raw).body):
        if index == 0 and isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            continue
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            modules = [node.module] if isinstance(node, ast.ImportFrom) else [alias.name for alias in node.names]
            if any(module not in allowed for module in modules):
                raise ValueError("Unapproved Step 6 test import")
            continue
        if not isinstance(node, ast.FunctionDef) or not node.name.startswith(("test_phase4_step6_", "phase4_step6_")):
            raise ValueError("Step 6 output tests gained definition-time execution")
        _phase4_step6_header(node, path)


def _phase4_step6_preserve_runtime(before: bytes, after: bytes, path: str) -> None:
    """Allow ownership-header maintenance and byte-exact additive helpers only."""
    try:
        old, new = ast.parse(before), ast.parse(after)
    except (SyntaxError, UnicodeError, ValueError) as error:
        raise ValueError("Output helper source cannot be inspected") from error
    if not ast.get_docstring(old) or not ast.get_docstring(new):
        raise ValueError("Output helper ownership documentation is required")
    old_tail = b"".join(before.splitlines(keepends=True)[old.body[0].end_lineno:])
    new_tail = b"".join(after.splitlines(keepends=True)[new.body[0].end_lineno:])
    if not new_tail.startswith(old_tail):
        raise ValueError(f"Inherited input/diagnostic bytes changed: {path}")



def phase4_step6_installed_publication_smoke(wheel: Path) -> None:
    """Exercise installed output safety outside the source checkout."""
    with tempfile.TemporaryDirectory(prefix="rit-p4-step6-installed-") as temporary:
        work = Path(temporary)
        subprocess.run([sys.executable, "-m", "venv", str(work / "venv")], check=True)
        bindir = work / "venv" / ("Scripts" if os.name == "nt" else "bin")
        python = bindir / ("python.exe" if os.name == "nt" else "python")
        subprocess.run([str(python), "-m", "pip", "install", "--no-index", "--no-deps", str(wheel.resolve())], cwd=work, check=True)
        program = 'import importlib.abc, json, os, socket, sys\nfrom pathlib import Path\nclass BlockOptional(importlib.abc.MetaPathFinder):\n    def find_spec(self, fullname, path=None, target=None):\n        if fullname.split(".")[0] in ("numpy", "pandas", "pyarrow"):\n            raise AssertionError("optional or analytical dependency imported")\nsys.meta_path.insert(0, BlockOptional())\ndef phase4_step6_view(mode="standard", label="publication-case"):\n    from recursive_integrity_toolkit.reports.assembly import privacy_view\n    from recursive_integrity_toolkit.result import CanonicalReport\n    from recursive_integrity_toolkit.utils.hashing import IdentifierProtection\n\n    payload = {\n        "run": {\n            "run_id": label, "toolkit_version": "0.1.0.dev2", "report_schema_version": "1.0",\n            "started_at": "2026-09-20T00:00:00+00:00", "completed_at": "2026-09-20T00:00:00.500000+00:00",\n            "duration_seconds": 0.5, "python_version": "3.12.14", "platform": "independent-test-platform",\n            "command": "rit validate", "config_hash": "0123456789abcdef" * 4,\n            "random_seed": None, "strict_mode": False, "redacted_mode": False,\n            "network_call_count": 0, "deterministic": True, "privacy_mode": "standard",\n            "run_status": "complete", "null_reasons": {"random_seed": "No stochastic scenario was requested."},\n        },\n        "inputs": {}, "observability": {}, "capabilities": {}, "observed_facts": {},\n        "derived_metrics": {}, "proxy_signals": {}, "simulations": {},\n        "unavailable_conclusions": [], "recommended_next_metadata": [], "warnings": [], "errors": [],\n    }\n    return privacy_view(CanonicalReport.from_dict(payload), mode=mode,\n                        protection=IdentifierProtection.create(secret=b"publication-test-only-key-32byte!"))\nfrom recursive_integrity_toolkit.utils.paths import publish_reports, PublicationResult\nfrom recursive_integrity_toolkit.utils.logging import format_publication_diagnostic\nfrom recursive_integrity_toolkit.utils import paths\nfrom recursive_integrity_toolkit.reports.json_report import render_json\nfrom recursive_integrity_toolkit.reports.markdown_report import render_markdown\nimport recursive_integrity_toolkit as package\nassert not Path(package.__file__).resolve().is_relative_to(Path(sys.argv[2]).resolve())\nwork=Path(sys.argv[1]); source=work/\'input.txt\'; source.write_bytes(b\'PRIVATE_INSTALLED_SOURCE\')\nview=phase4_step6_view(\'redacted\')\nexpected={\'report.json\':render_json(view).encode(), \'report.md\':render_markdown(view).encode()}\ndef deny(*args, **kwargs):\n    raise AssertionError(\'network forbidden\')\nsocket.socket=deny; socket.getaddrinfo=deny\nactual_open=os.open\ndef no_input(path,*args,**kwargs):\n    assert Path(path)!=source\n    return actual_open(path,*args,**kwargs)\nos.open=no_input\ndef no_analysis(frame,event,arg):\n    if event==\'call\':\n        name=frame.f_globals.get(\'__name__\',\'\')\n        assert not name.startswith((\'recursive_integrity_toolkit.io.\',\'recursive_integrity_toolkit.metrics.\',\'recursive_integrity_toolkit.representations.\'))\nsys.setprofile(no_analysis)\ntry:\n    result=publish_reports(view,work/\'out\',input_paths=(source,))\n    assert result==PublicationResult(\'complete\',None,0,(\'report.json\',\'report.md\'))\n    assert publish_reports(view,work/\'out\',input_paths=(source,)).code==\'E_OUTPUT_EXISTS\'\n    actual_publish=paths._output_publish_one\n    def fail_second(src,dst):\n        if dst.name==\'report.md\':raise OSError(\'PRIVATE_INSTALLED_FAILURE\')\n        return actual_publish(src,dst)\n    paths._output_publish_one=fail_second\n    failed=publish_reports(view,work/\'failure\',input_paths=(source,))\n    assert failed.status==\'failed\' and failed.code==\'E_OUTPUT_IO\' and failed.temporary_cleanup_complete\n    assert \'PRIVATE_\' not in format_publication_diagnostic(failed)\nfinally:\n    sys.setprofile(None)\nassert {p.name:p.read_bytes() for p in (work/\'out\').iterdir()}==expected\nassert list((work/\'failure\').iterdir())==[]\nassert source.read_bytes()==b\'PRIVATE_INSTALLED_SOURCE\'\nprint(\'installed Step 6: exact safe JSON/Markdown bytes, no-overwrite, partial failure cleanup, safe diagnostics, unchanged input, blocked network/analysis: PASS\')\n'
        subprocess.run([str(python), "-I", "-c", program, str(work), str(ROOT)], cwd=work, check=True)



# Phase 4 Step 7: single-version CLI orchestration, no later-stage expansion.


PHASE4_STEP6_FINAL = 'aa2355f2359c3af4fc05345c792f9903b0d5858c'


PHASE4_STEP6_TREE = 'd9b6910079f49a2c739f86eceec05040918a41a5'


PHASE4_STEP6_TEST_TREE = '8d3a03c61da807d1fef8d26fc4af0d6f72e4546e'


PHASE4_STEP7_APPROVAL = 'Phase 4 Step 7 继续'


PHASE4_STEP7_APPROVAL_DATE = '2026-09-21'


PHASE4_STEP7_NEW = ('tests/integration/test_phase4_cli.py',)


PHASE4_STEP7_ALLOWED = {'.github/workflows/ci.yml',
 '.github/workflows/golden.yml',
 '.github/workflows/release.yml',
 '.github/workflows/security.yml',
 'PHASE_4_BASELINE.json',
 'PHASE_4_DECISIONS.md',
 'docs/architecture.md',
 'docs/cli.md',
 'docs/theory_traceability.md',
 'scripts/check_spec_consistency.py',
 'scripts/check_traceability.py',
 'scripts/release_check.py',
 'src/recursive_integrity_toolkit/cli.py',
 'src/recursive_integrity_toolkit/config.py',
 'tests/conftest.py',
 'tests/integration/test_ci_workflows.py',
 'tests/integration/test_cli_validation.py',
 'tests/integration/test_hero_structure.py',
 'tests/integration/test_license_notices.py',
 'tests/integration/test_no_algorithms.py',
 'tests/integration/test_no_network.py',
 'tests/integration/test_optional_dependency.py',
 'tests/integration/test_owner_ids.py',
 'tests/integration/test_package_import.py',
 'tests/integration/test_package_install.py',
 'tests/integration/test_phase4_cli.py',
 'tests/integration/test_phase4_gates.py',
 'tests/integration/test_prohibited_structure.py',
 'tests/integration/test_repository_structure.py',
 'tests/integration/test_schema_json.py',
 'tests/unit/test_phase4_contracts.py'}


PHASE4_STEP7_MIGRATIONS = {'tests/integration/test_phase4_gates.py': [{'new': 'def '
                                                    'test_phase4_step6_current_runtime_opens_only_output_helpers_and_freezes_schema(repo_root, '
                                                    'phase4_step5_snapshot, phase4_step6_snapshot):\n'
                                                    '    repo_root = phase4_step6_snapshot\n'
                                                    '    package = "src/recursive_integrity_toolkit"\n'
                                                    '    current = {path.relative_to(repo_root).as_posix(): '
                                                    'hashlib.sha256(path.read_bytes()).hexdigest()\n'
                                                    '               for path in (repo_root / '
                                                    'package).rglob("*.py")}\n'
                                                    '    frozen = '
                                                    '{path.relative_to(phase4_step5_snapshot).as_posix(): '
                                                    'hashlib.sha256(path.read_bytes()).hexdigest()\n'
                                                    '              for path in (phase4_step5_snapshot / '
                                                    'package).rglob("*.py")}\n'
                                                    '    assert len(current) == len(frozen) == 40\n'
                                                    '    assert current.keys() == frozen.keys()\n'
                                                    '    opened = {package + "/" + relative for relative in '
                                                    '(\n'
                                                    '        "utils/paths.py", "utils/logging.py",\n'
                                                    '    )}\n'
                                                    '    assert {path for path in current if current[path] '
                                                    '!= frozen[path]} == opened\n'
                                                    '    assert {path: digest for path, digest in '
                                                    'current.items() if path not in opened} == {\n'
                                                    '        path: digest for path, digest in frozen.items() '
                                                    'if path not in opened\n'
                                                    '    }\n'
                                                    '    schemas = {path.name: path.read_bytes() for path in '
                                                    '(repo_root / "schemas").glob("*.json")}\n'
                                                    '    assert len(schemas) == 5\n'
                                                    '    assert schemas == {path.name: path.read_bytes() for '
                                                    'path in (phase4_step5_snapshot / '
                                                    '"schemas").glob("*.json")}',
                                             'node': 'test_phase4_step6_current_runtime_opens_only_output_helpers_and_freezes_schema',
                                             'old': 'def '
                                                    'test_phase4_step6_current_runtime_opens_only_output_helpers_and_freezes_schema(repo_root, '
                                                    'phase4_step5_snapshot):\n'
                                                    '    package = "src/recursive_integrity_toolkit"\n'
                                                    '    current = {path.relative_to(repo_root).as_posix(): '
                                                    'hashlib.sha256(path.read_bytes()).hexdigest()\n'
                                                    '               for path in (repo_root / '
                                                    'package).rglob("*.py")}\n'
                                                    '    frozen = '
                                                    '{path.relative_to(phase4_step5_snapshot).as_posix(): '
                                                    'hashlib.sha256(path.read_bytes()).hexdigest()\n'
                                                    '              for path in (phase4_step5_snapshot / '
                                                    'package).rglob("*.py")}\n'
                                                    '    assert len(current) == len(frozen) == 40\n'
                                                    '    assert current.keys() == frozen.keys()\n'
                                                    '    opened = {package + "/" + relative for relative in '
                                                    '(\n'
                                                    '        "utils/paths.py", "utils/logging.py",\n'
                                                    '    )}\n'
                                                    '    assert {path for path in current if current[path] '
                                                    '!= frozen[path]} == opened\n'
                                                    '    assert {path: digest for path, digest in '
                                                    'current.items() if path not in opened} == {\n'
                                                    '        path: digest for path, digest in frozen.items() '
                                                    'if path not in opened\n'
                                                    '    }\n'
                                                    '    schemas = {path.name: path.read_bytes() for path in '
                                                    '(repo_root / "schemas").glob("*.json")}\n'
                                                    '    assert len(schemas) == 5\n'
                                                    '    assert schemas == {path.name: path.read_bytes() for '
                                                    'path in (phase4_step5_snapshot / '
                                                    '"schemas").glob("*.json")}'},
                                            {'new': 'def '
                                                    'test_phase4_step6_current_workflows_preserve_matrix_and_use_active_dispatch(repo_root, '
                                                    'phase4_step6_snapshot):\n'
                                                    '    repo_root = phase4_step6_snapshot\n'
                                                    '    names = {"ci.yml", "golden.yml", "security.yml", '
                                                    '"release.yml"}\n'
                                                    '    root = repo_root / ".github/workflows"\n'
                                                    '    expected_timeouts = {"ci.yml": [60, 20], '
                                                    '"golden.yml": [15], "security.yml": [20], '
                                                    '"release.yml": [25]}\n'
                                                    '    assert {path.name for path in root.glob("*.yml")} '
                                                    '== names\n'
                                                    '    for name in sorted(names):\n'
                                                    '        text = (root / '
                                                    'name).read_text(encoding="utf-8")\n'
                                                    '        assert [int(line.split(":", 1)[1]) for line in '
                                                    'text.splitlines()\n'
                                                    '                if '
                                                    'line.strip().startswith("timeout-minutes:")] == '
                                                    'expected_timeouts[name]\n'
                                                    '        assert "Phase 4 Step 6" in text, name\n'
                                                    '        assert "--phase 4 --step 6" in text, name\n'
                                                    '        for older in ("--phase 4 --step 5", "--phase 4 '
                                                    '--step 4", "--phase 4 --step 3", "--phase 4 --step 2", '
                                                    '"--phase 4 --step 1", "--phase 3 --step 11"):\n'
                                                    '            assert older not in text, (name, older)\n'
                                                    '        assert "permissions:\\n  contents: read" in '
                                                    'text\n'
                                                    '        assert "persist-credentials: false" in text\n'
                                                    '        assert "timeout-minutes:" in text and "set -euo '
                                                    'pipefail" in text\n'
                                                    '        assert "actions/upload-artifact@v4" in text and '
                                                    '"if-no-files-found: error" in text\n'
                                                    '        for line in text.splitlines():\n'
                                                    '            if "python scripts/release_check.py" in '
                                                    'line:\n'
                                                    '                assert "--phase 4 --step 6" in line, '
                                                    '(name, line)\n'
                                                    '        for forbidden in ("continue-on-error:", "|| '
                                                    'true", "contents: write", "id-token: write", "twine '
                                                    'upload", "git push"):\n'
                                                    '            assert forbidden not in text, (name, '
                                                    'forbidden)\n'
                                                    '    ci = (root / "ci.yml").read_text(encoding="utf-8")\n'
                                                    "    for required in ('os: [ubuntu-latest, "
                                                    'windows-latest]\', \'python-version: ["3.11", '
                                                    '"3.12"]\',\n'
                                                    "                     'dependencies: [current, "
                                                    'minimum]\', \'"numpy==2.0.0" "pandas==2.2.2"\',\n'
                                                    '                     \'RIT_TEST_PARQUET: "0"\', '
                                                    '\'RIT_TEST_PARQUET: "1"\', \'--require-parquet\',\n'
                                                    "                     '--baseline-evidence', 'python -m "
                                                    "pip check',\n"
                                                    "                     '--minimum-tests 3215', "
                                                    "'--minimum-tests 3218',\n"
                                                    '                     "find_spec(\'pyarrow\') is None", '
                                                    "'import pyarrow'):\n"
                                                    '        assert required in ci\n'
                                                    '    assert ci.count("python -m pytest -p '
                                                    'no:cacheprovider -q --junitxml=") == 2\n'
                                                    '    assert " -k " not in ci\n'
                                                    '    golden = (root / '
                                                    '"golden.yml").read_text(encoding="utf-8")\n'
                                                    '    for required in '
                                                    '("tests/golden/test_phase3_math.py", '
                                                    '"tests/integration/test_hero_structure.py",\n'
                                                    '                     '
                                                    '"tests/integration/test_phase3_metric_pipeline.py"):\n'
                                                    '        assert required in golden\n'
                                                    '    security = (root / '
                                                    '"security.yml").read_text(encoding="utf-8")\n'
                                                    '    for required in '
                                                    "('tests/integration/test_no_network.py', "
                                                    "'tests/integration/test_optional_dependency.py',\n"
                                                    '                     '
                                                    "'tests/unit/test_PR012_evidence_classes.py', "
                                                    "'tests/unit/test_PR013_report_schema.py',\n"
                                                    '                     '
                                                    "'tests/unit/test_PR014_unavailable.py', "
                                                    "'tests/unit/test_PR015_redaction.py',\n"
                                                    '                     '
                                                    "'tests/unit/test_PR016_determinism.py', "
                                                    "'tests/unit/test_PR018_language.py',\n"
                                                    '                     '
                                                    "'tests/integration/test_partial_provenance_report.py',\n"
                                                    '                     '
                                                    "'tests/integration/test_partial_lineage_report.py',\n"
                                                    '                     '
                                                    "'tests/unit/test_phase4_output_safety.py', "
                                                    "'tests/unit/test_phase4_contracts.py', "
                                                    "'tests/integration/test_phase4_gates.py'):\n"
                                                    '        assert required in security\n'
                                                    '    release = (root / '
                                                    '"release.yml").read_text(encoding="utf-8")\n'
                                                    '    assert "python -m build" in release and "python -m '
                                                    'twine check --strict" in release\n'
                                                    '    assert "--dist" in release and "--candidate" in '
                                                    'release\n'
                                                    '    assert "--delivery" not in release\n'
                                                    '    assert '
                                                    '"recursive-integrity-toolkit-phase4-step6-candidate" in '
                                                    'release\n'
                                                    '    assert "rit-phase4-step4" not in release\n'
                                                    '    assert "--minimum-tests 3215" in release and '
                                                    '"--minimum-tests 3218" in release\n'
                                                    '    assert release.count("python -m pytest -p '
                                                    'no:cacheprovider -q --junitxml=") == 2',
                                             'node': 'test_phase4_step6_current_workflows_preserve_matrix_and_use_active_dispatch',
                                             'old': 'def '
                                                    'test_phase4_step6_current_workflows_preserve_matrix_and_use_active_dispatch(repo_root):\n'
                                                    '    names = {"ci.yml", "golden.yml", "security.yml", '
                                                    '"release.yml"}\n'
                                                    '    root = repo_root / ".github/workflows"\n'
                                                    '    expected_timeouts = {"ci.yml": [60, 20], '
                                                    '"golden.yml": [15], "security.yml": [20], '
                                                    '"release.yml": [25]}\n'
                                                    '    assert {path.name for path in root.glob("*.yml")} '
                                                    '== names\n'
                                                    '    for name in sorted(names):\n'
                                                    '        text = (root / '
                                                    'name).read_text(encoding="utf-8")\n'
                                                    '        assert [int(line.split(":", 1)[1]) for line in '
                                                    'text.splitlines()\n'
                                                    '                if '
                                                    'line.strip().startswith("timeout-minutes:")] == '
                                                    'expected_timeouts[name]\n'
                                                    '        assert "Phase 4 Step 6" in text, name\n'
                                                    '        assert "--phase 4 --step 6" in text, name\n'
                                                    '        for older in ("--phase 4 --step 5", "--phase 4 '
                                                    '--step 4", "--phase 4 --step 3", "--phase 4 --step 2", '
                                                    '"--phase 4 --step 1", "--phase 3 --step 11"):\n'
                                                    '            assert older not in text, (name, older)\n'
                                                    '        assert "permissions:\\n  contents: read" in '
                                                    'text\n'
                                                    '        assert "persist-credentials: false" in text\n'
                                                    '        assert "timeout-minutes:" in text and "set -euo '
                                                    'pipefail" in text\n'
                                                    '        assert "actions/upload-artifact@v4" in text and '
                                                    '"if-no-files-found: error" in text\n'
                                                    '        for line in text.splitlines():\n'
                                                    '            if "python scripts/release_check.py" in '
                                                    'line:\n'
                                                    '                assert "--phase 4 --step 6" in line, '
                                                    '(name, line)\n'
                                                    '        for forbidden in ("continue-on-error:", "|| '
                                                    'true", "contents: write", "id-token: write", "twine '
                                                    'upload", "git push"):\n'
                                                    '            assert forbidden not in text, (name, '
                                                    'forbidden)\n'
                                                    '    ci = (root / "ci.yml").read_text(encoding="utf-8")\n'
                                                    "    for required in ('os: [ubuntu-latest, "
                                                    'windows-latest]\', \'python-version: ["3.11", '
                                                    '"3.12"]\',\n'
                                                    "                     'dependencies: [current, "
                                                    'minimum]\', \'"numpy==2.0.0" "pandas==2.2.2"\',\n'
                                                    '                     \'RIT_TEST_PARQUET: "0"\', '
                                                    '\'RIT_TEST_PARQUET: "1"\', \'--require-parquet\',\n'
                                                    "                     '--baseline-evidence', 'python -m "
                                                    "pip check',\n"
                                                    "                     '--minimum-tests 3215', "
                                                    "'--minimum-tests 3218',\n"
                                                    '                     "find_spec(\'pyarrow\') is None", '
                                                    "'import pyarrow'):\n"
                                                    '        assert required in ci\n'
                                                    '    assert ci.count("python -m pytest -p '
                                                    'no:cacheprovider -q --junitxml=") == 2\n'
                                                    '    assert " -k " not in ci\n'
                                                    '    golden = (root / '
                                                    '"golden.yml").read_text(encoding="utf-8")\n'
                                                    '    for required in '
                                                    '("tests/golden/test_phase3_math.py", '
                                                    '"tests/integration/test_hero_structure.py",\n'
                                                    '                     '
                                                    '"tests/integration/test_phase3_metric_pipeline.py"):\n'
                                                    '        assert required in golden\n'
                                                    '    security = (root / '
                                                    '"security.yml").read_text(encoding="utf-8")\n'
                                                    '    for required in '
                                                    "('tests/integration/test_no_network.py', "
                                                    "'tests/integration/test_optional_dependency.py',\n"
                                                    '                     '
                                                    "'tests/unit/test_PR012_evidence_classes.py', "
                                                    "'tests/unit/test_PR013_report_schema.py',\n"
                                                    '                     '
                                                    "'tests/unit/test_PR014_unavailable.py', "
                                                    "'tests/unit/test_PR015_redaction.py',\n"
                                                    '                     '
                                                    "'tests/unit/test_PR016_determinism.py', "
                                                    "'tests/unit/test_PR018_language.py',\n"
                                                    '                     '
                                                    "'tests/integration/test_partial_provenance_report.py',\n"
                                                    '                     '
                                                    "'tests/integration/test_partial_lineage_report.py',\n"
                                                    '                     '
                                                    "'tests/unit/test_phase4_output_safety.py', "
                                                    "'tests/unit/test_phase4_contracts.py', "
                                                    "'tests/integration/test_phase4_gates.py'):\n"
                                                    '        assert required in security\n'
                                                    '    release = (root / '
                                                    '"release.yml").read_text(encoding="utf-8")\n'
                                                    '    assert "python -m build" in release and "python -m '
                                                    'twine check --strict" in release\n'
                                                    '    assert "--dist" in release and "--candidate" in '
                                                    'release\n'
                                                    '    assert "--delivery" not in release\n'
                                                    '    assert '
                                                    '"recursive-integrity-toolkit-phase4-step6-candidate" in '
                                                    'release\n'
                                                    '    assert "rit-phase4-step4" not in release\n'
                                                    '    assert "--minimum-tests 3215" in release and '
                                                    '"--minimum-tests 3218" in release\n'
                                                    '    assert release.count("python -m pytest -p '
                                                    'no:cacheprovider -q --junitxml=") == 2'},
                                            {'new': 'def '
                                                    'test_phase4_step6_current_snapshot_checks_valid_tree_before_mutations(repo_root, '
                                                    'tmp_path, phase4_gate_tools, mutation, '
                                                    'phase4_step6_snapshot):\n'
                                                    '    import json\n'
                                                    '\n'
                                                    '    paths = '
                                                    '{path.relative_to(phase4_step6_snapshot).as_posix()\n'
                                                    '             for path in '
                                                    'phase4_step6_snapshot.rglob("*") if path.is_file()}\n'
                                                    '    assert len(paths) == 228\n'
                                                    '    for relative in sorted(paths):\n'
                                                    '        destination = tmp_path / relative\n'
                                                    '        destination.parent.mkdir(parents=True, '
                                                    'exist_ok=True)\n'
                                                    '        shutil.copyfile(phase4_step6_snapshot / '
                                                    'relative, destination)\n'
                                                    '    verify = '
                                                    'phase4_gate_tools["verify_phase4_step6_snapshot"]\n'
                                                    '    baseline = verify(tmp_path)\n'
                                                    '    assert baseline["package_modules"] == 40\n'
                                                    '    assert baseline["frozen_runtime_modules"] == 38\n'
                                                    '    assert baseline["frozen_schemas"] == 5\n'
                                                    '    assert baseline["result_contracts_enabled"] is '
                                                    'True\n'
                                                    '    assert baseline["adapters_enabled"] is True\n'
                                                    '    assert baseline["privacy_views_enabled"] is True\n'
                                                    '    assert baseline["renderers_enabled"] is True\n'
                                                    '    assert baseline["output_publication_enabled"] is '
                                                    'True\n'
                                                    '    assert baseline["cli_analysis_enabled"] is False\n'
                                                    '    assert baseline["phase_complete"] is False\n'
                                                    '    if mutation == "unchanged":\n'
                                                    '        return\n'
                                                    '    replacements = {\n'
                                                    '        "formula": '
                                                    '("src/recursive_integrity_toolkit/metrics/diversity.py",\n'
                                                    '                    b"diversity = 1.0 - concentration", '
                                                    'b"diversity = 0.5 - concentration"),\n'
                                                    '        "math_oracle": '
                                                    '("tests/golden/phase3_math_cases.json", '
                                                    'b\'"v2_support":5\', b\'"v2_support":3\'),\n'
                                                    '        "hero": ("examples/hero/records_v2.csv", '
                                                    'b"v2_08,v2,", b"v2_99,v2,"),\n'
                                                    '        "dependency": ("pyproject.toml", b"numpy>=2.0", '
                                                    'b"numpy>=3.0"),\n'
                                                    '        "historical_assertion": '
                                                    '("tests/unit/test_phase4_contracts.py",\n'
                                                    "                                 b'    assert "
                                                    'control["active_phase"] == 4 and control["active_step"] '
                                                    "== 4\\n',\n"
                                                    '                                 b"    assert '
                                                    'True\\n"),\n'
                                                    '        "historical_tooling": '
                                                    '("scripts/release_check.py",\n'
                                                    '                               b"def '
                                                    'verify_phase4_step4_control(control: dict, step: int = '
                                                    '4) -> None:",\n'
                                                    '                               b"def '
                                                    'verify_phase4_step4_control(control: dict, step: int = '
                                                    '4) -> None:\\n    return"),\n'
                                                    '        "historical_binding": '
                                                    '("tests/integration/test_phase4_gates.py",\n'
                                                    '                               b"def '
                                                    'test_phase4_step4_current_workflows_preserve_matrix_and_use_active_dispatch(repo_root, '
                                                    'phase4_step4_snapshot):\\n    repo_root = '
                                                    'phase4_step4_snapshot\\n",\n'
                                                    '                               b"def '
                                                    'test_phase4_step4_current_workflows_preserve_matrix_and_use_active_dispatch(repo_root, '
                                                    'phase4_step4_snapshot):\\n"),\n'
                                                    '        "historical_document": ("docs/cli.md", b"# '
                                                    'CLI\\n",\n'
                                                    '                                b"# Unauthorized '
                                                    'historical document\\n"),\n'
                                                    '        "input_hash_helper": '
                                                    '("src/recursive_integrity_toolkit/utils/hashing.py",\n'
                                                    '                              b"return '
                                                    'hashlib.sha256(data).hexdigest()", b"return '
                                                    'hashlib.sha256(b\'changed\').hexdigest()"),\n'
                                                    '        "config_resolver_helper": '
                                                    '("src/recursive_integrity_toolkit/config.py",\n'
                                                    '                                   b"def '
                                                    'resolve_config(", b"def resolve_config_disabled("),\n'
                                                    '    }\n'
                                                    '    appended = {\n'
                                                    '        "frozen_model": '
                                                    '"src/recursive_integrity_toolkit/models.py",\n'
                                                    '        "frozen_schema": "schemas/report.schema.json",\n'
                                                    '        "plan": "PHASE_4_PLAN.md",\n'
                                                    '        "cli": '
                                                    '"src/recursive_integrity_toolkit/cli.py",\n'
                                                    '        "html": '
                                                    '"src/recursive_integrity_toolkit/reports/html_report.py",\n'
                                                    '        "assembly": '
                                                    '"src/recursive_integrity_toolkit/reports/assembly.py",\n'
                                                    '        "result": '
                                                    '"src/recursive_integrity_toolkit/result.py",\n'
                                                    '        "config": '
                                                    '"src/recursive_integrity_toolkit/config.py",\n'
                                                    '        "hashing": '
                                                    '"src/recursive_integrity_toolkit/utils/hashing.py",\n'
                                                    '        "logging": '
                                                    '"src/recursive_integrity_toolkit/utils/logging.py",\n'
                                                    '        "output_paths": '
                                                    '"src/recursive_integrity_toolkit/utils/paths.py",\n'
                                                    '    }\n'
                                                    '    added = {\n'
                                                    '        "unknown_runtime": '
                                                    '"src/recursive_integrity_toolkit/reports/unauthorized.py",\n'
                                                    '        "premature_completion": '
                                                    '"PHASE_4_COMPLETION.md", "premature_report": '
                                                    '"report.json",\n'
                                                    '    }\n'
                                                    '    if mutation in replacements:\n'
                                                    '        relative, original, replacement = '
                                                    'replacements[mutation]\n'
                                                    '        path = tmp_path / relative\n'
                                                    '        source = path.read_bytes()\n'
                                                    '        assert source.count(original) == 1\n'
                                                    '        path.write_bytes(source.replace(original, '
                                                    'replacement, 1))\n'
                                                    '    elif mutation in appended:\n'
                                                    '        path = tmp_path / appended[mutation]\n'
                                                    '        path.write_bytes(path.read_bytes() + '
                                                    'b"\\nUnauthorized Step 6 mutation\\n")\n'
                                                    '    elif mutation in added:\n'
                                                    '        path = tmp_path / added[mutation]\n'
                                                    '        assert not path.exists()\n'
                                                    '        path.write_text("Unauthorized later-stage '
                                                    'file\\n", encoding="utf-8")\n'
                                                    '    elif mutation == "missing_runtime":\n'
                                                    '        (tmp_path / '
                                                    '"src/recursive_integrity_toolkit/metrics/bounds.py").unlink()\n'
                                                    '    elif mutation.startswith("control_"):\n'
                                                    '        path = tmp_path / "PHASE_4_BASELINE.json"\n'
                                                    '        control = '
                                                    'json.loads(path.read_text(encoding="utf-8"))\n'
                                                    '        if mutation == "control_step":\n'
                                                    '            control["active_step"] = 7\n'
                                                    '        elif mutation == "control_scope":\n'
                                                    '            '
                                                    'control["runtime_paths_authorized"].append("src/recursive_integrity_toolkit/reports/assembly.py")\n'
                                                    '        else:\n'
                                                    '            control["schema_changes_authorized"] = '
                                                    'True\n'
                                                    '            '
                                                    'control["schema_paths_authorized"].append("schemas/report.schema.json")\n'
                                                    '        path.write_text(json.dumps(control), '
                                                    'encoding="utf-8")\n'
                                                    '    else:\n'
                                                    '        raise AssertionError(f"Unknown active mutation '
                                                    'case: {mutation}")\n'
                                                    '    with pytest.raises(ValueError):\n'
                                                    '        verify(tmp_path)',
                                             'node': 'test_phase4_step6_current_snapshot_checks_valid_tree_before_mutations',
                                             'old': 'def '
                                                    'test_phase4_step6_current_snapshot_checks_valid_tree_before_mutations(repo_root, '
                                                    'tmp_path, phase4_gate_tools, mutation):\n'
                                                    '    import json\n'
                                                    '\n'
                                                    '    tracked = subprocess.check_output(["git", "-C", '
                                                    'str(repo_root), "ls-files", "-z"])\n'
                                                    '    paths = set(tracked.decode().split("\\0")) - {""}\n'
                                                    '    assert len(paths) == 228\n'
                                                    '    for relative in sorted(paths):\n'
                                                    '        destination = tmp_path / relative\n'
                                                    '        destination.parent.mkdir(parents=True, '
                                                    'exist_ok=True)\n'
                                                    '        shutil.copyfile(repo_root / relative, '
                                                    'destination)\n'
                                                    '    verify = '
                                                    'phase4_gate_tools["verify_phase4_step6_snapshot"]\n'
                                                    '    baseline = verify(tmp_path)\n'
                                                    '    assert baseline["package_modules"] == 40\n'
                                                    '    assert baseline["frozen_runtime_modules"] == 38\n'
                                                    '    assert baseline["frozen_schemas"] == 5\n'
                                                    '    assert baseline["result_contracts_enabled"] is '
                                                    'True\n'
                                                    '    assert baseline["adapters_enabled"] is True\n'
                                                    '    assert baseline["privacy_views_enabled"] is True\n'
                                                    '    assert baseline["renderers_enabled"] is True\n'
                                                    '    assert baseline["output_publication_enabled"] is '
                                                    'True\n'
                                                    '    assert baseline["cli_analysis_enabled"] is False\n'
                                                    '    assert baseline["phase_complete"] is False\n'
                                                    '    if mutation == "unchanged":\n'
                                                    '        return\n'
                                                    '    replacements = {\n'
                                                    '        "formula": '
                                                    '("src/recursive_integrity_toolkit/metrics/diversity.py",\n'
                                                    '                    b"diversity = 1.0 - concentration", '
                                                    'b"diversity = 0.5 - concentration"),\n'
                                                    '        "math_oracle": '
                                                    '("tests/golden/phase3_math_cases.json", '
                                                    'b\'"v2_support":5\', b\'"v2_support":3\'),\n'
                                                    '        "hero": ("examples/hero/records_v2.csv", '
                                                    'b"v2_08,v2,", b"v2_99,v2,"),\n'
                                                    '        "dependency": ("pyproject.toml", b"numpy>=2.0", '
                                                    'b"numpy>=3.0"),\n'
                                                    '        "historical_assertion": '
                                                    '("tests/unit/test_phase4_contracts.py",\n'
                                                    "                                 b'    assert "
                                                    'control["active_phase"] == 4 and control["active_step"] '
                                                    "== 4\\n',\n"
                                                    '                                 b"    assert '
                                                    'True\\n"),\n'
                                                    '        "historical_tooling": '
                                                    '("scripts/release_check.py",\n'
                                                    '                               b"def '
                                                    'verify_phase4_step4_control(control: dict, step: int = '
                                                    '4) -> None:",\n'
                                                    '                               b"def '
                                                    'verify_phase4_step4_control(control: dict, step: int = '
                                                    '4) -> None:\\n    return"),\n'
                                                    '        "historical_binding": '
                                                    '("tests/integration/test_phase4_gates.py",\n'
                                                    '                               b"def '
                                                    'test_phase4_step4_current_workflows_preserve_matrix_and_use_active_dispatch(repo_root, '
                                                    'phase4_step4_snapshot):\\n    repo_root = '
                                                    'phase4_step4_snapshot\\n",\n'
                                                    '                               b"def '
                                                    'test_phase4_step4_current_workflows_preserve_matrix_and_use_active_dispatch(repo_root, '
                                                    'phase4_step4_snapshot):\\n"),\n'
                                                    '        "historical_document": ("docs/cli.md", b"# '
                                                    'CLI\\n",\n'
                                                    '                                b"# Unauthorized '
                                                    'historical document\\n"),\n'
                                                    '        "input_hash_helper": '
                                                    '("src/recursive_integrity_toolkit/utils/hashing.py",\n'
                                                    '                              b"return '
                                                    'hashlib.sha256(data).hexdigest()", b"return '
                                                    'hashlib.sha256(b\'changed\').hexdigest()"),\n'
                                                    '        "config_resolver_helper": '
                                                    '("src/recursive_integrity_toolkit/config.py",\n'
                                                    '                                   b"def '
                                                    'resolve_config(", b"def resolve_config_disabled("),\n'
                                                    '    }\n'
                                                    '    appended = {\n'
                                                    '        "frozen_model": '
                                                    '"src/recursive_integrity_toolkit/models.py",\n'
                                                    '        "frozen_schema": "schemas/report.schema.json",\n'
                                                    '        "plan": "PHASE_4_PLAN.md",\n'
                                                    '        "cli": '
                                                    '"src/recursive_integrity_toolkit/cli.py",\n'
                                                    '        "html": '
                                                    '"src/recursive_integrity_toolkit/reports/html_report.py",\n'
                                                    '        "assembly": '
                                                    '"src/recursive_integrity_toolkit/reports/assembly.py",\n'
                                                    '        "result": '
                                                    '"src/recursive_integrity_toolkit/result.py",\n'
                                                    '        "config": '
                                                    '"src/recursive_integrity_toolkit/config.py",\n'
                                                    '        "hashing": '
                                                    '"src/recursive_integrity_toolkit/utils/hashing.py",\n'
                                                    '        "logging": '
                                                    '"src/recursive_integrity_toolkit/utils/logging.py",\n'
                                                    '        "output_paths": '
                                                    '"src/recursive_integrity_toolkit/utils/paths.py",\n'
                                                    '    }\n'
                                                    '    added = {\n'
                                                    '        "unknown_runtime": '
                                                    '"src/recursive_integrity_toolkit/reports/unauthorized.py",\n'
                                                    '        "premature_completion": '
                                                    '"PHASE_4_COMPLETION.md", "premature_report": '
                                                    '"report.json",\n'
                                                    '    }\n'
                                                    '    if mutation in replacements:\n'
                                                    '        relative, original, replacement = '
                                                    'replacements[mutation]\n'
                                                    '        path = tmp_path / relative\n'
                                                    '        source = path.read_bytes()\n'
                                                    '        assert source.count(original) == 1\n'
                                                    '        path.write_bytes(source.replace(original, '
                                                    'replacement, 1))\n'
                                                    '    elif mutation in appended:\n'
                                                    '        path = tmp_path / appended[mutation]\n'
                                                    '        path.write_bytes(path.read_bytes() + '
                                                    'b"\\nUnauthorized Step 6 mutation\\n")\n'
                                                    '    elif mutation in added:\n'
                                                    '        path = tmp_path / added[mutation]\n'
                                                    '        assert not path.exists()\n'
                                                    '        path.write_text("Unauthorized later-stage '
                                                    'file\\n", encoding="utf-8")\n'
                                                    '    elif mutation == "missing_runtime":\n'
                                                    '        (tmp_path / '
                                                    '"src/recursive_integrity_toolkit/metrics/bounds.py").unlink()\n'
                                                    '    elif mutation.startswith("control_"):\n'
                                                    '        path = tmp_path / "PHASE_4_BASELINE.json"\n'
                                                    '        control = '
                                                    'json.loads(path.read_text(encoding="utf-8"))\n'
                                                    '        if mutation == "control_step":\n'
                                                    '            control["active_step"] = 7\n'
                                                    '        elif mutation == "control_scope":\n'
                                                    '            '
                                                    'control["runtime_paths_authorized"].append("src/recursive_integrity_toolkit/reports/assembly.py")\n'
                                                    '        else:\n'
                                                    '            control["schema_changes_authorized"] = '
                                                    'True\n'
                                                    '            '
                                                    'control["schema_paths_authorized"].append("schemas/report.schema.json")\n'
                                                    '        path.write_text(json.dumps(control), '
                                                    'encoding="utf-8")\n'
                                                    '    else:\n'
                                                    '        raise AssertionError(f"Unknown active mutation '
                                                    'case: {mutation}")\n'
                                                    '    with pytest.raises(ValueError):\n'
                                                    '        verify(tmp_path)'},
                                            {'new': 'def '
                                                    'test_phase4_step4_privacy_ast_checks_current_source_before_rejecting_scope_injection(repo_root, '
                                                    'tmp_path, relative, injection, phase4_step5_snapshot, '
                                                    'phase4_step6_snapshot):\n'
                                                    '    checker = runpy.run_path(str(repo_root / '
                                                    '"scripts/check_traceability.py"), '
                                                    'run_name="phase4_step4_ast_tests")\n'
                                                    '    verify = checker["phase4_step4_runtime_boundary"]\n'
                                                    '    repository_path = '
                                                    '"src/recursive_integrity_toolkit/" + relative\n'
                                                    '    current = (phase4_step5_snapshot if relative == '
                                                    '"utils/logging.py" else phase4_step6_snapshot if '
                                                    'relative == "config.py" else repo_root) / '
                                                    'repository_path\n'
                                                    '    verify(current, repository_path)\n'
                                                    '    copy = tmp_path / "source.py"\n'
                                                    '    copy.write_bytes(current.read_bytes() + injection)\n'
                                                    '    with pytest.raises(ValueError):\n'
                                                    '        verify(copy, repository_path)',
                                             'node': 'test_phase4_step4_privacy_ast_checks_current_source_before_rejecting_scope_injection',
                                             'old': 'def '
                                                    'test_phase4_step4_privacy_ast_checks_current_source_before_rejecting_scope_injection(repo_root, '
                                                    'tmp_path, relative, injection, phase4_step5_snapshot):\n'
                                                    '    checker = runpy.run_path(str(repo_root / '
                                                    '"scripts/check_traceability.py"), '
                                                    'run_name="phase4_step4_ast_tests")\n'
                                                    '    verify = checker["phase4_step4_runtime_boundary"]\n'
                                                    '    repository_path = '
                                                    '"src/recursive_integrity_toolkit/" + relative\n'
                                                    '    current = (phase4_step5_snapshot if relative == '
                                                    '"utils/logging.py" else repo_root) / repository_path\n'
                                                    '    verify(current, repository_path)\n'
                                                    '    copy = tmp_path / "source.py"\n'
                                                    '    copy.write_bytes(current.read_bytes() + injection)\n'
                                                    '    with pytest.raises(ValueError):\n'
                                                    '        verify(copy, repository_path)'},
                                            {'new': 'def '
                                                    'test_phase4_step1_keeps_current_help_and_future_commands_unopened(subprocess_env, '
                                                    'tmp_path, phase4_step6_snapshot):\n'
                                                    '    subprocess_env = dict(subprocess_env, '
                                                    'PYTHONPATH=str(phase4_step6_snapshot / "src"))\n'
                                                    '    before = set(tmp_path.iterdir())\n'
                                                    '    result = subprocess.run(\n'
                                                    '        [sys.executable, "-m", '
                                                    '"recursive_integrity_toolkit", "--help"],\n'
                                                    '        cwd=tmp_path, env=subprocess_env, text=True, '
                                                    'capture_output=True, check=False,\n'
                                                    '    )\n'
                                                    '    assert result.returncode == 0 and "version" in '
                                                    'result.stdout\n'
                                                    '    assert "Analytical audit functionality is not '
                                                    'implemented" in " ".join(result.stdout.split())\n'
                                                    '    rejected = subprocess.run(\n'
                                                    '        [sys.executable, "-m", '
                                                    '"recursive_integrity_toolkit", "audit"],\n'
                                                    '        cwd=tmp_path, env=subprocess_env, text=True, '
                                                    'capture_output=True, check=False,\n'
                                                    '    )\n'
                                                    '    assert rejected.returncode == 2\n'
                                                    '    assert set(tmp_path.iterdir()) == before',
                                             'node': 'test_phase4_step1_keeps_current_help_and_future_commands_unopened',
                                             'old': 'def '
                                                    'test_phase4_step1_keeps_current_help_and_future_commands_unopened(subprocess_env, '
                                                    'tmp_path):\n'
                                                    '    before = set(tmp_path.iterdir())\n'
                                                    '    result = subprocess.run(\n'
                                                    '        [sys.executable, "-m", '
                                                    '"recursive_integrity_toolkit", "--help"],\n'
                                                    '        cwd=tmp_path, env=subprocess_env, text=True, '
                                                    'capture_output=True, check=False,\n'
                                                    '    )\n'
                                                    '    assert result.returncode == 0 and "version" in '
                                                    'result.stdout\n'
                                                    '    assert "Analytical audit functionality is not '
                                                    'implemented" in " ".join(result.stdout.split())\n'
                                                    '    rejected = subprocess.run(\n'
                                                    '        [sys.executable, "-m", '
                                                    '"recursive_integrity_toolkit", "audit"],\n'
                                                    '        cwd=tmp_path, env=subprocess_env, text=True, '
                                                    'capture_output=True, check=False,\n'
                                                    '    )\n'
                                                    '    assert rejected.returncode == 2\n'
                                                    '    assert set(tmp_path.iterdir()) == before'}],
 'tests/unit/test_phase4_contracts.py': [{'new': 'def '
                                                 'test_phase4_step6_approved_control_keeps_independent_step5_anchors(phase4_tools, '
                                                 'phase4_step6_snapshot):\n'
                                                 '    control = json.loads((phase4_step6_snapshot / '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\n'
                                                 '    assert phase4_tools["PHASE4_STEP5_FINAL"] == '
                                                 '"c1667179e895a798bba2349960162542efa5ef87"\n'
                                                 '    assert phase4_tools["PHASE4_STEP5_TREE"] == '
                                                 '"d83f9fc8e0b569f2d796bd2a83b87422fe350fba"\n'
                                                 '    assert phase4_tools["PHASE4_STEP5_TEST_TREE"] == '
                                                 '"974f8e65904c24ed4e226996eaf571aab6123965"\n'
                                                 '    assert control["active_phase"] == 4 and '
                                                 'control["active_step"] == 6\n'
                                                 '    assert control["approval_basis"] == "批准开始Phase 4   '
                                                 '**Step 6**"\n'
                                                 '    assert control["baseline_commit"] == BASELINE\n'
                                                 '    assert control["previous_step_commit"] == '
                                                 '"c1667179e895a798bba2349960162542efa5ef87"\n'
                                                 '    assert control["previous_step_tree"] == '
                                                 '"d83f9fc8e0b569f2d796bd2a83b87422fe350fba"\n'
                                                 '    assert control["previous_step_test_tree"] == '
                                                 '"974f8e65904c24ed4e226996eaf571aab6123965"\n'
                                                 '    assert control["previous_step_core_tests"] == 3215\n'
                                                 '    assert control["previous_step_parquet_tests"] == 3218\n'
                                                 '    assert len(control["previous_step_files_sha256"]) == '
                                                 '227\n'
                                                 '    assert set(control["runtime_paths_authorized"]) == {\n'
                                                 '        "src/recursive_integrity_toolkit/utils/paths.py",\n'
                                                 '        '
                                                 '"src/recursive_integrity_toolkit/utils/logging.py",\n'
                                                 '    }\n'
                                                 '    assert control["schema_changes_authorized"] is False\n'
                                                 '    assert control["schema_paths_authorized"] == []\n'
                                                 '    assert control["new_files_permitted"] == '
                                                 '["tests/unit/test_phase4_output_safety.py"]\n'
                                                 '    for name in ("phase_complete", "next_step_authorized", '
                                                 '"main_merge_authorized", "publication_authorized"):\n'
                                                 '        assert control[name] is False\n'
                                                 '    phase4_tools["verify_phase4_step6_control"](control, '
                                                 'step=6)\n'
                                                 '    with pytest.raises(ValueError):\n'
                                                 '        '
                                                 'phase4_tools["verify_phase4_step4_control"](control, '
                                                 'step=4)',
                                          'node': 'test_phase4_step6_approved_control_keeps_independent_step5_anchors',
                                          'old': 'def '
                                                 'test_phase4_step6_approved_control_keeps_independent_step5_anchors(phase4_tools):\n'
                                                 '    control = json.loads((ROOT / '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\n'
                                                 '    assert phase4_tools["PHASE4_STEP5_FINAL"] == '
                                                 '"c1667179e895a798bba2349960162542efa5ef87"\n'
                                                 '    assert phase4_tools["PHASE4_STEP5_TREE"] == '
                                                 '"d83f9fc8e0b569f2d796bd2a83b87422fe350fba"\n'
                                                 '    assert phase4_tools["PHASE4_STEP5_TEST_TREE"] == '
                                                 '"974f8e65904c24ed4e226996eaf571aab6123965"\n'
                                                 '    assert control["active_phase"] == 4 and '
                                                 'control["active_step"] == 6\n'
                                                 '    assert control["approval_basis"] == "批准开始Phase 4   '
                                                 '**Step 6**"\n'
                                                 '    assert control["baseline_commit"] == BASELINE\n'
                                                 '    assert control["previous_step_commit"] == '
                                                 '"c1667179e895a798bba2349960162542efa5ef87"\n'
                                                 '    assert control["previous_step_tree"] == '
                                                 '"d83f9fc8e0b569f2d796bd2a83b87422fe350fba"\n'
                                                 '    assert control["previous_step_test_tree"] == '
                                                 '"974f8e65904c24ed4e226996eaf571aab6123965"\n'
                                                 '    assert control["previous_step_core_tests"] == 3215\n'
                                                 '    assert control["previous_step_parquet_tests"] == 3218\n'
                                                 '    assert len(control["previous_step_files_sha256"]) == '
                                                 '227\n'
                                                 '    assert set(control["runtime_paths_authorized"]) == {\n'
                                                 '        "src/recursive_integrity_toolkit/utils/paths.py",\n'
                                                 '        '
                                                 '"src/recursive_integrity_toolkit/utils/logging.py",\n'
                                                 '    }\n'
                                                 '    assert control["schema_changes_authorized"] is False\n'
                                                 '    assert control["schema_paths_authorized"] == []\n'
                                                 '    assert control["new_files_permitted"] == '
                                                 '["tests/unit/test_phase4_output_safety.py"]\n'
                                                 '    for name in ("phase_complete", "next_step_authorized", '
                                                 '"main_merge_authorized", "publication_authorized"):\n'
                                                 '        assert control[name] is False\n'
                                                 '    phase4_tools["verify_phase4_step6_control"](control, '
                                                 'step=6)\n'
                                                 '    with pytest.raises(ValueError):\n'
                                                 '        '
                                                 'phase4_tools["verify_phase4_step4_control"](control, '
                                                 'step=4)'},
                                         {'new': 'def '
                                                 'test_phase4_step6_control_rejects_forged_scope_and_stage(phase4_tools, '
                                                 'field, value, phase4_step6_snapshot):\n'
                                                 '    control = json.loads((phase4_step6_snapshot / '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\n'
                                                 '    verify = phase4_tools["verify_phase4_step6_control"]\n'
                                                 '    verify(control, step=6)\n'
                                                 '    control[field] = value\n'
                                                 '    with pytest.raises(ValueError):\n'
                                                 '        verify(control, step=6)',
                                          'node': 'test_phase4_step6_control_rejects_forged_scope_and_stage',
                                          'old': 'def '
                                                 'test_phase4_step6_control_rejects_forged_scope_and_stage(phase4_tools, '
                                                 'field, value):\n'
                                                 '    control = json.loads((ROOT / '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\n'
                                                 '    verify = phase4_tools["verify_phase4_step6_control"]\n'
                                                 '    verify(control, step=6)\n'
                                                 '    control[field] = value\n'
                                                 '    with pytest.raises(ValueError):\n'
                                                 '        verify(control, step=6)'},
                                         {'new': 'def '
                                                 'test_phase4_step6_control_rejects_unapproved_dispatch(phase4_tools, '
                                                 'step, phase4_step6_snapshot):\n'
                                                 '    control = json.loads((phase4_step6_snapshot / '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\n'
                                                 '    phase4_tools["verify_phase4_step6_control"](control, '
                                                 'step=6)\n'
                                                 '    with pytest.raises(ValueError):\n'
                                                 '        '
                                                 'phase4_tools["verify_phase4_step6_control"](control, '
                                                 'step=step)',
                                          'node': 'test_phase4_step6_control_rejects_unapproved_dispatch',
                                          'old': 'def '
                                                 'test_phase4_step6_control_rejects_unapproved_dispatch(phase4_tools, '
                                                 'step):\n'
                                                 '    control = json.loads((ROOT / '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\n'
                                                 '    phase4_tools["verify_phase4_step6_control"](control, '
                                                 'step=6)\n'
                                                 '    with pytest.raises(ValueError):\n'
                                                 '        '
                                                 'phase4_tools["verify_phase4_step6_control"](control, '
                                                 'step=step)'},
                                         {'new': 'def '
                                                 'test_phase4_step6_control_requires_explicit_approval_fields(phase4_tools, '
                                                 'field, phase4_step6_snapshot):\n'
                                                 '    control = json.loads((phase4_step6_snapshot / '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\n'
                                                 '    phase4_tools["verify_phase4_step6_control"](control)\n'
                                                 '    del control[field]\n'
                                                 '    with pytest.raises(ValueError):\n'
                                                 '        '
                                                 'phase4_tools["verify_phase4_step6_control"](control)',
                                          'node': 'test_phase4_step6_control_requires_explicit_approval_fields',
                                          'old': 'def '
                                                 'test_phase4_step6_control_requires_explicit_approval_fields(phase4_tools, '
                                                 'field):\n'
                                                 '    control = json.loads((ROOT / '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\n'
                                                 '    phase4_tools["verify_phase4_step6_control"](control)\n'
                                                 '    del control[field]\n'
                                                 '    with pytest.raises(ValueError):\n'
                                                 '        '
                                                 'phase4_tools["verify_phase4_step6_control"](control)'},
                                         {'new': 'def '
                                                 'test_phase4_step6_control_cannot_mint_extra_permission(phase4_tools, '
                                                 'phase4_step6_snapshot):\n'
                                                 '    control = json.loads((phase4_step6_snapshot / '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\n'
                                                 '    phase4_tools["verify_phase4_step6_control"](control)\n'
                                                 '    control["approved_scope_expansion"] = {"step": 6, '
                                                 '"publication": True}\n'
                                                 '    with pytest.raises(ValueError):\n'
                                                 '        '
                                                 'phase4_tools["verify_phase4_step6_control"](control)',
                                          'node': 'test_phase4_step6_control_cannot_mint_extra_permission',
                                          'old': 'def '
                                                 'test_phase4_step6_control_cannot_mint_extra_permission(phase4_tools):\n'
                                                 '    control = json.loads((ROOT / '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\n'
                                                 '    phase4_tools["verify_phase4_step6_control"](control)\n'
                                                 '    control["approved_scope_expansion"] = {"step": 6, '
                                                 '"publication": True}\n'
                                                 '    with pytest.raises(ValueError):\n'
                                                 '        '
                                                 'phase4_tools["verify_phase4_step6_control"](control)'},
                                         {'new': 'def '
                                                 'test_phase4_step6_historical_bindings_preserve_assertions_and_headers(phase4_tools, '
                                                 'phase4_step5_snapshot, phase4_step6_snapshot):\n'
                                                 '    import ast\n'
                                                 '\n'
                                                 '    registry = phase4_tools["PHASE4_STEP6_MIGRATIONS"]\n'
                                                 '    assert set(registry) == '
                                                 '{"tests/unit/test_phase4_contracts.py", '
                                                 '"tests/integration/test_phase4_gates.py"}\n'
                                                 '    assert sorted(len(rows) for rows in registry.values()) '
                                                 '== [7, 8]\n'
                                                 '    expected_inventory = {"phase4_mutation_tree"} | {\n'
                                                 '        "test_phase4_step" + str(step) + '
                                                 '"_current_snapshot_checks_valid_tree_before_mutations"\n'
                                                 '        for step in (2, 3, 4, 5)\n'
                                                 '    }\n'
                                                 '    inventory_seen = set()\n'
                                                 '    for path, rows in registry.items():\n'
                                                 '        '
                                                 'phase4_tools["verify_phase4_step6_test_migration"](\n'
                                                 '            path, (phase4_step5_snapshot / '
                                                 'path).read_bytes(), (phase4_step6_snapshot / '
                                                 'path).read_bytes())\n'
                                                 '        for row in rows:\n'
                                                 '            trees = [ast.parse(row[key]) for key in '
                                                 '("old", "new")]\n'
                                                 '            assertions = [[ast.dump(n) for n in '
                                                 'ast.walk(tree) if isinstance(n, ast.Assert)] for tree in '
                                                 'trees]\n'
                                                 '            assert assertions[0] == assertions[1]\n'
                                                 '            assert trees[0].body[0].name == '
                                                 'trees[1].body[0].name == row["node"]\n'
                                                 '            if row["node"] in expected_inventory:\n'
                                                 '                inventory_seen.add(row["node"])\n'
                                                 '                assert \'"ls-files"\' in row["old"] and '
                                                 '\'rglob("*")\' in row["new"]\n'
                                                 '    assert inventory_seen == expected_inventory',
                                          'node': 'test_phase4_step6_historical_bindings_preserve_assertions_and_headers',
                                          'old': 'def '
                                                 'test_phase4_step6_historical_bindings_preserve_assertions_and_headers(phase4_tools, '
                                                 'phase4_step5_snapshot):\n'
                                                 '    import ast\n'
                                                 '\n'
                                                 '    registry = phase4_tools["PHASE4_STEP6_MIGRATIONS"]\n'
                                                 '    assert set(registry) == '
                                                 '{"tests/unit/test_phase4_contracts.py", '
                                                 '"tests/integration/test_phase4_gates.py"}\n'
                                                 '    assert sorted(len(rows) for rows in registry.values()) '
                                                 '== [7, 8]\n'
                                                 '    expected_inventory = {"phase4_mutation_tree"} | {\n'
                                                 '        "test_phase4_step" + str(step) + '
                                                 '"_current_snapshot_checks_valid_tree_before_mutations"\n'
                                                 '        for step in (2, 3, 4, 5)\n'
                                                 '    }\n'
                                                 '    inventory_seen = set()\n'
                                                 '    for path, rows in registry.items():\n'
                                                 '        '
                                                 'phase4_tools["verify_phase4_step6_test_migration"](\n'
                                                 '            path, (phase4_step5_snapshot / '
                                                 'path).read_bytes(), (ROOT / path).read_bytes())\n'
                                                 '        for row in rows:\n'
                                                 '            trees = [ast.parse(row[key]) for key in '
                                                 '("old", "new")]\n'
                                                 '            assertions = [[ast.dump(n) for n in '
                                                 'ast.walk(tree) if isinstance(n, ast.Assert)] for tree in '
                                                 'trees]\n'
                                                 '            assert assertions[0] == assertions[1]\n'
                                                 '            assert trees[0].body[0].name == '
                                                 'trees[1].body[0].name == row["node"]\n'
                                                 '            if row["node"] in expected_inventory:\n'
                                                 '                inventory_seen.add(row["node"])\n'
                                                 '                assert \'"ls-files"\' in row["old"] and '
                                                 '\'rglob("*")\' in row["new"]\n'
                                                 '    assert inventory_seen == expected_inventory'},
                                         {'new': 'def '
                                                 'test_phase4_step6_historical_guard_rejects_weakening(phase4_tools, '
                                                 'phase4_step5_snapshot, mutation, phase4_step6_snapshot):\n'
                                                 '    path = "tests/integration/test_phase4_gates.py" if '
                                                 'mutation in ("inventory", "logging") else '
                                                 '"tests/unit/test_phase4_contracts.py"\n'
                                                 '    before = (phase4_step5_snapshot / path).read_bytes()\n'
                                                 '    after = (phase4_step6_snapshot / path).read_bytes()\n'
                                                 '    verify = '
                                                 'phase4_tools["verify_phase4_step6_test_migration"]\n'
                                                 '    verify(path, before, after)\n'
                                                 '    if mutation == "assertion":\n'
                                                 '        needle = b\'    assert control["active_phase"] == '
                                                 '4 and control["active_step"] == 5\\n\'\n'
                                                 '        assert after.count(needle) == 1\n'
                                                 '        after = after.replace(needle, b"    assert '
                                                 'True\\n", 1)\n'
                                                 '    elif mutation == "binding":\n'
                                                 "        needle = b'json.loads((phase4_step5_snapshot / "
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\'\n'
                                                 '        assert needle in after\n'
                                                 '        after = after.replace(needle, '
                                                 'needle.replace(b"phase4_step5_snapshot", b"ROOT"), 1)\n'
                                                 '    elif mutation == "inventory":\n'
                                                 "        needle = b'for path in "
                                                 'phase4_step1_snapshot.rglob("*") if path.is_file()\'\n'
                                                 '        assert after.count(needle) == 1\n'
                                                 '        after = after.replace(needle, '
                                                 'needle.replace(b"phase4_step1_snapshot", b"repo_root"), '
                                                 '1)\n'
                                                 '    elif mutation == "logging":\n'
                                                 "        needle = b'(phase4_step5_snapshot if relative == "
                                                 '"utils/logging.py" else repo_root)\'\n'
                                                 '        assert after.count(needle) == 1\n'
                                                 '        after = after.replace(needle, b"repo_root", 1)\n'
                                                 '    elif mutation == "shadow":\n'
                                                 '        after += b"\\ndef '
                                                 'test_phase4_step5_fixed_boundary_opens_only_approved_existing_paths():\\n    '
                                                 'assert True\\n"\n'
                                                 '    else:\n'
                                                 '        after += b"\\ndef '
                                                 'test_phase4_step6_bad(value=globals().clear()):\\n    '
                                                 'pass\\n"\n'
                                                 '    with pytest.raises(ValueError):\n'
                                                 '        verify(path, before, after)',
                                          'node': 'test_phase4_step6_historical_guard_rejects_weakening',
                                          'old': 'def '
                                                 'test_phase4_step6_historical_guard_rejects_weakening(phase4_tools, '
                                                 'phase4_step5_snapshot, mutation):\n'
                                                 '    path = "tests/integration/test_phase4_gates.py" if '
                                                 'mutation in ("inventory", "logging") else '
                                                 '"tests/unit/test_phase4_contracts.py"\n'
                                                 '    before = (phase4_step5_snapshot / path).read_bytes()\n'
                                                 '    after = (ROOT / path).read_bytes()\n'
                                                 '    verify = '
                                                 'phase4_tools["verify_phase4_step6_test_migration"]\n'
                                                 '    verify(path, before, after)\n'
                                                 '    if mutation == "assertion":\n'
                                                 '        needle = b\'    assert control["active_phase"] == '
                                                 '4 and control["active_step"] == 5\\n\'\n'
                                                 '        assert after.count(needle) == 1\n'
                                                 '        after = after.replace(needle, b"    assert '
                                                 'True\\n", 1)\n'
                                                 '    elif mutation == "binding":\n'
                                                 "        needle = b'json.loads((phase4_step5_snapshot / "
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\'\n'
                                                 '        assert needle in after\n'
                                                 '        after = after.replace(needle, '
                                                 'needle.replace(b"phase4_step5_snapshot", b"ROOT"), 1)\n'
                                                 '    elif mutation == "inventory":\n'
                                                 "        needle = b'for path in "
                                                 'phase4_step1_snapshot.rglob("*") if path.is_file()\'\n'
                                                 '        assert after.count(needle) == 1\n'
                                                 '        after = after.replace(needle, '
                                                 'needle.replace(b"phase4_step1_snapshot", b"repo_root"), '
                                                 '1)\n'
                                                 '    elif mutation == "logging":\n'
                                                 "        needle = b'(phase4_step5_snapshot if relative == "
                                                 '"utils/logging.py" else repo_root)\'\n'
                                                 '        assert after.count(needle) == 1\n'
                                                 '        after = after.replace(needle, b"repo_root", 1)\n'
                                                 '    elif mutation == "shadow":\n'
                                                 '        after += b"\\ndef '
                                                 'test_phase4_step5_fixed_boundary_opens_only_approved_existing_paths():\\n    '
                                                 'assert True\\n"\n'
                                                 '    else:\n'
                                                 '        after += b"\\ndef '
                                                 'test_phase4_step6_bad(value=globals().clear()):\\n    '
                                                 'pass\\n"\n'
                                                 '    with pytest.raises(ValueError):\n'
                                                 '        verify(path, before, after)'}]}


def _phase4_step6_files():
    """Read the exact accepted Step 6 Git tree and verify every blob identity."""
    for suffix, expected in (("^{commit}", PHASE4_STEP6_FINAL), ("^{tree}", PHASE4_STEP6_TREE),
                             (":tests", PHASE4_STEP6_TEST_TREE)):
        if git("rev-parse", PHASE4_STEP6_FINAL + suffix).decode().strip() != expected:
            raise ValueError("Pinned Phase 4 Step 6 identity mismatch")
    objects = {}
    for entry in git("ls-tree", "-rz", PHASE4_STEP6_FINAL).split(b"\0"):
        if not entry:
            continue
        metadata, raw_path = entry.split(b"\t", 1)
        mode, kind, oid = metadata.split()
        path = raw_path.decode("utf-8")
        if (mode not in (b"100644", b"100755") or kind != b"blob" or path in objects
                or path.startswith("/") or ".." in path.split("/") or ".git" in path.split("/")):
            raise ValueError("Unsafe pinned Step 6 Git object")
        objects[path] = oid.decode("ascii")
    if len(objects) != 228:
        raise ValueError("Pinned Step 6 must contain exactly 228 files")
    files = {}
    with zipfile.ZipFile(io.BytesIO(git("archive", "--format=zip", PHASE4_STEP6_FINAL))) as archive:
        names = [item.filename for item in archive.infolist() if not item.is_dir()]
        if len(names) != len(objects) or set(names) != set(objects):
            raise ValueError("Pinned Step 6 archive identity mismatch")
        for name in names:
            raw = archive.read(name)
            oid = hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()
            if oid != objects[name]:
                raise ValueError(f"Pinned Step 6 blob mismatch: {name}")
            files[name] = raw
    return MappingProxyType(files)


def phase4_step7_expected_control() -> dict:
    """Actual Step 7 approval is independent of the mutable control document."""
    prior = _phase4_step6_files()
    result = phase4_step6_expected_control()
    result.update({
        "control_version": "1.6", "active_step": 7,
        "approval_date": PHASE4_STEP7_APPROVAL_DATE, "approval_basis": PHASE4_STEP7_APPROVAL,
        "previous_step_commit": PHASE4_STEP6_FINAL,
        "previous_step_tree": PHASE4_STEP6_TREE,
        "previous_step_test_tree": PHASE4_STEP6_TEST_TREE,
        "previous_step_core_tests": 3420, "previous_step_parquet_tests": 3423,
        "previous_step_files_sha256": {p: hashlib.sha256(raw).hexdigest() for p, raw in sorted(prior.items())},
        "permitted_paths": sorted(PHASE4_STEP7_ALLOWED), "new_files_permitted": list(PHASE4_STEP7_NEW),
        "runtime_changes_authorized": True, "schema_changes_authorized": False,
        "runtime_paths_authorized": sorted(p for p in PHASE4_STEP7_ALLOWED if p.startswith("src/")),
        "schema_paths_authorized": [],
        "step6_historical_binding_nodes": {p: sorted({r["node"] for r in rows})
                                          for p, rows in sorted(PHASE4_STEP7_MIGRATIONS.items())},
    })
    return result


def verify_phase4_step7_control(control: dict, step: int = 7) -> None:
    if type(step) is not int or step != 7 or type(control) is not dict:
        raise ValueError("Unsupported Phase 4 Step 7 stage/control")
    try:
        actual = json.dumps(control, sort_keys=True, ensure_ascii=True, allow_nan=False)
        expected = json.dumps(phase4_step7_expected_control(), sort_keys=True, ensure_ascii=True, allow_nan=False)
    except (TypeError, ValueError) as error:
        raise ValueError("Invalid Phase 4 Step 7 control") from error
    if actual != expected:
        raise ValueError("Phase 4 control differs from the independently approved Step 7 contract")


def verify_phase4_step7_changes(changes: list[tuple[str, str]]) -> None:
    seen = set()
    for status, path in changes:
        if path in seen or path not in PHASE4_STEP7_ALLOWED or status != ("A" if path in PHASE4_STEP7_NEW else "M"):
            raise ValueError(f"Unapproved Phase 4 Step 7 path/operation: {status} {path}")
        seen.add(path)


def _phase4_step7_header(node, path):
    """Allow explicit test parametrization/fixtures, never definition-time effects."""
    for decorator in node.decorator_list:
        if not isinstance(decorator, ast.Call) or ast.unparse(decorator.func) not in {
                "pytest.fixture", "pytest.mark.parametrize"}:
            raise ValueError(f"Unapproved Step 7 test decorator: {path}:{node.name}")
        if ast.unparse(decorator.func) == "pytest.fixture" and not node.name.startswith("phase4_step"):
            raise ValueError("A Step 7 fixture must have an explicit scoped name")
        if any(keyword.arg is None for keyword in decorator.keywords):
            raise ValueError("Decorator expansion is outside the Step 7 contract")
        for value in [*decorator.args, *(keyword.value for keyword in decorator.keywords)]:
            try:
                ast.literal_eval(value)
            except (ValueError, TypeError, SyntaxError) as error:
                raise ValueError("Step 7 decorator arguments must be literal") from error
    clone = ast.parse(ast.unparse(node)).body[0]
    clone.decorator_list = []
    _phase4_preserve_function_header(clone, path)


def _phase4_step7_append_only(before: bytes, after: bytes, path: str) -> None:
    if not after.startswith(before):
        raise ValueError(f"Inherited Step 6 prefix changed: {path}")
    old, new = ast.parse(before), ast.parse(after)
    bindings = set()
    for node in old.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            bindings.add(node.name)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            bindings.update(alias.asname or alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            bindings.update(child.id for target in targets for child in ast.walk(target) if isinstance(child, ast.Name))
    for node in new.body[len(old.body):]:
        if not isinstance(node, ast.FunctionDef) or node.name in bindings:
            raise ValueError(f"Step 7 addition executes, rebinds or shadows inherited source: {path}")
        allowed_snapshot = path == "tests/conftest.py" and node.name == "phase4_step6_snapshot"
        if not allowed_snapshot and not node.name.startswith(("test_phase4_step7_", "phase4_step7_")):
            raise ValueError(f"Step 7 added test/helper is not explicitly scoped: {path}:{node.name}")
        if path == "tests/conftest.py" and node.name != "phase4_step6_snapshot":
            raise ValueError("Only the pinned Step 6 shared fixture is authorized")
        bindings.add(node.name)
        _phase4_step7_header(node, path)


def verify_phase4_step7_test_migration(path: str, before: bytes, after: bytes) -> None:
    prior = _phase4_step6_files()
    if path not in prior or path not in PHASE4_STEP7_ALLOWED or before != prior[path] or not path.startswith("tests/"):
        raise ValueError("Step 7 migration requires the exact named Step 6 source")
    _phase4_step7_check_test_migration(path, before, after)


def _phase4_step7_check_test_migration(path: str, before: bytes, after: bytes) -> None:
    """Check a source already read from the verified Step 6 immutable mapping."""
    expected = before
    for row in PHASE4_STEP7_MIGRATIONS.get(path, []):
        old, new = row["old"].encode(), row["new"].encode()
        if expected.count(old) != 1:
            raise ValueError("Step 6 historical binding is not unique")
        expected = expected.replace(old, new, 1)
    _phase4_step7_append_only(expected, after, path)


def _phase4_step7_preserve_tooling(before: bytes, after: bytes, path: str) -> None:
    """Preserve exact inherited statements using one source-line split per tree."""
    if path == "scripts/release_check.py":
        old = '    return phase4_cli_main() if explicit_phase4 else main()'
        new = ('    explicit_step7 = "--step=7" in argv or any(a == "--step" and b == "7" for a, b in zip(argv, argv[1:]))\n'
               '    if explicit_phase4 and explicit_step7:\n'
               '        return phase4_step7_cli_main()\n' + old)
        # Earlier preserved dispatch functions contain this source too; bind cli_main only.
        parsed = ast.parse(before)
        entry = next(node for node in parsed.body if isinstance(node, ast.FunctionDef) and node.name == "cli_main")
        old_entry = ast.get_source_segment(before.decode(), entry)
        if old_entry.count(old) != 1:
            raise ValueError("Step 6 release dispatcher identity mismatch")
        replacements = [(old_entry, old_entry.replace(old, new, 1))]
    else:
        old = '    if args.phase == 4 and args.step == 6:\n        return phase4_step6_main(step=args.step)\n'
        new = old + '    if args.phase == 4 and args.step == 7:\n        return phase4_step7_main(step=args.step)\n'
        replacements = [(old, new),
                        ('Choose explicit --phase 3 --step 11 or --phase 4 --step 1 or --phase 4 --step 2 or --phase 4 --step 3 or --phase 4 --step 4 or --phase 4 --step 5 or --phase 4 --step 6',
                         'Choose explicit --phase 3 --step 11 or --phase 4 --step 1 or --phase 4 --step 2 or --phase 4 --step 3 or --phase 4 --step 4 or --phase 4 --step 5 or --phase 4 --step 6 or --phase 4 --step 7')]
    expected = before
    for old, new in replacements:
        if expected.count(old.encode()) != 1:
            raise ValueError(f"Historical dispatcher identity mismatch: {path}")
        expected = expected.replace(old.encode(), new.encode(), 1)
    trees = [ast.parse(expected), ast.parse(after)]
    lines = [expected.splitlines(keepends=True), after.splitlines(keepends=True)]
    def segment(index, node):
        if node.lineno == node.end_lineno:
            return lines[index][node.lineno - 1][node.col_offset:node.end_col_offset]
        return (lines[index][node.lineno - 1][node.col_offset:]
                + b"".join(lines[index][node.lineno:node.end_lineno - 1])
                + lines[index][node.end_lineno - 1][:node.end_col_offset])
    def entry_guard(node):
        return isinstance(node, ast.If) and isinstance(node.test, ast.Compare) and "__name__" in ast.unparse(node.test)
    guards = [n for n in trees[1].body if entry_guard(n)]
    expected_guard = ast.parse('if __name__ == "__main__":\n    raise SystemExit(cli_main())').body[0]
    if len(guards) != 1 or ast.dump(guards[0]) != ast.dump(expected_guard):
        raise ValueError(f"Unapproved Step 7 maintainer entrypoint: {path}")
    historical = [n for n in trees[0].body if not entry_guard(n)]
    current = [n for n in trees[1].body if not entry_guard(n)]
    old_entries = [(segment(0, n), ast.dump(n)) for n in historical]
    cursor = 0
    for node in current:
        if cursor < len(old_entries) and (segment(1, node), ast.dump(node)) == old_entries[cursor]:
            cursor += 1
            continue
        if isinstance(node, ast.FunctionDef) and (node.name == "_phase4_step6_files" or node.name.startswith(
                ("phase4_step7_", "_phase4_step7_", "verify_phase4_step7_", "audit_phase4_step7"))):
            _phase4_preserve_function_header(node, path)
            continue
        if isinstance(node, ast.Assign) and all(isinstance(target, ast.Name) and target.id.startswith(
                ("PHASE4_STEP7_", "PHASE4_STEP6_")) for target in node.targets):
            try:
                ast.literal_eval(node.value)
            except (ValueError, TypeError, SyntaxError) as error:
                raise ValueError(f"Nonliteral added Step 7 maintainer constant: {path}") from error
            continue
        raise ValueError(f"Unapproved Step 7 maintainer addition: {path}")
    if cursor != len(historical):
        raise ValueError(f"Inherited Step 6 maintainer statement changed: {path}")
    def binding_counts(tree):
        counts = {}
        for node in tree.body:
            names = []
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                names = [node.name]
            elif isinstance(node, (ast.Assign, ast.AnnAssign)):
                targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                names = [child.id for target in targets for child in ast.walk(target) if isinstance(child, ast.Name)]
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                names = [alias.asname or alias.name.split(".")[0] for alias in node.names]
            for name in names:
                counts[name] = counts.get(name, 0) + 1
        return counts
    inherited_counts = binding_counts(trees[0])
    for name, count in binding_counts(trees[1]).items():
        if count > inherited_counts.get(name, 1):
            raise ValueError(f"Duplicate Step 7 maintainer binding: {path}:{name}")


def verify_phase4_step7_snapshot(root: Path = ROOT) -> dict:
    prior = _phase4_step6_files()
    for path, raw in prior.items():
        target = root / path
        if not target.is_file() or target.is_symlink():
            raise ValueError(f"Missing or aliased inherited Step 6 file: {path}")
        current = target.read_bytes()
        if path not in PHASE4_STEP7_ALLOWED and current != raw:
            raise ValueError(f"Protected Step 6 bytes changed: {path}")
        if path.startswith("tests/") and path in PHASE4_STEP7_ALLOWED:
            _phase4_step7_check_test_migration(path, raw, current)
        elif path.startswith("scripts/") and path in PHASE4_STEP7_ALLOWED:
            _phase4_step7_preserve_tooling(raw, current, path)
        elif path in {"docs/architecture.md", "docs/theory_traceability.md", "PHASE_4_DECISIONS.md"}:
            if not current.startswith(raw):
                raise ValueError(f"Step 6 historical documentation prefix changed: {path}")
    if not (root / "docs/cli.md").read_bytes().endswith(prior["docs/cli.md"]):
        raise ValueError("Step 7 CLI documentation must retain the historical notes verbatim")
    for path in PHASE4_STEP7_NEW:
        target = root / path
        if not target.is_file() or target.is_symlink():
            raise ValueError("Missing Step 7 output safety tests")
        _phase4_step7_new_test(target.read_bytes(), path)
    for path in ("src/recursive_integrity_toolkit/config.py",):
        _phase4_step7_preserve_runtime(prior[path], (root / path).read_bytes(), path)
    actual_modules = {p.relative_to(root).as_posix() for p in (root / "src/recursive_integrity_toolkit").rglob("*.py")}
    expected_modules = {p for p in prior if p.startswith("src/") and p.endswith(".py")}
    if actual_modules != expected_modules or len(actual_modules) != 40:
        raise ValueError("Step 7 cannot change the runtime module set")
    if {p.name for p in (root / "schemas").iterdir()} != {Path(p).name for p in prior if p.startswith("schemas/")}:
        raise ValueError("Step 7 cannot change the schema set")
    if hashlib.sha256((root / "PHASE_4_PLAN.md").read_bytes()).hexdigest() != PHASE4_PLAN_SHA256:
        raise ValueError("Approved Phase 4 plan changed")
    verify_phase4_step7_control(json.loads((root / "PHASE_4_BASELINE.json").read_text(encoding="utf-8")))
    decisions = (root / "PHASE_4_DECISIONS.md").read_text(encoding="utf-8")
    if PHASE4_STEP7_APPROVAL not in decisions or PHASE4_STEP6_FINAL not in decisions:
        raise ValueError("Actual Step 7 authorization or Step 6 evidence anchor missing")
    if any((root / name).exists() for name in PHASE4_FORBIDDEN_OUTPUTS):
        raise ValueError("Step 7 cannot create Phase 4 completion records or audit outputs")
    import runpy
    checker = runpy.run_path(str(root / "scripts/check_traceability.py"), run_name="phase4_step7_renderer_boundary")
    checker["phase4_step7_cli_boundary"](root)
    schema_bytes = (root / "schemas/report.schema.json").read_bytes()
    if hashlib.sha256(schema_bytes).hexdigest() != PHASE4_STEP2_REPORT_SCHEMA_SHA256:
        raise ValueError("Step 7 report schema differs from its independently reviewed bytes")
    schema = json.loads(schema_bytes)
    if (schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema"
            or schema.get("type") != "object" or schema.get("additionalProperties") is not False):
        raise ValueError("Step 7 report schema dialect/closed root mismatch")
    return {"package_modules": 40, "frozen_runtime_modules": 38, "frozen_schemas": 5,
            "hero_files_unchanged": 6, "historical_phase3_migrated_nodes": 16,
            "phase_complete": False, "result_contracts_enabled": True,
            "adapters_enabled": True, "privacy_views_enabled": True, "renderers_enabled": True, "output_publication_enabled": True, "cli_analysis_enabled": True, "comparison_enabled": False, "example_enabled": False}


def audit_phase4_step7(step: int = 7) -> dict:
    verify_phase4_step7_control(json.loads((ROOT / "PHASE_4_BASELINE.json").read_text(encoding="utf-8")), step)
    result = {"phase": 4, "active_step": step, **verify_phase4_step7_snapshot(),
              "phase0_hashes_verified": 16, "publication_authorized": False}
    print(json.dumps(result, indent=2))
    return result


def audit_phase4_step7_diff(step: int = 7) -> dict:
    if type(step) is not int or step != 7:
        raise ValueError("Unsupported Phase 4 Step 7 stage")
    _phase4_step6_files()
    subprocess.run(["git", "-C", str(ROOT), "merge-base", "--is-ancestor", PHASE4_STEP6_FINAL, "HEAD"], check=True)
    raw = git("diff", "--name-status", "--no-renames", "-z", PHASE4_STEP6_FINAL, "--").split(b"\0")
    raw = [part.decode("utf-8") for part in raw if part]
    if len(raw) % 2:
        raise ValueError("Malformed Step 7 Git difference records")
    changes = list(zip(raw[::2], raw[1::2]))
    changes.extend(("A", p.decode()) for p in git("ls-files", "--others", "--exclude-standard", "-z").split(b"\0") if p)
    verify_phase4_step7_changes(changes)
    result = {"previous_step_commit": PHASE4_STEP6_FINAL, "changed_files": len(changes),
              "changes": changes, "step": 7, "scope": "PASS"}
    print(json.dumps(result, indent=2))
    return result


def phase4_step7_baseline_evidence(output: Path) -> dict:
    """Reconcile all inherited identities, including the accepted Step 6 suite."""
    output.mkdir(parents=True, exist_ok=True)
    inherited = phase4_step6_baseline_evidence(output / "phase4-step6-inherited")
    with tempfile.TemporaryDirectory(prefix="rit-p4-step6-identities-") as temp:
        baseline = Path(temp)
        for name, raw in _phase4_step6_files().items():
            target = baseline / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(raw)
        old, old_log = _collect(baseline)
    current, current_log = _collect(ROOT)
    expected = 3423 if os.environ.get("RIT_TEST_PARQUET") == "1" else 3420
    if len(old) != expected or set(old) - set(current):
        raise ValueError("Accepted Phase 4 Step 6 test identities were lost")
    result = {"baseline_commit": PHASE4_STEP6_FINAL, "baseline_test_tree": PHASE4_STEP6_TEST_TREE,
              "baseline_nodeids": old, "current_nodeids": current, "missing_nodeids": [],
              "baseline_tests": len(old), "current_tests": len(current), "inherited": inherited,
              "nodeids_sha256": hashlib.sha256(("\n".join(old)+"\n").encode()).hexdigest()}
    (output / "phase4_step7_test_identity_manifest.json").write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    (output / "phase4-step6-collection.log").write_text(old_log, encoding="utf-8")
    (output / "phase4-step7-collection.log").write_text(current_log, encoding="utf-8")
    print(json.dumps({k: result[k] for k in ("baseline_tests", "current_tests", "missing_nodeids")}, indent=2))
    return result


def phase4_step7_candidate(output: Path, step: int = 7) -> None:
    """Build tested Step 7 intermediate evidence without declaring Phase 4 complete."""
    if os.environ.get("RIT_TEST_PARQUET") != "1" or importlib.util.find_spec("pyarrow") is None:
        raise ValueError("Step 7 candidate evidence requires RIT_TEST_PARQUET=1 and real PyArrow")
    output.mkdir(parents=True, exist_ok=True)
    result = audit_phase4_step7(step)
    result["diff"] = audit_phase4_step7_diff(step)
    if git("status", "--porcelain").strip():
        raise ValueError("Step 7 candidate archive requires committed, clean source")
    result["core"] = verify_junit(output / "core.xml", minimum=3420)
    result["parquet"] = verify_junit(output / "parquet.xml", require_parquet=True, minimum=3423)
    result["core_math_measurements"] = verify_step10_evidence(output / "core.xml", output / "phase4-step7-core-observations.json")
    result["parquet_math_measurements"] = verify_step10_evidence(output / "parquet.xml", output / "phase4-step7-parquet-observations.json")
    identity = phase4_step7_baseline_evidence(output)
    result["test_identity"] = {k: identity[k] for k in ("baseline_tests", "current_tests", "nodeids_sha256")}
    expected = set()
    for node in identity["current_nodeids"]:
        base, bracket, parameter = node.partition("[")
        owner, name = base.rsplit("::", 1)
        expected.add((owner.removesuffix(".py").replace("/", ".").replace("::", "."), name + bracket + parameter))
    for name, parquet in (("core.xml", False), ("parquet.xml", True)):
        cases = {(c.get("classname", ""), c.get("name", "")) for c in ET.parse(output / name).getroot().iter("testcase")}
        target = expected if parquet else {c for c in expected if c[1] not in PARQUET_CASES}
        if cases != target:
            raise ValueError(f"Step 7 JUnit does not execute the entire current suite: {name}")
    wheel, _ = verify_distributions(output / "dist")
    smoke_installed(wheel)
    smoke_installed_duplicates(wheel)
    phase4_step2_installed_contract_smoke(wheel)
    phase4_step3_installed_assembly_smoke(wheel)
    phase4_step4_installed_privacy_smoke(wheel)
    phase4_step5_installed_renderers_smoke(wheel)
    phase4_step6_installed_publication_smoke(wheel)
    phase4_step7_installed_cli_smoke(wheel)
    archive = output / "recursive-integrity-toolkit-phase4-step7-candidate.zip"
    subprocess.run(["git", "-C", str(ROOT), "archive", "--format=zip", "--prefix=recursive-integrity-toolkit/", "HEAD", "-o", str(archive.resolve())], check=True)
    tracked = {p for p in git("ls-files", "-z").decode().split("\0") if p}
    with zipfile.ZipFile(archive) as zipped:
        entries = [item.filename for item in zipped.infolist() if not item.is_dir()]
        prefix = "recursive-integrity-toolkit/"
        if (len(entries) != len(set(entries)) or any(not name.startswith(prefix) for name in entries)):
            raise ValueError("Step 7 source archive has duplicate or unprefixed entries")
        names = {name.removeprefix(prefix) for name in entries}
        if names != tracked or len(tracked) != 229 or len(entries) != 229:
            raise ValueError("Step 7 source archive file set mismatch")
        for name in names:
            if zipped.read("recursive-integrity-toolkit/"+name) != (ROOT / name).read_bytes():
                raise ValueError(f"Step 7 source archive byte mismatch: {name}")
    result.update({"commit": git("rev-parse", "HEAD").decode().strip(),
                   "tree": git("rev-parse", "HEAD^{tree}").decode().strip(),
                   "source_archive": archive.name, "tracked_files": len(tracked),
                   "python": sys.version, "platform": sys.platform,
                   "versions": {name: importlib.metadata.version(name) for name in ("numpy", "pandas", "pytest")}})
    (output / "phase4_step7_execution_metadata.json").write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    (output / "phase4_step7_repository_files.sha256").write_text("".join(f"{hashlib.sha256((ROOT/name).read_bytes()).hexdigest()}  {name}\n" for name in sorted(tracked)), encoding="utf-8")
    paths = sorted(p for p in output.rglob("*") if p.is_file() and p.name != "phase4_step7_artifacts.sha256")
    (output / "phase4_step7_artifacts.sha256").write_text("".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(output).as_posix()}\n" for p in paths), encoding="utf-8")
    print(f"Phase 4 Step 7 candidate: {len(tracked)} source files verified; Phase 4 remains incomplete.")


def phase4_step7_cli_main() -> int:
    parser = argparse.ArgumentParser(description="Phase 4 Step 7 maintainer gate")
    parser.add_argument("--phase", type=int, choices=(4,), required=True)
    parser.add_argument("--step", type=int, choices=(7,), required=True)
    parser.add_argument("--diff", action="store_true")
    parser.add_argument("--junit", type=Path)
    parser.add_argument("--require-parquet", action="store_true")
    parser.add_argument("--minimum-tests", type=int, default=1)
    parser.add_argument("--baseline-evidence", type=Path)
    parser.add_argument("--dist", type=Path)
    parser.add_argument("--smoke-wheel", type=Path)
    parser.add_argument("--candidate", type=Path)
    parser.add_argument("--delivery", type=Path)
    args = parser.parse_args()
    if args.delivery is not None:
        raise ValueError("Phase 4 Step 7 cannot certify a final phase delivery")
    if args.junit is not None:
        verify_junit(args.junit, require_parquet=args.require_parquet, minimum=args.minimum_tests)
    elif args.baseline_evidence is not None:
        phase4_step7_baseline_evidence(args.baseline_evidence)
    elif args.dist is not None:
        audit_phase4_step7(args.step)
        wheel, _ = verify_distributions(args.dist)
        smoke_installed(wheel)
        smoke_installed_duplicates(wheel)
        phase4_step2_installed_contract_smoke(wheel)
        phase4_step3_installed_assembly_smoke(wheel)
        phase4_step4_installed_privacy_smoke(wheel)
        phase4_step5_installed_renderers_smoke(wheel)
        phase4_step6_installed_publication_smoke(wheel)
        phase4_step7_installed_cli_smoke(wheel)
    elif args.smoke_wheel is not None:
        smoke_installed(args.smoke_wheel)
    elif args.candidate is not None:
        phase4_step7_candidate(args.candidate, args.step)
    else:
        audit_phase4_step7(args.step)
        if args.diff:
            audit_phase4_step7_diff(args.step)
    return 0


def _phase4_step7_new_test(raw: bytes, path: str) -> None:
    """Only literal test declarations and explicitly listed safe imports."""
    allowed = {"__future__", "json", "pathlib", "pytest"}
    for index, node in enumerate(ast.parse(raw).body):
        if index == 0 and isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            continue
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            modules = [node.module] if isinstance(node, ast.ImportFrom) else [alias.name for alias in node.names]
            if any(module not in allowed for module in modules):
                raise ValueError("Unapproved Step 7 test import")
            continue
        if not isinstance(node, ast.FunctionDef) or not node.name.startswith(("test_phase4_step7_", "phase4_step7_")):
            raise ValueError("Step 7 output tests gained definition-time execution")
        _phase4_step7_header(node, path)


def _phase4_step7_preserve_runtime(before: bytes, after: bytes, path: str) -> None:
    """Allow ownership-header maintenance and byte-exact additive helpers only."""
    try:
        old, new = ast.parse(before), ast.parse(after)
    except (SyntaxError, UnicodeError, ValueError) as error:
        raise ValueError("Output helper source cannot be inspected") from error
    if not ast.get_docstring(old) or not ast.get_docstring(new):
        raise ValueError("Output helper ownership documentation is required")
    old_tail = b"".join(before.splitlines(keepends=True)[old.body[0].end_lineno:])
    new_tail = b"".join(after.splitlines(keepends=True)[new.body[0].end_lineno:])
    if not new_tail.startswith(old_tail):
        raise ValueError(f"Inherited input/diagnostic bytes changed: {path}")


def phase4_step7_installed_cli_smoke(wheel: Path) -> None:
    """Run the installed CLI with caller core dependencies outside the checkout."""
    with tempfile.TemporaryDirectory(prefix="rit-p4-step7-installed-") as temporary:
        work = Path(temporary)
        target = work / "installed"
        subprocess.run([sys.executable, "-m", "pip", "install", "--no-index", "--no-deps", "--target", str(target), str(wheel.resolve())], cwd=work, check=True)
        program = "import importlib.abc, json, os, socket, sys\nfrom pathlib import Path\nsys.path.insert(0,sys.argv[1])\nimport recursive_integrity_toolkit as package\nassert Path(package.__file__).resolve().is_relative_to(Path(sys.argv[1]).resolve())\nassert not Path(package.__file__).resolve().is_relative_to(Path(sys.argv[3]).resolve())\nimport numpy,pandas\nclass NoParquet(importlib.abc.MetaPathFinder):\n def find_spec(self,fullname,path=None,target=None):\n  if fullname.split('.')[0]=='pyarrow':raise AssertionError('ordinary CLI requires no optional dependency')\nsys.meta_path.insert(0,NoParquet())\ndef deny(*args,**kwargs):raise AssertionError('network forbidden')\nsocket.socket=deny;socket.getaddrinfo=deny\nwork=Path(sys.argv[2]);records=work/'records.jsonl';config=work/'config.json'\nrecords.write_text('\\n'.join(json.dumps({'dataset_version':'v1','record_id':str(i),'content':'PRIVATE_CONTENT_'+str(i),'topic':topic}) for i,topic in enumerate(('A','A','B','C'))),encoding='utf-8')\nconfig.write_text(json.dumps({'representation':{'name':'topic','source':'topic_field','field':'topic','version':'1','missing_value_policy':'exclude'}}),encoding='utf-8')\nbefore=records.read_bytes()\nfrom recursive_integrity_toolkit.cli import main\nassert main(['audit','--records',str(records),'--config',str(config),'--out',str(work/'audit')])==0\nreport=json.loads((work/'audit/report.json').read_bytes())\nassert report['derived_metrics']['support']['by_version']['v1']['support_size']['value']==3\nassert report['derived_metrics']['diversity']['by_version']['v1']['gini_simpson_diversity']['value']==0.625\nassert report['simulations']=={} and report['run']['network_call_count']==0\nfrom recursive_integrity_toolkit import cli\ndef no_calculations(*args,**kwargs):raise AssertionError('validate invoked calculations')\noriginal_calculations=cli._calculations\ncli._calculations=no_calculations\nassert main(['validate','--records',str(records),'--out',str(work/'validate'),'--redacted'])==0\nvalidated=json.loads((work/'validate/report.json').read_bytes())\nassert validated['derived_metrics']==validated['proxy_signals']==validated['simulations']=={}\nassert records.read_bytes()==before\nassert all((work/name/'report.md').read_text(encoding='utf-8').startswith('# Recursive Integrity Audit Report') for name in ('audit','validate'))\nassert all('PRIVATE_CONTENT_' not in (work/name/file).read_text(encoding='utf-8') for name in ('audit','validate') for file in ('report.json','report.md'))\ncli._calculations=original_calculations\nimport importlib.metadata,runpy\nentries={entry.name:entry for entry in importlib.metadata.distribution('recursive-integrity-toolkit').entry_points}\nfor alias in ('rit','recursive-integrity'):\n assert entries[alias].load()(['version'])==0\n assert entries[alias].load()(['audit','--records',str(records),'--config',str(config),'--out',str(work/alias),'--redacted'])==0\nsys.argv=['rit','validate','--records',str(records),'--out',str(work/'module'),'--redacted']\ntry:runpy.run_module('recursive_integrity_toolkit',run_name='__main__')\nexcept SystemExit as error:assert error.code==0\nelse:raise AssertionError('module invocation did not exit')\nprint('installed Step 7: external local inputs, core dependencies, ordinary audit and input-only validate, blocked network, unchanged inputs: PASS')\n"
        subprocess.run([sys.executable, "-I", "-c", program, str(target), str(work), str(ROOT)], cwd=work, check=True)



# Phase 4 Step 8: explicit pair and exact packaged resources.


PHASE4_STEP7_FINAL = 'bacd33ae65e392872776c6d976401fdc3d565f63'


PHASE4_STEP7_TREE = '4c16914bb0f0c5281efc36624efb8b1a1d4a174e'


PHASE4_STEP7_TEST_TREE = '96317cb7b25236b79efc0f2d93e1e0f5f132fdb2'


PHASE4_STEP8_APPROVAL = 'phase 4 step 8 开始'


PHASE4_STEP8_APPROVAL_DATE = '2026-09-21'


PHASE4_STEP8_NEW = ('src/recursive_integrity_toolkit/data/hero/EXPECTED_OUTPUTS.md', 'src/recursive_integrity_toolkit/data/hero/config.json', 'src/recursive_integrity_toolkit/data/hero/provenance.csv', 'src/recursive_integrity_toolkit/data/hero/records_v1.csv', 'src/recursive_integrity_toolkit/data/hero/records_v2.csv', 'src/recursive_integrity_toolkit/data/hero/version_order.json', 'src/recursive_integrity_toolkit/data/report.schema.json')


PHASE4_STEP8_ALLOWED = {'.github/workflows/ci.yml',
 '.github/workflows/golden.yml',
 '.github/workflows/release.yml',
 '.github/workflows/security.yml',
 'PHASE_4_BASELINE.json',
 'PHASE_4_DECISIONS.md',
 'docs/architecture.md',
 'docs/cli.md',
 'docs/theory_traceability.md',
 'pyproject.toml',
 'scripts/check_spec_consistency.py',
 'scripts/check_traceability.py',
 'scripts/release_check.py',
 'src/recursive_integrity_toolkit/cli.py',
 'src/recursive_integrity_toolkit/config.py',
 'src/recursive_integrity_toolkit/data/hero/EXPECTED_OUTPUTS.md',
 'src/recursive_integrity_toolkit/data/hero/config.json',
 'src/recursive_integrity_toolkit/data/hero/provenance.csv',
 'src/recursive_integrity_toolkit/data/hero/records_v1.csv',
 'src/recursive_integrity_toolkit/data/hero/records_v2.csv',
 'src/recursive_integrity_toolkit/data/hero/version_order.json',
 'src/recursive_integrity_toolkit/data/report.schema.json',
 'tests/conftest.py',
 'tests/integration/test_ci_workflows.py',
 'tests/integration/test_hero_end_to_end.py',
 'tests/integration/test_hero_structure.py',
 'tests/integration/test_license_notices.py',
 'tests/integration/test_no_algorithms.py',
 'tests/integration/test_no_network.py',
 'tests/integration/test_optional_dependency.py',
 'tests/integration/test_owner_ids.py',
 'tests/integration/test_package_import.py',
 'tests/integration/test_package_install.py',
 'tests/integration/test_phase4_cli.py',
 'tests/integration/test_phase4_gates.py',
 'tests/integration/test_prohibited_structure.py',
 'tests/integration/test_repository_structure.py',
 'tests/integration/test_schema_json.py',
 'tests/unit/test_phase4_contracts.py'}


PHASE4_STEP8_RESOURCES = {'src/recursive_integrity_toolkit/data/hero/EXPECTED_OUTPUTS.md': 'examples/hero/EXPECTED_OUTPUTS.md',
 'src/recursive_integrity_toolkit/data/hero/config.json': 'examples/hero/config.json',
 'src/recursive_integrity_toolkit/data/hero/provenance.csv': 'examples/hero/provenance.csv',
 'src/recursive_integrity_toolkit/data/hero/records_v1.csv': 'examples/hero/records_v1.csv',
 'src/recursive_integrity_toolkit/data/hero/records_v2.csv': 'examples/hero/records_v2.csv',
 'src/recursive_integrity_toolkit/data/hero/version_order.json': 'examples/hero/version_order.json',
 'src/recursive_integrity_toolkit/data/report.schema.json': 'schemas/report.schema.json'}


PHASE4_STEP8_PACKAGING = '\n[tool.setuptools.package-data]\nrecursive_integrity_toolkit = ["data/hero/*", "data/report.schema.json"]\n'


PHASE4_STEP8_MIGRATIONS = {'tests/integration/test_phase4_gates.py': [{'new': 'def '
                                                    'test_phase4_step7_current_workflows_preserve_matrix_and_use_active_dispatch(repo_root, '
                                                    'phase4_step7_snapshot):\n'
                                                    '    repo_root = phase4_step7_snapshot\n'
                                                    '    names = {"ci.yml", "golden.yml", "security.yml", '
                                                    '"release.yml"}\n'
                                                    '    root = repo_root / ".github/workflows"\n'
                                                    '    expected_timeouts = {"ci.yml": [60, 20], '
                                                    '"golden.yml": [15], "security.yml": [20], '
                                                    '"release.yml": [40]}\n'
                                                    '    assert {path.name for path in root.glob("*.yml")} '
                                                    '== names\n'
                                                    '    for name in sorted(names):\n'
                                                    '        text = (root / '
                                                    'name).read_text(encoding="utf-8")\n'
                                                    '        assert [int(line.split(":", 1)[1]) for line in '
                                                    'text.splitlines()\n'
                                                    '                if '
                                                    'line.strip().startswith("timeout-minutes:")] == '
                                                    'expected_timeouts[name]\n'
                                                    '        assert "Phase 4 Step 7" in text, name\n'
                                                    '        assert "--phase 4 --step 7" in text, name\n'
                                                    '        for older in ("--phase 4 --step 6", "--phase 4 '
                                                    '--step 5", "--phase 4 --step 4", "--phase 4 --step 3", '
                                                    '"--phase 4 --step 2", "--phase 4 --step 1", "--phase 3 '
                                                    '--step 11"):\n'
                                                    '            assert older not in text, (name, older)\n'
                                                    '        assert "permissions:\\n  contents: read" in '
                                                    'text\n'
                                                    '        assert "persist-credentials: false" in text\n'
                                                    '        assert "timeout-minutes:" in text and "set -euo '
                                                    'pipefail" in text\n'
                                                    '        assert "actions/upload-artifact@v4" in text and '
                                                    '"if-no-files-found: error" in text\n'
                                                    '        for line in text.splitlines():\n'
                                                    '            if "python scripts/release_check.py" in '
                                                    'line:\n'
                                                    '                assert "--phase 4 --step 7" in line, '
                                                    '(name, line)\n'
                                                    '        for forbidden in ("continue-on-error:", "|| '
                                                    'true", "contents: write", "id-token: write", "twine '
                                                    'upload", "git push"):\n'
                                                    '            assert forbidden not in text, (name, '
                                                    'forbidden)\n'
                                                    '    ci = (root / "ci.yml").read_text(encoding="utf-8")\n'
                                                    "    for required in ('os: [ubuntu-latest, "
                                                    'windows-latest]\', \'python-version: ["3.11", '
                                                    '"3.12"]\',\n'
                                                    "                     'dependencies: [current, "
                                                    'minimum]\', \'"numpy==2.0.0" "pandas==2.2.2"\',\n'
                                                    '                     \'RIT_TEST_PARQUET: "0"\', '
                                                    '\'RIT_TEST_PARQUET: "1"\', \'--require-parquet\',\n'
                                                    "                     '--baseline-evidence', 'python -m "
                                                    "pip check',\n"
                                                    "                     '--minimum-tests 3420', "
                                                    "'--minimum-tests 3423',\n"
                                                    '                     "find_spec(\'pyarrow\') is None", '
                                                    "'import pyarrow'):\n"
                                                    '        assert required in ci\n'
                                                    '    assert ci.count("python -m pytest -p '
                                                    'no:cacheprovider -q --junitxml=") == 2\n'
                                                    '    assert " -k " not in ci\n'
                                                    '    golden = (root / '
                                                    '"golden.yml").read_text(encoding="utf-8")\n'
                                                    '    for required in '
                                                    '("tests/golden/test_phase3_math.py", '
                                                    '"tests/integration/test_hero_structure.py",\n'
                                                    '                     '
                                                    '"tests/integration/test_phase3_metric_pipeline.py"):\n'
                                                    '        assert required in golden\n'
                                                    '    security = (root / '
                                                    '"security.yml").read_text(encoding="utf-8")\n'
                                                    '    for required in '
                                                    "('tests/integration/test_no_network.py', "
                                                    "'tests/integration/test_optional_dependency.py',\n"
                                                    '                     '
                                                    "'tests/unit/test_PR012_evidence_classes.py', "
                                                    "'tests/unit/test_PR013_report_schema.py',\n"
                                                    '                     '
                                                    "'tests/unit/test_PR014_unavailable.py', "
                                                    "'tests/unit/test_PR015_redaction.py',\n"
                                                    '                     '
                                                    "'tests/unit/test_PR016_determinism.py', "
                                                    "'tests/unit/test_PR018_language.py',\n"
                                                    '                     '
                                                    "'tests/integration/test_partial_provenance_report.py',\n"
                                                    '                     '
                                                    "'tests/integration/test_partial_lineage_report.py',\n"
                                                    '                     '
                                                    "'tests/integration/test_phase4_cli.py', "
                                                    "'tests/unit/test_phase4_output_safety.py', "
                                                    "'tests/unit/test_phase4_contracts.py', "
                                                    "'tests/integration/test_phase4_gates.py'):\n"
                                                    '        assert required in security\n'
                                                    '    release = (root / '
                                                    '"release.yml").read_text(encoding="utf-8")\n'
                                                    '    assert "python -m build" in release and "python -m '
                                                    'twine check --strict" in release\n'
                                                    '    assert "--dist" in release and "--candidate" in '
                                                    'release\n'
                                                    '    assert "--delivery" not in release\n'
                                                    '    assert '
                                                    '"recursive-integrity-toolkit-phase4-step7-candidate" in '
                                                    'release\n'
                                                    '    assert "rit-phase4-step4" not in release\n'
                                                    '    assert "--minimum-tests 3420" in release and '
                                                    '"--minimum-tests 3423" in release\n'
                                                    '    assert release.count("python -m pytest -p '
                                                    'no:cacheprovider -q --junitxml=") == 2',
                                             'node': 'test_phase4_step7_current_workflows_preserve_matrix_and_use_active_dispatch',
                                             'old': 'def '
                                                    'test_phase4_step7_current_workflows_preserve_matrix_and_use_active_dispatch(repo_root):\n'
                                                    '    names = {"ci.yml", "golden.yml", "security.yml", '
                                                    '"release.yml"}\n'
                                                    '    root = repo_root / ".github/workflows"\n'
                                                    '    expected_timeouts = {"ci.yml": [60, 20], '
                                                    '"golden.yml": [15], "security.yml": [20], '
                                                    '"release.yml": [40]}\n'
                                                    '    assert {path.name for path in root.glob("*.yml")} '
                                                    '== names\n'
                                                    '    for name in sorted(names):\n'
                                                    '        text = (root / '
                                                    'name).read_text(encoding="utf-8")\n'
                                                    '        assert [int(line.split(":", 1)[1]) for line in '
                                                    'text.splitlines()\n'
                                                    '                if '
                                                    'line.strip().startswith("timeout-minutes:")] == '
                                                    'expected_timeouts[name]\n'
                                                    '        assert "Phase 4 Step 7" in text, name\n'
                                                    '        assert "--phase 4 --step 7" in text, name\n'
                                                    '        for older in ("--phase 4 --step 6", "--phase 4 '
                                                    '--step 5", "--phase 4 --step 4", "--phase 4 --step 3", '
                                                    '"--phase 4 --step 2", "--phase 4 --step 1", "--phase 3 '
                                                    '--step 11"):\n'
                                                    '            assert older not in text, (name, older)\n'
                                                    '        assert "permissions:\\n  contents: read" in '
                                                    'text\n'
                                                    '        assert "persist-credentials: false" in text\n'
                                                    '        assert "timeout-minutes:" in text and "set -euo '
                                                    'pipefail" in text\n'
                                                    '        assert "actions/upload-artifact@v4" in text and '
                                                    '"if-no-files-found: error" in text\n'
                                                    '        for line in text.splitlines():\n'
                                                    '            if "python scripts/release_check.py" in '
                                                    'line:\n'
                                                    '                assert "--phase 4 --step 7" in line, '
                                                    '(name, line)\n'
                                                    '        for forbidden in ("continue-on-error:", "|| '
                                                    'true", "contents: write", "id-token: write", "twine '
                                                    'upload", "git push"):\n'
                                                    '            assert forbidden not in text, (name, '
                                                    'forbidden)\n'
                                                    '    ci = (root / "ci.yml").read_text(encoding="utf-8")\n'
                                                    "    for required in ('os: [ubuntu-latest, "
                                                    'windows-latest]\', \'python-version: ["3.11", '
                                                    '"3.12"]\',\n'
                                                    "                     'dependencies: [current, "
                                                    'minimum]\', \'"numpy==2.0.0" "pandas==2.2.2"\',\n'
                                                    '                     \'RIT_TEST_PARQUET: "0"\', '
                                                    '\'RIT_TEST_PARQUET: "1"\', \'--require-parquet\',\n'
                                                    "                     '--baseline-evidence', 'python -m "
                                                    "pip check',\n"
                                                    "                     '--minimum-tests 3420', "
                                                    "'--minimum-tests 3423',\n"
                                                    '                     "find_spec(\'pyarrow\') is None", '
                                                    "'import pyarrow'):\n"
                                                    '        assert required in ci\n'
                                                    '    assert ci.count("python -m pytest -p '
                                                    'no:cacheprovider -q --junitxml=") == 2\n'
                                                    '    assert " -k " not in ci\n'
                                                    '    golden = (root / '
                                                    '"golden.yml").read_text(encoding="utf-8")\n'
                                                    '    for required in '
                                                    '("tests/golden/test_phase3_math.py", '
                                                    '"tests/integration/test_hero_structure.py",\n'
                                                    '                     '
                                                    '"tests/integration/test_phase3_metric_pipeline.py"):\n'
                                                    '        assert required in golden\n'
                                                    '    security = (root / '
                                                    '"security.yml").read_text(encoding="utf-8")\n'
                                                    '    for required in '
                                                    "('tests/integration/test_no_network.py', "
                                                    "'tests/integration/test_optional_dependency.py',\n"
                                                    '                     '
                                                    "'tests/unit/test_PR012_evidence_classes.py', "
                                                    "'tests/unit/test_PR013_report_schema.py',\n"
                                                    '                     '
                                                    "'tests/unit/test_PR014_unavailable.py', "
                                                    "'tests/unit/test_PR015_redaction.py',\n"
                                                    '                     '
                                                    "'tests/unit/test_PR016_determinism.py', "
                                                    "'tests/unit/test_PR018_language.py',\n"
                                                    '                     '
                                                    "'tests/integration/test_partial_provenance_report.py',\n"
                                                    '                     '
                                                    "'tests/integration/test_partial_lineage_report.py',\n"
                                                    '                     '
                                                    "'tests/integration/test_phase4_cli.py', "
                                                    "'tests/unit/test_phase4_output_safety.py', "
                                                    "'tests/unit/test_phase4_contracts.py', "
                                                    "'tests/integration/test_phase4_gates.py'):\n"
                                                    '        assert required in security\n'
                                                    '    release = (root / '
                                                    '"release.yml").read_text(encoding="utf-8")\n'
                                                    '    assert "python -m build" in release and "python -m '
                                                    'twine check --strict" in release\n'
                                                    '    assert "--dist" in release and "--candidate" in '
                                                    'release\n'
                                                    '    assert "--delivery" not in release\n'
                                                    '    assert '
                                                    '"recursive-integrity-toolkit-phase4-step7-candidate" in '
                                                    'release\n'
                                                    '    assert "rit-phase4-step4" not in release\n'
                                                    '    assert "--minimum-tests 3420" in release and '
                                                    '"--minimum-tests 3423" in release\n'
                                                    '    assert release.count("python -m pytest -p '
                                                    'no:cacheprovider -q --junitxml=") == 2'},
                                            {'new': 'def '
                                                    'test_phase4_step7_current_cli_ast_rejects_injection(repo_root, '
                                                    'tmp_path, relative, injection, phase4_step7_snapshot):\n'
                                                    '    repo_root = phase4_step7_snapshot\n'
                                                    '    checker = runpy.run_path(str(repo_root / '
                                                    '"scripts/check_traceability.py"), '
                                                    'run_name="phase4_step7_ast_tests")\n'
                                                    '    verify = checker["phase4_step7_runtime_boundary"]\n'
                                                    '    path = "src/recursive_integrity_toolkit/" + '
                                                    'relative\n'
                                                    '    verify(repo_root / path, path)\n'
                                                    '    changed = tmp_path / "changed.py"\n'
                                                    '    changed.write_bytes((repo_root / path).read_bytes() '
                                                    '+ injection)\n'
                                                    '    with pytest.raises(ValueError):\n'
                                                    '        verify(changed, path)',
                                             'node': 'test_phase4_step7_current_cli_ast_rejects_injection',
                                             'old': 'def '
                                                    'test_phase4_step7_current_cli_ast_rejects_injection(repo_root, '
                                                    'tmp_path, relative, injection):\n'
                                                    '    checker = runpy.run_path(str(repo_root / '
                                                    '"scripts/check_traceability.py"), '
                                                    'run_name="phase4_step7_ast_tests")\n'
                                                    '    verify = checker["phase4_step7_runtime_boundary"]\n'
                                                    '    path = "src/recursive_integrity_toolkit/" + '
                                                    'relative\n'
                                                    '    verify(repo_root / path, path)\n'
                                                    '    changed = tmp_path / "changed.py"\n'
                                                    '    changed.write_bytes((repo_root / path).read_bytes() '
                                                    '+ injection)\n'
                                                    '    with pytest.raises(ValueError):\n'
                                                    '        verify(changed, path)'},
                                            {'new': 'def '
                                                    'test_phase4_step7_new_cli_tests_reject_definition_effects(repo_root, '
                                                    'phase4_gate_tools, injection, phase4_step7_snapshot):\n'
                                                    '    repo_root = phase4_step7_snapshot\n'
                                                    '    path = "tests/integration/test_phase4_cli.py"\n'
                                                    '    raw = (repo_root / path).read_bytes()\n'
                                                    '    verify = '
                                                    'phase4_gate_tools["_phase4_step7_new_test"]\n'
                                                    '    verify(raw, path)\n'
                                                    '    with pytest.raises(ValueError):\n'
                                                    '        verify(raw + injection, path)',
                                             'node': 'test_phase4_step7_new_cli_tests_reject_definition_effects',
                                             'old': 'def '
                                                    'test_phase4_step7_new_cli_tests_reject_definition_effects(repo_root, '
                                                    'phase4_gate_tools, injection):\n'
                                                    '    path = "tests/integration/test_phase4_cli.py"\n'
                                                    '    raw = (repo_root / path).read_bytes()\n'
                                                    '    verify = '
                                                    'phase4_gate_tools["_phase4_step7_new_test"]\n'
                                                    '    verify(raw, path)\n'
                                                    '    with pytest.raises(ValueError):\n'
                                                    '        verify(raw + injection, path)'},
                                            {'new': 'def '
                                                    'test_phase4_step7_current_snapshot_checks_valid_tree_before_mutations(repo_root, '
                                                    'tmp_path, phase4_gate_tools, mutation, '
                                                    'phase4_step7_snapshot):\n'
                                                    '    import json\n'
                                                    '\n'
                                                    '    paths = '
                                                    '{path.relative_to(phase4_step7_snapshot).as_posix()\n'
                                                    '             for path in '
                                                    'phase4_step7_snapshot.rglob("*") if path.is_file()}\n'
                                                    '    assert len(paths) == 229\n'
                                                    '    for relative in sorted(paths):\n'
                                                    '        destination = tmp_path / relative\n'
                                                    '        destination.parent.mkdir(parents=True, '
                                                    'exist_ok=True)\n'
                                                    '        shutil.copyfile(phase4_step7_snapshot / '
                                                    'relative, destination)\n'
                                                    '    verify = '
                                                    'phase4_gate_tools["verify_phase4_step7_snapshot"]\n'
                                                    '    baseline = verify(tmp_path)\n'
                                                    '    assert baseline["package_modules"] == 40\n'
                                                    '    assert baseline["frozen_runtime_modules"] == 38\n'
                                                    '    assert baseline["frozen_schemas"] == 5\n'
                                                    '    assert baseline["result_contracts_enabled"] is '
                                                    'True\n'
                                                    '    assert baseline["adapters_enabled"] is True\n'
                                                    '    assert baseline["privacy_views_enabled"] is True\n'
                                                    '    assert baseline["renderers_enabled"] is True\n'
                                                    '    assert baseline["output_publication_enabled"] is '
                                                    'True\n'
                                                    '    assert baseline["cli_analysis_enabled"] is True\n'
                                                    '    assert baseline["phase_complete"] is False\n'
                                                    '    if mutation == "unchanged":\n'
                                                    '        return\n'
                                                    '    replacements = {\n'
                                                    '        "formula": '
                                                    '("src/recursive_integrity_toolkit/metrics/diversity.py",\n'
                                                    '                    b"diversity = 1.0 - concentration", '
                                                    'b"diversity = 0.5 - concentration"),\n'
                                                    '        "math_oracle": '
                                                    '("tests/golden/phase3_math_cases.json", '
                                                    'b\'"v2_support":5\', b\'"v2_support":3\'),\n'
                                                    '        "hero": ("examples/hero/records_v2.csv", '
                                                    'b"v2_08,v2,", b"v2_99,v2,"),\n'
                                                    '        "dependency": ("pyproject.toml", b"numpy>=2.0", '
                                                    'b"numpy>=3.0"),\n'
                                                    '        "historical_assertion": '
                                                    '("tests/unit/test_phase4_contracts.py",\n'
                                                    "                                 b'    assert "
                                                    'control["active_phase"] == 4 and control["active_step"] '
                                                    "== 4\\n',\n"
                                                    '                                 b"    assert '
                                                    'True\\n"),\n'
                                                    '        "historical_tooling": '
                                                    '("scripts/release_check.py",\n'
                                                    '                               b"def '
                                                    'verify_phase4_step4_control(control: dict, step: int = '
                                                    '4) -> None:",\n'
                                                    '                               b"def '
                                                    'verify_phase4_step4_control(control: dict, step: int = '
                                                    '4) -> None:\\n    return"),\n'
                                                    '        "historical_binding": '
                                                    '("tests/integration/test_phase4_gates.py",\n'
                                                    '                               b"def '
                                                    'test_phase4_step4_current_workflows_preserve_matrix_and_use_active_dispatch(repo_root, '
                                                    'phase4_step4_snapshot):\\n    repo_root = '
                                                    'phase4_step4_snapshot\\n",\n'
                                                    '                               b"def '
                                                    'test_phase4_step4_current_workflows_preserve_matrix_and_use_active_dispatch(repo_root, '
                                                    'phase4_step4_snapshot):\\n"),\n'
                                                    '        "historical_document": ("docs/cli.md", b"# '
                                                    'CLI\\n",\n'
                                                    '                                b"# Unauthorized '
                                                    'historical document\\n"),\n'
                                                    '        "input_hash_helper": '
                                                    '("src/recursive_integrity_toolkit/utils/hashing.py",\n'
                                                    '                              b"return '
                                                    'hashlib.sha256(data).hexdigest()", b"return '
                                                    'hashlib.sha256(b\'changed\').hexdigest()"),\n'
                                                    '        "config_resolver_helper": '
                                                    '("src/recursive_integrity_toolkit/config.py",\n'
                                                    '                                   b"def '
                                                    'resolve_config(", b"def resolve_config_disabled("),\n'
                                                    '    }\n'
                                                    '    appended = {\n'
                                                    '        "frozen_model": '
                                                    '"src/recursive_integrity_toolkit/models.py",\n'
                                                    '        "frozen_schema": "schemas/report.schema.json",\n'
                                                    '        "plan": "PHASE_4_PLAN.md",\n'
                                                    '        "cli": '
                                                    '"src/recursive_integrity_toolkit/cli.py",\n'
                                                    '        "html": '
                                                    '"src/recursive_integrity_toolkit/reports/html_report.py",\n'
                                                    '        "assembly": '
                                                    '"src/recursive_integrity_toolkit/reports/assembly.py",\n'
                                                    '        "result": '
                                                    '"src/recursive_integrity_toolkit/result.py",\n'
                                                    '        "config": '
                                                    '"src/recursive_integrity_toolkit/config.py",\n'
                                                    '        "hashing": '
                                                    '"src/recursive_integrity_toolkit/utils/hashing.py",\n'
                                                    '        "logging": '
                                                    '"src/recursive_integrity_toolkit/utils/logging.py",\n'
                                                    '        "output_paths": '
                                                    '"src/recursive_integrity_toolkit/utils/paths.py",\n'
                                                    '    }\n'
                                                    '    added = {\n'
                                                    '        "unknown_runtime": '
                                                    '"src/recursive_integrity_toolkit/reports/unauthorized.py",\n'
                                                    '        "premature_completion": '
                                                    '"PHASE_4_COMPLETION.md", "premature_report": '
                                                    '"report.json",\n'
                                                    '    }\n'
                                                    '    if mutation in replacements:\n'
                                                    '        relative, original, replacement = '
                                                    'replacements[mutation]\n'
                                                    '        path = tmp_path / relative\n'
                                                    '        source = path.read_bytes()\n'
                                                    '        assert source.count(original) == 1\n'
                                                    '        path.write_bytes(source.replace(original, '
                                                    'replacement, 1))\n'
                                                    '    elif mutation in appended:\n'
                                                    '        path = tmp_path / appended[mutation]\n'
                                                    '        path.write_bytes(path.read_bytes() + '
                                                    'b"\\nUnauthorized Step 7 mutation\\n")\n'
                                                    '    elif mutation in added:\n'
                                                    '        path = tmp_path / added[mutation]\n'
                                                    '        assert not path.exists()\n'
                                                    '        path.write_text("Unauthorized later-stage '
                                                    'file\\n", encoding="utf-8")\n'
                                                    '    elif mutation == "missing_runtime":\n'
                                                    '        (tmp_path / '
                                                    '"src/recursive_integrity_toolkit/metrics/bounds.py").unlink()\n'
                                                    '    elif mutation.startswith("control_"):\n'
                                                    '        path = tmp_path / "PHASE_4_BASELINE.json"\n'
                                                    '        control = '
                                                    'json.loads(path.read_text(encoding="utf-8"))\n'
                                                    '        if mutation == "control_step":\n'
                                                    '            control["active_step"] = 8\n'
                                                    '        elif mutation == "control_scope":\n'
                                                    '            '
                                                    'control["runtime_paths_authorized"].append("src/recursive_integrity_toolkit/reports/assembly.py")\n'
                                                    '        else:\n'
                                                    '            control["schema_changes_authorized"] = '
                                                    'True\n'
                                                    '            '
                                                    'control["schema_paths_authorized"].append("schemas/report.schema.json")\n'
                                                    '        path.write_text(json.dumps(control), '
                                                    'encoding="utf-8")\n'
                                                    '    else:\n'
                                                    '        raise AssertionError(f"Unknown active mutation '
                                                    'case: {mutation}")\n'
                                                    '    with pytest.raises(ValueError):\n'
                                                    '        verify(tmp_path)',
                                             'node': 'test_phase4_step7_current_snapshot_checks_valid_tree_before_mutations',
                                             'old': 'def '
                                                    'test_phase4_step7_current_snapshot_checks_valid_tree_before_mutations(repo_root, '
                                                    'tmp_path, phase4_gate_tools, mutation):\n'
                                                    '    import json\n'
                                                    '\n'
                                                    '    tracked = subprocess.check_output(["git", "-C", '
                                                    'str(repo_root), "ls-files", "-z"])\n'
                                                    '    paths = set(tracked.decode().split("\\0")) - {""}\n'
                                                    '    assert len(paths) == 229\n'
                                                    '    for relative in sorted(paths):\n'
                                                    '        destination = tmp_path / relative\n'
                                                    '        destination.parent.mkdir(parents=True, '
                                                    'exist_ok=True)\n'
                                                    '        shutil.copyfile(repo_root / relative, '
                                                    'destination)\n'
                                                    '    verify = '
                                                    'phase4_gate_tools["verify_phase4_step7_snapshot"]\n'
                                                    '    baseline = verify(tmp_path)\n'
                                                    '    assert baseline["package_modules"] == 40\n'
                                                    '    assert baseline["frozen_runtime_modules"] == 38\n'
                                                    '    assert baseline["frozen_schemas"] == 5\n'
                                                    '    assert baseline["result_contracts_enabled"] is '
                                                    'True\n'
                                                    '    assert baseline["adapters_enabled"] is True\n'
                                                    '    assert baseline["privacy_views_enabled"] is True\n'
                                                    '    assert baseline["renderers_enabled"] is True\n'
                                                    '    assert baseline["output_publication_enabled"] is '
                                                    'True\n'
                                                    '    assert baseline["cli_analysis_enabled"] is True\n'
                                                    '    assert baseline["phase_complete"] is False\n'
                                                    '    if mutation == "unchanged":\n'
                                                    '        return\n'
                                                    '    replacements = {\n'
                                                    '        "formula": '
                                                    '("src/recursive_integrity_toolkit/metrics/diversity.py",\n'
                                                    '                    b"diversity = 1.0 - concentration", '
                                                    'b"diversity = 0.5 - concentration"),\n'
                                                    '        "math_oracle": '
                                                    '("tests/golden/phase3_math_cases.json", '
                                                    'b\'"v2_support":5\', b\'"v2_support":3\'),\n'
                                                    '        "hero": ("examples/hero/records_v2.csv", '
                                                    'b"v2_08,v2,", b"v2_99,v2,"),\n'
                                                    '        "dependency": ("pyproject.toml", b"numpy>=2.0", '
                                                    'b"numpy>=3.0"),\n'
                                                    '        "historical_assertion": '
                                                    '("tests/unit/test_phase4_contracts.py",\n'
                                                    "                                 b'    assert "
                                                    'control["active_phase"] == 4 and control["active_step"] '
                                                    "== 4\\n',\n"
                                                    '                                 b"    assert '
                                                    'True\\n"),\n'
                                                    '        "historical_tooling": '
                                                    '("scripts/release_check.py",\n'
                                                    '                               b"def '
                                                    'verify_phase4_step4_control(control: dict, step: int = '
                                                    '4) -> None:",\n'
                                                    '                               b"def '
                                                    'verify_phase4_step4_control(control: dict, step: int = '
                                                    '4) -> None:\\n    return"),\n'
                                                    '        "historical_binding": '
                                                    '("tests/integration/test_phase4_gates.py",\n'
                                                    '                               b"def '
                                                    'test_phase4_step4_current_workflows_preserve_matrix_and_use_active_dispatch(repo_root, '
                                                    'phase4_step4_snapshot):\\n    repo_root = '
                                                    'phase4_step4_snapshot\\n",\n'
                                                    '                               b"def '
                                                    'test_phase4_step4_current_workflows_preserve_matrix_and_use_active_dispatch(repo_root, '
                                                    'phase4_step4_snapshot):\\n"),\n'
                                                    '        "historical_document": ("docs/cli.md", b"# '
                                                    'CLI\\n",\n'
                                                    '                                b"# Unauthorized '
                                                    'historical document\\n"),\n'
                                                    '        "input_hash_helper": '
                                                    '("src/recursive_integrity_toolkit/utils/hashing.py",\n'
                                                    '                              b"return '
                                                    'hashlib.sha256(data).hexdigest()", b"return '
                                                    'hashlib.sha256(b\'changed\').hexdigest()"),\n'
                                                    '        "config_resolver_helper": '
                                                    '("src/recursive_integrity_toolkit/config.py",\n'
                                                    '                                   b"def '
                                                    'resolve_config(", b"def resolve_config_disabled("),\n'
                                                    '    }\n'
                                                    '    appended = {\n'
                                                    '        "frozen_model": '
                                                    '"src/recursive_integrity_toolkit/models.py",\n'
                                                    '        "frozen_schema": "schemas/report.schema.json",\n'
                                                    '        "plan": "PHASE_4_PLAN.md",\n'
                                                    '        "cli": '
                                                    '"src/recursive_integrity_toolkit/cli.py",\n'
                                                    '        "html": '
                                                    '"src/recursive_integrity_toolkit/reports/html_report.py",\n'
                                                    '        "assembly": '
                                                    '"src/recursive_integrity_toolkit/reports/assembly.py",\n'
                                                    '        "result": '
                                                    '"src/recursive_integrity_toolkit/result.py",\n'
                                                    '        "config": '
                                                    '"src/recursive_integrity_toolkit/config.py",\n'
                                                    '        "hashing": '
                                                    '"src/recursive_integrity_toolkit/utils/hashing.py",\n'
                                                    '        "logging": '
                                                    '"src/recursive_integrity_toolkit/utils/logging.py",\n'
                                                    '        "output_paths": '
                                                    '"src/recursive_integrity_toolkit/utils/paths.py",\n'
                                                    '    }\n'
                                                    '    added = {\n'
                                                    '        "unknown_runtime": '
                                                    '"src/recursive_integrity_toolkit/reports/unauthorized.py",\n'
                                                    '        "premature_completion": '
                                                    '"PHASE_4_COMPLETION.md", "premature_report": '
                                                    '"report.json",\n'
                                                    '    }\n'
                                                    '    if mutation in replacements:\n'
                                                    '        relative, original, replacement = '
                                                    'replacements[mutation]\n'
                                                    '        path = tmp_path / relative\n'
                                                    '        source = path.read_bytes()\n'
                                                    '        assert source.count(original) == 1\n'
                                                    '        path.write_bytes(source.replace(original, '
                                                    'replacement, 1))\n'
                                                    '    elif mutation in appended:\n'
                                                    '        path = tmp_path / appended[mutation]\n'
                                                    '        path.write_bytes(path.read_bytes() + '
                                                    'b"\\nUnauthorized Step 7 mutation\\n")\n'
                                                    '    elif mutation in added:\n'
                                                    '        path = tmp_path / added[mutation]\n'
                                                    '        assert not path.exists()\n'
                                                    '        path.write_text("Unauthorized later-stage '
                                                    'file\\n", encoding="utf-8")\n'
                                                    '    elif mutation == "missing_runtime":\n'
                                                    '        (tmp_path / '
                                                    '"src/recursive_integrity_toolkit/metrics/bounds.py").unlink()\n'
                                                    '    elif mutation.startswith("control_"):\n'
                                                    '        path = tmp_path / "PHASE_4_BASELINE.json"\n'
                                                    '        control = '
                                                    'json.loads(path.read_text(encoding="utf-8"))\n'
                                                    '        if mutation == "control_step":\n'
                                                    '            control["active_step"] = 8\n'
                                                    '        elif mutation == "control_scope":\n'
                                                    '            '
                                                    'control["runtime_paths_authorized"].append("src/recursive_integrity_toolkit/reports/assembly.py")\n'
                                                    '        else:\n'
                                                    '            control["schema_changes_authorized"] = '
                                                    'True\n'
                                                    '            '
                                                    'control["schema_paths_authorized"].append("schemas/report.schema.json")\n'
                                                    '        path.write_text(json.dumps(control), '
                                                    'encoding="utf-8")\n'
                                                    '    else:\n'
                                                    '        raise AssertionError(f"Unknown active mutation '
                                                    'case: {mutation}")\n'
                                                    '    with pytest.raises(ValueError):\n'
                                                    '        verify(tmp_path)'}],
 'tests/unit/test_phase4_contracts.py': [{'new': 'def '
                                                 'test_phase4_step7_approved_control_keeps_independent_step6_anchors(phase4_tools, '
                                                 'phase4_step7_snapshot):\n'
                                                 '    control = json.loads((phase4_step7_snapshot / '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\n'
                                                 '    assert phase4_tools["PHASE4_STEP6_FINAL"] == '
                                                 '"aa2355f2359c3af4fc05345c792f9903b0d5858c"\n'
                                                 '    assert phase4_tools["PHASE4_STEP6_TREE"] == '
                                                 '"d9b6910079f49a2c739f86eceec05040918a41a5"\n'
                                                 '    assert phase4_tools["PHASE4_STEP6_TEST_TREE"] == '
                                                 '"8d3a03c61da807d1fef8d26fc4af0d6f72e4546e"\n'
                                                 '    assert control["active_phase"] == 4 and '
                                                 'control["active_step"] == 7\n'
                                                 '    assert control["approval_basis"] == "Phase 4 Step 7 '
                                                 '继续"\n'
                                                 '    assert control["baseline_commit"] == BASELINE\n'
                                                 '    assert control["previous_step_commit"] == '
                                                 '"aa2355f2359c3af4fc05345c792f9903b0d5858c"\n'
                                                 '    assert control["previous_step_tree"] == '
                                                 '"d9b6910079f49a2c739f86eceec05040918a41a5"\n'
                                                 '    assert control["previous_step_test_tree"] == '
                                                 '"8d3a03c61da807d1fef8d26fc4af0d6f72e4546e"\n'
                                                 '    assert control["previous_step_core_tests"] == 3420\n'
                                                 '    assert control["previous_step_parquet_tests"] == 3423\n'
                                                 '    assert len(control["previous_step_files_sha256"]) == '
                                                 '228\n'
                                                 '    assert set(control["runtime_paths_authorized"]) == {\n'
                                                 '        "src/recursive_integrity_toolkit/cli.py",\n'
                                                 '        "src/recursive_integrity_toolkit/config.py",\n'
                                                 '    }\n'
                                                 '    assert control["schema_changes_authorized"] is False\n'
                                                 '    assert control["schema_paths_authorized"] == []\n'
                                                 '    assert control["new_files_permitted"] == '
                                                 '["tests/integration/test_phase4_cli.py"]\n'
                                                 '    for name in ("phase_complete", "next_step_authorized", '
                                                 '"main_merge_authorized", "publication_authorized"):\n'
                                                 '        assert control[name] is False\n'
                                                 '    phase4_tools["verify_phase4_step7_control"](control, '
                                                 'step=7)\n'
                                                 '    with pytest.raises(ValueError):\n'
                                                 '        '
                                                 'phase4_tools["verify_phase4_step4_control"](control, '
                                                 'step=4)',
                                          'node': 'test_phase4_step7_approved_control_keeps_independent_step6_anchors',
                                          'old': 'def '
                                                 'test_phase4_step7_approved_control_keeps_independent_step6_anchors(phase4_tools):\n'
                                                 '    control = json.loads((ROOT / '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\n'
                                                 '    assert phase4_tools["PHASE4_STEP6_FINAL"] == '
                                                 '"aa2355f2359c3af4fc05345c792f9903b0d5858c"\n'
                                                 '    assert phase4_tools["PHASE4_STEP6_TREE"] == '
                                                 '"d9b6910079f49a2c739f86eceec05040918a41a5"\n'
                                                 '    assert phase4_tools["PHASE4_STEP6_TEST_TREE"] == '
                                                 '"8d3a03c61da807d1fef8d26fc4af0d6f72e4546e"\n'
                                                 '    assert control["active_phase"] == 4 and '
                                                 'control["active_step"] == 7\n'
                                                 '    assert control["approval_basis"] == "Phase 4 Step 7 '
                                                 '继续"\n'
                                                 '    assert control["baseline_commit"] == BASELINE\n'
                                                 '    assert control["previous_step_commit"] == '
                                                 '"aa2355f2359c3af4fc05345c792f9903b0d5858c"\n'
                                                 '    assert control["previous_step_tree"] == '
                                                 '"d9b6910079f49a2c739f86eceec05040918a41a5"\n'
                                                 '    assert control["previous_step_test_tree"] == '
                                                 '"8d3a03c61da807d1fef8d26fc4af0d6f72e4546e"\n'
                                                 '    assert control["previous_step_core_tests"] == 3420\n'
                                                 '    assert control["previous_step_parquet_tests"] == 3423\n'
                                                 '    assert len(control["previous_step_files_sha256"]) == '
                                                 '228\n'
                                                 '    assert set(control["runtime_paths_authorized"]) == {\n'
                                                 '        "src/recursive_integrity_toolkit/cli.py",\n'
                                                 '        "src/recursive_integrity_toolkit/config.py",\n'
                                                 '    }\n'
                                                 '    assert control["schema_changes_authorized"] is False\n'
                                                 '    assert control["schema_paths_authorized"] == []\n'
                                                 '    assert control["new_files_permitted"] == '
                                                 '["tests/integration/test_phase4_cli.py"]\n'
                                                 '    for name in ("phase_complete", "next_step_authorized", '
                                                 '"main_merge_authorized", "publication_authorized"):\n'
                                                 '        assert control[name] is False\n'
                                                 '    phase4_tools["verify_phase4_step7_control"](control, '
                                                 'step=7)\n'
                                                 '    with pytest.raises(ValueError):\n'
                                                 '        '
                                                 'phase4_tools["verify_phase4_step4_control"](control, '
                                                 'step=4)'},
                                         {'new': 'def '
                                                 'test_phase4_step7_control_rejects_forged_scope_and_stage(phase4_tools, '
                                                 'field, value, phase4_step7_snapshot):\n'
                                                 '    control = json.loads((phase4_step7_snapshot / '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\n'
                                                 '    verify = phase4_tools["verify_phase4_step7_control"]\n'
                                                 '    verify(control, step=7)\n'
                                                 '    control[field] = value\n'
                                                 '    with pytest.raises(ValueError):\n'
                                                 '        verify(control, step=7)',
                                          'node': 'test_phase4_step7_control_rejects_forged_scope_and_stage',
                                          'old': 'def '
                                                 'test_phase4_step7_control_rejects_forged_scope_and_stage(phase4_tools, '
                                                 'field, value):\n'
                                                 '    control = json.loads((ROOT / '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\n'
                                                 '    verify = phase4_tools["verify_phase4_step7_control"]\n'
                                                 '    verify(control, step=7)\n'
                                                 '    control[field] = value\n'
                                                 '    with pytest.raises(ValueError):\n'
                                                 '        verify(control, step=7)'},
                                         {'new': 'def '
                                                 'test_phase4_step7_control_rejects_unapproved_dispatch(phase4_tools, '
                                                 'step, phase4_step7_snapshot):\n'
                                                 '    control = json.loads((phase4_step7_snapshot / '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\n'
                                                 '    phase4_tools["verify_phase4_step7_control"](control, '
                                                 'step=7)\n'
                                                 '    with pytest.raises(ValueError):\n'
                                                 '        '
                                                 'phase4_tools["verify_phase4_step7_control"](control, '
                                                 'step=step)',
                                          'node': 'test_phase4_step7_control_rejects_unapproved_dispatch',
                                          'old': 'def '
                                                 'test_phase4_step7_control_rejects_unapproved_dispatch(phase4_tools, '
                                                 'step):\n'
                                                 '    control = json.loads((ROOT / '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\n'
                                                 '    phase4_tools["verify_phase4_step7_control"](control, '
                                                 'step=7)\n'
                                                 '    with pytest.raises(ValueError):\n'
                                                 '        '
                                                 'phase4_tools["verify_phase4_step7_control"](control, '
                                                 'step=step)'},
                                         {'new': 'def '
                                                 'test_phase4_step7_control_requires_explicit_approval_fields(phase4_tools, '
                                                 'field, phase4_step7_snapshot):\n'
                                                 '    control = json.loads((phase4_step7_snapshot / '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\n'
                                                 '    phase4_tools["verify_phase4_step7_control"](control)\n'
                                                 '    del control[field]\n'
                                                 '    with pytest.raises(ValueError):\n'
                                                 '        '
                                                 'phase4_tools["verify_phase4_step7_control"](control)',
                                          'node': 'test_phase4_step7_control_requires_explicit_approval_fields',
                                          'old': 'def '
                                                 'test_phase4_step7_control_requires_explicit_approval_fields(phase4_tools, '
                                                 'field):\n'
                                                 '    control = json.loads((ROOT / '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\n'
                                                 '    phase4_tools["verify_phase4_step7_control"](control)\n'
                                                 '    del control[field]\n'
                                                 '    with pytest.raises(ValueError):\n'
                                                 '        '
                                                 'phase4_tools["verify_phase4_step7_control"](control)'},
                                         {'new': 'def '
                                                 'test_phase4_step7_control_cannot_mint_extra_permission(phase4_tools, '
                                                 'phase4_step7_snapshot):\n'
                                                 '    control = json.loads((phase4_step7_snapshot / '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\n'
                                                 '    phase4_tools["verify_phase4_step7_control"](control)\n'
                                                 '    control["approved_scope_expansion"] = {"step": 7, '
                                                 '"publication": True}\n'
                                                 '    with pytest.raises(ValueError):\n'
                                                 '        '
                                                 'phase4_tools["verify_phase4_step7_control"](control)',
                                          'node': 'test_phase4_step7_control_cannot_mint_extra_permission',
                                          'old': 'def '
                                                 'test_phase4_step7_control_cannot_mint_extra_permission(phase4_tools):\n'
                                                 '    control = json.loads((ROOT / '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\n'
                                                 '    phase4_tools["verify_phase4_step7_control"](control)\n'
                                                 '    control["approved_scope_expansion"] = {"step": 7, '
                                                 '"publication": True}\n'
                                                 '    with pytest.raises(ValueError):\n'
                                                 '        '
                                                 'phase4_tools["verify_phase4_step7_control"](control)'},
                                         {'new': 'def '
                                                 'test_phase4_step7_historical_bindings_preserve_assertions(phase4_tools, '
                                                 'phase4_step6_snapshot, phase4_step7_snapshot):\n'
                                                 '    import ast\n'
                                                 '    registry = phase4_tools["PHASE4_STEP7_MIGRATIONS"]\n'
                                                 '    assert set(registry) == '
                                                 '{"tests/unit/test_phase4_contracts.py", '
                                                 '"tests/integration/test_phase4_gates.py"}\n'
                                                 '    assert sorted(len(rows) for rows in registry.values()) '
                                                 '== [5, 7]\n'
                                                 '    for path, rows in registry.items():\n'
                                                 '        '
                                                 'phase4_tools["verify_phase4_step7_test_migration"](path, '
                                                 '(phase4_step6_snapshot / path).read_bytes(), '
                                                 '(phase4_step7_snapshot / path).read_bytes())\n'
                                                 '        for row in rows:\n'
                                                 '            trees = [ast.parse(row[key]) for key in '
                                                 '("old", "new")]\n'
                                                 '            assert trees[0].body[0].name == '
                                                 'trees[1].body[0].name == row["node"]\n'
                                                 '            assertions = [[ast.dump(n) for n in '
                                                 'ast.walk(tree) if isinstance(n, ast.Assert)] for tree in '
                                                 'trees]\n'
                                                 '            assert assertions[0] == assertions[1]',
                                          'node': 'test_phase4_step7_historical_bindings_preserve_assertions',
                                          'old': 'def '
                                                 'test_phase4_step7_historical_bindings_preserve_assertions(phase4_tools, '
                                                 'phase4_step6_snapshot):\n'
                                                 '    import ast\n'
                                                 '    registry = phase4_tools["PHASE4_STEP7_MIGRATIONS"]\n'
                                                 '    assert set(registry) == '
                                                 '{"tests/unit/test_phase4_contracts.py", '
                                                 '"tests/integration/test_phase4_gates.py"}\n'
                                                 '    assert sorted(len(rows) for rows in registry.values()) '
                                                 '== [5, 7]\n'
                                                 '    for path, rows in registry.items():\n'
                                                 '        '
                                                 'phase4_tools["verify_phase4_step7_test_migration"](path, '
                                                 '(phase4_step6_snapshot / path).read_bytes(), (ROOT / '
                                                 'path).read_bytes())\n'
                                                 '        for row in rows:\n'
                                                 '            trees = [ast.parse(row[key]) for key in '
                                                 '("old", "new")]\n'
                                                 '            assert trees[0].body[0].name == '
                                                 'trees[1].body[0].name == row["node"]\n'
                                                 '            assertions = [[ast.dump(n) for n in '
                                                 'ast.walk(tree) if isinstance(n, ast.Assert)] for tree in '
                                                 'trees]\n'
                                                 '            assert assertions[0] == assertions[1]'},
                                         {'new': 'def '
                                                 'test_phase4_step7_historical_guard_rejects_weakening(phase4_tools, '
                                                 'phase4_step6_snapshot, mutation, phase4_step7_snapshot):\n'
                                                 '    path = "tests/integration/test_phase4_gates.py" if '
                                                 'mutation == "config" else '
                                                 '"tests/unit/test_phase4_contracts.py"\n'
                                                 '    before, after = (phase4_step6_snapshot / '
                                                 'path).read_bytes(), (phase4_step7_snapshot / '
                                                 'path).read_bytes()\n'
                                                 '    verify = '
                                                 'phase4_tools["verify_phase4_step7_test_migration"]\n'
                                                 '    verify(path, before, after)\n'
                                                 '    if mutation == "assertion":\n'
                                                 '        needle = b\'    assert control["active_phase"] == '
                                                 '4 and control["active_step"] == 6\\n\'\n'
                                                 '        assert after.count(needle) == 1\n'
                                                 '        after = after.replace(needle, b"    assert '
                                                 'True\\n", 1)\n'
                                                 '    elif mutation == "binding":\n'
                                                 "        needle = b'json.loads((phase4_step6_snapshot / "
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\'\n'
                                                 '        assert needle in after\n'
                                                 '        after = after.replace(needle, '
                                                 'needle.replace(b"phase4_step6_snapshot", b"ROOT"), 1)\n'
                                                 '    elif mutation == "config":\n'
                                                 "        needle = b'else phase4_step6_snapshot if relative "
                                                 '== "config.py" else repo_root\'\n'
                                                 '        assert after.count(needle) == 1\n'
                                                 '        after = after.replace(needle, b"else repo_root", '
                                                 '1)\n'
                                                 '    elif mutation == "shadow":\n'
                                                 '        after += b"\\ndef '
                                                 'test_phase4_step6_fixed_boundary_opens_only_approved_existing_paths():\\n    '
                                                 'assert True\\n"\n'
                                                 '    else:\n'
                                                 '        after += b"\\ndef '
                                                 'test_phase4_step7_bad(value=globals().clear()):\\n    '
                                                 'pass\\n"\n'
                                                 '    with pytest.raises(ValueError):\n'
                                                 '        verify(path, before, after)',
                                          'node': 'test_phase4_step7_historical_guard_rejects_weakening',
                                          'old': 'def '
                                                 'test_phase4_step7_historical_guard_rejects_weakening(phase4_tools, '
                                                 'phase4_step6_snapshot, mutation):\n'
                                                 '    path = "tests/integration/test_phase4_gates.py" if '
                                                 'mutation == "config" else '
                                                 '"tests/unit/test_phase4_contracts.py"\n'
                                                 '    before, after = (phase4_step6_snapshot / '
                                                 'path).read_bytes(), (ROOT / path).read_bytes()\n'
                                                 '    verify = '
                                                 'phase4_tools["verify_phase4_step7_test_migration"]\n'
                                                 '    verify(path, before, after)\n'
                                                 '    if mutation == "assertion":\n'
                                                 '        needle = b\'    assert control["active_phase"] == '
                                                 '4 and control["active_step"] == 6\\n\'\n'
                                                 '        assert after.count(needle) == 1\n'
                                                 '        after = after.replace(needle, b"    assert '
                                                 'True\\n", 1)\n'
                                                 '    elif mutation == "binding":\n'
                                                 "        needle = b'json.loads((phase4_step6_snapshot / "
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\'\n'
                                                 '        assert needle in after\n'
                                                 '        after = after.replace(needle, '
                                                 'needle.replace(b"phase4_step6_snapshot", b"ROOT"), 1)\n'
                                                 '    elif mutation == "config":\n'
                                                 "        needle = b'else phase4_step6_snapshot if relative "
                                                 '== "config.py" else repo_root\'\n'
                                                 '        assert after.count(needle) == 1\n'
                                                 '        after = after.replace(needle, b"else repo_root", '
                                                 '1)\n'
                                                 '    elif mutation == "shadow":\n'
                                                 '        after += b"\\ndef '
                                                 'test_phase4_step6_fixed_boundary_opens_only_approved_existing_paths():\\n    '
                                                 'assert True\\n"\n'
                                                 '    else:\n'
                                                 '        after += b"\\ndef '
                                                 'test_phase4_step7_bad(value=globals().clear()):\\n    '
                                                 'pass\\n"\n'
                                                 '    with pytest.raises(ValueError):\n'
                                                 '        verify(path, before, after)'}]}


def _phase4_step7_files():
    """Read the exact accepted Step 7 Git tree and verify every blob identity."""
    for suffix, expected in (("^{commit}", PHASE4_STEP7_FINAL), ("^{tree}", PHASE4_STEP7_TREE),
                             (":tests", PHASE4_STEP7_TEST_TREE)):
        if git("rev-parse", PHASE4_STEP7_FINAL + suffix).decode().strip() != expected:
            raise ValueError("Pinned Phase 4 Step 7 identity mismatch")
    objects = {}
    for entry in git("ls-tree", "-rz", PHASE4_STEP7_FINAL).split(b"\0"):
        if not entry:
            continue
        metadata, raw_path = entry.split(b"\t", 1)
        mode, kind, oid = metadata.split()
        path = raw_path.decode("utf-8")
        if (mode not in (b"100644", b"100755") or kind != b"blob" or path in objects
                or path.startswith("/") or ".." in path.split("/") or ".git" in path.split("/")):
            raise ValueError("Unsafe pinned Step 7 Git object")
        objects[path] = oid.decode("ascii")
    if len(objects) != 229:
        raise ValueError("Pinned Step 7 must contain exactly 229 files")
    files = {}
    with zipfile.ZipFile(io.BytesIO(git("archive", "--format=zip", PHASE4_STEP7_FINAL))) as archive:
        names = [item.filename for item in archive.infolist() if not item.is_dir()]
        if len(names) != len(objects) or set(names) != set(objects):
            raise ValueError("Pinned Step 7 archive identity mismatch")
        for name in names:
            raw = archive.read(name)
            oid = hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()
            if oid != objects[name]:
                raise ValueError(f"Pinned Step 7 blob mismatch: {name}")
            files[name] = raw
    return MappingProxyType(files)


def phase4_step8_expected_control() -> dict:
    """Actual Step 8 approval is independent of the mutable control document."""
    prior = _phase4_step7_files()
    result = phase4_step7_expected_control()
    result.update({
        "control_version": "1.7", "active_step": 8,
        "approval_date": PHASE4_STEP8_APPROVAL_DATE, "approval_basis": PHASE4_STEP8_APPROVAL,
        "previous_step_commit": PHASE4_STEP7_FINAL,
        "previous_step_tree": PHASE4_STEP7_TREE,
        "previous_step_test_tree": PHASE4_STEP7_TEST_TREE,
        "previous_step_core_tests": 3620, "previous_step_parquet_tests": 3623,
        "previous_step_files_sha256": {p: hashlib.sha256(raw).hexdigest() for p, raw in sorted(prior.items())},
        "permitted_paths": sorted(PHASE4_STEP8_ALLOWED), "new_files_permitted": list(PHASE4_STEP8_NEW),
        "runtime_changes_authorized": True, "schema_changes_authorized": False,
        "runtime_paths_authorized": sorted(p for p in PHASE4_STEP8_ALLOWED if p.startswith("src/") and p.endswith(".py")),
        "schema_paths_authorized": [], "package_resource_copies": PHASE4_STEP8_RESOURCES,
        "package_data_declaration_only": True,
        "step7_historical_binding_nodes": {p: sorted({r["node"] for r in rows})
                                          for p, rows in sorted(PHASE4_STEP8_MIGRATIONS.items())},
    })
    return result


def verify_phase4_step8_control(control: dict, step: int = 8) -> None:
    if type(step) is not int or step != 8 or type(control) is not dict:
        raise ValueError("Unsupported Phase 4 Step 8 stage/control")
    try:
        actual = json.dumps(control, sort_keys=True, ensure_ascii=True, allow_nan=False)
        expected = json.dumps(phase4_step8_expected_control(), sort_keys=True, ensure_ascii=True, allow_nan=False)
    except (TypeError, ValueError) as error:
        raise ValueError("Invalid Phase 4 Step 8 control") from error
    if actual != expected:
        raise ValueError("Phase 4 control differs from the independently approved Step 8 contract")


def verify_phase4_step8_changes(changes: list[tuple[str, str]]) -> None:
    seen = set()
    for status, path in changes:
        if path in seen or path not in PHASE4_STEP8_ALLOWED or status != ("A" if path in PHASE4_STEP8_NEW else "M"):
            raise ValueError(f"Unapproved Phase 4 Step 8 path/operation: {status} {path}")
        seen.add(path)


def _phase4_step8_header(node, path):
    """Allow explicit test parametrization/fixtures, never definition-time effects."""
    for decorator in node.decorator_list:
        if not isinstance(decorator, ast.Call) or ast.unparse(decorator.func) not in {
                "pytest.fixture", "pytest.mark.parametrize"}:
            raise ValueError(f"Unapproved Step 8 test decorator: {path}:{node.name}")
        if ast.unparse(decorator.func) == "pytest.fixture" and not node.name.startswith("phase4_step"):
            raise ValueError("A Step 8 fixture must have an explicit scoped name")
        if any(keyword.arg is None for keyword in decorator.keywords):
            raise ValueError("Decorator expansion is outside the Step 8 contract")
        for value in [*decorator.args, *(keyword.value for keyword in decorator.keywords)]:
            try:
                ast.literal_eval(value)
            except (ValueError, TypeError, SyntaxError) as error:
                raise ValueError("Step 8 decorator arguments must be literal") from error
    clone = ast.parse(ast.unparse(node)).body[0]
    clone.decorator_list = []
    _phase4_preserve_function_header(clone, path)


def _phase4_step8_append_only(before: bytes, after: bytes, path: str) -> None:
    if not after.startswith(before):
        raise ValueError(f"Inherited Step 7 prefix changed: {path}")
    old, new = ast.parse(before), ast.parse(after)
    bindings = set()
    for node in old.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            bindings.add(node.name)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            bindings.update(alias.asname or alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            bindings.update(child.id for target in targets for child in ast.walk(target) if isinstance(child, ast.Name))
    for node in new.body[len(old.body):]:
        if not isinstance(node, ast.FunctionDef) or node.name in bindings:
            raise ValueError(f"Step 8 addition executes, rebinds or shadows inherited source: {path}")
        allowed_snapshot = path == "tests/conftest.py" and node.name == "phase4_step7_snapshot"
        if not allowed_snapshot and not node.name.startswith(("test_phase4_step8_", "phase4_step8_")):
            raise ValueError(f"Step 8 added test/helper is not explicitly scoped: {path}:{node.name}")
        if path == "tests/conftest.py" and node.name != "phase4_step7_snapshot":
            raise ValueError("Only the pinned Step 7 shared fixture is authorized")
        bindings.add(node.name)
        _phase4_step8_header(node, path)


def verify_phase4_step8_test_migration(path: str, before: bytes, after: bytes) -> None:
    prior = _phase4_step7_files()
    if path not in prior or path not in PHASE4_STEP8_ALLOWED or before != prior[path] or not path.startswith("tests/"):
        raise ValueError("Step 8 migration requires the exact named Step 7 source")
    _phase4_step8_check_test_migration(path, before, after)


def _phase4_step8_check_test_migration(path: str, before: bytes, after: bytes) -> None:
    """Check a source already read from the verified Step 7 immutable mapping."""
    expected = before
    for row in PHASE4_STEP8_MIGRATIONS.get(path, []):
        old, new = row["old"].encode(), row["new"].encode()
        if expected.count(old) != 1:
            raise ValueError("Step 7 historical binding is not unique")
        expected = expected.replace(old, new, 1)
    _phase4_step8_append_only(expected, after, path)


def _phase4_step8_preserve_tooling(before: bytes, after: bytes, path: str) -> None:
    """Preserve exact inherited statements using one source-line split per tree."""
    if path == "scripts/release_check.py":
        old = '    return phase4_cli_main() if explicit_phase4 else main()'
        new = ('    explicit_step8 = "--step=8" in argv or any(a == "--step" and b == "8" for a, b in zip(argv, argv[1:]))\n'
               '    if explicit_phase4 and explicit_step8:\n'
               '        return phase4_step8_cli_main()\n' + old)
        # Earlier preserved dispatch functions contain this source too; bind cli_main only.
        parsed = ast.parse(before)
        entry = next(node for node in parsed.body if isinstance(node, ast.FunctionDef) and node.name == "cli_main")
        old_entry = ast.get_source_segment(before.decode(), entry)
        if old_entry.count(old) != 1:
            raise ValueError("Step 7 release dispatcher identity mismatch")
        replacements = [(old_entry, old_entry.replace(old, new, 1))]
    else:
        old = '    if args.phase == 4 and args.step == 7:\n        return phase4_step7_main(step=args.step)\n'
        new = old + '    if args.phase == 4 and args.step == 8:\n        return phase4_step8_main(step=args.step)\n'
        replacements = [(old, new),
                        ('Choose explicit --phase 3 --step 11 or --phase 4 --step 1 or --phase 4 --step 2 or --phase 4 --step 3 or --phase 4 --step 4 or --phase 4 --step 5 or --phase 4 --step 6 or --phase 4 --step 7',
                         'Choose explicit --phase 3 --step 11 or --phase 4 --step 1 or --phase 4 --step 2 or --phase 4 --step 3 or --phase 4 --step 4 or --phase 4 --step 5 or --phase 4 --step 6 or --phase 4 --step 7 or --phase 4 --step 8')]
    expected = before
    for old, new in replacements:
        if expected.count(old.encode()) != 1:
            raise ValueError(f"Historical dispatcher identity mismatch: {path}")
        expected = expected.replace(old.encode(), new.encode(), 1)
    trees = [ast.parse(expected), ast.parse(after)]
    lines = [expected.splitlines(keepends=True), after.splitlines(keepends=True)]
    def segment(index, node):
        if node.lineno == node.end_lineno:
            return lines[index][node.lineno - 1][node.col_offset:node.end_col_offset]
        return (lines[index][node.lineno - 1][node.col_offset:]
                + b"".join(lines[index][node.lineno:node.end_lineno - 1])
                + lines[index][node.end_lineno - 1][:node.end_col_offset])
    def entry_guard(node):
        return isinstance(node, ast.If) and isinstance(node.test, ast.Compare) and "__name__" in ast.unparse(node.test)
    guards = [n for n in trees[1].body if entry_guard(n)]
    expected_guard = ast.parse('if __name__ == "__main__":\n    raise SystemExit(cli_main())').body[0]
    if len(guards) != 1 or ast.dump(guards[0]) != ast.dump(expected_guard):
        raise ValueError(f"Unapproved Step 8 maintainer entrypoint: {path}")
    historical = [n for n in trees[0].body if not entry_guard(n)]
    current = [n for n in trees[1].body if not entry_guard(n)]
    old_entries = [(segment(0, n), ast.dump(n)) for n in historical]
    cursor = 0
    for node in current:
        if cursor < len(old_entries) and (segment(1, node), ast.dump(node)) == old_entries[cursor]:
            cursor += 1
            continue
        if isinstance(node, ast.FunctionDef) and (node.name == "_phase4_step7_files" or node.name.startswith(
                ("phase4_step8_", "_phase4_step8_", "verify_phase4_step8_", "audit_phase4_step8"))):
            _phase4_preserve_function_header(node, path)
            continue
        if isinstance(node, ast.Assign) and all(isinstance(target, ast.Name) and target.id.startswith(
                ("PHASE4_STEP8_", "PHASE4_STEP7_")) for target in node.targets):
            try:
                ast.literal_eval(node.value)
            except (ValueError, TypeError, SyntaxError) as error:
                raise ValueError(f"Nonliteral added Step 8 maintainer constant: {path}") from error
            continue
        raise ValueError(f"Unapproved Step 8 maintainer addition: {path}")
    if cursor != len(historical):
        raise ValueError(f"Inherited Step 7 maintainer statement changed: {path}")
    def binding_counts(tree):
        counts = {}
        for node in tree.body:
            names = []
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                names = [node.name]
            elif isinstance(node, (ast.Assign, ast.AnnAssign)):
                targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                names = [child.id for target in targets for child in ast.walk(target) if isinstance(child, ast.Name)]
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                names = [alias.asname or alias.name.split(".")[0] for alias in node.names]
            for name in names:
                counts[name] = counts.get(name, 0) + 1
        return counts
    inherited_counts = binding_counts(trees[0])
    for name, count in binding_counts(trees[1]).items():
        if count > inherited_counts.get(name, 1):
            raise ValueError(f"Duplicate Step 8 maintainer binding: {path}:{name}")


def verify_phase4_step8_snapshot(root: Path = ROOT) -> dict:
    prior = _phase4_step7_files()
    for path, raw in prior.items():
        target = root / path
        if not target.is_file() or target.is_symlink():
            raise ValueError(f"Missing or aliased inherited Step 7 file: {path}")
        current = target.read_bytes()
        if path not in PHASE4_STEP8_ALLOWED and current != raw:
            raise ValueError(f"Protected Step 7 bytes changed: {path}")
        if path.startswith("tests/") and path in PHASE4_STEP8_ALLOWED:
            _phase4_step8_check_test_migration(path, raw, current)
        elif path.startswith("scripts/") and path in PHASE4_STEP8_ALLOWED:
            _phase4_step8_preserve_tooling(raw, current, path)
        elif path in {"docs/architecture.md", "docs/theory_traceability.md", "PHASE_4_DECISIONS.md"}:
            if not current.startswith(raw):
                raise ValueError(f"Step 7 historical documentation prefix changed: {path}")
    if not (root / "docs/cli.md").read_bytes().endswith(prior["docs/cli.md"]):
        raise ValueError("Step 8 CLI documentation must retain the historical notes verbatim")
    phase4_step8_resources(root, prior)
    for path in ("src/recursive_integrity_toolkit/config.py",):
        _phase4_step8_preserve_runtime(prior[path], (root / path).read_bytes(), path)
    actual_modules = {p.relative_to(root).as_posix() for p in (root / "src/recursive_integrity_toolkit").rglob("*.py")}
    expected_modules = {p for p in prior if p.startswith("src/") and p.endswith(".py")}
    if actual_modules != expected_modules or len(actual_modules) != 40:
        raise ValueError("Step 8 cannot change the runtime module set")
    if {p.name for p in (root / "schemas").iterdir()} != {Path(p).name for p in prior if p.startswith("schemas/")}:
        raise ValueError("Step 8 cannot change the schema set")
    if hashlib.sha256((root / "PHASE_4_PLAN.md").read_bytes()).hexdigest() != PHASE4_PLAN_SHA256:
        raise ValueError("Approved Phase 4 plan changed")
    verify_phase4_step8_control(json.loads((root / "PHASE_4_BASELINE.json").read_text(encoding="utf-8")))
    decisions = (root / "PHASE_4_DECISIONS.md").read_text(encoding="utf-8")
    if PHASE4_STEP8_APPROVAL not in decisions or PHASE4_STEP7_FINAL not in decisions:
        raise ValueError("Actual Step 8 authorization or Step 7 evidence anchor missing")
    if any((root / name).exists() for name in PHASE4_FORBIDDEN_OUTPUTS):
        raise ValueError("Step 8 cannot create Phase 4 completion records or audit outputs")
    import runpy
    checker = runpy.run_path(str(root / "scripts/check_traceability.py"), run_name="phase4_step8_renderer_boundary")
    checker["phase4_step8_cli_boundary"](root)
    schema_bytes = (root / "schemas/report.schema.json").read_bytes()
    if hashlib.sha256(schema_bytes).hexdigest() != PHASE4_STEP2_REPORT_SCHEMA_SHA256:
        raise ValueError("Step 8 report schema differs from its independently reviewed bytes")
    schema = json.loads(schema_bytes)
    if (schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema"
            or schema.get("type") != "object" or schema.get("additionalProperties") is not False):
        raise ValueError("Step 8 report schema dialect/closed root mismatch")
    return {"package_modules": 40, "frozen_runtime_modules": 38, "frozen_schemas": 5,
            "hero_files_unchanged": 6, "historical_phase3_migrated_nodes": 16,
            "phase_complete": False, "result_contracts_enabled": True,
            "adapters_enabled": True, "privacy_views_enabled": True, "renderers_enabled": True, "output_publication_enabled": True, "cli_analysis_enabled": True, "comparison_enabled": True, "example_enabled": True, "packaged_resources": 7}


def audit_phase4_step8(step: int = 8) -> dict:
    verify_phase4_step8_control(json.loads((ROOT / "PHASE_4_BASELINE.json").read_text(encoding="utf-8")), step)
    result = {"phase": 4, "active_step": step, **verify_phase4_step8_snapshot(),
              "phase0_hashes_verified": 16, "publication_authorized": False}
    print(json.dumps(result, indent=2))
    return result


def audit_phase4_step8_diff(step: int = 8) -> dict:
    if type(step) is not int or step != 8:
        raise ValueError("Unsupported Phase 4 Step 8 stage")
    _phase4_step7_files()
    subprocess.run(["git", "-C", str(ROOT), "merge-base", "--is-ancestor", PHASE4_STEP7_FINAL, "HEAD"], check=True)
    raw = git("diff", "--name-status", "--no-renames", "-z", PHASE4_STEP7_FINAL, "--").split(b"\0")
    raw = [part.decode("utf-8") for part in raw if part]
    if len(raw) % 2:
        raise ValueError("Malformed Step 8 Git difference records")
    changes = list(zip(raw[::2], raw[1::2]))
    changes.extend(("A", p.decode()) for p in git("ls-files", "--others", "--exclude-standard", "-z").split(b"\0") if p)
    verify_phase4_step8_changes(changes)
    result = {"previous_step_commit": PHASE4_STEP7_FINAL, "changed_files": len(changes),
              "changes": changes, "step": 8, "scope": "PASS"}
    print(json.dumps(result, indent=2))
    return result


def phase4_step8_baseline_evidence(output: Path) -> dict:
    """Reconcile all inherited identities, including the accepted Step 7 suite."""
    output.mkdir(parents=True, exist_ok=True)
    inherited = phase4_step7_baseline_evidence(output / "phase4-step7-inherited")
    with tempfile.TemporaryDirectory(prefix="rit-p4-step7-identities-") as temp:
        baseline = Path(temp)
        for name, raw in _phase4_step7_files().items():
            target = baseline / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(raw)
        old, old_log = _collect(baseline)
    current, current_log = _collect(ROOT)
    expected = 3623 if os.environ.get("RIT_TEST_PARQUET") == "1" else 3620
    if len(old) != expected or set(old) - set(current):
        raise ValueError("Accepted Phase 4 Step 7 test identities were lost")
    result = {"baseline_commit": PHASE4_STEP7_FINAL, "baseline_test_tree": PHASE4_STEP7_TEST_TREE,
              "baseline_nodeids": old, "current_nodeids": current, "missing_nodeids": [],
              "baseline_tests": len(old), "current_tests": len(current), "inherited": inherited,
              "nodeids_sha256": hashlib.sha256(("\n".join(old)+"\n").encode()).hexdigest()}
    (output / "phase4_step8_test_identity_manifest.json").write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    (output / "phase4-step7-collection.log").write_text(old_log, encoding="utf-8")
    (output / "phase4-step8-collection.log").write_text(current_log, encoding="utf-8")
    print(json.dumps({k: result[k] for k in ("baseline_tests", "current_tests", "missing_nodeids")}, indent=2))
    return result


def phase4_step8_candidate(output: Path, step: int = 8) -> None:
    """Build tested Step 8 intermediate evidence without declaring Phase 4 complete."""
    if os.environ.get("RIT_TEST_PARQUET") != "1" or importlib.util.find_spec("pyarrow") is None:
        raise ValueError("Step 8 candidate evidence requires RIT_TEST_PARQUET=1 and real PyArrow")
    output.mkdir(parents=True, exist_ok=True)
    result = audit_phase4_step8(step)
    result["diff"] = audit_phase4_step8_diff(step)
    if git("status", "--porcelain").strip():
        raise ValueError("Step 8 candidate archive requires committed, clean source")
    result["core"] = verify_junit(output / "core.xml", minimum=3620)
    result["parquet"] = verify_junit(output / "parquet.xml", require_parquet=True, minimum=3623)
    result["core_math_measurements"] = verify_step10_evidence(output / "core.xml", output / "phase4-step8-core-observations.json")
    result["parquet_math_measurements"] = verify_step10_evidence(output / "parquet.xml", output / "phase4-step8-parquet-observations.json")
    identity = phase4_step8_baseline_evidence(output)
    result["test_identity"] = {k: identity[k] for k in ("baseline_tests", "current_tests", "nodeids_sha256")}
    expected = set()
    for node in identity["current_nodeids"]:
        base, bracket, parameter = node.partition("[")
        owner, name = base.rsplit("::", 1)
        expected.add((owner.removesuffix(".py").replace("/", ".").replace("::", "."), name + bracket + parameter))
    for name, parquet in (("core.xml", False), ("parquet.xml", True)):
        cases = {(c.get("classname", ""), c.get("name", "")) for c in ET.parse(output / name).getroot().iter("testcase")}
        target = expected if parquet else {c for c in expected if c[1] not in PARQUET_CASES}
        if cases != target:
            raise ValueError(f"Step 8 JUnit does not execute the entire current suite: {name}")
    wheel, sdist = phase4_step8_distributions(output / "dist")
    smoke_installed(wheel)
    smoke_installed_duplicates(wheel)
    phase4_step2_installed_contract_smoke(wheel)
    phase4_step3_installed_assembly_smoke(wheel)
    phase4_step4_installed_privacy_smoke(wheel)
    phase4_step5_installed_renderers_smoke(wheel)
    phase4_step6_installed_publication_smoke(wheel)
    phase4_step7_installed_cli_smoke(wheel)
    phase4_step8_installed_example_smoke(wheel)
    phase4_step8_sdist_smoke(sdist)
    archive = output / "recursive-integrity-toolkit-phase4-step8-candidate.zip"
    subprocess.run(["git", "-C", str(ROOT), "archive", "--format=zip", "--prefix=recursive-integrity-toolkit/", "HEAD", "-o", str(archive.resolve())], check=True)
    tracked = {p for p in git("ls-files", "-z").decode().split("\0") if p}
    with zipfile.ZipFile(archive) as zipped:
        entries = [item.filename for item in zipped.infolist() if not item.is_dir()]
        prefix = "recursive-integrity-toolkit/"
        if (len(entries) != len(set(entries)) or any(not name.startswith(prefix) for name in entries)):
            raise ValueError("Step 8 source archive has duplicate or unprefixed entries")
        names = {name.removeprefix(prefix) for name in entries}
        if names != tracked or len(tracked) != 236 or len(entries) != 236:
            raise ValueError("Step 8 source archive file set mismatch")
        for name in names:
            if zipped.read("recursive-integrity-toolkit/"+name) != (ROOT / name).read_bytes():
                raise ValueError(f"Step 8 source archive byte mismatch: {name}")
    result.update({"commit": git("rev-parse", "HEAD").decode().strip(),
                   "tree": git("rev-parse", "HEAD^{tree}").decode().strip(),
                   "source_archive": archive.name, "tracked_files": len(tracked),
                   "python": sys.version, "platform": sys.platform,
                   "versions": {name: importlib.metadata.version(name) for name in ("numpy", "pandas", "pytest")}})
    (output / "phase4_step8_execution_metadata.json").write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    (output / "phase4_step8_repository_files.sha256").write_text("".join(f"{hashlib.sha256((ROOT/name).read_bytes()).hexdigest()}  {name}\n" for name in sorted(tracked)), encoding="utf-8")
    paths = sorted(p for p in output.rglob("*") if p.is_file() and p.name != "phase4_step8_artifacts.sha256")
    (output / "phase4_step8_artifacts.sha256").write_text("".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(output).as_posix()}\n" for p in paths), encoding="utf-8")
    print(f"Phase 4 Step 8 candidate: {len(tracked)} source files verified; Phase 4 remains incomplete.")


def phase4_step8_cli_main() -> int:
    parser = argparse.ArgumentParser(description="Phase 4 Step 8 maintainer gate")
    parser.add_argument("--phase", type=int, choices=(4,), required=True)
    parser.add_argument("--step", type=int, choices=(8,), required=True)
    parser.add_argument("--diff", action="store_true")
    parser.add_argument("--junit", type=Path)
    parser.add_argument("--require-parquet", action="store_true")
    parser.add_argument("--minimum-tests", type=int, default=1)
    parser.add_argument("--baseline-evidence", type=Path)
    parser.add_argument("--dist", type=Path)
    parser.add_argument("--smoke-wheel", type=Path)
    parser.add_argument("--candidate", type=Path)
    parser.add_argument("--delivery", type=Path)
    args = parser.parse_args()
    if args.delivery is not None:
        raise ValueError("Phase 4 Step 8 cannot certify a final phase delivery")
    if args.junit is not None:
        verify_junit(args.junit, require_parquet=args.require_parquet, minimum=args.minimum_tests)
    elif args.baseline_evidence is not None:
        phase4_step8_baseline_evidence(args.baseline_evidence)
    elif args.dist is not None:
        audit_phase4_step8(args.step)
        wheel, sdist = phase4_step8_distributions(args.dist)
        smoke_installed(wheel)
        smoke_installed_duplicates(wheel)
        phase4_step2_installed_contract_smoke(wheel)
        phase4_step3_installed_assembly_smoke(wheel)
        phase4_step4_installed_privacy_smoke(wheel)
        phase4_step5_installed_renderers_smoke(wheel)
        phase4_step6_installed_publication_smoke(wheel)
        phase4_step7_installed_cli_smoke(wheel)
        phase4_step8_installed_example_smoke(wheel)
        phase4_step8_sdist_smoke(sdist)
    elif args.smoke_wheel is not None:
        smoke_installed(args.smoke_wheel)
    elif args.candidate is not None:
        phase4_step8_candidate(args.candidate, args.step)
    else:
        audit_phase4_step8(args.step)
        if args.diff:
            audit_phase4_step8_diff(args.step)
    return 0


def _phase4_step8_preserve_runtime(before: bytes, after: bytes, path: str) -> None:
    """Allow ownership-header maintenance and byte-exact additive helpers only."""
    try:
        old, new = ast.parse(before), ast.parse(after)
    except (SyntaxError, UnicodeError, ValueError) as error:
        raise ValueError("Output helper source cannot be inspected") from error
    if not ast.get_docstring(old) or not ast.get_docstring(new):
        raise ValueError("Output helper ownership documentation is required")
    old_tail = b"".join(before.splitlines(keepends=True)[old.body[0].end_lineno:])
    new_tail = b"".join(after.splitlines(keepends=True)[new.body[0].end_lineno:])
    if not new_tail.startswith(old_tail):
        raise ValueError(f"Inherited input/diagnostic bytes changed: {path}")


def phase4_step8_resources(root: Path, prior: dict) -> None:
    """Exact approved copies, with no build/dependency/version change."""
    for destination, source in PHASE4_STEP8_RESOURCES.items():
        path = root / destination
        if not path.is_file() or path.is_symlink() or path.read_bytes() != (root / source).read_bytes():
            raise ValueError("Step 8 packaged resource differs from its canonical source")
    resource_root = root / "src/recursive_integrity_toolkit/data"
    if any(p.is_symlink() for p in resource_root.rglob("*")) or {p.relative_to(root).as_posix() for p in resource_root.rglob("*") if p.is_file()} != set(PHASE4_STEP8_RESOURCES):
        raise ValueError("Step 8 packaged resource set differs from its exact allowlist")
    before = prior["pyproject.toml"]
    marker = b'include = ["recursive_integrity_toolkit*"]\n'
    if before.count(marker) != 1 or (root / "pyproject.toml").read_bytes() != before.replace(marker, marker + PHASE4_STEP8_PACKAGING.encode(), 1):
        raise ValueError("Step 8 packaging may add only the exact package-data declaration")


def phase4_step8_distributions(directory: Path, expected_version: str = "0.1.0.dev2"):
    wheel, sdist = verify_distributions(directory, expected_version=expected_version)
    with zipfile.ZipFile(wheel) as archive:
        actual = {name for name in archive.namelist() if name.startswith("recursive_integrity_toolkit/data/") and not name.endswith("/")}
        if actual != {path.removeprefix("src/") for path in PHASE4_STEP8_RESOURCES}:
            raise ValueError("Wheel resource inventory differs")
        for destination, source in PHASE4_STEP8_RESOURCES.items():
            if archive.read(destination.removeprefix("src/")) != (ROOT / source).read_bytes():
                raise ValueError("Wheel resource bytes differ")
    with tarfile.open(sdist, "r:gz") as archive:
        root = next(iter({m.name.split("/")[0] for m in archive.getmembers()}))
        for destination, source in PHASE4_STEP8_RESOURCES.items():
            member = archive.getmember(root + "/" + destination)
            if not member.isfile() or archive.extractfile(member).read() != (ROOT / source).read_bytes():
                raise ValueError("Sdist resource bytes differ")
    print("Step 8 wheel/sdist: seven exact canonical resources: PASS")
    return wheel, sdist



def phase4_step8_example_program() -> str:
    """Independent installed acceptance, using frozen section 8 Hero values."""
    return r'''import hashlib, importlib.abc, json, socket, sys, urllib.request
from pathlib import Path
sys.path.insert(0,sys.argv[1])
import recursive_integrity_toolkit as package
assert Path(package.__file__).resolve().is_relative_to(Path(sys.argv[1]).resolve())
assert not Path(package.__file__).resolve().is_relative_to(Path(sys.argv[3]).resolve())
import numpy,pandas
from importlib.resources import files
expected=json.loads(sys.argv[4]);resources=files('recursive_integrity_toolkit')
for relative,digest in expected.items():
 assert hashlib.sha256(resources.joinpath(*relative.split('/')).read_bytes()).hexdigest()==digest
class NoOptional(importlib.abc.MetaPathFinder):
 def find_spec(self,fullname,path=None,target=None):
  if fullname.split('.')[0]=='pyarrow':raise AssertionError('Hero requires no optional dependency')
sys.meta_path.insert(0,NoOptional())
def deny(*args,**kwargs):raise AssertionError('network forbidden')
socket.socket=deny;socket.getaddrinfo=deny;urllib.request.urlopen=deny
from recursive_integrity_toolkit.cli import main
work=Path(sys.argv[2]);target=work/'example'
assert main(['example','--out',str(target)])==0
report=json.loads((target/'reports/report.json').read_bytes())
assert report['run']['command']=='rit example' and report['run']['run_status']=='complete'
assert report['observability']['maximum_level']==4
assert report['capabilities']==report['observability']['capabilities']
support=report['derived_metrics']['support'];diversity=report['derived_metrics']['diversity']
assert [support['by_version'][v]['support_size']['value'] for v in ('v1','v2')]==[8,5]
assert [diversity['by_version'][v]['gini_simpson_diversity']['value'] for v in ('v1','v2')]==[0.875,0.75]
assert support['support_delta']['value']==-3 and support['support_retention_ratio']['value']==0.625
assert support['extinct_states']['value']==['battery','lizard','turtle']
assert diversity['gini_simpson_diversity_delta']['value']==-0.125
assert report['derived_metrics']['provenance']['source_type_shares']['value']=={'human':0.5,'synthetic':0.5,'mixed':0.0,'sensor':0.0,'unknown':0.0}
assert report['derived_metrics']['provenance']['missing_provenance_share']['value']==0.0
for name in ('provenance_row_coverage','provenance_required_field_coverage','grounding_field_coverage'):
 assert report['observed_facts']['provenance'][name]['value']==1.0
 assert report['observed_facts']['provenance'][name]['scope']['dataset_versions']==['v2']
assert [report['derived_metrics']['closure_exposure']['direct'][n]['value'] for n in ('lower_bound','upper_bound','interval_width')]==[0.5,0.5,0]
assert report['capabilities']['lineage']['execution_status']=='deferred'
assert report['capabilities']['dataset_longitudinal']['execution_status']=='partial'
assert report['simulations']=={} and report['errors']==[]
assert {'model_performance_decline','causal_ancestor_effect','universal_integrity','universal_collapse_prediction'} <= {x['conclusion'] for x in report['unavailable_conclusions']}
import jsonschema
jsonschema.Draft202012Validator(json.loads(resources.joinpath('data','report.schema.json').read_bytes())).validate(report)
assert (target/'reports/report.md').read_text(encoding='utf-8').startswith('# Recursive Integrity Audit Report')
before={p:p.read_bytes() for p in target.rglob('*') if p.is_file()}
assert main(['example','--out',str(target)])==1
assert all(p.read_bytes()==raw for p,raw in before.items())
assert main(['example','--out',str(work/'redacted'),'--redacted'])==0
redacted=json.loads((work/'redacted/reports/report.json').read_bytes())
assert redacted['derived_metrics']['support']['support_delta']['value']==-3
assert redacted['run']['redacted_mode'] is True and redacted['simulations']=={}
assert str(work) not in (work/'redacted/reports/report.json').read_text(encoding='utf-8')
for relative,digest in expected.items():
 assert hashlib.sha256(resources.joinpath(*relative.split('/')).read_bytes()).hexdigest()==digest
for p in (target/'inputs').iterdir():
 assert p.read_bytes()==resources.joinpath('data','hero',p.name).read_bytes()
print('installed Step 8: hand-counted Hero, local schema, exact resources, core-only, standard/redacted, no overwrite, blocked network: PASS')
'''


def phase4_step8_installed_example_smoke(wheel: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="rit-p4-step8-wheel-") as temporary:
        work = Path(temporary)
        target = work / "installed"
        subprocess.run([sys.executable, "-m", "pip", "install", "--no-index", "--no-deps", "--target", str(target), str(wheel.resolve())], cwd=work, check=True)
        hashes = {destination.removeprefix("src/recursive_integrity_toolkit/"): hashlib.sha256((ROOT/source).read_bytes()).hexdigest() for destination,source in PHASE4_STEP8_RESOURCES.items()}
        subprocess.run([sys.executable, "-I", "-c", phase4_step8_example_program(), str(target), str(work), str(ROOT), json.dumps(hashes)], cwd=work, check=True)


def phase4_step8_sdist_smoke(sdist: Path) -> None:
    """Extract regular sdist members and audit without build/download operations."""
    with tempfile.TemporaryDirectory(prefix="rit-p4-step8-sdist-") as temporary:
        work = Path(temporary)
        extracted = work / "source"
        with tarfile.open(sdist, "r:gz") as archive:
            roots = {m.name.split("/")[0] for m in archive.getmembers()}
            if len(roots) != 1:
                raise ValueError("Sdist needs exactly one root")
            for member in archive.getmembers():
                if member.isdir():
                    continue
                if (not member.isfile() or member.name.startswith("/") or ".." in member.name.split("/") or "\\" in member.name):
                    raise ValueError("Unsafe sdist member")
                target = extracted / member.name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(archive.extractfile(member).read())
        source = extracted / next(iter(roots)) / "src"
        hashes = {destination.removeprefix("src/recursive_integrity_toolkit/"): hashlib.sha256((ROOT/original).read_bytes()).hexdigest() for destination,original in PHASE4_STEP8_RESOURCES.items()}
        subprocess.run([sys.executable, "-I", "-c", phase4_step8_example_program(), str(source), str(work), str(ROOT), json.dumps(hashes)], cwd=work, check=True)



# Phase 4 Step 9: independently authored report oracles and adversarial integration.


PHASE4_STEP8_FINAL = '63e347a785838b64a9c32e636ea48c664458cee4'


PHASE4_STEP8_TREE = '3ac450b5f67cad738849de18601999fefee98f63'


PHASE4_STEP8_TEST_TREE = 'ddaaab24d83080b7c1a27229c15e6e4a3f5b3cd8'


PHASE4_STEP9_APPROVAL = 'Phase 4  **Step 9**  开始'


PHASE4_STEP9_APPROVAL_DATE = '2026-09-22'


PHASE4_STEP9_NEW = ('tests/golden/phase4_hero_redacted.json',
 'tests/golden/phase4_hero_redacted.md',
 'tests/golden/phase4_hero_report.json',
 'tests/golden/phase4_hero_report.md',
 'tests/golden/phase4_report_cases.md',
 'tests/golden/phase4_report_expected.json',
 'tests/golden/test_phase4_reports.py')


PHASE4_STEP9_ALLOWED = {'.github/workflows/ci.yml',
 '.github/workflows/golden.yml',
 '.github/workflows/release.yml',
 '.github/workflows/security.yml',
 'PHASE_4_BASELINE.json',
 'PHASE_4_DECISIONS.md',
 'docs/architecture.md',
 'docs/theory_traceability.md',
 'scripts/build_golden.py',
 'scripts/check_spec_consistency.py',
 'scripts/check_traceability.py',
 'scripts/normalize_golden.py',
 'scripts/release_check.py',
 'tests/conftest.py',
 'tests/golden/README.md',
 'tests/golden/phase4_hero_redacted.json',
 'tests/golden/phase4_hero_redacted.md',
 'tests/golden/phase4_hero_report.json',
 'tests/golden/phase4_hero_report.md',
 'tests/golden/phase4_report_cases.md',
 'tests/golden/phase4_report_expected.json',
 'tests/golden/test_phase4_reports.py',
 'tests/integration/test_ci_workflows.py',
 'tests/integration/test_hero_end_to_end.py',
 'tests/integration/test_hero_structure.py',
 'tests/integration/test_license_notices.py',
 'tests/integration/test_no_algorithms.py',
 'tests/integration/test_no_network.py',
 'tests/integration/test_optional_dependency.py',
 'tests/integration/test_owner_ids.py',
 'tests/integration/test_package_import.py',
 'tests/integration/test_package_install.py',
 'tests/integration/test_partial_lineage_report.py',
 'tests/integration/test_partial_provenance_report.py',
 'tests/integration/test_phase4_cli.py',
 'tests/integration/test_phase4_gates.py',
 'tests/integration/test_prohibited_structure.py',
 'tests/integration/test_repository_structure.py',
 'tests/integration/test_schema_json.py',
 'tests/unit/test_phase4_contracts.py'}


PHASE4_STEP9_MIGRATIONS = {'tests/integration/test_phase4_gates.py': [{'new': 'def '
                                                    'test_phase4_step8_current_workflows_preserve_matrix_and_use_active_dispatch(repo_root, '
                                                    'phase4_step8_snapshot):\n'
                                                    '    repo_root = phase4_step8_snapshot\n'
                                                    '    names = {"ci.yml", "golden.yml", '
                                                    '"security.yml", "release.yml"}\n'
                                                    '    root = repo_root / ".github/workflows"\n'
                                                    '    expected_timeouts = {"ci.yml": [60, 20], '
                                                    '"golden.yml": [15], "security.yml": [20], '
                                                    '"release.yml": [40]}\n'
                                                    '    assert {path.name for path in '
                                                    'root.glob("*.yml")} == names\n'
                                                    '    for name in sorted(names):\n'
                                                    '        text = (root / '
                                                    'name).read_text(encoding="utf-8")\n'
                                                    '        assert [int(line.split(":", 1)[1]) '
                                                    'for line in text.splitlines()\n'
                                                    '                if '
                                                    'line.strip().startswith("timeout-minutes:")] '
                                                    '== expected_timeouts[name]\n'
                                                    '        assert "Phase 4 Step 8" in text, '
                                                    'name\n'
                                                    '        assert "--phase 4 --step 8" in text, '
                                                    'name\n'
                                                    '        for older in ("--phase 4 --step 7", '
                                                    '"--phase 4 --step 6", "--phase 4 --step 5", '
                                                    '"--phase 4 --step 4", "--phase 4 --step 3", '
                                                    '"--phase 4 --step 2", "--phase 4 --step 1", '
                                                    '"--phase 3 --step 11"):\n'
                                                    '            assert older not in text, (name, '
                                                    'older)\n'
                                                    '        assert "permissions:\\n  contents: '
                                                    'read" in text\n'
                                                    '        assert "persist-credentials: false" '
                                                    'in text\n'
                                                    '        assert "timeout-minutes:" in text and '
                                                    '"set -euo pipefail" in text\n'
                                                    '        assert "actions/upload-artifact@v4" '
                                                    'in text and "if-no-files-found: error" in '
                                                    'text\n'
                                                    '        for line in text.splitlines():\n'
                                                    '            if "python '
                                                    'scripts/release_check.py" in line:\n'
                                                    '                assert "--phase 4 --step 8" '
                                                    'in line, (name, line)\n'
                                                    '        for forbidden in '
                                                    '("continue-on-error:", "|| true", "contents: '
                                                    'write", "id-token: write", "twine upload", '
                                                    '"git push"):\n'
                                                    '            assert forbidden not in text, '
                                                    '(name, forbidden)\n'
                                                    '    ci = (root / '
                                                    '"ci.yml").read_text(encoding="utf-8")\n'
                                                    "    for required in ('os: [ubuntu-latest, "
                                                    'windows-latest]\', \'python-version: ["3.11", '
                                                    '"3.12"]\',\n'
                                                    "                     'dependencies: [current, "
                                                    'minimum]\', \'"numpy==2.0.0" '
                                                    '"pandas==2.2.2"\',\n'
                                                    "                     'RIT_TEST_PARQUET: "
                                                    '"0"\', \'RIT_TEST_PARQUET: "1"\', '
                                                    "'--require-parquet',\n"
                                                    "                     '--baseline-evidence', "
                                                    "'python -m pip check',\n"
                                                    "                     '--minimum-tests 3620', "
                                                    "'--minimum-tests 3623',\n"
                                                    '                     "find_spec(\'pyarrow\') '
                                                    'is None", \'import pyarrow\'):\n'
                                                    '        assert required in ci\n'
                                                    '    assert ci.count("python -m pytest -p '
                                                    'no:cacheprovider -q --junitxml=") == 2\n'
                                                    '    assert " -k " not in ci\n'
                                                    '    golden = (root / '
                                                    '"golden.yml").read_text(encoding="utf-8")\n'
                                                    '    for required in '
                                                    '("tests/golden/test_phase3_math.py", '
                                                    '"tests/integration/test_hero_structure.py",\n'
                                                    '                     '
                                                    '"tests/integration/test_phase3_metric_pipeline.py", '
                                                    '"tests/integration/test_hero_end_to_end.py"):\n'
                                                    '        assert required in golden\n'
                                                    '    security = (root / '
                                                    '"security.yml").read_text(encoding="utf-8")\n'
                                                    '    for required in '
                                                    "('tests/integration/test_no_network.py', "
                                                    "'tests/integration/test_optional_dependency.py',\n"
                                                    '                     '
                                                    "'tests/unit/test_PR012_evidence_classes.py', "
                                                    "'tests/unit/test_PR013_report_schema.py',\n"
                                                    '                     '
                                                    "'tests/unit/test_PR014_unavailable.py', "
                                                    "'tests/unit/test_PR015_redaction.py',\n"
                                                    '                     '
                                                    "'tests/unit/test_PR016_determinism.py', "
                                                    "'tests/unit/test_PR018_language.py',\n"
                                                    '                     '
                                                    "'tests/integration/test_partial_provenance_report.py',\n"
                                                    '                     '
                                                    "'tests/integration/test_partial_lineage_report.py',\n"
                                                    '                     '
                                                    "'tests/integration/test_phase4_cli.py', "
                                                    "'tests/unit/test_phase4_output_safety.py', "
                                                    "'tests/unit/test_phase4_contracts.py', "
                                                    "'tests/integration/test_phase4_gates.py'):\n"
                                                    '        assert required in security\n'
                                                    '    release = (root / '
                                                    '"release.yml").read_text(encoding="utf-8")\n'
                                                    '    assert "python -m build" in release and '
                                                    '"python -m twine check --strict" in release\n'
                                                    '    assert "--dist" in release and '
                                                    '"--candidate" in release\n'
                                                    '    assert "--delivery" not in release\n'
                                                    '    assert '
                                                    '"recursive-integrity-toolkit-phase4-step8-candidate" '
                                                    'in release\n'
                                                    '    assert "rit-phase4-step4" not in release\n'
                                                    '    assert "--minimum-tests 3620" in release '
                                                    'and "--minimum-tests 3623" in release\n'
                                                    '    assert release.count("python -m pytest -p '
                                                    'no:cacheprovider -q --junitxml=") == 2',
                                             'node': 'test_phase4_step8_current_workflows_preserve_matrix_and_use_active_dispatch',
                                             'old': 'def '
                                                    'test_phase4_step8_current_workflows_preserve_matrix_and_use_active_dispatch(repo_root):\n'
                                                    '    names = {"ci.yml", "golden.yml", '
                                                    '"security.yml", "release.yml"}\n'
                                                    '    root = repo_root / ".github/workflows"\n'
                                                    '    expected_timeouts = {"ci.yml": [60, 20], '
                                                    '"golden.yml": [15], "security.yml": [20], '
                                                    '"release.yml": [40]}\n'
                                                    '    assert {path.name for path in '
                                                    'root.glob("*.yml")} == names\n'
                                                    '    for name in sorted(names):\n'
                                                    '        text = (root / '
                                                    'name).read_text(encoding="utf-8")\n'
                                                    '        assert [int(line.split(":", 1)[1]) '
                                                    'for line in text.splitlines()\n'
                                                    '                if '
                                                    'line.strip().startswith("timeout-minutes:")] '
                                                    '== expected_timeouts[name]\n'
                                                    '        assert "Phase 4 Step 8" in text, '
                                                    'name\n'
                                                    '        assert "--phase 4 --step 8" in text, '
                                                    'name\n'
                                                    '        for older in ("--phase 4 --step 7", '
                                                    '"--phase 4 --step 6", "--phase 4 --step 5", '
                                                    '"--phase 4 --step 4", "--phase 4 --step 3", '
                                                    '"--phase 4 --step 2", "--phase 4 --step 1", '
                                                    '"--phase 3 --step 11"):\n'
                                                    '            assert older not in text, (name, '
                                                    'older)\n'
                                                    '        assert "permissions:\\n  contents: '
                                                    'read" in text\n'
                                                    '        assert "persist-credentials: false" '
                                                    'in text\n'
                                                    '        assert "timeout-minutes:" in text and '
                                                    '"set -euo pipefail" in text\n'
                                                    '        assert "actions/upload-artifact@v4" '
                                                    'in text and "if-no-files-found: error" in '
                                                    'text\n'
                                                    '        for line in text.splitlines():\n'
                                                    '            if "python '
                                                    'scripts/release_check.py" in line:\n'
                                                    '                assert "--phase 4 --step 8" '
                                                    'in line, (name, line)\n'
                                                    '        for forbidden in '
                                                    '("continue-on-error:", "|| true", "contents: '
                                                    'write", "id-token: write", "twine upload", '
                                                    '"git push"):\n'
                                                    '            assert forbidden not in text, '
                                                    '(name, forbidden)\n'
                                                    '    ci = (root / '
                                                    '"ci.yml").read_text(encoding="utf-8")\n'
                                                    "    for required in ('os: [ubuntu-latest, "
                                                    'windows-latest]\', \'python-version: ["3.11", '
                                                    '"3.12"]\',\n'
                                                    "                     'dependencies: [current, "
                                                    'minimum]\', \'"numpy==2.0.0" '
                                                    '"pandas==2.2.2"\',\n'
                                                    "                     'RIT_TEST_PARQUET: "
                                                    '"0"\', \'RIT_TEST_PARQUET: "1"\', '
                                                    "'--require-parquet',\n"
                                                    "                     '--baseline-evidence', "
                                                    "'python -m pip check',\n"
                                                    "                     '--minimum-tests 3620', "
                                                    "'--minimum-tests 3623',\n"
                                                    '                     "find_spec(\'pyarrow\') '
                                                    'is None", \'import pyarrow\'):\n'
                                                    '        assert required in ci\n'
                                                    '    assert ci.count("python -m pytest -p '
                                                    'no:cacheprovider -q --junitxml=") == 2\n'
                                                    '    assert " -k " not in ci\n'
                                                    '    golden = (root / '
                                                    '"golden.yml").read_text(encoding="utf-8")\n'
                                                    '    for required in '
                                                    '("tests/golden/test_phase3_math.py", '
                                                    '"tests/integration/test_hero_structure.py",\n'
                                                    '                     '
                                                    '"tests/integration/test_phase3_metric_pipeline.py", '
                                                    '"tests/integration/test_hero_end_to_end.py"):\n'
                                                    '        assert required in golden\n'
                                                    '    security = (root / '
                                                    '"security.yml").read_text(encoding="utf-8")\n'
                                                    '    for required in '
                                                    "('tests/integration/test_no_network.py', "
                                                    "'tests/integration/test_optional_dependency.py',\n"
                                                    '                     '
                                                    "'tests/unit/test_PR012_evidence_classes.py', "
                                                    "'tests/unit/test_PR013_report_schema.py',\n"
                                                    '                     '
                                                    "'tests/unit/test_PR014_unavailable.py', "
                                                    "'tests/unit/test_PR015_redaction.py',\n"
                                                    '                     '
                                                    "'tests/unit/test_PR016_determinism.py', "
                                                    "'tests/unit/test_PR018_language.py',\n"
                                                    '                     '
                                                    "'tests/integration/test_partial_provenance_report.py',\n"
                                                    '                     '
                                                    "'tests/integration/test_partial_lineage_report.py',\n"
                                                    '                     '
                                                    "'tests/integration/test_phase4_cli.py', "
                                                    "'tests/unit/test_phase4_output_safety.py', "
                                                    "'tests/unit/test_phase4_contracts.py', "
                                                    "'tests/integration/test_phase4_gates.py'):\n"
                                                    '        assert required in security\n'
                                                    '    release = (root / '
                                                    '"release.yml").read_text(encoding="utf-8")\n'
                                                    '    assert "python -m build" in release and '
                                                    '"python -m twine check --strict" in release\n'
                                                    '    assert "--dist" in release and '
                                                    '"--candidate" in release\n'
                                                    '    assert "--delivery" not in release\n'
                                                    '    assert '
                                                    '"recursive-integrity-toolkit-phase4-step8-candidate" '
                                                    'in release\n'
                                                    '    assert "rit-phase4-step4" not in release\n'
                                                    '    assert "--minimum-tests 3620" in release '
                                                    'and "--minimum-tests 3623" in release\n'
                                                    '    assert release.count("python -m pytest -p '
                                                    'no:cacheprovider -q --junitxml=") == 2'},
                                            {'new': 'def '
                                                    'test_phase4_step8_current_snapshot_checks_valid_tree_before_mutations(repo_root, '
                                                    'tmp_path, phase4_gate_tools, mutation, '
                                                    'phase4_step8_snapshot):\n'
                                                    '    import json\n'
                                                    '\n'
                                                    '    paths = '
                                                    '{path.relative_to(phase4_step8_snapshot).as_posix()\n'
                                                    '             for path in '
                                                    'phase4_step8_snapshot.rglob("*") if '
                                                    'path.is_file()}\n'
                                                    '    assert len(paths) == 236\n'
                                                    '    for relative in sorted(paths):\n'
                                                    '        destination = tmp_path / relative\n'
                                                    '        '
                                                    'destination.parent.mkdir(parents=True, '
                                                    'exist_ok=True)\n'
                                                    '        shutil.copyfile(phase4_step8_snapshot '
                                                    '/ relative, destination)\n'
                                                    '    verify = '
                                                    'phase4_gate_tools["verify_phase4_step8_snapshot"]\n'
                                                    '    baseline = verify(tmp_path)\n'
                                                    '    assert baseline["package_modules"] == 40\n'
                                                    '    assert baseline["frozen_runtime_modules"] '
                                                    '== 38\n'
                                                    '    assert baseline["frozen_schemas"] == 5\n'
                                                    '    assert '
                                                    'baseline["result_contracts_enabled"] is True\n'
                                                    '    assert baseline["adapters_enabled"] is '
                                                    'True\n'
                                                    '    assert baseline["privacy_views_enabled"] '
                                                    'is True\n'
                                                    '    assert baseline["renderers_enabled"] is '
                                                    'True\n'
                                                    '    assert '
                                                    'baseline["output_publication_enabled"] is '
                                                    'True\n'
                                                    '    assert baseline["cli_analysis_enabled"] '
                                                    'is True\n'
                                                    '    assert baseline["phase_complete"] is '
                                                    'False\n'
                                                    '    if mutation == "unchanged":\n'
                                                    '        return\n'
                                                    '    replacements = {\n'
                                                    '        "formula": '
                                                    '("src/recursive_integrity_toolkit/metrics/diversity.py",\n'
                                                    '                    b"diversity = 1.0 - '
                                                    'concentration", b"diversity = 0.5 - '
                                                    'concentration"),\n'
                                                    '        "math_oracle": '
                                                    '("tests/golden/phase3_math_cases.json", '
                                                    'b\'"v2_support":5\', b\'"v2_support":3\'),\n'
                                                    '        "hero": '
                                                    '("examples/hero/records_v2.csv", '
                                                    'b"v2_08,v2,", b"v2_99,v2,"),\n'
                                                    '        "dependency": ("pyproject.toml", '
                                                    'b"numpy>=2.0", b"numpy>=3.0"),\n'
                                                    '        "historical_assertion": '
                                                    '("tests/unit/test_phase4_contracts.py",\n'
                                                    "                                 b'    assert "
                                                    'control["active_phase"] == 4 and '
                                                    'control["active_step"] == 4\\n\',\n'
                                                    '                                 b"    assert '
                                                    'True\\n"),\n'
                                                    '        "historical_tooling": '
                                                    '("scripts/release_check.py",\n'
                                                    '                               b"def '
                                                    'verify_phase4_step4_control(control: dict, '
                                                    'step: int = 4) -> None:",\n'
                                                    '                               b"def '
                                                    'verify_phase4_step4_control(control: dict, '
                                                    'step: int = 4) -> None:\\n    return"),\n'
                                                    '        "historical_binding": '
                                                    '("tests/integration/test_phase4_gates.py",\n'
                                                    '                               b"def '
                                                    'test_phase4_step4_current_workflows_preserve_matrix_and_use_active_dispatch(repo_root, '
                                                    'phase4_step4_snapshot):\\n    repo_root = '
                                                    'phase4_step4_snapshot\\n",\n'
                                                    '                               b"def '
                                                    'test_phase4_step4_current_workflows_preserve_matrix_and_use_active_dispatch(repo_root, '
                                                    'phase4_step4_snapshot):\\n"),\n'
                                                    '        "historical_document": '
                                                    '("docs/cli.md", b"# CLI\\n",\n'
                                                    '                                b"# '
                                                    'Unauthorized historical document\\n"),\n'
                                                    '        "input_hash_helper": '
                                                    '("src/recursive_integrity_toolkit/utils/hashing.py",\n'
                                                    '                              b"return '
                                                    'hashlib.sha256(data).hexdigest()", b"return '
                                                    'hashlib.sha256(b\'changed\').hexdigest()"),\n'
                                                    '        "config_resolver_helper": '
                                                    '("src/recursive_integrity_toolkit/config.py",\n'
                                                    '                                   b"def '
                                                    'resolve_config(", b"def '
                                                    'resolve_config_disabled("),\n'
                                                    '    }\n'
                                                    '    appended = {\n'
                                                    '        "frozen_model": '
                                                    '"src/recursive_integrity_toolkit/models.py",\n'
                                                    '        "frozen_schema": '
                                                    '"schemas/report.schema.json",\n'
                                                    '        "plan": "PHASE_4_PLAN.md",\n'
                                                    '        "cli": '
                                                    '"src/recursive_integrity_toolkit/cli.py",\n'
                                                    '        "html": '
                                                    '"src/recursive_integrity_toolkit/reports/html_report.py",\n'
                                                    '        "assembly": '
                                                    '"src/recursive_integrity_toolkit/reports/assembly.py",\n'
                                                    '        "result": '
                                                    '"src/recursive_integrity_toolkit/result.py",\n'
                                                    '        "config": '
                                                    '"src/recursive_integrity_toolkit/config.py",\n'
                                                    '        "hashing": '
                                                    '"src/recursive_integrity_toolkit/utils/hashing.py",\n'
                                                    '        "logging": '
                                                    '"src/recursive_integrity_toolkit/utils/logging.py",\n'
                                                    '        "output_paths": '
                                                    '"src/recursive_integrity_toolkit/utils/paths.py",\n'
                                                    '    }\n'
                                                    '    added = {\n'
                                                    '        "unknown_runtime": '
                                                    '"src/recursive_integrity_toolkit/reports/unauthorized.py",\n'
                                                    '        "premature_completion": '
                                                    '"PHASE_4_COMPLETION.md", "premature_report": '
                                                    '"report.json",\n'
                                                    '    }\n'
                                                    '    if mutation in replacements:\n'
                                                    '        relative, original, replacement = '
                                                    'replacements[mutation]\n'
                                                    '        path = tmp_path / relative\n'
                                                    '        source = path.read_bytes()\n'
                                                    '        assert source.count(original) == 1\n'
                                                    '        '
                                                    'path.write_bytes(source.replace(original, '
                                                    'replacement, 1))\n'
                                                    '    elif mutation in appended:\n'
                                                    '        path = tmp_path / appended[mutation]\n'
                                                    '        path.write_bytes(path.read_bytes() + '
                                                    'b"\\nUnauthorized Step 8 mutation\\n")\n'
                                                    '    elif mutation in added:\n'
                                                    '        path = tmp_path / added[mutation]\n'
                                                    '        assert not path.exists()\n'
                                                    '        path.write_text("Unauthorized '
                                                    'later-stage file\\n", encoding="utf-8")\n'
                                                    '    elif mutation == "missing_runtime":\n'
                                                    '        (tmp_path / '
                                                    '"src/recursive_integrity_toolkit/metrics/bounds.py").unlink()\n'
                                                    '    elif mutation.startswith("control_"):\n'
                                                    '        path = tmp_path / '
                                                    '"PHASE_4_BASELINE.json"\n'
                                                    '        control = '
                                                    'json.loads(path.read_text(encoding="utf-8"))\n'
                                                    '        if mutation == "control_step":\n'
                                                    '            control["active_step"] = 9\n'
                                                    '        elif mutation == "control_scope":\n'
                                                    '            '
                                                    'control["runtime_paths_authorized"].append("src/recursive_integrity_toolkit/reports/assembly.py")\n'
                                                    '        else:\n'
                                                    '            '
                                                    'control["schema_changes_authorized"] = True\n'
                                                    '            '
                                                    'control["schema_paths_authorized"].append("schemas/report.schema.json")\n'
                                                    '        path.write_text(json.dumps(control), '
                                                    'encoding="utf-8")\n'
                                                    '    else:\n'
                                                    '        raise AssertionError(f"Unknown active '
                                                    'mutation case: {mutation}")\n'
                                                    '    with pytest.raises(ValueError):\n'
                                                    '        verify(tmp_path)',
                                             'node': 'test_phase4_step8_current_snapshot_checks_valid_tree_before_mutations',
                                             'old': 'def '
                                                    'test_phase4_step8_current_snapshot_checks_valid_tree_before_mutations(repo_root, '
                                                    'tmp_path, phase4_gate_tools, mutation):\n'
                                                    '    import json\n'
                                                    '\n'
                                                    '    tracked = subprocess.check_output(["git", '
                                                    '"-C", str(repo_root), "ls-files", "-z"])\n'
                                                    '    paths = '
                                                    'set(tracked.decode().split("\\0")) - {""}\n'
                                                    '    assert len(paths) == 236\n'
                                                    '    for relative in sorted(paths):\n'
                                                    '        destination = tmp_path / relative\n'
                                                    '        '
                                                    'destination.parent.mkdir(parents=True, '
                                                    'exist_ok=True)\n'
                                                    '        shutil.copyfile(repo_root / relative, '
                                                    'destination)\n'
                                                    '    verify = '
                                                    'phase4_gate_tools["verify_phase4_step8_snapshot"]\n'
                                                    '    baseline = verify(tmp_path)\n'
                                                    '    assert baseline["package_modules"] == 40\n'
                                                    '    assert baseline["frozen_runtime_modules"] '
                                                    '== 38\n'
                                                    '    assert baseline["frozen_schemas"] == 5\n'
                                                    '    assert '
                                                    'baseline["result_contracts_enabled"] is True\n'
                                                    '    assert baseline["adapters_enabled"] is '
                                                    'True\n'
                                                    '    assert baseline["privacy_views_enabled"] '
                                                    'is True\n'
                                                    '    assert baseline["renderers_enabled"] is '
                                                    'True\n'
                                                    '    assert '
                                                    'baseline["output_publication_enabled"] is '
                                                    'True\n'
                                                    '    assert baseline["cli_analysis_enabled"] '
                                                    'is True\n'
                                                    '    assert baseline["phase_complete"] is '
                                                    'False\n'
                                                    '    if mutation == "unchanged":\n'
                                                    '        return\n'
                                                    '    replacements = {\n'
                                                    '        "formula": '
                                                    '("src/recursive_integrity_toolkit/metrics/diversity.py",\n'
                                                    '                    b"diversity = 1.0 - '
                                                    'concentration", b"diversity = 0.5 - '
                                                    'concentration"),\n'
                                                    '        "math_oracle": '
                                                    '("tests/golden/phase3_math_cases.json", '
                                                    'b\'"v2_support":5\', b\'"v2_support":3\'),\n'
                                                    '        "hero": '
                                                    '("examples/hero/records_v2.csv", '
                                                    'b"v2_08,v2,", b"v2_99,v2,"),\n'
                                                    '        "dependency": ("pyproject.toml", '
                                                    'b"numpy>=2.0", b"numpy>=3.0"),\n'
                                                    '        "historical_assertion": '
                                                    '("tests/unit/test_phase4_contracts.py",\n'
                                                    "                                 b'    assert "
                                                    'control["active_phase"] == 4 and '
                                                    'control["active_step"] == 4\\n\',\n'
                                                    '                                 b"    assert '
                                                    'True\\n"),\n'
                                                    '        "historical_tooling": '
                                                    '("scripts/release_check.py",\n'
                                                    '                               b"def '
                                                    'verify_phase4_step4_control(control: dict, '
                                                    'step: int = 4) -> None:",\n'
                                                    '                               b"def '
                                                    'verify_phase4_step4_control(control: dict, '
                                                    'step: int = 4) -> None:\\n    return"),\n'
                                                    '        "historical_binding": '
                                                    '("tests/integration/test_phase4_gates.py",\n'
                                                    '                               b"def '
                                                    'test_phase4_step4_current_workflows_preserve_matrix_and_use_active_dispatch(repo_root, '
                                                    'phase4_step4_snapshot):\\n    repo_root = '
                                                    'phase4_step4_snapshot\\n",\n'
                                                    '                               b"def '
                                                    'test_phase4_step4_current_workflows_preserve_matrix_and_use_active_dispatch(repo_root, '
                                                    'phase4_step4_snapshot):\\n"),\n'
                                                    '        "historical_document": '
                                                    '("docs/cli.md", b"# CLI\\n",\n'
                                                    '                                b"# '
                                                    'Unauthorized historical document\\n"),\n'
                                                    '        "input_hash_helper": '
                                                    '("src/recursive_integrity_toolkit/utils/hashing.py",\n'
                                                    '                              b"return '
                                                    'hashlib.sha256(data).hexdigest()", b"return '
                                                    'hashlib.sha256(b\'changed\').hexdigest()"),\n'
                                                    '        "config_resolver_helper": '
                                                    '("src/recursive_integrity_toolkit/config.py",\n'
                                                    '                                   b"def '
                                                    'resolve_config(", b"def '
                                                    'resolve_config_disabled("),\n'
                                                    '    }\n'
                                                    '    appended = {\n'
                                                    '        "frozen_model": '
                                                    '"src/recursive_integrity_toolkit/models.py",\n'
                                                    '        "frozen_schema": '
                                                    '"schemas/report.schema.json",\n'
                                                    '        "plan": "PHASE_4_PLAN.md",\n'
                                                    '        "cli": '
                                                    '"src/recursive_integrity_toolkit/cli.py",\n'
                                                    '        "html": '
                                                    '"src/recursive_integrity_toolkit/reports/html_report.py",\n'
                                                    '        "assembly": '
                                                    '"src/recursive_integrity_toolkit/reports/assembly.py",\n'
                                                    '        "result": '
                                                    '"src/recursive_integrity_toolkit/result.py",\n'
                                                    '        "config": '
                                                    '"src/recursive_integrity_toolkit/config.py",\n'
                                                    '        "hashing": '
                                                    '"src/recursive_integrity_toolkit/utils/hashing.py",\n'
                                                    '        "logging": '
                                                    '"src/recursive_integrity_toolkit/utils/logging.py",\n'
                                                    '        "output_paths": '
                                                    '"src/recursive_integrity_toolkit/utils/paths.py",\n'
                                                    '    }\n'
                                                    '    added = {\n'
                                                    '        "unknown_runtime": '
                                                    '"src/recursive_integrity_toolkit/reports/unauthorized.py",\n'
                                                    '        "premature_completion": '
                                                    '"PHASE_4_COMPLETION.md", "premature_report": '
                                                    '"report.json",\n'
                                                    '    }\n'
                                                    '    if mutation in replacements:\n'
                                                    '        relative, original, replacement = '
                                                    'replacements[mutation]\n'
                                                    '        path = tmp_path / relative\n'
                                                    '        source = path.read_bytes()\n'
                                                    '        assert source.count(original) == 1\n'
                                                    '        '
                                                    'path.write_bytes(source.replace(original, '
                                                    'replacement, 1))\n'
                                                    '    elif mutation in appended:\n'
                                                    '        path = tmp_path / appended[mutation]\n'
                                                    '        path.write_bytes(path.read_bytes() + '
                                                    'b"\\nUnauthorized Step 8 mutation\\n")\n'
                                                    '    elif mutation in added:\n'
                                                    '        path = tmp_path / added[mutation]\n'
                                                    '        assert not path.exists()\n'
                                                    '        path.write_text("Unauthorized '
                                                    'later-stage file\\n", encoding="utf-8")\n'
                                                    '    elif mutation == "missing_runtime":\n'
                                                    '        (tmp_path / '
                                                    '"src/recursive_integrity_toolkit/metrics/bounds.py").unlink()\n'
                                                    '    elif mutation.startswith("control_"):\n'
                                                    '        path = tmp_path / '
                                                    '"PHASE_4_BASELINE.json"\n'
                                                    '        control = '
                                                    'json.loads(path.read_text(encoding="utf-8"))\n'
                                                    '        if mutation == "control_step":\n'
                                                    '            control["active_step"] = 9\n'
                                                    '        elif mutation == "control_scope":\n'
                                                    '            '
                                                    'control["runtime_paths_authorized"].append("src/recursive_integrity_toolkit/reports/assembly.py")\n'
                                                    '        else:\n'
                                                    '            '
                                                    'control["schema_changes_authorized"] = True\n'
                                                    '            '
                                                    'control["schema_paths_authorized"].append("schemas/report.schema.json")\n'
                                                    '        path.write_text(json.dumps(control), '
                                                    'encoding="utf-8")\n'
                                                    '    else:\n'
                                                    '        raise AssertionError(f"Unknown active '
                                                    'mutation case: {mutation}")\n'
                                                    '    with pytest.raises(ValueError):\n'
                                                    '        verify(tmp_path)'}],
 'tests/unit/test_phase4_contracts.py': [{'new': 'def '
                                                 'test_phase4_step8_approved_control_keeps_independent_step7_anchors(phase4_tools, '
                                                 'phase4_step8_snapshot):\n'
                                                 '    control = json.loads((phase4_step8_snapshot '
                                                 '/ '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\n'
                                                 '    assert phase4_tools["PHASE4_STEP7_FINAL"] == '
                                                 '"bacd33ae65e392872776c6d976401fdc3d565f63"\n'
                                                 '    assert phase4_tools["PHASE4_STEP7_TREE"] == '
                                                 '"4c16914bb0f0c5281efc36624efb8b1a1d4a174e"\n'
                                                 '    assert '
                                                 'phase4_tools["PHASE4_STEP7_TEST_TREE"] == '
                                                 '"96317cb7b25236b79efc0f2d93e1e0f5f132fdb2"\n'
                                                 '    assert control["active_phase"] == 4 and '
                                                 'control["active_step"] == 8\n'
                                                 '    assert control["approval_basis"] == "phase 4 '
                                                 'step 8 开始"\n'
                                                 '    assert control["baseline_commit"] == '
                                                 'BASELINE\n'
                                                 '    assert control["previous_step_commit"] == '
                                                 '"bacd33ae65e392872776c6d976401fdc3d565f63"\n'
                                                 '    assert control["previous_step_tree"] == '
                                                 '"4c16914bb0f0c5281efc36624efb8b1a1d4a174e"\n'
                                                 '    assert control["previous_step_test_tree"] == '
                                                 '"96317cb7b25236b79efc0f2d93e1e0f5f132fdb2"\n'
                                                 '    assert control["previous_step_core_tests"] '
                                                 '== 3620\n'
                                                 '    assert '
                                                 'control["previous_step_parquet_tests"] == 3623\n'
                                                 '    assert '
                                                 'len(control["previous_step_files_sha256"]) == '
                                                 '229\n'
                                                 '    assert '
                                                 'set(control["runtime_paths_authorized"]) == {\n'
                                                 '        '
                                                 '"src/recursive_integrity_toolkit/cli.py",\n'
                                                 '        '
                                                 '"src/recursive_integrity_toolkit/config.py",\n'
                                                 '    }\n'
                                                 '    assert control["schema_changes_authorized"] '
                                                 'is False\n'
                                                 '    assert control["schema_paths_authorized"] == '
                                                 '[]\n'
                                                 '    assert control["new_files_permitted"] == '
                                                 "['src/recursive_integrity_toolkit/data/hero/EXPECTED_OUTPUTS.md', "
                                                 "'src/recursive_integrity_toolkit/data/hero/config.json', "
                                                 "'src/recursive_integrity_toolkit/data/hero/provenance.csv', "
                                                 "'src/recursive_integrity_toolkit/data/hero/records_v1.csv', "
                                                 "'src/recursive_integrity_toolkit/data/hero/records_v2.csv', "
                                                 "'src/recursive_integrity_toolkit/data/hero/version_order.json', "
                                                 "'src/recursive_integrity_toolkit/data/report.schema.json']\n"
                                                 '    for name in ("phase_complete", '
                                                 '"next_step_authorized", "main_merge_authorized", '
                                                 '"publication_authorized"):\n'
                                                 '        assert control[name] is False\n'
                                                 '    '
                                                 'phase4_tools["verify_phase4_step8_control"](control, '
                                                 'step=8)\n'
                                                 '    with pytest.raises(ValueError):\n'
                                                 '        '
                                                 'phase4_tools["verify_phase4_step4_control"](control, '
                                                 'step=4)',
                                          'node': 'test_phase4_step8_approved_control_keeps_independent_step7_anchors',
                                          'old': 'def '
                                                 'test_phase4_step8_approved_control_keeps_independent_step7_anchors(phase4_tools):\n'
                                                 '    control = json.loads((ROOT / '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\n'
                                                 '    assert phase4_tools["PHASE4_STEP7_FINAL"] == '
                                                 '"bacd33ae65e392872776c6d976401fdc3d565f63"\n'
                                                 '    assert phase4_tools["PHASE4_STEP7_TREE"] == '
                                                 '"4c16914bb0f0c5281efc36624efb8b1a1d4a174e"\n'
                                                 '    assert '
                                                 'phase4_tools["PHASE4_STEP7_TEST_TREE"] == '
                                                 '"96317cb7b25236b79efc0f2d93e1e0f5f132fdb2"\n'
                                                 '    assert control["active_phase"] == 4 and '
                                                 'control["active_step"] == 8\n'
                                                 '    assert control["approval_basis"] == "phase 4 '
                                                 'step 8 开始"\n'
                                                 '    assert control["baseline_commit"] == '
                                                 'BASELINE\n'
                                                 '    assert control["previous_step_commit"] == '
                                                 '"bacd33ae65e392872776c6d976401fdc3d565f63"\n'
                                                 '    assert control["previous_step_tree"] == '
                                                 '"4c16914bb0f0c5281efc36624efb8b1a1d4a174e"\n'
                                                 '    assert control["previous_step_test_tree"] == '
                                                 '"96317cb7b25236b79efc0f2d93e1e0f5f132fdb2"\n'
                                                 '    assert control["previous_step_core_tests"] '
                                                 '== 3620\n'
                                                 '    assert '
                                                 'control["previous_step_parquet_tests"] == 3623\n'
                                                 '    assert '
                                                 'len(control["previous_step_files_sha256"]) == '
                                                 '229\n'
                                                 '    assert '
                                                 'set(control["runtime_paths_authorized"]) == {\n'
                                                 '        '
                                                 '"src/recursive_integrity_toolkit/cli.py",\n'
                                                 '        '
                                                 '"src/recursive_integrity_toolkit/config.py",\n'
                                                 '    }\n'
                                                 '    assert control["schema_changes_authorized"] '
                                                 'is False\n'
                                                 '    assert control["schema_paths_authorized"] == '
                                                 '[]\n'
                                                 '    assert control["new_files_permitted"] == '
                                                 "['src/recursive_integrity_toolkit/data/hero/EXPECTED_OUTPUTS.md', "
                                                 "'src/recursive_integrity_toolkit/data/hero/config.json', "
                                                 "'src/recursive_integrity_toolkit/data/hero/provenance.csv', "
                                                 "'src/recursive_integrity_toolkit/data/hero/records_v1.csv', "
                                                 "'src/recursive_integrity_toolkit/data/hero/records_v2.csv', "
                                                 "'src/recursive_integrity_toolkit/data/hero/version_order.json', "
                                                 "'src/recursive_integrity_toolkit/data/report.schema.json']\n"
                                                 '    for name in ("phase_complete", '
                                                 '"next_step_authorized", "main_merge_authorized", '
                                                 '"publication_authorized"):\n'
                                                 '        assert control[name] is False\n'
                                                 '    '
                                                 'phase4_tools["verify_phase4_step8_control"](control, '
                                                 'step=8)\n'
                                                 '    with pytest.raises(ValueError):\n'
                                                 '        '
                                                 'phase4_tools["verify_phase4_step4_control"](control, '
                                                 'step=4)'},
                                         {'new': 'def '
                                                 'test_phase4_step8_control_rejects_forged_scope_and_stage(phase4_tools, '
                                                 'field, value, phase4_step8_snapshot):\n'
                                                 '    control = json.loads((phase4_step8_snapshot '
                                                 '/ '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\n'
                                                 '    verify = '
                                                 'phase4_tools["verify_phase4_step8_control"]\n'
                                                 '    verify(control, step=8)\n'
                                                 '    control[field] = value\n'
                                                 '    with pytest.raises(ValueError):\n'
                                                 '        verify(control, step=8)',
                                          'node': 'test_phase4_step8_control_rejects_forged_scope_and_stage',
                                          'old': 'def '
                                                 'test_phase4_step8_control_rejects_forged_scope_and_stage(phase4_tools, '
                                                 'field, value):\n'
                                                 '    control = json.loads((ROOT / '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\n'
                                                 '    verify = '
                                                 'phase4_tools["verify_phase4_step8_control"]\n'
                                                 '    verify(control, step=8)\n'
                                                 '    control[field] = value\n'
                                                 '    with pytest.raises(ValueError):\n'
                                                 '        verify(control, step=8)'},
                                         {'new': 'def '
                                                 'test_phase4_step8_control_rejects_unapproved_dispatch(phase4_tools, '
                                                 'step, phase4_step8_snapshot):\n'
                                                 '    control = json.loads((phase4_step8_snapshot '
                                                 '/ '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\n'
                                                 '    '
                                                 'phase4_tools["verify_phase4_step8_control"](control, '
                                                 'step=8)\n'
                                                 '    with pytest.raises(ValueError):\n'
                                                 '        '
                                                 'phase4_tools["verify_phase4_step8_control"](control, '
                                                 'step=step)',
                                          'node': 'test_phase4_step8_control_rejects_unapproved_dispatch',
                                          'old': 'def '
                                                 'test_phase4_step8_control_rejects_unapproved_dispatch(phase4_tools, '
                                                 'step):\n'
                                                 '    control = json.loads((ROOT / '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\n'
                                                 '    '
                                                 'phase4_tools["verify_phase4_step8_control"](control, '
                                                 'step=8)\n'
                                                 '    with pytest.raises(ValueError):\n'
                                                 '        '
                                                 'phase4_tools["verify_phase4_step8_control"](control, '
                                                 'step=step)'},
                                         {'new': 'def '
                                                 'test_phase4_step8_control_requires_explicit_approval_fields(phase4_tools, '
                                                 'field, phase4_step8_snapshot):\n'
                                                 '    control = json.loads((phase4_step8_snapshot '
                                                 '/ '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\n'
                                                 '    '
                                                 'phase4_tools["verify_phase4_step8_control"](control)\n'
                                                 '    del control[field]\n'
                                                 '    with pytest.raises(ValueError):\n'
                                                 '        '
                                                 'phase4_tools["verify_phase4_step8_control"](control)',
                                          'node': 'test_phase4_step8_control_requires_explicit_approval_fields',
                                          'old': 'def '
                                                 'test_phase4_step8_control_requires_explicit_approval_fields(phase4_tools, '
                                                 'field):\n'
                                                 '    control = json.loads((ROOT / '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\n'
                                                 '    '
                                                 'phase4_tools["verify_phase4_step8_control"](control)\n'
                                                 '    del control[field]\n'
                                                 '    with pytest.raises(ValueError):\n'
                                                 '        '
                                                 'phase4_tools["verify_phase4_step8_control"](control)'},
                                         {'new': 'def '
                                                 'test_phase4_step8_control_cannot_mint_extra_permission(phase4_tools, '
                                                 'phase4_step8_snapshot):\n'
                                                 '    control = json.loads((phase4_step8_snapshot '
                                                 '/ '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\n'
                                                 '    '
                                                 'phase4_tools["verify_phase4_step8_control"](control)\n'
                                                 '    control["approved_scope_expansion"] = '
                                                 '{"step": 8, "publication": True}\n'
                                                 '    with pytest.raises(ValueError):\n'
                                                 '        '
                                                 'phase4_tools["verify_phase4_step8_control"](control)',
                                          'node': 'test_phase4_step8_control_cannot_mint_extra_permission',
                                          'old': 'def '
                                                 'test_phase4_step8_control_cannot_mint_extra_permission(phase4_tools):\n'
                                                 '    control = json.loads((ROOT / '
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\n'
                                                 '    '
                                                 'phase4_tools["verify_phase4_step8_control"](control)\n'
                                                 '    control["approved_scope_expansion"] = '
                                                 '{"step": 8, "publication": True}\n'
                                                 '    with pytest.raises(ValueError):\n'
                                                 '        '
                                                 'phase4_tools["verify_phase4_step8_control"](control)'},
                                         {'new': 'def '
                                                 'test_phase4_step8_historical_bindings_preserve_assertions(phase4_tools, '
                                                 'phase4_step7_snapshot, phase4_step8_snapshot):\n'
                                                 '    import ast\n'
                                                 '    registry = '
                                                 'phase4_tools["PHASE4_STEP8_MIGRATIONS"]\n'
                                                 '    assert sorted(len(rows) for rows in '
                                                 'registry.values()) == [4, 7]\n'
                                                 '    for path, rows in registry.items():\n'
                                                 '        '
                                                 'phase4_tools["verify_phase4_step8_test_migration"](path, '
                                                 '(phase4_step7_snapshot / path).read_bytes(), '
                                                 '(phase4_step8_snapshot / path).read_bytes())\n'
                                                 '        for row in rows:\n'
                                                 '            trees = [ast.parse(row[key]) for key '
                                                 'in ("old", "new")]\n'
                                                 '            assert trees[0].body[0].name == '
                                                 'trees[1].body[0].name == row["node"]\n'
                                                 '            assert [[ast.dump(n) for n in '
                                                 'ast.walk(t) if isinstance(n, ast.Assert)] for t '
                                                 'in trees][0] == [[ast.dump(n) for n in '
                                                 'ast.walk(t) if isinstance(n, ast.Assert)] for t '
                                                 'in trees][1]',
                                          'node': 'test_phase4_step8_historical_bindings_preserve_assertions',
                                          'old': 'def '
                                                 'test_phase4_step8_historical_bindings_preserve_assertions(phase4_tools, '
                                                 'phase4_step7_snapshot):\n'
                                                 '    import ast\n'
                                                 '    registry = '
                                                 'phase4_tools["PHASE4_STEP8_MIGRATIONS"]\n'
                                                 '    assert sorted(len(rows) for rows in '
                                                 'registry.values()) == [4, 7]\n'
                                                 '    for path, rows in registry.items():\n'
                                                 '        '
                                                 'phase4_tools["verify_phase4_step8_test_migration"](path, '
                                                 '(phase4_step7_snapshot / path).read_bytes(), '
                                                 '(ROOT / path).read_bytes())\n'
                                                 '        for row in rows:\n'
                                                 '            trees = [ast.parse(row[key]) for key '
                                                 'in ("old", "new")]\n'
                                                 '            assert trees[0].body[0].name == '
                                                 'trees[1].body[0].name == row["node"]\n'
                                                 '            assert [[ast.dump(n) for n in '
                                                 'ast.walk(t) if isinstance(n, ast.Assert)] for t '
                                                 'in trees][0] == [[ast.dump(n) for n in '
                                                 'ast.walk(t) if isinstance(n, ast.Assert)] for t '
                                                 'in trees][1]'},
                                         {'new': 'def '
                                                 'test_phase4_step8_historical_guard_rejects_weakening(phase4_tools, '
                                                 'phase4_step7_snapshot, mutation, '
                                                 'phase4_step8_snapshot):\n'
                                                 '    path = '
                                                 '"tests/unit/test_phase4_contracts.py"\n'
                                                 '    before, after = (phase4_step7_snapshot / '
                                                 'path).read_bytes(), (phase4_step8_snapshot / '
                                                 'path).read_bytes()\n'
                                                 '    verify = '
                                                 'phase4_tools["verify_phase4_step8_test_migration"]\n'
                                                 '    verify(path, before, after)\n'
                                                 '    if mutation == "assertion":\n'
                                                 "        needle = b'    assert "
                                                 'control["active_phase"] == 4 and '
                                                 'control["active_step"] == 7\\n\'\n'
                                                 '        assert after.count(needle) == 1\n'
                                                 '        after = after.replace(needle, b"    '
                                                 'assert True\\n", 1)\n'
                                                 '    elif mutation == "binding":\n'
                                                 '        needle = '
                                                 "b'json.loads((phase4_step7_snapshot / "
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\'\n'
                                                 '        assert needle in after\n'
                                                 '        after = after.replace(needle, '
                                                 'needle.replace(b"phase4_step7_snapshot", '
                                                 'b"ROOT"), 1)\n'
                                                 '    elif mutation == "shadow":\n'
                                                 '        after += b"\\ndef '
                                                 'test_phase4_step7_fixed_boundary_opens_only_approved_existing_paths():\\n    '
                                                 'assert True\\n"\n'
                                                 '    else:\n'
                                                 '        after += b"\\ndef '
                                                 'test_phase4_step8_bad(value=globals().clear()):\\n    '
                                                 'pass\\n"\n'
                                                 '    with pytest.raises(ValueError): verify(path, '
                                                 'before, after)',
                                          'node': 'test_phase4_step8_historical_guard_rejects_weakening',
                                          'old': 'def '
                                                 'test_phase4_step8_historical_guard_rejects_weakening(phase4_tools, '
                                                 'phase4_step7_snapshot, mutation):\n'
                                                 '    path = '
                                                 '"tests/unit/test_phase4_contracts.py"\n'
                                                 '    before, after = (phase4_step7_snapshot / '
                                                 'path).read_bytes(), (ROOT / path).read_bytes()\n'
                                                 '    verify = '
                                                 'phase4_tools["verify_phase4_step8_test_migration"]\n'
                                                 '    verify(path, before, after)\n'
                                                 '    if mutation == "assertion":\n'
                                                 "        needle = b'    assert "
                                                 'control["active_phase"] == 4 and '
                                                 'control["active_step"] == 7\\n\'\n'
                                                 '        assert after.count(needle) == 1\n'
                                                 '        after = after.replace(needle, b"    '
                                                 'assert True\\n", 1)\n'
                                                 '    elif mutation == "binding":\n'
                                                 '        needle = '
                                                 "b'json.loads((phase4_step7_snapshot / "
                                                 '"PHASE_4_BASELINE.json").read_text(encoding="utf-8"))\'\n'
                                                 '        assert needle in after\n'
                                                 '        after = after.replace(needle, '
                                                 'needle.replace(b"phase4_step7_snapshot", '
                                                 'b"ROOT"), 1)\n'
                                                 '    elif mutation == "shadow":\n'
                                                 '        after += b"\\ndef '
                                                 'test_phase4_step7_fixed_boundary_opens_only_approved_existing_paths():\\n    '
                                                 'assert True\\n"\n'
                                                 '    else:\n'
                                                 '        after += b"\\ndef '
                                                 'test_phase4_step8_bad(value=globals().clear()):\\n    '
                                                 'pass\\n"\n'
                                                 '    with pytest.raises(ValueError): verify(path, '
                                                 'before, after)'}]}


PHASE4_STEP9_GOLDEN_SHA256 = {'tests/golden/phase4_hero_redacted.json': 'd2138b4f982d09c967cc3268323511ba29add6420ed6b64d91cf13379652e523',
 'tests/golden/phase4_hero_redacted.md': 'df9a0cfabf6eb95f2f494eddf23adb55cc161e2df197b16fbcc36b654eeba3f9',
 'tests/golden/phase4_hero_report.json': 'ce259014260e296e13707693745308c958b829c26373a0ed27c0826690abe633',
 'tests/golden/phase4_hero_report.md': 'bcab1cf1c3008ec86ee1c2a11cac0b130d668911f8e00868209451d74807da80',
 'tests/golden/phase4_report_cases.md': '3ca7005e2dddc990ea1c18fa3408343f9b51a943e0210fe0f611771111ce9709',
 'tests/golden/phase4_report_expected.json': '94fb170bc4095a8f765f23c9b8b87ffb784020734315d0704f36ec4ba3eba10f'}


def _phase4_step8_files():
    """Read the exact accepted Step 8 Git tree and verify every blob identity."""
    for suffix, expected in (("^{commit}", PHASE4_STEP8_FINAL), ("^{tree}", PHASE4_STEP8_TREE),
                             (":tests", PHASE4_STEP8_TEST_TREE)):
        if git("rev-parse", PHASE4_STEP8_FINAL + suffix).decode().strip() != expected:
            raise ValueError("Pinned Phase 4 Step 8 identity mismatch")
    objects = {}
    for entry in git("ls-tree", "-rz", PHASE4_STEP8_FINAL).split(b"\0"):
        if not entry:
            continue
        metadata, raw_path = entry.split(b"\t", 1)
        mode, kind, oid = metadata.split()
        path = raw_path.decode("utf-8")
        if (mode not in (b"100644", b"100755") or kind != b"blob" or path in objects
                or path.startswith("/") or ".." in path.split("/") or ".git" in path.split("/")):
            raise ValueError("Unsafe pinned Step 8 Git object")
        objects[path] = oid.decode("ascii")
    if len(objects) != 236:
        raise ValueError("Pinned Step 8 must contain exactly 236 files")
    files = {}
    with zipfile.ZipFile(io.BytesIO(git("archive", "--format=zip", PHASE4_STEP8_FINAL))) as archive:
        names = [item.filename for item in archive.infolist() if not item.is_dir()]
        if len(names) != len(objects) or set(names) != set(objects):
            raise ValueError("Pinned Step 8 archive identity mismatch")
        for name in names:
            raw = archive.read(name)
            oid = hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()
            if oid != objects[name]:
                raise ValueError(f"Pinned Step 8 blob mismatch: {name}")
            files[name] = raw
    return MappingProxyType(files)


PHASE4_CURRENT_STEP = 11
PHASE4_CURRENT_APPROVAL = "继续 Phase 4 Step 11"
PHASE4_CURRENT_BASE = "9142b344bfc2dc2b33dbc696159f07bbc81b223a"
PHASE4_CURRENT_TREE = "a485078d3e7cf739e10b087acb604f317ee19854"
PHASE4_CURRENT_VERSION_PATHS = {
    "src/recursive_integrity_toolkit/__init__.py", "pyproject.toml",
}
PHASE4_CURRENT_NEW = {
    "PHASE_4_COMPLETION.md", "PHASE_4_VALIDATION_REPORT.md",
    "PHASE_4_ARCHITECTURE_COMPLIANCE_REPORT.md",
}
PHASE4_CURRENT_ALLOWED = PHASE4_G | PHASE4_CURRENT_VERSION_PATHS | PHASE4_CURRENT_NEW | {
    "README.md", "CHANGELOG.md", "docs/cli.md", "docs/report_schema.md",
    "docs/data_schema.md", "docs/privacy.md", "docs/release_process.md",
    "tests/integration/test_cli_validation.py", "tests/integration/test_phase4_cli.py",
    "tests/golden/test_phase4_reports.py",
}


def _phase4_current_files() -> dict[str, bytes]:
    """Use accepted Git content directly, without another source-hash registry."""
    if git("rev-parse", PHASE4_CURRENT_BASE + "^{tree}").decode().strip() != PHASE4_CURRENT_TREE:
        raise ValueError("Accepted Phase 4 source tree mismatch")
    with zipfile.ZipFile(io.BytesIO(git("archive", "--format=zip", PHASE4_CURRENT_BASE))) as archive:
        return {item.filename: archive.read(item) for item in archive.infolist() if not item.is_dir()}


def phase4_current_expected_control() -> dict:
    """Bind current permission to the user's authorization and accepted Git source."""
    result = json.loads(git("show", PHASE4_CURRENT_BASE + ":PHASE_4_BASELINE.json"))
    result.update({
        "control_version": "1.10", "active_step": PHASE4_CURRENT_STEP,
        "approval_date": "2026-09-22", "approval_basis": PHASE4_CURRENT_APPROVAL,
        "previous_step_commit": PHASE4_CURRENT_BASE, "previous_step_tree": PHASE4_CURRENT_TREE,
        "previous_step_test_tree": "2fc4e86c4dee9f069f93af59caab138f0ea63224",
        "permitted_paths": sorted(PHASE4_CURRENT_ALLOWED), "new_files_permitted": sorted(PHASE4_CURRENT_NEW),
        "report_goldens_authorized": False,
        "runtime_changes_authorized": True,
        "runtime_paths_authorized": ["src/recursive_integrity_toolkit/__init__.py"],
    })
    # Git preserves this accepted snapshot; avoid growing parallel hash registries.
    for key in ("previous_step_files_sha256", "previous_step_core_tests",
                "previous_step_parquet_tests", "runtime_repair_approval_basis"):
        result.pop(key, None)
    return result


def verify_phase4_current_control(control: dict, step: int = PHASE4_CURRENT_STEP) -> None:
    if type(step) is not int or step != PHASE4_CURRENT_STEP or type(control) is not dict:
        raise ValueError("Unsupported current Phase 4 stage/control")
    try:
        actual = json.dumps(control, sort_keys=True, ensure_ascii=True, allow_nan=False)
        expected = json.dumps(phase4_current_expected_control(), sort_keys=True, ensure_ascii=True, allow_nan=False)
    except (TypeError, ValueError) as error:
        raise ValueError("Invalid current Phase 4 control") from error
    if actual != expected:
        raise ValueError("Phase 4 control differs from the independently authorized current scope")


def verify_phase4_current_changes(changes: list[tuple[str, str]]) -> None:
    seen = set()
    for status, path in changes:
        if (path in seen or path not in PHASE4_CURRENT_ALLOWED
                or status != ("A" if path in PHASE4_CURRENT_NEW else "M")):
            raise ValueError(f"Unapproved current Phase 4 path/operation: {status} {path}")
        seen.add(path)


def _phase4_step9_header(node, path):
    """Allow explicit test parametrization/fixtures, never definition-time effects."""
    for decorator in node.decorator_list:
        if not isinstance(decorator, ast.Call) or ast.unparse(decorator.func) not in {
                "pytest.fixture", "pytest.mark.parametrize"}:
            raise ValueError(f"Unapproved Step 9 test decorator: {path}:{node.name}")
        if ast.unparse(decorator.func) == "pytest.fixture" and not node.name.startswith("phase4_step"):
            raise ValueError("A Step 9 fixture must have an explicit scoped name")
        if any(keyword.arg is None for keyword in decorator.keywords):
            raise ValueError("Decorator expansion is outside the Step 9 contract")
        for value in [*decorator.args, *(keyword.value for keyword in decorator.keywords)]:
            try:
                ast.literal_eval(value)
            except (ValueError, TypeError, SyntaxError) as error:
                raise ValueError("Step 9 decorator arguments must be literal") from error
    clone = ast.parse(ast.unparse(node)).body[0]
    clone.decorator_list = []
    _phase4_preserve_function_header(clone, path)


def _phase4_step9_append_only(before: bytes, after: bytes, path: str) -> None:
    if not after.startswith(before):
        raise ValueError(f"Inherited Step 8 prefix changed: {path}")
    old, new = ast.parse(before), ast.parse(after)
    bindings = set()
    for node in old.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            bindings.add(node.name)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            bindings.update(alias.asname or alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            bindings.update(child.id for target in targets for child in ast.walk(target) if isinstance(child, ast.Name))
    for node in new.body[len(old.body):]:
        if not isinstance(node, ast.FunctionDef) or node.name in bindings:
            raise ValueError(f"Step 9 addition executes, rebinds or shadows inherited source: {path}")
        allowed_snapshot = path == "tests/conftest.py" and node.name == "phase4_step8_snapshot"
        if not allowed_snapshot and not node.name.startswith(("test_phase4_step9_", "phase4_step9_")):
            raise ValueError(f"Step 9 added test/helper is not explicitly scoped: {path}:{node.name}")
        if path == "tests/conftest.py" and node.name != "phase4_step8_snapshot":
            raise ValueError("Only the pinned Step 8 shared fixture is authorized")
        bindings.add(node.name)
        _phase4_step9_header(node, path)


def verify_phase4_step9_test_migration(path: str, before: bytes, after: bytes) -> None:
    prior = _phase4_step8_files()
    if path not in prior or path not in PHASE4_STEP9_ALLOWED or before != prior[path] or not path.startswith("tests/"):
        raise ValueError("Step 9 migration requires the exact named Step 8 source")
    _phase4_step9_check_test_migration(path, before, after)


def _phase4_step9_check_test_migration(path: str, before: bytes, after: bytes) -> None:
    """Check a source already read from the verified Step 8 immutable mapping."""
    expected = before
    for row in PHASE4_STEP9_MIGRATIONS.get(path, []):
        old, new = row["old"].encode(), row["new"].encode()
        if expected.count(old) != 1:
            raise ValueError("Step 8 historical binding is not unique")
        expected = expected.replace(old, new, 1)
    _phase4_step9_append_only(expected, after, path)


def _phase4_step9_preserve_tooling(before: bytes, after: bytes, path: str) -> None:
    """Preserve exact inherited statements using one source-line split per tree."""
    if path == "scripts/release_check.py":
        old = '    return phase4_cli_main() if explicit_phase4 else main()'
        new = ('    explicit_step9 = "--step=9" in argv or any(a == "--step" and b == "9" for a, b in zip(argv, argv[1:]))\n'
               '    if explicit_phase4 and explicit_step9:\n'
               '        return phase4_step9_cli_main()\n' + old)
        # Earlier preserved dispatch functions contain this source too; bind cli_main only.
        parsed = ast.parse(before)
        entry = next(node for node in parsed.body if isinstance(node, ast.FunctionDef) and node.name == "cli_main")
        old_entry = ast.get_source_segment(before.decode(), entry)
        if old_entry.count(old) != 1:
            raise ValueError("Step 8 release dispatcher identity mismatch")
        replacements = [(old_entry, old_entry.replace(old, new, 1))]
    else:
        old = '    if args.phase == 4 and args.step == 8:\n        return phase4_step8_main(step=args.step)\n'
        new = old + '    if args.phase == 4 and args.step == 9:\n        return phase4_step9_main(step=args.step)\n'
        replacements = [(old, new),
                        ('Choose explicit --phase 3 --step 11 or --phase 4 --step 1 or --phase 4 --step 2 or --phase 4 --step 3 or --phase 4 --step 4 or --phase 4 --step 5 or --phase 4 --step 6 or --phase 4 --step 7 or --phase 4 --step 8',
                         'Choose explicit --phase 3 --step 11 or --phase 4 --step 1 or --phase 4 --step 2 or --phase 4 --step 3 or --phase 4 --step 4 or --phase 4 --step 5 or --phase 4 --step 6 or --phase 4 --step 7 or --phase 4 --step 8 or --phase 4 --step 9')]
    expected = before
    for old, new in replacements:
        if expected.count(old.encode()) != 1:
            raise ValueError(f"Historical dispatcher identity mismatch: {path}")
        expected = expected.replace(old.encode(), new.encode(), 1)
    trees = [ast.parse(expected), ast.parse(after)]
    lines = [expected.splitlines(keepends=True), after.splitlines(keepends=True)]
    def segment(index, node):
        if node.lineno == node.end_lineno:
            return lines[index][node.lineno - 1][node.col_offset:node.end_col_offset]
        return (lines[index][node.lineno - 1][node.col_offset:]
                + b"".join(lines[index][node.lineno:node.end_lineno - 1])
                + lines[index][node.end_lineno - 1][:node.end_col_offset])
    def entry_guard(node):
        return isinstance(node, ast.If) and isinstance(node.test, ast.Compare) and "__name__" in ast.unparse(node.test)
    guards = [n for n in trees[1].body if entry_guard(n)]
    expected_guard = ast.parse('if __name__ == "__main__":\n    raise SystemExit(cli_main())').body[0]
    if len(guards) != 1 or ast.dump(guards[0]) != ast.dump(expected_guard):
        raise ValueError(f"Unapproved Step 9 maintainer entrypoint: {path}")
    historical = [n for n in trees[0].body if not entry_guard(n)]
    current = [n for n in trees[1].body if not entry_guard(n)]
    old_entries = [(segment(0, n), ast.dump(n)) for n in historical]
    cursor = 0
    for node in current:
        if cursor < len(old_entries) and (segment(1, node), ast.dump(node)) == old_entries[cursor]:
            cursor += 1
            continue
        if isinstance(node, ast.FunctionDef) and (node.name == "_phase4_step8_files" or node.name.startswith(
                ("phase4_step9_", "_phase4_step9_", "verify_phase4_step9_", "audit_phase4_step9"))):
            _phase4_preserve_function_header(node, path)
            continue
        if isinstance(node, ast.Assign) and all(isinstance(target, ast.Name) and target.id.startswith(
                ("PHASE4_STEP9_", "PHASE4_STEP8_")) for target in node.targets):
            try:
                ast.literal_eval(node.value)
            except (ValueError, TypeError, SyntaxError) as error:
                raise ValueError(f"Nonliteral added Step 9 maintainer constant: {path}") from error
            continue
        raise ValueError(f"Unapproved Step 9 maintainer addition: {path}")
    if cursor != len(historical):
        raise ValueError(f"Inherited Step 8 maintainer statement changed: {path}")
    def binding_counts(tree):
        counts = {}
        for node in tree.body:
            names = []
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                names = [node.name]
            elif isinstance(node, (ast.Assign, ast.AnnAssign)):
                targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                names = [child.id for target in targets for child in ast.walk(target) if isinstance(child, ast.Name)]
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                names = [alias.asname or alias.name.split(".")[0] for alias in node.names]
            for name in names:
                counts[name] = counts.get(name, 0) + 1
        return counts
    inherited_counts = binding_counts(trees[0])
    for name, count in binding_counts(trees[1]).items():
        if count > inherited_counts.get(name, 1):
            raise ValueError(f"Duplicate Step 9 maintainer binding: {path}:{name}")


def phase4_step9_golden_contract(root: Path = ROOT) -> dict:
    """Check separately frozen rationale and literal expected reports byte for byte."""
    expected = {
        "tests/golden/phase4_report_cases.md", "tests/golden/phase4_report_expected.json",
        "tests/golden/phase4_hero_report.json", "tests/golden/phase4_hero_report.md",
        "tests/golden/phase4_hero_redacted.json", "tests/golden/phase4_hero_redacted.md",
    }
    if set(PHASE4_STEP9_GOLDEN_SHA256) != expected:
        raise ValueError("Step 9 independently authored golden identities are not frozen")
    for name, digest in PHASE4_STEP9_GOLDEN_SHA256.items():
        path = root / name
        if not path.is_file() or path.is_symlink() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise ValueError(f"Step 9 golden rationale or expected bytes changed: {name}")
    return {"frozen_report_oracle_files": len(expected)}


def verify_phase4_current_snapshot(root: Path = ROOT) -> dict:
    """Protect unchanged product/authority bytes with the accepted Git snapshot.

    Current maintenance is reviewed and tested by behavior. Obsolete source forms
    are retained in Git instead of adding another source-binding migration layer.
    """
    prior = _phase4_current_files()
    for path, raw in prior.items():
        target = root / path
        if not target.is_file() or target.is_symlink():
            raise ValueError(f"Missing or aliased accepted file: {path}")
        if path in PHASE4_CURRENT_VERSION_PATHS:
            if raw.count(b"0.1.0.dev2") != 1 or target.read_bytes() != raw.replace(b"0.1.0.dev2", b"0.1.0.dev3", 1):
                raise ValueError(f"Only the approved dev3 version literal may change: {path}")
        if path not in PHASE4_CURRENT_ALLOWED and target.read_bytes() != raw:
            raise ValueError(f"Protected accepted bytes changed: {path}")
    for prefix in ("src/recursive_integrity_toolkit/", "schemas/", "examples/hero/"):
        paths = list((root / prefix).rglob("*"))
        if any(path.is_symlink() for path in paths):
            raise ValueError(f"Aliased protected content: {prefix}")
        current = {path.relative_to(root).as_posix() for path in paths
                   if path.is_file() and "__pycache__" not in path.parts}
        if current != {path for path in prior if path.startswith(prefix)}:
            raise ValueError(f"Protected accepted file set changed: {prefix}")
    verify_phase4_current_control(json.loads((root / "PHASE_4_BASELINE.json").read_text(encoding="utf-8")))
    decisions = (root / "PHASE_4_DECISIONS.md").read_text(encoding="utf-8")
    if PHASE4_CURRENT_APPROVAL not in decisions or PHASE4_CURRENT_BASE not in decisions:
        raise ValueError("Actual authorization or accepted source anchor missing")
    for name in PHASE4_CURRENT_NEW:
        path = root / name
        if not path.is_file() or path.is_symlink() or not path.read_text(encoding="utf-8").strip():
            raise ValueError(f"Step 11 requires a nonempty regular completion record: {name}")
    if any((root / name).exists() for name in PHASE4_FORBIDDEN_OUTPUTS - PHASE4_CURRENT_NEW):
        raise ValueError("Audit outputs cannot be committed as completion records")
    return {"package_modules": 40, "frozen_runtime_modules": 39, "version_literal_changes": 2, "frozen_schemas": 5,
            "hero_files_unchanged": 6, "packaged_resources": 7, "phase_complete": False,
            **phase4_step9_golden_contract(root)}


def phase4_step9_golden_evidence(junit: Path) -> dict:
    """Require all collected report goldens and all twenty unchanged math cases."""
    verify_junit(junit)
    selected = ["tests/golden/test_phase4_reports.py", "tests/golden/test_phase3_math.py"]
    process = subprocess.run([sys.executable, "-m", "pytest", "-p", "no:cacheprovider", "--collect-only", "-q", *selected], cwd=ROOT, capture_output=True, text=True, check=True)
    nodes = [line.strip() for line in process.stdout.splitlines() if line.startswith("tests/") and "::" in line]
    oracle_path = "tests/golden/phase3_math_cases.json"
    oracle_bytes = (ROOT / oracle_path).read_bytes()
    if hashlib.sha256(oracle_bytes).hexdigest() != STEP10_FROZEN_FILES[oracle_path]:
        raise ValueError("Step 9 mathematical oracle bytes differ from the frozen authority")
    expected_math = {selected[1] + "::test_phase3_frozen_case[" + case["case_id"] + "]"
                     for case in json.loads(oracle_bytes)["cases"]}
    registry = selected[1] + "::test_phase3_all_twenty_oracles_have_unique_traceable_identity"
    actual_math = {n for n in nodes if n.startswith(selected[1] + "::")}
    if len(nodes) != len(set(nodes)) or len(expected_math) != 20 or actual_math != expected_math | {registry}:
        raise ValueError("Step 9 golden collection lost mathematical cases or their registry identity")
    if not any(n.startswith(selected[0] + "::") for n in nodes):
        raise ValueError("Step 9 report golden suite is empty")
    expected = set()
    for node in nodes:
        base, bracket, parameter = node.partition("[")
        owner, name = base.rsplit("::", 1)
        expected.add((owner.removesuffix(".py").replace("/", ".").replace("::", "."), name + bracket + parameter))
    cases = {(c.get("classname", ""), c.get("name", "")) for c in ET.parse(junit).getroot().iter("testcase")}
    selected_owners = {p.removesuffix(".py").replace("/", ".") for p in selected}
    actual = {case for case in cases if case[0] in selected_owners}
    if actual != expected:
        raise ValueError("Step 9 JUnit does not execute every collected golden and mathematical case")
    return {"mathematical_cases": 20, "report_golden_tests": sum(n.startswith(selected[0] + "::") for n in nodes),
            "report_golden_nodeids": [n for n in nodes if n.startswith(selected[0] + "::")],
            "mathematical_nodeids": [n for n in nodes if n in expected_math],
            "mathematical_registry_nodeid": registry,
            "missing_nodeids": [], "golden_nodeids_sha256": hashlib.sha256(("\n".join(nodes) + "\n").encode()).hexdigest()}


def audit_phase4_current(step: int = PHASE4_CURRENT_STEP) -> dict:
    verify_phase4_current_control(json.loads((ROOT / "PHASE_4_BASELINE.json").read_text(encoding="utf-8")), step)
    result = {"phase": 4, "active_step": step, **verify_phase4_current_snapshot(),
              "phase0_hashes_verified": 16, "publication_authorized": False}
    print(json.dumps(result, indent=2))
    return result


def audit_phase4_current_diff(step: int = PHASE4_CURRENT_STEP) -> dict:
    if type(step) is not int or step != PHASE4_CURRENT_STEP:
        raise ValueError("Unsupported current Phase 4 stage")
    subprocess.run(["git", "-C", str(ROOT), "merge-base", "--is-ancestor", PHASE4_CURRENT_BASE, "HEAD"], check=True)
    raw = [part.decode("utf-8") for part in git("diff", "--name-status", "--no-renames", "-z", PHASE4_CURRENT_BASE, "--").split(b"\0") if part]
    if len(raw) % 2:
        raise ValueError("Malformed current Git difference records")
    changes = list(zip(raw[::2], raw[1::2]))
    changes.extend(("A", p.decode()) for p in git("ls-files", "--others", "--exclude-standard", "-z").split(b"\0") if p)
    verify_phase4_current_changes(changes)
    result = {"previous_step_commit": PHASE4_CURRENT_BASE, "changed_files": len(changes),
              "changes": changes, "step": step, "scope": "PASS"}
    print(json.dumps(result, indent=2))
    return result


def phase4_current_suite_evidence(output: Path) -> dict:
    """Collect canonical current identities once; historical receipts remain archived."""
    output.mkdir(parents=True, exist_ok=True)
    current, log = _collect(ROOT)
    result = {"current_nodeids": current, "current_tests": len(current),
              "nodeids_sha256": hashlib.sha256(("\n".join(current)+"\n").encode()).hexdigest()}
    (output / "phase4_current_test_identity_manifest.json").write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    (output / "phase4-current-collection.log").write_text(log, encoding="utf-8")
    print(json.dumps({"current_tests": len(current)}, indent=2))
    return result


def phase4_current_candidate(output: Path, step: int = PHASE4_CURRENT_STEP) -> None:
    """Build tested current Phase 4 candidate evidence without declaring Phase 4 complete."""
    if os.environ.get("RIT_TEST_PARQUET") != "1" or importlib.util.find_spec("pyarrow") is None:
        raise ValueError("current Phase 4 candidate evidence requires RIT_TEST_PARQUET=1 and real PyArrow")
    output.mkdir(parents=True, exist_ok=True)
    result = audit_phase4_current(step)
    result["diff"] = audit_phase4_current_diff(step)
    if git("status", "--porcelain").strip():
        raise ValueError("current Phase 4 candidate archive requires committed, clean source")
    result["core"] = verify_junit(output / "core.xml", minimum=3768)
    result["parquet"] = verify_junit(output / "parquet.xml", require_parquet=True, minimum=3771)
    result["core_math_measurements"] = verify_step10_evidence(output / "core.xml", output / "phase4-current-core-observations.json")
    result["parquet_math_measurements"] = verify_step10_evidence(output / "parquet.xml", output / "phase4-current-parquet-observations.json")
    result["core_report_goldens"] = phase4_step9_golden_evidence(output / "core.xml")
    result["parquet_report_goldens"] = phase4_step9_golden_evidence(output / "parquet.xml")
    print(json.dumps({name: result[name] for name in ("core_report_goldens", "parquet_report_goldens")}, indent=2))
    identity = phase4_current_suite_evidence(output)
    result["test_identity"] = {k: identity[k] for k in ("current_tests", "nodeids_sha256")}
    expected = set()
    for node in identity["current_nodeids"]:
        base, bracket, parameter = node.partition("[")
        owner, name = base.rsplit("::", 1)
        expected.add((owner.removesuffix(".py").replace("/", ".").replace("::", "."), name + bracket + parameter))
    for name, parquet in (("core.xml", False), ("parquet.xml", True)):
        cases = {(c.get("classname", ""), c.get("name", "")) for c in ET.parse(output / name).getroot().iter("testcase")}
        target = expected if parquet else {c for c in expected if c[1] not in PARQUET_CASES}
        if cases != target:
            raise ValueError(f"current Phase 4 JUnit does not execute the entire current suite: {name}")
    wheel, sdist = phase4_step8_distributions(output / "dist", expected_version="0.1.0.dev3")
    smoke_installed(wheel)
    smoke_installed_duplicates(wheel)
    phase4_step2_installed_contract_smoke(wheel)
    phase4_step3_installed_assembly_smoke(wheel)
    phase4_step4_installed_privacy_smoke(wheel)
    phase4_step5_installed_renderers_smoke(wheel)
    phase4_step6_installed_publication_smoke(wheel)
    phase4_step7_installed_cli_smoke(wheel)
    phase4_step8_installed_example_smoke(wheel)
    phase4_step8_sdist_smoke(sdist)
    archive = output / "recursive-integrity-toolkit-phase4-current-candidate.zip"
    subprocess.run(["git", "-C", str(ROOT), "archive", "--format=zip", "--prefix=recursive-integrity-toolkit/", "HEAD", "-o", str(archive.resolve())], check=True)
    tracked = {p for p in git("ls-files", "-z").decode().split("\0") if p}
    with zipfile.ZipFile(archive) as zipped:
        entries = [item.filename for item in zipped.infolist() if not item.is_dir()]
        prefix = "recursive-integrity-toolkit/"
        if (len(entries) != len(set(entries)) or any(not name.startswith(prefix) for name in entries)):
            raise ValueError("current Phase 4 source archive has duplicate or unprefixed entries")
        names = {name.removeprefix(prefix) for name in entries}
        if names != tracked or len(tracked) != 246 or len(entries) != 246:
            raise ValueError("current Phase 4 source archive file set mismatch")
        for name in names:
            if zipped.read("recursive-integrity-toolkit/"+name) != (ROOT / name).read_bytes():
                raise ValueError(f"current Phase 4 source archive byte mismatch: {name}")
    result.update({"commit": git("rev-parse", "HEAD").decode().strip(),
                   "tree": git("rev-parse", "HEAD^{tree}").decode().strip(),
                   "source_archive": archive.name, "tracked_files": len(tracked),
                   "python": sys.version, "platform": sys.platform,
                   "versions": {name: importlib.metadata.version(name) for name in ("numpy", "pandas", "pytest")}})
    (output / "phase4_current_execution_metadata.json").write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    (output / "phase4_current_repository_files.sha256").write_text("".join(f"{hashlib.sha256((ROOT/name).read_bytes()).hexdigest()}  {name}\n" for name in sorted(tracked)), encoding="utf-8")
    paths = sorted(p for p in output.rglob("*") if p.is_file() and p.name != "phase4_current_artifacts.sha256")
    (output / "phase4_current_artifacts.sha256").write_text("".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(output).as_posix()}\n" for p in paths), encoding="utf-8")
    print(f"Phase 4 current candidate: {len(tracked)} source files verified; Phase 4 remains incomplete.")


def phase4_current_cli_main() -> int:
    parser = argparse.ArgumentParser(description="Current Phase 4 maintainer gate")
    parser.add_argument("--phase", type=int, choices=(4,), required=True)
    parser.add_argument("--step", type=int, choices=(PHASE4_CURRENT_STEP,), required=True)
    parser.add_argument("--diff", action="store_true")
    parser.add_argument("--junit", type=Path)
    parser.add_argument("--golden-junit", type=Path)
    parser.add_argument("--require-parquet", action="store_true")
    parser.add_argument("--minimum-tests", type=int, default=1)
    parser.add_argument("--baseline-evidence", type=Path)
    parser.add_argument("--dist", type=Path)
    parser.add_argument("--smoke-wheel", type=Path)
    parser.add_argument("--candidate", type=Path)
    parser.add_argument("--delivery", type=Path)
    args = parser.parse_args()
    if args.delivery is not None:
        raise ValueError("Current Phase 4 cannot certify a final phase delivery")
    if args.golden_junit is not None:
        print(json.dumps(phase4_step9_golden_evidence(args.golden_junit), indent=2))
    elif args.junit is not None:
        verify_junit(args.junit, require_parquet=args.require_parquet, minimum=args.minimum_tests)
    elif args.baseline_evidence is not None:
        phase4_current_suite_evidence(args.baseline_evidence)
    elif args.dist is not None:
        audit_phase4_current(args.step)
        wheel, sdist = phase4_step8_distributions(args.dist, expected_version="0.1.0.dev3")
        smoke_installed(wheel)
        smoke_installed_duplicates(wheel)
        phase4_step2_installed_contract_smoke(wheel)
        phase4_step3_installed_assembly_smoke(wheel)
        phase4_step4_installed_privacy_smoke(wheel)
        phase4_step5_installed_renderers_smoke(wheel)
        phase4_step6_installed_publication_smoke(wheel)
        phase4_step7_installed_cli_smoke(wheel)
        phase4_step8_installed_example_smoke(wheel)
        phase4_step8_sdist_smoke(sdist)
    elif args.smoke_wheel is not None:
        smoke_installed(args.smoke_wheel)
    elif args.candidate is not None:
        phase4_current_candidate(args.candidate, args.step)
    else:
        audit_phase4_current(args.step)
        if args.diff:
            audit_phase4_current_diff(args.step)
    return 0


def cli_main() -> int:
    argv = sys.argv[1:]
    explicit_phase4 = "--phase=4" in argv or any(a == "--phase" and b == "4" for a, b in zip(argv, argv[1:]))
    explicit_step2 = "--step=2" in argv or any(a == "--step" and b == "2" for a, b in zip(argv, argv[1:]))
    if explicit_phase4 and explicit_step2:
        return phase4_step2_cli_main()
    explicit_step3 = "--step=3" in argv or any(a == "--step" and b == "3" for a, b in zip(argv, argv[1:]))
    if explicit_phase4 and explicit_step3:
        return phase4_step3_cli_main()
    explicit_step4 = "--step=4" in argv or any(a == "--step" and b == "4" for a, b in zip(argv, argv[1:]))
    if explicit_phase4 and explicit_step4:
        return phase4_step4_cli_main()
    explicit_step5 = "--step=5" in argv or any(a == "--step" and b == "5" for a, b in zip(argv, argv[1:]))
    if explicit_phase4 and explicit_step5:
        return phase4_step5_cli_main()
    explicit_step6 = "--step=6" in argv or any(a == "--step" and b == "6" for a, b in zip(argv, argv[1:]))
    if explicit_phase4 and explicit_step6:
        return phase4_step6_cli_main()
    explicit_step7 = "--step=7" in argv or any(a == "--step" and b == "7" for a, b in zip(argv, argv[1:]))
    if explicit_phase4 and explicit_step7:
        return phase4_step7_cli_main()
    explicit_step8 = "--step=8" in argv or any(a == "--step" and b == "8" for a, b in zip(argv, argv[1:]))
    if explicit_phase4 and explicit_step8:
        return phase4_step8_cli_main()
    explicit_current = "--step=11" in argv or any(a == "--step" and b == "11" for a, b in zip(argv, argv[1:]))
    if explicit_phase4 and explicit_current:
        return phase4_current_cli_main()
    return phase4_cli_main() if explicit_phase4 else main()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", type=int, choices=(2, 3), default=2)
    parser.add_argument("--step", type=int, default=ACTIVE_STEP)
    parser.add_argument("--diff", action="store_true")
    parser.add_argument("--junit", type=Path)
    parser.add_argument("--require-parquet", action="store_true")
    parser.add_argument("--minimum-tests", type=int, default=1)
    parser.add_argument("--baseline-evidence", type=Path)
    parser.add_argument("--dist", type=Path)
    parser.add_argument("--smoke-wheel", type=Path)
    parser.add_argument("--candidate", type=Path)
    parser.add_argument("--delivery", type=Path)
    args = parser.parse_args()
    if args.delivery is not None:
        if args.phase != 3 or args.step != 11:
            raise ValueError("Phase 3 delivery requires explicit Step 11")
        candidate(args.delivery, args.step)
    elif args.junit is not None:
        verify_junit(args.junit, require_parquet=args.require_parquet, minimum=args.minimum_tests)
    elif args.baseline_evidence is not None:
        baseline_evidence(args.baseline_evidence)
    elif args.dist is not None:
        wheel, _ = verify_distributions(args.dist); smoke_installed(wheel); smoke_installed_duplicates(wheel)
    elif args.smoke_wheel is not None:
        smoke_installed(args.smoke_wheel)
    elif args.candidate is not None:
        if args.phase != 3:
            raise ValueError("Candidate requires explicit --phase 3")
        candidate(args.candidate, args.step)
    else:
        audit(args.phase, args.step)
        if args.diff:
            audit_phase3_diff(args.step) if args.phase == 3 else audit_step10_diff()
    return 0


if __name__ == "__main__":
    raise SystemExit(cli_main())
