"""
Document loader for the Quillstack corpus.
In branch 03, each document is split into structure-aware chunks (headings, code blocks, tables preserved)
with breadcrumb metadata prepended to embed_text.
"""

from pathlib import Path
from typing import List
from rag import chunk
from rag.schema import Chunk


def load_docs(docs_dir: Path) -> List[Chunk]:
    """
    Loads all .md files from docs_dir and splits them using structure-aware markdown parser.
    """
    chunks: List[Chunk] = []
    for doc_path in sorted(docs_dir.glob("*.md")):
        text = doc_path.read_text(encoding="utf-8").strip()
        doc_chunks = chunk.structure_aware_chunks(doc_path.name, text)
        chunks.extend(doc_chunks)
    return chunks
