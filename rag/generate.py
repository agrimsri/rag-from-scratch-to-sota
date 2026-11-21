"""
Answer generation from retrieved hits.
In branch 02, chunks are small (~1000 chars) so top-k chunks fit comfortably in context.
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

    # Format the retrieved chunks into the prompt (capped to keep prompt well within 2048 tokens)
    context_parts = []
    total_len = 0
    for hit in hits:
        part = f"=== Chunk: {hit.chunk.id} ===\n{hit.chunk.text}"
        if total_len + len(part) > 6000 and context_parts:
            break
        context_parts.append(part)
        total_len += len(part)
    context_str = "\n\n".join(context_parts)

    prompt = (
        f"Answer the question based on the following passages:\n\n"
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
