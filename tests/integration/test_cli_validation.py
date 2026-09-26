"""Check help and version startup against the current package."""

import subprocess
import sys


def test_cli_version_runs(subprocess_env) -> None:
    result = subprocess.run(
        [sys.executable, "-m", "recursive_integrity_toolkit", "version"],
        capture_output=True,
        text=True,
        env=subprocess_env,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "recursive-integrity-toolkit 0.1.0.dev4"


def test_phase4_cli_help_uses_current_source(subprocess_env) -> None:
    """The current CLI starts with a useful help response and no diagnostics."""
    result = subprocess.run(
        [sys.executable, "-m", "recursive_integrity_toolkit", "--help"],
        capture_output=True,
        text=True,
        env=subprocess_env,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert "usage:" in result.stdout.lower()
    assert "version" in result.stdout
    assert "--help" in result.stdout
    assert result.stderr == ""


def test_phase4_step7_current_help_documents_enabled_commands(subprocess_env) -> None:
    result = subprocess.run([sys.executable, "-m", "recursive_integrity_toolkit", "--help"],
                            capture_output=True, text=True, env=subprocess_env, check=False)
    assert result.returncode == 0 and result.stderr == ""
    assert "audit" in result.stdout and "validate" in result.stdout and "version" in result.stdout
    assert "Analytical audit functionality is not implemented" not in result.stdout
