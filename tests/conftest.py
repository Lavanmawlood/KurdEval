"""Pytest configuration."""
import pytest
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

@pytest.fixture
def sample_prompts():
    return [
        {"id": 1, "category": "creative", "prompt": "چیرۆکێکی کورت بە کوردی بۆم بنووسە."},
        {"id": 2, "category": "instruction", "prompt": "بە کوردی فێرم بکە چای ئامادە بکەم."},
    ]
