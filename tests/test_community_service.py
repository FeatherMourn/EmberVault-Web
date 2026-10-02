import tempfile
import unittest
from pathlib import Path
from community_service import CommunityService


class CommunityServiceTests(unittest.TestCase):
    def test_submission_requires_moderator_approval(self):
        with tempfile.TemporaryDirectory() as temp:
            service = CommunityService(Path(temp))
            member = service.create_user("Member")
            moderator = service.create_user("Moderator", ["moderator"])
            submission = service.submit(member["id"], "mod", "A public mod")
            self.assertEqual(submission["status"], "submitted")
            approved = service.review(moderator["id"], submission["id"], "approve", "Reviewed public metadata")
            self.assertEqual(approved["status"], "approved")

    def test_suspended_user_cannot_submit_or_post(self):
        with tempfile.TemporaryDirectory() as temp:
            service = CommunityService(Path(temp)); user = service.create_user("Suspended")
            data = service._load(); data["users"][0]["status"] = "suspended"; service._save(data)
            with self.assertRaises(ValueError):
                service.submit(user["id"], "research", "Hidden")


if __name__ == "__main__":
    unittest.main()
