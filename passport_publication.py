"""Build sanitized, review-only Mod Package Passport summaries."""
from __future__ import annotations


PRIVATE_KEYS = {"files", "evidence", "source_path", "local_path", "backup_id", "approval_history"}


def sanitize_passport(passport: dict) -> dict:
    if not isinstance(passport, dict) or passport.get("runtime_approval") is not False:
        raise ValueError("Passport must be explicitly runtime-unapproved.")
    public = {
        "id": passport.get("id", "unknown"),
        "version": passport.get("version", "unknown"),
        "builds": list(passport.get("builds", [])),
        "targets": list(passport.get("targets", [])),
        "dependencies": list(passport.get("dependencies", [])),
        "settings_schema": passport.get("settings_schema", "unknown"),
        "compatibility_state": "review-required",
        "runtime_behavior": "unverified",
        "limitations": list(passport.get("runtime_limitations", [])),
        "backup_required": bool(passport.get("backup_required", False)),
        "reviewed": False,
        "public": False,
    }
    if PRIVATE_KEYS.intersection(public):
        raise ValueError("Sanitized Passport contains private fields.")
    return public
