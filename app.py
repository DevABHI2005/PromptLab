import json
import textwrap
import streamlit as st
import streamlit.components.v1 as components

from utils.ai_providers import generate_gemini_response, generate_groq_response
from utils.prompt_templates import build_prompt
from utils.database import (
    initialize_database,
    save_prompt,
    get_all_prompts,
    search_prompts,
    delete_prompt,
)


# ============================================================
# PAGE SETUP, STYLES AND DATABASE
# ============================================================
st.set_page_config(
    page_title="PromptLab | AI Prompt Workspace",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)


def load_css():
    try:
        with open("assets/style.css", encoding="utf-8") as file:
            css = file.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("CSS file not found. Create assets/style.css to enable the custom theme.")


load_css()
st.markdown("""<style>
/* PromptLab component polish */
:root { --pl-purple:#8b5cf6; --pl-indigo:#6366f1; --pl-panel:#151c31; --pl-border:#303d5c; }
.stApp { background: radial-gradient(circle at 82% 5%, rgba(99,102,241,.13), transparent 28%), #0b1020; }
.block-container { max-width: 1380px; padding-top: 2rem; padding-bottom: 3rem; }
.sidebar-brand { color:#c4b5fd; font-size:1.65rem; font-weight:800; letter-spacing:-.5px; padding:.35rem 0; }
[data-testid="stSidebar"] { background:linear-gradient(180deg,#111827 0%,#1e1b4b 100%); border-right:1px solid #37306b; }
[data-testid="stSidebar"] [data-testid="stRadio"] label { padding:.48rem .65rem; border-radius:10px; }
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover { background:rgba(139,92,246,.16); }
.hero-title { color:#f8fafc; font-size:clamp(2rem,4vw,3.25rem); line-height:1.12; font-weight:850; letter-spacing:-1.5px; margin-bottom:.7rem; }
.hero-subtitle { color:#a78bfa; font-size:1.05rem; font-weight:650; margin-bottom:1.5rem; }
.page-kicker { color:#a78bfa; font-size:.72rem; font-weight:800; letter-spacing:2px; margin-bottom:.35rem; }
.qa-answer { background:linear-gradient(135deg,#211b46,#142344); border:1px solid #7356c9; border-radius:18px; padding:24px 26px; margin:1.2rem 0; box-shadow:0 12px 34px rgba(99,102,241,.12); }
.answer-label { color:#c4b5fd; font-size:.72rem; font-weight:850; letter-spacing:2px; margin-bottom:12px; }
.qa-answer p { color:#e2e8f0; font-size:1rem; line-height:1.75; }
.qa-answer b { color:#c4b5fd; }
.feature-card { background:linear-gradient(145deg,#1a2440,#141b30); border:1px solid #303d5c; border-radius:17px; padding:22px; min-height:190px; margin:0 0 10px; transition:transform .2s ease,border-color .2s ease,box-shadow .2s ease; }
.feature-card:hover { transform:translateY(-4px); border-color:#8b5cf6; box-shadow:0 12px 30px rgba(99,102,241,.16); }
.feature-icon { font-size:30px; margin-bottom:12px; }
.feature-title { color:#f8fafc; font-size:1.08rem; font-weight:750; margin-bottom:9px; }
.feature-description { color:#b8c4d9; font-size:.9rem; line-height:1.6; min-height:62px; }
.feature-label { display:inline-block; color:#ddd6fe; background:#38266e; border-radius:20px; padding:5px 11px; font-size:.68rem; font-weight:750; letter-spacing:.5px; margin-top:12px; }
.stButton > button, .stDownloadButton > button { border:1px solid rgba(167,139,250,.25); border-radius:11px; min-height:42px; font-weight:700; transition:all .18s ease; }
.stButton > button[kind="primary"] { background:linear-gradient(135deg,#7c3aed,#4f46e5); color:white; }
.stButton > button:hover, .stDownloadButton > button:hover { border-color:#a78bfa; transform:translateY(-1px); }
.stTextInput input, .stTextArea textarea, [data-baseweb="select"] > div { background:#151c31 !important; color:#f8fafc !important; border-color:#34415c !important; border-radius:10px !important; }
.stTextInput input:focus, .stTextArea textarea:focus { border-color:#8b5cf6 !important; box-shadow:0 0 0 1px #8b5cf6 !important; }
[data-testid="stVerticalBlockBorderWrapper"] { background:rgba(21,28,49,.56); border-color:#303d5c !important; border-radius:16px !important; padding:1rem; }
[data-testid="stExpander"] { background:#151c31; border:1px solid #303d5c; border-radius:12px; }
[data-testid="stAlert"] { border-radius:12px; }
.stTabs [data-baseweb="tab-list"] { gap:8px; }
.app-footer { text-align:center; color:#94a3b8; padding:24px 0 8px; line-height:1.9; }
.app-footer strong { color:#c4b5fd; font-size:1.25rem; }
@media (max-width: 768px) { .hero-title { font-size:2rem; } .feature-card { min-height:unset; } .feature-description { min-height:unset; } }
</style>""", unsafe_allow_html=True)
initialize_database()

PAGES = {
    "🏠 Home": "Home",
    "📝 Prompt Builder": "Build structured prompts",
    "✨ Prompt Optimizer": "Improve an existing prompt",
    "📊 Prompt Evaluator": "Measure prompt quality",
    "⚖️ Model Comparison": "Compare Gemini and Groq",
    "🕘 Prompt History": "Find previously saved prompts",
    "📚 Prompt Library": "Manage reusable prompts",
    "🔧 JSON Generator": "Turn information into JSON",
}

if "active_page" not in st.session_state:
    st.session_state.active_page = "🏠 Home"

DEFAULTS = {
    "generated_prompt": "",
    "builder_response": "",
    "optimized_result": "",
    "original_prompt": "",
    "evaluation_result": "",
    "comparison_gemini": "",
    "comparison_groq": "",
    "comparison_original_prompt": "",
    "json_result": None,
}
for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


def go_to(page):
    st.session_state.active_page = page


def page_heading(icon, title, subtitle):
    st.markdown(f"<div class='page-kicker'>{icon} PROMPTLAB WORKSPACE</div>", unsafe_allow_html=True)
    st.title(f"{icon} {title}")
    st.caption(subtitle)
    st.divider()


def result_panel(title, content, download_name, key, mime="text/plain"):
    st.markdown(f"#### {title}")
    st.code(content, language="text")
    st.download_button(
        "⬇️ Download result",
        data=content,
        file_name=download_name,
        mime=mime,
        key=key,
        use_container_width=False,
    )


def generate_response(prompt, provider="Gemini"):
    return generate_groq_response(prompt) if provider == "Groq" else generate_gemini_response(prompt)


def optimize_prompt(original_prompt, objective, context):
    instruction = f"""You are an expert prompt engineer. Improve the user's prompt while preserving its intent.

ORIGINAL PROMPT:
{original_prompt}

OBJECTIVE:
{objective}

ADDITIONAL CONTEXT:
{context if context.strip() else 'No additional context provided.'}

Requirements: improve clarity and specificity; add a suitable role, context, task, output format and constraints; avoid unsupported assumptions and fabricated facts.

Return these sections:
### Improved Prompt
### Improvements Made
### Why It Is Better
"""
    return generate_gemini_response(instruction)


def evaluate_prompt(prompt, objective):
    instruction = f"""You are a professional prompt quality evaluator. Evaluate this prompt objectively.

PROMPT:
{prompt}

INTENDED OBJECTIVE:
{objective}

Score each dimension from 1 to 10: Clarity, Context, Specificity, Task Definition and Output Format. Calculate the average score.

Return: Overall Score; Dimension Scores in a table; Strengths; Weaknesses; Recommendations; Final Verdict. Justify scores and do not inflate them.
"""
    return generate_gemini_response(instruction)


def generate_json_response(task, data):
    instruction = f"""You are an expert data processing assistant.

TASK:
{task}

INPUT DATA:
{data}

Return valid JSON only. Use meaningful keys and correct data types. Do not invent missing information; use null when information is unavailable. Do not include Markdown fences.
"""
    response = generate_gemini_response(instruction).strip()
    if response.startswith("```"):
        response = response.replace("```json", "", 1).replace("```", "").strip()
    try:
        return json.loads(response)
    except json.JSONDecodeError as exc:
        raise ValueError("The AI did not return valid JSON. Please try again.") from exc


def save_prompt_to_library(title, prompt, category, prompt_type):
    save_prompt(title, prompt, category, prompt_type)


# ============================================================
# SIDEBAR NAVIGATION
# ============================================================
with st.sidebar:
    st.markdown("<div class='sidebar-brand'>🚀 PromptLab</div>", unsafe_allow_html=True)
    st.caption("Your AI Prompt Engineering Workspace")
    st.divider()
    st.markdown("### WORKSPACE")
    st.radio(
        "Navigate to a workspace",
        options=list(PAGES.keys()),
        key="active_page",
        label_visibility="collapsed",
    )
    st.divider()
    st.markdown("### ABOUT PROMPTLAB")
    st.write("Create, improve, evaluate and organize prompts, then compare outputs from different AI models.")
    st.divider()
    st.markdown("### POWERED BY")
    st.markdown("🐍 Python  ·  🎨 Streamlit  \\n🤖 Gemini  ·  ⚡ Groq  \\n🗄️ SQLite")
    st.divider()
    st.caption("PromptLab v1.6 · Built for better AI interactions")

page = st.session_state.active_page


# ============================================================
# HOME DASHBOARD
# ============================================================
if page == "🏠 Home":
    left, right = st.columns([1.1, 0.9], gap="large", vertical_alignment="center")
    with left:
        st.markdown('<div class="hero-title">🚀 Welcome to PromptLab</div>', unsafe_allow_html=True)
        st.markdown('<div class="hero-subtitle">Your AI-Powered Prompt Engineering Workspace</div>', unsafe_allow_html=True)
        st.html("""
        <div class="qa-answer">
          <div class="answer-label">❓ WHAT IS PROMPTLAB?</div>
          <p>PromptLab is an AI-powered workspace that helps you <b>create, improve, evaluate and manage prompts</b>, while comparing responses from different AI models.</p>
          <p>Everything you need for better AI interactions in one place.</p>
        </div>
        """)
        st.markdown("**✨ Seven powerful tools. One AI workspace.**")
    with right:
        robot_html = """
        <!DOCTYPE html>
        <html>
        <head>
        <style>
            body {
                margin: 0;
                background: transparent;
                display: flex;
                justify-content: center;
                align-items: center;
                overflow: hidden;
            }
            svg {
                width: 100%;
                max-width: 440px;
                height: auto;
                filter: drop-shadow(0 0 25px #8b5cf666);
            }
        </style>
        </head>
        <body>
        <svg viewBox="0 0 420 350"
             xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="body" x1="0" y1="0" x2="1" y2="1">
                    <stop offset="0%" stop-color="#ffffff"/>
                    <stop offset="100%" stop-color="#a5a9ff"/>
                </linearGradient>
                <linearGradient id="screen" x1="0" y1="0" x2="1" y2="1">
                    <stop offset="0%" stop-color="#101b48"/>
                    <stop offset="100%" stop-color="#050817"/>
                </linearGradient>
            </defs>

            <ellipse cx="210" cy="320" rx="145" ry="17"
                     fill="#7044ff" opacity=".35"/>
            <circle cx="210" cy="155" r="125"
                    fill="#663cff" opacity=".12"/>

            <path d="M210 42 L210 19" stroke="#c4b5fd"
                  stroke-width="7" stroke-linecap="round"/>
            <circle cx="210" cy="14" r="10" fill="#38bdf8"/>

            <rect x="105" y="70" width="210" height="165"
                  rx="65" fill="url(#body)"
                  stroke="#c4b5fd" stroke-width="4"/>

            <rect x="130" y="105" width="160" height="100"
                  rx="42" fill="url(#screen)"
                  stroke="#8b5cf6" stroke-width="3"/>

            <path d="M165 150 Q180 125 195 150"
                  fill="none" stroke="#38bdf8"
                  stroke-width="9" stroke-linecap="round"/>
            <path d="M225 150 Q240 125 255 150"
                  fill="none" stroke="#38bdf8"
                  stroke-width="9" stroke-linecap="round"/>
            <path d="M184 172 Q210 194 236 172"
                  fill="none" stroke="#a78bfa"
                  stroke-width="5" stroke-linecap="round"/>

            <circle cx="103" cy="155" r="22"
                    fill="#8b5cf6" stroke="#c4b5fd" stroke-width="5"/>
            <circle cx="317" cy="155" r="22"
                    fill="#8b5cf6" stroke="#c4b5fd" stroke-width="5"/>

            <rect x="155" y="235" width="110" height="70"
                  rx="28" fill="url(#body)"
                  stroke="#c4b5fd" stroke-width="3"/>
            <rect x="177" y="250" width="66" height="40"
                  rx="16" fill="#111b45"/>
            <path d="M190 271 L205 282 L230 258"
                  fill="none" stroke="#38bdf8"
                  stroke-width="5" stroke-linecap="round"
                  stroke-linejoin="round"/>

            <path d="M110 245 L70 280"
                  stroke="#c4b5fd" stroke-width="22"
                  stroke-linecap="round"/>
            <circle cx="67" cy="282" r="17" fill="#dbe4ff"/>

            <path d="M310 245 L350 280"
                  stroke="#c4b5fd" stroke-width="22"
                  stroke-linecap="round"/>
            <circle cx="353" cy="282" r="17" fill="#dbe4ff"/>

            <rect x="105" y="280" width="210" height="12"
                  rx="6" fill="#8b5cf6" opacity=".5"/>

            <text x="45" y="85" font-size="25" fill="#c4b5fd">✦</text>
            <text x="350" y="110" font-size="28" fill="#38bdf8">✧</text>
            <text x="40" y="210" font-size="22" fill="#a78bfa">✦</text>
        </svg>
        </body>
        </html>
        """
        components.html(robot_html, height=390, scrolling=False)
    st.divider()
    st.markdown("## ✨ Explore Your Workspace")
    st.caption("Choose a tool to get started. Each workspace is designed for one clear task.")

    cards = [
        ("📝", "Prompt Builder", "Create structured prompts using roles, context, tasks and output formats.", "PROMPT CREATION", "📝 Prompt Builder"),
        ("✨", "Prompt Optimizer", "Turn rough instructions into clearer, more useful prompts.", "AI OPTIMIZATION", "✨ Prompt Optimizer"),
        ("📊", "Prompt Evaluator", "Score prompt quality across five important dimensions.", "QUALITY ANALYSIS", "📊 Prompt Evaluator"),
        ("⚖️", "Model Comparison", "Send the same prompt to Gemini and Groq and compare the answers.", "MULTI-MODEL AI", "⚖️ Model Comparison"),
        ("🕘", "Prompt History", "Search, review, download or remove prompts saved in your database.", "PROMPT MANAGEMENT", "🕘 Prompt History"),
        ("📚", "Prompt Library", "Keep useful prompts organized and ready to reuse.", "SAVED PROMPTS", "📚 Prompt Library"),
        ("🔧", "JSON Generator", "Convert instructions and raw information into structured JSON.", "STRUCTURED OUTPUT", "🔧 JSON Generator"),
    ]
    for row_start in range(0, len(cards), 3):
        columns = st.columns(3)
        for col, card in zip(columns, cards[row_start:row_start + 3]):
            icon, title, description, label, target = card
            with col:
                st.markdown(
                    f"<div class='feature-card'><div class='feature-icon'>{icon}</div><div class='feature-title'>{title}</div><div class='feature-description'>{description}</div><span class='feature-label'>{label}</span></div>",
                    unsafe_allow_html=True,
                )
                if st.button(f"Open {title} →", key=f"open_{target}", use_container_width=True):
                    go_to(target)
                    st.rerun()


# ============================================================
# PROMPT BUILDER
# ============================================================
elif page == "📝 Prompt Builder":
    page_heading("📝", "Prompt Builder", "Build a clear, reusable AI instruction from a role, context, task and output format.")
    with st.container(border=True):
        st.markdown("#### 1. Define your prompt")
        role = st.text_input("AI role", "Act as a senior business data analyst", help="Tell the AI what kind of expert it should act as.", key="builder_role")
        context = st.text_area("Context", placeholder="Describe the situation, audience, data or background...", height=120, key="builder_context")
        task = st.text_area("Task", placeholder="What exactly should the AI accomplish?", height=120, key="builder_task")
        output_format = st.selectbox("Preferred output format", ["Structured report", "Bullet points", "Table", "Executive summary", "Step-by-step explanation", "JSON"], key="builder_format")
        if st.button("✨ Generate prompt", type="primary", key="builder_button"):
            if not context.strip() or not task.strip():
                st.warning("Please provide both context and task.")
            else:
                st.session_state.generated_prompt = build_prompt(role, context, task, output_format)
                st.session_state.builder_response = ""
                st.success("Your prompt is ready.")
    if st.session_state.generated_prompt:
        with st.container(border=True):
            result_panel("2. Your generated prompt", st.session_state.generated_prompt, "generated_prompt.txt", "download_builder")
            save_title = st.text_input("Give this prompt a title", "My Generated Prompt", key="builder_save_title")
            a, b = st.columns(2)
            with a:
                if st.button("📚 Save to library", key="save_builder", use_container_width=True):
                    try:
                        save_prompt_to_library(save_title, st.session_state.generated_prompt, "General", "Generated")
                        st.success("Prompt saved to your library.")
                    except Exception as error:
                        st.error(f"Could not save prompt: {error}")
            with b:
                provider = st.selectbox("Run with", ["Gemini", "Groq"], key="builder_provider")
                if st.button("▶ Run prompt", key="builder_run", type="primary", use_container_width=True):
                    try:
                        with st.spinner(f"Generating with {provider}..."):
                            st.session_state.builder_response = generate_response(st.session_state.generated_prompt, provider)
                    except Exception as error:
                        st.error(f"API request failed: {error}")
            if st.session_state.builder_response:
                st.markdown("#### 3. AI response")
                st.markdown(st.session_state.builder_response)


# ============================================================
# PROMPT OPTIMIZER
# ============================================================
elif page == "✨ Prompt Optimizer":
    page_heading("✨", "Prompt Optimizer", "Improve a rough prompt while keeping its original intention.")
    with st.container(border=True):
        original_prompt = st.text_area("Original prompt", placeholder="Example: Analyze my sales data.", height=150, key="optimizer_input")
        objective = st.text_input("What result do you want?", placeholder="Example: Identify sales trends and business opportunities.", key="optimizer_objective")
        additional_context = st.text_area("Additional context (optional)", placeholder="Add relevant background, audience or constraints...", height=100, key="optimizer_context")
        if st.button("✨ Optimize my prompt", type="primary", key="optimizer_button"):
            if not original_prompt.strip() or not objective.strip():
                st.warning("Enter the original prompt and the intended objective.")
            else:
                try:
                    with st.spinner("Analyzing and improving your prompt..."):
                        st.session_state.optimized_result = optimize_prompt(original_prompt, objective, additional_context)
                    st.session_state.original_prompt = original_prompt
                    st.success("Optimization complete.")
                except Exception as error:
                    st.error(f"Optimization failed: {error}")
    if st.session_state.optimized_result:
        first, second = st.columns(2)
        with first:
            with st.container(border=True):
                st.markdown("#### Original prompt")
                st.write(st.session_state.original_prompt)
        with second:
            with st.container(border=True):
                st.markdown("#### Improved result")
                st.success("A refined prompt is ready")
        with st.container(border=True):
            st.markdown("#### Optimization report")
            st.markdown(st.session_state.optimized_result)
            st.download_button("⬇️ Download optimized result", st.session_state.optimized_result, "optimized_prompt.txt", key="download_optimizer")


# ============================================================
# PROMPT EVALUATOR
# ============================================================
elif page == "📊 Prompt Evaluator":
    page_heading("📊", "Prompt Evaluator", "Understand how strong your prompt is and what to improve next.")
    with st.container(border=True):
        evaluation_prompt = st.text_area("Prompt to evaluate", placeholder="Paste the complete prompt you want to assess...", height=180, key="evaluation_input")
        evaluation_objective = st.text_input("Intended objective", placeholder="What should this prompt accomplish?", key="evaluation_objective")
        if st.button("📊 Evaluate prompt", type="primary", key="evaluator_button"):
            if not evaluation_prompt.strip() or not evaluation_objective.strip():
                st.warning("Enter a prompt and its intended objective.")
            else:
                try:
                    with st.spinner("Evaluating clarity, context and structure..."):
                        st.session_state.evaluation_result = evaluate_prompt(evaluation_prompt, evaluation_objective)
                    st.success("Evaluation report generated.")
                except Exception as error:
                    st.error(f"Evaluation failed: {error}")
    if st.session_state.evaluation_result:
        with st.container(border=True):
            st.markdown("#### Your evaluation report")
            st.markdown(st.session_state.evaluation_result)
            st.download_button("⬇️ Download evaluation", st.session_state.evaluation_result, "prompt_evaluation.txt", key="download_evaluator")


# ============================================================
# MODEL COMPARISON
# ============================================================
elif page == "⚖️ Model Comparison":
    page_heading("⚖️", "Model Comparison", "Compare two model responses to the exact same instruction.")
    with st.container(border=True):
        comparison_prompt = st.text_area("Prompt for both models", placeholder="Example: Explain how AI can improve customer support.", height=170, key="comparison_input")
        st.caption("The same prompt is sent to Gemini and Groq so you can compare their responses.")
        if st.button("⚖️ Compare models", type="primary", key="comparison_button"):
            if not comparison_prompt.strip():
                st.warning("Please enter a prompt.")
            else:
                try:
                    with st.spinner("Waiting for Gemini and Groq..."):
                        st.session_state.comparison_gemini = generate_gemini_response(comparison_prompt)
                        st.session_state.comparison_groq = generate_groq_response(comparison_prompt)
                    st.session_state.comparison_original_prompt = comparison_prompt
                    st.success("Both responses are ready.")
                except Exception as error:
                    st.error(f"Model comparison failed: {error}")
    if st.session_state.comparison_gemini or st.session_state.comparison_groq:
        st.markdown("#### Side-by-side results")
        left, right = st.columns(2)
        with left:
            with st.container(border=True):
                st.subheader("💎 Gemini")
                st.markdown(st.session_state.comparison_gemini or "No Gemini response available.")
                if st.session_state.comparison_gemini:
                    st.download_button("Download Gemini response", st.session_state.comparison_gemini, "gemini_response.txt", key="download_gemini")
        with right:
            with st.container(border=True):
                st.subheader("⚡ Groq")
                st.markdown(st.session_state.comparison_groq or "No Groq response available.")
                if st.session_state.comparison_groq:
                    st.download_button("Download Groq response", st.session_state.comparison_groq, "groq_response.txt", key="download_groq")


# ============================================================
# PROMPT HISTORY
# ============================================================
elif page == "🕘 Prompt History":
    page_heading("🕘", "Prompt History", "Search and manage prompts stored in your PromptLab database.")
    query = st.text_input("Search history", placeholder="Search by prompt title or content...", key="history_search")
    try:
        prompts = search_prompts(query) if query.strip() else get_all_prompts()
        st.caption(f"{len(prompts)} saved prompt(s)")
        if prompts:
            for item in prompts:
                prompt_id, title, content, category, prompt_type, created_at = item
                with st.expander(f"📄 {title}  ·  {created_at}"):
                    st.caption(f"{category}  ·  {prompt_type}")
                    st.code(content, language="text")
                    c1, c2 = st.columns(2)
                    with c1:
                        st.download_button("⬇️ Download", content, f"{title}.txt", key=f"history_download_{prompt_id}", use_container_width=True)
                    with c2:
                        if st.button("🗑️ Delete", key=f"history_delete_{prompt_id}", use_container_width=True):
                            delete_prompt(prompt_id)
                            st.success("Prompt deleted.")
                            st.rerun()
        else:
            st.info("No saved prompts found yet. Save a prompt from Prompt Builder to see it here.")
    except Exception as error:
        st.error(f"Could not load prompt history: {error}")


# ============================================================
# PROMPT LIBRARY
# ============================================================
elif page == "📚 Prompt Library":
    page_heading("📚", "Prompt Library", "A reusable collection of prompts you have saved.")
    query = st.text_input("Search your library", placeholder="Search by title or keyword...", key="library_search")
    try:
        prompts = search_prompts(query) if query.strip() else get_all_prompts()
        metric_col, _ = st.columns([1, 3])
        metric_col.metric("Saved prompts", len(prompts))
        if prompts:
            for item in prompts:
                prompt_id, title, content, category, prompt_type, created_at = item
                with st.expander(f"📚 {title}"):
                    st.caption(f"{category}  ·  {prompt_type}  ·  {created_at}")
                    st.code(content, language="text")
                    c1, c2 = st.columns(2)
                    with c1:
                        st.download_button("⬇️ Download prompt", content, f"{title}.txt", key=f"library_download_{prompt_id}", use_container_width=True)
                    with c2:
                        if st.button("🗑️ Remove from library", key=f"library_delete_{prompt_id}", use_container_width=True):
                            delete_prompt(prompt_id)
                            st.success("Prompt removed.")
                            st.rerun()
        else:
            st.info("Your library is empty. Create a prompt and save it from Prompt Builder.")
    except Exception as error:
        st.error(f"Could not load prompt library: {error}")


# ============================================================
# JSON GENERATOR
# ============================================================
elif page == "🔧 JSON Generator":
    page_heading("🔧", "Structured JSON Generator", "Turn plain-language instructions and source information into valid JSON.")
    with st.container(border=True):
        json_task = st.text_input("What should the AI extract or create?", placeholder="Analyze customer feedback and identify sentiment, product and main issue.", key="json_task")
        json_data = st.text_area("Input data", placeholder="Paste the text or information to structure...", height=170, key="json_data")
        if st.button("🔧 Generate JSON", type="primary", key="json_button"):
            if not json_task.strip() or not json_data.strip():
                st.warning("Please provide both an instruction and input data.")
            else:
                try:
                    with st.spinner("Converting your information into JSON..."):
                        st.session_state.json_result = generate_json_response(json_task, json_data)
                    st.success("Valid JSON generated.")
                except Exception as error:
                    st.error(f"JSON generation failed: {error}")
    if st.session_state.json_result is not None:
        formatted_json = json.dumps(st.session_state.json_result, indent=4, ensure_ascii=False)
        with st.container(border=True):
            st.markdown("#### Generated JSON")
            st.json(st.session_state.json_result)
            st.download_button("⬇️ Download JSON", formatted_json, "generated_data.json", mime="application/json", key="download_json")


# ============================================================
# FOOTER
# ============================================================
st.divider()
st.markdown(
    "<div class='app-footer'><strong>🚀 PromptLab</strong><br>Better prompts. Better AI interactions.<br><small>Python · Streamlit · Gemini · Groq · SQLite</small></div>",
    unsafe_allow_html=True,
)
