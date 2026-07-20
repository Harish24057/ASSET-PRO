import json
from pathlib import Path
from typing import List, Optional
from uuid import uuid4

try:
    from .models import Asset
except ImportError:  # pragma: no cover - supports running this file directly
    from models import Asset


class AssetManager:
    def __init__(self, storage_path: Optional[str | Path] = None) -> None:
        self.storage_path = Path(storage_path or Path(__file__).resolve().parent.parent / "assets.json")
        self._assets: List[Asset] = []
        self._load()

    def _load(self) -> None:
        if not self.storage_path.exists():
            self._assets = []
            return

        with self.storage_path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)

        self._assets = [Asset.from_dict(item) for item in data]

    def _save(self) -> None:
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        with self.storage_path.open("w", encoding="utf-8") as handle:
            json.dump([asset.to_dict() for asset in self._assets], handle, indent=2)

    def list_assets(self) -> List[Asset]:
        return list(self._assets)

    def add_asset(self, name: str, category: str, value: float, status: str = "active") -> Asset:
        asset = Asset(id=uuid4().hex[:8], name=name, category=category, value=value, status=status)
        self._assets.append(asset)
        self._save()
        return asset

    def get_asset(self, asset_id: str) -> Optional[Asset]:
        for asset in self._assets:
            if asset.id == asset_id:
                return asset
        return None

    def update_asset(self, asset_id: str, **updates) -> Optional[Asset]:
        asset = self.get_asset(asset_id)
        if asset is None:
            return None

        for key, value in updates.items():
            if hasattr(asset, key):
                setattr(asset, key, value)

        self._save()
        return asset

    def delete_asset(self, asset_id: str) -> bool:
        original_count = len(self._assets)
        self._assets = [asset for asset in self._assets if asset.id != asset_id]
        if len(self._assets) != original_count:
            self._save()
            return True
        return False
