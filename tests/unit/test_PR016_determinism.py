"""PR-016 lexical order retained; Step 8 seeded determinism has explicit boundaries."""

import ast
from itertools import permutations
import pytest

from recursive_integrity_toolkit.io.normalization import normalize_row
from recursive_integrity_toolkit.utils.ordering import stable_record_order


def _row(version, identity):
    return normalize_row({"dataset_version": version, "record_id": identity, "content": "synthetic"},
                         kind="records")


def test_PR016_ordering_owner_and_no_later_behavior(owner_checker, package_root, placeholder_checker,phase3_final_placeholder_checker):
    placeholder_checker = phase3_final_placeholder_checker
    owner_checker("utils/ordering.py", "PR-016")
    tree = ast.parse((package_root / "utils/ordering.py").read_text())
    names = {node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}
    assert names == {"_record_order_key", "stable_record_order"}
    for path in ["reports/json_report.py", "reports/markdown_report.py"]:
        placeholder_checker(path)
    # The authorized shared module is checked against its exact reviewed body.
    import runpy
    checker = runpy.run_path(str(package_root.parents[1] / "scripts/check_traceability.py"))
    source = (package_root / "metrics/resampling.py").read_text(encoding="utf-8")
    checker["_phase3_resampling_boundary"](ast.parse(source))


def test_PR016_stable_exact_lexical_order_is_not_version_chronology():
    rows = (_row("v2", "a"), _row("v10", "b"), _row("v1", "0001"))
    expected = (rows[2], rows[1], rows[0])
    for permutation in permutations(rows):
        assert stable_record_order(permutation) == expected
    assert rows[0].record_key.dataset_version == "v2"


def test_PR016_ordering_does_not_drop_repeated_rows():
    row = _row("v1", "a")
    assert stable_record_order((row, row)) == (row, row)


@pytest.mark.parametrize("rows", [[], ("invalid",)])
def test_PR016_only_canonical_tuple_rows_accepted(rows):
    with pytest.raises(TypeError):
        stable_record_order(rows)


# Phase 4 Step 4 additive acceptance: calculation determinism and privacy scope
# are distinct; these cases do not normalize identity/configuration meaning.


def test_phase4_step4_PR016_hmac_independent_vector_and_domain_framing():
    from recursive_integrity_toolkit.utils.hashing import IdentifierProtection, canonical_json_bytes

    protection = IdentifierProtection.create(secret=bytes(range(32)))
    assert protection.pseudonym("record_id", ["v1", "record"]) == (
        "hmac-sha256:cbc01ccb4e2ef82415c51ac3b2e05f9df5b5bb82cc60997becf3de82a8ee08db")
    assert canonical_json_bytes({"z": [True, 1, 1.0], "a": "é"}) == b'{"a":"\\u00e9","z":[true,1,1.0]}'
    assert protection.pseudonym("record_id", ["a::b", "c"]) != protection.pseudonym("record_id", ["a", "b::c"])
    assert protection.pseudonym("record_id", "same") != protection.pseudonym("dataset_version", "same")
    assert protection.pseudonym("state_id", True) != protection.pseudonym("state_id", 1)
    assert protection.pseudonym("state_id", {"a": 1, "b": 2}) == protection.pseudonym("state_id", {"b": 2, "a": 1})


def test_phase4_step4_PR016_fresh_keys_are_unlinkable_and_injected_keys_repeat():
    from recursive_integrity_toolkit.utils.hashing import IdentifierProtection

    first, second = IdentifierProtection.create(), IdentifierProtection.create()
    assert first.pseudonym("state_id", "s") == first.pseudonym("state_id", "s")
    assert first.pseudonym("state_id", "s") != second.pseudonym("state_id", "s")
    assert first.stability_scope == second.stability_scope == "run"
    assert first.secret_source == second.secret_source == "fresh"
    injected = IdentifierProtection.create(secret=b"TEST-ONLY-PRIVATE-KEY-123456789012")
    same = IdentifierProtection.create(secret=b"TEST-ONLY-PRIVATE-KEY-123456789012")
    assert injected.pseudonym("record_id", ["v", "r"]) == same.pseudonym("record_id", ["v", "r"])
    assert injected.stability_scope == "run" and injected.secret_source == "injected"
    assert injected.algorithm == "HMAC-SHA-256"
    assert "PRIVATE-KEY" not in repr(injected)


def test_phase4_step4_PR016_secret_file_declares_cross_run_without_retaining_path(tmp_path):
    from recursive_integrity_toolkit.utils.hashing import IdentifierProtection

    secret = b"PRIVATE-KEY-CONTENT-123456789012345\r\n"
    key_file = tmp_path / "PRIVATE-SECRET-PATH"
    key_file.write_bytes(secret)
    first = IdentifierProtection.create(secret_file=key_file)
    second = IdentifierProtection.create(secret_file=key_file)
    injected = IdentifierProtection.create(secret=secret)
    assert first.stability_scope == second.stability_scope == "cross_run"
    assert first.secret_source == "local_file"
    assert first.pseudonym("dataset_version", "v") == second.pseudonym("dataset_version", "v")
    assert first.pseudonym("dataset_version", "v") == injected.pseudonym("dataset_version", "v")
    assert "PRIVATE" not in repr(first)
    assert key_file.read_bytes() == secret
    assert not hasattr(first, "secret_file")


@pytest.mark.parametrize("case", ["short_bytes", "text", "mutable_bytes", "oversized"])
def test_phase4_step4_PR016_invalid_secret_rejected_without_echo(case):
    from recursive_integrity_toolkit.errors import ConfigurationError
    from recursive_integrity_toolkit.utils.hashing import IdentifierProtection

    secret = {"short_bytes": b"short", "text": "PRIVATE-KEY" * 4,
              "mutable_bytes": bytearray(32), "oversized": b"a" * 4097}[case]
    with pytest.raises(ConfigurationError) as error:
        IdentifierProtection.create(secret=secret)
    assert "PRIVATE-KEY" not in str(error.value)


@pytest.mark.parametrize("path", ["https://PRIVATE.invalid/key", "//PRIVATE/key", "\\\\PRIVATE\\key", "file:/PRIVATE/key", "PRIVATE\x00KEY"])
def test_phase4_step4_PR016_nonlocal_secret_rejected_before_filesystem(path, monkeypatch):
    from pathlib import Path
    from recursive_integrity_toolkit.errors import ConfigurationError
    from recursive_integrity_toolkit.utils.hashing import IdentifierProtection

    def forbidden(*args, **kwargs):
        raise AssertionError("filesystem access must not occur")

    monkeypatch.setattr(Path, "lstat", forbidden)
    with pytest.raises(ConfigurationError) as error:
        IdentifierProtection.create(secret_file=path)
    assert "PRIVATE" not in str(error.value)


def test_phase4_step4_PR016_secret_symlink_and_double_sources_fail(tmp_path):
    from recursive_integrity_toolkit.errors import ConfigurationError
    from recursive_integrity_toolkit.utils.hashing import IdentifierProtection

    key = tmp_path / "key"
    key.write_bytes(b"k" * 32)
    link = tmp_path / "link"
    try:
        link.symlink_to(key)
    except (OSError, NotImplementedError):
        # Cross-platform regular-file and double-source behavior remains tested.
        with pytest.raises(ConfigurationError):
            IdentifierProtection.create(secret=b"k" * 32, secret_file=key)
        return
    with pytest.raises(ConfigurationError):
        IdentifierProtection.create(secret_file=link)
    with pytest.raises(ConfigurationError):
        IdentifierProtection.create(secret=b"k" * 32, secret_file=key)


@pytest.mark.parametrize("case", ["nan", "infinity", "nontext_key", "opaque_object"])
def test_phase4_step4_PR016_canonical_encoding_refuses_nonplain_data(case):
    from recursive_integrity_toolkit.utils.hashing import canonical_json_bytes

    value = {"nan": float("nan"), "infinity": float("inf"),
             "nontext_key": {1: "PRIVATE"}, "opaque_object": object()}[case]
    with pytest.raises(ValueError) as error:
        canonical_json_bytes(value)
    assert "PRIVATE" not in str(error.value)


def test_phase4_step4_PR016_canonical_encoding_refuses_cycle():
    from recursive_integrity_toolkit.utils.hashing import canonical_json_bytes

    value = []
    value.append(value)
    with pytest.raises(ValueError, match="finite acyclic plain JSON"):
        canonical_json_bytes(value)


def test_phase4_step4_PR016_options_defaults_and_inherited_output_remains_inert():
    from recursive_integrity_toolkit.config import resolve_config, resolve_phase4_options
    from recursive_integrity_toolkit.errors import ConfigurationError

    ordinary = resolve_phase4_options()
    assert ordinary.privacy_mode == "standard" and ordinary.record_id_mode == "preserve"
    assert str(ordinary.directory) == "rit-report"
    assert resolve_phase4_options(cli={"redacted": True}).record_id_mode == "hash"
    inherited = resolve_config({"output": {"PRIVATE_UNKNOWN": "PRIVATE_VALUE"}, "privacy_mode": "debug"})
    assert dict(inherited.output) == {"PRIVATE_UNKNOWN": "PRIVATE_VALUE"}
    assert inherited.privacy_mode.value == "debug"
    with pytest.raises(ConfigurationError) as error:
        resolve_phase4_options(inherited)
    assert "PRIVATE" not in str(error.value)


@pytest.mark.parametrize(("config", "cli"), [
    ({"inputs": {"records_primary": "a.csv"}}, {"records": "a.csv"}),
    ({"inputs": {"records_compare": ["a.csv", "b.csv"]}}, {}),
    ({"output": {"directory": "reports"}}, {"out": "reports"}),
    ({"privacy_mode": "redacted", "output": {"record_id_mode": "hash"}}, {"record_ids": "hash"}),
    ({"privacy_mode": "redacted", "output": {"id_salt_file": "key"}}, {"id_salt_file": "key"}),
    ({"privacy_mode": "redacted"}, {"redacted": True}),
    ({"strict_mode": True}, {"strict": True}),
    ({"version_order": ["v1"]}, {"version_order": ["v1"]}),
    ({"version_order": ["v1"], "inputs": {"version_order": "versions.json"}}, {}),
])
def test_phase4_step4_PR016_competing_singletons_never_override(config, cli):
    from recursive_integrity_toolkit.config import resolve_phase4_options
    from recursive_integrity_toolkit.errors import ConfigurationError

    with pytest.raises(ConfigurationError):
        resolve_phase4_options(config, cli=cli)


@pytest.mark.parametrize(("config", "cli"), [
    ({"simulation": {"enabled": True}}, {}),
    ({"state_mapping": {"PRIVATE": "value"}}, {}),
    ({"representation_compatibility": {"PRIVATE": "value"}}, {}),
    ({"output": {"PRIVATE": "value"}}, {}),
    ({}, {"PRIVATE": "value"}),
    ({}, {"record_ids": "hash"}),
    ({}, {"id_salt_file": "PRIVATE"}),
    ({}, {"redacted": "PRIVATE"}),
    ({}, {"strict": 1}),
    ({"output": {"directory": 1}}, {}),
])
def test_phase4_step4_PR016_unsupported_and_malformed_options_are_safe(config, cli):
    from recursive_integrity_toolkit.config import resolve_phase4_options
    from recursive_integrity_toolkit.errors import ConfigurationError

    with pytest.raises(ConfigurationError) as error:
        resolve_phase4_options(config, cli=cli)
    assert "PRIVATE" not in str(error.value)


@pytest.mark.parametrize(("rule", "threshold", "valid"), [
    (None, None, True), (None, 1, False),
    ("singleton_count", None, True), ("singleton_count", 1, False),
    ("count_at_or_below", 0, True), ("count_at_or_below", 2, True),
    ("count_at_or_below", 1.0, False), ("count_at_or_below", True, False),
    ("frequency_at_or_below", 0.0, True), ("frequency_at_or_below", 1, True),
    ("frequency_at_or_below", "nan", False), ("frequency_at_or_below", "infinity", False),
    ("frequency_at_or_below", "oversized_integer", False), ("state_list", None, False),
])
def test_phase4_step4_PR016_tail_declarations_have_exact_domains(rule, threshold, valid):
    from recursive_integrity_toolkit.config import resolve_phase4_options
    from recursive_integrity_toolkit.errors import ConfigurationError

    if type(threshold) is str:
        threshold = {"nan": float("nan"), "infinity": float("inf"), "oversized_integer": 10 ** 1000}[threshold]
    config = {"representation": {"name": "literal", "source": "field", "field": "topic", "missing_value_policy": "exclude"}}
    cli = {"tail_rule": rule, "tail_threshold": threshold}
    if valid:
        result = resolve_phase4_options(config, cli=cli)
        assert result.tail_rule == rule and result.tail_threshold == threshold
    else:
        with pytest.raises(ConfigurationError):
            resolve_phase4_options(config, cli=cli)


def test_phase4_step4_PR016_missing_state_is_explicit_and_tail_has_no_fallback():
    from recursive_integrity_toolkit.config import resolve_phase4_options
    from recursive_integrity_toolkit.errors import ConfigurationError

    config = {"representation": {"missing_value_policy": "explicit_missing_state"}}
    with pytest.raises(ConfigurationError):
        resolve_phase4_options(config)
    assert resolve_phase4_options(config, cli={"missing_state_id": "declared"}).missing_state_id == "declared"
    with pytest.raises(ConfigurationError):
        resolve_phase4_options(cli={"missing_state_id": "invented"})
    with pytest.raises(ConfigurationError):
        resolve_phase4_options(cli={"tail_rule": "singleton_count"})


def test_phase4_step4_PR016_summary_excludes_private_declarations_hash_retains_meaning(monkeypatch):
    import json
    from pathlib import Path
    from recursive_integrity_toolkit.config import phase4_config_hash, phase4_config_summary, resolve_phase4_options

    config = {"privacy_mode": "redacted", "inputs": {"records_primary": "PRIVATE-INPUT.csv"},
              "representation": {"name": "PRIVATE-LABEL", "field": "PRIVATE-FIELD"},
              "version_order": ["PRIVATE-VERSION"],
              "output": {"directory": "PRIVATE-OUTPUT", "id_salt_file": "PRIVATE-KEY"}}
    def forbidden(*args, **kwargs):
        raise AssertionError("declaration resolution must not read a file")
    monkeypatch.setattr(Path, "read_bytes", forbidden)
    options = resolve_phase4_options(config, cli={"state_semantics": "PRIVATE-SEMANTICS"})
    assert "PRIVATE" not in json.dumps(phase4_config_summary(options))
    assert "PRIVATE" not in repr(options)
    baseline = phase4_config_hash(options)
    reordered = dict(reversed(list(config.items())))
    assert baseline == phase4_config_hash(resolve_phase4_options(reordered, cli={"state_semantics": "PRIVATE-SEMANTICS"}))
    moved_secret = dict(config, output=dict(config["output"], id_salt_file="DIFFERENT-PRIVATE-KEY"))
    assert baseline == phase4_config_hash(resolve_phase4_options(moved_secret, cli={"state_semantics": "PRIVATE-SEMANTICS"}))
    changes = [dict(config, inputs={"records_primary": "OTHER.csv"}),
               dict(config, representation={"name": "OTHER", "field": "PRIVATE-FIELD"}),
               dict(config, version_order=["OTHER"]),
               dict(config, output=dict(config["output"], directory="OTHER")),
               dict(config, resource_limits={"max_rows": 5}),
               dict(config, strict_warning_codes=["W_OPTIONAL_FIELD_MISSING"])]
    for changed in changes:
        assert baseline != phase4_config_hash(resolve_phase4_options(changed, cli={"state_semantics": "PRIVATE-SEMANTICS"}))
    assert baseline != phase4_config_hash(resolve_phase4_options(config, cli={"state_semantics": "OTHER"}))


def test_phase4_step4_PR016_comparison_is_an_inert_explicit_declaration():
    from recursive_integrity_toolkit.config import phase4_config_summary, resolve_phase4_options
    from recursive_integrity_toolkit.models import FileRole

    options = resolve_phase4_options(cli={"compare": "earlier.csv", "records": "later.csv", "strict": True})
    assert phase4_config_summary(options)["comparison_requested"] is True
    assert {source.role for source in options.inputs} == {FileRole.RECORDS_PRIMARY, FileRole.RECORDS_COMPARE}
    assert options.configuration.strict_mode is False and options.strict_mode is True


def test_phase4_step4_PR016_safe_summary_revalidates_forged_options():
    from recursive_integrity_toolkit.config import phase4_config_summary, resolve_phase4_options
    from recursive_integrity_toolkit.errors import ConfigurationError

    options = resolve_phase4_options()
    object.__setattr__(options, "privacy_mode", "PRIVATE")
    with pytest.raises(ConfigurationError) as error:
        phase4_config_summary(options)
    assert "PRIVATE" not in str(error.value)


# Phase 4 Step 5: renderer ordering follows declared structure, never new chronology.
def phase4_step5_reverse_mapping_insertions(value):
    if type(value) is dict:
        return {key: phase4_step5_reverse_mapping_insertions(child)
                for key, child in reversed(tuple(value.items()))}
    if type(value) is list:
        return [phase4_step5_reverse_mapping_insertions(child) for child in value]
    return value


def phase4_step5_replace_literal_states(value):
    if type(value) is dict:
        return {key: phase4_step5_replace_literal_states(child) for key, child in value.items()}
    if type(value) is list:
        return [phase4_step5_replace_literal_states(child) for child in value]
    if type(value) is str:
        return {"a": "z-state", "b": "a-state", "c": "中文状态"}.get(value, value)
    return value


def test_phase4_step5_identical_safe_views_repeat_exact_json_and_markdown_bytes():
    from test_PR013_report_schema import phase4_step5_renderers, phase4_step5_rich_payload, phase4_step5_view

    for mode in ("standard", "redacted"):
        first = phase4_step5_view(phase4_step5_rich_payload(), mode)
        second = phase4_step5_view(phase4_step5_rich_payload(), mode)
        for render in phase4_step5_renderers():
            expected = render(first)
            assert expected.encode("utf-8") == render(first).encode("utf-8")
            assert expected.encode("utf-8") == render(second).encode("utf-8")
            assert expected.endswith("\n")
            assert "\r" not in expected


def test_phase4_step5_mapping_insertion_order_does_not_change_serialization():
    from test_PR013_report_schema import phase4_step5_renderers, phase4_step5_rich_payload, phase4_step5_view

    payload = phase4_step5_rich_payload()
    permuted = phase4_step5_reverse_mapping_insertions(payload)
    assert permuted == payload
    for mode in ("standard", "redacted"):
        first, second = phase4_step5_view(payload, mode), phase4_step5_view(permuted, mode)
        for render in phase4_step5_renderers():
            assert render(first) == render(second)


def test_phase4_step5_json_nested_mapping_keys_are_lexical_without_reordering_sections():
    import json
    from test_PR013_report_schema import phase4_step5_renderers, phase4_step5_rich_payload, phase4_step5_view

    render_json, _ = phase4_step5_renderers()
    actual = json.loads(render_json(phase4_step5_view(phase4_step5_rich_payload())))

    def verify(value):
        if type(value) is dict:
            assert list(value) == sorted(value)
            for child in value.values():
                verify(child)
        elif type(value) is list:
            for child in value:
                verify(child)

    assert tuple(actual) == ("run", "inputs", "observability", "capabilities", "observed_facts",
        "derived_metrics", "proxy_signals", "simulations", "unavailable_conclusions",
        "recommended_next_metadata", "warnings", "errors")
    for section in actual.values():
        verify(section)


def test_phase4_step5_declared_state_order_keeps_parallel_arrays_and_event_identity():
    import json
    from test_PR012_evidence_classes import phase4_step2_sampled_path_report_fixture
    from test_PR013_report_schema import phase4_step5_renderers, phase4_step5_view

    payload = phase4_step5_replace_literal_states(phase4_step2_sampled_path_report_fixture())
    render_json, render_markdown = phase4_step5_renderers()
    for mode in ("standard", "redacted"):
        view = phase4_step5_view(payload, mode)
        before = view.to_dict()["simulations"]["closed_resampling"]
        actual = json.loads(render_json(view))["simulations"]["closed_resampling"]
        assert actual == before
        order = actual["parameters"]["state_order"]
        assert [item["state_id"] for item in actual["initial_distribution"]] == order
        assert [item["probability"] for item in actual["initial_distribution"]] == [0.25, 0.25, 0.5]
        generations = actual["sampled_paths"][0]["generations"]
        assert generations[0]["state_frequencies"] == [0.25, 0.25, 0.5]
        assert generations[1]["state_counts"] == [0, 0, 2]
        assert generations[1]["support"] == [order[2]]
        assert [item["state_id"] for item in actual["extinction_events"]] == order[:2]
        if mode == "standard":
            assert order == ["z-state", "a-state", "中文状态"]
        markdown = render_markdown(view)
        for identity in order:
            assert identity in markdown
        assert view.to_dict()["simulations"]["closed_resampling"] == before


def test_phase4_step5_explicit_pair_direction_and_duplicate_members_survive_both_outputs(tmp_path):
    import json
    from test_PR013_report_schema import phase4_step5_renderers, phase4_step5_view
    from test_PR015_redaction import phase4_step4_private_report

    report = phase4_step4_private_report(tmp_path, pair=True, scenario=True, duplicates=True)
    render_json, render_markdown = phase4_step5_renderers()
    for mode, record_id_mode in (("standard", None), ("redacted", "hash"),
                                 ("redacted", "preserve"), ("redacted", "omit")):
        view = phase4_step5_view(report.to_dict(), mode, record_id_mode)
        before = view.to_dict()
        actual = json.loads(render_json(view))
        assert actual == before
        pair = actual["derived_metrics"]["support"]["support_delta"]["scope"]
        assert pair == before["derived_metrics"]["support"]["support_delta"]["scope"]
        assert len(pair["dataset_versions"]) == 2
        if mode == "standard":
            assert pair["dataset_versions"] == ["VERSION_SENTINEL", "LATER_VERSION_SENTINEL"]
        markdown = render_markdown(view)
        assert "support_delta" in markdown
        assert "exact_duplicate_groups" in markdown
        assert "sampled_paths" in markdown
        assert view.to_dict() == before


def test_phase4_step5_list_permutation_changes_outputs_instead_of_hiding_declared_order():
    import copy
    import json
    from test_PR012_evidence_classes import phase4_step2_sampled_path_report_fixture
    from test_PR013_report_schema import phase4_step5_renderers, phase4_step5_view

    original = phase4_step2_sampled_path_report_fixture()
    changed = copy.deepcopy(original)
    changed["simulations"]["closed_resampling"]["extinction_events"].reverse()
    for render in phase4_step5_renderers():
        assert render(phase4_step5_view(original)) != render(phase4_step5_view(changed))
    actual = json.loads(phase4_step5_renderers()[0](phase4_step5_view(changed)))
    assert [item["state_id"] for item in actual["simulations"]["closed_resampling"][
        "extinction_events"]] == ["b", "a"]
