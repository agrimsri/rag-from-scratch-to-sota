# Lesson 02: Fixed-Size Chunking — "Search the Part, Not the Whole"

## Goal
Solve the embedding truncation and topic-blurring failures of whole-document retrieval by breaking documents into fixed-size character chunks with sliding-window overlap.

## The Failure
In Branch 01, `q008` asked about the Shardlet rebalance drift tolerance (`shard_drift_tolerance_pct = 14.5%`), located deep inside `api-reference.md` (~5,200 words). Because Ollama's `nomic-embed-text` truncates inputs past token 2048, that section was never embedded.

**Before (01-whole-doc):**
- **Question:** *"What is the shard drift tolerance percentage that triggers an immediate rebalance?"*
- **Recall@5:** 0.00 (The evidence string was never retrieved in top 5).
- **Answer:** Incorrect / Failed.

**After (02-chunking):**
- **Retrieved:** `api-reference.md#28` (Hit 1, Score 0.742)
- **Recall@5:** 1.00 (The exact sub-chunk containing the drift tolerance formula was retrieved at rank 1).
- **Answer:** *"The shard drift tolerance percentage is 14.5%."*

## The Idea
Documents are often thousands of words long, but user questions typically target a specific paragraph. By splitting text into smaller chunks (e.g. 1000 characters with 200 character overlap):
1. **No truncation:** Every section of the document gets embedded.
2. **Sharp vector representations:** Each vector represents a single cohesive concept rather than an entire book.
3. **Sliding window overlap:** Overlap prevents facts positioned near chunk boundaries from being sliced in half.

```
[------------- Chunk 0 (1000 chars) -------------]
                           [============= Overlap (200 chars) =============]
                           [------------- Chunk 1 (1000 chars) -------------]
```

## What Changed
- `rag/chunk.py`: Created `fixed_size_chunks(text, size=1000, overlap=200)`.
- `rag/config.py`: Added `CHUNK_SIZE = 1000` and `CHUNK_OVERLAP = 200`.
- `rag/loader.py`: Generates indexed chunks named `<doc>#<index>` instead of single doc chunks.
- `scripts/sweep_chunk_size.py`: Parameter sweep tool across sizes and overlaps.

View the diff:
```bash
git diff 01-whole-doc..02-chunking --stat
```

## Run It
```bash
python scripts/sweep_chunk_size.py
python cli.py index
python cli.py ask "What is the shard drift tolerance percentage that triggers an immediate rebalance?" --show-context
python cli.py eval
python eval/compare.py
```

## Results
- **Prompt context chars:** Plummeted from **~51,700 chars** to **~4,900 chars** (a 10x reduction in prompt bloat).
- **Long-doc Recall:** Rose significantly as truncated sections are now indexable.
- **The new visible flaw:** Fixed-size chunking cuts text mechanically mid-thought, often splitting markdown tables or separating a critical sentence from its section header.

## Gotchas / Trade-offs
- **Tokens vs Characters:** We chunk by characters for simplicity and zero-dependency portability. In production, tokenizer-aware chunking aligns chunks with exact LLM context limits.
- **Chunk Size Dilemma:** Too small = loss of surrounding context; too big = vector dilution and truncation.

## Exercises
1. Run `python scripts/sweep_chunk_size.py` with overlap 0 and note the drop in recall.
2. Try `CHUNK_SIZE=200` and see what happens to `multi-chunk` questions.
