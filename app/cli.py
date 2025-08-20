import json
import click
from pathlib import Path
from reviewer.api import evaluate_file
from reviewer.report import write_json, write_html


@click.group()
def cli():
    pass


@cli.command()
@click.argument("pdf", type=click.Path(exists=True))
@click.option("--paper-id", required=False, default="paper", help="Identifier for outputs")
@click.option("--out", required=True, type=click.Path())
@click.option("--templates", default="assets/templates", show_default=True)
def evaluate(pdf, paper_id, out, templates):
    r = evaluate_file(pdf, paper_id)
    outdir = Path(out)
    write_json(r, outdir)
    write_html(r, Path(templates), outdir)
    click.echo(json.dumps({"paper_id": r.paper_id, "total": r.weighted_total}))


if __name__ == "__main__":
    cli()