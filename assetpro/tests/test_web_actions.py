import tempfile
import unittest
from pathlib import Path

from asset_pro.web import create_app


class WebActionsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.storage_path = Path(self.temp_dir.name) / "assets.json"
        self.app = create_app(storage_path=self.storage_path)
        self.client = self.app.test_client()

    def test_update_and_delete_via_web_routes(self) -> None:
        self.client.post(
            "/assets",
            data={"name": "Laptop", "category": "IT", "value": "1200", "status": "active"},
            follow_redirects=True,
        )

        response = self.client.post(
            "/assets/1/update",
            data={"name": "Server", "category": "IT", "value": "5000", "status": "inactive"},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Server", response.data)

        delete_response = self.client.post("/assets/1/delete", follow_redirects=True)
        self.assertEqual(delete_response.status_code, 200)
        self.assertIn(b"No assets found.", delete_response.data)


if __name__ == "__main__":
    unittest.main()
