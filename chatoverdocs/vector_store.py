from langchain_community.vectorstores import Qdrant
from langchain_community.embeddings import OpenAIEmbeddings
import os

def get_qdrant_vectorstore():
    embeddings = OpenAIEmbeddings()

    return Qdrant(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY"),
        collection_name=os.getenv("QDRANT_COLLECTION"),
        embeddings=embeddings
    )
