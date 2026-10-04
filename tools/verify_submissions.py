"""Pre-review checks for public Ember Vault contribution records."""
from __future__ import annotations

import json
from pathlib import Path

PRIVATE_MARKERS = ("password", "token", "secret", "c:\\users\\", "/users/", "\\appdata\\")


def check_public_text(path: Path) -> None:
    text = path.read_text(encoding="utf-8").lower()
    if any(marker in text for marker in PRIVATE_MARKERS):
        raise ValueError(f"Possible private data marker in {path}")


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors: list[str] = []
    for path in sorted((root / "content" / "mods").glob("*.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            if any(not isinstance(payload.get(key), str) or not payload[key].strip()
                   for key in ("id", "name", "version")):
                raise ValueError("mod record requires non-empty id, name, and version")
            check_public_text(path)
        except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
            errors.append(str(exc))
    for directory, required_markers in (("research", ("build", "hypothesis", "evidence")),
                                         ("knowledge", ("#",))):
        for path in sorted((root / "content" / directory).glob("*")):
            if path.is_file():
                try:
                    check_public_text(path)
                    text = path.read_text(encoding="utf-8").lower()
                    if any(marker not in text for marker in required_markers):
                        errors.append(f"{path} is missing required public metadata")
                except (OSError, UnicodeError, ValueError) as exc:
                    errors.append(str(exc))
    if errors:
        print("Submission validation failed:\n" + "\n".join(f"- {error}" for error in errors))
        return 1
    print("Submission validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
