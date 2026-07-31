# SUCCESS_CRITERIA

## Document control

| Field | Value |
|---|---|
| Project | Recursive Integrity Toolkit |
| Target release | v0.1 |
| Phase | Phase 0 |
| Status | APPROVED PHASE 0 BASELINE |
| Primary owner | Theory Owner |
| Reviewers | Technical Maintainer, Mathematical Reviewer, Security Reviewer, Domain Validator |
| Depends on | `V0.1_PRODUCT_SPEC.md`, `VALIDATION_PLAN.md`, `THEORY_TO_CODE_TRACEABILITY.md`, `PRIVACY_AND_DATA_HANDLING.md`, `LICENSING_NOTES.md`, `GOVERNANCE_AND_HANDOFF.md` |
| Purpose | Define the minimum product, theory, software, privacy, usability, and release conditions that constitute a successful v0.1 |

v0.1 succeeds when it is useful, auditable, reproducible, evidence-bounded, local-first, and transferable.

Success does not require production deployment, universal thresholds, enterprise integrations, or a universal collapse prediction.

A feature is not successful merely because it runs.

It must produce the right result, in the right evidence class, under the right observability conditions, with explicit limits and passing tests.

---

## 1. Success statement

Recursive Integrity Toolkit v0.1 is successful when a new user can install it, run the canonical hero audit locally, obtain the approved results, inspect every public result back to its source and test, understand what remains unavailable, and share a redacted report without exposing raw content.

---

## 2. Success dimensions

v0.1 is evaluated across ten dimensions.

| Dimension | Core question |
|---|---|
| Product usefulness | Does the toolkit answer practical audit questions? |
| Theory fidelity | Does implementation preserve the theory's actual boundaries? |
| Mathematical correctness | Do formulas and metrics match independent expected values? |
| Data integrity | Are unknowns, provenance, lineage, and representations handled honestly? |
| Reporting integrity | Are evidence classes and unavailable conclusions preserved? |
| Reproducibility | Do identical inputs and seeds reproduce outputs? |
| Privacy and security | Does local execution avoid hidden exposure and executable inputs? |
| Usability | Can a new user complete the hero workflow? |
| Performance | Does v0.1 meet declared local targets? |
| Transferability | Can future maintainers understand and extend the project? |

Failure in a release-blocking dimension prevents `official-v0.1`.

---

## 3. Product-usefulness criteria

### SC-P01. Low-observability value

Minimum condition:

A records-only Level 1 audit produces useful output.

Required outputs where eligible:

- record inventory,
- exact duplicates,
- support size,
- Gini-Simpson diversity,
- tail structure,
- unavailable provenance conclusions.

Proof artifacts:

- Level 1 fixture,
- JSON report,
- Markdown report,
- passing integration test.

### SC-P02. Partial-provenance value

Minimum condition:

A partial Level 2 manifest produces:

- row coverage,
- field coverage,
- source shares,
- direct closure interval,
- recommended next metadata.

The report must preserve unknown values.

### SC-P03. Lineage value

Minimum condition:

A Level 3 audit identifies:

- parent-resolution coverage,
- external roots,
- top shared ancestors,
- ancestry concentration,
- unresolved lineage.

### SC-P04. Longitudinal value

Minimum condition:

A Level 4 audit identifies:

- support delta,
- extinct observed states,
- diversity delta,
- provenance changes,
- lineage changes where available.

### SC-P05. Honest experimental value

When Phase 6B ships:

- simulations are useful,
- assumptions are explicit,
- results remain experimental,
- no empirical causal claim appears.

---

## 4. Theory-fidelity criteria

### SC-T01. Closed-resampling fidelity

The finite-resampling implementation matches the theory equations under the declared assumptions.

### SC-T02. Entropy boundary

Reports do not use entropy as an independent causal agent.

### SC-T03. Concentration versus failure

Low diversity, support contraction, or ancestry concentration does not automatically become proven functional failure.

### SC-T04. Exact versus structural domains

The software does not claim that every cross-domain case follows one identical transition equation.

### SC-T05. No universal compact-formula scoring

The theory relations:

\[
Q=I\times D
\]

and:

\[
S=P\times I
\]

do not become universal numerical scores in v0.1.

### SC-T06. Amplification separation

The amplification-dominant branch remains deferred or visibly separate.

### SC-T07. Theory-version trace

Official v0.1 names the exact theory versions used.

---

## 5. Mathematical-correctness criteria

### SC-M01. Gini-Simpson tests

All hand-calculated cases pass.

### SC-M02. Hero diversity

Required values:

```text
v1 diversity: 0.875
v2 diversity: 0.75
delta: -0.125
```

### SC-M03. Support comparison

Required values:

```text
v1 support: 8
v2 support: 5
delta: -3
retention: 0.625
extinct: battery, lizard, turtle
```

### SC-M04. Tail probability

Closed-form one-step extinction cases pass.

### SC-M05. Expected contraction

One-step and multi-step expected diversity calculations pass.

### SC-M06. Closure bounds

Required invariants pass:

```text
0 <= lower <= upper <= 1
width = unresolved share
```

### SC-M07. Ancestry concentration

Hand-calculated single-root, equal-root, uneven-root, and multi-root cases pass.

### SC-M08. Reopening

When implemented, \(\lambda\) boundary and state-reachability tests pass.

### SC-M09. Independent oracles

No required expected value is generated solely from implementation output.

---

## 6. Data-integrity criteria

### SC-D01. Canonical identity

Composite record identity works across versions.

### SC-D02. Unknown preservation

The following remain distinct:

- missing provenance,
- source type unknown,
- grounding unknown,
- zero,
- unavailable.

### SC-D03. Source and grounding separation

Source type does not overwrite external grounding.

### SC-D04. Parent ambiguity

Ambiguous parent references fail explicitly.

### SC-D05. Missing parent

Missing parent remains unresolved and reduces coverage.

### SC-D06. Cycle handling

Cycles block ancestry interpretation without silent repair.

### SC-D07. Version order

Longitudinal analysis requires explicit order.

### SC-D08. Representation declaration

Every support and diversity result names its representation.

### SC-D09. Safe schema mapping

Only approved declarative operations execute.

### SC-D10. Original-file preservation

Source files are never modified in place.

---

## 7. Reporting-integrity criteria

### SC-R01. Required sections

Every full report contains:

1. Run metadata
2. Input inventory
3. Observability summary
4. Capability matrix
5. Observed facts
6. Derived metrics
7. Proxy signals
8. Simulations
9. Unavailable conclusions
10. Recommended next metadata
11. Warnings
12. Errors

### SC-R02. Evidence-class separation

Counts, metrics, proxies, simulations, and unavailable conclusions appear in the correct sections.

### SC-R03. Closure interval

Closure exposure is reported as lower and upper bounds.

### SC-R04. Simulation labeling

Tail probability and reopening scenarios remain simulations.

### SC-R05. Topological ancestry wording

Ancestry HHI does not become causal contribution.

### SC-R06. Hero unavailable conclusions

The hero report lists:

- model-performance decline unavailable,
- causal ancestor effect unavailable,
- universal integrity unavailable,
- universal collapse prediction unavailable.

### SC-R07. Restricted terminology

No public collapse score, integrity score, or entropy score appears.

### SC-R08. Next metadata

The report identifies the smallest useful metadata improvement.

---

## 8. Reproducibility criteria

### SC-REP01. Stable analytical output

Same inputs, config, version, and seed produce the same analytical JSON after variable run metadata is normalized.

### SC-REP02. Fixed-seed simulation

Fixed-seed scenarios reproduce identical paths.

### SC-REP03. Stable sorting

States, ancestors, warnings, and errors use deterministic ordering.

### SC-REP04. Input hashes

Reports include input hashes.

### SC-REP05. Config hash

Resolved configuration has a stable hash.

### SC-REP06. Environment record

Run metadata records Python and toolkit versions.

---

## 9. Privacy and security criteria

### SC-PS01. Local execution

Hero audit runs without network access.

### SC-PS02. No telemetry

No hidden telemetry exists.

### SC-PS03. Content-safe logs

Normal logs contain no raw content, notes, or full embeddings.

### SC-PS04. Redacted sharing

Redacted JSON and Markdown remove sensitive fields.

### SC-PS05. Metric invariance

Redaction does not change analytical values.

### SC-PS06. Safe content references

Path traversal, symlink escape, and remote URI resolution are blocked.

### SC-PS07. Safe schema mapping

Executable mappings are rejected.

### SC-PS08. Temporary files

Temporary files are run-scoped and cleaned at normal exit.

### SC-PS09. No private fixtures

Repository fixtures contain no private data.

---

## 10. Usability criteria

### SC-U01. One-command hero

A new user can run the hero example in one documented command.

### SC-U02. Installation clarity

README instructions support a first successful local run without author intervention.

### SC-U03. Error clarity

Invalid inputs produce:

- exact error code,
- affected field,
- clear cause,
- remediation.

### SC-U04. Report readability

A non-author technical reader can identify:

- what was supplied,
- what was observed,
- what was derived,
- what was simulated,
- what remains unavailable.

### SC-U05. Output discoverability

CLI prints generated report paths.

### SC-U06. No mandatory infrastructure

A user does not need:

- cloud account,
- database,
- server,
- API key,
- remote model.

### SC-U07. Partial-run usefulness

A family-specific failure does not erase valid unrelated results when a partial report is safe.

---

## 11. Performance criteria

### SC-PERF01. Hero runtime

Required target:

```text
under 5 seconds on a common laptop CPU
```

### SC-PERF02. Standard metadata audit

The toolkit should process approximately 100,000 rows for exact metadata analysis on a workstation.

### SC-PERF03. Sparse lineage

Sparse lineage graphs fitting workstation memory should complete without uncontrolled growth.

### SC-PERF04. No silent quadratic work

Impractical pairwise analysis is blocked or warned before execution.

### SC-PERF05. Performance evidence

Release includes benchmark environment and results.

---

## 12. Transferability criteria

### SC-H01. Repository architecture

Repository structure matches the approved skeleton.

### SC-H02. Module purpose

Every module has:

- purpose,
- owner IDs,
- assumptions,
- limitations.

### SC-H03. Traceability

Every public field has an owner and test.

### SC-H04. Governance

Theory-relevant changes require the approved review path.

### SC-H05. Handoff documentation

A future maintainer can identify:

- canonical repository,
- official release,
- theory version,
- test suite,
- open decisions,
- deferred scope.

### SC-H06. No author-only hidden knowledge

Required behavior must be present in files, tests, and fixtures.

---

## 13. Hero success criteria

The canonical hero run succeeds when all of these values match.

### 13.1 Inputs

```text
v1 records: 8
v2 records: 8
representation: topic
maximum observability level: 4
```

### 13.2 Capabilities

```text
ingestion: available
content_diagnostics: available
provenance: available
lineage: available
dataset_longitudinal: available
model_longitudinal: unavailable
intervention_simulation: unavailable
```

### 13.3 Support and diversity

```text
v1 support: 8
v2 support: 5
support delta: -3
support retention: 0.625
v1 diversity: 0.875
v2 diversity: 0.75
diversity delta: -0.125
```

### 13.4 Extinct observed states

```text
battery
lizard
turtle
```

### 13.5 Provenance

```text
v2 provenance row coverage: 1.0
v2 required-field coverage: 1.0
v2 grounding-field coverage: 1.0
human share: 0.5
synthetic share: 0.5
unknown share: 0.0
missing provenance share: 0.0
```

### 13.6 Closure

Pending final approval:

```text
direct closure interval: 0.5 to 0.5
lineage closure interval: 0.0 to 0.0
```

### 13.7 Lineage

Pending final HHI approval:

```text
cycle detected: false
distinct external roots: 5
top root: v1::v1_01
top-root incidence: 3
top-root incidence share: 0.375
ancestry HHI: 0.25
effective external roots: 4.0
```

### 13.8 Reports

Required:

- JSON created,
- Markdown created,
- section order correct,
- unavailable conclusions visible,
- no forbidden score.

### 13.9 Privacy and performance

Required:

```text
network calls: 0
raw content in normal logs: none
runtime: under 5 seconds
exit code: 0
```

---

## 14. Quantitative release requirements

| Requirement | Target |
|---|---:|
| Required unit-test pass rate | 100% |
| Required integration-test pass rate | 100% |
| Required golden match rate | 100% |
| Public-field trace coverage | 100% |
| Active-owner test coverage | 100% |
| Proxy limitation coverage | 100% |
| Simulation assumption coverage | 100% |
| Hero network calls | 0 |
| Forbidden public fields | 0 |
| Unresolved release-blocking decisions | 0 |

No required test may remain `xfail`.

---

## 15. Phase success criteria

### Phase 0

Success requires:

- specification baseline,
- theory map,
- decision register,
- traceability,
- validation plan,
- no code,
- no unresolved Phase 1 blocker.

### Phase 1

Success requires:

- correct repository tree,
- placeholder modules,
- dependency justification,
- test skeleton,
- no analysis algorithm.

### Phase 2

Success requires:

- loaders,
- mapping,
- validation,
- observability,
- capability matrix,
- hero inputs load,
- unknown remains unknown.

### Phase 3

Success requires:

- exact metrics,
- hand-calculated tests,
- fixed-seed simulation behavior,
- correct evidence classes.

### Phase 4

Success requires:

- JSON,
- Markdown,
- CLI,
- redacted mode,
- golden hero report,
- language restrictions.

### Phase 5

Success requires:

- graph,
- cycles,
- external roots,
- multi-root allocation,
- ancestry concentration,
- lineage coverage.

### Phase 6A

Success requires:

- ordered longitudinal comparison,
- compatible representation,
- support and diversity deltas,
- observed extinction.

### Phase 6B

Success requires:

- experimental scenario labeling,
- assumptions,
- seeds,
- no causal overclaim.

---

## 16. Non-goals

The following are not v0.1 success criteria:

- universal model-collapse prediction,
- universal integrity score,
- universal entropy score,
- epoch countdown,
- production cloud service,
- web dashboard,
- automatic policy enforcement,
- mandatory database,
- enterprise-scale connector breadth,
- multimodal completeness,
- causal attribution from ancestry,
- social or biological diagnosis,
- universal threshold calibration,
- amplification-dominant analysis,
- empirical intervention ingestion,
- full OpenLineage or ML Metadata adapter support.

A release should not be delayed because it lacks a non-goal.

A release must be delayed if it falsely claims a non-goal.

---

## 17. Failure conditions

v0.1 fails release when:

- hero values do not match,
- formula tests fail,
- unknown provenance is inferred,
- support lacks a representation,
- a probability appears as an observation,
- a proxy appears as proof,
- a cycle is silently repaired,
- a parent is chosen through ambiguity,
- a closure interval becomes a point,
- a forbidden score appears,
- raw content leaks,
- hidden network activity occurs,
- required reports are missing,
- traceability coverage is incomplete,
- licensing files are incoherent,
- a blocking decision remains open.

---

## 18. Release labels

Recommended labels:

```text
experimental
reviewed
official-v0.1
```

### 18.1 Experimental

A feature may be experimental when:

- behavior is bounded,
- tests exist,
- assumptions are visible,
- public output says experimental.

### 18.2 Reviewed

Requires:

- tests,
- documentation,
- traceability,
- relevant reviewer approval.

### 18.3 Official v0.1

Requires:

- all release gates,
- Theory Owner approval,
- Technical Maintainer approval,
- validation summary,
- coherent licensing,
- no blocking issue.

---

## 19. Proof artifacts

Official v0.1 should preserve:

- release tag,
- source archive,
- wheel,
- source distribution,
- validation summary,
- benchmark summary,
- traceability coverage report,
- specification consistency report,
- golden outputs,
- license files,
- theory-source manifest,
- known limitations,
- release notes.

---

## 20. Success review table

| Goal | Minimum condition | Proof artifact | Owner |
|---|---|---|---|
| New-user usability | hero runs in one command | README and smoke test | Technical Maintainer |
| Auditability | every public field traces | traceability report | Theory Owner |
| Mathematical fidelity | exact tests pass | unit-test summary | Mathematical Reviewer |
| Honest limits | unavailable conclusions visible | golden report | Theory Owner |
| Low-observability value | Level 1 and 2 useful | fixture reports | Domain Validator |
| Lineage value | shared ancestry visible | lineage golden | Mathematical Reviewer |
| Reproducibility | same input, same output | determinism tests | Technical Maintainer |
| Privacy | no leakage | privacy tests | Security Reviewer |
| Local-first | no network | no-network test | Security Reviewer |
| Transferability | handoff docs complete | governance review | Theory Owner |

---

## 21. Decision dependencies

| Decision | Success effect |
|---|---|
| `UD-003` | hero Level 4 |
| `UD-004` | capability matrix |
| `UD-010` | closure bounds |
| `UD-014` | ancestry HHI |
| `UD-017` | Phase 6 split |
| `UD-019` | Markdown required |
| `UD-023` | licensing baseline |
| `UD-024` | theory-source publication policy |
| `UD-025` | runtime and dependencies |
| `UD-032` | release labels |
| `UD-033` | hero corrections |
| `UD-035` | collapse restriction |
| `UD-036` | optional HTML |

---

## 22. Approval

### Theory Owner decision

- [ ] Approve success baseline
- [ ] Approve with exceptions
- [ ] Return for revision

Exceptions:

```text

```

Theory Owner:

```text
Xiangyu Guo
```

Approval date:

```text

```

Approved status:

```text
PENDING
```

### Technical Maintainer acknowledgment

- [ ] Required conditions are implementable.
- [ ] Quantitative targets are testable.
- [ ] Hero success can be automated.
- [ ] Release proof artifacts are feasible.

Technical notes:

```text

```

Maintainer:

```text

```

Date:

```text

```

### Mathematical Reviewer acknowledgment

- [ ] Mathematical values are correct.
- [ ] Required exact tests are sufficient.
- [ ] No theory formula becomes an unsupported score.

Reviewer notes:

```text

```

Reviewer:

```text

```

Date:

```text

```

### Security Reviewer acknowledgment

- [ ] Privacy targets are testable.
- [ ] No-network behavior is testable.
- [ ] Unsafe inputs block release.

Security notes:

```text

```

Reviewer:

```text

```

Date:

```text

```

### Domain Validator acknowledgment

- [ ] Low-observability output is useful.
- [ ] Hero report is understandable.
- [ ] Recommended metadata is actionable.
- [ ] Unavailable conclusions prevent overreading.

Domain notes:

```text

```

Validator:

```text

```

Date:

```text

```

---

## 23. Change-control rule

After approval:

1. a new success criterion requires a proof artifact,
2. a quantitative target requires a benchmark or test,
3. a public non-goal cannot become a hidden requirement,
4. a release blocker cannot be waived silently,
5. a hero-value change requires golden and theory review,
6. a privacy target cannot weaken without security review,
7. a traceability target cannot weaken,
8. an experimental feature cannot be labeled official without passing its gate,
9. success must remain evidence-bounded rather than feature-count driven.
