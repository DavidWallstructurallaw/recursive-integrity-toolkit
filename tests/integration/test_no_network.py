"""Check that importing the complete package makes no network call."""

import subprocess
import sys


BLOCKED_IMPORT_SCRIPT = r"""
import importlib
import pkgutil
import socket
import urllib.request


def blocked(*args, **kwargs):
    raise AssertionError("network access attempted during import")

socket.socket.connect = blocked
socket.create_connection = blocked
urllib.request.urlopen = blocked

import recursive_integrity_toolkit
for info in pkgutil.walk_packages(
    recursive_integrity_toolkit.__path__,
    recursive_integrity_toolkit.__name__ + ".",
):
    importlib.import_module(info.name)
print("all modules imported with network blocked")
"""


def test_import_with_network_blocked(subprocess_env) -> None:
    result = subprocess.run(
        [sys.executable, "-c", BLOCKED_IMPORT_SCRIPT],
        capture_output=True,
        text=True,
        env=subprocess_env,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "all modules imported with network blocked"
