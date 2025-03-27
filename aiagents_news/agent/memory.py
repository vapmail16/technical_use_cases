# agent/memory.py

import os
import json
from datetime import datetime

MEMORY_FILE = "agent/memory.json"

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def mark_topic_used(topic, memory):
    memory[topic.lower()] = {
        "last_used": datetime.now().isoformat()
    }

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

def has_topic_been_used(topic, memory):
    normalized = topic.strip().lower()
    return normalized in (key.strip().lower() for key in memory.keys())

