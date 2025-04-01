# security/safety_check.py

from security.guardrails import contains_unsafe_content
from security.pii_filter import detect_pii

def run_safety_checks(prompt: str) -> dict:
    pii_result = detect_pii(prompt)
    if pii_result:
        return {
            "is_safe": False,
            "reason": "PII detected",
            "pii": pii_result
        }

    if contains_unsafe_content(prompt):
        return {
            "is_safe": False,
            "reason": "Unsafe content detected",
            "pii": None
        }

    return {"is_safe": True}
