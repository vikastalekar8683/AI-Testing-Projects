from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles

import os
from dotenv import load_dotenv

# Import Layer 3 Deterministic Tools
from tools.jira_fetcher import fetch_jira_issue, test_jira_connection
from tools.llm_generator import generate_test_plan

# Layer 2: Routing / Navigation Orchestrator
app = FastAPI(title="Intelligent Test Plan Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Since frontend is static HTML
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve Frontend
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
def read_root():
    from fastapi.responses import FileResponse
    return FileResponse("frontend/index.html")


load_dotenv()

class JiraFetchRequest(BaseModel):
    issue_id: str

class GeneratePlanRequest(BaseModel):
    issue_payload: dict
    llm_type: str = "local"
    model_name: str = "gpt-oss:120b"

@app.post("/api/jira/fetch")
def route_fetch_jira(req: JiraFetchRequest):
    """Orchestrates fetching the Jira issue"""
    try:
        payload = fetch_jira_issue(req.issue_id)
        return {"status": "success", "data": payload}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/jira/test")
def route_test_jira():
    """Tests the Jira connection"""
    try:
        user_info = test_jira_connection()
        return {"status": "success", "message": user_info}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/generate")
def route_generate_plan(req: GeneratePlanRequest):
    """Orchestrates passing Jira payload to the LLM"""
    try:
        test_plan = generate_test_plan(
            jira_payload=req.issue_payload,
            llm_type=req.llm_type,
            model_name=req.model_name
        )
        return {"status": "success", "data": test_plan}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

