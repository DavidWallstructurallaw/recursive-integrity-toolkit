"""Check the Phase 1 GitHub workflow scaffold without running a hosted service."""

from pathlib import Path


EXPECTED = {"ci.yml", "golden.yml", "security.yml", "release.yml"}
FORBIDDEN_WORKFLOW_TERMS = {
    "services:",
    "docker run",
    "fastapi",
    "streamlit",
    "telemetry",
    "publish-package",
}


def test_workflow_file_set_and_basic_contract(repo_root: Path) -> None:
    workflow_root = repo_root / ".github" / "workflows"
    assert {path.name for path in workflow_root.glob("*.yml")} == EXPECTED
    for path in sorted(workflow_root.glob("*.yml")):
        text = path.read_text(encoding="utf-8")
        assert text.startswith("name:")
        assert "permissions:\n  contents: read" in text
        assert "actions/checkout@v4" in text
        assert "actions/setup-python@v5" in text
        assert "\t" not in text


def test_workflows_preserve_phase_boundary(repo_root: Path) -> None:
    workflow_root = repo_root / ".github" / "workflows"
    combined = "\n".join(
        path.read_text(encoding="utf-8").lower()
        for path in workflow_root.glob("*.yml")
    )
    for term in FORBIDDEN_WORKFLOW_TERMS:
        assert term not in combined
    assert "test_no_algorithms.py" in combined
    assert "test_no_network.py" in combined
    assert "python -m build" in combined
    assert "rit version" in combined
