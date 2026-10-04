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
