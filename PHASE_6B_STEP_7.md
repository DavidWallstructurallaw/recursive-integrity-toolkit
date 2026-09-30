# Phase 6B Step 7: scientific, adversarial and performance preparation

Date: 2026-09-30. Status: **TASK COMPLETE, PHASE CONTINUES**.

## Scope and source

The Theory Owner requested `Phase 6B Step 7`, authorizing this increment from
Step 6 commit `065cafa017881258c6dc139c22815b806b75bce6`, source tree
`109339bcf7c98de1caf2d45798d8b5ed63352e08`, on `phase6b-simulation`.

All 83 product files remain byte-for-byte frozen at that source. The existing
source gate advances to Step 6 with an empty implementation allowlist and removes
the completed Step 6 package-data exception. No product algorithm, admission
limit, dependency, schema, packaged resource or version change was needed.
There are still 41 runtime modules, 18 canonical packaged resources and 16 frozen
specifications. The package remains `0.1.0.dev5`, report schema `1.3`.

## Scientific and adversarial checks

Two new direct scientific tests fill distinct gaps. A three-state one-step
experiment uses `p=(3/4,1/4,0)`, `r=(1/4,1/2,1/4)`, lambda `1/2` and sample
size 3. Independent rational multinomial enumeration gives ten joint count
outcomes under source `(1/2,3/8,1/8)`, third-state re-entry probability `169/512`
and expected sampled diversity `19/48`. Ten thousand replicates are checked
against broad six-binomial-standard-deviation bounds for every joint outcome.
This tests count dependence and the conditional sampler's complement branch
without fixing a cross-environment random path.

A second case uses lambda one, initial `p=(1/2,1/2)`, sample size 4 and a
concentrated external source. Every sampled transition has zero diversity while
the selected closed F-015 expectation stays positive at finite steps. External
input therefore supplies no guaranteed
diversity benefit, and the closed expectation remains model-specific.

Twelve integration cases exercise resource and failure behavior:

- The actual 1,000,000-cell aggregate boundary is admitted by configuration,
  eligibility, collective experiment preflight and individual kernel preflight
  for closed-only, reopened-only and both model orders. A first-generation
  sentinel stops execution before trajectory allocation.
- The nearest selected over-budget requests use 1,000,001 cells for a single
  model or 1,000,004 for two models. Configuration, forged typed eligibility
  and kernel execution refuse them before model execution, RNG or allocation.
- Audit and input-only validation publish safe failure reports for an excessive
  request, without leaking private state identifiers.
- In each model order, the first model actually completes and the second model's
  RNG initialization raises an injected private error. The complete experiment
  is discarded, independent audit metrics remain available, and protected
  diagnostics disclose no partial successful scenario or private error text.

The equality probes establish real-limit admission. They do not allocate or
publish a million-cell report, and do not establish full-capacity performance.

## Bounded fault sensitivity

The plan's ten faults were injected independently into disposable copies of the
accepted source. The unchanged selected baseline passed 22 cases in 1.29 seconds.
Each fault was detected by its intended direct assertion, execution sentinel
or semantic report validation. Each source copy was restored and checked by
hash. The main product tree was
never mutated. Existing test names below uniquely identify the detectors.

| Injected fault | Existing detector | Observed failure |
| --- | --- | --- |
| Wrong lambda coefficient | `test_T5_authored_exact_mixture_cases` | Mixture `(1/4,3/4)` rejected against `(3/4,1/4)` |
| External input applied only initially | `test_T5_lambda_one_refreshes_external_source_after_disappearance` | Second-step source failed the prescribed refresh |
| Nonabsorbing lambda-zero state | `test_T5_lambda_zero_exactly_retains_closed_paths` | Four path-equality cases failed; two zero-horizon controls passed |
| Reachability reported as realized re-entry | `test_T5_reachability_is_not_realized_reentry` | Fabricated event had a zero sampled count |
| Step-zero event | `test_T5_horizon_zero_keeps_initial_without_events` | Fabricated initial event rejected |
| Recurrent event deduplication | `test_T5_prescribed_repeated_loss_and_reentry` | Earlier repeated event identities were missing |
| Closed F-015 on reopened paths | `test_experiment_executes_only_explicit_models_in_order` | Three analytic dispatch-count cases failed; closed-only control passed |
| Swapped comparison direction | `test_comparison_retains_exact_per_replicate_values_and_direction` | Signed support deltas reversed |
| Implicit scenario execution | `test_disabled_scenarios_are_inert_during_audit` | Two execution sentinels fired; partial disabled legacy control passed |
| Raw state identity through a new field | `test_scenario_privacy_preserves_state_alignment_in_all_record_modes` | Raw `reachable_states` failed semantic identity alignment in all three record modes before protected publication |

All ten concrete faults were detected. The privacy result is a semantic
cross-field rejection before construction of `SafeReportView`. No syntax,
import or JSON-shape failure is counted as fault sensitivity. This finite
exercise establishes no exhaustive mutation score and adds no permanent
mutation framework or registry.

## Complete-report performance

The existing CLI measurement fixture now optionally times the actual
`run_scenario_experiment` call. On Linux it reads `/proc/self/status` `VmHWM`
for the executed process, avoiding the fork-parent high-water floor in
`getrusage().ru_maxrss`. Windows and macOS retain their existing platform methods.
Before/after RSS values are whole-process high-water marks, including native
allocations. They are not incremental memory estimates.

Each fresh process executes ordinary audit calculations, requested simulations,
report validation and complete JSON/Markdown publication. Outer wall time also
includes interpreter startup and measurement bookkeeping; the CLI interval begins
before imports and ends after publication. The nested experiment interval
includes admission, sampling, baseline and comparison and excludes report work.
Input preparation and parent-side report assertions are outside those intervals.

Both workloads use two loaded fictional audit records, empty scenario record
membership, two explicitly selected models, seed 17 and lambda `1/4`:

| Workload | States | Horizon | Replicates | Sample size | Combined state cells |
| --- | ---: | ---: | ---: | ---: | ---: |
| Packaged small | 2 | 6 | 3 | 2 | 84 |
| Representative bounded | 32 | 64 | 8 | 64 | 33,280 |

Cells equal `models * states * (horizon + 1) * replicates`. The small vectors are
`(1,0)` and `(0,1)`. The representative initial vector is uniform on the first
16 states, while its external vector is uniform on the last 16; all remaining
masses are literal zero. Scenario cells never substitute for dataset records.

Measured on Linux 6.18.44 x86_64, glibc 2.39, Python 3.12.14, NumPy 2.3.5,
pandas 2.2.3, PyArrow 25.0.1 and pytest 9.1.1. The environment reported
AMD EPYC 9V74 80-Core Processor and nine logical CPUs. Other heavy checks were
paused during measurement. Tracemalloc was disabled for these four observations.
All attempts are listed, rounded to six decimals; no fastest attempt was selected.

| Attempt | Outer wall (s) | CLI (s) | Experiment (s) | Peak RSS (bytes) | JSON bytes | Markdown bytes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Small 1 | 0.365786 | 0.312016 | 0.044696 | 38,694,912 | 163,582 | 139,535 |
| Small 2 | 0.369446 | 0.319516 | 0.044991 | 38,690,816 | 163,581 | 139,534 |
| Small 3 | 0.360281 | 0.310766 | 0.045303 | 38,694,912 | 163,581 | 139,534 |
| Representative 1 | 4.673421 | 4.606455 | 0.088043 | 152,576,000 | 8,229,291 | 194,568 |

Both performance test cases passed in 6.14 seconds. Every attempt exited zero,
published both reports and passed independent path/count/support/diversity,
source-mixture, event-identity and closed-baseline assertions. JSON retains full
paths; Markdown discloses the exact number omitted by each bounded table.
The three small runs reproduce the same simulation evidence in this environment.
No attempt failed or timed out. The 180-second guard is an operational timeout;
this increment creates no new latency or memory SLA and makes no full-capacity
or cross-platform performance claim.

One existing Hero performance test separately checked the shared fixture's
default path: **1 passed in 3.50 seconds**, including three untraced and one
traced attempt. No simulation ran, and its optional simulation timing remained
null. All four observations and original scientific assertions passed.
The [performance README](tests/performance/README.md) records every Hero value,
RSS starting marks, measurement methods and local evidence paths. Observation
JSON retains exact timing precision, input sizes/hashes, environment, exit status
and report sizes; JUnit retains the measurement properties.

## Regression and handoff

The final affected regression passed **576 tests in 21.23 seconds**:

```text
tests/unit/test_reopening_fixture_inputs.py
tests/unit/test_T1_resampling.py
tests/unit/test_T5_reopening.py
tests/unit/test_scenario_experiment.py
tests/unit/test_scenario_report_contract.py
tests/unit/test_scenario_config.py
tests/integration/test_scenario_reports.py
tests/integration/test_scenario_cli.py
tests/integration/test_simulation_example.py
tests/integration/test_scenario_adversarial.py
tests/integration/test_current_verification.py
tests/integration/test_ci_workflows.py
tests/integration/test_no_algorithms.py
tests/integration/test_repository_structure.py
tests/integration/test_no_network.py
```

The three existing source checks and `git diff --check` pass. They confirm 83
protected product files, zero allowed implementation paths, 41 runtime modules,
18 canonical resource copies and 16 frozen specifications. JUnit for the final
affected run is retained at `phase6b_step7_work/affected.xml` in the local workspace.
Earlier focused development checks passed 285 numerical/experiment cases,
12 new adversarial cases and 63 gate/workflow cases; these overlap the final run
and are not added to its total. During adversarial test development, report-field
assertions were aligned with the accepted context shape and protected internal
error classification. No product change was required.

The focused CI selection adds the new adversarial file once. Existing candidate
performance selection already covers the new simulation test; no duplicate job
or additional verification dispatcher is introduced. Product artifacts were not
rebuilt because product bytes are unchanged; Step 6's local installed checks
remain evidence for their named source and environment.

Step 8 retains the dev6 version change, full regression, supported Ubuntu/Windows
and Python 3.11/3.12 matrix, actual optional-dependency absence/presence, security,
100k dataset performance, delivery checks and development handoff. No candidate
acceptance, main merge, tag or registry publication is claimed by Step 7.
