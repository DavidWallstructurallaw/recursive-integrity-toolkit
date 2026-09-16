"""Hash an explicitly supplied file-byte snapshot for input inventory.

Owner IDs:
    PR-016; PR-002 supporting input identity; PR-006 and PR-015 remain deferred.

Inputs:
    Bytes already read by the local file loader.

Outputs:
    Lowercase SHA-256 hexadecimal digest of exactly those bytes.

Assumptions:
    The caller uses the same snapshot for parsing and inventory.

Limits:
    No file access, content normalization, duplicate detection, ID redaction,
    provenance inference, or analytical calculation.

Current phase status:
    Phase 2 Step 2 file hashing only. No analytical behavior.
"""

from __future__ import annotations

import hashlib


def sha256_bytes(data: bytes) -> str:
    """Return the SHA-256 of bytes without decoding or normalizing them."""
    if not isinstance(data, bytes):
        raise TypeError("file snapshot must be bytes")
    return hashlib.sha256(data).hexdigest()
