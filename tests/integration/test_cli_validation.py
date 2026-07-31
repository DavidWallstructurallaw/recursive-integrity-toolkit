"""Check the Phase 1 help and version startup commands."""

import subprocess
import sys


def test_cli_help_runs(subprocess_env) -> None:
    result = subprocess.run(
        [sys.executable, "-m", "recursive_integrity_toolkit", "--help"],
        capture_output=True,
        text=True,
        env=subprocess_env,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    normalized = " ".join(result.stdout.split())
    assert "Phase 1 scaffold" in normalized
    assert "Analytical audit functionality is not implemented" in normalized


def test_cli_version_runs(subprocess_env) -> None:
    result = subprocess.run(
        [sys.executable, "-m", "recursive_integrity_toolkit", "version"],
        capture_output=True,
        text=True,
        env=subprocess_env,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "recursive-integrity-toolkit 0.1.0.dev1"
