import inspect
import os
import unicodedata
from pathlib import Path
from typing import List, Optional

import streamlit as st
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


def get_caller_pagename(pos: int = 1) -> str:
    caller_page = inspect.stack()[pos]
    caller_filename = caller_page.filename if caller_page else "unknown"
    return os.path.relpath(caller_filename, os.path.dirname(__file__))


def get_site_metadata_value(key: str, default: str = "") -> str:
    metadata_path = Path(__file__).parent / "content" / "site" / "header.md"
    if not metadata_path.exists():
        return default

    for line in metadata_path.read_text(encoding="utf-8").splitlines():
        if ":" not in line:
            continue
        raw_key, raw_value = line.split(":", 1)
        if raw_key.strip() == key:
            return raw_value.strip().strip('"\'')
    return default


def inject_global_css():
    from streamlit import markdown
    from streamlit.components.v1 import html

    require_authentication()

    page_name = get_caller_pagename()
    analytics_domain = get_site_metadata_value("analytics_domain")

    html(
        f"""
        <script defer data-domain="{analytics_domain}" src="https://plausible.io/js/script.manual.js"></script>
        <script>
          window.plausible = window.plausible || function() {{
            (window.plausible.q = window.plausible.q || []).push(arguments)
          }};
          plausible('pageview', {{ u: 'https://{analytics_domain}/{page_name}' }});
        </script>
        """,
        height=0,
    )

    markdown(
        """
        <style>
        @import url('https://api.fontshare.com/v2/css?f[]=chillax@400,500,600,700&display=swap');

        :root {
            --color-dark: #2E5FA9;
            --color-light: #5D9FD2;
            --color-bg-start: #F8FBFF;
            --color-bg-end: #E2EDFF;
        }

        body {
            background: linear-gradient(180deg, var(--color-bg-start) 0%, var(--color-bg-end) 100%);
            color: var(--color-dark);
            font-family: 'Helvetica Now', 'Helvetica Neue', Helvetica, Arial, sans-serif;
        }

        h1, h2, h3, h4, h5, h6 {
            font-family: 'Chillax', 'Helvetica Now', sans-serif;
            color: var(--color-dark);
        }

        .stApp {
            background: transparent;
        }

        .chat-message.llm {
            background-color: #E8F4FB;
        }
        .chat-message.user {
            background-color: #D3F3F1;
        }
        codebit {
            color: var(--color-dark);
        }
        .section {
            background-color: white;
            border: 1px solid var(--color-light);
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 2px 8px rgba(46, 95, 169, 0.08);
        }
        .start-btn {
            display: inline-block;
            padding: 0.75rem 1.5rem;
            background-color: var(--color-light);
            color: white;
            padding: 10px 20px;
            border-radius: 10px;
            font-size: 1.1rem;
            font-weight: 600;
            text-decoration: none;
            transition: background-color 0.3s ease;
        }
        .start-btn:hover {
            background-color: var(--color-dark);
        }
        hr {
            border-top: 1px solid var(--color-light);
        }
        p, div, li, span, .markdown-text-container {
            text-align: justify !important;
        }
        .stButton > button {
            white-space: nowrap;
            width: auto;
        }
        div[data-testid="column"]:has(> div > div > div .stButton) button {
            max-width: 100%;
        }
        /* Primary button styling */
        .stButton > button[kind="primary"] {
            background-color: var(--color-dark);
            color: white;
        }
        .stButton > button[kind="primary"]:hover {
            background-color: var(--color-light);
        }
        /* Secondary button styling */
        .stButton > button[kind="secondary"] {
            background-color: var(--color-light);
            color: white;
        }
        /* Success/info boxes */
        .stAlert {
            border-left: 4px solid var(--color-dark);
        }
        /* Progress bar */
        .stProgress > div > div {
            background-color: var(--color-light);
        }
        /* Links */
        a {
            color: var(--color-dark);
        }
        a:hover {
            color: var(--color-light);
        }
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: transparent;
            color: var(--color-dark);
            border-radius: 8px 8px 0 0;
        }
        .stTabs [aria-selected="true"] {
            background-color: var(--color-dark);
            color: white;
        }
        /* Sidebar wider for navigation */
        [data-testid="stSidebarNav"] {
            min-width: 320px;
            max-width: 320px;
        }
        [data-testid="stSidebarNav"] > div {
            flex-wrap: nowrap;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )


def collapsible_section(
    title: str, content: str, key: Optional[str] = None, compact: bool = False
):
    """
    Create a collapsible section with a clickable title that expands to show content.

    Args:
        title: The title to display in the collapsible header
        content: The content to show when expanded (can be markdown)
        key: Unique key for the collapsible state (auto-generated if not provided)
    """
    import streamlit as st

    if key is None:
        key = f"collapsible_{hash(title)}"

    # Initialize session state for this collapsible
    if key not in st.session_state:
        st.session_state[key] = False

    # Create the collapsible header with click functionality
    button_label = f"{'▼' if st.session_state[key] else '▶'} {title}"
    if st.button(
        button_label,
        key=f"{key}_button",
        help="Click to expand/collapse",
        use_container_width=False,  # keep natural width so it doesn't stretch
    ):
        st.session_state[key] = not st.session_state[key]
        st.rerun()

    # Show content if expanded
    if st.session_state[key]:
        # In compact mode, remove the surrounding .section box styling if present
        if compact and isinstance(content, str):
            import re as _re

            # Strip a single outer <div class="section"> ... </div>
            content = _re.sub(
                r"^\s*<div\s+class=\"section\">\s*([\s\S]*?)\s*</div>\s*$",
                r"\1",
                content,
            )
        st.markdown(content, unsafe_allow_html=True)


def paginate_content(
    page_id: str,
    sections: List,
    section_titles: List[str],
    show_end_of_page: bool = True,
    previous_page_path: Optional[str] = None,
    previous_page_label: Optional[str] = None,
    next_page_path: Optional[str] = None,
    next_page_label: Optional[str] = None,
):
    import streamlit as st

    if not sections:
        return

    if len(sections) != len(section_titles):
        raise ValueError(
            f"Number of sections ({len(sections)}) must match number of titles ({len(section_titles)})"
        )

    step_key = f"{page_id}_step_index"
    prev_key = f"{page_id}_prev"
    next_key = f"{page_id}_next"
    last_page_key = "_last_paginated_page_id"

    # Reset to first step when navigating to a new page from the sidebar
    if st.session_state.get(last_page_key) != page_id:
        st.session_state[step_key] = 0
        st.session_state[last_page_key] = page_id
    elif step_key not in st.session_state:
        st.session_state[step_key] = 0

    total_steps = len(sections)
    # Ensure current_step is always an integer
    current_step = (
        int(st.session_state[step_key]) if st.session_state[step_key] is not None else 0
    )

    if current_step < 0:
        current_step = 0
    if current_step > total_steps - 1:
        current_step = total_steps - 1
    st.session_state[step_key] = current_step

    st.caption(f"Step {current_step + 1} of {total_steps}")
    st.progress((current_step + 1) / total_steps)
    st.markdown(
        f"""
        <style>
        .st-key-{prev_key} {{
            width: 100%;
        }}
        .st-key-{prev_key} .stButton {{
            width: 100%;
            display: flex;
            justify-content: flex-start;
        }}
        .st-key-{prev_key} button {{
            width: 20rem !important;
            max-width: 100%;
            box-sizing: border-box;
            padding-left: 1.5rem !important;
            padding-right: 1.5rem !important;
            overflow: hidden;
        }}
        .st-key-{prev_key} button p {{
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            text-align: center !important;
            width: 100%;
        }}
        .st-key-{next_key} {{
            width: 100%;
        }}
        .st-key-{next_key} .stButton {{
            width: 100%;
            display: flex;
            justify-content: flex-end;
        }}
        .st-key-{next_key} button {{
            width: 20rem !important;
            max-width: 100%;
            box-sizing: border-box;
            padding-left: 1.5rem !important;
            padding-right: 1.5rem !important;
            overflow: hidden;
        }}
        .st-key-{next_key} button p {{
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            text-align: center !important;
            width: 100%;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    left, _, middle, _, right = st.columns([3, 2, 4, 2, 3])

    def _truncate_text(text: str, max_chars: int) -> str:
        if len(text) <= max_chars:
            return text
        return text[: max(0, max_chars - 1)] + "…"

    prev_label = "Previous"
    if current_step > 0:
        prev_title = section_titles[current_step - 1]
        constrained_title = _truncate_text(prev_title, 28)
        prev_label = f"Previous ({constrained_title})"
    elif previous_page_path:
        prev_label = "Previous week"

    next_label = "Next"
    if current_step < total_steps - 1:
        next_title = section_titles[current_step + 1]
        constrained_title = _truncate_text(next_title, 28)
        next_label = f"Next ({constrained_title})"
    elif next_page_path:
        next_label = "Next week"

    with left:
        if current_step > 0:
            if st.button(prev_label, key=prev_key):
                st.session_state[step_key] = current_step - 1
                st.rerun()
        elif previous_page_path:
            if st.button(prev_label, key=prev_key):
                st.switch_page(previous_page_path)
        else:
            st.button(prev_label, disabled=True, key=prev_key)

    with middle:
        page_options = [f"{i + 1}. {section_titles[i]}" for i in range(total_steps)]
        page_select_key = f"{page_id}_page_select"

        selected_page = st.selectbox(
            "Jump to page:",
            options=list(range(total_steps)),
            format_func=lambda i: page_options[i],
            index=current_step,
            key=page_select_key,
            label_visibility="collapsed",
        )

        if selected_page != current_step:
            st.session_state[step_key] = selected_page
            st.rerun()

    with right:
        if current_step < total_steps - 1:
            if st.button(next_label, key=next_key):
                st.session_state[step_key] = current_step + 1
                st.rerun()
        elif next_page_path:
            if st.button(next_label, key=next_key):
                st.switch_page(next_page_path)

    sections[current_step]()

    # End-of-page notice
    if show_end_of_page and current_step >= total_steps - 1 and next_page_path:
        st.info("End of this part. Click Next to open the next weekly page.")
    elif show_end_of_page and current_step >= total_steps - 1:
        st.info(
            "End of this part. Use the left navigation to open the next part in this module."
        )


ph = PasswordHasher(time_cost=2, memory_cost=102400, parallelism=8)


def hash_argon2(password: str) -> str:
    pw = unicodedata.normalize("NFKC", password)
    return ph.hash(pw)


def verify_argon2(stored_hash: str, provided_password: str) -> bool:
    try:
        return ph.verify(stored_hash, unicodedata.normalize("NFKC", provided_password))
    except VerifyMismatchError:
        return False


def check_password():
    """
    Show login form if user not authenticated yet.
    Return True if user is authenticated.
    """
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    # Load hash from secrets if available
    try:
        actual = st.secrets["password"]
    except Exception:
        # local run, no need to use a password
        st.session_state.authenticated = True

    if st.session_state.authenticated:
        return True

    # Show login form
    st.title("🔒 Please log in")
    with st.form("login_form"):
        password = st.text_input("Enter password:", type="password")
        submitted = st.form_submit_button("Login")

    if submitted:
        if verify_argon2(actual, password):
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("❌ Incorrect password")

    return False


def require_authentication(page_key: str = ""):
    """
    Call this at the top of each page to enforce authentication.
    - page_key doit correspondre à la clé (ou chemin) que tu utilises dans st.navigation.
    """

    if page_key == "":
        page_key = get_caller_pagename(3)

    if not check_password():
        st.session_state.redirect_to = page_key
        st.stop()
