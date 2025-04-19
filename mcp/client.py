# client.py

import requests
import os
from dotenv import load_dotenv

load_dotenv()

MCP_SERVER = "http://localhost:8080"  # Default LangSmit MCP port

def call_tool(tool_name, input_data):
    url = f"{MCP_SERVER}/tools/{tool_name}"
    response = requests.post(url, json={"input": input_data})
    if response.status_code == 200:
        return response.json()["output"]
    else:
        print(f"❌ Error from {tool_name}:", response.text)
        return []

def run_blog_to_threads(blog):
    print("🔍 Generating tweet hooks...\n")
    tweets = call_tool("blog_to_tweets", blog)
    if not tweets:
        print("No tweet hooks returned.")
        return

    print(f"✅ Got {len(tweets)} tweet hooks.\n")
    all_threads = []
    
    for i, tweet in enumerate(tweets, 1):
        print(f"🧵 Expanding Tweet {i}: {tweet}\n")
        thread = call_tool("expand_tweet", tweet)
        all_threads.append((tweet, thread))
    
    print("\n📢 Final Thread Output:")
    for i, (lead, thread) in enumerate(all_threads, 1):
        print(f"\n🔹 Thread {i}: {lead}")
        for j, t in enumerate(thread, 1):
            print(f"  {j}. {t}")
    
    return all_threads

if __name__ == "__main__":
    blog_input = input("📥 Paste your blog content:\n\n")
    run_blog_to_threads(blog_input)
