#!/usr/bin/env python3
"""End-to-end check of amc_feedback_scan.py on synthetic scans of the printed form.

Run: .venv/bin/python scripts/test_amc_feedback_scan.py [keep_report_dir]
(needs AMC, XeLaTeX and quiz-drafts/feedback-form-build/; Tesseract only stands in for Claude reading the crops)
"""

from __future__ import annotations

import csv
import sqlite3
import subprocess
import sys
import tempfile
from pathlib import Path

import cv2
import pytesseract
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import amc_feedback_scan as fs  # noqa: E402

# form copy -> closed answers (labels; a list = several ticks, None = blank) and open answers
FORMS = {
    1: (
        {
            "overall": "4",
            "lecturesuseful": "5",
            "motivation": "5",
            "weeklyhours": "about 2 to 6h",
            "workload": "3",
            "quizformat": "4",
            "expliqueuse": "Both quizzes",
        },
        {
            "worksplit": "30% quizzes 70% project",
            "coursethoughts": "The lectures are great but the project deadlines are tight",
            "expliquethoughts": "Useful for quiz practice",
        },
    ),
    2: (
        {
            "overall": None,
            "lecturesuseful": "2",
            "motivation": ["3", "8"],
            "weeklyhours": "> 15h",
            "workload": "5",
            "quizformat": "1",
            "expliqueuse": "None of them",
        },
        {
            "worksplit": "",
            "coursethoughts": "Too much workload for eight credits",
            "expliquethoughts": "I did not understand its purpose",
        },
    ),
    3: (
        {
            "overall": "3",
            "lecturesuseful": "3",
            "motivation": "10",
            "weeklyhours": "< 2h",
            "workload": "1",
            "quizformat": "5",
            "expliqueuse": "Only quiz 1",
        },
        {"worksplit": "half and half", "coursethoughts": "", "expliquethoughts": ""},
    ),
}
MISSING_PAGE2_COPY = 4  # only page 1 scanned, all blank
BLACKED_OUT = {
    1: {"overall": "2", "motivation": "7"},
    3: {"weeklyhours": "> 15h"},
}  # solid fill = cancelled, not ticked


def make_scans(project: Path, printed_pdf: Path, out_pdf: Path) -> None:
    questions = fs.parse_questions(
        ROOT / fs.BUILD_DIR / "BiGHT_Detailed_Feedback_Form_AMC_fixed.txt"
    )
    regions = fs.open_regions(project, questions, 2)
    plain = fs.plain_boxes(project, questions, {"motivation"}, 2)
    labels = {q["id"]: q["choices"] for q in questions}
    db = sqlite3.connect(project / "data" / "layout.sqlite")
    names = dict(db.execute("SELECT question, name FROM layout_question"))
    hand = ImageFont.truetype("DejaVuSans.ttf", 44)

    pages = []
    for copy in [*FORMS, MISSING_PAGE2_COPY]:
        closed, open_ = FORMS.get(copy, ({}, {}))
        for page in (1, 2):
            if copy == MISSING_PAGE2_COPY and page == 2:
                continue
            index = (copy - 1) * 2 + page
            subprocess.run(
                [
                    "pdftoppm",
                    "-r",
                    "300",
                    "-gray",
                    "-f",
                    str(index),
                    "-l",
                    str(index),
                    "-singlefile",
                    str(printed_pdf),
                    str(out_pdf.parent / "pg"),
                ],
                check=True,
            )
            image = Image.open(out_pdf.parent / "pg.pgm").convert("L")
            draw = ImageDraw.Draw(image)
            boxes = [
                (names[q], a, x0, x1, y0, y1)
                for q, a, x0, x1, y0, y1 in db.execute(
                    "SELECT question, answer, xmin, xmax, ymin, ymax FROM layout_box WHERE student=? AND page=?",
                    (copy, page),
                )
            ]
            boxes += [
                (qid, a, x0, x1, y0, y1)
                for qid, rects in plain.items()
                for a, (p, x0, y0, x1, y1) in enumerate(rects, 1)
                if p == page
            ]
            for qid, answer, x0, x1, y0, y1 in boxes:
                wanted = closed.get(qid)
                wanted = wanted if isinstance(wanted, list) else [wanted]
                if labels[qid][answer - 1] in wanted:  # a cross, like a student's tick
                    draw.line((x0 + 6, y0 + 6, x1 - 6, y1 - 6), fill=30, width=7)
                    draw.line((x0 + 6, y1 - 6, x1 - 6, y0 + 6), fill=30, width=7)
                if BLACKED_OUT.get(copy, {}).get(qid) == labels[qid][answer - 1]:
                    draw.rectangle((x0 - 2, y0 - 2, x1 + 2, y1 + 2), fill=15)
            for qid, text in open_.items():
                p, x0, y0, x1, y1 = regions[qid]
                if p == page and text:
                    draw.text((x0 + 40, y0 + 10), text, font=hand, fill=20)
            pages.append(
                image.rotate(0.6 if copy == 2 else 0, fillcolor=255, expand=False)
            )
    pages.reverse()  # AMC must identify pages by their codes, not by order
    pages[0].save(out_pdf, save_all=True, append_images=pages[1:], resolution=300)


def read(report: Path, name: str, key) -> dict:
    return {key(r): r for r in csv.DictReader((report / name).open())}


def transcribe_like_claude(report: Path) -> None:
    """Stand-in for the Claude session reading each crop: Tesseract on the typed test text."""
    sheet = list(csv.DictReader((report / "transcriptions.csv").open()))
    for row in sheet:
        gray = cv2.imread(str(report / row["crop_path"]), cv2.IMREAD_GRAYSCALE)
        _, ink = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)
        _, labels, stats, _ = cv2.connectedComponentsWithStats(ink)
        dots = (stats[:, cv2.CC_STAT_WIDTH] <= 9) & (
            stats[:, cv2.CC_STAT_HEIGHT] <= 9
        )  # printed dotted lines
        ink[dots[labels] & (labels > 0)] = 0
        text = pytesseract.image_to_string(
            Image.fromarray(255 - ink), config="--psm 6"
        ).strip()
        row["text"] = text
        row["legibility"] = (
            "empty"
            if not text
            else "partly_uncertain"
            if (row["form_id"], row["question_id"]) == ("02", "expliquethoughts")
            else "clear"
        )
    with (report / "transcriptions.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(sheet[0]))
        writer.writeheader()
        writer.writerows(sheet)


def main() -> None:
    script = [sys.executable, str(ROOT / "scripts/amc_feedback_scan.py")]
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        layout = tmp / "layout"
        fs.prepare_project(
            layout, ROOT / fs.BUILD_DIR / "BiGHT_Detailed_Feedback_Form_20copies.tex"
        )
        scan = tmp / "scan.pdf"
        make_scans(
            layout,
            ROOT / fs.BUILD_DIR / "BiGHT_Detailed_Feedback_Form_20copies.pdf",
            scan,
        )
        out = tmp / "analysis"
        report = out / "report"

        # 1. scan analysis: closed answers read, open answers cropped and waiting for transcription
        subprocess.run(
            [*script, "--scans", str(scan), "--out", str(out)], cwd=ROOT, check=True
        )
        closed = read(report, "closed_responses.csv", lambda r: r["form_id"])
        opened = read(
            report, "open_responses.csv", lambda r: (r["form_id"], r["question_id"])
        )
        assert sorted(closed) == ["01", "02", "03", "04"], closed.keys()
        for copy, (answers, _) in FORMS.items():
            for qid, want in answers.items():
                got = closed[f"{copy:02d}"][qid]
                assert got == (want if isinstance(want, str) else ""), (
                    copy,
                    qid,
                    got,
                    want,
                )
        assert (
            "overall=blank" in closed["02"]["flags"]
            and "motivation=multiple:3|8" in closed["02"]["flags"]
        )
        assert (
            closed["01"]["flags"] == "" and closed["03"]["flags"] == ""
        )  # blacked-out boxes are silently not ticked
        assert (
            opened[("01", "worksplit")]["confidence_or_status"]
            == "pending_transcription"
        )
        assert (
            opened[("04", "coursethoughts")]["confidence_or_status"] == "page_missing"
        )
        sheet = read(
            report, "transcriptions.csv", lambda r: (r["form_id"], r["question_id"])
        )
        assert (
            len(sheet) == 10 and ("04", "coursethoughts") not in sheet
        )  # 3 full forms x 3 + form 4 page 1
        assert (report / "transcription_instructions.md").exists()

        # 2. Claude fills transcriptions.csv, then --report-only merges it
        transcribe_like_claude(report)
        subprocess.run(
            [*script, "--report-only", "--out", str(out)], cwd=ROOT, check=True
        )
        opened = read(
            report, "open_responses.csv", lambda r: (r["form_id"], r["question_id"])
        )
        review = list(csv.DictReader((report / "manual_review.csv").open()))
        for copy, (_, texts) in FORMS.items():
            for qid, want in texts.items():
                got = opened[(f"{copy:02d}", qid)]
                assert (report / got["crop_path"]).exists()
                if not want:
                    assert got["confidence_or_status"] == "empty", (copy, qid, got)
                    continue
                words, found = (
                    set(want.lower().split()),
                    set(got["ocr_text"].lower().split()),
                )
                assert len(words & found) >= len(words) / 2, (
                    copy,
                    qid,
                    got["ocr_text"],
                )  # crop holds the right answer
        assert opened[("02", "expliquethoughts")]["confidence_or_status"] == "uncertain"
        assert any(
            r["form_id"] == "02" and r["question_id"] == "expliquethoughts"
            for r in review
        )
        assert any(
            r["form_id"] == "04" and "missing page" in r["issue"] for r in review
        )
        for qid in ["overall", "motivation", "weeklyhours", "expliqueuse"]:
            assert (report / "charts" / f"{qid}.png").exists()
        assert "Completed forms detected: 4" in (report / "summary.md").read_text()

        # 3. human corrections survive a re-run
        (report / "manual_corrections.csv").write_text(
            "form_id,question_id,value\n2,motivation,8\n03,coursethoughts,checked: really empty\n"
        )
        subprocess.run(
            [*script, "--report-only", "--out", str(out)], cwd=ROOT, check=True
        )
        closed = read(report, "closed_responses.csv", lambda r: r["form_id"])
        opened = read(
            report, "open_responses.csv", lambda r: (r["form_id"], r["question_id"])
        )
        assert (
            closed["02"]["motivation"] == "8"
            and "motivation=manually_corrected" in closed["02"]["flags"]
        )
        assert (
            opened[("03", "coursethoughts")]["reviewed_text"] == "checked: really empty"
        )
        assert (
            opened[("01", "worksplit")]["confidence_or_status"] == "ok"
        )  # transcriptions kept across re-runs
        if len(sys.argv) > 1:  # keep the report for inspection
            subprocess.run(["cp", "-r", str(report), sys.argv[1]], check=True)
        print("OK")


if __name__ == "__main__":
    main()
