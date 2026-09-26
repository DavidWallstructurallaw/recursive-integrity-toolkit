# Phase 5 Step 1 Completion

Date: 2026-09-23 UTC. Status: **STEP 1 COMPLETE; PHASE 5 INCOMPLETE**.

The Theory Owner approved the Phase 5 plan and instructed Step 1 to start.
Work begins from `1db3b1a460c233242ff37fbe45b8fac74d6101ef` on the new
`phase5-lineage` branch. This record covers contracts, fixtures and verification
consolidation only. It grants no subsequent-step execution, merge, tag or
publication.

## Delivered

- Approved `PHASE_5_PLAN.md` and P5-D01 through P5-D11 in
  `PHASE_5_DECISIONS.md`.
- `docs/lineage_contract.md`: immutable type/field interfaces, explicit scope,
  root/uncertainty/depth rules, status semantics, bounded privacy-safe detail and
  resource interfaces for later implementation.
- Twelve independent acceptance cases across the three existing lineage fixture
  directories, plus separate frozen-Hero lineage expectations. Exact oracle
  arithmetic is recorded independently of future algorithms.
- One current path in the three existing verification scripts. Historical
  source-body migrations, snapshot fixtures and staged authorization assertions
  no longer run by default. Earlier forms remain recoverable from Git.
- Focused ordinary CI and explicitly selected candidate CI. The supported matrix,
  real Parquet, Hero, security, installed packages and reproducibility remain
  required at candidate gates; the expensive performance directory runs once on
  a designated reference profile.

The executable product is unchanged: forty Python modules, five root schemas,
seven packaged resource copies, six canonical Hero files and package metadata
match the accepted Phase 4 product. Package version remains `0.1.0.dev3`; report
schema remains `1.0`. General lineage algorithms are still deferred.

## Contract details resolved

One canonical parent remains one parent even when its declaration has multiple
aliases. Reference coverage retains those declarations, while adjacency/root mass
deduplicates them. Unknown grounding can coexist with known structural depth.
Other grounded-with-parent forms remain unresolved outside the approved
single-parent carryover rule. Empty analytical scopes do not imply current CLI
acceptance of an empty records file.

Detail collections are capped at 100 rows; complete cycle witnesses at 64 edges.
Long witnesses are explicitly omitted rather than presented as nonclosed prefixes.
The four initial lineage budgets are 200,000 nodes, 1,000,000 edges, 1,000,000
logical root memberships and 10,000,000 root-union visits. These are future graph
work guards, separate from ingestion limits and measured RSS.

Current normalization preserves an absent parent field in
`CanonicalRow.field_states` while its normalized value is null. Step 2 must use
that retained evidence to preserve absent/null declaration semantics.

## Verification performed

| Check | Actual result |
|---|---|
| Three current source/specification/traceability commands | PASS: 59 protected product files unchanged, 16 frozen specifications, 7 exact resource copies and 40 owned modules |
| Exact focused CI test selection | 212 passed in 3.62 seconds |
| Affected current-control and neighboring tests | 263 passed in 3.01 seconds; overlaps the focused selection and is not added to it |
| Workflow scheduling/JUnit boundary tests after final path-filter fix | 18 passed |
| New fixture input validation | 12 passed; these also belong to the focused selection |
| Final canonical collection, excluding designated performance directory | 2,629 collected without errors; this is collection, not a full passing run |
| Independent fixture arithmetic | Hero and rational multi-root partitions, coverage, bounds, HHI and effective-root values checked |
| Four workflow files | YAML parsed; candidate dependencies and read-only permissions checked |
| Retained same-named test/helper definitions | 746 compared structurally; executable bodies unchanged, excluding explanatory docstrings |
| Diff formatting and independent review | PASS; no remaining Step 1 blocker |

Checks used Python 3.12, pytest 9.1.1, NumPy 2.5.3 and pandas 3.0.6. Missing test
dependencies in the resumed local environment were installed before execution.
No full regression, cross-platform matrix, real-Parquet profile, release build,
installed-artifact check or 100k performance run was performed for Step 1.
Hosted execution of the changed workflows is not claimed by this record.

The local focused command was:

```bash
python -m pytest -p no:cacheprovider -q \
  tests/integration/test_current_verification.py \
  tests/integration/test_ci_workflows.py \
  tests/unit/test_lineage_fixture_inputs.py \
  tests/unit/test_phase3_contracts.py \
  tests/integration/test_phase3_metric_pipeline.py \
  tests/unit/test_PR016_determinism.py \
  tests/integration/test_no_algorithms.py \
  tests/integration/test_repository_structure.py
```

## Guarantees retained through consolidation

Direct current tests continue to protect mathematical formulas, representation
semantics, provenance and direct bounds, input-only validation, unavailable
states, report schemas, privacy, no-network behavior, safe paths and CLI output.
Current negative checks reject unauthorized runtime mutation, self-authorized
specification edits, corrupted/extra packaged resources, damaged or incomplete
wheel/sdist payloads, duplicate archive entries and unsafe extraction members.
Existing installed behavioral checks remain in candidate verification.

The three verification scripts shrink from 17,316 to 1,444 lines by removing
historical dispatch and repeated source-preservation machinery. This count
describes the consolidation and is not an acceptance target. The behavior map is
in `PHASE_5_DECISIONS.md`; historical bodies and evidence remain recoverable at
the accepted Phase 4 commit and its earlier history. No new baseline registry,
historical source-binding migration or evidence-of-evidence mechanism was added.

Independent review found that a blanket documentation path exclusion would hide
changes to the new authoritative lineage contract. The workflow now excludes only
named nonauthoritative documents; a lineage-contract change receives focused
checks. The final workflow tests cover that distinction.

## Handoff

Step 2 will construct the validated parent graph and retain per-record reference
successes/failures using one identity lookup. Its algorithms and runtime changes
are not implemented here. Phase 6A and Phase 6B remain deferred.

Continue only when Phase 5 Step 2 is instructed.
