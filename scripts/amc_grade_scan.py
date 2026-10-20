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
import html
import re
import shutil
import subprocess
import tempfile
import unicodedata
import zipfile
from pathlib import Path

SCIPER_BOX_MM = (57, 64, 152, 80)
SCIPER_ROW_HEIGHT_MM = 22
SCIPER_LABEL_WIDTH_MM = 20
SCIPER_CROP_WIDTH_MM = 95
SCIPER_MARGIN_MM = 12

ONECOPY_RE = re.compile(r"\\onecopy\{\d+\}")
PAGE_MARKER_RE = re.compile(r"\\page\{(\d+)/")
HRULE_RE = re.compile(r"\\vspace\{4mm\}\\noindent\\hrule", re.MULTILINE)
SHUFFLEGROUP_RE = re.compile(r"\\shufflegroup\{")
COVER_BODY_RE = re.compile(
    r"(\\onecopy\{\d+\}\{)(.*?)(\\vspace\{4mm\}\\noindent\\hrule)",
    re.DOTALL,
)
TITLE_IN_COVER_RE = re.compile(
    r"\\begin\{center\}\s*\\bf\\large\s*(.*?)\\end\{center\}", re.DOTALL
)
NAMEFIELD_END = "\\end{minipage}\\vspace{4mm}"
ESCAPED_TEXTBF_RE = re.compile(r"\\\(\\backslash\\\)textbf\\\{(.*?)\\\}")
OPEN_QUESTION_RE = re.compile(r"^\*<[^>]*>.*")
OPEN_TITLE_RE = re.compile(r"^\*<[^>]*>\[[^\]]*\]\s*(.*)")
# Written by markdown_quiz_to_amc.py after each open question's score boxes.
CRITERIA_COMMENT = "# criteria: "
QUESTION_RE = re.compile(r"^\*\*.*")
CHOICE_RE = re.compile(r"^[+-](?:\[[^\]]*\])?(?:\{([^}]*)\})?")
SCORING_RE = re.compile(r"\{([^}]*)\}")
SCORING_MAX_RE = re.compile(r"(?:^|,)\s*MAX\s*=\s*([+-]?(?:\d+(?:\.\d*)?|\.\d+))")


def run_command(command: list[str], *, cwd: Path) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        command, cwd=cwd, text=True, capture_output=True, check=False
    )
    if result.returncode != 0:
        output = "\n".join(part for part in [result.stdout, result.stderr] if part)
        raise RuntimeError(f"Command failed: {' '.join(command)}\n{output}")
    return result


def require_command(command: str) -> None:
    if shutil.which(command) is None:
        raise RuntimeError(f"Required command not found: {command}")


def patch_copy_count(filtered_tex_path: Path, copies: int) -> None:
    tex = filtered_tex_path.read_text(encoding="utf-8")
    tex, replacements = ONECOPY_RE.subn(
        lambda _: f"\\onecopy{{{copies}}}", tex, count=1
    )
    if replacements != 1:
        raise RuntimeError(
            f"Could not find exactly one \\onecopy{{...}} command in {filtered_tex_path}."
        )
    filtered_tex_path.write_text(tex, encoding="utf-8")


def patch_instructions_image(
    filtered_tex_path: Path, image_path: Path, width: str
) -> None:
    tex = filtered_tex_path.read_text(encoding="utf-8")
    if "\\usepackage{graphicx}" not in tex:
        tex = tex.replace(
            "\\usepackage{xltxtra}\n",
            "\\usepackage{xltxtra}\n\\usepackage{graphicx}\n",
            1,
        )

    image_block = (
        "\\par\\vspace{2mm}\\noindent\\begin{center}\n"
        f"\\includegraphics[width={width}]{{{image_path.name}}}\n"
        "\\end{center}\\par\\vspace{2mm}\n\n"
    )
    replacement = image_block + r"\vspace{4mm}\noindent\hrule"
    tex, replacements = HRULE_RE.subn(lambda _: replacement, tex, count=1)
    if replacements != 1:
        raise RuntimeError(
            f"Could not find insertion point for instructions image in {filtered_tex_path}."
        )
    filtered_tex_path.write_text(tex, encoding="utf-8")


def patch_page_break_before_questions(filtered_tex_path: Path) -> None:
    """Keep the first page of each copy cover-only (SCIPER field, instructions)."""
    tex = filtered_tex_path.read_text(encoding="utf-8")
    tex, replacements = SHUFFLEGROUP_RE.subn(
        lambda match: "\\newpage\n\n" + match.group(0), tex, count=1
    )
    if replacements != 1:
        raise RuntimeError(
            f"Could not find a question group in {filtered_tex_path} to insert a page break before."
        )
    filtered_tex_path.write_text(tex, encoding="utf-8")


def patch_cover_style(filtered_tex_path: Path) -> None:
    """Replace the plain AMC cover with a larger, more polished layout.

    Must produce exactly the same output as the print script (see
    markdown_quiz_to_amc.py's patch_cover_style, which this mirrors) so that
    the rebuilt subject used for scan calibration matches the printed sheets.
    """

    tex = filtered_tex_path.read_text(encoding="utf-8")
    body_match = COVER_BODY_RE.search(tex)
    if not body_match:
        raise RuntimeError(f"Could not find the cover block in {filtered_tex_path}.")
    opener, body, closing = (
        body_match.group(1),
        body_match.group(2),
        body_match.group(3),
    )

    title_match = TITLE_IN_COVER_RE.search(body)
    title = title_match.group(1).strip() if title_match else "Quiz"

    rest_index = body.rfind(NAMEFIELD_END)
    if rest_index < 0:
        raise RuntimeError(
            f"Could not find the name-field block in {filtered_tex_path}."
        )
    presentation = body[rest_index + len(NAMEFIELD_END) :].strip().splitlines()
    paragraphs = [paragraph.strip() for paragraph in presentation if paragraph.strip()]

    lines = [
        "\\vspace{3mm}",
        "\\begin{center}",
        f"{{\\Huge\\bfseries {title}\\par}}",
        "\\vspace{2mm}",
        "\\rule{0.6\\linewidth}{1.2pt}\\par",
        "\\vspace{4mm}",
        "\\end{center}",
        "\\vspace{3mm}",
        "\\namefield{%",
        "\\hbox to \\linewidth{\\hss",
        "{\\fboxsep=4mm\\fbox{\\begin{minipage}{.58\\linewidth}",
        "\\centering",
        "{\\LARGE\\bfseries SCIPER}\\\\[5mm]",
        "\\dotfill",
        "\\end{minipage}}}",
        "\\hss}%",
        "}",
        "",
    ]
    lines.append("\\vspace{3mm}")
    for paragraph in paragraphs:
        lines.append(
            f"\\begin{{center}}{{\\large {paragraph}\\par}}\\end{{center}}\\vspace{{2mm}}"
        )

    new_cover = opener + "\n" + "\n".join(lines) + "\n\n" + closing
    tex, replacements = COVER_BODY_RE.subn(lambda _: new_cover, tex, count=1)
    if replacements != 1:
        raise RuntimeError(f"Could not replace the cover block in {filtered_tex_path}.")
    filtered_tex_path.write_text(tex, encoding="utf-8")


def patch_inline_markup(filtered_tex_path: Path) -> None:
    tex = filtered_tex_path.read_text(encoding="utf-8")
    tex = ESCAPED_TEXTBF_RE.sub(r"\\textbf{\1}", tex)
    tex = tex.replace(r"\(\backslash\)vspace\{2mm\}", r"\vspace{2mm}")
    filtered_tex_path.write_text(tex, encoding="utf-8")


def patch_open_unit_shuffle(filtered_tex_path: Path) -> None:
    """Shuffle open-question units while keeping multi-field units adjacent.

    Must mirror markdown_quiz_to_amc.py's patch so the grading layout matches
    the printed layout exactly.
    """

    tex = filtered_tex_path.read_text(encoding="utf-8")
    parent_names = re.findall(
        r"\\def\\insertPlainGroup(gr\w+)\{\\insertgroup\{\1\}\}", tex
    )
    for parent in parent_names:
        children = re.findall(
            rf"\\element\{{{re.escape(parent)}\}}\{{\n\\insertPlainGroup([^\n]+)\n\}}\n",
            tex,
        )
        if len(children) < 2:
            continue

        open_children: list[str] = []
        mcq_children: list[str] = []
        for child in children:
            start = tex.find(f"\\element{{{child}}}")
            end = tex.find(f"\\def\\insertPlainGroup{child}", start)
            if start < 0 or end < 0:
                continue
            chunk = tex[start:end]
            if r"\begin{questionmult}" in chunk:
                mcq_children.append(child)
            elif r"\begin{question}" in chunk:
                open_children.append(child)

        if len(open_children) < 2 or not mcq_children:
            continue

        for child in mcq_children:
            tex = tex.replace(
                f"\\element{{{parent}}}{{\n\\insertPlainGroup{child}\n}}\n", ""
            )

        replacement = "\n".join(
            [
                f"\\shufflegroup{{{parent}}}",
                f"\\insertPlainGroup{parent}",
                *[f"\\insertPlainGroup{child}" for child in mcq_children],
            ]
        )
        tex, replacements = re.subn(
            rf"(?m)^\\insertPlainGroup{re.escape(parent)}$",
            lambda _: replacement,
            tex,
            count=1,
        )
        if replacements != 1:
            raise RuntimeError(
                f"Could not find insertion point for shuffled open group {parent} in {filtered_tex_path}."
            )
        filtered_tex_path.write_text(tex, encoding="utf-8")
        return

    filtered_tex_path.write_text(tex, encoding="utf-8")


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
    patch_copy_count(filtered_tex, args.copies)
    patch_cover_style(filtered_tex)
    patch_inline_markup(filtered_tex)
    patch_open_unit_shuffle(filtered_tex)
    if args.instructions_image is not None:
        shutil.copy2(
            args.instructions_image, project_dir / args.instructions_image.name
        )
        patch_instructions_image(
            filtered_tex, args.instructions_image, args.instructions_image_width
        )
    patch_page_break_before_questions(filtered_tex)
    shutil.copy2(filtered_tex, source_tex)
    return source_tex


def compile_subject(project_dir: Path, source_tex: Path) -> None:
    (project_dir / "amc-compiled-config.tex").write_text(
        r"\def\SujetExterne{1}\def\NoHyperRef{1}\def\NoWatermarkExterne{1}" + "\n",
        encoding="utf-8",
    )
    run_command(
        [
            "xelatex",
            "-interaction=nonstopmode",
            "-halt-on-error",
            "-jobname=amc-compiled",
            source_tex.name,
        ],
        cwd=project_dir,
    )
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


def compute_marks(
    project_dir: Path, args: argparse.Namespace, raw_total: float | None
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
    notemax = args.notemax if args.notemax is not None else raw_total
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


def copy_pages_per_copy(calage_path: Path) -> int:
    """Counts the physical pages of copy 1 from the calage file.

    All copies share the same question set (just reshuffled), so every copy
    has the same page count.
    """
    count = sum(
        1
        for line in calage_path.read_text(encoding="utf-8").splitlines()
        if PAGE_MARKER_RE.match(line) and PAGE_MARKER_RE.match(line).group(1) == "1"
    )
    if not count:
        raise RuntimeError(f"No page markers found for copy 1 in {calage_path}.")
    return count


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
    project_dir: Path, args: argparse.Namespace, raw_total: float | None
) -> None:
    entries = read_grades(project_dir / "exports" / args.csv_name)
    if not entries:
        return
    notemax = args.notemax if args.notemax is not None else raw_total
    if notemax is None:
        notemax = max(note for _, note in entries)
    pages_per_copy = copy_pages_per_copy(project_dir / "DOC-calage.xy")
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
        page_pairs = [(i * pages_per_copy, i) for i in range(len(entries))]
        apply_score_stamps(pdf_path, stamps_path, page_pairs)
    else:
        pdf_dir = project_dir / "cr/corrections/pdf"
        for stamp_index, (copy_number, _) in enumerate(entries):
            pdf_path = find_copy_pdf(pdf_dir, args.filename_model, copy_number)
            apply_score_stamps(pdf_path, stamps_path, [(0, stamp_index)])


def read_open_criteria(amc_txt_path: Path) -> list[tuple[str, list[str]]]:
    """Returns (question title, criteria lines) for each open question that
    has ``# criteria:`` comments in the AMC-TXT source, in source order."""

    criteria: list[tuple[str, list[str]]] = []
    title = ""
    for raw_line in amc_txt_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        title_match = OPEN_TITLE_RE.match(line)
        if title_match:
            title = re.sub(r"\\textbf\{(.*?)\}", r"\1", title_match.group(1))
        elif line.startswith(CRITERIA_COMMENT):
            if not criteria or criteria[-1][0] != title:
                criteria.append((title, []))
            criteria[-1][1].append(line.removeprefix(CRITERIA_COMMENT))
    return criteria


def append_criteria_page(project_dir: Path, args: argparse.Namespace) -> None:
    """Appends one page listing the open questions' expected keywords and
    scoring rules to every annotated copy, so students see how they were graded."""

    criteria = read_open_criteria(args.txt)
    if not criteria:
        return
    if args.single_pdf:
        # ponytail: per-copy PDFs only; inserting after each copy of a single PDF needs page offsets.
        print("Skipping grading-criteria page: not supported with --single-pdf.")
        return

    import fitz

    parts = ["<h2>Grading criteria for open questions</h2>"]
    for title, lines in criteria:
        parts.append(f"<p><b>{html.escape(title)}</b></p>")
        for line in lines:
            label, _, value = line.partition(": ")
            parts.append(f"<p><i>{html.escape(label)}:</i> {html.escape(value)}</p>")
    page_html = "\n".join(parts)

    mm = 72 / 25.4
    pattern = re.compile(
        "^" + re.escape(args.filename_model).replace(re.escape("(N)"), r"\d+") + "$"
    )
    for pdf_path in sorted((project_dir / "cr/corrections/pdf").iterdir()):
        if not pattern.match(pdf_path.name):
            continue
        document = fitz.open(pdf_path)
        page = document.new_page(width=210 * mm, height=297 * mm)
        spare_height, _ = page.insert_htmlbox(
            fitz.Rect(20 * mm, 20 * mm, 190 * mm, 277 * mm), page_html
        )
        if spare_height < 0:
            raise RuntimeError(
                "Grading criteria do not fit on one page; shorten the keywords or scoring rules."
            )
        temp_path = pdf_path.with_suffix(".tmp")
        document.save(temp_path)
        document.close()
        temp_path.replace(pdf_path)


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
    raw_total: float | None,
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
            if raw_total and max_grade:
                score = score * max_grade / raw_total
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
    compute_marks(project_dir, args, raw_total)
    annotate(project_dir, args)
    export_csv(project_dir, args)
    if not args.no_score_stamp:
        stamp_scores(project_dir, args, raw_total)
    append_criteria_page(project_dir, args)

    print(f"Annotated PDFs: {project_dir / 'cr/corrections/pdf'}")
    print(f"Grades CSV: {project_dir / 'exports' / args.csv_name}")

    results_dir = (
        args.results_dir
        or Path("quiz-drafts") / "quizzes" / f"quiz{args.quiz_number}" / "results"
    )
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
            f"Fill in SCIPER values in {sciper_csv}, then re-run this same command to finalize."
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
                raw_total,
            )
        print(f"\nResults folder: {results_dir}")
        print(f"  Per-student PDFs: {len(rows)} in {results_dir / 'pdfs'}")
        print(f"  {results_dir / 'grades' / f'grades_quiz{args.quiz_number}.csv'}")
        print(
            f"  {results_dir / 'grades' / f'moodle_export_quiz{args.quiz_number}.csv'}"
        )


if __name__ == "__main__":
    main()
