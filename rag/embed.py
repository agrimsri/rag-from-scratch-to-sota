"""
Ollama embedding wrapper with batching, L2 normalization, and SQLite caching.
"""

import json
from typing import List, Literal
import numpy as np
import ollama

from rag import cache, config


def _normalize(vectors: np.ndarray) -> np.ndarray:
    """L2-normalizes vectors so cosine similarity is simply the dot product."""
    norms = np.linalg.norm(vectors, axis=-1, keepdims=True)
    norms[norms == 0] = 1e-12
    return vectors / norms


def embed(
    texts: List[str], kind: Literal["doc", "query"] = "doc", batch_size: int = 16
) -> np.ndarray:
    """
    Computes normalized embeddings for a list of texts using Ollama.
    Applies the model-specific prefix and reads/writes to SQLite cache.
    """
    prefix = (
        config.EMBED_DOC_PREFIX if kind == "doc" else config.EMBED_QUERY_PREFIX
    )
    client = ollama.Client(host=config.OLLAMA_HOST)

    results: List[np.ndarray] = [None] * len(texts)  # type: ignore
    missing_indices: List[int] = []
    missing_prefixed: List[str] = []

    for idx, text in enumerate(texts):
        prefixed_text = prefix + text
        cache_key = cache.hash_key(
            {
                "model": config.OLLAMA_EMBED_MODEL,
                "text": prefixed_text,
                "ctx": config.EMBED_NUM_CTX,
            }
        )
        cached_val = cache.get("embed", cache_key)
        if cached_val is not None:
            results[idx] = np.array(json.loads(cached_val), dtype=np.float32)
        else:
            missing_indices.append(idx)
            missing_prefixed.append(prefixed_text)

    # Batch embed missing texts
    if missing_indices:
        for i in range(0, len(missing_indices), batch_size):
            batch_slice = missing_indices[i : i + batch_size]
            batch_inputs = missing_prefixed[i : i + batch_size]

            response = client.embed(
                model=config.OLLAMA_EMBED_MODEL,
                input=batch_inputs,
                options={"num_ctx": config.EMBED_NUM_CTX},
            )
            raw_embeddings = response["embeddings"]

            for orig_idx, raw_emb, p_text in zip(
                batch_slice, raw_embeddings, batch_inputs
            ):
                emb_arr = np.array(raw_emb, dtype=np.float32)
                results[orig_idx] = emb_arr
                cache_key = cache.hash_key(
                    {
                        "model": config.OLLAMA_EMBED_MODEL,
                        "text": p_text,
                        "ctx": config.EMBED_NUM_CTX,
                    }
                )
                cache.set("embed", cache_key, json.dumps(raw_emb))

    stacked = np.stack(results, axis=0)
    return _normalize(stacked)
