from langchain.agents import initialize_agent, Tool
from langchain_community.chat_models import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.memory import ConversationBufferMemory
import os
from dotenv import load_dotenv

load_dotenv()

# ✅ Create LLM
llm = ChatOpenAI(
    temperature=0,
    model_name="gpt-3.5-turbo"
)

# ✅ Add tool (DuckDuckGo Search)
search = DuckDuckGoSearchRun()

# ✅ Setup memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# ✅ Create Agent with tools + memory
def get_conversation_chain():
    tools = [
        Tool(
            name="Search",
            func=search.run,
            description="Use this tool for answering general knowledge or real-time questions"
        )
    ]

    agent_chain = initialize_agent(
        tools=tools,
        llm=llm,
        agent="chat-conversational-react-description",
        memory=memory,
        verbose=True,
        handle_parsing_errors=True,
    )
    return agent_chain

def get_memory():
    return memory
