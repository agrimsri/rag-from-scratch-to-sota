"""
Small-to-big context expansion.
Retrieves narrow, specific chunks for high-precision search, then expands
retrieved chunks to include surrounding context (parent section / adjacent chunks)
for generation.
Introduced in branch 09.
"""

from typing import Dict, List
from rag import config
from rag.schema import Chunk, Hit


def expand_hits(hits: List[Hit], all_chunks_by_id: Dict[str, Chunk]) -> List[Hit]:
    """Expands each hit to include surrounding window or parent context."""
    if not config.USE_SMALL_TO_BIG or not hits:
        return hits

    expanded_hits = []

    for hit in hits:
        cid = hit.chunk.id
        doc_name = hit.chunk.doc
        meta = hit.chunk.meta or {}
        pos = meta.get("pos", 0)

        # Fetch adjacent siblings (pos - 1, pos, pos + 1) if in same document and section
        expanded_parts = []
        prev_id = f"{doc_name}#{pos - 1}"
        next_id = f"{doc_name}#{pos + 1}"

        if prev_id in all_chunks_by_id:
            prev_chunk = all_chunks_by_id[prev_id]
            if (prev_chunk.meta or {}).get("heading_path") == meta.get("heading_path"):
                expanded_parts.append(prev_chunk.text)

        expanded_parts.append(hit.chunk.text)

        if next_id in all_chunks_by_id:
            next_chunk = all_chunks_by_id[next_id]
            if (next_chunk.meta or {}).get("heading_path") == meta.get("heading_path"):
                expanded_parts.append(next_chunk.text)

        full_text = "\n\n".join(expanded_parts)
        new_chunk = Chunk(
            id=hit.chunk.id,
            doc=hit.chunk.doc,
            text=full_text,
            embed_text=hit.chunk.embed_text,
            meta={**meta, "expanded": True},
        )
        expanded_hits.append(Hit(chunk=new_chunk, score=hit.score))

    return expanded_hits
