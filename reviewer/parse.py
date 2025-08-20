# reviewer/parse.py
from typing import Dict, List, Tuple
import re
import fitz  # PyMuPDF

SECTION_KEYS = [
    "abstract", "introduction", "related work", "methods",
    "results", "discussion", "conclusion", "limitations", "references"
]

def extract_text(pdf_path: str) -> str:
    doc = fitz.open(pdf_path)
    text = []
    for page in doc:
        text.append(page.get_text())  # or page.get_text("text")
    return "\n".join(text)

def rough_section_split(full_text: str) -> Dict[str, str]:
    lower = full_text.lower()
    sections = {k: "" for k in SECTION_KEYS}

    # Find first occurrence of each heading using word boundaries
    indices: List[Tuple[int, str]] = []
    for k in SECTION_KEYS:
        m = re.search(rf"\b{k}\b", lower, flags=re.IGNORECASE)
        if m:
            indices.append((m.start(), k))

    indices.sort(key=lambda x: x[0])

    for idx, (pos, key) in enumerate(indices):
        end = indices[idx + 1][0] if idx + 1 < len(indices) else len(full_text)
        sections[key] = full_text[pos:end].strip()

    return sections
