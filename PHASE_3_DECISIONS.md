# PHASE_3_DECISIONS

## Approval record

Theory Owner: Xiangyu Guo. Approval date: 2026-09-17. The user approved PHASE_3_PLAN.md without exceptions and explicitly instructed Phase 3 Step 1. P3-D01 through P3-D10 are adopted. No later step, main merge, tag or publication is authorized.

Approved plan SHA-256: `e1c9a6776e3cd2511d37a6bbbdb4a9d5a33b66ff6b00bc00bf3e08a01e6576f1`.
Accepted Phase 2 commit: `78554993febb01609cb90814cc24cce2012bf7d7`.
Work branch: `phase3-metrics`, created from that exact commit.

The plan is stored byte-for-byte, including its historical draft/pending wording. This subsequent approval record determines its adopted status. No frozen Phase 0 specification or approval hash is rewritten.

## Adopted interpretations

The complete text of each decision remains in approved plan section 3. The following records its adoption and effect; it does not replace the authoritative wording.

| Decision | Status | Adopted effect |
|---|---|---|
| P3-D01 | APPROVED | T4/T6, roots/ancestor sets, HHI, effective roots, lineage closure and general graph validity remain Phase 5. Existing immediate-reference/generation validation is preserved. |
| P3-D02 | APPROVED | Later Phase 3 Step 8 implements only explicitly invoked finite closed-resampling kernels. T5, external-reference loss, reopening distributions and experimental orchestration remain Phase 6B. Default validation never runs simulation. |
| P3-D03 | APPROVED | Later Step 9 permits pure explicit ordered-pair kernels with validated compatible representations. Automatic longitudinal selection/dispatch and trajectories remain Phase 6A. |
| P3-D04 | APPROVED | Analytic extinction and expected contraction carry simulation as their primary evidence class. Their analytic method is separate from sampled paths; analytic methods have no invented seed. |
| P3-D05 | APPROVED | exact_utf8_v1 means UTF-8 of already validated text with no additional trim, case/Unicode normalization, whitespace or newline rewriting. Paths are not content. |
| P3-D06 | APPROVED | Explicit missing-state mode requires a caller-supplied collision-checked ID. Tail modes are singleton_count, count_at_or_below, frequency_at_or_below and state_list. No invented missing token, weighted tail, quantile or near-duplicate mode. |
| P3-D07 | APPROVED | Exact counts; finite numerical values; scalar atol/rtol 1e-12; mass tolerance 1e-12. Later sampled kernels use explicit PCG64 and seed. Only approved bounded disclosed roundoff correction is allowed; Step 1 performs none. |
| P3-D08 | APPROVED | Incomplete provenance cannot supply stronger direct classes or an invented public composition bucket. Retain original errors and distinct validation coverage. Valid estimated declarations are not silently discounted. |
| P3-D09 | APPROVED | Use the exact common maintenance set and current-step allowlists. Preserve earlier behavioral/security guarantees, baseline hashes and exact restoration tests. A shared file never authorizes all its later owners. |
| P3-D10 | APPROVED | Keep 0.1.0.dev1 for intermediate work. The proposed dev2 bump is confined to final Step 11. Identify actual review roles without inventing independent reviewers. |

## Actual reviewer roles

The user is the Theory Owner and approved the plan. The assistant performs the technical implementation review, mathematical-target transcription review and security-boundary review with roles consolidated under the existing governance allowance. No independent human mathematical/security reviewer or independent certification is claimed. Automated checks supply execution evidence, not human sign-off. Mathematical implementations have not started.

## Step 1 contracts

All new runtime types are immutable project-owned declarations in models.py. Existing Phase 2 definitions remain unchanged. Constructors check supplied types, ranges, disjoint membership and explicit metadata; they do not assign states, calculate metrics, verify empirical meaning, create an RNG, read data or certify completed analysis.

| Contract | Purpose | Owners |
|---|---|---|
| CalculationEvidenceClass, CalculationStatus | Explicit evidence/status vocabulary for future calculation records | T1/T2/T3, PR-005/006 supporting |
| CalculationReason | Ten documented unavailable reasons, separate from existing validation/observability registries | Supporting contracts |
| NumericalPolicy | Fixed approved scalar and mass tolerances | PR-016, P3-D07 |
| RepresentationDescriptor | Name, source, version and binning/mapping rule plus explicitly selected field/profile/missing policy | T1 input basis, PR-006 |
| RecordStateAssignment | Supplied canonical identity and a supplied state or explicit exclusion reason; no assignment execution | T1 input basis |
| CalculationScope | Explicit versions, included/excluded canonical keys and named denominator/scope identity | T1/T3, PR-004/005 |
| WeightingOptions | Unweighted default; weighted requires the explicit canonical weight field | T1, PR-005/016 |
| TailSelectionOptions | Four typed rule declarations; no tail selection or ranking | T2 |
| CalculationMetadata | Name, owner/formula ID, unit, method, evidence, scope, representation, weighting, assumptions and limits | Supporting traceability |
| ScalarCalculation | Already supplied finite scalar, or None and an unavailable reason; never a calculated answer | Supporting result metadata |
| ExplicitPairContext | Both scopes, both descriptors and retained VersionOrderResult; later compatibility validation required | T1, PR-007/011 |
| ClosedResamplingMetadata | Method, explicit n/horizon/state order/assumptions and sampled-only RNG/seed/replicate metadata | T1/T2, PR-016 |

Internal method names are analytic_expectation, analytic_extinction and sampled_path. The closed model name is closed_resampling. A future sampled call uses numpy.random.Generator(PCG64), records its actual NumPy version, and uses replicate_major_step_major scheduling with one explicit generator per call and canonical state ordering. No generator or probability correction runs in this step. The selected representation profile is exact_utf8_v1. No serialized run-config field, public report schema or CLI command is added.

These containers do not authenticate their metadata. Future kernels must check actual prerequisites and map every implemented numeric field to the original registry; a caller-created ScalarCalculation is not a verified result. Record weights, probability vectors, content-profile bytes, missing-state collisions and pair semantics remain unimplemented owner checks for their approved later steps.

### Unavailable reason registry

| Code | Meaning |
|---|---|
| R_CALC_EMPTY_SCOPE | No eligible records in the selected calculation scope. |
| R_CALC_ALL_EXCLUDED | A nonempty requested scope has no included representation records. |
| R_CALC_REPRESENTATION_MISSING | Required representation declaration or evidence is absent. |
| R_CALC_REPRESENTATION_INCOMPATIBLE | An explicit pair does not establish compatible state meaning. |
| R_CALC_ORDER_MISSING | Required chronology is not established. |
| R_CALC_PROVENANCE_FIELD_UNAVAILABLE | A matched source/confidence field cannot support the approved complete partition. |
| R_CALC_WEIGHT_BASIS_INVALID | Explicit weighted calculation lacks valid weight evidence. |
| R_CALC_NUMERICAL_INPUT_INVALID | A numerical input violates its declared domain. |
| R_CALC_UNSUPPORTED_OPTION | The requested option is excluded or undefined. |
| R_CALC_CONTENT_UNAVAILABLE | Explicit validated text is unavailable for record-form calculation. |

Reasons do not replace fatal-input exceptions or silently clear retained Phase 2 errors. Zero is a real value; unavailable carries no value.

## Independent mathematical targets

The golden JSON and its companion note transcribe approved plan section 8, with exact rational strings, source sections, owner/formula IDs and tolerances. No future implementation is run to generate its own expected outputs. Their Step 1 checks validate the fixture's structure and authored literals only. Later mathematical tests will separately establish implemented correctness. No T4/T5/T6, lineage bound, report or universal score target is executed.

## Immutable baseline and inherited tests

PHASE_3_BASELINE.json pins the exact final Phase 2 commit, root Git tree, test tree, all sixteen approval SHA-256 values and exact Step 1 path union. This Merkle-tree identity freezes each original filename, mode and blob. The baseline-evidence command materializes all 197 per-file SHA-256/blob identities and every baseline/current test node ID into retained execution evidence.

Baseline collection uses an isolated copy of the immutable original Git objects, never edited current tests. In core mode it must collect 1159 original tests; in real-Parquet mode 1162. All inherited identities must be present in current collection. The original tree and resulting baseline-node digest must not advance with later stages. Independent gate constants reject a forged manifest that changes the stage, baseline, decisions or file scope.

### Stage-assertion migration

No inherited test is deleted, skipped, xfailed or filtered from the full suite. Existing identities remain. Two stale assertions in tests/integration/test_ci_workflows.py are synchronized:

| Inherited identity | Stage-only adjustment | Guarantee retained |
|---|---|---|
| test_phase2_delivery_builds_both_formats_and_tests_installed_wheel | Expect a Step 1 candidate archive/log names and --candidate rather than Phase 2 final-delivery names. | Both builds, strict metadata checks, offline installed-wheel validation, checksums, retained logs, no publication. |
| test_workflows_preserve_phase_boundary | Additionally require explicit --phase 3 --step 1 dispatch. | All original forbidden workflow terms, imports and no-network checks remain. |

All original no-algorithm negative tests remain. The checker adds exact new contract definitions and a restricted operation check; all 26 deferred modules still require docstring-only bodies. No metrics are authorized in this step. The historical validation-plan restoration helper and all eight mutation tests remain exact, and its exception is not placed in the Phase 3 path allowlist.

## Build and stop

The current candidate workflow builds and installs the development package, tests the existing input-only Hero and archives a byte-verified Step 1 snapshot plus actual test evidence. It cannot generate final Phase 3 completion reports, call final delivery, publish a package, create a tag or merge main. The Phase 2 records remain historical and unchanged. Stop after Step 1 acceptance and wait for an explicit Step 2 instruction.


## Step 2 authorization and contracts

The Theory Owner explicitly instructed Phase 3 Step 2 and subsequently approved
the single-file exception for `tests/unit/test_phase3_contracts.py`. That exception
changes only `control[key]=2` to `control[key]+=1` in the forged-stage negative
test. The exact byte transition is enforced by the release checker. Test names,
parameterization, numerical expectations and other assertions are retained.

The accepted previous checkpoint is commit
`20487e356239d5b5642b6fff595b381d0faa2a4e`, tree
`7d9867fb7543bfd50a9b01bb48530a3411121d31`. The original Phase 2 root/test trees,
source hashes and inherited test identities remain frozen. The cumulative diff
is checked against Phase 2 and the incremental diff against Step 1. All previous
Step 1 test identities must also remain collected in both optional-input modes.

`representations/base.py` defines a static typing protocol, immutable selection
and assignment-result containers, and pure canonical scope validation.
`representations/field.py` implements `select_field_representation` and
`assign_field_states`. No user callback, plugin or representation code is run.
The only reused input-layer function is the existing pure canonical validator.

The caller explicitly selects versions and a scope ID. Multiple versions are
pooled only when explicitly named. Identity ordering is deterministic, included
and excluded keys remain separate, and coverage uses `selected_valid_records`.
The future representation denominator is `included_representation_records`.
Unselected records and the full provenance audit scope remain unchanged.

An explicit RepresentationConfig supplies name, supported source, canonical
field, taxonomy version and missing policy, and takes precedence over optional
fallback. Only topic/label and their field-source declarations are supported.
Custom upstream columns require prior mapping. No taxonomy version is invented.
Invalid explicit configuration blocks rather than silently selecting another mode.

Fallback requires explicit activation, a fallback version and a missing policy.
Presence of a field in the selected scope determines the first available entry
in topic-then-label order. The choice records considered fields and emits
W_REPRESENTATION_FALLBACK. No per-record or quality-driven substitution occurs.
A wholly absent configured column in nonempty input is a schema error; a present
all-null column can yield ALL_EXCLUDED.

The rule is literal_field_value. Case, whitespace and Unicode forms are preserved.
Absent, null and literal unknown stay distinct. Canonical empty strings remain
literal states as required by plan section 5.2. The in-scope RecordStateAssignment
constructor now permits these empty strings, while nonempty metadata/missing-ID,
NUL/type and contradictory exclusion checks remain intact. No Phase 2 parsing,
normalization or conservative input-capability behavior has changed.

The three missing policies are implemented. Error blocks missing cells. Exclude
retains explicit no-state assignments and exclusion reasons. Explicit missing
state requires a separate nonempty ID and rejects exact collisions anywhere in
the selected scope, even when no cell needs filling. Empty and all-excluded inputs
carry their existing reason codes. No numerical diversity value is fabricated.

### Step 2 boundary maintenance and reviews

The existing placeholder test identities now admit exactly the two field modules;
24 other modules remain docstring-only, within the unchanged forty-module layout.
Exact function, class, import-symbol, call and operation checks reject unauthorized
code. Additional negative tests cover hidden mathematics, file/network access,
callbacks, new paths and widening the single-file exception. Historical Phase 2
restoration tests are unchanged.

All four workflows identify Step 2 and preserve read-only permissions, full core
and real-Parquet regression, failed-command propagation, original logs and JUnit.
Build output is only an intermediate Step 2 candidate. Technical and security
review remains consolidated in the assistant, with Theory Owner approvals; no
independent human review or security certification is asserted.

No state frequencies, support, diversity, content hashing, tail calculation,
weighted calculation, sampling, pair comparison, graph or report is implemented.
Stop after Step 2 verification. Step 3, main merge and publication are not authorized.

## Phase 3 Step 3 authorization and implementation contract

The Theory Owner accepted Step 2 and explicitly instructed Phase 3 Step 3 in the
project conversation on 2026-09-17. The accepted Step 2 commit is
`9e5d4c4f38834c42a5b7c19de4e67f471ab9bbca`, tree
`096e038145bced4b01f2c0059659082a72501112`. The original Phase 2 baseline,
Step 1 anchor, sixteen source hashes, approved plan and mathematical oracle
remain frozen. The Step 2 single-expression exception remains historical;
no further edit to `tests/unit/test_phase3_contracts.py` is authorized here.

### Recorded before implementation

PR-006 uses `exact_utf8_v1`: UTF-8 bytes of validated decoded text with no trim,
casefold, Unicode normalization, whitespace collapse, newline rewrite or BOM
removal. Whitespace-only, empty, NUL-bearing and unencodable text is invalid,
consistent with required content and the safe content reader. Validation does
not alter valid text. State IDs are lowercase SHA-256 hex from the unchanged
`utils/hashing.py` helper. File inventory hashes remain separate.

The two explicit entry points are `assign_content_states` in the representation
module and `detect_exact_duplicates` in the metric module. They take canonical
rows, exactly one selected version, a named scope, explicit representation name,
version, profile and content mode. No implicit cross-version grouping is selected.
The duplicate entry point delegates to the pure representation implementation;
it accepts no caller-supplied digest or unchecked result as certified equality.

INLINE hashes the literal content value. LOCAL_REF requires an explicitly supplied
plain record-key-to-text mapping for exactly the selected records. A path alone,
missing payload, extra payload identity or ambiguous composite identity fails.
No path is opened, guessed or hashed in LOCAL_REF. The caller obtains text through
the existing PR-017 safe reader; the representation layer does not certify the
origin of arbitrary in-memory text. Missing content is an error, never a synthetic
missing-content state. Empty explicitly selected input returns unavailable with
EMPTY_SCOPE and no numeric counts; a nonempty scope without duplicates returns
real zero counts. No new serialized config keys or reason enums are introduced.

Before grouping, equal digests are checked against the exact normalized bytes.
An artificial digest collision between different bytes fails with the existing
SCHEMA_TYPE error. It does not create a suffixed state ID, merge unequal text or
change the declared representation. This records the fail-closed collision rule
per plan section 5.3 before its implementation.

Groups contain at least two canonical record keys, ordered by RecordKey; groups
are ordered by ascending digest. The first member is a presentation representative
only. `duplicate_record_count` sums group size minus one;
`duplicate_group_count` counts qualifying groups. Both use PR-006,
`observed_fact`, unweighted metadata, named units and the selected scope.
These definitions have no registered F-number; formula_id is None with explicit
method and source sections DEFINITIONS_AND_UNITS 8.3/8.4. No new F-ID is invented.

Raw bytes and state/member IDs are hidden from default repr where applicable.
Nothing logs, writes or returns source notes/provenance as duplicate evidence.
Explicit inspection of internal objects is not anonymization; content digests
remain linkable. No report redaction or PR-015 implementation is claimed.

### Gate migrations

Advance the active stage to 3 and allow exactly content_hash.py and duplicates.py
in addition to previously opened modules. Keep field/base behavior byte-identical,
all other metric/graph/report modules protected, and exact imports/call families
checked. Change the former PR-006 placeholder test in place to owner/import and
implemented-boundary checks; retain its historical node ID. The general placeholder
count becomes 22. Add negative injections and runtime no-I/O tests. Update workflow
stage arguments and artifact names without removing any safety/regression checks.
Freeze Step 2 source and test identities alongside Phase 2 and Step 1; previous
Step 2 tests and the exact historical exception remain preserved. No new scope
exception is requested. No main merge, publication, Step 4 or final phase completion.

### Review roles

Theory decisions: Theory Owner approval already recorded above and in P3-D05.
Implementation, numerical-definition, privacy and boundary review: assistant
self-review plus executable tests. No independent reviewer sign-off is claimed.

## Phase 3 Step 4 authorization and implementation contract

The Theory Owner explicitly requested Phase 3 Step 4 after accepting Step 3.
The prior checkpoint is `d2651ca755c82af2e2fec3963bcb6fe270a23be6`, tree
`7871e6253d770d1561d9f732dd5c0b0f842a4138`. Original Phase 2 authority,
approved plan bytes, P3-D01 through P3-D10 and all mathematical oracles remain
unchanged. This section authorizes only the current step, not Step 5.

### Single-scope calculation contract

The only runtime module opened is `metrics/diversity.py`. Its explicit entry
points are `calculate_state_distribution`, `distribution_from_counts` and
`distribution_from_probabilities`. The first consumes a structurally revalidated
RepresentationResult for exactly one selected version. The count entry point
requires nonnegative strict integers whose positive total matches the included
record denominator. The supplied-vector entry point preserves explicit
probabilities without inventing record counts or claiming to have computed
empirical frequencies. It therefore does not attach F-001 to those supplied
values. F-002, F-003 and F-004 remain separate derived results.

Every calculated scalar retains its T1 owner, formula ID, units, method, scope,
representation, weighting, assumptions and limitations. Literal state identities
including canonical empty strings remain distinct. Explicit zero components
stay in the state table but do not enlarge positive support. Empty/all-excluded
representation scopes return unavailable values and reasons, not a fabricated
zero diversity. Malformed explicit empty or zero-total distributions fail.

Weighting requires `WeightingOptions("weighted", "weight")` plus a plain map
covering exactly the included canonical record keys. Weighted results accompany
an unchanged unweighted result. Confidence is never converted into weights.
Excluded records remain in the original input and provenance scope. Missing or
extra keys, booleans, negative/nonfinite weights, a nonempty all-zero basis,
finite-sum overflow and positive-mass frequency underflow fail explicitly.
No sample size is inferred from weight mass.

Counts are exact integers. Frequencies and moments use binary64 arithmetic,
with deterministic state/record ordering and math.fsum for float totals and
Simpson moments. Components are checked before the approved absolute mass
tolerance of 1e-12. Accepted totals and residuals are disclosed without clipping,
normalization, smoothing or repair. A tiny positive component remains in support
even when finite-precision cancellation rounds diversity to zero. No random
sampling, Shannon entropy or functional-failure inference is performed.

### Step 4 gate and test migrations

The inherited support/diversity owner tests retain their original node IDs.
Their whole-module-placeholder assertion is replaced by the implemented formula
boundary and later-function prohibitions. New rational, invalid-input,
weighting, deterministic and independent-oracle tests check actual arithmetic.

`test_phase3_unauthorized_path_change_fails` retains all parameter identities and
now explicitly checks the historical Step 1 permission set. The Step 2 and
Step 3 incremental negative tests likewise retain their identities and check
their own historical permission sets. New tests separately verify the current
Step 4 permission set. `tests/unit/test_phase3_contracts.py` is already included
in Step 4's approved allowlist; no additional file exception is required.
The exact earlier Step 2 one-expression exception remains verified between its
frozen Step 1 and Step 2 Git objects. It is not treated as a permanent ban on
later expressly authorized edits to the same test file.

The checker admits the exact new function, class and import lists and adds a
literal fingerprint of the reviewed module AST. Existing checks still run.
Only empty type_params AST metadata added in Python 3.12 is omitted when
fingerprinting; nonempty parameters are rejected. The digest is never generated
from current runtime source during gate execution. In-body formula changes,
new executable symbols, I/O, dynamic execution and later layers are rejected.
This is a change-control guard, not mathematical proof. Independent rational,
frozen-golden and invariant tests provide numerical verification. Twenty-one
package modules remain docstring-only.

All workflows explicitly select `--phase 3 --step 4`. Full core and real-Parquet
regression, historical test identities, security, unchanged Hero, build and
installed-wheel checks remain required. Baseline evidence now includes the
accepted Step 3 node IDs (1575 core and 1578 real-Parquet). Installed checks keep
no-dependency import/input verification separate from exact-duplicate and
F-001 through F-004 calculation checks with approved dependencies present.

Review roles remain the Theory Owner's approval and assistant self-review with
actual executable evidence. No independent human review is claimed. There is
no source-share, closure, tail, resampling, pair, graph, report or audit-CLI work.
Stop after Step 4 acceptance; no main merge, publication or phase completion.

## Phase 3 Step 5 authorization and execution contracts

The Theory Owner explicitly instructed continuation of Step 5. Its accepted
predecessor is `b943a9712ed1e5b64e09c2c394077fdeed78114f`, tree
`e8f503b44cee0d3db059c03da6599fe44503f03b`. Actual Actions evidence confirms
1714 core and 1717 real-Parquet tests passed, with all four workflows successful.
The downloaded artifact's checksum and source root tree were verified. This
closes the preceding Step 4 acceptance uncertainty; no further Step 4 runtime
change or permission exception is required.

Only `metrics/provenance.py` gains runtime behavior in this step. Its explicit
`summarize_provenance` and `classify_direct_grounding` calls consume a Phase 2
join plus an exact, single-version CalculationScope. All selected valid records
remain in the denominator, named `all_valid_records_in_selected_dataset_scope`.
Representation exclusions, mismatched key sets and empty scopes are rejected.
Consumed provenance fields, flags, coverage and retained error/warning evidence
are revalidated without a second join. Input validation errors survive regardless
of whether an independently meaningful composition table can be calculated.

Source counts use human/synthetic/mixed/sensor/unknown. Missing provenance has
its own count/share and does not become unknown. Confidence has four category
counts, with no numeric trust conversion. A missing/null field in a matched row
makes only its own complete composition unavailable, with exact record keys,
coverage and reason. It never creates a new category, changes denominator or
silently normalizes a known subset. With no provenance rows, the declared counts
are zero and the separately identified missing share is one.

P3-D08 controls the direct partition: required-field-valid yes/no declarations
supply known open/closed; all other records remain unresolved. Source class,
human review and valid estimated/unknown confidence never substitute for or
discount grounding. An incomplete required row remains unresolved even when its
grounding cell contributes to Phase 2 grounding-field coverage. The three direct
counts are observed facts under `toolkit_operationalization`, relative to supplied
loop-grounding declarations. They do not certify source truth or independence,
resolve parents, or calculate F-009/F-010 intervals.

Explicit `WeightingOptions("weighted", "weight")` and a complete canonical-key
map enable separately named source weight masses/shares. Missing-provenance
records are included in the weight scope. Default counts/shares, confidence and
the direct partition remain unchanged. A zero weight cannot hide an absent
source declaration. Missing/extra identities, bools, negative/nonfinite values,
nonempty total zero, finite-sum overflow and positive-share underflow fail.
Deterministic canonical-key summation uses fsum. The denominator is explicitly
`all_selected_record_weight_mass`; no confidence or grounding weight is invented.

### Gate migrations and review record

The PR-004, PR-005 and T3 owner tests retain their original identities. Their
whole-module-placeholder assertion now checks the Step 5 boundary and explicit
prohibitions on later functions. All Phase 2 validation tests remain intact.
Step 4 permission tests retain their original identities and now query the frozen
Step 4 allowlist; new tests separately cover Step 5. The previously exceptional
`test_phase3_contracts.py` is unchanged. Original plan/oracle/authority bytes and
all earlier runtime code remain protected.

The new module has exact definition/import allowlists and a fixed reviewed AST
fingerprint, using the accepted empty-type-params/full-field compatibility rule.
Positive controls accept the reviewed source; mutations reject altered formulas,
missing-to-unknown reassignment, I/O, callbacks and deferred feature owners. This
change-control check is separate from the independent mathematical test oracles.
The Step 4 distribution fingerprint is unchanged. Twenty modules remain pure
placeholders. All four workflows explicitly select Step 5, with real Parquet,
historical test identity checks and installed-wheel numerical smoke coverage.

Technical, mathematical and security review roles are consolidated in the
assistant's source inspection and executed automated checks. No independent
human reviewer or truth certification is claimed. Three new synthetic fixtures
contain authored rational/cross-product expectations; no implementation generated
its own oracle. PR-005/F-007 owns source shares, PR-004/F-008 the inherited row
coverage, PR-004 confidence/missing-row facts, and T3 the direct partition basis.

Stop after Step 5 acceptance. No Step 6 calculation, Phase 3 completion, main
merge, tag, publication, report, audit CLI, general graph or simulation is authorized.
