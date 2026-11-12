#!/usr/bin/env python3
"""Check that grading notes in a quiz plan stay off the printed questions and
are kept as AMC-TXT comments for graders.

Run: .venv/bin/python scripts/test_quiz_criteria.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import markdown_quiz_to_amc as converter  # noqa: E402

PLAN = """**1\\. Edge AI**

Explain **two** trade-offs.

*Expected keywords:* connectivity; *latency*
*Scoring:* 2 = two trade-offs; 1 = one; 0 = none.
*Slides:* week 3, slides 12-18

**2. No notes**

Explain something.

## MCQs

**1\\. Which are correct?**

A. Yes
B. No

**Correct answer(s):** A
"""


def main() -> None:
    open_lines, mcq_lines = converter.split_sections(PLAN)
    questions = converter.parse_open_questions(open_lines)
    assert questions[0].text == "Edge AI.\n\nExplain \\textbf{two} trade-offs."
    assert questions[0].criteria == (
        "Expected keywords: connectivity; latency",
        "Scoring: 2 = two trade-offs; 1 = one; 0 = none.",
    )
    assert questions[1].criteria == ()

    lines = converter.amc_lines(
        questions,
        converter.parse_mcqs(mcq_lines),
        title="T",
        presentation="P",
        open_lines=8,
        open_points=2,
        mcq_points=2,
        shuffle_questions=False,
        random_seed=1,
    )
    assert [line for line in lines if line.startswith(converter.CRITERIA_COMMENT)] == [
        "# criteria: Expected keywords: connectivity; latency",
        "# criteria: Scoring: 2 = two trade-offs; 1 = one; 0 = none.",
    ]
    assert not any("week 3" in line for line in lines)  # *Slides:* is dropped
    # Labeled format, with the stray Markdown a Google Docs export leaves behind.
    labeled = """Quizz 3 \\- 28.10.2026
## **Q1**. Edge AI \\[Easy\\] \\[Week 3\\]
**`Explain two trade-offs.`**
Hint: think latency.
**`Expected answer:`** `Latency and privacy.`
Slides: week 3
MCQ1. Which are correct? FROM LATER QUIZ 1 [Easy]
Select all correct answers.
 `A. Yes`
* B) No
Correct answer(s): A
Justification:
* A: True. Because.
"""
    assert converter.is_labeled_format(labeled)
    (question,), (mcq,) = converter.parse_labeled_quiz(labeled)
    assert (
        question.text == "Edge AI.\n\nExplain two trade-offs.\n\nHint: think latency."
    )
    assert question.criteria == ("Expected answer: Latency and privacy.",)
    assert mcq.text == "Which are correct?\n\nSelect all correct answers."
    assert mcq.choices == [("A", "Yes"), ("B", "No")] and mcq.correct == {"A"}
    assert converter.protect_option_like("Hint: x") == "\\textbf{Hint:} x"
    print("OK")


if __name__ == "__main__":
    main()
