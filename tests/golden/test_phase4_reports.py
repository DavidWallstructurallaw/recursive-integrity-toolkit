"""P4-D08 independently authored report oracles and literal format parity.

Generation and validation are separate: assertions predate observations, reviewed
fixtures are immutable inputs, and candidates cannot promote themselves. Frozen
Phase 3 numerical oracles remain in their original module and execute separately.
"""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import runpy

import pytest


GOLDEN = Path(__file__).parent
ROOT = GOLDEN.parents[1]
EXPECTED = json.loads((GOLDEN / "phase4_report_expected.json").read_bytes())
CASES = EXPECTED["cases"]
BUILDER = runpy.run_path(str(ROOT / "scripts/build_golden.py"), run_name="phase4_step9_builder")
NORMALIZER = runpy.run_path(str(ROOT / "scripts/normalize_golden.py"), run_name="phase4_step9_normalizer")


@pytest.fixture(scope="module")
def phase4_step9_hero_observations(tmp_path_factory):
    import contextlib
    import http.client
    import socket
    import urllib.request
    from unittest.mock import patch
    root = tmp_path_factory.mktemp("phase4-step9-golden")
    attempts = []
    def denied(*args, **kwargs):
        attempts.append(True)
        raise AssertionError("golden example attempted a network operation")
    observed = {}
    with contextlib.ExitStack() as stack:
        for owner, name in ((socket, "socket"), (socket, "create_connection"), (socket, "getaddrinfo"),
                            (urllib.request, "urlopen"), (urllib.request.OpenerDirector, "open"),
                            (http.client.HTTPConnection, "connect"), (http.client.HTTPSConnection, "connect")):
            stack.enter_context(patch.object(owner, name, denied))
        for redacted in (False, True):
            directory = root / ("redacted" if redacted else "standard")
            actual = BUILDER["run_example"](directory, redacted=redacted)
            assert actual["exit_code"] == 0
            normalized = NORMALIZER["normalize_report"](actual["report"], test_root=directory,
                                                        declared_config=actual["declared_config"])
            normalized_md = NORMALIZER["normalize_markdown"](actual["markdown"], actual["report"], normalized)
            actual.update(exit=actual["exit_code"], root=directory, normalized=normalized,
                          normalized_markdown=normalized_md)
            observed[redacted] = actual
    assert not attempts
    return observed


@pytest.mark.parametrize("case", CASES, ids=[case["case_id"] for case in CASES])
def test_phase4_step9_independent_report_case(case, tmp_path, phase4_step9_hero_observations):
    if case["kind"] in {"hero_normal", "hero_redacted"}:
        actual = phase4_step9_hero_observations[case["kind"] == "hero_redacted"]
    elif case["kind"] == "hero_reordered":
        actual = phase4_step9_reordered_hero(case, tmp_path)
    elif case["kind"] == "installed_hero":
        actual = phase4_step9_installed_oracle(case, tmp_path, ROOT)
    else:
        actual = phase4_step9_execute_oracle(case, tmp_path, BUILDER["fixed_metadata"], GOLDEN)
    schema = json.loads((ROOT / "schemas/report.schema.json").read_bytes())
    phase4_step9_assert_oracle(case, actual, schema)
    if case.get("aggregate_parity_with") == "hero_normal":
        assert phase4_step9_aggregate_projection(actual["report"]) == phase4_step9_aggregate_projection(phase4_step9_hero_observations[False]["report"])


def test_phase4_step9_case_registry_is_explicit_independent_and_exhaustive():
    assert EXPECTED["expectations_generated_by_implementation"] is False
    assert len(CASES) == len({case["case_id"] for case in CASES})
    assert CASES and all(case.get("numeric_rationale") for case in CASES)
    allowed = {"hero_normal", "hero_redacted", "hero_reordered", "installed_hero", "cli", "canonical_rejection", "report_rejection", "pair_api_rejection"}
    assert {case["kind"] for case in CASES} <= allowed
    assert {"hero_normal", "hero_redacted", "cli", "canonical_rejection"} <= {case["kind"] for case in CASES}
    assert all("expected_exit" in case or case["kind"] in {"canonical_rejection", "report_rejection", "pair_api_rejection"} for case in CASES)
    assert (GOLDEN / "phase4_report_cases.md").read_text(encoding="utf-8").strip()


@pytest.mark.parametrize("redacted", [False, True])
def test_phase4_step9_literal_json_and_markdown_goldens(redacted, phase4_step9_hero_observations):
    from recursive_integrity_toolkit import __version__

    actual = phase4_step9_hero_observations[redacted]
    stem = "phase4_hero_redacted" if redacted else "phase4_hero_report"
    json_path, markdown_path = GOLDEN / (stem + ".json"), GOLDEN / (stem + ".md")
    before = {path: path.read_bytes() for path in (json_path, markdown_path)}
    # Current schema fixtures retain the independently authored numeric oracle.
    # Prior schema fixtures remain recoverable from Git history.
    expected_json = json.loads(before[json_path])
    assert expected_json["run"]["toolkit_version"] == __version__
    assert actual["report"]["run"]["toolkit_version"] == __version__
    assert actual["normalized"]["run"]["toolkit_version"] == __version__
    expected_markdown = before[markdown_path].decode("utf-8")
    NORMALIZER["assert_golden_pair"](actual["normalized"], actual["normalized_markdown"],
                                      expected_json, expected_markdown)
    assert {path: path.read_bytes() for path in before} == before


@pytest.mark.parametrize("pointer,replacement", [
    ("/run/toolkit_version", "0.1.0.dev2"),
    ("/derived_metrics/support/by_version/v1/support_size/value", 9001),
    ("/derived_metrics/support/by_version/v1/support_size/evidence_class", "observed_fact"),
    ("/derived_metrics/support/by_version/v1/support_size/scope/record_count", 9001),
    ("/derived_metrics/support/by_version/v1/support_size/availability", "partial"),
    ("/derived_metrics/support/by_version/v1/support_size/reason_codes", ["R_TAMPERED"]),
    ("/warnings", "insert_warning"),
    ("/unavailable_conclusions", []),
    ("/run/resolved_options/weighted", True),
    ("/run/run_status", "partial"),
])
def test_phase4_step9_substantive_mutation_never_disappears(pointer, replacement, phase4_step9_hero_observations):
    actual = phase4_step9_hero_observations[False]
    changed = deepcopy(actual["report"])
    if pointer == "/warnings":
        replacement = [{"code": "W_ORACLE_TAMPER", "message": "An authored warning was inserted.", "count": 1,
            "affected_scope": deepcopy(changed["inputs"]["scope"]), "representative_locations": [],
            "effect_on_capabilities": ["ingestion"], "remediation": ["Review the evidence."]}]
    parent, _, key = pointer.rpartition("/")
    phase4_step9_pointer(changed, parent)[key] = replacement
    try:
        normalized = NORMALIZER["normalize_report"](changed, test_root=actual["root"], declared_config=actual["declared_config"])
    except ValueError:
        return  # Structural/semantic corruption is rejected before normalization.
    assert phase4_step9_pointer(normalized, pointer) == replacement
    with pytest.raises(AssertionError):
        NORMALIZER["assert_golden_pair"](normalized, actual["normalized_markdown"], actual["normalized"], actual["normalized_markdown"])


@pytest.mark.parametrize("field", ["file_hash", "size_bytes"])
def test_phase4_step9_inventory_hashes_and_sizes_are_checked(field, phase4_step9_hero_observations):
    actual = phase4_step9_hero_observations[False]
    changed = deepcopy(actual["report"])
    changed["inputs"]["artifacts"][0][field] = "0" * 64 if field == "file_hash" else 0
    with pytest.raises(ValueError, match="hash or size"):
        NORMALIZER["normalize_report"](changed, test_root=actual["root"], declared_config=actual["declared_config"])


@pytest.mark.parametrize("mutation", ["raw_hash", "meaning", "path_escape", "input_order"])
def test_phase4_step9_config_hash_cannot_hide_meaning(mutation, phase4_step9_hero_observations):
    actual = phase4_step9_hero_observations[False]
    payload, declaration = deepcopy(actual["report"]), deepcopy(actual["declared_config"])
    if mutation == "raw_hash":
        payload["run"]["config_hash"] = "0" * 64
    elif mutation == "meaning":
        declaration["options"]["state_semantics"] = "same topology now means a different state"
    elif mutation == "path_escape":
        declaration["options"]["output"]["directory"] = str(actual["root"].parent / "outside")
        payload["run"]["config_hash"] = NORMALIZER["_declared_config_hash"](declaration)
    else:
        declaration["options"]["inputs"].reverse()
    with pytest.raises(ValueError):
        NORMALIZER["normalize_report"](payload, test_root=actual["root"], declared_config=declaration)


def test_phase4_step9_metadata_allowlist_is_exact_and_input_not_mutated(phase4_step9_hero_observations):
    actual = phase4_step9_hero_observations[False]
    payload = deepcopy(actual["report"])
    before = deepcopy(payload)
    output = NORMALIZER["normalize_report"](payload, test_root=actual["root"], declared_config=actual["declared_config"])
    assert payload == before
    assert set(NORMALIZER["RUN_METADATA"]) == {"run_id", "started_at", "completed_at", "duration_seconds", "python_version", "platform"}
    for name in payload:
        if name not in {"run", "inputs"}:
            assert output[name] == payload[name]
    expected_run = deepcopy(payload["run"])
    expected_run.update({key: value for key, value in NORMALIZER["RUN_METADATA"].items() if expected_run[key] is not None})
    expected_run["config_hash"] = output["run"]["config_hash"]
    assert output["run"] == expected_run
    for old, new in zip(payload["inputs"]["artifacts"], output["inputs"]["artifacts"], strict=True):
        untouched = deepcopy(new)
        untouched["path"] = old["path"]
        assert untouched == old
    assert {k: v for k, v in output["inputs"].items() if k != "artifacts"} == {k: v for k, v in payload["inputs"].items() if k != "artifacts"}


@pytest.mark.parametrize("mutation", ["metric", "missing_section", "forbidden_claim", "reason", "run_row_missing", "run_row_duplicate"])
def test_phase4_step9_markdown_mutations_fail_literal_comparison(mutation, phase4_step9_hero_observations):
    actual = phase4_step9_hero_observations[False]
    text = actual["markdown"]
    if mutation == "metric":
        assert "Value: 8." in text
        text = text.replace("Value: 8.", "Value: 8000.", 1)
    elif mutation == "missing_section":
        text = text.replace("## Unavailable conclusions\n", "", 1)
    elif mutation == "forbidden_claim":
        text += "This proves inevitable model collapse.\n"
    elif mutation == "reason":
        text += "An unsupported explanation was inserted.\n"
    else:
        line = next(line for line in text.splitlines(keepends=True) if line.startswith('| `["config_hash"]` |'))
        text = text.replace(line, "" if mutation == "run_row_missing" else line + line, 1)
    try:
        normalized = NORMALIZER["normalize_markdown"](text, actual["report"], actual["normalized"])
    except ValueError:
        assert mutation in {"run_row_missing", "run_row_duplicate"}
        return
    with pytest.raises(AssertionError):
        NORMALIZER["assert_golden_pair"](actual["normalized"], normalized, actual["normalized"], actual["normalized_markdown"])


def test_phase4_step9_redaction_preserves_analytical_values_and_scope_counts(phase4_step9_hero_observations):
    def values(node):
        found = []
        if isinstance(node, dict):
            if "evidence_class" in node and "value" in node and (node["value"] is None or type(node["value"]) in (int, float)):
                scope = node.get("scope", {})
                found.append(json.dumps({key: node.get(key) for key in ("value", "status", "evidence_class", "coverage", "denominator", "reason_codes")} | {
                    "record_count": scope.get("record_count"), "excluded_record_count": scope.get("excluded_record_count")}, sort_keys=True))
            for value in node.values():
                found.extend(values(value))
        elif isinstance(node, list):
            for value in node:
                found.extend(values(value))
        return found
    standard = phase4_step9_hero_observations[False]["report"]
    redacted = phase4_step9_hero_observations[True]["report"]
    import hmac
    def alias(domain, value):
        label = domain.encode("ascii")
        raw = json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode("ascii")
        framed = b"rit.identifier.v1\x00" + len(label).to_bytes(4, "big") + label + len(raw).to_bytes(8, "big") + raw
        return "hmac-sha256:" + hmac.new(BUILDER["TEST_KEY"], framed, hashlib.sha256).hexdigest()
    # Keyed association is checked independently, so swapping two versions with
    # the same record count cannot pass a multiset-only numerical comparison.
    for version, support, diversity in (("v1", 8, 0.875), ("v2", 5, 0.75)):
        private_version = alias("dataset_version", version)
        assert redacted["derived_metrics"]["support"]["by_version"][private_version]["support_size"]["value"] == support
        assert redacted["derived_metrics"]["diversity"]["by_version"][private_version]["gini_simpson_diversity"]["value"] == diversity
        for family in ("support", "diversity"):
            for name, item in standard["derived_metrics"][family]["by_version"][version].items():
                other = redacted["derived_metrics"][family]["by_version"][private_version][name]
                for field in ("status", "evidence_class", "method_id", "owner_ids", "denominator", "coverage", "reason_codes"):
                    assert other.get(field) == item.get(field), (version, family, name, field)
                assert other["scope"]["dataset_versions"] == [private_version]
                if item.get("value") is None or type(item.get("value")) in (int, float):
                    assert other.get("value") == item.get("value"), (version, family, name)
        before = standard["observed_facts"]["state_counts"]["by_version"][version]["value"]
        after = redacted["observed_facts"]["state_counts"]["by_version"][private_version]["value"]
        assert after == [{"state_id": alias("state_id", row["state_id"]), "state_count": row["state_count"]} for row in before]

    left, right = values(standard), values(redacted)
    assert len(left) >= 30 and sorted(left) == sorted(right)
    assert all(item["path"] is None for item in redacted["inputs"]["artifacts"])
    assert sorted(item["file_hash"] for item in standard["inputs"]["artifacts"]) == sorted(item["file_hash"] for item in redacted["inputs"]["artifacts"])
    assert redacted["run"]["identifier_protection"]["stability_scope"] == "run"
    assert redacted["run"]["run_id"].startswith("hmac-sha256:")
    for redacted_mode, actual in phase4_step9_hero_observations.items():
        sinks = json.dumps(actual["report"]) + actual["markdown"] + actual["stdout"] + actual["stderr"]
        assert BUILDER["TEST_KEY"].decode() not in sinks
        if redacted_mode:
            assert str(actual["root"]) not in sinks


@pytest.mark.parametrize("target", ["repository", "accepted_file", "existing", "relative", "parent_traversal", "double_root"])
def test_phase4_step9_candidate_writer_rejects_unsafe_destinations(target, tmp_path):
    if target == "repository":
        path = ROOT / "tests/golden/unapproved-candidate"
    elif target == "accepted_file":
        path = GOLDEN / "phase4_hero_report.json"
    elif target == "existing":
        path = tmp_path
    elif target == "relative":
        path = Path("unapproved-candidate")
    elif target == "double_root":
        path = "//" + str(GOLDEN / "unapproved-candidate").lstrip("/\\")
    else:
        path = tmp_path / ".." / "unapproved-candidate"
    before = {p: p.read_bytes() for p in GOLDEN.iterdir() if p.is_file()}
    with pytest.raises(ValueError):
        BUILDER["build_candidates"](path)
    assert {p: p.read_bytes() for p in before} == before


def test_phase4_step9_candidate_writer_and_cli_help_are_explicit(tmp_path, subprocess_env):
    import subprocess
    import sys
    for script in ("build_golden.py", "normalize_golden.py"):
        result = subprocess.run([sys.executable, str(ROOT / "scripts" / script), "--help"],
                                capture_output=True, text=True, env=subprocess_env, check=False)
        assert result.returncode == 0 and "--scratch-out" in result.stdout
        result = subprocess.run([sys.executable, str(ROOT / "scripts" / script)],
                                capture_output=True, text=True, env=subprocess_env, check=False)
        assert result.returncode == 2
    assert not list(tmp_path.iterdir())


def test_phase4_step9_candidate_generation_is_repeatable_and_never_promotes(tmp_path):
    before = {p: p.read_bytes() for p in GOLDEN.iterdir() if p.is_file()}
    first = BUILDER["build_candidates"](tmp_path / "first")
    second = BUILDER["build_candidates"](tmp_path / "second")
    assert first == second and first["candidate_only"] is True
    assert first["acceptance_requires_independent_review"] is True
    assert len(first["files"]) == 4
    for name, digest in first["files"].items():
        assert (tmp_path / "first" / name).read_bytes() == (tmp_path / "second" / name).read_bytes()
        assert hashlib.sha256((tmp_path / "first" / name).read_bytes()).hexdigest() == digest
    assert {p: p.read_bytes() for p in before} == before
"""Fragment for integration into the authorized Step 9 golden test module.

No production report has been observed to author this case execution helper.
Expected values are supplied by the independently frozen case manifest.
"""


def phase4_step9_pointer(payload, pointer):
    if pointer == "":
        return payload
    assert pointer.startswith("/"), pointer
    value = payload
    for encoded in pointer[1:].split("/"):
        part = encoded.replace("~1", "/").replace("~0", "~")
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


def phase4_step9_execute_oracle(case, directory, fixed_metadata, golden_directory):
    import contextlib
    import copy
    import hashlib
    import http.client
    import io
    import json
    from pathlib import Path
    import socket
    import urllib.request
    from unittest.mock import patch

    from recursive_integrity_toolkit.cli import main
    from recursive_integrity_toolkit.result import CanonicalReport

    root = Path(directory)
    root.mkdir(parents=True, exist_ok=True)
    spec = case["input_spec"]
    if case["kind"] == "pair_api_rejection":
        from recursive_integrity_toolkit.errors import CanonicalValidationError, ErrorCode
        from recursive_integrity_toolkit.io.validation import resolve_version_order
        from recursive_integrity_toolkit.metrics.diversity import compare_support, distribution_from_counts
        from recursive_integrity_toolkit.models import CalculationScope, ExplicitPairContext, RecordKey, RepresentationDescriptor
        distributions = []
        for side in ("earlier", "later"):
            version, counts = spec[side + "_version"], spec[side + "_counts"]
            descriptor = spec[side + "_representation"]
            scope = CalculationScope((version,), tuple(RecordKey(version, str(index)) for index in range(sum(counts.values()))),
                                     (), "included_representation_records", "golden-" + side)
            representation = RepresentationDescriptor(descriptor["name"], descriptor["source"], descriptor["version"],
                "literal_field_value", field_name=descriptor["field"], missing_value_policy=descriptor["missing_value_policy"])
            distributions.append(distribution_from_counts(counts, scope=scope, representation=representation))
        earlier, later = distributions
        # Two authored positive counts on each side give support 2 and D=1/2.
        assert earlier.support_size.value == later.support_size.value == 2
        assert earlier.gini_simpson_diversity.value == later.gini_simpson_diversity.value == 0.5
        order = resolve_version_order((spec["earlier_version"], spec["later_version"]), invocation_order=tuple(spec["version_order"]))
        context = ExplicitPairContext(earlier.scope, later.scope, earlier.representation, later.representation, order)
        try:
            compare_support(earlier, later, context=context, earlier_state_semantics=spec["state_semantics"],
                            later_state_semantics=spec["state_semantics"])
        except CanonicalValidationError as error:
            assert error.code is ErrorCode.REPRESENTATION_INCOMPATIBLE
            return {"rejected": True, "exception_type": type(error).__name__, "error_code": error.code.value}
        raise AssertionError("Incompatible representations silently produced a pair")
    if case["kind"] in {"canonical_rejection", "report_rejection"}:
        assert spec["baseline"] == "hero_normal"
        payload = json.loads((Path(golden_directory) / "phase4_hero_report.json").read_text(encoding="utf-8"))
        CanonicalReport.from_dict(payload)
        payload = copy.deepcopy(payload)
        for pointer, value in spec["mutations"].items():
            parent, _, encoded = pointer.rpartition("/")
            owner = phase4_step9_pointer(payload, parent)
            key = encoded.replace("~1", "/").replace("~0", "~")
            if isinstance(value, dict) and set(value) == {"$nonfinite"}:
                assert value["$nonfinite"] in {"NaN", "Infinity", "-Infinity"}
                value = float(value["$nonfinite"])
            owner[int(key) if isinstance(owner, list) else key] = value
        try:
            CanonicalReport.from_dict(payload)
        except ValueError as error:
            return {"rejected": True, "exception_type": type(error).__name__,
                    "exception_bases": [cls.__name__ for cls in type(error).__mro__]}
        raise AssertionError(f"{case['case_id']}: corrupt canonical result was accepted")
    assert case["kind"] == "cli", case["kind"]
    paths = {}
    for name, definition in spec["files"].items():
        relative = Path(name)
        assert not relative.is_absolute() and ".." not in relative.parts
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        kind = definition["format"]
        if kind == "jsonl":
            data = "".join(json.dumps(row, ensure_ascii=False, allow_nan=False) + "\n" for row in definition["rows"])
        elif kind == "json":
            data = json.dumps(definition["value"], ensure_ascii=False, allow_nan=False) + "\n"
        elif kind == "text":
            data = definition["text"]
        else:
            raise AssertionError(f"Unsupported authored input format: {kind}")
        path.write_bytes(data.encode("utf-8"))
        paths[name] = path
    before = {name: path.read_bytes() for name, path in paths.items()}
    argv = [value.replace("{root}", str(root)) for value in spec["argv"]]
    assert argv.count("--out") == 1
    output = Path(argv[argv.index("--out") + 1])
    network_attempts = []
    def denied(*args, **kwargs):
        network_attempts.append(True)
        raise AssertionError("A golden command attempted network access")
    stdout, stderr = io.StringIO(), io.StringIO()
    with contextlib.ExitStack() as stack:
        for owner, name in ((socket, "socket"), (socket, "create_connection"),
                            (socket, "getaddrinfo"), (socket, "gethostbyname"),
                            (socket, "gethostbyname_ex"), (socket, "gethostbyaddr"),
                            (urllib.request, "urlopen"), (urllib.request.OpenerDirector, "open"),
                            (http.client.HTTPConnection, "connect"), (http.client.HTTPSConnection, "connect")):
            stack.enter_context(patch.object(owner, name, denied))
        stack.enter_context(fixed_metadata())
        stack.enter_context(contextlib.redirect_stdout(stdout))
        stack.enter_context(contextlib.redirect_stderr(stderr))
        exit_code = main(argv)
    assert not network_attempts
    assert {name: path.read_bytes() for name, path in paths.items()} == before
    no_report = case.get("no_report", False)
    report_path, markdown_path = output / "report.json", output / "report.md"
    payload = None if no_report else json.loads(report_path.read_bytes())
    markdown = "" if no_report else markdown_path.read_bytes().decode("utf-8")
    if not no_report:
        assert [json.loads(line) for line in stderr.getvalue().splitlines()] == payload["warnings"] + payload["errors"]
    if no_report:
        for path in (report_path, markdown_path):
            if path.exists():
                relative = path.relative_to(root).as_posix()
                assert relative in before and path.read_bytes() == before[relative]
    for name in case.get("files_absent", []):
        assert not (root / name).exists()
    for name, text in case.get("files_unchanged", {}).items():
        assert (root / name).read_bytes() == text.encode("utf-8")
    return {"exit": exit_code, "report": payload, "markdown": markdown, "root": root,
            "stdout": stdout.getvalue(), "stderr": stderr.getvalue(),
            "input_sha256": {name: hashlib.sha256(data).hexdigest() for name, data in before.items()},
            "network_attempts": len(network_attempts), "inputs_unchanged": True}


def phase4_step9_assert_oracle(case, actual, schema):
    import json
    import jsonschema
    from recursive_integrity_toolkit import __version__
    from recursive_integrity_toolkit.result import SECTION_ORDER, validate_report

    if case["kind"] in {"canonical_rejection", "report_rejection", "pair_api_rejection"}:
        assert actual["rejected"]
        assert case["expected_exception"] in actual.get("exception_bases", [actual["exception_type"]])
        if "expected_error_code" in case:
            assert actual["error_code"] == case["expected_error_code"]
        return
    assert actual["exit"] == case["expected_exit"], (case["case_id"], actual["stderr"])
    payload, markdown = actual["report"], actual["markdown"]
    all_sinks = json.dumps(payload, ensure_ascii=False) + markdown + actual["stdout"] + actual["stderr"]
    for forbidden in case.get("forbidden_literals", []):
        forbidden = forbidden.replace("{root}", str(actual["root"]))
        escaped = json.dumps(forbidden, ensure_ascii=False)[1:-1]
        assert forbidden not in all_sinks and escaped not in all_sinks, (case["case_id"], forbidden)
    for forbidden in case.get("markdown_forbidden_literals", []):
        assert forbidden not in markdown, (case["case_id"], forbidden)
    for definition in case["input_spec"].get("files", {}).values():
        for row in definition.get("rows", []):
            content = row.get("content")
            if type(content) is str and content:
                assert content not in all_sinks, (case["case_id"], "raw content leaked")
    for forbidden in case.get("forbidden_claims", []):
        analytical = json.dumps({section: (payload or {}).get(section, {}) for section in
                                ("observed_facts", "derived_metrics", "proxy_signals", "simulations")})
        assert forbidden not in analytical, (case["case_id"], forbidden)
    for code in case.get("stderr_codes", []):
        assert code in actual["stderr"]
    if case.get("no_report", False):
        assert payload is None and markdown == ""
        return
    validate_report(payload)
    assert payload["run"]["toolkit_version"] == __version__
    jsonschema.Draft202012Validator(schema).validate(payload)
    assert tuple(payload) == tuple(SECTION_ORDER)
    headings = ["Run metadata", "Input inventory", "Observability summary", "Capability matrix",
                "Observed facts", "Derived metrics", "Proxy signals", "Simulations",
                "Unavailable conclusions", "Recommended next metadata", "Warnings", "Errors"]
    assert markdown.startswith("# Recursive Integrity Audit Report\n")
    assert [line for line in markdown.splitlines() if line.startswith("## ")] == ["## " + value for value in headings]
    for pointer, expected in case.get("expected", {}).items():
        got = phase4_step9_pointer(payload, pointer)
        assert got == expected, (case["case_id"], pointer, got, expected)
        if isinstance(expected, bool):
            assert type(got) is bool
    for pointer in case.get("absent_paths", []):
        try:
            phase4_step9_pointer(payload, pointer)
        except (KeyError, IndexError):
            pass
        else:
            raise AssertionError(f"{case['case_id']}: forbidden report field {pointer}")
    for pointer in case.get("nonempty_paths", []):
        assert phase4_step9_pointer(payload, pointer), (case["case_id"], pointer)
    for field, requirement in (("errors", "required_error_codes"), ("warnings", "required_warning_codes")):
        codes = {entry["code"] for entry in payload[field]}
        for code in case.get(requirement, []):
            assert code in codes, (case["case_id"], code, codes)
            assert code in markdown and code in actual["stderr"]
    claims = {entry["conclusion"] for entry in payload["unavailable_conclusions"]}
    assert set(case.get("unavailable_conclusions", [])) <= claims
    for expected in case.get("markdown_requirements", []):
        if expected == "all_twelve_sections_in_order":
            continue  # Exact ordered headings already checked above.
        if expected == "json_value_evidence_status_parity":
            phase4_step9_assert_markdown_envelopes(payload, markdown)
        else:
            assert expected in markdown, (case["case_id"], expected)


@pytest.mark.parametrize("mutation", ["duplicate_role", "missing_mirror", "mirror_digest", "mirror_index"])
def test_phase4_step9_inventory_is_bijective_and_hash_mirror_checked(mutation, phase4_step9_hero_observations):
    actual = phase4_step9_hero_observations[False]
    payload = deepcopy(actual["report"])
    if mutation == "duplicate_role":
        payload["inputs"]["artifacts"][1] = deepcopy(payload["inputs"]["artifacts"][0])
    elif mutation == "missing_mirror":
        payload["inputs"]["file_hashes"] = []
    elif mutation == "mirror_digest":
        payload["inputs"]["file_hashes"][0]["value"] = "0" * 64
    else:
        payload["inputs"]["file_hashes"][0]["artifact_index"] = 1
    with pytest.raises(ValueError):
        NORMALIZER["normalize_report"](payload, test_root=actual["root"], declared_config=actual["declared_config"])


def phase4_step9_assert_markdown_envelopes(payload, markdown):
    """Independently locate every analytical envelope and check its evidence."""
    def walk(value, path):
        if isinstance(value, dict) and {"evidence_class", "status", "method_id"} <= value.keys():
            yield path, value
        elif isinstance(value, dict):
            for key, child in value.items():
                yield from walk(child, (*path, key))
        elif isinstance(value, list):
            for index, child in enumerate(value):
                yield from walk(child, (*path, index))
    phase4_step9_assert_all_markdown_fields(payload, markdown)
    envelopes = []
    for section in ("observed_facts", "derived_metrics", "proxy_signals", "simulations", "unavailable_conclusions"):
        envelopes.extend(walk(payload[section], (section,)))
    blocks = markdown.split("### Analytical result\n\n")[1:]
    assert len(blocks) == len(envelopes)
    code = NORMALIZER["_markdown_literal"]
    for path, envelope in envelopes:
        marker = "`" + "".join("[" + json.dumps(part, ensure_ascii=False) + "]" for part in path) + "`\n"
        found = [block for block in blocks if block.startswith(marker)]
        assert len(found) == 1, path
        block = found[0]
        assert "Status: " + code(envelope["status"]) + "; evidence class: " + code(envelope["evidence_class"]) in block
        assert "; unit: " + code(envelope["unit"]) + "; method: " + code(envelope["method_id"]) + "." in block
        def scalar(field):
            value = envelope[field]
            if value is None:
                return "Unavailable (null): " + code(envelope[field + "_reason"])
            return str(value).lower() if type(value) is bool else repr(value) if type(value) in (int, float) else code(value)
        assert "Denominator: " + scalar("denominator") + "; coverage (ratio): " + scalar("coverage") + "." in block
        if "value" in envelope:
            value = envelope["value"]
            if value is None:
                assert envelope["reason_codes"] and envelope["required_evidence"]
                assert "Value: Unavailable (null): reason codes " + code(envelope["reason_codes"]) + "." in block
            elif type(value) in (int, float):
                assert "Value: " + repr(value) + "." in block
            elif type(value) is bool:
                assert "Value: " + str(value).lower() + "." in block
            elif type(value) is str:
                assert "Value: " + code(value) + "." in block
        for reason in envelope.get("reason_codes", []):
            assert json.dumps(reason)[1:-1] in block


def phase4_step9_reordered_hero(case, directory):
    adapted = deepcopy(case)
    adapted["kind"] = "cli"
    adapted["input_spec"]["files"] = {}
    for name in ("records_v1.csv", "records_v2.csv", "provenance.csv", "config.json", "version_order.json"):
        raw = (ROOT / "examples/hero" / name).read_bytes().decode("utf-8")
        if name.endswith(".csv"):
            lines = raw.splitlines(keepends=True)
            raw = lines[0] + "".join(reversed(lines[1:]))
        adapted["input_spec"]["files"][name] = {"format": "text", "text": raw}
    actual = phase4_step9_execute_oracle(adapted, directory, BUILDER["fixed_metadata"], GOLDEN)
    for artifact in actual["report"]["inputs"]["artifacts"]:
        path = Path(artifact["path"])
        assert artifact["file_hash"] == hashlib.sha256(path.read_bytes()).hexdigest()
        if path.suffix == ".csv":
            assert artifact["file_hash"] != hashlib.sha256((ROOT / "examples/hero" / path.name).read_bytes()).hexdigest()
    return actual


def phase4_step9_aggregate_projection(node):
    """Comparison projection only; never used to normalize literal goldens."""
    found = []
    if isinstance(node, dict):
        if "evidence_class" in node and "value" in node and (node["value"] is None or type(node["value"]) in (int, float)):
            scope = node.get("scope", {})
            found.append(json.dumps({key: node.get(key) for key in ("value", "status", "evidence_class", "coverage", "denominator", "reason_codes")} | {
                "record_count": scope.get("record_count"), "excluded_record_count": scope.get("excluded_record_count")}, sort_keys=True))
        for value in node.values():
            found.extend(phase4_step9_aggregate_projection(value))
    elif isinstance(node, list):
        for value in node:
            found.extend(phase4_step9_aggregate_projection(value))
    return sorted(found)
"""Step 9 installed wheel case helper for the golden test module."""


def phase4_step9_installed_oracle(case, directory, repo_root):
    import hashlib
    import json
    from pathlib import Path
    import subprocess
    import sys

    root, repository = Path(directory), Path(repo_root).resolve()
    root.mkdir(parents=True, exist_ok=True)
    output = root / "example"
    metadata = root / "installed-identity.json"
    program = r'''
import hashlib, importlib.abc, importlib.metadata, io, json, socket, sys, urllib.request, http.client
from pathlib import Path
target, repository, identity_path = map(Path, sys.argv[1:])
class DenyPyArrow(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] == 'pyarrow':
            raise ModuleNotFoundError('optional PyArrow intentionally unavailable')
sys.meta_path.insert(0, DenyPyArrow())
attempts = []
def denied(*args, **kwargs):
    attempts.append(True)
    raise AssertionError('installed command attempted network access')
socket.create_connection = socket.getaddrinfo = socket.gethostbyname = socket.gethostbyname_ex = socket.gethostbyaddr = denied
socket.socket.connect = socket.socket.connect_ex = socket.socket.sendto = denied
urllib.request.urlopen = urllib.request.OpenerDirector.open = denied
http.client.HTTPConnection.connect = http.client.HTTPSConnection.connect = denied
import recursive_integrity_toolkit as package
installed = Path(package.__file__).resolve().parent
assert not installed.is_relative_to(repository), installed
distribution = importlib.metadata.distribution('recursive-integrity-toolkit')
assert distribution.version == package.__version__ == '0.1.0.dev4'
members = {str(p).replace('\\', '/') for p in distribution.files or ()}
modules = sorted(p for p in installed.rglob('*.py'))
assert len(modules) == 40
hashes = {p.relative_to(installed).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in modules}
assert all('recursive_integrity_toolkit/' + p in members for p in hashes), 'Package must be installed from a wheel'
resources = sorted(p for p in (installed / 'data').rglob('*') if p.is_file())
assert len(resources) == 7
resource_hashes = {p.relative_to(installed).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in resources}
from recursive_integrity_toolkit.cli import main
exit_code = main(['example', '--out', str(target)])
assert not attempts and not any(n == 'pyarrow' or n.startswith('pyarrow.') for n in sys.modules)
identity_path.write_bytes((json.dumps({'installed_path': str(installed), 'module_sha256': hashes,
    'resource_sha256': resource_hashes, 'optional_pyarrow_imported': False, 'network_attempts': len(attempts)}, indent=2) + '\n').encode('utf-8'))
raise SystemExit(exit_code)
'''
    completed = subprocess.run([sys.executable, "-I", "-c", program, str(output), str(repository), str(metadata)],
                               cwd=root, capture_output=True, text=True, encoding="utf-8", check=False)
    assert completed.returncode == case["expected_exit"], completed.stderr
    proof = json.loads(metadata.read_bytes())
    for relative, digest in {**proof["module_sha256"], **proof["resource_sha256"]}.items():
        source = repository / "src" / "recursive_integrity_toolkit" / relative
        assert hashlib.sha256(source.read_bytes()).hexdigest() == digest, relative
    files = {p.name: p.read_bytes() for p in (output / "inputs").iterdir() if p.is_file()}
    assert set(files) == {p.name for p in (repository / "examples" / "hero").iterdir() if p.is_file()}
    for name, raw in files.items():
        assert (repository / "examples" / "hero" / name).read_bytes() == raw
    return {"exit": completed.returncode, "report": json.loads((output / "reports" / "report.json").read_bytes()),
            "markdown": (output / "reports" / "report.md").read_bytes().decode("utf-8"),
            "stdout": completed.stdout, "stderr": completed.stderr, "installed_identity": proof, "root": root,
            "input_sha256": {name: hashlib.sha256(raw).hexdigest() for name, raw in files.items()},
            "network_attempts": 0, "inputs_unchanged": True}


def test_phase4_step9_markdown_newlines_are_not_silently_normalized(phase4_step9_hero_observations):
    actual = phase4_step9_hero_observations[False]
    for changed in (actual["markdown"].replace("\n", "\r\n"), actual["markdown"].rstrip("\n")):
        with pytest.raises(ValueError, match="line endings"):
            NORMALIZER["normalize_markdown"](changed, actual["report"], actual["normalized"])


def phase4_step9_assert_all_markdown_fields(report, text):
    """Decode table/narrative arrays and account for every analytical JSON leaf.

    This parser comes from the independent candidate reviewer. It does not call
    production renderers; compact arrays, nested objects and null rows retain
    their original types and positions. The explanatory summaries are checked
    separately by phase4_step9_assert_markdown_envelopes.
    """
    import re
    def tokens(value):
        return [json.loads(token) for token in re.findall(r'\[("(?:[^"\\]|\\.)*"|[0-9]+)\]', value)]
    def cell(value):
        value = value.strip()
        if value.startswith("Unavailable (null)"):
            return None
        if value.startswith("`") and value.endswith("`"):
            value = value[1:-1]
        return json.loads(value)
    def get(value, path):
        for part in path:
            value = value[part]
        return value
    def leaves(value, path=()):
        if isinstance(value, dict) and value:
            for key, child in value.items():
                yield from leaves(child, (*path, key))
        elif isinstance(value, list) and value:
            for index, child in enumerate(value):
                yield from leaves(child, (*path, index))
        else:
            yield path, value
    def envelopes(value, path=()):
        if isinstance(value, dict):
            if "evidence_class" in value:
                yield path, value
            else:
                for key, child in value.items():
                    yield from envelopes(child, (*path, key))
        elif isinstance(value, list):
            for index, child in enumerate(value):
                yield from envelopes(child, (*path, index))
    def exact(left, right):
        assert json.dumps(left, sort_keys=True, ensure_ascii=False) == json.dumps(right, sort_keys=True, ensure_ascii=False)
    hits = list(re.finditer(r'^### Analytical result\n\n`([^\n]+)`\n', text, re.M))
    expected, seen = dict(envelopes(report)), set()
    for index, match in enumerate(hits):
        path = tuple(tokens(match.group(1)))
        assert path not in seen
        seen.add(path)
        obj = get(report, path)
        endpoint = hits[index + 1].start() if index + 1 < len(hits) else len(text)
        block = text[match.end():endpoint]
        next_section = re.search(r'^## ', block, re.M)
        if next_section:
            block = block[:next_section.start()]
        covered = set()
        for row in re.finditer(r'^\| `((?:\[[^\n]+)+)` \| (.+) \|$', block, re.M):
            subpath, value = tuple(tokens(row.group(1))), cell(row.group(2))
            exact(get(obj, subpath), value)
            paths = {key for key, _ in leaves(value, subpath)}
            assert not paths.intersection(covered)
            covered.update(paths)
        titles = list(re.finditer(r'^\*\*`([^\n]+)`\*\*\n', block, re.M))
        for offset, title in enumerate(titles):
            subpath = tuple(tokens(title.group(1)))
            array = get(obj, subpath)
            chunk = block[title.end():titles[offset + 1].start() if offset + 1 < len(titles) else len(block)]
            if not isinstance(array, list):
                continue
            bullets = re.findall(r'^- (.+)$', chunk, re.M)
            if bullets:
                decoded = [cell(item) for item in bullets]
            else:
                rows = [line for line in chunk.splitlines() if line.startswith("|")]
                if not rows:
                    continue
                fields = [cell(item) for item in rows[0].strip("|").split("|")]
                decoded = [dict(zip(fields, [cell(item) for item in row.strip("|").split("|")], strict=True)) for row in rows[2:]]
            exact(array, decoded)
            paths = {key for key, _ in leaves(array, subpath)}
            assert not paths.intersection(covered)
            covered.update(paths)
        assert covered == {key for key, _ in leaves(obj)}, path
    assert seen == set(expected)
