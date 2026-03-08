# OpenClaw Research Agent - Usage Guide

This agent is an autonomous internet exploration tool built on the OpenClaw architecture. It researches founders or CEOs, maintains a local memory, and generates structured reports.

## Prerequisites

1.  **Python 3.8+**
2.  **Dependencies**:
    ```bash
    pip install requests beautifulsoup4 python-dotenv
    ```
3.  **API Key**: Ensure your `.env` file contains a valid `GROQ_API_KEY` or `OPENAI_API_KEY`.

## Running the Agent

To start a research task, run the `research_agent.py` script and provide the name of the person you want to research in quotes:

```powershell
python research_agent.py "Sam Altman"
```

### Examples:
- `python research_agent.py "Elon Musk"`
- `python research_agent.py "Jensen Huang"`
- `python research_agent.py "Satya Nadella"`

## Understanding the Output

As the agent runs, it will:
1.  **Initialize**: Start a session via the `Gateway`.
2.  **Search & Browse**: Find sources and fetch content using `Skills`.
3.  **Think**: Use the `Brain` (via Groq/OpenAI) to reason about the gathered information.
4.  **Store**: Save "facts" into the local `memory/knowledge/` directory in Markdown format.
5.  **Finalize**: Generate a comprehensive report in the `output/` directory.

### Key Files:
- **Memory**: `memory/knowledge/[name].md` (RAW findings)
- **Final Report**: `output/[name]_report.md` (Structured insights)

## Customization

You can modify the `Brain` model or endpoint in `openclaw/brain.py` if you wish to use different LLM providers.
