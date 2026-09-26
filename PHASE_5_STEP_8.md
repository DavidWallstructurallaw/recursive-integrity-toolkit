# Phase 5 Step 8 Completion

Date: 2026-09-26 UTC. Status: **COMPLETE; PHASE INCOMPLETE**.

The Theory Owner instructed `Phase 5  Step 8  开始`. Work starts from
`267504e8fee4784f6d041e445a9e690c982e61a3` on `phase5-lineage`.
This step connects explicit CLI lineage requests, local context inputs and
configured resource limits to the accepted analysis and report owners.

## Delivered behavior

`rit audit --lineage` and `rit example --lineage` execute graph, ancestry,
lineage closure and shared-root analysis. Ordinary invocations retain lineage
`not_requested`. The CLI implements orchestration only; the accepted kernels
continue to own all calculations. No simulation is enabled by these flags.

Repeated `--lineage-records PATH` declarations and configured
`inputs.lineage_context` use the existing CSV, JSONL and optional Parquet loaders.
Context can provide ancestors without entering primary support, diversity,
duplicate, provenance, direct-bound or tail denominators. It does not implicitly
request comparison. An explicitly requested comparison can also supply ancestors
while retaining its existing comparison semantics.

Context versions must be disjoint from primary and comparison versions.
Duplicate composite identities fail before joining provenance. Repeated context
files may contain distinct records from the same context version. Existing
Python/config multiplicity for other input roles is preserved. Config-relative
and CLI-relative context paths retain their separate bases, even when their
relative spellings match.

`validate --lineage-records ...` performs input and immediate-reference validation
only. Both its unsupported `--lineage` flag and config `lineage: true` are
rejected. Configuration resolution and the Python `validate_bundle` API remain
inert with respect to analysis. Existing empty-file rejection remains unchanged;
the CLI never substitutes context for a missing primary population.

The four configured lineage budgets use the approved positive integer defaults:
200,000 nodes, 1,000,000 edges, 1,000,000 logical root memberships and 10,000,000
root-union candidate visits. They remain separate from loader limits. A small
optional field on the existing `FamilyFailure` retains admission resource usage
when graph construction fails. Reports preserve exact admitted counts, the limit
and the rejected next unit without claiming completed graph, cycle or root work.
Root-stage failures retain already completed graph observations. Independently
completed ordinary values survive either failure. Resource errors use exit 1,
configuration errors exit 2, and parent/cycle errors exit 3 under the existing
exit policy. Fatal admission errors retain failed run status; ordinary errors
with usable surviving evidence can retain partial run status.

Context identities and paths use the existing report/privacy boundary in every
output sink. Whole-list omission remains schema-valid. Executed lineage capability
notes no longer describe its graph implementation as deferred. Plain Hero stderr
now explains that lineage was not requested and names the opt-in command.

## Verification

Local verification used Python 3.12.14, NumPy 2.3.5 and pandas 2.2.3. The context
loader checks actually ran with PyArrow 25.0.1. A separate core environment had
no PyArrow installed and ran the installed-wheel Hero checks.

| Check | Actual result |
|---|---|
| Combined affected regression, 48 test modules | 2,314 passed in 153.09 seconds; no failures or skips |
| New CLI integration cases, included above | 28 passed |
| New inert configuration cases, included above | 21 passed |
| New context/input and admission-report cases, included above | 28 passed |
| Actual installed ordinary and lineage Hero, standard and redacted | PASS with network blocked and PyArrow absent |
| Wheel/source identity and report schema mirror | PASS; all 47 module/resource files match |
| Specification, traceability and current source checks | PASS |
| Four workflow YAML files and whitespace check | PASS |
| Independent implementation and boundary review | PASS; no remaining blockers |

The 77 new cases cover actual CSV/JSONL/Parquet context ingestion, opt-in versus
input-only dispatch, target denominators, explicit comparison, mixed path bases,
role overlap and duplicates, all four resource budgets, chronology recovery,
privacy, output collisions and Hero arithmetic. Direct wire mutations reject
false admission stages, counters and attempted values. Existing report goldens
passed unchanged, preserving ordinary numerical values, scope and configuration
hash behavior.

Installed Hero confirms N=8 with eight context records, G=8 and C=U=0, five roots,
HHI=0.25, four effective roots, lineage bounds `[0,0]`, direct bounds `[1/2,1/2]`
and a present descriptive shared-root signal. Both schemas and renderers preserve
the same meaning; scientific unavailable conclusions remain explicit. The six
packaged Hero inputs match their canonical bytes and remain unchanged.

### Findings resolved during implementation

Review identified mixed config/CLI context paths incorrectly sharing one base;
the adapter now retains declaration provenance when resolving their paths.
Review also identified admission counters being lost by the previous generic
family-failure handoff. The bounded payload extension fixes that concrete product
reporting gap without adding a new failure framework.

During the shared resource-validator refactor, tests caught a missing local
variable assignment that rejected otherwise valid lineage reports. It was fixed
before the clean focused and combined runs. A development-time source-snapshot
check also overlapped active edits; the unchanged check passed after the product
bytes stabilized. Final wheel identity verification and the combined regression
used those stable bytes. No failed check remains waived.

## Handoff

Package version remains `0.1.0.dev3`; report schema remains `1.1`. The current
source boundary advances to Step 7 and opens only the twelve changed product
paths. The other 47 product files, exact product inventory, 16 frozen
specifications and seven packaged resource copies remain protected. Existing CI
adds the affected cases and removes redundant CLI reruns. No new governance
registry, historical source migration or evidence-of-evidence layer is added.

Step 9 remains bounded adversarial/mutation work and actual lineage scale
measurement. Step 10 remains the complete candidate matrix, release checks and
dev4 handoff. No full OS/Python/dependency matrix, 100k lineage measurement, merge,
tag, software publication or hosted CI success is claimed by this step.
