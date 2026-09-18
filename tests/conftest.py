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
