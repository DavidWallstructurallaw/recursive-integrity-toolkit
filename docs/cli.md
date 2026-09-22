# CLI

Development version `0.1.0.dev3` supports `audit`, `validate`, `example`, `version`, `--version` and `--help`. The `recursive-integrity` alias and `python -m recursive_integrity_toolkit` use the same entry point. Help and version do not load analytical dependencies or user inputs.

## Packaged local example

```bash
rit example --out ./hero-workspace
```

Run after installation from a trusted local directory. The workspace must be new and its parent must already exist. Even an existing empty workspace is rejected. Six exact packaged Hero files are copied under `inputs/`; `report.json` and `report.md` appear under `reports/`. No data download occurs. Add `--redacted` to protect identifiers and paths in reports and console diagnostics. Extracted inputs remain the public canonical Hero files.

The copied `inputs/EXPECTED_OUTPUTS.md` includes full-product lineage targets. Phase 4 reports explicitly defer lineage calculation. Their current targets are support 8 and 5, delta -3, retention 5/8, diversity 7/8 and 3/4, delta -1/8, and missing states `battery`, `lizard`, `turtle`. Later human/synthetic shares are each 1/2 and direct exposure is [1/2, 1/2]. Input observability is Level 4 and default simulations are empty.

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
| `--compare FILE` | One earlier-version records file; current records are the later side |
| `--state-semantics TEXT` | Audit pair only; explicit shared literal meaning across both sides |

Repeated flags and competing CLI/config singleton declarations fail even if values match. Config output allows only `directory`, `record_id_mode` and `id_salt_file`. The CLI performs unweighted calculations even when weights are present and applies no implicit representation, tail threshold or simulation. Debug output, simulation requests, state-list tail selection and arbitrary state maps are unsupported.

An ordinary audit requires one dataset version. Multiple versions in a side cause an input error without pooling or choosing one. Validate can inspect multiple versions and two files through `--records`/`--compare`; it rejects state-semantics and tail requests. Its `derived_metrics`, `proxy_signals` and `simulations` stay empty. Empty/malformed input can produce an error-only report. Missing provenance never becomes supplied unknown or fabricated source evidence.

## Explicit earlier/later pair

```bash
rit audit --records ./hero-workspace/inputs/records_v2.csv --compare ./hero-workspace/inputs/records_v1.csv --provenance ./hero-workspace/inputs/provenance.csv --config ./hero-workspace/inputs/config.json --version-order ./hero-workspace/inputs/version_order.json --state-semantics "Hero topic labels retain their literal meaning across v1 and v2." --out ./pair-report
```

Each file must contain exactly one distinct dataset version. `--compare` is earlier and `--records` later, and declared chronology must confirm that relation. An order document uses accepted `version_order`, `version_rank` or `version_timestamps` fields. Filenames, argument order and lexical labels cannot supply chronology.

The shared representation comes from config. `--state-semantics` records the caller's declaration that literal states mean the same thing in both versions. Matching representation labels alone do not establish semantic compatibility, and the declaration does not authenticate semantic truth.

Both versions receive support/diversity values. The pair adds support delta, retention, diversity delta and lost/added/retained state sets and counts. Provenance composition, direct bounds, exact-content duplicate summary and any requested tail describe the later `--records` side. Envelopes keep their scope and denominator. Input inventory and input observability cover both files.

A completed pair still has `dataset_longitudinal.execution_status: partial`, because other change families remain deferred; this alone does not make the run fail. Invalid chronology or representation gives a nonzero exit while preserving independently valid single-version results. Revalidation after a chronology error makes no replacement ordering claim. A rejected chronology file remains input evidence. Same-version sides are rejected. No automatic pairing, version trajectory, provenance/lineage trend, arbitrary map, relative-change formula or simulation runs.

## Reports, diagnostics and exits

All twelve report sections remain present in JSON and Markdown. Success emits one stdout JSON line containing final report paths. Redacted mode emits fixed filenames relative to the selected output directory. Warnings and errors appear as content-safe structured stderr entries. Report and console diagnostics retain their code, severity, counts and safe locations; distinct warning contexts remain distinct.

Warnings carry an `affected_scope` summary of versions, record/exclusion counts, denominator basis and scope ID. Full input identities remain in `inputs.scope` when the selected privacy mode permits them. This avoids repeating all record identities in every warning while retaining diagnostic locations and meaning.

| Exit | Meaning |
|---|---|
| 0 | Supported work completed without error-severity diagnostics |
| 1 | Input/validation or output I/O failure |
| 2 | Invalid invocation/configuration or unsupported request |
| 3 | Existing immediate-parent/lineage-family validation error |
| 4 | Internal or invariant failure |

Precedence is 4, then 2, then 3, then 1. Warnings alone return 0 unless configured strict promotion applies. Deferred/optional unavailable analyses alone do not cause a partial run. A report may contain useful results despite a nonzero exit, so file presence is insufficient to establish success.

Parser errors use safe stderr. Other fatal failures attempt a protected, schema-conforming error-only pair when the destination is safe. If config resolution fails, the explicit CLI destination or local default is used with fresh redacted/omit protection. No traceback, raw input content, secret material or full configuration is emitted.

`run.duration_seconds` stops after input/calculation work and before assembly/publication. Use externally recorded complete-process timings for end-to-end performance. The network count covers `toolkit_managed_outbound_operations`; it is not an operating-system network monitor.

## Publication boundary

The output directory's existing ancestors must be stable and trusted. Ordinary audit/validate may use a new leaf or an existing directory with neither report target present. Existing `report.json` or `report.md` always causes failure. URI/UNC/device paths, unsupported path spellings, symlink/reparse paths, source aliases and unsafe targets are rejected. There is no overwrite option.

The Python helper `utils.paths.publish_reports(safe_view, output_directory, input_paths=...)` consumes a validated `SafeReportView`; supply every input path, including declared missing inputs. A `complete` result means both exact reports were verified and private staging removed. `E_OUTPUT_PATH_INVALID` maps to exit 2; collision, existing/unsafe target, I/O or cleanup failure maps to 1; rendering/invariant failure maps to 4.

Handled partial failures clean only files still identified as belonging to the attempt. An `incomplete` result discloses remaining or uncertain cleanup. Pair publication is not a filesystem transaction: another reader or process crash may observe one report before the other. See [privacy and filesystem limits](privacy.md) for platform permissions and race/crash boundaries. HTML, general ancestry and simulation orchestration remain deferred.
