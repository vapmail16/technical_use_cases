from langchain.tools import tool

@tool
def calculate_risk(input: dict) -> str:
    """
    Calculates a risk score based on data sensitivity and exposure level.
    Expects a dictionary with keys: 'data_sensitivity' and 'exposure_level'.

    Sensitivity: low, medium, high
    Exposure: internal, third-party, public
    """

    data_sensitivity = input.get("data_sensitivity", "").lower()
    exposure_level = input.get("exposure_level", "").lower()

    score = 0

    # Base score by sensitivity
    if data_sensitivity == "low":
        score += 10
    elif data_sensitivity == "medium":
        score += 30
    elif data_sensitivity == "high":
        score += 60
    else:
        return "❌ Invalid sensitivity. Use: low, medium, or high."

    # Exposure multiplier
    if exposure_level == "internal":
        multiplier = 1
    elif exposure_level == "third-party":
        multiplier = 1.5
    elif exposure_level == "public":
        multiplier = 2
    else:
        return "❌ Invalid exposure level. Use: internal, third-party, or public."

    final_score = int(score * multiplier)
    return f"📊 Risk Score: {final_score}/100 based on {data_sensitivity} sensitivity and {exposure_level} exposure."
