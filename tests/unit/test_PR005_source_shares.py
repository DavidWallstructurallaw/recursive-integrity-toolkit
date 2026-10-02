"""PR-005 Phase 3 Step 5 tests. Earlier Phase 2 checks are preserved.

Only declared composition, inherited coverage and direct classifications are
active. No closure interval, confidence score or report is produced.
"""


# Step 5 tests only declared-field separation. No source counts or shares.
def test_PR005_join_keeps_crossed_declarations_without_inference(repo_root):
    from recursive_integrity_toolkit.io.loaders import load_table
    from recursive_integrity_toolkit.io.normalization import normalize_row, normalize_table
    from recursive_integrity_toolkit.io.validation import join_provenance
    from recursive_integrity_toolkit.models import FileRole, InputSource
    path = repo_root / "tests/fixtures/provenance_unknown/step5_crossed.jsonl"
    before = path.read_bytes()
    provenance = normalize_table(load_table(InputSource(FileRole.PROVENANCE_MANIFEST, path)))
    records = tuple(normalize_row({"dataset_version": "v1", "record_id": row.record_key.record_id,
                                   "content": "synthetic"}, kind="records") for row in provenance)
    result = join_provenance(records, provenance)
    for match, declared in zip(result.matches, provenance):
        for field in ("source_type", "external_grounding", "human_reviewed", "provenance_confidence"):
            assert match.provenance.values[field] == declared.values[field]
    assert result.matches[1].provenance.values["source_type"] == "human"
    assert result.matches[1].provenance.values["external_grounding"] == "no"
    assert result.matches[3].provenance.values["source_type"] == "synthetic"
    assert result.matches[3].provenance.values["external_grounding"] == "yes"
    assert not hasattr(result, "source_type_shares") and not hasattr(result, "source_type_counts")
    assert path.read_bytes() == before


# Phase 3 Step 5 calculations. Every earlier input test above remains unchanged.
from dataclasses import replace
from fractions import Fraction
import json
import pytest
from recursive_integrity_toolkit.io.normalization import normalize_row
from recursive_integrity_toolkit.io.validation import assess_provenance_row, join_provenance
from recursive_integrity_toolkit.metrics.provenance import summarize_provenance
from recursive_integrity_toolkit.models import (
    CalculationScope, CalculationStatus, CalculationEvidenceClass, CalculationReason,
    RecordKey, WeightingOptions,
)
from recursive_integrity_toolkit.errors import CanonicalValidationError, ErrorCode


def _s5_case(fields=(None,), *, record_fields=None):
    records=tuple(normalize_row({'dataset_version':'v1','record_id':str(i),'content':'synthetic',
                                **(record_fields or {})},kind='records') for i in range(len(fields)))
    rows=tuple(assess_provenance_row({'dataset_version':'v1','record_id':str(i),'source_type':'unknown',
                'provenance_confidence':'confirmed','external_grounding':'unknown',**v})
                for i,v in enumerate(fields) if v is not None)
    j=join_provenance(records,rows)
    s=CalculationScope(('v1',),j.scope_record_keys,(),j.provenance_row_coverage.denominator_name,'source-test')
    return j,s,records


def _s5_fixture(repo_root):
    p=repo_root/'tests/fixtures/provenance_partial/phase3_composition.json'
    raw=p.read_bytes();d=json.loads(raw)
    records=tuple(normalize_row({'dataset_version':'v1','record_id':i,'content':'synthetic'},kind='records') for i in d['record_ids'])
    rows=tuple(assess_provenance_row({'dataset_version':'v1',**v}) for v in d['provenance'])
    j=join_provenance(records,rows)
    s=CalculationScope(('v1',),j.scope_record_keys,(),j.provenance_row_coverage.denominator_name,'rational')
    return p,raw,d,j,s


def test_PR005_step5_rational_unweighted_fixture(repo_root):
    p,raw,d,j,s=_s5_fixture(repo_root);r=summarize_provenance(j,scope=s)
    assert dict(r.source.counts)==d['expected']['source_type_counts']
    assert dict(r.confidence.counts)==d['expected']['confidence_counts']
    assert dict(r.source.shares)=={k:float(Fraction(v)) for k,v in d['expected']['source_type_shares'].items()}
    assert r.analyzed_record_count.value==8 and r.records_with_matching_rows.value==7
    assert r.missing_provenance_share.value==1/8
    assert sum(dict(r.source.shares).values())+r.missing_provenance_share.value==1
    assert tuple(c.numerator for c in (r.provenance_row_coverage,r.provenance_required_field_coverage,r.grounding_field_coverage))==(7,7,6)
    direct=r.direct_grounding
    assert (direct.known_open_count.value,direct.known_closed_count.value,direct.unresolved_grounding_count.value)==(3,3,2)
    assert r.source.shares_metadata.formula_id=='F-007'
    assert r.source.counts_metadata.evidence_class is CalculationEvidenceClass.OBSERVED_FACT
    assert r.source.shares_metadata.evidence_class is CalculationEvidenceClass.DERIVED_METRIC
    assert p.read_bytes()==raw


def test_PR005_step5_unknown_and_missing_are_separate():
    j,s,_=_s5_case(({'source_type':'unknown'},None));r=summarize_provenance(j,scope=s)
    assert dict(r.source.counts)=={'human':0,'synthetic':0,'mixed':0,'sensor':0,'unknown':1}
    assert dict(r.source.shares)['unknown']==.5 and r.missing_provenance_share.value==.5
    assert r.source.status is CalculationStatus.AVAILABLE
    assert r.confidence.shares is None and r.confidence.shares_metadata is None


def test_PR005_step5_all_missing_and_manifest_absence_remain_explicit():
    j,s,records=_s5_case((None,None))
    a=summarize_provenance(join_provenance(records),scope=s);b=summarize_provenance(j,scope=s)
    assert not a.provenance_supplied and b.provenance_supplied
    assert sum(dict(a.source.counts).values())==0 and a.missing_provenance_share.value==1
    assert a.direct_grounding.unresolved_grounding_count.value==2
    assert not a.input_has_errors and len(a.validation_messages)==2


@pytest.mark.parametrize('field',['source_type','provenance_confidence','external_grounding'])
@pytest.mark.parametrize('form',['absent','null'])
def test_PR005_step5_incomplete_field_does_not_become_unknown(field,form):
    values={'dataset_version':'v1','record_id':'0','source_type':'human','provenance_confidence':'confirmed','external_grounding':'yes'}
    if form=='absent':del values[field]
    else:values[field]=None
    row=assess_provenance_row(values);_,s,records=_s5_case();j=join_provenance(records,(row,))
    r=summarize_provenance(j,scope=s)
    for name,table in [('source_type',r.source),('provenance_confidence',r.confidence)]:
        if field==name:
            assert table.status is CalculationStatus.UNAVAILABLE and table.counts is None and table.shares is None
            assert table.reason_codes==(CalculationReason.PROVENANCE_FIELD_UNAVAILABLE,)
            assert table.unavailable_record_keys==(RecordKey('v1','0'),) and table.field_coverage.numerator==0
        else:
            assert table.status is CalculationStatus.AVAILABLE and sum(dict(table.counts).values())==1
    assert r.input_has_errors and r.missing_provenance_count.value==0
    assert r.direct_grounding.unresolved_grounding_count.value==1
    assert r.validation_messages==j.messages and (field in row.values)==(form=='null')


def test_PR005_step5_weights_require_explicit_opt_in():
    j,s,_=_s5_case(({'source_type':'human'},{'source_type':'synthetic'}),record_fields={'weight':0})
    r=summarize_provenance(j,scope=s)
    assert r.weighted_source is None and dict(r.source.shares)['human']==.5
    with pytest.raises(CanonicalValidationError):summarize_provenance(j,scope=s,weights={k:1 for k in j.scope_record_keys})


def test_PR005_step5_weighted_rational_fixture_preserves_unweighted(repo_root):
    _,_,_,j,s=_s5_fixture(repo_root)
    p=repo_root/'tests/fixtures/weighted/phase3_source_weights.json';raw=p.read_bytes();d=json.loads(raw)
    unweighted=summarize_provenance(j,scope=s)
    r=summarize_provenance(j,scope=s,weighting=WeightingOptions('weighted','weight'),weights={RecordKey('v1',k):v for k,v in d['weights'].items()})
    assert r.source==unweighted.source and r.confidence==unweighted.confidence and r.direct_grounding==unweighted.direct_grounding
    w=r.weighted_source
    assert dict(w.weighted_source_type_masses)==d['masses'] and w.total_weight.value==36
    assert dict(w.weighted_source_type_shares)=={k:pytest.approx(float(Fraction(v)),abs=1e-12,rel=1e-12) for k,v in d['shares'].items()}
    assert w.weighted_missing_provenance_share.value==2/9 and w.missing_provenance_weight.value==8
    assert w.denominator_basis=='all_selected_record_weight_mass'
    assert w.shares_metadata.weighting==WeightingOptions('weighted','weight')
    assert sum(dict(w.weighted_source_type_shares).values())+w.weighted_missing_provenance_share.value==pytest.approx(1)
    assert p.read_bytes()==raw


@pytest.mark.parametrize('values',[(0,0),(-1,1),(True,1),(None,1),('1',1),(float('nan'),1),(float('inf'),1),(1e308,1e308),(5e-324,1e308),(10**1000,1),(Fraction(1),1)])
def test_PR005_step5_invalid_weights_rejected(values):
    j,s,_=_s5_case(({'source_type':'human'},None))
    with pytest.raises(CanonicalValidationError) as e:
        summarize_provenance(j,scope=s,weighting=WeightingOptions('weighted','weight'),weights=dict(zip(j.scope_record_keys,values)))
    assert e.value.code is ErrorCode.WEIGHT_INVALID


@pytest.mark.parametrize('weights',[None,{},[],{'0':1},{RecordKey('v1','0'):1},{RecordKey('v1','0'):1,RecordKey('v1','1'):1,RecordKey('v1','2'):1}])
def test_PR005_step5_weight_identity_scope_is_exact(weights):
    j,s,_=_s5_case(({'source_type':'human'},None))
    with pytest.raises(CanonicalValidationError):summarize_provenance(j,scope=s,weighting=WeightingOptions('weighted','weight'),weights=weights)


def test_PR005_step5_zero_weight_never_deletes_missingness():
    j,s,_=_s5_case(({'source_type':None},{'source_type':'human'}))
    r=summarize_provenance(j,scope=s,weighting=WeightingOptions('weighted','weight'),weights={RecordKey('v1','0'):0,RecordKey('v1','1'):1})
    assert r.weighted_source.status is CalculationStatus.UNAVAILABLE and r.weighted_source.weighted_source_type_shares is None
    assert r.weighted_source.total_weight.value==1 and r.input_has_errors
    assert r.source.counts is None and r.confidence.counts is not None
    assert r.analyzed_record_count.value==2


def test_PR005_step5_representation_exclusion_does_not_shrink_provenance():
    from recursive_integrity_toolkit.config import RepresentationConfig
    from recursive_integrity_toolkit.representations.field import assign_field_states
    j,s,records=_s5_case(({'source_type':'human'},None),record_fields={'topic':None})
    rep=assign_field_states(records,dataset_versions=('v1',),scope_id='excluded',config=RepresentationConfig('topic','topic_field','topic','v1','exclude'))
    r=summarize_provenance(j,scope=s)
    assert r.analyzed_record_count.value==2 and r.provenance_row_coverage.denominator==2
    with pytest.raises(CanonicalValidationError):summarize_provenance(j,scope=rep.scope)


def test_PR005_step5_determinism_detachment_and_weight_scaling():
    j,s,_=_s5_case(({'source_type':'human'},{'source_type':'synthetic'},None))
    w={k:i+1 for i,k in enumerate(j.scope_record_keys)};option=WeightingOptions('weighted','weight')
    a=summarize_provenance(j,scope=s,weighting=option,weights=w)
    b=summarize_provenance(replace(j,matches=tuple(reversed(j.matches)),scope_record_keys=tuple(reversed(j.scope_record_keys))),
        scope=replace(s,included_record_keys=tuple(reversed(s.included_record_keys))),weighting=option,weights=dict(reversed(tuple(w.items()))))
    c=summarize_provenance(j,scope=s,weighting=option,weights={k:v*10 for k,v in w.items()})
    assert a==b and a.source==c.source and a.direct_grounding==c.direct_grounding
    assert a.weighted_source.weighted_source_type_shares==c.weighted_source.weighted_source_type_shares
    w.clear();assert a.weighted_source.total_weight.value==6
    with pytest.raises((AttributeError,TypeError)):a.source.counts=()


def test_PR005_step5_trace_metadata_and_later_outputs_remain_absent():
    j,s,_=_s5_case(({'source_type':'human','external_grounding':'yes'},));r=summarize_provenance(j,scope=s)
    for scalar in (r.analyzed_record_count,r.records_with_matching_rows,r.missing_provenance_count,r.missing_provenance_share,
                   r.direct_grounding.known_open_count,r.direct_grounding.known_closed_count,r.direct_grounding.unresolved_grounding_count):
        m=scalar.metadata
        assert m.scope==r.scope and m.owner_id in ('PR-004','T3') and m.unit and m.method and m.assumptions and m.limitations
        assert m.representation is None and m.weighting.weighting_mode=='unweighted'
    for name in ('closure_bounds','lower_bound','upper_bound','confidence_score','effective_source_diversity','ancestry_hhi','maximum_level','report'):
        assert not hasattr(r,name) and not hasattr(r.direct_grounding,name)


def test_PR005_step5_no_io_network_callbacks_logging_or_second_join(monkeypatch,capsys,tmp_path):
    import builtins,socket
    from pathlib import Path
    import recursive_integrity_toolkit.io.validation as validation
    j,s,_=_s5_case(({'notes':'PRIVATE_SENTINEL','source_uri':'https://inert.invalid/private'},))
    def blocked(*a,**k):raise AssertionError('unexpected execution')
    with monkeypatch.context() as m:
        for name in ('open','eval','exec'):m.setattr(builtins,name,blocked)
        m.setattr(Path,'open',blocked);m.setattr(socket,'create_connection',blocked);m.setattr(socket,'getaddrinfo',blocked)
        m.setattr(validation,'join_provenance',blocked)
        r=summarize_provenance(j,scope=s)
    assert 'PRIVATE_SENTINEL' not in repr(r) and 'inert.invalid' not in repr(r)
    assert capsys.readouterr()==('','') and not list(tmp_path.iterdir())


def test_PR005_step5_input_only_hero_never_starts_metrics(repo_root,monkeypatch):
    import recursive_integrity_toolkit.metrics.provenance as module
    from recursive_integrity_toolkit.models import AuditBundle,InputSource,FileRole
    from recursive_integrity_toolkit.io.validation import validate_bundle
    def blocked(*a,**kw):raise AssertionError('input layer invoked metric')
    monkeypatch.setattr(module,'summarize_provenance',blocked);monkeypatch.setattr(module,'classify_direct_grounding',blocked)
    h=repo_root/'examples/hero';roles=(FileRole.RECORDS_PRIMARY,FileRole.RECORDS_COMPARE,FileRole.PROVENANCE_MANIFEST,FileRole.CONFIG,FileRole.VERSION_ORDER)
    names=('records_v1.csv','records_v2.csv','provenance.csv','config.json','version_order.json')
    result=validate_bundle(AuditBundle(tuple(InputSource(role,h/name) for role,name in zip(roles,names))))
    assert result.observability.maximum_level==4 and not result.has_errors
