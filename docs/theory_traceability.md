# Theory Traceability

Status: Phase 1 scaffold.

The controlling maps are:

- `THEORY_SOURCE_MAP.md`
- `THEORY_TO_CODE_TRACEABILITY.md`

Every Python module identifies its Trace IDs or Product Rule IDs in the module docstring. Phase 1 does not implement the theory-derived formulas.


## Phase 3 Step 3 implemented trace

| Owner | Implemented basis | Authoritative definition | Evidence |
|---|---|---|---|
| PR-006 | exact_utf8_v1 decoded text bytes and SHA-256 | P3-D05; DEFINITIONS_AND_UNITS 6.10 and 20.2 | record-form identity only |
| PR-006 | duplicate_record_count, sum of group size minus one | DEFINITIONS_AND_UNITS 8.3; THEORY_TO_CODE_TRACEABILITY 17 | observed_fact, records |
| PR-006 | duplicate_group_count, groups of size greater than one | DEFINITIONS_AND_UNITS 8.4; THEORY_TO_CODE_TRACEABILITY 17 | observed_fact, groups |
| T1 supporting basis | immutable exact-content state assignments | PHASE_3_PLAN Step 3 | no support/diversity calculation |
| PR-016 supporting basis | canonical members and sorted digest groups | PHASE_3_PLAN 5.3 | deterministic ordering |

The PR-006 placeholder test keeps its original node ID but now checks the exact
implemented boundary. Tests cover known hashes, transformations that must remain
absent, exact grouping, source preservation, explicit payload selection, collisions,
private repr, unavailable versus zero, and rejection of premature capabilities.
No new F-number, theorem, entropy measure or semantic-support claim is introduced.
Report redaction remains a separate unimplemented PR-015/Phase 4 responsibility.

## Phase 3 Step 4 traceability

| Output | Owner and source | Computation |
|---|---|---|
| state_count | T1; Definitions 7.1 | Integer count of included assignments, or explicitly supplied aggregate |
| state_frequency | T1; F-001; Definitions 7.3 | State count divided by the included-record denominator |
| support_size | T1; F-002; Definitions 7.4-7.6 | Number of strictly positive frequency components |
| gini_simpson_diversity | T1; F-003; Definitions 9.2 | One minus sum of squared frequencies |
| simpson_concentration | T1; F-004; Definitions 9.3 | Sum of squared frequencies, without ancestry interpretation |
| Explicit weighted companions | T1; UD-021; Definitions 9.5 and 19 | State weight mass divided by total included weight; unweighted output preserved |

The supplied-vector entry point does not apply F-001 or fabricate record counts.
The vector's empirical relationship to its named scope remains caller-declared.
Calculated scalar fields use derived_metric evidence; supplied vectors and
integer record counts are labelled observed facts under their declared method.
Probability acceptance uses P3-D07 with no clipping or normalization.

Tests consume unchanged F001/F002 hand cases and frozen F003-A through F003-D.
Additional rational, weighting, zero-state, invalid-input and metamorphic cases
verify implementation behavior without extending the theory. Record-form
support remains representation-specific. Distributional concentration alone
never establishes functional failure or semantic completeness.
