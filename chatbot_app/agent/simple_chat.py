from chat_chain import get_conversation_chain

def run_cli_chat():
    print("🧠 LangChain Chatbot (type 'exit' to quit)")
    conversation = get_conversation_chain()

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye! 👋")
            break

        response = conversation.predict(input=user_input)
        print(f"AI: {response}\n")

if __name__ == "__main__":
    run_cli_chat()
