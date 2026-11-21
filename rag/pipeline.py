"""
End-to-end RAG query pipeline satisfying the standard ask() contract.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional

from rag import config, generate, index, llm, retrieve
from rag.schema import Hit

_GLOBAL_INDEX = None


def get_or_load_index(docs_dir: Optional[Path] = None) -> Dict[str, Any]:
    global _GLOBAL_INDEX
    if _GLOBAL_INDEX is None:
        if docs_dir is None:
            docs_dir = Path(__file__).resolve().parent.parent / "data" / "docs"
        _GLOBAL_INDEX = index.load_index(docs_dir)
    return _GLOBAL_INDEX


def ask(
    question: str,
    k: Optional[int] = None,
    no_rag: bool = False,
    retrieval_only: bool = False,
    docs_dir: Optional[Path] = None,
) -> Dict[str, Any]:
    """
    Executes the RAG pipeline for a given user question.
    Returns:
        {
            "answer": str,
            "answerable": bool | None,
            "citations": list[str],
            "hits": list[Hit],
            "trace": list[str],
            "llm_calls": int
        }
    """
    top_k = k if k is not None else config.TOP_K
    trace: List[str] = []
    calls_start = llm.get_call_count()

    if no_rag:
        trace.append("no_rag_baseline")
        if retrieval_only:
            gen_result = {"answer": "", "citations": [], "answerable": None}
        else:
            gen_result = generate.generate_answer(question, hits=[], no_rag=True)
        hits: List[Hit] = []
    else:
        idx = get_or_load_index(docs_dir)
        if config.USE_AGENT:
            from rag import agent
            agent_res = agent.agent_search_loop(question, idx, max_steps=3)
            hits = agent_res["hits"]
            trace.extend(agent_res["trace"])
        else:
            trace.append(f"dense_retrieve(k={top_k})")
            hits = retrieve.retrieve(question, idx, k=top_k)

        if config.USE_SMALL_TO_BIG:
            from rag import expand
            chunk_map = {c.id: c for c in idx["chunks"]}
            gen_hits = expand.expand_hits(hits, chunk_map)
        else:
            gen_hits = hits

        if retrieval_only:
            gen_result = {
                "answer": "",
                "citations": [h.chunk.id for h in hits],
                "answerable": True,
            }
        else:
            gen_result = generate.generate_answer(question, hits=gen_hits, no_rag=False)

    calls_used = llm.get_call_count() - calls_start

    return {
        "answer": gen_result["answer"],
        "answerable": gen_result.get("answerable"),
        "citations": gen_result.get("citations", []),
        "hits": hits,
        "trace": trace,
        "llm_calls": calls_used,
    }
