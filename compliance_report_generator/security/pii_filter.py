# security/pii_filter.py

import re

def detect_pii(prompt: str) -> dict:
    findings = {}

    email_matches = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", prompt)
    if email_matches:
        findings["email"] = email_matches

    phone_matches = re.findall(r"\b(?:\+?\d{1,3})?[-.\s]?(?:\(?\d{3}\)?[-.\s]?){2}\d{4}\b", prompt)
    if phone_matches:
        findings["phone"] = phone_matches

    ssn_matches = re.findall(r"\b\d{3}-\d{2}-\d{4}\b", prompt)
    if ssn_matches:
        findings["ssn"] = ssn_matches

    return findings
