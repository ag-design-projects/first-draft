#!/usr/bin/env python
"""Create a lightweight layout capacity catalog from a PPTX template."""

from __future__ import annotations

import argparse
import json
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


NS = {
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
}


def natural_key(value: str) -> list[object]:
    return [int(part) if part.isdigit() else part.lower() for part in re.split(r"(\d+)", value)]


def layout_record(name: str, xml: bytes) -> dict:
    root = ET.fromstring(xml)
    c_sld = root.find("p:cSld", NS)
    display_name = c_sld.attrib.get("name", Path(name).stem) if c_sld is not None else Path(name).stem
    placeholders = root.findall(".//p:ph", NS)
    text_shapes = root.findall(".//p:txBody", NS)
    pictures = root.findall(".//p:pic", NS)
    tables = root.findall(".//a:tbl", NS)
    charts = [node for node in root.iter() if node.tag.endswith("}chart")]
    all_text = " ".join(node.text or "" for node in root.iter())
    is_blank = "blank" in display_name.lower() or (not placeholders and not text_shapes and not pictures and not tables and not charts)
    variant = "dark" if re.search(r"\bwhite\b|light text", all_text, re.I) else "light"
    capacity = {
        "text_slots": max(len(text_shapes), len(placeholders)),
        "max_bullets": 5 if len(text_shapes) >= 2 else 3,
        "columns": 2 if len(text_shapes) >= 3 else 1,
        "has_image": bool(pictures),
        "has_table": bool(tables),
        "has_chart": bool(charts),
    }
    role_hints = []
    lower_name = display_name.lower()
    for key in ["title", "section", "quote", "image", "chart", "agenda", "closing", "divider"]:
        if key in lower_name:
            role_hints.append(key)
    return {
        "id": Path(name).stem,
        "name": display_name,
        "file": name,
        "variant": variant,
        "blank": is_blank,
        "fallback_only": is_blank,
        "role_hints": role_hints,
        "capacity": capacity,
    }


def catalog(source: Path) -> dict:
    with zipfile.ZipFile(source) as zf:
        layout_names = sorted(
            [n for n in zf.namelist() if re.match(r"ppt/slideLayouts/slideLayout\d+\.xml$", n)],
            key=natural_key,
        )
        layouts = [layout_record(name, zf.read(name)) for name in layout_names]
    return {
        "source_template": source.name,
        "layout_count": len(layouts),
        "font_default": "Helvetica Neue Regular",
        "rules": [
            "Choose a layout before rendering.",
            "If content exceeds layout capacity, split the beat across slides.",
            "Use image layouts only when imagery strengthens the claim.",
        ],
        "layouts": layouts,
    }


def write_markdown(data: dict, path: Path) -> None:
    lines = [
        f"# Layout Catalog - {data['source_template']}",
        "",
        f"- Layouts: {data['layout_count']}",
        f"- Default font: {data['font_default']}",
        "",
        "| ID | Name | Variant | Fallback only | Text slots | Bullets | Columns | Image | Hints |",
        "|---|---|---|---|---:|---:|---:|---|---|",
    ]
    for layout in data["layouts"]:
        cap = layout["capacity"]
        hints = ", ".join(layout["role_hints"]) or "-"
        lines.append(
            f"| {layout['id']} | {layout['name']} | {layout['variant']} | "
            f"{'yes' if layout['fallback_only'] else 'no'} | "
            f"{cap['text_slots']} | {cap['max_bullets']} | {cap['columns']} | "
            f"{'yes' if cap['has_image'] else 'no'} | {hints} |"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source")
    parser.add_argument("--json-out", required=True)
    parser.add_argument("--md-out")
    args = parser.parse_args()
    data = catalog(Path(args.source))
    json_path = Path(args.json_out)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    if args.md_out:
        write_markdown(data, Path(args.md_out))
    print(f"Wrote {json_path}")


if __name__ == "__main__":
    main()
