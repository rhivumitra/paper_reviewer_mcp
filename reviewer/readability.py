import re


def score_readability(text: str) -> float:
    # toy metric: inverse avg sentence length
    sents = re.split(r"[.!?]+\s", text)
    sents = [s for s in sents if s.strip()]
    if not sents:
        return 0.0
    avg_len = sum(len(s.split()) for s in sents) / len(sents)
    # map 10–40 words/sentence to 1.0–0.0
    return max(0.0, min(1.0, (40 - min(40, avg_len)) / 30))