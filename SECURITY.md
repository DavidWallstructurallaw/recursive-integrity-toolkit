# Security Policy

## Current status

The project is in Phase 2 Step 7 and is not an official production release.

## Security posture

Core v0.1 is designed for local-first execution with no required telemetry, hosted service, remote model, plugin execution, or network content retrieval.

## Reporting a vulnerability

Do not include private datasets, secrets, raw training content, or identifying local paths in a public issue. Provide a minimal synthetic reproduction. A private reporting channel should be configured before the first public release.

## Scope

Security-sensitive areas include schema mapping, local content references, path handling, report redaction, logging, dependencies, and any proposed network feature.

## Step 7 local content boundary

Content reads require an explicit call to `io.loaders.load_content_reference`.
The approved base is explicit, or defaults to the declared records file's directory.
Relative traversal and symlink targets must remain inside that base. Absolute
reference opt-in never grants access outside it. URI, UNC/device, alternate data
stream and reserved device-name forms are rejected before reference resolution.

The configured base and its containing filesystem must be trusted and stable
while a read executes. The resolver inspects untrusted link targets before
following them; broken links, escapes and overlong/cyclic chains fail. POSIX
reads pin directory descriptors and use no-follow flags where supported. All
platforms recheck the resolved path and file identity before reading, enforce
an explicit per-file byte limit, and reject detected changes during a read.

These controls do not constitute an OS sandbox. They do not defend against all
hostile concurrent directory renames, hostile kernel/filesystem behavior, or
network filesystems mounted by the host as local paths. Windows uses the portable
checked-path fallback because directory-descriptor opens are unavailable there.
Use a private, stable local input directory. Do not treat an earlier returned
resolved path as a lasting permission to open it later without revalidation.

Failures contain safe messages and redacted paths, never source text. No automatic
logging, raw-content report, total-bundle budget manager, or capability verdict is
introduced by this step. Report redaction and later orchestration remain deferred.
