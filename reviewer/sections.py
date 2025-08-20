from typing import Dict


EXPECTED = [
"abstract", "introduction", "related work", "methods",
"results", "discussion", "conclusion", "limitations", "references"
]


def score_structure(sections: Dict[str, str]) -> float:
    present = sum(1 for k in EXPECTED if sections.get(k, "").strip())
    return present / len(EXPECTED)