from pathlib import Path
from typing import Dict
from . import parse, sections as sec, citations, readability, claims, retrieve, nli, llm_judge, scoring, calibrate
from .schema import Report, Scores


def evaluate_file(pdf_path: str, paper_id: str, assets_dir: str = "assets") -> Report:
    pdf_path = str(pdf_path)
    full = parse.extract_text(pdf_path)
    sects: Dict[str, str] = parse.rough_section_split(full)


    # Deterministic scores
    s = Scores()
    s.structure = sec.score_structure(sects)
    s.readability = readability.score_readability(full)
    s.citations = citations.score_citations(full, sects)
    s.figs_tables = 0.6 # placeholder
    s.novelty = 0.5 # placeholder
    s.ethics_limits = 0.5 # placeholder


    # Claims → retrieval → NLI (stub)
    cs = claims.extract_claims(sects.get("abstract", ""), sects.get("conclusion", ""))
    retr = retrieve.SimpleRetriever([full])
    evidences = [retr.topk(c, k=1) for c in cs]
    s.nli_claims = nli.entailment_rate(cs, evidences)


    # LLM-as-judge (stub)
    s.methods_rubric = llm_judge.grade_methods(sects.get("methods", ""))
    s.results_rubric = llm_judge.grade_results(sects.get("results", ""))


    total = scoring.weighted_total(s)
    conf = calibrate.bootstrap_confidence()


    return Report(paper_id=paper_id, scores=s, weighted_total=total, confidence=conf)