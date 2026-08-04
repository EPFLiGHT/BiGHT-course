# Milestone 2: Reproducible Project Skeleton

Deadline: Friday of Week 5, October 9, 21:59.

Weight: 5% of the course grade.

## Purpose

This milestone checks whether your repository can actually be cloned, installed, checked, and run.

The goal is to show that your team has a healthy and reproducible development process.

## Submission

Submit inside your team repository.

No separate milestone report is required for this checkpoint. The repository itself is the submission.

Your README should explain how to install the project, run the checks, and run the minimal pipeline. Staff will grade the repository state, README instructions, CI results, tests, and collaboration history rather than a separate narrative document.

## Required Repository State

Your repository should include:

- documented environment installation with `uv`;
- pinned or locked dependencies;
- a clear source-code structure;
- a minimal executable pipeline;
- one or two representative unit tests;
- automated formatting and linting with `ruff`;
- type checking with `pyright`;
- mandatory `pre-commit` configuration;
- CI that runs formatting checks, linting, type checks, and tests;
- configuration separated from code;
- instructions for obtaining or generating a small sample of the data;
- no credentials committed to Git;
- no large files committed to Git unless staff approved them;
- evidence of pull-request-based collaboration.

## Minimal Executable Pipeline

Your pipeline can be deliberately simple, but it must run.

Example structure:

```text
load sample data -> run dummy model or simple operation -> save or display output
```

This can use fake, small, or public sample data. The point is that reproducibility can be tested now, before the project becomes complex.

## Required Commands

Your README should document commands equivalent to:

```bash
uv sync
uv run pre-commit run --all-files
uv run ruff format --check .
uv run ruff check .
uv run pyright
uv run pytest
```

Your README should also explain how to run the minimal pipeline.

## Collaboration Evidence

The teaching team may inspect:

- branches;
- pull requests;
- review comments;
- issue assignments;
- commit history;
- CI results.

At this point in the semester, there should already be evidence that the team is using the agreed workflow.

## Rubric

| Criterion | Weight |
|---|---:|
| Reproducible installation and execution | 20% |
| Repository structure and Python project organization | 15% |
| CI, pre-commit, linting, formatting, and type checks | 20% |
| Minimal executable pipeline | 15% |
| Tests and basic quality checks | 10% |
| Data/configuration handling and secret hygiene | 10% |
| PR workflow and team contribution evidence | 10% |

## Common Problems

Avoid:

- code that only runs on one student's machine;
- missing `uv.lock` or unpinned dependencies;
- hard-coded absolute paths;
- uncommitted local configuration required for execution;
- CI that is present but not actually checking the project;
- tests that do not run;
- pre-commit installed by only one team member;
- committing notebooks or outputs as the only working artifact.
