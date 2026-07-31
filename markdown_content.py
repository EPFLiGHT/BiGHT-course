import base64
import re
from pathlib import Path

import streamlit as st

from utils import inject_global_css, paginate_content

ROOT = Path(__file__).parent
WEEKS_DIR = ROOT / "content" / "weeks"


def get_base64_image(image_path: str) -> str:
    with open(ROOT / image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


def parse_value(value: str):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    if value.isdigit():
        return int(value)
    return value


def parse_front_matter(text: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        return {}, text

    end_marker = "\n---\n"
    end = text.find(end_marker, 4)
    if end == -1:
        return {}, text

    raw_metadata = text[4:end]
    body = text[end + len(end_marker) :]
    metadata = {}

    for line in raw_metadata.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        metadata[key.strip()] = parse_value(value)

    return metadata, body


def load_markdown_page(path: str | Path) -> tuple[dict, str, Path]:
    page_path = ROOT / path if isinstance(path, str) else path
    text = page_path.read_text(encoding="utf-8")
    metadata, body = parse_front_matter(text)
    return metadata, body, page_path


def load_metadata(path: str | Path) -> dict:
    metadata, _, _ = load_markdown_page(path)
    return metadata


def load_week_metadata() -> list[dict]:
    weeks = []
    for path in WEEKS_DIR.glob("*.md"):
        metadata = load_metadata(path)
        metadata["content_path"] = str(path.relative_to(ROOT))
        weeks.append(metadata)
    return sorted(weeks, key=lambda item: int(item.get("order", item.get("week", 0))))


def get_next_week_metadata(path: Path) -> dict | None:
    try:
        current_content_path = str(path.resolve().relative_to(ROOT))
    except ValueError:
        return None

    weeks = load_week_metadata()
    for index, week in enumerate(weeks):
        if week.get("content_path") == current_content_path:
            if index + 1 < len(weeks):
                return weeks[index + 1]
            return None
    return None


def get_previous_week_metadata(path: Path) -> dict | None:
    try:
        current_content_path = str(path.resolve().relative_to(ROOT))
    except ValueError:
        return None

    weeks = load_week_metadata()
    for index, week in enumerate(weeks):
        if week.get("content_path") == current_content_path:
            if index > 0:
                return weeks[index - 1]
            return None
    return None


def markdown_table(rows: list[tuple[str, ...]], headers: list[str]) -> str:
    header = "| " + " | ".join(headers) + " |"
    separator = "| " + " | ".join(["---"] * len(headers)) + " |"
    body = "\n".join("| " + " | ".join(row) + " |" for row in rows)
    return "\n".join([header, separator, body])


def build_weeks_table() -> str:
    rows = []
    for week in load_week_metadata():
        rows.append(
            (
                str(week.get("week", "")),
                str(week.get("theme", "")),
                str(week.get("domain_lecture", "")),
                str(week.get("engineering_lecture", "")),
            )
        )
    return markdown_table(rows, ["Week", "Theme", "Domain lecture", "Engineering lecture"])


def resolve_includes(body: str, base_dir: Path) -> str:
    def replace_include(match: re.Match) -> str:
        include_path = (base_dir / match.group(1).strip()).resolve()
        return include_path.read_text(encoding="utf-8").strip()

    body = re.sub(r"\{\{\s*include:\s*([^}]+)\s*\}\}", replace_include, body)
    return body.replace("{{ weeks_table }}", build_weeks_table())


def split_sections(body: str) -> list[tuple[str, str]]:
    sections = []
    current_title = None
    current_lines = []

    for line in body.splitlines():
        if line.startswith("## "):
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


def render_hero(metadata: dict) -> None:
    hero_image = metadata.get("hero_image")
    if not hero_image:
        return

    hero_width = metadata.get("hero_width", "100%")
    st.markdown(
        f"""
<div class="markdown-hero">
    <img src="data:image/png;base64,{get_base64_image(str(hero_image))}" />
</div>
<style>
    .markdown-hero {{
        width: 100%;
        margin-bottom: 0.5rem;
        line-height: 0;
        text-align: center;
    }}
    .markdown-hero img {{
        width: {hero_width};
        height: auto;
        display: block;
        margin: 0 auto;
    }}
</style>
        """,
        unsafe_allow_html=True,
    )


def render_week_title(metadata: dict) -> None:
    week = metadata.get("week")
    theme = metadata.get("theme")
    if not week or not theme:
        return

    st.markdown(
        f"""
<div class="week-title-banner">
    <h1>Week {week}: {theme}</h1>
</div>
<style>
    .week-title-banner {{
        margin: 0.35rem 0 1rem 0;
    }}
    .week-title-banner h1 {{
        color: #2E5FA9;
        font-size: clamp(1.8rem, 3vw, 3rem);
        line-height: 1.08;
        margin: 0;
    }}
</style>
        """,
        unsafe_allow_html=True,
    )


def make_section_renderer(title: str, content: str, show_hero: bool, metadata: dict):
    def render_section():
        if show_hero:
            render_hero(metadata)
            render_week_title(metadata)
        st.markdown(f"### {title}")
        st.markdown(
            f"""
<div class="section">

{content}

</div>
            """,
            unsafe_allow_html=True,
        )

    return render_section


def render_markdown_page(path: str) -> None:
    metadata, body, page_path = load_markdown_page(path)

    st.set_page_config(
        page_title=str(metadata.get("page_title", metadata.get("nav_title", "Course"))),
        layout="wide",
        page_icon="images/light_favicon.png",
    )
    inject_global_css()

    body = resolve_includes(body, page_path.parent)
    sections = split_sections(body)
    renderers = []
    titles = []

    for index, (title, content) in enumerate(sections):
        renderers.append(make_section_renderer(title, content, index == 0, metadata))
        titles.append(title)

    previous_week = get_previous_week_metadata(page_path)
    next_week = get_next_week_metadata(page_path)

    paginate_content(
        str(metadata.get("page_id", page_path.stem)),
        renderers,
        titles,
        previous_page_path=previous_week.get("stub_path") if previous_week else None,
        previous_page_label=previous_week.get("nav_title") if previous_week else None,
        next_page_path=next_week.get("stub_path") if next_week else None,
        next_page_label=next_week.get("nav_title") if next_week else None,
    )
