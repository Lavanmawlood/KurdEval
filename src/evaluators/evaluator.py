"""Evaluation logic for Kurdish LLM comparison."""

from typing import List, Dict, Any
from pathlib import Path
import json

from src.models.groq_client import GroqClient, LLMResponse


class KurdishEvaluator:
    """Evaluate multiple LLMs on Kurdish prompts."""

    def __init__(self, client: GroqClient):
        self.client = client

    def evaluate_prompts(
        self,
        prompts: List[Dict[str, Any]],
        models: List[str],
    ) -> List[LLMResponse]:
        """Evaluate multiple prompts across multiple models."""
        all_responses = []

        for prompt_data in prompts:
            prompt = prompt_data["prompt"]
            print(f"\n📝 Prompt {prompt_data['id']}: {prompt[:50]}...")

            for model in models:
                print(f"   🤖 {model}...", end=" ")
                response = self.client.generate(model=model, prompt=prompt)
                
                if response.success:
                    print(f"✅ {response.tokens_used} tokens, {response.time_seconds}s")
                else:
                    print(f"❌ {response.error}")
                
                # Add metadata
                response_dict = response.to_dict()
                response_dict["prompt_id"] = prompt_data["id"]
                response_dict["category"] = prompt_data.get("category", "unknown")
                all_responses.append(response_dict)

        return all_responses

    @staticmethod
    def save_results(responses: List[Dict], output_path: Path) -> None:
        """Save responses to JSON file."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(responses, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        print(f"\n💾 Saved {len(responses)} responses to {output_path}")
