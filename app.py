import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

from utils.prompt_templates import build_prompt

load_dotenv()

st.set_page_config(
    page_title="PromptLab",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 PromptLab")
st.caption("Your AI-powered Prompt Engineering Workspace")

st.sidebar.header("⚙️ Settings")

api_key = os.getenv("GEMINI_API_KEY")
model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

st.sidebar.write(f"Model: {model}")

st.header("Create Your Prompt")

role = st.text_input(
    "AI Role",
    "Act as a senior business data analyst"
)

context = st.text_area(
    "Context",
    placeholder="Describe your business scenario..."
)

task = st.text_area(
    "Task",
    placeholder="What should the AI accomplish?"
)

output_format = st.selectbox(
    "Output Format",
    [
        "Structured report",
        "Bullet points",
        "Table",
        "Executive summary",
        "Step-by-step explanation"
    ]
)

if st.button("Generate Prompt", type="primary"):

    if not context.strip() or not task.strip():
        st.warning("Please provide both context and task.")

    else:
        prompt = build_prompt(
            role,
            context,
            task,
            output_format
        )

        st.session_state["prompt"] = prompt

if "prompt" in st.session_state:

    st.subheader("Generated Prompt")

    st.code(
        st.session_state["prompt"],
        language="text"
    )

    st.download_button(
        "Download Prompt",
        data=st.session_state["prompt"],
        file_name="generated_prompt.txt"
    )

    st.subheader("AI Response")

    if st.button("Run with Gemini"):

        if not api_key:
            st.error(
                "Gemini API key missing. "
                "Configure GEMINI_API_KEY in your .env file."
            )

        else:
            try:
                with st.spinner("Gemini is thinking..."):

                    client = genai.Client(
                        api_key=api_key
                    )

                    response = client.models.generate_content(
                        model=model,
                        contents=st.session_state["prompt"]
                    )

                    st.session_state["response"] = response.text

            except Exception as error:
                st.error(f"API request failed: {error}")

    if "response" in st.session_state:
        st.markdown("### Generated Result")
        st.write(st.session_state["response"])

st.divider()

st.caption("PromptLab | Built with Python, Streamlit and Gemini API")
