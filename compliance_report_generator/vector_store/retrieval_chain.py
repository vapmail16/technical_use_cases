from langchain_community.vectorstores import Qdrant
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.chat_models import ChatOpenAI
from qdrant_client import QdrantClient
from dotenv import load_dotenv
import os

load_dotenv()

# ✅ Use QdrantClient explicitly
def get_qdrant_retriever():
    embeddings = OpenAIEmbeddings()

    client = QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY")
    )

    # ✅ This works with langchain_community
    qdrant = Qdrant(
        client=client,
        collection_name=os.getenv("QDRANT_COLLECTION"),
        embeddings=embeddings
    )

    return qdrant.as_retriever()

# ✅ Exportable retriever for agent chains
def get_retriever():
    return get_qdrant_retriever()

# Optional QA wrapper chain
def get_retrieval_chain():
    retriever = get_qdrant_retriever()
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True 
    )
    return qa_chain
