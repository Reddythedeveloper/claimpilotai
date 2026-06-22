import pytest
from unittest.mock import patch, MagicMock
from pydantic import BaseModel, Field
from app.services.groq_service import GroqService

class SampleOutputSchema(BaseModel):
    is_valid: bool = Field(description="Whether the claim is valid")
    reason: str = Field(description="Reason for the decision")

@pytest.fixture
def mock_env(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "test_mock_key")
    monkeypatch.setenv("GROQ_MODEL_PRIMARY", "llama3-70b-8192")

@patch("app.services.groq_service.ChatGroq")
def test_invoke_structured_success(mock_chat_groq_cls, mock_env):
    # Setup mock
    mock_llm_instance = MagicMock()
    mock_structured_llm = MagicMock()
    
    mock_chat_groq_cls.return_value = mock_llm_instance
    mock_llm_instance.with_structured_output.return_value = mock_structured_llm
    
    # Mock output
    expected_output = SampleOutputSchema(is_valid=True, reason="Valid case")
    mock_structured_llm.invoke.return_value = expected_output

    # Test
    service = GroqService()
    result = service.invoke_structured(
        prompt="Is this valid?",
        schema=SampleOutputSchema,
        system_prompt="You are an AI."
    )
    
    assert isinstance(result, SampleOutputSchema)
    assert result.is_valid is True
    assert result.reason == "Valid case"
    
    # Verify calls
    mock_llm_instance.with_structured_output.assert_called_once_with(SampleOutputSchema)
    mock_structured_llm.invoke.assert_called_once()
    args = mock_structured_llm.invoke.call_args[0][0]
    assert len(args) == 2
    assert args[0].content == "You are an AI."
    assert args[1].content == "Is this valid?"

@patch("app.services.groq_service.ChatGroq")
def test_invoke_text_success(mock_chat_groq_cls, mock_env):
    mock_llm_instance = MagicMock()
    mock_chat_groq_cls.return_value = mock_llm_instance
    
    mock_response = MagicMock()
    mock_response.content = "Plain text response"
    mock_llm_instance.invoke.return_value = mock_response
    
    service = GroqService()
    result = service.invoke_text("Hello")
    
    assert result == "Plain text response"
    mock_llm_instance.invoke.assert_called_once()
