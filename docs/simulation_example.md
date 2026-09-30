# Run and read the synthetic simulation example

The installed example compares a closed categorical process with an explicitly
reopened process. It gives a small case whose first-transition probabilities can
be checked by hand. All scenario results are experimental and carry `simulation`
evidence. The external input and its quality are assumptions supplied by the
caller; this example establishes no empirical intervention effect.

## Install and run

From the current project checkout, install the development package:

```bash
python -m pip install .
rit version
```

The current version remains `0.1.0.dev5`; these instructions do not refer to a
new registry release. Python 3.11 and 3.12 on Ubuntu and Windows are the supported
candidate targets. See [release verification](release_process.md) for the actual
environment evidence and candidate checks.

Then run from any trusted local working directory, choosing a new workspace:

```bash
rit example --dataset simulation --simulate --out ./simulation-workspace
```

The destination must not exist and its parent must already exist. The command
copies four packaged files into `simulation-workspace/inputs/`: `config.json`,
`records.jsonl`, `provenance.jsonl` and `EXPECTED_OUTPUTS.md`. It writes
`report.json` and `report.md` under `simulation-workspace/reports/`. Check the
exit code as well as the files. The independent expectations are in the
extracted `EXPECTED_OUTPUTS.md`.

This dataset requires `--simulate`; it rejects `--lineage`, `--longitudinal`
and a custom `--config`. The ordinary Hero and longitudinal examples retain
their separate interfaces. No runtime download, model, credential or service
is needed. Dependency installation is a separate operation.

## What is declared

| Assumption | Example value | Meaning and limit |
|---|---|---|
| State space | `A`, `B` | Fictional, fixed literal identities shared by both scenarios |
| Initial distribution `p` | `A: 1`, `B: 0` | Explicit scenario probabilities; zero for `B` remains declared |
| External distribution `r` | `A: 0`, `B: 1` | Constant input to each reopened transition; no source-quality inference |
| Reopening weight | `1/4` | External probability weight in the mixture |
| Resample size `n` | `2` | Exactly two categorical draws per transition |
| Horizon | `6` | Six transitions after the supplied initial state |
| Replicates | `3` | Three separate sampled paths per selected model |
| Seed | `17` | Fresh generator with this same seed for each model |
| Scenario scope | `simulation-example-scenario`, version `scenario-v1` | Declared scope labels with empty included/excluded record identities |
| Representation | `explicit_scenario_states`, version `simulation-example-v1` | Caller-declared literal probability-vector states |

The ordinary audit has two separate fictional records with topic states `X`
and `Y` in `audit-v1`. Its support is `2` and its Gini-Simpson diversity is
`1/2`. Those records do not produce `p`, `r` or scenario membership. The scenario
scope's denominator basis is `explicit_scenario_probability_vector`; sample
size `2` does not create two record identities.

At every reopened transition, the current internal frequencies mix with the
same external input:

\[
s_t=(1-\lambda)p_t+\lambda r,\qquad
X_t\sim\operatorname{Multinomial}(n,s_t),\qquad
p_{t+1}=X_t/n.
\]

Closed sampling uses the current internal frequencies alone. Here it starts
entirely in `A`, so every closed sample remains entirely in `A`. Its support
stays `1`; both sampled diversity and the distinct closed analytic expectation
stay `0`.

## Check the first transition

For the first reopened draw,
`(3/4) * (1, 0) + (1/4) * (0, 1) = (3/4, 1/4)`.
With two draws, the complete enumeration is:

| Sample counts `(A, B)` | Probability | Sample diversity | `B` re-enters |
|---|---|---|---|
| `(2, 0)` | `9/16` | `0` | No |
| `(1, 1)` | `6/16` | `1/2` | Yes |
| `(0, 2)` | `1/16` | `0` | Yes |

The mixed source has diversity `3/8`. Expected diversity after this one sample
is `(6/16) * (1/2) = 3/16`. The chance that initially absent `B` re-enters is
`7/16`, with absence still having probability `9/16`. These are exact
first-transition probabilities. Three realized replicates need not reproduce
those proportions or their expectation.

Later transitions use each path's latest sampled frequencies, so their mixed
sources can differ from `(3/4, 1/4)`. State loss and re-entry can recur. A
positive source probability establishes a possibility; a re-entry event also
requires a positive next sampled count. Reopening does not guarantee increasing
diversity at every step. The closed multi-step expectation is attached only to
the closed scenario.

## Read the report

Open `reports/report.md` for assumptions and compact tables. The schema `1.3`
JSON retains the complete bounded numerical evidence:

| JSON path | What to inspect |
|---|---|
| `run.random_seed` | Common recorded seed `17` |
| `simulations.closed_resampling` | Closed sampled paths and replay parameters |
| `simulations.closed_resampling.analytic_baseline` | Separate closed expectation, without an RNG identity |
| `simulations.external_reopening` | Reopened experimental envelope and assumptions |
| `simulations.external_reopening.mixed_sources` | Source distribution and possible re-entry states before each draw |
| `simulations.external_reopening.sampled_paths` | Initial frequencies and realized subsequent counts/frequencies |
| `simulations.external_reopening.state_reentry_events` | Realized `(replicate_index, step, state_id)` events |
| `simulations.external_reopening.extinction_events` | Positive-to-zero transitions, including recurrent losses |
| `simulations.external_reopening.scenario_comparison` | Per-replicate/step values and `reopened_minus_closed` differences |
| `unavailable_conclusions[]`, with `conclusion: empirical_intervention_effect` | Explanation of the empirical evidence still missing |

Read the closed baseline's assumptions and limitations within the scope of that
analytic result. The separately requested reopening calculation and its
limitations belong to the T5 `simulations.external_reopening` envelope.

Each model's `parameters.random_seed` agrees with the run seed. Replay metadata
also retains NumPy version, RNG and sampling method, state order and schedules.
Repeatability applies within the same method and numerical environment;
identical paths across dependency versions or platforms are not promised.
Matching replicate indices provide a reproducible comparison and make no
variance-reduction claim. Report timestamps, duration and protected identities
can differ across otherwise repeated runs.

Simulation `step` is a transition index, independent of dataset versions or a
record's generation metadata. Step zero is the supplied initial distribution:
it has no sampled count vector or transition event. The six transitions produce
seven generations per replicate, including step zero.

## Validate, rerun or change the declarations

Validate the extracted configuration and audit inputs without sampling:

```bash
rit validate --records ./simulation-workspace/inputs/records.jsonl --provenance ./simulation-workspace/inputs/provenance.jsonl --config ./simulation-workspace/inputs/config.json --out ./simulation-validation
```

`validate` leaves `simulations` empty and does not execute the sampler or create
an RNG. That remains true even if a copied config sets `simulation.enabled` to
`true`. The packaged config omits `enabled`, so an ordinary audit with that
config alone also leaves the simulation unrequested. For an explicit rerun:

```bash
rit audit --records ./simulation-workspace/inputs/records.jsonl --provenance ./simulation-workspace/inputs/provenance.jsonl --config ./simulation-workspace/inputs/config.json --simulate --out ./simulation-rerun
```

For your own scenario, copy the extracted config and edit its `simulation`
block. Retain the full representation and meaning declarations, and use scope
labels that describe your scenario. A complete standalone JSON declaration for
the same two-state example is:

```json
{
  "simulation": {
    "models": ["closed_resampling", "reopened_resampling"],
    "seed": 17,
    "state_distribution": {"A": 1, "B": 0},
    "external_input_distribution": {"A": 0, "B": 1},
    "reopening_weight": 0.25,
    "resample_size": 2,
    "simulation_horizon": 6,
    "simulation_replicates": 3,
    "representation": {
      "representation_name": "explicit_scenario_states",
      "representation_source": "declared_probability_vector",
      "representation_version": "simulation-example-v1",
      "binning_or_mapping_rule": "literal_state_id",
      "field_name": null,
      "missing_value_policy": "error",
      "missing_state_id": null,
      "normalization_profile": null
    },
    "state_semantics": "A and B are fictional scenario states with fixed literal identities.",
    "scope_id": "simulation-example-scenario",
    "dataset_version": "scenario-v1"
  }
}
```

Save this as a local config and explicitly provide your own audit records with
`audit --records ... --config ... --simulate --out ...`. Add the appropriate
top-level audit representation and provenance input separately when those
analyses are wanted. Audit records never silently become a scenario vector.
The JSON above is also a valid scenario-only overlay for the Hero or
longitudinal `example --config` interface.

Both probability objects must declare the same state set. A closed-only request
must remove `external_input_distribution` and `reopening_weight`. A complete
block with `enabled: true` requests execution without `--simulate`; an explicit
`enabled: false` conflicts with that flag. Consult the
[configuration contract](simulation_contract.md#5-configuration-and-cli) and
[numerical bounds](simulation_contract.md#2-numerical-policy-and-resource-admission)
before increasing the workload. A refused request is not silently shortened.
Use a fresh destination for each run; existing report targets are never
overwritten. A simulation failure retains independently completed audit results
and a nonzero exit code.

Add `--redacted` to protect state/scope identities, caller text and paths in
reports and diagnostics. It does not rewrite or protect the extracted input
files. Review those separately before sharing a workspace. Configuration hashes
remain linkable. See [privacy boundaries](privacy.md) for the complete policy.
