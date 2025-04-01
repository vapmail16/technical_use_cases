
from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

# Initialize driver
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

def ensure_fulltext_index():
    # ✅ Works in Neo4j Aura & local: safer, more portable
    query = """
    CREATE FULLTEXT INDEX entityIndex IF NOT EXISTS
    FOR (n:Entity) ON EACH [n.name]
    """
    try:
        with driver.session() as session:
            session.run(query)
            print("✅ entityIndex ensured.")
    except Exception as e:
        print(f"⚠️ Failed to create entityIndex: {e}")

def add_triple(subject, relation, obj):
    query = """
    MERGE (s:Entity {name: $subject})
    MERGE (o:Entity {name: $object})
    MERGE (s)-[:RELATION {type: $relation}]->(o)
    """
    try:
        with driver.session() as session:
            session.run(query, subject=subject, object=obj, relation=relation)
        print(f"🔗 Added to graph: ({subject}) -[{relation}]-> ({obj})")
    except Exception as e:
        print(f"⚠️ Failed to add triple: {e}")

def run_cypher_query(question):
    if not question.strip():
        return "⚠️ No graph query executed — question was empty."

    query = f"""
    CALL db.index.fulltext.queryNodes('entityIndex', '{question}')
    YIELD node, score
    RETURN node.name AS name, labels(node) AS labels
    LIMIT 5
    """
    results = []
    try:
        with driver.session() as session:
            output = session.run(query)
            for record in output:
                results.append(f"{record['labels'][0]}: {record['name']}")
    except Exception as e:
        print(f"⚠️ Failed to run fulltext search: {e}")
        results.append("⚠️ Fulltext index missing or query failed.")

    return "\n".join(results) or "No graph entities matched."

# Optional: Ensure index at import
ensure_fulltext_index()
