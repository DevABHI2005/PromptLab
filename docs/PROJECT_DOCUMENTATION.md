# PromptLab
## AI-Powered Prompt Engineering Workspace

**Project Type:** Generative AI Application  
**Version:** 1.6  
**Status:** Core features implemented and manually tested  
**Repository:** https://github.com/DevABHI2005/PromptLab  
**Technologies:** Python, Streamlit, Google Gemini API, Groq API, SQLite

---

# 1. Project Overview

PromptLab is an AI-powered prompt engineering workspace designed to help users create, optimize, evaluate, compare, and manage prompts using different large language models.

It provides seven tools in a single application:

1. Prompt Builder
2. Prompt Optimizer
3. Prompt Evaluator
4. Model Comparison
5. Prompt History
6. Prompt Library
7. Structured JSON Generator

The application provides a centralized interface for working with AI prompts instead of requiring users to perform each task manually across separate AI platforms.

Its purpose is to make interactions with AI models more structured, understandable, reusable, and efficient.

# 2. Problem Statement

Generative AI tools are increasingly used for education, software development, business analysis, research, content creation, and automation.

However, the quality of an AI response depends significantly on the quality of the prompt provided by the user.

Many users face the following problems:

- They do not know how to write clear and structured prompts.
- Their prompts often lack sufficient context, instructions, or output requirements.
- They cannot easily determine whether a prompt is effective.
- They have difficulty comparing responses from different AI models.
- Useful prompts are often lost because they are not organized or saved.
- Converting unstructured information into structured JSON requires additional manual work.
- Users need to switch between different AI tools to complete these activities.

**Core problem:** There is no single, simple workspace in this project context that brings prompt creation, improvement, evaluation, model comparison, prompt management, and structured output generation together.

# 3. Why I Built PromptLab

I developed PromptLab to understand how generative AI can be integrated into practical software applications.

The project was created to:

1. Understand prompt engineering through practical implementation.
2. Integrate multiple AI providers into one application.
3. Explore how different models respond to the same instructions.
4. Build useful AI-powered features rather than only experimenting with chat interfaces.
5. Learn how to store and manage application data using SQLite.
6. Develop a professional user interface using Streamlit and CSS.
7. Build a project that demonstrates practical AI development skills in a portfolio.

The project also helped me understand how individual AI capabilities can be combined into a complete application.

# 4. Proposed Solution

PromptLab addresses the identified problems through a unified AI workspace.

| Problem | PromptLab solution |
|---|---|
| Difficulty writing prompts | Prompt Builder |
| Poorly structured prompts | Prompt Optimizer |
| Uncertainty about prompt quality | Prompt Evaluator |
| Difficulty comparing models | Model Comparison |
| Losing useful prompts | Prompt History |
| Difficulty organizing reusable prompts | Prompt Library |
| Manual conversion into JSON | Structured JSON Generator |

Instead of using separate tools for each activity, users can access all seven features through one dashboard.

# 5. Features and Detailed Functionality

## 5.1 Prompt Builder

**Purpose:** Create structured prompts using user-provided information.

The user provides:

- AI role
- Context
- Task
- Preferred output format

The application combines these inputs into a structured prompt.

The generated prompt follows this structure:

```text
ROLE:
[Define the AI's role]

CONTEXT:
[Provide relevant background]

TASK:
[Describe what the AI should accomplish]

OUTPUT FORMAT:
[Specify the expected response format]

IMPORTANT:
Do not invent facts.
Clearly identify assumptions.
```

Available output formats include:

- Structured report
- Bullet points
- Table
- Executive summary
- Step-by-step explanation
- JSON

**Additional functionality:**

- Download generated prompts.
- Save generated prompts to the library.
- Run the generated prompt using Gemini or Groq.
- View the AI-generated response.

**Problem solved:** Helps users transform incomplete instructions into organized prompts.

## 5.2 Prompt Optimizer

**Purpose:** Improve an existing prompt without changing its original intention.

The user provides:

- Original prompt
- Intended objective
- Additional context (optional)

The application sends these details to Gemini with prompt optimization instructions.

The AI returns:

1. Improved Prompt
2. Improvements Made
3. Why It Is Better

The optimizer focuses on improving clarity, specificity, context, task definition, output format, and constraints.

**Problem solved:** Helps users improve vague or poorly structured prompts.

## 5.3 Prompt Evaluator

**Purpose:** Assess the quality of a prompt.

The user provides:

- Prompt to evaluate
- Intended objective

Gemini evaluates the prompt using five dimensions.

| Evaluation dimension | What it measures |
|---|---|
| Clarity | Whether the instruction is understandable |
| Context | Whether sufficient background is provided |
| Specificity | Whether the requirements are sufficiently detailed |
| Task Definition | Whether the expected task is clearly explained |
| Output Format | Whether the expected response format is specified |

Each dimension receives a score from 1 to 10.

The application requests an overall average score, strengths, weaknesses, recommendations, and a final verdict.

The evaluation report can be downloaded.

**Important:** These are AI-generated assessments, not independently validated benchmark scores.

**Problem solved:** Helps users identify weaknesses in their prompts and understand what can be improved.

## 5.4 Model Comparison

**Purpose:** Compare the responses generated by two different AI providers.

The application integrates:

- Google Gemini
- Groq

The user enters one prompt. The application sends the same prompt to both providers.

The responses are displayed side by side.

Users can compare:

- Accuracy
- Clarity
- Completeness
- Explanation quality
- Relevance
- Response structure

Both responses can be downloaded separately.

**Problem solved:** Makes it easier to explore how different AI models respond to identical instructions.

**Current limitation:** PromptLab displays the responses side by side but does not yet calculate automated performance, latency, or token-cost comparisons.

## 5.5 Prompt History

**Purpose:** Access previously saved prompts.

The feature uses SQLite to retrieve stored prompt records.

Users can:

- View saved prompts.
- Search by title, content, or category.
- Download individual prompts.
- Delete unwanted prompts.
- Review creation timestamps.

**Problem solved:** Reduces the chance of losing useful prompts.

## 5.6 Prompt Library

**Purpose:** Maintain a reusable collection of prompts.

The library allows users to browse saved prompts, search by keywords, view their contents, download them, and remove unwanted entries.

The current implementation uses the same SQLite prompt records as Prompt History.

The distinction is primarily in how the two pages present and manage the saved prompts, rather than separate database storage systems.

**Problem solved:** Makes useful prompts easier to find and reuse.

## 5.7 Structured JSON Generator

**Purpose:** Convert instructions and unstructured input information into structured JSON.

The user provides:

- Task or extraction instruction
- Input data

Gemini generates a JSON response.

The application then attempts to parse the response using Python's `json.loads()`.

If the output is invalid JSON, the application displays an error.

The user can view the generated JSON and download it as a `.json` file.

The application instructs the model to use meaningful keys, correct data types, and `null` when information is unavailable.

**Problem solved:** Reduces manual effort when transforming unstructured information into structured data.

# 6. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Streamlit | Web application framework |
| Google Gemini API | AI prompt optimization, evaluation, JSON generation and prompt execution |
| Groq API | Alternative AI response generation |
| SQLite | Local database for saved prompts |
| HTML | Custom interface elements |
| CSS | Styling and visual design |
| Git | Version control |
| GitHub | Source code hosting and project management |
| python-dotenv | Loading local environment variables |

## Why these technologies?

**Python:** Provides a straightforward way to integrate AI APIs, process information, and build application logic.

**Streamlit:** Allows interactive Python applications to be developed without building a separate frontend and backend.

**Gemini:** Provides the primary AI generation functionality in PromptLab.

**Groq:** Adds another AI provider, allowing users to compare model responses.

**SQLite:** Provides lightweight local database storage without requiring a separate database server.

**Git and GitHub:** Help track changes, maintain source code, and demonstrate the project publicly.

# 7. System Architecture

PromptLab follows a simple modular architecture.

```text
                 USER
                   |
                   v
          STREAMLIT INTERFACE
                   |
                   v
             APP.PY
                   |
        +----------+----------+
        |          |          |
        v          v          v
   PROMPT       AI MODEL    DATABASE
  TEMPLATES     PROVIDERS    MODULE
        |          |          |
        |       +--+--+       |
        |       |     |       |
        |       v     v       |
        |    GEMINI  GROQ     |
        |       |     |       |
        +-------+-----+-------+
                   |
                   v
             USER RESULTS
```

### Architecture explanation

1. The user interacts with the Streamlit interface.
2. `app.py` handles navigation, inputs, application logic, and output display.
3. Prompt templates construct structured prompts.
4. The AI provider module communicates with Gemini and Groq.
5. The database module stores and retrieves saved prompts.
6. The application displays the generated results and provides download options.

# 8. Project Folder Structure

The repository currently contains the following documented structure:

```text
PromptLab/
│
├── app.py
│
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
│
├── assets/
│   └── style.css
│
└── utils/
    ├── ai_providers.py
    ├── database.py
    └── prompt_templates.py
```

### Explanation of each file

**app.py**

The main application file.

Responsibilities:

- Streamlit page configuration.
- Sidebar navigation.
- Dashboard and feature cards.
- User input collection.
- Prompt generation and optimization.
- Prompt evaluation.
- Model comparison.
- JSON generation.
- Database operations.
- Result display and downloads.

**utils/ai_providers.py**

Handles AI provider integration.

It contains:

- `generate_gemini_response(prompt)`
- `generate_groq_response(prompt)`

It reads API keys and model configuration from environment variables and sends requests to the respective providers.

**utils/database.py**

Handles SQLite database operations.

It contains:

- `get_connection()`
- `initialize_database()`
- `save_prompt()`
- `get_all_prompts()`
- `search_prompts()`
- `delete_prompt()`

**utils/prompt_templates.py**

Contains the `build_prompt()` function, which combines role, context, task, and output format into a structured prompt.

**assets/style.css**

Contains the custom styling for the application, including:

- Dark theme
- Typography
- Buttons
- Input fields
- Sidebar
- Feature cards
- Hero section
- Responsive styling

**requirements.txt**

Lists the Python dependencies needed to run the application.

**.env.example**

Provides an example configuration file without real API credentials.

**.gitignore**

Prevents sensitive and unnecessary files from being included in Git commits.

# 9. Database Design

PromptLab uses SQLite.

The database filename is:

```text
promptlab.db
```

The application initializes a table named `prompts`.

### Database table: prompts

| Column | Data type | Description |
|---|---|---|
| id | INTEGER | Primary key |
| title | TEXT | Prompt title |
| prompt | TEXT | Complete prompt content |
| category | TEXT | Prompt category |
| prompt_type | TEXT | Type of prompt |
| created_at | TEXT | Date and time of creation |

### Database operations

**Create:** Save a new prompt.

**Read:** Retrieve all saved prompts.

**Search:** Search by title, prompt content, or category.

**Delete:** Remove a prompt using its ID.

The application uses parameterized SQL queries for inserting, searching, and deleting records.

### Current database limitation

The database is local to the application environment. It is suitable for local development, but cloud deployment requires a persistence strategy so that saved prompts are not lost when the hosting environment restarts or changes.

# 10. AI Integration Workflow

## Gemini workflow

1. The user selects a feature that requires Gemini.
2. The application prepares the appropriate instruction.
3. `generate_gemini_response()` retrieves the Gemini API key and model configuration.
4. The Google Gen AI client sends the request.
5. Gemini generates a response.
6. PromptLab displays the response.

## Groq workflow

1. The user selects Groq or opens Model Comparison.
2. PromptLab prepares the user prompt.
3. `generate_groq_response()` retrieves the Groq API key and model configuration.
4. The Groq client sends the request.
5. Groq generates a response.
6. PromptLab displays the response.

## Configuration variables

The provider module uses these environment variables:

```env
GEMINI_API_KEY=your_gemini_key
GEMINI_MODEL=your_gemini_model

GROQ_API_KEY=your_groq_key
GROQ_MODEL=your_groq_model
```

Never publish real API keys in GitHub.

# 11. User Interface and Design

PromptLab uses a dark, modern SaaS-inspired interface.

### Design elements

- Dark navy background.
- Purple and blue gradient accents.
- Sidebar navigation.
- Welcome dashboard.
- Custom robot illustration.
- Seven feature cards.
- Consistent buttons and input fields.
- Responsive layouts.

### Main dashboard

The homepage contains:

1. PromptLab branding.
2. Welcome message.
3. Explanation of what PromptLab does.
4. Robot illustration.
5. Seven feature cards.
6. Navigation buttons.

The dashboard provides direct access to each workspace.

### Navigation

Users can navigate using either:

- Sidebar navigation.
- Feature cards on the home dashboard.

# 12. How the Project Was Developed

The project was developed incrementally.

### Phase 1: Initial setup

- Created the PromptLab GitHub repository.
- Cloned the repository locally.
- Created a Python virtual environment.
- Installed the required packages.
- Configured environment variables.
- Created the initial Streamlit application.
- Tested the initial AI connection.

### Phase 2: Core prompt engineering features

- Developed the Prompt Builder.
- Added the Prompt Optimizer.
- Added the Prompt Evaluator.
- Integrated Gemini and Groq.

### Phase 3: Advanced functionality

- Added Model Comparison.
- Implemented Prompt History.
- Created the Prompt Library.
- Added the Structured JSON Generator.
- Integrated SQLite operations.

### Phase 4: User interface development

- Created the dark theme.
- Added custom CSS.
- Designed the homepage.
- Added the robot illustration.
- Created feature cards.
- Implemented sidebar navigation.
- Improved individual workspace layouts.

### Phase 5: Testing and GitHub integration

- Tested navigation.
- Tested prompt generation.
- Tested AI provider integration.
- Tested optimization and evaluation.
- Tested JSON generation.
- Tested database save, search, download, and delete.
- Updated project documentation.
- Pushed the final changes to GitHub.

# 13. Testing and Validation

The following functionality was manually tested and reported as working during development.

| Test | Expected result | Reported status |
|---|---|---|
| Homepage loading | Dashboard appears correctly | Passed |
| Sidebar navigation | Opens selected workspace | Passed |
| Feature-card navigation | Opens corresponding workspace | Passed |
| Prompt Builder | Generates structured prompt | Passed |
| Prompt Optimizer | Generates improved prompt | Passed |
| Prompt Evaluator | Generates evaluation report | Passed |
| Gemini integration | Generates AI response | Passed |
| Groq integration | Generates AI response | Passed |
| Model Comparison | Displays both model responses | Passed |
| Database save | Saves prompt record | Passed |
| Database search | Finds saved prompts | Passed |
| Database download | Downloads saved prompt | Passed |
| Database delete | Deletes selected prompt | Passed |
| JSON Generator | Generates and parses JSON | Passed |

**Testing note:** These are manual development test results reported during the project work. An automated test suite, performance benchmark, security audit, and production deployment test have not been established in the current project documentation.

# 14. Security Considerations

PromptLab uses external AI providers, so API credentials must be protected.

Current security measures include:

- `.env` for local credentials.
- `.env.example` for configuration examples.
- `.gitignore` excludes `.env`.
- `.gitignore` excludes local database files.
- API credentials are not hardcoded into the application source.

Additional precautions:

1. Revoke any API key that was previously exposed.
2. Generate replacement keys where necessary.
3. Never upload `.env` to GitHub.
4. Never include API keys in screenshots or project documentation.
5. Configure cloud secrets separately before deployment.
6. Avoid entering confidential or sensitive business data into a public demo.

# 15. Current Limitations

PromptLab is a functional learning and portfolio project, but it is not yet a production-grade enterprise application.

Current limitations include:

1. No user registration or authentication.
2. No role-based access control.
3. SQLite is designed for local persistence rather than a multi-user cloud environment.
4. No automated prompt benchmarking.
5. No automatic comparison of token usage, latency, or API costs.
6. Prompt optimization, evaluation, and JSON generation currently use Gemini.
7. Model comparison is limited to Gemini and Groq.
8. No automated test suite is included in the documented project structure.
9. No production monitoring or analytics.
10. No explicit privacy or data-retention controls for multiple users.

These limitations provide opportunities for future development.

# 16. Future Enhancements

Potential improvements for future versions:

### AI capabilities

- Add OpenAI API integration.
- Add more model providers.
- Add model response scoring.
- Add response latency measurement.
- Add token usage and cost estimation.
- Add prompt versioning.
- Add prompt templates for business, coding, research, and data analytics.

### Application functionality

- User authentication.
- Individual user prompt libraries.
- Prompt categories and tags.
- Prompt editing.
- Bulk prompt export.
- Prompt sharing.
- Advanced search and filtering.
- Prompt testing with multiple inputs.

### Technical improvements

- Automated unit and integration tests.
- Better exception handling.
- Logging and monitoring.
- PostgreSQL or a managed database for cloud persistence.
- Deployment secrets management.
- Rate limiting and usage controls.

# 17. Deployment Decision

## Should PromptLab be deployed or remain local?

**Recommendation: Do both.**

Keep the local development environment and deploy a public demonstration version.

### Local hosting

Advantages:

- Complete control over development.
- Easier debugging.
- No public access to the application.
- Suitable for experimentation.
- Local SQLite database works naturally.

Disadvantages:

- Other people cannot access the application unless you share your machine or expose a server.
- You cannot easily demonstrate a live application to recruiters.

### Cloud deployment

Advantages:

- Recruiters can access the project using a URL.
- You can demonstrate the working application.
- It strengthens your portfolio.
- It makes sharing and testing easier.

Disadvantages:

- API keys must be configured securely.
- Cloud storage and database persistence need attention.
- Public users can consume API quota.
- The application needs appropriate usage and privacy controls.

## Recommended hosting platform: Streamlit Community Cloud

Streamlit Community Cloud is a suitable first hosting option because PromptLab is already built using Streamlit.

It supports connecting GitHub repositories and deploying Streamlit applications. The service offers a free hosting option. See the official deployment documentation:

https://docs.streamlit.io/deploy/streamlit-community-cloud

### Deployment-readiness tasks

Before deploying, complete these improvements:

**1. Update secrets handling**

Your current provider module reads credentials through environment variables and `python-dotenv`.

Streamlit Community Cloud provides a secrets-management interface. Update the provider configuration to read secrets safely from `st.secrets` in the cloud while continuing to support `.env` locally.

Official guide:

https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management

**2. Configure both AI providers**

Add the required Gemini and Groq credentials and model settings to the deployment secrets.

**3. Review SQLite persistence**

The current database is a local `promptlab.db` file. Do not assume that local SQLite data will persist reliably in a cloud deployment.

For a public multi-user version, consider a managed database such as PostgreSQL or another persistent database service.

**4. Protect API usage**

Add usage limits or other controls before allowing unrestricted public access.

**5. Test the deployed version**

Check all seven workspaces, AI provider calls, error handling, downloads, and database operations after deployment.

### Deployment procedure

1. Open https://share.streamlit.io/
2. Sign in using GitHub.
3. Connect your GitHub account.
4. Select Create app.
5. Select the `DevABHI2005/PromptLab` repository.
6. Choose the `main` branch.
7. Set the application entrypoint to `app.py`.
8. Configure the required secrets.
9. Deploy the application.
10. Test the live URL.

Official deployment instructions:

https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy

**Deployment status:** Not yet deployed. The steps above are the recommended next stage, not completed work.

# 18. How to Run PromptLab Locally

### Prerequisites

- Python installed.
- Git installed.
- Gemini API key.
- Groq API key.

### Step 1: Clone the repository

```bash
git clone https://github.com/DevABHI2005/PromptLab.git
```

### Step 2: Enter the project directory

```bash
cd PromptLab
```

### Step 3: Create a virtual environment

```bash
python -m venv .venv
```

### Step 4: Activate it on Windows

```bash
.venv\Scripts\activate
```

### Step 5: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 6: Configure environment variables

Create a `.env` file in the project root and add the required Gemini and Groq configuration variables.

Use `.env.example` as a reference. Do not upload your actual `.env` file.

### Step 7: Run the application

```bash
streamlit run app.py
```

The application will open in your browser using the local Streamlit address.

# 19. Skills Demonstrated

This project demonstrates practical experience with:

- Python application development.
- Generative AI integration.
- Prompt engineering.
- API integration.
- Multiple AI provider management.
- Streamlit application development.
- SQLite database operations.
- SQL queries and CRUD operations.
- JSON processing.
- HTML and CSS customization.
- User interface design.
- Git and GitHub.
- Environment variable management.
- Application testing and debugging.

# 20. Project Conclusion

PromptLab was developed to solve a practical problem in generative AI usage: creating effective prompts and managing interactions with different AI models.

The application combines seven useful prompt engineering tools into one workspace.

Through this project, I gained practical experience in connecting AI models to Python applications, building interactive interfaces, managing persistent data, and organizing a software project for GitHub.

PromptLab represents my first complete AI-powered application in this learning journey and provides a foundation for future projects involving AI development and agentic systems.

**Project tagline:**

> Better prompts. Better AI interactions.

---

# 21. Project Status and Next Steps

| Area | Current status |
|---|---|
| Core application | Completed |
| Seven feature workspaces | Implemented |
| Gemini integration | Implemented |
| Groq integration | Implemented |
| SQLite storage | Implemented |
| Custom UI | Implemented |
| Manual functionality testing | Reported passed |
| GitHub repository | Updated |
| Detailed documentation | Prepared |
| Automated test suite | Future improvement |
| Cloud-ready secrets handling | To do |
| Persistent cloud database | To do |
| Public deployment | To do |

**Final recommendation:** Preserve the current working version, complete deployment-readiness changes, and publish a demo using Streamlit Community Cloud. Continue to use GitHub for source code and version history, and keep this detailed document updated as the application evolves.
