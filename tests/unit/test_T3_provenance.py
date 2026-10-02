"""T3 Phase 3 Step 5 tests. Earlier Phase 2 checks are preserved.

Only declared composition, inherited coverage and direct classifications are
active. No closure interval, confidence score or report is produced.
"""


# Direct declaration-bound input basis only; no intervals or graph traversal.
import json
import pytest
from recursive_integrity_toolkit.io.normalization import normalize_row
from recursive_integrity_toolkit.io.validation import assess_provenance_row,join_provenance
from recursive_integrity_toolkit.models import CalculationScope,CalculationEvidenceClass
from recursive_integrity_toolkit.metrics.provenance import classify_direct_grounding,summarize_provenance


def _t5_basis(fields):
    r=normalize_row({'dataset_version':'v1','record_id':'a','content':'synthetic'},kind='records')
    p=assess_provenance_row({'dataset_version':'v1','record_id':'a','source_type':'human','provenance_confidence':'confirmed','external_grounding':'yes',**fields})
    j=join_provenance((r,),(p,));s=CalculationScope(('v1',),j.scope_record_keys,(),j.provenance_row_coverage.denominator_name,'grounding')
    return classify_direct_grounding(j,scope=s),j,s


@pytest.mark.parametrize('source',['human','synthetic','mixed','sensor','unknown'])
@pytest.mark.parametrize('grounding,expected',[('yes','known_open'),('no','known_closed'),('unknown','unresolved_grounding')])
@pytest.mark.parametrize('review',[True,False,None])
def test_T3_step5_crossed_declarations_independent(source,grounding,expected,review):
    r,j,s=_t5_basis({'source_type':source,'external_grounding':grounding,'human_reviewed':review})
    assert r.assignments[0].classification==expected and r==summarize_provenance(j,scope=s).direct_grounding
    counts=(r.known_open_count,r.known_closed_count,r.unresolved_grounding_count)
    assert sum(c.value for c in counts)==1
    assert all(c.metadata.evidence_class is CalculationEvidenceClass.OBSERVED_FACT for c in counts)
    assert r.classification_basis=='toolkit_operationalization'


@pytest.mark.parametrize('confidence',['confirmed','log_derived','estimated','unknown'])
@pytest.mark.parametrize('grounding,expected',[('yes','known_open'),('no','known_closed'),('unknown','unresolved_grounding')])
def test_T3_step5_confidence_never_discounts_grounding(confidence,grounding,expected):
    r,j,_=_t5_basis({'provenance_confidence':confidence,'external_grounding':grounding})
    assert r.assignments[0].classification==expected
    assert j.matches[0].provenance.values['provenance_confidence']==confidence


@pytest.mark.parametrize('field',['source_type','provenance_confidence'])
@pytest.mark.parametrize('grounding',['yes','no'])
def test_T3_step5_invalid_required_row_remains_unresolved(field,grounding):
    r,j,_=_t5_basis({field:None,'external_grounding':grounding})
    assert r.input_has_errors and r.unresolved_grounding_count.value==1
    assert r.assignments[0].basis=='incomplete_required_provenance' and r.assignments[0].missing_required_fields==(field,)
    assert j.grounding_field_coverage.ratio==1


def test_T3_step5_never_traverses_parents_or_infers_generator():
    plain,_,_=_t5_basis({})
    declared,_,_=_t5_basis({'parent_ids':['v1::a','unresolved'],'generator_id':'same-family',
        'generation':99,'transformation':'carryover','human_reviewed':False})
    assert plain==declared
    assert not hasattr(declared,'root_count') and not hasattr(declared,'lower_bound')


def test_T3_step5_independent_crossed_fixture(repo_root):
    p=repo_root/'tests/fixtures/provenance_unknown/phase3_grounding_crossed.json';raw=p.read_bytes();d=json.loads(raw)
    for source in d['sources']:
        for grounding,expected in d['grounding_to_class'].items():
            for review in d['review_values']:
                r,_,_=_t5_basis({'source_type':source,'external_grounding':grounding,'human_reviewed':review})
                assert r.assignments[0].classification==expected
    assert p.read_bytes()==raw


# Step 6 bridge only; all previous classification tests remain unchanged.
def test_T3_step6_grounding_declarations_alone_restore_stronger_bounds():
    from recursive_integrity_toolkit.metrics.bounds import direct_closure_exposure
    for source in ('human','synthetic','mixed','sensor','unknown'):
        for review in (True,False,None):
            for grounding,expected in (('yes',(0,0)),('no',(1,1)),('unknown',(0,1))):
                _,j,s=_t5_basis({'source_type':source,'human_reviewed':review,'external_grounding':grounding})
                x=direct_closure_exposure(summarize_provenance(j,scope=s))
                assert (x.lower_bound.value,x.upper_bound.value)==expected


def test_T3_step6_input_workflow_does_not_invoke_bounds(repo_root,monkeypatch):
    from recursive_integrity_toolkit.io.validation import validate_bundle
    from recursive_integrity_toolkit.models import AuditBundle,InputSource,FileRole
    import recursive_integrity_toolkit.metrics.bounds as bounds
    def blocked(*args,**kwargs):raise AssertionError('input layer called direct bounds')
    monkeypatch.setattr(bounds,'direct_closure_exposure',blocked)
    monkeypatch.setattr(bounds,'closure_exposure_bounds',blocked)
    roles=(FileRole.RECORDS_PRIMARY,FileRole.RECORDS_COMPARE,FileRole.PROVENANCE_MANIFEST,FileRole.CONFIG,FileRole.VERSION_ORDER)
    names=('records_v1.csv','records_v2.csv','provenance.csv','config.json','version_order.json')
    h=repo_root/'examples/hero'
    x=validate_bundle(AuditBundle(tuple(InputSource(role,h/name) for role,name in zip(roles,names))))
    assert x.observability.maximum_level==4 and not x.has_errors
