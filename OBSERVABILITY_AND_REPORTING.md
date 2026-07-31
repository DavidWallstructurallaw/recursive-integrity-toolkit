# OBSERVABILITY_AND_REPORTING

## Document control

| Field | Value |
|---|---|
| Project | Recursive Integrity Toolkit |
| Target release | v0.1 |
| Phase | Phase 0 |
| Status | APPROVED PHASE 0 BASELINE |
| Primary owner | Theory Owner |
| Technical reviewers | Technical Maintainer, Mathematical Reviewer |
| Depends on | `SPEC_AUDIT.md`, `THEORY_SOURCE_MAP.md`, `UNRESOLVED_DECISIONS.md`, `PROJECT_INSTRUCTIONS.md`, `V0.1_PRODUCT_SPEC.md`, `DEFINITIONS_AND_UNITS.md`, `DATA_AND_PROVENANCE_SPEC.md` |
| Purpose | Freeze observability levels, capability status, evidence classes, public report structure, JSON schema, Markdown behavior, language rules, redaction, and unavailable-conclusion handling |

This file defines what Recursive Integrity Toolkit v0.1 may report from each class of evidence and how every public result must be labeled.

The toolkit must distinguish:

- what the inputs directly contain,
- what can be calculated deterministically,
- what is only a proxy,
- what is produced under simulation assumptions,
- what remains unavailable.

A higher observability level does not imply that every capability is available.

Unknown evidence must remain unknown.

A simulation must not be presented as an observation.

A topological signal must not be presented as causal proof.

Definitions marked `APPROVED DECISION` become implementation-authoritative only after the corresponding `UD-*` entry is approved.

---

## 1. Scope of this specification

This specification controls:

- observability levels,
- capability statuses,
- maximum-level assignment,
- evidence classes,
- public report sections,
- top-level JSON keys,
- required field metadata,
- report ordering,
- Markdown rendering,
- optional HTML rendering,
- redacted mode,
- warning and error presentation,
- unavailable conclusions,
- recommended next metadata,
- report-language restrictions,
- hero-report expectations,
- reporting acceptance tests.

This specification does not control:

- canonical input schemas,
- detailed field parsing,
- mathematical formula ownership,
- source-code layout,
- licensing,
- governance.

Those belong in the corresponding controlling files.

---

## 2. Reporting principles

### 2.1 Evidence before interpretation

Every public result must identify its evidence class.

No result may rely on report prose alone to communicate its status.

### 2.2 Capability before ambition

The report should show what the available inputs permit.

It should not imitate a stronger audit by filling missing evidence with assumptions.

### 2.3 Explicit uncertainty

Incomplete provenance, lineage, representation, or version order must widen uncertainty or block the affected conclusion.

### 2.4 Representation-bound results

Support, diversity, tail, and extinction results must name the representation used.

### 2.5 Mechanism-bound language

Reports should identify the observed or modeled mechanism, such as:

- finite resampling,
- missing provenance,
- unknown grounding,
- support contraction,
- ancestry concentration,
- unresolved lineage.

Entropy must not replace the local mechanism.

### 2.6 Traceable outputs

Every public field must map to:

```text
definition
-> theory or product basis
-> rule or formula
-> implementation module
-> test
-> report field
-> limitation
```

### 2.7 No silent strengthening

The renderer must not strengthen an internal result.

Examples:

- interval stays interval,
- unknown stays unknown,
- partial capability stays partial,
- scenario stays simulation,
- proxy stays proxy,
- unavailable conclusion stays unavailable.

---

## 3. Evidence classes

Every public result field must have exactly one primary evidence class.

Allowed values:

```text
observed_fact
derived_metric
proxy_signal
simulation
unavailable_conclusion
```

### 3.1 Observed fact

Definition:

> Information directly present in supplied inputs or exactly counted from validated inputs without interpretive modeling.

Examples:

- row count,
- file count,
- matching provenance-row count,
- declared source type,
- exact duplicate count,
- detected lineage cycle,
- unresolved-parent count.

Observed facts may still depend on:

- selected dataset scope,
- parser behavior,
- normalization profile,
- redaction.

Those conditions must be documented.

### 3.2 Derived metric

Definition:

> A deterministic calculation from observed inputs under a declared rule.

Examples:

- support size,
- Gini-Simpson diversity,
- source-type shares,
- provenance coverage,
- closure exposure bounds,
- support delta,
- ancestry HHI,
- effective external-root count.

A derived metric must provide:

- formula or deterministic rule,
- denominator,
- representation where applicable,
- units,
- missingness behavior,
- trace ID.

### 3.3 Proxy signal

Definition:

> A heuristic or structural warning that indicates possible risk without directly observing the full functional condition.

Examples:

- tail fragility warning,
- correlated-error exposure warning,
- support-contraction alert,
- ancestry-concentration alert.

A proxy signal must include:

- basis fields,
- trigger rule,
- limitation,
- confidence or coverage context where available.

A proxy signal must not be presented as causal proof.

### 3.4 Simulation

Definition:

> A result generated under explicit mathematical or stochastic assumptions rather than directly observed from the production system.

Examples:

- one-step extinction probability,
- finite-resampling trajectory,
- external-reopening scenario,
- expected diversity contraction under declared \(n\).

A simulation must include:

- model name,
- assumptions,
- parameters,
- random seed where applicable,
- horizon,
- replicate count where applicable,
- model limitations.

### 3.5 Unavailable conclusion

Definition:

> A relevant conclusion that cannot be supported because evidence is missing, assumptions are unmet, or the conclusion lies outside v0.1 scope.

Examples:

- universal collapse prediction,
- proven model-performance decline,
- causal effect of a shared ancestor,
- universal integrity score,
- universal entropy score,
- social or biological diagnosis.

An unavailable conclusion must include:

- conclusion name,
- reason,
- blocking evidence,
- metadata or study design needed to unlock it,
- related capability.

---

## 4. Observability levels

### 4.1 General rule

The toolkit reports one:

```text
maximum_observability_level
```

and one capability matrix.

The maximum level indicates the strongest validated evidence class available anywhere in the run.

The capability matrix shows which analysis families are:

- available,
- partial,
- unavailable,
- experimental.

### 4.2 Level 0: ingest observability

Minimum evidence:

- readable input,
- minimal canonical schema,
- at least one valid record.

Allowed outputs:

- file inventory,
- row counts,
- schema coverage,
- input hashes,
- validation status,
- auditability gaps,
- observability limitations.

Required capability state:

```text
ingestion: available
```

Other capabilities may remain unavailable.

### 4.3 Level 1: content or representation observability

Minimum evidence:

- analyzable content,
- or a valid declared representation such as topic, label, bin, cluster, or exact record form.

Allowed outputs:

- exact duplicates,
- support size,
- Gini-Simpson diversity,
- state counts,
- rarity ranking,
- tail membership,
- approved finite-resampling scenario inputs.

Restrictions:

- exact content hashes describe record-form support,
- semantic claims require a semantic representation,
- missing representation values reduce coverage,
- one-step extinction probabilities remain simulations.

### 4.4 Level 2: provenance observability

Minimum evidence:

- at least one valid matching provenance row.

Allowed outputs:

- provenance row coverage,
- provenance required-field coverage,
- grounding-field coverage,
- source-type shares,
- confidence shares,
- missing-provenance share,
- direct closure exposure bounds.

Restrictions:

- partial provenance can still support Level 2,
- closure exposure must remain an interval when grounding is unresolved,
- source type must not substitute for grounding,
- human review must not substitute for grounding.

### 4.5 Level 3: lineage observability

Minimum evidence:

- at least one resolvable parent-child path,
- no unresolved ambiguity in the analyzed valid subgraph,
- cycle-free ancestry for the analyzed path.

Allowed outputs:

- resolved-parent edge coverage,
- resolved-lineage coverage,
- external-root tracing,
- distinct external-root count,
- top shared ancestors,
- ancestor incidence,
- ancestry HHI,
- effective external-root count,
- lineage closure exposure bounds.

Restrictions:

- partial lineage produces partial capability,
- unresolved parents widen uncertainty,
- cycles block affected lineage analysis,
- ancestry concentration remains topological,
- shared ancestry does not prove shared error.

### 4.6 Level 4: longitudinal dataset observability

Minimum evidence:

- at least two ordered dataset versions,
- compatible representation for the requested comparison.

Allowed outputs:

- record-count delta,
- support delta,
- diversity delta,
- added states,
- extinct observed states,
- source-share changes,
- provenance-coverage changes,
- lineage changes where available.

Restrictions:

- model-performance claims require separate model evidence,
- representation mismatch blocks direct state comparison,
- version order must be explicit,
- observed extinction means absence from the later observed version under the declared representation.

### 4.7 Level 5: intervention or scenario observability

v0.1 status:

```text
experimental
```

Minimum evidence for v0.1 scenario use:

- explicit scenario configuration,
- valid model parameters,
- declared initial and external distributions where needed,
- fixed or recorded random seed.

Allowed outputs:

- closed finite-resampling comparison,
- expected diversity trajectory,
- sampled diversity trajectory,
- one-step extinction probability,
- external-reopening scenario,
- state re-entry events,
- assumption table.

Restrictions:

- Level 5 simulation does not establish empirical causality,
- empirical controlled intervention remains deferred,
- results must appear in the `simulations` section,
- every field must carry `experimental=true`.

### 4.8 Maximum-level assignment

Recommended algorithm:

```text
if approved Level 5 scenario is configured and valid:
    maximum level = 5
else if at least two ordered compatible dataset versions are present:
    maximum level = 4
else if at least one valid lineage path is present:
    maximum level = 3
else if at least one valid provenance row is present:
    maximum level = 2
else if analyzable content or representation is present:
    maximum level = 1
else:
    maximum level = 0
```

A level assignment must not erase lower-level limitations.

### 4.9 Hero maximum level

For the canonical hero run with:

- v1 records,
- v2 records,
- provenance,
- valid lineage,
- explicit version order,
- topic representation,

the maximum level is:

```text
4
```

Status:

```text
APPROVED DECISION UD-003
```

---

## 5. Capability matrix

### 5.1 Required capability keys

v0.1 reports these capability keys:

```text
ingestion
content_diagnostics
provenance
lineage
dataset_longitudinal
model_longitudinal
intervention_simulation
```

### 5.2 Capability status values

```text
available
partial
unavailable
experimental
```

### 5.3 Capability object

Each capability object must contain:

```json
{
  "status": "available",
  "reason_codes": [],
  "coverage": 1.0,
  "requirements_met": [],
  "requirements_missing": [],
  "notes": []
}
```

Fields may be null where not applicable.

### 5.4 Ingestion capability

Available when:

- at least one valid record remains after validation.

Partial when:

- some files or rows fail but a valid audit scope remains.

Unavailable when:

- no valid record remains.

### 5.5 Content diagnostics capability

Available when:

- exact content or a valid state representation covers the requested scope.

Partial when:

- some records lack representation values,
- some local content references fail,
- only record-form support is available while semantic analysis was requested.

Unavailable when:

- no analyzable content or representation exists.

### 5.6 Provenance capability

Available when:

- every analyzed record has a valid matched provenance row and required fields.

Partial when:

- at least one valid row exists,
- coverage is incomplete,
- grounding is unknown for some records.

Unavailable when:

- no valid matching provenance row exists.

### 5.7 Lineage capability

Available when:

- all requested lineage records have resolvable valid ancestry,
- graph is acyclic,
- grounding classification is sufficient.

Partial when:

- some valid lineage exists,
- unresolved parents or unknown roots reduce coverage,
- valid results can still be calculated for a disclosed subset.

Unavailable when:

- no valid parent path exists,
- ambiguity blocks resolution,
- cycle prevents the requested analysis.

### 5.8 Dataset longitudinal capability

Available when:

- two or more versions are explicitly ordered,
- requested representations are compatible.

Partial when:

- some metrics compare,
- representation or field mismatch blocks other metrics.

Unavailable when:

- only one version exists,
- version order is missing,
- representation incompatibility blocks comparison.

### 5.9 Model longitudinal capability

Available only when:

- approved model-performance or behavior evidence is supplied across versions.

Partial when:

- only some outcomes or versions have valid measurements.

Unavailable when:

- only dataset versions are supplied.

### 5.10 Intervention simulation capability

Status:

```text
experimental
```

when a valid approved scenario is configured.

Unavailable when:

- no scenario is requested,
- parameters are invalid,
- required distributions are missing.

### 5.11 Capability coverage

When meaningful:

\[
\text{capability coverage}
=
\frac{\text{records or edges included}}
{\text{records or edges in requested scope}}
\]

The denominator must be named.

Coverage does not replace status.

---

## 6. Required report outputs

### 6.1 Machine-readable report

Required format:

```text
JSON
```

### 6.2 Human-readable report

Required format:

```text
Markdown
```

Status:

```text
APPROVED DECISION UD-019
```

### 6.3 Optional report

Optional format:

```text
HTML
```

Status:

```text
APPROVED DECISION UD-036
```

### 6.4 Additional optional outputs

- normalized provenance manifest,
- validation-only report,
- run metadata file,
- redacted sharing bundle,
- simulation trace file,
- error-only JSON.

---

## 7. Required report section order

Every full JSON and Markdown report must preserve this conceptual order:

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

The JSON object preserves these top-level keys in this order where the serializer supports ordered mappings.

HTML should follow the same order.

---

## 8. Required top-level JSON schema

### 8.1 Required keys

```json
{
  "run": {},
  "inputs": {},
  "observability": {},
  "capabilities": {},
  "observed_facts": {},
  "derived_metrics": {},
  "proxy_signals": {},
  "simulations": {},
  "unavailable_conclusions": [],
  "recommended_next_metadata": [],
  "warnings": [],
  "errors": []
}
```

Every key must be present.

Empty sections use:

- `{}` for objects,
- `[]` for arrays.

Do not omit a required top-level section because it is empty.

### 8.2 Schema version

The report must include:

```json
{
  "run": {
    "report_schema_version": "1.0"
  }
}
```

### 8.3 JSON validity

JSON must not contain:

- comments,
- trailing commas,
- NaN,
- Infinity,
- negative Infinity,
- executable content.

### 8.4 Stable field names

Public field names must remain stable within report schema version 1.x.

A denominator or meaning change requires:

- new field name,
- or major schema version.

---

## 9. Common result envelope

Every public metric or signal should use a structured envelope.

### 9.1 Derived metric envelope

Recommended form:

```json
{
  "value": 0.5,
  "unit": "ratio",
  "evidence_class": "derived_metric",
  "status": "available",
  "method_id": "F-007",
  "theory_map_ids": ["TM-P02"],
  "trace_ids": ["T3"],
  "scope": {
    "dataset_versions": ["v2"],
    "record_count": 8
  },
  "representation": null,
  "coverage": 1.0,
  "assumptions": [],
  "limitations": []
}
```

### 9.2 Observed fact envelope

Recommended form:

```json
{
  "value": 8,
  "unit": "records",
  "evidence_class": "observed_fact",
  "status": "available",
  "scope": {
    "dataset_versions": ["v2"]
  },
  "coverage": 1.0,
  "limitations": []
}
```

### 9.3 Proxy signal envelope

Recommended form:

```json
{
  "signal": "ancestry_concentration",
  "level": "present",
  "evidence_class": "proxy_signal",
  "status": "available",
  "basis_fields": [
    "ancestry_concentration_hhi",
    "top_shared_ancestors"
  ],
  "coverage": 1.0,
  "limitations": [
    "Shared ancestry does not prove shared semantic error."
  ]
}
```

### 9.4 Simulation envelope

Recommended form:

```json
{
  "model": "closed_multinomial_resampling",
  "evidence_class": "simulation",
  "status": "experimental",
  "parameters": {
    "resample_size": 100,
    "simulation_horizon": 1,
    "random_seed": 42
  },
  "assumptions": [
    "finite categorical states",
    "multinomial sampling",
    "no external reopening"
  ],
  "results": {},
  "limitations": []
}
```

### 9.5 Unavailable-conclusion envelope

Recommended form:

```json
{
  "conclusion": "model_performance_decline",
  "evidence_class": "unavailable_conclusion",
  "status": "unavailable",
  "reason_codes": [
    "MODEL_OUTCOME_DATA_MISSING"
  ],
  "blocking_evidence": [
    "No model-performance measurements were supplied."
  ],
  "required_next_metadata": [
    "Versioned model evaluation results"
  ]
}
```

---

## 10. Run metadata section

### 10.1 Required fields

```text
run_id
toolkit_version
report_schema_version
started_at
completed_at
duration_seconds
python_version
platform
command
config_hash
random_seed
strict_mode
redacted_mode
network_call_count
```

Fields may be null where not applicable.

### 10.2 Input hashes

The run section or input section must report:

- file hash algorithm,
- file hashes,
- normalized configuration hash.

### 10.3 Determinism

The report must state:

```text
deterministic: true
```

when:

- no stochastic operation ran,
- or every stochastic operation had a recorded seed and deterministic implementation.

### 10.4 Network behavior

The hero report must show:

```text
network_call_count: 0
```

### 10.5 Privacy mode

Allowed values:

```text
standard
redacted
debug
```

Debug mode must be explicit.

---

## 11. Input inventory section

### 11.1 Required fields

For each input artifact:

```text
role
path or redacted path
format
file_hash
size_bytes
row_count
dataset_versions
schema_fields
parse_status
validation_status
```

### 11.2 Path redaction

In redacted mode:

- absolute paths should be replaced by filename or stable token,
- local base directories should be omitted,
- content references should be hidden.

### 11.3 Input scope

The report must state:

- records included,
- records excluded,
- reasons for exclusion,
- versions included,
- version order source,
- selected representation.

### 11.4 Mapping inventory

When schema mapping is used, report:

- mapping file hash,
- operations applied,
- fields affected,
- unmapped-field count,
- unsafe-operation count, expected to be zero in successful runs.

---

## 12. Observability summary section

### 12.1 Required fields

```json
{
  "maximum_level": 4,
  "level_label": "longitudinal_dataset_observability",
  "basis": [],
  "limitations": [],
  "partial_evidence": []
}
```

### 12.2 Basis

The basis list should identify the evidence that unlocked the level.

Hero example:

```text
two ordered dataset versions
compatible topic representation
valid lineage provenance
```

### 12.3 Limitations

The limitations list should identify missing evidence that prevents stronger conclusions.

Hero example:

```text
no model-performance measurements
no controlled intervention data
```

### 12.4 Level wording

Preferred labels:

| Level | Label |
|---|---|
| 0 | `ingest_observability` |
| 1 | `content_or_representation_observability` |
| 2 | `provenance_observability` |
| 3 | `lineage_observability` |
| 4 | `longitudinal_dataset_observability` |
| 5 | `experimental_intervention_or_scenario_observability` |

---

## 13. Capability matrix section

### 13.1 Required Markdown table

The Markdown report should render:

| Capability | Status | Coverage | Reason |
|---|---|---:|---|
| Ingestion | Available | 100% | Valid records loaded |
| Content diagnostics | Available | 100% | Topic representation present |
| Provenance | Available | 100% | Matching provenance rows |
| Lineage | Available | 100% | Parent graph resolves |
| Dataset longitudinal | Available | 100% | v1 and v2 ordered |
| Model longitudinal | Unavailable | n/a | No model outcomes |
| Intervention simulation | Unavailable | n/a | No scenario requested |

### 13.2 Partial capability rendering

When partial:

- display `Partial`,
- show exact coverage,
- show unresolved counts,
- link to warnings.

### 13.3 Experimental capability rendering

When experimental:

- display `Experimental`,
- identify scenario model,
- identify assumptions,
- separate it from observed and derived sections.

---

## 14. Observed facts section

### 14.1 Required categories

Depending on inputs, include:

- input counts,
- record counts,
- exact duplicate counts,
- provenance row counts,
- explicit source-type counts,
- explicit confidence counts,
- missing-parent counts,
- resolved-parent edge counts,
- cycle status,
- per-version field inventories.

### 14.2 Direct declarations

Declared metadata should be described as:

```text
declared source type
declared grounding state
declared provenance confidence
```

Do not imply external verification unless supplied.

### 14.3 Coverage context

Observed counts should show their scope.

Example:

```text
4 of 8 v2 records declare source_type=synthetic.
```

---

## 15. Derived metrics section

### 15.1 Required Level 1 metrics

When eligible:

- support size,
- Gini-Simpson diversity,
- state frequencies,
- tail support size,
- tail record share,
- rarity ranking.

### 15.2 Required Level 2 metrics

When eligible:

- provenance row coverage,
- provenance required-field coverage,
- grounding-field coverage,
- source-type shares,
- missing-provenance share,
- direct closure exposure lower bound,
- direct closure exposure upper bound,
- interval width.

### 15.3 Required Level 3 metrics

When eligible:

- resolved-parent edge coverage,
- resolved-lineage coverage,
- external ancestry coverage,
- distinct external-root count,
- ancestor incidence,
- ancestry HHI,
- effective external-root count,
- lineage closure exposure bounds.

### 15.4 Required Level 4 metrics

When eligible:

- record-count delta,
- support delta,
- support retention ratio,
- support loss count,
- added-state count,
- extinct states,
- diversity delta,
- source-share delta,
- provenance-coverage delta,
- lineage-concentration delta where available.

### 15.5 Method disclosure

Every metric must show:

- metric name,
- formula ID or method ID,
- unit,
- scope,
- denominator,
- representation where applicable,
- coverage,
- limitation.

### 15.6 Interval rendering

Closure exposure must appear as an interval.

Example:

```text
Direct closure exposure: 37.5% to 62.5%
```

Do not choose the midpoint unless a separate method explicitly authorizes it.

---

## 16. Proxy signals section

### 16.1 General rule

Proxy signals are secondary summaries of observed facts and derived metrics.

They must not appear before their basis fields.

### 16.2 Tail fragility signal

Basis may include:

- low state counts,
- tail membership,
- one-step extinction simulation.

Required limitation:

```text
This signal is not a calibrated forecast of the production pipeline.
```

### 16.3 Support-contraction signal

Basis:

- negative support delta,
- extinct observed states,
- compatible representation.

Preferred wording:

```text
The observed later version contains fewer represented states under the selected representation.
```

Restricted wording:

```text
The system has collapsed.
```

### 16.4 Ancestry-concentration signal

Basis:

- high incidence around one or more roots,
- ancestry HHI,
- effective external-root count.

Required limitation:

```text
This signal describes lineage concentration and does not establish shared semantic error or causal contribution.
```

### 16.5 Correlated-error exposure signal

This proxy may be emitted only when:

- shared ancestry is present,
- the report uses `exposure` language,
- no direct error claim is made.

Preferred name:

```text
shared_ancestry_dependence_signal
```

Avoid naming the public field:

```text
correlated_error
```

unless direct error evidence exists.

### 16.6 Signal severity

Recommended values:

```text
present
not_present
indeterminate
```

v0.1 should avoid generic high, medium, low risk labels unless thresholds are explicitly defined and validated.

---

## 17. Simulations section

### 17.1 Placement

All scenario probabilities and stochastic outputs must appear under:

```text
simulations
```

### 17.2 Required metadata

Every simulation must report:

- model,
- model version,
- parameters,
- initial distribution,
- representation,
- sample size,
- horizon,
- seed,
- replicate count,
- assumptions,
- limitations.

### 17.3 One-step extinction simulation

Required fields:

```text
state_id
observed_frequency
resample_size
one_step_extinction_probability
```

Required wording:

```text
Under the declared closed multinomial resampling scenario...
```

### 17.4 Expected diversity contraction

The expected value may appear as a derived scenario quantity inside the simulation section.

It should not be mixed with empirically observed version change.

### 17.5 External reopening simulation

Required fields:

```text
reopening_weight
external_input_distribution
internal_distribution
resample_size
horizon
seed
state_reentry_events
```

Required status:

```text
experimental
```

### 17.6 Simulation comparison

A scenario table may compare:

- closed,
- partially reopened,
- fully external source mixture.

Every row must preserve identical state representation and comparable parameters.

### 17.7 Monte Carlo uncertainty

When multiple replicates are used, the report may include:

- mean,
- median,
- quantiles,
- extinction frequency.

The report must distinguish:

- closed-form probability,
- Monte Carlo estimate,
- single simulated path.

### 17.8 No hidden default scenarios

A simulation must not run unless:

- explicitly requested,
- or clearly enabled in the hero example specification.

No scenario parameter may be silently chosen beyond approved documented defaults.

---

## 18. Unavailable conclusions section

### 18.1 Required use

The report must list relevant conclusions that a reasonable reader might otherwise infer incorrectly.

### 18.2 Required hero unavailable conclusions

The hero report must include:

- model-performance decline unavailable,
- causal effect of `v1::v1_01` unavailable,
- universal integrity loss unavailable,
- universal collapse prediction unavailable.

### 18.3 Standard unavailable conclusions

Potential entries:

```text
model_performance_decline
causal_ancestor_effect
universal_integrity
universal_quality
universal_stability
universal_entropy_score
universal_collapse_prediction
production_failure
semantic_error_correlation
empirical_intervention_effect
```

### 18.4 Required fields

Each entry must include:

- conclusion key,
- human-readable statement,
- reason codes,
- blocking evidence,
- required next metadata,
- related capability,
- theory or product limit.

### 18.5 Unavailable does not mean false

The report should state:

> Unavailable means the supplied evidence does not support the conclusion. It does not establish that the conclusion is false.

### 18.6 No empty confidence language

Avoid vague phrases such as:

```text
probably unavailable
may be unavailable
seems unclear
```

Use exact blocking reasons.

---

## 19. Recommended next metadata section

### 19.1 Purpose

This section identifies the smallest additional evidence that would unlock the next useful capability.

### 19.2 Recommendation structure

```json
{
  "priority": 1,
  "metadata": "external_grounding",
  "scope": "records missing grounding classification",
  "expected_unlock": [
    "narrower direct closure exposure bounds"
  ],
  "reason": "Grounding is unresolved for 25% of records."
}
```

### 19.3 Recommendation priority

Recommended priority order:

1. evidence that narrows uncertainty,
2. evidence that unlocks the next observability level,
3. evidence that resolves an error,
4. optional enrichment.

### 19.4 Common recommendations

- add missing provenance rows,
- supply `external_grounding`,
- provide composite parent references,
- resolve ambiguous parents,
- declare version order,
- preserve topic or label mapping across versions,
- provide model-performance outcomes,
- provide controlled intervention design,
- provide external reference distribution.

### 19.5 No prescriptive governance

Recommendations should focus on metadata and auditability.

v0.1 must not automatically enforce policy.

---

## 20. Warnings section

### 20.1 Required fields

Each warning includes:

```text
code
message
count
affected_scope
representative_locations
effect_on_capabilities
remediation
```

### 20.2 Warning order

Recommended order:

1. warnings affecting validity,
2. warnings affecting observability,
3. warnings affecting coverage,
4. compatibility warnings,
5. optional-field warnings.

### 20.3 Aggregation

Repeated warnings may be grouped by code.

The full machine-readable list may preserve every location.

### 20.4 Raw-content exclusion

Warnings must not include raw content.

### 20.5 Coverage warnings

Warnings affecting coverage must identify:

- numerator,
- denominator,
- affected capability.

---

## 21. Errors section

### 21.1 Required fields

Each error includes:

```text
code
severity
message
file_role
field
record_key
row_number
effect_on_run
effect_on_capabilities
remediation
```

### 21.2 Family-specific errors

An error may block one analysis family while preserving others.

Example:

- lineage cycle blocks lineage analysis,
- content and provenance reports may still render.

### 21.3 Fatal errors

Fatal errors prevent a valid full report.

When possible, the toolkit should still emit an error-only JSON document.

### 21.4 Error prose

Error messages should explain:

- what failed,
- where it failed,
- what the toolkit did,
- how the user can correct it.

Avoid stack traces in normal mode.

---

## 22. Markdown report specification

### 22.1 Required heading

Recommended:

```markdown
# Recursive Integrity Audit Report
```

### 22.2 Summary block

The report should begin with:

- run ID,
- maximum observability level,
- key capability statuses,
- record scope,
- representation,
- warning count,
- error count.

### 22.3 Tables

Use tables for:

- capability matrix,
- input inventory,
- source shares,
- coverage,
- version comparison,
- top shared ancestors,
- unavailable conclusions.

### 22.4 Lists

Use lists for:

- assumptions,
- limitations,
- warnings,
- recommended metadata.

### 22.5 Numeric display

Recommended display:

- counts as integers,
- ratios as percentages with two decimal places,
- metrics as four decimal places,
- probabilities as four decimal places plus percentage when useful.

Machine-readable JSON remains authoritative.

### 22.6 Null and unavailable display

Use:

```text
Unavailable
```

Do not display unavailable as:

```text
0
0.0
NaN
-
```

A dash may be used only in a table cell when the legend explicitly defines it as not applicable. `Unavailable` is preferred.

### 22.7 Partial coverage display

Example:

```text
Lineage capability: Partial, 75.00% resolved-lineage coverage
```

### 22.8 Report footer

Required footer content:

- toolkit version,
- report schema version,
- evidence-class legend,
- note that unavailable conclusions are not false conclusions,
- traceability reference.

---

## 23. Optional HTML report specification

### 23.1 Generation source

HTML should be generated from the structured result object, not by reparsing Markdown where that could lose field metadata.

### 23.2 Offline requirement

Default HTML must be self-contained.

It must not require:

- remote JavaScript,
- remote CSS,
- external fonts,
- telemetry,
- analytics.

### 23.3 Security

HTML must escape:

- record IDs,
- labels,
- file names,
- notes,
- user-provided metadata.

### 23.4 Redaction

HTML redacted mode must follow the same rules as JSON and Markdown.

### 23.5 Interactive features

Interactive filtering is optional and must work locally.

No web server is required.

---

## 24. Redacted mode

### 24.1 Purpose

Redacted mode supports sharing audit structure without exposing sensitive source material.

### 24.2 Required redactions

Redacted mode must hide or transform:

- raw content,
- notes,
- provenance notes,
- full file paths,
- local content references,
- source URIs,
- grounding-evidence paths,
- full embeddings.

### 24.3 Record IDs

Allowed modes:

```text
preserve
hash
omit
```

Recommended default for redacted mode:

```text
hash
```

### 24.4 Stable hash scope

The report must declare whether hashed IDs are stable:

- within one run,
- across a sharing bundle,
- across all runs with a user-provided salt.

### 24.5 Small-cell disclosure

A future privacy mode may suppress small counts.

v0.1 does not require statistical disclosure control.

### 24.6 Redaction must not alter metrics

Redaction occurs after calculation.

The public report must not recompute metrics from redacted identifiers.

---

## 25. Report-language rules

### 25.1 Preferred language

Use:

- `the supplied records show`,
- `the declared provenance indicates`,
- `the selected representation contains`,
- `the observed later version omits`,
- `the available lineage resolves`,
- `the scenario assumes`,
- `the conclusion remains unavailable`.

### 25.2 Restricted language

Avoid direct statements such as:

- `the dataset is collapsing`,
- `the model has lost integrity`,
- `entropy caused the failure`,
- `the top ancestor caused the error`,
- `human data makes the system safe`,
- `synthetic data proves closure`,
- `the system will fail after N generations`.

### 25.3 Collapse terminology

`collapse` may appear in:

- cited theory,
- product motivation,
- names of cited phenomena,
- unavailable conclusions.

It must not be:

- a metric name,
- a score,
- a direct alert,
- a threshold label,
- a conclusion from support contraction alone.

Status:

```text
APPROVED DECISION UD-035
```

### 25.4 Entropy terminology

A report may use entropy only when:

- a specific entropy metric is computed and named,
- or the theory boundary is explained in documentation.

A report must not state that entropy acts as a causal agent.

### 25.5 Grounding language

Preferred:

```text
declared externally grounded
```

Avoid:

```text
verified real
true human source
safe source
```

unless external verification evidence exists.

### 25.6 Extinction language

Preferred:

```text
The state is absent from the observed later version under the topic representation.
```

Avoid:

```text
The topic is permanently extinct.
```

### 25.7 Ancestry language

Preferred:

```text
This root appears in the reachable ancestry of three records.
```

Avoid:

```text
This root contributed 37.5% of the content.
```

unless weighted contribution evidence exists.

### 25.8 Capability language

Preferred:

```text
Lineage analysis is partial because 2 of 10 parent references are unresolved.
```

Avoid:

```text
The data is mostly good.
```

---

## 26. Method and assumption disclosure

### 26.1 Every metric

Must disclose:

- method ID,
- version,
- unit,
- denominator,
- representation,
- coverage,
- limitations.

### 26.2 Every simulation

Must disclose:

- model,
- assumptions,
- parameters,
- seed,
- horizon,
- replicate count,
- whether closed-form or Monte Carlo.

### 26.3 Every proxy

Must disclose:

- basis fields,
- trigger rule,
- uncertainty,
- interpretation limit.

### 26.4 Every unavailable conclusion

Must disclose:

- exact missing evidence,
- scope boundary,
- next metadata.

---

## 27. Report field naming

### 27.1 General naming

Use lowercase snake_case.

### 27.2 No ambiguous generic fields

Avoid:

```text
score
risk
health
quality
integrity
entropy
collapse
```

without a fully qualified approved definition.

### 27.3 Recommended names

```text
gini_simpson_diversity
direct_closure_exposure_lower_bound
direct_closure_exposure_upper_bound
ancestry_concentration_hhi
effective_external_root_count
support_retention_ratio
one_step_extinction_probability
```

### 27.4 Weighted outputs

Use distinct names:

```text
weighted_gini_simpson_diversity
weighted_state_frequency
```

### 27.5 Versioned fields

Version-specific values should be nested by dataset version rather than encoded into unstable field names.

Preferred:

```json
{
  "by_version": {
    "v1": {},
    "v2": {}
  }
}
```

---

## 28. Hero report requirements

### 28.1 Maximum observability

```text
4
```

### 28.2 Capability matrix

```text
ingestion: available
content_diagnostics: available
provenance: available
lineage: available
dataset_longitudinal: available
model_longitudinal: unavailable
intervention_simulation: unavailable
```

### 28.3 Required observed facts

- 8 v1 records,
- 8 v2 records,
- 8 valid v2 provenance rows,
- 4 v2 records declared human,
- 4 v2 records declared synthetic,
- 0 v2 records declared unknown source type,
- no lineage cycle.

### 28.4 Required derived metrics

- v1 topic support: 8,
- v2 topic support: 5,
- support delta: -3,
- support retention ratio: 5/8,
- extinct states: `lizard`, `turtle`, `battery`,
- v2 provenance row coverage: 1.0,
- v2 human share: 0.5,
- v2 synthetic share: 0.5,
- v2 unknown share: 0.0,
- distinct external-root count supporting v2: 5,
- top shared external root: `v1::v1_01`,
- top shared-root incidence: 3,
- top shared-root incidence share: 0.375.

### 28.5 Required proxy signals

- topic support contraction signal,
- ancestry concentration signal around `v1::v1_01`.

### 28.6 Required simulations

Default hero run:

```text
none
```

A separate hero simulation command may exist, but it must remain optional and experimental.

### 28.7 Required unavailable conclusions

- model-performance decline,
- causal ancestor effect,
- universal integrity loss,
- universal collapse prediction.

### 28.8 Required recommendations

At minimum:

- preserve or reintroduce independent externally grounded examples for extinct topic states,
- provide model-performance results if model decline is being evaluated,
- preserve explicit lineage and grounding metadata in future versions.

The first recommendation must be framed as an audit recommendation tied to the selected topic representation.

### 28.9 Required wording

Preferred summary:

> Under the topic representation, support decreases from eight observed states in v1 to five in v2. The later version omits lizard, turtle, and battery. The supplied provenance fully covers v2 and shows concentrated ancestry around `v1::v1_01`. The available evidence does not establish model-performance decline or universal collapse.

---

## 29. Example top-level JSON report

```json
{
  "run": {
    "run_id": "hero-001",
    "toolkit_version": "0.1.0.dev1",
    "report_schema_version": "1.0",
    "started_at": "2026-01-01T00:00:00Z",
    "completed_at": "2026-01-01T00:00:01Z",
    "duration_seconds": 1.0,
    "python_version": "3.11",
    "platform": "local",
    "strict_mode": false,
    "redacted_mode": false,
    "network_call_count": 0,
    "deterministic": true
  },
  "inputs": {
    "dataset_versions": ["v1", "v2"],
    "version_order": ["v1", "v2"],
    "representation": {
      "name": "topic",
      "source": "topic_field",
      "version": "hero-topic-v1"
    }
  },
  "observability": {
    "maximum_level": 4,
    "level_label": "longitudinal_dataset_observability",
    "basis": [
      "two ordered dataset versions",
      "compatible topic representation",
      "valid provenance and lineage"
    ],
    "limitations": [
      "no model-performance measurements",
      "no controlled intervention data"
    ]
  },
  "capabilities": {
    "ingestion": {
      "status": "available",
      "coverage": 1.0
    },
    "content_diagnostics": {
      "status": "available",
      "coverage": 1.0
    },
    "provenance": {
      "status": "available",
      "coverage": 1.0
    },
    "lineage": {
      "status": "available",
      "coverage": 1.0
    },
    "dataset_longitudinal": {
      "status": "available",
      "coverage": 1.0
    },
    "model_longitudinal": {
      "status": "unavailable",
      "coverage": null
    },
    "intervention_simulation": {
      "status": "unavailable",
      "coverage": null
    }
  },
  "observed_facts": {
    "record_counts": {
      "v1": 8,
      "v2": 8
    },
    "declared_source_type_counts": {
      "v2": {
        "human": 4,
        "synthetic": 4,
        "mixed": 0,
        "sensor": 0,
        "unknown": 0
      }
    },
    "cycle_status": {
      "detected": false
    }
  },
  "derived_metrics": {
    "support": {
      "by_version": {
        "v1": {
          "support_size": 8
        },
        "v2": {
          "support_size": 5
        }
      },
      "support_delta": -3,
      "support_retention_ratio": 0.625,
      "extinct_states": [
        "lizard",
        "turtle",
        "battery"
      ]
    },
    "provenance": {
      "v2_provenance_row_coverage": 1.0,
      "v2_human_share": 0.5,
      "v2_synthetic_share": 0.5,
      "v2_unknown_share": 0.0
    },
    "lineage": {
      "distinct_external_root_count": 5,
      "top_shared_ancestors": [
        {
          "record_key": "v1::v1_01",
          "ancestor_incidence_count": 3,
          "ancestor_incidence_share": 0.375
        }
      ]
    }
  },
  "proxy_signals": {
    "support_contraction": {
      "status": "present",
      "evidence_class": "proxy_signal",
      "basis_fields": [
        "support_delta",
        "extinct_states"
      ]
    },
    "ancestry_concentration": {
      "status": "present",
      "evidence_class": "proxy_signal",
      "basis_fields": [
        "top_shared_ancestors"
      ],
      "limitations": [
        "Shared ancestry does not prove shared semantic error."
      ]
    }
  },
  "simulations": {},
  "unavailable_conclusions": [
    {
      "conclusion": "model_performance_decline",
      "status": "unavailable",
      "reason_codes": [
        "MODEL_OUTCOME_DATA_MISSING"
      ]
    },
    {
      "conclusion": "universal_collapse_prediction",
      "status": "unavailable",
      "reason_codes": [
        "OUT_OF_SCOPE"
      ]
    }
  ],
  "recommended_next_metadata": [
    {
      "priority": 1,
      "metadata": "versioned_model_evaluation_results",
      "expected_unlock": [
        "model_longitudinal capability"
      ]
    }
  ],
  "warnings": [],
  "errors": []
}
```

The example is illustrative.

Exact final field placement must match the approved report schema and traceability file.

---

## 30. Example Markdown report skeleton

```markdown
# Recursive Integrity Audit Report

## Run metadata

| Field | Value |
|---|---|
| Run ID | hero-001 |
| Toolkit version | 0.1.0.dev1 |
| Maximum observability level | 4 |
| Representation | topic |
| Network calls | 0 |

## Input inventory

| Role | File | Rows | Status |
|---|---|---:|---|
| Records | records_v1.csv | 8 | Valid |
| Records | records_v2.csv | 8 | Valid |
| Provenance | provenance.csv | 16 | Valid |

## Observability summary

The run reaches Level 4 because it contains two ordered dataset versions with a compatible topic representation.

Model longitudinal analysis remains unavailable because no model-performance measurements were supplied.

## Capability matrix

| Capability | Status | Coverage | Reason |
|---|---|---:|---|
| Ingestion | Available | 100% | Valid records loaded |
| Content diagnostics | Available | 100% | Topic representation present |
| Provenance | Available | 100% | Matching provenance rows |
| Lineage | Available | 100% | Parent graph resolves |
| Dataset longitudinal | Available | 100% | v1 and v2 are ordered |
| Model longitudinal | Unavailable | Unavailable | No model outcomes |
| Intervention simulation | Unavailable | Unavailable | No scenario requested |

## Observed facts

- v1 contains 8 records.
- v2 contains 8 records.
- 4 v2 records declare human source type.
- 4 v2 records declare synthetic source type.
- No lineage cycle is present.

## Derived metrics

| Metric | v1 | v2 | Change |
|---|---:|---:|---:|
| Topic support | 8 | 5 | -3 |

Observed extinct topic states:

- lizard
- turtle
- battery

## Proxy signals

Topic support contraction is present under the selected representation.

Ancestry is concentrated around `v1::v1_01`, which appears in the reachable ancestry of 3 v2 records.

## Simulations

No simulation was requested.

## Unavailable conclusions

- Model-performance decline is unavailable because no model evaluation data was supplied.
- A causal effect of `v1::v1_01` is unavailable.
- Universal integrity loss is unavailable.
- Universal collapse prediction is unavailable.

## Recommended next metadata

- Add versioned model-evaluation results to unlock model longitudinal analysis.
- Preserve explicit external-grounding and parent metadata in future versions.

## Warnings

None.

## Errors

None.
```

---

## 31. Reporting of partial and failed runs

### 31.1 Partial report

A partial report may be produced when:

- some capabilities remain valid,
- one analysis family fails,
- the overall input bundle still supports a meaningful audit.

The report must show:

- `run_status: partial`,
- failed capabilities,
- preserved capabilities,
- exact errors.

### 31.2 Validation-only report

When metric calculation is blocked but parsing succeeds, the toolkit may produce a validation-only report.

Required sections remain present.

### 31.3 Error-only report

When the run fails fatally before analysis, the toolkit should emit:

- run metadata,
- input inventory where available,
- observability Level 0 or unavailable,
- empty metric sections,
- errors.

### 31.4 Exit status and report status

CLI exit status and report status must be consistent.

Recommended run statuses:

```text
complete
partial
failed
```

---

## 32. Sorting and determinism

### 32.1 State lists

Default order:

- descending count for frequency tables,
- ascending frequency for rarity tables,
- canonical state ID as tie-break.

### 32.2 Ancestor lists

Default order:

- descending incidence count,
- descending fractional mass,
- canonical record key.

### 32.3 Warning and error lists

Default order:

- severity,
- code,
- file,
- row,
- record key.

### 32.4 Unavailable conclusions

Default order:

1. conclusions commonly over-inferred from the present report,
2. conclusions blocking the next capability,
3. general out-of-scope conclusions.

### 32.5 Stable JSON

The same inputs and configuration should produce stable public JSON except for explicitly variable run metadata such as timestamps and run ID.

Golden tests may normalize those fields.

---

## 33. Reporting thresholds

### 33.1 No universal risk thresholds

v0.1 does not define universal thresholds for:

- high closure,
- dangerous tail fragility,
- excessive ancestry concentration,
- impending collapse.

### 33.2 Presence signals

A signal may be triggered by a direct structural condition.

Example:

```text
support_delta < 0
```

This supports a support-contraction signal.

It does not support a failure prediction.

### 33.3 Threshold metadata

Any configurable threshold must appear in:

- run config,
- report assumptions,
- result envelope.

---

## 34. Traceability requirements

### 34.1 Required IDs

Every theory-relevant public field must contain or map to:

- one or more `TM-*` Theory Map IDs,
- one or more `T*` trace IDs,
- or a clearly identified product-only rule ID.

### 34.2 Product-only rules

Examples:

- cycle validity,
- schema completeness,
- report ordering.

These must not be presented as direct theory theorems.

### 34.3 Deferred claims

A deferred claim may appear only under:

```text
unavailable_conclusions
```

or in documentation.

### 34.4 Report schema registry

A future `docs/report_schema.md` should list:

- field path,
- type,
- unit,
- evidence class,
- minimum observability,
- trace IDs,
- null behavior.

---

## 35. Acceptance tests

### 35.1 Observability classification tests

Required cases:

- Level 0 minimal file,
- Level 1 records only,
- Level 2 partial provenance,
- Level 3 partial lineage,
- Level 4 ordered versions,
- Level 5 explicit scenario,
- hero Level 4.

### 35.2 Capability tests

Required cases:

- high maximum level with unavailable lower-family capability,
- partial provenance,
- partial lineage,
- unavailable model longitudinal,
- experimental simulation.

### 35.3 Evidence-class tests

Verify:

- exact count appears under observed facts,
- diversity appears under derived metrics,
- warning appears under proxy signals,
- extinction probability appears under simulations,
- universal collapse appears only as unavailable.

### 35.4 Interval tests

Verify:

- closure exposure remains lower and upper bounds,
- no midpoint is inserted,
- interval width matches unresolved share.

### 35.5 Representation tests

Verify:

- every support metric names representation,
- incompatible representations block longitudinal state comparison,
- content hash is labeled record-form support.

### 35.6 Lineage tests

Verify:

- unresolved parent reduces coverage,
- cycle blocks lineage analysis,
- top ancestor is incidence-based,
- ancestry HHI limitation is rendered.

### 35.7 Language golden tests

The report must not contain prohibited phrases as direct conclusions.

Test for absence of:

```text
collapse score
entropy caused
proved failure
human data is safe
synthetic data caused collapse
ancestor caused the error
```

### 35.8 Redaction tests

Verify:

- raw content absent,
- notes absent,
- paths hidden,
- record IDs hashed when configured,
- metrics unchanged.

### 35.9 Empty-section tests

Verify every required top-level key exists even when empty.

### 35.10 Determinism tests

Verify stable ordering and normalized timestamps in golden comparisons.

---

## 36. Phase acceptance gates

### 36.1 Phase 2 gate

Before observability implementation is complete:

- maximum-level rules pass,
- capability statuses pass,
- partial coverage is visible,
- no metric is calculated beyond validated prerequisites.

### 36.2 Phase 3 gate

Before metric release:

- evidence classes are correct,
- scenario outputs remain simulations,
- proxy signals cite basis fields,
- unavailable conclusions are generated.

### 36.3 Phase 4 gate

Phase 4 passes when:

- JSON report validates,
- Markdown report renders,
- section order is correct,
- hero report matches golden values,
- collapse language restrictions pass,
- redacted mode passes,
- errors and warnings are human-readable.

### 36.4 Release gate

Public v0.1 release requires:

- report schema version 1.0,
- stable field registry,
- passing observability tests,
- passing evidence-class tests,
- passing language golden tests,
- passing redaction tests,
- no deferred metric in public derived outputs,
- no unresolved blocking reporting decision.

---

## 37. Decision dependencies

| Decision | Reporting behavior affected |
|---|---|
| `UD-003` | hero maximum level |
| `UD-004` | capability matrix |
| `UD-008` | provenance coverage fields |
| `UD-010` | closure exposure intervals |
| `UD-011` | representation reporting |
| `UD-012` | tail threshold display |
| `UD-013` | extinction probability classification |
| `UD-014` | ancestry concentration fields |
| `UD-017` | Level 5 scenario scope |
| `UD-019` | Markdown required |
| `UD-020` | near-duplicate reporting |
| `UD-021` | weighted result naming |
| `UD-033` | hero values |
| `UD-035` | collapse terminology |
| `UD-036` | HTML optional status |

Until approved, affected behavior remains the recommended baseline.

---

## 38. Approval checklist

The Theory Owner and reviewers should confirm:

- [ ] maximum level and capability matrix remain separate,
- [ ] partial capability shows exact coverage,
- [ ] every result has one evidence class,
- [ ] support and diversity name the representation,
- [ ] closure exposure remains an interval,
- [ ] tail probability remains a simulation,
- [ ] ancestry concentration remains topological,
- [ ] unavailable conclusions are explicit,
- [ ] Markdown is the required human-readable format,
- [ ] HTML remains optional,
- [ ] redacted mode removes sensitive content,
- [ ] report language does not overclaim collapse,
- [ ] entropy does not replace mechanism,
- [ ] hero report reaches Level 4,
- [ ] model longitudinal remains unavailable in the hero,
- [ ] all top-level JSON sections are always present.

### Theory Owner decision

- [ ] Approve observability and reporting baseline
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

### Mathematical Reviewer acknowledgment

- [ ] Evidence classes match formula status.
- [ ] Intervals preserve uncertainty.
- [ ] Simulation assumptions are explicit.
- [ ] No proxy is presented as direct observation.

Reviewer notes:

```text

```

Reviewer:

```text

```

Date:

```text

```

### Technical Maintainer acknowledgment

- [ ] JSON schema is implementable.
- [ ] Markdown rendering is deterministic.
- [ ] Partial reports can preserve valid capabilities.
- [ ] Required fields can be serialized without NaN or hidden coercion.
- [ ] Redaction can occur after calculation.

Technical notes:

```text

```

Maintainer:

```text

```

Date:

```text

```

---

## 39. Change-control rule

After approval:

1. report-section order must not change without schema review,
2. a public field must not change evidence class silently,
3. a denominator change requires a new field name or schema version,
4. a simulation must not move into derived metrics without approved validation,
5. a proxy must not move into observed facts without direct evidence,
6. unavailable conclusions must remain visible when relevant,
7. redaction must not alter calculated values,
8. language restrictions must be covered by golden tests,
9. new capabilities require observability requirements and capability status rules,
10. new public metrics require traceability and report-schema entries,
11. report convenience must not weaken uncertainty or overstate causal meaning.
