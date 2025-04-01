from graph.checkpoint_graph import create_checkpoint_graph

workflow = create_checkpoint_graph()

state = {
    "file_path": "uploaded_docs/CELEX_32016R0679_EN_TXT.pdf",
    "status": "",
    "embedding_status": "",
    "graph_status": "",
    "memory_status": ""
}

final_state = workflow.invoke(state)
print(final_state)
