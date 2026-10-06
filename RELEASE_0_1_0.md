# Recursive Integrity Toolkit 0.1.0 release preparation

Request date: 2026-10-02 UTC (2026-10-01 in America/Los_Angeles).
Verification completed: 2026-10-02.
Independent assistant handoff rehearsal executed: 2026-10-06; human review pending.
Status: PREPARATION VERIFIED; PUBLICATION PENDING. No public release or registry upload is claimed.

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
protected product files, all other bytes in the two version owners, the 41-module
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

The tested 0.1.0 preparation is `c5837845da603167e6f0c8216766d0a3a874835e`,
tree `030fb987c9785ab7a4061c25302d079f9a37b341`, on `release-0.1.0`.
[PR #5](https://github.com/DavidWallstructurallaw/recursive-integrity-toolkit/pull/5)
retains the preparation as a draft. The existing complete candidate workflow
is [run 36976926784](https://github.com/DavidWallstructurallaw/recursive-integrity-toolkit/actions/runs/36976926784).
All required candidate jobs completed successfully, including performance and
dependent hosted delivery. The sections below retain their exact evidence scopes.

The three source/specification/traceability checks passed. Local gate/workflow
regression passed 67 tests in 6.16 seconds; the affected version/report/installed
selection passed 375 in 66.66 seconds through a newly wheel-installed interpreter.
Five current goldens were checked against the accepted Git blobs to contain only
exact version-token substitutions. No scientific expected values changed.

### Supported environment checks

| Profile | Python | NumPy | pandas | PyArrow | Passed | pytest s |
| --- | --- | --- | --- | --- | ---: | ---: |
| Core (current) on ubuntu-latest with Python 3.11 | 3.11.16 | 2.4.6 | 3.0.6 | absent, asserted | 4044 | 366.63 |
| Core (current) on ubuntu-latest with Python 3.12 | 3.12.14 | 2.5.3 | 3.0.6 | absent, asserted | 4044 | 404.63 |
| Core (current) on windows-latest with Python 3.11 | 3.11.9 | 2.4.6 | 3.0.6 | absent, asserted | 4044 | 437.06 |
| Core (current) on windows-latest with Python 3.12 | 3.12.10 | 2.5.3 | 3.0.6 | absent, asserted | 4044 | 488.96 |
| Core (minimum) on ubuntu-latest with Python 3.11 | 3.11.16 | 2.0.0 | 2.2.2 | absent, asserted | 4044 | 197.65 |
| Core (minimum) on ubuntu-latest with Python 3.12 | 3.12.14 | 2.0.0 | 2.2.2 | absent, asserted | 4044 | 402.47 |
| Core (minimum) on windows-latest with Python 3.11 | 3.11.9 | 2.0.0 | 2.2.2 | absent, asserted | 4044 | 333.77 |
| Core (minimum) on windows-latest with Python 3.12 | 3.12.10 | 2.0.0 | 2.2.2 | absent, asserted | 4044 | 411.28 |
| Real optional Parquet on Ubuntu with Python 3.12 | 3.12.14 | 2.5.3 | 3.0.6 | 25.0.1 | 4054 | 315.26 |
| hero / hero-contract | 3.12.14 | 2.5.3 | 3.0.6 | core-only install | 311 | 41.09 |
| security / local-first-boundary | 3.12.14 | 2.5.3 | 3.0.6 | core-only install | 2027 | 157.35 |

The eight 4,044-case core identity sets equal the current canonical collection.
Real Parquet equals the 4,054-case collection with exactly ten required optional
cases. All actual JUnit cases have zero failures, errors and skips. Counts overlap
between jobs. Core PyArrow absence is directly asserted and agrees with the
resolved dependency lists. Hero/security dependencies and exact source are
verified from checkout/install logs. All eleven evidence ZIPs match GitHub's
size and SHA-256 and pass CRC checks.

The separately scheduled focused PR run
[36976926727](https://github.com/DavidWallstructurallaw/recursive-integrity-toolkit/actions/runs/36976926727)
also passed: 1,153 tests in 10.44s, 483 in 145.34s, 637 in 82.71s and 508 in 27.00s.
The candidate workflow deliberately leaves the alternative focused job unselected.

### Local package preflight

Python 3.12.14, build 1.6.1 and setuptools 84.0.0 built a source distribution and
then its wheel from a clean committed source snapshot. Strict twine checks passed.
A new environment received the actual wheel with
`pip --ignore-installed --no-index --no-deps`; isolated imports resolved version
0.1.0 from its own site-packages. Existing test dependencies were supplied through
a separate retained path that also contains an older toolkit installation.
The new environment's package took precedence, with both file origin and installed
version asserted. NumPy was 2.5.3 and pandas 3.0.6. This is a shared-dependency
local preflight, distinct from the fresh hosted profiles.

| Local artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| Wheel | 393068 | `b1fc9500f978bd58092704aa91de1c8dc4115c4c8cd4891f6a705afa9d49f666` |
| Source distribution | 361459 | `bf045a234ffc01f6da1c07534f28c4b6a124b1da6eb5d29691a880483ff4955c` |

The existing full installed checks passed package import, input validation,
mathematics, privacy, JSON/Markdown, output safety, CLI and packaged examples,
including independent scenario arithmetic, replay and blocked network.
All 41 module files and 18 resources match the source. Sdist smoke executes its
safely extracted source; the built wheel itself was produced from the sdist.
No second independent sdist installation is asserted here.

The initial lookup of a historical build-environment executable found that it
was no longer present. The available Python runtime with retained build/test
dependencies supplied the preflight. This setup lookup did not produce a failed
product build or test; every executed release-preparation test above passed.
The successful dev6 measurements and artifacts remain bound to their named
candidate in PHASE_6B_COMPLETION.md and are not relabeled as 0.1.0 results.

## Current performance acceptance

Performance job `110742650107` passed every required case once: the separate
actual 100k longitudinal invocation passed 1 test in 995.94s of pytest console
time; the retained invocation passed 20 tests in 1080.75s. Its one deselection
is the separately executed 100k case. Both JUnit files have zero failures,
errors and skips, and their 21 unique identities match current collection.

[Performance artifact 11214867697](https://github.com/DavidWallstructurallaw/recursive-integrity-toolkit/actions/runs/36976926784/artifacts/11214867697)
contains 97,209,329 bytes, SHA-256
`3cfe8162ba592323bd6ce6d4b13a554051448c27d7b488133cc311a969b9eed9`.
GitHub size/digest and all 260 member CRCs match. The complete archive is
retained; 148 ordinary members were extracted and 112 redundant `*current`
alias members excluded from observation counts. All 131 recorded input
references match their SHA-256 and lengths; all 48 report lengths match.
There are 24 CLI attempts, one ancestry API attempt and seven traced calculation
observations. Every measured process exited zero without timeout. No retries
or fastest-attempt selection occurred.

The reference environment was AMD EPYC 7763 64-Core, four visible logical CPUs,
Linux 6.17.0-1022-azure x86_64/glibc 2.39, Python 3.12.14, NumPy 2.5.3,
pandas 3.0.6 and pytest 9.1.1; PyArrow was absent. Host RAM was
16,766,414,848 bytes and configured swap 3,221,221,376 bytes.

Outer wall includes interpreter startup, imports, complete publication and
measurement bookkeeping; input construction and parent assertions are excluded.
CLI time begins before imports and ends after JSON/Markdown publication.
Scenario time measures only the experiment call, excluding report assembly.
API time covers validation, graph/ancestry assertions and summary output, with
no full audit report. Linux RSS uses executed-image `VmHWM` high-water marks
without subtracting the pre-CLI reading. Traced Python allocation is a different
measure and is not total process RSS.

### Every CLI and API attempt

| Workload / attempt | Mode | Outer s | CLI / worker s | Scenario s | RSS before B | RSS peak B | JSON / API B | Markdown B |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| longitudinal_100000, 1 | untraced | 990.297926 | 990.081419 | n/a | 14,069,760 | 7,347,503,104 | 427,983,686 | 266,479,088 |
| hero_complete_reports, 1 | untraced | 0.740980 | 0.681098 | n/a | 14,065,664 | 42,483,712 | 209,417 | 185,625 |
| hero_complete_reports, 2 | untraced | 0.734110 | 0.678032 | n/a | 14,065,664 | 42,479,616 | 209,416 | 185,624 |
| hero_complete_reports, 3 | untraced | 0.732234 | 0.675718 | n/a | 14,041,088 | 42,369,024 | 209,417 | 185,625 |
| hero_complete_reports, 4 | traced | 3.976660 | 3.903638 | n/a | 14,032,896 | 58,519,552 | 209,416 | 185,624 |
| hero_lineage_complete_reports, 1 | untraced | 0.771735 | 0.714319 | n/a | 14,139,392 | 43,114,496 | 242,114 | 218,641 |
| hero_lineage_complete_reports, 2 | untraced | 0.773477 | 0.716446 | n/a | 14,139,392 | 43,122,688 | 242,113 | 218,640 |
| hero_lineage_complete_reports, 3 | untraced | 0.764130 | 0.707705 | n/a | 14,143,488 | 43,110,400 | 242,114 | 218,641 |
| longitudinal_1000, 1 | untraced | 9.367430 | 9.300661 | n/a | 14,143,488 | 110,071,808 | 4,417,801 | 3,020,661 |
| longitudinal_10000, 1 | untraced | 95.029868 | 94.945441 | n/a | 14,045,184 | 774,144,000 | 42,907,998 | 26,943,379 |
| longitudinal_20_versions_220_records, 1 | untraced | 5.629277 | 5.565835 | n/a | 14,143,488 | 76,169,216 | 3,377,582 | 4,086,956 |
| longitudinal_hero / distribution, 1 | untraced | 0.887515 | 0.827560 | n/a | 14,209,024 | 43,511,808 | 283,855 | 318,666 |
| longitudinal_hero / distribution, 2 | untraced | 0.894519 | 0.835234 | n/a | 14,213,120 | 43,606,016 | 283,854 | 318,665 |
| longitudinal_hero / distribution, 3 | untraced | 0.897337 | 0.835097 | n/a | 14,217,216 | 43,511,808 | 283,855 | 318,666 |
| longitudinal_hero / lineage, 1 | untraced | 0.964710 | 0.902761 | n/a | 14,094,336 | 43,401,216 | 312,575 | 342,622 |
| longitudinal_hero / lineage, 2 | untraced | 0.933844 | 0.874684 | n/a | 14,213,120 | 43,536,384 | 312,575 | 342,622 |
| longitudinal_hero / lineage, 3 | untraced | 0.948368 | 0.888698 | n/a | 14,090,240 | 43,429,888 | 312,575 | 342,622 |
| metadata_100k_complete_reports, 1 | untraced | 776.855068 | 776.747237 | n/a | 14,008,320 | 7,681,265,664 | 442,741,949 | 165,121,768 |
| simulation_small, 1 | untraced | 0.757878 | 0.691502 | 0.067341 | 14,098,432 | 54,906,880 | 163,605 | 139,553 |
| simulation_small, 2 | untraced | 0.753078 | 0.689276 | 0.067391 | 14,204,928 | 55,201,792 | 163,605 | 139,553 |
| simulation_small, 3 | untraced | 0.757192 | 0.693231 | 0.068023 | 14,209,024 | 55,058,432 | 163,605 | 139,553 |
| simulation_representative, 1 | untraced | 7.848551 | 7.778378 | 0.150602 | 14,188,544 | 168,878,080 | 8,229,315 | 194,587 |
| lineage_chain_1000, 1 | untraced | 8.497836 | 8.435485 | n/a | 14,118,912 | 145,326,080 | 6,203,340 | 1,534,130 |
| lineage_reverse_chain_100000_api, 1 | untraced API | 67.420686 | 66.925394 | n/a | not recorded | 1,851,367,424 | 938 | not produced |
| lineage_fan_in_64, 1 | untraced | 1.746752 | 1.689272 | n/a | 14,139,392 | 50,524,160 | 612,010 | 286,520 |

### Scientific and resource scope

The 100k longitudinal input contains 100 context anchors and three selected
populations of 33,300 records, with three comparisons. Graph work remains
100,000 nodes, 99,900 edges, 100,000 stored root memberships and 99,900 union
visits. Its full reports total 694,462,774 bytes and its 990.297926-second outer
interval passes the unchanged 1,800-second guard.

Ordinary 100k metadata retains 100 equally occupied states, source shares 0.18
each, 10% missing provenance and direct closure interval [0.18, 0.64].
Its full-report interval is 776.855068 seconds, within the same 1,800-second
guard. The 100k reverse-chain API retains depth 99,999, one root, G/C/U =
100,000/0/0, HHI and effective roots 1. Validation takes 26.811385 seconds and
ancestry 40.056579 seconds; the 67.420686-second outer interval passes 600 seconds.

Both simulation profiles contain two independent fictional audit records and
zero-record scenario scopes. The small profile admits 84 cells (two models,
K=2, horizon=6, replicates=3, n=2). The representative profile admits 33,280
cells (two models, K=32, horizon=64, replicates=8, n=64). Both use seed 17 and
lambda 1/4; full path/count/source/event oracles and truthful Markdown omission
disclosures pass. The representative complete report takes 7.848551 seconds,
of which 0.150602 seconds is the experiment call. These are bounded observations
with no million-cell runtime claim or empirical causal interpretation.

All twelve untraced ordinary/lineage/longitudinal Hero attempts are below the
existing five-second reference target. The separate traced Hero attempt retains
11,421,965 current and 19,454,790 peak Python allocation bytes; its wall time
includes tracing overhead. The 20-version/220-record workload is a separate,
larger workload with 37 pairs and is not the tiny canonical Hero.

### Retained calculation observations

| Calculation | Traced wall s | Traced Python peak B |
| --- | ---: | ---: |
| hero_input_plus_calculations | 0.120651 | 1,695,001 |
| metadata_100k_setup | 28.461898 | 265,131,522 |
| metadata_100k_field_representation | 7.277994 | 66,295,688 |
| metadata_100k_support_diversity | 4.979652 | 39,070,984 |
| metadata_100k_provenance_join | 14.927903 | 112,088,900 |
| metadata_100k_composition | 15.071485 | 70,367,904 |
| metadata_100k_exact_duplicates | 7.561808 | 88,422,856 |

### Comparison and output limitations

The 32 matched observation comparisons use the previous dev6 candidate
`1e1fcd1466db92c3a39591cf5740331a79f910eb`, run `36784026671`.
Input hashes, workload identity, attempt and tracing mode match. Python,
dependency versions and OS/kernel match; CPU changed from EPYC 9V74 to EPYC
7763. Both runs use the same executed-image VmHWM method for process RSS.
Physical host allocation/load were uncontrolled. No observation crossed the
+20% time or +50% recorded-memory review thresholds; maximum observed increases
were 11.2197% and 0.3209%, respectively. These are observations under
stated conditions, not a hardware-independent latency or memory SLA.

The full 100k reports still require roughly 7.35-7.68 billion bytes of peak
process RSS and hundreds of MB of report output. API-only results exclude that
publication cost. Version-only metadata changes do not establish a product
performance improvement.

| Growth input | Warning entries | JSON B | Markdown B | stderr B |
| ---: | ---: | ---: | ---: | ---: |
| 100 records | 66 | 548276 | 273307 | 41692 |
| 400 records | 264 | 1875284 | 767051 | 166930 |

Fourfold input growth stays within the existing 6x structural output bound.
This in-process growth check is not another timing/RSS observation. Complete
100k longitudinal stderr remains 97,991,102 bytes with 149,850 generation
mismatch entries; metadata stderr remains 42,049,360 bytes with 30,000 missing
provenance and 36,000 unknown-grounding entries. Diagnostics were not suppressed.

## Hosted package and source delivery

Delivery job `110752197955` passed on the exact tested candidate.
[Delivery artifact 11214578521](https://github.com/DavidWallstructurallaw/recursive-integrity-toolkit/actions/runs/36976926784/artifacts/11214578521)
is 3,430,551 bytes, SHA-256
`9a70beee7b21dec9e633a096f8954946953faf6ccb4234ac2a948b35986e6c92`.
Its size/digest and all 24 member CRCs match. Reused core and Parquet JUnit files
are byte-identical to the verified matrix originals.

The build environment used Python 3.12.14, build 1.6.1, setuptools 84.0.0 and
twine 7.0.0. `SOURCE_DATE_EPOCH=1790924821` matches the candidate timestamp.
The wheel is built from the sdist by the existing default build sequence.

| Verified candidate artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `recursive_integrity_toolkit-0.1.0-py3-none-any.whl` | 393068 | `b1fc9500f978bd58092704aa91de1c8dc4115c4c8cd4891f6a705afa9d49f666` |
| `recursive_integrity_toolkit-0.1.0.tar.gz` | 361674 | `4f6c775b1b0a0f7db01a945d9da92f8cc4bc41efa8e5c74a5b6cae644c0527a4` |
| `recursive-integrity-toolkit-source.zip` | 1773426 | `dac6a2185c5b6c0e71cec6927582ca9c32092b4238b62428293b7ad3660a993f` |

Repeated hosted wheel bytes are identical. The local preflight wheel is also
byte-identical to the hosted wheel. Every repeated sdist file payload matches,
while compressed bytes differ; the second hosted sdist SHA-256 is
`c1909cabc35b6abb39ccc63623b305c8ba34f23a3f2ac42abb0a9a2d4026e000`.
The source ZIP contains exactly 355 tracked files under one root, each matching
`git archive` of the candidate. Git internals, caches, environments and uploaded
theory PDFs are excluded. Both package forms contain the exact 41 runtime
modules, 18 canonical resources and required license/notice bytes.

The actual wheel was installed into temporary targets outside the checkout.
Installed input/API/mathematics/privacy/rendering/output/CLI checks and all
packaged examples passed. Sdist smoke runs safely extracted source; it is not
a second independent pip installation. These scopes remain distinct.
Import/isolated-input checks and numerical execution retain their separate
dependency boundaries, with network blocked where required.

All 13 required candidate jobs passed in this one candidate run. No hosted retry
or failed release-preparation build/test attempt occurred. The later update to
this record is documentation-only; executable, resource, workflow and test bytes
remain those of `c5837845`. Artifact hashes identify that tested candidate, not
a new source archive from the documentation successor. Existing administrative
evidence-reuse policy applies.

## Official publication requirements

UD-032 and GOVERNANCE_AND_HANDOFF.md require Theory Owner and Technical
Maintainer approval for `official-v0.1`. The user's current instruction records
merge and preparation authority. MAINTAINERS.md still lists the Technical
Maintainer as unassigned or acting; no named maintainer sign-off is invented.
The same person may hold multiple roles if that consolidation is declared.

GOVERNANCE_AND_HANDOFF.md section 31 requires a handoff rehearsal by a reviewer
who did not author the implementation. A fresh independent assistant reviewer
executed all nine steps on 2026-10-06 at documentation successor
`9fac436dc619900b19bc0ad4fa3cd38d3087435c`: clone, install, run Hero, locate
definitions and a trace owner, run a unit test, build, identify blockers and
explain unavailable conclusions. [HANDOFF_REHEARSAL.md](HANDOFF_REHEARSAL.md)
records the execution evidence, new rehearsal-build hashes and limitations.
This is an independent assistant rehearsal, not an external human review or
maintainer appointment. Human review of the record remains pending under
GOVERNANCE_AND_HANDOFF.md section 28.4; named release approvals remain pending.
The rehearsal builds do not replace the candidate artifacts identified above.

This follow-up adds the rehearsal record and updates this release record only.
Product, test, resource and workflow files retain the tested candidate bytes.
The existing administrative evidence-reuse policy applies; no new full candidate
run is claimed.

Before public publication:

1. Current version/package verification is complete, as recorded above.
2. Review and accept the recorded independent handoff rehearsal; record the
   Technical Maintainer appointment and approval.
3. Confirm the official release approval and exact target commit.
4. Create tag `v0.1.0` and the GitHub Release with verified artifacts and checksums.
5. Treat any package-registry upload as a separate requested action.

This preparation preserves the read-only verification workflows and does not add
release credentials, publication automation or a new approval registry. UD-017
continues to authorize experimental scenarios; UD-031 empirical ingestion remains
deferred. No new theory or product-scope decision is introduced.
