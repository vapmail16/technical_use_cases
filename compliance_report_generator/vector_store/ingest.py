import os
import pdfplumber
from langchain_community.vectorstores import Qdrant
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.docstore.document import Document
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.http import models as rest

load_dotenv()

def extract_text_from_pdf(file_path):
    documents = []
    with pdfplumber.open(file_path) as pdf:
        for i, page in enumerate(pdf.pages):
            try:
                table = page.extract_table()
                if table:
                    for row in table:
                        text = " | ".join(str(cell).strip() for cell in row if cell)
                        if text:
                            documents.append(Document(page_content=text, metadata={"source": file_path}))
                else:
                    text = page.extract_text()
                    if text:
                        documents.append(Document(page_content=text.strip(), metadata={"source": file_path}))
            except Exception as e:
                print(f"⚠️ Skipping page {i} due to error: {e}")
    return documents

def ingest_documents(file_path):
    print(f"📄 Loading document: {file_path}")
    documents = extract_text_from_pdf(file_path)
    print(f"✅ Loaded {len(documents)} chunks from {os.path.basename(file_path)}")

    embedding_model = OpenAIEmbeddings()
    
    # ✅ Define the Qdrant client before using it
    client = QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY"),
    )

    collection_name = os.getenv("QDRANT_COLLECTION")

    # ✅ Fix: define `client` before this line
    if not client.collection_exists(collection_name):
        print(f"📁 Creating new Qdrant collection: {collection_name}")
        client.create_collection(
            collection_name=collection_name,
            vectors_config=rest.VectorParams(size=1536, distance=rest.Distance.COSINE),
        )
    else:
        print(f"ℹ️ Using existing Qdrant collection: {collection_name}")

    Qdrant.from_documents(
        documents,
        embedding_model,
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY"),
        collection_name=collection_name,
    )

    print(f"✅ Ingested to Qdrant collection: {collection_name}")
