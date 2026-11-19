#!/usr/bin/env python3
"""Grade a scanned AMC batch from a generated AMC-TXT source.

The intended workflow is:

1. Generate and print the same AMC-TXT source with ``markdown_quiz_to_amc.py``.
2. Grade open questions on paper by ticking the printed 0/1/2 boxes.
3. Scan all completed pages into one or more PDFs (together covering every student).
4. Run this script to produce annotated PDFs and a CSV export.
"""

from __future__ import annotations

import argparse
import csv
import re
import shutil
import sqlite3
import tempfile
import unicodedata
import zipfile
from collections import Counter
from pathlib import Path

from markdown_quiz_to_amc import (
    PAGE_MARKER_RE,
    compile_amc_tex,
    patch_filtered_tex,
    require_command,
    run_command,
)

SCIPER_BOX_MM = (57, 64, 152, 80)
SCIPER_ROW_HEIGHT_MM = 22
SCIPER_LABEL_WIDTH_MM = 20
SCIPER_CROP_WIDTH_MM = 95
SCIPER_MARGIN_MM = 12

OPEN_QUESTION_RE = re.compile(r"^\*<[^>]*>.*")
QUESTION_RE = re.compile(r"^\*\*.*")
CHOICE_RE = re.compile(r"^[+-](?:\[[^\]]*\])?(?:\{([^}]*)\})?")
SCORING_RE = re.compile(r"\{([^}]*)\}")
SCORING_MAX_RE = re.compile(r"(?:^|,)\s*MAX\s*=\s*([+-]?(?:\d+(?:\.\d*)?|\.\d+))")


def parse_float(text: str) -> float | None:
    try:
        return float(text)
    except ValueError:
        return None


def braced_score(line: str) -> float | None:
    match = CHOICE_RE.match(line.strip())
    if not match or match.group(1) is None:
        return None
    return parse_float(match.group(1))


def question_max_score(line: str) -> float | None:
    match = SCORING_RE.search(line)
    if not match:
        return None
    scoring_match = SCORING_MAX_RE.search(match.group(1))
    if not scoring_match:
        return None
    return parse_float(scoring_match.group(1))


def computed_raw_total(amc_txt_path: Path) -> float | None:
    """Estimate the perfect raw score from the generated AMC-TXT file.

    This matches the format emitted by ``markdown_quiz_to_amc.py``: open
    questions use braced per-box scores (the question's max is the highest of
    them), and MCQs declare their max explicitly via a ``MAX=`` directive on
    the question line, since scoring is spread across per-choice ``b``/``m``
    overrides rather than a single question-level value.
    """

    total = 0.0
    saw_question = False
    current = ""
    open_scores: list[float] = []
    mcq_max: float | None = None

    def flush() -> None:
        nonlocal total, current, open_scores, mcq_max, saw_question
        if current == "open" and open_scores:
            total += max(open_scores)
            saw_question = True
        elif current == "mcq" and mcq_max is not None:
            total += mcq_max
            saw_question = True
        current = ""
        open_scores = []
        mcq_max = None

    for raw_line in amc_txt_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if OPEN_QUESTION_RE.match(line):
            flush()
            current = "open"
            continue
        if QUESTION_RE.match(line):
            flush()
            current = "mcq"
            mcq_max = question_max_score(line)
            continue
        if current == "open":
            score = braced_score(line)
            if score is not None:
                open_scores.append(score)

    flush()
    return total if saw_question else None


def make_scan_list(scan_pdfs: list[Path], project_dir: Path) -> Path:
    scan_list = project_dir / "scan-list.txt"
    scan_list.write_text(
        "".join(f"{scan_pdf.resolve()}\n" for scan_pdf in scan_pdfs), encoding="utf-8"
    )
    return scan_list


def ensure_directories(project_dir: Path) -> None:
    for relative in [
        "data",
        "cr",
        "cr/corrections/pdf",
        "exports",
        "scans",
    ]:
        (project_dir / relative).mkdir(parents=True, exist_ok=True)


def build_project_source(
    amc_txt: Path, project_dir: Path, args: argparse.Namespace
) -> Path:
    source_txt = project_dir / "source.txt"
    filtered_tex = project_dir / "source_filtered.tex"
    source_tex = project_dir / "DOC-source.tex"

    shutil.copy2(amc_txt, source_txt)
    run_command(
        [
            "auto-multiple-choice",
            "prepare",
            "--mode",
            "f",
            "--prefix",
            str(project_dir / "DOC-"),
            "--filter",
            "plain",
            "--filtered-source",
            str(filtered_tex),
            str(source_txt),
        ],
        cwd=project_dir,
    )
    if not filtered_tex.exists():
        raise RuntimeError(
            f"AMC did not create expected filtered LaTeX: {filtered_tex}"
        )
    patch_filtered_tex(
        filtered_tex,
        args.copies,
        args.instructions_image,
        args.instructions_image_width,
    )
    shutil.copy2(filtered_tex, source_tex)
    return source_tex


def compile_subject(project_dir: Path, source_tex: Path) -> None:
    compile_amc_tex(project_dir, source_tex.name)
    for suffix in ["pdf", "xy", "amc"]:
        path = project_dir / f"amc-compiled.{suffix}"
        if not path.exists():
            raise RuntimeError(f"XeLaTeX did not create expected file: {path}")
    shutil.copy2(project_dir / "amc-compiled.pdf", project_dir / "DOC-sujet.pdf")
    shutil.copy2(project_dir / "amc-compiled.xy", project_dir / "DOC-calage.xy")


def load_layout(project_dir: Path) -> None:
    run_command(
        [
            "auto-multiple-choice",
            "meptex",
            "--src",
            str(project_dir / "DOC-calage.xy"),
            "--data",
            str(project_dir / "data"),
        ],
        cwd=project_dir,
    )


def extract_scoring(project_dir: Path, source_tex: Path) -> None:
    run_command(
        [
            "auto-multiple-choice",
            "prepare",
            "--mode",
            "b",
            "--prefix",
            str(project_dir / "DOC-"),
            "--data",
            str(project_dir / "data"),
            "--with",
            "xelatex",
            str(source_tex),
        ],
        cwd=project_dir,
    )


def split_scans(project_dir: Path, scan_list: Path, vector_density: int) -> None:
    run_command(
        [
            "auto-multiple-choice",
            "getimages",
            "--list",
            str(scan_list),
            "--copy-to",
            str(project_dir / "scans"),
            "--vector-density",
            str(vector_density),
        ],
        cwd=project_dir,
    )


def analyse_scans(project_dir: Path, scan_list: Path, tolerance: str) -> None:
    run_command(
        [
            "auto-multiple-choice",
            "analyse",
            "--projet",
            str(project_dir),
            "--liste-fichiers",
            str(scan_list),
            "--tol-marque",
            tolerance,
        ],
        cwd=project_dir,
    )


def apply_tick_overrides(project_dir: Path, overrides_csv: Path) -> None:
    """Force boxes AMC misread (e.g. a faint tick) via AMC's own manual field.

    CSV columns: Copie,Question,Answer,Ticked -- Question is the AMC id
    (e.g. mcq1), Answer the option letter in source order, Ticked 1 or 0.
    """
    layout = sqlite3.connect(project_dir / "data/layout.sqlite")
    question_numbers = {
        name: number
        for number, name in layout.execute("SELECT question, name FROM layout_question")
    }
    layout.close()
    capture = sqlite3.connect(project_dir / "data/capture.sqlite")
    with overrides_csv.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            question = question_numbers[row["Question"].strip()]
            answer = ord(row["Answer"].strip().upper()) - ord("A") + 1
            updated = capture.execute(
                "UPDATE capture_zone SET manual = ? "
                "WHERE type = 4 AND student = ? AND id_a = ? AND id_b = ?",
                (float(row["Ticked"]), int(row["Copie"]), question, answer),
            ).rowcount
            if updated != 1:
                raise RuntimeError(f"Tick override matched {updated} boxes: {row}")
    capture.commit()
    capture.close()
    print(f"Applied tick overrides from {overrides_csv}")


def compute_marks(
    project_dir: Path, args: argparse.Namespace, notemax: float | None
) -> None:
    command = [
        "auto-multiple-choice",
        "note",
        "--data",
        str(project_dir / "data"),
        "--notemin",
        "0",
        "--notenull",
        "0",
        "--grain",
        str(args.grain),
        "--arrondi",
        args.rounding,
        "--plafond",
        "--seuil",
        str(args.threshold),
        "--seuil-up",
        str(args.threshold_up),
    ]
    if notemax is not None:
        command.extend(["--notemax", f"{notemax:g}"])
    run_command(command, cwd=project_dir)


def annotate(project_dir: Path, args: argparse.Namespace) -> None:
    command = [
        "auto-multiple-choice",
        "annotate",
        "--project",
        str(project_dir),
        "--subject",
        str(project_dir / "DOC-sujet.pdf"),
        "--pdf-dir",
        str(project_dir / "cr/corrections/pdf"),
        "--verdict",
        args.verdict,
        "--position",
        args.position,
        "--darkness-threshold",
        str(args.threshold),
        "--darkness-threshold-up",
        str(args.threshold_up),
    ]
    if args.single_pdf:
        command.extend(["--single-output", args.single_pdf.name, "--sort", "i"])
    else:
        command.extend(["--filename-model", args.filename_model])
    run_command(command, cwd=project_dir)


def export_csv(project_dir: Path, args: argparse.Namespace) -> None:
    output = project_dir / "exports" / args.csv_name
    run_command(
        [
            "auto-multiple-choice",
            "export",
            "--data",
            str(project_dir / "data"),
            "--module",
            "CSV",
            "--output",
            str(output),
            "--useall",
            "0",
            "--sort",
            "i",
            "--option-out",
            "columns=student.copy",
            "--option-out",
            "decimal=.",
            "--option-out",
            "separateur=,",
        ],
        cwd=project_dir,
    )


def read_grades(csv_path: Path) -> list[tuple[str, float]]:
    """Reads (copy, note) pairs from grades.csv, in the file's own order.

    ``export_csv`` sorts by "i" (student/copy number ascending), which is
    also the order ``annotate`` places copies in when using --single-pdf.
    """
    entries: list[tuple[str, float]] = []
    with csv_path.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            entries.append((row["Copie"], float(row["Note"])))
    return entries


def pages_per_copy(calage_path: Path) -> Counter[int]:
    """Physical page count of each copy, from the calage file's page markers.

    Shuffled copies can span different page counts, so each copy is counted.
    """
    counts = Counter(
        int(match.group(1))
        for line in calage_path.read_text(encoding="utf-8").splitlines()
        if (match := PAGE_MARKER_RE.search(line))
    )
    if not counts:
        raise RuntimeError(f"No page markers found in {calage_path}.")
    return counts


def build_score_stamps(
    project_dir: Path,
    entries: list[tuple[str, float]],
    notemax: float,
    *,
    x_mm: float,
    y_mm: float,
    width_mm: float,
) -> Path:
    """Builds a PDF with one page per entry, each holding just the score text
    positioned at (x_mm, y_mm) from the page's top-left corner, so it can be
    overlaid onto each copy's cover page next to the SCIPER field."""

    pages_tex = []
    for _, note in entries:
        text = f"SCORE: {note:g}/{notemax:g}"
        # A page with only absolute-positioned overlay boxes has no normal
        # flowing content, so consecutive \newpage commands collapse into
        # one; \mbox{} forces each page to actually exist.
        pages_tex.append(
            "\\mbox{}\n"
            f"\\begin{{textblock*}}{{{width_mm}mm}}({x_mm}mm,{y_mm}mm)\n"
            f"\\raggedright\\bfseries {text}\n"
            f"\\end{{textblock*}}"
        )
    body = "\n\\newpage\n".join(pages_tex)
    tex = (
        "\\documentclass[a4paper]{article}\n"
        "\\usepackage[absolute,overlay]{textpos}\n"
        "\\usepackage{xcolor}\n"
        "\\setlength{\\TPHorizModule}{1mm}\\setlength{\\TPVertModule}{1mm}\n"
        "\\pagestyle{empty}\\parindent0pt\\color{red}\n"
        "\\begin{document}\n"
        f"{body}\n"
        "\\end{document}\n"
    )
    stamp_dir = project_dir / "score-stamps"
    stamp_dir.mkdir(exist_ok=True)
    tex_path = stamp_dir / "stamps.tex"
    tex_path.write_text(tex, encoding="utf-8")
    run_command(
        ["xelatex", "-interaction=nonstopmode", "-halt-on-error", "stamps.tex"],
        cwd=stamp_dir,
    )
    pdf_path = stamp_dir / "stamps.pdf"
    if not pdf_path.exists():
        raise RuntimeError(f"XeLaTeX did not create expected PDF: {pdf_path}")
    return pdf_path


def apply_score_stamps(
    pdf_path: Path, stamps_path: Path, page_pairs: list[tuple[int, int]]
) -> None:
    """Overlays stamp pages onto pdf_path.

    ``page_pairs`` is a list of (target_page_index, stamp_page_index), both
    0-based.
    """
    from pypdf import PdfReader, PdfWriter

    stamps = PdfReader(stamps_path)
    writer = PdfWriter(clone_from=pdf_path)
    for target_index, stamp_index in page_pairs:
        writer.pages[target_index].merge_page(stamps.pages[stamp_index])
    with tempfile.NamedTemporaryFile(
        dir=pdf_path.parent, suffix=".pdf", delete=False
    ) as handle:
        writer.write(handle)
        temp_path = Path(handle.name)
    temp_path.replace(pdf_path)


def find_copy_pdf(pdf_dir: Path, filename_model: str, copy_number: str) -> Path:
    """Finds the corrected PDF for a given copy number.

    AMC's --filename-model substitution zero-pads (N) (e.g. "copy-0001.pdf"),
    so matching by substring on the raw copy number is ambiguous -- "1" is a
    substring of "copy-0010.pdf" too. Extract the numeric id and compare as
    an integer instead.
    """
    pattern = re.compile(
        "^" + re.escape(filename_model).replace(re.escape("(N)"), r"(\d+)") + "$"
    )
    for path in sorted(pdf_dir.iterdir()):
        match = pattern.match(path.name)
        if match and int(match.group(1)) == int(copy_number):
            return path
    raise RuntimeError(
        f"Could not find corrected PDF for copy {copy_number} in {pdf_dir} (pattern {filename_model!r})."
    )


def stamp_scores(
    project_dir: Path, args: argparse.Namespace, notemax: float | None
) -> None:
    entries = read_grades(project_dir / "exports" / args.csv_name)
    if not entries:
        return
    if notemax is None:
        notemax = max(note for _, note in entries)
    stamps_path = build_score_stamps(
        project_dir,
        entries,
        notemax,
        x_mm=args.score_stamp_x,
        y_mm=args.score_stamp_y,
        width_mm=args.score_stamp_width,
    )

    if args.single_pdf:
        pdf_path = project_dir / "cr/corrections/pdf" / args.single_pdf.name
        # Copies follow one another in grades.csv order; offset by each one's length.
        page_counts = pages_per_copy(project_dir / "DOC-calage.xy")
        page_pairs, first_page = [], 0
        for stamp_index, (copy_number, _) in enumerate(entries):
            page_pairs.append((first_page, stamp_index))
            first_page += page_counts[int(copy_number)]
        apply_score_stamps(pdf_path, stamps_path, page_pairs)
    else:
        pdf_dir = project_dir / "cr/corrections/pdf"
        for stamp_index, (copy_number, _) in enumerate(entries):
            pdf_path = find_copy_pdf(pdf_dir, args.filename_model, copy_number)
            apply_score_stamps(pdf_path, stamps_path, [(0, stamp_index)])


def read_full_grades(csv_path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with csv_path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def build_sciper_lookup_sheet(
    pdf_dir: Path, filename_model: str, rows: list[dict[str, str]], out_path: Path
) -> None:
    """Crops the handwritten SCIPER box from each copy's cover page into a
    single sheet (copy number next to the crop), for quick manual reading --
    neither AMC nor OCR (tesseract, surya) can reliably read cursive digits.
    """
    import fitz

    mm = 72 / 25.4
    out = fitz.open()
    page_h_mm, page_w_mm = 297, 210
    rows_per_page = int((page_h_mm - 2 * SCIPER_MARGIN_MM) // SCIPER_ROW_HEIGHT_MM)

    page = None
    for index, row in enumerate(rows):
        row_on_page = index % rows_per_page
        if row_on_page == 0:
            page = out.new_page(width=page_w_mm * mm, height=page_h_mm * mm)
        y = (SCIPER_MARGIN_MM + row_on_page * SCIPER_ROW_HEIGHT_MM) * mm
        page.insert_text(
            (SCIPER_MARGIN_MM * mm, y + 5 * mm), f"Copy {row['Copie']}", fontsize=11
        )

        copy_pdf = fitz.open(find_copy_pdf(pdf_dir, filename_model, row["Copie"]))
        clip = fitz.Rect(*(coord * mm for coord in SCIPER_BOX_MM))
        crop_rect = fitz.Rect(
            (SCIPER_MARGIN_MM + SCIPER_LABEL_WIDTH_MM) * mm,
            y,
            (SCIPER_MARGIN_MM + SCIPER_LABEL_WIDTH_MM + SCIPER_CROP_WIDTH_MM) * mm,
            y + SCIPER_ROW_HEIGHT_MM * mm,
        )
        page.show_pdf_page(crop_rect, copy_pdf, 0, clip=clip)
        copy_pdf.close()

    out.save(out_path)


def write_sciper_template(
    rows: list[dict[str, str]], sciper_csv: Path, existing: dict[str, str]
) -> None:
    sciper_csv.parent.mkdir(parents=True, exist_ok=True)
    with sciper_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["Copie", "SCIPER"])
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {"Copie": row["Copie"], "SCIPER": existing.get(row["Copie"], "")}
            )


def read_sciper_map(sciper_csv: Path) -> dict[str, str]:
    if not sciper_csv.exists():
        return {}
    with sciper_csv.open(encoding="utf-8", newline="") as handle:
        return {row["Copie"]: row["SCIPER"].strip() for row in csv.DictReader(handle)}


def finalize_results(
    project_dir: Path,
    fieldnames: list[str],
    rows: list[dict[str, str]],
    sciper_map: dict[str, str],
    results_dir: Path,
    quiz_number: str,
    filename_model: str,
) -> None:
    """Writes the three deliverables the grader actually needs: one PDF per
    student named after their SCIPER, a detailed per-question CSV, and a
    minimal SCIPER+total CSV for Moodle import."""

    pdf_dir = project_dir / "cr/corrections/pdf"
    student_pdf_dir = results_dir / "pdfs"
    grades_dir = results_dir / "grades"
    question_columns = [c for c in fieldnames if c not in ("Copie", "Note")]
    results_dir.mkdir(parents=True, exist_ok=True)
    student_pdf_dir.mkdir(parents=True, exist_ok=True)
    grades_dir.mkdir(parents=True, exist_ok=True)

    grades_path = grades_dir / f"grades_quiz{quiz_number}.csv"
    moodle_path = grades_dir / f"moodle_export_quiz{quiz_number}.csv"
    with (
        grades_path.open("w", encoding="utf-8", newline="") as grades_handle,
        moodle_path.open("w", encoding="utf-8", newline="") as moodle_handle,
    ):
        grades_writer = csv.DictWriter(
            grades_handle, fieldnames=["SCIPER", *question_columns, "Total"]
        )
        grades_writer.writeheader()
        moodle_writer = csv.DictWriter(moodle_handle, fieldnames=["SCIPER", "Total"])
        moodle_writer.writeheader()

        for row in rows:
            sciper = sciper_map[row["Copie"]]
            source_pdf = find_copy_pdf(pdf_dir, filename_model, row["Copie"])
            shutil.copy2(source_pdf, student_pdf_dir / f"{sciper}.pdf")

            grades_writer.writerow(
                {
                    "SCIPER": sciper,
                    **{c: row[c] for c in question_columns},
                    "Total": row["Note"],
                }
            )
            moodle_writer.writerow({"SCIPER": sciper, "Total": row["Note"]})


def normalize_header(value: str) -> str:
    value = (
        unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    )
    return re.sub(r"[^a-z0-9]", "", value.lower())


def format_french_grade(value: str) -> str:
    number = float(value)
    if number.is_integer():
        return str(int(number))
    return f"{number:.2f}".rstrip("0").rstrip(".").replace(".", ",")


def parse_french_number(value: str) -> float | None:
    value = value.strip().replace(" ", "").replace(",", ".")
    if not value:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def write_moodle_deliverables(
    rows: list[dict[str, str]],
    sciper_map: dict[str, str],
    moodle_csv: Path,
    results_dir: Path,
    quiz_number: str,
    notemax: float | None,
) -> None:
    """Fill the ``Note`` column of a Moodle CSV export (one per quiz) with the
    graded notes and write the per-student annotated PDFs into a ZIP using
    Moodle's ``<Full name>_<participant id>_assignsubmission_file_/feedback.pdf``
    upload layout."""

    scores = {sciper_map[row["Copie"]]: row["Note"] for row in rows}

    with moodle_csv.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader)
        table = list(reader)

    def find_column(candidates: set[str]) -> int:
        for index, cell in enumerate(header):
            if normalize_header(cell) in candidates:
                return index
        raise ValueError(f"Column not found in {moodle_csv.name}: {sorted(candidates)}")

    sciper_col = find_column({"numerodidentification", "idnumber"})
    note_col = find_column({"note", "grade"})
    name_col = find_column({"nomcomplet", "fullname"})
    identifiant_col = find_column({"identifiant", "identifier"})
    max_col = find_column({"notemaximale", "maximumgrade"})

    matched = {row[sciper_col].strip() for row in table}
    for sciper in scores:
        if sciper not in matched:
            print(f"WARNING: graded SCIPER {sciper} not found in {moodle_csv.name}.")

    for row in table:
        sciper = row[sciper_col].strip()
        if sciper in scores:
            score = float(scores[sciper])
            max_grade = parse_french_number(row[max_col])
            # AMC notes are already on the 0..notemax scale.
            if notemax and max_grade:
                score = score * max_grade / notemax
            row[note_col] = format_french_grade(str(score))

    grades_dir = results_dir / "grades"
    moodle_dir = results_dir / "moodle"
    student_pdf_dir = results_dir / "pdfs"
    grades_dir.mkdir(parents=True, exist_ok=True)
    moodle_dir.mkdir(parents=True, exist_ok=True)

    out_csv = grades_dir / f"{moodle_csv.stem}-graded{moodle_csv.suffix}"
    with out_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(header)
        writer.writerows(table)

    def participant_id(value: str) -> str:
        digits = re.search(r"\d+", value)
        return digits.group() if digits else value.strip()

    out_zip = moodle_dir / f"quiz{quiz_number}_feedback.zip"
    with zipfile.ZipFile(out_zip, "w", zipfile.ZIP_DEFLATED) as archive:
        for row in table:
            sciper = row[sciper_col].strip()
            if sciper not in scores:
                continue
            pdf = student_pdf_dir / f"{sciper}.pdf"
            if not pdf.exists():
                print(f"WARNING: missing feedback PDF for SCIPER {sciper}, skipping.")
                continue
            folder = f"{row[name_col].strip()}_{participant_id(row[identifiant_col])}_assignsubmission_file_"
            archive.write(pdf, f"{folder}/feedback.pdf")

    print(f"Moodle grades: {out_csv}")
    print(f"Feedback ZIP: {out_zip}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Grade a scanned AMC batch PDF and export annotated PDFs plus grades.csv.",
    )
    parser.add_argument(
        "--txt", required=True, type=Path, help="AMC-TXT source used to print the exam."
    )
    parser.add_argument(
        "--scans",
        required=True,
        type=Path,
        nargs="+",
        help="One or more PDFs containing scanned completed pages (together covering all students).",
    )
    parser.add_argument(
        "--out",
        required=True,
        type=Path,
        help="Output/project directory to create or reuse.",
    )
    parser.add_argument(
        "--quiz-number",
        help="Quiz number/id, e.g. '1'. Used to name grades_quiz<N>.csv, moodle_export_quiz<N>.csv, and the "
        "default results directory. Required unless --prepare-only.",
    )
    parser.add_argument(
        "--results-dir",
        type=Path,
        help="Where to write the per-student PDFs and the two summary CSVs. "
        "Defaults to quiz-drafts/quizzes/quiz<N>/results.",
    )
    parser.add_argument(
        "--sciper-csv",
        type=Path,
        help="Copie,SCIPER mapping to finalize results with. Defaults to <results-dir>/sciper.csv. "
        "If it doesn't exist yet or is missing values, a lookup sheet and a blank/partial template are "
        "(re)written there instead of finalizing, so it can be filled in and the command re-run.",
    )
    parser.add_argument(
        "--tick-overrides",
        type=Path,
        help="Copie,Question,Answer,Ticked CSV forcing boxes AMC misread, applied before scoring. "
        "Defaults to <results-dir>/tick_overrides.csv when that file exists.",
    )
    parser.add_argument(
        "--moodle-csv",
        type=Path,
        help="Moodle CSV export to fill with the graded notes (Note column) and to pair with a "
        "feedback ZIP in Moodle's '<Full name>_<participant id>_assignsubmission_file_/feedback.pdf' layout.",
    )
    parser.add_argument(
        "--copies", type=int, default=30, help="Number of printed randomized copies."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Delete an existing output directory before starting.",
    )
    parser.add_argument(
        "--prepare-only",
        action="store_true",
        help="Only build AMC project files; do not process scans.",
    )
    parser.add_argument(
        "--instructions-image",
        type=Path,
        help="Image used on the printed subject after the name field and before questions.",
    )
    parser.add_argument(
        "--instructions-image-width",
        default="0.92\\linewidth",
        help="LaTeX width used for --instructions-image.",
    )
    parser.add_argument(
        "--vector-density",
        type=int,
        default=300,
        help="DPI for PDF scan rasterization.",
    )
    parser.add_argument(
        "--tol-marque",
        default="0.2",
        help="Corner-mark detection tolerance for AMC analyse.",
    )
    parser.add_argument(
        "--threshold", type=float, default=0.1, help="Lower tick darkness threshold."
    )
    parser.add_argument(
        "--threshold-up",
        type=float,
        default=0.85,
        help="Upper darkness threshold; filled boxes above this are cancelled.",
    )
    parser.add_argument(
        "--grain", type=float, default=0.01, help="Grade rounding granularity."
    )
    parser.add_argument(
        "--rounding",
        choices=["i", "n", "s"],
        default="n",
        help="AMC rounding mode: i=floor, n=nearest, s=ceil.",
    )
    parser.add_argument(
        "--notemax",
        type=float,
        help="Grade scale maximum. Defaults to the computed raw total when possible.",
    )
    parser.add_argument(
        "--filename-model",
        default="copy-(N).pdf",
        help="Filename pattern for per-copy annotated PDFs.",
    )
    parser.add_argument(
        "--single-pdf",
        type=Path,
        help="Write one combined annotated PDF instead of per-copy PDFs.",
    )
    parser.add_argument(
        "--verdict",
        default="",
        help="Header text for annotated PDFs, drawn at AMC's fixed top-left/right corner. "
        "Empty by default since the total score is instead stamped next to the SCIPER field (see --score-stamp-*).",
    )
    parser.add_argument(
        "--position",
        default="marges",
        choices=["marge", "marges", "case", "zones", "none"],
        help="Where to write question scores on annotations.",
    )
    parser.add_argument(
        "--csv-name", default="grades.csv", help="CSV filename under exports/."
    )
    parser.add_argument(
        "--no-score-stamp",
        action="store_true",
        help="Don't stamp the total score next to the SCIPER field on each copy's cover page.",
    )
    parser.add_argument(
        "--score-stamp-x",
        type=float,
        default=155,
        help="Horizontal position (mm from the page's left edge) of the stamped score, just right of the SCIPER box.",
    )
    parser.add_argument(
        "--score-stamp-y",
        type=float,
        default=65,
        help="Vertical position (mm from the page's top edge) of the stamped score, level with the SCIPER box.",
    )
    parser.add_argument(
        "--score-stamp-width",
        type=float,
        default=45,
        help="Width (mm) reserved for the stamped score text.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.copies < 1:
        raise ValueError("--copies must be at least 1.")
    if not args.prepare_only and not args.quiz_number:
        raise ValueError("--quiz-number is required unless --prepare-only.")
    if not args.txt.exists():
        raise FileNotFoundError(args.txt)
    if args.instructions_image is not None and not args.instructions_image.exists():
        raise FileNotFoundError(args.instructions_image)
    if not args.prepare_only:
        missing = [scan for scan in args.scans if not scan.exists()]
        if missing:
            raise FileNotFoundError(missing[0])
    if args.out.exists() and args.force:
        shutil.rmtree(args.out)
    if args.out.exists() and any(args.out.iterdir()) and not args.force:
        raise RuntimeError(
            f"Output directory is not empty: {args.out}. Use --force to replace it."
        )

    for command in ["auto-multiple-choice", "xelatex"]:
        require_command(command)

    project_dir = args.out.resolve()
    project_dir.mkdir(parents=True, exist_ok=True)
    ensure_directories(project_dir)

    raw_total = computed_raw_total(args.txt)
    notemax = args.notemax if args.notemax is not None else raw_total
    source_tex = build_project_source(args.txt.resolve(), project_dir, args)
    compile_subject(project_dir, source_tex)
    load_layout(project_dir)
    extract_scoring(project_dir, source_tex)

    if args.prepare_only:
        print(f"AMC project prepared in {project_dir}")
        return

    scan_list = make_scan_list(args.scans, project_dir)
    split_scans(project_dir, scan_list, args.vector_density)
    analyse_scans(project_dir, scan_list, args.tol_marque)
    results_dir = (
        args.results_dir
        or Path("quiz-drafts") / "quizzes" / f"quiz{args.quiz_number}" / "results"
    )
    overrides_csv = args.tick_overrides or (results_dir / "tick_overrides.csv")
    if overrides_csv.exists():
        apply_tick_overrides(project_dir, overrides_csv)
    compute_marks(project_dir, args, notemax)
    annotate(project_dir, args)
    export_csv(project_dir, args)
    if not args.no_score_stamp:
        stamp_scores(project_dir, args, notemax)

    print(f"Annotated PDFs: {project_dir / 'cr/corrections/pdf'}")
    print(f"Grades CSV: {project_dir / 'exports' / args.csv_name}")

    results_dir.mkdir(parents=True, exist_ok=True)
    sciper_csv = args.sciper_csv or (results_dir / "sciper.csv")
    fieldnames, rows = read_full_grades(project_dir / "exports" / args.csv_name)
    sciper_map = read_sciper_map(sciper_csv)
    missing = [row["Copie"] for row in rows if not sciper_map.get(row["Copie"])]

    if missing:
        lookup_path = results_dir / "sciper-lookup.pdf"
        build_sciper_lookup_sheet(
            project_dir / "cr/corrections/pdf", args.filename_model, rows, lookup_path
        )
        write_sciper_template(rows, sciper_csv, existing=sciper_map)
        print(f"\nSCIPER needed for {len(missing)} of {len(rows)} copies.")
        print(f"Lookup sheet: {lookup_path}")
        print(
            f"Fill in SCIPER values in {sciper_csv}, then re-run this command with --force to finalize."
        )
    else:
        finalize_results(
            project_dir,
            fieldnames,
            rows,
            sciper_map,
            results_dir,
            args.quiz_number,
            args.filename_model,
        )
        if args.moodle_csv is not None:
            write_moodle_deliverables(
                rows,
                sciper_map,
                args.moodle_csv,
                results_dir,
                args.quiz_number,
                notemax,
            )
        print(f"\nResults folder: {results_dir}")
        print(f"  Per-student PDFs: {len(rows)} in {results_dir / 'pdfs'}")
        print(f"  {results_dir / 'grades' / f'grades_quiz{args.quiz_number}.csv'}")
        print(
            f"  {results_dir / 'grades' / f'moodle_export_quiz{args.quiz_number}.csv'}"
        )


if __name__ == "__main__":
    main()
