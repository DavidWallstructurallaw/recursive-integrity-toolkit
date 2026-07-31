# Architecture

Status: Phase 1 scaffold.

The controlling architecture is `REPOSITORY_ARCHITECTURE.md`.

The approved dependency direction is:

```text
utilities and shared models
-> input and representation boundaries
-> observability eligibility
-> metrics and lineage
-> result assembly
-> renderers
-> CLI
```

Phase 1 provides import-safe module locations and owner metadata. Analytical behavior begins only in later approved phases.
