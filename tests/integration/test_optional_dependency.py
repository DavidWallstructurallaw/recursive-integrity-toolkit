"""Check that core import succeeds when the optional PyArrow dependency is blocked."""

import subprocess
import sys


BLOCK_PYARROW_SCRIPT = r"""
import importlib.abc
import sys

class BlockPyArrow(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname == "pyarrow" or fullname.startswith("pyarrow."):
            raise ModuleNotFoundError("pyarrow intentionally blocked for Phase 1 core-import test")
        return None

sys.meta_path.insert(0, BlockPyArrow())
import recursive_integrity_toolkit
print(recursive_integrity_toolkit.__version__)
"""


def test_core_import_without_optional_pyarrow(subprocess_env) -> None:
    result = subprocess.run(
        [sys.executable, "-c", BLOCK_PYARROW_SCRIPT],
        capture_output=True,
        text=True,
        env=subprocess_env,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "0.1.0.dev1"
