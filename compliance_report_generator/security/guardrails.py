# security/guardrails.py

def contains_unsafe_content(prompt: str) -> bool:
    UNSAFE_KEYWORDS = [
        "bypass the law", "how to hack", "steal data", "destroy", "blackmail", "kill",
        "illegal", "cheat exam", "spoof", "fraud", "how to make a bomb"
    ]
    prompt_lower = prompt.lower()
    return any(keyword in prompt_lower for keyword in UNSAFE_KEYWORDS)
