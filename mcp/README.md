# 🧠 TweetGen MCP

Generate high-quality Twitter threads from long-form blogs using modular LangGraph architecture.

## 🚀 Features
- Paste a blog and extract 5 tweet-worthy ideas
- Expand each idea into a 10-tweet Twitter thread
- Clean, Streamlit-powered UI for interaction
- Modular, scalable backend with LangGraph tool orchestration

## 🧰 Architecture Overview

```
[Streamlit UI] → [LangGraph Workflow]
   ├─ blog_to_tweets (5 tweet hooks)
   └─ expand_tweet (10-part thread per hook)
         ↓
   [Final output: 50 tweets displayed in UI]
```

## 🛠 Tools Used
- `blog_to_tweets`: Extracts 5 engaging hooks from a blog
- `expand_tweet`: Expands each into a 10-part thread

## 📦 Tech Stack
- Python 3.11
- Poetry (dependency management)
- LangGraph (modular agent orchestration)
- OpenAI GPT-4 API
- Streamlit (interactive frontend)

## ▶️ Usage

```bash
# Setup
poetry install --no-root
cp .env.example .env  # Add your OpenAI key here

# Run LangGraph tools
make run

# Run Streamlit UI
poetry run streamlit run streamlit_app.py
```

## ✅ Why LangGraph / MCP-style vs Direct Calls
- **Modular**: Tools are cleanly separated
- **Composable**: Easy to add/replace tools
- **Debuggable**: Each tool step is inspectable
- **Upgradeable**: Supports agents, memory, filtering

## 📄 Project Structure

```
📁 mcp/
├── main.py              # LangGraph workflow
├── tools.py             # Tool definitions (@tool)
├── streamlit_app.py     # Frontend UI
├── diagnostic.py        # Pre-run checks
├── Makefile             # Run commands
├── pyproject.toml       # Poetry project config
├── troubleshooting.md   # All dev issues/fixes logged
├── .env / .env.example  # API key management
```

## ✨ Future Add-ons
- Export to PDF or Markdown
- Post scheduling or API integration with Twitter/X
- Admin dashboard

---

© 2025 TweetGen MCP – Powered by LangGraph + Streamlit
