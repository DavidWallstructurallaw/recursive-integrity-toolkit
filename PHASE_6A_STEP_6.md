# Phase 6A Step 6: canonical series reporting

## Authority and scope

The Theory Owner requested `Phase 6A Step 6 继续` on 2026-09-26
America/Los_Angeles (2026-09-27 UTC). This step starts from accepted commit
`e8d888614a2d6d2ce446cc0c86d9577036f27cd8` on `phase6a-longitudinal`.
P6A-D07 and the Step 1 public field contract govern the implementation.

The package remains `0.1.0.dev4`. Every current report uses schema `1.2`, with
the canonical schema and packaged mirror kept identical. Strict schema 1.1
consumers must explicitly adopt the new schema. The twelve top-level sections,
legacy scientific values and input-observability meanings remain intact.

## Implemented behavior

`assemble_report(..., longitudinal=result)` now accepts the validated series
handoff. It records ordered snapshots, exact adjacent/first-baseline pair rows,
original and harmonized bases, complete population and representation scope
references, source/direct/lineage changes, endpoint coverage and reasons, shared
graph evidence, and both equal capability execution mirrors. Ordinary result
arguments remain independent; a series never selects a legacy pair implicitly.
Not-requested series have explicit empty inventories and execution metadata.

Every approved snapshot/comparison field is registered with its owner, method,
unit and evidence class. Main coverage remains the inherited ratio/null shape;
delta endpoint coverage retains full count denominators. The zero-parent
reference convention retains both endpoint flags. Numerical values and exact
counts precede display limits. State sets, mapping entries, collision groups,
each collision's source states, context versions and graph diagnostics retain
bounded detail with exact totals and omissions.

JSON and Markdown consume the same canonical safe view. Markdown adds ordered
snapshot and comparison summaries and retains the complete envelopes underneath.
Hash mode preserves report joins with basis-local state pseudonyms. Omit mode
retains structural IDs/references and exact aggregates, while protecting version
literals and identity-bearing details. User state-meaning text is absent from
redacted views; identity strings cannot become dictionary keys in the new family.

`analyze_longitudinal_failure(...)` confirms a rejected selection and preserves
usable independent snapshot evidence. Missing/conflicting chronology leaves
the order source, primary reference and comparisons empty; declaration order
identifies rows without becoming chronology. Version admission failure computes
no snapshot prefix. Its exact requested selection count is retained.
`assemble_report(..., longitudinal_failure=result)` validates this handoff.

Existing `validate` CLI output retains the empty, not-requested longitudinal
metadata required by schema 1.2. It still dispatches no analytical work. This is
report-shape integration only; no longitudinal CLI flag or config execution is
introduced in this step.

## Consumer validation

The report boundary verifies current input binding, complete membership,
assignment/count/provenance evidence, owner metadata, mapping and set arithmetic,
tail rules, deltas and family statuses. It rejects stale same-ID results and
self-consistent forged aggregates rather than treating a signature as proof.
It does not call analysis, assignment, graph-building or I/O entry points.
Canonical validation also checks public scopes/bases/endpoints, chronological
schedule, exact endpoint reasons/coverage, finite arithmetic, statuses, bounded
detail and valid identity omission before and after privacy transformation.

Completed selected lineage retains a private immutable certificate for all
loaded roots/reasons and SCC quotient ranks. Consumers check accepted edges,
SCC connectivity/ranks and affected nodes, local depth/root equations, target
aggregates and completed membership/union counters. The certificate reuses
immutable root sets and is never serialized. Root-aborted runs retain no root
prefix: failure counters establish limit consistency, not runtime attestation.
The validation boundary does not independently establish the truth of the
supplied validated input bundle.

## Verification

The existing Python 3.12 environment ran the following broad regression:

```sh
/workspace/scratch/954124762a46/phase5_step8_env/bin/python -m pytest -q \
  tests/unit tests/integration tests/golden \
  --ignore=tests/integration/test_package_install.py \
  --ignore=tests/integration/test_optional_dependency.py \
  -k 'not distribution_integrity and not sdist_extraction and not installed_without_pyarrow and not parquet'
```

This run completed with **3402 passed, 2 failed, 16 deselected** in 232.02 seconds.
Both failures were old validate-output assertions expecting an empty derived
object. Their no-calculation checks already passed. The assertions now require
the explicit empty series metadata, and both corrected cases passed in 1.22
seconds. No production calculation was changed to resolve those assertions.

A final focused run of `test_longitudinal_report_contract.py`,
`test_optional_dependency.py` and `test_package_install.py` passed **42 cases**
in 4.70 seconds. This includes the final shared-graph count and repeated safe
diagnostic checks, which were added after broad collection. These package tests
inspect metadata and import boundaries; they do not build or install artifacts.

Across those three runs, de-duplicating by test identity and retaining the latest
result gives **3412 distinct passing cases, zero unresolved failures or skips**.
The broad selection excludes 14 archive integrity/extraction cases, the fresh
installed-Hero case and one Parquet-specific boundary case. The explicit real
PyArrow suite was not enabled. A preliminary broad run was interrupted only to
correct the installed-case selector; it supplies no claimed completion count.

The five new test files contain **175 cases**. Additional overlapping checks
included 68 canonical/report cases, 229 computational-handoff cases, 157 lineage
neighbors and 72 golden/validate cases; these are not additive coverage counts.

The final protection checks passed:

```sh
python scripts/check_spec_consistency.py
python scripts/check_traceability.py
python scripts/release_check.py
git diff --check
```

These retain 16 frozen specifications, seven canonical resource copies, five
schemas, six Hero inputs, 41 owned modules and the local-only/layer boundaries.
The current source gate protects 51 product files and admits nine Step 6 paths.

The new tests cover independent frozen two/three-version values, full and partial
lineage, zero roots, all four lineage limits, selection/admission failure,
incompatible and incomplete-mapped pairs, empty/all-excluded distributions,
earlier-tail disappearance, privacy joins, nested display limits, hostile
Markdown literals, invalid handoffs and canonical mutations.

The normal and redacted Hero goldens were independently reviewed against the
accepted Step 5 outputs. All 33 existing scientific envelopes in each view are
exactly unchanged. Existing JSON fields differ only in schema version; new empty
series inventories and execution mirrors are additive. The authored numerical
oracle, frozen Hero inputs and longitudinal acceptance fixtures are unchanged.

## Remaining scope

No package version bump, full candidate matrix, fresh wheel/sdist installation,
scale measurement, merge, tag or release is part of this step. Step 7 owns
longitudinal CLI/config and installed examples; Step 8 owns bounded scale and
adversarial preflight; Step 9 owns dev5 and the candidate/delivery checks.
Repeated full-input provenance joins and certificate verification remain
explicit work for the bounded performance assessment. No new dependency or
package module is introduced.

**Step 6 is complete. Step 7 has not started.** The deliverable is committed and
synchronized on `phase6a-longitudinal`; no merge, tag or release is implied.
