from langchain.tools import tool

@tool
def filter_summary(text: str) -> str:
    """
    Filters a long compliance answer and returns only the 3 most important points.
    """
    import re

    # Simple sentence-based summary (for POC – can replace with LLM later)
    sentences = re.split(r"(?<=[.!?]) +", text)
    summary = sentences[:3] if len(sentences) >= 3 else sentences
    return "📝 Key Points:\n" + "\n".join(f"- {s.strip()}" for s in summary)
