# Course Project Overview

The course project is a semester-long team project in which you will design, build, evaluate, and document an AI system for global health or humanitarian response.

The goal is not only to train a model or build an interface. We want to make you build a credible prototype of an AI system that could support decision making, communication, translation, risk analysis, or clinical work in a constrained and high-stakes setting.

## Project Philosophy

Your project will be evaluated through five recurring questions.

| Question | What It Means For Your Project |
|---|---|
| Constraints | What makes this setting technically, socially, clinically, or operationally difficult? |
| Trust | Why should a user trust this system? |
| Evidence | How do we know the system works? |
| Scale | What changes if the system reaches many people, responders, or health workers? |
| Uncertainty | What does the system not know, and how does it communicate uncertainty or limitations? |

These questions should appear in your technical design, your proof of concept, and your final report.

## Project Timeline

Deadlines are set at 21:59. Students will choose on the first lecture whether to have deadlines on Fridays or Sundays.

| Date | Moment | Deliverable |
|---:|---|---|
| September 7 | Week 1 | Project descriptions and scopes released |
| September 20, 21:59 | Sunday of Week 2 | Group assignment finalized |
| September 25, 21:59 | Friday of Week 3 | Technical design and reproducible repository skeleton |
| November 6, 21:59 | Friday of Week 8 | Proof of concept technical checkpoint and midterm oral presentation |
| November 23-27 | Week 10 | 30-minute team checkpoint |
| December 18, 21:59 | Friday of Week 14 | Final submission |

## Assessment

The table below mirrors the assessment structure in the course overview.

| Component | Weight | Project Documentation Mapping |
|---|---:|---|
| Project report and code, with final presentation with a live demo | 40% | Final submission |
| Initial submission: conception and reproducible base code | 10% | Technical design and reproducible repository skeleton |
| Midterm checkpoint: technical project design | 20% | Proof of concept technical checkpoint |
| Midterm oral presentation with live demo | 10% | Week 8 oral presentation and live demo |
| In-class tests and quizzes, including ethics certification | 20% | Assessed outside the team repository |

## Repository-Based Submission

All project submissions happen inside your team GitHub repository.

Staff will create one repository per team in the course GitHub organization. The `main` branch will be protected. You will have to work through branches, pull requests, and peer review.

Your repository is both your software artifact and your submission record. Reports, milestone documents, presentation material, and final documentation should be committed to the repository.

## Required Technical Stack

All teams use the same baseline engineering stack.

| Area | Requirement |
|---|---|
| Language | Python |
| Environment | `uv` virtual environments |
| Package configuration | `pyproject.toml` |
| Formatting and linting | `ruff` |
| Type checking | `pyright` |
| Tests | `pytest` or an equivalent Python test runner approved by staff |
| Pre-commit hooks | Required |
| Continuous integration | Required for tests, linting, and type checks |
| Repository workflow | Pull requests into protected `main` |

## Expected Final Output

By the end of the course, each team should submit:

- a working prototype;
- a reproducible code repository;
- tests, linting, type checks, pre-commit hooks, and CI;
- a final report submitted as a PDF inside the repository;
- a live demo during the final class presentation;
- final presentation material;
- an individual contribution report for each team member;
- handover or maintenance documentation.

## What Counts As Success

A successful project does not need to solve the full real-world problem. It should instead make a well-scoped, technically credible, and well-evaluated contribution.

Strong projects usually have:

- a clear user and use case;
- a working vertical slice through the system;
- a realistic evaluation strategy;
- honest limitations and failure analysis;
- readable and reproducible code;
- evidence of collaboration through issues, pull requests, and reviews;
- a final demo that shows the system working, not just slides describing it.
