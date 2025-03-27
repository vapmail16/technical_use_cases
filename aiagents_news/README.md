# 📰 AI Agents News Blogger

This project is an **AI-powered blog generation agent** that:
- Accepts a blog topic from the user.
- Generates a structured outline.
- Fetches real-world news using NewsAPI.
- Writes an engaging, human-readable blog post using OpenAI's GPT-4.
- Humanizes the blog for a more narrative tone.
- Optionally saves the blog post with a timestamped filename.
- Tracks previously used topics in a memory file.

### 🧠 Features
- GPT-4-based outline + blog generation.
- News snippet enrichment via NewsAPI.
- Human-in-the-loop memory tracking (`memory.json`).
- File-based storage of all generated blogs.
- Devcontainer support for reproducible environment.

### ⚙️ Tech Stack
- Python 3.11
- Poetry
- OpenAI GPT-4
- NewsAPI
- Devcontainers

### ▶️ Run Instructions
```bash
make install     # Installs all dependencies
make run         # Starts the blog writing agent
