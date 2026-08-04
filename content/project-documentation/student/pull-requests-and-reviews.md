# Pull Requests And Reviews

Use pull requests for all the project work. This is part of the project requirements, as a good habit that you will need in professional settings.

This will make your work easier to review, easier to reproduce, and less likely to break your teammates' work.

## Basic Workflow

Create a branch.

```bash
git switch -c feature/my-change
```

Make your changes and run checks.

```bash
uv run ruff format .
uv run ruff check .
uv run pyright
uv run pytest
```

Commit and push.

```bash
git add .
git commit -m "Add baseline data loader"
git push -u origin feature/my-change
```

Open a pull request on GitHub.

Request review from at least one teammate.

Merge only after CI passes and the required review is complete.

## Good Pull Requests

A good pull request should:

- solve one clear problem;
- have a descriptive title;
- explain what changed and why;
- link to the relevant issue or milestone task when possible;
- include tests or explain why tests are not applicable;
- include screenshots, logs, or demo notes when user-facing behavior changes;
- avoid unrelated formatting or refactoring;
- avoid committing generated files unless they are part of the required output;
- pass CI before review;
- be small enough for a teammate to review seriously.

Good PR title examples:

- `Add baseline temporal split for risk model`
- `Implement trusted-source retrieval for messenger prototype`
- `Add CI workflow for ruff, pyright, and pytest`
- `Document data download for Freetown geospatial layers`

Weak PR title examples:

- `updates`
- `fix stuff`
- `final version`
- `code`

## Pull Request Description Template

Use a short, useful description.

```markdown
## What changed

Describe the change in 2-5 bullets.

## Why

Explain the reason for the change.

## How to test

List the commands or manual steps used to check the change.

## Notes for reviewer

Mention risks, shortcuts, known limitations, or questions.
```

## Good Reviews

A good review should check correctness, reproducibility, and clarity.

Reviewers should ask:

- Does this change do what it claims?
- Can I understand the code or documentation?
- Does it introduce hard-coded paths or hidden assumptions?
- Does it handle errors clearly?
- Does it keep configuration separate from code?
- Does it avoid committing secrets, large data, or generated artifacts?
- Does it include tests or a reasonable explanation for missing tests?
- Does it preserve the ability to run the project from a fresh clone?

## Review Comment Style

Use clear labels when possible.

Examples:

- `Blocking: This will fail on a fresh clone because the path is absolute.`
- `Question: Should this threshold be configurable?`
- `Suggestion: This function name could be more specific.`
- `Nitpick: Typo in the README.`

Approving a PR means you believe the change is understandable, appropriate, and safe to merge. Do not approve a PR you have not read.

## What Not To Do

Avoid:

- giant PRs that combine many unrelated changes;
- direct pushes to `main`;
- approving PRs only because CI is green;
- merging broken tests because the deadline is close;
- committing credentials or private data;
- using PRs only at the end of the project after all work is already done.

## Evidence Of Collaboration

The teaching team may inspect your repository history.

Healthy collaboration usually includes:

- issues or tasks assigned to team members;
- multiple contributors making meaningful commits;
- pull requests opened throughout the project;
- reviews by teammates;
- discussions about design, tests, and trade-offs;
- no single student doing almost all technical work without explanation.
