# Food Batch Traceability Agent

A local, explainable tool for validating batch records and linking ingredient lots, production batches, and shipments for traceability and recall-support workflows.

## Features
- Validates required batch, product, date, and quantity fields.
- Links input ingredient lots to production batches and output shipments using supplied IDs.
- Flags orphaned references, duplicate IDs, and missing links.
- Produces a traceability summary for human-led mock recall review.
- Uses only the supplied records; it does not infer undocumented lot relationships.

## Run
```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m pytest -q
python3 verification/readiness_audit.py
python3 -m core.cli examples/batch_records.json
```
If the OpenGAP CLI is installed, run `opengap validate` from this directory.

## Limitations
Traceability quality depends on the completeness and correctness of source records. This tool does not test food, determine contamination, certify regulatory compliance, or replace a qualified food-safety and recall team.
