from typing import List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class SimpleRetriever:
    def __init__(self, passages: List[str]):
        self.passages = passages
        self.v = TfidfVectorizer(max_features=5000)
        self.X = self.v.fit_transform(passages)


    def topk(self, query: str, k: int = 3) -> List[str]:
        q = self.v.transform([query])
        sims = cosine_similarity(q, self.X)[0]
        idx = sims.argsort()[::-1][:k]
        return [self.passages[i] for i in idx]