"""
Contextual retrieval situating chunks within their parent document at index time.
Based on Anthropic (2024) contextual retrieval methodology.
Introduced in branch 08.
"""

from typing import Dict, List
from rag import cache, config, llm
from rag.schema import Chunk


def contextualize_chunks(doc_name: str, full_doc: str, chunks: List[Chunk]) -> List[Chunk]:
    """
    Prompts the LLM to write 1 sentence situating each chunk within the document.
    Prepends this context to embed_text for enhanced dense & BM25 indexing.
    Results are cached in SQLite kv_cache so indexing is resume-safe and costs zero on re-runs.
    """
    if not config.USE_CONTEXTUAL:
        return chunks

    missing_chunks = []
    cached_contexts = {}
    for c in chunks:
        ck = cache.hash_key({"doc": doc_name, "chunk_id": c.id, "text": c.text, "type": "context"})
        val = cache.get("contextual", ck)
        if val:
            cached_contexts[c.id] = val
        else:
            missing_chunks.append(c)

    batch_size = 8
    for i in range(0, len(missing_chunks), batch_size):
        batch = missing_chunks[i : i + batch_size]
        items_payload = [f'<chunk id="{c.id}">\n{c.text[:400]}\n</chunk>' for c in batch]
        prompt = (
            f"You are situating documentation chunks for search retrieval.\n"
            f"Document: {doc_name}\n"
            f"Overview: {full_doc[:1200]}\n\n"
            f"Here are {len(batch)} chunks:\n"
            f"{chr(10).join(items_payload)}\n\n"
            f"For each chunk, write a 1-sentence context situating what it discusses.\n"
            f"Output ONLY JSON array of objects with 'id' and 'context':\n"
            f'[{{"id": "...", "context": "..."}}]'
        )
        try:
            res = llm.generate_json(prompt)
            items = res if isinstance(res, list) else []
            if isinstance(res, dict):
                for k in ["contexts", "chunks", "items"]:
                    if isinstance(res.get(k), list):
                        items = res[k]
                        break
            for it in items:
                if isinstance(it, dict) and "id" in it and "context" in it:
                    cid = it["id"]
                    ctx_str = str(it["context"]).strip()
                    cached_contexts[cid] = ctx_str
                    ck = cache.hash_key({"doc": doc_name, "chunk_id": cid, "text": c.text, "type": "context"})
                    cache.set("contextual", ck, ctx_str)
        except Exception:
            pass

    updated = []
    for c in chunks:
        ctx = cached_contexts.get(c.id, "")
        new_embed_text = f"[{doc_name} | {ctx}]\n{c.text}" if ctx else c.embed_text
        updated.append(
            Chunk(
                id=c.id,
                doc=c.doc,
                text=c.text,
                embed_text=new_embed_text,
                meta={**c.meta, "contextual_prefix": ctx},
            )
        )
    return updated
