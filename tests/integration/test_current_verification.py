"""Current integrity controls protect source scope, specifications and resources.

These negatives exercise the live controls against disposable copies. Historical
phase tests and their source-binding migrations remain recoverable in Git.
"""

import json
import runpy
import shutil

import pytest


@pytest.fixture(scope="module")
def current_tools(repo_root):
    return runpy.run_path(str(repo_root / "scripts/release_check.py"))


@pytest.fixture
def protected_copy(repo_root, tmp_path):
    for relative in ("src", "schemas", "examples/hero"):
        shutil.copytree(repo_root / relative, tmp_path / relative,
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    shutil.copy2(repo_root / "pyproject.toml", tmp_path / "pyproject.toml")
    return tmp_path


@pytest.mark.parametrize("mutation", ["formula", "new_module", "deleted_module"])
def test_current_scope_rejects_unauthorized_product_changes(current_tools, protected_copy, mutation):
    """Lineage closure and proxy do not authorize unrelated product changes."""
    verify = current_tools["verify_source_scope"]
    verify(protected_copy)
    target = protected_copy / "src/recursive_integrity_toolkit/metrics/diversity.py"
    if mutation == "formula":
        source = target.read_text(encoding="utf-8")
        assert "1.0 -" in source
        target.write_text(source.replace("1.0 -", "1.0 +", 1), encoding="utf-8")
    elif mutation == "new_module":
        target.with_name("unauthorized_metric.py").write_text("def score(): return 1\n", encoding="utf-8")
    else:
        target.unlink()
    with pytest.raises(ValueError):
        verify(protected_copy)


def test_specification_changes_cannot_self_authorize(current_tools, repo_root, tmp_path):
    """A changed specification and forged working manifest still fail the gate."""
    control = json.loads((repo_root / "PHASE_4_BASELINE.json").read_text(encoding="utf-8"))
    for relative in control["phase0_sha256"]:
        shutil.copy2(repo_root / relative, tmp_path / relative)
    current_tools["verify_frozen_specifications"](tmp_path)
    specification = tmp_path / "DEFINITIONS_AND_UNITS.md"
    specification.write_bytes(specification.read_bytes() + b"\nUnauthorized formula change.\n")
    control["phase0_sha256"][specification.name] = "0" * 64
    (tmp_path / "PHASE_4_BASELINE.json").write_text(json.dumps(control), encoding="utf-8")
    with pytest.raises(ValueError):
        current_tools["verify_frozen_specifications"](tmp_path)


@pytest.mark.parametrize("relative", [
    "src/recursive_integrity_toolkit/data/hero/config.json",
    "src/recursive_integrity_toolkit/data/report.schema.json",
])
def test_packaged_resource_corruption_is_rejected(current_tools, protected_copy, relative):
    verify = current_tools["verify_resources"]
    verify(protected_copy)
    (protected_copy / relative).write_text("{}\n", encoding="utf-8")
    with pytest.raises(ValueError):
        verify(protected_copy)


def test_unlisted_packaged_resource_is_rejected(current_tools, protected_copy):
    current_tools["verify_resources"](protected_copy)
    (protected_copy / "src/recursive_integrity_toolkit/data/unlisted.json").write_text("{}", encoding="utf-8")
    with pytest.raises(ValueError):
        current_tools["verify_resources"](protected_copy)


def _write_test_archives(directory, wheel_entries, sdist_entries):
    """Create validator inputs only; these are never release or install evidence."""
    import io
    import tarfile
    import warnings
    import zipfile
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="Duplicate name:.*", category=UserWarning)
        with zipfile.ZipFile(directory / "synthetic.whl", "w") as archive:
            for name, content in wheel_entries:
                archive.writestr(name, content)
    with tarfile.open(directory / "synthetic.tar.gz", "w:gz") as archive:
        for name, content in sdist_entries:
            member = tarfile.TarInfo("synthetic/" + name)
            member.size = len(content)
            archive.addfile(member, io.BytesIO(content))


@pytest.mark.parametrize("kind", ["wheel", "sdist"])
@pytest.mark.parametrize("mutation", ["code", "resource", "missing_resource", "duplicate_member"])
def test_distribution_integrity_rejects_changed_payloads(current_tools, repo_root, tmp_path, kind, mutation):
    runtime = {path.relative_to(repo_root / "src").as_posix(): path.read_bytes()
               for path in (repo_root / "src/recursive_integrity_toolkit").rglob("*.py")}
    resources = {name.removeprefix("src/"): (repo_root / source).read_bytes()
                 for name, source in current_tools["RESOURCES"].items()}
    wheel_entries = list(runtime.items()) + list(resources.items()) + [
        ("synthetic.dist-info/METADATA", b"Version: 0.1.0.test\n"),
        ("synthetic.dist-info/LICENSE", b"synthetic notice"),
        ("synthetic.dist-info/NOTICE", b"synthetic notice"),
    ]
    sdist_entries = [("src/" + name, raw) for name, raw in (*runtime.items(), *resources.items())]
    sdist_entries += [("LICENSE", b"synthetic notice"), ("NOTICE", b"synthetic notice")]
    verify = current_tools["verify_distributions"]
    _write_test_archives(tmp_path, wheel_entries, sdist_entries)
    verify(tmp_path, expected_version="0.1.0.test")
    entries = wheel_entries if kind == "wheel" else sdist_entries
    target = "recursive_integrity_toolkit/metrics/diversity.py" if mutation == "code" else "recursive_integrity_toolkit/data/report.schema.json"
    if kind == "sdist":
        target = "src/" + target
    original = next(raw for name, raw in entries if name == target)
    if mutation == "duplicate_member":
        entries.append((target, original))
    elif mutation == "missing_resource":
        entries[:] = [(name, raw) for name, raw in entries if name != target]
    else:
        entries[:] = [(name, b"corrupted payload" if name == target else raw) for name, raw in entries]
    _write_test_archives(tmp_path, wheel_entries, sdist_entries)
    with pytest.raises(ValueError):
        verify(tmp_path, expected_version="0.1.0.test")


@pytest.mark.parametrize("mutation", ["parent", "absolute", "backslash", "drive", "symlink", "hardlink"])
def test_sdist_extraction_rejects_unsafe_members_before_writes(current_tools, tmp_path, mutation):
    import io
    import tarfile

    path = tmp_path / "unsafe.tar.gz"
    names = {"parent": "root/../outside", "absolute": "/outside",
             "backslash": "root\\outside", "drive": "C:/outside"}
    with tarfile.open(path, "w:gz") as archive:
        first = tarfile.TarInfo("root/valid.txt")
        first.size = 5
        archive.addfile(first, io.BytesIO(b"valid"))
        member = tarfile.TarInfo(names.get(mutation, "root/link"))
        if mutation in {"symlink", "hardlink"}:
            member.type = tarfile.SYMTYPE if mutation == "symlink" else tarfile.LNKTYPE
            member.linkname = "../outside"
            archive.addfile(member)
        else:
            member.size = 6
            archive.addfile(member, io.BytesIO(b"unsafe"))
    destination = tmp_path / "extracted"
    destination.mkdir()
    with pytest.raises(ValueError):
        current_tools["extract_sdist"](path, destination)
    assert list(destination.iterdir()) == []
    assert not (tmp_path / "outside").exists()
