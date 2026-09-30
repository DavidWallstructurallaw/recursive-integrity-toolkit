"""Supplied scenario evidence remains bound, complete, and purely simulated.

The kernels have separate mathematical tests. These checks protect the boundary
where immutable execution results become public, validated report evidence.
"""
from copy import deepcopy
from dataclasses import replace
import inspect
import json

import numpy as np
import pytest

from recursive_integrity_toolkit.metrics import resampling
from recursive_integrity_toolkit.models import (
    CalculationScope, CapabilityKey, RecordKey, RepresentationDescriptor,
    ScenarioParameters, ValidationMessage, ValidationSeverity,
)
from recursive_integrity_toolkit.reports import assembly
from recursive_integrity_toolkit.result import CanonicalReport

from test_PR012_evidence_classes import (
    phase4_step3_bundle, phase4_step3_distribution, phase4_step3_run,
)
from test_PR013_report_schema import phase4_step2_schema_validator


CLOSED = 'closed_resampling'
REOPENED = 'reopened_resampling'


def declaration(models=(CLOSED, REOPENED), *, initial=(('a', .5), ('b', .5)),
                external=(('a', .25), ('b', .75)), weight=.5,
                n=4, horizon=3, replicates=2):
    scenarios = tuple(ScenarioParameters(model, n, horizon, replicates, initial,
        external if model == REOPENED else None, weight if model == REOPENED else None)
        for model in models)
    return resampling.ScenarioExperimentRequest(scenarios=scenarios,
        scope=CalculationScope(('scenario-v1',), (), (),
            'explicit_scenario_probability_vector', 'scenario-report'),
        representation=RepresentationDescriptor('category', 'topic_field', 'v1',
            'literal_field_value', field_name='topic'),
        state_semantics='Explicit synthetic categories with common meaning', seed=29)


def execution(models=(CLOSED, REOPENED), **kwargs):
    return resampling.run_scenario_experiment(declaration(models, **kwargs))


def run_metadata(seed=None):
    run = phase4_step3_run()
    run['report_schema_version'] = '1.3'
    run['random_seed'] = seed
    if seed is not None:
        del run['null_reasons']['random_seed']
    return run


@pytest.fixture
def bundle(tmp_path):
    return phase4_step3_bundle(tmp_path)


@pytest.fixture(scope='module')
def validator(schema_root):
    return phase4_step2_schema_validator(schema_root)


def assembled(bundle, result, **kwargs):
    return assembly.assemble_report(bundle, run=run_metadata(result.request.seed),
        scenario_experiment=result, **kwargs)


def event_ids(events):
    return [(row['replicate_index'], row['step'], row['state_id']) for row in events]


def probabilities(rows):
    return {row['state_id']: row['probability'] for row in rows}


def forbid_numerical_dispatch(monkeypatch):
    def forbidden(*_args, **_kwargs):
        raise AssertionError('A supplied-evidence adapter dispatched numerical work')
    for name, function in tuple(vars(resampling).items()):
        if inspect.isfunction(function) and function.__module__ == resampling.__name__:
            monkeypatch.setattr(resampling, name, forbidden)
    for name, function in tuple(vars(assembly).items()):
        if inspect.isfunction(function) and function.__module__.startswith(
                'recursive_integrity_toolkit.metrics'):
            monkeypatch.setattr(assembly, name, forbidden)
    for name in ('Generator', 'PCG64', 'default_rng'):
        monkeypatch.setattr(np.random, name, forbidden)


@pytest.mark.parametrize('models', [(CLOSED,), (REOPENED,),
    (CLOSED, REOPENED), (REOPENED, CLOSED)])
def test_selected_scenarios_have_distinct_public_simulation_envelopes(bundle, validator, models):
    result = execution(models)
    report = assembled(bundle, result).to_dict()
    validator.validate(report)
    assert report['run']['report_schema_version'] == '1.3'
    expected = {'closed_resampling' if model == CLOSED else 'external_reopening' for model in models}
    assert set(report['simulations']) == expected
    for model, wire in ((CLOSED, 'closed_resampling'), (REOPENED, 'external_reopening')):
        if model not in models:
            continue
        value = report['simulations'][wire]
        assert value['model'] == model
        assert value['method'] == 'sampled_path'
        assert value['evidence_class'] == 'simulation' and value['status'] == 'experimental'
        assert value['trace_ids'] == ['T1' if model == CLOSED else 'T5']
        assert value['state_semantics'] == result.request.state_semantics
        assert value['scope']['dataset_versions'] == ['scenario-v1']
        assert value['scope']['record_count'] == 0
        assert value['parameters']['random_seed'] == 29
        assert value['parameters']['scenario_schedule'] == 'reset_same_seed_per_model'
        assert value['parameters']['sampler_algorithm'] == 'sequential_binomial_complement_v1'
        assert value['assumption_table'] and value['limitations']
        assert wire not in report['observed_facts'] and wire not in report['derived_metrics']
    if CLOSED in models:
        closed = report['simulations']['closed_resampling']
        baseline = closed['analytic_baseline']
        assert baseline['method'] == 'analytic_expectation'
        assert baseline['baseline_basis'] == 'closed_sampled_effective_distribution'
        assert baseline['expected_diversity'] == pytest.approx([.5, .375, .28125, .2109375])
        for field in ('random_seed', 'simulation_replicates', 'rng_name', 'numpy_version'):
            assert baseline['parameters'][field] is None
        assert 'sampled_paths' not in baseline
    if REOPENED in models:
        reopened = report['simulations']['external_reopening']
        assert ('scenario_comparison' in reopened) == (CLOSED in models)
        assert 'expected_diversity' not in reopened and 'analytic_baseline' not in reopened
        assert reopened['parameters']['reopening_weight'] == .5
        assert probabilities(reopened['external_input_distribution']) == {'a': .25, 'b': .75}


def test_unsupplied_execution_remains_empty_and_supplied_execution_is_honest(bundle, validator):
    empty = assembly.assemble_report(bundle, run=run_metadata()).to_dict()
    validator.validate(empty)
    assert empty['simulations'] == {}
    assert empty['capabilities']['intervention_simulation']['execution_status'] == 'not_requested'
    result = assembled(bundle, execution((REOPENED,))).to_dict()
    capability = result['capabilities']['intervention_simulation']
    assert capability['execution_status'] == 'completed'
    assert capability['status'] == empty['capabilities']['intervention_simulation']['status']
    assert capability['execution_scope']
    unavailable = [row for row in result['unavailable_conclusions']
        if row['conclusion'] == 'empirical_intervention_effect']
    assert len(unavailable) == 1
    assert unavailable[0]['status'] == 'unavailable'
    assert 'empirical' in json.dumps(unavailable[0]).lower()
    assert 'scenario' in json.dumps(unavailable[0]).lower() or 'simulat' in json.dumps(unavailable[0]).lower()


def test_assembly_validation_and_rendering_use_only_supplied_evidence(bundle, validator, monkeypatch):
    from recursive_integrity_toolkit.reports.json_report import render_json
    from recursive_integrity_toolkit.reports.markdown_report import render_markdown

    result = execution()
    before = repr(result)
    forbid_numerical_dispatch(monkeypatch)
    report = assembled(bundle, result)
    validator.validate(report.to_dict())
    CanonicalReport.from_dict(report.to_dict())
    view = assembly.privacy_view(report, mode='standard')
    assert json.loads(render_json(view)) == view.to_dict()
    assert 'simulation' in render_markdown(view).lower()
    assert repr(result) == before


def test_baseline_uses_corrected_closed_start_and_preserves_original_input(bundle, validator):
    supplied = (('b', .5), ('a', .5 + 4e-13))
    result = execution(initial=supplied)
    payload = assembled(bundle, result).to_dict()
    validator.validate(payload)
    closed = payload['simulations']['closed_resampling']
    normalized = closed['input_normalization']
    assert normalized['correction_applied'] is True
    assert probabilities(normalized['supplied_distribution']) == dict(supplied)
    baseline = closed['analytic_baseline']
    assert baseline['input_normalization']['supplied_distribution'] == normalized['effective_distribution']
    assert baseline['input_normalization']['correction_applied'] is False
    assert baseline['initial_gini_simpson_diversity'] == closed['sampled_paths'][0]['generations'][0]['gini_simpson_diversity']
    assert result.request.scenarios[0].state_distribution == supplied


def test_float_diversity_validation_preserves_the_kernel_multiplication_rule(bundle, validator):
    # On this ordinary finite input p*p and p**2 differ by one float unit.
    # Report admission must not reject a genuine result by changing its formula.
    initial = (('a', 0.9284608330919648), ('b', 0.07153916690803519))
    result = execution((CLOSED,), initial=initial)
    payload = assembled(bundle, result).to_dict()
    validator.validate(payload)
    closed = payload['simulations']['closed_resampling']
    assert closed['analytic_baseline']['initial_gini_simpson_diversity'] == result.closed_analytic_baseline.initial_gini_simpson_diversity
    assert closed['sampled_paths'][0]['generations'][0]['gini_simpson_diversity'] == result.selected_results[0].sampled_paths[0].generations[0].gini_simpson_diversity


@pytest.fixture
def recurrent(bundle, monkeypatch):
    # Each reopened draw is possible under lambda=.5. State b enters twice and
    # disappears twice; state identity alone is not an event uniqueness key.
    draws = iter(((2, 0),) * 4 + ((1, 1), (2, 0), (1, 1), (2, 0)))
    with monkeypatch.context() as patch:
        patch.setattr(resampling, '_sample_counts', lambda *_args: next(draws))
        result = execution(initial=(('a', 1.), ('b', 0.)),
            external=(('a', .5), ('b', .5)), n=2, horizon=4, replicates=1)
    return result, assembled(bundle, result).to_dict()


def test_recurrent_events_sources_and_comparison_have_complete_composite_identity(recurrent, validator):
    _, payload = recurrent
    validator.validate(payload)
    CanonicalReport.from_dict(payload)
    value = payload['simulations']['external_reopening']
    assert event_ids(value['state_reentry_events']) == [(0, 1, 'b'), (0, 3, 'b')]
    assert event_ids(value['extinction_events']) == [(0, 2, 'b'), (0, 4, 'b')]
    assert payload['simulations']['closed_resampling']['extinction_events'] == []
    assert [(row['replicate_index'], row['step']) for row in value['mixed_sources']] == [(0, step) for step in range(1, 5)]
    sources = value['mixed_sources']
    assert [probabilities(row['input_normalization']['effective_distribution']) for row in sources] == [
        {'a': .75, 'b': .25}, {'a': .5, 'b': .5},
        {'a': .75, 'b': .25}, {'a': .5, 'b': .5}]
    assert [row['possible_reentry_states'] for row in sources] == [['b'], [], ['b'], []]
    assert value['support_trajectory'] == [{'replicate_index': 0, 'support_sizes': [1, 2, 1, 2, 1]}]
    assert value['diversity_trajectory'] == [{'replicate_index': 0, 'gini_simpson_diversities': [0., .5, 0., .5, 0.]}]
    comparison = value['scenario_comparison']
    assert comparison['difference_direction'] == 'reopened_minus_closed'
    assert [(row['replicate_index'], row['step']) for row in comparison['rows']] == [(0, step) for step in range(5)]
    assert [row['support_size_difference'] for row in comparison['rows']] == [0, 1, 0, 1, 0]
    assert [row['diversity_difference'] for row in comparison['rows']] == [0., .5, 0., .5, 0.]


def test_closed_extinction_coverage_is_complete_across_replicates(bundle, validator):
    result = execution((CLOSED,), n=1, horizon=2, replicates=2)
    payload = assembled(bundle, result).to_dict()
    validator.validate(payload)
    events = payload['simulations']['closed_resampling']['extinction_events']
    assert [(row['replicate_index'], row['step']) for row in events] == [(0, 1), (1, 1)]
    # Exactly one of two initially present states disappears in each first draw.
    assert len(events) == 2
    events.pop()
    with pytest.raises(ValueError):
        CanonicalReport.from_dict(payload)


@pytest.mark.parametrize('case', [
    'missing_reentry', 'missing_extinction', 'duplicate_event', 'invented_event',
    'event_step_zero', 'missing_source', 'duplicate_source', 'stale_source',
    'false_possible_reentry', 'wrong_counts', 'wrong_frequencies', 'wrong_support',
    'wrong_diversity', 'wrong_support_trajectory', 'wrong_diversity_trajectory',
    'missing_comparison_row', 'wrong_comparison_values', 'wrong_comparison_sign',
    'wrong_initial_reachability', 'wrong_external_parameter', 'wrong_seed',
    'wrong_baseline', 'wrong_baseline_basis', 'hidden_input_correction',
    'external_normalization_total', 'mixed_normalization_divisor',
])
def test_public_contract_rejects_incomplete_or_misbound_simulation_evidence(recurrent, case):
    _, original = recurrent
    payload = deepcopy(original)
    value = payload['simulations']['external_reopening']
    if case == 'missing_reentry':
        value['state_reentry_events'].pop()
    elif case == 'missing_extinction':
        value['extinction_events'].pop()
    elif case == 'duplicate_event':
        value['state_reentry_events'].append(deepcopy(value['state_reentry_events'][0]))
    elif case == 'invented_event':
        value['state_reentry_events'].append({'replicate_index': 0, 'step': 2, 'state_id': 'a'})
    elif case == 'event_step_zero':
        value['state_reentry_events'][0]['step'] = 0
    elif case == 'missing_source':
        value['mixed_sources'].pop()
    elif case == 'duplicate_source':
        value['mixed_sources'][1] = deepcopy(value['mixed_sources'][0])
    elif case == 'stale_source':
        value['mixed_sources'][1]['input_normalization'] = deepcopy(value['mixed_sources'][0]['input_normalization'])
    elif case == 'false_possible_reentry':
        value['mixed_sources'][1]['possible_reentry_states'] = ['b']
    elif case == 'wrong_counts':
        value['sampled_paths'][0]['generations'][1]['state_counts'] = [2, 1]
    elif case == 'wrong_frequencies':
        value['sampled_paths'][0]['generations'][1]['state_frequencies'] = [.75, .25]
    elif case == 'wrong_support':
        value['sampled_paths'][0]['generations'][1]['support'] = ['a']
    elif case == 'wrong_diversity':
        value['sampled_paths'][0]['generations'][1]['gini_simpson_diversity'] = .25
    elif case == 'wrong_support_trajectory':
        value['support_trajectory'][0]['support_sizes'][1] = 1
    elif case == 'wrong_diversity_trajectory':
        value['diversity_trajectory'][0]['gini_simpson_diversities'][1] = .25
    elif case == 'missing_comparison_row':
        value['scenario_comparison']['rows'].pop()
    elif case == 'wrong_comparison_values':
        value['scenario_comparison']['rows'][1].update(closed_support_size=2,
            reopened_support_size=1, support_size_difference=-1)
    elif case == 'wrong_comparison_sign':
        value['scenario_comparison']['rows'][1]['diversity_difference'] = -.5
    elif case == 'wrong_initial_reachability':
        value['scenario_comparison']['initial_reachability'][1]['possible_reentry_states'] = []
    elif case == 'wrong_external_parameter':
        value['parameters']['external_input_distribution'][0]['probability'] = .4
    elif case == 'wrong_seed':
        value['parameters']['random_seed'] += 1
    elif case == 'wrong_baseline':
        payload['simulations']['closed_resampling']['analytic_baseline']['expected_diversity'][1] = .5
    elif case == 'wrong_baseline_basis':
        payload['simulations']['closed_resampling']['analytic_baseline']['baseline_basis'] = 'uncorrected_caller_distribution'
    elif case == 'hidden_input_correction':
        value['input_normalization']['probability_corrections'][0]['correction'] = .01
    elif case == 'external_normalization_total':
        value['external_input_normalization']['supplied_probability_total'] = .9
    elif case == 'mixed_normalization_divisor':
        value['mixed_sources'][0]['input_normalization']['normalization_divisor'] = .5
    with pytest.raises(ValueError):
        CanonicalReport.from_dict(payload)


@pytest.mark.parametrize('field,value', [('method', 'analytic_expectation'),
    ('trace_ids', ['T1']), ('expected_diversity', [0., 0., 0., 0., 0.]),
    ('contraction_factor', .5), ('evidence_class', 'derived_metric'), ('status', 'available')])
def test_reopened_wire_cannot_claim_closed_contraction_or_empirical_evidence(recurrent, validator, field, value):
    _, original = recurrent
    payload = deepcopy(original)
    payload['simulations']['external_reopening'][field] = value
    assert not validator.is_valid(payload)
    with pytest.raises(ValueError):
        CanonicalReport.from_dict(payload)


@pytest.mark.parametrize('case', ['request_seed', 'request_distribution', 'request_size',
    'request_scope', 'request_representation', 'missing_selected_model', 'duplicate_selected_model',
    'model_seed', 'model_horizon', 'model_replicates', 'model_method', 'model_assumptions',
    'external_input', 'mixture_formula', 'trajectory_formula', 'missing_baseline',
    'baseline_seed', 'missing_comparison', 'comparison_values', 'event_coverage'])
def test_typed_handoff_is_revalidated_against_the_explicit_request(bundle, recurrent, case, monkeypatch):
    original, _ = recurrent
    closed, reopened = original.selected_results
    if case == 'request_seed':
        bad = replace(original, request=replace(original.request, seed=30))
    elif case == 'request_distribution':
        scenarios = tuple(replace(row, state_distribution=(('a', .5), ('b', .5))) for row in original.request.scenarios)
        bad = replace(original, request=replace(original.request, scenarios=scenarios))
    elif case == 'request_size':
        scenarios = tuple(replace(row, resample_size=3) for row in original.request.scenarios)
        bad = replace(original, request=replace(original.request, scenarios=scenarios))
    elif case == 'request_scope':
        scope = replace(original.request.scope, scope_id='different-scenario')
        bad = replace(original, request=replace(original.request, scope=scope))
    elif case == 'request_representation':
        representation = replace(original.request.representation, representation_version='different-meaning')
        bad = replace(original, request=replace(original.request, representation=representation))
    elif case == 'missing_selected_model':
        bad = replace(original, selected_results=(closed,))
    elif case == 'duplicate_selected_model':
        bad = replace(original, selected_results=(closed, closed))
    elif case.startswith('model_'):
        field, value = {'model_seed': ('random_seed', 30), 'model_horizon': ('simulation_horizon', 5),
            'model_replicates': ('simulation_replicates', 2), 'model_method': ('method', 'analytic_expectation'),
            'model_assumptions': ('assumptions', ('Independent external quality proven.',))}[case]
        bad = replace(original, selected_results=(closed, replace(reopened, **{field: value})))
    elif case == 'external_input':
        bad_input = replace(reopened.external_inputs, supplied_distribution=(('a', .75), ('b', .25)))
        bad = replace(original, selected_results=(closed, replace(reopened, external_inputs=bad_input)))
    elif case == 'mixture_formula':
        metadata = replace(reopened.mixture_metadata, formula_id='F-015')
        bad = replace(original, selected_results=(closed, replace(reopened, mixture_metadata=metadata)))
    elif case == 'trajectory_formula':
        metadata = reopened.trajectory_metadata[:-1] + (replace(reopened.trajectory_metadata[-1], formula_id='F-015'),)
        bad = replace(original, selected_results=(closed, replace(reopened, trajectory_metadata=metadata)))
    elif case == 'missing_baseline':
        bad = replace(original, closed_analytic_baseline=None)
    elif case == 'baseline_seed':
        bad = replace(original, closed_analytic_baseline=replace(original.closed_analytic_baseline, random_seed=29))
    elif case == 'missing_comparison':
        bad = replace(original, comparison=None)
    elif case == 'comparison_values':
        row = replace(original.comparison.rows[1], support_size_difference=-1)
        bad = replace(original, comparison=replace(original.comparison,
            rows=original.comparison.rows[:1] + (row,) + original.comparison.rows[2:]))
    else:
        bad = replace(original, selected_results=(closed, replace(reopened, state_reentry_events=())))
    forbid_numerical_dispatch(monkeypatch)
    with pytest.raises(ValueError):
        assembled(bundle, bad)


@pytest.mark.parametrize('weight', [0., 1.])
def test_endpoint_sources_retain_effective_basis_without_second_normalization(bundle, validator, weight):
    initial = (('a', .1), ('b', .4), ('c', .5000000000004))
    external = (('a', .1), ('b', .1), ('c', .7999999999996))
    result = execution(initial=initial, external=external, weight=weight)
    payload = assembled(bundle, result).to_dict()
    validator.validate(payload)
    value = payload['simulations']['external_reopening']
    for row in value['mixed_sources']:
        normalization = row['input_normalization']
        assert normalization['correction_applied'] is False
        assert normalization['supplied_distribution'] == normalization['effective_distribution']
        if weight == 1.:
            assert row['input_basis'] == 'effective_external_distribution'
            assert normalization['effective_distribution'] == value['external_input_distribution']
        else:
            assert row['input_basis'] == ('effective_internal_distribution' if row['step'] == 1
                else 'sampled_integer_counts_over_resample_size')
    if weight == 0.:
        assert value['sampled_paths'] == payload['simulations']['closed_resampling']['sampled_paths']
        assert value['state_reentry_events'] == []


def test_partial_mixture_discloses_its_own_roundoff_correction(bundle, validator):
    result = execution((REOPENED,), initial=(('a', .1), ('b', .4), ('c', .5000000000004)),
        external=(('a', .1), ('b', .1), ('c', .7999999999996)), weight=.3, horizon=1)
    payload = assembled(bundle, result).to_dict()
    validator.validate(payload)
    value = payload['simulations']['external_reopening']
    assert value['input_normalization']['correction_applied'] is True
    assert value['external_input_normalization']['correction_applied'] is True
    first = value['mixed_sources'][0]
    assert first['input_basis'] == 'computed_external_mixture'
    correction = first['input_normalization']
    assert correction['supplied_probability_total'] == .9999999999999998
    assert correction['correction_applied'] is True
    assert correction['normalization_divisor'] == correction['supplied_probability_total']
    assert correction['supplied_distribution'] != correction['effective_distribution']
    assert any(row['correction'] != 0 for row in correction['probability_corrections'])


def test_horizon_zero_has_declared_possibilities_without_sources_or_events(bundle, validator):
    result = execution(initial=(('a', 1.), ('b', 0.)), external=(('a', 0.), ('b', 1.)),
        weight=5e-324, horizon=0, replicates=2)
    payload = assembled(bundle, result).to_dict()
    validator.validate(payload)
    value = payload['simulations']['external_reopening']
    assert value['mixed_sources'] == value['state_reentry_events'] == value['extinction_events'] == []
    assert len(value['sampled_paths']) == 2
    assert all(len(path['generations']) == 1 and path['generations'][0]['state_counts'] is None
        for path in value['sampled_paths'])
    comparison = value['scenario_comparison']
    assert len(comparison['rows']) == 2
    assert comparison['initial_reachability'][1]['reachable_states'] == ['a', 'b']
    assert comparison['initial_reachability'][1]['possible_reentry_states'] == ['b']
    assert all(row['timing'] == 'before_first_draw' for row in comparison['initial_reachability'])


@pytest.mark.parametrize('model', [CLOSED, REOPENED])
def test_coherently_rewritten_sample_cannot_create_a_state_with_zero_source_probability(bundle, model):
    result = execution((model,), initial=(('a', 1.), ('b', 0.)),
        external=(('a', 1.), ('b', 0.)), n=2, horizon=1, replicates=1)
    payload = assembled(bundle, result).to_dict()
    wire = 'closed_resampling' if model == CLOSED else 'external_reopening'
    value = payload['simulations'][wire]
    value['sampled_paths'][0]['generations'][1].update(state_counts=[1, 1],
        state_frequencies=[.5, .5], support=['a', 'b'], support_size=2,
        gini_simpson_diversity=.5)
    if model == CLOSED:
        value['support_trajectories'][0]['support_sizes'][1] = 2
    else:
        value['support_trajectory'][0]['support_sizes'][1] = 2
        value['diversity_trajectory'][0]['gini_simpson_diversities'][1] = .5
    with pytest.raises(ValueError):
        CanonicalReport.from_dict(payload)


@pytest.mark.parametrize('target', ['closed_resampling', 'external_reopening', 'analytic_baseline'])
@pytest.mark.parametrize('denominator', [99, None])
def test_scenario_envelope_denominator_stays_bound_to_sample_size(bundle, target, denominator):
    payload = assembled(bundle, execution(n=4)).to_dict()
    envelope = (payload['simulations']['closed_resampling']['analytic_baseline']
        if target == 'analytic_baseline' else payload['simulations'][target])
    envelope['denominator'] = denominator
    envelope['denominator_reason'] = 'Caller claims denominator unavailable.' if denominator is None else None
    with pytest.raises(ValueError):
        CanonicalReport.from_dict(payload)


@pytest.mark.parametrize('baseline', [False, True])
def test_experiment_closed_model_identity_is_fixed_for_sample_and_baseline(bundle, baseline):
    payload = assembled(bundle, execution((CLOSED,))).to_dict()
    closed = payload['simulations']['closed_resampling']
    target = closed['analytic_baseline'] if baseline else closed
    target['model_version'] = 'invented_categorical_model_v99'
    with pytest.raises(ValueError):
        CanonicalReport.from_dict(payload)


def test_standalone_reopened_scope_cannot_claim_multiple_dataset_versions(bundle):
    payload = assembled(bundle, execution((REOPENED,))).to_dict()
    payload['simulations']['external_reopening']['scope']['dataset_versions'] = ['scenario-v1', 'extra']
    with pytest.raises(ValueError):
        CanonicalReport.from_dict(payload)


@pytest.mark.parametrize('legacy_argument', ['expected_diversity', 'resampling'])
def test_experiment_rejects_competing_legacy_closed_slot(bundle, legacy_argument):
    result = execution()
    legacy = result.closed_analytic_baseline if legacy_argument == 'expected_diversity' else result.selected_results[0]
    with pytest.raises(ValueError):
        assembled(bundle, result, **{legacy_argument: legacy})


def test_reopened_only_accepts_separately_supplied_legacy_closed_result_without_comparison(bundle, validator):
    reopened = execution((REOPENED,))
    legacy = execution((CLOSED,)).selected_results[0]
    payload = assembled(bundle, reopened, resampling=legacy).to_dict()
    validator.validate(payload)
    closed = payload['simulations']['closed_resampling']
    assert 'analytic_baseline' not in closed and 'state_semantics' not in closed
    assert 'scenario_comparison' not in payload['simulations']['external_reopening']


def test_legacy_closed_and_tail_still_prohibit_external_inputs(bundle, validator):
    from recursive_integrity_toolkit.metrics.tail import one_step_extinction_probability

    result = execution((CLOSED,))
    scope = CalculationScope(('v1',), (RecordKey('v1', 'r0'),), (), 'explicit_record', 'tail-case')
    tail = one_step_extinction_probability(.25, resample_size=4, state_id='b', scope=scope,
        representation=result.request.representation)
    payload = assembly.assemble_report(bundle, run=run_metadata(29),
        resampling=result.selected_results[0], extinction=(tail,)).to_dict()
    validator.validate(payload)
    assert 'analytic_baseline' not in payload['simulations']['closed_resampling']
    for model in ('closed_resampling', 'tail_extinction'):
        for field, value in (('reopening_weight', .5),
                ('external_input_distribution', [{'state_id': 'b', 'probability': 1.}])):
            bad = deepcopy(payload)
            bad['simulations'][model]['parameters'][field] = value
            assert not validator.is_valid(bad)
            with pytest.raises(ValueError):
                CanonicalReport.from_dict(bad)


def test_scenario_failure_preserves_independent_completed_audit_evidence(bundle):
    distribution = phase4_step3_distribution(bundle)
    failure = assembly.FamilyFailure(CapabilityKey.INTERVENTION_SIMULATION, (
        ValidationMessage('E_CONFIG_INVALID', ValidationSeverity.ERROR,
            'Explicit scenario request exceeds its resource limit.', field='simulation'),))
    report = assembly.assemble_report(bundle, run=run_metadata(), distributions=(distribution,),
        family_errors=(failure,)).to_dict()
    assert report['simulations'] == {}
    assert report['capabilities']['intervention_simulation']['execution_status'] == 'failed'
    assert report['capabilities']['intervention_simulation']['execution_reason_codes']
    assert report['derived_metrics']['diversity']['by_version']['v1']['gini_simpson_diversity']['value'] == .625
    assert report['capabilities']['content_diagnostics']['execution_status'] == 'completed'
    assert report['run']['run_status'] == 'partial'
    unavailable = [row for row in report['unavailable_conclusions']
        if row['conclusion'] == 'empirical_intervention_effect']
    assert len(unavailable) == 1 and unavailable[0]['status'] == 'unavailable'
