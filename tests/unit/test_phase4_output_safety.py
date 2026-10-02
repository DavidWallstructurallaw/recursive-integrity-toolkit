"""PR-013/015: independent output-boundary and failure-injection contracts.

Filesystem contents below are synthetic. No mathematical oracle is generated.
Existing renderers supply the already accepted bytes; publication must preserve
those bytes, input files, competing files and truthful operational status.
"""
from __future__ import annotations

import errno
import io
import json
import os
from pathlib import Path
from types import SimpleNamespace

import pytest

from recursive_integrity_toolkit.utils import paths


def phase4_step6_view(mode="standard", label="publication-case"):
    from recursive_integrity_toolkit.reports.assembly import privacy_view
    from recursive_integrity_toolkit.result import CanonicalReport
    from recursive_integrity_toolkit.utils.hashing import IdentifierProtection

    payload = {
        "run": {
            "run_id": label, "toolkit_version": "0.1.0.dev2", "report_schema_version": "1.0",
            "started_at": "2026-09-20T00:00:00+00:00", "completed_at": "2026-09-20T00:00:00.500000+00:00",
            "duration_seconds": 0.5, "python_version": "3.12.14", "platform": "independent-test-platform",
            "command": "rit validate", "config_hash": "0123456789abcdef" * 4,
            "random_seed": None, "strict_mode": False, "redacted_mode": False,
            "network_call_count": 0, "deterministic": True, "privacy_mode": "standard",
            "run_status": "complete", "null_reasons": {"random_seed": "No stochastic scenario was requested."},
        },
        "inputs": {}, "observability": {}, "capabilities": {}, "observed_facts": {},
        "derived_metrics": {}, "proxy_signals": {}, "simulations": {},
        "unavailable_conclusions": [], "recommended_next_metadata": [], "warnings": [], "errors": [],
    }
    return privacy_view(CanonicalReport.from_dict(payload), mode=mode,
                        protection=IdentifierProtection.create(secret=b"publication-test-only-key-32byte!"))


def phase4_step6_expected(view):
    from recursive_integrity_toolkit.reports.json_report import render_json
    from recursive_integrity_toolkit.reports.markdown_report import render_markdown

    return {"report.json": render_json(view).encode("utf-8"), "report.md": render_markdown(view).encode("utf-8")}


def phase4_step6_assert_no_temporary(directory):
    assert not list(directory.glob(".rit-stage-*"))


@pytest.mark.parametrize("mode", ["standard", "redacted"])
def test_phase4_step6_publishes_both_exact_utf8_reports_and_preserves_inputs(tmp_path, mode):
    view = phase4_step6_view(mode)
    before = view.to_dict()
    source = tmp_path / "private-input.txt"
    source.write_bytes(b"RAW_PRIVATE_RECORD_NOT_FOR_OUTPUT\x00\xff")
    expected = phase4_step6_expected(view)
    output = tmp_path / "reports"
    result = paths.publish_reports(view, output, input_paths=[source])
    assert result == paths.PublicationResult("complete", None, 0, ("report.json", "report.md"))
    assert {p.name: p.read_bytes() for p in output.iterdir()} == expected
    assert json.loads((output / "report.json").read_bytes()) == before
    assert source.read_bytes() == b"RAW_PRIVATE_RECORD_NOT_FOR_OUTPUT\x00\xff"
    assert view.to_dict() == before
    assert "RAW_PRIVATE_RECORD_NOT_FOR_OUTPUT" not in repr(expected) + repr(result)
    phase4_step6_assert_no_temporary(output)


@pytest.mark.parametrize("value", [
    "", " ", "https://example.invalid/out", "file:///tmp/out", "s3://bucket/out",
    "//server/share", "\\\\server\\share", "\\\\?\\C:\\out", "\\\\.\\NUL",
    "/\\server/share", "\\/server/share", "folder\x00name", "folder\nname", "out\u202ename",
    "C:relative", "folder/file:stream", "CON", "nul.txt", "COM¹.log", "aux .txt",
    "folder/trailing.", "folder/trailing ", "../escape", "folder/../escape", 7, None, b"bytes",
])
def test_phase4_step6_rejects_unsafe_spellings_before_any_filesystem_access(monkeypatch, value):
    def forbidden(*args, **kwargs):
        raise AssertionError("filesystem was touched before lexical rejection")

    monkeypatch.setattr(Path, "lstat", forbidden)
    result = paths.publish_reports(object(), value, input_paths=())
    assert result.code == "E_OUTPUT_PATH_INVALID" and result.exit_code == 2
    assert result.status == "failed" and result.temporary_cleanup_complete


@pytest.mark.parametrize("value,valid", [
    ("C:\\reports", True), ("D:/reports/Unicode-水", True), ("reports/result", True), (".\\reports", True),
    ("C:reports", False), ("/reports", False), ("\\reports", False), ("C:/NUL.txt", False),
    ("C:/name:stream", False), ("\\\\?\\C:\\reports", False), ("\\\\server\\share", False),
])
def test_phase4_step6_windows_lexical_rules_are_independent_of_host(value, valid):
    if valid:
        paths._output_validate_text(value, windows=True)
    else:
        with pytest.raises(paths._OutputFailure):
            paths._output_validate_text(value, windows=True)


def test_phase4_step6_all_input_spellings_checked_before_filesystem_access(tmp_path, monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("unsafe input triggered filesystem access")

    monkeypatch.setattr(Path, "lstat", forbidden)
    result = paths.publish_reports(object(), tmp_path / "out", input_paths=[tmp_path / "a", "https://private.invalid/input"])
    assert result.code == "E_OUTPUT_PATH_INVALID"


def test_phase4_step6_pathlike_objects_are_not_coerced(tmp_path):
    class Hostile:
        def __str__(self):
            raise AssertionError("arbitrary string conversion")

        def __fspath__(self):
            raise AssertionError("arbitrary filesystem conversion")

    for directory, inputs in ((Hostile(), ()), (tmp_path / "out", (Hostile(),)), (tmp_path / "out", Hostile())):
        result = paths.publish_reports(object(), directory, input_paths=inputs)
        assert result.code == "E_OUTPUT_PATH_INVALID"


def test_phase4_step6_relative_unicode_destination_and_literal_expansion(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    output = "~$PRIVATE_REPORT_水"
    result = paths.publish_reports(phase4_step6_view(), output, input_paths=())
    assert result.status == "complete"
    assert {p.name for p in tmp_path.iterdir()} == {output}


def test_phase4_step6_missing_ancestors_are_not_created(tmp_path):
    result = paths.publish_reports(phase4_step6_view(), tmp_path / "missing" / "out", input_paths=())
    assert result.code == "E_OUTPUT_IO"
    assert not (tmp_path / "missing").exists()


@pytest.mark.parametrize("name", ["report.json", "report.md"])
def test_phase4_step6_existing_targets_and_hardlink_aliases_are_never_replaced(tmp_path, name):
    source = tmp_path / "source"
    source.write_bytes(b"PRIVATE_INPUT")
    output = tmp_path / "out"
    output.mkdir()
    os.link(source, output / name)
    unrelated = output / "unrelated"
    unrelated.write_bytes(b"UNRELATED")
    result = paths.publish_reports(phase4_step6_view(), output, input_paths=(source,))
    assert result.code == "E_OUTPUT_EXISTS" and result.published_files == ()
    assert source.read_bytes() == (output / name).read_bytes() == b"PRIVATE_INPUT"
    assert unrelated.read_bytes() == b"UNRELATED"
    assert {p.name for p in output.iterdir()} == {name, "unrelated"}


@pytest.mark.parametrize("kind", ["directory", "output_link", "ancestor_link", "target_link", "dangling_target", "input_link"])
def test_phase4_step6_rejects_unsafe_destination_types_and_symlinks(tmp_path, kind):
    view = phase4_step6_view()
    source = tmp_path / "input"
    source.write_bytes(b"SECRET_SOURCE")
    output = tmp_path / "out"
    output.mkdir()
    inputs = (source,)
    if kind == "directory":
        (output / "report.json").mkdir()
    elif kind == "output_link":
        link = tmp_path / "linked-output"
        link.symlink_to(output, target_is_directory=True)
        output = link
    elif kind == "ancestor_link":
        link = tmp_path / "linked-parent"
        link.symlink_to(output, target_is_directory=True)
        output = link / "child"
    elif kind in ("target_link", "dangling_target"):
        (output / "report.json").symlink_to(source if kind == "target_link" else tmp_path / "missing")
    else:
        link = tmp_path / "input-link"
        link.symlink_to(source)
        inputs = (link,)
    result = paths.publish_reports(view, output, input_paths=inputs)
    assert result.status == "failed" and result.exit_code == 1
    assert result.code in ("E_OUTPUT_EXISTS", "E_OUTPUT_UNSAFE")
    assert source.read_bytes() == b"SECRET_SOURCE"
    assert result.published_files == ()


def test_phase4_step6_remote_link_target_is_never_resolved(tmp_path, monkeypatch):
    output = tmp_path / "link"
    output.symlink_to("//server/private/share", target_is_directory=True)

    def forbidden(*args, **kwargs):
        raise AssertionError("symlink target must not be read or resolved")

    monkeypatch.setattr(os, "readlink", forbidden)
    monkeypatch.setattr(Path, "resolve", forbidden)
    result = paths.publish_reports(phase4_step6_view(), output, input_paths=())
    assert result.code == "E_OUTPUT_UNSAFE"


def test_phase4_step6_windows_reparse_points_are_rejected_before_children(tmp_path, monkeypatch):
    output = tmp_path / "junction"
    output.mkdir()
    original = Path.lstat

    def reparse(path, *args, **kwargs):
        if path == output:
            return SimpleNamespace(st_mode=0o40700, st_reparse_tag=0, st_file_attributes=1024)
        assert output not in path.parents, "reparse point was traversed"
        return original(path, *args, **kwargs)

    monkeypatch.setattr(Path, "lstat", reparse)
    result = paths.publish_reports(phase4_step6_view(), output / "child", input_paths=())
    assert result.code == "E_OUTPUT_UNSAFE"


@pytest.mark.parametrize("role", ["directory", "report.json", "report.md"])
def test_phase4_step6_declared_missing_inputs_cannot_become_outputs(tmp_path, role):
    output = tmp_path / "out"
    source = output if role == "directory" else output / role
    result = paths.publish_reports(phase4_step6_view(), output, input_paths=(source,))
    assert result.code == "E_OUTPUT_INPUT_COLLISION"
    assert not output.exists()


@pytest.mark.parametrize("renderer", ["json_report", "markdown_report"])
def test_phase4_step6_both_renderers_must_finish_before_writes(tmp_path, monkeypatch, renderer):
    import importlib

    module = importlib.import_module("recursive_integrity_toolkit.reports." + renderer)

    def fail(value):
        raise ValueError("PRIVATE_RENDER_EXCEPTION")

    monkeypatch.setattr(module, "render_json" if renderer == "json_report" else "render_markdown", fail)
    result = paths.publish_reports(phase4_step6_view(), tmp_path / "out", input_paths=())
    assert result.code == "E_OUTPUT_RENDER" and result.exit_code == 4
    assert not (tmp_path / "out").exists()
    assert "PRIVATE_RENDER_EXCEPTION" not in repr(result)


def test_phase4_step6_raw_or_forged_reports_cannot_reach_writes(tmp_path):
    from recursive_integrity_toolkit.result import CanonicalReport, SafeReportView

    view = phase4_step6_view()
    forged = object.__new__(SafeReportView)
    object.__setattr__(forged, "_report", CanonicalReport.from_dict(view.to_dict()))
    object.__setattr__(forged._report, "sections", {"raw": "PRIVATE_INVALID"})
    for value in (view.to_dict(), CanonicalReport.from_dict(view.to_dict()), object(), forged):
        result = paths.publish_reports(value, tmp_path / "out", input_paths=())
        assert result.code == "E_OUTPUT_RENDER"
        assert not (tmp_path / "out").exists()


def test_phase4_step6_stages_both_complete_private_files_before_first_publish(tmp_path, monkeypatch):
    view = phase4_step6_view()
    expected = phase4_step6_expected(view)
    publish = paths._output_publish_one
    seen = []

    def inspect(source, target):
        if not seen:
            assert {p.name: p.read_bytes() for p in source.parent.iterdir()} == expected
            if os.name != "nt":
                assert source.parent.stat().st_mode & 0o077 == 0
                assert all(p.stat().st_mode & 0o077 == 0 for p in source.parent.iterdir())
        seen.append(target.name)
        return publish(source, target)

    monkeypatch.setattr(paths, "_output_publish_one", inspect)
    result = paths.publish_reports(view, tmp_path / "out", input_paths=())
    assert result.status == "complete" and seen == ["report.json", "report.md"]


@pytest.mark.parametrize("failure", ["permission", "disk_first", "disk_second", "zero_write", "fsync"])
def test_phase4_step6_staging_failures_leave_no_reports_or_temporary_payloads(tmp_path, monkeypatch, failure):
    view = phase4_step6_view()
    output = tmp_path / "out"
    output.mkdir()
    actual_write = os.write
    actual_open = os.open
    file_number = 0

    def write(descriptor, data):
        if failure == "zero_write":
            return 0
        if (failure == "disk_first" and file_number == 1) or (failure == "disk_second" and file_number == 2):
            actual_write(descriptor, data[:7])
            raise OSError(errno.ENOSPC, "PRIVATE_DISK_DETAIL")
        return actual_write(descriptor, data)

    def opened(path, flags, *args, **kwargs):
        nonlocal file_number
        if flags & os.O_CREAT:
            file_number += 1
        return actual_open(path, flags, *args, **kwargs)

    def denied(*args, **kwargs):
        raise PermissionError("PRIVATE_PERMISSION_DETAIL")

    monkeypatch.setattr(os, "open", opened)
    monkeypatch.setattr(os, "write", write)
    if failure == "permission":
        monkeypatch.setattr(paths.tempfile, "mkdtemp", denied)
    if failure == "fsync":
        monkeypatch.setattr(os, "fsync", denied)
    result = paths.publish_reports(view, output, input_paths=())
    assert result.status == "failed" and result.code == "E_OUTPUT_IO"
    assert result.published_files == () and result.temporary_cleanup_complete
    assert list(output.iterdir()) == []
    assert "PRIVATE_" not in repr(result)


def test_phase4_step6_short_writes_are_completed_without_truncation(tmp_path, monkeypatch):
    actual = os.write
    monkeypatch.setattr(os, "write", lambda descriptor, data: actual(descriptor, data[:17]))
    view = phase4_step6_view()
    result = paths.publish_reports(view, tmp_path / "out", input_paths=())
    assert result.status == "complete"
    assert {p.name: p.read_bytes() for p in (tmp_path / "out").iterdir()} == phase4_step6_expected(view)


@pytest.mark.parametrize("failure", ["first", "second", "after_first", "after_second"])
def test_phase4_step6_publication_failures_roll_back_only_own_outputs(tmp_path, monkeypatch, failure):
    original = paths._output_publish_one
    output = tmp_path / "out"
    output.mkdir()
    (output / "keep").write_bytes(b"EXISTING_UNRELATED")

    def fail(source, target):
        chosen = "report.json" if failure in ("first", "after_first") else "report.md"
        if target.name == chosen:
            if failure.startswith("after_"):
                original(source, target)
            raise OSError(errno.EIO, "PRIVATE_PUBLISH_ERROR")
        return original(source, target)

    monkeypatch.setattr(paths, "_output_publish_one", fail)
    result = paths.publish_reports(phase4_step6_view(), output, input_paths=())
    assert result.status == "failed" and result.code == "E_OUTPUT_IO"
    assert result.residual_files == () and result.temporary_cleanup_complete
    assert {p.name: p.read_bytes() for p in output.iterdir()} == {"keep": b"EXISTING_UNRELATED"}


@pytest.mark.parametrize("name", ["report.json", "report.md"])
def test_phase4_step6_concurrent_target_creation_is_not_overwritten(tmp_path, monkeypatch, name):
    original = paths._output_publish_one
    output = tmp_path / "out"
    output.mkdir()

    def compete(source, target):
        if target.name == name:
            target.write_bytes(b"COMPETING_OWNER")
        return original(source, target)

    monkeypatch.setattr(paths, "_output_publish_one", compete)
    result = paths.publish_reports(phase4_step6_view(), output, input_paths=())
    assert result.status == "failed" and result.code == "E_OUTPUT_EXISTS"
    assert {p.name: p.read_bytes() for p in output.iterdir()} == {name: b"COMPETING_OWNER"}


def test_phase4_step6_real_concurrent_publishers_do_not_mix_report_pairs(tmp_path, monkeypatch):
    from concurrent.futures import ThreadPoolExecutor
    from threading import Barrier

    output = tmp_path / "out"
    output.mkdir()
    views = [phase4_step6_view(label="first"), phase4_step6_view(label="second")]
    expected = [phase4_step6_expected(view) for view in views]
    assert expected[0] != expected[1]
    barrier = Barrier(2)
    original = paths._output_publish_one

    def compete(source, target):
        if target.name == "report.json":
            barrier.wait(timeout=15)
        return original(source, target)

    monkeypatch.setattr(paths, "_output_publish_one", compete)
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(paths.publish_reports, view, output, input_paths=()) for view in views]
        results = [future.result(timeout=30) for future in futures]
    winners = [index for index, result in enumerate(results) if result.status == "complete"]
    assert len(winners) == 1
    assert results[1 - winners[0]].code == "E_OUTPUT_EXISTS"
    assert {p.name: p.read_bytes() for p in output.iterdir()} == expected[winners[0]]


@pytest.mark.parametrize("failure", ["rollback", "stage_file", "stage_directory", "replacement", "extra_stage_file"])
def test_phase4_step6_incomplete_cleanup_is_explicit_and_foreign_files_survive(tmp_path, monkeypatch, failure):
    output = tmp_path / "out"
    output.mkdir()
    publish = paths._output_publish_one
    unlink = Path.unlink
    rmdir = Path.rmdir

    def fail_publish(source, target):
        if failure == "stage_file" and os.name == "nt":
            raise OSError("PRIVATE_PRE_RENAME_FAILURE")
        if failure in ("rollback", "replacement") and target.name == "report.md":
            if failure == "replacement":
                (output / "report.json").unlink()
                (output / "report.json").write_bytes(b"REPLACEMENT_OWNER")
            raise OSError("PRIVATE_SECOND_FAILURE")
        if failure == "extra_stage_file":
            (source.parent / "foreign").write_bytes(b"FOREIGN_STAGE_FILE")
        return publish(source, target)

    def refuse_unlink(path, *args, **kwargs):
        if (failure == "rollback" and path == output / "report.json"
                or failure == "stage_file" and path.parent.name.startswith(".rit-stage-")):
            raise PermissionError("PRIVATE_CLEANUP_FAILURE")
        return unlink(path, *args, **kwargs)

    def refuse_rmdir(path, *args, **kwargs):
        if failure == "stage_directory" and path.name.startswith(".rit-stage-"):
            raise PermissionError("PRIVATE_DIRECTORY_CLEANUP")
        return rmdir(path, *args, **kwargs)

    monkeypatch.setattr(paths, "_output_publish_one", fail_publish)
    monkeypatch.setattr(Path, "unlink", refuse_unlink)
    monkeypatch.setattr(Path, "rmdir", refuse_rmdir)
    result = paths.publish_reports(phase4_step6_view(), output, input_paths=())
    # On Windows fail before rename so owned stage files need cleanup too.
    assert result.status == "incomplete" and result.exit_code == 1
    if failure == "replacement":
        assert (output / "report.json").read_bytes() == b"REPLACEMENT_OWNER"
        assert result.residual_files == ("report.json",)
    if failure == "extra_stage_file":
        assert [p.read_bytes() for p in output.glob(".rit-stage-*/foreign")] == [b"FOREIGN_STAGE_FILE"]
    assert "PRIVATE_" not in repr(result)


def test_phase4_step6_removed_report_during_cleanup_cannot_be_announced_success(tmp_path, monkeypatch):
    clean = paths._output_clean_stage
    output = tmp_path / "out"

    def interfere(stage, chain, owned):
        result = clean(stage, chain, owned)
        (output / "report.md").unlink()
        return result

    monkeypatch.setattr(paths, "_output_clean_stage", interfere)
    result = paths.publish_reports(phase4_step6_view(), output, input_paths=())
    assert result.code == "E_OUTPUT_UNSAFE" and result.status == "failed"
    assert list(output.iterdir()) == []


def test_phase4_step6_parent_change_is_detected_and_unknown_files_not_deleted(tmp_path, monkeypatch):
    output = tmp_path / "out"
    moved = tmp_path / "moved"
    original = paths._output_write
    view = phase4_step6_view()

    def change_parent(path, data, owned):
        original(path, data, owned)
        if path.name == "report.md":
            output.rename(moved)
            output.mkdir()
            (output / "private-other").write_bytes(b"OTHER_OWNER")

    monkeypatch.setattr(paths, "_output_write", change_parent)
    result = paths.publish_reports(view, output, input_paths=())
    assert result.status == "incomplete" and result.code == "E_OUTPUT_UNSAFE"
    assert not result.temporary_cleanup_complete
    assert {p.name: p.read_bytes() for p in output.iterdir()} == {"private-other": b"OTHER_OWNER"}
    assert list(moved.glob(".rit-stage-*/report.json"))


def test_phase4_step6_does_not_read_inputs_run_calculations_or_use_network(tmp_path, monkeypatch, capsys):
    import socket
    import sys

    view = phase4_step6_view("redacted")
    source = tmp_path / "private-input"
    source.write_bytes(b"PRIVATE_SOURCE_SENTINEL")
    original = os.open

    def no_input(path, *args, **kwargs):
        assert Path(path) != source, "publisher read an input"
        return original(path, *args, **kwargs)

    def no_network(*args, **kwargs):
        raise AssertionError("publisher attempted a network call")

    def no_analysis(frame, event, argument):
        if event == "call":
            module = frame.f_globals.get("__name__", "")
            assert not module.startswith(("recursive_integrity_toolkit.metrics.", "recursive_integrity_toolkit.io.",
                                          "recursive_integrity_toolkit.representations.")), module

    monkeypatch.setattr(os, "open", no_input)
    monkeypatch.setattr(socket, "socket", no_network)
    monkeypatch.setattr(socket, "getaddrinfo", no_network)
    previous = sys.getprofile()
    try:
        sys.setprofile(no_analysis)
        result = paths.publish_reports(view, tmp_path / "out", input_paths=(source,))
    finally:
        sys.setprofile(previous)
    assert result.status == "complete"
    assert source.read_bytes() == b"PRIVATE_SOURCE_SENTINEL"
    captured = capsys.readouterr()
    assert captured.out == captured.err == ""


@pytest.mark.parametrize("code,exit_code", [
    ("E_OUTPUT_PATH_INVALID", 2), ("E_OUTPUT_INPUT_COLLISION", 1), ("E_OUTPUT_EXISTS", 1),
    ("E_OUTPUT_UNSAFE", 1), ("E_OUTPUT_IO", 1), ("E_OUTPUT_RENDER", 4),
    ("E_OUTPUT_INTERNAL", 4), ("E_OUTPUT_CLEANUP", 1),
])
def test_phase4_step6_failure_diagnostics_are_fixed_safe_actionable_lines(code, exit_code):
    from recursive_integrity_toolkit.utils.logging import emit_publication_diagnostic, format_publication_diagnostic

    result = paths.PublicationResult("failed", code, exit_code)
    text = format_publication_diagnostic(result)
    body = json.loads(text)
    assert body["code"] == code and body["exit_code"] == exit_code
    assert body["severity"] == ("fatal" if exit_code == 4 else "error")
    assert body["remediation"] and body["message"] and text.count("\n") == 1
    stream = io.StringIO()
    emit_publication_diagnostic(result, stream=stream)
    assert stream.getvalue() == text


@pytest.mark.parametrize("field,value", [
    ("published_files", ("PRIVATE_PATH",)), ("residual_files", ("PRIVATE_RECORD",)),
    ("code", "PRIVATE_EXCEPTION"), ("status", "PRIVATE_STATUS"), ("exit_code", True),
])
def test_phase4_step6_forged_publication_results_cannot_inject_diagnostics(field, value):
    from recursive_integrity_toolkit.utils.logging import format_publication_diagnostic

    result = paths.PublicationResult("failed", "E_OUTPUT_IO", 1)
    object.__setattr__(result, field, value)
    with pytest.raises((TypeError, ValueError)) as caught:
        format_publication_diagnostic(result)
    assert "PRIVATE_" not in str(caught.value)
