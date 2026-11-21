#!/usr/bin/env python3
"""
Compares evaluation results across branches.
Emits a CLI table or Markdown table for README.md.
"""

import argparse
import json
from pathlib import Path

RESULTS_DIR = Path(__file__).resolve().parent / "results"

HEADER = [
    "Branch / Step",
    "Recall@5",
    "Hit@5",
    "MRR",
    "Accuracy",
    "Context Chars",
    "LLM Calls",
    "Latency (s)",
]


def load_all_results():
    results = {}
    if not RESULTS_DIR.exists():
        return results
    for p in sorted(RESULTS_DIR.glob("*.json")):
        try:
            with open(p, "r", encoding="utf-8") as f:
                data = json.load(f)
                results[p.stem] = data
        except Exception:
            pass
    return results


def format_table(results: dict, markdown: bool = False):
    rows = []
    for name, data in sorted(results.items()):
        row = [
            name,
            f"{data.get('recall@5', 0.0):.3f}",
            f"{data.get('hit@5', 0.0):.3f}",
            f"{data.get('mrr', 0.0):.3f}",
            f"{data.get('accuracy', 0.0):.3f}",
            str(data.get("avg_context_chars", 0)),
            f"{data.get('avg_llm_calls', 0.0):.1f}",
            f"{data.get('avg_latency_s', 0.0):.2f}",
        ]
        rows.append(row)

    if markdown:
        md = []
        md.append("| " + " | ".join(HEADER) + " |")
        md.append("| " + " | ".join(["---"] * len(HEADER)) + " |")
        for r in rows:
            md.append("| " + " | ".join(r) + " |")
        return "\n".join(md)
    else:
        # Simple ASCII table
        col_widths = [len(h) for h in HEADER]
        for r in rows:
            for i, val in enumerate(r):
                col_widths[i] = max(col_widths[i], len(val))

        lines = []
        fmt = "  ".join(f"{{:<{w}}}" for w in col_widths)
        lines.append(fmt.format(*HEADER))
        lines.append("  ".join("-" * w for w in col_widths))
        for r in rows:
            lines.append(fmt.format(*r))
        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Compare cross-branch eval results")
    parser.add_argument("--markdown", action="store_true", help="Print table in Markdown format")
    args = parser.parse_args()

    results = load_all_results()
    if not results:
        print("No evaluation results found in eval/results/.")
        return

    table_str = format_table(results, markdown=args.markdown)
    print(table_str)


if __name__ == "__main__":
    main()
