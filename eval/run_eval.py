#!/usr/bin/env python3
"""
Evaluation harness computing retrieval, generation accuracy, faithfulness,
cost, and latency metrics across the evaluation dataset.
"""

import json
import re
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from rag import config, llm, pipeline
DATASET_PATH = REPO_ROOT / "eval" / "dataset.jsonl"
RESULTS_DIR = REPO_ROOT / "eval" / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def normalize_text(text: str) -> str:
    """Normalize text for matching: lowercase, strip markdown and extra whitespace."""
    text = text.lower()
    text = re.sub(r"[`*_#]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def check_answer_keys(answer: str, answer_keys: List[str]) -> bool:
    """
    Checks if all required answer keys are satisfied in the answer string.
    Keys can have alternatives separated by '|' (e.g. '30 days|thirty days').
    """
    norm_ans = normalize_text(answer)
    for key_pattern in answer_keys:
        alternatives = [normalize_text(alt) for alt in key_pattern.split("|")]
        if not any(alt in norm_ans for alt in alternatives if alt):
            return False
    return True


def check_evidence_in_hits(evidence_list: List[str], hits: List[Any], k: int = 5) -> Dict[str, Any]:
    """
    Evaluates retrieval recall, hit, and MRR against top-k hits.
    Checks chunk.text ONLY (never embed_text).
    """
    if not evidence_list:
        return {"recall": 1.0, "hit": 1.0, "mrr": 1.0}

    top_hits = hits[:k]
    matched_evidence = 0
    first_hit_rank = None

    for ev in evidence_list:
        norm_ev = normalize_text(ev)
        ev_found = False
        for rank, h in enumerate(top_hits, 1):
            if norm_ev in normalize_text(h.chunk.text):
                ev_found = True
                if first_hit_rank is None or rank < first_hit_rank:
                    first_hit_rank = rank
        if ev_found:
            matched_evidence += 1

    recall = matched_evidence / len(evidence_list)
    hit = 1.0 if matched_evidence > 0 else 0.0
    mrr = (1.0 / first_hit_rank) if first_hit_rank is not None else 0.0

    return {"recall": recall, "hit": hit, "mrr": mrr}


def judge_faithfulness(question: str, context: str, answer: str) -> bool:
    """Uses LLM judge to determine whether every claim in the answer is supported by the context."""
    prompt = (
        f"You are an impartial evaluation judge. Decide whether the following answer is fully supported "
        f"by the provided context. Answer in JSON with boolean key 'faithful'.\n\n"
        f"Context:\n{context}\n\n"
        f"Question:\n{question}\n\n"
        f"Answer:\n{answer}\n\n"
        f"JSON output:"
    )
    res = llm.generate_json(prompt)
    return bool(res.get("faithful", False))


def judge_abstention(question: str, answer: str) -> bool:
    """Determines whether the system correctly abstained when context lacked the answer."""
    norm = normalize_text(answer)
    abstain_signals = [
        "cannot answer",
        "do not have",
        "does not contain",
        "not mentioned",
        "insufficient information",
        "no information",
        "not provided",
        "unanswerable",
    ]
    return any(sig in norm for sig in abstain_signals)


def run_eval(
    split: str = "dev",
    retrieval_only: bool = False,
    judge: bool = False,
    no_rag: bool = False,
    limit: Optional[int] = None,
    output_filename: Optional[str] = None,
) -> Dict[str, Any]:
    # Load dataset
    questions = []
    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                q = json.loads(line)
                if q.get("split") == split:
                    questions.append(q)

    if limit is not None:
        questions = questions[:limit]

    print(f"\nRunning evaluation on {len(questions)} '{split}' questions (no_rag={no_rag}, retrieval_only={retrieval_only}, judge={judge})...")

    results_rows = []
    t0 = time.time()

    for idx, item in enumerate(questions, 1):
        q_id = item["id"]
        q_text = item["question"]
        q_cat = item["category"]
        is_answerable = item["answerable"]
        ev_list = item.get("evidence", [])
        keys = item.get("answer_keys", [])

        start_time = time.time()
        pipeline_res = pipeline.ask(q_text, no_rag=no_rag, retrieval_only=retrieval_only)
        latency = time.time() - start_time

        hits = pipeline_res.get("hits", [])
        answer = pipeline_res.get("answer", "")
        llm_calls = pipeline_res.get("llm_calls", 0)

        # Retrieval metrics
        ret_metrics = check_evidence_in_hits(ev_list, hits, k=5)

        # Context length
        context_chars = sum(len(h.chunk.text) for h in hits)

        # Answer accuracy
        if is_answerable:
            if retrieval_only:
                correct = False
            else:
                correct = check_answer_keys(answer, keys)
        else:
            # Unanswerable: correct if abstained
            correct = judge_abstention(q_text, answer)

        # Faithfulness
        is_faithful = None
        if judge and not retrieval_only and is_answerable:
            context_str = "\n\n".join(h.chunk.text for h in hits)
            is_faithful = judge_faithfulness(q_text, context_str, answer)

        row = {
            "id": q_id,
            "category": q_cat,
            "answerable": is_answerable,
            "recall@5": ret_metrics["recall"],
            "hit@5": ret_metrics["hit"],
            "mrr": ret_metrics["mrr"],
            "context_chars": context_chars,
            "correct": correct,
            "faithful": is_faithful,
            "llm_calls": llm_calls,
            "latency_s": latency,
            "answer": answer,
        }
        results_rows.append(row)
        print(f"[{idx}/{len(questions)}] {q_id} ({q_cat}): recall@5={row['recall@5']:.2f}, correct={row['correct']}, calls={llm_calls}")

    total_time = time.time() - t0

    # Aggregate metrics
    answerable_rows = [r for r in results_rows if r["answerable"]]
    unanswerable_rows = [r for r in results_rows if not r["answerable"]]

    avg_recall = sum(r["recall@5"] for r in answerable_rows) / max(len(answerable_rows), 1)
    avg_hit = sum(r["hit@5"] for r in answerable_rows) / max(len(answerable_rows), 1)
    avg_mrr = sum(r["mrr"] for r in answerable_rows) / max(len(answerable_rows), 1)
    avg_context = sum(r["context_chars"] for r in results_rows) / max(len(results_rows), 1)
    accuracy = sum(1 for r in results_rows if r["correct"]) / max(len(results_rows), 1)
    avg_calls = sum(r["llm_calls"] for r in results_rows) / max(len(results_rows), 1)
    avg_latency = total_time / max(len(results_rows), 1)

    faithful_evaluated = [r["faithful"] for r in results_rows if r["faithful"] is not None]
    faithfulness_rate = (sum(1 for f in faithful_evaluated if f) / len(faithful_evaluated)) if faithful_evaluated else None

    # Category breakdown
    categories = sorted(list(set(r["category"] for r in results_rows)))
    category_summary = {}
    for cat in categories:
        cat_rows = [r for r in results_rows if r["category"] == cat]
        cat_ans = [r for r in cat_rows if r["answerable"]]
        cat_recall = sum(r["recall@5"] for r in cat_ans) / max(len(cat_ans), 1) if cat_ans else 1.0
        cat_acc = sum(1 for r in cat_rows if r["correct"]) / max(len(cat_rows), 1)
        category_summary[cat] = {
            "count": len(cat_rows),
            "recall@5": round(cat_recall, 4),
            "accuracy": round(cat_acc, 4),
        }

    summary = {
        "split": split,
        "total_questions": len(results_rows),
        "recall@5": round(avg_recall, 4),
        "hit@5": round(avg_hit, 4),
        "mrr": round(avg_mrr, 4),
        "accuracy": round(accuracy, 4),
        "faithfulness": round(faithfulness_rate, 4) if faithfulness_rate is not None else None,
        "avg_context_chars": int(avg_context),
        "avg_llm_calls": round(avg_calls, 2),
        "avg_latency_s": round(avg_latency, 2),
        "total_time_s": round(total_time, 2),
        "by_category": category_summary,
        "rows": results_rows,
    }

    if output_filename:
        out_file = RESULTS_DIR / output_filename
    elif no_rag:
        out_file = RESULTS_DIR / "00-no-rag.json"
    else:
        out_file = RESULTS_DIR / "01-whole-doc.json"

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(f"\nSaved evaluation results to {out_file}")
    print(f"Summary: Recall@5={summary['recall@5']:.4f} | MRR={summary['mrr']:.4f} | Accuracy={summary['accuracy']:.4f} | Context={summary['avg_context_chars']} chars")
    return summary


def main(split="dev", retrieval_only=False, judge=False, no_rag=False, limit=None):
    run_eval(
        split=split,
        retrieval_only=retrieval_only,
        judge=judge,
        no_rag=no_rag,
        limit=limit,
    )


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--split", default="dev")
    parser.add_argument("--retrieval-only", action="store_true")
    parser.add_argument("--judge", action="store_true")
    parser.add_argument("--no-rag", action="store_true")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--output", type=str, default=None)
    args = parser.parse_args()
    run_eval(
        split=args.split,
        retrieval_only=args.retrieval_only,
        judge=args.judge,
        no_rag=args.no_rag,
        limit=args.limit,
        output_filename=args.output,
    )
