from langchain.tools import tool
import requests
import os
from dotenv import load_dotenv
load_dotenv()

@tool
def get_compliance_news(query: str = "GDPR") -> str:
    """
    Fetches latest compliance-related news headlines for a given query.
    Defaults to 'GDPR' if no query is provided.
    """
    try:
        api_key = os.getenv("NEWS_API_KEY")  # Put in .env
        url = f"https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&pageSize=3&apiKey={api_key}"
        response = requests.get(url)
        articles = response.json().get("articles", [])

        if not articles:
            return "No relevant news found."

        headlines = [f"📰 {a['title']} ({a['source']['name']})" for a in articles]
        return "\n".join(headlines)

    except Exception as e:
        return f"Error fetching news: {e}"

if __name__ == "__main__":
    import sys
    query = sys.argv[1] if len(sys.argv) > 1 else "GDPR"
    print(get_compliance_news.run(query))

