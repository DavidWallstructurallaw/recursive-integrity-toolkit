"""Step 10 Hero input-plus-calculation observation; report layers remain absent."""
from fractions import Fraction
import hashlib


def test_phase3_hero_input_and_calculation_runtime(phase3_hero_pipeline, phase3_measure, repo_root):
    hero = repo_root / "examples/hero"
    before = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in hero.iterdir() if p.is_file()}
    result = phase3_measure("hero_input_plus_calculations", phase3_hero_pipeline, record_count=16,
        includes="input loading/validation, representation, single-version metrics, provenance, direct bounds, exact duplicates, tail and explicit pair",
        excludes="JSON/Markdown report assembly, redaction, audit CLI, lineage, simulation")
    assert result["pair"].support_delta.value == -3
    assert result["pair"].support_retention_ratio.value == float(Fraction(5, 8))
    assert result["bundle"].observability.maximum_level == 4 and not result["bundle"].has_errors
    assert before == {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in hero.iterdir() if p.is_file()}
