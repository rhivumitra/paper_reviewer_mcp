from pydantic import BaseModel, Field
from typing import Dict, Any, Optional


class RubricScore(BaseModel):
    repro: int = 0
    design: int = 0
    stats: int = 0
    compute: int = 0
    limits: int = 0
    comments: str = ""


class ResultsRubric(BaseModel):
    stats: int = 0
    fairness: int = 0
    effect: int = 0
    failures: int = 0
    comments: str = ""


class Scores(BaseModel):
    structure: float = 0.0
    readability: float = 0.0
    citations: float = 0.0
    nli_claims: float = 0.0
    figs_tables: float = 0.0
    novelty: float = 0.0
    ethics_limits: float = 0.0
    methods_rubric: RubricScore = Field(default_factory=RubricScore)
    results_rubric: ResultsRubric = Field(default_factory=ResultsRubric)


class Confidence(BaseModel):
    bootstrap_std: float = 0.0


class Report(BaseModel):
    paper_id: str
    meta: Dict[str, Any] = Field(default_factory=dict)
    scores: Scores = Field(default_factory=Scores)
    weighted_total: float = 0.0
    confidence: Confidence = Field(default_factory=Confidence)