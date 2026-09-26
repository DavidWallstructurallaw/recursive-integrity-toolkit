# Phase 5 Completion and Candidate Verification

Status: **PHASE 5 COMPLETE; ALL 13 REQUIRED CANDIDATE JOBS PASSED**.

The Theory Owner instructed `Phase 5 Step 10` on 2026-09-26 UTC. Development
version is `0.1.0.dev4`; report schema remains `1.1`.

| Reference | Value |
|---|---|
| Starting Step 9 commit | `15d50c3d992265e716b0b27e69c43107d947d21d` |
| Tested code candidate | `53802fb0e99ea867a27bb82210cc9fa32d8e02d1` |
| Tested candidate tree | `5f235a4e008f65d0cb76d0af2e5b7d929271f018` |
| Branch / draft PR | `phase5-lineage`; [PR #2](https://github.com/DavidWallstructurallaw/recursive-integrity-toolkit/pull/2), based on the accepted unmerged Phase 4 branch |
| Candidate workflow | [Run 36270399128](https://github.com/DavidWallstructurallaw/recursive-integrity-toolkit/actions/runs/36270399128) |

## Candidate scope

Steps 1-9 implement retained parent evidence, canonical graphs, cycles and depth,
strict external ancestry, G/C/U partition, root concentration, lineage closure
bounds, descriptive shared-root evidence, schema 1.1 and explicit CLI/context
integration. Step 10 updates version metadata, public documentation and the
existing candidate verification path. All analytical source, frozen scientific
definitions, canonical Hero inputs and schema resources retain Step 9 bytes.

Two existing Parquet context tests now use the explicit dependency profile,
matching the original three real-PyArrow cases. Candidate selection adds a PR
label event to the existing workflow because the default branch still contains
the early workflow without manual dispatch. No additional workflow, source
migration framework or evidence registry is introduced.

## Acceptance gates

The following completed jobs checked out the exact candidate above. JUnit
artifacts and dependency profiles were retrieved from this run. Every executed
test in these jobs passed, with zero failures, errors or skips.

| Role | Python / NumPy / pandas | Passed |
|---|---|---:|
| Ubuntu current | 3.11.16 / 2.4.6 / 3.0.6 | 2,960 |
| Ubuntu current | 3.12.14 / 2.5.3 / 3.0.6 | 2,960 |
| Ubuntu minimum | 3.11.16 / 2.0.0 / 2.2.2 | 2,960 |
| Ubuntu minimum | 3.12.14 / 2.0.0 / 2.2.2 | 2,960 |
| Windows current | 3.11.9 / 2.4.6 / 3.0.6 | 2,960 |
| Windows current | 3.12.10 / 2.5.3 / 3.0.6 | 2,960 |
| Windows minimum | 3.11.9 / 2.0.0 / 2.2.2 | 2,960 |
| Windows minimum | 3.12.10 / 2.0.0 / 2.2.2 | 2,960 |
| Ubuntu real Parquet | 3.12.14 / 2.5.3 / 3.0.6; PyArrow 25.0.1 | 2,965 |
| Hero and mathematical contracts | Ubuntu / Python 3.12 | 279 |
| Security and local boundaries | Ubuntu / Python 3.12 | 1,992 |
| Designated reference performance | Ubuntu / Python 3.12 | 13 |
| Dependent package and delivery checks | Ubuntu / Python 3.12 | PASS |

The eight core jobs verify actual PyArrow absence. Real Parquet includes all
five optional cases, including both lineage context paths. Current dependencies
are the resolved compatible versions for each Python, rather than one shared
NumPy pin. These supported profiles do not certify every Python/OS/version
combination permitted by broad package declarations.

Local preflight ran all 2,965 canonical cases with real PyArrow in 157.46 seconds
and 136 affected cases in an actual no-PyArrow environment. Source/specification/
traceability checks and affected document links passed. Golden edits in Step 10
were verified to change package-version strings only.

Candidate run 36270399128 completed successfully on its first attempt. Its
unselected focused job was intentionally skipped; no required test was skipped.
The PR-open focused run 36270393683 also passed. There were no failed candidate
jobs or hidden retries. Completed logs and all candidate artifacts were
retrieved successfully.

## Performance observations and review

The designated hosted profile was Ubuntu 24.04.5, Linux 6.17.0-1022-azure,
glibc 2.39, AMD EPYC 7763 with four visible CPUs, 16,766,410,752 bytes host memory
and 3,221,221,376 bytes configured swap. Python was 3.12.14, NumPy 2.5.3,
pandas 3.0.6, pytest 9.1.1 and PyArrow absent. The 13-case performance suite
passed in 954.63 seconds. Full-scale tests ran once on this designated profile.

| Workload and scope | Outer wall seconds | Recorded whole-process peak RSS bytes | Output bytes |
|---|---:|---:|---|
| Hero with lineage, attempt 1 | 0.683194 | 42,614,784 | JSON 240,782; Markdown 216,519 |
| Hero with lineage, attempt 2 | 0.676312 | 42,614,784 | JSON 240,782; Markdown 216,519 |
| Hero with lineage, attempt 3 | 0.678967 | 42,614,784 | JSON 240,783; Markdown 216,520 |
| Actual 100k reverse-chain input and ancestry API | 66.225214 | 1,848,307,712 | API summary 937; no audit report |
| 1,000-target chain, complete lineage CLI | 8.440556 | 1,785,204,736* | JSON 6,201,924; Markdown 1,531,924 |
| 64 context roots and 64 targets, complete lineage CLI | 1.653459 | 1,785,204,736* | JSON 610,566; Markdown 284,286 |
| Retained 100k metadata audit, complete ordinary CLI | 780.729803 | 7,681,183,744 | JSON 442,740,533; Markdown 165,119,562 |

All three untraced lineage Hero attempts meet the under-five-second target on
this profile. Ordinary Hero attempts were 0.660752, 0.654029 and 0.655411 seconds.
Its separate allocation-traced attempt was 3.560648 seconds with 14,652,609 bytes
peak traced Python allocations; it is not an untraced throughput measurement.

The 100k chain has 100,000 target nodes, 99,999 edges, no context nodes,
100,000 root memberships, 99,999 union visits and depth 99,999. G/C/U is
100,000/0/0, with one root, HHI 1 and effective roots 1. Validation took
26.480915 seconds and ancestry 39.209371 seconds. This scope includes loading,
generation validation and ancestry, and excludes ordinary metrics and full
JSON/Markdown audit serialization. The bounded fan-in case has 4,096 edges,
4,160 memberships, 4,096 visits and depth 1. The metadata audit checks all
100,000 records, independent arithmetic and 66,000 retained warnings.

*Memory review:* both bounded hosted CLI cases already recorded a
1,785,204,736-byte high-water mark before CLI invocation, unchanged afterward.
That pre-invocation floor cannot establish a new 1.66 GiB CLI memory requirement.
A narrowly selected two-case recheck on the unchanged candidate runtime passed
in 13.59 seconds. On the Step 9 reference container, the 1,000-target CLI took
11.099089 seconds with a 29,306,880-byte pre-CLI mark and a 131,702,784-byte peak;
fan-in took 1.964126 seconds with a 48,889,856-byte mark both before and after.
The fan-in observation remains bounded by its pre-CLI floor and is not an
incremental allocation estimate. This recheck used Python 3.12.14, NumPy 2.3.5,
pandas 2.2.3 and installed but unused PyArrow 25.0.1 on the Xeon 8370C container
documented in Step 9. It did not rerun the 100k workloads or candidate matrix.

The comparable local chain result remains close to Step 9's 11.152764 seconds
and 131,334,144-byte peak, below the approved regression-review thresholds.
Hosted/container timing differences are separate observations, not a claimed
product speedup. Raw pre-invocation RSS, every measured attempt and all scopes
remain in their respective JUnit records. No timing guard or resource threshold
was relaxed, and no product change was needed for the review.

## Packaging, installation and reproducibility

Delivery job 108485664963 passed on the exact candidate after all prerequisite
jobs. It reused this run's complete core/Parquet JUnit with source-commit checks,
then verified complete current test identities, strict wheel/sdist metadata,
40 shipped Python modules, seven canonical resources and clean installed
behavior outside the checkout. Installed checks covered import/input-only
boundaries, mathematical APIs, report/privacy/output behavior and ordinary plus
explicit-lineage Hero in standard/redacted modes with network blocked. Both
wheel and sdist paths passed the existing installed checks.

Two builds used the same committed source, recorded build environment and
`SOURCE_DATE_EPOCH=1790455223`. Wheel bytes were identical. Every sdist file
payload matched; compressed sdist container bytes differed because timestamps
may differ. This establishes the documented same-environment reproducibility
scope. It does not claim identical bytes across arbitrary toolchains.

| Delivered artifact | Bytes | SHA-256 |
|---|---:|---|
| `recursive_integrity_toolkit-0.1.0.dev4-py3-none-any.whl` | 284,740 | `e7d763ea05fc30cb2fdfea298cf1ef7f1ecbe8c0a273907d35676afdb41fbb9a` |
| `recursive_integrity_toolkit-0.1.0.dev4.tar.gz` | 256,685 | `5b0c6d88f4488150ccded959bdedeabdafa93f97ad4af513704b7d5e69822655` |
| `recursive-integrity-toolkit-source.zip` | 1,307,831 | `0df49b1a3f3dd837be2082bc98836a71377148715d72ca61a93bca96fce20551` |

The source ZIP was checked against all 273 tracked candidate files and their
exact bytes. [Delivery artifact 10915637271](https://github.com/DavidWallstructurallaw/recursive-integrity-toolkit/actions/runs/36270399128/artifacts/10915637271)
contains the packages, candidate source ZIP, dependency records, complete reused
JUnit, build/install logs and reproducibility results. [Performance artifact
10916225143](https://github.com/DavidWallstructurallaw/recursive-integrity-toolkit/actions/runs/36270399128/artifacts/10916225143)
contains the raw scale observations. These hosted ZIPs were retrieved and their
downloaded bytes matched the reported artifact digests. GitHub retention is
90 days for delivery and 30 days for other job evidence; this completion record
and prior phase records remain recoverable from Git.

## Administrative handoff

The final administrative successor changes only this completion report. The
other 272 tracked entries retain the tested candidate's exact mode, type and
blob identity. Existing source/specification/traceability and affected document
checks pass. Candidate evidence is reused under the approved governance policy;
no second full matrix is claimed. The archived code candidate contains the
earlier pending form of this report; the final report records its completed
results separately. A skipped administrative CI run does not imply merge-ready
branch-protection status.

## Scientific and operational limits

Root identity and structural depth describe declared topology. They do not
certify independently generated evidence, truth, quality or causal dependence.
Missing, unknown and unresolved evidence remains explicit. The primary version
owns the target denominators; context records supply ancestors only. The
shared-root proxy is descriptive and does not provide a calibrated risk score.

The frozen Hero has eight resolved v2 targets, five roots, HHI 1/4, effective
roots 4 and lineage bounds [0,0], while direct bounds remain [1/2,1/2]. The
independent partial oracle and adversarial cases preserve incomplete evidence.

[Step 9](PHASE_5_STEP_9.md) records seven detected meaningful mutations and the
actual 100k reverse-chain input/ancestry run: 123.36 seconds and 1.71 GiB peak RSS.
That measurement excludes ordinary metrics and full audit serialization. The
1,000-record complete lineage CLI took 11.15 seconds. These scopes differ from
the historical Phase 4 metadata-only 100k audit. Timeouts and finite graph/root
limits are engineering resource guards, not scientific thresholds or performance
SLAs. Inputs are intended for trusted stable local filesystems as documented.

Phase 6A longitudinal orchestration and Phase 6B reopening/experiments remain
deferred. This milestone does not merge a PR, tag or publish a package, or claim
final v0.1 completion.
