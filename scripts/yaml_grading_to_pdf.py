#!/usr/bin/env python3
"""Convert a grading YAML file to PDF.

Install:
    pip install pyyaml reportlab

Usage:
    python yaml_to_pdf.py grading.yaml
    python yaml_to_pdf.py grading.yaml -o grading.pdf
"""

from __future__ import annotations

import argparse
import html
import sys
from pathlib import Path
from typing import Any

import yaml
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    CondPageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
BRAND_ASSETS = ROOT / "assets" / "brand"
LOGO_PATH = BRAND_ASSETS / "light_logo.png"
BANNER_PATH = ROOT / "assets" / "banner.png"

EGGSHELL = colors.HexColor("#FEFFF7")
DARK_BLUE = colors.HexColor("#0C43A0")
LIGHT_BLUE = colors.HexColor("#68AFE7")
PALE_BLUE = colors.HexColor("#EAF5FC")
INK = colors.HexColor("#151515")
MUTED = colors.HexColor("#667085")
LINE = colors.HexColor("#B9DDF5")

BODY_FONT = "Helvetica"
BODY_FONT_MEDIUM = "Helvetica-Bold"
BODY_FONT_BOLD = "Helvetica-Bold"
TITLE_FONT = "Times-Bold"


def register_brand_fonts() -> None:
    """Use temporary brand fonts when present; fall back to built-in PDF fonts."""
    global BODY_FONT, BODY_FONT_MEDIUM, BODY_FONT_BOLD

    fonts = {
        "Manrope-Regular": BRAND_ASSETS / "Manrope-Regular.ttf",
        "Manrope-Medium": BRAND_ASSETS / "Manrope-Medium.ttf",
        "Manrope-Bold": BRAND_ASSETS / "Manrope-Bold.ttf",
    }
    if not all(path.is_file() for path in fonts.values()):
        return

    try:
        for name, path in fonts.items():
            if name not in pdfmetrics.getRegisteredFontNames():
                pdfmetrics.registerFont(TTFont(name, str(path)))
        BODY_FONT = "Manrope-Regular"
        BODY_FONT_MEDIUM = "Manrope-Medium"
        BODY_FONT_BOLD = "Manrope-Bold"
    except Exception as exc:  # pragma: no cover - cosmetic fallback only
        print(f"Warning: could not load brand fonts: {exc}", file=sys.stderr)


def draw_image_cover(
    canvas, image_path: Path, x: float, y: float, width: float, height: float
) -> None:
    """Draw an image cropped to fill a target rectangle without distortion."""
    image = ImageReader(str(image_path))
    image_width, image_height = image.getSize()
    scale = max(width / image_width, height / image_height)
    draw_width = image_width * scale
    draw_height = image_height * scale
    draw_x = x + (width - draw_width) / 2
    draw_y = y + (height - draw_height) / 2

    canvas.saveState()
    path = canvas.beginPath()
    path.rect(x, y, width, height)
    canvas.clipPath(path, stroke=0, fill=0)
    canvas.drawImage(
        image, draw_x, draw_y, width=draw_width, height=draw_height, mask="auto"
    )
    canvas.restoreState()


def text(value: Any) -> str:
    """Escape YAML text for ReportLab and preserve line breaks."""
    return html.escape("" if value is None else str(value)).replace("\n", "<br/>")


def number(value: Any) -> float | None:
    try:
        return None if value in (None, "") else float(value)
    except (TypeError, ValueError):
        return None


def points(value: Any) -> str:
    value = number(value)
    return "-" if value is None else f"{value:.2f}"


def label_text(key: str) -> str:
    return (
        "AI slop penalty" if key == "ai_slop_penalty" else key.replace("_", " ").title()
    )


def ai_slop_penalty(data: dict[str, Any]) -> float:
    feedback = data.get("general_feedback")
    if not isinstance(feedback, dict):
        return 0.0

    raw = feedback.get("ai_slop_penalty")
    penalty = number(raw)
    if penalty is None:
        if isinstance(raw, bool):
            penalty = 2.0 if raw else 0.0
        elif raw is None or str(raw).strip() in ("", "-", "0"):
            penalty = 0.0
        else:
            penalty = 2.0
    return min(max(penalty, 0.0), 2.0)


def blocks(data: dict[str, Any]):
    grading = data.get("grading", {})
    if isinstance(grading, dict):
        for block in grading.values():
            if isinstance(block, dict):
                yield block


def overall_score(data: dict[str, Any]) -> tuple[float, float, int, int]:
    all_blocks = list(blocks(data))
    possible = sum(number(b.get("max_points")) or 0 for b in all_blocks)
    awarded = 0.0
    graded = total = 0

    for block in all_blocks:
        for criterion in block.get("criteria", []) or []:
            if not isinstance(criterion, dict):
                continue
            for item in criterion.get("items", []) or []:
                if not isinstance(item, dict):
                    continue
                total += 1
                value = number(item.get("awarded_points"))
                if value is not None:
                    awarded += value
                    graded += 1

    # Avoid cosmetic artifacts such as 0.6667 * 3 = 2.0001.
    if graded == total and abs(awarded - possible) < 1e-3:
        awarded = possible
    return awarded, possible, graded, total


def block_score(block: dict[str, Any]) -> tuple[float, float | None, int, int]:
    possible = number(block.get("max_points"))
    awarded = 0.0
    graded = total = 0

    for criterion in block.get("criteria", []) or []:
        if not isinstance(criterion, dict):
            continue
        for item in criterion.get("items", []) or []:
            if not isinstance(item, dict):
                continue
            total += 1
            value = number(item.get("awarded_points"))
            if value is not None:
                awarded += value
                graded += 1

    if possible is not None and graded == total and abs(awarded - possible) < 1e-3:
        awarded = possible
    return awarded, possible, graded, total


def draw_page(canvas, doc) -> None:
    canvas.saveState()

    width, height = A4
    canvas.setFillColor(EGGSHELL)
    canvas.rect(0, 0, width, height, fill=1, stroke=0)

    if BANNER_PATH.is_file():
        draw_image_cover(canvas, BANNER_PATH, 0, height - 28 * mm, width, 28 * mm)
    else:
        canvas.setFillColor(LIGHT_BLUE)
        canvas.rect(0, height - 28 * mm, width, 28 * mm, fill=1, stroke=0)

    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.5)
    canvas.line(doc.leftMargin, 14 * mm, width - doc.rightMargin, 14 * mm)
    canvas.setFont(BODY_FONT, 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(doc.leftMargin, 9 * mm, "LiGHT grading report")
    canvas.drawRightString(width - doc.rightMargin, 9 * mm, f"Page {doc.page}")
    canvas.restoreState()


def convert(source: Path, output: Path) -> None:
    register_brand_fonts()

    try:
        data = yaml.safe_load(source.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ValueError(f"Invalid YAML: {exc}") from exc

    if not isinstance(data, dict) or not isinstance(data.get("grading"), dict):
        raise ValueError("Expected a YAML mapping with a top-level 'grading' mapping.")

    base = getSampleStyleSheet()
    body = ParagraphStyle(
        "body",
        parent=base["BodyText"],
        fontName=BODY_FONT,
        fontSize=9,
        leading=12,
        textColor=INK,
    )
    body_bold = ParagraphStyle("body_bold", parent=body, fontName=BODY_FONT_BOLD)
    body_bold_inverse = ParagraphStyle(
        "body_bold_inverse", parent=body_bold, textColor=EGGSHELL
    )
    small = ParagraphStyle("small", parent=body, fontSize=8.1, leading=10.4)
    small_bold = ParagraphStyle("small_bold", parent=small, fontName=BODY_FONT_BOLD)
    h1 = ParagraphStyle(
        "h1",
        parent=base["Heading1"],
        fontName=TITLE_FONT,
        fontSize=15,
        leading=18,
        textColor=DARK_BLUE,
        spaceBefore=10,
        spaceAfter=6,
    )
    h2 = ParagraphStyle(
        "h2",
        parent=base["Heading2"],
        fontName=BODY_FONT_MEDIUM,
        fontSize=10.5,
        leading=13,
        textColor=DARK_BLUE,
        spaceBefore=5,
        spaceAfter=3,
    )
    course = ParagraphStyle(
        "course",
        parent=body,
        fontName=BODY_FONT_BOLD,
        fontSize=8.5,
        leading=11,
        textColor=DARK_BLUE,
        spaceAfter=2,
    )
    title = ParagraphStyle(
        "title",
        parent=base["Title"],
        fontName=TITLE_FONT,
        fontSize=25,
        leading=29,
        textColor=DARK_BLUE,
        alignment=0,
        spaceAfter=7,
    )
    label = ParagraphStyle(
        "label",
        parent=small_bold,
        fontName=BODY_FONT_BOLD,
        fontSize=7.4,
        leading=9,
        textColor=DARK_BLUE,
    )
    label_inverse = ParagraphStyle("label_inverse", parent=label, textColor=EGGSHELL)
    note = ParagraphStyle(
        "note",
        parent=small,
        backColor=PALE_BLUE,
        borderColor=LIGHT_BLUE,
        borderWidth=0.5,
        borderPadding=6,
        leftIndent=4,
        rightIndent=4,
        spaceAfter=6,
    )

    doc = SimpleDocTemplate(
        str(output),
        pagesize=A4,
        leftMargin=16 * mm,
        rightMargin=16 * mm,
        topMargin=34 * mm,
        bottomMargin=20 * mm,
        title="Grading report",
    )
    story = []

    project = data.get("project") if isinstance(data.get("project"), dict) else {}
    story.append(Paragraph(text(project.get("milestone") or "Grading report"), title))
    story.append(Paragraph("BiGHT course", course))
    story.append(Paragraph("Evaluation summary and detailed rubric feedback", body))
    story.append(Spacer(1, 4 * mm))

    meta = []
    for key, value in project.items():
        if key not in ("milestone", "grading_date"):
            meta.append(
                [
                    Paragraph(text(key.replace("_", " ").title()).upper(), label),
                    Paragraph(text(value) if value not in (None, "") else "-", body),
                ]
            )
    if meta:
        t = Table(meta, colWidths=[42 * mm, 126 * mm])
        t.setStyle(
            TableStyle(
                [
                    ("GRID", (0, 0), (-1, -1), 0.35, LINE),
                    ("BACKGROUND", (0, 0), (0, -1), PALE_BLUE),
                    ("BACKGROUND", (1, 0), (1, -1), colors.white),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("PADDING", (0, 0), (-1, -1), 5),
                ]
            )
        )
        story += [t, Spacer(1, 5 * mm)]

    awarded, possible, graded, total = overall_score(data)
    penalty = ai_slop_penalty(data)
    awarded_after_penalty = max(0.0, awarded - penalty)
    score = (
        f"Not graded / {points(possible)}"
        if graded == 0
        else f"{points(awarded)} / {points(possible)}"
    )
    if graded > 0 and penalty:
        score = f"{points(awarded_after_penalty)} / {points(possible)} (AI slop penalty: -{points(penalty)})"
    if graded < total:
        score += f" (partial: {graded}/{total} items graded)"
    score_card = Table(
        [
            [
                Paragraph("SCORE SUMMARY", label_inverse),
                Paragraph(text(score), body_bold),
            ]
        ],
        colWidths=[42 * mm, 126 * mm],
    )
    score_card.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, 0), DARK_BLUE),
                ("BACKGROUND", (1, 0), (1, 0), PALE_BLUE),
                ("TEXTCOLOR", (0, 0), (0, 0), EGGSHELL),
                ("BOX", (0, 0), (-1, -1), 0.6, DARK_BLUE),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("PADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    story += [score_card, Spacer(1, 4 * mm)]

    feedback = data.get("general_feedback")
    if isinstance(feedback, dict):
        story.append(Paragraph("General feedback", h1))
        for key, value in feedback.items():
            if key == "ai_slop_penalty":
                continue
            story.append(Paragraph(f"<b>{text(label_text(key))}</b>", h2))
            story.append(
                Paragraph(text(value) if value not in (None, "") else "-", body)
            )

    for block in blocks(data):
        b_awarded, b_possible, b_graded, b_total = block_score(block)
        b_score = (
            f"Not graded / {points(b_possible)}"
            if b_graded == 0
            else f"{points(b_awarded)} / {points(b_possible)}"
        )
        if 0 < b_graded < b_total:
            b_score += " partial"
        story.append(
            Paragraph(
                f"{text(block.get('title', 'Grading block'))} ({text(b_score)} points)",
                h1,
            )
        )

        for criterion in block.get("criteria", []) or []:
            if not isinstance(criterion, dict):
                continue

            # Keep enough free space so a criterion title is not orphaned.
            story.append(CondPageBreak(45 * mm))

            items = [x for x in (criterion.get("items") or []) if isinstance(x, dict)]
            awarded_values = [number(x.get("awarded_points")) for x in items]
            c_graded = sum(x is not None for x in awarded_values)
            c_awarded = sum(x for x in awarded_values if x is not None)
            c_max = number(criterion.get("max_points"))
            if (
                c_max is not None
                and c_graded == len(items)
                and abs(c_awarded - c_max) < 1e-3
            ):
                c_awarded = c_max

            c_score = (
                f"Not graded / {points(c_max)}"
                if c_graded == 0
                else f"{points(c_awarded)} / {points(c_max)}"
            )
            if 0 < c_graded < len(items):
                c_score += " (partial)"

            heading = f"{text(criterion.get('id', ''))} - {text(criterion.get('title', 'Criterion'))}"
            header = Table(
                [
                    [
                        Paragraph(heading, body_bold_inverse),
                        Paragraph(text(c_score), body_bold_inverse),
                    ]
                ],
                colWidths=[127 * mm, 41 * mm],
            )
            header.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, -1), DARK_BLUE),
                        ("TEXTCOLOR", (0, 0), (-1, -1), EGGSHELL),
                        ("BOX", (0, 0), (-1, -1), 0.5, DARK_BLUE),
                        ("ALIGN", (1, 0), (1, 0), "RIGHT"),
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("PADDING", (0, 0), (-1, -1), 5),
                    ]
                )
            )
            story.append(header)

            if criterion.get("grading_note"):
                story.append(
                    Paragraph(f"<b>Note:</b> {text(criterion['grading_note'])}", note)
                )

            rows = [
                [
                    Paragraph("ITEM", small_bold),
                    Paragraph("MAX", small_bold),
                    Paragraph("AWARDED", small_bold),
                    Paragraph("COMMENT", small_bold),
                ]
            ]
            for item in items:
                item_name = text(item.get("item", ""))
                expected = item.get("expected_content")
                if isinstance(expected, list) and expected:
                    item_name += "<br/><b>Expected:</b><br/>" + "<br/>".join(
                        f"- {text(x)}" for x in expected
                    )

                awarded_value = item.get("awarded_points")
                if (
                    number(awarded_value) is not None
                    and number(item.get("max_points")) is not None
                ):
                    if number(awarded_value) > number(item.get("max_points")):
                        print(
                            f"Warning: awarded points exceed max for {item.get('item', 'item')}",
                            file=sys.stderr,
                        )

                rows.append(
                    [
                        Paragraph(item_name, small),
                        Paragraph(points(item.get("max_points")), small),
                        Paragraph(
                            "Not graded"
                            if awarded_value is None
                            else points(awarded_value),
                            small_bold
                            if number(awarded_value) == number(item.get("max_points"))
                            else small,
                        ),
                        Paragraph(text(item.get("comment") or "-"), small),
                    ]
                )

            table = Table(
                rows,
                colWidths=[72 * mm, 16 * mm, 24 * mm, 56 * mm],
                repeatRows=1,
                splitByRow=1,
                splitInRow=1,
            )
            table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), LIGHT_BLUE),
                        ("TEXTCOLOR", (0, 0), (-1, 0), DARK_BLUE),
                        ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                        ("GRID", (0, 0), (-1, -1), 0.35, LINE),
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("ALIGN", (1, 1), (2, -1), "CENTER"),
                        ("PADDING", (0, 0), (-1, -1), 5),
                    ]
                )
            )
            story.append(table)

            if criterion.get("criterion_comment"):
                story.append(
                    Paragraph(
                        f"<b>Criterion comment:</b> {text(criterion['criterion_comment'])}",
                        body,
                    )
                )
            story.append(Spacer(1, 3 * mm))

    doc.build(story, onFirstPage=draw_page, onLaterPages=draw_page)


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert grading YAML to PDF")
    parser.add_argument("input", type=Path)
    parser.add_argument("-o", "--output", type=Path)
    args = parser.parse_args()

    if not args.input.is_file():
        parser.error(f"Input file not found: {args.input}")
    output = args.output or args.input.with_suffix(".pdf")
    output.parent.mkdir(parents=True, exist_ok=True)

    try:
        convert(args.input, output)
    except (OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"Created: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
