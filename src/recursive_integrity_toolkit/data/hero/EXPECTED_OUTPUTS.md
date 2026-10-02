# Hero Example Expected Outputs

## Status

These values are the approved reference expectations for the canonical hero fixture.

They are copied from the approved Phase 0 specifications. Phase 1 Step 6 does not calculate or validate the analytical values.

## Input identity

```text
records_v1.csv rows: 8
records_v2.csv rows: 8
provenance.csv rows: 16
version order: v1, v2
representation: topic
representation version: hero-topic-v1
maximum observability level: 4
```

## Capability matrix

```text
ingestion: available
content_diagnostics: available
provenance: available
lineage: available
dataset_longitudinal: available
model_longitudinal: unavailable
intervention_simulation: unavailable
```

## Approved support and diversity expectations

```text
v1 support size: 8
v2 support size: 5
support delta: -3
support retention: 0.625
v1 Gini-Simpson diversity: 0.875
v2 Gini-Simpson diversity: 0.75
diversity delta: -0.125
```

## Approved extinct observed states

Deterministic order:

```text
battery
lizard
turtle
```

## Approved v2 provenance expectations

```text
provenance row coverage: 1.0
required-field coverage: 1.0
grounding-field coverage: 1.0
human share: 0.5
synthetic share: 0.5
mixed share: 0.0
sensor share: 0.0
unknown share: 0.0
missing provenance share: 0.0
```

## Approved closure expectations

```text
direct closure lower bound: 0.5
direct closure upper bound: 0.5
direct interval width: 0.0
lineage closure lower bound: 0.0
lineage closure upper bound: 0.0
lineage interval width: 0.0
```

## Approved lineage expectations

```text
cycle detected: false
declared parent edges for v2: 8
resolved parent edges for v2: 8
unresolved parent edges for v2: 0
distinct external roots supporting v2: 5
top shared root: v1::v1_01
top shared-root incidence: 3
top shared-root incidence share: 0.375
ancestry HHI: 0.25
effective external-root count: 4.0
```

Ancestry HHI is a topological toolkit operationalization. It is not a causal contribution score.

## Approved proxy signals

```text
support_contraction: present
shared_ancestry_dependence: present
```

No universal risk level is approved.

## Simulations

```text
none in the default hero audit
```

## Required unavailable conclusions

```text
model_performance_decline
causal_ancestor_effect
universal_integrity
universal_collapse_prediction
```

## Required interpretive boundary

The fixture supports a topic-representation comparison, declared provenance coverage, and declared lineage structure.

It does not establish model-performance decline, causal effect of any ancestor, universal integrity loss, or universal collapse.
