import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.api.cases import db_cases
from app.api.workflows import db_workflow_results

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_db():
    db_cases.clear()
    db_workflow_results.clear()
    yield

def test_create_case():
    response = client.post("/cases/", json={
        "payer": "Aetna",
        "amount": 100.0,
        "denial_reason": "Missing auth",
        "procedure_code": "99285",
        "diagnosis_code": "J18.9",
        "member_plan": "PPO",
        "notes": "Test case"
    })
    
    assert response.status_code == 201
    data = response.json()
    assert "case_id" in data
    assert data["status"] == "created"
    assert data["case_id"] in db_cases

def test_trigger_workflow_not_found():
    response = client.post("/workflows/INVALID/run")
    assert response.status_code == 404

def test_trigger_workflow_success(mocker):
    # Mock the background task execution to prevent real API calls
    mock_run = mocker.patch("app.api.workflows.run_workflow_background")
    
    # Create a case first
    create_resp = client.post("/cases/", json={
        "payer": "Aetna",
        "amount": 100.0,
        "denial_reason": "Missing auth",
        "procedure_code": "99285",
        "diagnosis_code": "J18.9",
        "member_plan": "PPO",
        "notes": "Test case"
    })
    case_id = create_resp.json()["case_id"]
    
    # Trigger workflow
    response = client.post(f"/workflows/{case_id}/run")
    assert response.status_code == 202
    assert response.json()["message"] == "Workflow triggered successfully"
    assert db_cases[case_id]["status"] == "processing"
    
    # Check background task was queued
    mock_run.assert_called_once()
    
def test_get_workflow_summary():
    case_id = "TEST-123"
    db_workflow_results[case_id] = {
        "status": "completed",
        "evaluation": {"decision": "Approved"}
    }
    
    response = client.get(f"/workflows/{case_id}/summary")
    assert response.status_code == 200
    assert response.json()["status"] == "completed"
    assert response.json()["evaluation"]["decision"] == "Approved"
