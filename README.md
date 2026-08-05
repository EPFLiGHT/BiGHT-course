# bight-course

Static GitHub Pages website for the BiGHT course.

The source content lives in Markdown files under `content/`. The generated HTML is built into `docs/` by `build_site.py` and deployed by GitHub Actions.

## Edit course content

- Site/header metadata: `content/site/header.md`
- Home page: `content/pages/home.md`
- Shared snippets: `content/shared/`
- Weekly pages: `content/weeks/`
- Project documentation: `content/project-documentation/`

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

Preview it locally:

```bash
python -m http.server 8000 -d docs
```

Open `http://localhost:8000`.

## Deploy

The `.github/workflows/pages.yml` workflow builds and deploys the site on pushes to `main`.

In GitHub, enable Pages for this repository with source set to `GitHub Actions`.

## Quality checks

Run the linter before opening a pull request:

```bash
ruff check build_site.py
ruff format --check build_site.py
python build_site.py
```

## Licensing

Software in this repository, including source code, website infrastructure, configuration, and deployment tooling, is licensed separately from course content under the repository's Apache License 2.0 software license.

Original BiGHT course and teaching content is licensed under CC BY 4.0 except where otherwise stated. See `LICENSE-CONTENT.md` for the content license, exclusions for third-party material and trademarks, and suggested attribution.

Lecturers preparing public slides should use `SLIDE-LICENSING-NOTICES.md` before publishing decks or other teaching materials.
