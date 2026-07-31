# DATA_AND_PROVENANCE_SPEC

## Document control

| Field | Value |
|---|---|
| Project | Recursive Integrity Toolkit |
| Target release | v0.1 |
| Phase | Phase 0 |
| Status | APPROVED PHASE 0 BASELINE |
| Primary owner | Theory Owner |
| Technical reviewers | Technical Maintainer, Mathematical Reviewer, Security Reviewer |
| Depends on | `SPEC_AUDIT.md`, `THEORY_SOURCE_MAP.md`, `UNRESOLVED_DECISIONS.md`, `PROJECT_INSTRUCTIONS.md`, `V0.1_PRODUCT_SPEC.md`, `DEFINITIONS_AND_UNITS.md` |
| Purpose | Freeze accepted input bundles, canonical schemas, serialization rules, joins, lineage encoding, mapping behavior, validation rules, normalization behavior, and provenance uncertainty handling |

This file defines how Recursive Integrity Toolkit v0.1 receives, validates, normalizes, and interprets records, provenance, lineage, representations, versions, and optional auxiliary inputs.

The toolkit must preserve the difference between supplied evidence and inferred interpretation.

Unknown provenance remains unknown.

Missing parents remain unresolved.

A source type does not determine external grounding.

No schema mapping may execute arbitrary code.

No input format may silently change the meaning of a canonical field.

Definitions marked `APPROVED DECISION` become implementation-authoritative only after the corresponding `UD-*` entry is approved.

---

## 1. Scope of this specification

This specification controls:

- accepted input-file roles,
- accepted file formats,
- canonical field names,
- canonical value types,
- enum values,
- identifier rules,
- record-version identity,
- content handling,
- provenance joins,
- parent-reference encoding,
- lineage completeness,
- version ordering,
- schema mapping,
- normalization,
- validation,
- warning and error behavior,
- redaction-sensitive fields,
- normalized manifest export,
- hero fixture data layout.

This specification does not define:

- mathematical metric formulas beyond data requirements,
- report section order,
- public report rendering,
- theory interpretation,
- release governance,
- software-module structure.

Those belong in the corresponding controlling files.

---

## 2. Input bundle model

### 2.1 Audit bundle

An `audit_bundle` is the complete set of inputs supplied to one toolkit run.

A bundle may contain:

- one primary records source,
- zero or more comparison records sources,
- zero or one provenance manifest source,
- zero or one schema mapping source,
- zero or one configuration source,
- zero or one explicit version-order source,
- zero or one embedding source per declared representation,
- zero or one external reference distribution per scenario,
- zero or more local content files referenced by records.

### 2.2 Minimum valid bundle

The minimum valid bundle contains:

- one readable records file,
- required canonical records fields after mapping,
- at least one valid record.

A minimum bundle supports Level 0 and may support Level 1 depending on available content or representation fields.

### 2.3 Bundle roles

| Role | Required | Cardinality | Purpose |
|---|---:|---:|---|
| `records_primary` | yes | exactly 1 | Primary dataset version or multi-version records source |
| `records_compare` | no | 0 or more | Additional ordered dataset versions |
| `provenance_manifest` | no | 0 or 1 | Source, grounding, transformation, and parent metadata |
| `schema_mapping` | no | 0 or 1 | Declarative mapping to canonical schema |
| `config` | no | 0 or 1 | Run behavior and representation settings |
| `version_order` | no | 0 or 1 | Explicit ordering of dataset versions |
| `embedding_data` | no | 0 or more | User-supplied vectors, bins, or clusters |
| `external_reference` | no | 0 or more | User-supplied scenario reference distributions |

### 2.4 One run, one normalized record table

All records supplied to one run must normalize into one logical record table keyed by:

```text
(dataset_version, record_id)
```

Physical file boundaries do not change canonical record identity.

### 2.5 One run, one normalized provenance table

All provenance rows supplied to one run must normalize into one logical provenance table keyed by:

```text
(dataset_version, record_id)
```

v0.1 accepts one provenance-manifest input argument. That file may contain rows for multiple dataset versions.

---

## 3. Accepted file formats

### 3.1 Records files

Required support:

- CSV
- JSONL

Optional support:

- Parquet through an optional dependency

### 3.2 Provenance manifest

Required support:

- CSV
- JSONL

Optional support:

- Parquet through an optional dependency

### 3.3 Schema mapping

Required support:

- JSON

Optional future support:

- TOML
- YAML

YAML is not required for v0.1 because it would add a parser dependency and additional type-coercion ambiguity.

### 3.4 Run configuration

Recommended required support:

- JSON
- TOML using Python 3.11 standard-library parsing

### 3.5 Version order

Supported forms:

- embedded in config,
- standalone JSON,
- CLI order supplied by the user.

### 3.6 Embedding data

Recommended forms:

- Parquet,
- NumPy `.npy` with a separate record-key index,
- CSV only for small fixtures.

Exact embedding support remains optional in v0.1.

### 3.7 File extension and declared format

The toolkit should infer format from the file extension when unambiguous.

Users may explicitly declare a format.

A declared format overrides extension inference only when parsing succeeds.

Unsupported or conflicting format declarations produce an error.

---

## 4. Text and character encoding

### 4.1 Required encoding

CSV, JSONL, JSON, and TOML text inputs must use UTF-8.

UTF-8 with a byte-order mark may be accepted and normalized.

Other encodings are unsupported unless a future approved mapping layer adds explicit decoding configuration.

### 4.2 Newlines

Accepted newline forms:

- LF
- CRLF

Newline normalization must not change content strings after parsing.

### 4.3 Unicode normalization

Canonical identifier fields must not be silently Unicode-normalized in v0.1.

Content normalization for exact duplicate analysis may use a separately declared normalization profile.

### 4.4 Invalid byte sequences

Invalid UTF-8 produces a fatal input error.

The error must identify:

- file,
- byte region where available,
- encoding expectation,
- remediation guidance.

Raw content must not be printed.

---

## 5. CSV serialization rules

### 5.1 General CSV profile

Recommended canonical CSV profile:

| Property | Value |
|---|---|
| delimiter | comma |
| quote character | double quote |
| escape behavior | RFC 4180 compatible |
| header | required |
| encoding | UTF-8 |
| blank lines | ignored outside quoted fields |
| duplicate headers | error |
| empty header | error |

### 5.2 CSV null handling

Canonical input null forms:

- empty unquoted field,
- explicit configured null token.

Recommended default explicit null tokens:

```text
null
NULL
```

The empty string and null are distinct for content and notes.

Canonical behavior:

- empty identifier: invalid,
- empty required enum: missing,
- empty optional string: empty string unless config says blank-as-null,
- empty optional numeric or boolean: null,
- literal `"unknown"` remains an enum value where allowed.

### 5.3 CSV booleans

Accepted case-insensitive boolean tokens:

```text
true
false
```

Optional compatibility tokens:

```text
1
0
yes
no
```

Compatibility tokens must be enabled explicitly because `yes` and `no` are also canonical external-grounding values.

Canonical normalized booleans are:

```text
true
false
null
```

### 5.4 CSV list fields

List-valued fields must be JSON array strings.

Example:

```csv
parent_ids
"[""v1::v1_01"",""v1::v1_02""]"
```

A blank CSV field normalizes to an empty list only for fields whose schema defines blank as empty list.

For `parent_ids`:

- blank field: empty list,
- `[]`: empty list,
- malformed JSON array: error,
- JSON scalar: error,
- array containing non-string entries: error.

### 5.5 CSV datetimes

Datetime fields must use ISO 8601 unless a schema mapping declares another parse format.

### 5.6 CSV numbers

Numeric fields must use a period as the decimal separator.

Thousands separators are not accepted in canonical numeric fields.

Examples:

```text
1
1.0
0.25
```

Invalid canonical numeric examples:

```text
1,000
25%
NaN
Infinity
```

---

## 6. JSONL serialization rules

### 6.1 One object per line

Every nonblank JSONL line must contain one JSON object.

Arrays, scalars, and null at the top level are invalid.

### 6.2 Native types

JSONL should use native types:

- strings for identifiers and enums,
- numbers for weights,
- booleans for flags,
- arrays of strings for `parent_ids`,
- null for missing optional values.

### 6.3 Duplicate keys

JSON objects with duplicate keys must be rejected where the parser can detect them.

### 6.4 Nonfinite numbers

JSONL must not contain:

- NaN,
- Infinity,
- negative Infinity.

### 6.5 Comments

JSONL comments are not supported.

### 6.6 Blank lines

Blank lines may be ignored.

The parser must preserve original line numbers for validation messages.

---

## 7. Parquet serialization rules

### 7.1 Optional status

Parquet support is optional in v0.1 and may require the `pyarrow` extra.

### 7.2 Native types

Recommended canonical Parquet types:

| Canonical field kind | Recommended type |
|---|---|
| identifier | UTF-8 string |
| enum | UTF-8 string |
| content | UTF-8 string |
| boolean | boolean |
| integer | signed 64-bit integer |
| weight | double |
| timestamp | timestamp with timezone |
| parent list | list of UTF-8 strings |

### 7.3 Dictionary encoding

Dictionary-encoded strings may be accepted and normalized.

### 7.4 Partitioned datasets

Partitioned Parquet datasets are deferred unless the CLI explicitly supports a directory input.

### 7.5 Schema conflicts

Conflicting Parquet schemas across row groups or files produce a schema error unless an approved coercion exists.

---

## 8. Canonical records schema

### 8.1 Required fields

| Field | Required | Type | Null allowed | Unit | Notes |
|---|---:|---|---:|---|---|
| `record_id` | yes | string | no | identifier | unique within dataset version |
| `dataset_version` | yes | string | no | version identifier | stable snapshot identifier |
| `content` | yes | string | no | payload or local reference | interpretation controlled by content mode |

### 8.2 Optional common fields

| Field | Required | Type | Null allowed | Unit | Intended use |
|---|---:|---|---:|---|---|
| `topic` | no | string | yes | state identifier | topic representation |
| `label` | no | string | yes | state identifier | task-label representation |
| `timestamp` | no | datetime | yes | ISO 8601 datetime | source or record time |
| `weight` | no | float | yes | user-declared mass | optional weighted analysis |
| `embedding_ref` | no | string | yes | local reference or key | user-supplied embeddings |
| `batch_id` | no | string | yes | identifier | grouping |
| `notes` | no | string | yes | free text | private metadata |
| `content_type` | no | string | yes | media type | v0.1 text default |
| `language` | no | string | yes | language tag | metadata only unless configured |

### 8.3 Required identity uniqueness

Within one normalized run:

```text
(dataset_version, record_id)
```

must be unique.

Duplicate composite keys produce:

```text
E_RECORD_DUPLICATE_ID
```

### 8.4 Record ID restrictions

Recommended v0.1 restrictions:

- nonempty,
- no leading or trailing whitespace,
- maximum 512 Unicode code points,
- must not contain the reserved sequence `::`,
- must not contain NUL.

The `::` restriction enables unambiguous composite-reference serialization.

Status:

```text
APPROVED DECISION UD-006
```

### 8.5 Dataset-version restrictions

Recommended v0.1 restrictions:

- nonempty,
- no leading or trailing whitespace,
- maximum 256 Unicode code points,
- must not contain the reserved sequence `::`,
- must not contain NUL.

### 8.6 Content mode

The entire records source must declare one content mode.

Allowed modes:

```text
inline
local_ref
```

Default:

```text
inline
```

#### Inline mode

`content` contains the analyzable string.

#### Local-reference mode

`content` contains a relative local path.

The path is resolved against an approved base directory.

Mixed inline and local-reference values within one source are not supported unless a future field-level mode is approved.

### 8.7 Content restrictions

For inline text:

- empty content is invalid by default,
- whitespace-only content is invalid by default,
- maximum size may be configured,
- content is excluded from normal logs.

For local references:

- absolute paths may be rejected by default,
- path traversal outside the approved base directory is forbidden,
- network schemes are forbidden,
- symlink handling must follow the privacy specification,
- missing files produce an error for content-dependent analysis.

### 8.8 Content type

Default:

```text
text/plain
```

v0.1 does not promise equal support for image, audio, video, or arbitrary binary content.

### 8.9 Topic and label

`topic` and `label` values:

- are strings,
- are case-sensitive by default,
- must not be silently normalized,
- may be mapped through explicit declarative rules,
- may be null.

A missing topic does not become an `unknown` topic automatically.

The representation specification determines whether missing state values:

- exclude a record from that representation,
- map to an explicit configured missing-state token,
- block the analysis.

### 8.10 Weight

Valid weight:

- finite,
- greater than or equal to zero.

Negative or nonfinite weight produces an error.

When weighted analysis requires complete weights:

- missing weight is an error.

When weighted analysis permits fallback:

- missing weight behavior must be explicit.

Default analysis is unweighted.

### 8.11 Notes

`notes` is private free text.

It must not:

- affect public metrics by default,
- appear in normal logs,
- appear in redacted reports,
- be interpreted through an embedded model.

---

## 9. Canonical provenance schema

### 9.1 Required provenance fields

| Field | Required in provenance row | Type | Null allowed | Notes |
|---|---:|---|---:|---|
| `record_id` | yes | string | no | joins to records |
| `dataset_version` | yes | string | no | joins to records |
| `source_type` | yes | enum | no | declared source class |
| `provenance_confidence` | yes | enum | no | confidence category |
| `external_grounding` | yes | enum | no | `yes`, `no`, `unknown` |

The original migration package treated `external_grounding` as optional. This specification recommends making it required in a matched provenance row while allowing the explicit value `unknown`.

Rationale:

- missing row and unknown grounding remain distinct,
- grounding-field coverage remains meaningful,
- every provenance row has an explicit grounding state.

Status:

```text
APPROVED DECISION UD-008 and UD-009
```

### 9.2 Optional provenance fields

| Field | Type | Null allowed | Notes |
|---|---|---:|---|
| `parent_ids` | list of strings | yes | immediate parent references |
| `generator_id` | string | yes | declared model, process, or author |
| `generator_version` | string | yes | generator version |
| `transformation` | enum | yes | operation connecting parents to child |
| `generation` | non-negative integer | yes | consecutive non-grounding steps |
| `human_reviewed` | boolean | yes | review flag only |
| `batch_id` | string | yes | provenance group |
| `timestamp` | datetime | yes | creation or transformation time |
| `grounding_evidence_ref` | string | yes | local reference or evidence identifier |
| `source_uri` | string | yes | identifier only, no automatic retrieval |
| `license_id` | string | yes | declared license identifier |
| `notes` | string | yes | private provenance notes |

### 9.3 Source type enum

Allowed values:

```text
human
synthetic
mixed
sensor
unknown
```

Enum matching is case-sensitive after mapping.

### 9.4 Provenance confidence enum

Allowed values:

```text
confirmed
log_derived
estimated
unknown
```

### 9.5 External grounding enum

Allowed values:

```text
yes
no
unknown
```

This field controls direct grounding claims.

### 9.6 Transformation enum

Allowed values:

```text
generate
rewrite
summarize
translate
filter
label
carryover
other
```

Unknown transformation must use:

```text
other
```

with optional notes, or remain null.

### 9.7 Human reviewed

Canonical values:

```text
true
false
null
```

A true value does not alter `source_type` or `external_grounding`.

### 9.8 Generation

Canonical type:

- integer,
- greater than or equal to zero,
- nullable.

Recommended meaning:

> Number of consecutive non-grounding generative steps since the most recent externally grounded state.

Validation depends on parent and grounding evidence.

Related decision:

```text
UD-005
```

### 9.9 Provenance-row uniqueness

Each composite key may have at most one canonical provenance row.

Duplicate provenance rows for one record produce:

```text
E_PROVENANCE_DUPLICATE_ROW
```

v0.1 does not merge duplicate provenance rows automatically.

### 9.10 Provenance rows without matching records

A provenance row whose composite key does not match any loaded record produces:

```text
E_PROVENANCE_UNMATCHED_ROW
```

This is an error because the row cannot be attached to the analyzed record set.

Optional future mode may permit ignored external provenance rows, but it is not required.

### 9.11 Records without matching provenance

A record without a matching provenance row:

- remains valid for record-level analysis,
- reduces provenance row coverage,
- is classified as unresolved for direct closure bounds,
- produces:

```text
W_PROVENANCE_MISSING_ROW
```

### 9.12 Conflicting record and provenance fields

When both the records table and provenance table contain the same canonical metadata field:

- identity fields must match exactly,
- provenance-specific fields use the provenance manifest as authority,
- conflicts must not be silently overwritten,
- exact behavior must be declared by field.

Recommended rule:

- `batch_id` conflict: warning,
- `timestamp` conflict: warning with both values preserved in normalized metadata,
- identity conflict: error.

---

## 10. Canonical parent-reference encoding

### 10.1 Composite reference

Canonical text form:

```text
dataset_version::record_id
```

Example:

```text
v1::v1_01
```

### 10.2 Reserved separator

The sequence:

```text
::
```

is reserved.

Canonical `dataset_version` and `record_id` values must not contain it.

This avoids an escaping language in v0.1.

### 10.3 Parent list by format

| Format | Canonical parent representation |
|---|---|
| CSV | JSON array string |
| JSONL | native JSON array of strings |
| Parquet | list of strings |

### 10.4 Empty parent list

Canonical meaning:

```json
[]
```

An empty list means no declared immediate parent.

It does not prove:

- external grounding,
- independence,
- lineage completeness.

### 10.5 Bare parent compatibility

A bare parent ID lacking a dataset version may be accepted only when it resolves to exactly one loaded record.

Behavior:

| Result | Behavior |
|---|---|
| exactly one match | accept with compatibility warning |
| no match | unresolved-parent warning |
| more than one match | ambiguous-parent error |

Canonical normalized export always uses composite references.

### 10.6 Parent-reference whitespace

Leading and trailing whitespace around a parent reference is invalid in canonical inputs.

A schema mapping may trim whitespace if the transformation is explicitly declared.

### 10.7 Duplicate parent references

Repeated identical parent references inside one `parent_ids` list:

- produce a warning or error according to final validation policy,
- normalize to one unique edge only if approved,
- must not increase ancestry mass.

Recommended behavior:

```text
W_PARENT_DUPLICATE_REFERENCE
```

then deduplicate deterministically.

### 10.8 Self-parent

A record referencing itself as a parent produces:

```text
E_LINEAGE_CYCLE
```

### 10.9 Parent version constraints

A parent may reference:

- the same dataset version,
- an earlier dataset version.

A parent must not reference a later version under the approved version order.

Future-version parent produces:

```text
E_PARENT_FUTURE_VERSION
```

Same-version parent is allowed only when the graph remains acyclic.

### 10.10 Parent existence

Parent resolution occurs against all loaded records in the audit bundle.

No parent is fetched from a remote source.

### 10.11 Parent order

Parent-list order has no semantic meaning in v0.1.

Implementations must not infer:

- contribution weight,
- priority,
- causal order.

A future weighted-parent schema requires a new field and specification.

---

## 11. Lineage completeness and classification

### 11.1 Resolvable lineage

A lineage edge is resolvable when its parent reference maps to exactly one loaded record.

### 11.2 Unresolved lineage

Lineage is unresolved when any required ancestry path contains:

- missing parent record,
- unknown grounding at a stopping point,
- conflicting identity,
- invalid parent encoding,
- unapproved stopping boundary.

### 11.3 Ambiguous lineage

Ambiguous parent identity is an error.

The toolkit must not choose a parent through:

- nearest version,
- filename,
- content similarity,
- generator match,
- timestamp proximity.

### 11.4 Cycles

The generational ancestry graph must be a directed acyclic graph.

Cycle detection belongs to graph validity.

A cycle blocks ancestry metrics for the affected graph.

### 11.5 Partial lineage capability

A run may retain partial Level 3 capability when:

- at least one valid path exists,
- affected unresolved records are identified,
- coverage denominators are reported,
- no ambiguous parent remains in the analyzed subgraph.

### 11.6 Declared stopping boundary

A future schema may allow a parent reference to an intentionally unprovided external registry.

v0.1 does not define this mechanism.

Missing parents remain unresolved.

### 11.7 External-root determination

External-root determination uses:

- validated `external_grounding`,
- parent links,
- transformation meaning where relevant,
- carryover collapse rules.

A lineage root without grounding evidence is not an external root.

### 11.8 Carryover rule

Recommended v0.1 carryover behavior:

When a record has:

```text
transformation=carryover
external_grounding=yes
```

and exactly one resolved parent, it preserves the reachable external roots of that parent unless provenance explicitly declares new independent external input.

The carryover record must not automatically become a new distinct root.

### 11.9 New external input

A record may introduce a new external root when:

- `external_grounding=yes`,
- provenance identifies independent external input,
- the grounding is not inherited only through declared parents.

Exact evidence fields may include:

- parentless externally grounded record,
- separate grounding evidence reference,
- approved source relation.

### 11.10 Multi-parent lineage

A child may have zero, one, or multiple parents.

Multi-parent records require:

- all parent references serialized,
- no implied contribution weights,
- complete root-union computation for resolved paths.

---

## 12. Version-order specification

### 12.1 Ordering authority

Version chronology must come from one approved source.

Priority:

1. explicit standalone or config `version_order`,
2. valid version timestamps,
3. user-declared CLI order.

Lexical sorting is not sufficient.

### 12.2 Version-order JSON form

Recommended structure:

```json
{
  "version_order": [
    "v1",
    "v2",
    "v3"
  ]
}
```

Every loaded dataset version used in longitudinal analysis must appear exactly once.

### 12.3 Integer-rank form

Alternative mapping:

```json
{
  "version_rank": {
    "v1": 0,
    "v2": 1,
    "v3": 2
  }
}
```

Ranks must be:

- integers,
- unique,
- contiguous after normalization unless gaps are explicitly permitted.

Recommended v0.1 rule:

- gaps allowed,
- order determined by numeric rank.

### 12.4 Timestamp order

When timestamps define order:

- every compared version must have one valid timestamp,
- timestamps must include timezone,
- equal timestamps produce an ordering conflict unless a tie-break is explicitly supplied.

### 12.5 CLI order

The user may declare comparison order through argument order.

The resolved order must appear in run metadata.

### 12.6 Conflicting order sources

If multiple sources disagree:

```text
E_VERSION_ORDER_CONFLICT
```

No longitudinal metric may run until resolved.

### 12.7 Missing ordering evidence

When multiple versions exist without order:

- per-version analysis may continue,
- longitudinal comparison is unavailable,
- capability status is `unavailable`,
- warning:

```text
W_VERSION_ORDER_MISSING
```

### 12.8 Parent version validation

Parent version checks use the resolved version order.

If version order is unavailable:

- same-version cycle checks may run,
- cross-version future-parent validation is unavailable,
- warning must be reported.

---

## 13. Representation-input specification

### 13.1 Explicit representation config

Recommended structure:

```json
{
  "representation": {
    "name": "topic",
    "source": "topic_field",
    "field": "topic",
    "version": "hero-topic-v1",
    "missing_value_policy": "exclude"
  }
}
```

### 13.2 Supported representation sources

```text
config
topic_field
label_field
embedding_clusters
content_hash
```

### 13.3 Field representation

For `topic_field` or `label_field`:

- configured field must exist,
- values must be strings or null,
- mapping may normalize values only through declared rules,
- state identity remains case-sensitive by default.

### 13.4 Missing state-value policies

Allowed policies:

```text
exclude
error
explicit_missing_state
```

#### Exclude

Record remains in general audit but is excluded from representation metrics.

#### Error

Missing value blocks representation analysis.

#### Explicit missing state

Record maps to a configured state ID, such as:

```text
__MISSING__
```

The state ID must not collide with observed values.

### 13.5 Content-hash representation

Config must declare a normalization profile.

Example:

```json
{
  "representation": {
    "name": "record_form",
    "source": "content_hash",
    "normalization_profile": "exact_utf8_v1"
  }
}
```

### 13.6 Embedding-cluster representation

Required metadata:

- embedding source ID,
- embedding model name where known,
- embedding model version,
- dimension,
- clustering method,
- clustering parameters,
- cluster-label file hash.

The toolkit does not create embeddings through a remote model in v0.1.

### 13.7 Representation compatibility declaration

Recommended structure:

```json
{
  "representation_compatibility": {
    "v1": "hero-topic-v1",
    "v2": "hero-topic-v1"
  }
}
```

Different representation versions require an explicit mapping.

### 13.8 Representation mapping

A state mapping across versions may be supplied declaratively.

Example:

```json
{
  "state_mapping": {
    "old_cat": "cat",
    "house_cat": "cat"
  }
}
```

Many-to-one mapping is allowed when declared.

One-to-many mapping is deferred because it requires allocation rules.

---

## 14. Schema-mapping specification

### 14.1 Purpose

Schema mapping converts user-specific field names and supported values into canonical fields without changing the source files.

### 14.2 Mapping file structure

Recommended JSON structure:

```json
{
  "schema_version": "1.0",
  "records": {
    "fields": {
      "record_id": {
        "source": "id",
        "operations": [
          {"op": "trim"}
        ]
      },
      "dataset_version": {
        "constant": "v1"
      },
      "content": {
        "source": "text"
      },
      "topic": {
        "source": "category",
        "operations": [
          {
            "op": "map_values",
            "mapping": {
              "Cats": "cat",
              "Dogs": "dog"
            },
            "unmapped": "keep"
          }
        ]
      }
    }
  },
  "provenance": {
    "fields": {
      "source_type": {
        "source": "origin",
        "operations": [
          {
            "op": "map_values",
            "mapping": {
              "person": "human",
              "model": "synthetic"
            },
            "unmapped": "error"
          }
        ]
      }
    }
  }
}
```

### 14.3 Allowed operations

Recommended approved operations:

```text
rename
trim
cast_string
cast_integer
cast_float
cast_boolean
parse_datetime
parse_json_list
constant
coalesce
map_values
normalize_whitespace
lowercase
uppercase
```

Not every operation is appropriate for every field.

### 14.4 Operation definitions

#### `trim`

Removes leading and trailing Unicode whitespace.

Must be explicitly declared for identifiers.

#### `cast_string`

Converts supported scalar values to canonical strings.

Must not convert nested objects or arrays.

#### `cast_integer`

Accepts integer values or exact integer strings.

Must reject fractional numbers.

#### `cast_float`

Accepts finite numeric values or finite numeric strings.

#### `cast_boolean`

Uses explicitly configured token mapping.

#### `parse_datetime`

Requires a declared format or ISO 8601 mode.

#### `parse_json_list`

Parses a JSON array string.

#### `constant`

Assigns one declared constant value.

#### `coalesce`

Selects the first nonmissing value among named source fields.

#### `map_values`

Maps exact source values to canonical values.

Unmapped behavior must be one of:

```text
keep
null
error
```

#### `normalize_whitespace`

Applies a declared internal-whitespace rule.

It must not be applied to content silently.

#### `lowercase` and `uppercase`

Allowed only when the user explicitly chooses case-folding semantics.

### 14.5 Forbidden operations

The mapping engine must reject:

- arbitrary Python,
- `eval`,
- `exec`,
- shell commands,
- subprocess execution,
- dynamic imports,
- network calls,
- remote scripts,
- Jinja or templating execution,
- regular-expression replacement with executable callbacks,
- hidden model inference,
- arbitrary user functions,
- filesystem writes outside approved outputs.

### 14.6 Regular expressions

General regular-expression transforms are deferred from the minimum safe mapping language.

A future approved restricted regex operation may be added with timeout and complexity controls.

### 14.7 Mapping order

Operations execute in listed order.

The resolved operation sequence must appear in run metadata.

### 14.8 Mapping source-field existence

Missing required source field produces:

```text
E_MAPPING_SOURCE_FIELD_MISSING
```

Optional coalesce fields may be absent.

### 14.9 Canonical-field collision

Two source mappings targeting the same canonical field produce an error unless one approved coalesce rule owns the field.

### 14.10 Unmapped source fields

Unmapped source fields:

- may be ignored,
- may be preserved in a namespaced extras object when configured,
- must not silently influence metrics.

Recommended default:

```text
ignore and record field inventory
```

### 14.11 Unsafe mapping error

Unsafe operation produces:

```text
E_MAPPING_UNSAFE_TRANSFORM
```

---

## 15. Normalization rules

### 15.1 Source preservation

The toolkit must not mutate original input files.

Normalization produces an in-memory table and may optionally produce a normalized export.

### 15.2 Canonical field names

After mapping, canonical fields use exact lowercase snake_case names.

### 15.3 Identifier normalization

Default:

- no case conversion,
- no Unicode normalization,
- no automatic prefixing,
- no numeric coercion,
- no whitespace trimming unless explicitly declared.

### 15.4 Enum normalization

Canonical enums must match exact approved values after mapping.

Unknown source tokens do not automatically become canonical `unknown`.

Unrecognized enum values produce:

```text
E_SCHEMA_ENUM
```

unless the mapping explicitly maps them.

### 15.5 Numeric normalization

- integer fields remain integers,
- float fields must be finite,
- ratios are not accepted as percentages unless explicitly mapped,
- strings such as `"50%"` require an approved conversion operation, which is not in the minimum v0.1 mapping language.

### 15.6 Datetime normalization

Normalized datetimes must include timezone information.

Recommended internal form:

```text
UTC-aware datetime
```

Original timezone may be preserved in metadata.

### 15.7 List normalization

Parent lists:

- preserve unique canonical references,
- use deterministic order for export,
- do not use list order as weighting.

Recommended normalized order:

```text
ascending canonical record key
```

### 15.8 Blank and null normalization

Blank handling must be field-specific.

Canonical rules:

| Field kind | Blank behavior |
|---|---|
| required identifier | error |
| optional identifier | null |
| required enum | missing or error |
| optional enum | null |
| parent list | empty list |
| content inline | error by default |
| notes | empty string allowed |
| numeric | null if optional |
| boolean | null if optional |

### 15.9 Duplicate row normalization

Duplicate identical physical rows do not become one record automatically.

If they share the same composite record key, they produce an identity error.

Exact duplicate content is handled by metrics, not row deduplication.

---

## 16. Content-reference security

### 16.1 Base directory

Local content references resolve relative to a declared base directory.

Default base:

```text
directory containing the records file
```

### 16.2 Path traversal

Resolved paths must remain inside the approved base directory unless an explicit allowlist permits another local directory.

References containing traversal components are normalized and checked.

Escaping the base directory produces:

```text
E_CONTENT_REF_OUTSIDE_BASE
```

### 16.3 Network schemes

Forbidden schemes include:

```text
http
https
ftp
s3
gs
ssh
```

The toolkit may preserve a source URI as metadata, but it must not retrieve it automatically.

### 16.4 Absolute paths

Recommended default:

- reject absolute paths in portable fixtures,
- allow only through explicit local configuration.

### 16.5 Symlinks

Recommended security rule:

- resolve symlinks,
- confirm final path remains inside approved base,
- reject broken symlinks.

### 16.6 File type

v0.1 text analysis should accept UTF-8 text files.

Binary files require a future content loader.

### 16.7 Content size

Config may set:

- maximum bytes per content file,
- maximum total bytes loaded.

Exceeding limits produces a clear error.

---

## 17. Provenance-coverage calculation inputs

### 17.1 Total denominator

Default denominator:

```text
all valid analyzed records in the selected dataset scope
```

Invalid records excluded before analysis must appear in validation results.

### 17.2 Matching provenance row

A record has a matching provenance row when:

- composite keys match exactly,
- one and only one provenance row exists,
- required join fields are valid.

### 17.3 Required-field-valid row

A matched row counts toward required-field coverage when all required provenance fields are valid.

### 17.4 Grounding-known row

A matched row counts toward grounding-field coverage when:

```text
external_grounding=yes
```

or:

```text
external_grounding=no
```

The value `unknown` does not count as known.

### 17.5 Missing-row class

A record without a matching row is distinct from a row with:

```text
source_type=unknown
external_grounding=unknown
```

Reports should preserve both classes.

---

## 18. Direct closure classification inputs

### 18.1 Known open

Condition:

```text
valid matched provenance row
external_grounding=yes
```

### 18.2 Known closed

Condition:

```text
valid matched provenance row
external_grounding=no
```

### 18.3 Unresolved

Condition includes:

- missing provenance row,
- invalid provenance row,
- `external_grounding=unknown`.

### 18.4 Confidence handling

`provenance_confidence` does not change the lower and upper-bound category by default.

The report must disclose confidence shares separately.

A future sensitivity analysis may restrict known classifications to selected confidence levels.

### 18.5 Estimated grounding

A record may have:

```text
external_grounding=yes
provenance_confidence=estimated
```

It remains directly classified as open under the declared metadata, while the report identifies estimated confidence.

No silent confidence discount is applied.

---

## 19. Lineage closure classification inputs

### 19.1 Known grounded lineage

Requirements:

- complete resolved ancestry for the classification path,
- at least one validated external root,
- no blocking conflict.

### 19.2 Known closed lineage

Requirements:

- complete resolved ancestry,
- no external root,
- no missing parent,
- no unknown grounding at a stopping point,
- no cycle.

### 19.3 Unresolved lineage

Any missing or conflicting condition places the record in the unresolved class.

### 19.4 Multiple roots

A record with one or more external roots is lineage grounded.

The number of roots is reported separately.

### 19.5 Root confidence

The confidence of an external-root determination may be summarized from contributing provenance confidence values.

No canonical aggregation formula is approved in v0.1.

Root confidence aggregation remains deferred.

---

## 20. Error and warning taxonomy

### 20.1 Required error fields

Every error object must include:

- `code`,
- `severity`,
- `message`,
- `file_role`,
- `file_path` or redacted path,
- `field` where applicable,
- `record_key` where applicable,
- `row_number` or line number where applicable.

### 20.2 Core errors

| Code | Condition |
|---|---|
| `E_FILE_NOT_FOUND` | Input path does not exist |
| `E_FILE_FORMAT_UNSUPPORTED` | Format is unsupported |
| `E_FILE_ENCODING` | Invalid UTF-8 or text decoding failure |
| `E_FILE_PARSE` | CSV, JSONL, JSON, TOML, or Parquet parse failure |
| `E_SCHEMA_REQUIRED_FIELD` | Required canonical field missing |
| `E_SCHEMA_TYPE` | Value has invalid type |
| `E_SCHEMA_ENUM` | Enum value not canonical |
| `E_RECORD_DUPLICATE_ID` | Duplicate composite record key |
| `E_RECORD_EMPTY_CONTENT` | Required inline content empty |
| `E_PROVENANCE_DUPLICATE_ROW` | More than one provenance row per record |
| `E_PROVENANCE_UNMATCHED_ROW` | Provenance row has no matching record |
| `E_PARENT_FORMAT` | Parent reference or list encoding invalid |
| `E_PARENT_AMBIGUOUS` | Bare or mapped parent has multiple matches |
| `E_PARENT_FUTURE_VERSION` | Parent points to later version |
| `E_LINEAGE_CYCLE` | Directed ancestry cycle detected |
| `E_VERSION_ORDER_CONFLICT` | Ordering sources disagree |
| `E_REPRESENTATION_INCOMPATIBLE` | Longitudinal representation mismatch |
| `E_MAPPING_SOURCE_FIELD_MISSING` | Mapping source field absent |
| `E_MAPPING_TARGET_COLLISION` | Multiple mappings target one canonical field |
| `E_MAPPING_UNSAFE_TRANSFORM` | Mapping uses forbidden operation |
| `E_WEIGHT_INVALID` | Negative, nonfinite, or otherwise invalid weight |
| `E_CONTENT_REF_OUTSIDE_BASE` | Local reference escapes approved base |
| `E_CONTENT_REF_MISSING` | Local referenced file missing |
| `E_CONFIG_INVALID` | Configuration invalid |
| `E_EMPTY_DATASET` | No valid records remain |

### 20.3 Core warnings

| Code | Condition |
|---|---|
| `W_PROVENANCE_MISSING_ROW` | Record has no matching provenance row |
| `W_GROUNDING_UNKNOWN` | Grounding explicitly unknown |
| `W_PARENT_UNRESOLVED` | Parent has no loaded match |
| `W_PARENT_BARE_COMPATIBILITY` | Bare parent accepted through unique resolution |
| `W_PARENT_DUPLICATE_REFERENCE` | Parent list repeats a reference |
| `W_GENERATION_MISMATCH` | Declared generation conflicts with computable value |
| `W_REPRESENTATION_FALLBACK` | Lower-priority representation selected |
| `W_LONGITUDINAL_INCOMPATIBLE_REPRESENTATION` | Comparison blocked or partial |
| `W_VERSION_ORDER_MISSING` | Multiple versions lack order |
| `W_CONTENT_ANALYSIS_UNAVAILABLE` | Content reference unavailable but metadata analysis continues |
| `W_OPTIONAL_FIELD_MISSING` | Optional field needed for a requested capability absent |
| `W_PARTIAL_LINEAGE` | Lineage analysis covers only part of records |
| `W_PROVENANCE_ESTIMATED` | Result relies on estimated provenance |
| `W_MAPPING_VALUE_UNMAPPED` | Value preserved or nulled under declared mapping rule |

### 20.4 Severity promotion

Strict mode may promote selected warnings to errors.

The promoted set must be explicit in config and run metadata.

### 20.5 Warning deduplication

Repeated warnings may be summarized by code and count.

At least one representative location should remain available.

Raw content must not appear.

---

## 21. Validation sequence

Validation should occur in this order.

### Step 1: file inventory

Validate:

- existence,
- role,
- extension,
- declared format,
- size,
- encoding.

### Step 2: parse

Parse physical files without semantic coercion beyond format requirements.

### Step 3: map

Apply declarative schema mapping.

### Step 4: canonical type validation

Validate canonical field types and enums.

### Step 5: identity validation

Validate composite record and provenance uniqueness.

### Step 6: join validation

Join provenance rows to records.

### Step 7: version-order validation

Resolve and validate chronology.

### Step 8: parent-reference validation

Parse and resolve parent references.

### Step 9: graph validation

Check self-parent and cycles when lineage analysis is requested.

### Step 10: representation validation

Validate selected representation and cross-version compatibility.

### Step 11: capability classification

Determine available, partial, unavailable, and experimental capabilities.

### Step 12: metric eligibility

Authorize only metrics whose data prerequisites pass.

A later failure must not erase earlier valid validation results.

---

## 22. Validation result model

### 22.1 Valid record

A record is valid for general metadata analysis when:

- identity is valid,
- required records fields exist,
- content mode requirements are satisfied.

### 22.2 Valid record for representation analysis

Additional requirements:

- usable representation value,
- representation mapping valid.

### 22.3 Valid record for provenance analysis

Additional requirement:

- valid matched provenance row, or classification as missing provenance for bounds.

### 22.4 Valid record for lineage analysis

Additional requirements:

- parent references parse,
- ambiguous parents absent,
- affected graph acyclic,
- requested lineage operation supports partial resolution.

### 22.5 Excluded record

A record excluded from one metric family must be counted and explained.

Example:

```text
10 total valid records
8 records included in topic diversity
2 records excluded because topic is missing
```

### 22.6 Fatal versus family-specific failure

A lineage cycle may block lineage metrics while preserving content and provenance metrics if the overall run can still produce a valid partial report.

The reporting specification decides whether the run exits nonzero.

Recommended behavior:

- invalid primary record schema: fatal,
- cycle: lineage-family error,
- ambiguous parent: lineage-family error,
- unsafe mapping: fatal,
- representation incompatibility: longitudinal-family error.

---

## 23. Normalized internal tables

### 23.1 Normalized records table

Minimum columns:

```text
record_key
dataset_version
record_id
content
```

Optional normalized columns preserve canonical names.

### 23.2 Normalized provenance table

Minimum columns:

```text
record_key
dataset_version
record_id
source_type
provenance_confidence
external_grounding
parent_ids
```

### 23.3 Normalized lineage-edge table

Recommended columns:

```text
parent_record_key
child_record_key
resolution_status
source_parent_text
```

### 23.4 Normalized version table

Recommended columns:

```text
dataset_version
version_rank
version_timestamp
order_source
```

### 23.5 Normalized representation table

Recommended columns:

```text
record_key
representation_name
state_id
inclusion_status
exclusion_reason
```

### 23.6 Extras

Unmapped fields may be stored in:

```text
extras
```

for debugging or normalized export when explicitly enabled.

Extras must not influence metrics automatically.

---

## 24. Normalized manifest export

### 24.1 Optional output

The toolkit may export a normalized provenance manifest.

### 24.2 Export purpose

The export provides:

- canonical field names,
- canonical enum values,
- composite parent references,
- normalized lists,
- explicit nulls,
- validation status.

### 24.3 Export restrictions

The normalized export must not:

- invent provenance,
- resolve missing parents,
- convert unknown grounding,
- include private notes unless requested,
- rewrite source files in place.

### 24.4 Recommended JSONL export

Each row should include:

```json
{
  "dataset_version": "v2",
  "record_id": "v2_05",
  "source_type": "synthetic",
  "provenance_confidence": "confirmed",
  "parent_ids": ["v1::v1_01"],
  "generator_id": "model_A",
  "generator_version": "1.0",
  "transformation": "generate",
  "generation": 1,
  "human_reviewed": false,
  "external_grounding": "no"
}
```

### 24.5 Validation annotations

Optional fields:

```text
_validation_status
_warning_codes
```

These fields must be namespaced to avoid collision with canonical source fields.

---

## 25. Privacy classification of fields

### 25.1 Normal-report safe by default

Generally safe metadata:

- row counts,
- field names,
- version IDs,
- metric counts,
- enum shares,
- warning codes.

### 25.2 Potentially identifying

Treat as potentially identifying:

- record ID,
- batch ID,
- generator ID,
- source URI,
- grounding evidence reference,
- file paths.

Redacted mode may hash or omit them.

### 25.3 Sensitive content

Exclude by default from logs and public reports:

- content,
- notes,
- provenance notes,
- full embeddings,
- local content paths,
- private source URIs.

### 25.4 Hashing

Redacted record IDs must use the approved privacy hashing rule.

The same run should produce stable redacted IDs when configured for deterministic sharing.

---

## 26. Hero records schema

### 26.1 `records_v1.csv`

```csv
record_id,dataset_version,content,topic
v1_01,v1,"How to care for a house cat.",cat
v1_02,v1,"How to care for a house dog.",dog
v1_03,v1,"Why small birds need clean water.",bird
v1_04,v1,"Signs of stress in aquarium fish.",fish
v1_05,v1,"Basic habitat needs for lizards.",lizard
v1_06,v1,"How turtles regulate temperature.",turtle
v1_07,v1,"How to request a refund politely.",refund
v1_08,v1,"Battery overheating warning signs.",battery
```

### 26.2 `records_v2.csv`

```csv
record_id,dataset_version,content,topic
v2_01,v2,"How to care for a house cat.",cat
v2_02,v2,"How to care for a house dog.",dog
v2_03,v2,"Why small birds need clean water.",bird
v2_04,v2,"Signs of stress in aquarium fish.",fish
v2_05,v2,"Simple cat care checklist for beginners.",cat
v2_06,v2,"Simple dog care checklist for beginners.",dog
v2_07,v2,"Short refund request template.",refund
v2_08,v2,"House cat care tips in one paragraph.",cat
```

### 26.3 Canonical `provenance.csv`

```csv
dataset_version,record_id,source_type,provenance_confidence,parent_ids,generator_id,generator_version,transformation,generation,human_reviewed,external_grounding
v1,v1_01,human,confirmed,[],human_author,,carryover,0,true,yes
v1,v1_02,human,confirmed,[],human_author,,carryover,0,true,yes
v1,v1_03,human,confirmed,[],human_author,,carryover,0,true,yes
v1,v1_04,human,confirmed,[],human_author,,carryover,0,true,yes
v1,v1_05,human,confirmed,[],human_author,,carryover,0,true,yes
v1,v1_06,human,confirmed,[],human_author,,carryover,0,true,yes
v1,v1_07,human,confirmed,[],human_author,,carryover,0,true,yes
v1,v1_08,human,confirmed,[],human_author,,carryover,0,true,yes
v2,v2_01,human,confirmed,"[""v1::v1_01""]",human_author,,carryover,0,true,yes
v2,v2_02,human,confirmed,"[""v1::v1_02""]",human_author,,carryover,0,true,yes
v2,v2_03,human,confirmed,"[""v1::v1_03""]",human_author,,carryover,0,true,yes
v2,v2_04,human,confirmed,"[""v1::v1_04""]",human_author,,carryover,0,true,yes
v2,v2_05,synthetic,confirmed,"[""v1::v1_01""]",model_A,1.0,generate,1,false,no
v2,v2_06,synthetic,confirmed,"[""v1::v1_02""]",model_A,1.0,generate,1,false,no
v2,v2_07,synthetic,confirmed,"[""v1::v1_07""]",model_A,1.0,generate,1,false,no
v2,v2_08,synthetic,confirmed,"[""v1::v1_01""]",model_A,1.0,generate,1,false,no
```

### 26.4 Hero version order

```json
{
  "version_order": ["v1", "v2"]
}
```

### 26.5 Hero representation config

```json
{
  "representation": {
    "name": "topic",
    "source": "topic_field",
    "field": "topic",
    "version": "hero-topic-v1",
    "missing_value_policy": "error"
  }
}
```

### 26.6 Hero interpretation requirements

The canonical hero inputs establish:

- complete v2 provenance row coverage,
- declared v2 source shares,
- parent links from v2 to v1,
- five distinct external roots supporting v2,
- topic representation compatibility,
- ordered v1 to v2 comparison.

They do not establish:

- model-performance change,
- causal effect of any ancestor,
- universal collapse,
- universal integrity loss.

---

## 27. Additional lineage fixture requirements

### 27.1 Valid multi-root fixture

Required features:

- one child with two external-root parents,
- one child with one external root,
- unequal root incidence,
- one unresolved parent,
- one explicit unknown grounding value.

### 27.2 Expected valid outcomes

The fixture must support hand calculation of:

- resolved-parent edge coverage,
- resolved-lineage coverage,
- distinct external-root count,
- ancestor incidence,
- fractional root mass,
- ancestry HHI,
- effective external-root count,
- unresolved lineage count.

### 27.3 Ambiguous-parent fixture

Required features:

- same bare `record_id` in two versions,
- child uses bare parent ID,
- no explicit version.

Expected error:

```text
E_PARENT_AMBIGUOUS
```

### 27.4 Cycle fixtures

Required:

- self-cycle,
- two-node cycle,
- longer cycle.

Expected error:

```text
E_LINEAGE_CYCLE
```

### 27.5 Future-parent fixture

Child in earlier version references parent in later version.

Expected error:

```text
E_PARENT_FUTURE_VERSION
```

---

## 28. Schema compatibility and evolution

### 28.1 Specification version

Mapping and normalized exports should include:

```text
schema_version
```

Recommended initial value:

```text
1.0
```

### 28.2 Backward-compatible changes

Examples:

- adding optional field,
- adding optional enum with explicit unknown handling,
- adding optional report-only annotation.

### 28.3 Breaking changes

Examples:

- changing required field,
- changing denominator,
- changing parent encoding,
- changing canonical enum meaning,
- changing generation meaning,
- changing identifier uniqueness scope.

Breaking changes require:

- new schema version,
- migration note,
- fixture update,
- traceability review.

### 28.4 Unknown future fields

Readers should ignore unknown optional fields only when:

- core required fields remain valid,
- the file schema version is compatible,
- no unknown field claims to redefine canonical meaning.

---

## 29. Security requirements

### 29.1 No executable data

Input files are data only.

They must not cause:

- code execution,
- import,
- plugin loading,
- shell execution,
- network retrieval.

### 29.2 Formula injection in CSV export

When exporting CSV, fields beginning with spreadsheet formula markers should be escaped or protected.

Potential markers:

```text
=
+
-
@
```

The original raw value may be preserved in JSONL export.

### 29.3 Archive files

Automatic archive extraction is not required.

If later supported, archives require:

- path traversal protection,
- size limits,
- file-count limits,
- symlink restrictions.

### 29.4 Resource limits

Config should permit limits for:

- input file size,
- total rows,
- content bytes,
- parent edges,
- JSON nesting depth,
- list length.

Exceeding a limit must fail clearly.

### 29.5 JSON nesting

Schema mapping and config inputs should enforce a reasonable maximum nesting depth.

---

## 30. Acceptance tests for this specification

### 30.1 Records parsing

Required cases:

- minimal valid CSV,
- minimal valid JSONL,
- optional valid Parquet,
- duplicate header,
- missing required field,
- invalid UTF-8,
- empty dataset,
- duplicate composite key,
- empty content.

### 30.2 Provenance parsing

Required cases:

- complete valid manifest,
- missing provenance row,
- unmatched provenance row,
- duplicate provenance row,
- invalid source type,
- invalid confidence,
- unknown grounding,
- invalid boolean,
- invalid generation.

### 30.3 Parent parsing

Required cases:

- empty list,
- one composite parent,
- multiple composite parents,
- unique bare compatibility,
- unresolved bare parent,
- ambiguous bare parent,
- malformed JSON list,
- duplicate parent,
- self-parent.

### 30.4 Version order

Required cases:

- explicit list,
- explicit rank,
- timestamp order,
- CLI order,
- conflicting order,
- missing order,
- future parent.

### 30.5 Schema mapping

Required cases:

- rename success,
- constant success,
- coalesce success,
- enum map success,
- missing source field,
- target collision,
- unsafe operation,
- operation-order determinism,
- unmapped-value behavior.

### 30.6 Content references

Required cases:

- valid relative path,
- missing file,
- absolute path blocked,
- traversal blocked,
- symlink escape blocked,
- network URI blocked.

### 30.7 Representation

Required cases:

- topic field,
- label field,
- missing-state exclude,
- missing-state error,
- explicit missing state,
- content hash,
- compatible versions,
- incompatible versions.

### 30.8 Coverage

Required hand-checkable cases:

- 100 percent row coverage,
- partial row coverage,
- explicit unknown grounding,
- missing provenance versus unknown provenance,
- direct closure lower and upper bounds.

### 30.9 Lineage

Required cases:

- complete external ancestry,
- complete known-closed lineage,
- unresolved parent,
- unknown root grounding,
- multiple roots,
- cycle.

### 30.10 Privacy

Required cases:

- no raw content in normal logs,
- notes excluded,
- redacted IDs,
- source paths redacted when configured.

---

## 31. Phase acceptance requirements

### 31.1 Phase 2 gate

Phase 2 passes when:

- hero records load without manual changes,
- canonical provenance loads,
- schema mapping works,
- unknown provenance remains unknown,
- exact warnings and errors are emitted,
- observability and capability inputs are available,
- no metric implementation is required to validate inputs.

### 31.2 Phase 3 gate

Before Phase 3 metrics begin:

- closure-classification inputs are frozen,
- representation rules are frozen,
- tail input requirements are frozen,
- weight behavior is frozen.

### 31.3 Phase 5 gate

Before lineage release:

- composite parent encoding is approved,
- cycle behavior is approved,
- external-root rules are frozen,
- multi-root fixture passes,
- missing-parent coverage is reported.

### 31.4 Release gate

Public v0.1 release requires:

- schema version,
- example files,
- validation documentation,
- normalized manifest example,
- security review of mapping operations,
- no unresolved blocking data decisions.

---

## 32. Decision dependencies

| Decision | Data behavior affected |
|---|---|
| `UD-005` | generation validation |
| `UD-006` | parent encoding and reserved separator |
| `UD-007` | version ordering |
| `UD-008` | provenance coverage and required provenance fields |
| `UD-009` | grounding authority |
| `UD-010` | closure classification |
| `UD-011` | representation selection |
| `UD-012` | tail input config |
| `UD-014` | multi-root allocation inputs |
| `UD-015` | missing and ambiguous parent behavior |
| `UD-016` | schema mapping operations |
| `UD-018` | cycle classification |
| `UD-020` | near-duplicate inputs |
| `UD-021` | weight behavior |
| `UD-033` | hero corrections |

Until approved, related rules remain the recommended baseline.

---

## 33. Approval checklist

The Theory Owner and reviewers should confirm:

- [ ] records and provenance use composite identity,
- [ ] source type and grounding remain separate,
- [ ] missing provenance and explicit unknown remain separate,
- [ ] parent lists use canonical serialization,
- [ ] bare parent compatibility cannot create ambiguity,
- [ ] reserved identifier syntax is acceptable,
- [ ] version order cannot be inferred from filenames,
- [ ] local content references cannot escape approved directories,
- [ ] mapping operations remain declarative,
- [ ] original files are never mutated,
- [ ] normalization is deterministic,
- [ ] raw content is excluded from normal logs,
- [ ] incomplete lineage widens uncertainty,
- [ ] a lineage root is not automatically an external root,
- [ ] carryovers do not multiply independent roots,
- [ ] the hero files conform to the canonical schema,
- [ ] all required validation cases are testable.

### Theory Owner decision

- [ ] Approve data and provenance baseline
- [ ] Approve with exceptions
- [ ] Return for revision

Exceptions:

```text

```

Theory Owner:

```text
Xiangyu Guo
```

Approval date:

```text

```

Approved status:

```text
PENDING
```

### Technical Maintainer acknowledgment

- [ ] File formats are implementable.
- [ ] Canonical types are unambiguous.
- [ ] Joins and parent resolution are deterministic.
- [ ] Mapping operations can be sandbox-free and local.
- [ ] Error conditions can be tested.

Technical notes:

```text

```

Maintainer:

```text

```

Date:

```text

```

### Security Reviewer acknowledgment

- [ ] No input field authorizes code execution.
- [ ] Content references remain local.
- [ ] Path traversal is blocked.
- [ ] Normal logs exclude content and notes.
- [ ] CSV export injection risk is addressed.

Security notes:

```text

```

Reviewer:

```text

```

Date:

```text

```

---

## 34. Change-control rule

After approval:

1. a canonical field must not change type without a schema-version change,
2. a required field must not become optional silently,
3. an optional field must not become required silently,
4. identifier uniqueness scope must remain stable,
5. parent encoding changes require a migration path,
6. new mapping operations require security review,
7. new source types or grounding states require definition and report updates,
8. normalized exports must declare schema version,
9. fixture changes require golden-output review,
10. input convenience must not weaken unknown handling or lineage uncertainty,
11. no implementation may infer provenance through content unless a future separately governed feature is approved.
