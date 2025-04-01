from risk_calculator import calculate_risk

print("\n🧪 Risk Calculator Test\n")
sensitivity = input("Enter data sensitivity (low, medium, high): ")
exposure = input("Enter exposure level (internal, third-party, public): ")

input_dict = {
    "data_sensitivity": sensitivity,
    "exposure_level": exposure
}

result = calculate_risk.invoke(input_dict)
print(f"\n{result}")
