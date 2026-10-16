from pathlib import Path

from models import ProcessedRequest


def write_processing_report(items: list[ProcessedRequest], path: Path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["AI Business Automation Processing Report", "=" * 40, ""]
    for item in items:
        lines.extend([
            f"Request ID: {item.request_id}",
            f"Customer: {item.customer_name}",
            f"Type: {item.request_type}",
            f"Priority: {item.priority}",
            f"API status: {item.api_status}",
            f"Processing status: {item.processing_status}",
            f"Response: {item.response_text}",
            "",
        ])
    path.write_text("\n".join(lines), encoding="utf-8")
    return path
