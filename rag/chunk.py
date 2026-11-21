"""
Structure-aware markdown chunking.
Splits by headings and paragraphs, preserving tables and fenced code blocks intact.
Maintains heading path metadata and prepends a breadcrumb to embed_text.
Introduced in branch 03.
"""

import re
from typing import Any, Dict, List
from rag.schema import Chunk


def _split_into_sections(text: str) -> List[Dict[str, Any]]:
    """Splits markdown text into hierarchical heading sections."""
    lines = text.split("\n")
    sections = []
    current_headings = []
    current_lines = []

    for line in lines:
        heading_match = re.match(r"^(#{1,4})\s+(.+)$", line)
        if heading_match:
            if current_lines:
                sec_text = "\n".join(current_lines).strip()
                if sec_text:
                    sections.append({
                        "heading_path": " > ".join(current_headings) if current_headings else "Overview",
                        "text": sec_text,
                    })
            level = len(heading_match.group(1))
            title = heading_match.group(2).strip()
            # Adjust heading stack
            current_headings = current_headings[: level - 1]
            current_headings.append(title)
            current_lines = [line]
        else:
            current_lines.append(line)

    if current_lines:
        sec_text = "\n".join(current_lines).strip()
        if sec_text:
            sections.append({
                "heading_path": " > ".join(current_headings) if current_headings else "Overview",
                "text": sec_text,
            })

    return sections


def structure_aware_chunks(doc_name: str, text: str, max_chunk_size: int = 1200) -> List[Chunk]:
    """
    Parses markdown document into structured chunks:
    - Never splits inside code blocks or tables
    - Splits oversized sections on double newlines
    - Stores heading path in meta and prepends breadcrumb to embed_text
    """
    sections = _split_into_sections(text)
    chunks: List[Chunk] = []
    chunk_idx = 0
    doc_title = doc_name.replace(".md", "").replace("-", " ").title()

    for sec in sections:
        sec_text = sec["text"]
        heading_path = sec["heading_path"]

        # If section is small enough, keep as single chunk
        if len(sec_text) <= max_chunk_size:
            breadcrumb = f"{doc_title} > {heading_path}"
            chunks.append(
                Chunk(
                    id=f"{doc_name}#{chunk_idx}",
                    doc=doc_name,
                    text=sec_text,
                    embed_text=f"[{breadcrumb}]\n{sec_text}",
                    meta={
                        "heading_path": heading_path,
                        "pos": chunk_idx,
                        "doc_title": doc_title,
                    },
                )
            )
            chunk_idx += 1
            continue

        # Oversized section: split on paragraph boundaries without breaking code/tables
        paragraphs = sec_text.split("\n\n")
        current_p_lines = []
        current_len = 0
        in_code_block = False

        for p in paragraphs:
            # Check if entering or exiting code block
            if "```" in p:
                count = p.count("```")
                if count % 2 == 1:
                    in_code_block = not in_code_block

            # Check if table block
            is_table = p.strip().startswith("|")

            if (current_len + len(p) > max_chunk_size) and not in_code_block and not is_table:
                if current_p_lines:
                    chunk_text = "\n\n".join(current_p_lines).strip()
                    breadcrumb = f"{doc_title} > {heading_path}"
                    chunks.append(
                        Chunk(
                            id=f"{doc_name}#{chunk_idx}",
                            doc=doc_name,
                            text=chunk_text,
                            embed_text=f"[{breadcrumb}]\n{chunk_text}",
                            meta={
                                "heading_path": heading_path,
                                "pos": chunk_idx,
                                "doc_title": doc_title,
                            },
                        )
                    )
                    chunk_idx += 1
                    current_p_lines = []
                    current_len = 0

            current_p_lines.append(p)
            current_len += len(p) + 2

        if current_p_lines:
            chunk_text = "\n\n".join(current_p_lines).strip()
            breadcrumb = f"{doc_title} > {heading_path}"
            chunks.append(
                Chunk(
                    id=f"{doc_name}#{chunk_idx}",
                    doc=doc_name,
                    text=chunk_text,
                    embed_text=f"[{breadcrumb}]\n{chunk_text}",
                    meta={
                        "heading_path": heading_path,
                        "pos": chunk_idx,
                        "doc_title": doc_title,
                    },
                )
            )
            chunk_idx += 1

    return chunks
