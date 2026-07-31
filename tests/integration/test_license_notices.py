"""Check Phase 1 license, notice, theory, and third-party declarations."""

from pathlib import Path


def test_license_and_notice_files_are_consistent(repo_root: Path) -> None:
    license_text = (repo_root / "LICENSE").read_text(encoding="utf-8")
    notice_text = (repo_root / "NOTICE").read_text(encoding="utf-8")
    theory_text = (repo_root / "THEORY_SOURCES.md").read_text(encoding="utf-8")

    assert "Apache License" in license_text
    assert "Version 2.0" in license_text
    assert "Apache License, Version 2.0" in notice_text
    assert "Theory publications" in notice_text
    assert "retain their stated licenses" in notice_text
    assert "The Universal Inbreeding Law" in theory_text
    assert "| v2 | Primary law" in theory_text
    assert "Entropy as a Structural Boundary Condition" in theory_text


def test_third_party_declarations_cover_direct_dependencies(repo_root: Path) -> None:
    text = (repo_root / "THIRD_PARTY_NOTICES.md").read_text(encoding="utf-8")
    for name in ["NumPy", "pandas", "PyArrow", "pytest", "pip-audit"]:
        assert name in text
