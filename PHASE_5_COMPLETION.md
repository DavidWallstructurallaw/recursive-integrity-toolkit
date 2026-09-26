# Phase 5 Completion and Candidate Verification

Status: **STEP 10 IN PROGRESS; CANDIDATE ACCEPTANCE PENDING**.

The Theory Owner instructed `Phase 5 Step 10` on 2026-09-26 UTC. The starting
commit is `15d50c3d992265e716b0b27e69c43107d947d21d` on `phase5-lineage`.
Development version is `0.1.0.dev4`; report schema remains `1.1`.

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

Complete core regression on Ubuntu/Windows, Python 3.11/3.12 and current/minimum
dependencies; real Parquet; Hero/math; security; one reference performance job;
and dependent build, clean-install and reproducibility checks are required.
No pending gate is counted as a pass. Actual candidate identifiers, outcomes,
failed attempts and artifact availability will replace this pending record.

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
