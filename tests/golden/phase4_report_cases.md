# Phase 4 report oracle: independent cases and rationale

Status: authored from frozen authorities and raw inputs before Step 9 candidate
execution or comparison. These internal expectation records are not public audit
reports. Their values are not obtained by running the report implementation.

The source baseline is `63e347a785838b64a9c32e636ea48c664458cee4`.
The companion JSON records SHA-256 hashes of every source used for its derivation,
fixed metadata, input declarations, exact JSON-pointer assertions, and executable
case identifiers. A failed comparison does not authorize replacing an expectation
with the observed value. Resolve a discrepancy against the cited authority, retain
the original failed attempt, and record any approved correction.

The author previously reviewed Phase 4 Step 8 outputs. For this Step 9 oracle the
author used the frozen field registry, model contracts, canonical raw CSV rows and
independent arithmetic, without reopening or copying emitted reports. A separately
delegated assistant recomputed raw Hero counts and exact fractions without viewing
production calculations or generated output. This is consolidated assistant
technical review; it is not independent human mathematical certification.

## Authority and scope

`PHASE_4_PLAN.md` P4-D01/D02/D03/D05/D06/D08 and sections 4, 8, and Step 9 control
phase boundaries, fields, privacy, exit statuses and independent expectations.
`docs/report_schema.md` and `schemas/report.schema.json` fix public envelope paths,
units, evidence classes, null rules and capability semantics. The unchanged
`examples/hero/EXPECTED_OUTPUTS.md` and `tests/golden/phase3_math_cases.*` supply the
already approved numeric anchors. Synthetic case expectations below are separately
authored derivations; no Phase 3 oracle bytes or values change.

All original twenty mathematical cases must still execute unchanged. The new report
cases complement those tests; a grouped vector of assertions is not a replacement
for any original mathematical test identity.

## Hand calculation of the Hero

v1 contains eight records with distinct topics battery, bird, cat, dog, fish,
lizard, refund and turtle. Each empirical frequency is 1/8. F-002 support is 8;
F-004 concentration is 8/64=1/8; F-003 diversity is 1-1/8=7/8.

v2 contains cat three times, dog twice, and bird, fish and refund once each.
Frequencies are 3/8, 2/8, 1/8, 1/8, 1/8. Its support is 5, concentration is
(9+4+1+1+1)/64=1/4 and diversity is 3/4. The original positive supports lose
battery, lizard and turtle in Unicode order, add no state, and retain five states.
The explicitly declared v1-to-v2 pair therefore has F-005 delta 5-8=-3,
F-006 retention 5/8, and F-018 diversity delta 3/4-7/8=-1/8.

The analytical provenance scope is v2's eight records. All eight have matching,
valid required provenance; all eight grounding cells are yes or no. Row,
required-field and known-grounding coverage are each 8/8. Four records declare
human/yes and four synthetic/no. Source shares use all eight records: human=1/2,
synthetic=1/2, mixed=sensor=unknown=missing=0. There are four known-open, four
known-closed and zero unresolved records. F-009/F-010 direct bounds are
[4/8,(4+0)/8]=[1/2,1/2], width zero. These declarations do not establish factual
truth, source independence or confidence probabilities.

The full input inventory contains sixteen records and sixteen provenance rows.
Its coverage/capability basis is distinct from the v2-only analytic denominator.
The eight v2 parent declarations all resolve to earlier v1 identities. The retained
observations may state 8 declared, 8 resolved and 0 unresolved references and the
sufficient declared-earlier-version ordering certificate. They cannot claim graph
traversal or a general cycle verdict.

Maximum input observability stays Level 4. Lineage execution is not requested;
dataset-longitudinal execution is partial with the sole explicit-pair support and
diversity operation identified. The successful run remains complete. Model
longitudinal is unavailable/deferred, default intervention simulation is
unavailable/not_requested, and simulations is empty.

The frozen future-product lineage bounds [0,0], external-root count5, top root
incidence3, ancestry HHI1/4 and effective roots4 are not Phase 4 calculated values.
Registered lineage scalar placeholders must be unavailable/null with reasons;
fields that the assembler omits must stay absent. No shared-ancestry proxy may be
emitted. Required unavailable conclusions include model-performance decline,
causal ancestor effect, universal integrity and universal collapse prediction.

## Envelopes, denominators and render parity

The companion JSON asserts substantive registered paths, not only bare numerical
values. Counts and provenance coverage are observed_fact. Support, computed
frequencies, diversity and direct bounds are derived_metric. Support contraction
is proxy_signal with status available and level present. Schema reconciliation
explicitly separates a proxy's availability status from its present/not_present
level. An unavailable conclusion has unavailable_conclusion class and unavailable
status, blocking evidence and next metadata. Any supplied scenario would remain
simulation/experimental, although none runs by default here.

A representation-dependent available value retains its literal representation,
version, scope count, exclusions, denominator, method ID and unit. v1 and v2
single-version denominators are eight. Provenance uses the complete selected
version even when topic rows are excluded. Coverage and denominator nulls require
reasons; unavailable scalar value=null requires nonempty reason_codes and
required_evidence. Null never becomes zero, an interval midpoint, an authenticated
human source, or a stronger capability. A singleton's measured diversity zero is
available and remains distinguishable from unavailable empty/all-excluded scopes.

Every emitted report preserves the twelve JSON sections in registered order,
including empty objects/arrays, and an exactly equal observability capability
mirror. Markdown begins with the registered title and the twelve prescribed
headings. Its displayed values, classes, units, statuses, denominators, reasons,
errors and deferred work must agree with JSON. Raw caller labels appear as escaped
literal data and cannot introduce headings, HTML or display controls. A name in an
unavailable conclusion is permitted; affirmative universal or causal scores are
forbidden. Check semantic analytical placement rather than rejecting every textual
occurrence of a safeguard's name.

## Determinism and permitted normalization

Literal fixtures inject run_id `phase4-step9-golden`, start and completion
`2000-01-01T00:00:00+00:00`, duration0.0, python_version `3.test`, and platform
`golden-test`. These are explicit test measurements, not claims about real timing.
The test-only injected secret is the 34-byte UTF-8 string
`phase4-step9-fixed-test-key-000000`; it is never a product default or production
credential. Redacted identifiers retain HMAC-SHA-256 and run stability. No secret
bytes, secret path or reversible mapping appears in a report or diagnostic.

Only the six exact run paths listed in the JSON and explicitly enumerated test-root
path prefixes may normalize. The config hash is first independently checked against
the complete declared resolved meaning, excluding only approved secret material.
For stable fixture comparison an independent declaration encoder can replace exact
test-root prefixes in input/output path slots and hash that declared configuration.
This does not authorize recursively changing report values or copying an expected
hash. Input SHA-256 hashes always cover actual supplied bytes. Row reversal must
therefore change affected hashes even while all analytical aggregates remain equal.

Metrics, scope membership/counts, denominators, evidence classes, availability,
reason text/codes, warnings, errors, semantics, unavailable conclusions and all
nonpath configuration meaning are substantive. No wildcard rule may normalize every
id/value or erase arbitrary fields. Negative normalization tests must reject these
changes. Literal JSON and Markdown candidate files require per-field and human
reading review against these expectations before acceptance.

## Execution and adversarial cases

The companion JSON contains concrete input files and argv for generic CLI cases.
`{root}` is a test-owned temporary root, not an inferred production path. JSONL
rows retain authored order and data types. Text files preserve exact authored
bytes. `expected` is an RFC6901 JSON-pointer map of exact literals, with the inherited
1e-12 absolute/relative scalar tolerance. `absent_paths`, `nonempty_paths`, required
error/warning codes, unavailable conclusions and leakage tokens add independent
checks. Negative canonical cases use only the named mutation against the reviewed
Hero fixture; nonfinite markers instruct the test to supply the named IEEE value.
Their expected exception is a rejection, not an emitted report.

Every case ID must execute. Hero row reordering uses the same raw CSV rows with
headers retained. Installed execution uses the installed wheel from outside the
checkout and blocks optional PyArrow. CLI and API case drivers must block toolkit
network paths on success and failure, checking socket/DNS/URL sentinels separately
from the reported toolkit-managed count. Output failures retain prior target bytes
and never count a missing/error-only artifact as a successful publication.

### hero_normal

Driver: `hero_normal`. Expected exit: `0`.

Eight unique v1 topics give support 8 and D=1-8*(1/8)^2=7/8.

v2 topic counts cat=3,dog=2,bird=fish=refund=1 give support 5; sum squared frequencies=16/64=1/4 and D=3/4.

Earlier minus later is battery,lizard,turtle; intersection contains five states. Delta=5-8=-3, retention=5/8, diversity delta=3/4-7/8=-1/8.

The selected v2 scope has eight matching valid provenance rows: four human/yes and four synthetic/no. Each coverage is 8/8; each nonzero source share is 4/8. Direct interval=(closed/N,(closed+unresolved)/N)=[4/8,4/8].

All eight supplied v2 parent references resolve to explicitly earlier v1 records. This supports reference counts and a declared-order certificate only. This CLI invocation does not request graph traversal or ancestry metrics.

### hero_redacted

Driver: `hero_redacted`. Expected exit: `0`.

Apply identifier protection after calculation. Every aggregate, denominator, status and evidence class retains the hero_normal value; identity fields use the fixed test key.

### hero_row_reordered

Driver: `hero_reordered`. Expected exit: `0`.

A bijective row permutation preserves records, counts, selected ordered versions and every statistic. Input byte hashes must be recomputed from the permuted files and are expected to differ; do not normalize those hashes.

### records_only_missing_representation

Driver: `cli`. Expected exit: `0`.

No representation is declared. Four valid records support inventory evidence, but no state assignment or topic/hash fallback is authorized.

### no_provenance

Driver: `cli`. Expected exit: `0`.

A,A,B,C gives support3 and D=1-(4+1+1)/16=5/8.

No matching rows gives row coverage0, missing share1, explicit unknown source count0. Dataset-facing direct bounds are unavailable because no usable required-provenance row exists; the distinct explicit count-envelope API is not invoked.

Required retained warnings: `W_PROVENANCE_MISSING_ROW`.

### matched_missing_and_unknown_provenance

Driver: `cli`. Expected exit: `0`.

Four selected records have human/yes, synthetic/no, unknown/unknown, and one missing row. Matching and valid required rows=3, resolved grounding=2. Distinct coverage denominators all retain4.

One closed and two unresolved records give [1/4,3/4], width1/2. Each declared nonzero category and missing share is1/4. Unknown source remains separate from absence.

Required retained warnings: `W_PROVENANCE_MISSING_ROW`, `W_GROUNDING_UNKNOWN`.

### invalid_required_provenance_retains_content

Driver: `cli`. Expected exit: `1`.

All four identities match; s3 lacks required source_type. Row coverage1 differs from required coverage3/4. Three grounding cells are yes/no, giving field coverage3/4 independently of validity of the complete row.

Invalid required provenance cannot erase A,A,B,C content metrics, turn s3 into human/unknown source, or remove its error.

The fully usable rows supply one open, one closed and one explicitly unknown record; the incomplete source-type row is unresolved. Thus direct bounds are [1/4,(1+2)/4]=[1/4,3/4]. Its supplied no cell does not override the incomplete-row boundary.

Required retained errors: `E_SCHEMA_REQUIRED_FIELD`.

### valid_unknown_grounding

Driver: `cli`. Expected exit: `0`.

Four valid rows explicitly declare unknown grounding. Required coverage1 permits [0/4,4/4]; no source category or confidence declaration imputes grounding. This differs from no_provenance, whose dataset-facing bounds are null.

Required retained warnings: `W_GROUNDING_UNKNOWN`.

### empty_records

Driver: `cli`. Expected exit: `1`.

Zero input rows fail ingestion. No version, distribution, zero diversity or zero direct interval may be invented.

Required retained errors: `E_EMPTY_DATASET`.

### all_representation_values_excluded

Driver: `cli`. Expected exit: `0`.

Explicit exclude policy excludes four missing topic values; included representation scope0, excluded4, so support/diversity are unavailable with R_CALC_ALL_EXCLUDED.

Provenance retains the original four-record scope and matching coverage3/4. Representation exclusion never narrows its denominator.

### singleton_scope

Driver: `cli`. Expected exit: `0`.

One positive state among one included record: K=1, concentration1, diversity1-1=0. This zero is an available result, not missing evidence.

### missing_pair_chronology

Driver: `cli`. Expected exit: `1`.

Each side independently has two distinct states and D=1/2. An explicit pair requires a supplied order consistent with earlier then later. No pair value or contraction signal follows from missing/reversed chronology.

### reversed_pair_chronology

Driver: `cli`. Expected exit: `1`.

Each side independently has two distinct states and D=1/2. An explicit pair requires a supplied order consistent with earlier then later. No pair value or contraction signal follows from missing/reversed chronology.

### pair_missing_representation

Driver: `cli`. Expected exit: `1`.

Declared order cannot replace a declared representation. Preserve four validated input records and fail the requested pair.

### contradictory_state_meanings

Driver: `cli`. Expected exit: `2`.

The bounded CLI accepts one shared literal meaning and does not authorize arbitrary compatibility declarations. Conflicting configured meanings are invalid invocation/configuration, never inferred compatible.

Required retained errors: `E_CONFIG_INVALID`.

### requested_unsupported_simulation

Driver: `cli`. Expected exit: `2`.

Simulation activation is explicitly unsupported by this CLI stage. A request must return configuration exit2; the default unrequested Hero is complete with an empty simulations section. No experimental result is fabricated.

Required retained errors: `E_CONFIG_INVALID`.

### partial_parent_validation

Driver: `cli`. Expected exit: `0`.

Of two later parent references one resolves and one is absent: 2 declared,1 resolved,1 unresolved. Missing references retain a warning and cannot become external roots. One valid resolved path and one unresolved reference give partial input capability under the frozen lineage classification; execution is not requested.

Independent ordered supports {A,B} and {A,C} both have size2, intersection1, retention1/2; lineage execution is not requested.

Required retained warnings: `W_PARENT_UNRESOLVED`.

### invalid_parent_retains_independent_metrics

Driver: `cli`. Expected exit: `3`.

An explicit self-parent violates existing parent validation and gives lineage-family exit3. Later content still has K2,D1/2 and dataset observability remains4. No Phase5 graph traversal is invoked.

Required retained errors: `E_LINEAGE_CYCLE`.

### malformed_records

Driver: `cli`. Expected exit: `1`.

Invalid JSONL syntax is a known input parse failure. Safe diagnostics must not echo the offending bytes.

Required retained errors: `E_FILE_PARSE`.

### malformed_config_duplicate_key

Driver: `cli`. Expected exit: `2`.

Duplicate singleton configuration keys cannot select a winner silently. Reject as exit2 before analysis.

Required retained errors: `E_CONFIG_INVALID`.

### unsafe_mapping

Driver: `cli`. Expected exit: `1`.

Only the approved finite mapping operation vocabulary may execute. An executable Python transform fails schema-mapping input validation with E_MAPPING_UNSAFE_TRANSFORM and exit1; its payload must never be executed or printed. Unsupported CLI activation/configuration remains the separate exit2 class.

Required retained errors: `E_MAPPING_UNSAFE_TRANSFORM`.

### duplicate_record_identity

Driver: `cli`. Expected exit: `1`.

Two records with the same (dataset_version,record_id) are invalid even when their raw content differs. No silently deduplicated support result is allowed.

Required retained errors: `E_RECORD_DUPLICATE_ID`.

### output_collision

Driver: `cli`. Expected exit: `1`.

Publication cannot overwrite an existing report target. Leave its bytes unchanged, publish no peer report and return output-I/O exit1.

### output_missing_parent

Driver: `cli`. Expected exit: `1`.

Only the resolved output leaf may be created; a nonexistent parent is an I/O failure. No success path or fabricated report is announced.

### hostile_label_control_characters

Driver: `cli`. Expected exit: `0`.

The hostile topic is a literal state distinct from ordinary: K2,D1/2. Markdown must encode control/markup characters as literal JSON data, preserving value meaning and the twelve section boundaries.

### redacted_nested_error

Driver: `cli`. Expected exit: `1`.

The first provenance row lacks required confidence. Retain the error and usable four-state content metrics while protecting version, record, state, scope and nested diagnostic identities in JSON, Markdown, stdout and stderr.

Required retained errors: `E_SCHEMA_REQUIRED_FIELD`.

### nonfinite_supplied_result_nan

Driver: `canonical_rejection`. Expected rejection: `ValueError`.

The canonical report accepts only finite JSON numbers. Reject the supplied nonfinite result without rounding, replacement or rendering.

### nonfinite_supplied_result_positive_infinity

Driver: `canonical_rejection`. Expected rejection: `ValueError`.

The canonical report accepts only finite JSON numbers. Reject the supplied nonfinite result without rounding, replacement or rendering.

### nonfinite_supplied_result_negative_infinity

Driver: `canonical_rejection`. Expected rejection: `ValueError`.

The canonical report accepts only finite JSON numbers. Reject the supplied nonfinite result without rounding, replacement or rendering.

### corrupted_capability_mirror

Driver: `canonical_rejection`. Expected rejection: `ValueError`.

The compatibility mirror must be exactly equal to the canonical matrix. Also, completed lineage analysis is beyond Phase4. Reject the mutation before serialization.

### incompatible_representation

Driver: `pair_api_rejection`. Expected rejection: `CanonicalValidationError`.

The CLI only accepts one shared representation, so distinct declared versions exercise the accepted explicit-pair API boundary. Each independent two-state distribution has D1/2, but no compatible pair exists without an approved harmonization declaration.

### installed_without_pyarrow

Driver: `installed_hero`. Expected exit: `0`.

The packaged CSV/JSON Hero needs core dependencies only. The installed command must retain all Hero values and both reports when optional PyArrow is absent.

## Acceptance boundary

The two independent oracle files are frozen before candidate generation and their
SHA-256 values are recorded separately in execution evidence. Generation writes to
an explicitly requested scratch destination and cannot overwrite accepted fixtures.
Acceptance requires every case, unchanged original math cases, literal JSON and
Markdown review, normalization mutation rejection, privacy/format/reordering
metamorphic checks and the governing regression gates. This oracle alone makes no
claim that current implementation, installed artifacts or remote jobs have passed.

## Phase 5 Step 7 current-schema consolidation

Current canonical fixtures use report schema 1.1 and package 0.1.0.dev4.
Ordinary CLI calls report lineage execution as `not_requested`; explicit lineage
report assembly is covered by the current integration suite. Original numeric
expectations are retained. Prior schema 1.0 fixtures and the original authority
hashes remain auditable in Git history. No source-binding migration is added.
