from pathlib import Path

import processor
from models import normalize_payload


def fake_classify(text, model="qwen2:1.5b"):
    return normalize_payload({
        "customer_name": "Nina",
        "company": "Orbit",
        "email": "nina@example.com",
        "request_type": "automation",
        "priority": "high",
        "summary": "Automate lead intake",
        "requested_action": "Build workflow",
        "confidence": 0.9,
    })


def test_process_request_builds_processed_record(monkeypatch):
    monkeypatch.setattr(processor, "classify_request", fake_classify)
    monkeypatch.setattr(processor, "enrich_request", lambda req, endpoint=None: {"api_status": "ok", "enrichment_note": "CRM matched"})
    item = processor.process_request("Please automate this")
    assert item.customer_name == "Nina"
    assert item.api_status == "ok"
    assert item.processing_status == "processed"
    assert "Nina" in item.response_text
    assert "high priority" in item.response_text.lower()


def test_rest_failure_still_returns_processed(monkeypatch):
    monkeypatch.setattr(processor, "classify_request", fake_classify)
    monkeypatch.setattr(processor, "enrich_request", lambda req, endpoint=None: {"api_status": "timeout", "enrichment_note": "API timed out"})
    item = processor.process_request("Please automate this", endpoint="https://example.test")
    assert item.processing_status == "processed"
    assert item.api_status == "timeout"


def test_ai_fallback_result_is_accepted(monkeypatch):
    monkeypatch.setattr(processor, "classify_request", lambda text, model="qwen2:1.5b": normalize_payload({"summary": text, "request_type": "general"}))
    item = processor.process_request("plain request")
    assert item.request_type == "general"
    assert item.response_text


def test_processing_report_contains_records(tmp_path: Path):
    base = fake_classify("x")
    item = processor.ProcessedRequest.from_business_request(base, api_status="demo-local", response_text="Done", processing_status="processed")
    path = processor.write_processing_report([item], tmp_path / "report.txt")
    text = path.read_text(encoding="utf-8")
    assert item.request_id in text
    assert "processed" in text
