from __future__ import annotations

import os
import re
import shutil
import sys
from collections import OrderedDict
from datetime import date, datetime, time
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

try:
    from jinja2 import Environment, FileSystemLoader, select_autoescape
    from markdown_it import MarkdownIt
except ModuleNotFoundError as exc:
    missing_module = exc.name or "required build dependency"
    raise SystemExit(
        f"Missing Python module: {missing_module}\n"
        "Install the static-site build dependencies first:\n\n"
        "    python -m pip install -r requirements-build.txt\n\n"
        "Then rebuild with:\n\n"
        "    python build_site.py"
    ) from exc

ROOT = Path(__file__).parent.resolve()
CONTENT_DIR = ROOT / "content"
WEEKS_DIR = CONTENT_DIR / "weeks"
PROJECT_DOCS_DIR = CONTENT_DIR / "project-documentation"
TEMPLATES_DIR = ROOT / "templates"
SOURCE_ASSETS_DIR = ROOT / "assets"
BUILD_DIR = ROOT / "docs"
BUILD_TIME_ENV = "BIGHT_BUILD_TIME"
RELEASE_ZONE = ZoneInfo("Europe/Zurich")
RELEASE_TIME = time(15, 0)

MARKDOWN = MarkdownIt("commonmark", {"html": True}).enable(["table", "strikethrough"])

STUDENT_DOCUMENTATION_ORDER = [
    "student/project-overview.md",
    "student/project-setup.md",
    "student/pull-requests-and-reviews.md",
    "student/milestone-1-technical-design.md",
    "student/milestone-2-reproducible-skeleton.md",
    "student/milestone-3-proof-of-concept.md",
    "student/week-10-checkpoint.md",
    "student/final-submission.md",
    "student/rubrics.md",
    "student/report-template.md",
]

PROJECT_BRIEF_ORDER = [
    "projects/project-1-offline-translator.md",
    "projects/project-2-public-health-messenger.md",
    "projects/project-3-geospatial-intelligence.md",
    "projects/project-4-zoonotic-risk-prediction.md",
    "projects/project-5-rwanda-medical-assistant.md",
]

PROJECT_DOCUMENTATION_ORDER = [
    ("README.md", "Project Documentation"),
]


def parse_value(value: str) -> str | int:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    if value.isdigit():
        return int(value)
    return value


def parse_front_matter(text: str) -> tuple[dict[str, str | int], str]:
    if not text.startswith("---\n"):
        return {}, text

    end_marker = "\n---\n"
    end = text.find(end_marker, 4)
    if end == -1:
        return {}, text

    raw_metadata = text[4:end]
    body = text[end + len(end_marker) :]
    metadata: dict[str, str | int] = {}

    for line in raw_metadata.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        metadata[key.strip()] = parse_value(value)

    return metadata, body


def load_markdown_page(path: str | Path) -> tuple[dict[str, str | int], str, Path]:
    page_path = ROOT / path if isinstance(path, str) else path
    text = page_path.read_text(encoding="utf-8")
    metadata, body = parse_front_matter(text)
    return metadata, body, page_path


def load_metadata(path: str | Path) -> dict[str, str | int]:
    metadata, _, _ = load_markdown_page(path)
    return metadata


def week_slug(week: dict[str, Any]) -> str:
    return f"week-{int(week['week']):02d}"


def load_week_metadata() -> list[dict[str, Any]]:
    weeks: list[dict[str, Any]] = []
    for path in WEEKS_DIR.glob("*.md"):
        metadata = dict(load_metadata(path))
        metadata["content_path"] = path.relative_to(ROOT).as_posix()
        metadata["slug"] = week_slug(metadata)
        metadata["output_path"] = BUILD_DIR / "weeks" / metadata["slug"] / "index.html"
        weeks.append(metadata)
    return sorted(weeks, key=lambda item: int(item.get("order", item.get("week", 0))))


def parse_build_time(raw_value: str | None) -> datetime:
    if raw_value:
        normalized_value = raw_value.strip().replace("Z", "+00:00")
        build_time = datetime.fromisoformat(normalized_value)
        if build_time.tzinfo is None:
            build_time = build_time.replace(tzinfo=RELEASE_ZONE)
        return build_time.astimezone(RELEASE_ZONE)
    return datetime.now(RELEASE_ZONE)


def current_build_time() -> datetime:
    return parse_build_time(os.environ.get(BUILD_TIME_ENV))


def week_release_datetime(week: dict[str, Any]) -> datetime:
    raw_lecture_date = week.get("lecture_date")
    if not raw_lecture_date:
        msg = f"Missing lecture_date for week {week.get('week', 'unknown')}"
        raise ValueError(msg)
    lecture_date = date.fromisoformat(str(raw_lecture_date))
    return datetime.combine(lecture_date, RELEASE_TIME, tzinfo=RELEASE_ZONE)


def format_release_label(release_at: datetime) -> str:
    return f"Available after {release_at:%b} {release_at.day}, 15:00 Europe/Zurich"


def annotate_week_releases(
    weeks: list[dict[str, Any]], build_time: datetime
) -> list[dict[str, Any]]:
    annotated_weeks = []
    for week in weeks:
        release_at = week_release_datetime(week)
        is_released = build_time >= release_at
        annotated_weeks.append(
            {
                **week,
                "is_released": is_released,
                "release_at": release_at,
                "release_label": format_release_label(release_at),
            }
        )
    return annotated_weeks


def extract_h1(body: str, fallback: str) -> tuple[str, str]:
    lines = body.splitlines()
    for index, line in enumerate(lines):
        if not line.strip():
            continue
        if line.startswith("# "):
            title = line[2:].strip()
            remaining = "\n".join(lines[:index] + lines[index + 1 :]).strip()
            return title, remaining
        break
    return fallback, body


def documentation_slug(relative_path: str) -> str:
    if relative_path == "README.md":
        return "index"
    return relative_path.removesuffix(".md")


def slug_from_path(relative_path: str) -> str:
    return Path(relative_path).stem


def load_project_documentation_metadata() -> list[dict[str, Any]]:
    documents: list[dict[str, Any]] = []
    for order, (relative_path, sidebar_group) in enumerate(
        PROJECT_DOCUMENTATION_ORDER, start=1
    ):
        content_path = PROJECT_DOCS_DIR / relative_path
        _, body, _ = load_markdown_page(content_path)
        fallback_title = content_path.stem.replace("-", " ").title()
        title, _ = extract_h1(body, fallback_title)
        slug = documentation_slug(relative_path)
        output_path = (
            BUILD_DIR / "project-documentation" / "index.html"
            if slug == "index"
            else BUILD_DIR / "project-documentation" / slug / "index.html"
        )
        documents.append(
            {
                "page_id": f"project-docs:{relative_path}",
                "page_title": title,
                "nav_title": title,
                "page_heading": title,
                "sidebar_group": sidebar_group,
                "content_path": content_path.relative_to(ROOT).as_posix(),
                "output_path": output_path,
                "order": order if relative_path == "README.md" else order + 1,
            }
        )
        if relative_path == "README.md":
            documents.append(
                {
                    "page_id": "project-docs:student",
                    "page_title": "Student Project Guide",
                    "nav_title": "Student Project Guide",
                    "page_heading": "Student Project Guide",
                    "sidebar_group": "Student Project Guide",
                    "output_path": BUILD_DIR
                    / "project-documentation"
                    / "student"
                    / "index.html",
                    "order": 2,
                    "tabbed_documents": build_student_tabs(),
                }
            )
            documents.append(
                {
                    "page_id": "project-docs:briefs",
                    "page_title": "Project Briefs",
                    "nav_title": "Project Briefs",
                    "page_heading": "Project Briefs",
                    "sidebar_group": "Project Briefs",
                    "output_path": BUILD_DIR
                    / "project-documentation"
                    / "projects"
                    / "index.html",
                    "order": 3,
                    "tabbed_documents": build_project_brief_tabs(),
                }
            )
    return sorted(documents, key=lambda document: int(document["order"]))


def build_student_tabs() -> list[dict[str, Any]]:
    sections = []
    for index, relative_path in enumerate(STUDENT_DOCUMENTATION_ORDER):
        content_path = PROJECT_DOCS_DIR / relative_path
        _, body, _ = load_markdown_page(content_path)
        fallback_title = content_path.stem.replace("-", " ").title()
        title, body = extract_h1(body, fallback_title)
        sections.append(
            {
                "index": index,
                "step": index + 1,
                "title": title,
                "html": render_markdown(body),
            }
        )
    return sections


def build_project_brief_tabs() -> list[dict[str, Any]]:
    sections = []
    for index, relative_path in enumerate(PROJECT_BRIEF_ORDER):
        content_path = PROJECT_DOCS_DIR / relative_path
        _, body, _ = load_markdown_page(content_path)
        fallback_title = content_path.stem.replace("-", " ").title()
        title, body = extract_h1(body, fallback_title)
        sections.append(
            {
                "index": index,
                "step": index + 1,
                "title": title,
                "html": render_markdown(body),
            }
        )
    return sections


def markdown_table(rows: list[tuple[str, ...]], headers: list[str]) -> str:
    header = "| " + " | ".join(headers) + " |"
    separator = "| " + " | ".join(["---"] * len(headers)) + " |"
    body = "\n".join("| " + " | ".join(row) + " |" for row in rows)
    return "\n".join([header, separator, body])


def build_weeks_table(weeks: list[dict[str, Any]]) -> str:
    rows = []
    for week in weeks:
        rows.append(
            (
                str(week.get("week", "")),
                str(week.get("theme", "")),
                str(week.get("domain_lecture", "")),
                str(week.get("engineering_lecture", "")),
            )
        )
    return markdown_table(
        rows, ["Week", "Theme", "Domain lecture", "Engineering lecture"]
    )


def resolve_includes(body: str, base_dir: Path, weeks: list[dict[str, Any]]) -> str:
    def replace_include(match: re.Match[str]) -> str:
        include_path = (base_dir / match.group(1).strip()).resolve()
        try:
            include_path.relative_to(ROOT)
        except ValueError as exc:
            msg = f"Include path escapes project root: {include_path}"
            raise ValueError(msg) from exc
        return include_path.read_text(encoding="utf-8").strip()

    body = re.sub(r"\{\{\s*include:\s*([^}]+)\s*\}\}", replace_include, body)
    return body.replace("{{ weeks_table }}", build_weeks_table(weeks))


def split_sections(body: str) -> list[tuple[str, str]]:
    sections: list[tuple[str, str]] = []
    current_title: str | None = None
    current_lines: list[str] = []

    for line in body.splitlines():
        if line.startswith("## "):
            if current_title is None and "\n".join(current_lines).strip():
                sections.append(("Overview", "\n".join(current_lines).strip()))
            if current_title is not None:
                sections.append((current_title, "\n".join(current_lines).strip()))
            current_title = line[3:].strip()
            current_lines = []
        else:
            current_lines.append(line)

    if current_title is not None:
        sections.append((current_title, "\n".join(current_lines).strip()))

    if not sections and body.strip():
        sections.append(("Content", body.strip()))

    return sections


def relative_url(from_file: Path, to_file: Path) -> str:
    return Path(os.path.relpath(to_file, from_file.parent)).as_posix()


def output_relative_path(path: Path) -> str:
    return path.relative_to(BUILD_DIR).as_posix()


def canonical_page_path(output_path: Path) -> str:
    relative_path = output_relative_path(output_path)
    if relative_path == "index.html":
        return ""
    return relative_path.removesuffix("index.html")


def analytics_page_url(site_metadata: dict[str, Any], output_path: Path) -> str:
    domain = str(site_metadata.get("analytics_domain", "")).strip().strip("/")
    if not domain:
        return ""

    path_prefix = str(site_metadata.get("analytics_path_prefix", "")).strip("/")
    page_path = canonical_page_path(output_path).strip("/")
    url_path = "/".join(part for part in (path_prefix, page_path) if part)

    if url_path:
        return f"https://{domain}/{url_path}/"
    return f"https://{domain}/"


def static_url(output_path: Path, root_relative_path: str | int | None) -> str:
    if not root_relative_path:
        return ""
    return relative_url(output_path, BUILD_DIR / str(root_relative_path))


def render_markdown(content: str) -> str:
    return MARKDOWN.render(content)


def build_navigation(
    output_path: Path,
    current_page_id: str,
    home_metadata: dict[str, Any],
    weeks: list[dict[str, Any]],
    documentation: list[dict[str, Any]],
) -> dict[str, Any]:
    groups: OrderedDict[str, list[dict[str, Any]]] = OrderedDict()

    def add_document(document: dict[str, Any]) -> None:
        group = str(document["sidebar_group"])
        groups.setdefault(group, [])
        groups[group].append(
            {
                "title": str(document["nav_title"]),
                "url": relative_url(output_path, document["output_path"]),
                "active": current_page_id == str(document["page_id"]),
            }
        )

    for document in documentation:
        add_document(document)

    for week in weeks:
        group = str(week["sidebar_group"])
        groups.setdefault(group, [])
        is_released = bool(week.get("is_released"))
        groups[group].append(
            {
                "title": str(week["nav_title"]),
                "url": relative_url(output_path, week["output_path"])
                if is_released
                else "",
                "active": current_page_id == str(week["page_id"]),
                "release_label": "" if is_released else str(week["release_label"]),
            }
        )

    return {
        "home": {
            "title": str(home_metadata.get("nav_title", "Course overview")),
            "url": relative_url(output_path, home_metadata["output_path"]),
            "active": current_page_id == str(home_metadata.get("page_id", "home")),
        },
        "groups": [{"title": group, "pages": pages} for group, pages in groups.items()],
    }


def page_sections(
    body: str, page_path: Path, weeks: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    resolved_body = resolve_includes(body, page_path.parent, weeks)
    _, resolved_body = extract_h1(resolved_body, "")
    sections = []
    for index, (title, content) in enumerate(split_sections(resolved_body)):
        sections.append(
            {
                "index": index,
                "step": index + 1,
                "title": title,
                "html": render_markdown(content),
            }
        )
    return sections


def sections_for_page(
    metadata: dict[str, Any], body: str, page_path: Path, weeks: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    if metadata.get("tabbed_documents"):
        return list(metadata["tabbed_documents"])
    return page_sections(body, page_path, weeks)


def render_page(
    *,
    template,
    output_path: Path,
    metadata: dict[str, Any],
    body: str,
    page_path: Path,
    site_metadata: dict[str, Any],
    home_metadata: dict[str, Any],
    weeks: list[dict[str, Any]],
    documentation: list[dict[str, Any]],
    previous_week: dict[str, Any] | None = None,
    next_week: dict[str, Any] | None = None,
) -> None:
    page_id = str(metadata.get("page_id", page_path.stem))
    sections = sections_for_page(metadata, body, page_path, weeks)

    context = {
        "site_title": str(site_metadata.get("site_title", "BiGHT")),
        "page_title": str(
            metadata.get("page_title", metadata.get("nav_title", "BiGHT"))
        ),
        "header_title": str(
            site_metadata.get("header_title", site_metadata.get("site_title", "BiGHT"))
        ),
        "logo_url": static_url(output_path, site_metadata.get("logo_image")),
        "logo_height": str(site_metadata.get("logo_height", 100)),
        "favicon_url": static_url(output_path, "images/light_favicon.png"),
        "css_url": static_url(output_path, "assets/site.css"),
        "js_url": static_url(output_path, "assets/site.js"),
        "hero_url": static_url(output_path, metadata.get("hero_image")),
        "hero_width": str(metadata.get("hero_width", "100%")),
        "week": metadata.get("week"),
        "theme": metadata.get("theme"),
        "page_heading": str(metadata.get("page_heading", "")),
        "sections": sections,
        "section_count": len(sections),
        "previous_week_url": (
            relative_url(output_path, previous_week["output_path"])
            if previous_week
            else ""
        ),
        "next_week_url": (
            relative_url(output_path, next_week["output_path"]) if next_week else ""
        ),
        "navigation": build_navigation(
            output_path, page_id, home_metadata, weeks, documentation
        ),
        "analytics_domain": str(site_metadata.get("analytics_domain", "")),
        "analytics_page_url": analytics_page_url(site_metadata, output_path),
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(template.render(context), encoding="utf-8")


def copy_tree(source: Path, target: Path) -> None:
    if source.exists():
        shutil.copytree(source, target, dirs_exist_ok=True)


def prepare_build_dir() -> None:
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
    BUILD_DIR.mkdir(parents=True)
    (BUILD_DIR / ".nojekyll").write_text("", encoding="utf-8")


def copy_static_files() -> None:
    copy_tree(ROOT / "images", BUILD_DIR / "images")
    copy_tree(SOURCE_ASSETS_DIR, BUILD_DIR / "assets")


def build_site() -> None:
    site_metadata = dict(load_metadata("content/site/header.md"))
    home_metadata, home_body, home_path = load_markdown_page("content/pages/home.md")
    home_metadata = dict(home_metadata)
    home_metadata["output_path"] = BUILD_DIR / "index.html"

    weeks = annotate_week_releases(load_week_metadata(), current_build_time())
    released_weeks = [week for week in weeks if week["is_released"]]
    documentation = load_project_documentation_metadata()

    environment = Environment(
        loader=FileSystemLoader(TEMPLATES_DIR),
        autoescape=select_autoescape(["html", "xml"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = environment.get_template("layout.html.j2")

    prepare_build_dir()
    copy_static_files()

    render_page(
        template=template,
        output_path=home_metadata["output_path"],
        metadata=home_metadata,
        body=home_body,
        page_path=home_path,
        site_metadata=site_metadata,
        home_metadata=home_metadata,
        weeks=weeks,
        documentation=documentation,
    )

    for index, week in enumerate(released_weeks):
        metadata, body, page_path = load_markdown_page(week["content_path"])
        render_page(
            template=template,
            output_path=week["output_path"],
            metadata=dict(metadata),
            body=body,
            page_path=page_path,
            site_metadata=site_metadata,
            home_metadata=home_metadata,
            weeks=weeks,
            documentation=documentation,
            previous_week=released_weeks[index - 1] if index > 0 else None,
            next_week=released_weeks[index + 1]
            if index + 1 < len(released_weeks)
            else None,
        )

    for document in documentation:
        if "content_path" in document:
            metadata, body, page_path = load_markdown_page(document["content_path"])
            metadata = {**metadata, **document}
        else:
            metadata = dict(document)
            body = ""
            page_path = PROJECT_DOCS_DIR / "student"
        render_page(
            template=template,
            output_path=document["output_path"],
            metadata=metadata,
            body=body,
            page_path=page_path,
            site_metadata=site_metadata,
            home_metadata=home_metadata,
            weeks=weeks,
            documentation=documentation,
        )


def check_release_schedule() -> None:
    weeks = load_week_metadata()
    cases = [
        ("2026-09-09T12:59:00+00:00", []),
        ("2026-09-09T13:01:00+00:00", [1]),
        ("2026-10-28T13:59:00+00:00", [1, 2, 3, 4, 5, 6]),
        ("2026-10-28T14:01:00+00:00", [1, 2, 3, 4, 5, 6, 7]),
        ("2026-12-16T14:01:00+00:00", list(range(1, 15))),
    ]
    for raw_build_time, expected_weeks in cases:
        build_time = parse_build_time(raw_build_time)
        released_weeks = [
            int(week["week"])
            for week in annotate_week_releases(weeks, build_time)
            if week["is_released"]
        ]
        if released_weeks != expected_weeks:
            msg = (
                f"Release schedule check failed for {raw_build_time}: "
                f"expected {expected_weeks}, got {released_weeks}"
            )
            raise SystemExit(msg)
    print("Release schedule checks passed")


if __name__ == "__main__":
    if "--check-release-schedule" in sys.argv:
        check_release_schedule()
        raise SystemExit(0)
    build_site()
    print(f"Built static site in {BUILD_DIR.relative_to(ROOT)}")
