"""Phase 4 Step 9: create review candidates in an explicit scratch directory.

Candidates never approve or overwrite accepted expectations. The independent
oracle must already exist; its identity is recorded in the candidate manifest.
Both real CLI report formats are retained and compared only after human-readable
review. Fixed metadata and an injected public test-only key ensure repeatability.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager, redirect_stderr, redirect_stdout
import hashlib
import io
import json
from pathlib import Path
import runpy
from unittest.mock import patch


TEST_KEY = b"phase4-step9-fixed-test-key-000000"
HERO_SEMANTICS = "Hero topic labels retain their literal meaning across v1 and v2."


def _normalizer():
    return runpy.run_path(str(Path(__file__).with_name("normalize_golden.py")), run_name="golden_normalizer")


@contextmanager
def fixed_metadata():
    """Inject test metadata/key without changing calculations or runtime files."""
    from recursive_integrity_toolkit import cli
    from recursive_integrity_toolkit.reports.assembly import build_run_metadata
    from recursive_integrity_toolkit.utils.hashing import IdentifierProtection
    metadata = _normalizer()["RUN_METADATA"]
    def fixed(options, operation, started_at, started_clock, *, status="complete"):
        return build_run_metadata(options=options, operation=operation,
                                  run_status=status, **metadata)
    protection = IdentifierProtection(secret=TEST_KEY)
    with patch.object(cli, "_run_metadata", fixed), patch.object(IdentifierProtection, "create", return_value=protection):
        yield


def declared_hero_config(destination, *, redacted=False):
    """Independent explicit Hero declaration and accepted default values.

    This encoder reads no production option object and calls no production hash
    or configuration-summary function. Literal defaults follow config.py's
    frozen public resolution contract, documented in the independent oracle.
    """
    inputs = Path(destination) / "inputs"
    pairs = [("provenance_manifest", "provenance.csv"),
             ("records_compare", "records_v1.csv"), ("records_primary", "records_v2.csv"),
             ("version_order", "version_order.json")]
    return {"encoding": "rit.phase4.config.v1",
            "input_inventory": [{"role": role, "path": str(inputs / name), "format": None}
                                for role, name in [("config", "config.json"), *pairs]],
            "options": {
        "config_version": None,
        "inputs": [{"role": role, "path": str(inputs / name), "format": None} for role, name in pairs],
        "representation": {"name": "topic", "source": "topic_field", "field": "topic",
                           "version": "hero-topic-v1", "missing_value_policy": "error", "normalization_profile": None},
        "representation_compatibility": {}, "state_mapping": {}, "version_order": [],
        "privacy_mode": "redacted" if redacted else "standard", "strict_mode": False, "strict_warning_codes": [],
        "resource_limits": {"max_file_bytes": None, "max_rows": None, "max_content_bytes": None,
                            "max_parent_list_length": None, "max_json_depth": None},
        "output": {"directory": str(Path(destination) / "reports"),
                   "record_id_mode": "hash" if redacted else "preserve", "identifier_secret_source": "fresh"},
        "simulation": {"enabled": False, "seed": None}, "state_semantics": HERO_SEMANTICS,
        "missing_state_id": None, "tail_rule": None, "tail_threshold": None,
    }}


def run_example(destination, *, redacted=False):
    """Execute the real packaged example and preserve both observed formats."""
    from recursive_integrity_toolkit.cli import main
    stdout, stderr = io.StringIO(), io.StringIO()
    with fixed_metadata(), redirect_stdout(stdout), redirect_stderr(stderr):
        code = main(["example", "--out", str(destination), *(["--redacted"] if redacted else [])])
    root = Path(destination)
    report_path = root / "reports" / "report.json"
    result = {"exit_code": code, "stdout": stdout.getvalue(), "stderr": stderr.getvalue(),
              "declared_config": declared_hero_config(root, redacted=redacted)}
    if report_path.is_file():
        result["report"] = json.loads(report_path.read_bytes())
        result["markdown"] = report_path.with_suffix(".md").read_bytes().decode("utf-8")
    return result


def build_candidates(destination, repo_root=None):
    """Write candidates only; never touch the repository's accepted fixtures."""
    repository = Path(repo_root) if repo_root is not None else Path(__file__).resolve().parents[1]
    normalizer = _normalizer()
    output = normalizer["_scratch_destination"](destination, repository)
    oracle_paths = [repository / "tests/golden" / name for name in ("phase4_report_cases.md", "phase4_report_expected.json")]
    oracle_hashes = {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in oracle_paths}
    declared = json.loads(oracle_paths[1].read_bytes())
    if not declared.get("cases") or declared.get("expectations_generated_by_implementation") is not False:
        raise ValueError("independently authored expectations must exist before candidate generation")
    output.mkdir(mode=0o700)
    manifest = {"phase": 4, "step": 9, "candidate_only": True,
                "acceptance_requires_independent_review": True, "oracle_sha256": oracle_hashes, "files": {}}
    for redacted in (False, True):
        label = "redacted" if redacted else "standard"
        observed = run_example(output / label, redacted=redacted)
        if observed["exit_code"] != 0 or "report" not in observed:
            (output / (label + "-failure.json")).write_text(json.dumps(observed, indent=2) + "\n", encoding="utf-8", newline="\n")
            raise ValueError("candidate execution failed; retained observation requires review")
        normalized = normalizer["normalize_report"](observed["report"], test_root=output / label,
                                                     declared_config=observed["declared_config"])
        markdown = normalizer["normalize_markdown"](observed["markdown"], observed["report"], normalized)
        stem = "phase4_hero_redacted" if redacted else "phase4_hero_report"
        for suffix, text in (("json", json.dumps(normalized, ensure_ascii=False, allow_nan=False, indent=2) + "\n"), ("md", markdown)):
            path = output / (stem + "." + suffix)
            path.write_text(text, encoding="utf-8", newline="\n")
            manifest["files"][path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
        (output / (label + "-declared-config.json")).write_text(json.dumps(observed["declared_config"], indent=2) + "\n", encoding="utf-8", newline="\n")
        (output / (label + "-stdout.log")).write_text(observed["stdout"], encoding="utf-8", newline="\n")
        (output / (label + "-stderr.log")).write_text(observed["stderr"], encoding="utf-8", newline="\n")
    (output / "candidate-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8", newline="\n")
    return manifest


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scratch-out", required=True, type=Path,
                        help="New absolute directory outside the repository; candidates require independent review.")
    args = parser.parse_args(argv)
    build_candidates(args.scratch_out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
