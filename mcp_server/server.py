from mcp.server.fastmcp import FastMCP
from reviewer.api import evaluate_file
from reviewer.schema import Report


mcp = FastMCP(name="PaperReviewer")


@mcp.tool()
def evaluate_paper(pdf_path: str, paper_id: str = "paper") -> dict:
"""Run evaluation and return a JSON-able dict."""
    r: Report = evaluate_file(pdf_path, paper_id)
    return r.model_dump()


@mcp.resource()
def review(paper_id: str):
# In a real app you would load from disk/cache by paper_id.
    return {"error": "not_implemented", "paper_id": paper_id}


if __name__ == "__main__":
    mcp.run()