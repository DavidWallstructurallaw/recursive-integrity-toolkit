"""T1 F-003/F-004 and explicit weighted companions, independently verified.

Rational oracles are from approved definitions or authored arithmetic cases.
No sampling, state repair, report or functional-failure inference is tested.
"""
from fractions import Fraction
from itertools import permutations
import pytest
from recursive_integrity_toolkit.config import RepresentationConfig
from recursive_integrity_toolkit.errors import CanonicalValidationError, ErrorCode
from recursive_integrity_toolkit.io.normalization import normalize_row
from recursive_integrity_toolkit.metrics.diversity import calculate_state_distribution, distribution_from_counts, distribution_from_probabilities
from recursive_integrity_toolkit.models import CalculationScope, CalculationEvidenceClass, CalculationStatus, ContentMode, RecordKey, RepresentationDescriptor, WeightingOptions
from recursive_integrity_toolkit.representations.field import assign_field_states
from recursive_integrity_toolkit.representations.content_hash import assign_content_states


def scope(n=4):
    return CalculationScope(('v1',),tuple(RecordKey('v1',str(i)) for i in range(n)),(),'included_representation_records','diversity-test')


def descriptor():
    return RepresentationDescriptor('topic','topic_field','v1','literal_field_value',field_name='topic',missing_value_policy='exclude')


def represented(labels=('a','a','b','c')):
    rows=tuple(normalize_row(dict(dataset_version='v1',record_id=str(i),content='synthetic',topic=v),kind='records') for i,v in enumerate(labels))
    return assign_field_states(rows,dataset_versions=('v1',),scope_id='diversity-test',config=RepresentationConfig('topic','topic_field','topic','v1','exclude'))


def weights(values): return {RecordKey('v1',str(i)):v for i,v in enumerate(values)}
def weighted(r,w): return calculate_state_distribution(r,weighting=WeightingOptions('weighted','weight'),weights=w)
def approx(v): return pytest.approx(float(v),abs=1e-12,rel=1e-12)


def test_T1_diversity_owner_and_placeholder(owner_checker,repo_root):
    owner_checker('metrics/diversity.py','T1')
    text=(repo_root/'src/recursive_integrity_toolkit/metrics/diversity.py').read_text(encoding='utf-8')
    assert 'F-003' in text and 'F-004' in text
    assert all('def '+name not in text for name in ('support_delta','shannon_entropy','simulate','ancestry_hhi'))


@pytest.mark.parametrize('p,d',[(('1',),'0'),(('1/2','1/2'),'1/2'),(('1/4',)*4,'3/4'),(('1/2','1/4','1/4'),'5/8')])
def test_F003_A_to_D(p,d):
    x=distribution_from_probabilities(tuple((str(i),float(Fraction(v))) for i,v in enumerate(p)),scope=scope(),representation=descriptor())
    assert x.gini_simpson_diversity.value==approx(Fraction(d))
    assert x.simpson_concentration.value==approx(1-Fraction(d))
    assert x.gini_simpson_diversity.metadata.formula_id=='F-003'
    assert x.simpson_concentration.metadata.formula_id=='F-004'


@pytest.mark.parametrize('n',[1,2,3,4,8,17,100])
def test_equal_state_distribution(n):
    x=distribution_from_counts(tuple((str(i),1) for i in range(n)),scope=scope(n),representation=descriptor())
    assert x.gini_simpson_diversity.value==approx(1-Fraction(1,n))
    assert x.simpson_concentration.value==approx(Fraction(1,n)) and x.support_size.value==n


@pytest.mark.parametrize('p',[(('a',-1e-30),('b',1.)),(('a',float('nan')),),(('a',float('inf')),),(('a',float('-inf')),),(('a',True),),(('a',False),),(('a','1'),),(('a',None),),(('a',1.0000000000001),),(('a',0),),(('a',.3),('b',.3)),(('a',.5),('b',.5001)),(('a',Fraction(1)),),(('a',10**1000),)])
def test_bad_probabilities(p):
    with pytest.raises(CanonicalValidationError): distribution_from_probabilities(p,scope=scope(),representation=descriptor())


def test_roundoff_retained_without_normalization():
    p=(('a',.5),('b',.5-4e-13))
    x=distribution_from_probabilities(p,scope=scope(),representation=descriptor())
    assert x.states[1].state_frequency==p[1][1]
    assert x.probability_residual!=0 and abs(x.probability_residual)<=1e-12
    assert x.gini_simpson_diversity.value==approx(1-p[0][1]**2-p[1][1]**2)


def test_tolerance_does_not_allow_negative():
    with pytest.raises(CanonicalValidationError): distribution_from_probabilities((('a',1.),('b',-5e-324)),scope=scope(),representation=descriptor())


def test_subnormal_positive_probability_keeps_support():
    x=distribution_from_probabilities((('a',1.),('b',5e-324)),scope=scope(),representation=descriptor())
    assert x.support_size.value==2 and x.states[1].state_frequency>0


def test_permutation_and_replication_invariance():
    for items in permutations((('a',2),('b',1),('c',1))):
        x=distribution_from_counts(items,scope=scope(),representation=descriptor())
        assert x.gini_simpson_diversity.value==approx(Fraction(5,8))
    a=calculate_state_distribution(represented()).unweighted
    b=calculate_state_distribution(represented(('a','a','b','c')*2)).unweighted
    assert tuple(s.state_frequency for s in a.states)==tuple(s.state_frequency for s in b.states)
    assert a.gini_simpson_diversity.value==b.gini_simpson_diversity.value and a.support==b.support
    assert b.analyzed_record_count==2*a.analyzed_record_count


def test_weighting_is_explicit():
    r=represented(); assert calculate_state_distribution(r).weighted is None
    with pytest.raises(CanonicalValidationError) as e: calculate_state_distribution(r,weights=weights((1,2,3,4)))
    assert e.value.code is ErrorCode.WEIGHT_INVALID


def test_weighted_and_unweighted_are_separate():
    r=represented(); x=weighted(r,weights((1,1,0,2)))
    assert x.unweighted==calculate_state_distribution(r).unweighted
    assert x.unweighted.gini_simpson_diversity.value==approx(Fraction(5,8))
    assert x.weighted.gini_simpson_diversity.value==.5 and x.weighted.simpson_concentration.value==.5
    assert x.weighted.support==('a','c') and x.unweighted.support==('a','b','c')
    assert tuple(s.state_count for s in x.weighted.states)==(2,1,1)
    assert tuple(s.state_mass for s in x.weighted.states)==(2,0,2)
    assert x.weighted.frequency_denominator==4 and x.weighted.denominator_basis=='included_record_weight_mass'
    assert x.weighted.gini_simpson_diversity.metadata.weighting.weighting_mode=='weighted'


@pytest.mark.parametrize('w',[None,{},weights((1,1,1)),weights((1,1,1,1,1)),weights((1,-1,1,1)),weights((0,0,0,0)),weights((1,None,1,1)),weights((1,True,1,1)),weights((1,'2',1,1)),weights((1,float('nan'),1,1)),weights((1,float('inf'),1,1)),weights((1e308,1e308,1,1)),weights((0,0,5e-324,1e308)),{0:1},weights((Fraction(1),1,1,1))])
def test_invalid_weight_basis(w):
    with pytest.raises(CanonicalValidationError): weighted(represented(),w)


def test_weight_permutation_and_scale_invariance():
    r=represented(); w=weights((.1,.2,.3,.4))
    a=weighted(r,w); b=weighted(r,dict(reversed(tuple(w.items())))); c=weighted(r,weights((1,2,3,4)))
    assert a==b and a.weighted.gini_simpson_diversity.value==approx(c.weighted.gini_simpson_diversity.value)
    assert a.unweighted==c.unweighted


def test_zero_weight_does_not_delete_unweighted_record():
    x=weighted(represented(),weights((0,0,1,0)))
    assert x.unweighted.analyzed_record_count==4 and x.unweighted.support_size.value==3
    assert x.weighted.support_size.value==1 and x.weighted.gini_simpson_diversity.value==0
    assert x.weighted.status is CalculationStatus.AVAILABLE


def test_excluded_record_not_in_weighted_denominator():
    r=represented(('a',None,'b'))
    x=weighted(r,{RecordKey('v1','0'):1,RecordKey('v1','2'):3})
    assert x.coverage.denominator==3 and x.unweighted.analyzed_record_count==2 and x.weighted.frequency_denominator==4
    with pytest.raises(CanonicalValidationError): weighted(r,weights((1,0,3)))


def test_all_excluded_weighted_unavailable():
    x=weighted(represented((None,None)),{})
    assert x.weighted.status is CalculationStatus.UNAVAILABLE and x.weighted.gini_simpson_diversity.value is None


def test_exact_content_keeps_record_form_scope():
    rows=tuple(normalize_row(dict(dataset_version='v1',record_id=str(i),content=v),kind='records') for i,v in enumerate(('A','A','a')))
    r=assign_content_states(rows,dataset_versions=('v1',),scope_id='exact',representation_name='record_form',representation_version='v1',normalization_profile='exact_utf8_v1',content_mode=ContentMode.INLINE)
    x=calculate_state_distribution(r.representation).unweighted
    assert x.support_size.value==2 and x.representation.normalization_profile=='exact_utf8_v1'
    assert x.gini_simpson_diversity.value==approx(Fraction(4,9))


def test_unchanged_frozen_oracles(repo_root):
    import json
    p=repo_root/'tests/golden/phase3_math_cases.json'; before=p.read_bytes(); data=json.loads(before)
    cases={c['case_id']:c for c in data['cases']}
    for key in ('F003-A','F003-B','F003-C','F003-D'):
        c=cases[key]; pairs=tuple((str(i),float(Fraction(v))) for i,v in enumerate(c['inputs']['probabilities']))
        x=distribution_from_probabilities(pairs,scope=scope(),representation=descriptor())
        assert x.gini_simpson_diversity.value==approx(Fraction(c['expected']['gini_simpson_diversity']))
    assert data['expectations_generated_by_implementation'] is False and p.read_bytes()==before


def test_weighted_fixture(repo_root):
    import json
    p=repo_root/'tests/fixtures/weighted/phase3_distribution_cases.json'; before=p.read_bytes()
    for c in json.loads(before)['cases']:
        x=weighted(represented(tuple(c['labels'])),weights(c['weights']))
        assert x.unweighted.gini_simpson_diversity.value==approx(Fraction(c['unweighted_diversity']))
        assert x.weighted.gini_simpson_diversity.value==approx(Fraction(c['weighted_diversity']))
        assert x.weighted.support_size.value==c['weighted_support']
    assert p.read_bytes()==before


def test_no_io_network_dynamic_execution_or_private_logging(monkeypatch,capsys,tmp_path):
    import builtins,socket
    from pathlib import Path
    r=represented(('PRIVATE_SENTINEL','PRIVATE_SENTINEL','other'))
    def blocked(*args,**kwargs): raise AssertionError('unexpected side effect')
    with monkeypatch.context() as m:
        for name in ('open','eval','exec'): m.setattr(builtins,name,blocked)
        m.setattr(Path,'open',blocked); m.setattr(socket,'create_connection',blocked); m.setattr(socket,'getaddrinfo',blocked)
        x=calculate_state_distribution(r)
    assert 'PRIVATE_SENTINEL' not in repr(x)
    assert capsys.readouterr()==('','') and not list(tmp_path.iterdir())
    with pytest.raises(CanonicalValidationError) as e: distribution_from_probabilities({'PRIVATE_SENTINEL':-1},scope=scope(),representation=descriptor())
    assert 'PRIVATE_SENTINEL' not in str(e.value)


def test_unsafe_object_hooks_are_not_called():
    class Hostile:
        def __iter__(self): raise AssertionError('iterator')
        def __float__(self): raise AssertionError('float')
        def __str__(self): raise AssertionError('str')
        def __bool__(self): raise AssertionError('bool')
    for x in (Hostile(),{'a':Hostile()},((Hostile(),1),)):
        with pytest.raises(CanonicalValidationError): distribution_from_probabilities(x,scope=scope(),representation=descriptor())


def test_no_later_computations():
    x=calculate_state_distribution(represented()).unweighted
    for name in ('support_delta','support_retention','shannon_entropy','tail','simulation','source_type_shares','closure_bounds','ancestry_hhi','report'):
        assert not hasattr(x,name)
    assert x.gini_simpson_diversity.metadata.evidence_class is CalculationEvidenceClass.DERIVED_METRIC
