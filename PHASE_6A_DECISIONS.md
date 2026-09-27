# Phase 6A decisions

| Field | Value |
|---|---|
| Status | APPROVED; Step 1 contract record |
| Authority | Theory Owner instruction: `phase 6a step 1开始` |
| Authorization date | 2026-09-26 America/Los_Angeles; 2026-09-27 UTC |
| Approved plan | `PHASE_6A_PLAN.md` version 1.0, delivered at `753829a79fb6aa550d58dcd6fced360399c597e9` |
| Accepted product baseline | Phase 5 completion `f09521907558a193e6438d9acb316adb9e191195` |
| Working branch | `phase6a-longitudinal` |
| Current scope | Contracts, independent acceptance inputs and affected current checks |
| Current runtime | `0.1.0.dev4`, report schema `1.1`; unchanged by Step 1 |
| Eventual phase target | `0.1.0.dev5`, report schema `1.2` |

The instruction starts Step 1 under the delivered plan without stated exceptions.
It authorizes P6A-D01 through P6A-D08. It does not authorize executing all later
steps, Phase 6B, merging PRs, tagging or publishing a release. Existing permission
to synchronize project work continues on the planned development branch.

## Approved decisions

| Decision | Required boundary |
|---|---|
| P6A-D01 | Select primary/comparison snapshots explicitly; retain validated chronology; context and unloaded order entries do not become snapshots. |
| P6A-D02 | Adjacent pairs by default; optional first-baseline pairs; deduplicate overlaps; retain unavailable gaps. |
| P6A-D03 | Reuse descriptor, meaning, directed mapping and weighting contracts; retain original and pair-local harmonized bases and independent populations. |
| P6A-D04 | Later-minus-earlier deltas, observed disappearance and earlier-tail disappearance; preserve valid zero, empty set and unavailable evidence distinctions. |
| P6A-D05 | Per-version provenance, separate coverage types, declared source shares and direct-closure interval changes; unknown stays distinct from missing. |
| P6A-D06 | Explicit opt-in selected-target lineage with shared validated graph evidence, complete version populations, partial-coverage disclosures and retained input binding. |
| P6A-D07 | One schema 1.2 integration in Step 6, canonical JSON/Markdown, truthful execution states and privacy on every new identity-bearing path. |
| P6A-D08 | Explicit inert configuration, 100 selected versions by default, inherited graph limits, 100-row detail tables and input-only validation. |

The exact proposed runtime types, field names, serialized configuration, public
report inventory, statuses, reasons and edge cases are fixed in
[docs/longitudinal_contract.md](docs/longitudinal_contract.md). They are future
implementation contracts. Step 1 does not add these types to the running package,
accept new CLI flags, or claim that schema 1.2 already exists.

## Step 1 clarifications

1. Use a separate selected-version lineage entry point returning shared graph
   evidence and target-only summaries. Preserve ordinary `analyze_lineage` and
   its primary-only default. Copying or replacing a full target-bound graph
   result once per version is not the intended sharing strategy.
2. Record-based series are unweighted in this phase. Existing explicit weighted
   and probability-vector pair APIs retain their accepted support; they do not
   acquire automatic series dispatch.
3. Explicit empty Python snapshots retain their own declarations and selected
   chronology. They are never inserted into `BundleValidationResult.records` or
   `VersionOrderResult.loaded_versions`. A narrow compatibility check reuses
   descriptor/meaning/mapping rules without fabricating loaded records.
4. All required provenance/direct and distribution families are requested by a
   series invocation. Tail and lineage are optional. No provenance manifest
   means genuinely missing provenance with inherited values/reasons, not an
   unrequested provenance family. Metadata with `unknown` remains supplied data.
5. New report scope references are confined to longitudinal fields. Legacy
   scopes and ordinary/pair fields retain their wire meaning. Internal scopes
   retain exact membership; new public scope summaries avoid duplicating record
   identity arrays for each pair and metric.
6. Ordinal snapshot/pair references are structural report identifiers. Literal
   versions and semantic state identifiers receive established privacy handling;
   semantic state labels from different bases are never implicitly unified.
7. Exact new config fields and their conflict rules are defined before adapters
   are changed. Existing bare `state_mapping` fields remain insufficient for a
   directed scientific comparison.

These settle interfaces within the approved plan. They introduce no scientific
formula, observed-to-causal promotion, new grounding rule or automatic scenario.

## Independent acceptance inputs

`tests/fixtures/longitudinal/` records literal synthetic inputs and rational
expectations. Cases exercise the approved three-version progression, provenance
missingness, complete/partial/empty-root lineage, mapping/order boundaries and
explicitly absent distributions. `hero_expected.json` derives additional
two-version expectations from the unchanged canonical Hero rows.

The fixture test uses only implemented input and explicit per-version/pair
kernels. Future series expectations remain independent acceptance targets.
Passing Step 1 checks does not certify later orchestration, multi-target lineage,
new CLI/config parsing or schema 1.2.

## Current verification boundary

Update the single existing accepted Git reference to the delivered plan commit
`753829a`. Step 1's product implementation allowlist is empty. All runtime,
schemas, canonical Hero resources and package metadata retain their accepted
bytes. The existing scope/spec/resource rejection tests remain the enforcement
checks. Later authorized steps update that same current boundary as necessary;
no historical dispatch or additional approval mechanism is added.

Current specification checking requires this plan and decision record. Preserve
frozen Phase 0 specifications and existing formula ownership. Targeted fixture,
order, representation, provenance or lineage checks may run where they validate
the actual new acceptance inputs. Full candidate matrices, package rebuilds,
100k measurements and publication are outside this step.

See [PHASE_6A_STEP_1.md](PHASE_6A_STEP_1.md) for actual completed changes and
verification. Step 2 remains the next separately authorized implementation step.
