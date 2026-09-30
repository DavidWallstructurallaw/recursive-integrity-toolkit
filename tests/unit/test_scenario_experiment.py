"""Explicit scenario selection, common admission and per-path comparisons.

Kernel mathematics already have independent T1/T5 oracles. These tests protect
what experiment orchestration may execute and what its evidence actually means.
"""
from dataclasses import FrozenInstanceError
from math import fsum

import numpy as np
import pytest

from recursive_integrity_toolkit.errors import CanonicalValidationError
from recursive_integrity_toolkit.models import (
    CalculationScope, RepresentationDescriptor, ScenarioParameters,
)
from recursive_integrity_toolkit.metrics import resampling as module


CLOSED = 'closed_resampling'
REOPENED = 'reopened_resampling'


def parameters(model=CLOSED, **changes):
    values = dict(model_name=model, resample_size=4, simulation_horizon=3,
        simulation_replicates=2, state_distribution=(('a', .5), ('b', .5)))
    if model == REOPENED:
        values.update(external_input_distribution=(('a', .25), ('b', .75)),
            reopening_weight=.5)
    values.update(changes)
    return ScenarioParameters(**values)


def request(models=(CLOSED, REOPENED), *, scenarios=None, **changes):
    values = dict(scenarios=tuple(parameters(model) for model in models)
        if scenarios is None else scenarios,
        scope=CalculationScope(('scenario-v1',), (), (),
            'explicit_scenario_probability_vector', 'experiment-test'),
        representation=RepresentationDescriptor('topic', 'topic_field', 'v1',
            'literal_field_value', field_name='topic'),
        state_semantics='Literal categories shared by both synthetic scenarios', seed=29)
    values.update(changes)
    return module.ScenarioExperimentRequest(**values)


def run(models=(CLOSED, REOPENED), **changes):
    return module.run_scenario_experiment(request(models, **changes))


def by_model(result):
    return {selected.model_name: selected for selected in result.selected_results}


def event_ids(events):
    return tuple((event.replicate_index, event.step, event.state_id) for event in events)


def forbid_work(monkeypatch):
    def forbidden(*_args, **_kwargs):
        pytest.fail('Invalid experiment started numerical execution or path allocation')
    for name in ('simulate_closed_resampling', 'simulate_reopened_resampling',
            'expected_diversity_after_steps', '_generation', '_sample_counts'):
        monkeypatch.setattr(module, name, forbidden)
    monkeypatch.setattr(np.random, 'PCG64', forbidden)


@pytest.mark.parametrize('models', [(CLOSED,), (REOPENED,),
    (CLOSED, REOPENED), (REOPENED, CLOSED)])
def test_experiment_executes_only_explicit_models_in_order(models, monkeypatch):
    sampled = []; analytic = []
    for name, model in (('simulate_closed_resampling', CLOSED),
            ('simulate_reopened_resampling', REOPENED)):
        original = getattr(module, name)
        def record(*args, _original=original, _model=model, **kwargs):
            sampled.append((_model, kwargs['seed']))
            return _original(*args, **kwargs)
        monkeypatch.setattr(module, name, record)
    original_expected = module.expected_diversity_after_steps
    def expected(*args, **kwargs):
        analytic.append(args[0])
        return original_expected(*args, **kwargs)
    monkeypatch.setattr(module, 'expected_diversity_after_steps', expected)
    declared = request(models)
    result = module.run_scenario_experiment(declared)
    assert sampled == [(model, declared.seed) for model in models]
    assert tuple(selected.model_name for selected in result.selected_results) == models
    assert result.request == declared
    assert result.scenario_schedule == 'reset_same_seed_per_model'
    assert len(analytic) == int(CLOSED in models)
    assert (result.closed_analytic_baseline is not None) == (CLOSED in models)
    assert result.baseline_basis == (
        'closed_sampled_effective_distribution' if CLOSED in models else None)
    assert (result.comparison is not None) == (len(models) == 2)
    if CLOSED not in models:
        assert result.closed_extinction_events == ()


def test_closed_baseline_uses_effective_sampled_start_and_keeps_correction(monkeypatch):
    supplied = (('b', .5), ('a', .5 + 4e-13))
    declared = request((CLOSED,), scenarios=(parameters(state_distribution=supplied),))
    passed = []
    original = module.expected_diversity_after_steps
    def expected(initial, **kwargs):
        passed.append(initial)
        return original(initial, **kwargs)
    monkeypatch.setattr(module, 'expected_diversity_after_steps', expected)
    result = module.run_scenario_experiment(declared)
    closed = result.selected_results[0]; baseline = result.closed_analytic_baseline
    assert closed.inputs.correction_applied
    assert closed.inputs.supplied_distribution == tuple(sorted(supplied))
    assert closed.inputs.effective_distribution != closed.inputs.supplied_distribution
    assert passed == [closed.inputs.effective_distribution]
    assert baseline.inputs.supplied_distribution == closed.inputs.effective_distribution
    assert baseline.initial_gini_simpson_diversity == closed.sampled_paths[0].generations[0].gini_simpson_diversity
    d0 = 1 - fsum(p * p for _, p in closed.inputs.effective_distribution)
    assert baseline.expected_diversity == pytest.approx(tuple(d0 * .75 ** step for step in range(4)))
    assert baseline.expected_diversity_metadata.formula_id == 'F-015'
    assert baseline.random_seed is None and baseline.simulation_replicates is None
    assert result.request.scenarios[0].state_distribution == supplied


def test_each_model_is_independent_of_selection_order_and_other_model():
    both = run(); reverse = run((REOPENED, CLOSED))
    for model in (CLOSED, REOPENED):
        assert by_model(both)[model] == by_model(reverse)[model] == run((model,)).selected_results[0]
    assert both.comparison == reverse.comparison
    for selected in both.selected_results:
        assert selected.random_seed == both.request.seed
        assert selected.rng_name == 'numpy.random.Generator(PCG64)'
        assert selected.sampler_algorithm == 'sequential_binomial_complement_v1'
        assert selected.replicate_schedule == 'replicate_major_step_major'
        assert selected.numpy_version == np.__version__


def test_comparison_retains_exact_per_replicate_values_and_direction(monkeypatch):
    # Both signs matter: reopening first loses b, then restores it as closed loses b.
    draws = iter(((1, 1), (2, 0), (2, 0), (1, 1)))
    monkeypatch.setattr(module, '_sample_counts', lambda *_args: next(draws))
    scenarios = tuple(parameters(model, resample_size=2, simulation_horizon=2,
        simulation_replicates=1) for model in (CLOSED, REOPENED))
    result = run(scenarios=scenarios)
    comparison = result.comparison
    assert comparison.difference_direction == 'reopened_minus_closed'
    rows = comparison.rows
    assert [(r.replicate_index, r.step) for r in rows] == [(0, 0), (0, 1), (0, 2)]
    assert [(r.closed_support_size, r.reopened_support_size, r.support_size_difference)
        for r in rows] == [(2, 2, 0), (2, 1, -1), (1, 2, 1)]
    assert [(r.closed_gini_simpson_diversity, r.reopened_gini_simpson_diversity,
        r.diversity_difference) for r in rows] == [(.5, .5, 0.), (.5, 0., -.5), (0., .5, .5)]
    assert event_ids(result.closed_extinction_events) == ((0, 2, 'b'),)
    assert event_ids(by_model(result)[REOPENED].extinction_events) == ((0, 1, 'b'),)
    assert event_ids(by_model(result)[REOPENED].state_reentry_events) == ((0, 2, 'b'),)


def test_comparison_rows_cover_each_path_without_pooling():
    result = run()
    closed, reopened = (by_model(result)[model] for model in (CLOSED, REOPENED))
    assert [(row.replicate_index, row.step) for row in result.comparison.rows] == [
        (rep, step) for rep in range(2) for step in range(4)]
    for row in result.comparison.rows:
        left = closed.sampled_paths[row.replicate_index].generations[row.step]
        right = reopened.sampled_paths[row.replicate_index].generations[row.step]
        assert (row.closed_support_size, row.reopened_support_size) == (left.support_size, right.support_size)
        assert row.support_size_difference == right.support_size - left.support_size
        assert row.diversity_difference == right.gini_simpson_diversity - left.gini_simpson_diversity
        if row.step == 0:
            assert row.support_size_difference == row.diversity_difference == 0


def test_lambda_zero_comparison_has_identical_paths_and_zero_differences():
    result = run(scenarios=(parameters(), parameters(REOPENED, reopening_weight=0.)))
    assert by_model(result)[CLOSED].sampled_paths == by_model(result)[REOPENED].sampled_paths
    assert all(row.support_size_difference == row.diversity_difference == 0
        for row in result.comparison.rows)


def test_initial_reachability_uses_pre_first_draw_model_sources():
    p = (('c', 0.), ('b', .5), ('', 0.), ('a', .5))
    r = (('a', 0.), ('', 0.), ('b', 0.), ('c', 1.))
    result = run(scenarios=(parameters(state_distribution=p),
        parameters(REOPENED, state_distribution=p, external_input_distribution=r,
            reopening_weight=1.)))
    possibilities = result.comparison.initial_reachability
    assert tuple(item.model_name for item in possibilities) == (CLOSED, REOPENED)
    assert all(item.timing == 'before_first_draw' for item in possibilities)
    assert possibilities[0].reachable_states == ('a', 'b')
    assert possibilities[0].possible_reentry_states == ()
    assert possibilities[1].reachable_states == ('c',)
    assert possibilities[1].possible_reentry_states == ('c',)
    assert by_model(result)[REOPENED].sampled_paths[0].generations[0].support == ('a', 'b')


def test_horizon_zero_has_structural_possibility_without_mixing_or_transitions(monkeypatch):
    def forbidden(*_args, **_kwargs):
        pytest.fail('Horizon zero evaluated a transition mixture')
    monkeypatch.setattr(module, '_mixed_source', forbidden)
    p = (('a', 1.), ('b', 0.)); r = (('a', .75), ('b', .25))
    scenarios = (parameters(state_distribution=p, simulation_horizon=0),
        parameters(REOPENED, state_distribution=p, simulation_horizon=0,
            external_input_distribution=r, reopening_weight=5e-324))
    result = run(scenarios=scenarios)
    initial = result.comparison.initial_reachability
    assert initial[0].reachable_states == ('a',)
    assert initial[1].reachable_states == ('a', 'b')
    assert initial[1].possible_reentry_states == ('b',)
    assert [(row.replicate_index, row.step) for row in result.comparison.rows] == [(0, 0), (1, 0)]
    assert result.closed_extinction_events == ()
    assert by_model(result)[REOPENED].mixed_sources == ()
    assert by_model(result)[REOPENED].state_reentry_events == ()
    assert by_model(result)[REOPENED].extinction_events == ()


def test_common_distribution_may_use_different_order_and_literal_empty_state():
    p = (('z', .5), ('', 0.), ('A', .5))
    result = run(scenarios=(parameters(state_distribution=p), parameters(REOPENED,
        state_distribution=tuple(reversed(p)), external_input_distribution=p)))
    assert all(selected.state_order == ('', 'A', 'z') for selected in result.selected_results)
    assert by_model(result)[CLOSED].inputs.supplied_distribution == by_model(result)[REOPENED].inputs.supplied_distribution


@pytest.mark.parametrize('changes', [
    {'resample_size': 5}, {'simulation_horizon': 4}, {'simulation_replicates': 3},
    {'state_distribution': (('a', .25), ('b', .75))},
    # Equal after normalization is insufficient: supplied declarations conflict.
    {'state_distribution': (('a', .5 + 1e-13), ('b', .5 + 1e-13))},
])
def test_conflicting_common_parameters_rejected_before_any_selected_model(changes, monkeypatch):
    forbid_work(monkeypatch)
    with pytest.raises(CanonicalValidationError):
        run(scenarios=(parameters(), parameters(REOPENED, **changes)))


@pytest.mark.parametrize('scenarios', [
    (), (parameters(), parameters()),
    (parameters(), parameters(REOPENED), parameters()),
    (parameters('unregistered_model'),),
    (parameters(external_input_distribution=(('a', .5), ('b', .5))),),
    (parameters(reopening_weight=0.),),
    (parameters(REOPENED, external_input_distribution=None),),
    (parameters(REOPENED, reopening_weight=None),),
    (parameters(REOPENED, reopening_weight=True),),
    (parameters(REOPENED, reopening_weight=1.01),),
    (parameters(REOPENED, external_input_distribution=(('a', 1.), ('c', 0.))),),
    (parameters(resample_size=True),), (parameters(simulation_horizon=-1),),
    (parameters(simulation_replicates=0),),
    (parameters(state_distribution=(('a', .4), ('b', .4))),),
])
def test_invalid_declaration_rejected_before_execution(scenarios, monkeypatch):
    forbid_work(monkeypatch)
    with pytest.raises(CanonicalValidationError):
        run(scenarios=scenarios)


def test_reopened_future_underflow_preflight_precedes_closed_execution(monkeypatch):
    forbid_work(monkeypatch)
    # First mixture has internal support, but the next mixture could erase tiny
    # external mass after a sampled loss. No closed path may start first.
    with pytest.raises(CanonicalValidationError):
        run(scenarios=(parameters(), parameters(REOPENED, reopening_weight=5e-324,
            external_input_distribution=(('a', .5), ('b', .5)))))


def test_combined_path_cell_limit_precedes_rng_and_generation_allocation(monkeypatch):
    forbid_work(monkeypatch)
    scenarios = tuple(parameters(model, simulation_horizon=10000,
        simulation_replicates=25) for model in (CLOSED, REOPENED))
    cells_each = 2 * (10000 + 1) * 25
    assert cells_each <= module.MAX_PATH_CELLS < 2 * cells_each
    with pytest.raises(CanonicalValidationError):
        run(scenarios=scenarios)


def test_combined_path_cell_limit_is_inclusive(monkeypatch):
    monkeypatch.setattr(module, 'MAX_PATH_CELLS', 16)
    scenarios = tuple(parameters(model, simulation_horizon=1,
        simulation_replicates=2) for model in (CLOSED, REOPENED))
    result = run(scenarios=scenarios)
    assert sum(len(selected.state_order) * sum(len(path.generations)
        for path in selected.sampled_paths) for selected in result.selected_results) == 16


@pytest.mark.parametrize('seed', [True, -1, 2 ** 53, 3.0])
def test_experiment_seed_requires_report_safe_integer(seed, monkeypatch):
    forbid_work(monkeypatch)
    with pytest.raises(CanonicalValidationError):
        run(seed=seed)


def test_report_safe_seed_upper_endpoint_is_retained():
    result = run((REOPENED,), seed=2 ** 53 - 1,
        scenarios=(parameters(REOPENED, simulation_horizon=0),))
    assert result.request.seed == result.selected_results[0].random_seed == 2 ** 53 - 1


@pytest.mark.parametrize('state_semantics', ['', True, 'invalid\0meaning'])
def test_state_meaning_is_explicit_literal_text(state_semantics, monkeypatch):
    forbid_work(monkeypatch)
    with pytest.raises(CanonicalValidationError):
        run(state_semantics=state_semantics)


def test_mutable_or_untyped_declaration_is_not_admitted(monkeypatch):
    forbid_work(monkeypatch)
    invalid = (
        {'scenarios': [parameters()]},
        {'scenarios': ({'model_name': CLOSED},)},
        {'scenarios': (parameters(state_distribution=[('a', .5), ('b', .5)]),)},
        {'scenarios': (parameters(REOPENED, external_input_distribution={'a': .5, 'b': .5}),)},
        {'scope': 'scope'}, {'representation': 'representation'},
    )
    for changes in invalid:
        with pytest.raises(CanonicalValidationError):
            run(**changes)
    with pytest.raises(CanonicalValidationError):
        module.run_scenario_experiment({'scenarios': (parameters(),)})


def test_invalid_values_never_invoke_numeric_conversion_hooks(monkeypatch):
    forbid_work(monkeypatch)
    class FloatHook:
        def __float__(self):
            pytest.fail('Untrusted numeric conversion hook was invoked')
    for changes in ({'reopening_weight': FloatHook()},
            {'state_distribution': (('a', FloatHook()), ('b', .5))}):
        with pytest.raises(CanonicalValidationError):
            run((REOPENED,), scenarios=(parameters(REOPENED, **changes),))


def test_request_construction_is_inert_and_result_is_immutable(monkeypatch):
    with monkeypatch.context() as guarded:
        forbid_work(guarded)
        declared = request()
    with pytest.raises(FrozenInstanceError):
        declared.seed = 8
    with pytest.raises(FrozenInstanceError):
        declared.scenarios[0].resample_size = 8
    result = module.run_scenario_experiment(declared)
    with pytest.raises(FrozenInstanceError):
        result.scenario_schedule = 'shared_rng'
    with pytest.raises(FrozenInstanceError):
        result.comparison.rows[0].step = 8


def test_request_and_result_repr_hide_caller_labels_and_state_meaning():
    private_state = 'private-state-id'; private_meaning = 'private-state-meaning'
    p = ((private_state, 1.), ('', 0.))
    declared = request(state_semantics=private_meaning,
        scenarios=(parameters(state_distribution=p), parameters(REOPENED,
            state_distribution=p, external_input_distribution=p)))
    result = module.run_scenario_experiment(declared)
    for text in (repr(declared), repr(result), repr(result.comparison)):
        assert private_state not in text
        assert private_meaning not in text


def test_experiment_does_not_read_or_change_numpy_global_rng(monkeypatch):
    before = np.random.get_state()
    def forbidden(*_args, **_kwargs):
        pytest.fail('Experiment used the NumPy global/default RNG')
    with monkeypatch.context() as guarded:
        for name in ('seed', 'binomial', 'multinomial', 'default_rng', 'get_state', 'set_state'):
            guarded.setattr(np.random, name, forbidden)
        run()
    after = np.random.get_state()
    assert before[0] == after[0]
    assert np.array_equal(before[1], after[1])
    assert before[2:] == after[2:]
