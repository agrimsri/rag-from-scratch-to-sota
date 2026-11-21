#!/usr/bin/env python3
"""
Validates the evaluation dataset against the corpus and specifications.
Checks:
1. Every evidence string occurs verbatim in the referenced corpus document (after whitespace collapse).
2. Category counts satisfy requirements (>= 5 per category in dev, adversarial >= 2).
3. Split counts satisfy dev (~45) and test (~15).
4. Unanswerable questions have answerable=False, empty evidence, and empty answer_keys.
5. Answerable questions have answerable=True, non-empty evidence, and non-empty answer_keys.
"""

import json
import re
import sys
from collections import Counter
from pathlib import Path

REQUIRED_DEV_CATEGORIES = [
    "lookup",
    "long-doc",
    "multi-chunk",
    "unanswerable",
    "exact",
    "paraphrase",
    "noisy-top-k",
    "context-dependent",
    "multi-hop",
    "adversarial",
]

MIN_COUNTS_DEV = {
    "lookup": 5,
    "long-doc": 5,
    "multi-chunk": 5,
    "unanswerable": 5,
    "exact": 5,
    "paraphrase": 5,
    "noisy-top-k": 5,
    "context-dependent": 5,
    "multi-hop": 5,
    "adversarial": 2,
}


def normalize_ws(text: str) -> str:
    """Collapse all whitespace sequences to a single space."""
    return re.sub(r"\s+", " ", text).strip()


def validate():
    repo_root = Path(__file__).resolve().parent.parent
    docs_dir = repo_root / "data" / "docs"
    dataset_file = repo_root / "eval" / "dataset.jsonl"

    if not docs_dir.exists():
        print(f"ERROR: Docs directory {docs_dir} not found.")
        sys.exit(1)

    if not dataset_file.exists():
        print(f"ERROR: Dataset file {dataset_file} not found.")
        sys.exit(1)

    # Load corpus documents
    docs = {}
    for doc_path in docs_dir.glob("*.md"):
        content = doc_path.read_text(encoding="utf-8")
        docs[doc_path.name] = {
            "raw": content,
            "norm": normalize_ws(content),
            "words": len(content.split()),
        }

    print(f"Loaded {len(docs)} corpus documents.")
    total_words = sum(d["words"] for d in docs.values())
    print(f"Total corpus word count: {total_words}")

    # Load questions
    questions = []
    with open(dataset_file, "r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                item = json.loads(line)
                item["_line"] = line_no
                questions.append(item)
            except Exception as e:
                print(f"ERROR: Line {line_no} is invalid JSON: {e}")
                sys.exit(1)

    print(f"Loaded {len(questions)} evaluation questions.")

    dev_q = [q for q in questions if q.get("split") == "dev"]
    test_q = [q for q in questions if q.get("split") == "test"]
    print(f"Split distribution: dev={len(dev_q)}, test={len(test_q)}")

    if len(dev_q) < 40:
        print(f"ERROR: Expected at least 40 dev questions, found {len(dev_q)}")
        sys.exit(1)
    if len(test_q) < 10:
        print(f"ERROR: Expected at least 10 test questions, found {len(test_q)}")
        sys.exit(1)

    dev_counts = Counter(q.get("category") for q in dev_q)
    print("\nDev category counts:")
    for cat in REQUIRED_DEV_CATEGORIES:
        count = dev_counts.get(cat, 0)
        req = MIN_COUNTS_DEV.get(cat, 5)
        status = "OK" if count >= req else "FAIL"
        print(f"  [{status}] {cat}: {count} (required: >={req})")
        if count < req:
            print(f"ERROR: Category {cat} has {count} questions in dev, needed {req}")
            sys.exit(1)

    # Check question validation & evidence matching
    errors = []
    seen_ids = set()

    for q in questions:
        qid = q.get("id")
        line = q.get("_line")
        if not qid:
            errors.append(f"Line {line}: missing question id")
            continue
        if qid in seen_ids:
            errors.append(f"Line {line}: duplicate question id '{qid}'")
        seen_ids.add(qid)

        is_answerable = q.get("answerable")
        evidence_list = q.get("evidence", [])
        answer_keys = q.get("answer_keys", [])
        q_docs = q.get("docs", [])

        if not is_answerable:
            if evidence_list:
                errors.append(f"[{qid}] unanswerable question has non-empty evidence")
            if answer_keys:
                errors.append(f"[{qid}] unanswerable question has non-empty answer_keys")
        else:
            if not evidence_list:
                errors.append(f"[{qid}] answerable question has empty evidence")
            if not answer_keys:
                errors.append(f"[{qid}] answerable question has empty answer_keys")
            if not q_docs:
                errors.append(f"[{qid}] answerable question has empty docs list")

            # Validate each evidence string is in at least one referenced doc
            for ev in evidence_list:
                ev_norm = normalize_ws(ev)
                found = False
                for doc_name in q_docs:
                    if doc_name not in docs:
                        errors.append(f"[{qid}] references unknown doc '{doc_name}'")
                        continue
                    if ev_norm in docs[doc_name]["norm"]:
                        found = True
                        break
                if not found:
                    errors.append(
                        f"[{qid}] evidence not found in referenced doc(s) {q_docs}:\n    '{ev}'"
                    )

    if errors:
        print(f"\nFound {len(errors)} validation errors:")
        for err in errors[:20]:
            print(f"  - {err}")
        if len(errors) > 20:
            print(f"  ... and {len(errors) - 20} more errors.")
        sys.exit(1)

    print("\n✓ Dataset validation passed! All evidence strings match verbatim.")


if __name__ == "__main__":
    validate()
