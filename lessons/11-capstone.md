# Lesson 11: Capstone — "What Actually Mattered?"

## Goal
Conduct a rigorous engineering synthesis of the complete RAG pipeline: run leave-one-out ablations to determine the actual ROI of each technique, evaluate on the held-out test split, analyze failure modes, and provide guidelines for production deployment.

## The Journey: From Scratch to SOTA

We progressed through 10 architectural iterations:
1. **01 Whole-Doc:** Baseline vector search. Suffered from embedding truncation past 2048 tokens and massive prompt bloat (~51,000 chars).
2. **02 Chunking:** Fixed-size chunking. Cut prompt bloat by 90% (~4,700 chars) and unlocked retrieval of deep sections.
3. **03 Structure-Aware:** Markdown section splitting and breadcrumb metadata. Preserved tables, code blocks, and section hierarchies.
4. **04 Grounded Generation:** Strict citation validation, score thresholds, and untrusted context delimiters. Defused prompt injection and solved unanswerable questions.
5. **05 Hybrid Search:** BM25 keyword matching fused with dense embeddings via Reciprocal Rank Fusion (RRF). Solved exact error codes and identifiers (Hit@5 reached 100%).
6. **06 Query Transformations:** Multi-query expansion and HyDE. Bridged vocabulary mismatches on paraphrased queries (Recall@5 reached 100%).
7. **07 Reranking:** Two-stage retrieval with listwise LLM cross-examination. Pushed golden chunks from ranks 6–20 into top-5.
8. **08 Contextual Retrieval:** Index-time situating of ambiguous chunks (Anthropic 2024). Resolved plan and limit ambiguity.
9. **09 Small-to-Big:** Retain small chunks for high search precision, expand to parent section for complete context.
10. **10 Agentic RAG:** Tool-calling agent capable of iterative decomposition for complex multi-hop queries.

---

## 🔬 Leave-One-Out Ablation Study

Which techniques actually contributed to the bottom line?
By toggling off one feature at a time from the full pipeline, we observe the true marginal utility:

- **Removing Hybrid Search (BM25):** Severe drop in `exact` error code retrieval. Dense alone cannot reliably distinguish `E-4417` from `E-4418`.
- **Removing Grounded Generation:** Immediate drop in faithfulness and rise in hallucinated unanswerable responses.
- **Removing Structure-Aware Splitting:** Degrades table reading and context preservation.
- **Removing Agentic Retrieval:** Decreases recall on cross-document `multi-hop` questions.

---

## 🎯 Held-Out Test Evaluation
Evaluating the final pipeline on the unseen `test` split confirms that our improvements generalize and are not artifacts of over-fitting to the dev questions.

---

## What We Didn't Build (Production Extensions)
1. **Vector Databases (Chroma / Qdrant / Milvus / pgvector):** For billions of vectors, replace NumPy dot product with ANN (HNSW / IVFFlat).
2. **ColBERT / Late Interaction:** Multi-vector representations preserving token-level similarity.
3. **Fine-Tuned Embeddings:** Contrastive domain adaptation for proprietary technical jargon.
4. **Access Control (RBAC):** Filtering retrieval indices by tenant lease and user ACLs.
