import requests

import ai_client


class FakeResponse:
    def __init__(self, payload, status_code=200):
        self._payload = payload
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(str(self.status_code))

    def json(self):
        return self._payload


def test_valid_ollama_json_response(monkeypatch):
    payload = '{"customer_name":"Mira","company":"Nova","email":"mira@example.com","request_type":"automation","priority":"high","summary":"Automate reports","requested_action":"Build workflow","confidence":0.91}'
    monkeypatch.setattr(ai_client.requests, "post", lambda *a, **k: FakeResponse({"response": payload}))
    item = ai_client.classify_request("hello")
    assert item.customer_name == "Mira"
    assert item.request_type == "automation"
    assert item.priority == "high"
    assert item.confidence == 0.91


def test_malformed_model_response_uses_fallback(monkeypatch):
    monkeypatch.setattr(ai_client.requests, "post", lambda *a, **k: FakeResponse({"response": "not-json"}))
    item = ai_client.classify_request("Contact bob@example.com about urgent Excel cleanup")
    assert item.email == "bob@example.com"
    assert item.priority == "urgent"
    assert item.request_type == "data_cleanup"


def test_unavailable_ollama_uses_fallback(monkeypatch):
    def boom(*args, **kwargs):
        raise requests.ConnectionError("offline")
    monkeypatch.setattr(ai_client.requests, "post", boom)
    item = ai_client.classify_request("Need API automation for Acme")
    assert item.request_type == "automation"
    assert item.company == "Unknown"


def test_missing_model_fields_receive_defaults(monkeypatch):
    monkeypatch.setattr(ai_client.requests, "post", lambda *a, **k: FakeResponse({"response": "{}"}))
    item = ai_client.classify_request("anything")
    assert item.customer_name == "Unknown"
    assert item.priority == "normal"
    assert item.summary == "No summary provided"
