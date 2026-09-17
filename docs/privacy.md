# Privacy and Local Input Boundaries

Status: Phase 2. `PRIVACY_AND_DATA_HANDLING.md` remains authoritative.

Package import does not contact a network, open user audit files, require optional PyArrow or start a service. Runtime operates on explicitly supplied local files and declarations. No telemetry, background worker, plugin, cloud client, database, model download or LLM service exists. CI/package installation acquire dependencies separately; CI uses synthetic fixtures only.

## Mapping

The fixed language accepts plain finite data. It cannot evaluate expressions, execute templates/commands, invoke user callbacks, resolve dotted attributes or access environment/network resources. URL/code-like literals remain data. Only the explicit mapping-file loader reads a declared snapshot with limits. Row source values are not echoed in ordinary errors. Payload/declaration repr suppression does not anonymize caller-owned objects. These are language constraints, not a sandbox for arbitrary host Python.

## Content references

Explicit base_directory controls resolution. Without it, an explicit records_path supplies the containing directory; current-directory fallback is prohibited. Absolute references are blocked by default; explicit in-memory opt-in still cannot escape the same base.

The reader accepts only regular local UTF-8 files, with configured per-file max_content_bytes checked before and during reading. Original line endings/BOM remain. Empty/whitespace-only content, malformed encoding and NUL-bearing binary content fail. No archive extraction, encoding guessing or content analysis occurs.

Portable separators include slash/backslash. Remote URI, UNC/device, drive-relative Windows syntax, alternate data streams, reserved devices, control characters and trailing dots/spaces are rejected. Percent escapes, variables and tilde text remain literal. Internal symlinks are allowed only inside the base. Targets are inspected before following; remote targets are rejected. A forty-link limit bounds loops. Error codes distinguish missing targets, containment and input failures. Normal content errors use [redacted] paths and never echo payloads.

Configured bases and directory trees must be trusted and stable while reading. POSIX uses additional directory-descriptor/no-follow controls; Windows uses checked-path and file-identity verification. Malicious concurrent directory replacement and host-mounted network filesystems remain outside the guarantee. No universally race-proof containment or operating-system sandbox is claimed.

## Orchestration and internal results

Table loading, mapping, normalization, joins and generation checks do not automatically follow reference-valued metadata. validate_bundle requires LOCAL_REF and resolve_local_content=True before invoking PR-017. Each record uses its source-file directory when no explicit base is supplied.

Content failures preserve metadata and enter diagnostics. Independent capabilities can remain usable, but errors remain visible. Output paths are not executed and no report is written. Resource controls are explicit per-file/row/depth limits, not a total-bundle memory or decompression sandbox.

Internal results retain records, provenance, file inventory and private source locations. Default repr excludes payloads, while aggregate messages redact paths. Explicit object serialization can still expose sensitive local data. Redacted public report generation is deferred; handle these internal objects under the governing data policy.

## Development evidence

Tests use synthetic data and verify offline behavior, unchanged sources, rejected mapping execution and contained reference access. A clean installed-wheel check blocks network plus NumPy/pandas/PyArrow, imports all forty modules and runs Hero validation.

Delivery archives contain tracked public source, project wheel/sdist and synthetic test evidence. Git internals, environments, caches, private data and full theory PDFs are excluded. No third-party source, datasets, models or fonts are bundled. Metadata lists actual installed tool versions and their declared license metadata; this is not an independent vulnerability or legal audit.

The completion record reports failures, repairs and unexecuted checks separately. No production security certification is claimed. Phase 3 is not authorized.
