# 🤖 LangChain Chatbot App

A simple but powerful chatbot app built with **LangChain**, **Streamlit**, and **OpenAI**, demonstrating:

- ✅ **LangChain Agents** with Search Tool (DuckDuckGo)
- 🧠 **Memory** with context-aware conversations
- 🚨 **Moderation Guardrails** using OpenAI's Moderation API
- 💬 Clean Streamlit-based chat UI

---

## 📦 Features

| Feature          | Status | Details                                                                 |
|------------------|--------|-------------------------------------------------------------------------|
| LangChain Agent  | ✅      | Uses `initialize_agent` with tool calling                              |
| Tool Support     | ✅      | DuckDuckGo Search tool integrated                                      |
| Memory           | ✅      | ConversationBufferMemory (context-aware chat)                          |
| Moderation       | ✅      | Blocks unsafe content using OpenAI Moderation                          |
| Streamlit UI     | ✅      | Fully interactive, modern chat layout                                  |
| Token Tracking   | ✅      | Displays token usage per message                                       |

---

## 🧠 Tech Stack

- **LangChain** (`v0.1+`)
- **Streamlit** (`v1.x`)
- **OpenAI / langchain-openai**
- **DuckDuckGo Search Tool**
- **Python 3.11**
- **Poetry** for dependency management

---

## 🚀 Getting Started

### 1. Clone the Repo
```bash
git clone https://github.com/vapmail16/technical_use_cases.git
cd technical_use_cases/chatbot_app
```

### 2. Install Dependencies
```bash
poetry install
```

### 3. Add `.env` file with OpenAI Key
```env
OPENAI_API_KEY=your-api-key-here
```

### 4. Run the App
```bash
poetry run streamlit run agent/app.py
```

---

## 🧪 Example Prompts

```text
what is the capital of India?
who is the president of the USA?
what is the population of Japan?
```

---

## 🛡️ Moderation
- Uses OpenAI's moderation endpoint to prevent unsafe inputs
- If blocked, user gets an error before the message is sent to the model

---

## 📈 Future Enhancements (v2+)
- 🎙️ Voice input (Whisper / Browser Mic)
- 🌐 LangGraph-based agent orchestration
- 🧩 Tool chaining (e.g. Calculator + Search)
- 🧼 More advanced memory (Neo4j, Vector Store)
- 🔐 Advanced security/PII filtering

---

## 👤 Author
**Vikkas Arun Pareek**  
[GitHub](https://github.com/vapmail16) • [LinkedIn](https://www.linkedin.com/in/vikkaspareek/)

---

## 📄 License
MIT License. Use freely with attribution 🙏
