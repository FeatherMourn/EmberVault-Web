"""Import a sanitized Mod Research publication into the public catalog."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from research_publication import load_publication, merge_publication_into_catalog


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("publication", type=Path)
    parser.add_argument("--catalog", type=Path, default=Path("embervault-catalog.json"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    output = args.output or args.catalog
    records = load_publication(args.publication)
    catalog = json.loads(args.catalog.read_text(encoding="utf-8"))
    merged = merge_publication_into_catalog(catalog, records)
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(output.suffix + ".tmp")
    temporary.write_text(json.dumps(merged, indent=2) + "\n", encoding="utf-8")
    temporary.replace(output)
    print(f"imported {len(records)} reviewed research records into {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
