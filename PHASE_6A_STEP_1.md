# Phase 6A Step 1 completion

Status: **COMPLETE: CONTRACTS AND INDEPENDENT ACCEPTANCE INPUTS**.

The Theory Owner instructed `phase 6a step 1开始` on 2026-09-26
America/Los_Angeles (2026-09-27 UTC). Work starts from delivered plan commit
`753829a79fb6aa550d58dcd6fced360399c597e9` on accepted Phase 5 history and uses
`phase6a-longitudinal`.

## Completed scope

- Recorded plan approval and P6A-D01 through P6A-D08 in
  [PHASE_6A_DECISIONS.md](PHASE_6A_DECISIONS.md).
- Fixed forthcoming selection/configuration, immutable types, selected lineage
  API, report field inventory, scope references, statuses, reasons, resource
  guards and privacy in [docs/longitudinal_contract.md](docs/longitudinal_contract.md).
- Added 11 concrete synthetic cases with independent rational expectations and
  an additional Hero oracle in
  [tests/fixtures/longitudinal/README.md](tests/fixtures/longitudinal/README.md).
- Added 47 direct fixture/input/current-kernel checks. These use existing
  supported APIs; they do not implement series orchestration.
- Updated the existing current verification reference to the delivered plan
  commit and closed the implementation allowlist for this contract-only step.
  Added current plan/decision documents to the existing consistency check.

The contract preserves separate coverage types, per-version populations,
context exclusion, pair-local mapping bases and partial ancestry. New public
mapping entries and nested collision lists are bounded. Empty Python snapshots
remain separate declarations; the fixture confirms that the current pair API
rejects an unloaded endpoint rather than fabricating loaded-version evidence.

## Verification performed

Final combined command, using the existing Python 3.12 test environment:

```sh
/workspace/scratch/954124762a46/phase5_step8_env/bin/python -m pytest -q \
  tests/unit/test_longitudinal_fixture_inputs.py \
  tests/unit/test_lineage_fixture_inputs.py \
  tests/unit/test_T1_compatibility.py \
  tests/unit/test_PR007_version_order.py \
  tests/integration/test_current_verification.py \
  -k 'not distribution_integrity and not sdist_extraction'
```

Result: **230 passed, 14 deselected, zero failures**, in 2.09 seconds. The
14 intentionally unselected cases cover unchanged archive/package behavior.
They are not skipped cases in a claimed full candidate run. The 47 new cases
also passed separately after the empty-snapshot correction.

Existing source/specification/traceability checks passed:

```sh
python scripts/check_spec_consistency.py
python scripts/check_traceability.py
python scripts/release_check.py
git diff --check
```

These verify 16 frozen specifications, seven canonical resource copies,
40 owned modules and 59 protected product files. No product implementation path
is open in this step. A direct diff against the starting commit confirms no
change to runtime code, executable schemas, canonical Hero files or package
version metadata. Document references and code-fence consistency were checked.

Independent review covered formula IDs, arithmetic, denominators, empty states,
canonical field names, selected-target binding, shared graph costs, report
statuses and bounded mapping/privacy shapes. Report ownership retains the
existing PR-002 record-count method; observed tail disappearance uses the
canonical `tail_extinct_states` field.

## Checked examples and limitations

The three-version oracle has support 3/2/3 and diversity 5/8, 1/2, 2/3. It
preserves B's disappearance and reappearance, with adjacent diversity deltas
-1/8 and +1/6. Its provenance example distinguishes row/required coverage
improvement (+1/4) from known-grounding coverage decline (-1/12).

The unchanged Hero's newly recorded v1 ancestry has eight roots, HHI 1/8 and
effective roots 8. Against the established v2 values, root count changes by -3,
HHI by +1/8 and effective roots by -4. Complete, partial and zero-grounded cases
retain distinct expected root/coverage outcomes. These are existing-kernel and
independent-oracle checks, not a completed multi-target implementation.

Runtime remains `0.1.0.dev4`, report schema `1.1`. Schema 1.2, new CLI flags,
series calculations and shared selected-version lineage remain scheduled for
later steps. No full matrix, package rebuild, 100k measurement, PR merge, tag or
publication was performed. No additional governance framework was introduced.

Step 1 is complete. **Step 2 has not started**; it will implement ordered
selection and representation compatibility under the approved contract.
