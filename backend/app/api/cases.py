from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import uuid

router = APIRouter(prefix="/cases", tags=["Cases"])

# Mock database for MVP
db_cases: Dict[str, Dict[str, Any]] = {}

class CaseCreate(BaseModel):
    payer: str
    amount: float
    denial_reason: str
    procedure_code: str
    diagnosis_code: str
    member_plan: str
    notes: str
    attachments: List[str] = []

@router.post("/", status_code=201)
async def create_case(case: CaseCreate):
    case_id = f"CLM-{uuid.uuid4().hex[:8].upper()}"
    case_data = case.model_dump()
    case_data["claim_id"] = case_id
    case_data["status"] = "pending"
    
    db_cases[case_id] = case_data
    return {"case_id": case_id, "status": "created"}

@router.get("/{case_id}")
async def get_case(case_id: str):
    if case_id not in db_cases:
        raise HTTPException(status_code=404, detail="Case not found")
    return db_cases[case_id]
