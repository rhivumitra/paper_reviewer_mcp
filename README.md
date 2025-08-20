# Paper Reviewer (Barebones)


End-to-end scaffold for a research paper reviewer with deterministic checks + (later) local NLI & LLM-as-judge. Ships with an MCP wrapper.


## Usage
- `python -m app.cli evaluate <pdf> --out <dir>` → produces `report.json` and `report.html`.
- `python -m mcp_server.server` → exposes tools `evaluate_paper` and resource `review`.