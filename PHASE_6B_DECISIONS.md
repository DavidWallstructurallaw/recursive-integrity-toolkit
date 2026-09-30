# Phase 6B decisions

| Field | Value |
|---|---|
| Status | Phase authorized; Step 1 complete |
| Authority | Theory Owner instruction `Phase 6B 继续吧`, 2026-09-30 |
| Governing decision | Approved UD-017; empirical ingestion remains deferred by UD-031 |
| Accepted baseline | `b6389c6c50f2fc61d39580274bd24ed39e09ca45` |
| Branch | `phase6b-simulation` |
| Current runtime | `0.1.0.dev5`, report schema `1.2` |
| Staged target | `0.1.0.dev6`, report schema `1.3` |

The current instruction authorizes starting Phase 6B. It is not represented as
prior approval of this newly written plan's individual engineering choices.
P6B-D01 through P6B-D07 in `PHASE_6B_PLAN.md` implement the existing authorized
model, evidence classes and product boundaries. There is no identified missing
theory decision blocking this bounded start.

The current work completes Step 1 in the established stepwise workflow. Existing
permission to synchronize project work continues on this branch. No merge, tag,
publication, empirical intervention feature or F-016 public field is authorized
by this record.

## Step 1 clarifications

1. Use constant `r_t=r` as an explicit model assumption. Both vectors declare
   identical state IDs; their positive supports may differ. States introduced
   by `r` must be explicitly present with zero internal mass.
2. Exact event meaning comes from `DEFINITIONS_AND_UNITS.md` sections 12.10 and
   13.6. Repeated state losses and re-entries are valid separate transitions.
3. Reset the supplied PCG64 seed independently for each requested model. This
   makes replay and the lambda-zero equality check well defined; it does not
   establish paired statistical precision or causal effect.
4. Limit each request to one closed and/or one reopened scenario. Shared
   parameters are declared once. No general parameter grid or automatic
   lambda-zero/one control is added.
5. Reuse existing limits with a combined one-million-path-cell admission bound.
   New report-facing experiment requests use exactly representable nonnegative
   JSON seeds up to `2**53-1`; the existing standalone kernel's seed domain is
   unchanged. This is a serialization boundary, not a change in theory.
6. Opening T5 requires a model-specific report variant. The existing closed
   family continues to reject external parameters. Event uniqueness must retain
   replicate, step and state; valid recurrence must not be deduplicated.
7. Eligibility remains input-only. Align literal state validation and absolute
   mass tolerance with the accepted kernel; separately check executable limits.
   Config resolution, validation, assembly and rendering never create an RNG.

## Current verification boundary

The single current source reference advances to accepted Phase 6A completion
`b6389c6`. Step 1's product implementation allowlist is empty. All 75 protected
product files, all 16 frozen specifications and all 14 canonical packaged
resources retain their accepted bytes. The obsolete dev4-to-dev5 exception is
removed because dev5 is now part of the accepted baseline.

The new rational fixtures are independent acceptance targets, not generated
sampled outputs. They validate their stated arithmetic; they do not certify an
unimplemented reopened sampler, report, CLI, privacy transform or performance
profile. Actual Step 1 checks are recorded in `PHASE_6B_STEP_1.md`.
