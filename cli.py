#!/usr/bin/env python3
"""
Unified CLI for the RAG textbook pipeline.
Supports:
  python cli.py doctor
  python cli.py index
  python cli.py ask "<question>" [--show-context] [--no-rag]
  python cli.py eval [--split dev|test] [--retrieval-only] [--judge] [--no-rag] [--limit N]
"""

import argparse
import sys
from pathlib import Path

from rag import config, embed, index, llm, pipeline


def cmd_doctor():
    """Validates local environment, Ollama models, and Gemini API connectivity."""
    print("=== [Preflight Doctor] Checking Environment ===")
    print(f"Python version: {sys.version.split()[0]}")
    print(f"LLM Provider: {config.LLM_PROVIDER}")
    print(f"Embedding Model: {config.OLLAMA_EMBED_MODEL}")
    print(f"Ollama Host: {config.OLLAMA_HOST}")

    # 1. Test Ollama connectivity & list models
    try:
        import ollama
        client = ollama.Client(host=config.OLLAMA_HOST)
        tags = client.list()
        models = [m["name"] if isinstance(m, dict) else m.model for m in tags.get("models", [])]
        print(f"✓ Ollama reachable. Installed models: {', '.join(models)}")

        if any(config.OLLAMA_EMBED_MODEL in m for m in models):
            print(f"✓ Ollama embedding model '{config.OLLAMA_EMBED_MODEL}' is ready.")
        else:
            print(f"⚠ Warning: '{config.OLLAMA_EMBED_MODEL}' not found in Ollama models list.")

        if any(config.LLM_MODEL in m for m in models):
            print(f"✓ Ollama generation model '{config.LLM_MODEL}' is ready.")
    except Exception as e:
        print(f"✗ Ollama connection failed: {e}")
        sys.exit(1)

    # 2. Test Embedding
    print("\nTesting one embedding generation...")
    try:
        vec = embed.embed(["doctor preflight test"], kind="doc")
        print(f"✓ Embed successful: vector shape {vec.shape}, norm = {float(sum(vec[0]**2)):.4f}")
    except Exception as e:
        print(f"✗ Embedding failed: {e}")
        sys.exit(1)

    # 3. Test LLM generation
    print("\nTesting LLM generation...")
    try:
        res = llm.generate("Reply with exactly the word 'READY'.")
        print(f"✓ LLM response: {res.strip()}")
    except Exception as e:
        print(f"✗ LLM generation failed: {e}")
        sys.exit(1)

    # 4. Check Gemini if key present
    if config.GEMINI_API_KEY:
        print("\nChecking Gemini API credentials...")
        try:
            from google import genai
            g_client = genai.Client(api_key=config.GEMINI_API_KEY)
            m_list = [m.name for m in g_client.models.list()]
            print(f"✓ Gemini reachable. Total models found: {len(m_list)}")
        except Exception as e:
            print(f"⚠ Gemini API check failed: {e}")
    else:
        print("\nNote: GEMINI_API_KEY not configured. Running 100% locally with Ollama models.")

    print("\n✓ Preflight doctor passed completely.")


def cmd_index():
    """Builds and caches the vector index from data/docs/."""
    docs_dir = Path(__file__).resolve().parent / "data" / "docs"
    index.build_index(docs_dir)


def cmd_ask(question: str, show_context: bool = False, no_rag: bool = False):
    """Executes the pipeline on a single question and displays results."""
    result = pipeline.ask(question, no_rag=no_rag)

    print("\n" + "=" * 60)
    print(f"QUESTION: {question}")
    print("=" * 60)
    print(f"ANSWER:\n{result['answer']}")
    print("-" * 60)
    print(f"Citations: {', '.join(result['citations']) or 'None'}")
    print(f"Trace: {' -> '.join(result['trace'])}")
    print(f"LLM calls used: {result['llm_calls']}")

    if show_context and result["hits"]:
        print("\n--- RETRIEVED CONTEXT ---")
        for rank, hit in enumerate(result["hits"], 1):
            print(f"\n[Hit {rank} | Score: {hit.score:.4f} | Chunk ID: {hit.chunk.id}]")
            preview = hit.chunk.text[:300].replace("\n", " ")
            print(f"Text preview: {preview}...")
    print("=" * 60 + "\n")


def cmd_eval(args):
    """Delegates to eval.run_eval."""
    from eval import run_eval
    run_eval.main(
        split=args.split,
        retrieval_only=args.retrieval_only,
        judge=args.judge,
        no_rag=args.no_rag,
        limit=args.limit,
        output_filename=args.output,
    )


def main():
    parser = argparse.ArgumentParser(description="RAG Pipeline CLI")
    subparsers = parser.add_subparsers(dest="command")

    # doctor
    subparsers.add_parser("doctor", help="Check local environment and model connectivity")

    # index
    subparsers.add_parser("index", help="Build vector index from corpus")

    # ask
    ask_p = subparsers.add_parser("ask", help="Query the RAG pipeline")
    ask_p.add_argument("question", type=str, help="Question to ask")
    ask_p.add_argument("--show-context", action="store_true", help="Print retrieved passages and scores")
    ask_p.add_argument("--no-rag", action="store_true", help="Ask without retrieval (baseline test)")

    # eval
    eval_p = subparsers.add_parser("eval", help="Run evaluation harness")
    eval_p.add_argument("--split", choices=["dev", "test"], default="dev", help="Dataset split to evaluate")
    eval_p.add_argument("--retrieval-only", action="store_true", help="Run retrieval metrics only (zero LLM calls)")
    eval_p.add_argument("--judge", action="store_true", help="Run LLM faithfulness & abstention judge")
    eval_p.add_argument("--no-rag", action="store_true", help="Evaluate raw LLM without retrieval")
    eval_p.add_argument("--limit", type=int, default=None, help="Limit number of questions to evaluate")
    eval_p.add_argument("--output", type=str, default=None, help="Custom output filename for results")

    args = parser.parse_args()
    if args.command == "doctor":
        cmd_doctor()
    elif args.command == "index":
        cmd_index()
    elif args.command == "ask":
        cmd_ask(args.question, show_context=args.show_context, no_rag=args.no_rag)
    elif args.command == "eval":
        cmd_eval(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
