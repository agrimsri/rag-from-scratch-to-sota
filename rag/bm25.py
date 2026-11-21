"""
Handcrafted BM25 search engine with specialized identifier tokenization.
Preserves tokens like E-4417, v3.2.1, /dev/shm, etc.
Introduced in branch 05.
"""

import math
import re
from collections import Counter
from typing import Dict, List, Tuple


def tokenize(text: str) -> List[str]:
    """
    Tokenizes text while keeping identifiers intact.
    Emits both full identifiers (e.g. 'e-4417', 'v3.2.1') and their split subparts ('e', '4417').
    """
    text = text.lower()
    raw_tokens = re.findall(r"[a-z0-9_\-\./]+", text)
    tokens: List[str] = []
    for tok in raw_tokens:
        tok_clean = tok.strip(".-/")
        if not tok_clean:
            continue
        tokens.append(tok_clean)
        # Emit sub-tokens if composite identifier
        sub_tokens = re.findall(r"[a-z]+|[0-9]+", tok_clean)
        if len(sub_tokens) > 1:
            tokens.extend(sub_tokens)
    return tokens


class BM25Index:
    def __init__(self, corpus: List[str], k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.corpus_size = len(corpus)
        self.doc_lengths = []
        self.doc_freqs: Dict[str, int] = Counter()
        self.term_freqs: List[Counter] = []

        for text in corpus:
            tokens = tokenize(text)
            self.doc_lengths.append(len(tokens))
            counts = Counter(tokens)
            self.term_freqs.append(counts)
            for term in counts.keys():
                self.doc_freqs[term] += 1

        self.avg_dl = sum(self.doc_lengths) / max(self.corpus_size, 1)

    def score(self, query: str) -> List[Tuple[int, float]]:
        """Returns list of (doc_index, bm25_score) sorted descending by score."""
        query_terms = tokenize(query)
        scores = [0.0] * self.corpus_size

        for term in query_terms:
            df = self.doc_freqs.get(term, 0)
            if df == 0:
                continue
            # Standard Robertson-Spärck Jones BM25 IDF formula
            idf = math.log(1.0 + (self.corpus_size - df + 0.5) / (df + 0.5))

            for idx in range(self.corpus_size):
                tf = self.term_freqs[idx].get(term, 0)
                if tf == 0:
                    continue
                num = tf * (self.k1 + 1.0)
                den = tf + self.k1 * (1.0 - self.b + self.b * (self.doc_lengths[idx] / self.avg_dl))
                scores[idx] += idf * (num / den)

        ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
        return ranked
