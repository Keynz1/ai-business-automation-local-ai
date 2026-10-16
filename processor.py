from __future__ import annotations

from ai_client import classify_request
from api_client import enrich_request
from logging_utils import write_processing_report
from models import BusinessRequest, ProcessedRequest


def generate_response(request: BusinessRequest, enrichment: dict) -> str:
    priority_text = "High priority. " if request.priority in {"high", "urgent"} else ""
    action = request.requested_action or "Review request"
    type_labels = {
        "automation": "automation request",
        "data_cleanup": "data cleanup request",
        "reporting": "reporting request",
        "general": "request",
    }
    label = type_labels.get(request.request_type, "request")
    return (
        f"Hello {request.customer_name}. {priority_text}"
        f"We received your {label}: {request.summary}. "
        f"Next step: {action}."
    )


def process_request(
    text: str,
    *,
    model: str = "qwen2:1.5b",
    endpoint: str | None = None,
) -> ProcessedRequest:
    request = classify_request(text, model=model)
    enrichment = enrich_request(request, endpoint)
    response_text = generate_response(request, enrichment)
    return ProcessedRequest.from_business_request(
        request,
        api_status=str(enrichment.get("api_status", "unknown")),
        response_text=response_text,
        processing_status="processed",
    )
