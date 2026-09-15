"""Tests for model connectors."""

import pytest
from unittest.mock import Mock, patch
from src.models.groq_client import GroqClient, LLMResponse


def test_llm_response_to_dict():
    """Test LLMResponse serialization."""
    response = LLMResponse(
        model="test-model",
        prompt="test prompt",
        response="test response",
        tokens_used=100,
        time_seconds=1.5,
        success=True,
    )
    
    result = response.to_dict()
    
    assert result["model"] == "test-model"
    assert result["tokens_used"] == 100
    assert result["success"] is True


def test_groq_client_no_api_key():
    """Test that missing API key raises error."""
    with pytest.raises(ValueError, match="GROQ_API_KEY not set"):
        GroqClient(api_key=None)
