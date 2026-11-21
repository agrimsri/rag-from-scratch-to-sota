# Lesson 08: Contextual Retrieval — "Give Every Chunk Its Context Back"

## Goal
Eliminate chunk ambiguity at index time by having an LLM generate a short 1–2 sentence contextual explanation prepended to each chunk's search representation.

## The Failure
When documents are sliced into granular pieces, individual chunks lose their overarching reference points.
Consider this chunk from `plans-and-pricing.md`:
> *"The limit is 500 requests per minute."*

When embedded on its own, neither dense retrieval nor BM25 knows whether this applies to the Hobby plan, Team plan, or public unauthenticated endpoints. Retrieval returns this chunk indiscriminately for all rate limit queries.

**Before (without contextual retrieval):**
- Query: *"What is the rate limit for the Team Developer Add-on?"*
- Retrieved chunk is ambiguous; model hallucinates or assigns it to the wrong plan.

**After (with contextual retrieval):**
- Index-time prompt prepends:
  *"This chunk describes burst quotas under the Team Developer Add-on for Quillstack Team workspaces."*
- `embed_text` now contains both semantic keywords and plan associations.
- Precision jumps across both dense and BM25 search.

## The Idea
Introduced by Anthropic in 2024:
1. **At index time:** Pass the document and batches of chunks to a fast model.
2. **Generate context:** The model generates 1–2 sentences situating each chunk.
3. **Dual Representation:**
   - `embed_text`: `context + "\n" + chunk.text` (searched by dense vectors and BM25).
   - `chunk.text`: Unmodified verbatim text (read by LLM at query time and checked by evals).

```
Full Document + Chunk
       |
       v (Index Time LLM)
"This section details burst limits for Team Developer Add-ons..."
       |
       +---> Prepend to embed_text (Dense & BM25)
       +---> Keep chunk.text pristine for generation
```

## What Changed
- `rag/contextualize.py`: Created batch contextualizer.
- `rag/loader.py`: Invokes contextualizer when loading documents for indexing.
- `rag/config.py`: Added toggle `USE_CONTEXTUAL = True`.

View the diff:
```bash
git diff 07-reranking..08-contextual-retrieval --stat
```

## Run It
```bash
python cli.py index
python cli.py ask "What tier and feature has the limit of 500 requests per minute?" --show-context
python cli.py eval
python eval/compare.py
```

## Results
- `context-dependent` accuracy improves significantly.
- Trade-off: One-time index generation cost (cached in SQLite).
