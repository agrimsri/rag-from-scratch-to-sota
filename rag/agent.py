"""
Agentic RAG using iterative tool-calling search loop.
Introduced in branch 10.
"""

from typing import Any, Dict, List
from rag import config, llm, retrieve
from rag.schema import Hit


def agent_search_loop(question: str, index: Dict[str, Any], max_steps: int = 3) -> Dict[str, Any]:
    """
    Iterative agentic retrieval loop:
    1. First search on question.
    2. Inspects retrieved hits.
    3. If multi-hop or insufficient information, issues follow-up search queries.
    4. Returns deduplicated hits and execution trace.
    """
    all_hits: Dict[str, Hit] = {}
    search_history: List[str] = []
    current_query = question

    for step in range(1, max_steps + 1):
        search_history.append(f"step_{step}:search(\"{current_query}\")")
        new_hits = retrieve.retrieve(current_query, index, k=config.TOP_K)
        for h in new_hits:
            if h.chunk.id not in all_hits:
                all_hits[h.chunk.id] = h

        if step == max_steps:
            break

        # Format concise snippets for agent decision
        snippets = []
        for h in list(all_hits.values())[:6]:
            snippets.append(f"[{h.chunk.id}]: {h.chunk.text[:220]}")
        snippets_str = "\n".join(snippets)

        prompt = (
            f"Question: \"{question}\"\n\n"
            f"Retrieved passages:\n{snippets_str}\n\n"
            f"Can the question be completely answered using ONLY the retrieved passages?\n"
            f"If YES, output: {{\"done\": true, \"next_query\": \"\"}}\n"
            f"If NO, output: {{\"done\": false, \"next_query\": \"<short focused query for missing detail>\"}}\n"
            f"Output ONLY JSON:"
        )

        try:
            decision = llm.generate_json(prompt)
            if isinstance(decision, dict):
                if decision.get("done", False) or not decision.get("next_query"):
                    break
                next_q = str(decision.get("next_query", "")).strip()
                if not next_q or next_q == current_query:
                    break
                current_query = next_q
            else:
                break
        except Exception:
            break

    return {
        "hits": list(all_hits.values()),
        "trace": search_history,
    }
