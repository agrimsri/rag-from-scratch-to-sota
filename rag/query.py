"""
Query transformation: Multi-Query Expansion and Hypothetical Document Embeddings (HyDE).
Introduced in branch 06.
"""

from typing import List
from rag import config, llm


def expand_queries(query: str, n: int = 2) -> List[str]:
    """Generates alternative perspectives and search variations of the original query."""
    prompt = (
        f"Generate {n} short alternative search queries or technical synonyms for: '{query}'\n"
        f'Output ONLY a JSON array of strings, e.g. ["alt query 1", "alt query 2"]'
    )
    res = llm.generate_json(prompt)
    if isinstance(res, list):
        return [str(q).strip() for q in res if str(q).strip()][:n]
    if isinstance(res, dict):
        queries = res.get("queries", res.get("variations", []))
        if isinstance(queries, list):
            return [str(q).strip() for q in queries if str(q).strip()][:n]
    return []


def hyde_passage(query: str) -> str:
    """Generates a hypothetical documentation passage answering the query."""
    prompt = (
        f"Write a 1-sentence hypothetical technical documentation excerpt that directly answers:\n"
        f"Question: {query}\nExcerpt:"
    )
    passage = llm.generate(prompt)
    return passage.strip()
