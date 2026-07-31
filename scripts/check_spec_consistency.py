"""Run Phase 1 specification and repository-presence checks only.

This script reads repository metadata and scaffold files. It does not load hero
records into the toolkit or calculate an analytical result.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_ROOT = {
    "README.md",
    "LICENSE",
    "NOTICE",
    "pyproject.toml",
    "PHASE_0_APPROVAL.md",
    "PHASE_1_PLAN.md",
    "PROJECT_INSTRUCTIONS.md",
    "REPOSITORY_ARCHITECTURE.md",
    "DEPENDENCY_STRATEGY.md",
    "VALIDATION_PLAN.md",
    "THEORY_TO_CODE_TRACEABILITY.md",
}

SCHEMAS = {
    "report.schema.json",
    "config.schema.json",
    "schema_mapping.schema.json",
    "version_order.schema.json",
    "normalized_manifest.schema.json",
}

HERO = {
    "records_v1.csv",
    "records_v2.csv",
    "provenance.csv",
    "version_order.json",
    "config.json",
    "EXPECTED_OUTPUTS.md",
}

WORKFLOWS = {"ci.yml", "golden.yml", "security.yml", "release.yml"}


def main() -> int:
    missing_root = sorted(name for name in REQUIRED_ROOT if not (ROOT / name).is_file())
    if missing_root:
        raise SystemExit(f"Missing required root files: {missing_root}")

    schema_root = ROOT / "schemas"
    actual_schemas = {path.name for path in schema_root.glob("*.json")}
    if actual_schemas != SCHEMAS:
        raise SystemExit(f"Schema set mismatch: {sorted(actual_schemas)}")
    for path in sorted(schema_root.glob("*.json")):
        json.loads(path.read_text(encoding="utf-8"))

    actual_hero = {path.name for path in (ROOT / "examples" / "hero").iterdir() if path.is_file()}
    if actual_hero != HERO:
        raise SystemExit(f"Hero file set mismatch: {sorted(actual_hero)}")

    actual_workflows = {path.name for path in (ROOT / ".github" / "workflows").glob("*.yml")}
    if actual_workflows != WORKFLOWS:
        raise SystemExit(f"Workflow set mismatch: {sorted(actual_workflows)}")

    print(f"required root files: {len(REQUIRED_ROOT)}")
    print(f"schemas parsed: {len(SCHEMAS)}")
    print(f"hero files found: {len(HERO)}")
    print(f"workflows found: {len(WORKFLOWS)}")
    print("specification structure: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
