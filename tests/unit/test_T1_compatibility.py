"""Step 9 explicit pair gates and F-005/F-006/F-018 independent oracles.

Only explicitly selected pairs are calculated. Frozen Hero expectations, exact
rational arithmetic and authored mapping cases remain independent of kernels.
"""
from dataclasses import replace
from fractions import Fraction
from types import MappingProxyType
import json
import pytest

from recursive_integrity_toolkit.config import RepresentationConfig
from recursive_integrity_toolkit.errors import CanonicalValidationError, ErrorCode
from recursive_integrity_toolkit.io.normalization import normalize_row
from recursive_integrity_toolkit.io.validation import resolve_version_order
from recursive_integrity_toolkit.models import (
    CalculationScope, CalculationStatus, CalculationReason, CalculationEvidenceClass,
    ExplicitPairContext, RecordKey, RepresentationDescriptor, WeightingOptions,
)
from recursive_integrity_toolkit.representations.compatibility import (
    StateMappingDeclaration, validate_representation_compatibility,
)
from recursive_integrity_toolkit.representations.field import assign_field_states
from recursive_integrity_toolkit.metrics.diversity import (
    compare_support, calculate_state_distribution, distribution_from_counts,
    distribution_from_probabilities,
)


def _rep(**changes):
    return replace(RepresentationDescriptor('topic', 'topic_field', 'taxonomy-v1',
                    'literal_field_value', field_name='topic', missing_value_policy='exclude'), **changes)


def _counts(version, counts, rep=None):
    scope = CalculationScope((version,), tuple(RecordKey(version, str(i)) for i in range(sum(counts.values()))),
                             (), 'included_representation_records', 'scope-' + version)
    return distribution_from_counts(counts, scope=scope, representation=_rep() if rep is None else rep)


def _pair(a=None, b=None):
    a = _counts('v1', {'a':2, 'b':1, 'c':1}) if a is None else a
    b = _counts('v2', {'a':1, 'c':1, 'd':2}) if b is None else b
    order = resolve_version_order((a.scope.dataset_versions[0], b.scope.dataset_versions[0]),
                    invocation_order=(a.scope.dataset_versions[0], b.scope.dataset_versions[0]))
    context = ExplicitPairContext(a.scope, b.scope, a.representation, b.representation, order)
    return a, b, context


def _compare(a=None, b=None, **kwargs):
    a, b, context = _pair(a, b)
    options = dict(context=context, earlier_state_semantics='taxonomy-meaning-v1', later_state_semantics='taxonomy-meaning-v1')
    options.update(kwargs)
    return compare_support(a, b, **options)


def _compatible(context, **kwargs):
    options = dict(earlier_state_semantics='taxonomy-meaning-v1', later_state_semantics='taxonomy-meaning-v1')
    options.update(kwargs)
    return validate_representation_compatibility(context, **options)


def _mapping_pair(direction='earlier_to_later'):
    fine = _rep(representation_version='fine-v1')
    coarse = _rep(representation_version='coarse-v1', binning_or_mapping_rule='literal_coarse_labels')
    a = _counts('v1', {'red':2, 'green':1, 'pear':1}, fine) if direction == 'earlier_to_later' else _counts('v1', {'apple':1, 'pear':3}, coarse)
    b = _counts('v2', {'apple':1, 'pear':3}, coarse) if direction == 'earlier_to_later' else _counts('v2', {'red':2, 'green':1, 'pear':1}, fine)
    a, b, context = _pair(a, b)
    mapping = StateMappingDeclaration(direction, fine, coarse, 'fine-meaning', 'coarse-meaning',
                                      {'red':'apple', 'green':'apple', 'pear':'pear'})
    kw = dict(context=context, state_mapping=mapping,
              earlier_state_semantics='fine-meaning' if direction=='earlier_to_later' else 'coarse-meaning',
              later_state_semantics='coarse-meaning' if direction=='earlier_to_later' else 'fine-meaning')
    return a, b, kw


def test_equal_size_support_can_lose_and_add_states():
    x = _compare()
    assert x.support_delta.value == 0 and x.support_loss_count.value == x.support_added_count.value == 1
    assert x.extinct_states == ('b',) and x.added_states == ('d',) and x.retained_states == ('a','c')
    assert x.support_retention_ratio.value == 2/3 and x.retention_denominator == 3
    assert x.gini_simpson_diversity_delta.value == 0


def test_same_support_changed_frequencies():
    x = _compare(_counts('v1', {'a':2, 'b':2}), _counts('v2', {'a':3, 'b':1}))
    assert x.support_delta.value == 0 and x.support_retention_ratio.value == 1
    assert x.extinct_states == x.added_states == ()
    assert x.gini_simpson_diversity_delta.value == float(Fraction(-1,8))


def test_approved_hero_pair_through_explicit_calls(repo_root):
    from recursive_integrity_toolkit.io.validation import validate_bundle
    from recursive_integrity_toolkit.models import AuditBundle, InputSource, FileRole
    h = repo_root / 'examples/hero'
    files = tuple(h.iterdir()); before={p.name:p.read_bytes() for p in files if p.is_file()}
    roles=(FileRole.RECORDS_PRIMARY,FileRole.RECORDS_COMPARE,FileRole.PROVENANCE_MANIFEST,FileRole.CONFIG,FileRole.VERSION_ORDER)
    names=('records_v1.csv','records_v2.csv','provenance.csv','config.json','version_order.json')
    bundle=validate_bundle(AuditBundle(tuple(InputSource(r,h/n) for r,n in zip(roles,names))))
    represented=tuple(assign_field_states(bundle.records,dataset_versions=(v,),scope_id=v,
        config=RepresentationConfig('topic','topic_field','topic','hero-topic-v1','exclude')) for v in ('v1','v2'))
    distributions=tuple(calculate_state_distribution(r).unweighted for r in represented)
    a,b=distributions
    context=ExplicitPairContext(a.scope,b.scope,a.representation,b.representation,bundle.version_order)
    x=compare_support(a,b,context=context,earlier_state_semantics='hero-topic-v1',later_state_semantics='hero-topic-v1')
    manifest=repo_root/'tests/golden/phase3_math_cases.json'; oracle_before=manifest.read_bytes()
    oracle=next(c['expected'] for c in json.loads(oracle_before)['cases'] if c['case_id']=='HERO-PAIR')
    assert x.support_delta.value == oracle['support_delta'] == -3
    assert x.support_retention_ratio.value == float(Fraction(oracle['support_retention'])) == 5/8
    assert x.gini_simpson_diversity_delta.value == float(Fraction(oracle['diversity_delta'])) == -1/8
    assert list(x.extinct_states)==oracle['lost_states'] and list(x.added_states)==oracle['added_states']
    assert bundle.observability.maximum_level==4 and not bundle.has_errors
    assert before=={p.name:p.read_bytes() for p in files if p.is_file()} and manifest.read_bytes()==oracle_before
    assert represented[0].included_count==8 and len(bundle.records)==16


@pytest.mark.parametrize('direction',['earlier_to_later','later_to_earlier'])
def test_declared_many_to_one_retains_both_original_bases(direction):
    a,b,kw = _mapping_pair(direction)
    x=compare_support(a,b,**kw)
    assert x.support_delta.value==0 and x.support_retention_ratio.value==1
    assert x.gini_simpson_diversity_delta.value==0
    assert x.harmonized_earlier.support_size.value==x.harmonized_later.support_size.value==2
    assert x.compatibility.collision_groups == (('apple',('green','red')),)
    assert x.compatibility.method == 'explicit_directed_state_mapping'
    assert a.support_size.value == (3 if direction=='earlier_to_later' else 2)
    assert x.mapping_effect == (('earlier',a.support_size.value,2),('later',b.support_size.value,2))
    assert 'red' in (a.support if direction=='earlier_to_later' else b.support)
    assert x.compatibility.harmonized_representation.representation_version=='coarse-v1'


def test_mapping_is_detached_and_extra_declared_states_do_not_create_records():
    a,b,kw=_mapping_pair(); raw=kw['state_mapping'].state_mapping
    raw['unobserved']='new-target'
    x=compare_support(a,b,**kw)
    raw.clear()
    assert 'new-target' not in x.harmonized_earlier.support
    assert 'red' in x.compatibility.mapping.state_mapping
    with pytest.raises(TypeError):x.compatibility.mapping.state_mapping['red']='bad'
    with pytest.raises((TypeError,AttributeError)):x.status=CalculationStatus.UNAVAILABLE


@pytest.mark.parametrize('directory,allowed',[('representation_compatible',True),('representation_incompatible',False)])
def test_literal_pair_fixtures(repo_root,directory,allowed):
    p=repo_root/'tests/fixtures'/directory/'phase3_pair.json'; before=p.read_bytes(); d=json.loads(before)
    a=_counts('v1',d['earlier_counts'],_rep(representation_version=d['earlier_version']))
    b=_counts('v2',d['later_counts'],_rep(representation_version=d['later_version']))
    if allowed:
        a,b,context=_pair(a,b)
        mapping=StateMappingDeclaration(d['direction'],a.representation,b.representation,'fine-meaning','coarse-meaning',d['mapping'])
        x=compare_support(a,b,context=context,earlier_state_semantics='fine-meaning',later_state_semantics='coarse-meaning',state_mapping=mapping)
        assert x.original_earlier.gini_simpson_diversity.value==float(Fraction(d['expected']['earlier_original_diversity']))
        assert x.harmonized_earlier.gini_simpson_diversity.value==float(Fraction(d['expected']['earlier_harmonized_diversity']))
        assert x.support_retention_ratio.value==float(Fraction(d['expected']['support_retention']))
        assert x.support_delta.value==d['expected']['support_delta']
        assert x.gini_simpson_diversity_delta.value==float(Fraction(d['expected']['diversity_delta']))
    else:
        with pytest.raises(CanonicalValidationError) as e:_compare(a,b)
        assert e.value.code is ErrorCode.REPRESENTATION_INCOMPATIBLE
    assert p.read_bytes()==before


@pytest.mark.parametrize('change',[
    {'representation_name':'label'},{'representation_version':'another'},
    {'binning_or_mapping_rule':'changed'},{'missing_value_policy':'error'},
    {'representation_source':'label_field'},{'field_name':'label'},{'normalization_profile':'exact_utf8_v1'},
])
def test_identity_declaration_mismatch_blocks_pair(change):
    a,b,c=_pair();c=replace(c,later_representation=replace(c.later_representation,**change))
    with pytest.raises(CanonicalValidationError) as e:_compatible(c)
    assert e.value.code is ErrorCode.REPRESENTATION_INCOMPATIBLE


@pytest.mark.parametrize('meaning',[None,'',[],42,'\ud800','invalid\x00text'])
def test_explicit_state_meaning_required(meaning):
    a,b,c=_pair()
    with pytest.raises(CanonicalValidationError):_compatible(c,later_state_semantics=meaning)


def test_identical_version_strings_do_not_certify_state_meanings():
    a,b,c=_pair()
    with pytest.raises(CanonicalValidationError):_compatible(c,later_state_semantics='different-distinction')


@pytest.mark.parametrize('order_kind',['missing','reversed','same_version','unloaded_pair','conflicting_sources'])
def test_invalid_chronology_never_guessed(order_kind):
    a,b,c=_pair()
    if order_kind=='missing':o=resolve_version_order(('v1','v2'))
    elif order_kind=='reversed':o=resolve_version_order(('v1','v2'),invocation_order=('v2','v1'))
    elif order_kind=='unloaded_pair':o=resolve_version_order(('v0','v2'),invocation_order=('v0','v2'))
    elif order_kind=='same_version':c=replace(c,later_scope=c.earlier_scope);o=c.version_order
    else:o=replace(c.version_order,declarations={'version_order':['v2','v1']})
    with pytest.raises(CanonicalValidationError) as e:_compatible(replace(c,version_order=o))
    assert e.value.code is ErrorCode.VERSION_ORDER_CONFLICT


def test_full_loaded_order_allows_explicit_nonadjacent_pair():
    a,b,c=_pair();o=resolve_version_order(('v1','middle','v2'),document={'version_order':['v1','middle','v2']})
    x=_compare(a,b,context=replace(c,version_order=o))
    assert x.compatibility.context.version_order.order==('v1','middle','v2')
    assert len(x.mapping_effect)==2


def test_forged_cached_order_is_revalidated_from_declarations():
    a,b,c=_pair();o=replace(c.version_order,order=('v2','v1'),order_source='invented')
    x=_compare(a,b,context=replace(c,version_order=o))
    assert x.compatibility.context.version_order.order==('v1','v2')


@pytest.mark.parametrize('value',[{}, {'a':'a'}, (), 'mapping', None])
def test_missing_or_bare_mapping_does_not_override_incompatibility(value):
    a,b,kw=_mapping_pair();kw['state_mapping']=value
    with pytest.raises(CanonicalValidationError):compare_support(a,b,**kw)


@pytest.mark.parametrize('change',[
    {'direction':'auto'},{'direction':'later_to_earlier'}, {'source_state_semantics':'different'},
    {'target_state_semantics':'different'}, {'state_mapping':{}}, {'state_mapping':[('red','apple')]},
    {'state_mapping':{'red':['apple','pear'],'green':'apple','pear':'pear'}},
    {'state_mapping':{'red':{'apple':.5},'green':'apple','pear':'pear'}},
    {'state_mapping':{'red':'apple','green':'apple'}},
    {'state_mapping':{'red':None,'green':'apple','pear':'pear'}},
    {'state_mapping':{'red':'bad\x00','green':'apple','pear':'pear'}},
])
def test_mapping_direction_completeness_and_literal_types(change):
    a,b,kw=_mapping_pair();kw['state_mapping']=replace(kw['state_mapping'],**change)
    with pytest.raises(CanonicalValidationError):compare_support(a,b,**kw)


def test_mapping_cannot_change_row_inclusion_policy():
    a,b,kw=_mapping_pair(); target=replace(b.representation,missing_value_policy='error')
    kw['context']=replace(kw['context'],later_representation=target)
    kw['state_mapping']=replace(kw['state_mapping'],target_representation=target)
    with pytest.raises(CanonicalValidationError):compare_support(a,b,**kw)


@pytest.mark.parametrize('collision',[True,False])
def test_explicit_missing_marker_is_not_an_observed_state(collision):
    ra=_rep(missing_value_policy='explicit_missing_state',missing_state_id='MISS-A')
    rb=replace(ra,missing_state_id='MISS-B',representation_version='v2')
    a,b,c=_pair(_counts('v1',{'a':1,'MISS-A':1},ra),_counts('v2',{'a':1,'MISS-B':1},rb))
    mapping=StateMappingDeclaration('earlier_to_later',ra,rb,'meaning','meaning',
        {'MISS-A':'MISS-B','a':'MISS-B' if collision else 'a'})
    args=dict(context=c,earlier_state_semantics='meaning',later_state_semantics='meaning',state_mapping=mapping)
    if collision:
        with pytest.raises(CanonicalValidationError):compare_support(a,b,**args)
    else:
        assert compare_support(a,b,**args).support_retention_ratio.value==1


def _represented(version,labels):
    rows=tuple(normalize_row(dict(dataset_version=version,record_id=str(i),content='s',topic=v),kind='records') for i,v in enumerate(labels))
    result=assign_field_states(rows,dataset_versions=(version,),scope_id='scope-'+version,
                              config=RepresentationConfig('topic','topic_field','topic','taxonomy-v1','exclude'))
    return result,rows


@pytest.mark.parametrize('which',['earlier','later','both'])
@pytest.mark.parametrize('labels',[(),(None,None)])
def test_empty_or_all_excluded_pair_is_unavailable(labels,which):
    ra,_=_represented('v1',labels if which in ('earlier','both') else ('a','b'))
    rb,_=_represented('v2',labels if which in ('later','both') else ('a','b'))
    a,b=calculate_state_distribution(ra).unweighted,calculate_state_distribution(rb).unweighted
    x=_compare(a,b)
    assert x.status is CalculationStatus.UNAVAILABLE
    assert x.extinct_states is x.added_states is x.retained_states is None
    assert x.retention_denominator is None
    expected=CalculationReason.EMPTY_SCOPE if not labels else CalculationReason.ALL_EXCLUDED
    assert x.reason_codes==(expected,)
    for scalar in (x.support_delta,x.support_loss_count,x.support_added_count,x.support_retention_ratio,x.gini_simpson_diversity_delta):
        assert scalar.value is None and scalar.reason_codes==(expected,)


def test_literal_state_identity_and_zero_states_remain_distinct():
    labels=('', 'unknown','A','a',' ','é','e\u0301')
    a=_counts('v1',{**{s:1 for s in labels},'zero':0})
    b=_counts('v2',{s:2 for s in labels})
    x=_compare(a,b)
    assert x.support_retention_ratio.value==1 and x.support_delta.value==0
    assert 'zero' not in x.retained_states and len(x.retained_states)==7


def test_original_assignment_and_provenance_denominators_unchanged():
    from recursive_integrity_toolkit.io.validation import join_provenance
    ra,rowsa=_represented('v1',('a',None,'b'));rb,rowsb=_represented('v2',('b',None,'c'))
    before=(ra.assignments,rb.assignments)
    a,b=calculate_state_distribution(ra).unweighted,calculate_state_distribution(rb).unweighted
    x=_compare(a,b)
    assert x.support_retention_ratio.value==.5
    assert x.compatibility.context.earlier_scope.excluded_record_keys==(RecordKey('v1','1'),)
    assert join_provenance(rowsa).provenance_row_coverage.denominator==3
    assert (ra.assignments,rb.assignments)==before and len(rowsa)==len(rowsb)==3


def test_explicit_weighted_pair_stays_separate_from_unweighted_presence():
    ra,_=_represented('v1',('a','b'));rb,_=_represented('v2',('a','b'))
    a=calculate_state_distribution(ra,weighting=WeightingOptions('weighted','weight'),weights={RecordKey('v1','0'):1,RecordKey('v1','1'):0})
    b=calculate_state_distribution(rb,weighting=WeightingOptions('weighted','weight'),weights={RecordKey('v2','0'):1,RecordKey('v2','1'):1})
    x=_compare(a.weighted,b.weighted)
    assert x.support_delta.value==1 and x.gini_simpson_diversity_delta.value==.5
    assert x.support_delta.metadata.weighting.weighting_mode=='weighted'
    assert _compare(a.unweighted,b.unweighted).support_delta.value==0
    with pytest.raises(CanonicalValidationError):_compare(a.unweighted,b.weighted)


def test_supplied_probability_vectors_never_gain_record_counts():
    a,b,c=_pair()
    a=distribution_from_probabilities({'a':.5,'b':.5,'zero':0},scope=a.scope,representation=a.representation)
    b=distribution_from_probabilities({'a':1.,'b':0},scope=b.scope,representation=b.representation)
    x=_compare(a,b)
    assert x.support_delta.value==-1 and x.gini_simpson_diversity_delta.value==-.5
    assert x.original_earlier.count_metadata is None and x.original_later.input_basis=='explicit_probability_vector'
    with pytest.raises(CanonicalValidationError):_compare(_pair()[0],b)


@pytest.mark.parametrize('field',['support_size','gini_simpson_diversity','simpson_concentration'])
def test_forged_derived_scalar_is_rejected(field):
    a,b,c=_pair(); original=getattr(a,field)
    altered=replace(a,**{field:replace(original,value=999)})
    with pytest.raises(CanonicalValidationError):_compare(altered,b,context=c)


@pytest.mark.parametrize('change',[
    {'status':CalculationStatus.UNAVAILABLE},{'support':('a','b')},{'support':('a','a','b','c')},
    {'states':()},{'reason_codes':(CalculationReason.EMPTY_SCOPE,)},{'analyzed_record_count':True},
    {'frequency_denominator':5},{'denominator_basis':'all_records'},{'probability_residual':.1},
    {'supplied_probability_total':.9},{'weighting':WeightingOptions('weighted','weight')},
])
def test_forged_summary_is_rejected(change):
    a,b,c=_pair()
    with pytest.raises(CanonicalValidationError):_compare(replace(a,**change),b,context=c)


@pytest.mark.parametrize('change',[{'state_count':True},{'state_count':-1},{'state_frequency':float('nan')},
                                   {'state_frequency':-.1},{'state_mass':1},{'state_id':None}])
def test_forged_table_component_is_rejected(change):
    a,b,c=_pair();a=replace(a,states=(replace(a.states[0],**change),)+a.states[1:])
    with pytest.raises(CanonicalValidationError):_compare(a,b,context=c)


def test_distributions_cannot_use_another_pair_context():
    a,b,c=_pair();scope=replace(c.earlier_scope,scope_id='different')
    with pytest.raises(CanonicalValidationError):_compare(a,b,context=replace(c,earlier_scope=scope))


def test_pair_metadata_binds_both_scopes_and_sign_convention():
    x=_compare()
    for scalar,formula in ((x.support_delta,'F-005'),(x.support_retention_ratio,'F-006'),(x.gini_simpson_diversity_delta,'F-018')):
        assert scalar.metadata.formula_id==formula and scalar.metadata.owner_id=='T1'
        assert scalar.metadata.evidence_class is CalculationEvidenceClass.DERIVED_METRIC
        assert scalar.metadata.scope.dataset_versions==('v1','v2')
        assert scalar.metadata.representation==x.compatibility.harmonized_representation
        assert scalar.metadata.assumptions and scalar.metadata.limitations and scalar.metadata.unit


def test_order_permutations_produce_identical_detached_results():
    a,b,c=_pair()
    p=replace(a,states=tuple(reversed(a.states)),support=tuple(reversed(a.support)))
    assert _compare(a,b)==_compare(p,b,context=c)
    assert a.support==('a','b','c')


def test_no_io_network_randomness_logging_or_user_callbacks(monkeypatch,capsys,tmp_path):
    import builtins,socket,random
    from pathlib import Path
    a=_counts('v1',{'PRIVATE_SENTINEL':1,'b':1});b=_counts('v2',{'b':2})
    a,b,c=_pair(a,b)
    def blocked(*args,**kwargs):raise AssertionError('unexpected execution')
    with monkeypatch.context() as m:
        for name in ('open','eval','exec'):m.setattr(builtins,name,blocked)
        m.setattr(Path,'open',blocked);m.setattr(socket,'getaddrinfo',blocked);m.setattr(socket,'create_connection',blocked)
        m.setattr(random,'random',blocked)
        x=_compare(a,b,context=c)
    assert 'PRIVATE_SENTINEL' not in repr(x) and capsys.readouterr()==('','') and not list(tmp_path.iterdir())
    for name in ('trajectory','lineage_delta','model_performance_delta','report','relative_change','simulations'):
        assert not hasattr(x,name)


def test_unsafe_object_hooks_are_not_used():
    class Hostile:
        def __eq__(self,x):raise AssertionError('comparison hook')
        def __bool__(self):raise AssertionError('bool hook')
        def __iter__(self):raise AssertionError('iterator hook')
        def __str__(self):raise AssertionError('string hook')
    a,b,c=_pair()
    for value in (Hostile(),{},'context'):
        with pytest.raises(CanonicalValidationError):_compatible(value)
    with pytest.raises(CanonicalValidationError):_compatible(c,state_mapping=Hostile())
    bad=replace(c.earlier_representation);object.__setattr__(bad,'missing_value_policy',Hostile())
    with pytest.raises(CanonicalValidationError):_compatible(replace(c,earlier_representation=bad))


def test_input_only_bundle_never_dispatches_pair_comparisons(repo_root,monkeypatch):
    import recursive_integrity_toolkit.metrics.diversity as diversity
    import recursive_integrity_toolkit.representations.compatibility as compatibility
    from recursive_integrity_toolkit.io.validation import validate_bundle
    from recursive_integrity_toolkit.models import AuditBundle,InputSource,FileRole
    def blocked(*args,**kw):raise AssertionError('input workflow invoked pair kernel')
    monkeypatch.setattr(diversity,'compare_support',blocked)
    monkeypatch.setattr(compatibility,'validate_representation_compatibility',blocked)
    h=repo_root/'examples/hero'
    roles=(FileRole.RECORDS_PRIMARY,FileRole.RECORDS_COMPARE,FileRole.PROVENANCE_MANIFEST,FileRole.CONFIG,FileRole.VERSION_ORDER)
    names=('records_v1.csv','records_v2.csv','provenance.csv','config.json','version_order.json')
    x=validate_bundle(AuditBundle(tuple(InputSource(r,h/n) for r,n in zip(roles,names))))
    assert x.observability.maximum_level==4 and not x.has_errors


@pytest.mark.parametrize('change',[{'owner_id':'T4'},{'formula_id':'F-019'},
    {'evidence_class':CalculationEvidenceClass.SIMULATION},{'unit':'percent'},{'metric_name':'risk_score'}])
def test_trace_substitution_cannot_relabel_pair_inputs(change):
    a,b,c=_pair();scalar=a.support_size
    altered=replace(a,support_size=replace(scalar,metadata=replace(scalar.metadata,**change)))
    with pytest.raises(CanonicalValidationError):_compare(altered,b,context=c)


@pytest.mark.parametrize('which',['scope','representation','order'])
def test_forged_context_containers_fail_without_untyped_exceptions(which):
    a,b,c=_pair()
    if which=='scope':object.__setattr__(c.earlier_scope,'included_record_keys',{'a':'b'})
    elif which=='representation':object.__setattr__(c.earlier_representation,'representation_version',None)
    else:object.__setattr__(c.version_order,'declarations',[])
    with pytest.raises(CanonicalValidationError):_compatible(c)


def test_weighted_many_to_one_sums_mass_without_altering_unweighted_counts():
    ra,_=_represented('v1',('red','green','pear'));rb,_=_represented('v2',('apple','pear'))
    ra=replace(ra,selection=replace(ra.selection,descriptor=_rep(representation_version='fine-v1')))
    rb=replace(rb,selection=replace(rb.selection,descriptor=_rep(representation_version='coarse-v1')))
    a=calculate_state_distribution(ra,weighting=WeightingOptions('weighted','weight'),weights={RecordKey('v1','0'):1,RecordKey('v1','1'):2,RecordKey('v1','2'):3}).weighted
    b=calculate_state_distribution(rb,weighting=WeightingOptions('weighted','weight'),weights={RecordKey('v2','0'):1,RecordKey('v2','1'):1}).weighted
    a,b,c=_pair(a,b)
    mapping=StateMappingDeclaration('earlier_to_later',a.representation,b.representation,'fine','coarse',{'red':'apple','green':'apple','pear':'pear'})
    x=compare_support(a,b,context=c,earlier_state_semantics='fine',later_state_semantics='coarse',state_mapping=mapping)
    assert x.gini_simpson_diversity_delta.value==0 and x.harmonized_earlier.frequency_denominator==6
    assert tuple(row.state_count for row in x.harmonized_earlier.states)==(2,1)
    assert tuple(row.state_mass for row in x.harmonized_earlier.states)==(3,3)
    assert a.analyzed_record_count==3 and b.analyzed_record_count==2


def test_zero_mass_source_state_requires_declared_mapping_but_never_enters_support():
    a,b,kw=_mapping_pair()
    a=_counts('v1',{'red':2,'green':1,'pear':1,'zero':0},a.representation)
    with pytest.raises(CanonicalValidationError):compare_support(a,b,**kw)
    mapping=dict(kw['state_mapping'].state_mapping);mapping['zero']='absent-target'
    kw['state_mapping']=replace(kw['state_mapping'],state_mapping=mapping)
    x=compare_support(a,b,**kw)
    assert 'absent-target' not in x.harmonized_earlier.support and x.support_delta.value==0


def test_mapped_target_absent_in_later_data_remains_visible_loss():
    a,b,kw=_mapping_pair()
    mapping=dict(kw['state_mapping'].state_mapping);mapping['pear']='absent-target'
    kw['state_mapping']=replace(kw['state_mapping'],state_mapping=mapping)
    x=compare_support(a,b,**kw)
    assert x.extinct_states==('absent-target',) and x.added_states==('pear',)
    assert x.support_delta.value==0 and x.support_retention_ratio.value==.5


def test_readonly_mapping_and_permutation_produce_same_output():
    a,b,kw=_mapping_pair();x=compare_support(a,b,**kw)
    mapping=MappingProxyType(dict(reversed(tuple(kw['state_mapping'].state_mapping.items()))))
    kw['state_mapping']=replace(kw['state_mapping'],state_mapping=mapping)
    assert x==compare_support(a,b,**kw)


def test_equal_initial_and_later_counts_return_real_zero_not_unavailable():
    x=_compare(_counts('v1',{'a':1}),_counts('v2',{'a':7}))
    assert x.status is CalculationStatus.AVAILABLE and x.support_delta.value==0
    assert x.gini_simpson_diversity_delta.value==0 and x.support_retention_ratio.value==1


def test_original_trace_methods_and_limitations_survive_revalidation():
    a,b,c=_pair()
    a=replace(a,limitations=a.limitations+('additional declared scope restriction',),
        frequency_metadata=replace(a.frequency_metadata,method='explicit validated counts divided by this scope',
                                   limitations=a.frequency_metadata.limitations+('input-specific restriction',)))
    x=_compare(a,b,context=c)
    assert x.original_earlier.frequency_metadata.method==a.frequency_metadata.method
    assert x.original_earlier.frequency_metadata.limitations==a.frequency_metadata.limitations
    assert x.original_earlier.limitations==a.limitations
