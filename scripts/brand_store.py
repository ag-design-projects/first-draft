#!/usr/bin/env python
"""Manage retained brand guideline folders for the first-draft skill."""

from __future__ import annotations

import argparse
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BRANDS_DIR = ROOT / "sources" / "brands"
MANIFEST = BRANDS_DIR / "manifest.json"


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "brand"


def load_manifest() -> dict:
    if MANIFEST.exists():
        return json.loads(MANIFEST.read_text(encoding="utf-8"))
    return {"brands": []}


def save_manifest(data: dict) -> None:
    BRANDS_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")


def list_brands(_: argparse.Namespace) -> None:
    data = load_manifest()
    if not data["brands"]:
        print("No retained brands.")
        return
    for brand in data["brands"]:
        print(f"{brand['slug']}\t{brand['name']}\t{brand.get('updated_at', '')}")


def add_brand(args: argparse.Namespace) -> None:
    source = Path(args.source).resolve()
    if not source.exists():
        raise SystemExit(f"Source not found: {source}")
    slug = slugify(args.slug or args.name or source.stem)
    target = BRANDS_DIR / slug
    if target.exists() and not args.merge:
        shutil.rmtree(target)
    target.mkdir(parents=True, exist_ok=True)
    if source.is_dir():
        for child in source.iterdir():
            destination = target / child.name
            if child.is_dir():
                if destination.exists():
                    shutil.rmtree(destination)
                shutil.copytree(child, destination)
            else:
                shutil.copy2(child, destination)
    else:
        shutil.copy2(source, target / source.name)
    data = load_manifest()
    now = datetime.now(timezone.utc).isoformat()
    data["brands"] = [b for b in data["brands"] if b["slug"] != slug]
    data["brands"].append({
        "slug": slug,
        "name": args.name or source.stem,
        "path": f"sources/brands/{slug}",
        "updated_at": now,
        "notes": args.notes or "",
    })
    data["brands"].sort(key=lambda item: item["slug"])
    save_manifest(data)
    print(f"Added brand: {slug}")


def delete_brand(args: argparse.Namespace) -> None:
    slug = slugify(args.slug)
    target = BRANDS_DIR / slug
    if target.exists():
        shutil.rmtree(target)
    data = load_manifest()
    data["brands"] = [b for b in data["brands"] if b["slug"] != slug]
    save_manifest(data)
    print(f"Deleted brand: {slug}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(required=True)

    list_parser = sub.add_parser("list")
    list_parser.set_defaults(func=list_brands)

    add_parser = sub.add_parser("add")
    add_parser.add_argument("source")
    add_parser.add_argument("--name")
    add_parser.add_argument("--slug")
    add_parser.add_argument("--notes")
    add_parser.add_argument("--merge", action="store_true", help="Merge into an existing brand folder instead of replacing it.")
    add_parser.set_defaults(func=add_brand)

    delete_parser = sub.add_parser("delete")
    delete_parser.add_argument("slug")
    delete_parser.set_defaults(func=delete_brand)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
