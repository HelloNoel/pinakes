"""Run with: python -m pip install jsonschema pyyaml; python tests/validate.py."""
import json
from pathlib import Path
import jsonschema
import yaml

root = Path(__file__).resolve().parents[1]
validators = {}
for kind, filename in [("index", "pinakes.schema.json"), ("registry", "registry.schema.json")]:
    schema = json.loads((root / "schema" / filename).read_text())
    jsonschema.Draft202012Validator.check_schema(schema)
    validators[kind] = jsonschema.Draft202012Validator(schema)
cases = json.loads((root / "tests" / "validation.json").read_text())
for case in cases:
    errors = list(validators[case["kind"]].iter_errors(case["value"]))
    assert (not errors) == case["valid"], (case["name"], [e.message for e in errors])
examples = list((root / "examples").glob("*.yaml"))
for path in examples:
    kind = "registry" if path.name == "registry.yaml" else "index"
    validators[kind].validate(yaml.safe_load(path.read_text()))
print(f"Validated {len(cases)} shared cases and {len(examples)} examples against both schemas")
