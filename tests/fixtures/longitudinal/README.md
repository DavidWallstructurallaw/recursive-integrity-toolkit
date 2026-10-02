# Phase 6A independent acceptance fixtures

These fixtures freeze small, concrete inputs and independently authored expected
values for the approved Phase 6A plan. They do not constitute product output or
claim that multi-version orchestration exists in Step 1.

## Files and conventions

- `cases.json`: eleven canonical row sets, provenance manifests, chronology
  documents, explicit selected/context version identities, representation
  declarations and exact snapshot/pair expectations.
- `hero_expected.json`: additional per-version provenance and lineage expectations
  derived directly from the unchanged canonical Hero rows. The six Hero source
  and expectation files remain unchanged.
- `../../unit/test_longitudinal_fixture_inputs.py`: input validation and explicit
  calls to existing distribution, compatibility, tail, provenance, direct-bound
  and single-target lineage kernels, plus independent rational oracle checks.

Rational values are strings such as `"1/6"`, avoiding decimal approximation in the
oracle. Integers remain counts. Null means unavailable, with adjacent status or
reason fields. An empty state list is a valid observed empty set. Bounds always
use `[lower, upper, width]`; deltas always mean later minus earlier. Fixture field
names describe expected quantities and are not a second public report schema.

Records and manifests are embedded canonical JSON rows. Tests materialize them
as temporary JSONL files and a JSON order document, using each selected version's
own file. This keeps the exact source rows reviewable beside their expectations
without duplicating many tiny input files. Missing provenance is represented by
an absent manifest row, never by an invented unknown row. Explicit unknown,
confirmed, log-derived and estimated declarations remain separate.

## Cases

| Case | Protected distinction |
|---|---|
| `observed_three_version` | A/B/C to A/D to A/B/D; reappearance, unequal N, independent source and grounding declarations, missing rows, direct bounds |
| `lineage_complete` | Two loaded anchors; target-supported roots 2, 1, 2; HHI 1/2, 1, 1/2; target-specific populations |
| `lineage_partial` | Additional unresolved v3 record changes N and coverage while grounded-subset HHI stays 1/2 |
| `lineage_zero_grounded` | Known closed v3 population has zero roots and unavailable concentration |
| `lexical_order_context_unloaded` | v2 precedes v10; loaded context and order-only versions stay outside snapshot populations |
| `missing_order` | Single-version observations remain usable while the pair is blocked |
| `incompatible_middle` | Two invalid adjacent comparisons retain valid snapshots and a compatible first/last pair |
| `directed_many_to_one` | Directed literal coarsening, collision disclosure and original/harmonized values stay separate |
| `all_excluded_later` | Two real later records have no eligible representation; pair state sets stay null |
| `identified_empty_later` | Explicit empty Python scope retains N=0 and unavailable distribution; no empty CLI file or inferred version |
| `tied_timestamps_explicit_order` | Equivalent timezone timestamps require and retain an explicit tie-break |

The observed three-version example implements the plan's Section 5.2 arithmetic.
In v3 the explicit unknown-grounding record still has a complete provenance row.
Thus row/required coverage rises from 3/4 to 1, while known-grounding coverage
falls from 3/4 to 2/3. The grounding-coverage delta is -1/12. This deliberately
prevents a single generic "coverage" field from replacing the three measures.

Lineage fixtures use a disclosed common loaded evidence set. Each direct kernel
check loads a fresh ordinary invocation with that selected snapshot as primary
and the others in supported comparison/context roles. It never edits a validated
object or bypasses primary-target checks. These separate invocations verify
accepted single-target arithmetic only. Shared graph work and a validated series
target selector remain later Phase 6A work.

For the identified empty Python case, the field kernel receives an explicit
empty tuple for v2. The old pair kernel rejects that endpoint under the unchanged
actual-loaded-version chronology. Its future selected-scope compatibility helper
is required; the test does not insert v2 into `loaded_versions`. The future null
state-set and unavailable-distribution oracle is checked independently. The input
loader receives only actual nonempty files. The fixture makes no claim of current
CLI support for identifying an empty snapshot.

## Hero extension

The v1 Hero has eight human, confirmed, grounded, parentless records. Each record
is its own root: N=G=8, C=U=0, eight roots, HHI=1/8, effective roots=8, and both
direct and lineage bounds [0,0]. No declared parent references yields the accepted
reference-coverage value 1 with a zero reference denominator; this is distinct
from evidence of parent links.

The existing v2 has eight targets and five supported roots with incidences
3,2,1,1,1. Its HHI is 1/4, effective roots 4, direct bounds [1/2,1/2], and lineage
bounds [0,0]. Therefore v1 to v2 root count changes by -3, HHI by +1/8 and
effective roots by -4. Human/synthetic shares change by -1/2/+1/2. All three
provenance coverage deltas and both lineage coverage deltas are zero.

No simulation, report serializer, mutation framework, performance gate or
longitudinal runtime is added by these fixtures. Later steps must test their own
new behavior against these independent values and the approved contract.
