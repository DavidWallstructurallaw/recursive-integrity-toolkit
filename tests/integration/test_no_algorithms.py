"""Protect Phase 2 Step 9 from premature analytical implementation."""

import ast
from pathlib import Path


STEP1_EXECUTABLE = {"__init__.py", "__main__.py", "cli.py", "config.py", "errors.py", "models.py"}
STEP2_EXECUTABLE = {"io/loaders.py", "utils/hashing.py", "utils/paths.py"}
STEP3_EXECUTABLE = {"io/schema_mapping.py"}
STEP8_EXECUTABLE = {"observability/levels.py"}
PHASE3_FIELD_EXECUTABLE = {"representations/base.py", "representations/field.py"}
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
        if relative.as_posix() in STEP2_EXECUTABLE | STEP3_EXECUTABLE | STEP4_EXECUTABLE | STEP8_EXECUTABLE | PHASE3_FIELD_EXECUTABLE or (len(relative.parts) == 1 and path.name in STEP1_EXECUTABLE):
            continue
        assert _is_docstring_only(path), f"Premature executable body: {relative}"


def test_protected_phase3_plus_modules_remain_placeholders(package_root) -> None:
    for prefix in PROTECTED_PREFIXES:
        for path in sorted((package_root / prefix).rglob("*.py")):
            if path.relative_to(package_root).as_posix() in STEP2_EXECUTABLE | STEP3_EXECUTABLE | STEP4_EXECUTABLE | STEP8_EXECUTABLE | PHASE3_FIELD_EXECUTABLE:
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
    assert "protected docstring-only modules: 24" in result.stdout


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
        checker["verify_phase3_changes"]([("M", path)], incremental=True)


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
