"""Check current module ownership and local-only architectural boundaries.

Behavioral tests own formulas and product outcomes. This static check retains
owner declarations, dependency boundaries, input-only validation and pure
rendering. It does not pin function bodies or replay historical source forms.
"""
from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_IMPORTS = {"socket", "urllib", "http", "ftplib", "requests", "httpx",
                     "aiohttp", "subprocess", "networkx", "scipy", "sklearn", "torch",
                     "tensorflow", "transformers"}
FORBIDDEN_FILES = {"collapse_score.py", "integrity_score.py", "universal_score.py"}
DYNAMIC_CALLS = {"eval", "exec", "compile", "__import__"}
INPUT_ONLY = {"io/validation.py", "io/normalization.py", "io/schema_mapping.py", "io/loaders.py",
              "observability/levels.py"}
RENDERERS = {"reports/json_report.py", "reports/markdown_report.py"}


def _module_name(node: ast.ImportFrom, relative: str) -> str:
    """Resolve relative imports sufficiently to check the package layer."""
    if not node.level:
        return node.module or ""
    parent = ["recursive_integrity_toolkit", *Path(relative).parts[:-1]]
    prefix = parent[:len(parent) - node.level + 1]
    return ".".join(prefix + ([node.module] if node.module else []))


def audit(root: Path = ROOT) -> dict:
    package = root / "src/recursive_integrity_toolkit"
    paths = sorted(package.rglob("*.py"))
    if not paths:
        raise ValueError("Package source is missing")
    for path in paths:
        relative = path.relative_to(package).as_posix()
        if path.is_symlink() or path.name in FORBIDDEN_FILES:
            raise ValueError(f"Aliased or prohibited module: {relative}")
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        doc = ast.get_docstring(tree) or ""
        if "Owner IDs:" not in doc or "Current phase status:" not in doc:
            raise ValueError(f"Owner or implementation status missing: {relative}")
        for node in ast.walk(tree):
            imports = []
            if isinstance(node, ast.Import):
                imports = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                module = _module_name(node, relative)
                imports = [module, *(module + "." + alias.name for alias in node.names)]
            for module in imports:
                if module.split(".")[0] in FORBIDDEN_IMPORTS:
                    raise ValueError(f"Prohibited network/execution/dependency import in {relative}: {module}")
                if relative in INPUT_ONLY and module.startswith(tuple("recursive_integrity_toolkit." + layer for layer in ("metrics", "lineage", "reports"))):
                    raise ValueError(f"Input-only module imports an analytical/report owner: {relative}")
                if relative in RENDERERS and module.startswith(tuple("recursive_integrity_toolkit." + layer for layer in ("io", "metrics", "lineage", "representations"))):
                    raise ValueError(f"Renderer imports a calculation or input owner: {relative}")
                if module.split(".")[0] == "pyarrow" and relative != "io/loaders.py":
                    raise ValueError(f"Optional Parquet dependency escaped its loader: {relative}")
                if module.split(".")[0] == "numpy" and relative != "metrics/resampling.py":
                    raise ValueError(f"Numerical dependency escaped the explicit sampler: {relative}")
            if isinstance(node, ast.Call):
                name = node.func.id if isinstance(node.func, ast.Name) else node.func.attr if isinstance(node.func, ast.Attribute) else ""
                regex_compile = (isinstance(node.func, ast.Attribute)
                                 and isinstance(node.func.value, ast.Name)
                                 and node.func.value.id == "re" and name == "compile")
                if name in DYNAMIC_CALLS and not regex_compile:
                    raise ValueError(f"Dynamic execution is prohibited: {relative}")
                if relative in RENDERERS and name in {"open", "read_text", "read_bytes", "write_text", "write_bytes"}:
                    raise ValueError(f"Renderer performs file IO: {relative}")
    return {"owned_modules_checked": len(paths), "local_only_and_layer_boundaries": "PASS"}


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if any(arg in {"--phase", "--step"} or arg.startswith(("--phase=", "--step=")) for arg in argv):
        raise SystemExit("Historical phase dispatch has been retired. Run this current check without --phase/--step; prior gates are recoverable from Git history.")
    argparse.ArgumentParser(description=__doc__).parse_args(argv)
    print(json.dumps(audit(), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
