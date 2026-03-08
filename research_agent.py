from openclaw.gateway import Gateway
from openclaw.brain import Brain
from openclaw.memory import Memory
from openclaw.skills.browser import WebSearch, Browser
from openclaw.skills.extractor import DataExtractor
import os

class ResearchAgent:
    def __init__(self, target_name):
        self.target_name = target_name
        self.gateway = Gateway()
        self.memory = Memory()
        self.brain = Brain()
        self.skills = {
            "search": WebSearch(),
            "browser": Browser(),
            "extractor": DataExtractor(brain=self.brain)
        }
        self.session_id = self.gateway.create_session("User1", f"Research {target_name}")

    def run(self):
        print(f"\n--- Starting Research Workflow for: {self.target_name} ---\n")
        
        # Step 1: Initialize research
        self.gateway.update_session(self.session_id, f"Initializing research for {self.target_name}", role="system")
        
        # Step 2: Execute ReAct loop via the Brain
        report = self.brain.reason_and_act(self.target_name, self.skills, self.memory)
        
        # Step 3: Finalize
        print("\n--- Research Complete ---\n")
        print("FINAL REPORT (Snippet):\n")
        print(report[:500] + "...")
        
        # Save to output folder
        if not os.path.exists("output"):
            os.makedirs("output")
        report_path = f"output/{self.target_name.lower().replace(' ', '_')}_report.md"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"\nSaved full report to: {report_path}")
        return report_path

if __name__ == "__main__":
    import sys
    name = sys.argv[1] if len(sys.argv) > 1 else "Sam Altman"
    agent = ResearchAgent(name)
    agent.run()
