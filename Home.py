import streamlit as st

from markdown_content import get_base64_image, load_metadata, load_week_metadata
from utils import check_password

site_metadata = load_metadata("content/site/header.md")
home_metadata = load_metadata("content/pages/home.md")
logo_image = str(site_metadata["logo_image"])
logo_height = str(site_metadata["logo_height"])
header_title = str(
    site_metadata.get("header_title", site_metadata.get("site_title", ""))
)

st.set_page_config(
    page_title=str(site_metadata.get("site_title", "Course")),
    page_icon="images/light_favicon.png",
)

if not check_password():
    st.stop()


def build_navigation():
    pages_to_show = {
        "Home": [
            st.Page(
                str(home_metadata["stub_path"]),
                title=str(home_metadata.get("nav_title", "Course overview")),
            ),
            st.Page("pages/Chat_with_an_LLM.py", title="Chat with an LLM"),
        ]
    }

    for week in load_week_metadata():
        group = str(week["sidebar_group"])
        pages_to_show.setdefault(group, [])
        pages_to_show[group].append(
            st.Page(
                str(week["stub_path"]),
                title=str(week["nav_title"]),
            )
        )

    return pages_to_show


st.markdown(
    f"""
    <style>
        .logo-strip {{
            display: flex;
            align-items: center;
            gap: 1.25rem;
            margin: 0 0 -2rem 0;
            padding: 0;
        }}
        .logo-strip img {{
            display: block;
        }}
        .logo-strip-title {{
            color: #2E5FA9;
            font-family: 'Chillax', 'Helvetica Now', 'Helvetica Neue', Helvetica, Arial, sans-serif;
            font-size: clamp(1.35rem, 2.2vw, 2.25rem);
            font-weight: 600;
            line-height: 1.12;
            max-width: 980px;
        }}
    </style>
    <div class="logo-strip">
        <img src="data:image/png;base64,{get_base64_image(logo_image)}" height="{logo_height}" />
        <div class="logo-strip-title">{header_title}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

pg = st.navigation(build_navigation())
pg.run()
