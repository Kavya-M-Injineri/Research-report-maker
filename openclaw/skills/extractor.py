class DataExtractor:
    def __init__(self, brain=None):
        self.brain = brain

    def extract_structured_data(self, raw_text, schema):
        print(f"[Skill: DataExtractor] Extracting data from text...")
        # This skill normally uses the Brain's LLM to process text
        # For our implementation, we'll provide a prompt to the brain
        prompt = f"Extract structured information from the following text based on this schema: {schema}\n\nText: {raw_text[:2000]}..."
        if self.brain:
            return self.brain.think(prompt)
        return "Brain not initialized for extraction."
