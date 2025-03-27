import requests
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def generate_outline(topic):
    prompt = f"Create a 3-point blog outline on the topic: {topic}"
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful blog writing assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

def fetch_news_snippets(topic):
    print("🔎 Searching real news using NewsAPI...")
    url = (
        f"https://newsapi.org/v2/everything?"
        f"q={topic}&"
        f"sortBy=publishedAt&"
        f"language=en&"
        f"apiKey={NEWS_API_KEY}"
    )

    response = requests.get(url)
    data = response.json()

    if data.get("status") != "ok":
        print("❌ Failed to fetch news.")
        print(f"📦 NewsAPI Response: {data}")
        return []

    articles = data.get("articles", [])[:3]  # Take top 3
    snippets = []

    for article in articles:
        content = article.get("content") or article.get("description") or ""
        title = article.get("title", "")
        url = article.get("url", "")
        if content:
            snippets.append(f"{title}: {content.strip()} (Source: {url})")

    return snippets

def generate_blog_post(topic, outline, research):
    research_text = "\n".join(research)
    prompt = f"""Write a 300-word blog post on "{topic}".
Use this outline: {outline}
Incorporate this research (each with source link) and cite explicitly in parentheses:
{research_text}

Make sure to reference the sources inline like this: (Source: https://example.com).
Make the tone clear, engaging, and human-like."""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a brilliant blog writer."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

def humanize_blog(blog_text):
    prompt = f"""Rewrite the following blog post to sound more human, emotional, and narrative-driven.
Make it feel like it was written by a passionate storyteller:

{blog_text}
"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a creative storyteller and editor."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()
