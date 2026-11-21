# RAG From Scratch to SOTA — Build Spec for the Coding Agent

You are building a **teaching repository** that takes students from "embed a whole document" to a modern,
production-style RAG pipeline. Each concept lives on its own **git branch**. Every branch builds on the previous
one, adds exactly one idea, and measurably improves answer quality on a fixed evaluation set.

The repo is the textbook. Students will `git checkout` a branch, read a small diff, run it, see the numbers move.

Read this whole file before writing any code.

---

## 1. Goals and non-goals

**Goals**

- A natural story: every branch exists because the previous branch **fails in a way students can see**.
- Minimal, readable code. A student with basic Python should understand any branch in 15 minutes.
- Every branch is runnable end-to-end and reports the same metrics, so progress is visible as a table.
- Practical techniques only: things people actually ship.

**Non-goals**

- No LangChain, LlamaIndex, Haystack, or any RAG framework. We build the parts ourselves.
- No vector database in the main line (numpy brute-force is enough and is more instructive). One optional extension branch may add one.
- No web UI, no async, no Docker, no packaging. CLI only.

## 2. Stack and environment

| Piece                                                                | Choice                                                                                                                            |
| -------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| Language                                                             | Python 3.10+                                                                                                                      |
| Embeddings                                                           | **Ollama**, local. Default `nomic-embed-text`. Config-switchable to `embeddinggemma`, `qwen3-embedding:0.6b`, `mxbai-embed-large` |
| LLM (generation, query rewriting, reranking, contextualizing, agent) | **Gemini API, free tier**, via the `google-genai` SDK (`from google import genai`). NOT the legacy `google-generativeai` package  |
| Vector search                                                        | numpy, normalized vectors, cosine = dot product                                                                                   |
| Keyword search                                                       | BM25 written by hand (branch 05)                                                                                                  |
| Cache                                                                | stdlib `sqlite3` key-value cache for embeddings and LLM calls                                                                     |
| Dependencies                                                         | `numpy`, `ollama`, `google-genai`, `python-dotenv`. Nothing else unless unavoidable                                               |

**Facts you must verify, not assume** (they change fast; do this in preflight and write the findings into `README.md`):

1. **Gemini model IDs churn quickly.** Do not trust names in this file or in your memory. In `cli.py doctor`, call `client.models.list()` and pick current Flash and Flash-Lite IDs available to the key. Put them only in `.env` / `config.py` as `GEMINI_MODEL` (quality) and `GEMINI_MODEL_FAST` (bulk: judging, reranking, contextualizing). Never hard-code a model ID anywhere else.
2. **Thinking tokens.** Current Flash models may "think" by default, which burns quota and latency. Check the current docs for how to minimize/disable thinking and set it low for bulk calls.
3. **Free-tier limits** are per project (RPM, TPM, RPD) and differ per model. Read them from the docs or AI Studio, put the RPM in `.env` as `GEMINI_RPM`, and have `llm.py` respect it.
4. **Ollama embedding context.** Check the real context length (`ollama show <model>`). Ollama truncates over-long inputs. We rely on this on purpose in branch 01 (see §9). Expose `EMBED_NUM_CTX` in config (default `2048`) and pass it as an option.
5. **Embedding prefixes.** `nomic-embed-text` wants `search_document: ` / `search_query: ` prefixes; other models differ (check each model card). Make `EMBED_DOC_PREFIX` / `EMBED_QUERY_PREFIX` config values. Wrong prefixes silently hurt quality.
6. **Free-tier data terms.** Free-tier prompts may be used by Google to improve its products. The corpus is synthetic, so this is fine; say so in the README and warn students not to send private data.

If Ollama or the Gemini key is unreachable, **stop and tell me**. Do not mock either service.

`.env.example`:

```
GEMINI_API_KEY=
GEMINI_MODEL=            # filled from `doctor`
GEMINI_MODEL_FAST=       # filled from `doctor`
GEMINI_RPM=10
OLLAMA_HOST=http://localhost:11434
OLLAMA_EMBED_MODEL=nomic-embed-text
EMBED_NUM_CTX=2048
EMBED_DOC_PREFIX=search_document:
EMBED_QUERY_PREFIX=search_query:
```

## 3. Git workflow

- `main` = **bootstrap only**: README, `.gitignore`, `.env.example`, `requirements.txt`, the corpus (`data/docs/`), the eval dataset and its validator. No pipeline code. This is "start here" for students, and it keeps the corpus and dataset **identical across every branch**.
- Branches, in order, each created from the previous one (never from `main`, except 01):

```
01-whole-doc        02-chunking          03-structure-aware   04-grounded-generation
05-hybrid-search    06-query-transform   07-reranking         08-contextual-retrieval
09-small-to-big     10-agentic-rag       11-capstone
```

- Tag the head of each branch `step-01` … `step-11`.
- Each branch: 2–4 commits: `feat: …`, `eval: results for NN`, `docs: lesson NN`. Short, imperative messages.
- **Fixing something in an earlier branch** (bug, dataset change): fix it there, then merge forward through every later branch in order:
  ```
  git checkout 04-grounded-generation && git merge 03-structure-aware
  git checkout 05-hybrid-search       && git merge 04-grounded-generation   # …and so on
  ```
  Then re-run evals on every affected branch so the results table stays truthful.
- Students compare steps with `git diff 04-grounded-generation..05-hybrid-search --stat`. **Keep diffs small and focused**; that is the product.
- Never commit `.env`, `.cache/`, or anything with a key.

## 4. Code style (this is a teaching repo)

- Plain functions and dicts/dataclasses. A class only if it earns its place.
- Functions ≤ ~30 lines. Docstring says **why**, not just what.
- Type hints on signatures. No metaprogramming, no decorators beyond `@dataclass`.
- One new concept per branch. If you are tempted to add a second, it belongs in the next branch.
- Hyper-parameters live in `rag/config.py` with a one-line comment each. Technique toggles are plain booleans (`USE_HYBRID = True`) so students can ablate by flipping one line.
- Prefer clarity over cleverness over performance. Corpus is small.
- LOC budget per branch (delta over previous): 01 ≈ 300 total, 02 +30, 03 +40, 04 +40, 05 +50, 06 +50, 07 +50, 08 +70, 09 +50, 10 +90, 11 ≈ polish only. If you blow a budget by >50%, simplify.

## 5. Repo layout (stable across branches, so diffs stay small)

```
data/docs/*.md              # corpus (on main)
eval/dataset.jsonl          # questions (on main)
eval/validate_dataset.py    # checks every evidence string occurs verbatim in the corpus (on main)
eval/run_eval.py            # metrics (01)
eval/compare.py             # prints the cross-branch results table (01)
eval/results/NN-name.json   # one file per branch, committed
rag/config.py               # env + hyper-parameters
rag/cache.py                # sqlite kv cache
rag/llm.py                  # Gemini wrapper: generate(), generate_json(); rate limit, retry, cache
rag/embed.py                # Ollama wrapper: embed(texts, kind="doc"|"query"); batching, normalize, cache
rag/schema.py               # Chunk, Hit dataclasses
rag/loader.py               # read docs
rag/chunk.py                # (02+)
rag/index.py                # build / save / load index
rag/retrieve.py             # retrieve(query, index, k) -> list[Hit]  (grows stage by stage)
rag/generate.py             # answer from hits
rag/pipeline.py             # ask(question) -> dict
cli.py                      # doctor | index | ask | eval
scripts/                    # small experiment scripts (e.g. sweep_chunk_size.py in 02)
lessons/NN-name.md          # one-page lesson per branch
README.md
```

### Contracts (introduce in 01 and **never break them**)

```python
@dataclass
class Chunk:
    id: str          # "pricing.md#3"
    doc: str         # "pricing.md"
    text: str        # what the LLM reads and what eval checks against
    embed_text: str  # what is embedded / BM25-indexed (== text until branch 08)
    meta: dict       # heading path, position, parent_id, ... grows over time

@dataclass
class Hit:
    chunk: Chunk
    score: float

def retrieve(query: str, index, k: int) -> list[Hit]: ...

def ask(question: str) -> dict:
    # {"answer": str, "answerable": bool | None, "citations": [chunk ids],
    #  "hits": [Hit...], "trace": [str], "llm_calls": int}
```

In branch 01 a whole document **is** one `Chunk`. That is the trick that keeps every later diff small: chunking later just changes how `Chunk`s are made.

`cli.py` commands (from 01): `doctor` (checks Ollama + Gemini, lists models, runs one embed + one generate), `index`, `ask "…" [--show-context]` (prints answer, citations, and retrieved chunks with scores; this powers live demos), `eval [--split dev|test] [--retrieval-only] [--judge] [--no-rag] [--limit N]`.

## 6. Corpus (build on `main`, before any branch)

A **synthetic** knowledge base so the LLM cannot already know the answers (that is what makes "no retrieval" fail honestly).

Invent one fictional developer-platform company, **Quillstack**. Write ~12 markdown docs, ~25–30k words total, realistic and a bit messy, with headings, tables, lists, code blocks, and cross-references between docs:

`overview.md` · `plans-and-pricing.md` · `api-reference.md` (long) · `error-codes.md` · `sdk-guide.md` (long) · `security-and-compliance.md` · `sla-and-incident-policy.md` · `data-retention-and-privacy.md` · `migration-v2-to-v3.md` · `employee-handbook.md` (long, different domain) · `runbook-oncall.md` (long) · `community-forum-export.md` (noisy Q&A; contains **one planted prompt-injection sentence**, e.g. text telling the assistant to ignore its instructions)

Rules:

- At least four docs ≥ ~4,000 words so they overflow `EMBED_NUM_CTX=2048` by a wide margin.
- Plant facts deliberately to create each failure category in §7. Write them yourself; do not have an LLM generate the corpus, because planted facts must be exact and consistent.
- Make some facts look similar across docs (plan limits vs. API limits; v2 vs. v3 behavior) so retrieval has to discriminate.
- Include chunks that read ambiguously on their own ("The limit is 500 requests per minute." with the product/plan named only in the section heading or earlier paragraph).

## 7. Evaluation set (build on `main`, freeze before branch 01)

`eval/dataset.jsonl`, one JSON object per line:

```json
{
  "id": "q017",
  "split": "dev",
  "category": "exact",
  "question": "What does error E-4417 mean?",
  "answerable": true,
  "reference_answer": "…",
  "answer_keys": ["rate limit", "429"],
  "evidence": [
    "verbatim string from the corpus that contains the answer",
    "…second string if multi-hop…"
  ],
  "docs": ["error-codes.md"]
}
```

- **~60 questions**: 45 `dev` (used while building and in every results table) and 15 `test` (held out; only run in the capstone, once, to show students about over-tuning).
- ≥ 5 dev questions per category:

| category                 | what it stresses                                                      | which branch should help      |
| ------------------------ | --------------------------------------------------------------------- | ----------------------------- |
| `lookup`                 | easy single fact, shared wording with the doc                         | baseline (01)                 |
| `long-doc`               | answer is deep inside a long doc, past the embedding truncation point | 02                            |
| `multi-chunk`            | answer spans adjacent paragraphs / a table plus the note under it     | 03, 09                        |
| `unanswerable`           | not in the corpus; correct behavior is to abstain                     | 04                            |
| `exact`                  | IDs, error codes, version strings, identifiers                        | 05                            |
| `paraphrase`             | question shares almost no words with the doc                          | 06 (and dense retrieval)      |
| `noisy-top-k`            | right chunk is retrieved but ranked 6–20                              | 07                            |
| `context-dependent`      | the chunk alone is ambiguous (which plan? which version?)             | 08                            |
| `multi-hop`              | needs facts from two different docs                                   | 10                            |
| `adversarial` (2–3 only) | retrieved text contains an injected instruction                       | 04 (prompt hygiene), capstone |

- `evidence` strings must be **verbatim substrings** of the corpus. `eval/validate_dataset.py` checks that (after whitespace normalization), checks the category counts, and fails loudly otherwise. Run it in CI-style fashion before every eval.
- `answer_keys`: short normalized strings that must all appear in a correct answer (e.g. `"99.95%"`). This gives a **free, deterministic correctness check** with no LLM judge. Write them carefully (accept obvious variants via simple alternatives like `["30 days|thirty days"]`, where `|` means OR).
- Unanswerable questions have `answerable: false`, empty `evidence`, empty `answer_keys`.

**Dataset honesty rule.** If a technique doesn't help its target category, first ask whether the dataset really exhibits that failure. You may revise corpus/questions on `main` so the _realistic_ failure exists, then merge forward and re-run everything. You may **never** change a question to make a specific technique win, never touch the metrics to flatter a result, and never fake numbers. If a technique legitimately gives no gain or hurts, record that and say so in the lesson. That is a valuable lesson too.

## 8. Eval harness (`eval/run_eval.py`, built in 01, reused everywhere)

Metrics, computed per category and overall:

- **Retrieval** (free, local, no LLM): `recall@k` = fraction of `evidence` strings found (normalized substring) in the **original `chunk.text`** of the top-k hits; `hit@k` (any evidence found); `MRR` of first hit containing evidence. Always check `chunk.text`, never `embed_text`, so contextual-retrieval prefixes can't inflate scores.
- **Context size**: `avg_context_chars` of what is actually passed to the LLM. Report it next to recall so techniques that "win" by stuffing more text are visible (matters for branch 09).
- **Answer correctness**: all `answer_keys` present in the answer. Free.
- **Faithfulness and abstention** (`--judge`, uses `GEMINI_MODEL_FAST`, temperature 0, cached): judge returns `{"faithful": bool}` (is every claim supported by the retrieved context?). For `unanswerable`, correct = the system abstained (judge decides in 01–03; from 04 use the structured `answerable` field, optionally cross-checked by the judge).
- **Cost**: `llm_calls` per question and wall-clock latency per question.

Output: `eval/results/NN-name.json` (per-question rows plus aggregates). `eval/compare.py` prints a table of all result files, one row per branch, and can emit Markdown (`--markdown`) for the README. Add `--no-rag` (answer with Gemini only, no context) so the table starts with a **"00 no retrieval"** row. Teaching moment: it hallucinates on the fictional company.

Quota hygiene: all LLM and embedding calls are cached by hash of (model, prompt/config, text). `--retrieval-only` runs the whole retrieval metric with zero Gemini calls; use it for fast iteration. Run `--judge` only when finalizing a branch's numbers.

## 9. Course map

| #   | Branch                    | New idea                                                                | Failure of the previous step it fixes            |
| --- | ------------------------- | ----------------------------------------------------------------------- | ------------------------------------------------ |
| 00  | (eval flag) `--no-rag`    | the baseline                                                            | LLM has no knowledge of the corpus, hallucinates |
| 01  | `01-whole-doc`            | embeddings + cosine search + stuff into prompt                          | (starting point)                                 |
| 02  | `02-chunking`             | fixed-size chunks with overlap                                          | one vector per doc is truncated and blurry       |
| 03  | `03-structure-aware`      | split on headings/paragraphs, keep tables intact, heading-path metadata | chunks cut mid-thought                           |
| 04  | `04-grounded-generation`  | grounded prompt, citations, abstain, untrusted-context hygiene          | model answers even when retrieval found nothing  |
| 05  | `05-hybrid-search`        | BM25 + dense + Reciprocal Rank Fusion                                   | dense search misses exact IDs and rare terms     |
| 06  | `06-query-transform`      | multi-query expansion and HyDE                                          | user wording ≠ document wording                  |
| 07  | `07-reranking`            | retrieve wide, rerank narrow                                            | right chunk is in the top 20 but not the top 5   |
| 08  | `08-contextual-retrieval` | LLM-written context prepended to each chunk at index time               | chunks that are ambiguous on their own           |
| 09  | `09-small-to-big`         | search small, hand the LLM the surrounding section                      | precise chunks too small to answer from          |
| 10  | `10-agentic-rag`          | LLM decides what to search, searches again, decomposes                  | multi-hop questions need several searches        |
| 11  | `11-capstone`             | ablations, held-out test, cost/latency, failure analysis                | "which of these actually mattered?"              |

---

## 10. Branch specifications

Every branch must satisfy the **per-branch deliverables** in §11.

### 01-whole-doc — "Embed it, search it, stuff it"

- **Concept:** what an embedding is, cosine similarity, retrieve-then-generate. The smallest possible RAG.
- **Build:** all files in §5 except `chunk.py`. `loader.py` reads docs; each doc becomes one `Chunk`. `embed.py` batches through `ollama.embed(model=…, input=[…], options={"num_ctx": EMBED_NUM_CTX})`, L2-normalizes with numpy, caches. `index.py` saves a vector matrix plus chunk records under `.cache/`. `retrieve.py`: embed query (query prefix), `scores = M @ q`, top-k. `generate.py`: a plain prompt "Answer using this context" with the top-k docs pasted in. `cli.py` and `eval/` complete, including `--no-rag`, `doctor`, `--show-context`.
- **Teach:** why normalize; query vs. document prefixes; why we cache; what `k` does.
- **Visible failures to set up** (pick real dataset questions after running and put them in the lesson):
  1. `long-doc` questions fail: Ollama silently truncated the doc to `EMBED_NUM_CTX`, so the answer was never embedded. Add a small `inspect` output (or a lesson snippet) that compares doc length to the context window to make the truncation tangible.
  2. One vector per doc blurs topics together.
  3. Pasting whole documents wastes context, latency, and money.
- **Expected movement:** no-RAG very low (hallucinates; may "abstain" by luck on some unanswerable). 01 decent on `lookup`, poor on `long-doc`, `exact`, `context-dependent`.
- **Talking point for the lesson:** "Why not just put the whole corpus in the prompt?" (Gemini has a huge context.) Answer honestly: it works for a toy corpus; cost/latency/accuracy-on-long-context/scale/permissions are why RAG exists. Optional measured version in the capstone.
- **Exercises:** switch the embedding model; change `k`; try wrong prefixes and watch recall drop.

### 02-chunking — "Search the part, not the whole"

- **Concept:** chunking, chunk size vs. precision, overlap.
- **Build:** `chunk.py: fixed_size_chunks(text, size, overlap) -> list[str]` (characters, to keep it simple; explain tokens vs. characters in the lesson). `index.py` creates multiple `Chunk`s per doc with ids like `doc#i`. Config: `CHUNK_SIZE`, `CHUNK_OVERLAP`, `TOP_K`. Add `scripts/sweep_chunk_size.py`: sweep sizes (e.g. 200/500/1000/2000) × overlaps, print `recall@k` and `avg_context_chars` per setting. Retrieval-only, so it's free.
- **Teach:** the precision/context trade-off; why overlap exists; why `k` and chunk size interact. Show a chunk cut mid-sentence as the new problem.
- **Expected movement:** big jump on `long-doc`; `recall@k` up across the board; `avg_context_chars` down vs. 01.
- **Exercises:** make the sweep plot; try overlap 0; find where bigger chunks start hurting.

### 03-structure-aware — "Respect the document"

- **Concept:** recursive/structure-aware splitting and metadata.
- **Build:** replace the splitter with a recursive one: split on markdown headings, then blank lines, then sentences, merging up to `CHUNK_SIZE`. Never split inside a table or fenced code block (keep them whole even if over the limit). Store `meta = {"heading_path": "Plans > Limits", "pos": i}`. Show the heading path in citations and prepend a one-line breadcrumb (`Doc title > Section`) to `embed_text`. This is a cheap, non-LLM form of "context", which sets up branch 08.
- **Teach:** documents have structure; metadata is free signal; a breadcrumb is context.
- **Expected movement:** `multi-chunk` improves modestly (tables stay with their notes); small gains on `context-dependent`.
- **Exercises:** compare breadcrumb on/off; add a doc type to `meta` and filter on it.

### 04-grounded-generation — "Answer only from evidence"

- **Concept:** grounded prompting, citations, abstention, treating retrieved text as untrusted data.
- **Build:**
  - New generation prompt: answer only from the numbered context; cite chunk ids; if the context doesn't contain the answer, say so. Wrap context in clear delimiters and state that it is data, not instructions (this defuses the planted injection).
  - Gemini structured output: `{"answer": str, "answerable": bool, "citations": [str]}` via `response_mime_type="application/json"` with a schema.
  - Programmatic check: every cited id must be among the retrieved ids; drop or flag invented citations.
  - A simple retrieval-level guard: if the top score is below `MIN_SCORE`, abstain without calling the LLM (calibrate the threshold on dev; show the score distribution of answerable vs. unanswerable questions).
  - Raise `TOP_K` to ~5 now that the prompt can handle it.
- **Teach:** hallucination is a generation problem as much as a retrieval problem; abstaining is a feature; what a threshold costs (false abstentions).
- **Expected movement:** `unanswerable` and faithfulness jump; `adversarial` improves; answer accuracy on answerable questions should not drop. Report any false-abstention rate honestly.
- **Exercises:** break the prompt on purpose and watch faithfulness fall; find the threshold sweet spot.

### 05-hybrid-search — "Meaning and keywords"

- **Concept:** lexical (BM25) vs. semantic (dense) retrieval; Reciprocal Rank Fusion.
- **Build:** `rag/bm25.py` (~40 lines: tokenizer, document frequencies, idf, `k1=1.5`, `b=0.75`, `score(query)`). The tokenizer must keep identifiers like `E-4417` and `v3.2.1` searchable (emit the whole token plus its parts). `retrieve.py`: dense top-N and BM25 top-N (N≈20), fuse with RRF (`score = Σ 1/(60 + rank)`), return top-k. Toggle `USE_HYBRID`.
- **Teach:** dense search is great at paraphrase and bad at rare strings; BM25 is the reverse; RRF needs no score calibration, which is why it's the go-to fusion. Show one query where each alone fails.
- **Expected movement:** large gain on `exact`; paraphrase stays good (dense still contributes).
- **Exercises:** try weighted fusion; try different `k1`/`b`; add stop-word removal and see if it matters.

### 06-query-transform — "Fix the question"

- **Concept:** query expansion. Two techniques, each behind its own toggle:
  - **Multi-query:** one fast-model call returns 3 rewrites (different wording / sub-aspects); retrieve for each, RRF-merge with the original.
  - **HyDE:** the model writes a short hypothetical answer passage; embed that instead of/in addition to the query for the dense side.
- **Build:** `rag/query.py` (`expand_queries`, `hyde_passage`), wired into `retrieve.py`. Cached LLM calls. Record the generated queries in `trace` so students can read them.
- **Teach:** queries and documents live in different "languages"; the cost is one extra LLM call per question (latency!), and expansions can also add noise.
- **Expected movement:** gains on `paraphrase`; maybe small elsewhere. **Run an ablation** (neither / multi-query / HyDE / both) and report all four honestly. If HyDE hurts factual lookups, default it to off and say why. Do not hide this.
- **Exercises:** inspect bad expansions; try a one-call "rewrite + HyDE" variant.

### 07-reranking — "Retrieve wide, read narrow"

- **Concept:** two-stage retrieval. Bi-encoders are fast but coarse; a reranker reads query and passage together.
- **Build:** `rag/rerank.py: rerank(query, hits, top_n) -> list[Hit]`. Retrieve `RERANK_CANDIDATES=30` via the current pipeline, then rerank with one **listwise** Gemini call (`GEMINI_MODEL_FAST`): numbered passages truncated to ~600 chars, return JSON `[{"id": n, "score": 0-10}]`. On any parse or API failure, fall back to the original order and note it in `trace`. Keep the function interface clean so students can swap in a local cross-encoder (mention `bge-reranker` / `qwen3-reranker` style models, don't build them).
- **Teach:** recall vs. precision stages; why we rerank 30 not 3000; the extra latency and cost; position bias in LLM judges.
- **Expected movement:** `noisy-top-k` improves strongly; `MRR` and answer accuracy up; `recall@5` rises because the right chunk moves into the top 5.
- **Exercises:** vary candidate count; compare pointwise vs. listwise.

### 08-contextual-retrieval — "Give every chunk its context back"

- **Concept:** contextual retrieval (Anthropic, 2024): at **index time**, an LLM writes 1–2 sentences situating each chunk within its document; prepend that to the chunk before embedding **and** before BM25. Link the original post in the lesson: https://www.anthropic.com/news/contextual-retrieval
- **Build:** `rag/contextualize.py`. Per doc, send the full document plus chunks in **batches of ~8 chunks per call**, ask for JSON `[{"id":…, "context":…}]`. This keeps the free-tier request count low. Resume-safe via the sqlite cache. Then `embed_text = context + "\n" + text`; `text` stays the original (LLM answer generation reads `text`; optionally show context in citations). Print an index-time cost summary (LLM calls, tokens if available).
- **Teach:** ambiguity ("the limit", "it", "this plan") is the silent killer of chunk retrieval; this trades one-time index cost for query-time quality. Compare with the cheap breadcrumb from 03.
- **Expected movement:** strong gain on `context-dependent`; helps BM25 too. Report the index-time cost.
- **Exercises:** contextualize only a subset; compare "context in embedding only" vs. "in BM25 only" vs. both.

### 09-small-to-big — "Find with small, read with big"

- **Concept:** parent-document / small-to-big retrieval. Small chunks match precisely; the LLM often needs the surrounding section to answer.
- **Build:** each chunk carries `meta["parent_id"]` (its markdown section) and neighbor order. After retrieval and reranking, `expand(hits)` swaps each hit for its parent section if it fits `MAX_PARENT_CHARS`, else for the hit plus ±`NEIGHBOR_WINDOW` neighbors. Deduplicate overlapping expansions and enforce a total `CONTEXT_BUDGET_CHARS`. Optionally sweep a smaller child size now that expansion compensates (the contextualization cache means re-running 08 for new chunk boundaries costs LLM calls; mention that).
- **Teach:** precision for finding, context for answering; budgets matter. **Always compare at equal context size**, since this is the branch where cheating by sending more text is easiest. Report `avg_context_chars` beside accuracy.
- **Expected movement:** `multi-chunk` improves; answer accuracy up at similar or modestly larger context.
- **Exercises:** vary `NEIGHBOR_WINDOW`; make a failure case where expansion drags in distracting text.

### 10-agentic-rag — "Let the model decide what to look up"

- **Concept:** agentic retrieval: the model issues searches, reads results, and searches again. Handles multi-hop questions and sufficiency checks.
- **Build:** `rag/agent.py`. Give Gemini a `search(query: str) -> str` tool that wraps the existing `retrieve` pipeline (including hybrid, rerank, expand) and returns formatted chunks with ids. Use the SDK's tool-calling support (pass the Python function in the config; check the current docs for automatic function calling and set a maximum number of remote calls, e.g. 4–5). Record every tool call in `trace`. The agent's job is **only retrieval**: collect and dedupe the chunks it retrieved, cap to the context budget, then hand them to the **same** grounded generator from branch 04 for the final structured answer (structured output and tool calling don't always combine). Add a step budget and a clear stop condition ("enough evidence" or budget exhausted → abstain). Config toggle `USE_AGENT`; optional tiny router: single-pass for simple questions, agent only when the model says the question needs decomposition.
- **Teach:** decomposition, iteration, the step budget, and the honest costs (several LLM calls, latency, non-determinism). When not to use an agent: most questions don't need one.
- **Expected movement:** `multi-hop` improves clearly; other categories roughly flat; `llm_calls` and latency up. Show the cost table.
- **Exercises:** read agent traces for the failures; tighten the system prompt; compare agent vs. multi-query (06).

### 11-capstone — "What actually mattered?"

No new retrieval technique. This branch turns the build into a lesson on engineering judgment.

- **Leave-one-out ablation table:** the full pipeline vs. disabling each of 03/04/05/06/07/08/09/10 one at a time (by config toggle). Present it as the answer to "which techniques earned their cost?"
- **Held-out test split:** run `--split test` **once** on the final pipeline and compare with dev. Explain over-tuning.
- **Cost/latency table:** LLM calls and seconds per question per branch; index-time cost for 08.
- **Failure analysis:** `lessons/11-capstone.md` lists the remaining failing questions with a one-line diagnosis each (retrieval miss, ranking, generation, dataset issue).
- **Optional measured baseline:** `--full-context` (whole corpus in the prompt, paced to respect TPM). It may score well on this small corpus; report it honestly next to cost and latency and tie it back to why scale, cost, and access control still favor RAG.
- **What we didn't build** (short pointers, no code): GraphRAG, late-interaction (ColBERT-style), fine-tuning embeddings, late chunking, multimodal RAG, incremental indexing and freshness, access control, prompt-injection defense in depth.
- **Optional extension branches** from `11-capstone`, if time allows: `x-vector-db` (swap numpy for sqlite-vec/FAISS/Chroma, show nothing else changes) and `x-local-reranker` (local cross-encoder).

---

## 11. Per-branch deliverables (checklist)

For every branch, before moving on:

1. `python cli.py doctor` and `python cli.py ask "<a dataset question>" --show-context` work.
2. `python eval/validate_dataset.py` passes.
3. `python cli.py eval --retrieval-only` runs; then the full `eval --judge` run; results saved to `eval/results/NN-name.json`.
4. `lessons/NN-name.md` written using this template (≤ one page, plain language):
   - **Goal** (one sentence)
   - **The failure** this branch fixes, with one real before/after example from the dataset (question, what was retrieved before, what is retrieved now)
   - **The idea** (a short, intuitive explanation, one small diagram or code snippet at most)
   - **What changed** (files and the `git diff` command to view it)
   - **Run it** (exact commands)
   - **Results** (the table row for this branch and what it means, including anything that got worse)
   - **Gotchas / trade-offs** (cost, latency, failure modes)
   - **Exercises** (2–3)
   - **Further reading** (named papers/posts; only include a URL you have actually verified exists, never invent links)
5. `README.md` updated: the static course map, a "You are here" line, the results table up to this branch (`eval/compare.py --markdown`), and quick-start. Keep the static part identical across branches to avoid merge noise.
6. The diff against the previous branch is focused and within the LOC budget.
7. Commit(s) made, `step-NN` tag placed.

## 12. Practical notes and pitfalls

- **Free-tier quota is the bottleneck.** Cache everything. Use `GEMINI_MODEL_FAST` for bulk. Batch where the task allows (08: many chunks per call; 07: one call per rerank). Implement in `llm.py`: minimum interval between calls from `GEMINI_RPM`, exponential backoff on 429/5xx, and a clear error when the daily quota is exhausted. If a full eval can't finish today, make runs **resumable** (the cache already does this) and tell me. Do not skip the judge or shrink the dataset silently.
- **Re-index when anything upstream changes**: embedding model, prefixes, chunking, contextualization. Include the relevant config values in the cache key and in the saved index metadata, and refuse to load a stale index.
- **Determinism:** temperature 0 for judge, rerank, query expansion, and contextualization. Generation may use a small temperature; fix it in config.
- **Normalization for eval matching:** lowercase, collapse whitespace, strip markdown emphasis characters. Document it in `eval/README.md`.
- **Never** let eval read anything not visible to the pipeline at query time. No peeking at `evidence` or `docs` fields inside `ask()`.
- Keep the printed output of `ask --show-context` clean and readable. It is the main classroom demo tool.

## 13. Execution order

1. **Preflight:** check Python, Ollama (`ollama pull <embed model>`), Gemini key; run `doctor` logic by hand; record verified model IDs, limits, and the embedding model's real context length. Report any blocker to me.
2. **Bootstrap `main`:** README skeleton, `.gitignore`, `.env.example`, `requirements.txt`, corpus, dataset, validator. Validate. Commit.
3. **Branches 01 → 10 in order**, finishing each §11 checklist before starting the next.
4. **Consistency pass:** if the corpus or dataset changed, merge forward through all branches and re-run all evals so the table is from one consistent dataset.
5. **Capstone (11)** and final README results table.
6. **Report back to me** with: the final results table (all branches × metrics), which techniques helped / didn't / hurt, total Gemini calls used, anything you changed from this spec and why, and any open issues.

## 14. Definition of done

- All branches exist, are linear, tagged, and runnable with the same commands.
- Each branch's results table row reproduces from a clean checkout plus `.env`.
- Every lesson shows a real before/after from the dataset.
- The results table tells a truthful story: improvement where expected, and honest notes where not.
- A newcomer can clone, follow the README on `main`, and reach branch 05 in under an hour without asking anyone for help.
