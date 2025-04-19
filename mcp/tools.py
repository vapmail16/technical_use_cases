from langchain_core.tools import tool
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

@tool
def blog_to_tweets(blog: str) -> list:
    """Extracts 5 tweet hooks from a given blog."""
    prompt = f"Extract 5 engaging tweet hooks from this blog:\n\n{blog}"
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return [line.strip("- ").strip() for line in response.choices[0].message.content.split("\n") if line.strip()]

@tool
def expand_tweet(tweet: str) -> list:
    """Expands a single tweet hook into a 10-part Twitter thread."""
    prompt = f"Write a 10-part Twitter thread expanding on:\n\n{tweet}"
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return [line.strip("- ").strip() for line in response.choices[0].message.content.split("\n") if line.strip()]
