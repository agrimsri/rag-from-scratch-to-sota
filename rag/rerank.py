"""
Two-stage retrieval reranker using listwise LLM scoring.
Retrieves wide (candidate pool ~15-20), reranks narrow to top_n.
Introduced in branch 07.
"""

from typing import Any, Dict, List
from rag import config, llm
from rag.schema import Hit


def rerank(query: str, hits: List[Hit], top_n: int = 5) -> List[Hit]:
    """
    Reranks candidate hits using a listwise LLM prompt.
    Falls back gracefully to original order on any parsing error.
    """
    if not hits or not config.USE_RERANK:
        return hits[:top_n]

    candidates = hits[: min(len(hits), 15)]

    # Format numbered passages (truncated to 350 chars for prompt efficiency)
    passages = []
    for idx, hit in enumerate(candidates):
        snippet = hit.chunk.text[:350].replace("\n", " ").strip()
        passages.append(f"[{idx}] {snippet}")

    passages_str = "\n".join(passages)
    prompt = (
        f"You are a search reranker. Score the relevance of each passage (0 to 10) to the query.\n"
        f"Query: \"{query}\"\n\n"
        f"Passages:\n{passages_str}\n\n"
        f"Output ONLY a JSON array of objects with 'id' (integer 0..N) and 'score' (number 0..10):\n"
        f'[{{"id": 0, "score": 8.5}}, ...]'
    )

    try:
        ranked_data = llm.generate_json(prompt)
        items = []
        if isinstance(ranked_data, list):
            items = ranked_data
        elif isinstance(ranked_data, dict):
            for k in ["ranking", "rankings", "passages", "scores", "results"]:
                if isinstance(ranked_data.get(k), list):
                    items = ranked_data[k]
                    break

        if items:
            score_map = {}
            for item in items:
                if isinstance(item, dict) and "id" in item:
                    try:
                        score_map[int(item["id"])] = float(item.get("score", 0.0))
                    except (ValueError, TypeError):
                        pass

            if score_map:
                reranked = sorted(
                    candidates,
                    key=lambda h, sm=score_map: sm.get(candidates.index(h), 0.0),
                    reverse=True,
                )
                # Assign reranked scores (normalized)
                for h in reranked:
                    idx = candidates.index(h)
                    if idx in score_map:
                        h.score = max(score_map[idx] / 10.0, 0.01)
                return reranked[:top_n]
    except Exception:
        pass

    return candidates[:top_n]
