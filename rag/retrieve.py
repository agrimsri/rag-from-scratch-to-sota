"""
Hybrid retrieval module combining Dense embeddings and BM25 via Reciprocal Rank Fusion (RRF).
Introduced in branch 05.
"""

from typing import Any, Dict, List
import numpy as np

from rag import config, embed
from rag.bm25 import BM25Index
from rag.schema import Hit

_BM25_INDEX = None
_INDEXED_CHUNKS_SIG = None


def get_or_build_bm25(chunks) -> BM25Index:
    global _BM25_INDEX, _INDEXED_CHUNKS_SIG
    sig = len(chunks)
    if _BM25_INDEX is None or _INDEXED_CHUNKS_SIG != sig:
        corpus = [c.embed_text for c in chunks]
        _BM25_INDEX = BM25Index(corpus)
        _INDEXED_CHUNKS_SIG = sig
    return _BM25_INDEX


def rrf_fuse(dense_hits: List[Hit], bm25_hits: List[Hit], k: int = 60, top_n: int = 5) -> List[Hit]:
    """
    Reciprocal Rank Fusion (RRF):
    RRF_score(d) = sum_{rankings r} 1.0 / (k + rank(r, d))
    """
    scores: Dict[str, float] = {}
    chunk_map = {}

    for rank, hit in enumerate(dense_hits, 1):
        cid = hit.chunk.id
        chunk_map[cid] = hit.chunk
        scores[cid] = scores.get(cid, 0.0) + (1.0 / (k + rank))

    for rank, hit in enumerate(bm25_hits, 1):
        cid = hit.chunk.id
        chunk_map[cid] = hit.chunk
        scores[cid] = scores.get(cid, 0.0) + (1.0 / (k + rank))

    ranked_items = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
    return [Hit(chunk=chunk_map[cid], score=score) for cid, score in ranked_items]


def retrieve(query: str, index: Dict[str, Any], k: int = 5) -> List[Hit]:
    """
    If config.USE_HYBRID is True, performs dense + BM25 hybrid search fused via RRF.
    Otherwise performs standard dense retrieval.
    """
    chunks = index["chunks"]
    vectors: np.ndarray = index["vectors"]

    # Dense retrieval
    q_vec = embed.embed([query], kind="query")[0]
    dense_scores = vectors @ q_vec
    candidate_k = max(k, 20)
    dense_indices = np.argsort(dense_scores)[::-1][:candidate_k]
    dense_hits = [Hit(chunk=chunks[i], score=float(dense_scores[i])) for i in dense_indices]

    if not config.USE_HYBRID:
        return dense_hits[:k]

    # BM25 retrieval
    bm25 = get_or_build_bm25(chunks)
    bm25_ranked = bm25.score(query)[:candidate_k]
    bm25_hits = [Hit(chunk=chunks[idx], score=sc) for idx, sc in bm25_ranked]

    # Reciprocal Rank Fusion
    fused_hits = rrf_fuse(dense_hits, bm25_hits, k=60, top_n=k)
    return fused_hits
