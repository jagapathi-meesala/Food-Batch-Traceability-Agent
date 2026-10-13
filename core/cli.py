"""CLI for food batch traceability."""
import json, sys
from pathlib import Path
from .engine import build_traceability

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 -m core.cli <batch_records.json>")
        return 2
    try:
        data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": str(exc)}, indent=2)); return 1
    if not isinstance(data, dict):
        print(json.dumps({"error": "Input JSON must be an object."}, indent=2)); return 1
    print(json.dumps(build_traceability(data), indent=2)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
