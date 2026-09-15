"""Data loading utilities."""

import json
from pathlib import Path
from typing import List, Dict, Any

PROJECT = Path(__file__).parent.parent.parent


def load_prompts() -> List[Dict[str, Any]]:
    """Load Kurdish prompts."""
    path = PROJECT / "data" / "prompts" / "kurdish_prompts.json"
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def load_responses() -> List[Dict[str, Any]]:
    """Load LLM responses."""
    path = PROJECT / "data" / "responses" / "responses.json"
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def load_annotations() -> Dict[str, Any]:
    """Load human annotations."""
    path = PROJECT / "data" / "annotations" / "annotations.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))
