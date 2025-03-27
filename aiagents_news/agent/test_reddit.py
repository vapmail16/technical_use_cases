import os
from dotenv import load_dotenv
import praw

load_dotenv()

print("Loaded Reddit credentials:")
print("USER:", os.getenv("REDDIT_USERNAME"))
print("PASS:", os.getenv("REDDIT_PASSWORD"))
print("ID:", os.getenv("REDDIT_CLIENT_ID"))
print("SECRET:", os.getenv("REDDIT_CLIENT_SECRET"))

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT"),
    username=os.getenv("REDDIT_USERNAME"),
    password=os.getenv("REDDIT_PASSWORD")
)

print("\n🔍 Searching Reddit...\n")
for post in reddit.subreddit("news").search("AI in politics", sort="top", limit=3):
    print(post.title, "-", post.url)
