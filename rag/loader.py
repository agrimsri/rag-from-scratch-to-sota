"""
Document loader for the Quillstack corpus.
In branch 02, each document is split into fixed-size character chunks with overlap.
"""

from pathlib import Path
from typing import List
from rag import chunk, config
from rag.schema import Chunk


def load_docs(docs_dir: Path) -> List[Chunk]:
    """
    Loads all .md files from docs_dir and splits them into fixed-size chunks.
    """
    chunks: List[Chunk] = []
    for doc_path in sorted(docs_dir.glob("*.md")):
        text = doc_path.read_text(encoding="utf-8").strip()
        sub_chunks = chunk.fixed_size_chunks(
            text,
            chunk_size=config.CHUNK_SIZE,
            overlap=config.CHUNK_OVERLAP,
        )
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
    return chunks
