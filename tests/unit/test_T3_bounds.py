"""T3 Step 6: independently specified F-009/F-010 direct interval tests.

Retain the inherited test identity. Only its obsolete whole-module-empty
assertion changes. Fractions/oracles are authored independently of the kernel.
"""
from dataclasses import replace
from fractions import Fraction
import json
import pytest
from recursive_integrity_toolkit.errors import CanonicalValidationError
from recursive_integrity_toolkit.io.normalization import normalize_row
from recursive_integrity_toolkit.io.validation import assess_provenance_row, join_provenance
from recursive_integrity_toolkit.metrics.bounds import closure_exposure_bounds, direct_closure_exposure
from recursive_integrity_toolkit.metrics.provenance import summarize_provenance
from recursive_integrity_toolkit.models import (
    CalculationEvidenceClass, CalculationScope, CalculationStatus, RecordKey, ValidationCoverage,
)


def scope(n=8):
    return CalculationScope(('v1',), tuple(RecordKey('v1',str(i)) for i in range(n)), (),
                            'all_valid_records_in_selected_dataset_scope','bounds-test')


def kernel(c=3,u=2,n=8):
    return closure_exposure_bounds(known_closed=c,unresolved=u,total=n,scope=scope(n))


def composition(fields):
    records=tuple(normalize_row({'dataset_version':'v1','record_id':str(i),'content':'synthetic'},kind='records')
                  for i in range(len(fields)))
    rows=tuple(assess_provenance_row(dict(dataset_version='v1',record_id=str(i),source_type='human',
               provenance_confidence='confirmed',external_grounding='unknown') | data)
               for i,data in enumerate(fields) if data is not None)
    joined=join_provenance(records,rows)
    return summarize_provenance(joined,scope=scope(len(fields)))


def values(x): return x.lower_bound.value,x.upper_bound.value,x.interval_width.value


def test_T3_bounds_owner_and_placeholder(owner_checker,repo_root):
    owner_checker('metrics/bounds.py','T3')
    text=(repo_root/'src/recursive_integrity_toolkit/metrics/bounds.py').read_text()
    assert 'Phase 3 Step 6' in text
    for name in ('lineage_closure_bounds','midpoint','risk_score','ancestry_hhi'):
        assert 'def '+name+'(' not in text


@pytest.mark.parametrize('c,u,n,expected',[(3,2,8,(3/8,5/8,1/4)),(0,0,8,(0,0,0)),
    (8,0,8,(1,1,0)),(0,8,8,(0,1,1)),(1,0,1,(1,1,0)),(0,1,1,(0,1,1)),(2,0,8,(1/4,1/4,0))])
def test_exact_intervals(c,u,n,expected):
    x=kernel(c,u,n)
    assert values(x)==expected and x.denominator==n
    assert x.known_open_count+x.known_closed_count+x.unresolved_grounding_count==n
    assert x.status is CalculationStatus.AVAILABLE


@pytest.mark.parametrize('c,u,n',[(-1,0,8),(0,-1,8),(0,0,0),(0,0,-1),(True,0,8),(0,False,8),(0,0,True),
    (1.,0,8),(0,1.,8),(0,0,8.),(9,0,8),(5,4,8),(10**1000,0,8),(None,0,8),('1',0,8),(0,float('nan'),8)])
def test_invalid_count_partition(c,u,n):
    with pytest.raises(CanonicalValidationError):
        closure_exposure_bounds(known_closed=c,unresolved=u,total=n,scope=scope())


@pytest.mark.parametrize('field,value',[('dataset_versions',('v1','v2')),('dataset_versions',(' v1',)),
    ('included_record_keys',(RecordKey('v2','x'),)*8),('included_record_keys',scope().included_record_keys[:-1]),
    ('excluded_record_keys',(RecordKey('v1','x'),)),('scope_id',''),('scope_id','\ud800'),
    ('denominator_basis','representation_records'),('included_record_keys',[]),('excluded_record_keys',[])])
def test_forged_scope(field,value):
    s=scope(); object.__setattr__(s,field,value)
    with pytest.raises(CanonicalValidationError):
        closure_exposure_bounds(known_closed=3,unresolved=2,total=8,scope=s)


def test_every_small_partition_obeys_independent_fraction_oracle_and_masking():
    for n in range(1,17):
        for c in range(n+1):
            for u in range(n-c+1):
                x=kernel(c,u,n)
                assert values(x)==(float(Fraction(c,n)),float(Fraction(c+u,n)),float(Fraction(u,n)))
                assert 0<=x.lower_bound.value<=x.upper_bound.value<=1
                assert x.upper_bound.value-x.lower_bound.value==pytest.approx(x.interval_width.value,abs=1e-12,rel=1e-12)
                if c:
                    y=kernel(c-1,u+1,n)
                    assert y.lower_bound.value<=x.lower_bound.value and y.upper_bound.value==x.upper_bound.value
                if c+u<n:
                    y=kernel(c,u+1,n)
                    assert y.lower_bound.value==x.lower_bound.value and y.upper_bound.value>=x.upper_bound.value


def test_independent_fixture_and_frozen_oracle(repo_root):
    p=repo_root/'tests/fixtures/provenance_unknown/phase3_direct_bounds.json'; before=p.read_bytes()
    for c in json.loads(before)['cases']:
        assert values(kernel(c['known_closed'],c['unresolved'],c['total']))==tuple(float(Fraction(c[k])) for k in ('lower','upper','width'))
    oracle=repo_root/'tests/golden/phase3_math_cases.json'; raw=oracle.read_bytes()
    assert json.loads(raw)['expectations_generated_by_implementation'] is False
    assert p.read_bytes()==before and oracle.read_bytes()==raw


def test_metadata_and_no_later_outputs():
    x=kernel()
    for scalar,formula in ((x.lower_bound,'F-009'),(x.upper_bound,'F-010'),(x.interval_width,None)):
        m=scalar.metadata
        assert m.owner_id=='T3' and m.formula_id==formula and m.unit=='ratio'
        assert m.evidence_class is CalculationEvidenceClass.DERIVED_METRIC
        assert m.scope==x.scope and m.representation is None and m.weighting.weighting_mode=='unweighted'
        assert m.assumptions and m.limitations
    assert x.classification_basis==x.operationalization_label=='toolkit_operationalization'
    for name in ('midpoint','risk_score','severity','risk_threshold','lineage_interval','ancestry_hhi','report','universal_score'):
        assert not hasattr(x,name)


@pytest.mark.parametrize('fields',[(None,None),({'source_type':None},{'source_type':None}),
                                  ({'provenance_confidence':None},None)])
def test_no_usable_provenance_stays_unavailable(fields):
    c=composition(fields); x=direct_closure_exposure(c)
    assert values(x)==(None,None,None) and x.status is CalculationStatus.UNAVAILABLE
    assert x.validation_messages==c.validation_messages and x.input_has_errors==c.input_has_errors
    assert x.provenance_required_field_coverage.numerator==0


def test_valid_explicit_unknown_differs_from_no_provenance():
    x=direct_closure_exposure(composition(({},{})))
    assert values(x)==(0,1,1) and x.status is CalculationStatus.AVAILABLE
    assert x.provenance_required_field_coverage.numerator==2 and x.grounding_field_coverage.numerator==0


def test_partial_errors_survive_and_coverages_remain_distinct():
    c=composition(({'external_grounding':'no'},None,{'source_type':None,'external_grounding':'yes'},{'external_grounding':'yes'}))
    x=direct_closure_exposure(c)
    assert values(x)==(.25,.75,.5) and x.input_has_errors
    assert x.validation_messages==c.validation_messages
    assert x.provenance_row_coverage.numerator==3 and x.provenance_required_field_coverage.numerator==2
    assert x.grounding_field_coverage.numerator==3
    assert x.confidence_counts==c.confidence.counts and x.confidence_field_coverage==c.confidence.field_coverage


@pytest.mark.parametrize('confidence',['confirmed','log_derived','estimated','unknown'])
def test_confidence_does_not_discount(confidence):
    c=composition(({'external_grounding':'no','provenance_confidence':confidence},{'external_grounding':'yes'}))
    x=direct_closure_exposure(c)
    assert values(x)==(.5,.5,0)
    assert x.confidence_counts==c.confidence.counts and x.confidence_status is CalculationStatus.AVAILABLE
    assert x.confidence_disclosure=='provenance_confidence_is_separate_and_does_not_discount_grounding'


def test_incomplete_confidence_disclosure_remains_unavailable_with_valid_partial_bounds():
    x=direct_closure_exposure(composition(({'external_grounding':'no'},{'provenance_confidence':None})))
    assert values(x)==(.5,1,.5) and x.confidence_counts is None
    assert x.confidence_status is CalculationStatus.UNAVAILABLE and x.input_has_errors


@pytest.mark.parametrize('field',['analyzed_record_count','records_with_matching_rows','missing_provenance_count'])
def test_count_tampering(field):
    c=composition(({},None)); scalar=getattr(c,field)
    with pytest.raises(CanonicalValidationError):direct_closure_exposure(replace(c,**{field:replace(scalar,value=99)}))


@pytest.mark.parametrize('field',['provenance_row_coverage','provenance_required_field_coverage','grounding_field_coverage'])
def test_coverage_tampering(field):
    c=composition(({},None)); old=getattr(c,field)
    with pytest.raises(CanonicalValidationError):
        direct_closure_exposure(replace(c,**{field:ValidationCoverage(2,2,old.denominator_name)}))


@pytest.mark.parametrize('change',[{'assignments':(None,)},{'assignments':[]}, {'classification_basis':'invented'},
    {'known_open_count':None},{'input_has_errors':True},{'validation_messages':[]}])
def test_invalid_direct_contract_is_structured_error(change):
    c=composition(({},)); b=replace(c.direct_grounding,**change)
    with pytest.raises(CanonicalValidationError):direct_closure_exposure(replace(c,direct_grounding=b))


@pytest.mark.parametrize('change',[{'classification':'known_open'},{'basis':'invented'},{'missing_required_fields':('source_type',)},
    {'record_key':RecordKey('v2','0')},{'classification':True}])
def test_classification_cannot_be_upgraded_from_unknown(change):
    c=composition(({},)); a=replace(c.direct_grounding.assignments[0],**change)
    b=replace(c.direct_grounding,assignments=(a,))
    with pytest.raises(CanonicalValidationError):direct_closure_exposure(replace(c,direct_grounding=b))


def test_incomplete_missing_error_cannot_be_erased():
    c=composition(({'source_type':None},))
    b=replace(c.direct_grounding,validation_messages=(),input_has_errors=False)
    with pytest.raises(CanonicalValidationError):
        direct_closure_exposure(replace(c,direct_grounding=b,validation_messages=(),input_has_errors=False))


@pytest.mark.parametrize('change',[{'status':CalculationStatus.UNAVAILABLE},{'counts':(('confirmed',1),)},
    {'counts':(('confirmed',True),('log_derived',0),('estimated',0),('unknown',0))},
    {'shares':(('confirmed',1.),)}, {'field_coverage':ValidationCoverage(0,1,'all_valid_records_in_selected_dataset_scope')},
    {'unavailable_record_keys':(RecordKey('v1','0'),)}])
def test_confidence_tampering(change):
    c=composition(({},))
    with pytest.raises(CanonicalValidationError):direct_closure_exposure(replace(c,confidence=replace(c.confidence,**change)))


def test_scope_order_and_assignment_order_do_not_change_result():
    c=composition(({}, {'external_grounding':'no'}, None))
    s=replace(c.scope,included_record_keys=tuple(reversed(c.scope.included_record_keys)))
    b=replace(c.direct_grounding,scope=s,assignments=tuple(reversed(c.direct_grounding.assignments)))
    assert direct_closure_exposure(c)==direct_closure_exposure(replace(c,scope=s,direct_grounding=b))


def test_no_automatic_weighting():
    c=composition(({'external_grounding':'no'},None))
    assert values(direct_closure_exposure(replace(c,weighted_source='inert unused field')))==(.5,1,.5)
    with pytest.raises(TypeError):closure_exposure_bounds(known_closed=1,unresolved=1,total=2,scope=scope(2),weighting='weighted')


def test_pure_and_dataset_calls_do_not_read_write_execute_or_traverse(monkeypatch,tmp_path,capsys):
    import builtins,socket
    from pathlib import Path
    import recursive_integrity_toolkit.io.validation as validation
    c=composition(({'notes':'PRIVATE_SENTINEL','parent_ids':('v99::unread',),'external_grounding':'no'},{}))
    def blocked(*a,**kw):raise AssertionError('unexpected side effect')
    with monkeypatch.context() as m:
        for name in ('open','eval','exec'):m.setattr(builtins,name,blocked)
        m.setattr(Path,'open',blocked);m.setattr(socket,'create_connection',blocked);m.setattr(socket,'getaddrinfo',blocked)
        m.setattr(validation,'join_provenance',blocked);m.setattr(validation,'resolve_parent_references',blocked)
        x=direct_closure_exposure(c);y=kernel()
    assert values(x)==(.5,1,.5) and values(y)==(3/8,5/8,1/4)
    assert 'PRIVATE_SENTINEL' not in repr(x) and 'v99' not in repr(x)
    assert capsys.readouterr()==('','') and not list(tmp_path.iterdir())


def test_hostile_inputs_rejected_before_hooks():
    class Hostile:
        def __getattr__(self,name):raise AssertionError('attribute hook')
        def __eq__(self,other):raise AssertionError('equality hook')
        def __int__(self):raise AssertionError('integer hook')
    with pytest.raises(CanonicalValidationError):direct_closure_exposure(Hostile())
    with pytest.raises(CanonicalValidationError):kernel(Hostile())
    c=composition(({},));b=replace(c.direct_grounding,assignments=(Hostile(),))
    with pytest.raises(CanonicalValidationError):direct_closure_exposure(replace(c,direct_grounding=b))
