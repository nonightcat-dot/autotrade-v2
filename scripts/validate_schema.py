import json
from pathlib import Path

try:
    from jsonschema import validate
except ImportError:
    print("Please install jsonschema: pip install jsonschema")
    raise

BASE_DIR = Path(__file__).resolve().parents[1]

schema_path = BASE_DIR / "schemas" / "autotrade_v2.schema.json"
sample_path = BASE_DIR / "schemas" / "examples" / "barrow.sample.json"

with open(schema_path, "r", encoding="utf-8") as f:
    schema = json.load(f)

with open(sample_path, "r", encoding="utf-8") as f:
    sample = json.load(f)

validate(instance=sample, schema=schema)

print("Schema validation passed.")
