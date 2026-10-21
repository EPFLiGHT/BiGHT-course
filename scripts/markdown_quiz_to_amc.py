#!/usr/bin/env python3
"""Convert quiz-plan Markdown drafts to AMC-TXT.

Expected input format:
- an open-question section before a ``## MCQs`` heading;
- open questions written as bold numbered prompts; ``*Expected keywords:*``,
  ``*Scoring:*`` and ``*Slides:*`` lines are grading notes, kept off the
  printed quiz (keywords and scoring go to AMC-TXT comments for the grader);
- MCQs written as bold numbered prompts, options ``A. ...``, and a
  ``Correct answer(s): A, C`` line.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from datetime import date
from pathlib import Path

OPEN_HEADING_RE = re.compile(r"^##\s+MCQs\s*$", re.IGNORECASE)
# Titles may write the number as "1." or Markdown-escaped "1\.".
QUESTION_RE = re.compile(r"^\*\*(\d+)\\?\.\s+(.+?)\*\*\s*$")
CHOICE_RE = re.compile(r"^([A-Z])\.\s+(.+?)\s*$")
CRITERIA_RE = re.compile(
    r"^\*(Expected keywords|Scoring|Slides):\*\s*(.+?)\s*$", re.IGNORECASE
)
# Grading notes are kept in the AMC-TXT as comments, for graders only; AMC ignores them.
CRITERIA_COMMENT = "# criteria: "
# AMC's default box is 2.5ex; bigger boxes are easier to tick and to read on scans.
BOX_DIMENSIONS = r"\AMCboxDimensions{size=3.5ex,down=.8ex}"
CORRECT_RE = re.compile(r"^\*\*Correct answer\(s\):\*\*\s+(.+?)\s*$", re.IGNORECASE)
ONECOPY_RE = re.compile(r"\\onecopy\{\d+\}")
HRULE_RE = re.compile(r"\\vspace\{4mm\}\\noindent\\hrule", re.MULTILINE)
PAGE_MARKER_RE = re.compile(r"\\page\{(\d+)/(\d+)/")
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
AMC_MAX_RANDOM_SEED = 4_194_303


@dataclass(frozen=True)
class OpenQuestion:
    number: int
    text: str
    criteria: tuple[str, ...] = ()


@dataclass(frozen=True)
class MCQ:
    text: str
    choices: list[tuple[str, str]]
    correct: set[str]


def strip_inline_markdown(text: str) -> str:
    text = text.strip()
    text = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", text)
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    return text.replace("\\.", ".")


def split_sections(markdown: str) -> tuple[list[str], list[str]]:
    lines = markdown.splitlines()
    for index, line in enumerate(lines):
        if OPEN_HEADING_RE.match(line.strip()):
            return lines[:index], lines[index + 1 :]
    raise ValueError("Could not find a '## MCQs' heading.")


def parse_open_questions(lines: list[str]) -> list[OpenQuestion]:
    questions: list[OpenQuestion] = []
    current_paragraphs: list[str] = []
    current_criteria: list[str] = []

    def finish_question() -> None:
        nonlocal current_paragraphs, current_criteria
        if current_paragraphs:
            if len(current_paragraphs) == 1:
                text = current_paragraphs[0]
            else:
                title = current_paragraphs[0]
                if not title.endswith((".", "?", "!", ":")):
                    title += "."
                text = "\n\n".join([title, *current_paragraphs[1:]])
            questions.append(
                OpenQuestion(current_number, text, tuple(current_criteria))
            )
            current_paragraphs = []
            current_criteria = []

    current_number = 0

    for raw_line in lines:
        line = raw_line.strip()
        match = QUESTION_RE.match(line)
        if match:
            finish_question()
            current_number = int(match.group(1))
            current_paragraphs = [strip_inline_markdown(match.group(2))]
        elif current_paragraphs and (criteria_match := CRITERIA_RE.match(line)):
            label, value = criteria_match.groups()
            if label.lower() != "slides":
                current_criteria.append(
                    f"{label.capitalize()}: {value.replace('*', '')}"
                )
        elif current_paragraphs and line.lower() in {"<br>", "<br/>", "<blank>"}:
            current_paragraphs.append(r"\vspace{2mm}")
        elif current_paragraphs and line:
            current_paragraphs.append(strip_inline_markdown(line))
    finish_question()
    if not questions:
        raise ValueError("No open questions found before the '## MCQs' heading.")
    return questions


def parse_correct_letters(text: str) -> set[str]:
    letters = {letter.strip().upper() for letter in text.split(",") if letter.strip()}
    if not letters or any(not re.fullmatch(r"[A-Z]", letter) for letter in letters):
        raise ValueError(f"Invalid correct-answer list: {text!r}")
    return letters


def finish_mcq(
    question_text: list[str] | None,
    choices: list[tuple[str, str]],
    correct: set[str] | None,
) -> MCQ | None:
    if question_text is None:
        return None
    if not choices:
        raise ValueError(f"MCQ has no choices: {question_text}")
    if correct is None:
        raise ValueError(f"MCQ has no correct-answer line: {question_text}")
    available = {letter for letter, _ in choices}
    missing = correct - available
    if missing:
        raise ValueError(
            f"MCQ correct-answer letters not present in choices for {question_text!r}: "
            f"{', '.join(sorted(missing))}"
        )
    return MCQ("\n\n".join(question_text), choices.copy(), correct.copy())


def parse_mcqs(lines: list[str]) -> list[MCQ]:
    mcqs: list[MCQ] = []
    question_text: list[str] | None = None
    choices: list[tuple[str, str]] = []
    correct: set[str] | None = None

    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue

        question_match = QUESTION_RE.match(line)
        if question_match:
            finished = finish_mcq(question_text, choices, correct)
            if finished is not None:
                mcqs.append(finished)
            question_text = [strip_inline_markdown(question_match.group(2))]
            choices = []
            correct = None
            continue

        if question_text is None:
            continue

        choice_match = CHOICE_RE.match(line)
        if choice_match:
            choices.append(
                (choice_match.group(1), strip_inline_markdown(choice_match.group(2)))
            )
            continue

        correct_match = CORRECT_RE.match(line)
        if correct_match:
            correct = parse_correct_letters(correct_match.group(1))
            continue

        if not choices:
            question_text.append(strip_inline_markdown(line))

    finished = finish_mcq(question_text, choices, correct)
    if finished is not None:
        mcqs.append(finished)
    if not mcqs:
        raise ValueError("No MCQs found after the '## MCQs' heading.")
    return mcqs


def format_decimal(value: float) -> str:
    return f"{value:.6f}".rstrip("0").rstrip(".")


def amc_lines(
    open_questions: list[OpenQuestion],
    mcqs: list[MCQ],
    *,
    title: str,
    presentation: str,
    open_lines: int,
    open_points: int,
    mcq_points: int,
    shuffle_questions: bool,
    random_seed: int | None,
) -> list[str]:
    lines = [
        "# AMC-TXT generated from a Markdown quiz plan.",
        "PaperSize: A4",
        "Lang: EN",
        f"Title: {title}",
        "L-Name: SCIPER",
        "NameFieldLines: 1",
        "CompleteMulti: 0",
        # Keep top-level categories fixed (open questions first, MCQs second).
        # The groups below still shuffle questions within each category.
        "ShuffleQuestions: 0",
        f"LaTeX-BeginDocument: {BOX_DIMENSIONS}",
    ]
    if random_seed is not None:
        lines.append(f"RandomSeed: {random_seed}")
    lines.extend(["", "Presentation: " + presentation, ""])

    open_index = 1

    def emit_open_question(question: OpenQuestion, index: int) -> None:
        question_lines = question.text.splitlines()
        lines.append(
            f"*<lines={open_lines}>[ordered,id=open{index}] {question_lines[0]}"
        )
        lines.extend(question_lines[1:])
        lines.extend(
            [
                "-[0]{0} 0",
                f"-[1]{{{format_decimal(open_points / 2)}}} 1",
                f"+[2]{{{open_points}}} 2",
                *(CRITERIA_COMMENT + criterion for criterion in question.criteria),
                "",
            ]
        )

    def emit_open_group(questions: list[OpenQuestion], *, shuffle: bool) -> None:
        nonlocal open_index
        if not questions:
            return
        lines.extend([f"*([shuffle={'true' if shuffle else 'false'}]", ""])
        for question in questions:
            emit_open_question(question, open_index)
            open_index += 1
        lines.extend(["*)", ""])

    open_units: list[list[OpenQuestion]] = []
    cursor = 0
    while cursor < len(open_questions):
        run_end = cursor + 1
        while (
            run_end < len(open_questions)
            and open_questions[run_end].number == open_questions[cursor].number
        ):
            run_end += 1
        open_units.append(open_questions[cursor:run_end])
        cursor = run_end

    for unit in open_units:
        emit_open_group(unit, shuffle=False)

    mcq_group_shuffle = "true" if shuffle_questions else "false"
    lines.extend([f"*([shuffle={mcq_group_shuffle}]", ""])
    for index, question in enumerate(mcqs, start=1):
        choice_count = len(question.choices)
        correct_count = len(question.correct)
        wrong_count = choice_count - correct_count
        per_correct = mcq_points / correct_count
        wrong_penalty = mcq_points / wrong_count if wrong_count else 0.0
        # Per-choice b/m overrides so only ticked boxes contribute: AMC's
        # default multi-answer scoring instead scores every box by whether
        # its ticked-state matches its correct-state, so a correctly
        # untouched wrong box would earn "b" too, inflating the question
        # far past mcq_points.
        question_lines = question.text.splitlines()
        lines.append(f"**[id=mcq{index}]{{v=0,MAX={mcq_points}}} {question_lines[0]}")
        lines.extend(question_lines[1:])
        for letter, choice_text in question.choices:
            if letter in question.correct:
                lines.append(f"+{{b={format_decimal(per_correct)},m=0}} {choice_text}")
            else:
                lines.append(
                    f"-{{b=0,m=-{format_decimal(wrong_penalty)}}} {choice_text}"
                )
        lines.append("")
    lines.extend(["*)", ""])

    return lines


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

    Keeps the same content (title, SCIPER field, presentation text) and keeps
    the ``\\namefield`` so AMC still recognizes the field.
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

    AMC-TXT cannot nest shuffled groups reliably. The generated TXT therefore
    emits each open-question unit as a fixed top-level group. AMC then creates
    a parent group containing those units plus the MCQ group; here we remove
    the MCQ group from that parent and shuffle only the open-unit parent.
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


def count_pdf_pages(pdf_path: Path) -> int:
    result = run_command(["pdfinfo", str(pdf_path)], cwd=pdf_path.parent)
    for line in result.stdout.splitlines():
        if line.lower().startswith("pages:"):
            return int(line.split()[1])
    raise RuntimeError(f"Could not read the page count from {pdf_path}.")


def pdf_copy_page_ranges(calage_path: Path, copies: int) -> list[tuple[int, int]]:
    """Return the physical start/end page of each copy from the calage file.

    Copies may span a variable number of pages, so the fixed chunking given by
    ``total_pages / copies`` would be wrong. The ``\\page{copy/page}`` markers
    written into the calage file record the exact boundaries.
    """

    pages_by_copy: dict[int, list[int]] = {}
    physical_page = 0
    for line in calage_path.read_text(encoding="utf-8").splitlines():
        match = PAGE_MARKER_RE.search(line)
        if not match:
            continue
        physical_page += 1
        pages_by_copy.setdefault(int(match.group(1)), []).append(physical_page)
    if not pages_by_copy:
        raise RuntimeError(f"No page markers found in {calage_path}.")
    if len(pages_by_copy) != copies:
        raise RuntimeError(
            f"Calage file describes {len(pages_by_copy)} copies, but {copies} were requested."
        )
    ranges: list[tuple[int, int]] = []
    for copy_number in range(1, copies + 1):
        pages = pages_by_copy.get(copy_number)
        if not pages or max(pages) - min(pages) + 1 != len(pages):
            raise RuntimeError(
                f"Calage file has invalid page ranges for copy {copy_number}."
            )
        ranges.append((min(pages), max(pages)))
    return ranges


def extract_pdf_range(source: Path, destination: Path, start: int, end: int) -> None:
    if shutil.which("pdftk") is not None:
        destination.unlink(missing_ok=True)
        run_command(
            [
                "pdftk",
                f"A={source}",
                "cat",
                f"A{start}-{end}",
                "output",
                str(destination),
            ],
            cwd=source.parent,
        )
    elif shutil.which("mutool") is not None:
        run_command(
            [
                "mutool",
                "draw",
                "-F",
                "pdf",
                "-o",
                str(destination),
                str(source),
                f"{start}-{end}",
            ],
            cwd=source.parent,
        )
    else:
        raise RuntimeError("No PDF splitting tool found; install pdftk or mutool.")


def generate_subject_pdfs(
    txt_path: Path,
    subject_dir: Path,
    *,
    pattern: str,
    copies: int,
    work_dir: Path | None,
    instructions_image: Path | None,
    instructions_image_width: str,
) -> None:
    if copies < 1:
        raise ValueError("Copy count must be at least 1.")
    if "(N)" not in pattern:
        raise ValueError("--subject-pattern must contain the (N) placeholder.")

    require_command("auto-multiple-choice")
    require_command("xelatex")
    require_command("pdfinfo")

    subject_dir = subject_dir.resolve()
    subject_dir.mkdir(parents=True, exist_ok=True)

    def build_in(amc_dir: Path) -> None:
        amc_dir.mkdir(parents=True, exist_ok=True)
        source_path = amc_dir / txt_path.name
        shutil.copy2(txt_path, source_path)
        (amc_dir / f"{source_path.stem}-data").mkdir(exist_ok=True)

        run_command(
            [
                "auto-multiple-choice",
                "prepare",
                "--mode",
                "s",
                "--prefix",
                str(amc_dir),
                "--out-sujet",
                str(amc_dir / "initial-subject.pdf"),
                "--filter",
                "plain",
                source_path.name,
            ],
            cwd=amc_dir,
        )

        filtered_tex_path = amc_dir / f"{source_path.stem}_filtered.tex"
        if not filtered_tex_path.exists():
            raise RuntimeError(
                f"AMC did not create expected filtered LaTeX: {filtered_tex_path}"
            )

        patch_copy_count(filtered_tex_path, copies)
        patch_cover_style(filtered_tex_path)
        patch_inline_markup(filtered_tex_path)
        patch_open_unit_shuffle(filtered_tex_path)
        if instructions_image is not None:
            shutil.copy2(instructions_image, amc_dir / instructions_image.name)
            patch_instructions_image(
                filtered_tex_path, instructions_image, instructions_image_width
            )
        patch_page_break_before_questions(filtered_tex_path)
        (amc_dir / "amc-compiled-config.tex").write_text(
            r"\def\SujetExterne{1}\def\NoHyperRef{1}\def\NoWatermarkExterne{1}" + "\n",
            encoding="utf-8",
        )
        run_command(
            [
                "xelatex",
                "-interaction=nonstopmode",
                "-halt-on-error",
                "-jobname=amc-compiled",
                filtered_tex_path.name,
            ],
            cwd=amc_dir,
        )

        combined_pdf = amc_dir / "amc-compiled.pdf"
        calage_path = amc_dir / "amc-compiled.xy"
        if not combined_pdf.exists():
            raise RuntimeError(f"XeLaTeX did not create expected PDF: {combined_pdf}")
        if not calage_path.exists():
            raise RuntimeError(
                f"XeLaTeX did not create expected calage file: {calage_path}"
            )

        total_pages = count_pdf_pages(combined_pdf)
        copy_ranges = pdf_copy_page_ranges(calage_path, copies)
        last_page = copy_ranges[-1][1] if copy_ranges else 0
        if last_page != total_pages:
            raise RuntimeError(
                f"Calage file ends at page {last_page}, but the subject PDF has {total_pages} pages."
            )
        for copy_number, (start, end) in enumerate(copy_ranges, start=1):
            output_name = pattern.replace("(N)", f"{copy_number:04d}")
            extract_pdf_range(combined_pdf, subject_dir / output_name, start, end)

    if work_dir is None:
        with tempfile.TemporaryDirectory(prefix="amc-build-") as temporary_dir:
            build_in(Path(temporary_dir))
    else:
        build_in(work_dir.resolve())

    print(f"Generated {copies} per-copy subject PDFs in {subject_dir}")


def parse_quiz_date_code(code: str) -> tuple[date, int]:
    if not re.fullmatch(r"\d{6}", code):
        raise ValueError(
            f"Invalid quiz date code {code!r}: expected DDMMYY, e.g. 230926."
        )
    day, month, year = int(code[0:2]), int(code[2:4]), int(code[4:6])
    quiz_date = date(2000 + year, month, day)
    seed_source = int(f"{quiz_date:%Y%m%d}")
    random_seed = seed_source % AMC_MAX_RANDOM_SEED or AMC_MAX_RANDOM_SEED
    return quiz_date, random_seed


def build_presentation(args: argparse.Namespace) -> str:
    if args.presentation is not None:
        return args.presentation
    quiz_date, _ = parse_quiz_date_code(args.quiz_date_code)
    return (
        f"{quiz_date.strftime('%B')} {quiz_date.day}, {quiz_date.year}, {args.quiz_time}. Duration: 30 minutes.\n\n"
        "Use a black or blue pen. For each MCQ, mark all correct answers with a clear cross or "
        "tick; the number of correct answers can range from 1 to 5, unless the question says "
        "there is only one.\n\n"
        "Draft paper is authorized as long as it is shown to the course team before the quiz.\n\n"
        "Each question, open-ended or multiple choice, is worth 2 points.\n\nMCQs use negative "
        "marking: incorrect answers subtract points, so the expected score from guessing is 0.\n\n"
        "Points are counted per ticked box, so an MCQ can score below 0, but a box left blank never "
        "costs points."
    )


def convert(input_path: Path, output_path: Path, args: argparse.Namespace) -> None:
    quiz_date, random_seed = parse_quiz_date_code(args.quiz_date_code)
    if not 1 <= random_seed <= AMC_MAX_RANDOM_SEED:
        raise ValueError("AMC random seeds must be between 1 and 4194303.")

    markdown = input_path.read_text(encoding="utf-8")
    open_lines, mcq_lines = split_sections(markdown)
    open_questions = parse_open_questions(open_lines)
    mcqs = parse_mcqs(mcq_lines)
    output = amc_lines(
        open_questions,
        mcqs,
        title=args.title,
        presentation=build_presentation(args),
        open_lines=args.open_lines,
        open_points=args.open_points,
        mcq_points=args.mcq_points,
        shuffle_questions=not args.no_shuffle_questions,
        random_seed=random_seed,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(output).rstrip() + "\n", encoding="utf-8")

    if args.subject_dir is not None:
        generate_subject_pdfs(
            output_path,
            args.subject_dir,
            pattern=args.subject_pattern,
            copies=args.copies,
            work_dir=args.amc_work_dir,
            instructions_image=args.instructions_image,
            instructions_image_width=args.instructions_image_width,
        )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convert a Markdown quiz plan to AMC-TXT.",
    )
    parser.add_argument("input", type=Path, help="Markdown quiz plan to convert.")
    parser.add_argument("output", type=Path, help="AMC-TXT file to write.")
    parser.add_argument("--title", default="Mock Quiz", help="Exam title.")
    parser.add_argument(
        "--presentation",
        help="Full presentation/instructions text. Overrides --quiz-date-code and --quiz-time in the instructions.",
    )
    parser.add_argument(
        "--quiz-date-code",
        default="071026",
        help="Quiz date as DDMMYY, e.g. 071026 means October 7, 2026. Also used as the AMC random seed.",
    )
    parser.add_argument(
        "--quiz-time",
        default="13:20-13:50",
        help="Quiz time shown in the presentation text.",
    )
    parser.add_argument(
        "--open-lines", type=int, default=8, help="Answer lines per open question."
    )
    parser.add_argument(
        "--open-points", type=int, default=2, help="Maximum points per open question."
    )
    parser.add_argument(
        "--mcq-points", type=int, default=2, help="Maximum points per MCQ."
    )
    parser.add_argument(
        "--subject-dir",
        type=Path,
        help="Directory in which to write one printable subject PDF per student/copy.",
    )
    parser.add_argument(
        "--subject-pattern",
        default="copy-(N).pdf",
        help="Filename pattern for --subject-dir; (N) is replaced by the zero-padded copy number.",
    )
    parser.add_argument(
        "--copies",
        type=int,
        default=30,
        help="Number of randomized exam copies to include in --subject-pdf.",
    )
    parser.add_argument(
        "--amc-work-dir",
        type=Path,
        help="Directory for intermediate AMC files. By default, a temporary directory is used.",
    )
    parser.add_argument(
        "--instructions-image",
        type=Path,
        help="Image to show after the name field/instructions and before the first question.",
    )
    parser.add_argument(
        "--instructions-image-width",
        default="0.92\\linewidth",
        help="LaTeX width for --instructions-image, e.g. 0.92\\linewidth.",
    )
    parser.add_argument(
        "--no-shuffle-questions",
        action="store_true",
        help="Keep questions in source order instead of shuffling copies.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    convert(args.input, args.output, args)


if __name__ == "__main__":
    main()
