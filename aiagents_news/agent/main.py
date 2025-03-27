from langchain.agents import initialize_agent, Tool
from langchain_openai import OpenAI
from langchain.tools import tool
import os
import requests
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import json
from datetime import datetime
import hashlib
import sys

load_dotenv()

MEMORY_PATH = "memory.json"
BLOG_DIR = "blogs"
os.makedirs(BLOG_DIR, exist_ok=True)

# --- Memory Functions ---
def load_memory():
    if os.path.exists(MEMORY_PATH):
        try:
            with open(MEMORY_PATH, "r") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except json.JSONDecodeError:
            return []
    return []

def save_to_memory(topic):
    memory = load_memory()
    if topic not in memory:
        memory.append(topic)
        with open(MEMORY_PATH, "w") as f:
            json.dump(memory, f, indent=2)

def topic_used(topic):
    return topic in load_memory()

# --- Tool: News API ---
@tool
def fetch_newsapi_headlines(topic: str) -> str:
    """Fetch recent news headlines about a topic using NewsAPI."""
    api_key = os.getenv("NEWS_API_KEY")
    url = (
        f"https://newsapi.org/v2/everything?"
        f"q={topic}&sortBy=publishedAt&language=en&apiKey={api_key}"
    )
    response = requests.get(url).json()

    if response.get("status") != "ok":
        return f"NewsAPI error: {response.get('message')}"

    articles = response.get("articles", [])[:3]
    return json.dumps([
        {"title": article["title"], "url": article["url"], "source": article["source"]["name"]}
        for article in articles
    ], indent=2)

# --- LangChain Agent ---
llm = OpenAI(temperature=0.7)

news_tool = Tool(
    name="NewsFetcher",
    func=fetch_newsapi_headlines.run,
    description="Useful for fetching latest news headlines on any topic."
)

news_selector_agent = initialize_agent(
    tools=[news_tool],
    llm=llm,
    agent="zero-shot-react-description",
    verbose=True
)

# --- Blog Prompt Templates ---
gen_prompt = PromptTemplate(
    input_variables=["topic", "headlines"],
    template="""
You are a political journalist writing a blog post.

Topic: {topic}

These are the top headlines to consider:
{headlines}

Write a compelling blog post of at least **700+ words**.  
- Make it engaging, emotional, witty, and even sarcastic at times.  
- Use storytelling, historical context, opinions, and references from the headlines.  
- Don't stop abruptly — finish with a conclusion.

Your tone should feel very **human** and **conversational**. Avoid being robotic.
"""
)

humanize_prompt = PromptTemplate(
    input_variables=["raw_blog"],
    template="""
    Improve the tone and structure of the following blog post:

    {raw_blog}

    Make it feel more human, sarcastic where needed, emotional, and immersive.
    """
)

# --- Blog Generation Pipeline ---
def blog_writer_pipeline(topic: str, headlines: str):
    chain = LLMChain(llm=llm, prompt=gen_prompt)
    blog_raw = chain.run(topic=topic, headlines=headlines)

    humanizer = LLMChain(llm=llm, prompt=humanize_prompt)
    blog_final = humanizer.run(raw_blog=blog_raw)

    blog_id = hashlib.md5((topic + str(datetime.now())).encode()).hexdigest()[:8]
    file_path = os.path.join(BLOG_DIR, f"{datetime.today().date()}_{blog_id}.md")

    with open(file_path, "w") as f:
        f.write(f"# {topic}\n\n")
        f.write(blog_final.strip())
        f.write("\n\n---\n\n")
        f.write("### Headlines Used:\n")

        try:
            headline_data = json.loads(headlines)
            for h in headline_data:
                f.write(f"- {h['title']} ({h['source']}) - {h['url']}\n")
        except:
            f.write(headlines.strip())

    save_to_memory(topic)
    print(f"\n✅ Blog saved as: {file_path}")

# --- Orchestration ---
def run_news_blog_pipeline():
    topic = input("Enter a topic to fetch news and generate blog: ")

    if topic_used(topic):
        choice = input("⚠️ This topic has already been used. Do you want to continue anyway? (y/n): ")
        if choice.lower() != "y":
            print("Cancelled.")
            sys.exit(0)

    headlines = fetch_newsapi_headlines.run(topic)
    print("\n--- News Summary ---")
    print(headlines)

    confirm = input("\nGenerate blog with above headlines? (y/n): ")
    if confirm.lower() != "y":
        print("Cancelled.")
        return

    print("\n--- Generating blog ---")
    blog_writer_pipeline(topic, headlines)

if __name__ == "__main__":
    run_news_blog_pipeline()
