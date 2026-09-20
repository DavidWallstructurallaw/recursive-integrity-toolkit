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
