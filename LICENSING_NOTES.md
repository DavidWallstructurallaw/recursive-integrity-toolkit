# LICENSING_NOTES

## Document control

| Field | Value |
|---|---|
| Project | Recursive Integrity Toolkit |
| Target release | v0.1 |
| Phase | Phase 0 |
| Status | APPROVED PHASE 0 BASELINE |
| Primary owner | Theory Owner |
| Reviewers | Technical Maintainer, optional legal reviewer |
| Depends on | `UNRESOLVED_DECISIONS.md`, `V0.1_PRODUCT_SPEC.md`, `GOVERNANCE_AND_HANDOFF.md` |
| Purpose | Define the recommended license split, asset boundaries, attribution, contribution terms, theory-reference handling, third-party notices, naming control, and release checks |

This file documents the intended licensing structure of Recursive Integrity Toolkit v0.1.

It is a project-governance document.

It does not replace legal advice.

The project contains distinct asset classes:

- source code,
- reusable specifications,
- general documentation,
- example datasets,
- tests and fixtures,
- theory publications,
- third-party materials,
- project name and release identity.

These assets should not be treated as though one license automatically governs all of them.

---

## 1. Licensing objectives

The licensing structure should support:

- public inspection,
- code reuse,
- forks,
- contributions,
- commercial implementation of the software,
- attribution to the theory source,
- preservation of the author's chosen theory-publication terms,
- clear separation between official releases and third-party forks,
- low legal ambiguity for users and contributors.

---

## 2. Recommended asset split

| Asset class | Recommended license | Status |
|---|---|---|
| Source code | Apache License 2.0 | recommended |
| Reusable specifications | CC BY 4.0 | recommended |
| General repository documentation | CC BY 4.0 or Apache-2.0 where code-adjacent | recommended split |
| Example datasets created for the repository | CC BY 4.0 | recommended |
| Test fixtures created for the repository | CC BY 4.0, unless code-like | recommended |
| Test code | Apache License 2.0 | recommended |
| Theory PDFs | retain their existing license | required separation |
| Third-party materials | original license | required |
| Project name and official-release designation | governed separately from copyright | recommended |

Related decision:

```text
UD-023
```

---

## 3. Source-code license

### 3.1 Recommended license

```text
Apache License 2.0
```

### 3.2 Reasons

Apache-2.0 provides:

- permission to use,
- permission to modify,
- permission to redistribute,
- permission for commercial use,
- an explicit patent license,
- established open-source compatibility,
- notice requirements that fit a theory-led reference implementation.

### 3.3 Repository file

The repository root should contain:

```text
LICENSE
```

with the complete Apache License 2.0 text.

### 3.4 Code headers

Per-file license headers are optional unless project policy later requires them.

A short header may identify:

- copyright owner,
- SPDX identifier.

Recommended SPDX identifier:

```text
Apache-2.0
```

### 3.5 Test code

Python test code belongs under Apache-2.0.

---

## 4. Specifications and documentation

### 4.1 Recommended license

```text
Creative Commons Attribution 4.0 International
```

SPDX-style identifier:

```text
CC-BY-4.0
```

### 4.2 Covered material

Recommended CC BY 4.0 coverage:

- `PROJECT_INSTRUCTIONS.md`
- `V0.1_PRODUCT_SPEC.md`
- `DEFINITIONS_AND_UNITS.md`
- `DATA_AND_PROVENANCE_SPEC.md`
- `OBSERVABILITY_AND_REPORTING.md`
- `THEORY_TO_CODE_TRACEABILITY.md`
- `VALIDATION_PLAN.md`
- `PRIVACY_AND_DATA_HANDLING.md`
- `SUCCESS_CRITERIA.md`
- `GOVERNANCE_AND_HANDOFF.md`
- public architecture documentation,
- report-schema documentation,
- tutorials.

### 4.3 Rationale

CC BY 4.0 permits:

- adaptation,
- redistribution,
- commercial reuse,
- translation,
- reuse in other governance systems,

with attribution.

### 4.4 Code-adjacent documentation

Files that are primarily package metadata or code configuration may remain under Apache-2.0.

Examples:

- `pyproject.toml`
- CI configuration
- command examples embedded in code packages.

### 4.5 Single-license alternative

A simpler alternative is to place code and repository Markdown under Apache-2.0.

This reduces license boundaries but gives up the familiar documentation-specific CC BY framing.

The final choice is controlled by `UD-023`.

---

## 5. Example datasets and fixtures

### 5.1 Repository-created examples

Recommended license:

```text
CC BY 4.0
```

### 5.2 Test code versus test data

- test code: Apache-2.0,
- fixture data: CC BY 4.0,
- golden output generated from repository fixture: CC BY 4.0 unless treated as code-adjacent output.

### 5.3 Synthetic content

Repository fixtures should use content created for the project.

### 5.4 Third-party examples

A third-party dataset must preserve:

- source,
- license,
- attribution,
- modification notice,
- redistribution permission.

### 5.5 No uncertain redistribution

Do not include a third-party dataset when redistribution rights are unclear.

A download script may be considered later, but it would introduce network and privacy implications and remains outside core v0.1.

---

## 6. Theory publications

### 6.1 Separate asset class

The theory PDFs are reference works.

They do not become software merely because the implementation is based on them.

### 6.2 Existing theory license

The uploaded theory works currently state:

```text
Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International
```

Common identifier:

```text
CC-BY-NC-ND-4.0
```

### 6.3 Consequences for repository handling

The theory license should remain separate from:

- code license,
- specification license,
- example-data license.

### 6.4 Public repository recommendation

Recommended default:

- preserve full citations,
- preserve DOI or canonical publication links,
- preserve version identifiers,
- include a theory-source manifest,
- keep full PDFs in the private Project source bundle,
- exclude full PDFs from the public code repository unless the Theory Owner deliberately approves redistribution there.

Related decision:

```text
UD-024
```

### 6.5 No modified theory PDF

A public repository must not distribute modified versions of a no-derivatives theory PDF.

### 6.6 Implementation independence

The open-source code and reusable specifications should be independently licensed.

Users should not need permission under the theory-PDF license to:

- run the software,
- fork the code,
- modify the code,
- create compatible implementations.

### 6.7 Attribution

The repository should state that the toolkit is theory-led and cite:

- *The Universal Inbreeding Law v2*
- *Entropy as a Structural Boundary Condition, Not a Causal Force v2*
- *Supplementary Case Registry for the Universal Inbreeding Law, Version 2.0*

---

## 7. Theory source manifest

Recommended file:

```text
THEORY_SOURCES.md
```

Recommended fields:

| Field | Description |
|---|---|
| title | canonical title |
| author | Xiangyu Guo |
| version | cited version |
| publication date | date |
| DOI | canonical DOI where available |
| canonical URL | publication location |
| license | theory license |
| role | mathematical source, interpretation source, case registry |
| repository inclusion | citation only or included file |
| checksum | optional local source-bundle hash |

### 7.1 Version pinning

Official releases should identify the exact theory versions used.

### 7.2 Later theory revisions

A new theory version does not silently change an existing software release.

A toolkit update should record:

- old theory version,
- new theory version,
- affected Trace IDs,
- changed definitions,
- changed tests,
- release notes.

---

## 8. NOTICE file

Recommended root file:

```text
NOTICE
```

Suggested content categories:

- project name,
- primary copyright,
- theory attribution,
- documentation license notice,
- third-party attribution summary,
- official repository reference.

### 8.1 Apache notice preservation

Redistributors must preserve notices as required by Apache-2.0.

### 8.2 Theory notice

The NOTICE file should state that theory publications retain their own licenses.

---

## 9. README licensing section

The README should explain:

- code license,
- documentation license,
- example-data license,
- theory-publication license,
- third-party-material rule.

Suggested concise structure:

```text
Code: Apache-2.0
Specifications and documentation: CC BY 4.0
Repository-created example data: CC BY 4.0
Theory publications: retain their stated licenses
Third-party assets: retain their original licenses
```

---

## 10. Attribution requirements

### 10.1 Code attribution

Follow Apache-2.0 notice requirements.

### 10.2 Documentation attribution

CC BY 4.0 reuse should identify:

- author or project,
- title where practical,
- source,
- license,
- modification indication.

### 10.3 Modified specifications

A modified specification should clearly state:

- that it was modified,
- who modified it,
- whether it remains compatible,
- whether it is an official project specification.

### 10.4 Theory attribution

Do not present modified implementation documentation as though it were a modified theory publication.

---

## 11. Contributions

### 11.1 Code contributions

Recommended rule:

Contributions are accepted under the repository code license.

### 11.2 Documentation contributions

Contributions to CC BY 4.0 documentation are accepted under CC BY 4.0.

### 11.3 Contribution agreement

v0.1 does not require a CLA by default.

### 11.4 Developer Certificate of Origin

A Developer Certificate of Origin may be added later.

It should not block the initial reference implementation unless maintainers need it.

### 11.5 Contribution notice

Recommended `CONTRIBUTING.md` statement:

> By submitting a contribution, you agree that it may be distributed under the license applicable to the target file or asset class.

### 11.6 Contributor authority

Contributors must submit material they have the right to contribute.

### 11.7 No private datasets

Contributors should not include private or restricted datasets in issues, tests, or pull requests.

---

## 12. Third-party dependencies

### 12.1 Dependency review

Every dependency should be reviewed for:

- license,
- required notices,
- compatibility with Apache-2.0,
- optional or required status,
- bundled assets,
- model or dataset licenses.

### 12.2 Dependency inventory

Recommended generated file:

```text
THIRD_PARTY_NOTICES.md
```

### 12.3 Lockfile metadata

Dependency lockfiles do not replace third-party notice review.

### 12.4 Copyleft dependencies

Strong copyleft dependencies require explicit review before inclusion.

### 12.5 Optional extras

Optional dependency notices remain required when the optional feature is distributed or installed.

---

## 13. Third-party code and snippets

### 13.1 Copying code

Do not copy code from incompatible or unclear sources.

### 13.2 Generated code

AI-generated code still requires review for:

- copied fragments,
- license headers,
- attribution,
- dependency introduction.

### 13.3 External examples

External examples should be rewritten or cited according to their license.

---

## 14. Report outputs

### 14.1 User data ownership

The project license does not claim ownership over user-supplied datasets.

### 14.2 Generated audit reports

Users control reports generated from their own inputs, subject to rights in the underlying data and included project documentation.

### 14.3 Boilerplate report text

Standard report templates may remain under the documentation license.

### 14.4 Sensitive data

Licensing permission does not override privacy, confidentiality, or data-protection obligations.

---

## 15. Naming and official releases

### 15.1 Copyright versus naming

Open-source licensing permits forks and modified distributions.

It does not require every fork to be presented as an official project release.

### 15.2 Official-release identity

The project should reserve these designations for approved releases:

```text
Recursive Integrity Toolkit
official-v0.1
official release
canonical implementation
```

Exact trademark policy may be developed later.

### 15.3 Fork labeling

Forks should identify:

- that they are modified,
- their repository,
- their maintainer,
- their compatibility status,
- their theory-version basis.

### 15.4 Compatibility claims

A fork should not claim full compatibility without passing the public conformance suite.

### 15.5 Project name reuse

A future naming policy may allow descriptive use while restricting confusing official branding.

---

## 16. License file layout

Recommended repository layout:

```text
LICENSE
NOTICE
LICENSES/
├── Apache-2.0.txt
├── CC-BY-4.0.txt
└── CC-BY-NC-ND-4.0-reference.txt
LICENSING_NOTES.md
THIRD_PARTY_NOTICES.md
THEORY_SOURCES.md
```

### 16.1 SPDX file annotations

Where practical, files may include:

```text
SPDX-License-Identifier: Apache-2.0
```

or:

```text
SPDX-License-Identifier: CC-BY-4.0
```

### 16.2 Theory reference text

Including the CC BY-NC-ND license text does not change the license of other files.

---

## 17. Repository file-class matrix

| Path class | Recommended license |
|---|---|
| `src/**/*.py` | Apache-2.0 |
| `tests/**/*.py` | Apache-2.0 |
| `pyproject.toml` | Apache-2.0 |
| `.github/**` | Apache-2.0 |
| root specifications | CC BY 4.0 |
| `docs/**` | CC BY 4.0 |
| `examples/**/*.csv` | CC BY 4.0 |
| `examples/**/*.json` | CC BY 4.0 |
| golden Markdown and JSON | CC BY 4.0 |
| full theory PDFs | existing theory license |
| third-party files | original license |

---

## 18. License compatibility checks

Before release, verify:

- Apache-2.0 text included,
- CC BY 4.0 text or link included in license bundle,
- theory assets clearly separated,
- third-party notices complete,
- example data redistributable,
- no unknown-license code,
- no no-derivatives content modified,
- README matches actual file licensing.

---

## 19. Publication package

An official release should include:

- source archive,
- wheel and source distribution,
- license files,
- NOTICE,
- theory-source manifest,
- third-party notices,
- release notes,
- validation summary.

### 19.1 Zenodo or archival release

An archival release may include:

- repository snapshot,
- release tag,
- specification version,
- theory-version references,
- validation summary.

Whether full theory PDFs are included depends on the Theory Owner's explicit publication choice.

---

## 20. License acceptance tests and checks

Recommended automated checks:

```text
test_license_root_file_exists
test_notice_file_exists
test_spdx_headers_valid_where_required
test_public_files_have_declared_asset_class
test_third_party_notice_entries_resolve
test_theory_files_not_misclassified_as_apache
test_no_modified_no_derivatives_pdf_in_release
```

Recommended manual checks:

- dependency-license review,
- example-data review,
- README license review,
- theory citation review.

---

## 21. Release blockers

Release must stop if:

- no code license exists,
- theory PDFs are presented as Apache-2.0 software,
- third-party code has unknown licensing,
- a no-derivatives theory work is modified and redistributed,
- repository documentation claims a license different from its actual notice,
- example data lacks redistribution rights,
- a contributor submits code without authority to license it,
- required notices are missing.

---

## 22. Decision dependencies

| Decision | Licensing effect |
|---|---|
| `UD-023` | code and documentation license split |
| `UD-024` | public theory-PDF inclusion |
| `UD-026` | package and repository naming |
| `UD-032` | official release labels |

---

## 23. Recommended v0.1 decision

Recommended baseline:

```text
Code: Apache-2.0
Specifications and documentation: CC BY 4.0
Repository-created examples: CC BY 4.0
Theory publications: retain stated license
Public repository: citations and theory-source manifest by default
Private Project bundle: full authoritative PDFs
```

---

## 24. Approval

### Theory Owner decision

- [ ] Approve licensing baseline
- [ ] Approve single Apache-2.0 repository alternative
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

- [ ] Asset classes can be separated.
- [ ] Package files can use Apache-2.0.
- [ ] Documentation notices can use CC BY 4.0.
- [ ] Theory files can remain separate.
- [ ] Third-party notices can be generated and reviewed.

Technical notes:

```text

```

Maintainer:

```text

```

Date:

```text

```

### Optional legal review

Reviewer:

```text

```

Review date:

```text

```

Notes:

```text

```

---

## 25. Change-control rule

After approval:

1. a file must not change asset class silently,
2. a new dependency requires license review,
3. a third-party fixture requires redistribution review,
4. a theory-file inclusion change requires Theory Owner approval,
5. a documentation-license change requires NOTICE and README updates,
6. an official naming policy must remain separate from code permissions,
7. release archives must contain coherent notices,
8. contributor terms must match the target file license,
9. licensing convenience must not erase theory-publication boundaries.
