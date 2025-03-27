import os
from dotenv import load_dotenv
from agent.tools import generate_outline, fetch_news_snippets, generate_blog_post, humanize_blog
from agent.memory import load_memory, save_memory, has_topic_been_used, mark_topic_used
import datetime

def main():
    load_dotenv()
    memory = load_memory()

    topic = input("🧠 Enter a blog topic: ").strip()

    # 🧠 Normalize topic key
    topic_key = topic.lower()

    if has_topic_been_used(topic_key, memory):
     confirm = input(f"⚠️ This topic has been used before. Do you want to write on it again? (y/n): ").lower()
     if confirm != "y":
        print("❌ Exiting. Try with a different topic.")
        return

    print("\n📝 Generating outline...")
    outline = generate_outline(topic)
    print(f"\n🧩 Outline:\n{outline}")

    print("\n🗞️ Fetching related news snippets...")
    news_snippets = fetch_news_snippets(topic)
    print(f"\n📰 News Snippets:\n{news_snippets}")

    print("\n✍️ Writing blog post...")
    blog = generate_blog_post(topic, outline, news_snippets)

    print("\n✅ Your Blog Post:\n")
    print(blog)

    print("\n🧠 Humanizing blog post...")
    human_blog = humanize_blog(blog)

    print("\n✨ Final Humanized Blog:\n")
    print(human_blog)

    confirm_save = input("\n👤 Do you want to save this blog post? (y/n): ").lower()
    if confirm_save != "y":
        print("❌ Blog not saved. Exiting.")
        return
    
    # ✅ Save to memory
    mark_topic_used(topic, memory)
    save_memory(memory)
    print("✅ Memory updated with:", topic_key)
    

    filename = f"blogs/{topic.lower().replace(' ', '_')}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(filename, "w") as f:
        f.write(f"# Blog: {topic}\n\n")
        f.write(blog)

    print(f"\n💾 Blog saved to: {filename}")

    print("✅ Memory updated with:", topic.lower())

if __name__ == "__main__":
    main()
