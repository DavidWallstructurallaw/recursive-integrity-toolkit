# PRIVACY_AND_DATA_HANDLING

## Document control

| Field | Value |
|---|---|
| Project | Recursive Integrity Toolkit |
| Target release | v0.1 |
| Phase | Phase 0 |
| Status | APPROVED PHASE 0 BASELINE |
| Primary owner | Theory Owner |
| Technical reviewers | Technical Maintainer, Security Reviewer |
| Depends on | `PROJECT_INSTRUCTIONS.md`, `V0.1_PRODUCT_SPEC.md`, `DEFINITIONS_AND_UNITS.md`, `DATA_AND_PROVENANCE_SPEC.md`, `OBSERVABILITY_AND_REPORTING.md`, `THEORY_TO_CODE_TRACEABILITY.md`, `VALIDATION_PLAN.md` |
| Purpose | Freeze the local-first privacy posture, content-handling rules, logging limits, temporary-file behavior, redaction, sharing guidance, security boundaries, and release checks for v0.1 |

This file defines how Recursive Integrity Toolkit v0.1 handles records, content, provenance, lineage, embeddings, file paths, reports, temporary artifacts, logs, and user-supplied metadata.

The default posture is local-first and data-minimizing.

The toolkit should examine the structure necessary for an audit while avoiding unnecessary exposure of source content.

v0.1 is a local research toolkit. It is not a hardened multi-tenant service, a hosted compliance platform, or a secure data enclave.

---

## 1. Privacy objectives

v0.1 must preserve the following properties.

### 1.1 Local execution

Core analysis runs on the user's local machine.

No cloud service is required.

### 1.2 No hidden network behavior

Core analysis must not:

- upload source data,
- retrieve remote content,
- contact analytics services,
- send telemetry,
- submit errors automatically,
- download models,
- contact a licensing server.

### 1.3 Data minimization

The toolkit should load, retain, display, and export only the data required for the requested analysis.

### 1.4 Content-safe observability

Normal logs and standard summary reports should describe:

- counts,
- coverage,
- identifiers,
- structural metrics,
- warnings,
- errors.

They should avoid raw content unless the user explicitly requests a content-bearing output.

### 1.5 Explicit sharing mode

A report intended for sharing should use redacted mode.

### 1.6 Stable uncertainty

Redaction and privacy settings must not change calculated metrics.

### 1.7 No silent persistence

The toolkit must not retain user data after a run beyond documented output and temporary-file behavior.

### 1.8 Inspectable behavior

Privacy-relevant behavior must be documented and testable.

---

## 2. Privacy scope

This specification applies to:

- records files,
- provenance manifests,
- schema mappings,
- configuration files,
- embedding files,
- lineage graphs,
- local content references,
- external reference distributions,
- temporary normalized tables,
- simulation traces,
- JSON reports,
- Markdown reports,
- optional HTML reports,
- logs,
- error files,
- caches,
- debug output,
- issue templates,
- example data.

This specification does not claim to control:

- user operating-system security,
- disk encryption,
- shell history outside the toolkit,
- third-party backup software,
- external repository hosting,
- user-created copies of reports,
- the security of unrelated dependencies.

---

## 3. Data classes

### 3.1 Structural metadata

Examples:

- record counts,
- dataset versions,
- field names,
- enum counts,
- support size,
- diversity values,
- warning codes,
- error codes.

Default treatment:

```text
reportable
```

### 3.2 Pseudonymous identifiers

Examples:

- record IDs,
- batch IDs,
- generator IDs,
- run IDs,
- parent references.

Default treatment:

```text
reportable in standard local reports
hashable or omittable in redacted reports
```

### 3.3 Potentially identifying paths and references

Examples:

- full file paths,
- local content paths,
- source URIs,
- grounding-evidence references.

Default treatment:

```text
local only
redacted in sharing mode
```

### 3.4 Raw content

Examples:

- text samples,
- documents,
- prompts,
- model outputs,
- notes,
- source passages.

Default treatment:

```text
excluded from normal logs
excluded from redacted reports
included only in explicitly requested diagnostic output
```

### 3.5 Provenance notes

Free-text provenance notes may contain:

- names,
- internal systems,
- private explanations,
- URLs,
- legal information,
- confidential context.

Default treatment:

```text
private
```

### 3.6 Embeddings

Full embedding vectors may encode sensitive features and may be large.

Default treatment:

```text
excluded from reports and logs
```

### 3.7 Configuration secrets

The toolkit should not require secrets for core operation.

If a configuration file contains secrets accidentally, the toolkit must not echo the complete file into reports or logs.

---

## 4. Default execution posture

### 4.1 Required defaults

```text
network access: disabled or unused
telemetry: none
content upload: none
automatic issue submission: none
raw content in normal logs: none
full embeddings in reports: none
debug mode: off
redacted sharing mode: available
```

### 4.2 Network-call counter

A run should record:

```text
network_call_count
```

The hero example must report:

```text
0
```

### 4.3 No remote content resolution

Fields such as:

```text
source_uri
grounding_evidence_ref
content
```

may preserve remote-looking identifiers as metadata.

They do not authorize retrieval.

### 4.4 Optional future connectors

Any future connector or remote adapter requires:

- separate specification,
- explicit opt-in,
- authentication handling,
- data-flow documentation,
- privacy review,
- security review,
- new tests,
- new capability labeling.

No such connector is part of core v0.1.

---

## 5. Input handling

### 5.1 Original files

The toolkit must not modify source files in place.

### 5.2 Read-only posture

Inputs should be opened read-only where practical.

### 5.3 File inventory

The run may record:

- file role,
- file name,
- size,
- hash,
- row count,
- format.

### 5.4 Full paths

Standard local reports may include full paths when useful.

Redacted reports should replace them with:

- file names,
- relative paths,
- or stable tokens.

### 5.5 Content references

Local content references must remain inside approved local directories.

Path traversal and network schemes are prohibited.

### 5.6 Archive behavior

Automatic archive extraction is outside minimum v0.1.

### 5.7 Unsupported binary content

Unsupported binary content should produce a clear error or unavailable content-analysis status.

It must not be uploaded for remote interpretation.

---

## 6. In-memory handling

### 6.1 Minimum necessary loading

The implementation should avoid loading raw content when the requested audit uses metadata only.

### 6.2 Content-bearing metrics

Exact duplicate detection may require content hashing.

The implementation should hash content without preserving unnecessary copies.

### 6.3 Embeddings

When embeddings are used:

- vectors remain local,
- vectors are not printed,
- only dimensions, file hashes, cluster IDs, and aggregate metrics may appear in standard reports.

### 6.4 Copies

The implementation should avoid unnecessary duplicate in-memory copies of large content tables.

### 6.5 Process isolation

v0.1 does not require a sandboxed worker process.

Security-sensitive extensions may add one later.

---

## 7. Logging rules

### 7.1 Normal log fields

Normal logs may include:

- run ID,
- toolkit version,
- file roles,
- file names or paths,
- row counts,
- schema fields,
- coverage values,
- metric names,
- duration,
- warning codes,
- error codes,
- affected record keys,
- capability status.

### 7.2 Prohibited normal-log fields

Normal logs must not include:

- raw record content,
- notes,
- provenance notes,
- full embeddings,
- complete mapping source rows,
- credentials,
- environment variables,
- full local content payloads,
- stack traces containing user content.

### 7.3 Representative locations

Validation may identify:

- file,
- row,
- line,
- field,
- record key.

### 7.4 Message sanitization

Error-message construction must not interpolate raw content.

### 7.5 Log levels

Recommended levels:

```text
DEBUG
INFO
WARNING
ERROR
CRITICAL
```

### 7.6 Debug mode

Debug mode must be explicitly enabled.

Debug mode may include:

- normalized rows,
- detailed mapping output,
- graph-edge details,
- stack traces.

Debug mode should still avoid:

- credentials,
- complete environment dumps,
- automatic upload,
- unrelated file content.

### 7.7 Debug warning

When debug mode is enabled, the CLI should warn that additional local details may be written.

---

## 8. Temporary data

### 8.1 Run-scoped directory

Temporary artifacts should be stored in a run-scoped directory.

### 8.2 Default contents

Temporary storage may include:

- normalized intermediate tables,
- parsed parent-edge tables,
- simulation intermediates,
- render intermediates.

### 8.3 Default cleanup

Temporary files should be deleted at normal exit unless:

- the user requests preservation,
- debugging preservation is enabled,
- a failure bundle is explicitly requested.

### 8.4 Abnormal exit

The toolkit should document that temporary files may remain after:

- process termination,
- system crash,
- forced kill,
- power loss.

### 8.5 Temporary-file permissions

Use restrictive local permissions where supported.

### 8.6 Temporary-file names

Temporary names should not embed raw content or sensitive notes.

### 8.7 User-selected output directory

Final outputs remain in the user-selected output directory.

The toolkit must not delete final outputs automatically.

---

## 9. Persistent outputs

### 9.1 Required persistent outputs

A successful full run may preserve:

- JSON report,
- Markdown report,
- optional HTML report,
- validation summary,
- run metadata,
- user-requested normalized manifest.

### 9.2 Optional persistent outputs

- simulation traces,
- error-only report,
- redacted sharing bundle,
- benchmark summary.

### 9.3 No hidden cache

Core v0.1 should not create a persistent global cache of user records.

### 9.4 Cache proposal

A future cache requires:

- explicit purpose,
- location,
- invalidation rules,
- deletion command,
- privacy review.

---

## 10. Redacted mode

### 10.1 Purpose

Redacted mode prepares a report for broader sharing.

### 10.2 Required redactions

Redacted mode must remove or transform:

- raw content,
- notes,
- provenance notes,
- full file paths,
- local content references,
- source URIs,
- grounding-evidence paths,
- full embeddings.

### 10.3 Record-ID modes

Allowed:

```text
preserve
hash
omit
```

Recommended redacted default:

```text
hash
```

### 10.4 Other identifier modes

Batch IDs, generator IDs, and root IDs may use:

```text
preserve
hash
omit
```

The report should disclose the selected mode.

### 10.5 Stable hashing

The hashing policy must state whether stability applies:

- within one run,
- within one bundle,
- across runs with a user-provided salt.

### 10.6 Salt

A default random run salt protects cross-run correlation.

A user-provided salt may enable stable cross-run redacted comparisons.

The salt must not be printed into a public report.

### 10.7 Metric invariance

Redacted and standard reports must contain identical aggregate analytical values when calculated from the same run.

### 10.8 Redaction order

Calculate first, redact for output second.

### 10.9 Small groups

v0.1 does not promise formal disclosure control for small groups.

Reports intended for sensitive publication should receive human review.

---

## 11. Hashing

### 11.1 File hashes

Recommended:

```text
SHA-256
```

### 11.2 Content hashes

Recommended:

```text
SHA-256 of normalized content bytes
```

### 11.3 Security meaning

Hashes support:

- reproducibility,
- equality checks,
- artifact identity.

Hashes do not prove:

- authorship,
- factual accuracy,
- provenance,
- external grounding.

### 11.4 Unsalted content hashes

Unsalted hashes of predictable content may permit guessing.

Public redacted reports should avoid exposing raw content hashes unless the user understands that risk.

### 11.5 Redacted identifier hashes

Use keyed or salted hashing when cross-record guessing is a concern.

Exact implementation belongs to the technical security review.

---

## 12. Normalized manifest export

### 12.1 User control

Normalized manifest export is optional.

### 12.2 Private fields

Default normalized export should omit:

- notes,
- private evidence paths,
- raw content.

### 12.3 Explicit inclusion

The user may request full local export.

The CLI should warn when sensitive fields are included.

### 12.4 No in-place rewrite

Normalized export must use a new path.

---

## 13. Error handling and privacy

### 13.1 Normal errors

Normal errors should show:

- error code,
- file role,
- field,
- record key,
- row or line,
- remediation.

### 13.2 Raw parser fragments

Parser libraries may include source fragments in exceptions.

The toolkit should sanitize them before user-visible output.

### 13.3 Internal stack traces

Stack traces should appear only in debug mode.

### 13.4 Error bundles

A user-requested diagnostic bundle should contain:

- configuration summary,
- schema inventory,
- warning and error codes,
- redacted fixture where possible.

It should not contain source data by default.

---

## 14. Issue and collaboration guidance

Repository issue templates should tell users:

- do not upload private training data,
- do not paste secrets,
- prefer a minimal synthetic reproduction,
- replace content with harmless placeholders,
- preserve the schema shape,
- share provenance separately when needed,
- use redacted mode,
- remove private paths.

### 14.1 Maintainer response

Maintainers should not request full private datasets when a minimal reproduction can isolate the defect.

### 14.2 Security reports

Security issues should use a private reporting channel when available.

### 14.3 Public discussions

Public examples should avoid real confidential generator IDs, batch names, or internal paths.

---

## 15. Security boundary

### 15.1 v0.1 security claim

v0.1 is a local research toolkit designed to reduce unnecessary exposure and attack surface.

It is not certified for:

- multi-tenant hosting,
- hostile untrusted users,
- regulated data processing,
- classified data,
- high-assurance isolation.

### 15.2 Excluded attack surface

Core v0.1 excludes:

- web server,
- authentication system,
- remote plugin system,
- background telemetry,
- hosted dashboard,
- arbitrary mapping code,
- remote model download.

### 15.3 Dependencies

Dependencies must not silently:

- send telemetry,
- fetch models,
- call remote APIs,
- execute user code.

### 15.4 Input trust

Input files should be treated as untrusted data.

They must not be treated as executable configuration beyond the restricted mapping language.

---

## 16. Schema-mapping privacy and security

### 16.1 Declarative only

Schema mapping must remain allowlisted and declarative.

### 16.2 Forbidden access

A mapping must not access:

- filesystem outside approved inputs,
- environment variables,
- network,
- process execution,
- system commands,
- Python imports.

### 16.3 Audit record

Applied mapping operations may be reported.

Source values need not be printed.

### 16.4 Failure

Unsafe mapping produces:

```text
E_MAPPING_UNSAFE_TRANSFORM
```

---

## 17. Local content-reference security

### 17.1 Base directory

References resolve inside a declared base directory.

### 17.2 Traversal

Path traversal is blocked.

### 17.3 Symlinks

Final resolved path must remain inside the approved base.

### 17.4 Network schemes

Remote schemes are rejected.

### 17.5 Size limits

Config should allow file-size and total-load limits.

### 17.6 Logging

Full resolved local paths are hidden in redacted mode.

---

## 18. Privacy modes

### 18.1 Standard mode

Intended for local analysis.

May show:

- record IDs,
- version IDs,
- local file paths,
- aggregate metrics.

Excludes raw content from normal summary and logs.

### 18.2 Redacted mode

Intended for sharing.

Hides sensitive fields and transforms identifiers.

### 18.3 Debug mode

Intended for local troubleshooting.

May expose additional local details.

Must be explicitly enabled.

### 18.4 Mode recording

The run report must record:

```text
privacy_mode
```

---

## 19. Data retention

### 19.1 Toolkit-controlled retention

The toolkit retains only:

- outputs,
- explicitly preserved temporary files,
- user-requested exports.

### 19.2 No retention service

Core v0.1 has no server-side retention.

### 19.3 User deletion

Users can delete outputs using normal filesystem tools.

A future cleanup command may simplify this.

### 19.4 Release fixtures

Repository fixtures are public test assets and must contain no private user data.

---

## 20. Third-party tools

### 20.1 Local libraries

Local parsing and numerical libraries process data inside the user's environment.

### 20.2 External command invocation

Core v0.1 should not invoke external commands for analysis.

### 20.3 Optional renderers

Optional HTML rendering should remain local and self-contained.

### 20.4 Dependency documentation

The repository should document privacy-relevant dependency behavior.

---

## 21. Report-sharing checklist

Before sharing a report, users should verify:

- [ ] redacted mode was used,
- [ ] raw content is absent,
- [ ] notes are absent,
- [ ] file paths are hidden,
- [ ] record IDs are hashed or acceptable,
- [ ] generator IDs are acceptable,
- [ ] source URIs are absent,
- [ ] screenshots do not reveal local paths,
- [ ] unavailable conclusions remain visible,
- [ ] the report contains no private attachments.

---

## 22. Privacy acceptance tests

Required tests:

```text
test_PR015_normal_log_excludes_raw_content
test_PR015_normal_log_excludes_notes
test_PR015_normal_log_excludes_full_embeddings
test_PR015_redacted_json_hides_content
test_PR015_redacted_markdown_hides_notes
test_PR015_redacted_paths_hidden
test_PR015_redacted_ids_hashed
test_PR015_redaction_preserves_metrics
test_PR015_debug_mode_requires_explicit_enable
test_PR016_hero_network_call_count_zero
test_no_network_hero
test_PR017_network_content_reference_rejected
test_PR003_network_mapping_operation_rejected
```

### 22.1 Sentinel tests

Fixtures should include unique sentinel strings in:

- raw content,
- notes,
- provenance notes,
- file paths.

Tests must search outputs and logs for leakage.

### 22.2 Temporary-file tests

Required:

```text
test_temp_directory_is_run_scoped
test_temp_files_removed_on_normal_exit
test_preserve_temp_requires_explicit_config
```

### 22.3 Hash tests

Required:

```text
test_file_hash_is_sha256
test_redacted_hash_stable_with_same_salt
test_redacted_hash_changes_with_different_salt
test_salt_not_emitted_in_public_report
```

---

## 23. Security acceptance tests

Required attack fixtures:

- path traversal,
- symlink escape,
- remote URI,
- executable mapping,
- shell mapping,
- dynamic import,
- environment access,
- malformed JSON nesting,
- oversized input,
- CSV formula injection on export.

Required tests:

```text
test_PR017_path_traversal_blocked
test_PR017_symlink_escape_blocked
test_PR017_remote_uri_blocked
test_PR003_eval_rejected
test_PR003_shell_rejected
test_PR003_dynamic_import_rejected
test_PR003_environment_access_rejected
test_json_depth_limit_enforced
test_input_size_limit_enforced
test_csv_export_formula_injection_protected
```

---

## 24. Privacy failure conditions

Release must stop if:

- raw content appears in normal logs,
- notes appear in redacted reports,
- full embeddings appear in reports,
- hero makes a network call,
- a content reference escapes the approved directory,
- a mapping executes code,
- a report includes a secret from config,
- redaction changes analytical values,
- a temporary global cache stores user records without documentation,
- debug mode activates silently.

---

## 25. Privacy release checklist

Before official v0.1:

- [ ] local-first behavior documented,
- [ ] no-network test passes,
- [ ] telemetry absent,
- [ ] logging tests pass,
- [ ] redaction tests pass,
- [ ] content-reference tests pass,
- [ ] schema-mapping security tests pass,
- [ ] temporary-file behavior documented,
- [ ] issue templates warn against private uploads,
- [ ] fixtures contain no private data,
- [ ] optional HTML has no remote resources,
- [ ] dependency privacy behavior reviewed.

---

## 26. Decision dependencies

| Decision | Privacy effect |
|---|---|
| `UD-016` | safe schema mapping |
| `UD-019` | required Markdown output |
| `UD-020` | optional near-duplicate methods |
| `UD-022` | deferred external metadata adapters |
| `UD-024` | theory PDF repository policy |
| `UD-025` | dependency choices |
| `UD-036` | optional HTML |

---

## 27. Approval

### Theory Owner decision

- [ ] Approve privacy and data-handling baseline
- [ ] Approve with exceptions
- [ ] Return for revision

Exceptions:

```text

```

Theory Owner:

```text
Xiangyu Guo
```

Approval date:

```text

```

Approved status:

```text
PENDING
```

### Technical Maintainer acknowledgment

- [ ] Local-first behavior is implementable.
- [ ] Logging can exclude content.
- [ ] Temporary files can remain run-scoped.
- [ ] Redaction can occur after calculation.
- [ ] No persistent global data cache is required.

Technical notes:

```text

```

Maintainer:

```text

```

Date:

```text

```

### Security Reviewer acknowledgment

- [ ] Mapping cannot execute code.
- [ ] Content references remain local.
- [ ] Network behavior is absent by default.
- [ ] Redaction tests cover sensitive fields.
- [ ] Error handling avoids source-content leakage.

Security notes:

```text

```

Reviewer:

```text

```

Date:

```text

```

---

## 28. Change-control rule

After approval:

1. a new data sink requires privacy review,
2. a new network feature requires explicit opt-in and separate specification,
3. a new persistent cache requires retention and deletion rules,
4. a new log field requires sensitivity review,
5. a new report field requires redaction behavior,
6. a new mapping operation requires security tests,
7. a new content loader requires path and resource-limit tests,
8. privacy defaults must not weaken silently,
9. example data must remain synthetic or safely public,
10. release convenience must not override local-first behavior.
