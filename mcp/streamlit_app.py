# streamlit_app.py

import streamlit as st
from main import app  # This uses LangGraph app from main.py

st.set_page_config(page_title="TweetGen 🧵", layout="wide")

st.title("🧠 Blog to Twitter Threads Generator")
st.markdown("Paste your blog below and generate 5 tweet threads (10 tweets each).")

blog_input = st.text_area("📝 Blog Input", height=300)

if st.button("🚀 Generate Threads"):
    if not blog_input.strip():
        st.warning("Please paste a blog first!")
    else:
        with st.spinner("Generating tweet hooks and threads..."):
            result = app.invoke({"blog": blog_input})

        st.success("✅ Threads Generated!")

        for i, thread in enumerate(result["threads"], 1):
            st.markdown(f"### 🧵 Thread {i}: {thread['lead']}")
            for j, tweet in enumerate(thread['thread'], 1):
                st.markdown(f"- **{j}.** {tweet}")
