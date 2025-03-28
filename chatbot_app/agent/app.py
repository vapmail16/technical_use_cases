import streamlit as st
from chat_chain import get_conversation_chain
from langchain.callbacks import get_openai_callback
from moderation import moderate_input  # ✅ Add this

st.set_page_config(page_title="LangChain Tool + Memory Chatbot", page_icon="🤖")
st.title("🧠 Ask me anything!")

# ✅ Load the conversation chain (includes memory)
conversation = get_conversation_chain()

# ✅ Display memory messages from LangChain
for msg in conversation.memory.chat_memory.messages:
    role = "user" if msg.type == "human" else "assistant"
    with st.chat_message(role):
        st.markdown(msg.content)

# ✅ Input box
if prompt := st.chat_input("Type your message here..."):

    # ✅ Run moderation BEFORE LLM call
    is_safe, categories = moderate_input(prompt)
    if not is_safe:
        flagged = ", ".join([k for k in categories.__dict__ if getattr(categories, k)])
        st.error(f"❌ Input flagged for: {flagged}")
        st.stop()

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with get_openai_callback() as cb:
            response = conversation.run(prompt)
            st.markdown(response)

        st.markdown(
            f"🔢 Tokens used: {cb.total_tokens} (prompt: {cb.prompt_tokens}, completion: {cb.completion_tokens})"
        )
