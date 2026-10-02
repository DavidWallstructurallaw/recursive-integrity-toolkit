"""T1 Step 8: independent F-015 oracles, exact enumeration and seeded invariants.

The frozen source expectations are read, never regenerated. Sampler correctness
uses integer/mass/absorption invariants and finite exact multinomial expectations.
"""
from dataclasses import replace
from fractions import Fraction
from itertools import product
from math import factorial, fsum
from types import MappingProxyType
import json
import pytest

from recursive_integrity_toolkit.errors import CanonicalValidationError, ErrorCode
from recursive_integrity_toolkit.models import (
    CalculationScope, CalculationEvidenceClass, RecordKey, RepresentationDescriptor,
)
from recursive_integrity_toolkit.metrics.resampling import (
    expected_diversity_after_steps, simulate_closed_resampling,
    MAX_STATES, MAX_STEPS, MAX_REPLICATES, MAX_PATH_CELLS, MAX_RESAMPLE_SIZE, MAX_SEED_BITS,
)


def context():
    scope = CalculationScope(('v1',), (RecordKey('v1', 'r1'),), (), 'explicit_scenario_basis', 'closed-test')
    rep = RepresentationDescriptor('topic', 'topic_field', 'v1', 'literal_field_value', field_name='topic')
    return dict(scope=scope, representation=rep)


def analytic(p=None, **kw):
    args = dict(resample_size=4, steps=2, **context()); args.update(kw)
    return expected_diversity_after_steps({'a':.5,'b':.25,'c':.25} if p is None else p, **args)


def sample(p=None, **kw):
    args = dict(resample_size=4, steps=3, seed=17, replicates=2, **context()); args.update(kw)
    return simulate_closed_resampling({'a':.5,'b':.25,'c':.25} if p is None else p, **args)


def test_T1_resampling_owner_and_placeholder(owner_checker, repo_root):
    owner_checker('metrics/resampling.py', 'T1')
    text = (repo_root/'src/recursive_integrity_toolkit/metrics/resampling.py').read_text()
    assert 'Phase 3 Step 8' in text
    assert 'def simulate_closed_resampling(' in text
    for name in ('simulate_reopening', 'external_reference_loss', 'ancestry_hhi'):
        assert 'def '+name+'(' not in text


def test_T1_expected_one_step_contraction_matches_formula():
    result=analytic({'a':.5,'b':.5},resample_size=2,steps=1)
    assert result.expected_diversity == (.5,.25)
    assert result.random_seed is None and result.rng_name is None
    assert result.method=='analytic_expectation' and result.simulation_replicates is None


def test_T1_expected_multi_step_contraction_matches_formula():
    result=analytic(dict.fromkeys('abcd',.25),resample_size=4,steps=2)
    assert result.expected_diversity == pytest.approx((3/4,9/16,27/64),abs=1e-12,rel=1e-12)
    assert result.expected_diversity_metadata.formula_id=='F-015'


def test_T1_all_frozen_F015_cases(repo_root):
    p=repo_root/'tests/golden/phase3_math_cases.json'; raw=p.read_bytes()
    cases=[c for c in json.loads(raw)['cases'] if c.get('formula_ids')==['F-015']]
    distributions={Fraction(1,2):{'a':.5,'b':.5},Fraction(3,4):dict.fromkeys('abcd',.25),
                   Fraction(7,8):dict.fromkeys('abcdefgh',.125)}
    assert len(cases)==5
    for case in cases:
        v=case['inputs']; result=analytic(distributions[Fraction(v['gini_simpson_diversity'])],
            resample_size=v['resample_size'],steps=v['simulation_horizon'])
        assert result.expected_diversity[-1]==pytest.approx(float(Fraction(case['expected']['expected_gini_simpson_diversity'])),abs=1e-12,rel=1e-12)
    assert p.read_bytes()==raw


def test_T1_authored_closed_fixture(repo_root):
    p=repo_root/'tests/fixtures/resampling/phase3_closed_cases.json'; raw=p.read_bytes(); data=json.loads(raw)
    assert data['expectations_generated_by_implementation'] is False
    for case in data['cases']:
        dist={k:float(Fraction(v)) for k,v in case['probabilities'].items()}
        result=analytic(dist,resample_size=case['n'],steps=case['steps'])
        assert result.expected_diversity==pytest.approx(tuple(float(Fraction(v)) for v in case['expected']),abs=1e-12,rel=1e-12)
    assert p.read_bytes()==raw


@pytest.mark.parametrize('n',[1,2,7,100,MAX_RESAMPLE_SIZE])
def test_T1_horizon_zero_keeps_initial(n):
    a=analytic(resample_size=n,steps=0); b=sample(resample_size=n,steps=0)
    assert a.expected_diversity==(.625,)
    for path in b.sampled_paths:
        assert len(path.generations)==1 and path.generations[0].step==0
        assert path.generations[0].state_counts is None
        assert path.generations[0].state_frequencies==(.5,.25,.25)


@pytest.mark.parametrize('p',[{'only':1.}, {'zero':0.,'only':1.}, {'':1.}])
def test_T1_single_state_absorption(p):
    a=analytic(p,steps=5); b=sample(p,steps=5)
    assert a.expected_diversity==(0.,)*6
    for path in b.sampled_paths:
        assert all(g.support_size==1 and g.gini_simpson_diversity==0 for g in path.generations)


def test_T1_n_one_absorbs_after_first_step():
    a=analytic(resample_size=1,steps=4); b=sample(resample_size=1,steps=4,replicates=12)
    assert a.expected_diversity==(.625,0,0,0,0)
    for path in b.sampled_paths:
        assert all(g.support==path.generations[1].support for g in path.generations[1:])
        assert all(g.gini_simpson_diversity==0 for g in path.generations[1:])


@pytest.mark.parametrize('n',[1,2,7,17,100,MAX_RESAMPLE_SIZE])
def test_T1_integer_sample_total_and_frequency_lattice(n):
    result=sample(resample_size=n,replicates=5)
    for path in result.sampled_paths:
        for g in path.generations[1:]:
            assert all(type(c) is int and 0<=c<=n for c in g.state_counts)
            assert sum(g.state_counts)==n
            assert g.state_frequencies==tuple(c/n for c in g.state_counts)
            assert fsum(g.state_frequencies)==pytest.approx(1.,abs=1e-12)
            assert g.support_size==sum(c>0 for c in g.state_counts)
            assert g.gini_simpson_diversity==pytest.approx(1-sum(Fraction(c,n)**2 for c in g.state_counts))


@pytest.mark.parametrize('zero_position',[0,1,2,3])
def test_T1_closed_zero_state_remains_zero(zero_position):
    p=dict(zip('abcd',(.5,.25,.25,0.)));items=list(p.values());items[zero_position],items[3]=items[3],items[zero_position]
    result=sample(dict(zip('abcd',items)),steps=12,replicates=10)
    for path in result.sampled_paths:
        previous=set(path.generations[0].support)
        for g in path.generations[1:]:
            assert g.state_counts[zero_position]==0 and set(g.support)<=previous
            previous=set(g.support)


def test_T1_fixed_seed_path_is_deterministic():
    a=sample(); b=sample(); assert a==b
    assert [p.replicate_index for p in a.sampled_paths]==[0,1]
    assert a.rng_name=='numpy.random.Generator(PCG64)'
    assert a.replicate_schedule=='replicate_major_step_major'
    assert a.state_order==('a','b','c') and a.numpy_version


def test_T1_probability_order_invariance_and_detachment():
    p={'c':.25,'a':.5,'b':.25}
    a=sample(p);b=sample(tuple(reversed(tuple(p.items()))));c=sample(MappingProxyType(p))
    assert a==b==c
    p['a']=0
    assert a.inputs.supplied_distribution==( ('a',.5),('b',.25),('c',.25))
    with pytest.raises((AttributeError,TypeError)):a.sampled_paths=()


@pytest.mark.parametrize('seed',[0,1,2**128+17,2**1024])
def test_T1_explicit_seed_used_and_global_RNG_untouched(seed,monkeypatch):
    import numpy as np, random
    before=np.random.get_state(); pybefore=random.getstate(); captured=[]
    pcg=np.random.PCG64
    def factory(value): captured.append(value); return pcg(value)
    monkeypatch.setattr(np.random,'PCG64',factory)
    sample(seed=seed)
    after=np.random.get_state()
    assert captured==[seed]
    assert before[0]==after[0] and (before[1]==after[1]).all() and before[2:]==after[2:]
    assert pybefore==random.getstate()


def test_T1_different_seeds_may_give_identical_paths():
    a=sample({'a':1},seed=1);b=sample({'a':1},seed=2)
    assert a.sampled_paths==b.sampled_paths and a.random_seed!=b.random_seed


def test_T1_realized_diversity_may_increase():
    result=sample({'a':.875,'b':.125},resample_size=8,steps=6,replicates=32,seed=19)
    assert any(after.gini_simpson_diversity>before.gini_simpson_diversity
               for path in result.sampled_paths for before,after in zip(path.generations,path.generations[1:]))


@pytest.mark.parametrize('p,n',[((Fraction(1,2),)*2,2),((Fraction(1,2),Fraction(1,3),Fraction(1,6)),3),((Fraction(1,4),)*4,4)])
def test_T1_exact_multinomial_enumeration(p,n):
    # Independent finite enumeration of all count outcomes and their rational PMF.
    expectation=Fraction(0);mass=Fraction(0)
    for counts in product(range(n+1),repeat=len(p)):
        if sum(counts)!=n:continue
        chance=Fraction(factorial(n),1)
        for c,prob in zip(counts,p):chance=chance*prob**c/factorial(c)
        mass+=chance;expectation+=chance*(1-sum(Fraction(c,n)**2 for c in counts))
    assert mass==1
    d0=1-sum(prob**2 for prob in p)
    assert expectation==(1-Fraction(1,n))*d0
    actual=analytic({str(i):float(v) for i,v in enumerate(p)},resample_size=n,steps=1)
    assert actual.expected_diversity[-1]==pytest.approx(float(expectation),abs=1e-12,rel=1e-12)


def test_T1_monte_carlo_sanity_against_exact_expectation():
    result=sample({'a':.5,'b':.5},resample_size=4,steps=3,replicates=8000,seed=812)
    for t in range(1,4):
        mean=fsum(path.generations[t].gini_simpson_diversity for path in result.sampled_paths)/8000
        assert abs(mean-float(Fraction(1,2)*Fraction(3,4)**t))<.025


@pytest.mark.parametrize('residual',[-4e-13,4e-13])
def test_T1_bounded_disclosed_sampler_correction_preserves_zeros(residual):
    p={'a':.5,'b':.5+residual,'zero':0.}
    a=analytic(p);b=sample(p)
    assert not a.inputs.correction_applied and a.inputs.supplied_distribution==a.inputs.effective_distribution
    inp=b.inputs
    assert inp.correction_applied and inp.correction_method=='divide_by_validated_total'
    assert inp.normalization_divisor==fsum(p.values())
    assert dict(inp.effective_distribution)=={s:v/inp.supplied_probability_total for s,v in p.items()}
    assert max(abs(d) for s,d in inp.probability_corrections)<=1e-12
    assert all(g.state_frequencies[2]==0 for path in b.sampled_paths for g in path.generations)


def test_T1_exact_mass_needs_no_correction():
    result=sample(); assert result.inputs.correction_applied is False
    assert result.inputs.probability_residual==0 and result.inputs.normalization_divisor==1


@pytest.mark.parametrize('p',[{},(),[],{'a':0}, {'a':.2,'b':.3}, {'a':.5,'b':.500000000002},
    {'a':-5e-324,'b':1}, {'a':float('nan')}, {'a':float('inf')}, {'a':True}, {'a':None}, {'a':'1'},
    {'a':Fraction(1)}, {'a':1.000000000001}, {'a':10**1000}, (('a',.5),('a',.5)), ((1,1),),
    (('a',1,2),), (['a',1],), {'\x00':1}, {'\ud800':1}])
@pytest.mark.parametrize('method',[analytic,sample])
def test_T1_invalid_distribution_rejected(p,method):
    with pytest.raises(CanonicalValidationError):method(p)


@pytest.mark.parametrize('name,values',[
    ('resample_size',(0,-1,True,2.5,None,'4')),
    ('steps',(-1,True,1.5,None,'2')),
    ('seed',(-1,True,2.5,None,'17')),
    ('replicates',(0,-1,True,1.5,None,'2')),
])
def test_T1_invalid_integer_parameters(name,values):
    for value in values:
        with pytest.raises(CanonicalValidationError): sample(**{name:value})
        if name in ('steps','resample_size'):
            with pytest.raises(CanonicalValidationError):analytic(**{name:value})


@pytest.mark.parametrize('option',[{'steps':MAX_STEPS+1},{'resample_size':MAX_RESAMPLE_SIZE+1},
    {'replicates':MAX_REPLICATES+1},{'seed':1<<MAX_SEED_BITS},{'steps':10000,'replicates':10000}])
def test_T1_resource_checks_before_numpy_import(option,monkeypatch):
    import builtins
    orig=builtins.__import__
    def guard(name,*a,**kw):
        if name=='numpy':raise AssertionError('NumPy was imported before bounded-work rejection')
        return orig(name,*a,**kw)
    monkeypatch.setattr(builtins,'__import__',guard)
    with pytest.raises(CanonicalValidationError) as e:sample(**option)
    assert e.value.code is ErrorCode.CONFIG_INVALID


def test_T1_state_limit_before_numpy(monkeypatch):
    p={str(i):1/(MAX_STATES+1) for i in range(MAX_STATES+1)}
    with pytest.raises(CanonicalValidationError):sample(p)


@pytest.mark.parametrize('field',[ 'resample_size','steps','seed','replicates','scope','representation'])
def test_T1_all_sample_parameters_are_required(field):
    args=dict(resample_size=2,steps=1,seed=1,replicates=1,**context());del args[field]
    with pytest.raises(TypeError):simulate_closed_resampling({'a':1},**args)


@pytest.mark.parametrize('extra',['external_distribution','reopening_weight','q','r','lambda_','rng','initial_diversity','weights'])
def test_T1_unsupported_inputs_are_not_ignored(extra):
    with pytest.raises(TypeError):sample(**{extra:1})
    with pytest.raises(TypeError):analytic(**{extra:1})


@pytest.mark.parametrize('field',[ 'scope','representation'])
@pytest.mark.parametrize('value',[None,{},(),1])
def test_T1_required_context_revalidated(field,value):
    with pytest.raises(CanonicalValidationError):sample(**{field:value})
    with pytest.raises(CanonicalValidationError):analytic(**{field:value})


def test_T1_canonical_empty_string_state_and_unknown_kept():
    x=sample({'':.25,'unknown':.25,'a':.25,'A':.25})
    assert x.state_order==('', 'A','a','unknown')


def test_T1_underflow_is_disclosed_and_not_finite_absorption():
    a=analytic({'a':.5,'b':.5},resample_size=2,steps=1200)
    assert a.expected_diversity[-1]==0 and a.numerical_underflow_steps
    assert not analytic({'a':1.},resample_size=2,steps=1200).numerical_underflow_steps


def test_T1_metadata_and_simulation_evidence():
    a=analytic();b=sample()
    for result in (a,b):
        assert result.evidence_class is CalculationEvidenceClass.SIMULATION and result.experimental
        assert result.model_name=='closed_resampling' and result.assumptions and result.limitations
        assert result.inputs.scope==context()['scope'] and result.inputs.representation==context()['representation']
    for meta in (a.expected_diversity_metadata,)+b.trajectory_metadata:
        assert meta.owner_id=='T1' and meta.evidence_class is CalculationEvidenceClass.SIMULATION
        assert meta.unit and meta.method and meta.assumptions and meta.limitations
    assert not hasattr(b,'expected_diversity') and not hasattr(a,'sampled_paths')


def test_T1_no_io_callbacks_network_or_raw_logging(monkeypatch,capsys):
    import builtins, socket, numpy
    from pathlib import Path
    # Preload NumPy; a runtime import itself is allowed, but runtime I/O is not.
    def blocked(*args,**kw): raise AssertionError('unexpected I/O or execution')
    with monkeypatch.context() as m:
        for key in ('open','eval','exec'):m.setattr(builtins,key,blocked)
        m.setattr(Path,'open',blocked);m.setattr(socket,'create_connection',blocked);m.setattr(socket,'getaddrinfo',blocked)
        a=analytic({'PRIVATE_SENTINEL':1.});b=sample({'PRIVATE_SENTINEL':1.})
    assert 'PRIVATE_SENTINEL' not in repr(a) and 'PRIVATE_SENTINEL' not in repr(b)
    assert capsys.readouterr()==('','')


def test_T1_object_conversion_hooks_are_never_called():
    class Hostile:
        def __float__(self):raise AssertionError('float')
        def __iter__(self):raise AssertionError('iter')
        def __bool__(self):raise AssertionError('bool')
        def __str__(self):raise AssertionError('str')
    for value in (Hostile(),{'a':Hostile()},((Hostile(),1),)):
        with pytest.raises(CanonicalValidationError):sample(value)


def test_T1_numpy_absence_does_not_break_analytic_or_input_imports(repo_root,subprocess_env):
    import subprocess,sys
    code='''import sys, importlib.abc
class Block(importlib.abc.MetaPathFinder):
    def find_spec(self,fullname,path=None,target=None):
        if fullname.split('.')[0] in {'numpy','pandas','pyarrow'}:raise ModuleNotFoundError('blocked')
sys.meta_path.insert(0,Block())
from recursive_integrity_toolkit.metrics.resampling import expected_diversity_after_steps,simulate_closed_resampling
from recursive_integrity_toolkit.models import CalculationScope,RepresentationDescriptor,RecordKey
from recursive_integrity_toolkit.errors import CanonicalValidationError
ctx=dict(scope=CalculationScope(('v1',),(RecordKey('v1','r'),),(),'scenario','import'),representation=RepresentationDescriptor('topic','topic_field','v1','literal',field_name='topic'))
assert expected_diversity_after_steps({'a':.5,'b':.5},resample_size=2,steps=1,**ctx).expected_diversity==(.5,.25)
try:simulate_closed_resampling({'a':1},resample_size=2,steps=1,replicates=1,seed=0,**ctx)
except CanonicalValidationError:pass
else:raise AssertionError('missing NumPy did not block sampling')
assert not {'numpy','pandas','pyarrow'} & set(sys.modules)
'''
    p=subprocess.run([sys.executable,'-S','-c',code],env=subprocess_env,capture_output=True,text=True)
    assert p.returncode==0,p.stderr


def test_T1_default_and_enabled_input_validation_never_runs_sampler(repo_root,monkeypatch):
    import recursive_integrity_toolkit.metrics.resampling as module
    from recursive_integrity_toolkit.io.validation import validate_bundle
    from recursive_integrity_toolkit.config import ScenarioConfig
    from recursive_integrity_toolkit.models import AuditBundle,InputSource,FileRole
    def blocked(*a,**kw):raise AssertionError('input-only validation executed a simulation')
    monkeypatch.setattr(module,'simulate_closed_resampling',blocked)
    monkeypatch.setattr(module,'expected_diversity_after_steps',blocked)
    h=repo_root/'examples/hero'
    roles=(FileRole.RECORDS_PRIMARY,FileRole.RECORDS_COMPARE,FileRole.PROVENANCE_MANIFEST,FileRole.CONFIG,FileRole.VERSION_ORDER)
    names=('records_v1.csv','records_v2.csv','provenance.csv','config.json','version_order.json')
    bundle=AuditBundle(tuple(InputSource(role,h/name) for role,name in zip(roles,names)))
    assert validate_bundle(bundle).observability.maximum_level==4

    from recursive_integrity_toolkit.models import ScenarioParameters,CapabilityKey,CapabilityStatus
    config=json.loads((h/'config.json').read_bytes());config['simulation']={'enabled':True,'seed':17}
    no_config=AuditBundle(tuple(s for s in bundle.sources if s.role is not FileRole.CONFIG))
    result=validate_bundle(no_config,configuration=config,scenario_parameters=ScenarioParameters(
        'closed_resampling',resample_size=8,simulation_horizon=2,simulation_replicates=3,
        state_distribution=(('a',.5),('b',.5))))
    cap=result.observability.capabilities[CapabilityKey.INTERVENTION_SIMULATION]
    assert cap.status is CapabilityStatus.EXPERIMENTAL
    assert 'R_SCENARIO_EXECUTION_DEFERRED' in cap.reason_codes and not result.has_errors
