# Three-version longitudinal example

This compact local example follows topic support, diversity, provenance coverage
and direct closure intervals through three supplied snapshots. It contains 11
records and 10 provenance rows. The missing row for `v2::r4` is intentional.

After installing the toolkit, run from any directory:

```bash
rit example --dataset longitudinal --longitudinal --out ./longitudinal-demo
```

Use a new output directory whose parent already exists. The command extracts
packaged inputs and the independent expected values into
`longitudinal-demo/inputs/`, and writes JSON and Markdown to
`longitudinal-demo/reports/`. Add `--redacted` to protect report identifiers and
paths, or `--lineage` to request ancestry for all three snapshots.

For a checkout, the equivalent explicit audit is:

```bash
rit audit \
  --records examples/longitudinal/records_v3.jsonl \
  --compare examples/longitudinal/records_v1.jsonl \
  --compare examples/longitudinal/records_v2.jsonl \
  --provenance examples/longitudinal/provenance.jsonl \
  --version-order examples/longitudinal/version_order.json \
  --config examples/longitudinal/config.json \
  --longitudinal \
  --out ./longitudinal-report
```

The primary file is the latest selected snapshot. Repeated comparison arguments
identify the other snapshots; `version_order.json` supplies chronology. The
configuration declares the common topic representation and literal category
meaning. The CLI flag explicitly enables execution.

The default reports adjacent changes `v1 -> v2` and `v2 -> v3`. Add
`--baseline first` to the audit command to include `v1 -> v3`; the already
adjacent `v1 -> v2` pair appears once with both kinds. Add
`--tail-rule singleton_count` to select each earlier snapshot's singleton
states for that pair. Neither option is implicit.

The intentional missing provenance row produces `W_PROVENANCE_MISSING_ROW`.
Coverage and interval fields retain the gap. Inspect family execution statuses
alongside values. The example does not establish model performance, causal
effects or a forecast.

See [EXPECTED_OUTPUTS.md](EXPECTED_OUTPUTS.md) for exact fractions and state sets.
These inputs copy the independently authored Phase 6A acceptance case
`observed_three_version`. The existing Hero example remains available as
`rit example --out ./hero-demo` and
`rit example --longitudinal --out ./hero-series-demo`.
