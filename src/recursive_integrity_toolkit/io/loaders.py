"""Read local physical tables and explicit contained UTF-8 content files.

Owner IDs:
    PR-002; PR-017 local paths and content references; PR-016 file-hash support.

Inputs:
    Explicit InputSource declarations, content references and ResourceLimits.

Outputs:
    FileInventoryEntry, LoadedTable or explicitly requested local text.

Assumptions:
    CSV and JSONL are UTF-8. A declared format overrides the extension only
    when that parser succeeds. Parquet is optional and loaded lazily.
    Content reference directories are trusted and stable during a read.

Limits:
    No schema mapping, canonical coercion, joins, record-key validation,
    observability, metric, graph, or report. Table parsing never opens content.
    File-byte limits bound the snapshot, not arbitrary decompression memory.
    A successful parse establishes physical format only.

Current phase status:
    Phase 2 Step 7 explicit local content loading. No analytical behavior.
"""

from __future__ import annotations

import csv
import io
import math
import os
import stat
from pathlib import Path
from threading import Lock

import json

from ..config import ResourceLimits
from ..errors import ConfigurationError, ErrorCode, IngestionError, InputError
from ..models import FileFormat, FileInventoryEntry, FileRole, InputSource, LoadedTable, RawRow
from ..utils.hashing import sha256_bytes
from ..utils.paths import local_input_path


_TABLE_ROLES = {FileRole.RECORDS_PRIMARY, FileRole.RECORDS_COMPARE, FileRole.PROVENANCE_MANIFEST}
_TABLE_FORMATS = {FileFormat.CSV, FileFormat.JSONL, FileFormat.PARQUET}
_EXTENSIONS = {".csv": FileFormat.CSV, ".jsonl": FileFormat.JSONL, ".parquet": FileFormat.PARQUET,
               ".json": FileFormat.JSON, ".toml": FileFormat.TOML, ".npy": FileFormat.NPY}
_CSV_LOCK = Lock()


def _failure(source: InputSource, code: ErrorCode, message: str, **location) -> IngestionError:
    return IngestionError(code, message, file_role=source.role.value,
                          file_path=str(source.path), **location)


def _limits(limits: ResourceLimits | None) -> ResourceLimits:
    result = ResourceLimits() if limits is None else limits
    if not isinstance(result, ResourceLimits):
        raise ConfigurationError(ErrorCode.CONFIG_INVALID, "limits must use ResourceLimits")
    for name in ("max_file_bytes", "max_rows", "max_json_depth"):
        value = getattr(result, name)
        if value is not None and (isinstance(value, bool) or not isinstance(value, int) or value <= 0):
            raise ConfigurationError(ErrorCode.CONFIG_INVALID, f"{name} must be a positive integer")
    return result


def _select_format(source: InputSource) -> FileFormat:
    if not isinstance(source, InputSource) or not isinstance(source.role, FileRole):
        raise ConfigurationError(ErrorCode.CONFIG_INVALID, "source must declare an approved file role")
    path = local_input_path(source.path)
    chosen = source.declared_format
    if chosen is None:
        chosen = _EXTENSIONS.get(path.suffix.lower())
    if not isinstance(chosen, FileFormat):
        raise _failure(source, ErrorCode.FILE_FORMAT_UNSUPPORTED, "declare a supported input format")
    allowed = {
        FileRole.RECORDS_PRIMARY: _TABLE_FORMATS,
        FileRole.RECORDS_COMPARE: _TABLE_FORMATS,
        FileRole.PROVENANCE_MANIFEST: _TABLE_FORMATS,
        FileRole.SCHEMA_MAPPING: {FileFormat.JSON},
        FileRole.CONFIG: {FileFormat.JSON, FileFormat.TOML},
        FileRole.VERSION_ORDER: {FileFormat.JSON},
        FileRole.EMBEDDING_DATA: {FileFormat.CSV, FileFormat.PARQUET, FileFormat.NPY},
        FileRole.EXTERNAL_REFERENCE: {FileFormat.JSON},
    }
    if chosen not in allowed[source.role]:
        raise _failure(source, ErrorCode.FILE_FORMAT_UNSUPPORTED, "declared format conflicts with file role")
    return chosen


def _read_source(source: InputSource, limits: ResourceLimits) -> tuple[Path, bytes]:
    try:
        path = local_input_path(source.path)
        initial = path.stat()
        if not stat.S_ISREG(initial.st_mode):
            raise _failure(source, ErrorCode.FILE_PARSE, "input must be a regular file")
        if limits.max_file_bytes is not None and initial.st_size > limits.max_file_bytes:
            raise _failure(source, ErrorCode.FILE_PARSE, "configured max_file_bytes exceeded")
        # Nonblocking open avoids hanging if a regular path is replaced by a FIFO.
        flags = os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_NONBLOCK", 0)
        fd = os.open(path, flags)
        with os.fdopen(fd, "rb") as stream:
            opened = os.fstat(stream.fileno())
            if not stat.S_ISREG(opened.st_mode):
                raise _failure(source, ErrorCode.FILE_PARSE, "input must remain a regular file")
            chunks: list[bytes] = []
            total = 0
            while True:
                size = 65536
                if limits.max_file_bytes is not None:
                    size = min(size, limits.max_file_bytes - total + 1)
                chunk = stream.read(size)
                if not chunk:
                    break
                total += len(chunk)
                if limits.max_file_bytes is not None and total > limits.max_file_bytes:
                    raise _failure(source, ErrorCode.FILE_PARSE, "configured max_file_bytes exceeded")
                chunks.append(chunk)
            final = os.fstat(stream.fileno())
            if total != opened.st_size or (final.st_size, final.st_mtime_ns) != (opened.st_size, opened.st_mtime_ns):
                raise _failure(source, ErrorCode.FILE_PARSE, "input changed while reading; retry with a stable file")
        return path, b"".join(chunks)
    except IngestionError:
        raise
    except InputError as exc:
        raise _failure(source, exc.code, exc.safe_message) from None
    except FileNotFoundError:
        raise _failure(source, ErrorCode.FILE_NOT_FOUND, "input file not found; check the declared local path") from None
    except (OSError, ValueError):
        raise _failure(source, ErrorCode.FILE_PARSE, "local input cannot be read") from None


def inventory_source(source: InputSource, *, limits: ResourceLimits | None = None) -> FileInventoryEntry:
    """Inventory bytes only; row count and schema fields require load_table."""
    checked = _limits(limits)
    chosen = _select_format(source)
    path, raw = _read_source(source, checked)
    return FileInventoryEntry(source.role, path, chosen, len(raw), sha256_bytes(raw))


def _text(source: InputSource, raw: bytes) -> str:
    try:
        result = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise _failure(source, ErrorCode.FILE_ENCODING, "input must use valid UTF-8; resave the file as UTF-8",
                       byte_offset=exc.start) from None
    return result[1:] if result.startswith("\ufeff") else result


def _row_limit(source: InputSource, count: int, limits: ResourceLimits, line: int | None = None) -> None:
    if limits.max_rows is not None and count > limits.max_rows:
        raise _failure(source, ErrorCode.FILE_PARSE, "configured max_rows exceeded",
                       row_number=count, line_number=line)


def _headers(source: InputSource, names: list[str], line: int | None = None) -> None:
    if not names or any(not name for name in names):
        raise _failure(source, ErrorCode.FILE_PARSE, "column names must be nonempty", line_number=line)
    if len(set(names)) != len(names):
        raise _failure(source, ErrorCode.FILE_PARSE, "duplicate column names are not allowed", line_number=line)


def _check_csv_quotes(spelling: str) -> None:
    """Reject bare-field quotes that csv.reader otherwise accepts literally."""
    state = "start"
    for character in spelling:
        if state == "quoted":
            if character == '"':
                state = "closed"
        elif state == "closed":
            if character == '"':
                state = "quoted"
            elif character == ",":
                state = "start"
            elif character not in "\r\n":
                raise csv.Error("invalid character after closing quote")
        elif character == ",":
            state = "start"
        elif character == '"':
            if state != "start":
                raise csv.Error("quote inside unquoted field")
            state = "quoted"
        elif character not in "\r\n":
            state = "bare"
    if state == "quoted":
        raise csv.Error("unterminated quoted field")


def _parse_csv(source: InputSource, text: str, limits: ResourceLimits) -> tuple[tuple[str, ...], tuple[RawRow, ...]]:
    stream = io.StringIO(text, newline="")
    reader = csv.reader(stream, strict=True)
    header: list[str] | None = None
    rows: list[RawRow] = []
    # csv.field_size_limit is process-global; restore it even on a parse failure.
    # The snapshot has already passed max_file_bytes, so no hidden 128 KiB cap is added.
    with _CSV_LOCK:
        previous = csv.field_size_limit()
        csv.field_size_limit(max(previous, len(text)))
        try:
            while True:
                start = stream.tell()
                line = reader.line_num + 1
                try:
                    values = next(reader)
                except StopIteration:
                    break
                spelling = text[start:stream.tell()]
                if not values or not spelling.strip():
                    continue
                _check_csv_quotes(spelling)
                if header is None:
                    _headers(source, values, line)
                    header = values
                    continue
                if len(values) != len(header):
                    raise _failure(source, ErrorCode.FILE_PARSE, "CSV row width differs from header",
                                   row_number=len(rows) + 1, line_number=line)
                _row_limit(source, len(rows) + 1, limits, line)
                rows.append(RawRow(dict(zip(header, values)), len(rows) + 1, line, spelling))
        except csv.Error:
            raise _failure(source, ErrorCode.FILE_PARSE, "malformed CSV; check quoting and delimiters",
                           row_number=len(rows) + 1, line_number=reader.line_num) from None
        finally:
            csv.field_size_limit(previous)
    return tuple(header or ()), tuple(rows)


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def _reject_constant(value: str) -> None:
    raise ValueError("nonfinite JSON number")


def _finite_float(value: str) -> float:
    result = float(value)
    if not math.isfinite(result):
        raise ValueError("nonfinite JSON number")
    return result


def _check_depth(text: str, maximum: int | None) -> None:
    if maximum is None:
        return
    depth = 0
    quoted = False
    escaped = False
    for character in text:
        if quoted:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                quoted = False
        elif character == '"':
            quoted = True
        elif character in "[{":
            depth += 1
            if depth > maximum:
                raise ValueError("configured max_json_depth exceeded")
        elif character in "]}":
            depth -= 1


def _parse_jsonl(source: InputSource, text: str, limits: ResourceLimits) -> tuple[tuple[str, ...], tuple[RawRow, ...]]:
    rows: list[RawRow] = []
    fields: dict[str, None] = {}
    for line, spelling in enumerate(io.StringIO(text, newline=""), start=1):
        if not spelling.strip():
            continue
        _row_limit(source, len(rows) + 1, limits, line)
        try:
            _check_depth(spelling, limits.max_json_depth)
            value = json.loads(spelling, object_pairs_hook=_unique_object,
                               parse_constant=_reject_constant, parse_float=_finite_float)
            if not isinstance(value, dict):
                raise ValueError("JSONL root must be an object")
        except (ValueError, RecursionError):
            raise _failure(source, ErrorCode.FILE_PARSE,
                           "invalid JSONL object, duplicate key, nonfinite number, or exceeded JSON depth limit",
                           row_number=len(rows) + 1, line_number=line) from None
        fields.update(dict.fromkeys(value))
        rows.append(RawRow(value, len(rows) + 1, line, spelling))
    return tuple(fields), tuple(rows)


def _parse_parquet(source: InputSource, raw: bytes, limits: ResourceLimits) -> tuple[tuple[str, ...], tuple[RawRow, ...]]:
    try:
        import pyarrow as pa
        import pyarrow.parquet as pq
    except ImportError:
        raise _failure(source, ErrorCode.FILE_FORMAT_UNSUPPORTED,
                       'Parquet requires the optional extra: install "recursive-integrity-toolkit[parquet]"') from None
    try:
        with pa.BufferReader(raw) as buffer:
            parquet = pq.ParquetFile(buffer)
            names = parquet.schema_arrow.names
            _headers(source, names)
            _row_limit(source, parquet.metadata.num_rows, limits)
            rows: list[RawRow] = []
            for batch in parquet.iter_batches(batch_size=1024, use_threads=False):
                for values in batch.to_pylist():
                    _row_limit(source, len(rows) + 1, limits)
                    rows.append(RawRow(values, len(rows) + 1))
    except IngestionError:
        raise
    except (pa.ArrowException, OSError, ValueError, TypeError):
        raise _failure(source, ErrorCode.FILE_PARSE, "invalid or unsupported local Parquet file") from None
    return tuple(names), tuple(rows)


def load_table(source: InputSource, *, limits: ResourceLimits | None = None) -> LoadedTable:
    """Parse a records/compare/provenance table; canonical validation is later.

    A declared format selects exactly one parser. No fallback sniffing occurs.
    CSV values stay strings. JSONL and Parquet retain their native values.
    Hash and parser consume the same byte snapshot. No record content is opened.
    """
    checked = _limits(limits)
    chosen = _select_format(source)
    if source.role not in _TABLE_ROLES:
        raise _failure(source, ErrorCode.FILE_FORMAT_UNSUPPORTED, "table loading requires a records or provenance role")
    path, raw = _read_source(source, checked)
    if chosen is FileFormat.CSV:
        fields, rows = _parse_csv(source, _text(source, raw), checked)
    elif chosen is FileFormat.JSONL:
        fields, rows = _parse_jsonl(source, _text(source, raw), checked)
    else:
        fields, rows = _parse_parquet(source, raw, checked)
    if not rows and source.role in {FileRole.RECORDS_PRIMARY, FileRole.RECORDS_COMPARE}:
        raise _failure(source, ErrorCode.EMPTY_DATASET, "records table contains no data rows")
    inventory = FileInventoryEntry(source.role, path, chosen, len(raw), sha256_bytes(raw), len(rows), fields)
    return LoadedTable(inventory, rows)


def load_content_reference(reference: str, *, base_directory: str | Path | None = None,
                           records_path: str | Path | None = None, allow_absolute: bool = False,
                           limits: ResourceLimits | None = None, location=None) -> str:
    """Explicitly read one contained, regular UTF-8 text file under PR-017.

    No table loader or normalizer calls this automatically. The returned text
    belongs to the caller; no content, path, or notes are logged or reported.
    A failure leaves caller-owned records/provenance intact. Total-bundle load
    budgeting and capability classification belong to later orchestration.
    """
    from ..errors import CanonicalValidationError
    from ..models import RowLocation
    from ..utils.paths import _content_base, _open_content_fd, resolve_content_reference

    loc = RowLocation() if location is None else location
    if type(loc) is not RowLocation or (loc.file_role is not None and type(loc.file_role) is not FileRole):
        raise CanonicalValidationError(ErrorCode.CONFIG_INVALID, "content location must use the approved types")
    for number in (loc.row_number, loc.line_number):
        if number is not None and (type(number) is not int or number < 1):
            raise CanonicalValidationError(ErrorCode.CONFIG_INVALID, "content location numbers must be positive integers")
    maximum = None
    if limits is not None:
        if type(limits) is not ResourceLimits:
            raise CanonicalValidationError(ErrorCode.CONFIG_INVALID, "content limits must use ResourceLimits")
        maximum = limits.max_content_bytes
        if maximum is not None and (type(maximum) is not int or maximum <= 0):
            raise CanonicalValidationError(ErrorCode.CONFIG_INVALID, "max_content_bytes must be a positive integer")
    try:
        path = resolve_content_reference(reference, base_directory=base_directory,
                                         records_path=records_path, allow_absolute=allow_absolute)
        base = _content_base(base_directory, records_path)
        before = path.lstat()
        if maximum is not None and before.st_size > maximum:
            raise CanonicalValidationError(ErrorCode.FILE_PARSE, "content exceeds max_content_bytes")
        fd = _open_content_fd(path, base)
        try:
            opened = os.fstat(fd)
            again = resolve_content_reference(reference, base_directory=base, allow_absolute=allow_absolute)
            checked = again.lstat()
            if (again != path or not stat.S_ISREG(opened.st_mode)
                    or (before.st_dev, before.st_ino) != (opened.st_dev, opened.st_ino)
                    or (checked.st_dev, checked.st_ino) != (opened.st_dev, opened.st_ino)):
                raise CanonicalValidationError(ErrorCode.FILE_PARSE, "content path changed before reading")
            chunks = []
            total = 0
            while True:
                amount = 65536 if maximum is None else min(65536, maximum - total + 1)
                chunk = os.read(fd, amount)
                if not chunk:
                    break
                total += len(chunk)
                if maximum is not None and total > maximum:
                    raise CanonicalValidationError(ErrorCode.FILE_PARSE, "content exceeds max_content_bytes")
                chunks.append(chunk)
            after = os.fstat(fd)
            if (total != opened.st_size or (after.st_size, after.st_mtime_ns) != (opened.st_size, opened.st_mtime_ns)):
                raise CanonicalValidationError(ErrorCode.FILE_PARSE, "content file changed during reading")
        finally:
            os.close(fd)
        raw = b"".join(chunks)
        if b"\x00" in raw:
            raise CanonicalValidationError(ErrorCode.FILE_FORMAT_UNSUPPORTED, "NUL-bearing binary content is unsupported")
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            raise CanonicalValidationError(ErrorCode.FILE_ENCODING, "content file must use valid UTF-8") from None
        if not text.strip():
            raise CanonicalValidationError(ErrorCode.RECORD_EMPTY_CONTENT, "referenced text is empty or whitespace-only")
        return text
    except CanonicalValidationError as error:
        raise CanonicalValidationError(error.code, error.safe_message, field="content",
            file_role=loc.file_role.value if loc.file_role is not None else None,
            file_path="[redacted]", row_number=loc.row_number, line_number=loc.line_number) from None
    except FileNotFoundError:
        raise CanonicalValidationError(ErrorCode.CONTENT_REF_MISSING, "content disappeared before reading",
            field="content", file_path="[redacted]", row_number=loc.row_number, line_number=loc.line_number) from None
    except (OSError, ValueError, RuntimeError):
        raise CanonicalValidationError(ErrorCode.FILE_PARSE, "local content cannot be read safely",
            field="content", file_path="[redacted]", row_number=loc.row_number, line_number=loc.line_number) from None
