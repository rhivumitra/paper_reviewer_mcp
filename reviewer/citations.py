# reviewer/citations.py
import re
from typing import Dict

# Numeric citations like [1], [12], [1,2,3]
NUMERIC_BRACKETS = r"\[(?:\d+(?:\s*[,–-]\s*\d+)*)\]"
# Author-year like (Smith, 2020) or [Smith 2020]
AUTHOR_YEAR_PAREN = r"\([A-Z][A-Za-z-]+(?:\s+et al\.)?,?\s+\d{4}[a-z]?\)"
AUTHOR_YEAR_BRACK = r"\[[A-Z][A-Za-z-]+(?:\s+et al\.)?,?\s+\d{4}[a-z]?\]"

CITATION_RE = re.compile(
    rf"(?:{NUMERIC_BRACKETS}|{AUTHOR_YEAR_PAREN}|{AUTHOR_YEAR_BRACK})",
    flags=re.IGNORECASE
)

def score_citations(text: str, sections: Dict[str, str]) -> float:
    hits = len(CITATION_RE.findall(text))
    words = max(1, len(text.split()))
    density = hits / words  # tiny
    # Scale: ~0–1 (tweak as you like)
    return min(1.0, density * 200)
