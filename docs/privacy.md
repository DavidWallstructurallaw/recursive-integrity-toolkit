# Privacy

Status: Phase 2 Step 7 input-security boundary.

Core behavior is local-first. Importing the package must not contact a network, load user content, create a service, or require the optional Parquet dependency.

The controlling privacy specification is `PRIVACY_AND_DATA_HANDLING.md`.

## Phase 2 Step 3 mapping boundary

Compiling and applying a declaration operate on supplied plain data. They do
not open files, call a network, execute commands, discover plugins, resolve
attribute paths or read environment variables. Only the explicit `load_mapping`
entry point reads its declared local mapping file using the Step 2 byte-snapshot
reader and its configured limits. URLs inside fields and constants are inert.

Mapping diagnostics carry section, target and operation index, plus available
row/line positions, without echoing source values or parser fragments. Normal
execution prints nothing. Mapping plans and result payloads are excluded from
`repr`; callers can explicitly inspect them locally. The field/operation trace
contains names rather than source values. Unused source values are retained only
when the caller explicitly requests the separate extras namespace.

Tests deny file access, network connections, subprocesses and executable builtins
while a normal mapping runs. Additional tests reject unsafe operation syntax,
unknown executable parameters, custom conversion/copy hooks and altered plans.
These controls concern the mapping language, not a sandbox for arbitrary Python
code run by the host process. Redacted report generation remains deferred.

## Phase 2 Step 7 content references

`utils.paths.resolve_content_reference(reference, base_directory=...)` resolves
one explicitly supplied local reference. With no `base_directory`, the caller
must supply `records_path`; its containing directory supplies the base. There is
no implicit current-directory fallback. `allow_absolute=True` is an explicit
in-memory opt-in and still cannot escape the same approved base. No run-config
schema, new output field, or public CLI command has been added.

`io.loaders.load_content_reference` performs the safe resolution and explicit
read together. It accepts the existing `ResourceLimits(max_content_bytes=...)`
and an optional `RowLocation`. A configured size limit is checked both before
and during streaming. Text is decoded as strict UTF-8 with line endings and BOM
preserved. Empty/whitespace-only files and NUL-bearing binary payloads fail.
No extension-based decoding, archive extraction, byte guessing or content
analysis occurs. The returned string is available only to the explicit caller.
Table loaders, normalization, provenance joins and generation validation never
call this loader automatically or start traversing reference-valued metadata.

Slash and backslash are treated as portable separators. References cannot use
remote schemes, UNC/device syntax, drive-relative Windows syntax, alternate
data streams, reserved device names, or control characters. Percent escapes,
variables, and tilde text are literal filename data, never expanded. Portable
content references reject trailing dots/spaces in path components. Existing
explicit source-file path behavior remains unchanged.

Internal symlinks are permitted when their targets remain inside the base.
Link targets are inspected before following them so a remote target is rejected
without fetching it. A maximum of 40 link traversals bounds loops. Missing targets
use `E_CONTENT_REF_MISSING`; containment violations use `E_CONTENT_REF_OUTSIDE_BASE`.
Unsupported file types, malformed encoding and resource-limit failures use the
existing structured input codes. No full source path or rejected content is
interpolated into a normal error; content paths are represented as `[redacted]`.

Configured base directories are trusted local inputs. Reads assume a stable
filesystem tree, with extra directory-descriptor/no-follow protections on POSIX
and pre-read identity checks on all platforms. Windows uses a checked-path
fallback. Hostile concurrent directory replacement and host-mounted network
filesystems are outside this boundary; this is not an operating-system sandbox.
No claim of race-proof containment across all platforms is made.

A content-specific failure leaves caller-owned record and provenance objects
unchanged. Later validation orchestration decides whether metadata-only work
can continue and how to expose unavailable capabilities. This step introduces
no observability verdict, report, global content cache, or total-bundle load
budget manager. Real optional Parquet-presence validation remains outstanding.
