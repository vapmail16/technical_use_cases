from summary_filter_tool import summarize_and_filter

print("🧪 Summary Filter Tool Test\n")

text = input("Paste compliance text:\n")
keywords = input("Enter keywords (comma-separated, optional): ")

result = summarize_and_filter.invoke({"text": text, "keywords": keywords})
print(f"\n📝 Summary:\n{result}")
