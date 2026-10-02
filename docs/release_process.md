# Development and Release Verification

`0.1.0.dev3` is the Phase 4 report/CLI development milestone. Completion requires recorded candidate evidence and does not authorize stable v0.1 publication, a tag, main merge or Phase 5 implementation. The three `PHASE_4_*` milestone reports distinguish actual acceptance, remaining limits and unexecuted work. Prior phase records remain historical evidence.

## Choose the gate by impact

| Change or milestone | Required scope |
|---|---|
| Documentation or nonauthoritative metadata | Formatting/static checks and affected document consistency |
| Isolated implementation | Affected unit tests, dependency neighbors and applicable mathematical/security checks |
| Schema, public API, mathematics, provenance, privacy or package boundary | Relevant integration, compatibility and broader regression appropriate to impact |
| PR candidate | Complete canonical regression and required supported-environment matrix |
| Release candidate or phase delivery candidate | Complete regression, supported matrix, build/install, canonical examples, reproducibility, artifact integrity and applicable security checks |

Documentation that participates in executable authority receives the applicable authority checks. Administrative successors after an accepted code candidate do not automatically repeat the full matrix when executable and authoritative bytes are unchanged. Preserve the accepted source identity and state exactly what changed. If an executable or authoritative change invalidates prior evidence, rerun the affected gate before acceptance.

Keep three concerns distinct: the canonical suite protects current supported behavior; release verification covers environment/package/reproducibility boundaries; Git and archived records preserve superseded evidence. Preserve historical behavioral guarantees without automatically adding test-body migrations, registries or evidence-of-evidence layers. A new verification mechanism needs a concrete failure that existing controls cannot adequately detect. New governance mechanisms additionally require the reason Git/archive evidence is insufficient, maintenance cost and an exit or consolidation path.

## Supported candidate profiles

| Profile | Environment and evidence |
|---|---|
| Core, current dependencies | Ubuntu and Windows, Python 3.11 and 3.12; resolved versions retained; PyArrow genuinely absent |
| Core, minimum jointly compatible dependencies | Same OS/Python matrix, NumPy 2.0.0 and pandas 2.2.2; PyArrow absent |
| Real Parquet | Ubuntu/Python 3.12 with actual PyArrow; real roundtrip, row-limit and invalid-file regressions |
| Security | No-network/import, declarative mapping, safe input/output paths, privacy/redaction and protected-owner boundaries |
| Hero and mathematics | Frozen mathematical cases, literal standard/redacted report goldens and installed Hero behavior |
| Package and delivery | Wheel/sdist integrity, strict metadata checks, clean installed execution outside the checkout, resource equality and tracked-source archive |

The package still declares `numpy>=2.0` and `pandas>=2.2`. NumPy 2.0.0 with pandas 2.2.0 cannot resolve because that pandas version requires NumPy below 2. The retained minimum profile uses pandas 2.2.2. This covers that jointly compatible pair, without claiming every intervening version or all optional-dependency minimums. Current profiles record the versions actually resolved at execution time.

Retain Python/platform/dependency details, `pip freeze`, `pip check`, commands, exit codes, JUnit identities and workflow logs. Core absence and real-PyArrow presence must be checked explicitly. A skipped, failed, duplicate or uncollected required test cannot stand in for an executed passing test. Do not add repeated jobs/subsets into a fictitious distinct-test total.

## Local checks and builds

From a prepared full Git checkout:

```bash
python -m pip install ".[test,release]"
python scripts/check_spec_consistency.py --phase 4 --step 11
python scripts/check_traceability.py --phase 4 --step 11
python scripts/release_check.py --phase 4 --step 11 --diff
```

The Phase 4 Step 11 candidate runs `python -m pytest -p no:cacheprovider -q` in all eight core matrix cells and the real-Parquet cell, retaining the complete suite including the 100,000-record report case. The release job reuses the exact same-commit Ubuntu/Python 3.12 current-core and real-Parquet results rather than running both suites again. The Hero/mathematics and security roles run separately. Full Git history is needed for the bounded retained historical checks. Scope guards protect the fixed authority files, supported runtime behavior, schemas, Hero resources and mathematical/report oracles. The active manifest cannot expand its own permissions.

Build into a fresh evidence directory:

```bash
python -m build --outdir /absolute/evidence/dist
python -m twine check --strict /absolute/evidence/dist/*
python scripts/release_check.py --phase 4 --step 11 --dist /absolute/evidence/dist
```

The candidate build role performs two default builds from sdist with the same recorded build environment and `SOURCE_DATE_EPOCH`, comparing wheel bytes and sdist payloads. The package checks compare wheel/sdist module and resource bytes with the tested tree. Installed checks must import the installed artifact, with checkout source excluded. Keep import/input-only checks with NumPy/pandas/PyArrow blocked separate from numerical/audit checks with required dependencies available. Both operate under the declared no-network checks. Exercise installed `example`, `audit`, `validate`, help/version and the documented Python examples. Wheel and sdist must include the six exact Hero files and report schema, without adding Python modules.

A source archive contains one project root and the complete tracked tree. Compare archived member bytes with the accepted checkout. Exclude Git internals, environments, caches, generated bytecode, private inputs and full theory PDFs. Wheel, sdist and source archive have different documented scopes. Retain artifact hashes with actual source commit/tree identity in the external receipt; committed documents need not encode their own eventual hash.

## Performance evidence and limits

Keep complete-report timing separate from the CLI's pre-publication `run.duration_seconds`. Use untraced wall time for the Hero under-five-second target and record hardware/environment. Allocation tracing is a separate observation with measured overhead. RSS describes fresh-process peak resident size and includes interpreter/native allocation; it is not a delta or a Python-only allocation measure.

The accepted Step 10 reference-container 100,000-record metadata run took 1,362.4708 seconds, peaked at 7.12 GiB RSS and produced approximately 443 MB JSON and 165 MB Markdown. That run checked independent aggregate expectations through actual published outputs. It measures the declared synthetic workload without certifying other data shapes, common-laptop throughput, general linear scaling or deferred lineage behavior. Its full-scale Python allocation peak was not measured; a separately labeled bounded run characterized tracing overhead.

The Step 10 observation supplies the comparison baseline; the Step 11 full candidate matrix also records fresh complete-suite performance observations. For later changes, reuse accepted observations when product/report bytes and relevant conditions are unchanged. Repeat expensive performance measurements only for a concrete impact or required gate, with comparable dataset, tracing mode, environment and resources. Preserve all attempts and explain target misses. A timeout is a resource guard and a failed attempt, never a successful throughput result. The [performance README](../tests/performance/README.md) defines the generator, expectations and measurement scope.

## Acceptance and handoff

The active CI workflow calls the reusable build/delivery workflow after core and Parquet success. Together with the separately dispatched Hero and security workflows, this supplies four verification roles from three dispatchable workflows. There is no additional push-triggered full matrix or standalone performance job. Record the actual immutable candidate commit and required workflow roles. Completion can be claimed only after their required checks pass and deliverable identities are known. If the final record changes only nonauthoritative documentation, verify those changes and reuse the identified code-candidate evidence under the policy above. Changes to executable/authoritative content require the corresponding checks. Do not claim a matrix was rerun when it was reused.

The external receipt identifies candidate/final source, actual workflow attempts, commands, artifacts, hashes, failed attempts, fixes and limitations. Hosted artifacts have finite retention. If a hosted binary cannot be retrieved and verified, disclose that gap and distinguish locally reproduced bytes from the hosted artifact. Archive previous evidence without expanding permanent current execution merely to preserve old source forms.

GitHub evaluates PR path filters against the complete three-dot diff. A documentation-only successor on an existing code PR can therefore trigger the matrix despite `paths-ignore`. After every required candidate gate passes, an acceptance-record successor may use `[skip ci]` when an exact diff confirms that only nonauthoritative documentation changed and executable, workflow, test and authority bytes are unchanged. Retain the accepted candidate identity and results, run focused document/source checks, and record evidence reuse. This cannot excuse a failed or outstanding product gate. Required checks may remain pending on the skipped head, so this handoff keeps the PR draft and unmerged; a later merge must satisfy its applicable checks. See GitHub's [path-filter semantics](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow#git-diff-comparisons) and [skip instructions](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/skip-workflow-runs).

Stop at the approved development milestone. Stable release, merge, tag, publication and the next phase remain separate actions.
