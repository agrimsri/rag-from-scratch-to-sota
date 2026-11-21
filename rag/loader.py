"""
Document loader for the Quillstack corpus.
In branch 01, each entire markdown document is loaded as exactly ONE Chunk.
"""

from pathlib import Path
from typing import List
from rag.schema import Chunk


def load_docs(docs_dir: Path) -> List[Chunk]:
    """
    Loads all .md files from docs_dir.
    In branch 01, each document IS one Chunk.
    """
    chunks: List[Chunk] = []
    for doc_path in sorted(docs_dir.glob("*.md")):
        text = doc_path.read_text(encoding="utf-8").strip()
        chunks.append(
            Chunk(
                id=doc_path.name,
                doc=doc_path.name,
                text=text,
                embed_text=text,
                meta={"title": doc_path.stem, "length_chars": len(text)},
            )
        )
    return chunks
