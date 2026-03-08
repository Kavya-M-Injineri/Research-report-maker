import os
import json
from datetime import datetime

class Memory:
    def __init__(self, base_dir="memory"):
        self.base_dir = base_dir
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)
        self.knowledge_dir = os.path.join(self.base_dir, "knowledge")
        if not os.path.exists(self.knowledge_dir):
            os.makedirs(self.knowledge_dir)

    def store_fact(self, entity, fact, source="unknown"):
        timestamp = datetime.now().isoformat()
        filename = f"{entity.lower().replace(' ', '_')}.md"
        filepath = os.path.join(self.knowledge_dir, filename)
        
        entry = f"## {timestamp}\n- **Source**: {source}\n- **Fact**: {fact}\n\n"
        
        with open(filepath, "a", encoding="utf-8") as f:
            f.write(entry)
        return filepath

    def get_context(self, entity):
        filename = f"{entity.lower().replace(' ', '_')}.md"
        filepath = os.path.join(self.knowledge_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read()
        return "No prior knowledge found."

    def list_known_entities(self):
        return [f.replace(".md", "") for f in os.listdir(self.knowledge_dir)]
