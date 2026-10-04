"""Read-only importer for sanitized Mod Research Web Catalog publications."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_publication(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    if payload.get("schema_version") != 1 or payload.get("publication") != "web-catalog":
        raise ValueError("unsupported research publication")
    records = payload.get("records")
    if not isinstance(records, list):
        raise ValueError("publication records must be a list")
    for record in records:
        required = {"id", "kind", "identity", "build_scope", "status", "confidence", "summary", "limitations", "evidence_count", "reviewed"}
        if not required.issubset(record) or not record["reviewed"]:
            raise ValueError("publication contains an incomplete or unreviewed record")
        if any(key in record for key in ("evidence", "source_path", "local_path", "profile_id")):
            raise ValueError("publication contains private evidence data")
    return sorted(records, key=lambda record: record["id"])


def merge_publication_into_catalog(catalog: dict[str, Any], records: list[dict[str, Any]]) -> dict[str, Any]:
    """Return a catalog copy with reviewed Research records replaced by publication data."""
    result = json.loads(json.dumps(catalog))
    incoming = {record["id"]: record for record in records}
    existing = {record["id"]: record for record in result["research"]}
    for record_id, record in incoming.items():
        prior = existing.get(record_id, {})
        existing[record_id] = {
            "id": record_id,
            "title": prior.get("title", record["identity"].get("finding", record["identity"].get("build", record_id))),
            "category": "Research",
            "summary": record["summary"][0] if record["summary"] else "",
            "content": record["summary"][0] if record["summary"] else "",
            "status": record["status"],
            "build_scope": record["build_scope"],
            "confidence": record["confidence"],
            "limitations": record["limitations"],
            "open_questions": record["open_questions"],
            "evidence_count": record["evidence_count"],
            "reviewed": True,
            "published_at": result["generated_at"],
            "version": 1,
        }
    result["research"] = sorted(existing.values(), key=lambda record: record["id"])
    return result
