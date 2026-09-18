"""Check the approved repository scaffold at Phase 2 Step 1."""

from pathlib import Path


def test_required_repository_directories_exist(repo_root: Path) -> None:
    for relative in ["src/recursive_integrity_toolkit", "schemas", "docs", "tests/fixtures", "tests/unit", "tests/integration", "tests/golden", "tests/performance", "examples/hero", "scripts", ".github/workflows", ".github/ISSUE_TEMPLATE"]:
        assert (repo_root / relative).is_dir(), relative


def test_required_root_schema_documentation_and_script_files_exist(repo_root: Path) -> None:
    required = [
        "PHASE_3_COMPLETION.md", "PHASE_3_VALIDATION_REPORT.md", "PHASE_3_ARCHITECTURE_COMPLIANCE_REPORT.md",
        "README.md", "LICENSE", "NOTICE", "pyproject.toml", "PHASE_0_APPROVAL.md", "PHASE_1_PLAN.md", "PHASE_1_COMPLETION.md", "ARCHITECTURE_COMPLIANCE_REPORT.md",
        "schemas/report.schema.json", "schemas/config.schema.json", "schemas/schema_mapping.schema.json", "schemas/version_order.schema.json", "schemas/normalized_manifest.schema.json",
        "docs/architecture.md", "docs/cli.md", "docs/report_schema.md", "docs/data_schema.md", "docs/theory_traceability.md", "docs/privacy.md", "docs/release_process.md",
        "scripts/check_spec_consistency.py", "scripts/check_traceability.py", "scripts/build_golden.py", "scripts/normalize_golden.py", "scripts/release_check.py",
        "tests/integration/test_package_install.py", "tests/performance/test_hero_runtime.py", "tests/performance/test_metadata_100k.py", "tests/performance/test_sparse_lineage_100k.py"
    ]
    for relative in required:
        assert (repo_root / relative).is_file(), relative
