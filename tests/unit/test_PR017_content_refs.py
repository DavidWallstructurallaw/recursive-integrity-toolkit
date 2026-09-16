"""PR-017 Step 2 input-path checks. Content-reference resolution stays deferred."""

import os
from pathlib import Path

import pytest

from recursive_integrity_toolkit.errors import InputError
from recursive_integrity_toolkit.utils.paths import local_input_path


def test_PR017_paths_owner(owner_checker):
    owner_checker("utils/paths.py", "PR-017")


@pytest.mark.parametrize("value", ["http://invalid.example/data.csv", "https:/invalid/data.csv", "s3://bucket/file.csv", "gs://bucket/file.csv", "ftp://host/f.csv", "file:///tmp/f.csv", "ssh://host/file", "//server/share/file.csv", r"\\server\share\file.csv", r"\\?\C:\file.csv", "", "bad\x00path"])
def test_PR017_nonlocal_paths_rejected_before_io(value, monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("filesystem touched before rejecting nonlocal path")
    monkeypatch.setattr(Path, "stat", forbidden)
    with pytest.raises(InputError):
        local_input_path(value)


def test_PR017_explicit_local_path_can_be_absolute(tmp_path):
    # This is an input-file declaration, not a record content reference.
    assert local_input_path(tmp_path / "file.csv") == tmp_path / "file.csv"


def test_PR017_relative_path_normalization_does_not_create_or_open(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    result = local_input_path("sub/../file.csv")
    assert result == tmp_path / "file.csv"
    assert list(tmp_path.iterdir()) == []


def test_PR017_tilde_and_environment_variables_are_not_expanded(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert local_input_path("~/file.csv") == tmp_path / "~" / "file.csv"
    assert local_input_path("$HOME/file.csv") == tmp_path / "$HOME" / "file.csv"
