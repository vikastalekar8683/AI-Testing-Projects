
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

# Add parent directory to path to import tools
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.ollama_tool import generate_completion

app = FastAPI(title="Pilot Backend")

# Enable CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Pilot Backend is active",
        "docs": "/docs",
        "health": "/api/health"
    }

@app.post("/api/generate")
async def generate(request: Request):
    data = await request.json()
    model = data.get("model", "qwen3:4b")
    prompt = data.get("prompt", "")
    
    async def event_generator():
        async for chunk in generate_completion(model, prompt):
            yield chunk

    return StreamingResponse(event_generator(), media_type="text/plain")

@app.get("/api/health")
async def health():
    print("Health Check Received")
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
