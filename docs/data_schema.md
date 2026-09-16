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

## Phase 2 Step 3: declarative field mapping

`io.schema_mapping.load_mapping(path)` reads an explicit local JSON mapping
snapshot. `compile_mapping(document)` validates a supplied plain dictionary;
`parse_mapping_json(text)` additionally detects duplicate object keys before
JSON decoding can discard them. `map_row(row, plan, section="records")` applies
the frozen declaration to a plain dictionary or an existing `RawRow`. No CLI
audit command, canonical validation, table join, or analysis is added.

The canonical version key is `schema_version: "1.0"`, from the approved data
specification section 14.2. The Phase 1 skeleton used `mapping_version`; that
spelling remains an explicit compatibility option. Exactly one version key is
required. A document needs a `records` or `provenance` section with `fields`.
Every target has one selector: `source`, `constant`, or an initial `constant`
or `coalesce` operation. Two selectors for one target are rejected. Duplicate
JSON target keys are errors. All operation-specific parameters are closed.

The following are the Step 3 parameter conventions for the approved verbs:

| Operation | Explicit parameters and behavior |
|---|---|
| `rename` | The enclosing `fields` key names the target and `source` names the original field. The operation has no additional parameter. |
| `trim` | Removes leading and trailing Unicode whitespace only when listed. |
| `cast_string` | Strings or finite scalar numbers/booleans; booleans become `true` or `false`. Arrays and objects are rejected. |
| `cast_integer` | Integer values or ASCII integer strings with optional sign. Booleans, floats, surrounding whitespace and fractional strings are rejected. |
| `cast_float` | Finite numeric values or explicit decimal/exponent strings. No booleans, nonfinite values, underscores or implicit trim. |
| `cast_boolean` | Requires `mapping`, an exact string-token to boolean dictionary. No implicit truthiness, trimming or case conversion. |
| `parse_datetime` | Requires `format: "iso8601"` or a portable numeric strptime format using `%Y`, `%y`, `%m`, `%d`, `%H`, `%M`, `%S`, `%f`, `%z`, `%j`, `%%`. Locale-dependent directives are rejected. Missing timezones are not inferred. |
| `parse_json_list` | Parses a strict JSON array string; objects, scalars, duplicate nested keys and nonfinite numbers fail. |
| `constant` | Requires `value` when used as an operation. Field-level `constant` is also supported. |
| `coalesce` | Requires a nonempty `sources` list. Selects the first present, non-null value from the original row. |
| `map_values` | Requires `mapping` and `unmapped: keep`, `null` or `error`. String keys match exactly; other input types are not converted to token strings. |
| `normalize_whitespace` | Requires `format: "collapse"`. Replaces Unicode whitespace runs with one space; boundary spaces are retained unless `trim` is separately listed. |
| `lowercase`, `uppercase` | Explicit string case conversion; no automatic Unicode normalization. |

All selectors read the original row. Fields cannot refer to previously generated
targets. Operations execute in listed order. An absent required `source` raises
`E_MAPPING_SOURCE_FIELD_MISSING`; optional coalesce sources may be absent.
When all coalesce sources are absent, the target remains absent. When at least
one is explicitly null and no value is available, the target is null. Zero,
false, empty strings, empty arrays/objects and the literal `unknown` are not
missing. Ordinary transforms preserve explicit nulls. CSV null-token and
quoted-empty semantics remain available in the original `RawRow` for Step 4;
this step does not guess them from decoded empty strings.

`MappedRow.extras` is empty by default. The explicit `preserve_extras=True`
argument preserves unused source fields in a separate namespace. Unmapped
field names are always recorded. Payloads are copied; source rows and plans are
not mutated. This remains mapping output, not certified canonical records.

Each result retains original row/line locations, source/unmapped field names,
selector and operation order for each target, a mapping snapshot SHA-256, and
any `W_MAPPING_VALUE_UNMAPPED` notices for the explicit keep/null policy.
The frozen plan retains the full declaration without printing its values in
`repr`. A loaded plan also retains the original mapping-file inventory and
byte hash. These are internal metadata for later assembly, not an audit report.

No dependency was added. The mapper uses fixed local branches, accepts plain
finite data, and never resolves dotted fields, paths, URLs, templates, environment
variables or callable objects. Unsafe syntax raises `E_MAPPING_UNSAFE_TRANSFORM`.
Strings that resemble code remain inert data when used as literal values.

## Phase 2 Step 4: canonical row fields and identity

`io.normalization.normalize_row(row, kind="records")` and its `provenance` form
accept already supplied fields. `normalize_table(loaded_table)` accepts the
existing `LoadedTable`, performs row-local normalization and same-kind identity
uniqueness checks, and returns lexically ordered rows. It never loads a file,
executes mapping, joins tables, resolves parents, or classifies observability.
Required table columns are checked even for a zero-row provenance table; a
header-only table with the required columns remains an empty supplied table.

The implementation follows the record/provenance fields in sections 8 and 9
and field-specific normalization rules in section 15 of the data specification.
Identity is exactly `(dataset_version, record_id)`: no trim, case conversion,
Unicode normalization, numeric coercion, or content deduplication is implicit.
Duplicate keys fail, even for identical physical rows. Repeated IDs in different
versions remain different keys. `validate_unique_keys` can validate a caller's
explicit combined same-kind scope across files, without a provenance join.

CSV conversion requires `file_format=FileFormat.CSV` and original `RawRow`
spelling. It distinguishes unquoted blank/null tokens from quoted empty or
literal strings. `null` and `NULL` are the default unquoted tokens. Required
empty fields fail; blank optional IDs/numbers/booleans become null; a blank CSV
parent list becomes an empty sequence. Native JSONL/Parquet values do not acquire
CSV token semantics. Native `unknown`, false, zero, null and absent fields remain
distinct. String identifiers, categories and notes are never inferred.

For an existing mapped CSV row, supply `source_row=original_raw_row`. Unchanged
source selectors inherit quoting evidence; explicit transforms/constants use
their returned values without fabricating original quote states. CSV numeric
and boolean serialization still follows the target field's type. A plain typed
mapping result can instead use the default native mode. This step does not
change the previously approved mapper's coalesce or null behavior.

`NormalizationOptions` supplies explicit in-memory policies for content mode,
null tokens, optional blank-as-null behavior, boolean compatibility tokens, and
extras preservation. No additional JSON/TOML run-config keys or CLI commands
have been introduced. Compatibility boolean tokens require explicit opt-in.
Source type, external grounding and human review never overwrite one another.

Finite, nonnegative weights are checked per row. Generation is nullable,
nonnegative and integer-only; no expected generation or lineage depth is
computed. Timestamps require an explicit timezone and normalize to UTC.
Native standard-library timezone/ZoneInfo datetimes and ISO 8601 strings are
supported; no local timezone is guessed. An inline content byte limit can be
provided. Local-reference strings are never opened or certified as safe here;
complete content-reference validation remains Step 7.

`CanonicalRow.values`, `field_states` and `extras` are detached read-only
mappings. Parent arrays are immutable tuples internally, sorted for presentation
without deduplication or reference resolution. An omitted or explicit-null
parent declaration stays null, with its original absence/null state retained.
It never becomes proof of parentlessness, external grounding or independence.
The existing export-row schema still requires an array; these nullable internal
rows are not advertised as export-ready and no exporter exists in this step.

Optional fields stay absent unless supplied, apart from the documented
`text/plain` content-type default and minimum nullable parent column. Defaults
are marked separately from source-supplied fields. Extras stay separate and are
empty unless explicitly preserved. Normalized payloads and private notes do not
appear in default repr or error messages. Errors include field, role, original
row/line, and key where valid; they never echo the rejected value.

Lexical row order is a deterministic presentation convention. In particular,
`v10` can precede `v2`; this does not supply version chronology. Observability,
provenance joins/coverage, parent resolution, generation consistency, metrics,
reports and simulation remain outside Step 4. The normalized manifest schema
adds field types/enums and identifier constraints only, without cross-row logic.
