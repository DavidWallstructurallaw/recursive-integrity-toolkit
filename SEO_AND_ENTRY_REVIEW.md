# Discovery and entry review

Reviewed: 2026-10-06. Scope: repository entry copy and existing documentation.
No capability, scientific definition, dependency or runtime behavior is added.
This is a task-fit assessment from current primary sources. Search volume,
conversion rates, ranking gains and commercial demand were not measured.

## Recommended position

Audit synthetic training data for missing categories, provenance gaps, and
concentrated ancestry. Lead with the user's dataset question, show a real report
result, and offer one local command before linking detailed contracts.

The strongest audience is a research or data engineer who already exports
synthetic or mixed training data after generation, filtering or reuse. Inputs
need declared representations and, for lineage results, supplied provenance.

## Current demand signals

| Primary source | Observed problem | Existing capability and limit |
| --- | --- | --- |
| [NVIDIA, July 9, 2026](https://developer.nvidia.com/blog/synthetic-data-generation-for-financial-ai-research-with-nvidia-nemo/) | An iterative synthetic-data workflow adjusts category weights and checks duplication across repeated rounds. | Audit category support, frequency and diversity before/after curation. The toolkit's exact-duplicate analysis does not implement NVIDIA's semantic deduplication. |
| [Synthetic Eggs in Many Baskets, ACL Findings, July 2026](https://aclanthology.org/2026.findings-acl.360/) | Experiments investigate how synthetic-source diversity changes fine-tuned model behavior. | Record declared source-type composition and representation-bound diversity. Declared human/synthetic shares do not measure generator diversity or prove model robustness. |
| [RLVR Datasets and Where to Find Them, May 26, 2026 preprint](https://arxiv.org/html/2605.26971v1) | The authors trace many training datasets to shared upstream sources. | Calculate concentration and coverage from supplied parent graphs. This toolkit does not reconstruct missing lineage or implement the paper's semantic matching, leakage detection or performance scoring. |
| [When Sample Selection Bias Precipitates Model Collapse, ICML 2026](https://proceedings.mlr.press/v306/qiao26c.html) | The paper examines tail loss under biased selection in recursive synthetic-data pipelines. | Compare observed category loss and declared-tail diagnostics across ordered exports. Observed loss alone does not identify a cause or predict model failure. |

These sources establish active engineering and research problems. They do not
validate this toolkit, endorse it, or demonstrate its results on those datasets.
The keyword priorities below are an inference from capability fit.

## Search intent and entry placement

| Priority | Search family | Entry that answers it |
| --- | --- | --- |
| Primary | synthetic data audit; synthetic training data audit | README opening, purpose table and installed local demo |
| Primary | dataset diversity; topic coverage; rare-category coverage | Concrete support 8 to 5 example and declared representation explanation |
| Primary | training data provenance; dataset lineage analysis | Missing-row coverage and supplied-root concentration explanation |
| Secondary | compare dataset versions; synthetic dataset comparison | Three-version example, disappearance/reappearance and chronology requirements |
| Supporting | recursive training; model collapse research | Bounded research-use paragraph with explicit unavailable predictions |
| Supporting | exact duplicate diagnostics; local Python data audit | Content-hash boundary, offline runtime and CLI/API links |

Avoid using AI text detection, collapse detector/prevention, semantic quality,
automatic provenance verification, compliance certification or synthetic-data
generation as product promises. Broad data-quality terms require the specific
coverage/provenance/lineage qualifier. Category coverage and exact duplicates
are useful features but do not establish a unique market position.

## Adjacent tools

| Tool and official reference | Documented task | Complementary toolkit use |
| --- | --- | --- |
| [NeMo Curator](https://docs.nvidia.com/nemo/curator/latest/curate-text/process-data/deduplication) | Exact, fuzzy and semantic deduplication | Compare declared category coverage and supplied ancestry around curation steps. No built-in adapter or semantic-deduplication claim. |
| [SDMetrics](https://docs.sdv.dev/sdmetrics/data-metrics/quality) | Statistical synthetic-tabular quality comparisons | Audit ordered dataset snapshots together with supplied lineage. No claim that category coverage is unique. |
| [Evidently](https://docs.evidentlyai.com/metrics/preset_data_drift) | Current/reference data-drift metrics | Inspect explicit snapshots and ancestry without claiming production monitoring or significance testing. |

## Implemented entry changes

- README opens with the concrete audit job and common questions.
- The first example shows inspectable results and links the independent oracle.
- A workflow table routes users to version comparison, shared ancestry or simulation.
- Own-data guidance names canonical inputs and links sample records/configuration.
- Detailed commands, Python examples, historical timings and caveats are retained
  in `docs/getting_started.md` with corrected relative links.
- Active CLI/data/report guides are corrected where they still described dev5,
  schema 1.2, single-pair-only CLI behavior or unopened simulation fields.
  Historical evidence and schema-family introduction dates remain unchanged.

The README is also the package long description. Its change requires refreshed
wheel/sdist metadata and scoped installed checks before those new bytes can be
used for publication. Existing full runtime evidence retains its original source
identity; see `RELEASE_0_1_0.md` for the recorded verification scope.

## Repository metadata applied, 2026-10-06

Before this update, GitHub About read:

> An auditable, local-first research toolkit for analyzing recursive closure risk in synthetic-data training pipelines.

The repository previously had no topics. On 2026-10-06, the user authorized
browser editing and confirmed the acting Technical Maintainer role. The following
description and eleven topics were saved through the repository About editor;
the saved UI and the GitHub repository API both confirm the exact values.
Website and other repository settings were left unchanged.

Applied About description:

> Audit synthetic training data for category loss, provenance gaps and shared ancestry. Local Python CLI with dataset comparisons and JSON/Markdown reports.

Applied topics:

```text
synthetic-data
training-data
data-provenance
data-lineage
dataset-audit
data-quality
dataset-comparison
reproducible-research
machine-learning
python
cli
```

README changes were prepared on `release-0.1.0` in PR #5. They become the default
repository landing page when that PR is merged. Xiangyu Guo is now the acting
Technical Maintainer. On 2026-10-06 the user accepted the handoff and authorized
merging PR #5 and publishing v0.1.0. The release entry now uses the immutable
v0.1.0 tag; refreshed package descriptions and final artifact identities are
recorded in RELEASE_0_1_0.md and the GitHub Release.
