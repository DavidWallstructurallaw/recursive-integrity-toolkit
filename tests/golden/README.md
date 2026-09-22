# Golden output placeholder

Phase 1 creates the approved directory only.
No analytical JSON, Markdown, or HTML report is generated or compared in this step.

## Phase 4 Step 9 independent report goldens

`phase4_report_cases.md` records authored reasoning, traceability and limitations.
`phase4_report_expected.json` freezes executable independent assertions before
production output is observed. Every declared case is parametrized by
`test_phase4_reports.py`; the twenty Phase 3 mathematical cases remain unchanged.
The four `phase4_hero_report.*` / `phase4_hero_redacted.*` files contain reviewed
literal JSON and Markdown. Both formats must agree with their accepted fixtures.

Candidate generation is explicit and writes only to a new scratch directory:

```sh
python scripts/build_golden.py --scratch-out /absolute/new/scratch-directory
```

The generator injects fixed test metadata and a public test-only identifier key.
It records the independent oracle hashes, raw observations, declared configuration
and candidate hashes. It never updates accepted fixtures. Accepting candidates
requires checking every report field and the human-readable Markdown against the
independent rationale, followed by the Step 9 controlled fixture digest update.
No expected analytical value may be accepted solely from observed output.

`normalize_golden.py` changes only the six explicit run metadata fields and each
verified input-inventory test-root prefix. It verifies original input bytes and
configuration hashes. The configuration hash is recomputed from an independent
resolved declaration after changing only declared input/output root prefixes.
Metrics, scopes, evidence classes, reason codes, warnings, availability,
configuration meaning and unavailable conclusions retain their exact values.
Markdown normalization edits the corresponding exact rows and run-ID summary;
it never renders fresh Markdown from JSON. Missing or duplicate rows fail closed.

The public key makes golden identity stable for tests. Production fresh-key
unlinkability is tested independently and is not claimed from deterministic
fixtures. Hashes identify supplied bytes and declared meaning, not authenticity.
