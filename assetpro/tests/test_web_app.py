import json
import tempfile
import unittest
from pathlib import Path

from asset_pro.web import create_app


class WebAppTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.storage_path = Path(self.temp_dir.name) / "assets.json"
        self.app = create_app(storage_path=self.storage_path)
        self.client = self.app.test_client()

    def test_home_page_lists_assets(self) -> None:
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Asset Pro", response.data)

    def test_add_asset_via_form(self) -> None:
        response = self.client.post(
            "/assets",
            data={"name": "Laptop", "category": "IT", "value": "1200", "status": "active"},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Laptop", response.data)

        with self.storage_path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], "Laptop")


if __name__ == "__main__":
    unittest.main()
