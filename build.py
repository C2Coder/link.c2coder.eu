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

ICONS = {
    "external-link": (
        '<path d="M14 4h6v6"/><path d="M20 4 10 14"/>'
        '<path d="M18 13v5a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h5"/>'
    ),
    "github": (
        '<path d="M9 19c-4.3 1.4-4.3-2.5-6-3m12 5v-3.5c0-1 .1-1.4-.5-2 '
        '1.7-.3 3.5-1.3 3.5-4.7 0-1.1-.4-2-.9-2.7.1-.3.4-1.4-.1-2.9 0 0-.9-.3-3 1a10.9 10.9 0 0 0-5.4 0c'
        '-2.1-1.3-3-1-3-1-.5 1.5-.2 2.6-.1 2.9C4.4 8.5 4 9.4 4 10.5 4 13.9 5.8 14.9 7.5 15.2c-.4.4-.6 1-.5 2V19"/>'
    ),
    "mail": '<rect x="3" y="5" width="18" height="14"/><path d="m3 7 9 6 9-6"/>',
    "aperture": (
        '<circle cx="12" cy="12" r="9"/>'
        '<path d="M14.3 8 19.9 17.8M9.7 8H21M7.3 12l5.7-9.9M9.7 16 4 6.1M14.3 16H3M16.6 12l-5.6 9.9"/>'
    ),
    "instagram": '<rect x="3" y="3" width="18" height="18"/><circle cx="12" cy="12" r="4.5"/><path d="M17.5 6.5h.01"/>',
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
