🔧 Technical Use Cases – AI App Experiments
==========================================

This monorepo contains various AI-driven mini projects focused on **LLMs, automation, and agentic workflows**. Built using modern Python tools like Poetry and DevContainers for consistency and reusability.

---

## 📁 Projects Included

### 1. `aiagents_news/` – Blog Writer Agent
- GPT-4 based blog generator with NewsAPI enrichment.
- Human-in-the-loop memory tracking.
- CLI-powered interface.
- Ideal for content creators and news bloggers.

### 2. `careerpro/` – Resume Reviewer & Tailor
- Streamlit UI to review and tailor CVs.
- Optimized for job applications using OpenAI GPT.
- Resume-to-job alignment and PDF output.

### 3. `chatbot_app/` – LangChain Chatbot with Memory + Tools
- Streamlit-based chatbot interface.
- Conversational memory using LangChain.
- Tool-calling support (DuckDuckGo search).
- Moderation guardrails via OpenAI's safety API.
- Token usage tracking.

### 4. `chatoverdocs/` – Chat Over Large Documents (PDF/TXT)
- Streamlit interface to upload and query large documents.
- PDF-aware ingestion using `pdfplumber` for tables.
- LangChain-powered RAG pipeline with Qdrant as vector store.
- Uses OpenAI embeddings and GPT models.
- Helpful for researchers, journalists, and legal document analysis.

### 5. `compliance_report_generator/` – Secure AI Agent with Graph + Guardrails
- Ingests PDF regulations and extracts structured entity relationships into Neo4j.
- Uses Qdrant for semantic search + memory.
- Graph-based reasoning + checkpointing with LangGraph.
- Tool-calling agents and human-in-the-loop validation.
- Prompt guardrails, PII detection, and unsafe content blocker.
- Streamlit UI for full document upload → Q&A → insights.

### 6. `mcp/` – TweetGen MCP: Blog-to-Twitter Thread Generator
- Generate 5 tweet-worthy hooks from a long blog.
- Expand each into a 10-part Twitter thread.
- Modular backend powered by LangGraph + LangChain tools.
- Streamlit UI with clean UX.
- OpenAI GPT-4 backend with CLI and diagnostics.
- Ideal for authors, influencers, and thought leaders.
- → [View README](mcp/README.md)

---

## 🛠️ Setup Instructions

```bash
# Clone the repository
git clone https://github.com/vapmail16/technical_use_cases.git
cd technical_use_cases

# Open in VS Code DevContainer
code .

# For aiagents_news
cd aiagents_news
make install && make run

# For careerpro
cd ../careerpro
poetry install
poetry run streamlit run app.py

# For chatbot_app
cd ../chatbot_app/agent
poetry install
poetry run streamlit run app.py

# For chatoverdocs
cd ../../chatoverdocs
poetry install
poetry run streamlit run app.py

# For compliance_report_generator
cd ../compliance_report_generator
poetry install
poetry run streamlit run main.py

# For tweetgen_mcp
cd ../mcp
poetry install --no-root
cp .env.example .env  # Add your OpenAI key
make run              # Start LangGraph pipeline
poetry run streamlit run streamlit_app.py  # Launch UI
