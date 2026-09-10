# Repository Instructions For Agents

## Pull Requests And Deployments

- Do not merge pull requests unless the user explicitly asks.
- Do not trigger, watch, or otherwise run deployments unless the user explicitly asks.
- If the user asks for a PR, open it and return the URL; leave the merge to the user unless instructed otherwise.

## Student-Facing Change Tracking

Every repository change must be classified before commit or PR:

- **Student-facing:** affects content, behavior, navigation, deadlines, release timing, rendered pages, slides, or any documentation visible on the deployed course site.
- **Internal-only:** affects tooling, comments, tests, CI, or repository maintenance without changing what students see.

For every student-facing change:

- Update `content/pages/changelog.md` with a concise, reverse-chronological entry.
- Add or update `last_edited: "YYYY-MM-DD"` and `change_note: "Short description."` in the front matter of each changed student-facing Markdown file.
- Keep local notices short and factual. Important changes may still require a separate course announcement from staff.

For internal-only changes:

- State clearly in the PR description that the change is internal-only and does not affect the deployed student site.

Use `.github/pull_request_template.md` as the PR checklist.
