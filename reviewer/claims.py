from typing import List
import re


def extract_claims(abstract: str, conclusion: str) -> List[str]:
    source = f"{abstract}\n{conclusion}"
    sents = re.split(r"[.!?]+\s", source)
    claims = [s.strip() for s in sents if len(s.split()) >= 8]
    return claims[:10] # cap for speed