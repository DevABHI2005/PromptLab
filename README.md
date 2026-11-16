# 🚀 PromptLab – AI Prompt Engineering Workspace

PromptLab is an AI-powered workspace designed to help users create, optimize, evaluate and manage prompts while comparing responses from different AI models.

## ✨ Features

- **Prompt Builder:** Create structured prompts using roles, context, tasks and output formats.
- **Prompt Optimizer:** Improve existing prompts using AI.
- **Prompt Evaluator:** Evaluate prompt quality across five dimensions.
- **Model Comparison:** Compare responses from Google Gemini and Groq.
- **Prompt History:** Search, view and download saved prompts.
- **Prompt Library:** Store and manage reusable prompts.
- **JSON Generator:** Generate structured JSON from instructions and input data.

## 🛠️ Technologies Used

- Python
- Streamlit
- Google Gemini API
- Groq API
- SQLite
- Git and GitHub

## ⚙️ Installation

1. Clone the repository:

   `git clone YOUR_GITHUB_REPOSITORY_URL`

2. Navigate into the project:

   `cd PromptLab`

3. Create a virtual environment:

   `python -m venv .venv`

4. Activate it on Windows:

   `.venv\Scripts\activate`

5. Install dependencies:

   `pip install -r requirements.txt`

6. Create a `.env` file using `.env.example` as a reference.

7. Add your API keys and required model settings to `.env`. Never publish API keys.

8. Start the application:

   `streamlit run app.py`

## 📁 Project Structure

```text
PromptLab/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── assets/
│   └── style.css
├── utils/
│   ├── ai_providers.py
│   ├── database.py
│   └── prompt_templates.py
└── README.md
```

## 🔐 Security

- Store API keys in your local `.env` file.
- Never commit `.env` or expose API credentials.
- Use `.env.example` to document required environment variables without real secrets.

## 🎯 Project Goal

To build a practical AI prompt engineering workspace that demonstrates prompt design, AI integration, model comparison, structured outputs and data persistence.

---

**Built with Python, Streamlit, Gemini and Groq.**