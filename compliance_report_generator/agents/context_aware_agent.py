from vector_store.retrieval_chain import get_qdrant_retriever
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOpenAI

# Prompt templates for different user roles
ROLE_PROMPT_TEMPLATES = {
    "legal_analyst": """You are a legal analyst. Provide detailed, citation-rich answers with references to specific clauses or legal documents where possible.""",
    "policy_researcher": """You are a policy researcher. Focus on summarizing the broader policy impacts, comparisons, and real-world implications.""",
    "compliance_officer": """You are a compliance officer. Respond with risk-oriented insights, potential compliance violations, and checklist-style responses where applicable."""
}

def get_context_aware_chain(role: str = "legal_analyst"):
    # Retrieve Qdrant-based document chunks
    retriever = get_qdrant_retriever()

    # Select role-specific prompt
    system_prompt = ROLE_PROMPT_TEMPLATES.get(role, "")
    
    # Build the full prompt
    prompt = PromptTemplate.from_template(
        f"{system_prompt}\n\nContext: {{context}}\n\nQuestion: {{question}}"
    )

    # Use OpenAI LLM
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    # Construct and return the retrieval-augmented QA chain
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt}
    )
