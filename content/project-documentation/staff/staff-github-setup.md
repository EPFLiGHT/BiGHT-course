# Staff GitHub Setup Guide

This guide describes the recommended GitHub organization and repository setup for the course projects.

## Goals

The setup should ensure that every team starts with:

- one repository inside the course GitHub organization;
- a protected `main` branch;
- required pull requests;
- required CI checks;
- a common Python baseline using `uv`, `ruff`, `pyright`, `pytest`, and `pre-commit`;
- a place to submit written milestone documents, the final report, and individual contribution reports.

## Organization Setup

Create one GitHub organization for the course.

Recommended organization settings:

- disable repository creation by students unless needed;
- require two-factor authentication if feasible;
- create teams for staff and student groups;
- give staff admin access;
- give each student team write access only to its own repository;
- keep visibility private unless the course explicitly wants public repositories.

## Repository Naming

Use predictable names.

Examples:

- `team-01-offline-translator`
- `team-02-public-health-messenger`
- `team-03-geospatial-intelligence`
- `team-04-zoonotic-risk-prediction`
- `team-05-rwanda-medical-assistant`

Avoid names that reveal sensitive student information.

## Template Repository

Staff should prepare a template repository before Week 1.

Recommended template structure:

```text
.
|-- README.md
|-- pyproject.toml
|-- uv.lock
|-- .pre-commit-config.yaml
|-- .gitignore
|-- .github/
|   `-- workflows/
|       `-- ci.yml
|-- docs/
|   |-- milestone-1-technical-design.md
|   |-- milestone-3-proof-of-concept.md
|   |-- final-report-placeholder.md
|   `-- individual-reports/
|       `-- student-name.md
|-- src/
|   `-- project_package/
|       `-- __init__.py
|-- tests/
|   `-- test_smoke.py
|-- configs/
|   `-- example.yaml
|-- scripts/
|   `-- run_smoke_pipeline.py
|-- data/
|   `-- README.md
`-- outputs/
    `-- README.md
```

The template should pass CI before it is used to create team repositories.

## Baseline Tooling

The template should support these commands:

```bash
uv sync
uv run pre-commit run --all-files
uv run ruff format --check .
uv run ruff check .
uv run pyright
uv run pytest
```

Suggested development dependencies:

- `pytest`;
- `ruff`;
- `pyright`;
- `pre-commit`.

## Branch Protection

Protect `main` on each repository.

Recommended branch protection rules:

- require pull request before merging;
- require at least one approving review;
- require status checks to pass before merging;
- require branches to be up to date before merging if practical;
- prevent force pushes;
- prevent deletion of `main`;
- include administrators only if staff wants to enforce the same rules on itself.

Required checks should include:

- formatting check;
- linting;
- type checking;
- tests.

## Student Permissions

Recommended access model:

- students have write access to their own team repository;
- students do not have admin access;
- students can create branches and pull requests;
- students cannot bypass branch protection;
- staff can merge or unblock if necessary.

## Milestone And Final Submission Locations

Ask students to submit written milestone and final documents in `docs/`. Milestone 2 is a repository-state checkpoint and does not require a separate milestone document.

For grading, staff should evaluate the repository state as it existed at the milestone deadline. Record the commit SHA, pull request, or release tag used for grading so later commits do not accidentally change the assessed submission.

Recommended paths:

- `docs/milestone-1-technical-design.md`;
- `docs/milestone-3-proof-of-concept.md`;
- `docs/final-report.pdf`;
- `docs/individual-reports/<student-name>.md` for each student.

Do not ask teams to create `docs/milestone-2-reproducible-skeleton.md`; staff should grade Milestone 2 from the repository state, README, CI, tests, and runnable minimal pipeline.

Presentation materials can be stored in `docs/presentations/` or `slides/`.

## Staff Checks Before Releasing Repositories

Before releasing repositories to teams, verify:

- the repository can be cloned;
- `uv sync` succeeds;
- pre-commit runs;
- CI passes;
- branch protection is active;
- each team has correct access;
- the README contains course-specific setup instructions;
- no secrets are present;
- placeholder package names do not conflict across repositories if copied.
