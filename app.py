
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

api_key = os.getenv("GEMINI_API_KEY")
model = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")

def generate_response(prompt):
    if not api_key:
        raise ValueError("Gemini API key is missing. Configure your local .env file.")

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model=model,
        contents=prompt
    )

    if not response.text:
        raise ValueError("Gemini returned an empty response.")

    return response.text


def optimize_prompt(original_prompt, objective, context):
    instruction = f"""
You are an expert prompt engineer.

Your task is to optimize the user's existing prompt.

ORIGINAL PROMPT:
{original_prompt}

OBJECTIVE:
{objective}

ADDITIONAL CONTEXT:
{context if context.strip() else "No additional context provided."}

REQUIREMENTS:
1. Preserve the original intent.
2. Improve clarity and specificity.
3. Add an appropriate AI role.
4. Include relevant context.
5. Define clear tasks and requirements.
6. Specify a useful output format.
7. Include constraints to prevent fabricated information.
8. Do not introduce unsupported assumptions.

RETURN THESE SECTIONS:

### Improved Prompt
Provide the complete optimized prompt.

### Improvements Made
Explain the important changes.

### Why It Is Better
Explain how the improvements help.
"""
    return generate_response(instruction)


def evaluate_prompt(prompt, objective):
    instruction = f"""
You are a professional prompt quality evaluator.

Evaluate the following prompt.

PROMPT:
{prompt}

INTENDED OBJECTIVE:
{objective}

Score each dimension from 1 to 10:

1. Clarity
2. Context
3. Specificity
4. Task Definition
5. Output Format

Calculate the average score out of 10.

Return:

### Overall Score
Provide the average score out of 10.

### Dimension Scores
Show all five scores in a table.

### Strengths
Identify what the prompt does well.

### Weaknesses
Identify what is missing or unclear.

### Recommendations
Provide actionable improvements.

### Final Verdict
Explain whether the prompt is ready to use.

Be objective. Do not give high scores without justification.
"""
    return generate_response(instruction)


builder_tab, optimizer_tab, evaluator_tab = st.tabs([
    "📝 Prompt Builder",
    "✨ Prompt Optimizer",
    "📊 Prompt Evaluator"
])


with builder_tab:

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
            "Step-by-step explanation",
            "JSON"
        ]
    )

    if st.button("Generate Prompt", key="builder_button"):

        if not context.strip() or not task.strip():
            st.warning("Please provide both context and task.")

        else:
            prompt = build_prompt(
                role,
                context,
                task,
                output_format
            )

            st.session_state["generated_prompt"] = prompt

    if "generated_prompt" in st.session_state:

        st.subheader("Generated Prompt")

        st.code(
            st.session_state["generated_prompt"],
            language="text"
        )

        st.download_button(
            "Download Prompt",
            data=st.session_state["generated_prompt"],
            file_name="generated_prompt.txt",
            key="download_builder"
        )

        if st.button("Run with Gemini", key="builder_run"):

            try:
                with st.spinner("Gemini is generating a response..."):
                    result = generate_response(
                        st.session_state["generated_prompt"]
                    )

                st.session_state["builder_response"] = result

            except Exception as error:
                st.error(f"API request failed: {error}")

        if "builder_response" in st.session_state:
            st.subheader("AI Response")
            st.write(st.session_state["builder_response"])


with optimizer_tab:

    st.header("✨ AI Prompt Optimizer")

    st.write(
        "Transform basic prompts into clear, structured and effective prompts."
    )

    original_prompt = st.text_area(
        "Original Prompt",
        placeholder="Example: Analyze my sales data.",
        height=150
    )

    objective = st.text_input(
        "What do you want to achieve?",
        placeholder="Example: Identify sales trends and business opportunities."
    )

    additional_context = st.text_area(
        "Additional Context (Optional)",
        placeholder="Provide relevant background information..."
    )

    if st.button("Optimize My Prompt", type="primary"):

        if not original_prompt.strip() or not objective.strip():
            st.warning("Please enter an original prompt and objective.")

        else:
            try:
                with st.spinner("Optimizing your prompt..."):

                    result = optimize_prompt(
                        original_prompt,
                        objective,
                        additional_context
                    )

                st.session_state["optimized_result"] = result
                st.session_state["original_prompt"] = original_prompt

            except Exception as error:
                st.error(f"Optimization failed: {error}")

    if "optimized_result" in st.session_state:

        st.divider()

        st.subheader("Optimization Results")

        left, right = st.columns(2)

        with left:
            st.markdown("**Original Prompt**")
            st.info(st.session_state["original_prompt"])

        with right:
            st.markdown("**AI Optimized Result**")
            st.success("Improved prompt generated")

        st.markdown(st.session_state["optimized_result"])

        st.download_button(
            "Download Optimized Result",
            data=st.session_state["optimized_result"],
            file_name="optimized_prompt.txt",
            key="download_optimizer"
        )


with evaluator_tab:

    st.header("📊 Prompt Quality Evaluator")

    st.write(
        "Evaluate your prompt across five quality dimensions."
    )

    evaluation_prompt = st.text_area(
        "Enter Prompt to Evaluate",
        placeholder="Paste your prompt here...",
        height=180
    )

    evaluation_objective = st.text_input(
        "Intended Objective",
        placeholder="What should this prompt accomplish?"
    )

    if st.button("Evaluate Prompt", type="primary"):

        if not evaluation_prompt.strip() or not evaluation_objective.strip():
            st.warning("Please enter a prompt and its intended objective.")

        else:
            try:
                with st.spinner("Evaluating prompt quality..."):

                    result = evaluate_prompt(
                        evaluation_prompt,
                        evaluation_objective
                    )

                st.session_state["evaluation_result"] = result

            except Exception as error:
                st.error(f"Evaluation failed: {error}")

    if "evaluation_result" in st.session_state:

        st.divider()
        st.subheader("Evaluation Report")

        st.markdown(st.session_state["evaluation_result"])

        st.download_button(
            "Download Evaluation",
            data=st.session_state["evaluation_result"],
            file_name="prompt_evaluation.txt",
            key="download_evaluator"
        )


st.divider()

st.caption(
    "PromptLab v1.1 | Python · Streamlit · Gemini API"
)
