"""
Fixed-size character chunking with sliding window overlap.
Introduced in branch 02.
"""

from typing import List


def fixed_size_chunks(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """
    Splits text into fixed-size character chunks with sliding window overlap.
    Guarantees no empty chunks.
    """
    if not text:
        return []
    if len(text) <= chunk_size:
        return [text]

    chunks = []
    step = max(1, chunk_size - overlap)
    start = 0
    text_len = len(text)

    while start < text_len:
        end = min(start + chunk_size, text_len)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end >= text_len:
            break
        start += step

    return chunks
