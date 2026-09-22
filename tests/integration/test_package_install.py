"""Check the declared package and CLI installation contract without network access."""

from __future__ import annotations

import tomllib
from pathlib import Path


def test_package_metadata_and_entry_points(repo_root: Path) -> None:
    config = tomllib.loads((repo_root / "pyproject.toml").read_text(encoding="utf-8"))
    project = config["project"]
    assert project["name"] == "recursive-integrity-toolkit"
    assert project["version"] == "0.1.0.dev3"
    assert project["requires-python"] == ">=3.11"
    assert project["license"] == "Apache-2.0"
    assert project["scripts"] == {
        "rit": "recursive_integrity_toolkit.cli:main",
        "recursive-integrity": "recursive_integrity_toolkit.cli:main",
    }


def test_dependency_groups_preserve_core_and_optional_boundary(repo_root: Path) -> None:
    config = tomllib.loads((repo_root / "pyproject.toml").read_text(encoding="utf-8"))
    project = config["project"]
    assert project["dependencies"] == ["numpy>=2.0", "pandas>=2.2"]
    assert project["optional-dependencies"]["parquet"] == ["pyarrow>=15"]
    assert "pyarrow>=15" not in project["dependencies"]
