import streamlit as st
from chat_chain import get_retrieval_chain
from ingestion import ingest_documents
import os

st.set_page_config(page_title="📄 Chat Over Documents", page_icon="🧠")

st.title("📄 Chat Over Documents with Qdrant + LangChain")
st.markdown("Upload a `.pdf` or `.txt` file, then ask questions about its contents.")

# Folder to store uploaded files
UPLOAD_FOLDER = "uploaded_docs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Upload
uploaded_file = st.file_uploader("Upload your document", type=["pdf", "txt"])

if uploaded_file is not None:
    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)

    if not os.path.exists(file_path):  # Only ingest if not already ingested
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())
        st.success(f"✅ Uploaded: {uploaded_file.name}")

        with st.spinner("⚙️ Ingesting document..."):
            ingest_documents(file_path)
            st.success("✅ Ingestion complete!")
    else:
        st.info("ℹ️ File already exists. Skipping ingestion.")

    # Initialize RAG chain
    st.session_state.qa_chain = get_retrieval_chain()

# Chat Section
if "qa_chain" in st.session_state:
    st.markdown("### 💬 Ask a question about the document:")
    question = st.text_input("Your question")

    if question:
        with st.spinner("🤖 Generating response..."):
            result = st.session_state.qa_chain(question)
            st.success("✅ Answer ready!")

            # Display Answer
            st.markdown(f"**🧠 Answer:**\n\n{result['result']}")

            # Display Source Chunks
            with st.expander("📚 Source Chunks"):
                for i, doc in enumerate(result["source_documents"], 1):
                    st.markdown(f"**Chunk {i}:** `{doc.metadata.get('source', 'Unknown')}`")
                    st.code(doc.page_content)
