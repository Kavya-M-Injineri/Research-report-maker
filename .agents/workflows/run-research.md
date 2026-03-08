---
description: How to run the OpenClaw Research Agent
---

To run the research agent for a specific target (founder or CEO), follow these steps:

1.  **Ensure dependencies are installed**:
    ```bash
    pip install requests beautifulsoup4 python-dotenv
    ```

2.  **Set your API Key**:
    Open the `.env` file and ensure your `GROQ_API_KEY` (or `OPENAI_API_KEY`) is present.

3.  **Run the Research Command**:
    Replace `"Sam Altman"` with the person you wish to research.
    ```bash
    python research_agent.py "Sam Altman"
    ```

4.  **View Results**:
    - Compiled Report: `output/[target_name]_report.md`
    - Research Memory: `memory/knowledge/[target_name].md`
