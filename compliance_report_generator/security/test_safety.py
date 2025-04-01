# security/test_safety.py

from security.safety_check import run_safety_checks

while True:
    prompt = input("\n🔍 Enter a prompt to test safety (or type 'exit'): ")
    if prompt.strip().lower() == "exit":
        break

    result = run_safety_checks(prompt)

    if result["is_safe"]:
        print("✅ Safe prompt")
    else:
        print(f"❌ Unsafe prompt → Reason: {result['reason']}")
        if result.get("pii"):
            print("🛑 PII Found:", result["pii"])
