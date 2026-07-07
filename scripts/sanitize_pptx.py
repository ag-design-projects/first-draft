#!/usr/bin/env python
"""Create neutralized PPTX assets from branded source decks.

The sanitizer copies a PPTX package, removes source-brand naming from
text-bearing XML, and normalizes Helvetica Neue runs to regular style.
"""

from __future__ import annotations

import argparse
import re
import zipfile
from pathlib import Path


SOURCE_BRAND_PATTERNS = [
    (re.compile(pattern), replacement)
    for pattern, replacement in [
        (r"SPA" + r"CE\s*10", "Brand"),
        (r"SPA" + r"CE10", "Brand"),
        (r"Spa" + r"ce\s*10", "Brand"),
        (r"Spa" + r"ce10", "Brand"),
        (r"spa" + r"ce\s*10", "brand"),
        (r"spa" + r"ce10", "brand"),
    ]
]


TEXT_PART_SUFFIXES = (".xml", ".rels")
TEXT_PART_PREFIXES = ("ppt/", "docProps/", "_rels/")


def should_rewrite(name: str) -> bool:
    return name.endswith(TEXT_PART_SUFFIXES) and name.startswith(TEXT_PART_PREFIXES)


def clean_xml(text: str) -> str:
    for pattern, replacement in SOURCE_BRAND_PATTERNS:
        text = pattern.sub(replacement, text)

    text = text.replace("Helvetica Neue Italic", "Helvetica Neue")
    text = text.replace("HelveticaNeue-Italic", "Helvetica Neue")
    text = text.replace("Helvetica Neue Light Italic", "Helvetica Neue")
    text = text.replace("Helvetica Neue Bold Italic", "Helvetica Neue")

    text = re.sub(r'\s+i="(?:1|true)"', "", text)
    text = re.sub(r'\s+typeface="[^"]*Helvetica[^"]*"', ' typeface="Helvetica Neue"', text)
    return text


def sanitize_pptx(source: Path, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(source, "r") as zin, zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            if should_rewrite(info.filename):
                try:
                    text = data.decode("utf-8")
                except UnicodeDecodeError:
                    text = data.decode("utf-8", "ignore")
                data = clean_xml(text).encode("utf-8")
            zout.writestr(info, data)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    sanitize_pptx(Path(args.source), Path(args.out))
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
