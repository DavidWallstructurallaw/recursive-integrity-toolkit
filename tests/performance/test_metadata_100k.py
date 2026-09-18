"""Step 10 measured 100k calculation paths, with synthetic independent oracles.

Performance observations are diagnostics, not a whole-report SLA. Synthetic input
construction is recorded separately. No user data or sparse lineage is involved.
"""
from fractions import Fraction
import sys
import pytest

from recursive_integrity_toolkit.config import RepresentationConfig
from recursive_integrity_toolkit.io.normalization import normalize_row
from recursive_integrity_toolkit.io.validation import join_provenance
from recursive_integrity_toolkit.metrics.diversity import calculate_state_distribution
from recursive_integrity_toolkit.metrics.duplicates import detect_exact_duplicates
from recursive_integrity_toolkit.metrics.provenance import summarize_provenance
from recursive_integrity_toolkit.models import CalculationScope, ContentMode
from recursive_integrity_toolkit.representations.field import assign_field_states


def _synthetic(size):
    records = tuple(normalize_row(dict(dataset_version="synthetic-v1", record_id=f"r{i:06d}",
        content=f"synthetic text {i % 1000:04d}", topic=f"state-{i % 100:03d}"), kind="records") for i in range(size))
    provenance = tuple(normalize_row(dict(dataset_version="synthetic-v1", record_id=f"r{i:06d}",
        source_type="human" if i % 2 == 0 else "synthetic", provenance_confidence="confirmed",
        external_grounding="yes" if i % 2 == 0 else "no"), kind="provenance") for i in range(size))
    return records, provenance


def _duplicates(records):
    return detect_exact_duplicates(records, dataset_versions=("synthetic-v1",), scope_id="100k-exact",
        representation_name="record_form", representation_version="exact-v1", normalization_profile="exact_utf8_v1", content_mode=ContentMode.INLINE)


def test_phase3_metadata_100k_measured_calculations(phase3_measure):
    size = 100000
    records, provenance = phase3_measure("metadata_100k_setup", lambda: _synthetic(size), record_count=size, purpose="synthetic normalization only")
    before = tuple((r.record_key, tuple(r.values.items())) for r in records)
    representation = phase3_measure("metadata_100k_field_representation", lambda: assign_field_states(records,
        dataset_versions=("synthetic-v1",), scope_id="100k-topic",
        config=RepresentationConfig("topic", "topic_field", "topic", "synthetic-topic-v1", "error")), record_count=size)
    distribution = phase3_measure("metadata_100k_support_diversity", lambda: calculate_state_distribution(representation), record_count=size)
    # Authored independent exact oracle: 100 equiprobable states, 1000 records each.
    assert distribution.unweighted.support_size.value == 100
    assert all(s.state_count == 1000 and s.state_frequency == .01 for s in distribution.unweighted.states)
    assert abs(distribution.unweighted.gini_simpson_diversity.value - float(Fraction(99, 100))) <= 1e-12
    joined = phase3_measure("metadata_100k_provenance_join", lambda: join_provenance(records, provenance), record_count=size)
    scope = CalculationScope(("synthetic-v1",), joined.scope_record_keys, (), joined.provenance_row_coverage.denominator_name, "100k-provenance")
    composition = phase3_measure("metadata_100k_composition", lambda: summarize_provenance(joined, scope=scope), record_count=size)
    assert dict(composition.source.counts) == dict(human=50000, synthetic=50000, mixed=0, sensor=0, unknown=0)
    assert dict(composition.source.shares) == dict(human=.5, synthetic=.5, mixed=0., sensor=0., unknown=0.)
    assert composition.provenance_required_field_coverage.numerator == size and not composition.input_has_errors
    duplicates = phase3_measure("metadata_100k_exact_duplicates", lambda: _duplicates(records), record_count=size)
    # 1000 exact forms, each appearing 100 times: 1000*(100-1) duplicates.
    assert duplicates.duplicate_group_count.value == 1000 and duplicates.duplicate_record_count.value == 99000
    assert len(records) == len(provenance) == size
    assert before == tuple((r.record_key, tuple(r.values.items())) for r in records)


@pytest.mark.parametrize("pattern", ["same", "unique", "groups"])
def test_phase3_duplicate_path_operation_growth_is_not_quadratic(pattern):
    """Count actual Python line events, independent of noisy wall-clock ratios.

    This regression covers current duplicate/representation/key code paths. It
    complements review of bucket grouping; it is not a proof for every input.
    """
    measurements = []
    for size in (256, 1024):
        rows = tuple(normalize_row(dict(dataset_version="synthetic-v1", record_id=f"r{i:06d}",
            content=("same synthetic payload" if pattern == "same" else f"synthetic payload {i if pattern == 'unique' else i % 16}")), kind="records") for i in range(size))
        counter = [0]
        def trace(frame, event, arg):
            if event == "line" and "recursive_integrity_toolkit" in frame.f_code.co_filename:
                counter[0] += 1
            return trace
        previous = sys.gettrace()
        try:
            sys.settrace(trace)
            result = _duplicates(rows)
        finally:
            sys.settrace(previous)
        assert result.duplicate_record_count.value == size - (1 if pattern == "same" else size if pattern == "unique" else 16)
        measurements.append(counter[0])
    assert 0 < measurements[0] < measurements[1]
    assert measurements[1] <= 6 * measurements[0], measurements
