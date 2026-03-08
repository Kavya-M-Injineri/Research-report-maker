import os
import sys
# Add parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import io
import contextlib
import threading
import queue
import uuid
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from research_agent import ResearchAgent

app = FastAPI()

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for task logs and reports
tasks = {}

class ResearchRequest(BaseModel):
    target: str

class RedirectStdout:
    def __init__(self, task_id):
        self.task_id = task_id
        self.queue = queue.Queue()

    def write(self, data):
        if data.strip():
            tasks[self.task_id]["logs"].append(data.strip())

    def flush(self):
        pass

def run_research_task(task_id, target):
    tasks[task_id]["status"] = "running"
    
    # Catching print statements for the UI
    f = io.StringIO()
    with contextlib.redirect_stdout(RedirectStdout(task_id)):
        try:
            agent = ResearchAgent(target)
            report_path = agent.run()
            tasks[task_id]["status"] = "completed"
            tasks[task_id]["report_path"] = report_path
            with open(report_path, "r", encoding="utf-8") as rf:
                tasks[task_id]["report"] = rf.read()
        except Exception as e:
            tasks[task_id]["status"] = "failed"
            tasks[task_id]["logs"].append(f"Fatal Error: {str(e)}")

@app.post("/research")
async def start_research(request: ResearchRequest, background_tasks: BackgroundTasks):
    task_id = str(uuid.uuid4())
    tasks[task_id] = {
        "target": request.target,
        "status": "pending",
        "logs": [],
        "report": None
    }
    background_tasks.add_task(run_research_task, task_id, request.target)
    return {"task_id": task_id}

@app.get("/status/{task_id}")
async def get_status(task_id: str):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[task_id]

@app.get("/latest-report/{target}")
async def get_latest_report(target: str):
    # Just a helper to get the latest file if it exists
    filename = f"output/{target.lower().replace(' ', '_')}_report.md"
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return {"report": f.read()}
    return {"report": None}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
