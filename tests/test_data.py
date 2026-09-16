"""Tests for data files."""
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

class TestPromptsData:
    def test_prompts_file_exists(self):
        assert (PROJECT_ROOT / "data/prompts/kurdish_prompts.json").exists()

    def test_prompts_have_required_fields(self):
        prompts = json.loads((PROJECT_ROOT / "data/prompts/kurdish_prompts.json").read_text(encoding="utf-8"))
        assert len(prompts) > 0
        for p in prompts:
            assert "id" in p and "prompt" in p and "category" in p

    def test_prompts_unique_ids(self):
        prompts = json.loads((PROJECT_ROOT / "data/prompts/kurdish_prompts.json").read_text(encoding="utf-8"))
        ids = [p["id"] for p in prompts]
        assert len(ids) == len(set(ids))
