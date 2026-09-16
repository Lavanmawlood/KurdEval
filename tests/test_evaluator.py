"""Tests for evaluator."""
from unittest.mock import Mock
from src.evaluators.evaluator import KurdishEvaluator
from src.models.groq_client import LLMResponse

class TestKurdishEvaluator:
    def test_evaluate_prompts(self, sample_prompts):
        mock_client = Mock()
        mock_client.generate.return_value = LLMResponse(
            model="test", prompt="test", response="test",
            tokens_used=10, time_seconds=1.0, success=True,
        )
        evaluator = KurdishEvaluator(mock_client)
        results = evaluator.evaluate_prompts(sample_prompts, ["model-1"])
        assert len(results) == 2
