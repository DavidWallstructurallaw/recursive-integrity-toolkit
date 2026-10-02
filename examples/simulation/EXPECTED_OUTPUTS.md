# Synthetic simulation example: independent expectations

This is a fully fictional teaching fixture. Its two local audit records and
complete provenance declarations are supplied example data. The declarations
do not document independently verified origins. The scenario uses separately
declared states A and B; the audit topics X and Y never determine its inputs.

## Run and replay

From an installed package, in a directory whose parent already exists:

```bash
rit example --dataset simulation --simulate --out ./simulation-workspace
```

The command creates a new workspace containing these four unchanged input
files and `reports/report.json` plus `reports/report.md`. An existing workspace
is never overwritten. This fixture requires `--simulate` and rejects
`--config`, `--lineage` and `--longitudinal`. To change the experiment, copy and
edit the extracted config, then use `rit audit --simulate` with that config and
the explicit audit input paths. The packaged config omits `simulation.enabled`;
without explicit activation it remains input-only scenario material.

Replay requires the same inputs, seed, model version, sampler identity, NumPy
version and numerical platform. Stochastic arrays are reproducible in a
matched environment; no exact sampled path is promised across NumPy versions
or platforms. Report timestamps, run IDs and paths also vary. No network access
is needed for this example after installation.

## Independent audit expectations

| Item | Expected value |
|---|---:|
| Dataset version | `audit-v1` |
| Record count | 2 |
| Topic counts | X: 1, Y: 1 |
| Topic support | 2 |
| Gini-Simpson diversity | 1/2 |
| Provenance row coverage | 1 |
| Declared synthetic share | 1 |
| Direct closure lower and upper bounds | 1, 1 |

The provenance rows explicitly declare synthetic generation with no external
grounding and empty parent lists. These audit facts have their own two-record
scope and do not establish any empirical effect of reopening.

## Scenario declarations and assumptions

| Declaration or assumption | Explicit choice |
|---|---|
| Model order | `closed_resampling`, `reopened_resampling` |
| Initial distribution p | A: 1, B: 0 |
| Constant external distribution r | A: 0, B: 1 |
| Reopening weight lambda | 1/4 |
| Sample size n | 2 |
| Horizon | 6 transitions, with step 0 retained |
| Replicates | 3 per model |
| Common seed | 17 |
| RNG schedule | Fresh PCG64 with the same seed for each model |
| Sampling law | Multinomial draws of size n from each current source |
| Reopened source | (1 - lambda) times current distribution + lambda times r |
| State identities | Fixed literal categories A and B |
| Representation | `explicit_scenario_states`, version `simulation-example-v1` |
| Scope | `simulation-example-scenario`, version `scenario-v1` |
| Scope record membership | Empty included and excluded record lists |
| Scope denominator basis | `explicit_scenario_probability_vector` |

Each sampled step has integer counts summing to 2 and probabilities equal to
counts divided by 2. Step 0 is the declared starting probability vector. The
report records three paths with seven steps per selected model, model and RNG
metadata, source and sampled distributions, support/diversity, extinction and
re-entry events, and per-step reopened-minus-closed comparisons. The shared
seed schedule provides matched experiment declarations; it does not make the
models' individual draws a causal pairing or a confidence interval.

## Closed result and analytic baseline

The closed model starts at p=(1,0). Every draw contains two A observations, so
A remains present and B remains absent at every step. Support is exactly 1 and
Gini-Simpson diversity is exactly 0 in every replicate. No closed extinction
event occurs because B was already absent at step 0.

The closed analytic diversity baseline is

```text
D(p) = 1 - (1^2 + 0^2) = 0
E[D(p_t)] = (1 - 1/n)^t D(p_0) = (1/2)^t * 0 = 0
```

This identity concerns the closed model's expected diversity under the stated
finite multinomial process.

## First reopened transition: exact arithmetic

The following rational expectations are independently authored from the
declared source and the binomial law. They are not sampled-output snapshots.

```text
q_0 = (3/4)(1,0) + (1/4)(0,1) = (3/4,1/4)
D(q_0) = 1 - ((3/4)^2 + (1/4)^2) = 3/8
```

| Sample counts (A, B) | Probability | Sampled diversity |
|---|---:|---:|
| (2, 0) | 9/16 | 0 |
| (1, 1) | 6/16 | 1/2 |
| (0, 2) | 1/16 | 0 |

Thus the expected first sampled diversity is `(6/16)(1/2) = 3/16`.
Source diversity `3/8` and expected sampled diversity `3/16` are different
quantities. With only three replicates, the observed sample mean may differ
from `3/16`.

B has positive source mass at the first reopened transition. The probability
that it appears in that first sample is `1 - (3/4)^2 = 7/16`. The probability
that it is still absent is `9/16`. Reported possible re-entry identifies this
positive-probability route; an actual re-entry event requires positive B
counts after its prior absence. Reopening therefore permits B to return while
any particular sample can still contain only A.

Later reopened source distributions depend on the previously sampled state.
The three possible current distributions produce these next sources:

| Current distribution (A, B) | Next reopened source (A, B) |
|---|---|
| (1, 0) | (3/4, 1/4) |
| (1/2, 1/2) | (3/8, 5/8) |
| (0, 1) | (0, 1) |

Under this particular r, loss of A cannot be reversed by external input.
Both the closed and reopened models permit absorbing outcomes under these
specific declarations. A particular reopened path can have zero diversity.

## Interpretation

Scenario nodes are explicitly `experimental` with evidence class `simulation`.
The report's simulation capability completes only after these kernels run.
No empirical intervention effect, model-performance effect, universal
integrity score, or universal collapse prediction follows from this fixture.
The independently reported audit statistics retain their original evidence
classes. Use `validate` on the extracted files to check declarations without
sampling; it produces no simulation result.
