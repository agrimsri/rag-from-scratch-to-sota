"""
Answer generation from retrieved hits.
In branch 01, we use a simple 'embed it, search it, stuff it' prompt.
"""

from typing import Any, Dict, List
from rag import llm
from rag.schema import Hit


def generate_answer(
    question: str, hits: List[Hit], no_rag: bool = False
) -> Dict[str, Any]:
    """Generates an answer using retrieved chunks or purely from model weights if no_rag=True."""
    if no_rag or not hits:
        prompt = (
            f"Answer the following question about the Quillstack developer platform directly:\n\n"
            f"Question: {question}\nAnswer:"
        )
        answer = llm.generate(prompt)
        return {
            "answer": answer.strip(),
            "answerable": None,
            "citations": [],
        }

    # Format the retrieved documents into the prompt (capped to fit LLM context window)
    context_parts = []
    total_chars = 0
    max_context_budget = 8000

    for hit in hits:
        chunk_text = hit.chunk.text
        if total_chars + len(chunk_text) > max_context_budget:
            chunk_text = chunk_text[: max(0, max_context_budget - total_chars)]
        if chunk_text:
            context_parts.append(f"=== Document: {hit.chunk.id} ===\n{chunk_text}")
            total_chars += len(chunk_text)
        if total_chars >= max_context_budget:
            break
    context_str = "\n\n".join(context_parts)

    prompt = (
        f"Answer the question based on the following documents:\n\n"
        f"{context_str}\n\n"
        f"Question: {question}\n"
        f"Answer:"
    )

    answer = llm.generate(prompt)
    citations = [h.chunk.id for h in hits]

    return {
        "answer": answer.strip(),
        "answerable": True,
        "citations": citations,
    }
