"""Check that all approved package modules retain an Owner IDs section."""

import ast


def test_every_module_has_owner_and_phase_status(package_root) -> None:
    paths = sorted(package_root.rglob("*.py"))
    assert len(paths) == 40
    for path in paths:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        doc = ast.get_docstring(tree) or ""
        assert "Owner IDs:" in doc, str(path)
        assert "Current phase status:" in doc, str(path)
