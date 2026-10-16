from pathlib import Path

import processor
from exporters import append_csv, append_excel
from sample_requests import SAMPLE_REQUESTS


def main() -> int:
    output_dir = Path("output")
    items = [processor.process_request(text) for text in SAMPLE_REQUESTS]
    append_csv(items, output_dir / "requests.csv")
    append_excel(items, output_dir / "requests.xlsx")
    processor.write_processing_report(items, output_dir / "processing_report.txt")

    print("AI Business Automation Demo")
    print("=" * 27)
    for item in items:
        print(f"{item.request_type:12} | {item.priority:6} | {item.customer_name} | {item.api_status}")
    print(f"Processed: {len(items)}")
    print(f"Outputs: {output_dir.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
