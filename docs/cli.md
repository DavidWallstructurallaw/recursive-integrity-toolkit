# CLI

Development version `0.1.0.dev4`, through Phase 6A Step 7, supports `audit`, `validate`, `example`, `version`, `--version` and `--help`. Reports use schema `1.2`. The `recursive-integrity` alias and `python -m recursive_integrity_toolkit` use the same entry point. Help and version do not load analytical dependencies or user inputs.

## Packaged local example

```bash
rit example --out ./hero-workspace
rit example --lineage --out ./hero-lineage-workspace
```

Run after installation from a trusted local directory. The workspace must be new and its parent must already exist. Even an existing empty workspace is rejected. Six exact packaged Hero files are copied under `inputs/`; `report.json` and `report.md` appear under `reports/`. No data download occurs. Add `--redacted` to protect identifiers and paths in reports and console diagnostics. Extracted inputs remain the public canonical Hero files.

Both commands retain support 8 and 5, delta -3, retention 5/8, diversity 7/8 and 3/4, delta -1/8, and missing states `battery`, `lizard`, `turtle`. Later human/synthetic shares are each 1/2 and direct exposure is [1/2, 1/2]. Input observability is Level 4 and default simulations are empty.

With `--lineage`, v2 is the eight-record target and v1 supplies eight ancestor records. All eight targets have resolved external ancestry, supported by five distinct roots. Ancestry HHI is 1/4, effective root count is 4, lineage exposure is [0, 0], and the shared-ancestry proxy is `present`. The report retains the distinction between declared topology and causal evidence. Plain `example` leaves lineage `not_requested`. Both modes use schema 1.2 and preserve the scientific values in the unchanged packaged `inputs/EXPECTED_OUTPUTS.md` oracle.

Explicit series examples are also available:

```bash
rit example --longitudinal --out ./hero-series-workspace
rit example --longitudinal --lineage --redacted --out ./hero-series-lineage-workspace
rit example --dataset longitudinal --longitudinal --out ./three-version-workspace
```

The default dataset is `hero`. Its series mode requests the same two selected snapshots, with separate distribution/provenance/direct summaries and changes. Adding `--lineage` requests both lineage snapshots: supporting roots 8 to 5, HHI 1/8 to 1/4 and effective roots 8 to 4. The `longitudinal` dataset is a separate seven-file JSONL example with support 3 to 2 to 3 and a disappearing/reappearing state. `--dataset longitudinal` requires `--longitudinal`. Neither example enables first-baseline or tail analysis by default. All example destinations follow the same exclusive-workspace rule.

Successful stdout names both report files. In redacted mode the fixed names are relative to the example's `reports/` directory. An audit failure may leave extracted inputs and an error report. Extraction failures clean only files owned by that attempt; incomplete cleanup is disclosed on stderr. Inspect a failed destination and choose a fresh one for retry.

## Audit and validate

After creating the example above, these commands use its local inputs and separate destinations:

```bash
rit validate --records ./hero-workspace/inputs/records_v2.csv --out ./validation-report
rit audit --records ./hero-workspace/inputs/records_v2.csv --config ./hero-workspace/inputs/config.json --out ./topic-report
rit audit --records ./hero-workspace/inputs/records_v2.csv --config ./hero-workspace/inputs/config.json --tail-rule singleton_count --out ./tail-report
rit audit --records ./hero-workspace/inputs/records_v2.csv --config ./hero-workspace/inputs/config.json --redacted --record-ids omit --out ./redacted-report
```

Only `--records` is mandatory. CSV, UTF-8 JSONL and optional Parquet follow the accepted input rules. Config is JSON or TOML. Config paths resolve relative to the config file and CLI paths relative to the working directory. Environment variables and `~` are literal text. These commands do not resolve content references.

Audit calculates only an explicitly declared representation. A field config has this form:

```json
{
  "representation": {
    "name": "declared-topic",
    "source": "topic_field",
    "field": "topic",
    "version": "1",
    "missing_value_policy": "exclude"
  }
}
```

Without a representation, audit retains input/provenance evidence and explains unavailable representation-dependent analyses. Exact-content analysis needs `source: content_hash`, an explicit name/version and `normalization_profile: exact_utf8_v1`; its canonical field is `content` and its missing policy is `error`. It reports record-form support and exact duplicates. Neither field nor hash states certify semantic validity.

| Option | Contract |
|---|---|
| `--provenance`, `--config`, `--schema-mapping`, `--version-order` | Explicit local input/control files |
| `--out DIR` | Default `./rit-report`; parent must exist; targets never overwritten |
| `--redacted` | Protect full paths and nested identifiers across output sinks |
| `--record-ids preserve\|hash\|omit` | Requires redacted output; default `hash` there |
| `--id-salt-file PATH` | Requires redacted mode; local 32-4096 byte secret for cross-run identifier stability |
| `--strict` | Promote only configured `strict_warning_codes` |
| `--missing-state-id TEXT` | Required exactly for `explicit_missing_state`; collisions fail |
| `--tail-rule singleton_count` | Audit only; rejects a threshold |
| `--tail-rule count_at_or_below --tail-threshold N` | Audit only; nonnegative integer |
| `--tail-rule frequency_at_or_below --tail-threshold P` | Audit only; finite number in [0,1] |
| `--compare FILE` | One earlier input in ordinary audit; repeatable for series audit and input-only validate |
| `--state-semantics TEXT` | Explicit shared literal meaning for a pair or common-representation series |
| `--longitudinal` | Audit/example only; explicitly request ordered selected snapshot comparisons |
| `--baseline none\|first` | Audit only; requires longitudinal enablement; default `none` |
| `--lineage` | Audit/example only; explicitly execute the validated parent graph and ancestry families |
| `--lineage-records PATH` | Repeatable audit/validate context input; audit requires lineage opt-in |

Repeated singleton flags and competing CLI/config singleton declarations fail even if values match. `--lineage-records` is repeatable. Config output allows only `directory`, `record_id_mode` and `id_salt_file`. The CLI performs unweighted calculations even when weights are present and applies no implicit representation, tail threshold or simulation. Debug output, simulation requests and state-list tail selection are unsupported. Directed series maps use the complete declarative contract below.

An ordinary audit requires one primary dataset version. Multiple versions in a calculated side cause an input error without pooling or choosing one. Validate can inspect multiple versions through `--records`, repeated `--compare` and repeated `--lineage-records`; it rejects explicit lineage, longitudinal, state-semantics and tail execution requests. Inert `longitudinal` config is accepted, including `enabled: true`, without analytical execution. Its `derived_metrics` contains only the schema's unrequested series metadata; `proxy_signals` and `simulations` stay empty. Empty/malformed input can produce an error-only report. Missing provenance never becomes supplied unknown or fabricated source evidence.

## Explicit lineage and context

The extracted Hero inputs can run ancestry without requesting a comparison:

```bash
rit audit --records ./hero-workspace/inputs/records_v2.csv --lineage --lineage-records ./hero-workspace/inputs/records_v1.csv --provenance ./hero-workspace/inputs/provenance.csv --version-order ./hero-workspace/inputs/version_order.json --config ./hero-workspace/inputs/config.json --out ./lineage-report
rit validate --records ./hero-workspace/inputs/records_v2.csv --lineage-records ./hero-workspace/inputs/records_v1.csv --provenance ./hero-workspace/inputs/provenance.csv --version-order ./hero-workspace/inputs/version_order.json --out ./lineage-input-check
```

Repeat `--lineage-records` for additional local context files. CSV, JSONL and optional Parquet use the existing local table loaders. A context file may contain multiple context versions. Context versions must be disjoint from the primary and comparison versions; duplicate composite keys across context inputs fail. Keep same-version ancestors in the primary records file. Splitting one version between primary/comparison and context roles is unsupported. The provenance manifest may describe all loaded versions.

Ordinary ancestry targets exactly the primary `--records` version; `--longitudinal --lineage` requests every selected snapshot. Context contributes ancestors and appears in input inventory, graph scope and diagnostics. It does not enlarge selected target denominators. Adding `--lineage` to an explicit pair lets the existing comparison input also supply ancestors. Context alone never requests comparison or state compatibility, and parent chronology still requires explicit declarations where needed.

JSON/TOML config can declare `lineage: true`, repeated `inputs.lineage_context`, and the four finite graph limits. For example, a JSON config relative to its own directory may include:

```json
{
  "lineage": true,
  "inputs": {
    "lineage_context": ["ancestors_v1.jsonl", "ancestors_v0.csv"]
  },
  "resource_limits": {
    "max_lineage_nodes": 200000,
    "max_lineage_edges": 1000000,
    "max_lineage_root_memberships": 1000000,
    "max_lineage_root_union_visits": 10000000
  }
}
```

These are the defaults. Each override must be a positive integer; null, booleans and fractional values fail. They bound admitted nodes, unique edges, logical record/root memberships and candidate root-union visits. Existing input byte/row/parent-list limits remain separate. The limits do not guarantee a peak memory budget. Exhaustion produces a lineage error and unavailable dependent values; independently completed ordinary metrics survive. A cycle anywhere in the loaded graph remains an error, even if primary ancestry is unaffected.

CLI context declarations extend the configured context list. Declare the lineage opt-in once, through either config or the CLI; an explicit config `lineage` value together with `--lineage` is a conflicting singleton declaration.

`validate` accepts context declarations with lineage disabled, performs existing input and immediate-reference validation, and never runs graph metrics. Both `--lineage` and config `lineage: true` are rejected for `validate`. Config parsing and the Python `validate_bundle` function also remain input-only. `--strict` promotes only configured warning codes, including a configured missing-parent warning; ordinary unresolved ancestry remains explicit in coverage and bounds.

Use `--redacted` for protected context paths, dataset labels, roots and cycle witnesses. `--record-ids omit` removes identity-bearing lineage detail collections while retaining counts, values and omission reasons. Resource failures and validation errors retain severity in both report formats and stderr.

## Explicit earlier/later pair

```bash
rit audit --records ./hero-workspace/inputs/records_v2.csv --compare ./hero-workspace/inputs/records_v1.csv --provenance ./hero-workspace/inputs/provenance.csv --config ./hero-workspace/inputs/config.json --version-order ./hero-workspace/inputs/version_order.json --state-semantics "Hero topic labels retain their literal meaning across v1 and v2." --out ./pair-report
```

Each file must contain exactly one distinct dataset version. `--compare` explicitly identifies the earlier side and `--records` the later side. An order document uses accepted `version_order`, `version_rank` or `version_timestamps` fields and must agree with that relation. The established two-version invocation-order contract remains supported in ordinary pair mode. Filenames and lexical labels never supply chronology.

The shared representation comes from config. `--state-semantics` records the caller's declaration that literal states mean the same thing in both versions. Matching representation labels alone do not establish semantic compatibility, and the declaration does not authenticate semantic truth.

Both versions receive support/diversity values. The pair adds support delta, retention, diversity delta and lost/added/retained state sets and counts. Provenance composition, direct bounds, exact-content duplicate summary and any requested tail describe the later `--records` side. Envelopes keep their scope and denominator. Input inventory and input observability cover both files.

A completed ordinary pair still has `dataset_longitudinal.execution_status: partial`, because its scope remains limited to support/diversity; this alone does not make the run fail. Its separate series execution remains `not_requested`. Invalid chronology or representation gives a nonzero exit while preserving independently valid single-version results. Revalidation after a chronology error makes no replacement ordering claim. A rejected chronology file remains input evidence. Same-version sides are rejected. Ordinary pair mode does not schedule a series or calculate provenance/lineage changes.

## Explicit ordered series

After extracting the separate three-version example, this requests adjacent and first-baseline pairs:

```bash
rit audit --records ./three-version-workspace/inputs/records_v3.jsonl \
  --compare ./three-version-workspace/inputs/records_v1.jsonl \
  --compare ./three-version-workspace/inputs/records_v2.jsonl \
  --config ./three-version-workspace/inputs/config.json \
  --provenance ./three-version-workspace/inputs/provenance.jsonl \
  --version-order ./three-version-workspace/inputs/version_order.json \
  --longitudinal --baseline first --out ./series-baseline-report
```

Each selected primary/comparison file must identify one nonempty version, distinct from every other selected file. The primary is latest among selected versions. Context versions and unloaded labels in an order document stay outside snapshot membership. Series chronology requires explicit config/order-file declarations, including accepted timezone-aware timestamp declarations with existing tie/conflict rules. Repeated path order cannot establish chronology. Ordinary audit accepts at most one comparison file; input-only validate accepts repeated comparisons without enabling series execution.

The default schedule has `k - 1` adjacent pairs. `--baseline first` also requests first-to-later pairs, deduplicating the first adjacent pair. A failed middle pair stays visible and is never replaced by a skipped-version comparison. Snapshot observations remain available where valid. Required families are distribution, provenance and direct closure; tail and lineage run only when requested. Missing provenance remains missing evidence. Representation incompatibility blocks the affected pair and gives a nonzero exit. Primary ordinary summaries reuse their selected snapshot evidence; the old singular-pair slot is never filled with an arbitrary series pair.

Common mode uses the top-level `representation` plus one meaning declaration from `longitudinal.state_semantics` or `--state-semantics`:

```json
{
  "representation": {
    "name": "topic",
    "source": "topic_field",
    "field": "topic",
    "version": "topics-v1",
    "missing_value_policy": "exclude"
  },
  "longitudinal": {
    "enabled": true,
    "baseline": "none",
    "state_semantics": "Literal topic meanings are shared across selected versions."
  },
  "resource_limits": {"max_longitudinal_versions": 100}
}
```

With this config, omit `--longitudinal` and `--state-semantics` because the config already declares them. CLI/config singleton declarations compete even when equal. Comparison inputs may repeat within CLI or config declarations; the two comparison sources cannot be combined. The version limit is a positive built-in integer, rejects null/boolean/fractional values, and is checked before snapshot calculation. Selection is never truncated to fit it.

Per-version mode supplies `longitudinal.versions` with exactly one entry per selected version. Each entry contains `dataset_version`, a complete existing `representation` object, `state_semantics`, and `missing_state_id` exactly when its policy is `explicit_missing_state`. Common representation, common semantics and common missing-state declarations are rejected in that mode. Optional `longitudinal.mappings` name the earlier/later endpoints of scheduled pairs and include direction, full source/target descriptors, both state meanings and a literal `state_mapping` object. Maps must cover every supplied source state; they are never composed across pairs. Legacy bare `state_mapping` and `representation_compatibility` cannot substitute for these declarations. See the [exact configuration shapes](longitudinal_contract.md#2-configuration-and-cli-contract).

Config parsing stays inert. Audit rejects nondefault series execution declarations when enablement is false. Validate accepts the inert object even when enabled, checks its structure and loads inputs without running the series; explicit execution flags remain unsupported. `--lineage` plus series builds the supplied graph once for all selected targets. Context still requires lineage opt-in for audit. Partial ancestry, resource exhaustion and incompatible pairs retain exact reasons, coverage and nulls. No fitted trend, relative-change formula or simulation is added.

## Reports, diagnostics and exits

All twelve report sections remain present in JSON and Markdown. Success emits one stdout JSON line containing final report paths. Redacted mode emits fixed filenames relative to the selected output directory. Warnings and errors appear as content-safe structured stderr entries. Report and console diagnostics retain their code, severity, counts and safe locations; distinct warning contexts remain distinct.

Warnings carry an `affected_scope` summary of versions, record/exclusion counts, denominator basis and scope ID. Full input identities remain in `inputs.scope` when the selected privacy mode permits them. This avoids repeating all record identities in every warning while retaining diagnostic locations and meaning.

| Exit | Meaning |
|---|---|
| 0 | Supported work completed without error-severity diagnostics |
| 1 | Input/validation, representation incompatibility, resource-limit or output I/O failure |
| 2 | Invalid invocation/configuration or unsupported request |
| 3 | Immediate-parent format/resolution or lineage-cycle error |
| 4 | Internal or invariant failure |

Precedence is 4, then 2, then 3, then 1. Warnings alone return 0 unless configured strict promotion applies. Deferred/optional unavailable analyses alone do not cause a partial run. A report may contain useful results despite a nonzero exit, so file presence is insufficient to establish success.

Parser errors use safe stderr. Other fatal failures attempt a protected, schema-conforming error-only pair when the destination is safe. If config resolution fails, the explicit CLI destination or local default is used with fresh redacted/omit protection. No traceback, raw input content, secret material or full configuration is emitted.

`run.duration_seconds` stops after input/calculation work and before assembly/publication. Use externally recorded complete-process timings for end-to-end performance. The network count covers `toolkit_managed_outbound_operations`; it is not an operating-system network monitor.

## Publication boundary

The output directory's existing ancestors must be stable and trusted. Ordinary audit/validate may use a new leaf or an existing directory with neither report target present. Existing `report.json` or `report.md` always causes failure. URI/UNC/device paths, unsupported path spellings, symlink/reparse paths, source aliases and unsafe targets are rejected. There is no overwrite option.

The Python helper `utils.paths.publish_reports(safe_view, output_directory, input_paths=...)` consumes a validated `SafeReportView`; supply every input path, including declared missing inputs. A `complete` result means both exact reports were verified and private staging removed. `E_OUTPUT_PATH_INVALID` maps to exit 2; collision, existing/unsafe target, I/O or cleanup failure maps to 1; rendering/invariant failure maps to 4.

Handled partial failures clean only files still identified as belonging to the attempt. An `incomplete` result discloses remaining or uncertain cleanup. Pair publication is not a filesystem transaction: another reader or process crash may observe one report before the other. See [privacy and filesystem limits](privacy.md) for platform permissions and race/crash boundaries. HTML and simulation orchestration remain deferred. Phase 6A Step 8 scale preparation and Step 9 candidate verification have not started.
