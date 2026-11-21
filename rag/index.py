"""
Vector index builder and persistence.
Saves embedding matrix and chunk metadata under .cache/index.pkl.
"""

import pickle
from pathlib import Path
from typing import Any, Dict, List
import numpy as np

from rag import embed, loader
from rag.schema import Chunk

CACHE_DIR = Path(__file__).resolve().parent.parent / ".cache"
INDEX_FILE = CACHE_DIR / "index.pkl"


def build_index(docs_dir: Path) -> Dict[str, Any]:
    """Loads chunks, computes normalized embeddings, and persists the index."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    chunks = loader.load_docs(docs_dir)
    print(f"Embedding {len(chunks)} documents...")
    vectors = embed.embed([c.embed_text for c in chunks], kind="doc")

    index_data = {
        "chunks": chunks,
        "vectors": vectors,
    }
    with open(INDEX_FILE, "wb") as f:
        pickle.dump(index_data, f)
    print(f"Index built and saved to {INDEX_FILE} ({len(chunks)} chunks, shape {vectors.shape})")
    return index_data


def load_index(docs_dir: Path) -> Dict[str, Any]:
    """Loads existing index from cache or builds a new one if missing."""
    if INDEX_FILE.exists():
        with open(INDEX_FILE, "rb") as f:
            return pickle.load(f)
    return build_index(docs_dir)
