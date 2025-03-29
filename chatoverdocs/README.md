# 📄 Chat Over Documents with Qdrant + LangChain

This app lets you **upload a PDF or text file** and **chat with its contents** using LangChain, Qdrant, and OpenAI.

✅ Built for exploring **Retrieval-Augmented Generation (RAG)** use cases  
✅ Powered by **Streamlit** for a beautiful UI  
✅ Uses **Qdrant Vector Store** for scalable document search  

---

## 🛠 Tech Stack

| Component    | Tech                  |
|-------------|------------------------|
| UI          | Streamlit              |
| LLM         | OpenAI (via LangChain) |
| Vector DB   | Qdrant (Cloud)         |
| Embeddings  | `OpenAIEmbeddings`     |
| Parsing     | `pdfplumber` (table-aware) |
| Frameworks  | LangChain, LangChain OpenAI |

---

## 🚀 Getting Started

### 1. Clone this repo

```bash
git clone https://github.com/your-username/chatoverdocs.git
cd chatoverdocs

2. Install dependencies using Poetry
poetry install

3. Setup .env file
Create a .env file in the root with these keys:
OPENAI_API_KEY=sk-...
QDRANT_URL=https://your-qdrant-url
QDRANT_API_KEY=your-qdrant-api-key

4. Run the app
poetry run streamlit run app.py

📁 Folder Structure
chatoverdocs/
│
├── app.py               # Streamlit frontend
├── ingestion.py         # PDF/text loader with table-aware parsing
├── chat_chain.py        # LangChain-based retrieval QA chain
├── vector_store.py      # (Optional) Vector DB helper logic
├── uploaded_docs/       # Auto-saves uploaded PDFs
├── .env.example         # Example env file
├── README.md
└── pyproject.toml       # Poetry config

🧠 How It Works
Upload PDF – UI lets you drop in .pdf or .txt files
Ingestion – Uses pdfplumber to extract tables and paragraphs
Embeddings – Text chunks embedded via OpenAIEmbeddings
Storage – Vectors pushed into Qdrant collection
Chat – Ask natural language questions, get LLM answers with sources

✅ To-Do Next
 Add support for .docx
 Streamed responses
 Advanced chunking and metadata tagging
 Support multiple files
 Guardrails for moderation



