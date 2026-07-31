# THEORY_SOURCE_MAP

## Document control

| Field | Value |
|---|---|
| Project | Recursive Integrity Toolkit |
| Target release | v0.1 |
| Phase | Phase 0: theory extraction and implementation eligibility |
| Status | APPROVED PHASE 0 BASELINE |
| Implementation code produced | None |
| Depends on | `SPEC_AUDIT.md` |
| Primary function | Map authoritative theory passages to mathematical objects, implementation eligibility, observability requirements, tests, report fields, and prohibited overclaims |

This file is the canonical theory-source index for the Recursive Integrity Toolkit. It identifies which parts of the uploaded theory corpus may control v0.1 behavior, which parts provide interpretive boundaries, which parts serve only as validation witnesses, and which parts remain deferred.

The map is designed to prevent five common failures:

1. turning a structural theory claim into an unsupported numerical score,
2. treating an analogy as a shared equation,
3. presenting a simulation as an observed fact,
4. allowing implementation conventions to masquerade as theory,
5. expanding v0.1 merely because a valid theory branch exists.

The map does not replace the source articles. When interpretation is disputed, the cited source passage remains authoritative.

---

## 1. Authoritative theory corpus

### TS1. Primary law and mathematical source

**Title:** *The Universal Inbreeding Law v2*  
**Role:** Primary theory source for closure, diversity contraction, rare-state extinction, inherited deviation, absorption, and external reopening.  
**Highest-authority sections for v0.1:**

- Executive Summary and Abstract, pages 1-3
- Theory and entropy boundary, pages 4-5
- Mathematical core, pages 6-9
- Mechanism of collapse, pages 9-10
- AI evidence, pages 11-12
- Discussion, limits, and conclusion, pages 14-17

**Source strength inside v0.1:**

- exact stochastic source for finite closed resampling,
- structural source for closure and integrity decay,
- interpretive boundary for concentration versus functional failure,
- cross-domain source only where the paper explicitly limits identical mathematics.

### TS2. Entropy interpretation source

**Title:** *Entropy as a Structural Boundary Condition, Not a Causal Force v2*  
**Role:** Governs causal language, entropy language, open-system interpretation, and the separation between local mechanism and structural boundary.  
**Highest-authority sections for v0.1:**

- Introduction and misconceptions, pages 1-2
- Thermodynamic boundary and emergent irreversibility, pages 3-4
- Information and AI systems, pages 5-6
- Why entropy requires no additional force, pages 7-9
- Category errors and conclusion, pages 9-11

**Source strength inside v0.1:**

- interpretive constraint,
- report-language constraint,
- prohibition on entropy as an independent causal agent,
- justification for evidence-bounded conclusions,
- no direct authorization for a universal entropy score.

### TS3. Supplementary witness and taxonomy source

**Title:** *Supplementary Case Registry for the Universal Inbreeding Law, Version 2.0*  
**Role:** Supplies a contraction-dominant genetic-algorithm witness, an amplification-dominant prion witness, and a taxonomy that keeps these branches distinct.  
**Highest-authority sections for v0.1:**

- Registry purpose and classification, pages 1-3
- Genetic-algorithm mathematical structure, pages 3-6
- GA closure, diversity, correlated error, and corrective channels, pages 6-9
- Prion amplification classification and threshold structure, pages 10-14
- Admission template and versioning policy, page 15

**Source strength inside v0.1:**

- supporting mathematical witness for finite resampling and ancestry concentration,
- future validation fixture source,
- source for contraction versus amplification taxonomy,
- amplification branch deferred from the core v0.1 product.

---

## 2. Authority and use rules

### 2.1 Theory authority

The theory corpus controls:

- the meaning of closure,
- the distinction between difference and noise,
- the relation between internal recursion and external correction,
- the interpretation of diversity contraction,
- the meaning of inherited deviation,
- the boundary between concentration and functional failure,
- causal limits on entropy language,
- the distinction between exact mathematical commonality and structural analogy.

### 2.2 Product authority

Approved v0.1 specifications control:

- file formats,
- field names,
- module ownership,
- report schemas,
- exact validation behavior,
- release sequencing,
- performance targets,
- privacy defaults.

A product convention must be identified as a convention when no theory passage fixes it directly.

### 2.3 Implementation eligibility labels

Every mapped claim receives one status.

| Status | Meaning |
|---|---|
| `APPROVED_DIRECT` | The source supplies a sufficiently exact mathematical or definitional object for direct implementation |
| `APPROVED_DERIVED` | A deterministic metric may be computed from observed inputs under a declared representation |
| `APPROVED_PROXY` | The source supports a warning or ranking, while the output remains heuristic or evidence-limited |
| `APPROVED_SIMULATION` | The source supports a scenario model under explicit assumptions |
| `SUPPORTING_ONLY` | The claim informs interpretation, documentation, or validation but does not power a public metric |
| `DEFERRED` | The theory claim remains outside v0.1 or lacks an approved operational definition |
| `FORBIDDEN` | v0.1 must not implement or claim this result |

### 2.4 Evidence classes

A report field must be assigned to one evidence class:

- `observed_fact`
- `derived_metric`
- `proxy_signal`
- `simulation`
- `unavailable_conclusion`

The source map may authorize more than one output related to a theory claim, but each individual field must have one primary evidence class.

### 2.5 Source-location rule

Every theory-relevant module header and traceability record must include:

- Theory Map ID
- source ID
- page or section
- implementation eligibility
- limits

A bare reference to the article title is insufficient for a public metric.

---

## 3. Core vocabulary map

### TM-C01. Closed recursion

| Field | Mapping |
|---|---|
| Theory Map ID | `TM-C01` |
| Primary source | TS1 |
| Source location | Pages 3-6, especially the Introduction and "Closed Recursion and the Compact Formulas" |
| Theory statement | A system enters closed recursion when future states are generated mainly from prior internal outputs while externally grounded input, heterogeneous recombination, or adversarial correction falls below the level required to preserve functional difference. |
| Mathematical object | In the minimal exact case, \(p_{t+1}=R_n(p_t)\) with no mutation, migration, independent real data, or external correction |
| v0.1 eligibility | `APPROVED_DIRECT` as a definition; `APPROVED_DERIVED` for evidence-bounded exposure measures |
| Minimum observability | Level 2 for direct provenance exposure; Level 3 for lineage-aware exposure |
| Module owner | `metrics/provenance.py`, `metrics/bounds.py`, `lineage/ancestry.py` |
| Public output | `derived_metrics.closure_exposure_bounds` and lineage-qualified variants |
| Required limits | The toolkit measures evidence of closure relative to supplied metadata. It does not observe every hidden data dependency. |
| Prohibited overclaim | "The pipeline is fully closed" when provenance or ancestry is incomplete |
| Spec dependency | `DEFINITIONS_AND_UNITS.md`, `DATA_AND_PROVENANCE_SPEC.md` |
| Test requirement | Unknown-grounding envelope, partial-provenance envelope, complete-lineage case |

**Interpretive note**

Closure is relational to the audited loop. A human-authored record can remain internal to an organizational loop. A synthetic record can introduce genuine external grounding when its source includes independent reality-bearing information. Source type alone cannot settle closure.

---

### TM-C02. External difference

| Field | Mapping |
|---|---|
| Theory Map ID | `TM-C02` |
| Primary source | TS1 |
| Source location | Pages 3, 5, 8-9, and 15-17 |
| Supporting source | TS3, pages 6-8 |
| Theory statement | Sustained correction requires states, signals, or structures that are not generated solely by the current internal distribution. |
| Mathematical object | External distribution \(r_t\) entering through mixture weight \(\lambda\) |
| v0.1 eligibility | `APPROVED_DIRECT` as a definition; `APPROVED_SIMULATION` for reopening scenarios |
| Minimum observability | Level 2 for declared grounding; Level 3 for ancestry-resolved external roots |
| Module owner | `metrics/provenance.py`, `metrics/resampling.py`, `lineage/ancestry.py` |
| Public output | grounding coverage, external-root counts, reopening simulation |
| Required limits | Difference must be both external to the loop and relevant to the represented external structure. |
| Prohibited overclaim | Treating any new record, human review flag, or model change as genuine external difference |
| Test requirement | Synthetic but grounded case, human but ungrounded case, mixed unknown case |

---

### TM-C03. Integrity

| Field | Mapping |
|---|---|
| Theory Map ID | `TM-C03` |
| Primary source | TS1 |
| Source location | Pages 5, 8-10, 15-16 |
| Supporting source | TS3, pages 6-8 |
| Theory statement | Integrity is fidelity to the external distribution, adaptive landscape, source reality, or continuing obligation that the system must track. |
| Mathematical object | In one exact model, \(L_t=\lVert p_t-q\rVert_2^2\) measures error relative to fixed external distribution \(q\) |
| v0.1 eligibility | `SUPPORTING_ONLY` as a universal concept; `APPROVED_SIMULATION` for the specific \(L_t\) model when \(q\) is supplied |
| Minimum observability | Level 1 plus a declared external reference distribution for the exact loss model |
| Module owner | `metrics/resampling.py` or future `metrics/fidelity.py` |
| Public output | scenario-specific external-reference loss only |
| Required limits | No universal integrity variable is operationalized in v0.1. |
| Prohibited overclaim | A single toolkit-wide integrity score |
| Deferred object | Universal `I` in \(Q=I\times D\) and \(S=P\times I\) |
| Test requirement | Hand-checkable distribution-distance scenario |

---

### TM-C04. Diversity

| Field | Mapping |
|---|---|
| Theory Map ID | `TM-C04` |
| Primary source | TS1 |
| Source location | Pages 5-9 |
| Supporting source | TS3, pages 5-8 |
| Theory statement | Diversity represents the surviving spread of states under a declared representation. |
| Mathematical object | Gini-Simpson index \(D=1-\sum_i p_i^2\) |
| v0.1 eligibility | `APPROVED_DERIVED` |
| Minimum observability | Level 1 |
| Module owner | `metrics/diversity.py` |
| Public output | `derived_metrics.diversity.gini_simpson` |
| Required inputs | Declared representation and empirical state frequencies |
| Required limits | Diversity values from incompatible representations cannot be compared. |
| Prohibited overclaim | Describing exact text uniqueness as semantic diversity |
| Test requirement | Uniform, concentrated, singleton, and empty-invalid cases |

---

### TM-C05. Presence

| Field | Mapping |
|---|---|
| Theory Map ID | `TM-C05` |
| Primary source | TS1 |
| Source location | Pages 5 and 8-9 |
| Supporting source | TS2, pages 5-11 |
| Theory statement | Presence is the maintained channel through which reality-bearing input can enter the recursive process. |
| Mathematical object | \(\lambda r_t\) in the reopening equation |
| v0.1 eligibility | `SUPPORTING_ONLY` as a general concept; `APPROVED_SIMULATION` through explicit \(\lambda\) scenarios |
| Minimum observability | Level 2 for declared grounding; simulation config for \(\lambda\) |
| Module owner | `metrics/resampling.py` |
| Public output | simulation assumptions and scenario comparison |
| Required limits | Large input volume does not establish useful presence when the input shares the same closed ancestry or lacks integrity. |
| Prohibited overclaim | A universal presence score |
| Test requirement | Zero, partial, and full reopening scenarios |

---

### TM-C06. Tail

| Field | Mapping |
|---|---|
| Theory Map ID | `TM-C06` |
| Primary source | TS1 |
| Source location | Pages 1-3, 7, 9-12 |
| Theory statement | Low-frequency states face greater extinction risk under finite closed resampling. |
| Mathematical object | Tail subset under declared threshold; one-step absence probability \((1-p_i)^n\) |
| v0.1 eligibility | `APPROVED_DERIVED` for rarity ranking; `APPROVED_SIMULATION` for extinction probability; `APPROVED_PROXY` for fragility warnings |
| Minimum observability | Level 1 |
| Module owner | `metrics/tail.py` |
| Public output | tail membership, rarity rank, scenario extinction probability, fragility warning |
| Required limits | Tail membership depends on representation and threshold. Extinction probability depends on the closed multinomial scenario. |
| Prohibited overclaim | Predicting actual production disappearance without matching process assumptions |
| Test requirement | Hand-checkable rare-state ranking and one-step probability |

---

### TM-C07. Correlated error

| Field | Mapping |
|---|---|
| Theory Map ID | `TM-C07` |
| Primary source | TS1 |
| Source location | Pages 2-3, 8-10, 14-17 |
| Supporting source | TS3, pages 6-9 and 10-15 |
| Theory statement | Deviations become correlated when the same narrowed internal state controls future generation, selection, validation, or source construction. |
| Mathematical object | Inherited deviations in recursive distributions; ancestry concentration as a topological witness |
| v0.1 eligibility | `APPROVED_PROXY` |
| Minimum observability | Level 3 for ancestry-based signals; Level 4 for persistent version patterns |
| Module owner | `lineage/ancestry.py`, future longitudinal module |
| Public output | `proxy_signals.correlated_error_exposure` or narrower named signals |
| Required limits | Shared ancestry indicates dependence structure. It does not establish identical semantic error without outcome evidence. |
| Prohibited overclaim | "All descendants contain the same error" based only on a shared ancestor |
| Test requirement | Shared-root graph, independent-root graph, unresolved-lineage case |

---

### TM-C08. Functional failure

| Field | Mapping |
|---|---|
| Theory Map ID | `TM-C08` |
| Primary source | TS1 |
| Source location | Pages 9, 15-17 |
| Supporting source | TS3, pages 6-8 |
| Theory statement | Distributional concentration becomes integrity decay when the system still needs breadth, adaptation, correction, or fidelity to a broader external structure. |
| Mathematical object | No universal equation in v0.1 |
| v0.1 eligibility | `SUPPORTING_ONLY` |
| Minimum observability | Domain-specific external performance evidence |
| Module owner | None in core v0.1 |
| Public output | `unavailable_conclusions.functional_failure` unless suitable external evidence is supplied under a future approved schema |
| Required limits | Convergence to a correct stable optimum can be functional. |
| Prohibited overclaim | Equating low diversity, high ancestry concentration, or support contraction with proven failure |
| Test requirement | Golden report must list functional failure as unavailable for hero data |

---

## 4. Exact mathematical core map

### TM-M01. Finite closed-resampling process

| Field | Mapping |
|---|---|
| Theory Map ID | `TM-M01` |
| Primary source | TS1 |
| Source location | Page 6 |
| Theory statement | Each generation is reconstructed from a finite sample of the current distribution with no external source. |
| Equation | \(X_t\mid p_t\sim\operatorname{Multinomial}(n,p_t)\), \(p_{t+1}=X_t/n=R_n(p_t)\) |
| v0.1 eligibility | `APPROVED_SIMULATION` |
| Module owner | `metrics/resampling.py` |
| Inputs | initial distribution, sample size \(n\), horizon, random seed |
| Outputs | simulated paths, expected summaries, extinction events |
| Evidence class | `simulation` |
| Required assumptions | finite categorical states, multinomial sampling, closed recursion |
| Prohibited overclaim | Treating the model as the literal transition law of every ML pipeline |
| Required test | Fixed-seed deterministic path and distributional sanity checks |
| Traceability target | T1, T2, T5 |

---

### TM-M02. Conditional unbiasedness

| Field | Mapping |
|---|---|
| Theory Map ID | `TM-M02` |
| Primary source | TS1 |
| Source location | Page 6 |
| Theory statement | The next generation is conditionally unbiased relative to the current generation. |
| Equation | \(\mathbb{E}[p_{t+1}\mid p_t]=p_t\) |
| v0.1 eligibility | `APPROVED_DIRECT` as mathematical documentation; optional deterministic result |
| Module owner | `metrics/resampling.py` |
| Evidence class | `derived_metric` when calculated symbolically from scenario settings |
| Interpretive limit | Unbiasedness relative to \(p_t\) does not restore fidelity to the original or external distribution. |
| Prohibited overclaim | "No drift occurs because the estimator is unbiased" |
| Required test | Monte Carlo sanity check plus exact formula test |

---

### TM-M03. Gini-Simpson diversity contraction

| Field | Mapping |
|---|---|
| Theory Map ID | `TM-M03` |
| Primary source | TS1 |
| Source location | Page 7 |
| Supporting source | TS3, page 5 |
| Theory statement | Expected diversity contracts under finite closed multinomial resampling. |
| Equation | \(\mathbb{E}[D_{t+1}\mid p_t]=(1-1/n)D_t\) |
| Iterated equation | \(\mathbb{E}[D_t]=(1-1/n)^tD_0\) |
| v0.1 eligibility | `APPROVED_DIRECT` for expected scenario calculation; `APPROVED_SIMULATION` for sampled paths |
| Module owner | `metrics/diversity.py`, `metrics/resampling.py` |
| Evidence class | formula output as `derived_metric`; stochastic path as `simulation` |
| Required assumptions | multinomial finite resampling, fixed \(n\), no reopening |
| Prohibited overclaim | Applying the contraction factor to arbitrary data-generation pipelines without model-fit evidence |
| Required test | Hand-calculated two-state and multi-state examples |
| Report target | `derived_metrics.resampling.expected_diversity` |
| Traceability target | T1 |

---

### TM-M04. Rare-state one-step extinction

| Field | Mapping |
|---|---|
| Theory Map ID | `TM-M04` |
| Primary source | TS1 |
| Source location | Page 7 |
| Theory statement | A state with frequency \(p_i\) is absent from the next finite sample with probability \((1-p_i)^n\). |
| Equation | \(\Pr(p_{t+1,i}=0\mid p_{t,i})=(1-p_{t,i})^n\) |
| v0.1 eligibility | `APPROVED_SIMULATION` |
| Module owner | `metrics/tail.py` |
| Evidence class | `simulation` |
| Required assumptions | one-step closed multinomial resampling |
| Public companion | rarity rank as `derived_metric`; fragility alert as `proxy_signal` |
| Prohibited overclaim | "This state has an X percent chance of disappearing from the real pipeline" without process equivalence |
| Required test | Exact probabilities for selected \(p_i\) and \(n\) |
| Traceability target | T2 |

---

### TM-M05. Absorbing support loss

| Field | Mapping |
|---|---|
| Theory Map ID | `TM-M05` |
| Primary source | TS1 |
| Source location | Pages 7-9 |
| Supporting source | TS3, pages 5-6 |
| Theory statement | A missing state has no internal route back under the closed resampling operator. |
| Equation | \(p_{t,i}=0 \Rightarrow p_{t+k,i}=0\) for all \(k>0\) |
| v0.1 eligibility | `APPROVED_DIRECT` inside the declared simulation model; `SUPPORTING_ONLY` for empirical pipelines |
| Module owner | `metrics/resampling.py`, `metrics/tail.py` |
| Evidence class | `simulation` or model property |
| Required limits | Mutation, migration, retrieval, fresh data, or external correction remove permanent absorption. |
| Prohibited overclaim | Calling an empirically missing topic permanently extinct when reopening channels may exist |
| Required test | Zero-frequency persistence under closed scenario and re-entry under reopened scenario |

---

### TM-M06. External-reference loss

| Field | Mapping |
|---|---|
| Theory Map ID | `TM-M06` |
| Primary source | TS1 |
| Source location | Page 8 |
| Theory statement | Finite internal resampling preserves current expectation while adding expected squared deviation relative to a fixed external distribution. |
| Definition | \(L_t=\lVert p_t-q\rVert_2^2\) |
| Equation | \(\mathbb{E}[L_{t+1}\mid p_t]=L_t+D_t/n\) |
| v0.1 eligibility | `APPROVED_SIMULATION` when \(q\) is supplied explicitly |
| Module owner | `metrics/resampling.py` |
| Evidence class | `simulation` |
| Required inputs | current distribution, external reference \(q\), sample size |
| Required limits | \(q\) must be user-supplied or derived from an approved external baseline. |
| Prohibited overclaim | Treating the earliest observed version as ground truth by default |
| Required test | Hand-checkable two-state example |

---

### TM-M07. Reopening equation

| Field | Mapping |
|---|---|
| Theory Map ID | `TM-M07` |
| Primary source | TS1 |
| Source location | Pages 8-9 |
| Supporting source | TS3, pages 6-8 |
| Theory statement | Persistent external input can restore reachability for states absent from the internal distribution. |
| Equation | \(p_{t+1}=R_n((1-\lambda)p_t+\lambda r_t)\), \(0\leq\lambda\leq1\) |
| v0.1 eligibility | `APPROVED_SIMULATION` and experimental |
| Module owner | `metrics/resampling.py` |
| Evidence class | `simulation` |
| Required inputs | \(p_t\), \(r_t\), \(\lambda\), \(n\), horizon, seed |
| Required limits | \(r_t\) must represent genuine external difference for an anti-closure interpretation. |
| Prohibited overclaim | Assuming that higher \(\lambda\) improves integrity when \(r_t\) is contaminated or shares the same ancestry |
| Required test | Closed versus reopened golden scenario |
| Traceability target | T5 |

---

## 5. Provenance and lineage map

### TM-P01. Provenance incompleteness widens uncertainty

| Field | Mapping |
|---|---|
| Theory Map ID | `TM-P01` |
| Primary source | TS1 |
| Source location | Pages 3, 8-10, 15-17 |
| Supporting source | TS2, pages 5-10 |
| Theory basis | Claims about openness and correction require evidence about where input originates and whether it remains connected to external reality. |
| Mathematical object | No direct provenance-bound formula in the theory articles |
| Product operationalization | Unknown provenance enters a lower and upper exposure envelope |
| v0.1 eligibility | `APPROVED_DERIVED` as an explicitly labeled implementation convention |
| Minimum observability | Level 2 |
| Module owner | `metrics/bounds.py`, `metrics/provenance.py` |
| Evidence class | `derived_metric` |
| Required disclosure | The closure bounds are a toolkit operationalization informed by theory, not a theorem stated in the source papers. |
| Prohibited overclaim | Presenting the bound formula as part of the Universal Inbreeding Law |
| Required test | Complete, partial, and absent provenance cases |
| Traceability target | T3 |

---

### TM-P02. Source type and grounding are distinct

| Field | Mapping |
|---|---|
| Theory Map ID | `TM-P02` |
| Primary source | TS1 |
| Source location | Pages 8-9 and 11-12 |
| Supporting source | TS2, pages 5-6 |
| Theory basis | Openness depends on genuine external information. Synthetic status alone does not determine whether a source contains independent grounding. |
| Product operationalization | Separate `source_type` from `external_grounding` |
| v0.1 eligibility | `APPROVED_DIRECT` as a specification distinction |
| Minimum observability | Level 2 |
| Module owner | `io/validation.py`, `metrics/provenance.py` |
| Evidence class | `observed_fact` for declared fields; `derived_metric` for shares |
| Prohibited overclaim | Human equals grounded; synthetic equals ungrounded |
| Required test | Crossed source-type and grounding matrix |

---

### TM-P03. External roots

| Field | Mapping |
|---|---|
| Theory Map ID | `TM-P03` |
| Primary source | TS1 |
| Source location | Pages 8-9 |
| Supporting source | TS3, pages 6-9 |
| Theory basis | External input reopens the process when its ancestry does not depend solely on the current closed lineage. |
| Product operationalization | A lineage node with confirmed external grounding that anchors a reachable ancestry path |
| v0.1 eligibility | `APPROVED_DERIVED` |
| Minimum observability | Level 3 |
| Module owner | `lineage/ancestry.py` |
| Evidence class | `derived_metric` |
| Required limits | Grounded carryovers should not be double-counted as independent roots when they preserve the same ancestry. |
| Prohibited overclaim | Counting every grounded record as a distinct independent source |
| Required test | Carryover chain, branching roots, unresolved parents |

---

### TM-P04. Ancestry concentration

| Field | Mapping |
|---|---|
| Theory Map ID | `TM-P04` |
| Primary source | TS3 |
| Source location | Pages 6-9 |
| Supporting source | TS1, pages 8-10 and 14-16 |
| Theory statement | A large apparent population can remain dependent on a narrow ancestor set, causing shared internal bias and reduced adaptive range. |
| Mathematical object | Ancestor incidence; fractional-root allocation; HHI over external-root mass |
| v0.1 eligibility | `APPROVED_DERIVED` for topology; `APPROVED_PROXY` for correlated-error exposure |
| Minimum observability | Level 3 |
| Module owner | `lineage/ancestry.py` |
| Evidence class | concentration as `derived_metric`; risk interpretation as `proxy_signal` |
| Required limits | Topological concentration does not measure semantic error or causal contribution without edge weights and outcome evidence. |
| Prohibited overclaim | "This ancestor caused the observed failure" |
| Required test | Single root, equal roots, uneven roots, multiple-root descendants |
| Traceability target | T4 |

---

### TM-P05. Cycle invalidity

| Field | Mapping |
|---|---|
| Theory Map ID | `TM-P05` |
| Primary source | Product engineering rule |
| Theory support | TS1 and TS3 assume generational or cross-cycle direction, but neither article presents a general graph-cycle theorem for provenance manifests |
| Product operationalization | Parent-child lineage used for generational ancestry must be acyclic |
| v0.1 eligibility | `APPROVED_DIRECT` as an implementation-integrity rule |
| Minimum observability | Level 3 |
| Module owner | `lineage/cycles.py` |
| Evidence class | `observed_fact` or `error` |
| Required disclosure | This is a graph-validity requirement derived from the chosen lineage representation. It is not a standalone theorem of the Universal Inbreeding Law. |
| Prohibited overclaim | Treating any real-world feedback loop as invalid merely because the manifest representation requires a DAG |
| Required test | Self-cycle, two-node cycle, longer cycle, acyclic graph |
| Traceability target | T6, with source class changed from theory claim to implementation rule |

---

## 6. Entropy and causal-language map

### TM-E01. Entropy as structural boundary

| Field | Mapping |
|---|---|
| Theory Map ID | `TM-E01` |
| Primary source | TS2 |
| Source location | Pages 1-4 and 7-11 |
| Theory statement | Entropy describes the structural direction, dispersion, uncertainty, or boundary of sustainable order under stated constraints. |
| v0.1 eligibility | `SUPPORTING_ONLY` |
| Module owner | Reporting and documentation layers |
| Public effect | Controls explanation language and unavailable conclusions |
| Required language | Name the observed mechanism before invoking entropy language |
| Prohibited overclaim | "Entropy caused the dataset to collapse" |
| Required test | Golden report language review |

---

### TM-E02. Local mechanism remains necessary

| Field | Mapping |
|---|---|
| Theory Map ID | `TM-E02` |
| Primary source | TS2 |
| Source location | Pages 7-10 |
| Theory statement | Entropy accounting does not replace identification of the local process that produced the change. |
| v0.1 eligibility | `SUPPORTING_ONLY` |
| Module owner | Report renderer |
| Public effect | Reports must name finite resampling, source concentration, missing grounding, lineage concentration, or observed support loss |
| Prohibited overclaim | Explaining every warning through entropy alone |
| Required test | Report contains mechanism and assumption fields |

---

### TM-E03. Emergent direction does not imply an entropic force

| Field | Mapping |
|---|---|
| Theory Map ID | `TM-E03` |
| Primary source | TS2 |
| Source location | Pages 3-4 and 7-9 |
| Theory statement | Directional macroscopic behavior can emerge from reversible or locally ordinary dynamics without introducing entropy as an additional agent. |
| v0.1 eligibility | `SUPPORTING_ONLY` |
| Module owner | Theory documentation |
| Public effect | Supports stochastic contraction explanations without mystical causal language |
| Prohibited overclaim | "The metric exerts pressure on the system" |

---

### TM-E04. Cross-domain restraint

| Field | Mapping |
|---|---|
| Theory Map ID | `TM-E04` |
| Primary source | TS2 |
| Source location | Pages 4 and 6-11 |
| Supporting source | TS1, pages 4, 9, 14-16 |
| Theory statement | Similar structural boundaries across domains do not establish identical thermodynamic or microphysical laws. |
| v0.1 eligibility | `SUPPORTING_ONLY` |
| Module owner | Documentation and report renderer |
| Public effect | The ML toolkit must remain within data-pipeline claims |
| Prohibited overclaim | Converting an ML audit into a biological, psychological, social, or civilizational diagnosis |

---

### TM-E05. No universal entropy score

| Field | Mapping |
|---|---|
| Theory Map ID | `TM-E05` |
| Primary source | TS2 |
| Source location | Pages 1-11 |
| Theory basis | Different entropy concepts quantify different distributions and physical or informational objects. |
| v0.1 eligibility | `FORBIDDEN` |
| Module owner | None |
| Public output | `unavailable_conclusions.universal_entropy_score` when relevant |
| Prohibited implementation | Single cross-domain entropy or collapse score |

---

## 7. Structural formulas and deferred constructs

### TM-S01. Quality relation

| Field | Mapping |
|---|---|
| Theory Map ID | `TM-S01` |
| Primary source | TS1 |
| Source location | Page 5 |
| Formula | \(Q=I\times D\) |
| Theory role | Compact structural dependency |
| v0.1 eligibility | `DEFERRED` |
| Reason | Universal integrity and quality variables lack approved units, scales, and measurement procedures |
| Permitted use | Documentation of theory architecture |
| Prohibited use | Numerical quality score, threshold, or ranking |
| Future requirement | Domain-specific operational definition, calibration, and validation |

---

### TM-S02. Stability relation

| Field | Mapping |
|---|---|
| Theory Map ID | `TM-S02` |
| Primary source | TS1 |
| Source location | Page 5 |
| Formula | \(S=P\times I\) |
| Theory role | Compact structural dependency |
| v0.1 eligibility | `DEFERRED` |
| Reason | Presence and integrity lack universal operational units |
| Permitted use | Documentation and conceptual explanation of reopening |
| Prohibited use | Stability score or universal failure threshold |
| Future requirement | Domain-specific definitions and validated measurement model |

---

### TM-S03. Collapse sequence

| Field | Mapping |
|---|---|
| Theory Map ID | `TM-S03` |
| Primary source | TS1 |
| Source location | Pages 9-10 |
| Sequence | closure rises -> external difference falls -> diversity contracts -> errors become correlated -> integrity weakens -> collapse or functional dead zones emerge |
| v0.1 eligibility | `SUPPORTING_ONLY` as a report architecture |
| Public use | Organize diagnostics by stage without claiming every later stage is observed |
| Required behavior | Stop the chain at the strongest evidenced stage and place later stages under unavailable conclusions |
| Prohibited overclaim | Filling missing stages through assumption |
| Test requirement | Hero report stops before proven functional failure |

---

## 8. Genetic-algorithm witness map

### TM-GA01. Selection concentration

| Field | Mapping |
|---|---|
| Theory Map ID | `TM-GA01` |
| Primary source | TS3 |
| Source location | Pages 3-5 |
| Theory statement | Selection increases the reproductive share of current winners and can accelerate lineage takeover. |
| Mathematical object | Tournament selection probability \(p_t^{sel}=1-(1-p_t)^s\) |
| v0.1 eligibility | `SUPPORTING_ONLY` for core product; eligible for later validation fixture |
| Future module | `examples/genetic_algorithm` or experimental simulation |
| Prohibited transfer | Applying tournament-selection equations to ordinary dataset pipelines without an equivalent operator |

---

### TM-GA02. Finite-population diversity contraction

| Field | Mapping |
|---|---|
| Theory Map ID | `TM-GA02` |
| Primary source | TS3 |
| Source location | Page 5 |
| Theory statement | Finite reproduction adds expected diversity contraction even after the algorithmic operators have formed a post-selection distribution. |
| Equation | \(\mathbb{E}[D(x_{t+1})\mid x_t]=(1-1/N)D(y_t)\) |
| v0.1 eligibility | `SUPPORTING_ONLY` as independent witness for TM-M03 |
| Public effect | Strengthens mathematical validation and future example design |

---

### TM-GA03. Absorbing homogeneity

| Field | Mapping |
|---|---|
| Theory Map ID | `TM-GA03` |
| Primary source | TS3 |
| Source location | Pages 5-6 |
| Theory statement | Without mutation, immigration, or another novelty operator, a homogeneous population remains homogeneous. |
| Equation | \(\Pr(x_{t+1}=e_j\mid x_t=e_j)=1\) |
| v0.1 eligibility | `SUPPORTING_ONLY` for core product; `APPROVED_SIMULATION` in a future GA fixture |
| Interpretive value | Demonstrates that recombination cannot recreate building blocks already lost |

---

### TM-GA04. Reopening operators

| Field | Mapping |
|---|---|
| Theory Map ID | `TM-GA04` |
| Primary source | TS3 |
| Source location | Pages 6-9 |
| Theory statement | Mutation restores reachability, immigration introduces ancestry outside the elite lineage, dissimilar mating preserves usable difference, and restart performs strong reopening. |
| v0.1 eligibility | `SUPPORTING_ONLY` |
| Public effect | Informs intervention taxonomy and future scenario design |
| Required distinction | Reachability, retention, recombination, and external ancestry are separate functions |
| Prohibited overclaim | Treating all novelty operators as equivalent |

---

### TM-GA05. Convergence versus premature convergence

| Field | Mapping |
|---|---|
| Theory Map ID | `TM-GA05` |
| Primary source | TS3 |
| Source location | Pages 6-8 |
| Theory statement | Concentration becomes failure when it occurs before the relevant landscape is adequately resolved or when the environment changes beyond the occupied basin. |
| v0.1 eligibility | `SUPPORTING_ONLY` |
| Public effect | Reinforces TM-C08 |
| Prohibited overclaim | Low diversity automatically means failure |

---

## 9. Amplification-dominant branch map

### TM-A01. Amplification branch classification

| Field | Mapping |
|---|---|
| Theory Map ID | `TM-A01` |
| Primary source | TS3 |
| Source location | Pages 10-15 |
| Theory statement | Closed recursive failure can amplify a retained defect even when diversity contraction is not the first or primary stage. |
| v0.1 eligibility | `DEFERRED` |
| Reason | Core v0.1 metrics are contraction-focused and lack an amplification input schema |
| Future module | `recursive_amplification` |
| Prohibited overclaim | Treating every amplification case as a complete contraction-dominant realization |

---

### TM-A02. Cross-cycle transfer threshold

| Field | Mapping |
|---|---|
| Theory Map ID | `TM-A02` |
| Primary source | TS3 |
| Source location | Pages 12-14 |
| Mathematical object | \(z_{t+1}=Kz_t+\epsilon_t\) |
| Threshold | \(\rho(K)<1\) implies decay; \(\rho(K)>1\) permits amplification along a dominant mode |
| v0.1 eligibility | `DEFERRED` |
| Future evidence class | `simulation` or domain-native derived metric |
| Future requirements | Valid transfer matrix, unit definitions, observation model, domain-specific validation |
| Prohibited overclaim | Reusing \(\rho(K)\) as a generic collapse score |

---

### TM-A03. Delayed visibility

| Field | Mapping |
|---|---|
| Theory Map ID | `TM-A03` |
| Primary source | TS3 |
| Source location | Pages 12-14 |
| Theory statement | The state of a recursive amplification loop and the visible failure curve can evolve on different timescales. |
| v0.1 eligibility | `SUPPORTING_ONLY` |
| Public effect | Supports cautious interpretation of surface stability |
| Prohibited overclaim | Inferring hidden amplification merely because visible metrics lag |

---

### TM-A04. Boundary interruption

| Field | Mapping |
|---|---|
| Theory Map ID | `TM-A04` |
| Primary source | TS3 |
| Source location | Page 14 |
| Theory statement | Source separation, path removal, traceability, and exclusion controls reduce or sever recursive return routes. |
| v0.1 eligibility | `SUPPORTING_ONLY` |
| Future role | Intervention taxonomy for amplification systems |
| Prohibited transfer | Claiming that provenance documentation alone changes the underlying feedback matrix |

---

## 10. Existing design Trace ID reconciliation

The migration package contains Trace IDs T1-T6. They should be reconciled with this map as follows.

| Existing Trace ID | Existing claim | Primary Theory Map IDs | Audit result |
|---|---|---|---|
| T1 | Closed recursive reuse contracts effective support | `TM-M01`, `TM-M03`, `TM-M05` | Approved with explicit finite-resampling assumptions |
| T2 | Low-frequency states disappear first under closure | `TM-C06`, `TM-M04` | Approved; extinction probability must appear as simulation |
| T3 | Missing provenance widens uncertainty | `TM-P01`, `TM-C01` | Approved as toolkit operationalization, not a direct theorem |
| T4 | Shared ancestry matters more than apparent record count | `TM-P04`, `TM-C07` | Approved as topological metric plus proxy interpretation |
| T5 | External inputs reopen closed support | `TM-M07`, `TM-C02`, `TM-C05` | Approved as experimental simulation |
| T6 | Cycles invalidate naive lineage interpretation | `TM-P05` | Reclassified as graph-validity engineering rule |

No additional public Trace ID should be created until it is first entered in this map.

---

## 11. Initial public field map

This section gives the intended source basis for the first public result fields. Exact field names remain controlled by the reporting specification.

| Public result concept | Theory Map IDs | Evidence class | Minimum level | Status |
|---|---|---|---|---|
| Record count | Product metadata | `observed_fact` | 0 | Approved |
| Exact duplicate count | Product metadata | `observed_fact` | 1 | Approved |
| Representation support size | `TM-C04` | `derived_metric` | 1 | Approved |
| Gini-Simpson diversity | `TM-C04`, `TM-M03` | `derived_metric` | 1 | Approved |
| Tail membership | `TM-C06` | `derived_metric` | 1 | Approved |
| Rare-state ranking | `TM-C06` | `derived_metric` | 1 | Approved |
| One-step extinction scenario | `TM-M04` | `simulation` | 1 | Approved |
| Tail fragility warning | `TM-C06`, `TM-M04` | `proxy_signal` | 1 | Approved |
| Provenance row coverage | `TM-P01` | `observed_fact` | 2 | Approved |
| Grounding field coverage | `TM-P01`, `TM-P02` | `observed_fact` | 2 | Approved |
| Source-type shares | `TM-P02` | `derived_metric` | 2 | Approved |
| Direct closure exposure bounds | `TM-C01`, `TM-P01` | `derived_metric` | 2 | Approved after spec freeze |
| Cycle status | `TM-P05` | `observed_fact` or error | 3 | Approved |
| External-root count | `TM-P03` | `derived_metric` | 3 | Approved |
| Top shared ancestors | `TM-P04` | `derived_metric` | 3 | Approved |
| Ancestry HHI | `TM-P04` | `derived_metric` | 3 | Approved after spec freeze |
| Correlated-error exposure | `TM-C07`, `TM-P04` | `proxy_signal` | 3 | Narrow naming required |
| Version support loss | `TM-C04`, `TM-C06`, `TM-M05` | `derived_metric` | 4 | Approved |
| Tail extinction list | `TM-C06`, `TM-M05` | `derived_metric` | 4 | Approved |
| External reopening scenario | `TM-M07` | `simulation` | 5 or experimental | Approved experimental |
| Universal integrity | `TM-C03`, `TM-S01` | `unavailable_conclusion` | Any | Deferred |
| Proven functional failure | `TM-C08` | `unavailable_conclusion` | Any without outcome evidence | Deferred |
| Universal collapse prediction | `TM-S03` | `unavailable_conclusion` | Any | Forbidden |
| Universal entropy score | `TM-E05` | `unavailable_conclusion` | Any | Forbidden |
| Amplification threshold | `TM-A02` | `unavailable_conclusion` | v0.1 | Deferred |

---

## 12. Required test-source map

### Mathematical tests

| Test family | Theory Map IDs | Expected basis |
|---|---|---|
| Finite-resampling expectation | `TM-M01`, `TM-M02` | Exact formula |
| Diversity contraction | `TM-M03` | Hand calculation |
| Rare-state extinction | `TM-M04` | Closed-form probability |
| Absorbing support | `TM-M05` | Exact process property |
| External-reference loss | `TM-M06` | Hand calculation |
| Reopening | `TM-M07` | Fixed-seed scenario and exact reachability logic |

### Provenance and lineage tests

| Test family | Theory Map IDs | Expected basis |
|---|---|---|
| Unknown provenance envelope | `TM-P01` | Approved toolkit convention |
| Grounding versus source type | `TM-P02` | Specification matrix |
| External-root tracing | `TM-P03` | Graph traversal |
| Ancestry concentration | `TM-P04` | Hand-checkable graph |
| Cycle rejection | `TM-P05` | Graph-validity rule |

### Reporting tests

| Test family | Theory Map IDs | Expected basis |
|---|---|---|
| Mechanism named before entropy language | `TM-E01`, `TM-E02` | Golden language review |
| Cross-domain restraint | `TM-E04` | Golden report review |
| Functional failure unavailable | `TM-C08` | Hero golden report |
| Simulation clearly labeled | `TM-M04`, `TM-M06`, `TM-M07` | JSON and Markdown schema |
| Compact formulas excluded from scoring | `TM-S01`, `TM-S02` | Schema absence and negative test |

---

## 13. Report-language rules derived from theory

### 13.1 Permitted language

The following formulations are consistent with the theory map:

- "The supplied metadata shows partial recursive closure exposure."
- "Topic support contracted between the two supplied dataset versions."
- "Low-frequency topic states have higher one-step extinction probability under the declared closed-resampling scenario."
- "Three records share the same external root, creating concentrated ancestry."
- "The available evidence does not establish production failure."
- "Unknown provenance widens the closure exposure interval."
- "External reopening restores reachability in the stated simulation."
- "Surface continuity can coexist with support loss."

### 13.2 Restricted language

The following formulations require stronger evidence or clearer assumptions:

- "The dataset is collapsing."
- "The system has lost integrity."
- "The model will fail after a fixed number of generations."
- "Human data prevents collapse."
- "Synthetic data causes collapse."
- "Entropy is destroying the pipeline."
- "The top ancestor caused the downstream error."
- "A high observability level proves complete auditability."
- "An external source is independent because it has a different filename or generator ID."

### 13.3 Required qualifiers

Every scenario output must identify:

- representation,
- sample size,
- horizon,
- random seed,
- closure assumption,
- external input assumption,
- baseline distribution,
- evidence class.

Every lineage output must identify:

- loaded graph scope,
- resolved-parent coverage,
- grounding coverage,
- unresolved parent count,
- cycle status,
- ancestor allocation convention.

Every longitudinal output must identify:

- version ordering rule,
- representation compatibility,
- missing-version fields,
- whether the comparison concerns data, model performance, or both.

---

## 14. Deferred research queue

The following theory objects are intentionally preserved for later versions.

### D01. Universal operational integrity

Required before implementation:

- domain-specific external reference,
- unit and scale,
- measurement error model,
- calibration procedure,
- evidence that the score tracks meaningful external fidelity.

### D02. Presence measurement

Required before implementation:

- distinction between volume and independent information,
- ancestry-aware source novelty,
- source reliability,
- temporal continuity,
- external relevance.

### D03. Effective source diversity

Required before implementation:

- source identity model,
- source dependence rules,
- treatment of shared generators,
- treatment of copied and transformed records,
- weighting convention.

### D04. Semantic tail analysis

Required before a default implementation:

- approved embedding or representation model,
- versioned clustering method,
- stability checks,
- threshold policy,
- privacy and dependency review.

### D05. Amplification branch

Required before implementation:

- transfer-matrix schema,
- state units,
- time-step definition,
- threshold interpretation,
- domain-native validation,
- separation from contraction metrics.

### D06. Controlled empirical interventions

Required before implementation:

- treatment and control schema,
- assignment or identification assumptions,
- outcome definitions,
- causal limitations,
- reporting contract.

### D07. Hidden-decay indicators

Required before implementation:

- operational definition,
- observable proxy set,
- calibration evidence,
- false-positive analysis,
- separation from ordinary version drift.

---

## 15. Theory coverage matrix

| Theory area | Directly implemented in v0.1 | Used for interpretation | Deferred |
|---|---:|---:|---:|
| Closed finite resampling | Yes | Yes | No |
| Gini-Simpson diversity contraction | Yes | Yes | No |
| Rare-state extinction | Scenario | Yes | No |
| Absorbing support under closure | Scenario | Yes | No |
| External reopening | Experimental scenario | Yes | No |
| External-reference loss | Optional scenario | Yes | No |
| Provenance uncertainty | Operational bounds | Yes | No |
| External-root ancestry | Yes | Yes | No |
| Ancestry concentration | Yes | Yes | No |
| Correlated semantic error | No | Proxy only | Yes |
| Universal integrity | No | Yes | Yes |
| Universal presence | No | Yes | Yes |
| Universal quality or stability | No | Yes | Yes |
| Entropy as causal force | No | Prohibited framing | No |
| Thermodynamic identity across domains | No | Prohibited framing | No |
| Genetic-algorithm selection dynamics | No | Validation witness | Yes |
| Recursive amplification threshold | No | Taxonomy only | Yes |
| Social or institutional audit | No | Theory context only | Yes |

---

## 16. Approval gate

This map is approved when the Theory Owner confirms all of the following:

- [ ] TS1 is the primary mathematical authority for v0.1.
- [ ] TS2 controls entropy and causal language.
- [ ] TS3 supplies supporting witnesses and the contraction/amplification taxonomy.
- [ ] Compact formulas \(Q=I\times D\) and \(S=P\times I\) remain non-operational in v0.1.
- [ ] Tail extinction probability is reported as a scenario result.
- [ ] Closure exposure bounds are identified as a toolkit operationalization.
- [ ] Ancestry concentration is topological unless causal edge weights exist.
- [ ] Cycle rejection is classified as a graph-validity rule.
- [ ] Functional failure remains unavailable without domain outcome evidence.
- [ ] Amplification-dominant analysis remains deferred.
- [ ] Cross-domain interpretation does not become cross-domain software output.
- [ ] No public field exists without a Theory Map ID or a clearly identified product-only basis.

### Theory Owner decision

- [ ] Approve
- [ ] Approve with exceptions
- [ ] Return for revision

Exceptions or modifications:

```text

```

Theory Owner:

```text
Xiangyu Guo
```

Approval date:

```text

```

Approved baseline status:

```text
PENDING
```

---

## 17. Change-control rule

After approval:

1. every new theory-relevant public metric must receive a new `TM-*` entry,
2. every changed interpretation must cite the source location that authorizes the change,
3. every deferred claim promoted into implementation must gain units, observability requirements, tests, and report fields,
4. no source-map entry may be deleted silently,
5. superseded entries remain in version history with the reason for replacement,
6. product-only engineering rules must remain visibly distinct from source-derived theory claims.

This file should be reviewed again before each official release and whenever the authoritative theory corpus changes.
