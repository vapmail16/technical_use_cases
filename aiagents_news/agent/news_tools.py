from langchain.tools import tool
import os
import requests
from dotenv import load_dotenv

load_dotenv()

# NewsAPI Tool
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
    return "\n".join(
        [f"{article['title']} - {article['url']}" for article in articles]
    )
