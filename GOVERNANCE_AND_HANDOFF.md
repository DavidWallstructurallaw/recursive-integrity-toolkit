# GOVERNANCE_AND_HANDOFF

## Document control

| Field | Value |
|---|---|
| Project | Recursive Integrity Toolkit |
| Target release | v0.1 |
| Phase | Phase 0 |
| Status | APPROVED PHASE 0 BASELINE |
| Primary owner | Theory Owner |
| Reviewers | Technical Maintainer, Mathematical Reviewer, Security Reviewer, Domain Validator |
| Depends on | `PROJECT_INSTRUCTIONS.md`, `UNRESOLVED_DECISIONS.md`, `THEORY_SOURCE_MAP.md`, `THEORY_TO_CODE_TRACEABILITY.md`, `VALIDATION_PLAN.md`, `SUCCESS_CRITERIA.md`, `LICENSING_NOTES.md` |
| Purpose | Define decision authority, roles, review paths, release labels, change classes, official identity, contribution flow, dispute handling, succession, and future maintainer handoff |

Recursive Integrity Toolkit begins as a theory-led reference implementation.

Its governance must protect two things at the same time:

- conceptual fidelity,
- technical transferability.

The project should remain open to technical improvement while preserving explicit authority over the meaning of theory-derived public results.

No maintainer should need private author knowledge to understand the approved product contract.

No implementation convenience should silently redefine the theory.

---

## 1. Governance objectives

The governance model should:

- preserve theory meaning,
- permit technical improvement,
- maintain traceability,
- keep decisions reviewable,
- support external contributions,
- distinguish official and third-party releases,
- prevent hidden scope drift,
- make future handoff possible,
- preserve repository history,
- preserve release evidence,
- resolve disputes through documented authority.

---

## 2. Initial governance model

v0.1 uses a role-based review model.

The Theory Owner holds final authority over theory-relevant meaning.

The Technical Maintainer holds implementation authority within approved meaning and scope.

Mathematical, security, and domain reviewers provide required approval for their areas.

A single person may temporarily hold multiple roles.

Role consolidation should be disclosed.

---

## 3. Roles

### 3.1 Theory Owner

Responsibilities:

- protects conceptual boundaries,
- approves theory interpretation,
- approves Theory Map changes,
- approves Trace ID meaning,
- approves public claims,
- approves theory-version updates,
- approves release-level theory fidelity,
- resolves conflicts between theory and implementation meaning,
- approves official release identity.

The initial Theory Owner is:

```text
Xiangyu Guo
```

### 3.2 Technical Maintainer

Responsibilities:

- repository structure,
- package architecture,
- dependency review,
- implementation quality,
- CI,
- tests,
- packaging,
- releases,
- issue triage,
- technical documentation,
- security patch coordination.

The Technical Maintainer must not redefine theory terms through code.

### 3.3 Mathematical Reviewer

Responsibilities:

- formula transcription,
- units,
- denominators,
- ranges,
- expected values,
- numerical tolerances,
- simulation assumptions,
- ancestry allocation,
- mathematical test adequacy.

### 3.4 Security Reviewer

Responsibilities:

- local-first posture,
- dependency attack surface,
- schema-mapping safety,
- content-reference safety,
- path handling,
- logging,
- redaction,
- no-network validation,
- vulnerability review.

### 3.5 Domain Validator

Responsibilities:

- realistic workflow review,
- usefulness,
- report clarity,
- actionability,
- domain-native limitations,
- prevention of overinterpretation.

### 3.6 Contributor

Responsibilities:

- follows contribution scope,
- cites owner IDs,
- adds tests,
- preserves licensing,
- avoids private data,
- documents changes.

### 3.7 Release Manager

Optional role.

Responsibilities:

- prepares release candidate,
- runs release checklist,
- collects approvals,
- publishes artifacts,
- verifies tags and notes.

The Technical Maintainer may initially serve as Release Manager.

### 3.8 Documentation Maintainer

Optional role.

Responsibilities:

- README,
- tutorials,
- CLI help,
- report-schema documentation,
- terminology consistency.

---

## 4. Authority domains

### 4.1 Theory authority

Theory Owner approval is required for changes to:

- closure meaning,
- diversity interpretation,
- external grounding meaning,
- integrity language,
- entropy language,
- concentration-versus-failure boundary,
- theory source hierarchy,
- Theory Map entries,
- Trace ID claims,
- unavailable-conclusion policy,
- cross-domain claims.

### 4.2 Mathematical authority

Mathematical Reviewer approval is required for changes to:

- formulas,
- units,
- denominators,
- probability interpretation,
- HHI allocation,
- numerical tolerances,
- expected values,
- simulation model.

### 4.3 Technical authority

Technical Maintainer approval is required for:

- code architecture,
- dependency changes,
- packaging,
- CI,
- performance implementation,
- refactoring,
- CLI structure,
- internal data structures.

### 4.4 Security authority

Security Reviewer approval is required for:

- network features,
- remote adapters,
- executable configuration,
- content loaders,
- path handling,
- authentication,
- telemetry,
- persistent cache,
- redaction changes.

### 4.5 Domain authority

Domain Validator approval is required for:

- domain-specific interpretation,
- real-workflow claims,
- empirical validation,
- user-facing recommendations that extend beyond metadata collection.

---

## 5. Decision classes

### 5.1 Class A: theory-relevant public meaning

Examples:

- new public metric,
- evidence-class change,
- changed closure definition,
- changed unavailable conclusion,
- changed report claim.

Required approvals:

- Theory Owner,
- Technical Maintainer,
- Mathematical Reviewer when numerical.

### 5.2 Class B: mathematical implementation

Examples:

- formula,
- normalization,
- denominator,
- allocation rule,
- simulation parameter semantics.

Required approvals:

- Mathematical Reviewer,
- Technical Maintainer,
- Theory Owner when interpretation changes.

### 5.3 Class C: technical implementation

Examples:

- refactor,
- performance optimization,
- internal type,
- dependency,
- code organization.

Required approvals:

- Technical Maintainer.

Additional review when public behavior changes.

### 5.4 Class D: security and privacy

Examples:

- network access,
- new parser,
- plugin,
- cache,
- redaction,
- logging.

Required approvals:

- Security Reviewer,
- Technical Maintainer,
- Theory Owner when product boundary changes.

### 5.5 Class E: documentation-only

Examples:

- typo,
- clarification,
- tutorial,
- navigation.

Required approval:

- Documentation Maintainer or Technical Maintainer.

Theory review is required when wording changes meaning.

### 5.6 Class F: emergency security fix

May proceed quickly to protect users.

Required post-action:

- incident record,
- tests,
- release note,
- full review.

Emergency authority does not permit theory redefinition.

---

## 6. Change requirements

Every theory-relevant pull request should include:

```text
Change class:
Trace IDs:
Theory Map IDs:
Product Rule IDs:
Formula IDs:
Decision IDs:
Public fields changed:
Tests changed:
Golden outputs changed:
Evidence classes changed:
Limitations changed:
Security impact:
Licensing impact:
```

### 6.1 No hidden public behavior

A public behavior change requires:

- specification update,
- traceability update,
- tests,
- report-schema update,
- release note.

### 6.2 Internal refactor

An internal refactor should prove no public behavior change through tests.

### 6.3 Deferred scope

A deferred feature cannot enter implementation through an unrelated pull request.

---

## 7. Phase governance

### 7.1 Phase approval

A phase begins only after:

- prior phase passes,
- blocking decisions close,
- scope is explicit.

### 7.2 Phase completion

A phase completes only after:

- deliverables exist,
- acceptance tests pass,
- required reviewers approve,
- later-phase work remains excluded.

### 7.3 Stop rule

Work stops when:

- a blocking decision is open,
- a conflict exists,
- a metric lacks ownership,
- a phase gate fails.

---

## 8. Decision register

`UNRESOLVED_DECISIONS.md` is the formal decision register for v0.1.

### 8.1 Decision states

```text
OPEN
RECOMMENDED
APPROVED
DEFERRED
REJECTED
SUPERSEDED
```

### 8.2 Approved decisions

Only `APPROVED` decisions authorize implementation.

### 8.3 Deferred decisions

Deferred decisions must not power public v0.1 behavior.

### 8.4 Decision change

A changed decision must:

- retain ID,
- preserve history,
- update downstream specs,
- identify implementation impact.

---

## 9. Official release labels

Recommended labels:

```text
experimental
reviewed
official-v0.1
```

Related decision:

```text
UD-032
```

### 9.1 Experimental

Minimum requirements:

- bounded scope,
- basic tests,
- assumptions,
- limitations,
- visible experimental label.

### 9.2 Reviewed

Minimum requirements:

- documentation,
- tests,
- traceability,
- relevant reviewer acceptance.

### 9.3 Official v0.1

Minimum requirements:

- all release gates,
- Theory Owner approval,
- Technical Maintainer approval,
- validation summary,
- license coherence,
- no release blocker.

### 9.4 No ambiguous status

A feature should not be described as reviewed or official without the corresponding evidence.

---

## 10. Canonical repository and release identity

Official releases should identify:

- canonical repository,
- release tag,
- commit hash,
- toolkit version,
- report schema version,
- theory versions,
- validation status,
- release label.

### 10.1 Forks

Forks are permitted under the code license.

Forks should identify:

- modifications,
- maintainer,
- compatibility,
- theory basis,
- nonofficial status.

### 10.2 Compatibility claims

Compatibility should mean passing the published conformance suite.

### 10.3 Official naming

A future naming policy may protect users from confusing unofficial forks with canonical releases.

---

## 11. Contribution workflow

### 11.1 Issue first for large changes

Large public changes should begin with:

- issue,
- problem statement,
- proposed owner IDs,
- scope,
- alternatives,
- expected tests.

### 11.2 Pull request scope

Each pull request should remain small enough to review.

### 11.3 Required tests

Contributions changing behavior must add or update tests.

### 11.4 Private data

Contributions must not include private datasets.

### 11.5 License

Contributors agree to the license of the target asset class.

### 11.6 Attribution

Substantial contributions should be credited through repository history and release notes.

---

## 12. Review procedure

### 12.1 Theory review questions

- Does the change preserve conceptual meaning?
- Does it overclaim?
- Does it confuse exact and structural domains?
- Does it weaken unavailable conclusions?
- Does it create a hidden score?

### 12.2 Mathematical review questions

- Are formulas correct?
- Are denominators explicit?
- Are units stable?
- Are expected values independent?
- Are assumptions visible?

### 12.3 Technical review questions

- Is code readable?
- Is behavior deterministic?
- Are modules bounded?
- Are dependencies justified?
- Are failure modes clear?

### 12.4 Security review questions

- Does data leave the machine?
- Can input execute code?
- Are paths safe?
- Are logs content-safe?
- Does redaction work?

### 12.5 Domain review questions

- Is output useful?
- Is language understandable?
- Are recommendations actionable?
- Could users overread the result?

---

## 13. Dispute resolution

### 13.1 Theory-meaning dispute

Theory Owner has final authority over official project interpretation.

### 13.2 Mathematical dispute

The Mathematical Reviewer should provide:

- derivation,
- counterexample,
- test,
- proposed resolution.

If interpretation changes, Theory Owner approval is required.

### 13.3 Technical dispute

Technical Maintainer decides among implementations that preserve approved behavior.

### 13.4 Security dispute

The safer behavior should prevail until review closes.

### 13.5 Public record

Material disputes should be recorded in:

- issue,
- decision entry,
- architecture note,
- release note.

---

## 14. Release process

### 14.1 Release candidate

The Release Manager prepares:

- version bump,
- changelog,
- validation summary,
- benchmark,
- license package,
- theory-source manifest,
- known limitations.

### 14.2 Required approvals

Official v0.1 requires:

- Theory Owner,
- Technical Maintainer.

Also required when applicable:

- Mathematical Reviewer,
- Security Reviewer,
- Domain Validator.

### 14.3 Tagging

Recommended tag:

```text
v0.1.0
```

### 14.4 Release artifacts

- source archive,
- wheel,
- source distribution,
- JSON schema or report schema,
- example files,
- validation summary,
- license files,
- release notes.

### 14.5 Immutable release record

Official release artifacts should not be replaced silently.

Corrections should use a new version.

---

## 15. Versioning

### 15.1 Software versioning

Recommended semantic versioning.

### 15.2 Development versions

Recommended:

```text
0.1.0.devN
```

### 15.3 Patch release

Use for:

- bug fix,
- security fix,
- no intentional public meaning change.

### 15.4 Minor release

Use for:

- backward-compatible capability,
- optional new report field,
- new supported input.

### 15.5 Major release

Use for:

- breaking schema,
- changed metric meaning,
- changed parent encoding,
- changed theory contract,
- changed evidence class.

### 15.6 Theory version

Software version and theory version remain separate.

---

## 16. Release notes

Every release note should identify:

- public fields added,
- public fields changed,
- evidence-class changes,
- formula changes,
- theory-version changes,
- schema changes,
- migration instructions,
- known limitations,
- security fixes,
- deferred features.

---

## 17. Security response

### 17.1 Private reporting

The repository should provide a private security-report path when available.

### 17.2 Triage

Security issues should be classified:

- critical,
- high,
- medium,
- low.

### 17.3 Fix priority

Critical and high issues receive priority over feature work.

### 17.4 Disclosure

Coordinate disclosure when a public exploit description would put users at risk.

### 17.5 Emergency release

Emergency release may bypass normal timing.

It must still preserve:

- tests,
- license,
- changelog,
- incident record.

---

## 18. Deprecation

### 18.1 Public field deprecation

A field should be deprecated before removal when practical.

### 18.2 Deprecation notice

Include:

- replacement,
- reason,
- removal target,
- migration example.

### 18.3 Meaning changes

Do not reuse an old field name for a new meaning.

### 18.4 Deferred versus deprecated

- deferred: not yet implemented,
- deprecated: implemented but scheduled for removal.

---

## 19. Handoff objectives

A future maintainer should be able to assume responsibility without losing:

- theory meaning,
- repository history,
- release evidence,
- issue context,
- test fixtures,
- official identity,
- security knowledge,
- licensing boundaries.

---

## 20. Handoff package

The minimum handoff package should contain:

```text
README.md
PROJECT_INSTRUCTIONS.md
V0.1_PRODUCT_SPEC.md
DEFINITIONS_AND_UNITS.md
DATA_AND_PROVENANCE_SPEC.md
OBSERVABILITY_AND_REPORTING.md
THEORY_SOURCE_MAP.md
THEORY_TO_CODE_TRACEABILITY.md
VALIDATION_PLAN.md
PRIVACY_AND_DATA_HANDLING.md
LICENSING_NOTES.md
SUCCESS_CRITERIA.md
GOVERNANCE_AND_HANDOFF.md
UNRESOLVED_DECISIONS.md
THEORY_SOURCES.md
CHANGELOG.md
CONTRIBUTING.md
SECURITY.md
release validation summaries
```

### 20.1 Repository state

Preserve:

- full Git history,
- tags,
- branches,
- issues,
- pull requests,
- discussions,
- release artifacts.

### 20.2 Credentials

Credentials should be transferred through secure external processes.

They must not be stored in repository files.

---

## 21. Maintainer onboarding

A new Technical Maintainer should complete:

1. read Project instructions,
2. read theory-source map,
3. run hero example,
4. run full tests,
5. reproduce golden outputs,
6. review open decisions,
7. review security posture,
8. build a release candidate locally,
9. confirm license files,
10. shadow one reviewed change.

### 21.1 Theory onboarding

A maintainer changing theory-relevant behavior should review:

- primary theory article,
- entropy boundary article,
- supplementary registry,
- Trace IDs,
- unavailable conclusions.

---

## 22. Succession

### 22.1 Theory Owner succession

A future Theory Owner designation should be explicit and public.

### 22.2 Technical Maintainer succession

A new maintainer should be appointed through:

- Theory Owner approval,
- repository announcement,
- documented access transfer.

### 22.3 Temporary absence

A backup maintainer may handle:

- security fixes,
- packaging fixes,
- CI fixes.

Theory-relevant changes should wait unless delegated authority exists.

### 22.4 Project dormancy

If the project becomes inactive:

- repository remains available,
- official release status remains historical,
- forks remain permitted,
- no fork becomes official automatically.

---

## 23. Bus-factor reduction

The project should reduce single-person dependence through:

- explicit specifications,
- golden fixtures,
- traceability,
- decision history,
- release scripts,
- architecture documentation,
- documented credentials inventory outside the repository.

---

## 24. Governance artifacts

Recommended files:

```text
CONTRIBUTING.md
CODE_OF_CONDUCT.md
SECURITY.md
CHANGELOG.md
THEORY_SOURCES.md
THIRD_PARTY_NOTICES.md
MAINTAINERS.md
```

### 24.1 MAINTAINERS file

Should list:

- role,
- person,
- scope,
- contact method,
- appointment date.

### 24.2 Code of conduct

A standard code of conduct may support collaboration.

It should not replace technical review criteria.

---

## 25. Roadmap governance

### 25.1 Roadmap status

Roadmap items should use:

```text
proposed
approved
in_progress
experimental
reviewed
released
deferred
rejected
```

### 25.2 No roadmap authority

A roadmap entry does not authorize implementation without decisions and phase approval.

### 25.3 v0.2 candidates

Potential later work:

- effective source diversity,
- OpenLineage adapter,
- ML Metadata adapter,
- semantic representation modules,
- amplification branch,
- controlled intervention schema,
- additional domain fixtures.

---

## 26. Metrics governance

### 26.1 New metric proposal

A proposal must include:

- problem,
- theory basis,
- formula,
- unit,
- observability,
- evidence class,
- module owner,
- tests,
- report field,
- limitation.

### 26.2 Rejected metric pattern

Reject:

- opaque combined score,
- score without unit,
- metric without denominator,
- theory claim without source,
- proxy presented as fact.

### 26.3 Threshold governance

A threshold requires:

- source,
- calibration,
- false-positive review,
- versioning,
- domain scope.

---

## 27. Schema governance

### 27.1 Schema owner

Technical Maintainer owns schema implementation.

Theory Owner approves meaning changes.

### 27.2 Breaking change

Requires:

- major schema version,
- migration path,
- fixture update,
- report update,
- release note.

### 27.3 Enum addition

Requires:

- definition,
- unknown behavior,
- mapping behavior,
- report behavior,
- tests.

---

## 28. Documentation governance

### 28.1 Canonical definitions

Documentation should link to canonical definitions rather than creating parallel meanings.

### 28.2 Examples

Examples must match current behavior.

### 28.3 Draft markers

Official docs must not contain:

- internal notes,
- placeholders,
- unresolved editorial comments.

### 28.4 AI-generated drafts

AI-assisted documentation requires human review for:

- accuracy,
- licensing,
- traceability,
- public tone.

---

## 29. Repository permissions

Recommended:

- protected main branch,
- required CI,
- required review,
- restricted release permission,
- restricted security-setting permission.

### 29.1 Theory-relevant paths

Changes to theory and traceability files should require Theory Owner review where platform controls permit.

### 29.2 Security-sensitive paths

Changes to loaders, mapping, redaction, and dependencies should require Security Reviewer or Technical Maintainer review.

---

## 30. Governance acceptance tests

Governance is successful when:

- every official release has approvals,
- every public field has ownership,
- decisions are preserved,
- deferred scope stays deferred,
- security changes receive review,
- a new maintainer can reproduce the hero and release process,
- official and fork identities remain distinguishable.

Recommended checks:

```text
test_governance_required_files_exist
test_release_has_validation_summary
test_release_has_theory_source_manifest
test_public_fields_have_owners
test_open_blocking_decisions_zero
test_official_tag_matches_release_metadata
```

---

## 31. Handoff rehearsal

Before official v0.1, conduct one handoff rehearsal.

A reviewer who did not author the implementation should:

1. clone repository,
2. install package,
3. run hero,
4. locate definitions,
5. locate trace owner for one metric,
6. run one unit test,
7. build package,
8. identify release blockers,
9. explain unavailable conclusions.

Record results in:

```text
HANDOFF_REHEARSAL.md
```

---

## 32. Governance failure conditions

Release or governance must stop when:

- theory meaning changes without Theory Owner review,
- a formula changes without mathematical review,
- a network feature ships without security review,
- a public field has no owner,
- a golden change lacks approval,
- an official release lacks validation evidence,
- a fork is presented as canonical without authority,
- a blocking decision remains open,
- a contributor adds private data,
- licensing boundaries are ignored.

---

## 33. Decision dependencies

| Decision | Governance effect |
|---|---|
| `UD-001` | dual authority model |
| `UD-017` | phase split |
| `UD-023` | license split |
| `UD-024` | theory-PDF policy |
| `UD-026` | naming |
| `UD-032` | release labels |
| `UD-033` | hero baseline |

---

## 34. Approval

### Theory Owner decision

- [ ] Approve governance and handoff baseline
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

- [ ] Review paths are implementable.
- [ ] Release workflow is feasible.
- [ ] Handoff package is complete enough.
- [ ] Repository protections can support the model.

Technical notes:

```text

```

Maintainer:

```text

```

Date:

```text

```

### Mathematical Reviewer acknowledgment

- [ ] Mathematical authority is clear.
- [ ] Formula changes require review.
- [ ] Test evidence is preserved.

Reviewer notes:

```text

```

Reviewer:

```text

```

Date:

```text

```

### Security Reviewer acknowledgment

- [ ] Security-review triggers are clear.
- [ ] Emergency process is defined.
- [ ] Sensitive paths receive appropriate review.

Security notes:

```text

```

Reviewer:

```text

```

Date:

```text

```

### Domain Validator acknowledgment

- [ ] Domain-review responsibility is clear.
- [ ] User-facing claims receive review.
- [ ] Handoff does not depend on private author knowledge.

Domain notes:

```text

```

Validator:

```text

```

Date:

```text

```

---

## 35. Change-control rule

After approval:

1. role authority must not change silently,
2. official release labels require documented evidence,
3. theory-relevant changes require Theory Owner review,
4. mathematical changes require mathematical review,
5. network and executable-input changes require security review,
6. schema changes require migration and tests,
7. a fork does not become official automatically,
8. handoff documents must remain current,
9. repository history and decisions must be preserved,
10. governance should support contribution without allowing conceptual drift.
