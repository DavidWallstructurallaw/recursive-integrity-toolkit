"""T5/F-017 mixtures, transitions and events from independent rational cases.

Scripted draws isolate transition/event semantics. Real RNG checks separately
protect the accepted closed endpoint, frequency lattice and repeatability.
"""
from collections import Counter
from dataclasses import FrozenInstanceError
from fractions import Fraction
from math import factorial, fsum, sqrt
from types import MappingProxyType
import json

import pytest

from recursive_integrity_toolkit.errors import CanonicalValidationError, ErrorCode
from recursive_integrity_toolkit.models import (
    CalculationEvidenceClass, CalculationScope, RepresentationDescriptor,
)
from recursive_integrity_toolkit.metrics import resampling as module


def context():
    return dict(scope=CalculationScope(('scenario-v1',), (), (),
        'explicit_scenario_probability_vector', 'reopening-test'),
        representation=RepresentationDescriptor('topic', 'topic_field', 'v1',
            'literal_field_value', field_name='topic'))


def mix(internal=None, external=None, **kw):
    args = dict(reopening_weight=.25, **context()); args.update(kw)
    return module.mix_external_input(
        {'a': 1., 'b': 0.} if internal is None else internal,
        {'a': 0., 'b': 1.} if external is None else external, **args)


def sample(internal=None, external=None, **kw):
    args = dict(reopening_weight=.25, resample_size=4, steps=3,
        seed=17, replicates=2, **context()); args.update(kw)
    return module.simulate_reopened_resampling(
        {'a': 1., 'b': 0.} if internal is None else internal,
        {'a': 0., 'b': 1.} if external is None else external, **args)


@pytest.fixture
def cases(repo_root):
    return json.loads((repo_root / 'tests/fixtures/reopening/cases.json').read_bytes())


def distribution(states, probabilities):
    return dict(zip(states, (float(Fraction(value)) for value in probabilities)))


def event_ids(events):
    return tuple((event.replicate_index, event.step, event.state_id) for event in events)


def test_T5_authored_exact_mixture_cases(cases):
    for case in cases['one_step_cases']:
        states = case['state_order']
        actual = mix(distribution(states, case['internal']), distribution(states, case['external']),
            reopening_weight=float(Fraction(case['reopening_weight'])))
        expected = tuple(distribution(states, case['expected_mixed']).items())
        assert actual.mixed_inputs.supplied_distribution == expected
        assert actual.mixed_inputs.effective_distribution == expected
        assert actual.mixed_inputs.effective_probability_total == 1.
        assert actual.reachable_states == tuple(s for s, p in expected if p > 0)
        assert actual.possible_reentry_states == tuple(case['expected_reachable_absent_states'])
        assert 1 - fsum(p * p for _, p in expected) == float(Fraction(case['expected_mixed_diversity']))


def test_T5_reachability_is_not_realized_reentry(cases, monkeypatch):
    case = next(c for c in cases['one_step_cases']
        if c['case_id'] == 'partial_reopening_possible_not_guaranteed')
    for outcome in case['expected_positive_outcomes']:
        counts = tuple(outcome['counts'])
        monkeypatch.setattr(module, '_sample_counts', lambda *_args: counts)
        actual = sample(resample_size=2, steps=1, replicates=1)
        assert actual.mixed_sources[0].possible_reentry_states == ('b',)
        assert event_ids(actual.state_reentry_events) == (((0, 1, 'b'),) if counts[1] else ())
        assert event_ids(actual.extinction_events) == (((0, 1, 'a'),) if not counts[0] else ())


def test_T5_prescribed_repeated_loss_and_reentry(cases, monkeypatch):
    case = cases['prescribed_event_path']; transitions = case['transitions']
    draws = iter(tuple(t['counts']) for _ in range(2) for t in transitions); sources = []
    def draw(_rng, masses, n):
        assert n == case['resample_size']
        sources.append(masses)
        return next(draws)
    monkeypatch.setattr(module, '_sample_counts', draw)
    result = sample(distribution(case['state_order'], case['initial']),
        distribution(case['state_order'], case['external']),
        reopening_weight=float(Fraction(case['reopening_weight'])),
        resample_size=case['resample_size'], steps=len(transitions), replicates=2)
    assert sources == [(0.5, 0.5)] * 8
    assert event_ids(result.state_reentry_events) == tuple((rep, e['step'], e['state_id'])
        for rep in range(2) for e in case['expected_reentry_events'])
    assert event_ids(result.extinction_events) == tuple((rep, e['step'], e['state_id'])
        for rep in range(2) for e in case['expected_disappearance_events'])
    assert [(s.replicate_index, s.step) for s in result.mixed_sources] == [
        (rep, step) for rep in range(2) for step in range(1, 5)]
    for path in result.sampled_paths:
        assert path.generations[0].state_counts is None
        assert tuple(g.support for g in path.generations) == tuple(map(tuple, case['expected_support']))
        assert tuple(g.support_size for g in path.generations) == tuple(case['expected_support_sizes'])
        assert tuple(g.gini_simpson_diversity for g in path.generations) == tuple(
            float(Fraction(d)) for d in case['expected_diversity'])


def test_T5_every_transition_uses_current_internal_source(monkeypatch):
    draws = iter(((1, 1), (2, 0), (1, 1))); sources = []
    def draw(_rng, masses, _n):
        sources.append(masses)
        return next(draws)
    monkeypatch.setattr(module, '_sample_counts', draw)
    result = sample(resample_size=2, steps=3, replicates=1)
    expected = ((.75, .25), (.375, .625), (.75, .25))
    assert tuple(sources) == expected
    assert tuple(tuple(p for _, p in s.inputs.effective_distribution)
        for s in result.mixed_sources) == expected


@pytest.mark.parametrize('internal', [
    {'a': .5, 'b': .25, 'c': .25, 'zero': 0.},
    {'z': .5 + 4e-13, 'a': .25, 'A': .25, '': 0.},
])
@pytest.mark.parametrize('n,steps', [(1, 6), (7, 8), (17, 0)])
def test_T5_lambda_zero_exactly_retains_closed_paths(internal, n, steps):
    states = tuple(internal); external = dict.fromkeys(states, 0.); external[states[-1]] = 1.
    args = dict(resample_size=n, steps=steps, seed=13, replicates=4, **context())
    closed = module.simulate_closed_resampling(internal, **args)
    reopened = module.simulate_reopened_resampling(internal, external, reopening_weight=0., **args)
    assert reopened.inputs == closed.inputs
    assert reopened.state_order == closed.state_order == tuple(sorted(internal))
    assert reopened.sampled_paths == closed.sampled_paths
    assert reopened.state_reentry_events == ()


def test_T5_lambda_zero_keeps_integer_transition_masses(monkeypatch):
    original = module._sample_counts; calls = []
    def draw(rng, masses, n):
        calls.append(masses)
        return original(rng, masses, n)
    monkeypatch.setattr(module, '_sample_counts', draw)
    sample({'a': .5, 'b': .5 + 4e-13}, {'a': .1, 'b': .9},
        reopening_weight=0., resample_size=7, steps=4, replicates=1)
    assert all(type(mass) is float for mass in calls[0])
    assert all(type(mass) is int for call in calls[1:] for mass in call)
    assert all(sum(call) == 7 for call in calls[1:])


def test_T5_lambda_one_refreshes_external_source_after_disappearance(cases, monkeypatch):
    case = cases['two_step_external_endpoint']; draws = iter((tuple(case['first_counts']), (1, 1))); sources = []
    def draw(_rng, masses, _n):
        sources.append(masses)
        return next(draws)
    monkeypatch.setattr(module, '_sample_counts', draw)
    result = sample(distribution(case['state_order'], case['initial']),
        distribution(case['state_order'], case['external']),
        reopening_weight=1., resample_size=2, steps=2, replicates=1)
    assert sources == [(0.5, 0.5), (0.5, 0.5)]
    assert result.sampled_paths[0].generations[1].support == ('a',)
    assert event_ids(result.state_reentry_events) == ((0, 2, 'b'),)


def test_T5_lambda_one_preserves_effective_external_vector_without_second_correction():
    result = sample({'a': 1., 'b': 0.}, {'a': .5, 'b': .5 + 4e-13}, reopening_weight=1.)
    assert result.external_inputs.correction_applied
    for source in result.mixed_sources:
        assert source.inputs.supplied_distribution == result.external_inputs.effective_distribution
        assert source.inputs.effective_distribution == result.external_inputs.effective_distribution
        assert not source.inputs.correction_applied
    assert result.sampled_paths[0].generations[0].state_frequencies == (1., 0.)


def test_T5_horizon_zero_keeps_initial_without_events(cases):
    case = cases['zero_horizon']
    result = sample(distribution(case['state_order'], case['initial']),
        distribution(case['state_order'], case['external']), reopening_weight=1., steps=0)
    assert not result.mixed_sources
    assert not result.state_reentry_events and not result.extinction_events
    for path in result.sampled_paths:
        assert len(path.generations) == 1
        generation = path.generations[0]
        assert generation.step == 0 and generation.state_counts is None
        assert generation.state_frequencies == (1., 0.)
        assert generation.support == ('a',) and generation.gini_simpson_diversity == 0.


@pytest.mark.parametrize('n', [1, 2, 7, module.MAX_RESAMPLE_SIZE])
def test_T5_count_lattice_support_and_diversity(n):
    result = sample({'a': .6, 'b': .4, 'c': 0., 'zero': 0.},
        {'a': .1, 'b': .2, 'c': .7, 'zero': 0.}, resample_size=n, steps=5, replicates=4)
    for path in result.sampled_paths:
        for g in path.generations[1:]:
            assert all(type(c) is int and 0 <= c <= n for c in g.state_counts)
            assert sum(g.state_counts) == n
            assert g.state_frequencies == tuple(c / n for c in g.state_counts)
            assert fsum(g.state_frequencies) == pytest.approx(1., abs=1e-12)
            assert g.support == tuple(s for s, c in zip(result.state_order, g.state_counts) if c)
            assert g.support_size == sum(c > 0 for c in g.state_counts)
            assert g.gini_simpson_diversity == pytest.approx(
                float(1 - sum(Fraction(c, n) ** 2 for c in g.state_counts)), abs=1e-12)
            assert g.state_counts[-1] == 0
            if n == 1:
                assert g.support_size == 1 and g.gini_simpson_diversity == 0.


def test_T5_sampled_marginals_agree_with_authored_one_step_case(cases):
    case = next(c for c in cases['one_step_cases']
        if c['case_id'] == 'partial_reopening_possible_not_guaranteed')
    result = sample(resample_size=2, steps=1, replicates=8000, seed=812)
    reentry_fraction = len(result.state_reentry_events) / result.simulation_replicates
    mean_diversity = fsum(p.generations[1].gini_simpson_diversity
        for p in result.sampled_paths) / result.simulation_replicates
    assert abs(reentry_fraction - float(Fraction(case['expected_reentry_probability_by_absent_state']['b']))) < .025
    assert abs(mean_diversity - float(Fraction(case['expected_sample_diversity']))) < .025


def test_T5_three_state_joint_counts_match_exact_multinomial_enumeration():
    # The second conditional draw has probability 3/4. This exercises the
    # complement branch as well as dependence between three category counts;
    # two-state re-entry or diversity averages alone cannot establish that law.
    source = (Fraction(1, 2), Fraction(3, 8), Fraction(1, 8))
    n = 3
    outcomes = {}
    for a in range(n + 1):
        for b in range(n - a + 1):
            counts = (a, b, n - a - b)
            probability = Fraction(factorial(n))
            for count, mass in zip(counts, source):
                probability *= mass ** count / factorial(count)
            outcomes[counts] = probability
    assert len(outcomes) == 10 and sum(outcomes.values()) == 1
    assert sum(probability for counts, probability in outcomes.items()
        if counts[2] > 0) == Fraction(169, 512)
    assert sum(probability * (1 - sum(Fraction(count, n) ** 2 for count in counts))
        for counts, probability in outcomes.items()) == Fraction(19, 48)

    replicates = 10000
    result = sample({'a': .75, 'b': .25, 'c': 0.},
        {'a': .25, 'b': .5, 'c': .25}, reopening_weight=.5,
        resample_size=n, steps=1, replicates=replicates, seed=937)
    observed = Counter(path.generations[1].state_counts for path in result.sampled_paths)
    assert set(observed) <= set(outcomes)
    # Six binomial standard deviations per joint outcome gives a broad numerical
    # sanity bound without pinning paths across supported NumPy environments.
    for counts, exact_probability in outcomes.items():
        probability = float(exact_probability)
        tolerance = 6 * sqrt(probability * (1 - probability) / replicates) + 1 / replicates
        assert abs(observed[counts] / replicates - probability) < tolerance


def test_T5_fixed_seed_order_invariance_and_immutable_detached_results():
    internal = {'z': .5, '': 0., 'a': .5}; external = {'a': .25, 'z': .25, '': .5}
    a = sample(internal, external)
    b = sample(tuple(reversed(tuple(internal.items()))), MappingProxyType(external))
    assert a == b == sample(internal, external)
    assert a.state_order == ('', 'a', 'z')
    internal['a'] = 0.; external[''] = 0.
    assert dict(a.inputs.supplied_distribution)['a'] == .5
    assert dict(a.external_inputs.supplied_distribution)[''] == .5
    with pytest.raises(FrozenInstanceError): a.sampled_paths = ()
    with pytest.raises(FrozenInstanceError): a.mixed_sources[0].step = 0
    with pytest.raises(TypeError): a.mixed_sources[0].inputs.effective_distribution[0] = ('changed', 1.)


@pytest.mark.parametrize('seed', [0, 17, 2 ** 128 + 1])
def test_T5_explicit_rng_identity_and_untouched_global_rng(seed, monkeypatch):
    import random
    import numpy as np
    before = np.random.get_state(); pybefore = random.getstate(); captured = []; original = np.random.PCG64
    def pcg(value):
        captured.append(value)
        return original(value)
    monkeypatch.setattr(np.random, 'PCG64', pcg)
    result = sample(seed=seed); after = np.random.get_state()
    assert captured == [seed]
    assert before[0] == after[0] and (before[1] == after[1]).all() and before[2:] == after[2:]
    assert pybefore == random.getstate()
    assert result.random_seed == seed and result.numpy_version == np.__version__
    assert result.rng_name == 'numpy.random.Generator(PCG64)'
    assert result.sampler_algorithm == 'sequential_binomial_complement_v1'
    assert result.replicate_schedule == 'replicate_major_step_major'


@pytest.mark.parametrize('residual', [-4e-13, 4e-13])
def test_T5_internal_external_and_mixed_corrections_are_disclosed(residual):
    internal = {'a': .5, 'b': .5 + residual, 'zero': 0.}
    external = {'a': .25, 'b': .75 - residual, 'zero': 0.}; result = mix(internal, external)
    for source, supplied in ((result.inputs, internal), (result.external_inputs, external)):
        assert source.correction_applied and source.correction_method == 'divide_by_validated_total'
        assert source.supplied_probability_total == fsum(supplied.values())
        assert source.probability_residual == source.supplied_probability_total - 1.
        assert source.normalization_divisor == source.supplied_probability_total
        assert dict(source.effective_distribution) == {s: p / source.normalization_divisor for s, p in supplied.items()}
        assert dict(source.probability_corrections) == {s: p / source.normalization_divisor - p for s, p in supplied.items()}
    expected_raw = tuple((s, fsum((.75 * p, .25 * r))) for (s, p), (_, r) in
        zip(result.inputs.effective_distribution, result.external_inputs.effective_distribution))
    mixed = result.mixed_inputs
    assert mixed.supplied_distribution == expected_raw
    assert mixed.normalization_divisor == (fsum(p for _, p in expected_raw) if mixed.correction_applied else 1.)
    assert mixed.effective_distribution == tuple((s, p / mixed.normalization_divisor) for s, p in expected_raw)
    assert dict(mixed.effective_distribution)['zero'] == 0.
    assert all(abs(delta) <= 1e-12 for _, delta in mixed.probability_corrections)


def test_T5_mixed_total_roundoff_gets_its_own_disclosed_correction():
    result = mix({'a': .1, 'b': .4, 'c': .5000000000004},
        {'a': .1, 'b': .1, 'c': .7999999999996}, reopening_weight=.3)
    source = result.mixed_inputs
    expected_raw = tuple((s, fsum((.7 * p, .3 * r))) for (s, p), (_, r) in
        zip(result.inputs.effective_distribution, result.external_inputs.effective_distribution))
    expected_total = fsum(p for _, p in expected_raw)
    assert expected_total != 1.
    assert source.supplied_distribution == expected_raw
    assert source.correction_applied and source.correction_method == 'divide_by_validated_total'
    assert source.normalization_divisor == source.supplied_probability_total == expected_total
    assert source.probability_residual == expected_total - 1.
    assert source.effective_distribution == tuple((s, p / expected_total) for s, p in expected_raw)
    assert source.probability_corrections == tuple((s, p / expected_total - p) for s, p in expected_raw)


@pytest.mark.parametrize('weight', [0., 1.])
def test_T5_endpoints_do_not_renormalize_remaining_roundoff(weight):
    vector = {'a': .1, 'b': .4, 'c': .5000000000004}
    mixture = mix(vector, vector, reopening_weight=weight)
    expected = mixture.inputs.effective_distribution
    assert mixture.inputs.correction_applied and fsum(p for _, p in expected) != 1.
    assert mixture.mixed_inputs.supplied_distribution == expected
    assert mixture.mixed_inputs.effective_distribution == expected
    assert not mixture.mixed_inputs.correction_applied
    result = sample(vector, vector, reopening_weight=weight, steps=1)
    assert result.sampled_paths[0].generations[0].state_frequencies == tuple(p for _, p in expected)
    for source in result.mixed_sources:
        assert source.inputs.effective_distribution == expected
        assert not source.inputs.correction_applied


@pytest.mark.parametrize('internal,external,weight', [
    ({'a': 1., 'b': 0.}, {'a': .5, 'b': .5}, 5e-324),
    ({'a': 1., 'b': 5e-324}, {'a': 1., 'b': 0.}, .5),
])
def test_T5_underflow_cannot_erase_positive_mixture_before_rng(internal, external, weight, monkeypatch):
    import builtins
    original = builtins.__import__
    def guard(name, *args, **kw):
        if name == 'numpy': raise AssertionError('NumPy reached before numerical refusal')
        return original(name, *args, **kw)
    monkeypatch.setattr(builtins, '__import__', guard)
    for method in (mix, sample):
        with pytest.raises(CanonicalValidationError): method(internal, external, reopening_weight=weight)


def test_T5_representable_tiny_positive_reachability_is_preserved():
    result = mix({'a': 1., 'b': 0.}, {'a': 1., 'b': 5e-324}, reopening_weight=1.)
    assert dict(result.mixed_inputs.effective_distribution)['b'] == 5e-324
    assert result.possible_reentry_states == ('b',)


def test_T5_future_external_underflow_refused_before_rng(monkeypatch):
    internal = external = {'a': .5, 'b': .5}
    one_step = sample(internal, external, reopening_weight=5e-324, steps=1)
    assert one_step.mixed_sources[0].inputs.effective_distribution == (('a', .5), ('b', .5))
    import builtins
    original = builtins.__import__
    def guard(name, *args, **kw):
        if name == 'numpy': raise AssertionError('NumPy reached before future-reachability refusal')
        return original(name, *args, **kw)
    monkeypatch.setattr(builtins, '__import__', guard)
    with pytest.raises(CanonicalValidationError):
        sample(internal, external, reopening_weight=5e-324, steps=2)


def test_T5_horizon_zero_has_no_unexecuted_mixture_underflow():
    result = sample({'a': 1., 'b': 0.}, {'a': .5, 'b': .5},
        reopening_weight=5e-324, steps=0)
    assert not result.mixed_sources and not result.state_reentry_events
    assert all(p.generations[0].state_frequencies == (1., 0.) for p in result.sampled_paths)


@pytest.mark.parametrize('weight', [True, False, -.1, 1.1, float('nan'), float('inf'),
    None, '0.5', Fraction(1, 2), 10 ** 1000])
@pytest.mark.parametrize('method', [mix, sample])
def test_T5_invalid_weight_rejected(weight, method):
    with pytest.raises(CanonicalValidationError): method(reopening_weight=weight)


@pytest.mark.parametrize('value', [{}, (), [], {'a': 0., 'b': 0.}, {'a': .2, 'b': .3},
    {'a': .5, 'b': .500000000002}, {'a': -5e-324, 'b': 1.}, {'a': float('nan'), 'b': 1.},
    {'a': float('inf'), 'b': 0.}, {'a': True, 'b': 0.}, {'a': Fraction(1), 'b': 0.},
    (('a', .5), ('a', .5)), ((1, 1.),), (('a', 1., 2.),), {'\x00': 1.}, {'\ud800': 1.}, {'different': 1.}])
@pytest.mark.parametrize('side', ['internal', 'external'])
def test_T5_both_vectors_require_independent_validation(value, side, monkeypatch):
    import builtins
    original = builtins.__import__
    def guard(name, *args, **kw):
        if name == 'numpy': raise AssertionError('NumPy reached before vector validation')
        return original(name, *args, **kw)
    monkeypatch.setattr(builtins, '__import__', guard)
    for method in (mix, sample):
        with pytest.raises(CanonicalValidationError): method(**{side: value})


@pytest.mark.parametrize('weight', [0., 1.])
def test_T5_endpoint_does_not_skip_unused_vector_validation(weight):
    for internal, external in (({'a': .2, 'b': .3}, {'a': 1., 'b': 0.}),
            ({'a': 1., 'b': 0.}, {'a': .2, 'b': .3})):
        with pytest.raises(CanonicalValidationError): sample(internal, external, reopening_weight=weight)


@pytest.mark.parametrize('name,value', [('resample_size', 0), ('resample_size', True),
    ('steps', -1), ('steps', True), ('seed', -1), ('seed', True), ('replicates', 0),
    ('replicates', 1.5), ('scope', None), ('representation', None)])
def test_T5_invalid_execution_parameters_precede_rng(name, value, monkeypatch):
    import numpy as np
    def blocked(*_args, **_kw): raise AssertionError('RNG created before parameter validation')
    monkeypatch.setattr(np.random, 'PCG64', blocked)
    with pytest.raises(CanonicalValidationError): sample(**{name: value})


@pytest.mark.parametrize('options', [{'steps': module.MAX_STEPS + 1},
    {'resample_size': module.MAX_RESAMPLE_SIZE + 1}, {'replicates': module.MAX_REPLICATES + 1},
    {'seed': 1 << module.MAX_SEED_BITS}, {'steps': 10000, 'replicates': 10000}])
def test_T5_resource_refusal_before_numpy_or_trajectory_allocation(options, monkeypatch):
    import builtins
    original = builtins.__import__
    def guard(name, *args, **kw):
        if name == 'numpy': raise AssertionError('NumPy reached before resource refusal')
        return original(name, *args, **kw)
    def blocked(*_args, **_kw): raise AssertionError('trajectory allocated before resource refusal')
    monkeypatch.setattr(builtins, '__import__', guard); monkeypatch.setattr(module, '_generation', blocked)
    with pytest.raises(CanonicalValidationError) as error: sample(**options)
    assert error.value.code is ErrorCode.CONFIG_INVALID


def test_T5_state_limit_rejected_by_pure_and_sampled_methods():
    vector = {str(i): 1 / (module.MAX_STATES + 1) for i in range(module.MAX_STATES + 1)}
    for method in (mix, sample):
        with pytest.raises(CanonicalValidationError) as error: method(vector, vector)
        assert error.value.code is ErrorCode.CONFIG_INVALID


def test_T5_untrusted_conversion_hooks_never_execute():
    class Hostile:
        def __float__(self): raise AssertionError('float')
        def __iter__(self): raise AssertionError('iter')
        def __bool__(self): raise AssertionError('bool')
        def __str__(self): raise AssertionError('str')
    for method in (mix, sample):
        for value in (Hostile(), {'a': Hostile()}, ((Hostile(), 1.),)):
            for side in ('internal', 'external'):
                with pytest.raises(CanonicalValidationError): method(**{side: value})
        with pytest.raises(CanonicalValidationError): method(reopening_weight=Hostile())


@pytest.mark.parametrize('field', ['reopening_weight', 'resample_size', 'steps', 'seed',
    'replicates', 'scope', 'representation'])
def test_T5_all_sampler_parameters_are_explicit(field):
    args = dict(reopening_weight=.5, resample_size=2, steps=1, seed=0, replicates=1, **context()); del args[field]
    with pytest.raises(TypeError): module.simulate_reopened_resampling({'a': 1.}, {'a': 1.}, **args)


def test_T5_metadata_retains_conditional_simulation_owner_and_scope():
    result = sample(); mixture = mix()
    assert result.model_name == 'reopened_resampling' and result.method == 'sampled_path'
    assert result.method_version == 'reopened_categorical_constant_v1'
    for value in (result, mixture):
        assert value.evidence_class is CalculationEvidenceClass.SIMULATION and value.experimental
        assert value.assumptions and value.limitations
        assert value.inputs.scope == value.external_inputs.scope == context()['scope']
        assert value.inputs.representation == value.external_inputs.representation == context()['representation']
    assert not hasattr(result, 'expected_diversity') and not hasattr(result, 'causal_effect')
    assert not hasattr(module, 'external_reference_loss')
    assert mixture.mixture_metadata.formula_id == 'F-017'
    for metadata in result.trajectory_metadata + (mixture.mixture_metadata,):
        assert metadata.owner_id == 'T5' and metadata.evidence_class is CalculationEvidenceClass.SIMULATION
        assert metadata.unit and metadata.method and metadata.assumptions and metadata.limitations


def test_T5_no_io_or_raw_state_logging(monkeypatch, capsys):
    import builtins
    import socket
    import numpy  # preload dependency before blocking runtime I/O
    from pathlib import Path
    private_context = dict(scope=CalculationScope(('PRIVATE_VERSION',), (), (),
        'PRIVATE_BASIS', 'PRIVATE_SCOPE'), representation=RepresentationDescriptor(
            'PRIVATE_REP', 'topic_field', 'PRIVATE_REP_VERSION', 'PRIVATE_NORMALIZATION',
            field_name='PRIVATE_FIELD'))
    def blocked(*_args, **_kw): raise AssertionError('unexpected I/O or execution')
    with monkeypatch.context() as patch:
        for name in ('open', 'eval', 'exec'): patch.setattr(builtins, name, blocked)
        patch.setattr(Path, 'open', blocked); patch.setattr(socket, 'create_connection', blocked)
        patch.setattr(socket, 'getaddrinfo', blocked)
        mixture = mix({'PRIVATE_STATE': 1.}, {'PRIVATE_STATE': 1.}, **private_context)
        result = sample({'PRIVATE_STATE': 1.}, {'PRIVATE_STATE': 1.}, **private_context)
    assert 'PRIVATE_' not in repr(mixture) and 'PRIVATE_' not in repr(result)
    assert capsys.readouterr() == ('', '')


def test_T5_pure_mixture_without_numpy_and_explicit_sampling_failure(subprocess_env):
    import subprocess
    import sys
    code = '''import sys, importlib.abc
class Block(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in {'numpy', 'pandas', 'pyarrow'}:
            raise ModuleNotFoundError('blocked')
sys.meta_path.insert(0, Block())
from recursive_integrity_toolkit.metrics.resampling import mix_external_input, simulate_reopened_resampling
from recursive_integrity_toolkit.models import CalculationScope, RepresentationDescriptor
from recursive_integrity_toolkit.errors import CanonicalValidationError
ctx = dict(scope=CalculationScope(('v1',), (), (), 'scenario', 'import'),
    representation=RepresentationDescriptor('topic', 'topic_field', 'v1', 'literal', field_name='topic'))
mix = mix_external_input({'a': 1., 'b': 0.}, {'a': 0., 'b': 1.}, reopening_weight=.25, **ctx)
assert mix.mixed_inputs.effective_distribution == (('a', .75), ('b', .25))
try:
    simulate_reopened_resampling({'a': 1.}, {'a': 1.}, reopening_weight=.5,
        resample_size=2, steps=1, replicates=1, seed=0, **ctx)
except CanonicalValidationError:
    pass
else:
    raise AssertionError('missing NumPy did not block sampling')
assert not {'numpy', 'pandas', 'pyarrow'} & set(sys.modules)
'''
    completed = subprocess.run([sys.executable, '-S', '-c', code], env=subprocess_env,
        capture_output=True, text=True)
    assert completed.returncode == 0, completed.stderr
