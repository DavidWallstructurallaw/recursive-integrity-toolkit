# Three-version example expected outputs

These expectations were independently authored in Phase 6A Step 1 and use
literal row counts, exact fractions and set operations. They are copied from
the `observed_three_version` acceptance case; they are not generated from a
toolkit report. Report JSON uses the corresponding finite decimal values.

## Inputs and scope

There are 4 records in v1, 4 in v2 and 3 in v3. All are representation eligible.
Chronology is explicitly v1, v2, v3. The common representation is topic,
version `topics-v1`, field `topic`, with missing values excluded. States retain
their literal category meanings. No lineage context is supplied.

The v2 record r4 intentionally has no provenance row. Its missing evidence
remains part of the complete v2 denominator. The v3 record r3 has an explicit
unknown source and unknown grounding, which remain distinct from a missing row.

## Snapshot distributions

| Snapshot | State counts | Records | Support | Gini-Simpson diversity |
|---|---|---:|---:|---:|
| v1 | A: 2, B: 1, C: 1 | 4 | 3 | 5/8 |
| v2 | A: 2, D: 2 | 4 | 2 | 1/2 |
| v3 | A: 1, B: 1, D: 1 | 3 | 3 | 2/3 |

## Observed pair changes

All deltas are later minus earlier. Default execution includes the two adjacent
rows. The last row is additionally requested with `--baseline first`.

| Pair | Record delta | Support delta | Diversity delta | Missing states | Added states | Retained states | Support retention |
|---|---:|---:|---:|---|---|---|---:|
| v1 -> v2 | 0 | -1 | -1/8 | B, C | D | A | 1/3 |
| v2 -> v3 | -1 | 1 | 1/6 | none | B | A, D | 1 |
| v1 -> v3 | -1 | 0 | 1/24 | C | D | A, B | 2/3 |

With explicit `--tail-rule singleton_count`, earlier-selected tail states
missing later are B, C for v1 -> v2; none for v2 -> v3; C for v1 -> v3.
Without that flag, tail execution is `not_requested` and tail values are null.
An observed missing state only concerns these supplied snapshots.

## Provenance and direct closure

Source shares and coverage use every record in that snapshot as denominator.
Mixed and sensor counts/shares are zero throughout. Confidence categories remain
separate declared evidence; they do not weight records or source shares.

| Snapshot | Human share | Synthetic share | Unknown share | Missing provenance share | Row coverage | Required-field coverage | Grounding-field coverage |
|---|---:|---:|---:|---:|---:|---:|---:|
| v1 | 1 | 0 | 0 | 0 | 1 | 1 | 1 |
| v2 | 1/2 | 1/4 | 0 | 1/4 | 3/4 | 3/4 | 3/4 |
| v3 | 1/3 | 1/3 | 1/3 | 0 | 1 | 1 | 2/3 |

| Snapshot | Direct closure lower | Direct closure upper | Interval width |
|---|---:|---:|---:|
| v1 | 0 | 0 | 0 |
| v2 | 1/4 | 1/2 | 1/4 |
| v3 | 1/3 | 2/3 | 1/3 |

| Pair | Row/required coverage delta | Grounding coverage delta | Human share delta | Synthetic share delta | Unknown share delta | Missing share delta | Lower delta | Upper delta | Width delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| v1 -> v2 | -1/4 | -1/4 | -1/2 | 1/4 | 0 | 1/4 | 1/4 | 1/2 | 1/4 |
| v2 -> v3 | 1/4 | -1/12 | -1/6 | 1/12 | 1/3 | -1/4 | 1/12 | 1/6 | 1/12 |
| v1 -> v3 | 0 | -1/3 | -2/3 | 1/3 | 1/3 | 0 | 1/3 | 2/3 | 1/3 |

The missing row must produce `W_PROVENANCE_MISSING_ROW`; it cannot be filled with
a synthetic, unknown or externally grounded declaration. Direct closure bounds
describe supplied evidence, with explicit unresolved mass.

## Execution and interpretation

The default requests distribution, provenance and direct closure families.
Tail and lineage remain `not_requested` unless explicitly enabled. A finite
scalar can coexist with partial evidence; retain each family's status and
endpoint denominators when interpreting a change.

Lineage can be requested with `--lineage`. It uses the common supplied
retrospective graph and all selected target populations. This example declares
no parent references; the existing Hero fixture demonstrates inherited
ancestry and shared roots with its independent lineage oracle.

No simulation, fitted trajectory, risk score, performance decline, causal
ancestor effect or universal collapse conclusion is part of this example.
