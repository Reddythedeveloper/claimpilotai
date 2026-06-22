from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import cases, workflows

app = FastAPI(
    title="ClaimPilot AI API",
    description="Backend API for ClaimPilot AI multi-agent platform",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(cases.router)
app.include_router(workflows.router)

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "ClaimPilot AI API is healthy"}
