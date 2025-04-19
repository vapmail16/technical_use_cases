# main.py

from langgraph.graph import END, StateGraph
from tools import blog_to_tweets, expand_tweet
from pydantic import BaseModel
from typing import List, Optional

# ✅ Define schema using Pydantic
class TweetGenState(BaseModel):
    blog: str
    tweets: Optional[List[str]] = []
    threads: Optional[List[dict]] = []

# Tool wrappers
def generate_tweet_hooks(state: TweetGenState):
    tweet_hooks = blog_to_tweets.invoke(state.blog)
    return {"tweets": tweet_hooks}

def expand_all_tweets(state: TweetGenState):
    threads = []
    for tweet in state.tweets:
        thread = expand_tweet.invoke(tweet)
        threads.append({"lead": tweet, "thread": thread})
    return {"threads": threads}

# ✅ Build LangGraph
builder = StateGraph(TweetGenState)
builder.add_node("extract_tweets", generate_tweet_hooks)
builder.add_node("expand_threads", expand_all_tweets)

builder.set_entry_point("extract_tweets")
builder.add_edge("extract_tweets", "expand_threads")
builder.add_edge("expand_threads", END)

app = builder.compile()
