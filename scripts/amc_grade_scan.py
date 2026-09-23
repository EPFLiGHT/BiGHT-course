#!/usr/bin/env python3
"""Grade a scanned AMC batch from a generated AMC-TXT source.

The intended workflow is:

1. Generate and print the same AMC-TXT source with ``markdown_quiz_to_amc.py``.
2. Grade open questions on paper by ticking the printed 0/1/2 boxes.
3. Scan all completed pages into one PDF.
4. Run this script to produce annotated PDFs and a CSV export.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
from pathlib import Path

ONECOPY_RE = re.compile(r"\\onecopy\{\d+\}")
OPEN_QUESTION_RE = re.compile(r"^\*<[^>]*>.*")
QUESTION_RE = re.compile(r"^\*\*.*")
CHOICE_RE = re.compile(r"^[+-](?:\[[^\]]*\])?(?:\{([^}]*)\})?")
SCORING_RE = re.compile(r"\{([^}]*)\}")
SCORING_VALUE_RE = re.compile(r"(?:^|,)\s*b\s*=\s*([+-]?(?:\d+(?:\.\d*)?|\.\d+))")


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


def question_b_score(line: str) -> float | None:
    match = SCORING_RE.search(line)
    if not match:
        return None
    scoring_match = SCORING_VALUE_RE.search(match.group(1))
    if not scoring_match:
        return None
    return parse_float(scoring_match.group(1))


def computed_raw_total(amc_txt_path: Path) -> float | None:
    """Estimate the perfect raw score from the generated AMC-TXT file.

    This matches the format emitted by ``markdown_quiz_to_amc.py``: open
    questions use braced per-box scores, and MCQs use a per-choice ``b`` value.
    """

    total = 0.0
    saw_question = False
    current = ""
    open_scores: list[float] = []
    mcq_b: float | None = None
    mcq_choices = 0

    def flush() -> None:
        nonlocal total, current, open_scores, mcq_b, mcq_choices, saw_question
        if current == "open" and open_scores:
            total += max(open_scores)
            saw_question = True
        elif current == "mcq" and mcq_b is not None and mcq_choices:
            total += mcq_b * mcq_choices
            saw_question = True
        current = ""
        open_scores = []
        mcq_b = None
        mcq_choices = 0

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
            mcq_b = question_b_score(line)
            continue
        if current == "open":
            score = braced_score(line)
            if score is not None:
                open_scores.append(score)
        elif current == "mcq" and line.startswith(("+", "-")):
            mcq_choices += 1

    flush()
    return total if saw_question else None


def make_scan_list(scan_pdf: Path, project_dir: Path) -> Path:
    scan_list = project_dir / "scan-list.txt"
    scan_list.write_text(str(scan_pdf.resolve()) + "\n", encoding="utf-8")
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


def build_project_source(amc_txt: Path, project_dir: Path, copies: int) -> Path:
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
    patch_copy_count(filtered_tex, copies)
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
        help="Single PDF containing all scanned completed pages.",
    )
    parser.add_argument(
        "--out",
        required=True,
        type=Path,
        help="Output/project directory to create or reuse.",
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
        "--verdict", default="SCORE: %s/%m", help="Header text for annotated PDFs."
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
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.copies < 1:
        raise ValueError("--copies must be at least 1.")
    if not args.txt.exists():
        raise FileNotFoundError(args.txt)
    if not args.scans.exists() and not args.prepare_only:
        raise FileNotFoundError(args.scans)
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
    source_tex = build_project_source(args.txt.resolve(), project_dir, args.copies)
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

    print(f"Annotated PDFs: {project_dir / 'cr/corrections/pdf'}")
    print(f"Grades CSV: {project_dir / 'exports' / args.csv_name}")


if __name__ == "__main__":
    main()
