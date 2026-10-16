# AI Business Automation — Local AI + Excel/CSV + REST API

A portfolio-ready Python workflow that turns incoming business requests into structured records, optional API enrichment, Excel/CSV outputs, generated responses, and an auditable processing report.

## Business Problem
Small teams often copy information manually from emails or forms into spreadsheets, decide what each request means, check external systems, and write repetitive replies. This demo shows how that entire flow can be automated while keeping the default AI step on the local computer.

## How It Works

`Incoming text → Local Ollama AI → Validation → Optional REST API → CSV/XLSX → Response → Processing report`

The workflow extracts customer name, company, email, request type, priority, summary, requested action, and confidence. It then creates a validated business record, enriches it when an endpoint is configured, generates a concise response, and exports the result.

## Local AI & Privacy
The default model is `qwen2:1.5b` through a local Ollama server at `http://127.0.0.1:11434`. No paid AI API or secret key is required. The model name and Ollama URL are configurable in code, and the deterministic fallback keeps the workflow operational if Ollama is unavailable.

This architecture is useful for clients who prefer sensitive business text to stay on their own PC or server.

## Quick Start

```powershell
python -m pip install -r requirements.txt
python run_demo.py
```

For local-AI classification, install Ollama and make sure `qwen2:1.5b` (or another configured model) is available. The demo still runs without Ollama by using its fallback parser.

Run the tests with:

```powershell
python -m pytest -q
```

## Example Outputs
A successful run writes:

- `output/requests.csv` — spreadsheet-friendly request log
- `output/requests.xlsx` — Excel workbook with stable headers
- `output/processing_report.txt` — readable processing audit

The included demo processes three scenarios: Excel/CSV cleanup, lead/API automation, and an urgent management-report request.

## Graceful Fallbacks
- Invalid or non-JSON AI output falls back to deterministic parsing.
- Missing customer fields receive explicit defaults instead of crashing.
- Empty email values remain valid export rows.
- REST timeouts and non-200 responses are recorded in `api_status` while processing continues.
- Re-running the demo appends rows without duplicating CSV/Excel headers.

## Extension Path
The business logic is intentionally separated from integrations. A production version can add n8n or Make as a visual workflow layer, Gmail/Outlook intake, CRM webhooks, authenticated REST services, Google Sheets, Slack/Telegram notifications, or a small web dashboard without rewriting the core processor.

## Project Structure

```text
ai_client.py        Local Ollama adapter + fallback parser
api_client.py       Optional REST enrichment
models.py           Validated request structures
processor.py        End-to-end business workflow
exporters.py        CSV and Excel output
logging_utils.py    Processing report
run_demo.py         One-command demo
sample_requests.py  Three portfolio scenarios
tests/              Deterministic offline test suite
```

## Tech Stack
Python 3.12, Ollama, Requests, openpyxl, Pillow, pytest.

## Portfolio Value
This project demonstrates a complete automation outcome rather than a single script: request intake, local AI classification, validation, API integration, spreadsheet delivery, customer-response generation, resilience, and automated tests.