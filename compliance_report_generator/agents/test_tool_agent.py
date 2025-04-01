from agents.tool_calling_agent import get_tool_agent

if __name__ == "__main__":
    agent = get_tool_agent()

    print("\n🧠 Ask your agent a question involving compliance, risk, or summaries:")
    while True:
        q = input("💬> ")
        if q.lower() in ["exit", "quit"]:
            break
        result = agent.run(q)
        print(f"\n🧾 Response:\n{result}\n")
