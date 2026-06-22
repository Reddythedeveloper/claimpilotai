import operator
from typing import TypedDict, Annotated, List, Dict, Any

class AgentState(TypedDict):
    # The original claim payload
    claim_id: str
    claim_data: Dict[str, Any]
    
    # Information retrieved by the Retrieval node
    retrieved_evidence: List[Dict[str, Any]]
    
    # Final evaluation from the Evaluator node
    evaluation_result: Dict[str, Any]
    
    # Current status in the workflow
    status: str
    
    # Messages or reasoning logs (appended at each step)
    messages: Annotated[List[str], operator.add]
