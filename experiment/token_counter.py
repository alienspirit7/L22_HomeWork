from __future__ import annotations

"""
Token counting utilities for MCP experiment.
Uses tiktoken (OpenAI's tokenizer) as a proxy for token counting.
"""

from dataclasses import dataclass, field
from typing import Optional
import tiktoken


# Use cl100k_base encoding (GPT-4/Claude compatible)
_encoder = tiktoken.get_encoding("cl100k_base")


def count_tokens(text: str) -> int:
    """Count tokens in a text string."""
    if not text:
        return 0
    return len(_encoder.encode(text))


@dataclass
class TokenMetrics:
    """Token metrics for a single operation or message."""
    context_tokens: int = 0  # System prompt + tool definitions
    reasoning_tokens: int = 0  # LLM reasoning/thinking
    tool_call_tokens: int = 0  # Tool invocation JSON
    response_tokens: int = 0  # Tool response content
    
    @property
    def total(self) -> int:
        return (self.context_tokens + self.reasoning_tokens + 
                self.tool_call_tokens + self.response_tokens)
    
    def to_dict(self) -> dict:
        return {
            "context_tokens": self.context_tokens,
            "reasoning_tokens": self.reasoning_tokens,
            "tool_call_tokens": self.tool_call_tokens,
            "response_tokens": self.response_tokens,
            "total_tokens": self.total
        }


@dataclass
class TokenAccumulator:
    """Accumulates token metrics across multiple operations."""
    
    paradigm_name: str
    operations: list[TokenMetrics] = field(default_factory=list)
    initial_context_tokens: int = 0
    
    def add_operation(self, metrics: TokenMetrics) -> None:
        """Add metrics from a single operation."""
        self.operations.append(metrics)
    
    @property
    def total_context_tokens(self) -> int:
        """Total context tokens (initial + per-operation)."""
        return self.initial_context_tokens + sum(m.context_tokens for m in self.operations)
    
    @property
    def total_reasoning_tokens(self) -> int:
        return sum(m.reasoning_tokens for m in self.operations)
    
    @property
    def total_tool_call_tokens(self) -> int:
        return sum(m.tool_call_tokens for m in self.operations)
    
    @property
    def total_response_tokens(self) -> int:
        return sum(m.response_tokens for m in self.operations)
    
    @property
    def grand_total(self) -> int:
        return (self.total_context_tokens + self.total_reasoning_tokens +
                self.total_tool_call_tokens + self.total_response_tokens)
    
    @property
    def operation_count(self) -> int:
        return len(self.operations)
    
    @property
    def tokens_per_operation(self) -> float:
        if not self.operations:
            return 0.0
        return self.grand_total / len(self.operations)
    
    def summary(self) -> dict:
        """Return summary of all token metrics."""
        return {
            "paradigm": self.paradigm_name,
            "operation_count": self.operation_count,
            "initial_context_tokens": self.initial_context_tokens,
            "total_context_tokens": self.total_context_tokens,
            "total_reasoning_tokens": self.total_reasoning_tokens,
            "total_tool_call_tokens": self.total_tool_call_tokens,
            "total_response_tokens": self.total_response_tokens,
            "grand_total": self.grand_total,
            "tokens_per_operation": round(self.tokens_per_operation, 2)
        }
