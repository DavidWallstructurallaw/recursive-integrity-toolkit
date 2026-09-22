"""Shared scaffold fixtures and explicit Phase 3 Step 10 test-only composition.

Owner IDs:
    Technical Maintainer, Phase 1 acceptance gate

Current scope:
    Repository structure, safe import, CLI startup, JSON parsing, owner IDs,
    prohibited paths, optional dependency isolation, no-network import, and
    absence of analytical implementation.

Limits:
    Existing scaffold fixtures stay unchanged. New helpers use only approved Hero
    or synthetic data. Nothing here is an importable product orchestrator.
"""

from __future__ import annotations

import ast
import os
import sys
from pathlib import Path
from typing import Callable

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
PACKAGE_ROOT = SRC_ROOT / "recursive_integrity_toolkit"
SCHEMA_ROOT = REPO_ROOT / "schemas"

if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))


@pytest.fixture(scope="session")
def repo_root() -> Path:
    """Return the repository root without reading user data."""
    return REPO_ROOT


@pytest.fixture(scope="session")
def package_root() -> Path:
    """Return the Python package root."""
    return PACKAGE_ROOT


@pytest.fixture(scope="session")
def schema_root() -> Path:
    """Return the schema directory."""
    return SCHEMA_ROOT


@pytest.fixture(scope="session")
def subprocess_env() -> dict[str, str]:
    """Return an environment that imports the local src package without installation."""
    env = os.environ.copy()
    current = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = str(SRC_ROOT) if not current else f"{SRC_ROOT}{os.pathsep}{current}"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return env


@pytest.fixture(scope="session")
def owner_checker(package_root: Path) -> Callable[[str, str], None]:
    """Return a checker for approved owner IDs in module docstrings."""
    def check(relative_path: str, owner_id: str) -> None:
        path = package_root / relative_path
        assert path.is_file(), f"Missing approved module: {relative_path}"
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        doc = ast.get_docstring(tree) or ""
        assert "Owner IDs:" in doc, f"Owner section missing in {relative_path}"
        assert owner_id in doc, f"{owner_id} missing from {relative_path} owner section"
        assert "Current phase status:" in doc, f"Phase status missing in {relative_path}"
        assert "No analytical" in doc or "No " in doc, f"No-implementation limit missing in {relative_path}"
    return check


@pytest.fixture(scope="session")
def placeholder_checker(package_root: Path) -> Callable[[str], None]:
    """Return a checker that requires a module to contain only its docstring."""
    def check(relative_path: str) -> None:
        path = package_root / relative_path
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        assert len(tree.body) == 1, f"Unexpected executable body in {relative_path}"
        node = tree.body[0]
        assert isinstance(node, ast.Expr)
        assert isinstance(node.value, ast.Constant)
        assert isinstance(node.value.value, str)
    return check


@pytest.fixture
def phase3_hero_pipeline(repo_root):
    """Return a test-only callable; ordinary validation still performs no metrics."""
    def run():
        from recursive_integrity_toolkit.config import load_config
        from recursive_integrity_toolkit.io.validation import validate_bundle, join_provenance
        from recursive_integrity_toolkit.models import AuditBundle, InputSource, FileRole, CalculationScope, ExplicitPairContext, ContentMode, TailSelectionOptions
        from recursive_integrity_toolkit.representations.field import assign_field_states
        from recursive_integrity_toolkit.metrics.diversity import calculate_state_distribution, compare_support
        from recursive_integrity_toolkit.metrics.duplicates import detect_exact_duplicates
        from recursive_integrity_toolkit.metrics.provenance import summarize_provenance
        from recursive_integrity_toolkit.metrics.bounds import direct_closure_exposure
        from recursive_integrity_toolkit.metrics.tail import select_tail
        hero = repo_root / "examples/hero"
        roles = (FileRole.RECORDS_PRIMARY, FileRole.RECORDS_COMPARE, FileRole.PROVENANCE_MANIFEST, FileRole.CONFIG, FileRole.VERSION_ORDER)
        names = ("records_v1.csv", "records_v2.csv", "provenance.csv", "config.json", "version_order.json")
        bundle = validate_bundle(AuditBundle(tuple(InputSource(role, hero / name) for role, name in zip(roles, names))))
        config = load_config(hero / "config.json")
        distributions, provenance, bounds, duplicates, tails = {}, {}, {}, {}, {}
        for version in ("v1", "v2"):
            representation = assign_field_states(bundle.records, dataset_versions=(version,), scope_id="hero-"+version, config=config.representation)
            distributions[version] = calculate_state_distribution(representation)
            joined = join_provenance(bundle.records, bundle.provenance, dataset_versions=(version,))
            scope = CalculationScope((version,), joined.scope_record_keys, (), joined.provenance_row_coverage.denominator_name, "hero-provenance-"+version)
            provenance[version] = summarize_provenance(joined, scope=scope)
            bounds[version] = direct_closure_exposure(provenance[version])
            duplicates[version] = detect_exact_duplicates(bundle.records, dataset_versions=(version,), scope_id="hero-exact-"+version,
                representation_name="record_form", representation_version="exact-v1", normalization_profile="exact_utf8_v1", content_mode=ContentMode.INLINE)
            tails[version] = select_tail(distributions[version].unweighted, options=TailSelectionOptions("singleton_count"))
        a, b = distributions["v1"].unweighted, distributions["v2"].unweighted
        pair = compare_support(a, b, context=ExplicitPairContext(a.scope, b.scope, a.representation, b.representation, bundle.version_order),
                               earlier_state_semantics="literal Hero topic categories", later_state_semantics="literal Hero topic categories")
        return dict(bundle=bundle, config=config, distributions=distributions, provenance=provenance, bounds=bounds,
                    duplicates=duplicates, tails=tails, pair=pair)
    return run


@pytest.fixture
def phase3_measure(request):
    """Attach reproducible timing/memory observations to JUnit, without a speed gate.

    tracemalloc measures traced Python allocations, not process RSS or all native
    allocations. Tracing overhead is included in elapsed time. Inputs allocated
    before the callable are excluded from the per-operation peak.
    """
    def measure(name, operation, **details):
        import gc
        import importlib.metadata
        import json
        import platform
        import time
        import tracemalloc
        assert not tracemalloc.is_tracing(), "measurement needs its own tracing interval"
        gc.collect()
        tracemalloc.start(1)
        start = time.perf_counter()
        try:
            value = operation()
            elapsed = time.perf_counter() - start
            current, peak = tracemalloc.get_traced_memory()
        finally:
            tracemalloc.stop()
        versions = {}
        for package in ("numpy", "pandas", "pytest", "pyarrow"):
            try:
                versions[package] = importlib.metadata.version(package)
            except importlib.metadata.PackageNotFoundError:
                versions[package] = None
        observation = dict(name=name, elapsed_seconds=elapsed, traced_current_bytes=current, traced_peak_bytes=peak,
            memory_method="tracemalloc(1); per-call Python allocations; excludes preexisting inputs and untracked native allocations",
            timing_method="perf_counter wall clock with tracing enabled; no repeated best-of selection",
            python=platform.python_version(), platform=platform.platform(), processor=platform.machine(), versions=versions,
            whole_product_report_target_certified=False, **details)
        request.node.user_properties.append(("phase3_performance", json.dumps(observation, sort_keys=True)))
        assert elapsed >= 0 and peak >= current >= 0
        return value
    return measure


@pytest.fixture(scope="session")
def phase3_step10_snapshot(repo_root, tmp_path_factory):
    """Materialize immutable Step 10 source for its historical stage assertions."""
    import io
    import subprocess
    import zipfile
    root = tmp_path_factory.mktemp("phase3-step10")
    commit = "150a2a105e01883672ef0c2300b41b0de3be352e"
    tree = subprocess.check_output(["git", "-C", str(repo_root), "rev-parse", commit+"^{tree}"], text=True).strip()
    assert tree == "b609cb75913fc6352729086819a24795caae1dd8"
    raw = subprocess.check_output(["git", "-C", str(repo_root), "archive", "--format=zip", commit])
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        archive.extractall(root)
    return root


@pytest.fixture(scope="session")
def phase3_final_snapshot(repo_root, tmp_path_factory):
    """Provide verified final Phase 3 bytes only to listed historical tests.

    The source checkout is never rebound. The private archive has no Git working
    tree, accepts only pinned regular-file blobs, and is checked again after use.
    Files remain writable so copies in inherited mutation tests work on Windows;
    changing this snapshot itself fails the closing byte and file-set check.
    """
    import hashlib
    import io
    import subprocess
    import zipfile
    from pathlib import PurePosixPath

    commit = "e3ffb8c0a88bfe31f669f9662d9b5213da628b3a"
    tree = "e2a25f8cfdc66c3317809c479f80fdae162e6ba9"
    tests_tree = "6ab22cb9197a8f094f455b29a07a851062bb26c9"

    def git(*arguments):
        return subprocess.check_output(["git", "-C", str(repo_root), *arguments])

    assert git("rev-parse", commit + "^{commit}").decode().strip() == commit
    assert git("rev-parse", commit + "^{tree}").decode().strip() == tree
    assert git("rev-parse", commit + ":tests").decode().strip() == tests_tree
    blobs = {}
    for entry in git("ls-tree", "-rz", commit).split(b"\0"):
        if not entry:
            continue
        metadata, name = entry.split(b"\t", 1)
        mode, kind, oid = metadata.split()
        relative = name.decode("utf-8")
        parts = PurePosixPath(relative).parts
        assert mode in (b"100644", b"100755") and kind == b"blob"
        assert parts and not relative.startswith("/") and ".." not in parts and ".git" not in parts
        assert relative not in blobs
        blobs[relative] = oid.decode("ascii")

    def blob_oid(raw):
        return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()

    root = tmp_path_factory.mktemp("phase3-final")
    raw = git("archive", "--format=zip", commit)
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        members = [member for member in archive.infolist() if not member.is_dir()]
        assert len(members) == len(blobs)
        assert {member.filename for member in members} == set(blobs)
        for member in members:
            content = archive.read(member)
            assert blob_oid(content) == blobs[member.filename], member.filename
            destination = root.joinpath(*PurePosixPath(member.filename).parts)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(content)

    def verify_unchanged():
        paths = list(root.rglob("*"))
        assert not any(path.is_symlink() for path in paths), "Historical snapshot gained a symlink"
        files = {path.relative_to(root).as_posix(): path for path in paths if path.is_file()}
        assert set(files) == set(blobs), "Historical snapshot file set changed"
        for name, path in files.items():
            assert blob_oid(path.read_bytes()) == blobs[name], f"Historical snapshot changed: {name}"

    verify_unchanged()
    yield root
    verify_unchanged()


@pytest.fixture(scope="session")
def phase3_final_package_root(phase3_final_snapshot):
    """Return the pinned package only to explicitly migrated historical checks."""
    return phase3_final_snapshot / "src/recursive_integrity_toolkit"


@pytest.fixture(scope="session")
def phase3_final_owner_checker(phase3_final_package_root):
    """Run the inherited ownership assertions against pinned Phase 3 source."""
    def check(relative_path, owner_id):
        path = phase3_final_package_root / relative_path
        assert path.is_file(), f"Missing approved module: {relative_path}"
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        doc = ast.get_docstring(tree) or ""
        assert "Owner IDs:" in doc, f"Owner section missing in {relative_path}"
        assert owner_id in doc, f"{owner_id} missing from {relative_path} owner section"
        assert "Current phase status:" in doc, f"Phase status missing in {relative_path}"
        assert "No analytical" in doc or "No " in doc, f"No-implementation limit missing in {relative_path}"
    return check


@pytest.fixture(scope="session")
def phase3_final_placeholder_checker(phase3_final_package_root):
    """Run the inherited empty-module assertions against pinned Phase 3 source."""
    def check(relative_path):
        path = phase3_final_package_root / relative_path
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        assert len(tree.body) == 1, f"Unexpected executable body in {relative_path}"
        node = tree.body[0]
        assert isinstance(node, ast.Expr)
        assert isinstance(node.value, ast.Constant)
        assert isinstance(node.value.value, str)
    return check


@pytest.fixture(scope="session")
def phase3_final_subprocess_env(phase3_final_snapshot):
    """Import only the pinned src tree for historical help, without bytecode writes."""
    env = os.environ.copy()
    env["PYTHONPATH"] = str(phase3_final_snapshot / "src")
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return env


@pytest.fixture(scope="session")
def phase4_step1_snapshot(repo_root, tmp_path_factory):
    """Provide verified accepted Phase 4 Step 1 bytes only to listed historical tests.

    The source checkout is never rebound. The private archive has no Git working
    tree, accepts only pinned regular-file blobs, and is checked again after use.
    Files remain writable so copies in inherited mutation tests work on Windows;
    changing this snapshot itself fails the closing byte and file-set check.
    """
    import hashlib
    import io
    import subprocess
    import zipfile
    from pathlib import PurePosixPath

    commit = "a7f3c46d6ca05de36bfcb60f496ebb2d5ab4a37c"
    tree = "7f8ef492568456bf5d46fb1b7e2631cb9b94e3fd"
    tests_tree = "2ce77e331a0fc377387735bb55dffd3be630b59c"

    def git(*arguments):
        return subprocess.check_output(["git", "-C", str(repo_root), *arguments])

    assert git("rev-parse", commit + "^{commit}").decode().strip() == commit
    assert git("rev-parse", commit + "^{tree}").decode().strip() == tree
    assert git("rev-parse", commit + ":tests").decode().strip() == tests_tree
    blobs = {}
    for entry in git("ls-tree", "-rz", commit).split(b"\0"):
        if not entry:
            continue
        metadata, name = entry.split(b"\t", 1)
        mode, kind, oid = metadata.split()
        relative = name.decode("utf-8")
        parts = PurePosixPath(relative).parts
        assert mode in (b"100644", b"100755") and kind == b"blob"
        assert parts and not relative.startswith("/") and ".." not in parts and ".git" not in parts
        assert relative not in blobs
        blobs[relative] = oid.decode("ascii")

    def blob_oid(raw):
        return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()

    root = tmp_path_factory.mktemp("phase4-step1")
    raw = git("archive", "--format=zip", commit)
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        members = [member for member in archive.infolist() if not member.is_dir()]
        assert len(members) == len(blobs)
        assert {member.filename for member in members} == set(blobs)
        for member in members:
            content = archive.read(member)
            assert blob_oid(content) == blobs[member.filename], member.filename
            destination = root.joinpath(*PurePosixPath(member.filename).parts)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(content)

    def verify_unchanged():
        paths = list(root.rglob("*"))
        assert not any(path.is_symlink() for path in paths), "Historical snapshot gained a symlink"
        files = {path.relative_to(root).as_posix(): path for path in paths if path.is_file()}
        assert set(files) == set(blobs), "Historical snapshot file set changed"
        for name, path in files.items():
            assert blob_oid(path.read_bytes()) == blobs[name], f"Historical snapshot changed: {name}"

    verify_unchanged()
    yield root
    verify_unchanged()


@pytest.fixture(scope="session")
def phase4_step2_snapshot(repo_root, tmp_path_factory):
    """Provide verified accepted Phase 4 Step 2 bytes only to listed historical tests.

    The source checkout is never rebound. The private archive has no Git working
    tree, accepts only pinned regular-file blobs, and is checked again after use.
    Files remain writable so copies in inherited mutation tests work on Windows;
    changing this snapshot itself fails the closing byte and file-set check.
    """
    import hashlib
    import io
    import subprocess
    import zipfile
    from pathlib import PurePosixPath

    commit = "fcea74e2b1858e83cdbfd1b8212d15343d63ff08"
    tree = "c3ce887fd393cfc6c18364546005f2b74a63b746"
    tests_tree = "9d6ac0cbf3827ab54c7852503d99d442a3796259"

    def git(*arguments):
        return subprocess.check_output(["git", "-C", str(repo_root), *arguments])

    assert git("rev-parse", commit + "^{commit}").decode().strip() == commit
    assert git("rev-parse", commit + "^{tree}").decode().strip() == tree
    assert git("rev-parse", commit + ":tests").decode().strip() == tests_tree
    blobs = {}
    for entry in git("ls-tree", "-rz", commit).split(b"\0"):
        if not entry:
            continue
        metadata, name = entry.split(b"\t", 1)
        mode, kind, oid = metadata.split()
        relative = name.decode("utf-8")
        parts = PurePosixPath(relative).parts
        assert mode in (b"100644", b"100755") and kind == b"blob"
        assert parts and not relative.startswith("/") and ".." not in parts and ".git" not in parts
        assert relative not in blobs
        blobs[relative] = oid.decode("ascii")

    def blob_oid(raw):
        return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()

    root = tmp_path_factory.mktemp("phase4-step2")
    raw = git("archive", "--format=zip", commit)
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        members = [member for member in archive.infolist() if not member.is_dir()]
        assert len(members) == len(blobs)
        assert {member.filename for member in members} == set(blobs)
        for member in members:
            content = archive.read(member)
            assert blob_oid(content) == blobs[member.filename], member.filename
            destination = root.joinpath(*PurePosixPath(member.filename).parts)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(content)

    def verify_unchanged():
        paths = list(root.rglob("*"))
        assert not any(path.is_symlink() for path in paths), "Historical snapshot gained a symlink"
        files = {path.relative_to(root).as_posix(): path for path in paths if path.is_file()}
        assert set(files) == set(blobs), "Historical snapshot file set changed"
        for name, path in files.items():
            assert blob_oid(path.read_bytes()) == blobs[name], f"Historical snapshot changed: {name}"

    verify_unchanged()
    yield root
    verify_unchanged()


@pytest.fixture(scope="session")
def phase4_step3_snapshot(repo_root, tmp_path_factory):
    """Provide verified accepted Phase 4 Step 3 bytes only to listed historical tests.

    The source checkout is never rebound. The private archive has no Git working
    tree, accepts only pinned regular-file blobs, and is checked again after use.
    Files remain writable so copies in inherited mutation tests work on Windows;
    changing this snapshot itself fails the closing byte and file-set check.
    """
    import hashlib
    import io
    import subprocess
    import zipfile
    from pathlib import PurePosixPath

    commit = "974545c456e535ba1e1c5b6bf4ae0ce25bc04b57"
    tree = "15498f3f00d0ce048c3cba2156eb7a44f096ae88"
    tests_tree = "17b87858f77ee4413c98cfd76f16f52170246741"

    def git(*arguments):
        return subprocess.check_output(["git", "-C", str(repo_root), *arguments])

    assert git("rev-parse", commit + "^{commit}").decode().strip() == commit
    assert git("rev-parse", commit + "^{tree}").decode().strip() == tree
    assert git("rev-parse", commit + ":tests").decode().strip() == tests_tree
    blobs = {}
    for entry in git("ls-tree", "-rz", commit).split(b"\0"):
        if not entry:
            continue
        metadata, name = entry.split(b"\t", 1)
        mode, kind, oid = metadata.split()
        relative = name.decode("utf-8")
        parts = PurePosixPath(relative).parts
        assert mode in (b"100644", b"100755") and kind == b"blob"
        assert parts and not relative.startswith("/") and ".." not in parts and ".git" not in parts
        assert relative not in blobs
        blobs[relative] = oid.decode("ascii")

    def blob_oid(raw):
        return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()

    root = tmp_path_factory.mktemp("phase4-step3")
    raw = git("archive", "--format=zip", commit)
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        members = [member for member in archive.infolist() if not member.is_dir()]
        assert len(members) == len(blobs)
        assert {member.filename for member in members} == set(blobs)
        for member in members:
            content = archive.read(member)
            assert blob_oid(content) == blobs[member.filename], member.filename
            destination = root.joinpath(*PurePosixPath(member.filename).parts)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(content)

    def verify_unchanged():
        paths = list(root.rglob("*"))
        assert not any(path.is_symlink() for path in paths), "Historical snapshot gained a symlink"
        files = {path.relative_to(root).as_posix(): path for path in paths if path.is_file()}
        assert set(files) == set(blobs), "Historical snapshot file set changed"
        for name, path in files.items():
            assert blob_oid(path.read_bytes()) == blobs[name], f"Historical snapshot changed: {name}"

    verify_unchanged()
    yield root
    verify_unchanged()


@pytest.fixture(scope="session")
def phase4_step4_snapshot(repo_root, tmp_path_factory):
    """Provide verified accepted Phase 4 Step 4 bytes only to listed historical tests.

    The source checkout is never rebound. The private archive has no Git working
    tree, accepts only pinned regular-file blobs, and is checked again after use.
    Files remain writable so copies in inherited mutation tests work on Windows;
    changing this snapshot itself fails the closing byte and file-set check.
    """
    import hashlib
    import io
    import subprocess
    import zipfile
    from pathlib import PurePosixPath

    commit = "49454a9b162cb8d35e38d1cb1ae32cb208d3a01c"
    tree = "79264d845e08f73ee68e160dea04f7786f18fd0a"
    tests_tree = "4aa4ca0b22f8b8c25afe27feeaba713d6f0830bf"

    def git(*arguments):
        return subprocess.check_output(["git", "-C", str(repo_root), *arguments])

    assert git("rev-parse", commit + "^{commit}").decode().strip() == commit
    assert git("rev-parse", commit + "^{tree}").decode().strip() == tree
    assert git("rev-parse", commit + ":tests").decode().strip() == tests_tree
    blobs = {}
    for entry in git("ls-tree", "-rz", commit).split(b"\0"):
        if not entry:
            continue
        metadata, name = entry.split(b"\t", 1)
        mode, kind, oid = metadata.split()
        relative = name.decode("utf-8")
        parts = PurePosixPath(relative).parts
        assert mode in (b"100644", b"100755") and kind == b"blob"
        assert parts and not relative.startswith("/") and ".." not in parts and ".git" not in parts
        assert relative not in blobs
        blobs[relative] = oid.decode("ascii")

    def blob_oid(raw):
        return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()

    root = tmp_path_factory.mktemp("phase4-step4")
    raw = git("archive", "--format=zip", commit)
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        members = [member for member in archive.infolist() if not member.is_dir()]
        assert len(members) == len(blobs)
        assert {member.filename for member in members} == set(blobs)
        for member in members:
            content = archive.read(member)
            assert blob_oid(content) == blobs[member.filename], member.filename
            destination = root.joinpath(*PurePosixPath(member.filename).parts)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(content)

    def verify_unchanged():
        paths = list(root.rglob("*"))
        assert not any(path.is_symlink() for path in paths), "Historical snapshot gained a symlink"
        files = {path.relative_to(root).as_posix(): path for path in paths if path.is_file()}
        assert set(files) == set(blobs), "Historical snapshot file set changed"
        for name, path in files.items():
            assert blob_oid(path.read_bytes()) == blobs[name], f"Historical snapshot changed: {name}"

    verify_unchanged()
    yield root
    verify_unchanged()


@pytest.fixture(scope="session")
def phase4_step5_snapshot(repo_root, tmp_path_factory):
    """Provide verified accepted Phase 4 Step 5 bytes only to listed historical tests.

    The source checkout is never rebound. The private archive has no Git working
    tree, accepts only pinned regular-file blobs, and is checked again after use.
    Files remain writable so copies in inherited mutation tests work on Windows;
    changing this snapshot itself fails the closing byte and file-set check.
    """
    import hashlib
    import io
    import subprocess
    import zipfile
    from pathlib import PurePosixPath

    commit = "c1667179e895a798bba2349960162542efa5ef87"
    tree = "d83f9fc8e0b569f2d796bd2a83b87422fe350fba"
    tests_tree = "974f8e65904c24ed4e226996eaf571aab6123965"

    def git(*arguments):
        return subprocess.check_output(["git", "-C", str(repo_root), *arguments])

    assert git("rev-parse", commit + "^{commit}").decode().strip() == commit
    assert git("rev-parse", commit + "^{tree}").decode().strip() == tree
    assert git("rev-parse", commit + ":tests").decode().strip() == tests_tree
    blobs = {}
    for entry in git("ls-tree", "-rz", commit).split(b"\0"):
        if not entry:
            continue
        metadata, name = entry.split(b"\t", 1)
        mode, kind, oid = metadata.split()
        relative = name.decode("utf-8")
        parts = PurePosixPath(relative).parts
        assert mode in (b"100644", b"100755") and kind == b"blob"
        assert parts and not relative.startswith("/") and ".." not in parts and ".git" not in parts
        assert relative not in blobs
        blobs[relative] = oid.decode("ascii")

    def blob_oid(raw):
        return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()

    root = tmp_path_factory.mktemp("phase4-step5")
    raw = git("archive", "--format=zip", commit)
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        members = [member for member in archive.infolist() if not member.is_dir()]
        assert len(members) == len(blobs)
        assert {member.filename for member in members} == set(blobs)
        for member in members:
            content = archive.read(member)
            assert blob_oid(content) == blobs[member.filename], member.filename
            destination = root.joinpath(*PurePosixPath(member.filename).parts)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(content)

    def verify_unchanged():
        paths = list(root.rglob("*"))
        assert not any(path.is_symlink() for path in paths), "Historical snapshot gained a symlink"
        files = {path.relative_to(root).as_posix(): path for path in paths if path.is_file()}
        assert set(files) == set(blobs), "Historical snapshot file set changed"
        for name, path in files.items():
            assert blob_oid(path.read_bytes()) == blobs[name], f"Historical snapshot changed: {name}"

    verify_unchanged()
    yield root
    verify_unchanged()


@pytest.fixture(scope="session")
def phase4_step6_snapshot(repo_root, tmp_path_factory):
    """Provide verified accepted Phase 4 Step 6 bytes only to listed historical tests.

    The source checkout is never rebound. The private archive has no Git working
    tree, accepts only pinned regular-file blobs, and is checked again after use.
    Files remain writable so copies in inherited mutation tests work on Windows;
    changing this snapshot itself fails the closing byte and file-set check.
    """
    import hashlib
    import io
    import subprocess
    import zipfile
    from pathlib import PurePosixPath

    commit = "aa2355f2359c3af4fc05345c792f9903b0d5858c"
    tree = "d9b6910079f49a2c739f86eceec05040918a41a5"
    tests_tree = "8d3a03c61da807d1fef8d26fc4af0d6f72e4546e"

    def git(*arguments):
        return subprocess.check_output(["git", "-C", str(repo_root), *arguments])

    assert git("rev-parse", commit + "^{commit}").decode().strip() == commit
    assert git("rev-parse", commit + "^{tree}").decode().strip() == tree
    assert git("rev-parse", commit + ":tests").decode().strip() == tests_tree
    blobs = {}
    for entry in git("ls-tree", "-rz", commit).split(b"\0"):
        if not entry:
            continue
        metadata, name = entry.split(b"\t", 1)
        mode, kind, oid = metadata.split()
        relative = name.decode("utf-8")
        parts = PurePosixPath(relative).parts
        assert mode in (b"100644", b"100755") and kind == b"blob"
        assert parts and not relative.startswith("/") and ".." not in parts and ".git" not in parts
        assert relative not in blobs
        blobs[relative] = oid.decode("ascii")

    def blob_oid(raw):
        return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()

    root = tmp_path_factory.mktemp("phase4-step6")
    raw = git("archive", "--format=zip", commit)
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        members = [member for member in archive.infolist() if not member.is_dir()]
        assert len(members) == len(blobs)
        assert {member.filename for member in members} == set(blobs)
        for member in members:
            content = archive.read(member)
            assert blob_oid(content) == blobs[member.filename], member.filename
            destination = root.joinpath(*PurePosixPath(member.filename).parts)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(content)

    def verify_unchanged():
        paths = list(root.rglob("*"))
        assert not any(path.is_symlink() for path in paths), "Historical snapshot gained a symlink"
        files = {path.relative_to(root).as_posix(): path for path in paths if path.is_file()}
        assert set(files) == set(blobs), "Historical snapshot file set changed"
        for name, path in files.items():
            assert blob_oid(path.read_bytes()) == blobs[name], f"Historical snapshot changed: {name}"

    verify_unchanged()
    yield root
    verify_unchanged()


@pytest.fixture(scope="session")
def phase4_step7_snapshot(repo_root, tmp_path_factory):
    """Provide verified accepted Phase 4 Step 7 bytes only to listed historical tests.

    The source checkout is never rebound. The private archive has no Git working
    tree, accepts only pinned regular-file blobs, and is checked again after use.
    Files remain writable so copies in inherited mutation tests work on Windows;
    changing this snapshot itself fails the closing byte and file-set check.
    """
    import hashlib
    import io
    import subprocess
    import zipfile
    from pathlib import PurePosixPath

    commit = "bacd33ae65e392872776c6d976401fdc3d565f63"
    tree = "4c16914bb0f0c5281efc36624efb8b1a1d4a174e"
    tests_tree = "96317cb7b25236b79efc0f2d93e1e0f5f132fdb2"

    def git(*arguments):
        return subprocess.check_output(["git", "-C", str(repo_root), *arguments])

    assert git("rev-parse", commit + "^{commit}").decode().strip() == commit
    assert git("rev-parse", commit + "^{tree}").decode().strip() == tree
    assert git("rev-parse", commit + ":tests").decode().strip() == tests_tree
    blobs = {}
    for entry in git("ls-tree", "-rz", commit).split(b"\0"):
        if not entry:
            continue
        metadata, name = entry.split(b"\t", 1)
        mode, kind, oid = metadata.split()
        relative = name.decode("utf-8")
        parts = PurePosixPath(relative).parts
        assert mode in (b"100644", b"100755") and kind == b"blob"
        assert parts and not relative.startswith("/") and ".." not in parts and ".git" not in parts
        assert relative not in blobs
        blobs[relative] = oid.decode("ascii")

    def blob_oid(raw):
        return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()

    root = tmp_path_factory.mktemp("phase4-step7")
    raw = git("archive", "--format=zip", commit)
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        members = [member for member in archive.infolist() if not member.is_dir()]
        assert len(members) == len(blobs)
        assert {member.filename for member in members} == set(blobs)
        for member in members:
            content = archive.read(member)
            assert blob_oid(content) == blobs[member.filename], member.filename
            destination = root.joinpath(*PurePosixPath(member.filename).parts)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(content)

    def verify_unchanged():
        paths = list(root.rglob("*"))
        assert not any(path.is_symlink() for path in paths), "Historical snapshot gained a symlink"
        files = {path.relative_to(root).as_posix(): path for path in paths if path.is_file()}
        assert set(files) == set(blobs), "Historical snapshot file set changed"
        for name, path in files.items():
            assert blob_oid(path.read_bytes()) == blobs[name], f"Historical snapshot changed: {name}"

    verify_unchanged()
    yield root
    verify_unchanged()


@pytest.fixture(scope="session")
def phase4_step8_snapshot(repo_root, tmp_path_factory):
    """Provide verified accepted Phase 4 Step 8 bytes only to listed historical tests.

    The source checkout is never rebound. The private archive has no Git working
    tree, accepts only pinned regular-file blobs, and is checked again after use.
    Files remain writable so copies in inherited mutation tests work on Windows;
    changing this snapshot itself fails the closing byte and file-set check.
    """
    import hashlib
    import io
    import subprocess
    import zipfile
    from pathlib import PurePosixPath

    commit = "63e347a785838b64a9c32e636ea48c664458cee4"
    tree = "3ac450b5f67cad738849de18601999fefee98f63"
    tests_tree = "ddaaab24d83080b7c1a27229c15e6e4a3f5b3cd8"

    def git(*arguments):
        return subprocess.check_output(["git", "-C", str(repo_root), *arguments])

    assert git("rev-parse", commit + "^{commit}").decode().strip() == commit
    assert git("rev-parse", commit + "^{tree}").decode().strip() == tree
    assert git("rev-parse", commit + ":tests").decode().strip() == tests_tree
    blobs = {}
    for entry in git("ls-tree", "-rz", commit).split(b"\0"):
        if not entry:
            continue
        metadata, name = entry.split(b"\t", 1)
        mode, kind, oid = metadata.split()
        relative = name.decode("utf-8")
        parts = PurePosixPath(relative).parts
        assert mode in (b"100644", b"100755") and kind == b"blob"
        assert parts and not relative.startswith("/") and ".." not in parts and ".git" not in parts
        assert relative not in blobs
        blobs[relative] = oid.decode("ascii")

    def blob_oid(raw):
        return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()

    root = tmp_path_factory.mktemp("phase4-step8")
    raw = git("archive", "--format=zip", commit)
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        members = [member for member in archive.infolist() if not member.is_dir()]
        assert len(members) == len(blobs)
        assert {member.filename for member in members} == set(blobs)
        for member in members:
            content = archive.read(member)
            assert blob_oid(content) == blobs[member.filename], member.filename
            destination = root.joinpath(*PurePosixPath(member.filename).parts)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(content)

    def verify_unchanged():
        paths = list(root.rglob("*"))
        assert not any(path.is_symlink() for path in paths), "Historical snapshot gained a symlink"
        files = {path.relative_to(root).as_posix(): path for path in paths if path.is_file()}
        assert set(files) == set(blobs), "Historical snapshot file set changed"
        for name, path in files.items():
            assert blob_oid(path.read_bytes()) == blobs[name], f"Historical snapshot changed: {name}"

    verify_unchanged()
    yield root
    verify_unchanged()


@pytest.fixture
def phase4_step10_measure_reports(request, tmp_path, subprocess_env):
    """Measure complete CLI publication in fresh processes; retain every attempt.

    Untraced wall time and separately traced Python allocation are distinct
    observations. Process peak RSS includes interpreter/native allocations and
    is a process high-water mark, never a per-operation allocation estimate.
    """
    import hashlib
    import importlib.metadata
    import json
    import platform
    import subprocess
    import time

    program = r'''
import json, os, sys, time, tracemalloc
from pathlib import Path

def peak_rss():
    if os.name == "nt":
        import ctypes
        from ctypes import wintypes
        class Counters(ctypes.Structure):
            _fields_ = [("cb", wintypes.DWORD), ("PageFaultCount", wintypes.DWORD),
                ("PeakWorkingSetSize", ctypes.c_size_t), ("WorkingSetSize", ctypes.c_size_t),
                ("QuotaPeakPagedPoolUsage", ctypes.c_size_t), ("QuotaPagedPoolUsage", ctypes.c_size_t),
                ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t), ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
                ("PagefileUsage", ctypes.c_size_t), ("PeakPagefileUsage", ctypes.c_size_t)]
        counters = Counters()
        counters.cb = ctypes.sizeof(counters)
        kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel.GetCurrentProcess.restype = wintypes.HANDLE
        psapi = ctypes.WinDLL("psapi", use_last_error=True)
        psapi.GetProcessMemoryInfo.argtypes = [wintypes.HANDLE, ctypes.POINTER(Counters), wintypes.DWORD]
        if not psapi.GetProcessMemoryInfo(kernel.GetCurrentProcess(), ctypes.byref(counters), counters.cb):
            raise ctypes.WinError(ctypes.get_last_error())
        return counters.PeakWorkingSetSize, "GetProcessMemoryInfo.PeakWorkingSetSize; whole fresh process"
    import resource
    raw = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return int(raw if sys.platform == "darwin" else raw * 1024), "getrusage(RUSAGE_SELF).ru_maxrss; whole fresh process"

traced = sys.argv[1] == "traced"
observation_path = Path(sys.argv[2])
before, rss_method = peak_rss()
if traced:
    tracemalloc.start(1)
start = time.perf_counter()
code = None
try:
    from recursive_integrity_toolkit.cli import main
    code = main(sys.argv[3:])
finally:
    elapsed = time.perf_counter() - start
    current, peak = tracemalloc.get_traced_memory() if traced else (None, None)
    if traced:
        tracemalloc.stop()
    after, _ = peak_rss()
    observation_path.write_text(json.dumps(dict(cli_elapsed_seconds=elapsed,
        tracing=traced, traced_current_bytes=current, traced_peak_bytes=peak,
        rss_peak_before_cli_bytes=before, rss_peak_after_cli_bytes=after,
        rss_method=rss_method, cli_exit_code=code), sort_keys=True) + "\n", encoding="utf-8")
sys.exit(code)
'''
    versions = {}
    for package in ("numpy", "pandas", "pytest", "pyarrow"):
        try:
            versions[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            versions[package] = None
    cpu = platform.processor() or platform.machine()
    cpuinfo = Path("/proc/cpuinfo")
    if cpuinfo.is_file():
        cpu = next((line.split(":", 1)[1].strip() for line in cpuinfo.read_text().splitlines()
                    if line.startswith("model name")), cpu)
    environment = dict(python=platform.python_version(), executable=sys.executable,
        platform=platform.platform(), machine=platform.machine(), cpu=cpu,
        logical_cpu_count=os.cpu_count(), versions=versions)

    def measure(name, arguments, input_paths, *, record_count, untraced_attempts=1,
                timeout_seconds=60, trace_allocations=True):
        root = tmp_path / name
        root.mkdir()
        inputs = {str(path): dict(bytes=path.stat().st_size,
                    sha256=hashlib.sha256(path.read_bytes()).hexdigest()) for path in input_paths}
        assembly = SRC_ROOT / "recursive_integrity_toolkit/reports/assembly.py"
        assembly_sha256 = hashlib.sha256(assembly.read_bytes()).hexdigest()
        attempts, reports = [], []
        modes = ["untraced"] * untraced_attempts + (["traced"] if trace_allocations else [])
        for index, mode in enumerate(modes, 1):
            destination = root / f"attempt-{index:02d}-{mode}"
            measurement = root / f"attempt-{index:02d}-{mode}.json"
            command = [sys.executable, "-c", program, mode, str(measurement),
                       "audit", *arguments, "--out", str(destination)]
            start = time.perf_counter()
            timed_out = False
            try:
                completed = subprocess.run(command, env=subprocess_env, cwd=tmp_path,
                    capture_output=True, text=True, check=False, timeout=timeout_seconds)
            except subprocess.TimeoutExpired as error:
                timed_out = True
                def captured(value):
                    return value.decode("utf-8", errors="replace") if isinstance(value, bytes) else value or ""
                completed = subprocess.CompletedProcess(command, -1, captured(error.stdout), captured(error.stderr))
            elapsed = time.perf_counter() - start
            observation = json.loads(measurement.read_text()) if measurement.exists() else {}
            observation.update(name=name, attempt=index, record_count=record_count,
                mode=mode, command=command, subprocess_wall_seconds=elapsed,
                timed_out=timed_out, timeout_seconds=timeout_seconds,
                process_exit_code=completed.returncode, stdout=completed.stdout, stderr=completed.stderr,
                inputs=inputs, environment=environment,
                assembly_source_path=str(assembly), assembly_source_sha256=assembly_sha256,
                allocation_omission_reason=None if trace_allocations else
                    "Full-scale Python allocation tracing was omitted to bound diagnostic runtime and memory; separately labeled bounded observations measure tracing overhead. Actual full-process peak RSS is recorded.",
                includes="fresh interpreter startup, CLI import, loading, validation, metrics, JSON and Markdown publication; outer wall also includes measurement bookkeeping",
                excludes="synthetic input construction, parent-side report assertions and environment discovery",
                allocation_scope="tracemalloc(1), Python allocations during CLI import and audit; excludes untracked native allocations",
                rss_scope="whole fresh process high-water mark; includes interpreter and native allocations; not a delta",
                whole_product_report_target_certified=False,
                report_bytes={filename: (destination / filename).stat().st_size
                    for filename in ("report.json", "report.md") if (destination / filename).is_file()})
            measurement.write_text(json.dumps(observation, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            request.node.user_properties.append(("phase4_performance", json.dumps(observation, sort_keys=True)))
            attempts.append(observation)
            assert completed.returncode == 0, observation
            assert set(observation["report_bytes"]) == {"report.json", "report.md"}
            with (destination / "report.md").open(encoding="utf-8") as markdown:
                assert markdown.readline() == "# Recursive Integrity Audit Report\n"
            reports.append(destination / "report.json")
        summary = dict(name=name, all_attempts=[item["subprocess_wall_seconds"] for item in attempts],
            tracing_overhead_ratio=(attempts[-1]["subprocess_wall_seconds"] / attempts[0]["subprocess_wall_seconds"]
                                    if trace_allocations else None),
            comparison=("one separate traced run divided by the first untraced run; descriptive, affected by scheduling and cache state"
                        if trace_allocations else "no allocation-traced run of this workload; peak RSS remains measured"),
            best_run_selection=False)
        request.node.user_properties.append(("phase4_performance_summary", json.dumps(summary, sort_keys=True)))
        assert inputs == {str(path): dict(bytes=path.stat().st_size,
                    sha256=hashlib.sha256(path.read_bytes()).hexdigest()) for path in input_paths}
        assert hashlib.sha256(assembly.read_bytes()).hexdigest() == assembly_sha256
        return reports, attempts
    return measure
