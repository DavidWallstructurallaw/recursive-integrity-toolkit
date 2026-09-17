"""Protect Phase 2 Step 6 from premature analytical implementation."""

import ast
from pathlib import Path


STEP1_EXECUTABLE = {"__init__.py", "__main__.py", "cli.py", "config.py", "errors.py", "models.py"}
STEP2_EXECUTABLE = {"io/loaders.py", "utils/hashing.py", "utils/paths.py"}
STEP3_EXECUTABLE = {"io/schema_mapping.py"}
STEP4_EXECUTABLE = {"io/normalization.py", "io/validation.py", "utils/ordering.py"}
PROTECTED_PREFIXES = {"io", "lineage", "metrics", "observability", "reports", "representations", "utils"}
FORBIDDEN_ANALYTICAL_IMPORT_ROOTS = {"networkx", "scipy", "sklearn", "torch", "tensorflow", "transformers"}
FORBIDDEN_ANALYTICAL_NAMES = {"support_size", "gini_simpson", "tail_fragility", "source_type_shares", "closure_bounds", "ancestry_hhi", "effective_external_roots", "resample", "reopening"}


def _is_docstring_only(path: Path) -> bool:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    return len(tree.body) == 1 and isinstance(tree.body[0], ast.Expr) and isinstance(tree.body[0].value, ast.Constant) and isinstance(tree.body[0].value.value, str)


def test_only_step6_authorized_modules_gain_behavior(package_root) -> None:
    for path in sorted(package_root.rglob("*.py")):
        relative = path.relative_to(package_root)
        if relative.as_posix() in STEP2_EXECUTABLE | STEP3_EXECUTABLE | STEP4_EXECUTABLE or (len(relative.parts) == 1 and path.name in STEP1_EXECUTABLE):
            continue
        assert _is_docstring_only(path), f"Premature executable body: {relative}"


def test_protected_phase3_plus_modules_remain_placeholders(package_root) -> None:
    for prefix in PROTECTED_PREFIXES:
        for path in sorted((package_root / prefix).rglob("*.py")):
            if path.relative_to(package_root).as_posix() in STEP2_EXECUTABLE | STEP3_EXECUTABLE | STEP4_EXECUTABLE:
                continue
            assert _is_docstring_only(path), f"Protected module changed after Step 6: {path}"
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


def test_PR003_traceability_script_enforces_step6_scope(repo_root) -> None:
    import subprocess
    import sys
    result = subprocess.run([sys.executable, "scripts/check_traceability.py"],
                            cwd=repo_root, capture_output=True, text=True, check=False)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "protected docstring-only modules: 27" in result.stdout


# The checker itself must reject new work outside the current Step 6 boundary.
import shutil
import subprocess
import sys
import pytest


@pytest.mark.parametrize("relative,injected", [
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
