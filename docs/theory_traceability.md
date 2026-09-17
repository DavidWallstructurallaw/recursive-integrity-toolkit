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
