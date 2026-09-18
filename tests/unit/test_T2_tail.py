"""T2 Step 7: independent tail and F-014 oracles; no random sampler.

Sources: Definitions 10; Validation 15; approved P3-D06/P3-D07.
Additional boundary, metamorphic and hostile-input cases are test design.
"""
from dataclasses import replace
from decimal import Decimal, localcontext
from fractions import Fraction
import json
import math
import pytest
from recursive_integrity_toolkit.config import RepresentationConfig
from recursive_integrity_toolkit.errors import CanonicalValidationError
from recursive_integrity_toolkit.io.normalization import normalize_row
from recursive_integrity_toolkit.metrics.diversity import (
    calculate_state_distribution, distribution_from_counts, distribution_from_probabilities,
)
from recursive_integrity_toolkit.metrics.tail import select_tail, one_step_extinction_probability
from recursive_integrity_toolkit.models import (
    CalculationScope, CalculationStatus, CalculationReason, CalculationEvidenceClass,
    RecordKey, RepresentationDescriptor, TailSelectionOptions, WeightingOptions,
)
from recursive_integrity_toolkit.representations.field import assign_field_states


def descriptor():
    return RepresentationDescriptor('topic','topic_field','test-v1','literal_field_value',field_name='topic',missing_value_policy='exclude')


def scope(n=8):
    return CalculationScope(('v1',),tuple(RecordKey('v1',str(i)) for i in range(n)),(),'included_representation_records','T2-test')


def dist(counts=None):
    counts={'cat':3,'dog':2,'bird':1,'fish':1,'refund':1} if counts is None else counts
    return distribution_from_counts(counts,scope=scope(sum(counts.values())),representation=descriptor())


def represented(labels):
    rows=tuple(normalize_row(dict(dataset_version='v1',record_id=str(i),content='synthetic',topic=v),kind='records') for i,v in enumerate(labels))
    r=assign_field_states(rows,dataset_versions=('v1',),scope_id='T2-test',config=RepresentationConfig('topic','topic_field','topic','test-v1','exclude'))
    return calculate_state_distribution(r).unweighted


def scenario(p,n=8,**changes):
    args=dict(resample_size=n,state_id='a',scope=scope(),representation=descriptor());args.update(changes)
    return one_step_extinction_probability(p,**args)


def value(result):
    return result.one_step_extinction_probability.value


def test_T2_tail_owner_and_placeholder(owner_checker,repo_root):
    owner_checker('metrics/tail.py','T2')
    text=(repo_root/'src/recursive_integrity_toolkit/metrics/tail.py').read_text()
    assert 'Phase 3 Step 7' in text
    assert all('def '+name+'(' not in text for name in ('simulate','reopen','risk_score','tail_fragility_signal'))


@pytest.mark.parametrize('rule,args,expected',[
    ('singleton_count',{},('bird','fish','refund')),
    ('count_at_or_below',{'count_threshold':0},()),
    ('count_at_or_below',{'count_threshold':1},('bird','fish','refund')),
    ('count_at_or_below',{'count_threshold':2},('bird','dog','fish','refund')),
    ('count_at_or_below',{'count_threshold':8},('bird','cat','dog','fish','refund')),
    ('frequency_at_or_below',{'frequency_threshold':0},()),
    ('frequency_at_or_below',{'frequency_threshold':.125},('bird','fish','refund')),
    ('frequency_at_or_below',{'frequency_threshold':math.nextafter(.125,0)},()),
    ('frequency_at_or_below',{'frequency_threshold':.25},('bird','dog','fish','refund')),
    ('frequency_at_or_below',{'frequency_threshold':1},('bird','cat','dog','fish','refund')),
    ('state_list',{'state_ids':('refund','cat')},('cat','refund')),
])
def test_T2_selected_rule_thresholds(rule,args,expected):
    d=dist();before=repr(d)
    result=select_tail(d,options=TailSelectionOptions(rule,**args))
    assert result.tail_membership==expected
    assert result.tail_support_size.value==len(expected)
    counts={s.state_id:s.state_count for s in d.states}
    assert result.tail_record_share.value==sum(counts[s] for s in expected)/8
    assert result.denominator==8 and result.status is CalculationStatus.AVAILABLE
    assert repr(d)==before


def test_T2_hero_rarity_ties_and_canonical_membership():
    result=select_tail(dist(),options=TailSelectionOptions('singleton_count'))
    assert tuple(e.state_id for e in result.rarity_ranking)==('bird','fish','refund','dog','cat')
    assert tuple(e.rarity_rank for e in result.rarity_ranking)==(1,2,3,4,5)
    assert tuple(e.in_tail for e in result.rarity_ranking)==(True,True,True,False,False)
    assert result.tail_record_share.value==3/8


def test_T2_unicode_empty_literal_states_and_zero_support():
    d=dist({'':1,' ':1,'A':1,'a':1,'é':1,'e\u0301':1,'unknown':1,'absent':0})
    result=select_tail(d,options=TailSelectionOptions('frequency_at_or_below',frequency_threshold=1))
    assert result.tail_membership==tuple(sorted(('', ' ', 'A','a','é','e\u0301','unknown')))
    assert len(result.rarity_ranking)==7 and result.tail_record_share.value==1


@pytest.mark.parametrize('state',['absent','zero'])
def test_T2_list_never_invents_absent_states(state):
    with pytest.raises(CanonicalValidationError):
        select_tail(dist({'a':1,'zero':0}),options=TailSelectionOptions('state_list',state_ids=(state,)))


@pytest.mark.parametrize('labels,reason',[((),CalculationReason.EMPTY_SCOPE),((None,None),CalculationReason.ALL_EXCLUDED)])
def test_T2_unavailable_scope_is_not_empty_tail(labels,reason):
    result=select_tail(represented(labels),options=TailSelectionOptions('singleton_count'))
    assert result.status is CalculationStatus.UNAVAILABLE and result.reason_codes==(reason,)
    assert result.tail_record_share.value is None and result.tail_support_size.value is None
    assert result.denominator is None and result.rarity_ranking==()


def test_T2_valid_empty_tail_and_singleton_dataset():
    a=select_tail(dist({'a':2}),options=TailSelectionOptions('singleton_count'))
    assert a.tail_record_share.value==0 and a.tail_support_size.value==0 and a.status is CalculationStatus.AVAILABLE
    b=select_tail(dist({'a':1}),options=TailSelectionOptions('singleton_count'))
    assert b.tail_record_share.value==1 and b.tail_support_size.value==1


def test_T2_exclusion_denominator_stays_representation_scoped():
    d=represented(('a',None,'b',None,'a'))
    result=select_tail(d,options=TailSelectionOptions('singleton_count'))
    assert result.denominator==3 and result.tail_record_share.value==1/3
    assert len(result.scope.excluded_record_keys)==2


@pytest.mark.parametrize('changes',[
    {'rule':'bottom_frequency_quantile'},{'rule':'weighted_tail'},{'rule':None},
    {'count_threshold':True},{'count_threshold':-1},{'count_threshold':1.5},
    {'state_ids':['a']},{'state_ids':('a','a')},{'state_ids':('\ud800',)},
    {'frequency_threshold':float('nan')},{'frequency_threshold':-1},{'frequency_threshold':2},
])
def test_T2_revalidates_forged_options(changes):
    opts=TailSelectionOptions('count_at_or_below',count_threshold=1)
    for key,v in changes.items():object.__setattr__(opts,key,v)
    with pytest.raises(CanonicalValidationError):select_tail(dist(),options=opts)


@pytest.mark.parametrize('obj',[None,{},(),42,'singleton_count'])
def test_T2_rejects_wrong_option_type(obj):
    with pytest.raises(CanonicalValidationError):select_tail(dist(),options=obj)


@pytest.mark.parametrize('changes',[
    {'analyzed_record_count':True},{'analyzed_record_count':7},{'frequency_denominator':8.0},
    {'frequency_denominator':0},{'status':CalculationStatus.UNAVAILABLE},{'reason_codes':(CalculationReason.EMPTY_SCOPE,)},
    {'denominator_basis':'other'},{'count_metadata':None},{'frequency_metadata':None},
    {'support':('cat',)},{'states':()},{'states':[]},{'input_basis':'weighted_record_mass'},
    {'weighting':WeightingOptions('weighted','weight')},
])
def test_T2_rejects_inconsistent_distribution(changes):
    with pytest.raises(CanonicalValidationError):select_tail(replace(dist(),**changes),options=TailSelectionOptions('singleton_count'))


@pytest.mark.parametrize('changes',[{'state_count':True},{'state_count':-1},{'state_frequency':float('nan')},
    {'state_frequency':.99},{'state_mass':1},{'state_id':None},{'state_id':'\ud800'}])
def test_T2_rejects_forged_state_entries(changes):
    d=dist();rows=(replace(d.states[0],**changes),)+d.states[1:]
    with pytest.raises(CanonicalValidationError):select_tail(replace(d,states=rows),options=TailSelectionOptions('singleton_count'))


def test_T2_rejects_duplicate_rows_and_probability_only_record_claim():
    d=dist()
    with pytest.raises(CanonicalValidationError):select_tail(replace(d,states=d.states+(d.states[0],)),options=TailSelectionOptions('singleton_count'))
    p=distribution_from_probabilities({'a':.5,'b':.5},scope=scope(),representation=descriptor())
    with pytest.raises(CanonicalValidationError):select_tail(p,options=TailSelectionOptions('frequency_at_or_below',frequency_threshold=.5))


def test_T2_permutation_invariance_and_detachment():
    d=dist();p=replace(d,states=tuple(reversed(d.states)),support=tuple(reversed(d.support)))
    a=select_tail(d,options=TailSelectionOptions('state_list',state_ids=('cat','dog')))
    b=select_tail(p,options=TailSelectionOptions('state_list',state_ids=('dog','cat')))
    assert a==b
    with pytest.raises((AttributeError,TypeError)):a.rarity_ranking[0].rarity_rank=99


def test_T2_frequency_tail_replication_invariance():
    a=select_tail(dist(),options=TailSelectionOptions('frequency_at_or_below',frequency_threshold=.25))
    b=select_tail(dist({'cat':6,'dog':4,'bird':2,'fish':2,'refund':2}),options=TailSelectionOptions('frequency_at_or_below',frequency_threshold=.25))
    assert a.tail_membership==b.tail_membership and a.tail_record_share.value==b.tail_record_share.value


@pytest.mark.parametrize('p,n,expected',[(0,8,'1'),(1,8,'0'),(.5,2,'1/4'),(.25,4,'81/256'),
    (.125,8,'5764801/16777216'),(.25,8,'6561/65536'),(.375,8,'390625/16777216')])
def test_T2_F014_exact_rational_cases(p,n,expected):
    x=scenario(p,n)
    assert value(x)==pytest.approx(float(Fraction(expected)),abs=1e-12,rel=1e-12)
    assert x.numerical_underflow is False


def test_T2_frozen_oracles_and_new_tail_fixture(repo_root):
    p=repo_root/'tests/fixtures/minimal_valid/phase3_tail_cases.json';before=p.read_bytes();data=json.loads(before)
    for case in data['tail_cases']:
        opts=dict(case['options'])
        if 'state_ids' in opts:opts['state_ids']=tuple(opts['state_ids'])
        x=select_tail(dist(case['counts']),options=TailSelectionOptions(**opts))
        assert x.tail_membership==tuple(case['membership'])
        assert x.tail_record_share.value==pytest.approx(float(Fraction(case['share'])),abs=1e-12,rel=1e-12)
    g=repo_root/'tests/golden/phase3_math_cases.json';old=g.read_bytes()
    for case in json.loads(old)['cases']:
        if case['case_id'].startswith('F014'):
            inputs=case['inputs'];expected=case['expected']
            assert value(scenario(float(Fraction(inputs['probability'])),inputs['resample_size']))==pytest.approx(float(Fraction(expected['one_step_extinction_probability'])),abs=1e-12,rel=1e-12)
    assert p.read_bytes()==before and g.read_bytes()==old


@pytest.mark.parametrize('p',[-1,-5e-324,1.000000001,float('nan'),float('inf'),float('-inf'),True,False,None,'0.5',Fraction(1,2),10**1000])
def test_T2_rejects_invalid_probability(p):
    with pytest.raises(CanonicalValidationError):scenario(p)


@pytest.mark.parametrize('n',[0,-1,True,False,None,1.0,.5,'8',float('inf'),10**1000])
def test_T2_rejects_invalid_sample_size(n):
    with pytest.raises(CanonicalValidationError):scenario(.5,n)


@pytest.mark.parametrize('changes',[{'scope':None},{'scope':scope(0)},{'representation':None},{'state_id':None},{'state_id':'\ud800'}])
def test_T2_scenario_requires_scope_and_representation(changes):
    with pytest.raises(CanonicalValidationError):scenario(.5,**changes)


def test_T2_n_one_and_frequency_monotonicity():
    frequencies=(0,5e-324,1e-18,.01,.125,.25,.5,.99,1)
    outputs=[value(scenario(p)) for p in frequencies]
    assert outputs==sorted(outputs,reverse=True) and all(0<=x<=1 for x in outputs)
    for p in frequencies:assert value(scenario(p,1))==pytest.approx(1-p,abs=1e-12,rel=1e-12)


def test_T2_sample_size_monotonicity_and_underflow_disclosure():
    results=[scenario(.25,n) for n in (1,2,8,100,10000)]
    assert [value(x) for x in results]==sorted((value(x) for x in results),reverse=True)
    assert value(results[-1])==0 and results[-1].numerical_underflow
    assert value(scenario(1))==0 and not scenario(1).numerical_underflow


def test_T2_tiny_frequency_avoids_subtraction_cancellation():
    p=1e-18;n=10**18
    with localcontext() as ctx:
        ctx.prec=80
        expected=float((Decimal(1)-Decimal.from_float(p))**n)
    assert value(scenario(p,n))==pytest.approx(expected,abs=1e-12,rel=1e-12)
    assert value(scenario(p,n))<.4


def test_T2_trace_metadata_keeps_observation_and_scenario_separate():
    tail=select_tail(dist(),options=TailSelectionOptions('singleton_count'))
    for m in (tail.ranking_metadata,tail.membership_metadata,tail.tail_support_size.metadata,tail.tail_record_share.metadata):
        assert m.owner_id=='T2' and m.evidence_class is CalculationEvidenceClass.DERIVED_METRIC
        assert m.scope==tail.scope and m.representation==tail.representation and m.unit and m.assumptions and m.limitations
    s=scenario(.125);m=s.one_step_extinction_probability.metadata
    assert m.formula_id=='F-014' and m.evidence_class is CalculationEvidenceClass.SIMULATION
    assert s.method=='analytic_extinction' and s.experimental and s.simulation_horizon==1 and s.resample_size==8
    assert s.random_seed is None and s.input_basis=='supplied_selected_state_marginal'
    for name in ('risk_score','tail_fragility_signal','lineage','reopening_weight','report','sampled_path'):
        assert not hasattr(tail,name) and not hasattr(s,name)


def test_T2_no_side_effects_rng_or_implicit_extinction(monkeypatch,capsys,tmp_path):
    import builtins,socket,random
    from pathlib import Path
    import recursive_integrity_toolkit.metrics.tail as module
    d=dist({'PRIVATE_SENTINEL':1,'b':2});state=random.getstate()
    def blocked(*a,**kw):raise AssertionError('unexpected side effect')
    with monkeypatch.context() as m:
        for name in ('open','eval','exec'):m.setattr(builtins,name,blocked)
        m.setattr(Path,'open',blocked);m.setattr(socket,'create_connection',blocked);m.setattr(socket,'getaddrinfo',blocked)
        m.setattr(random,'random',blocked);m.setattr(random,'seed',blocked)
        s=scenario(.25)
        m.setattr(module,'one_step_extinction_probability',blocked)
        x=select_tail(d,options=TailSelectionOptions('singleton_count'))
    assert state==random.getstate() and capsys.readouterr()==('','') and not list(tmp_path.iterdir())
    assert 'PRIVATE_SENTINEL' not in repr(x) and 'PRIVATE_SENTINEL' not in repr(x.rarity_ranking)


def test_T2_input_hero_does_not_invoke_tail_or_extinction(repo_root,monkeypatch):
    from recursive_integrity_toolkit.models import AuditBundle,InputSource,FileRole
    from recursive_integrity_toolkit.io.validation import validate_bundle
    import recursive_integrity_toolkit.metrics.tail as module
    def blocked(*a,**kw):raise AssertionError('validation invoked T2')
    monkeypatch.setattr(module,'select_tail',blocked);monkeypatch.setattr(module,'one_step_extinction_probability',blocked)
    h=repo_root/'examples/hero'
    roles=(FileRole.RECORDS_PRIMARY,FileRole.RECORDS_COMPARE,FileRole.PROVENANCE_MANIFEST,FileRole.CONFIG,FileRole.VERSION_ORDER)
    names=('records_v1.csv','records_v2.csv','provenance.csv','config.json','version_order.json')
    before={n:(h/n).read_bytes() for n in names}
    x=validate_bundle(AuditBundle(tuple(InputSource(r,h/n) for r,n in zip(roles,names))))
    assert x.observability.maximum_level==4 and not x.has_errors
    assert before=={n:(h/n).read_bytes() for n in names}


def test_T2_enabled_valid_scenario_is_still_input_only(repo_root,monkeypatch):
    from recursive_integrity_toolkit.models import AuditBundle,InputSource,FileRole,ScenarioParameters,CapabilityKey,CapabilityStatus
    from recursive_integrity_toolkit.io.validation import validate_bundle
    import recursive_integrity_toolkit.metrics.tail as module
    def blocked(*a,**kw):raise AssertionError('eligible scenario implicitly executed T2')
    monkeypatch.setattr(module,'select_tail',blocked);monkeypatch.setattr(module,'one_step_extinction_probability',blocked)
    h=repo_root/'examples/hero';config=json.loads((h/'config.json').read_bytes())
    config['simulation']={'enabled':True,'seed':17}
    roles=(FileRole.RECORDS_PRIMARY,FileRole.RECORDS_COMPARE,FileRole.PROVENANCE_MANIFEST,FileRole.VERSION_ORDER)
    names=('records_v1.csv','records_v2.csv','provenance.csv','version_order.json')
    result=validate_bundle(AuditBundle(tuple(InputSource(r,h/n) for r,n in zip(roles,names))),configuration=config,
        scenario_parameters=ScenarioParameters('closed_resampling',resample_size=8,simulation_horizon=1,
            simulation_replicates=1,state_distribution=(('a',.5),('b',.5))))
    cap=result.observability.capabilities[CapabilityKey.INTERVENTION_SIMULATION]
    assert cap.status is CapabilityStatus.EXPERIMENTAL
    assert 'R_SCENARIO_EXECUTION_DEFERRED' in cap.reason_codes and not result.has_errors
