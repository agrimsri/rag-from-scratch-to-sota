# Lesson 06: Query Transformations — "Fix the Question"

## Goal
Bridge the semantic vocabulary gap between user inquiries and technical documentation using Multi-Query Expansion and Hypothetical Document Embeddings (HyDE).

## The Failure
Users rarely formulate queries using exact internal documentation nomenclature.
In `q032` (paraphrase), the user asks:
*"What happens if a worker node's internal clock drifts away from real time by a quarter of a second?"*
The corpus documents `error-codes.md` using the terms *"QuillLock lease validation failed due to clock skew exceeding 250ms"*.
Because the words *"quarter of a second"* and *"clock drifts"* have low lexical overlap with *"clock skew 250ms"*, standard queries can rank the target passage low.

**Before (without query transformation):**
- Query: *"What happens if a worker node's internal clock drifts away from real time by a quarter of a second?"*
- Chunks retrieved: General overview or drift rebalancing sections.

**After (with Multi-Query & HyDE):**
- Expanded queries include: *"Quillstack clock skew tolerance error"*, *"worker node clock drift limit"*.
- HyDE generates a passage predicting error code `E-3108` and 250ms lease validation.
- Target chunk retrieved at Rank 1.

## The Idea
1. **Multi-Query Expansion:** An LLM generates 2 alternate formulations from different perspectives. Each query retrieves candidates, and the lists are merged with Reciprocal Rank Fusion.
2. **HyDE (Hypothetical Document Embeddings):** An LLM generates a hypothetical answer passage. Embedding the hypothetical passage projects the query into document space rather than query space.

```
User Query: "quarter of a second clock drift"
      |
      +---> Multi-Query: ["clock skew limits", "E-3108 lease validation", ...]
      |
      +---> HyDE: "If clock skew exceeds 250ms, lease validation fails..."
      |
      v
  Fused Retrieval Candidates
```

## What Changed
- `rag/query.py`: Implemented `expand_queries()` and `hyde_passage()`.
- `rag/retrieve.py`: Integrated query transformations into retrieval pipeline.
- `rag/config.py`: Added toggles `USE_MULTI_QUERY = True`, `USE_HYDE = True`.

View the diff:
```bash
git diff 05-hybrid-search..06-query-transform --stat
```

## Run It
```bash
python cli.py ask "What happens if a worker node's internal clock drifts away from real time by a quarter of a second?" --show-context
python cli.py eval
python eval/compare.py
```

## Results
- Measurable gain in the `paraphrase` category.
- Trade-off: Extra LLM calls at query time increase overall latency.
