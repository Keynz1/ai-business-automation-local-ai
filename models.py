from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


@dataclass
class BusinessRequest:
    request_id: str
    received_at: str
    customer_name: str
    company: str
    email: str
    request_type: str
    priority: str
    summary: str
    requested_action: str
    confidence: float


@dataclass
class ProcessedRequest(BusinessRequest):
    api_status: str
    response_text: str
    processing_status: str

    @classmethod
    def from_business_request(
        cls,
        request: BusinessRequest,
        *,
        api_status: str,
        response_text: str,
        processing_status: str,
    ) -> "ProcessedRequest":
        return cls(**asdict(request), api_status=api_status, response_text=response_text, processing_status=processing_status)

    def to_row(self) -> dict[str, Any]:
        return {field.name: getattr(self, field.name) for field in fields(self)}


def _text(value: Any, default: str) -> str:
    if value is None:
        return default
    value = str(value).strip()
    return value if value else default


def normalize_payload(payload: dict) -> BusinessRequest:
    raw_priority = _text(payload.get("priority"), "normal").lower()
    priority = raw_priority if raw_priority in {"low", "normal", "high", "urgent"} else "normal"
    try:
        confidence = float(payload.get("confidence", 0.0) or 0.0)
    except (TypeError, ValueError):
        confidence = 0.0
    confidence = max(0.0, min(1.0, confidence))

    return BusinessRequest(
        request_id=_text(payload.get("request_id"), str(uuid4())),
        received_at=_text(payload.get("received_at"), datetime.now(timezone.utc).isoformat()),
        customer_name=_text(payload.get("customer_name"), "Unknown"),
        company=_text(payload.get("company"), "Unknown"),
        email=str(payload.get("email") or "").strip(),
        request_type=_text(payload.get("request_type"), "general").lower(),
        priority=priority,
        summary=_text(payload.get("summary"), "No summary provided"),
        requested_action=_text(payload.get("requested_action"), "Review request"),
        confidence=confidence,
    )
