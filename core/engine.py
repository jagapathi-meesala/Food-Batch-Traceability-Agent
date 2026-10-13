"""Food batch traceability validation and link building."""
from typing import Any

def validate_dataset(data: dict[str, Any]) -> list[str]:
    issues = []
    sections = (("ingredient_lots", "lot_id"), ("production_batches", "batch_id"), ("shipments", "shipment_id"))
    seen = {name: set() for name, _ in sections}
    for section, id_key in sections:
        records = data.get(section, [])
        if not isinstance(records, list):
            issues.append(f"{section} must be a list")
            continue
        for index, record in enumerate(records):
            if not isinstance(record, dict):
                issues.append(f"{section}[{index}] must be an object")
                continue
            if not record.get(id_key):
                issues.append(f"{section}[{index}] missing {id_key}")
                continue
            rid = str(record[id_key])
            if rid in seen[section]:
                issues.append(f"Duplicate {id_key}: {rid}")
            seen[section].add(rid)
            for field in (("ingredient", "supplier", "received_date", "quantity") if section == "ingredient_lots" else
                          ("product", "production_date", "input_lot_ids", "quantity") if section == "production_batches" else
                          ("batch_id", "destination", "ship_date", "quantity")):
                if field not in record or record[field] in ("", None):
                    issues.append(f"{section}[{index}] missing {field}")
    lots = {str(x.get("lot_id")) for x in data.get("ingredient_lots", []) if isinstance(x, dict) and x.get("lot_id")}
    batches = {str(x.get("batch_id")) for x in data.get("production_batches", []) if isinstance(x, dict) and x.get("batch_id")}
    for batch in data.get("production_batches", []) if isinstance(data.get("production_batches", []), list) else []:
        if isinstance(batch, dict):
            for lot_id in batch.get("input_lot_ids", []) if isinstance(batch.get("input_lot_ids", []), list) else []:
                if str(lot_id) not in lots:
                    issues.append(f"Production batch {batch.get('batch_id')} references unknown lot_id: {lot_id}")
    for shipment in data.get("shipments", []) if isinstance(data.get("shipments", []), list) else []:
        if isinstance(shipment, dict) and shipment.get("batch_id") and str(shipment["batch_id"]) not in batches:
            issues.append(f"Shipment {shipment.get('shipment_id')} references unknown batch_id: {shipment['batch_id']}")
    return issues

def build_traceability(data: dict[str, Any]) -> dict[str, Any]:
    issues = validate_dataset(data)
    lots = {str(x["lot_id"]): x for x in data.get("ingredient_lots", []) if isinstance(x, dict) and x.get("lot_id")}
    batches = {str(x["batch_id"]): x for x in data.get("production_batches", []) if isinstance(x, dict) and x.get("batch_id")}
    shipments_by_batch: dict[str, list] = {}
    for shipment in data.get("shipments", []):
        if isinstance(shipment, dict) and shipment.get("batch_id"):
            shipments_by_batch.setdefault(str(shipment["batch_id"]), []).append(shipment)
    links = []
    for batch_id, batch in batches.items():
        input_ids = batch.get("input_lot_ids", []) if isinstance(batch.get("input_lot_ids", []), list) else []
        links.append({
            "batch_id": batch_id,
            "input_lots": [{"lot_id": str(lot_id), "known": str(lot_id) in lots} for lot_id in input_ids],
            "shipments": [{"shipment_id": s.get("shipment_id"), "destination": s.get("destination"), "quantity": s.get("quantity")} for s in shipments_by_batch.get(batch_id, [])]
        })
    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "counts": {"ingredient_lots": len(lots), "production_batches": len(batches), "shipments": sum(len(v) for v in shipments_by_batch.values())},
        "traceability_links": links,
        "limitations": "Links reflect supplied records only; completeness and food safety are not certified."
    }

def prepare_recall_summary(data: dict[str, Any], batch_id: str) -> dict[str, Any]:
    result = build_traceability(data)
    match = next((item for item in result["traceability_links"] if item["batch_id"] == str(batch_id)), None)
    if match is None:
        return {"found": False, "batch_id": batch_id, "message": "Batch ID not found in supplied records.", "issues": result["issues"]}
    return {"found": True, "batch_id": batch_id, "input_lots": match["input_lots"], "known_shipments": match["shipments"], "dataset_issues": result["issues"], "human_review_required": True}
