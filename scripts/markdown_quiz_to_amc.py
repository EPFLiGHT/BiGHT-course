#!/usr/bin/env python3
"""Convert quiz-plan Markdown drafts to AMC-TXT.

Expected input format:
- an open-question section before a ``## MCQs`` heading;
- open questions written as bold numbered prompts, followed by grading notes;
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
from pathlib import Path

OPEN_HEADING_RE = re.compile(r"^##\s+MCQs\s*$", re.IGNORECASE)
QUESTION_RE = re.compile(r"^\*\*(\d+)\\\.\s+(.+?)\*\*\s*$")
CHOICE_RE = re.compile(r"^([A-Z])\.\s+(.+?)\s*$")
CORRECT_RE = re.compile(r"^\*\*Correct answer\(s\):\*\*\s+(.+?)\s*$", re.IGNORECASE)
ONECOPY_RE = re.compile(r"\\onecopy\{\d+\}")


@dataclass(frozen=True)
class OpenQuestion:
    text: str


@dataclass(frozen=True)
class MCQ:
    text: str
    choices: list[tuple[str, str]]
    correct: set[str]


def strip_inline_markdown(text: str) -> str:
    text = text.strip()
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
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
    for line in lines:
        match = QUESTION_RE.match(line.strip())
        if match:
            questions.append(OpenQuestion(strip_inline_markdown(match.group(2))))
    if not questions:
        raise ValueError("No open questions found before the '## MCQs' heading.")
    return questions


def parse_correct_letters(text: str) -> set[str]:
    letters = {letter.strip().upper() for letter in text.split(",") if letter.strip()}
    if not letters or any(not re.fullmatch(r"[A-Z]", letter) for letter in letters):
        raise ValueError(f"Invalid correct-answer list: {text!r}")
    return letters


def finish_mcq(
    question_text: str | None,
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
    return MCQ(question_text, choices.copy(), correct.copy())


def parse_mcqs(lines: list[str]) -> list[MCQ]:
    mcqs: list[MCQ] = []
    question_text: str | None = None
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
            question_text = strip_inline_markdown(question_match.group(2))
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
    name_label: str,
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
        f"L-Name: {name_label}",
        "NameFieldLines: 2",
        "CompleteMulti: 0",
        f"ShuffleQuestions: {1 if shuffle_questions else 0}",
    ]
    if random_seed is not None:
        lines.append(f"RandomSeed: {random_seed}")
    lines.extend(["", "Presentation: " + presentation, ""])

    open_group_shuffle = "true" if shuffle_questions else "false"
    lines.extend([f"*([shuffle={open_group_shuffle},group=open]", ""])
    for index, question in enumerate(open_questions, start=1):
        lines.extend(
            [
                f"*<lines={open_lines}>[ordered,id=open{index}] {question.text}",
                "-[0]{0} 0",
                f"-[1]{{{format_decimal(open_points / 2)}}} 1",
                f"+[2]{{{open_points}}} 2",
                "",
            ]
        )
    lines.extend(["*)", ""])

    mcq_group_shuffle = "true" if shuffle_questions else "false"
    lines.extend([f"*([shuffle={mcq_group_shuffle},group=mcq]", ""])
    for index, question in enumerate(mcqs, start=1):
        choice_count = len(question.choices)
        per_choice = mcq_points / choice_count
        scoring = f"b={format_decimal(per_choice)},m=-{format_decimal(per_choice)},v=0"
        lines.append(f"**[id=mcq{index}]{{{scoring}}} {question.text}")
        for letter, choice_text in question.choices:
            prefix = "+" if letter in question.correct else "-"
            lines.append(f"{prefix} {choice_text}")
        lines.append("")
    lines.extend(["*)", ""])

    return lines


def run_command(command: list[str], *, cwd: Path) -> None:
    result = subprocess.run(
        command, cwd=cwd, text=True, capture_output=True, check=False
    )
    if result.returncode != 0:
        output = "\n".join(part for part in [result.stdout, result.stderr] if part)
        raise RuntimeError(f"Command failed: {' '.join(command)}\n{output}")


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


def generate_subject_pdf(
    txt_path: Path, pdf_path: Path, *, copies: int, work_dir: Path | None
) -> None:
    if copies < 1:
        raise ValueError("Copy count must be at least 1.")

    require_command("auto-multiple-choice")
    require_command("xelatex")

    pdf_path.parent.mkdir(parents=True, exist_ok=True)

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

        built_pdf = amc_dir / "amc-compiled.pdf"
        if not built_pdf.exists():
            raise RuntimeError(f"XeLaTeX did not create expected PDF: {built_pdf}")
        shutil.copy2(built_pdf, pdf_path)

    if work_dir is None:
        with tempfile.TemporaryDirectory(prefix="amc-build-") as temporary_dir:
            build_in(Path(temporary_dir))
    else:
        build_in(work_dir)


def convert(input_path: Path, output_path: Path, args: argparse.Namespace) -> None:
    if args.random_seed is not None and not 1 <= args.random_seed <= 4_194_303:
        raise ValueError("AMC random seeds must be between 1 and 4194303.")

    markdown = input_path.read_text(encoding="utf-8")
    open_lines, mcq_lines = split_sections(markdown)
    open_questions = parse_open_questions(open_lines)
    mcqs = parse_mcqs(mcq_lines)
    output = amc_lines(
        open_questions,
        mcqs,
        title=args.title,
        presentation=args.presentation,
        name_label=args.name_label,
        open_lines=args.open_lines,
        open_points=args.open_points,
        mcq_points=args.mcq_points,
        shuffle_questions=not args.no_shuffle_questions,
        random_seed=args.random_seed,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(output).rstrip() + "\n", encoding="utf-8")

    if args.subject_pdf is not None:
        generate_subject_pdf(
            output_path,
            args.subject_pdf,
            copies=args.copies,
            work_dir=args.amc_work_dir,
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
        default=(
            "September 16, 2026, 13:20-13:45. Duration: 25 minutes. "
            "Write your name in the box. "
            "For each MCQ, select all correct answers; the number of correct answers may vary. "
            "Use a black or blue pen. Mark selected boxes with a clear cross or tick. "
            "To cancel a marked box, fill it completely; do not redraw boxes."
        ),
        help="Presentation/instructions text shown below the title.",
    )
    parser.add_argument(
        "--name-label", default="Name", help="Label for the name field."
    )
    parser.add_argument(
        "--open-lines", type=int, default=5, help="Answer lines per open question."
    )
    parser.add_argument(
        "--open-points", type=int, default=2, help="Maximum points per open question."
    )
    parser.add_argument(
        "--mcq-points", type=int, default=2, help="Maximum points per MCQ."
    )
    parser.add_argument(
        "--subject-pdf",
        type=Path,
        help="Also generate one printable subject PDF containing all randomized copies.",
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
        "--no-shuffle-questions",
        action="store_true",
        help="Keep questions in source order instead of shuffling copies.",
    )
    parser.add_argument(
        "--random-seed",
        type=int,
        help="AMC random seed. Set this before printing and do not change it afterwards.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    convert(args.input, args.output, args)


if __name__ == "__main__":
    main()
