import json
import tempfile
import unittest
from pathlib import Path

from tools.research_publication import load_publication


class ResearchPublicationTests(unittest.TestCase):
    def test_loads_reviewed_sanitized_publication(self):
        payload = {"schema_version": 1, "publication": "web-catalog", "records": [{
            "id": "finding-1", "kind": "recipe-schema", "identity": {}, "build_scope": ["1076226"],
            "status": "experimental", "confidence": "bounded", "summary": ["offline finding"],
            "limitations": ["runtime unverified"], "open_questions": [], "evidence_count": 1, "reviewed": True
        }]}
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "publication.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            self.assertEqual(load_publication(path)[0]["id"], "finding-1")

    def test_rejects_private_evidence_or_unreviewed_record(self):
        payload = {"schema_version": 1, "publication": "web-catalog", "records": [{"id": "bad", "reviewed": False, "evidence": ["private"]}]}
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "publication.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaises(ValueError):
                load_publication(path)


if __name__ == "__main__":
    unittest.main()
