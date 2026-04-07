"""Semantic convention shortcuts for NexusAI-specific spans."""

from .nexusai import NexusAISpanAttributes
from .gen_ai import ChainAttributes, GenAIAttributes, LLMAttributes, RetrieverAttributes, ToolAttributes

__all__ = [
    "ChainAttributes",
    "NexusAISpanAttributes",
    "GenAIAttributes",
    "LLMAttributes",
    "RetrieverAttributes",
    "ToolAttributes",
]
