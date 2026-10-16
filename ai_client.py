from __future__ import annotations

import json
import re

import requests

from models import BusinessRequest, normalize_payload

EMAIL_RE = re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.I)


def fallback_parse(text: str) -> BusinessRequest:
    lower = text.lower()
    if "excel" in lower or "csv" in lower or "cleanup" in lower or "clean up" in lower:
        request_type = "data_cleanup"
    elif "api" in lower or "automat" in lower or "workflow" in lower:
        request_type = "automation"
    elif "report" in lower:
        request_type = "reporting"
    else:
        request_type = "general"

    priority = "urgent" if any(word in lower for word in ("urgent", "asap", "immediately")) else "normal"
    email_match = EMAIL_RE.search(text)
    payload = {
        "email": email_match.group(0) if email_match else "",
        "request_type": request_type,
        "priority": priority,
        "summary": text.strip() or "No summary provided",
        "requested_action": "Review request",
        "confidence": 0.35,
    }
    return normalize_payload(payload)


def classify_request(
    text: str,
    model: str = "qwen2:1.5b",
    ollama_url: str = "http://127.0.0.1:11434",
) -> BusinessRequest:
    prompt = (
        "Return ONLY strict JSON with keys customer_name, company, email, request_type, "
        "priority, summary, requested_action, confidence. Priority must be low, normal, high, or urgent. "
        f"Customer request: {text}"
    )
    try:
        response = requests.post(
            f"{ollama_url.rstrip('/')}/api/generate",
            json={"model": model, "prompt": prompt, "stream": False, "format": "json"},
            timeout=20,
        )
        response.raise_for_status()
        body = response.json()
        raw = body.get("response", "")
        payload = json.loads(raw)
        if not isinstance(payload, dict):
            raise ValueError("Ollama response is not an object")
        return normalize_payload(payload)
    except (requests.RequestException, ValueError, TypeError, json.JSONDecodeError, KeyError):
        return fallback_parse(text)
