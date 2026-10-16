from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


def test_readme_has_required_sections():
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    for heading in [
        "# AI Business Automation",
        "## Business Problem",
        "## How It Works",
        "## Local AI & Privacy",
        "## Quick Start",
        "## Example Outputs",
        "## Graceful Fallbacks",
        "## Extension Path",
    ]:
        assert heading in text


def test_cover_is_exact_portfolio_size():
    with Image.open(ROOT / "portfolio_cover_1600x1200.png") as image:
        assert image.size == (1600, 1200)
