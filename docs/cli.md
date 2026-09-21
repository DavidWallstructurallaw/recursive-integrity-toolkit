# CLI (Phase 4 Step 7)

Current commands: `audit`, `validate`, `version`, `--version` and `--help`.
The `recursive-integrity` alias and `python -m recursive_integrity_toolkit` use
the same entry point. Comparison and packaged `example` require Step 8.

```bash
rit audit --records ./records.csv --out ./audit-report
rit validate --records ./records.csv --out ./validation-report
rit audit --records ./records.csv --config ./config.json --out ./audit-topic
rit audit --records ./records.csv --config ./config.json --tail-rule singleton_count --out ./audit-tail
rit audit --records ./records.csv --config ./config.json --redacted --out ./audit-redacted
```

Only `--records` is mandatory. CSV, UTF-8 JSONL and optional-Parquet inputs use the
accepted input validation rules. Supply local paths explicitly. Config paths are
relative to the config file; CLI paths are relative to the working directory.
There is no environment-variable or home-directory expansion. Local content
reference reading is never activated by these commands.

An example explicit field declaration in JSON config:

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

Without a representation, audit produces input/provenance evidence and explains
unavailable representation-dependent analyses. No default topic or content hash
is selected. Exact-content analysis requires `source: content_hash`, an explicit
name/version and `normalization_profile: exact_utf8_v1`; its canonical field is
content and its missing policy is error. It reports record-form support and exact
duplicates. Neither field nor hash states establish semantic validity.

| Options | Contract |
|---|---|
| `--provenance`, `--config`, `--schema-mapping`, `--version-order` | Explicit local inputs; config is JSON or TOML |
| `--out DIR` | Default `./rit-report`; its parent must exist |
| `--redacted` | Protect full paths and nested identifiers across all sinks |
| `--record-ids preserve|hash|omit` | Requires redacted output; default hash in redacted mode |
| `--id-salt-file PATH` | Requires redacted mode; explicit local 32-4096 byte secret for cross-run identifiers |
| `--strict` | Promote only configured `strict_warning_codes` |
| `--missing-state-id TEXT` | Required exactly for `explicit_missing_state`; collisions fail |
| `--tail-rule singleton_count` | Audit only; rejects a threshold |
| `--tail-rule count_at_or_below --tail-threshold N` | Audit only; nonnegative integer |
| `--tail-rule frequency_at_or_below --tail-threshold P` | Audit only; finite value in [0,1] |
| `--compare`, `--state-semantics`, `example` | Unsupported until Step 8 |

Competing CLI/config singleton declarations and repeated flags fail, even if
values match. Config output permits only `directory`, `record_id_mode` and
`id_salt_file`. Debug output, simulations and state mappings are unsupported.
The CLI performs disclosed unweighted calculations even if input weights exist.
It applies no default tail threshold, state-list selection or simulation.

Audit requires one dataset version. Multiversion inputs retain valid inventory
and counts but return an input error without pooling or choosing a version.
Validate can inspect multiversion inputs; its derived-metric, proxy-signal and
simulation sections remain empty. Both commands retain all twelve report sections.
An absent manifest leaves direct closure bounds unavailable. Empty or malformed
inputs can produce an error-only report, without invented versions or values.

Reports are `report.json` and `report.md`, published through the accepted safe
paired-output helper. Existing targets and unsafe paths fail without replacement.
Success prints one JSON line containing final paths. Redacted mode prints the two
fixed filenames relative to the selected output directory, omitting full paths.
Warnings/errors are safe structured stderr entries. Failure may preserve useful
partial evidence; a nonzero exit must be checked even when reports exist.

| Exit | Meaning |
|---|---|
| 0 | Supported work completed, no error-severity diagnostics |
| 1 | Input/validation or output IO failure |
| 2 | Invalid invocation/configuration or unsupported request |
| 3 | Existing validated lineage-family error |
| 4 | Internal or invariant failure |

Precedence is 4, then 2, then 3, then 1. Warnings alone return 0 unless configured
strict promotion applies. Deferred lineage or optional unavailable analyses do
not alone make a report partial. Invalid parser declarations emit safe stderr.
Other fatal failures attempt a protected, schema-conforming error-only pair when
the destination is safe. If config resolution failed, the explicit CLI destination
or local default is used with a fresh redacted/omit context. No traceback, raw
input content, salt material or full configuration is emitted.

Run duration is captured after input/calculation work, before report assembly
and publication. End-to-end performance acceptance belongs to Step 10.

The reported network count covers toolkit-managed outbound operations. It is not
an operating-system network monitor. See the retained output-helper notes below
and `privacy.md` for publication race/crash limits.

## Historical notes through Step 6

The following original documentation records the earlier accepted stages.

# CLI

Status: Phase 1 scaffold.

Available commands:

```bash
rit --help
rit version
python -m recursive_integrity_toolkit --help
python -m recursive_integrity_toolkit version
```

The CLI reports scaffold status only. It does not load datasets or produce analytical audit results in Phase 1.

## Phase 4 Step 6: output helper available for later CLI wiring

The CLI remains at its previously accepted behavior. This step adds the Python
publication helper; CLI analysis and audit commands require Step 7 authorization.

```python
from recursive_integrity_toolkit.utils.paths import publish_reports
from recursive_integrity_toolkit.utils.logging import emit_publication_diagnostic

# safe_view is the already constructed, validated SafeReportView.
result = publish_reports(safe_view, "./output/run-001", input_paths=(records_path,))
if result.status != "complete":
    emit_publication_diagnostic(result, stream=error_stream)
```

Supply every caller input path explicitly, including declared inputs that do not
currently exist. The parent directory must exist; the final output directory may
be new or may already exist with neither report target present. The only final
names are `report.json` and `report.md`, containing the exact accepted renderer
UTF-8 bytes. Existing targets cause a failure and remain untouched. No force or
overwrite option exists. Input path validation does not open source contents.

| Result | Meaning | Exit code |
|---|---|---|
| `complete` | Both exact outputs verified and private staging removed | 0 |
| `E_OUTPUT_PATH_INVALID` | Invalid or unsupported local path spelling/configuration | 2 |
| `E_OUTPUT_INPUT_COLLISION`, `E_OUTPUT_EXISTS`, `E_OUTPUT_UNSAFE`, `E_OUTPUT_IO` | Reserved input collision, existing target, unsafe filesystem path or IO failure | 1 |
| `E_OUTPUT_CLEANUP` | Published outputs remain but staging cleanup is incomplete | 1 |
| `E_OUTPUT_RENDER`, `E_OUTPUT_INTERNAL` | Rendering validation or an internal invariant failed | 4 |

On handled partial failures, only files still identified as belonging to the
attempt are removed. `failed` means no known attempt output/staging remains;
`incomplete` signals remaining or uncertain cleanup, even when both reports are
present. `published_files` is publication history, not current directory state.
`residual_files` contains only the two fixed output names when their cleanup is
unconfirmed; `temporary_cleanup_complete` separately covers private staging.
A conflicting file owned by someone else is not listed as this attempt's file.

Treat failure as a failed operation, inspect incomplete destinations, and choose
a fresh explicit directory. Do not claim pair atomicity, durable completion after
power loss or protection from hostile ancestor swaps. See `privacy.md` for the
supported filesystem boundary. The result and diagnostic are operational data;
they are not inserted into the canonical report or used to change its conclusions.
