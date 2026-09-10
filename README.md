# bight-course

Static GitHub Pages website for the BiGHT course.

The source content lives in Markdown files under `content/`. The generated HTML is built into `docs/` by `build_site.py` and deployed by GitHub Actions.

## Edit course content

- Site/header metadata: `content/site/header.md`
- Home page: `content/pages/home.md`
- Shared snippets: `content/shared/`
- Weekly pages: `content/weeks/`
- Project documentation: `content/project-documentation/`

To add a PDF slide deck link to a released week page, set `slides_pdf` in that week's frontmatter. Use a local path such as `slides/week_01.pdf` for files stored in a top-level `slides/` directory, or use a full external URL.

Weekly pages are split into browsable sections from `##` headings. Project documentation pages are generated from `#` document titles and `##` section headings. Student project documentation is generated as one paginated page from the Markdown files in `content/project-documentation/student/`.

The build script also resolves:

- `{{ include: relative/path.md }}`
- `{{ weeks_table }}`

## Build locally

Create a virtual environment, then install build dependencies:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-build.txt
```

Build the static site:

```bash
python build_site.py
```

Weekly pages are published after each Wednesday lecture. The build releases each week's content at 14:40 Europe/Zurich while the site displays "Available after <lecture date>, 15:00". To preview the site at a specific release point, set `BIGHT_BUILD_TIME` to an ISO timestamp:

```bash
BIGHT_BUILD_TIME=2026-10-28T14:01:00+00:00 python build_site.py
```

Preview it locally:

```bash
python -m http.server 8000 -d docs
```

Open `http://localhost:8000`.

## Deploy

The `.github/workflows/pages.yml` workflow builds and deploys the site on pushes to `main`. A scheduled run fires every Wednesday at 14:40 Europe/Zurich to unlock the week before the 15:00 lecture (the site still displays 15:00). GitHub Actions `schedule` delivery can occasionally be delayed or skipped, so there is also an easy manual trigger.

### Deploy on demand

If the automatic release build was missed and a week is still locked on the site:

```bash
./scripts/redeploy.sh
```

The rebuild uses the current time, so as soon as a week's content is due (any time after the lecture's 14:40 release moment) it unlocks immediately. You can also trigger it from the GitHub UI: **Actions → Deploy static site to GitHub Pages → Run workflow**.

To preview the build as of a specific time instead, pass an ISO UTC timestamp:

```bash
./scripts/redeploy.sh 2026-10-28T13:59:00+00:00
```

To check whether a rebuild is currently needed:

```bash
python build_site.py --check-release-state
```

In GitHub, enable Pages for this repository with source set to `GitHub Actions`.

## Quality checks

Run the linter before opening a pull request:

```bash
ruff check build_site.py
ruff format --check build_site.py
python build_site.py --check-release-schedule
python build_site.py
```

## Pre-commit hooks

The repository uses [pre-commit](https://pre-commit.com) to run `isort` and `ruff` automatically before each commit. The configuration lives in `.pre-commit-config.yaml`.

Install the hooks once in your virtual environment:

```bash
python -m pip install pre-commit
pre-commit install
```

The hooks then run on your staged changes every time you commit and auto-fix issues where possible.

To run all hooks on the whole repository without committing:

```bash
pre-commit run --all-files
```

To skip the hooks for a single commit:

```bash
git commit --no-verify
```

## Licensing

Software in this repository, including source code, website infrastructure, configuration, and deployment tooling, is licensed separately from course content under the repository's Apache License 2.0 software license.

Third-party software vendored in this repository: [Mozilla PDF.js](https://mozilla.github.io/pdf.js/) (v3.11.174), hosted under `assets/pdfjs/` and used to render slide decks in the browser. PDF.js is licensed under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0); its license header is retained in the vendored files.

Original BiGHT course and teaching content is licensed under CC BY 4.0 except where otherwise stated. See `LICENSE-CONTENT.md` for the content license, exclusions for third-party material and trademarks, and suggested attribution.

Lecturers preparing public slides should use `SLIDE-LICENSING-NOTICES.md` before publishing decks or other teaching materials.
