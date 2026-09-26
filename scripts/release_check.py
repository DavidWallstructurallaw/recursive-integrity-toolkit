"""Current source and candidate checks for Recursive Integrity Toolkit.

Step 8 opens the approved explicit lineage CLI and context-input scope. Historical dispatch, source-body
migrations and phase registries are recoverable from the accepted Git commit.
Installed checks below retain their existing product, privacy and package cases.
"""
from __future__ import annotations

import argparse
from functools import lru_cache
import hashlib
import importlib.metadata
import importlib.util
import io
import json
import os
from pathlib import Path, PurePosixPath
import subprocess
import sys
import tarfile
import tempfile
import tomllib
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
ACCEPTED_COMMIT = "267504e8fee4784f6d041e445a9e690c982e61a3"
PROTECTED_PREFIXES = ("src/", "schemas/", "examples/hero/")
CURRENT_IMPLEMENTATION_PATHS = frozenset({
    "src/recursive_integrity_toolkit/cli.py",
    "src/recursive_integrity_toolkit/config.py",
    "src/recursive_integrity_toolkit/models.py",
    "src/recursive_integrity_toolkit/io/loaders.py",
    "src/recursive_integrity_toolkit/io/normalization.py",
    "src/recursive_integrity_toolkit/io/validation.py",
    "src/recursive_integrity_toolkit/lineage/graph.py",
    "src/recursive_integrity_toolkit/reports/assembly.py",
    "src/recursive_integrity_toolkit/result.py",
    "schemas/config.schema.json",
    "schemas/report.schema.json",
    "src/recursive_integrity_toolkit/data/report.schema.json",
})
PARQUET_CASES = {"test_PR002_parquet_real_roundtrip", "test_PR002_parquet_real_row_limit", "test_PR002_parquet_real_invalid_file"}
HERO_NAMES = {"records_v1.csv", "records_v2.csv", "provenance.csv", "config.json", "version_order.json", "EXPECTED_OUTPUTS.md"}
RESOURCES = {f"src/recursive_integrity_toolkit/data/hero/{name}": f"examples/hero/{name}" for name in HERO_NAMES}
RESOURCES["src/recursive_integrity_toolkit/data/report.schema.json"] = "schemas/report.schema.json"


def git(*arguments: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(ROOT), *arguments])


@lru_cache(maxsize=1)
def _accepted_files() -> dict[str, bytes]:
    """Read the existing accepted Git authority, with no new file registry."""
    raw = git("archive", "--format=zip", ACCEPTED_COMMIT)
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        return {member.filename: archive.read(member) for member in archive.infolist() if not member.is_dir()}


def _regular_file(root: Path, relative: str) -> Path:
    path = root / relative
    inside = [root.joinpath(*Path(relative).parts[:index])
              for index in range(len(Path(relative).parts) + 1)]
    if not path.is_file() or any(part.is_symlink() for part in inside):
        raise ValueError(f"Missing or aliased protected file: {relative}")
    return path


def verify_source_scope(root: Path = ROOT) -> dict:
    """Reject product changes outside the currently authorized lineage owners.

    Later authorized implementation updates this single current boundary. It does
    not append another historical dispatcher or grant authority through metadata.
    """
    expected = {name: raw for name, raw in _accepted_files().items()
                if name.startswith(PROTECTED_PREFIXES) or name == "pyproject.toml"}
    for name, raw in expected.items():
        current = _regular_file(root, name).read_bytes()
        if name not in CURRENT_IMPLEMENTATION_PATHS and current != raw:
            raise ValueError(f"Unauthorized product mutation outside Step 8 scope: {name}")
    for prefix in PROTECTED_PREFIXES:
        paths = list((root / prefix).rglob("*"))
        if (root / prefix).is_symlink() or any(path.is_symlink() for path in paths):
            raise ValueError(f"Aliased protected content: {prefix}")
        actual = {path.relative_to(root).as_posix() for path in paths
                  if path.is_file() and "__pycache__" not in path.parts
                  # setuptools writes this metadata during normal wheel installs.
                  # It is outside the package; all product paths stay protected.
                  and not path.relative_to(root).as_posix().startswith(
                      "src/recursive_integrity_toolkit.egg-info/")}
        if actual != {name for name in expected if name.startswith(prefix)}:
            raise ValueError(f"Unauthorized product file-set mutation during Step 8: {prefix}")
    return {"protected_product_files": len(expected) - len(CURRENT_IMPLEMENTATION_PATHS),
            "authorized_implementation_files": len(CURRENT_IMPLEMENTATION_PATHS),
            "product_file_inventory": "unchanged"}


def verify_frozen_specifications(root: Path = ROOT) -> dict:
    """Use the already approved specification hashes from the accepted commit."""
    hashes = json.loads(_accepted_files()["PHASE_4_BASELINE.json"])["phase0_sha256"]
    for name, expected in hashes.items():
        if hashlib.sha256(_regular_file(root, name).read_bytes()).hexdigest() != expected:
            raise ValueError(f"Frozen specification changed: {name}")
    return {"frozen_specifications": len(hashes)}


def verify_resources(root: Path = ROOT) -> dict:
    for destination, source in RESOURCES.items():
        if _regular_file(root, destination).read_bytes() != _regular_file(root, source).read_bytes():
            raise ValueError(f"Packaged resource differs from canonical source: {destination}")
    resource_root = root / "src/recursive_integrity_toolkit/data"
    if {path.relative_to(root).as_posix() for path in resource_root.rglob("*") if path.is_file()} != set(RESOURCES):
        raise ValueError("Packaged resource inventory differs")
    return {"canonical_resource_copies": len(RESOURCES)}


def audit(root: Path = ROOT) -> dict:
    result = {**verify_source_scope(root), **verify_frozen_specifications(root), **verify_resources(root)}
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


def verify_distributions(directory: Path, expected_version: str | None = None) -> tuple[Path, Path]:
    expected_version = expected_version or tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]["version"]
    wheels, sdists = list(directory.glob("*.whl")), list(directory.glob("*.tar.gz"))
    if len(wheels) != 1 or len(sdists) != 1:
        raise ValueError("Require one wheel and one sdist")
    expected = {p.relative_to(ROOT / "src").as_posix(): p.read_bytes() for p in (ROOT / "src/recursive_integrity_toolkit").rglob("*.py")}
    with zipfile.ZipFile(wheels[0]) as wheel:
        for path, raw in expected.items():
            if wheel.read(path) != raw:
                raise ValueError(f"Wheel code mismatch: {path}")
        names = wheel.namelist()
        if len(names) != len(set(names)):
            raise ValueError("Duplicate wheel entries")
        if {n for n in names if n.endswith(".py")} != set(expected):
            raise ValueError("Wheel module set differs from source")
        metadata = [n for n in names if n.endswith(".dist-info/METADATA")]
        if len(metadata) != 1 or f"Version: {expected_version}\n" not in wheel.read(metadata[0]).decode():
            raise ValueError("Wheel metadata mismatch")
        for notice in ("LICENSE", "NOTICE"):
            if not any(n.endswith("/"+notice) for n in names):
                raise ValueError(f"Wheel lacks {notice}")
    with tarfile.open(sdists[0], "r:gz") as archive:
        entries = archive.getmembers()
        members = {m.name: m for m in entries}
        if len(members) != len(entries):
            raise ValueError("Duplicate sdist entries")
        roots = {n.split("/", 1)[0] for n in members}
        if len(roots) != 1:
            raise ValueError("Source archive requires one root")
        prefix = next(iter(roots))
        if {n.removeprefix(prefix + "/src/") for n in members
                if n.startswith(prefix + "/src/recursive_integrity_toolkit/") and n.endswith(".py")} != set(expected):
            raise ValueError("Sdist module set differs from source")
        for notice in ("LICENSE", "NOTICE"):
            if f"{prefix}/{notice}" not in members:
                raise ValueError(f"Sdist lacks {notice}")
        for path, raw in expected.items():
            stream = archive.extractfile(members[f"{prefix}/src/{path}"])
            if stream is None or stream.read() != raw:
                raise ValueError(f"Sdist code mismatch: {path}")
    with zipfile.ZipFile(wheels[0]) as archive:
        actual = {name for name in archive.namelist() if name.startswith("recursive_integrity_toolkit/data/") and not name.endswith("/")}
        if actual != {path.removeprefix("src/") for path in RESOURCES}:
            raise ValueError("Wheel resource inventory differs")
        for destination, source in RESOURCES.items():
            if archive.read(destination.removeprefix("src/")) != (ROOT / source).read_bytes():
                raise ValueError("Wheel resource bytes differ")
    with tarfile.open(sdists[0], "r:gz") as archive:
        prefix = next(iter({m.name.split("/")[0] for m in archive.getmembers()}))
        actual = {m.name.removeprefix(prefix + "/") for m in archive.getmembers()
                  if m.name.startswith(prefix + "/src/recursive_integrity_toolkit/data/") and m.isfile()}
        if actual != set(RESOURCES):
            raise ValueError("Sdist resource inventory differs")
        for destination, source in RESOURCES.items():
            member = archive.getmember(prefix + "/" + destination)
            stream = archive.extractfile(member)
            if not member.isfile() or stream is None or stream.read() != (ROOT / source).read_bytes():
                raise ValueError("Sdist resource bytes differ")
    print(f"wheel/sdist: {len(expected)} source modules and canonical resources match")
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
assert names
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
print('installed: all package imports, field assignment, input-only Hero Level 4, no dependencies/network: PASS')
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


def smoke_installed_contract(wheel: Path) -> None:
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
        'report_schema_version': '1.1', 'started_at': '2026-09-19T00:00:00+00:00',
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


def smoke_installed_assembly(wheel: Path) -> None:
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
    'report_schema_version': '1.1', 'started_at': None, 'completed_at': None,
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
assert payload['capabilities']['lineage']['execution_status'] == 'not_requested'
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


def smoke_installed_privacy(wheel: Path) -> None:
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
    'report_schema_version': '1.1', 'started_at': None, 'completed_at': None,
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
assert payload['capabilities']['lineage']['execution_status'] == 'not_requested'
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


def smoke_installed_renderers(wheel: Path) -> None:
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
assert views[0][2]['capabilities']['lineage']['execution_status'] == 'not_requested'
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


def smoke_installed_publication(wheel: Path) -> None:
    """Exercise installed output safety outside the source checkout."""
    with tempfile.TemporaryDirectory(prefix="rit-p4-step6-installed-") as temporary:
        work = Path(temporary)
        subprocess.run([sys.executable, "-m", "venv", str(work / "venv")], check=True)
        bindir = work / "venv" / ("Scripts" if os.name == "nt" else "bin")
        python = bindir / ("python.exe" if os.name == "nt" else "python")
        subprocess.run([str(python), "-m", "pip", "install", "--no-index", "--no-deps", str(wheel.resolve())], cwd=work, check=True)
        program = 'import importlib.abc, json, os, socket, sys\nfrom pathlib import Path\nclass BlockOptional(importlib.abc.MetaPathFinder):\n    def find_spec(self, fullname, path=None, target=None):\n        if fullname.split(".")[0] in ("numpy", "pandas", "pyarrow"):\n            raise AssertionError("optional or analytical dependency imported")\nsys.meta_path.insert(0, BlockOptional())\ndef phase4_step6_view(mode="standard", label="publication-case"):\n    from recursive_integrity_toolkit.reports.assembly import privacy_view\n    from recursive_integrity_toolkit.result import CanonicalReport\n    from recursive_integrity_toolkit.utils.hashing import IdentifierProtection\n\n    payload = {\n        "run": {\n            "run_id": label, "toolkit_version": "0.1.0.dev2", "report_schema_version": "1.1",\n            "started_at": "2026-09-20T00:00:00+00:00", "completed_at": "2026-09-20T00:00:00.500000+00:00",\n            "duration_seconds": 0.5, "python_version": "3.12.14", "platform": "independent-test-platform",\n            "command": "rit validate", "config_hash": "0123456789abcdef" * 4,\n            "random_seed": None, "strict_mode": False, "redacted_mode": False,\n            "network_call_count": 0, "deterministic": True, "privacy_mode": "standard",\n            "run_status": "complete", "null_reasons": {"random_seed": "No stochastic scenario was requested."},\n        },\n        "inputs": {}, "observability": {}, "capabilities": {}, "observed_facts": {},\n        "derived_metrics": {}, "proxy_signals": {}, "simulations": {},\n        "unavailable_conclusions": [], "recommended_next_metadata": [], "warnings": [], "errors": [],\n    }\n    return privacy_view(CanonicalReport.from_dict(payload), mode=mode,\n                        protection=IdentifierProtection.create(secret=b"publication-test-only-key-32byte!"))\nfrom recursive_integrity_toolkit.utils.paths import publish_reports, PublicationResult\nfrom recursive_integrity_toolkit.utils.logging import format_publication_diagnostic\nfrom recursive_integrity_toolkit.utils import paths\nfrom recursive_integrity_toolkit.reports.json_report import render_json\nfrom recursive_integrity_toolkit.reports.markdown_report import render_markdown\nimport recursive_integrity_toolkit as package\nassert not Path(package.__file__).resolve().is_relative_to(Path(sys.argv[2]).resolve())\nwork=Path(sys.argv[1]); source=work/\'input.txt\'; source.write_bytes(b\'PRIVATE_INSTALLED_SOURCE\')\nview=phase4_step6_view(\'redacted\')\nexpected={\'report.json\':render_json(view).encode(), \'report.md\':render_markdown(view).encode()}\ndef deny(*args, **kwargs):\n    raise AssertionError(\'network forbidden\')\nsocket.socket=deny; socket.getaddrinfo=deny\nactual_open=os.open\ndef no_input(path,*args,**kwargs):\n    assert Path(path)!=source\n    return actual_open(path,*args,**kwargs)\nos.open=no_input\ndef no_analysis(frame,event,arg):\n    if event==\'call\':\n        name=frame.f_globals.get(\'__name__\',\'\')\n        assert not name.startswith((\'recursive_integrity_toolkit.io.\',\'recursive_integrity_toolkit.metrics.\',\'recursive_integrity_toolkit.representations.\'))\nsys.setprofile(no_analysis)\ntry:\n    result=publish_reports(view,work/\'out\',input_paths=(source,))\n    assert result==PublicationResult(\'complete\',None,0,(\'report.json\',\'report.md\'))\n    assert publish_reports(view,work/\'out\',input_paths=(source,)).code==\'E_OUTPUT_EXISTS\'\n    actual_publish=paths._output_publish_one\n    def fail_second(src,dst):\n        if dst.name==\'report.md\':raise OSError(\'PRIVATE_INSTALLED_FAILURE\')\n        return actual_publish(src,dst)\n    paths._output_publish_one=fail_second\n    failed=publish_reports(view,work/\'failure\',input_paths=(source,))\n    assert failed.status==\'failed\' and failed.code==\'E_OUTPUT_IO\' and failed.temporary_cleanup_complete\n    assert \'PRIVATE_\' not in format_publication_diagnostic(failed)\nfinally:\n    sys.setprofile(None)\nassert {p.name:p.read_bytes() for p in (work/\'out\').iterdir()}==expected\nassert list((work/\'failure\').iterdir())==[]\nassert source.read_bytes()==b\'PRIVATE_INSTALLED_SOURCE\'\nprint(\'installed Step 6: exact safe JSON/Markdown bytes, no-overwrite, partial failure cleanup, safe diagnostics, unchanged input, blocked network/analysis: PASS\')\n'
        subprocess.run([str(python), "-I", "-c", program, str(work), str(ROOT)], cwd=work, check=True)


def smoke_installed_cli(wheel: Path) -> None:
    """Run the installed CLI with caller core dependencies outside the checkout."""
    with tempfile.TemporaryDirectory(prefix="rit-p4-step7-installed-") as temporary:
        work = Path(temporary)
        target = work / "installed"
        subprocess.run([sys.executable, "-m", "pip", "install", "--no-index", "--no-deps", "--target", str(target), str(wheel.resolve())], cwd=work, check=True)
        program = "import importlib.abc, json, os, socket, sys\nfrom pathlib import Path\nsys.path.insert(0,sys.argv[1])\nimport recursive_integrity_toolkit as package\nassert Path(package.__file__).resolve().is_relative_to(Path(sys.argv[1]).resolve())\nassert not Path(package.__file__).resolve().is_relative_to(Path(sys.argv[3]).resolve())\nimport numpy,pandas\nclass NoParquet(importlib.abc.MetaPathFinder):\n def find_spec(self,fullname,path=None,target=None):\n  if fullname.split('.')[0]=='pyarrow':raise AssertionError('ordinary CLI requires no optional dependency')\nsys.meta_path.insert(0,NoParquet())\ndef deny(*args,**kwargs):raise AssertionError('network forbidden')\nsocket.socket=deny;socket.getaddrinfo=deny\nwork=Path(sys.argv[2]);records=work/'records.jsonl';config=work/'config.json'\nrecords.write_text('\\n'.join(json.dumps({'dataset_version':'v1','record_id':str(i),'content':'PRIVATE_CONTENT_'+str(i),'topic':topic}) for i,topic in enumerate(('A','A','B','C'))),encoding='utf-8')\nconfig.write_text(json.dumps({'representation':{'name':'topic','source':'topic_field','field':'topic','version':'1','missing_value_policy':'exclude'}}),encoding='utf-8')\nbefore=records.read_bytes()\nfrom recursive_integrity_toolkit.cli import main\nassert main(['audit','--records',str(records),'--config',str(config),'--out',str(work/'audit')])==0\nreport=json.loads((work/'audit/report.json').read_bytes())\nassert report['derived_metrics']['support']['by_version']['v1']['support_size']['value']==3\nassert report['derived_metrics']['diversity']['by_version']['v1']['gini_simpson_diversity']['value']==0.625\nassert report['simulations']=={} and report['run']['network_call_count']==0\nfrom recursive_integrity_toolkit import cli\ndef no_calculations(*args,**kwargs):raise AssertionError('validate invoked calculations')\noriginal_calculations=cli._calculations\ncli._calculations=no_calculations\nassert main(['validate','--records',str(records),'--out',str(work/'validate'),'--redacted'])==0\nvalidated=json.loads((work/'validate/report.json').read_bytes())\nassert validated['derived_metrics']==validated['proxy_signals']==validated['simulations']=={}\nassert records.read_bytes()==before\nassert all((work/name/'report.md').read_text(encoding='utf-8').startswith('# Recursive Integrity Audit Report') for name in ('audit','validate'))\nassert all('PRIVATE_CONTENT_' not in (work/name/file).read_text(encoding='utf-8') for name in ('audit','validate') for file in ('report.json','report.md'))\ncli._calculations=original_calculations\nimport importlib.metadata,runpy\nentries={entry.name:entry for entry in importlib.metadata.distribution('recursive-integrity-toolkit').entry_points}\nfor alias in ('rit','recursive-integrity'):\n assert entries[alias].load()(['version'])==0\n assert entries[alias].load()(['audit','--records',str(records),'--config',str(config),'--out',str(work/alias),'--redacted'])==0\nsys.argv=['rit','validate','--records',str(records),'--out',str(work/'module'),'--redacted']\ntry:runpy.run_module('recursive_integrity_toolkit',run_name='__main__')\nexcept SystemExit as error:assert error.code==0\nelse:raise AssertionError('module invocation did not exit')\nprint('installed Step 7: external local inputs, core dependencies, ordinary audit and input-only validate, blocked network, unchanged inputs: PASS')\n"
        subprocess.run([sys.executable, "-I", "-c", program, str(target), str(work), str(ROOT)], cwd=work, check=True)


def installed_example_program() -> str:
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
assert report['capabilities']['lineage']['execution_status']=='not_requested'
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
for name,privacy in (('lineage',[]),('lineage-redacted',['--redacted'])):
 destination=work/name
 assert main(['example','--lineage','--out',str(destination),*privacy])==0
 current=json.loads((destination/'reports/report.json').read_bytes())
 jsonschema.Draft202012Validator(json.loads(resources.joinpath('data','report.schema.json').read_bytes())).validate(current)
 assert current['run']['report_schema_version']=='1.1' and current['run']['run_status']=='complete'
 assert current['capabilities']['lineage']['execution_status']=='completed'
 assert current['capabilities']==current['observability']['capabilities']
 assert current['simulations']=={} and current['errors']==[]
 facts=current['observed_facts']['lineage'];metrics=current['derived_metrics']['lineage']
 graph=facts['graph_scope']['value']
 assert (graph['target_record_count'],graph['loaded_record_count'],graph['context_record_count'])==(8,16,8)
 assert [metrics[k]['value'] for k in ('grounded_record_count','closed_record_count','unresolved_record_count')]==[8,0,0]
 assert metrics['distinct_external_root_count']['value']==5
 assert metrics['ancestry_concentration_hhi']['value']==0.25
 assert metrics['effective_external_root_count']['value']==4.0
 assert [metrics[k]['value'] for k in ('resolved_lineage_coverage','external_ancestry_coverage','resolved_parent_edge_coverage')]==[1.0,1.0,1.0]
 assert facts['declared_parent_edge_count']['value']==facts['resolved_parent_edge_count']['value']==8
 assert facts['cycle_status']['value']=='acyclic'
 roots=metrics['top_shared_ancestors']['value']['items']
 assert [root['incidence_count'] for root in roots]==[3,2,1,1,1]
 assert [root['normalized_weight'] for root in roots]==[3/8,2/8,1/8,1/8,1/8]
 assert [current['derived_metrics']['closure_exposure']['lineage'][k]['value'] for k in ('lower_bound','upper_bound','interval_width')]==[0.0,0.0,0.0]
 assert [current['derived_metrics']['closure_exposure']['direct'][k]['value'] for k in ('lower_bound','upper_bound','interval_width')]==[0.5,0.5,0.0]
 assert current['derived_metrics']['support']['support_delta']['value']==-3
 assert current['derived_metrics']['diversity']['gini_simpson_diversity_delta']['value']==-0.125
 assert current['proxy_signals']['shared_ancestry_dependence']['level']=='present'
 assert {'model_performance_decline','causal_ancestor_effect','universal_integrity','universal_collapse_prediction'} <= {x['conclusion'] for x in current['unavailable_conclusions']}
 markdown=(destination/'reports/report.md').read_text(encoding='utf-8')
 assert '`["derived_metrics"]["lineage"]["ancestry_concentration_hhi"]`' in markdown
 if privacy:
  assert str(work) not in (destination/'reports/report.json').read_text(encoding='utf-8')
  assert str(work) not in markdown
  assert all(root['record_key']['record_id'] not in {f'v1_{i:02d}' for i in range(1,9)} for root in roots)
 else:
  assert graph['target_dataset_version']=='v2'
  assert roots[0]['record_key']=={'dataset_version':'v1','record_id':'v1_01'}
 for p in (destination/'inputs').iterdir():
  assert p.read_bytes()==resources.joinpath('data','hero',p.name).read_bytes()
for relative,digest in expected.items():
 assert hashlib.sha256(resources.joinpath(*relative.split('/')).read_bytes()).hexdigest()==digest
for p in (target/'inputs').iterdir():
 assert p.read_bytes()==resources.joinpath('data','hero',p.name).read_bytes()
print('installed Hero: ordinary and explicit lineage, frozen numerical oracles, local schema, exact resources, core-only, standard/redacted, no overwrite, blocked network: PASS')
'''


def smoke_installed_example(wheel: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="rit-p4-step8-wheel-") as temporary:
        work = Path(temporary)
        target = work / "installed"
        subprocess.run([sys.executable, "-m", "pip", "install", "--no-index", "--no-deps", "--target", str(target), str(wheel.resolve())], cwd=work, check=True)
        hashes = {destination.removeprefix("src/recursive_integrity_toolkit/"): hashlib.sha256((ROOT/source).read_bytes()).hexdigest() for destination,source in RESOURCES.items()}
        subprocess.run([sys.executable, "-I", "-c", installed_example_program(), str(target), str(work), str(ROOT), json.dumps(hashes)], cwd=work, check=True)


def extract_sdist(sdist: Path, destination: Path) -> Path:
    """Preflight regular archive members before copying any source bytes."""
    with tarfile.open(sdist, "r:gz") as archive:
        members = archive.getmembers()
        names = [member.name for member in members]
        if len(names) != len(set(names)):
            raise ValueError("Duplicate sdist entries")
        roots = {PurePosixPath(name).parts[0] for name in names if PurePosixPath(name).parts}
        if len(roots) != 1:
            raise ValueError("Sdist needs exactly one root")
        for member in members:
            parts = PurePosixPath(member.name).parts
            if (not parts or member.name.startswith("/") or ".." in parts
                    or "\\" in member.name or any(":" in part for part in parts)
                    or not (member.isdir() or member.isfile())):
                raise ValueError("Unsafe sdist member")
            target = destination.joinpath(*parts)
            if any(path.is_symlink() for path in (target, *target.parents)):
                raise ValueError("Aliased sdist extraction destination")
        for member in members:
            if member.isdir():
                continue
            target = destination / member.name
            target.parent.mkdir(parents=True, exist_ok=True)
            stream = archive.extractfile(member)
            if stream is None:
                raise ValueError("Missing regular sdist content")
            target.write_bytes(stream.read())
    return destination / next(iter(roots))


def smoke_sdist(sdist: Path) -> None:
    """Extract regular sdist members and audit without build/download operations."""
    with tempfile.TemporaryDirectory(prefix="rit-p4-step8-sdist-") as temporary:
        work = Path(temporary)
        source = extract_sdist(sdist, work / "source") / "src"
        hashes = {destination.removeprefix("src/recursive_integrity_toolkit/"): hashlib.sha256((ROOT/original).read_bytes()).hexdigest() for destination,original in RESOURCES.items()}
        subprocess.run([sys.executable, "-I", "-c", installed_example_program(), str(source), str(work), str(ROOT), json.dumps(hashes)], cwd=work, check=True)


def smoke_all(wheel: Path, sdist: Path) -> None:
    for check in (smoke_installed, smoke_installed_duplicates, smoke_installed_contract,
                  smoke_installed_assembly, smoke_installed_privacy, smoke_installed_renderers,
                  smoke_installed_publication, smoke_installed_cli, smoke_installed_example):
        check(wheel)
    smoke_sdist(sdist)


def _canonical_identities() -> set[tuple[str, str]]:
    env = dict(os.environ, PYTHONPATH=str(ROOT / "src"), PYTHONDONTWRITEBYTECODE="1", RIT_TEST_PARQUET="1")
    result = subprocess.run([sys.executable, "-m", "pytest", "-p", "no:cacheprovider",
                             "--collect-only", "-q", "--ignore=tests/performance"],
                            cwd=ROOT, env=env, capture_output=True, text=True, check=True)
    nodes = [line.strip() for line in result.stdout.splitlines() if line.startswith("tests/") and "::" in line]
    if not nodes or len(nodes) != len(set(nodes)):
        raise ValueError("Canonical collection is empty or has duplicate identities")
    identities = set()
    for node in nodes:
        base, bracket, parameter = node.partition("[")
        owner, name = base.rsplit("::", 1)
        identities.add((owner.removesuffix(".py").replace("/", ".").replace("::", "."), name + bracket + parameter))
    return identities


def candidate(output: Path) -> None:
    """Verify a committed candidate; workflow separately requires its scale job.

    Core/Parquet JUnit must belong to this source revision, checked by the existing
    workflow before invocation. This entry point does not prove their origin.
    """
    if os.environ.get("RIT_TEST_PARQUET") != "1" or importlib.util.find_spec("pyarrow") is None:
        raise ValueError("Candidate verification requires RIT_TEST_PARQUET=1 and real PyArrow")
    if git("status", "--porcelain").strip():
        raise ValueError("Candidate archive requires committed, clean source")
    result = audit()
    expected = _canonical_identities()
    for name, parquet in (("core.xml", False), ("parquet.xml", True)):
        result[name] = verify_junit(output / name, require_parquet=parquet)
        actual = {(case.get("classname", ""), case.get("name", ""))
                  for case in ET.parse(output / name).getroot().iter("testcase")}
        required = expected if parquet else {item for item in expected if item[1] not in PARQUET_CASES}
        if actual != required:
            raise ValueError(f"Candidate JUnit does not execute the complete canonical regression suite: {name}")
    wheel, sdist = verify_distributions(output / "dist")
    smoke_all(wheel, sdist)
    archive = output / "recursive-integrity-toolkit-source.zip"
    subprocess.run(["git", "-C", str(ROOT), "archive", "--format=zip",
                    "--prefix=recursive-integrity-toolkit/", "HEAD", "-o", str(archive.resolve())], check=True)
    tracked = {name for name in git("ls-files", "-z").decode().split("\0") if name}
    with zipfile.ZipFile(archive) as zipped:
        entries = [member.filename for member in zipped.infolist() if not member.is_dir()]
        prefix = "recursive-integrity-toolkit/"
        if len(entries) != len(set(entries)) or {name.removeprefix(prefix) for name in entries} != tracked:
            raise ValueError("Candidate source archive file set mismatch")
        for name in tracked:
            if zipped.read(prefix + name) != (ROOT / name).read_bytes():
                raise ValueError(f"Candidate source archive byte mismatch: {name}")
    result.update(commit=git("rev-parse", "HEAD").decode().strip(),
                  source_archive=archive.name, tracked_files=len(tracked),
                  canonical_scope="tests excluding performance; designated scale job required separately",
                  python=sys.version, platform=sys.platform)
    (output / "candidate.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("Current candidate package and installation checks: PASS; no publication performed")


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if any(arg in {"--phase", "--step"} or arg.startswith(("--phase=", "--step=")) for arg in argv):
        raise SystemExit("Historical phase dispatch has been retired. Run the current command without --phase/--step; use Git history at the accepted commit to inspect prior gates.")
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--junit", type=Path)
    modes.add_argument("--dist", type=Path)
    modes.add_argument("--smoke-wheel", type=Path)
    modes.add_argument("--candidate", type=Path)
    parser.add_argument("--require-parquet", action="store_true")
    parser.add_argument("--minimum-tests", type=int, default=1)
    args = parser.parse_args(argv)
    if args.minimum_tests < 1:
        parser.error("--minimum-tests must be positive")
    if args.junit:
        verify_junit(args.junit, require_parquet=args.require_parquet, minimum=args.minimum_tests)
    elif args.dist:
        audit()
        smoke_all(*verify_distributions(args.dist))
    elif args.smoke_wheel:
        smoke_installed(args.smoke_wheel)
    elif args.candidate:
        candidate(args.candidate)
    else:
        audit()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
