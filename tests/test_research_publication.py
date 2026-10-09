import json
import tempfile
import unittest
from pathlib import Path

from tools.research_publication import load_publication, merge_publication_into_catalog


class ResearchPublicationTests(unittest.TestCase):
    def test_content_creator_rehearsal_fixture_is_not_public_catalog_content(self):
        fixture = json.loads((Path(__file__).parents[1] / "tests" / "fixtures" / "content_creator_publication_rehearsal.json").read_text(encoding="utf-8"))
        catalog = json.loads((Path(__file__).parents[1] / "embervault-catalog.json").read_text(encoding="utf-8"))
        self.assertEqual(catalog["content_projects"], [])
        self.assertEqual(fixture["application_state"], "design-only")
        self.assertFalse(fixture["live_game_files_touched"])

    def test_imports_mod_research_snapshot(self):
        records = load_publication(Path(__file__).parents[1] / "content/research/mod-research-publication-20261004.json")
        self.assertEqual(len(records), 11)
        self.assertTrue(all(record["reviewed"] for record in records))

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

    def test_merge_replaces_reviewed_records_without_private_fields(self):
        records = load_publication(Path(__file__).parents[1] / "content/research/mod-research-publication-20261004.json")
        catalog = {"generated_at": "2026-10-04", "research": [{"id": "old", "title": "Old"}]}
        merged = merge_publication_into_catalog(catalog, records)
        self.assertEqual(catalog["research"][0]["id"], "old")
        self.assertEqual(len(merged["research"]), 12)
        self.assertNotIn("evidence", merged["research"][-1])


if __name__ == "__main__":
    unittest.main()
