from __future__ import annotations

import requests

from models import BusinessRequest


def enrich_request(request: BusinessRequest, endpoint: str | None = None) -> dict:
    if not endpoint:
        return {
            "api_status": "demo-local",
            "enrichment_note": "No external API configured",
        }

    try:
        response = requests.post(endpoint, json={
            "request_id": request.request_id,
            "company": request.company,
            "email": request.email,
            "request_type": request.request_type,
        }, timeout=10)
    except requests.Timeout:
        return {
            "api_status": "timeout",
            "enrichment_note": "External API timed out; processing continued locally",
        }
    except requests.RequestException as exc:
        return {
            "api_status": "request-error",
            "enrichment_note": f"External API unavailable: {exc}",
        }

    if response.status_code != 200:
        return {
            "api_status": f"http-{response.status_code}",
            "enrichment_note": "External API returned a non-success status; processing continued locally",
        }

    try:
        payload = response.json()
    except ValueError:
        payload = {}
    return {
        "api_status": "ok",
        "enrichment_note": str(payload.get("note") or "External API enrichment completed"),
    }
