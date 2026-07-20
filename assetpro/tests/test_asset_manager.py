import json
import tempfile
import unittest
from pathlib import Path

from asset_pro.manager import AssetManager


class AssetManagerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.storage_path = Path(self.temp_dir.name) / "assets.json"
        self.manager = AssetManager(storage_path=self.storage_path)

    def test_add_and_list_assets(self) -> None:
        asset = self.manager.add_asset("Laptop", "IT", 1200)
        self.assertEqual(asset.name, "Laptop")
        self.assertEqual(len(self.manager.list_assets()), 1)

    def test_update_and_delete_assets(self) -> None:
        asset = self.manager.add_asset("Car", "Vehicle", 30000)
        updated = self.manager.update_asset(asset.id, status="inactive")
        self.assertIsNotNone(updated)
        self.assertEqual(updated.status, "inactive")

        deleted = self.manager.delete_asset(asset.id)
        self.assertTrue(deleted)
        self.assertEqual(self.manager.list_assets(), [])

    def test_persists_to_json(self) -> None:
        self.manager.add_asset("Desk", "Furniture", 500)
        with self.storage_path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], "Desk")


if __name__ == "__main__":
    unittest.main()
