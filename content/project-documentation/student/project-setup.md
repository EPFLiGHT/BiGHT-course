# Project Setup Guide

This guide explains how your project repository should be set up and maintained.

Staff will create your repository in the course GitHub organization.

## Repository Access

Each team receives one repository.

The `main` branch is protected. Do not push directly to `main`. All changes should go through pull requests.

Recommended branch names:

- `feature/add-data-loader`
- `feature/baseline-model`
- `fix/ci-type-check`
- `docs/update-design`
- `experiment/geospatial-query-demo`

## Local Setup With uv

Clone your repository.

```bash
git clone <your-team-repository-url>
cd <your-team-repository>
```

Create the virtual environment and synchronize dependencies.

```bash
uv venv
uv sync
```

Activate the virtual environment if needed.

```bash
source .venv/bin/activate
```

Install pre-commit hooks.

```bash
uv run pre-commit install
```

Run the quality checks locally.

```bash
uv run ruff format --check .
uv run ruff check .
uv run pyright
uv run pytest
```

If formatting fails, format the code.

```bash
uv run ruff format .
```

## Required Repository Structure

Your exact structure may differ by project, but it should be clear and consistent.

Recommended structure:

```text
.
|-- README.md
|-- pyproject.toml
|-- uv.lock
|-- .pre-commit-config.yaml
|-- .github/
|   `-- workflows/
|       `-- ci.yml
|-- docs/
|   |-- milestone-1-technical-design-and-repository.md
|   |-- milestone-2-proof-of-concept.md
|   |-- final-report.pdf
|   `-- contribution-statement.md
|-- src/
|   `-- <project_package>/
|-- tests/
|-- configs/
|-- scripts/
|-- data/
|   |-- README.md
|   |-- DATASET_LICENSE.md
|   `-- data-provenance.md
`-- outputs/
    `-- README.md
```

The root README should explain how to obtain or generate any data needed to run the project. Do not commit large datasets unless staff explicitly approves it.

## Python Project Requirements

Your repository must include a `pyproject.toml`.

The project must be installable and runnable from a fresh clone using documented commands. A staff member should be able to clone the repository, run `uv venv` and `uv sync`, and execute your minimal pipeline or demo instructions.

Dependencies should be pinned or locked. Commit `uv.lock` unless staff gives different instructions.

## CI Requirements

Your repository must include continuous integration that runs on pull requests and pushes to `main`.

CI must run at least:

- formatting check with `ruff`;
- linting with `ruff`;
- type checking with `pyright`;
- tests.

This will ensure every change can be checked automatically.

## Pre-Commit Requirements

All teams must use pre-commit.

Pre-commit should run the same basic checks that developers should not skip locally, such as formatting, linting, and simple file hygiene checks.

Install pre-commit before your first contribution.

```bash
uv run pre-commit install
```

Run all hooks manually when needed.

```bash
uv run pre-commit run --all-files
```

## Data And Secrets

Do not commit:

- API keys;
- passwords;
- private credentials;
- personal data;
- protected health information;
- large datasets;
- generated model checkpoints unless staff approves them.

If your project needs a secret, document the required environment variable and provide a placeholder example.

Use `.env.example` for examples. Do not commit `.env`.

If your project needs data, include a `data/README.md` explaining:

- what data is needed;
- where it comes from;
- whether it is public or restricted;
- how to download or generate a small sample;
- what should not be committed.

Also document dataset licensing and provenance:

- `data/DATASET_LICENSE.md` should describe usage rights, redistribution terms, attribution requirements, and anonymization or de-identification status;
- `data/data-provenance.md` should describe where each dataset came from, when it was obtained, how it was processed, and known limitations or biases.

## Configuration

Separate configuration from code.

Examples of configuration:

- model name;
- dataset path;
- language pair;
- geospatial region;
- threshold;
- prompt template path;
- output directory.

Configuration can be stored in `configs/`, environment variables, or command-line arguments. Avoid hard-coded absolute paths such as `/home/<name>/...`.

## README Requirements

Your `README.md` should include:

- project title;
- short description;
- team members and their contact information;
- setup instructions;
- how to run tests and checks;
- how to run the current pipeline or demo;
- data instructions;
- current limitations.

Keep the README current. A stale README is a reproducibility problem.
