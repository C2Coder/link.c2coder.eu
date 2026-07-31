from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).resolve().parent
TEMPLATES = ROOT / "templates"
CONTENT = ROOT / "content"
DIST = ROOT / "dist"

_STROKE_ATTRS = 'fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"'

ICONS = {
    "external-link": (
        f'<svg viewBox="0 0 24 24" width="24" height="24" {_STROKE_ATTRS}>'
        '<path d="M14 4h6v6"/><path d="M20 4 10 14"/>'
        '<path d="M18 13v5a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h5"/></svg>'
    ),
    "github": (
        '<svg viewBox="0 0 16 16" width="24" height="24" fill="currentColor">'
        '<path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 '
        '0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 '
        '1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 '
        '0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 '
        '1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25 '
        '.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"/></svg>'
    ),
    "mail": (
        f'<svg viewBox="0 0 24 24" width="24" height="24" {_STROKE_ATTRS}>'
        '<rect x="3" y="5" width="18" height="14"/><path d="m3 7 9 6 9-6"/></svg>'
    ),
    "instagram": (
        f'<svg viewBox="0 0 24 24" width="24" height="24" {_STROKE_ATTRS}>'
        '<rect x="3" y="3" width="18" height="18"/><circle cx="12" cy="12" r="4.5"/><path d="M17.5 6.5h.01"/></svg>'
    ),
}


def load_json(name: str):
    with open(CONTENT / name, "r", encoding="utf-8") as handle:
        return json.load(handle)


def build() -> None:
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True, exist_ok=True)

    env = Environment(loader=FileSystemLoader(TEMPLATES))
    data = load_json("links.json")

    html = env.get_template("index.html").render(
        site=data["site"],
        shared=data["shared"],
        tabs=data["tabs"],
        icons=ICONS,
    )
    (DIST / "index.html").write_text(html, encoding="utf-8")

    c_name = ROOT / "CNAME"
    if c_name.exists():
        shutil.copy2(c_name, DIST / "CNAME")

    assets = ROOT / "assets"
    if assets.exists():
        shutil.copytree(assets, DIST / "assets", dirs_exist_ok=True)


def serve() -> None:
    from livereload import Server

    build()
    server = Server()
    server.watch(str(TEMPLATES / "*.html"), build)
    server.watch(str(CONTENT / "*.json"), build)
    server.watch(str(ROOT / "assets" / "**"), build)
    server.serve(root=str(DIST), host="0.0.0.0", port=8002)


if __name__ == "__main__":
    if "--serve" in sys.argv:
        serve()
    else:
        build()
