from langchain.tools import tool

@tool
def get_compliance_score(company_name: str) -> str:
    """
    Mock compliance score lookup for a company.
    Returns a predefined risk rating.
    """
    sample_scores = {
        "Meta": "Low risk",
        "Palantir": "Medium risk",
        "Cambridge Analytica": "High risk",
        "Tesla": "Medium risk",
        "OpenAI": "Low risk",
        "Clearview AI": "High risk",
        "Google": "Low risk",
        "TikTok": "Medium risk"
    }

    return sample_scores.get(company_name, "Unknown risk – no data available.")
