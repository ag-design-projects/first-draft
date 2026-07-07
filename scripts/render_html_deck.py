#!/usr/bin/env python
"""Render a first-draft deck spec to a printable HTML deck."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path


def esc(value: object) -> str:
    return html.escape(str(value or ""))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    spec = json.loads(Path(args.spec).read_text(encoding="utf-8-sig"))
    brand = spec.get("brand", {})
    colors = brand.get("colors", {})
    fonts = brand.get("fonts", {})
    primary = colors.get("primary", "#111111")
    accent = colors.get("accent", "#0A66CC")
    bg = colors.get("background", "#FFFFFF")
    text = colors.get("text", "#111111")
    heading = fonts.get("heading", "Aptos Display, Arial, sans-serif")
    body_font = fonts.get("body", "Aptos, Arial, sans-serif")

    slides = []
    for index, slide in enumerate(spec.get("slides", []), start=1):
        bullets = "".join(f"<li>{esc(item)}</li>" for item in slide.get("body", []))
        evidence = "".join(
            f"<li>{esc(ev.get('source'))} {esc(ev.get('locator'))}: {esc(ev.get('claim'))}</li>"
            for ev in slide.get("evidence", [])
        )
        visual = slide.get("visual", {}) or {}
        visual_block = ""
        if visual.get("type") and visual.get("type") != "none":
            visual_block = f"<div class='visual'><strong>{esc(visual.get('type'))}</strong><br>{esc(visual.get('description'))}</div>"
        slides.append(f"""
<section class="slide">
  <div class="kicker">{esc(brand.get('name', ''))} / {index:02d}</div>
  <h1>{esc(slide.get('title'))}</h1>
  <div class="grid">
    <ul>{bullets}</ul>
    {visual_block}
  </div>
  <footer><ul>{evidence}</ul></footer>
</section>""")

    document = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(spec.get('title', 'First Draft Deck'))}</title>
<style>
@page {{ size: 16in 9in; margin: 0; }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; background: #ddd; color: {text}; font-family: {body_font}; }}
.slide {{ width: 16in; height: 9in; page-break-after: always; background: {bg}; padding: .65in .8in; position: relative; overflow: hidden; }}
.kicker {{ color: {accent}; font-size: 14pt; font-weight: 700; letter-spacing: .04em; text-transform: uppercase; }}
h1 {{ color: {primary}; font-family: {heading}; font-size: 34pt; line-height: 1.1; margin: .22in 0 .45in; max-width: 12.5in; }}
.grid {{ display: grid; grid-template-columns: 1.05fr .95fr; gap: .55in; align-items: start; }}
ul {{ margin: 0; padding-left: .28in; font-size: 19pt; line-height: 1.35; }}
li {{ margin-bottom: .16in; }}
.visual {{ border-left: .08in solid {accent}; background: rgba(0,0,0,.035); padding: .28in; font-size: 20pt; min-height: 3in; }}
footer {{ position: absolute; left: .8in; right: .8in; bottom: .38in; color: #666; font-size: 9pt; }}
footer ul {{ font-size: 9pt; line-height: 1.25; padding-left: .16in; }}
@media screen {{ .slide {{ margin: .25in auto; box-shadow: 0 6px 24px rgba(0,0,0,.16); }} }}
</style>
</head>
<body>
{''.join(slides)}
</body>
</html>
"""
    output = Path(args.out)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(document, encoding="utf-8")
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
