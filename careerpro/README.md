# 🧠 CareerPro – CV Review & Tailoring with AI

CareerPro is a **Streamlit-based AI application** that lets users:
- Upload a CV and get a professional review.
- Upload a job description to tailor their CV for that role.
- Download a well-formatted, ATS-friendly PDF resume.

### 🎯 Features
- Resume analysis and suggestions using GPT-4.
- CV tailoring based on job descriptions.
- Supports PDF and TXT uploads.
- Download tailored resumes as clean PDFs (via ReportLab).
- Beautiful Streamlit interface for non-tech users.

### ⚙️ Tech Stack
- Python 3.11
- Poetry
- Streamlit
- OpenAI GPT-4
- PyPDF2 & ReportLab
- dotenv

### ▶️ Run Instructions
```bash
poetry install
poetry run streamlit run app.py
