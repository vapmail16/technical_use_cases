from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from graph.neo4j_utils import add_triple

# Step 1: Define the Pydantic schema
class Triple(BaseModel):
    subject: str = Field(..., description="Subject of the relationship")
    relation: str = Field(..., description="Type of relationship")
    object: str = Field(..., description="Object of the relationship")

class TripletOutput(BaseModel):
    triplets: list[Triple]

# Step 2: Run structured extraction
def extract_and_store_knowledge(text: str):
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    runnable = llm.with_structured_output(TripletOutput)

    print("🔍 Extracting structured knowledge...")
    response = runnable.invoke(
    f"Extract subject-relation-object triplets from the following compliance document text:\n\n{text}"
)

    for triple in response.triplets:
        add_triple(triple.subject, triple.relation, triple.object)
        print(f"✅ Added: {triple.subject} -[{triple.relation}]-> {triple.object}")
