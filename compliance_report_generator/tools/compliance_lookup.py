from langchain.tools import tool

MOCK_COMPLIANCE_DATA = {
    "gdpr": "GDPR (General Data Protection Regulation) applies to all EU member states and governs data privacy and protection.",
    "ccpa": "CCPA (California Consumer Privacy Act) grants privacy rights to residents of California, USA.",
    "hipaa": "HIPAA ensures medical data privacy in the US healthcare industry.",
    "iso27001": "ISO 27001 is an international standard for information security management systems (ISMS)."
}

@tool
def lookup_compliance(input: str) -> str:
    """
    Look up a compliance regulation. Valid terms: GDPR, CCPA, HIPAA, ISO27001.
    """
    key = input.lower().strip().replace("'", "").replace('"', "")
    return MOCK_COMPLIANCE_DATA.get(key, f"No information found for '{key}'. Try 'GDPR', 'CCPA', 'HIPAA', or 'ISO27001'.")
