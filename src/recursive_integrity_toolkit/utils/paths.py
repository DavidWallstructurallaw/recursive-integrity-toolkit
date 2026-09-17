"""Validate explicit input paths and contained local content references.

Owner IDs:
    PR-017, PR-002 supporting file inventory.

Inputs:
    Explicit local input paths or content-reference text with an approved base.

Outputs:
    Normalized input paths or checked, symlink-resolved local content paths.

Assumptions:
    The configured base and its directory tree are trusted and stable during a
    read. An omitted base uses the directory containing the declared records file.

Limits:
    No network, environment expansion, content analysis, file writes, or report.
    OS mounts and hostile concurrent directory replacement are not sandboxed.
    Content reads must use the dedicated loader, not a later unchecked path open.

Current phase status:
    Phase 2 Step 7 local content-reference security. No analytical behavior.
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
