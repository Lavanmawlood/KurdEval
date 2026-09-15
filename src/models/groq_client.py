"""Groq API connector for LLM evaluation."""

from groq import Groq
from typing import Optional, Dict, Any
import os
import time
from dataclasses import dataclass, asdict


@dataclass
class LLMResponse:
    """Structured LLM response."""
    model: str
    prompt: str
    response: str
    tokens_used: int
    time_seconds: float
    success: bool
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class GroqClient:
    """Client for Groq API with error handling."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not set")
        self.client = Groq(api_key=self.api_key)

    def generate(
        self,
        model: str,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 500,
    ) -> LLMResponse:
        """Generate response from a model."""
        start_time = time.time()
        
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            
            elapsed = time.time() - start_time
            
            return LLMResponse(
                model=model,
                prompt=prompt,
                response=response.choices[0].message.content,
                tokens_used=response.usage.total_tokens,
                time_seconds=round(elapsed, 2),
                success=True,
            )
            
        except Exception as e:
            return LLMResponse(
                model=model,
                prompt=prompt,
                response="",
                tokens_used=0,
                time_seconds=round(time.time() - start_time, 2),
                success=False,
                error=str(e),
            )
