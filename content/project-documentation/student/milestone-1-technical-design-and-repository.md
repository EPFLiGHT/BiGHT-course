# Milestone 1: Technical Design and Reproducible Repository

Deadline: Friday of Week 3, September 25, 21:59.

Weight: 10% of the course grade, equivalent to 12.5% of the project grade.

## Purpose

This milestone combines the technical design with the initial reproducible repository skeleton. It checks whether your project is well-scoped, technically feasible, and evaluable, and whether your repository can already be cloned, installed, checked, and run.

The main goal is to make your assumptions explicit before you invest heavily in implementation, and to establish a healthy and reproducible development process from the start. Staff feedback will focus on scope, feasibility, evaluation validity, team organization, and repository hygiene.

Your technical design should also address the five recurring project questions from the course overview: constraints, trust, evidence, scale, and uncertainty.

## Assigned Project

Your team is assigned one of the proposed course projects. Read the brief for your project on the Project Briefs overview page before writing the design.

Your technical design must be consistent with your assigned project brief.

It should:

- commit to a small core use case from the brief rather than attempting all possible features;
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

- exact problem statement;
- intended users and usage context;
- core use cases;
- connection to the assigned project brief's proof-of-concept expectation;
- non-goals;
- proposed system architecture;
- datasets, models, APIs, and external dependencies;
- evaluation strategy and success criteria;
- major risks and fallback plans;
- division of responsibilities;
- semester-level work plan (identify the strengths and weaknesses of each team member to split the work).

## Additional Requirements For ML Projects

All six course projects involve prediction, classification, ranking, generation, retrieval, or risk scoring. Include:

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
- a clear source-code structure;
- a minimal executable pipeline;
- one or two representative unit tests;
- automated formatting and linting with `ruff`;
- type checking with `pyright`;
- mandatory `pre-commit` configuration;
- CI that runs formatting checks, linting, type checks, and tests;
- configuration separated from code;
- instructions for obtaining or generating a small sample of the data;
- data licensing and provenance documented in `data/DATASET_LICENSE.md` and `data/data-provenance.md` when data is used;
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

By the end of Week 3 there should already be evidence that the team is using the agreed workflow.

## Recommended Structure

```markdown
# Milestone 1: Technical Design and Reproducible Repository

## Team

## Problem Statement

## Intended Users And Context

## Core Use Cases

## Non-Goals

## System Architecture

## Data, Models, APIs, And Dependencies

## Evaluation Strategy

## Risks And Fallback Plans

## Team Responsibilities

## Work Plan

```

## Rubric

| Criterion | Weight |
|---|---:|
| Problem framing and user/context understanding | 10% |
| System architecture and technical feasibility | 15% |
| Data, model, and dependency plan | 10% |
| Evaluation strategy and success criteria | 15% |
| Risks, fallback plans, and non-goals | 5% |
| Reproducible setup, CI, and code quality checks | 15% |
| Repository structure, minimal executable pipeline, and tests | 15% |
| Team organization and PR-based collaboration | 15% |

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
- hard-coded absolute paths;
- uncommitted local configuration required for execution;
- CI that is present but not actually checking the project;
- tests that do not run;
- pre-commit installed by only one team member;
- committing notebooks or outputs as the only working artifact.
