# Lesson 05: Hybrid Search & Reciprocal Rank Fusion — "Meaning and Keywords"

## Goal
Combine semantic dense embeddings with lexical keyword search (BM25) using Reciprocal Rank Fusion (RRF) to excel at both conceptual queries and exact identifier lookups.

## The Failure
Dense embeddings map sentences into smooth semantic spaces. While excellent for fuzzy concepts and paraphrasing, dense models struggle with rare alphanumeric tokens, version numbers, and error codes (`E-4417`, `E-3108`, `v3.2.1`). In dense vector space, `E-4417` looks almost identical to `E-4418` or `E-1001`.

**Before (dense only):**
- **Question:** *"What does error E-4417 mean?"*
- **Dense rank:** The exact error code chunk was often ranked #8 or lower, pushed down by general error descriptions.
- **Answer:** Misidentified error or failed exact lookup.

**After (hybrid BM25 + Dense):**
- **BM25 rank:** Rank 1 (BM25 matched the rare token `e-4417` with high IDF).
- **RRF fusion:** Boosted directly to Rank 1 with combined reciprocal score.
- **Answer:** *"Error E-4417 indicates that downstream tenant throughput quota was exceeded on the ingress pipe."*

## The Idea
1. **BM25 with Identifier Tokenization:** A lightweight, pure-Python BM25 index that retains hyphenated terms, error codes, and path strings (`e-4417`, `/dev/shm`).
2. **Dense Semantic Search:** Captures high-level meaning and paraphrase variants.
3. **Reciprocal Rank Fusion (RRF):** Fuses the two candidate rankings without needing score calibration:
   $$\text{RRF}(d) = \sum_{r \in \{\text{dense}, \text{bm25}\}} \frac{1}{60 + \text{rank}_r(d)}$$

```
Query: "What does error E-4417 mean?"
   |
   +---> Dense Search (Top 20) ---+
   |                              |---> RRF Fusion (k=60) ---> Top 5 Balanced Hits
   +---> BM25 Search  (Top 20) ---+
```

## What Changed
- `rag/bm25.py`: Custom BM25 implementation (~70 LOC) with identifier tokenization.
- `rag/retrieve.py`: Dense + BM25 multi-stage retrieval fused via `rrf_fuse()`.
- `rag/config.py`: Added toggle `USE_HYBRID = True`.

View the diff:
```bash
git diff 04-grounded-generation..05-hybrid-search --stat
```

## Run It
```bash
python cli.py ask "What does error E-4417 mean?" --show-context
python cli.py eval
python eval/compare.py
```

## Results
- **Exact category recall:** Climbs sharply.
- **Paraphrase recall:** Remains high because dense search still votes in the RRF pool.
- **Zero score calibration:** RRF works out of the box regardless of embedding cosine scale vs BM25 raw scores.
