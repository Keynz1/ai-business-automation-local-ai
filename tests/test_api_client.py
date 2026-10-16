import requests

import api_client
from models import normalize_payload


class FakeResponse:
    def __init__(self, status_code=200, payload=None):
        self.status_code = status_code
        self._payload = payload or {}

    def json(self):
        return self._payload


def test_no_endpoint_is_deterministic_local():
    result = api_client.enrich_request(normalize_payload({"company": "Acme"}))
    assert result == {"api_status": "demo-local", "enrichment_note": "No external API configured"}


def test_successful_endpoint(monkeypatch):
    monkeypatch.setattr(api_client.requests, "post", lambda *a, **k: FakeResponse(200, {"note": "CRM matched"}))
    result = api_client.enrich_request(normalize_payload({}), "https://example.test/enrich")
    assert result["api_status"] == "ok"
    assert result["enrichment_note"] == "CRM matched"


def test_timeout_is_nonfatal(monkeypatch):
    def boom(*a, **k):
        raise requests.Timeout("slow")
    monkeypatch.setattr(api_client.requests, "post", boom)
    result = api_client.enrich_request(normalize_payload({}), "https://example.test/enrich")
    assert result["api_status"] == "timeout"
    assert "timed out" in result["enrichment_note"].lower()


def test_non_200_is_nonfatal(monkeypatch):
    monkeypatch.setattr(api_client.requests, "post", lambda *a, **k: FakeResponse(503, {}))
    result = api_client.enrich_request(normalize_payload({}), "https://example.test/enrich")
    assert result["api_status"] == "http-503"
