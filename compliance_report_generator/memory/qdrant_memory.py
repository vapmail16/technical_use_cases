import os
from dotenv import load_dotenv
from langchain_community.vectorstores import Qdrant
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.docstore.document import Document
from qdrant_client import QdrantClient
from qdrant_client.http import models as rest

load_dotenv()

def store_memory_entry(question: str, answer: str):
    embedding = OpenAIEmbeddings()
    client = QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY")
    )
    collection_name = "session_memory"

    # Create memory collection if needed
    if not client.collection_exists(collection_name):
        client.create_collection(
            collection_name=collection_name,
            vectors_config=rest.VectorParams(size=1536, distance=rest.Distance.COSINE),
        )

    doc = Document(
        page_content=f"Q: {question}\nA: {answer}",
        metadata={"source": "session_log"}
    )

    Qdrant.from_documents(
        [doc],
        embedding,
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY"),
        collection_name=collection_name,
    )

def get_memory_retriever():
    embedding = OpenAIEmbeddings()
    return Qdrant(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY"),
        collection_name="session_memory",
        embeddings=embedding
    ).as_retriever()
