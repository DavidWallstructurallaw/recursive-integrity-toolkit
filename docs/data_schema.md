# Data Schema and Calculation Contracts

Canonical field meanings remain governed by `DATA_AND_PROVENANCE_SPEC.md` and `DEFINITIONS_AND_UNITS.md`. This guide describes implemented interfaces and their boundaries. Actual final acceptance is recorded separately.

## Explicit bundle

`io.validation.validate_bundle(AuditBundle(...))` performs the complete input workflow and returns `BundleValidationResult` in memory. Exactly one primary records source, zero or more comparison sources, and at most one provenance, mapping, config and version-order source are accepted. Duplicate or competing singleton declarations fail. No directory discovery or recursive include occurs.

Bundle paths must be absolute or relative to explicit absolute base_directory. Config-file input paths resolve relative to that file. An in-memory configuration cannot silently override a supplied config file. Conflicting explicit resource limits fail. Control snapshots reject invalid roots, duplicate JSON keys, nonfinite values and syntax/depth violations. TOML uses the standard-library parser. EXPECTED_OUTPUTS.md remains a static analytical contract, never input data.

## Physical ingestion

`load_table(InputSource(...), limits=ResourceLimits(...))` reads local CSV/JSONL or optional Parquet. Inventory retains role, format, exact byte SHA-256, size, row count, fields and source path. Hashing and parsing consume the same snapshot. `inventory_source` alone leaves row_count=None and fields empty, without interpreting contents.

CSV retains strings, original row spelling, quoted/empty distinctions, embedded newlines and physical row/line positions. JSONL retains native values and absent fields. Nonempty unique CSV headers and consistent widths are required. Blank lines outside quotes are ignored. Malformed quoting, non-object JSONL, duplicate keys, nonfinite/overflowed numbers and invalid UTF-8 fail. Empty record tables fail; supplied-empty provenance remains distinct from no manifest and must still have required schema columns.

An explicit format selects one parser and may override the extension when parsing succeeds, under data-spec section 3.7. There is no fallback sniffing. Role conflicts fail. JSON/TOML/NPY declarations can be inventoried without becoming evidence for unimplemented capabilities. max_file_bytes, max_rows and max_json_depth are explicit; compressed-byte bounds do not certify decompression memory safety. Detected file changes during reads fail. URI/UNC/device forms are blocked; host-mounted network filesystems are outside the lexical guarantee. No source file is changed.

### Real optional Parquet

PyArrow imports only in the Parquet reader. A byte buffer is used rather than allowing Arrow to resolve paths or remote filesystems. Missing PyArrow does not break package import or CSV/JSONL. To run the explicit real backend suite:

```bash
python -m pip install ".[test,parquet]"
RIT_TEST_PARQUET=1 python -m pytest -p no:cacheprovider -q
```

PowerShell requires setting `$env:RIT_TEST_PARQUET = "1"` separately. Selecting those tests without PyArrow fails instead of skipping. Candidate CI runs full core and real-extra suites independently and checks that roundtrip, row-limit and invalid-file cases were all collected. Results are never summed as independent populations.

## Safe mapping

`load_mapping` reads an explicit snapshot; `compile_mapping` validates a plain dictionary; `parse_mapping_json` preserves duplicate-key diagnostics; `map_row` transforms a plain row or RawRow without mutation.

Canonical version syntax is schema_version=1.0. The early mapping_version spelling remains compatibility-only; exactly one is allowed. Sections are records/provenance with fields. Each target has one source/constant selector or an initial constant/coalesce. Duplicate targets/selectors and extra operation arguments fail.

| Operation | Explicit behavior |
|---|---|
| rename | Enclosing field key names target; source names original literal field. |
| trim | Leading/trailing Unicode whitespace removal only when listed. |
| cast_string | Strings and finite scalar numbers/booleans; no objects/arrays. |
| cast_integer | Native integers or signed ASCII integer strings, no booleans/floats/fractions/implicit trim. |
| cast_float | Finite numbers or explicit decimal/exponent strings, no bool/nonfinite/implicit trim. |
| cast_boolean | Exact string-token-to-boolean mapping required. |
| parse_datetime | Explicit iso8601 or portable numeric strptime directives; no timezone inference. |
| parse_json_list | Strict JSON-array parsing with duplicate/nonfinite rejection. |
| constant | Explicit field constant or operation value. |
| coalesce | First present non-null original source in declared order. |
| map_values | Exact mapping and explicit unmapped keep/null/error. |
| normalize_whitespace | Explicit collapse mode, separate from trim. |
| lowercase, uppercase | Explicit case changes without automatic Unicode normalization. |

All selectors read the original row; targets never feed other targets. Operations remain ordered. Missing required sources fail. All-absent coalesce leaves absent; present-null with no value yields null. Zero, false, empty values and literal unknown are not missing. CSV null-token interpretation belongs to normalization, with original spelling retained.

MappedRow retains source/unmapped names, SHA-256, selector/operation traces, locations and explicit unmapped-policy notices. preserve_extras=True keeps unused values separately; default does not. Payload/declaration values are hidden from repr. Expressions, templates, callbacks, dynamic imports, subprocess and environment/network access are forbidden; literal code-like strings remain inert.

## Canonical normalization

`normalize_row` accepts typed dictionaries, RawRow or MappedRow; `normalize_table` accepts LoadedTable. Neither loads files, maps fields, joins evidence or classifies capabilities. Identity is exactly (dataset_version, record_id), serialized as dataset_version::record_id. No automatic trim, case folding, Unicode normalization, numeric-ID coercion or content deduplication. Repeated composite keys fail; same ID in different versions remains distinct.

CSV needs FileFormat.CSV and original RawRow spelling. Unquoted blanks and default null/NULL tokens, quoted empty strings, literal unknown, native null and absent fields retain distinctions. Required empty values fail. Blank optional IDs/numbers/booleans become null; blank CSV parents become an empty tuple. JSONL/Parquet do not inherit CSV token semantics.

Mapped CSV additionally supplies source_row. Unchanged selectors inherit quoting evidence; explicit transforms/constants use their returned values without invented lexemes. Numeric/boolean target serialization still applies. NormalizationOptions provides explicit in-memory content/null/blank/boolean/extras policies without changing run-config grammar.

Finite nonnegative weights are row-validated. Generation is nullable nonnegative integer-only. Timestamp strings need explicit timezone and normalize to UTC; supported native timezone/ZoneInfo objects do likewise. Local timezone is not guessed. Inline content obeys an explicit byte limit; local references remain unread.

Canonical values, field_states and extras are detached read-only mappings. Parents are sorted immutable tuples here without resolution/deduplication. Missing/null parents remain unavailable declarations, not inferred independence or grounding. Optional fields stay absent except documented text/plain default and minimum nullable parent column. Defaults are identified. Internal nullable parents do not satisfy the unchanged normalized export-row schema's array requirement; there is no exporter. Private values are excluded from ordinary repr/errors, while source locations remain internal metadata. Lexical presentation order never supplies chronology.

## Provenance attachment

`join_provenance` uses exact composite identities. Duplicate provenance and unmatched loaded-record identities fail. Missing attachment remains None plus warning, not a fabricated unknown. Absent and supplied-empty manifests remain distinct. Explicit version selection affects coverage only; supplied provenance outside the selected scope must still match the full loaded scope and errors survive.

Three independent unweighted coverage measures use all valid records in the selected scope: matched-row count, matched valid-required-field count, and explicit yes/no grounding count. Numerator, denominator and denominator name remain attached. Unknown is valid enum syntax but not known grounding. Weight does not alter fractions. Empty selected scope fails; generic zero-denominator ratio is None.

Typed incomplete required fields remain ProvenanceAssessment plus errors, never canonical certification. Invalid present types/enums fail. The strict normalizer stays strict; bundle orchestration reuses conversion helpers for eligible incomplete CSV assessments without substituting valid values. Source type, grounding and human review remain independent. Estimated/unknown warnings and explicit strict-promotion settings preserve counts/declarations. Conflicting shared batch_id/timestamps retain both namespaces. Joins never follow parents or source URIs.

## Chronology and dependencies

`resolve_version_order` validates parsed explicit lists, integer ranks, timezone timestamps and optional tie-break/invocation evidence. Every source covers loaded versions and agrees on shared pairs; extra declared versions remain recorded. Rank gaps/negative starting points are allowed, duplicates/conflicts are errors. Equal instants need explicit ties. Empty explicit documents fail. Retained declarations, not cached flags or filename spelling, are authoritative.

`parse_parent_ids` validates native arrays or explicitly CSV-encoded JSON arrays. Null stays null, blank CSV means empty, limits apply before deduplication. `resolve_parent_references` resolves immediate targets only. Bare identifiers require one match; ambiguity fails. Missing targets remain unresolved. Aliases/duplicates collapse deterministically with warnings and retained original spellings. Direct self-parent uses the existing cycle input code without implementing general T6. Declared future targets fail when chronology proves them future, even if unloaded. Same-version graph validation remains deferred.

`validate_generation_declarations` independently establishes expected counts from validated grounding/dependencies. Grounding yes establishes zero including carryovers. Ungrounded children require all parent counts before one plus their maximum. Declared generation never seeds expectation. Missing/unknown/invalid evidence and stalled dependencies retain unavailable reasons; stalling is not called a cycle. Mismatches warn or explicitly promote. Bounded monotone scans use flat indexes and existing version order, without root traversal, depth or topological graph algorithms. Some same-version chains have quadratic worst case; no large-scale performance certification is claimed.

## Content, classification and internal handoff

Content is read only by explicit LOCAL_REF requests through PR-017 containment and UTF-8 checks. See docs/privacy.md for trusted stable filesystem assumptions. Reference-like metadata stays inert.

The bundle returns inventory, records, optional provenance, join evidence, chronology, generation when available, capability classification, mapping evidence, resolved-content identities and diagnostics. It writes no report. Check has_errors independently of maximum level. Content/parent-family failures can coexist with independent valid metadata; fatal structural input errors raise.

Hero input validation qualifies as Level 4 without metric calculation. Model longitudinal remains unavailable. Scenario declarations may establish experimental eligibility without execution. The separately invoked calculation calls below provide approved fields. Phase 4 CLI audit orchestrates these calls and renders reports through the separate report contract. General lineage and ancestry remain deferred. Input/configuration schemas retain their accepted meanings; `report.schema.json` defines the Phase 4 public report.


## Literal field representations

This internal interface creates scoped state assignments after canonical
normalization:

```python
from recursive_integrity_toolkit.config import RepresentationConfig
from recursive_integrity_toolkit.representations.field import assign_field_states

representation = assign_field_states(
    validated_records,
    dataset_versions=("v1",),
    scope_id="v1-topic-audit",
    config=RepresentationConfig(
        name="topic", source="topic_field", field="topic",
        version="declared-topic-taxonomy-v1", missing_value_policy="exclude",
    ),
)
```

Every declaration is explicit, including taxonomy version. Topic and label are
supported; custom upstream columns require prior mapping. State labels preserve
case, whitespace and Unicode spelling. Empty strings surviving normalization are
literal states, distinct from absent fields, null and explicit missing-state IDs.
Labels supply no independent proof of semantics, truth or source independence.

The three policies are error, exclude and explicit_missing_state. The last needs
a separately supplied nonempty missing_state_id and rejects collisions with any
selected observed value, even without missing cells. No serialized config field
is added. Excluded records remain in the audit. A wholly absent configured column
is an error; present all-null columns may yield ALL_EXCLUDED. Empty explicit
input with complete config yields EMPTY_SCOPE, not a zero diversity value.

Fallback requires no explicit config plus allow_fallback=True, fallback_version
and fallback_missing_policy. It selects field presence in topic-then-label order,
records the choice and emits W_REPRESENTATION_FALLBACK. Explicit config wins;
invalid config fails. No per-row substitution, embedding or hashing occurs.

The immutable result retains selection metadata, ordered assignments, source
field states, included/excluded identities and coverage. Coverage uses all
selected_valid_records. Future representation calculations use only
included_representation_records; provenance scope is unchanged. There are no
state-frequency, support, diversity or tail calculations in this interface.
Payload-bearing result fields are hidden from repr; errors retain coordinates
without echoing raw contents or unredacted paths. Inputs are never mutated.

## Exact decoded-content representation

`assign_content_states` and `detect_exact_duplicates` are explicit in-memory calls.
The first returns an `ExactContentRepresentation` whose `.representation` uses the
shared immutable representation result. The second returns the two registered
PR-006 counts and exact duplicate groups. Neither is called by `validate_bundle`.

Both require exactly one `dataset_versions` entry, `scope_id`,
`representation_name`, `representation_version`, `normalization_profile` and a
`ContentMode` enum. The only implemented profile is `exact_utf8_v1`.
The profile encodes the validated decoded text as UTF-8 without changes to case,
Unicode form, whitespace, line endings or BOM. Empty/whitespace-only, NUL-bearing
or unencodable content fails. File-inventory hashing remains a separate operation.

```python
from recursive_integrity_toolkit.metrics.duplicates import detect_exact_duplicates
from recursive_integrity_toolkit.models import ContentMode

result = detect_exact_duplicates(
    canonical_records,
    dataset_versions=("v1",),
    scope_id="v1-exact-record-form",
    representation_name="record_form",
    representation_version="declared-v1",
    normalization_profile="exact_utf8_v1",
    content_mode=ContentMode.INLINE,
)
```

In `LOCAL_REF`, additionally pass `resolved_content={RecordKey(...): loaded_text}`
for exactly the selected keys. The caller explicitly obtains text through the
existing PR-017 reader before this call. Missing/extra payload keys fail, and the
path-valued canonical cell is never used as content in that mode. An INLINE call
rejects payload substitution. A type or metadata declaration cannot prove that a
caller-created string came from a trusted source. No new serialized config key is
introduced; this is an internal call interface.

Equal SHA-256 digests are checked against their exact bytes. Unequal bytes sharing
an artificial digest cause a structured error; no alternate state ID is invented.
Groups are maximal equal-content sets of at least two records. Members are ordered
by canonical RecordKey, groups by digest. The first member is a display
representative, not a retained replacement for the group.

`duplicate_record_count` is the sum of each group size minus one;
`duplicate_group_count` is the number of qualifying groups. Both are unweighted
`observed_fact` values owned by PR-006, with method, unit, scope, representation,
assumptions and limitations. Definitions 8.3/8.4 register these counts without
F-numbers, so `formula_id` remains None. Empty input yields no numeric values and
EMPTY_SCOPE; a nonempty unique scope yields real zero counts.

Exact record form establishes no semantic equivalence, independent origin,
authorship or provenance. No record/provenance is edited, removed or reweighted.
Support/diversity and report assembly use separate explicit APIs. Near-duplicate
analysis and automatic longitudinal grouping are unsupported.

## Mathematical call contracts

These are internal Python result containers. Public report serialization is a separate explicit assembly step under `report.schema.json`. `CalculationScope` supplies selected versions, included/excluded canonical keys, denominator basis and scope ID. Every representation-bound result retains name, source, version and mapping rule. Constructors alone do not certify that a caller's supplied data has the claimed empirical meaning; each kernel validates its own prerequisites.

| Call / result | Input and denominator | Output contract |
|---|---|---|
| `calculate_state_distribution` / `StateDistributionResult` | Included representation records; optional explicit valid record weights | Always an unweighted distribution; a separate weighted companion when requested; retained excluded assignments and coverage |
| `distribution_from_counts` | Explicit nonnegative integer counts consistent with selected scope | Exact counts and F-001 frequencies over the count total |
| `distribution_from_probabilities` | Explicit finite vector with total one within 1e-12 | No invented counts/masses/empirical sample size; supplied total/residual retained |
| `summarize_provenance` / `ProvenanceCompositionResult` | Explicit unweighted single-version audit scope, independent of representation exclusions | Five source categories, four confidence count categories, missing-row inventory, separate coverage and direct classes |
| `direct_closure_exposure` / `DirectClosureExposureBounds` | Full selected scope N; known closed C and unresolved U | F-009 C/N, F-010 (C+U)/N, width U/N, preserved coverage/errors and classification basis |
| `select_tail` / `TailSelectionResult` | Unweighted count-backed distribution; explicit `TailSelectionOptions` | Selected positive states, ordinal ranks, tail support and tail count share |
| `one_step_extinction_probability` | Explicit state marginal p and positive integer resample size n | F-014 (1-p)^n, one-step simulation, analytic method, no invented seed |
| `expected_diversity_after_steps` | Explicit vector, n and horizon | F-015 analytic sequence including t=0; method/underflow disclosure |
| `simulate_closed_resampling` | Explicit vector, n, horizon, seed and replicates | Ordered sampled paths; t=0 has no invented counts; each later generation has integer counts, frequencies, support and diversity |
| `compare_support` / `SupportComparison` | Two distributions, `ExplicitPairContext`, explicit state semantics and optional validated directed map | F-005/F-006/F-018, lost/added/retained state sets and counts; retained original and harmonized distributions |

Weights must be finite, nonnegative and explicitly aligned to canonical record keys. Zero-weight states do not enter weighted positive support; a nonpositive total cannot supply a weighted distribution. Weighted and unweighted values remain distinct. Counts and cardinalities are exact; scalar checks use the fixed absolute/relative 1e-12 policy.

Matched provenance with unavailable required fields retains its original errors and unresolved direct class. Missing rows never become a sixth source category or a confidence value. Explicit unknown remains a valid declaration. Source/grounding/review/confidence are never substituted for each other. A dataset with no usable required provenance yields unavailable bound scalars; explicit valid unknown grounding can support the full [0,1] interval. Confidence counts are not trust scores or weights.

Tail options are `singleton_count`, `count_at_or_below`, `frequency_at_or_below` and `state_list`. Their required threshold/state declarations are explicit. Ranks use frequency, count and Unicode state ID for deterministic ties. Weighted tails and undeclared quantiles remain unsupported.

Scenario results retain `simulation` evidence even for analytically evaluated probabilities or expectations. Only sampled input permits the P3-D07 bounded, disclosed within-tolerance correction; larger mass errors fail. Negative probabilities are never clipped. Sampled calls record PCG64, actual NumPy version, canonical state order and replicate-major/step-major schedule. Resource limits are checked before allocation/RNG creation. Analytic methods have no random seed. Numerical underflow is distinct from model extinction.

The pair context revalidates chronology and representation declarations. Both sides must share weighting/denominator families and compatible state semantics. A complete directed many-to-one map may aggregate the source side; mapping collisions and before/after support sizes remain visible. Empty/unavailable sides propagate unavailability without erasing the individually valid side. This interface performs one caller-selected comparison and makes no automatic temporal, causal or model-performance inference.


## CLI and report handoff

The installed `audit` command accepts one primary records file and at most one
`--compare` file. Each audit side must contain exactly one dataset version. The
comparison side is earlier and the primary side later; explicit chronology and
`--state-semantics` must establish the declared pair. The broader `AuditBundle`
input API can validate more comparison sources without automatically analyzing
them. Neither interface infers chronology from filenames or lexical version order.

CLI field/content-hash representations use the accepted representation config.
CLI output calculations are unweighted, even if row weights exist. Tail selection
accepts `singleton_count`, `count_at_or_below` and `frequency_at_or_below`; the
Python-only `state_list` and directed state-mapping capabilities are not exposed
through CLI flags. Closed-resampling Python functions require explicit invocation,
and the CLI leaves simulations empty. No CLI command enables `LOCAL_REF` reading.

`validate` publishes input-only reports. `audit` passes accepted result objects to
`reports.assembly.assemble_report`, selects `privacy_view`, and publishes the
validated JSON/Markdown pair. Support/diversity may exclude unrepresented rows
under the declared missing-value policy; provenance counts and exposure use their
separately retained full selected scope. Missing, null, declared unknown, false,
zero and unavailable conclusions remain distinct throughout this handoff.

See [CLI options](cli.md), [public field registry](report_schema.md) and
[privacy limits](privacy.md). The Phase 4 report schema is available both at
`schemas/report.schema.json` in the checkout and
`recursive_integrity_toolkit/data/report.schema.json` in installed resources.
