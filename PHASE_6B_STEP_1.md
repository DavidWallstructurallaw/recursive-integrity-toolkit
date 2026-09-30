# Phase 6B Step 1: contracts and independent acceptance inputs

Date: 2026-09-30. Status: **TASK COMPLETE, PHASE CONTINUES**.

## Completed

Started `phase6b-simulation` from accepted Phase 6A completion
`b6389c6c50f2fc61d39580274bd24ed39e09ca45` under the Theory Owner's explicit
`Phase 6B 继续吧` instruction. The work follows the established stepwise workflow.

Produced `PHASE_6B_PLAN.md`, `PHASE_6B_DECISIONS.md` and
`docs/simulation_contract.md`. They specify the constant external-source model,
literal shared state space, numerical and RNG rules, exact event meaning,
one/two-model comparison, bounded execution, staged report/config interfaces and
privacy. The eight-step plan ends in a development candidate handoff.

Replaced the reopening fixture placeholder with eight rational one-step cases,
a possible recurring loss/re-entry path, a zero-horizon case and a two-step
lambda-one contrast. The fixture expectations were authored independently of
any reopening implementation. Small exact multinomial enumeration checks their
arithmetic. Conditional next-step statements and unconditional diversity
expectations are explicitly distinguished.

Advanced the existing source gate to the accepted dev5 baseline with an empty
product-change allowlist, removed the completed dev4-to-dev5 exception, and
adapted its existing negative version test. The existing specification check
requires the three new contract documents. No additional verification framework
was introduced.

## Validation

The supplied Universal Inbreeding Law v2.2 page 8 was rendered and inspected for
F-017; its surrounding source limitations agree with the frozen T5 definitions.
Read-only reviews found no remaining scientific or authority conflict. Review
corrections clarified semantic-state pseudonymization, preserved state meaning,
the effective-vector basis of a future closed analytic baseline, bounded state
tables, degenerate fixtures and conditional/unconditional expectations.

Targeted final run:

```text
tests/unit/test_reopening_fixture_inputs.py
tests/unit/test_T1_resampling.py
tests/unit/test_T5_reopening.py
tests/unit/test_PR016_determinism.py
tests/integration/test_current_verification.py

247 passed in 7.28s; zero failures or skips
```

The run used Python 3.12.14, pytest 9.1.1 and NumPy 2.3.5, importing this
checkout's `src` package. It reused preserved test dependencies through
`PYTHONPATH`; this was source verification, not a new installed-wheel check.
The 29 new fixture checks verify exact acceptance inputs. The existing T5 test
still verifies that runtime reopening has not yet opened.

Current static checks passed: five schemas parsed, 16 frozen specifications
unchanged, 14 canonical resource copies unchanged, 41 module ownership/local-only
boundaries checked, and 75 protected product files unchanged with zero allowed
runtime changes. `git diff --check` passed.

No full regression matrix, package rebuild, 100k dataset measurement or Phase 6B
performance claim was made for this contract-only step.

## Decisions, conflicts and continuation

Used approved UD-017 and existing T1/T5/F-015/F-017 definitions, the accepted
Phase 3 numerical/replay policy, and the existing verification governance.
UD-031 keeps empirical intervention ingestion deferred. P6B-D01 through
P6B-D07 record bounded implementation choices within the newly authorized phase.

Conflicts: none. Runtime remains `0.1.0.dev5`, report schema `1.2`. Step 2 will
implement the pure mixture and reopened sampler in `metrics/resampling.py`;
the remaining report, orchestration, CLI and delivery work stays assigned to
its planned steps. No merge, tag or publication was performed.
