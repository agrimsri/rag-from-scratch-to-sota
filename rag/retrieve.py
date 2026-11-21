"""
Vector retrieval module using NumPy dot product cosine similarity.
"""

from typing import Any, Dict, List
import numpy as np

from rag import embed
from rag.schema import Hit


def retrieve(query: str, index: Dict[str, Any], k: int = 5) -> List[Hit]:
    """
    Embeds the user query and computes cosine similarity against indexed chunks.
    Returns the top-k highest scoring Hits.
    """
    q_vec = embed.embed([query], kind="query")[0]  # shape: (dim,)
    vectors: np.ndarray = index["vectors"]          # shape: (num_chunks, dim)
    chunks = index["chunks"]

    scores = vectors @ q_vec                       # shape: (num_chunks,)
    top_indices = np.argsort(scores)[::-1][:k]

    hits = [
        Hit(chunk=chunks[i], score=float(scores[i]))
        for i in top_indices
    ]
    return hits
