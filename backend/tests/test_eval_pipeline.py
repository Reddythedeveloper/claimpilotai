import json
import os
import pytest
from app.agents.graph import claim_graph

def load_eval_dataset():
    file_path = os.path.join(os.path.dirname(__file__), "eval_dataset.json")
    with open(file_path, "r") as f:
        return json.load(f)

@pytest.mark.parametrize("case", load_eval_dataset())
def test_agent_accuracy(case):
    # 1. Prepare initial state
    initial_state = {
        "claim_id": case["case_id"],
        "claim_data": case["case_data"],
        "messages": []
    }
    
    # 2. Run the graph end-to-end (This will hit the real Groq API)
    result = claim_graph.invoke(initial_state)
    
    # 3. Extract evaluation output
    evaluation = result.get("evaluation_result", {})
    decision = evaluation.get("decision")
    reasoning = evaluation.get("reasoning", "")
    retrieved_evidence = result.get("retrieved_evidence", [])
    
    # 4. Guardrail: Decision Accuracy Check
    # Ensure the LLM came to the expected logical conclusion
    assert decision == case["expected_decision"], f"Expected {case['expected_decision']}, but got {decision} for {case['case_id']}"
    
    # 5. Guardrail: Grounding Check
    # Ensure the evidence actually contained the expected keywords
    evidence_text = " ".join([e.get("text", "").lower() for e in retrieved_evidence])
    for keyword in case["expected_evidence_keywords"]:
        assert keyword.lower() in evidence_text, f"Grounding failed: missing '{keyword}' in evidence for {case['case_id']}"
    
    # 6. Guardrail: Hallucination/Consistency Check
    # Ensure the confidence score is above a threshold (e.g. 0.7)
    confidence = evaluation.get("confidence_score", 0.0)
    assert confidence >= 0.7, f"Confidence too low ({confidence}) for {case['case_id']}"
