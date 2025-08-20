from .schema import Scores


WEIGHTS = {
"structure": 0.10,
"readability": 0.10,
"citations": 0.10,
"nli_claims": 0.20,
"methods_rubric": 0.15,
"results_rubric": 0.15,
"figs_tables": 0.05,
"novelty": 0.10,
"ethics_limits": 0.05,
}


def rubric_to_float(d: dict) -> float:
    # naive: average of 0–5 items mapped to 0–1
    vals = [v for k, v in d.items() if isinstance(v, int)]
    return (sum(vals) / max(1, len(vals))) / 5


def weighted_total(s: Scores) -> float:
    total = 0.0
    total += s.structure * WEIGHTS["structure"]
    total += s.readability * WEIGHTS["readability"]
    total += s.citations * WEIGHTS["citations"]
    total += s.nli_claims * WEIGHTS["nli_claims"]
    total += rubric_to_float(s.methods_rubric.model_dump()) * WEIGHTS["methods_rubric"]
    total += rubric_to_float(s.results_rubric.model_dump()) * WEIGHTS["results_rubric"]
    total += s.figs_tables * WEIGHTS["figs_tables"]
    total += s.novelty * WEIGHTS["novelty"]
    total += s.ethics_limits * WEIGHTS["ethics_limits"]
    return round(total * 100, 1)