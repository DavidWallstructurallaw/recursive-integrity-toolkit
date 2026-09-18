"""Protect Phase 3 Step 9 scoped metrics from premature analytical implementation."""

import ast
from pathlib import Path


STEP1_EXECUTABLE = {"__init__.py", "__main__.py", "cli.py", "config.py", "errors.py", "models.py"}
STEP2_EXECUTABLE = {"io/loaders.py", "utils/hashing.py", "utils/paths.py"}
STEP3_EXECUTABLE = {"io/schema_mapping.py"}
STEP8_EXECUTABLE = {"observability/levels.py"}
PHASE3_FIELD_EXECUTABLE = {"representations/base.py", "representations/field.py"}
PHASE3_DISTRIBUTION_EXECUTABLE = {"metrics/diversity.py"}
PHASE3_PROVENANCE_EXECUTABLE = {"metrics/provenance.py"}
PHASE3_BOUNDS_EXECUTABLE = {"metrics/bounds.py"}
PHASE3_TAIL_EXECUTABLE = {"metrics/tail.py"}
PHASE3_RESAMPLING_EXECUTABLE = {"metrics/resampling.py"}
PHASE3_PAIR_EXECUTABLE = {"representations/compatibility.py"}
PHASE3_EXACT_EXECUTABLE = {"representations/content_hash.py", "metrics/duplicates.py"}
STEP4_EXECUTABLE = {"io/normalization.py", "io/validation.py", "utils/ordering.py"}
PROTECTED_PREFIXES = {"io", "lineage", "metrics", "observability", "reports", "representations", "utils"}
FORBIDDEN_ANALYTICAL_IMPORT_ROOTS = {"networkx", "scipy", "sklearn", "torch", "tensorflow", "transformers"}
FORBIDDEN_ANALYTICAL_NAMES = {"support_size", "gini_simpson", "tail_fragility", "source_type_shares", "closure_bounds", "ancestry_hhi", "effective_external_roots", "resample", "reopening"}


def _is_docstring_only(path: Path) -> bool:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    return len(tree.body) == 1 and isinstance(tree.body[0], ast.Expr) and isinstance(tree.body[0].value, ast.Constant) and isinstance(tree.body[0].value.value, str)


def test_only_step8_authorized_modules_gain_behavior(package_root) -> None:
    for path in sorted(package_root.rglob("*.py")):
        relative = path.relative_to(package_root)
        if relative.as_posix() in STEP2_EXECUTABLE | STEP3_EXECUTABLE | STEP4_EXECUTABLE | STEP8_EXECUTABLE | PHASE3_FIELD_EXECUTABLE | PHASE3_EXACT_EXECUTABLE | PHASE3_DISTRIBUTION_EXECUTABLE | PHASE3_PROVENANCE_EXECUTABLE | PHASE3_BOUNDS_EXECUTABLE | PHASE3_TAIL_EXECUTABLE | PHASE3_RESAMPLING_EXECUTABLE | PHASE3_PAIR_EXECUTABLE or (len(relative.parts) == 1 and path.name in STEP1_EXECUTABLE):
            continue
        assert _is_docstring_only(path), f"Premature executable body: {relative}"


def test_protected_phase3_plus_modules_remain_placeholders(package_root) -> None:
    for prefix in PROTECTED_PREFIXES:
        for path in sorted((package_root / prefix).rglob("*.py")):
            if path.relative_to(package_root).as_posix() in STEP2_EXECUTABLE | STEP3_EXECUTABLE | STEP4_EXECUTABLE | STEP8_EXECUTABLE | PHASE3_FIELD_EXECUTABLE | PHASE3_EXACT_EXECUTABLE | PHASE3_DISTRIBUTION_EXECUTABLE | PHASE3_PROVENANCE_EXECUTABLE | PHASE3_BOUNDS_EXECUTABLE | PHASE3_TAIL_EXECUTABLE | PHASE3_RESAMPLING_EXECUTABLE | PHASE3_PAIR_EXECUTABLE:
                continue
            assert _is_docstring_only(path), f"Protected module changed after Step 8: {path}"
    assert _is_docstring_only(package_root / "result.py")


def test_no_prohibited_analytical_dependency_imports(package_root) -> None:
    imported_roots = set()
    for path in sorted(package_root.rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_roots.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported_roots.add(node.module.split(".")[0])
    assert not (imported_roots & FORBIDDEN_ANALYTICAL_IMPORT_ROOTS)


def test_no_analytical_function_names_exist(package_root) -> None:
    names = set()
    for path in sorted(package_root.rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        names.update(node.name for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)))
    assert not (names & FORBIDDEN_ANALYTICAL_NAMES)


def test_PR003_traceability_script_enforces_step8_scope(repo_root) -> None:
    import subprocess
    import sys
    result = subprocess.run([sys.executable, "scripts/check_traceability.py"],
                            cwd=repo_root, capture_output=True, text=True, check=False)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "protected docstring-only modules: 16" in result.stdout


# The checker itself must reject new work outside the current Step 8 boundary.
import shutil
import subprocess
import sys
import pytest


@pytest.mark.parametrize("relative,injected", [
    ("io/validation.py", '_read_source(None, None)\n'),
    ("io/validation.py", 'load_table(None)\n'),
    ("io/validation.py", 'inventory_source(None)\n'),
    ("io/validation.py", "load_content_reference('x')\n"),
    ("io/validation.py", 'validate_bundle(None)\n'),
    ("io/validation.py", '_bundle_control(None, None)\n'),
    ("io/validation.py", 'from .loaders import load_table\n'),
    ("io/validation.py", 'from .normalization import normalize_row\n'),
    ("io/validation.py", 'from .loaders import _parse_csv\n'),
    ("io/validation.py", "Path('x').write_text('data')\n"),

    ("observability/levels.py", "import socket\n"),
    ("observability/levels.py", "from ..metrics import diversity\n"),
    ("observability/levels.py", "from ..lineage import graph\n"),
    ("observability/levels.py", "from ..io.loaders import load_table\n"),
    ("observability/levels.py", "eval('1')\n"),
    ("observability/levels.py", "open('unexpected')\n"),
    ("observability/levels.py", "lambda: None\n"),
    ("observability/levels.py", "math.sqrt(4)\n"),
    ("observability/levels.py", "math.fsum((0.5, 0.5))\n"),
    ("observability/levels.py", "1 - 0.5 ** 2\n"),
    ("observability/levels.py", "1 / 2\n"),
    ("observability/levels.py", "def universal_score(): pass\n"),

    ("utils/paths.py", "import socket\n"),
    ("utils/paths.py", "eval('1')\n"),
    ("utils/paths.py", "os.system('unapproved')\n"),
    ("utils/paths.py", "Path('x').write_text('unapproved')\n"),
    ("io/loaders.py", "__import__('socket')\n"),
    ("io/loaders.py", "os.remove('unapproved')\n"),
    ("io/schema_mapping.py", "def premature(): pass\n"),
    ("io/normalization.py", "def premature(): pass\n"),
    ("io/validation.py", "def premature(): pass\n"),
    ("observability/levels.py", "def premature(): pass\n"),
    ("metrics/diversity.py", "def premature(): pass\n"),
    ("lineage/graph.py", "def premature(): pass\n"),
    ("representations/field.py", "def premature(): pass\n"),
    ("reports/assembly.py", "def premature(): pass\n"),
    ("utils/ordering.py", "def premature(): pass\n"),
    ("result.py", "def premature(): pass\n"),
    ("io/loaders.py", "def premature(): pass\n"),
    ("io/loaders.py", "import pyarrow\n"),
    ("io/loaders.py", "import pandas\n"),
    ("models.py", "import math\n"),
    ("io/normalization.py", "import socket\n"),
    ("io/normalization.py", "import pandas\n"),
    ("io/normalization.py", "eval('1')\n"),
    ("io/normalization.py", "open('unapproved')\n"),
    ("io/validation.py", "def derive_generation(): pass\n"),
    ("io/validation.py", "import networkx\n"),
    ("io/validation.py", "open('unapproved')\n"),
    ("io/validation.py", "def source_type_shares(): pass\n"),
    ("io/validation.py", "def closure_bounds(): pass\n"),
    ("io/validation.py", "def resolve_parents(): pass\n"),
    ("models.py", "class UniversalScore: pass\n"),
    ("io/validation.py", "def detect_cycles(): pass\n"),
    ("io/validation.py", "def lineage_depth(): pass\n"),
    ("io/validation.py", "import socket\n"),
    ("models.py", "__import__('socket')\n"),
    ("models.py", "eval('1')\n"),
    ("models.py", "lambda: None\n"),
    ("utils/ordering.py", "def version_rank(): pass\n"),
    ("io/schema_mapping.py", "import os\n"),
    ("io/schema_mapping.py", "import socket\n"),
    ("io/schema_mapping.py", "eval('1')\n"),
    ("io/schema_mapping.py", "exec('pass')\n"),
    ("io/schema_mapping.py", "__import__('os')\n"),
    ("io/schema_mapping.py", "lambda: None\n"),
    ("io/schema_mapping.py", "Path('unexpected').write_text('x')\n"),
])
def test_PR002_checker_rejects_unauthorized_mutations(repo_root, package_root, tmp_path, relative, injected):
    target = tmp_path / "repo"
    script = target / "scripts/check_traceability.py"
    script.parent.mkdir(parents=True)
    script.write_bytes((repo_root / "scripts/check_traceability.py").read_bytes())
    copied = target / "src/recursive_integrity_toolkit"
    shutil.copytree(package_root, copied, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    path = copied / relative
    path.write_text(path.read_text(encoding="utf-8") + "\n" + injected, encoding="utf-8")
    result = subprocess.run([sys.executable, str(script)], capture_output=True, text=True, check=False)
    assert result.returncode != 0, f"Unauthorized implementation accepted: {relative}"
    assert any(word in result.stderr for word in ("Protected", "Unexpected", "Dependency", "Import")), result.stderr


# Phase 3 Step 2: retain all prior negative identities and add pure-field gates.
@pytest.mark.parametrize("relative", ["representations/base.py", "representations/field.py"])
@pytest.mark.parametrize("injection", [
    "import socket\n", "from ..metrics import diversity\n", "from ..models import __builtins__\n",
    "from ..config import RepresentationConfig as eval\n", "value = 1\n",
    "open('private')\n", "eval('1')\n", "lambda: None\n",
    "def support_size(): return 1\n", "from ..io.loaders import load_table\n",
])
def test_phase3_step2_injected_later_feature_is_rejected(repo_root, tmp_path, relative, injection):
    target = tmp_path / "gate"
    shutil.copytree(repo_root / "src", target / "src", ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    (target / "scripts").mkdir()
    shutil.copy2(repo_root / "scripts/check_traceability.py", target / "scripts/check_traceability.py")
    file = target / "src/recursive_integrity_toolkit" / relative
    file.write_text(file.read_text(encoding="utf-8") + "\n" + injection, encoding="utf-8")
    result = subprocess.run([sys.executable, str(target / "scripts/check_traceability.py")],
                            cwd=target, text=True, capture_output=True)
    assert result.returncode != 0, result.stdout + result.stderr


@pytest.mark.parametrize("body", [
    "return sum(values)", "return values ** 2", "return value / 2", "return value * value",
    "return open(value)", "return values.pop()", "return callback(values)",
    "return __import__('numpy')", "return (lambda: value)()", "return value.lower()",
])
def test_phase3_step2_hidden_computation_is_rejected(repo_root, body):
    import runpy
    checker = runpy.run_path(str(repo_root / "scripts/check_traceability.py"), run_name="field_gate")
    with pytest.raises(SystemExit):
        checker["_phase3_representation_boundary"](
            ast.parse("def _selection():\n    " + body + "\n"), "representations/field.py")


@pytest.mark.parametrize("path", ["PHASE_3_PLAN.md", "tests/golden/phase3_math_cases.json",
    "src/recursive_integrity_toolkit/metrics/diversity.py", "src/recursive_integrity_toolkit/io/validation.py",
    "VALIDATION_PLAN.md", "pyproject.toml"])
def test_phase3_step2_incremental_scope_rejects_unapproved_edits(repo_root, path):
    import runpy
    checker = runpy.run_path(str(repo_root / "scripts/release_check.py"), run_name="step2_paths")
    with pytest.raises(ValueError):
        checker["verify_prior_step_changes"]([("M", path)], step=2)


@pytest.mark.parametrize("change", ["none", "extra_newline", "skip", "numeric_expectation", "wrong_type"])
def test_phase3_step2_contract_test_exception_is_exact(repo_root, change):
    import runpy
    checker = runpy.run_path(str(repo_root / "scripts/release_check.py"), run_name="step2_exception")
    after = (repo_root / "tests/unit/test_phase3_contracts.py").read_bytes()
    before = after.replace(b"control[key]+=1", b"control[key]=2", 1)
    checker["verify_step2_contract_test_migration"](before, after)
    if change == "none": bad = before
    elif change == "extra_newline": bad = after + b"\n"
    elif change == "skip": bad = b"# skipped\n" + after
    elif change == "numeric_expectation": bad = after.replace(b'=="5/8"', b'=="1/2"')
    else: bad = after.decode()
    with pytest.raises(ValueError):
        checker["verify_step2_contract_test_migration"](before, bad)


# Phase 3 Step 3: inherited identities stay; exact-content modules have bounded calls.
@pytest.mark.parametrize("relative", ["representations/content_hash.py", "metrics/duplicates.py"])
@pytest.mark.parametrize("injection", [
    "import socket\n", "from ..io.loaders import load_table\n", "from ..metrics import diversity\n",
    "from ..utils.hashing import sha256_bytes as eval\n", "from ..models import __builtins__\n",
    "open('private')\n", "def semantic_support(): return 1\n", "x = 1\n",
    "lambda: None\n", "eval('1')\n",
])
def test_phase3_step3_later_feature_injection_is_rejected(repo_root, tmp_path, relative, injection):
    target = tmp_path / "gate"
    shutil.copytree(repo_root / "src", target / "src", ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    (target / "scripts").mkdir()
    shutil.copy2(repo_root / "scripts/check_traceability.py", target / "scripts/check_traceability.py")
    file = target / "src/recursive_integrity_toolkit" / relative
    file.write_text(file.read_text(encoding="utf-8") + "\n" + injection, encoding="utf-8")
    result = subprocess.run([sys.executable, str(target / "scripts/check_traceability.py")],
                            cwd=target, text=True, capture_output=True)
    assert result.returncode != 0, result.stdout + result.stderr


@pytest.mark.parametrize("relative", ["representations/content_hash.py", "metrics/duplicates.py"])
@pytest.mark.parametrize("body", [
    "return value ** 2", "return value / 2", "return sum(values)", "return callback(values)",
    "return text.lower()", "return text.casefold()", "return text.replace('a', 'b')",
    "return __import__('numpy')", "return open(value)", "return members.pop()", "value += 1",
])
def test_phase3_step3_hidden_operation_is_rejected(repo_root, relative, body):
    import runpy
    checker = runpy.run_path(str(repo_root / "scripts/check_traceability.py"), run_name="exact_gate")
    with pytest.raises(SystemExit):
        checker["_phase3_exact_boundary"](ast.parse("def helper():\n    " + body + "\n"), relative)


@pytest.mark.parametrize("path", ["tests/unit/test_phase3_contracts.py",
    "src/recursive_integrity_toolkit/representations/base.py",
    "src/recursive_integrity_toolkit/representations/field.py",
    "src/recursive_integrity_toolkit/utils/hashing.py", "tests/golden/phase3_math_cases.json"])
def test_phase3_step3_incremental_scope_keeps_prior_implementations_frozen(repo_root, path):
    import runpy
    checker = runpy.run_path(str(repo_root / "scripts/release_check.py"), run_name="step3_paths")
    with pytest.raises(ValueError):
        checker["verify_prior_step_changes"]([("M", path)], step=3)


# Step 4 adds a reviewed-body pin to all inherited phase boundaries.
@pytest.mark.parametrize("injection", [
    "import socket", "from math import log", "from ..io.loaders import load_table",
    "from ..metrics.resampling import resample", "from ..lineage import graph",
    "from math import fsum as eval", "open('private')", "x=1",
    "def shannon_entropy(): return 1", "def support_delta(): return 1",
    "def closure_bounds(): return 1",
])
def test_phase3_step4_later_injection_rejected(repo_root,tmp_path,injection):
    target=tmp_path/"step4-gate"
    shutil.copytree(repo_root/"src",target/"src",ignore=shutil.ignore_patterns("__pycache__","*.pyc"))
    (target/"scripts").mkdir()
    shutil.copy2(repo_root/"scripts/check_traceability.py",target/"scripts/check_traceability.py")
    p=target/"src/recursive_integrity_toolkit/metrics/diversity.py"
    p.write_text(p.read_text(encoding="utf-8")+"\n"+injection+"\n",encoding="utf-8")
    result=subprocess.run([sys.executable,str(target/"scripts/check_traceability.py")],cwd=target,capture_output=True,text=True)
    assert result.returncode!=0


@pytest.mark.parametrize("old,new", [
    ("value * value", "value ** 3"), ("1.0 - concentration", "1.0 - concentration / 2"),
    ("count / total", "count / (total + 1)"), ("if value > 0", "if value >= 0"),
    ("counts.get(state, 0) + 1", "counts.get(state, 0) + 2"),
    ("return value", "return eval(value)"),
])
def test_phase3_step4_hidden_formula_changes_rejected(repo_root,old,new):
    import runpy
    gate=runpy.run_path(str(repo_root/"scripts/check_traceability.py"),run_name="step4-ast")
    source=(repo_root/"src/recursive_integrity_toolkit/metrics/diversity.py").read_text(encoding="utf-8")
    assert old in source
    gate["_phase3_distribution_boundary"](ast.parse(source))
    with pytest.raises(SystemExit): gate["_phase3_distribution_boundary"](ast.parse(source.replace(old,new,1)))


@pytest.mark.parametrize("path", [
    "src/recursive_integrity_toolkit/metrics/resampling.py", "src/recursive_integrity_toolkit/metrics/provenance.py",
    "src/recursive_integrity_toolkit/metrics/duplicates.py", "src/recursive_integrity_toolkit/io/validation.py",
    "src/recursive_integrity_toolkit/representations/base.py", "docs/data_schema.md", "docs/privacy.md",
    "pyproject.toml", "PHASE_3_PLAN.md", "tests/golden/phase3_math_cases.json",
])
def test_phase3_step4_unapproved_paths_rejected(repo_root,path):
    import runpy
    gate=runpy.run_path(str(repo_root/"scripts/release_check.py"),run_name="step4-path")
    with pytest.raises(ValueError): gate["verify_prior_step_changes"]([("M",path)],step=4)


def test_phase3_step4_current_and_historical_permissions_separate(repo_root):
    import runpy
    gate=runpy.run_path(str(repo_root/"scripts/release_check.py"),run_name="step4-authorization")
    path="src/recursive_integrity_toolkit/metrics/diversity.py"
    gate["verify_prior_step_changes"]([("M",path)],step=4)
    for step in (1,2,3):
        with pytest.raises(ValueError): gate["verify_prior_step_changes"]([("M",path)],step=step)


# Step 5 retains the reviewed positive control and rejects future behavior.
@pytest.mark.parametrize('injection',[
    'import socket', 'from ..io.loaders import load_table', 'from ..lineage import graph',
    'from .bounds import direct_closure_bounds', 'from math import log', 'from math import fsum as eval',
    "open('private')", 'x = 1', 'def confidence_score(): return 1',
    'def effective_source_diversity(): return 1', 'def closure_bounds(): return 1', 'def resample(): return 1',
])
def test_phase3_step5_rejects_later_features(repo_root,injection):
    import runpy
    gate=runpy.run_path(str(repo_root/'scripts/check_traceability.py'),run_name='step5-boundary')
    source=(repo_root/'src/recursive_integrity_toolkit/metrics/provenance.py').read_text(encoding='utf-8')
    gate['_phase3_provenance_boundary'](ast.parse(source))
    with pytest.raises(SystemExit):gate['_phase3_provenance_boundary'](ast.parse(source+'\n'+injection+'\n'))


@pytest.mark.parametrize('old,new',[
    ('counts[value] += 1','counts[value] += 2'),
    ('counts[c] / len(entries)','counts[c] / (len(entries) + 1)'),
    ('elif not row.required_fields_valid:', 'elif False:'),
    ('mass / total','mass / (total + 1)'),
    ('if row is None:\n            continue','if row is None:\n            counts["unknown"] += 1\n            continue'),
])
def test_phase3_step5_rejects_in_body_changes(repo_root,old,new):
    import runpy
    gate=runpy.run_path(str(repo_root/'scripts/check_traceability.py'),run_name='step5-formula')
    source=(repo_root/'src/recursive_integrity_toolkit/metrics/provenance.py').read_text(encoding='utf-8')
    assert old in source
    gate['_phase3_provenance_boundary'](ast.parse(source))
    with pytest.raises(SystemExit):gate['_phase3_provenance_boundary'](ast.parse(source.replace(old,new,1)))


@pytest.mark.parametrize('path',[
    'src/recursive_integrity_toolkit/metrics/bounds.py','src/recursive_integrity_toolkit/metrics/diversity.py',
    'src/recursive_integrity_toolkit/metrics/resampling.py','src/recursive_integrity_toolkit/metrics/duplicates.py',
    'src/recursive_integrity_toolkit/io/validation.py','src/recursive_integrity_toolkit/lineage/graph.py',
    'docs/data_schema.md','docs/privacy.md','pyproject.toml','PHASE_3_PLAN.md',
    'tests/unit/test_phase3_contracts.py','tests/golden/phase3_math_cases.json',
])
def test_phase3_step5_unapproved_paths_rejected(repo_root,path):
    import runpy
    gate=runpy.run_path(str(repo_root/'scripts/release_check.py'),run_name='step5-path')
    with pytest.raises(ValueError):gate['verify_prior_step_changes']([('M',path)],step=5)


def test_phase3_step5_permissions_keep_prior_boundaries(repo_root):
    import runpy
    gate=runpy.run_path(str(repo_root/'scripts/release_check.py'),run_name='step5-permissions')
    path='src/recursive_integrity_toolkit/metrics/provenance.py'
    gate['verify_prior_step_changes']([('M',path)],step=5)
    for step in (1,2,3,4):
        with pytest.raises(ValueError):gate['verify_prior_step_changes']([('M',path)],step=step)
    assert gate['STEP5_NEW']=={
        'tests/fixtures/provenance_partial/phase3_composition.json',
        'tests/fixtures/provenance_unknown/phase3_grounding_crossed.json',
        'tests/fixtures/weighted/phase3_source_weights.json'}


# Step 6 historical gates remain; only direct interval computation is newly opened.
@pytest.mark.parametrize('injection',[
    'import socket','from ..lineage import graph','from .resampling import resample',
    'open("private")','x = 1','def midpoint(): return 0.5','def risk_score(): return 1',
    'def classify_lineage_grounding(): return 1','def ancestry_hhi(): return 1',
])
def test_phase3_step6_rejects_later_bounds_features(repo_root,injection):
    import runpy
    gate=runpy.run_path(str(repo_root/'scripts/check_traceability.py'))
    source=(repo_root/'src/recursive_integrity_toolkit/metrics/bounds.py').read_text()
    gate['_phase3_bounds_boundary'](ast.parse(source))
    with pytest.raises(SystemExit):gate['_phase3_bounds_boundary'](ast.parse(source+'\n'+injection+'\n'))


@pytest.mark.parametrize('old,new',[
    ('lower = known_closed / total','lower = 0.0'),
    ('upper = (known_closed + unresolved) / total','upper = known_closed / total'),
    ('width = unresolved / total','width = 0.0'),
    ('required_cov.numerator == 0','False'),
])
def test_phase3_step6_rejects_formula_and_availability_edits(repo_root,old,new):
    import runpy
    gate=runpy.run_path(str(repo_root/'scripts/check_traceability.py'))
    source=(repo_root/'src/recursive_integrity_toolkit/metrics/bounds.py').read_text()
    assert old in source
    with pytest.raises(SystemExit):gate['_phase3_bounds_boundary'](ast.parse(source.replace(old,new,1)))


@pytest.mark.parametrize('path',[
    'src/recursive_integrity_toolkit/metrics/provenance.py','src/recursive_integrity_toolkit/metrics/diversity.py',
    'src/recursive_integrity_toolkit/metrics/resampling.py','src/recursive_integrity_toolkit/lineage/graph.py',
    'tests/unit/test_phase3_contracts.py','docs/data_schema.md','docs/privacy.md','PHASE_3_PLAN.md','pyproject.toml',
])
def test_phase3_step6_unapproved_file_changes_fail(repo_root,path):
    import runpy
    gate=runpy.run_path(str(repo_root/'scripts/release_check.py'))
    with pytest.raises(ValueError):gate['verify_prior_step_changes']([('M',path)],step=6)


def test_phase3_step6_requires_reviewed_source_bytes(repo_root,tmp_path):
    import runpy
    gate=runpy.run_path(str(repo_root/'scripts/check_traceability.py'))
    source=(repo_root/'src/recursive_integrity_toolkit/metrics/bounds.py').read_text()
    (tmp_path/'metrics').mkdir();(tmp_path/'metrics/bounds.py').write_text(source+'\nx = 1\n')
    gate['_phase3_bounds_boundary'].__globals__['PACKAGE']=tmp_path
    with pytest.raises(SystemExit):gate['_phase3_bounds_boundary'](ast.parse(source+'\nx = 1\n'))


# Step 7: only observed tail/rank and analytic one-step F-014 are authorized.
@pytest.mark.parametrize('injection',[
    'import socket','from ..lineage import graph','from .resampling import resample',
    'import numpy.random','open("private")','x = 1','def risk_score(): return 1',
    'def reopen(): return 1','def tail_fragility_signal(): return "high"',
    'def bottom_frequency_quantile(): return 1','def simulate(): return 1',
])
def test_phase3_step7_rejects_later_tail_features(repo_root,injection):
    import runpy
    gate=runpy.run_path(str(repo_root/'scripts/check_traceability.py'))
    source=(repo_root/'src/recursive_integrity_toolkit/metrics/tail.py').read_text()
    gate['_phase3_tail_boundary'](ast.parse(source))
    with pytest.raises(SystemExit):gate['_phase3_tail_boundary'](ast.parse(source+'\n'+injection+'\n'))


@pytest.mark.parametrize('old,new',[
    ('probability = exp(resample_size * log1p(-p))','probability = 0.5'),
    ('row.state_count == 1','row.state_count <= 1'),
    ('row.state_frequency <= options.frequency_threshold','row.state_frequency < options.frequency_threshold'),
    ('row.state_count > 0','row.state_count >= 0'),
    ('CalculationEvidenceClass.SIMULATION if scenario','CalculationEvidenceClass.DERIVED_METRIC if scenario'),
])
def test_phase3_step7_rejects_formula_or_rule_rewrite(repo_root,old,new):
    import runpy
    gate=runpy.run_path(str(repo_root/'scripts/check_traceability.py'))
    source=(repo_root/'src/recursive_integrity_toolkit/metrics/tail.py').read_text()
    assert old in source
    with pytest.raises(SystemExit):gate['_phase3_tail_boundary'](ast.parse(source.replace(old,new,1)))


@pytest.mark.parametrize('path',[
    'src/recursive_integrity_toolkit/metrics/provenance.py','src/recursive_integrity_toolkit/metrics/diversity.py',
    'src/recursive_integrity_toolkit/metrics/bounds.py','src/recursive_integrity_toolkit/metrics/resampling.py',
    'src/recursive_integrity_toolkit/lineage/graph.py','src/recursive_integrity_toolkit/io/validation.py',
    'docs/data_schema.md','docs/privacy.md','PHASE_3_PLAN.md','pyproject.toml',
    'tests/golden/phase3_math_cases.json',
])
def test_phase3_step7_unapproved_file_changes_fail(repo_root,path):
    import runpy
    gate=runpy.run_path(str(repo_root/'scripts/release_check.py'))
    with pytest.raises(ValueError):gate['verify_prior_step_changes']([('M',path)],step=7)


def test_phase3_step7_requires_reviewed_source_bytes(repo_root,tmp_path):
    import runpy
    gate=runpy.run_path(str(repo_root/'scripts/check_traceability.py'))
    source=(repo_root/'src/recursive_integrity_toolkit/metrics/tail.py').read_text()
    (tmp_path/'metrics').mkdir();(tmp_path/'metrics/tail.py').write_text(source+'\nx = 1\n')
    gate['_phase3_tail_boundary'].__globals__['PACKAGE']=tmp_path
    with pytest.raises(SystemExit):gate['_phase3_tail_boundary'](ast.parse(source+'\nx = 1\n'))


# Step 8 authorizes only F-015 and the explicit fixed-state closed sampler.
@pytest.mark.parametrize('injection',[
    'import socket', 'import numpy as np', 'np.random.seed(1)',
    'from ..lineage import graph', 'from ..io.loaders import load_table',
    'open("private")', 'def simulate_reopening(): return 1',
    'def external_reference_loss(): return 1', 'def report(): return "ok"',
    'def auto_simulate(): return 1', 'def universal_score(): return 1',
])
def test_phase3_step8_rejects_unapproved_resampling_features(repo_root,injection):
    import runpy
    gate=runpy.run_path(str(repo_root/'scripts/check_traceability.py'))
    source=(repo_root/'src/recursive_integrity_toolkit/metrics/resampling.py').read_text()
    gate['_phase3_resampling_boundary'](ast.parse(source))
    with pytest.raises(SystemExit):gate['_phase3_resampling_boundary'](ast.parse(source+'\n'+injection+'\n'))


@pytest.mark.parametrize('old,new',[
    ('factor = 1.0 - 1.0 / resample_size','factor = 1.0'),
    ('masses = counts','masses = probabilities'),
    ('np.random.PCG64(seed)','np.random.PCG64()'),
    ('mass == 0 or remaining == 0','remaining == 0'),
    ('corrected = sampled and total != 1.0','corrected = True'),
    ('abs(total - 1.0) > tolerance','abs(total - 1.0) > .1'),
    ('CalculationEvidenceClass.SIMULATION','CalculationEvidenceClass.OBSERVED_FACT'),
    ('replicates: int, scope:', 'replicates: int = 1, scope:'),
])
def test_phase3_step8_rejects_formula_seed_and_evidence_edits(repo_root,old,new):
    import runpy
    gate=runpy.run_path(str(repo_root/'scripts/check_traceability.py'))
    source=(repo_root/'src/recursive_integrity_toolkit/metrics/resampling.py').read_text()
    assert old in source
    with pytest.raises(SystemExit):gate['_phase3_resampling_boundary'](ast.parse(source.replace(old,new,1)))


@pytest.mark.parametrize('path',[
    'src/recursive_integrity_toolkit/metrics/tail.py','src/recursive_integrity_toolkit/metrics/diversity.py',
    'src/recursive_integrity_toolkit/metrics/provenance.py','src/recursive_integrity_toolkit/metrics/bounds.py',
    'src/recursive_integrity_toolkit/io/validation.py','src/recursive_integrity_toolkit/lineage/graph.py',
    'src/recursive_integrity_toolkit/representations/compatibility.py',
    'PHASE_3_PLAN.md','pyproject.toml','tests/golden/phase3_math_cases.json','docs/data_schema.md',
])
def test_phase3_step8_unapproved_file_changes_fail(repo_root,path):
    import runpy
    gate=runpy.run_path(str(repo_root/'scripts/release_check.py'))
    with pytest.raises(ValueError):gate['verify_prior_step_changes']([('M',path)],step=8)


def test_phase3_step8_current_permission_does_not_change_prior_permission(repo_root):
    import runpy
    gate=runpy.run_path(str(repo_root/'scripts/release_check.py'))
    path='src/recursive_integrity_toolkit/metrics/resampling.py'
    gate['verify_prior_step_changes']([('M',path)],step=8)
    for step in range(1,8):
        with pytest.raises(ValueError):gate['verify_prior_step_changes']([('M',path)],step=step)
    assert gate['STEP8_NEW']=={'tests/fixtures/resampling/phase3_closed_cases.json'}


def test_phase3_step8_reviewed_source_bytes_required(repo_root,tmp_path):
    import runpy
    gate=runpy.run_path(str(repo_root/'scripts/check_traceability.py'))
    source=(repo_root/'src/recursive_integrity_toolkit/metrics/resampling.py').read_text()
    (tmp_path/'metrics').mkdir();(tmp_path/'metrics/resampling.py').write_text(source+'\nx = 1\n')
    gate['_phase3_resampling_boundary'].__globals__['PACKAGE']=tmp_path
    with pytest.raises(SystemExit):gate['_phase3_resampling_boundary'](ast.parse(source+'\nx = 1\n'))


# Step 9 opens only compatibility declarations and an explicitly selected pair.
@pytest.mark.parametrize('path,boundary',[
    ('representations/compatibility.py','_phase3_pair_boundary'),
    ('metrics/diversity.py','_phase3_distribution_boundary'),
])
@pytest.mark.parametrize('injection',[
    'import socket', 'from ..io.loaders import load_table', 'from ..lineage import graph',
    'open("private")', 'def compare_all_versions(): return []',
    'def model_performance_delta(): return 1', 'def render_report(): return "ok"',
    'def infer_state_mapping(): return {}',
])
def test_phase3_step9_rejects_unapproved_pair_features(repo_root,path,boundary,injection):
    import runpy
    gate=runpy.run_path(str(repo_root/'scripts/check_traceability.py'))
    source=(repo_root/'src/recursive_integrity_toolkit'/path).read_text(encoding='utf-8')
    gate[boundary](ast.parse(source))
    with pytest.raises(SystemExit):gate[boundary](ast.parse(source+'\n'+injection+'\n'))


@pytest.mark.parametrize('old,new',[
    ('len(right) - len(left)','len(left) - len(right)'),
    ('len(left & right) / len(left)','len(left & right) / len(right)'),
    ('b.gini_simpson_diversity.value - a.gini_simpson_diversity.value','0.0'),
    ('a.scope != context.earlier_scope','False'),
    ('if any(row.state_id not in mapping for row in value.states):','if False:'),
])
def test_phase3_step9_rejects_formula_or_scope_bypass(repo_root,old,new):
    import runpy
    gate=runpy.run_path(str(repo_root/'scripts/check_traceability.py'))
    source=(repo_root/'src/recursive_integrity_toolkit/metrics/diversity.py').read_text(encoding='utf-8')
    assert old in source
    with pytest.raises(SystemExit):gate['_phase3_distribution_boundary'](ast.parse(source.replace(old,new,1)))


@pytest.mark.parametrize('path',[
    'src/recursive_integrity_toolkit/metrics/resampling.py','src/recursive_integrity_toolkit/metrics/tail.py',
    'src/recursive_integrity_toolkit/metrics/provenance.py','src/recursive_integrity_toolkit/metrics/bounds.py',
    'src/recursive_integrity_toolkit/io/validation.py','src/recursive_integrity_toolkit/lineage/graph.py',
    'src/recursive_integrity_toolkit/reports/json_report.py','src/recursive_integrity_toolkit/cli.py',
    'tests/unit/test_phase3_contracts.py','PHASE_3_PLAN.md','tests/golden/phase3_math_cases.json',
    'docs/data_schema.md','docs/privacy.md','pyproject.toml',
])
def test_phase3_step9_prohibits_unlisted_modifications(repo_root,path):
    import runpy
    gate=runpy.run_path(str(repo_root/'scripts/release_check.py'))
    with pytest.raises(ValueError):gate['verify_phase3_changes']([('M',path)],incremental=True)


def test_phase3_step9_current_scope_does_not_change_step8_scope(repo_root):
    import runpy
    gate=runpy.run_path(str(repo_root/'scripts/release_check.py'))
    path='src/recursive_integrity_toolkit/representations/compatibility.py'
    gate['verify_phase3_changes']([('M',path)],incremental=True)
    with pytest.raises(ValueError):gate['verify_prior_step_changes']([('M',path)],step=8)
    assert gate['STEP9_NEW']=={
        'tests/unit/test_T1_compatibility.py','tests/fixtures/representation_compatible/phase3_pair.json',
        'tests/fixtures/representation_incompatible/phase3_pair.json'}


def test_phase3_step9_compatibility_source_bytes_must_be_reviewed(repo_root,tmp_path):
    import runpy
    gate=runpy.run_path(str(repo_root/'scripts/check_traceability.py'))
    source=(repo_root/'src/recursive_integrity_toolkit/representations/compatibility.py').read_text(encoding='utf-8')
    (tmp_path/'representations').mkdir()
    (tmp_path/'representations/compatibility.py').write_text(source+'\nx = 1\n',encoding='utf-8')
    gate['_phase3_pair_boundary'].__globals__['PACKAGE']=tmp_path
    with pytest.raises(SystemExit):gate['_phase3_pair_boundary'](ast.parse(source+'\nx = 1\n'))
