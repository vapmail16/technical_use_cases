from langchain.tools import tool
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

@tool
def summarize_and_filter(input: str) -> str:
    """
    Summarizes compliance text and optionally filters by keywords.
    Input format: 'text=[TEXT] | keywords=[comma,separated,words]'
    """
    try:
        parts = dict(item.strip().split("=") for item in input.split("|"))
        text = parts.get("text", "").strip()
        keywords = parts.get("keywords", "").strip()
    except Exception:
        return "❌ Invalid format. Use: 'text=... | keywords=...'"

    if not text:
        return "❌ Please provide text to summarize."

    base_prompt = f"Summarize the following compliance text:\n{text}"
    if keywords:
        base_prompt += f"\nOnly include points relevant to: {keywords}"

    try:
        response = llm.invoke(base_prompt)
        return f"📝 Summary:\n{response}"
    except Exception as e:
        return f"❌ LLM Error: {e}"
