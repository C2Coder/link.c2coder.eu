# link.c2coder.eu

Source for [link.c2coder.eu](https://link.c2coder.eu) - a custom styled linktreec clone, meant mainly to be scanned from a printed QR code. One tab
for the general (portfolio, GitHub, email), one for the
photography side (`photo.c2coder.eu`, Instagram). Built the same way as its
sibling sites, `c2coder.eu` and `photo.c2coder.eu` - a static site
from a small Python + Jinja2 generator, deployed to GitHub Pages.

## Layout

```
content/
  links.json     # site copy + both tabs' link lists
templates/
  index.html     # the only page
assets/          # favicon, CSS (copied into dist/ as-is)
build.py         # renders content/links.json through templates/index.html into dist/
```

## Content model

`content/links.json` has `site` (title, eyebrow, tagline), `shared` (footer
quote, GitHub link for the colophon), and `tabs` - a list of two tabs
(`main`, `photo`), each with a `label` and a `links` array. Each link is
`{ label, sublabel, url, icon }`, where `icon` is a key into the icon dict in
`build.py` (`external-link`, `github`, `mail`, `instagram`).
Adding, removing, or reordering links is a JSON-only change.

The photo tab's accent color (darkroom-red, matching `photo.c2coder.eu`) is
applied via a `data-tab="photo"` attribute on `<html>`, toggled by the tab
switcher in `templates/index.html`. Both tabs' markup is always present in the
rendered page - switching is a `hidden`-attribute toggle done in JS, so the
page is still fully readable with JS disabled.

## Build & run

Requires Python 3 and the packages in `requirements.txt` (`Jinja2`,
`livereload`).

```
make build       # renders content/links.json + templates/index.html -> dist/
make serve       # build once, then serve dist/ on :8002
make serve-live  # build + rebuild on every content/template/asset change, serve on :8002
```

Equivalent to `python build.py` / `python build.py --serve`.

## Deployment

Pushing to `main` runs `.github/workflows/pages.yml`, which builds the site and
publishes `dist/` to GitHub Pages. The custom domain (`link.c2coder.eu`) is set
via the `CNAME` file at the repo root, which `build.py` copies into `dist/` on
every build.
