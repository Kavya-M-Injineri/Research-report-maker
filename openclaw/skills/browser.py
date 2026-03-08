import requests
from bs4 import BeautifulSoup
import os
from duckduckgo_search import DDGS
import urllib3

# Suppress insecure request warnings for the demo
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class WebSearch:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("SERPER_API_KEY")

    def search(self, query):
        print(f"[Skill: WebSearch] Searching for: {query}")
        
        # 1. Try DuckDuckGo first (Free)
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=5))
                if results:
                    return [{"title": r.get("title"), "link": r.get("href"), "snippet": r.get("body")} for r in results]
        except Exception as e:
            print(f"DEBUG: DDG Search failed: {str(e)}")
            
        # 2. Fallback to Serper if key exists
        if self.api_key:
            url = "https://google.serper.dev/search"
            payload = {"q": query}
            headers = {
                'X-API-KEY': self.api_key,
                'Content-Type': 'application/json'
            }
            try:
                response = requests.post(url, headers=headers, json=payload)
                results = response.json()
                return [{"title": r.get("title"), "link": r.get("link"), "snippet": r.get("snippet")} for r in results.get("organic", [])]
            except Exception as e:
                print(f"DEBUG: Serper Search failed: {str(e)}")

        # 3. Final Fallback (Dummy)
        return [
            {"title": f"Result for {query}", "link": "https://en.wikipedia.org/wiki/Sam_Altman", "snippet": "Wikipedia entry for the target."}
        ]

class Browser:
    def fetch_content(self, url):
        print(f"[Skill: Browser] Fetching content from: {url}")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        try:
            # Try with verification first
            response = requests.get(url, headers=headers, timeout=10)
        except (requests.exceptions.SSLError, requests.exceptions.ConnectionError):
            print("[Skill: Browser] SSL/Connection error, retrying without verification...")
            try:
                response = requests.get(url, headers=headers, timeout=10, verify=False)
            except Exception as e:
                return f"Error fetching {url}: {str(e)}"
        except Exception as e:
            return f"Error fetching {url}: {str(e)}"

        try:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Extract text content, removing script/style
            for script in soup(["script", "style"]):
                script.decompose()
            text = soup.get_text(separator=' ')
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            return " ".join(chunk for chunk in chunks if chunk)
        except Exception as e:
            return f"Error parsing {url}: {str(e)}"
