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
    assert result.stdout.strip() == "0.1.0.dev3"


def test_PR002_csv_and_jsonl_work_with_pyarrow_blocked(subprocess_env, tmp_path) -> None:
    script = BLOCK_PYARROW_SCRIPT + r'''
import pathlib
import tempfile
from recursive_integrity_toolkit.models import InputSource, FileRole
from recursive_integrity_toolkit.io.loaders import load_table
from recursive_integrity_toolkit.errors import InputError, ErrorCode
with tempfile.TemporaryDirectory() as folder:
    root = pathlib.Path(folder)
    csv_path = root / "one.csv"
    csv_path.write_text("id\na\n", encoding="utf-8")
    json_path = root / "one.jsonl"
    json_path.write_text('{"id":"a"}\n', encoding="utf-8")
    for path in (csv_path, json_path):
        assert load_table(InputSource(FileRole.RECORDS_PRIMARY, path)).rows[0].values["id"] == "a"
    parquet_path = root / "one.parquet"
    parquet_path.write_bytes(b"PAR1")
    try:
        load_table(InputSource(FileRole.RECORDS_PRIMARY, parquet_path))
    except InputError as exc:
        assert exc.code is ErrorCode.FILE_FORMAT_UNSUPPORTED
        assert "[parquet]" in str(exc)
    else:
        raise AssertionError("missing optional dependency was hidden")
assert not any(name == "pyarrow" or name.startswith("pyarrow.") for name in sys.modules)
print("Step 2 core loaders succeed without PyArrow; optional request fails clearly")
'''
    result = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True,
                            env=subprocess_env, check=False)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "optional request fails clearly" in result.stdout
