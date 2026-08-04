# Project Release Checklist

Use this checklist before releasing project repositories and documentation to students.

## Before Week 1

Confirm:

- project descriptions are final enough to release;
- team sizes are known;
- the course GitHub organization exists;
- staff GitHub accounts have admin access;
- the template repository passes CI;
- branch protection settings are tested;
- student documentation is ready;
- staff grading rubrics are approved;
- staff grading rubrics match the assessment table in the course overview;
- deadline time is decided or marked provisional;
- staff have agreed how to identify and record the repository state at each milestone deadline;
- the Week 1 informal deadline vote is prepared.

## Repository Template

Verify the template includes:

- `README.md`;
- `pyproject.toml`;
- `uv.lock`;
- `.pre-commit-config.yaml`;
- `.github/workflows/ci.yml`;
- `src/` package placeholder;
- `tests/` with at least one passing smoke test;
- `docs/` with placeholders for `milestone-1-technical-design.md`, `milestone-3-proof-of-concept.md`, `final-report-placeholder.md`, and individual reports;
- no `docs/milestone-2-reproducible-skeleton.md` placeholder, since Milestone 2 is graded from the repository state;
- `data/README.md`;
- `.gitignore` excluding `.env`, `.venv`, outputs, caches, and large local data.

## Required Commands

Verify these commands pass in the template:

```bash
uv sync
uv run pre-commit run --all-files
uv run ruff format --check .
uv run ruff check .
uv run pyright
uv run pytest
```

## Repository Creation

For each team:

- create repository from template;
- set repository visibility;
- rename package placeholder if needed;
- add team members with write access;
- add staff with admin access;
- enable branch protection on `main`;
- verify required CI checks are selected;
- verify students cannot bypass protection;
- create initial issues or labels if desired.

## Documentation Release

Release or link:

- `student/project-overview.md`;
- `student/project-setup.md`;
- `student/pull-requests-and-reviews.md`;
- written milestone instructions for Milestone 1 and Milestone 3;
- final submission instructions, including one individual contribution report per student;
- `student/rubrics.md`;
- project-specific brief;
- report template.

## Week 1 Lecture Items

Cover:

- project goals and philosophy;
- available projects;
- group formation process;
- GitHub organization workflow;
- protected `main` and PR requirement;
- deadline schedule;
- assessment split from the course overview;
- informal Friday versus Sunday deadline vote;
- rationale for 21:59 deadlines;
- Week 10 checkpoint format as a non-graded 30-minute conversation;
- where students should ask for help.

## After Group Assignment

After groups are finalized:

- assign teams to repositories;
- verify all students can clone their repository;
- verify each team has installed `uv`;
- verify students understand the first milestone;
- remind students to install pre-commit;
- remind students that milestone submissions happen inside the repository only;
- remind staff that Milestone 2 should be graded from the repository state at the deadline, not from a separate report.
