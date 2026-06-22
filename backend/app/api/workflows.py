from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.api.cases import db_cases
from app.agents.graph import claim_graph

router = APIRouter(prefix="/workflows", tags=["Workflows"])

# In-memory store for workflow results
db_workflow_results = {}

def run_workflow_background(case_id: str, case_data: dict):
    initial_state = {
        "claim_id": case_id,
        "claim_data": case_data,
        "messages": []
    }
    
    try:
        # Run the LangGraph orchestration
        result = claim_graph.invoke(initial_state)
        
        db_workflow_results[case_id] = {
            "status": "completed",
            "evaluation": result.get("evaluation_result", {}),
            "evidence_count": len(result.get("retrieved_evidence", [])),
            "messages": result.get("messages", [])
        }
        db_cases[case_id]["status"] = "resolved"
        
    except Exception as e:
        db_workflow_results[case_id] = {
            "status": "failed",
            "error": str(e)
        }
        db_cases[case_id]["status"] = "error"

@router.post("/{case_id}/run", status_code=202)
async def trigger_workflow(case_id: str, background_tasks: BackgroundTasks):
    if case_id not in db_cases:
        raise HTTPException(status_code=404, detail="Case not found")
        
    case_data = db_cases[case_id]
    if case_data.get("status") in ["processing", "resolved"]:
        raise HTTPException(status_code=400, detail="Workflow already running or completed")
        
    db_cases[case_id]["status"] = "processing"
    db_workflow_results[case_id] = {"status": "running"}
    
    background_tasks.add_task(run_workflow_background, case_id, case_data)
    
    return {"case_id": case_id, "message": "Workflow triggered successfully"}

@router.get("/{case_id}/summary")
async def get_workflow_summary(case_id: str):
    if case_id not in db_workflow_results:
        raise HTTPException(status_code=404, detail="No workflow run found for this case")
        
    return db_workflow_results[case_id]
