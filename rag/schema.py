"""
Core data contracts for RAG pipelines.
Introduced in branch 01 and never broken.
"""

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class Chunk:
    id: str  # Unique chunk identifier, e.g. "overview.md" or "pricing.md#3"
    doc: str  # Source document filename
    text: str  # Verbatim text that the LLM reads and evaluation checks against
    embed_text: str  # Text passed to embedding and BM25 indexer (== text in 01-07)
    meta: Dict[str, Any] = field(default_factory=dict)  # Metadata e.g. headings, offsets


@dataclass
class Hit:
    chunk: Chunk
    score: float
