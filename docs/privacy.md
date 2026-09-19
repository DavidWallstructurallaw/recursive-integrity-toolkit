# Privacy and Local Input Boundaries

Status: Phase 3 development milestone. `PRIVACY_AND_DATA_HANDLING.md` remains authoritative.

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

Delivery bundles contain separate tracked-source archives, project wheel/sdist and synthetic test evidence. Git internals, environments, caches, private data and full theory PDFs are excluded. No third-party source, datasets, models or fonts are bundled. Metadata lists actual installed tool versions and their declared license metadata; this is not an independent vulnerability or legal audit.

The completion record reports failures, repairs and unexecuted checks separately. No production security certification is claimed. Only explicitly authorized Phase 3 steps may add bounded calculation behavior.


## Phase 3 Step 3 exact-content privacy

Exact hashing and duplicate grouping operate solely on explicitly supplied memory.
LOCAL_REF paths are never opened or hashed by this layer. The existing safe reader
remains responsible for explicit reads, containment, encoding and resource limits.
No new file reader, network client, logger or background process is introduced.

The representation object retains exact byte snapshots for equality checks and
hides them from default repr. The duplicate result retains only the selected scope,
representation metadata, groups and counts, without source content or notes.
Default repr suppression is not anonymization or protection from deliberate object
inspection. A content digest is linkable and can be tested against guessed text;
it must not be described as a redacted record ID or proof of origin.

Tests use synthetic text, independent copies, supplied local-reference payloads,
Unicode and newline variants, artificial digest collisions, and no-I/O/no-logging
checks. Errors use static messages; collision failures do not echo the conflicting
text. Public report serialization and redaction remain deferred to Phase 4.

## Explicit mathematical invocation

Representation and metric calls operate on supplied immutable memory and do not read user files, environment variables, content references, network resources or user code. Static operation/import gates and fail-on-call runtime tests protect these boundaries. Ordinary input validation never invokes metrics, including when a simulation configuration is present. All forty imports and input-only smoke tests retain numerical/optional import blockers; a separate numerical smoke uses the installed wheel with dependencies present and network blocked.

Sampled closed resampling creates one explicitly seeded local PCG64 generator per call after domain/resource checks. It does not read or alter the global random stream. No auto-installation or remote RNG exists. Declared operation/state/horizon/replicate bounds limit allocation; they do not provide an OS memory sandbox or certify full-report performance.

Scopes, state IDs, source declarations, weights, content digests and original distributions can be sensitive. Default repr suppression and static errors reduce accidental disclosure, but deliberate serialization or inspection of these internal objects can expose caller data. They are not redacted public reports. Missing provenance and errors remain visible; no inference of authorship, external truth, semantic independence or safe deployment is performed. Evidence bundles use only repository-owned synthetic fixtures.

## Phase 4 Step 4: explicit safe report views

The Step 4 APIs implement approved P4-D05 and P4-D08, with PR-015 privacy and
PR-016 reproducibility ownership. The earlier paragraphs describe their accepted
historical stages. `assemble_report` continues to assemble standard internal
evidence. Its `CanonicalReport` validates structure and evidence semantics;
validation alone is not a privacy transformation. After calculation and assembly,
call `reports.assembly.privacy_view` to create an immutable `SafeReportView` for
an output sink. This operation does not ingest files, invoke a metric, change a
classifier result, start a simulation or publish a report.

Standard views retain structural identifiers and approved local input inventory,
while excluding raw content, private notes, full embeddings, secrets and raw
configuration dumps. Caller-supplied narrative and exception text are not trusted
because they pass structural validation. Approved static explanations remain
readable; unrecognized text is withheld with an explicit privacy disclosure.
Structured diagnostics retain severity, counts, affected capabilities and
available safe locations. Registered diagnostic codes retain their meaning;
unknown codes cannot be relabeled as another registered error category.

Redacted views additionally remove full paths, source/evidence references and raw
per-record content digests. Input-inventory SHA-256 and normalized configuration
SHA-256 remain reproducibility metadata under P4-D08. They are linkable and do
not provide statistical anonymity. Dataset, state, scope and other potentially sensitive identifiers
are transformed consistently across nested scopes, map keys, comparisons and
simulation identities. The selected order and all supplied aggregate numbers,
denominators, evidence classes, availability and error severity remain unchanged.
Pseudonyms do not reorder parallel simulation arrays.

Record-ID modes are `hash` (the redacted default), `preserve` and `omit`.
An explicit `preserve` applies only to declared record-ID fields, never to a
matching string embedded in a diagnostic, path or other narrative. `omit` removes
record-level linkage while retaining aggregate counts and disclosure of exclusion
reasons. An omitted duplicate-group identity list uses the existing
`redacted_identity_details` contract. These omissions describe a privacy choice,
not missing input evidence, and do not turn an available metric into unavailable.

Identifier protection uses domain-separated HMAC-SHA-256 over unambiguous
canonical encodings. A fresh secret gives run-scoped consistency and separates
otherwise identical runs. An explicitly supplied local secret file permits
declared cross-run consistency. A fixed injected secret is useful for deterministic
tests. Secrets, secret file paths and reverse mappings are never included in a
safe view or diagnostic. Domain separation prevents an identical string used as
a dataset version and a state from acquiring the same identifier by accident.

Safe run metadata uses explicit supplied execution measurements and a reconstructed
approved command description. It never copies raw command-line arguments. A
normalized resolved-config SHA-256 identifies the declared configuration under
documented exclusions; it is not an authenticity check. Input SHA-256 values still
describe supplied bytes. The network count has scope
`toolkit_managed_outbound_operations`, not operating-system-wide monitoring.
Unavailable metadata has a specific null reason rather than an invented clock,
environment or execution claim.

The Phase 4 options adapter validates supported output declarations and conflicts
without changing inherited `resolve_config` or `validate_bundle` behavior. Direct
Phase 2 calls retain their inert output mappings. Only standard and redacted
privacy are selected; inherited debug labels do not activate raw-content output.

These views provide identifier and content protection, not statistical anonymity,
small-cell suppression, evidence authentication or protection from deliberate
inspection of the caller's original internal objects. Step 4 does not implement
renderers, CLI analysis or output publication. Those later sinks must consume the
validated privacy view before emitting a report or diagnostic.
