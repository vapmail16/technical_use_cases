from compliance_lookup_tool import get_compliance_score
from compliance_lookup import lookup_compliance

if __name__ == "__main__":
    print("\n🧪 Mock Compliance Tools Test\n")

    company = input("Enter company name for risk score: ")
    risk_score = get_compliance_score.run(company)
    print(f"📊 Compliance Risk: {risk_score}")

    term = input("\nEnter compliance term to look up (e.g., GDPR, CCPA): ")
    definition = lookup_compliance.run(term)
    print(f"📘 Compliance Info: {definition}")
