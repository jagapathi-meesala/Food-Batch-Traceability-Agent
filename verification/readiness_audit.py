from pathlib import Path
required = [
"agent.yaml","SOUL.md","README.md","RULES.md","DUTIES.md","AGENTS.md","EXPLAINABILITY.md",
"requirements.txt",".env.example",".gitignore","pytest.ini","core/__init__.py","core/engine.py","core/cli.py",
"tools/validate-batch-record.yaml","tools/build-traceability-links.yaml","tools/prepare-recall-summary.yaml",
"skills/batch-record-validation/SKILL.md","skills/traceability-linking/SKILL.md","skills/recall-reporting/SKILL.md",
"tests/test_engine.py","examples/batch_records.json"
]
missing = [x for x in required if not Path(x).is_file()]
if missing:
    print("FAIL: missing required files: " + ", ".join(missing)); raise SystemExit(1)
print(f"PASS: all {len(required)}/{len(required)} required files present")
