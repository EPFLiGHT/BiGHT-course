import base64
import os
from typing import Dict, List, Optional

import streamlit as st
from openai import OpenAI


def get_available_models():
    """Get available language models for quiz interactions."""
    return {
        "Gemma 3 27B": "google/gemma-3-27b-it:free",
        # "Mistral Small 3.2": "mistralai/mistral-small-3.1-24b-instruct:free",
        # "Llama 3.3 70B": "meta-llama/llama-3.3-70b-instruct:free",
        # "Qwen3 Next 80B": "qwen/qwen3-next-80b-a3b-instruct:free",
    }


def get_openai_client():
    """Get OpenAI client with API key configuration."""
    api_key = None

    # Read from local file
    if os.path.exists("cle_openrouter.txt"):
        try:
            with open("cle_openrouter.txt", "r") as f:
                api_key = f.read().strip()
        except Exception as e:
            st.error(f"Error reading API key from file: {str(e)}")
            api_key = None
    else:
        st.write("Text file not found")

    # If no local file, try to get from Streamlit secrets
    if not api_key:
        try:
            api_key = st.secrets.get("openrouterkey")
            if api_key:
                st.write("Found API key in Streamlit secrets")
        except Exception:
            api_key = None

    # If still no API key, show configuration instructions
    if not api_key:
        st.error(
            "**API Key Required**: Please configure your OpenRouter API key to use the quiz feature."
        )
        st.stop()

    # Validate API key format (basic check)
    if not api_key or len(api_key) < 10:
        st.error("Invalid API key format. Please check your configuration.")
        st.stop()

    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )


def ask_llm_streaming(messages, placeholder, model_name):
    """Stream LLM response and update placeholder in real-time."""
    client = get_openai_client()
    full_names_models = get_available_models()

    try:
        completion = client.chat.completions.create(
            extra_headers={},
            extra_body={},
            model=full_names_models[model_name],
            messages=messages,
            stream=True,
        )

        full_response = ""
        for chunk in completion:
            if chunk.choices[0].delta.content is not None:
                full_response += chunk.choices[0].delta.content
                # Update the placeholder with the accumulated response
                placeholder.markdown(full_response + "▌")

        # Final update without the cursor
        placeholder.markdown(full_response)
        return full_response

    except Exception as e:
        placeholder.error(f"Error during streaming: {str(e)}")
        return None


def create_quiz_conversation(
    questions: List[str],
    quiz_title: str,
    quiz_description: str,
    question_start: int = 0,
    questions_per_chunk: int = 5,
) -> List[Dict]:
    """
    Create a conversation starter for a quiz section.

    Args:
        questions: List of questions for the quiz
        quiz_title: Title of the quiz
        quiz_description: Description of the quiz
        question_start: Starting question index (0-based)
        questions_per_chunk: Number of questions to include in this chunk

    Returns:
        List of message dictionaries for the conversation
    """
    # Get the subset of questions for this chunk
    end_index = min(question_start + questions_per_chunk, len(questions))
    chunk_questions = questions[question_start:end_index]

    # Create the conversation starter
    conversation = [
        {
            "role": "llm",
            "content": f"""Welcome to the {quiz_title}!

{quiz_description}

I'll be asking you {len(chunk_questions)} questions to assess your current knowledge. Please answer each question to the best of your ability. It's perfectly fine if you don't know some answers - just say "I don't know" rather than guessing.

Here are the questions:

{chr(10).join(f"{i + 1}. {q}" for i, q in enumerate(chunk_questions))}

Please provide your answers, and I'll assess your understanding and provide personalized feedback and learning recommendations.""",
        }
    ]

    return conversation


def make_quiz_page(
    questions: List[str],
    quiz_title: str,
    quiz_description: str,
    page_title: str,
    page_icon: str = "images/light_favicon.png",
    quiz_id: Optional[str] = None,
):
    """Create an interactive quiz page with AI grading and feedback."""

    st.set_page_config(page_title=page_title, layout="wide", page_icon=page_icon)

    # Create unique session state keys for this quiz
    if quiz_id is None:
        quiz_id = page_title.replace(" ", "_").replace("-", "_").lower()

    progress_key = f"quiz_progress_{quiz_id}"
    messages_key = f"messages_{quiz_id}"
    model_key = f"model_name_{quiz_id}"

    st.title(quiz_title)
    st.markdown(f"*{quiz_description}*")

    # Model selection
    available_models = get_available_models()
    list_models = list(available_models.keys())

    if model_key not in st.session_state:
        st.session_state[model_key] = "Gemma 3 27B"
    elif st.session_state[model_key] not in list_models:
        st.session_state[model_key] = "Gemma 3 27B"

    selected_model = st.selectbox(
        "Choose a Language Model for assessment:",
        list_models,
        index=list_models.index(st.session_state[model_key]),
    )
    st.session_state[model_key] = selected_model

    # Quiz progress tracking
    if progress_key not in st.session_state:
        st.session_state[progress_key] = {
            "current_batch": 0,
            "questions_per_batch": 5,
            "total_questions": len(questions),
            "completed_questions": 0,
            "user_responses": [],
        }

    progress = st.session_state[progress_key]
    current_start = progress["current_batch"] * progress["questions_per_batch"]

    # Progress indicator
    st.progress(progress["completed_questions"] / progress["total_questions"])
    st.caption(
        f"Progress: {progress['completed_questions']}/{progress['total_questions']} questions completed"
    )

    # Start quiz button (only when no messages yet)
    if progress["completed_questions"] == 0 and messages_key not in st.session_state:
        if st.button("🚀 Start Quiz Assessment", type="primary"):
            # Initialize quiz conversation
            quiz_messages = create_quiz_conversation(
                questions,
                quiz_title,
                quiz_description,
                current_start,
                progress["questions_per_batch"],
            )
            st.session_state[messages_key] = quiz_messages
            st.rerun()

    # Continue quiz button (if more questions exist)
    elif (
        current_start < progress["total_questions"]
        and messages_key not in st.session_state
    ):
        # Create next batch conversation
        quiz_messages = create_quiz_conversation(
            questions,
            quiz_title,
            quiz_description,
            current_start,
            progress["questions_per_batch"],
        )
        st.session_state[messages_key] = quiz_messages
        st.rerun()

    # Chat interface
    if messages_key in st.session_state and st.session_state[messages_key]:
        # Load avatars
        def load_avatar_base64(file_path):
            with open(file_path, "rb") as f:
                return base64.b64encode(f.read()).decode()

        ai_avatar = load_avatar_base64("images/avatar_man.png")
        user_avatar = "images/avatar_man.png"

        # Clear chat button
        if len(st.session_state[messages_key]) > 1:
            if st.button(
                "🗑️ Clear Chat History",
                help="Clear all conversation history",
                type="secondary",
            ):
                if messages_key in st.session_state:
                    del st.session_state[messages_key]
                st.rerun()
            st.markdown("---")

        # Display messages
        for msg in st.session_state[messages_key]:
            role = msg["role"]
            avatar = ai_avatar if role == "llm" else user_avatar
            avatar_url = avatar if role == "user" else "data:image/png;base64," + avatar

            if role == "user":
                with st.chat_message("user", avatar=avatar_url):
                    st.markdown(msg["content"])
            else:
                with st.chat_message("ai"):
                    st.markdown(msg["content"])

        # Store chat input data in session state for external handling
        st.session_state[f"chat_input_data_{quiz_id}"] = {
            "messages_key": messages_key,
            "progress_key": progress_key,
            "model_key": model_key,
            "current_start": current_start,
            "progress": progress,
        }

    # Quiz completion message
    if progress["completed_questions"] >= progress["total_questions"]:
        st.success("🎉 Congratulations! You have completed the quiz assessment.")
        st.markdown("### 📊 Your Responses Summary")
        for i, response in enumerate(progress["user_responses"]):
            st.markdown(
                f"**Batch {response['batch'] + 1}:** {response['response'][:100]}..."
            )

        if st.button("🔄 Restart Quiz", type="secondary"):
            # Reset progress
            st.session_state[progress_key] = {
                "current_batch": 0,
                "questions_per_batch": 5,
                "total_questions": len(questions),
                "completed_questions": 0,
                "user_responses": [],
            }
            if messages_key in st.session_state:
                del st.session_state[messages_key]
            st.rerun()


def handle_quiz_chat_input(quiz_id):
    """Handle chat input for quiz pages - to be called after pagination."""
    chat_data_key = f"chat_input_data_{quiz_id}"

    if chat_data_key in st.session_state:
        chat_data = st.session_state[chat_data_key]
        messages_key = chat_data["messages_key"]
        model_key = chat_data["model_key"]
        current_start = chat_data["current_start"]
        progress = chat_data["progress"]

        # User input
        user_input = st.chat_input("Type your answers here...")
        if user_input:
            # Ensure message list exists
            if messages_key not in st.session_state:
                st.session_state[messages_key] = []
            # Add user message to session state immediately
            st.session_state[messages_key].append(
                {"role": "user", "content": user_input}
            )

            # Save user response
            progress["user_responses"].append(
                {
                    "batch": progress["current_batch"],
                    "question_start": current_start,
                    "response": user_input,
                }
            )

            # Force a rerun to display the user message immediately
            st.rerun()

        # Check if we need to generate a response (after user message was added)
        if (
            messages_key in st.session_state
            and st.session_state[messages_key]
            and st.session_state[messages_key][-1]["role"] == "user"
        ):
            # Create a placeholder for the streaming response
            with st.chat_message("ai"):
                response_placeholder = st.empty()

            # Stream the response
            full_response = ask_llm_streaming(
                st.session_state[messages_key],
                response_placeholder,
                st.session_state[model_key],
            )

            # Add the complete response to session state
            if full_response:
                st.session_state[messages_key].append(
                    {"role": "llm", "content": full_response}
                )

                # Mark this batch as completed but DO NOT auto-advance
                progress["completed_questions"] = min(
                    progress["completed_questions"] + progress["questions_per_batch"],
                    progress["total_questions"],
                )

                # Set a flag to allow the user to manually proceed
                next_ready_key = f"next_ready_{quiz_id}"
                st.session_state[next_ready_key] = True

        # Offer a manual Next button after the AI response
        next_ready_key = f"next_ready_{quiz_id}"
        if (
            st.session_state.get(next_ready_key)
            and progress["completed_questions"] < progress["total_questions"]
        ):
            if st.button("➡️ Next questions", key=f"next_btn_{quiz_id}"):
                # Advance to the next batch explicitly on user action
                progress["current_batch"] += 1
                # Clear current messages to show the next batch cleanly
                if messages_key in st.session_state:
                    del st.session_state[messages_key]
                # Reset flag and rerun
                del st.session_state[next_ready_key]
                st.rerun()
