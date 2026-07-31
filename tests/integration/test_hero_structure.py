"""Validate the approved hero files as format fixtures only.

No support, diversity, provenance-share, lineage, ancestry, or other analytical
value is calculated in this test module.
"""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path


HERO_FILES = {
    "records_v1.csv",
    "records_v2.csv",
    "provenance.csv",
    "version_order.json",
    "config.json",
    "EXPECTED_OUTPUTS.md",
}
RECORD_FIELDS = ["record_id", "dataset_version", "content", "topic"]
PROVENANCE_FIELDS = [
    "dataset_version",
    "record_id",
    "source_type",
    "provenance_confidence",
    "parent_ids",
    "generator_id",
    "generator_version",
    "transformation",
    "generation",
    "human_reviewed",
    "external_grounding",
]
COMPOSITE_PARENT = re.compile(r"^[^:]+::[^:]+$")


def _read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def test_hero_file_set_and_csv_structure(repo_root: Path) -> None:
    hero = repo_root / "examples" / "hero"
    assert {path.name for path in hero.iterdir() if path.is_file()} == HERO_FILES

    v1_fields, v1_rows = _read_csv(hero / "records_v1.csv")
    v2_fields, v2_rows = _read_csv(hero / "records_v2.csv")
    provenance_fields, provenance_rows = _read_csv(hero / "provenance.csv")

    assert v1_fields == RECORD_FIELDS
    assert v2_fields == RECORD_FIELDS
    assert provenance_fields == PROVENANCE_FIELDS
    assert len(v1_rows) == 8
    assert len(v2_rows) == 8
    assert len(provenance_rows) == 16


def test_hero_json_and_composite_parent_references(repo_root: Path) -> None:
    hero = repo_root / "examples" / "hero"
    version_order = json.loads((hero / "version_order.json").read_text(encoding="utf-8"))
    config = json.loads((hero / "config.json").read_text(encoding="utf-8"))

    assert version_order == {"version_order": ["v1", "v2"]}
    assert config["representation"]["name"] == "topic"
    assert config["representation"]["field"] == "topic"
    assert config["representation"]["version"] == "hero-topic-v1"

    _, rows = _read_csv(hero / "provenance.csv")
    for row in rows:
        parents = json.loads(row["parent_ids"])
        assert isinstance(parents, list)
        if row["dataset_version"] == "v1":
            assert parents == []
        else:
            assert parents
            assert all(COMPOSITE_PARENT.fullmatch(parent) for parent in parents)


def test_expected_outputs_contains_approved_reference_contract(repo_root: Path) -> None:
    text = (repo_root / "examples" / "hero" / "EXPECTED_OUTPUTS.md").read_text(
        encoding="utf-8"
    )
    required_reference_lines = {
        "v1 support size: 8",
        "v2 support size: 5",
        "v1 Gini-Simpson diversity: 0.875",
        "v2 Gini-Simpson diversity: 0.75",
        "direct closure lower bound: 0.5",
        "direct closure upper bound: 0.5",
        "ancestry HHI: 0.25",
        "effective external-root count: 4.0",
        "No universal risk level is approved.",
        "none in the default hero audit",
    }
    for line in required_reference_lines:
        assert line in text
    assert "Phase 1 Step 6 does not calculate" in text
