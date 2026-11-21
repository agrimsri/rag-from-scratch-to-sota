# Lesson 09: Small-to-Big Retrieval — "Search Small, Answer Big"

## Goal
Resolve the fundamental conflict in RAG: small chunks are optimal for dense embedding retrieval accuracy, while large surrounding contexts are necessary for complete LLM answer synthesis.

## The Failure
When chunks are kept very small (e.g. 500–800 characters), embedding vectors are sharp and specific. However, answers frequently span across paragraphs. In `multi-chunk` questions (e.g. comparing two configuration parameters described in adjacent paragraphs of `migration-v2-to-v3.md`), the retriever fetches only the child paragraph matching the query terms. The model generates a partial answer because the comparison sentence in the adjacent sibling chunk is missing.

**Before (small chunks only):**
- Query: *"How does the partition leader election in QuillStream compare to legacy QuillQueue?"*
- Retrieved: Only the paragraph describing QuillStream.
- Answer: Partial answer omitting the legacy comparison.

**After (Small-to-Big Expansion):**
- Retrieval runs on the small, high-precision child chunk.
- At generation time, `expand_hits()` dynamically merges neighboring sibling chunks from the same section into `chunk.text`.
- The generation model receives the complete section context and synthesizes a comprehensive answer.

## The Idea
1. **Search Small:** Retain granular chunks in the vector and BM25 index. This prevents dilution of embedding representations.
2. **Expand Big:** Upon retrieval, expand each top-k hit by fetching adjacent siblings sharing the same document section.
3. **Purity of Contract:** Chunk IDs and citation verification remain anchored to the retrieved child chunk, preserving clean attribution.

```
Query: "compare partition election"
         |
         v
Retrieved Hit: Chunk #14 (child paragraph, 450 chars)
         |
         v (expand_hits)
Expanded Context: [Chunk #13 (previous) + Chunk #14 + Chunk #15 (next)]
         |
         v
LLM Generation: Full comparative answer synthesized accurately
```

## What Changed
- `rag/expand.py`: Implemented `expand_hits()` sibling aggregator.
- `rag/pipeline.py`: Passes expanded hits to generation while tracking child IDs.
- `rag/config.py`: Added toggle `USE_SMALL_TO_BIG = True`.

View the diff:
```bash
git diff 08-contextual-retrieval..09-small-to-big --stat
```

## Run It
```bash
python cli.py ask "How does the partition leader election in QuillStream compare to legacy QuillQueue?" --show-context
python cli.py eval
python eval/compare.py
```

## Results
- `multi-chunk` accuracy increases significantly.
- No penalty to retrieval precision (Recall@5 remains at 100%).
