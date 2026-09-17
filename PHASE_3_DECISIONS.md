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
