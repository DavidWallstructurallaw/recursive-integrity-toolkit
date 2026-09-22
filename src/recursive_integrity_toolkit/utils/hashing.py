"""Preserve input hashes and add scoped identifier and configuration protection.

Owner IDs:
    PR-016, PR-015; PR-002 supporting input identity; PR-006 remains deferred.

Inputs:
    Bytes already read by the local file loader; explicit finite JSON declarations;
    fresh or explicitly injected/local-file identifier secrets.

Outputs:
    Unchanged snapshot SHA-256; canonical configuration hashes; domain-separated
    HMAC-SHA-256 identifiers without a retained reversible mapping.

Assumptions:
    The caller uses the same snapshot for parsing and inventory.

Limits:
    Only an explicit secret-file factory reads a bounded checked local file.
    No secret emission, content normalization, duplicate detection, provenance
    inference, analytical calculation or statistical anonymity guarantee.

Current phase status:
    Phase 4 Step 4 additive privacy helpers; inherited byte hashing unchanged.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import math
import os
import secrets
import stat
from dataclasses import dataclass, field
from pathlib import Path

from ..errors import ConfigurationError, ErrorCode, ToolkitError
from .paths import _content_lexical, _open_content_fd, local_input_path


def sha256_bytes(data: bytes) -> str:
    """Return the SHA-256 of bytes without decoding or normalizing them."""
    if not isinstance(data, bytes):
        raise TypeError("file snapshot must be bytes")
    return hashlib.sha256(data).hexdigest()


def canonical_json_bytes(value: object) -> bytes:
    """Encode finite plain JSON data without coercing keys or joining identities.

    Object keys sort by Unicode code point; arrays retain order. Tuples denote
    JSON arrays. Number spelling follows the supported Python JSON encoder and
    distinguishes integers from floats. This is a versioned local encoding,
    not a claim of RFC 8785 interoperability.
    """
    def plain(item: object, active: set[int]) -> object:
        if item is None or type(item) in (str, bool, int):
            return item
        if type(item) is float and math.isfinite(item):
            return item
        if type(item) not in (dict, list, tuple) or id(item) in active:
            raise ValueError("canonical data must be finite acyclic plain JSON")
        active.add(id(item))
        try:
            if type(item) is dict:
                if any(type(key) is not str for key in item):
                    raise ValueError("canonical object keys must be strings")
                return {key: plain(item[key], active) for key in sorted(item)}
            return [plain(child, active) for child in item]
        finally:
            active.remove(id(item))

    try:
        return json.dumps(plain(value, set()), ensure_ascii=True, sort_keys=True,
                          separators=(",", ":"), allow_nan=False).encode("ascii")
    except (RecursionError, OverflowError, ValueError):
        raise ValueError("canonical data must be finite acyclic plain JSON") from None


def sha256_canonical(value: object) -> str:
    """Hash the documented canonical encoding, without implying authenticity."""
    return sha256_bytes(canonical_json_bytes(value))


def _phase4_secret_file(value: str | Path) -> bytes:
    """Read one explicit bounded regular local file through checked path helpers.

    Reject all symlink/reparse components. POSIX opens pinned directories with
    no-follow flags using the inherited content reader. Stable trusted directory
    trees remain required on other platforms; mounted filesystems are not an OS
    network sandbox. No secret path or underlying exception is propagated.
    """
    try:
        if not isinstance(value, (str, Path)):
            raise ValueError
        declared = _content_lexical(str(value), allow_absolute=True)
        path = local_input_path(declared)
        cursor = Path(path.anchor)
        for part in path.parts[1:]:
            cursor /= part
            info = cursor.lstat()
            if stat.S_ISLNK(info.st_mode) or getattr(info, "st_reparse_tag", 0):
                raise ValueError
            if cursor != path and not stat.S_ISDIR(info.st_mode):
                raise ValueError
        before = path.lstat()
        if not stat.S_ISREG(before.st_mode) or not 32 <= before.st_size <= 4096:
            raise ValueError
        descriptor = _open_content_fd(path, Path(path.anchor))
        try:
            opened = os.fstat(descriptor)
            if (opened.st_dev, opened.st_ino, opened.st_size) != (before.st_dev, before.st_ino, before.st_size):
                raise ValueError
            if not stat.S_ISREG(opened.st_mode):
                raise ValueError
            material = bytearray()
            while len(material) <= 4096:
                chunk = os.read(descriptor, 4097 - len(material))
                if not chunk:
                    break
                material.extend(chunk)
            if not 32 <= len(material) <= 4096 or len(material) != opened.st_size:
                raise ValueError
            return bytes(material)
        finally:
            os.close(descriptor)
    except (OSError, ValueError, RuntimeError, ToolkitError):
        raise ConfigurationError(ErrorCode.CONFIG_INVALID,
                                 "identifier secret must be a checked local regular file containing 32 to 4096 bytes") from None


@dataclass(frozen=True, slots=True, init=False, repr=False)
class IdentifierProtection:
    """Opaque identifier HMAC context; explicit inspection is not a sandbox.

    Fresh and injected in-memory keys declare run scope. Only an explicit local
    secret file declares cross-run scope. A fixed injected key supports tests,
    but does not make fresh-key production reports cross-run deterministic.
    """

    _secret: bytes = field(repr=False)
    stability_scope: str
    secret_source: str

    def __init__(self, *, secret: bytes | None = None, secret_file: str | Path | None = None) -> None:
        if secret is not None and secret_file is not None:
            raise ConfigurationError(ErrorCode.CONFIG_INVALID, "supply only one identifier secret source")
        if secret_file is not None:
            material, scope, source = _phase4_secret_file(secret_file), "cross_run", "local_file"
        elif secret is not None:
            material, scope, source = secret, "run", "injected"
        else:
            material, scope, source = secrets.token_bytes(32), "run", "fresh"
        if type(material) is not bytes or not 32 <= len(material) <= 4096:
            raise ConfigurationError(ErrorCode.CONFIG_INVALID, "identifier secret must contain 32 to 4096 bytes")
        object.__setattr__(self, "_secret", material)
        object.__setattr__(self, "stability_scope", scope)
        object.__setattr__(self, "secret_source", source)

    @classmethod
    def create(cls, *, secret: bytes | None = None, secret_file: str | Path | None = None) -> IdentifierProtection:
        """Create fresh run protection or explicitly supplied local protection."""
        return cls(secret=secret, secret_file=secret_file)

    @property
    def algorithm(self) -> str:
        return "HMAC-SHA-256"

    def pseudonym(self, domain: str, value: object) -> str:
        """HMAC a length-framed domain and canonical value, retaining no map."""
        if type(domain) is not str or not domain or len(domain) > 128 or any(
                character not in "abcdefghijklmnopqrstuvwxyz0123456789_.-" for character in domain):
            raise ValueError("identifier domain must be a nonempty bounded ASCII label")
        domain_bytes = domain.encode("ascii")
        payload = canonical_json_bytes(value)
        framed = (b"rit.identifier.v1\x00" + len(domain_bytes).to_bytes(4, "big") + domain_bytes
                  + len(payload).to_bytes(8, "big") + payload)
        return "hmac-sha256:" + hmac.new(self._secret, framed, hashlib.sha256).hexdigest()

    def __repr__(self) -> str:
        return (f"IdentifierProtection(algorithm={self.algorithm!r}, "
                f"stability_scope={self.stability_scope!r}, secret_source={self.secret_source!r})")
