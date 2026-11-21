# Lesson 10: Agentic RAG — "Let the Model Decide What to Look Up"

## Goal
Solve complex multi-hop questions across disparate documents by allowing the LLM to dynamically formulate queries, read intermediate evidence, and perform iterative follow-up searches.

## The Failure
Single-pass retrieval pipelines assume one search query is sufficient to locate all required evidence.
In `q050` (multi-hop):
*"How much does the Business tier cost, and does it include Customer-Managed Encryption Keys (CMEK)?"*
- Finding the Business tier price requires searching `plans-and-pricing.md`.
- Verifying CMEK specifications requires searching `security-and-compliance.md`.

In single-pass RAG, a hybrid search query for the combined question often retrieves only one of the two documents in the top 5, causing the generator to fail or hallucinate the other half.

**Before (single-pass retrieval):**
- Single query only retrieved `plans-and-pricing.md`.
- Failed on CMEK details from `security-and-compliance.md`.

**After (agentic search):**
- Step 1: Searches *"Quillstack Business tier monthly price"* -> Finds $299/mo in `plans-and-pricing.md`.
- Step 2: Agent observes missing CMEK info and issues follow-up search: *"Quillstack Business plan CMEK customer managed encryption keys"* -> Finds AWS & GCP KMS support in `security-and-compliance.md`.
- Step 3: Generator synthesizes both findings with complete citations!

## The Idea
1. **Dynamic Tool Use:** The LLM is provided with an iterative `search(query: str)` loop wrapping the retrieval pipeline.
2. **Step Budget:** Strict execution limit (max 3 iterations) prevents runaway loops.
3. **Retrieval Only:** The agent's responsibility is purely evidence collection. All gathered passages are handed off to the grounded generator (Branch 04) for final answer formatting.

```
Question -> Agent (LLM) ---> Tool: search(Query 1) ---> Hits 1
               ^                   |
               +--- Inspect -------+
               |
               v
         Tool: search(Query 2) ---> Hits 2 ---> Deduplicate -> Grounded Generator -> Final Answer
```

## What Changed
- `rag/agent.py`: Created `agent_search_loop()`.
- `rag/pipeline.py`: Added toggle `USE_AGENT = True` routing queries through the agentic loop.
- `rag/config.py`: Set `USE_AGENT = True`.

View the diff:
```bash
git diff 09-small-to-big..10-agentic-rag --stat
```

## Run It
```bash
python cli.py ask "How much does the Business tier cost, and does it include Customer-Managed Encryption Keys (CMEK)?" --show-context
python cli.py eval
python eval/compare.py
```

## Results
- `multi-hop` category accuracy reaches its peak.
- Trade-off: Higher latency and multiple LLM calls per question.
