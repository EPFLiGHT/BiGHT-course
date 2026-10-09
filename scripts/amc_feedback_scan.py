#!/usr/bin/env python3
"""Analyse a scanned batch of the anonymous BiGHT feedback form.

1. Rebuild the AMC layout from the exact LaTeX used for printing and check it
   is pixel-identical to the printed PDF (same question order on every copy).
2. Let AMC read the ticked boxes of the closed questions.
3. Crop the handwritten open answers into ``report/crops/`` and list them in
   ``report/transcriptions.csv``. No OCR runs here: the Claude session running this
   task reads each crop, fills in that sheet (rules in
   ``report/transcription_instructions.md``), then re-runs with ``--report-only``.
4. Write CSVs, bar charts and a Markdown summary.

Nothing uncertain is guessed: ambiguous ticks and uncertain / illegible
transcriptions are listed in ``report/manual_review.csv`` (crops copied to
``manual_review/``).
Human corrections go in ``report/manual_corrections.csv`` (columns
``form_id,question_id,value``: reviewed text for open answers, the true choice
label for closed ones); re-run with ``--report-only`` to apply them.

Example:
    python scripts/amc_feedback_scan.py --scans scan.pdf --force
"""

from __future__ import annotations

import argparse
import csv
import re
import shutil
import sqlite3
import statistics
import subprocess
from pathlib import Path

import cv2
import numpy as np
import pymupdf
from amc_grade_scan import (
    compile_subject,
    load_layout,
    make_scan_list,
    require_command,
    run_command,
    split_scans,
)
from PIL import Image, ImageDraw, ImageFont

BUILD_DIR = Path("quiz-drafts/feedback-form-build")
LAYOUT_DPI = 300
PT_TO_PX = LAYOUT_DPI / 72
BOTTOM_MARGIN_PT = 62  # stop above the bottom corner marks / page code
OPEN_X_PT = (
    60,
    590,
)  # text width plus the margins: students write past the dotted lines
AMBIGUOUS_DARKNESS = (
    0.03,
    0.10,
)  # tuned on the 2026-10 scan: empty boxes <= 0.014, lightest real tick 0.099
NEAR_CANCEL = 0.05  # darkness this close to --threshold-up is ambiguous: heavy tick or blacked out?
OCR_STATUS = {
    "clear": "ok",
    "empty": "empty",
    "partly_uncertain": "uncertain",
    "mostly_illegible": "illegible",
}
TRANSCRIPTION_RULES = """# Transcribing the open answers

Open each image listed in `transcriptions.csv` (column `crop_path`, relative to this folder) and fill in
`text` and `legibility` for that row. Then re-run `amc_feedback_scan.py --report-only` to merge.

- Verbatim: keep the student's language (English or French), spelling, abbreviations and line breaks
  (write a line break as " / "). Do not correct, translate or summarise.
- Ignore the printed dotted writing lines and any printed question text at the edges of the crop.
- Write [illegible] for a word you cannot read and [word?] for a word you are unsure of. Never guess to fill a gap.
- legibility is one of: `clear`, `partly_uncertain`, `mostly_illegible`, `empty` (nothing handwritten; leave text blank).
- `partly_uncertain` and `mostly_illegible` answers are listed for manual review.
"""
SCALE_QUESTIONS = {"overall", "lecturesuseful", "motivation", "workload", "quizformat"}
MOTIVATION_GROUPS = [
    ("low motivation (1-3)", 1, 3),
    ("balanced (4-6)", 4, 6),
    ("anxiety-dominated (7-10)", 7, 10),
]


# --- questionnaire -----------------------------------------------------------------------------------------


def parse_questions(txt_path: Path) -> list[dict]:
    """Read question ids, texts and choice labels from the AMC-TXT source, in printed order."""
    questions: list[dict] = []
    for line in txt_path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^\*(<[^>]*>)?\[[^\]]*id=(\w+)\]\s*(.*)", line)
        if match:
            questions.append(
                {
                    "id": match.group(2),
                    "text": match.group(3).strip(),
                    "open": bool(match.group(1)),
                    "choices": [],
                }
            )
        elif questions and line.startswith("+ ") and not questions[-1]["open"]:
            questions[-1]["choices"].append(line[2:].strip())
    return questions


# --- AMC project -------------------------------------------------------------------------------------------


def prepare_project(project: Path, tex: Path) -> None:
    for sub in ["data", "cr", "scans"]:
        (project / sub).mkdir(parents=True, exist_ok=True)
    shutil.copy2(tex, project / "DOC-source.tex")
    compile_subject(project, project / "DOC-source.tex")
    load_layout(project)


def render_gray(pdf: Path, dpi: int, out_prefix: Path) -> list[np.ndarray]:
    run_command(
        ["pdftoppm", "-r", str(dpi), "-gray", str(pdf), str(out_prefix)],
        cwd=out_prefix.parent,
    )
    pages = sorted(out_prefix.parent.glob(out_prefix.name + "-*.pgm"))
    images = [np.asarray(Image.open(page), dtype=np.int16) for page in pages]
    for page in pages:
        page.unlink()
    return images


def verify_layout(
    project: Path, questions: list[dict], printed_pdf: Path
) -> tuple[int, int, list[str]]:
    """Check layout vs. questionnaire and printed PDF. Returns (#copies, pages per copy, notes)."""
    db = sqlite3.connect(project / "data" / "layout.sqlite")
    names = [
        name
        for (name,) in db.execute("SELECT name FROM layout_question ORDER BY question")
    ]
    expected = [q["id"] for q in questions]
    if names != expected:
        raise RuntimeError(f"Layout question order {names} != AMC-TXT order {expected}")

    copies = [
        s
        for (s,) in db.execute(
            "SELECT DISTINCT student FROM layout_page ORDER BY student"
        )
    ]
    pages_per_copy = db.execute("SELECT MAX(page) FROM layout_page").fetchone()[0]
    reference = None
    for student in copies:
        boxes = db.execute(
            "SELECT b.page, q.name, b.answer, ROUND(b.xmin), ROUND(b.ymin) FROM layout_box b "
            "JOIN layout_question q ON q.question = b.question WHERE b.student = ? ORDER BY b.page, b.ymin, b.xmin",
            (student,),
        ).fetchall()
        if reference is None:
            reference = boxes
        elif boxes != reference:
            raise RuntimeError(
                f"Copy {student} does not have the same layout as copy {copies[0]}"
            )
    amc_ids = {box[1] for box in reference}
    plain = plain_boxes(
        project,
        questions,
        {q["id"] for q in questions if q["choices"] and q["id"] not in amc_ids},
        pages_per_copy,
    )
    for q in questions:
        count = sum(1 for box in reference if box[1] == q["id"]) or len(
            plain.get(q["id"], [])
        )
        if count != len(q["choices"]):
            raise RuntimeError(
                f"Question {q['id']}: {count} boxes in layout, {len(q['choices'])} choices in AMC-TXT"
            )

    notes = [
        f"Layout: {len(copies)} copies x {pages_per_copy} pages, identical box layout and question order on every copy."
    ]
    if plain:
        notes.append(
            f"Printed as plain boxes AMC cannot see, so read by this script with AMC's page registration: {', '.join(plain)}."
        )
    compiled = render_gray(project / "amc-compiled.pdf", 40, project / "cmp-a")
    printed = render_gray(printed_pdf, 40, project / "cmp-b")
    if len(compiled) != len(printed) or any(
        a.shape != b.shape or (abs(a - b) > 40).any() for a, b in zip(compiled, printed)
    ):
        raise RuntimeError(
            f"Rebuilt layout differs from printed PDF {printed_pdf}; scans would be misread."
        )
    notes.append(
        f"Rebuilt layout is pixel-identical to {printed_pdf} ({len(printed)} pages)."
    )

    printed_text = subprocess.run(
        ["pdftotext", "-f", "1", "-l", str(pages_per_copy), str(printed_pdf), "-"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    squashed = re.sub(r"\s+", " ", printed_text)
    missing = [
        label for q in questions for label in q["choices"] if label not in squashed
    ]
    if missing:
        raise RuntimeError(f"Choice labels not found on printed form: {missing}")
    notes.append(
        "All closed-question choice labels from the AMC-TXT source appear on the printed form."
    )
    return len(copies), pages_per_copy, notes, plain


def page_lines(doc, page_index: int) -> list[tuple[tuple, str]]:
    return [
        (line["bbox"], "".join(span["text"] for span in line["spans"]).strip())
        for block in doc[page_index].get_text("dict")["blocks"]
        for line in block.get("lines", [])
    ]


def question_span(doc, number: int, pages_per_copy: int) -> tuple[int, float, float]:
    """(page index, y of the 'Question N' header, y of the next header or page bottom) in pt, on copy 1."""
    for page_index in range(pages_per_copy):
        heads = {
            int(m.group(1)): bbox[1]
            for bbox, text in page_lines(doc, page_index)
            if (m := re.fullmatch(r"Question (\d+)", text))
        }
        if number in heads:
            below = [y for y in heads.values() if y > heads[number]]
            return (
                page_index,
                heads[number],
                min(below, default=doc[page_index].rect.height),
            )
    raise RuntimeError(f"'Question {number}' not found in the layout PDF")


def open_regions(
    project: Path, questions: list[dict], pages_per_copy: int
) -> dict[str, tuple[int, float, float, float, float]]:
    """Writing area of each open question on copy 1, in layout px: page, x0, y0, x1, y1."""
    doc = pymupdf.open(project / "amc-compiled.pdf")
    regions = {}
    for number, q in enumerate(questions, start=1):
        if not q["open"]:
            continue
        page_index, top, bottom = question_span(doc, number, pages_per_copy)
        lines = [
            (bbox, text)
            for bbox, text in page_lines(doc, page_index)
            if top <= bbox[1] < bottom
        ]
        dots = [bbox for bbox, text in lines if text.startswith(". . .")]
        if not dots:
            raise RuntimeError(
                f"No writing lines found for open question {number} ({q['id']})"
            )
        text_bottom = max(
            bbox[3]
            for bbox, text in lines
            if not text.startswith(". . .") and bbox[1] < dots[0][1]
        )
        # Students keep writing past the last dotted line: extend down to the next printed text, or the bottom margin.
        below = [
            bbox[1]
            for bbox, _ in page_lines(doc, page_index)
            if bbox[1] > dots[-1][3] and bbox[0] > OPEN_X_PT[0]
        ]
        bottom = min(below, default=doc[page_index].rect.height - BOTTOM_MARGIN_PT) - 1
        x0, x1 = OPEN_X_PT
        regions[q["id"]] = (
            page_index + 1,
            x0 * PT_TO_PX,
            (text_bottom + 1) * PT_TO_PX,
            x1 * PT_TO_PX,
            bottom * PT_TO_PX,
        )
    return regions


def plain_boxes(
    project: Path, questions: list[dict], ids: set[str], pages_per_copy: int
) -> dict[str, list[tuple]]:
    """Boxes printed as plain \\fbox (invisible to AMC), in layout px, in choice order: (page, x0, y0, x1, y1)."""
    doc = pymupdf.open(project / "amc-compiled.pdf")
    found = {}
    for number, q in enumerate(questions, start=1):
        if q["id"] not in ids:
            continue
        page_index, top, bottom = question_span(doc, number, pages_per_copy)
        sides = sorted(
            (round(path["rect"].y0), path["rect"].x0, path["rect"].y1)
            for path in doc[page_index].get_drawings()
            if path["rect"].width < 0.5
            and path["rect"].height > 5
            and top <= path["rect"].y0 < bottom
        )
        if len(sides) % 2:
            raise RuntimeError(f"Unpaired box sides for {q['id']}")
        found[q["id"]] = [
            (
                page_index + 1,
                left[1] * PT_TO_PX,
                left[0] * PT_TO_PX,
                right[1] * PT_TO_PX,
                left[2] * PT_TO_PX,
            )
            for left, right in zip(sides[::2], sides[1::2])
        ]
    return found


def analyse(project: Path, scans: list[Path], args: argparse.Namespace) -> None:
    scan_list = make_scan_list(scans, project)
    split_scans(project, scan_list, args.vector_density)
    command = [
        "auto-multiple-choice",
        "analyse",
        "--projet",
        str(project),
        "--liste-fichiers",
        str(scan_list),
        "--tol-marque",
        args.tol_marque,
    ]
    run_command(command, cwd=project)


# --- reading AMC results -----------------------------------------------------------------------------------


def form_id(student: int, copy: int) -> str:
    return f"{student:02d}" if not copy else f"{student:02d}-{copy}"


def scan_image(project: Path, src: str) -> np.ndarray:
    return cv2.imread(src.replace("%PROJET", str(project)), cv2.IMREAD_GRAYSCALE)


def to_scan(
    transform, x0: float, y0: float, x1: float, y1: float, image: np.ndarray
) -> np.ndarray:
    """Deskewed crop of a layout-px rectangle, via AMC's page transform x' = a x + b y + e, y' = c x + d y + f."""
    a, b, c, d, e, f = transform
    matrix = np.array([[a, b, a * x0 + b * y0 + e], [c, d, c * x0 + d * y0 + f]])
    size = (round(x1 - x0), round(y1 - y0))
    return cv2.warpAffine(
        image,
        matrix,
        size,
        flags=cv2.INTER_LINEAR | cv2.WARP_INVERSE_MAP,
        borderValue=255,
    )


def measure_plain_boxes(
    project: Path, pages: list, plain: dict, crops_dir: Path
) -> list[tuple]:
    """Same tuples as AMC's capture_zone rows, for the plain boxes: darkness of the central 60% of each box.

    Also saves a crop of all the question's boxes per form for visual checks.
    """
    rows = []
    for student, copy, page, src, *transform, _ in pages:
        for qid, boxes in plain.items():
            boxes = [box for box in boxes if box[0] == page]
            if not boxes:
                continue
            image = scan_image(project, src)
            for answer, (_, x0, y0, x1, y1) in enumerate(boxes, start=1):
                inset_x, inset_y = 0.2 * (x1 - x0), 0.2 * (y1 - y0)
                zone = to_scan(
                    transform,
                    x0 + inset_x,
                    y0 + inset_y,
                    x1 - inset_x,
                    y1 - inset_y,
                    image,
                )
                rows.append(
                    (
                        student,
                        copy,
                        page,
                        qid,
                        answer,
                        zone.size,
                        int((zone < 128).sum()),
                        -1,
                        "script",
                    )
                )
            margin = 60
            area = to_scan(
                transform,
                boxes[0][1] - margin,
                boxes[0][2] - margin,
                boxes[-1][3] + 2 * margin,
                boxes[-1][4] + margin,
                image,
            )
            cv2.imwrite(
                str(crops_dir / f"form{form_id(student, copy)}_{qid}.png"), area
            )
    return rows


def read_capture(
    project: Path,
    questions: list[dict],
    plain: dict,
    crops_dir: Path,
    args: argparse.Namespace,
):
    db = sqlite3.connect(project / "data" / "capture.sqlite")
    pages = db.execute(
        "SELECT student, copy, page, src, a, b, c, d, e, f, mse FROM capture_page ORDER BY student, copy, page"
    ).fetchall()
    failed = [name for (name,) in db.execute("SELECT filename FROM capture_failed")]
    names = dict(
        sqlite3.connect(project / "data" / "layout.sqlite").execute(
            "SELECT question, name FROM layout_question"
        )
    )
    zones = [
        (s, c, p, names[q], a, total, black, manual, "amc")
        for s, c, p, q, a, total, black, manual in db.execute(
            "SELECT student, copy, page, id_a, id_b, total, black, manual FROM capture_zone WHERE type = 4"
        )
    ]
    by_id = {q["id"]: q for q in questions}
    zones += measure_plain_boxes(project, pages, plain, crops_dir)

    raw_rows = []
    for student, copy, page, qid, answer, total, black, manual, reader in zones:
        q = by_id[qid]
        darkness = black / total if total > 0 else 0.0
        ticked = (
            manual == 1
            if manual >= 0
            else args.threshold <= darkness <= args.threshold_up
        )
        raw_rows.append(
            {
                "form_id": form_id(student, copy),
                "page": page,
                "question_id": q["id"],
                "answer_number": answer,
                "answer_label": q["choices"][answer - 1],
                "pixels_total": total,
                "pixels_black": black,
                "darkness": round(darkness, 4),
                "manual": manual,
                "ticked": int(ticked),
                "reader": reader,
            }
        )
    order = {q["id"]: i for i, q in enumerate(questions)}
    raw_rows.sort(
        key=lambda r: (r["form_id"], order[r["question_id"]], r["answer_number"])
    )
    return pages, failed, raw_rows


def closed_answers(
    raw_rows: list[dict],
    forms: list[str],
    closed: list[dict],
    corrections: dict,
    report: Path,
    review: list[dict],
    threshold_up: float,
) -> list[dict]:
    rows = []
    for fid in forms:
        row: dict = {"form_id": fid}
        flags = []
        for q in closed:
            if (fid, q["id"]) in corrections:
                value = corrections[(fid, q["id"])]
                if value not in q["choices"]:
                    raise ValueError(
                        f"manual_corrections.csv: {value!r} is not a choice of {q['id']} ({q['choices']})"
                    )
                row[q["id"]] = value
                flags.append(f"{q['id']}=manually_corrected")
                continue
            boxes = [
                r
                for r in raw_rows
                if r["form_id"] == fid and r["question_id"] == q["id"]
            ]
            ticked = [r["answer_label"] for r in boxes if r["ticked"]]
            if not boxes:
                status = "page_missing"
            elif len(ticked) == 1:
                status = "ok"
            elif not ticked:
                status = "blank"
            else:
                status = "multiple:" + "|".join(ticked)
            ambiguous = [
                r["answer_label"]
                for r in boxes
                if r["manual"] < 0
                and (
                    AMBIGUOUS_DARKNESS[0] <= r["darkness"] <= AMBIGUOUS_DARKNESS[1]
                    or abs(r["darkness"] - threshold_up) <= NEAR_CANCEL
                )
            ]
            if ambiguous:
                status += ";ambiguous_darkness:" + "|".join(ambiguous)
            row[q["id"]] = ticked[0] if len(ticked) == 1 and status == "ok" else ""
            if status != "ok":
                flags.append(f"{q['id']}={status}")
                if status not in (
                    "blank",
                    "page_missing",
                ):  # a missing page is reported once per page
                    crop = report / "crops" / f"form{fid}_{q['id']}.png"
                    if crop.exists():
                        shutil.copy2(crop, report / "manual_review" / crop.name)
                    crop_path = (
                        f"manual_review/{crop.name}"
                        if crop.exists()
                        else "check in AMC GUI (data capture)"
                    )
                    review.append(
                        {
                            "form_id": fid,
                            "question_id": q["id"],
                            "kind": "closed",
                            "issue": status,
                            "crop_path": crop_path,
                        }
                    )
        row["flags"] = "; ".join(flags)
        rows.append(row)
    return rows


# --- open answers ------------------------------------------------------------------------------------------


def open_answers(
    project, report, pages, forms, regions, questions, review
) -> list[dict]:
    """Crop every open answer; take its text from transcriptions.csv (filled by Claude reading the crops)."""
    page_info = {
        (form_id(s, c), p): (src, a, b, cc, d, e, f)
        for s, c, p, src, a, b, cc, d, e, f, _ in pages
    }
    done = read_transcriptions(report)
    rows = []
    for fid in forms:
        for q in (q for q in questions if q["open"]):
            page, x0, y0, x1, y1 = regions[q["id"]]
            row = {
                "form_id": fid,
                "question_id": q["id"],
                "question_text": q["text"],
                "ocr_text": "",
                "confidence_or_status": "",
                "crop_path": "",
            }
            rows.append(row)
            if (fid, page) not in page_info:
                row["confidence_or_status"] = "page_missing"
                continue
            src, a, b, c, d, e, f = page_info[(fid, page)]
            crop_path = report / "crops" / f"form{fid}_{q['id']}.png"
            cv2.imwrite(
                str(crop_path),
                to_scan((a, b, c, d, e, f), x0, y0, x1, y1, scan_image(project, src)),
            )
            row["crop_path"] = str(crop_path.relative_to(report))
            text, legibility = done.get((fid, q["id"]), ("", ""))
            row["ocr_text"] = text
            row["confidence_or_status"] = OCR_STATUS.get(
                legibility, "pending_transcription"
            )
            if row["confidence_or_status"] in ("uncertain", "illegible"):
                shutil.copy2(crop_path, report / "manual_review" / crop_path.name)
                review.append(
                    {
                        "form_id": fid,
                        "question_id": q["id"],
                        "kind": "open",
                        "issue": row["confidence_or_status"],
                        "crop_path": f"manual_review/{crop_path.name}",
                    }
                )
    write_transcriptions(report, rows, done)
    return rows


def read_transcriptions(report: Path) -> dict[tuple[str, str], tuple[str, str]]:
    path = report / "transcriptions.csv"
    if not path.exists():
        return {}
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    bad = [
        r
        for r in rows
        if r["legibility"].strip() and r["legibility"].strip() not in OCR_STATUS
    ]
    if bad:
        raise ValueError(
            f"transcriptions.csv: legibility must be one of {sorted(OCR_STATUS)}; got {bad[0]['legibility']!r}"
        )
    return {
        (r["form_id"].zfill(2), r["question_id"]): (
            r["text"].strip(),
            r["legibility"].strip(),
        )
        for r in rows
        if r["legibility"].strip()
    }


def write_transcriptions(report: Path, rows: list[dict], done: dict) -> None:
    """(Re)write the transcription sheet: one line per crop, keeping what was already filled in."""
    sheet = [
        {
            "form_id": r["form_id"],
            "question_id": r["question_id"],
            "crop_path": r["crop_path"],
            "text": done.get(key, ("", ""))[0],
            "legibility": done.get(key, ("", ""))[1],
        }
        for r in rows
        if r["crop_path"] and (key := (r["form_id"], r["question_id"]))
    ]
    write_csv(
        report / "transcriptions.csv",
        sheet,
        ["form_id", "question_id", "crop_path", "text", "legibility"],
    )
    (report / "transcription_instructions.md").write_text(
        TRANSCRIPTION_RULES, encoding="utf-8"
    )


def load_corrections(report: Path) -> dict[tuple[str, str], str]:
    """Human corrections: reviewed text for open answers, or the true choice label for closed ones."""
    path = report / "manual_corrections.csv"
    if not path.exists():
        with path.open("w", newline="", encoding="utf-8") as handle:
            csv.writer(handle).writerow(["form_id", "question_id", "value"])
        return {}
    with path.open(newline="", encoding="utf-8") as handle:
        return {
            (r["form_id"].zfill(2), r["question_id"]): r["value"].strip()
            for r in csv.DictReader(handle)
            if r.get("value", "").strip()
        }


# --- outputs -----------------------------------------------------------------------------------------------


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def font(size: int, bold: bool = False):
    try:
        return ImageFont.truetype(
            "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf", size
        )
    except OSError:
        return ImageFont.load_default(size=size)


def bar_chart(path: Path, title: str, labels: list[str], counts: list[int]) -> None:
    """Horizontal single-series bars with direct 'count (pct)' labels."""
    surface, ink, muted, bar = "#fcfcfb", "#0b0b0b", "#52514e", "#2a78d6"
    total = sum(counts) or 1
    label_font, title_font = font(22), font(24, bold=True)
    label_w = max(int(label_font.getlength(label)) for label in labels) + 30
    bar_area, row_h, top = 700, 54, 90
    width, height = label_w + bar_area + 190, top + row_h * len(labels) + 30
    image = Image.new("RGB", (width, height), surface)
    draw = ImageDraw.Draw(image)
    draw.text((20, 20), title, font=title_font, fill=ink)
    draw.text((20, 54), f"n = {sum(counts)} answered", font=font(18), fill=muted)
    peak = max(counts) or 1
    for i, (label, count) in enumerate(zip(labels, counts)):
        y = top + i * row_h
        draw.text(
            (label_w - 15, y + row_h / 2), label, font=label_font, fill=ink, anchor="rm"
        )
        length = bar_area * count / peak
        if count:
            draw.rounded_rectangle(
                (label_w, y + 10, label_w + max(length, 8), y + row_h - 10),
                radius=4,
                fill=bar,
            )
        draw.text(
            (label_w + length + 12, y + row_h / 2),
            f"{count} ({100 * count / total:.0f}%)",
            font=label_font,
            fill=muted,
            anchor="lm",
        )
    draw.line((label_w, top, label_w, height - 30), fill="#c3c2b7", width=2)
    image.save(path)


def stats_line(values: list[int]) -> str:
    if not values:
        return "no valid answers"
    sd = f"{statistics.stdev(values):.2f}" if len(values) > 1 else "n/a"
    return f"n = {len(values)}, mean = {statistics.mean(values):.2f}, median = {statistics.median(values):g}, SD = {sd}"


def write_summary(
    report, questions, closed_rows, open_rows, review, notes, pages_info
) -> None:
    out = ["# BiGHT detailed feedback form: scan analysis", "", "## Processing", ""]
    out += [f"- {note}" for note in notes + pages_info]
    out += ["", "## Closed questions", ""]
    for q in (q for q in questions if not q["open"]):
        answers = [r[q["id"]] for r in closed_rows if r[q["id"]]]
        counts = [answers.count(label) for label in q["choices"]]
        bar_chart(report / "charts" / f"{q['id']}.png", q["id"], q["choices"], counts)
        not_valid = len(closed_rows) - len(answers)
        out += [
            f"### `{q['id']}`: {q['text']}",
            "",
            f"![{q['id']}](charts/{q['id']}.png)",
            "",
        ]
        if q["id"] in SCALE_QUESTIONS:
            out += [f"**Stats:** {stats_line([int(a) for a in answers])}", ""]
        out += ["| Answer | Count | % of valid |", "|---|---:|---:|"]
        out += [
            f"| {label} | {count} | {100 * count / (len(answers) or 1):.0f}% |"
            for label, count in zip(q["choices"], counts)
        ]
        out += ["", f"Blank / invalid / missing: {not_valid}", ""]
        if q["id"] == "motivation" and answers:
            out += [
                "Custom grouping (not an NPS score): "
                + ", ".join(
                    f"{name}: {sum(lo <= int(a) <= hi for a in answers)}"
                    for name, lo, hi in MOTIVATION_GROUPS
                ),
                "",
            ]
    out += [
        "## Open-ended answers (verbatim OCR)",
        "",
        "OCR text is Claude's verbatim transcription from `transcriptions.csv` ([illegible] / [word?] mark uncertain words; `pending_transcription` = not read yet); `reviewed` text comes from `manual_corrections.csv`. Interpretation belongs in the qualitative section below, not here.",
        "",
    ]
    for q in (q for q in questions if q["open"]):
        out += [
            f"### `{q['id']}`: {q['text']}",
            "",
            "| Form | Status | OCR text | Reviewed text | Crop |",
            "|---|---|---|---|---|",
        ]
        for r in (r for r in open_rows if r["question_id"] == q["id"]):
            cell = lambda s: s.replace("|", "\\|").replace("\n", " / ")  # noqa: E731
            crop = f"[crop]({r['crop_path']})" if r["crop_path"] else ""
            out.append(
                f"| {r['form_id']} | {r['confidence_or_status']} | {cell(r['ocr_text'])} | {cell(r.get('reviewed_text', ''))} | {crop} |"
            )
        out.append("")
    out += [
        "## Manual review",
        "",
        f"{len(review)} item(s); see `manual_review.csv` and `manual_review/`.",
        "",
    ]
    out += [
        f"- form {r['form_id']}, `{r['question_id']}`: {r['issue']}" for r in review
    ]
    qualitative = (
        report / "qualitative_summary.md"
    )  # written by hand / by Claude after reading the answers; kept across re-runs
    out += [
        "",
        qualitative.read_text(encoding="utf-8")
        if qualitative.exists()
        else "## Qualitative summary\n\n_Not written yet: put it in qualitative_summary.md (themes, sentiment, suggestions, pain points, Explique)._\n",
    ]
    (report / "summary.md").write_text("\n".join(out), encoding="utf-8")


# --- main --------------------------------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--scans", nargs="+", type=Path, help="Scanned PDF(s) of completed forms."
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=BUILD_DIR / "analysis",
        help="AMC project + report directory.",
    )
    parser.add_argument(
        "--tex",
        type=Path,
        default=BUILD_DIR / "BiGHT_Detailed_Feedback_Form_20copies.tex",
        help="Exact LaTeX used for printing.",
    )
    parser.add_argument(
        "--txt",
        type=Path,
        default=BUILD_DIR / "BiGHT_Detailed_Feedback_Form_AMC_fixed.txt",
        help="AMC-TXT source (labels).",
    )
    parser.add_argument(
        "--printed-pdf",
        type=Path,
        default=BUILD_DIR / "BiGHT_Detailed_Feedback_Form_20copies.pdf",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Delete an existing output directory first.",
    )
    parser.add_argument(
        "--report-only",
        action="store_true",
        help="Reuse existing AMC capture (e.g. after manual fixes in AMC); rebuild report only.",
    )
    parser.add_argument("--vector-density", type=int, default=300)
    parser.add_argument("--tol-marque", default="0.2")
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.1,
        help="Darkness ratio from which a box counts as ticked.",
    )
    parser.add_argument(
        "--threshold-up",
        type=float,
        default=0.6,
        help="Darkness ratio above which a box counts as blacked out, i.e. not ticked (2026-10 scan: heaviest tick 0.54, lightest scribble-out 0.63).",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    args.tex, args.txt, args.printed_pdf = (
        args.tex.resolve(),
        args.txt.resolve(),
        args.printed_pdf.resolve(),
    )
    args.scans = [scan.resolve() for scan in args.scans or []]
    project = args.out.resolve()
    report = project / "report"
    questions = parse_questions(args.txt)

    if not args.report_only:
        if not args.scans:
            raise SystemExit("--scans is required unless --report-only")
        for path in [*args.scans, args.tex, args.txt, args.printed_pdf]:
            if not path.exists():
                raise FileNotFoundError(path)
        for command in ["auto-multiple-choice", "xelatex", "pdftoppm"]:
            require_command(command)
        if project.exists() and any(project.iterdir()):
            if not args.force:
                raise SystemExit(
                    f"{project} is not empty; use --force or --report-only"
                )
            shutil.rmtree(project)
        prepare_project(project, args.tex)
        analyse(project, args.scans, args)
    for sub in ["manual_review", "crops", "charts"]:
        shutil.rmtree(report / sub, ignore_errors=True)
        (report / sub).mkdir(parents=True)
    corrections = load_corrections(report)

    n_copies, pages_per_copy, notes, plain = verify_layout(
        project, questions, args.printed_pdf
    )
    regions = open_regions(project, questions, pages_per_copy)
    pages, failed, raw_rows = read_capture(
        project, questions, plain, report / "crops", args
    )
    forms = sorted({form_id(s, c) for s, c, *_ in pages})
    review: list[dict] = []

    scan_pages = sum(
        int(
            re.search(
                r"Pages:\s+(\d+)",
                subprocess.run(
                    ["pdfinfo", str(s)], capture_output=True, text=True
                ).stdout,
            ).group(1)
        )
        for s in args.scans
    )
    pages_info = [
        f"Scanned PDF pages: {scan_pages if args.scans else 'n/a (report-only)'}; pages recognised by AMC: {len(pages)}; unrecognised scan files: {len(failed)}.",
        f"Completed forms detected: {len(forms)} (of {n_copies} printed copies).",
    ]
    if args.scans and scan_pages != len(pages):
        pages_info.append(
            f"WARNING: {scan_pages - len(pages)} scanned page(s) not captured (unrecognised, or the same copy page scanned twice)."
        )
    for name in failed:
        review.append(
            {
                "form_id": "",
                "question_id": "",
                "kind": "page",
                "issue": f"AMC could not recognise {name}",
                "crop_path": "",
            }
        )
    for fid in forms:
        missing = sorted(
            set(range(1, pages_per_copy + 1))
            - {p for s, c, p, *_ in pages if form_id(s, c) == fid}
        )
        if missing:
            review.append(
                {
                    "form_id": fid,
                    "question_id": "",
                    "kind": "page",
                    "issue": f"missing page(s) {missing}",
                    "crop_path": "",
                }
            )
    for s, c, p, *_, mse in pages:
        if mse > 5:
            review.append(
                {
                    "form_id": form_id(s, c),
                    "question_id": "",
                    "kind": "page",
                    "issue": f"page {p}: poor corner-mark fit (mse {mse:.1f})",
                    "crop_path": "",
                }
            )

    closed = [q for q in questions if not q["open"]]
    closed_rows = closed_answers(
        raw_rows, forms, closed, corrections, report, review, args.threshold_up
    )
    open_rows = open_answers(project, report, pages, forms, regions, questions, review)
    for row in open_rows:
        row["reviewed_text"] = corrections.get((row["form_id"], row["question_id"]), "")
    notes.append(
        f"Ticked if darkness in [{args.threshold}, {args.threshold_up}]; above that a box is blacked out and counts as not ticked. "
        f"Flagged as ambiguous: darkness in {AMBIGUOUS_DARKNESS} or within {NEAR_CANCEL} of {args.threshold_up}. Open answers: crops transcribed by Claude into transcriptions.csv."
    )
    if corrections:
        notes.append(
            f"{len(corrections)} manual correction(s) applied from manual_corrections.csv."
        )

    write_csv(
        report / "amc_raw_boxes.csv",
        raw_rows,
        list(raw_rows[0]) if raw_rows else ["form_id"],
    )
    write_csv(
        report / "closed_responses.csv",
        closed_rows,
        ["form_id", *[q["id"] for q in closed], "flags"],
    )
    write_csv(
        report / "open_responses.csv",
        open_rows,
        [
            "form_id",
            "question_id",
            "question_text",
            "ocr_text",
            "confidence_or_status",
            "crop_path",
            "reviewed_text",
        ],
    )
    write_csv(
        report / "manual_review.csv",
        review,
        ["form_id", "question_id", "kind", "issue", "crop_path"],
    )
    write_summary(report, questions, closed_rows, open_rows, review, notes, pages_info)

    print("\n".join(notes + pages_info))
    print(f"Manual-review items: {len(review)}")
    pending = sum(
        r["confidence_or_status"] == "pending_transcription" for r in open_rows
    )
    if pending:
        print(
            f"{pending} open answer(s) awaiting transcription: fill {report / 'transcriptions.csv'} (rules in transcription_instructions.md), then re-run with --report-only."
        )
    print(f"Report: {report}")


if __name__ == "__main__":
    main()
