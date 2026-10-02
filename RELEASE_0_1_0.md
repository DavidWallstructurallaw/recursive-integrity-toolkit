# Recursive Integrity Toolkit 0.1.0 release preparation

Date: 2026-10-02 UTC (2026-10-01 in America/Los_Angeles).
Status: PREPARATION IN PROGRESS. No public release or registry upload is claimed.

The Theory Owner requested: `合并 PR，再准备正式版本和 Release`.
This authorizes the accepted PR merges and preparation of version 0.1.0 and its
release materials. Official publication requirements remain explicit below.

## Merged implementation

| PR | Scope | Merge commit on main |
| --- | --- | --- |
| [#1](https://github.com/DavidWallstructurallaw/recursive-integrity-toolkit/pull/1) | Phase 4 reports and CLI | `765aa0628eb267e07278c98a7d7b58a8fdc60072` |
| [#2](https://github.com/DavidWallstructurallaw/recursive-integrity-toolkit/pull/2) | Phase 5 lineage | `debfdfbd28318ab96f4370fc3f4ae33be296e592` |
| [#3](https://github.com/DavidWallstructurallaw/recursive-integrity-toolkit/pull/3) | Phase 6A longitudinal | `3855b390e6cf46c70add7c7ec4be6261cfb68f07` |
| [#4](https://github.com/DavidWallstructurallaw/recursive-integrity-toolkit/pull/4) | Phase 6B experimental simulation | `dd4646cda6eedb00af261441c1e58f226415e935` |

The merges preserve original commits and use the reviewed head SHA of each PR.
The final main tree is `bfdb283a158061f577c7642aa6a85263bf72270c`, exactly equal
to accepted Phase 6B handoff `64bc1ce627e79f6960a5a17b0ac401246155549c`.
No source content changed while merging. Prior successful candidate workflows
were rechecked before the merges; no branch-protection requirement was bypassed.

## Proposed release identity

- Canonical repository: <https://github.com/DavidWallstructurallaw/recursive-integrity-toolkit>.
- Package: `recursive-integrity-toolkit`, version `0.1.0`.
- Planned tag: `v0.1.0`, not created by this preparation.
- Report schema: `1.3`.
- Theory versions and canonical references: [THEORY_SOURCES.md](THEORY_SOURCES.md).
- Licensing: [LICENSING_NOTES.md](LICENSING_NOTES.md), [LICENSE](LICENSE),
  [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

Only the two package-version tokens change in product files. The other 81
protected product files, all other bytes in the two version owners, 41 module
inventory, 18 canonical packaged resources and 16 frozen specifications remain
unchanged. The five current report goldens change only toolkit-version metadata.
No numerical expectation, input contract, dependency, resource guard or privacy
behavior is changed. The existing source-scope check advances its single accepted
reference to the Phase 6B handoff and permits exactly dev6-to-0.1.0 in both owners.

## Release notes draft

Recursive Integrity Toolkit is a local-first research toolkit for supplied-data
audits of recursive reuse, support/diversity, provenance gaps, closure exposure,
ancestry and ordered version changes. It writes inspectable JSON and Markdown
reports with explicit evidence classes, assumptions and unavailable conclusions.

The initial release includes:

- CSV/JSONL ingestion, optional Parquet, declarative mapping and input-only validation.
- Exact record-form and declared categorical support/diversity, duplicate and
  tail diagnostics, provenance composition and direct closure intervals.
- Explicit lineage graphs, cycle/depth checks, strict external roots, ancestry
  concentration and lineage closure intervals with incomplete ancestry retained.
- Explicit ordered longitudinal comparison with adjacent and optional baseline
  pairs, compatibility checks and protected per-snapshot/per-pair results.
- Explicit closed and constant-source reopened categorical experiments with
  fixed seeds, separate closed expectations, complete transition events and
  per-path comparisons. All scenario evidence remains experimental simulation.
- Standard and redacted JSON/Markdown, safe no-overwrite publication, two console
  aliases and installed Hero, longitudinal and simulation examples.

Compared with dev6, this preparation changes only package-version metadata and
release material. Public field meanings, formulae, evidence classes, theory
versions and schema 1.3 are unchanged. Strict older schema readers must adopt
schema 1.3 explicitly; same-environment replay does not promise identical random
paths across dependency versions or platforms.

There is no universal integrity/collapse score, empirical causal-intervention
ingestion, model-performance certification, external-source quality inference or
guarantee that reopening improves every realized path. HTML, remote services,
telemetry and automatic enforcement remain outside the release scope. Large
complete reports can require several GB of memory and hundreds of MB of output;
[Phase 6B measurements](PHASE_6B_COMPLETION.md) retain their exact dev6 source,
environment, workload and measurement limits.

## Current validation and artifacts

Verification of the 0.1.0 preparation and its newly built artifacts is pending.
The successful dev6 matrix and artifacts remain historical, explicitly bound
to candidate `1e1fcd1466db92c3a39591cf5740331a79f910eb`; they are not relabeled
as 0.1.0 packages. Current results will be recorded here after execution.

## Official publication requirements

UD-032 and GOVERNANCE_AND_HANDOFF.md require Theory Owner and Technical
Maintainer approval for `official-v0.1`. The user's current instruction records
merge and preparation authority. MAINTAINERS.md still lists the Technical
Maintainer as unassigned or acting; no named maintainer sign-off is invented.
The same person may hold multiple roles if that consolidation is declared.

GOVERNANCE_AND_HANDOFF.md section 31 also requires a handoff rehearsal by a
reviewer who did not author the implementation: clone, install, run Hero, locate
definitions and a trace owner, run a unit test, build, identify blockers and
explain unavailable conclusions. No completed HANDOFF_REHEARSAL.md is currently
recorded. Existing assistant test reviews do not supply an unrecorded human role
appointment or a completed independent handoff rehearsal.

Before public publication:

1. Complete and record current version/package verification.
2. Record the required independent handoff rehearsal and maintainer approval.
3. Confirm the official release approval and exact target commit.
4. Create tag `v0.1.0` and the GitHub Release with verified artifacts and checksums.
5. Treat any package-registry upload as a separate requested action.

This preparation preserves the read-only verification workflows and does not add
release credentials, publication automation or a new approval registry. UD-017
continues to authorize experimental scenarios; UD-031 empirical ingestion remains
deferred. No new theory or product-scope decision is introduced.
