"""Shared Phase 1 scaffold-test fixtures.

Owner IDs:
    Technical Maintainer, Phase 1 acceptance gate

Current scope:
    Repository structure, safe import, CLI startup, JSON parsing, owner IDs,
    prohibited paths, optional dependency isolation, no-network import, and
    absence of analytical implementation.

Limits:
    No data fixture is loaded and no mathematical or analytical result is tested.
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
