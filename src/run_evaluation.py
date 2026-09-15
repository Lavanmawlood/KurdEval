"""Main runner for Kurdish LLM evaluation."""

import json
from pathlib import Path

from src.models.groq_client import GroqClient
from src.evaluators.evaluator import KurdishEvaluator


# Configuration
MODELS = [
    "openai/gpt-oss-120b",
    "openai/gpt-oss-20b",
]

PROJECT = Path(__file__).parent.parent
PROMPTS_FILE = PROJECT / "data" / "prompts" / "kurdish_prompts.json"
OUTPUT_FILE = PROJECT / "data" / "responses" / "responses.json"


def main():
    print("=" * 60)
    print("🎯 Kurdish LLM Evaluator")
    print("=" * 60)
    
    # Load prompts
    prompts = json.loads(PROMPTS_FILE.read_text(encoding="utf-8"))
    print(f"📋 Loaded {len(prompts)} prompts")
    print(f"🤖 Models: {len(MODELS)}")
    print(f"📊 Total requests: {len(prompts) * len(MODELS)}")
    
    # Initialize
    client = GroqClient()
    evaluator = KurdishEvaluator(client)
    
    # Evaluate
    print("\n" + "=" * 60)
    print("🚀 Starting evaluation...")
    print("=" * 60)
    
    responses = evaluator.evaluate_prompts(prompts, MODELS)
    
    # Save
    evaluator.save_results(responses, OUTPUT_FILE)
    
    # Summary
    successful = [r for r in responses if r["success"]]
    print(f"\n✅ Success: {len(successful)}/{len(responses)}")
    print(f"📊 Total tokens: {sum(r['tokens_used'] for r in responses):,}")
    print(f"⏱️ Total time: {sum(r['time_seconds'] for r in responses):.1f}s")


if __name__ == "__main__":
    main()
