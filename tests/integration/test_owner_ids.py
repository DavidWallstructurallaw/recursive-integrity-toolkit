"""Check that all approved package modules retain ownership and phase status."""

import ast


def test_every_module_has_owner_and_phase_status(package_root) -> None:
    paths = sorted(package_root.rglob("*.py"))
    assert len(paths) == 40
    for path in paths:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        doc = ast.get_docstring(tree) or ""
        assert "Owner IDs:" in doc, str(path)
        assert "Current phase status:" in doc, str(path)


def test_step1_core_contract_owners(package_root) -> None:
    expected = {
        "models.py": {"PR-001", "PR-007", "PR-010", "PR-011"},
        "errors.py": {"PR-001", "PR-007", "PR-010", "PR-011"},
        "config.py": {"PR-007", "PR-010", "PR-011"},
    }
    for relative, owner_ids in expected.items():
        tree = ast.parse((package_root / relative).read_text(encoding="utf-8"), filename=relative)
        doc = ast.get_docstring(tree) or ""
        for owner_id in owner_ids:
            assert owner_id in doc, f"{owner_id} missing from {relative}"
