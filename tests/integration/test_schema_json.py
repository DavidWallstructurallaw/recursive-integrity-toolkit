"""Check that the five approved schema files are legal JSON scaffold documents."""

import json


EXPECTED = {
    "report.schema.json",
    "config.schema.json",
    "schema_mapping.schema.json",
    "version_order.schema.json",
    "normalized_manifest.schema.json",
}


def test_schema_file_set_is_exact(schema_root) -> None:
    assert {path.name for path in schema_root.glob("*.json")} == EXPECTED


def test_all_schemas_parse_as_json(schema_root) -> None:
    for path in sorted(schema_root.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        assert data["$schema"] == "https://json-schema.org/draft/2020-12/schema"
        assert data["type"] == "object"
        assert data["additionalProperties"] is False
        assert isinstance(data.get("description"), str) and data["description"]
