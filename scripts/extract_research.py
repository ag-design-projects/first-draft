#!/usr/bin/env python
"""Extract lightweight research notes from common upload formats."""

from __future__ import annotations

import argparse
import csv
import json
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree


TEXT_EXTS = {".txt", ".md", ".markdown", ".rst"}
CSV_EXTS = {".csv", ".tsv"}
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"}


def natural_key(value: str) -> list[object]:
    return [int(part) if part.isdigit() else part.lower() for part in re.split(r"(\d+)", value)]


def clean(text: str, limit: int = 12000) -> str:
    normalized = " ".join(text.replace("\x00", " ").split())
    return normalized[:limit]


def extract_pdf(path: Path) -> list[dict]:
    try:
        from pypdf import PdfReader
    except Exception as exc:
        return [{"locator": "", "text": "", "warning": f"pypdf unavailable: {exc}"}]
    notes = []
    reader = PdfReader(str(path))
    for index, page in enumerate(reader.pages, start=1):
        try:
            text = clean(page.extract_text() or "", 2500)
        except Exception as exc:
            text = ""
            notes.append({"locator": f"page {index}", "text": "", "warning": str(exc)})
        if text:
            notes.append({"locator": f"page {index}", "text": text})
    return notes


def extract_docx_like(path: Path, pattern: str) -> list[dict]:
    notes = []
    with zipfile.ZipFile(path) as archive:
        for name in sorted(archive.namelist(), key=natural_key):
            if not name.startswith(pattern) or not name.endswith(".xml"):
                continue
            xml = archive.read(name)
            root = ElementTree.fromstring(xml)
            pieces = [node.text for node in root.iter() if node.text]
            text = clean(" ".join(pieces), 3000)
            if text:
                notes.append({"locator": name, "text": text})
    return notes


def extract_csv(path: Path) -> list[dict]:
    delimiter = "\t" if path.suffix.lower() == ".tsv" else ","
    rows = []
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.reader(handle, delimiter=delimiter)
        for index, row in enumerate(reader):
            rows.append(row)
            if index >= 30:
                break
    preview = "\n".join(" | ".join(row) for row in rows)
    return [{"locator": "preview rows 1-31", "text": clean(preview, 5000)}]


def extract_file(path: Path) -> dict:
    suffix = path.suffix.lower()
    result = {"source": str(path), "kind": suffix.lstrip(".") or "unknown", "notes": []}
    try:
        if suffix == ".pdf":
            result["notes"] = extract_pdf(path)
        elif suffix == ".docx":
            result["notes"] = extract_docx_like(path, "word/")
        elif suffix == ".pptx":
            result["notes"] = extract_docx_like(path, "ppt/slides/")
        elif suffix in TEXT_EXTS:
            result["notes"] = [{"locator": "file", "text": clean(path.read_text(encoding="utf-8", errors="replace"))}]
        elif suffix in CSV_EXTS:
            result["notes"] = extract_csv(path)
        elif suffix in IMAGE_EXTS:
            result["notes"] = [{"locator": "file", "text": "", "warning": "Image file retained as visual source; inspect visually or OCR if needed."}]
        else:
            result["notes"] = [{"locator": "file", "text": "", "warning": "Unsupported extension; inspect manually."}]
    except Exception as exc:
        result["notes"] = [{"locator": "file", "text": "", "warning": str(exc)}]
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="+")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    payload = {"sources": [extract_file(Path(file).resolve()) for file in args.files]}
    output = Path(args.out)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
