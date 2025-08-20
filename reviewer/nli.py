# reviewer/nli.py
from typing import List, Sequence, Tuple
import os, torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Try these in order if NLI_MODEL_ID is not set or fails
_MODEL_CANDIDATES = [
    os.getenv("NLI_MODEL_ID", "").strip() or None,
    "microsoft/deberta-v3-base-mnli",
    "facebook/bart-large-mnli",
    "roberta-large-mnli",
    "cross-encoder/nli-deberta-v3-base",
]
_MODEL_ID = None
_TOKENIZER = None
_MODEL = None

def _load_model():
    global _MODEL_ID, _TOKENIZER, _MODEL
    last_err = None
    for mid in [m for m in _MODEL_CANDIDATES if m]:
        try:
            tok = AutoTokenizer.from_pretrained(mid)
            mdl = AutoModelForSequenceClassification.from_pretrained(mid)
            _MODEL_ID, _TOKENIZER, _MODEL = mid, tok, mdl
            return
        except Exception as e:
            last_err = e
            continue
    raise RuntimeError(
        f"Failed to load any NLI model. Tried: {', '.join([m for m in _MODEL_CANDIDATES if m])}\nLast error: {last_err}"
    )

if _MODEL is None:
    _load_model()

_DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
_MODEL.to(_DEVICE).eval()

# Map labels safely
_LABELS = {int(i): lab.upper() for i, lab in _MODEL.config.id2label.items()}
_ENTAIL_IDX = next(i for i, lab in _LABELS.items() if lab.startswith("ENTAIL"))
_NEUTRAL_IDX = next(i for i, lab in _LABELS.items() if lab.startswith("NEUTRAL"))
_CONTRA_IDX = next(i for i, lab in _LABELS.items() if lab.startswith("CONTRAD"))

@torch.inference_mode()
def _nli_probs(premises: Sequence[str], hypotheses: Sequence[str], batch_size: int = 8):
    assert len(premises) == len(hypotheses), "premises and hypotheses must align"
    probs = []
    for i in range(0, len(premises), batch_size):
        batch_p = premises[i:i+batch_size]
        batch_h = hypotheses[i:i+batch_size]
        enc = _TOKENIZER(
            batch_p, batch_h, padding=True, truncation=True, max_length=512, return_tensors="pt"
        ).to(_DEVICE)
        logits = _MODEL(**enc).logits
        p = torch.softmax(logits, dim=-1)
        probs.append(p.detach().cpu())
    return torch.cat(probs, dim=0) if probs else torch.empty(0, len(_LABELS))

def score_pairs(pairs: Sequence[Tuple[str, str]]) -> List[float]:
    if not pairs:
        return []
    premises = [ev for _, ev in pairs]
    hypotheses = [cl for cl, _ in pairs]
    p = _nli_probs(premises, hypotheses)
    return p[:, _ENTAIL_IDX].tolist()

def entailment_rate(claims: List[str], evidences: List[List[str]], threshold: float = 0.6) -> float:
    if not claims:
        return 0.0
    passed = 0
    for claim, ev_list in zip(claims, evidences):
        if not ev_list:
            continue
        scores = score_pairs([(claim, ev) for ev in ev_list])
        if scores and max(scores) >= threshold:
            passed += 1
    return passed / len(claims)
