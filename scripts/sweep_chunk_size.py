#!/usr/bin/env python3
"""
Sweeps chunk size and overlap configurations to evaluate the precision/context tradeoff.
Runs in retrieval-only mode: free, zero LLM calls, deterministic.
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from rag import chunk, embed, index, retrieve
from eval import run_eval
from rag.schema import Chunk

CHUNK_SIZES = [500, 1000, 2000]
OVERLAPS = [0, 200]


def build_temp_index(docs_dir: Path, size: int, overlap: int):
    chunks = []
    for doc_path in sorted(docs_dir.glob("*.md")):
        text = doc_path.read_text(encoding="utf-8").strip()
        sub_chunks = chunk.fixed_size_chunks(text, chunk_size=size, overlap=overlap)
        for i, c_text in enumerate(sub_chunks):
            chunks.append(
                Chunk(
                    id=f"{doc_path.name}#{i}",
                    doc=doc_path.name,
                    text=c_text,
                    embed_text=c_text,
                    meta={"chunk_idx": i, "total_chunks": len(sub_chunks)},
                )
            )

    vectors = embed.embed([c.embed_text for c in chunks], kind="doc")
    return {"chunks": chunks, "vectors": vectors}


def main():
    docs_dir = REPO_ROOT / "data" / "docs"
    questions = []
    with open(REPO_ROOT / "eval" / "dataset.jsonl", "r", encoding="utf-8") as f:
        import json
        for line in f:
            if line.strip():
                q = json.loads(line)
                if q.get("split") == "dev" and q.get("answerable"):
                    questions.append(q)

    print("=" * 65)
    print(f"{'Chunk Size':<12} {'Overlap':<10} {'Recall@5':<12} {'Hit@5':<10} {'Avg Context Chars':<18}")
    print("=" * 65)

    for size in CHUNK_SIZES:
        for overlap in OVERLAPS:
            if overlap >= size:
                continue
            idx = build_temp_index(docs_dir, size, overlap)

            total_recall = 0.0
            total_hit = 0.0
            total_chars = 0

            for q in questions:
                hits = retrieve.retrieve(q["question"], idx, k=5)
                m = run_eval.check_evidence_in_hits(q.get("evidence", []), hits, k=5)
                total_recall += m["recall"]
                total_hit += m["hit"]
                total_chars += sum(len(h.chunk.text) for h in hits)

            n = len(questions)
            avg_recall = total_recall / n
            avg_hit = total_hit / n
            avg_chars = total_chars / n

            print(f"{size:<12} {overlap:<10} {avg_recall:<12.4f} {avg_hit:<10.4f} {int(avg_chars):<18}", flush=True)
    print("=" * 65, flush=True)


if __name__ == "__main__":
    main()
