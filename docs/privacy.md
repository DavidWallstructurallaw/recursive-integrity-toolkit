# Privacy

Status: Phase 1 scaffold.

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
