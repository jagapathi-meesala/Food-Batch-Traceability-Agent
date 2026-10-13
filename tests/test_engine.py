from core.engine import build_traceability, prepare_recall_summary, validate_dataset

def sample():
    return {"ingredient_lots":[{"lot_id":"L1","ingredient":"flour","supplier":"S1","received_date":"2026-01-01","quantity":10}],
            "production_batches":[{"batch_id":"B1","product":"bread","production_date":"2026-01-02","input_lot_ids":["L1"],"quantity":8}],
            "shipments":[{"shipment_id":"SHP1","batch_id":"B1","destination":"Shop A","ship_date":"2026-01-03","quantity":8}]}

def test_valid_dataset():
    assert validate_dataset(sample()) == []

def test_unknown_lot_flagged():
    data = sample(); data["production_batches"][0]["input_lot_ids"] = ["MISSING"]
    assert any("unknown lot_id" in issue for issue in validate_dataset(data))

def test_unknown_batch_shipment_flagged():
    data = sample(); data["shipments"][0]["batch_id"] = "MISSING"
    assert any("unknown batch_id" in issue for issue in validate_dataset(data))

def test_duplicate_lot_id_flagged():
    data = sample(); data["ingredient_lots"].append(dict(data["ingredient_lots"][0]))
    assert any("Duplicate lot_id" in issue for issue in validate_dataset(data))

def test_links_built():
    result = build_traceability(sample())
    assert result["traceability_links"][0]["input_lots"][0]["known"] is True

def test_shipments_linked():
    result = build_traceability(sample())
    assert result["traceability_links"][0]["shipments"][0]["shipment_id"] == "SHP1"

def test_recall_summary_found():
    assert prepare_recall_summary(sample(), "B1")["found"] is True

def test_unknown_recall_batch():
    assert prepare_recall_summary(sample(), "NOPE")["found"] is False
