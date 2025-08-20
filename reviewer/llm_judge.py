# reviewer/llm_judge.py
from typing import Dict, List
from dataclasses import dataclass
import math
from .schema import RubricScore, ResultsRubric
from . import nli  # reuse the same NLI

# Helper: map P(entailment) in [0,1] → discrete 0..5 with mild sharpening
def _p_to_0_5(p: float) -> int:
    # Optional shaping: emphasize confidence (gamma)
    gamma = 1.2
    shaped = p ** gamma
    return int(max(0, min(5, round(shaped * 5))))

# -------- Methods rubric via NLI --------

_METHODS_HYPOTHESES = {
    "repro":   "The methods section provides enough detail to reproduce the results, including datasets, code or links, and hyperparameters.",
    "design":  "The experimental design includes appropriate controls, baselines, and ablation studies.",
    "stats":   "The methods specify valid statistical procedures, including confidence intervals or standard errors and corrections for multiple comparisons when relevant.",
    "compute": "The paper reports compute details such as hardware, training time, and budget or carbon footprint.",
    "limits":  "The methods explicitly discuss limitations or assumptions that affect reproducibility or scope.",
}

def grade_methods(methods_text: str) -> RubricScore:
    if not methods_text.strip():
        return RubricScore()  # zeros
    pairs = [(hyp, methods_text) for hyp in _METHODS_HYPOTHESES.values()]
    probs = nli.score_pairs(pairs)  # P(entailment) per hypothesis
    keys = list(_METHODS_HYPOTHESES.keys())
    scores_0_5 = {k: _p_to_0_5(p) for k, p in zip(keys, probs)}
    comments = (
        "NLI-as-judge: scores derived from entailment of rubric statements against the Methods text."
    )
    return RubricScore(**scores_0_5, comments=comments)

# -------- Results/Discussion rubric via NLI --------

_RESULTS_HYPOTHESES = {
    "stats":    "The results correctly interpret statistical tests and avoid overstating significance.",
    "fairness": "Comparisons against baselines are fair and clearly described, with consistent settings.",
    "effect":   "Effect sizes or practical significance are reported or discussed, not only p-values.",
    "failures": "The paper analyzes failure cases or negative results and discusses why they occur.",
}

def grade_results(results_text: str) -> ResultsRubric:
    if not results_text.strip():
        return ResultsRubric()
    pairs = [(hyp, results_text) for hyp in _RESULTS_HYPOTHESES.values()]
    probs = nli.score_pairs(pairs)
    keys = list(_RESULTS_HYPOTHESES.keys())
    scores_0_5 = {k: _p_to_0_5(p) for k, p in zip(keys, probs)}
    comments = (
        "NLI-as-judge: scores derived from entailment of rubric statements against the Results/Discussion."
    )
    return ResultsRubric(**scores_0_5, comments=comments)
