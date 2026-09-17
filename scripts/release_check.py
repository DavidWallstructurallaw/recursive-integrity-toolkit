"""Audit explicit phase boundaries and retain tested intermediate artifacts.

Maintainer tooling only. Phase 2 authority and restoration guards stay frozen.
Phase 3 Step 3 adds exact duplicates only; no publication, merge or completion.
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
ACTIVE_PHASE, ACTIVE_STEP = 3, 3
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
CUMULATIVE_ALLOWED = STEP1_ALLOWED | STEP2_ALLOWED | STEP3_ALLOWED
CUMULATIVE_NEW = STEP1_NEW | STEP2_NEW | STEP3_NEW
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
                "permitted_paths": sorted(STEP3_ALLOWED), "approved_decisions": [f"P3-D{i:02d}" for i in range(1, 11)],
                "phase_complete": False, "next_step_authorized": False,
                "previous_step_commit": STEP2_FINAL, "previous_step_tree": STEP2_TREE,
                "new_files_permitted": sorted(STEP3_NEW), "main_merge_authorized": False,
                "publication_authorized": False}
    if type(control) is not dict or type(step) is not int or step != ACTIVE_STEP:
        raise ValueError("Unsupported active phase or step")
    for key, value in expected.items():
        if type(control.get(key)) is not type(value) or control[key] != value:
            raise ValueError(f"Frozen Phase 3 control mismatch: {key}")


def verify_phase3_changes(changes: list[tuple[str, str]], *, incremental: bool = False) -> None:
    allowed = STEP3_ALLOWED if incremental else CUMULATIVE_ALLOWED
    new_files = STEP3_NEW if incremental else CUMULATIVE_NEW
    for status, path in changes:
        if path not in allowed or status not in ("M", "A"):
            raise ValueError(f"Unauthorized active-stage change: {status} {path}")
        if status == "A" and path not in new_files:
            raise ValueError(f"Unapproved new file: {path}")


def verify_step2_contract_test_migration(before: bytes, after: bytes) -> None:
    """Only the explicitly authorized forged-stage expression may change."""
    old = b'if key in ("active_phase","active_step"): control[key]=2'
    new = b'if key in ("active_phase","active_step"): control[key]+=1'
    if (type(before) is not bytes or type(after) is not bytes
            or before.count(old) != 1 or after != before.replace(old, new, 1)):
        raise ValueError("Step 2 contract-test exception exceeded its exact approved edit")


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
            or project["license"] != "Apache-2.0" or project["version"] != "0.1.0.dev1"
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
        if hashlib.sha256((ROOT / "PHASE_3_PLAN.md").read_bytes()).hexdigest() != PLAN_SHA256:
            raise ValueError("Approved plan bytes changed")
        if control["phase0_sha256"] != dict(entries):
            raise ValueError("Authority hashes differ from original approval")
    result = {"phase": phase, "active_step": step if phase == 3 else None, "package_modules": 40,
              "phase0_hashes_verified": 16, "license_notices": "PASS", "runtime_dependencies": "UNCHANGED",
              "phase_complete": False if phase == 3 else None, "publication_authorized": False}
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
    incremental = [tuple(line.split("\t", 1)) for line in
                   git("diff", "--name-status", "--no-renames", STEP2_FINAL, "HEAD").decode().splitlines()]
    verify_phase3_changes(incremental, incremental=True)
    verify_step2_contract_test_migration(git("show", f"{STEP1_FINAL}:{STEP2_EXCEPTION}"),
                                         (ROOT / STEP2_EXCEPTION).read_bytes())
    if git("diff", "--name-only", "HEAD", "--"):
        raise ValueError("Tracked checkout differs from tested commit")
    for path in ("src/recursive_integrity_toolkit/models.py", "src/recursive_integrity_toolkit/errors.py"):
        before, current = ast.parse(git("show", f"{PHASE2_FINAL}:{path}")), ast.parse((ROOT / path).read_bytes())
        definitions = {n.name: ast.dump(n, include_attributes=False) for n in current.body if isinstance(n, (ast.ClassDef, ast.FunctionDef))}
        for node in before.body:
            if isinstance(node, (ast.ClassDef, ast.FunctionDef)) and definitions.get(node.name) != ast.dump(node, include_attributes=False):
                raise ValueError(f"Inherited contract changed: {path}:{node.name}")
    result = {"baseline": PHASE2_FINAL, "head": git("rev-parse", "HEAD").decode().strip(),
              "changes": changes, "incremental_changes": incremental, "previous_step": STEP2_FINAL,
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
    expected = 1162 if os.environ.get("RIT_TEST_PARQUET") == "1" else 1159
    if len(files) != 197 or len(old) != expected or set(old) - set(new):
        raise ValueError(f"Frozen file/test identities do not reconcile: {len(files)} files, {len(old)} baseline tests, {len(set(old)-set(new))} missing")
    payload = {"baseline_commit": PHASE2_FINAL, "files": files, "baseline_nodeids": old, "current_nodeids": new,
               "previous_step_commit": STEP2_FINAL, "previous_step_nodeids": prior2,
               "step1_commit": STEP1_FINAL, "step1_nodeids": prior,
               "missing_nodeids": [], "nodeids_sha256": hashlib.sha256(("\n".join(old)+"\n").encode()).hexdigest()}
    (output / "baseline-identities.json").write_text(json.dumps(payload, indent=2)+"\n", encoding="utf-8")
    (output / "baseline-collection.log").write_text(old_log, encoding="utf-8")
    (output / "current-collection.log").write_text(new_log, encoding="utf-8")
    summary = {"baseline_files": len(files), "inherited_tests": len(old), "current_tests": len(new), "missing_tests": 0, "previous_step_tests": len(prior2), "step1_tests": len(prior),
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
        names = wheel.namelist(); metadata = [n for n in names if n.endswith(".dist-info/METADATA")]
        if len(metadata) != 1 or "Version: 0.1.0.dev1\n" not in wheel.read(metadata[0]).decode():
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
print('installed duplicates with NumPy/pandas present; exact counts, no I/O/network: PASS')
"""
        subprocess.run([str(python), "-I", "-c", program, str(work)], cwd=work, check=True)


def candidate(output: Path, step: int = ACTIVE_STEP) -> None:
    result = {"audit": audit_phase3_diff(step), "phase_complete": False, "next_step_authorized": False}
    output.mkdir(parents=True, exist_ok=True)
    result["core"] = verify_junit(output / "core.xml", minimum=1429)
    result["parquet"] = verify_junit(output / "parquet.xml", require_parquet=True, minimum=1432)
    result["identities"] = baseline_evidence(output)
    verify_distributions(output / "dist")
    archive = output / "recursive-integrity-toolkit-phase3-step3-candidate.zip"
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
    result["python"] = sys.version; result["platform"] = sys.platform; result["versions"] = {}
    for name in ("numpy", "pandas", "pyarrow", "pytest", "build", "setuptools", "twine"):
        try:
            result["versions"][name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            result["versions"][name] = None
    (output / "phase3_step3_execution.json").write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    files = sorted(p for p in output.rglob("*") if p.is_file() and p.name != "phase3_artifacts.sha256")
    (output / "phase3_artifacts.sha256").write_text("".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(output).as_posix()}\n" for p in files), encoding="utf-8")
    print(f"Step 3 candidate: {len(tracked)} tracked files verified. No Phase 3 completion or publication.")


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
        raise ValueError("Final Phase 3 delivery is not authorized in Step 3")
    if args.junit is not None:
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
