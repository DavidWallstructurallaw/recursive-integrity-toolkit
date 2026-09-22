# Phase 4 validation report

Status: final candidate verification pending.
Version: `0.1.0.dev3`.
Starting commit: `9142b344bfc2dc2b33dbc696159f07bbc81b223a`.

## Required candidate checks

| Check | Scope | Current result |
| --- | --- | --- |
| Canonical regression | Complete suite on Ubuntu/Windows, Python 3.11/3.12, current/minimum dependencies | Pending |
| Real Parquet | Complete extra-enabled suite and all three real-Parquet cases | Pending |
| Scientific fidelity | All 20 frozen mathematical cases and current report goldens | Pending |
| Boundaries | Privacy, local-only execution, malformed input, safe paired output and current unauthorized-mutation checks | Pending |
| Packages | Wheel/sdist metadata, 40 modules, seven resource files, clean installed commands and package payloads | Pending |
| Examples | Documented Python and CLI examples outside the checkout | 18 commands passed using installed dev3; 11 JSON/Markdown pairs retained |
| Security | Required boundary/security workflow | First candidate failed historical stage preconditions; repair verification pending |
| Source integrity | Exact tracked source archive, current scope and frozen authority | Pending |

The minimum profile uses NumPy 2.0.0 and pandas 2.2.2, the documented jointly
compatible pair. Core environments require actual PyArrow absence; the optional
profile requires a real PyArrow installation. No skipped or projected scale run
can substitute for a required candidate performance case.

Local candidate preparation passed 96 affected current/historical control cases
and a separate 244-case selection covering the changed version tests, current
CLI, report goldens and frozen mathematical cases. Both selections passed on
their first attempt. Specification, traceability, current scope, whitespace and
document-link checks passed. These selections do not replace the pending full
supported-environment matrix. The installed example commands ran outside the
checkout with package origin verified in site-packages.

The first published candidate `0c2f5e4b5bb4730923ea87e54086fb077a66e996`
passed the remote Hero/mathematical job (203 tests). Its security job recorded
3,267 passes and 10 failures in 920.72 seconds. Those failures concern five
historical stage preconditions that still inspect the moving checkout: the
dev2 CLI migration, absence of Step 1 completion records, pre-repair assembly
bytes and the Step 7/8 module-change sets. This candidate is not accepted.
The repair binds those historical checks to already available accepted stage
snapshots, retaining their assertions and mutation cases. Current Step 11
behavior and unauthorized-mutation checks continue to inspect current source.
The Ubuntu current/minimum, Windows minimum and real-Parquet complete runs
also failed only these ten historical cases. Focused repair verification passed
118 affected cases plus 143 related historical/workflow cases. A broader local
control attempt was interrupted after partial progress; it is not recorded as a
complete pass. Full repaired remote gates remain required. Full remote logs and
every attempt remain in the external evidence.

## Accepted prior measurements

Step 10 already measured the repaired complete 100,000-record audit on Linux,
Python 3.12.14, NumPy 2.5.3 and pandas 3.0.6: 1,362.470766888 seconds outer wall
time and 7,640,743,936 bytes peak RSS. JSON size was 442,741,529 bytes and Markdown
size 165,120,454 bytes. The expected 66,000 warnings and independent numerical
values passed. Full-scale traced Python allocation peak was not measured.

Three complete untraced Hero observations were 0.493891416, 0.654631544 and
0.762660259 seconds. A separate traced Hero observation was 4.137158500 seconds
with 11,044,047 bytes peak traced Python allocations. The traced observation is
not an untraced throughput measurement. These results describe the recorded
reference host and fixtures. Large report size and memory use remain limitations.

The accepted Step 10 remote run 35718603026 passed 333 focused cases. Its raw
artifact download was unavailable; available remote logs and metadata were
archived. This prior result is not presented as Step 11's full matrix result.

## Evidence and acceptance

Raw commands, environment versions, JUnit, logs, measured observations and any
failed attempts belong in the external Step 11 evidence bundle. This report
will record actual outcomes after execution. Packaging reuses the same candidate
run's full-suite evidence. Acceptance-only report edits receive focused checks
under the user's governance policy; no new meta-verification layer is required.
