from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from tools.registry import TOOLS

def get_tool_agent():
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    agent_executor = initialize_agent(
        tools=TOOLS,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )

    return agent_executor
