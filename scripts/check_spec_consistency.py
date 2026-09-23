"""Check current specifications, schema shape and canonical packaged resources.

Historical phase/step gates remain recoverable in Git. This command performs no
product calculations and does not certify a test run or release candidate.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import runpy
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {
    "README.md", "LICENSE", "NOTICE", "pyproject.toml", "PHASE_0_APPROVAL.md",
    "REPOSITORY_ARCHITECTURE.md", "DEPENDENCY_STRATEGY.md",
    "DATA_AND_PROVENANCE_SPEC.md", "OBSERVABILITY_AND_REPORTING.md",
    "THEORY_TO_CODE_TRACEABILITY.md", "PHASE_5_PLAN.md", "PHASE_5_DECISIONS.md",
}
SCHEMAS = {"report.schema.json", "config.schema.json", "schema_mapping.schema.json",
           "version_order.schema.json", "normalized_manifest.schema.json"}
HERO = {"records_v1.csv", "records_v2.csv", "provenance.csv", "config.json",
        "version_order.json", "EXPECTED_OUTPUTS.md"}
WORKFLOWS = {"ci.yml", "golden.yml", "security.yml", "release.yml"}


def audit(root: Path = ROOT) -> dict:
    missing = sorted(name for name in REQUIRED if not (root / name).is_file())
    if missing:
        raise ValueError(f"Missing required files: {missing}")
    if {path.name for path in (root / "schemas").glob("*.json")} != SCHEMAS:
        raise ValueError("Schema file set differs from the supported architecture")
    for path in sorted((root / "schemas").glob("*.json")):
        schema = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(schema, dict) or schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            raise ValueError(f"Unexpected schema dialect or root: {path.name}")
    if {path.name for path in (root / "examples/hero").iterdir() if path.is_file()} != HERO:
        raise ValueError("Canonical Hero file set differs")
    if {path.name for path in (root / ".github/workflows").glob("*.yml")} != WORKFLOWS:
        raise ValueError("Workflow file set differs")
    checker = runpy.run_path(str(ROOT / "scripts/release_check.py"), run_name="current_specification_checks")
    return {"schemas_parsed": len(SCHEMAS), "hero_files": len(HERO),
            **checker["verify_frozen_specifications"](root), **checker["verify_resources"](root)}


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if any(arg in {"--phase", "--step"} or arg.startswith(("--phase=", "--step=")) for arg in argv):
        raise SystemExit("Historical phase dispatch has been retired. Run this current check without --phase/--step; prior gates are recoverable from Git history.")
    argparse.ArgumentParser(description=__doc__).parse_args(argv)
    print(json.dumps(audit(), indent=2))
    print("Current specification consistency: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
