# External reopening contract fixtures

Phase 6B Step 1 records exact, independently authored expectations for T5 and
F-017. All cases are synthetic experimental simulation scenarios. No fixture
value was produced by a toolkit reopening implementation or a random seed.

`cases.json` uses rational strings so its probabilities and expectations can be
checked exactly with `Fraction`. `state_order` is the common declared state
space, including zero-mass states. The initial distribution, external
distribution, reopening weight and resample size are always explicit. The
external distribution and weight are constant across steps in these fixtures.

The one-step cases cover both weight endpoints, partial reopening, a state
absent from both sources, identical sources, and a concentrated external source
that reduces diversity. The single-state case remains degenerate; the `n=1`
case allows re-entry while every sample has zero diversity. The partial case
has source `(3/4, 1/4)` and `n=2`:
the outcomes `(2,0)`, `(1,1)` and `(0,2)` have probabilities `9/16`, `6/16`
and `1/16`; re-entry probability for the absent second state is `7/16`.
Positive reachability therefore does not guarantee realized re-entry.

The prescribed path is a possible sequence of counts, not a sampled realization
or a seeded golden output. It records a state's repeated disappearance and
re-entry. A re-entry event requires an internally absent state, positive mixed
source probability and positive subsequent count. Equal support size can hide
a change in state identity. The zero-horizon case retains only the initial
distribution, with no initial counts, transitions or events.

The two-step endpoint case distinguishes fully external sampling from a closed
process initialized at the external distribution. At weight one, every source
is reset to the external distribution. After first drawing `(2,0)` from
`(1/2,1/2)`, its second-step re-entry probability is `3/4`; the corresponding
closed conditional probability is zero. No closed multi-step expectation is
assigned to the reopened process. The second-source and re-entry fields are
conditioned on the specified `first_counts`. The diversity arrays are
unconditional expectations over all paths from the initial distribution;
they do not describe only that conditioned branch. Both bases are recorded
explicitly in the fixture metadata.

`tests/unit/test_reopening_fixture_inputs.py` checks rational mixtures, complete
small multinomial outcome tables, conditional expectations and the authored
event definitions. It also checks the accepted closed analytic kernel against
a literal closed expectation. The test module uses pytest; all oracle
calculations use Python's standard-library rational arithmetic.

These tests certify fixture consistency only. They do not certify a future
reopening sampler, fixed-seed replay, input rejection, resource bounds,
orchestration, scenario comparison API, report schema, CLI behavior or empirical
causality. Those behaviors remain assigned to later Phase 6B steps. There is no
external truth reference, fidelity score, integrity score or inferred causal
effect in these fixtures.
