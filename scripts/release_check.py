"""Run non-analytical Phase 1 release-scaffold checks."""

from __future__ import annotations

import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROHIBITED = {
    "server",
    "webapp",
    "cloud",
    "telemetry",
    "plugins",
    "agents",
    "llm",
    "auth",
    "database",
    "policy_enforcement",
}


def main() -> int:
    for name in ["LICENSE", "NOTICE", "THIRD_PARTY_NOTICES.md", "THEORY_SOURCES.md"]:
        if not (ROOT / name).is_file():
            raise SystemExit(f"Missing release file: {name}")

    config = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    project = config["project"]
    if project["name"] != "recursive-integrity-toolkit":
        raise SystemExit("Unexpected package name")
    if project["requires-python"] != ">=3.11":
        raise SystemExit("Unexpected Python baseline")

    found = sorted(
        {path.name for path in ROOT.rglob("*") if path.is_dir() and path.name in PROHIBITED}
    )
    if found:
        raise SystemExit(f"Prohibited directories found: {found}")

    print(f"package: {project['name']} {project['version']}")
    print(f"Python requirement: {project['requires-python']}")
    print("license and notice files: PASS")
    print("prohibited structure: PASS")
    print("release scaffold: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
