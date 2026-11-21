# Lesson 03: Structure-Aware Splitting & Breadcrumbs — "Respect the Document"

## Goal
Improve retrieval quality and answer synthesis by respecting document boundaries (headings, paragraphs, tables, code blocks) and enriching search vectors with structural breadcrumb metadata.

## The Failure
Fixed-size chunking (Branch 02) cuts text at arbitrary character limits. In `plans-and-pricing.md`, it split markdown tables across chunks, separating plan features from pricing notes. Furthermore, chunks lacked semantic context: a chunk stating *"The limit is 500 requests per minute."* was retrieved without knowing which plan or add-on it belonged to.

**Before (02-chunking):**
- **Question:** *"What tier and feature has the limit of 500 requests per minute?"*
- **Retrieved:** A raw text fragment lacking the parent section title.
- **Answer:** Ambiguous or inaccurate ("It applies to Quillstack API").

**After (03-structure-aware):**
- **Retrieved:** Chunk with `meta={"heading_path": "Subscription Tiers > Concurrency and Burst Quotas"}` and `embed_text="[Plans And Pricing > Subscription Tiers > Concurrency and Burst Quotas]\nUnder the Team Developer Add-on..."`
- **Answer:** *"The limit of 500 requests per minute applies to the Developer Add-on for Team workspaces."*

## The Idea
1. **Respect Structure:** Split markdown on `#` heading boundaries, then paragraphs (`\n\n`). Never split inside fenced code blocks (` ``` `) or markdown tables (`|...|`).
2. **Metadata Breadcrumbs:** Extract the full heading hierarchy path (`Doc > Section > Subsection`) and prepend it to `embed_text`.
3. **Purity of Contract:** The LLM still reads `chunk.text` (and eval checks against `chunk.text`), but embedding and vector retrieval benefit from the structural breadcrumbs.

```
Document Markdown
       |
       +---> Heading Stack: "Plans > Concurrency and Burst Quotas"
       |
       +---> Preserved Table/Block
       |
       v
Chunk: text = "Under the Team Developer Add-on..."
       embed_text = "[Plans > Concurrency and Burst Quotas]\nUnder the Team Developer Add-on..."
```

## What Changed
- `rag/chunk.py`: Replaced fixed splitter with `structure_aware_chunks()`.
- `rag/loader.py`: Populates `meta["heading_path"]` and breadcrumbs.

View the diff:
```bash
git diff 02-chunking..03-structure-aware --stat
```

## Run It
```bash
python cli.py index
python cli.py ask "What tier and feature has the limit of 500 requests per minute?" --show-context
python cli.py eval
python eval/compare.py
```

## Results
- `multi-chunk` questions score higher because tables and explanatory notes stay intact.
- `context-dependent` queries gain precision through breadcrumb matching.

## Gotchas / Trade-offs
- Tables with dozens of rows can exceed chunk budgets. In production, specialized table summarization or markdown table chunkers are needed.
