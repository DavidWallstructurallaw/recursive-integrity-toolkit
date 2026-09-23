# Complete and boundary lineage acceptance inputs

Phase 5 Step 1 specifies synthetic inputs and independent future acceptance
values. `cases.json` contains canonical record/provenance rows, explicit version
order, selected target keys, current input-validation expectations, and future
lineage expectations. These files are test data, not report-schema documents.

The cases separate root support from strict ancestry, preserve known-empty root
sets, distinguish unknown grounding from absent/null parent declarations, and
cover single-parent carryover, duplicate aliases, diamond paths, and conservative
grounded-parent handling. The empty-target case selects no observations from a
loaded context; it concerns the future analysis API and makes no claim about
current empty-file CLI support.

`hero_expected.json` transcribes the approved Hero arithmetic into exact rational
values for later lineage tests. The six canonical files in `examples/hero` remain
unchanged. The three roots with incidence one are ordered by canonical key.

Conventions shared by these three lineage fixture directories:

- Rational strings are exact values. `lineage_bounds` lists lower, upper, width.
- `complete_root_sets` omits unresolved targets. An empty array is a completely
  resolved known-empty set. Roots on incomplete paths contribute no exact mass.
- Counts distinguish selected targets from loaded supporting records.
- Conceptual unresolved reasons are explanatory fixture values; later runtime
  tests map them to the approved typed reason codes.
- `shared_ancestry_proxy` uses existing report levels: `present`, `not_present`,
  or `indeterminate`. The last includes unavailable empty-target results.
- The Step 1 loader test validates only `expected_input`. It uses the existing
  comparison input role to load supporting records until the dedicated context
  role is implemented. It executes no graph or lineage formula.
- `expected_lineage` becomes a product oracle when Steps 2 through 8 implement
  the corresponding behavior. Its presence is not a passing lineage result.

Arithmetic was derived from the approved P5-D01 through P5-D07 contracts before
graph implementation. No output from the future implementation generated these
expected values. General permutation, renaming, long-chain and resource-boundary
cases belong in the later direct tests instead of expanded static fixture copies.
