# Phase 5 Step 5 Completion

Date: 2026-09-23 UTC. Status: **COMPLETE; PHASE INCOMPLETE**.

The Theory Owner instructed `Phase 5 Step 5 继续`. Work starts from
`2450100d08355d8cb1e0be931345f44572861e4a` on `phase5-lineage`.
This step implements root incidence, fractional mass, ancestry concentration
and effective external-root count in the existing ancestry owner.

## Delivered behavior

`analyze_lineage` extends its immutable result with typed `RootContribution`
rows and the complete distinct-root count. Each root's incidence counts complete
nonempty-root targets containing that root. Incidence shares divide by the full
target population N. Each grounded target contributes mass one, divided equally
among its unique roots. Root weights divide accumulated mass by G, the number
of targets with complete nonempty roots. HHI sums squared weights; effective
root count is its reciprocal.

Context records supply ancestry without entering either denominator. Repeated
paths and aliases do not multiply a target's root contribution. Unresolved
targets supply no exact mass. Their presence marks conditional root metrics
partial, accompanied by existing G/N coverage. Complete known-empty targets
remain distinct from unresolved targets.

Contributions retain all supporting roots and are ordered by decreasing
incidence with canonical-key ties. Numerical reduction is deterministic. The
future report detail limit does not truncate the calculation. The values
describe a topological allocation; they do not measure causal influence,
semantic error, independent information or universal source diversity.

A completed G=0 partition returns an empty contribution tuple and root count
zero. HHI and effective roots are null with `NO_RESOLVED_EXTERNAL_ROOTS`.
Resource-aborted propagation returns null contributions and aggregate values
with `LINEAGE_RESOURCE_LIMIT_EXCEEDED`; independently completed structural and
reference observations retain their Step 4 behavior.

## Verification

Local verification used Python 3.12.14 with the core dependency profile.

| Check | Result |
|---|---|
| Combined Step 5 direct and affected regression gate | 565 passed in 6.59 seconds |
| Separate validation/pair CLI isolation checks | 2 passed in 0.48 seconds |
| Specification consistency, traceability and source scope | PASS |
| Four workflow YAML files and whitespace check | PASS |
| Independent implementation and test review | PASS; no outstanding blockers |

The combined gate includes 24 new concentration cases alongside the existing
ancestry, resource, graph, cycle, parent and dependency-neighbor cases. It covers
all twelve frozen ancestry fixtures and the Hero. Hero HHI/effective roots remain
`1/4` and `4`; the frozen mixed multi-root fixture remains `5/8` and `8/5`.
An additional unequal-support oracle with N=6, G=4, C=1 and U=1 produces HHI
`35/96` and effective roots `96/35` using exact rational expectations.

Direct tests also exercise permutation, identity renaming, duplicate paths and
aliases, incidence-first ranking, a full 105-root distribution, unavailable
concentration, resource-aborted null distributions, and immutable typed
handoffs. The completed all-unresolved partition retains its empty observed
root distribution even when input errors make overall execution fail.
Independent review ran forty bounded rational/relabeling cases; the maximum
observed relative HHI rounding difference was approximately `3.16e-16`.
Its initial ad hoc `3e-16` tolerance was adjusted to `1e-15`; no product change
was required. The permanent new suite passed on its first execution.

### Bounded mutation check

One passing unequal-support test was rerun against three disposable source
variants. Each variant successfully imported, calculated and constructed its
result, then failed an independent assertion with exit code 1. Denominator
mutations changed the corresponding declared metadata as well as arithmetic,
so local row consistency alone could not reject them.

| Seeded defect | Detection |
|---|---|
| Incidence denominator N replaced with G | Reported denominator 4 rejected against independent N=6. |
| Weight denominator G replaced with N | Reported denominator 6 rejected against independent G=4. |
| Effective count uses HHI without its reciprocal | `0.3645833333333333` rejected against `96/35`. |

All three meaningful mutations were killed. No permanent mutation runner,
registry or additional execution layer was added. Broader adversarial and scale
work remains Step 9.

The existing source check advances its single comparison commit to completed
Step 4 and continues to open only `lineage/ancestry.py`. The other 58 product
files, product inventory, 16 frozen specifications and seven packaged resource
copies remain protected. No new governance registry or historical migration
is introduced.

## Handoff

Package version remains `0.1.0.dev3`; executable report schema remains `1.0`.
Step 6 lineage bounds and shared-root proxy need their separate execution
instruction. Report and CLI integration remain Steps 7-8.

No full compatibility matrix, release build, clean install, optional Parquet
profile or 100k performance measurement is claimed here. Their designated
candidate/performance gates remain unchanged. No merge, tag, publication or
hosted CI success is claimed.
