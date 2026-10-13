import json
import unittest
from pathlib import Path

from passport_publication import sanitize_passport


class PassportPublicationTests(unittest.TestCase):
    def test_passport_summary_is_sanitized_and_not_public(self):
        source = json.loads((Path(__file__).parents[1].parent / "EmberVault-Mod-Research/research/external/SHROUDFORGE_PACKAGE_PASSPORT_FIXTURE_20261013.json").read_text())
        public = sanitize_passport(source)
        self.assertEqual(public["id"], "sf.example")
        self.assertFalse(public["reviewed"])
        self.assertFalse(public["public"])
        self.assertEqual(public["runtime_behavior"], "unverified")
        self.assertNotIn("files", public)
        self.assertNotIn("evidence", public)

    def test_runtime_approved_passport_is_rejected(self):
        with self.assertRaises(ValueError):
            sanitize_passport({"id": "unsafe", "runtime_approval": True})


if __name__ == "__main__":
    unittest.main()
