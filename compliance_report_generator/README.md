# 🧠 Compliance Report Generator (CRG)

A powerful AI-powered system to process compliance documents, extract structured insights, and answer regulatory questions — all with robust safety, agent workflows, and graph-based memory.

---

## 🚀 Key Features

### 📄 Smart Document Processing
- **PDF/Text Ingestion** with table-aware parsing using `pdfplumber`
- **Chunked Embeddings** stored in **Qdrant** for high-speed vector search
- **Entity Extraction** and **Relationship Mapping** into **Neo4j GraphDB**

### 🧠 Intelligent Agent Workflows
- **LangChain-Powered Agents**:
  - 🔍 Memory-Aware QA for contextual answers
  - 🔧 Tool Agent for risk scoring, news fetch, summarization, etc.
- **LangGraph Checkpointing Workflow**:
  - Stepwise fault-tolerant ingestion, embedding, graph update, and checkpoint storage

### 🔐 Security & Guardrails
- **Prompt Filtering** for harmful instructions or unethical queries
- **PII Detection** for emails, phone numbers, SSNs, and more
- **Unified Safety Layer** that protects:
  - CLI interface
  - Agents
  - Streamlit UI

### 🧑‍⚖️ Human-in-the-Loop (HITL)
- **Manual Approval** before saving AI-generated answers
- Transparent **Session Logs** with timestamps and roles

---

## 🛠️ Developer Setup

### 1. Clone & Install
```bash
git clone https://github.com/your-org/compliance-report-generator.git
cd compliance-report-generator
poetry install
poetry shell

2. Environment Setup
Create a .env file with the following variables:

OPENAI_API_KEY=your-key
NEWS_API_KEY=your-key
QDRANT_API_KEY=your-key
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your-password

💻 Run the App
🔍 CLI Tool Tests (Optional)
python -m tools.test_compliance_lookup
python -m tools.test_risk_calculator
python -m tools.test_summary_filter_tool
python -m security.test_safety

🌐 Streamlit Interface
streamlit run main.py

🧩 Folder Structure
compliance_report_generator/
│
├── agents/                # LangChain agents (memory-aware, tool-using)
├── graph/                 # Neo4j logic, doc-to-graph extraction, checkpoint graphs
├── memory/                # Persistent Qdrant memory
├── tools/                 # LangChain-compatible tools (news, compliance, risk)
├── security/              # Prompt filtering + PII detection
├── vector_store/          # Ingestion logic and vector DB setup
├── uploaded_docs/         # Uploaded PDFs (local dev only)
│
├── diagnostics.py         # Pre-launch sanity checks
├── main.py                # Streamlit UI + safety + HITL integration
├── .env.example           # Environment variable template
├── README.md              # This file 😄


✅ Roadmap Summary
✅ Phase 1–4: Ingestion, RAG pipeline, Streamlit UI
✅ Phase 5: Tool Agent Integration
✅ Phase 6: Neo4j Graph Memory
✅ Phase 7: LangGraph Checkpointing Workflow
✅ Phase 8: Prompt Filtering + PII Detection
✅ Phase 9: HITL Approval Workflow
✅ Phase 10: Final Polish & Demo Ready 🎉


👥 Contributing
If you'd like to contribute to CRG:
Fork the repo
Make your changes
Submit a pull request 🚀

