# DEFINITIONS_AND_UNITS

## Document control

| Field | Value |
|---|---|
| Project | Recursive Integrity Toolkit |
| Target release | v0.1 |
| Phase | Phase 0 |
| Status | APPROVED PHASE 0 BASELINE |
| Primary owner | Theory Owner |
| Technical reviewers | Mathematical Reviewer, Technical Maintainer |
| Depends on | `SPEC_AUDIT.md`, `THEORY_SOURCE_MAP.md`, `UNRESOLVED_DECISIONS.md`, `PROJECT_INSTRUCTIONS.md`, `V0.1_PRODUCT_SPEC.md` |
| Purpose | Freeze canonical terminology, units, value domains, formulas, denominators, missingness rules, and interpretive boundaries for v0.1 |

This file defines the canonical vocabulary and measurement conventions of Recursive Integrity Toolkit v0.1.

All code, schemas, tests, reports, CLI help, and documentation must use these meanings. A public result cannot use a term defined here with a different denominator, unit, representation, or evidence class.

Definitions marked `APPROVED DECISION` become implementation-authoritative only after the corresponding `UD-*` entry is approved.

---

## 1. General conventions

### 1.1 Normative words

| Word | Meaning |
|---|---|
| `must` | Required for conformance |
| `must not` | Prohibited |
| `should` | Recommended unless a documented reason justifies another choice |
| `may` | Optional |
| `required` | Needed for the stated input, output, metric, or phase |
| `optional` | May be absent without invalidating the whole run |
| `deferred` | Preserved for later work and excluded from v0.1 public computation |
| `unavailable` | The present evidence does not support the conclusion |

### 1.2 Identifier comparison

Unless a schema mapping explicitly states otherwise:

- identifiers are strings,
- identifiers are case-sensitive,
- leading and trailing whitespace in identifiers is invalid after normalization,
- empty identifiers are invalid,
- identifiers are not converted to numbers,
- filenames do not establish identity,
- display labels do not replace canonical identifiers.

### 1.3 Count, ratio, share, and percentage

| Quantity | Canonical storage | Unit |
|---|---|---|
| count | non-negative integer | records, states, roots, edges, files, or events |
| ratio | finite number in \([0,1]\), unless another range is defined | dimensionless |
| share | finite number in \([0,1]\) | dimensionless |
| probability | finite number in \([0,1]\) | dimensionless |
| percentage | display form of a ratio multiplied by 100 | percent |

Machine-readable outputs store shares and probabilities as ratios.

Example:

```json
{
  "synthetic_share": 0.5
}
```

A human-readable report may display the same value as `50.00%`.

### 1.4 Missing, unknown, unavailable, and zero

These states have different meanings.

| State | Meaning | Machine-readable form |
|---|---|---|
| missing field | Expected input field or value is absent | absent key or `null`, according to schema |
| unknown enum value | The input explicitly declares lack of knowledge | `"unknown"` |
| unavailable result | The toolkit cannot calculate or support a conclusion | `null` plus reason code |
| zero | A measured or calculated quantity equals zero | `0` or `0.0` |
| not applicable | The concept does not apply to the current run | `null` plus applicability reason |

Rules:

- unknown must not be converted to zero,
- unavailable must not be converted to zero,
- a missing provenance row must not be treated as `source_type=human`,
- `external_grounding=unknown` must remain unknown,
- JSON outputs must not use `NaN`, positive infinity, or negative infinity,
- a result with a zero denominator is unavailable unless a separate definition states otherwise.

### 1.5 Internal numeric precision

Recommended v0.1 convention:

- integer counts use exact integers,
- numerical metrics use IEEE 754 double precision,
- JSON emits finite numerical values without display rounding,
- Markdown may round ratios and metrics to four decimal places,
- Markdown percentages may round to two decimal places,
- tests compare floating-point values using approved tolerances,
- golden outputs must declare the tolerance where exact decimal identity is not guaranteed.

`APPROVED DECISION`: exact display precision may be changed by the reporting specification without changing metric meaning.

### 1.6 Deterministic ordering

When output order has no mathematical meaning, use a deterministic sort order.

Recommended order:

1. descending primary metric,
2. descending count,
3. canonical identifier in ascending Unicode code-point order.

Rarity rankings reverse the primary metric and sort from lowest frequency to highest frequency.

Tie-breaking rules must be recorded in the report schema.

### 1.7 Time

| Term | Canonical type | Unit |
|---|---|---|
| timestamp | ISO 8601 datetime | UTC or declared offset |
| duration | non-negative number | seconds |
| dataset time | source or snapshot time | ISO 8601 datetime |
| run start and end | execution timestamps | UTC |

A timestamp without timezone information must be:

- rejected in strict mode, or
- interpreted only through an explicit configuration rule.

The toolkit must not silently assume local time.

### 1.8 File size and memory

| Quantity | Canonical unit |
|---|---|
| file size | bytes |
| memory estimate | bytes |
| human-readable display | KiB, MiB, GiB using binary units |

---

## 2. Core entities

### 2.1 Record

| Field | Definition |
|---|---|
| Canonical term | `record` |
| Definition | One analyzable sample row in a dataset version |
| Unit | record |
| Identity | composite record key |
| Required public fields | `record_id`, `dataset_version`, `content` |
| Theory relation | A record is one realized sample, not automatically one independent source |

A record may contain:

- inline content,
- a local content reference,
- a topic,
- a label,
- a timestamp,
- a weight,
- an embedding reference,
- provenance metadata.

A large record count does not establish large independent ancestry.

### 2.2 Record ID

| Field | Definition |
|---|---|
| Canonical field | `record_id` |
| Type | non-empty string |
| Uniqueness | unique within one `dataset_version` |
| Unit | identifier |
| Case sensitivity | case-sensitive |

The pair `(dataset_version, record_id)` defines canonical record identity.

### 2.3 Composite record key

| Field | Definition |
|---|---|
| Canonical term | `record_key` |
| Type | ordered pair of strings |
| Components | `dataset_version`, `record_id` |
| Text serialization | `dataset_version::record_id` |
| Example | `v1::v1_01` |

The text serialization is a transport format. Internal implementations may use tuples or immutable record-key objects.

The separator `::` must not be parsed from arbitrary unvalidated identifiers without escaping rules defined in `DATA_AND_PROVENANCE_SPEC.md`.

### 2.4 Content

| Field | Definition |
|---|---|
| Canonical field | `content` |
| Type | string or local content reference |
| Unit | payload |
| Required | yes |
| Logging status | excluded from normal logs |

`content` is the primary analyzable payload.

A content reference does not authorize network retrieval.

### 2.5 Dataset

| Field | Definition |
|---|---|
| Canonical term | `dataset` |
| Definition | A named collection of one or more dataset versions |
| Type | logical collection |
| Unit | dataset |

A dataset may have multiple files, but file boundaries do not automatically define dataset versions.

### 2.6 Dataset version

| Field | Definition |
|---|---|
| Canonical field | `dataset_version` |
| Type | non-empty string |
| Definition | A stable named or timestamped snapshot of records |
| Unit | version identifier |
| Ordering | requires explicit evidence |

Version IDs do not establish chronology through lexical order.

Valid ordering evidence includes:

- explicit `version_order`,
- valid timestamps,
- user-declared CLI order.

Related decision: `UD-007`.

### 2.7 Version order

| Field | Definition |
|---|---|
| Canonical term | `version_order` |
| Type | ordered list or integer rank |
| Unit | ordinal position |
| Purpose | Establish earlier and later versions for longitudinal analysis |

A lower ordinal rank represents an earlier version unless the configuration explicitly states another convention.

### 2.8 Batch

| Field | Definition |
|---|---|
| Canonical field | `batch_id` |
| Type | optional string |
| Definition | A declared group of records sharing a production, collection, or transformation event |
| Unit | batch identifier |

Batch membership does not establish shared ancestry unless parent or process evidence supports that conclusion.

### 2.9 Run

| Field | Definition |
|---|---|
| Canonical term | `run` |
| Definition | One execution of the toolkit using a resolved set of inputs and configuration |
| Identity | `run_id` |
| Unit | execution |
| Required metadata | toolkit version, input hashes, resolved config, timestamps |

The run ID identifies the audit execution, not a training run unless a mapping explicitly connects them.

### 2.10 Audit session

| Field | Definition |
|---|---|
| Canonical term | `audit_session` |
| Definition | One or more related toolkit runs grouped by a user or workflow |
| Unit | context |
| v0.1 status | optional metadata |

### 2.11 Artifact

| Field | Definition |
|---|---|
| Canonical term | `artifact` |
| Definition | A file or structured object consumed or produced by a run |
| Examples | records file, provenance manifest, config, JSON report |
| Unit | artifact |

The term supports compatibility with lineage ecosystems. It does not create a mandatory external metadata dependency.

### 2.12 Generator

| Field | Definition |
|---|---|
| Canonical field | `generator_id` |
| Type | optional string |
| Definition | Declared model, process, system, or authoring mechanism associated with record creation |
| Unit | generator identifier |

`generator_id` does not establish source independence.

### 2.13 Generator version

| Field | Definition |
|---|---|
| Canonical field | `generator_version` |
| Type | optional string |
| Definition | Declared version of the generator |
| Unit | version identifier |

A changed generator version does not automatically create external difference.

### 2.14 Transformation

| Field | Definition |
|---|---|
| Canonical field | `transformation` |
| Type | enum |
| Definition | Declared operation connecting a record to its parent inputs |

Allowed v0.1 values:

- `generate`
- `rewrite`
- `summarize`
- `translate`
- `filter`
- `label`
- `carryover`
- `other`

Transformation describes the declared operation. It does not determine grounding by itself.

### 2.15 Manifest

| Field | Definition |
|---|---|
| Canonical term | `provenance_manifest` |
| Definition | A sidecar table containing record-level origin, grounding, transformation, and lineage metadata |
| Unit | manifest |
| Join key | composite record key |

### 2.16 Schema mapping

| Field | Definition |
|---|---|
| Canonical term | `schema_mapping` |
| Definition | Declarative rules mapping user field names and supported source values to canonical fields and values |
| Unit | mapping specification |

A schema mapping must not execute arbitrary code.

---

## 3. Provenance vocabulary

### 3.1 Provenance

| Field | Definition |
|---|---|
| Canonical term | `provenance` |
| Definition | Declared and validated information about a record's origin, creation process, grounding, and lineage |
| Unit | metadata state |

Provenance describes available evidence. It does not guarantee truth beyond the declared confidence.

### 3.2 Source type

| Field | Definition |
|---|---|
| Canonical field | `source_type` |
| Type | enum |
| Unit | category |
| Required in matched provenance row | yes |

Allowed values:

| Value | Meaning |
|---|---|
| `human` | Declared direct human authorship or human-origin material |
| `synthetic` | Declared machine-generated or procedurally generated origin |
| `mixed` | Declared combination of multiple source classes that cannot be represented as one class |
| `sensor` | Declared measurement from a physical or digital sensing system |
| `unknown` | Source class is not known |

Rules:

- source type does not determine external grounding,
- human source does not prove independence,
- synthetic source does not prove closure,
- mixed remains a distinct category unless explicit component weights are supplied,
- sensor data may still belong to a closed internal process.

Related decision: `UD-009`.

### 3.3 Provenance confidence

| Field | Definition |
|---|---|
| Canonical field | `provenance_confidence` |
| Type | enum |
| Unit | category |

Allowed values:

| Value | Meaning |
|---|---|
| `confirmed` | Supported by direct authoritative record or controlled creation process |
| `log_derived` | Derived from retained system logs or process records |
| `estimated` | Assigned through a declared estimation procedure |
| `unknown` | Confidence cannot be established |

Confidence applies to the provenance assignment.

It must not be converted into a probability unless a separate calibrated model defines that mapping.

### 3.4 Human reviewed

| Field | Definition |
|---|---|
| Canonical field | `human_reviewed` |
| Type | nullable boolean |
| Unit | flag |
| Values | `true`, `false`, `null` |

Meaning:

- `true`: a human review event is declared,
- `false`: no human review is declared,
- `null`: review status is unknown or unavailable.

Human review does not prove:

- human origin,
- external grounding,
- factual correctness,
- independent ancestry,
- integrity.

### 3.5 External grounding

| Field | Definition |
|---|---|
| Canonical field | `external_grounding` |
| Type | enum |
| Unit | category |
| Status | `APPROVED DECISION UD-009` |

Allowed values:

| Value | Meaning |
|---|---|
| `yes` | The record contains or preserves signal grounded outside the audited recursive loop according to supplied provenance |
| `no` | The record is declared to depend only on the audited internal recursive process for the relevant signal |
| `unknown` | Available evidence cannot determine grounding |

External grounding is relational to the audited loop.

A record can be:

- human and ungrounded,
- synthetic and grounded,
- mixed and unknown,
- sensor-derived and internal to a closed loop.

A grounded carryover can preserve external signal without constituting a new independent external root.

### 3.6 Grounding evidence

| Field | Definition |
|---|---|
| Canonical term | `grounding_evidence` |
| Definition | Metadata or records supporting the `external_grounding` assignment |
| Type | optional reference or note |
| Unit | evidence reference |

v0.1 may preserve this field without evaluating the truth of external evidence.

### 3.7 Known open record

| Field | Definition |
|---|---|
| Canonical internal class | `known_open` |
| Condition | `external_grounding=yes` with a valid provenance row |
| Unit | record classification |
| Use | direct closure exposure bounds |

The class is relative to direct record-level grounding metadata.

### 3.8 Known closed record

| Field | Definition |
|---|---|
| Canonical internal class | `known_closed` |
| Condition | `external_grounding=no` with a valid provenance row |
| Unit | record classification |
| Use | direct closure exposure bounds |

### 3.9 Unresolved grounding record

| Field | Definition |
|---|---|
| Canonical internal class | `unresolved_grounding` |
| Condition | missing provenance row, invalid grounding, or `external_grounding=unknown` |
| Unit | record classification |
| Use | uncertainty envelope |

### 3.10 Provenance row coverage

Let:

- \(N\) be total analyzed records,
- \(N_{\text{prov row}}\) be records with one valid matching provenance row.

Then:

\[
P_{\text{row}}
=
\frac{N_{\text{prov row}}}{N}
\]

| Property | Value |
|---|---|
| Canonical field | `provenance_row_coverage` |
| Unit | ratio |
| Range | \([0,1]\) |
| Evidence class | observed fact |
| Zero denominator | unavailable, empty dataset is invalid |

A matching row can still contain unknown values.

### 3.11 Provenance required-field coverage

Let \(N_{\text{required valid}}\) be records whose matched provenance row contains valid required fields.

\[
P_{\text{required}}
=
\frac{N_{\text{required valid}}}{N}
\]

| Property | Value |
|---|---|
| Canonical field | `provenance_required_field_coverage` |
| Unit | ratio |
| Range | \([0,1]\) |
| Evidence class | observed fact |

Required provenance fields are defined by `DATA_AND_PROVENANCE_SPEC.md`.

### 3.12 Grounding-field coverage

Let \(N_{\text{grounding known}}\) be records whose valid grounding value is `yes` or `no`.

\[
P_{\text{grounding}}
=
\frac{N_{\text{grounding known}}}{N}
\]

| Property | Value |
|---|---|
| Canonical field | `grounding_field_coverage` |
| Unit | ratio |
| Range | \([0,1]\) |
| Evidence class | observed fact |

`unknown` does not count as known grounding.

### 3.13 Field coverage

For provenance field \(f\):

\[
P_f
=
\frac{N_{\text{valid nonmissing } f}}{N}
\]

| Property | Value |
|---|---|
| Canonical term | `field_coverage` |
| Unit | ratio |
| Use | exact disclosure for fields powering conclusions |

A report must name the field and denominator.

---

## 4. Lineage vocabulary

### 4.1 Parent

| Field | Definition |
|---|---|
| Canonical field | `parent_ids` |
| Type | list of composite record references |
| Definition | Immediate predecessor records declared as inputs to a record |
| Unit | record references |

An empty list means no declared parent.

An empty list does not automatically prove external grounding.

### 4.2 Parent edge

| Field | Definition |
|---|---|
| Canonical term | `parent_edge` |
| Direction | parent to child |
| Type | directed graph edge |
| Unit | edge |

The generational ancestry graph must be acyclic for lineage analysis.

### 4.3 Resolved parent

A parent reference is resolved when it maps to exactly one loaded composite record key.

### 4.4 Unresolved parent

| Field | Definition |
|---|---|
| Canonical term | `unresolved_parent` |
| Condition | parent reference maps to no loaded record |
| Default severity | warning |
| Unit | reference failure |

An unresolved parent must not be converted into an external root.

### 4.5 Ambiguous parent

| Field | Definition |
|---|---|
| Canonical term | `ambiguous_parent` |
| Condition | parent reference maps to more than one possible record |
| Default severity | error |
| Unit | reference failure |

### 4.6 Ancestor

| Field | Definition |
|---|---|
| Canonical term | `ancestor` |
| Definition | Any upstream record reachable through one or more parent edges |
| Unit | record |
| Type | set member |

A record is not its own ancestor.

### 4.7 Descendant

| Field | Definition |
|---|---|
| Canonical term | `descendant` |
| Definition | Any downstream record reachable through one or more child edges |
| Unit | record |

### 4.8 Root

| Field | Definition |
|---|---|
| Canonical term | `lineage_root` |
| Definition | A loaded record with no resolved parent edge inside the analyzed graph |
| Unit | record |

A lineage root can be:

- externally grounded,
- internally generated with missing earlier history,
- unknown.

Root status alone does not prove external grounding.

### 4.9 External root

| Field | Definition |
|---|---|
| Canonical term | `external_root` |
| Definition | A lineage anchor supported by `external_grounding=yes` whose grounding is not inherited solely from an earlier declared parent in the loaded lineage |
| Unit | record |
| Evidence class | derived metric when identified through validated metadata |

Operational rules:

1. a directly grounded parentless record can be an external root,
2. a grounded carryover remains linked to its earlier external root,
3. a carryover must not be counted as a new independent root solely because it has `external_grounding=yes`,
4. a new external source introduced during a transformation may form a new root only when provenance declares that source,
5. ambiguous grounding ancestry produces unresolved root status.

Exact root-collapsing rules belong in `DATA_AND_PROVENANCE_SPEC.md`.

### 4.10 Reachable external-root set

For record \(r\):

\[
A_r
=
\{a : a \text{ is a validated external root reachable from } r\}
\]

| Property | Value |
|---|---|
| Canonical field | `reachable_external_roots` |
| Type | set of record keys |
| Unit | roots |

A fully resolved empty set can support a known-closed lineage classification.

An empty set caused by missing ancestry remains unresolved.

### 4.11 Generation

| Field | Definition |
|---|---|
| Canonical field | `generation` |
| Type | nullable non-negative integer |
| Unit | recursive non-grounding steps |
| Status | `APPROVED DECISION UD-005` |

Recommended definition:

> The number of consecutive non-grounding generative steps since the most recent externally grounded state.

Rules:

- externally grounded record: generation may be 0,
- grounded carryover: generation may remain 0,
- ungrounded child with known parent generation: expected generation is one plus the maximum relevant parent generation,
- unknown grounding or unresolved parent can make expected generation unavailable,
- generation does not mean training epoch,
- generation does not mean model release,
- generation does not mean dataset-version number,
- generation does not equal graph depth in every case.

### 4.12 Expected generation

For a record with validated metadata:

\[
g_{\text{expected}}(r)
=
\begin{cases}
0, & \text{if external grounding is yes} \\
1+\max_{p \in Parents(r)} g(p), & \text{if grounding is no and all required parents are resolved} \\
\text{unavailable}, & \text{otherwise}
\end{cases}
\]

This equation is a validation convention for v0.1.

It does not replace the theory's general concept of recursive depth.

### 4.13 Generation mismatch

A generation mismatch occurs when a declared generation conflicts with the computable expected generation under the approved validation convention.

Default classification:

```text
warning
```

Strict mode may elevate impossible combinations to an error.

### 4.14 Lineage depth

| Field | Definition |
|---|---|
| Canonical field | `lineage_depth` |
| Type | nullable non-negative integer |
| Unit | parent edges |
| Definition | Maximum number of resolved parent edges from a record to any loaded lineage root |
| Evidence class | derived metric |

For a loaded root:

\[
d(r)=0
\]

For a non-root record with fully resolved parents:

\[
d(r)
=
1+\max_{p \in Parents(r)}d(p)
\]

If a required path is unresolved, lineage depth is partial or unavailable according to the reporting specification.

`lineage_depth` and `generation` must remain separate fields.

### 4.15 Cycle

| Field | Definition |
|---|---|
| Canonical term | `lineage_cycle` |
| Definition | A directed path in the ancestry graph that returns to a previously visited record |
| Unit | graph condition |
| Evidence class | observed fact or error |
| Source class | graph-validity engineering rule |

A cycle invalidates generational ancestry interpretation for the affected graph.

A real process feedback loop may be represented at run or process level without forcing the record-ancestry graph to contain a cycle.

### 4.16 Resolved-parent edge coverage

Let:

- \(E_{\text{declared}}\) be declared parent references,
- \(E_{\text{resolved}}\) be references resolving to one loaded record.

\[
P_{\text{edge resolved}}
=
\frac{E_{\text{resolved}}}{E_{\text{declared}}}
\]

| Property | Value |
|---|---|
| Canonical field | `resolved_parent_edge_coverage` |
| Unit | ratio |
| Range | \([0,1]\) |
| Zero denominator | `1.0` when no parent references are declared, with explicit `no_declared_parents=true` |

The zero-parent convention describes reference completeness. It does not establish lineage richness.

### 4.17 Fully resolved lineage record

A record has fully resolved lineage when:

- all required parent references resolve,
- no reachable cycle exists,
- every ancestry branch reaches a classifiable root or a declared stopping boundary,
- external-root status can be determined under the approved rules.

### 4.18 Resolved lineage coverage

Let \(N_{\text{lineage resolved}}\) be records with fully resolved lineage classification.

\[
P_{\text{lineage resolved}}
=
\frac{N_{\text{lineage resolved}}}{N}
\]

| Property | Value |
|---|---|
| Canonical field | `resolved_lineage_coverage` |
| Unit | ratio |
| Range | \([0,1]\) |

### 4.19 Records with resolved external ancestry

| Field | Definition |
|---|---|
| Canonical field | `records_with_resolved_external_ancestry` |
| Type | non-negative integer |
| Unit | records |
| Definition | Records whose complete reachable external-root set is known, including a known empty set |

### 4.20 Externally rooted record

A record is externally rooted when its fully resolved reachable external-root set is nonempty.

### 4.21 External ancestry coverage

Let \(N_{\text{externally rooted}}\) be analyzed records with a nonempty fully resolved external-root set.

\[
P_{\text{external ancestry}}
=
\frac{N_{\text{externally rooted}}}{N}
\]

| Property | Value |
|---|---|
| Canonical field | `external_ancestry_coverage` |
| Unit | ratio |
| Range | \([0,1]\) |
| Evidence class | derived metric |

This measure describes the share of analyzed records with resolved external ancestry.

It must be reported alongside `resolved_lineage_coverage`.

### 4.22 Distinct external-root count

\[
K_{\text{external roots}}
=
\left|
\bigcup_{r \in G} A_r
\right|
\]

where \(G\) is the set of externally rooted records with fully resolved root sets.

| Property | Value |
|---|---|
| Canonical field | `distinct_external_root_count` |
| Unit | roots |
| Type | non-negative integer |
| Evidence class | derived metric |

### 4.23 Ancestor incidence count

For external root \(a\):

\[
I_a
=
\left|
\{r : a \in A_r\}
\right|
\]

| Property | Value |
|---|---|
| Canonical field | `ancestor_incidence_count` |
| Unit | records |
| Type | non-negative integer |

A record with multiple roots contributes one incidence to each reachable root.

### 4.24 Ancestor incidence share

Canonical denominator:

\[
S_a^{\text{all}}
=
\frac{I_a}{N}
\]

| Property | Value |
|---|---|
| Canonical field | `ancestor_incidence_share` |
| Unit | ratio |
| Range | \([0,1]\) |

The report must also show lineage coverage so the denominator does not hide unresolved ancestry.

An optional resolved-only share may use:

\[
S_a^{\text{resolved}}
=
\frac{I_a}{N_{\text{lineage resolved}}}
\]

with field name:

```text
ancestor_incidence_share_resolved
```

### 4.25 Fractional external-root mass

For externally rooted record \(r\) with \(k_r=|A_r|\):

\[
m_{r,a}
=
\begin{cases}
1/k_r, & a \in A_r \\
0, & a \notin A_r
\end{cases}
\]

Aggregate mass for root \(a\):

\[
M_a
=
\sum_{r \in G}m_{r,a}
\]

Each externally rooted record contributes total mass 1.

### 4.26 Normalized external-root share

\[
w_a
=
\frac{M_a}{\sum_b M_b}
\]

Because each record in \(G\) contributes total mass 1:

\[
\sum_b M_b=|G|
\]

| Property | Value |
|---|---|
| Canonical field | `external_root_fractional_share` |
| Unit | ratio |
| Range | \([0,1]\) |
| Sum | 1 across roots when \(G\) is nonempty |

### 4.27 Ancestry concentration HHI

\[
HHI_{\text{ancestry}}
=
\sum_a w_a^2
\]

| Property | Value |
|---|---|
| Canonical field | `ancestry_concentration_hhi` |
| Unit | dimensionless |
| Range | \((0,1]\) when at least one root exists |
| Evidence class | derived metric |
| Status | `APPROVED DECISION UD-014` |

Interpretation:

- 1 indicates all fractional root mass belongs to one external root,
- lower values indicate broader root distribution,
- the minimum equals \(1/K\) when mass is evenly divided across \(K\) roots.

The metric describes lineage topology.

It does not measure:

- causal influence,
- semantic error,
- record quality,
- biological relatedness.

### 4.28 Effective external-root count

\[
N_{\text{effective roots}}
=
\frac{1}{HHI_{\text{ancestry}}}
\]

| Property | Value |
|---|---|
| Canonical field | `effective_external_root_count` |
| Unit | effective roots |
| Range | \([1,K]\) when \(K>0\) |
| Evidence class | derived metric |

This value is the inverse concentration equivalent.

It must not be called universal source diversity.

### 4.29 Top shared ancestor

| Field | Definition |
|---|---|
| Canonical field | `top_shared_ancestors` |
| Definition | External roots ranked by ancestor incidence count |
| Type | ordered list |
| Tie-break | incidence count, then canonical record key |

The hero fixture uses incidence count.

---

## 5. Closure vocabulary

### 5.1 Closed recursion

| Field | Definition |
|---|---|
| Canonical term | `closed_recursion` |
| Definition | A process in which future states are generated primarily from prior internal outputs while externally grounded input, heterogeneous recombination, or corrective contact remains insufficient to preserve required functional difference |
| Unit | structural condition |
| Direct observability | limited |

The toolkit measures evidence related to closure.

It does not directly observe every hidden dependency in a production system.

### 5.2 Closure exposure

| Field | Definition |
|---|---|
| Canonical term | `closure_exposure` |
| Definition | The share of analyzed records whose available grounding or lineage evidence is consistent with internal recursive dependence |
| Unit | ratio or interval |
| Evidence class | derived metric |
| Status | toolkit operationalization |

Closure exposure is an audit construct guided by theory.

It is not a universal theorem-level score.

### 5.3 Direct closure exposure lower bound

Let:

- \(N_C\) be known-closed records,
- \(N_U\) be unresolved-grounding records,
- \(N\) be total records.

\[
C_{\min}^{\text{direct}}
=
\frac{N_C}{N}
\]

| Property | Value |
|---|---|
| Canonical field | `direct_closure_exposure_lower_bound` |
| Unit | ratio |
| Range | \([0,1]\) |

### 5.4 Direct closure exposure upper bound

\[
C_{\max}^{\text{direct}}
=
\frac{N_C+N_U}{N}
\]

| Property | Value |
|---|---|
| Canonical field | `direct_closure_exposure_upper_bound` |
| Unit | ratio |
| Range | \([0,1]\) |

### 5.5 Direct closure exposure interval width

\[
W_C^{\text{direct}}
=
C_{\max}^{\text{direct}}
-
C_{\min}^{\text{direct}}
=
\frac{N_U}{N}
\]

| Property | Value |
|---|---|
| Canonical field | `direct_closure_exposure_interval_width` |
| Unit | ratio |
| Interpretation | uncertainty created by unresolved direct grounding evidence |

### 5.6 Lineage known grounded

A record is `lineage_known_grounded` when:

- its reachable ancestry is fully resolved,
- at least one validated external root is reachable,
- no blocking ancestry ambiguity remains.

### 5.7 Lineage known closed

A record is `lineage_known_closed` when:

- its reachable ancestry is fully resolved,
- no validated external root is reachable,
- no unresolved parent or grounding ambiguity remains.

### 5.8 Lineage unresolved

A record is `lineage_unresolved` when any required ancestry path contains:

- unresolved parent,
- ambiguous parent,
- unknown grounding,
- conflicting grounding evidence,
- cycle,
- undeclared stopping boundary.

### 5.9 Lineage closure exposure bounds

Let:

- \(N_{LC}\) be lineage-known-closed records,
- \(N_{LU}\) be lineage-unresolved records.

\[
C_{\min}^{\text{lineage}}
=
\frac{N_{LC}}{N}
\]

\[
C_{\max}^{\text{lineage}}
=
\frac{N_{LC}+N_{LU}}{N}
\]

| Field | Unit |
|---|---|
| `lineage_closure_exposure_lower_bound` | ratio |
| `lineage_closure_exposure_upper_bound` | ratio |
| `lineage_closure_exposure_interval_width` | ratio |

Direct and lineage bounds must not be merged into one unlabeled number.

### 5.10 Closure classification completeness

\[
P_{\text{closure classified}}
=
\frac{N-N_U}{N}
\]

Direct and lineage variants must use distinct field names.

---

## 6. Representation vocabulary

### 6.1 Representation

| Field | Definition |
|---|---|
| Canonical term | `representation` |
| Definition | The declared mapping that converts records into analyzable states |
| Unit | mapping |
| Required for | support, diversity, tail, extinction, state-level comparison |

Examples:

- topic,
- label,
- exact normalized content hash,
- user-provided embedding cluster,
- declared bin.

### 6.2 Representation name

| Field | Definition |
|---|---|
| Canonical field | `representation_name` |
| Type | non-empty string |
| Example | `topic` |

### 6.3 Representation source

| Field | Definition |
|---|---|
| Canonical field | `representation_source` |
| Type | enum or string |
| Recommended values | `config`, `topic_field`, `label_field`, `embedding_clusters`, `content_hash` |

### 6.4 Representation version

| Field | Definition |
|---|---|
| Canonical field | `representation_version` |
| Type | string or `null` |
| Definition | Version of the mapping, taxonomy, embedding model, clustering output, or normalization profile |

### 6.5 Binning or mapping rule

| Field | Definition |
|---|---|
| Canonical field | `binning_or_mapping_rule` |
| Type | structured object or string |
| Definition | Exact rule assigning records to states |

### 6.6 State

| Field | Definition |
|---|---|
| Canonical term | `state` |
| Definition | One distinct value or bin under the selected representation |
| Unit | state |
| Identity | canonical state identifier |

A state is representation-dependent.

### 6.7 State identifier

| Field | Definition |
|---|---|
| Canonical term | `state_id` |
| Type | stable string |
| Unit | identifier |

### 6.8 Representation fallback

A fallback occurs when the toolkit selects a lower-priority representation because the preferred representation is unavailable.

A fallback must:

- be explicit,
- be reported,
- emit the approved warning,
- preserve the distinction between record-form and semantic support.

Related decision: `UD-011`.

### 6.9 Representation compatibility

Two versions are representation-compatible when:

- the representation name matches,
- the state semantics match,
- the representation version matches or an approved mapping exists,
- the binning or mapping rule is compatible.

Filename similarity does not establish compatibility.

### 6.10 Exact content normalization profile

| Field | Definition |
|---|---|
| Canonical term | `content_normalization_profile` |
| Definition | Declared deterministic transformation applied before exact hashing |
| Unit | configuration |
| Exact rules | controlled by `DATA_AND_PROVENANCE_SPEC.md` |

A content hash state represents normalized record form.

It must not be labeled semantic content.

---

## 7. Distribution and support vocabulary

### 7.1 State count

For state \(i\):

\[
n_i
=
\text{number of analyzed records assigned to state } i
\]

| Property | Value |
|---|---|
| Canonical field | `state_count` |
| Unit | records |
| Type | non-negative integer |

### 7.2 Total analyzed record count

\[
N
=
\sum_i n_i
\]

| Property | Value |
|---|---|
| Canonical field | `analyzed_record_count` |
| Unit | records |

### 7.3 Empirical state frequency

\[
p_i
=
\frac{n_i}{N}
\]

| Property | Value |
|---|---|
| Canonical field | `state_frequency` |
| Unit | ratio |
| Range | \([0,1]\) |
| Sum | 1 over observed states when \(N>0\) |

### 7.4 Support

\[
\operatorname{supp}(p)
=
\{i:p_i>0\}
\]

| Property | Value |
|---|---|
| Canonical term | `support` |
| Definition | Set of distinct observed states under the declared representation |
| Unit | set of states |

### 7.5 Support size

\[
K
=
|\operatorname{supp}(p)|
\]

| Property | Value |
|---|---|
| Canonical field | `support_size` |
| Unit | states |
| Type | non-negative integer |
| Evidence class | derived metric |

### 7.6 Record-form support

| Field | Definition |
|---|---|
| Canonical term | `record_form_support` |
| Definition | Support calculated from exact normalized content hashes |
| Unit | normalized record forms |

Record-form support must remain visibly distinct from topic, label, or semantic support.

### 7.7 Support delta

For earlier version \(a\) and later version \(b\):

\[
\Delta K
=
K_b-K_a
\]

| Property | Value |
|---|---|
| Canonical field | `support_delta` |
| Unit | states |
| Sign convention | later minus earlier |

Negative values indicate observed support contraction under the declared representation.

### 7.8 Support retention ratio

\[
R_{\text{support}}
=
\frac{|S_a \cap S_b|}{|S_a|}
\]

| Property | Value |
|---|---|
| Canonical field | `support_retention_ratio` |
| Unit | ratio |
| Range | \([0,1]\) |
| Zero denominator | unavailable if earlier support is empty |

### 7.9 Support loss count

\[
L_{\text{support}}
=
|S_a \setminus S_b|
\]

| Property | Value |
|---|---|
| Canonical field | `support_loss_count` |
| Unit | states |

### 7.10 Added-state count

\[
A_{\text{support}}
=
|S_b \setminus S_a|
\]

| Property | Value |
|---|---|
| Canonical field | `support_added_count` |
| Unit | states |

### 7.11 Extinct observed state

A state is `observed_extinct` from version \(a\) to version \(b\) when:

- it appears in \(a\),
- it is absent from \(b\),
- \(a\) precedes \(b\),
- representations are compatible.

This means:

> absent from the observed later version under the declared representation.

It does not establish permanent absence from the full production process.

### 7.12 Extinct-state set

\[
E_{a\rightarrow b}
=
S_a \setminus S_b
\]

| Property | Value |
|---|---|
| Canonical field | `extinct_states` |
| Unit | set of states |
| Evidence class | derived metric |

---

## 8. Duplicate vocabulary

### 8.1 Exact duplicate

| Field | Definition |
|---|---|
| Canonical term | `exact_duplicate` |
| Definition | Two or more records sharing the same content hash under the declared normalization profile |
| Unit | record relation |
| Evidence class | observed fact |

### 8.2 Exact duplicate group

| Field | Definition |
|---|---|
| Canonical term | `exact_duplicate_group` |
| Definition | Maximal set of records with the same normalized content hash |
| Unit | group |

### 8.3 Duplicate record count

Recommended definition:

\[
N_{\text{duplicate records}}
=
\sum_{g}(|g|-1)
\]

where \(g\) ranges over exact duplicate groups.

| Property | Value |
|---|---|
| Canonical field | `duplicate_record_count` |
| Unit | records |

This counts records beyond the first representative in each group.

### 8.4 Duplicate group count

\[
N_{\text{duplicate groups}}
=
|\{g:|g|>1\}|
\]

| Property | Value |
|---|---|
| Canonical field | `duplicate_group_count` |
| Unit | groups |

### 8.5 Near duplicate

| Field | Definition |
|---|---|
| Canonical term | `near_duplicate` |
| Definition | Pair or group satisfying an explicitly configured similarity method and threshold |
| Unit | relation |
| v0.1 status | optional |

No universal near-duplicate threshold is defined in v0.1.

---

## 9. Diversity vocabulary

### 9.1 Diversity

| Field | Definition |
|---|---|
| Canonical term | `diversity` |
| Definition | Distributional spread under a declared representation and metric |
| Unit | metric-specific, usually dimensionless |

A diversity value must name its metric.

### 9.2 Gini-Simpson diversity

\[
D
=
1-\sum_{i=1}^{K}p_i^2
\]

| Property | Value |
|---|---|
| Canonical field | `gini_simpson_diversity` |
| Unit | dimensionless |
| Range | \([0,1)\) for finite observed support |
| Minimum | 0 when all mass occupies one state |
| Maximum for fixed \(K\) | \(1-1/K\) under equal frequencies |
| Evidence class | derived metric |

Gini-Simpson diversity is the default v0.1 diversity metric.

### 9.3 Simpson concentration

\[
C_{\text{Simpson}}
=
\sum_i p_i^2
\]

| Property | Value |
|---|---|
| Canonical field | `simpson_concentration` |
| Unit | dimensionless |
| Relation | \(C_{\text{Simpson}}=1-D\) |

This distributional concentration must not be confused with ancestry concentration HHI, though the mathematical form is similar.

### 9.4 Diversity delta

For earlier version \(a\) and later version \(b\):

\[
\Delta D
=
D_b-D_a
\]

| Property | Value |
|---|---|
| Canonical field | `gini_simpson_diversity_delta` |
| Unit | dimensionless |
| Sign convention | later minus earlier |

A negative delta indicates observed diversity contraction under the selected representation.

### 9.5 Weighted state mass

When weighted analysis is explicitly enabled:

\[
m_i
=
\sum_{r \in i}w_r
\]

\[
p_i^{(w)}
=
\frac{m_i}{\sum_j m_j}
\]

Requirements:

- \(w_r\) is finite,
- \(w_r\geq0\),
- total weight is positive.

Weighted outputs must use distinct field names, such as:

```text
weighted_gini_simpson_diversity
```

Unweighted results remain available.

Related decision: `UD-021`.

### 9.6 Shannon entropy

\[
H
=
-\sum_i p_i\log p_i
\]

| Property | Value |
|---|---|
| Canonical term | `shannon_entropy` |
| Unit | nats for natural logarithm, bits for base 2 |
| v0.1 status | optional or deferred until explicitly approved |

Any Shannon output must declare the logarithm base.

Shannon entropy must not become a universal system-entropy score.

---

## 10. Tail vocabulary

### 10.1 Tail

| Field | Definition |
|---|---|
| Canonical term | `tail` |
| Definition | Low-frequency subset of observed support under a declared threshold rule |
| Unit | set of states |

Tail membership depends on:

- representation,
- observed frequencies,
- threshold rule,
- weighting mode.

### 10.2 Tail rule

| Field | Definition |
|---|---|
| Canonical field | `tail_rule` |
| Type | enum or structured rule |
| Unit | configuration |

Recommended v0.1 rule types:

- `singleton_count`
- `count_at_or_below`
- `frequency_at_or_below`
- `bottom_frequency_quantile`
- user-declared state list

### 10.3 Hero tail default

Recommended hero configuration:

```text
tail_rule: singleton_count
tail_count_threshold: 1
```

A state belongs to the hero tail when its observed count equals 1.

Status: `APPROVED DECISION UD-012`.

### 10.4 Tail size

\[
K_{\text{tail}}
=
|T|
\]

| Property | Value |
|---|---|
| Canonical field | `tail_support_size` |
| Unit | states |

### 10.5 Tail record share

\[
P_{\text{tail records}}
=
\sum_{i\in T}p_i
\]

| Property | Value |
|---|---|
| Canonical field | `tail_record_share` |
| Unit | ratio |
| Range | \([0,1]\) |

### 10.6 Rarity rank

| Field | Definition |
|---|---|
| Canonical field | `rarity_rank` |
| Definition | Deterministic rank of states from lowest frequency to highest frequency |
| Unit | ordinal rank |
| Evidence class | derived metric |

Tie-breaking must use the approved deterministic rule.

### 10.7 One-step extinction probability

For a state with current frequency \(p_i\) and a closed multinomial resample of size \(n\):

\[
P_{\text{extinct,next}}(i)
=
(1-p_i)^n
\]

| Property | Value |
|---|---|
| Canonical field | `one_step_extinction_probability` |
| Unit | probability |
| Range | \([0,1]\) |
| Evidence class | simulation |
| Status | `APPROVED DECISION UD-013` |

Required assumptions:

- categorical states,
- multinomial sampling,
- sample size \(n\),
- one-step horizon,
- declared representation,
- no external reopening unless modeled.

This value is a scenario result.

### 10.8 Tail fragility ranking

| Field | Definition |
|---|---|
| Canonical field | `tail_fragility_ranking` |
| Definition | Ordered states based on approved rarity or scenario extinction measure |
| Unit | ordered list |
| Evidence class | derived metric or simulation, field-specific |

The report must state which measure determines the ranking.

### 10.9 Tail fragility signal

| Field | Definition |
|---|---|
| Canonical field | `tail_fragility_signal` |
| Definition | Narrative or categorical warning derived from tail rarity and declared scenario assumptions |
| Unit | category or message |
| Evidence class | proxy signal |

No universal threshold is defined.

### 10.10 Tail extinction across versions

\[
E_{\text{tail},a\rightarrow b}
=
T_a \cap (S_a\setminus S_b)
\]

| Property | Value |
|---|---|
| Canonical field | `tail_extinct_states` |
| Unit | set of states |
| Evidence class | derived metric |

---

## 11. Source-share vocabulary

### 11.1 Source-type count

For source class \(c\):

\[
N_c
=
|\{r:\operatorname{source\_type}(r)=c\}|
\]

| Property | Value |
|---|---|
| Canonical field | `source_type_count` |
| Unit | records |

Records without matched provenance must be represented separately from declared `unknown` where the report schema supports that distinction.

### 11.2 Source-type share

\[
S_c
=
\frac{N_c}{N}
\]

| Property | Value |
|---|---|
| Canonical field | `source_type_share` |
| Unit | ratio |
| Range | \([0,1]\) |
| Evidence class | derived metric |

Recommended named fields:

- `human_share`
- `synthetic_share`
- `mixed_share`
- `sensor_share`
- `unknown_share`
- `missing_provenance_share`

The sum equals 1 only when the category partition includes all analyzed records.

### 11.3 Unknown source share

`unknown_share` includes records whose matched provenance row explicitly declares `source_type=unknown`.

It does not automatically include records with missing provenance rows.

### 11.4 Missing provenance share

\[
S_{\text{missing provenance}}
=
1-P_{\text{row}}
\]

| Property | Value |
|---|---|
| Canonical field | `missing_provenance_share` |
| Unit | ratio |

### 11.5 Effective source diversity

| Field | Definition |
|---|---|
| Canonical term | `effective_source_diversity` |
| v0.1 status | deferred |
| Reason | no approved dependence model across sources, generators, ownership, and ancestry |

Do not substitute distinct generator count or source-type count for this term.

---

## 12. Finite-resampling model

### 12.1 Current distribution

\[
p_t
=
(p_{t,1},\ldots,p_{t,K})
\]

Requirements:

\[
p_{t,i}\geq0
\]

\[
\sum_i p_{t,i}=1
\]

| Property | Value |
|---|---|
| Canonical field | `state_distribution` |
| Unit | probability vector |

### 12.2 Resample size

| Field | Definition |
|---|---|
| Canonical field | `resample_size` |
| Symbol | \(n\) |
| Type | positive integer |
| Unit | sampled records |

### 12.3 Closed resampling operator

\[
X_t\mid p_t
\sim
\operatorname{Multinomial}(n,p_t)
\]

\[
p_{t+1}
=
\frac{X_t}{n}
=
R_n(p_t)
\]

| Property | Value |
|---|---|
| Canonical term | `closed_resampling` |
| Unit | stochastic transition |
| Evidence class | simulation |

Assumptions:

- finite categorical support,
- multinomial sampling,
- no mutation,
- no migration,
- no independent external input,
- no hidden state-restoration process.

### 12.4 Conditional unbiasedness

\[
\mathbb{E}[p_{t+1}\mid p_t]
=
p_t
\]

This means the next generation is conditionally unbiased relative to the current distribution.

It does not guarantee fidelity to an earlier external distribution.

### 12.5 Expected diversity contraction

\[
\mathbb{E}[D_{t+1}\mid p_t]
=
\left(1-\frac{1}{n}\right)D_t
\]

For fixed \(n\):

\[
\mathbb{E}[D_t]
=
\left(1-\frac{1}{n}\right)^tD_0
\]

| Property | Value |
|---|---|
| Canonical field | `expected_gini_simpson_diversity` |
| Unit | dimensionless |
| Evidence class | derived scenario quantity |

This formula applies to the declared finite closed-resampling model.

### 12.6 Absorbing state loss

If:

\[
p_{t,i}=0
\]

then under the closed resampling operator:

\[
p_{t+k,i}=0
\quad
\text{for all }k>0
\]

This property applies within the closed model.

Production systems with fresh data, mutation, retrieval, or other reopening channels can restore a missing state.

### 12.7 Simulation horizon

| Field | Definition |
|---|---|
| Canonical field | `simulation_horizon` |
| Type | non-negative integer |
| Unit | simulated recursive steps |

### 12.8 Random seed

| Field | Definition |
|---|---|
| Canonical field | `random_seed` |
| Type | integer |
| Unit | seed |
| Requirement | recorded for stochastic public output |

### 12.9 Simulation replicate count

| Field | Definition |
|---|---|
| Canonical field | `simulation_replicates` |
| Type | positive integer |
| Unit | replicate runs |

Single-path and replicate-summary outputs must remain distinct.

### 12.10 Extinction event

| Field | Definition |
|---|---|
| Canonical term | `simulated_extinction_event` |
| Definition | A state changes from positive simulated frequency to zero frequency |
| Unit | event |
| Evidence class | simulation |

---

## 13. External reference and reopening

### 13.1 External reference distribution

\[
q
=
(q_1,\ldots,q_K)
\]

| Field | Definition |
|---|---|
| Canonical field | `external_reference_distribution` |
| Unit | probability vector |
| Source | user-supplied or approved external baseline |

The toolkit must not silently select the first observed version as external truth.

### 13.2 External-reference squared loss

\[
L_t
=
\lVert p_t-q\rVert_2^2
=
\sum_i(p_{t,i}-q_i)^2
\]

| Property | Value |
|---|---|
| Canonical field | `external_reference_l2_squared` |
| Unit | dimensionless |
| Range | \([0,2]\) for probability vectors |
| Evidence class | simulation or derived scenario metric |

Under the closed multinomial model:

\[
\mathbb{E}[L_{t+1}\mid p_t]
=
L_t+\frac{D_t}{n}
\]

### 13.3 External input distribution

\[
r_t
=
(r_{t,1},\ldots,r_{t,K})
\]

| Field | Definition |
|---|---|
| Canonical field | `external_input_distribution` |
| Unit | probability vector |
| Meaning | Distribution entering from outside the modeled internal recursion |

### 13.4 Reopening weight

| Field | Definition |
|---|---|
| Canonical field | `reopening_weight` |
| Symbol | \(\lambda\) |
| Type | finite number |
| Unit | ratio |
| Range | \([0,1]\) |

Interpretation:

- \(\lambda=0\): fully closed scenario,
- \(0<\lambda<1\): mixed internal and external input,
- \(\lambda=1\): next source distribution is entirely external before resampling.

### 13.5 Reopened resampling model

\[
p_{t+1}
=
R_n\left((1-\lambda)p_t+\lambda r_t\right)
\]

| Property | Value |
|---|---|
| Canonical term | `reopened_resampling` |
| Evidence class | simulation |
| Public status | experimental |

A larger reopening weight does not guarantee higher integrity when the external input distribution is poor, contaminated, irrelevant, or not genuinely external.

### 13.6 State re-entry

A state re-enters when:

- its internal frequency is zero,
- its mixed pre-resampling probability is positive through external input,
- it appears with positive frequency after resampling.

| Property | Value |
|---|---|
| Canonical field | `state_reentry_event` |
| Unit | event |
| Evidence class | simulation |

---

## 14. Longitudinal vocabulary

### 14.1 Earlier and later version

| Term | Definition |
|---|---|
| `earlier_version` | version with lower approved ordinal position |
| `later_version` | version with higher approved ordinal position |

### 14.2 Version delta

For metric \(M\):

\[
\Delta M
=
M_{\text{later}}-M_{\text{earlier}}
\]

| Property | Value |
|---|---|
| Canonical term | `metric_delta` |
| Unit | unit of \(M\) |
| Sign convention | later minus earlier |

### 14.3 Relative change

When \(M_{\text{earlier}}\neq0\):

\[
R_M
=
\frac{M_{\text{later}}-M_{\text{earlier}}}
{|M_{\text{earlier}}|}
\]

| Property | Value |
|---|---|
| Canonical term | `relative_change` |
| Unit | ratio |

If the earlier value is zero, relative change is unavailable.

### 14.4 Longitudinal comparison

| Field | Definition |
|---|---|
| Canonical term | `longitudinal_comparison` |
| Definition | Comparison between two or more explicitly ordered compatible dataset versions |
| Unit | comparison |

### 14.5 Dataset longitudinal capability

| Field | Definition |
|---|---|
| Canonical capability | `dataset_longitudinal` |
| Minimum evidence | two ordered representation-compatible dataset versions |

### 14.6 Model longitudinal capability

| Field | Definition |
|---|---|
| Canonical capability | `model_longitudinal` |
| Minimum evidence | approved model-performance or behavior evidence across versions |

Dataset-version evidence alone does not authorize a model-performance conclusion.

---

## 15. Observability vocabulary

### 15.1 Observability

| Field | Definition |
|---|---|
| Canonical term | `observability` |
| Definition | The set of conclusions supported by the available inputs and validated metadata |
| Unit | level plus capability status |

Observability measures available evidence.

It does not measure product quality or system health.

### 15.2 Maximum observability level

| Level | Minimum evidence | Core permitted output |
|---|---|---|
| 0 | readable file and minimal schema | ingest and auditability gaps |
| 1 | analyzable content or declared representation | duplicates, support, diversity, tail diagnostics |
| 2 | partial or complete provenance | coverage, source shares, direct closure bounds |
| 3 | resolvable cycle-free lineage | ancestry and lineage bounds |
| 4 | ordered compatible dataset versions | longitudinal dataset comparison |
| 5 | approved scenario or controlled-intervention evidence | experimental comparison |

| Property | Value |
|---|---|
| Canonical field | `maximum_observability_level` |
| Type | integer |
| Range | 0 through 5 |

### 15.3 Capability

| Field | Definition |
|---|---|
| Canonical term | `capability` |
| Definition | One independently evaluated analysis family |
| Unit | capability |

Required initial capability keys:

- `ingestion`
- `content_diagnostics`
- `provenance`
- `lineage`
- `dataset_longitudinal`
- `model_longitudinal`
- `intervention_simulation`

### 15.4 Capability status

Allowed values:

| Value | Meaning |
|---|---|
| `available` | Required evidence is present and valid |
| `partial` | Some valid output is possible, with material coverage or completeness limits |
| `unavailable` | Required evidence is absent or invalid |
| `experimental` | Output is available only under an explicitly experimental method or scenario |

A maximum level must be accompanied by the capability matrix.

Related decisions: `UD-003`, `UD-004`.

---

## 16. Evidence-class vocabulary

### 16.1 Observed fact

| Field | Definition |
|---|---|
| Canonical value | `observed_fact` |
| Definition | Directly present in supplied data or exactly counted from validated inputs |

Examples:

- row count,
- declared source type,
- matching provenance row count,
- exact duplicate group,
- detected graph cycle.

### 16.2 Derived metric

| Field | Definition |
|---|---|
| Canonical value | `derived_metric` |
| Definition | Deterministic function of observed inputs under a declared rule |

Examples:

- support size,
- Gini-Simpson diversity,
- source share,
- closure bounds,
- ancestry concentration,
- support delta.

### 16.3 Proxy signal

| Field | Definition |
|---|---|
| Canonical value | `proxy_signal` |
| Definition | Heuristic warning or interpretation that does not directly observe the underlying functional condition |

Examples:

- tail fragility signal,
- correlated-error exposure warning,
- support-contraction alert.

### 16.4 Simulation

| Field | Definition |
|---|---|
| Canonical value | `simulation` |
| Definition | Result generated under explicit mathematical or stochastic assumptions |

Examples:

- one-step extinction probability,
- simulated diversity trajectory,
- external reopening scenario.

### 16.5 Unavailable conclusion

| Field | Definition |
|---|---|
| Canonical value | `unavailable_conclusion` |
| Definition | A requested or relevant conclusion blocked by missing evidence, unsupported inference, or v0.1 scope |

Examples:

- universal collapse prediction,
- proven production failure,
- causal ancestor effect,
- universal integrity score.

### 16.6 Evidence-class exclusivity

Each public result field must have one primary evidence class.

A report may link related fields across classes.

Example:

- rarity rank: derived metric,
- one-step extinction probability: simulation,
- tail warning: proxy signal.

---

## 17. Warning, error, and validation vocabulary

### 17.1 Warning

| Field | Definition |
|---|---|
| Canonical term | `warning` |
| Definition | Nonfatal condition that reduces completeness, confidence, or available capability |
| Run outcome | may continue |

### 17.2 Error

| Field | Definition |
|---|---|
| Canonical term | `error` |
| Definition | Condition preventing a requested operation, metric family, or valid run |
| Run outcome | affected operation stops |

### 17.3 Fatal run error

| Field | Definition |
|---|---|
| Canonical term | `fatal_error` |
| Definition | Error preventing creation of a valid audit result |
| Run outcome | nonzero exit status |

### 17.4 Validation message

A validation message contains:

- code,
- severity,
- file,
- record key or row when available,
- field,
- concise explanation,
- remediation hint where appropriate.

Normal validation messages must not include raw content.

### 17.5 Strict mode

| Field | Definition |
|---|---|
| Canonical field | `strict_mode` |
| Type | boolean |
| Definition | Configuration that promotes selected warnings to errors |
| Default | false, pending final validation specification |

Strict mode must not alter formulas.

---

## 18. Integrity, quality, stability, and entropy boundaries

### 18.1 Integrity

| Field | Definition |
|---|---|
| Canonical theory term | `integrity` |
| Definition | Fidelity to the external distribution, adaptive landscape, source reality, or continuing obligation the system must track |
| Universal v0.1 unit | none |
| Public numeric status | deferred |

A domain-specific external-reference loss may measure one limited form of fidelity.

It must not be labeled universal integrity.

### 18.2 Diversity in the compact quality relation

The theory relation:

\[
Q=I\times D
\]

uses diversity as a structural dependency.

v0.1 operationalizes Gini-Simpson diversity under declared representations.

v0.1 does not operationalize universal \(Q\) or universal \(I\).

### 18.3 Presence

| Field | Definition |
|---|---|
| Canonical theory term | `presence` |
| Definition | Maintained channel through which reality-bearing external input can enter the recursive process |
| Universal v0.1 unit | none |
| Scenario proxy | reopening weight \(\lambda\) under an explicit model |
| Public numeric status | deferred outside scenario context |

### 18.4 Stability

The theory relation:

\[
S=P\times I
\]

remains a structural dependency.

v0.1 does not calculate a universal stability score.

### 18.5 Quality

| Field | Definition |
|---|---|
| Canonical theory term | `quality` |
| Definition | Functional adequacy produced through the relation of integrity and diversity in the theory |
| Universal v0.1 unit | none |
| Public numeric status | deferred |

### 18.6 Entropy

| Field | Definition |
|---|---|
| Canonical theory role | structural boundary, distributional quantity, or descriptive signature under declared constraints |
| Universal v0.1 metric | none |

A specific entropy metric must name:

- the distribution,
- formula,
- logarithm base where applicable,
- unit,
- interpretation.

The toolkit must not output a universal entropy score.

### 18.7 Collapse

| Field | Definition |
|---|---|
| Canonical product status | restricted term |
| Metric status | forbidden |
| Score status | forbidden |
| Universal prediction status | unavailable |

Permitted contexts:

- cited theory,
- cited research phenomenon,
- product motivation,
- unavailable conclusion.

Preferred public diagnostic terms:

- support contraction,
- tail extinction,
- closure exposure,
- provenance incompleteness,
- ancestry concentration.

### 18.8 Functional failure

| Field | Definition |
|---|---|
| Canonical term | `functional_failure` |
| Definition | Failure to meet a domain-specific external performance or fidelity obligation |
| v0.1 evidence requirement | approved outcome evidence |
| Default status | unavailable conclusion |

Low diversity alone does not establish functional failure.

### 18.9 Correlated error

| Field | Definition |
|---|---|
| Canonical theory term | `correlated_error` |
| Definition | Error dependence created when a narrowed internal state or shared ancestry shapes future generation, validation, or selection |
| Direct v0.1 measurement | unavailable without error labels or outcomes |
| Approved proxy | shared-ancestry concentration signal |

Ancestry concentration must not be reported as proven shared semantic error.

---

## 19. Weighting conventions

### 19.1 Record weight

| Field | Definition |
|---|---|
| Canonical field | `weight` |
| Type | finite non-negative number |
| Unit | user-declared sampling or importance mass |
| Default use | ignored unless weighted analysis is explicitly enabled |

### 19.2 Invalid weights

Invalid conditions:

- negative weight,
- nonfinite weight,
- all weights equal zero,
- missing weights under a configuration requiring complete weights.

### 19.3 Unweighted default

Default counts assign every analyzed record weight 1.

### 19.4 Weighted result naming

Weighted outputs must include `weighted_` in the canonical field name or a structured `weighting` descriptor.

Weighted and unweighted outputs must not overwrite one another.

---

## 20. Hashing and normalization units

### 20.1 File hash

| Field | Definition |
|---|---|
| Canonical field | `file_hash` |
| Recommended algorithm | SHA-256 |
| Type | lowercase hexadecimal string |
| Unit | digest |

### 20.2 Content hash

| Field | Definition |
|---|---|
| Canonical field | `content_hash` |
| Recommended algorithm | SHA-256 |
| Input | normalized content bytes |
| Unit | digest |

A content hash supports deterministic equality checks.

It does not prove authorship, provenance, or semantic identity.

### 20.3 ID hashing for redaction

| Field | Definition |
|---|---|
| Canonical term | `redacted_record_id` |
| Definition | Deterministic hash or token replacing a record ID in a sharing report |
| Unit | identifier |

The hashing method and salt policy must be declared in the privacy specification.

---

## 21. Performance and execution units

### 21.1 Runtime

| Field | Definition |
|---|---|
| Canonical field | `duration_seconds` |
| Type | non-negative number |
| Unit | seconds |

### 21.2 Rows processed

| Field | Definition |
|---|---|
| Canonical field | `rows_processed` |
| Type | non-negative integer |
| Unit | rows |

### 21.3 Throughput

\[
\text{throughput}
=
\frac{\text{rows processed}}{\text{duration seconds}}
\]

| Property | Value |
|---|---|
| Canonical field | `rows_per_second` |
| Unit | rows per second |
| v0.1 status | optional diagnostic |

### 21.4 Network calls

| Field | Definition |
|---|---|
| Canonical field | `network_call_count` |
| Type | non-negative integer |
| Unit | calls |
| Required hero value | 0 |

---

## 22. Canonical enum registry

### 22.1 Source type

```text
human
synthetic
mixed
sensor
unknown
```

### 22.2 Provenance confidence

```text
confirmed
log_derived
estimated
unknown
```

### 22.3 External grounding

```text
yes
no
unknown
```

### 22.4 Transformation

```text
generate
rewrite
summarize
translate
filter
label
carryover
other
```

### 22.5 Capability status

```text
available
partial
unavailable
experimental
```

### 22.6 Evidence class

```text
observed_fact
derived_metric
proxy_signal
simulation
unavailable_conclusion
```

### 22.7 Severity

```text
info
warning
error
fatal
```

### 22.8 Weighting mode

```text
unweighted
weighted
```

### 22.9 Representation source

Recommended values:

```text
config
topic_field
label_field
embedding_clusters
content_hash
```

---

## 23. Hero example units and expected meanings

### 23.1 Representation

```text
representation_name: topic
representation_source: topic_field
```

### 23.2 Support

```text
v1_support_size: 8 states
v2_support_size: 5 states
support_delta: -3 states
```

### 23.3 Extinct states

```text
lizard
turtle
battery
```

Meaning:

These topic states appear in v1 and are absent from v2 under the `topic` representation.

### 23.4 Provenance

```text
v2_provenance_row_coverage: 1.0
```

Meaning:

Every v2 record has one valid matching provenance row.

### 23.5 Source shares

```text
v2_human_share: 0.5
v2_synthetic_share: 0.5
v2_unknown_share: 0.0
```

Unit:

```text
ratio
```

### 23.6 External roots

```text
distinct_external_root_count: 5 roots
```

### 23.7 Top shared root

```text
root: v1::v1_01
ancestor_incidence_count: 3 records
ancestor_incidence_share: 0.375
```

The share uses all eight analyzed v2 records as denominator.

### 23.8 Observability

```text
maximum_observability_level: 4
```

Required capability interpretation:

```text
ingestion: available
content_diagnostics: available
provenance: available
lineage: available
dataset_longitudinal: available
model_longitudinal: unavailable
intervention_simulation: unavailable
```

### 23.9 Unavailable hero conclusions

The hero inputs do not support:

- model-performance decline,
- causal effect of the top ancestor,
- universal integrity loss,
- universal collapse prediction.

---

## 24. Forbidden ambiguities

The following usages are prohibited.

### 24.1 Generation ambiguity

`generation` must not mean:

- epoch,
- model release,
- dataset version,
- generic graph depth.

### 24.2 Unknown ambiguity

`unknown` must not mean:

- human-curated,
- safe,
- open,
- synthetic,
- missing,
- zero.

### 24.3 Mixed ambiguity

`mixed` must not imply:

- external grounding,
- a 50-50 split,
- independent ancestry,
- human review.

### 24.4 Review ambiguity

`human_reviewed=true` must not imply:

- factual correctness,
- external grounding,
- human origin,
- independent source.

### 24.5 Support ambiguity

`support` must name its representation.

### 24.6 Diversity ambiguity

`diversity` must name its metric and representation.

### 24.7 Tail ambiguity

`tail` must name its threshold rule.

### 24.8 Extinction ambiguity

Observed extinction across versions must not be described as permanent extinction from the full process.

### 24.9 Ancestry ambiguity

Ancestry concentration must not be interpreted as causal contribution.

### 24.10 Entropy ambiguity

A distributional entropy value must not become a universal system-health score.

### 24.11 Collapse ambiguity

`collapse` must not be a v0.1 metric name.

### 24.12 Root ambiguity

A lineage root must not automatically become an external root.

### 24.13 Source-count ambiguity

Distinct generator count must not be called effective source diversity.

### 24.14 Level ambiguity

A maximum observability level must not imply every capability is available.

### 24.15 Probability ambiguity

A scenario extinction probability must not be presented as a calibrated production forecast.

---

## 25. Deferred definitions

The following terms remain theory-relevant but lack approved v0.1 operational definitions.

| Term | v0.1 status | Reopening requirement |
|---|---|---|
| universal integrity score | deferred | domain-specific fidelity measure and validation |
| universal presence score | deferred | independent-input and relevance model |
| universal quality score | deferred | operational integrity and diversity relation |
| universal stability score | deferred | operational presence and integrity |
| universal entropy score | forbidden | no planned universal form |
| effective source diversity | deferred | source-dependence model |
| correlated semantic error rate | deferred | labeled outcome evidence |
| amplification threshold | deferred | transfer matrix and domain schema |
| hidden-decay indicator | deferred | calibrated proxy design |
| causal ancestor contribution | deferred | weighted causal lineage model |
| empirical intervention effect | deferred | treatment, control, outcome, and identification schema |

Deferred terms must not power public v0.1 results.

---

## 26. Formula registry

| Formula ID | Quantity | Formula | Unit | Evidence class |
|---|---|---|---|---|
| F-001 | state frequency | \(p_i=n_i/N\) | ratio | derived metric |
| F-002 | support size | \(K=|\{i:p_i>0\}|\) | states | derived metric |
| F-003 | Gini-Simpson diversity | \(D=1-\sum_i p_i^2\) | dimensionless | derived metric |
| F-004 | Simpson concentration | \(\sum_i p_i^2\) | dimensionless | derived metric |
| F-005 | support delta | \(K_b-K_a\) | states | derived metric |
| F-006 | support retention | \(|S_a\cap S_b|/|S_a|\) | ratio | derived metric |
| F-007 | source share | \(N_c/N\) | ratio | derived metric |
| F-008 | provenance row coverage | \(N_{\text{prov row}}/N\) | ratio | observed fact |
| F-009 | direct closure lower bound | \(N_C/N\) | ratio | derived metric |
| F-010 | direct closure upper bound | \((N_C+N_U)/N\) | ratio | derived metric |
| F-011 | ancestor incidence share | \(I_a/N\) | ratio | derived metric |
| F-012 | ancestry HHI | \(\sum_a w_a^2\) | dimensionless | derived metric |
| F-013 | effective external roots | \(1/HHI_{\text{ancestry}}\) | effective roots | derived metric |
| F-014 | one-step extinction | \((1-p_i)^n\) | probability | simulation |
| F-015 | expected diversity contraction | \((1-1/n)D_t\) | dimensionless | derived scenario quantity |
| F-016 | external-reference loss | \(\|p_t-q\|_2^2\) | dimensionless | simulation or derived scenario metric |
| F-017 | reopened source mixture | \((1-\lambda)p_t+\lambda r_t\) | probability vector | simulation |
| F-018 | metric delta | \(M_b-M_a\) | metric-specific | derived metric |
| F-019 | relative change | \((M_b-M_a)/|M_a|\) | ratio | derived metric |

---

## 27. Decision dependencies

| Decision | Definitions affected |
|---|---|
| `UD-003` | maximum hero observability level |
| `UD-004` | capability matrix |
| `UD-005` | generation and lineage depth |
| `UD-006` | composite parent references |
| `UD-007` | version order |
| `UD-008` | provenance coverage |
| `UD-009` | external grounding authority |
| `UD-010` | closure exposure bounds |
| `UD-011` | representation selection |
| `UD-012` | tail default |
| `UD-013` | extinction probability evidence class |
| `UD-014` | ancestry HHI and effective roots |
| `UD-015` | missing and ambiguous parent behavior |
| `UD-018` | cycle classification |
| `UD-021` | weighted analysis |
| `UD-033` | hero values |
| `UD-035` | collapse language |

Until the relevant decisions are approved, affected definitions remain the recommended baseline.

---

## 28. Approval checklist

The Theory Owner and reviewers should confirm:

- [ ] all canonical entities have stable names,
- [ ] identifier units and uniqueness scopes are explicit,
- [ ] source type and grounding remain separate,
- [ ] provenance coverage uses explicit denominators,
- [ ] generation and lineage depth remain separate,
- [ ] parent, ancestor, root, and external root remain distinct,
- [ ] support always names a representation,
- [ ] diversity always names a metric,
- [ ] tail always names a threshold,
- [ ] extinction probability remains a scenario result,
- [ ] direct and lineage closure bounds remain separate,
- [ ] ancestry incidence and concentration use explicit denominators,
- [ ] weighted and unweighted outputs remain separate,
- [ ] unknown, unavailable, and zero remain distinct,
- [ ] entropy does not become a universal causal or scoring variable,
- [ ] compact theory formulas remain non-operational,
- [ ] deferred terms do not power public outputs.

### Theory Owner decision

- [ ] Approve definitions baseline
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

- [ ] Formulas are correctly transcribed.
- [ ] Denominators and ranges are explicit.
- [ ] Scenario assumptions are visible.
- [ ] No universal score is smuggled through a local metric.

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

- [ ] Types can be represented without hidden coercion.
- [ ] Missingness states can be serialized safely.
- [ ] Metric names are implementable.
- [ ] Required validation rules are testable.

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

## 29. Change-control rule

After approval:

1. a public term must not change meaning without a recorded decision,
2. a denominator change requires a new field name or versioned schema,
3. a unit change requires a new field name or explicit schema version,
4. a formula change requires updated Theory Map and Trace IDs,
5. a new metric requires definition, unit, evidence class, observability requirement, test, and report field,
6. a deferred term may enter v0.1 only through approved change control,
7. deprecated terms remain documented until all public outputs and fixtures migrate,
8. code comments and user documentation must link to the canonical definition rather than restating a divergent version.
