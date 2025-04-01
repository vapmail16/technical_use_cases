# diagnostics.py
import os
import sys
import importlib
from qdrant_client import QdrantClient
from neo4j import GraphDatabase
from dotenv import load_dotenv


# Load env vars
load_dotenv()

def check_python_version():
    print(f"🐍 Python Version: {sys.version.split()[0]}")
    if sys.version_info < (3, 10):
        print("⚠️ Warning: Python 3.10+ recommended for LangChain stability.")

def check_required_env_vars():
    required_vars = [
        "QDRANT_URL", "QDRANT_API_KEY",
        "NEO4J_URI", "NEO4J_USERNAME", "NEO4J_PASSWORD"
    ]
    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        print(f"❌ Missing ENV vars: {', '.join(missing)}")
    else:
        print("✅ All required environment variables are set.")

def check_imports():
    required_modules = [
        "langchain", "langchain_openai", "qdrant_client", "neo4j", "tiktoken", "pdfplumber"
    ]
    missing = []
    for module in required_modules:
        if importlib.util.find_spec(module) is None:
            missing.append(module)
    if missing:
        print(f"❌ Missing Python packages: {', '.join(missing)}")
        print("🔧 Run: poetry add " + " ".join(missing))
    else:
        print("✅ All critical Python packages are installed.")

def check_qdrant():
    try:
        client = QdrantClient(
            url=os.getenv("QDRANT_URL"),
            api_key=os.getenv("QDRANT_API_KEY")
        )
        status = client.get_collections()
        print("✅ Qdrant connection successful.")
    except Exception as e:
        print(f"❌ Qdrant connection failed: {e}")

def check_neo4j():
    try:
        uri = os.getenv("NEO4J_URI")
        user = os.getenv("NEO4J_USERNAME")
        password = os.getenv("NEO4J_PASSWORD")
        driver = GraphDatabase.driver(uri, auth=(user, password))
        with driver.session() as session:
            result = session.run("RETURN 1 AS check")
            if result.single()["check"] == 1:
                print("✅ Neo4j connection successful.")
    except Exception as e:
        print(f"❌ Neo4j connection failed: {e}")

def check_openai():
    try:
        from langchain_openai import ChatOpenAI
        llm = ChatOpenAI()
        output = llm.invoke("Say hello")
        if output:
            print("✅ OpenAI LLM response received.")
    except Exception as e:
        print(f"❌ OpenAI LLM test failed: {e}")

def check_uploaded_docs_folder():
    if not os.path.exists("uploaded_docs"):
        print("❌ Folder 'uploaded_docs' missing. Creating it...")
        os.makedirs("uploaded_docs")
    else:
        print("✅ Folder 'uploaded_docs' exists.")

def run_diagnostics():
    print("📋 Running Diagnostics...\n")
    check_python_version()
    check_required_env_vars()
    check_imports()
    check_uploaded_docs_folder()
    check_qdrant()
    check_neo4j()
    check_openai()

if __name__ == "__main__":
    run_diagnostics()

if __name__ == "__main__":
    run_diagnostics()
    # You can define pass/fail criteria here
    sys.exit(0)  # or sys.exit(1) if any critical check fails