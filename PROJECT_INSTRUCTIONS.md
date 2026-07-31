# PROJECT_INSTRUCTIONS

## Document control

| Field | Value |
|---|---|
| Project | Recursive Integrity Toolkit |
| Target release | v0.1 |
| Status | APPROVED OPERATING BASELINE |
| Primary owner | Theory Owner |
| Intended environment | ChatGPT Project with phase-gated Work execution |
| Governing audit files | `SPEC_AUDIT.md`, `THEORY_SOURCE_MAP.md`, `UNRESOLVED_DECISIONS.md` |

## Phase 0 approval record

| Field | Value |
|---|---|
| Approved by | Xiangyu Guo, Theory Owner |
| Approval date | 2026-07-29 |
| Decision basis | All recommended options in `UNRESOLVED_DECISIONS.md` approved without exceptions |
| Baseline effect | This file is frozen as part of the approved Phase 0 baseline |
| Change policy | Later changes require the recorded change-control process |

These instructions govern all work performed for the Recursive Integrity Toolkit.

The Project is the authoritative specification and source bundle. Work must execute only the approved phase, obey the files in the Project, preserve theory-to-code traceability, and stop whenever a blocking decision remains unresolved.

---

## 1. Project purpose

Build an auditable, local-first research toolkit for analyzing recursive closure risk in synthetic-data and recursive-data pipelines.

The toolkit should help users examine:

- recursive data reuse,
- support contraction,
- diversity contraction,
- tail vulnerability,
- provenance incompleteness,
- direct and lineage-aware closure exposure,
- ancestry concentration,
- version-to-version support loss,
- observability limits.

The toolkit must report only what the supplied evidence and declared assumptions support.

---

## 2. Primary product domain

v0.1 is designed for machine-learning data pipelines.

Primary users include:

- ML researchers using model-generated training data,
- research engineers operating iterative or recursive training loops,
- data-governance teams maintaining provenance metadata,
- auditors examining dataset lineage and source concentration.

Biological, cognitive, social, institutional, and civilizational cases remain theory sources and validation witnesses. v0.1 reports must not convert an ML data audit into a diagnosis of another domain.

---

## 3. Operating model

### 3.1 Project role

The ChatGPT Project stores:

- authoritative theory PDFs,
- approved specifications,
- decision records,
- validation rules,
- hero fixtures,
- accepted outputs,
- repository instructions.

Treat these files as persistent project sources. Do not rely on free-form chat memory when a controlling file exists.

### 3.2 Work role

Use Work for:

- specification auditing,
- bounded document production,
- repository planning,
- staged implementation tasks,
- test and report generation,
- finished phase deliverables.

Work must not improvise scope or continue into the next phase without explicit approval.

### 3.3 Repository role

The public repository contains the implementation, reusable specifications, tests, examples, release artifacts, and public documentation.

Repository code must remain traceable to the Project source bundle.

---

## 4. Authority model

### 4.1 Approved decision authority

Use only decisions marked `APPROVED` in `UNRESOLVED_DECISIONS.md`.

Entries marked `OPEN`, `RECOMMENDED`, or `DEFERRED` do not authorize implementation.

When a phase depends on an unresolved blocking decision, stop and report the decision ID.

### 4.2 Theory authority

The uploaded theory sources control:

- conceptual meaning,
- mathematical interpretation,
- causal boundaries,
- the distinction between exact results and structural extensions,
- prohibited overclaims,
- the meaning of closure, difference, external correction, integrity decay, and entropy.

Primary theory sources:

1. `The Universal Inbreeding Law v2.pdf`
2. `Entropy as a Structural Boundary Condition, Not a Causal Force v2.pdf`
3. `Supplementary Case Registry for the Universal Inbreeding Law, Version 2.0.pdf`

### 4.3 Product authority

Approved product specifications control:

- v0.1 scope,
- exact field names,
- accepted file formats,
- public output schemas,
- implementation order,
- performance targets,
- privacy defaults,
- release gates.

A theory claim does not automatically become a v0.1 feature.

### 4.4 Exact contract order

After Phase 0 approval, use the following order for exact implementation behavior:

1. `SPEC_AUDIT.md`
2. approved decisions in `UNRESOLVED_DECISIONS.md`
3. `THEORY_SOURCE_MAP.md`
4. `V0.1_PRODUCT_SPEC.md`
5. `DEFINITIONS_AND_UNITS.md`
6. `DATA_AND_PROVENANCE_SPEC.md`
7. `OBSERVABILITY_AND_REPORTING.md`
8. `THEORY_TO_CODE_TRACEABILITY.md`
9. `VALIDATION_PLAN.md`
10. `PRIVACY_AND_DATA_HANDLING.md`
11. `SUCCESS_CRITERIA.md`
12. `GOVERNANCE_AND_HANDOFF.md`

The theory PDFs remain authoritative for conceptual meaning even when exact product behavior is defined by a specification.

---

## 5. Conflict protocol

Never silently resolve conflicts.

When two controlling sources disagree:

1. identify the exact files and passages,
2. describe the practical consequence,
3. identify any related `UD-*` decision,
4. propose a resolution,
5. classify the conflict as blocking or nonblocking,
6. stop if it blocks the approved phase.

Use this format:

```text
CONFLICT ID:
SOURCES:
CONFLICT:
IMPLEMENTATION CONSEQUENCE:
RELATED DECISION:
RECOMMENDED RESOLUTION:
BLOCKING STATUS:
```

Do not implement both interpretations.

Do not choose the easier interpretation merely because it simplifies code.

---

## 6. Phase stop rules

Complete only the approved phase.

### Phase 0: specification audit

Allowed:

- identify contradictions,
- freeze definitions,
- map theory sources,
- list unresolved decisions,
- define acceptance gates,
- prepare controlling Markdown specifications.

Forbidden:

- implementation modules,
- analysis algorithms,
- production CLI,
- repository feature expansion.

Required outputs include:

- `SPEC_AUDIT.md`
- `THEORY_SOURCE_MAP.md`
- `UNRESOLVED_DECISIONS.md`
- approved specification baseline
- repository architecture
- dependency strategy

### Phase 1: repository scaffold

Allowed:

- directory tree,
- package metadata,
- placeholder modules,
- README shell,
- test directories,
- example directories,
- CI skeleton,
- license files.

Forbidden:

- analysis algorithms,
- provisional metrics,
- hidden defaults,
- generated scores.

Acceptance condition:

- tree matches the approved architecture,
- dependencies are justified,
- no analysis behavior is implemented.

### Phase 2: ingestion, validation, and observability

Allowed:

- loaders,
- schema mapping,
- input normalization,
- validation,
- observability classifier,
- capability matrix.

Forbidden:

- unapproved analytical metrics,
- inference of missing provenance,
- semantic classification through an embedded LLM.

Acceptance condition:

- hero inputs load without manual edits,
- unknown provenance remains unknown,
- validation messages are exact and human-readable,
- capability status follows approved rules.

### Phase 3: deterministic metrics and simulations

Allowed:

- diversity,
- support,
- tail ranking,
- approved extinction scenarios,
- provenance exposure bounds,
- resampling,
- approved ancestry metrics,
- golden mathematical tests.

Acceptance condition:

- hand-checkable cases pass,
- fixed-seed simulations are deterministic,
- every public field has theory and test traceability.

### Phase 4: reports and CLI

Allowed:

- JSON report,
- required Markdown report,
- optional HTML report,
- CLI entrypoint,
- redacted output mode.

Acceptance condition:

- hero command runs end to end,
- report sections follow the approved order,
- evidence classes remain distinct,
- unavailable conclusions are explicit.

### Phase 5: lineage graph

Allowed:

- parent graph,
- cycle detection,
- ancestry tracing,
- external roots,
- ancestry concentration,
- lineage coverage.

Acceptance condition:

- cycles fail cleanly,
- unresolved parents reduce coverage,
- hero and advanced lineage fixtures match golden values.

### Phase 6A: longitudinal comparison

Allowed:

- ordered version comparison,
- support deltas,
- topic or label extinction,
- provenance changes,
- lineage changes where available.

Acceptance condition:

- comparison requires compatible representations and explicit ordering.

### Phase 6B: experimental scenarios

Allowed only when explicitly approved:

- closed finite-resampling scenarios,
- external reopening scenarios,
- fixed-seed comparisons,
- assumption tables.

All Phase 6B outputs must be labeled `experimental` and `simulation`.

Empirical causal-intervention ingestion remains deferred until a separate specification is approved.

---

## 7. Hard product constraints

v0.1 must:

- run locally by default,
- produce reproducible outputs,
- preserve unknown values,
- expose assumptions,
- separate evidence classes,
- remain inspectable by human reviewers,
- keep modules small and single-purpose,
- provide exact validation messages,
- support a complete hero example,
- trace every public result to definitions, code, tests, and reports.

v0.1 must not include:

- a universal collapse score,
- a universal integrity score,
- a universal entropy score,
- automatic human-versus-model text inference as fact,
- automatic policy enforcement,
- a production web application,
- a cloud service,
- a mandatory database server,
- hidden telemetry,
- an embedded LLM,
- auto-executed remote plugins,
- universal failure thresholds,
- epoch countdowns,
- social or civilizational diagnosis,
- multimodal parity across text, image, and audio.

---

## 8. Theory boundaries

### 8.1 Exact mathematical core

The exact v0.1 stochastic core comes from the finite closed-resampling model in `The Universal Inbreeding Law v2`.

For a categorical state distribution \(p_t\):

\[
X_t \mid p_t \sim \operatorname{Multinomial}(n,p_t)
\]

\[
p_{t+1}=\frac{X_t}{n}
\]

Gini-Simpson diversity:

\[
D_t=1-\sum_i p_{t,i}^2
\]

Expected one-generation contraction:

\[
\mathbb{E}[D_{t+1}\mid p_t]
=
\left(1-\frac{1}{n}\right)D_t
\]

One-step extinction probability for state \(i\):

\[
\Pr(p_{t+1,i}=0\mid p_{t,i})
=
(1-p_{t,i})^n
\]

External reopening scenario:

\[
p_{t+1}
=
R_n\left((1-\lambda)p_t+\lambda r_t\right)
\]

Implement these equations only under their declared assumptions.

### 8.2 Structural formulas

The following remain theory-level structural dependencies:

\[
Q=I\times D
\]

\[
S=P\times I
\]

Do not operationalize them as public numerical scores in v0.1.

### 8.3 Concentration and failure

Distributional concentration does not automatically establish functional failure.

A report may identify:

- lower diversity,
- support loss,
- tail extinction,
- source concentration,
- ancestry concentration,
- reduced external grounding.

A report must not claim proven functional failure without approved domain outcome evidence.

### 8.4 Entropy language

Entropy functions as a structural boundary, distributional quantity, or descriptive signature under declared conditions.

Reports must identify the local mechanism, such as:

- finite resampling,
- missing external input,
- source concentration,
- support contraction,
- incomplete provenance,
- shared ancestry.

Do not use entropy as an independent causal agent.

### 8.5 Cross-domain restraint

Exact stochastic commonality applies only where the same mathematical structure has been established.

Broader cases may share a topology of:

- closure,
- loss of difference,
- inherited distortion,
- weakened external fidelity.

Do not claim that all domains obey the same transition equation.

---

## 9. Evidence classes

Every public result must have exactly one primary evidence class.

### 9.1 Observed fact

Directly present in or exactly counted from supplied data.

Examples:

- row count,
- matching provenance-row count,
- declared source type,
- exact duplicate count,
- cycle detected in the supplied graph.

### 9.2 Derived metric

A deterministic function of observed inputs.

Examples:

- support size,
- Gini-Simpson diversity,
- source-type share,
- closure exposure bounds,
- ancestry HHI,
- version support delta.

### 9.3 Proxy signal

A heuristic interpretation with declared limits.

Examples:

- tail fragility warning,
- correlated-error exposure based on shared ancestry,
- support-contraction alert.

### 9.4 Simulation

A scenario result under explicit assumptions.

Examples:

- one-step extinction probability under closed multinomial resampling,
- fixed-horizon diversity path,
- external reopening comparison.

### 9.5 Unavailable conclusion

A conclusion blocked by missing evidence or outside v0.1 scope.

Examples:

- universal collapse prediction,
- proven production failure,
- causal effect of a shared ancestor,
- universal integrity,
- universal entropy score.

Do not move an output between evidence classes to make the report appear stronger.

---

## 10. Data and provenance rules

### 10.1 Unknown values

Unknown means unknown.

Do not silently map unknown to:

- human,
- synthetic,
- external,
- grounded,
- reviewed,
- safe,
- independent.

### 10.2 Source type

Approved source types:

- `human`
- `synthetic`
- `mixed`
- `sensor`
- `unknown`

`mixed` remains its own category unless explicit component weights are supplied.

### 10.3 External grounding

`external_grounding` controls direct grounding claims.

Allowed values:

- `yes`
- `no`
- `unknown`

Do not infer grounding from:

- `source_type`,
- `human_reviewed`,
- generator identity,
- content quality,
- writing style,
- filename,
- organizational ownership.

### 10.4 Provenance confidence

Allowed values:

- `confirmed`
- `log_derived`
- `estimated`
- `unknown`

Reports must distinguish confirmed and estimated provenance.

### 10.5 Parent references

Use the approved canonical parent reference format from `DATA_AND_PROVENANCE_SPEC.md`.

Do not:

- guess delimiters,
- resolve ambiguous bare IDs,
- create missing roots,
- infer parents from content similarity.

### 10.6 Missing parents

A missing parent does not become an external root.

Missing ancestry must:

- reduce lineage coverage,
- widen uncertainty,
- appear in warnings,
- block conclusions that require complete ancestry.

### 10.7 Generation

Use the approved definition from `DEFINITIONS_AND_UNITS.md`.

Do not use `generation` to mean:

- training epoch,
- model release,
- arbitrary dataset version,
- graph depth unless the approved definition explicitly says so.

When declared generation conflicts with graph evidence, emit the approved warning or error.

### 10.8 Version order

Never infer chronology from filenames or lexical order alone.

Longitudinal analysis requires:

- explicit version order,
- valid timestamps,
- or user-declared comparison order.

Record the selected ordering rule.

---

## 11. Representation rules

Support, diversity, tail, and extinction require a declared representation.

Every related result must record:

- `representation_name`
- `representation_source`
- `representation_version`
- `binning_or_mapping_rule`

Use the approved selection policy from `DEFINITIONS_AND_UNITS.md`.

General restrictions:

- exact content hashes describe record-form support,
- exact content hashes do not establish semantic support,
- topic and label comparisons require compatible definitions across versions,
- user-provided embedding bins require version and method metadata,
- no embedded LLM may infer topics in v0.1,
- silent representation fallback is forbidden.

---

## 12. Observability model

Report a maximum observability level and a capability matrix.

Capability statuses:

- `available`
- `partial`
- `unavailable`
- `experimental`

Initial capabilities:

- ingestion,
- content diagnostics,
- provenance,
- lineage,
- dataset longitudinal comparison,
- model longitudinal comparison,
- intervention simulation.

A high maximum level does not imply that every capability or metric is available.

### Level 0

Inputs:

- readable file,
- minimal schema.

Allowed:

- ingest status,
- row count,
- schema inventory,
- validation gaps.

### Level 1

Inputs:

- analyzable records, labels, topics, bins, or embeddings.

Allowed:

- exact duplicates,
- support,
- diversity,
- tail ranking,
- representation-bound diagnostics.

### Level 2

Inputs:

- partial or complete provenance.

Allowed:

- provenance coverage,
- source shares,
- grounding coverage,
- direct closure exposure bounds.

### Level 3

Inputs:

- resolvable parent-child lineage.

Allowed:

- cycle checks,
- ancestry tracing,
- external-root analysis,
- ancestry concentration,
- lineage exposure bounds.

Partial lineage must disclose coverage.

### Level 4

Inputs:

- at least two ordered, representation-compatible dataset versions.

Allowed:

- version deltas,
- support loss,
- tail extinction,
- provenance changes,
- lineage changes where available.

Model-performance conclusions require separate model evidence.

### Level 5

v0.1 status:

- optional,
- experimental,
- scenario-based.

No empirical causal conclusion is authorized by Level 5 simulation alone.

---

## 13. Metric implementation rules

Every public metric must have:

1. a frozen definition,
2. units or type,
3. a representation requirement where applicable,
4. one primary module owner,
5. one or more Theory Map IDs or an identified product-only basis,
6. deterministic tests,
7. report field,
8. evidence class,
9. documented limitations.

Do not add a public metric directly from an implementation idea.

Do not expose internal intermediate values as public results without traceability review.

Do not combine multiple metrics into an opaque score.

---

## 14. Tail analysis rules

Tail membership must use an approved declared threshold.

Reports must include:

- tail rule,
- threshold,
- representation,
- frequency counts,
- analyzed sample size.

The one-step formula

\[
(1-p_i)^n
\]

must appear as a simulation result under the closed multinomial assumption.

Required classification:

- observed frequency: observed fact,
- rarity rank: derived metric,
- one-step extinction probability: simulation,
- narrative warning: proxy signal.

Do not present the scenario probability as a calibrated forecast of a production pipeline unless a later approved validation establishes that equivalence.

---

## 15. Lineage and ancestry rules

Lineage outputs must include:

- analyzed node count,
- analyzed edge count,
- resolved-parent coverage,
- unresolved parent count,
- grounding coverage,
- cycle status,
- root allocation method.

Cycle detection is a graph-validity rule for generational ancestry.

Ancestry concentration may describe:

- incidence,
- root share,
- HHI,
- effective root count.

It must not claim:

- causal contribution,
- semantic error,
- biological relatedness,
- production failure.

When multiple roots support one record, use only the approved allocation convention.

---

## 16. Schema mapping and input safety

Schema mapping must remain declarative.

Permitted operations may include only those approved in `DATA_AND_PROVENANCE_SPEC.md`, such as:

- rename,
- declared type cast,
- declared datetime parse,
- JSON-list parse,
- constant assignment,
- named-field coalesce,
- whitespace normalization.

Forbidden:

- `eval`,
- arbitrary Python,
- shell execution,
- network access,
- remote code,
- hidden content inference,
- user-supplied executable plugins.

Record every mapping transformation in run metadata.

---

## 17. Privacy and security

Default privacy posture:

- local execution,
- no hidden network calls,
- no telemetry,
- no content upload,
- no automatic issue submission.

Normal logs may contain:

- file paths,
- row counts,
- schema coverage,
- metric names,
- timing,
- warning codes,
- error codes.

Normal logs must not contain:

- raw record content,
- full embeddings,
- private notes,
- expanded parent-child content,
- secrets,
- credentials.

Debug mode may expose additional details only when explicitly enabled.

Human-readable reports must support redaction:

- hide raw content,
- show counts and IDs only,
- optionally hash record IDs,
- avoid leaking private notes.

---

## 18. Implementation style

Prefer:

- plain Python,
- type hints,
- small functions,
- small modules,
- explicit data structures,
- deterministic code paths,
- stable field names,
- readable error messages,
- direct formulas,
- documented assumptions,
- standard-library solutions where reasonable.

Avoid:

- framework-heavy architecture,
- deep inheritance,
- plugin systems,
- metaprogramming,
- hidden global state,
- dynamic imports,
- implicit network access,
- premature performance abstraction,
- undocumented caching,
- silent data mutation.

Every source file should include:

- file purpose,
- owning Trace IDs or Theory Map IDs,
- public behavior,
- assumptions,
- known limits.

---

## 19. Dependency rules

Dependencies must be justified during Phase 1.

For every proposed dependency, record:

- package name,
- exact purpose,
- importing modules,
- optional or required status,
- privacy or network behavior,
- maintenance risk,
- reason a simpler alternative was rejected.

Do not add a dependency merely for convenience.

Parquet support may be optional if it requires a dedicated extra.

No dependency may silently download models or remote assets during analysis.

---

## 20. Testing rules

### 20.1 Mathematical tests

Expected values must come from:

- hand calculation,
- closed-form derivation,
- separately reviewed notebook,
- independently prepared golden fixture.

Do not create expected values by running the implementation and copying its output.

### 20.2 Unit tests

Test:

- valid inputs,
- invalid inputs,
- boundary values,
- unknown states,
- deterministic seeds,
- empty and singleton cases,
- incompatible representations,
- incomplete provenance,
- ambiguous lineage.

### 20.3 Integration tests

Test:

- end-to-end hero execution,
- report generation,
- redacted mode,
- CLI errors,
- schema mapping,
- multi-version comparison,
- no-network behavior.

### 20.4 Golden tests

Golden outputs must cover:

- observability level,
- capability matrix,
- provenance row coverage,
- support values,
- diversity,
- extinct states,
- source shares,
- closure bounds,
- ancestry results,
- unavailable conclusions,
- warnings and errors.

### 20.5 Negative tests

Verify that v0.1 does not output:

- universal collapse score,
- universal integrity score,
- universal entropy score,
- inferred human provenance,
- inferred external grounding,
- causal ancestry claims,
- unapproved semantic diversity.

---

## 21. Report requirements

Required outputs:

- machine-readable JSON,
- human-readable Markdown.

Optional:

- HTML,
- normalized manifest,
- error report,
- run metadata export.

Required report sections, in order:

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

Every report must answer:

- what inputs were used,
- how versions were ordered,
- which representation was used,
- what was directly observed,
- what was calculated,
- what was treated as a proxy,
- what was simulated,
- what could not be concluded,
- what metadata would unlock additional analysis.

---

## 22. Report language rules

Use exact defined terms.

Preferred result language includes:

- support contraction,
- diversity change,
- tail extinction,
- closure exposure bounds,
- provenance incompleteness,
- external-root coverage,
- ancestry concentration,
- unavailable functional-failure conclusion.

The word `collapse` may appear only in:

- theory references,
- project motivation,
- names of cited research phenomena,
- statements describing unavailable universal conclusions.

Do not use `collapse` as:

- a metric,
- a score,
- a direct alert from support contraction,
- a universal prediction,
- a threshold label.

Do not convert:

- a range into a point estimate,
- unknown into open or closed,
- correlation into causation,
- a scenario into an observation,
- a topological metric into semantic failure.

---

## 23. Traceability rules

Every public output must trace through:

```text
theory or product basis
    -> definition
    -> mathematical object or deterministic rule
    -> module
    -> test
    -> report field
    -> documented limitation
```

Use:

- `TM-*` IDs from `THEORY_SOURCE_MAP.md`,
- `T*` IDs from `THEORY_TO_CODE_TRACEABILITY.md`,
- product-only rule IDs where no theory claim exists.

No report field may exist without a trace record.

No theory-relevant module may implement behavior absent from the traceability files.

Deferred claims must not power public results.

---

## 24. Hero example requirements

The hero example must remain:

- tiny,
- exact,
- local,
- auditable,
- deterministic,
- executable in one command.

The approved hero baseline must identify:

- representation: `topic`,
- v1 topic support,
- v2 topic support,
- extinct topics,
- v2 provenance row coverage,
- source-type shares,
- distinct external roots,
- top shared ancestor by incidence,
- maximum observability level,
- capability matrix,
- unavailable model-performance conclusion,
- unavailable universal-collapse conclusion.

Do not silently change hero data or golden values.

Any change requires:

- decision record,
- updated expected outputs,
- updated tests,
- updated documentation.

---

## 25. File creation rules

When producing or modifying a project file:

1. read all controlling files relevant to that file,
2. preserve exact canonical field names,
3. preserve status and approval blocks,
4. remove drafting notes before release,
5. avoid duplicated definitions,
6. avoid copying PDF line-wrap artifacts,
7. validate formulas against rendered source equations,
8. record unresolved conflicts,
9. do not create implementation behavior inside prose-only files,
10. stop after the requested file or phase is complete.

Do not overwrite an approved file without showing the change and its reason.

---

## 26. Work response format

At the end of each Work task, return:

### Completed

List only the deliverables produced.

### Validation

State:

- files checked,
- tests run,
- acceptance conditions passed or failed.

### Decisions used

List approved `UD-*` decisions used by the task.

### Conflicts

List any unresolved conflicts or write `None`.

### Deferred items

List any intentionally excluded work.

### Stop status

Use one:

- `PHASE COMPLETE`
- `TASK COMPLETE, PHASE CONTINUES`
- `BLOCKED BY DECISION`
- `FAILED ACCEPTANCE GATE`

Do not announce work from a later phase.

---

## 27. Failure and stop conditions

Stop immediately when:

- a required decision is not approved,
- two authoritative sources conflict,
- a public metric lacks a definition,
- a result lacks an evidence class,
- a formula cannot be verified,
- a representation is missing or incompatible,
- parent references are ambiguous,
- implementation would require arbitrary code execution,
- a request would expand v0.1 beyond approved scope,
- a phase acceptance gate fails.

When stopping, provide:

- the exact blocker,
- the relevant file,
- the decision or trace ID,
- the minimum resolution required.

Do not work around the blocker through hidden assumptions.

---

## 28. Review posture

Treat this repository as a theory-led reference implementation that future specialists must be able to inspect, challenge, and extend.

Prioritize:

- conceptual fidelity,
- transparent uncertainty,
- explicit limitations,
- reproducibility,
- local execution,
- small modules,
- testable behavior,
- transferable governance.

Reject or postpone features that increase:

- ambiguity,
- hidden defaults,
- code opacity,
- attack surface,
- dependency burden,
- unsupported confidence,
- scope drift.

---

## 29. Current phase instruction

Phase 0 was approved by the Theory Owner on 2026-07-29 with no exceptions.

Phase 1 repository scaffolding is authorized.

During Phase 1:

- create the approved repository tree,
- create package metadata,
- create import-safe empty modules and ownership docstrings,
- create schema placeholders,
- create test and fixture directories,
- add hero files,
- add license and governance files,
- add CI skeletons,
- verify the dependency baseline.

Phase 1 must not implement:

- support or diversity calculations,
- closure bounds,
- tail probabilities,
- lineage ancestry metrics,
- simulations,
- report metric assembly,
- hidden provenance inference,
- any universal score.

Phase 2 may begin only after the Phase 1 acceptance gate passes.
