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
PHASE3_COMPLETE = False  # Final acceptance is recorded only after all workflow roles pass.
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
                "publication_authorized": False}
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


def verify_distributions(directory: Path) -> tuple[Path, Path]:
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
        if len(metadata) != 1 or "Version: 0.1.0.dev2\n" not in wheel.read(metadata[0]).decode():
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
    raise SystemExit(main())
