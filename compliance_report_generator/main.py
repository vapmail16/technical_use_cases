import subprocess
import streamlit as st
import os
import datetime
import pdfplumber

# Run diagnostics
try:
    result = subprocess.run(["python", "diagnostics.py"], check=True, capture_output=True, text=True)
    print("🛠️ Pre-launch diagnostics completed successfully.\n")
    print(result.stdout)
except subprocess.CalledProcessError as e:
    print("❌ Diagnostics failed. Details below:\n")
    print(e.stdout)
    print(e.stderr)
    st.error("Startup diagnostics failed. Check terminal for details.")
    st.stop()

# Imports AFTER diagnostics
from agents.memory_aware_agent import get_memory_aware_chain
from agents.tool_calling_agent import get_tool_agent
from vector_store.ingest import ingest_documents
from memory.qdrant_memory import store_memory_entry
from graph.doc_to_graph import extract_and_store_knowledge
from graph.neo4j_utils import ensure_fulltext_index
from security.safety_check import run_safety_checks

# Ensure Neo4j index on startup
ensure_fulltext_index()

st.set_page_config(page_title="📊 Compliance Report Generator", page_icon="🧠")
st.title("📊 Compliance Report Generator")
st.markdown("Upload a `.pdf` compliance document and ask questions about its contents.")

UPLOAD_FOLDER = "uploaded_docs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

if "session_logs" not in st.session_state:
    st.session_state.session_logs = []

if "graph_memory" not in st.session_state:
    st.session_state.graph_memory = "No graph memory retrieved."

if "last_result" not in st.session_state:
    st.session_state.last_result = None
if "last_question" not in st.session_state:
    st.session_state.last_question = None
if "awaiting_approval" not in st.session_state:
    st.session_state.awaiting_approval = False

# Role selector
st.markdown("### 🧑‍⚖️ Select your role:")
role = st.selectbox("Choose your context", ["legal_analyst", "policy_researcher", "compliance_officer"])

# Agent mode selector
st.markdown("### 🧠 Select Agent Mode:")
agent_mode = st.radio("Choose how you want to interact:", ["Memory-Aware QA", "Tool Agent"])

# File upload
uploaded_file = st.file_uploader("Upload your document", type=["pdf", "txt"])

if uploaded_file is not None:
    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)

    if not os.path.exists(file_path):
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())
        st.success(f"✅ Uploaded: {uploaded_file.name}")

        with st.spinner("⚙️ Ingesting document..."):
            ingest_documents(file_path)
            st.success("✅ Ingestion complete!")

        with st.spinner("🔍 Extracting structured knowledge..."):
            with pdfplumber.open(file_path) as pdf:
                first_page = pdf.pages[0].extract_text()
                if first_page:
                    extract_and_store_knowledge(first_page)
                    st.success("✅ Entities extracted and stored in Neo4j!")
    else:
        st.info("ℹ️ File already exists. Skipping ingestion.")

    # Initialize chains
    if agent_mode == "Memory-Aware QA":
        st.session_state.qa_chain = get_memory_aware_chain(role, question="")
    else:
        st.session_state.tool_agent = get_tool_agent()

# Chat section
if agent_mode == "Memory-Aware QA" and "qa_chain" in st.session_state:
    st.markdown("### 💬 Ask a question about the document:")
    question = st.text_input("Your question")

    if question and not st.session_state.awaiting_approval:
        safety = run_safety_checks(question)
        if not safety["is_safe"]:
            st.error(f"🚫 Unsafe question detected: {safety['reason']}")
            if safety["pii"]:
                st.warning(f"🔍 PII Found: {safety['pii']}")
            st.stop()

        with st.spinner("🤖 Generating response..."):
            result = st.session_state.qa_chain.invoke({
                "input": question,
                "role": role,
                "graph_memory": st.session_state.graph_memory
            })

        st.session_state.last_result = result
        st.session_state.last_question = question
        st.session_state.awaiting_approval = True
        st.rerun()

    elif st.session_state.awaiting_approval:
        result = st.session_state.last_result
        question = st.session_state.last_question

        st.success("✅ Answer ready (Not saved yet)")
        st.markdown(f"**🧠 Answer:**\n\n{result['answer']}")

        with st.expander("📚 Source Chunks"):
            for i, doc in enumerate(result.get("context", []), 1):
                st.markdown(f"**Chunk {i}:** `{doc.metadata.get('source', 'Unknown')}`")
                st.code(doc.page_content)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Approve & Save to Memory"):
                store_memory_entry(question, result["answer"])
                st.session_state.session_logs.append({
                    "timestamp": datetime.datetime.now().isoformat(),
                    "role": role,
                    "file": uploaded_file.name if uploaded_file else "None",
                    "question": question
                })
                st.success("💾 Saved to memory!")
                st.session_state.awaiting_approval = False
                st.session_state.last_result = None
                st.session_state.last_question = None
                st.rerun()

        with col2:
            if st.button("🔁 Regenerate"):
                st.session_state.awaiting_approval = False
                st.rerun()

elif agent_mode == "Tool Agent" and "tool_agent" in st.session_state:
    st.markdown("### 🤖 Ask your agent (news, summaries, scores, etc.):")
    user_question = st.text_input("Your query")

    if user_question:
        safety = run_safety_checks(user_question)
        if not safety["is_safe"]:
            st.error(f"🚫 Unsafe query detected: {safety['reason']}")
            if safety["pii"]:
                st.warning(f"🔍 PII Found: {safety['pii']}")
            st.stop()

        with st.spinner("🧠 Thinking..."):
            result = st.session_state.tool_agent.invoke(user_question)
            st.markdown(f"**🧾 Agent Response:**\n\n{result}")

# Session log viewer
with st.expander("🧾 Session Log"):
    for log in st.session_state.session_logs:
        st.markdown(f"- 🕒 `{log['timestamp']}` | 👤 Role: `{log['role']}` | 📄 File: `{log['file']}`")
        st.markdown(f"  ➤ **Q:** {log['question']}")
