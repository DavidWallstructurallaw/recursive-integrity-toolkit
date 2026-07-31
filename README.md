# Recursive Integrity Toolkit

Recursive Integrity Toolkit is a local-first, auditable research toolkit for examining recursive closure risk in synthetic-data and recursive-data pipelines.

## Current status

The repository is in **Phase 1: repository scaffold**. Package installation, import, help, and version commands are available. Analytical audit functionality has not been implemented.

## v0.1 product boundary

Planned capabilities include representation-bound support and diversity analysis, provenance coverage, closure exposure bounds, lineage tracing, ancestry concentration, longitudinal comparison, and clearly labeled simulations.

The project does not provide a universal collapse score, universal integrity score, universal entropy score, hidden provenance inference, a hosted service, telemetry, an embedded LLM, or automatic policy enforcement.

## Local-first posture

Core analysis is designed to run locally without required network calls, telemetry, a server, a database service, or a remote model.

## Phase 1 startup

```bash
python -m recursive_integrity_toolkit
rit --help
rit version
```

The current commands report scaffold status only.

## Specifications

The approved Phase 0 specifications are stored in the repository root. Start with:

- `PHASE_0_APPROVAL.md`
- `PROJECT_INSTRUCTIONS.md`
- `V0.1_PRODUCT_SPEC.md`
- `REPOSITORY_ARCHITECTURE.md`
- `DEPENDENCY_STRATEGY.md`
- `THEORY_TO_CODE_TRACEABILITY.md`
- `VALIDATION_PLAN.md`

## Theory sources

The toolkit is a theory-led reference implementation based on the works listed in `THEORY_SOURCES.md`. Full theory PDFs retain their own licenses and are not included in this public repository scaffold.

## Licensing

- Source code and code-adjacent configuration: Apache-2.0
- Reusable specifications and documentation: CC BY 4.0
- Repository-created examples: CC BY 4.0
- Theory publications: retain their stated licenses

See `LICENSING_NOTES.md` and `NOTICE`.
