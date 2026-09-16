"""Recognize explicit local input-file paths without fetching remote resources.

Owner IDs:
    PR-017, PR-002 supporting file inventory.

Inputs:
    An explicit path string or pathlib Path for an audit-bundle source file.

Outputs:
    A normalized local Path, without opening the file.

Assumptions:
    Explicit source-file paths may be absolute. Record content references use
    a separate base-directory policy to be implemented in Step 7.

Limits:
    No content-reference traversal, remote filesystem client, environment or
    tilde expansion, data loading, directory creation, or analytical behavior.
    Local operating-system mounts remain the user's responsibility.

Current phase status:
    Phase 2 Step 2 lexical local-input boundary. No analytical behavior.
"""

from __future__ import annotations

import os
import re
from pathlib import Path

from ..errors import ErrorCode, InputError


_SCHEME = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
_DRIVE_ABSOLUTE = re.compile(r"^[A-Za-z]:[\\/]")


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
