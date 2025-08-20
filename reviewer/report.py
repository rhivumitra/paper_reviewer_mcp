from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from .schema import Report
import json


def write_json(report: Report, outdir: Path):
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "report.json").write_text(report.model_dump_json(indent=2), encoding="utf-8")


_def_env = None


def _env(templates_dir: Path):
    global _def_env
    if _def_env is None:
        _def_env = Environment(loader=FileSystemLoader(str(templates_dir)))
    return _def_env


def write_html(report: Report, templates_dir: Path, outdir: Path):
    env = _env(templates_dir)
    tpl = env.get_template("report.html.j2")
    html = tpl.render(r=report.model_dump())
    (outdir / "report.html").write_text(html, encoding="utf-8")