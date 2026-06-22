from typing import Dict, Any
from pydantic import BaseModel, Field
from app.agents.state import AgentState
from app.services.retrieval_service import retrieval_service
from app.services.groq_service import primary_llm_service

class EvaluationOutput(BaseModel):
    decision: str = Field(description="The final decision: 'Approved', 'Denied', or 'Requires Manual Review'")
    confidence_score: float = Field(description="Confidence score between 0.0 and 1.0")
    reasoning: str = Field(description="Detailed explanation for the decision based on the evidence")

def ingest_node(state: AgentState) -> Dict[str, Any]:
    """
    Validates and prepares the claim data for processing.
    """
    claim_data = state.get("claim_data", {})
    claim_id = state.get("claim_id", "Unknown")
    
    return {
        "status": "ingested",
        "messages": [f"Claim {claim_id} ingested successfully."]
    }

def retrieve_node(state: AgentState) -> Dict[str, Any]:
    """
    Retrieves relevant policy and historical evidence from Qdrant.
    """
    claim_data = state.get("claim_data", {})
    procedure_code = claim_data.get("procedure_code", "")
    diagnosis_code = claim_data.get("diagnosis_code", "")
    
    # Formulate a query to find relevant policies and history
    query = f"procedure code {procedure_code} diagnosis code {diagnosis_code}"
    
    # Fetch evidence
    policies = retrieval_service.search_evidence(query=query, category="policy", top_k=2)
    history = retrieval_service.search_evidence(query=query, category="historical_note", top_k=2)
    
    evidence = policies + history
    
    return {
        "retrieved_evidence": evidence,
        "status": "retrieved",
        "messages": [f"Retrieved {len(evidence)} pieces of evidence."]
    }

def evaluate_node(state: AgentState) -> Dict[str, Any]:
    """
    Evaluates the claim using Groq LLM based on retrieved evidence.
    """
    claim_data = state.get("claim_data", {})
    evidence = state.get("retrieved_evidence", [])
    
    system_prompt = (
        "You are an expert medical claims adjudicator. "
        "Review the provided claim data against the retrieved policy and historical evidence. "
        "Determine if the claim should be Approved, Denied, or if it Requires Manual Review. "
        "You must output valid structured JSON matching the schema."
    )
    
    evidence_text = "\n".join([f"- [{e.get('category')}] {e.get('text')}" for e in evidence])
    
    prompt = (
        f"Claim Data:\n{claim_data}\n\n"
        f"Retrieved Evidence:\n{evidence_text}\n\n"
        f"Evaluate this claim."
    )
    
    result = primary_llm_service.invoke_structured(
        prompt=prompt,
        schema=EvaluationOutput,
        system_prompt=system_prompt
    )
    
    return {
        "evaluation_result": result.model_dump(),
        "status": "evaluated",
        "messages": [f"Evaluation complete: {result.decision}"]
    }
