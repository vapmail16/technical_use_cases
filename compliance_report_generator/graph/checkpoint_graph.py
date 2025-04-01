from typing import TypedDict

class WorkflowState(TypedDict):
    file_path: str
    status: str
    embedding_status: str
    graph_status: str

from langgraph.graph import StateGraph, END
from typing import TypedDict
from vector_store.ingest import ingest_documents
from graph.doc_to_graph import extract_and_store_knowledge
from graph.neo4j_utils import ensure_fulltext_index
import os
import pdfplumber
from textwrap import shorten

# ✅ Ensure Neo4j index
ensure_fulltext_index()

# ✅ Define state structure
class State(TypedDict):
    file_path: str
    status: str
    embedding_status: str
    graph_status: str
    memory_status: str

# ✅ Ingest Node
def ingest_node(state: State) -> State:
    file_path = state["file_path"]
    print(f"📥 Ingesting: {file_path}")
    ingest_documents(file_path)
    return {**state, "status": "ingested"}

# ✅ Embed Node
def embed_node(state: State) -> State:
    file_path = state["file_path"]
    from vector_store.ingest import ingest_documents  # Ensure available here
    ingest_documents(file_path)
    return {**state, "embedding_status": "stored"}

# ✅ Graph Node
def graph_node(state: State) -> State:
    file_path = state["file_path"]
    try:
        with pdfplumber.open(file_path) as pdf:
            all_text = "\n".join([page.extract_text() or "" for page in pdf.pages])
        
        # Split into chunks of ~1500 words (adjust as needed)
        chunks = all_text.split("\n\n")  # Simple paragraph-based split
        max_tokens = 3000
        processed = 0

        for chunk in chunks:
            if len(chunk.strip()) == 0:
                continue

            # Truncate chunk to avoid token overflow
            short_chunk = shorten(chunk, width=12000, placeholder="...")
            extract_and_store_knowledge(short_chunk)
            processed += 1

        print(f"✅ Knowledge extracted in {processed} chunks and pushed to Neo4j.")
        return {**state, "graph_status": "stored"}

    except Exception as e:
        print(f"❌ Graph Node Error: {e}")
        return {**state, "graph_status": "failed"}

# ✅ Memory Node (Checkpoint)
def memory_node(state: State) -> State:
    file_path = state["file_path"]
    print(f"🧠 Checkpoint saved for: {file_path}")
    return {**state, "memory_status": "checkpointed"}

# ✅ LangGraph Builder
def create_checkpoint_graph():
    graph = StateGraph(WorkflowState)

    # Add nodes
    graph.add_node("ingest", ingest_node)
    graph.add_node("embed", embed_node)
    graph.add_node("graph", graph_node)
    graph.add_node("memory", memory_node)

    # Define edges
    graph.set_entry_point("ingest")
    graph.add_edge("ingest", "embed")
    graph.add_edge("embed", "graph")
    graph.add_edge("graph", "memory")
    graph.set_finish_point("memory")

    return graph.compile()
