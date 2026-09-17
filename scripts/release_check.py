"""Audit and package the Phase 2 input-only milestone; never publish a release.

This is maintainer tooling, outside the importable toolkit. It may invoke Git,
create an isolated installation, inspect test evidence, and archive tracked
repository files. It never accepts user audit data or invokes analytical layers.
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
STEP10_ALLOWED = {
    "README.md", "CHANGELOG.md", "docs/architecture.md", "docs/data_schema.md",
    "docs/privacy.md", ".github/workflows/ci.yml", ".github/workflows/security.yml",
    ".github/workflows/release.yml", ".github/workflows/golden.yml",
    "tests/integration/test_ci_workflows.py", "tests/integration/test_license_notices.py",
    "tests/integration/test_no_algorithms.py", "tests/integration/test_prohibited_structure.py",
    "tests/integration/test_repository_structure.py", "scripts/check_spec_consistency.py",
    "scripts/check_traceability.py", "scripts/release_check.py", "pyproject.toml",
    "PHASE_2_COMPLETION.md", "PHASE_2_VALIDATION_REPORT.md",
    "PHASE_2_ARCHITECTURE_COMPLIANCE_REPORT.md",
}
COMPLETION = {"PHASE_2_COMPLETION.md", "PHASE_2_VALIDATION_REPORT.md",
              "PHASE_2_ARCHITECTURE_COMPLIANCE_REPORT.md"}
PROHIBITED = {"server", "webapp", "cloud", "telemetry", "plugins", "agents", "llm",
              "auth", "database", "policy_enforcement"}
PARQUET_CASES = {"test_PR002_parquet_real_roundtrip", "test_PR002_parquet_real_row_limit",
                 "test_PR002_parquet_real_invalid_file"}


def git(*args: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(ROOT), *args])


def project_metadata() -> dict:
    return tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]


def audit() -> dict:
    """Check present authority, exact module shape, licenses, and fixed boundaries."""
    for name in {"LICENSE", "NOTICE", "THIRD_PARTY_NOTICES.md", "THEORY_SOURCES.md"} | COMPLETION:
        if not (ROOT / name).is_file():
            raise ValueError(f"Missing milestone file: {name}")
    project = project_metadata()
    if project["name"] != "recursive-integrity-toolkit" or project["requires-python"] != ">=3.11":
        raise ValueError("Package identity or Python baseline changed")
    if project["license"] != "Apache-2.0":
        raise ValueError("Unexpected code license")
    init = ast.parse((ROOT / "src/recursive_integrity_toolkit/__init__.py").read_text(encoding="utf-8"))
    versions = [ast.literal_eval(node.value) for node in init.body
                if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "__version__" for t in node.targets)]
    if versions != [project["version"]]:
        raise ValueError("Package and metadata versions disagree")
    approval = (ROOT / "PHASE_0_APPROVAL.md").read_text(encoding="utf-8")
    approved = re.findall(r"\| `([^`]+\.md)` \| `([0-9a-f]{64})` \|", approval)
    if len(approved) != 16:
        raise ValueError("Expected sixteen approved Phase 0 file hashes")
    mismatch = [name for name, digest in approved
                if hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != digest]
    if mismatch:
        raise ValueError(f"Approved Phase 0 content changed: {mismatch}")
    if "Apache License" not in (ROOT / "LICENSE").read_text(encoding="utf-8"):
        raise ValueError("Apache license text missing")
    notices = (ROOT / "THIRD_PARTY_NOTICES.md").read_text(encoding="utf-8")
    if any(name not in notices for name in ("NumPy", "pandas", "PyArrow", "pytest", "pip-audit")):
        raise ValueError("Dependency notices are incomplete")
    if project["dependencies"] != ["numpy>=2.0", "pandas>=2.2"]:
        raise ValueError("Unreviewed runtime dependency change")
    modules = sorted((ROOT / "src/recursive_integrity_toolkit").rglob("*.py"))
    if len(modules) != 40:
        raise ValueError("The approved package has forty modules")
    forbidden = sorted({p.name for p in ROOT.rglob("*") if p.is_dir() and p.name in PROHIBITED})
    if forbidden:
        raise ValueError(f"Prohibited directories: {forbidden}")
    result = {"package": project["name"], "version": project["version"],
              "phase0_hashes_verified": len(approved), "package_modules": len(modules),
              "license_notices": "PASS", "runtime_dependencies": "UNCHANGED",
              "prohibited_structure": "PASS", "phase3_authorized": False}
    print(json.dumps(result, indent=2))
    return result


def audit_step10_diff() -> dict:
    """Compare to the approved Step 9 Git object; no file-list inference."""
    changes = []
    for line in git("diff", "--name-status", "--no-renames", STEP9_BASELINE, "HEAD").decode().splitlines():
        status, path = line.split("\t", 1)
        if path not in STEP10_ALLOWED or status not in ("M", "A"):
            raise ValueError(f"Out-of-scope Step 10 change: {status} {path}")
        if status == "A" and path not in COMPLETION:
            raise ValueError(f"Unapproved new repository file: {path}")
        changes.append({"status": status, "path": path})
    if git("diff", "--name-only", STEP9_BASELINE, "HEAD", "--", "src", "schemas", "examples/hero"):
        raise ValueError("Step 10 changed package, schemas, or Hero inputs")
    if git("diff", "--name-only", "HEAD", "--"):
        raise ValueError("Tracked checkout differs from the tested Git object")
    baseline_project = tomllib.loads(git("show", f"{STEP9_BASELINE}:pyproject.toml").decode())
    current_project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    if baseline_project != current_project:
        raise ValueError("This milestone retains its approved dependency and version declarations")
    result = {"baseline": STEP9_BASELINE, "head": git("rev-parse", "HEAD").decode().strip(),
              "changes": changes, "all_40_package_modules_unchanged": True,
              "all_five_schemas_unchanged": True, "all_six_hero_files_unchanged": True}
    print(json.dumps(result, indent=2))
    return result


def verify_junit(path: Path, *, require_parquet: bool = False, minimum: int = 1) -> dict:
    """Require actual passed cases; skips, xfails and duplicate identities fail."""
    tree = ET.parse(path)
    cases = list(tree.getroot().iter("testcase"))
    identities = [(case.get("classname", ""), case.get("name", "")) for case in cases]
    bad = [case.get("name", "") for case in cases
           if any(child.tag in ("failure", "error", "skipped") for child in case)]
    if len(cases) < minimum or bad or len(identities) != len(set(identities)):
        raise ValueError(f"Unacceptable test evidence: count={len(cases)}, failed_or_skipped={bad}")
    names = {case.get("name", "") for case in cases}
    if require_parquet and not PARQUET_CASES <= names:
        raise ValueError("Real PyArrow cases were not all collected and passed")
    # Collection/setup failures can exist as suite counters without normal test cases.
    for suite in tree.getroot().iter("testsuite"):
        if any(int(suite.get(key, "0")) for key in ("failures", "errors", "skipped")):
            raise ValueError("JUnit reports a failed, errored, or skipped suite")
    result = {"tests": len(cases), "passed": len(cases), "failed": 0, "skipped": 0,
              "real_parquet_cases": len(PARQUET_CASES & names)}
    print(json.dumps(result, indent=2))
    return result


def verify_distributions(directory: Path) -> tuple[Path, Path]:
    version = project_metadata()["version"]
    wheels = list(directory.glob("*.whl"))
    sdists = list(directory.glob("*.tar.gz"))
    if len(wheels) != 1 or len(sdists) != 1:
        raise ValueError("Require exactly one wheel and one source distribution")
    expected = {p.relative_to(ROOT / "src").as_posix(): p.read_bytes()
                for p in (ROOT / "src/recursive_integrity_toolkit").rglob("*.py")}
    with zipfile.ZipFile(wheels[0]) as wheel:
        names = wheel.namelist()
        for name, raw in expected.items():
            if wheel.read(name) != raw:
                raise ValueError(f"Wheel code mismatch: {name}")
        metadata = [n for n in names if n.endswith(".dist-info/METADATA")]
        if len(metadata) != 1 or f"Version: {version}\n" not in wheel.read(metadata[0]).decode():
            raise ValueError("Wheel metadata version mismatch")
        for notice in ("LICENSE", "NOTICE"):
            if not any(name.endswith("/" + notice) for name in names):
                raise ValueError(f"Wheel lacks {notice}")
    with tarfile.open(sdists[0], "r:gz") as sdist:
        members = {m.name: m for m in sdist.getmembers()}
        roots = {name.split("/", 1)[0] for name in members}
        if len(roots) != 1:
            raise ValueError("Source distribution must have one root")
        prefix = next(iter(roots))
        for name, raw in expected.items():
            member = members[f"{prefix}/src/{name}"]
            stream = sdist.extractfile(member)
            if stream is None or stream.read() != raw:
                raise ValueError(f"Source distribution code mismatch: {name}")
    print(f"wheel: {wheels[0].name}; source distribution: {sdists[0].name}; 40 modules match")
    return wheels[0], sdists[0]


def smoke_installed(wheel: Path) -> None:
    """Install without dependencies into a fresh venv and test its installed files."""
    with tempfile.TemporaryDirectory(prefix="rit-phase2-install-") as temporary:
        work = Path(temporary)
        subprocess.run([sys.executable, "-m", "venv", str(work / "venv")], check=True)
        bin_dir = work / "venv" / ("Scripts" if os.name == "nt" else "bin")
        python = bin_dir / ("python.exe" if os.name == "nt" else "python")
        subprocess.run([str(python), "-m", "pip", "install", "--no-index", "--no-deps", str(wheel.resolve())],
                       cwd=work, check=True)
        program = '''import hashlib, importlib, importlib.abc, importlib.metadata, pkgutil, socket, sys
from pathlib import Path
class DenyOptional(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in {'pyarrow', 'numpy', 'pandas'}:
            raise ModuleNotFoundError('optional or analytical dependency blocked')
sys.meta_path.insert(0, DenyOptional())
def blocked(*args, **kwargs):
    raise AssertionError('network call during installed smoke test')
socket.create_connection = blocked
socket.getaddrinfo = blocked
socket.socket.connect = blocked
import recursive_integrity_toolkit as package
assert not Path(package.__file__).resolve().is_relative_to(Path(sys.argv[1]) / 'src')
assert package.__version__ == importlib.metadata.version('recursive-integrity-toolkit')
names = [package.__name__] + [m.name for m in pkgutil.walk_packages(package.__path__, package.__name__ + '.')]
assert len(names) == 40
for name in names:
    importlib.import_module(name)
from recursive_integrity_toolkit.io.validation import validate_bundle
from recursive_integrity_toolkit.models import AuditBundle, InputSource, FileRole, CapabilityKey, CapabilityStatus
hero = Path(sys.argv[1]) / 'examples' / 'hero'
files = ('records_v1.csv', 'records_v2.csv', 'provenance.csv', 'config.json', 'version_order.json', 'EXPECTED_OUTPUTS.md')
before = {n: hashlib.sha256((hero / n).read_bytes()).hexdigest() for n in files}
roles = (FileRole.RECORDS_PRIMARY, FileRole.RECORDS_COMPARE, FileRole.PROVENANCE_MANIFEST, FileRole.CONFIG, FileRole.VERSION_ORDER)
result = validate_bundle(AuditBundle(tuple(InputSource(r, hero / n) for r, n in zip(roles, files))))
assert result.observability.maximum_level == 4 and not result.has_errors
assert result.observability.capabilities[CapabilityKey.MODEL_LONGITUDINAL].status is CapabilityStatus.UNAVAILABLE
assert before == {n: hashlib.sha256((hero / n).read_bytes()).hexdigest() for n in files}
assert not {'numpy', 'pandas', 'pyarrow'} & set(sys.modules)
print('installed-wheel modules: 40; Hero Level 4: PASS; no-dependency/no-network: PASS')
'''
        subprocess.run([str(python), "-I", "-c", program, str(ROOT)], cwd=work, check=True)
        for args in (("--help",), ("version",)):
            subprocess.run([str(python), "-I", "-m", "recursive_integrity_toolkit", *args], cwd=work, check=True)
        subprocess.run([str(bin_dir / ("rit.exe" if os.name == "nt" else "rit")), "version"], cwd=work, check=True)
        subprocess.run([str(bin_dir / ("recursive-integrity.exe" if os.name == "nt" else "recursive-integrity")), "--help"],
                       cwd=work, check=True)


def archive_repository(output: Path) -> Path:
    output.mkdir(parents=True, exist_ok=True)
    archive = output / "recursive-integrity-toolkit-phase2.zip"
    subprocess.run(["git", "-C", str(ROOT), "archive", "--format=zip",
                    "--prefix=recursive-integrity-toolkit/", "HEAD", "-o", str(archive.resolve())], check=True)
    tracked = {name for name in git("ls-files", "-z").decode().split("\0") if name}
    with zipfile.ZipFile(archive) as zipped:
        actual = {name.removeprefix("recursive-integrity-toolkit/") for name in zipped.namelist() if not name.endswith("/")}
        if actual != tracked:
            raise ValueError("Archive does not match the tracked repository")
        for name in actual:
            if any(part in {".git", "__pycache__", ".pytest_cache", ".venv", "venv", "build", "dist"}
                   for part in Path(name).parts) or name.endswith((".pyc", ".pyo")):
                raise ValueError(f"Forbidden generated artifact in repository archive: {name}")
            if zipped.read("recursive-integrity-toolkit/" + name) != (ROOT / name).read_bytes():
                raise ValueError(f"Archive byte mismatch: {name}")
    print(f"repository archive: {archive.name}; {len(tracked)} tracked files; single root; byte-verified")
    return archive


def environment_metadata() -> dict:
    result = {"python": sys.version, "platform": sys.platform, "packages": {}}
    for name in ("recursive-integrity-toolkit", "numpy", "pandas", "pyarrow", "pytest", "jsonschema", "build", "setuptools", "twine"):
        try:
            metadata = importlib.metadata.metadata(name)
            license_text = metadata.get("License-Expression") or metadata.get("License") or "not declared in metadata"
            result["packages"][name] = {"version": importlib.metadata.version(name),
                                      "license_metadata_first_line": license_text.splitlines()[0][:200]}
        except importlib.metadata.PackageNotFoundError:
            result["packages"][name] = None
    return result


def delivery(output: Path) -> None:
    """Produce source/archive evidence only after the caller's test gates pass."""
    output.mkdir(parents=True, exist_ok=True)
    metadata = {"audit": audit(), "step10_diff": audit_step10_diff(), "environment": environment_metadata()}
    metadata["core_tests"] = verify_junit(output / "core.xml", minimum=1131)
    metadata["parquet_tests"] = verify_junit(output / "parquet.xml", require_parquet=True, minimum=1134)
    metadata["security_tests"] = verify_junit(output / "security.xml")
    metadata["hero_tests"] = verify_junit(output / "hero.xml")
    verify_distributions(output / "dist")
    archive_repository(output)
    for name in COMPLETION:
        (output / name).write_bytes((ROOT / name).read_bytes())
    (output / "phase2_execution_metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    tracked = [n for n in git("ls-files", "-z").decode().split("\0") if n]
    (output / "phase2_repository_files.sha256").write_text("".join(
        f"{hashlib.sha256((ROOT / n).read_bytes()).hexdigest()}  {n}\n" for n in sorted(tracked)), encoding="utf-8")
    artifacts = sorted(p for p in output.rglob("*") if p.is_file() and p.name != "phase2_artifacts.sha256")
    (output / "phase2_artifacts.sha256").write_text("".join(
        f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(output).as_posix()}\n" for p in artifacts), encoding="utf-8")
    print("Phase 2 delivery artifacts verified. No publication or Phase 3 action performed.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--diff", action="store_true")
    parser.add_argument("--junit", type=Path)
    parser.add_argument("--require-parquet", action="store_true")
    parser.add_argument("--minimum-tests", type=int, default=1)
    parser.add_argument("--dist", type=Path)
    parser.add_argument("--smoke-wheel", type=Path)
    parser.add_argument("--delivery", type=Path)
    args = parser.parse_args()
    if args.junit is not None:
        verify_junit(args.junit, require_parquet=args.require_parquet, minimum=args.minimum_tests)
    elif args.smoke_wheel is not None:
        smoke_installed(args.smoke_wheel)
    elif args.dist is not None:
        wheel, _ = verify_distributions(args.dist)
        smoke_installed(wheel)
    elif args.delivery is not None:
        delivery(args.delivery)
    else:
        audit()
        if args.diff:
            audit_step10_diff()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
