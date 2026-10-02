"""PR-017 Step 2 input paths and Step 7 explicit local content references."""

import os
from pathlib import Path

import pytest

from recursive_integrity_toolkit.errors import InputError
from recursive_integrity_toolkit.utils.paths import local_input_path


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


# Phase 2 Step 7: explicit local content-reference security.
import socket
import subprocess
import sys

from recursive_integrity_toolkit.config import ResourceLimits
from recursive_integrity_toolkit.errors import CanonicalValidationError, ErrorCode
from recursive_integrity_toolkit.io.loaders import load_content_reference
from recursive_integrity_toolkit.models import RowLocation, FileRole
from recursive_integrity_toolkit.utils.paths import resolve_content_reference, _content_lexical


def _s7_base(tmp_path):
    base = tmp_path / "base"
    base.mkdir()
    (base / "text.txt").write_bytes("hello 世界\r\n".encode("utf-8"))
    (tmp_path / "outside.txt").write_text("PRIVATE_OUTSIDE_SENTINEL", encoding="utf-8")
    return base


def test_PR017_utf8_content_is_exact_and_source_unchanged(tmp_path):
    base = _s7_base(tmp_path)
    path = base / "text.txt"
    before = path.read_bytes()
    assert load_content_reference("text.txt", base_directory=base) == "hello 世界\r\n"
    assert before == path.read_bytes()
    assert resolve_content_reference("text.txt", base_directory=base) == path.resolve()


def test_PR017_default_base_is_records_directory_not_cwd(tmp_path, monkeypatch):
    base = _s7_base(tmp_path)
    monkeypatch.chdir(tmp_path)
    assert load_content_reference("text.txt", records_path=base / "records.csv") == "hello 世界\r\n"


@pytest.mark.parametrize("reference", ["../outside.txt", "sub/../../outside.txt", r"..\outside.txt"])
def test_PR017_parent_traversal_blocked(tmp_path, reference):
    base = _s7_base(tmp_path)
    (base / "sub").mkdir()
    with pytest.raises(CanonicalValidationError) as caught:
        load_content_reference(reference, base_directory=base)
    assert caught.value.code is ErrorCode.CONTENT_REF_OUTSIDE_BASE


def test_PR017_internal_traversal_is_normalized_inside_base(tmp_path):
    base = _s7_base(tmp_path)
    (base / "sub").mkdir()
    assert load_content_reference("sub/../text.txt", base_directory=base) == "hello 世界\r\n"


def test_PR017_absolute_path_blocked_by_default(tmp_path):
    base = _s7_base(tmp_path)
    with pytest.raises(CanonicalValidationError) as caught:
        load_content_reference(str(base / "text.txt"), base_directory=base)
    assert caught.value.code is ErrorCode.CONTENT_REF_OUTSIDE_BASE
    assert load_content_reference(str(base / "text.txt"), base_directory=base, allow_absolute=True)


def test_PR017_absolute_opt_in_never_grants_outside_access(tmp_path):
    base = _s7_base(tmp_path)
    with pytest.raises(CanonicalValidationError) as caught:
        load_content_reference(str(tmp_path / "outside.txt"), base_directory=base, allow_absolute=True)
    assert caught.value.code is ErrorCode.CONTENT_REF_OUTSIDE_BASE


@pytest.mark.parametrize("value", ["http://bad.example/a", "https:/bad/a", "ftp://bad/a", "s3://bucket/a",
    "gs://bucket/a", "ssh://bad/a", "file:///a", "data:text/plain,hi", "//server/share/a",
    r"\\server\share\a", r"\\?\C:\a", r"\\.\pipe\a", "C:relative.txt"])
def test_PR017_network_uri_blocked(value, tmp_path, monkeypatch):
    def blocked(*args, **kwargs):
        raise AssertionError("IO happened before lexical rejection")
    monkeypatch.setattr(Path, "resolve", blocked)
    monkeypatch.setattr(Path, "lstat", blocked)
    monkeypatch.setattr(socket, "getaddrinfo", blocked)
    with pytest.raises(CanonicalValidationError) as caught:
        resolve_content_reference(value, base_directory=tmp_path)
    assert caught.value.code is ErrorCode.CONTENT_REF_OUTSIDE_BASE


def test_PR017_http_content_reference_rejected(tmp_path):
    with pytest.raises(CanonicalValidationError):
        load_content_reference("https://bad.example/a", base_directory=tmp_path)


@pytest.mark.parametrize("value", ["a\x00b", "a\nb", "a\rb", "a\tb", "a:b", "text.txt:secret", "NUL", "con.txt",
                                   "COM1", "LPT9.txt", "COM¹", "file. ", "text.txt."])
def test_PR017_device_aliases_and_controls_are_rejected(value, tmp_path):
    with pytest.raises(CanonicalValidationError) as caught:
        resolve_content_reference(value, base_directory=tmp_path)
    assert caught.value.code is ErrorCode.CONTENT_REF_OUTSIDE_BASE


@pytest.mark.parametrize("kind", ["relative", "absolute", "directory"])
def test_PR017_symlink_escape_blocked(tmp_path, kind):
    base = _s7_base(tmp_path)
    link = base / "link"
    if kind == "relative":
        link.symlink_to("../outside.txt")
    elif kind == "absolute":
        link.symlink_to(tmp_path / "outside.txt")
    else:
        link.symlink_to(tmp_path, target_is_directory=True)
    reference = "link/outside.txt" if kind == "directory" else "link"
    with pytest.raises(CanonicalValidationError) as caught:
        load_content_reference(reference, base_directory=base)
    assert caught.value.code is ErrorCode.CONTENT_REF_OUTSIDE_BASE


@pytest.mark.parametrize("kind", ["relative", "absolute", "directory", "chain"])
def test_PR017_inside_symlinks_are_usable(tmp_path, kind):
    base = _s7_base(tmp_path)
    if kind == "relative":
        (base / "link").symlink_to("text.txt")
    elif kind == "absolute":
        (base / "link").symlink_to(base / "text.txt")
    elif kind == "directory":
        (base / "sub").mkdir()
        (base / "sub/data.txt").write_text("hello", encoding="utf-8")
        (base / "link").symlink_to(base / "sub", target_is_directory=True)
    else:
        (base / "link").symlink_to("other")
        (base / "other").symlink_to("text.txt")
    reference = "link/data.txt" if kind == "directory" else "link"
    assert load_content_reference(reference, base_directory=base).startswith("hello")


def test_PR017_remote_symlink_target_rejected_without_resolving_it(tmp_path, monkeypatch):
    base = _s7_base(tmp_path)
    (base / "link").symlink_to("text.txt")
    calls = []
    def fake_readlink(path, *args, **kwargs):
        calls.append(str(path))
        return "//server/share/private.txt"
    monkeypatch.setattr(os, "readlink", fake_readlink)
    with pytest.raises(CanonicalValidationError) as caught:
        load_content_reference("link", base_directory=base)
    assert caught.value.code is ErrorCode.CONTENT_REF_OUTSIDE_BASE
    assert calls == [str(base / "link")]


def test_PR017_broken_symlink_is_missing(tmp_path):
    base = _s7_base(tmp_path)
    (base / "broken").symlink_to("missing.txt")
    with pytest.raises(CanonicalValidationError) as caught:
        load_content_reference("broken", base_directory=base)
    assert caught.value.code is ErrorCode.CONTENT_REF_MISSING


def test_PR017_symlink_loop_is_bounded_failure(tmp_path):
    base = _s7_base(tmp_path)
    (base / "a").symlink_to("b")
    (base / "b").symlink_to("a")
    with pytest.raises(CanonicalValidationError) as caught:
        load_content_reference("a", base_directory=base)
    assert caught.value.code is ErrorCode.FILE_PARSE


def test_PR017_missing_file_error(tmp_path):
    base = _s7_base(tmp_path)
    with pytest.raises(CanonicalValidationError) as caught:
        load_content_reference("missing.txt", base_directory=base)
    assert caught.value.code is ErrorCode.CONTENT_REF_MISSING


@pytest.mark.parametrize("reference", [".", "sub", "text.txt/child"])
def test_PR017_nonregular_content_is_not_read(tmp_path, reference):
    base = _s7_base(tmp_path)
    (base / "sub").mkdir()
    with pytest.raises(CanonicalValidationError) as caught:
        load_content_reference(reference, base_directory=base)
    assert caught.value.code is ErrorCode.FILE_FORMAT_UNSUPPORTED


def test_PR017_size_limit_enforced(tmp_path):
    base = _s7_base(tmp_path)
    length = len((base / "text.txt").read_bytes())
    assert load_content_reference("text.txt", base_directory=base, limits=ResourceLimits(max_content_bytes=length))
    with pytest.raises(CanonicalValidationError) as caught:
        load_content_reference("text.txt", base_directory=base, limits=ResourceLimits(max_content_bytes=length - 1))
    assert caught.value.code is ErrorCode.FILE_PARSE
    assert "max_content_bytes" in caught.value.safe_message


def test_PR017_streaming_limit_is_enforced_even_after_growth(tmp_path, monkeypatch):
    import recursive_integrity_toolkit.utils.paths as paths
    base = _s7_base(tmp_path)
    (base / "text.txt").write_bytes(b"abc")
    original = paths._open_content_fd
    def grow(path, root):
        path.write_bytes(b"abcdef")
        return original(path, root)
    monkeypatch.setattr(paths, "_open_content_fd", grow)
    with pytest.raises(CanonicalValidationError) as caught:
        load_content_reference("text.txt", base_directory=base, limits=ResourceLimits(max_content_bytes=3))
    assert caught.value.code is ErrorCode.FILE_PARSE


@pytest.mark.parametrize("raw,code", [(b"\xff\xfeprivate", ErrorCode.FILE_ENCODING),
    (b"hello\x00private", ErrorCode.FILE_FORMAT_UNSUPPORTED), (b"", ErrorCode.RECORD_EMPTY_CONTENT),
    (b" \r\n\t", ErrorCode.RECORD_EMPTY_CONTENT)])
def test_PR017_invalid_text_encoding_error(tmp_path, raw, code):
    base = _s7_base(tmp_path)
    (base / "text.txt").write_bytes(raw)
    with pytest.raises(CanonicalValidationError) as caught:
        load_content_reference("text.txt", base_directory=base)
    assert caught.value.code is code
    assert "private" not in str(caught.value)


def test_PR017_error_does_not_include_raw_content_or_paths(tmp_path, capsys):
    base = _s7_base(tmp_path)
    (base / "text.txt").write_bytes(b"PRIVATE_SENTINEL\xff")
    with pytest.raises(CanonicalValidationError) as caught:
        load_content_reference("text.txt", base_directory=base,
            location=RowLocation(FileRole.RECORDS_PRIMARY, "PRIVATE_LOCATION", 3, 4))
    err = caught.value
    assert err.file_path == "[redacted]" and err.row_number == 3 and err.line_number == 4
    assert err.file_role == "records_primary" and err.field == "content"
    assert "PRIVATE" not in str(err) and str(base) not in str(err)
    assert err.__cause__ is None and err.__suppress_context__
    assert capsys.readouterr() == ("", "")


def test_PR017_filename_prefix_is_not_directory_containment(tmp_path):
    base = _s7_base(tmp_path)
    other = tmp_path / "base-sibling"
    other.mkdir()
    (other / "a").write_text("private", encoding="utf-8")
    with pytest.raises(CanonicalValidationError):
        load_content_reference(str(other / "a"), base_directory=base, allow_absolute=True)


@pytest.mark.parametrize("name", ["%2e%2e.txt", "$HOME.txt", "~name.txt"])
def test_PR017_reference_values_are_literal_not_expanded(tmp_path, name):
    base = _s7_base(tmp_path)
    (base / name).write_text("literal", encoding="utf-8")
    assert load_content_reference(name, base_directory=base) == "literal"


def test_PR017_content_looking_like_code_is_inert(tmp_path):
    base = _s7_base(tmp_path)
    text = "__import__('os').remove('anything') https://never-fetch.example/"
    (base / "text.txt").write_text(text, encoding="utf-8")
    assert load_content_reference("text.txt", base_directory=base) == text


@pytest.mark.parametrize("kwargs", [{}, {"allow_absolute": 1}, {"base_directory": object()},
    {"limits": object()}, {"limits": ResourceLimits(max_content_bytes=0)},
    {"limits": ResourceLimits(max_content_bytes=True)}, {"location": object()},
    {"location": RowLocation(row_number=True)}, {"location": RowLocation(file_role="bad")}])
def test_PR017_bad_options_are_explicit_errors(tmp_path, kwargs):
    with pytest.raises(CanonicalValidationError) as caught:
        load_content_reference("text.txt", **kwargs)
    assert caught.value.code is ErrorCode.CONFIG_INVALID


def test_PR017_successful_reads_use_no_network_and_create_no_outputs(tmp_path, monkeypatch):
    base = _s7_base(tmp_path)
    before = sorted(str(path.relative_to(tmp_path)) for path in tmp_path.rglob("*"))
    def blocked(*args, **kwargs):
        raise AssertionError("network activity")
    monkeypatch.setattr(socket, "getaddrinfo", blocked)
    monkeypatch.setattr(socket, "create_connection", blocked)
    assert load_content_reference("text.txt", base_directory=base)
    assert sorted(str(path.relative_to(tmp_path)) for path in tmp_path.rglob("*")) == before


def test_PR017_replacement_before_read_is_rejected(tmp_path, monkeypatch):
    import recursive_integrity_toolkit.utils.paths as paths
    base = _s7_base(tmp_path)
    original = paths._open_content_fd
    def replace_target(path, root):
        # Replace with an outside symlink after resolution. No payload may be read.
        path.unlink()
        path.symlink_to(tmp_path / "outside.txt")
        return original(path, root)
    monkeypatch.setattr(paths, "_open_content_fd", replace_target)
    with pytest.raises(CanonicalValidationError):
        load_content_reference("text.txt", base_directory=base)


def test_PR017_import_does_not_resolve_content(package_root):
    source = r'''
import sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import recursive_integrity_toolkit.config
import recursive_integrity_toolkit.models
import recursive_integrity_toolkit.errors
import recursive_integrity_toolkit.utils.hashing
import socket
calls=[]
def blocked(*args, **kwargs):
    calls.append(1)
    raise AssertionError('unexpected content or network access at import')
Path.resolve=blocked
Path.lstat=blocked
Path.open=blocked
socket.create_connection=blocked
socket.getaddrinfo=blocked
import recursive_integrity_toolkit.utils.paths
import recursive_integrity_toolkit.io.loaders
assert not calls
'''
    result = subprocess.run([sys.executable, "-B", "-c", source, str(package_root.parent)],
                            capture_output=True, text=True, check=False)
    assert result.returncode == 0, result.stdout + result.stderr


def test_PR017_step7_local_fixture(repo_root):
    base = repo_root / "tests/fixtures/content_references"
    path = base / "step7_utf8.txt"
    before = path.read_bytes()
    assert load_content_reference("step7_utf8.txt", base_directory=base) == before.decode("utf-8")
    assert path.read_bytes() == before
