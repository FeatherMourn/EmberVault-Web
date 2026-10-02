"""Verify the dependency-free public site and its privacy boundary."""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def validate() -> None:
    required_assets = ("index.html", "site.css", "site.js", "embervault-catalog.json", "content/community.json")
    missing = [name for name in required_assets if not (ROOT / name).is_file()]
    if missing:
        raise ValueError(f"Missing public site assets: {', '.join(missing)}")
    catalog = json.loads((ROOT / "embervault-catalog.json").read_text(encoding="utf-8"))
    if "profile_id" in json.dumps(catalog) or "local_path" in json.dumps(catalog) or "evidence_text" in json.dumps(catalog):
        raise ValueError("Public catalog contains a private field")
    community = json.loads((ROOT / "schemas" / "community.schema.json").read_text(encoding="utf-8"))
    if set(community["properties"]) != {"user", "submission", "forum_thread", "shared_project", "moderation_action"}:
        raise ValueError("Community schema is incomplete")
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    if "site.js" not in html or "embervault-catalog.json" not in (ROOT / "site.js").read_text(encoding="utf-8"):
        raise ValueError("Public site is not wired to the reviewed catalog")


if __name__ == "__main__":
    validate()
    print("Public site verification passed")
