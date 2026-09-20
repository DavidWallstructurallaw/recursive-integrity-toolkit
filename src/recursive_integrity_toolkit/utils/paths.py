"""Validate local inputs and explicitly publish a pair of safe reports.

Owner IDs:
    PR-017, PR-002 supporting file inventory; PR-013, PR-015 output publication.

Inputs:
    Explicit local input paths or content-reference text with an approved base;
    a SafeReportView, output directory and complete declared input path list.

Outputs:
    Checked input paths, or a content-free PublicationResult for report.json/md.

Assumptions:
    The configured base and its directory tree are trusted and stable during a
    read. An omitted base uses the directory containing the declared records file.

Limits:
    Input helpers remain read-only. Publication renders before writes, rejects
    links/reparse points, and never replaces a destination. No input reads,
    network, expansion, analysis or privacy-policy selection is added.
    OS mounts and hostile concurrent directory replacement are not sandboxed.
    Content reads must use the dedicated loader, not a later unchecked path open.
    Publication requires stable trusted ancestors. Two names are not a crash-
    atomic transaction; handled failures remove only identity-matched own files.

Current phase status:
    Preserved Phase 2 Step 7 input security; additive Phase 4 Step 6 publication.
"""

from __future__ import annotations

import os
import re
import stat
from pathlib import Path, PureWindowsPath

from ..errors import CanonicalValidationError, ErrorCode, InputError


_SCHEME = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
_DRIVE_ABSOLUTE = re.compile(r"^[A-Za-z]:[\\/]")
_RESERVED = {"CON", "PRN", "AUX", "NUL", "CONIN$", "CONOUT$"}
_RESERVED.update(f"{prefix}{digit}" for prefix in ("COM", "LPT") for digit in "123456789¹²³")


def local_input_path(value: str | Path) -> Path:
    """Reject URI, UNC, device, and malformed paths before filesystem access."""
    if not isinstance(value, (str, Path)):
        raise InputError(ErrorCode.FILE_FORMAT_UNSUPPORTED, "input path must be local text")
    text = str(value)
    if not text or "\x00" in text:
        raise InputError(ErrorCode.FILE_FORMAT_UNSUPPORTED, "input path is empty or invalid")
    if text.startswith(("//", "\\\\")):
        raise InputError(ErrorCode.FILE_FORMAT_UNSUPPORTED, "network and device paths are unsupported")
    if _SCHEME.match(text):
        if os.name != "nt" or not _DRIVE_ABSOLUTE.match(text):
            raise InputError(ErrorCode.FILE_FORMAT_UNSUPPORTED, "URI and nonlocal input paths are unsupported")
    # On POSIX, absolute() deliberately avoids resolving a symlink here.
    return Path(os.path.abspath(text))


def _content_error(code: ErrorCode, message: str) -> CanonicalValidationError:
    return CanonicalValidationError(code, message, field="content", file_path="[redacted]")


def _content_lexical(value: object, *, allow_absolute: bool, link_target: bool = False) -> Path:
    """Reject network/device forms before any filesystem call; never URL-decode."""
    if type(value) is not str or not value or not value.strip():
        raise _content_error(ErrorCode.SCHEMA_TYPE, "content reference must be nonempty text")
    if any(ord(character) < 32 or ord(character) == 127 for character in value):
        raise _content_error(ErrorCode.CONTENT_REF_OUTSIDE_BASE, "control characters are forbidden in content references")
    # Windows readlink returns a substitution path. Only local drive targets can
    # shed that OS-supplied prefix; user-supplied device paths stay forbidden.
    if link_target and os.name == "nt" and value.startswith("\\\\?\\"):
        if not _DRIVE_ABSOLUTE.match(value[4:]):
            raise _content_error(ErrorCode.CONTENT_REF_OUTSIDE_BASE, "nonlocal symlink target is forbidden")
        value = value[4:]
    if value.startswith(("//", "\\\\")):
        raise _content_error(ErrorCode.CONTENT_REF_OUTSIDE_BASE, "network and device content references are forbidden")
    if _SCHEME.match(value) and not (os.name == "nt" and _DRIVE_ABSOLUTE.match(value)):
        raise _content_error(ErrorCode.CONTENT_REF_OUTSIDE_BASE, "URI or non-native drive reference is forbidden")
    portable = value.replace("\\", "/")
    windows = PureWindowsPath(value)
    absolute = Path(portable).is_absolute() or bool(windows.drive or windows.root)
    if absolute and (not allow_absolute or not Path(portable).is_absolute()):
        raise _content_error(ErrorCode.CONTENT_REF_OUTSIDE_BASE, "absolute content reference is not explicitly allowed")
    path = Path(portable)
    for part in path.parts:
        if part in (path.anchor, ".", ".."):
            continue
        if ":" in part or part.endswith((" ", ".")) or part.split(".")[0].upper() in _RESERVED:
            raise _content_error(ErrorCode.CONTENT_REF_OUTSIDE_BASE, "ambiguous or device-like path component is forbidden")
    return path


def _content_base(base_directory: str | Path | None, records_path: str | Path | None) -> Path:
    """Resolve a trusted, explicitly supplied local base; no implicit cwd base."""
    if base_directory is None and records_path is None:
        raise _content_error(ErrorCode.CONFIG_INVALID, "supply a content base or the records file path")
    supplied = base_directory if base_directory is not None else records_path
    if type(supplied) not in (str, type(Path())):
        raise _content_error(ErrorCode.CONFIG_INVALID, "content base declaration must be a local path")
    try:
        base = local_input_path(supplied)
        if base_directory is None:
            base = base.parent
        base = base.resolve(strict=True)
        # Configured base is trusted, but a directly resolved UNC base is rejected.
        local_input_path(base)
        if not base.is_dir():
            raise _content_error(ErrorCode.CONFIG_INVALID, "content base must be an existing directory")
        return base
    except CanonicalValidationError:
        raise
    except (InputError, OSError, ValueError, RuntimeError):
        raise _content_error(ErrorCode.CONFIG_INVALID, "content base is not a usable local directory") from None


def _inside_base(path: Path, base: Path) -> tuple[str, ...]:
    try:
        return path.relative_to(base).parts
    except ValueError:
        raise _content_error(ErrorCode.CONTENT_REF_OUTSIDE_BASE, "content reference escapes its approved base") from None


def resolve_content_reference(reference: str, *, base_directory: str | Path | None = None,
                              records_path: str | Path | None = None,
                              allow_absolute: bool = False) -> Path:
    """Resolve links component by component without following remote link targets.

    Both slash spellings are treated as portable separators. No tilde, variable,
    percent escape, URI, extension, or metadata value is expanded. Absolute
    opt-in remains constrained to this one base; it grants no outside access.
    """
    if type(allow_absolute) is not bool:
        raise _content_error(ErrorCode.CONFIG_INVALID, "allow_absolute must be an explicit boolean")
    declared = _content_lexical(reference, allow_absolute=allow_absolute)
    base = _content_base(base_directory, records_path)
    pending = list(_inside_base(declared, base) if declared.is_absolute() else declared.parts)
    current = base
    links = 0
    try:
        while pending:
            part = pending.pop(0)
            if part == "..":
                if current == base:
                    raise _content_error(ErrorCode.CONTENT_REF_OUTSIDE_BASE, "content reference escapes its approved base")
                current = current.parent
                continue
            if part == ".":
                continue
            candidate = current / part
            info = candidate.lstat()
            reparse = getattr(info, "st_reparse_tag", 0)
            is_link = stat.S_ISLNK(info.st_mode) or reparse in (
                getattr(stat, "IO_REPARSE_TAG_SYMLINK", -1), getattr(stat, "IO_REPARSE_TAG_MOUNT_POINT", -2))
            if reparse and not is_link:
                raise _content_error(ErrorCode.FILE_FORMAT_UNSUPPORTED, "unsupported filesystem reparse point")
            if is_link:
                links += 1
                if links > 40:
                    raise _content_error(ErrorCode.FILE_PARSE, "content symlink chain is cyclic or exceeds the safety limit")
                target = _content_lexical(os.readlink(candidate), allow_absolute=True, link_target=True)
                if target.is_absolute():
                    pending = list(_inside_base(target, base)) + pending
                    current = base
                else:
                    pending = list(target.parts) + pending
                continue
            if pending and not stat.S_ISDIR(info.st_mode):
                raise _content_error(ErrorCode.FILE_FORMAT_UNSUPPORTED, "intermediate content path must be a directory")
            current = candidate
        _inside_base(current, base)
        info = current.lstat()
        if not stat.S_ISREG(info.st_mode) or stat.S_ISLNK(info.st_mode) or getattr(info, "st_reparse_tag", 0):
            raise _content_error(ErrorCode.FILE_FORMAT_UNSUPPORTED, "content reference must resolve to a regular local file")
        return current
    except CanonicalValidationError:
        raise
    except FileNotFoundError:
        raise _content_error(ErrorCode.CONTENT_REF_MISSING, "content file or symlink target is missing") from None
    except (OSError, ValueError, RuntimeError):
        raise _content_error(ErrorCode.FILE_PARSE, "content reference cannot be resolved safely") from None


def _open_content_fd(path: Path, base: Path) -> int:
    """Open an already resolved path; pin directories and disallow links on POSIX.

    Caller verifies file identity before reading on every platform. On systems
    without dir_fd support, stable trusted directory trees remain a prerequisite.
    """
    parts = _inside_base(path, base)
    flags = os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_NONBLOCK", 0)
    if os.open not in os.supports_dir_fd or not hasattr(os, "O_NOFOLLOW"):
        return os.open(path, flags)
    directory_flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    directory = os.open(base, directory_flags)
    try:
        for part in parts[:-1]:
            child = os.open(part, directory_flags, dir_fd=directory)
            os.close(directory)
            directory = child
        return os.open(parts[-1], flags | os.O_NOFOLLOW, dir_fd=directory)
    finally:
        os.close(directory)


# Phase 4 Step 6 additions. Inherited input helpers above remain byte-exact.
from dataclasses import dataclass
import tempfile
import unicodedata


_OUTPUT_NAMES = ("report.json", "report.md")
_OUTPUT_CODES = {
    "E_OUTPUT_PATH_INVALID": 2,
    "E_OUTPUT_INPUT_COLLISION": 1,
    "E_OUTPUT_EXISTS": 1,
    "E_OUTPUT_UNSAFE": 1,
    "E_OUTPUT_IO": 1,
    "E_OUTPUT_RENDER": 4,
    "E_OUTPUT_INTERNAL": 4,
    "E_OUTPUT_CLEANUP": 1,
}


@dataclass(frozen=True, slots=True)
class PublicationResult:
    """Operational outcome, separate from the unchanged analytical report.

    published_files records successful publication calls, even if rolled back.
    residual_files names outputs whose cleanup cannot be confirmed. It never
    contains a supplied path, source value, temporary name or exception text.
    """

    status: str
    code: str | None
    exit_code: int
    published_files: tuple[str, ...] = ()
    residual_files: tuple[str, ...] = ()
    temporary_cleanup_complete: bool = True

    def __post_init__(self):
        if type(self.status) is not str or self.status not in ("complete", "failed", "incomplete"):
            raise ValueError("invalid publication status")
        if type(self.exit_code) is not int or type(self.temporary_cleanup_complete) is not bool:
            raise TypeError("invalid publication outcome types")
        for names in (self.published_files, self.residual_files):
            if (type(names) is not tuple or any(type(name) is not str or name not in _OUTPUT_NAMES for name in names)
                    or tuple(name for name in _OUTPUT_NAMES if name in names) != names):
                raise ValueError("publication filenames must be fixed, unique and ordered")
        if self.status == "complete":
            if (self.code is not None or self.exit_code != 0 or self.published_files != _OUTPUT_NAMES
                    or self.residual_files or not self.temporary_cleanup_complete):
                raise ValueError("complete publication requires both outputs and completed cleanup")
        else:
            if type(self.code) is not str or self.code not in _OUTPUT_CODES or self.exit_code != _OUTPUT_CODES[self.code]:
                raise ValueError("invalid publication failure code")
            incomplete = bool(self.residual_files) or not self.temporary_cleanup_complete
            if (self.status == "incomplete") != incomplete:
                raise ValueError("publication failure status must disclose residual effects")


class _OutputFailure(Exception):
    """Private fixed-code control flow, with no captured operating-system text."""

    def __init__(self, code):
        self.code = code
        super().__init__(code)


def _output_validate_text(text: str, *, windows: bool) -> None:
    """Validate native spelling without touching a filesystem or expanding it."""
    if type(text) is not str or not text or not text.strip():
        raise _OutputFailure("E_OUTPUT_PATH_INVALID")
    if any(unicodedata.category(character) in ("Cc", "Cf", "Cs", "Zl", "Zp") for character in text):
        raise _OutputFailure("E_OUTPUT_PATH_INVALID")
    portable = text.replace("\\", "/")
    if portable.startswith("//") or (not windows and "\\" in text):
        raise _OutputFailure("E_OUTPUT_PATH_INVALID")
    drive = bool(_DRIVE_ABSOLUTE.match(text))
    if _SCHEME.match(text) and not (windows and drive):
        raise _OutputFailure("E_OUTPUT_PATH_INVALID")
    if windows and portable.startswith("/"):
        raise _OutputFailure("E_OUTPUT_PATH_INVALID")
    tail = portable[3:] if windows and drive else portable
    for part in tail.split("/"):
        if part in ("", "."):
            continue
        if (part == ".." or ":" in part or part.endswith((" ", "."))
                or part.split(".", 1)[0].rstrip(" .").upper() in _RESERVED):
            raise _OutputFailure("E_OUTPUT_PATH_INVALID")


def _output_local(value) -> Path:
    if type(value) not in (str, type(Path())):
        raise _OutputFailure("E_OUTPUT_PATH_INVALID")
    text = str(value)
    _output_validate_text(text, windows=os.name == "nt")
    absolute = os.path.abspath(text)
    _output_validate_text(absolute, windows=os.name == "nt")
    return Path(absolute)


def _output_info(path):
    try:
        return path.lstat()
    except FileNotFoundError:
        return None


def _output_is_link(info):
    return (stat.S_ISLNK(info.st_mode) or bool(getattr(info, "st_reparse_tag", 0))
            or bool(getattr(info, "st_file_attributes", 0) & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 1024)))


def _output_identity(info):
    if not info.st_ino:
        raise _OutputFailure("E_OUTPUT_UNSAFE")
    return info.st_dev, info.st_ino


def _output_fingerprint(info):
    return (*_output_identity(info), info.st_size, info.st_mtime_ns)


def _output_walk(path, *, missing=False):
    """Inspect one component at a time; never resolve or follow a link target."""
    chain = []
    current = Path(path.anchor)
    components = (current, *path.parts[1:])
    for index, part in enumerate(components):
        current = part if index == 0 else current / part
        info = _output_info(current)
        if info is None:
            if missing:
                return chain, None
            raise _OutputFailure("E_OUTPUT_IO")
        if _output_is_link(info):
            raise _OutputFailure("E_OUTPUT_UNSAFE")
        if index < len(components) - 1 and not stat.S_ISDIR(info.st_mode):
            raise _OutputFailure("E_OUTPUT_UNSAFE")
        if stat.S_ISDIR(info.st_mode):
            chain.append((current, _output_identity(info)))
    return chain, info


def _output_recheck(chain):
    for path, identity in chain:
        info = _output_info(path)
        if info is None or _output_is_link(info) or not stat.S_ISDIR(info.st_mode) or _output_identity(info) != identity:
            raise _OutputFailure("E_OUTPUT_UNSAFE")


def _output_prepare(directory, inputs):
    targets = tuple(directory / name for name in _OUTPUT_NAMES)
    forbidden = {os.path.normcase(str(path)) for path in (directory, *targets)}
    if any(os.path.normcase(str(path)) in forbidden for path in inputs):
        raise _OutputFailure("E_OUTPUT_INPUT_COLLISION")
    for path in inputs:
        _output_walk(path, missing=True)
    parent_chain, parent = _output_walk(directory.parent)
    if not stat.S_ISDIR(parent.st_mode):
        raise _OutputFailure("E_OUTPUT_UNSAFE")
    info = _output_info(directory)
    if info is not None:
        if _output_is_link(info) or not stat.S_ISDIR(info.st_mode):
            raise _OutputFailure("E_OUTPUT_UNSAFE")
        for target in targets:
            if _output_info(target) is not None:
                raise _OutputFailure("E_OUTPUT_EXISTS")
    return parent_chain, info


def _output_write(path, payload, owned):
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(path, flags, 0o600)
    try:
        owned[path.name] = _output_fingerprint(os.fstat(descriptor))
        offset = 0
        while offset < len(payload):
            written = os.write(descriptor, memoryview(payload)[offset:])
            if written <= 0:
                raise OSError("staged report write made no progress")
            offset += written
        os.fsync(descriptor)
        info = os.fstat(descriptor)
        if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1 or info.st_size != len(payload):
            raise _OutputFailure("E_OUTPUT_UNSAFE")
    finally:
        try:
            owned[path.name] = _output_fingerprint(os.fstat(descriptor))
        finally:
            os.close(descriptor)


def _output_publish_one(source, target):
    """No fallback to an overwriting rename or a visible partial byte copy."""
    if os.name == "nt":
        os.rename(source, target)
    else:
        os.link(source, target, follow_symlinks=False)


def _output_remove_owned(path, fingerprint, chain):
    """Return absent/removed, or refuse when identity/parent/metadata changed."""
    try:
        _output_recheck(chain)
        info = _output_info(path)
        if info is None:
            return True
        if _output_is_link(info) or not stat.S_ISREG(info.st_mode) or _output_fingerprint(info) != fingerprint:
            return False
        path.unlink()
        return True
    except Exception:
        return False


def _output_clean_stage(stage, stage_chain, owned):
    if stage is None:
        return True
    if stage_chain is None:
        return False
    okay = True
    for name, fingerprint in owned.items():
        okay = _output_remove_owned(stage / name, fingerprint, stage_chain) and okay
    try:
        _output_recheck(stage_chain)
        stage.rmdir()
    except Exception:
        okay = False
    return okay


def _output_rollback(directory, chain, owned, attempted, published):
    residual = []
    if chain is None:
        return residual
    for name in attempted:
        try:
            _output_recheck(chain)
            info = _output_info(directory / name)
            is_ours = info is not None and not _output_is_link(info) and _output_fingerprint(info) == owned[name]
            if is_ours:
                if not _output_remove_owned(directory / name, owned[name], chain):
                    residual.append(name)
            elif info is not None and name in published:
                residual.append(name)
        except Exception:
            residual.append(name)
    return residual


def publish_reports(report, output_directory, *, input_paths) -> PublicationResult:
    """Render an exact SafeReportView and publish both required UTF-8 files.

    input_paths is an explicit list/tuple of every consumed or declared input,
    including config, mapping, order and salt files. No input content is opened.
    Parents must exist; only the output leaf may be created. All path ancestors
    must be stable local directories without links or reparse points. Missing
    inputs remain protected by spelling, allowing an error-only report.

    The result never contains caller text. Every handled error is nonzero. A
    crash or hostile ancestor replacement is outside this portable guarantee.
    """
    stage = stage_chain = chain = None
    owned = {}
    attempted = []
    published = []
    residual = []
    code = None
    try:
        directory = _output_local(output_directory)
        if type(input_paths) not in (tuple, list):
            raise _OutputFailure("E_OUTPUT_PATH_INVALID")
        inputs = tuple(_output_local(path) for path in input_paths)
        parent_chain, existing = _output_prepare(directory, inputs)
        from ..result import SafeReportView
        from ..reports.json_report import render_json
        from ..reports.markdown_report import render_markdown

        if type(report) is not SafeReportView:
            raise _OutputFailure("E_OUTPUT_RENDER")
        try:
            rendered = (render_json(report), render_markdown(report))
            payloads = tuple(text.encode("utf-8") for text in rendered)
        except Exception:
            raise _OutputFailure("E_OUTPUT_RENDER") from None
        _output_recheck(parent_chain)
        if existing is None:
            try:
                directory.mkdir(mode=0o700)
            except FileExistsError:
                pass
        chain, info = _output_walk(directory)
        if not stat.S_ISDIR(info.st_mode) or (existing is not None and _output_identity(info) != _output_identity(existing)):
            raise _OutputFailure("E_OUTPUT_UNSAFE")
        for name in _OUTPUT_NAMES:
            if _output_info(directory / name) is not None:
                raise _OutputFailure("E_OUTPUT_EXISTS")
        _output_recheck(chain)
        stage = Path(tempfile.mkdtemp(prefix=".rit-stage-", dir=directory))
        stage_chain, stage_info = _output_walk(stage)
        if not stat.S_ISDIR(stage_info.st_mode):
            raise _OutputFailure("E_OUTPUT_UNSAFE")
        for name, payload in zip(_OUTPUT_NAMES, payloads):
            _output_recheck(stage_chain)
            _output_write(stage / name, payload, owned)
        for name in _OUTPUT_NAMES:
            _output_recheck(stage_chain)
            source = stage / name
            source_info = _output_info(source)
            if source_info is None or _output_is_link(source_info) or _output_fingerprint(source_info) != owned[name]:
                raise _OutputFailure("E_OUTPUT_UNSAFE")
            attempted.append(name)
            _output_publish_one(source, directory / name)
            published.append(name)
        _output_recheck(chain)
        for name in _OUTPUT_NAMES:
            info = _output_info(directory / name)
            if info is None or _output_is_link(info) or _output_fingerprint(info) != owned[name]:
                raise _OutputFailure("E_OUTPUT_UNSAFE")
    except _OutputFailure as error:
        code = error.code
    except FileExistsError:
        code = "E_OUTPUT_EXISTS"
    except (OSError, ValueError):
        code = "E_OUTPUT_IO"
    except Exception:
        code = "E_OUTPUT_INTERNAL"
    finally:
        if code is not None and chain is not None:
            residual = _output_rollback(directory, chain, owned, attempted, published)
        cleaned = _output_clean_stage(stage, stage_chain, owned)
    if not cleaned and code is None:
        code = "E_OUTPUT_CLEANUP"
        residual = list(_OUTPUT_NAMES)
    if code is None:
        try:
            _output_recheck(chain)
            for name in _OUTPUT_NAMES:
                info = _output_info(directory / name)
                if info is None or _output_is_link(info) or _output_fingerprint(info) != owned[name]:
                    raise _OutputFailure("E_OUTPUT_UNSAFE")
        except Exception:
            code = "E_OUTPUT_UNSAFE"
            residual = _output_rollback(directory, chain, owned, attempted, published)
    if code is None:
        return PublicationResult("complete", None, 0, tuple(published))
    status = "incomplete" if residual or not cleaned else "failed"
    return PublicationResult(status, code, _OUTPUT_CODES[code], tuple(published), tuple(residual), cleaned)
