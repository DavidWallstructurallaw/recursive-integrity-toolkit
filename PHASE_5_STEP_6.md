# Phase 5 Step 6 Completion

Date: 2026-09-23 UTC. Status: **COMPLETE; PHASE INCOMPLETE**.

The Theory Owner instructed `ok 继续Phase 5 Step 6`. Work starts from
`d81966561502b94701712a3d4b4b7fd50783cba9` on `phase5-lineage`.
This step implements lineage closure bounds and the descriptive shared-root
proxy using the completed ancestry result.

## Delivered behavior

`metrics.bounds.lineage_closure_exposure` returns the conservative interval
`[C/N, (C+U)/N]` with width `U/N`. Only selected targets enter the denominator.
The immutable result retains the source G/C/U partition, coverage, unresolved
reasons and input diagnostics. A complete all-unresolved partition yields
`[0,1]`; empty targets and resource-aborted propagation have unavailable values
with explicit reasons. Available bounds do not erase input errors or imply
complete ancestry. Existing direct-bound behavior is preserved.

`lineage.ancestry.shared_ancestry_dependence` returns `present` only when an
exact root supports at least two targets. It discloses partial status when U>0.
`not_present` requires nonempty targets with fully resolved ancestry and no
shared root. Incomplete evidence without a witness, empty targets and resource
failure remain `unavailable` with `indeterminate` level. Duplicate paths and
aliases cannot manufacture target incidence.

Both results retain one validated immutable ancestry source, with computed
properties instead of duplicate record/root tables or independently mutable
summary fields. The proxy exposes a real root contribution witness and coverage
references. Neither operation starts ingestion, graph analysis, report assembly
or file/network access. Direct-only bounds retain their lazy dependency boundary.
The outputs remain operational descriptions of lineage topology and conservative
exposure, with no risk calibration or causal/scientific certification.

## Verification

Local verification used Python 3.12.14 with the core dependency profile.

| Check | Result |
|---|---|
| Combined Step 6 direct and affected regression gate | 664 passed in 5.50 seconds |
| Separate validation/pair CLI isolation checks | 2 passed in 0.47 seconds |
| Specification consistency, traceability and source scope | PASS |
| Four workflow YAML files and whitespace check | PASS |
| Independent implementation and test review | PASS; no outstanding blockers |

The combined gate includes 25 new lineage-bound/proxy cases, all 74 unchanged
direct-bound cases, and existing ancestry, concentration, graph, cycle, resource,
metric-pipeline and input-boundary checks. All twelve frozen ancestry fixtures
retain their interval values. Hero lineage closure remains `[0,0]`, while
its direct closure remains `[1/2,1/2]` before and after explicit lineage calls.

The direct tests distinguish exact incidence one from two, target incidence from
context/path/alias multiplicity, partial positive witnesses from incomplete
negative evidence, missing from unknown branches, complete all-unresolved
classification from resource-aborted classification, and empty target scope.
Masking grounded or closed evidence into unresolved evidence can only widen the
conservative interval. Invalid typed handoffs are rejected, frozen snapshots
retain input errors, and blocked loaders/graph functions confirm no repeated
graph execution or I/O.

Independent review additionally checked nine bounded semantic cases with graph,
cycle and provenance dispatch blocked. An isolated process imported the bounds
module and executed both existing direct entry points while all lineage modules
remained unloaded. The review harness needed its source import path and empty
fixture role corrected; no product defect or corresponding source change was
required. The new permanent suite passed on its first execution.

### Bounded mutation check

Three passing selected tests were rerun against three disposable source
variants. Each variant imported and executed successfully, then failed actual
semantic assertions with exit code 1.

| Seeded defect | Detection |
|---|---|
| Upper bound omits U | Expected `2/3`; observed `1/3`. |
| Shared-root threshold changes from `>=2` to `>2` | Exactly two target records lost their required `present` signal. |
| Absence drops the U=0 requirement | Incomplete evidence incorrectly returned `available` instead of `unavailable`. |

All three mutations were killed. The unchanged variant passed all three selected
tests. No permanent mutation runner or registry was added.

The current source check advances its single comparison commit to completed
Step 5 and opens only the existing ancestry and bounds modules. The other 57
product files, exact product inventory, 16 frozen specifications and seven
packaged resource copies remain protected. No additional governance framework,
historical migration chain or permanent mutation mechanism is introduced.

## Handoff

Package version remains `0.1.0.dev3`; executable report schema remains `1.0`.
Step 7 report/schema integration requires its separate execution instruction.
Ordinary reports and CLI calls retain their current behavior.

Full compatibility/release verification and 100k lineage performance measurement
remain their designated candidate/scale gates. No merge, tag, software
publication or hosted CI success is claimed here.
