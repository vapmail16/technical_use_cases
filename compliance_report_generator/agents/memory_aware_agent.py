from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from vector_store.retrieval_chain import get_retriever
from graph.neo4j_utils import run_cypher_query

def get_memory_aware_chain(role, question):
    # Pull graph memory
    graph_memory = run_cypher_query(question)

    # Create prompt template
    template = """You are an AI compliance assistant for the role of a {role}.

Context from Graph DB:
{graph_memory}

Relevant chunks from the document:
{context}

Now answer this question:
{input}
"""

    prompt = PromptTemplate(
    input_variables=["input", "role", "graph_memory", "context"],
    template=template,
)

    # LLM setup
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    # Combine doc chain with prompt
    combine_chain = create_stuff_documents_chain(llm=llm, prompt=prompt)

    # Get vector retriever
    retriever = get_retriever()

    # New retrieval QA chain
    chain = create_retrieval_chain(
        retriever=retriever,
        combine_docs_chain=combine_chain
    )

    return chain
