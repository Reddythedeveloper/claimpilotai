import pytest
from app.agents.graph import claim_graph

def test_graph_compile():
    # Just ensure the graph is built and compiled correctly
    assert claim_graph is not None

def test_graph_execution_mocked(monkeypatch, mocker):
    # Mock retrieval service
    mocker.patch("app.agents.nodes.retrieval_service.search_evidence", return_value=[{"category": "policy", "text": "mock evidence"}])
    
    # Mock LLM service structured output
    mock_llm = mocker.patch("app.agents.nodes.primary_llm_service.invoke_structured")
    from app.agents.nodes import EvaluationOutput
    mock_llm.return_value = EvaluationOutput(decision="Approved", confidence_score=0.9, reasoning="Mocked reason")

    initial_state = {
        "claim_id": "CLM-TEST",
        "claim_data": {"procedure_code": "12345", "diagnosis_code": "ABC"},
        "messages": []
    }
    
    result = claim_graph.invoke(initial_state)
    
    assert result["status"] == "evaluated"
    assert result["evaluation_result"]["decision"] == "Approved"
    assert len(result["retrieved_evidence"]) == 2 # Because retrieval service is called twice
    assert "Mocked reason" in result["evaluation_result"]["reasoning"]
