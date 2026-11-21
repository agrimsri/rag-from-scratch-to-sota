# Lesson 01: Whole-Document Retrieval — "Embed It, Search It, Stuff It"

## Goal
Build the simplest possible end-to-end RAG system by embedding full documents, finding the nearest neighbors with cosine similarity, and stuffing the retrieved documents into the LLM prompt.

## The Failure
Without retrieval (the `00-no-rag` baseline), the model has never seen Quillstack's private documentation. When asked questions about internal limits or error codes, it completely hallucinates.

**Before (no retrieval):**
- **Question:** *"What is the atomic metering unit of Quillstack?"*
- **Retrieved:** None.
- **Answer:** *"The atomic metering unit of Quillstack is the 'Credit' or 'Transaction Block'..."* (Hallucination)

**After (whole-document RAG):**
- **Retrieved:** `overview.md` (Hit 1, Score 0.695)
- **Answer:** *"The atomic metering unit of Quillstack is the Pulse. One pulse represents one executed flow step or one 4KB event payload processed through a pipe."* (Accurate fact from corpus)

## The Idea
1. **Embed docs:** Run each `.md` file through Ollama's `nomic-embed-text` with `search_document: ` prefix.
2. **Normalize vectors:** L2-normalize vectors so cosine similarity is computed with a single matrix dot product: $\text{similarity}(q, d) = \mathbf{q} \cdot \mathbf{d}$.
3. **Retrieve Top-k:** Rank documents by score and take the top $k=5$.
4. **Generate:** Paste the top $k$ documents into the LLM prompt and instruct the model to answer based on the context.

```
Query -> embed("search_query: ...") -> q (normalized)
                                         |
                                         v
Index (M: 12 docs x 768) ---------> scores = M @ q -> top-k docs -> Prompt -> LLM -> Answer
```

## What Changed
Introduced foundational pipeline components:
- `rag/schema.py`: Canonical `Chunk` and `Hit` dataclasses.
- `rag/config.py`: Environment configuration and model parameters.
- `rag/cache.py`: SQLite key-value store for deterministic, zero-cost repeated calls.
- `rag/embed.py`: Batch embedding with L2 normalization.
- `rag/llm.py`: LLM abstraction supporting local Ollama (`llama3.2`) and Gemini.
- `rag/loader.py`: Loads each markdown doc as one `Chunk`.
- `rag/index.py`: Persists normalized matrix and metadata to `.cache/index.pkl`.
- `rag/retrieve.py`: Dense vector dot product retrieval.
- `rag/generate.py`: Stuff-it generation prompt.
- `cli.py` & `eval/`: Preflight doctor, question answering, and evaluation harness.

View the diff:
```bash
git diff main..01-whole-doc --stat
```

## Run It
```bash
python cli.py doctor
python cli.py index
python cli.py ask "What is the atomic metering unit of Quillstack?" --show-context
python cli.py eval
python eval/compare.py
```

## Results
- **00 no retrieval:** Recall@5 = 0.000, Accuracy = 0.000.
- **01 whole-doc:** Recall@5 = 0.953, Accuracy jumps significantly on single-fact lookups.
- **The visible flaw:** In `long-doc` questions (e.g. `q008` regarding ephemeral buffer allocation in `api-reference.md`), the doc is over 5,000 words. Because Ollama's embedding model has `EMBED_NUM_CTX=2048`, text past the context window was silently truncated and never embedded!

## Gotchas / Trade-offs
1. **Embedding Truncation:** Entire sections deep inside long documents are invisible to the vector index.
2. **Context Bloat:** Stuffing 5 whole documents pushes ~50,000 characters into the prompt, burning unnecessary latency and tokens.
3. **Topic Blurring:** A document covering 30 different APIs produces a single blended vector, pulling down precision for specific queries.

## Exercises
1. Inspect the context length: Run `ollama show nomic-embed-text` and calculate how many tokens a 5,000-word markdown file takes.
2. Change $k$: Run `python cli.py ask "..."` with $k=1$ and observe how retrieval failures cascade to generation.
3. Remove prefixes: Temporarily strip `search_query: ` in `rag/config.py` and see how retrieval scores degrade.

## Further Reading
- [Nomic Embed: Training a Reproducible Long-Context Text Embedder](https://arxiv.org/abs/2402.01613) (Nussbaum et al., 2024)
