# Data Schema

Status: Phase 1 structural contract.

Canonical field meanings are controlled by `DATA_AND_PROVENANCE_SPEC.md` and `DEFINITIONS_AND_UNITS.md`.

The hero files under `examples/hero/` are format fixtures. Phase 1 checks names, types, JSON syntax, and composite parent-reference form without calculating metrics.

## Phase 2 Step 2: physical ingestion

`io.loaders.load_table(InputSource(...), limits=ResourceLimits(...))` now parses
local records, comparison, and provenance tables. `inventory_source` inventories
a declared file without parsing it; its row count is `None` and its field list
is empty. A parsed `LoadedTable` supplies row count, field order, file role,
byte size, exact SHA-256, unmapped values, and physical row/line locations.
These objects are internal input contracts, not final audit reports.

CSV/JSONL use the standard library so parsing does not adopt pandas' default
missing-value or identifier coercions. pandas remains an approved dependency
for later tabular operations. CSV strings and raw record spelling are retained,
including quoted empty strings and embedded newlines. JSONL native values,
missing keys, explicit null, and literal `unknown` remain distinct. The loader
never validates canonical record IDs, joins provenance, maps fields, resolves
parent links, opens paths found in content, or computes an analytical metric.

CSV has a required nonempty unique header and consistent row width. Blank
physical lines are ignored outside quoted fields. Malformed quotes, duplicate
JSON keys, non-object JSONL lines, nonfinite JSON numbers (including overflow),
and invalid UTF-8 fail with content-safe errors. Empty primary/comparison tables
fail; an empty provenance table remains a zero-row input for later validation.
An empty content cell or duplicate record key is preserved here for canonical
validation in a later step. The loader does not certify these records as valid.

Explicit format declarations select one parser and may override an extension
when parsing succeeds, as specified in `DATA_AND_PROVENANCE_SPEC.md` section
3.7. There is no fallback sniffing. A format incompatible with the declared file
role, or bytes rejected by the selected parser, fails. JSON/TOML control files
and NPY embedding files can be inventoried; they are not executed or interpreted
by the table loader. Snapshot hashing and parsing use the same bytes.

Only `max_file_bytes`, `max_rows`, and `max_json_depth` are enforced in this step.
No default universal size threshold is invented. Limits on content references,
parent lists, and later capabilities remain deferred. File size limits cover
compressed input bytes, not arbitrary decompression memory. File changes detected
during reading fail rather than attaching an inconsistent hash to parsed data.

Explicit local source-file paths may be absolute. URI, UNC, device, and invalid
paths are rejected before opening. Record-content path containment and symlink
policy belong to Step 7 and are not claimed here. OS-mounted filesystems are
outside this lexical path check. No source file is written or modified.

### Optional Parquet verification

The optional backend imports `pyarrow` only inside the Parquet read function and
passes a byte buffer to `ParquetFile`; it never asks Arrow to resolve a path or
remote filesystem. No core runtime or test dependency has been changed.

Core tests verify CSV/JSONL with PyArrow actively blocked and verify the clear
missing-extra error. Real Parquet tests require explicit selection after the
extra is installed. They fail if selected without it, rather than skipping or
substituting a fake reader:

```bash
python -m pip install ".[parquet,test]"
RIT_TEST_PARQUET=1 python -m pytest -p no:cacheprovider -q
```

On PowerShell, set `$env:RIT_TEST_PARQUET = "1"` before the pytest command.
The current workflows retain their approved dependency sets; optional-presence
coverage must be reported separately from core CI coverage.
