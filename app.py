import json
import streamlit as st

from utils.ai_providers import (
    generate_gemini_response,
    generate_groq_response
)

from utils.database import (
    initialize_database,
    save_prompt,
    get_all_prompts,
    search_prompts,
    delete_prompt
)

initialize_database()

from utils.prompt_templates import build_prompt


st.set_page_config(
    page_title="PromptLab",
    page_icon="🚀",
    layout="wide"
)


st.title("🚀 PromptLab")
st.caption("Your AI-powered Prompt Engineering Workspace")


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
    return generate_gemini_response(instruction)


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
    return generate_gemini_response(instruction)


def generate_json_response(task, data):
    import json

    instruction = f"""
You are an expert data processing assistant.

TASK:
{task}

INPUT DATA:
{data}

Return valid JSON only.

Requirements:
1. Use meaningful JSON keys.
2. Use correct data types.
3. Do not include Markdown formatting.
4. Do not invent missing information.
5. Use null for unavailable information.
"""

    response = generate_gemini_response(instruction)

    try:
        return json.loads(response)
    except json.JSONDecodeError:
        raise ValueError("AI did not return valid JSON.")
# --------------------------------------------------
# TABS
# --------------------------------------------------

builder_tab, optimizer_tab, evaluator_tab, comparison_tab, history_tab, library_tab, json_tab = st.tabs([
    "📝 Prompt Builder",
    "✨ Prompt Optimizer",
    "📊 Prompt Evaluator",
    "⚖️ Model Comparison",
    "🕘 Prompt History",
    "📚 Prompt Library",
    "🔧 JSON Generator"
])


# --------------------------------------------------
# 1. PROMPT BUILDER
# --------------------------------------------------

with builder_tab:

    st.header("Create Your Prompt")

    role = st.text_input(
        "AI Role",
        "Act as a senior business data analyst",
        key="builder_role"
    )

    context = st.text_area(
        "Context",
        placeholder="Describe your business scenario...",
        key="builder_context"
    )

    task = st.text_area(
        "Task",
        placeholder="What should the AI accomplish?",
        key="builder_task"
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
        ],
        key="builder_format"
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

            save_prompt(
    "Generated Prompt",
    prompt,
    "General",
    "History"
)

    st.success("Prompt saved to history!")

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

                    result = generate_gemini_response(
                        st.session_state["generated_prompt"]
                    )

                st.session_state["builder_response"] = result

                save_prompt(
    "Optimized Prompt",
    result,
    "General",
    "History"
)

            except Exception as error:
                st.error(f"API request failed: {error}")

        if "builder_response" in st.session_state:

            st.subheader("AI Response")

            st.write(st.session_state["builder_response"])


# --------------------------------------------------
# 2. PROMPT OPTIMIZER
# --------------------------------------------------

with optimizer_tab:

    st.header("✨ AI Prompt Optimizer")

    st.write(
        "Transform basic prompts into clear, structured and effective prompts."
    )

    original_prompt = st.text_area(
        "Original Prompt",
        placeholder="Example: Analyze my sales data.",
        height=150,
        key="optimizer_original"
    )

    objective = st.text_input(
        "What do you want to achieve?",
        placeholder="Example: Identify sales trends and business opportunities.",
        key="optimizer_objective"
    )

    additional_context = st.text_area(
        "Additional Context (Optional)",
        placeholder="Provide relevant background information...",
        key="optimizer_context"
    )

    if st.button("Optimize My Prompt", type="primary"):

        if not original_prompt.strip() or not objective.strip():

            st.warning(
                "Please enter an original prompt and objective."
            )

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


# --------------------------------------------------
# 3. PROMPT EVALUATOR
# --------------------------------------------------

with evaluator_tab:

    st.header("📊 Prompt Quality Evaluator")

    st.write(
        "Evaluate your prompt across five quality dimensions."
    )

    evaluation_prompt = st.text_area(
        "Enter Prompt to Evaluate",
        placeholder="Paste your prompt here...",
        height=180,
        key="evaluation_prompt"
    )

    evaluation_objective = st.text_input(
        "Intended Objective",
        placeholder="What should this prompt accomplish?",
        key="evaluation_objective"
    )

    if st.button("Evaluate Prompt", type="primary"):

        if not evaluation_prompt.strip() or not evaluation_objective.strip():

            st.warning(
                "Please enter a prompt and its intended objective."
            )

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


# --------------------------------------------------
# 4. MULTI-MODEL AI COMPARISON
# --------------------------------------------------

with comparison_tab:

    st.header("⚖️ Multi-Model AI Comparison")

    st.write(
        "Compare responses from Gemini and Groq using the same prompt."
    )

    comparison_prompt = st.text_area(
        "Enter Your Prompt",
        placeholder="Example: Explain how AI is transforming e-commerce.",
        height=160,
        key="comparison_prompt"
    )

    compare_button = st.button(
        "Compare AI Responses",
        type="primary",
        key="compare_button"
    )

    if compare_button:

        if not comparison_prompt.strip():

            st.warning("Please enter a prompt before comparing.")

        else:

            gemini_response = None
            groq_response = None

            with st.spinner("Generating responses from both AI models..."):

                try:

                    gemini_response = generate_gemini_response(
                        comparison_prompt
                    )

                except Exception as error:

                    st.error(f"Gemini Error: {error}")

                try:

                    groq_response = generate_groq_response(
                        comparison_prompt
                    )

                except Exception as error:

                    st.error(f"Groq Error: {error}")

            st.session_state["comparison_gemini"] = gemini_response
            st.session_state["comparison_groq"] = groq_response

            st.session_state["comparison_original_prompt"] = comparison_prompt

    if (
        "comparison_gemini" in st.session_state
        or "comparison_groq" in st.session_state
    ):

        st.divider()

        st.subheader("AI Model Responses")

        col1, col2 = st.columns(2)

        with col1:

            st.markdown("### 🌐 Gemini")

            gemini_result = st.session_state.get(
                "comparison_gemini"
            )

            if gemini_result:

                st.markdown(gemini_result)

                st.download_button(
                    "Download Gemini Response",
                    data=gemini_result,
                    file_name="gemini_response.txt",
                    key="download_gemini"
                )

            else:

                st.warning("Gemini response is unavailable.")

        with col2:

            st.markdown("### ⚡ Groq")

            groq_result = st.session_state.get(
                "comparison_groq"
            )

            if groq_result:

                st.markdown(groq_result)

                st.download_button(
                    "Download Groq Response",
                    data=groq_result,
                    file_name="groq_response.txt",
                    key="download_groq"
                )

            else:

                st.warning("Groq response is unavailable.")

        if gemini_result and groq_result:

            st.success(
                "Both AI models generated responses successfully. "
                "Compare their accuracy, clarity, completeness and usefulness."
            )



# --------------------------------------------------
# 5. PROMPT HISTORY
# --------------------------------------------------

with history_tab:

    st.header("🕘 Prompt History")

    keyword = st.text_input(
        "Search prompt history",
        key="history_search"
    )

    if keyword.strip():
        prompts = search_prompts(keyword)
        prompts = [p for p in prompts if p[4] == "History"]
    else:
        prompts = [
            p for p in get_all_prompts()
            if p[4] == "History"
        ]

    if prompts:

        for prompt in prompts:

            with st.expander(f"{prompt[1]} - {prompt[6]}"):

                st.write(prompt[2])

                st.caption(
                    f"Category: {prompt[3]} | Type: {prompt[5]}"
                )

                st.download_button(
                    "Download",
                    data=prompt[2],
                    file_name=f"prompt_{prompt[0]}.txt",
                    key=f"history_download_{prompt[0]}"
                )

                if st.button(
                    "Delete",
                    key=f"history_delete_{prompt[0]}"
                ):
                    delete_prompt(prompt[0])
                    st.rerun()

    else:
        st.info("No prompt history found.")



# --------------------------------------------------
# 6. PROMPT LIBRARY
# --------------------------------------------------

with library_tab:

    st.header("📚 Reusable Prompt Library")

    st.write("Save your favourite prompts and reuse them later.")

    with st.form("save_library_prompt"):

        title = st.text_input("Prompt Title")

        category = st.selectbox(
            "Category",
            [
                "Business",
                "Data Analytics",
                "Programming",
                "Education",
                "Content Writing",
                "Other"
            ]
        )

        prompt_text = st.text_area(
            "Enter Prompt",
            height=150
        )

        submitted = st.form_submit_button("Save to Library")

        if submitted:

            if title.strip() and prompt_text.strip():

                save_prompt(
                    title,
                    prompt_text,
                    category,
                    "Library"
                )

                st.success("Prompt saved to your library!")
                st.rerun()

            else:
                st.warning("Please enter both a title and a prompt.")

    st.divider()

    st.subheader("Your Saved Prompts")

    library_search = st.text_input(
        "Search your library",
        key="library_search"
    )

    if library_search.strip():
        saved_prompts = search_prompts(library_search)
        saved_prompts = [
            p for p in saved_prompts if p[4] == "Library"
        ]
    else:
        saved_prompts = [
            p for p in get_all_prompts()
            if p[4] == "Library"
        ]

    if saved_prompts:

        for prompt in saved_prompts:

            with st.expander(prompt[1]):

                st.caption(
                    f"Category: {prompt[3]} | Saved: {prompt[6]}"
                )

                st.code(prompt[2], language="text")

                st.download_button(
                    "Download Prompt",
                    data=prompt[2],
                    file_name=f"library_prompt_{prompt[0]}.txt",
                    key=f"library_download_{prompt[0]}"
                )

                if st.button(
                    "Delete Prompt",
                    key=f"library_delete_{prompt[0]}"
                ):
                    delete_prompt(prompt[0])
                    st.rerun()

    else:
        st.info("Your prompt library is empty.")


# --------------------------------------------------
# 7. STRUCTURED JSON GENERATOR
# --------------------------------------------------

with json_tab:

    st.header("🔧 Structured JSON Generator")

    st.write(
        "Convert instructions and information into structured JSON."
    )

    json_task = st.text_input(
        "What should AI do?",
        placeholder="Example: Analyze customer feedback"
    )

    json_data = st.text_area(
        "Enter your data",
        placeholder="Example: The product is excellent and delivery was fast.",
        height=150
    )

    if st.button("Generate JSON", type="primary"):

        if not json_task.strip() or not json_data.strip():

            st.warning("Please enter both a task and input data.")

        else:

            try:

                with st.spinner("Generating structured JSON..."):

                    result = generate_json_response(
                        json_task,
                        json_data
                    )

                st.session_state["json_result"] = result

            except Exception as error:

                st.error(f"JSON generation failed: {error}")

    if "json_result" in st.session_state:

        st.subheader("Generated JSON")

        st.json(st.session_state["json_result"])

        json_string = json.dumps(
            st.session_state["json_result"],
            indent=4,
            ensure_ascii=False
        )

        st.download_button(
            "Download JSON",
            data=json_string,
            file_name="generated_data.json",
            mime="application/json",
            key="download_json"
        )



# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "PromptLab v1.2 | Python · Streamlit · Gemini API · Groq API"
)



def generate_json_response(task, data):
    instruction = f"""
You are an expert data processing assistant.

TASK:
{task}

INPUT DATA:
{data}

Return the result as valid JSON only.

Requirements:
1. Use meaningful JSON keys.
2. Use correct data types.
3. Do not include Markdown formatting.
4. Do not include explanations outside JSON.
5. Do not invent missing information.
6. If information is unavailable, use null.

Return valid JSON only.
"""

    response = generate_gemini_response(instruction)

    try:
        return json.loads(response)
    except json.JSONDecodeError:
        raise ValueError(
            "AI did not return valid JSON. Please try again."
        )
