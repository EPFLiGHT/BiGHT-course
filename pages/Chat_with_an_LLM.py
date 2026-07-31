import base64
import os
from typing import Optional

import streamlit as st
from openai import OpenAI

from utils import inject_global_css


def make_chat_page(
    title: str = "Chat with an LLM",
    messages: Optional[list] = None,
    api_key: Optional[str] = None,
    intro_msg: str = "",
):
    # Handle API key configuration
    if api_key is None:
        # Read from local file
        if os.path.exists("cle_openrouter.txt"):
            try:
                with open("cle_openrouter.txt", "r") as f:
                    api_key = f.read().strip()
            except Exception:
                api_key = None

        # If no local file, try to get from Streamlit secrets
        if not api_key:
            try:
                api_key = st.secrets.get("openrouterkey")
            except Exception:
                api_key = None

        # If still no API key, show configuration instructions
        if not api_key:
            st.error(
                "**API Key Required**: Please configure your OpenRouter API key to use the chat feature."
            )
            st.stop()

    # Validate API key format (basic check)
    if not api_key or len(api_key) < 10:
        st.error("Invalid API key format. Please check your configuration.")
        st.stop()

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    st.session_state.model_name = "Gemma 3 27B"  # "Mistral Small 3.2"
    full_names_models = {
        "Gemma 3 27B": "google/gemma-3-27b-it:free",
        # "Mistral Small 3.2": "mistralai/mistral-small-3.1-24b-instruct:free",
        # "Llama 3.3 70B": "meta-llama/llama-3.3-70b-instruct:free",
        # "Qwen3 Next 80B": "qwen/qwen3-next-80b-a3b-instruct:free",
    }

    def ask_gpt_streaming(messages, placeholder):
        # Stream the LLM response and update the placeholder in real-time
        try:
            completion = client.chat.completions.create(
                extra_headers={},
                extra_body={},
                model=full_names_models[st.session_state.model_name],
                messages=messages,
                stream=True,
            )

            full_response = ""
            for chunk in completion:
                if chunk.choices and chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    # Update the placeholder with the accumulated response
                    placeholder.markdown(full_response + "▌")

            # Final update without the cursor
            placeholder.markdown(full_response)
            return full_response

        except Exception as e:
            placeholder.error(f"Error during streaming: {str(e)}")
            return None

    # Page setup
    st.title(title)

    st.set_page_config(
        page_title=title, layout="wide", page_icon="images/light_favicon.png"
    )
    inject_global_css()

    # Load avatars (make sure to have your avatar PNGs in the same folder or update path)
    def load_avatar_base64(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()

    ai_avatar = load_avatar_base64("images/avatar_man.png")
    user_avatar = "images/avatar_man.png"  # default user icon

    list_models = list(full_names_models.keys())
    value = st.selectbox(
        "Choose a Language Model to interact with",
        list_models,
        index=list_models.index(st.session_state.model_name),
    )
    st.session_state.model_name = value

    # Initial message state
    if "messages" not in st.session_state:
        if messages:
            st.session_state.messages = messages
        else:
            st.session_state.messages = [
                {
                    "role": "llm",
                    "content": """Welcome! I'm here to help you with your learning journey.

You can ask me questions about:
- AI and Machine Learning concepts
- Programming and technical topics
- Healthcare applications of AI
- Any other topic you'd like to explore

What would you like to know today?""",
                }
            ]

    # --- Top bar ---
    if intro_msg:
        st.markdown(
            f"""
            {intro_msg}
            <hr>
        """,
            unsafe_allow_html=True,
        )

    # --- Chat controls ---
    if (
        st.session_state.messages and len(st.session_state.messages) > 1
    ):  # Only show if there are messages to clear
        if st.button(
            "🗑️ Clear Chat History",
            help="Clear all conversation history",
            type="secondary",
        ):
            # Clear the messages from session state
            if "messages" in st.session_state:
                del st.session_state.messages
            st.rerun()
        st.markdown("---")  # Add a separator

    # --- Chat area ---
    for msg in st.session_state.messages:
        role = msg["role"]
        avatar = ai_avatar if role == "llm" else user_avatar
        avatar_url = avatar if role == "user" else "data:image/png;base64," + avatar

        # with st.chat_message(role):
        # st.markdown(msg["content"])

        if role == "user":
            with st.chat_message("user", avatar=avatar_url):
                st.markdown(msg["content"])
        else:
            with st.chat_message("ai"):
                st.markdown(msg["content"])

    # --- User input ---
    user_input = st.chat_input("Type your message here...")
    if user_input:
        # Add user message to session state immediately
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Force a rerun to display the user message immediately
        st.rerun()

    if (
        st.session_state.messages and st.session_state.messages[-1]["role"] == "user"
    ):  # User just sent a message, need AI response
        # Create a placeholder for the streaming response
        with st.chat_message("ai"):
            response_placeholder = st.empty()

        # Stream the response
        full_response = ask_gpt_streaming(
            st.session_state.messages, response_placeholder
        )

        # Add the complete response to session state
        if full_response:
            st.session_state.messages.append({"role": "llm", "content": full_response})


if __name__ == "__main__":
    make_chat_page()
