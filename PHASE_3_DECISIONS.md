# PHASE_3_DECISIONS

Current work: Phase 3 Step 11. Earlier approval/contract/build sections below are historical step records. Current authority and the subsequent precise test-maintenance approval are recorded in the Step 11 sections at the end. Actual final acceptance is tracked in the three Phase 3 milestone reports.

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


## Phase 3 Step 6 execution contract

Theory Owner authorization: explicit instruction to continue Phase 3 Step 6.
Accepted predecessor: `4611f897d054b352733cc90543eef6f6d71cd811`, tree
`faffd5717dc1bf99e0081a122a338c65a68a13a7`; 1888 core / 1891 extra-enabled
historical test identities must remain. Original authority and oracle bytes stay frozen.

Only `metrics/bounds.py` gains runtime behavior. F-009 is C/N; F-010 is
(C+U)/N; width is U/N, without clipping or midpoint substitution. The pure count
kernel is `closure_exposure_bounds`; `direct_closure_exposure` consumes the Step 5
composition with its unfiltered single-version record denominator. Original errors,
row/required-field/grounding coverage, confidence counts or unavailable confidence
status are retained. Confidence never discounts a grounding declaration.

The Step 6 plan already distinguishes count envelopes from dataset validity:
all-unresolved counts permit [0,1], but absence of every complete valid required
provenance row leaves dataset-facing scalars unavailable. A valid unknown grounding
row may support [0,1]. Internal consistency checks do not independently verify the
truth of supplied declarations and do not reconstruct provenance or lineage.

Test migrations preserve identities: `test_T3_bounds_owner_and_placeholder` keeps
its name and owner check, replaces whole-module emptiness with a direct-only boundary;
Step 5 permission tests use their frozen historical permission set after advancement;
workflow names and the placeholder count advance to Step 6 and 19 respectively.
Prior positive checks and mutation rejection remain. The new bounds guard pins
reviewed source bytes and compares ASTs inside the same interpreter, avoiding
cross-version serialized-AST assumptions without accepting arbitrary edits.

No Phase 4 report/CLI, Phase 5 lineage, Step 7 tail, resampling or publication is
authorized. Stop after Step 6 tests/build/installed-candidate checks and delivery.

## Phase 3 Step 7 execution contract

Theory Owner instruction: continue Phase 3 Step 7 after the Step 6 delivery.
Accepted predecessor `c7d5ceed2f154bd2ccffbe49961dbf1b65b9df63`, tree
`bc1878e10a9fd056afd196e85126af7ddb9555e5`; retain 1987 core / 1990
extra-enabled identities and all earlier approved sources and implementations.

Only `metrics/tail.py` gains runtime behavior. `select_tail` consumes a Step 4
unweighted count-backed distribution and explicit TailSelectionOptions. It does
not reconstruct records or turn probability-only vectors into record shares.
The four P3-D06 rules are singleton_count, count_at_or_below,
frequency_at_or_below and state_list. Thresholds are inclusive; zero counts are
outside observed support. List requests must name positive observed states.
Membership uses Unicode order. Rarity uses ascending frequency, then count, then
Unicode state ID, with ordinal ranks starting at one. There is no weighted-tail
or bottom-quantile implementation. Existing option contracts remain unchanged.

The selected count sum divided by the included record denominator is the tail
record share. A nonempty dataset with an empty tail returns zero; an empty or
all-excluded representation returns unavailable scalars and inherited reasons.
Representation exclusions remain visible and do not affect provenance scope.
Tail metadata carries the rule, representation, scope, denominator, evidence,
units and limits. No importance, risk severity or permanent loss is inferred.

`one_step_extinction_probability` separately evaluates F-014 using an explicit
selected-state marginal p and positive integer n. It is `simulation`, experimental,
method analytic_extinction, horizon one, with no seed or random realization.
The numeric evaluation uses exp(n*log1p(-p)), with exact p=0/1 branches to avoid
cancellation for small p. Interior underflow is disclosed and does not assert an
impossible event. Out-of-range numeric inputs fail without clipping, probability
repair, inferred n, external input or random sampling. This changes no formula.

The independent fixture and tests use approved rational F-014 targets; added
boundary/metamorphic checks are test design. The original golden files are frozen.
Only the old T2 placeholder assertion migrates to its implemented boundary. Step 6
permission negatives now explicitly test the frozen Step 6 allowlist; their test
identities and rejection guarantees remain. Step 7 has separate path, formula,
evidence-class, I/O and later-owner injection negatives. Prior protected runtime
hashes are unchanged. The new tail source digest is fixed after review, never
learned by a running gate from edited code. All four workflow roles are retained.

Technical, mathematical and security review work is performed by the same AI
assistant with execution evidence and source-based oracles; no independent human
reviewer or security certification is claimed. No new theory decision, dependency,
report schema, audit command, Phase 3 completion, main merge or release is authorized.
Stop before Step 8.


## Phase 3 Step 8 execution contract

Theory Owner authorization: accept Step 7 and continue Phase 3 Step 8. Accepted
predecessor: `d3d95bde50762e60b4dd03cb2bd988618c9a10fe`, tree
`5cb81772542ebfa87c634572068dbf9ee49f41d0`. Preserve all 2117 core / 2120
real-Parquet historical test identities and the original Phase 0 authority hashes.

Only `metrics/resampling.py` gains runtime behavior. The T1 mathematical source
is the fixed finite multinomial model in Definitions 12.1-12.5 and the approved
P3-D02/D04/D07 resolutions. Public interfaces require a complete explicit
state/probability vector, scope, representation, resample_size and steps.
`expected_diversity_after_steps` returns the F-015 analytic sequence from t=0
through the requested horizon. Its fixed-n iteration is D0*(1-1/n)**t.
`simulate_closed_resampling` additionally requires explicit seed and replicates.
It returns each replicate and each generation separately; initial counts are
None, because an arbitrary initial probability vector does not supply record
counts. There is no scalar-diversity overload that could omit the distribution
basis, no default sampler seed/size/horizon/replicates, and no q/r/lambda input.

Both branches are `simulation`, experimental, and bound to their supplied scope
and representation. Analytic and sampled results are separate types. An analytic
expectation contains no fabricated seed or RNG. Sampled results record actual
NumPy version, named `numpy.random.Generator(PCG64)`, method version
`closed_categorical_v1`, canonical ascending Unicode state order and
`replicate_major_step_major`. One generator is constructed per explicit call.
No global RNG state is used. Replicate index starts at zero, as does the initial
model-time step. Simulation time has no mapping to dataset generation or epoch.

### Numerical implementation and resource bounds

Probability components must be built-in finite int/float values in [0,1], with
no bools, duplicate state IDs or negative components. State IDs remain literal,
including an existing empty-string state; their Unicode order is deterministic.
Total mass must be positive and within the approved absolute 1e-12 tolerance.
Analytic inputs retain the supplied near-unit vector and disclose its residual.
The sampled branch, and only that branch, divides by the validated total when it
differs from one. Both original and effective vectors, total, residual, divisor,
component corrections and correction flag remain available. Exact zero states
stay zero. Material mass errors fail; no arbitrary count-vector repair exists.

The closed multinomial transition is implemented by its sequential conditional
binomial factorization, `sequential_binomial_complement_v1`. States are visited
in canonical Unicode order, skipping zeros. The smaller binomial side is sampled
to avoid cancellation of a tiny complementary tail. The last positive state
receives the remaining count. Zero states never receive a floating residual.
After generation one, exact integer counts supply the next transition's relative
masses and exact suffix sums, equivalent to sampling from counts/n. Exposed
frequencies are counts/n. The initial float suffix sums use fsum. No external
state or smoothing mass is introduced. This is an implementation of the approved
multinomial transition, not a new stochastic model. Same-environment replay is
required; cross-version bit identity is not promised. NumPy's official binomial
and random-compatibility documentation informed API usage, not product scope.

Engineering limits are explicit: maximum 4096 states, 10000 steps, 10000
replicates, 1000000 state-by-time-by-replicate cells (including t=0), resample
size 2147483647 and seed bit length 4096. All work/domain checks precede path
allocation and lazy NumPy import. These bounds are operational safeguards, not
model constants or inferred parameter defaults. Excess requests fail with the
existing E_CONFIG_INVALID rather than being truncated. Numerical domain errors
use the existing E_SCHEMA_TYPE. No enum or serialized config extension is made.
Analytic positive values that underflow are explicitly listed by step; no exact
finite-time absorption is inferred from floating zero.

### Tests and stage maintenance

The original T1 and T5 test identities remain. Their shared-module placeholder
assertions migrate to exact implemented-scope and no-reopening checks. T5 tests
only protect the deferred branch; no T5 scenario is implemented. Step 7 path
negative tests now target the frozen Step 7 allowlist, retaining their rejection
guarantee; new negatives target the current Step 8 scope. Original runtime
sources, numeric oracles and previously authorized exceptions remain untouched.

New T1 tests use the frozen F015 targets, independent rational fixture values,
exact finite multinomial enumeration, Monte Carlo sanity checks, integer totals,
zero absorption, constant state identities, repeatability and global-state
isolation. Individual diversity paths may increase, so no false pathwise theorem
is asserted. Probability correction, invalid inputs, object hooks, explicit
parameters and bounded resource failure are tested separately. Default and
explicitly enabled eligible `validate_bundle` scenarios still never execute
kernels. Imports and analytic calls remain possible with numerical dependencies
blocked; sampled calls fail clearly when NumPy is unavailable. Separate installed
wheel checks exercise actual sampling with NumPy present and I/O/network blocked.

The exact reviewed source digest and same-interpreter AST comparison protect the
new module. NumPy is authorized only as the lazy `import numpy as np` inside
`simulate_closed_resampling`. All other prior import restrictions are preserved.
Technical, mathematical and security review roles are consolidated in this AI
assistant's inspection and executed tests; no independent human review or security
certification is claimed. No external loss/reopening, graph, report, audit CLI,
Phase 3 completion, publication or main merge is authorized. Stop before Step 9.

The inherited PR-016 lexical-order test also contained a resampling placeholder
assertion. Step 8 migrates that one assertion to the exact reviewed resampling
source/AST boundary, while retaining the lexical-order assertions and both report
placeholders. Its original test identity is preserved. This test file is in G;
no additional file exception is needed. The first full local run exposed this
stale assertion (2267 passed, one failed); it is not hidden or skipped.

## Phase 3 Step 9 authorization and implementation record

The Theory Owner requested Phase 3 Step 9 after the accepted Step 8 delivery.
The immutable starting commit is `a43cba0e81fd89c3b20a64737bfa89cd2bac4de9`,
root tree `f7ecf2326770b362b51ba67357ec450e311a086a`. Its 2268 core and 2271
real-Parquet test identities remain required. Original Phase 0 authority, the
approved plan bytes, previous decisions, and prior test identities are retained.
No new theory decision, file exception, merge, publication or next-step execution
is authorized. This record implements P3-D03 and Step 9, without rewriting them.

### Explicit comparison contracts

`validate_representation_compatibility(...)` consumes `ExplicitPairContext`,
explicit earlier/later state-meaning declarations and optionally a
`StateMappingDeclaration`. Identical representation name, source, version, rule,
field, normalization profile, missing policy and missing-state ID plus identical
state-meaning declarations establish the identity comparison basis. These are
caller declarations, not semantic certification. Version strings alone cannot
establish compatibility. Retained Phase 2 ordering declarations are revalidated;
cached order flags, filenames, lexical order and capability labels do not select
or authorize a pair. A full loaded chronology may include intermediate versions;
only the two explicitly selected scopes are compared.

A directed literal map requires the source and target descriptors, source and
target state meanings, and `earlier_to_later` or `later_to_earlier`. Its plain
string-to-string dictionary is copied into immutable evidence. Multiple source
states may intentionally map to one target; collision groups are recorded rather
than overwritten. Every supplied source-state entry, including explicit zeros,
requires a map entry. Extra declared but unobserved keys add no records or mass.
No implicit identity mapping, inferred equivalence, one-to-many allocation,
callable, or bare global `state_mapping` is executed. A map cannot change row
inclusion/missing policy. An explicit missing marker must map to the target
missing marker, and ordinary states cannot collide with that marker.

`compare_support(...)` consumes two Step 4 `DistributionMetrics` objects and the
explicit compatibility context. Consumed scopes, counts, masses, frequencies,
status, support, scalar values, numerical policy and trace identities are checked
again. The original independently useful single-version calculations are
preserved. Original and harmonized distributions remain separate in the result.
Any coarsening's before/after support sizes, exact mapping and collision groups
are retained. Support/difference sets use positive mass only and deterministic
Unicode ordering. Explicit probability vectors retain their supplied-input label;
they are not mixed with count-backed inputs or promoted to empirical records.
Both sides must use the same weighting and denominator family. Weighted pairs
are possible only when both explicitly supplied distributions are the previously
opted-in weighted companions. Their mass support never substitutes for the
unweighted record-presence result.

F-005 uses later support size minus earlier support size. F-006 divides the
intersection by earlier positive-mass support. F-018 uses later minus earlier
Gini-Simpson diversity. Loss and added counts/sets remain separately visible even
when the support delta is zero. Pair trace metadata identifies both ordered
scopes, the harmonized representation, evidence class `derived_metric`, units,
methods and limitations. Earlier/later empty or all-excluded input makes the pair
unavailable; affected values and sets are None with retained reasons. An empty
later input never fabricates measured extinction of every earlier state. Real
zero changes on valid distributions remain available numerical zeros.

This is a pure explicitly invoked pair kernel, not Phase 6A longitudinal
orchestration. No version discovery, trajectory, automatic adjacent pairing,
relative-change calculation, provenance/lineage change, model-performance claim,
report, audit CLI or runtime network access is introduced. Observed absence in
the later declared representation does not certify permanent production-process
extinction. `validate_bundle(...)` remains input-only, even when it declares
`dataset_longitudinal` available.

### Tests, preservation and gate migrations

Frozen Hero pair expectations are unchanged: support delta -3, retention 5/8,
diversity delta -1/8, lost battery/lizard/turtle and no added states. Independent
rational mapping fixtures and edge cases test identity, chronology, incompatible
versions/meaning, mapping direction and aggregation, missing-marker collision,
scope exhaustion, weighted separation, original assignment preservation,
forged summaries, determinism and no I/O/automatic dispatch.

The runtime change is restricted to the approved compatibility module plus
additive functions/types/imports in diversity.py. All preexisting diversity
functions and classes are retained exactly and verified against Step 8 Git source
in the release audit. Models, errors and field representation need no changes.
The current full-source digest plus same-interpreter AST guard protects the
additive implementation without cross-Python AST serialization dependence.
Historical Step 4 numerical-injection tests remain unchanged and still fail on
altered formulas. The Step 8 file-permission tests are routed to the frozen Step 8
allowlist; their identities and original rejection conditions are retained.
New negative tests enforce the Step 9 scope and reject later-layer behavior.
The new compatibility module reduces the protected placeholder count from 17 to
16, without changing the total of 40 package modules.

Review roles for technical, mathematical and security checks are consolidated in
this AI assistant and executed tests. No independent human review or broad
security certification is claimed. Stop after Step 9 acceptance, before Step 10.

## Phase 3 Step 10 authorization and integration record

The Theory Owner accepted the Step 9 delivery and explicitly requested Phase 3
Step 10 in the project conversation. The starting commit is
`03fe1e7e99c8170e6be7714649ab0d926e01b6d6`, tree
`765d28e6ff4715fa6d59f44760f1a937489d7120`. Its 2404 core and 2407 real-Parquet
identities remain required. No new theory decision, runtime repair exception,
merge, publication, or Step 11 execution is authorized.

### Test-only composition and frozen expectations

A callable pytest fixture explicitly loads the unchanged Hero through the Phase 2
validator, then calls field representation, single-version distributions,
provenance composition, direct bounds, duplicates, tail selection and one ordered
pair comparison. It is test infrastructure only. The importable package gains no
orchestrator, report object or audit CLI. Separate calls test analytic extinction,
F-015 expectations and explicitly seeded closed paths. Default Hero validation
still executes no metrics or simulations, including when scenario eligibility is
otherwise satisfied. Partial required-provenance errors remain visible beside
independently usable calculations; missingness and representation exclusions keep
separate denominators. Synthetic mapped inputs exercise the full schema-mapping
handoff while preserving original source files and leading-zero identities.

The new golden runner executes every one of the twenty cases frozen in Step 1.
Neither golden manifest nor its notes are changed. For F-015 cases specifying
only initial diversity, explicit equal-state probability vectors are mathematical
witnesses of that diversity; they do not invent empirical record frequencies.
Source-derived numerical targets retain their original owner, formula, rational
value and source section. New metamorphic and performance cases are authored
validation design, not additional claims attributed to the source articles.
Newly provided theory articles do not alter the frozen approved product scope.

### Performance measurement contract

The synthetic case contains 100000 records, 100 equiprobable topic states and
1000 exact text forms, each repeated 100 times. Source classes alternate between
human and synthetic with valid required provenance. These construction rules
independently determine support 100, diversity 99/100, source shares 1/2 each,
1000 duplicate groups and 99000 duplicate records.

Setup, field representation, distribution metrics, provenance join, composition
and exact duplicates are measured separately. The Hero measurement covers input
plus explicitly invoked calculations. Each actual test attaches elapsed wall time,
Python/platform/dependency versions and traced allocation peaks to its JUnit
record. Timing uses perf_counter with tracemalloc(1) enabled. Per-call traced peaks
exclude preexisting inputs and untracked native allocations; setup is measured
separately. They are not process RSS or measurements of a completed public report.
There is no hardware-dependent pass/fail speed threshold and no best-of-run
selection. JSON/Markdown reporting is not present, so the complete under-five-second
product target is not certified. Duplicate-path line-event growth is separately
checked for repeated, unique and mixed forms to guard against an accidental
quadratic comparison pass without relying on timing ratios.

### Gates and preservation

All forty runtime modules remain byte-for-byte identical to Step 9. The existing
Step 9 source/AST checker is intentionally retained unchanged as the frozen
runtime boundary. The Step 10 release audit additionally verifies the full runtime
byte digest, unchanged Hero, schemas, dependency declaration, approved plan and
both mathematical oracle files. Exact Step 10 allowed paths contain no src entry.
The historical Step 9 path tests are routed to the fixed Step 9 permission set;
all names and rejection conditions are retained. New Step 10 tests reject runtime
edits, forged authorizations, oracle changes and missing/invalid measurement
records. Workflow labels and explicit phase/step arguments advance together;
read-only tokens, failure propagation, complete matrix, real Parquet, installed
wheel checks and immutable historical identities remain required.

This is a narrow active-stage synchronization. The earlier proposed general
checker refactor is not performed. No protected runtime file is opened to make
integration pass. Technical review is by this assistant and executed tests; no
independent human review or general security certification is claimed. Stop after
Step 10 acceptance and evidence delivery, before Step 11.

## Step 11 authorization and finalization boundary

On 2026-09-18 the Theory Owner explicitly requested Phase 3 Step 11. After the assistant identified two stage-test files absent from the planned Step 11 list and proposed precise maintenance exceptions, the Theory Owner instructed continuation: `很好，继续phase 3 step 11`. This approves the stated exceptions. No additional runtime repair, dependency change, main merge, publication or later-phase work is authorized.

The accepted Step 10 commit is `150a2a105e01883672ef0c2300b41b0de3be352e`, tree `b609cb75913fc6352729086819a24795caae1dd8`. It contains 219 tracked files, 2472 core test identities and 2475 real-Parquet identities. The Step 11 gate preserves that full baseline, all prior step identities and the original Phase 2 root/test identities.

| Approved exception | Exact change | Retained guarantee |
|---|---|---|
| `tests/unit/test_phase3_contracts.py` | Change only completion-forgery assignment from unconditional True to `not control[key]` | A forged completion flag is rejected in both pending and completed stages; exact byte transition enforced |
| `tests/integration/test_phase3_metric_pipeline.py` | Bind three historical Step 10 scope/control/snapshot tests to immutable Step 10 bytes; append Step 11 gate tests | Every inherited name, parameter and numerical assertion retained; transformed inherited prefix checked byte-for-byte |

The `tests/conftest.py` historical fixture extracts the exact pinned Step 10 commit after verifying its tree. The fixed historical control digest and historical file allowlist remain independent of current manifest permissions. The Step 11 runtime digest normalizes only the two authorized dev2-to-dev1 version literals before comparison; every other runtime/dependency/backend/CLI/schema/Hero/oracle byte remains frozen.

Active workflow/version assertions in the already authorized maintenance files move to Step 11/dev2. Both distributions, all forty installed imports, input-only validation, no-network/no-execution boundaries, actual real-Parquet tests and strict JUnit checks remain mandatory. The source ZIP is renamed to the planned final Phase 3 filename. Four workflow roles remain; none publishes or merges.

The direct-dependency minimum declarations cannot be installed literally together: pandas 2.2.0 requires NumPy below 2, while this package requires NumPy at least 2.0. The recorded minimum profile therefore uses the lowest jointly compatible pair, NumPy 2.0.0 / pandas 2.2.2, without changing declarations. The rejected literal resolver command is retained. Current-compatible profiles and real PyArrow are separately recorded. This interpretation tests actual compatibility and makes no claim that the impossible pair passed.

The assistant performs implementation, mathematical-transcription/traceability and security-boundary reviews with consolidated roles allowed by governance. The user is the Theory Owner and approval authority. No new independent reviewer or certification is claimed. Review findings, real failures/repairs and final workflow evidence belong in the milestone reports and external receipt.

The implementation-acceptance commit will be recorded only after all four workflow roles pass. Final acceptance-record changes require a second complete run on the exact final source commit. A pending candidate does not certify Phase 3 completion. After verified final delivery, stop before Phase 4, main merge, tag or publication.


### Additional final-report historical-test approval

After the initial complete run (2488 passed, one failed), the assistant identified
`test_phase3_final_completion_records_not_created` as a second stale stage assertion
in the already excepted unit file. The Theory Owner explicitly replied `批准` to
the proposed narrow migration. The historical test now reads `phase3_step10_snapshot`
and preserves its name and three original absence assertions. The current Step 11
repository-structure test requires all three reports to exist. The byte-transition
guard permits only this signature/root binding and the previously approved
completion-forgery expression. No numerical expectation or security assertion is
changed. The original failed run remains retained and does not count as acceptance.


### Step 11 implementation acceptance and final record

All four workflow roles and twelve jobs passed on `9dc321c6997a231209653a0f86d0476824e96e3a` (tree `a1086ca95075aff3ea8a83afae548806b2079dc9`).
The CI core matrix passed 2489 cases in each of eight environments; real Parquet
passed 2492; security passed 1678; Hero/math passed 83. Build/delivery repeated
complete suites, verified installed behavior and archived 222 tracked source files.
Actual run IDs are recorded in the milestone reports. The source implementation is
technically accepted; the completion flag and immutable acceptance anchors now
record that observed result. No main merge, publication or later phase follows.

The acceptance-record commit changes the three reports, these decision/control
records and the maintainer's acceptance constants/check. It changes no runtime or
oracle. Its own complete four-workflow rerun and regenerated artifacts are mandatory
before final handoff. Final HEAD and hashes are recorded by execution metadata and
the external receipt rather than a circular in-document self-hash. Consolidated
assistant review roles and the hosted-binary download limitation remain disclosed.
