# Milestone 1: Technical Design and Reproducible Repository

Deadline: Friday of Week 3, September 25, 21:59.

Weight: 12.5% of the project grade.

## Purpose

This milestone has two main goals:
- Prepare the technical design for your project, based on the problem statement;
- Prepare the repository skeleton according to your technical design.

We'll check whether your project is well-scoped, technically feasible, and evaluable, and whether your repository already has the right form for your technical design. We may give you feedback on things to change for the rest of the semester.

The main goal is to make your assumptions explicit and validated by the course team, before you invest heavily in implementation, and to establish a healthy and reproducible development process from the start. Staff feedback will focus on scope, feasibility, evaluation validity, team organization, and repository hygiene.

Your technical design should also address the five recurring project questions from the course overview: constraints, trust, evidence, scale, and uncertainty.

## Assigned Project

Your team is assigned one of the proposed course projects. Read the brief for your project on the Project Briefs overview page before writing the design.

Your technical design must be consistent with your assigned project brief.

It should:

- commit to one well-defined core use case from the brief rather than attempting all possible features;
- answer the brief's design questions in the relevant sections;
- target the brief's minimum convincing proof of concept;
- use the brief's evaluation ideas when defining your evaluation strategy.

## Submission

Submit inside your team repository.

Required design file:

```text
docs/milestone-1-technical-design-and-repository.md
```

The repository itself is also part of the submission. By the deadline, the repository should be in a reproducible state as described below and should contain an initial task breakdown, for example through GitHub issues or a project board.

## Required Design Content

Your technical design should include:

- an exact problem statement, broader than the project brief;
- intended users and usage context;
- core use cases and the one you will be focusing on during the semester;
- connection to the assigned project brief's proof-of-concept expectation;
- non-goals;
- proposed system architecture;
- initial idea of datasets, models, APIs, and external dependencies and justification of their selection (we know that you will likely find more resources later on in the project);
- evaluation strategy and success criteria;
- major risks and fallback plans;
- division of responsibilities (we recommend that you take the time to identify the strengths and weaknesses of each team member to split the work efficiently);
- provisional semester-level work plan.

All course projects are full-stack: dataset curation, ML tasks, evaluation, user interface. Ensure all of those aspects are covered in your Technical Design Document.

Regarding ML tasks, define provisional:

- prediction target or model objective;
- available data and data assumptions;
- train, validation, and test split strategy;
- baseline method;
- evaluation metric;
- expected failure modes;
- validity risks.

## Required Repository State

Your repository should include:

- documented environment installation with `uv`;
- pinned or locked dependencies;
- a clear source-code structure, folders and empty scripts that follow your Technical Design;
- a minimal executable pipeline (check the section below);
- automated formatting and linting with `ruff`;
- mandatory `pre-commit` configuration;
- a CI that runs formatting checks, linting, type checks with `pyright`, and tests;
- configuration separated from code;
- instructions for obtaining or generating a small sample of the data;
- data licensing and provenance documented in `data/DATASET_LICENSE.md` and `data/data-provenance.md` when data is used;
- no credentials committed to Git;
- no large files committed to Git (you may need to have some later, ask staff for approval);
- evidence of pull-request-based collaboration (even for those first few steps).

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

By the end of Week 3 there should already be evidence that the team is using this workflow.

## Recommended Structure

Check the provided `docs/milestone-1-technical-design-and-repository.md` in your repository, you can just populate it.

## Common Problems

Avoid:

- defining the project only as a list of features;
- attempting every feature in the project brief instead of committing to the core use case;
- proposing an architecture without an evaluation plan;
- assuming unavailable data will appear later;
- planning to build everything before testing anything;
- assigning all technical risk to the final weeks;
- describing users too vaguely;
- ignoring privacy, safety, or deployment constraints;
- code that only runs on one student's machine;
- missing `uv.lock` or unpinned dependencies;
- hard-coded absolute paths to resources in your personal folders;
- uncommitted local configuration required for execution;
- CI that is present but not actually checking the project;
- tests that do not run;
- pre-commit not installed or by only one team member;
- committing notebooks or outputs as the only working artifact.
