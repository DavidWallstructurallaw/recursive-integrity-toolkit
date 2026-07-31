"""Check required Phase 1 final directories and prohibited structures."""

from pathlib import Path


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

FORBIDDEN_FILES = {
    "collapse_score.py",
    "integrity_score.py",
    "universal_score.py",
}


def test_prohibited_directories_and_score_files_absent(repo_root: Path) -> None:
    found_directories = {
        path.name
        for path in repo_root.rglob("*")
        if path.is_dir() and path.name in PROHIBITED
    }
    found_files = {
        path.name
        for path in repo_root.rglob("*")
        if path.is_file() and path.name in FORBIDDEN_FILES
    }
    assert found_directories == set()
    assert found_files == set()


def test_approved_phase1_final_directories_exist(repo_root: Path) -> None:
    required = [
        "examples/hero",
        ".github/workflows",
        "docs",
        "scripts",
    ]
    for relative in required:
        assert (repo_root / relative).is_dir(), relative
