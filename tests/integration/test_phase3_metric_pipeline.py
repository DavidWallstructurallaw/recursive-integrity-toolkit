"""Step 10 test-only composition of the frozen input and calculation layers.

No product dispatcher is created. Exact oracles stay in their approved files;
synthetic metamorphic/edge cases below are authored validation design.
"""
from dataclasses import replace
from fractions import Fraction
from pathlib import Path
import ast
import builtins
import hashlib
import importlib
import json
import runpy
import socket
import pytest

from recursive_integrity_toolkit.config import RepresentationConfig
from recursive_integrity_toolkit.errors import CanonicalValidationError
from recursive_integrity_toolkit.io.validation import validate_bundle, join_provenance
from recursive_integrity_toolkit.models import (
    AuditBundle, InputSource, FileRole, CalculationScope, CalculationStatus,
    CalculationEvidenceClass, CapabilityKey, CapabilityStatus, ContentMode,
    WeightingOptions, ExplicitPairContext, ScenarioParameters,
)
from recursive_integrity_toolkit.representations.field import assign_field_states
from recursive_integrity_toolkit.metrics.diversity import calculate_state_distribution, compare_support
from recursive_integrity_toolkit.metrics.provenance import summarize_provenance
from recursive_integrity_toolkit.metrics.bounds import direct_closure_exposure
from recursive_integrity_toolkit.metrics.duplicates import detect_exact_duplicates
from recursive_integrity_toolkit.metrics.resampling import expected_diversity_after_steps, simulate_closed_resampling


def _write(tmp_path, name, value, role):
    path = tmp_path / name
    raw = "\n".join(json.dumps(row) for row in value)+"\n" if name.endswith(".jsonl") else json.dumps(value)
    path.write_text(raw, encoding="utf-8")
    return InputSource(role, path)


def _case(tmp_path, *, partial=False, all_missing=False):
    # Source/mapping fixture deliberately preserves a leading-zero record ID.
    source = _write(tmp_path,"records.jsonl",[
        dict(id="0001",text="PRIVATE_SENTINEL",category="a",weight=1),
        dict(id="0002",text="different text",category=None,weight=3),
        dict(id="0003",text="PRIVATE_SENTINEL",category="unknown",weight=2),
        dict(id="0004",text="last text",category="a",weight=2),
    ],FileRole.RECORDS_PRIMARY)
    mapping = _write(tmp_path,"mapping.json",{"schema_version":"1.0","records":{"fields":{
        "record_id":{"source":"id"},"dataset_version":{"constant":"v1"},"content":{"source":"text"},
        "topic":{"source":"category"},"weight":{"source":"weight"}}}},FileRole.SCHEMA_MAPPING)
    if all_missing:
        return AuditBundle((source,mapping))
    rows = [dict(dataset_version="v1",record_id="0001",source_type="human",external_grounding="yes",provenance_confidence="confirmed"),
            dict(dataset_version="v1",record_id="0002",source_type="synthetic",external_grounding="no",provenance_confidence="confirmed"),
            dict(dataset_version="v1",record_id="0003",source_type="unknown",external_grounding="unknown",provenance_confidence="estimated")]
    if partial:
        del rows[1]["provenance_confidence"]
    provenance = _write(tmp_path,"provenance.jsonl",rows,FileRole.PROVENANCE_MANIFEST)
    return AuditBundle((source,mapping,provenance))


def _calculate(bundle):
    represented = assign_field_states(bundle.records,dataset_versions=("v1",),scope_id="mapped-topic",
        config=RepresentationConfig("topic","topic_field","topic","mapped-v1","exclude"))
    distribution = calculate_state_distribution(represented)
    joined = bundle.provenance_join
    scope = CalculationScope(("v1",),joined.scope_record_keys,(),joined.provenance_row_coverage.denominator_name,"mapped-provenance")
    composition = summarize_provenance(joined,scope=scope)
    bounds = direct_closure_exposure(composition)
    duplicates = detect_exact_duplicates(bundle.records,dataset_versions=("v1",),scope_id="mapped-exact",representation_name="record_form",
        representation_version="exact-v1",normalization_profile="exact_utf8_v1",content_mode=ContentMode.INLINE)
    return represented,distribution,composition,bounds,duplicates


def _files(root):
    return {p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob("*") if p.is_file()}


def test_phase3_mapping_to_metrics_preserves_raw_evidence_and_denominators(tmp_path):
    sources = _case(tmp_path)
    before = _files(tmp_path)
    bundle = validate_bundle(sources)
    represented,distribution,composition,bounds,duplicates = _calculate(bundle)
    assert [r.record_key.record_id for r in bundle.records] == ["0001","0002","0003","0004"]
    assert len(bundle.mapping_traces) == 4 and all(t.mapping_sha256 for t in bundle.mapping_traces)
    assert bundle.records[1].values["topic"] is None and bundle.records[2].values["topic"] == "unknown"
    assert distribution.coverage.numerator == 3 and distribution.coverage.denominator == 4
    assert distribution.unweighted.frequency_denominator == 3 and distribution.unweighted.support_size.value == 2
    assert distribution.unweighted.gini_simpson_diversity.value == pytest.approx(float(Fraction(4,9)))
    assert distribution.weighted is None
    assert composition.provenance_row_coverage.denominator == composition.analyzed_record_count.value == 4
    assert dict(composition.source.shares) == dict(human=.25,synthetic=.25,mixed=0.,sensor=0.,unknown=.25)
    assert composition.missing_provenance_share.value == .25
    assert (bounds.lower_bound.value,bounds.upper_bound.value,bounds.interval_width.value) == (.25,.75,.5)
    assert duplicates.duplicate_record_count.value == duplicates.duplicate_group_count.value == 1
    assert len(bundle.records) == 4 and len(represented.scope.excluded_record_keys) == 1
    assert before == _files(tmp_path)


def test_phase3_error_bearing_partial_input_cannot_become_silent_success(tmp_path):
    bundle = validate_bundle(_case(tmp_path,partial=True))
    assert bundle.has_errors
    represented,distribution,composition,bounds,duplicates = _calculate(bundle)
    assert distribution.unweighted.status is CalculationStatus.AVAILABLE
    assert composition.confidence.status is CalculationStatus.UNAVAILABLE and composition.confidence.counts is None
    assert composition.input_has_errors and bounds.input_has_errors
    assert bounds.validation_messages == composition.validation_messages
    assert bounds.status is CalculationStatus.AVAILABLE
    assert (bounds.lower_bound.value,bounds.upper_bound.value,bounds.interval_width.value) == (0.,.75,.75)
    assert any(m.field == "provenance_confidence" for m in bounds.validation_messages)
    assert len(bundle.records) == 4


def test_phase3_no_provenance_is_disclosed_separately_from_unknown(tmp_path):
    bundle = validate_bundle(_case(tmp_path,all_missing=True))
    _,distribution,composition,bounds,_ = _calculate(bundle)
    assert distribution.unweighted.support_size.value == 2
    assert composition.missing_provenance_share.value == 1
    assert dict(composition.source.counts)["unknown"] == 0
    assert bounds.status is CalculationStatus.UNAVAILABLE
    assert all(v.value is None and v.reason_codes for v in (bounds.lower_bound,bounds.upper_bound,bounds.interval_width))


def test_phase3_explicit_weighting_retains_unweighted_and_separate_scopes(tmp_path):
    bundle = validate_bundle(_case(tmp_path))
    represented,plain,composition,_,_ = _calculate(bundle)
    weights = {r.record_key:r.values["weight"] for r in bundle.records}
    selected = {k:weights[k] for k in represented.scope.included_record_keys}
    weighted = calculate_state_distribution(represented,weighting=WeightingOptions("weighted","weight"),weights=selected)
    weighted_source = summarize_provenance(bundle.provenance_join,scope=composition.scope,weighting=WeightingOptions("weighted","weight"),weights=weights)
    assert weighted.unweighted == plain.unweighted
    assert weighted.weighted.frequency_denominator == 5
    assert weighted_source.source == composition.source
    assert weighted_source.weighted_source.total_weight.value == 8
    assert len(bundle.records) == 4


def test_phase3_hero_explicit_scenarios_remain_separate_from_observed_pair(phase3_hero_pipeline):
    result = phase3_hero_pipeline()
    pair = result["pair"]
    assert result["config"].simulation.enabled is False
    for version,expected in (("v1",Fraction(49,64)),("v2",Fraction(21,32))):
        distribution = result["distributions"][version].unweighted
        probabilities = tuple((s.state_id,s.state_frequency) for s in distribution.states)
        expectation = expected_diversity_after_steps(probabilities,resample_size=8,steps=1,
            scope=distribution.scope,representation=distribution.representation)
        assert expectation.expected_diversity[1] == pytest.approx(float(expected),abs=1e-12,rel=1e-12)
        sampled = simulate_closed_resampling(probabilities,resample_size=8,steps=2,seed=19,replicates=2,
            scope=distribution.scope,representation=distribution.representation)
        assert expectation.evidence_class is sampled.evidence_class is CalculationEvidenceClass.SIMULATION
        assert expectation.random_seed is None and sampled.random_seed == 19
        for path in sampled.sampled_paths:
            assert all(sum(g.state_counts) == 8 for g in path.generations[1:])
    assert result["pair"] == pair and pair.gini_simpson_diversity_delta.metadata.evidence_class is CalculationEvidenceClass.DERIVED_METRIC
    assert len(result["bundle"].records) == 16


@pytest.mark.parametrize("enabled",[False,True])
def test_phase3_validation_never_dispatches_metrics_even_when_enabled(tmp_path,monkeypatch,enabled):
    sources = _case(tmp_path)
    def blocked(*args,**kwargs):
        raise AssertionError("validation invoked a metric or scenario")
    names = {
        "diversity":("calculate_state_distribution","distribution_from_counts","distribution_from_probabilities","compare_support"),
        "provenance":("summarize_provenance","classify_direct_grounding"),"bounds":("direct_closure_exposure","closure_exposure_bounds"),
        "duplicates":("detect_exact_duplicates",),"tail":("select_tail","one_step_extinction_probability"),
        "resampling":("expected_diversity_after_steps","simulate_closed_resampling"),
    }
    for module,functions in names.items():
        loaded = importlib.import_module("recursive_integrity_toolkit.metrics."+module)
        for name in functions:
            monkeypatch.setattr(loaded,name,blocked)
    config = {"simulation":{"enabled":enabled,"seed":19},
              "representation":{"name":"topic","source":"topic_field","field":"topic","version":"mapped-v1","missing_value_policy":"exclude"}}
    params = ScenarioParameters("closed_resampling",resample_size=4,simulation_horizon=1,simulation_replicates=2,
                               state_distribution=(("a",.5),("b",.5)))
    bundle = validate_bundle(sources,configuration=config,scenario_parameters=params)
    assert len(bundle.records) == 4
    assert not hasattr(bundle,"simulation_results")
    capability = bundle.observability.capabilities[CapabilityKey.INTERVENTION_SIMULATION]
    if enabled:
        assert capability.status is CapabilityStatus.EXPERIMENTAL
        assert "R_SCENARIO_EXECUTION_DEFERRED" in capability.reason_codes
    else:
        assert capability.status is CapabilityStatus.UNAVAILABLE


def test_phase3_metric_stage_has_no_io_dynamic_execution_or_protected_imports(tmp_path,monkeypatch,capsys):
    bundle = validate_bundle(_case(tmp_path,partial=True))
    before = _files(tmp_path)
    original_import = builtins.__import__
    def checked_import(name,*args,**kwargs):
        assert not name.startswith(("recursive_integrity_toolkit.reports","recursive_integrity_toolkit.lineage"))
        return original_import(name,*args,**kwargs)
    def blocked(*args,**kwargs):
        raise AssertionError("calculation attempted forbidden side effect")
    with monkeypatch.context() as patch:
        for name in ("open","eval","exec"):
            patch.setattr(builtins,name,blocked)
        patch.setattr(builtins,"__import__",checked_import)
        patch.setattr(Path,"open",blocked)
        patch.setattr(socket,"create_connection",blocked)
        patch.setattr(socket,"getaddrinfo",blocked)
        results = _calculate(bundle)
    assert capsys.readouterr() == ("","")
    assert "PRIVATE_SENTINEL" not in repr(results)
    assert _files(tmp_path) == before


def test_phase3_hero_source_and_oracle_bytes_are_not_rewritten(repo_root,phase3_hero_pipeline):
    paths = [repo_root/"PHASE_0_APPROVAL.md",repo_root/"PHASE_3_PLAN.md"]
    paths += list((repo_root/"examples/hero").glob("*"))
    paths += list((repo_root/"schemas").glob("*.json"))
    paths += [repo_root/"tests/golden/phase3_math_cases.json",repo_root/"tests/golden/phase3_math_cases.md"]
    before = {p:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths if p.is_file()}
    result = phase3_hero_pipeline()
    assert before == {p:hashlib.sha256(p.read_bytes()).hexdigest() for p in before}
    assert len(result["bundle"].records) == 16
    assert not any((repo_root/name).exists() for name in ("hero_report.json","hero_report.md","lineage_report.json","cycle_report.json"))


@pytest.mark.parametrize("module",["lineage/graph.py","lineage/cycles.py","lineage/ancestry.py","reports/assembly.py","reports/json_report.py","reports/markdown_report.py","reports/html_report.py","result.py"])
def test_phase3_later_implementations_remain_empty(package_root,module):
    tree = ast.parse((package_root/module).read_bytes())
    assert len(tree.body) == 1 and isinstance(tree.body[0],ast.Expr) and isinstance(tree.body[0].value,ast.Constant)
    assert isinstance(tree.body[0].value.value,str)


@pytest.mark.parametrize("path",[
    "src/recursive_integrity_toolkit/metrics/diversity.py",
    "src/recursive_integrity_toolkit/metrics/provenance.py",
    "src/recursive_integrity_toolkit/io/validation.py",
    "src/recursive_integrity_toolkit/reports/assembly.py",
    "src/recursive_integrity_toolkit/cli.py",
    "tests/unit/test_T1_compatibility.py","tests/unit/test_phase3_contracts.py",
    "PHASE_3_PLAN.md","DEFINITIONS_AND_UNITS.md","pyproject.toml",
    "examples/hero/EXPECTED_OUTPUTS.md","schemas/report.schema.json",
])
def test_phase3_step10_rejects_unopened_file_changes(repo_root,path):
    gate = runpy.run_path(str(repo_root/"scripts/release_check.py"))
    with pytest.raises(ValueError):
        gate["verify_prior_step_changes"]([("M",path)],step=10)


def test_phase3_step10_scope_is_fixed_not_self_authorized(repo_root,phase3_step10_snapshot):
    gate = runpy.run_path(str(repo_root/"scripts/release_check.py"))
    control = json.loads((phase3_step10_snapshot/"PHASE_3_BASELINE.json").read_bytes())
    gate["verify_step10_control"](control)
    assert gate["PHASE3_STEP10_NEW"] == {"tests/integration/test_phase3_metric_pipeline.py","tests/golden/test_phase3_math.py"}
    assert not any(p.startswith("src/") for p in gate["PHASE3_STEP10_ALLOWED"])
    for key,value in (("active_step",11),("previous_step_commit","0"*40),("phase_complete",True),("main_merge_authorized",True)):
        altered = dict(control,**{key:value})
        with pytest.raises(ValueError):
            gate["verify_step10_control"](altered)
    altered = dict(control,permitted_paths=control["permitted_paths"]+["src/new.py"])
    with pytest.raises(ValueError):
        gate["verify_step10_control"](altered)
    assert gate["verify_step10_snapshot"](phase3_step10_snapshot)["runtime_modules_unchanged"] == 40


@pytest.mark.parametrize("path",["src/recursive_integrity_toolkit/metrics/diversity.py","tests/golden/phase3_math_cases.json","examples/hero/records_v2.csv","pyproject.toml"])
def test_phase3_step10_snapshot_rejects_byte_changes(repo_root,tmp_path,path,phase3_step10_snapshot):
    import shutil
    gate = runpy.run_path(str(repo_root/"scripts/release_check.py"))
    shutil.copytree(phase3_step10_snapshot/"src/recursive_integrity_toolkit",tmp_path/"src/recursive_integrity_toolkit",ignore=shutil.ignore_patterns("__pycache__"))
    for name in gate["STEP10_FROZEN_FILES"]:
        target = tmp_path/name
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes((phase3_step10_snapshot/name).read_bytes())
    gate["verify_step10_snapshot"](tmp_path)
    target = tmp_path/path
    target.write_bytes(target.read_bytes()+b"\n")
    with pytest.raises(ValueError):
        gate["verify_step10_snapshot"](tmp_path)


def _synthetic_evidence(repo_root,tmp_path,change=None):
    # Synthetic XML solely for testing the evidence validator, never run evidence.
    import xml.etree.ElementTree as ET
    root = ET.Element("testsuites")
    suite = ET.SubElement(root,"testsuite",tests="21",failures="0",errors="0",skipped="0")
    cases = json.loads((repo_root/"tests/golden/phase3_math_cases.json").read_bytes())["cases"]
    for c in cases:
        ET.SubElement(suite,"testcase",classname="tests.golden.test_phase3_math",name="test_phase3_frozen_case["+c["case_id"]+"]")
    test = ET.SubElement(suite,"testcase",classname="synthetic",name="synthetic_performance_evidence")
    properties = ET.SubElement(test,"properties")
    names = ["hero_input_plus_calculations","metadata_100k_setup","metadata_100k_field_representation","metadata_100k_support_diversity",
             "metadata_100k_provenance_join","metadata_100k_composition","metadata_100k_exact_duplicates"]
    for name in names:
        d = dict(name=name,elapsed_seconds=0.0,traced_current_bytes=0,traced_peak_bytes=0,
            record_count=16 if name.startswith("hero") else 100000,whole_product_report_target_certified=False,
            memory_method="synthetic validator test",timing_method="synthetic validator test",python="synthetic",platform="synthetic")
        if change and name == names[-1]:
            d.update(change)
        ET.SubElement(properties,"property",name="phase3_performance",value=json.dumps(d))
    path = tmp_path/"synthetic-evidence.xml"
    ET.ElementTree(root).write(path,encoding="utf-8")
    return path


@pytest.mark.parametrize("change",[{"elapsed_seconds":-1},{"elapsed_seconds":True},{"traced_peak_bytes":float("nan")},
    {"record_count":1000},{"whole_product_report_target_certified":True},{"memory_method":""},{"name":"metadata_100k_setup"}])
def test_phase3_step10_rejects_invalid_performance_evidence(repo_root,tmp_path,change):
    gate = runpy.run_path(str(repo_root/"scripts/release_check.py"))
    with pytest.raises(ValueError):
        gate["verify_step10_evidence"](_synthetic_evidence(repo_root,tmp_path,change))


def test_phase3_step10_evidence_requires_executed_cases_and_all_measurements(repo_root,tmp_path):
    import xml.etree.ElementTree as ET
    gate = runpy.run_path(str(repo_root/"scripts/release_check.py"))
    path = _synthetic_evidence(repo_root,tmp_path)
    assert gate["verify_step10_evidence"](path)["frozen_cases_executed"] == 20
    tree = ET.parse(path)
    suite = tree.getroot().find("testsuite")
    suite.remove(suite.find("testcase"))
    tree.write(path)
    with pytest.raises(ValueError):
        gate["verify_step10_evidence"](path)
    path = _synthetic_evidence(repo_root,tmp_path)
    tree = ET.parse(path)
    props = tree.getroot().find(".//properties")
    props.remove(props.find("property"))
    tree.write(path)
    with pytest.raises(ValueError):
        gate["verify_step10_evidence"](path)


@pytest.mark.parametrize("path",[
    "src/recursive_integrity_toolkit/metrics/diversity.py",
    "src/recursive_integrity_toolkit/models.py",
    "src/recursive_integrity_toolkit/io/validation.py",
    "src/recursive_integrity_toolkit/cli.py",
    "tests/unit/test_T1_compatibility.py",
    "tests/golden/phase3_math_cases.json",
    "tests/golden/phase3_math_cases.md",
    "PHASE_3_PLAN.md","PHASE_2_COMPLETION.md",
    "schemas/report.schema.json","examples/hero/EXPECTED_OUTPUTS.md",
])
def test_phase3_step11_rejects_unopened_changes(repo_root,path):
    gate = runpy.run_path(str(repo_root/"scripts/release_check.py"))
    with pytest.raises(ValueError):
        gate["verify_phase3_changes"]([("M",path)],incremental=True)


def test_phase3_step11_control_and_new_files_are_fixed(repo_root):
    gate = runpy.run_path(str(repo_root/"scripts/release_check.py"))
    control = json.loads((repo_root/"PHASE_3_BASELINE.json").read_bytes())
    gate["verify_phase3_control"](control,11)
    assert gate["PHASE3_STEP11_NEW"] == {"PHASE_3_COMPLETION.md","PHASE_3_VALIDATION_REPORT.md","PHASE_3_ARCHITECTURE_COMPLIANCE_REPORT.md"}
    assert gate["STEP11_TEST_EXCEPTIONS"] == {"tests/unit/test_phase3_contracts.py","tests/integration/test_phase3_metric_pipeline.py"}
    for key,value in (("active_step",12),("phase_complete",not control["phase_complete"]),
                      ("previous_step_commit","0"*40),("next_step_authorized",True),
                      ("main_merge_authorized",True),("publication_authorized",True)):
        with pytest.raises(ValueError):
            gate["verify_phase3_control"](dict(control,**{key:value}),11)
    for status,path in (("A","src/new.py"),("A","tests/unit/test_phase3_contracts.py"),
                        ("D","README.md"),("R100","docs/privacy.md")):
        with pytest.raises(ValueError):
            gate["verify_phase3_changes"]([(status,path)],incremental=True)


@pytest.mark.parametrize("path",[
    "src/recursive_integrity_toolkit/__init__.py",
    "src/recursive_integrity_toolkit/metrics/resampling.py",
    "pyproject.toml","tests/golden/phase3_math_cases.json",
])
def test_phase3_step11_rejects_changes_beyond_version_literals(repo_root,tmp_path,path):
    import shutil
    gate = runpy.run_path(str(repo_root/"scripts/release_check.py"))
    shutil.copytree(repo_root/"src/recursive_integrity_toolkit",tmp_path/"src/recursive_integrity_toolkit",ignore=shutil.ignore_patterns("__pycache__"))
    for name in gate["STEP10_FROZEN_FILES"]:
        target = tmp_path/name
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes((repo_root/name).read_bytes())
    assert gate["verify_step11_snapshot"](tmp_path)["approved_version_literals"] == 2
    target = tmp_path/path
    original = target.read_bytes()
    for altered in (original+b"\n", original.replace(b"0.1.0.dev2",b"0.1.0.dev3")):
        if altered == original:
            continue
        target.write_bytes(altered)
        with pytest.raises(ValueError):
            gate["verify_step11_snapshot"](tmp_path)


def test_phase3_step11_test_exceptions_are_exact(repo_root,phase3_step10_snapshot):
    gate = runpy.run_path(str(repo_root/"scripts/release_check.py"))
    unit = "tests/unit/test_phase3_contracts.py"
    pipeline = "tests/integration/test_phase3_metric_pipeline.py"
    for name,verify in ((unit,gate["verify_step11_contract_test_migration"]),
                        (pipeline,gate["verify_step11_pipeline_test_migration"])):
        before = (phase3_step10_snapshot/name).read_bytes()
        current = (repo_root/name).read_bytes()
        verify(before,current)
        with pytest.raises(ValueError):
            verify(before,b"# unauthorized inherited edit\n"+current)
        with pytest.raises(ValueError):
            verify(before,current+b"\nFORGED_TEST = True\n")
