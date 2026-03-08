import os
import requests
from dotenv import load_dotenv

load_dotenv()

class Brain:
    def __init__(self, api_key=None, model=None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY") or os.getenv("OPENAI_API_KEY")
        if self.api_key and self.api_key.startswith("gsk_"):
            self.endpoint = "https://api.groq.com/openai/v1/chat/completions"
            self.model = model or "llama-3.3-70b-versatile"
        else:
            self.endpoint = "https://api.openai.com/v1/chat/completions"
            self.model = model or "gpt-4o"

    def think(self, prompt, context=""):
        print(f"[Brain: Thinking] Processing task via {self.endpoint}...")
        # For our demonstration, if no API key, we return a mock plan/thought
        if not self.api_key:
            return "No API key found. (Simulating thinking...)"

        url = self.endpoint
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": f"You are an expert research agent. Context: {context}"},
                {"role": "user", "content": prompt}
            ]
        }
        try:
            response = requests.post(url, headers=headers, json=data)
            res_json = response.json()
            if "choices" in res_json:
                return res_json["choices"][0]["message"]["content"]
            else:
                print(f"DEBUG: OpenAI Response: {res_json}")
                return f"Brain Error: {res_json.get('error', {}).get('message', 'Unknown error')}"
        except Exception as e:
            return f"Brain Error: {str(e)}"

    def reason_and_act(self, goal, skills, memory):
        print(f"[Brain: ReAct Loop] Starting research for: {goal}")
        thought_process = []
        
        # Simple ReAct Loop simulation for the assignment
        # 1. Search for basic info
        thought = f"Thought: I need to search for basic info about {goal} to get a broad overview."
        thought_process.append(thought)
        print(thought)
        
        results = skills["search"].search(f"{goal} biography CEO founder")
        observation = f"Observation: Found {len(results)} potential sources."
        thought_process.append(observation)
        
        # 2. Extract context from a source
        if results:
            first_link = results[0]["link"]
            content = skills["browser"].fetch_content(first_link)
            memory.store_fact(goal, content[:500], source=first_link) # store a snippet
            
            thought = "Thought: I have gathered basic information. Now I will synthesize it into a report."
            thought_process.append(thought)
            print(thought)
            
            report = self.think(f"Generate a structured report for {goal} based on this text: {content[:2000]}")
            return report
        return "Failed to find any information."

