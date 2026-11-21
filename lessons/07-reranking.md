# Lesson 07: Reranking — "Retrieve Wide, Read Narrow"

## Goal
Improve precision and push relevant passages from positions 6–20 into the top 5 by introducing a second-stage cross-encoder listwise reranker.

## The Failure
Bi-encoder embedding search is fast because query and document are embedded independently:
$\text{score} = \mathbf{q} \cdot \mathbf{d}$.
However, because the document vector is computed without knowledge of the query, nuanced relevance cues are missed. In `noisy-top-k` questions, the golden evidence chunk is often retrieved at rank 8, 12, or 18, falling outside the LLM's top-5 context window.

**Before (retrieval without reranking):**
- Candidate at Rank 12: Falls outside top $k=5$ context.
- Result: Retrieval Miss at $k=5$, incorrect answer.

**After (two-stage rerank):**
- Stage 1: Retrieve wide candidate pool ($N=15$).
- Stage 2: Listwise LLM cross-examination compares all candidate snippets directly against the query.
- The Golden chunk jumps from Rank 12 to Rank 1!

## The Idea
1. **Bi-encoder stage (High Recall):** Fast vector / BM25 search fetches 15 candidates.
2. **Cross-encoder / Listwise stage (High Precision):** A single LLM call evaluates all candidates simultaneously, capturing cross-attention between question terms and passage content.
3. **Graceful Fallback:** If JSON parsing fails, the pipeline safely falls back to the original bi-encoder ordering.

```
Query -> Fast Retrieval -> 15 Candidates -> Listwise LLM -> Top 5 High-Precision Hits
```

## What Changed
- `rag/rerank.py`: Implemented `rerank()` with listwise scoring.
- `rag/retrieve.py`: Chains candidate generation into reranking.
- `rag/config.py`: Added toggle `USE_RERANK = True`.

View the diff:
```bash
git diff 06-query-transform..07-reranking --stat
```

## Run It
```bash
python cli.py ask "What default port does Sarah's Prometheus metrics exporter listen on?" --show-context
python cli.py eval
python eval/compare.py
```

## Results
- `noisy-top-k` recall@5 jumps significantly.
- Overall MRR (Mean Reciprocal Rank) increases.
