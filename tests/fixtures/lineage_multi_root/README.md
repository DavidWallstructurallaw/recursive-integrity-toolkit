# Multi-root and independent uncertainty inputs

These three Phase 5 Step 1 cases each load seven records and select four targets.
Targets t1 and t2 have complete roots {a} and {a,b}; t3 is known-empty; t4 remains
unresolved. Context records a, b and u never enlarge the target denominator.

The mixed case gives t4 both an unknown-grounding ancestor and a missing parent.
The two variants isolate each failure: remove the missing reference while keeping
u unknown, or ground u while retaining the missing reference. Either defect alone
keeps t4 out of exact root allocation. Grounding u in the latter variant does not
make u a contributing root while its only target remains unresolved.

Hand arithmetic: incidence is (2,1), with target shares (1/2,1/4). Fractional mass
is (3/2,1/2); normalization by two externally rooted targets yields (3/4,1/4).
Thus HHI is 9/16 + 1/16 = 5/8 and effective roots are 8/5. Resolved coverage is
3/4, external ancestry coverage is 1/2, and closure bounds are [1/4,1/2]. Width
is 1/4. Reference coverage is 5/6 with a missing reference and 1 in the
unknown-only variant. Perfect reference coverage alone does not resolve unknown
grounding.

`cases.json` is future acceptance data. Step 1 executes only its input-validation
expectations. Shared format and execution limits are documented in
`../lineage_complete/README.md`.
