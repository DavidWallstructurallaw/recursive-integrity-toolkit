"""Phase 4 Step 9: exact-slot golden normalization, never expectation approval.

P4-D08 permits metadata and explicitly declared test-root prefixes only. Input
hashes are verified against supplied bytes; config hashes are verified before
recomputing the same independent declaration with its test-root prefix changed.
No runtime renderer or hash helper is used. Imports have no I/O side effects.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
import stat
from pathlib import Path
import unicodedata


RUN_METADATA = {
    "run_id": "phase4-step9-golden",
    "started_at": "2000-01-01T00:00:00+00:00",
    "completed_at": "2000-01-01T00:00:00+00:00",
    "duration_seconds": 0.0,
    "python_version": "3.test",
    "platform": "golden-test",
}
ROOT_TOKEN = "<TEST_ROOT>"


def _canonical_hash(value):
    encoded = json.dumps(value, ensure_ascii=True, sort_keys=True,
                         separators=(",", ":"), allow_nan=False).encode("ascii")
    return hashlib.sha256(encoded).hexdigest()


def _declared_config_hash(declaration):
    return _canonical_hash({key: declaration[key] for key in ("encoding", "options")})


def _root_prefix(value, test_root):
    if type(value) is not str:
        raise ValueError("declared path must be literal text")
    root = Path(test_root).absolute()
    candidate = Path(value)
    try:
        relative = candidate.relative_to(root)
    except ValueError:
        raise ValueError("declared input/output path escapes explicit test root") from None
    if ".." in relative.parts:
        raise ValueError("declared path contains parent traversal")
    return ROOT_TOKEN + ("/" + relative.as_posix() if relative.parts else "")


def normalize_report(payload, *, test_root, declared_config):
    """Copy a report while changing only the closed P4-D08 slot allowlist.

    ``declared_config`` is independently assembled from the input contract,
    including defaults, with encoding ``rit.phase4.config.v1``. It must not be
    copied from a production hash function. Each inventory hash and size is
    checked against that declaration's input bytes, including redacted inputs.
    """
    from recursive_integrity_toolkit.result import validate_report
    validate_report(payload)
    if (type(declared_config) is not dict or set(declared_config) != {"encoding", "options", "input_inventory"}
            or declared_config["encoding"] != "rit.phase4.config.v1"):
        raise ValueError("explicit independent resolved configuration is required")
    if payload["run"]["config_hash"] != _declared_config_hash(declared_config):
        raise ValueError("configuration hash differs from independently declared meaning")
    normalized_config = deepcopy(declared_config)
    declared_inputs = declared_config["input_inventory"]
    calculation_inputs = [item for item in declared_inputs if item["role"] != "config"]
    if calculation_inputs != declared_config["options"]["inputs"]:
        raise ValueError("inventory declarations differ from hashed input declarations")
    by_role = {}
    for item in declared_inputs:
        by_role.setdefault(item["role"], []).append(item)
    artifacts = payload.get("inputs", {}).get("artifacts", [])
    if (len(artifacts) != len(declared_inputs) or
            sorted(item["role"] for item in artifacts) != sorted(item["role"] for item in declared_inputs)):
        raise ValueError("inventory differs from independently declared inputs")
    result = deepcopy(payload)
    for index, artifact in enumerate(artifacts):
        candidates = by_role.get(artifact["role"], [])
        if len(candidates) != 1:
            raise ValueError("golden inventory roles must identify one declared input")
        source = Path(candidates[0]["path"])
        raw = source.read_bytes()
        if artifact["file_hash"] != hashlib.sha256(raw).hexdigest() or artifact["size_bytes"] != len(raw):
            raise ValueError("input hash or size differs from supplied bytes")
        if artifact["path"] is not None:
            if artifact["path"] != str(source):
                raise ValueError("inventory path differs from independent input declaration")
            result["inputs"]["artifacts"][index]["path"] = _root_prefix(str(source), test_root)
    expected_hashes = [{"artifact_index": index, "algorithm": "sha256", "value": item["file_hash"]}
                       for index, item in enumerate(artifacts)]
    if payload.get("inputs", {}).get("file_hashes") != expected_hashes:
        raise ValueError("input hash mirror differs from verified inventory")
    for name, value in RUN_METADATA.items():
        # Missing metadata and its null reasons remain visible and cannot be
        # silently filled by normalization.
        if result["run"][name] is not None:
            result["run"][name] = value
    for item in normalized_config["options"]["inputs"]:
        item["path"] = _root_prefix(item["path"], test_root)
    output = normalized_config["options"]["output"]
    output["directory"] = _root_prefix(output["directory"], test_root)
    result["run"]["config_hash"] = _declared_config_hash(normalized_config)
    validate_report(result)
    return result


def _markdown_literal(value):
    if type(value) in (int, float):
        return repr(value)
    encoded = json.dumps(value, ensure_ascii=False, allow_nan=False, sort_keys=True,
                         separators=(", ", ": "))
    parts = []
    for character in encoded:
        if character in "`|<>&" or unicodedata.category(character) in {"Cc", "Cf", "Zl", "Zp"}:
            point = ord(character)
            if point <= 0xFFFF:
                parts.append(f"\\u{point:04x}")
            else:
                point -= 0x10000
                parts.append(f"\\u{0xD800 + (point >> 10):04x}\\u{0xDC00 + (point & 0x3FF):04x}")
        else:
            parts.append(character)
    return "`" + "".join(parts) + "`"


def normalize_markdown(text, original, normalized):
    """Replace only exact metadata/inventory rows in their registered sections.

    The existing Markdown is inspected and retained. It is never regenerated
    from JSON; absent, duplicated, malformed or contradictory rows fail closed.
    Narrative, metric rows and all unlisted sections retain their exact bytes.
    """
    if "\r" in text or not text.endswith("\n"):
        raise ValueError("Markdown must retain exact LF line endings and final newline")
    changes = []
    for name in (*RUN_METADATA, "config_hash"):
        old, new = original["run"][name], normalized["run"][name]
        if old is not None:
            changes.append(("Run metadata", f'| `["{name}"]` | {_markdown_literal(old)} |',
                            f'| `["{name}"]` | {_markdown_literal(new)} |'))
    for index, artifact in enumerate(original.get("inputs", {}).get("artifacts", [])):
        old, new = artifact["path"], normalized["inputs"]["artifacts"][index]["path"]
        if old != new:
            field = f'`["artifacts"][{index}]["path"]`'
            changes.append(("Input inventory", f"| {field} | {_markdown_literal(old)} |",
                            f"| {field} | {_markdown_literal(new)} |"))
    lines = text.splitlines(keepends=True)
    section = None
    seen = [0] * len(changes)
    result = []
    summary_old = "- Run ID: " + _markdown_literal(original["run"]["run_id"]) + "."
    summary_new = "- Run ID: " + _markdown_literal(normalized["run"]["run_id"]) + "."
    summary_count = 0
    for line in lines:
        body = line.removesuffix("\n")
        if body.startswith("## "):
            section = body[3:]
        if section is None and body == summary_old:
            summary_count += 1
            line = summary_new + ("\n" if line.endswith("\n") else "")
        for index, (required, old, new) in enumerate(changes):
            if section == required and body == old:
                seen[index] += 1
                line = new + ("\n" if line.endswith("\n") else "")
        result.append(line)
    if summary_count != 1 or any(count != 1 for count in seen):
        raise ValueError("Markdown metadata rows are missing, duplicate or inconsistent with JSON")
    return "".join(result)


def assert_golden_pair(actual_json, actual_markdown, expected_json, expected_markdown):
    """Require every literal field and every Markdown byte to agree."""
    if json.dumps(actual_json, sort_keys=True, ensure_ascii=False, allow_nan=False) != json.dumps(expected_json, sort_keys=True, ensure_ascii=False, allow_nan=False):
        raise AssertionError("JSON golden differs; review substantive evidence before acceptance")
    if actual_markdown != expected_markdown:
        raise AssertionError("Markdown golden differs; review the human-readable artifact")


def _scratch_destination(value, repo_root):
    spelling = str(value)
    if spelling.startswith(("//", "\\\\")):
        raise ValueError("scratch destination cannot use remote or aliased roots")
    path = Path(value).absolute()
    if ".." in Path(value).parts or not Path(value).is_absolute():
        raise ValueError("scratch destination must be an explicit absolute path")
    for candidate in reversed((path, *path.parents)):
        try:
            info = candidate.lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(info.st_mode) or getattr(info, "st_reparse_tag", 0):
            raise ValueError("scratch destination cannot traverse a symlink or reparse point")
    resolved = path.resolve()
    repositories = (Path(repo_root).resolve(), Path(__file__).resolve().parents[1])
    if any(resolved == repository or repository in resolved.parents for repository in repositories):
        raise ValueError("scratch destination cannot be inside the repository")
    if path.exists() or not path.parent.is_dir():
        raise ValueError("scratch destination must be new with an existing parent")
    return resolved


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report-json", required=True, type=Path)
    parser.add_argument("--report-markdown", required=True, type=Path)
    parser.add_argument("--declared-config", required=True, type=Path)
    parser.add_argument("--test-root", required=True, type=Path)
    parser.add_argument("--scratch-out", required=True, type=Path)
    args = parser.parse_args(argv)
    destination = _scratch_destination(args.scratch_out, Path(__file__).resolve().parents[1])
    original = json.loads(args.report_json.read_bytes())
    normalized = normalize_report(original, test_root=args.test_root,
                                  declared_config=json.loads(args.declared_config.read_bytes()))
    markdown = normalize_markdown(args.report_markdown.read_bytes().decode("utf-8"), original, normalized)
    destination.mkdir(mode=0o700)
    (destination / "report.json").write_text(json.dumps(normalized, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    (destination / "report.md").write_text(markdown, encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
