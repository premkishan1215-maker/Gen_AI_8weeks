# 📄 AI Bulk Resume Evaluator

An intelligent, automated resume screening and evaluation platform powered by **Groq** and **Large Language Models (LLMs)**. This application parses multiple resumes in bulk (PDF and DOCX formats), analyzes them against a target job description, provides structured candidate match scores, extracts key strengths, weaknesses, matched/missing skills, and outputs actionable candidate insights with CSV export capabilities.

---

## 🚀 Key Features

- **📂 Bulk Resume Processing**: Upload and evaluate multiple resumes simultaneously in `.pdf` and `.docx` formats.
- **⚡ High-Speed LLM Inference**: Powered by **Groq** (`openai/gpt-oss-120b`) for rapid, accurate analysis with deterministic temperature settings.
- **🎯 Structured Pydantic Output**: Strictly enforced JSON schema validation ensuring complete, consistent evaluation metrics:
  - Overall Match Score (0–100%)
  - Matched Skills & Missing Skills
  - Candidate Strengths & Weaknesses
  - Actionable Improvement Suggestions
  - Executive Candidate Summary
- **📊 Interactive Streamlit Dashboard**:
  - Live progress tracking and batch request throttling (built-in delay to stay within API rate limits).
  - Leaderboard ranking top candidate matches.
  - Drill-down expandable panels for each applicant with visual score metrics.
- **📥 One-Click CSV Export**: Download the comprehensive evaluation report formatted for spreadsheet tools like Microsoft Excel or Google Sheets.
- **🛡️ Objective & Hallucination-Free**: Prompt engineering strictly instructs the model to evaluate only documented evidence without inventing experience.
- **💻 CLI & Web Interfaces**: Run either as a full-featured Streamlit web application or a headless Python script for quick testing.

---

## 🛠️ Tech Stack & Dependencies

- **Language**: Python 3.13+
- **Frontend / Dashboard**: [Streamlit](https://streamlit.io/)
- **LLM Engine**: [Groq API](https://groq.com/) running `openai/gpt-oss-120b`
- **Data Validation & Schemas**: [Pydantic v2](https://docs.pydantic.dev/)
- **Document Parsing**:
  - [pypdf](https://pypi.org/project/pypdf/) (PDF text extraction)
  - [python-docx](https://python-docx.readthedocs.io/) (Word document extraction)
- **Environment Management**: `python-dotenv`, `uv` / `pip`

---

## 📁 Project Structure

```text
LLM_Resume_Evaluator/
│
├── src/
│   └── llm_resume_evaluator/
│       └── __init__.py           # Package entry point
│
├── app.py                        # Streamlit web dashboard for bulk resume evaluation
├── evaluator.py                  # Groq API integration and Pydantic validation
├── main.py                       # CLI test script for single resume evaluation
├── prompts.py                    # System prompts and schema formatting rules
├── schemas.py                    # Pydantic data models (ResumeEvaluation)
├── utils.py                      # Multi-format document text extraction (PDF & DOCX)
│
├── .env                          # API keys and environment variables (create this)
├── pyproject.toml                # Project configuration and dependencies (uv-compatible)
├── requirements.txt              # Standard pip dependencies list
├── README.md                     # Project documentation
└── uv.lock                       # Dependency lockfile
```

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/premkishan1215-maker/llm-resume-evaluator.git
cd LLM_Resume_Evaluator
```

### 2. Set Up a Virtual Environment

#### Using `uv` (Recommended):
```bash
# Create and sync virtual environment
uv venv
uv sync
```

#### Using standard Python `venv`:
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```
*Or directly install from `pyproject.toml`:*
```bash
pip install groq pydantic pypdf python-docx python-dotenv streamlit
```

---

## 🔑 Environment Configuration

Create a `.env` file in the root directory:

```ini
groq_API_keys=your_groq_api_key_here
```

> **Note**: Obtain your API key from the [Groq Console](https://console.groq.com/keys). Ensure the variable name is `groq_API_keys` as expected by `evaluator.py`.

---

## 🖥️ Usage

### Option 1: Run the Interactive Web Dashboard (Streamlit)

Launch the Streamlit user interface:

```bash
streamlit run app.py
```

1. **Upload Resumes**: Select one or multiple candidate resumes (`.pdf` or `.docx`).
2. **Enter Job Description**: Paste the target role's responsibilities, requirements, and tech stack.
3. **Filter Top Candidates**: Choose how many top candidates you want highlighted in the summary.
4. **Evaluate**: Click **🚀 Evaluate All Resumes**.
5. **Review Results**:
   - Inspect the ranking leaderboard table.
   - Expand individual candidate cards to review matched/missing skills, strengths, weaknesses, and suggestions.
6. **Download Report**: Click **📥 Download Top Candidates (CSV)** to save the evaluation results.

---

### Option 2: Run via CLI (Headless Script)

For a quick test on a single file:

1. Place a sample resume file named `resume.pdf` in the project root directory.
2. Run `main.py`:

```bash
python main.py
```

Sample CLI output:
```text
========== RESUME EVALUATION ==========
Match Score: 85

Matched Skills:
- Python
- Machine Learning
- SQL
- TensorFlow

Missing Skills:
- Docker
- AWS

Suggestions:
- Highlight any cloud deployment experience or containerization projects.

Summary:
The candidate demonstrates strong foundations in machine learning algorithms and Python development...
```

---

## 📊 Evaluation Schema

The LLM returns structured data validated by the `ResumeEvaluation` Pydantic model:

| Field | Type | Description |
| :--- | :--- | :--- |
| `match_score` | `int` | Candidate match rating between `0` and `100` |
| `matched_skills` | `List[str]` | Job description skills evidenced in the candidate's resume |
| `missing_skills` | `List[str]` | Required/preferred job skills not found in the resume |
| `strengths` | `List[str]` | Key competitive advantages and experience highlights |
| `weaknesses` | `List[str]` | Gaps, lack of specific domain tools, or missing qualifications |
| `suggestions` | `List[str]` | Specific guidance to improve candidate alignment |
| `summary` | `str` | Concise executive summary of candidate suitability |

---

## ⚡ Rate Limiting & Throttling

To prevent hitting Groq's API rate limits when screening large batches of resumes, `app.py` includes a **5-second cooldown interval** between consecutive API requests. Progress is displayed live on the UI with status updates.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!
Feel free to open an issue or submit a pull request.

---

## 👤 Author

- **Prem Kishan**
- Email: [premkishan1215@gmail.com](mailto:premkishan1215@gmail.com)
- GitHub: [@premkishan1215-maker](https://github.com/premkishan1215-maker)
