"""Check that every approved package module imports safely."""

import importlib
import pkgutil

import recursive_integrity_toolkit


def test_all_package_modules_import() -> None:
    names = [recursive_integrity_toolkit.__name__]
    names.extend(
        info.name
        for info in pkgutil.walk_packages(
            recursive_integrity_toolkit.__path__,
            recursive_integrity_toolkit.__name__ + ".",
        )
    )
    imported = [importlib.import_module(name).__name__ for name in sorted(names)]
    assert len(imported) == 40
    assert len(set(imported)) == 40
