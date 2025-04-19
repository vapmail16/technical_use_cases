# diagnostic.py

import os
import sys
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def check_python_version():
    print("✅ Python version:", sys.version)
    if sys.version_info < (3, 11):
        print("❌ Python 3.11+ is required.")
        return False
    return True

def check_env_vars():
    print("\n🔍 Checking environment variables...")
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        print("❌ OPENAI_API_KEY not set in environment.")
        return False
    print("✅ OPENAI_API_KEY is set.")
    return True

def check_openai_auth():
    print("\n🔌 Testing OpenAI API key...")
    try:
        client = OpenAI()
        models = client.models.list()
        print("✅ OpenAI API authentication successful. Sample models:", [m.id for m in models.data[:3]])
        return True
    except Exception as e:
        print("❌ OpenAI test failed:", e)
        return False

if __name__ == "__main__":
    print("🧪 Running diagnostics...\n")
    all_ok = all([
        check_python_version(),
        check_env_vars(),
        check_openai_auth()
    ])
    if all_ok:
        print("\n✅ All systems go!")
    else:
        print("\n⚠️ Diagnostics failed. Please fix the above issues.")
