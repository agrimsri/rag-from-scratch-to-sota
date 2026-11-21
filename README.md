# RAG From Scratch to SOTA

A hands-on, pedagogical course taking you from "embed a whole document" to a modern, production-grade RAG pipeline.

Each technique lives on its own dedicated git branch. Every branch builds on the previous one, introduces **exactly one new idea**, and measurably improves answer quality on a fixed evaluation set.

No heavy frameworks (no LangChain, no LlamaIndex). Pure Python, NumPy, Ollama, and SQLite.

📍 **You are here:** `01-whole-doc` (`step-01`) — Embedding whole documents with cosine similarity.

---

## 📊 Results Progression

| Branch / Step | Recall@5 | Hit@5 | MRR | Accuracy | Context Chars | LLM Calls | Latency (s) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 00-no-rag | 0.000 | 0.000 | 0.000 | 0.000 | 0 | 0.6 | 2.08 |
| 01-whole-doc | 0.954 | 0.954 | 0.765 | 0.521 | 51733 | 1.0 | 2.60 |

---

## 🗺️ Course Map

| # | Branch | Tag | Core Concept | Failure Fixed |
|---|---|---|---|---|
| 00 | `--no-rag` | - | Raw LLM Baseline | Model has no corpus knowledge and hallucinates |
| 01 | `01-whole-doc` | `step-01` | Embed full doc + cosine similarity | Starting point for RAG |
| 02 | `02-chunking` | `step-02` | Fixed-size sliding window chunking | Whole docs exceed embedding context and blur topics |
| 03 | `03-structure-aware` | `step-03` | Heading/paragraph aware splitting | Chunks cut mid-sentence, tables shattered |
| 04 | `04-grounded-generation`| `step-04` | Grounded prompting, citations, abstention | Answering without evidence; prompt injections |
| 05 | `05-hybrid-search` | `step-05` | Lexical BM25 + Dense + RRF | Semantic search misses exact error codes and IDs |
| 06 | `06-query-transform` | `step-06` | Multi-query expansion & HyDE | User vocabulary differs from document vocabulary |
| 07 | `07-reranking` | `step-07` | Two-stage listwise LLM reranking | Right chunk is in top-20 but not top-5 |
| 08 | `08-contextual-retrieval`| `step-08`| LLM-situated contextual chunks | Ambiguous chunks ("the limit", "this plan") |
| 09 | `09-small-to-big` | `step-09` | Child retrieval with parent expansion | Precise search chunks too small to answer from |
| 10 | `10-agentic-rag` | `step-10` | Iterative tool-calling search agent | Complex multi-hop questions across docs |
| 11 | `11-capstone` | `step-11` | Ablations, held-out test split, cost analysis | "Which techniques actually mattered?" |

---

## 🚀 Quick Start

### 1. Requirements & Setup
- Python 3.10+
- [Ollama](https://ollama.com/) running locally (`ollama serve`)
- Pulled Ollama models:
  ```bash
  ollama pull nomic-embed-text
  ollama pull llama3.2
  ```

### 2. Installation
```bash
git clone https://github.com/agrimsri/rag-from-scratch-to-sota.git
cd rag-from-scratch-to-sota
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

### 3. Verify Environment
```bash
python cli.py doctor
```

### 4. Running the Pipeline
```bash
python cli.py index
python cli.py ask "What is the atomic metering unit of Quillstack?" --show-context
python cli.py eval
python eval/compare.py
```
