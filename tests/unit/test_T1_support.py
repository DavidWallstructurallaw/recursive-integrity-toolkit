"""T1 F-001/F-002 tests: exact counts, scoped frequencies and positive support.

Independent oracles: Definitions section 7 and approved F001-A/F002-A.
Extra cases exercise boundaries and invariants, without adding theory claims.
"""
from dataclasses import replace
from fractions import Fraction
import pytest
from recursive_integrity_toolkit.config import RepresentationConfig
from recursive_integrity_toolkit.errors import CanonicalValidationError
from recursive_integrity_toolkit.io.normalization import normalize_row
from recursive_integrity_toolkit.metrics.diversity import calculate_state_distribution, distribution_from_counts, distribution_from_probabilities
from recursive_integrity_toolkit.models import CalculationScope, CalculationStatus, CalculationReason, CalculationEvidenceClass, RecordKey, RepresentationDescriptor, ValidationCoverage
from recursive_integrity_toolkit.representations.field import assign_field_states


def scope(n=4):
    return CalculationScope(('v1',),tuple(RecordKey('v1',str(i)) for i in range(n)),(), 'included_representation_records','support-test')


def descriptor():
    return RepresentationDescriptor('topic','topic_field','v1','literal_field_value',field_name='topic',missing_value_policy='exclude')


def represented(fields, policy='exclude', missing=None):
    rows=tuple(normalize_row(dict(dataset_version='v1',record_id=str(i),content='synthetic',**f),kind='records') for i,f in enumerate(fields))
    return assign_field_states(rows,dataset_versions=('v1',),scope_id='support-test',config=RepresentationConfig('topic','topic_field','topic','v1',policy),missing_state_id=missing)


def test_T1_support_owner_and_placeholder(owner_checker,repo_root):
    owner_checker('metrics/diversity.py','T1')
    text=(repo_root/'src/recursive_integrity_toolkit/metrics/diversity.py').read_text(encoding='utf-8')
    assert 'Phase 3 Step 4' in text
    assert all('def '+name not in text for name in ('support_delta','support_retention','resample'))


def test_F001_counts_and_frequencies():
    x=distribution_from_counts({'c':1,'a':2,'b':1},scope=scope(),representation=descriptor())
    assert tuple(s.state_count for s in x.states)==(2,1,1)
    assert tuple(s.state_frequency for s in x.states)==(.5,.25,.25)
    assert x.frequency_denominator==4 and x.analyzed_record_count==4
    assert x.frequency_metadata.formula_id=='F-001'
    assert x.count_metadata.evidence_class is CalculationEvidenceClass.OBSERVED_FACT


def test_F002_zero_mass_is_retained_outside_support():
    x=distribution_from_probabilities((('a',.5),('b',.5),('c',0)),scope=scope(),representation=descriptor())
    assert x.support==('a','b') and x.support_size.value==2
    assert len(x.states)==3 and x.states[-1].state_count is None
    assert x.count_metadata is None and x.frequency_denominator is None
    assert x.frequency_metadata.formula_id is None and x.input_basis=='explicit_probability_vector'


@pytest.mark.parametrize('value',[-1,.5,True,False,None,'2',float('nan'),float('inf'),Fraction(1)])
def test_invalid_count_components(value):
    with pytest.raises(CanonicalValidationError): distribution_from_counts({'a':value,'b':1},scope=scope(),representation=descriptor())


@pytest.mark.parametrize('counts',[{}, {'a':0}, {'a':2}, {'a':5}, (('a',2),('a',2)), [('a',4)], {'a':10**1000}])
def test_invalid_count_total_or_structure(counts):
    with pytest.raises(CanonicalValidationError): distribution_from_counts(counts,scope=scope(),representation=descriptor())


@pytest.mark.parametrize('value',[(),{},(('a',),),(('a',1,2),),((None,1),),((True,1),),(('\x00',1),), (('\ud800',1),),(['a',1],),'a'])
def test_malformed_vector(value):
    with pytest.raises(CanonicalValidationError): distribution_from_probabilities(value,scope=scope(),representation=descriptor())


def test_zero_count_state_retained():
    x=distribution_from_counts({'a':4,'z':0},scope=scope(),representation=descriptor())
    assert x.support==('a',) and x.states[-1].state_count==0


def test_literal_states_remain_distinct():
    labels=('', 'unknown',' ','A','a','é','e\u0301')
    x=calculate_state_distribution(represented([{'topic':v} for v in labels])).unweighted
    assert x.support_size.value==7 and set(x.support)==set(labels)


def test_exclusion_denominator_and_original_provenance_scope():
    from recursive_integrity_toolkit.io.validation import join_provenance
    rows=tuple(normalize_row(dict(dataset_version='v1',record_id=str(i),content='s',topic=v),kind='records') for i,v in enumerate(('a',None,'b',None)))
    r=assign_field_states(rows,dataset_versions=('v1',),scope_id='exclusions',config=RepresentationConfig('topic','topic_field','topic','v1','exclude'))
    x=calculate_state_distribution(r)
    assert x.coverage==ValidationCoverage(2,4,'selected_valid_records')
    assert x.unweighted.frequency_denominator==2 and len(x.excluded_assignments)==2
    assert join_provenance(rows).provenance_row_coverage.denominator==4
    assert len(rows)==4 and len(r.assignments)==4


@pytest.mark.parametrize('fields,reason',[([],CalculationReason.EMPTY_SCOPE),([{'topic':None},{}],CalculationReason.ALL_EXCLUDED)])
def test_empty_is_unavailable_not_point_mass(fields,reason):
    x=calculate_state_distribution(represented(fields)).unweighted
    assert x.status is CalculationStatus.UNAVAILABLE and x.frequency_denominator is None
    for scalar in (x.support_size,x.gini_simpson_diversity,x.simpson_concentration):
        assert scalar.value is None and scalar.reason_codes==(reason,)


def test_explicit_missing_state_separate_from_unknown():
    x=calculate_state_distribution(represented([{'topic':'unknown'},{},{'topic':None}],'explicit_missing_state','MISSING')).unweighted
    assert {s.state_id:s.state_count for s in x.states}=={'MISSING':2,'unknown':1}


@pytest.mark.parametrize('change',[{'status':CalculationStatus.UNAVAILABLE},{'coverage':ValidationCoverage(1,2,'selected_valid_records')},{'reason_codes':(CalculationReason.ALL_EXCLUDED,)},{'assignments':()},{'field_states':()},{'assignments':'rows'}])
def test_forged_representation_summary(change):
    with pytest.raises(CanonicalValidationError): calculate_state_distribution(replace(represented([{'topic':'a'},{'topic':'b'}]),**change))


def test_duplicate_assignment_rejected():
    r=represented([{'topic':'a'},{'topic':'b'}])
    with pytest.raises(CanonicalValidationError): calculate_state_distribution(replace(r,assignments=(r.assignments[0],)*2))


@pytest.mark.parametrize('change',[{'dataset_versions':('v1','v2')},{'scope_id':''},{'denominator_basis':''},{'included_record_keys':(RecordKey('v2','a'),)}])
def test_forged_scope_is_revalidated(change):
    x=scope()
    for k,v in change.items(): object.__setattr__(x,k,v)
    with pytest.raises(CanonicalValidationError): distribution_from_counts({'a':4},scope=x,representation=descriptor())


@pytest.mark.parametrize('value',[None,{},(),'scope'])
def test_wrong_context_types(value):
    with pytest.raises(CanonicalValidationError): distribution_from_counts({'a':4},scope=value,representation=descriptor())
    with pytest.raises(CanonicalValidationError): distribution_from_counts({'a':4},scope=scope(),representation=value)


def test_deterministic_detached_output():
    values={'a':2,'b':1,'c':1}
    a=distribution_from_counts(values,scope=scope(),representation=descriptor())
    b=distribution_from_counts(tuple(reversed(tuple(values.items()))),scope=scope(),representation=descriptor())
    assert a==b
    values['a']=99
    assert a.states[0].state_count==2
    with pytest.raises((AttributeError,TypeError)): a.states[0].state_count=7


def test_assignment_permutation():
    r=represented([{'topic':'b'},{'topic':'a'},{'topic':'a'}])
    p=replace(r,assignments=tuple(reversed(r.assignments)),field_states=tuple(reversed(r.field_states)),scope=replace(r.scope,included_record_keys=tuple(reversed(r.scope.included_record_keys))))
    assert calculate_state_distribution(r)==calculate_state_distribution(p)


@pytest.mark.parametrize('name',['normalization_profile','missing_value_policy','representation_source'])
def test_descriptor_rejects_object_hooks(name):
    class Hostile:
        def __eq__(self,other): raise AssertionError('comparison hook')
    d=descriptor(); object.__setattr__(d,name,Hostile())
    with pytest.raises(CanonicalValidationError): distribution_from_probabilities({'a':1.},scope=scope(),representation=d)


def test_forged_excluded_assignment_rejected():
    r=represented([{'topic':'a'},{'topic':None}])
    bad=replace(r.assignments[1],state_id='invented',exclusion_reason=None)
    with pytest.raises(CanonicalValidationError): calculate_state_distribution(replace(r,assignments=(r.assignments[0],bad)))
