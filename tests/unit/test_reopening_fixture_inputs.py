"""Check authored Phase 6B oracles without implementing a reopening simulator.

Fraction arithmetic and finite one-step PMFs validate literal fixture values.
The only production call is the already accepted closed analytic expectation.
No random paths, input rejection or future report/CLI behavior are certified.
"""

from fractions import Fraction
from itertools import product
import json
from math import factorial
from pathlib import Path

import pytest


FIXTURE = Path(__file__).resolve().parents[1] / 'fixtures' / 'reopening' / 'cases.json'
DOCUMENT = json.loads(FIXTURE.read_text(encoding='utf-8'))
CASES = DOCUMENT['one_step_cases']


def _fractions(values):
    return tuple(Fraction(value) for value in values)


def _diversity(probabilities):
    return 1 - sum((value * value for value in probabilities), Fraction())


def _enumerate_multinomial(probabilities, n):
    """Finite exact PMF, independent of sequential-binomial toolkit sampling."""
    outcomes = {}
    for counts in product(range(n + 1), repeat=len(probabilities)):
        if sum(counts) != n:
            continue
        probability = Fraction(factorial(n))
        for count, mass in zip(counts, probabilities, strict=True):
            probability *= mass ** count / factorial(count)
        if probability:
            outcomes[counts] = probability
    return outcomes


@pytest.mark.parametrize('case', CASES, ids=lambda case: case['case_id'])
def test_authored_distributions_and_mixtures_are_exact(case):
    assert not DOCUMENT['expectations_generated_by_implementation']
    assert DOCUMENT['status'] == 'experimental'
    assert DOCUMENT['evidence_class'] == 'simulation'
    states = case['state_order']
    internal = _fractions(case['internal'])
    external = _fractions(case['external'])
    mixed = _fractions(case['expected_mixed'])
    weight = Fraction(case['reopening_weight'])
    assert states == sorted(set(states))
    assert 0 <= weight <= 1
    for values in (internal, external, mixed):
        assert len(values) == len(states)
        assert sum(values) == 1
        assert all(value >= 0 for value in values)
    assert mixed == tuple((1 - weight) * p + weight * r
                          for p, r in zip(internal, external, strict=True))
    assert _diversity(mixed) == Fraction(case['expected_mixed_diversity'])


@pytest.mark.parametrize('case', CASES, ids=lambda case: case['case_id'])
def test_literal_multinomial_tables_and_expected_diversity(case):
    n = case['resample_size']
    mixed = _fractions(case['expected_mixed'])
    outcomes = _enumerate_multinomial(mixed, n)
    literal = {tuple(row['counts']): Fraction(row['probability'])
               for row in case['expected_positive_outcomes']}
    assert len(literal) == len(case['expected_positive_outcomes'])
    assert outcomes == literal
    assert sum(outcomes.values()) == 1
    expected = sum((chance * _diversity(tuple(Fraction(c, n) for c in counts))
                    for counts, chance in outcomes.items()), Fraction())
    assert expected == Fraction(case['expected_sample_diversity'])
    assert expected == (1 - Fraction(1, n)) * _diversity(mixed)


@pytest.mark.parametrize('case', CASES, ids=lambda case: case['case_id'])
def test_reachability_and_reentry_probability_are_distinct(case):
    states = case['state_order']
    internal = _fractions(case['internal'])
    mixed = _fractions(case['expected_mixed'])
    outcomes = _enumerate_multinomial(mixed, case['resample_size'])
    reachable = [state for state, p, s in zip(states, internal, mixed, strict=True)
                 if p == 0 and s > 0]
    assert reachable == case['expected_reachable_absent_states']
    probabilities = {
        state: sum((chance for counts, chance in outcomes.items() if counts[i] > 0),
                   Fraction())
        for i, (state, p) in enumerate(zip(states, internal, strict=True)) if p == 0
    }
    assert probabilities == {
        state: Fraction(value)
        for state, value in case['expected_reentry_probability_by_absent_state'].items()
    }
    for i, state in enumerate(states):
        if internal[i] == 0:
            assert probabilities[state] == 1 - (1 - mixed[i]) ** case['resample_size']
    if case['case_id'] == 'partial_reopening_possible_not_guaranteed':
        assert 0 < probabilities['b'] < 1


def test_identical_and_concentrated_external_sources_do_not_imply_diversity_gain():
    identical = next(case for case in CASES
                     if case['case_id'] == 'identical_sources_no_strict_diversity_gain')
    assert _fractions(identical['internal']) == _fractions(identical['expected_mixed'])
    concentrated = next(case for case in CASES
                        if case['case_id'] == 'concentrated_external_source_reduces_diversity')
    assert (Fraction(concentrated['expected_mixed_diversity'])
            < _diversity(_fractions(concentrated['internal'])))


def test_prescribed_path_has_positive_probability_and_exact_reentry_events():
    case = DOCUMENT['prescribed_event_path']
    states = case['state_order']
    n = case['resample_size']
    external = _fractions(case['external'])
    weight = Fraction(case['reopening_weight'])
    previous = _fractions(case['initial'])
    reentries, disappearances = [], []
    support = [[state for state, p in zip(states, previous, strict=True) if p > 0]]
    diversities = [_diversity(previous)]
    path_probability = Fraction(1)
    for step, row in enumerate(case['transitions'], start=1):
        assert row['step'] == step
        assert _fractions(row['internal']) == previous
        mixed = _fractions(row['mixed'])
        assert mixed == tuple((1 - weight) * p + weight * r
                              for p, r in zip(previous, external, strict=True))
        counts = tuple(row['counts'])
        chance = _enumerate_multinomial(mixed, n)[counts]
        assert chance == Fraction(row['probability'])
        path_probability *= chance
        for state, before, source, count in zip(
            states, previous, mixed, counts, strict=True
        ):
            if before == 0 and source > 0 and count > 0:
                reentries.append({'step': step, 'state_id': state})
            if before > 0 and count == 0:
                disappearances.append({'step': step, 'state_id': state})
        previous = tuple(Fraction(count, n) for count in counts)
        support.append([state for state, count in zip(states, counts, strict=True)
                        if count > 0])
        diversities.append(_diversity(previous))
    assert path_probability == Fraction(case['expected_path_probability'])
    assert path_probability > 0
    assert reentries == case['expected_reentry_events']
    assert disappearances == case['expected_disappearance_events']
    assert support == case['expected_support']
    assert [len(states) for states in support] == case['expected_support_sizes']
    assert tuple(diversities) == _fractions(case['expected_diversity'])
    assert [event['step'] for event in reentries if event['state_id'] == 'b'] == [1, 3]
    assert len(support[2]) == len(support[3])
    assert support[2] != support[3]


def test_zero_horizon_literal_has_only_the_initial_state():
    case = DOCUMENT['zero_horizon']
    initial = _fractions(case['initial'])
    assert case['horizon'] == 0
    assert case['expected_initial_counts'] is None
    assert tuple(map(_fractions, case['expected_distributions'])) == (initial,)
    assert case['expected_support'] == [[
        state for state, p in zip(case['state_order'], initial, strict=True) if p > 0
    ]]
    assert _fractions(case['expected_diversity']) == (_diversity(initial),)
    assert case['expected_transition_count'] == 0
    assert case['expected_reentry_events'] == []


def test_fully_external_second_step_differs_from_closed_absorption():
    case = DOCUMENT['two_step_external_endpoint']
    n = case['resample_size']
    external = _fractions(case['external'])
    assert Fraction(case['reopening_weight']) == 1
    first_counts = tuple(case['first_counts'])
    assert (_enumerate_multinomial(external, n)[first_counts]
            == Fraction(case['expected_first_counts_probability']))
    reopened_source = _fractions(case['expected_second_source_reopened'])
    closed_source = _fractions(case['expected_second_source_closed'])
    assert reopened_source == external
    assert closed_source == tuple(Fraction(count, n) for count in first_counts)
    for name, source in (('reopened', reopened_source), ('closed', closed_source)):
        chance = sum((p for counts, p in _enumerate_multinomial(source, n).items()
                      if counts[1] > 0), Fraction())
        assert chance == Fraction(case['expected_second_b_reentry_probability_' + name])
    assert reopened_source != closed_source
    one_step_mean = sum(
        (chance * _diversity(tuple(Fraction(c, n) for c in counts))
         for counts, chance in _enumerate_multinomial(external, n).items()),
        Fraction(),
    )
    assert _fractions(case['expected_diversity_by_step_reopened']) == (
        _diversity(_fractions(case['initial'])), one_step_mean, one_step_mean
    )


def test_existing_closed_analytic_kernel_matches_literal_closed_baseline():
    from recursive_integrity_toolkit.metrics.resampling import expected_diversity_after_steps
    from recursive_integrity_toolkit.models import (
        CalculationScope, RecordKey, RepresentationDescriptor,
    )
    case = DOCUMENT['two_step_external_endpoint']
    initial = dict(zip(case['state_order'], map(float, _fractions(case['initial'])),
                       strict=True))
    result = expected_diversity_after_steps(
        initial, resample_size=case['resample_size'], steps=2,
        scope=CalculationScope(('fixture',), (RecordKey('fixture', 'basis'),), (),
                               'explicit_scenario_basis', 'reopening-fixture-closed-control'),
        representation=RepresentationDescriptor('state', 'topic_field', 'fixture-v1',
                                                'literal_field_value', field_name='state'),
    )
    for actual, expected in zip(
        result.expected_diversity,
        _fractions(case['expected_diversity_by_step_closed']),
        strict=True,
    ):
        assert actual == pytest.approx(float(expected), abs=1e-12, rel=1e-12)
    assert result.random_seed is None
