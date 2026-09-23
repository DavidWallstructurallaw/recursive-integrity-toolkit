"""Shared fixtures for current product behavior and bounded performance runs."""

from __future__ import annotations

import os
import sys
from pathlib import Path

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
