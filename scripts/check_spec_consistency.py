"""Check Phase 2 specification and repository presence without analytical work."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {
    "README.md", "LICENSE", "NOTICE", "pyproject.toml", "PHASE_0_APPROVAL.md",
    "PHASE_1_PLAN.md", "REPOSITORY_ARCHITECTURE.md", "DEPENDENCY_STRATEGY.md",
    "DATA_AND_PROVENANCE_SPEC.md", "OBSERVABILITY_AND_REPORTING.md",
    "THEORY_TO_CODE_TRACEABILITY.md", "PHASE_1_COMPLETION.md",
    "PHASE_2_COMPLETION.md", "PHASE_2_VALIDATION_REPORT.md",
    "PHASE_2_ARCHITECTURE_COMPLIANCE_REPORT.md",
}
SCHEMAS = {"report.schema.json", "config.schema.json", "schema_mapping.schema.json",
           "version_order.schema.json", "normalized_manifest.schema.json"}
HERO = {"records_v1.csv", "records_v2.csv", "provenance.csv", "config.json",
        "version_order.json", "EXPECTED_OUTPUTS.md"}
WORKFLOWS = {"ci.yml", "golden.yml", "security.yml", "release.yml"}


def main() -> int:
    missing = sorted(name for name in REQUIRED if not (ROOT / name).is_file())
    if missing:
        raise SystemExit(f"Missing required files: {missing}")
    schema_root = ROOT / "schemas"
    if {path.name for path in schema_root.glob("*.json")} != SCHEMAS:
        raise SystemExit("Schema file set differs from approved architecture")
    for path in sorted(schema_root.glob("*.json")):
        schema = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(schema, dict) or schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            raise SystemExit(f"Unexpected schema dialect or root: {path.name}")
    if {p.name for p in (ROOT / "examples/hero").iterdir() if p.is_file()} != HERO:
        raise SystemExit("Hero file set differs from approved architecture")
    if {p.name for p in (ROOT / ".github/workflows").glob("*.yml")} != WORKFLOWS:
        raise SystemExit("Workflow file set differs from approved architecture")
    print(f"required root files: {len(REQUIRED)}")
    print(f"schemas parsed: {len(SCHEMAS)}")
    print(f"hero files found: {len(HERO)}")
    print(f"workflows found: {len(WORKFLOWS)}")
    print("specification structure: PASS")
    return 0


def phase4_main(step: int = 1) -> int:
    """Validate Step 1 control and preserve the inherited structure checks."""
    import runpy

    if type(step) is not int or step != 1:
        raise ValueError("Only authorized Phase 4 Step 1 specification checking is available")
    control = runpy.run_path(str(ROOT / "scripts/release_check.py"),
                            run_name="phase4_specification_control")
    control["audit_phase4"](step=step)
    result = main()
    print("Phase 4 Step 1: approved governance and frozen specification structure: PASS")
    return result


def phase4_step2_main(step: int = 2) -> int:
    """Check the authorized canonical contract and the frozen repository layout."""
    import runpy

    if type(step) is not int or step != 2:
        raise ValueError("Only authorized Phase 4 Step 2 specification checking is available")
    control = runpy.run_path(str(ROOT / "scripts/release_check.py"),
                            run_name="phase4_step2_specification_control")
    control["audit_phase4_step2"](step=step)
    result = main()
    print("Phase 4 Step 2: canonical report schema and preserved specification structure: PASS")
    return result


def cli_main(argv: list[str] | None = None) -> int:
    """Keep the argument-free historical gate and add explicit Phase 4 dispatch."""
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", type=int, choices=(3, 4))
    parser.add_argument("--step", type=int)
    args = parser.parse_args(argv)
    if args.phase is None and args.step is None:
        return main()
    if args.phase == 3 and args.step == 11:
        return main()
    if args.phase == 4 and args.step == 1:
        return phase4_main(step=args.step)
    if args.phase == 4 and args.step == 2:
        return phase4_step2_main(step=args.step)
    parser.error("Choose explicit --phase 3 --step 11 or --phase 4 --step 1 or --phase 4 --step 2")
    return 2


if __name__ == "__main__":
    raise SystemExit(cli_main())
