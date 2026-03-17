# OpenClaw Research Agent
.
An **autonomous AI research agent** that takes a founder or CEO's name, searches the internet, reasons over gathered content, and produces a structured intelligence report — with persistent local memory between runs.

---

## Highlights

- Built a **multi-stage autonomous agent pipeline** — search → browse → reason → store → report — using a modular architecture (Gateway, Skills, Brain)
- Integrated **Groq and OpenAI LLM backends** as swappable reasoning engines via a unified `Brain` abstraction in `openclaw/brain.py`
- Implemented **persistent local memory** using Markdown files, allowing the agent to accumulate and reference prior findings across sessions
- Used **BeautifulSoup4** for web content extraction and **Requests** for source fetching, with structured fact parsing before LLM reasoning
- Designed for **CLI-first usage** — single command execution with named output files per subject for easy review and comparison

---

## Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3.8+ |
| LLM Backend | Groq API / OpenAI API (swappable) |
| Web Scraping | Requests, BeautifulSoup4 |
| Config | python-dotenv |
| Memory | Local Markdown file store |

---

## Agent Architecture

```
Gateway          ← Session init, orchestration
  └── Skills     ← Web search + content fetching (BeautifulSoup4)
  └── Brain      ← LLM reasoning layer (Groq / OpenAI)
  └── Memory     ← Persistent Markdown knowledge store
  └── Reporter   ← Structured report generation
```

---

## Setup

```bash
pip install requests beautifulsoup4 python-dotenv
```

Create a `.env` file:
```
GROQ_API_KEY=your_key_here
# or
OPENAI_API_KEY=your_key_here
```

---

## Usage

```bash
python research_agent.py "Sam Altman"
python research_agent.py "Jensen Huang"
python research_agent.py "Satya Nadella"
```

---

## Output

| File | Contents |
|---|---|
| `memory/knowledge/[name].md` | Raw extracted facts, updated per run |
| `output/[name]_report.md` | Final structured research report |

---

## Customization

Swap LLM providers by editing `openclaw/brain.py` — the Brain abstraction supports any OpenAI-compatible endpoint.
