from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
COVER = ROOT / "portfolio_cover_1600x1200.png"


def font(size: int, bold: bool = False):
    candidates = [
        Path(r"C:\Windows\Fonts\segoeuib.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf"),
        Path(r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf"),
    ]
    for path in candidates:
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def main() -> None:
    img = Image.new("RGB", (1600, 1200), "#0b1426")
    draw = ImageDraw.Draw(img)
    white = "#f4f7fb"
    muted = "#a8b4c8"
    cyan = "#39c6ff"
    green = "#55e39b"
    panel = "#152239"
    line = "#2c4162"

    draw.text((70, 60), "AI Business Automation", font=font(66, True), fill=white)
    draw.text((72, 150), "Local AI • REST API • Excel/CSV", font=font(32), fill=muted)

    steps = ["REQUEST", "LOCAL AI", "VALIDATE", "REST API", "EXCEL/CSV", "RESPONSE"]
    x, y, width, height = 70, 275, 210, 150
    for index, label in enumerate(steps):
        accent = cyan if index < 3 else green
        draw.rounded_rectangle((x, y, x + width, y + height), radius=22, fill=panel, outline=accent, width=3)
        bbox = draw.textbbox((0, 0), label, font=font(24, True))
        tx = x + (width - (bbox[2] - bbox[0])) / 2
        draw.text((tx, y + 52), label, font=font(24, True), fill=white)
        if index < len(steps) - 1:
            draw.line((x + width + 12, y + height // 2, x + width + 50, y + height // 2), fill=muted, width=5)
            draw.polygon([
                (x + width + 50, y + height // 2),
                (x + width + 34, y + height // 2 - 10),
                (x + width + 34, y + height // 2 + 10),
            ], fill=muted)
        x += 245

    draw.rounded_rectangle((70, 500, 1530, 915), radius=28, fill=panel, outline=line, width=3)
    draw.text((110, 545), "Portfolio-ready workflow", font=font(38, True), fill=white)

    metrics = [
        ("LOCAL", "AI by default"),
        ("3", "business scenarios"),
        ("CSV + XLSX", "structured outputs"),
        ("21", "tests passing"),
    ]
    x = 110
    for value, label in metrics:
        value_font = font(46 if len(value) < 7 else 36, True)
        draw.text((x, 655), value, font=value_font, fill=cyan if value != "CSV + XLSX" else green)
        draw.text((x, 730), label, font=font(25), fill=muted)
        x += 355

    draw.text((110, 825), "No paid AI API required • graceful fallback • auditable processing", font=font(28, True), fill=white)
    draw.text((80, 1020), "Python  •  Ollama  •  Requests  •  openpyxl  •  pytest", font=font(29), fill=white)
    draw.text((80, 1075), "Built as a reusable foundation for n8n, CRM, email and webhook integrations", font=font(25), fill=muted)

    img.save(COVER)
    print(COVER)


if __name__ == "__main__":
    main()
