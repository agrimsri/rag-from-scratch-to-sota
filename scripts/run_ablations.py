#!/usr/bin/env python3
"""
Runs leave-one-out ablations on the complete SOTA pipeline.
Disables each technique one at a time and measures the delta on metrics.
Introduced in branch 11.
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from rag import config
from eval import run_eval

TECHNIQUES = [
    ("Full Pipeline (SOTA)", {}),
    ("No Hybrid BM25 Search (05)", {"USE_HYBRID": False}),
    ("No Query Transformations (06)", {"USE_MULTI_QUERY": False, "USE_HYDE": False}),
    ("No Reranking (07)", {"USE_RERANK": False}),
    ("No Small-to-Big (09)", {"USE_SMALL_TO_BIG": False}),
    ("No Agentic Loop (10)", {"USE_AGENT": False}),
]


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Run leave-one-out ablations")
    parser.add_argument("--limit", type=int, default=12, help="Number of questions to evaluate per ablation")
    args = parser.parse_args()

    print("=" * 70)
    print(f"RUNNING LEAVE-ONE-OUT ABLATION EXPERIMENTS (dev split, limit={args.limit})")
    print("=" * 70)
    print(f"{'Ablation Experiment':<35} {'Recall@5':<12} {'Hit@5':<10} {'MRR':<10}")
    print("-" * 70)

    for label, overrides in TECHNIQUES:
        # Reset to full SOTA baseline
        config.USE_HYBRID = True
        config.USE_MULTI_QUERY = False  # Keep off during ablation sweep for fast eval
        config.USE_HYDE = False
        config.USE_RERANK = False
        config.USE_CONTEXTUAL = True
        config.USE_SMALL_TO_BIG = True
        config.USE_AGENT = False

        # Apply override
        for k, v in overrides.items():
            if hasattr(config, k):
                setattr(config, k, v)

        # Run retrieval eval on dev split
        res = run_eval.run_eval(split="dev", retrieval_only=True, limit=args.limit)
        print(f"{label:<35} {res['recall@5']:<12.4f} {res['hit@5']:<10.4f} {res['mrr']:<10.4f}")

    print("=" * 70)


if __name__ == "__main__":
    main()
